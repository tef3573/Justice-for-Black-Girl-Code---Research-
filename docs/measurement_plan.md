# Measurement and data-source plan

## Socioeconomic risk

| Measure | Primary operational rule | Role |
|---|---|---|
| Average household-income rank | Mean survey-weighted percentile rank of nominal household income within survey-year and age across observed ages 15–17 | Primary class predictor |
| Average poverty ratio | Mean NLSY97 income-to-poverty ratio across ages 15–17 | Predictor/component |
| Proportion of years in poverty | Eligible observed ages below 100% of poverty divided by observed eligible ages | Predictor/component |
| Income instability | Within-person standard deviation of annual household-income rank; require at least two observations | Separate predictor/component |
| Low parental education | Highest available parent/guardian education is high school/GED or less | Predictor/control |
| Household joblessness | Baseline indicator that the responding parent was not employed and no employed spouse was present; this is a parent-household proxy, not an all-adult measure | Predictor/component |
| Public-assistance exposure | Baseline parent report of any prior-year AFDC, food-stamp, or SSI receipt by the parent or spouse | Predictor/component |
| Socioeconomic-risk index | Mean of available sign-aligned standardized components with a minimum count | Main composite predictor |

Ages 10–17 are not the primary window because NLSY97 does not observe every
respondent throughout it. Ages 15–17 provide a common pre-outcome window; ages
12–17 are a sensitivity analysis. ACS and CPS cannot produce within-person
adolescent averages for NLSY97 respondents.

The current risk index averages available sign-aligned z-scores for low income
rank, low poverty ratio, poverty persistence, low parental education, baseline
public assistance, and baseline parent-household joblessness. At least four of
six components are required. The components remain available separately because
income rank and poverty measures overlap conceptually; PCA/CFA and alternative
component sets are planned sensitivity analyses rather than replacements for the
approved construct.

NLSY97 cumulative-cases cross-sectional weights are used only to calculate
survey-year-by-age household-income ranks at this stage. The final weight for
multi-round outcome models remains a modeling-gate decision.

## STEM educational quality

Quantitative indicators are highest mathematics progression, highest science
progression, mathematics Carnegie credits, advanced-mathematics credits, and
science Carnegie credits. Use component models first and a sign-aligned
standardized summary second; use PCA/CFA as sensitivity analyses. In methods and
results, state that this operationalizes the approved construct through STEM
curricular exposure and rigor, not complete institutional quality.

## Comparison structure

1. Black women versus White women: racial contrast among women.
2. Black women versus Black men: gender contrast among Black respondents.
3. Black women versus White men: combined benchmark.
4. Additional groups: secondary, dependent on coding and sample size.

Models will use race-by-gender interactions and planned contrasts. Within-group
economic gradients remain important secondary estimates.

## Source compatibility

| Source | Proper use | Improper use |
|---|---|---|
| NLSY97 | Primary individual longitudinal analysis | Public neighborhood linkage without geography |
| ELS:2002 | Supplementary cohort and STEM measurement validation | Person-level merge to NLSY97 |
| HSLS:09 | Later-cohort STEM robustness | Primary age-23 earnings trajectory with current follow-ups |
| ACS | Area context after valid geographic linkage | Individual longitudinal history |
| Opportunity Atlas | Area mobility/context and external comparison | Substitution for individual NLSY97 outcomes |
| CPS ASEC | National benchmarks | Person-level merge to NLSY97 |
| PSID/SIPP | Separate longitudinal robustness study | Filling missing NLSY97 records |

Interview completion, retention, and weights are existing quantitative fields.
Using them does not involve conducting interviews or collecting new responses.

## Upward-mobility prediction boundary

The main explanatory measures remain within age 25. For prediction, features are
frozen at age 23 when predicting age-25 position and at age 25 when predicting
later position. Records after age 25 provide labels only.

The primary future economic target is percentile rank in real individual labor
earnings, averaged within a prespecified later age window when repeated
observations are available. Primary upward mobility is future earnings rank minus
average adolescent household-income rank. A gain of at least 10 percentile points
is the primary binary target; 5- and 20-point definitions and quintile transitions
are sensitivity outcomes. Adult household/family-income rank is a robustness
target because it is more comparable to adolescent household income. A
professional-position target will be added only after occupation codes can be
mapped consistently to a documented occupational-status measure.
