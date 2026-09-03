# Cohort definition

## Focal population

The focal population is respondents classified in the NLSY97 baseline variables as Black and female.

- `KEY_RACE_ETHNICITY_1997 = 1` identifies Black respondents.
- `KEY_SEX_1997 = 2` identifies female respondents.

These codes were verified against the official NLSY97 public-use codebook. The baseline variables are used because race and sex are treated as stable cohort-defining characteristics in this study.

## Age construction

The official created variables `CV_AGE_INT_DATE_<year>` provide age at the date of interview for each survey round. These measures are retained for the initial longitudinal restructuring. Birth month and birth year are also retained so that age can later be independently verified against interview dates.

## Current processing boundary

The first half of cohort construction creates a small respondent-level file containing:

- Public respondent ID
- Baseline sex
- Baseline race/ethnicity
- Birth month and year
- Sample type
- Age at each interview
- A reproducible Black-female indicator

The final age 15–23 person-age filter, duplicate resolution, and sample-flow audit belong to the second half of cohort construction.
