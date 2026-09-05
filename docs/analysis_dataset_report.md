# Final analysis-dataset construction report

## Dataset role

`analysis_dataset.csv` is the respondent-level structural merge for the primary
age-23 analyses. It retains every approved comparison-panel respondent observed
at age 23 and does not delete records merely because one predictor or outcome is
missing. Outcome-specific eligibility flags define reproducible analytic samples.

The dataset is final with respect to its current cleaned components, but model
estimation remains gated on survey-weight and attrition work.

## Merge structure

The age-23 outcomes file is the merge base. Socioeconomic-risk summaries and
high-school STEM transcript measures are joined one-to-one by `respondent_id`.

- Base age-23 respondents: **7,149**
- Output rows: **7,149**
- Unique respondent IDs: **7,149**
- Socioeconomic records matched: **7,087**
- STEM records matched: **7,149**
- Demographic conflicts: **0**

The 62 respondents without a socioeconomic summary record remain in the dataset
with an explicit unmatched flag.

## Temporal ordering

- Socioeconomic-risk exposure: ages 15–17
- STEM coursework: high-school transcript history
- Attainment and employment: observed at the age-23 interview
- Earnings: previous calendar year reported at the age-23 interview

The merge validation rejects duplicate respondent keys, demographic conflicts,
records outside age 23, and invalid socioeconomic exposure-window counts.

## Observed component flow

- Socioeconomic-risk index observed: **3,131**
- High-school transcript collected: **5,179**
- Attainment complete-case eligibility: **2,285**
- Civilian employment complete-case eligibility: **2,210**
- Earnings participation complete-case eligibility: **2,278**
- Positive exact-earnings complete-case eligibility: **1,489**

These eligibility counts are processing results, not findings. They are not a
single universal sample: each outcome uses the largest defensible sample for its
measurement requirements.

## Generated files

- `data/processed/analysis_dataset.csv`
- `outputs/tables/analysis_merge_validation.json`
- `outputs/tables/analysis_sample_flow.csv`
- `outputs/tables/missingness_by_group.csv`
- `outputs/tables/missingness_patterns.csv`

Generated data and tables remain excluded from Git. The tracked builder, tests,
and documentation reproduce them.
