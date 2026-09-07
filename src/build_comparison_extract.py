"""Build race-by-gender age panels and a raw socioeconomic extraction."""
from __future__ import annotations

import argparse
import csv
import io
import json
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

from build_core_cohort import read_metadata


BASE_NAMES = {
    "PUBID_1997", "KEY_SEX_1997", "KEY_ETHNICITY_1997", "KEY_RACE_1997",
    "KEY_RACE_ETHNICITY_1997", "CV_SAMPLE_TYPE_1997",
    "CV_HGC_BIO_DAD_1997", "CV_HGC_BIO_MOM_1997",
    "CV_HGC_RES_DAD_1997", "CV_HGC_RES_MOM_1997",
}
SOCIO_PREFIXES = (
    "CV_INCOME_GROSS_YR_", "CV_HH_POV_RATIO_", "CV_HH_SIZE_",
    "CV_INTERVIEW_CMONTH_", "CV_INTERVIEW_DATE_M_", "CV_INTERVIEW_DATE~M_",
    "CV_INTERVIEW_DATE_Y_", "CV_INTERVIEW_DATE~Y_", "SAMPLING_WEIGHT_",
    "SAMPLING_WEIGHT_CC_",
)


def race_ethnicity_group(ethnicity: int, race: int) -> str:
    if ethnicity == 1:
        return "Hispanic_any_race"
    if ethnicity != 0:
        return "unknown_race_ethnicity"
    return {
        1: "White_non_Hispanic",
        2: "Black_non_Hispanic",
        3: "American_Indian_Alaska_Native_non_Hispanic",
        4: "Asian_Pacific_Islander_non_Hispanic",
        5: "Other_race_non_Hispanic",
    }.get(race, "unknown_race_ethnicity")


def race_gender_group(ethnicity: int, race: int, sex: int) -> str:
    group = race_ethnicity_group(ethnicity, race)
    sex_label = {1: "men", 2: "women"}.get(sex, "unknown_sex")
    return f"{group}_{sex_label}"


def wanted(name: str) -> bool:
    if name in BASE_NAMES or name.startswith("CV_AGE_INT_DATE_"):
        return True
    if name.startswith(SOCIO_PREFIXES):
        year_text = name.rsplit("_", 1)[-1]
        return year_text.isdigit() and 1997 <= int(year_text) <= 2002
    return False


def construct(rows: list[dict[str, str]], age_fields: list[str]):
    panel_candidates = []
    demographics = {}
    for row in rows:
        pid = int(row["PUBID_1997"])
        if pid in demographics:
            raise ValueError("Duplicate respondent ID")
        sex = int(row["KEY_SEX_1997"])
        ethnicity = int(row["KEY_ETHNICITY_1997"])
        race = int(row["KEY_RACE_1997"])
        group = race_gender_group(ethnicity, race, sex)
        demographics[pid] = (sex, ethnicity, race, group)
        for round_no, field in enumerate(age_fields, 1):
            raw = row[field].strip()
            if not raw or int(raw) < 0:
                continue
            age = int(raw)
            if 15 <= age <= 23:
                panel_candidates.append({
                    "respondent_id": pid, "age": age, "survey_round": round_no,
                    "survey_year": int(field.rsplit("_", 1)[-1]),
                    "source_age_variable": field, "baseline_sex_code": sex,
                    "baseline_ethnicity_code": ethnicity, "baseline_race_code": race,
                    "race_ethnicity_group": race_ethnicity_group(ethnicity, race),
                    "race_gender_group": group,
                })
    grouped = defaultdict(list)
    for record in panel_candidates:
        grouped[(record["respondent_id"], record["age"])].append(record)
    panel = [max(records, key=lambda r: r["survey_round"])
             for _, records in sorted(grouped.items())]
    return panel, demographics


def write_csv(path: Path, rows: list[dict], fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fields or list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def build(source: Path, output: Path, reports: Path):
    with zipfile.ZipFile(source) as archive:
        r_member = next(n for n in archive.namelist() if n.endswith(".R"))
        csv_member = next(n for n in archive.namelist() if n.endswith(".csv"))
        refs, names = read_metadata(archive, r_member)
        selected = [(r, n) for r, n in zip(refs, names) if wanted(n)]
        with archive.open(csv_member) as raw:
            reader = csv.reader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""))
            positions = {ref: i for i, ref in enumerate(next(reader))}
            indexes = [(positions[ref], name) for ref, name in selected]
            rows = [{name: source_row[i] for i, name in indexes} for source_row in reader]

    age_fields = sorted((n for _, n in selected if n.startswith("CV_AGE_INT_DATE_")),
                        key=lambda n: int(n.rsplit("_", 1)[-1]))
    panel, demographics = construct(rows, age_fields)
    by_id_year = {(r["respondent_id"], r["survey_year"]): r for r in panel if 15 <= r["age"] <= 17}
    source_by_id = {int(r["PUBID_1997"]): r for r in rows}
    socio_fields = [n for _, n in selected if n in BASE_NAMES or n.startswith(SOCIO_PREFIXES)]
    socioeconomic = []
    for (pid, year), panel_row in sorted(by_id_year.items()):
        source_row = source_by_id[pid]
        record = {k: panel_row[k] for k in (
            "respondent_id", "age", "survey_round", "survey_year",
            "baseline_sex_code", "baseline_ethnicity_code", "baseline_race_code",
            "race_ethnicity_group", "race_gender_group")}
        for name in socio_fields:
            if name in BASE_NAMES or name.endswith(f"_{year}"):
                record[name] = source_row[name]
        socioeconomic.append(record)

    if len({(r["respondent_id"], r["age"]) for r in panel}) != len(panel):
        raise ValueError("Duplicate respondent-age panel key")
    if len({(r["respondent_id"], r["age"]) for r in socioeconomic}) != len(socioeconomic):
        raise ValueError("Duplicate socioeconomic respondent-age key")
    write_csv(output / "nlsy97_comparison_age15_23.csv", panel)
    write_csv(output / "nlsy97_socioeconomic_raw_age15_17.csv", socioeconomic,
              sorted({k for r in socioeconomic for k in r}, key=lambda x: (x not in socioeconomic[0], x)))
    summary = {
        "source_respondents": len(rows),
        "comparison_panel_respondents": len({r["respondent_id"] for r in panel}),
        "comparison_panel_records": len(panel),
        "socioeconomic_records_age15_17": len(socioeconomic),
        "socioeconomic_respondents_age15_17": len({r["respondent_id"] for r in socioeconomic}),
        "race_gender_counts_all_source": dict(sorted(Counter(v[3] for v in demographics.values()).items())),
        "race_gender_counts_panel": dict(sorted(Counter(
            next(v[3] for k, v in demographics.items() if k == pid)
            for pid in {r["respondent_id"] for r in panel}).items())),
        "selected_source_variables": len(selected),
        "status": "raw extraction complete; no socioeconomic cleaning or index construction",
        "unresolved": ["public-assistance routing", "household-adult joblessness construction", "final analytic weight"],
        "validation": "PASS",
    }
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "comparison_extraction_validation.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("data/raw/nlsy97_all_1997-2023.zip"))
    parser.add_argument("--output", type=Path, default=Path("data/interim"))
    parser.add_argument("--reports", type=Path, default=Path("outputs/tables"))
    args = parser.parse_args()
    print(json.dumps(build(args.source, args.output, args.reports), indent=2))
