<a id="source-skills-academic-paper-references-anti-leakage-protocol-md"></a>

## SOURCE: skills/academic-paper/references/anti_leakage_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=4273 -->
# Anti-Leakage Protocol (Knowledge Isolation)

**Status**: v3.3
**Used by**: `draft_writer_agent`, `report_compiler_agent`
**Source**: Adapted from PaperOrchestra (Song et al., 2026, Appendix D.4)

---

## Purpose

When the user provides comprehensive research materials (RQ Brief, Synthesis Report, Annotated Bibliography, experimental data), the writing agent should construct the paper **primarily from those materials**, not from LLM parametric memory. This prevents:

1. **Methodology fabrication (Failure Mode 6)**: The LLM writes a plausible Methods section from training data rather than the user's actual procedure
2. **Implicit knowledge leakage**: The LLM fills gaps with memorized content that may be inaccurate, outdated, or from a different context
3. **Unintentional plagiarism**: The LLM reproduces near-verbatim passages from training data

---

## Protocol

### When to activate

Activate when ALL of the following are true:
- The user has provided research materials via the pipeline handoff (RQ Brief + Synthesis Report + Annotated Bibliography)
- The paper is in `full` or `revision` mode (not `plan` or `outline-only`)
- The materials are substantive (not placeholder stubs)

### When NOT to activate

Do NOT activate when:
- The user is in `plan` or `socratic` mode (exploratory — LLM knowledge is expected)
- The materials are minimal (e.g., only a RQ Brief with no bibliography)
- The user explicitly requests the LLM to supplement with its own knowledge

### Prompt insertion

When activated, prepend the following to the draft_writer_agent's working context:

```
## Knowledge Isolation Directive

You are writing this paper based on the research materials provided in this session:
- RQ Brief, Synthesis Report, and Annotated Bibliography (from deep-research)
- Any additional materials the user has provided (experimental logs, datasets, prior drafts)

Priority rules:
1. PREFER session materials over your parametric knowledge for all factual claims
2. Every claim in the paper MUST be traceable to a source in the Annotated Bibliography or user-provided data
3. If the materials do not cover a topic the outline requires, flag it as [MATERIAL GAP] rather than filling from memory
4. Do NOT introduce references not present in the Annotated Bibliography unless explicitly asked by the user
5. The Methods section must describe ONLY what is documented in the user's materials — do not infer or interpolate experimental procedures

This is NOT a prohibition on using language skills or academic writing knowledge.
You may use your knowledge of academic conventions, writing style, logical argumentation,
and discipline norms. The restriction applies only to FACTUAL CONTENT — claims, citations,
data, and methodology descriptions must come from session materials.
```

### [MATERIAL GAP] handling

> **Tag vocabulary.** The `[MATERIAL GAP]`, `[WEAK EVIDENCE]`, `[GAP]` tags used throughout this protocol are canonically defined in [`shared/compliance_checkpoint_protocol.md#canonical-gap-tag-vocabulary`](../../shared/compliance_checkpoint_protocol.md#canonical-gap-tag-vocabulary). This section describes how the anti-leakage writing-time flag interacts with that vocabulary during manuscript production.

When a `[MATERIAL GAP]` is flagged:
1. The gap is surfaced at the next checkpoint
2. The user can provide additional materials, or authorize LLM supplementation for that specific gap
3. If supplemented: the gap section is tagged `[LLM-SUPPLEMENTED]` in the draft metadata for integrity review

---

## Relationship to existing checks

| Check | What it catches | Anti-leakage adds |
|-------|----------------|-------------------|
| Integrity gate (Stage 2.5) | Fabricated citations post-hoc | Prevents fabrication at writing time |
| Failure Mode 6 (Methodology fabrication) | Methods don't match actual procedures | Prevents LLM from inventing procedures |
| Writing Quality Check | AI-typical phrasing patterns | Anti-leakage prevents AI-typical *content* (as opposed to style) |

---

## References

- Song, Y. et al. (2026). PaperOrchestra. *arXiv:2604.05018*. Appendix D.4 (Anti-Leakage Prompt).
- Lu, C. et al. (2026). Towards end-to-end automation of AI research. *Nature* 651, 914-919. — Mode 6 (Methodology fabrication).
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-references-changelog-md"></a>

## SOURCE: skills/academic-paper/references/changelog.md

<!-- SOURCE-CONTENT-BEGIN bytes=2821 -->
# Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.5 | 2026-03-27 | Style Calibration (intake Step 10: learn author's writing voice from 3+ past papers, produce Style Profile with 6 dimensions, consumed by draft_writer as soft guide with discipline-convention priority). Writing Quality Check (`references/writing_quality_check.md`: 25-term AI high-frequency word warnings, em dash limits, throat-clearing detection, structural pattern warnings, burstiness checks — applied in draft_writer self-review). Style Profile carried through academic-pipeline Material Passport (Schema 10 in `shared/handoff_schemas.md`). deep-research report_compiler also consumes both features optionally |
| 2.4 | 2026-03-08 | LaTeX output formatting hardening: mandatory `apa7` document class for APA 7.0 output; text justification fix (`ragged2e` + `etoolbox` to override apa7 man mode `\raggedright`); table column width formula (`(\linewidth - N\tabcolsep) * \real{proportion}` — prevents overflow); bilingual abstract centering (`\begin{center}\textbf{...}\end{center}`); font stack standardized (Times New Roman + Source Han Serif TC VF + Courier New); `xurl` for URL line breaking; `fancyvrb` Verbatim with `fontsize` for wide content; PDF must compile from LaTeX via tectonic (no HTML-to-PDF) |
| 2.3 | 2026-03-08 | NEW visualization_agent (11th: publication-quality figures with matplotlib/ggplot2, APA 7.0, colorblind-safe); NEW revision_coach_agent (12th: standalone reviewer comment parser → Revision Roadmap); Socratic convergence criteria (4 signals: thesis clarity, chapter coherence, evidence mapping, limitation honesty) + question taxonomy (clarifying, probing, structuring, challenging); revision tracking template (4 status types); citation format conversion in formatter_agent (APA 7 ↔ Chicago ↔ MLA ↔ IEEE ↔ Vancouver); Quick Mode Selection Guide; 9th mode: revision-coach |
| 2.2 | 2026-03-05 | 4-level argument strength scoring with quantified thresholds; plagiarism & retraction screening protocol; F11 Desk-Reject Recovery + F12 Conference-to-Journal Conversion failure paths; Plan -> Full mode conversion protocol; cross-skill reference to `shared/handoff_schemas.md` |
| 2.1 | 2026-03 | Added CRediT authorship guide, funding statement guide, 2 new templates (credit_statement_template, funding_statement_template); enhanced intake_agent with co-author + funding questions (Step 9-10); enhanced formatter_agent with CRediT + funding quality checks |
| 2.0 | 2026-02 | NEW plan mode (Socratic guided chapter-by-chapter planning), deep-research handoff protocol, Chinese APA 7.0 citation guide, failure path handling, mode selection guide |
| 1.0 | 2026-01 | Initial release: 9-agent pipeline, 6 paper types, 5 citation formats, bilingual abstracts, multi-format output |
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-references-disclosure-mode-protocol-md"></a>

## SOURCE: skills/academic-paper/references/disclosure_mode_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=12764 -->
# Disclosure Mode Protocol

**Status**: v3.2 (#108 extension: parallel `--policy-anchor=<a>` path; v3.2 venue path unchanged)
**Parent skill**: `academic-paper`
**Mode name**: `disclosure`
**Purpose**: Generate either (a) a venue-specific AI-usage disclosure statement that complies with the target venue's current AI policy (v3.2 path, default), or (b) a policy-anchor-specific disclosure rendered from the 4-anchor matrix (PRISMA-trAIce / ICMJE / Nature / IEEE) when the author targets a policy anchor rather than a specific journal venue (#108 path).

---

## Two parallel tracks (#108 + v3.2)

The `disclosure` mode dispatches on the author-supplied selector:

| Selector | Track | Lookup source | Output shape |
|---|---|---|---|
| `--venue=<v>` (v3.2, default) | Venue track | `venue_disclosure_policies.md` v1 database (ICLR / NeurIPS / Nature / Science / ACL / EMNLP) | Single venue-tailored disclosure paragraph + placement instruction |
| `--policy-anchor=<a>` (#108) | Anchor track | `policy_anchor_table.md` 4-anchor × 16-field matrix | 4-anchor-conditioned render per `policy_anchor_disclosure_protocol.md` |

The two tracks are **selector-mutually-exclusive by default** — one selector picks one track. When the author supplies **both** selectors in the same invocation, the renderer evaluates compatibility per concern #7 rules: a consistent pair (Nature venue + nature anchor, both sourced from `shared/policy_data/nature_policy.md`) proceeds; any other pair is **rejected with an explicit error** listing the policy conflict. Silent precedence between selectors is forbidden. See [policy_anchor_disclosure_protocol.md §5](policy_anchor_disclosure_protocol.md) for the full conflict-resolution detail.

If neither selector is supplied and the pipeline orchestrator does not infer one from upstream context, the mode prompts the user to specify which selector applies. The venue track remains the default for explicit journal submissions; the anchor track applies when targeting policy frameworks (e.g., compliance reporting to ICMJE-adopting journals collectively, or pre-submission alignment to IEEE author guidelines).

**Conflict resolution (concern #7) — exhaustive cases:**
- Supplied both, **consistent pair** (only currently defined case): `--venue=Nature` (any Nature Portfolio variant string) **and** `--policy-anchor=nature` → both target Nature substantive policy via the shared source pointer → **proceed**.
- Supplied both, **any other combination** (e.g., `--venue=Nature` + `--policy-anchor=ieee`; `--venue=ICLR` + `--policy-anchor=icmje`; or a Nature-venue spelling that does not match the canonical set with a non-nature anchor) → **reject** with explicit error citing the policy conflict; require the user to drop one selector. Silent precedence is forbidden by §4.4 #7.
- Supplied only one selector → run that track.
- Supplied neither selector → prompt the user to specify.

---

## Why this mode exists

`academic-paper` already ships two generic AI disclosure templates in `journal_submission_guide.md` ("Minimal Disclosure" and "Detailed Disclosure"). Those templates are a good starting point but they are venue-agnostic: they don't know that Nature requires disclosure in the Methods section specifically, that ICLR requires it in the paper body with acknowledgement that "LLMs were used as general-purpose writing tools", or that ACL requires the disclosure in a dedicated "Use of AI Assistance" subsection.

The v3.2 venue track closes the venue-specific gap. The #108 anchor track closes the policy-framework-specific gap that emerges when authors target a policy anchor (PRISMA-trAIce SLR guideline, ICMJE recommendations, Nature Portfolio editorial policy, IEEE author guidelines) rather than a specific journal venue.

---

## Inputs

1. **Paper draft**: current manuscript text (the mode needs to know what the AI actually did in order to describe it accurately).

2. **Selector** (one of):
   - **Target venue (`--venue=<v>`)**: journal or conference name (v3.2 path). If the venue is in the v1 database (ICLR, NeurIPS, Nature, Science, ACL, EMNLP), use the cached policy. If not, refuse to guess — prompt the user to paste the venue's current AI policy text from the venue's submission page.
   - **Policy anchor (`--policy-anchor=<a>`)**: one of `prisma-trAIce, icmje, nature, ieee` (#108 path). Anchor lookup follows `policy_anchor_disclosure_protocol.md`.

3. **Pipeline signal** (#108 anchor path only): `slr_lineage=true|false` set by the upstream pipeline orchestrator. Required for `--policy-anchor=prisma-trAIce` per §4.3 G2 invariant. Cold-start invocation requires explicit `mode=<value>` parameter; silent fallback to general track is forbidden.

4. **What ARS did**: the mode reads the paper's commit history / pipeline log (if using the full `academic-pipeline`) to identify which AI-assisted steps produced which parts of the paper. At minimum: research assistance, drafting assistance, revision assistance, citation checking, peer review simulation. If the pipeline log is not available, ask the user to confirm which categories apply.

---

## Process

### Phase 1: Intake + lookup (selector-aware)

**Step 1a — selector dispatch:**
- Both `--venue=<v>` and `--policy-anchor=<a>` supplied → check policy compatibility per the Two-parallel-tracks section above. **Consistent pair (currently only any Nature Portfolio venue + `--policy-anchor=nature`, where "Nature Portfolio venue" includes canonical labels {"Nature", "Nature Portfolio", "Nature (Nature Publishing Group)", "Nature Publishing Group"} and the journal-family prefix `"Nature "` matching e.g. "Nature Medicine", "Nature Communications", "Nature Climate Change", etc.) → route the consistent pair to **step 1c (anchor path)** so the shared canonical source `shared/policy_data/nature_policy.md` drives rendering; step 1b's v1 venue database does not need to contain every Nature Portfolio journal**. Conflicting pair → reject with explicit error.
- `--venue=<v>` only → step 1b (venue path).
- `--policy-anchor=<a>` only → step 1c (anchor path).
- Neither supplied → prompt the user to specify selector.

**Step 1b — venue lookup (v3.2 path, unchanged):**
- If venue is in the v1 database → load policy from `venue_disclosure_policies.md`.
- If venue is unknown → halt. Print: "I do not have a cached policy for {venue}. Please paste the venue's current AI-usage / generative-AI policy text so I don't guess." Do NOT fabricate a policy.
- If the user pastes a policy for an unknown venue, use it for this session only. Do NOT auto-persist it to the database — policies drift, and the database needs curation.

**Step 1c — anchor lookup (#108 path):**
- Validate `--policy-anchor=<a>` ∈ `{prisma-trAIce, icmje, nature, ieee}`. Other values → reject with the closed-enum error.
- For `--policy-anchor=prisma-trAIce`: confirm `slr_lineage=true` (pipeline signal) or `mode=systematic-review` (cold-start input) per the G2 invariant track gate. Otherwise refuse with G2 invariant citation.
- Delegate Phase 3 + Phase 4 to `policy_anchor_disclosure_protocol.md` per-anchor render flows. Phase 2 (AI usage categorization) and Phase 5 (placement instructions) are shared with the venue path with the anchor-specific routing applied inside Phase 3/4.

### Phase 2: Categorize AI usage

Produce a categorized list of how AI was used in the manuscript:

| Category | Examples |
|---|---|
| Research assistance | Literature search, annotated bibliography, claim verification |
| Drafting assistance | Section drafting, paraphrasing, outline generation |
| Revision assistance | Reviewer response drafting, tracked changes, consistency checking |
| Editing assistance | Grammar, style, formatting, citation format conversion |
| Analysis assistance | Not applicable to pure writing flows; flag if the paper reports any analysis the AI did |
| Peer review simulation | `academic-paper-reviewer` was used on the draft pre-submission |

For each category, mark: USED / NOT USED / UNCERTAIN. UNCERTAIN items require user confirmation before the disclosure text is finalized.

### Phase 3: Match categories to the venue's required phrasing

Each venue in the policy database specifies (a) which categories are mandatory to disclose, (b) which are optional, (c) which are prohibited (e.g., analysis assistance may require separate disclosure at some venues). The mode matches the user's category list against the venue's requirements and flags any mismatch (e.g., "Venue requires disclosure of research assistance; your categorization marked it UNCERTAIN").

### Phase 4: Generate the disclosure text

Generate a single disclosure paragraph using:
- The venue's preferred voice (first person vs passive, past tense vs present)
- The venue's required phrasing elements (many venues require the phrase "The authors take full responsibility for the content" or equivalent)
- The specific tool name — "Claude (Anthropic) via Academic Research Skills pipeline" — not generic "AI tools"
- The specific categories marked USED

Example output for Nature (which requires disclosure in Methods):

```
## AI-assisted tools

The authors used Claude [MODEL_VERSION] (Anthropic), orchestrated via the
Academic Research Skills pipeline (Wu, 2026), during the preparation
of this manuscript. Specifically, the tool was used for literature
search assistance, citation verification, drafting of section outlines,
and internal peer-review simulation prior to submission. All
AI-assisted output was reviewed, edited, and verified by the authors,
who take full responsibility for the content of this article.
```

**Note**: Replace `[MODEL_VERSION]` with the actual model used in this run (e.g., `Opus 4.7`, `Sonnet 4.6`). Pull the identifier from session metadata rather than hard-coding a version, since Anthropic's lineup changes over time.

### Phase 5: Placement instructions

Output includes explicit placement instructions matching the venue's policy:

```
Placement: Methods section (Nature policy, accessed YYYY-MM-DD from
https://www.nature.com/.../policy-url). Include as the final
subsection of Methods, before Data Availability.
```

If the venue requires placement in multiple locations (e.g., Methods + cover letter + Acknowledgements), the mode generates tailored text for each location rather than a single paragraph.

---

## Failure cases this mode does NOT cover

- **Venues outside the v1 database**: the mode halts and asks the user. It does not guess.
- **Policies that have changed since the database snapshot**: the mode records the access date in the placement instructions. Users should verify against the current venue page before submission.
- **Analysis assistance**: if the AI actually ran computations or generated analysis results (not just writing), most venues require a separate disclosure in a Code Availability or Analysis section. This mode flags the case and produces a separate paragraph; the user must place it manually.
- **Co-authored AI**: as of the 2026 policy snapshot, no venue in the v1 database accepts AI as a listed author. The mode refuses to produce author-list text and instead produces authorship-rejection text plus the disclosure.

---

## Integration with existing journal_submission_guide.md

`journal_submission_guide.md` retains the two generic templates (Minimal / Detailed) as fallback for venues not in the v1 database. Disclosure mode's output supersedes those templates when the venue is known. The guide is updated to point to this mode for known venues.

---

## References

- `venue_disclosure_policies.md` — v1 policy database (ICLR, NeurIPS, Nature, Science, ACL, EMNLP)
- `policy_anchor_table.md` — #108 4-anchor × 16-field matrix (PRISMA-trAIce, ICMJE, Nature, IEEE) for the policy-anchor track
- `policy_anchor_disclosure_protocol.md` — #108 policy-anchor track render protocol (per-anchor flows, G10 7-row precedence table, auto-promotion forbiddance, §4.4 11 concerns resolved paths)
- `journal_submission_guide.md` — existing generic templates (fallback)
- `credit_authorship_guide.md` — existing CRediT authorship best practices
- Lu et al. (2026). Towards end-to-end automation of AI research. *Nature* 651, 914-919 — the ethics statement for Lu 2026 was drafted in compliance with Nature's policy; their methodology is a worked example of what this mode should produce.
- `docs/design/2026-05-14-ai-disclosure-schema-decision.md` — #108 Decision Doc (G1-G10 + §4.3 invariants + §4.4 11 open concerns)
- `docs/design/2026-05-14-ai-disclosure-impl-spec.md` — #108 implementation spec (resolved-paths table)
- ROADMAP_v3.2.md item 6 — design decisions (v1 venue set, unknown-venue halt, education/QA venues deferred to v2)
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-references-failure-paths-md"></a>

## SOURCE: skills/academic-paper/references/failure_paths.md

<!-- SOURCE-CONTENT-BEGIN bytes=14163 -->
# Failure Paths — Academic Paper Writing Failure Path Map

This document records the failure scenarios that the academic-paper skill may encounter at each stage, their trigger conditions, and handling strategies. All agents should refer to this guide when they detect a failure scenario.

---

## Failure Path Overview

| # | Failure Scenario | Trigger Condition | Severity | Handling Strategy |
|---|---------|---------|--------|---------|
| F1 | Insufficient research foundation | Plan mode Step 0 finds no RQ / no data | High | Recommend running `deep-research` first |
| F2 | Wrong paper structure selected | structure_architect finds RQ-structure mismatch | Medium | Return to Phase 2, suggest alternative structures |
| F3 | Severely over word count | Draft exceeds target word count by 30% or more | Medium | Identify sections to cut, suggest condensing |
| F4 | Severely under word count | Draft is 30% or more below target word count | Medium | Identify sections to expand, suggest additions |
| F5 | Citation format entirely wrong | citation_compliance finds > 50% format errors | High | Completely re-run citation phase |
| F6 | Poor bilingual abstract quality | Chinese and English abstracts have inconsistent logic | Medium | Re-run abstract_bilingual |
| F7 | Peer review rejection | peer_reviewer issues a Reject verdict | High | Analyze rejection reasons, recommend major revision or restructuring |
| F8 | Plan mode does not converge | > 15 rounds of dialogue without completing all chapters | Medium | Suggest switching to outline-only mode |
| F9 | Incomplete handoff materials | From deep-research but missing key materials | Low | List missing items, suggest supplementing or re-running |
| F10 | User abandons midway | Explicitly states unwillingness to continue | Low | Save completed Chapter Plan |
| F11 | Desk-reject | Journal editor rejects without sending to reviewers | High | Classify rejection cause, select recovery strategy |
| F12 | Conference-to-journal conversion failure | Conference paper expansion to journal article rejected | Medium | Ensure 30-50% new content + proper citation |

---

## Detailed Handling Strategies

### F1: Insufficient Research Foundation

**Trigger Timing**: Plan mode Step 0 (Research Readiness Check) or Full mode Phase 0

**Detection Indicators**:
- User cannot describe their research question in one sentence
- No literature foundation
- No concept of research methods
- Topic is too broad and cannot be focused

**Handling Process**:
```
1. Affirm the user's research interest
2. Specifically explain what is currently missing
3. Recommend using deep-research (socratic mode)
4. Explain that they can come back to continue after deep-research is completed
5. If the user insists on continuing, switch to outline-only mode (low risk)
```

**Response Template**:
```
Your research topic is very interesting, but I notice that a clear research question
and literature foundation are still missing.

I recommend you first use the deep-research tool to:
1. Systematically search and organize relevant literature
2. Focus on a researchable question
3. Gain a preliminary understanding of possible research methods

Once completed, bring the materials back and we can produce a high-quality paper
more efficiently.
```

---

### F2: Wrong Paper Structure Selected

**Trigger Timing**: Phase 2 (structure_architect_agent)

**Detection Indicators**:
- RQ is a causal question but a Literature Review structure was selected
- No data but IMRaD was selected
- Topic suits a Case Study but Policy Brief was selected
- Word count target and structure are mismatched (e.g., 3000-word IMRaD)

**Handling Process**:
```
1. Point out the mismatch between RQ and structure
2. Explain why they are mismatched
3. Suggest 1-2 alternative structures
4. Explain how the alternative structures better answer the RQ
5. Return to Phase 2 to let the user re-select
```

---

### F3: Severely Over Word Count

**Trigger Timing**: Phase 4 (after draft_writer_agent completes)

**Detection Indicators**:
- Actual word count > target word count x 1.3

**Handling Process**:
```
1. List actual word count vs. target word count for each chapter
2. Identify the most over-count chapters
3. Suggest reduction strategies:
   a. Merge duplicate arguments
   b. Condense the literature review (keep core literature)
   c. Remove overly detailed method descriptions
   d. Compress repeated literature dialogue in Discussion
4. Do not proactively delete; let the user decide
```

---

### F4: Severely Under Word Count

**Trigger Timing**: Phase 4 (after draft_writer_agent completes)

**Detection Indicators**:
- Actual word count < target word count x 0.7

**Handling Process**:
```
1. List actual word count vs. target word count for each chapter
2. Identify the most deficient chapters
3. Suggest expansion strategies:
   a. Increase the depth and breadth of the literature review
   b. Add more evidence and examples
   c. Expand Discussion (more literature dialogue)
   d. Add more detail to methodology descriptions
4. Provide specific expansion directions
```

---

### F5: Citation Format Entirely Wrong

**Trigger Timing**: Phase 5a (citation_compliance_agent)

**Detection Indicators**:
- Citation format error rate > 50%
- Systematic errors (e.g., all missing DOIs, all using wrong format)

**Handling Process**:
```
1. Analyze error patterns (systematic vs. scattered)
2. If systematic errors:
   a. Identify root cause (user may have selected the wrong citation format)
   b. Confirm the correct citation format
   c. Completely re-run citation phase
3. If scattered errors:
   a. Fix one by one
   b. Produce a correction report
```

---

### F6: Poor Bilingual Abstract Quality

**Trigger Timing**: Phase 5b (abstract_bilingual_agent)

**Detection Indicators**:
- Chinese and English abstracts cover different key points
- One language version omits important findings
- Keywords do not correspond between Chinese and English
- Word count seriously deviates from standards

**Handling Process**:
```
1. Compare the structure and coverage of Chinese and English abstracts
2. List inconsistencies
3. Rewrite based on the actual paper content as the standard
4. Ensure both versions are independently written but cover the same key points
```

---

### F7: Peer Review Rejection

**Trigger Timing**: Phase 6 (peer_reviewer_agent issues Reject)

**Detection Indicators**:
- Two or more of the five dimensions scored below 60
- Fatal flaws exist (logical breakdowns, missing core evidence, serious methodology flaws)

**Handling Process**:
```
1. List all issues flagged as Critical
2. Classify the nature of the problems:
   a. Fixable (writing, formatting, minor logic issues) → Recommend Major Revision
   b. Structural issues (argument architecture needs reorganization) → Return to Phase 3 for restructuring
   c. Fundamental issues (RQ infeasible, insufficient data) → Return to Phase 0 for re-evaluation
3. Produce a revision roadmap
4. Execute revision after user confirmation
```

**Note**: If still Reject after 2 rounds of revision, recommend the user to:
- Consult domain experts
- Rethink the research design
- Consider switching target journals (lower the bar)

---

### F8: Plan Mode Does Not Converge

**Trigger Timing**: Plan mode dialogue exceeds 15 rounds

**Detection Indicators**:
- User repeatedly modifies the direction of the same chapter
- Unable to make definitive decisions
- Discussion drifts off the paper topic

**Handling Process**:
```
1. Pause and summarize what has been determined so far
2. List completed and uncompleted chapters
3. Provide two options:
   a. Jump to outline-only mode (directly produce an outline)
   b. Continue dialogue (but narrow the scope of each discussion)
4. Save the completed Chapter Plan
```

---

### F9: Incomplete Handoff Materials

**Trigger Timing**: intake_agent detects deep-research materials but they are incomplete

**Detection Indicators**:
- Has RQ but missing Annotated Bibliography
- Has Bibliography but missing Synthesis Report
- Has INSIGHT Collection but some INSIGHTs are incomplete

**Handling Process**:
```
1. List received and missing materials
2. Assess the impact of missing materials:
   a. Missing Bibliography → Need Phase 1 (literature_strategist)
   b. Missing Synthesis → Can continue, Phase 3 handles it additionally
   c. Missing Methodology Blueprint → Need Phase 0 supplementary questions
3. Recommend:
   a. Return to deep-research to complete the missing parts
   b. Or supplement within academic-paper (add Phase 0 interview questions)
```

---

### F10: User Abandons Midway

**Trigger Timing**: User explicitly states unwillingness to continue

**Detection Indicators**:
- "Forget it" / "Not writing anymore" / "Too complicated" / "Let me think about it"
- Abandons after prolonged unresponsiveness

**Handling Process**:
```
1. Respect the user's decision
2. Save all completed outputs:
   - Paper Configuration Record
   - Chapter Plan (completed portions)
   - INSIGHT Collection
   - Any completed draft sections
3. Inform the user they can come back anytime with these materials to continue
4. Do not actively persuade them to continue (but encouragement is fine)
```

**Save Format**:
```markdown
## Academic Paper — Saved Record

**Topic**: {topic}
**Progress**: Phase {N} / Step {M}
**Completed**:
- [x] Paper Configuration Record
- [x/partial] Chapter Plan (completed {N}/{total} chapters)
- [ ] Draft
- [ ] Citation check
- [ ] Peer review

**How to Resume**: Bring this record and restart academic-paper; can continue from Phase {N}
```

---

## Relationships Between Failure Paths

```
F1 (Insufficient research foundation) → Recommend deep-research → May encounter F9 (incomplete materials) upon return
F2 (Wrong structure) → Return to Phase 2 → May cascading affect F3/F4 (word count issues)
F5 (All citations wrong) → May be a downstream effect of F2 (wrong format selected)
F7 (Rejection) → Analysis may require returning to F2 (structure) or F1 (foundation)
F8 (Non-convergence) → May evolve into F10 (abandonment)
```

### F11: Desk-Reject Recovery

**Trigger**: Editor rejects the paper without sending to reviewers.

**Cause Classification & Recovery**:

| Cause | Diagnostic Signs | Recovery Strategy |
|-------|-----------------|-------------------|
| **Scope Mismatch** | Editor states "outside journal scope" or "not aligned with journal aims" | Re-analyze journal scope using `top_journals_by_field.md`; identify 3 alternative journals; may need to reframe the paper's contribution |
| **Insufficient Novelty** | "Incremental contribution" or "well-established findings" | Strengthen the novelty claim in introduction; consider additional analysis or a new dataset; reposition the paper's unique contribution |
| **Formatting Non-Compliance** | Immediate rejection for template/length/style violations | Review target journal's author guidelines; use `formatter_agent` to reformat; resubmit (often same journal accepts after formatting fix) |
| **Poor Opening** | No specific reason given; likely the abstract/introduction failed to hook | Rewrite abstract with the CARS model (Create A Research Space); lead with the gap, not the background; have `peer_reviewer_agent` evaluate the new opening |

**General Protocol**:
1. Do NOT take desk-reject personally — 30-50% of submissions to top journals are desk-rejected
2. Read the editor's email carefully for any specific feedback
3. Determine the cause category above
4. If Scope Mismatch: pivot journal, not paper
5. If Novelty/Opening: revise paper, then resubmit (different journal recommended)
6. Turnaround target: 2 weeks for reformatting, 4 weeks for substantive revision

---

### F12: Conference-to-Journal Conversion Failure

**Trigger**: Attempt to expand a published conference paper into a journal article fails review.

**Common Rejection Reasons & Solutions**:

| Reason | Solution |
|--------|----------|
| **Insufficient Extension** (< 30% new content) | Journal expects 30-50% new material beyond the conference version. Add: extended related work, additional experiments/data, deeper analysis, new discussion sections |
| **Self-Plagiarism Flag** | Explicitly cite the conference version in the introduction: "This paper extends our previous work [conf-citation] with..." Use iThenticate to verify < 30% text overlap |
| **Stale Results** | If the conference paper is > 2 years old, results may be outdated. Update experiments with current data/baselines; acknowledge temporal limitations |
| **Missing Journal Standards** | Conference papers often lack: detailed methodology, reproducibility information, limitations section, broader impact discussion. Add all of these |

**Conversion Checklist**:
- [ ] Conference version explicitly cited in introduction
- [ ] 30-50% genuinely new content added (not just padding)
- [ ] Text overlap with conference version < 30% (verified by similarity tool)
- [ ] All reviewer expectations for a journal-length paper met
- [ ] Notation in cover letter: "This is an extended version of [conference paper]"
- [ ] Check journal policy: some journals prohibit conference-to-journal conversion

---

## Preventive Measures

| Failure Path | Preventive Measure |
|---------|---------|
| F1 | Phase 0 / Step 0 strictly checks research readiness |
| F2 | structure_architect cross-validates the match between RQ and structure |
| F3/F4 | draft_writer checks word count progress after completing each section |
| F5 | draft_writer uses the correct format during writing |
| F6 | abstract_bilingual writes independently based on the paper content as the standard |
| F7 | argument_builder stress-tests arguments in Phase 3 |
| F8 | socratic_mentor sets a dialogue cap per chapter |
| F9 | intake_agent performs a complete materials check when detecting a handoff |
| F10 | Maintain dialogue rhythm to avoid user fatigue |
| F11 | Phase 7 researches target journal scope when producing the cover letter; format_agent strictly follows formatting rules |
| F12 | intake_agent detects whether this is a conference paper expansion; calculate new content ratio early |
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-references-mode-selection-guide-md"></a>

## SOURCE: skills/academic-paper/references/mode_selection_guide.md

<!-- SOURCE-CONTENT-BEGIN bytes=12396 -->
# Mode Selection Guide

This guide helps users and the `intake_agent` select the most appropriate operational mode.

---

## Mode Selection Flowchart

```
User Input →
│
├── Already have complete research?
│   ├── Yes → Want a full paper?
│   │   ├── Yes ─────────────────────────→ full mode
│   │   └── No → Just need an outline?
│   │       ├── Yes ─────────────────────→ outline-only mode
│   │       └── No → Just need an abstract?
│   │           ├── Yes ──────────────────→ abstract-only mode
│   │           └── No → Just need a literature review?
│   │               ├── Yes ─────────────→ lit-review mode
│   │               └── No ──────────────→ full mode
│   │
│   └── No → Want guided thinking?
│       ├── Yes ─────────────────────────→ plan mode ★ NEW
│       └── No ──────────────────────────→ full mode (Phase 0 will conduct an interview)
│
├── Have an existing paper to revise? ──────────────────────→ revision mode
├── Just need format conversion? ────────────────────────→ format-convert mode
└── Just need a citation check? ────────────────────────→ citation-check mode
```

---

## Detailed Description of Each Mode

### full mode — Complete Paper Writing

**Applicable Scenarios**:
- User has a clear research question and (partial) materials
- Needs to produce a complete paper from start to finish
- Includes all phases: Interview → Literature → Structure → Argumentation → Writing → Citation → Review → Formatting

**Not Applicable When**:
- User has no idea about research direction (→ use `deep-research` first)
- Only need a specific section (→ use another specialized mode)

**Expected Output**: Complete paper draft + references + bilingual abstract + review report
**Expected Duration**: Long (all 8 Phases fully executed)
**Agents Used**: All 9 + socratic_mentor (if needed)

---

### outline-only mode — Outline Generation

**Applicable Scenarios**:
- Only need the paper structure and outline
- A proposal to submit to an advisor for review
- Need to quickly plan the paper structure

**Not Applicable When**:
- Need complete paper content (→ full mode)
- Need guided thinking (→ plan mode)

**Expected Output**: Detailed outline + evidence allocation + word count distribution
**Expected Duration**: Short (Phase 0-2)
**Agents Used**: intake → literature_strategist → structure_architect

---

### plan mode — Chapter-by-Chapter Guided Planning ★ NEW

**Applicable Scenarios**:
- User has ideas but they are not yet clear enough
- Wants guided thinking for each chapter's content
- First-time academic paper writer
- Wants to think through every section before writing
- Just received materials from deep-research and needs to transform them into a paper plan

**Not Applicable When**:
- Already knows exactly what to write (→ full mode is faster)
- Only needs an outline without deep thinking (→ outline-only mode)
- Time-pressured and needs rapid output (→ full mode)

**Expected Output**: Chapter Plan + INSIGHT Collection
**Expected Duration**: Medium (Step 0-3, approximately 20-30 rounds of conversation)
**Agents Used**: intake → socratic_mentor → structure_architect → argument_builder

**Subsequent Connections**:
- Chapter Plan → full mode (produce complete paper)
- Chapter Plan → academic-paper-reviewer (review the plan)

---

### revision mode — Paper Revision

**Applicable Scenarios**:
- Already have a completed paper draft
- Received reviewer comments requiring revision
- Feel certain sections need improvement

**Not Applicable When**:
- No existing paper draft (→ full mode)
- Only need to check citation format (→ citation-check mode)

**Expected Output**: Revised paper + revision notes (tracked changes)
**Expected Duration**: Medium
**Agents Used**: peer_reviewer → draft_writer → citation_compliance

**Prerequisite**: User must provide existing paper content

---

### abstract-only mode — Abstract Writing

**Applicable Scenarios**:
- Paper is already complete, only need an abstract
- Need to submit a conference abstract
- Need a bilingual abstract

**Not Applicable When**:
- No paper content to summarize (→ full mode or plan mode)

**Expected Output**: Bilingual abstract (zh-TW + EN) + keywords
**Expected Duration**: Short
**Agents Used**: intake → abstract_bilingual

---

### lit-review mode — Literature Review

**Applicable Scenarios**:
- Need a literature review on a specific topic
- Preparing the Literature Review chapter of a paper
- Need a systematic search strategy and literature matrix

**Not Applicable When**:
- Need a complete paper (→ full mode)
- Need an in-depth research investigation (→ deep-research)

**Expected Output**: Annotated bibliography + literature matrix + synthesis analysis
**Expected Duration**: Medium
**Agents Used**: intake → literature_strategist

---

### format-convert mode — Format Conversion

**Applicable Scenarios**:
- Already have paper content, need format conversion
- Markdown → LaTeX / DOCX / PDF
- Need to comply with a specific journal's formatting requirements

**Not Applicable When**:
- No existing content (→ full mode)
- Need content modifications (→ revision mode)

**Expected Output**: Document in target format
**Expected Duration**: Short
**Agents Used**: formatter used standalone

---

### citation-check mode — Citation Check

**Applicable Scenarios**:
- Already have a paper, only need to check citation format
- Final check before submission
- Switching citation format (e.g., APA → IEEE)

**Not Applicable When**:
- No existing citation list (→ full mode)
- Need to modify paper content (→ revision mode)

**Expected Output**: Citation error report + automatic correction suggestions
**Expected Duration**: Short
**Agents Used**: citation_compliance used standalone

---

## Paths from deep-research

```
deep-research completed
  │
  ├── deep-research (full mode) outputs:
  │   RQ Brief + Methodology Blueprint + Annotated Bibliography + Synthesis Report
  │   │
  │   ├── Want to write the paper directly ──→ academic-paper (full mode)
  │   │   intake_agent auto-detects materials, skips redundant questions
  │   │
  │   └── Want to plan before writing ──→ academic-paper (plan mode)
  │       socratic_mentor leverages existing materials to accelerate guidance
  │
  └── deep-research (socratic mode) outputs:
      INSIGHT Collection + Synthesis Report
      │
      ├── INSIGHTs are sufficiently clear ──→ academic-paper (full mode)
      │
      └── Need more guidance ──→ academic-paper (plan mode)
          socratic_mentor continues deepening from INSIGHTs
```

## Connecting to academic-paper-reviewer

```
academic-paper completed
  │
  ├── full mode produces complete paper ──→ academic-paper-reviewer (full / guided)
  │   Complete peer review + revision suggestions
  │
  ├── plan mode produces Chapter Plan ──→ academic-paper-reviewer (guided)
  │   Review the plan's feasibility and completeness
  │
  └── reviewer feedback ──→ academic-paper (revision mode)
      Revise paper based on review comments
```

---

## Common Misselection Scenarios

| User Says | Easily Misselected | Correct Choice | Reason |
|---------|---------|---------|------|
| "Help me write an outline" / 「幫我寫大綱」 | outline-only | First confirm: Do they want a simple outline or deep planning? | May need plan mode |
| "I want to write a paper but don't know how to start" / 「想寫論文但不知道怎麼開始」 | full | plan mode | Needs guided thinking |
| "Help me revise my paper" / 「幫我修改論文」 | revision | First confirm: Are there reviewer comments? | May need full mode rewrite |
| "Help me search for literature" / 「幫我找文獻」 | lit-review | First confirm: Is it a literature review for a paper or a research investigation? | May need deep-research |
| "I have deep-research results, help me write a paper" / 「我有研究結果，幫我寫成論文」 | full (skip Phase 0 directly) | full (but intake needs to detect handoff) | Materials need to be properly imported |
| "I want to plan my paper step by step" / 「我想逐步規劃論文」 | outline-only | plan mode | Needs interactive guidance |
| "The paper format is wrong" / 「論文格式不對」 | revision | citation-check or format-convert | May only need format correction |
| 「帶我寫論文」/「引導我寫論文」 | full | plan mode | 使用者需要互動式引導，不是直接產出 |
| 「第一次寫論文」/「論文新手」 | full | plan mode | 新手需要蘇格拉底式逐章引導 |

---

## Quick Decision Table

| What Do You Have? | What Do You Want? | Choose This Mode |
|-----------|-----------|------------|
| Nothing | Complete paper | plan mode → full mode |
| Research question + literature | Complete paper | full mode |
| Research question + literature | Outline | outline-only mode |
| Vague idea | Paper plan | plan mode |
| deep-research results | Complete paper | full mode (auto-handoff) |
| deep-research results | Guided planning | plan mode |
| Completed paper | Revision | revision mode |
| Completed paper | Abstract | abstract-only mode |
| Completed paper | Format conversion | format-convert mode |
| Completed paper | Citation check | citation-check mode |

---

### Plan to Full Mode Conversion Protocol

When a user completes `plan` mode and wants to proceed to `full` mode for actual paper writing:

#### Conversion Checklist

| Plan Mode Output | Full Mode Input | Conversion Action |
|-----------------|-----------------|-------------------|
| Chapter Plan (structure outline) | `structure_architect` agent | Map chapters → formal sections with heading levels; validate against `paper_structure_patterns.md` |
| Socratic Responses (Q&A transcripts) | `argument_builder` agent | Extract claims + evidence + warrants from dialogue; discard conversational scaffolding |
| Literature Notes (if any) | `literature_strategist` agent | Independent execution — plan mode notes serve as seed keywords only; full systematic search required |
| Argument Sketches | `argument_builder` agent | Evaluate each sketch against 4-level scoring; only `adequate` or above proceed |

#### Quality Gate

Before conversion, ALL of the following must be true:
- [ ] Every chapter in the Chapter Plan has at least 1 argument sketch rated `adequate` or above
- [ ] The overall paper structure maps to a recognized pattern in `paper_structure_patterns.md`
- [ ] At least 5 potential references have been identified (seeds for `literature_strategist`)
- [ ] The research question is finalized (not still evolving from Socratic dialogue)

#### What Gets Discarded
- Conversational filler from Socratic dialogue (greetings, confirmations, repetitions)
- Tentative ideas explicitly marked as "maybe" or "not sure" by the user
- Plan mode's iterative drafts (only the final version of each chapter plan carries over)

---

## Trigger-to-Mode Mapping Examples

```
"Write a paper on SDGs in HEI"           -> full
"Give me a paper outline for..."         -> outline-only
"Revise this paper based on feedback"    -> revision
"Write an abstract for this paper"       -> abstract-only
"Do a literature review on..."           -> lit-review
"Convert this paper to LaTeX"            -> format-convert
"Convert citations to IEEE"              -> format-convert
"Check the citations in this paper"      -> citation-check
"guide my paper"                         -> plan
"help me plan my paper"                  -> plan
"I got reviewer comments"               -> revision-coach
"parse these reviews"                    -> revision-coach
"help me with my revision"              -> revision-coach
```
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-references-plan-mode-protocol-md"></a>

## SOURCE: skills/academic-paper/references/plan_mode_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=4839 -->
# Plan Mode: Chapter-by-Chapter Guided Planning

Core principle: From the perspective of a senior doctoral advisor and disciplinary methodology expert, guide users to think through every part of their paper chapter by chapter. Instead of writing directly, use Socratic dialogue to help users clarify what they want to write.

```
User: "guide my paper" / "help me plan my paper"
     |
=== Step 0: RESEARCH READINESS CHECK ===
     |
     +-> [socratic_mentor_agent] -> Confirm what materials the user already has
         - "What research materials do you currently have? (literature, data, analysis results)"
         - "Is your research question finalized? Can you state it in one sentence?"
         -> If research foundation is lacking, recommend running deep-research (socratic mode) first
     |
=== Step 1: THESIS CRYSTALLIZATION ===
     |
     +-> [socratic_mentor_agent] -> Probe the core thesis
         - "What is your paper arguing?"
         - "How would someone who disagrees with you respond?"
         - "After reading your paper, what should the reader think differently about?"
         Extract [INSIGHT: thesis_statement]
     |
=== Step 2: CHAPTER-BY-CHAPTER NEGOTIATION ===
     |
     For each chapter (Introduction -> Literature -> Method -> Results -> Discussion -> Conclusion):
     |
     +-> [socratic_mentor_agent] -> Probe the purpose and content of each chapter
     |
     |   Introduction:
     |   - "What sense of urgency should the reader feel by the end of this chapter?"
     |   - "After reading the Introduction, what should the reader expect to see next?"
     |   - "What is your research gap? State it in one sentence."
     |
     |   Literature Review:
     |   - "How many stories are you telling? What is the relationship between them?"
     |   - "What conclusion should your literature review ultimately lead to?"
     |   - "Is there an important work you disagree with? Why?"
     |
     |   Methodology:
     |   - "If someone challenges your method, how would you respond?"
     |   - "Is there a simpler method that could also answer your question? Why didn't you choose it?"
     |   - "What is the biggest limitation of your method? How do you handle it?"
     |
     |   Results:
     |   - "What is your most important finding? State it in one sentence."
     |   - "Were there any unexpected results? How do you explain them?"
     |   - "Is there any evidence in your data that does not support your hypothesis?"
     |
     |   Discussion:
     |   - "How do your results dialogue with existing literature?"
     |   - "What is the one thing you most want the reader to remember?"
     |   - "What recommendations does your research have for practice/policy?"
     |
     |   Conclusion:
     |   - "If you could only leave one paragraph, what would you say?"
     |   - "What future research directions does your study open up?"
     |
     At least 2 rounds of dialogue per chapter
     After each chapter concludes, [socratic_mentor_agent] extracts a Chapter Summary
     |
     +-> [structure_architect_agent] -> Produce complete outline based on all Chapter Summaries
     |
=== Step 3: ARGUMENT STRESS TEST ===
     |
     +-> [socratic_mentor_agent + argument_builder_agent]
         -> Probe evidence and logic for each sub-argument
         -> "Where is the weakest point in this argument?"
         -> "If you reverse your argument, does it still hold?"
         -> Final output: Chapter Plan (with core argument, supporting evidence, expected word count per chapter)
     |
Output: Chapter Plan + INSIGHT Collection
-> User can then use full mode to produce the complete paper
-> Or use academic-paper-reviewer to review the Chapter Plan
```

## Plan Mode Activation Rules

Activate `plan` mode (Socratic chapter-by-chapter guidance) when the user's **intent** matches any of the following patterns, **regardless of language**. Detect meaning, not exact keywords.

**Intent signals** (any one is sufficient):
1. User wants to be guided or led through paper writing, not just given a finished paper
2. User asks for step-by-step or chapter-by-chapter planning
3. User expresses uncertainty about how to start or structure a paper
4. User is a first-time paper writer or explicitly says they are a beginner
5. User has research results but doesn't know how to turn them into a paper
6. User wants to think through each section before writing

**Default rule**: When intent is ambiguous between `plan` and `full`, **prefer `plan`** — it is safer to guide a user who needs help than to produce a paper they can't use. The user can always switch to `full` later.

**Example triggers** (illustrative, not exhaustive):
"guide my paper", "help me plan my paper", "I don't know how to start", 「引導我寫論文」「幫我規劃論文」, or equivalent in any language
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-references-policy-anchor-disclosure-protocol-md"></a>

## SOURCE: skills/academic-paper/references/policy_anchor_disclosure_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=20797 -->
# Policy-Anchor Disclosure Protocol

**Status**: #108 implementation (parented to Decision Doc 20ed72d)
**Parent skill**: `academic-paper`
**Mode name**: `disclosure` with `--policy-anchor=<a>` selector (parallel track to `--venue=<v>` v3.2 path; see `disclosure_mode_protocol.md` for the dispatch).
**Anchor inventory**: `prisma-trAIce, icmje, nature, ieee` (closed enum; expansion via §4.7 deferred per Decision Doc §4.2).
**Data source**: `policy_anchor_table.md` (read at runtime; LLM looks up the row for `--policy-anchor=<a>` × field-N).

This protocol document is the runtime instruction set the LLM follows when the user invokes `disclosure` mode with a policy-anchor selector. It encodes the 8 Decision Doc §4.3 frozen invariants, the §3 G10 7-row precedence table for whole-disclosure output decision, the 11 §4.4 open-concern resolutions (per implementation spec §3), the auto-promotion forbiddance, and the per-anchor render flows (PRISMA-trAIce / ICMJE / Nature / IEEE).

---

## 0. Why this protocol exists

ARS's v3.2 `disclosure` mode renders venue-targeted AI disclosure text (ICLR, NeurIPS, Nature, Science, ACL, EMNLP). The 4-anchor `--policy-anchor=<a>` track parallels v3.2's venue track when the author targets a **policy anchor** (PRISMA-trAIce, ICMJE, Nature Portfolio, IEEE) rather than a specific journal venue. The two tracks coexist; v3.2 venue path remains the default for journal submissions.

---

## 1. Inputs

1. **Paper draft** (same as v3.2): manuscript text plus pipeline log if available.
2. **Selector**: `--policy-anchor=<a>` where `a ∈ {prisma-trAIce, icmje, nature, ieee}`. **Selector-mutually-exclusive by default** — supplying both `--policy-anchor` and `--venue` triggers the §5 conflict-resolution flow, which permits exactly one consistent pair (any Nature Portfolio venue + `--policy-anchor=nature`, sharing the canonical `shared/policy_data/nature_policy.md` source) and rejects every other combination with explicit error. See §5 for the full enumeration.
3. **Pipeline signal**: `slr_lineage=true|false` set by the upstream pipeline orchestrator when an SLR-mode stage appears in the run history. Drives the §4.3 G2 invariant track gate (concern #1 resolution: explicit `slr_lineage` input).
4. **Cold-start fallback**: when the renderer runs outside a pipeline (no `slr_lineage` set), the author supplies `mode=<value>` explicitly. Silent fallback to general track on missing input is **forbidden** by §4.3 G2 invariant.
5. **v3.2 Phase 2 AI usage categorization**: the same input shape v3.2 uses. Each AI usage category carries state ∈ `{USED, NOT USED, UNCERTAIN}`.
6. **Optional `ai_used: true | false`**: explicit author-supplied flag layered on top of category state. Composes with category state per §2 G10 7-row precedence table below.
7. **Tool identity per AI tool** (concern #2 resolution): auto-detected from session metadata (mirror v3.2 `disclosure_mode_protocol.md` Phase 4 detection); explicit fallback per tool when session metadata absent or non-Claude tools are involved.

---

## 2. Whole-disclosure decision — §3 G10 7-row precedence table

Rows are evaluated in priority order from top to bottom; the renderer emits the output of the **first** row whose precondition matches. Subsequent rows do not fire. This table is the §4.3 **G3 / G10 invariant** in load-bearing form.

| # | Precondition (first match wins) | Whole-disclosure output |
|---|---|---|
| 1 | `ai_used: false` supplied AND ≥1 v3.2 category is USED (contradiction) | Honest "AI-disclosure conflict — explicit no-AI input contradicts USED category" annotation; renderer prompts the user to reconcile before any anchor render emits. |
| 2 | `ai_used: false` supplied AND no v3.2 category is USED AND no v3.2 category is UNCERTAIN | "No AI was used in preparing this paper" statement (G10 opt-in path). |
| 3 | `ai_used: false` supplied AND ≥1 v3.2 category is UNCERTAIN AND no v3.2 category is USED | Honest "AI-disclosure tension — explicit no-AI input but categories still UNCERTAIN" annotation; renderer prompts the user to resolve UNCERTAIN before emitting the no-AI statement. |
| 4 | `ai_used: true` supplied OR ≥1 v3.2 category is USED, AND row 1 did not match | Full anchor-specific disclosure render per §3 below, applying the **concern #6 resolution** (USED facets at full strength; per-facet "AI disclosure pending — category {X} not confirmed; resolve via v3.2 Phase 2" annotation immediately after each still-UNCERTAIN facet's render slot). |
| 5 | ≥1 v3.2 category is UNCERTAIN AND no v3.2 category is USED AND no `ai_used` input | Honest "AI-disclosure status not supplied — categories pending confirmation" annotation; renderer prompts the user to run the v3.2 UNCERTAIN-confirmation flow before re-invoking. |
| 6 | ≥1 v3.2 category supplied AND every supplied category is NOT USED AND no UNCERTAIN AND no `ai_used` input | Silence — emit no AI-disclosure statement at all (G10 "silence is default-OK"). |
| 7 | None of rows 1–6 match (empty input across every dimension) | Honest "AI-disclosure status not supplied for this run" annotation (G3 D3 pure cold-start). |

**Concern #10 resolution (`ai_used: true` substantive-content gate):** when `ai_used: true` is supplied **and no v3.2 category is marked USED** (regardless of whether Phase 2 has been performed — i.e., this gate fires for both "bare-flag input only, no categorization" **and** "Phase 2 done but every category came back NOT USED while `ai_used:true` is still set"), row 4 does not emit a complete render. Instead, the input is treated as a **prompt-trigger** that halts the current run and asks the user to reconcile: either supply a USED category, change `ai_used` to false, or run / re-run v3.2 Phase 2 categorization. Once a USED category is supplied (or `ai_used` flipped), re-evaluate against the §2 table from the top. This implements the concern #10 resolved path: "force v3.2 categorization flow", consistent with concern #6's honest-signal-preservation discipline. The forbiddance: emitting a full anchor disclosure with `ai_used:true` and zero USED facets.

---

## 3. Per-anchor render flows

For each anchor, the renderer reads `policy_anchor_table.md` rows 1..16 and applies the field-level rules below. The 4 anchors share the row-4 dispatcher above; the per-anchor sections only describe **what to emit** after row 4 fires.

### 3.1 `--policy-anchor=prisma-trAIce`

**Track gate (G2 invariant):** this anchor is only valid when `slr_lineage=true` (pipeline signal) or `mode=systematic-review` (cold-start input). Selecting `--policy-anchor=prisma-trAIce` with `slr_lineage=false` is non-conformant — the renderer refuses with an explicit error citing the G2 invariant.

**G5 invariant — three gates for M6 prompt disclosure:** PRISMA-trAIce M6 prompt disclosure fires only when **all three** hold:
1. PRISMA-trAIce track selected (the gate above).
2. `tool_type ∈ {LLM, GenAI}` (per PRISMA M6 "if any" predicate).
3. AI use is methodological-in-SLR (search / screening / data extraction / Risk of Bias / synthesis / drafting per PRISMA M3.a), **not pure copyediting**.

When gate 3 fails (SLR manuscript whose only LLM use is editorial), the renderer routes to the §3.5 copyediting-carve-out path instead. PRISMA-trAIce track does not own the copyediting case.

**Render fields:**
- Per `policy_anchor_table.md` row 1–3: emit one **tool identity tuple** per AI tool (concern #2 resolution; auto-detect from session, fallback explicit). Identity tuple = (tool name, version if applicable, developer/provider).
- Row 4–5: emit one **(tool × task) record** per (tool, task) tuple across the M3.a 6-stage enum (concern #3 resolution). Missing tuples produce "not supplied" annotation per tuple. Per-task prompt disclosure follows M6.a granularity.
- Row 8: emit prompt records per (tool × task) tuple per gate G5.
- Row 9: emit human oversight description per M8 sub-items.
- Rows 11–12: emit performance evaluation method + results per M9 + R2 when applicable.
- Row 13: emit limitations narrative per D1.
- Row 14: distribute disclosure fragments per Table 1 row groupings (Title / Abstract / Introduction / Methods / Results / Discussion). The renderer emits per-section fragments, not a single paragraph.

### 3.2 `--policy-anchor=icmje`

**Track gate:** no SLR lineage requirement. Available regardless of `slr_lineage` value.

**Render fields:**
- Row 10 (explicit-mandate): emit ICMJE human-responsibility statement using the verbatim "humans are responsible for any submitted material that included the use of AI-assisted technologies" language. This sentence appears in **every** ICMJE render where row 4 fires.
- Row 14 (explicit-recommend): emit two channels — cover letter (verbatim ICMJE language) + manuscript "appropriate section" (per the venue's submission policy). The two channels carry different paragraphs, not a single duplicated paragraph.
- Row 16 (explicit-mandate): emit the text-attribution clause: appropriate attribution and full citations for AI-quoted material + the prohibition against citing AI-generated material as primary source. Surface this paragraph even when no images are involved (rule covers text-attribution).
- Rows with `not-addressed` strength (9/16 cells): the renderer skips these by default; if v3.2 Phase 2 provides a category USED that would be served by such a field, surface a "ICMJE delegates this detail to journal-level policy; consider the v3.2 venue track for journal-specific phrasing" annotation.

### 3.3 `--policy-anchor=nature`

**Track gate:** no SLR lineage requirement.

**Dedup with v3.2 Nature venue path:** the Nature substantive policy text is co-cited from `shared/policy_data/nature_policy.md` (canonical source pointer). Both consumers — the v3.2 Nature venue renderer in `venue_disclosure_policies.md` and this Nature anchor renderer — derive their substantive content from that shared source. **G4 invariant**: edits to Nature-specific policy quotes must go through the shared source first, never directly into either consumer.

**Render fields:**
- Rows 9–10 (both explicit-mandate): emit the human-accountability statement using Nature's "In all cases, there must be human accountability for the final version of the text" verbatim language. Combine with the authorship-rejection clause from row 10's second quote when the manuscript proposes any AI co-authorship.
- Row 14 (explicit-recommend): emit Methods-section placement instruction citing the verbatim "Methods section (and if a Methods section is not available, in a suitable alternative part)" language.
- Row 15 (explicit-recommend) carve-out semantics: **eliminate** strength. Copyediting-only use produces **no disclosure paragraph**, only an internal renderer log entry. The §4.3 G7 invariant forbids collapsing this into a boolean shared with IEEE's downgrade semantics.
- Row 16 (explicit-mandate) image-rights handling: concern #5 resolution = **hybrid (annotation block + suggested inline patches)**. The renderer emits two outputs:
  1. A standalone `image_disclosure_instructions.md` block describing, per image, which Nature carve-out applies (or default-deny) and what Nature label text appears in the image field.
  2. A suggested patch diff against manuscript source figure metadata (caption, alt-text, image-field caption) for the author to optionally apply. **ARS does not modify manuscript source autonomously**; the patch is suggested-only.

### 3.4 `--policy-anchor=ieee`

**Track gate:** no SLR lineage requirement.

**G8 invariant — paired mandate:** IEEE row 5 (`Specific task within stage`, explicit-mandate) and row 6 (`Affected manuscript sections / content locator`, explicit-mandate) are a paired mandate. The renderer emits **both** inputs together. Emitting `level_of_involvement` (row 5 narrative annotation) without an `affected_sections` locator (row 6) — or vice versa — is **non-conformant**.

**Concern #4 resolution (IEEE section locator shape):** free-form list with recommended IMRaD exemplars. Accepted values: `"Introduction" | "Methods" | "Results" | "Discussion" | "Abstract" | "Title" | free-form-other`. Closed-enum would over-constrain IEEE's "brief explanation" language; free-form preserves the policy's narrative invitation. Test fixture covers both exemplar-match and free-form-other inputs.

**Render fields:**
- Row 1 (explicit-mandate): emit "The AI system used shall be identified" formulation — name + identifier per AI tool.
- Rows 5–6 (paired explicit-mandate per G8): emit `affected_sections` list + `level_of_involvement` narrative annotation **together**.
- Row 14 (explicit-mandate): emit placement instruction citing "acknowledgments section of any article submitted to an IEEE publication" verbatim. **No Methods placement, no cover-letter channel** — the tightest closed enum across all four anchors.
- Row 15 (explicit-recommend) carve-out semantics: **downgrade-not-eliminate** strength. Copyediting-only use still produces a disclosure paragraph at the same acknowledgments location, but with recommend-strength rather than mandate language. The §4.3 G7 invariant forbids collapsing this into a boolean shared with Nature's eliminate semantics.
- Row 16 (implicit): images/figures/code fold into the same acknowledgments-disclosure mandate as text. **No separate image-rights regime, no default-prohibition** (contrasts with Nature). The renderer emits a single acknowledgments paragraph covering all content types per IEEE policy. The §4.3 G9 invariant: each anchor's image-rights regime stays distinct; IEEE's fold-into-acknowledgments path does not merge with Nature's default-deny regime.

### 3.5 Copyediting carve-out cross-anchor handling

Per §4.3 G7 invariant + §4.5 / §4.6 cell #15, the copyediting carve-out semantics are anchor-specific:

- **Nature anchor**: eliminate strength — no disclosure paragraph for copyediting-only use.
- **IEEE anchor**: downgrade-not-eliminate — disclosure still emitted at acknowledgments, with recommend-strength language ("is recommended" rather than "shall be disclosed").
- **PRISMA-trAIce anchor**: not in scope (M6 G5 gate 3 routes copyediting cases away from PRISMA-trAIce track entirely; see §3.1).
- **ICMJE anchor**: not-addressed in the policy text; the renderer treats copyediting cases per the same path as substantive AI use (no carve-out, full ICMJE render).

The renderer MUST NOT collapse these four behaviors into a single boolean `exempted_uses: [copyediting]` field — doing so would silently lose the eliminate-vs-downgrade-vs-not-in-scope distinctions.

---

## 4. Auto-promotion forbiddance (§4.3 G3 / G10 invariant)

A still-UNCERTAIN category MUST NOT be rendered as though USED in any of the four anchor outputs. This is the load-bearing constraint behind concern #6's resolution: USED facets render at full strength; UNCERTAIN facets surface the per-facet annotation, never the full-strength render. The renderer MUST surface UNCERTAIN as UNCERTAIN throughout the disclosure text; silent promotion of any UNCERTAIN category to USED is **forbidden**.

The test suite covers this forbiddance with negative fixtures asserting that an input with `ai_used:true` + 1 UNCERTAIN category + 0 USED categories does NOT emit a full-strength render of the UNCERTAIN category.

---

## 5. Venue + anchor conflict resolution (concern #7)

When the user passes both `--venue=<v>` and `--policy-anchor=<a>`, the renderer evaluates whether the two map to compatible policies. The consistent-pair recognition for the Nature track covers the full Nature Portfolio venue family:

- **Consistent — Nature Portfolio venue + `--policy-anchor=nature`**: includes canonical labels `{"Nature", "Nature Portfolio", "Nature (Nature Publishing Group)", "Nature Publishing Group"}` **and** any venue whose name starts with the prefix `"Nature "` (e.g., `Nature Medicine`, `Nature Communications`, `Nature Climate Change`, `Nature Energy`, `Nature Methods`, ...). All Nature Portfolio journals inherit the same parent AI policy, so each of these venue strings + `--policy-anchor=nature` proceeds via the shared source pointer.
- **Conflicting — any other (venue, anchor) pair**: e.g., `--venue=Nature` + `--policy-anchor=IEEE`, `--venue=ICLR` + `--policy-anchor=icmje`, or a Nature Portfolio venue with a non-nature anchor → **reject with explicit error** listing the policy conflict and the canonical Nature consistent-pair definition above.

Silent precedence is **forbidden** (Decision Doc §4.4 #7 + concern #7 resolution). The renderer must surface the conflict to the user and require an explicit selector choice. The recognition logic above is mirrored by the conformance referee's `is_nature_portfolio_venue()` helper in `scripts/policy_anchor_disclosure_referee.py` — when this protocol text drifts from that helper, the alignment is a non-conformance.

---

## 6. Three-state input completeness flag (concern #8)

The §2 G10 7-row table evaluates first-match across (`ai_used` × per-category-state). Field-level computation:

- `ai_used` ∈ `{true, false, unset}`.
- Each v3.2 category ∈ `{USED, NOT USED, UNCERTAIN, not-supplied}`.
- First-match-wins evaluation across §2's 7 rows.
- Row-4 partial-state composition per concern #6 resolution: USED at full strength; per-facet annotation for each still-UNCERTAIN; auto-promotion forbidden.

The §4.3 invariants constrain the evaluation:
- **G1 invariant** — no `ai_disclosure` field is read from / written to the corpus entry schema; all input flows through the renderer's runtime input contract.
- **G2 invariant** — track selection reads `slr_lineage` first, never derives SLR-status from `origin_mode` alone.
- **G3 / G10 invariant** — the 7-row table holds; auto-promotion forbidden.
- **G4 invariant** — 4 anchors, Nature dedup via shared source.
- **G5 invariant** — three gates for M6 prompts.
- **G7 invariant** — anchor-specific carve-out semantics.
- **G8 invariant** — IEEE paired-mandate (row 5 + row 6).
- **G9 invariant** — anchor-specific image-rights regimes.

---

## 7. §4.4 concern resolutions reference

For audit traceability, this protocol implements each Decision Doc §4.4 open concern as follows. See implementation spec §3 for full rationale.

- **concern #1** — Track-selection lookup mechanism resolved as: explicit `slr_lineage` input from pipeline orchestrator; cold-start `mode=` parameter.
- **concern #2** — Tool identity collection: auto-detect from session metadata (v3.2 Phase 4 pattern); explicit fallback per tool for cold-start or non-Claude pipelines.
- **concern #3** — Prompt scope: per-(tool × task) tuple across M3.a 6-stage enum; missing tuples emit "not supplied" annotation per tuple.
- **concern #4** — IEEE section locator: free-form list with recommended IMRaD exemplars; parallel to G8 `level_of_involvement` design.
- **concern #5** — Nature image metadata + labelling: hybrid output channel — standalone annotation block + suggested inline manuscript patches; ARS does not modify manuscript source autonomously.
- **concern #6** — UNCERTAIN per-facet finalization: USED facets render at full strength; UNCERTAIN facets surface per-facet annotation immediately after each render slot.
- **concern #7** — Venue + anchor conflict: reject with explicit error citing the policy conflict; silent precedence forbidden.
- **concern #8** — Three-state completeness flag: full spec encoded in §6 above.
- **concern #9** — Test set scope: covers §4.3 8 invariants + §4.4 #1–#8 + #10 + #11; positive + negative fixture per resolved path / forbidden path.
- **concern #10** — `ai_used: true` substantive-content gate: bare-flag input treated as prompt-trigger forcing v3.2 categorization flow before any anchor render.
- **concern #11** — G1 invariant scope: §2.1 G1 Decision authoritative (no `ai_disclosure` field added to corpus entry schema); non-renderer code changes for §4.4 #1 pipeline-plumbing **permitted** (pipeline orchestrator setting `slr_lineage` is not corpus-schema mutation).

---

## 8. Related

- Decision Doc: `../docs/design/2026-05-14-ai-disclosure-schema-decision.md`
- Implementation spec: `../docs/design/2026-05-14-ai-disclosure-impl-spec.md`
- Anchor data table (consumer of this protocol): `policy_anchor_table.md`
- v3.2 disclosure mode protocol (parallel track): `disclosure_mode_protocol.md`
- v3.2 venue disclosure policies (Nature dedup peer): `venue_disclosure_policies.md`
- Shared Nature policy source (canonical pointer, forthcoming): `shared/policy_data/nature_policy.md`
- Lint contract: `../../scripts/check_policy_anchor_protocol.py`
- Conformance test suite: `../../scripts/test_policy_anchor_disclosure.py` (Task #7)
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-references-vlm-figure-verification-md"></a>

## SOURCE: skills/academic-paper/references/vlm_figure_verification.md

<!-- SOURCE-CONTENT-BEGIN bytes=3312 -->
# VLM Figure Verification Protocol (Optional)

**Status**: v3.3
**Used by**: `visualization_agent`
**Requires**: Multimodal LLM with vision capability (e.g., Claude with vision, GPT-4V)

---

## Purpose

After the visualization_agent generates a figure, an optional verification loop uses a vision-capable LLM to check the rendered figure against the paper's data and APA 7.0 standards. This catches issues invisible in code review: truncated labels, overlapping text, incorrect data rendering, misleading scales.

Inspired by PaperOrchestra's Plotting Agent (Song et al., 2026), which uses a "VLM critic" in a closed-loop refinement system.

---

## When to use

- **Recommended**: When figures contain complex data (multi-panel, many categories, statistical plots)
- **Optional**: For simple figures (single bar chart, basic line plot)
- **Required**: When the pipeline is in `final-check` mode (Stage 4.5+)
- **Skip**: When no multimodal capability is available (graceful degradation)

---

## Verification Checklist

The VLM receives the rendered figure image and the source data, then checks:

### Data Accuracy
1. Do the plotted values visually match the source data? (e.g., a bar labeled "45%" should be approximately 45% of the axis range)
2. Are all data series present? (no missing categories or groups)
3. Do error bars / confidence intervals appear correct in scale?

### APA 7.0 Compliance
4. Are both axes labeled with descriptive text and units?
5. Is the legend present and readable (for multi-series)?
6. Is the figure title in the correct format (bold label + italic title)?
7. Are fonts readable at publication size (no text < 8pt)?

### Visual Quality
8. Is any text truncated, overlapping, or cut off at figure edges?
9. Are colors distinguishable (no two series with visually identical colors)?
10. Is the figure free of chart junk (3D effects, unnecessary gridlines)?

---

## Verification Loop

```
Step 1: visualization_agent generates figure code
Step 2: Execute code to render figure image
Step 3: Send figure image + source data + checklist to VLM
Step 4: VLM returns pass/fail for each checklist item
Step 5: If any FAIL:
  - VLM describes the specific issue
  - visualization_agent modifies code to fix
  - Return to Step 2 (max 2 iterations)
Step 6: If all PASS or max iterations reached:
  - Attach verification result to Figure Package
  - Any remaining issues noted in figure caption Note
```

**Max iterations**: 2 refinement cycles (3 total renders). If issues persist after 2 fixes, flag for user review rather than continuing the loop.

---

## Output Addition to Figure Package

When VLM verification is run, the Figure Package (from visualization_agent) includes:

```markdown
### VLM Verification
- **Status**: PASS / PASS_WITH_NOTES / NEEDS_REVIEW / SKIPPED
- **Iterations**: [N] (1 = passed first time, N/A if SKIPPED)
- **Issues found**: [list of issues, if any]
- **Issues fixed**: [list of fixes applied]
- **Remaining issues**: [issues that could not be auto-fixed, if any]
```

---

## References

- Song, Y. et al. (2026). PaperOrchestra. *arXiv:2604.05018*. — Section 4 Step 2 (Plotting Agent with VLM critic).
- Zhu, D. et al. (2026). PaperBanana: Automating academic illustration for AI scientists. *arXiv:2601.23265*. — Closed-loop VLM refinement system.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-references-workflow-phase-details-md"></a>

## SOURCE: skills/academic-paper/references/workflow_phase_details.md

<!-- SOURCE-CONTENT-BEGIN bytes=3378 -->
# Orchestration Workflow — Phase Details

Detailed per-phase agent behavior and output descriptions for the 8-phase orchestration workflow.

---

## Phase 0: CONFIG (Interactive)

**Agent**: `intake_agent`
**Output**: Paper Configuration Record

- Paper type (IMRaD / Lit Review / Theoretical / Case Study / Policy Brief / Conference)
- Discipline and sub-field
- Target journal (optional)
- Citation format (APA 7 / Chicago / MLA / IEEE / Vancouver)
- Output format (LaTeX / DOCX / PDF / Markdown / Combined)
- Language (EN / zh-TW / bilingual sections)
- Bilingual abstract (Yes / EN-only / zh-TW-only)
- Word count target
- Existing materials (RQ, data, drafts, lit)

**Checkpoint**: User confirms configuration.

---

## Phase 1: RESEARCH

**Agent**: `literature_strategist_agent`
**Output**: Search Strategy + Source Corpus

- Database selection + search strings
- Inclusion/exclusion criteria
- Source screening + annotated bibliography
- Literature matrix (Source x Theme)
- Research gap mapping

**Checkpoint**: User reviews sources (optional add/remove).

---

## Phase 2: ARCHITECTURE

**Agent**: `structure_architect_agent`
**Output**: Paper Outline + Evidence Map

- Structure pattern selection (from paper_structure_patterns.md)
- Section-by-section outline with word count allocation
- Evidence-to-section assignment
- Transition logic between sections

**Checkpoint**: User approves outline.

---

## Phase 3: ARGUMENTATION

**Agent**: `argument_builder_agent`
**Output**: Argument Blueprint

- Central thesis + sub-arguments
- Claim-Evidence-Reasoning chains per section
- Counter-argument identification + rebuttal strategy
- Logical flow diagram

---

## Phase 4: DRAFTING

**Agent**: `draft_writer_agent`
**Output**: Complete Draft

- Section-by-section writing following outline
- Register adjustment for discipline
- In-text citations integrated
- Word count tracking per section
- Transition paragraphs between sections

---

## Phase 5a & 5b: CITATIONS + ABSTRACT (Parallel)

### Phase 5a: Citations

**Agent**: `citation_compliance_agent`
**Output**: Citation Audit Report

- In-text <-> reference list cross-check (zero orphans)
- Format compliance (per selected style)
- DOI/URL verification
- Self-citation ratio check
- Auto-correction of detected errors

### Phase 5b: Abstract

**Agent**: `abstract_bilingual_agent`
**Output**: Bilingual Abstract + Keywords

- English abstract (150-300 words, structured)
- Traditional Chinese abstract (300-500 characters, structured)
- EN keywords (5-7)
- zh-TW keywords (5-7)
- Independent writing (not mechanical translation)

---

## Phase 6: PEER REVIEW

**Agent**: `peer_reviewer_agent`
**Output**: Review Report + Revision Instructions

- 5-dimension scoring:
  Originality (20%) | Methodological Rigor (25%) | Evidence Sufficiency (25%)
  Argument Coherence (15%) | Writing Quality (15%)
- Verdict: Accept / Minor Revision / Major Revision / Reject
- Line-level feedback with suggested fixes
- Max 2 revision loops -> back to Phase 4 [draft_writer_agent] (limited to 1 round in academic-pipeline)

---

## Phase 7: FORMAT

**Agent**: `formatter_agent`
**Output**: Final Output Package

- Target format conversion (LaTeX + .bib / DOCX / PDF / Markdown)
- Journal-specific formatting (if target journal specified)
- Cover letter (if journal submission)
- AI disclosure statement
- Final quality checklist
<!-- SOURCE-CONTENT-END -->
