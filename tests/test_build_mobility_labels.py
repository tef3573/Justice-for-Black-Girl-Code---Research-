import unittest
import numpy as np
from build_mobility_labels import weighted_midrank
class MobilityLabelTests(unittest.TestCase):
 def test_weighted_midrank_ties(self):
  np.testing.assert_allclose(weighted_midrank([0,0,10],[1,1,1]),[100/3,100/3,250/3])
if __name__=="__main__":unittest.main()
