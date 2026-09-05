# ACS neighborhood acquisition specification

## Role

The ACS five-year estimates will provide geographically and temporally aligned
neighborhood indicators after an approved NLSY97 county or tract key is available.

## Candidate ACS concepts

- Poverty and income-to-poverty distribution
- Median household income
- Employment status and employment-population ratio
- Educational attainment
- Public-assistance receipt
- Housing-cost burden and rent
- Vacancy and occupancy
- Household structure
- Race/ethnicity composition

## Status and merge gate

The source is approved but a full nationwide multi-year pull is intentionally
deferred until geography level and reference years are known. Pulling it now would
create data that cannot yet be linked and could select the wrong ACS vintage.
ACS records will be joined by validated FIPS geography and year, never by person.
