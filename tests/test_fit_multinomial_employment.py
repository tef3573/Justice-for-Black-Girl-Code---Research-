import unittest

from fit_multinomial_employment import OUTCOME_CODES, parameter_labels


class MultinomialEmploymentTests(unittest.TestCase):
    def test_employed_is_reference(self):
        self.assertEqual(OUTCOME_CODES["employed"], 0)
        self.assertEqual(OUTCOME_CODES["unemployed"], 1)

    def test_parameter_order_is_equation_major(self):
        labels = parameter_labels(["const", "risk"])
        self.assertEqual(labels[0], ("unemployed_vs_employed", "const"))
        self.assertEqual(labels[2], ("not_in_labor_force_vs_employed", "const"))


if __name__ == "__main__":
    unittest.main()
