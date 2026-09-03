# Justice for Black Girl Code — Research

## Research question

How do socioeconomic risk and STEM educational quality interact to shape long-term academic and economic outcomes for Black girls and young Black women?

## Study design

This project uses the National Longitudinal Survey of Youth 1997 (NLSY97) to study Black girls and young Black women from ages 15 through 23. The proposed pathway is:

> Socioeconomic risk → STEM educational opportunity → educational attainment → employment access → earnings by age 23

The primary explanatory method will be generalized structural equation modeling. A two-part earnings model will account for respondents with zero earnings, and elastic net will provide a complementary machine-learning analysis.

## Current milestone

The official NLSY97 public-use package for rounds 1–21 (1997–2023) is stored locally in the Git-ignored `data/raw/` directory. A reproducible core cohort extract now identifies 1,166 Black female respondents and retains interview ages across every round. See `docs/data_inventory.md` for the source, checksum, file inventory, and current extraction status.

## Repository structure

- `config/`: future study and variable specifications
- `data/`: local raw, interim, and processed data
- `docs/`: research and data documentation
- `src/`: future reusable analysis code
- `tests/`: future automated checks
- `outputs/`: generated tables, figures, and model files
