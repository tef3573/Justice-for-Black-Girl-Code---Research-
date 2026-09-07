import unittest

from build_checkpoint_weight_attrition import effective_n, rni_category


class CheckpointWeightAttritionTests(unittest.TestCase):
    def test_reason_categories(self):
        self.assertEqual(rni_category(60), "completed")
        self.assertEqual(rni_category(67), "completed")
        self.assertEqual(rni_category(90), "unlocatable")
        self.assertEqual(rni_category(96), "refusal")
        self.assertEqual(rni_category(98), "deceased")

    def test_effective_n_equal_weights(self):
        self.assertEqual(effective_n([2, 2, 2]), 3)

    def test_effective_n_ignores_zero(self):
        self.assertEqual(effective_n([1, 1, 0, None]), 2)


if __name__ == "__main__":
    unittest.main()
