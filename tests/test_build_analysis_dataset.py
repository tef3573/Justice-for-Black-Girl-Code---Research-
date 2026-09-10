import unittest

from build_analysis_dataset import add_checkpoint_weights, add_supplementary_checkpoints, eligible_flags, merge, missingness_tables


class AnalysisDatasetTests(unittest.TestCase):
    def base(self):
        return {
            "respondent_id": "1", "age": "23",
            "race_ethnicity_group": "Black_non_Hispanic",
            "race_gender_group": "Black_non_Hispanic_women",
            "attainment_level": "3", "employment_status": "employed",
            "positive_labor_earnings": "1", "labor_earnings_2025_dollars": "25000",
            "socioeconomic_risk_index": ".5", "transcript_collected": "1",
            "math_pipeline_level": "4", "science_pipeline_level": "3",
        }

    def test_outcome_specific_flags(self):
        flags = eligible_flags(self.base())
        self.assertTrue(all(flags.values()))
        row = self.base(); row["employment_status"] = "active_military"
        self.assertEqual(eligible_flags(row)["eligible_employment_complete_case"], 0)

    def test_part_two_requires_positive_exact_earnings(self):
        row = self.base(); row["labor_earnings_2025_dollars"] = ""
        flags = eligible_flags(row)
        self.assertEqual(flags["eligible_earnings_part1_complete_case"], 1)
        self.assertEqual(flags["eligible_earnings_part2_complete_case"], 0)

    def test_merge_rejects_demographic_mismatch(self):
        outcome = [self.base()]
        socio = {"1": {"respondent_id": "1", "race_ethnicity_group": "White_non_Hispanic",
                        "race_gender_group": "White_non_Hispanic_women"}}
        with self.assertRaises(ValueError):
            merge(outcome, socio, {})

    def test_missingness_is_group_specific(self):
        row = self.base(); row.update(eligible_flags(row))
        groups, patterns = missingness_tables([row])
        self.assertEqual(groups[0]["respondents"], 1)
        self.assertEqual(patterns[0]["missingness_pattern"], "complete_on_audited_fields")

    def test_supplementary_checkpoint_is_suffixed(self):
        row = self.base()
        checkpoint = dict(self.base(), age="25", attainment_level="4")
        add_supplementary_checkpoints([row], [checkpoint])
        self.assertEqual(row["age25_record_matched"], 1)
        self.assertEqual(row["attainment_level_age25"], "4")
        self.assertEqual(row["age24_record_matched"], 0)

    def test_checkpoint_weights_set_primary_design(self):
        row = self.base()
        weights = [{"respondent_id": "1", "age": str(age), "survey_year": "2005",
                    "sampling_weight_cc": "1000", "vstrat": "12", "vpsu": "1",
                    "rni_code": "60", "rni_category": "completed"}
                   for age in (23, 24, 25)]
        add_checkpoint_weights([row], weights)
        self.assertEqual(row["analysis_weight"], "1000")
        self.assertEqual(row["analysis_vstrat"], "12")
        self.assertEqual(row["sampling_weight_cc_age25"], "1000")


if __name__ == "__main__":
    unittest.main()
