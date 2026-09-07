import unittest

from fit_two_part_earnings import PARTS, interpretation_scale


class TwoPartEarningsTests(unittest.TestCase):
    def test_parts_use_distinct_eligibility_flags(self):
        self.assertEqual(PARTS["positive_earnings"]["eligibility"], "eligible_earnings_part1_mi")
        self.assertEqual(PARTS["log_positive_earnings"]["eligibility"], "eligible_earnings_part2_mi")

    def test_logit_coefficient_is_odds_ratio(self):
        name, value = interpretation_scale("positive_earnings", 0.0)
        self.assertEqual(name, "odds_ratio")
        self.assertAlmostEqual(value, 1.0)

    def test_log_earnings_coefficient_is_exact_percent_difference(self):
        name, value = interpretation_scale("log_positive_earnings", 0.0)
        self.assertEqual(name, "percent_difference")
        self.assertAlmostEqual(value, 0.0)


if __name__ == "__main__":
    unittest.main()
