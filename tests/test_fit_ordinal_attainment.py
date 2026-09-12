import unittest
import numpy as np
import pandas as pd

from fit_ordinal_attainment import design_matrix, effective_n, rubin


class OrdinalAttainmentTests(unittest.TestCase):
    def test_black_women_are_reference(self):
        frame = pd.DataFrame({"race_gender_group": ["Black_non_Hispanic_women"],
                              "socioeconomic_risk_index": [1.0],
                              "stem_coursework_rigor_index": [2.0]})
        x = design_matrix(frame)
        self.assertEqual(x.filter(like="group_").sum().sum(), 0)
        self.assertEqual(x.filter(like="_x_").sum().sum(), 0)

    def test_rubin_pool(self):
        q, total, within, between = rubin(np.array([[1.0], [2.0]]), np.array([[[1.0]], [[1.0]]]))
        self.assertEqual(q[0], 1.5)
        self.assertGreater(total[0, 0], within[0, 0])

    def test_effective_n(self):
        self.assertEqual(effective_n([1, 1, 1]), 3)


if __name__ == "__main__":
    unittest.main()
