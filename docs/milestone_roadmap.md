# Daily development roadmap

Each milestone should end with runnable code, updated documentation, and a focused Git commit.

## Milestone 1 — Repository foundation

- Establish safe data and output directories — **completed; `docs/data` also protected from Git as a safety fallback**
- Record the approved study design — **completed**
- Document the staged research and development roadmap — **completed**

## Milestone 2 — Exact NLSY97 extraction specification

- Resolve every required variable to its NLSY97 reference number — **candidate audit completed; employment, interview status, and final weight choices remain**
- Create an uploadable NLS Investigator tagset — **candidate crosswalk completed; final tagset pending remaining choices**
- Document rounds and weights — **rounds documented; final longitudinal weight pending analytic sample definition**
- Mark public versus restricted variables — **completed for current scope**

## Milestone 3 — Cohort construction

- Select the focal and comparison populations — **completed for the focal Black-female cohort**
- Retain and verify interview-age measures across all rounds — **completed**
- Convert survey rounds into person-age records — **completed**
- Retain ages 15–23 — **completed**
- Audit duplicate and missing person-age observations — **age coverage and duplicate audit completed; interview-status attrition audit remains**

## Milestone 4 — Construct development

- Build socioeconomic-risk indicators and index
- Clean the public-use STEM transcript coursework component — **completed**
- Decide whether additional authorized data are needed to represent institutional STEM quality — **pending**
- Derive attainment, employment, and earnings outcomes
- Adjust earnings to constant dollars

## Milestone 5 — Descriptive analysis

- Produce preliminary unweighted sample-flow characteristics — **completed for currently cleaned data; weighted estimates pending weight extraction**
- Visualize trajectories from ages 15–23 — **deferred until final poster development**
- Report missingness and attrition — **age coverage and STEM transcript missingness completed; confirmed interview attrition pending interview-status fields**
- Examine within-group class differences

## Modeling gate

- Review `docs/model_readiness_report.md`
- Resolve every blocked item in `outputs/tables/model_readiness_matrix.csv`
- Do not start Milestone 6 until the final merged analysis dataset, weights,
  temporal ordering, missing-data rules, and outcome definitions pass validation

## Approved design amendments

- Keep the approved labels `socioeconomic risk` and `STEM educational quality`
- Explain their measurable operational forms in the white paper
- Expand to planned race-by-gender comparisons while keeping Black girls and
  women as the focal population
- Use ages 15–17 as the common socioeconomic exposure window and age 23 as the
  primary outcome point
- Use ELS:2002 for supplementary STEM measurement validation
- Use ACS and Opportunity Atlas only after valid geographic linkage

## Milestone 6 — Statistical models

- Fit attainment and employment models
- Fit the two-part earnings model
- Fit the mediation/path model
- Generate interpretable marginal effects

## Milestone 7 — Machine learning

- Fit cross-validated elastic-net models
- Evaluate calibration and prediction error
- Compare performance across class groups

## Milestone 8 — Robustness and reporting

- Run planned sensitivity analyses
- Produce publication-ready tables and figures
- Complete methods, results, limitations, and reproducibility documentation
