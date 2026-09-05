"""Merge validated respondent-level components and audit analysis missingness."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


KEY = "respondent_id"
MISSING_FIELDS = (
    "socioeconomic_risk_index",
    "math_pipeline_level",
    "science_pipeline_level",
    "attainment_level",
    "employment_status",
    "positive_labor_earnings",
    "labor_earnings_2025_dollars",
)


def read_unique(path: Path) -> tuple[list[dict], dict[str, dict]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    indexed = {}
    for row in rows:
        pid = row[KEY]
        if pid in indexed:
            raise ValueError(f"Duplicate {KEY}={pid} in {path}")
        indexed[pid] = row
    return rows, indexed


def present(value) -> bool:
    return value is not None and value != ""


def eligible_flags(row: dict) -> dict[str, int]:
    exposure = present(row.get("socioeconomic_risk_index"))
    stem = (row.get("transcript_collected") == "1"
            and present(row.get("math_pipeline_level"))
            and present(row.get("science_pipeline_level")))
    common = exposure and stem
    civilian = row.get("employment_status") in {
        "employed", "unemployed", "not_in_labor_force"
    }
    positive_status = row.get("positive_labor_earnings") in {"0", "1"}
    real = row.get("labor_earnings_2025_dollars")
    return {
        "eligible_attainment_complete_case": int(common and present(row.get("attainment_level"))),
        "eligible_employment_complete_case": int(common and civilian),
        "eligible_earnings_part1_complete_case": int(common and positive_status),
        "eligible_earnings_part2_complete_case": int(
            common and row.get("positive_labor_earnings") == "1"
            and present(real) and float(real) > 0
        ),
    }


def merge(outcomes: list[dict], socioeconomic: dict[str, dict], stem: dict[str, dict]):
    merged = []
    for outcome in outcomes:
        pid = outcome[KEY]
        socio = socioeconomic.get(pid)
        course = stem.get(pid)
        row = dict(outcome)
        for source in (socio, course):
            if not source:
                continue
            for name, value in source.items():
                if name in (KEY, "race_ethnicity_group", "race_gender_group"):
                    continue
                if name in row:
                    raise ValueError(f"Unplanned duplicate column: {name}")
                row[name] = value
        row["socioeconomic_record_matched"] = int(socio is not None)
        row["stem_record_matched"] = int(course is not None)
        if socio and (socio["race_gender_group"] != row["race_gender_group"]
                      or socio["race_ethnicity_group"] != row["race_ethnicity_group"]):
            raise ValueError(f"Demographic mismatch for {pid} in socioeconomic data")
        row.update(eligible_flags(row))
        merged.append(row)
    return merged


def missingness_tables(rows: list[dict]):
    groups = defaultdict(list)
    for row in rows:
        groups[row["race_gender_group"]].append(row)
    by_group = []
    for group, members in sorted(groups.items()):
        record = {"race_gender_group": group, "respondents": len(members)}
        for field in MISSING_FIELDS:
            count = sum(not present(r.get(field)) for r in members)
            record[f"missing_{field}_n"] = count
            record[f"missing_{field}_pct"] = round(100 * count / len(members), 2)
        for flag in (
            "eligible_attainment_complete_case", "eligible_employment_complete_case",
            "eligible_earnings_part1_complete_case", "eligible_earnings_part2_complete_case",
        ):
            count = sum(int(r[flag]) for r in members)
            record[f"{flag}_n"] = count
            record[f"{flag}_pct"] = round(100 * count / len(members), 2)
        by_group.append(record)
    patterns = Counter()
    for row in rows:
        pattern = "|".join(field for field in MISSING_FIELDS if not present(row.get(field))) or "complete_on_audited_fields"
        patterns[pattern] += 1
    pattern_rows = [
        {"missingness_pattern": pattern, "respondents": count,
         "percent": round(100 * count / len(rows), 2)}
        for pattern, count in patterns.most_common()
    ]
    return by_group, pattern_rows


def write_csv(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def build(outcome_path: Path, socioeconomic_path: Path, stem_path: Path,
          output_path: Path, table_dir: Path):
    outcomes, _ = read_unique(outcome_path)
    _, socioeconomic = read_unique(socioeconomic_path)
    _, stem = read_unique(stem_path)
    rows = merge(outcomes, socioeconomic, stem)
    if any(int(r["age"]) != 23 for r in rows):
        raise ValueError("Outcome base includes records outside age 23")
    if any(int(r["observed_ages_15_17"]) < 1 or int(r["observed_ages_15_17"]) > 3
           for r in rows if r["socioeconomic_record_matched"]):
        raise ValueError("Socioeconomic exposure window failed temporal audit")
    by_group, patterns = missingness_tables(rows)
    write_csv(output_path, rows)
    write_csv(table_dir / "missingness_by_group.csv", by_group)
    write_csv(table_dir / "missingness_patterns.csv", patterns)
    flow = [
        {"stage": "observed_at_age_23", "respondents": len(rows)},
        {"stage": "socioeconomic_record_matched", "respondents": sum(r["socioeconomic_record_matched"] for r in rows)},
        {"stage": "socioeconomic_risk_index_observed", "respondents": sum(present(r.get("socioeconomic_risk_index")) for r in rows)},
        {"stage": "stem_record_matched", "respondents": sum(r["stem_record_matched"] for r in rows)},
        {"stage": "transcript_collected", "respondents": sum(r.get("transcript_collected") == "1" for r in rows)},
    ]
    for flag in (
        "eligible_attainment_complete_case", "eligible_employment_complete_case",
        "eligible_earnings_part1_complete_case", "eligible_earnings_part2_complete_case",
    ):
        flow.append({"stage": flag, "respondents": sum(r[flag] for r in rows)})
    write_csv(table_dir / "analysis_sample_flow.csv", flow)
    summary = {
        "base_age23_respondents": len(rows),
        "output_rows": len(rows),
        "unique_respondents": len({r[KEY] for r in rows}),
        "socioeconomic_records_matched": sum(r["socioeconomic_record_matched"] for r in rows),
        "stem_records_matched": sum(r["stem_record_matched"] for r in rows),
        "temporal_order": "socioeconomic exposures ages 15–17; transcript coursework during high school; outcomes observed/reported at age 23",
        "eligibility_counts": {r["stage"]: r["respondents"] for r in flow if r["stage"].startswith("eligible_")},
        "primary_row_policy": "retain every respondent observed at age 23; use outcome-specific eligibility flags",
        "validation": "PASS",
    }
    (table_dir / "analysis_merge_validation.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--outcomes", type=Path, default=Path("data/processed/age23_outcomes.csv"))
    p.add_argument("--socioeconomic", type=Path, default=Path("data/processed/socioeconomic_risk_respondent.csv"))
    p.add_argument("--stem", type=Path, default=Path("data/processed/stem_transcript_clean.csv"))
    p.add_argument("--output", type=Path, default=Path("data/processed/analysis_dataset.csv"))
    p.add_argument("--tables", type=Path, default=Path("outputs/tables"))
    a = p.parse_args()
    print(json.dumps(build(a.outcomes, a.socioeconomic, a.stem, a.output, a.tables), indent=2))
