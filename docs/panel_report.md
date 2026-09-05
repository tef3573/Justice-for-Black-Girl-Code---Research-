# Observed-age cohort scaffold

The observed ages cohort construction is complete. This is an unweighted demographic/interview-age scaffold, not the final model-ready dataset. Educational, employment, earnings, weighting and item-missingness work remains for later stages.

## Reproduce

From the repository root:

```sh
python3 src/build_age_panel.py
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_age_panel.py' -v
```

## Verified sample flow

| Stage | Count |
|---|---:|
| Source respondents | 8,984 |
| Baseline Black female respondents | 1,166 |
| Potential respondent-round slots (21 rounds) | 24,486 |
| Slots with nonnegative interview age, all ages | 21,902 |
| Slots with source missing-age code -5 | 2,584 |
| Observations ages 15–23 before deduplication | 8,820 |
| Repeated-age records removed | 472 |
| Retained respondent-age observations | 8,348 |
| Respondents with at least one eligible observation | 1,163 |
| Focal respondents without eligible observations | 3 |
| Respondents observed at all nine ages | 282 |
| Retained respondents with incomplete age coverage | 881 |

## Decisions

- Cohort membership: baseline race/ethnicity code 1 and sex code 2. These
  are source classifications, not comprehensive measures of gender identity.
- Ages are taken from CV_AGE_INT_DATE variables; retain 15 through 23 inclusive.
- No interpolation, forward filling, or missing-age imputation.
- For repeated ages, retain the highest survey round with a valid eligible age.
  Selection does not depend on later outcomes. Every discarded round is audited.
- `survey_year` is the survey-wave label, NOT a verified actual interview year.
  Actual interview dates and income reference periods must be added before
  inflation adjustment or temporal pathway estimation. `survey_round` indexes
  the chronologically ordered age fields in the supplied core extract.
- Valid age availability is not proof of a fully completed interview; completion
  status has not yet been extracted. A skipped age is not automatically attrition.
- Preserve all otherwise eligible respondents, including incomplete trajectories.
  Age-coverage tables use the initial 1,166 as their fixed descriptive denominator.

## Validation and coverage

The build checks respondent-ID validity and uniqueness, source demographic codes,
agreement with the focal flag, nonempty age metadata, plausible ages, unique final
respondent-age keys, inclusion boundaries, and count reconciliation. No decreasing
age sequence was found across valid source observations. Six synthetic tests cover
boundary ages, missing codes, later-round tie-breaking, zero eligible records,
duplicate IDs, flag disagreement, demographic exclusion, and reversal detection.

Age and trajectory coverage are generated in `outputs/tables/day2_age_coverage.csv`
and `day2_trajectory_coverage.csv`. Respondent-level first/last age and internal
gaps are retained in the ignored interim coverage file. Confirmed nonresponse,
temporary gaps versus permanent attrition, and attrition bias cannot be determined
from the current extract alone. Those require interview-status and covariate audits.

## Outputs and provenance

- `data/interim/nlsy97_black_female_age15_23.csv`: cohort scaffold.
- `data/interim/day2_respondent_coverage.csv`: first/last age and missing-age list.
- `data/interim/day2_duplicate_audit.csv`: retained and discarded rounds.
- `data/interim/day2_age_reversals.csv`: source reversals (empty in this run).
- `outputs/tables/day2_sample_flow.csv`: aggregate sample flow.
- `outputs/tables/day2_age_coverage.csv`: fixed-denominator age coverage.
- `outputs/tables/day2_trajectory_coverage.csv`: observed-age count distribution.
- `outputs/tables/day2_validation.json`: counts, validation and input checksum.

All generated outputs are Git-ignored. Source data are unchanged. The input core
extract SHA256 is
`58bac6f76e0842fa2c5b03bae66c0ec79ebbd3c333485fb54bb16cd364853b82`.

## White paper methods text

The initial cohort included 1,166 respondents classified as Black and female at
baseline. Restructuring the available interview-age measures yielded 8,820
observations at ages 15–23. For repeated observations at the same age, the later
survey round was retained, removing 472 records. The resulting unbalanced cohort
scaffold contained 8,348 respondent-age observations from 1,163 respondents; 282
had observations at every age from 15 through 23. These are unweighted cohort
construction counts, before outcome-specific exclusions and missing-data treatment.

## Next step

Audit socioeconomic, STEM, attainment, employment, earnings, interview-date/status
and survey-design fields. Do not estimate models using this scaffold alone.
