import unittest
import pandas as pd
import numpy as np
from run_m6_sensitivity import fit

class SensitivityTests(unittest.TestCase):
 def test_fit_returns_focal_slopes(self):
  rng=np.random.default_rng(7); groups=["Black_non_Hispanic_women","White_non_Hispanic_women","Black_non_Hispanic_men","White_non_Hispanic_men"]
  f=pd.DataFrame({"socioeconomic_risk_index":rng.normal(size=80),"stem_coursework_rigor_index":rng.normal(size=80),"race_gender_group":[groups[i%4] for i in range(80)],"attainment_level":rng.normal(size=80)})
  p=fit(f,"attainment_level"); self.assertIn("socioeconomic_risk_index",p.index)

if __name__=="__main__": unittest.main()
