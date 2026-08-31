<a id="source-skills-academic-pipeline-templates-pipeline-status-template-md"></a>

## SOURCE: skills/academic-pipeline/templates/pipeline_status_template.md

<!-- SOURCE-CONTENT-BEGIN bytes=3813 -->
# Pipeline Status Dashboard Template

This template defines the output format for the Progress Dashboard. Switch between language versions based on user language.

---

## English Version

```
+=========================================+
|   Academic Pipeline Status              |
+=========================================+
| Topic: {topic}                          |
+-----------------------------------------+

  Stage 1 RESEARCH    [{status_icon}] {status_text}
    {mode_line}
    {outputs_line}

  Stage 2 WRITE       [{status_icon}] {status_text}
    {mode_line}
    {outputs_line}

  Stage 3 REVIEW      [{status_icon}] {status_text}
    {mode_line}
    {decision_line}

  Stage 4 REVISE      [{status_icon}] {status_text}
    {revision_round_line}
    {addressed_line}

  Stage 3' RE-REVIEW  [{status_icon}] {status_text}
    {loop_count_line}

  Stage 5 FINALIZE    [{status_icon}] {status_text}
    {format_line}

+-----------------------------------------+
| Materials:                              |
|   [{icon}] RQ Brief                     |
|   [{icon}] Methodology Blueprint        |
|   [{icon}] Bibliography                 |
|   [{icon}] Synthesis Report             |
|   [{icon}] Paper Draft                  |
|   [{icon}] Review Reports               |
|   [{icon}] Revision Roadmap             |
|   [{icon}] Revised Draft                |
|   [{icon}] Response to Reviewers        |
|   [{icon}] Final Paper                  |
+-----------------------------------------+
| Revision History:                       |
|   {revision_history}                    |
+-----------------------------------------+
| Next Step: {next_step_suggestion}       |
+=========================================+
```

---

## Field Definitions

### status_icon

| Status | Icon |
|--------|------|
| completed | `v` |
| in_progress | `..` |
| pending | ` ` (space) |
| skipped | `--` |

### status_text

| Status | Text |
|--------|------|
| completed | Completed |
| in_progress | In Progress |
| pending | Pending |
| skipped | Skipped |

### mode_line

Format: `Mode: {mode_name}`
- Only displayed when status is completed or in_progress
- If mode switched (e.g., plan -> full), display the full path

### outputs_line

Format: `Outputs: {output_1}, {output_2}, ...`
- Only displayed when status is completed
- List all deliverables for that stage

### decision_line

Format: `Decision: {Accept/Minor Revision/Major Revision/Reject}`
- Only displayed when Stage 3 or Stage 3' is completed

### revision_round_line

Format: `Revision Round: {current}/{max}`
- Only displayed when Stage 4 is in_progress

### addressed_line

Format: `Addressed: {count}/{total} required revisions`
- Only displayed when Stage 4 is in_progress

### loop_count_line

Format: `Loop: {count}/2`
- Only displayed for Stage 3'

### material icon

| Status | Icon |
|--------|------|
| available | `v` |
| missing | ` ` (space) |

### revision_history

One line per round:
```
Round {n}: {decision} | {addressed}/{total} items addressed
  Pending: {pending_items_summary}
```

If no revision history, display "(No revision history yet)".

### next_step_suggestion

Auto-generated suggestion based on current state:
- Stage 1 completed: "Recommend proceeding to Stage 2 (WRITE) using {recommended_mode} mode"
- Stage 3 completed (Major): "Need to enter Stage 4 (REVISE), {N} required items"
- Stage 4 completed: "Recommend proceeding to Stage 3' (RE-REVIEW) to confirm revision quality"
- Stage 3' completed (Accept): "Congratulations! Proceed to Stage 5 (FINALIZE) to produce final version"
- Pipeline completed: "Pipeline complete! Final paper is ready."

---

## Simplified Version (Auto-appended after stage completion)

One-line progress bar:

```
Pipeline: [v]RESEARCH -> [v]WRITE -> [..]REVIEW -> [ ]REVISE -> [ ]FINALIZE
```
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-examples-full-pipeline-example-md"></a>

## SOURCE: skills/academic-pipeline/examples/full_pipeline_example.md

<!-- SOURCE-CONTENT-BEGIN bytes=17187 -->
# Example: Full Pipeline Conversation Log

## Scenario Description

**User type**: Master's student in Education, first time writing an academic paper
**Topic**: The impact of declining birthrate on enrollment strategies of private universities in Taiwan
**Goal**: Complete a submission-ready IMRaD paper
**Language**: Traditional Chinese (bilingual abstract)

---

## User Input

```
I want to write a paper on the impact of declining birthrate on enrollment
strategies of private universities in Taiwan. Help me from start to finish.
This is my first time writing an academic paper and I'm not sure about the process.
```

---

## Pipeline Execution Log

### Orchestrator: Launch Detection

```
Detection results:
- Materials: None (starting from scratch)
- Goal: Full workflow
- Entry point: Stage 1 (RESEARCH)
- User preference: First time writing a paper --> recommend guided mode

Recommended Pipeline Configuration:

  Stage 1 RESEARCH: socratic -- First time doing research, Socratic guidance to help you think through
  Stage 2 WRITE:    plan     -- Chapter-by-chapter guidance to plan your paper structure
  Stage 3 REVIEW:   full     -- Complete 4-person review, simulating real submission experience
  Stage 4 REVISE:   revision -- Item-by-item revision based on review comments
  Stage 5 FINALIZE: format   -- Convert to your desired format (LaTeX/DOCX via Pandoc/PDF)

You can adjust any stage's mode at any time. Ready to begin?
```

**User**: Yes, let's start!

---

### Stage 1: RESEARCH (socratic mode)

```
Entering Stage 1 (RESEARCH) -- using deep-research socratic mode

Loading deep-research SKILL.md...
Launching socratic_mentor_agent...
```

**Socratic Mentor**: You mentioned "the impact of declining birthrate on private university enrollment strategies." Before we begin, I'd like to understand a few things:

1. Why are you interested in this topic? Did you observe some phenomenon?
2. When you say "enrollment strategies," what kind are you thinking of? Online marketing? Scholarships? Program adjustments? Or all of the above?

**User**: I've noticed that many private universities are starting to do things they wouldn't have done before, like hosting information sessions at high schools, lowering admission thresholds, and opening many new programs. I want to know if these strategies actually work.

**Socratic Mentor**: Great observation. You mentioned three types of strategies: outreach activities, admission standard adjustments, and new program establishment.

Let me follow up: What do you mean by "actually work"? Higher freshmen enrollment rate? Maintaining student quality? The school surviving? Different definitions of "working" lead to completely different research questions.

**User**: I think the most important thing is the freshmen enrollment rate — if you can't recruit students, nothing else matters.

**Socratic Mentor**:
[INSIGHT: Research focus = actual effectiveness of enrollment strategies on freshmen enrollment rate]

Good. Let's go deeper. If your research conclusion is "certain strategies can indeed improve enrollment rates," who would find this useful? Private university presidents? Ministry of Education policymakers? Or parents of high school students?

Different target audiences will significantly change how you write your paper.

**User**: Primarily for university administrators, so they know which strategies are worth investing in.

*(Socratic dialogue continues for 8 rounds, covering 5 Layers...)*

**Socratic Mentor -- Final Summary**:

```
Research Plan Summary

Research question:
  Under the declining birthrate trend, what is the impact of enrollment
  strategies (outreach activities, admission standard adjustments, new
  program establishment) adopted by private universities in Taiwan on
  freshmen enrollment rates? Which strategies are most effective for
  different types of private universities (general/technical-vocational)?

Methodology:
  Mixed Methods
  - Quantitative: Ministry of Education open data analysis (academic years 109-113)
  - Qualitative: In-depth interviews with enrollment directors at 3-5 private universities

Target journal level: TSSCI

Extracted INSIGHTs (8):
  [INSIGHT 1] Research focus = actual effectiveness of enrollment strategies on freshmen enrollment rate
  [INSIGHT 2] Target audience = university administrators
  [INSIGHT 3] Three strategy dimensions: outreach, admission standards, program adjustment
  [INSIGHT 4] Need control variables: school geographic location, school size, tuition level
  [INSIGHT 5] Method choice: mixed methods (quantitative trends + qualitative context)
  [INSIGHT 6] Quantitative data source: MOE University Information Disclosure Platform
  [INSIGHT 7] Major limitation: cannot obtain individual schools' marketing budget data
  [INSIGHT 8] Research contribution: provide evidence-based strategy recommendations for resource-limited private universities
```

Then bibliography_agent executes literature search, source_verification_agent verifies sources...

**Stage 1 Deliverables:**
- RQ Brief (with FINER scoring)
- Methodology Blueprint (mixed methods design)
- Annotated Bibliography (22 references, APA 7.0)
- Synthesis Report (thematic synthesis + research gaps)

---

### Orchestrator: Stage 1 --> 2 Transition

```
Stage 1 (RESEARCH) Complete!

Deliverables:
- RQ Brief: Focused on three enrollment strategies' impact on enrollment rates at private universities
- Methodology Blueprint: Mixed methods (quantitative MOE data + qualitative interviews)
- Annotated Bibliography: 22 references (17 Chinese + 5 English)
- Synthesis Report: Identified 3 research gaps

Next step is Stage 2 (WRITE).
Since this is your first time writing a paper, I recommend plan mode (chapter-by-chapter guidance).
After completing the outline, we'll switch to full mode to produce the complete draft.

Continue?

Progress: [v]Research -> [..]Writing -> [ ]Review -> [ ]Revision -> [ ]Finalization
```

**User**: Continue!

---

### Stage 2: WRITE (plan --> full mode)

```
Entering Stage 2 (WRITE) -- using academic-paper plan mode

Loading academic-paper SKILL.md...
handoff materials: RQ Brief + Bibliography + Synthesis
intake_agent auto-detected deep-research output, skipping redundant Phase 0 questions
Launching socratic_mentor_agent (plan mode)...
```

**Plan Mode Mentor**: I've reviewed your Research Plan Summary. The research question is clear. Let's plan the paper chapter by chapter. Starting with the Introduction.

What sense of urgency do you want the reader to feel? In other words, why should the reader read this paper right now?

**User**: Because the declining birthrate is already happening — many universities might close within 5 years.

**Plan Mode Mentor**: Good. Your Introduction opening could use a specific number to convey urgency. Do you know how many private universities have closed or suspended enrollment in the past 5 years?

*(Plan mode dialogue continues for 12 rounds, covering 6 chapters...)*

**Plan Mode Complete --> Switch to full mode**

```
Chapter Plan complete. Switching to full mode to write the complete draft.

academic-paper draft_writer_agent writing based on Chapter Plan...
citation_compliance_agent verifying citations...
abstract_bilingual_agent writing bilingual abstract...
```

**Stage 2 Deliverables:**
- Paper Draft (5,200 words, IMRaD structure, with bilingual abstract)

---

### Orchestrator: Stage 2 --> 3 Transition

```
Stage 2 (WRITE) Complete!

Deliverables:
- Paper Draft: 5,200-word IMRaD paper
  - Abstract (Chinese 420 words + English 230 words)
  - Introduction: Research background and problem statement
  - Literature Review: Three themes (birthrate trends, enrollment strategy classification, effectiveness evaluation)
  - Methodology: Mixed methods design
  - Results: Quantitative findings + qualitative themes
  - Discussion: Strategy effectiveness comparison + policy recommendations
  - References: 22 entries (APA 7.0)

Next step is Stage 3 (REVIEW).
Using full mode, simulating a complete review process with 4 reviewers.
After review, an Editorial Decision and Revision Roadmap will be produced.

Continue?

Progress: [v]Research -> [v]Writing -> [..]Review -> [ ]Revision -> [ ]Finalization
```

**User**: OK, review it for me.

---

### Stage 3: REVIEW (full mode)

```
Entering Stage 3 (REVIEW) -- using academic-paper-reviewer full mode

Loading academic-paper-reviewer SKILL.md...
Passing Paper Draft to reviewer...
field_analyst_agent analyzing paper domain...
```

**Field Analysis Results:**
```
Paper domain: Education Policy / Higher Education Management
Research paradigm: Pragmatism (mixed methods)
Method type: Quantitative (secondary data analysis) + Qualitative (interviews)

Reviewer Configuration:
  EIC:        Journal of Education Policy Editor, specializing in economics of education
  Reviewer 1: Quantitative methods expert, specializing in education statistics and large database analysis
  Reviewer 2: Higher education management scholar, specializing in university governance and enrollment policy
  Reviewer 3: Demographer, specializing in declining birthrate and labor market, interdisciplinary perspective
```

*(4 reviewers review in parallel... editorial_synthesizer_agent compiles...)*

**Editorial Decision: Major Revision**

```
Required Revisions:
R1: [Methodology] Quantitative analysis lacks control variables (school size, geographic location)
    -- Reviewer 1, Priority 1
R2: [Literature]  Literature review missing the most recent 2024-2026 studies
    -- Reviewer 2, Priority 1
R3: [Results]     Qualitative interviews with only 3 schools, sample representativeness insufficient
    -- Reviewer 1 & 3 consensus, Priority 2
R4: [Discussion]  Conclusions too general, need to differentiate between general/technical-vocational universities
    -- Reviewer 2, Priority 2
R5: [Introduction] Research gap argumentation not sharp enough, needs more specific data support
    -- EIC, Priority 3
```

**Stage 3 Deliverables:**
- 4 independent review reports
- Editorial Decision Letter: Major Revision
- Revision Roadmap (5 required items + 3 suggested modifications)

---

### Orchestrator: Stage 3 --> 4 Transition

```
Stage 3 (REVIEW) Complete!

Review result: Major Revision
  - 5 required revision items
  - 3 suggested modification items
  - Most critical issues: control variables in quantitative analysis + literature update

Next step is Stage 4 (REVISE).
I'll pass the Revision Roadmap to academic-paper revision mode,
guiding you through item-by-item revision.

After revision, we'll enter Stage 3' (RE-REVIEW) to confirm quality.
Maximum 2 revision cycles.

Ready to start revision?

Progress: [v]Research -> [v]Writing -> [v]Review -> [..]Revision -> [ ]Finalization
```

**User**: Start revision.

---

### Stage 4: REVISE (revision mode, Round 1)

```
Entering Stage 4 (REVISE) -- using academic-paper revision mode

Loading academic-paper SKILL.md (revision mode)...
Passing Paper Draft + Revision Roadmap...
peer_reviewer_agent monitoring revision quality...
```

**Revision Progress Tracking:**
```
R1: [v] Added control variables (school size, geographic location, tuition level)
R2: [v] Supplemented 2024-2026 literature (added 8 new citations)
R3: [v] Added explanation of qualitative sampling strategy (purposive sampling rationale)
R4: [v] Separated general/technical-vocational university analysis results, added comparison table
R5: [v] Rewrote Introduction paragraphs 2-3, added school closure data
```

**Stage 4 Deliverables:**
- Revised Draft (6,800 words, 1,600 words more than original)
- Response to Reviewers (R-A-C format, point-by-point response)

---

### Orchestrator: Stage 4 --> 3' Transition

```
Stage 4 (REVISE) Complete! Revision round: Round 1

Revision results:
- 5/5 required items all addressed
- Paper expanded from 5,200 to 6,800 words
- Added 8 new 2024-2026 citations
- Added general/technical-vocational university comparison table
- Response to Reviewers completed

Next step is Stage 3' (RE-REVIEW).
Using full mode to confirm revision quality.
This is revision cycle 1 (max 2 cycles).

Submit for re-review?

Progress: [v]Research -> [v]Writing -> [v]Review -> [v]Revision -> [..]Re-review -> [ ]Finalization
```

**User**: Submit for re-review.

---

### Stage 3': RE-REVIEW (full mode, Loop 1)

```
Entering Stage 3' (RE-REVIEW) -- Loop 1/2

Loading academic-paper-reviewer SKILL.md...
Passing Revised Draft + Response to Reviewers...
4 reviewers re-reviewing revision quality...
```

**Editorial Decision: Minor Revision**

```
R1 response: [v] Adequately addressed, control variable analysis complete
R2 response: [v] Literature update sufficient
R3 response: [v] Sampling strategy explanation acceptable, but recommend adding a limitation statement
R4 response: [v] Comparative analysis clear, but Discussion final paragraph could be further refined
R5 response: [v] Introduction improvement significant

New suggestions:
S1: Recommend refining Discussion final paragraph, focusing on policy recommendations
S2: Recommend moving sampling limitation statement to Methodology Limitations section
```

**Editorial Synthesizer**: Revision quality is good. Remaining issues are all minor. Recommend Accept with Minor Revision.

---

### Orchestrator: Stage 3' --> 5 Transition

```
Stage 3' (RE-REVIEW) Complete!

Review result: Minor Revision (Accept direction)
  - All required items passed
  - 2 remaining small suggested modifications (non-blocking)

Since this is Minor Revision (not Major), we can proceed directly to Stage 5 (FINALIZE).
Minor changes will be handled during the formatting process.

What format do you need for the final version?
  a) LaTeX (.tex + .bib) -- suitable for TSSCI journal submission
  b) DOCX -- suitable for internal school review
  c) PDF -- suitable for sharing
  d) All of the above

Progress: [v]Research -> [v]Writing -> [v]Review -> [v]Revision -> [v]Re-review -> [..]Finalization
```

**User**: All of the above.

---

### Stage 5: FINALIZE (format-convert mode)

```
Entering Stage 5 (FINALIZE) -- using academic-paper format-convert mode

Loading academic-paper SKILL.md (format-convert mode)...
Simultaneously handling 2 minor revision items...
formatter_agent executing format conversion...
```

**Stage 5 Deliverables:**
- `declining_birthrate_private_university.tex` + `.bib` (LaTeX version)
- `declining_birthrate_private_university.docx` (DOCX version)
- `declining_birthrate_private_university.pdf` (PDF version)
- `declining_birthrate_private_university.md` (Markdown original)

---

### Orchestrator: Pipeline Complete

```
+=========================================+
|   Academic Pipeline Status              |
+=========================================+
| Topic: Impact of Declining Birthrate on |
|        Private University Enrollment    |
|        Strategies in Taiwan             |
+-----------------------------------------+

  Stage 1 RESEARCH    [v] Completed
    Mode: socratic
    Outputs: RQ Brief, Methodology,
             Bibliography (22 sources),
             Synthesis

  Stage 2 WRITE       [v] Completed
    Mode: plan -> full
    Outputs: Paper Draft
             (5,200 words, IMRaD)

  Stage 3 REVIEW      [v] Completed
    Mode: full
    Decision: Major Revision
    Required Revisions: 5 items

  Stage 4 REVISE      [v] Completed
    Revision Round: 1
    Addressed: 5/5 required revisions

  Stage 3' RE-REVIEW  [v] Completed
    Loop: 1/2
    Decision: Minor Revision (Accept)

  Stage 5 FINALIZE    [v] Completed
    Formats: LaTeX, DOCX, PDF, Markdown

+-----------------------------------------+
| Materials:                              |
|   [v] RQ Brief                          |
|   [v] Methodology Blueprint             |
|   [v] Bibliography (30 sources)         |
|   [v] Synthesis Report                  |
|   [v] Paper Draft                       |
|   [v] Review Reports (4)               |
|   [v] Revision Roadmap                  |
|   [v] Revised Draft                     |
|   [v] Response to Reviewers             |
|   [v] Final Paper (4 formats)           |
+-----------------------------------------+
| Revision History:                       |
|   Round 1: Major -> 5/5 items addressed |
|   RE-REVIEW: Minor Revision (Accept)    |
+-----------------------------------------+
| Pipeline Complete!                      |
| Final paper: 6,800 words, IMRaD        |
| Citations: 30 (APA 7.0)               |
| Abstract: Chinese 420 words +          |
|           English 230 words            |
+=========================================+

Congratulations on completing your paper! It's ready for submission.

Final deliverables:
1. LaTeX version: declining_birthrate_private_university.tex
2. DOCX version: declining_birthrate_private_university.docx
3. PDF version: declining_birthrate_private_university.pdf
4. Original: declining_birthrate_private_university.md

If you later need to:
- Revise again --> just say "revise the paper" (triggers academic-paper revision mode)
- Create a presentation --> say "make slides" (triggers notebooklm-slides-generator)
- Convert to a website --> say "make an interactive webpage" (triggers report-to-website)
```
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-examples-integrity-failure-recovery-md"></a>

## SOURCE: skills/academic-pipeline/examples/integrity_failure_recovery.md

<!-- SOURCE-CONTENT-BEGIN bytes=27029 -->
---
scenario: Stage 2.5 integrity check fails, corrections made, re-verification passes
mode: full pipeline (mid-entry at Stage 2.5)
stages_shown: Stage 2.5 (FAIL -> corrections -> PASS)
demonstrates: How the pipeline handles integrity failures and guides recovery
---

# Integrity Failure Recovery Example

This example shows what happens when Stage 2.5 (Pre-Review Integrity Check) finds serious issues, how they are corrected, and how re-verification works. It demonstrates the pipeline's zero-tolerance integrity gate and the systematic correction workflow defined in `agents/integrity_verification_agent.md`.

## Scenario

A researcher submits a paper titled "Digital Transformation in European Higher Education: A Mixed-Methods Analysis of Institutional Readiness and Student Outcomes" for integrity verification. The paper has 45 references, makes 18 quantitative claims, and is entering the pipeline at Stage 2.5 after completing Stage 2 (WRITE).

**Paper details:**
- Word count: 7,200
- Structure: IMRaD
- Citation format: APA 7.0
- References: 45 entries (32 journal articles, 6 reports, 4 books, 3 working papers)

---

## Orchestrator: Stage 2 --> 2.5 Transition

```
━━━ Stage 2 (WRITE) Complete ━━━

Metrics:
- Word count: 7,200 (target: 7,000 +/-10%)    [OK]
- References: 45 (min: 30)                     [OK]
- Coverage: 6/6 sections drafted                [COMPLETE]

Deliverables:
- Paper Draft (7,200 words, IMRaD)
- Bilingual Abstract (EN 248 words + zh-TW 380 characters)
- Reference List (45 entries, APA 7.0)

Flagged: None

Next: Stage 2.5 (INTEGRITY) — Mandatory checkpoint.
This stage cannot be skipped. All references and data claims
will be verified before the paper proceeds to peer review.

Proceeding to Stage 2.5...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Stage 2.5: Pre-Review Integrity Check (Round 1)

```
Entering Stage 2.5 (INTEGRITY) -- Mode 1 (Pre-Review)

Loading integrity_verification_agent...
Executing: Phase A (Reference Verification) + Phase B (Citation Context, 31% spot-check)
         + Phase C (Data Verification) + Phase D (Originality, 33% spot-check)
         + Phase E (Claim Verification, 30% spot-check)
```

### integrity_verification_agent Output

**Mode**: Pre-review (Mode 1)
**Paper**: "Digital Transformation in European Higher Education: A Mixed-Methods Analysis of Institutional Readiness and Student Outcomes"

---

#### Phase A: Reference Existence Verification (45/45 checked)

| # | Reference | Status | Issue |
|---|-----------|--------|-------|
| 12 | Martinez, R. (2023). Artificial intelligence adoption in European universities: A cross-national survey. *Journal of Digital Education*, 15(2), 45-62. https://doi.org/10.1016/j.jde.2023.02.009 | FAIL | DOI resolves to a different article ("Machine Learning in K-12 Assessment" by Patel & Ross). No article with this exact title found in *Journal of Digital Education* or any indexed database. **GHOST REFERENCE** |
| 19 | Selwyn, N. (2022). Digital technologies and the automation of education. *Learning, Media and Technology*, 47(1), 1-5. | ISSUE | Article exists but published in 2023 (Vol. 48, No. 1), not 2022 (Vol. 47, No. 1). Correct DOI: https://doi.org/10.1080/17439884.2023.2141509 |
| 28 | European Commission. (2022). Digital Education Action Plan 2021-2027. Brussels: Publications Office of the European Union. | ISSUE | Title is "Digital Education Action Plan 2021-2027" but the official title is "Digital Education Action Plan (2021-2027)." Originally published September 2020, not 2022. The 2022 date may refer to a progress report, which is a different document. |
| 33 | Wong, K., & Liu, S. (2024). Blockchain-based micro-credentials in Asian higher education: A multi-site case study. *Higher Education Policy*, 37(1), 89-104. https://doi.org/10.1057/s41307-023-00318-5 | FAIL | Article exists but authors are Wong, K., & Liu, **S. K.** (not S.). Published in 2023 (online first), print edition 2024, Vol. **36**(4), pp. 612-629. DOI resolves to the correct article with the corrected metadata. |
| 41 | Organisation for Economic Co-operation and Development. (2021). *OECD Digital Education Outlook 2021*. OECD Publishing. | ISSUE | Correct title is *OECD Digital Education Outlook 2021: Pushing the Frontiers with Artificial Intelligence, Blockchain and Robots*. Subtitle is required per APA 7.0 for books. |
| -- | Remaining 41/45 references | PASS | All verified against DOI records, publisher databases, or Google Scholar. Bibliographic details match. |

**Phase A Summary**: 45 checked, 41 PASS, 2 FAIL (1 ghost reference, 1 wrong metadata), 2 ISSUE (wrong year/title)

---

#### Phase B: Citation Context Spot-Check (14/45 sampled = 31%)

| # | Citation | Location | Verdict | Detail |
|---|----------|----------|---------|--------|
| B1 | Ref 3 — Bond et al. (2020) | Section 2.1, para 2: "Bond et al. (2020) found that student engagement increased by 12-18% when blended learning was implemented with structured digital scaffolding." | PASS | Source (p. 847) reports "engagement scores improved between 12% and 18% across four cohorts," consistent with the paper's claim. |
| B2 | Ref 12 — Martinez (2023) | Section 2.3, para 1: "Martinez (2023) surveyed 1,200 faculty members across 15 EU countries and found that 68% reported using at least one AI tool in their teaching." | FAIL | **Cannot verify** — Ref 12 is a ghost reference (flagged in Phase A). The claim has no verifiable source. |
| B3 | Ref 22 — Castaneda & Selwyn (2018) | Section 2.2, para 3: "Critical scholars have argued that digital transformation in education is often driven by commercial interests rather than pedagogical evidence (Castaneda & Selwyn, 2018)." | PASS | Source discusses commercialization of EdTech; the paraphrase is a fair representation of the authors' argument (Chapter 3, pp. 45-52). |
| B4 | Ref 28 — European Commission (2022) | Section 1, para 2: "The European Commission committed EUR 2.1 billion to digital infrastructure in higher education between 2021 and 2025 (European Commission, 2022)." | ISSUE | Cannot confirm this exact figure in the Digital Education Action Plan. The EC Erasmus+ Digital allocation for 2021-2027 is approximately EUR 2.0 billion across all education sectors, not exclusively higher education. |
| B5 | Ref 33 — Wong & Liu (2024) | Section 2.4, para 1: "Wong and Liu (2024) demonstrated that blockchain micro-credentials improved employer trust in non-traditional qualifications by 41%." | ISSUE | Source reports 41% improvement in a specific employer survey (Table 3, p. 621 in the correct pagination), but the figure applies to "initial employer screening decisions," not general "employer trust." The paraphrase overgeneralizes. |
| -- | 9 additional citations sampled | Various | PASS | Context accurately reflects source content. |

**Phase B Summary**: 14 sampled, 11 PASS, 1 FAIL (ghost ref context), 2 ISSUE (data precision)

---

#### Phase C: Data Verification (18 quantitative claims checked)

| # | Claim in Paper | Cited Source | Verdict | Detail |
|---|---------------|-------------|---------|--------|
| C1 | "73% of EU universities have adopted a learning management system" (Section 1, para 3) | Ref 8 — Eurostat (2023), *Digital Economy and Society Index* | VERIFIED | DESI 2023 report (Table 4.2) states 73.1% of HEIs in EU-27 reported LMS adoption. |
| C2 | "Student satisfaction with digital learning increased by 34% between 2019 and 2022" (Section 4.1, para 2) | Ref 15 — Garcia, M. (2022). Student perceptions of emergency remote teaching. *Studies in Higher Education*, 47(8), 1620-1638. | MAJOR_DISTORTION | Source (p. 1631, Table 5) reports a **24% increase** in satisfaction with "specific digital tools," not a 34% overall increase. The 34% figure appears in a different column measuring "willingness to continue online learning," which is a distinct construct. |
| C3 | "The EU invested EUR 2.1 billion in digital infrastructure for higher education" (Section 1, para 2) | Ref 28 — European Commission (2022) | MINOR_DISTORTION | As noted in Phase B, the figure is approximately EUR 2.0 billion across all education sectors. "EUR 2.1 billion" and "higher education" both overstate the source. |
| C4 | "Faculty digital competency scores improved by 0.8 standard deviations after institutional training programs" (Section 4.2, para 3) | Ref 31 — Fernandez-Batanero et al. (2022) | VERIFIED | Source (p. 12, meta-analytic result) reports pooled effect size d = 0.79, rounded to 0.8 is acceptable. |
| C5 | "47% of interviewed faculty reported 'significant resistance' to mandatory digital tool adoption" (Section 4.3, para 1) | Paper's own interview data | VERIFIED | Internal consistency check: Table 6 shows 9 of 19 interviewees (47.4%) coded under "significant resistance" theme. Consistent. |
| C6 | "Only 12% of European universities have a dedicated Chief Digital Officer" (Section 5, para 2) | Ref 37 — Rampelt et al. (2019). *Digital Higher Education: A Dividing or Connecting Element?* EURASHE. | MINOR_DISTORTION | Source (p. 28) states "approximately 11% of surveyed institutions reported having a CDO or equivalent role." The paper says 12%, which is a minor rounding difference, but the source is from 2019 — the paper presents this as a current statistic without noting the 4-year gap. |
| -- | 12 additional claims | Various | VERIFIED | All match their cited sources within acceptable tolerance. |

**Phase C Summary**: 18 checked, 15 VERIFIED, 1 MAJOR_DISTORTION, 2 MINOR_DISTORTION

---

#### Phase D: Originality Check (33% paragraph sample)

| Grade | Paragraph Count | Proportion |
|-------|----------------|-----------|
| ORIGINAL | 12 | 63.2% |
| COMMON_KNOWLEDGE | 4 | 21.1% |
| PARAPHRASE | 3 | 15.8% |
| CLOSE_MATCH | 0 | 0% |
| VERBATIM | 0 | 0% |

**Phase D Summary**: 19/58 paragraphs sampled. No originality concerns detected. All paraphrased passages have proper citations.

---

#### Phase E: Claim Verification (30% spot-check, 6/18 claims)

Claims C1-C6 above were selected for the 30% spot-check. Results are reported in Phase C.

**Phase E Summary**: 6 claims checked, 3 VERIFIED, 1 MAJOR_DISTORTION, 2 MINOR_DISTORTION

---

### Verdict: FAIL

**Reason**: 2 SERIOUS issues + 2 MEDIUM issues detected. PASS requires zero SERIOUS and zero MEDIUM.

**Issues requiring correction (sorted by severity):**

| # | Issue | Severity | Phase | Description |
|---|-------|----------|-------|-------------|
| 1 | Ref 12: Ghost reference (fabricated) | SERIOUS | A | "Martinez, R. (2023)" does not exist. DOI resolves to a different article. No record found in any indexed database. All claims citing this reference are unsupported. |
| 2 | C2: "34% increase" claim distortion | SERIOUS | C/E | Source (Garcia, 2022) says 24% increase in tool-specific satisfaction, not 34% overall satisfaction increase. The 34% refers to a different construct in the source. |
| 3 | Ref 28: Wrong year, incomplete title | MEDIUM | A | European Commission document published 2020, not 2022. Title missing parentheses around date range. |
| 4 | Ref 33: Wrong author initials, year, and pagination | MEDIUM | A | Author is Liu, S. K. (not S.); year should be 2023; volume 36(4), pp. 612-629. |
| 5 | C3: "EUR 2.1 billion" slight overstatement | MINOR | C | Source says ~EUR 2.0 billion across all education sectors, not exclusively higher education. |
| 6 | Ref 19: Wrong year and volume | MINOR | A | Published 2023 (Vol. 48, No. 1), not 2022 (Vol. 47, No. 1). |
| 7 | Ref 41: Missing subtitle | MINOR | A | APA 7.0 requires the book's full subtitle. |
| 8 | B5: Wong & Liu paraphrase overgeneralization | MINOR | B | "Employer trust" is too broad; source specifically measures "initial employer screening decisions." |
| 9 | C6: Outdated statistic presented as current | MINOR | C | 2019 data (11%) presented as current fact (12%) without temporal qualifier. |

---

## Correction Process

### Pipeline Orchestrator Response

```
━━━ MANDATORY CHECKPOINT: Stage 2.5 INTEGRITY ━━━

Verdict: ❌ FAIL

Issues found:
  SERIOUS:  2 (must fix to proceed)
  MEDIUM:   2 (must fix to proceed)
  MINOR:    5 (recommended fix)

SERIOUS issues:
  1. Ghost reference — Ref 12 (Martinez, 2023) does not exist
  2. Data distortion — "34% increase" should be "24% increase"

MEDIUM issues:
  3. Ref 28 — wrong publication year (2020, not 2022)
  4. Ref 33 — wrong author initials, year, and pagination

The pipeline CANNOT proceed to Stage 3 (REVIEW) until
all SERIOUS and MEDIUM issues are resolved.

Options:
  a) "Fix all issues" — I will correct all 9 issues
  b) "Fix critical only" — I will fix the 4 SERIOUS/MEDIUM issues
  c) Review issues one by one — discuss each before fixing
  d) "Pause" — save state and return later
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### User Response

"Fix all issues."

---

### Corrections Applied

#### Issue 1 (SERIOUS): Ghost Reference — Ref 12 Replacement

**Problem**: "Martinez, R. (2023). Artificial intelligence adoption in European universities: A cross-national survey. *Journal of Digital Education*, 15(2), 45-62." does not exist. The DOI resolves to a completely different article.

**Resolution**: The ghost reference supported two claims in Section 2.3 about faculty AI tool adoption rates. A verified replacement source was identified via WebSearch:

| Aspect | Before | After |
|--------|--------|-------|
| Reference | Martinez, R. (2023). Artificial intelligence adoption in European universities: A cross-national survey. *Journal of Digital Education*, 15(2), 45-62. https://doi.org/10.1016/j.jde.2023.02.009 | Zawacki-Richter, O., Marin, V. I., Bond, M., & Gouverneur, F. (2019). Systematic review of research on artificial intelligence applications in higher education: Where are the educators? *International Journal of Educational Technology in Higher Education*, 16(1), Article 39. https://doi.org/10.1186/s41239-019-0171-0 |
| In-text (Section 2.3, para 1) | "Martinez (2023) surveyed 1,200 faculty members across 15 EU countries and found that 68% reported using at least one AI tool in their teaching." | "Zawacki-Richter et al. (2019) conducted a systematic review of 146 AI-in-education studies and found that the vast majority focused on student-facing applications, with faculty adoption and training remaining significantly understudied (p. 27)." |
| In-text (Section 2.3, para 4) | "The cross-national variation in AI adoption (Martinez, 2023) suggests that institutional culture plays a moderating role." | "The gap in research on faculty perspectives (Zawacki-Richter et al., 2019) suggests that institutional culture and educator readiness may be critical moderating factors that remain under-investigated." |
| Verification | DOI invalid, article non-existent | DOI verified (resolves to Springer), 4,800+ citations on Google Scholar |
| Status | -- | **FIXED** |

#### Issue 2 (SERIOUS): Data Distortion — 34% vs 24%

**Problem**: Section 4.1 claims "student satisfaction with digital learning increased by 34%," but the cited source (Garcia, 2022, Table 5) reports a 24% increase in tool-specific satisfaction. The 34% figure refers to "willingness to continue online learning," a distinct construct.

| Aspect | Before | After |
|--------|--------|-------|
| Text (Section 4.1, para 2) | "Student satisfaction with digital learning increased by 34% between 2019 and 2022 (Garcia, 2022)." | "Student satisfaction with specific digital learning tools increased by 24% between 2019 and 2022 (Garcia, 2022, p. 1631, Table 5). Notably, willingness to continue online learning showed a larger increase of 34%, suggesting that familiarity may drive acceptance more than satisfaction per se." |
| Rationale | Single number misattributed to wrong construct | Both figures now correctly attributed to their respective constructs with page reference |
| Status | -- | **FIXED** |

#### Issue 3 (MEDIUM): Ref 28 — European Commission Year and Title

| Aspect | Before | After |
|--------|--------|-------|
| Reference | European Commission. (2022). Digital Education Action Plan 2021-2027. Brussels: Publications Office of the European Union. | European Commission. (2020). *Digital Education Action Plan (2021-2027)*. Publications Office of the European Union. https://ec.europa.eu/education/education-in-the-eu/digital-education-action-plan_en |
| In-text citations | (European Commission, 2022) [3 instances] | (European Commission, 2020) [3 instances] |
| Status | -- | **FIXED** |

#### Issue 4 (MEDIUM): Ref 33 — Wong & Liu Metadata

| Aspect | Before | After |
|--------|--------|-------|
| Reference | Wong, K., & Liu, S. (2024). Blockchain-based micro-credentials in Asian higher education: A multi-site case study. *Higher Education Policy*, 37(1), 89-104. https://doi.org/10.1057/s41307-023-00318-5 | Wong, K., & Liu, S. K. (2023). Blockchain-based micro-credentials in Asian higher education: A multi-site case study. *Higher Education Policy*, 36(4), 612-629. https://doi.org/10.1057/s41307-023-00318-5 |
| In-text citations | (Wong & Liu, 2024) [2 instances] | (Wong & Liu, 2023) [2 instances] |
| Status | -- | **FIXED** |

#### Issue 5 (MINOR): EUR 2.1 Billion Overstatement

| Aspect | Before | After |
|--------|--------|-------|
| Text (Section 1, para 2) | "The EU invested EUR 2.1 billion in digital infrastructure for higher education." | "The EU allocated approximately EUR 2.0 billion to digital education initiatives across all sectors through the Erasmus+ programme for 2021-2027 (European Commission, 2020)." |
| Rationale | Corrected amount, removed "higher education" exclusivity claim, added programme name for precision |
| Status | -- | **FIXED** |

#### Issue 6 (MINOR): Ref 19 — Selwyn Year and Volume

| Aspect | Before | After |
|--------|--------|-------|
| Reference | Selwyn, N. (2022). Digital technologies and the automation of education. *Learning, Media and Technology*, 47(1), 1-5. | Selwyn, N. (2023). Digital technologies and the automation of education. *Learning, Media and Technology*, 48(1), 1-5. https://doi.org/10.1080/17439884.2023.2141509 |
| In-text citations | (Selwyn, 2022) [1 instance] | (Selwyn, 2023) [1 instance] |
| Status | -- | **FIXED** |

#### Issue 7 (MINOR): Ref 41 — Missing Subtitle

| Aspect | Before | After |
|--------|--------|-------|
| Reference | Organisation for Economic Co-operation and Development. (2021). *OECD Digital Education Outlook 2021*. OECD Publishing. | Organisation for Economic Co-operation and Development. (2021). *OECD Digital Education Outlook 2021: Pushing the frontiers with artificial intelligence, blockchain and robots*. OECD Publishing. https://doi.org/10.1787/589b283f-en |
| Status | -- | **FIXED** |

#### Issue 8 (MINOR): Wong & Liu Paraphrase Overgeneralization

| Aspect | Before | After |
|--------|--------|-------|
| Text (Section 2.4, para 1) | "Wong and Liu (2024) demonstrated that blockchain micro-credentials improved employer trust in non-traditional qualifications by 41%." | "Wong and Liu (2023) found that blockchain-verified micro-credentials increased the likelihood of favorable initial employer screening decisions by 41% compared to unverified digital badges (p. 621, Table 3)." |
| Rationale | "Employer trust" was overly broad; corrected to the specific construct measured in the source |
| Status | -- | **FIXED** |

#### Issue 9 (MINOR): Outdated CDO Statistic

| Aspect | Before | After |
|--------|--------|-------|
| Text (Section 5, para 2) | "Only 12% of European universities have a dedicated Chief Digital Officer." | "As of 2019, approximately 11% of surveyed European institutions reported having a Chief Digital Officer or equivalent role (Rampelt et al., 2019), a figure that may have since changed given accelerated digital transformation efforts." |
| Rationale | Added temporal qualifier and acknowledged potential data staleness |
| Status | -- | **FIXED** |

---

## Stage 2.5: Re-Verification (Round 2)

```
Stage 2.5 Re-verification -- Round 2 (focused on 9 corrected items)

integrity_verification_agent re-checking corrected items only...
```

### integrity_verification_agent Re-Verification Output

| # | Original Issue | Correction Applied | Re-verification | Status |
|---|---------------|-------------------|-----------------|--------|
| 1 | Ghost reference (Ref 12: Martinez, 2023) | Replaced with Zawacki-Richter et al. (2019). Both in-text citations rewritten to match new source content. | DOI verified (Springer). Article confirmed: 146 studies reviewed, educator-focused gap identified. In-text paraphrases accurately reflect source. | PASS |
| 2 | "34% increase" data distortion | Corrected to "24% increase" for tool satisfaction; added 34% for willingness construct with proper attribution and page reference. | Garcia (2022), Table 5, p. 1631 confirmed: 24% tool satisfaction, 34% willingness. Paper now correctly attributes both figures. | PASS |
| 3 | EC wrong year/title (Ref 28) | Changed year to 2020, added parentheses to title, added URL. | EC official page confirms September 2020 publication date. Title matches official listing. | PASS |
| 4 | Wong & Liu wrong metadata (Ref 33) | Changed to Liu, S. K.; year 2023; Vol. 36(4), pp. 612-629. | DOI resolves to correct metadata. Publisher page confirms all fields. | PASS |
| 5 | EUR 2.1B overstatement | Changed to "approximately EUR 2.0 billion" with sector and programme qualifier. | Erasmus+ allocation documents confirm ~EUR 2.0B for digital education across all sectors. | PASS |
| 6 | Selwyn wrong year (Ref 19) | Changed to 2023, Vol. 48(1). Added DOI. | DOI resolves correctly. Publisher confirms 2023 publication. | PASS |
| 7 | OECD missing subtitle (Ref 41) | Added full subtitle and DOI. | DOI resolves to OECD iLibrary. Full title matches. | PASS |
| 8 | Wong & Liu overgeneralization | Narrowed to "initial employer screening decisions" with page/table reference. | Matches source Table 3, p. 621. Paraphrase is now faithful. | PASS |
| 9 | Outdated CDO statistic | Added temporal qualifier ("As of 2019") and acknowledged potential staleness. | Rampelt et al. (2019), p. 28 confirms "approximately 11%." Temporal framing is appropriate. | PASS |

### Re-Verification Verdict: PASS

```
Integrity Verification Report — Round 2

Verification Mode: Pre-Review (Mode 1), Re-verification of corrected items
Verdict: ✅ PASS

Verification Summary:
| Category               | Total | Passed | Issues |
|------------------------|-------|--------|--------|
| Reference Existence    | 45    | 45     | 0      |
| Bibliographic Accuracy | 45    | 45     | 0      |
| Ghost Citations        | --    | --     | 0 orphan / 0 dangling |
| Citation Context       | 14    | 14     | 0      |
| Data Accuracy          | 18    | 18     | 0      |
| Internal Consistency   | --    | Pass   | 0      |
| Originality (D1)       | 19    | 19     | 0 CLOSE_MATCH / 0 VERBATIM |
| Self-Plagiarism (D2)   | N/A   | N/A    | Author name not provided |

Issue Summary:
  SERIOUS:  0 (was 2, both resolved)
  MEDIUM:   0 (was 2, both resolved)
  MINOR:    0 (was 5, all resolved)

All 9 issues from Round 1 have been verified as resolved.
Paper is cleared for peer review.
```

---

## Pipeline Continues: Stage 2.5 --> Stage 3

```
━━━ MANDATORY CHECKPOINT: Stage 2.5 INTEGRITY ━━━

Verdict: ✅ PASS (Round 2, after corrections)

Integrity verification complete:
  - Round 1: FAIL (2 SERIOUS, 2 MEDIUM, 5 MINOR)
  - Corrections applied: 9/9
  - Round 2: PASS (all issues resolved)

Corrections summary:
  - 1 ghost reference removed and replaced with verified source
  - 1 data distortion corrected (34% → 24% with proper attribution)
  - 3 bibliographic metadata errors fixed
  - 4 precision/recency improvements applied

The paper is now cleared for peer review.

Next: Stage 3 (REVIEW) — Full 5-reviewer review
  (EIC + R1 Methodology + R2 Domain + R3 Perspective + Devil's Advocate)

Continue?

Progress: [v]Research -> [v]Writing -> [v]Integrity -> [..]Review -> [ ]Revision -> [ ]Finalization
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**User**: Continue!

---

## Key Takeaways

### 1. Ghost References Are the Most Dangerous Integrity Failure

Reference 12 (Martinez, 2023) looked entirely plausible — a believable author name, a real-sounding journal, a formatted DOI. But the DOI resolved to a completely different article, and no record of this publication existed in any database. This is the hallmark of a fabricated reference, and it is the primary reason Stage 2.5 exists. Without integrity verification, this ghost reference would have entered peer review and potentially publication.

### 2. Data Distortions Can Be Subtle and Consequential

The "34% vs 24%" error (Issue 2) was not a careless typo — the 34% figure genuinely appeared in the cited source, but in a different column measuring a different construct. This type of construct confusion is common in academic writing and can survive multiple rounds of human review. The integrity verification agent caught it by cross-referencing the exact table and column in the source.

### 3. Corrections Must Be Verifiable, Not Just Plausible

Each correction includes a verification trail: DOI resolution, page numbers, table references, and publisher confirmations. The replacement reference for the ghost citation (Zawacki-Richter et al., 2019) was selected not just because it covered a similar topic, but because it has 4,800+ citations and is published by Springer with a valid DOI — maximizing verifiability.

### 4. Re-Verification Is Focused, Not Redundant

Round 2 only re-checks the 9 corrected items, not the entire paper. The 41 references that passed in Round 1 are not re-verified. This keeps the re-verification efficient while ensuring that corrections actually resolve the original issues (and do not introduce new ones).

### 5. The Integrity Gate Is Non-Negotiable

The pipeline cannot proceed to Stage 3 (REVIEW) until the integrity check returns PASS. This is a MANDATORY checkpoint — the user cannot skip it, override it, or request an exception. The maximum retry is 3 rounds; after that, unverifiable items are listed and the user must make an explicit decision about whether to proceed with acknowledged limitations.

### 6. MINOR Issues Are Worth Fixing Too

While only SERIOUS and MEDIUM issues block the pipeline, fixing MINOR issues (like the missing subtitle in Ref 41 or the temporal qualifier for the CDO statistic) strengthens the paper before it reaches reviewers. Reviewers will notice these small inaccuracies, and fixing them preemptively removes easy targets for criticism.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-examples-mid-entry-example-md"></a>

## SOURCE: skills/academic-pipeline/examples/mid_entry_example.md

<!-- SOURCE-CONTENT-BEGIN bytes=12640 -->
# Example: Mid-Entry into Pipeline

## Scenario Description

**User type**: University professor, experienced in paper writing
**Scenario**: Already completed an English paper draft, wants a simulated review before submission
**Goal**: Review --> Revision --> Format conversion (LaTeX)
**Language**: English (paper is in English; conversation with orchestrator in English)

---

## User Input

```
I've already written an English paper titled "Machine Learning Approaches for
Predicting University Attrition Risk in Taiwan," approximately 7,000 words.
I'd like a simulated review before submitting.
```

---

## Pipeline Execution Log

### Orchestrator: Mid-Entry Detection

```
Detection results:
- Materials: Complete English paper draft (7,000 words)
- Goal: Simulated review + revision + submission preparation
- Entry point: Stage 3 (REVIEW)
- User type: Experienced researcher

Detected that you have a complete paper — you can proceed directly to Stage 3 (REVIEW).

Before starting, let me confirm a few things:
1. What's the paper structure? (IMRaD / other)
2. What review mode would you like?
   - full: Complete 4-person review (EIC + 3 Peer Reviewers)
   - quick: EIC quick assessment (15-minute version)
   - guided: Socratic guided review (interactive dialogue)
3. Which journal (or what tier) are you targeting?
4. Will you need revision and format conversion after the review?

If you later want to revise based on review comments, I'll automatically guide you to Stage 4.
```

**User**: IMRaD structure, I'd like a quick review first to see if there are any big-picture issues. Targeting Computers & Education (SSCI Q1). Will decide about revision after the review.

### Orchestrator: Confirm Configuration

```
Got it. Pipeline configuration:

  Stage 1 RESEARCH    [--] Skipped (you already have a research foundation)
  Stage 2 WRITE       [--] Skipped (you already have a complete paper)
  Stage 3 REVIEW:     quick -- EIC quick assessment first, checking the big picture
  Stage 4 REVISE:     TBD -- based on Stage 3 results
  Stage 5 FINALIZE:   TBD -- when needed

Start Stage 3 (REVIEW) quick mode?

Progress: [--]Research -> [--]Writing -> [..]Review -> [ ]Revision -> [ ]Finalization
```

**User**: Start.

---

### Stage 3: REVIEW (quick mode)

```
Entering Stage 3 (REVIEW) -- using academic-paper-reviewer quick mode

Loading academic-paper-reviewer SKILL.md...
Receiving user-provided paper draft...
field_analyst_agent analyzing paper domain...
eic_agent executing quick assessment...
```

**Field Analysis (quick version):**
```
Paper domain: Educational Data Mining / Higher Education
Method type: Machine Learning (Supervised Classification)
Target journal: Computers & Education (SSCI Q1, IF: 12.0)

EIC Persona:
  Computers & Education Associate Editor
  Specialization: Learning Analytics, Educational AI
```

**EIC Quick Assessment:**

```
Overall: Promising but needs work (Minor-to-Major Revision range)

Key Strengths (top 3):
1. Timely topic -- university attrition prediction highly relevant
   in Taiwan's demographic context
2. Good feature engineering -- combining MOE open data with
   institutional records is novel
3. Clear methodology -- model comparison (RF, XGBoost, LSTM)
   is well-structured

Key Concerns (top 3):
C1: [CRITICAL] Ethical considerations section is missing.
    C&E requires explicit discussion of algorithmic fairness,
    student privacy, and potential discriminatory outcomes.
C2: [MAJOR] Model interpretability not discussed.
    C&E reviewers expect SHAP values or similar explainability
    analysis, not just accuracy metrics.
C3: [MAJOR] Literature gap -- no mention of Dropout Factory
    literature (Balfanz & Legters, 2004) or recent European
    attrition studies. Too Taiwan-centric for an international
    journal.

Quick Verdict: Major Revision
  Before full submission, address C1-C3.
  Estimated revision effort: 2-3 weeks.
```

**Stage 3 Deliverables:**
- EIC Quick Assessment Report
- 3 key issues list (priority sorted)

---

### Orchestrator: Transition Recommendation

```
Stage 3 (REVIEW) quick mode Complete!

Review result: Major Revision direction
  C1: [CRITICAL] Missing ethics discussion (hard requirement for C&E)
  C2: [MAJOR] Missing model interpretability analysis
  C3: [MAJOR] Literature review lacks international perspective

This is the quick review result. You have several options:

  a) Proceed directly to Stage 4 (REVISE) to address these 3 issues
  b) Upgrade to full review (complete 4-person review),
     to see if there are other issues
  c) Revise on your own first, come back when done

My recommendation: Since you're targeting C&E (Q1 journal),
fix C1-C3 first, then do a full review to ensure quality.

Which do you choose?
```

**User**: Fix C1-C3 first, then do full review.

### Orchestrator: Update Configuration

```
OK, updating pipeline:

  Stage 3 REVIEW (quick):  [v] Completed
  Stage 4 REVISE:          [..] Next -- fix C1-C3
  Stage 3' RE-REVIEW:      full mode -- full review after revision
  Stage 5 FINALIZE:        TBD

Start Stage 4 (REVISE)?

Progress: [--]Research -> [--]Writing -> [v]Review -> [..]Revision -> [ ]Re-review -> [ ]Finalization
```

**User**: Start revision.

---

### Stage 4: REVISE (revision mode, Round 1)

```
Entering Stage 4 (REVISE) -- using academic-paper revision mode

Loading academic-paper SKILL.md (revision mode)...
Passing Paper Draft + Quick Assessment Report...
```

**Revision Progress Tracking:**
```
C1: [v] Added Ethics & Fairness section (Section 5.3)
    - Algorithmic fairness analysis (demographic parity, equalized odds)
    - Student privacy framework (FERPA-equivalent for Taiwan)
    - Potential discriminatory outcomes discussion
    - Added 5 citations on AI ethics in education

C2: [v] Added Model Interpretability analysis (Section 4.3)
    - SHAP value analysis for top 20 features
    - Feature importance comparison across 3 models
    - Case study: 3 individual prediction explanations
    - Added SHAP visualization figures

C3: [v] Expanded Literature Review (Section 2)
    - Added Dropout Factory framework (Balfanz & Legters)
    - Added 6 European attrition studies (2020-2026)
    - Added cross-cultural comparison discussion
    - Restructured into 3 sub-sections: global -> Asia -> Taiwan
```

**Stage 4 Deliverables:**
- Revised Draft (9,200 words, 2,200 words more than original)
- Response to Reviewers (R-A-C format, 3 items all addressed)

---

### Orchestrator: Stage 4 --> 3' Transition

```
Stage 4 (REVISE) Complete!

Revision results:
- 3/3 issues all addressed
- Paper expanded from 7,000 to 9,200 words
- Added Ethics section, SHAP analysis, international literature
- Added 11 new citations

Next step is Stage 3' (RE-REVIEW) -- this time using full mode.
4 reviewers will do a complete review of the revised version.
This is revision cycle 1 (max 2 cycles).

Submit for full review?

Progress: [--]Research -> [--]Writing -> [v]Review -> [v]Revision -> [..]Re-review -> [ ]Finalization
```

**User**: Submit.

---

### Stage 3': RE-REVIEW (full mode, Loop 1)

```
Entering Stage 3' (RE-REVIEW) -- full mode, Loop 1/2

Loading academic-paper-reviewer SKILL.md (full mode)...
Passing Revised Draft + Response to Reviewers...
field_analyst_agent re-analyzing...
```

**Reviewer Configuration:**
```
EIC:        Computers & Education Associate Editor
            Educational AI, Learning Analytics
Reviewer 1: Machine Learning expert
            Predictive modeling, Model evaluation
Reviewer 2: Higher Education researcher
            Student success, Retention strategies
Reviewer 3: Research Ethics / Data Science ethicist
            Algorithmic fairness, Educational data mining ethics
```

**4 Review Reports Compiled:**

```
EIC: Minor Revision
  - C1 response adequate, Ethics section well-structured
  - Recommend updating Abstract to reflect new ethics + interpretability contributions
  - Recommend adding a Practical Implications section for university administrators

Reviewer 1: Accept
  - SHAP analysis thorough and insightful
  - Model comparison fair and well-documented
  - Minor: Table 3 precision/recall should include confidence intervals

Reviewer 2: Minor Revision
  - International literature coverage greatly improved
  - Recommend Discussion add dialogue with Tinto's Student Integration Model
  - Minor: Section 2.1 citation Chen (2023) should be Chen (2024)

Reviewer 3: Accept
  - Ethics section quality is high, exceeding typical C&E standards
  - Algorithmic fairness metrics well-chosen
  - Recommend adding a "limitations of fairness metrics" reflection paragraph
```

**Editorial Decision: Minor Revision (Accept direction)**

```
Required Revisions:
R1: Update Abstract (reflect new contributions)
R2: Add Practical Implications section

Suggested Revisions:
S1: Table 3 add confidence intervals
S2: Discussion add Tinto's model dialogue
S3: Fix Chen (2023) -> Chen (2024) citation year
S4: Add fairness metrics limitations paragraph
```

---

### Orchestrator: Quick Revision + FINALIZE

```
Stage 3' (RE-REVIEW) Complete!

Review result: Minor Revision (Accept direction)
  - 2 out of 4 reviewers Accept + 2 Minor Revision
  - 2 required items (Abstract update + Practical Implications)
  - 4 suggested modifications

These are all minor changes that can be handled during Stage 5 (FINALIZE).
Or would you prefer a formal Stage 4 revision before another review?

My recommendation: Since all items are minor, proceed directly to Stage 5 and handle them together.

What format do you need?
  a) LaTeX (.tex + .bib) -- suitable for C&E submission
  b) Other formats

Progress: [--]Research -> [--]Writing -> [v]Review -> [v]Revision -> [v]Re-review -> [..]Finalization
```

**User**: Go straight to finalize, LaTeX format.

---

### Stage 5: FINALIZE (format-convert mode)

```
Entering Stage 5 (FINALIZE) -- format-convert mode

Simultaneously handling minor revision items:
R1: [v] Abstract updated
R2: [v] Added Practical Implications section (200 words)
S1: [v] Table 3 confidence intervals added
S2: [v] Discussion Tinto's model paragraph added
S3: [v] Chen citation year corrected
S4: [v] Fairness metrics limitations paragraph added

formatter_agent executing LaTeX conversion...
- Using Elsevier article template (C&E format)
- Producing .tex + .bib + figures/
- Producing cover letter draft
```

**Stage 5 Deliverables:**
- `ml_university_attrition_taiwan.tex` (LaTeX main text)
- `references.bib` (BibTeX file)
- `figures/` (all figures and tables)
- `cover_letter.tex` (submission cover letter draft)

---

### Orchestrator: Pipeline Complete

```
+=========================================+
|   Academic Pipeline Status              |
+=========================================+
| Topic: ML Approaches for Predicting     |
|        University Attrition Risk        |
+-----------------------------------------+

  Stage 1 RESEARCH    [--] Skipped
  Stage 2 WRITE       [--] Skipped
  Stage 3 REVIEW      [v] Completed
    Mode: quick
    Decision: Major Revision (3 items)
  Stage 4 REVISE      [v] Completed
    Round: 1, Addressed: 3/3
  Stage 3' RE-REVIEW  [v] Completed
    Mode: full, Loop: 1/2
    Decision: Minor Revision (Accept)
  Stage 5 FINALIZE    [v] Completed
    Format: LaTeX (Elsevier)

+-----------------------------------------+
| Materials:                              |
|   [--] RQ Brief (skipped)               |
|   [--] Methodology (skipped)            |
|   [--] Bibliography (skipped)           |
|   [--] Synthesis (skipped)              |
|   [v] Paper Draft (user-provided)       |
|   [v] Review Reports (quick + full)     |
|   [v] Revision Roadmap                  |
|   [v] Revised Draft (9,500 words)       |
|   [v] Response to Reviewers             |
|   [v] Final Paper (LaTeX)              |
+-----------------------------------------+
| Revision History:                       |
|   Round 1: Major -> 3/3 addressed       |
|   RE-REVIEW: Minor (Accept direction)   |
|   Final minor fixes in FINALIZE         |
+-----------------------------------------+
| Pipeline Complete!                      |
+=========================================+

Your paper is ready for submission to Computers & Education.

Final deliverables:
1. ml_university_attrition_taiwan.tex (main text)
2. references.bib (citations)
3. figures/ (figures and tables)
4. cover_letter.tex (submission cover letter draft)

Pre-submission recommendations:
- Read through the cover letter one more time, adjust to your tone
- Confirm C&E Author Guidelines for any additional formatting requirements
- Prepare Highlights (3-5 bullet points) and Graphical Abstract
```
<!-- SOURCE-CONTENT-END -->
