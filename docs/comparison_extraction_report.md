# Comparison cohort and socioeconomic extraction report

## Completed scope

The NLSY97 cohort has been expanded from the earlier Black-female scaffold to a
race-by-gender comparison panel covering ages 15–23. A separate raw socioeconomic
extract covers the common adolescent exposure window, ages 15–17. No income,
poverty, parental-education, household-size, or weight value has yet been cleaned,
ranked, standardized, imputed, or combined into an index.

## Race and ethnicity rule

Baseline ethnicity and race are combined into mutually exclusive categories:
Hispanic of any race, followed by non-Hispanic White, Black, American Indian or
Alaska Native, Asian or Pacific Islander, and other race. Unknown source responses
remain unknown. This avoids treating the broad source category “non-Black/non-
Hispanic” as White.

The earlier focal scaffold used the NLSY97 four-category combined field and
contained 1,166 Black female respondents. The new mutually exclusive definition
contains 1,165 non-Hispanic Black women in the full source and 1,162 in the
age-eligible panel. The difference is definitional, not data loss, and must be
reported when comparing old and new files.

## Verified counts

- Source respondents: 8,984
- Respondents with at least one age 15–23 record: 8,924
- Unique respondent-age records: 62,883
- Raw socioeconomic records at ages 15–17: 18,699
- Respondents with at least one socioeconomic-window record: 8,828

Primary age-panel groups:

- Non-Hispanic Black women: 1,162
- Non-Hispanic Black men: 1,164
- Non-Hispanic White women: 2,098
- Non-Hispanic White men: 2,265
- Hispanic women: 917
- Hispanic men: 973

Asian/Pacific Islander and American Indian/Alaska Native groups are retained but
their smaller sample sizes require explicit precision and disclosure review before
group-specific modeling.

## Fields extracted

The raw ages 15–17 file includes respondent ID; baseline sex, ethnicity, and race;
race-by-gender classifications; survey year and age; household/family income;
income-to-poverty ratio; household size; baseline biological and residential
parent education; interview date fields; and available sampling-weight fields for
1997–2002. Seventy-seven source variables were selected in total, including age
fields used to construct the panel.

## Outputs

- `data/interim/nlsy97_comparison_age15_23.csv`
- `data/interim/nlsy97_socioeconomic_raw_age15_17.csv`
- `outputs/tables/comparison_extraction_validation.json`

Generated files are Git-ignored. Reproduce with:

```sh
python3 src/build_comparison_extract.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Remaining extraction decisions

Public-assistance routing, household-adult joblessness, and the final analytic
weight require dedicated codebook review before inclusion. Interview-date and
age availability are extracted quantitative metadata, but formal attrition status
still requires a defensible round-participation rule. These unresolved items do
not invalidate the completed comparison panel or the raw resolved-variable extract.
