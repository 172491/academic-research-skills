<a id="source-skills-academic-pipeline-references-ai-research-failure-modes-md"></a>

## SOURCE: skills/academic-pipeline/references/ai_research_failure_modes.md

<!-- SOURCE-CONTENT-BEGIN bytes=14978 -->
# AI Research Failure Mode Checklist

**Status**: v3.2
**Parent skill**: `academic-pipeline`
**Used at**: Stage 2.5 INTEGRITY (blocking), Stage 4.5 FINAL INTEGRITY (blocking), Stage 6 PROCESS SUMMARY (reporting only)
**Source**: Lu et al. (2026). Towards end-to-end automation of AI research. *Nature* 651, 914-919. doi:10.1038/s41586-026-10265-5 — Limitations section, Figure 2 (examples of failures in The AI Scientist's own accepted paper), Supplementary Information A.2.9 (debugging traces).

---

## Why this checklist exists

Lu et al. built the first autonomous AI research system to pass blind peer review (ICLR 2025 workshop). Their Limitations section enumerates the specific failure modes they observed — and most of them apply equally to human-in-the-loop AI research workflows like ARS.

These failures are dangerous because **they look like competent work**. A paper containing a hallucinated experimental result reads the same as a paper containing a real one. A shortcut-relying result reads the same as a genuine generalization. A methodology section describing experiments that were never actually run reads the same as a faithful account. The existing integrity verification catches citation hallucinations but is weak on the other failure modes.

The checklist exists to make these failures legible: **at Stage 2.5 and Stage 4.5, the integrity reviewer must explicitly rule out each of the 7 modes, or flag which are suspected and block the pipeline until the user acknowledges.**

This also extends the existing 5-type citation hallucination taxonomy (in `academic-paper-reviewer` references) into a broader 7-type AI research hallucination taxonomy. Citation hallucinations become mode 2 below.

---

## The 7 failure modes

### Mode 1: Implementation bug passing AI self-review

**What it is**: The analysis or experiment code has a bug (off-by-one, wrong variable, silent division-by-zero, type coercion, wrong flag) that produces numerically plausible but scientifically wrong results. The AI runs the code, looks at the output, sees nothing "obviously" wrong, and incorporates the result into the paper.

**Lu 2026 example**: Supplementary A.2.9 traces show The AI Scientist repeatedly accepting experimental runs that had silent crashes or numerical instabilities because the top-level metric "looked reasonable". Figure 2 shows an ICLR reviewer catching one such issue in the accepted paper — the paper's main analysis depended on a setup that the code did not actually implement.

**Detection questions at Stage 2.5**:
- For every numerical result in the draft: does the user have a saved log, notebook, or script run that produced this number? If yes, was the exit code 0 and were there zero warnings? If no log is saved, flag.
- Are any effect sizes suspiciously round (exactly 0.5, exactly 2x baseline, exactly zero variance across runs)? Suspiciously round numbers are a common signal of a constant leaking through a broken pipeline.
- Do error bars / confidence intervals actually vary across conditions, or are they suspiciously identical?

**Who catches it**: `methodology_reviewer_agent` at Stage 3 is downstream; the integrity gate at Stage 2.5 should ask the user directly.

---

### Mode 2: Hallucinated citation

**What it is**: A reference that does not exist, is miscited (wrong year, wrong journal, wrong authors), or is attributed a finding it does not contain. This is the mode ARS already covers most thoroughly via the 5-type citation hallucination taxonomy in `academic-paper-reviewer/references/`. It is included here for completeness of the 7-mode taxonomy.

**Lu 2026 example**: The AI Scientist pipeline includes a Semantic Scholar citation check to suppress this mode, acknowledging it as a primary failure class. PaperOrchestra (Song et al., 2026) extended this with a two-phase pipeline: web search discovery + sequential Semantic Scholar API verification (Levenshtein >= 0.70 title matching).

**Detection (v3.3 update)**: Covered by the existing integrity verification, now strengthened with Semantic Scholar API batch verification (Phase A0 in `integrity_verification_agent`). See `deep-research/references/semantic_scholar_api_protocol.md` for the API protocol. The S2 API provides structured, machine-readable verification that catches fabricated DOIs (DOI_MISMATCH pattern) missed by manual WebSearch.

**Who catches it**: `source_verification_agent` (Tier 0 S2 API + Tier 1 DOI + Tier 2 WebSearch) + `integrity_verification_agent` (Phase A0 + A1).

---

### Mode 3: Hallucinated experimental result

**What it is**: A result that does not correspond to any actual experiment run. The AI writes "we observed a 12% improvement" when no run produced a 12% improvement — either it averaged differently than the paper claims, or it reported a number from a crashed run, or it invented the number to match the narrative.

**Lu 2026 example**: Lu et al. specifically flag "hallucinated experimental results" as a Limitation, noting that automated reviewing struggles to detect them because the reviewer has no access to the underlying runs.

**Detection questions at Stage 2.5**:
- For every claim of the form "X% improvement" or "Y% reduction" or "outperforms baseline by Z": does the user have the raw numbers the paper's number was computed from?
- Does the table in the draft match a saved CSV / tensor log / wandb run the user can point to?
- Does the paper's "we ran N seeds" claim match the number of actual run directories the user has?

**Who catches it**: integrity gate at 2.5. This is harder than citation checking because there's no external database to verify against — the verification is against the user's own experiment logs.

---

### Mode 4: Shortcut reliance

**What it is**: The reported result is real but the model achieved it by exploiting a spurious feature rather than learning the intended generalization. A colour-biased MNIST model that gets 99% accuracy by reading the background colour, not the digit shape, is the canonical case.

**Lu 2026 example**: Figure 2b shows this exact case — The AI Scientist proposed a method, tested it on colour-biased MNIST, got high accuracy, and wrote a paper claiming the method "solved" the task. A reviewer caught that the method was exploiting the colour shortcut, not learning the digit shape. The paper was revised.

**Detection questions at Stage 2.5**:
- Is there any controlled ablation that rules out the most obvious shortcut feature? If the paper tests on dataset D, has the author run on a D-variant where the shortcut feature is removed?
- Does the paper's "ablation studies" section actually ablate the claimed mechanism, or does it ablate incidental hyperparameters?
- Is the baseline strong enough that beating it requires the proposed mechanism, not just more compute?

**Who catches it**: `devils_advocate_reviewer_agent` at Stage 3 is the natural home for this check, but it must be flagged at 2.5 so the user knows to prepare the ablation before Stage 3 arrives. Flag-only at 2.5, not block-only.

---

### Mode 5: Implementation bug reframed as novel insight

**What it is**: The pipeline produces an unexpected result that is actually caused by a bug, but the narrative-writing stage reframes the unexpected behaviour as a novel finding. The paper claims "we discovered that X behaves unexpectedly under condition Y" when in reality X behaves the expected way and condition Y is being mis-implemented.

**Lu 2026 example**: Lu et al. identify this as a compound failure mode — it requires Mode 1 (the bug) plus a writing-stage error in which the AI's narrative generator accepts the bug's output as real and builds a story around it. The paper reads *more* interesting than a bug-free version would have.

**Detection questions at Stage 2.5**:
- Does the draft contain any phrase like "surprisingly," "unexpectedly," "counterintuitively," or "contrary to our hypothesis"? For each such claim, can the user point to a literature reference that would have predicted the opposite? If no literature cites the opposite, the "surprise" may not be a surprise — it may be a bug.
- Did the surprising result appear on the first run, or only after many debugging iterations? First-run surprises are high-risk for this mode.
- Has the user attempted to reproduce the surprising result from scratch in a fresh environment?

**Who catches it**: integrity gate at 2.5. This is the most ARS-specific mode — it is the interaction of a bug (Mode 1) with narrative seduction.

---

### Mode 6: Methodology fabrication

**What it is**: The Methods section describes experiments, hyperparameters, datasets, or procedures that were not actually what the pipeline ran. The AI writes a plausible-sounding Methods section based on what a reasonable version of the experiment *would* look like, drifting from what actually happened.

**Lu 2026 example**: Lu et al. note that the writing stage of The AI Scientist sometimes produced Methods text that was disconnected from the actual hyperparameter log. They added a cross-check against the experiment run config to mitigate this.

**Detection questions at Stage 2.5**:
- Does every number in the Methods section (learning rate, batch size, epochs, dataset size, train/val split) appear in the user's actual run config / log?
- Does the Methods section describe any preprocessing step the user cannot point to in their code?
- Does the Methods section use the past tense where the actual pipeline didn't run?

**Who catches it**: integrity gate at 2.5. This requires the user to provide the actual run config as an integrity input, not just the paper text.

---

### Mode 7: Frame-lock at early pipeline stage

**What it is**: A wrong commitment made in early stages (research question framing, methodology choice, hyperparameter direction) that subsequent stages cannot back out of because they are structurally downstream of the commitment. The paper ends up well-executed but is answering the wrong question or using a fundamentally unsuitable method.

**Lu 2026 example**: Figure 3a traces The AI Scientist's agentic tree search and shows that most failed papers failed at Stage 2 (hyperparameter tuning) — the agent committed to a direction early and could not recover. This is the same frame-lock pattern ARS's anti-sycophancy protocol targets for dialogue, but here it applies to pipeline decisions.

**Detection questions at Stage 2.5**:
- If the user could go back to Stage 1 knowing what they know now, would they change the research question or methodology?
- Does the paper's Discussion section contain any phrase like "in hindsight" or "we realized later"? These are frame-lock tells.
- Is the paper's contribution better explained by the chosen framing, or despite it?

**Who catches it**: integrity gate at 2.5. If flagged, user is offered the option to return to Stage 1 or Stage 2 rather than proceeding to Stage 3.

---

## How the checklist runs at each stage

### At Stage 2.5 INTEGRITY (first integrity gate)

Run all 7 modes. For each mode, produce one of three outcomes:

- **CLEAR**: integrity reviewer has evidence that the mode does not apply. Record the evidence briefly.
- **SUSPECTED**: one or more detection questions returned a concerning answer. Must be surfaced to the user.
- **INSUFFICIENT EVIDENCE**: integrity reviewer cannot rule the mode in or out without user input (e.g., needs experiment logs the user hasn't provided).

**Block condition**: pipeline blocks if **any** mode is SUSPECTED, or if Modes 1, 3, 5, or 6 are INSUFFICIENT EVIDENCE (these four require user-provided logs to rule out and should not be silently skipped). Modes 2, 4, 7 INSUFFICIENT EVIDENCE can proceed with a warning and will be re-checked at 4.5.

**User acknowledgement options at block**:
- Confirm the flag — return to Stage 2 WRITE (or earlier) to fix
- Override with reasoning — user explicitly states why the flag is a false positive, reasoning is recorded in the process log for Stage 6
- Revise the specific passage and re-run the check

### At Stage 4.5 FINAL INTEGRITY

Re-run all 7 modes. Additional rule: any mode that was SUSPECTED at 2.5 must be resolved by 4.5 (CLEAR or user-Overridden-with-reasoning). If the same mode is still SUSPECTED at 4.5, the pipeline re-blocks and refuses to proceed to Finalize until the issue is addressed — no amount of revision loops can skip this.

### At Stage 6 PROCESS SUMMARY (AI Self-Reflection Report)

Report only, no blocking. The Self-Reflection Report includes a "Failure Mode Audit Log" section listing, for each of the 7 modes:
- Final status at 4.5 (CLEAR / OVERRIDDEN)
- History: was it ever SUSPECTED during the pipeline? At which stage? How was it resolved?
- If OVERRIDDEN: the user's reasoning

This makes the failure-mode history part of the permanent process record, giving future readers (and the user themselves) visibility into what the AI-human collaboration had to defend against.

---

## Relationship to existing ARS checks

| Existing check | Covers which modes |
|---|---|
| Citation hallucination taxonomy (5-type) | Mode 2 (fully) |
| `source_verification_agent` | Mode 2 (cross-check) |
| Existing Stage 2.5 integrity review | Mode 2, partial Mode 6 |
| `devils_advocate_reviewer_agent` (Stage 3) | Mode 4, partial Mode 7 |
| Anti-sycophancy protocol (v3.0) | Dialogue-level frame-lock, not pipeline-level Mode 7 |

Gap coverage provided by this checklist: **Modes 1, 3, 5, 6, and the pipeline-level aspect of Mode 7**. These are the modes that were not previously systematically checked.

---

## Open questions (for v3.3)

- **False positive rate**: Modes 1, 5, and 6 require the user to supply experiment logs. If the user is writing a purely theoretical paper or a qualitative study, many of these detection questions don't apply. The checklist needs a paper-type pre-filter that turns off inapplicable modes based on the paper type detected by `field_analyst_agent`. v3.2 ships with all modes always-on; v3.3 should add the pre-filter.
- **Override auditing**: if a user overrides a flag, is the reasoning ever reviewed? In v3.2 it goes into the Stage 6 record only. A stronger version would flag overrides for peer review during Stage 3 so that a reviewer can push back on the user's reasoning.

---

## References

- Lu, C. et al. (2026). Towards end-to-end automation of AI research. *Nature* 651, 914-919. [doi:10.1038/s41586-026-10265-5](https://doi.org/10.1038/s41586-026-10265-5) — Limitations section, Figure 2, Supplementary Information A.2.9.
- ARS `academic-paper-reviewer/references/` — existing 5-type citation hallucination taxonomy (Mode 2).
- ARS `academic-pipeline/references/claim_verification_protocol.md` — existing integrity verification that this checklist extends.
- ARS `academic-pipeline/references/integrity_review_protocol.md` — existing integrity review protocol that Stage 2.5 follows.
- ARS `ROADMAP_v3.2.md` — v3.2 integration plan, item 2.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-claim-audit-calibration-protocol-md"></a>

## SOURCE: skills/academic-pipeline/references/claim_audit_calibration_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=12987 -->
# Claim-Faithfulness Audit Calibration Protocol

**Status**: v3.8
**Parent agent**: `claim_ref_alignment_audit_agent`
**Mode name**: `calibration`
**Purpose**: Measure the audit agent's own false-negative rate (FNR) and false-positive rate (FPR) on alignment judgments (SUPPORTED / UNSUPPORTED / AMBIGUOUS / RETRIEVAL_FAILED) AND negative-constraint judgments (VIOLATED / NOT_VIOLATED) against a synthetic gold set, then gate CI on FNR < 0.15 AND FPR < 0.10.

This protocol is modeled on `academic-paper-reviewer/references/calibration_mode_protocol.md`. The reviewer mode measures editorial decision accuracy on whole papers; this mode measures claim-to-source alignment accuracy on per-citation tuples. Both share the same FNR / FPR / threshold-gate vocabulary; the difference is unit of analysis.

---

## Why this mode exists

The audit agent emits HIGH-WARN gate-refuse annotations on UNSUPPORTED rows and VIOLATED constraint matches. Those signals are only useful if the underlying judge is reliably distinguishing supported from unsupported claims. Without measurement, a judge that systematically over-flags AMBIGUOUS cases as UNSUPPORTED looks identical at the row level to a judge that nails the discrimination — but the former produces a flood of false HIGH-WARN refusals that erodes operator trust and eventually gets the agent ignored.

Calibration mode closes the measurability gap. It does NOT try to make the judge perfect; it makes the judge's error profile legible BEFORE the agent ships to a new operator's pipeline.

---

## Inputs

1. **Gold set**: 20 tuples (12 alignment + 8 constraint per the canonical shipped fixture at `scripts/fixtures/claim_audit_calibration/gold_set.json`). Per-tuple shape and the four ingestion-gate rules (alignment-judgment coverage, ≥3 NOT_VIOLATED floor, required constraint fields, tuple_kind validity) are spelled out in **Gold tuple schema** below + spec §7.7 rules (a)-(d). The shipped fixture is the canonical example.

2. **Judge function**: a callable matching the v3.8 judge interface (`claim_text`, `retrieved_excerpt`, `anchor_kind`, `anchor_value`, `active_constraints`, `judge_model` kwargs). The shipped test fixture pairs the gold set with a perfect-judge stub so T-C1 / T-C2 / T-C3 exercise the calibration tooling end-to-end without requiring a live LLM call. Production deployment plugs a real judge_fn in place of the stub.

3. **Thresholds** (optional): `{"FNR": 0.15, "FPR": 0.10}` per spec §7.7 + §9 acceptance. Tightening these is a spec bump; loosening them is not permitted without a corresponding judge-quality-improvement justification recorded in the calibration report's `thresholds` block.

---

## Gold tuple schema

Two discriminated `tuple_kind` shapes, validated at ingestion by `validate_gold_set` (raises `GoldSetValidationError` on the first rule violation).

### Alignment tuple

```jsonc
{
  "tuple_kind": "alignment",
  "claim_text": "<the prose claim under test>",
  "ref_text_excerpt": "<source-passage excerpt the judge will evaluate against; null for RETRIEVAL_FAILED tuples>",
  "anchor": {"kind": "page" | "section" | "quote" | "paragraph" | "none", "value": "<...>"},
  "expected_judgment": "SUPPORTED" | "UNSUPPORTED" | "AMBIGUOUS" | "RETRIEVAL_FAILED"
}
```

Alignment tuples MUST NOT carry any of: `constraint_under_test_id`, `constraint_under_test_rule_text`, `manifest_fixture_path` (rule (b)). Mixing constraint fields onto an alignment tuple corrupts the per-class confusion matrix because the judge call shape differs between the two kinds.

### Constraint tuple

```jsonc
{
  "tuple_kind": "constraint",
  "claim_text": "<the prose claim under test>",
  "ref_text_excerpt": null,
  "anchor": {"kind": "page" | "section" | ..., "value": "<...>"},
  "expected_judgment": "VIOLATED" | "NOT_VIOLATED",
  "constraint_under_test_id": "MNC-N" | "NC-CN-M",
  "constraint_under_test_rule_text": "<inline rule text>",     // EITHER this
  "manifest_fixture_path": "scripts/fixtures/.../mnc.json"     // OR this
}
```

Both rule sources are accepted by `validate_gold_set` because manifest-bound constraints sometimes carry domain-specific rule text that authors want versioned alongside the manifest. **The v3.8.0 calibration runner supports only the inline `constraint_under_test_rule_text` form.** A manifest-only tuple validates clean per rule (c) but `run_calibration` raises `NotImplementedError` at run time rather than reach the judge with an empty rule (R2 codex P1 closure on the silent-skip risk that T-C3 is meant to prevent). The manifest-fixture resolver is a post-v3.8 deliverable; until it ships, author calibration fixtures with inline rule text.

---

## Process

### Phase 0: Intake

1. Call `validate_gold_set(tuples)`. Any of the four spec §7.7 rules (a)/(b)/(c)/(d) failing raises `GoldSetValidationError` with the offending tuple index and the rule name. Do NOT catch the exception — fix the gold set.

### Phase 1: Per-tuple judge invocation

For each tuple, the calibration runner calls `judge_fn(...)` with kwargs matching the v3.8 judge interface:
- Alignment tuples (all four `expected_judgment` values including `RETRIEVAL_FAILED`) → `retrieved_excerpt = tuple.ref_text_excerpt` (may be `null` for `RETRIEVAL_FAILED` tuples), `active_constraints=[]`. The runner does NOT pre-filter `RETRIEVAL_FAILED` tuples — the judge stub is responsible for returning the matching label.
- Constraint tuples → `retrieved_excerpt = tuple.ref_text_excerpt` (typically `null`), `active_constraints=[{"constraint_id": ..., "rule": ..., "scope": "MNC" | "NC"}]`. Scope is derived from `constraint_under_test_id`: `MNC-N` → `"MNC"`, `NC-CN-M` → `"NC"`. Malformed ids are rejected by `_derive_constraint_scope` with a diagnostic naming the expected shape.

No ensembling at this layer. Spec §7.7 does not require N-run majority voting (reviewer mode does, but reviewer-paper unit-of-analysis is heavier and benefits more from variance reduction; per-tuple alignment is a simpler call). Re-running the same tuple is the operator's responsibility if a high-variance judge_model warrants it.

### Phase 2: Confusion-matrix accumulation

The runner accumulates two confusion matrices:

- **Aggregate** (the rates that T-C1 gates against): a tuple contributes a FN when `expected_judgment ≠ actual judgment`. For alignment, every mismatched tuple counts as both FN (for the expected class) and FP (for the wrongly-picked class), so aggregate FNR and FPR are symmetric. For constraint tuples, VIOLATED is the positive class (gate-refuse signal); the matrix is the standard binary form.
- **Per-class one-vs-rest** (the report block that T-C2 checks): for each of `SUPPORTED`, `UNSUPPORTED`, `AMBIGUOUS`, `violated_constraint`, the runner computes FNR / FPR with that class as the positive label. `n_positive` / `n_negative` denominators are surfaced so a "0.0 FNR on n_positive=0" entry is distinguishable from "0.0 FNR on n_positive=8".

The fourth alignment class `RETRIEVAL_FAILED` is intentionally NOT surfaced in `per_class`: the pipeline sets it pre-judge at operational deployment, so judge-quality FNR/FPR against this label is uninformative for tooling validation. To keep the per-tuple call shape uniform, the runner still passes `RETRIEVAL_FAILED` tuples to `judge_fn` (no pre-filter) — the stub or real judge echoes the expected label, and the tuple contributes to aggregate FNR/FPR via the non-`per_class` aggregate path.

### Phase 3: Threshold check

If `report["FNR"] >= thresholds["FNR"]` OR `report["FPR"] >= thresholds["FPR"]`, the test (T-C1) fails. The report's `thresholds` block echoes the active gate values so CI failure messages can distinguish:

- A regression (judge quality degraded — same gold set, higher FNR/FPR than the previous run).
- A spec bump (tighter thresholds — same judge, but T-C1 now demands more).

Both surface as the same CI failure; the report block makes the diagnosis explicit.

### Phase 4: Report shape

```jsonc
{
  "FNR": 0.0,
  "FPR": 0.0,
  "per_class": {
    "SUPPORTED":           {"FNR": 0.0, "FPR": 0.0, "n_positive": 5, "n_negative": 7},
    "UNSUPPORTED":         {"FNR": 0.0, "FPR": 0.0, "n_positive": 3, "n_negative": 9},
    "AMBIGUOUS":           {"FNR": 0.0, "FPR": 0.0, "n_positive": 3, "n_negative": 9},
    "violated_constraint": {"FNR": 0.0, "FPR": 0.0, "n_positive": 5, "n_negative": 3}
  },
  "thresholds": {"FNR": 0.15, "FPR": 0.10},
  "n_total": 20,
  "n_alignment": 12,
  "n_constraint": 8
}
```

The shape is the canonical contract `scripts/test_claim_audit_calibration.py` (T-C1 / T-C2) pins against. Adding fields is non-breaking; removing or renaming is a spec bump.

---

## Failure cases this mode does NOT fix

Calibration reports the judge's error profile on a **specific** gold set in a **specific** domain. It does not:

- Predict performance on tuples outside the gold-set distribution (the canonical fixture is mid-domain synthetic; ML / clinical / qualitative judges should run domain-specific gold sets).
- Detect rubric-discrimination-power problems on the LLM-as-judge side — that's the `#89 / gold fixtures` work tracked separately (per spec §2 out-of-scope).
- Replace the post-calibration ramp-on plan recorded in `academic-pipeline/SKILL.md` mode flags. v3.8.0 ships the audit agent dispatch as opt-in default-OFF; T-C1 passing on the canonical gold set is necessary but not sufficient evidence for default-ON.

If a deploying operator brings a gold set that is itself biased (all tuples from one venue, all post-2024, all heavily-redacted), calibration reports a biased profile. Emit a warning during intake if the gold set looks clustered — this protocol does not currently auto-detect clustering, but the operator's pre-deployment review should.

---

## Integration with existing modes

| Mode | Interaction with calibration |
|---|---|
| Stage 4 → 5 audit dispatch | Calibration runs offline; results inform the `ARS_CLAIM_AUDIT` ramp-on decision. |
| Cite-Time Provenance Finalizer | No direct coupling — calibration evaluates the judge in isolation; the finalizer's matrix is downstream. |
| `/ars-mark-read` clearance | Calibration does not interact with mark-read state; HIGH-WARN-CLAIM-NOT-SUPPORTED stays non-clearable regardless of calibration outcome. |
| Reviewer `calibration` mode | Sibling, not coupled. Both compute FNR/FPR but on different units (papers vs claim-tuples); both can run in the same session. |

---

## Resolved design decisions (2026-05-15, per spec §10 OQs)

- **Activation**: opt-in. The audit agent ships with default thresholds and the canonical fixture; operators run `scripts/test_claim_audit_calibration` as a CI gate. Re-calibration with a domain-specific gold set is the operator's call, not auto-triggered.
- **Threshold values**: FNR < 0.15 + FPR < 0.10. Tightened from the reviewer-mode 0.17 / 0.50 Lu 2026 reference points because the audit unit (per-claim) is simpler than the reviewer unit (whole paper) — the gate should track the stricter end of plausible LLM-as-judge accuracy.
- **Ensembling**: not in v3.8.0. Per-tuple alignment calls are short and the judge's response shape is constrained; majority-vote ensembling adds cost without obvious accuracy gain for this unit of analysis. Re-evaluate if calibration evidence in v3.8.x shows high variance.
- **Cross-model verification**: out of scope for the calibration runner — `ARS_CROSS_MODEL` interacts with the audit agent dispatch path, not the calibration script. An operator wanting cross-model calibration runs the runner twice with different `judge_model` settings.

---

## Running locally

```bash
PYTHONPATH=. python3 -m unittest scripts.test_claim_audit_calibration -v
```

The CI-equivalent invocation lives in `.github/workflows/spec-consistency.yml` (the v3.8 `#103` unittest step). Both paths exercise T-C1 (threshold gates), T-C2 (per-class FNR/FPR reporting), and T-C3 (gold-set shape integrity).

---

## References

- Spec: `docs/design/2026-05-15-issue-103-claim-alignment-audit-spec.md` §7.7 (test contract) + §1 deliverable 7 (this doc) + §9 (acceptance criteria) + §13 step 10 (implementation order).
- Issue: [academic-research-skills #103](https://github.com/Imbad0202/academic-research-skills/issues/103) acceptance criterion (FNR < 0.15 + FPR < 0.10 gates).
- Parent agent: `academic-pipeline/agents/claim_ref_alignment_audit_agent.md` — dispatches calibration mode and consumes the report's thresholds block. The agent prompt and this doc form a two-way pair following the v3.6.5 protocol-doc convention (`literature_corpus_consumers.md` ↔ `bibliography_agent.md`).
- Reviewer calibration baseline: `academic-paper-reviewer/references/calibration_mode_protocol.md` (same vocabulary, different unit of analysis).
- Lu, C. et al. (2026). *Nature* 651, 914-919 — Table 1 reference rates for LLM-vs-human agreement on whole-paper decisions; this protocol uses tighter thresholds for the simpler per-claim unit.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-claim-verification-protocol-md"></a>

## SOURCE: skills/academic-pipeline/references/claim_verification_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=2784 -->
# Claim Verification Protocol (Phase E)

## Purpose
Verifies that quantitative and factual claims in the paper are accurately supported by their cited sources. Phase A-D verify that references exist and are original; Phase E verifies that claims derived from those references are truthful.

## Scope
- All numerical claims (percentages, counts, effect sizes, p-values)
- All categorical assertions ("X is the largest...", "Y was the first to...")
- All trend claims ("increasing", "declining", "stable")
- All causal claims ("X causes Y", "X leads to Y")

## E1: Claim Extraction
- Scan the paper for all quantitative/factual claims
- For each claim, record: claim text, cited source(s), paper section, page/line
- Expected output: Claim Registry table

## E2: Source Tracing
- For each claim, locate the specific passage in the cited source that supports it
- Use WebSearch + DOI lookup to find the original source
- If source is behind paywall, note as UNVERIFIABLE_ACCESS

## E3: Cross-Referencing
- Compare claim text vs source text
- Check: exact numbers, date ranges, population descriptions, methodology descriptions
- Flag any discrepancies

## Verdict Taxonomy

| Verdict | Definition | Severity | Example |
|---------|-----------|----------|---------|
| VERIFIED | Claim matches source exactly or within rounding tolerance | None | Paper: "15.2%"; Source: "15.2%" |
| MINOR_DISTORTION | Claim paraphrases source but meaning is preserved | MINOR | Paper: "about 15%"; Source: "15.2%" |
| MAJOR_DISTORTION | Claim oversimplifies, exaggerates, or misrepresents source | SERIOUS | Paper: "declined sharply"; Source: "declined by 2.1%" |
| UNVERIFIABLE | Source doesn't contain the claimed information | SERIOUS | Paper cites Smith (2020) for a claim, but Smith (2020) doesn't discuss this topic |
| UNVERIFIABLE_ACCESS | Source exists but full text not accessible for verification | MEDIUM | Paywalled journal article |

## Sampling Strategy
- Mode 1 (pre-review): 30% random sample of claims (minimum 10 claims)
- Mode 2 (final-check): 100% of claims

## Output Format

### Claim Verification Report
| # | Claim | Source | Section | Verdict | Detail |
|---|-------|-------|---------|---------|--------|
| 1 | [claim text] | [source] | [section] | VERIFIED | Exact match |
| 2 | [claim text] | [source] | [section] | MAJOR_DISTORTION | Paper says X, source says Y |

### Summary
- Total claims checked: [N]
- VERIFIED: [N]
- MINOR_DISTORTION: [N]
- MAJOR_DISTORTION: [N] (must be 0 for PASS)
- UNVERIFIABLE: [N] (must be 0 for PASS)
- UNVERIFIABLE_ACCESS: [N] (noted but does not block PASS)

## Pass/Fail Criteria
- PASS: Zero MAJOR_DISTORTION + Zero UNVERIFIABLE
- FAIL: Any MAJOR_DISTORTION or UNVERIFIABLE
- PASS_WITH_NOTES: Only MINOR_DISTORTION and/or UNVERIFIABLE_ACCESS
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-external-review-protocol-md"></a>

## SOURCE: skills/academic-pipeline/references/external_review_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=6329 -->
# External Review Protocol (Added in v2.5)

**Scenario**: The user submitted to a journal and received feedback from real human reviewers, bringing those comments into the pipeline.

**Trigger**: User says "I received reviewer comments," "reviewer comments," "revise and resubmit," etc.

## Differences from Internal Review

| Aspect | Internal Review (Stage 3 simulation) | External Review (real journal) |
|--------|-------------------------------------|-------------------------------|
| Source of review comments | Pipeline's AI reviewers | Journal's human reviewers |
| Comment format | Structured (Revision Roadmap) | Unstructured (free text, PDF, email) |
| Comment quality | Consistent, predictable | Variable quality, may be vague or contradictory |
| Revision strategy | Can accept wholesale | Need to judge which to accept/reject/negotiate |
| Acceptance criteria | AI re-review suffices | Ultimately decided by human reviewers |

## Step 1: Intake and Structuring

```
1. Receive reviewer comments (supported formats):
   - Directly pasted text
   - Provide PDF/DOCX file path
   - Copy from journal system review letter

2. Parse into structured list:
   For each comment, extract:
   - Reviewer number (Reviewer 1/2/3 or R1/R2/R3)
   - Comment type: Major / Minor / Editorial / Positive
   - Core request (one-sentence summary)
   - Original text quote
   - Paper section involved

3. Produce External Review Summary:
   +----------------------------------------+
   | External Review Summary                |
   +----------------------------------------+
   | Journal: [journal name]                |
   | Decision: [R&R / Major / Minor]        |
   | Reviewers: [N]                         |
   | Total comments: [N]                    |
   |   Major: [n]  Minor: [n]  Editorial: [n]|
   +----------------------------------------+

4. Confirm parsing results with user:
   "I organized the reviewer comments into [N] items. Here is the summary — please confirm nothing was missed or misinterpreted."
```

## Step 2: Strategic Revision Coaching (External Revision Coaching)

Unlike the Socratic coaching for internal review, external review coaching focuses more on **strategic judgment**:

```
For each Major comment, guide the user to think through:

1. Understanding layer
   "What is this reviewer's core concern? Is it about methodology, theory, or presentation?"

2. Judgment layer
   "Do you agree with this criticism?"
   - Agree -> "How do you plan to revise?"
   - Partially agree -> "Which parts do you agree with and which not? What is your basis for disagreement?"
   - Disagree -> "What is your rebuttal argument? Can you support it with literature or data?"

3. Strategy layer
   "How will you phrase this in the response letter?"
   - Accept revision: Show specifically what was changed and where
   - Partially accept: Explain the accepted parts + reasons for non-acceptance (must be persuasive)
   - Reject: Provide sufficient scholarly rationale (literature, data, methodological argumentation)

4. Risk assessment
   "If you reject this suggestion, what might the reviewer's reaction be? Is it worth the risk?"
```

**Key principles**:
- **Do not default to "accept all"**: Real reviewer comments are not always correct — some may be based on misunderstanding or school-of-thought bias
- **Encourage user to inject context**: "What school of thought do you think this reviewer might come from? What context might they not be aware of?"
- **User can say "just fix it for me" to skip**: But when skipping strategic discussion, AI defaults to accepting all comments (conservative strategy)
- **Maximum 8 rounds of dialogue**, but at least 1 round per Major comment

## Step 3: Revision and Response to Reviewers

```
Produce two documents:

1. Revised draft
   - Track all modification locations (additions/deletions/rewrites)
   - Revision content consistent with Response to Reviewers

2. Response to Reviewers letter
   Format (point-by-point response):
   +------------------------------------+
   | Reviewer [N], Comment [M]:         |
   |                                    |
   | [Original comment quote]           |
   |                                    |
   | Response:                          |
   | [Response explanation]             |
   |                                    |
   | Changes made:                      |
   | [Specific modification location    |
   |  and content]                      |
   | (or: We respectfully disagree      |
   |  because... [rationale])           |
   +------------------------------------+
```

## Step 4: Self-Verification (Completeness Check)

```
Stage 3' behavior adjustments in external review mode:

1. Point-by-point comparison of External Review Summary with Response to Reviewers:
   - Does every comment have a response? (completeness)
   - Is each response consistent with actual changes? (consistency)
   - Were the places claimed as "modified" actually changed? (truthfulness)

2. New citation verification:
   - New references added during revision enter Stage 4.5 integrity verification

3. Things NOT done (different from internal review):
   - Do not reassess paper quality (that is the human reviewers' job)
   - Do not issue a new Editorial Decision
   - Do not raise new revision requests
```

## Honest Capability Boundaries

1. **AI verification does not equal human reviewer satisfaction**: Stage 3' can confirm revisions are "complete and consistent," but cannot predict whether human reviewers will accept your responses. Reviewers may have unstated expectations, school-of-thought preferences, or methodological insistence
2. **Unstructured comments may not parse perfectly**: Some reviewers write vaguely (e.g., "the methodology needs more work"), and AI will do its best to parse but may miss implied intentions. After parsing, **user confirmation is mandatory**
3. **AI cannot make scholarly judgments for you**: "Should I accept Reviewer 2's suggestion?" is your decision. AI can provide an analytical framework, but final judgment rests with the researcher
4. **Cross-cultural review convention differences**: Response conventions differ across journals/academic circles (some require extreme deference, others accept direct rebuttal). AI defaults to neutral academic tone; the user can request adjustments
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-integrity-review-protocol-md"></a>

## SOURCE: skills/academic-pipeline/references/integrity_review_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=2390 -->
# Integrity Review Protocol (Added in v2.0)

## Stage 2.5: First Integrity Check (Pre-Review Integrity)

**Trigger**: After Stage 2 (WRITE) completion, before Stage 3 (REVIEW)
**Purpose**: Ensure all references and data are not fabricated or erroneous before submission for review

```
Execution steps:
1. integrity_verification_agent executes Mode 1 (initial verification) on the paper
2. Verification scope:
   - Phase A: 100% reference existence + bibliographic accuracy + ghost citations
   - Phase B: >= 30% citation context spot-check
   - Phase C: 100% statistical data verification
   - Phase D: >= 30% originality spot-check + self-plagiarism check
   - Phase E: 30% claim verification spot-check (minimum 10 claims)
3. Result handling:
   - PASS -> checkpoint -> Stage 3
   - FAIL -> produce correction list -> fix item by item -> re-verify corrected items
   - PASS after corrections -> checkpoint -> Stage 3
   - Still FAIL after 3 rounds -> notify user, list unverifiable items
```

## Stage 4.5: Final Integrity Check (Post-Revision Final Check)

**Trigger**: After Stage 4' (RE-REVISE) or Stage 3' (RE-REVIEW, Accept) completion, before Stage 5 (FINALIZE)
**Purpose**: Confirm the revised paper is 100% correct and ready for publication

```
Execution steps:
1. integrity_verification_agent executes Mode 2 (final verification) on the revised draft
2. Verification scope:
   - Phase A: 100% reference verification (including those added during revision)
   - Phase B: 100% citation context verification (not spot-check, full check)
   - Phase C: 100% statistical data verification
   - Phase D: >= 50% originality spot-check (100% for newly added/modified paragraphs)
   - Phase E: 100% claim verification (zero MAJOR_DISTORTION + zero UNVERIFIABLE required)
3. Special check: Compare with Stage 2.5 results to confirm all previous issues are resolved
4. Result handling:
   - PASS (zero issues) -> checkpoint -> Stage 5
   - FAIL -> fix -> re-verify -> PASS -> Stage 5
5. ⚠️ **IRON RULE**: Must PASS with zero issues to proceed to Stage 5
```

## Score Trajectory Tracking (v3.3)

Reference: `academic-pipeline/references/score_trajectory_protocol.md`

At Stage 3' (RE-REVIEW), the `pipeline_orchestrator_agent` tracks per-dimension score deltas and triggers a MANDATORY checkpoint on regressions. Results stored in Integrity Report `score_trajectory` field (Schema 5).
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-plagiarism-detection-protocol-md"></a>

## SOURCE: skills/academic-pipeline/references/plagiarism_detection_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=13795 -->
# Plagiarism Detection Protocol — Phase D Originality Verification Protocol

This document defines the complete execution protocol for `integrity_verification_agent`'s Phase D (originality verification), including paragraph-level comparison, self-plagiarism check, AI-generated text characteristic detection, severity grading, and tool limitation disclaimers.

---

## Phase D Overview: Originality Verification

Phase D's purpose is to perform originality screening on body text content before paper submission for review and after revision completion. Unlike Phases A-C which focus on "whether citations and data are correct," Phase D focuses on "whether the body text itself is originally written."

**Core principle: Heuristic screening, not final determination.** This protocol uses WebSearch for publicly available literature comparison. Results are preliminary screening signals and do not equate to conclusions from professional plagiarism detection software.

---

## D1: Paragraph-Level Originality Check

### D1.1 Characteristic Sentence Extraction

```
For each paragraph in the paper body text:
1. Identify the paragraph's topic and core argument
2. Extract 1-2 "characteristic sentences"
   - Priority selection: Sentences containing specific data, proper nouns, or unique arguments
   - Avoid: Generic academic boilerplate (e.g., "This study aims to...")
3. Record the characteristic sentence's paragraph location (section + paragraph number)
```

### D1.2 WebSearch Comparison

```
For each extracted characteristic sentence:
1. Use the characteristic sentence (or key fragment) as a WebSearch query
   - Search term: Enclose 8-12 consecutive words in quotation marks
   - Supplementary search: Remove quotes to check for paraphrased versions
2. Review the top 5-10 search results
3. Compare text similarity between original and search results
```

### D1.3 Comparison Result Grading

| Grade | Code | Definition | Determination Criteria |
|-------|------|-----------|----------------------|
| Original | `ORIGINAL` | No similar expression found in public literature | WebSearch returns no related matches |
| Common Knowledge | `COMMON_KNOWLEDGE` | The knowledge is a widely accepted fact in the field | Multiple sources express the same fact in different ways |
| Paraphrase | `PARAPHRASE` | Expresses same viewpoint as a source but with clearly different wording | Semantically similar but significantly different sentence structure and word choice, with citation |
| Close Match | `CLOSE_MATCH` | Highly similar wording to a source, with only a few words substituted | Nearly identical sentence structure, with only synonym substitutions or word order changes |
| Verbatim | `VERBATIM` | Identical or nearly identical text to a source | 20+ consecutive identical words without quotation marks |

### D1.4 Sampling Rate Requirements

| Operating Mode | Minimum Sampling Rate | Description |
|---------------|----------------------|------------|
| Mode 1 (pre-review) | **30%** | At least 30% of all body text paragraphs checked |
| Mode 2 (final-check) | **50%** | At least 50% of all body text paragraphs checked |

**Sampling strategy**:
- Priority check: Literature Review, Background, Discussion and other high-risk sections
- Must cover: At least 1 paragraph sampled from each major chapter
- Random supplement: Beyond priority paragraphs, randomly sample paragraphs to reach minimum sampling rate
- Revised paragraphs: In Mode 2, all paragraphs newly added or substantially modified during revision must be checked 100%

---

## D2: Self-Plagiarism Check

### D2.1 Author's Existing Publications Search

```
Prerequisite: User provides author name(s)

For each author (or primary author):
1. WebSearch: "author name" + research area keywords
2. Identify author's existing publication list (Google Scholar profile preferred)
3. Record existing publications related to the current paper's topic
```

### D2.2 Comparison Items

```
Compare current paper with author's existing publications (focus on these areas):
1. Methodology descriptions:
   - Is the research design description verbatim identical to prior work?
   - Are data collection and analysis method descriptions directly copied?
2. Results narratives:
   - Are textual descriptions of results reused?
   - Are table/figure description texts identical?
3. Theoretical framework:
   - Are literature review paragraphs transferred wholesale?
```

### D2.3 Legitimate Self-Citation vs. Self-Plagiarism Determination Criteria

| Scenario | Determination | Description |
|----------|--------------|------------|
| Cites prior work and restates in new language | **Legitimate self-citation** | Normal academic practice — has citation and paraphrasing |
| Cites prior work but verbatim copies original text | **Self-plagiarism** | Even with citation, extensive verbatim copying is unacceptable |
| Content highly similar to prior work without citing it | **Self-plagiarism** | Conceals relationship with prior work |
| Uses prior work's data but re-analyzes | **Legitimate** | Secondary analysis is a legitimate research method — must clearly state this |
| Methodology reuses prior work's standardized description | **Gray area** | Standardized experimental procedure descriptions allow high similarity, but citing prior work is recommended |

---

## D3: AI-Generated Text Characteristic Detection

**Important disclaimer: This section is a checklist, not a determination tool.** AI text detection technology is not yet mature, and any judgment based on text characteristics has a high false-positive risk. The following indicators are for reference only and should not serve as the basis for final determination.

### D3.1 Typical AI Writing Pattern Indicators

| # | Indicator | Description | Observation Method |
|---|-----------|------------|-------------------|
| 1 | Excessive smoothness | Abnormally uniform sentence fluency throughout, lacking natural writing rhythm variation | Compare whether writing style across chapters is overly consistent |
| 2 | Lack of specificity | Arguments remain at conceptual level, lacking specific numbers, cases, or personal research experience | Check for "for example" followed by vague content |
| 3 | Formulaic transitions | Heavy use of "Furthermore," "Moreover," "It is worth noting that" and similar transitions | Count the variety and frequency of transition phrases |
| 4 | Excessive parallelism | Highly symmetric paragraph structures (e.g., every paragraph follows: claim -> evidence -> summary) | Observe whether paragraph structure mechanically repeats |
| 5 | Hedging overload | Excessive use of "may," "could," "might," "it is possible that" to avoid definitive positions | Check whether author over-hedges even on their own research results |
| 6 | Citation-argument gap | Literature is cited but the cited content is not organically integrated with the author's arguments | Remove citations — does the paragraph's argument still hold? |

### D3.2 Handling Approach

```
If the paper triggers 2 or more AI writing indicators:
1. Flag in the verification report as "AI writing characteristic alert"
2. List the specific indicators triggered and corresponding paragraphs
3. Do NOT make a "whether it is AI-generated" determination
4. Recommend the user review the flagged paragraphs and consider adjusting writing style
```

---

## Severity Grading

| Level | Code | Definition | Trigger Conditions |
|-------|------|-----------|-------------------|
| **Critical** | `CRITICAL` | Severe academic misconduct, sufficient for retraction | Verbatim plagiarism (>20 consecutive identical words without citation); fabricated citations (citing nonexistent sources to support plagiarized content) |
| **Serious** | `SERIOUS` | Significant originality problems, requiring major revisions | Multiple close paraphrases without citing sources; extensive undisclosed self-plagiarism |
| **Moderate** | `MODERATE` | Individual paragraphs need rewriting | Individual paragraphs inadequately paraphrased (1-2 instances of `CLOSE_MATCH`); methodology description overly similar to prior work |
| **Minor** | `MINOR` | Does not affect academic integrity but improvement recommended | Excessive generic academic boilerplate; AI writing characteristic alerts (informational only, does not affect verdict) |

### Severity-to-Verdict Mapping

| Severity | Impact on Verdict |
|---------|-----------------|
| CRITICAL | Immediate FAIL, listed as highest priority correction item |
| SERIOUS | FAIL, must fix and re-verify |
| MODERATE | FAIL, must fix |
| MINOR | Does not affect PASS/FAIL verdict, noted in report |

---

## Tool Limitation Disclaimer

This protocol's originality verification has the following inherent limitations that users must be aware of:

| # | Limitation | Description |
|---|-----------|------------|
| 1 | **Not professional plagiarism detection software** | This protocol uses WebSearch for heuristic comparison, not Turnitin, iThenticate, or other professional tools — cannot calculate precise text overlap rates |
| 2 | **Limited coverage** | Can only compare publicly searchable literature (open access, preprints, web pages) — cannot search full-text databases behind paywalls |
| 3 | **Language limitation** | Cross-language plagiarism (e.g., plagiarism via translation) is difficult to detect |
| 4 | **Sampling, not exhaustive** | Limited by efficiency, only 30%-50% of paragraphs are sampled — missed detection risk exists |
| 5 | **Time sensitivity** | Search results change over time; newly published literature may not be in search scope |
| 6 | **AI detection unreliable** | D3's AI writing indicators are heuristic alerts with high false-positive rates and should not serve as determination basis |

**Recommendation**: This protocol's results serve as preliminary screening. It is recommended to use professional plagiarism detection tools (such as Turnitin / iThenticate) for complete duplicate checking before formal submission.

---

## Output Format Template

```markdown
## Phase D: Originality Verification Results

### Verification Parameters
- Operating mode: [Mode 1 pre-review / Mode 2 final-check]
- Total body text paragraphs: X
- Paragraphs sampled: Y (sampling rate: Z%)
- Author self-plagiarism check: [Executed / Not executed (author information not provided)]

### D1 Paragraph-Level Comparison Results Summary

| Grade | Paragraph Count | Proportion |
|-------|----------------|-----------|
| ORIGINAL | X | X% |
| COMMON_KNOWLEDGE | X | X% |
| PARAPHRASE | X | X% |
| CLOSE_MATCH | X | X% |
| VERBATIM | X | X% |

### D2 Self-Plagiarism Check Results

| # | Current Paper Paragraph | Existing Publication | Similarity Type | Determination |
|---|------------------------|---------------------|----------------|--------------|
| 1 | §X.X, paragraph Y | Author (Year), Title | Methodology description similar | Legitimate self-citation / Self-plagiarism |

### D3 AI Writing Characteristic Alerts

| # | Indicator | Triggered Paragraph | Description |
|---|-----------|---------------------|------------|
| 1 | [Indicator name] | §X.X | [Specific observation] |

Indicators triggered: X / 6 ([Below threshold, not flagged / Threshold reached, user review recommended])

### Phase D Issue List

| # | Severity | Type | Location | Issue Description | Matching Source | Recommended Action |
|---|----------|------|----------|------------------|----------------|-------------------|
| 1 | CRITICAL | VERBATIM | §X.X, paragraph Y | N consecutive words identical to source | [URL] | Rewrite or add quotation marks for direct quote |
| 2 | SERIOUS | CLOSE_MATCH | §X.X, paragraph Y | Highly similar wording, only a few words substituted | [URL] | Rewrite and add citation |
| 3 | MODERATE | Self-plagiarism | §X.X, paragraph Y | Methodology description verbatim identical to prior work | Author (Year) | Rewrite and cite prior work |

### Tool Limitation Disclaimer

> This originality verification uses WebSearch for heuristic comparison and is not professional plagiarism detection software (such as Turnitin / iThenticate). Coverage is limited to publicly searchable literature, with a sampling rate of [Z]%, and there is a risk of missed detection. These results serve as preliminary screening; it is recommended to use professional plagiarism detection tools for complete duplicate checking before formal submission.
```

---

## Relationship with Other Phases

| Phase | Focus | Relationship with Phase D |
|-------|-------|--------------------------|
| Phase A: Reference Verification | Whether references exist and are correct | A verifies sources, D verifies body text; if D finds VERBATIM without citation, it may also reveal A3 dangling citation issues |
| Phase B: Citation Context Verification | Whether citations accurately reflect original text | B checks "whether cited content is correct," D checks "whether uncited content is original" |
| Phase C: Data Verification | Whether statistical data is correct | C and D are complementary: C verifies data, D verifies text |

---

## Reproducibility Requirements

To ensure the originality verification process is reproducible:

1. **Standardized search strategy**: Use the same search template for each characteristic sentence
   - Search term 1: `"key fragment" (8-12 words, in quotes)`
   - Search term 2: `keyword combination (without quotes, to match paraphrases)`

2. **Explicit determination criteria**: Each grade (ORIGINAL through VERBATIM) has clear determination criteria, not relying on subjective feeling

3. **Complete records**: Search terms, search results, and determination rationale for each sampled paragraph are recorded in the Audit Trail

4. **Timestamps**: Report includes execution time, as search results change over time
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-reproducibility-audit-md"></a>

## SOURCE: skills/academic-pipeline/references/reproducibility_audit.md

<!-- SOURCE-CONTENT-BEGIN bytes=2371 -->
# Reproducibility

v2.0 design ensures consistent quality assurance with each execution:

## Standardized Workflow

| Guarantee Item | Mechanism |
|---------------|-----------|
| Integrity check every time | Stage 2.5 + Stage 4.5 are **mandatory** stages, cannot be skipped |
| Consistent review angles | EIC + R1/R2/R3 + Devil's Advocate — five fixed perspectives |
| Consistent verification methods | integrity_verification_agent uses standardized search templates |
| Consistent quality thresholds | Integrity check PASS/FAIL criteria are explicit (zero SERIOUS + zero MEDIUM + zero MAJOR_DISTORTION + zero UNVERIFIABLE) |
| Traceable workflow | Every stage's deliverables are recorded, enabling retrospective audit |

## Audit Trail

When the pipeline ends, state_tracker_agent produces a complete audit trail:

```
Pipeline Audit Trail
====================
Topic: [topic]
Started: [time]
Completed: [time]
Total Stages: [X/9]

Stage 1 RESEARCH: [mode] -> [output count]
Stage 2 WRITE: [mode] -> [word count]
Stage 2.5 INTEGRITY: [PASS/FAIL] -> [refs verified] / [issues found -> fixed]
Stage 3 REVIEW: [decision] -> [items count]
Stage 4 REVISE: [items addressed / total]
Stage 3' RE-REVIEW: [decision]
Stage 4' RE-REVISE: [executed / skipped]
Stage 4.5 FINAL INTEGRITY: [PASS/FAIL] -> [refs verified]
Stage 5 FINALIZE: Ask format style -> MD -> DOCX via Pandoc when available (otherwise instructions) -> LaTeX (apa7/ieee/etc.) -> tectonic -> PDF
Stage 6 PROCESS SUMMARY: Ask language -> MD -> LaTeX -> PDF (zh/en)

Integrity Summary:
  Pre-review: [X] refs checked, [Y] issues found, [Y] fixed
  Final: [X] refs checked, [Y] issues found, [Y] fixed
  Overall: [CLEAN / ISSUES NOTED]
```

## Computational reproducibility (v3.3.5+)

This document defines PROCESS reproducibility — consistent stages, fixed reviewer angles,
explicit pass/fail thresholds. That's one of two meanings of "reproducible."

The other is COMPUTATIONAL re-run — could a third party re-execute the same pipeline and
produce the same (or near-same) output? For that, see [`../../shared/artifact_reproducibility_pattern.md`](../../shared/artifact_reproducibility_pattern.md).

Process reproducibility is enforced at the pipeline level. Computational documentation is
captured in the Material Passport's optional `repro_lock` sub-block. Both are complementary;
neither replaces the other.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-two-stage-review-protocol-md"></a>

## SOURCE: skills/academic-pipeline/references/two_stage_review_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=1404 -->
# Two-Stage Review Protocol (Added in v2.0)

## Stage 3: First Review (Full Review)

- **Input**: Paper that passed integrity check
- **Review team**: EIC + R1 (methodology) + R2 (domain) + R3 (interdisciplinary) + Devil's Advocate
- **Output**: 5 review reports + Editorial Decision + Revision Roadmap + Socratic Revision Coaching
- **Decision branches**: Accept -> Stage 4.5 / Minor|Major -> Revision Coaching -> Stage 4 / Reject -> Stage 2 or end

See `academic-paper-reviewer/SKILL.md` for review process details.

## Stage 3 -> 4 Transition: Revision Coaching

EIC uses Socratic dialogue to guide the user in understanding review comments and planning revision strategy (max 8 rounds). User can say "just fix it for me" to skip.

## Stage 3': Second Review (Verification Review)

- **Input**: Revised draft + Response to Reviewers + original Revision Roadmap
- **Mode**: `academic-paper-reviewer` re-review mode
- **Output**: Revision response comparison table + new issues list + new Editorial Decision + R&R Traceability Matrix (Schema 11)
- **Decision branches**: Accept|Minor -> Stage 4.5 / Major -> Residual Coaching -> Stage 4'

See `academic-paper-reviewer/SKILL.md` Re-Review Mode for verification review process.

## Stage 3' -> 4' Transition: Residual Coaching

EIC guides the user in understanding residual issues and making trade-offs (max 5 rounds). User can say "just fix it" to skip.
<!-- SOURCE-CONTENT-END -->
