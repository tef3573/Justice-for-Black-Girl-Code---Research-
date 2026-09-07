import unittest

from clean_stem_transcript import clean_credits, clean_flag, clean_pipeline, clean_record


class StemCleaningTests(unittest.TestCase):
    def test_math_pipeline_is_ordinal(self):
        self.assertEqual(clean_pipeline(600, set(range(100, 801, 100))), ("600", "6", "observed"))

    def test_science_zero_is_observed(self):
        self.assertEqual(clean_pipeline(0, set(range(0, 601, 100))), ("0", "0", "observed"))

    def test_no_course_is_zero_credits_but_flagged(self):
        self.assertEqual(clean_credits(-7), ("0.00", "no_course"))

    def test_missing_credits_are_not_zero(self):
        self.assertEqual(clean_credits(-6), ("", "credits_missing"))
        self.assertEqual(clean_credits(-8), ("", "invalid_or_pre_high_school"))

    def test_implied_decimals(self):
        self.assertEqual(clean_credits(375), ("3.75", "observed"))

    def test_negative_problem_flag_is_missing(self):
        self.assertEqual(clean_flag(-4), ("", "no_transcript"))

    def test_invalid_pipeline_value_rejected(self):
        with self.assertRaises(ValueError):
            clean_pipeline(650, set(range(0, 601, 100)))

    def test_status_and_problem_flag(self):
        raw = {"respondent_id": 1, "transcript_status": 1,
               "math_pipeline": 500, "physical_science_pipeline": 200,
               "science_pipeline": 400, "science_credits": 350,
               "math_credits": 425, "advanced_math_credits": -7,
               "transcript_problem_flag": 0}
        out = clean_record(raw)
        self.assertEqual(out["transcript_collected"], 1)
        self.assertEqual(out["math_credits"], "4.25")
        self.assertEqual(out["advanced_math_credits"], "0.00")


if __name__ == "__main__":
    unittest.main()
