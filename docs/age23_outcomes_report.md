# Age-23 outcome construction report

## Purpose

This pipeline constructs the three primary age-23 outcomes: educational
attainment, employment access, and labor earnings. The file contains one record
for every comparison-panel respondent observed at age 23. These are constructed
outcomes, not research findings.

## Analytic population

- Comparison-panel respondents observed at age 23: **7,149**
- Output respondents: **7,149**
- Duplicate respondent IDs: **0**

Race-by-gender group labels are retained for planned comparisons, with Black
girls and young Black women remaining the focal population.

## Educational attainment

The measure combines highest grade completed, highest degree received, and
postsecondary enrollment. Degree information takes priority, while completed
college grades identify some-college participation when no postsecondary degree
has been earned. The ordered categories are:

1. No high-school credential
2. High-school equivalency/GED or diploma
3. Some college, no degree
4. Associate degree
5. Bachelor's degree
6. Graduate or professional degree

GED and high-school diploma remain separate labels in the exported file but
share the same ordinal level. Current postsecondary enrollment is retained as a
separate indicator.

Observed attainment: **7,103 of 7,149**. Counts are 891 without a high-school
credential, 612 GED/equivalency, 2,049 high-school diploma, 2,011 some college,
377 associate degree, 1,141 bachelor's degree, and 22 graduate/professional
degree. Forty-six records are unresolved.

## Employment access

NLSY97 weekly employment-history status is used instead of a single job's hours.
Primary status is the week containing the 15th day of the interview month, which
serves as a reproducible proxy for status near the interview date. Annual
proportions of classified weeks are retained as secondary measures.

The categories are employed, unemployed, not in the labor force, active
military, and indeterminate not working. Active military is separated because
the BLS civilian labor-force framework does not classify active-duty service as
civilian employment.

Observed primary status: **7,096 of 7,149**. Counts are 5,231 employed, 346
unemployed, 1,312 not in the labor force, 179 active military, and 28
indeterminate not working. Fifty-three records are unresolved.

## Earnings

Labor earnings combine wage/salary/commission/tip income and net
self-employment income for the calendar year before the age-23 interview.
Routing variables distinguish legitimate zero earnings from refusal,
don't-know, bracket-only, and missing exact amounts. Valid negative net
self-employment income is preserved.

Positive-versus-zero earnings status is observed for **7,106 respondents**.
Exact combined nominal earnings are available for **5,792 respondents**.
Bracket-only respondents are retained for the participation model but do not
receive invented exact earnings.

Nominal earnings are converted with:

`real earnings = nominal earnings × (2025 CPI-U / earnings-year CPI-U)`

The official series is CPI-U, U.S. city average, all items, not seasonally
adjusted (`CUUR0000SA0`, 1982–84=100). The verified 2025 annual average is
321.943. The source's topcoded or truncated values are retained; individual
topcode flags are unavailable in the current extract.

## Files

- `src/build_age23_outcomes.py`: reproducible construction pipeline
- `config/cpi_u_annual.json`: annual CPI-U values and source metadata
- `data/processed/age23_outcomes.csv`: respondent-level outcomes
- `outputs/tables/age23_outcomes_validation.json`: validation summary
- `tests/test_build_age23_outcomes.py`: routing and classification tests

## Modeling implications

- Attainment can be modeled ordinally, with binary thresholds as sensitivity
  analyses.
- Civilian employment models should exclude or separately report active-military
  records rather than recoding them as employed.
- Earnings require a two-part model: probability of positive earnings, followed
  by log real earnings among respondents with positive exact earnings.
- The earnings period is the previous calendar year, not necessarily the exact
  respondent age-23 year.
- Final survey weights, attrition treatment, missing-data rules, and the merged
  analysis sample remain unresolved; therefore Milestone 6 is not yet open.
