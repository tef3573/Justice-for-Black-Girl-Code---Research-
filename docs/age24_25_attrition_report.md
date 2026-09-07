# Age-24/25 Missingness, Attrition, and Effective Sample Sizes

## Decision

Checkpoint-specific `SAMPLING_WEIGHT_CC` is the analysis weight for descriptive estimates and checkpoint outcome models. The archived integer is divided by 100, following NLSY97 documentation. The retained interview round supplies the weight for each exact-age observation: age 23 for the primary checkpoint and ages 24 or 25 for supplementary estimates.

A single checkpoint weight does not correct selection across the full multi-round pathway. Models that jointly use repeated adolescent exposures and later outcomes will include a custom longitudinal weight as a sensitivity analysis.

## Overall audit

The eligible comparison cohort contains 8,928 respondents. “Target-round completion” means the respondent completed the survey in the calendar year in which they turned the target age. “Exact-age observed” means an interview-age record at precisely age 24 or 25 exists. These are reported separately because interview timing can place a completed interview just before or after a birthday.

| Checkpoint | Eligible cohort | Target round completed | Exact-age observed | Exact-age coverage | Weighted effective N |
|---|---:|---:|---:|---:|---:|
| Age 24 | 8,928 | 7,397 (82.85%) | 7,129 | 79.85% | 5,891.04 |
| Age 25 | 8,928 | 7,459 (83.55%) | 7,057 | 79.05% | 5,833.16 |

Among target-year survey completions, 328 respondents at age 24 and 446 at age 25 did not have an exact-age record. These cases are timing-related noncoverage and must not automatically be classified as attrition.

## Focal and primary comparison groups

| Age | Group | Cohort N | Target round completed | Exact-age observed | Effective N | Attainment missing | Employment missing | Earnings-status missing | Exact earnings missing |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 24 | Black women | 1,162 | 1,050 (90.36%) | 1,007 (86.66%) | 860.08 | 0.70% | 0.79% | 0.30% | 22.64% |
| 24 | White women | 2,099 | 1,720 (81.94%) | 1,651 (78.66%) | 1,616.61 | 0.30% | 0.30% | 0.55% | 15.69% |
| 24 | Black men | 1,164 | 954 (81.96%) | 926 (79.55%) | 778.29 | 1.19% | 0.43% | 0.97% | 20.41% |
| 24 | White men | 2,267 | 1,828 (80.64%) | 1,759 (77.59%) | 1,741.61 | 0.40% | 0.91% | 0.51% | 13.13% |
| 25 | Black women | 1,162 | 1,048 (90.19%) | 991 (85.28%) | 847.33 | 0.71% | 0.71% | 0.40% | 20.79% |
| 25 | White women | 2,099 | 1,730 (82.42%) | 1,647 (78.47%) | 1,612.01 | 0.36% | 0.55% | 0.18% | 12.99% |
| 25 | Black men | 1,164 | 970 (83.33%) | 909 (78.09%) | 771.04 | 1.54% | 0.66% | 0.44% | 15.51% |
| 25 | White men | 2,267 | 1,848 (81.52%) | 1,744 (76.93%) | 1,724.54 | 0.52% | 0.80% | 0.46% | 11.18% |

The focal Black-women group has stronger exact-age retention than the three main comparison groups at both checkpoints. Missingness is very low for attainment, employment, and whether earnings are positive. Exact earnings amounts have substantially higher missingness, especially among Black women, so the two-part earnings strategy remains necessary and complete-case exact-earnings results require sensitivity checks.

## Target-round nonresponse reasons

At age 24, the largest nonresponse categories were refusal (950), unlocatable (311), other noninterview (83), deceased (69), inaccessible (57), unavailable during the field period (53), and illness/disability (6). At age 25, they were refusal (917), unlocatable (285), other noninterview (93), deceased (86), unavailable during the field period (55), inaccessible (28), and illness/disability (5).

## Effective sample size

Weighted effective sample size is calculated as:

`(sum of weights)^2 / sum of squared weights`

It is smaller than the raw sample because unequal survey weights reduce precision. Statistical models and uncertainty estimates must use the survey weights; effective N is a precision diagnostic, not a replacement for the raw analytic count.

## Analysis implications

- Use the age-23 retained-round weight for the primary endpoint.
- Use the age-24 or age-25 retained-round weight for each supplementary checkpoint.
- Report unweighted N, weighted estimates, and effective N together.
- Keep outcome-specific eligibility flags; do not discard respondents merely because the exact earnings amount is missing.
- Compare respondents with and without exact-age records on baseline race-gender and socioeconomic measures before final modeling.
- Use a custom longitudinal weight or response-propensity sensitivity analysis for full pathway models spanning multiple rounds.

## Retention comparisons and attrition-weight decision

Exact-age retention for Black women was significantly higher than each primary comparison group at both checkpoints. The differences ranged from 7.11 to 9.07 percentage points at age 24 and from 6.82 to 8.35 points at age 25; all six two-proportion tests had `p < .00001`. These tests describe differential exact-age coverage and are not evidence that missingness is harmless.

Baseline socioeconomic comparisons identified material imbalance. Using `|SMD| >= 0.10` as the diagnostic threshold, the all-sample or Black-women comparisons produced 16 flagged age-measure results. For Black women, examples included the socioeconomic-risk index (`SMD = 0.44` at age 24; `0.25` at age 25), poverty ratio (`-0.29`; `-0.26`), and public-assistance exposure (`0.26`; `0.31`). Some measures have small unavailable-case denominators and will be interpreted cautiously.

**Decision:** do not multiply the primary checkpoint weight by a separate attrition weight. The checkpoint cumulative-cases weight already adjusts survey-round nonresponse, while exact-age noncoverage partly reflects interview timing. However, an inverse-probability-of-exact-age-observation analysis is **required as a sensitivity analysis** because baseline imbalance exceeds the prespecified threshold. The final result will report whether that sensitivity changes substantive conclusions.

## Reproducible artifacts

- `src/build_checkpoint_weight_attrition.py`
- `data/processed/checkpoint_weights.csv`
- `data/processed/age24_25_attrition.csv`
- `outputs/tables/age24_25_missingness_attrition_effective_n.csv`
- `outputs/tables/age24_25_target_round_reasons.csv`
- `outputs/tables/age24_25_attrition_validation.json`
- `outputs/tables/age24_25_retention_baseline_balance.csv`
- `outputs/tables/age24_25_retention_group_tests.csv`
- `outputs/tables/attrition_weight_decision.json`

Validation status: **PASS**. All 21,335 exact-age checkpoint records have positive survey weights, and the full 50-test repository validation suite passes.
