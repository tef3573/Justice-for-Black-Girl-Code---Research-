import unittest

from build_age23_outcomes import attainment, earnings, employment, routed_component, weekly_class


class Age23OutcomeTests(unittest.TestCase):
    def test_attainment_uses_degree_then_grade(self):
        self.assertEqual(attainment("16", "4", "1")[4], "bachelors_degree")
        self.assertEqual(attainment("14", "0", "10")[4], "some_college_no_degree")
        self.assertEqual(attainment("12", "0", "1")[4], "no_high_school_credential")
        self.assertEqual(attainment("12", "1", "1")[4], "high_school_equivalent_GED")
        self.assertEqual(attainment("14", "2", "1")[4], "some_college_no_degree")

    def test_postsecondary_enrollment(self):
        self.assertEqual(attainment("14", "0", "10")[5], 1)
        self.assertEqual(attainment("12", "2", "3")[5], 0)

    def test_employment_midmonth_and_proportions(self):
        weeks = ["5"] * 52
        weeks[24] = "10001"
        status, week, known, props = employment("6", "2004", weeks)
        self.assertEqual(week, 25)
        self.assertEqual(status, "employed")
        self.assertEqual(known, 52)
        self.assertAlmostEqual(props["employed"], 1 / 52)

    def test_ambiguous_not_working_is_not_forced(self):
        weeks = ["2"] * 52
        self.assertEqual(employment("1", "2005", weeks)[0], "indeterminate_not_working")

    def test_active_military_is_not_civilian_employment(self):
        self.assertEqual(weekly_class(6), "active_military")
        self.assertEqual(weekly_class(9701), "employed")

    def test_routed_zero_and_valid_negative_self_employment(self):
        self.assertEqual(routed_component("0", "-4", "-4")[0], 0)
        self.assertEqual(routed_component("1", "-1200", "-4", allow_negative=True)[0], -1200)

    def test_bracket_only_is_positive_without_exact_amount(self):
        self.assertEqual(routed_component("1", "-2", "3"), (None, 1, "bracket_only", 3))

    def test_total_earnings_and_cpi(self):
        values = {
            "wage_receipt": "1", "wage_amount": "10000", "wage_bracket": "-4",
            "wage_receipt_dk": "-4", "wage_receipt_rf": "-4",
            "self_receipt": "0", "self_amount": "-4", "self_bracket": "-4",
        }
        out = earnings(values, {2003: 184.0, 2025: 321.943}, 2004)
        self.assertEqual(out[2], 10000)
        self.assertEqual(out[3], 1)
        self.assertEqual(out[4], 2003)
        self.assertAlmostEqual(out[6], 17496.9, places=1)


if __name__ == "__main__":
    unittest.main()
