# Missing-data analysis plan

## Objective

The plan preserves the distinction between ordinary item missingness, structural
noncollection, outcome routing, and longitudinal attrition. No missing value is
automatically converted to zero, and one universal complete-case sample will not
be imposed across outcomes.

## Current evidence

Among 7,149 respondents observed at age 23:

- 4,018 (56.20%) lack the current four-component-minimum socioeconomic-risk
  index.
- 1,970 (27.56%) lack math and science progression because a transcript was not
  collected at this stage of the merged sample.
- Attainment is missing for 46 (0.64%).
- Mid-interview-month employment status is missing for 53 (0.74%), with active
  military and indeterminate-not-working records retained as observed but outside
  the primary civilian three-category model.
- Positive-versus-zero earnings status is missing for 43 (0.60%).
- Exact combined real earnings are missing for 1,357 (18.98%), mainly because
  positive income was reported only as a bracket or without an exact amount.

Missingness differs across race-by-gender groups. For example, socioeconomic-risk
index missingness is 54.21% among Black women, 56.12% among Black men, 53.47%
among White women, and 57.68% among White men. Transcript progression missingness
is 25.89%, 34.40%, 24.10%, and 24.00%, respectively. These differences require
group-specific reporting and sensitivity analysis.

## Primary rules

1. **Retain the full age-23 base.** Keep all 7,149 rows and explicit missingness,
   match, status, and eligibility fields.
2. **Do not impute outcomes.** Attainment, employment status, positive-earnings
   status, and exact earnings remain observed outcomes. Outcome-specific models
   exclude records missing that outcome.
3. **Do not impute race or gender.** Unknown categories remain explicit and are
   excluded only from a contrast that cannot identify them.
4. **Do not impute an uncollected transcript in the primary analysis.** The
   primary STEM pathway sample requires a collected transcript. Item-level STEM
   values may be imputed only among respondents with a collected transcript when
   the specific item is missing and diagnostics support missing at random.
5. **Do not impute exact earnings from brackets in the primary earnings-amount
   model.** Bracket-only cases remain eligible for the positive-earnings first
   part but not the exact-amount second part.
6. **Impute socioeconomic components, not the finished composite.** For the
   primary adjusted pathway analysis, use multiple imputation by chained
   equations on eligible component variables after attrition and survey-design
   fields are added. Recalculate the risk index separately in each imputed
   dataset using the documented sign and minimum-component rules.
7. **Use at least 50 imputations.** Increase the number if the fraction of missing
   information or Monte Carlo error indicates instability. Include race-by-gender,
   observed outcomes, exposure components, STEM measures, baseline predictors,
   interview pattern, and survey-design variables in the imputation model. The
   outcome helps predict missing covariates but is never replaced by an imputed
   outcome in the estimation sample.
8. **Respect variable type.** Use predictive mean matching for continuous
   components, logistic models for binary variables, and appropriate ordinal or
   multinomial models for categorical predictors. Constrain values to valid
   ranges and preserve structural skips.

## Required sensitivity analyses

- Complete-case estimates using the exported outcome-specific flags.
- Separate-component models that avoid requiring the composite index.
- Alternative socioeconomic-index minimums and component sets.
- Transcript-selection analysis and, if diagnostics support it, inverse-
  probability-of-observation weighting.
- Earnings bracket sensitivity using documented lower/upper bounds or interval
  methods; midpoint substitution is not the primary specification.
- Attrition weighting after interview-status analysis.
- Comparison of estimates across Black women, White women, Black men, and White
  men, including group-specific missingness and effective sample sizes.

## Diagnostics and reporting

Before estimation, report missingness by variable and race-by-gender group,
common missingness patterns, observed-versus-excluded baseline differences,
complete-case counts for every outcome, and imputation convergence/distribution
checks. Compare observed and imputed distributions and report whether substantive
conclusions change across sensitivity specifications.

## Machine-learning boundary

For elastic net and any later predictive model, split or resample the data before
imputation, scaling, feature selection, or index re-estimation. Fit every
preprocessing step using the training fold only and apply it to the held-out fold.
This prevents information leakage. Report predictive performance and calibration
separately by race-by-gender group; do not treat imputation as evidence that a
missing lived experience was observed.

For upward-mobility prediction, define the feature cutoff before addressing
missingness. An age-25 prediction may use features through age 23; later-horizon
predictions may use features through age 25. Post-cutoff variables are outcome
labels only. Do not use later interview patterns, later income, later occupation,
or later missingness indicators to impute or engineer predictors. Missing future
labels reduce the evaluable prediction sample and require a separately reported
retention/selection analysis; future labels themselves will not be imputed.

## Implementation status

The dependency is resolved. Survey design and attrition fields are finalized,
and 50 predictor-only chained-equation imputations have been generated and
validated. Socioeconomic-risk and STEM coursework-rigor indices are reconstructed
inside every imputation. The stacked file is for statistical modeling with
Rubin's-rule pooling; machine-learning preprocessing must still be refitted
inside each training fold to prevent leakage.
