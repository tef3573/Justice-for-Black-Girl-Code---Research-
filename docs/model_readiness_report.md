# Milestones 1–5 completion and model-readiness report

## Executive decision

Milestones 1 and 3 are substantially complete. Milestone 2 has a reproducible
candidate-variable specification but still requires final approval of several
operational measures. Milestones 4 and 5 are partially complete. Statistical
modeling must not begin until the blocked items below are resolved and a final
analysis dataset is validated.

This is a readiness decision, not a substantive research result.

## Milestone status

| Milestone | Status | Evidence | Remaining work |
|---|---|---|---|
| 1 — Repository foundation | Complete with safety warning | Research design, documented structure, reproducible scripts, tests, and ignore rules | Keep raw/generated data out of Git; restore the canonical `data/` location when convenient |
| 2 — Extraction specification | Partial | Exact-reference candidate audit and codebook-linked profiles | Finalize employment, weights, interview status, socioeconomic index inputs, and outcome timing |
| 3 — Cohort construction | Substantially complete | 1,166-person focal cohort and 8,348 person-age records | Add interview status before calling missing age records attrition |
| 4 — Construct development | Partial | STEM transcript coursework cleaned | Clean socioeconomic risk, attainment, employment, earnings, inflation adjustment; resolve neighborhood and institutional-quality scope |
| 5 — Descriptive analysis | Partial | Preliminary sample-flow, age-coverage, and STEM-missingness tables | Add weights, formal attrition, class comparisons, outcomes, and final weighted tables |

## What is needed before Milestone 6

### Required data work

1. **Socioeconomic risk and class:** finalize 4–6 indicators, their adolescent
   exposure window, coding direction, missingness rules, and index method.
2. **Educational attainment:** select age-aligned highest grade, degree, and
   enrollment variables and define the age-23 outcome hierarchy.
3. **Employment access:** derive employed, unemployed, and not-in-labor-force
   status. A single job's hours cannot represent employment access.
4. **Earnings:** use routing variables to distinguish zero earnings from missing
   earnings; select the correct prior-year reference period; document topcoding;
   convert monetary values to constant dollars.
5. **Survey design:** select the appropriate longitudinal or custom weight and
   document how standard errors will account for the survey design.
6. **Attrition:** add interview-status variables and compare observed versus
   unavailable respondents using baseline covariates.
7. **Final merge:** produce one versioned analysis dataset with audited merge
   counts, unique keys, temporal-order checks, and an analysis-specific sample
   flow.

### Measurement decisions that cannot be hidden

- Public-use transcript measures support completed STEM coursework and rigor,
  not complete institutional STEM educational quality.
- Public-use NLSY97 data currently do not measure neighborhood disinvestment at
  the desired geographic level. Restricted geocodes or an approved linked source
  would be required. Household socioeconomic risk cannot be relabeled as
  neighborhood disinvestment.
- The available demographic field records sex at baseline and does not measure
  the full range of gender identities.

## Recommended Milestone 6 model sequence

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

## Go/no-go rule

Milestone 6 is ready only when every required predictor and outcome has a final
definition, the temporal ordering is defensible, weights and missingness are
specified, and the merged analysis dataset passes validation. The automated
readiness matrix intentionally returns `milestone_6_ready: false` until those
conditions are met.
