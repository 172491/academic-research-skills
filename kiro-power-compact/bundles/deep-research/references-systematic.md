<a id="source-skills-deep-research-references-cross-agent-quality-definitions-md"></a>

## SOURCE: skills/deep-research/references/cross_agent_quality_definitions.md

<!-- SOURCE-CONTENT-BEGIN bytes=1478 -->
# Cross-Agent Quality Alignment — Full Definitions

Unified definitions to prevent inconsistency across agents.

| Concept | Definition | Applies To |
|---------|-----------|------------|
| **Peer-reviewed** | Published in a journal with formal peer review process (editorial review alone does not qualify). Conference proceedings count only if explicitly peer-reviewed | bibliography_agent, source_verification_agent |
| **Currency Rule** | Default: published within 5 years. Override by domain: CS/AI = 3 years, History/Philosophy = 20 years, Law = depends on jurisdiction changes. Seminal works exempt regardless of age | bibliography_agent, ethics_review_agent |
| **CRITICAL severity** | IRON RULE: Issue that, if unresolved, would invalidate a core conclusion or constitute academic misconduct. Requires immediate resolution before pipeline can proceed | All agents |
| **Source Tier** | tier_1 = top-quartile peer-reviewed journal; tier_2 = other peer-reviewed; tier_3 = academic but not peer-reviewed; tier_4 = grey literature | bibliography_agent, source_verification_agent |
| **Minimum Source Count** | full = 15+, quick = 5-8, lit-review = 25+, systematic-review = all eligible (no limit), fact-check = 3+ per claim | bibliography_agent |
| **Verification Threshold** | 100% DOI check + 50% WebSearch spot-check | source_verification_agent, ethics_review_agent |

> **Cross-Skill Reference**: See `shared/handoff_schemas.md` for inter-stage data exchange formats.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-equator-reporting-guidelines-md"></a>

## SOURCE: skills/deep-research/references/equator_reporting_guidelines.md

<!-- SOURCE-CONTENT-BEGIN bytes=14319 -->
# EQUATOR Reporting Guidelines — Research Design and Reporting Guideline Mapping

## Purpose
Quick reference for EQUATOR Network (Enhancing the QUAlity and Transparency Of health Research) reporting guidelines. Assists the research_architect_agent in selecting the appropriate reporting checklist during the methodology design stage, and the report_compiler_agent in ensuring report completeness during the writing stage.

---

## 1. Research Design → Reporting Guideline Mapping Table

| Research Design | Primary Reporting Guideline | Applicable Scenario |
|----------|------------|---------|
| Systematic review / Meta-analysis | **PRISMA** | Literature review integrating multiple studies |
| Randomized controlled trial (RCT) | **CONSORT** | Intervention experiments with random assignment |
| Observational study (cohort, case-control, cross-sectional) | **STROBE** | Non-interventional quantitative observational research |
| Qualitative research | **COREQ** | Interviews, focus groups, observation |
| Quality improvement study | **SQUIRE** | Systematic quality improvement project reports |
| Diagnostic accuracy study | STARD | Diagnostic tool evaluation |
| Prognostic study | TRIPOD | Prediction model development and validation |
| Case report | CARE | Single or small number of in-depth case reports |
| Economic evaluation | CHEERS | Cost-effectiveness analysis |
| Mixed methods research | GRAMMS | Mixed qualitative-quantitative designs |
| Animal study | ARRIVE | Animal experiments |
| Network meta-analysis | PRISMA-NMA | Multiple comparison meta-analysis |
| Scoping review | PRISMA-ScR | Scoping review (less stringent than systematic review) |

---

## 2. PRISMA — Systematic Review Condensed Checklist

**Full Name**: Preferred Reporting Items for Systematic Reviews and Meta-Analyses
**Version**: PRISMA 2020 (latest)

### Core Reporting Items

| # | Item | Description | Necessity |
|---|------|------|--------|
| 1 | **Title** | Clearly identify as a systematic review (with or without meta-analysis) | Required |
| 2 | **Abstract** | Structured abstract (background, purpose, methods, results, conclusions) | Required |
| 3 | **Registration** | Registration number and platform (e.g., PROSPERO) | Strongly recommended |
| 4 | **Eligibility criteria** | Inclusion/exclusion criteria in PICOS or PEO format | Required |
| 5 | **Information sources** | Databases searched and dates | Required |
| 6 | **Search strategy** | Complete search strategy for at least one database | Required |
| 7 | **Selection process** | Screening process (number of reviewers, how disagreements were resolved) | Required |
| 8 | **Data extraction** | Data extraction methods | Required |
| 9 | **Risk of bias** | Risk of bias assessment tool and results | Required |
| 10 | **Synthesis methods** | Synthesis method (narrative / meta-analytic) | Required |
| 11 | **PRISMA flow diagram** | Literature screening flow diagram | Required |
| 12 | **Results** | Characteristics of each study, bias assessment, synthesis results | Required |
| 13 | **Discussion** | Certainty of evidence, limitations, relationship to existing knowledge | Required |
| 14 | **Funding** | Funding sources and conflicts of interest | Required |

### PRISMA Flow Diagram Template

```
Records identified (n = )
├── Database searching (n = )
└── Other sources (n = )
         ↓
Duplicates removed (n = )
         ↓
Records screened (n = )
├── Excluded (n = )
         ↓
Reports sought for retrieval (n = )
├── Not retrieved (n = )
         ↓
Reports assessed for eligibility (n = )
├── Excluded, with reasons (n = )
│   ├── Reason 1 (n = )
│   ├── Reason 2 (n = )
│   └── Reason 3 (n = )
         ↓
Studies included in review (n = )
├── In qualitative synthesis (n = )
└── In quantitative synthesis (meta-analysis) (n = )
```

---

## 3. CONSORT — Randomized Controlled Trial Condensed Checklist

**Full Name**: Consolidated Standards of Reporting Trials
**Version**: CONSORT 2010 + extensions

### Core Reporting Items

| # | Item | Description |
|---|------|------|
| 1 | **Title & Abstract** | Identify as RCT; structured abstract |
| 2 | **Background** | Scientific background and trial rationale |
| 3 | **Objectives** | Specific objectives or hypotheses |
| 4 | **Trial design** | Design type (parallel, crossover, factorial, etc.) and allocation ratio |
| 5 | **Participants** | Eligibility criteria, settings, data collection locations |
| 6 | **Interventions** | Specific description of each group's intervention (including how and when administered) |
| 7 | **Outcomes** | Primary and secondary outcome measures, including definitions and time points |
| 8 | **Sample size** | Sample size calculation method (power analysis) |
| 9 | **Randomisation** | Random sequence generation method, allocation concealment mechanism |
| 10 | **Blinding** | Blinding implementation (who was blinded, how it was implemented) |
| 11 | **Statistical methods** | Statistical analysis methods, ITT/PP analysis |
| 12 | **Flow diagram** | Participant flow diagram (recruitment → allocation → follow-up → analysis) |
| 13 | **Results** | Results per group, effect sizes and precision (CI) |
| 14 | **Harms** | Adverse events or side effects |
| 15 | **Limitations** | Sources of bias, imprecision, multiple comparisons |
| 16 | **Registration** | Trial registration number |

### Higher Education Research Application Notes

RCTs in the education field (e.g., comparing teaching methods) commonly face:
- Inability to fully randomize (cluster randomization is more common)
- Difficulty implementing blinding (teachers/students know their group)
- Recommended to use **CONSORT-SPI** (Social and Psychological Interventions extension)

---

## 4. STROBE — Observational Study Condensed Checklist

**Full Name**: Strengthening the Reporting of Observational Studies in Epidemiology
**Applicable to**: Cohort studies, case-control studies, cross-sectional studies

### Core Reporting Items

| # | Item | Description |
|---|------|------|
| 1 | **Title & Abstract** | Indicate the study design type |
| 2 | **Background** | Scientific background, study rationale |
| 3 | **Objectives** | Specific objectives, pre-specified hypotheses |
| 4 | **Study design** | Clearly state the study design (cohort / case-control / cross-sectional) |
| 5 | **Setting** | Setting, location, relevant dates (recruitment, exposure, follow-up) |
| 6 | **Participants** | Eligibility criteria, data sources, sampling method |
| 7 | **Variables** | Outcome variables, exposure variables, potential confounders, effect modifiers |
| 8 | **Data sources** | Data sources and measurement methods for each variable |
| 9 | **Bias** | Methods for addressing potential sources of bias |
| 10 | **Study size** | How the sample size was determined |
| 11 | **Statistical methods** | Statistical methods (including confounder handling, missing data handling) |
| 12 | **Results** | Descriptive statistics, main results (including effect sizes, CI, p-value) |
| 13 | **Discussion** | Key findings, limitations, generalizability, consistency with other studies |
| 14 | **Funding** | Funding sources |

### Higher Education Research Application Notes

Common observational studies in higher education:
- Student learning outcome cross-sectional survey → cross-sectional STROBE
- Graduate employment tracking → cohort STROBE
- Dropout risk factor analysis → case-control STROBE

---

## 5. COREQ — Qualitative Research Condensed Checklist

**Full Name**: Consolidated Criteria for Reporting Qualitative Research
**Applicable to**: Interviews, focus groups

### Core Reporting Items (32 items, across 3 domains)

#### Domain 1: Research Team and Reflexivity

| # | Item | Description |
|---|------|------|
| 1 | **Interviewer/facilitator** | Who conducted the interviews or facilitated focus groups |
| 2 | **Credentials** | Researcher qualifications |
| 3 | **Occupation** | Researcher's professional identity |
| 4 | **Gender** | Researcher gender |
| 5 | **Experience & training** | Qualitative research experience and training |
| 6 | **Relationship with participants** | Researcher's relationship with participants |
| 7 | **Participant knowledge** | Participants' level of knowledge about the research |

#### Domain 2: Study Design

| # | Item | Description |
|---|------|------|
| 8 | **Methodological orientation** | Theoretical framework (e.g., grounded theory, phenomenology) |
| 9 | **Sampling** | Sampling strategy and method |
| 10 | **Method of approach** | How participants were contacted |
| 11 | **Sample size** | Number of participants |
| 12 | **Non-participation** | Number and reasons for refusal to participate |
| 13 | **Setting** | Interview location |
| 14 | **Presence of non-participants** | Whether non-participants were present during interviews |
| 15 | **Description of sample** | Participant demographics |
| 16 | **Interview guide** | Whether an interview guide was used and whether it was pilot-tested |
| 17 | **Repeat interviews** | Whether repeat interviews were conducted |
| 18 | **Audio/visual recording** | Whether audio/video was recorded |
| 19 | **Field notes** | Whether field notes were taken |
| 20 | **Duration** | Interview duration |
| 21 | **Data saturation** | Whether data saturation was discussed |
| 22 | **Transcripts returned** | Whether transcripts were returned to participants for feedback |

#### Domain 3: Analysis and Findings

| # | Item | Description |
|---|------|------|
| 23 | **Data analysis** | Analysis method (e.g., thematic analysis, IPA) |
| 24 | **Software** | Analysis software used |
| 25 | **Participant checking** | Whether participants confirmed the findings |
| 26 | **Quotations** | Whether quotations are presented to support themes |
| 27 | **Data and findings consistency** | Consistency between data and findings |
| 28 | **Clarity of major themes** | Whether major themes are clearly presented |
| 29 | **Clarity of minor themes** | Whether minor themes are clearly presented |

---

## 6. SQUIRE — Quality Improvement Study Condensed Checklist

**Full Name**: Standards for QUality Improvement Reporting Excellence
**Version**: SQUIRE 2.0
**Applicable to**: Quality improvement projects, systematic quality improvement, higher education quality assurance (QA) research

### Core Reporting Items

| # | Item | Description |
|---|------|------|
| 1 | **Title** | Identify as a quality improvement study |
| 2 | **Abstract** | Structured abstract |
| 3 | **Problem description** | Nature and severity of the quality problem |
| 4 | **Available knowledge** | Known relevant evidence |
| 5 | **Rationale** | Theoretical basis for the improvement initiative |
| 6 | **Specific aims** | Specific improvement goals (quantifiable) |
| 7 | **Context** | Environmental context of the improvement |
| 8 | **Intervention(s)** | Specific description of improvement measures |
| 9 | **Study of the intervention(s)** | How the improvement effectiveness was evaluated |
| 10 | **Measures** | Outcome measures, process measures, balancing measures |
| 11 | **Analysis** | Quantitative/qualitative analysis methods |
| 12 | **Ethical considerations** | Ethics review (if applicable) |
| 13 | **Results** | Improvement results (including time series data) |
| 14 | **Discussion** | Key findings, relationship to context, generalizability |
| 15 | **Limitations** | Study limitations |

### Particularly Applicable for Higher Education QA Research

SQUIRE is especially valuable as a reference for the following HE quality assurance research:
- **Teaching quality improvement**: Introduction and evaluation of new teaching strategies
- **Curriculum reform**: Tracking the effects of curriculum redesign
- **Student support service improvement**: Systematic improvement of tutoring, counseling, and learning support
- **HEEACT accreditation self-improvement**: Improvement actions and tracking in response to accreditation findings
- **Institutional research (IR)-driven improvement**: Data-based decision-making and improvement cycles

---

## 7. Higher Education Research Context Recommendations

### Commonly Used Guidelines Ranking

| Rank | Guideline | Common HE Usage Scenario |
|------|------|----------------|
| 1 | **PRISMA** | Systematic review of education policy, teaching strategy meta-analysis |
| 2 | **COREQ** | Teacher/student experience interviews, focus groups |
| 3 | **STROBE** | Student surveys, institutional data analysis |
| 4 | **SQUIRE** | Teaching quality improvement, QA accreditation |
| 5 | **CONSORT** | Teaching intervention experiments (less common but high impact) |

### Research Design Quick Selection

```
What is your research type?
│
├── Integrating existing research → PRISMA
│   ├── Systematic review → PRISMA 2020
│   ├── Scoping review → PRISMA-ScR
│   └── Meta-analysis → PRISMA + MOOSE
│
├── Intervention experiment → CONSORT
│   ├── Individual randomization → CONSORT 2010
│   ├── Class/school randomization → CONSORT-Cluster
│   └── Social/psychological intervention → CONSORT-SPI
│
├── Observational survey → STROBE
│   ├── Cross-sectional survey → STROBE-CS
│   ├── Follow-up study → STROBE-Cohort
│   └── Retrospective comparison → STROBE-CC
│
├── Qualitative research → COREQ
│   ├── Interviews → COREQ
│   ├── Focus groups → COREQ
│   └── Ethnography → SRQR (alternative)
│
└── Quality improvement → SQUIRE
    ├── PDSA cycle → SQUIRE 2.0
    └── QA/accreditation improvement → SQUIRE 2.0
```

---

## Quick Reference: 3 Steps to Choosing a Reporting Guideline

1. **Identify your research design**: What type of research design is your study?
2. **Check the mapping table**: Find the corresponding reporting guideline
3. **Download the checklist**: Go to [EQUATOR Network](https://www.equator-network.org/) and download the full checklist

> Reminder: Reporting guidelines represent the minimum standard, not the quality ceiling. Meeting the checklist doesn't guarantee high research quality, but failing to meet the checklist typically indicates deficiencies in reporting quality.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-literature-monitoring-strategies-md"></a>

## SOURCE: skills/deep-research/references/literature_monitoring_strategies.md

<!-- SOURCE-CONTENT-BEGIN bytes=10792 -->
# Literature Monitoring Strategies — Reference Guide

## Purpose

Comprehensive reference for setting up post-research literature monitoring across major academic databases and platforms. Used by the `monitoring_agent` to configure monitoring strategies tailored to the user's research field and publication velocity.

---

## 1. Google Scholar Alerts

### Setup

1. Go to [Google Scholar](https://scholar.google.com)
2. Enter your search query (use the same keywords from your systematic search)
3. Click the envelope icon (📧) in the left sidebar, or go to scholar.google.com/scholar_alerts
4. Set email address and frequency

### Best Practices

- Create separate alerts for each major keyword cluster (not one giant query)
- Use quotes for exact phrases: `"quality assurance" "higher education"`
- Use OR for synonyms: `"quality assurance" OR "quality evaluation"`
- Limit to 10-15 active alerts to avoid email overload
- Review alerts monthly and deactivate stale ones

### Limitations

- No Boolean NOT support in alerts
- Cannot filter by date, journal, or document type
- May include non-peer-reviewed sources (theses, reports, patents)
- Coverage varies by discipline (strong in STEM, weaker in humanities)

---

## 2. PubMed Email Alerts

### Setup

1. Go to [PubMed](https://pubmed.ncbi.nlm.nih.gov)
2. Run your search using MeSH terms and filters
3. Click "Save" below the search box
4. Log in to My NCBI account (free)
5. Set email alert frequency: daily, weekly, or monthly

### Best Practices

- Use MeSH terms for precise matching (e.g., `"Quality Assurance, Health Care"[MeSH]`)
- Combine with free-text search for newer terms not yet in MeSH
- Set weekly frequency for active research areas, monthly for stable fields
- Use the "Sort by: Most Recent" option to prioritize new publications
- Save your search strategy for reproducibility

### Advanced Features

- **MyNCBI Collections**: Organize saved articles into folders
- **Filters**: Limit by date, article type, language, species
- **RSS feed**: Available for any saved search (click RSS icon)

### Limitations

- Biomedical focus — limited coverage of social sciences, education, humanities
- Indexing lag: 1-4 weeks for new articles to appear
- No citation tracking built in

---

## 3. RSS Feeds for Major Databases

### What is RSS?

RSS (Really Simple Syndication) allows you to subscribe to content updates from websites without checking each site manually. Use an RSS reader (e.g., Feedly, Inoreader, NewsBlur) to aggregate feeds.

### Recommended Feeds

| Source | Feed URL Pattern | Content |
|--------|-----------------|---------|
| **PubMed** | Saved search → RSS icon | New articles matching your search |
| **arXiv** | `arxiv.org/rss/[category]` (e.g., `cs.AI`, `cs.CL`) | Preprints by category |
| **bioRxiv** | `connect.biorxiv.org/biorxiv_xml.php?subject=[subject]` | Biology preprints |
| **medRxiv** | `connect.medrxiv.org/medrxiv_xml.php?subject=[subject]` | Medical preprints |
| **SSRN** | Subscribe to specific research networks | Social science preprints |
| **Journal TOC** | Most journals offer RSS on their homepage | New issues of specific journals |
| **Retraction Watch** | `retractionwatch.com/feed/` | Retraction news and updates |

### RSS Reader Recommendations

| Reader | Platform | Cost | Best For |
|--------|----------|------|----------|
| **Feedly** | Web, iOS, Android | Free (basic) / $6/mo (Pro) | Organized categorization, AI features |
| **Inoreader** | Web, iOS, Android | Free (basic) / $5/mo (Pro) | Power users, rules/filters |
| **NewsBlur** | Web, iOS, Android | Free (limited) / $36/yr | Open source option |
| **Zotero RSS** | Desktop | Free | Integrates with reference manager |

---

## 4. Retraction Watch Integration

### Retraction Watch Database

- **URL**: [retractiondatabase.org](http://retractiondatabase.org)
- **Coverage**: 40,000+ retracted or corrected papers
- **Searchable by**: author, journal, subject, reason, date

### Monitoring Workflow

1. **Baseline check**: Search all cited authors and paper titles in the Retraction Watch Database
2. **Ongoing monitoring**: Subscribe to Retraction Watch blog RSS feed
3. **Periodic re-check**: Every 3-6 months, re-run the baseline check for cited sources

### Retraction Reasons to Watch For

| Reason | Severity | Action Required |
|--------|----------|-----------------|
| Data fabrication/falsification | Critical | Remove citation; add note explaining removal |
| Plagiarism | High | Replace with original source |
| Duplicate publication | Moderate | Keep the primary publication; remove duplicate |
| Honest error | Moderate | Check whether the error affects cited findings |
| Author dispute | Low | Usually no impact on findings |
| Publisher error | Low | Update citation to corrected version |

---

## 5. Preprint Server Monitoring

### arXiv

- **Coverage**: Physics, mathematics, computer science, statistics, quantitative biology, economics
- **Monitoring**: Subscribe to RSS feeds by category and cross-list
- **Alert service**: [arxiv-sanity](http://arxiv-sanity-lite.com/) for AI-curated recommendations
- **Update frequency**: Daily (new submissions posted ~8 PM ET)

### SSRN

- **Coverage**: Social sciences, humanities, law, economics, management
- **Monitoring**: Subscribe to eJournal alerts by research network
- **Alert service**: Email notifications for new papers in subscribed networks
- **Note**: Now owned by Elsevier; some content behind paywall

### bioRxiv / medRxiv

- **Coverage**: Biology (bioRxiv) and health sciences (medRxiv)
- **Monitoring**: RSS feeds by subject area
- **Alert service**: Email alerts for specific keywords
- **Note**: Preprints are NOT peer-reviewed — flag accordingly in digests

### Key Preprint Monitoring Rules

1. Always label preprint sources clearly: `[PREPRINT — not peer-reviewed]`
2. Check whether a preprint has been published in a peer-reviewed journal (look for "Now published in..." banner)
3. Preprints can change or be withdrawn — re-check before citing
4. Preprint findings may differ from the final published version

---

## 6. Citation Tracking

### Web of Science

1. Find your key cited papers in Web of Science
2. Click "Create Citation Alert" (requires institutional access)
3. Receive email when someone cites that paper
4. Use "Cited Reference Search" for older papers not in the database

### Scopus

1. Find your key cited papers in Scopus
2. Click "Set Citation Alert" on the document page
3. Configure email frequency
4. Also available: author alerts (track all publications by an author)

### Google Scholar

1. Find the paper on Google Scholar
2. Click "Cited by N" to see citing papers
3. Click the "Follow" button (envelope icon) on author profiles
4. Set up alerts for specific papers by quoting the exact title

### Semantic Scholar

- **URL**: [semanticscholar.org](https://www.semanticscholar.org)
- **Alerts**: Click "Alert" on any paper to track citations
- **Advantage**: AI-powered relevance ranking of citing papers
- **Research feed**: Personalized recommendations based on your library

---

## 7. Recommended Monitoring Cadence by Field

### Determining Your Field's Publication Velocity

| Indicator | High Velocity | Moderate | Low |
|-----------|--------------|----------|-----|
| Papers per month (in your niche) | > 50 | 10-50 | < 10 |
| Median time from submission to publication | < 6 months | 6-12 months | > 12 months |
| Preprint prevalence | > 50% of key papers | 10-50% | < 10% |
| Conference vs. journal dominance | Conference-first | Mixed | Journal-only |

### Cadence Recommendations

| Field | Check Frequency | Digest Period | Sunset |
|-------|----------------|---------------|--------|
| **AI/ML, NLP** | Daily (arXiv) + Weekly (journals) | Weekly | 6 months |
| **Biomedical, Clinical** | Weekly (PubMed + preprints) | Biweekly | 12 months |
| **Education Technology** | Biweekly | Monthly | 12 months |
| **Higher Education Policy** | Monthly | Quarterly | 18 months |
| **Social Sciences (general)** | Monthly | Quarterly | 18 months |
| **Law, Philosophy** | Quarterly | Semi-annually | 24 months |
| **History, Classics** | Semi-annually | Annually | 36 months |

### Sunset Policy

- **Sunset date**: The date after which active monitoring stops (topic presumed stable)
- Set based on field velocity and research currency
- After sunset: switch to annual check-ins or opportunistic monitoring
- Exception: extend monitoring if a major development occurs (e.g., retraction of key source, paradigm shift)

---

## 8. Monitoring Maintenance Checklist

Run this checklist every monitoring cycle:

- [ ] Are all alerts still active? (some platforms deactivate after inactivity)
- [ ] Are any alerts returning zero results? (keywords may need updating)
- [ ] Are any alerts returning too many results? (keywords may need narrowing)
- [ ] Has the field's terminology evolved? (add new keywords, retire old ones)
- [ ] Any new major databases or preprint servers for this field?
- [ ] Has any tracked author changed institutions? (update author tracking)
- [ ] Is the sunset date still appropriate?
- [ ] Have you checked the Retraction Watch Database recently?

---

## Quick Reference: Setting Up in 30 Minutes

1. **Google Scholar** (5 min): Create 3-5 keyword alerts matching your original search strategy
2. **PubMed** (5 min): Save your search and set weekly email alerts (if your field is indexed)
3. **RSS** (5 min): Subscribe to RSS feeds for your top 5 cited journals in Feedly or Inoreader
4. **Retraction Watch** (5 min): Run baseline check on all cited authors; subscribe to RSS feed
5. **Citation tracking** (5 min): Set up citation alerts for your 5 most-cited sources in Google Scholar or Scopus
6. **Preprints** (5 min): Subscribe to relevant arXiv/SSRN/bioRxiv categories if applicable to your field

---

## SKILL.md Extracted Content: Literature Monitoring (Optional Post-Pipeline)

After any research mode is complete, users can optionally activate the `monitoring_agent` to set up post-research literature monitoring. This is not part of the main pipeline — it is an auxiliary capability triggered on demand.

See `agents/monitoring_agent.md` for the detailed agent definition.

**Trigger**: "monitor this topic", "set up alerts", "track new publications on this"

**Capabilities**:
- Weekly/monthly monitoring digest generation
- Retraction alerts for cited sources
- Contradictory findings detection
- Key author tracking
- Keyword evolution tracking

**Input**: Completed bibliography + search strategy from any research mode
**Output**: Monitoring configuration + digest template (markdown)

**Limitation**: The monitoring agent produces configurations and templates for the user to act on. It cannot run autonomous background monitoring.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-methodology-patterns-md"></a>

## SOURCE: skills/deep-research/references/methodology_patterns.md

<!-- SOURCE-CONTENT-BEGIN bytes=17382 -->
# Research Methodology Patterns — Design Templates

## Purpose
Ready-to-use methodology templates for common research designs. Used by the research_architect_agent.

## Pattern 1: Systematic Literature Review

### When to Use
- Mapping the state of knowledge on a topic
- Identifying gaps in existing research
- Synthesizing evidence for policy/practice recommendations

### Design Template
```
Research Question: What is known about [topic] in [context]?

Protocol:
1. Register protocol (PROSPERO or similar)
2. Define search strategy (databases, keywords, Boolean operators)
3. Establish inclusion/exclusion criteria
4. Search execution + documentation
5. Two-pass screening (title/abstract → full text)
6. Quality appraisal of included studies
7. Data extraction
8. Synthesis (narrative, thematic, or meta-analytic)
9. Report per PRISMA guidelines

Quality Criteria:
- Comprehensive search (minimum 3 databases)
- Reproducible strategy
- Dual screening (2 reviewers or reviewer + verification)
- PRISMA checklist completed

Reporting Standard: PRISMA 2020 (see references/equator_reporting_guidelines.md)
```

### PRISMA Flow Template
```
Records identified through database searching (n = )
Additional records from other sources (n = )
         ↓
Records after duplicates removed (n = )
         ↓
Records screened (title/abstract) (n = )
Records excluded (n = )
         ↓
Full-text articles assessed for eligibility (n = )
Full-text excluded, with reasons (n = )
         ↓
Studies included in synthesis (n = )
```

## Pattern 2: Comparative Case Study

### When to Use
- Comparing policies, programs, or institutions
- Understanding how context shapes outcomes
- Generating theoretical propositions from multiple cases

### Design Template
```
Research Question: How does [phenomenon] vary across [cases]?

Protocol:
1. Case selection (theoretical or purposive sampling)
2. Define comparison framework (dimensions, variables)
3. Data collection per case (documents, interviews, data)
4. Within-case analysis
5. Cross-case analysis
6. Pattern identification and explanation

Quality Criteria:
- Explicit case selection rationale
- Consistent data collection across cases
- Both within-case and cross-case analysis
- Rival explanations considered
```

### Comparison Matrix Template
```
| Dimension | Case A | Case B | Case C | Pattern |
|-----------|--------|--------|--------|---------|
| Context   |        |        |        |         |
| Input     |        |        |        |         |
| Process   |        |        |        |         |
| Outcome   |        |        |        |         |
```

## Pattern 3: Policy Analysis

### When to Use
- Evaluating existing or proposed policies
- Comparing policy approaches across jurisdictions
- Assessing policy outcomes and unintended consequences

### Design Template
```
Research Question: How effective is [policy] in achieving [goal]?

Framework Options:
A. Bardach's Eightfold Path
B. Dunn's Policy Analysis Framework
C. SWOT Analysis
D. Logic Model (Input → Activity → Output → Outcome → Impact)

Protocol:
1. Problem definition
2. Evidence gathering (quantitative + qualitative)
3. Policy option identification
4. Criteria development (effectiveness, efficiency, equity, feasibility)
5. Option assessment against criteria
6. Recommendation with trade-offs

Quality Criteria:
- Multiple criteria (not just effectiveness)
- Stakeholder perspectives included
- Unintended consequences assessed
- Implementation feasibility addressed
```

## Pattern 4: Mixed Methods (Convergent Parallel)

### When to Use
- Complex phenomena requiring multiple data types
- Need to triangulate findings
- Quantitative data needs qualitative explanation (or vice versa)

### Design Template
```
Research Question: What is the nature and extent of [phenomenon]?

Protocol:
QUAN strand:                    QUAL strand:
1. Survey/data collection       1. Interviews/focus groups
2. Statistical analysis         2. Thematic analysis
3. Quantitative findings        3. Qualitative findings
                    ↓
            4. Integration
            5. Joint display
            6. Meta-inference

Quality Criteria:
- Both strands have independent rigor
- Integration strategy explicit (not just parallel reporting)
- Joint display or mixed methods matrix
- Meta-inferences draw on both strands

Reporting Standards: QUAL strand → COREQ; QUAN strand → STROBE/CONSORT (see references/equator_reporting_guidelines.md)
```

## Pattern 5: Content/Document Analysis

### When to Use
- Analyzing texts, policies, media, or documents
- Identifying patterns in communication
- Systematic examination of large document sets

### Design Template
```
Research Question: What themes/patterns emerge from [document set]?

Protocol:
1. Define corpus (which documents, inclusion criteria)
2. Develop coding framework (deductive, inductive, or hybrid)
3. Code systematically (inter-coder reliability if multiple coders)
4. Analyze codes → categories → themes
5. Report with exemplar quotes/excerpts

Quality Criteria:
- Corpus selection transparent
- Coding framework documented
- Inter-coder reliability reported (if applicable)
- Saturation discussed
```

## Pattern 6: Exploratory Research

### When to Use
- New or under-researched topics
- Generating hypotheses for future research
- Understanding phenomena from participant perspective

### Design Template
```
Research Question: How do [participants] experience/understand [phenomenon]?

Protocol:
1. Purposive sampling
2. Semi-structured interviews or observations
3. Iterative data collection and analysis
4. Open coding → axial coding → selective coding
5. Theory or framework development
6. Member checking / peer debriefing

Quality Criteria:
- Reflexivity statement
- Thick description
- Data saturation discussed
- Transferability criteria addressed

Reporting Standard: COREQ for interviews/focus groups (see references/equator_reporting_guidelines.md)
```

## Pattern 7: Benchmarking Study

### When to Use
- Comparing performance against standards or peers
- Identifying best practices
- Setting performance targets

### Design Template
```
Research Question: How does [entity] perform compared to [benchmark]?

Protocol:
1. Select benchmarking type (internal, competitive, functional, generic)
2. Identify indicators and metrics
3. Collect comparable data
4. Analyze gaps
5. Identify best practices from high performers
6. Develop improvement recommendations

Quality Criteria:
- Comparable metrics (apples to apples)
- Context factors acknowledged
- Multiple indicators (not single metric)
- Actionable recommendations
```

## Pattern 8: Technology Requirements Analysis

### When to Use
- Assessing feasibility, requirements analysis, and technology comparison for new technologies
- Technology selection decisions before system design
- Risk and benefit assessment of technology adoption
- When research questions involve "Which technology should be used?" or "Can this technology solve the problem?"

### Design Template
```
Research Question: What technology approach best addresses [need] given [constraints]?

Protocol:
1. Requirement Elicitation
   - Stakeholder interviews
   - Existing system/process analysis
   - Functional requirements vs non-functional requirements (performance, security, scalability)
2. Technology Scanning
   - Inventory of candidate technologies (at least 3 options)
   - Technology Readiness Level (TRL) assessment
   - Community activity, documentation completeness, long-term maintenance risk
3. Feasibility Assessment
   - Technical feasibility: Can it be done?
   - Economic feasibility: Is it worth doing?
   - Organizational feasibility: Does the team have the capability?
   - Schedule feasibility: Is there enough time?
4. Proof of Concept (PoC)
   - Construct minimal verification targeting key technical risks
   - Define success criteria (performance thresholds, integration test pass rates)
   - Document encountered problems and solutions
5. Requirement Specification
   - Produce formal requirements document
   - Define acceptance criteria
   - Establish traceability matrix (requirements ↔ design ↔ testing)

Quality Criteria:
- Requirements completeness: All stakeholder requirements have been collected
- Traceability: Each requirement is traceable to its source; each design decision maps to a corresponding requirement
- Technical feasibility verification: Key technical risks have been validated through PoC
- Fair comparison of options: Consistent evaluation framework used to compare different technology options
```

### Technology Comparison Matrix Template
```
| Evaluation Dimension | Option A | Option B | Option C | Weight |
|---------------------|----------|----------|----------|--------|
| Functional Fit      |          |          |          | 30%    |
| Technology Maturity  |          |          |          | 20%    |
| Adoption Cost        |          |          |          | 15%    |
| Maintenance Cost     |          |          |          | 10%    |
| Learning Curve       |          |          |          | 10%    |
| Scalability          |          |          |          | 10%    |
| Community/Ecosystem  |          |          |          | 5%     |
| Weighted Total       |          |          |          | 100%   |
```

## Pattern 9: Legal Case Analysis

### When to Use
- Legal and regulatory policy analysis, case law research, legal text interpretation
- Analyzing current regulations and judicial opinions on specific legal issues
- Comparing legal approaches across different jurisdictions
- When research questions involve statutory interpretation, rights and obligations analysis, or legal aspects of policy analysis

### Distinction from Pattern 3 (Policy Analysis)
- **Policy Analysis**: Focuses on evaluating policy effectiveness — "Is this policy working?" "Are there better policy options?"
- **Legal Case Analysis**: Focuses on analyzing legal texts and case law — "What does the law say?" "How do courts interpret it?" "Are there legal loopholes?"

### Design Template
```
Research Question: How does the law address [issue] and what are the implications for [context]?

Protocol:
1. Issue Identification
   - Translate research question into specific legal issues
   - Distinguish questions of fact vs questions of law
   - Define the relevant legal domains (public law / private law / international law)
2. Legal Framework Mapping
   - Constitutional-level provisions
   - Statutory / regulatory / administrative rule levels
   - International conventions / soft law
   - Legislative history and rationale for amendments
3. Case Law Analysis
   - Systematic case law search (court level, time range, keywords)
   - Extract key holdings from decisions
   - Analyze trends in case law evolution
   - Identify majority opinions vs dissenting opinions
4. Legal Reasoning
   - Textual interpretation, systematic interpretation, purposive interpretation, historical interpretation
   - Comparative law analysis (how other jurisdictions handle the issue)
   - Review and evaluate scholarly opinions
   - Interest balancing and value judgments
5. Recommendations
   - Interpretive recommendations under existing law
   - Legislative reform recommendations (if necessary)
   - Practical implementation recommendations
   - Risk warnings

Quality Criteria:
- Legal source accuracy: Cited regulations and cases must be current and effective versions
- Logical consistency: Legal reasoning process must not be self-contradictory
- Argumentation completeness: All possible interpretive paths have been considered
- Comparative law rigor: When comparing jurisdictions, differences in legal system backgrounds must be noted
```

### Legal Analysis Structure Template
```
I. Legal Issues
   [Specific legal issues in dispute]

II. Relevant Provisions
   1. Statutory level:
   2. Regulatory level:
   3. International norms:

III. Judicial Opinions
   1. Majority opinion: [Case number] [Key holding]
   2. Dissenting opinion: [Case number] [Key holding]
   3. Trends:

IV. Scholarly Opinions
   1. View A:
   2. View B:
   3. Author's view:

V. Comparative Law
   [How other jurisdictions handle the issue]

VI. Conclusions and Recommendations
```

## Pattern 10: Creative/Practice-Based Research

### When to Use
- Art-based research: Generating knowledge through artistic creation
- Design research / research through design: Generating knowledge through the design process
- Practice-based / practice-led research: Practice itself is the research method
- When research questions involve creative practice, design thinking, or artistic inquiry

### Differences from Traditional Academic Research
- **Output format**: Can be a creative work + dissertation (not just a dissertation)
- **Knowledge type**: Values practical knowledge (tacit knowledge) and embodied knowledge
- **Process as method**: The creative/design process itself is the research method, not merely the object of study
- **Subjectivity**: The researcher's subjective experience is a legitimate source of knowledge, but requires systematic reflection

### Design Template
```
Research Question: What knowledge emerges through the practice of [creative activity] in [context]?

Protocol:
1. Reflective Practice
   - Define research question and creative intention
   - Establish reflective framework (e.g., Schön's reflection-in-action / reflection-on-action)
   - Confirm researcher positioning (insider / practitioner-researcher)
2. Process Documentation
   - Studio journal / design diary
   - Process video/audio documentation
   - Iteration version records (sketches, drafts, prototypes)
   - Decision point documentation: Why this approach and not another?
3. Contextual Analysis
   - Situate the creative process within disciplinary/cultural/historical context
   - Engage in dialogue with existing works/theories
   - Identify themes and insights emerging from the creative process
4. Knowledge Articulation
   - Transform tacit knowledge into communicable forms
   - Build bridges from practice to concepts
   - Distill transferable principles or frameworks
5. Presentation of Findings
   - Work presentation (exhibition, performance, prototype demonstration)
   - Written discourse (exegesis / critical commentary)
   - Integrate the relationship between work and discourse

Quality Criteria:
- Depth of reflection: Not just describing "what was done," but analyzing "why it was done this way" and "what was learned"
- Creative process transparency: Readers can understand the complete path from problem to work
- Clarity of knowledge contribution: Clearly state what this research contributes to knowledge
- Contextualization quality: The work does not exist in isolation but engages with the discipline
- Methodological reflexivity: The researcher is aware of their own role and biases
```

### Practice-Based Research Documentation Template
```
Phase 1: Positioning
- Research question:
- Creative intention:
- Researcher positioning (practitioner / observer / participant):
- Theoretical framework:

Phase 2: Process
| Iteration | Date | Action | Reflection | Turning Point |
|-----------|------|--------|------------|---------------|
| v1        |      |        |            |               |
| v2        |      |        |            |               |
| v3        |      |        |            |               |

Phase 3: Outcomes
- Work description:
- Knowledge contribution:
- Transferable principles/frameworks:
- Recommendations for future practice/research:
```

## Choosing the Right Pattern

```
What type of question?
├── "What is known?" → Systematic Literature Review
├── "How do cases compare?" → Comparative Case Study
├── "Is this policy working?" → Policy Analysis
├── "What's happening and why?" → Mixed Methods
├── "What do documents reveal?" → Content Analysis
├── "How is this experienced?" → Exploratory Research
├── "How do we compare?" → Benchmarking Study
├── "Which technology should we use?" → Technology Requirements Analysis
├── "What does the law say?" → Legal Case Analysis
└── "What knowledge emerges from practice?" → Creative/Practice-Based Research

More nuanced decision:
├── Technology assessment related
│   ├── Comparing different technology options → Pattern 8 (Technology Requirements Analysis)
│   └── Comparing technology adoption across organizations → Pattern 2 (Comparative Case Study)
├── Law/policy related
│   ├── What legal texts prescribe and how courts interpret them → Pattern 9 (Legal Case Analysis)
│   └── Whether a policy is effective and how to improve it → Pattern 3 (Policy Analysis)
├── Creative/design related
│   ├── Generating knowledge through the creative process → Pattern 10 (Creative/Practice-Based Research)
│   ├── Understanding the experience of creators → Pattern 6 (Exploratory Research)
│   └── Analyzing creative texts/works → Pattern 5 (Content Analysis)
└── Uncertain
    ├── New topic with scarce literature → Pattern 6 (Exploratory Research)
    ├── Complex problem requiring multiple data types → Pattern 4 (Mixed Methods)
    └── First see how others have approached it → Pattern 1 (Systematic Literature Review)
```
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-preregistration-guide-md"></a>

## SOURCE: skills/deep-research/references/preregistration_guide.md

<!-- SOURCE-CONTENT-BEGIN bytes=12106 -->
# Preregistration Guide — Research Preregistration Guide

## Purpose
Decision guide and operational manual for research preregistration. Assists the research_architect_agent in determining whether preregistration is needed during the methodology design stage, and guides researchers through the preregistration process.

---

## 1. Preregistration Decision Tree

```
Does your research have the following characteristics?
│
├── Confirmatory research (hypothesis testing)
│   └── Strongly recommend preregistration
│       ├── Has pre-specified statistical hypotheses → Preregister
│       ├── Will conduct significance testing → Preregister
│       └── Has primary outcome variables → Preregister
│
├── Exploratory research
│   └── Preregistration not required (but optional)
│       ├── Qualitative research → Typically not preregistered
│       ├── Data mining / EDA → Typically not preregistered
│       └── But you can preregister the research design and analysis process
│
├── Systematic review / Meta-analysis
│   └── Strongly recommend registration (PROSPERO)
│       └── Many journals require systematic reviews to be pre-registered
│
├── Randomized controlled trial (RCT)
│   └── Must register
│       ├── ICMJE requires RCTs to be pre-registered
│       └── Most journals will not accept unregistered RCTs
│
├── Replication study
│   └── Strongly recommend preregistration
│       └── Preregistration clearly distinguishes original from modified hypotheses
│
└── Secondary data analysis
    └── Recommend preregistration
        └── Prevents HARKing (Hypothesizing After Results are Known)
```

### When Preregistration Is Not Needed

- Purely qualitative research (grounded theory, phenomenology)
- Exploratory data analysis (no pre-specified hypotheses)
- Theoretical or philosophical research
- Literature reviews (except systematic reviews)
- Case reports or case studies

### When Preregistration Is Strongly Recommended

- Any research involving hypothesis testing
- Research involving multiple comparisons
- Research needing to distinguish confirmatory vs. exploratory analyses
- Research that may be questioned for p-hacking or HARKing
- When applying for research funding (demonstrates research rigor)
- When journals explicitly require or encourage preregistration

---

## 2. Preregistration Platform Overview

| Platform | Applicable Field | Features | Cost |
|------|---------|------|------|
| **OSF Registries** | All disciplines | Most widely used, multiple templates, DOI, permanent preservation | Free |
| **PROSPERO** | Systematic reviews | Dedicated to systematic reviews and meta-analyses | Free |
| **AEA Registry** | Economics | American Economic Association's RCT registration platform | Free |
| **AsPredicted** | All disciplines | Simplified preregistration (9 questions), quick to complete | Free |
| **ClinicalTrials.gov** | Clinical trials | US FDA-required RCT registration | Free |
| **EGAP** | Political science | Experiments in Governance and Politics | Free |
| **RIDIE** | Development economics | Registry for International Development Impact Evaluations | Free |

### Platform Selection Guide

```
What is your research?
│
├── Systematic review / meta-analysis → PROSPERO
├── Clinical trial / medical intervention → ClinicalTrials.gov
├── Economics RCT → AEA Registry
├── Just need simple preregistration → AsPredicted
└── All other research → OSF Registries (recommended)
```

---

## 3. 21-Item Core Content Checklist

Based on the OSF Standard Pre-Data Collection Registration format, the following are the 21 core items:

### A. Study Information

| # | Item | Description |
|---|------|------|
| 1 | **Study title** | Descriptive title |
| 2 | **Authors/Research team** | All researchers' names and affiliations |
| 3 | **Research questions** | Main research questions (clear, specific) |
| 4 | **Hypotheses** | Pre-specified hypotheses (including directional predictions) |

### B. Design Plan

| # | Item | Description |
|---|------|------|
| 5 | **Study design** | Experiment/observational, between/within-subjects, factorial design, etc. |
| 6 | **Randomization** | Randomization method (if applicable) |
| 7 | **Blinding** | Blinding level and implementation (if applicable) |
| 8 | **Conditions/manipulations** | Specific description of each experimental condition/group |

### C. Sampling Plan

| # | Item | Description |
|---|------|------|
| 9 | **Existing data** | Whether existing data is being used; nature and status of data |
| 10 | **Data collection procedures** | How data will be collected (survey, interview, experiment, archival) |
| 11 | **Sample size** | Planned sample size and basis for determination |
| 12 | **Sample size rationale** | Power analysis or other sample size calculation method |
| 13 | **Stopping rule** | When to stop collecting data (fixed N / target power reached / time cutoff) |

### D. Variables

| # | Item | Description |
|---|------|------|
| 14 | **Manipulated variables** | Operational definition of independent variables |
| 15 | **Measured variables** | Operational definition and measurement instruments of dependent variables |
| 16 | **Indices** | Specific indicators for each variable (scales, items, scoring methods) |

### E. Analysis Plan

| # | Item | Description |
|---|------|------|
| 17 | **Statistical models** | Primary statistical methods for analysis |
| 18 | **Transformations** | Data transformation plan (e.g., log transformation, standardization) |
| 19 | **Inference criteria** | Significance level (alpha), correction methods, effect size reporting |
| 20 | **Data exclusion** | Exclusion criteria (outlier definition, attention check failure, etc.) |
| 21 | **Exploratory analyses** | Planned but non-primary hypothesis analyses |

---

## 4. Higher Education Research Preregistration Examples

### Example: Effect of Teaching Strategy on Learning Outcomes

```
Title: The Effect of Flipped Classroom on University Students' Critical Thinking
       Skills: A Randomized Controlled Trial

Hypotheses:
H1: Students receiving flipped classroom instruction will score significantly
    higher on the CCTST than students receiving traditional lectures
H2: The benefit of flipped classroom will be greater for students with low
    prior knowledge than for those with high prior knowledge

Design: Cluster-randomized controlled trial (class as randomization unit)
Sample: 12 classes (6 experimental / 6 control), approximately 40 students
        per class, total 480
Power: 80% power to detect d = 0.4, alpha = .05, ICC = 0.05

Primary outcome: CCTST post-test score (controlling for pre-test)
Secondary outcomes: Final exam grade, learning motivation scale
Analysis: Multilevel modeling (students nested in classes)

Exclusion criteria:
- Attendance rate < 50%
- Both pre-test and post-test incomplete
- Attention check questions answered incorrectly

Exploratory analyses:
- Gender × teaching method interaction effect
- Learning motivation as a mediating variable
```

### Example: Systematic Review of University Dropout Factors

```
Title: Factors Influencing University Student Dropout Decisions in Taiwan:
       A Systematic Literature Review

Research question: What factors influence university student dropout decisions
                   in Taiwan?
Databases: Airiti Library, TSSCI, Scopus, Web of Science
Search strategy: (dropout OR withdrawal OR leave)
                 AND (university OR higher education)
                 AND (Taiwan)
Time range: 2010-2025
Inclusion criteria:
- Studies with Taiwan university students as research subjects
- Explore causes or factors of dropout/withdrawal
- Peer-reviewed journal articles or theses/dissertations
Exclusion criteria:
- Research subjects below high school level
- Pure policy commentary (no empirical data)
Quality assessment: Mixed Methods Appraisal Tool (MMAT)
Synthesis method: Thematic synthesis
Registration platform: PROSPERO
```

---

## 5. Preregistration Disclosure Statement Templates

### Disclosing Preregistration in a Paper

#### Standard Statement (Preregistered)
```
This study was preregistered on [Platform] prior to data collection
(registration number: [NUMBER]; URL: [URL]). All hypotheses, sample size
rationale, and analysis plans were specified before data collection began.
Deviations from the preregistered plan are noted in [section/supplementary
materials].
```

#### Disclosure of Deviations from Preregistration
```
Deviations from preregistered plan:
1. [Deviation description]: [Reason for deviation]
2. [Deviation description]: [Reason for deviation]
These deviations do not affect the confirmatory nature of the primary analyses.
The preregistered analyses are reported as planned; additional exploratory
analyses are clearly labeled.
```

#### Disclosure When Not Preregistered
```
This study was not preregistered. While the hypotheses were formulated before
data analysis, the distinction between confirmatory and exploratory analyses
should be interpreted with this limitation in mind.
```

---

## 6. Preregistration vs. Registered Reports

| Aspect | Preregistration | Registered Reports |
|------|-------------------------|-------------------------------|
| **Definition** | Research plan publicly registered in advance | Research plan submitted to a journal for pre-review |
| **Review** | Does not undergo peer review | Stage 1 peer review (research design) |
| **Acceptance timing** | Paper submitted only after completion | Receives "In-Principle Acceptance" (IPA) after passing Stage 1 |
| **Results bias** | Reduced but not eliminated (researchers can still selectively report) | Substantially eliminated (published regardless of results) |
| **Publication bias** | Cannot solve | Effectively solved (null results also published) |
| **Applicable journals** | All journals | Only journals accepting Registered Reports |
| **Difficulty** | Low (just fill in a form) | High (requires complete methodology and passing review) |
| **Flexibility** | Higher (deviations require disclosure but don't block submission) | Lower (major deviations may affect acceptance) |

### Registered Reports Process

```
Stage 1: Submit research plan
├── Introduction (theoretical background, literature review)
├── Methods (complete methodology, analysis plan)
├── Pilot data (if available)
└── Interpretation plan for predicted results
         ↓
Stage 1 Review (research design quality)
├── Accept (In-Principle Acceptance, IPA)
├── Revise and resubmit
└── Reject
         ↓
Stage 2: Conduct research, write results
├── Strictly follow the Stage 1 plan
├── Report all preregistered analyses (including null results)
├── Exploratory analyses clearly labeled
└── Deviations disclosed and explained
         ↓
Stage 2 Review (execution quality)
├── Was the Stage 1 plan faithfully executed?
├── Are results reported completely?
└── Typically not rejected due to null results
         ↓
Publication
```

### Selected Higher Education Journals Supporting Registered Reports

- *Studies in Higher Education*
- *Higher Education*
- *Assessment & Evaluation in Higher Education*
- *Teaching in Higher Education*
- *Educational Research Review*
- *Learning and Instruction*

> Full list: [COS Registered Reports](https://www.cos.io/initiatives/registered-reports)

---

## Quick Reference: 3 Steps to Preregistration

1. **Decide whether to preregister**: Determine if your research involves hypothesis testing
2. **Choose a platform**: Use PROSPERO for systematic reviews, OSF for everything else
3. **Fill in the 21-item checklist**: Use the `templates/preregistration_template.md` template

> Preregistration is not a perfect solution, but it is currently the most practical transparency tool. Even an imperfect preregistration is better than no preregistration at all.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-source-quality-hierarchy-md"></a>

## SOURCE: skills/deep-research/references/source_quality_hierarchy.md

<!-- SOURCE-CONTENT-BEGIN bytes=7332 -->
# Source Quality Hierarchy — Evidence Grading Framework

## Purpose
Systematic framework for grading evidence quality, used by the source_verification_agent and bibliography_agent.

## Evidence Pyramid (7 Levels)

```
         ╱╲
        ╱ I ╲        Systematic Reviews / Meta-Analyses
       ╱──────╲
      ╱  II    ╲     Randomized Controlled Trials
     ╱──────────╲
    ╱   III      ╲   Controlled Studies (non-randomized)
   ╱──────────────╲
  ╱    IV          ╲  Case-Control / Cohort Studies
 ╱──────────────────╲
╱     V              ╲  Systematic Reviews of Descriptive Studies
╱──────────────────────╲
╱      VI                ╲  Single Descriptive / Qualitative Studies
╱──────────────────────────╲
╱       VII                  ╲  Expert Opinion / Committee Reports
╱──────────────────────────────╲
```

## Detailed Level Descriptions

### Level I: Systematic Reviews & Meta-Analyses
**Weight**: Highest
**Description**: Rigorous synthesis of all available evidence using predefined, systematic methods.
**Characteristics**:
- Pre-registered protocol (PROSPERO or similar)
- Comprehensive search across multiple databases
- Explicit inclusion/exclusion criteria
- Quality assessment of included studies
- Statistical pooling (meta-analysis) when appropriate
- PRISMA reporting guidelines followed

**Trusted Sources**: Cochrane Library, Campbell Collaboration, JBI Evidence Synthesis

**Caveats**: Quality depends on included studies ("garbage in, garbage out"); may be outdated if field moves fast.

### Level II: Randomized Controlled Trials (RCTs)
**Weight**: Very High
**Description**: Experimental studies with random allocation to intervention/control groups.
**Characteristics**:
- Random assignment
- Control/comparison group
- Blinding (single, double, or triple)
- Pre-registered protocol
- Adequate sample size
- Intention-to-treat analysis

**Caveats**: Not always feasible (especially in social science/education); ethical constraints; external validity concerns.

### Level III: Controlled Studies Without Randomization
**Weight**: High
**Description**: Quasi-experimental designs with comparison groups but no randomization.
**Characteristics**:
- Comparison group present
- Pre-post measurements
- Attempts to control confounds
- Larger samples than case studies

**Examples**: Difference-in-differences, propensity score matching, regression discontinuity.

**Caveats**: Selection bias risk; confounding variables harder to control.

### Level IV: Case-Control & Cohort Studies
**Weight**: Moderate-High
**Description**: Observational studies tracking groups over time or comparing cases to controls.
**Characteristics**:
- Longitudinal (cohort) or retrospective (case-control)
- Natural variation, no researcher intervention
- Large samples possible
- Real-world context

**Caveats**: Cannot establish causation; confounders possible; recall bias (case-control).

### Level V: Systematic Reviews of Descriptive/Qualitative Studies
**Weight**: Moderate
**Description**: Rigorous synthesis of qualitative or descriptive research.
**Characteristics**:
- Systematic search and selection
- Quality appraisal of included studies
- Meta-synthesis or meta-ethnography techniques
- Transparent methods

**Caveats**: Quality limited by included studies; interpretive layer adds subjectivity.

### Level VI: Single Descriptive or Qualitative Studies
**Weight**: Low-Moderate
**Description**: Individual case studies, ethnographies, surveys, descriptive analyses.
**Characteristics**:
- In-depth, context-rich
- Exploratory or descriptive purpose
- Small samples typical
- Thick description

**Caveats**: Limited generalizability; researcher subjectivity; no causal claims warranted.

### Level VII: Expert Opinion & Committee Reports
**Weight**: Lowest
**Description**: Position papers, editorials, committee reports, guidelines based on expert consensus.
**Characteristics**:
- Based on expertise and experience
- Often integrates multiple evidence types informally
- May reflect institutional or ideological positions

**Caveats**: Not empirically tested; potential bias; "authority" ≠ "evidence."

## Grading Rubric

### Per-Source Assessment

| Criterion | Grade A (Excellent) | Grade B (Good) | Grade C (Adequate) | Grade D (Weak) | Grade F (Unacceptable) |
|-----------|-------|-------|-------|-------|-------|
| Evidence Level | I-II | III | IV-V | VI | VII or unclassifiable |
| Peer Review | Rigorous peer review | Standard peer review | Editorial review | No formal review | Self-published |
| Methodology | Exemplary, replicable | Sound, described | Adequate | Questionable | Absent/flawed |
| Sample/Data | Large, representative | Adequate | Limited but justified | Small, convenience | Unspecified |
| Currency | < 3 years | 3-5 years | 5-10 years | > 10 years | Outdated for topic |
| Conflicts | None declared or detected | Minor, disclosed | Moderate, disclosed | Undisclosed potential | Clear undisclosed conflict |

### Overall Source Grade
- **A**: Use as primary evidence
- **B**: Use as supporting evidence
- **C**: Use with explicit caveats
- **D**: Use only if no better source; acknowledge weakness
- **F**: Do not use; cite only if critiquing

## Field-Specific Adjustments

Not all fields use the same evidence hierarchy. Adjust expectations:

| Field | Gold Standard | Common Level | Notes |
|-------|--------------|-------------|-------|
| Medicine/Health | Level I-II (RCTs, meta-analyses) | Level I-III | Evidence-based medicine tradition |
| Education | Level III-IV (quasi-experimental) | Level IV-VI | Randomization often impractical |
| Social Science | Level III-V | Level IV-VI | Mixed methods common |
| Policy | Level IV-V + VII (expert panels) | Level V-VII | Context-dependent; expert opinion valued |
| Humanities | Level VI (primary sources) | Level VI-VII | Different epistemology; "evidence" means different things |
| Technology | Level III + industry reports | Level V-VII | Fast-moving; peer review lags reality |

## Predatory Publication Indicators

### Red Flags Checklist
- [ ] Aggressive email solicitation to submit
- [ ] Acceptance within 72 hours of submission
- [ ] No identifiable editorial board (or fake names)
- [ ] Not indexed in Scopus, Web of Science, or PubMed
- [ ] Not member of COPE (Committee on Publication Ethics)
- [ ] Not listed in DOAJ (Directory of Open Access Journals)
- [ ] Excessively broad scope ("International Journal of Everything")
- [ ] Fake or inflated impact metrics
- [ ] Poor grammar/spelling on journal website
- [ ] APC (article processing charge) suspiciously low (< $200 for full OA)
- [ ] Editorial office in different country from stated location
- [ ] No retraction policy or ethics guidelines

### Verification Resources
- Beall's List (unofficial, but useful starting point)
- Cabell's Predatory Reports (subscription-based)
- DOAJ (whitelist of legitimate OA journals)
- COPE member directory
- Scopus Source List
- Journal Citation Reports (Clarivate)
- Think. Check. Submit. (thinkchecksubmit.org)
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-systematic-review-protocol-md"></a>

## SOURCE: skills/deep-research/references/systematic_review_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=4035 -->
# Systematic Review Mode — Full Protocol

Full PRISMA-compliant systematic literature review with optional meta-analysis. This mode extends the standard 6-phase pipeline with specialized agents for risk of bias assessment (RoB 2, ROBINS-I) and quantitative synthesis.

See `agents/risk_of_bias_agent.md` and `agents/meta_analysis_agent.md` for detailed agent definitions.
See `references/systematic_review_toolkit.md` for the Cochrane/PRISMA/GRADE reference guide.

## 5-Phase Pipeline

```
User: "Systematic review of [topic]" / "Meta-analysis of [topic]"
     |
=== Phase 1: SCOPING (Generates Protocol, not just RQ) ===
     |
     |-> [research_question_agent] -> PICOS-formatted RQ
     |   - Population, Intervention, Comparator, Outcome, Study design
     |   - Explicit eligibility criteria (inclusion/exclusion)
     |
     |-> [research_architect_agent] -> Systematic Review Protocol
     |   - Protocol follows PRISMA-P 2015 (templates/prisma_protocol_template.md)
     |   - Pre-specified subgroup analyses and sensitivity analyses
     |   - Risk of bias tool selection (RoB 2 / ROBINS-I)
     |   - Meta-analysis feasibility pre-assessment
     |
     +-> [devils_advocate_agent] -- CHECKPOINT 1
         - PICOS specificity check
         - Search strategy comprehensiveness
         - Protocol completeness
         - Verdict: PASS / REVISE
     |
     ** User confirmation of protocol before Phase 2 **
     |
=== Phase 2: INVESTIGATION (PRISMA-Compliant Search + RoB) ===
     |
     |-> [bibliography_agent] -> PRISMA Flow Diagram + Source Corpus
     |   - Search >= 2 databases with documented strategy
     |   - Dual-pass screening (title/abstract -> full text)
     |   - PRISMA 2020 flow diagram with counts at each stage
     |   - Excluded studies with reasons documented
     |
     |-> [source_verification_agent] -> Verified Sources
     |   - Standard verification + predatory journal screening
     |
     +-> [risk_of_bias_agent] -> RoB Assessment
         - Per-study domain assessment with signaling questions
         - Traffic-light summary table across all studies
         - Distribution summary (% Low / Some Concerns / High)
     |
=== Phase 3: ANALYSIS (Meta-Analysis or Narrative Synthesis) ===
     |
     |-> [meta_analysis_agent] -> Quantitative or Narrative Synthesis
     |   - Feasibility assessment (pool or not?)
     |   - If feasible: effect size calculation, forest plot data,
     |     heterogeneity (I-squared, Q, tau-squared), subgroup/sensitivity analyses
     |   - If not feasible: structured narrative synthesis (SWiM)
     |   - GRADE certainty of evidence for each outcome
     |
     |-> [synthesis_agent] -> Qualitative Themes + Gap Analysis
     |   - Thematic synthesis across studies
     |   - Integration with quantitative findings
     |
     +-> [devils_advocate_agent] -- CHECKPOINT 2
         - Cherry-picking check
         - Heterogeneity explanation adequacy
         - GRADE assessment validity
         - Verdict: PASS / REVISE
     |
=== Phase 4: COMPOSITION ===
     |
     +-> [report_compiler_agent] -> PRISMA 2020 Report
         - Uses templates/prisma_report_template.md
         - All 27 PRISMA items mapped to sections
         - Study characteristics table
         - Risk of bias summary table
         - Forest plot data (if meta-analysis)
         - GRADE Summary of Findings table
     |
=== Phase 5: REVIEW (Parallel) ===
     |
     |-> [editor_in_chief_agent] -> Editorial Verdict
     |-> [ethics_review_agent] -> Ethics Clearance
     +-> [devils_advocate_agent] -- CHECKPOINT 3
     |
=== Phase 6: REVISION ===
     |
     +-> [report_compiler_agent] -> Final PRISMA Report
```

## Checkpoint Rules

1. All standard checkpoint rules apply (see SKILL.md Checkpoint Rules)
2. **Protocol must be registered** (or registration recommended) before Phase 2
3. **Risk of bias must be completed for all studies** before Phase 3
4. **GRADE assessment required** for every pooled outcome
5. **PRISMA checklist compliance** verified in Phase 5
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-systematic-review-toolkit-md"></a>

## SOURCE: skills/deep-research/references/systematic_review_toolkit.md

<!-- SOURCE-CONTENT-BEGIN bytes=19134 -->
# Systematic Review Toolkit — Reference Guide

## Purpose

Comprehensive reference for conducting systematic reviews and meta-analyses. Covers Cochrane methodology, PRISMA 2020 reporting, risk of bias instruments, heterogeneity interpretation, GRADE certainty framework, and protocol registration. Used by `risk_of_bias_agent`, `meta_analysis_agent`, `bibliography_agent`, and `report_compiler_agent`.

---

## 1. Cochrane Handbook v6.4 — Key Principles

The Cochrane Handbook for Systematic Reviews of Interventions (v6.4, 2023) is the gold standard reference for systematic review methodology.

### Core Methodology Stages

| Stage | Cochrane Chapter | Key Requirements |
|-------|-----------------|-----------------|
| Planning | Ch 1-3 | Protocol registration, clear objectives, PICOS |
| Searching | Ch 4 | Comprehensive search (≥ 2 databases), documented strategy |
| Selecting | Ch 4 | Independent dual screening, predefined criteria |
| Data extraction | Ch 5 | Standardized forms, pilot testing, dual extraction |
| Risk of bias | Ch 8 (RoB 2), Ch 25 (ROBINS-I) | Domain-based assessment, signaling questions |
| Synthesis | Ch 10-12 | Appropriate statistical methods, heterogeneity assessment |
| GRADE | Ch 14 | Certainty of evidence for each outcome |
| Reporting | Ch 15 | PRISMA 2020 compliance |

### Fundamental Principles

1. **A priori protocol**: Register the protocol before conducting the review (PROSPERO, OSF)
2. **Comprehensive searching**: Search multiple databases; do not rely on a single source
3. **Dual independent processes**: Two reviewers for screening, extraction, and risk of bias (at minimum for a subset)
4. **Pre-specified methods**: Analysis plan defined before seeing results
5. **Transparent reporting**: Document everything; another team should be able to replicate the review

---

## 2. PRISMA 2020 — Full 27-Item Checklist

**Full Name**: Preferred Reporting Items for Systematic Reviews and Meta-Analyses
**Reference**: Page et al. (2021). BMJ, 372, n71. https://doi.org/10.1136/bmj.n71

### Title and Abstract

| # | Item | Guidance |
|---|------|---------|
| 1 | **Title** | Identify the report as a systematic review, meta-analysis, or both |
| 2 | **Abstract** | Structured summary: background, objectives, data sources, study eligibility criteria, participants, interventions, study appraisal/synthesis methods, results, limitations, conclusions, registration number |

### Introduction

| # | Item | Guidance |
|---|------|---------|
| 3 | **Rationale** | Describe the rationale for the review in the context of existing knowledge |
| 4 | **Objectives** | Provide an explicit statement of the questions being addressed with reference to PICOS |

### Methods

| # | Item | Guidance |
|---|------|---------|
| 5 | **Eligibility criteria** | Specify inclusion and exclusion criteria (PICOS components, date range, language, publication status) |
| 6 | **Information sources** | Describe all information sources searched (databases, registers, websites, organizations, reference lists) with dates |
| 7 | **Search strategy** | Present the complete search strategy for at least one database, including any filters and limits |
| 8 | **Selection process** | State methods for deciding which studies met eligibility criteria (number of reviewers, consensus process) |
| 9 | **Data collection process** | Describe methods for extracting data (number of reviewers, whether independently, any processes for obtaining/confirming data from investigators) |
| 10 | **Data items** | List and define all outcome variables and other variables extracted |
| 11 | **Study risk of bias assessment** | Describe methods for assessing risk of bias in included studies, including tools used and how results were used in synthesis |
| 12 | **Effect measures** | Specify for each outcome the effect measure(s) used (e.g., RR, MD, SMD) |
| 13a | **Synthesis methods** | Describe the processes used to decide which studies were eligible for each synthesis |
| 13b | | Describe any methods required to prepare the data for synthesis (e.g., handling multi-arm studies) |
| 13c | | Describe any methods used to tabulate or visually display results of individual studies and syntheses |
| 13d | | Describe any methods used to synthesize results and rationale (meta-analysis: model, software; narrative: SWiM) |
| 13e | | Describe any methods used to explore possible causes of heterogeneity (subgroup, meta-regression) |
| 13f | | Describe any sensitivity analyses conducted |
| 14 | **Reporting bias assessment** | Describe any methods used to assess risk of bias due to missing results (publication bias) |
| 15 | **Certainty assessment** | Describe any methods used to assess certainty in the body of evidence (e.g., GRADE) |

### Results

| # | Item | Guidance |
|---|------|---------|
| 16a | **Study selection** | Describe results of the search and selection process, ideally using a PRISMA flow diagram |
| 16b | | Cite studies that appeared to meet inclusion criteria but were excluded, and explain why |
| 17 | **Study characteristics** | For each included study cite it and present its characteristics |
| 18 | **Risk of bias in studies** | Present assessments of risk of bias for each included study |
| 19 | **Results of individual studies** | For all outcomes, present for each study: summary data, effect estimates and CIs, results of syntheses |
| 20a | **Results of syntheses** | For each synthesis, briefly summarize the characteristics and risk of bias among contributing studies |
| 20b | | Present results of all statistical syntheses conducted, including CIs and measures of heterogeneity |
| 20c | | Present results of all investigations of possible causes of heterogeneity |
| 20d | | Present results of all sensitivity analyses |
| 21 | **Reporting biases** | Present assessments of risk of bias due to missing results |
| 22 | **Certainty of evidence** | Present assessments of certainty of evidence for each outcome assessed |

### Discussion

| # | Item | Guidance |
|---|------|---------|
| 23 | **Discussion** | Provide a general interpretation of results in the context of other evidence, discuss limitations of the evidence and of the review process, implications |
| 24 | **Registration and protocol** | Provide registration information including register name and registration number, and a link to the protocol |
| 25 | **Support** | Describe sources of financial or non-financial support and the role of funders |
| 26 | **Competing interests** | Declare any competing interests of review authors |
| 27 | **Availability of data, code, and other materials** | Report which of the following are publicly available: template data collection forms, data extracted from included studies, analysis code, any other materials |

### PRISMA 2020 Flow Diagram

```
 ┌─────────────────────────────────────────────────────┐
 │                 IDENTIFICATION                      │
 ├─────────────────────────────────────────────────────┤
 │ Records identified from databases (n = )            │
 │ Records identified from other sources (n = )        │
 └──────────────────────┬──────────────────────────────┘
                        │
 ┌──────────────────────▼──────────────────────────────┐
 │ Records removed before screening:                   │
 │   Duplicate records (n = )                          │
 │   Records marked as ineligible by automation (n = ) │
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
 │                                                     │
 │ Studies included in quantitative synthesis (n = )   │
 └─────────────────────────────────────────────────────┘
```

---

## 3. RoB 2 Instrument Summary

**Full Name**: Risk of Bias tool for randomized trials (version 2)
**Reference**: Sterne et al. (2019). BMJ, 366, l4898. https://doi.org/10.1136/bmj.l4898

### Domains

| Domain | Abbreviation | Focus |
|--------|-------------|-------|
| Bias arising from the randomization process | D1 | Sequence generation, allocation concealment, baseline balance |
| Bias due to deviations from intended interventions | D2 | Blinding, protocol adherence, ITT analysis |
| Bias due to missing outcome data | D3 | Completeness, differential dropout, handling of missing data |
| Bias in measurement of the outcome | D4 | Outcome assessment method, blinding of assessors |
| Bias in selection of the reported result | D5 | Pre-registration, selective reporting |

### Judgment Scale

- **Low risk of bias**: The study is judged to be at low risk of bias for this domain
- **Some concerns**: The study raises some concerns about bias for this domain
- **High risk of bias**: The study is judged to be at high risk of bias for this domain

### Overall Judgment Algorithm

- All domains Low → Overall **Low**
- Some Concerns in ≥ 1 domain, no High → Overall **Some Concerns**
- High in ≥ 1 domain → Overall **High**

---

## 4. ROBINS-I Summary

**Full Name**: Risk Of Bias In Non-randomized Studies of Interventions
**Reference**: Sterne et al. (2016). BMJ, 355, i4919. https://doi.org/10.1136/bmj.i4919

### Domains (7 domains spanning 3 time points)

**Pre-intervention**:
- D1: Bias due to confounding
- D2: Bias in selection of participants into the study

**At intervention**:
- D3: Bias in classification of interventions

**Post-intervention**:
- D4: Bias due to deviations from intended interventions
- D5: Bias due to missing data
- D6: Bias in measurement of outcomes
- D7: Bias in selection of the reported result

### Judgment Scale

- **Low risk**: Comparable to a well-performed RCT
- **Moderate risk**: Sound for a non-randomized study but cannot be considered comparable to a well-performed RCT
- **Serious risk**: Some important problems
- **Critical risk**: Study is too problematic to provide useful evidence
- **No information**: Insufficient reporting

---

## 5. I² Interpretation Guide

| I² Range | Label | What It Means | Action |
|----------|-------|---------------|--------|
| 0-40% | Low | Heterogeneity might not be important | Proceed with pooling; report I² |
| 30-60% | Moderate | May represent moderate heterogeneity | Proceed with pooling; investigate sources |
| 50-90% | Substantial | Substantial heterogeneity | Investigate sources; consider subgroup analyses; report prediction interval |
| 75-100% | Considerable | Considerable heterogeneity | Question whether pooling is meaningful; consider narrative synthesis |

**Important caveats**:
- Ranges overlap intentionally (per Cochrane Handbook 10.10.2)
- I² significance depends on: magnitude of effects, p-value from Q-test, and visual inspection of forest plot
- A high I² with all effects in the same direction is less concerning than moderate I² with effects crossing zero
- I² is influenced by precision of studies — many precise studies can yield high I² even with small absolute differences
- Always report the 95% CI for I² (which can be very wide with few studies)

---

## 6. GRADE Certainty of Evidence Framework

**Full Name**: Grading of Recommendations, Assessment, Development and Evaluations
**Reference**: Guyatt et al. (2008). BMJ, 336, 924-926.

### Starting Points

| Study Design | Starting Certainty |
|-------------|-------------------|
| Randomized trials | HIGH (⊕⊕⊕⊕) |
| Non-randomized studies | LOW (⊕⊕◯◯) |

### Factors That Lower Certainty (Rate Down)

| Factor | Rate Down | When to Apply |
|--------|-----------|---------------|
| Risk of bias | -1 or -2 | Serious or very serious limitations in study design/execution |
| Inconsistency | -1 or -2 | Unexplained heterogeneity (I² > 50%, different directions of effect) |
| Indirectness | -1 or -2 | Evidence does not directly address the PICOS of the review question |
| Imprecision | -1 or -2 | Wide CIs, small sample sizes, CIs cross clinical decision threshold |
| Publication bias | -1 | Funnel plot asymmetry, small study effects, known unpublished trials |

### Factors That Raise Certainty (Rate Up — Observational Studies Only)

| Factor | Rate Up | When to Apply |
|--------|---------|---------------|
| Large effect | +1 or +2 | RR > 2 or < 0.5 (large), RR > 5 or < 0.2 (very large), without confounders |
| Dose-response gradient | +1 | Clear dose-response relationship observed |
| Plausible confounding | +1 | All plausible confounders would reduce the observed effect |

### Certainty Levels

| Level | Symbol | Meaning |
|-------|--------|---------|
| High | ⊕⊕⊕⊕ | Very confident the true effect lies close to the estimate |
| Moderate | ⊕⊕⊕◯ | Moderately confident; the true effect is likely close but may be substantially different |
| Low | ⊕⊕◯◯ | Limited confidence; the true effect may be substantially different |
| Very Low | ⊕◯◯◯ | Very little confidence; the true effect is likely substantially different |

---

## 7. Protocol Registration Guidance

### When to Register

- **Always** for systematic reviews intended for publication
- **Before** starting the literature search
- Registration prevents outcome reporting bias and demonstrates a priori planning

### Where to Register

| Platform | Focus | Cost | URL |
|----------|-------|------|-----|
| **PROSPERO** | Health-related systematic reviews | Free | crd.york.ac.uk/prospero |
| **OSF Registries** | Any discipline | Free | osf.io/registries |
| **INPLASY** | Any discipline | ~$40 | inplasy.com |
| **Research Registry** | Any discipline | Free for systematic reviews | researchregistry.com |

### Protocol Content (PRISMA-P 2015)

See `templates/prisma_protocol_template.md` for the complete protocol template.

Key sections:
1. Title, registration, authors, amendments
2. Rationale, objectives, PICOS eligibility criteria
3. Information sources, search strategy, study records management
4. Data extraction, risk of bias assessment, data synthesis plan
5. Meta-bias assessment, confidence in cumulative evidence

---

## 8. Software and Tools

### Statistical Software for Meta-Analysis

| Tool | Language | Best For | Key References |
|------|----------|----------|---------------|
| **metafor** (R) | R | Comprehensive meta-analysis (all models, diagnostics) | Viechtbauer (2010) |
| **meta** (R) | R | User-friendly standard meta-analyses | Balduzzi et al. (2019) |
| **dmetar** (R) | R | Companion to "Doing Meta-Analysis in R" textbook | Harrer et al. (2021) |
| **RevMan** | Standalone | Cochrane reviews (required for Cochrane) | Cochrane Collaboration |
| **robvis** (R) | R | Risk of bias visualization (traffic-light plots) | McGuinness & Higgins (2020) |
| **GRADE pro GDT** | Web-based | GRADE Summary of Findings tables | McMaster University |

### Screening and Management Tools

| Tool | Purpose | Cost |
|------|---------|------|
| **Covidence** | Study screening, data extraction, RoB | Paid (free Cochrane license) |
| **Rayyan** | Abstract screening (AI-assisted) | Free |
| **EPPI-Reviewer** | Full review management | Paid |
| **ASReview** | AI-assisted screening | Free (open source) |
| **Zotero/Mendeley** | Reference management | Free |

---

## Quick Decision Guide

```
Starting a systematic review?
│
├── 1. Register your protocol
│   └── PROSPERO (health) or OSF (any field)
│
├── 2. Write your protocol
│   └── Use PRISMA-P template → templates/prisma_protocol_template.md
│
├── 3. Search systematically
│   └── ≥ 2 databases, document everything, PRISMA flow
│
├── 4. Screen and select
│   └── Dual screening, predefined criteria
│
├── 5. Assess risk of bias
│   └── RCTs → RoB 2 | Non-randomized → ROBINS-I
│
├── 6. Synthesize evidence
│   ├── Quantitative data + comparable studies → Meta-analysis
│   └── Otherwise → Narrative synthesis (SWiM)
│
├── 7. Assess certainty
│   └── GRADE for each outcome
│
└── 8. Report
    └── PRISMA 2020 checklist → templates/prisma_report_template.md
```
<!-- SOURCE-CONTENT-END -->
