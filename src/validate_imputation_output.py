"""Validate preservation, structural missingness, and stability of MI output."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from impute_predictors import NONIMPUTED, SOCIO, STEM


def validate(source_path: Path, imputed_path: Path, index_path: Path, output_path: Path):
    source = pd.read_csv(source_path, low_memory=False).set_index("respondent_id")
    imputed = pd.read_csv(imputed_path)
    observed_preserved = {}
    for field in SOCIO + STEM:
        observed = source[field].notna()
        expected = source.loc[observed, field]
        values = imputed[imputed["respondent_id"].isin(expected.index)][["respondent_id", field]]
        differences = values[field].to_numpy() - expected.reindex(values["respondent_id"]).to_numpy()
        observed_preserved[field] = bool(np.all(np.abs(differences) < 1e-9))
    uncollected_ids = source.index[source["transcript_collected"].eq(0)]
    structural = imputed[imputed["respondent_id"].isin(uncollected_ids)]
    structural_preserved = bool(structural[STEM + ["stem_coursework_rigor_index"]].isna().all().all())
    sizes = imputed.groupby("imputation_id").size()
    dimensions_valid = bool(len(sizes) == 50 and sizes.nunique() == 1 and sizes.iloc[0] == len(source))
    unique_keys = bool(~imputed.duplicated(["respondent_id", "imputation_id"]).any())
    socio_ids = source.index[source["socioeconomic_record_matched"].eq(1)]
    eligible_complete = bool(
        imputed[imputed["respondent_id"].isin(socio_ids)][SOCIO + ["socioeconomic_risk_index"]].notna().all().all()
        and imputed[imputed["respondent_id"].isin(source.index[source["transcript_collected"].eq(1)])]
        [STEM + ["stem_coursework_rigor_index"]].notna().all().all()
    )
    means = pd.read_csv(index_path)
    stability = {}
    for field in means.columns[1:]:
        sd = means[field].std(ddof=1)
        stability[field] = {
            "monte_carlo_se": float(sd / np.sqrt(50)),
            "first10_last10_difference": float(means[field].head(10).mean() - means[field].tail(10).mean()),
            "passes_prespecified_thresholds": bool(sd / np.sqrt(50) < .005 and
                                                    abs(means[field].head(10).mean() - means[field].tail(10).mean()) < .02),
        }
    outcome_columns_absent = all(field not in imputed for field in NONIMPUTED)
    passed = (all(observed_preserved.values()) and structural_preserved and dimensions_valid
              and unique_keys and eligible_complete and outcome_columns_absent
              and all(v["passes_prespecified_thresholds"] for v in stability.values()))
    summary = {
        "imputations": 50, "rows_per_imputation": int(sizes.iloc[0]),
        "unique_respondent_imputation_keys": unique_keys,
        "all_observed_predictor_values_preserved": all(observed_preserved.values()),
        "observed_preservation_by_field": observed_preserved,
        "uncollected_transcript_structural_missingness_preserved": structural_preserved,
        "eligible_imputed_components_and_indices_complete": eligible_complete,
        "outcome_race_gender_columns_absent_from_imputed_output": outcome_columns_absent,
        "monte_carlo_and_convergence": stability,
        "validation": "PASS" if passed else "FAIL",
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", type=Path, default=Path("data/processed/analysis_dataset.csv"))
    p.add_argument("--imputed", type=Path, default=Path("data/processed/imputed_predictors_long.csv"))
    p.add_argument("--indices", type=Path, default=Path("outputs/tables/imputation_index_means.csv"))
    p.add_argument("--output", type=Path, default=Path("outputs/tables/imputation_preservation_validation.json"))
    a = p.parse_args()
    print(json.dumps(validate(a.source, a.imputed, a.indices, a.output), indent=2))
