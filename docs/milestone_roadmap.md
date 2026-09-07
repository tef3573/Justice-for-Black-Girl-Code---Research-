# Daily development roadmap

Each milestone should end with runnable code, updated documentation, and a focused Git commit.

## Milestone 1 — Repository foundation

- Establish safe data and output directories — **completed; `docs/data` also protected from Git as a safety fallback**
- Record the approved study design — **completed**
- Document the staged research and development roadmap — **completed**

## Milestone 2 — Exact NLSY97 extraction specification

- Resolve every required variable to its NLSY97 reference number — **candidate audit completed; employment, interview status, and final weight choices remain**
- Resolve age-24/25 attainment, employment, earnings, interview-status, and age-specific weight fields — **planned for the within-program endpoint extension**
- Resolve post-25 adult earnings and household/family-income fields only as future prediction targets — **planned for Milestone 7; never predictor features**
- Create an uploadable NLS Investigator tagset — **candidate crosswalk completed; final tagset pending remaining choices**
- Document rounds and weights — **rounds documented; final longitudinal weight pending analytic sample definition**
- Mark public versus restricted variables — **completed for current scope**

## Milestone 3 — Cohort construction

- Select the focal and comparison populations — **completed for the focal Black-female cohort**
- Retain and verify interview-age measures across all rounds — **completed**
- Convert survey rounds into person-age records — **completed**
- Retain ages 15–23 — **completed; expand through age 25 where observations support the program endpoint**
- Audit duplicate and missing person-age observations — **age coverage and duplicate audit completed; interview-status attrition audit remains**
- Expand to approved race-by-gender comparison groups — **completed**
- Extend the explanatory person-age scaffold through age 25 — **planned**
- Build a separate post-25 outcome-label scaffold and audit later observation — **planned for prediction only; keep separate from the explanatory dataset**

## Milestone 4 — Construct development

- Build socioeconomic-risk indicators and index — **completed for the current public-use specification; 3,926 respondents meet the four-component minimum**
- Extract resolved socioeconomic fields for ages 15–17 — **completed; raw values only**
- Resolve public-assistance, household-joblessness, and final weight fields — **baseline public-assistance and parent-household joblessness proxies resolved; cumulative-cases weights used for age-year income ranks; final longitudinal model weight remains pending**
- Clean the public-use STEM transcript coursework component — **completed**
- Decide whether additional authorized data are needed to represent institutional STEM quality — **pending**
- Derive attainment, employment, and earnings outcomes — **completed at age 23 for 7,149 respondents; validation passed**
- Adjust earnings to constant dollars — **completed using annual CPI-U and a 2025-dollar target**
- Derive age-24/25 attainment, employment, and earnings checkpoints — **planned; descriptive and statistical scope remains at or below age 25**
- Preserve age-23 outcomes as the common primary checkpoint when age-25 coverage is incomplete — **approved**

## Milestone 5 — Descriptive analysis

- Produce preliminary unweighted sample-flow characteristics — **completed for currently cleaned data; weighted estimates pending weight extraction**
- Visualize trajectories from ages 15–23 — **deferred until final poster development**
- Report missingness and attrition — **age coverage and STEM transcript missingness completed; confirmed interview attrition pending interview-status fields**
- Examine within-group class differences
- Describe age-23 and age-25 checkpoint outcomes by race-by-gender group
- Report age-24/25 missingness, attrition, and effective sample sizes

## Modeling

- Review `docs/model_readiness_report.md`
- Resolve every blocked item in `outputs/tables/model_readiness_matrix.csv`
- Do not start Milestone 6 until the within-age-25 analysis dataset, weights,
  temporal ordering, missing-data rules, and outcome definitions pass validation

## Approved design amendments

- Keep the approved labels `socioeconomic risk` and `STEM educational quality`
- Explain their measurable operational forms in the white paper
- Expand to planned race-by-gender comparisons while keeping Black girls and
  women as the focal population
- Keep explanatory and inferential research inputs within the program's age-5-to-25
  boundary; available NLSY97 measurement begins in adolescence
- Use ages 15–17 as the common socioeconomic exposure window, age 23 as the
  common primary checkpoint, and age 25 as a supplementary within-bound endpoint
- Use records after age 25 only as future outcome labels for upward-mobility
  prediction; they must never be included as predictor features
- Use ELS:2002 for supplementary STEM measurement validation
- Use ACS and Opportunity Atlas only after valid geographic linkage

## Milestone 6 — Statistical models

- Fit attainment and employment models
- Fit the two-part earnings model
- Fit age-23 primary models and age-25 supplementary models where coverage permits
- Fit the mediation/path model within the age-25 boundary
- Generate interpretable marginal effects

## Milestone 7 — Machine learning

- Freeze predictor features at age 23 for age-25 prediction and at age 25 for all
  later prediction horizons
- Build post-25 future labels from observed adult economic and professional
  position; these labels are used only for supervised model training/evaluation
- Construct prediction targets: future economic-position rank, rank change from
  adolescent position, 10-point upward mobility, quintile transition, and
  professional-position advancement where valid measures exist
- Fit cross-validated elastic-net models for future position and upward mobility
- Compare elastic net with a nonlinear boosted-tree sensitivity model
- Use respondent-level temporal train/validation/test procedures and verify that
  no post-cutoff information enters preprocessing or feature engineering
- Evaluate calibration and prediction error
- Compare calibration, prediction error, false-positive rates, and false-negative
  rates across race-by-gender groups, with Black women reported explicitly

## Milestone 8 — Robustness and reporting

- Run planned sensitivity analyses, including prediction horizons, 5/10/20-point
  mobility thresholds, individual earnings versus household income, social and
  professional position definitions, separate socioeconomic components, and
  alternative index specifications
- Produce publication-ready tables and figures
- Complete methods, results, limitations, and reproducibility documentation
