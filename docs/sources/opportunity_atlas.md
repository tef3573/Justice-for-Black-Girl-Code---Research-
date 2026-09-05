# Opportunity Atlas tract characteristics

## Role

Contextual source for the neighborhood-disinvestment extension. It is not an
individual longitudinal dataset and will not be merged to NLSY97 until approved
restricted geographic identifiers are available.

## Files acquired

- Raw data: `data/raw/opportunity_atlas/tract_covariates.csv`
- Official codebook: `data/raw/opportunity_atlas/tract_covariates_codebook.pdf`
- Source: Opportunity Insights, Table 9, Neighborhood Characteristics by Census Tract
- Geography: 2010 Census tracts identified by state, county, and tract FIPS parts
- Rows: 74,044
- Columns: 38

## Candidate constructs

- Poverty: `poor_share1990`, `poor_share2000`, `poor_share2010`
- Income: `hhinc_mean2000`, `med_hhinc1990`, `med_hhinc2016`
- Employment: `emp2000`, job growth, job density, and jobs within five miles
- Education: college-graduate share and district-linked third-grade mathematics performance
- Housing/transportation: two-bedroom rent and commuting measures
- Demographic context: racial/ethnic population shares and single-parent share

## Provenance and integrity

- Data SHA-256: `270297349f75a60b39873ed5b71184ca68fc297397feeab7755221e1f6a82319`
- Codebook SHA-256: `80ace63f4e1c8c1cbb4a058418f40daf917af11fdc33066496ac5a54f8d52df4`
- Acquired: 2026-09-05

Raw data are excluded from Git. The variables combine multiple historical years;
the final index must align each measure conceptually with the NLSY97 adolescent
period and report temporal mismatch. Area-level associations must not be presented
as individual characteristics.
