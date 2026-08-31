<a id="source-skills-academic-paper-reviewer-references-calibration-mode-protocol-md"></a>

## SOURCE: skills/academic-paper-reviewer/references/calibration_mode_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=10542 -->
# Calibration Mode Protocol

**Status**: v3.2
**Parent skill**: `academic-paper-reviewer`
**Mode name**: `calibration`
**Purpose**: Measure this reviewer's own false-negative rate (FNR), false-positive rate (FPR), and balanced accuracy against a user-supplied gold-standard set, then attach the resulting error profile as a confidence disclosure to subsequent reviews in the same session.

---

## Why this mode exists

A single LLM reviewer produces an absolute 0-100 rubric score, but that score is weakly interpretable without knowing the reviewer's error profile. Two reviewers could give the same paper a 65, yet one might systematically over-score weak methodology papers and the other might systematically under-score cross-disciplinary work. Absolute scores don't reveal this.

Lu et al. (2026, Nature 651:914-919) demonstrated in Table 1 that an LLM-based Automated Reviewer can approach human balanced accuracy (0.65 vs human 0.67-0.73 on 500 ICLR 2022 papers) while having a dramatically different error profile: FNR 0.17 vs human 0.52, at the cost of FPR 0.50 vs human 0.17-0.34. Human reviewers miss half of the papers that should be rejected; the Automated Reviewer misses very few but over-rejects more.

Translation for ARS: **our reviewer has an error profile too, and we do not currently measure it.** Calibration mode closes that gap. It does not try to make the reviewer perfect; it makes the reviewer's imperfections legible.

---

## Inputs

1. **Gold-standard set**: 5-20 papers the user has labelled with known outcomes. Minimum 5; recommended 10-15. Each entry:
   - Paper file path or text
   - Ground-truth label: `accept`, `reject`, or `borderline`
   - Venue context (journal/conference, tier)
   - Optional: human reviewer scores for comparison

2. **Domain specification**: the user's target field, used to seed `field_analyst_agent`. Calibration for "machine learning venues" is not valid for "qualitative education research" — error profiles are domain-specific.

3. **Session persistence**: the error profile is cached for the **current session only**. No cross-session caching, no `~/.ars_calibration_cache/` directory. Calibration is explicitly opt-in per the v3.2 design decision: the user decides when to spend tokens on calibration, and a new session starts fresh. If the user wants to reuse a profile across sessions, they re-run calibration or paste a prior Calibration Report as a session prompt.

---

## Process

### Phase 0: Intake

- Verify the set has at least one `accept` and one `reject` (otherwise FNR or FPR is undefined).
- If all labels are on one side, refuse to proceed and ask the user for at least one counter-example.
- Warn if n < 10: "Calibration with fewer than 10 papers produces wide confidence intervals. Results should be treated as directional, not conclusive."

### Phase 1: Run `full` mode on each gold paper, with ensembling

For each paper, run the standard `full` review pipeline **5 times** (ensembling, per Lu 2026 Methods A.1.1). Each run uses a fresh context window to avoid within-session bias. Aggregate:
- Median rubric score per dimension
- Variance across the 5 runs (reported as a stability indicator)
- Editorial decision (majority vote across 5)

**Cross-model verification**: In calibration mode, `ARS_CROSS_MODEL` is **default-on** rather than opt-in. At least one of the 5 runs should use a different model family if available, to avoid single-model blind spots. If no cross-model is configured, emit a warning and run all 5 on the primary model.

### Phase 2: Build the confusion matrix

Compare reviewer's majority-vote decision against the user's ground-truth label.

- `borderline` ground truth papers are excluded from the binary confusion matrix but reported separately (see Phase 3).
- Map `Accept` and `Minor Revision` reviewer decisions → positive. Map `Major Revision` and `Reject` → negative. This follows Lu 2026 Table 1's binarization.

Compute:

| Metric | Formula | Report with |
|---|---|---|
| Balanced accuracy | (TPR + TNR) / 2 | 95% CI via bootstrap (1000 resamples) |
| FNR (miss rate) | FN / (FN + TP) | Same |
| FPR (false alarm) | FP / (FP + TN) | Same |
| AUC | ROC over rubric-score threshold | Same |
| Calibration error | Mean &#124;rubric_score - ground_truth_severity&#124; | Per-dimension |

### Phase 3: Borderline handling

Borderline papers don't enter the binary matrix but are useful for rubric-score calibration. For each borderline paper, report:
- The reviewer's rubric score
- The reviewer's decision
- Whether the reviewer's decision respects the user's "this is borderline" signal (i.e., did it correctly land in Major Revision rather than confidently Accept or Reject?)

A reviewer that confidently Accepts or Rejects borderline papers has a "confidence miscalibration" problem even if its binary accuracy looks fine.

### Phase 4: Produce the Calibration Report

Output document structured as:

```
# Calibration Report for <Reviewer Instance>
Domain: <domain>
Gold set: n=<N> (accept=<a>, reject=<r>, borderline=<b>)
Runs per paper: 5 (ensembled)
Cross-model: <yes/no, model families used>

## Summary metrics
- Balanced accuracy: 0.XX [95% CI: 0.XX - 0.XX]
- FNR: 0.XX [95% CI ...]
- FPR: 0.XX [95% CI ...]
- AUC: 0.XX
- Ensemble stability: <mean std of rubric scores across runs>

## Comparison to Lu 2026 Table 1 baselines
| Metric | This reviewer | Lu 2026 Automated Reviewer | Lu 2026 Human |
|---|---|---|---|
| Balanced accuracy | X | 0.65 | 0.67-0.73 |
| FNR | X | 0.17 | 0.52 |
| FPR | X | 0.50 | 0.17-0.34 |

(Note: Lu 2026 numbers are for ML venues specifically. Compare with caution outside ML.)

## Per-dimension calibration error
<table of 7 review dimensions with mean absolute calibration error>

## Systematic biases detected
<natural-language narrative identifying patterns, e.g.
 "Reviewer tends to over-score originality on cross-disciplinary papers"
 "Reviewer under-scores qualitative methodology by ~8 points vs ground truth"
>

## Recommendations for session use
- Treat this reviewer's rubric scores as having calibration error ±X points
- For accept/reject decisions, the reviewer misses X% of reject cases (FNR)
- For decisions near the accept/reject boundary, escalate to human judgement
```

### Phase 5: Session attachment

If session persistence is enabled, the Calibration Report is attached to every subsequent review in the same session as a **confidence disclosure header**. The disclosure appears in the editorial letter before the verdict:

```
> **Reviewer Confidence Disclosure (from calibration session <id>):**
> This reviewer has measured balanced accuracy 0.XX, FNR 0.XX, FPR 0.XX on a
> gold set of <N> papers in <domain>. Rubric scores below have calibration
> error ±X points. Treat borderline decisions with human judgement.
```

This is non-negotiable in calibration-enabled sessions: the user cannot hide the disclosure. The point of calibration is to make error profiles legible; suppressing the disclosure defeats the mode.

---

## Ensembling methodology notes

Lu 2026 Methods A.1.1 describes reviewer ensembling across 5 independent runs with majority voting. This mode follows that spec with two changes:

1. **Median instead of mean for rubric scores**: mean is vulnerable to single-run outliers (e.g., a run that hallucinates a methodological flaw); median is robust.
2. **Fresh context per run**: Lu 2026 allowed within-session memory across runs. ARS uses fresh context to prevent cascading errors from a single run's misreading.

Users with token budget concerns can reduce `runs_per_paper` to 3. Below 3, ensembling is meaningless — do not allow 1 or 2.

---

## Failure cases this mode does NOT fix

Calibration reports this reviewer's error profile on a **specific** gold set in a **specific** domain. It does not:

- Predict performance on papers outside that domain
- Detect frame-lock within a single paper review (that's `devils_advocate_reviewer` territory)
- Catch implementation-bug-as-finding cases (that's the AI Research Failure Mode Checklist, ROADMAP_v3.2.md item 2)
- Replace the `re-review` mode for revision verification

If the user's gold set is itself biased (e.g., all papers from one lab, all from one year), calibration reports a biased profile. Emit a warning during intake if papers share obvious metadata clusters.

---

## Integration with existing modes

| Existing mode | Interaction with calibration |
|---|---|
| `full` | Calibration runs `full` 5x per gold paper. No change to `full` itself. |
| `re-review` | Calibration profile attaches to re-review decisions. |
| `quick` | Calibration profile attaches. Confidence disclosure notes that `quick` has additional uncalibrated error on top of the measured profile. |
| `methodology-focus` | Calibration should ideally be run with methodology-heavy gold papers if this mode is the user's target. |
| `guided` | Not applicable — guided mode is Socratic dialogue, rubric scores are not the primary output. |

---

## Resolved design decisions (2026-04-09)

- **Activation**: opt-in only. User invokes `calibration` mode explicitly. ARS does not auto-calibrate on first use in a new domain.
- **Persistence**: session-scoped only. No cross-session caching of profiles, no `~/.ars_calibration_cache/`, no privacy questions about storing paper content on disk.
- **Shipped gold sets**: not planned for v3.2. Users bring their own gold set. Shipping a built-in ML gold set was considered and rejected to avoid domain-coverage bias and staleness.
- **Continuous/self-calibration**: rejected. Using the reviewer's own historical decisions as pseudo-ground-truth is circular and would make the error profile look better over time without actually improving accuracy.

---

## References

- Lu, C. et al. (2026). Towards end-to-end automation of AI research. *Nature* 651, 914-919. doi:10.1038/s41586-026-10265-5 — Table 1 (reviewer validation), Methods A.1.1 (ensembling).
- Efron, B. & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall/CRC — bootstrap CI methodology.
- ARS `shared/cross_model_verification.md` — cross-model reviewer integration.
- ARS `academic-paper-reviewer/references/quality_rubrics.md` — scoring rubric definitions.

## v3.6.2 sprint contract status

v3.6.2 introduces sprint contracts for `reviewer_full` and `reviewer_methodology_focus` only. A template for this mode will follow in a subsequent patch release. Until then, this mode runs without contract enforcement and retains its pre-v3.6.2 behaviour.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-reviewer-references-changelog-md"></a>

## SOURCE: skills/academic-paper-reviewer/references/changelog.md

<!-- SOURCE-CONTENT-BEGIN bytes=976 -->
# Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.4 | 2026-03-08 | Quality rubrics reference (0-100 scoring with 5 descriptors per dimension, weighted aggregation formula, decision mapping); Quick Mode Selection Guide; Dimension Scores upgraded from optional 1-5 to required 0-100 with rubric descriptors |
| 1.3 | 2026-03-05 | DA vs R3 role boundaries with explicit responsibility tables; CRITICAL finding criteria with concrete examples; Consensus classification (CONSENSUS-4/3/SPLIT/DA-CRITICAL); Confidence Score weighting rules; Asian & Regional Journals reference (TSSCI + Asia-Pacific + OA options) |
| 1.2 | 2026-03 | Added statistical reporting standards reference; enhanced methodology_reviewer_agent with statistical reporting adequacy sub-step |
| 1.1 | 2026-02 | Added Devil's Advocate Reviewer (7th agent), added re-review mode, expanded review team from 4 to 5 |
| 1.0 | 2026-02 | Initial version: 6 agents, 4 modes, 3-phase workflow |
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-reviewer-references-editorial-decision-standards-md"></a>

## SOURCE: skills/academic-paper-reviewer/references/editorial_decision_standards.md

<!-- SOURCE-CONTENT-BEGIN bytes=9230 -->
# Editorial Decision Standards — Criteria for Editorial Decision Making

This document defines the explicit criteria for Accept / Minor Revision / Major Revision / Reject decisions, for use by `eic_agent` and `editorial_synthesizer_agent`.

---

## 1. Decision Categories

### Accept

**Definition**: The paper can be published without further review.

**Criteria**:
- Average score across all universal dimensions >= 4.0
- No dimension scores below 3.0
- At least 3/4 reviewers recommend Accept or Minor Revision
- No unresolved major academic issues

**Conditions**:
- May include minor copyediting suggestions
- May require final formatting adjustments
- Does not need to be sent for review again

**Typical scenarios**:
- Paper has undergone multiple revision rounds, all issues resolved
- Rare first-pass acceptance (< 5% of submissions at top-tier journals)

---

### Minor Revision

**Definition**: The paper is fundamentally acceptable and can be published after limited modifications; typically does not need to be sent for review again after revision.

**Criteria**:
- Average score across all universal dimensions >= 3.5
- No dimension scores below 2.5
- At least 3/4 reviewers recommend Accept or Minor Revision
- Issues can be resolved within 2-4 weeks
- Modifications do not involve restructuring core arguments or methods

**Typical revision items**:
- Supplementing a small number of references
- Clarifying certain methodology description details
- Improving clarity of argumentation
- Correcting citation format
- Adding discussion of limitations
- Adjusting conclusion wording (avoiding overclaiming)

**Response requirements**:
- Authors must respond to reviewer comments item by item
- After revision, reviewed by EIC (usually not sent for external review again)
- Revision deadline: 2-4 weeks

---

### Major Revision

**Definition**: The paper has potential but has significant issues, requiring substantial revision followed by re-review.

**Criteria**:
- Universal dimension average score between 2.5-3.4
- Some dimensions may score below 2.5 (but not fatal)
- At least 2/4 reviewers recommend Major Revision or better
- Issues are serious but fixable (not fundamental design flaws)
- Revision requires 6-8 weeks of work

**Typical revision items**:
- Re-analyzing data (additional analysis or correcting errors)
- Substantially rewriting literature review (missing key references)
- Supplementing additional data collection
- Reorganizing paper structure
- Correcting significant methodological flaws
- Strengthening theoretical framework application
- Adding robustness checks

**Response requirements**:
- Authors must write a detailed point-by-point response letter
- After revision, sent for re-review (may go back to original reviewers or new reviewers)
- Revision deadline: 6-8 weeks
- Typically a maximum of 2 rounds of Major Revision allowed

---

### Reject

**Definition**: The paper is not suitable for publication in this journal, even with revision.

**Criteria (meeting any one may trigger Reject consideration)**:
- Universal dimension average score < 2.5
- Any core dimension (methodology, evidence) = 1
- At least 3/4 reviewers recommend Reject
- Fundamental unfixable issues exist

**Reject subtypes**:

| Subtype | Description | Suggestion |
|---------|-------------|-----------|
| **Reject — Out of Scope** | Topic not within journal scope | Recommend more suitable journals |
| **Reject — Fundamental Flaw** | Fatal flaw in research design | Suggest redesigning the research |
| **Reject — Insufficient Contribution** | Lacks originality or incremental contribution | Suggest how to strengthen contribution |
| **Reject — Premature** | Paper not yet mature enough | Suggest specific improvement directions |
| **Reject — Resubmit Encouraged** | Has potential but needs fundamental restructuring | Provide detailed restructuring suggestions |

**Even with Reject, must**:
- Affirm the paper's merits
- Provide specific improvement suggestions
- Recommend more suitable journals (if it's a scope issue)
- Maintain professional, respectful tone

---

## 2. Decision Matrix

### Decision Matrix Based on Reviewer Recommendations

| EIC | R1 | R2 | R3 | -> Recommended Decision |
|-----|----|----|-----|----------------------|
| Accept | Accept | Accept | Accept | **Accept** |
| Accept | Accept | Accept | Minor | **Accept** (with suggestions) |
| Accept | Accept | Minor | Minor | **Minor Revision** |
| Accept | Minor | Minor | Minor | **Minor Revision** |
| Minor | Minor | Minor | Minor | **Minor Revision** |
| Minor | Minor | Minor | Major | **Minor-to-Major** (depends on specific issues) |
| Minor | Minor | Major | Major | **Major Revision** |
| Minor | Major | Major | Major | **Major Revision** |
| Major | Major | Major | Major | **Major Revision** |
| Major | Major | Major | Reject | **Major Revision** (last chance) |
| Major | Major | Reject | Reject | **Reject** (resubmit encouraged) |
| Major | Reject | Reject | Reject | **Reject** |
| Reject | Reject | Reject | Reject | **Reject** |

### Special Situation Handling

**Split Decision (evenly divided)**:
- Example: Accept + Accept + Reject + Reject
- EIC (or synthesizer) needs to deeply analyze the cause of disagreement
- Lean toward conservative strategy: Major Revision, requiring the author to respond to the Reject side's comments
- May consider inviting a fifth reviewer

**One Outlier (one unusual opinion)**:
- Example: Minor + Minor + Minor + Reject
- Carefully examine the Reject rationale
- If the rationale is valid and others missed it, escalate to Major Revision
- If the rationale is insufficient, maintain Minor Revision but mention the opinion in the Decision Letter

---

## 3. Decision Confidence Calibration

### Impact of Reviewer Confidence Score

| Confidence | Impact on Decision |
|-----------|-------------------|
| 5 (Very High) | This reviewer's opinion carries the highest weight |
| 4 (High) | Standard weight |
| 3 (Medium) | Standard weight, but reduced in case of disagreement |
| 2 (Low) | For reference only, not used as a decisive opinion |
| 1 (Very Low) | Ignore this reviewer's recommendation (but retain specific comments) |

### Cross-Dimension Severity Assessment

| Situation | Severity | Handling |
|-----------|----------|---------|
| Methodology has fatal flaw (R1 score = 1) | Critical | Even if other dimensions are excellent, lean toward Reject |
| Major literature review omission (R2 score = 2) | Serious | Major Revision, require supplementation |
| Cross-disciplinary perspective overlooked (R3 score = 2) | Moderate | Minor/Major, depends on other dimensions |
| Poor writing quality (score = 2) | Minor | Does not affect academic decision, but require language revision |

---

## 4. Revision Round Policy

### Standard Policy

| Round | Expectation | Handling |
|-------|-------------|---------|
| R1 (First revision) | Respond to all reviewer comments | Send for re-review or EIC review |
| R2 (Second revision) | Respond to residual issues | Usually EIC makes final decision |
| R3 (Third revision) | Very rare, usually only handling formatting | EIC makes final decision |

### Upgrade/Downgrade Rules

- Minor Revision with incomplete revisions -> May escalate to Major Revision
- Major Revision with excellent revisions -> May downgrade to Minor Revision or Accept
- Major Revision with insufficient revisions -> May Reject (infinite revision cycles are not encouraged)
- Beyond 2 rounds of Major Revision -> Strongly recommend Accept or Reject, no further extension

---

## 5. Professional Ethics of Editorial Review

### Reviewer Ethics

1. **Confidentiality**: The review process and paper content are confidential
2. **Conflict of interest**: Recuse if there is a collaborative or competitive relationship with the author
3. **Timeliness**: Complete the review within the committed timeframe
4. **Constructiveness**: Even when recommending Reject, provide constructive feedback
5. **Impartiality**: No bias based on author's gender, race, institution, or nationality
6. **No plagiarism**: Do not use unpublished ideas seen during review
7. **Appropriate language**: Avoid personal attacks, sarcasm, or demeaning language

### Editor Ethics

1. **Fair decision**: Based on academic quality, not influenced by external pressure
2. **Transparent process**: Decision letter must clearly explain the rationale
3. **Reasonable deadlines**: Give authors sufficient revision time
4. **Appeal channel**: Authors have the right to respond to or challenge review comments
5. **Consistent standards**: Papers of similar quality should receive similar decisions

### Ethical Considerations for Special Situations

| Situation | Ethical Handling |
|-----------|-----------------|
| Author is your student/colleague | Must recuse or disclose the relationship |
| Paper's viewpoint is opposite to yours | Evaluate argument quality, not correctness of position |
| Paper uses your theory but misunderstands it | May point it out but cannot require citation of your own work |
| Suspected data fabrication | Report to EIC; journal initiates investigation procedure |
| Paper is similar to your ongoing research | Disclose potential conflict of interest |
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-reviewer-references-guided-mode-protocol-md"></a>

## SOURCE: skills/academic-paper-reviewer/references/guided_mode_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=1971 -->
# Guided Mode (Socratic Guided Review)

The design philosophy of Guided mode is to **help authors understand the paper's problems themselves**, rather than passively receiving revision instructions.

### How It Works

```
Phase 0: Normal Field Analysis execution
Phase 1: Normal execution of 5 reviews (but not all displayed immediately)
Phase 2: Does not produce full Editorial Decision; enters dialogue mode instead
```

### Dialogue Flow

1. **EIC opens**: First points out 1-2 core strengths of the paper (building confidence), then raises the most critical structural issue
2. **Wait for author response**: Author thinks, responds, or asks questions
3. **Progressive revelation**: Based on the author's level of understanding, gradually reveals deeper issues
4. **Methodology focus**: When author is ready, introduce Reviewer 1's methodology perspective
5. **Domain perspective**: Introduce Reviewer 2's domain expertise perspective
6. **Cross-disciplinary challenge**: Introduce Reviewer 3's unique perspective
7. **Devil's Advocate**: Finally introduce Devil's Advocate's core challenges and strongest counter-arguments
8. **Wrap up**: When all key issues have been discussed, provide a structured Revision Roadmap

### Dialogue Rules

- Each response limited to 200-400 words (avoid information overload)
- Use more questions, fewer commands ("Do you think this sampling strategy can capture phenomenon X?" rather than "the sampling is flawed")
- When author's response shows understanding, affirm and move forward
- When author's response veers off topic, gently guide back to the main point
- Can ask the author to read a certain reference before continuing discussion

### v3.6.2 sprint contract status

v3.6.2 introduces sprint contracts for `reviewer_full` and `reviewer_methodology_focus` only. A template for this mode will follow in a subsequent patch release. Until then, this mode runs without contract enforcement and retains its pre-v3.6.2 behaviour.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-reviewer-references-integration-guide-md"></a>

## SOURCE: skills/academic-paper-reviewer/references/integration_guide.md

<!-- SOURCE-CONTENT-BEGIN bytes=680 -->
# Pipeline Usage Example

```
User: I want to write a paper about AI in higher education quality assurance, from research to submission

Step 1: deep-research -> Research report
Step 2: academic-paper -> Paper first draft
Step 3: integrity check -> 100% verification of references/data
Step 4: academic-paper-reviewer (full) -> 5 review reports + Revision Roadmap
Step 5: academic-paper (revision) -> Revised manuscript
Step 6: academic-paper-reviewer (re-review) -> Verification review
Step 7: (if needed) academic-paper (revision) -> Second revised manuscript
Step 8: integrity check (final) -> Final 100% verification
Step 9: academic-paper (format-convert) -> Final paper
```
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-reviewer-references-quality-rubrics-md"></a>

## SOURCE: skills/academic-paper-reviewer/references/quality_rubrics.md

<!-- SOURCE-CONTENT-BEGIN bytes=7679 -->
# Quality Rubrics for Academic Paper Review

## Purpose

Provides calibrated scoring rubrics for the 7 review dimensions used by all reviewers (R1, R2, R3, DA). Ensures consistent, reproducible scoring across different papers and review sessions.

## Known error profile (v3.2)

These rubrics define *what* to measure, not *how accurate* the measurement is. A single LLM reviewer's absolute rubric score has calibration error that depends on domain, paper type, and model version.

For users who want to know this reviewer's empirical FNR / FPR / balanced accuracy before relying on these rubric scores, run the opt-in **calibration mode** (see `calibration_mode_protocol.md`). Calibration mode compares this reviewer's decisions against a user-supplied gold set and produces a Calibration Report that attaches as a confidence disclosure to subsequent reviews in the same session.

Without calibration, treat rubric scores as *ordinally* meaningful (papers scored 85 are better than papers scored 65) but *not cardinally* interpretable (a 85 does not guarantee venue acceptance).

## Scoring Scale

All dimensions scored 0-100. Final weighted score determines editorial decision.

## Decision Mapping

| Weighted Average | Decision |
|-----------------|----------|
| >= 80 | Accept |
| 65-79 | Minor Revision |
| 50-64 | Major Revision |
| < 50 | Reject |

---

## Dimension 1: Originality (Weight: 20%)

| Score Range | Descriptor | Behavioral Indicators |
|------------|------------|----------------------|
| 90-100 | Exceptional | Novel theoretical framework supported by empirical evidence; opens entirely new research direction; implications span 3+ fields; no prior work addresses this exact question |
| 75-89 | Strong | Novel methodology OR novel application of existing theory to new context; clear contribution beyond incremental extension; implications for 2+ fields |
| 60-74 | Adequate | Extends existing framework with new data, population, or context; contribution is clear but incremental; single-field implications |
| 45-59 | Weak | Replicates existing study with minor variations; contribution is marginal; "so what?" question not convincingly answered |
| < 45 | Insufficient | No discernible original contribution; duplicates existing work without justification; purely descriptive without analytical insight |

## Dimension 2: Methodological Rigor (Weight: 25%)

| Score Range | Descriptor | Behavioral Indicators |
|------------|------------|----------------------|
| 90-100 | Exceptional | Research design perfectly aligned with RQ; all validity threats addressed; appropriate statistical methods with power analysis; transparent reporting (all EQUATOR items); reproducible |
| 75-89 | Strong | Sound design with minor gaps; most validity threats addressed; appropriate methods with minor reporting omissions; largely reproducible |
| 60-74 | Adequate | Acceptable design but some validity concerns; methods appropriate but justification lacking; some reporting gaps (missing effect sizes, CIs) |
| 45-59 | Weak | Design has significant flaws; method choice questionable; multiple reporting gaps; reproducibility doubtful |
| < 45 | Insufficient | Fundamental design flaws that invalidate findings; inappropriate methods; results cannot be trusted |

## Dimension 3: Evidence Sufficiency (Weight: 25%)

| Score Range | Descriptor | Behavioral Indicators |
|------------|------------|----------------------|
| 90-100 | Exceptional | >40 sources, 80%+ peer-reviewed, multi-method triangulation, primary + secondary data, all claims well-supported, counter-evidence acknowledged |
| 75-89 | Strong | 25-40 sources, 70%+ peer-reviewed, adequate evidence for main claims, some triangulation |
| 60-74 | Adequate | 15-25 sources, 60%+ peer-reviewed, key claims supported but some gaps, limited triangulation |
| 45-59 | Weak | <15 sources OR <50% peer-reviewed, several unsupported claims, no triangulation |
| < 45 | Insufficient | Severely under-sourced, major claims unsupported, relies heavily on grey literature or anecdotal evidence |

## Dimension 4: Argument Coherence (Weight: 15%)

| Score Range | Descriptor | Behavioral Indicators |
|------------|------------|----------------------|
| 90-100 | Exceptional | Crystal-clear logical flow from problem -> gap -> RQ -> method -> findings -> implications; every section builds on previous; no logical jumps; counterarguments pre-empted |
| 75-89 | Strong | Clear logical flow with minor gaps; most transitions well-handled; argument generally persuasive |
| 60-74 | Adequate | Main argument visible but some sections feel disconnected; occasional logical jumps; conclusions mostly follow from evidence |
| 45-59 | Weak | Argument structure unclear; significant logical gaps; conclusions overreach evidence; reader must infer connections |
| < 45 | Insufficient | No coherent argument; sections appear unrelated; conclusions do not follow from evidence; circular reasoning |

## Dimension 5: Writing Quality (Weight: 15%)

| Score Range | Descriptor | Behavioral Indicators |
|------------|------------|----------------------|
| 90-100 | Exceptional | Professional academic prose; precise terminology; excellent paragraph structure; zero grammatical errors; appropriate register throughout |
| 75-89 | Strong | Good academic writing; minor stylistic inconsistencies; few grammatical issues; terminology mostly precise |
| 60-74 | Adequate | Acceptable writing but room for improvement; some verbose passages; occasional imprecise terminology; some grammar issues |
| 45-59 | Weak | Below journal standards; frequent verbose/unclear passages; terminology inconsistent; multiple grammar issues |
| < 45 | Insufficient | Unacceptable writing quality; incomprehensible passages; severe grammar problems; not suitable for peer review |

## Optional Dimensions (reviewer-specific)

### Literature Integration (R2 Domain Expert focus)

| Score Range | Descriptor |
|------------|------------|
| 90-100 | Comprehensive coverage of seminal + recent works; identifies theoretical lineage; positions paper precisely in scholarly conversation |
| 75-89 | Good coverage; most key works cited; reasonable positioning in literature |
| 60-74 | Adequate but gaps in coverage; some important works missing; positioning somewhat vague |
| < 60 | Significant literature gaps; key works missing; poor positioning |

### Significance & Impact (R3 Perspective Reviewer focus)

| Score Range | Descriptor |
|------------|------------|
| 90-100 | Clear practical implications for policy/practice AND theory; addresses urgent real-world problem; likely to influence field direction |
| 75-89 | Good practical OR theoretical implications; addresses relevant problem; moderate influence potential |
| 60-74 | Some implications but narrowly scoped; relevance clear but impact limited |
| < 60 | Minimal practical or theoretical significance; unclear why this matters |

---

## Aggregation Formula

```
Final Score = (Originality x 0.20) + (Methodology x 0.25) + (Evidence x 0.25) + (Coherence x 0.15) + (Writing x 0.15)
```

Optional dimensions are reported separately and factored into the editorial synthesis narrative but do not change the numerical score.

---

## Calibration Notes

- Scores should reflect the paper's quality relative to the target journal's standards
- A "75" for Nature is not equivalent to "75" for a regional journal
- When in doubt, err toward the middle of a range
- Reviewers should explicitly state which range descriptor best matches, then fine-tune within that range
- If two dimensions are at odds (e.g., excellent methodology but weak writing), do NOT average down — report both scores honestly
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-reviewer-references-re-review-mode-protocol-md"></a>

## SOURCE: skills/academic-paper-reviewer/references/re_review_mode_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=4250 -->
# Re-Review Mode (Verification Review)

Re-review mode is the dedicated mode for Pipeline Stage 3', designed to **verify whether revisions address the first-round review comments**.

### How It Works

```
Input:
1. Original Revision Roadmap (Stage 3 output)
2. Revised manuscript
3. Response to Reviewers (optional)

Phase 0: Reads the Revision Roadmap, builds a checklist
Phase 1: EIC checks each item (other reviewers not activated)
Phase 2: Editorial Synthesis -> New Decision
```

### Verification Logic

```
For each item in the Revision Roadmap:

Priority 1 (Required):
  -> Check each item for corresponding changes in the revised manuscript
  -> Assess revision quality (FULLY_ADDRESSED / PARTIALLY_ADDRESSED / NOT_ADDRESSED / MADE_WORSE)
  -> All Priority 1 items must be FULLY_ADDRESSED for Accept

**Traceability Rule**: For each Priority 1 item, the reviewer MUST:
1. Read the author's claim from the Response to Reviewers
2. Navigate to the stated revision location in the manuscript
3. Independently verify the claim matches the actual change
4. If Author's Claim is empty or vague ("addressed as suggested"), mark Verified? as `🔍 Cannot verify` and flag in Quality Assessment

Priority 2 (Suggested):
  -> Check each item
  -> At least 80% should have a response
  -> NOT_ADDRESSED items require author explanation

Priority 3 (Nice to Fix):
  -> Check but does not affect Decision
```

### New Issue Detection

```
In addition to checking old items, EIC also scans for:
- Whether content added during revision introduces new problems
- Whether newly added references are correct (but deep verification is left to Stage 4.5 integrity check)
- Whether revisions cause inconsistencies
```

### Socratic Guidance After Re-Review

```
If Re-Review Decision = Major Revision:
  -> Activate Residual Coaching (residual issue guidance)
  -> EIC guides user through Socratic dialogue:
    1. Gap analysis — "How many issues did the first round of revisions resolve? Why are the remaining ones hard to address?"
    2. Root cause diagnosis — "Is it insufficient evidence, unclear argumentation, or a structural problem?"
    3. Trade-off decisions — "Which ones can be marked as research limitations?"
    4. Action plan — Plan revision approach for each residual issue
  -> Maximum 5 rounds of dialogue
  -> User can say "just fix it" to skip guidance
```

### Re-Review Output Format

```markdown
# Verification Review Report

## Decision
[Accept / Minor Revision / Major Revision]

## Revision Response Checklist

### Priority 1 — Required Revisions

| # | Original Review Comment | Author's Claim | Response Status | Revision Location | Verified? | Quality Assessment |
|---|------------------------|---------------|-----------------|-------------------|-----------|-------------------|
| R1 | [Original text] | [What the author claims to have done in Response to Reviewers] | FULLY_ADDRESSED | Section X.X | ✅ Yes | Adequately addressed; newly added content effectively resolves the issue |
| R2 | [Original text] | [Author's stated change] | PARTIALLY_ADDRESSED | Section Y.Y | ⚠️ Partial | Partially addressed, but still missing [specific gap] |

### Priority 2 — Suggested Revisions

| # | Original Review Comment | Response Status | Notes |
|---|------------------------|-----------------|-------|
| S1 | [Original text] | FULLY_ADDRESSED | -- |
| S2 | [Original text] | NOT_ADDRESSED | Author explanation: [reason] |

### Priority 3 — Nice to Fix

| # | Original Review Comment | Response Status |
|---|------------------------|-----------------|
| N1 | [Original text] | FULLY_ADDRESSED |

## New Issues (Discovered During Revision)

| # | Type | Location | Description |
|---|------|----------|-------------|
| NEW-1 | [Type] | Section X.X | [Description] |

## Decision Rationale
[Rationale based on the checklist]

## Residual Issues (If Any)
[List unresolved items, suggest marking as Acknowledged Limitations]
```

## v3.6.2 sprint contract status

v3.6.2 introduces sprint contracts for `reviewer_full` and `reviewer_methodology_focus` only. A template for this mode will follow in a subsequent patch release. Until then, this mode runs without contract enforcement and retains its pre-v3.6.2 behaviour.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-reviewer-references-review-criteria-framework-md"></a>

## SOURCE: skills/academic-paper-reviewer/references/review_criteria_framework.md

<!-- SOURCE-CONTENT-BEGIN bytes=10139 -->
# Review Criteria Framework — Structured Review Criteria Framework

This document defines universal criteria for academic paper review and type-specific criteria differentiated by paper type. All reviewer agents share this framework.

---

## 1. Universal Review Dimensions

Seven core dimensions applicable to all paper types:

### Dimension 1: Originality — Weight 15%

| Level | Score | Description |
|-------|-------|-------------|
| Outstanding | 5 | Proposes entirely new theory/method/evidence that could change the field's direction |
| Strong | 4 | Has clear new insights or novel combinations, fills a specific research gap |
| Adequate | 3 | Incremental contribution, reasonable extension of existing knowledge |
| Weak | 2 | Highly overlapping with existing literature, new contribution unclear |
| None | 1 | Essentially repeats what is already known |

### Dimension 2: Methodological Rigor — Weight 25%

| Level | Score | Description |
|-------|-------|-------------|
| Outstanding | 5 | Impeccable research design, innovative methods executed flawlessly |
| Strong | 4 | Sound design, appropriate methods, minor room for improvement in execution |
| Adequate | 3 | Methods basically acceptable, but with some design or execution limitations |
| Weak | 2 | Methods have significant flaws affecting the credibility of conclusions |
| Unacceptable | 1 | Methods fundamentally unsuitable for answering the research question, or contain serious errors |

### Dimension 3: Evidence Sufficiency — Weight 20%

| Level | Score | Description |
|-------|-------|-------------|
| Outstanding | 5 | Rich, diverse, and persuasive evidence that exceeds expectations |
| Strong | 4 | Evidence sufficiently supports all major arguments |
| Adequate | 3 | Most arguments supported by evidence, a few need supplementation |
| Weak | 2 | Key arguments lack sufficient evidence |
| Unacceptable | 1 | Serious disconnect between arguments and evidence |

### Dimension 4: Argument Coherence — Weight 15%

| Level | Score | Description |
|-------|-------|-------------|
| Outstanding | 5 | Clear arguments, rigorous logic, elegant structure |
| Strong | 4 | Smooth argumentation, occasional minor logical leaps |
| Adequate | 3 | Basically coherent, but some inter-paragraph connections are unclear |
| Weak | 2 | Multiple logical breaks, readers have difficulty following the argument |
| Unacceptable | 1 | Confused argumentation, core claims cannot be identified |

### Dimension 5: Writing Quality — Weight 10%

| Level | Score | Description |
|-------|-------|-------------|
| Outstanding | 5 | Precise and fluent academic English/Chinese, a model of scholarly writing |
| Strong | 4 | Clear language, occasional minor imperfections that don't affect understanding |
| Adequate | 3 | Generally readable, with some grammar or word choice issues |
| Weak | 2 | Frequent language issues that affect understanding |
| Unacceptable | 1 | Language quality does not meet reviewable standards |

### Dimension 6: Literature Integration — Weight 10%

| Level | Score | Description |
|-------|-------|-------------|
| Outstanding | 5 | Comprehensive, contemporary, critically integrated literature with a compelling research gap argument |
| Strong | 4 | Covers major literature, with good integration and positioning |
| Adequate | 3 | Basic coverage, but with omissions or insufficient integration |
| Weak | 2 | Literature is outdated, incomplete, or merely enumerated |
| Unacceptable | 1 | Seriously insufficient literature review or irrelevant to the topic |

### Dimension 7: Significance & Impact — Weight 5%

| Level | Score | Description |
|-------|-------|-------------|
| Outstanding | 5 | Could change policy, practice, or theoretical direction |
| Strong | 4 | Clear impact on a specific field or practice |
| Adequate | 3 | Has some academic or practical value |
| Weak | 2 | Limited scope of impact, mainly academic interest |
| Marginal | 1 | Difficult to see the significance of the research |

---

## 2. Paper Type-Specific Criteria

### 2.1 Empirical Research

Beyond universal dimensions, specifically focus on:

| Additional Dimension | Review Focus |
|---------------------|-------------|
| Research hypothesis clarity | Are hypotheses testable and consistent with theory |
| Variable operational definitions | Are independent/dependent/control variable definitions precise |
| Internal validity | Are confounding variables controlled |
| External validity | Generalizability of results |
| Statistical reporting completeness | Effect sizes, confidence intervals, assumption testing |
| Conclusion conservatism | Do conclusions exceed what the data supports |

### 2.2 Theoretical/Conceptual Paper

| Additional Dimension | Review Focus |
|---------------------|-------------|
| Conceptual definition precision | Are core concepts clearly delineated |
| Argument logic structure | Is the premise -> inference -> conclusion logic chain complete |
| Counterargument handling | Are possible opposing viewpoints considered and addressed |
| Theoretical novelty | Does it truly advance theoretical development |
| Testability | Can the theory generate testable propositions |

### 2.3 Literature Review / Meta-analysis

| Additional Dimension | Review Focus |
|---------------------|-------------|
| Search strategy | Is it comprehensive and reproducible (PRISMA compliance) |
| Inclusion/exclusion criteria | Are criteria clear, reasonable, and consistently applied |
| Bias risk assessment | Is bias risk of included studies assessed |
| Heterogeneity handling | Is statistical and conceptual heterogeneity appropriately handled |
| Synthesis method | Goes beyond simple vote counting to achieve critical synthesis |
| Publication Bias | Is publication bias assessed and discussed |

### 2.4 Case Study

| Additional Dimension | Review Focus |
|---------------------|-------------|
| Case selection justification | Why was this case chosen? What does it represent? |
| Theoretical vs convenience sampling | Is case selection theoretically grounded |
| Triangulation | Are multiple data sources used |
| Context description thickness | Is thick description sufficient |
| Analysis transferability | Are analysis results transferable to other contexts |
| Researcher reflexivity | Is the researcher's relationship with the case reflected upon |

### 2.5 Policy Analysis / Policy Brief

| Additional Dimension | Review Focus |
|---------------------|-------------|
| Policy problem definition | Is the problem clearly defined and evidence-supported |
| Stakeholder analysis | Are key stakeholders identified |
| Policy option analysis | Are multiple options proposed and compared |
| Feasibility assessment | Are policy recommendations practically feasible |
| Evidence quality | Are policy recommendations based on reliable evidence |
| Unintended consequences | Are unintended policy impacts considered |

---

## 3. Common Review Pitfalls

### Biases Reviewers Should Avoid

| Pitfall | Description | How to Avoid |
|---------|-------------|--------------|
| **Hypercriticism** | Overblowing minor issues, ignoring the paper's overall contribution | Affirm strengths first, then point out issues; distinguish major from minor |
| **Confirmation Bias** | Only finding evidence supporting pre-existing views | Deliberately seek the paper's merits and counterexamples to your own views |
| **Preference Projection** | Requiring authors to use "my method" rather than evaluating "the author's method" | Ask "can this method answer the question" rather than "what would I do" |
| **Paradigm Bias** | Using quantitative standards to judge qualitative research (or vice versa) | Use evaluation criteria matching the paper's research paradigm |
| **Prestige Bias** | Relaxing standards because of the author's institution or past achievements | Focus on the quality of the paper itself |
| **Novelty Bias** | Only valuing novel research, undervaluing replication studies | Acknowledge the important role of replication in science |
| **Length Bias** | Long paper = good paper, short paper = sloppy | Evaluate content density, not page count |
| **Language Discrimination** | Undervaluing research quality due to non-native language imperfections | Distinguish "language needs polishing" from "research quality is poor" |

### Principles of Constructive Feedback

1. **Specific, not vague**: "The causal inference in Section 3, paragraph 2 lacks control variables" is better than "methodology has problems"
2. **Problem + reason + suggestion**: Every criticism should include "what," "why," and "how to fix"
3. **Distinguish required from suggested**: Which changes are mandatory, which are "nice to have"
4. **Acknowledge uncertainty**: "I'm not sure whether this analysis accounts for X" is more accurate than "the author ignored X"
5. **Respect the author**: Even if paper quality is poor, the author still invested time and effort

---

## 4. Scoring Aggregation

### Weighted Total Score Calculation

```
Total Score =
  Originality (15%) +
  Methodological Rigor (25%) +
  Evidence Sufficiency (20%) +
  Argument Coherence (15%) +
  Writing Quality (10%) +
  Literature Integration (10%) +
  Significance (5%)
```

### Score-to-Decision Mapping

| Weighted Total | Recommended Decision | Note |
|---------------|---------------------|------|
| 4.5-5.0 | Accept | Very few papers reach this level |
| 3.5-4.4 | Minor Revision | Overall quality is good, minor revisions needed |
| 2.5-3.4 | Major Revision | Has potential but needs substantial revision |
| 1.5-2.4 | Reject (Resubmit) | Fundamental issues need rework, but topic has value |
| 1.0-1.4 | Reject | Not suitable for this journal or quality below standard |

**Important reminder**: Scores are only reference. The final decision also needs to consider:
- Whether any single dimension is particularly low (e.g., methodology score of 1), which may lead to Reject even if the overall score is passable
- Specific content of reviewer comments is more important than numbers
- Special considerations of the journal (special issue, field development needs, etc.)
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-reviewer-references-review-quality-thinking-md"></a>

## SOURCE: skills/academic-paper-reviewer/references/review_quality_thinking.md

<!-- SOURCE-CONTENT-BEGIN bytes=3015 -->
# Review Quality Thinking Framework

A cognitive framework for producing high-quality reviews. Teaches **how to think** about paper quality, not just what to score.

## The Three Lenses

Every paper should be evaluated through three lenses simultaneously:

### Lens 1: Internal Validity — "Does the evidence support the claims?"

Ask in order:
1. What is the central claim?
2. What evidence is presented?
3. Is there a logical chain from evidence to claim? (Warrant)
4. Are there alternative explanations the authors didn't consider?
5. Would removing any single piece of evidence collapse the argument?

**If #5 is yes**: The argument depends on a single linchpin. Flag it — the paper's contribution is only as strong as that one piece of evidence.

### Lens 2: External Validity — "Does this matter beyond this study?"

Ask in order:
1. Who is the population of interest?
2. Does the sample represent that population?
3. Are the conditions replicable?
4. Would the findings hold in a different context/culture/time?
5. What are the boundary conditions the authors don't mention?

**Judgment heuristic**: Most authors overstate generalizability. If the sample is from one university in one country, findings cannot claim to apply "generally" without qualification.

### Lens 3: Contribution — "So what?"

Ask in order:
1. What did we know before this paper?
2. What do we know after?
3. Is the delta meaningful (not just statistically significant)?
4. Who benefits from knowing this?
5. What new questions does this open?

**Judgment heuristic**: If you can't articulate the delta in one sentence, either the contribution is weak or the paper hasn't communicated it clearly. Both are review-worthy observations.

## Common Reviewer Traps

| Trap | Description | How to Avoid |
|------|-------------|-------------|
| **Methodological tunnel vision** | Only critiquing methods, ignoring whether the question matters | Start with Lens 3 (contribution) before Lens 1 |
| **Novelty bias** | Penalizing replication or incremental work | Replication IS valuable; evaluate on execution quality |
| **Expertise projection** | Expecting the paper to use your preferred method | Evaluate the chosen method on its own terms |
| **Positivity-severity oscillation** | Being too nice in comments, too harsh in scores | Write the score first, then justify with comments |
| **Missing forest for trees** | Listing 20 minor issues, missing the one fatal flaw | Always state the single most important issue first |

## Calibration Questions (ask after drafting your review)

1. If this paper were published as-is, would it mislead readers? (If yes → Major Revision or Reject)
2. Could the authors reasonably address my concerns in one revision cycle? (If no → Reject)
3. Am I being harder on this paper than I would be on my own work? (Calibration check)
4. Did I identify at least one genuine strength? (Balance check)
5. Would my review help the authors improve, even if the paper is rejected? (Constructiveness check)
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-reviewer-references-sprint-contract-protocol-md"></a>

## SOURCE: skills/academic-paper-reviewer/references/sprint_contract_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=11621 -->
# Sprint Contract Protocol (v3.6.2)

> Authoritative orchestration reference for the ARS v3.6.2 sprint-contract hard gate.
> Schema: `shared/sprint_contract.schema.json` (Schema 13.1 since v3.6.6).
> Templates: `shared/contracts/reviewer/*.json`.
> Design spec: `docs/design/2026-04-23-ars-v3.6.2-sprint-contract-design.md`.
>
> **v3.6.6 cross-reference**: this reviewer protocol is byte-equivalent across v3.6.2 → v3.6.6 (zero-touch promise per §3.6 of `docs/design/2026-04-27-ars-v3.6.6-generator-evaluator-contract-design.md`). The v3.6.6 release adds a parallel generator-evaluator protocol inside `academic-paper` for the in-pair writer / evaluator pair (see `academic-paper/SKILL.md` § "v3.6.6 Generator-Evaluator Contract Protocol" and design doc §5).

## 1. Overview

A reviewer sprint contract is a machine-checkable pre-registered acceptance criterion. The orchestrator loads a frozen template, inlines runtime fields (`generated_at`, optional `agent_amendments`), and drives each reviewer through a paper-content-blind Phase 1 followed by a paper-visible Phase 2. The synthesizer then runs a three-step mechanical protocol over the `panel_size` reviewer outputs to emit an editorial decision.

This protocol exists to destroy the "read the paper, then rationalise the scoring standard" drift path. The load-bearing mechanism is the **physical separation of calls**: Phase 1 never sees paper content.

## 2. Two-phase reviewer call

For each reviewer in `range(panel_size)`:

1. **Prepare contract.** Load template from `shared/contracts/<domain>/<mode>.json`. Populate `generated_at` (ISO-8601 UTC). Optionally populate `agent_amendments` (field-specific notes from `field_analyst_agent`). Run `check_sprint_contract.py` on the in-memory object; abort on error.
2. **Phase 1 call (paper-content-blind).**
   - System prompt: the `### Phase 1 — Paper-content-blind pre-commitment` sub-section of the reviewer agent's `## v3.6.2 Sprint Contract Protocol` block.
   - User content: contract JSON + paper metadata ONLY (`title`, `field`, `word_count`).
   - Expected output: `## Contract Paraphrase`, `## Scoring Plan`, terminal `[CONTRACT-ACKNOWLEDGED]` tag.
3. **Phase 1 output lint.** See §4 below.
4. **Phase 2 call (paper-visible).**
   - System prompt: the `### Phase 2 — Paper-visible review` sub-section of the same `## v3.6.2 Sprint Contract Protocol` block.
   - User content: contract JSON (re-injected) + Phase 1 output wrapped in `<phase1_output>...</phase1_output>` data delimiter + full paper.
   - Expected output: optional `## Scoring Plan Dissent`, `## Dimension Scores`, `## Failure Condition Checks`, `## Review Body`, `## Editorial Decision`.
5. **Phase 2 output lint.** See §5 below.
6. **Panel cardinality invariant.** After all reviewers complete, verify `len(usable_phase2_outputs) == panel_size`. If any reviewer was dropped, emit `[PANEL-SHRUNK]` and abort the round (see §6).
7. Feed usable Phase 2 outputs into synthesizer (see §7).

## 3. Contract injection

- **Template on disk is frozen.** Do not mutate. Deep-copy into an in-memory dict.
- **Runtime-only fields:** `generated_at`, `agent_amendments.stage_specific_notes`, `agent_amendments.additional_measurement_hints`.
- **Baseline fields are orchestrator-immutable.** Schema cannot enforce this; the orchestrator must not rewrite `acceptance_dimensions` / `failure_conditions` / `measurement_procedure` / `override_ladder` / `mode` / `stage` / `contract_id` / `baseline_version` / `panel_size` between template load and injection. Optional: emit sha256 of baseline-field subset to audit log for drift detection.

## 4. Phase 1 output lint

Structural checks (orchestrator, not validator). On failure retry Phase 1 once with the specific lint gap hinted in the system prompt; second failure aborts that reviewer.

- Required sections in order: `## Contract Paraphrase`, `## Scoring Plan`, terminal `[CONTRACT-ACKNOWLEDGED]`.
- Paraphrase paragraph count ≥ `measurement_procedure.paraphrase_minimum_dimensions` (for `"all"`, one paragraph per dimension; for integer `k`, at least `k` paragraphs each matching a distinct dimension).
- `## Scoring Plan` has one `### <Dn>: <name>` subsection per acceptance dimension (always full coverage, regardless of `paraphrase_minimum_dimensions`).
- Each `scoring_plan` subsection contains lines matching `measurement_procedure.scoring_plan_schema.required`.
- Phase 1 content refers to `<title>`, `<field>`, `<word_count>` only; no specific paper content. Not schema-enforced; behavioural rule in reviewer prompt.

**Lint is structural, not semantic.** A reviewer can in principle pass this lint by emitting generic boilerplate triggers — semantic judgement (whether triggers are concrete and discriminating) is deferred to a post-v3.6.2 judge-agent layer.

On second Phase 1 failure: emit `[PROTOCOL-VIOLATION: reviewer=<role>, contract=<id>, phase1_lint_failed=true]` and mark this reviewer unusable.

## 5. Phase 2 output lint

Structural checks run before handoff to synthesizer. **No Phase 2 retry** (reviewer has seen the paper; a second call is tainted) EXCEPT the multi-dissent case below.

- Required sections: `## Dimension Scores`, `## Failure Condition Checks`, `## Review Body`, `## Editorial Decision`.
- `## Dimension Scores` has one `### <Dn>: <name>` subsection per contract dimension; each carries a value in `$defs.score` (`block | warn | pass`).
- `## Failure Condition Checks` has one subsection per `failure_conditions[]` entry with `fired: true | false`.
- **Multi-dissent rule:** If `## Scoring Plan Dissent` names two or more `dimension_id` entries, orchestrator aborts this reviewer and retries from **Phase 1** once. If the retried Phase 1/2 also multi-dissents, mark the reviewer unusable (`[PROTOCOL-VIOLATION]`). One-dimension-per-reviewer-per-Phase-2-call is the cap.
- **Consistency check (structural):** For every dimension not under dissent, the Phase 2 score must substring-match the reviewer's Phase 1 `scoring_plan` trigger tokens. Vacuous triggers bypass this check — documented limitation.
- `## Editorial Decision` is one of the `action` values derivable from `## Failure Condition Checks` via the synthesizer precedence rule (§8 step 3). Inconsistency marks the reviewer unusable.

On any Phase 2 lint failure other than multi-dissent: emit `[PROTOCOL-VIOLATION]` and mark reviewer unusable. Do not synthesise a substitute score for the synthesizer.

## 6. Multi-reviewer orchestration

- **Independent cycles.** Each of the `panel_size` reviewers runs its own Phase 1 + Phase 2. Failures in one do not pause the others.
- **Panel cardinality invariant (§2 step 6).** After all reviewers complete, if `len(usable_phase2_outputs) < panel_size`, abort the editorial round with `[PANEL-SHRUNK]`. Do not silently recompute `cross_reviewer_quantifier` thresholds against a smaller panel — the contract's published aggregation semantics bind on a specific `panel_size`.
- **Operational monitor.** Track `[PANEL-SHRUNK]` rate in real SR runs. If > 5% of rounds abort in first 3 months, v3.6.3 introduces graceful-degradation fallback.

## 7. Reviewer panel mapping

| mode                          | panel_size | invoked reviewers |
|-------------------------------|------------|-------------------|
| `reviewer_full`               | 5          | EIC + methodology + domain + perspective + DA |
| `reviewer_methodology_focus`  | 2          | EIC + methodology (only) |
| `reviewer_re_review`          | —          | not shipped in v3.6.2; continues pre-v3.6.2 behaviour |
| `reviewer_calibration`        | —          | not shipped in v3.6.2 |
| `reviewer_guided`             | —          | not shipped in v3.6.2 |

The orchestrator uses `mode` to determine the panel and the contract's `panel_size` as the invariant target. SC-11 validator check ensures mode and `panel_size` are consistent.

## 8. Synthesizer three-step protocol

Let `N = contract.panel_size`.

**Step 1 — Build scoring matrix.** For each `acceptance_dimensions[i]`, gather N reviewers' `## Dimension Scores` for that dimension into a length-N array of `$defs.score` values. Dimensions resolved by `id`.

**Step 2 — Evaluate each `failure_conditions[]`.** For each condition:

1. Parse `expression` against the recognised patterns (see §9 vocabulary). Unrecognised → emit `[EXPRESSION-UNRECOGNISED]`, abort synthesizer.
2. Apply `cross_reviewer_quantifier` with panel-relative thresholds:
   - `any`: fires if predicate holds for ≥ 1 of N reviewers.
   - `majority`: for N ≥ 3, fires if ≥ `⌈N/2⌉ + 1`; for N == 2, fires if all 2; for N == 1, vacuous (SC-11 warns).
   - `all`: fires if predicate holds for all N reviewers.
3. Record `{condition_id, fired}`.

**Step 3 — Precedence and decision.** Among fired conditions, pick the one with highest `severity`. Ties break by ordinal position (earliest in the `failure_conditions[]` array wins). Emit its `action` as `editorial_decision`.

**Forbidden operations (synthesizer prompt hard constraint):**
- Introduce aggregation rules not derivable from `cross_reviewer_quantifier` + `severity`.
- Average or vote-aggregate scores within a single dimension unless `cross_reviewer_quantifier: majority` explicitly requests it.
- Soften a fired condition's `action` on post-hoc grounds.
- Synthesise substitute scores for reviewers marked unusable — the round is either complete with `panel_size` usable outputs or `[PANEL-SHRUNK]` aborted.

## 9. Recognised expression vocabulary

Synthesizer recognises the following patterns (with accepted natural-English variants):

1. **Priority-scoped single-match:** `any <priority> dimension scores '<score>'` | `any dimension with priority=<priority> scores '<score>'` | `any <priority>-priority dimension scores '<score>'`
2. **Priority-scoped count-based:** `two or more <priority> dimensions score '<score>' or worse` | `two or more dimensions with priority=<priority> score '<score>' or worse` (ordering `pass` < `warn` < `block`)
3. **Universal over priority:** `every <priority> dimension scores '<score>'`
4. **Single-dimension literal:** `<Dn> scores '<score>'`
5. **Conjunction:** any of the above joined by `AND`

Shipped template coverage:
- `reviewer/full.json`: F1 pattern 1 (bare mandatory), F2 pattern 2, F3 pattern 1 (`high-priority` variant), F0 pattern 3.
- `reviewer/methodology_focus.json`: F1 / F2 / F0 pattern 4 (literal D1).

New expression forms require a PR updating both this §9 and the synthesizer prompt's recognised-pattern list.

## 10. Token cost expectations

Reviewer total calls = `2 × panel_size`. For `reviewer_full` that is 5 → 10 calls; for `reviewer_methodology_focus` 2 → 4. Phase 1 input is small (contract + metadata only); Phase 1 output is short (paraphrase + scoring_plan). Real token bound is well below 2x raw increase.

## 11. Failure modes and diagnostics

Audit-log tags the orchestrator may emit:

| Tag | When | Action |
|-----|------|--------|
| `[CONTRACT-ACKNOWLEDGED]` | normal Phase 1 completion | none (expected) |
| `[PROTOCOL-VIOLATION: phase1_lint_failed=true]` | Phase 1 lint fails twice for a reviewer | mark reviewer unusable |
| `[PROTOCOL-VIOLATION: phase2_lint_failed=<check>]` | Phase 2 lint fails (non multi-dissent) | mark reviewer unusable |
| `[PROTOCOL-VIOLATION: multi_dissent=true]` | Phase 2 has ≥ 2 dissent entries, retry exhausted | mark reviewer unusable |
| `[PANEL-SHRUNK: usable=<k>, panel_size=<N>]` | §6 invariant failed | abort editorial round |
| `[EXPRESSION-UNRECOGNISED: condition_id=<F>, expression=<...>]` | synthesizer step 2.1 | abort synthesizer |
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-reviewer-references-statistical-reporting-standards-md"></a>

## SOURCE: skills/academic-paper-reviewer/references/statistical_reporting_standards.md

<!-- SOURCE-CONTENT-BEGIN bytes=22703 -->
# Statistical Reporting Standards — Statistical Reporting Standards & APA 7.0 Format Quick Reference

This document defines the complete review standards for statistical reporting in quantitative research. `methodology_reviewer_agent` uses this document as the primary reference in Step 4a (Statistical Reporting Adequacy).

---

## 1. Universal Statistical Reporting Checklist

All quantitative research papers **must** report the following items. Check each item during review:

### 1.1 Descriptive Statistics

| Item | Standard | Common Omission |
|------|----------|----------------|
| Mean (*M*) | Must be reported for all continuous variables | Only overall reported, not by group |
| Standard deviation (*SD*) | Must appear paired with the mean | Standard error (*SE*) used incorrectly in place of SD |
| Sample size (*N* / *n*) | Both total and group sample sizes must be reported | Sample attrition during analysis unexplained |
| Range | Report Min-Max or interquartile range | Completely absent, unable to judge distribution characteristics |
| Categorical variable distribution | Report frequency (*f*) and percentage (%) | Only percentage reported, missing raw frequency |

### 1.2 Effect Size

| Item | Standard | Common Omission |
|------|----------|----------------|
| Reporting obligation | **All statistical tests must be accompanied by effect sizes** — APA 7.0 mandatory requirement | Only *p*-value reported, no effect size |
| Select appropriate metric | Choose effect size metric corresponding to the analysis method (see Section 2) | Inappropriate effect size metric used |
| Interpretation | Must provide Cohen's conventional benchmarks or field-specific benchmarks | Numbers reported but magnitude not interpreted |

**Common Effect Size Metrics Quick Reference:**

| Analysis Method | Effect Size Metric | Small/Medium/Large (Cohen's Convention) |
|----------------|-------------------|----------------------------------------|
| *t*-test | Cohen's *d* | 0.2 / 0.5 / 0.8 |
| ANOVA | *eta*-squared | .01 / .06 / .14 |
| ANOVA (partial) | partial *eta*-squared | .01 / .06 / .14 |
| Correlation | *r* | .10 / .30 / .50 |
| Regression | *R*-squared, *f*-squared | *f*-squared: .02 / .15 / .35 |
| Chi-square | Cramer's *V*, *phi* | *V*: .10 / .30 / .50 (*df*=1) |
| Odds Ratio | OR | 1.5 / 2.5 / 4.3 (Rosenthal) |

### 1.3 Confidence Intervals

| Item | Standard | Common Omission |
|------|----------|----------------|
| CI reporting | All effect sizes and key estimates **should** report 95% CI | CI completely absent |
| Format | 95% CI [lower bound, upper bound] | Inconsistent format or using parentheses instead of brackets |
| Interpretation | Describe the substantive meaning of the CI, not just statistical meaning | Only checking whether CI includes zero, not interpreting width |

### 1.4 Statistical Significance

| Item | Standard | Common Omission |
|------|----------|----------------|
| *p*-value format | Report exact *p* value (e.g., *p* = .032) | Only reporting *p* < .05 or *p* > .05 |
| *p* < .001 | Can report *p* < .001 when *p* is very small | Reporting *p* = .000 (raw statistical software output) |
| Alpha level | Declare alpha level a priori | Failure to state whether alpha = .05 or another value |
| Multiple comparisons | Use Bonferroni, Holm, FDR correction | Multiple comparisons without any correction |
| Non-significant results | Must be fully reported; cannot be hidden | Selectively reporting only significant results |

### 1.5 Statistical Power

| Item | Standard | Common Omission |
|------|----------|----------------|
| A priori power analysis | State target power (typically >= .80), assumed effect size, alpha, required sample size | Power analysis completely absent |
| Effect size source | Based on prior research, pilot study, or theoretical expectation | Using Cohen's convention without explanation |
| Tool | Use G*Power, pwr package, etc. | Tool not specified |
| Post-hoc power | Report observed power for non-significant results | Type II error risk not discussed for non-significant results |
| Sensitivity analysis | Report the minimum detectable effect size given *N* | Sensitivity analysis not conducted |

### 1.6 Missing Data Handling

| Item | Standard | Common Omission |
|------|----------|----------------|
| Missing data reporting | Report missing data amount and proportion for each variable | Missing data situation not reported |
| Missing mechanism | Discuss MCAR / MAR / MNAR | MCAR assumed without testing |
| Handling method | State the method used: listwise deletion / pairwise deletion / MI / FIML | Not stated or only using listwise deletion |
| Sensitivity analysis | Compare result robustness across different missing data handling methods | Only one method used, sensitivity not tested |

### 1.7 Assumption Testing

| Assumption | Applicable Analysis | Testing Method | Common Omission |
|-----------|-------------------|---------------|----------------|
| Normality | *t*-test, ANOVA, regression | Shapiro-Wilk / K-S / Q-Q plot / skewness & kurtosis | Completely untested or only invoking CLT |
| Homogeneity of variance | Independent *t*-test, ANOVA | Levene's test | Not reported or alternative method not used when violated |
| Linearity | Regression, correlation | Residual plot / scatter plot | Linearity assumed without testing |
| Independence | Most parametric tests | Durbin-Watson / research design explanation | Nested data not handled |
| Multicollinearity | Multiple regression | VIF, tolerance, correlation matrix | VIF not reported or reported but not addressed |
| Residual normality / homoscedasticity | Regression | Residual plot, Breusch-Pagan | Residuals not checked after model fitting |

---

## 2. Method-Specific Checklists

### 2.1 *t*-test (Independent / Paired Samples)

| Check Item | Description |
|-----------|-------------|
| Report *t* statistic | *t*(df) = X.XX, *p* = .XXX |
| Independent vs paired | Correct selection? Paired designs need to report pairing logic |
| Effect size | Cohen's *d* (independent) or *d*_z (paired) |
| Assumption testing | Normality (important for small samples), homogeneity of variance (independent *t*-test) |
| Welch's *t*-test | Is Welch correction used when variances are unequal? |
| Directionality | Is one-tailed vs two-tailed supported by a priori theoretical basis? |

### 2.2 ANOVA (One-Way / Factorial / Repeated Measures)

| Check Item | Description |
|-----------|-------------|
| Report *F* statistic | *F*(df1, df2) = X.XX, *p* = .XXX |
| Effect size | *eta*-squared, partial *eta*-squared, or *omega*-squared |
| Post-hoc comparisons | When main effect is significant, are post-hoc tests done (Tukey / Bonferroni / Games-Howell)? |
| Interaction effects | In factorial designs, are interactions interpreted? Are simple effects tested? |
| Sphericity assumption | For repeated measures, is Mauchly's test reported + Greenhouse-Geisser / Huynh-Feldt correction? |
| Assumption testing | Normality, homogeneity of variance (Levene's), independence of between-group observations |
| Unequal group sizes | When group sizes differ substantially, is Type III SS used? |

### 2.3 Regression Analysis (Linear / Logistic)

#### Linear Regression

| Check Item | Description |
|-----------|-------------|
| Model summary | *R*-squared, adjusted *R*-squared, *F* test for model |
| Coefficient table | *B*, *SE*, *beta*, *t*, *p*, 95% CI for *B* |
| Multicollinearity | VIF (< 5 or < 10 depending on field convention), tolerance |
| Residual diagnostics | Normality, homoscedasticity, linearity, outliers (Cook's *D*) |
| Variable selection | Rationale for enter vs stepwise method |
| Effect size | *R*-squared, *f*-squared, Cohen's *f*-squared |

#### Logistic Regression

| Check Item | Description |
|-----------|-------------|
| Model fit | Hosmer-Lemeshow / chi-squared / -2LL / Nagelkerke *R*-squared |
| Coefficient reporting | *B*, *SE*, Wald, OR, 95% CI for OR |
| Classification accuracy | Classification table, sensitivity, specificity, AUC/ROC |
| Assumptions | Independence of observations, linearity in the logit (linear relationship between continuous predictors and logit) |
| Sample size | At least 10-20 events per predictor variable (EPV rule) |

### 2.4 Structural Equation Modeling (SEM)

| Check Item | Standard |
|-----------|----------|
| Sample size | Typically >= 200; or 5-10 times the number of estimated parameters |
| Model fit indices | **Must report multiple indices simultaneously** (at least 4) |
| CFI / TLI | >= .95 (good); >= .90 (acceptable) |
| RMSEA | <= .06 (good); <= .08 (acceptable); must report 90% CI |
| SRMR | <= .08 |
| chi-squared/df | <= 3 (some scholars suggest <= 2) |
| Factor loadings | Standardized >= .50 (ideal >= .70) |
| Measurement model | CFA before SEM (two-step approach) — Anderson & Gerbing (1988) |
| Reliability and validity | CR >= .70, AVE >= .50, discriminant validity (Fornell-Larcker / HTMT) |
| Modification indices | When using modification indices, must have theoretical support |
| Normality | Multivariate normality (Mardia's coefficient); when violated, use robust ML or bootstrapping |

### 2.5 Hierarchical Linear Modeling (HLM / MLM)

| Check Item | Standard |
|-----------|----------|
| Nested structure | Clearly explain each level (e.g., students -> classes -> schools) |
| ICC | Report Intraclass Correlation Coefficient; ICC > .05 supports using MLM |
| Random effects | Report random intercept and (if applicable) random slope variances |
| Fixed effects | Report coefficients, *SE*, *t* / *z*, *p*, CI |
| Between-group sample size | Level-2 unit count (typically recommended >= 30) |
| Centering | Explain whether grand-mean centering or group-mean centering is used and why |
| Model comparison | Use deviance (-2LL), AIC, BIC to compare nested models |
| Effect size | Pseudo *R*-squared (e.g., Snijders & Bosker's *R*-squared) |

### 2.6 Chi-Square Test

| Check Item | Description |
|-----------|-------------|
| Reporting format | chi-squared(df, *N* = XX) = X.XX, *p* = .XXX |
| Effect size | Cramer's *V* (larger than 2x2) or *phi* (2x2) |
| Expected frequencies | All cells expected frequency >= 5; if any cell < 5, use Fisher's exact test |
| Independence | Are observations truly independent? (Repeated measures are not suitable for ordinary chi-square) |
| Residual analysis | When significant, check standardized residuals to determine which cells contribute to significance |

### 2.7 Non-Parametric Tests

| Check Item | Description |
|-----------|-------------|
| Justification for use | Clearly explain why parametric tests are not used (e.g., normality violation, ordinal scale) |
| Method selection | Mann-Whitney *U* / Wilcoxon / Kruskal-Wallis / Friedman — is the correct test matched |
| Effect size | *r* = *Z* / sqrt(*N*) (Mann-Whitney); *W* (Kendall's) |
| Reporting format | Report test statistic, *p*-value, effect size |
| Post-hoc comparisons | After significant Kruskal-Wallis, pairwise comparisons + correction needed |

---

## 3. APA 7th Edition Statistical Format Quick Reference

### 3.1 Number Formatting

| Rule | Correct | Incorrect |
|------|---------|-----------|
| *p*-value no leading zero | *p* = .032 | *p* = 0.032 |
| Statistics that can exceed 1.0 have leading zero | *M* = 0.75 | *M* = .75 |
| Statistics that cannot exceed 1.0 have no leading zero | *r* = .45 | *r* = 0.45 |
| Generally 2 decimal places | *M* = 3.45 | *M* = 3.4 |
| *p*-value 2-3 decimal places | *p* = .03 or *p* = .032 | *p* = .0321 |
| Percentages 0-1 decimal places | 45.2% | 45.2381% |

**Statistics that cannot exceed 1.0** (no leading zero): correlation coefficients (*r*, *R*), proportions (*p*-value), Cramer's *V*, *phi*, *eta*-squared, *R*-squared, *beta* (standardized regression coefficient)

**Statistics that can exceed 1.0** (leading zero): *M*, *SD*, *B* (unstandardized regression coefficient), Cohen's *d*, *t*, *F*, chi-squared

### 3.2 Statistical Symbol Italicization Rules

| Italic | Non-italic |
|--------|-----------|
| *M*, *SD*, *SE* | df |
| *N* (total sample), *n* (subsample) | SS, MS |
| *t*, *F*, *p*, *r*, *R*, *z* | OR, CI, VIF |
| *d*, *f*-squared, *eta*-squared, *omega*-squared | AIC, BIC, CFI, TLI |
| *B*, *beta* | RMSEA, SRMR |
| *chi*-squared | ICC |
| *U*, *W* (non-parametric statistics) | ANOVA, SEM, HLM |

### 3.3 Statistical Results Reporting Format Examples

| Analysis Method | APA Format Example |
|----------------|-------------------|
| Independent samples *t*-test | *t*(58) = 2.45, *p* = .017, *d* = 0.63, 95% CI [0.12, 1.14] |
| Paired samples *t*-test | *t*(29) = -3.12, *p* = .004, *d*_z = 0.57 |
| One-way ANOVA | *F*(2, 87) = 4.56, *p* = .013, partial *eta*-squared = .09 |
| Linear regression | *B* = 0.34, *SE* = 0.12, *beta* = .28, *t*(95) = 2.83, *p* = .006, 95% CI [0.10, 0.58] |
| Logistic regression | *B* = 1.24, *SE* = 0.45, Wald = 7.59, *p* = .006, OR = 3.46, 95% CI [1.43, 8.37] |
| Chi-square | chi-squared(2, *N* = 150) = 8.34, *p* = .015, *V* = .24 |
| Mann-Whitney | *U* = 245.00, *z* = -2.31, *p* = .021, *r* = .29 |
| SEM fit | chi-squared(52) = 78.34, *p* = .011, CFI = .97, TLI = .96, RMSEA = .045 [.018, .068], SRMR = .038 |
| HLM fixed effects | *gamma*_10 = 0.45, *SE* = 0.15, *t*(28) = 3.00, *p* = .006 |

### 3.4 Table Format Standards

| Rule | Description |
|------|-------------|
| Three-line table | APA tables have only three horizontal lines (above header, below header, bottom of table), no vertical lines |
| Table numbering | Table 1, Table 2... (bold), title on the line below the number (italic) |
| Note levels | General note (Note.) -> Specific note (superscript a, b) -> Significance (*p* < .05, **p* < .01) |
| Asterisks | \**p* < .05. \*\**p* < .01. \*\*\**p* < .001. |
| Alignment | Numbers right-aligned, decimal points aligned |

---

## 4. Statistical Red Flags

The following patterns during review should raise red flags, requiring further investigation or author clarification:

### 4.1 P-hacking Indicators

| Red Flag | Description | Severity |
|----------|-------------|----------|
| Many *p* near .05 | Multiple results with *p* concentrated in the .04-.05 range | HIGH |
| Selective reporting | Only significant results reported, non-significant ones disappeared | HIGH |
| Vague analysis strategy | Analysis strategy not stated a priori, appears exploratory in hindsight | MEDIUM |
| Unexpected subgroups | Post-hoc subgroup decomposition to find significant results | MEDIUM |
| Flexible sample size | No pre-defined stopping rule (sequential testing without correction) | HIGH |
| "Excluding outliers" | Large number of outliers excluded with unclear criteria | MEDIUM |

### 4.2 HARKing (Hypothesizing After Results are Known)

| Red Flag | Description | Severity |
|----------|-------------|----------|
| Perfect hypothesis-result match | All hypotheses supported without exception | MEDIUM |
| Exploratory analysis packaged as confirmatory | Literature review clearly constructed post-hoc | HIGH |
| Hypothesis directionality change | Originally predicted positive but result was negative, yet claimed "as expected" | HIGH |
| No pre-registration | No OSF / AsPredicted pre-registration link provided (not mandatory but recommended) | LOW |

### 4.3 Missing Effect Sizes and Confidence Intervals

| Red Flag | Description | Severity |
|----------|-------------|----------|
| No effect sizes reported at all | Conclusions based solely on *p*-values | HIGH |
| CI completely absent | Cannot judge estimation precision | MEDIUM |
| Extremely wide CI | CI spans from small to large effect sizes, imprecise estimation | MEDIUM |
| Inconsistent effect sizes | Reported effect sizes inconsistent with calculations from raw data | HIGH |

### 4.4 Sample Size Issues

| Red Flag | Description | Severity |
|----------|-------------|----------|
| No power analysis | Sample size lacks a priori calculation basis | MEDIUM |
| Sample too small | In regression analysis, *N* < 10 x number of predictors | HIGH |
| Unexplained sample attrition | Large gap between starting *N* and final *N* without explanation | MEDIUM |
| SEM small sample | *N* < 200 without small sample correction | MEDIUM |
| HLM Level-2 insufficient | Level-2 units < 30 | MEDIUM |

### 4.5 Uncorrected Multiple Comparisons

| Red Flag | Description | Severity |
|----------|-------------|----------|
| Multiple *t*-tests instead of ANOVA | 3+ group comparisons using multiple *t*-tests | HIGH |
| No post-hoc after ANOVA | Main effect significant but claiming group differences without post-hoc tests | MEDIUM |
| Multiple DVs uncorrected | Multiple dependent variables tested separately on the same dataset without Bonferroni or FDR | MEDIUM |
| Multiple model comparisons | Trying multiple models but only reporting "the best one" | HIGH |

### 4.6 Assumption Violation

| Red Flag | Description | Severity |
|----------|-------------|----------|
| Assumption testing completely absent | Skipping normality/homogeneity/linearity tests | MEDIUM |
| Violations not addressed | Violations reported but original analysis still used | HIGH |
| CLT as excuse | "Because *N* > 30, normality can be ignored" without actual testing | LOW |
| Excessive VIF | VIF > 10 but no action taken | HIGH |

### 4.7 Other Red Flags

| Red Flag | Description | Severity |
|----------|-------------|----------|
| *p* = .000 | Raw statistical software output, should be *p* < .001 | LOW |
| df inconsistent with *N* | *N* derived from degrees of freedom doesn't match reported *N* | HIGH |
| Inconsistent table numbers | Text narrative contradicts table values | HIGH |
| Statistical software not stated | Not reporting SPSS / R / Stata / Mplus and version | LOW |
| Causal language | Non-experimental designs (correlational/survey) using causal inference language | MEDIUM |

---

## 5. Common Statistical Methods in Higher Education Research

Higher education research papers frequently involve the following topics and corresponding analysis methods. This table can be referenced during review to judge whether method selection is appropriate.

### 5.1 Recommended Methods by Research Question Type

| Research Question Type | Recommended Method | Description |
|-----------------------|-------------------|-------------|
| Two-group comparison (e.g., experimental vs control) | Independent samples *t*-test / Mann-Whitney | Depending on data normality |
| Multi-group comparison (e.g., different institution types) | ANOVA / Kruskal-Wallis | Mean comparison for 3+ groups |
| Pre-post comparison | Paired *t*-test / Wilcoxon | Change within the same group |
| Predictive analysis (continuous DV) | Multiple regression | Multiple predictors' effects on continuous outcome |
| Predictive analysis (binary DV) | Logistic regression | E.g., graduation/dropout, pass/fail |
| Nested data (students -> schools) | HLM / MLM | Higher education data naturally has nested structure |
| Latent constructs and path analysis | SEM / CFA | Measuring unobservable constructs (e.g., teaching quality) |
| Scale reliability and validity | EFA -> CFA | Scale development or validation |
| Categorical variable association | Chi-square / Fisher's exact | Cross-tabulation analysis |
| Longitudinal data | Growth curve models / Latent growth models | Tracking student trajectories over multiple years |
| Large-scale datasets | Weighted analysis / sampling design correction | Accounting for sampling design when using national survey data |

### 5.2 Special Considerations for Higher Education Research

| Consideration | Description |
|--------------|-------------|
| **Nested structure** | Higher education data almost always has nesting (students -> departments -> institutions); ignoring it underestimates standard errors and inflates Type I error |
| **Sampling design** | When using national databases (e.g., MOE statistics, public higher education data), must account for sampling weights and clustering |
| **Selection bias** | Students self-select into departments/institutions, not randomly assigned; consider propensity score matching or Heckman correction |
| **Ceiling effects** | Satisfaction surveys often show extreme skewness; need to check and consider Tobit model or non-parametric methods |
| **Small population** | Taiwan has a limited number of universities (~150); census surveys are not appropriate for inferential statistics (census, not sample) |
| **Time series** | Analyzing multi-year enrollment trends requires considering autocorrelation |
| **Multiple roles** | Same faculty completing multiple surveys (e.g., teaching evaluations) -> observations not independent |

---

## 6. Statistical Reporting Completeness Scoring Standards

`methodology_reviewer_agent` uses the following standards to assess statistical reporting completeness:

### Scoring Dimensions and Weights

| Dimension | Weight | Full Score Criteria |
|-----------|--------|-------------------|
| A. Descriptive statistics completeness | 15% | M, SD, N, Range all present |
| B. Effect size reporting | 20% | All tests accompanied by effect sizes |
| C. Confidence interval reporting | 15% | Key estimates include CI |
| D. Assumption testing reporting | 15% | All statistical assumptions tested |
| E. Statistical power | 10% | Complete a priori power analysis |
| F. Missing data handling | 10% | Missing data amounts + handling method reported |
| G. APA format correctness | 10% | Symbols, decimals, tables compliant |
| H. No red flag indicators | 5% | No red flags from Section 4 detected |

### Scoring Levels

| Level | Score | Description |
|-------|-------|-------------|
| Exemplary | 90-100 | Statistical reporting is exemplary, all items complete and correctly formatted |
| Adequate | 70-89 | Major items complete, minor omissions that don't affect conclusion credibility |
| Needs Improvement | 50-69 | Significant omissions (e.g., missing effect sizes or assumption testing), supplementation needed |
| Inadequate | 30-49 | Multiple items missing, statistical reporting insufficient to support conclusions |
| Unacceptable | 0-29 | Severely insufficient statistical reporting, major rewrite needed |

---

## 7. Quick Reference: Recommended Review Sequence

Methodology reviewer should follow this sequence when reviewing statistical reporting:

```
Step 1: Confirm research question -> analysis method correspondence is reasonable (Section 5)
Step 2: Check whether assumption testing is reported (Section 1.7)
Step 3: Check universal checklist item by item (Sections 1.1-1.6)
Step 4: Consult method-specific checklist (Section 2)
Step 5: Scan red flag list (Section 4)
Step 6: Verify APA formatting (Section 3)
Step 7: Produce completeness score (Section 6)
```
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-paper-reviewer-references-top-journals-by-field-md"></a>

## SOURCE: skills/academic-paper-reviewer/references/top_journals_by_field.md

<!-- SOURCE-CONTENT-BEGIN bytes=12874 -->
# Top Journals by Field — Key Academic Discipline Journal Directory

This document is used by `field_analyst_agent` and `eic_agent` as a reference for calibrating EIC identity and assessing journal fit.

---

## 1. Education

### Higher Education
| Journal | Publisher | Impact Factor Range | Typical Review Preferences |
|---------|----------|-------------------|---------------------------|
| *Studies in Higher Education* | Taylor & Francis | 5-7 | Emphasizes theoretical depth, international comparison, policy implications |
| *Higher Education* | Springer | 4-6 | Accepts diverse methodologies, values contextual description |
| *Research in Higher Education* | Springer | 3-5 | Prefers quantitative research, large datasets |
| *Journal of Higher Education* | Taylor & Francis | 3-5 | Primarily U.S. context, values empirical research |
| *Quality in Higher Education* | Taylor & Francis | 2-4 | Quality assurance topics, HEEACT/ENQA related |
| *Assessment & Evaluation in Higher Education* | Taylor & Francis | 4-6 | Assessment and evaluation topics |
| *Higher Education Research & Development* | Taylor & Francis | 3-5 | Teaching and learning research |
| *European Journal of Higher Education* | Taylor & Francis | 2-3 | European perspective, Bologna Process |

### General Education
| Journal | Publisher | Impact Factor Range | Typical Review Preferences |
|---------|----------|-------------------|---------------------------|
| *Review of Educational Research* | SAGE | 10-12 | Accepts only review articles, highest standards |
| *Educational Researcher* | SAGE | 6-9 | Interdisciplinary education research, policy-relevant |
| *American Educational Research Journal* | SAGE | 5-7 | Diverse methodologies, U.S. context |
| *British Educational Research Journal* | Wiley | 3-5 | U.K. context, critical perspectives |
| *Comparative Education Review* | U Chicago Press | 2-4 | Comparative education, cross-national research |

### Educational Technology
| Journal | Publisher | Impact Factor Range | Typical Review Preferences |
|---------|----------|-------------------|---------------------------|
| *Computers & Education* | Elsevier | 10-13 | Primarily empirical research, large samples |
| *The Internet and Higher Education* | Elsevier | 7-10 | Online learning, blended instruction |
| *British Journal of Educational Technology* | Wiley | 5-7 | Balances theory and practice |
| *Educational Technology Research & Development* | Springer | 4-6 | Instructional design, learning sciences |

---

## 2. Computer Science / AI

| Journal | Publisher | Impact Factor Range | Typical Review Preferences |
|---------|----------|-------------------|---------------------------|
| *Nature Machine Intelligence* | Springer Nature | 20-25 | High-impact AI research, interdisciplinary |
| *Artificial Intelligence* | Elsevier | 8-12 | Foundational AI theory and methods |
| *Journal of Machine Learning Research* | JMLR | 4-7 | Machine learning theory and algorithms |
| *IEEE Transactions on Pattern Analysis and Machine Intelligence* | IEEE | 20-25 | Computer vision, pattern recognition |
| *ACM Computing Surveys* | ACM | 15-18 | High-quality survey articles |
| *Computers in Human Behavior* | Elsevier | 8-10 | Human-computer interaction, user behavior |

---

## 3. Business & Management

| Journal | Publisher | Impact Factor Range | Typical Review Preferences |
|---------|----------|-------------------|---------------------------|
| *Academy of Management Review* | AOM | 10-13 | Pure theory, conceptual innovation |
| *Academy of Management Journal* | AOM | 9-11 | Empirical research, large samples |
| *Strategic Management Journal* | Wiley | 8-10 | Strategic management, competitive advantage |
| *Administrative Science Quarterly* | SAGE | 9-12 | Organizational theory, boutique papers |
| *Journal of Management* | SAGE | 10-13 | General management journal |
| *Organization Science* | INFORMS | 5-7 | Organizational behavior, decision science |
| *Management Science* | INFORMS | 5-7 | Quantitative management, decision models |

---

## 4. Social Sciences

### Sociology
| Journal | Publisher | Impact Factor Range | Typical Review Preferences |
|---------|----------|-------------------|---------------------------|
| *American Sociological Review* | SAGE | 6-8 | Top U.S. sociology journal |
| *American Journal of Sociology* | U Chicago Press | 4-6 | Balances theory and empirical work |
| *Annual Review of Sociology* | Annual Reviews | 7-10 | High-quality reviews |
| *British Journal of Sociology* | Wiley | 3-5 | Critical theory, European perspectives |

### Political Science / Public Policy
| Journal | Publisher | Impact Factor Range | Typical Review Preferences |
|---------|----------|-------------------|---------------------------|
| *American Political Science Review* | Cambridge | 5-7 | Top political science journal |
| *Journal of Policy Analysis and Management* | Wiley | 3-5 | Policy analysis, causal inference |
| *Public Administration Review* | Wiley | 5-8 | Public administration, governance |
| *Policy Sciences* | Springer | 3-5 | Policy process theory |
| *Journal of Public Policy* | Cambridge | 3-5 | Comparative public policy |

### Psychology
| Journal | Publisher | Impact Factor Range | Typical Review Preferences |
|---------|----------|-------------------|---------------------------|
| *Psychological Bulletin* | APA | 18-22 | High-quality meta-analyses |
| *American Psychologist* | APA | 14-17 | Interdisciplinary psychology |
| *Journal of Applied Psychology* | APA | 6-8 | Applied psychology research |
| *Educational Psychology Review* | Springer | 8-11 | Educational psychology reviews |

---

## 5. Engineering

| Journal | Publisher | Impact Factor Range | Typical Review Preferences |
|---------|----------|-------------------|---------------------------|
| *Nature Engineering* | Springer Nature | — | Interdisciplinary engineering breakthroughs |
| *Journal of Engineering Education* | ASEE/Wiley | 3-5 | Engineering education research |
| *IEEE Transactions* (various branches) | IEEE | 5-15 | Technical contributions, experimental validation |
| *International Journal of Engineering Education* | TEMPUS | 1-3 | International engineering education journal |
| *European Journal of Engineering Education* | Taylor & Francis | 2-4 | European engineering education |

---

## 6. Medicine & Health Sciences

| Journal | Publisher | Impact Factor Range | Typical Review Preferences |
|---------|----------|-------------------|---------------------------|
| *The Lancet* | Elsevier | 90-170 | Highest standards, global health |
| *BMJ (British Medical Journal)* | BMJ | 90-100 | Clinical research, public health policy |
| *Medical Education* | Wiley | 5-7 | Medical education research |
| *Academic Medicine* | AAMC | 6-8 | Medical education, academic medicine |
| *BMC Medical Education* | Springer | 3-4 | Open access, medical education |
| *Advances in Health Sciences Education* | Springer | 3-5 | Health sciences education theory |

---

## 7. Information Systems (Senior Scholars' Basket of 11)

| Journal | Publisher | Impact Factor Range | Typical Review Preferences |
|---------|----------|-------------------|---------------------------|
| *MIS Quarterly* | MIS Quarterly | 7-9 | Theory-driven empirical research, design science; rigorous quantitative and qualitative methods |
| *Information Systems Research* | INFORMS | 5-7 | Analytical, behavioral, and design science; strong methodological standards |
| *Journal of Management Information Systems* | Taylor & Francis | 5-7 | Management-oriented IS research, theory and practice |
| *Journal of the Association for Information Systems* | AIS | 4-6 | Broad IS topics, AIS flagship journal |
| *European Journal of Information Systems* | Taylor & Francis | 8-10 | European and international IS perspectives, pluralist methodologies |
| *Information Systems Journal* | Wiley | 6-8 | Qualitative and interpretive IS research, socio-technical perspectives |
| *Journal of Information Technology* | SAGE | 7-10 | IT strategy, policy, and organizational impact |
| *Journal of Strategic Information Systems* | Elsevier | 8-11 | Strategic role of IS, digital transformation, organizational change |
| *Decision Support Systems* | Elsevier | 6-8 | Analytics, decision-making, DSS design and evaluation |
| *Information & Management* | Elsevier | 8-11 | IS management, technology adoption, organizational impact |
| *Information and Organization* | Elsevier | 5-7 | Socio-material perspectives, qualitative and interpretive research |

---

## 8. Interdisciplinary

| Journal | Publisher | Impact Factor Range | Typical Review Preferences |
|---------|----------|-------------------|---------------------------|
| *Nature* | Springer Nature | 50-70 | All natural sciences, highest standards |
| *Science* | AAAS | 45-65 | All natural sciences, breakthrough discoveries |
| *Proceedings of the National Academy of Sciences* | NAS | 10-12 | Interdisciplinary scientific research |
| *PLOS ONE* | PLOS | 3-4 | Open access, methodological rigor as primary criterion |
| *Science Advances* | AAAS | 13-15 | Interdisciplinary science, open access |
| *Sustainability* | MDPI | 3-4 | Cross-disciplinary sustainability |

---

## Usage Guide

### Logic for Selecting Journals for EIC

1. **Match the discipline first**: Find the corresponding journal list from the paper's primary discipline
2. **Then match quality**: Select an appropriate tier of journal based on the paper's quality
3. **Consider context**: Taiwan or Asian research may be better suited to journals with regional focus
4. **Consider methodology**: Quantitative research may be better suited to certain journals, qualitative research to others

### Notes

- Impact Factor is for reference only; baseline values differ across fields
- Emerging fields may lack high-IF journals, but that does not mean the research is unimportant
- Open access journals should not be assumed to be lower quality by default
- This list cannot be exhaustive; `field_analyst_agent` can recommend more precisely matched journals based on the specific paper topic

---

## 9. Asian & Regional Journals

### Taiwan (TSSCI-Indexed)

| Journal | Field | ISSN | Notes |
|---------|-------|------|-------|
| 教育研究集刊 (Bulletin of Educational Research) | Education | 1028-8708 | NTNU; top Taiwan education journal |
| 高等教育 (Higher Education) | Higher Education | 1813-3282 | Taiwan HE policy and practice |
| 課程與教學季刊 (Curriculum & Instruction Quarterly) | Curriculum Studies | 1560-1277 | Curriculum design and pedagogy |
| 教育科學研究期刊 (Journal of Research in Education Sciences) | Education Sciences | 2073-753X | Broad education research scope |
| 當代教育研究季刊 (Contemporary Educational Research Quarterly) | Education | 1814-4810 | NTNU; contemporary education issues |
| 教育政策論壇 (Educational Policy Forum) | Education Policy | 1560-3601 | NCNU; policy analysis |
| 教育心理學報 (Bulletin of Educational Psychology) | Educational Psychology | 1011-5714 | NTNU; psychological perspectives in education |
| 測驗學刊 (Psychological Testing) | Psychometrics | 1609-4905 | Assessment and measurement |

### Asia-Pacific

| Journal | Field | Publisher | Impact |
|---------|-------|-----------|--------|
| Asia Pacific Education Review | Education | Springer | Q2 in Education; strong Asia focus |
| Higher Education Policy | Higher Education | Springer/IAU | Q1-Q2; international HE policy |
| Journal of Asian Public Policy | Public Policy | Taylor & Francis | Asian policy contexts |
| Asia Pacific Journal of Education | Education | Taylor & Francis | Q2; pan-Asian education research |
| International Journal of Educational Development | Development Education | Elsevier | Q1; includes Asia extensively |
| Compare: A Journal of Comparative and International Education | Comparative Ed | Taylor & Francis | Q1; strong Asian coverage |
| Asian Journal of Social Science | Social Sciences | Brill | Multidisciplinary Asian studies |

### Open Access Options (by Field)

| Field | OA Journal | Publisher | APC (USD) | Notes |
|-------|-----------|-----------|-----------|-------|
| Education | Frontiers in Education | Frontiers | ~$1,350 | Q2; fast review; broad scope |
| Multidisciplinary | PLOS ONE | PLOS | ~$1,931 | Q1; accepts all fields; rigorous methodology focus |
| Higher Education | Education Sciences | MDPI | ~$1,800 | Q2; HE section available |
| Educational Technology | International Journal of Educational Technology in Higher Education | Springer | Free (funded) | Q1; excellent for ed-tech research |
| Social Sciences | Social Sciences | MDPI | ~$1,600 | Q2; broad social science scope |
| Asian Studies | Asian Education and Development Studies | Emerald | ~$3,350 | Q2; specifically Asian education development |
<!-- SOURCE-CONTENT-END -->
