# Research design

## Approved focus and operational language

The approved construct names remain **socioeconomic risk** and **STEM educational
quality**. The white paper will explain that socioeconomic risk is operationalized
through adolescent economic disadvantage and instability, while the available
transcript data operationalize STEM educational quality through observed STEM
curricular exposure and rigor. This narrows the measurement claim without changing
the approved research focus.

## Objective and questions

Estimate how adolescent socioeconomic risk is associated with STEM educational
quality, educational attainment, labor-market attachment, and earnings by age 23
among Black girls and young Black women, and determine how these trajectories
differ across relevant race-by-gender groups.

**Primary approved question.** How do structural inequalities shape the economic
and educational trajectories of Black girls and young Black women?

**Operational pathway question.** To what extent are associations between
socioeconomic risk and earnings by age 23 transmitted through STEM educational
quality, educational attainment, and labor-market attachment?

**Comparative question.** How do these trajectories differ for Black girls and
young Black women relative to White women and Black men with similar observed
adolescent economic circumstances?

## Population, timing, and pathway

Black girls and young Black women remain the focal population. White women provide
the primary racial contrast and Black men the primary gender contrast. White men
provide a combined benchmark. Other race-by-gender groups are secondary and depend
on source coding and effective sample size.

Respondents contribute observations from ages 15–23. Ages 15–17 form the common
adolescent exposure window; earlier ages may be used in sensitivity analyses.
Age 23 is the primary outcome point. Prior-calendar-year income reported at age 23
will be labeled accordingly. Age-24/25 measures may provide supplementary
within-program checkpoints where coverage permits.

The pathway is: socioeconomic risk → STEM educational quality → educational
attainment → labor-market attachment → earnings. Neighborhood disinvestment
remains a structural exposure for a geographic-data extension; household measures
will not be relabeled as neighborhood conditions.

The explanatory and inferential research period ends at age 25 to remain within
the program's age-5-to-25 scope. Records after age 25 are not additional exposures
or extensions of the focal developmental population. They are used only as future
outcome labels for a distinct supervised prediction analysis asking whether
conditions observed by age 23 or 25 predict later upward movement in economic,
social-class, or professional position.

## Combined hypothesis

Greater adolescent socioeconomic risk will be associated with lower STEM
educational quality, lower attainment, weaker labor-market attachment, and lower
earnings by age 23; STEM educational quality, attainment, and labor-market
attachment will partially account for this association; and these pathways will
differ for Black women relative to White women and Black men because race and
gender jointly structure educational and economic opportunity.

Component hypotheses will test each pathway link and race-by-gender interaction.
All hypotheses concern associations unless a later identification strategy
supports causal interpretation.

## Measurement decisions

The primary class measure is average household-income rank during ages 15–17.
Separate socioeconomic measures include average poverty ratio, proportion of
observed adolescent years below poverty, income instability, low parental
education, household joblessness, and public-assistance exposure. A transparent,
sign-aligned standardized summary is the primary socioeconomic-risk index; PCA or
CFA scores are sensitivity analyses.

The transcript component retains highest mathematics and science levels, total
mathematics and science credits, and advanced-mathematics credits. Component
models are primary; a standardized STEM curricular-exposure-and-rigor index is
secondary. These fields do not directly measure teaching quality, academic
support, or course availability.

Labor-market status follows BLS-compatible employed, unemployed, and not-in-labor-
force categories. Full-time employment (35 or more usual weekly hours), hours,
weeks worked, and positive annual earnings are secondary outcomes.

Earnings routing will distinguish valid zero, positive earnings, refusal,
inapplicability, and non-interview. Monetary values will be converted to constant
2025 dollars using one official annual price series and `nominal value × (2025
index / source-year index)`.

## Data strategy

- **NLSY97:** primary individual panel for demographics, socioeconomic measures,
  transcripts, attainment, employment, and earnings.
- **ELS:2002:** supplementary cohort for validating broader STEM curricular and
  school-context measures with later education and labor-market outcomes.
- **ACS and Opportunity Atlas:** neighborhood extension, linked only through
  approved restricted NLSY97 geographic identifiers.

These sources contain different people and must never be merged person-to-person
without a legitimate shared identifier. External sources may provide contextual
geography, validation, or population benchmarks, but cannot fill an NLSY97
respondent's missing values.

## Planned methods and boundaries

Methods include survey-weighted descriptions, race-by-gender interactions and
planned contrasts, attainment and multinomial labor-force models, a two-part
earnings model, generalized structural equation/path modeling, mechanism-specific
multiple imputation with complete-case sensitivity analysis, and elastic net as
a complementary predictive analysis. Outcomes, race/gender classifications,
transcript noncollection, and bracket-only exact earnings will not be imputed.
Eligible item-level predictors may be imputed within their observed data
structures; predictive preprocessing for machine learning will be fitted inside
each training fold.

Primary estimates are associational. Restricted data must never enter the public
repository. Interview-status variables are existing quantitative metadata used
to measure attrition; this project does not conduct interviews or collect surveys.

## Predictive upward-mobility extension

The prediction analysis will freeze all features at a declared cutoff. An age-25
target model may use information observed only through age 23; models for later
adult horizons may use information observed only through age 25. Post-cutoff
earnings, household income, occupational position, and related measures serve
only as labels used to train and evaluate predictions.

Primary targets are future economic-position rank and an indicator that future
rank exceeds adolescent household-income rank by at least 10 percentile points.
Quintile transitions are secondary targets. Professional advancement may be added
only after a defensible occupation-status measure is specified. The model will be
described as prediction, not causal estimation or guaranteed future mobility.
