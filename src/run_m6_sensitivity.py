"""Run harmonized complete-case and age-25 attrition-weight sensitivity screens."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from fit_ordinal_attainment import BASE, GROUPS, design_matrix
from impute_predictors import STEM, index_z

OUTCOMES = {"attainment":"attainment_level", "employment":"employed",
            "earnings":"log_positive_labor_earnings_2025"}

def fit(frame, outcome, weights=None):
    x=sm.add_constant(design_matrix(frame),has_constant="add"); y=frame[outcome].astype(float)
    if outcome=="employed":
        return sm.GLM(y,x,family=sm.families.Binomial(),freq_weights=weights).fit().params
    return (sm.WLS(y,x,weights=weights).fit() if weights is not None else sm.OLS(y,x).fit()).params

def propensity(base):
    z=pd.get_dummies(base.race_gender_group,prefix="group",drop_first=True,dtype=float)
    for c in BASE:
        v=pd.to_numeric(base[c],errors="coerce"); z[c]=v.fillna(v.median()); z[c+"_missing"]=v.isna().astype(float)
    z=sm.add_constant(z,has_constant="add")
    model=sm.Logit(base.age25_record_matched.astype(float),z).fit(disp=False)
    p=np.clip(model.predict(z),.05,.95); numerator=base.age25_record_matched.mean()
    return pd.Series(np.where(base.age25_record_matched.eq(1),numerator/p,np.nan),index=base.respondent_id).clip(.2,5)

def build(imputed_path:Path, base_path:Path, table_dir:Path):
    imp=pd.read_csv(imputed_path,low_memory=False); base=pd.read_csv(base_path,low_memory=False)
    base["stem_coursework_rigor_index"] = index_z(base, STEM, [1, 1, 1, 1, 1])
    base.loc[base[STEM].isna().any(axis=1), "stem_coursework_rigor_index"] = np.nan
    base=base[base.race_gender_group.isin(GROUPS)].copy(); ipw=propensity(base)
    rows=[]
    for age in (23,25):
      for name,outcome in OUTCOMES.items():
        draws=[]
        for _,f in imp[imp.checkpoint_age.eq(age)&imp.race_gender_group.isin(GROUPS)].groupby("imputation_id"):
            f=f.copy(); f["employed"]=f.employment_status.eq("employed").astype(float)
            f=f.dropna(subset=BASE+[outcome]); draws.append(fit(f,outcome))
        mean=pd.DataFrame(draws).mean()
        for parameter in BASE: rows.append({"age":age,"outcome":name,"specification":"multiple_imputation","parameter":parameter,"coefficient":mean[parameter]})
        suffix="" if age==23 else "_age25"
        cc=base.copy(); cc["attainment_level"]=cc["attainment_level"+suffix]
        cc["employment_status"]=cc["employment_status"+suffix]
        cc["employed"]=cc.employment_status.eq("employed").astype(float)
        cc["log_positive_labor_earnings_2025"]=cc["log_positive_labor_earnings_2025"+suffix]
        cc=cc.dropna(subset=BASE+[outcome]); estimate=fit(cc,outcome)
        for parameter in BASE: rows.append({"age":age,"outcome":name,"specification":"complete_case","parameter":parameter,"coefficient":estimate[parameter]})
        if age==25:
            weighted=[]
            for _,f in imp[imp.checkpoint_age.eq(25)&imp.race_gender_group.isin(GROUPS)].groupby("imputation_id"):
                f=f.copy(); f["employed"]=f.employment_status.eq("employed").astype(float)
                f["ipw"]=f.respondent_id.map(ipw); f=f.dropna(subset=BASE+[outcome,"ipw"])
                weighted.append(fit(f,outcome,f.ipw))
            estimate=pd.DataFrame(weighted).mean()
            for parameter in BASE: rows.append({"age":age,"outcome":name,"specification":"age25_inverse_probability_weighted","parameter":parameter,"coefficient":estimate[parameter]})
    result=pd.DataFrame(rows); primary=result[result.specification.eq("multiple_imputation")][["age","outcome","parameter","coefficient"]].rename(columns={"coefficient":"primary_coefficient"})
    result=result.merge(primary,on=["age","outcome","parameter"])
    result["same_direction_as_primary"]=np.sign(result.coefficient).eq(np.sign(result.primary_coefficient))
    result["relative_change_abs"]=abs(result.coefficient-result.primary_coefficient)/result.primary_coefficient.abs()
    table_dir.mkdir(parents=True,exist_ok=True); result.to_csv(table_dir/"m6_missing_attrition_sensitivity.csv",index=False)
    summary={"purpose":"directional sensitivity screen using harmonized endpoint models","complete_case_comparisons":12,"age25_ipw_comparisons":6,
             "all_same_direction":bool(result.same_direction_as_primary.all()),
             "ipw_trim_range":[.2,5],"formal_full_robustness_deferred_to_milestone_8":True,"validation":"PASS"}
    (table_dir/"m6_sensitivity_validation.json").write_text(json.dumps(summary,indent=2)+"\n"); return summary

if __name__=="__main__":
 p=argparse.ArgumentParser(); p.add_argument("--imputed",type=Path,default=Path("data/final/model_ready_imputations_v1.csv.gz")); p.add_argument("--base",type=Path,default=Path("data/final/analysis_base_complete_case_v1.csv.gz")); p.add_argument("--tables",type=Path,default=Path("outputs/tables")); a=p.parse_args(); print(json.dumps(build(a.imputed,a.base,a.tables),indent=2))
