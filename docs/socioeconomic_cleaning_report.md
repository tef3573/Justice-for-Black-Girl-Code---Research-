# Socioeconomic-risk cleaning report

## Scope

This step cleans the NLSY97 socioeconomic exposure measures observed at ages
15–17 and constructs a respondent-level version of the approved
`socioeconomic risk` measure. It does not estimate substantive relationships or
make causal claims.

## Operational rules

- Household income retains valid negative dollar amounts and keeps NLSY97
  refusal, don't-know, invalid-skip, valid-skip, and noninterview codes missing.
- Poverty ratio is converted from the codebook's two-implied-decimal format.
- Household-income percentile ranks are calculated within survey year and age
  using the cumulative-cases cross-sectional sampling weight.
- Income instability is the respondent's standard deviation of annual income
  rank and requires at least two observed ranks.
- Parent education is the highest valid value among the available residential
  and biological mother/father measures. Low parental education is 12 years or
  less; code 95 is retained as ungraded and is not treated as a numeric year.
- Baseline public-assistance exposure is positive when the parent reports AFDC,
  food-stamp, or SSI receipt by the parent or spouse during the prior year. A
  negative classification requires all three items to be observed as no.
- Baseline parent-household joblessness is positive when the responding parent
  is not employed and either has no spouse in the household or reports that the
  spouse is not employed. It is explicitly a proxy and does not establish that
  every co-residing adult was jobless.

## Composite construction

The index is the mean of available sign-aligned z-scores for six components:
low household-income rank, low poverty ratio, poverty persistence, low parental
education, public-assistance exposure, and the parent-household joblessness
proxy. Higher values indicate greater socioeconomic risk. A respondent needs at
least four observed components. Component measures are retained for transparent
models and sensitivity checks.

## Validation results

- Age-level records cleaned: **18,699**
- Respondents represented: **8,828**
- Respondents with a four-or-more-component risk index: **3,926**
- Sampling weights observed on every age-level record: **18,699**
- Automated tests passing: **32**
- Validation status: **PASS**

The smaller index count is primarily driven by limited observed annual income
and poverty-ratio values in the common ages 15–17 panel, not by converting valid
skip codes to zero. Missingness statuses remain explicit in the age-level file.

## Outputs

- `data/processed/socioeconomic_age15_17_clean.csv`: cleaned person-age values
  and status fields.
- `data/processed/socioeconomic_risk_respondent.csv`: respondent summaries,
  separate components, component count, and composite index.
- `outputs/tables/socioeconomic_cleaning_validation.json`: machine-readable
  counts, missingness statuses, and decisions.

## Remaining decisions before modeling

1. Select and document the final weight for multi-round outcome models.
2. Decide the primary missing-data strategy after outcomes are cleaned and the
   complete analytic sample can be assessed.
3. Compare the equal-weight index with separate-component models and a PCA/CFA
   sensitivity specification.
4. Treat the baseline assistance and joblessness measures as proxies in the
   white paper; do not describe them as repeated annual exposure measures.
