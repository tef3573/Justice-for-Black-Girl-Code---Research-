import tempfile
import unittest
from pathlib import Path

from audit_model_readiness import audit


class ReadinessTests(unittest.TestCase):
    def test_finds_data_in_protected_docs_fallback(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ("research_design.md", "variables.json", "preliminary_descriptive_report.md"):
                (root / "docs").mkdir(exist_ok=True)
                (root / "docs" / name).touch()
            (root / "docs/data/interim").mkdir(parents=True)
            (root / "docs/data/processed").mkdir(parents=True)
            (root / "docs/data/interim/nlsy97_black_female_age15_23.csv").touch()
            (root / "docs/data/processed/stem_transcript_clean.csv").touch()
            (root / "docs/data/processed/socioeconomic_risk_respondent.csv").touch()
            (root / "docs/data/processed/age23_outcomes.csv").touch()
            (root / "docs/data/processed/analysis_dataset.csv").touch()
            (root / "docs/data/processed/imputed_predictors_long.csv").touch()
            (root / "docs/data/final").mkdir(parents=True)
            (root / "docs/data/final/model_ready_imputations_v1.csv.gz").touch()
            (root / "docs/data/final/analysis_base_complete_case_v1.csv.gz").touch()
            (root / "docs/outputs/tables").mkdir(parents=True)
            (root / "docs/outputs/tables/model_ready_freeze_manifest.json").touch()
            (root / "docs/missing_data_plan.md").touch()
            (root / "docs/imputation_report.md").touch()
            _, summary = audit(root)
            self.assertEqual(summary["validation"], "PASS")
            self.assertTrue(summary["milestone_6_ready"])
            self.assertEqual(summary["requirements_complete"], 11)

    def test_missing_artifact_fails_validation(self):
        with tempfile.TemporaryDirectory() as folder:
            _, summary = audit(Path(folder))
            self.assertTrue(summary["validation"].startswith("FAIL"))


if __name__ == "__main__":
    unittest.main()
