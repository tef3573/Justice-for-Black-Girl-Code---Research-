"""Audit whether the repository is ready to begin statistical modeling."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REQUIREMENTS = (
    ("focal cohort", "complete", "Age 15–23 person-age scaffold exists and is validated."),
    ("STEM coursework", "complete", "Public-use transcript coursework component is cleaned."),
    ("socioeconomic risk", "complete", "Ages 15–17 components and four-component-minimum composite are cleaned and validated."),
    ("neighborhood disinvestment", "blocked", "No public-use neighborhood or district identifier is currently available."),
    ("educational attainment", "complete", "Age-23 degree-first attainment hierarchy is cleaned and validated."),
    ("employment access", "complete", "Age-23 weekly labor-force status is cleaned with active military separated."),
    ("earnings", "complete", "Prior-year wage and self-employment routing, zeros, and 2025-dollar conversion are validated."),
    ("survey design", "blocked", "Choose longitudinal/transcript weights and document variance/design treatment."),
    ("attrition", "blocked", "Extract interview status and compare retained versus unavailable respondents."),
    ("class comparisons", "blocked", "Clean measures exist; final merged sample and weighted comparisons remain."),
    ("missing-data plan", "complete", "Mechanism-specific nonimputation, imputation, sensitivity, and ML leakage rules are documented."),
    ("analysis dataset", "complete", "Age-23 respondent merge, temporal ordering, keys, and outcome-specific eligibility flags are validated."),
)


def locate(root: Path, relative: str) -> Path | None:
    candidates = (root / relative, root / "docs" / relative)
    return next((path for path in candidates if path.exists()), None)


def audit(root: Path):
    required_files = {
        "age_panel": "data/interim/nlsy97_black_female_age15_23.csv",
        "stem_component": "data/processed/stem_transcript_clean.csv",
        "socioeconomic_risk": "data/processed/socioeconomic_risk_respondent.csv",
        "age23_outcomes": "data/processed/age23_outcomes.csv",
        "analysis_dataset": "data/processed/analysis_dataset.csv",
        "missing_data_plan": "docs/missing_data_plan.md",
        "research_design": "docs/research_design.md",
        "variable_dictionary": "docs/variables.json",
        "descriptive_report": "docs/preliminary_descriptive_report.md",
    }
    files = {name: locate(root, path) for name, path in required_files.items()}
    rows = []
    for construct, status, action in REQUIREMENTS:
        rows.append({"requirement": construct, "status": status, "required_action": action})
    summary = {
        "files": {name: str(path.relative_to(root)) if path else None for name, path in files.items()},
        "requirements_complete": sum(row["status"] == "complete" for row in rows),
        "requirements_blocked": sum(row["status"] == "blocked" for row in rows),
        "milestone_6_ready": False,
        "reason": "Core predictors, outcomes, merge, and missing-data rules are complete; survey design, attrition, and weighted comparisons remain incomplete.",
        "validation": "PASS",
    }
    if not all(files.values()):
        summary["validation"] = "FAIL: required repository artifact missing"
    return rows, summary


def build(root: Path, output: Path):
    rows, summary = audit(root)
    output.mkdir(parents=True, exist_ok=True)
    with (output / "model_readiness_matrix.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("requirement", "status", "required_action"))
        writer.writeheader()
        writer.writerows(rows)
    (output / "model_readiness_validation.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path("outputs/tables"))
    args = parser.parse_args()
    print(json.dumps(build(args.root.resolve(), args.output), indent=2))
