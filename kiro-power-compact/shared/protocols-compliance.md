<a id="source-shared-agents-compliance-agent-md"></a>

## SOURCE: shared/agents/compliance_agent.md

<!-- SOURCE-CONTENT-BEGIN bytes=7383 -->
---
name: compliance_agent
description: "Runs PRISMA-trAIce + RAISE compliance checks at Stage 2.5 / 4.5 integrity gates and emits Schema 12 compliance_report"
version: 1.0.0
owner_skill: shared
invoked_by: [academic-pipeline, deep-research, academic-paper]
data_access_level: verified_only
task_type: open-ended
status: active
related_skills: [academic-pipeline, deep-research, academic-paper]
last_updated: "2026-04-20"
related_protocols:
  - shared/prisma_trAIce_protocol.md
  - shared/raise_framework.md
  - shared/compliance_checkpoint_protocol.md
  - shared/compliance_report.schema.json
  - academic-paper/references/anti_leakage_protocol.md
  - academic-pipeline/references/ai_research_failure_modes.md
---

# compliance_agent

Mode-aware agent that runs PRISMA-trAIce + RAISE compliance checks at Stage 2.5 / 4.5 Integrity Gates, producing Schema 12 `compliance_report` outputs.

## Scope

- **Reads:** manuscript draft, methodology blueprint, bibliography, material passport, user-provided AI tool metadata
- **Writes nothing to the manuscript.** Output is a separate `compliance_report` handed to the orchestrator.
- **Does not hallucinate missing items.** Anti-Leakage Protocol applies: missing material → `[MATERIAL GAP: <item_id>]` in the gap reason (see [`shared/compliance_checkpoint_protocol.md#canonical-gap-tag-vocabulary`](../compliance_checkpoint_protocol.md#canonical-gap-tag-vocabulary)).

## Input contract

```yaml
compliance_mode: "systematic_review" | "primary_research" | "other_evidence_synthesis"
stage: "2.5" | "4.5"
materials:
  manuscript_draft: <path or inline>
  methodology_blueprint: <path>
  bibliography: <path>
  material_passport: <Schema 9 payload>
user_metadata:
  intended_venue: <string or null>
  ai_tools_used:
    - {name, version, developer, stage, purpose, access_url_or_doi}
```

## Output contract

`compliance_report` conforming to `shared/compliance_report.schema.json` (Schema 12). Appended to `material_passport.compliance_history[]` by the orchestrator.

## Dispatch logic

```python
if compliance_mode == "systematic_review":
    run PRISMA-trAIce checks (Stage-specific item subset)
    run RAISE full (principles + 8-role matrix)
    block_decision respects tier semantics
elif compliance_mode == "other_evidence_synthesis":
    run PRISMA-trAIce checks in "adaptation" mode (items become Info)
    run RAISE full
    block_decision capped at warn
elif compliance_mode == "primary_research":
    run RAISE principles_only
    set prisma_trAIce to null
    block_decision capped at warn
```

## Stage behaviour

| Stage | PRISMA-trAIce items checked | RAISE focus |
|---|---|---|
| 2.5 | M1, M2, M3, M4, M5, M6, M7, M8, M9, M10 | human_oversight, fit_for_purpose |
| 4.5 | T1, A1, I1, R1, R2, D1, D2 | transparency, reproducibility (+ full 8-role matrix for SR) |

Items within each stage subset are independent and MAY be evaluated concurrently. The agent SHOULD read `material_passport.compliance_history[]` only for prior-loop auditability context; prior reports are not re-evaluated.

## Tier → decision mapping (SR mode)

| Tier | FAIL → |
|---|---|
| Mandatory | `block_decision = block` |
| Highly Recommended | `block_decision = warn` |
| Recommended | `block_decision = pass` (logged as info) |
| Optional | `block_decision = pass` (logged as info) |

Multiple tier contributions aggregate using `max_severity` (see `compliance_checkpoint_protocol.md §Decision precedence`).

### Mandatory-block surface message

When a Mandatory-tier PRISMA-trAIce item triggers `block_decision = block`, the surfaced block message MUST include the following maturity note alongside the gap reason and override-ladder reference, so the user understands what authority is blocking them:

> *Note: PRISMA-trAIce is currently a foundational proposal (Holst et al. 2025, *JMIR AI*, doi:[10.2196/80247](https://doi.org/10.2196/80247)), developed via systematic adaptation rather than a formal Delphi consensus study. Items have not yet been empirically validated across diverse research contexts. See `shared/prisma_trAIce_protocol.md` § Status disclaimer.*

This note is informational only — it does not lower the block severity. The Mandatory-as-block design choice follows the authors' own argument (Holst et al. 2025) that non-transparent AI use is the higher-cost failure mode. Surfacing the maturity note mirrors the disclosure pattern in [`academic-pipeline/references/plagiarism_detection_protocol.md`](../../academic-pipeline/references/plagiarism_detection_protocol.md), which discloses heuristic-screening scope to the user.

## Self-check protocol

Before finalising the report, the agent runs four self-checks. Any flagged check requires re-examination:

| ID | Question | On fail |
|---|---|---|
| CA-1 | Am I quoting PRISMA-trAIce items from memory or from `shared/prisma_trAIce_protocol.md`? | Re-read the protocol file; requote. |
| CA-2 | Are my block decisions anchored to each item's stated tier, not promoted/demoted from memory? | Re-read tier assignments; correct any drift. |
| CA-3 | **SR mode only.** Did all 17 items pass AND `evidence[]` is empty? (Sycophancy risk) | Do a second pass over the 3 most-commonly-missed Mandatory items (M4, M6, M8); require explicit evidence path citation. |
| CA-4 | For each RAISE principle marked `pass`, is `principle_evidence[<principle>]` non-empty? | Downgrade the principle to `warn` with note `[WEAK EVIDENCE]`. |

Self-check failures are not errors — they are the agent's guardrail. Document the self-check pass/fail in the agent log (not in compliance_report) for auditability.

## Error behaviour

| Error | Handling |
|---|---|
| Missing input material | Apply Anti-Leakage: mark `[MATERIAL GAP]`, item auto-FAILs, tier dictates block/warn. Never hallucinate. |
| Mode/context mismatch (e.g. `academic-paper full` passes SR mode) | Refuse with `{decision: "abort", reason: "mode/context mismatch"}`. Orchestrator must re-evaluate and re-invoke. |
| Schema validation failure on own output | Halt, surface internal error to orchestrator. Do NOT append invalid report to compliance_history. |
| Upstream drift (snapshot_date vs GitHub) | Set `upstream_sync_status: "stale"` in report. Non-blocking. |

## Interaction with existing agents

- Runs AFTER `integrity_verification_agent` (existing) at Stage 2.5 / 4.5 — compliance extends integrity, does not replace it.
- Runs ALONGSIDE `failure_mode_checklist` (v3.2). Non-overlapping scope: failure_mode checks research validity; compliance checks reporting transparency.
- Provides output consumed by `report_compiler_agent` (at Stage 6) for the AI Self-Reflection Report compliance summary.

## Invocation protocol

The orchestrator (or standalone skill) passes the input contract via the Agent tool with `model: sonnet` or higher (per user CLAUDE.md: never haiku). The agent returns the serialised compliance_report. The orchestrator validates against Schema 12 before appending to passport.

## Related reading

- `shared/prisma_trAIce_protocol.md` — item-level checks
- `shared/raise_framework.md` — principle definitions and role matrix
- `shared/compliance_checkpoint_protocol.md` — checkpoint behaviour and override ladder
- `academic-paper/references/anti_leakage_protocol.md` — gap-marking discipline
- `academic-pipeline/references/pipeline_state_machine.md` — FAIL-loop integration
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-compliance-checkpoint-protocol-md"></a>

## SOURCE: shared/compliance_checkpoint_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=7175 -->
---
title: Compliance Checkpoint Protocol (Stage 2.5 / 4.5 dual gate)
applies_to: "shared/agents/compliance_agent.md"
---

# Compliance Checkpoint Protocol

Defines how `compliance_agent` participates in Stage 2.5 and Stage 4.5 Integrity Gates, how its decision interacts with the existing FAIL loop, and how user overrides are processed.

**Used by**: `compliance_agent` (Task 8), `academic-pipeline/SKILL.md` Stage 2.5 / 4.5.

## Dual-gate summary

| Aspect | Stage 2.5 | Stage 4.5 |
|---|---|---|
| PRISMA-trAIce scope (SR mode only) | M1, M2, M3, M4, M5, M6, M7, M8, M9, M10 | T1, A1, I1, R1, R2, D1, D2 |
| RAISE principles focus | human_oversight, fit_for_purpose | transparency, reproducibility |
| RAISE 8-role matrix | not populated | populated (SR mode only) |
| Block condition | SR mode AND any Mandatory item = FAIL, OR SR mode AND any RAISE principle = fail | Same |
| Warn condition | Highly Recommended FAIL, OR RAISE principle = warn | Same |
| Info condition | Recommended / Optional FAIL | Same |
| Non-SR mode | RAISE principles_only, warn-only (never block) | Same |
| Checkpoint output | FULL checkpoint + `compliance` section in dashboard | Same |

## Decision precedence

Inside a single checkpoint, decisions aggregate as:

```
overall_decision = max_severity(
  prisma_trAIce.block_decision,
  raise.block_decision,
  legacy_integrity_verification_decision,  # existing Stage 2.5/4.5 check
  legacy_failure_mode_checklist_decision   # v3.2 Failure Mode Checklist
)

severity order: pass < warn < block
```

Non-SR mode caps the compliance contribution at `warn`.

## User action UX

### On block

Orchestrator presents:

```
[COMPLIANCE BLOCK] Stage <N>

PRISMA-trAIce Mandatory fails: M4 (Input Data)
RAISE principles fail: reproducibility

Choose:
  (a) backfill — return to Stage 2 and add missing material
  (b) manual handling — edit manuscript directly, rerun compliance
  (c) acknowledge limitation — invoke user override (see §Override Ladder)
```

### On warn

Dashboard bullets, FULL checkpoint. User confirms with free text or `continue`.

### On info (Recommended / Optional fail)

Bullet in dashboard, no flow interruption.

## Canonical gap-tag vocabulary

Compliance reports and fixture templates use these canonical tags in `gaps[].reason`, `principle_evidence[]`, and narrative fields. They are lexical signals — `compliance_agent` (Task 8) and downstream readers pattern-match on them.

| Tag | Where it appears | Meaning |
|---|---|---|
| `[MATERIAL GAP]` | `gaps[].reason`, `principle_evidence[]`, `evidence[]` | The item cannot be verified because the underlying material (passport field, manuscript section, supplementary file) is missing. Apply [Anti-Leakage Protocol](../academic-paper/references/anti_leakage_protocol.md) — do not hallucinate. |
| `[WEAK EVIDENCE]` | `principle_evidence[]` | The item is nominally reported but the description is too vague for auditor use. Triggers CA-4 downgrade: a RAISE principle marked `pass` with `[WEAK EVIDENCE]` in its evidence should be downgraded to `warn`. |
| `[GAP]` | `roles[].evidence_synthesists` narrative and similar role-level fields | Short form for a role-level gap carried forward from item-level fails. Permitted only in the 8-role matrix narrative; item-level reasons MUST use the long `[MATERIAL GAP]` form. |

Casing is significant — uppercase square-bracketed. Lowercase or missing brackets are treated as plain prose and will not be recognised as gap signals.

## Override Ladder (3-round friction)

Triggered when user picks "acknowledge limitation" on a block.

| Round | Behaviour |
|---|---|
| 1st block override | Warn user. Rationale optional. Allowed. |
| 2nd (if user re-enters block state) | Require rationale string (any length). |
| 3rd | Require rationale ≥ 100 chars. Only released on rationale confirmation. |

Round count is per-stage-per-pipeline-run, stored in `compliance_history[].user_override` entries.

> **Enforcement boundary.** This ladder is enforced at **runtime by `compliance_agent`** using the `compliance_history[]` round counter, NOT by Schema 12. Schema 12 intentionally permits `user_override.rationale.minLength: 1` so that legacy passports and cross-session resume do not fail validation on historical entries. The round-counter increment and ≥100-char rationale check live in the agent's write-path, not in the JSON Schema. If you bypass the agent and hand-write a `user_override` entry into the passport, Schema 12 will accept any rationale length — but that entry will not have gone through the friction ladder and must be treated as unaudited.

On any successful override, the agent generates `disclosure_addendum` text and the orchestrator **auto-injects** it into the manuscript's AI disclosure section. The addendum is non-removable — this is the concrete form of the `no detection evasion` iron rule in CONTRIBUTING.md.

### `disclosure_addendum` template

```
The authors acknowledge the following compliance limitations for this <evidence synthesis|manuscript>:
- PRISMA-trAIce <item_id> (<item_title>) not fully reported. Rationale: <user text>.
- RAISE principle <principle_name>: <partial|not met>. Rationale: <user text>.
```

**Template fill rules** (compliance_agent uses these deterministically):

- `<evidence synthesis|manuscript>`: pick `evidence synthesis` when `mode in {systematic_review, other_evidence_synthesis}`; pick `manuscript` when `mode == primary_research`.
- `<partial|not met>`: pick `partial` when the principle's original status was `warn`; pick `not met` when it was `fail`.
- `<item_id>`: the PRISMA-trAIce item ID as listed in `user_override.scope[]`.
- `<item_title>`: look up the short title from `shared/prisma_trAIce_protocol.md` (e.g. `M4` → "Input data").
- `<principle_name>`: one of `human_oversight`, `transparency`, `reproducibility`, `fit_for_purpose`.
- `<user text>`: verbatim copy of `user_override.rationale`, truncated to first 500 chars if longer (the addendum keeps prose; the full rationale lives in the compliance_history).

## Fail loop integration

After 3 unresolved rounds of retry at the same stage, orchestrator invokes the existing `pipeline_state_machine.md §Integrity Check FAIL Loop` procedure:

1. List all unresolvable items.
2. User picks [manual handling / remove AI usage from this stage / continue with "partially non-compliant" warning].
3. Chosen path is recorded as `compliance_history[].resolution_path`.

## Append-only history

`material_passport.compliance_history[]` never overwrites. On retry-pass, the previous fail entry is preserved with its own timestamp. The AI Self-Reflection Report at Stage 6 cites the full history to demonstrate how the correction was made — this is RAISE transparency applied to ARS itself.

## Boundary: non-pipeline invocation

When invoked from `academic-paper full` (primary research standalone), no pipeline state machine is available. Compliance_agent:

- Writes report to `./compliance_reports/<ISO-timestamp>.yaml` (local file)
- Does not trigger pipeline checkpoint dashboard
- If skill has a `disclosure` mode, hooks compliance output there
- `block_decision` capped at `warn`
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-prisma-traice-protocol-md"></a>

## SOURCE: shared/prisma_trAIce_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=10415 -->
---
title: PRISMA-trAIce Protocol (v3.4.0 snapshot)
snapshot_date: "2025-12-10"
upstream_source: "https://github.com/cqh4046/PRISMA-trAIce"
upstream_version_commit: "main"
update_policy: "Manual sync. CI freshness check runs weekly; drift emits warning, not merge block."
citation: "Holst D, et al. Transparent Reporting of AI in Systematic Literature Reviews: Development of the PRISMA-trAIce Checklist. JMIR AI. 2025. doi:10.2196/80247"
---

# PRISMA-trAIce Protocol

Verbatim snapshot of the 17-item PRISMA-trAIce checklist from the GitHub canonical source (`cqh4046/PRISMA-trAIce`), dated 2025-12-10, with per-item ARS check procedures and tier-based behaviour.

**Used by**: `compliance_agent` (Task 8), `scripts/check_prisma_trAIce_freshness.py` (Task 12).

> ⚠️ **Upstream sync warning.** If `cqh4046/PRISMA-trAIce` updates, a freshness CI check emits an annotation but does not block merges. Maintainers must manually re-sync this file and bump `snapshot_date` + `upstream_version_commit`. See `scripts/check_prisma_trAIce_freshness.py`.

## Status disclaimer

**PRISMA-trAIce is a foundational proposal, not a Delphi-consensus standard.** Holst et al. (2025) explicitly characterize their checklist as a "well-reasoned albeit preliminary guideline," developed via systematic adaptation of PRISMA 2020 rather than "a formal, broad-based Delphi study or consensus meeting," and note that the 17 items "have not yet been empirically validated across diverse research contexts." The authors frame PRISMA-trAIce as a "foundational proposal" and a "living standard" intended for the research community to "immediately adopt and refine."

ARS adopts the authors' Mandatory / Highly Recommended / Recommended / Optional tier system as defined upstream, and treats Mandatory failures as Stage 2.5 / 4.5 blocks (per the Tier legend below). This block-on-Mandatory choice follows the authors' own argument that the risk of non-transparent AI use outweighs the risk of adopting a preliminary guideline. Future revisions of the upstream living standard are pulled in via the existing freshness CI (`scripts/check_prisma_trAIce_freshness.py`).

> See Holst D, et al. JMIR AI. 2025. doi:[10.2196/80247](https://doi.org/10.2196/80247) — Discussion and Limitations sections.

## Tier legend

| Tier | Behaviour when item FAILs |
|---|---|
| Mandatory (M) | **Block**: pipeline halts; user must backfill, retreat a stage, or use the 3-round override ladder (see [`shared/compliance_checkpoint_protocol.md#override-ladder-3-round-friction`](./compliance_checkpoint_protocol.md#override-ladder-3-round-friction)) |
| Highly Recommended (HR) | **Warn**: surfaced at checkpoint; user can skip |
| Recommended (R) | **Info**: logged in compliance_report, shown as dashboard bullet |
| Optional (O) | **Info**: same as R |

> **Gap-tag vocabulary.** Tags `[MATERIAL GAP]`, `[WEAK EVIDENCE]`, `[GAP]` used in this protocol's `reason` fields are defined in [`shared/compliance_checkpoint_protocol.md#canonical-gap-tag-vocabulary`](./compliance_checkpoint_protocol.md#canonical-gap-tag-vocabulary).

## Stage assignment

| Checked at | Items |
|---|---|
| Stage 2.5 (Methods) | M1, M2, M3, M4, M5, M6, M7, M8, M9, M10 |
| Stage 4.5 (remaining) | T1, A1, I1, R1, R2, D1, D2 |

## Items

### T1 — Title
**Tier:** Optional
**Original (upstream verbatim):** "Indicate the use of AI in the title or subtitle if it played a substantial role."
**ARS check procedure:** If `user_metadata.ai_tools_used[].stage` includes any of `{screening, data_extraction, synthesis, writing}` (i.e. substantial involvement), verify manuscript title OR subtitle mentions AI. If none of the AI tools are substantial, pass automatically.
**Pass criterion:** Substring match for one of: "AI-assisted", "AI-augmented", "artificial intelligence", "LLM-assisted", or language-equivalent.

### A1 — Abstract
**Tier:** Optional
**Original:** "Briefly summarize the AI tool(s) used, the review stage(s) where they were applied."
**ARS check procedure:** Locate manuscript abstract. Verify it names ≥1 AI tool AND the review stages.
**Pass criterion:** Both named. Absence of either → fail.

### I1 — Introduction
**Tier:** Recommended
**Original:** "Briefly state the rationale for using AI tools for specific tasks."
**ARS check procedure:** In introduction, locate one sentence or more that explains why AI was chosen for its task.
**Pass criterion:** Rationale present and tied to ≥1 specific AI task.

### M1 — Protocol registration
**Tier:** Mandatory
**Original:** "State if the use of AI was pre-specified in a protocol, and document deviations."
**ARS check procedure:** Check `material_passport.protocol_registration` field OR manuscript §Methods for explicit pre-registration statement. If AI was added mid-review, check for a "deviation from protocol" paragraph.
**Pass criterion:** Either (a) pre-registration clearly stated, or (b) deviation explicitly disclosed.

### M2 — Tool identification and access
**Tier:** Mandatory
**Original:** "Specify name, version, and provider/developer for each tool, with access details."
**ARS check procedure:** For each entry in `user_metadata.ai_tools_used`, require `name`, `version`, `developer`. If tool is open-source, require repository URL or DOI.
**Pass criterion:** All three fields non-empty for every tool.

### M3 — Purpose and stage
**Tier:** Mandatory
**Original:** "Describe the specific SLR stage and the precise task the AI performed."
**ARS check procedure:** For each tool, verify stage-level task description exists (not just "used AI for screening").
**Pass criterion:** Per-tool, per-stage prose description of ≥1 sentence in manuscript §Methods.

### M4 — Input data
**Tier:** Mandatory
**Original:** "Describe data provided to the AI (e.g., training data for fine-tuning)."
**ARS check procedure:** If any tool was fine-tuned or custom-trained, verify dataset description (source, size, preprocessing). If no fine-tuning, verify this is explicitly stated.
**Pass criterion:** Either (a) dataset described, or (b) explicit "no fine-tuning performed" statement.

### M5 — Output data
**Tier:** Mandatory
**Original:** "Describe the output format (e.g., JSON, scores) and any automated post-processing."
**ARS check procedure:** Verify manuscript §Methods documents output format per tool + any post-processing pipelines.
**Pass criterion:** Format + post-processing both described.

### M6 — Prompt engineering
**Tier:** Mandatory
**Original:** "Report prompt engineering process, full prompts, key parameters for LLMs."
**ARS check procedure:** If any tool is an LLM, verify full prompt text is included (main text or supplementary) AND model parameters (temperature, top_p, max tokens, model version) are documented.
**Pass criterion:** All three present for every LLM tool.

### M7 — Operational details
**Tier:** Highly Recommended
**Original:** "Describe key operational settings, algorithms, or configurations for non-LLM AI."
**ARS check procedure:** For classical ML tools (e.g. ASReview, Abstrackr), verify algorithm + hyperparameters documented.
**Pass criterion:** Algorithm name + at least 2 hyperparameters.

### M8 — Human-AI interaction
**Tier:** Mandatory
**Original:** "Describe human interaction (number of reviewers, verification process)."
**ARS check procedure:** Verify manuscript §Methods states reviewer count, qualifications, and oversight mechanism (e.g., independent dual screening, adjudication).
**Pass criterion:** Reviewer count + oversight mechanism both present.

### M9 — AI performance evaluation methods
**Tier:** Mandatory
**Original:** "Describe methods used to evaluate AI performance (metrics, reference standards)."
**ARS check procedure:** Verify manuscript §Methods describes what performance metrics were computed (e.g., sensitivity, agreement) and against what gold standard.
**Pass criterion:** Metric + reference standard both stated.

### M10 — Data management
**Tier:** Recommended
**Original:** "Describe data management, storage, privacy measures, and compliance."
**ARS check procedure:** Verify manuscript §Methods addresses data handling (where stored, privacy controls, GDPR/IRB compliance if applicable).
**Pass criterion:** ≥2 of {storage, privacy, compliance} addressed.

### R1 — Study selection (AI-assisted)
**Tier:** Mandatory
**Original:** "In the PRISMA flow diagram/text, distinguish between records handled by AI versus human reviewers."
**ARS check procedure:** Verify PRISMA flow diagram or accompanying text explicitly separates AI-handled vs human-handled records at each screening stage.
**Pass criterion:** Explicit AI/human split in flow diagram numbers OR prose.

### R2 — AI performance metrics (results)
**Tier:** Mandatory
**Original:** "Report results of any AI performance evaluations (e.g., agreement rates)."
**ARS check procedure:** Verify manuscript §Results reports numeric performance outcomes referenced by M9.
**Pass criterion:** ≥1 quantitative metric (% agreement, Cohen's κ, sensitivity, etc.).

### D1 — Limitations of AI use
**Tier:** Recommended
**Original:** "Discuss limitations (technical issues, biases, hallucinations) and their impact."
**ARS check procedure:** Verify manuscript §Discussion has ≥1 paragraph specifically on AI limitations (not generic review limitations).
**Pass criterion:** Dedicated AI-limitations paragraph of ≥3 sentences.

### D2 — Implications of AI use
**Tier:** Optional
**Original:** "Briefly discuss the experience of using AI tools for future reviews."
**ARS check procedure:** Verify manuscript §Discussion reflects on the usability/experience of AI for this review, forward-looking.
**Pass criterion:** ≥1 forward-looking sentence about AI utility.

## Summary counts

- Mandatory: 10 — M1, M2, M3, M4, M5, M6, M8, M9, R1, R2
- Highly Recommended: 1 — M7
- Recommended: 3 — I1, M10, D1
- Optional: 3 — T1, A1, D2

Total: 17 items.

> **ARS promotion note.** Upstream's README header summary says "Mandatory: 9". Per-item tier annotations in upstream (and mirrored here) mark **both R1 and R2 as Mandatory**, summing to 10. ARS treats the per-item annotation as authoritative, since the Results-stage items (R1: AI/human split in flow diagram; R2: AI performance metric reporting) are both operationally block-level for a compliance audit. If upstream clarifies the discrepancy, re-sync.
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-policy-data-nature-policy-md"></a>

## SOURCE: shared/policy_data/nature_policy.md

<!-- SOURCE-CONTENT-BEGIN bytes=4028 -->
# Nature Portfolio — Canonical AI Policy Source

**Status**: Source of truth for Nature substantive policy content cited by both:

1. `academic-paper/references/policy_anchor_table.md` — Nature anchor (#108 policy-anchor track, verbatim quotes per 16 fields)
2. `academic-paper/references/venue_disclosure_policies.md` — Nature venue entry (v3.2 venue track, summary form)

**Provenance**: extracted from the Nature Portfolio AI editorial policy page (`https://www.nature.com/nature-portfolio/editorial-policies/ai`), wayback snapshot `nature:wayback=20260513075542` (sha256 `cf691cba…`). Section structure: `§AI authorship`, `§Generative AI images`, `§AI use by peer reviewers`, `§Editorial use`. ARS author-side matrix covers `§AI authorship` + `§Generative AI images` only.

**G4 invariant** (Decision Doc §4.3): edits to Nature substantive policy content must go through **this file** first; both downstream consumers (policy_anchor_table.md Nature section and venue_disclosure_policies.md Nature entry) re-cite from here. Direct edits to either consumer that change Nature substantive content are non-conformant.

**Dedup lint**: `verify_nature_dedup_with_venue()` in `scripts/check_policy_anchor_table.py` confirms (a) this file exists, (b) both consumers reference the path `shared/policy_data/nature_policy.md` as their canonical pointer.

---

## Nature substantive policy quotes (verbatim, source-of-truth)

### §AI authorship — text-use policy

> "Large Language Models (LLMs), such as ChatGPT, do not currently satisfy our authorship criteria. Notably an attribution of authorship carries with it accountability for the work, which cannot be effectively applied to LLMs. Use of an LLM should be properly documented in the Methods section (and if a Methods section is not available, in a suitable alternative part) of the manuscript."

> "In all cases, there must be human accountability for the final version of the text and agreement from the authors that the edits reflect their original work."

### §AI authorship — copyediting carve-out

> "The use of an LLM (or other AI-tool) for "AI assisted copy editing" purposes does not need to be declared."

The carve-out predicate (paraphrased policy framing, partial verbatim): AI-assisted improvements to human-generated texts for readability and style — explicitly **excluding** generative editorial work and autonomous content creation.

### §Generative AI images — image-rights regime

> "Springer Nature journals are unable to permit its use for publication."

> "All exceptions must be labelled clearly as generated by AI within the image field."

Carve-outs (per Nature policy text, three categories): figures using AI to enhance or compose existing scientific data; AI-generated images that are themselves the subject of academic study (e.g., AI-art history); image-generation tools used to produce illustrations clearly marked as conceptual rather than scientific.

### §Generative AI images — non-generative ML caption rule

> "should be disclosed in the relevant caption upon submission"

---

## Consumer integration notes

- `policy_anchor_table.md` Nature anchor: extracts these quotes per 16-field matrix (3 explicit-mandate + 2 explicit-recommend + 4 implicit + 7 not-addressed).
- `venue_disclosure_policies.md` Nature entry: summarises the same source as venue-track guidance (Methods placement default, full responsibility statement requirement, no AI authorship).
- Renderer (LLM-prose): when the user selects either `--venue=Nature` or `--policy-anchor=nature`, the renderer cites this file's verbatim quotes in the emitted disclosure paragraph. Both tracks share the substantive policy content; placement (Methods vs anchor-specific) is the track-specific rendering decision.

---

## Related

- Discovery doc §4.5 — Nature anchor matrix with cross-anchor observation
- Decision Doc §2.4 G4 (renderer target) + §4.3 G4 invariant (Nature dedup)
- Impl spec §3 concern #5 resolution (hybrid image output channel)
<!-- SOURCE-CONTENT-END -->
