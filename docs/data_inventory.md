# Data inventory

## Primary source acquired

**Dataset:** National Longitudinal Survey of Youth 1997 (NLSY97)  
**Release:** Rounds 1–21, 1997–2023  
**Release date:** January 23, 2026  
**Official package update:** February 5, 2026  
**Publisher:** U.S. Bureau of Labor Statistics, National Longitudinal Surveys  
**Access level:** Public use  
**Local archive:** `data/raw/nlsy97_all_1997-2023.zip`  
**Compressed size:** Approximately 453 MB  
**Uncompressed size:** Approximately 17 GB  
**SHA-256:** `8c513e4804e5b07fce0e6b913258747dcf8707c73bb9ae54cce88dbff6d23c28`

## Package contents

- Complete public-use CSV
- Plain-text data file
- Full codebook
- NLSY97 tagset
- R import program
- SAS import program and supporting definition file

## Storage decision

The complete package remains compressed because the uncompressed files require more disk space than is currently available. A focused research extract will be used for analysis. The archive and all future raw data are excluded from Git by `.gitignore`.

## Focused extract scope

The focused extract should contain:

- Respondent identifier, birth date, interview dates, race, sex, and survey weights
- Adolescent household income, poverty ratio, parental education, parental employment, public assistance, and family structure
- High-school transcript mathematics and science course measures
- Highest grade and credential measures
- Employment status, work hours, weeks worked, and job tenure
- Wage, salary, self-employment, hourly-pay, and compensation measures

## Core cohort extract created

The first focused file, `data/interim/nlsy97_core_cohort.csv`, contains 8,984 respondents and 27 source variables covering respondent ID, baseline demographics, birth month/year, sample type, and age at interview across 21 rounds. It also contains a derived cohort flag.

- Full NLSY97 respondents: 8,984
- Black female respondents: 1,166
- Black female interview-age observations before age filtering: 21,902
- Observed age range before filtering: 12–44

The interim file is excluded from Git. It can be reproduced from the official archive with `src/build_core_cohort.py`.

## Restricted data boundary

Restricted-use geocode and school-survey files have not been acquired. They must not be stored in this public GitHub repository. Any future request for restricted data will require a separate approved access process and secure storage plan.

## Approved multi-source strategy

- NLSY97 remains the primary individual longitudinal dataset and will be expanded
  to documented race-by-gender comparisons.
- ELS:2002 is the preferred supplementary cohort for validating broader STEM
  curricular and school-context measures with later attainment, employment, and
  earnings.
- ACS five-year estimates and Opportunity Atlas are approved candidates for the
  neighborhood extension, but an individual-level merge requires restricted
  NLSY97 geographic identifiers and secure storage.
- CPS ASEC may provide national benchmarks; PSID or SIPP may support a separate
  robustness study. They cannot be merged person-to-person with NLSY97.

See `docs/measurement_plan.md` for operational source and compatibility rules.

## External-source acquisition status

- Opportunity Atlas tract characteristics — **acquired and checksum-verified**;
  74,044 tracts and 38 fields. See `docs/sources/opportunity_atlas.md`.
- ELS:2002 public use — **extraction specification complete; official NCES
  Online Codebook extract pending**. See `docs/sources/els2002.md`.
- ACS five-year estimates — **indicator specification complete; pull deferred
  until the restricted geography level and relevant years are known**. See
  `docs/sources/acs_neighborhood.md`.
- Machine-readable registry: `config/external_sources.json`.
