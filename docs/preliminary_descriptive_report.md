# Preliminary descriptive profile

## Purpose

This checkpoint completes the first usable portion of descriptive analysis with
the variables currently cleaned. It reports sample flow, observed-age coverage,
and STEM transcript missingness. It does not estimate relationships, test the
hypothesis, or present final study findings.

## Current analytic boundary

The available files support unweighted descriptions only. Survey weights,
socioeconomic-risk variables, attainment, employment, and earnings are not yet
part of the focused analytic extract. Therefore:

- weighted sample characteristics are deferred;
- class-stratified comparisons are deferred;
- outcome trajectories and statistical models are deferred; and
- no figure is produced at this stage, consistent with the plan to create
  visuals for the final research poster.

## Tables produced

- `outputs/tables/preliminary_sample_characteristics.csv`: fixed-denominator
  sample flow, complete age coverage, transcript collection, and problem flags.
- `outputs/tables/preliminary_age_coverage.csv`: observed records at each age,
  using all 1,166 baseline focal respondents as the denominator.
- `outputs/tables/preliminary_stem_missingness.csv`: source-preserving status
  distributions among the 1,163 respondents represented in the age panel.
- `outputs/tables/preliminary_descriptive_validation.json`: validation counts
  and explicit statements about unavailable weighting and class measures.

Generated tables are excluded from Git; the reproducible builder, tests, and
this report are tracked.

## Denominator rules

The baseline focal cohort of 1,166 is the denominator for cohort retention and
age coverage. The 1,163 respondents with at least one observed record from ages
15–23 are the denominator for transcript collection and variable-status tables.
The number of collected transcripts is the denominator for the transcript
problem-flag percentage. Denominators are included in every aggregate table.

## Interpretation rules for the white paper

These tables describe the construction and observability of the analytic data.
They must not be described as evidence that STEM coursework causes educational,
employment, or earnings outcomes. Transcript noncollection is analytically
different from taking no course, and the official problem flag does not by
itself require record exclusion. Both will be addressed in sensitivity analyses.

## Reproduction

```sh
python3 src/build_descriptive_profile.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Remaining descriptive work

1. Add documented survey weights and interview-status fields.
2. Clean the socioeconomic-risk and class measures.
3. Clean attainment, employment, and inflation-adjusted earnings outcomes.
4. Rebuild weighted characteristics and attrition comparisons.
5. Examine within-group class differences before creating final figures.
