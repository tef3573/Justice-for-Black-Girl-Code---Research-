import unittest

from build_ml_splits import assign_stratum


class MlSplitTests(unittest.TestCase):
    def test_assignment_is_complete_disjoint_and_reproducible(self):
        ids = list(range(100))
        first = assign_stratum(ids, 42)
        second = assign_stratum(ids, 42)
        self.assertEqual(first, second)
        self.assertEqual(set(first), set(ids))
        self.assertEqual(list(first.values()).count("train"), 60)
        self.assertEqual(list(first.values()).count("validation"), 20)
        self.assertEqual(list(first.values()).count("test"), 20)


if __name__ == "__main__":
    unittest.main()
