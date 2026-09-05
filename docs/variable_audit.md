# Day 3 — Candidate-variable audit (2026-09-04)

## What is clean, and what is not

Day 2 produced an age-filtered, deduplicated demographic scaffold. It did not
clean or harmonize substantive predictors/outcomes. Day 3 maps exact codebook
references, inventories coding and timing risks, and profiles raw availability.
No values are recoded, imputed, standardized, indexed, or merged into the panel.
No charts, models or substantive research findings are produced.

## Principal finding: measurement scope

The initial Day 3 audit is complete: 180 candidate variable-wave entries, an
official-codebook crosswalk, raw availability profiles, and ten passing automated
tests across Days 2 and 3. This is not completion of substantive data cleaning.

## Verified raw availability (denominator: 1,166 baseline focal respondents)

- Math progression: 838 nonnegative records; 328 coded -4.
- Science progression: 838 nonnegative records; 328 coded -4.
- Total math credits: 790 nonnegative; -4: 328, -6: 19, -7: 5, -8: 24.
- Total science credits: 775 nonnegative; -4: 328, -6: 21, -7: 18, -8: 24.
- Advanced math credits: 467 nonnegative; -4: 328, -6: 18, -7: 329, -8: 24.

These are marginal raw-code counts, not final eligible or complete-case counts.
In particular, the 329 advanced-math records coded -7 represent no course taken,
not ordinary item nonresponse. The profiled denominator precedes Day 2's age-based
restriction to 1,163 respondents. Joint panel/transcript availability and quality
flag distributions must be evaluated before selecting a model sample. No excluded
case or valid zero has been reconstructed in this audit.

## Measurement interpretation

The public-use transcript data support math/science coursework and rigor measures.
They do not, by themselves, establish instructional quality, availability of
courses not taken, teacher support, or neighborhood disinvestment. The approved
research question is unchanged. Any narrower operationalization must be explicitly
approved and justified, not silently substituted for STEM educational quality.

## STEM shortlist — HSTR transcript module

- R98602.00 / TRANS_MATHPIPE: mathematics curriculum progression, coded 100–800.
  Treat as ordered categories, not equal-interval quantities. Code 100 is no math;
  -4 denotes a skipped record, not the lowest course level.
- R98617.00 / TRANS_SCI_PIPE: life/physical science curriculum progression,
  categories 0–600. Zero is a substantive category, not missing.
- R98615.00 / TRANS_PHYS_SCI_PIPE: alternative physical-science progression;
  avoid mechanically combining overlapping progression measures.
- R98643.00 / TRANS_TOT_MATH: total math Carnegie credits.
- R98646.00 / TRANS_TOT_ADV_MATH: advanced-math Carnegie credits.
- R98642.00 / TRANS_TOT_LIFE_PHYS_SCI: life/physical science Carnegie credits.
  For these credit fields the codebook specifies two implied decimals. Confirm
  raw serialization before dividing valid values by 100. Their -7 category means
  did not take the course; -6 means credits missing despite course participation;
  -8 means invalid credits or only pre-high-school coursework. Do not collapse
  these into the same missing category or automatically recode all to zero.
- R98722.00 / TRANS_CRD_GPA_MATH and R98724.00 / TRANS_CRD_GPA_LP_SCI:
  achievement candidates, kept separate from opportunity and quality. GPA is not
  a direct measure of institutional resources. TRANS_GPA is also inventoried.
- R98596.00 / TRANS_STATUS: transcript collection status; codes 1–2 indicate
  completed collection waves; other categories identify noncollection reasons.
- R98725.00 / TRANS_PROBFLAG: transcript completeness/problem flag. Keep it for
  sensitivity analysis; do not discard flagged respondents without reporting impact.

Transcript totals are not annual exposures. Establish course/term timing before
using them to predict adolescent outcomes. The official appendix explains that
transcript variables are associated with round 3 despite two collection waves.
HSTR is a module label, not a calendar year. Transcript-specific school sequence
numbers are not external school identifiers.

## Other constructs — initial shortlist, not final selection

- Household economic resources: CV_INCOME_GROSS_YR, CV_HH_POV_RATIO,
  CV_HH_INCOME_SOURCE, CV_HH_SIZE. Baseline examples: R12045.00, R12049.00,
  R12046.00, R12054.00. Household income is prior-year, topcoded and can contain
  genuine negative amounts. Do not apply a blanket negative-to-missing rule.
  Poverty ratio has two implied decimal places. Parent/youth income sources and
  eligibility vary across rounds and must be harmonized before longitudinal use.
- Parental education: R13024.00–R13027.00 / CV_HGC_BIO_DAD, CV_HGC_BIO_MOM,
  CV_HGC_RES_DAD, CV_HGC_RES_MOM. Biological and residential parent measures
  are not interchangeable. Absence of a parent is not zero schooling.
- Attainment: CV_HGC_EVER, CV_HIGHEST_DEGREE_EVER, CV_ENROLLSTAT. Baseline
  references R12044.00, R12057.00, R12014.00. Later revised/suffixed versions
  require additional review; the exact-name search is not an exhaustive inventory.
- Earnings: YINC-1700 (baseline R04902.00) is pretax wage/salary/commission/tip
  income for the previous calendar year, not total income or all self-employment.
  Receipt and follow-up screeners YINC-1400, YINC-1500, YINC-1600 are inventoried
  to support later zero-versus-missing derivation. Never turn all valid skips into
  zero earnings. Confirm each round's routing, topcodes and reference period.
- Employment: CV_HRS_PER_WEEK.01 (baseline R12091.01) measures regular hours at
  job 01, not total annual hours, unemployment or access to job opportunities.
  This is a discovery candidate only. Full employment histories and aggregation
  across jobs still need specification; no employment-access measure is finalized.
- Timing/design: CV_INTERVIEW_CMONTH, CV_INTERVIEW_DATE month/year variants,
  SAMPLING_WEIGHT and PUBID. No single-round weight has been selected for a
  pooled longitudinal/transcript model. Custom weighting and design effects remain
  decisions after the analytic sample is defined.

## Gaps and decisions before cleaning

1. Review whether coursework/rigor is an acceptable partial operationalization
   of STEM educational quality; otherwise investigate authorized school data.
2. Search adolescent support and course-offering items and inspect their universes.
   A keyword miss is not evidence that a measure does not exist.
3. Specify household instability using repeated compatible measures; low income
   at one wave does not establish instability. Household resources do not directly
   measure neighborhood disinvestment or district resources.
4. Resolve employment history, earnings zero routing, actual dates, and the age-23
   outcome/reference-period rule. Current design names age-23 earnings, but prior-year
   income reported at age 23 is not necessarily income earned entirely at age 23.
5. Test joint availability and transcript-selection patterns before choosing models.
   Marginal nonnegative counts are not a final eligible sample.
6. Confirm missing-value meanings, unit scaling, topcodes and time order per field.

## Reproduction and provenance

Run from the repository root:

```sh
python3 src/audit_variables.py --codebook data/raw/nlsy97_all_1997-2023/nlsy97_all_1997-2023.cdb --data data/raw/nlsy97_all_1997-2023.zip --crosswalk docs/day3_variable_crosswalk.json
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Candidate codebook entries, discovery hits, manifest and raw profiles go into
Git-ignored data/interim/day3. The tracked crosswalk contains metadata only:
construct, source name/reference, wave and codebook line. Candidates are explicitly
marked as requiring further timing, eligibility and coding review. The annual
search window is 1997–2009, a bounded initial scan rather than proof of full coverage.

The codebook SHA256 is
`a0419e898c561b75c445312b8bde8feaa06695ef9401cb57f5dd086eb70d1c4e`.
The expanded source package is present locally; older storage notes saying only
the compressed archive exists are now outdated. Raw files have not been changed.
The system unzip utility could not list the archive, but Python's ZIP reader
successfully read its directory; this alone is not evidence of corruption.
The expanded CSV was flagged dataless (cloud placeholder), causing read stalls.
The audit supports direct ZIP streaming to avoid requiring the 8 GB CSV locally.

## Sources

- Official local release codebook: nlsy97_all_1997-2023.cdb; exact entries are
  preserved in candidate_codebook.json and locatable by the crosswalk line numbers.
- [NLSY97 transcript collection and timing](https://www.nlsinfo.org/content/cohorts/nlsy97/other-documentation/codebook-supplement/appendix-11-collection-of-transcript-data)
- [NLSY97 school/transcript access, status and quality flags](https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/education/school-transcript-surveys)
- [NLSY97 weights and design](https://nlsinfo.org/content/cohorts/nlsy97/using-and-understanding-the-data/sample-weights-design-effects)

## White-paper language

The measurement audit distinguished transcript-based coursework and rigor from
institutional educational quality and student achievement. Candidate variables
were mapped to official reference numbers and reviewed for special codes, units,
reference periods and transcript coverage. The availability of these proxies does
not establish that the full STEM-quality or neighborhood-disinvestment constructs
are observed. Final operational definitions and coding decisions remain subject
to the variable and sample-feasibility review.
