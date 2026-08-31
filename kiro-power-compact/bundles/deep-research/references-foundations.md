<a id="source-skills-deep-research-references-apa7-style-guide-md"></a>

## SOURCE: skills/deep-research/references/apa7_style_guide.md

<!-- SOURCE-CONTENT-BEGIN bytes=4684 -->
# APA 7th Edition — Quick Reference Guide

## Purpose
Quick reference for APA 7.0 formatting used by the report_compiler_agent and editor_in_chief_agent.

## Document Formatting

### General
- Font: 12pt Times New Roman, 11pt Calibri, or 11pt Arial
- Margins: 1 inch (2.54 cm) on all sides
- Line spacing: Double-spaced throughout
- Paragraph indent: 0.5 inch (1.27 cm) first line
- Page numbers: Top right corner

### Headings (5 Levels)

| Level | Format |
|-------|--------|
| 1 | **Centered, Bold, Title Case** |
| 2 | **Left-Aligned, Bold, Title Case** |
| 3 | *Left-Aligned, Bold Italic, Title Case* |
| 4 | **Indented, Bold, Title Case, Ending With a Period.** Text continues... |
| 5 | *Indented, Bold Italic, Title Case, Ending With a Period.* Text continues... |

## In-Text Citations

### Parenthetical Citations
- One author: (Smith, 2023)
- Two authors: (Smith & Jones, 2023)
- Three+ authors: (Smith et al., 2023)
- Multiple works: (Jones, 2022; Smith, 2023) — alphabetical order
- Same author, same year: (Smith, 2023a, 2023b)
- Organization: (World Health Organization [WHO], 2023) first time; (WHO, 2023) after
- No date: (Smith, n.d.)
- Secondary source: (Original Author, Year, as cited in Citing Author, Year)

### Narrative Citations
- Smith (2023) found that...
- Smith and Jones (2023) argued...
- Smith et al. (2023) demonstrated...

### Direct Quotations
- Short (< 40 words): "exact words" (Author, Year, p. X)
- Long (≥ 40 words): Block quote, indented 0.5 inch, no quotation marks
  (Author, Year, p. X) at end

### Page Numbers
- Required for direct quotes: p. X or pp. X–Y
- Encouraged for paraphrases from long works

## Reference List

### General Rules
- Heading: "References" (Level 1 heading)
- Hanging indent: 0.5 inch
- Double-spaced
- Alphabetical by first author's surname
- Include DOI as hyperlink when available: https://doi.org/xxxxx

### Journal Article
```
Author, A. A., Author, B. B., & Author, C. C. (Year). Title of article in sentence case. *Title of Periodical in Title Case*, *Volume*(Issue), Page–Page. https://doi.org/xxxxx
```

### Book
```
Author, A. A. (Year). *Title of work in sentence case: Capital letter for subtitle* (Edition). Publisher. https://doi.org/xxxxx
```

### Edited Book Chapter
```
Author, A. A. (Year). Title of chapter. In E. E. Editor (Ed.), *Title of book* (pp. xx–xx). Publisher. https://doi.org/xxxxx
```

### Report / Grey Literature
```
Organization Name. (Year). *Title of report* (Report No. xxx). https://www.url.com
```

### Webpage
```
Author, A. A. (Year, Month Day). *Title of page*. Site Name. https://www.url.com
```

### Government Document
```
Government Agency. (Year). *Title of document* (Publication No. xxx). Publisher. https://www.url.com
```

### Conference Paper
```
Author, A. A. (Year, Month Days). *Title of contribution* [Type]. Conference Name, Location. https://doi.org/xxxxx
```

### Thesis / Dissertation
```
Author, A. A. (Year). *Title of dissertation* [Doctoral dissertation, University Name]. Database Name. https://www.url.com
```

### Dataset
```
Author, A. A. (Year). *Title of dataset* (Version) [Data set]. Publisher. https://doi.org/xxxxx
```

## Special Cases

### No Author
- Use organization or title in author position
- Short title in citations: ("Short Title," Year)

### No Date
- (n.d.) in place of year

### Translated Works
```
Author, A. A. (Year). *Title in original language* [Title in English] (T. Translator, Trans.). Publisher. (Original work published Year)
```

### Multiple Works by Same Author Same Year
- Assign lowercase letters: 2023a, 2023b
- Based on title alphabetical order

## Tables

```
Table X

Descriptive Title of Table in Italic

[Table content]

Note. General note about the table. Adapted from "Title," by Author, Year, Journal, Volume, p. X. Copyright Year by Copyright Holder.
```

## Figures

```
Figure X

Descriptive Title of Figure in Italic

[Figure]

Note. Description and source information.
```

## Numbers

- Spell out: numbers below 10, numbers beginning a sentence
- Use numerals: 10 and above, statistical/mathematical, dates, ages, scores
- Exception: Always use numerals with units (3 cm, 5 mg)

## Common Errors to Avoid

1. Using "&" in text (use "and" in text; "&" only in parenthetical citations and reference list)
2. Missing DOIs for sources that have them
3. Inconsistent heading levels
4. Period after DOI/URL (don't add one)
5. Using "et al." with only 2 authors (use both names)
6. Orphan references (cited but not in reference list, or vice versa)
7. Incorrect capitalization in reference titles (sentence case, not title case)
8. Missing issue numbers for journals that paginate by issue
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-argumentation-reasoning-framework-md"></a>

## SOURCE: skills/deep-research/references/argumentation_reasoning_framework.md

<!-- SOURCE-CONTENT-BEGIN bytes=4000 -->
# Argumentation & Reasoning Framework

A cognitive framework for evaluating the strength and validity of research arguments. Use this to **think about** argument quality, not just check boxes.

## Toulmin Model of Argumentation

Every research argument has 6 components. When evaluating, identify each:

| Component | Question | Red Flag if Missing |
|-----------|----------|-------------------|
| **Claim** | What is being asserted? | Vague or shifting thesis |
| **Data/Evidence** | What evidence supports it? | Claims without empirical backing |
| **Warrant** | Why does the evidence support the claim? | Logical gap between data and conclusion |
| **Backing** | What supports the warrant itself? | Assumed methodology validity |
| **Qualifier** | How certain is the claim? | Absolute language ("proves", "always") |
| **Rebuttal** | What would undermine the claim? | No acknowledged limitations |

**Judgment heuristic**: If you can't identify the Warrant, the argument is likely weak regardless of how much Data is presented. Data without Warrant is just information.

## Causal Reasoning (Bradford Hill Criteria, adapted)

When a paper claims X causes Y, evaluate against these 9 criteria:

1. **Strength of association** — How large is the effect?
2. **Consistency** — Replicated across studies/contexts?
3. **Specificity** — Does X specifically lead to Y (not everything)?
4. **Temporality** — Does X precede Y? (Only mandatory criterion)
5. **Biological/theoretical gradient** — More X → more Y?
6. **Plausibility** — Is there a reasonable mechanism?
7. **Coherence** — Consistent with existing knowledge?
8. **Experiment** — Is there experimental evidence?
9. **Analogy** — Do similar causes produce similar effects?

**Judgment heuristic**: Most social science papers satisfy 3-5 criteria. Fewer than 3 = causal claim is unsupported. Only #4 (temporality) is strictly required; the rest are cumulative evidence.

## Inference to Best Explanation (IBE)

When multiple explanations exist for the same finding:

1. List ALL plausible explanations (not just the author's preferred one)
2. Evaluate each on: **explanatory scope** (how much it explains), **simplicity** (fewer ad-hoc assumptions), **fit** (consistency with known facts), **predictive power** (does it predict new observations?)
3. The best explanation is the one that scores highest across all four — not the one that fits the author's hypothesis

**Judgment heuristic**: If the paper only considers one explanation, that's confirmation bias regardless of how well-argued it is. At minimum, the Discussion section should address the two strongest alternative explanations.

## Epistemic Status of Claims

Not all claims carry equal weight. Classify each major claim:

| Status | Meaning | Appropriate Language |
|--------|---------|---------------------|
| **Established** | Replicated, peer-reviewed, high consensus | "X is..." |
| **Supported** | Evidence exists but not yet replicated | "Evidence suggests X..." |
| **Preliminary** | Single study or small sample | "Preliminary findings indicate..." |
| **Speculative** | Based on reasoning, not direct evidence | "We hypothesize that..." |
| **Contested** | Conflicting evidence exists | "While some studies find X, others..." |

**Judgment heuristic**: If a paper uses "Established" language for "Preliminary" findings, that's overclaiming — one of the most common quality issues in academic writing.

## Application by Agent

| Agent | Primary Use |
|-------|------------|
| `synthesis_agent` | Toulmin analysis of synthesized arguments; IBE for competing explanations |
| `devils_advocate_agent` | Causal reasoning audit; identify missing Rebuttals and Qualifiers |
| `source_verification_agent` | Epistemic status classification of source claims |
| `socratic_mentor_agent` | Guide users through Toulmin decomposition of their own arguments |
| `research_architect_agent` | Ensure methodology design supports causal claims at appropriate level |
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-changelog-md"></a>

## SOURCE: skills/deep-research/references/changelog.md

<!-- SOURCE-CONTENT-BEGIN bytes=2348 -->
## [2.9.1] - 2026-04-22

### Added

- **Opt-in reading-check probe** in Socratic Mentor. Gated by `ARS_SOCRATIC_READING_PROBE=1`. See `agents/socratic_mentor_agent.md` §"Optional Reading Probe Layer" and `SKILL.md` §"Opt-in Reading Probe (v3.5.1)".

### Version

- 2.9.0 → 2.9.1 (patch; opt-in, default OFF).

---

# Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.4 | 2026-03-27 | Report compiler now consumes optional Style Profile (from academic-paper intake) and runs Writing Quality Check checklist before finalizing reports. Style Profile applied as soft guide for Executive Summary and Synthesis sections; discipline conventions take priority. Writing Quality Check catches overused AI-typical terms, em dash overuse, throat-clearing openers, and monotonous sentence rhythm. See `academic-paper/references/writing_quality_check.md` and `shared/style_calibration_protocol.md` |
| 2.3 | 2026-03-08 | Added systematic-review mode (7th mode): PRISMA 2020 compliant pipeline with risk_of_bias_agent (RoB 2 + ROBINS-I), meta_analysis_agent (effect sizes, heterogeneity, GRADE, narrative synthesis), 2 new templates (PRISMA protocol + report), systematic_review_toolkit reference. Added monitoring_agent (post-pipeline literature monitoring with digests, retraction alerts, author tracking) + literature_monitoring_strategies reference. Enhanced socratic_mentor_agent with 4 convergence signals, 4-type question taxonomy, and auto-end triggers. Added Quick Mode Selection Guide to SKILL.md |
| 2.2 | 2026-03-05 | Added synthesis anti-patterns, Socratic quantified thresholds & auto-end conditions, reference existence verification (DOI + WebSearch), enhanced ethics reference integrity check (50% + Retraction Watch), mode transition matrix, cross-agent quality alignment definitions |
| 2.1 | 2026-03 | Added IRB decision tree, EQUATOR reporting guidelines, preregistration guide + template; enhanced ethics_review_agent with human subjects dimension; enhanced research_architect_agent with ethics/EQUATOR/preregistration integration; enhanced methodology_patterns with EQUATOR cross-references |
| 2.0 | 2026-02 | Added socratic mode (10th agent), failure paths, mode selection guide, handoff protocol, 2 new examples, 3 new references |
| 1.0 | 2026-02 | Initial release: 9 agents, 5 modes, 6-phase pipeline |
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-crossref-api-protocol-md"></a>

## SOURCE: skills/deep-research/references/crossref_api_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=4243 -->
# Crossref API Verification Protocol

**Status**: v3.9.0
**Used by**: `bibliography_agent`, `migrate_literature_corpus_to_v3_9_0.py`
**API base**: `https://api.crossref.org`
**Rate limit**: 10 req/s (polite pool, with `mailto:` in User-Agent), ~5 req/s (anonymous, varies). Confirmed via live `x-rate-limit-limit` / `x-rate-limit-interval` response headers (2026-05).
**Polite email env var**: `CROSSREF_POLITE_EMAIL` (optional)

---

## Purpose

Provides a third bibliographic-index lookup for v3.9.0 cross-index triangulation per spec v3.9.0 §3.5. Crossref is the DOI registry of record — strongest coverage for journal articles with DOIs. Monograph / chapter coverage is partial (publisher participation dependent). v3.9.0 surfaces `crossref_unmatched` as one of three signals; the user retains discretion per R-L3-2-A.

Mirrors the structure of `semantic_scholar_api_protocol.md` and `openalex_api_protocol.md`.

## Query Patterns

### Pattern 1: DOI Lookup with Title Cross-Check (primary when DOI is available)

```
GET /works/{doi}
```

Note: raw DOI in path, NO `doi:` prefix (Crossref convention; OpenAlex uses `/works/doi:{doi}`).

**Matching rule (mirrors S2 `DOI_MISMATCH` pattern):** DOI lookup hits are gated by a Levenshtein 0.70 title cross-check. Crossref returns `title` as a list of language variants; the first entry is compared. If similarity below threshold -> DOI_MISMATCH, return None, fall through to title search.

### Pattern 2: Title Search (fallback when DOI absent or DOI_MISMATCH)

```
GET /works?query.title={url_encoded_title}&rows=5
```

**Matching rule:** Levenshtein similarity >= 0.70 (matching S2 / OpenAlex / PaperOrchestra threshold). When multiple candidates pass, prefer matching-year tiebreaker via +0.05 score bonus. Crossref year lives in `issued.date-parts[0][0]` (canonical); fall through to `published-print` / `published-online` if `issued` absent.

## `crossref_unmatched` derivation

`true` if and only if:
- DOI present: DOI lookup either returns 404, misses title cross-check, AND title search returns no match meeting threshold; OR
- DOI absent: title search alone returns no match meeting threshold.

The check fires only when `obtained_via != 'manual'`.

## Degradation handling

| Condition | Action |
|---|---|
| HTTP 404 on DOI | Treat as miss -- return `{}` from `_get`; caller falls through to title search. NOT a degradation. |
| HTTP 429 (rate limit) | Back off 2 seconds, retry up to 3 times. After exhaustion, raise `CrossrefUnavailable`. Throttle anchor refreshed after each backoff. |
| HTTP 5xx | Raise `CrossrefUnavailable` immediately (no retry). |
| Network timeout (30s default) | Raise `CrossrefUnavailable`. |
| `CrossrefUnavailable` raised | Caller MUST omit `crossref_unmatched` from the entry (per spec v3.9.0 R-L3-2-C: absent != false). Other indexes proceed independently. |

## v3.9.0 R-L3-2-D constraint

Crossref returns `type` (e.g., `journal-article`, `book-chapter`). **v3.9.0 ignores this field.** Not stored on entries, not surfaced to finalizer, not used in any derivation. v3.10 will introduce adapter-declared `venue_type` with explicit provenance.

## Crossref-specific notes

- **Coverage caveat:** strongest for journal articles with DOIs. Monograph / chapter coverage depends on publisher DOI registration. Conference proceedings vary. This asymmetry is by design -- combined with S2 and OpenAlex, the three-index signal captures different genre profiles.
- **Polite pool etiquette:** the `mailto:` in User-Agent header (not query param) follows Crossref's documented convention for higher rate limits.

## Client implementation

See `scripts/crossref_client.py`. Class `CrossrefClient` exposes `doi_lookup_with_title_check(doi, expected_title)` and `title_search(title, year=None)`. Both return `dict | None` (the dict being either the `message` for DOI, or one item from `message.items` for title search). Both raise `CrossrefUnavailable` on degradation per the table above.

## Cross-references

- Spec: `docs/design/2026-05-17-ars-v3.9.0-cross-index-triangulation-measurement-spec.md` §3.5
- Mirror template: `deep-research/references/semantic_scholar_api_protocol.md`
- Sibling protocol: `deep-research/references/openalex_api_protocol.md`
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-ethics-checklist-md"></a>

## SOURCE: skills/deep-research/references/ethics_checklist.md

<!-- SOURCE-CONTENT-BEGIN bytes=10478 -->
# Research Ethics Checklist — AI-Assisted Research

## Purpose
Comprehensive ethics checklist for AI-assisted academic research. Used by the ethics_review_agent.

## 1. AI Disclosure

### Mandatory Disclosure Elements
- [ ] AI tools used are named (e.g., "Claude," "GPT-4," "Gemini")
- [ ] Scope of AI involvement specified:
  - [ ] Literature search assistance
  - [ ] Source screening
  - [ ] Evidence synthesis
  - [ ] Draft writing
  - [ ] Editing/revision
  - [ ] Data analysis
  - [ ] Translation
- [ ] Human oversight described (who reviewed what, at which stages)
- [ ] AI limitations acknowledged (potential hallucination, knowledge cutoff, etc.)
- [ ] AI version/date noted (for reproducibility)

### Disclosure Statement Template
```
AI Disclosure: This research was conducted with assistance from [AI Tool Name]
(version/date). AI was used for [specific tasks]. All findings were verified
against cited sources by [human role]. The research team maintains full
responsibility for the accuracy and interpretation of all content.
```

### Where to Place Disclosure
- In the methodology section (detailed)
- In the abstract or author note (brief)
- In footnotes for specific AI-generated analyses

## 2. Attribution Integrity

### Citation Ethics
- [ ] Every factual claim has at least one supporting citation
- [ ] No fabricated or hallucinated references
  - Verification: Spot-check minimum 20% of references for existence
  - Cross-check DOIs, publication years, author names
- [ ] Paraphrasing is genuine (not just rearranging words)
- [ ] Direct quotes are exact and attributed
- [ ] Ideas are attributed to original authors, not intermediary sources
- [ ] Self-citation is proportionate (not excessive or exclusionary)

### AI-Specific Attribution Risks
| Risk | Description | Mitigation |
|------|-------------|-----------|
| Hallucinated references | AI generates plausible but non-existent citations | Verify every reference against database |
| Merged citations | AI combines details from multiple sources | Cross-check each citation element |
| Incorrect authors | AI assigns wrong authors to works | Verify author names against actual publications |
| Wrong year | AI uses incorrect publication year | Cross-check against database records |
| Ghost citations | References listed but never cited in text | Audit reference list against in-text citations |

## 3. Dual-Use Assessment

### Screening Questions
1. Could this research be used to harm individuals or communities?
2. Does it reveal vulnerabilities that could be exploited?
3. Could it be used to develop surveillance or control mechanisms?
4. Does it provide information that could be weaponized?
5. Could it be used to discriminate against specific groups?

### Risk Levels and Responses

| Level | Action Required |
|-------|----------------|
| None | No additional action |
| Low | Brief note in limitations |
| Moderate | Responsible Use statement in report |
| High | Prominent warning + limited distribution recommendation |
| Critical | Do not publish without institutional ethics review |

### Responsible Use Statement Template
```
Responsible Use: This research is intended for [stated purpose]. The authors
acknowledge that findings related to [sensitive area] could potentially be
applied in ways not intended by this research. Users of this research are
urged to consider the ethical implications of their applications and to
prioritize [specific ethical principle].
```

## 4. Fair Representation

### Balanced Treatment Checklist
- [ ] Multiple perspectives on contested issues are presented
- [ ] Minority/dissenting viewpoints are not dismissed without engagement
- [ ] Subjects and communities are described accurately
- [ ] Language is respectful and non-stigmatizing
- [ ] Cultural context is acknowledged where relevant
- [ ] Power dynamics are considered (who is studied vs. who studies)
- [ ] Geographic and cultural diversity in sources

### Sensitive Topics
- Indigenous knowledge: Respect OCAP principles (Ownership, Control, Access, Possession)
- Disability: Person-first language unless community prefers identity-first
- Gender/sexuality: Use inclusive, current terminology
- Race/ethnicity: Use preferred terminology of the communities discussed
- Socioeconomic status: Avoid deficit framing
- Mental health: Avoid stigmatizing language

### Representation Audit Questions
1. Whose voices are centered? Whose are missing?
2. Are communities described on their own terms?
3. Is there implicit bias in the framing?
4. Would the subjects/communities recognize themselves in this description?

## 5. Data Ethics

### Data Source Ethics
- [ ] All data sources are legal to use
- [ ] Public data: Confirm public domain or appropriate license
- [ ] Licensed data: Usage complies with license terms
- [ ] Scraped data: Complies with robots.txt and terms of service
- [ ] Personal data: GDPR/privacy law compliance (if applicable)
- [ ] Institutional data: Authorized access confirmed

### Privacy Protection
- [ ] No personally identifiable information (PII) without consent
- [ ] Aggregated data used where possible
- [ ] Small-N groups protected from identification
- [ ] Institutional identities protected when not public
- [ ] Data retention/deletion plan (if primary data collected)

### AI-Specific Data Concerns
- [ ] AI training data biases acknowledged
- [ ] AI knowledge cutoff date noted
- [ ] AI-generated data clearly labeled as such
- [ ] No circular citation (AI cites AI-generated content)

## 6. Conflict of Interest

### Types to Assess
- [ ] Financial: Funding source, consulting relationships
- [ ] Institutional: Author evaluating own institution
- [ ] Intellectual: Author defending own prior work
- [ ] Personal: Relationships with subjects/stakeholders
- [ ] Political: Government-funded research on government policy
- [ ] Commercial: Industry connections or product interests
- [ ] AI-specific: AI tool company influence on research design

### Disclosure Requirement
Any identified conflict must be disclosed in the report, with an assessment of whether it could have influenced the findings.

## 7. Reproducibility Ethics

### Documentation Requirements
- [ ] Search strategies documented (databases, terms, dates)
- [ ] Inclusion/exclusion criteria documented
- [ ] Analytical methods described in replicable detail
- [ ] AI prompts/instructions documented (if relevant)
- [ ] Data processing steps documented
- [ ] Code/scripts shared (if applicable)

### Reproducibility Statement Template
```
Reproducibility: The search strategy, inclusion criteria, and analytical
methods used in this research are documented in [section/appendix]. The
AI-assisted components used [specific prompts/parameters]. Researchers
wishing to replicate or extend this work should note [relevant limitations
or conditions].
```

## 8. Human Subjects Ethics

### 8.1 Human Subjects Determination

- [ ] Does the research collect, use, or analyze human-related data?
- [ ] If yes, is the data personally identifiable?
- [ ] If the data is publicly available and de-identified, has exempt review status been confirmed with the IRB?

### 8.2 IRB Review Levels

| Review Level | Applicable Conditions | Review Timeline |
|-------------|----------------------|-----------------|
| **Exempt Review** | Public data, de-identified data, anonymous surveys (no sensitive topics) | 1-2 weeks |
| **Expedited Review** | Minimal risk, non-vulnerable populations, general surveys/interviews | 2-4 weeks |
| **Full Board Review** | Greater than minimal risk, vulnerable populations, sensitive topics, deception | 4-8 weeks |

- [ ] Applicable IRB review level has been determined
- [ ] IRB review timeline has been incorporated into the research project schedule
- [ ] Researcher has completed research ethics training (CITI or equivalent course)

### 8.3 Informed Consent

- [ ] Informed consent form includes research title, purpose, procedures, risks, and benefits
- [ ] Clearly states voluntary nature of participation (may withdraw at any time, no penalties)
- [ ] Provides researcher and IRB contact information
- [ ] Special situations addressed:
  - [ ] Online survey: Electronic consent (clicking "I agree")
  - [ ] Audio/video recording: Separate checkbox item
  - [ ] Minors: Legal guardian consent + subject assent
  - [ ] Indigenous research: Community consent + individual informed consent

### 8.4 Data De-identification

- [ ] Remove direct identifiers (names, student IDs, national ID numbers)
- [ ] Assess indirect identifier risks (department + year + gender combinations)
- [ ] Small sample re-identification risk assessment (small departments may allow re-identification of individuals)
- [ ] Remove identifiable details from qualitative quotations
- [ ] Encrypt data storage with access controls
- [ ] Establish data retention and destruction timeline

### 8.5 Vulnerable Population Protection

| Population | Additional Protective Measures |
|-----------|-------------------------------|
| **Minors** | Legal guardian consent + age-appropriate assent form |
| **Persons with disabilities** | Assess consent capacity, provide accessible consent procedures |
| **Students (researcher is a teacher)** | Avoid power dynamics affecting voluntariness, use third-party recruitment |
| **Indigenous peoples** | Community consultation and consent, respect OCAP principles |
| **Economically disadvantaged** | Compensation must not constitute undue inducement |
| **Incarcerated persons** | Additional IRB review, ensure non-coercive participation |

- [ ] Vulnerable populations involved in the research have been identified
- [ ] Corresponding additional protective measures have been planned
- [ ] IRB review level accounts for vulnerable population considerations

> For detailed IRB decision tree and Taiwan-specific process: see `references/irb_decision_tree.md`

---

## Quick Audit Checklist (Final Gate)

Before delivery, confirm ALL items:

- [ ] AI disclosure present and accurate
- [ ] All references spot-checked (minimum 20%)
- [ ] No fabricated citations detected
- [ ] Dual-use assessment completed
- [ ] Fair representation reviewed
- [ ] Data sources legally and ethically used
- [ ] Conflicts of interest disclosed
- [ ] Reproducibility documentation provided
- [ ] Writing is inclusive and respectful
- [ ] Report benefits stated audience without causing foreseeable harm
- [ ] If the research involves human subjects, has IRB review been planned?
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-failure-paths-md"></a>

## SOURCE: skills/deep-research/references/failure_paths.md

<!-- SOURCE-CONTENT-BEGIN bytes=15135 -->
# Failure Paths — Research Pipeline Failure Path Map

## Overview

This document lists all failure scenarios that may be encountered across all modes of the deep-research skill, along with their detection conditions, user notification messages, handling steps, and recovery paths. The purpose is to ensure every failure scenario has a clear handling strategy, preventing users from reaching a dead end.

---

## Failure Path Summary

| # | Failure Scenario | Affected Modes | Severity | Handling Strategy |
|---|---------|---------|---------|---------|
| F1 | RQ cannot converge | full, socratic | Medium | Narrow scope / provide candidate RQs |
| F2 | Insufficient literature | full, quick, lit-review | High | Expand search strategy |
| F3 | Methodology mismatch | full | High | Return to Phase 1 |
| F4 | Devil's Advocate CRITICAL | full | Critical | STOP + correct |
| F5 | Ethics BLOCKED | full, review | Critical | STOP + remediation path |
| F6 | Socratic dialogue does not converge | socratic | Medium | Switch to full mode |
| F7 | User abandons mid-process | all | Low | Save progress |
| F8 | Only Chinese-language literature available | full, lit-review | Medium | Switch search strategy |
| F9 | All source quality below threshold | full, fact-check | High | Downgrade or expand sources |
| F10 | Conclusions inconsistent with evidence | full | High | Return to Phase 3 |
| F11 | Revision loop exceeds limit | full | Medium | Force-complete + limitation list |
| F12 | Interdisciplinary bridging failure | full | Low | Revert to single discipline |

---

## Detailed Failure Paths

### F1: Research Question Cannot Converge

**Affected Modes**: `full` (Phase 1), `socratic` (Layer 1)
**Severity**: Medium

**Trigger Conditions**:
- `full` mode: research_question_agent interaction exceeds 3 rounds, user still cannot determine the RQ
- `socratic` mode: Layer 1 exceeds 5 rounds, user repeatedly revises without a clear direction

**User Notification Message**:
> I notice we've been discussing for a while, but the research question hasn't converged to a clear direction yet. This is perfectly normal — sometimes the question itself is the hardest part. Let me offer a few possible directions to see which one is closest to your thinking.

**Handling Steps**:
1. Compile key topics discussed and user-expressed preferences
2. Produce 3 candidate RQs, each with a brief explanation and rough FINER assessment
3. Ask the user to select the closest one as a starting point
4. If the user still cannot choose → suggest doing a `lit-review` mode to explore the literature first, then return

**Recovery Paths**:
- Select a candidate RQ → continue the original workflow
- Do lit-review → restart RQ clarification after the literature review is complete
- User redescribes on their own → restart Phase 1 / Layer 1

---

### F2: Insufficient Literature

**Affected Modes**: `full` (Phase 2), `quick`, `lit-review`
**Severity**: High

**Trigger Conditions**:
- bibliography_agent finds < 5 usable sources after standard search strategy
- After excluding quality-unqualified sources, < 3 remain

**User Notification Message**:
> With the current search strategy, I found only limited relevant literature. This could mean: (1) this is a very new research area; (2) the search keywords need adjustment; (3) the research question scope may need refinement. Let me try expanding the search strategy.

**Handling Steps**:
1. Expand search keywords (synonyms, broader terms, related concepts)
2. Expand database scope (add grey literature, policy reports, working papers)
3. Relax time range (from past 5 years to past 10 years)
4. Try keywords from adjacent disciplines
5. If still insufficient → suggest the user consider adjusting the RQ or accept this as an exploratory study

**Recovery Paths**:
- Expanded search yields sufficient literature → continue original workflow
- Accept as exploratory research → adjust report positioning, emphasize the study's pioneering nature
- Adjust RQ → return to Phase 1

---

### F3: Methodology Mismatch

**Affected Modes**: `full` (Checkpoint 1)
**Severity**: High

**Trigger Conditions**:
- devils_advocate_agent at Checkpoint 1 determines that the methodology proposed by research_architect_agent cannot answer the RQ produced by research_question_agent
- There is a logical gap between the methodology and the RQ

**User Notification Message**:
> Devil's Advocate found an important issue in the methodology review: your research question asks "why," but your method design can only answer "whether." Let's go back and adjust — here are three possible directions...

**Handling Steps**:
1. Clearly state the gap between the RQ type (descriptive/comparative/causal/evaluative) and the method's capability
2. Provide 3 alternative method suggestions, each with pros and cons
3. Confirm whether the RQ needs adjustment to match a feasible method
4. Re-execute research_architect_agent

**Recovery Paths**:
- Select an alternative method → regenerate Methodology Blueprint → Checkpoint 1 re-review
- Adjust RQ → return to research_question_agent → redo Phase 1
- Maximum 2 retries; if still mismatched on the 3rd attempt → suggest the user consult their advisor

---

### F4: Devil's Advocate CRITICAL

**Affected Modes**: `full` (any Checkpoint)
**Severity**: Critical

**Trigger Conditions**:
- devils_advocate_agent finds a Critical severity issue at any Checkpoint
- Includes: fatal logical flaws, core assumptions that cannot hold, evidence contradicting conclusions

**User Notification Message**:
> STOP — Devil's Advocate found a critical issue that must be resolved before continuing:
> [Specific issue description]
> This is not an issue that can be ignored, as it fundamentally affects the research's validity.

**Handling Steps**:
1. Fully present the Critical issue's description, impact, and suggested correction direction
2. Pause the workflow; do not allow advancement to the next Phase
3. Wait for user response or correction
4. After user correction → re-execute the Checkpoint
5. 2 consecutive CRITICALs → suggest the user fundamentally rethink the research direction

**Recovery Paths**:
- User corrects the issue → re-execute Checkpoint → continue after PASS
- User chooses to modify the RQ/method → return to the corresponding Phase
- User abandons the direction → enter F7 workflow

---

### F5: Ethics BLOCKED

**Affected Modes**: `full` (Phase 5), `review`
**Severity**: Critical

**Trigger Conditions**:
- ethics_review_agent determines BLOCKED
- Includes: research involving non-consensual use of personal data, potentially discriminatory impact, dual-use risk

**User Notification Message**:
> Ethics Review has determined that this research has ethical issues requiring prior resolution:
> [Specific issue list]
> The research report cannot be delivered until these issues are resolved. Here are the suggested remediation paths...

**Handling Steps**:
1. List all BLOCKED reasons, each with specific remediation suggestions
2. Distinguish between remediable (e.g., add informed consent statement) and irremediable (e.g., research design inherently has ethical issues)
3. Remediable issues → provide modification suggestions → re-review after user confirmation
4. Irremediable issues → suggest fundamental redesign of the research

**Recovery Paths**:
- Fix ethical issues → re-execute ethics_review_agent → continue after CLEARED
- Modify research design → return to Phase 1
- Issues are irremediable → suggest abandoning this research direction, provide alternative direction suggestions

---

### F6: Socratic Dialogue Does Not Converge

**Affected Modes**: `socratic`
**Severity**: Medium

**Trigger Conditions**:
- Dialogue exceeds 10 rounds, user still vacillating between different directions
- Extracted INSIGHTs < 3

**User Notification Message**:
> We've explored several directions, each with its own value. However, I notice we've been going back and forth between a few directions — this may mean you have multifaceted interests in this topic, but it can also make the research hard to focus. Would you like to:
> (A) Continue the Socratic dialogue, but focus on [the most promising direction] you just mentioned?
> (B) Switch to full mode, and let my team help you systematically explore and converge?
> (C) Take a pause, think it over, and come back later?

**Handling Steps**:
1. Compile currently extracted INSIGHTs
2. Identify the 1-2 directions with the most convergence potential
3. Provide 3 options (continue with focus / switch mode / pause)
4. If user chooses to continue but still hasn't converged by round 15 → auto-compile + end

**Recovery Paths**:
- Continue with focus → restrict discussion scope, converge within 5 rounds
- Switch to full mode → pass extracted INSIGHTs to research_question_agent
- Pause → save INSIGHT list; user can re-enter at any time

---

### F7: User Abandons Mid-Process

**Affected Modes**: All modes
**Severity**: Low

**Trigger Conditions**:
- User explicitly states they don't want to continue ("never mind," "I quit," "too complicated")
- User abandons after a long period of non-response

**User Notification Message**:
> No problem. I've saved the current progress. Here's a summary of what we've accomplished so far:
> [List of completed stages and outputs]
> You can re-enter at any time by saying "continue the previous research," and we'll pick up where we left off.

**Handling Steps**:
1. Save all outputs from the current stage (RQ Brief, INSIGHTs, Bibliography, etc.)
2. Produce a progress summary
3. Provide instructions for re-entry

**Recovery Paths**:
- User says "continue the previous research" → load saved outputs, continue from where interrupted
- User starts over → entirely new workflow

---

### F8: Only Chinese-Language Literature Available

**Affected Modes**: `full` (Phase 2), `lit-review`
**Severity**: Medium

**Trigger Conditions**:
- English academic database searches (Web of Science, Scopus, PubMed, etc.) yield empty or very few results
- The topic is strongly localized (e.g., Taiwan-specific policy, regulations, institutional systems)

**User Notification Message**:
> English-language literature on this topic is very limited, but Chinese-language literature resources are abundant. I will adjust the search strategy to include Chinese academic databases. Please note that citation conventions for Chinese-language literature in international publications may differ.

**Handling Steps**:
1. Switch search strategy to Chinese academic databases (Airiti Library, National Digital Library of Theses and Dissertations in Taiwan, CNKI)
2. Re-search using Chinese keywords
3. Note the language distribution of the literature in the report
4. If the user needs an English report → provide suggestions for English citation format of Chinese literature
5. If the user needs to publish internationally → suggest finding comparable international cases

**Recovery Paths**:
- Chinese literature is sufficient → continue workflow with clear language annotations
- User needs international publication → suggest adjusting RQ to add a comparative perspective

---

### F9: All Source Quality Below Threshold

**Affected Modes**: `full` (Phase 2), `fact-check`
**Severity**: High

**Trigger Conditions**:
- source_verification_agent rates all found sources as Level V or below
- No peer-reviewed sources

**User Notification Message**:
> The overall quality of currently found sources is low, lacking high-quality peer-reviewed research. This may indicate an emerging field, or the search strategy may need adjustment. I suggest we consider...

**Handling Steps**:
1. Expand source types (add policy reports, white papers, official statistics)
2. Lower the threshold but clearly annotate quality levels
3. Reposition the report as "preliminary exploration" rather than "systematic review"
4. Add an "Evidence Quality Limitations" section to the report

**Recovery Paths**:
- Find sufficient alternative sources → continue workflow with clear quality annotations
- Cannot find qualified sources → suggest the user consider conducting primary research

---

### F10: Conclusions Inconsistent with Evidence

**Affected Modes**: `full` (Phase 5, Checkpoint 3)
**Severity**: High

**Trigger Conditions**:
- editor_in_chief_agent or devils_advocate_agent finds in Phase 5 that report conclusions exceed the scope supported by the evidence

**User Notification Message**:
> The review found that some conclusions in the report go beyond what the evidence supports. Specifically:
> [List of issues]
> I will return for revision to ensure every conclusion has corresponding evidence support.

**Handling Steps**:
1. Flag all "over-inferred" conclusions
2. For each flag: (a) weaken the conclusion to match the evidence, or (b) supplement with additional evidence
3. Re-execute Checkpoint 3

**Recovery Paths**:
- Revision successful → complete Phase 6
- Issues remain after revision → 2nd revision round
- Issues remain after 2 revisions → convert issues to a "Research Limitations" section

---

### F11: Revision Loop Exceeds Limit

**Affected Modes**: `full` (Phase 6)
**Severity**: Medium

**Trigger Conditions**:
- Phase 6 revision has been executed 2 times (maximum), with unresolved Major issues remaining

**User Notification Message**:
> After two rounds of revision, the following issues have been resolved: [resolved list]. However, the following issues remain unresolved due to inherent research limitations: [unresolved list]. These will be listed in the "Acknowledged Limitations" section. The report is now the best version achievable under current conditions.

**Handling Steps**:
1. Compile resolved and unresolved issues
2. Convert unresolved Major issues into the "Acknowledged Limitations" section
3. Deliver the final report

**Recovery Paths**:
- User accepts → deliver the report
- User does not accept → suggest redesigning the research from Phase 1

---

### F12: Interdisciplinary Bridging Failure

**Affected Modes**: `full`
**Severity**: Low

**Trigger Conditions**:
- synthesis_agent attempts interdisciplinary integration but cannot find meaningful connections
- Conceptual frameworks from different disciplines cannot be reconciled

**User Notification Message**:
> I attempted to integrate perspectives from [Discipline A] and [Discipline B], but these two disciplines' understanding frameworks for this phenomenon differ substantially. Forcing integration may actually blur the focus. I suggest we center on the [primary discipline] framework, and mention other disciplines' perspectives in the discussion section as reference.

**Handling Steps**:
1. Select the primary disciplinary framework as the analytical foundation
2. Present other disciplinary perspectives in an "Alternative Perspectives" or "Interdisciplinary Insights" section
3. Do not force integration of irreconcilable frameworks

**Recovery Paths**:
- Focus on a single framework → continue workflow
- User insists on interdisciplinary → suggest switching to mixed-methods or narrative review
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-interdisciplinary-bridges-md"></a>

## SOURCE: skills/deep-research/references/interdisciplinary_bridges.md

<!-- SOURCE-CONTENT-BEGIN bytes=21430 -->
# Interdisciplinary Bridges — Cross-Discipline Connection Patterns

## Purpose
Reference for identifying connections across academic disciplines. Used by the synthesis_agent and research_architect_agent to enrich analysis with cross-disciplinary perspectives.

## Why Interdisciplinary Bridges Matter

Most real-world problems don't respect disciplinary boundaries. A research team that stays within one discipline risks:
- Missing relevant evidence from adjacent fields
- Reinventing concepts already developed elsewhere
- Producing narrow recommendations that ignore systemic effects
- Overlooking methodological innovations from other traditions

## Common Bridge Patterns

### Pattern 1: Shared Concept, Different Names
The same concept exists in multiple fields under different names.

| Concept | Field A | Field B | Field C |
|---------|---------|---------|---------|
| Feedback loops | Systems Theory: feedback | Education: formative assessment | Economics: market correction |
| Path dependency | History: historical institutionalism | Economics: increasing returns | Technology: lock-in effect |
| Social capital | Sociology: Bourdieu/Putnam | Management: organizational networks | Education: community engagement |
| Resilience | Psychology: coping capacity | Ecology: ecosystem recovery | Engineering: structural redundancy |
| Quality assurance | Manufacturing: TQM/ISO | Education: accreditation | Software: testing/CI-CD |
| Stakeholder theory | Management: Freeman | Public policy: participatory governance | Education: community engagement |
| Knowledge transfer | Education: learning transfer | Management: knowledge management | Technology: technology transfer |

### Pattern 2: Shared Method, Different Applications
The same method is used across fields for different purposes.

| Method | Application A | Application B | Application C |
|--------|-------------|-------------|-------------|
| Network analysis | Social networks (Sociology) | Citation networks (Bibliometrics) | Neural networks (Neuroscience) |
| Thematic analysis | Qualitative research (Social Science) | Literary criticism (Humanities) | Market research (Business) |
| Regression analysis | Epidemiology (Health) | Econometrics (Economics) | Psychometrics (Psychology) |
| Case study | Law (precedent) | Business (HBS method) | Education (institutional research) |
| Simulation/modeling | Climate science | Economics (agent-based) | Epidemiology (SIR models) |
| Cost-benefit analysis | Public policy | Healthcare (QALY) | Environmental impact |

### Pattern 3: Complementary Perspectives
Different disciplines offer different lenses on the same phenomenon.

**Example: Higher Education Quality**
| Discipline | Lens | Key Questions |
|-----------|------|--------------|
| Education | Pedagogy & learning outcomes | Are students learning? |
| Economics | Human capital & ROI | Is the investment worthwhile? |
| Sociology | Access, equity & social mobility | Who benefits? Who is excluded? |
| Management | Organizational effectiveness | Is the institution well-run? |
| Public Policy | Accountability & public interest | Is the public well-served? |
| Psychology | Student development & well-being | Are students thriving? |
| Technology | Digital transformation | How does technology reshape learning? |
| Philosophy | Epistemology & purpose of education | What is education for? |

### Pattern 4: Theory Migration
Theories developed in one field are adapted and applied in another.

| Theory | Origin | Migration |
|--------|--------|-----------|
| Disruptive Innovation (Christensen) | Business → Education, Healthcare |
| Actor-Network Theory (Latour) | Sociology of Science → Information Systems, Education |
| Ecological Systems (Bronfenbrenner) | Developmental Psychology → Education, Social Work |
| Diffusion of Innovations (Rogers) | Communication → Health, Technology, Education |
| Institutional Theory (DiMaggio/Powell) | Sociology → Management, Education Policy |
| Complex Adaptive Systems | Biology → Management, Healthcare, Education |
| Game Theory | Mathematics → Economics, Political Science, Biology |
| Nudge Theory (Thaler/Sunstein) | Behavioral Economics → Public Policy, Health, Education |

## How to Use Interdisciplinary Bridges

### For the Research Architect
1. When designing methodology, check if adjacent fields have established methods for similar questions
2. Consider mixed-paradigm approaches when no single discipline adequately addresses the RQ
3. Look for theoretical frameworks from other fields that might illuminate the phenomenon

### For the Synthesis Agent
1. When synthesizing evidence, check for relevant studies in adjacent fields
2. Use shared concepts to connect findings across disciplinary silos
3. Identify where different disciplines' findings converge or diverge
4. Note when a knowledge gap in one field has been addressed in another

### For Expanding Search
When a bibliography search feels narrow, try:
1. Identify the core concept
2. Check the "Shared Concept" table for alternative terms
3. Search adjacent disciplines using their vocabulary
4. Look for review papers in bridging fields (e.g., "educational economics," "health policy," "science of learning")

## Discipline Map for Common Research Topics

### Education
- Core: Curriculum, Pedagogy, Assessment, Educational Psychology
- Adjacent: Sociology (equity), Economics (human capital), Policy (governance), Technology (ed-tech), Psychology (development)

### Health
- Core: Medicine, Public Health, Epidemiology, Nursing
- Adjacent: Economics (health economics), Policy (health policy), Psychology (behavioral health), Technology (digital health), Ethics (bioethics)

### Technology
- Core: Computer Science, Information Systems, Engineering
- Adjacent: Sociology (digital divide), Psychology (HCI), Business (innovation), Ethics (AI ethics), Policy (tech regulation)

### Governance & Policy
- Core: Political Science, Public Administration, Law
- Adjacent: Economics (public finance), Sociology (institutional analysis), Management (organizational theory), Ethics (political philosophy)

### Sustainability
- Core: Environmental Science, Ecology, Climate Science
- Adjacent: Economics (environmental economics), Policy (climate policy), Engineering (clean tech), Ethics (environmental ethics), Business (CSR/ESG)

### Pattern 5: Methodological Transfer
A mature methodology from one field, when systematically borrowed into another, often yields breakthrough research results.

| Original Method | Original Field | Post-Transfer Application | Target Field | Key Adaptations |
|-----------------|---------------|--------------------------|--------------|-----------------|
| Ethnography | Anthropology | Organizational Ethnography | Organizational Studies/Management | Shifted from "foreign cultures" to "organizational culture"; shorter fieldwork duration; focused on work practices |
| Randomized Controlled Trial (RCT) | Medicine/Clinical Trials | Randomized Experiments in Education | Education | Different ethical considerations (cannot deny students education); commonly uses cluster randomization |
| A/B Testing | Computer Science/Web Industry | Field Experiments | Social Science/Policy Evaluation | From product optimization to policy intervention effectiveness; different expectations for sample sizes and effect sizes |
| Design Thinking | Design Studies | Policy Design / Service Design | Public Policy/Public Services | Incorporates stakeholder participation, regulatory constraints, and equity considerations |
| Cohort Study | Epidemiology | Longitudinal Student Tracking | Education | From tracking disease risk factors to tracking learning trajectories; different approaches to handling attrition |
| Corpus Analysis | Linguistics | Social Media Analytics | Communication/Sociology | From normative linguistic structure analysis to informal language sentiment/topic analysis; requires handling noisy data |
| Grounded Theory | Sociology | Software Engineering Research | Software Engineering | From social phenomenon theory building to development practice pattern extraction; often combined with action research |
| Monte Carlo Simulation | Physics/Mathematics | Financial Risk Modeling | Finance | From particle behavior simulation to asset price volatility simulation; reasonableness of distribution assumptions becomes a core issue |

**Key Success Factors for Methodological Transfer:**
1. Understand the full context of the methodology in its original field (don't just learn the steps — understand why it was designed this way)
2. Identify the constraints of the new field (ethics, feasibility, data characteristics)
3. Make necessary adaptations rather than copying directly
4. Clearly describe what modifications were made during the transfer and why

### Pattern 6: Problem Reframing
The same real-world problem, redefined from different disciplinary perspectives, produces entirely different research questions, method choices, and solutions.

**Example 1: "Student Dropout"**

| Discipline | How the Problem Is Defined | Core Concepts | Typical Methods | Possible Solutions |
|-----------|---------------------------|---------------|-----------------|-------------------|
| Education | Insufficient learning motivation, teaching method mismatch | Engagement, self-regulated learning | Classroom observation, learning analytics | Adaptive instruction, remedial teaching, mentoring systems |
| Economics | Insufficient expected returns on educational investment | Human capital, opportunity cost, expected income | Cost-benefit analysis, regression analysis | Scholarships, tuition reduction, improving graduate employment rates |
| Sociology | Reproduction of structural social inequality | Social capital, cultural capital, class reproduction | Qualitative interviews, statistical analysis | Social support networks, first-generation college student programs |
| Psychology | Insufficient self-efficacy and sense of belonging | Self-efficacy, sense of belonging, growth mindset | Scale administration, experimental design | Psychological counseling, growth mindset interventions, peer support |
| Data Science | High-risk students can be predicted from historical data | Predictive models, early warning indicators | Machine learning, survival analysis | Early warning systems, automated intervention notifications |

**Interdisciplinary Integration Perspective**: The most effective dropout prevention does not approach the problem from a single discipline; rather, it combines financial support (economics) + learning support (education) + psychological counseling (psychology) + early warning systems (data science) + social support networks (sociology).

**Example 2: "University Transformation"**

| Discipline | How the Problem Is Defined | Core Concepts | Typical Methods | Possible Solutions |
|-----------|---------------------------|---------------|-----------------|-------------------|
| Management | Planning and executing organizational change | Change management, strategic planning, organizational learning | Case study, action research | Kotter's 8 steps, Balanced Scorecard, OKR |
| Political Science | Power dynamics among stakeholders | Governance structure, stakeholder analysis, institutional path dependency | Stakeholder analysis, institutional analysis | Governance reform, decision transparency, faculty participation mechanisms |
| Education | Fundamental curriculum and pedagogical innovation | Curriculum reform, competency-based education, learning outcomes | Curriculum analysis, teaching experiments | Curriculum restructuring, micro-credentials, interdisciplinary learning |
| Economics | Sustainable business model and revenue structure | Revenue diversification, cost structure, market positioning | Financial analysis, market analysis | Industry-university partnerships, lifelong learning market, international student recruitment |

**Interdisciplinary Integration Perspective**: University transformation often fails because only the management dimension (strategic planning) is addressed while ignoring the political science dimension (stakeholder resistance) and the education dimension (faculty buy-in for curriculum reform).

**Example 3: "AI Ethics"**

| Discipline | How the Problem Is Defined | Core Concepts | Typical Methods | Possible Solutions |
|-----------|---------------------------|---------------|-----------------|-------------------|
| Philosophy | Moral legitimacy of AI decision-making | Moral frameworks (utilitarianism/deontology/virtue ethics), moral agents | Conceptual analysis, thought experiments | Ethical guidelines, moral reasoning frameworks |
| Law | Legal liability when AI causes harm | Legal personhood, liability attribution, regulatory frameworks | Legal interpretation, comparative law | AI-specific legislation, liability insurance, certification systems |
| Computer Science | Achieving fairness and explainability at the technical level | Fairness metrics, XAI, alignment | Algorithm design, benchmarking | Bias detection tools, explainable models, red teaming |
| Sociology | How AI reinforces or reshapes existing power structures | Digital inequality, surveillance capitalism, algorithmic discrimination | Qualitative research, critical analysis | Algorithm auditing, civic participation, digital literacy education |

**Interdisciplinary Integration Perspective**: Technology alone (computer science's fairness metrics) cannot solve AI ethics, because "what counts as fair" is a philosophical question, "who decides" is a political question, and "how to enforce" is a legal question.

## Practical Guide

### How to Begin Thinking Interdisciplinarily

**Step 1: Define your core problem (in one sentence)**
- Good: "Why is the freshman enrollment rate at Taiwan's private universities continuously declining?"
- Not good: "Taiwan's higher education faces many challenges" (too vague)
- A one-sentence definition forces you to focus and helps people from other fields quickly understand what you're working on

**Step 2: List 3 disciplines you're unfamiliar with but that may be relevant**
- Find inspiration from the Problem Reframing examples
- Ask yourself: Who else is dealing with a similar problem? (Education → Economists also study human capital)
- Ask yourself: What are the upstream/downstream aspects of this problem? (University admissions → upstream is secondary education, downstream is the labor market)

**Step 3: Find one classic reference in each discipline**
- You don't need the most recent — find the most cited (Google Scholar sorted by citations)
- Finding review articles or handbook chapters is more efficient than finding individual papers
- Ask someone in that field: "If I could only read one paper, which would you recommend?"

**Step 4: Ask — "How would someone in this discipline view my problem?"**
- What concepts would they use to describe this phenomenon?
- What methods would they use to study this problem?
- What kind of answers would they give?
- How do their answers complement or contradict those from my own discipline?

**Step 5: Find at least one method or concept you can borrow**
- You don't need to go deep into every discipline — finding one valuable borrowing is enough
- When borrowing, "translate" it: explain in your own discipline's language why you're borrowing this concept/method
- Describe what adaptations you made (see Pattern 5 Methodological Transfer)

### Cross-Disciplinary Literature Search Strategies

**Strategy 1: Reverse Citation Tracking**
- Find your core reference in Google Scholar
- Click "Cited by" to see which papers from other fields have cited it
- These citing papers are cross-disciplinary bridge references

**Strategy 2: Cross-Domain Keyword Search**
- Search "interdisciplinary" + your topic (e.g., "interdisciplinary student retention")
- Search "perspectives on" + your topic
- Search "[other discipline name] + [your topic]" (e.g., "economic analysis of higher education quality")

**Strategy 3: Target Cross-Disciplinary Journals**
- Research Policy (technology policy + innovation + management)
- Science and Public Policy (science + policy)
- Higher Education (education + policy + sociology)
- Journal of Mixed Methods Research (cross-methodology)
- Studies in Higher Education (higher education research, multi-discipline)

**Strategy 4: Attend Conferences in Other Fields**
- You don't need to present a paper — just attend and listen
- Pay particular attention to how they define problems and what terminology they use
- Conference coffee breaks are the best opportunities for cross-disciplinary conversation

### Avoiding Common Pitfalls in Interdisciplinary Research

**Pitfall 1: Surface-Level Borrowing**
- Symptom: Borrowing terminology without understanding the underlying theoretical context
- Example: Using "disruptive innovation" to describe all change, without understanding the specific conditions in Christensen's definition
- Remedy: Read the original literature (not just secondary citations), understand the concept's scope and limitations

**Pitfall 2: Methodological Mismatch**
- Symptom: Forcing quantitative methods onto qualitative questions, or vice versa
- Example: Using survey scales to "measure" the value of artistic creation
- Remedy: First understand the nature of the question (is the goal to measure or to understand?), then choose the method

**Pitfall 3: Ignoring Disciplinary Nuance**
- Symptom: The same word means different things in different disciplines
- Example: "Validity" in quantitative research (statistical validity) vs. qualitative research (trustworthiness) means entirely different things
- Example: "Model" in mathematics (mathematical model) vs. design (prototype) vs. management (business model) means different things
- Remedy: Consult textbooks or handbooks in the target discipline to confirm terminology definitions

**Pitfall 4: Oversimplification**
- Symptom: Ignoring debates within another discipline, treating the entire field as monolithic
- Example: "Economists believe..." (Which economists? Neoclassical and behavioral economists may hold completely opposite views)
- Remedy: At minimum, understand 2-3 major schools or perspectives within the target discipline

## Discipline Map for Common Research Topics

### Education
- Core: Curriculum, Pedagogy, Assessment, Educational Psychology
- Adjacent: Sociology (equity), Economics (human capital), Policy (governance), Technology (ed-tech), Psychology (development)

### Health
- Core: Medicine, Public Health, Epidemiology, Nursing
- Adjacent: Economics (health economics), Policy (health policy), Psychology (behavioral health), Technology (digital health), Ethics (bioethics)

### Technology
- Core: Computer Science, Information Systems, Engineering
- Adjacent: Sociology (digital divide), Psychology (HCI), Business (innovation), Ethics (AI ethics), Policy (tech regulation)

### Governance & Policy
- Core: Political Science, Public Administration, Law
- Adjacent: Economics (public finance), Sociology (institutional analysis), Management (organizational theory), Ethics (political philosophy)

### Sustainability
- Core: Environmental Science, Ecology, Climate Science
- Adjacent: Economics (environmental economics), Policy (climate policy), Engineering (clean tech), Ethics (environmental ethics), Business (CSR/ESG)

### Arts & Humanities
- Core: Philosophy, Literature, History, Art History, Cultural Studies, Linguistics
- Adjacent: Sociology (cultural sociology), Psychology (aesthetics, creativity), Education (arts education), Technology (digital humanities), Communication (media studies)
- Cross-disciplinary highlights:
  - **Digital Humanities**: Applying computational methods to humanities research (text mining, GIS, network analysis)
  - **Medical Humanities**: How literature, philosophy, and history help understand doctor-patient relationships and health narratives
  - **Environmental Humanities**: Understanding climate change and environmental justice from a humanities perspective
  - **Practice-Based Research**: Artistic creation itself as a research method (see Methodology Patterns #10)

### Law & Justice
- Core: Constitutional Law, Civil Law, Criminal Law, International Law, Jurisprudence
- Adjacent: Political Science (judicial politics), Sociology (law and society, criminology), Economics (law and economics), Philosophy (legal philosophy, ethics), Psychology (forensic psychology), Technology (legal tech, AI and law)
- Cross-disciplinary highlights:
  - **Law and Economics**: Analyzing the effects of legal rules using the economic concept of efficiency
  - **Law and Society**: Law is not just statutes — it is social practice; how law is actually used, circumvented, and experienced
  - **Technology Law**: AI regulation, personal data protection, platform governance — how law responds to technological change
  - **Transitional Justice**: Combining law, political science, history, and psychology to address historical injustice

## Warning Signs of Shallow Interdisciplinarity

- Using another field's jargon without understanding its meaning
- Citing one paper from another field as representative of the whole field
- Ignoring methodological differences when comparing across disciplines
- Treating "interdisciplinary" as buzzword rather than genuine integration
- Assuming your discipline's methods are universal
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-irb-decision-tree-md"></a>

## SOURCE: skills/deep-research/references/irb_decision_tree.md

<!-- SOURCE-CONTENT-BEGIN bytes=11801 -->
# IRB Decision Tree — Human Subjects Research Ethics Review Guide

## Purpose
IRB (Institutional Review Board) ethics review decision tree and Taiwan process guide. Used by the ethics_review_agent to determine whether research involves human subjects, and by the research_architect_agent to plan IRB review during methodology design.

---

## 1. Human Subjects Research Determination Decision Tree

```
Does your research collect, use, or analyze data from humans?
│
├── No → Does not involve human subjects, no IRB review needed
│         (e.g., pure theoretical research, literature review, secondary analysis of public statistics)
│
└── Yes → Is the data personally identifiable?
          │
          ├── No → Is the data publicly available public data?
          │        │
          │        ├── Yes → Typically exempt from review
          │        │         But must still submit an exempt review application to IRB for confirmation
          │        │
          │        └── No → Proceed to "Review Level Determination" below
          │
          └── Yes → Does the research involve direct interaction with subjects?
                    │
                    ├── No → Only uses existing data/specimens
                    │        │
                    │        ├── Data already de-identified → May apply for exempt review
                    │        └── Data contains identifiable information → Expedited or full board review
                    │
                    └── Yes → Proceed to "Review Level Determination" below
```

---

## 2. Three-Level Review System

### 2.1 Exempt Review

**Applicable Conditions** (any one of the following):
- [ ] Uses publicly available, de-identified datasets
- [ ] Research on educational practices in normal educational settings
- [ ] Involves only anonymous surveys (no sensitive topics)
- [ ] Observation of public behavior (no identifiable information recorded)
- [ ] Uses government public statistical data

**Note**: Exempt review does not mean exempt from application — you must still submit to IRB to confirm exempt status.

### 2.2 Expedited Review

**Applicable Conditions** (all must be met):
- [ ] Research risk is no greater than risks ordinarily encountered in daily life (minimal risk)
- [ ] Does not involve vulnerable populations
- [ ] Research methods are on the expedited review category list

**Common Categories**:
- Surveys (containing sensitive but not high-risk topics)
- Interviews (general topics)
- Teaching intervention research (non-invasive)
- Audio/video recording (with consent)
- Secondary analysis of previously collected clinical data

### 2.3 Full Board Review

**Applicable Conditions** (any one of the following):
- [ ] Greater than minimal risk
- [ ] Involves vulnerable populations (children, prisoners, pregnant women, individuals with cognitive impairments)
- [ ] Involves sensitive topics (sexual behavior, illegal behavior, mental health)
- [ ] Uses deception
- [ ] May cause psychological or social harm

---

## 3. Taiwan IRB Process

### 3.1 Governing Authorities

| Authority | Jurisdiction | Legal Basis |
|-----------|-------------|-------------|
| **National Science and Technology Council (formerly MOST)** | NSTC-funded projects involving human research | "NSTC Guidelines for Research Grant Applications" |
| **Ministry of Health and Welfare** | Human research, clinical trials, human biobanks | "Human Subjects Research Act" (2011) |
| **Ministry of Education** | Research ethics in educational settings | Institutional regulations |

### 3.2 Regulatory Framework

| Regulation | Scope | Key Requirements |
|-----------|-------|------------------|
| **Human Subjects Research Act** | Research involving human subjects (surveys, interviews, observations, interventions) | Prior review, informed consent, personal data protection |
| **Personal Data Protection Act** | Collection, processing, and use of personal data | Notification obligation, purpose limitation, security maintenance |
| **Regulations Governing Human Trials** | Drug/medical device clinical trials | GCP compliance, subject insurance |

### 3.3 Application Process

```
1. Write research proposal
   ↓
2. Determine whether human subjects are involved
   ↓ (Involved)
3. Confirm review level (Exempt / Expedited / Full Board)
   ↓
4. Submit application to institutional IRB
   - Research proposal
   - Informed consent form
   - Questionnaire/interview guide
   - Researcher qualification documentation (CITI or equivalent training)
   ↓
5. IRB review (timeline: Expedited 2-4 weeks, Full Board 4-8 weeks)
   ↓
6. Research may only begin after receiving approval letter
   ↓
7. Periodic progress reports (typically annual)
   ↓
8. Final report
```

### 3.4 Online Research Ethics Review Platforms

| Platform | Description | URL |
|----------|-------------|-----|
| **AREC** (Academic Research Ethics Committee) | Multi-institutional joint ethics review committee | Institutional IRB websites |
| **Institutional IRB systems** | Online application systems within universities | Institutional R&D office websites |
| **CITI Program** | Online research ethics training course | citiprogram.org |
| **Taiwan Research Ethics Education Resource Center** | Research ethics education materials | Institutional teaching development centers |

---

## 4. Higher Education Research Quick Reference Table

| Research Scenario | Involves Human Subjects | Recommended Review Level | Notes |
|-------------------|------------------------|--------------------------|-------|
| MOE public statistical data analysis | No | Exempt | Already publicly available de-identified data |
| Institutional research (IR) data analysis | Depends | Exempt/Expedited | Depends on whether data is de-identified |
| Student learning outcome survey | Yes | Expedited | Anonymous surveys typically qualify for expedited review |
| Teacher interviews (general teaching experience) | Yes | Expedited | Non-sensitive topics |
| Teaching experiment (A/B teaching method comparison) | Yes | Expedited/Full Board | Depends on whether it affects students' grades/rights |
| Student mental health survey | Yes | Full Board | Sensitive topic |
| Vulnerable student population study | Yes | Full Board | Vulnerable population protection |
| Student learning portfolio analysis | Depends | Expedited | Contains identifiable information requiring expedited review |
| Classroom observation (no personal data recorded) | Yes | Exempt/Expedited | Public setting observation |
| Graduate career tracking survey | Yes | Expedited | Contains personal data requiring expedited review |
| HEEACT accreditation data analysis | Depends | Exempt/Expedited | Publicly available portions exempt from review |
| University faculty salary/labor conditions survey | Yes | Expedited/Full Board | May involve institutional power dynamics |

---

## 5. Informed Consent Form Elements

### 5.1 Required Items

- [ ] Research title
- [ ] Research institution and principal investigator name
- [ ] Research purpose
- [ ] Research procedures description (what subjects need to do, how long it takes)
- [ ] Potential risks and discomfort
- [ ] Potential benefits
- [ ] Confidentiality measures (how data is stored, who has access, retention period)
- [ ] Voluntary nature of participation (may withdraw at any time, no penalties)
- [ ] Researcher contact information
- [ ] IRB contact information (complaint channel)
- [ ] Subject signature and date field

### 5.2 Special Situations

| Situation | Additional Requirements |
|-----------|------------------------|
| **Online survey** | Electronic consent (clicking "I agree" constitutes consent); must state that IP addresses will not be recorded |
| **Audio/video recording** | Separate checkbox item: consent to audio/video recording |
| **Minors** | Legal guardian consent + subject assent |
| **Cross-national research** | Comply with local IRB requirements + Taiwan IRB requirements |
| **Indigenous research** | Community consent (tribal consent) + individual informed consent |

### 5.3 Informed Consent Form Template Structure

```
Research Participation Consent Form

1. Research Project Title: [                    ]
2. Principal Investigator: [      ] / Institution: [        ]
3. Research Purpose: [                              ]
4. Research Methods and Procedures:
    You will be invited to [specific description of what the subject will do],
    estimated to take [  ] minutes.
5. Potential Risks or Discomfort: [                        ]
6. Potential Benefits: [                              ]
7. Confidentiality Measures:
    Your data will be processed using codes; research results will only be
    presented in aggregate form, and your personal identity will not be
    disclosed. Data will be destroyed after [X] years.
8. Voluntary Nature of Participation:
    You are free to decide whether to participate in this study and may
    withdraw at any time without any adverse consequences.
9. Contact Information:
    Principal Investigator: [Name] [Phone] [Email]
    IRB Contact: [Institution Name] [Phone] [Email]

□ I have read and understood the above explanation and agree to participate
  in this research.

Subject Signature: __________ Date: __________
Researcher Signature: __________ Date: __________
```

---

## 6. Data De-identification and Privacy Protection

### 6.1 De-identification Strategies

| Strategy | Description | Applicable Scenario |
|----------|-------------|---------------------|
| **Anonymization** | Complete removal of all identifiable information, irreversible | Final data publication |
| **Pseudonymization** | Replace with codes, retain a linkage table | Need to track during research process |
| **Data generalization** | Convert precise values to ranges (e.g., age → age group) | Statistical analysis |
| **Data masking** | Hide partial information (e.g., partially masked email) | Data display |
| **k-anonymity** | Ensure each record is indistinguishable from at least k-1 other records | Dataset release |

### 6.2 Common Privacy Risks in Higher Education Research

- **Small sample identification**: Small departments may allow re-identification through descriptive statistics
- **Cross-referencing**: Combining multiple de-identified datasets may enable re-identification
- **Narrative identification**: Qualitative research quotations may reveal interviewee identity
- **Institutional identification**: Overly specific institutional characteristics may allow institution identification

### 6.3 Recommended Practices

- [ ] Remove direct identifiers (names, student IDs, national ID numbers)
- [ ] Assess indirect identifier risks (department + year + gender combinations may identify individuals)
- [ ] Check qualitative quotations: remove identifiable details
- [ ] Handle institutional names: decide whether to anonymize based on research needs
- [ ] Encrypt data storage with access controls
- [ ] Establish data retention and destruction timeline

---

## Quick Reference: Researcher Self-Check

Before starting research, answer the following questions:

1. [ ] Does my research collect, use, or analyze human-related data?
2. [ ] If yes, is the data completely de-identified and publicly available?
3. [ ] If not, which level of IRB review do I need to apply for?
4. [ ] Have I completed research ethics training (CITI or equivalent)?
5. [ ] Does my informed consent form include all required elements?
6. [ ] Do I have an appropriate data protection plan?
7. [ ] If vulnerable populations are involved, are there additional protective measures?
8. [ ] Has the IRB review timeline been incorporated into the research project timeline?
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-logical-fallacies-md"></a>

## SOURCE: skills/deep-research/references/logical_fallacies.md

<!-- SOURCE-CONTENT-BEGIN bytes=10614 -->
# Logical Fallacies Catalog — 30+ Fallacies for Research Review

## Purpose
Reference catalog of logical fallacies commonly encountered in research. Used by the devils_advocate_agent.

## Formal Fallacies (Invalid Logical Structure)

### 1. Affirming the Consequent
**Structure**: If P then Q; Q is true; therefore P is true.
**Example**: "If a university has high research funding, it has good outcomes. This university has good outcomes. Therefore, it must have high research funding."
**Problem**: Q can have multiple causes.

### 2. Denying the Antecedent
**Structure**: If P then Q; not P; therefore not Q.
**Example**: "If enrollment increases, revenue increases. Enrollment didn't increase. Therefore, revenue didn't increase."
**Problem**: Revenue can increase from other sources.

### 3. Undistributed Middle
**Structure**: All A are B; All C are B; therefore All A are C.
**Example**: "All successful programs use technology. Our program uses technology. Therefore, our program is successful."
**Problem**: B (technology use) is shared but doesn't link A and C.

### 4. False Dilemma / False Dichotomy
**Structure**: Either A or B; not A; therefore B.
**Example**: "Either we adopt online learning completely or maintain traditional methods."
**Problem**: Many hybrid options exist.

## Informal Fallacies

### Relevance Fallacies

### 5. Ad Hominem
**Description**: Attacking the person rather than the argument.
**Research Example**: "This study's conclusions are unreliable because the author works for a for-profit university."
**Correct Approach**: Evaluate the methodology and evidence, not the author's affiliation (though COI should be noted).

### 6. Appeal to Authority
**Description**: Accepting a claim solely because an authority figure endorses it.
**Research Example**: "Published in Nature, so the findings must be valid."
**Correct Approach**: Even prestigious journals publish flawed studies. Evaluate on merit.

### 7. Appeal to Tradition
**Description**: Arguing something is correct because it has always been done that way.
**Research Example**: "This metric has been used for 30 years, so it must be the best measure."
**Correct Approach**: Evaluate whether the metric is still valid in current context.

### 8. Appeal to Novelty
**Description**: Arguing something is better because it's new.
**Research Example**: "This new framework must be superior to the established one."
**Correct Approach**: Novelty doesn't equal improvement. Compare on evidence.

### 9. Appeal to Popularity (Bandwagon)
**Description**: Arguing something is true because many people believe it.
**Research Example**: "Most researchers in the field use this method, so it must be the best."
**Correct Approach**: Popularity doesn't validate methodology. Assess independently.

### 10. Red Herring
**Description**: Introducing an irrelevant topic to divert from the argument.
**Research Example**: Responding to criticism of methodology by discussing the importance of the topic.

### Evidence Fallacies

### 11. Cherry-Picking (Selection Bias)
**Description**: Selecting evidence that supports the conclusion while ignoring contradictory evidence.
**Research Example**: Citing 5 studies that support the hypothesis while omitting 12 that don't.
**Detection**: Compare cited sources against comprehensive search results.

### 12. Confirmation Bias
**Description**: Seeking, interpreting, and remembering information that confirms pre-existing beliefs.
**Research Example**: Designing search terms that are more likely to return supportive results.
**Detection**: Check if search strategy was neutral; look for actively sought disconfirming evidence.

### 13. Survivorship Bias
**Description**: Drawing conclusions only from "survivors" (successes), ignoring those that didn't survive.
**Research Example**: "All top-ranked universities implemented X" — ignoring universities that implemented X and didn't improve.
**Detection**: Ask "what about those that failed?"

### 14. Anecdotal Evidence
**Description**: Using individual stories as proof of a general claim.
**Research Example**: "One university tripled enrollment after rebranding, so rebranding drives enrollment."
**Detection**: Is this a systematic finding or an isolated case?

### 15. Hasty Generalization
**Description**: Drawing broad conclusions from insufficient evidence.
**Research Example**: "Three case studies from Taiwan show X, therefore this applies to all Asian universities."
**Detection**: Is the sample representative? Is the generalization proportionate to the evidence?

### Causal Fallacies

### 16. Post Hoc Ergo Propter Hoc
**Description**: Assuming that because B followed A, A caused B.
**Research Example**: "After implementing the new curriculum, graduation rates improved. Therefore the curriculum caused the improvement."
**Detection**: Were there confounders? Was there a control group?

### 17. Cum Hoc Ergo Propter Hoc (Correlation ≠ Causation)
**Description**: Assuming that correlation implies causation.
**Research Example**: "Universities with more international students have higher rankings, so international students cause higher rankings."
**Detection**: Is there a plausible mechanism? Could both be caused by a third factor?

### 18. Reverse Causation
**Description**: Getting cause and effect backwards.
**Research Example**: "Good facilities attract students" when actually "student fees fund better facilities."
**Detection**: Consider temporal order and alternative causal directions.

### 19. Ecological Fallacy
**Description**: Inferring individual-level conclusions from group-level data.
**Research Example**: "Countries with more education spending have higher GDP, so spending on education makes individuals richer."
**Detection**: Are individual-level and group-level relationships the same?

### 20. Simpson's Paradox
**Description**: A trend present in subgroups reverses when groups are combined.
**Research Example**: Department A and B both show improving retention, but the university overall shows declining retention (due to shifting enrollment proportions).
**Detection**: Always check disaggregated data alongside aggregate.

### Reasoning Fallacies

### 21. Straw Man
**Description**: Misrepresenting an opponent's argument to make it easier to attack.
**Research Example**: Critic says "this method has limitations" → Author responds "my critic says the entire study is worthless."
**Detection**: Does the refutation address the actual criticism?

### 22. Moving the Goalposts
**Description**: Changing the criteria for success after seeing results.
**Research Example**: Defining "program success" as enrollment growth, then shifting to "student satisfaction" when enrollment drops.
**Detection**: Were success criteria pre-defined?

### 23. Slippery Slope
**Description**: Arguing that one action will inevitably lead to an extreme outcome.
**Research Example**: "If we allow flexible admission criteria, academic standards will collapse entirely."
**Detection**: Is each step in the chain actually probable?

### 24. Circular Reasoning (Begging the Question)
**Description**: The conclusion is assumed in the premise.
**Research Example**: "This university is excellent because it is highly ranked, and it is highly ranked because it is excellent."
**Detection**: Does the argument depend on the truth of what it's trying to prove?

### 25. No True Scotsman
**Description**: Redefining a category to exclude counterexamples.
**Research Example**: "All quality assurance systems improve outcomes." "But system X didn't." "Well, X wasn't a true quality assurance system."
**Detection**: Is the definition being modified to fit the claim?

### 26. Equivocation
**Description**: Using a term in two different senses within the same argument.
**Research Example**: "Quality" used sometimes to mean "standards compliance" and sometimes to mean "student satisfaction."
**Detection**: Is the key term defined consistently throughout?

### Statistical Fallacies

### 27. Base Rate Neglect
**Description**: Ignoring the base rate (overall probability) in favor of specific information.
**Research Example**: "This program has a 90% satisfaction rate" — but the base rate for all programs is 88%.
**Detection**: Always compare against relevant base rates.

### 28. Regression to the Mean
**Description**: Extreme performances naturally tend back toward average on subsequent measurements.
**Research Example**: "Our intervention improved scores for the lowest-performing students" — they may have improved anyway.
**Detection**: Was there a control group? Were initial measurements extreme?

### 29. Texas Sharpshooter
**Description**: Finding a pattern in random data by focusing on clusters and ignoring misses.
**Research Example**: Running 20 statistical tests and reporting only the 1 that was significant.
**Detection**: Were hypotheses pre-registered? Was multiple testing corrected for?

### 30. Gambler's Fallacy
**Description**: Believing past random events influence future random events.
**Research Example**: "This institution has declined for 5 years, so it's due for improvement."
**Detection**: Is there a causal mechanism for reversal, or is this just pattern-seeking?

### 31. McNamara Fallacy (Quantitative Bias)
**Description**: Making decisions based solely on quantitative metrics while ignoring qualitative factors.
**Research Example**: Ranking universities only by publication counts, ignoring teaching quality and community impact.
**Detection**: Are important but hard-to-measure factors being excluded?

### 32. Goodhart's Law
**Description**: "When a measure becomes a target, it ceases to be a good measure."
**Research Example**: Universities gaming rankings metrics instead of genuinely improving quality.
**Detection**: Has the metric become a target? Are there signs of metric manipulation?

## Quick Reference: Detection Questions

| Ask This | Detects |
|----------|---------|
| "Does B have other possible causes?" | Post hoc, false cause |
| "What about the failures?" | Survivorship bias |
| "Is this sample representative?" | Hasty generalization |
| "Were criteria defined before results?" | Moving goalposts, Texas sharpshooter |
| "Is the key term used consistently?" | Equivocation |
| "What's the base rate?" | Base rate neglect |
| "What evidence was left out?" | Cherry-picking, confirmation bias |
| "Is this the actual argument being made?" | Straw man |
| "Can we distinguish correlation from causation?" | Cum hoc, ecological fallacy |
| "Are individual and group levels being mixed?" | Ecological fallacy, Simpson's paradox |
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-mode-selection-guide-md"></a>

## SOURCE: skills/deep-research/references/mode_selection_guide.md

<!-- SOURCE-CONTENT-BEGIN bytes=16593 -->
# Mode Selection Guide

## Overview

deep-research provides 7 modes suited to different research stages and needs. This guide helps users select the most appropriate mode.

---

## Decision Flowchart

```
User Input
    │
    ├── Have a clear research question?
    │   ├── Yes ──→ Have a text to review?
    │   │            ├── Yes ──→ review mode
    │   │            └── No ───→ Need PRISMA-compliant systematic review / meta-analysis?
    │   │                         ├── Yes ──→ systematic-review mode
    │   │                         └── No ───→ Need a complete report?
    │   │                                     ├── Yes ──→ full mode
    │   │                                     └── No ───→ Only need literature?
    │   │                                                 ├── Yes ──→ lit-review mode
    │   │                                                 └── No ───→ quick mode
    │   │
    │   └── No ──→ Want guided thinking?
    │              ├── Yes ──→ socratic mode
    │              └── No ───→ full mode
    │                          (Phase 1 interactive RQ clarification)
    │
    ├── Only need to verify specific facts?
    │   └── Yes ──→ fact-check mode
    │
    └── Not sure what you need?
        └── Describe your situation → System auto-recommends a mode
```

---

## Detailed Mode Information

### full mode (Complete Research)

| Item | Description |
|------|------|
| **Applicable Scenario** | Need to conduct complete academic research from scratch, producing a citable research report |
| **Not Applicable** | Just need a quick understanding of a topic; already have complete research and only need review; only need a bibliography |
| **Typical Users** | Graduate students preparing thesis proposals, policy researchers writing analysis reports, scholars exploring new fields |
| **Expected Output** | Complete APA 7.0 report (3,000-8,000 words), including literature review, methodology, analysis, conclusions |
| **Expected Dialogue Rounds** | 2-5 rounds (Phase 1 interaction + checkpoints) |
| **Agents Activated** | All 9 |
| **Time Required** | Longer; suitable for in-depth research without time pressure |

**Trigger Examples**:
```
"Research the impact of AI on higher education quality assurance"
"Deep research on the impact of declining birth rates on Taiwan's higher education"
"Research the current state of SDGs implementation in Asian universities"
```

---

### quick mode (Quick Research)

| Item | Description |
|------|------|
| **Applicable Scenario** | Need a quick understanding of a topic's core viewpoints and key literature, under time constraints |
| **Not Applicable** | Need complete methodology design; need in-depth critical analysis; need publication-quality reports |
| **Typical Users** | Administrative staff preparing meeting background materials, researchers needing a quick literature scan, preliminary exploration before writing a proposal |
| **Expected Output** | Research brief (500-1,500 words), including key summary, major literature, preliminary viewpoints |
| **Expected Dialogue Rounds** | 0-1 round (typically direct output) |
| **Agents Activated** | 4 (RQ + Biblio + Verification + Report) |
| **Time Required** | Shorter |

**Trigger Examples**:
```
"Quick research on blockchain in education"
"Quick research on the latest trends in educational technology"
```

---

### review mode (Text Review)

| Item | Description |
|------|------|
| **Applicable Scenario** | Already have a paper/report/draft that needs professional review and feedback |
| **Not Applicable** | No text to review yet; need to write research from scratch; need literature search |
| **Typical Users** | Graduate students who finished a paper and need peer review feedback, self-check before journal submission, peer review |
| **Expected Output** | Review report with Editorial Verdict (Accept/Revise/Reject), specific revision suggestions, ethics review |
| **Expected Dialogue Rounds** | 0-1 round |
| **Agents Activated** | 3 (Editor + Devil's Advocate + Ethics) |
| **Time Required** | Medium, depends on text length |

**Trigger Examples**:
```
"Review this paper"
"Help me review this paper's methodology"
"Check this manuscript before submission"
```

---

### lit-review mode (Literature Review)

| Item | Description |
|------|------|
| **Applicable Scenario** | Need systematic literature search and synthesis analysis, but not a complete research report |
| **Not Applicable** | Need a complete report with original analysis; only need to verify a few facts; need methodology design |
| **Typical Users** | Graduate students writing the literature review chapter of their thesis, research teams conducting systematic reviews, coursework assignments |
| **Expected Output** | Annotated bibliography + synthesis analysis (1,500-4,000 words), including thematic classification, evidence matrix, research gaps |
| **Expected Dialogue Rounds** | 1-2 rounds (confirm search scope) |
| **Agents Activated** | 3 (Biblio + Verification + Synthesis) |
| **Time Required** | Medium |

**Trigger Examples**:
```
"Literature review on SDGs in higher education"
"Literature review: the evolution of quality assurance in Taiwan's higher education"
"Systematic review of AI-assisted assessment"
```

---

### fact-check mode (Fact-Checking)

| Item | Description |
|------|------|
| **Applicable Scenario** | Need to verify the truthfulness and source quality of specific factual claims |
| **Not Applicable** | Need complete research analysis; need literature synthesis; need to produce a research report |
| **Typical Users** | Verifying data cited in meetings, checking factual accuracy in reports, checking policy claims |
| **Expected Output** | Verification report (300-800 words), including source rating, factual accuracy assessment, credibility determination |
| **Expected Dialogue Rounds** | 0 rounds (direct output) |
| **Agents Activated** | 1 (Source Verification) |
| **Time Required** | Shortest |

**Trigger Examples**:
```
"Fact-check these claims about Taiwan's university enrollment"
"Fact-check: Is the number of universities in Taiwan really declining?"
"Verify: 'OECD countries average 50% tertiary attainment rate'"
```

---

### socratic mode (Guided Research)

| Item | Description |
|------|------|
| **Applicable Scenario** | Interested in a topic but unsure how to start research; want to clarify thinking through dialogue; need research guidance |
| **Not Applicable** | Already have a clear research question and methodology; need quick report output; only need literature or fact-checking |
| **Typical Users** | Master's students encountering research for the first time, scholars transitioning research fields, doctoral students brainstorming research proposals |
| **Expected Output** | Research Plan Summary with extracted INSIGHTs, research question direction, methodology suggestions |
| **Expected Dialogue Rounds** | 8-15 rounds (multi-round dialogue is the core feature) |
| **Agents Activated** | 2-3 (socratic_mentor + research_question + devils_advocate as needed) |
| **Time Required** | Longer, but the focus is on the thinking process rather than output speed |

**Trigger Examples**:
```
"Guide my research on higher education topics"
"Guide my research on educational technology"
"Help me think through my thesis direction"
"Help me think through my research topic"
「引導我的研究：高教品保」
「幫我釐清我的研究方向」
「幫我想想，我對少子化議題有興趣但不確定要研究什麼」
「我有個模糊的想法，想找研究題目」
「帶我做研究」
```

---

### systematic-review mode (Systematic Review / Meta-Analysis)

| Item | Description |
|------|------|
| **Applicable Scenario** | Need a PRISMA-compliant systematic review, potentially with meta-analysis; evidence synthesis for policy or clinical decisions |
| **Not Applicable** | Exploratory research without a focused PICOS question; narrative literature review; quick overview of a topic |
| **Typical Users** | Researchers conducting Cochrane-style reviews, doctoral students writing systematic review chapters, policy teams synthesizing evidence for guidelines |
| **Expected Output** | PRISMA 2020 report: protocol, flow diagram, risk of bias assessment, forest plot data (if meta-analysis), GRADE evidence table, full reference list |
| **Expected Dialogue Rounds** | 3-6 rounds (protocol review + screening decisions + synthesis decisions) |
| **Agents Activated** | 8-10 (RQ + Architect + Biblio + Verification + RoB + Meta-Analysis/Synthesis + Report + Editor + Ethics) |
| **Time Required** | Longest; systematic reviews are inherently comprehensive |

**Trigger Examples**:
```
"Systematic review of AI-assisted assessment in higher education"
"Meta-analysis of the effect of active learning on STEM outcomes"
"PRISMA review of quality assurance frameworks in Asian universities"
"Evidence synthesis on the impact of accreditation on institutional improvement"
```

---

## Common Misselection Scenarios

| What the User Says | What They Probably Need | Recommended Mode | Reason |
|-----------|------------------|---------|------|
| "Help me do a complete literature review" | Complete report (with analysis and conclusions) | `full`, not `lit-review` | lit-review only produces bibliography and synthesis, no original analysis |
| "Quickly check the situation with X" | Fact-checking | `fact-check`, not `quick` | If only needing to verify specific facts, fact-check is more precise |
| "I want to research X" / 「我想研究X」(but can't articulate what they want to know) | Research thinking clarification | `socratic`, not `full` | full mode's Phase 1 also offers interaction, but socratic goes deeper |
| "Help me fix this paper" | Paper revision guidance | `review`, not `full` | Already has text, needs review not research from scratch |
| "I need APA-formatted references" | Reference formatting | `lit-review`, not `full` | If only a reference list and formatting is needed, no complete research required |
| "Help me think of a research topic" / 「幫我想研究題目」 | Research direction exploration | `socratic` | Best suited for users without a clear direction |
| "Systematic review of X" | PRISMA-compliant review | `systematic-review`, not `lit-review` | lit-review is a narrative survey; systematic-review follows PRISMA protocol with risk of bias and optional meta-analysis |
| "I need a meta-analysis" | Quantitative evidence synthesis | `systematic-review` | Meta-analysis is a component of systematic review, not a standalone mode |
| "Literature review for my thesis chapter" | Narrative literature review | `lit-review`, not `systematic-review` | Thesis lit review chapters are typically narrative, not PRISMA-compliant |

---

## Mode Transitions

### Common Transition Paths

```
socratic → full              Continue with complete research after Socratic completion
socratic → academic-paper    Write paper directly after Socratic completion
lit-review → full            Want complete analysis after literature review
lit-review → systematic-review  Need formal PRISMA compliance after initial lit survey
fact-check → full            Need deeper research after fact-checking
quick → full                 Worth going deeper after quick research
review → full                Need to re-research after review
systematic-review → academic-paper  Write up systematic review as a paper
```

### deep-research to academic-paper Mode Mapping

| deep-research Mode | Output | Maps to academic-paper Mode | Description |
|-------------------|------|--------------------------|------|
| `full` | Complete research report | `full` or `revision` | Research complete, proceed to paper writing |
| `socratic` | Research Plan Summary | `plan` | Research direction determined, plan paper structure |
| `lit-review` | Annotated bibliography + synthesis | `full` (literature-based) | Literature review complete, start writing paper |
| `quick` | Research brief | `plan` (needs expansion) | Preliminary exploration complete, plan full paper |
| `review` | Review report | Does not map | Review concluded, revise original paper |
| `fact-check` | Verification report | Does not map | Fact-checking concluded |
| `systematic-review` | PRISMA report + forest plots + GRADE table | `full` (systematic review paper) | Systematic review complete, write as a journal article |

### deep-research vs academic-paper-reviewer Mode Mapping

| deep-research `review` mode | academic-paper-reviewer |
|------------------------------|------------------------|
| 3 agents (Editor + DA + Ethics) | Dedicated paper review skill |
| Suitable for quality review of any text | Designed specifically for academic paper review process |
| Produces Editorial Verdict | Produces structured review comments |
| Recommended for: initial draft screening, non-academic texts | Recommended for: formal pre-submission review |

---

## Complete Academic Research Pipeline

```
Step 1: deep-research (socratic/full)
          ↓ Research Plan / Full Report
Step 2: academic-paper (plan/full)
          ↓ Paper draft
Step 3: academic-paper-reviewer (full/guided)
          ↓ Review comments
Step 4: academic-paper (revision)
          ↓ Revised paper
Step 5: [Repeat Steps 3-4 until passed]
          ↓ Final paper
```

---

## Mode Transition Matrix

Rules for switching between modes mid-research. Not all transitions are safe.

### Transition: quick → full
- **When**: Quick brief reveals the topic is more complex than expected
- **Reusable**: RQ Brief (as-is), initial keyword list
- **Must Redo**: Full literature search (quick only uses 5-8 sources), synthesis, verification
- **Quality Delta**: Full mode requires 15+ sources, 3+ databases, formal methodology design

### Transition: lit-review → full
- **When**: Literature review reveals a gap worth investigating with original methodology
- **Reusable**: Complete bibliography, synthesis themes, evidence gap analysis
- **Must Redo**: Research design (methodology_patterns), data collection plan, ethics review (if primary research)
- **Quality Delta**: Full mode adds original research design; lit-review is secondary analysis only

### Transition: socratic → full
- **When**: Socratic dialogue produces a well-formed RQ and user wants autonomous research
- **Reusable**: RQ Brief (with socratic_insights), accumulated INSIGHTs, scope definition
- **Must Redo**: Everything after RQ formulation (bibliography, synthesis, verification, report)
- **Quality Delta**: socratic mode only produces RQ Brief; full mode executes the complete pipeline

### Transition: fact-check → full
- **When**: Fact-checking reveals a claim is part of a larger contested topic worth researching
- **Reusable**: Verified/debunked claims, source verification results
- **Must Redo**: RQ formulation (reframe from verification to inquiry), full bibliography, synthesis
- **Quality Delta**: Fact-check is binary (true/false/mixed); full mode produces nuanced analysis

### Transition: lit-review → systematic-review
- **When**: Literature review reveals the topic warrants formal PRISMA compliance (e.g., for publication in a journal that requires it)
- **Reusable**: Initial keyword strategy, some identified sources (need re-screening)
- **Must Redo**: Protocol registration, formal inclusion/exclusion criteria, dual screening, risk of bias assessment, meta-analysis feasibility assessment
- **Quality Delta**: systematic-review requires protocol, RoB assessment, GRADE; lit-review has none of these

### Transition: systematic-review → academic-paper
- **When**: Systematic review is complete and user wants to write it up as a journal article
- **Reusable**: Everything — PRISMA report is essentially the paper draft
- **Must Redo**: Formatting to target journal requirements, abstract restructuring
- **Quality Delta**: Minimal — systematic review output is already structured per PRISMA 2020

### Prohibited Transitions
- **full → quick**: Cannot downgrade a full research to quick brief (loss of rigor)
- **Any → socratic**: Socratic mode is an entry point only; cannot transition into it mid-pipeline
- **paper-review → full**: Paper review evaluates existing work; full mode creates new research. These are fundamentally different tasks
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-openalex-api-protocol-md"></a>

## SOURCE: skills/deep-research/references/openalex_api_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=4194 -->
# OpenAlex API Verification Protocol

**Status**: v3.9.0
**Used by**: `bibliography_agent`, `migrate_literature_corpus_to_v3_9_0.py`
**API base**: `https://api.openalex.org`
**Rate limit**: 10 req/s (polite pool, with `mailto`), 1 req/s (anonymous)
**Polite email env var**: `OPENALEX_POLITE_EMAIL` (optional)

---

## Purpose

Provides a second bibliographic-index lookup for v3.9.0 cross-index triangulation per spec v3.9.0 §3.4. Mirrors the structure of `semantic_scholar_api_protocol.md` so adapters and migration tools can swap clients with minimal contract divergence. Used by `bibliography_agent` at ingest time and by the v3.9.0 migration tool for legacy backfill.

OpenAlex coverage complements Semantic Scholar for OA venues, monographs, and works without DOIs. Per Zhao et al. arXiv:2605.07723 §3, cross-index triangulation reduces false-positive rate vs. single-index detection (e.g., a paper unmatched in S2 but matched in OpenAlex is high-coverage-gap evidence, not fabrication evidence).

## Query Patterns

### Pattern 1: DOI Lookup with Title Cross-Check (primary when DOI is available)

```
GET /works/doi:{doi}?select=id,title,authorships,publication_year,doi,primary_location
```

**Matching rule (mirrors S2 `DOI_MISMATCH` pattern):** DOI lookup hits are gated by a Levenshtein 0.70 title cross-check. If the returned `title` field fails the threshold against the entry's canonical title, the DOI hit is rejected (DOI_MISMATCH — a known hallucination pattern where a fabricated DOI resolves to an unrelated paper). The caller falls through to title search.

### Pattern 2: Title Search (fallback when DOI absent or DOI_MISMATCH)

```
GET /works?search={url_encoded_title}&per-page=5&select=id,title,authorships,publication_year,doi,primary_location
```

**Matching rule:** Compute Levenshtein similarity between query title and each result title (case-insensitive, punctuation stripped) per `_normalize_title` in the client. Accept if similarity >= 0.70 (matching PaperOrchestra threshold). If multiple candidates pass, prefer matching-year tiebreaker, then highest similarity, then candidate with populated DOI.

## `openalex_unmatched` derivation

`true` if and only if:
- DOI present: DOI lookup either misses or fails the title cross-check, AND title search returns no match meeting threshold; OR
- DOI absent: title search alone returns no match meeting threshold.

The check fires only when `obtained_via != 'manual'` (manual entries are user-vouched per spec v3.9.0 §3.1).

## Degradation handling

| Condition | Action |
|---|---|
| HTTP 429 (rate limit) | Back off 2 seconds, retry up to 3 times. After exhaustion, raise `OpenAlexUnavailable`. |
| HTTP 5xx | Skip — raise `OpenAlexUnavailable` immediately. |
| Network timeout (30s default) | Skip — raise `OpenAlexUnavailable`. |
| `OpenAlexUnavailable` raised | Caller MUST omit `openalex_unmatched` from the entry (per spec v3.9.0 R-L3-2-C: absent ≠ false). Other indexes proceed independently. |

## v3.9.0 R-L3-2-D constraint

OpenAlex returns `primary_location.source.type` and other classification fields. **v3.9.0 ignores these.** They are not stored on the entry, not surfaced to the finalizer, and not used in any derivation. v3.10 will introduce `venue_type` as an explicit adapter-declared field; the OpenAlex-inferred classification is NOT a v3.10 acceptance provenance value because the k=3 case (where OpenAlex itself is unmatched) makes the classification untrusted.

## Client implementation

See `scripts/openalex_client.py`. The client class `OpenAlexClient` exposes `doi_lookup_with_title_check(doi, expected_title)` and `title_search(title, year=None)` methods. Both return `dict | None`. Both raise `OpenAlexUnavailable` on degradation per the table above. The optional `year` parameter in `title_search` enables a matching-year tiebreaker (+0.05 score bonus) mirroring the S2 client `_lookup_by_title` pattern.

## Cross-references

- Spec: `docs/design/2026-05-17-ars-v3.9.0-cross-index-triangulation-measurement-spec.md` §3.4
- Mirror template: `deep-research/references/semantic_scholar_api_protocol.md`
- Sibling protocol: `deep-research/references/crossref_api_protocol.md`
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-semantic-scholar-api-protocol-md"></a>

## SOURCE: skills/deep-research/references/semantic_scholar_api_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=5159 -->
# Semantic Scholar API Verification Protocol

**Status**: v3.3
**Used by**: `source_verification_agent`, `bibliography_agent`, `integrity_verification_agent`
**API base**: `https://api.semanticscholar.org/graph/v1`
**Rate limit**: 1 request/second (unauthenticated), 10 requests/second (with API key)
**API key env var**: `S2_API_KEY` (optional; graceful degradation if unset)

---

## Purpose

Provides programmatic verification of reference existence and bibliographic accuracy using the Semantic Scholar Academic Graph API. This supplements (not replaces) WebSearch-based verification by adding a structured, API-grounded check that returns machine-readable metadata.

PaperOrchestra (Song et al., 2026) demonstrated that a two-phase citation pipeline — (1) broad discovery via web search, (2) sequential verification via Semantic Scholar API — achieves significantly higher citation coverage (P0 Recall +2-6%, P1 Recall +12-14% over baselines). ARS adopts the verification phase as an additional tier in the existing multi-tier verification strategy.

---

## Query Patterns

### Pattern 1: Title Search (primary)

```
GET /paper/search?query={url_encoded_title}&limit=5&fields=title,authors,year,externalIds,venue,publicationDate
```

**Matching rule**: Compute Levenshtein similarity between query title and each result title (case-insensitive, stripped of punctuation). Accept if similarity >= 0.70 (matching PaperOrchestra's threshold). If multiple results >= 0.70, prefer the one with matching year.

### Pattern 2: DOI Lookup (when DOI is available)

```
GET /paper/DOI:{doi}?fields=title,authors,year,externalIds,venue,publicationDate,citationCount
```

**Matching rule**: DOI match is exact. Cross-check that returned title matches the reference title (Levenshtein >= 0.70). If title mismatch despite DOI match, flag as `DOI_MISMATCH` — a known hallucination pattern where a fabricated DOI resolves to an unrelated paper.

### Pattern 3: Semantic Scholar ID Lookup (for re-verification)

```
GET /paper/{paperId}?fields=title,authors,year,externalIds,venue,publicationDate,citationCount
```

Used when re-verifying a reference that was previously resolved to a Semantic Scholar ID (stored in the bibliography's `semantic_scholar_id` field).

---

## Verification Tiers (Updated with S2 API)

| Tier | Method | Coverage | Purpose |
|------|--------|----------|---------|
| **Tier 0 (NEW)** | Semantic Scholar API | 100% of references | Programmatic existence check + metadata extraction |
| Tier 1 | DOI resolution | 100% of DOI-bearing refs | URL-level existence check |
| Tier 2 | WebSearch spot-check | 50% of sources | Human-readable verification |

**Execution order**: Tier 0 first (batch, 1 req/sec). References that PASS Tier 0 skip Tier 2 unless flagged for other reasons. References that FAIL Tier 0 proceed to Tier 1 + Tier 2 for manual investigation.

---

## Response Handling

### On successful match

Record the following in the reference's verification audit trail:
- `semantic_scholar_id`: the S2 paper ID (e.g., `"649def34f8be52c8b66281af98ae884c09aef38b"`)
- `s2_title`: returned title
- `s2_authors`: returned author list
- `s2_year`: returned year
- `s2_venue`: returned venue
- `s2_citation_count`: citation count (informational)
- `match_score`: Levenshtein similarity score
- `verification_method`: `"s2_title_search"` or `"s2_doi_lookup"`

### On no match

- If 0 results with Levenshtein >= 0.70: classify as `S2_NOT_FOUND`
- `S2_NOT_FOUND` does NOT automatically mean fabrication — the paper may exist but not be indexed in Semantic Scholar (e.g., very recent, non-English, grey literature)
- Proceed to Tier 1 (DOI) and Tier 2 (WebSearch) for further investigation
- If ALL tiers fail: classify as `NOT_FOUND` per existing protocol

### On API failure

- HTTP 429 (rate limit): back off 2 seconds, retry up to 3 times
- HTTP 5xx: skip S2 for this reference, proceed to Tier 1
- Network error: skip S2 entirely for remaining batch, log `[S2-API-UNAVAILABLE]`
- **Never block the pipeline on S2 API failure** — graceful degradation to existing WebSearch-only verification

---

## Deduplication via S2 ID

When two references resolve to the same `semantic_scholar_id`, flag as duplicate. The `bibliography_agent` uses this for deduplication during search (matching PaperOrchestra's approach of deduplicating via Semantic Scholar IDs).

---

## Cost and Performance

- **API calls per paper**: ~30-80 (one per reference, typical paper has 30-80 references)
- **Time**: At 1 req/sec (unauthenticated), 30-80 seconds for a full paper. With API key (10 req/sec): 3-8 seconds
- **Cost**: Free (Semantic Scholar API is free for academic use)
- **Recommendation**: Set `S2_API_KEY` for faster verification. Obtain from https://www.semanticscholar.org/product/api#api-key

---

## References

- Song, Y., Song, Y., Pfister, T., & Yoon, J. (2026). PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing. *arXiv preprint arXiv:2604.05018*. — Section 4 Step 3 (Literature Review Agent), Appendix D.3 (Citation Verification).
- Semantic Scholar API documentation: https://api.semanticscholar.org/
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-socratic-mode-protocol-md"></a>

## SOURCE: skills/deep-research/references/socratic_mode_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=4194 -->
# Socratic Mode: Guided Research Dialogue — Full Protocol

## Core Principle

From the perspective of a Q1 international journal editor-in-chief, guide users to clarify their research questions through Socratic questioning. **IRON RULE**: Never give direct answers; instead, use follow-up questions to help users think through the issues themselves.

See `agents/socratic_mentor_agent.md` for the detailed agent definition.
See `references/socratic_questioning_framework.md` for the questioning framework.

## 5-Layer Dialogue Flow

```
User: "Guide my research on [topic]"
     |
=== Layer 1: PROBLEM FRAMING (corresponds to first half of Phase 1) ===
     |
     +-> [socratic_mentor_agent] -> Follow-up on research motivation and problem definition
         [research_question_agent] -> Provide FINER guidance framework
         - "What is the question you truly want to answer?"
         - "Why does this question matter? To whom?"
         - "If your research succeeds, how would the world be different?"
         Extract [INSIGHT: ...] each round
         At least 2 rounds of dialogue before entering Layer 2
     |
=== Layer 2: METHODOLOGY REFLECTION (corresponds to second half of Phase 1) ===
     |
     +-> [socratic_mentor_agent] -> Follow-up on rationale for methodology choices
         [devils_advocate_agent] -> Challenge methodology assumptions at end of Layer 2
         - "How do you plan to answer this question? Why this approach?"
         - "Is there a completely different method that could also answer your question?"
         - "What is the biggest weakness of your method?"
         At least 2 rounds of dialogue before entering Layer 3
     |
=== Layer 3: EVIDENCE DESIGN (corresponds to Phase 2-3) ===
     |
     +-> [socratic_mentor_agent] -> Follow-up on evidence strategy
         - "What kind of evidence would convince you of your conclusion?"
         - "What evidence would make you change your conclusion?"
         - "What are you most worried about not finding?"
         At least 2 rounds of dialogue before entering Layer 4
     |
=== Layer 4: CRITICAL SELF-EXAMINATION (corresponds to Phase 5) ===
     |
     +-> [socratic_mentor_agent] -> Follow-up on limitations and risks
         [devils_advocate_agent] -> Challenge conclusion assumptions
         - "What does your research assume? What if those assumptions don't hold?"
         - "How would someone with the opposite view refute you?"
         - "What negative impact could your research have?"
         At least 2 rounds of dialogue before entering Layer 5
     |
=== Layer 5: SIGNIFICANCE & CONTRIBUTION (conclusion) ===
     |
     +-> [socratic_mentor_agent] -> Follow-up on "so what?"
         - "Why should readers care about your findings?"
         - "What aspects of our understanding of this issue does your research change?"
         At least 1 round of dialogue
     |
     +-> Compile all [INSIGHT]s into Research Plan Summary
         Can directly hand off to academic-paper (plan mode)
```

## Dialogue Management Rules

- At least 2 rounds of dialogue per layer before moving to the next (Layer 5 requires at least 1)
- Users can request to skip to the next layer at any time
- Mentor responses limited to 200-400 words
- If no convergence after 10 rounds -> suggest switching to `full` mode (see Failure Paths F6)
- If dialogue exceeds 15 rounds -> automatically compile INSIGHTs and end
- If user requests direct answers -> gently decline, explain the value of guided learning

## Reading Probe (opt-in, goal-oriented only)

When `ARS_SOCRATIC_READING_PROBE=1`, the Mentor runs a one-time honesty probe at the Layer 2 → Layer 3 transition, but only for goal-oriented sessions where the user has already cited a specific paper.

The probe asks the user to paraphrase one passage from that paper. The user may decline; the decline is logged without penalty. The probe is not a gate — it records user self-report only. It does not change convergence signals, intent classification, or any scoring.

Default is OFF. Exploratory sessions never probe. See `agents/socratic_mentor_agent.md` §"Optional Reading Probe Layer" for the full trigger, wording, and logging rules.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-deep-research-references-socratic-questioning-framework-md"></a>

## SOURCE: skills/deep-research/references/socratic_questioning_framework.md

<!-- SOURCE-CONTENT-BEGIN bytes=11706 -->
# Socratic Questioning Framework — Academic Research Application

## Overview

Socratic Questioning originates from the dialogue-based teaching method of the ancient Greek philosopher Socrates. Its core is not about imparting knowledge, but about helping the interlocutor discover blind spots, contradictions, and deep-seated assumptions in their own thinking through systematic questioning. This framework applies this method to the context of academic research guidance.

---

## 6 Core Question Types

### Type 1: Clarification Questions

**Purpose**: Ensure the interlocutor truly understands the concepts they are using

| Question Pattern | Usage Context |
|---------|---------|
| What do you mean by "X"? | When the user uses vague or polysemous terms |
| Can you give a specific example? | When abstract descriptions need concretization |
| Can you put it another way? | To confirm mutual understanding |
| How is this different from Y? | To distinguish similar concepts |
| What does X include? What does it exclude? | To define scope |

### Type 2: Probing Assumptions

**Purpose**: Reveal hidden premises and assumptions

| Question Pattern | Usage Context |
|---------|---------|
| What are you assuming? | When the user's reasoning skips certain premises |
| Is this assumption justified? | When the reasonableness of a premise needs verification |
| What if this assumption doesn't hold? | To test the robustness of reasoning |
| Why do you take this for granted? | When the user is overconfident about a premise |
| Does anyone disagree with this premise? Why? | To introduce different perspectives |

### Type 3: Probing Rationale and Evidence

**Purpose**: Probe the basis and evidence foundation of reasoning

| Question Pattern | Usage Context |
|---------|---------|
| What is your evidence? | When the user makes unsupported assertions |
| How do you know this is true? | When distinguishing facts from opinions is needed |
| What other evidence supports or contradicts this? | To broaden the evidence horizon |
| Is this evidence sufficient? | To evaluate the match between evidence and conclusions |
| How would you respond to doubts about data reliability? | To test the solidity of evidence |

### Type 4: Questioning Viewpoints and Perspectives

**Purpose**: Introduce alternative viewpoints to break the limitations of a single perspective

| Question Pattern | Usage Context |
|---------|---------|
| What would this look like from another perspective? | When the user is stuck in a single viewpoint |
| What would someone who disagrees say? | To introduce opposing thinking |
| If you were X (a different stakeholder), how would you see this? | Multi-stakeholder analysis |
| Why might others see this differently? | To understand the sources of viewpoint differences |
| Does another discipline frame this phenomenon differently? | Interdisciplinary thinking |

### Type 5: Probing Implications and Consequences

**Purpose**: Explore the logical consequences and practical impacts of reasoning

| Question Pattern | Usage Context |
|---------|---------|
| If this conclusion is correct, what does it imply? | To trace logical implications |
| What are the practical consequences? | To connect theory to practice |
| What are the best and worst case scenarios? | To assess impact range |
| Who benefits? Who is harmed? | Ethical dimension thinking |
| Where does this trend lead in the long run? | Extended thinking |

### Type 6: Questioning the Question

**Purpose**: Examine whether the question itself is worth asking and whether the framing is correct

| Question Pattern | Usage Context |
|---------|---------|
| Why does this question matter? | To return to research motivation |
| Is there a better way to frame this question? | To optimize question formulation |
| What is the question behind this question? | To excavate deeper concerns |
| What if we're asking the wrong question? | Fundamental reflection |
| What preconditions must exist to answer this? | To examine answerability |

---

## Academic Research Question Banks

### Research Question Clarification

1. Are you asking a "whether" question, a "how much" question, or a "why" question?
2. Can you state your research question in a single sentence? If it takes more than one sentence, it may need splitting.
3. If you could run only one statistical test or interview one person, what would it be?
4. Does your question imply an expected answer? If so, is that a question or a hypothesis?
5. Five years from now, what do you hope this research will have answered?

### Methodology Probing

1. Did you choose this method because it best fits your question, or because you're most familiar with it?
2. What alternative explanations can your design rule out? What can't it?
3. Would your conclusions hold with half your expected sample size?
4. Is your instrument actually measuring what you intend to measure? (validity)
5. Would another researcher get the same results using the same method? (reliability)

### Literature Positioning

1. What is the dominant narrative in this field? Are you supporting or challenging it?
2. If your research is a conversation, who are you responding to?
3. Are there decade-old studies now considered wrong? What does that tell you?
4. Do your cited sources share a common blind spot?
5. Have you deliberately searched for literature that contradicts your view?

### Analytical Reasoning

1. Is what you observe correlation or causation? How do you distinguish them?
2. Where does your analytical framework come from? Has it been criticized?
3. If you gave your data to another researcher without your hypothesis, what would they see?
4. Are there outliers that don't fit your theory? How do you handle them?
5. Have you tried to disprove your own hypothesis?

### Conclusions and Limitations

1. Does your conclusion go beyond what your evidence supports?
2. To what extent can your findings be generalized? Where do they not apply?
3. If you had to add a section "I might be wrong because...", what would it say?
4. Is your limitations section a genuine reflection or a formality?
5. What would future researchers need to verify or refute your conclusions?

### Contribution and Significance

1. If your research were never published, what would academia and practice lose?
2. Can you explain why your research matters in three sentences to a non-expert?
3. Is your research "filling a gap" or "changing understanding"? These differ in value.
4. Will your research still be cited in ten years? Why?
5. How does your research connect to the most pressing issues in society today?

---

## Questioning Strategies

### Strategy 1: Funnel Strategy
From open to focused, progressively narrowing scope.

```
Q1: "What aspects of higher education interest you?" (Open)
Q2: "You mentioned quality assurance — what part of QA makes you most curious?" (Focused)
Q3: "Where do you think the problem lies with accreditation indicator design?" (More focused)
Q4: "So what you're asking is: can current accreditation indicators truly reflect teaching quality?" (Precise)
```

### Strategy 2: Mirror Strategy
Restate the user's words, then follow up.

```
User: "I think declining birth rates will cause many private universities to close down"
Mentor: "You think there's a direct causal relationship between declining birth rates and private university closures. Do you think there might be other mediating factors in this causal chain? For example, are there some private universities that have actually grown against the trend despite declining birth rates?"
```

### Strategy 3: Counterfactual Strategy
Imagine the opposite situation to test reasoning.

```
User: "Online learning has improved learning outcomes"
Mentor: "If a university that completely didn't adopt online learning had better student grades and satisfaction than those that did, how would you explain that? Would this change your research question?"
```

### Strategy 4: Analogy Strategy
Use similar problems from other domains to inspire thinking.

```
User: "I want to research the effectiveness of university mergers"
Mentor: "Research on corporate mergers and acquisitions shows that most M&A actually damages rather than improves performance in the short term. Do you think university mergers might have a similar pattern? What are the key differences between university mergers and corporate M&A?"
```

### Strategy 5: Strategic Silence
Sometimes the best follow-up is waiting, giving the user space to think.

```
User: "I think... maybe... actually I'm not sure"
Mentor: "Take your time. You just said 'actually I'm not sure' — what exactly are you unsure about? Is it the question itself, or your position on the question?"
```

---

## Design Alignment with AI Learning Guidance Engines

The dialogue design principles of this framework are consistent with AI learning guidance engines:

| Design Principle | Socratic Mentor | ai-study-learn-engine |
|---------|-----------------|----------------------|
| Brief feedback | 1-2 sentences of affirmation/restatement | 1-2 sentences of indicator performance feedback |
| Data citation | Hint at literature directions | Cite specific indicator data |
| Focused follow-up | 1-2 precise questions | 1 learning guidance question |
| Response length limit | 200-400 words | 200-300 words |
| Insight extraction | [INSIGHT: ...] | [LEARNING: ...] |
| Convergence mechanism | 15-round limit | 10-round limit |

This consistency ensures a coherent experience when users switch between different tools.

---

## SCR Overlay Protocol

The SCR (State-Challenge-Reflect) overlay works ON TOP of existing Socratic questioning. It does not replace any existing mechanism; it adds a commitment-tracking layer that deepens the learning impact.

### Mapping to Socratic Functions

| SCR Phase | Socratic Function | Timing | Purpose |
|-----------|------------------|--------|---------|
| **State** (表態) | Clarifying + Probing | Before presenting data/evidence | Collect user's prediction or self-assessment |
| **Challenge** (挑戰) | Structuring + Challenging | After commitment collected | Present information that tests the commitment |
| **Reflect** (反思) | Probing + Structuring | After divergence revealed | Guide user to self-explain the gap |

### Design Constraints
1. The user never sees the words "SCR", "commitment gate", or "divergence reveal"
2. The experience feels like a natural Socratic dialogue that happens to ask for predictions before showing data
3. The mechanism is invisible; the learning is visible
4. Commitment questions should feel like natural warm-up questions, not formal assessments
5. If the user's commitment turns out to be accurate, acknowledge it and move on — no need to force divergence where none exists

### Integration with Convergence Signals
The new S5/C5 (Self-Calibration) signal tracks whether the user's commitments become more accurate over the dialogue. This signal:
- Strengthens convergence when present (user is both understanding AND self-aware)
- Does NOT block convergence when absent (understanding can exist without perfect self-calibration)
- Provides valuable coaching feedback at dialogue end

---

## References

- Paul, R., & Elder, L. (2007). *Critical Thinking: The Art of Socratic Questioning*. Journal of Developmental Education, 31(1), 36-37.
- Overholser, J. C. (1993). Elements of the Socratic method: I. Systematic questioning. Psychotherapy, 30(1), 67-74.
- Burbules, N. C. (1993). *Dialogue in Teaching: Theory and Practice*. Teachers College Press.
- Copeland, M. (2005). *Socratic Circles: Fostering Critical and Creative Thinking in Middle and High School*. Stenhouse Publishers.
<!-- SOURCE-CONTENT-END -->
