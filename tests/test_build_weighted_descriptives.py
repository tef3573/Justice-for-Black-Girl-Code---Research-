import unittest
import pandas as pd

from build_weighted_descriptives import domain_mean, pool


class WeightedDescriptiveTests(unittest.TestCase):
    def test_equal_weight_mean_and_effective_n(self):
        frame = pd.DataFrame({"model_weight": [1, 1, 1, 1],
                              "model_vstrat": [1, 1, 2, 2], "model_vpsu": [1, 2, 1, 2]})
        q, variance, n, neff, _ = domain_mean(frame, pd.Series([1, 2, 3, 4]), pd.Series([True] * 4))
        self.assertEqual(q, 2.5)
        self.assertEqual(n, 4)
        self.assertEqual(neff, 4)
        self.assertGreater(variance, 0)

    def test_rubin_pool_adds_between_variance(self):
        q, total, within, between = pool([1, 2], [1, 1])
        self.assertEqual(q, 1.5)
        self.assertGreater(total, within)
        self.assertGreater(between, 0)


if __name__ == "__main__":
    unittest.main()
