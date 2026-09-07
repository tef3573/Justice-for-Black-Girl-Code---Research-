# Milestones 1–5 completion and model-readiness report

## Executive decision

Milestones 1 and 3 are substantially complete. The socioeconomic-risk,
STEM-coursework, and age-23 outcome pipelines are now implemented and validated.
Milestones 2, 4, and 5 remain partial because the final survey design, attrition,
institutional STEM-quality extension, and attrition analysis remain unresolved.
The respondent-level merge and missing-data plan are complete. Statistical
modeling must not begin until the remaining blocked
items are resolved and a final analysis dataset is validated.

Post-25 mobility labels are not a gate for Milestone 6. They belong to the
separate Milestone 7 prediction extension and cannot be used as explanatory
features in the within-age-25 statistical analysis.

This is a readiness decision, not a substantive research result.

## Milestone status

| Milestone | Status | Evidence | Remaining work |
|---|---|---|---|
| 1 — Repository foundation | Complete with safety warning | Research design, documented structure, reproducible scripts, tests, and ignore rules | Keep raw/generated data out of Git; restore the canonical `data/` location when convenient |
| 2 — Extraction specification | Partial | Exact-reference candidate audit, codebook-linked profiles, and resolved age-23 outcomes | Finalize weights and interview status |
| 3 — Cohort construction | Substantially complete | 1,166-person focal cohort and 8,348 person-age records | Add interview status before calling missing age records attrition |
| 4 — Construct development | Substantially complete | Socioeconomic risk, STEM transcript coursework, attainment, employment, and real earnings cleaned | Resolve neighborhood and institutional-quality scope and evaluate alternative socioeconomic-index specifications |
| 5 — Descriptive analysis | Partial | Preliminary sample flow plus merged-sample and race-by-gender missingness tables | Add weights, formal attrition, class comparisons, and final weighted tables |

## What is needed before Milestone 6

### Required data work

1. **Survey design:** select the appropriate longitudinal or custom weight and
   document how standard errors will account for the survey design.
2. **Attrition:** add interview-status variables and compare observed versus
   unavailable respondents using baseline covariates.
3. **Apply the missing-data plan:** implement imputation and selection-weight
   sensitivity procedures only after survey-weight and attrition fields are
   available. The rules and eligibility flags are already documented.

### Measurement decisions that cannot be hidden

- Public-use transcript measures support completed STEM coursework and rigor,
  not complete institutional STEM educational quality.
- Public-use NLSY97 data currently do not measure neighborhood disinvestment at
  the desired geographic level. Restricted geocodes or an approved linked source
  would be required. Household socioeconomic risk cannot be relabeled as
  neighborhood disinvestment.
- The available demographic field records sex at baseline and does not measure
  the full range of gender identities.

## Milestone 6 model sequence

After the gates pass, begin with interpretable statistical models before machine
learning:

1. Ordinal or binary attainment model, depending on the finalized outcome.
2. Multinomial employment-status model at age 23.
3. Two-part earnings model: probability of positive earnings followed by a
   model of log earnings among respondents with positive earnings.
4. Path or generalized structural equation model for the hypothesized sequence:
   socioeconomic risk → STEM coursework → attainment → employment → earnings.
5. Marginal effects and predicted probabilities with survey-weighted uncertainty.

Elastic net belongs in Milestone 7 as a complementary prediction and variable-
selection analysis. It should not replace the interpretable pathway models.

For upward-mobility prediction, features must be frozen by age 23 or 25 before
constructing later labels. Post-cutoff data may define targets and evaluate the
model but must not enter preprocessing, imputation, feature selection, or index
construction.

## Go/no-go rule

Milestone 6 is ready only when every required predictor and outcome has a final
definition, the temporal ordering is defensible, weights and missingness are
specified, and the merged analysis dataset passes validation. The automated
readiness matrix intentionally returns `milestone_6_ready: false` until those
conditions are met.
