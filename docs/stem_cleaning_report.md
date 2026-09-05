# STEM transcript cleaning report

## Scope

This stage creates a respondent-level component for six public-use high-school
transcript measures. It cleans math/science progression and credit fields for the
8,924 respondents represented in the approved race-by-gender comparison panel.
The component is intended for a later documented respondent-level analysis merge.
It does not contain age-varying exposures, achievement outcomes, employment,
earnings, survey weights, imputations, an index, model estimates, or findings.

## Operational boundary

The cleaned variables describe **observed STEM coursework and rigor**. They do
not directly measure institutional STEM educational quality, course availability,
teacher quality, academic support, or neighborhood resources. The broader
construct remains under review, and the approved research question is unchanged.

## Source fields

- R98602.00 / TRANS_MATHPIPE: math progression (100–800).
- R98615.00 / TRANS_PHYS_SCI_PIPE: physical-science progression (0–200).
- R98617.00 / TRANS_SCI_PIPE: life/physical-science progression (0–600).
- R98642.00 / TRANS_TOT_LIFE_PHYS_SCI: total science Carnegie credits.
- R98643.00 / TRANS_TOT_MATH: total math Carnegie credits.
- R98646.00 / TRANS_TOT_ADV_MATH: advanced-math Carnegie credits.
- R98596.00 / TRANS_STATUS: collection status.
- R98725.00 / TRANS_PROBFLAG: transcript problem flag.
- R00001.00 / PUBID: respondent merge key.

## Rules

1. Preserve raw transcript-status codes and derive `transcript_collected` only
   from statuses 1 (wave 1 complete) and 2 (wave 2 complete).
2. Preserve pipeline source codes and derive ordinal levels by dividing valid
   category codes by 100. These levels are ordered categories, not equal-interval
   measurements. Science zero remains a substantive “none” category.
3. Convert valid Carnegie-credit integers using two implied decimal places.
4. Recode -7 (“did not take course”) and -10 (“no coursework”) to 0.00 credits,
   while retaining the reason in a companion status field.
5. Keep -6 (“credits missing”) and -8 (“invalid or only pre-high-school
   coursework”) missing. Preserve their distinct companion statuses.
6. Keep -4 as no-transcript missingness. Never convert it to zero.
7. Preserve problem flags for sensitivity analyses. Flagged records are not
   automatically excluded.
8. Do not impute or standardize any value and do not construct a composite index.

## Validation

The builder requires one output row per comparison-cohort respondent; unique respondent IDs;
allowed transcript-status, pipeline, and flag values; and no observed coursework
for records without a collected transcript. Eight focused tests cover ordinal
conversion, substantive zeros, implied decimals, no-course zeros, distinct
missing statuses, invalid category rejection, and transcript flags. The entire
repository test suite is rerun after installation.

## Generated outputs

- `data/processed/stem_transcript_clean.csv`: one row per comparison-cohort respondent.
- `outputs/tables/stem_cleaning_validation.json`: aggregate counts and field-status
  distributions.

Both generated outputs are excluded from Git. The cleaning script, tests, and
this methodological report are tracked. The raw archive is read directly and is
not modified.

## Merge rule for later work

Merge this respondent-level component onto the age-eligible panel by respondent
ID. Transcript measures repeat conceptually across a respondent’s person-age rows,
but must not be misrepresented as annual observations. Final models must establish
whether transcript completion predates the selected outcome period. The merge
must report matched/unmatched counts and distinguish transcript noncollection from
item-level missingness.

## Interpretation and sensitivity requirements

- Report selection into transcript collection and compare status distributions.
- Report how the problem flag affects retained sample size and estimates.
- Consider separate progression and credit measures before any composite.
- Keep GPA outside the coursework/rigor measure; GPA is achievement.
- Do not call the resulting component a complete STEM-quality measure.
- Do not use transcript-specific school sequence numbers as external school IDs.

## Reproduction

```sh
python3 src/clean_stem_transcript.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Verified processing counts

The verified comparison-cohort processing counts are generated in
`outputs/tables/stem_cleaning_validation.json`. They are unweighted processing
counts before outcome eligibility, problem-flag sensitivity, missing-data
treatment, and statistical analysis.
