# Final analysis-dataset construction report

## Dataset role

`analysis_dataset.csv` is the respondent-level structural merge for the primary
age-23 analyses. It retains every approved comparison-panel respondent observed
at age 23 and does not delete records merely because one predictor or outcome is
missing. Outcome-specific eligibility flags define reproducible analytic samples.

The dataset is final with respect to its current cleaned components, but model
estimation remains gated on survey-weight and attrition work.

The same 7,149-row age-23 base now includes suffixed age-24 and age-25
supplementary checkpoint columns. Respondents missing a later checkpoint remain
in the file with explicit `age24_record_matched` and `age25_record_matched` flags.

The file now also includes checkpoint-specific `SAMPLING_WEIGHT_CC`, `VSTRAT`,
and `VPSU` fields for ages 23–25. All age-23 rows have primary design fields;
6,400 match age-24 weights and 6,292 match age-25 weights. The aliases
`analysis_weight`, `analysis_vstrat`, and `analysis_vpsu` point to the primary
age-23 design.

## Frozen model-ready version

Milestone 5D freezes `model_ready_imputations_v1.csv.gz` and
`analysis_base_complete_case_v1.csv.gz`. The imputed file uses the unique key
`respondent_id + imputation_id + checkpoint_age` and contains 992,050 rows:
357,450 at age 23, 320,000 at age 24, and 314,600 at age 25. Each checkpoint is
normalized to the same outcome and survey-design column names, which prevents
accidental use of later-checkpoint suffixes.

The freeze manifest records source and output SHA-256 checksums, schema, row
counts, eligibility counts, temporal boundaries, and validation results. No
post-25 field appears in the frozen data.

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

## Supplementary checkpoint matches on the age-23 base

| Checkpoint | Matched | Attainment | Employment | Earnings status | Exact real earnings |
|---|---:|---:|---:|---:|---:|
| Age 24 | 6,400 | 6,360 | 6,363 | 6,369 | 5,352 |
| Age 25 | 6,292 | 6,247 | 6,258 | 6,269 | 5,406 |

These counts are lower than the full age-specific panels because the merged
analysis dataset deliberately retains the established age-23 base. Respondents
observed only at age 24 or 25 are not silently added to the primary sample.

## Temporal ordering

- Socioeconomic-risk exposure: ages 15–17
- STEM coursework: high-school transcript history
- Primary attainment and employment: observed at the age-23 interview
- Supplementary attainment and employment: observed at ages 24 and 25
- Earnings: previous calendar year reported at each checkpoint interview

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
