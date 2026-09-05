# STEM transcript cleaning report

## Scope

This stage creates a respondent-level component for six public-use high-school
transcript measures. It cleans math/science progression and credit fields for the
1,166 respondents identified as Black and female at baseline. The component is
intended for a later documented merge with the 1,163-person age-eligible panel.
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

The builder requires one output row per focal respondent; unique respondent IDs;
allowed transcript-status, pipeline, and flag values; and no observed coursework
for records without a collected transcript. Eight focused tests cover ordinal
conversion, substantive zeros, implied decimals, no-course zeros, distinct
missing statuses, invalid category rejection, and transcript flags. The entire
repository test suite is rerun after installation.

## Generated outputs

- `data/processed/stem_transcript_clean.csv`: one row per baseline focal respondent.
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

- Baseline focal respondents retained: 1,166.
- Collected transcripts: 838 (184 from collection wave 1; 654 from wave 2).
- Noncollected transcripts: 328, retained with missing coursework values.
- Among collected transcripts, official problem flag: 106 yes and 732 no.
- Math, physical-science, and combined-science pipeline fields: 838 observed and
  328 no-transcript records each.
- Total math credits: 790 observed, 5 no-course zeros, 19 credits missing,
  24 invalid/pre-high-school, and 328 no transcript.
- Total science credits: 775 observed, 18 no-course zeros, 21 credits missing,
  24 invalid/pre-high-school, and 328 no transcript.
- Advanced-math credits: 467 observed, 329 no-course zeros, 18 credits missing,
  24 invalid/pre-high-school, and 328 no transcript.

All status distributions reconcile to 1,166. The 838 collected transcript
records reconcile to the problem-flag counts. These are unweighted processing
counts before the age-panel merge, problem-flag sensitivity rule, outcome
eligibility, missing-data treatment, and statistical analysis.
