"""Create 50 chained-equation predictor imputations and reconstruct indices."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.imputation.mice import MICEData


SOCIO = [
    "average_household_income_rank", "average_poverty_ratio",
    "proportion_observed_years_in_poverty", "highest_parent_education_years",
    "baseline_public_assistance_exposure", "baseline_parent_household_jobless_proxy",
]
STEM = [
    "math_pipeline_level", "science_pipeline_level", "science_credits",
    "math_credits", "advanced_math_credits",
]
NONIMPUTED = [
    "race_ethnicity_group", "race_gender_group", "attainment_level",
    "employment_status", "positive_labor_earnings", "labor_earnings_2025_dollars",
    "transcript_collected",
]
BOUNDS = {
    "average_household_income_rank": (0, 100, False),
    "average_poverty_ratio": (0, None, False),
    "proportion_observed_years_in_poverty": (0, 1, False),
    "highest_parent_education_years": (0, 20, True),
    "baseline_public_assistance_exposure": (0, 1, True),
    "baseline_parent_household_jobless_proxy": (0, 1, True),
    "math_pipeline_level": (1, 8, True),
    "science_pipeline_level": (0, 6, True),
    "science_credits": (0, None, False),
    "math_credits": (0, None, False),
    "advanced_math_credits": (0, None, False),
}


def fingerprint(frame: pd.DataFrame, columns: list[str]) -> str:
    return hashlib.sha256(frame[columns].fillna("<MISSING>").astype(str).to_csv(index=False).encode()).hexdigest()


def auxiliaries(frame: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=frame.index)
    groups = pd.get_dummies(frame["race_gender_group"], prefix="group", dtype=float, drop_first=True)
    out = pd.concat([out, groups], axis=1)
    for field in ("analysis_weight", "analysis_vstrat", "analysis_vpsu", "age24_record_matched", "age25_record_matched"):
        values = pd.to_numeric(frame[field], errors="coerce")
        out[field] = values.fillna(values.median())
    mappings = {
        "attainment_aux": pd.to_numeric(frame["attainment_level"], errors="coerce"),
        "earnings_status_aux": pd.to_numeric(frame["positive_labor_earnings"], errors="coerce"),
        "log_earnings_aux": pd.to_numeric(frame["log_positive_labor_earnings_2025"], errors="coerce"),
    }
    for name, values in mappings.items():
        out[name] = values.fillna(values.median())
    employment = pd.get_dummies(frame["employment_status"].fillna("missing"), prefix="employment", dtype=float, drop_first=True)
    return pd.concat([out, employment], axis=1).astype(float)


def constrain(frame: pd.DataFrame, fields: list[str]) -> pd.DataFrame:
    for field in fields:
        lower, upper, integer = BOUNDS[field]
        frame[field] = frame[field].clip(lower=lower, upper=upper)
        if integer:
            frame[field] = frame[field].round()
    return frame


def index_z(frame: pd.DataFrame, fields: list[str], signs: list[int]) -> pd.Series:
    pieces = []
    for field, sign in zip(fields, signs):
        values = frame[field].astype(float) * sign
        sd = values.std(ddof=1)
        pieces.append((values - values.mean()) / sd if sd > 0 else values * 0)
    return pd.concat(pieces, axis=1).mean(axis=1)


def chain(source: pd.DataFrame, fields: list[str], aux: pd.DataFrame,
          imputations: int, burn_in: int, between: int, seed: int):
    usable_aux = aux.loc[:, aux.nunique(dropna=False) > 1]
    model = pd.concat([source[fields].apply(pd.to_numeric, errors="coerce"), usable_aux], axis=1)
    np.random.seed(seed)
    mice = MICEData(model, perturbation_method="boot", k_pmm=10)
    for field in fields:
        mice.set_imputer(field, regularized=True,
                         fit_kwds={"alpha": 1e-6, "L1_wt": 0.0})
    mice.update_all(burn_in)
    draws, trace = [], []
    for number in range(1, imputations + 1):
        mice.update_all(between)
        completed = constrain(mice.data[fields].copy(), fields)
        completed.index = source.index
        draws.append(completed)
        trace.append({"imputation": number, **{f"mean_{f}": float(completed[f].mean()) for f in fields}})
    return draws, trace


def build(source_path: Path, output_path: Path, table_dir: Path,
          imputations=50, burn_in=5, between=1, seed=20260906):
    data = pd.read_csv(source_path, low_memory=False)
    original_hash = fingerprint(data, NONIMPUTED)
    aux = auxiliaries(data)
    socio_eligible = data["socioeconomic_record_matched"].eq(1)
    stem_eligible = data["transcript_collected"].eq(1)
    socio_draws, socio_trace = chain(data.loc[socio_eligible], SOCIO, aux.loc[socio_eligible], imputations, burn_in, between, seed)
    stem_draws, stem_trace = chain(data.loc[stem_eligible], STEM, aux.loc[stem_eligible], imputations, burn_in, between, seed + 1)

    original_missing = {field: data[field].isna() for field in SOCIO + STEM}
    rows, diagnostics = [], []
    index_means = []
    for number, (socio, stem) in enumerate(zip(socio_draws, stem_draws), 1):
        out = pd.DataFrame({"respondent_id": data["respondent_id"], "imputation_id": number})
        for field in SOCIO:
            out[field] = np.nan
            out.loc[socio_eligible, field] = socio[field]
        out["low_parental_education"] = np.where(
            out["highest_parent_education_years"].notna(),
            (out["highest_parent_education_years"] <= 12).astype(float), np.nan)
        socio_fields = ["average_household_income_rank", "average_poverty_ratio",
                        "proportion_observed_years_in_poverty", "low_parental_education",
                        "baseline_public_assistance_exposure", "baseline_parent_household_jobless_proxy"]
        out["socioeconomic_risk_index"] = index_z(
            out.loc[socio_eligible, socio_fields], socio_fields, [-1, -1, 1, 1, 1, 1])
        for field in STEM:
            out[field] = np.nan
            out.loc[stem_eligible, field] = stem[field]
        out["stem_coursework_rigor_index"] = index_z(
            out.loc[stem_eligible, STEM], STEM, [1, 1, 1, 1, 1])
        rows.append(out)
        black_women = data["race_gender_group"].eq("Black_non_Hispanic_women")
        index_means.append({
            "imputation": number,
            "black_women_socioeconomic_risk_index_mean": float(out.loc[black_women, "socioeconomic_risk_index"].mean()),
            "black_women_stem_coursework_rigor_index_mean": float(out.loc[black_women, "stem_coursework_rigor_index"].mean()),
        })
        for field in SOCIO + STEM:
            eligible = socio_eligible if field in SOCIO else stem_eligible
            observed = data.loc[eligible & ~original_missing[field], field]
            imputed = out.loc[eligible & original_missing[field], field]
            diagnostics.append({
                "imputation": number, "variable": field,
                "observed_n": int(observed.notna().sum()), "imputed_n": int(imputed.notna().sum()),
                "observed_mean": float(observed.mean()),
                "imputed_mean": float(imputed.mean()) if len(imputed) else "",
                "imputed_min": float(imputed.min()) if len(imputed) else "",
                "imputed_max": float(imputed.max()) if len(imputed) else "",
            })

    stacked = pd.concat(rows, ignore_index=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    stacked.to_csv(output_path, index=False)
    table_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(diagnostics).to_csv(table_dir / "imputation_distribution_diagnostics.csv", index=False)
    traces = pd.DataFrame(socio_trace).merge(pd.DataFrame(stem_trace), on="imputation", suffixes=("_socio", "_stem"))
    traces.to_csv(table_dir / "imputation_convergence_trace.csv", index=False)
    means = pd.DataFrame(index_means)
    means.to_csv(table_dir / "imputation_index_means.csv", index=False)

    mc = {}
    for field in ("black_women_socioeconomic_risk_index_mean", "black_women_stem_coursework_rigor_index_mean"):
        mc[field] = {
            "between_imputation_sd": float(means[field].std(ddof=1)),
            "monte_carlo_se": float(means[field].std(ddof=1) / np.sqrt(imputations)),
            "first10_last10_mean_difference": float(means[field].head(10).mean() - means[field].tail(10).mean()),
        }
    bounds_valid = all(
        ((stacked[field].dropna() >= BOUNDS[field][0]).all()
         and (BOUNDS[field][1] is None or (stacked[field].dropna() <= BOUNDS[field][1]).all()))
        for field in SOCIO + STEM)
    summary = {
        "method": "fully conditional specification with predictive mean matching (10 donors)",
        "imputations": imputations, "burn_in_cycles": burn_in, "cycles_between_draws": between,
        "source_rows": len(data), "stacked_rows": len(stacked),
        "socioeconomic_eligible_rows_per_imputation": int(socio_eligible.sum()),
        "stem_eligible_rows_per_imputation": int(stem_eligible.sum()),
        "uncollected_transcripts_preserved": int((~stem_eligible).sum()),
        "outcomes_imputed": False, "race_gender_imputed": False,
        "nonimputed_source_fingerprint": original_hash,
        "valid_bounds": bool(bounds_valid), "monte_carlo_diagnostics": mc,
        "validation": "PASS" if bounds_valid and imputations >= 50 else "FAIL",
    }
    (table_dir / "imputation_validation.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", type=Path, default=Path("data/processed/analysis_dataset.csv"))
    p.add_argument("--output", type=Path, default=Path("data/processed/imputed_predictors_long.csv"))
    p.add_argument("--tables", type=Path, default=Path("outputs/tables"))
    p.add_argument("--imputations", type=int, default=50)
    p.add_argument("--burn-in", type=int, default=5)
    p.add_argument("--between", type=int, default=1)
    p.add_argument("--seed", type=int, default=20260906)
    a = p.parse_args()
    print(json.dumps(build(a.source, a.output, a.tables, a.imputations, a.burn_in, a.between, a.seed), indent=2))
