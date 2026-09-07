# Research development roadmap

This roadmap is ordered by dependency, not by calendar day. Each milestone ends
with reproducible code, validation outputs, updated white-paper notes, and a
focused Git commit. Generated or restricted data must remain outside Git.

## Research boundary

- Focal population: Black girls and young Black women.
- Primary comparisons: White women, Black men, and White men; other groups are
  secondary when sample size permits.
- Explanatory research period: within the program's age-5-to-25 boundary. The
  available NLSY97 measures begin in adolescence.
- Socioeconomic exposure window: ages 15–17.
- Primary education and early-employment checkpoint: age 23.
- Supplementary within-bound checkpoints: ages 24 and 25.
- Post-25 records: future labels for supervised upward-mobility prediction only.
  They cannot be predictor features or part of the primary explanatory models.

## Milestone 1 — Repository and study foundation

**Status: complete**

- [x] Establish protected raw, interim, processed, output, test, and document
  directories.
- [x] Record the approved research question and construct names.
- [x] Define the focal and comparison populations.
- [x] Document the associational interpretation and restricted-data boundary.
- [x] Establish reproducible scripts, tests, and Git ignore protections.

## Milestone 2 — Source and variable specification

**Status: substantially complete**

- [x] Acquire and checksum the NLSY97 public-use archive.
- [x] Audit candidate NLSY97 variables and codebook references.
- [x] Resolve socioeconomic, STEM transcript, attainment, employment, and
  earnings fields through age 25.
- [x] Document Opportunity Atlas, ACS, and ELS:2002 roles and merge boundaries.
- [x] Resolve interview-status fields through age 25.
- [x] Select checkpoint-specific cumulative-case weights; retain a custom
  longitudinal weight as a pathway-model sensitivity requirement.
- [ ] Finalize the uploadable NLS Investigator tagset after status and weight
  decisions.
- [ ] Decide whether ELS:2002 is necessary for the institutional STEM-quality
  validation analysis.

## Milestone 3 — Cohort and checkpoint construction

**Status: substantially complete**

- [x] Construct mutually exclusive race-by-gender groups.
- [x] Build the unique person-age panel for ages 15–25.
- [x] Retain 77,069 person-age records across 8,928 respondents.
- [x] Build age-23, age-24, and age-25 outcome checkpoints.
- [x] Audit duplicate respondent-age records and retain the latest eligible round.
- [x] Keep age 23 as the primary base and ages 24–25 as supplementary outcomes.
- [x] Add interview-status records and distinguish noninterview from ordinary
  item missingness.
- [x] Complete age-specific retention and attrition flow tables for ages 24–25.

## Milestone 4 — Predictor and outcome construction

**Status: substantially complete**

### Socioeconomic risk

- [x] Clean ages 15–17 household income, poverty ratio, parent education,
  baseline public assistance, and parent-household joblessness proxy.
- [x] Calculate survey-weighted age-year income ranks.
- [x] Construct the four-component-minimum socioeconomic-risk index.
- [x] Retain all component measures and explicit missingness statuses.
- [ ] Implement alternative component sets and PCA/CFA sensitivity versions.

### STEM educational quality

- [x] Clean mathematics/science progression and Carnegie-credit measures.
- [x] Expand transcript cleaning to the full approved comparison cohort.
- [x] Preserve transcript noncollection and problem flags.
- [ ] Construct the secondary sign-aligned STEM coursework-and-rigor index.
- [ ] Decide whether ELS:2002 will validate broader institutional quality,
  including course availability, academic support, and school context.

### Education, employment, and earnings

- [x] Construct degree-first educational-attainment categories at ages 23–25.
- [x] Construct weekly-history employment status and separate active military
  from the civilian labor-force categories.
- [x] Route wage and self-employment income so zero, positive, bracket-only, and
  missing amounts remain distinct.
- [x] Convert exact earnings to constant 2025 CPI-U dollars.
- [x] Validate 21,335 outcome checkpoint records: 7,149 at age 23, 7,129 at age
  24, and 7,057 at age 25.

## Milestone 5 — Model-readiness gate

**Status: complete**

Complete these tasks in order.

### 5A. Survey design

- [x] Choose the retained-round `SAMPLING_WEIGHT_CC` for age-23 and
  supplementary age-24/25 checkpoint estimates.
- [x] Determine that a custom longitudinal weight is necessary as a pathway-
  model sensitivity.
- [x] Specify `VSTRAT`/`VPSU`, Taylor-linearized uncertainty, subpopulation
  estimation, and singleton-stratum treatment.
- [x] Add finalized checkpoint weight and design fields to the analysis dataset
  and documentation.

**Status: complete**

### 5B. Attrition

- [x] Extract interview-status and noninterview-reason fields through age 25.
- [x] Compare respondents retained and unavailable at ages 24 and 25 using
  baseline race-by-gender and socioeconomic measures.
- [x] Report age-24/25 retention by race-by-gender group; formal adjusted tests
  remain part of the retention-model decision.
- [x] Keep the cumulative-case checkpoint weight as primary; require an
  inverse-probability-of-exact-age-observation sensitivity analysis because
  baseline imbalance exceeds `|SMD| = 0.10`.

**Status: complete**

### 5C. Missing-data implementation

- [x] Document the mechanism-specific missing-data plan.
- [x] Retain outcome-specific complete-case eligibility flags.
- [x] Implement 50 chained-equation predictive-mean-matching imputations for
  eligible predictor components only.
- [x] Reconstruct socioeconomic-risk and STEM coursework-rigor indices within
  each imputed dataset.
- [x] Preserve outcomes, race/gender, uncollected transcripts, and bracket-only
  exact earnings as nonimputed.
- [x] Validate 50 imputations, distributions, convergence, and Monte
  Carlo error.

**Status: complete**

### 5D. Final model-ready datasets

- [x] Create the 7,149-row age-23 structural analysis merge.
- [x] Add age-24 and age-25 supplementary columns and match flags.
- [x] Validate unique IDs, merge counts, demographics, temporal order, and
  outcome-specific sample flags.
- [x] Rebuild after weights, attrition fields, and imputation specifications are
  finalized.
- [x] Freeze and version the statistical-analysis dataset as `v1` with SHA-256
  provenance.
- [x] Run the automated readiness audit; required gates pass.

**Status: complete**

## Milestone 6 — Descriptive and statistical analysis within age 25

**Status: complete**

### Descriptive analysis

- [x] Produce weighted sample characteristics by race-by-gender group.
- [x] Compare socioeconomic-risk index and STEM coursework/rigor.
- [x] Compare age-23 primary and age-25 supplementary attainment, employment,
  and earnings outcomes.
- [x] Report missingness, retention, complete-case counts, and effective sample
  sizes for every fitted model.
- [x] Examine within-group socioeconomic and STEM gradients, with Black women
  reported explicitly through average marginal effects.

### Statistical models

- [x] Fit age-23 and age-25 proportional-odds attainment models across 50
  imputations with design-adjusted covariance and race-by-gender interactions.
- [x] Fit age-23 and age-25 multinomial civilian employment-status models across
  50 imputations with design-adjusted covariance and race-by-gender
  interactions.
- [x] Fit age-23 and age-25 two-part earnings models across 50 imputations:
  positive earnings followed by log real earnings among positive exact earners,
  with design-adjusted covariance and race-by-gender interactions.
- [x] Include race-by-gender interactions and planned Black-women contrasts in
  the attainment, employment, and earnings models.
- [x] Estimate age-23 primary models and age-25 supplementary models for
  attainment, employment, and earnings.
- [x] Fit the exploratory within-age-25 sequential generalized pathway model:
  socioeconomic risk → STEM coursework and rigor → attainment → employment →
  earnings; do not interpret its scale-dependent path products as causal
  mediation.
- [x] Report employment predicted probabilities and average marginal effects
  with design- and imputation-adjusted uncertainty and diagnostics.
- [x] Report attainment marginal effects and combined two-part expected-earnings
  predictions with uncertainty and diagnostics.
- [x] Complete the harmonized complete-case and inverse-probability-of-age-25-
  observation sensitivity screen; retain full exact-model robustness in
  Milestone 8.

All primary results remain associational unless a separate identification
strategy supports causal language.

## Milestone 7 — Post-25 upward-mobility prediction

**Status: in progress**

### Prediction design

- [x] Freeze age-25 prediction features at age 23 in a versioned, checksum-
  documented table.
- [x] Freeze later-horizon prediction features at age 25 in a separate
  versioned, checksum-documented table.
- [x] Build a physically separate post-25 future-outcome staging table covering
  observed ages 26–44; future label construction remains pending.
- [x] Confirm that no post-cutoff variable enters imputation, scaling, index
  construction, feature selection, or predictor engineering.
- [x] Freeze original pre-imputation age-23 ML source features and build the
  model matrix using training-only filling, scaling, index reconstruction, and
  encoding. Keep Milestone 6 multiply imputed files out of the primary ML
  pipeline because they predate the respondent split.

### Future labels

- [x] Construct survey-weighted, same-age future real individual-earnings ranks
  over ages 30–35, requiring at least two observed rank years.
- [x] Extract the full eligible NLSY97 post-25 earnings reference population so
  future ranks are not defined only within the four analytical comparison
  groups.
- [ ] Construct future household/family-income rank when coverage permits.
- [x] Construct rank change from adolescent household-income position.
- [x] Create the primary 10-percentile-point upward-mobility target.
- [x] Create quintile-transition and bottom-to-top mobility targets.
- [ ] Define professional advancement only after occupation codes are mapped to
  a defensible occupational-status measure.

### Machine-learning models

- [x] Fit cross-validated elastic net as the primary interpretable model.
- [x] Compare the primary structural feature set with protected-group and
  starting-rank-decoupled sensitivity specifications.
- [x] Compare with a boosted-tree nonlinear sensitivity model.
- [x] Freeze the final candidate and threshold using the prespecified validation
  selection rule; retain the protected-group Elastic Net at threshold 0.36.
- [x] Freeze a 60/20/20 respondent-level train/validation/test split stratified
  by race-by-gender group and mobility label; reuse it across all 50
  imputations.
- [ ] Evaluate discrimination, prediction error, and calibration.
- [ ] Report calibration, false-positive rates, false-negative rates, and sample
  sizes by race-by-gender group, with Black women explicit.
- [ ] Interpret the model as future-position prediction, not causal proof or a
  guarantee of mobility.

## Milestone 8 — Robustness, white paper, and poster

**Status: ongoing writing; final outputs follow analysis**

### Robustness

- [ ] Compare ages 12–17 and 15–17 socioeconomic exposure windows.
- [ ] Compare separate components, equal-weight indices, and PCA/CFA indices.
- [ ] Test transcript problem-flag and transcript-selection specifications.
- [ ] Compare complete-case, imputed, and attrition-weighted estimates.
- [ ] Test age-23 versus age-25 checkpoints.
- [ ] For prediction, test alternative horizons and 5-, 10-, and 20-point
  mobility thresholds.
- [ ] Compare individual earnings, household income, and validated professional
  position targets.

### White paper

- [ ] Finalize the 250–500 word abstract after results are available; maintain a
  pre-results draft now.
- [ ] Complete introduction, significance, literature review, and conceptual
  framework.
- [ ] Convert existing data, variable, missingness, and method records into prose.
- [ ] Write results, discussion, limitations, and policy implications after
  analysis.
- [ ] Complete reproducibility and technical appendices.

### Research poster

- [ ] Create final sample-flow, trajectory, marginal-effect, and model-performance
  visuals after estimates are frozen.
- [ ] Design and verify the final research poster.

## Optional extensions — not blockers

- [ ] Decide whether time permits an ELS:2002 external-validation analysis.
  If selected, keep ELS:2002 separate from the NLSY97 respondent dataset and
  test whether the STEM-to-attainment/employment pattern appears in the later
  cohort using harmonized constructs, ages, and survey design. Use it to
  strengthen external validity and institutional STEM context—not to “balance”
  or repair the NLSY97 analytic subsample.
- ACS and Opportunity Atlas neighborhood analysis after legitimate geographic
  linkage is available.
- Restricted NLSY97 geography under an approved secure-data process.
- Policy simulation only if the primary analysis, prediction work, and reporting
  are complete and time remains.

## Immediate next sequence

1. Evaluate the sealed test partition once, including overall and race-by-
   gender discrimination, calibration, prediction error, FPR, and FNR.
2. Interpret the prediction results as future-position prediction rather than
   causal proof, then carry the frozen findings into Milestone 8 writing.
