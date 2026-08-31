<a id="source-skills-deep-research-templates-evidence-assessment-template-md"></a>

## SOURCE: skills/deep-research/templates/evidence_assessment_template.md

<!-- SOURCE-CONTENT-BEGIN bytes=3775 -->
# Evidence Assessment Template

## Purpose
Per-source quality assessment card. Used by the source_verification_agent to systematically evaluate each source entering the research pipeline.

## Assessment Card

```markdown
## Evidence Assessment Card

### Source Identification
- **Citation (APA 7.0)**: [full reference]
- **DOI/URL**: [link]
- **Type**: [journal article / book / report / web / conference paper / thesis / other]
- **Access Date**: [when verified]

---

### Quality Assessment

#### 1. Evidence Level
**Level**: [I / II / III / IV / V / VI / VII]
**Justification**: [why this level]

#### 2. Publication Venue
- **Journal/Publisher**: [name]
- **Indexed in**: [Scopus / WoS / PubMed / DOAJ / other / none]
- **Impact Factor/CiteScore**: [value or N/A]
- **COPE member**: [Yes / No / Unknown]
- **Predatory indicators**: [None / Flags: list]

**Venue Grade**: [Excellent / Good / Adequate / Questionable / Unacceptable]

#### 3. Author Credibility
- **Author(s)**: [names]
- **Affiliation(s)**: [institutions]
- **ORCID**: [if available]
- **Track record**: [publication history in field]
- **Expertise match**: [relevant to topic? Yes/Partial/No]

**Author Grade**: [Excellent / Good / Adequate / Unknown / Questionable]

#### 4. Methodological Quality
- **Design**: [description]
- **Sample**: [size, selection, representativeness]
- **Analysis**: [appropriate for design?]
- **Limitations acknowledged**: [Yes / Partially / No]
- **Replicable**: [Yes / Partially / No]

**Method Grade**: [Excellent / Good / Adequate / Weak / Flawed]

#### 5. Currency
- **Publication year**: [YYYY]
- **Data collection period**: [if stated]
- **Field velocity**: [Rapid / Moderate / Slow / Foundational]
- **Still current**: [Yes / Conditionally / No]

**Currency Grade**: [Current / Acceptable / Dated / Outdated / Foundational]

#### 6. Conflict of Interest
- **Declared COI**: [None / Listed: details]
- **Funding source**: [source or Not stated]
- **Potential undeclared COI**: [None detected / Possible: details]

**COI Grade**: [Clean / Minor / Moderate / Significant / Critical]

---

### Overall Assessment

| Dimension | Grade |
|-----------|-------|
| Evidence Level | [I-VII] |
| Venue | [Excellent-Unacceptable] |
| Author | [Excellent-Questionable] |
| Method | [Excellent-Flawed] |
| Currency | [Current-Outdated] |
| COI | [Clean-Critical] |
| **Overall** | **[A / B / C / D / F]** |

### Recommendation
- [ ] **Use as primary evidence** (Grade A-B)
- [ ] **Use as supporting evidence** (Grade B-C)
- [ ] **Use with explicit caveats** (Grade C-D)
- [ ] **Do not use** (Grade D-F) — Reason: [specific reason]

### Notes
[Any additional observations, caveats, or context]
```

## Batch Assessment Summary

```markdown
## Source Verification Summary

**Date**: [YYYY-MM-DD]
**Sources assessed**: [N]
**Assessor**: source_verification_agent

### Grade Distribution
| Grade | Count | % |
|-------|-------|---|
| A (Excellent) | X | X% |
| B (Good) | X | X% |
| C (Adequate) | X | X% |
| D (Weak) | X | X% |
| F (Unacceptable) | X | X% |

### Flagged Sources
| Source | Issue | Severity | Recommendation |
|--------|-------|----------|---------------|
| [ref] | [issue] | [High/Medium/Low] | [Include with caveat / Exclude] |

### Predatory Journal Alerts
[List any flagged journals]

### Overall Source Base Quality
**Assessment**: [Strong / Adequate / Mixed / Weak]
**Recommendation**: [Proceed / Supplement / Major revision of source base needed]
```

## Usage Notes
- Complete one card per source for full verification
- Batch summary should be produced after all cards are complete
- Minimum spot-check: 20% of sources get full card assessment
- All Grade D/F sources require documented justification
- Any predatory journal flag requires full verification
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-templates-literature-matrix-template-md"></a>

## SOURCE: skills/deep-research/templates/literature_matrix_template.md

<!-- SOURCE-CONTENT-BEGIN bytes=3779 -->
# Literature Matrix Template

## Purpose
Source x Theme cross-tabulation for systematic evidence mapping. Used by the synthesis_agent to organize evidence before writing the synthesis narrative.

## Matrix Structure

### Basic Matrix

```markdown
## Literature Matrix: [Research Topic]

**Date compiled**: [YYYY-MM-DD]
**Total sources**: [N]
**Themes identified**: [N]

| Source | Year | Level | Theme A | Theme B | Theme C | Theme D | Theme E |
|--------|------|-------|---------|---------|---------|---------|---------|
| Author1 | 2024 | II | ✓ Supports | — | ✓ Supports | ✗ Contradicts | — |
| Author2 | 2023 | III | ✓ Supports | ✓ Supports | — | — | ✓ Supports |
| Author3 | 2022 | VI | — | ✓ Supports | ✓ Supports | ✓ Supports | — |
| Author4 | 2024 | I | ✓ Supports | ✓ Supports | ✗ Contradicts | — | ✓ Supports |
| Author5 | 2023 | IV | ✗ Contradicts | — | ✓ Supports | ✓ Supports | — |
| **Totals** | | | **4✓ 1✗** | **3✓ 0✗** | **3✓ 1✗** | **2✓ 1✗** | **2✓ 0✗** |

### Legend
- ✓ Supports: Source provides evidence supporting this theme
- ✗ Contradicts: Source provides evidence contradicting this theme
- — : Source does not address this theme
- Level: Evidence hierarchy level (I = highest, VII = lowest)
```

### Extended Matrix (with detail)

```markdown
## Extended Literature Matrix

| Source | Method | Sample | Theme A: [name] | Theme B: [name] | Quality |
|--------|--------|--------|-----------------|-----------------|---------|
| Author1 (2024) | RCT, N=500 | University students, US | "Finding X was significant (p<.001)" — Supports | Not addressed | A |
| Author2 (2023) | Case study, N=3 institutions | Asian universities | "Institution A showed..." — Supports | "However, in context B..." — Partial | C |
| Author3 (2022) | Meta-analysis, k=42 | Global | "Pooled effect size d=0.45" — Strong support | "Subgroup analysis revealed..." — Mixed | A |
```

### Convergence Summary

```markdown
## Evidence Convergence Summary

| Theme | Sources For | Sources Against | Net | Strength | Confidence |
|-------|-----------|----------------|-----|----------|-----------|
| Theme A | 4 (Levels I, II, III, IV) | 1 (Level VI) | +3 | Strong | High |
| Theme B | 3 (Levels I, III, IV) | 0 | +3 | Strong | High |
| Theme C | 3 (Levels II, III, VI) | 1 (Level I) | +2 | Contested | Medium |
| Theme D | 2 (Levels IV, VI) | 1 (Level II) | +1 | Weak | Low |
| Theme E | 2 (Levels I, III) | 0 | +2 | Moderate | Medium |

### Interpretation Guide
- **Strong** (≥3 supporting, higher-level evidence): Confident finding
- **Moderate** (2-3 supporting, mid-level evidence): Likely finding, more evidence welcome
- **Weak** (1-2 supporting, lower-level evidence): Tentative, needs more research
- **Contested** (evidence on both sides): Genuine debate, report both sides
- **Gap** (0 sources): Knowledge gap identified
```

### Gap Identification

```markdown
## Knowledge Gaps

| Gap | Type | Implication | Priority |
|-----|------|-------------|----------|
| No data on [population X] | Empirical | Cannot generalize to this group | High |
| Only [method type] used | Methodological | Triangulation needed | Medium |
| No studies since [year] | Temporal | Evidence may be outdated | Medium |
| Only studied in [region] | Geographic | Generalizability unknown | Low |
| No theoretical framework for [finding] | Theoretical | Theory development opportunity | Low |
```

## Usage Notes
- Start with the Basic Matrix for initial organization
- Upgrade to Extended Matrix as synthesis deepens
- Convergence Summary should directly inform the synthesis narrative
- Gap Identification feeds into the Discussion section
- Update the matrix as new sources are added — it is a living document
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-templates-preregistration-template-md"></a>

## SOURCE: skills/deep-research/templates/preregistration_template.md

<!-- SOURCE-CONTENT-BEGIN bytes=8716 -->
# Preregistration Template — OSF Standard 21-Item Preregistration Template

## Purpose
A fill-in template based on the OSF Standard Pre-Data Collection Registration format. Researchers complete this template before data collection and upload it to a preregistration platform (e.g., OSF Registries).

---

## Instructions

1. Complete this template **before** data collection
2. Items marked `[Required]` are mandatory; `[Optional]` are recommended but not required
3. If an item is not applicable, write "Not applicable" and briefly explain why
4. After completion, go to [OSF Registries](https://osf.io/registries) to create a preregistration
5. Once submitted, preregistrations cannot be modified (an embargo period can be set)

---

## A. Study Information

### 1. Title [Required]
> Study Title

```
[Enter descriptive study title]
```

### 2. Authors [Required]
> Research Team

| Name | Institution | Role | ORCID |
|------|-------------|------|-------|
| [Name] | [Institution] | [PI / Co-PI / RA] | [ORCID] |
| [Name] | [Institution] | [Role] | [ORCID] |

### 3. Research Questions [Required]
> Main Research Questions

```
RQ1: [Enter main research question]
RQ2: [Enter secondary research question, if any]
```

### 4. Hypotheses [Required]
> Pre-specified Hypotheses
> Please state directional predictions clearly

```
H1: [Enter hypothesis 1, including expected direction]
    Example: Students receiving treatment X will score significantly higher
    on test Y than the control group

H2: [Enter hypothesis 2, if any]

H3: [Enter hypothesis 3, if any]
```

---

## B. Design Plan

### 5. Study Type [Required]
> Study Design

- [ ] Experiment
  - [ ] Between-subjects
  - [ ] Within-subjects
  - [ ] Mixed design
  - [ ] Factorial design: ___ x ___
- [ ] Observational study
  - [ ] Cross-sectional
  - [ ] Longitudinal / Cohort
  - [ ] Case-control
- [ ] Survey
- [ ] Other: [Describe]

```
[Describe study design in detail]
```

### 6. Randomization [Optional]
> Randomization Procedure

```
Randomization method: [Simple random / Stratified random / Cluster random / Block random / Not applicable]
Randomization unit: [Individual / Class / School / Not applicable]
Randomization tool: [Random number table / Computer program / Lottery / Not applicable]
Allocation ratio: [1:1 / 2:1 / Other]
```

### 7. Blinding [Optional]
> Blinding / Masking

```
Blinding level: [No blinding / Single-blind / Double-blind / Triple-blind]
Blinded parties: [Participants / Researchers / Assessors / Not applicable]
Blinding maintenance: [Describe how blinding is maintained]
Unblinding timing: [Describe when unblinding occurs]
```

### 8. Study Design / Conditions [Required]
> Specific description of each group/condition

```
Experimental group/Condition 1: [Describe intervention content, duration, frequency in detail]
Experimental group/Condition 2: [If any]
Control group: [Describe control condition in detail]
```

---

## C. Sampling Plan

### 9. Existing Data [Required]
> Existing Data Declaration

- [ ] No data have been collected yet (Registration prior to creation of data)
- [ ] Data exist but have not been examined (Registration prior to any human observation of the data)
- [ ] Some data have been examined (Registration prior to accessing the data)
- [ ] Data have been used for preliminary analysis (Registration following analysis of the data)

```
[Describe data status and your level of familiarity with the data]
```

### 10. Data Collection Procedures [Required]
> Data Collection Procedures

```
Collection method: [Online survey / Paper survey / Interview / Experiment / Archival data / Other]
Collection instruments: [Questionnaire name / Scale name / Experimental software]
Collection location: [Online / Classroom / Laboratory / Other]
Collection timeline: [Start and end dates]
Data collectors: [Who is responsible for collection]
```

### 11. Sample Size [Required]
> Planned sample size

```
Target sample size: [N = ]
Sample size per group: [Experimental group n = , Control group n = ]
```

### 12. Sample Size Rationale [Required]
> Basis for sample size determination

```
Method: [Power analysis / Prior research conventions / Feasibility constraints / Other]

Power analysis parameters (if applicable):
- Effect size: [d = / f = / r = ]
- Effect size source: [Prior study / Meta-analysis / Pilot study]
- Significance level (alpha): [.05 / .01]
- Statistical power: [.80 / .90]
- Test type: [t-test / ANOVA / Regression / Other]
- Calculation tool: [G*Power / R / Other]
- Calculation result: Minimum required N = [  ]

Oversampling rate: [Accounting for ___% attrition, actual target N = ]
```

### 13. Stopping Rule [Required]
> When to stop data collection

```
Stopping rule:
- [ ] Stop when target sample size is reached
- [ ] Stop at specified date (Deadline: [Date])
- [ ] Stop when target power is reached (sequential analysis)
- [ ] Other: [Describe]
```

---

## D. Variables

### 14. Manipulated Variables [Required for experiments]
> Independent Variables

```
Independent variable 1: [Name]
Operational definition: [How it is manipulated]
Levels: [Level 1 / Level 2 / ...]

Independent variable 2: [If any]
```

### 15. Measured Variables [Required]
> Dependent Variables

```
Primary dependent variable: [Name]
Operational definition: [How it is measured]
Measurement instrument: [Scale name / Test name]
Reliability and validity: [Cite reliability/validity literature]

Secondary dependent variable: [If any]

Covariates/Control variables: [If any]
```

### 16. Indices [Required]
> Specific scoring method for each variable

```
Variable 1 scoring:
- Items: [Which items]
- Scoring method: [Sum / Mean / Factor score / Other]
- Reverse-scored items: [Which items need reverse scoring]
- Missing data handling: [How to handle missing values]

Variable 2 scoring: [Same format as above]
```

---

## E. Analysis Plan

### 17. Statistical Models [Required]
> Primary statistical analysis methods

```
Analysis for Hypothesis 1:
- Statistical method: [Independent t-test / ANOVA / Regression / HLM / SEM / Other]
- Detailed description: [Model specification, e.g., DV ~ IV + covariate + (1|cluster)]

Analysis for Hypothesis 2: [Same format as above]
```

### 18. Transformations [Optional]
> Data transformation plan

```
Planned transformations:
- [ ] No transformations
- [ ] Log transformation: Applied to [which variables], trigger condition [skewness > ]
- [ ] Standardization (Z-score)
- [ ] Other: [Describe]
```

### 19. Inference Criteria [Required]
> Statistical inference criteria

```
Significance level: alpha = [.05 / .01 / .005]
Multiple comparison correction: [Bonferroni / Holm / FDR / Not applicable]
Effect size reporting: [Cohen's d / eta-squared / R² / Other]
Confidence interval: [95% CI / 99% CI]
One-tailed/Two-tailed test: [Two-tailed / One-tailed, with justification]
```

### 20. Data Exclusion [Required]
> Data exclusion criteria

```
Exclusion criteria:
- [ ] Failed attention check (Specific criteria: [                ])
- [ ] Response time too short/long (Criteria: < [  ] minutes or > [  ] minutes)
- [ ] Outliers (Definition: [> 3 SD / IQR method / Other])
- [ ] Incomplete rate > [  ]%
- [ ] Other: [Describe]

Post-exclusion procedures:
- Report pre- and post-exclusion sample sizes
- Compare characteristics of excluded vs. retained samples
```

### 21. Exploratory Analyses [Optional]
> Planned exploratory analyses

```
Exploratory analyses (not primary hypotheses, but planned):
1. [Analysis description]
2. [Analysis description]

These analyses will be explicitly labeled as "exploratory" in the paper.
```

---

## F. Other

### Ethics Review [Optional]
```
IRB review status: [Approved / Under review / Exempt / Not applicable]
IRB number: [                ]
Reviewing institution: [                ]
```

### Data Availability [Optional]
```
Will data be made public: [Yes / No / Partially]
Data repository: [OSF / Dataverse / Other]
Timing: [After publication / After study completion / Other]
```

### Supplementary Materials [Optional]
```
- [ ] Full questionnaire/scale
- [ ] Stimulus materials
- [ ] Analysis code
- [ ] Power analysis report
- [ ] Pilot study results
```

---

## Pre-Submission Checklist

- [ ] All [Required] items have been completed
- [ ] Hypotheses are clearly stated and testable
- [ ] Analysis methods correspond to hypotheses
- [ ] Exclusion criteria were established before data collection
- [ ] Confirmatory and exploratory analyses have been distinguished
- [ ] IRB review status has been confirmed
- [ ] Preregistration platform has been selected (OSF Registries recommended)

> After completion, go to [OSF Registries](https://osf.io/registries) to submit the preregistration.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-templates-prisma-protocol-template-md"></a>

## SOURCE: skills/deep-research/templates/prisma_protocol_template.md

<!-- SOURCE-CONTENT-BEGIN bytes=8988 -->
# PRISMA-P 2015 — Systematic Review Protocol Template

## Purpose

Template for writing a systematic review protocol following PRISMA-P 2015 (Preferred Reporting Items for Systematic Review and Meta-Analysis Protocols). Complete this template before starting the literature search and register it on PROSPERO or OSF.

**Reference**: Shamseer et al. (2015). BMJ, 349, g7647. https://doi.org/10.1136/bmj.g7647

---

## ADMINISTRATIVE INFORMATION

### Title

**[Provide a descriptive title that identifies the report as a protocol for a systematic review. Include "systematic review" and "meta-analysis" if applicable.]**

Registration: [PROSPERO / OSF ID, or "To be registered"]

### Authors

| # | Name | Affiliation | Role | Contact |
|---|------|-------------|------|---------|
| 1 | [Name] | [Institution] | Guarantor / Lead | [email] |
| 2 | [Name] | [Institution] | Co-reviewer | [email] |

### Amendments

| Date | Section Changed | Description of Change | Rationale |
|------|----------------|----------------------|-----------|
| [date] | [section] | [change] | [why] |

### Support

**Sources**: [Funding source(s) or "No external funding"]
**Role of funder**: [Describe any role of funders in the review, or "None"]

---

## INTRODUCTION

### Rationale

**[Describe the rationale for the review in the context of what is already known. Explain why this review is needed.]**

Key points to address:
- What is the health/education/social problem?
- What is the current state of the evidence?
- Why is a systematic review needed now? (e.g., existing reviews are outdated, conflicting evidence, no previous review exists)

### Objectives

**[Provide an explicit statement of the question(s) the review will address. Use the PICOS framework.]**

- **P** (Population): [Define the target population]
- **I** (Intervention/Exposure): [Define the intervention or exposure of interest]
- **C** (Comparator): [Define the comparison group]
- **O** (Outcomes): [Define primary and secondary outcomes]
- **S** (Study design): [Specify eligible study designs]

Research Question: [State the review question in a single sentence]

---

## METHODS

### Eligibility Criteria

#### Study Characteristics

| Criterion | Include | Exclude |
|-----------|---------|---------|
| **Study design** | [e.g., RCTs, quasi-experimental, cohort] | [e.g., case reports, editorials, commentaries] |
| **Publication date** | [e.g., 2010-present] | [Before cutoff, with justification] |
| **Language** | [e.g., English and Chinese] | [Other languages, with justification] |
| **Publication status** | [e.g., published and preprints] | [e.g., conference abstracts only] |
| **Setting** | [e.g., higher education institutions] | [e.g., K-12, non-formal education] |

#### Participants

[Describe the target population in detail. Include age, gender, condition, or other relevant characteristics.]

#### Interventions/Exposures

[Describe the intervention(s) or exposure(s) of interest. Include dosage, frequency, duration if applicable.]

#### Comparators

[Describe the comparator(s). This may include no intervention, usual care, placebo, or alternative interventions.]

#### Outcomes

**Primary outcome(s)**:
1. [Outcome 1] — measured by [instrument/method], at [time point(s)]
2. [Outcome 2] — measured by [instrument/method], at [time point(s)]

**Secondary outcome(s)**:
1. [Outcome 3] — measured by [instrument/method], at [time point(s)]
2. [Outcome 4] — measured by [instrument/method], at [time point(s)]

#### Timing

[Specify any minimum follow-up duration or time constraints]

### Information Sources

| Database/Source | URL | Coverage | Justification |
|----------------|-----|----------|---------------|
| [e.g., PubMed/MEDLINE] | pubmed.ncbi.nlm.nih.gov | Biomedical | Core database for health research |
| [e.g., Web of Science] | webofscience.com | Multidisciplinary | Citation indexing, broad coverage |
| [e.g., Scopus] | scopus.com | Multidisciplinary | Large abstract database |
| [e.g., ERIC] | eric.ed.gov | Education | Core database for education research |
| [e.g., PsycINFO] | apa.org/pubs/databases/psycinfo | Psychology | Behavioral science coverage |
| [Grey literature] | [specify sources] | — | Reduce publication bias |
| [Trial registries] | clinicaltrials.gov, WHO ICTRP | — | Identify unpublished studies |

Additional sources:
- Reference lists of included studies (backward citation)
- Citation tracking of key studies (forward citation)
- Contact with experts in the field (if applicable)

### Search Strategy

**[Present the draft search strategy for at least one database. The strategy should be peer-reviewed using the PRESS checklist.]**

Example structure for [primary database]:
```
Search Block 1 (Population):
  "higher education" OR "university" OR "college" OR "postsecondary"

Search Block 2 (Intervention/Exposure):
  "quality assurance" OR "accreditation" OR "program review"

Search Block 3 (Outcome):
  "student outcomes" OR "learning outcomes" OR "graduation rate"

Combined: Block 1 AND Block 2 AND Block 3
Filters: [date range], [language], [document type]
```

### Study Records

#### Data Management

[Describe the software/tools to be used for managing records. E.g., Covidence, Rayyan, Excel, Zotero]

#### Selection Process

1. **Deduplication**: [Method for removing duplicates, e.g., automatic in Covidence + manual check]
2. **Title/Abstract screening**: [Number of reviewers, independence, process for resolving disagreements]
3. **Full-text screening**: [Number of reviewers, independence, process for resolving disagreements]
4. **Documentation**: [How excluded studies and reasons will be recorded]

Pilot: [Describe pilot testing of screening criteria, e.g., "Two reviewers will independently screen 50 records to calibrate criteria before full screening"]

#### Data Collection Process

1. **Data extraction form**: [Describe or attach the form. Pilot test with 3-5 studies]
2. **Extractors**: [Number, independence, process for resolving discrepancies]
3. **Missing data**: [How missing or unclear data will be handled, e.g., contact authors]

### Data Items

| Category | Variables to Extract |
|----------|---------------------|
| **Study metadata** | Authors, year, country, journal, study design |
| **Participants** | Sample size, demographics, setting, inclusion criteria |
| **Intervention/Exposure** | Description, duration, frequency, comparison group |
| **Outcomes** | Primary and secondary outcomes, measurement tools, time points |
| **Results** | Effect sizes, CIs, p-values, means, SDs, counts |
| **Quality** | Funding, COI declarations, registration status |

### Risk of Bias Assessment

**Tool**: [Specify the tool]
- RCTs: RoB 2 (Sterne et al., 2019)
- Non-randomized studies: ROBINS-I (Sterne et al., 2016)
- Qualitative studies: [e.g., CASP qualitative checklist]

**Process**: [Number of assessors, independence, consensus process]

**Use in synthesis**: [How risk of bias results will inform the synthesis, e.g., sensitivity analysis excluding high-risk studies]

### Data Synthesis

#### Quantitative Synthesis (Meta-Analysis)

**Conditions for meta-analysis**: [Describe when studies will be pooled, e.g., "When ≥ 3 studies report sufficiently similar outcomes measured in comparable populations"]

**Effect measure**: [Specify, e.g., SMD for continuous outcomes, RR for binary outcomes]

**Model**: [Fixed-effect / Random-effects, with justification]

**Heterogeneity assessment**:
- Q-test (significance at p < 0.10)
- I² statistic with 95% CI
- tau² (between-study variance)
- Prediction interval

**Subgroup analyses** (pre-specified):
1. [Subgroup variable 1] — Rationale: [why]
2. [Subgroup variable 2] — Rationale: [why]

**Sensitivity analyses**:
1. Leave-one-out analysis
2. Exclude high risk of bias studies
3. [Other planned sensitivity analyses]

**Software**: [Specify, e.g., R metafor package, RevMan]

#### Narrative Synthesis

**When meta-analysis is not feasible**: [Describe the narrative synthesis approach, e.g., SWiM reporting guideline, vote counting, effect direction plot]

### Meta-Bias Assessment

**Publication bias**: [Methods to assess, e.g., funnel plot + Egger's test if ≥ 10 studies]

**Selective reporting**: [How to detect, e.g., compare protocol to published report, search trial registries]

### Confidence in Cumulative Evidence

**Framework**: GRADE (Grading of Recommendations, Assessment, Development and Evaluations)

[Describe how GRADE will be applied to assess certainty for each outcome]

---

## APPENDICES

### Appendix A: Draft Search Strategy

[Complete search strategy for the primary database]

### Appendix B: Data Extraction Form

[Include or reference the data extraction form]

### Appendix C: PRISMA-P Checklist

[Mark each PRISMA-P item as addressed with the relevant page/section number]

---

## Revision Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [date] | [name] | Initial protocol |
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-templates-prisma-report-template-md"></a>

## SOURCE: skills/deep-research/templates/prisma_report_template.md

<!-- SOURCE-CONTENT-BEGIN bytes=16191 -->
# PRISMA 2020 — Systematic Review Report Template

## Purpose

Template for writing a systematic review report following PRISMA 2020 (Page et al., 2021). All 27 PRISMA items are mapped to their corresponding sections. Use alongside `references/systematic_review_toolkit.md` for detailed guidance.

**Reference**: Page et al. (2021). The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ, 372, n71. https://doi.org/10.1136/bmj.n71

---

## Title [PRISMA Item 1]

**[Full title identifying the report as a systematic review, meta-analysis, or both]**

Example: "The Effect of [Intervention] on [Outcome] in [Population]: A Systematic Review and Meta-Analysis"

---

## Abstract [PRISMA Item 2]

### Background
[1-2 sentences on context and why the review was done]

### Objectives
[Research question(s), ideally structured as PICOS]

### Data Sources
[Databases searched and dates of last search]

### Study Selection
[Eligibility criteria in brief]

### Data Extraction and Synthesis
[Methods used for data extraction, risk of bias, and synthesis]

### Results
[Number of studies included, key findings, effect estimates with CIs, certainty of evidence]

### Limitations
[Key limitations of the evidence and/or the review process]

### Conclusions
[General interpretation and implications]

### Registration
[Protocol registration number and repository]

**Keywords**: [3-5 keywords]

---

## 1. Introduction

### 1.1 Rationale [PRISMA Item 3]

[Describe the rationale for the review in the context of existing knowledge. Address:]
- What is the problem or question?
- What is already known (with references to existing reviews)?
- Why is this review needed (e.g., no existing review, existing review outdated, conflicting evidence)?

### 1.2 Objectives [PRISMA Item 4]

[Provide an explicit statement of the question(s) using PICOS:]

- **Population**: [target population]
- **Intervention/Exposure**: [intervention or exposure of interest]
- **Comparator**: [comparison group]
- **Outcome(s)**: [primary and secondary outcomes]
- **Study Design**: [eligible study designs]

---

## 2. Methods

### 2.1 Eligibility Criteria [PRISMA Item 5]

| Criterion | Include | Exclude |
|-----------|---------|---------|
| Study design | [e.g., RCTs, quasi-experimental] | [e.g., case reports, editorials] |
| Population | [describe] | [describe] |
| Intervention | [describe] | [describe] |
| Comparator | [describe] | [describe] |
| Outcome | [describe] | [describe] |
| Time frame | [e.g., published 2014-2024] | [before cutoff] |
| Language | [e.g., English] | [other] |
| Setting | [describe] | [describe] |

### 2.2 Information Sources [PRISMA Item 6]

[List all databases and other sources searched, with dates of coverage and last search date:]

| Source | Date Range | Last Searched |
|--------|-----------|---------------|
| [Database 1] | [start]-[end] | [date] |
| [Database 2] | [start]-[end] | [date] |
| [Other sources: reference lists, expert contact, grey literature] | — | [date] |

### 2.3 Search Strategy [PRISMA Item 7]

[Present the complete search strategy for at least one database. Include all search terms, Boolean operators, and any filters applied.]

**[Database Name] Search Strategy**:
```
#1 [search block 1 - Population terms]
#2 [search block 2 - Intervention terms]
#3 [search block 3 - Outcome terms]
#4 #1 AND #2 AND #3
#5 #4 with filters: [date, language, document type]
```

[Search strategies for other databases are available in Appendix A.]

### 2.4 Selection Process [PRISMA Item 8]

[Describe the study selection process:]
- Number of reviewers at each stage
- How independence was maintained
- How disagreements were resolved
- Software used (e.g., Covidence, Rayyan)
- Pilot testing of screening criteria

### 2.5 Data Collection Process [PRISMA Item 9]

[Describe methods for extracting data from reports:]
- Data extraction form (developed, piloted)
- Number of extractors and independence
- Process for resolving discrepancies
- How missing data were handled (e.g., contacted authors)

### 2.6 Data Items [PRISMA Item 10]

[List all variables for which data were sought:]

| Category | Variables |
|----------|----------|
| Study-level | Authors, year, country, design, setting, funding |
| Participants | N, age, gender, diagnosis/condition, attrition |
| Intervention | Type, duration, frequency, fidelity |
| Outcomes | Definition, measurement tool, time points |
| Results | Effect sizes, CIs, p-values, raw data |

### 2.7 Study Risk of Bias Assessment [PRISMA Item 11]

[Describe the risk of bias assessment:]
- Tool(s) used: [RoB 2 for RCTs / ROBINS-I for non-randomized / other]
- Domains assessed
- Number of assessors and independence
- How results were used in the synthesis

### 2.8 Effect Measures [PRISMA Item 12]

[Specify the effect measure(s) for each outcome:]

| Outcome | Type | Effect Measure | Justification |
|---------|------|---------------|---------------|
| [Outcome 1] | Continuous | SMD (Hedges' g) | Different scales across studies |
| [Outcome 2] | Binary | RR | Incidence data |

### 2.9 Synthesis Methods [PRISMA Items 13a-13f]

**13a. Eligibility for synthesis**: [Criteria for grouping studies into each synthesis]

**13b. Data preparation**: [Methods to prepare data, e.g., converting SE to SD, handling multi-arm studies]

**13c. Tabulation/visualization**: [Methods for displaying individual study and synthesis results, e.g., forest plots, summary tables]

**13d. Synthesis approach**: [Statistical model and software]
- Model: [Fixed-effect / Random-effects (DerSimonian-Laird / REML)]
- Software: [R metafor / RevMan / Stata]
- OR if narrative: [SWiM approach, vote counting, effect direction plot]

**13e. Heterogeneity exploration**: [Methods used]
- Subgroup analyses: [pre-specified subgroups and rationale]
- Meta-regression: [covariates tested, if applicable]

**13f. Sensitivity analyses**: [Planned sensitivity analyses]
1. Leave-one-out analysis
2. Excluding high risk of bias studies
3. Fixed-effect vs. random-effects comparison
4. [Other analyses]

### 2.10 Reporting Bias Assessment [PRISMA Item 14]

[Methods to assess publication bias:]
- Funnel plot (visual inspection)
- Statistical test: [Egger's / Peter's / trim-and-fill]
- Comparison of protocol to published reports

### 2.11 Certainty Assessment [PRISMA Item 15]

[Framework used to assess certainty of evidence:]
- GRADE approach
- Factors assessed: risk of bias, inconsistency, indirectness, imprecision, publication bias
- Rating up factors (for observational studies): large effect, dose-response, plausible confounding

---

## 3. Results

### 3.1 Study Selection [PRISMA Item 16a, 16b]

#### PRISMA Flow Diagram

```
 ┌─────────────────────────────────────────────────────┐
 │                 IDENTIFICATION                      │
 ├─────────────────────────────────────────────────────┤
 │ Records identified from databases (n = )            │
 │   Database 1 (n = )                                 │
 │   Database 2 (n = )                                 │
 │   Database 3 (n = )                                 │
 │ Records identified from other sources (n = )        │
 │   Reference lists (n = )                            │
 │   Expert recommendations (n = )                     │
 └──────────────────────┬──────────────────────────────┘
                        │
 ┌──────────────────────▼──────────────────────────────┐
 │ Records removed before screening:                   │
 │   Duplicate records (n = )                          │
 │   Records marked ineligible by automation (n = )    │
 │   Records removed for other reasons (n = )          │
 └──────────────────────┬──────────────────────────────┘
                        │
 ┌──────────────────────▼──────────────────────────────┐
 │                  SCREENING                          │
 ├─────────────────────────────────────────────────────┤
 │ Records screened (n = )                             │
 │ Records excluded (n = )                             │
 └──────────────────────┬──────────────────────────────┘
                        │
 ┌──────────────────────▼──────────────────────────────┐
 │ Reports sought for retrieval (n = )                 │
 │ Reports not retrieved (n = )                        │
 └──────────────────────┬──────────────────────────────┘
                        │
 ┌──────────────────────▼──────────────────────────────┐
 │ Reports assessed for eligibility (n = )             │
 │ Reports excluded, with reasons (n = )               │
 │   Reason 1 (n = )                                   │
 │   Reason 2 (n = )                                   │
 │   Reason 3 (n = )                                   │
 └──────────────────────┬──────────────────────────────┘
                        │
 ┌──────────────────────▼──────────────────────────────┐
 │                  INCLUDED                           │
 ├─────────────────────────────────────────────────────┤
 │ Studies included in review (n = )                   │
 │ Reports of included studies (n = )                  │
 │ Studies in quantitative synthesis (n = )             │
 └─────────────────────────────────────────────────────┘
```

[PRISMA Item 16b: Cite studies that appeared to meet inclusion criteria but were excluded, with reasons.]

### 3.2 Study Characteristics [PRISMA Item 17]

**Table: Characteristics of Included Studies**

| Study | Country | Design | Population (N) | Intervention | Comparator | Outcome(s) | Follow-up | Funding |
|-------|---------|--------|----------------|-------------|-----------|------------|-----------|---------|
| Author1 (Year) | [country] | [design] | [N] | [intervention] | [comparator] | [outcomes] | [duration] | [source] |
| Author2 (Year) | ... | ... | ... | ... | ... | ... | ... | ... |

### 3.3 Risk of Bias in Studies [PRISMA Item 18]

**Table: Risk of Bias Summary (Traffic-Light)**

| Study | D1 | D2 | D3 | D4 | D5 | Overall |
|-------|----|----|----|----|----|---------|
| Author1 (Year) | [L/S/H] | [L/S/H] | [L/S/H] | [L/S/H] | [L/S/H] | [L/S/H] |
| Author2 (Year) | ... | ... | ... | ... | ... | ... |

L = Low risk, S = Some concerns, H = High risk

[Narrative summary of risk of bias findings across studies]

### 3.4 Results of Individual Studies [PRISMA Item 19]

**Table: Individual Study Results**

| Study | Outcome | Effect Estimate | 95% CI | p-value | Weight |
|-------|---------|----------------|--------|---------|--------|
| Author1 (Year) | [outcome] | [estimate] | [lower, upper] | [p] | [%] |
| Author2 (Year) | ... | ... | ... | ... | ... |

### 3.5 Results of Syntheses [PRISMA Items 20a-20d]

#### Primary Outcome: [Name]

**20a. Study characteristics**: [Brief summary of contributing studies' characteristics and risk of bias]

**20b. Pooled result**:
- Pooled effect: [estimate] (95% CI: [lower, upper])
- Statistical significance: Z = [value], p = [value]
- Heterogeneity: I² = [value]% (95% CI: [lower, upper]), Q = [value] (df = [n], p = [value]), tau² = [value]
- Prediction interval: [lower, upper]

**Forest Plot**: [Insert or reference forest plot]

**20c. Heterogeneity investigation**:
- Subgroup analyses: [results]
- Meta-regression: [results, if conducted]

**20d. Sensitivity analyses**:
1. Leave-one-out: [results — did any single study substantially change the estimate?]
2. Excluding high-risk studies: [revised estimate]
3. Fixed vs. random effects: [comparison]

#### Secondary Outcome(s): [Name]

[Repeat structure above for each secondary outcome]

### 3.6 Reporting Biases [PRISMA Item 21]

[Report assessments of publication bias:]
- Funnel plot: [description of symmetry/asymmetry]
- Statistical test: [result]
- Trim-and-fill: [adjusted estimate, if applicable]
- Other assessments: [protocol-outcome comparison]

### 3.7 Certainty of Evidence [PRISMA Item 22]

**GRADE Summary of Findings Table**

| Outcome | Studies (n) | Participants (N) | Effect (95% CI) | Certainty | Rationale |
|---------|------------|-------------------|-----------------|-----------|-----------|
| [Outcome 1] | [n] | [N] | [estimate (CI)] | [High/Moderate/Low/Very Low] | [Reasons for up/downgrading] |
| [Outcome 2] | [n] | [N] | [estimate (CI)] | [level] | [reasons] |

---

## 4. Discussion [PRISMA Item 23]

### 4.1 Summary of Evidence

[Provide a general interpretation of the results in the context of other evidence. Address:]
- Main findings for each outcome
- How findings compare to previous reviews
- Consistency of findings across studies

### 4.2 Limitations

**Limitations of the evidence**:
- [e.g., risk of bias across studies, inconsistency, indirectness, imprecision]

**Limitations of the review process**:
- [e.g., language restrictions, database coverage, inability to contact authors]

### 4.3 Implications

**For practice**:
- [What practitioners should do based on these findings]

**For research**:
- [Gaps identified, recommended future study designs]

**For policy**:
- [Policy implications, if applicable]

---

## 5. Other Information

### 5.1 Registration and Protocol [PRISMA Item 24]

[Provide registration information and link to protocol:]
- Registry: [e.g., PROSPERO]
- Registration number: [number]
- Protocol URL: [link]
- Deviations from protocol: [describe any deviations and rationale]

### 5.2 Support [PRISMA Item 25]

[Describe sources of support:]
- Financial: [funding sources and grant numbers]
- Non-financial: [e.g., institutional support, access to databases]
- Role of funder: [describe any role of funders in the review]

### 5.3 Competing Interests [PRISMA Item 26]

[Declare competing interests of all authors]

### 5.4 Availability of Data and Materials [PRISMA Item 27]

[Report availability of:]
- [ ] Data extraction forms
- [ ] Extracted data from included studies
- [ ] Analysis code
- [ ] List of excluded studies with reasons
- [ ] PRISMA checklist (completed)

---

## Appendices

### Appendix A: Full Search Strategies

[Complete search strategies for all databases]

### Appendix B: Excluded Studies with Reasons

| Study | Reason for Exclusion |
|-------|---------------------|
| [citation] | [reason] |

### Appendix C: PRISMA 2020 Checklist

[Completed PRISMA 2020 checklist with page/section numbers for each item]

| Item # | Checklist Item | Reported on Page/Section |
|--------|---------------|-------------------------|
| 1 | Title | [page] |
| 2 | Abstract | [page] |
| ... | ... | ... |
| 27 | Availability | [page] |
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-templates-research-brief-template-md"></a>

## SOURCE: skills/deep-research/templates/research_brief_template.md

<!-- SOURCE-CONTENT-BEGIN bytes=2175 -->
# Research Brief Template

## Purpose
Standard output format for `quick` mode research. Concise, actionable, evidence-based.

## Template

```markdown
# Research Brief

**Title**: [Descriptive title in sentence case]
**Date**: [YYYY-MM-DD]
**Mode**: Quick Research Brief
**AI Disclosure**: This brief was produced with AI-assisted research tools. All findings are verified against cited sources.

---

## Executive Summary
[100-150 words. State the question, key findings, and main implication.]

---

## Background & Research Question

### Context
[2-3 paragraphs providing necessary background for the reader.]

### Research Question
> [The refined research question, as a single clear sentence.]

### Scope
- **In scope**: [what this brief covers]
- **Out of scope**: [what this brief does not cover]

---

## Key Findings

### Finding 1: [Title]
[2-3 sentences with citation(s)]

**Evidence strength**: [Strong / Moderate / Emerging]
**Source(s)**: [Brief citation]

### Finding 2: [Title]
[2-3 sentences with citation(s)]

**Evidence strength**: [Strong / Moderate / Emerging]
**Source(s)**: [Brief citation]

### Finding 3: [Title]
[2-3 sentences with citation(s)]

**Evidence strength**: [Strong / Moderate / Emerging]
**Source(s)**: [Brief citation]

[Add more findings as needed, typically 3-5]

---

## Analysis & Implications

### What This Means
[2-3 paragraphs interpreting the findings. Connect evidence to practical implications.]

### Recommendations
1. [Actionable recommendation with evidence basis]
2. [Actionable recommendation with evidence basis]
3. [Actionable recommendation with evidence basis]

---

## Limitations
- [Limitation 1: e.g., search scope, time constraints]
- [Limitation 2: e.g., evidence gaps]
- [Limitation 3: e.g., AI-assisted analysis limitations]

---

## References
[APA 7.0 format, 5-10 references typical for quick mode]

1. [Reference 1]
2. [Reference 2]
...
```

## Usage Notes
- Target length: 500-1,500 words
- Minimum 5 cited sources
- Every finding must have at least one citation
- Evidence strength ratings should align with source quality hierarchy
- Keep language accessible — this is a brief, not a journal article
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-examples-exploratory-research-md"></a>

## SOURCE: skills/deep-research/examples/exploratory_research.md

<!-- SOURCE-CONTENT-BEGIN bytes=7108 -->
# Example: Exploratory Research — Full Pipeline

## User Request
```
Research the impact of AI on higher education quality assurance
```

## Phase 1: SCOPING

### research_question_agent Output

**Topic Area**: Artificial intelligence applications in higher education quality assurance

**Primary Research Question**:
> How are artificial intelligence technologies being integrated into higher education quality assurance processes, and what are the emerging benefits, risks, and institutional implications?

**FINER Assessment**:
| Criterion | Score | Justification |
|-----------|-------|---------------|
| Feasible | 4/5 | Growing literature base; accessible through academic databases |
| Interesting | 5/5 | Rapidly evolving area at intersection of two major sectors |
| Novel | 4/5 | Few comprehensive reviews exist; most studies are case-specific |
| Ethical | 4/5 | Raises important AI ethics questions but not inherently harmful |
| Relevant | 5/5 | Directly informs QA agency strategy and policy |
| **Average** | **4.4/5** | |

**Scope Boundaries**:
- In scope: AI/ML applications in institutional/program accreditation, learning analytics for QA, automated assessment, AI in self-evaluation
- Out of scope: AI in teaching/learning (unless directly connected to QA), AI plagiarism detection (separate literature), specific vendor products
- Key assumptions: Focus on post-secondary education; "quality assurance" includes both internal QA and external accreditation

**Sub-questions**:
1. What AI technologies are currently being applied or piloted in HE quality assurance?
2. What benefits and risks do stakeholders report from AI integration in QA?
3. What institutional and policy implications arise from AI-augmented QA processes?

### research_architect_agent Output

**Research Paradigm**: Pragmatist (mixed evidence types, applied orientation)
**Method**: Systematic literature review with thematic synthesis
**Data Strategy**: Secondary data (academic literature + grey literature from QA agencies)
**Analytical Framework**: Thematic analysis organized by sub-questions
**Validity Criteria**: Comprehensive search, transparent inclusion criteria, PRISMA reporting

### devils_advocate_agent — CHECKPOINT 1

**Verdict**: PASS (with minor notes)
- Minor: RQ is broad — consider whether "emerging" limits to recent literature only
- Minor: Define "quality assurance" explicitly (internal vs. external, process vs. outcome)
- Observation: Fast-moving field means any review may be quickly outdated

## Phase 2: INVESTIGATION

### bibliography_agent Output

**Search Strategy**: 4 databases (Scopus, Web of Science, ERIC, Google Scholar), keywords: "artificial intelligence" AND "quality assurance" AND "higher education", date range: 2019-2025, English and Chinese languages.

**PRISMA Flow**: 847 identified -> 612 after dedup -> 89 screened -> 31 full-text -> 22 included

**Annotated Bibliography** (excerpt):
1. **Zawacki-Richter, O., et al. (2019). Systematic review of research on artificial intelligence applications in higher education. *International Journal of Educational Technology in Higher Education*, *16*(1), 39. https://doi.org/10.1186/s41239-019-0171-0**
   - Relevance: Foundational mapping of AI in HE
   - Key Findings: AI predominantly used in profiling/prediction, assessment, adaptive learning
   - Quality: Level V (systematic review of descriptive studies)

2. **Sanchez-Prieto, J.C., et al. (2024). AI-enhanced quality assurance: A framework for European higher education. *Quality in Higher Education*, *30*(1), 45-62.**
   - Relevance: Directly addresses AI+QA intersection
   - Key Findings: Proposed framework with 4 dimensions; stakeholder acceptance varies
   - Quality: Level VI (framework paper with case illustrations)

[... 20 more sources ...]

### source_verification_agent Output

**Sources Reviewed**: 22 | **Verified**: 20 | **Flagged**: 2 | **Rejected**: 0

**Flagged**:
1. Source #14 — Moderate COI (author is CTO of an AI-QA startup)
2. Source #19 — Currency concern (2019 review may not reflect post-GPT developments)

## Phase 3: ANALYSIS

### synthesis_agent Output

**Key Themes**:
1. **AI Application Typology** (Strong evidence, 15 sources): Categorization, analytics, automation, prediction
2. **Benefits: Efficiency & Scale** (Moderate evidence, 9 sources): Reduced reviewer burden, faster turnaround, larger data processing
3. **Risks: Bias & Transparency** (Moderate evidence, 8 sources): Algorithmic bias, black-box decisions, accountability gaps
4. **Institutional Readiness** (Emerging evidence, 5 sources): Capacity building, infrastructure, cultural resistance
5. **Policy Frameworks** (Emerging evidence, 4 sources): Regulation, standards, governance models

**Key Contradiction**: Sources disagree on whether AI reduces or amplifies bias in QA — resolution depends on implementation design and oversight mechanisms.

**Knowledge Gaps**: Limited evidence from Global South; few longitudinal studies; no studies on student perception of AI in QA.

### devils_advocate_agent — CHECKPOINT 2

**Verdict**: PASS
- Minor: Technology-positive framing detected — ensure risks are given equal weight
- Observation: Most evidence comes from European/North American contexts

## Phase 4: COMPOSITION

### report_compiler_agent Output

[Full APA 7.0 report, ~5,200 words]

Title: Artificial Intelligence in Higher Education Quality Assurance: A Systematic Review of Applications, Benefits, Risks, and Institutional Implications

[Abstract, Introduction, Literature Review, Methodology, Findings (organized by 5 themes), Discussion, Limitations, Conclusion, References (22 sources)]

## Phase 5: REVIEW

### editor_in_chief_agent Output

**Verdict**: Minor Revision (Score: 3.7/5.0)
- Strength: Comprehensive search, well-organized themes
- Major: Discussion section needs stronger connection between findings and existing QA theory
- Minor: Some inconsistency in citation format (3 references)
- Minor: Abstract exceeds 250-word limit

### ethics_review_agent Output

**Verdict**: CLEARED
- AI disclosure present and accurate
- All references spot-checked (5/22 = 23%) — all verified
- Dual-use risk: Low
- Fair representation: Adequate (noted geographic limitation)

### devils_advocate_agent — CHECKPOINT 3

**Verdict**: PASS
- Observation: Conclusion recommendation #3 ("QA agencies should adopt AI tools") is stronger than evidence warrants — suggest hedging
- "So what?" test: Passed — clear implications for QA practice

## Phase 6: REVISION

### report_compiler_agent (Revision 1)

**Changes**:
1. Discussion section expanded with QA theory connections (Major, Editor)
2. 3 citation format errors corrected (Minor, Editor)
3. Abstract trimmed to 248 words (Minor, Editor)
4. Recommendation #3 hedged: "should consider piloting" (Observation, Devil's Advocate)

**Final Word Count**: 5,450 words
**Revision Loops Used**: 1 of 2

---

## Final Output Summary
- Full APA 7.0 report: 5,450 words
- 22 cited sources (Levels I-VII)
- 5 thematic findings
- 3 recommendations
- Ethics cleared
- 1 revision loop completed
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-examples-fact-check-mode-md"></a>

## SOURCE: skills/deep-research/examples/fact_check_mode.md

<!-- SOURCE-CONTENT-BEGIN bytes=13164 -->
---
scenario: Fact-checking claims about Taiwan's higher education
mode: fact-check
agents_used:
  - source_verification_agent
input: User provides 7 claims about Taiwan's higher education
output: Claim-by-claim verification report + verification summary
note: This example uses Taiwan HEI data. The fact-check mode works with any topic — just provide claims about your research area (e.g., "US enrollment has declined 15% since 2010", "EU universities spend more on research than US ones").
---

# Fact-Check Mode Example: Taiwan Higher Education Claim Verification

This example demonstrates the complete workflow of `fact-check` mode using Taiwan higher education as a domain-specific case. The same workflow applies to any research domain — simply replace the claims with statements relevant to your field. The source_verification_agent verifies each claim against available evidence.

---

## User Request

```
Please fact-check the following claims about Taiwan's higher education:

1. Taiwan currently has 152 colleges and universities.
2. HEEACT was established in 2005 and is the only institution responsible for higher education accreditation in Taiwan.
3. The average student-to-faculty ratio in Taiwan's universities is 1:20.
4. Declining birth rates have caused more than 10 universities in Taiwan to complete their exit or closure procedures.
5. Taiwan's higher education expenditure as a percentage of GDP is approximately 0.4%, lower than the OECD average.
6. The vacancy rate for the 2024 academic year university examination distribution admission reached 15%.
7. Taiwan produces approximately 4,000 doctoral graduates per year, of which more than half enter academia as faculty.
```

---

## source_verification_agent Verification Report

### Claim 1

> "Taiwan currently has 152 colleges and universities."

**Verdict:** Warning — Partially True

**Verification Basis:** According to MOE's higher education overview statistics for Academic Year 112 (2023-2024), Taiwan's total number of higher education institutions is 145 (including universities, independent colleges, and junior colleges). This number continues to change due to school closures or mergers. If military and police academies (e.g., National Defense University, Central Police University) are included, the total increases slightly but still does not reach 152. "152" likely references data from an earlier year (approximately Academic Year 108-109), when more schools were still operating.

**Source:** MOE Statistics Division, *Higher Education Overview Statistics*, Academic Year 112 (2023-2024).

**Correction Suggestion:** Should be updated to the latest academic year figure, with clear definition of the statistical scope (whether military/police academies, religious seminary institutions, and other special types are included).

---

### Claim 2

> "HEEACT was established in 2005 and is the only institution responsible for higher education accreditation in Taiwan."

**Verdict:** Warning — Partially True

**Verification Basis:** The Higher Education Evaluation and Accreditation Council of Taiwan (HEEACT) was indeed established on December 26, 2005 — this part is correct. However, the claim of "only" is inaccurate. Taiwan's higher education evaluation system has promoted diversification since 2017. In addition to HEEACT, the Taiwan Assessment and Evaluation Association (TWAEA) and the Institute of Engineering Education Taiwan (IEET), among others, are also recognized by the MOE to conduct specific types of quality assurance accreditation. Furthermore, from the third cycle of institutional accreditation starting in 2023, universities are also allowed to choose self-conducted external evaluation. Therefore, HEEACT is the most prominent but not the only accreditation body.

**Sources:**
- HEEACT official website, About Us > History
- MOE, "Principles for Reviewing University Self-Evaluation Results" (2017 revision)
- MOE, "Implementation Plan for Commissioned Quality Assurance Accreditation of Higher Education Institutions" (Academic Year 116)

**Correction Suggestion:** Revise to "HEEACT was established in 2005 and is one of the most prominent higher education accreditation bodies in Taiwan."

---

### Claim 3

> "The average student-to-faculty ratio in Taiwan's universities is 1:20."

**Verdict:** Warning — Partially True

**Verification Basis:** The student-to-faculty ratio varies depending on the calculation formula used. The MOE's published full-school student-to-faculty ratio (including full-time and part-time equivalents) differs significantly from one calculated using only full-time faculty. According to Academic Year 112 data, the equivalent student-to-faculty ratio for public university daytime programs is approximately 18:1 to 22:1 (varies by institution), while private universities are approximately 22:1 to 28:1. The overall average is approximately 23:1, not 20:1. Additionally, "1:20" is an unconventional notation — the student-to-faculty ratio is typically written as "20:1" (20 students per 1 faculty), not "1:20."

**Source:** MOE Statistics Division, *Student and Faculty Statistics by Institution*, Academic Year 112.

**Correction Suggestion:** Revise to "The equivalent student-to-faculty ratio for Taiwan's daytime higher education programs is approximately 23:1, with significant differences between public and private institutions," and use the correct notation format.

---

### Claim 4

> "Declining birth rates have caused more than 10 universities in Taiwan to complete their exit or closure procedures."

**Verdict:** Verified

**Verification Basis:** According to MOE announcements and the implementation status of the "Private Senior High School and Above Exit Act," as of early 2025, institutions that have completed enrollment suspension or closure procedures include: Kao Fong College of Digital Contents (closed 2014), Yung Ta Institute of Technology (enrollment suspended 2014, closed 2021), Kao-Mei College of Health Care and Management (enrollment suspended 2018), Asia-Pacific Institute of Creativity (enrollment suspended 2019), Nan Jeon University of Science and Technology (enrollment suspended 2020), Toko University (enrollment suspended 2020), Taiwan Tourism College (closed 2022), Lan Yang Institute of Technology (enrollment suspended 2022), Chung Chou University of Science and Technology (enrollment suspended 2023), Hechun Institute of Technology (enrollment suspended 2023), Tatung Institute of Technology (enrollment suspended 2023), Taiwan Shoufu University (closed 2023), MingDao University (enrollment suspended 2024), TransWorld University (enrollment suspended 2024), among others. The total exceeds 10 institutions; this claim is verified.

**Sources:**
- MOE, annual higher education institution enrollment suspension/closure announcements
- MOE, "Private Senior High School and Above Exit Act" implementation progress report

**Note:** This number continues to increase; some schools are in the "special counseling" stage and have not yet completed their exit process.

---

### Claim 5

> "Taiwan's higher education expenditure as a percentage of GDP is approximately 0.4%, lower than the OECD average."

**Verdict:** Warning — Partially True

**Verification Basis:** This claim requires distinguishing between "government public expenditure" and "total expenditure (including private)." According to MOE statistics, Taiwan's government public expenditure on higher education as a percentage of GDP is approximately 0.4-0.5%, which is indeed lower than the OECD average of approximately 0.9% (Education at a Glance 2021 data). However, when private expenditure (tuition, corporate sponsorship, etc.) is included, Taiwan's total higher education expenditure as a percentage of GDP is approximately 1.2-1.3%, approaching the OECD average of 1.5%. Therefore, the "0.4%" figure only reflects the public expenditure portion. The claim does not distinguish between public and private expenditure, which can be misleading.

**Sources:**
- MOE Statistics Division, *Education Expenditure Statistics*, Year 112
- OECD, *Education at a Glance 2023*, Table C2.1

**Correction Suggestion:** Revise to "Taiwan's public expenditure on higher education as a percentage of GDP is approximately 0.4-0.5%, lower than the OECD average of 0.9%; however, when including private expenditure, the total proportion is approximately 1.2-1.3%, narrowing the gap."

---

### Claim 6

> "The vacancy rate for the 2024 academic year university examination distribution admission reached 15%."

**Verdict:** Unverifiable

**Verification Basis:** The University Entrance Exam Center for Placement publishes distribution results annually, but the definition and calculation method of "vacancy rate" may vary across reports. The "15%" cited here lacks a clear source and calculation basis: is the denominator the approved enrollment quota? Or the remaining quota after subtracting admissions through other channels? Media-reported figures in recent years vary widely, from single-digit percentages to over 20%, depending on the calculation method and whether only general universities or also technical colleges are included. Furthermore, the 2024 academic year distribution results should be based on the official announcement from the University Entrance Exam Center for Placement, not media estimates.

**Source:** Unable to obtain precise official data to verify this specific figure.

**Correction Suggestion:** Cite the official statistics from the University Entrance Exam Center for Placement, clearly define the calculation method for the vacancy rate, and specify the data source year.

---

### Claim 7

> "Taiwan produces approximately 4,000 doctoral graduates per year, of which more than half enter academia as faculty."

**Verdict:** False

**Verification Basis:** The first part is roughly correct — according to MOE statistics, the number of doctoral degrees awarded annually in Taiwan in recent years is approximately 3,800 to 4,200, making "approximately 4,000" a reasonable claim. However, the second part — "more than half enter academia as faculty" — does not match available data. According to the NSTC (formerly MOST) doctoral talent tracking survey and the MOE graduate career tracking survey, the proportion of doctoral graduates entering academia (as full-time faculty at higher education institutions) in recent years is approximately 25-30%. As faculty vacancies at higher education institutions have significantly decreased due to declining birth rates, new faculty positions have declined year by year, and the proportion of doctoral graduates entering academia continues to fall. Most doctoral graduates flow to industry, research institutions, or postdoctoral positions, rather than directly becoming full-time faculty.

**Sources:**
- MOE Statistics Division, *Graduate Career Tracking Survey*
- NSTC, *Doctoral Talent Development and Employment Survey*
- MOE Statistics Division, *Degrees Awarded at Higher Education Institutions*, Academic Years 111-112

**Correction Suggestion:** Revise to "Taiwan produces approximately 4,000 doctoral graduates per year, of which approximately 25-30% enter higher education institutions as full-time faculty. This proportion continues to decline as declining birth rates reduce faculty vacancies."

---

## Verification Summary Report

### Overview

| # | Claim Summary | Verdict | Severity |
|------|----------|------|--------|
| 1 | 152 higher education institutions | Warning — Partially True | Low — outdated figure |
| 2 | HEEACT is the only accreditation body | Warning — Partially True | Medium — factual error |
| 3 | Student-to-faculty ratio 1:20 | Warning — Partially True | Low — approximate but notation error |
| 4 | Over 10 schools have exited | Verified | N/A |
| 5 | HE expenditure 0.4% of GDP | Warning — Partially True | Medium — public vs private not distinguished |
| 6 | Vacancy rate 15% | Unverifiable | High — cannot verify |
| 7 | Over half of doctoral graduates enter academia | False | High — seriously inaccurate |

### Verification Statistics

- Verified: 1 claim (14%)
- Warning — Partially True: 4 claims (57%)
- False: 1 claim (14%)
- Unverifiable: 1 claim (14%)

### Overall Assessment

The overall accuracy of this set of claims is low. Of the 7 claims, only 1 is completely correct, 4 are partially correct but have omissions or insufficient precision, 1 is clearly false, and 1 cannot be verified. The most serious issue is Claim 7 (doctoral graduate career path), which diverges significantly from actual data and could lead to incorrect conclusions if used in policy discourse.

### Verification Recommendations

1. All data should indicate the specific source and year
2. Claims involving proportions or percentages should clearly define the numerator and denominator
3. Claims describing institutional systems (such as the accreditation system) should reflect the latest institutional changes
4. Claims where precise data cannot be obtained should be qualified as "estimated" or "according to media reports" rather than stated as established facts
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-examples-handoff-to-paper-md"></a>

## SOURCE: skills/deep-research/examples/handoff_to_paper.md

<!-- SOURCE-CONTENT-BEGIN bytes=11266 -->
# Handoff Example: deep-research → academic-paper

This example demonstrates how deep-research full mode, after completing research, hands off to academic-paper to begin paper writing.

---

## Scenario Setup

The user has completed deep-research full mode on the topic "AI-Assisted Quality Assurance in Higher Education: A Comparative Analysis of Implementation Strategies in East Asian Universities." Below is a summary of the research outputs.

---

## deep-research Output Summary

### 1. Research Question Brief (from research_question_agent)

```markdown
### Primary Research Question
How do East Asian universities (Taiwan, Japan, South Korea) differ in their
implementation strategies for AI-assisted quality assurance, and what factors
explain the variation in adoption patterns?

### FINER Assessment
| Criterion   | Score | Justification |
|-------------|-------|---------------|
| Feasible    | 4/5   | Public data + policy documents available |
| Interesting | 5/5   | Timely: AI policy divergence across similar systems |
| Novel       | 4/5   | Few cross-national comparisons in this space |
| Ethical     | 5/5   | No human subjects; public policy analysis |
| Relevant    | 5/5   | Directly informs HEEACT and peer agencies |
| **Average** | **4.6/5** | |

### Sub-questions
1. What AI-QA tools and frameworks have been adopted by accreditation agencies
   in Taiwan, Japan, and South Korea?
2. What institutional and policy factors facilitate or hinder AI-QA adoption?
3. To what extent do implementation outcomes align with stated policy objectives?
```

### 2. Methodology Blueprint (from research_architect_agent)

```markdown
- Paradigm: Pragmatist (comparative policy analysis)
- Method: Qualitative comparative analysis (QCA) + document analysis
- Data sources:
  - Policy documents (3 countries' QA frameworks)
  - Accreditation agency reports (HEEACT, JUAA/NIAD-QE, KCUE)
  - Published case studies and conference proceedings
- Analytical framework: Diffusion of Innovation (Rogers) +
  Institutional Isomorphism (DiMaggio & Powell)
- Validity: Triangulation across document types + member checking
  with QA practitioners
```

### 3. Annotated Bibliography (from bibliography_agent)

```markdown
23 sources identified, 18 retained after quality screening:
- 6 peer-reviewed articles (Level II-III evidence)
- 4 accreditation agency reports (Level IV)
- 3 policy documents (Level IV)
- 3 conference proceedings (Level V)
- 2 institutional case studies (Level V)

Key themes identified:
- AI adoption maturity gap (Taiwan > Korea > Japan in QA applications)
- Regulatory divergence (Japan's cautious approach vs Korea's top-down push)
- Data infrastructure as prerequisite (not just technology)
```

### 4. Synthesis Report (from synthesis_agent)

```markdown
## Core Findings

1. **Adoption patterns cluster into 3 models**:
   - Taiwan: bottom-up experimentation (agency-led pilots)
   - South Korea: top-down mandate (ministry-driven framework)
   - Japan: cautious incrementalism (voluntary guidelines)

2. **Critical success factors** (converging evidence across all 3 countries):
   - Data infrastructure maturity
   - Accreditation agency technical capacity
   - University willingness to share data
   - Clear governance framework for AI decisions

3. **Key tension**: efficiency gains vs transparency concerns
   - All 3 countries report resistance from faculty regarding "black box" decisions
   - Only Korea has attempted regulatory response (AI Ethics in Education Act 2025)

4. **Evidence gap**:
   - No rigorous outcome studies yet (all countries < 3 years into implementation)
   - Student/faculty experience data almost entirely absent

## Contradictions Identified
- Taiwan HEEACT reports "high adoption" but academic literature suggests
  most universities are still in pilot phase → definition of "adoption" varies

## Knowledge Gaps
- Impact on accreditation outcomes (pass/fail rates)
- Cost-effectiveness analysis
- Faculty perceptions and behavioral changes
```

---

## Handoff Instruction

After completing deep-research, the user inputs:

```
Now help me write a paper based on this research
```

---

## academic-paper intake_agent Auto-Detection

**intake_agent Detection Process**:

```
Scanning available materials...

[DETECTED] Research Question Brief
  - Source: deep-research / research_question_agent
  - Status: Complete (FINER 4.6/5)
  - Action: SKIP academic-paper Phase 1 (topic scoping)

[DETECTED] Methodology Blueprint
  - Source: deep-research / research_architect_agent
  - Status: Complete (pragmatist QCA + document analysis)
  - Action: SKIP academic-paper Phase 2 (methodology design)
  - Note: Will integrate into Method section directly

[DETECTED] Annotated Bibliography (18 sources, APA 7.0)
  - Source: deep-research / bibliography_agent
  - Status: Complete, quality-screened
  - Action: SKIP academic-paper literature search
  - Note: Will use as foundation for Literature Review section

[DETECTED] Synthesis Report
  - Source: deep-research / synthesis_agent
  - Status: Complete (3 core findings + 1 contradiction + 2 gaps)
  - Action: SKIP academic-paper analysis phase
  - Note: Will structure Findings and Discussion sections around synthesis

Materials Assessment: COMPREHENSIVE
Recommended academic-paper mode: full (with accelerated pipeline)
Estimated sections already covered: 60-70%
Remaining work: Writing, formatting, argumentation, and polish
```

---

## Skipped Steps and Reasons

| academic-paper Step | Normal Workflow | After Handoff | Reason |
|---------------------|---------|-----------|------|
| Phase 1: Topic Scoping | intake_agent clarifies from scratch | SKIPPED | RQ Brief is complete |
| Phase 2: Structure Planning | outline_agent designs structure | PARTIAL | Has Blueprint but needs conversion to paper structure |
| Phase 3: Literature Search | literature_agent searches | SKIPPED | Bibliography is complete |
| Phase 4: Literature Review Writing | review_writer_agent writes | ACTIVE | Has Synthesis but needs conversion to paper tone |
| Phase 5: Methodology Writing | method_writer_agent writes | ACTIVE | Has Blueprint but needs expansion to full paragraphs |
| Phase 6: Findings Writing | findings_writer_agent writes | ACTIVE | Has Synthesis but needs expanded argumentation |
| Phase 7: Discussion Writing | discussion_writer_agent writes | ACTIVE | Needs original discourse (not direct copy of Synthesis) |
| Phase 8: Intro + Conclusion | bookend_agent writes | ACTIVE | Needs to be written based on full text |
| Phase 9: Abstract + Formatting | format_agent processes | ACTIVE | Needs full text completion first |
| Phase 10: Self-Review | review_agent reviews | ACTIVE | Must be executed |

---

## Post-Handoff academic-paper Actual Workflow

```
=== academic-paper: Accelerated Pipeline ===

Step 1: STRUCTURAL MAPPING
  [outline_agent]
  - Input: RQ Brief + Methodology Blueprint + Synthesis Report
  - Output: Complete paper outline, each section tagged with corresponding deep-research materials
  - Output example:

    I. Introduction
       - Context: AI in HE QA (from Synthesis background)
       - Problem: Cross-national variation unexplained
       - Purpose: Compare 3 East Asian models
       - RQ: [Directly cite RQ Brief]

    II. Literature Review
       - 2.1 AI in Quality Assurance (from Bibliography themes)
       - 2.2 Diffusion of Innovation framework (from Blueprint)
       - 2.3 Institutional Isomorphism (from Blueprint)
       - 2.4 East Asian HE systems comparison

    III. Methodology
       - 3.1 Research design: QCA + document analysis (from Blueprint)
       - 3.2 Case selection and data sources
       - 3.3 Analytical framework
       - 3.4 Validity and limitations

    IV. Findings
       - 4.1 Three adoption models (from Synthesis Finding 1)
       - 4.2 Critical success factors (from Synthesis Finding 2)
       - 4.3 Efficiency vs transparency tension (from Synthesis Finding 3)

    V. Discussion
       - 5.1 Theoretical implications
       - 5.2 Policy implications for accreditation agencies
       - 5.3 Practical recommendations
       - 5.4 Limitations (from Synthesis gaps + Blueprint validity)

    VI. Conclusion
       - Summary + Future research directions

Step 2: SECTION WRITING (Parallel)
  [review_writer_agent] → Literature Review
    - Based on Annotated Bibliography and Synthesis, transform into a fluent literature review
    - Not sequential summaries, but thematic integration

  [method_writer_agent] → Methodology
    - Expand the Blueprint into complete methodology paragraphs
    - Add technical details and procedural explanation for QCA

  [findings_writer_agent] → Findings
    - Expand the Synthesis's 3 core findings into evidence-supported arguments
    - Each finding accompanied by specific cases and data
    - Address contradictions flagged in the Synthesis

Step 3: DISCUSSION + BOOKENDS
  [discussion_writer_agent] → Discussion
    - Original discourse: dialogue between findings and theory
    - Does not repeat Findings; instead explains "why"
    - Integrates deep-research Knowledge Gaps as Future Research

  [bookend_agent] → Introduction + Conclusion
    - Introduction: from macro context to specific RQ
    - Conclusion: no new information, echoes RQ and looks to the future

Step 4: ABSTRACT + FORMAT
  [format_agent]
    - Abstract: 150-250 words, IMRAD structure
    - APA 7.0 full-text formatting
    - Reference list cleanup (based on Bibliography + newly added citations)

Step 5: SELF-REVIEW
  [review_agent]
    - Internal consistency check (RQ → Method → Findings → Discussion logic chain)
    - Citation completeness (every claim has a citation)
    - Format compliance
    - Verdict: Ready for submission / Needs revision
```

---

## User-Facing Handoff Experience

**academic-paper's Opening Message**:

> I've read your complete outputs from the deep-research stage, including:
> - Research Question Brief (FINER 4.6/5)
> - Methodology Blueprint (QCA + document analysis)
> - Annotated Bibliography (18 quality-screened sources)
> - Synthesis Report (3 core findings + 2 knowledge gaps)
>
> Based on these materials, I've completed a preliminary plan for the paper outline. Here is the planned paper structure:
> [Display outline]
>
> I have two questions that need your confirmation:
> 1. What is your target journal? (This affects word limits and formatting requirements)
> 2. Should the paper language be English or bilingual?
>
> Once confirmed, I'll begin writing. Because the research foundation is already comprehensive, I can skip the early exploration stages and proceed directly to paper writing.

---

## Notes

1. **Not copy-paste**: academic-paper does not directly copy deep-research outputs, but transforms them into the tone and format of an academic paper
2. **May discover new issues**: During the writing process, academic-paper agents may discover points missed by deep-research and will proactively supplement them
3. **Still requires user confirmation**: Target journal, language preference, specific formatting requirements still require user input
4. **Review recommendation auto-connects**: After paper completion, the user can continue with `academic-paper-reviewer` for formal review
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-examples-policy-analysis-md"></a>

## SOURCE: skills/deep-research/examples/policy_analysis.md

<!-- SOURCE-CONTENT-BEGIN bytes=9609 -->
# Example: Policy Analysis (full mode)

## User Request
```
Research comparing outcomes-based funding models in higher education across OECD countries
```

## Phase 1: SCOPING

### research_question_agent Output

**Primary Research Question**:
> What are the design features, implementation strategies, and measured outcomes of performance-based funding (PBF) models in OECD higher education systems, and what contextual factors explain variation in effectiveness?

**FINER Assessment**:
| Criterion | Score | Justification |
|-----------|-------|---------------|
| Feasible | 4/5 | Substantial literature + OECD data available |
| Interesting | 4/5 | Active policy debate across multiple countries |
| Novel | 3/5 | Several reviews exist but few systematic cross-country comparisons |
| Ethical | 5/5 | Public policy analysis, no ethical concerns |
| Relevant | 5/5 | Directly informs national HE funding policy |
| **Average** | **4.2/5** | |

**Sub-questions**:
1. What PBF design features (metrics, weights, mechanisms) are used across OECD countries?
2. What outcomes (intended and unintended) have been documented?
3. What contextual factors (governance, culture, market structure) mediate PBF effectiveness?

### research_architect_agent Output

**Paradigm**: Pragmatist
**Method**: Comparative policy analysis with systematic evidence review
**Framework**: Modified Bardach's Eightfold Path + most-similar-systems design
**Data**: OECD reports, national policy documents, academic literature
**Analysis**: Cross-case comparison matrix + thematic synthesis

### devils_advocate_agent — CHECKPOINT 1

**Verdict**: PASS
- Minor: "Effectiveness" needs operational definition — suggest specifying measurable dimensions
- Observation: Country selection will significantly affect conclusions — justify selection criteria

## Phase 2: INVESTIGATION

### bibliography_agent Output

22 academic articles + 8 OECD/government reports + 3 think tank publications = 33 sources

Key sources include:
- OECD (2019). *Benchmarking Higher Education System Performance*
- Hillman, N. W., Tandberg, D. A., & Fryar, A. H. (2015). Evaluating the impacts of "new" performance funding in higher education. *Educational Evaluation and Policy Analysis*, *37*(4).
- de Boer, H., et al. (2015). *Performance-based funding and performance agreements in fourteen higher education systems*. CHEPS.

### source_verification_agent Output

33 sources assessed: 28 Grade A-B, 4 Grade C, 1 Grade D (included with caveat)

## Phase 3: ANALYSIS

### synthesis_agent Output

**Comparative Matrix** (8 countries x 6 design features x 4 outcome dimensions)

Countries analyzed: US (Tennessee, Ohio), Australia, Denmark, Netherlands, Finland, UK (England), South Korea, Chile

**Key Findings**:

1. **Design convergence**: Most PBF models use graduation rates and retention as primary metrics, but weights and mechanisms vary dramatically. Tennessee allocates 85% of state funding based on outcomes (the highest proportion globally), while most European models tie less than 5% to performance. Despite this range, all models converge on a similar set of 4-6 core metrics: completion, retention, research output, and employment.

2. **Modest positive effects on targeted metrics**: Graduation rates show small positive effects (2-5 percentage points) in most contexts where PBF has been implemented for more than 3 years. Tennessee's model, the most studied, shows a 3.2 percentage point increase in 6-year graduation rates after controlling for student demographics (Hillman et al., 2015). However, several studies note difficulty in attributing causality given concurrent policy changes.

3. **Significant unintended consequences**: Grade inflation, cream-skimming, narrowing of institutional mission documented in multiple countries. In Australia, the demand-driven system (2012-2017) led to rapid enrollment growth but declining completion rates at some institutions. In the US, evidence from Indiana suggests institutions may have shifted enrollment toward better-prepared students rather than improving outcomes for existing students (Umbricht et al., 2017).

4. **Context is king**: Governance structure (centralized vs. decentralized) is the strongest moderator of PBF effectiveness. Centralized systems (Denmark, Finland, Netherlands) show more consistent implementation and fewer gaming behaviors than decentralized systems (US states, Australia). The mechanism appears to be: centralized systems can enforce compliance and adjust metrics more rapidly, while decentralized systems create more opportunities for strategic behavior.

5. **Equity concerns**: Institutions serving disadvantaged students consistently report greater difficulty meeting PBF targets. This is documented across all 8 countries studied, though the magnitude varies. Tennessee partially addresses this through "premium" weights for Pell-eligible students and adult learners, while most European models lack explicit equity adjustments.

**Major Contradiction**: US state-level studies show mixed results (Tennessee positive, Ohio neutral, Indiana negative), while European models show more consistent modest effects — likely explained by funding proportion (US: 5-25% of budget; Europe: often < 5%).

### devils_advocate_agent — CHECKPOINT 2

**Verdict**: PASS
- Major (downgraded from Critical): Selection of 8 countries needs stronger justification — why not Germany, Japan, Canada?
- Minor: "Context is king" is an assertion — specify which contextual variables and their mechanisms

## Phase 4: COMPOSITION

### report_compiler_agent Output

**Title**: Performance-Based Funding in OECD Higher Education: A Comparative Analysis of Design, Outcomes, and Contextual Mediators

**Word Count**: 6,800 words

**Structure**:
1. **Introduction** (600 words): PBF as global policy trend; rationale for comparative analysis
2. **Literature Review** (1,200 words): Evolution of PBF models from 1970s to present; theoretical foundations (principal-agent theory, new public management, institutional theory)
3. **Methodology** (800 words): Comparative policy analysis framework; country selection criteria (most-similar-systems with variation on key variables); data sources and analytical approach
4. **Findings**:
   - 4.1 Design Feature Comparison (1,200 words): Cross-case matrix of 8 countries across 6 design dimensions (metrics, weights, mechanism type, funding proportion, adjustment frequency, equity provisions)
   - 4.2 Outcome Evidence (800 words): Intended effects on graduation, retention, research output
   - 4.3 Unintended Consequences (600 words): Gaming, cream-skimming, mission drift, administrative burden
   - 4.4 Contextual Mediators (600 words): Governance, market structure, institutional culture, data infrastructure
5. **Discussion** (600 words): Implications for policy design; transferability considerations
6. **Recommendations** (400 words): 5 evidence-based design principles
   - R1: Keep performance-linked proportion below 10% initially
   - R2: Include explicit equity adjustments from the start
   - R3: Use improvement metrics alongside absolute metrics
   - R4: Build in 3-year review cycles with stakeholder input
   - R5: Invest in institutional data capacity before implementation
7. **Limitations & Future Research** (300 words)
8. **References** (33 sources in APA 7.0)

## Phase 5: REVIEW

### editor_in_chief_agent Output

**Verdict**: Accept with Minor Revision (Score: 4.1/5.0)
- Strength: Well-structured comparative framework; balanced treatment of evidence
- Minor: Table 2 (design features) needs a notes column to explain country-specific nuances
- Minor: Recommendation #5 (data capacity) needs supporting evidence — currently assertion-based

### ethics_review_agent Output

**Verdict**: CLEARED
- AI disclosure: Present and accurate
- References spot-checked: 7/33 (21%) verified — all confirmed
- Dual-use risk: Low (public policy analysis)
- Fair representation: Adequate — noted absence of non-OECD perspectives as limitation
- Potential bias: Report slightly favors European models over US models; flagged for author awareness

### devils_advocate_agent — CHECKPOINT 3

**Verdict**: PASS
- Observation: Conclusion recommendation #3 ("use improvement metrics alongside absolute metrics") is the strongest recommendation but has the weakest evidence base — only 2 countries have implemented this
- "So what?" test: Passed — clear implications for policymakers designing or reforming PBF systems
- Counterfactual check: What if PBF effects are entirely explained by the Hawthorne effect (attention to metrics, not funding mechanism)? This alternative explanation is not adequately addressed

## Phase 6: REVISION

### report_compiler_agent (Revision 1)

**Changes**:
1. Table 2 expanded with notes column explaining country-specific nuances (Minor, Editor)
2. Recommendation #5 supported with evidence from Finnish data infrastructure investment (Minor, Editor)
3. Discussion section expanded to address Hawthorne effect alternative explanation (Observation, Devil's Advocate)
4. Country selection justification strengthened in Methodology — added explicit criteria and acknowledged Germany, Japan, Canada as excluded cases with rationale (Major, Devil's Advocate from Checkpoint 2)

**Final Word Count**: 6,800 words
**Revision Loops Used**: 1 of 2

---

## Final Output Summary
- Full APA 7.0 report: 6,800 words
- 33 cited sources (Levels I-VII)
- 8-country comparative matrix
- 5 key findings
- 5 evidence-based policy recommendations
- Ethics cleared
- 1 revision loop completed
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-examples-review-mode-md"></a>

## SOURCE: skills/deep-research/examples/review_mode.md

<!-- SOURCE-CONTENT-BEGIN bytes=17751 -->
---
scenario: Reviewing a policy recommendation summary
mode: review
agents_used:
  - editor_in_chief_agent
  - ethics_review_agent
  - devils_advocate_agent
input: User provides an approximately 300-word policy recommendation text about Taiwan's higher education
output: Complete reports from three review agents + revision recommendation summary
---

# Review Mode Example: Policy Recommendation Summary Review

This example demonstrates the complete workflow of `review` mode. The user provides a previously written policy recommendation summary, and deep-research activates three review agents for multi-dimensional review.

---

## User Request

```
Please use review mode to review the following policy recommendation summary:

"Facing the wave of declining birth rates, Taiwan's higher education system urgently needs
structural reform. According to MOE statistics, the number of first-year university students
in 2024 has dropped to 180,000, a decrease of over 40% compared to 2015. Private universities
have borne the brunt, with 12 schools already initiating exit mechanisms. This paper proposes
three major policy directions: First, establish cross-institutional credit recognition
alliances, allowing students to take courses across institutions and accumulate credits, thereby
improving educational resource utilization efficiency; Second, promote public-private merger
mechanisms, where public universities acquire struggling private universities, integrating
campus facilities, faculty, and equipment resources; Third, establish a Higher Education
Transformation Fund, providing each school up to NTD 500 million in transformation subsidies,
supporting schools in developing distinctive fields or transforming into lifelong learning
institutions. If the above three policies can be advanced simultaneously, it is estimated that
supply-demand imbalance can be reduced by 30% within five years while maintaining higher
education quality and regional accessibility. However, policy implementation must overcome
restrictions on dismissal under the Teachers' Act, disputes over campus property ownership, and
community resistance to school closures. Overall, Taiwan's higher education system must shift
from passive exit to proactive transformation in order to maintain competitiveness amid dramatic
demographic structural changes."
```

---

## Review Pipeline Activation

**Mode Detection**: User explicitly requests `review mode` and provides text to be reviewed. Activating 3 review agents:

1. `editor_in_chief_agent` — Academic quality and argumentation review
2. `ethics_review_agent` — Ethics and fairness review
3. `devils_advocate_agent` — Counter-arguments and challenges

---

## editor_in_chief_agent Review Report

### Review Summary

| Dimension | Score | Description |
|------|------|------|
| Originality | 3/5 | The three policy proposals have been discussed in existing literature; lacks novel perspectives |
| Rigor | 2/5 | Multiple data claims lack source citations; reasoning process has logical leaps |
| Evidence sufficiency | 2/5 | Only cites one source (MOE statistics); weak evidentiary basis |
| Argument coherence | 3/5 | The logical connection between the three policies is not sufficiently clear |
| Writing quality | 4/5 | Fluent writing, complete structure, reasonable paragraph organization |
| **Overall** | **2.8/5** | **Recommend Major Revision** |

### Paragraph-by-Paragraph Review

**Paragraph 1 (Problem Description)**:
> "The number of first-year university students in 2024 has dropped to 180,000, a decrease of over 40% compared to 2015"

Review comment: This data needs a source citation. According to MOE higher education overview statistics, the actual number of first-year daytime program students in Academic Year 2024 is approximately 192,000, not 180,000. Furthermore, the 2015 comparison baseline needs clarification on whether it refers to "academic year" or "calendar year" — the two may produce differences in cross-year data. Recommend correcting to the precise figure with source citation and academic year noted.

> "12 schools already initiating exit mechanisms"

Review comment: As of the end of 2024, the total number of schools listed for special counseling under the "Private Senior High School and Above Exit Act" plus those that have already suspended enrollment needs to be verified. The calculation method for "12" here is unclear — does it include schools that have already completed exit? Is it limited to higher education institutions? Recommend clearly defining the statistical scope and citing the exit regulations implementation report.

**Paragraph 2 (Policy Proposal 1: Cross-Institutional Credit Recognition Alliance)**:
> "Allowing students to take courses across institutions and accumulate credits, improving educational resource utilization efficiency"

Review comment: This proposal does not consider key practical barriers. Taiwan already has cross-institutional course-taking mechanisms such as the "Top University Alliance" and "University System of Taiwan." However, utilization rates are low (most alliances have cross-institutional course-taking rates below 3%). Recommend analyzing why existing mechanisms have been ineffective, then explaining how the new alliance would overcome these barriers; otherwise the proposal lacks incremental value.

**Paragraph 3 (Policy Proposal 2: Public-Private Merger Mechanism)**:
> "Public universities acquire struggling private universities"

Review comment: The term "acquire" has precise legal meaning, but the text does not discuss the applicability of relevant laws such as the Private School Act and National Property Act. There is no precedent for public universities merging with private universities in Taiwan, and the legal pathway for converting institutional legal status (from a foundation to an administrative corporation/national school) remains unclear. Recommend revising to "consolidation" or "merger" and discussing feasibility within the current legal framework.

**Paragraph 4 (Policy Proposal 3: Higher Education Transformation Fund)**:
> "Providing each school up to NTD 500 million in transformation subsidies"

Review comment: What is the basis for the NTD 500 million figure? No cost estimation logic is provided. If calculated for 30 potentially eligible schools, the fund would need to reach NTD 15 billion, which represents a significant proportion of MOE's Higher Education Department annual budget. Recommend providing a policy cost-benefit analysis, or at minimum citing comparable international case funding scales as reference.

**Paragraph 5 (Effect Estimate)**:
> "Estimated to reduce supply-demand imbalance by 30% within five years"

Review comment: This is the weakest argument in the paper. The "30%" estimate has no calculation basis or model support, and the operational definition of "supply-demand imbalance" is unclear — does it refer to the gap between enrollment quota and applicants? Or the ratio of school numbers to student demand? Recommend either deleting this unsupported estimate or providing the estimation model and assumptions.

### Editorial Verdict

**Verdict: MAJOR REVISION**

Core issues:
1. Insufficient data accuracy; multiple figures need verification and correction
2. Policy proposals lack analysis of existing mechanisms; incremental value not explained
3. Effect estimate has zero basis, damaging overall credibility
4. Lacks international comparison cases for support

---

## ethics_review_agent Review Report

### Ethics Review Summary

| Dimension | Verdict | Description |
|------|------|------|
| AI disclosure compliance | N/A | Text under review is not within AI disclosure scope |
| Attribution integrity | CONDITIONAL | Insufficient data source citations |
| Dual-use risk | CLEARED | No sensitive dual-use concerns |
| Fair representation | CONDITIONAL | Stakeholder perspectives imbalanced |
| **Overall Verdict** | **CONDITIONAL** | **Needs supplementation to pass** |

### Item-by-Item Analysis

**1. Stakeholder Fair Representation**

This text is written from a "policymaker" perspective, but the stakeholders involved include at least five groups:

- Students (learning rights, degree recognition)
- Faculty (employment rights, academic freedom)
- Administrative staff (job stability)
- Communities (regional accessibility, local development)
- Private school boards (campus property disposition rights)

The text only briefly mentions Teachers' Act restrictions and community resistance in the final paragraph, without presenting these groups' perspectives or needs. In particular:

> "Policy implementation must overcome restrictions on dismissal under the Teachers' Act"

This framing positions teachers' employment rights protection as "an obstacle to overcome," implicitly placing teacher rights below policy efficiency — a value judgment. From an ethical perspective, "the legitimacy of teacher employment protection" and "the need for system efficiency" should be presented as equal tensions, rather than unidirectionally describing the former as an impediment to the latter.

**2. Missing Vulnerable Population Impact Assessment**

The impact of public-private mergers and exit mechanisms on the following groups is not discussed:

- Rural students: If local schools exit or are merged, increased commuting distances would disproportionately affect economically disadvantaged students
- Students with disabilities: Accessibility facility transition issues during campus changes
- Indigenous program students: Whether culturally specific courses can be maintained after mergers

Recommend adding a "vulnerable population impact assessment" section to the policy proposals.

**3. Regional Justice Issues**

> "Public universities acquire struggling private universities, integrating campus facilities, faculty, and equipment resources"

This proposal may exacerbate the urban-rural divide in higher education resources. Struggling private universities are mostly located in non-metropolitan areas, while public universities capable of carrying out mergers are mostly in metropolitan areas. If resources are concentrated at metropolitan campuses after merger, this would further damage higher education accessibility in non-metropolitan areas. Recommend adding regional impact assessment and supporting measures.

### Ethics Verdict

**Verdict: CONDITIONAL**

Conditions for passing:
1. Supplement multi-stakeholder perspective presentation
2. Add vulnerable population impact assessment
3. Revise the "overcome Teachers' Act restrictions" framing to a more balanced presentation
4. Add discussion of the regional justice dimension

---

## devils_advocate_agent Review Report

### Counter-Argument Challenges

**Challenge 1: Can cross-institutional credit recognition alliances really improve efficiency?**

Original claim:
> "Establish cross-institutional credit recognition alliances...improving educational resource utilization efficiency"

Counter-argument: The root cause of low utilization in existing cross-institutional course-taking mechanisms is not institutional design but physical distance and time cost. Students won't commute to another school for one course unless that course is highly attractive and irreplaceable. Online courses can partially solve the distance problem, but Taiwan's higher education system remains conservative about recognizing online credits. Furthermore, credit recognition involves inter-institutional trust in teaching quality — would higher-ranked schools be willing to recognize credits from lower-ranked schools? If not, the alliance would become a one-way flow, ultimately accelerating the marginalization of weaker schools.

**Conclusion**: This policy proposal needs to address the question of "why will it be different this time." Without analyzing the structural reasons for existing mechanisms' failure, a new alliance proposal is difficult to find convincing.

**Challenge 2: The premise assumption of public-private mergers may be wrong**

Original claim:
> "Public universities acquire struggling private universities, integrating campus facilities, faculty, and equipment resources"

Counter-argument: This proposal implicitly assumes that "public universities have the motivation and capacity to absorb private universities." But the reality is the opposite:

1. Public universities themselves face enrollment pressure; merging only adds burden
2. Private universities' campuses are often leased or in remote locations, unattractive to public universities
3. If private university faculty cannot pass public university faculty evaluation standards, mass dismissals would follow
4. Japan's national university corporation merger cases (e.g., Hokkaido United University Institution) show that post-merger integration costs often exceed expected benefits

A completely opposite argument: rather than pushing public-private mergers, let market mechanisms naturally eliminate schools, with the government's role limited to protecting student rights (such as credit transfer, scholarship transfer) rather than maintaining excessive institutional survival.

**Challenge 3: The five-year 30% supply-demand imbalance reduction estimate cannot withstand scrutiny**

Original claim:
> "Estimated to reduce supply-demand imbalance by 30% within five years"

Counter-argument: This is a textbook case of "intuition dressed up with numbers."

1. The quantitative indicator for supply-demand imbalance is undefined: is it total enrollment vacancies? Number of suspended programs? Number of school exits?
2. No calculation basis for 30% exists: the contribution of each of the three policies has not been disaggregated
3. The five-year timeframe is unrealistic: Japan launched national university corporatization in 2004; the first corporate merger (2022) took 18 years
4. Policy effects have time lags and interaction effects: simultaneously advancing three policies could create interference (e.g., a transformation fund reduces exit pressure, potentially delaying necessary structural adjustment)

This paragraph should be completely deleted or revised to "further policy simulation research is needed to evaluate expected effects."

**Challenge 4: The definition of "proactive transformation" is unclear**

Original claim:
> "Taiwan's higher education system must shift from passive exit to proactive transformation"

Counter-argument: This is a rhetorically powerful but operationally vague conclusion. What is "proactive transformation"? For a school that has failed to meet minimum enrollment standards for five consecutive years, exit is the most reasonable transformation. Insisting on keeping a school running with no students, using "transformation" to justify "delay," wastes public resources. The text does not distinguish between "salvageable" and "unsalvageable" schools, but policy design must make this harsh classification.

### Challenge Summary

| Challenge | Severity | Recommendation |
|------|--------|------|
| Cross-institutional alliance lacks incremental value argument | Medium | Add analysis of existing mechanism failures |
| Public-private merger premise assumption is flawed | High | Re-argue feasibility and motivation |
| 30% estimate has no basis | Critical | Delete or change to research recommendation |
| "Proactive transformation" definition is vague | Medium | Add operational definition and classification |

---

## Revision Recommendation Summary

### Consensus Issues Across All Three Agents

The following three issues were raised in all review agents' reports:

1. **Data accuracy**: Core statistics (180,000, 40%, 12 schools) all need verification, correction, and source citation
2. **Insufficient policy feasibility argument**: All three proposals remain at "what should be done" rather than "how to do it" and "why it can be done"
3. **Effect estimate has no basis**: The "30%" figure damages overall credibility

### Priority Revision Items (by severity)

| Priority | Revision Item | Source |
|--------|----------|------|
| 1 | Delete or substantially revise the "reduce by 30% within five years" estimate | editor + devil's advocate |
| 2 | Add source citations to all data, correct inaccurate figures | editor |
| 3 | Analyze why existing cross-institutional course-taking mechanisms failed, argue the incremental value of the new proposal | devil's advocate |
| 4 | Add multi-stakeholder perspectives and vulnerable population impact assessment | ethics |
| 5 | Add international comparison cases (Japan, South Korea) | editor |
| 6 | Revise "overcome Teachers' Act restrictions" to a more balanced framing | ethics |
| 7 | Distinguish between "transformable" and "should exit" school types | devil's advocate |
| 8 | Add policy cost estimation and cost-benefit analysis framework | editor |

### Revised Conclusion Suggestion (for reference)

> "Facing the challenge of declining birth rates, Taiwan's higher education system needs structural reform that balances efficiency and equity. This paper proposes three policy directions: cross-institutional credit recognition, public-private consolidation, and a transformation fund. However, each policy must overcome the structural barriers of existing mechanisms, and implementation must balance teacher employment protection, student learning rights, and regional higher education accessibility. Quantitative evaluation of policy effects requires further simulation research, not intuitive estimates. Most importantly, policy design should differentiate schools' transformation potential: for schools that genuinely cannot operate sustainably, provide dignified exit pathways, while concentrating limited resources on institutions with transformation potential."
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-examples-socratic-guided-research-md"></a>

## SOURCE: skills/deep-research/examples/socratic_guided_research.md

<!-- SOURCE-CONTENT-BEGIN bytes=23472 -->
# Socratic Mode Example: Impact of Declining Birth Rates on Taiwan's Private University Management Strategies

This example demonstrates the complete multi-round dialogue process in Socratic mode, from a vague research interest to a clear Research Plan Summary.

---

## Scenario Setup

**User**:
```
Guide my research on the impact of declining birth rates on private universities
```

**System**: Detects trigger phrase "guide my research" → activates Socratic mode → invokes socratic_mentor_agent

---

## Layer 1: PROBLEM FRAMING — Problem Definition

### Round 1

**Socratic Mentor**:

The impact of declining birth rates on private universities — this is certainly one of the most discussed and urgent topics in Taiwan's higher education sector. But "impact" is a broad word, and I'd like to understand your starting point first.

When you say "impact," what specific phenomenon have you observed that made you want to explore this? For example, was it news of a university closing that got you thinking? Or did you encounter a challenge related to declining birth rates in your work?

**User**:
I work at a private university of technology, and enrollment has been getting harder and harder in recent years, especially for the daytime division. Our school has already started closing down some departments. I want to know how private universities should respond to this situation.

### Round 2

**Socratic Mentor**:

Starting from your own work experience is great — the most meaningful research often comes from real observations. The phenomena you mentioned are very specific: difficulty in daytime division enrollment, department closures.

[INSIGHT: The user's core concern is not just declining birth rates per se, but the "response strategies" of private universities under the pressure of declining birth rates]

But let me follow up: you said "how should they respond" — do you want to find out "what other schools are actually doing" (a descriptive question), or do you want to evaluate "which strategies are actually effective" (an evaluative question)?

These two directions are very different: the former is surveying the current state, the latter is judging effectiveness. Which one is closer to what you want to answer?

**User**:
I'm more interested in which strategies are actually effective. Because I see many schools doing transformation, but some seem effective while others seem to just be hanging on. I want to know what makes the difference.

### Round 3

**Socratic Mentor**:

Good — what you want to do is not just document phenomena, but understand "why some schools' transformations succeed while others fail." This is a question with analytical depth.

[INSIGHT: Research question direction: Among the transformation strategies adopted by private universities in response to declining birth rates, what factors differentiate successful from failed cases]

So let me ask: you said "effective" and "just hanging on" — how do you define "effective" in your mind? Is it enrollment numbers recovering? Financial indicators improving? Or just staying alive counts as effective?

Defining the criteria for "success" will directly affect your research conclusions. What do you think constitutes a transformation strategy being "truly effective"?

**User**:
I don't think we can just look at enrollment numbers. Some schools have stabilized their enrollment, but by lowering admission standards and recruiting large numbers of international students, with serious quality issues. I think "effective" should mean the school can sustain operations while maintaining a certain level of educational quality.

### Round 4

**Socratic Mentor**:

You've made a very important distinction: not all "survival" equals "success." You believe success needs to simultaneously satisfy two conditions — operational sustainability and educational quality.

[INSIGHT: The user's definition of "successful transformation" is a dual standard: (1) operational sustainability (financial viability) + (2) maintaining educational quality, not just enrollment numbers]

This gives your research more depth, but also more complexity. I want to confirm something: you said "a certain level of educational quality" — how do you plan to measure quality? Would you use HEEACT accreditation results? Graduate employment rates? Employer satisfaction? Or other indicators?

Also, how much quality decline do you consider "problematic"? Is there a floor you can accept?

**User**:
I haven't thought this through yet. Maybe I could use accreditation results plus graduate employment rates? But I know those indicators have problems too...

**Socratic Mentor**:

Your awareness of the limitations of the indicators themselves is one of the most important aspects of self-awareness in research. We don't need to decide on the perfect measurement method right now — that's a task for the methodology stage. But you've already started thinking about it, which is great.

Let me organize our discussion so far. Your research question seems to be converging toward this direction: "In the context of Taiwan's declining birth rates, among the transformation strategies adopted by private universities, which strategies can achieve operational sustainability while maintaining educational quality? What are the key differentiating factors between successful and failed cases?"

Does this direction capture your core concern? Or is something missing?

[INSIGHT: Candidate RQ direction confirmed: comparing successful and failed private university transformation strategies, focusing on the dual success criteria of quality maintenance + operational sustainability]

**User**:
Yes, that's roughly the direction. But is it too broad? There are a lot of private universities in Taiwan.

**Socratic Mentor**:

Good self-awareness. Indeed, if you want to compare "all" private universities, the scope would be too large. How do you think you could narrow it down? Are there specific types you want to focus on — such as universities of technology? Or schools of a specific size? Or a specific region?

---

## Layer 2: METHODOLOGY REFLECTION — Methodological Reflection

### Round 5

**User**:
I'm more familiar with private universities of technology, and the challenges they face are different from general private universities — they rely more on industry-academia partnerships and the vocational education system. I want to focus on private universities of technology.

**Socratic Mentor**:

Focusing on private universities of technology is a reasonable choice — you have first-hand experience, and technology universities indeed have a unique positioning and set of challenges.

[INSIGHT: Research scope narrowed to Taiwan's private universities of technology, due to the user's practical experience and the unique positioning of technology universities (reliance on industry-academia partnerships, vocational education system)]

Now let's move to the next important question: how do you plan to answer this question? Have you thought about what research method to use — such as surveys, case studies, statistical analysis, or interviews?

**User**:
I want to do case studies. Pick a few technology universities that have succeeded and failed in their transformation for comparison.

### Round 6

**Socratic Mentor**:

Multiple case comparison is a classic strategy analysis method that suits your question well. But let me follow up on a few things.

First, how do you plan to select cases? You said "succeeded and failed in transformation" — but in selecting cases, you'd need to first judge who succeeded and who failed, and you just said the definition of "success" isn't fully worked out yet. Could you end up in a loop: using the criteria you want to study to select the sample, then evaluating with those same criteria?

Second, "a few" — how many? 2? 6? 10? This affects how deep your analysis can go.

**User**:
Hmm... you're right, the case selection issue does need to be thought through first. Maybe I could use some objective indicators for preliminary screening, like changes in enrollment rates and financial status, then do in-depth analysis. Probably 4-6 schools?

**Socratic Mentor**:

4-6 is a manageable number, consistent with common practice in multiple case comparison research. Using objective indicators for preliminary screening, then doing in-depth analysis — this two-stage design is very practical.

[INSIGHT: Methodology choice: multiple case comparison method, 4-6 private technology universities, using objective indicators (enrollment rates, financials) for preliminary screening, then in-depth analysis of strategy differences]

One last methodology question: how do you plan to do the "in-depth analysis"? Interview presidents and administrators? Analyze public documents and reports? Or both? Do you think you can obtain this data?

**User**:
I should be able to interview a few technology university administrators through my network. And public data like MOE statistics and schools' self-assessment reports can also be used.

**[devils_advocate_agent triggered here — Checkpoint]**

**Devil's Advocate Challenge (integrated into Mentor's guidance)**:

My colleague raised a question worth thinking about: your interview subjects are all "administrators" — wouldn't they tend to describe their school's strategies as more planned than they actually were? After all, nobody is going to say in an interview "we actually had no idea what we were doing." How do you handle this social desirability bias?

---

## Layer 3: EVIDENCE DESIGN — Evidence Strategy

### Round 7

**User**:
Right, that's a problem. Maybe I can cross-validate — not just listen to what administrators say, but also check whether actual data supports their claims.

**Socratic Mentor**:

Cross-validation is an excellent strategy — in academic terms it's called triangulation. Using interview data plus statistical data to corroborate each other improves the credibility of your conclusions.

[INSIGHT: Data collection strategy employs triangulation: (1) administrator interviews (subjective experience) + (2) MOE statistical data (objective indicators) + (3) self-assessment report document analysis, with all three cross-validating each other]

Now let me ask you a sharper question: what kind of finding would make you change your conclusion? For example, if you originally thought "industry-academia partnerships" were the key to success, but the data shows that successful and failed schools don't differ significantly in industry-academia partnerships, what would you do?

**User**:
Then I'd need to accept that result and look for other explanatory factors.

### Round 8

**Socratic Mentor**:

Your attitude is excellent — being willing to let data change your mind is the most fundamental honesty in research.

Now let me ask a question you might not want to face: what are you most worried about not finding? Is there a possible finding that scares you because it would make the entire research meaningless?

**User**:
What I'm most worried about is... if it turns out that school success or failure has nothing to do with strategy at all, and is purely determined by geographic location and historical reputation. Then my research would become "no strategy is useful."

**Socratic Mentor**:

That's actually a very valuable finding — if geographic location and historical reputation are the decisive factors, then the implications for policymakers would be entirely different. You don't need to be afraid of a "no strategy is useful" conclusion, because that itself is a conclusion.

[INSIGHT: Important alternative hypothesis: Private technology universities' survival may depend more on structural factors (geographic location, historical reputation) than on active transformation strategies. This hypothesis doesn't make the research meaningless; rather, it would change the direction of policy recommendations]

However, if you want to control for the influence of these factors, you could intentionally pair cases during selection: choose one successful and one failed school from the north, one successful and one failed school from the south. That way geographic location is controlled. What do you think?

**User**:
Yes, paired design makes a lot of sense. I can pair by geographic location and school size.

---

## Layer 4: CRITICAL SELF-EXAMINATION — Critical Self-Review

### Round 9

**Socratic Mentor**:

Paired design can address some confounding factors. Good.

[INSIGHT: Case selection uses paired design: geographic location and school size as pairing conditions to control the influence of structural factors]

Now let's honestly face the limitations of this research. You work at one of these private technology universities — do you think this identity is an advantage or a disadvantage for your research? Or both?

**User**:
Both, I think. The advantage is that I understand the environment and can more easily access data and understand context. The disadvantage is that I might have biases, especially if my own school is one of the cases.

### Round 10

**Socratic Mentor**:

A very honest self-assessment. You've raised a key research ethics issue: the role conflict of insider research.

[INSIGHT: The researcher's identity has a dual nature: insider advantage (easy data access, contextual understanding) vs insider bias (bias toward one's own institution). This must be explicitly addressed in the research design]

**[devils_advocate_agent triggered here — Checkpoint]**

My colleague added a challenge: if your own school gets classified as a "failed case," would you be able to publish? What would your president and colleagues think when they see it? This isn't just a research bias issue — it's a political sensitivity issue. How do you plan to handle this?

**User**:
Maybe I should not include my own school in the cases. Or use anonymization.

**Socratic Mentor**:

Both are viable strategies, but each has trade-offs. Excluding your own school means losing the case you know best; anonymization in Taiwan's small academic circle can be easily identified. You'll need to explicitly state your position and handling approach in the methodology.

And there's an even more fundamental question: if your research conclusion is "Strategy X is ineffective," but your own school is currently pursuing Strategy X — would you publish honestly?

**User**:
I think I should publish honestly. If the research has value, the truth should be told. But I know there will be political pressure.

---

## Layer 5: SIGNIFICANCE & CONTRIBUTION — Contribution and Significance

### Round 11

**Socratic Mentor**:

Your willingness to face this tension is admirable. These limitations and challenges don't need to make you give up the research, but they need to be transparently discussed in the paper.

[INSIGHT: Research ethics decision: publish honestly, transparently disclose the researcher's identity and potential conflicts of interest in the methodology, anonymize case institutions]

Now let's address the most fundamental question: if you complete this research, who would make different decisions as a result? In other words, why should readers care about your findings?

**User**:
I think it would be useful for other private technology university presidents and decision-makers. They can learn which strategies are worth investing in and which might be a waste of effort. It would also have reference value for MOE policy, such as whether the exit regulations are too one-size-fits-all.

### Round 12

**Socratic Mentor**:

You've identified two levels of contribution: the practical level (school decision-makers) and the policy level (MOE). This makes your research not just an academic exercise, but one with real applied value.

[INSIGHT: Research contribution at two levels: (1) practical level — providing private technology university decision-makers with an evidence base for strategy choices; (2) policy level — providing case comparison evidence for exit and transformation policies]

One last question: can you complete this sentence in one statement — "Before my research, people thought... but my research might show..."

**User**:
Before my research, people thought that the survival of private technology universities under declining birth rates depended mainly on enrollment strategies. But my research might show that the decisive factor is not just enrollment, but whether the school can find a new value proposition beyond enrollment.

**Socratic Mentor**:

This is a very powerful research positioning. You're not just describing a phenomenon — you're challenging a common assumption: "enrollment is everything." If you can support this argument with empirical cases, this will be an impactful study.

[INSIGHT: Core academic contribution: challenging the simplified narrative of "declining birth rates = enrollment problem," proposing that "value repositioning" is the key factor for private technology universities' sustainable operation]

---

## Research Plan Summary

Dialogue concluded. Below is the Research Plan Summary extracted from 12 rounds of dialogue.

---

### Research Question

**Core Question**: In the context of Taiwan's declining birth rates, among the transformation strategies of private technology universities, which strategies can achieve operational sustainability while maintaining educational quality? What are the key differentiating factors between successful and failed cases?

**Sub-questions**:
1. What different types of transformation strategies have private technology universities adopted?
2. What common characteristics do the strategies of technology universities that have maintained both operations and quality share?
3. To what extent do structural factors (geographic location, historical reputation, school size) influence strategy effectiveness?

### Methodology Direction

- **Research design**: Multiple case comparison study
- **Number of cases**: 4-6 private technology universities
- **Case selection**: Two-stage — first screen with objective indicators (enrollment rate changes, financial status), then pair (geographic location x school size)
- **Data collection**: Triangulation
  - In-depth administrator interviews
  - MOE public statistical data
  - School self-assessment report document analysis

### Evidence Strategy

- Cross-validate interviews with data to avoid single-source bias
- Paired design to control structural factors like geography and scale
- Clear "change the conclusion" condition: if strategy factors are not significant while structural factors are, adjust the conclusion direction rather than hiding findings

### Known Limitations

1. **Researcher identity**: Employed at a private technology university, insider bias risk exists. Handling: transparent disclosure in methodology, case anonymization
2. **Interview bias**: Administrators may overstate their strategies. Handling: triangulation
3. **Limited sample size**: 4-6 cases cannot support statistical inference. Positioned as: analytic generalization rather than statistical inference
4. **Subjectivity of "success" definition**: Quality indicators themselves are debatable. Handling: use multiple indicators, discuss in limitations section
5. **Political sensitivity**: Conclusions may affect the researcher's relationship with their institution

### Expected Contribution

- **Academic contribution**: Challenge the simplified narrative of "declining birth rates = enrollment problem," propose an analytical framework of "value repositioning"
- **Practical contribution**: Provide private technology university decision-makers with evidence-based strategy choice reference
- **Policy contribution**: Provide case comparison evidence for exit and transformation policies

### Complete INSIGHT List

1. [INSIGHT: The user's core concern is not just declining birth rates per se, but the "response strategies" of private universities under the pressure of declining birth rates]
2. [INSIGHT: Research question direction: Among the transformation strategies adopted by private universities in response to declining birth rates, what factors differentiate successful from failed cases]
3. [INSIGHT: The user's definition of "successful transformation" is a dual standard: (1) operational sustainability (financial viability) + (2) maintaining educational quality, not just enrollment numbers]
4. [INSIGHT: Candidate RQ direction confirmed: comparing successful and failed private university transformation strategies, focusing on the dual success criteria of quality maintenance + operational sustainability]
5. [INSIGHT: Research scope narrowed to Taiwan's private technology universities, due to the user's practical experience and the unique positioning of technology universities (reliance on industry-academia partnerships, vocational education system)]
6. [INSIGHT: Methodology choice: multiple case comparison method, 4-6 private technology universities, using objective indicators (enrollment rates, financials) for preliminary screening, then in-depth analysis of strategy differences]
7. [INSIGHT: Data collection strategy employs triangulation: (1) administrator interviews (subjective experience) + (2) MOE statistical data (objective indicators) + (3) self-assessment report document analysis, with all three cross-validating each other]
8. [INSIGHT: Important alternative hypothesis: Private technology universities' survival may depend more on structural factors (geographic location, historical reputation) than on active transformation strategies. This hypothesis doesn't make the research meaningless; rather, it would change the direction of policy recommendations]
9. [INSIGHT: Case selection uses paired design: geographic location and school size as pairing conditions to control the influence of structural factors]
10. [INSIGHT: The researcher's identity has a dual nature: insider advantage (easy data access, contextual understanding) vs insider bias (bias toward one's own institution). This must be explicitly addressed in the research design]
11. [INSIGHT: Research ethics decision: publish honestly, transparently disclose the researcher's identity and potential conflicts of interest in the methodology, anonymize case institutions]
12. [INSIGHT: Research contribution at two levels: (1) practical level — providing private technology university decision-makers with an evidence base for strategy choices; (2) policy level — providing case comparison evidence for exit and transformation policies]
13. [INSIGHT: Core academic contribution: challenging the simplified narrative of "declining birth rates = enrollment problem," proposing that "value repositioning" is the key factor for private technology universities' sustainable operation]

### Recommended Next Steps

- **Option A**: Use `deep-research` (full mode) for systematic literature search to understand existing research on private university transformation strategy classification and evaluation
- **Option B**: Use `academic-paper` (plan mode) to start planning the paper structure directly, using this Research Plan Summary as a foundation
- **Recommended path**: Option A → Option B (confirm the literature foundation first, then plan the paper)

The user can directly input: "Now help me do a comprehensive literature review based on this research plan" or "Help me write a paper based on this research plan"
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-examples-systematic-review-md"></a>

## SOURCE: skills/deep-research/examples/systematic_review.md

<!-- SOURCE-CONTENT-BEGIN bytes=7874 -->
# Example: Systematic Literature Review (lit-review mode)

## User Request
```
Literature review on the effectiveness of micro-credentials in professional development
```

**Mode**: `lit-review` (bibliography_agent + source_verification_agent + synthesis_agent)

## bibliography_agent Output

### Search Strategy

**Databases**: Scopus, Web of Science, ERIC, ProQuest Education
**Keywords**:
- Primary: "micro-credentials" OR "micro-certifications" OR "digital badges" OR "stackable credentials"
- Combined with: "professional development" OR "workforce development" OR "continuing education" OR "upskilling"
- Filters: 2018-2025, English, peer-reviewed + selected grey literature

**PRISMA Flow**:
```
Records identified: 1,243
├── Scopus: 412
├── Web of Science: 389
├── ERIC: 287
└── ProQuest: 155

Duplicates removed: 318
Records screened (title/abstract): 925
Records excluded: 791
  - Not about micro-credentials: 423
  - Not professional development context: 198
  - Opinion/editorial only: 102
  - Non-English: 68
Full-text articles assessed: 134
Full-text excluded: 96
  - Insufficient methodology description: 41
  - Focus on K-12 not HE/professional: 32
  - Duplicate dataset: 14
  - Unable to access full text: 9
Studies included in synthesis: 38
```

### Annotated Bibliography (Selected entries)

1. **Kato, S., Galan-Muros, V., & Weko, T. (2020). The emergence of alternative credentials. *OECD Education Working Papers*, No. 216. https://doi.org/10.1787/b741f39e-en**
   - Relevance: Comprehensive OECD policy analysis of alternative credentials ecosystem
   - Key Findings: Micro-credentials gaining traction across OECD but lack standardization; quality assurance is critical challenge
   - Methodology: Policy analysis with cross-country comparison
   - Quality: Level VII (policy report) but high institutional credibility

2. **Ralston, S. J. (2021). Higher education's micro-credentialing craze: A postdigital-Deweyan critique. *Postdigital Science and Education*, *3*(1), 83-101.**
   - Relevance: Critical perspective on micro-credential movement
   - Key Findings: Warns of commodification of learning; micro-credentials risk reducing education to narrow skills training
   - Quality: Level VII (philosophical/critical analysis)
   - Contribution: Important counterpoint to dominant positive narrative

3. **Wheelahan, L., & Moodie, G. (2021). Analysing micro-credentials in higher education: A Bernsteinian analysis. *Journal of Curriculum Studies*, *53*(2), 212-228.**
   - Relevance: Theoretical framework for understanding micro-credential design
   - Key Findings: Micro-credentials risk "segmentalist" approach to knowledge; need to be embedded in coherent curricula
   - Quality: Level VI (theoretical analysis with empirical illustration)

[... 35 more sources ...]

## source_verification_agent Output

### Source Quality Matrix

| Grade | Count | % |
|-------|-------|---|
| A | 5 | 13% |
| B | 14 | 37% |
| C | 12 | 32% |
| D | 6 | 16% |
| F | 1 | 3% |

**Flagged**:
- Source #22: Predatory journal indicator (rapid acceptance, no editorial board listed) -> Excluded
- Source #31: Author is CEO of micro-credential platform -> COI noted, included with caveat
- Sources #8, #15, #29: Pre-2020 data may not reflect post-pandemic acceleration -> Currency caveat

**Final included**: 37 sources (1 excluded for quality)

## synthesis_agent Output

### Literature Matrix (Condensed)

| Theme | Sources For | Sources Against | Contested | Strength |
|-------|-----------|----------------|-----------|----------|
| Employer recognition improving | 8 | 3 | 2 | Moderate |
| Learner completion rates high | 6 | 4 | 1 | Contested |
| QA frameworks inadequate | 12 | 1 | 0 | Strong |
| Equity benefits | 9 | 5 | 3 | Contested |
| Skills-job alignment | 11 | 2 | 1 | Moderate-Strong |

### Synthesis Narrative

**Theme 1: Quality Assurance Frameworks Are Lagging** (Strong evidence)
The strongest finding across the literature is that existing QA frameworks were not designed for micro-credentials. Twelve of 37 sources address this theme, with near-universal agreement that current accreditation models — designed for degree programs — do not map well onto short-form, competency-based credentials (Kato et al., 2020; Wheelahan & Moodie, 2021). The European approach through the European MOOC Consortium has made progress on a common framework (Witthaus et al., 2016), but adoption remains uneven. Several authors argue that without robust QA, the micro-credential ecosystem risks becoming a "Wild West" of unverified claims (Ralston, 2021).

**Theme 2: Skills-Job Alignment Shows Promise** (Moderate-Strong)
Evidence suggests micro-credentials improve skills-job matching, particularly in technology and healthcare sectors. Employer surveys consistently report higher satisfaction with candidates who hold relevant micro-credentials alongside degrees (Brown & Kurzweil, 2023). However, alignment depends heavily on industry involvement in credential design — credentials developed without employer input show weaker labor market outcomes (Weise, 2020).

**Theme 3: Equity Outcomes Are Contested** (Contested)
The literature is split on whether micro-credentials improve or worsen educational equity. Proponents cite lower cost, flexible scheduling, and targeted skills development as benefits for underserved populations (Fishman et al., 2023). Critics counter that micro-credentials may create a two-tier system where disadvantaged learners receive "credential fragments" while privileged learners pursue full degrees (Wheelahan & Moodie, 2021). The resolution appears context-dependent: when micro-credentials are stackable toward degrees, equity benefits are stronger; when they serve as standalone alternatives, stratification risks increase.

**Theme 4: Employer Recognition Is Growing but Uneven** (Moderate)
Employer recognition of micro-credentials has increased significantly since 2020, driven partly by pandemic-accelerated digital transformation. However, recognition varies dramatically by industry, region, and credential provider. Technology sector employers show highest acceptance (78% in recent surveys), while traditional sectors like law and finance remain skeptical (under 30%) (Digital Promise, 2024).

**Theme 5: Completion and Engagement Patterns Vary** (Contested)
Completion rates for micro-credential programs range from 25% to 85% depending on program design, support structures, and learner demographics. Self-paced online formats show lowest completion (25-40%), while cohort-based blended models achieve highest rates (70-85%). Importantly, several studies note that "completion" may not be the right metric — some learners achieve their goals by completing specific modules without finishing the full credential (Reich & Ruiperez-Valiente, 2019).

### Knowledge Gaps
1. **Longitudinal outcomes**: No studies tracking micro-credential holders beyond 3 years
2. **Non-English contexts**: 89% of studies from English-speaking countries
3. **Cost-effectiveness**: No rigorous cost-benefit analyses found
4. **Stacking behavior**: Limited evidence on how learners combine micro-credentials over time

### Contradictions
| Claim A | Claim B | Assessment |
|---------|---------|-----------|
| Micro-credentials democratize access (9 sources) | Micro-credentials widen digital divide (5 sources) | Context-dependent: depends on infrastructure, digital literacy, and cost |
| High completion rates (6 sources) | Low completion for disadvantaged learners (4 sources) | Population-dependent: completion varies significantly by demographic |

---

## Final Output
- Annotated bibliography: 37 sources in APA 7.0
- Literature matrix: 5 themes x 37 sources
- Synthesis narrative: ~3,200 words
- 4 knowledge gaps identified
- 2 major contradictions analyzed
- Evidence strength assessment per theme
<!-- SOURCE-CONTENT-END -->
