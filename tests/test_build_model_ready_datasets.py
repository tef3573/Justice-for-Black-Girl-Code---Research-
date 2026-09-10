import unittest
import pandas as pd

from build_model_ready_datasets import endpoint_frame


class ModelReadyTests(unittest.TestCase):
    def test_endpoint_normalizes_checkpoint_and_drops_unmatched(self):
        base = pd.DataFrame({
            "respondent_id": [1], "race_ethnicity_group": ["Black_non_Hispanic"],
            "race_gender_group": ["Black_non_Hispanic_women"], "transcript_collected": [1],
            "sampling_weight_cc_age25": [10], "vstrat_age25": [2], "vpsu_age25": [1],
            "survey_year_age25": [2007], "age25_record_matched": [1],
            "attainment_level_age25": [4], "employment_status_age25": ["employed"],
            "positive_labor_earnings_age25": [1], "labor_earnings_2025_dollars_age25": [20000],
        })
        imputed = pd.DataFrame({
            "respondent_id": [1], "imputation_id": [1],
            "socioeconomic_risk_index": [.2], "stem_coursework_rigor_index": [.3],
        })
        fields = ["attainment_level", "employment_status", "positive_labor_earnings",
                  "labor_earnings_2025_dollars"]
        result = endpoint_frame(base, imputed, fields, 25)
        self.assertEqual(result.loc[0, "checkpoint_age"], 25)
        self.assertEqual(result.loc[0, "attainment_level"], 4)
        self.assertEqual(result.loc[0, "eligible_earnings_part2_mi"], 1)


if __name__ == "__main__":
    unittest.main()
