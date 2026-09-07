import unittest
import pandas as pd

from impute_predictors import chain, constrain, index_z


class ImputationTests(unittest.TestCase):
    def test_constraints_round_binary(self):
        frame = pd.DataFrame({"baseline_public_assistance_exposure": [-.2, .6, 1.4]})
        result = constrain(frame, ["baseline_public_assistance_exposure"])
        self.assertEqual(result.iloc[:, 0].tolist(), [0.0, 1.0, 1.0])

    def test_index_direction(self):
        frame = pd.DataFrame({"income": [10.0, 20.0, 30.0], "poverty": [1.0, .5, 0.0]})
        result = index_z(frame, ["income", "poverty"], [-1, 1])
        self.assertGreater(result.iloc[0], result.iloc[-1])

    def test_chain_preserves_subset_index(self):
        source = pd.DataFrame({"average_household_income_rank": [10.0, None, 30.0, 40.0]},
                              index=[2, 4, 7, 9])
        aux = pd.DataFrame({"aux": [0.0, 1.0, 2.0, 3.0]}, index=source.index)
        draws, _ = chain(source, ["average_household_income_rank"], aux, 1, 1, 1, 7)
        self.assertEqual(draws[0].index.tolist(), [2, 4, 7, 9])


if __name__ == "__main__":
    unittest.main()
