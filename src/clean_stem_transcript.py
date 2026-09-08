"""Create a respondent-level clean STEM transcript component for the comparison cohort."""
from __future__ import annotations

import argparse
import csv
import io
import json
import zipfile
from collections import Counter
from pathlib import Path


REFERENCES = {
    "respondent_id": "R00001.00",
    "transcript_status": "R98596.00",
    "math_pipeline": "R98602.00",
    "physical_science_pipeline": "R98615.00",
    "science_pipeline": "R98617.00",
    "science_credits": "R98642.00",
    "math_credits": "R98643.00",
    "advanced_math_credits": "R98646.00",
    "transcript_problem_flag": "R98725.00",
}
PIPELINE_VALUES = {
    "math_pipeline": set(range(100, 801, 100)),
    "physical_science_pipeline": set(range(0, 201, 100)),
    "science_pipeline": set(range(0, 601, 100)),
}
CREDIT_FIELDS = ("science_credits", "math_credits", "advanced_math_credits")
SPECIAL = {-1: "refusal", -2: "dont_know", -3: "invalid_skip",
           -4: "no_transcript", -5: "noninterview", -6: "credits_missing",
           -7: "no_course", -8: "invalid_or_pre_high_school", -9: "other_missing",
           -10: "no_coursework"}


def normalize_reference(reference: str) -> str:
    return reference.replace(".", "")


def clean_pipeline(raw: int, allowed: set[int]) -> tuple[str, str, str]:
    if raw in allowed:
        return str(raw), str(raw // 100), "observed"
    if raw < 0:
        return "", "", SPECIAL.get(raw, "unmapped_special_code")
    raise ValueError(f"Unexpected pipeline value: {raw}")


def clean_credits(raw: int) -> tuple[str, str]:
    if raw >= 0:
        return f"{raw / 100:.2f}", "observed"
    if raw in (-7, -10):
        return "0.00", SPECIAL[raw]
    return "", SPECIAL.get(raw, "unmapped_special_code")


def clean_flag(raw: int) -> tuple[str, str]:
    if raw in (0, 1):
        return str(raw), "observed"
    if raw < 0:
        return "", SPECIAL.get(raw, "unmapped_special_code")
    raise ValueError(f"Unexpected flag value: {raw}")


def clean_record(raw: dict[str, int]) -> dict[str, str | int]:
    status = raw["transcript_status"]
    if status not in range(1, 12):
        raise ValueError(f"Unexpected transcript status: {status}")
    out: dict[str, str | int] = {
        "respondent_id": raw["respondent_id"],
        "transcript_status_code": status,
        "transcript_collected": int(status in (1, 2)),
        "transcript_collection_wave": status if status in (1, 2) else "",
    }
    for field, allowed in PIPELINE_VALUES.items():
        code, level, value_status = clean_pipeline(raw[field], allowed)
        out[f"{field}_code"] = code
        out[f"{field}_level"] = level
        out[f"{field}_status"] = value_status
    for field in CREDIT_FIELDS:
        value, value_status = clean_credits(raw[field])
        out[field] = value
        out[f"{field}_status"] = value_status
    flag, flag_status = clean_flag(raw["transcript_problem_flag"])
    out["transcript_problem_flag"] = flag
    out["transcript_problem_flag_status"] = flag_status
    return out


def extract(source: Path, cohort_ids: set[int]):
    with zipfile.ZipFile(source) as archive:
        member = next(name for name in archive.namelist() if name.endswith(".csv"))
        with archive.open(member) as raw_file:
            text = io.TextIOWrapper(raw_file, encoding="utf-8-sig", newline="")
            reader = csv.reader(text)
            positions = {name.strip('"'): i for i, name in enumerate(next(reader))}
            indexes = {name: positions[normalize_reference(ref)] for name, ref in REFERENCES.items()}
            seen = set()
            for row in reader:
                pid = int(row[indexes["respondent_id"]])
                if pid not in cohort_ids:
                    continue
                if pid in seen:
                    raise ValueError(f"Duplicate source respondent: {pid}")
                seen.add(pid)
                yield {name: int(row[index]) for name, index in indexes.items()}
    if seen != cohort_ids:
        raise ValueError(f"Missing {len(cohort_ids - seen)} cohort respondents from source")


def build(source: Path, cohort: Path, destination: Path, validation: Path) -> dict:
    with cohort.open(newline="", encoding="utf-8-sig") as f:
        cohort_ids = {int(r["respondent_id"]) for r in csv.DictReader(f)}
    cleaned = [clean_record(record) for record in extract(source, cohort_ids)]
    cleaned.sort(key=lambda r: int(r["respondent_id"]))
    if len(cleaned) != len(cohort_ids) or len({r["respondent_id"] for r in cleaned}) != len(cleaned):
        raise ValueError("Cleaned output does not contain one row per cohort respondent")
    if any(r["transcript_collected"] == 0 and r["math_pipeline_status"] == "observed"
           for r in cleaned):
        raise ValueError("Coursework present without a collected transcript")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(cleaned[0]))
        writer.writeheader()
        writer.writerows(cleaned)
    collected = [r for r in cleaned if r["transcript_collected"] == 1]
    summary = {
        "comparison_cohort_respondents": len(cleaned),
        "transcripts_collected": len(collected),
        "transcripts_not_collected": len(cleaned) - len(collected),
        "transcript_problem_flag_yes": sum(r["transcript_problem_flag"] == "1" for r in cleaned),
        "transcript_problem_flag_no": sum(r["transcript_problem_flag"] == "0" for r in cleaned),
        "status_counts": dict(sorted(Counter(str(r["transcript_status_code"]) for r in cleaned).items())),
        "field_status_counts": {field: dict(sorted(Counter(r[f"{field}_status"] for r in cleaned).items()))
                                for field in (*PIPELINE_VALUES, *CREDIT_FIELDS, "transcript_problem_flag")},
        "validation": "PASS",
        "interpretation": "Respondent-level transcript coursework component; not institutional STEM quality",
    }
    validation.parent.mkdir(parents=True, exist_ok=True)
    validation.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("data/raw/nlsy97_all_1997-2023.zip"))
    parser.add_argument("--cohort", type=Path, default=Path("data/interim/nlsy97_comparison_age15_23.csv"))
    parser.add_argument("--destination", type=Path, default=Path("data/processed/stem_transcript_clean.csv"))
    parser.add_argument("--validation", type=Path, default=Path("outputs/tables/stem_cleaning_validation.json"))
    args = parser.parse_args()
    print(json.dumps(build(args.source, args.cohort, args.destination, args.validation), indent=2))


if __name__ == "__main__":
    main()
