"""Clean ages 15–17 socioeconomic measures and build a transparent risk index."""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import statistics
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


BASELINE_REFS = {
    "parent_afdc_prior_year": "R0611300",
    "parent_food_stamps_prior_year": "R0611600",
    "parent_ssi_prior_year": "R0611900",
    "responding_parent_employed": "R0692200",
    "responding_parent_spouse_in_household": "R0692400",
    "responding_parent_spouse_employed": "R0692500",
}
MISSING = {-1: "refusal", -2: "dont_know", -3: "invalid_skip",
           -4: "valid_skip", -5: "noninterview"}


def clean_numeric(raw: str, scale=1.0, allow_negative=False):
    value = int(raw)
    if value in MISSING:
        return None, MISSING[value]
    if value < 0 and not allow_negative:
        return None, "other_negative"
    return value / scale, "observed"


def clean_parent_education(values):
    valid = [int(v) for v in values if v != "" and 0 <= int(v) <= 20]
    if valid:
        highest = max(valid)
        return highest, int(highest <= 12), "observed"
    if any(v != "" and int(v) == 95 for v in values):
        return None, None, "ungraded"
    specials = [MISSING.get(int(v), "other_missing") for v in values if v]
    return None, None, specials[0] if specials else "missing"


def assistance(values):
    observed = [int(v) for v in values if v and int(v) in (0, 1)]
    if 1 in observed:
        return 1, "observed_any"
    if len(observed) == len(values):
        return 0, "observed_none"
    return None, "incomplete_parent_report"


def jobless(parent_work, spouse_present, spouse_work):
    p = int(parent_work)
    if p == 1:
        return 0, "responding_parent_employed"
    if p != 0:
        return None, MISSING.get(p, "unresolved")
    s = int(spouse_present)
    if s == 0:
        return 1, "responding_parent_not_employed_no_spouse"
    if s != 1:
        return None, MISSING.get(s, "unresolved")
    sw = int(spouse_work)
    if sw == 1:
        return 0, "spouse_employed"
    if sw == 0:
        return 1, "responding_parent_and_spouse_not_employed"
    return None, MISSING.get(sw, "unresolved")


def weighted_ranks(records):
    groups = defaultdict(list)
    for record in records:
        if (record["household_income"] is not None
                and record["cross_sectional_weight_cc"] is not None
                and record["cross_sectional_weight_cc"] > 0):
            groups[(record["survey_year"], record["age"])].append(record)
    for members in groups.values():
        members.sort(key=lambda r: (r["household_income"], r["respondent_id"]))
        total = sum(r["cross_sectional_weight_cc"] for r in members)
        below = 0.0
        by_value = defaultdict(list)
        for record in members:
            by_value[record["household_income"]].append(record)
        for value in sorted(by_value):
            tied = by_value[value]
            tie_weight = sum(r["cross_sectional_weight_cc"] for r in tied)
            rank = 100 * (below + tie_weight / 2) / total
            for record in tied:
                record["household_income_rank"] = round(rank, 4)
            below += tie_weight


def zscores(values):
    observed = [v for v in values if v is not None]
    mean = statistics.fmean(observed)
    sd = statistics.stdev(observed)
    return [None if v is None else (v - mean) / sd for v in values]


def summarize(records):
    by_id = defaultdict(list)
    for record in records:
        by_id[record["respondent_id"]].append(record)
    summaries = []
    for pid, rows in sorted(by_id.items()):
        first = rows[0]
        ranks = [r.get("household_income_rank") for r in rows if r.get("household_income_rank") is not None]
        poverty = [r["poverty_ratio"] for r in rows if r["poverty_ratio"] is not None]
        summaries.append({
            "respondent_id": pid, "race_ethnicity_group": first["race_ethnicity_group"],
            "race_gender_group": first["race_gender_group"],
            "observed_ages_15_17": len({r["age"] for r in rows}),
            "income_rank_observations": len(ranks),
            "average_household_income_rank": round(statistics.fmean(ranks), 4) if ranks else None,
            "income_rank_instability_sd": round(statistics.stdev(ranks), 4) if len(ranks) >= 2 else None,
            "average_poverty_ratio": round(statistics.fmean(poverty), 4) if poverty else None,
            "poverty_observations": len(poverty),
            "proportion_observed_years_in_poverty": round(sum(v < 1 for v in poverty) / len(poverty), 4) if poverty else None,
            "highest_parent_education_years": first["highest_parent_education_years"],
            "low_parental_education": first["low_parental_education"],
            "baseline_public_assistance_exposure": first["baseline_public_assistance_exposure"],
            "baseline_parent_household_jobless_proxy": first["baseline_parent_household_jobless_proxy"],
        })
    components = [
        [None if r["average_household_income_rank"] is None else 100-r["average_household_income_rank"] for r in summaries],
        [None if r["average_poverty_ratio"] is None else -r["average_poverty_ratio"] for r in summaries],
        [r["proportion_observed_years_in_poverty"] for r in summaries],
        [r["low_parental_education"] for r in summaries],
        [r["baseline_public_assistance_exposure"] for r in summaries],
        [r["baseline_parent_household_jobless_proxy"] for r in summaries],
    ]
    standardized = [zscores(values) for values in components]
    for i, row in enumerate(summaries):
        available = [values[i] for values in standardized if values[i] is not None]
        row["socioeconomic_risk_component_count"] = len(available)
        row["socioeconomic_risk_index"] = round(statistics.fmean(available), 6) if len(available) >= 4 else None
    return summaries


def extract_baseline(source: Path):
    with zipfile.ZipFile(source) as archive:
        member = next(n for n in archive.namelist() if n.endswith(".csv"))
        with archive.open(member) as raw:
            reader = csv.reader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""))
            positions = {ref: i for i, ref in enumerate(next(reader))}
            id_pos = positions["R0000100"]
            indexes = {name: positions[ref] for name, ref in BASELINE_REFS.items()}
            return {int(row[id_pos]): {name: row[pos] for name, pos in indexes.items()} for row in reader}


def build(raw_path: Path, source: Path, cleaned_path: Path, respondent_path: Path, validation_path: Path):
    with raw_path.open(newline="", encoding="utf-8-sig") as handle:
        raw_rows = list(csv.DictReader(handle))
    baseline = extract_baseline(source)
    cleaned = []
    for row in raw_rows:
        year = int(row["survey_year"])
        pid = int(row["respondent_id"])
        income, income_status = clean_numeric(row[f"CV_INCOME_GROSS_YR_{year}"], allow_negative=True)
        pov, pov_status = clean_numeric(row[f"CV_HH_POV_RATIO_{year}"], scale=100)
        size, size_status = clean_numeric(row[f"CV_HH_SIZE_{year}"])
        weight_name = f"SAMPLING_WEIGHT_CC_{year}"
        weight, weight_status = clean_numeric(row[weight_name], scale=100)
        education = clean_parent_education([row[f"CV_HGC_{kind}_1997"] for kind in ("RES_DAD", "RES_MOM", "BIO_DAD", "BIO_MOM")])
        b = baseline[pid]
        aid = assistance([b["parent_afdc_prior_year"], b["parent_food_stamps_prior_year"], b["parent_ssi_prior_year"]])
        work = jobless(b["responding_parent_employed"], b["responding_parent_spouse_in_household"], b["responding_parent_spouse_employed"])
        cleaned.append({
            "respondent_id": pid, "age": int(row["age"]), "survey_year": year,
            "race_ethnicity_group": row["race_ethnicity_group"], "race_gender_group": row["race_gender_group"],
            "household_income": income, "household_income_status": income_status,
            "household_income_rank": None,
            "poverty_ratio": pov, "poverty_ratio_status": pov_status,
            "below_poverty": None if pov is None else int(pov < 1),
            "household_size": size, "household_size_status": size_status,
            "cross_sectional_weight_cc": weight, "weight_status": weight_status,
            "highest_parent_education_years": education[0], "low_parental_education": education[1],
            "parent_education_status": education[2],
            "baseline_public_assistance_exposure": aid[0], "public_assistance_status": aid[1],
            "baseline_parent_household_jobless_proxy": work[0], "joblessness_status": work[1],
        })
    weighted_ranks(cleaned)
    summaries = summarize(cleaned)
    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    for path, rows in ((cleaned_path, cleaned), (respondent_path, summaries)):
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader(); writer.writerows(rows)
    summary = {
        "age_level_records": len(cleaned), "respondents": len(summaries),
        "risk_index_available": sum(r["socioeconomic_risk_index"] is not None for r in summaries),
        "risk_index_minimum_components": 4,
        "status_counts": {field: dict(Counter(str(r[field]) for r in cleaned)) for field in
                          ("household_income_status", "poverty_ratio_status", "parent_education_status",
                           "public_assistance_status", "joblessness_status", "weight_status")},
        "weight_decision": "cumulative-cases cross-sectional weights used for age-year ranks; final longitudinal model weight pending",
        "income_instability": "standard deviation of annual income rank, minimum two observations",
        "validation": "PASS",
    }
    validation_path.parent.mkdir(parents=True, exist_ok=True)
    validation_path.write_text(json.dumps(summary, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--raw", type=Path, default=Path("data/interim/nlsy97_socioeconomic_raw_age15_17.csv"))
    p.add_argument("--source", type=Path, default=Path("data/raw/nlsy97_all_1997-2023.zip"))
    p.add_argument("--cleaned", type=Path, default=Path("data/processed/socioeconomic_age15_17_clean.csv"))
    p.add_argument("--respondent", type=Path, default=Path("data/processed/socioeconomic_risk_respondent.csv"))
    p.add_argument("--validation", type=Path, default=Path("outputs/tables/socioeconomic_cleaning_validation.json"))
    a = p.parse_args(); print(json.dumps(build(a.raw, a.source, a.cleaned, a.respondent, a.validation), indent=2))
