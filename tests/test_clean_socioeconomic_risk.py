import unittest

from clean_socioeconomic_risk import assistance, clean_numeric, clean_parent_education, jobless, weighted_ranks


class SocioeconomicCleaningTests(unittest.TestCase):
    def test_poverty_scaling_and_missingness(self):
        self.assertEqual(clean_numeric("125", scale=100), (1.25, "observed"))
        self.assertEqual(clean_numeric("-3", scale=100), (None, "invalid_skip"))

    def test_valid_negative_income_preserved(self):
        self.assertEqual(clean_numeric("-6500", allow_negative=True), (-6500, "observed"))

    def test_parent_education(self):
        self.assertEqual(clean_parent_education(["12", "14", "-4", ""]), (14, 0, "observed"))
        self.assertEqual(clean_parent_education(["12", "11"]), (12, 1, "observed"))

    def test_assistance_requires_complete_no(self):
        self.assertEqual(assistance(["0", "1", "-4"]), (1, "observed_any"))
        self.assertEqual(assistance(["0", "0", "0"]), (0, "observed_none"))
        self.assertEqual(assistance(["0", "0", "-4"]), (None, "incomplete_parent_report"))

    def test_joblessness_routing(self):
        self.assertEqual(jobless("1", "-4", "-4")[0], 0)
        self.assertEqual(jobless("0", "0", "-4")[0], 1)
        self.assertEqual(jobless("0", "1", "1")[0], 0)
        self.assertEqual(jobless("0", "1", "0")[0], 1)

    def test_weighted_ranks_use_named_cross_sectional_weight(self):
        rows = [
            {"survey_year": 2001, "age": 16, "respondent_id": 1,
             "household_income": 10, "cross_sectional_weight_cc": 1},
            {"survey_year": 2001, "age": 16, "respondent_id": 2,
             "household_income": 20, "cross_sectional_weight_cc": 1},
        ]
        weighted_ranks(rows)
        self.assertEqual(rows[0]["household_income_rank"], 25.0)
        self.assertEqual(rows[1]["household_income_rank"], 75.0)


if __name__ == "__main__":
    unittest.main()
