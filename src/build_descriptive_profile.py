"""Build preliminary unweighted sample-flow and missingness tables."""
import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


STATUS_FIELDS = (
    "math_pipeline_status",
    "physical_science_pipeline_status",
    "science_pipeline_status",
    "science_credits_status",
    "math_credits_status",
    "advanced_math_credits_status",
    "transcript_problem_flag_status",
)


def read_rows(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def percent(numerator, denominator):
    return round(100 * numerator / denominator, 1) if denominator else None


def summarize(panel, stem):
    panel_ids = {int(row["respondent_id"]) for row in panel}
    stem_by_id = {int(row["respondent_id"]): row for row in stem}
    if len(stem_by_id) != len(stem):
        raise ValueError("Duplicate respondent ID in transcript component")
    if len({(int(r["respondent_id"]), int(r["age"])) for r in panel}) != len(panel):
        raise ValueError("Duplicate respondent-age record in panel")
    if not panel_ids.issubset(stem_by_id):
        raise ValueError("Age-panel respondent missing from transcript component")

    age_counts = Counter(int(row["age"]) for row in panel)
    records_by_id = defaultdict(int)
    for row in panel:
        records_by_id[int(row["respondent_id"])] += 1

    focal_n = len(stem)
    eligible_n = len(panel_ids)
    transcript_n = sum(int(stem_by_id[pid]["transcript_collected"]) for pid in panel_ids)
    problem_n = sum(
        stem_by_id[pid]["transcript_problem_flag"] == "1"
        for pid in panel_ids
        if stem_by_id[pid]["transcript_collected"] == "1"
    )
    complete_n = sum(count == 9 for count in records_by_id.values())
    characteristics = [
        {"measure": "baseline_focal_respondents", "count": focal_n, "denominator": focal_n, "percent": 100.0},
        {"measure": "respondents_with_age_15_23_record", "count": eligible_n, "denominator": focal_n, "percent": percent(eligible_n, focal_n)},
        {"measure": "respondents_observed_at_all_nine_ages", "count": complete_n, "denominator": focal_n, "percent": percent(complete_n, focal_n)},
        {"measure": "age_eligible_respondents_with_collected_transcript", "count": transcript_n, "denominator": eligible_n, "percent": percent(transcript_n, eligible_n)},
        {"measure": "collected_transcripts_with_problem_flag", "count": problem_n, "denominator": transcript_n, "percent": percent(problem_n, transcript_n)},
    ]
    age_coverage = [
        {"age": age, "observed_respondents": age_counts[age], "denominator": focal_n,
         "percent_of_baseline_focal": percent(age_counts[age], focal_n)}
        for age in range(15, 24)
    ]

    missingness = []
    for field in STATUS_FIELDS:
        counts = Counter(stem_by_id[pid][field] for pid in panel_ids)
        for status, count in sorted(counts.items()):
            missingness.append({"variable": field.removesuffix("_status"), "status": status,
                                "count": count, "denominator": eligible_n,
                                "percent": percent(count, eligible_n)})
    validation = {
        "baseline_focal_respondents": focal_n,
        "age_eligible_respondents": eligible_n,
        "respondent_age_records": len(panel),
        "complete_age_trajectories": complete_n,
        "transcripts_collected_age_eligible": transcript_n,
        "transcript_problem_flags_age_eligible": problem_n,
        "weighting_status": "not available in current focused extract",
        "class_comparison_status": "not available until socioeconomic variables are cleaned",
        "analysis_status": "preliminary processing description; not substantive findings",
        "validation": "PASS",
    }
    return characteristics, age_coverage, missingness, validation


def build(panel_path, stem_path, output):
    characteristics, ages, missingness, validation = summarize(
        read_rows(panel_path), read_rows(stem_path)
    )
    write_csv(output / "preliminary_sample_characteristics.csv",
              ["measure", "count", "denominator", "percent"], characteristics)
    write_csv(output / "preliminary_age_coverage.csv",
              ["age", "observed_respondents", "denominator", "percent_of_baseline_focal"], ages)
    write_csv(output / "preliminary_stem_missingness.csv",
              ["variable", "status", "count", "denominator", "percent"], missingness)
    output.mkdir(parents=True, exist_ok=True)
    (output / "preliminary_descriptive_validation.json").write_text(
        json.dumps(validation, indent=2) + "\n", encoding="utf-8"
    )
    return validation


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", type=Path, default=Path("data/interim/nlsy97_black_female_age15_23.csv"))
    parser.add_argument("--stem", type=Path, default=Path("data/processed/stem_transcript_clean.csv"))
    parser.add_argument("--output", type=Path, default=Path("outputs/tables"))
    args = parser.parse_args()
    print(json.dumps(build(args.panel, args.stem, args.output), indent=2))
