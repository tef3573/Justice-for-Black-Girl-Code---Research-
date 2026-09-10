import unittest
import pandas as pd

from build_attainment_marginal_effects import altered


class AttainmentMarginalEffectsTests(unittest.TestCase):
    def test_altered_design_changes_focal_predictor(self):
        frame = pd.DataFrame({"socioeconomic_risk_index": [0.0],
                              "stem_coursework_rigor_index": [0.0],
                              "race_gender_group": ["Black_non_Hispanic_women"]})
        self.assertAlmostEqual(altered(frame, "socioeconomic_risk_index", .01)[0, 0], .01)


if __name__ == "__main__":
    unittest.main()
