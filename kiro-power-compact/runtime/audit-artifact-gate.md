<a id="source-docs-design-2026-04-30-ars-v3-6-7-step-6-orchestrator-hooks-spec-md"></a>

## SOURCE: docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md

<!-- SOURCE-CONTENT-BEGIN bytes=272296 -->
# ARS v3.6.7 — Step 6 Orchestrator Hooks (artifact-as-contract audit gate)

**Status:** Design — brainstorm-driven, four rounds (Q1–Q4) settled before drafting; pending iterative codex review to zero finding before ship.
**Date:** 2026-04-30
**Target release:** v3.6.7 follow-up PR (Step 6 + Step 8 of v3.6.7 main spec §9)
**Scope:** Runtime enforcement of the v3.6.7 downstream-agent pattern protection layer via an artifact-as-contract audit gate at each `pipeline_orchestrator_agent` stage transition. Plus the Step 8 synthetic evaluation fixture set that demonstrates all 18 patterns trigger and protect end-to-end.

---

## 1. Background and scope

### 1.1 Anchor

This spec implements two of the eight steps in the v3.6.7 main spec ([`2026-04-29-ars-v3.6.7-downstream-agent-pattern-protection-spec.md`](2026-04-29-ars-v3.6.7-downstream-agent-pattern-protection-spec.md)) §9 implementation table:

- **Step 6** — orchestrator hooks for automatic per-agent audit + anti-fake-audit guard. Explicitly deferred at v3.6.7 Step 1+2+7 ship via codex round 6 finding R6-002.
- **Step 8** — synthetic evaluation case demonstrating all 18 patterns triggered and protected.

Steps 1–5 + Step 7 already shipped as v3.6.7 Step 1+2+7 (main `b4fbffd`, PRs #48 + #49). The runtime enforcement layer + the eval case are the remaining v3.6.7 work; this spec covers both because the eval case design is the survival test for the runtime layer and they share contract surfaces.

### 1.2 What this spec adds

The v3.6.7 protection that already shipped is **prompt-level + lint-level**: each downstream agent prompt carries a `PATTERN PROTECTION (v3.6.7)` block, and a static lint script verifies the prompt has the right obligation phrasing in CI. That covers what the agent is *told to do*; it does not cover what the agent *actually produces* at runtime.

This spec adds **runtime enforcement**: at every stage transition where one of the three v3.6.7 downstream agents (`synthesis_agent`, `research_architect_agent` survey-designer mode, `report_compiler_agent` abstract-only mode) just produced a deliverable, the orchestrator must locate a matching audit artifact in Material Passport (Schema 9), verify the artifact passes Layer 2 (JSONL schema) + Layer 3 (sidecar metadata) anti-fake-audit checks, and read the verdict. PASS proceeds; MATERIAL blocks; MINOR escalates to user.

Audit execution itself sits outside the LLM session — codex CLI is not LLM-callable in any safe way, and `feedback_subagent_tool_hallucination.md` documents what happens when sub-agents claim audit completion they could not perform. The spec therefore treats the audit artifact as the boundary object: the deployment runs the audit (via the wrapper script in §4), the orchestrator reads the artifact. Neither side can ship without the other; faking either side is the failure this spec prevents.

The eval case (§7) is two-tier (18 micro + 1 integration), mirroring the existing 29-mutation lint suite's unit-vs-integration split that already ships in v3.6.7 Step 1+2.

**Threat model (load-bearing — narrows the scope of what the anti-fake-audit guard claims to defend against):**

The guard defends against **inadvertent Pattern C3 over-claims**: a sub-agent dispatched to produce a deliverable internalizes the multi-stage description of the audit pipeline in its prompt and emits output annotated with audit-passed metadata it never produced. This is the failure mode documented in `feedback_subagent_tool_hallucination.md`: the agent has no codex tool, never ran any audit, but the prompt's mention of a downstream audit step triggers hallucinated metadata. The guard is sufficient against this case because the hallucinated agent does not write Layer 2 JSONL or Layer 3 sidecar files at all — orchestrator finds no proposal file (§4.9), the gate blocks, the failure is loud.

The guard is **not designed for motivated forgery**: an actor with shell access who knows the spec can fabricate Layer 2 + Layer 3 + verdict files that pass all eleven gating checks. Layer 2 + Layer 3 raise per-attempt forgery cost (compose a syntactically-valid JSONL stream matching the §3.3 canonical event ordering — including an `item.started` / `item.completed` pair for any claimed tool call — with self-consistent canonical UUID `thread_id`, monotonic timestamps, real git_sha, matching bundle SHAs, exit_code 0, plus a verdict file whose Section 6 text passes `parse_audit_verdict.py`) but do not provide cryptographic non-repudiation. Defense against motivated forgery relies on §4.7 (wrapper not LLM-callable from the same session producing the deliverable) plus deployment-side discipline (audit runs in CI / SubagentStop hook / human-triggered out-of-band terminal). The motivated-forgery boundary is the rejected scope for v3.6.7 — Layer 5 (cryptographic signing) was considered and rejected as over-engineering for the inadvertent-Pattern-C3 threat surface declared above. §9 R2 carries the full risk discussion; the threat-boundary statement above is the load-bearing version that §1-§5 rely on.

This narrowed threat model — Pattern C3 inadvertent over-claim, not motivated forgery — is what justifies Layer 2 + Layer 3 as proportionate. Spec §3.3 / §3.4 / §4.7 / §5.2 / §9 R2 must all read as defending the same threat boundary; cross-section drift on this point would invite scope creep into signing or attestation infrastructure that the v3.6.7 timeline does not budget for.

### 1.3 Schema §2.2 amendment to v3.6.7 main spec

The v3.6.7 main spec §2.2 lists "No schema change" as a non-goal. Step 6 amends that line to **"No breaking schema change"**: Schema 9 gains one optional `audit_artifact[]` field, mirroring the v3.6.3 (`reset_boundary[]`), v3.6.4 (`literature_corpus[]`), and v3.4 (`compliance_history[]`) precedents documented in [`shared/handoff_schemas.md`](../../shared/handoff_schemas.md). All three precedents added optional append-friendly Schema 9 fields without breaking prior versions; Step 6 follows the same pattern.

The amendment is recorded here, not by editing the v3.6.7 main spec, because:

1. The v3.6.7 main spec is already shipped and a new `audit_artifact[]` field is genuinely additive — the original "No schema change" framing was too absolutist given existing precedent.
2. Step 6 spec is the natural home for the schema design (§3) it requires, so the carve-out and the rationale live together.
3. Future maintainers reading the v3.6.7 main spec land at §2.2 → see "amended by Step 6" → land here for the actual rule.

The v3.6.7 main spec §2.2 line should be read as: "No schema change beyond the optional `audit_artifact[]` add specified in [Step 6 spec §3](#3-schema-additions)."

---

## 2. Settled design decisions

Two rounds of decisions converged before this spec started: a four-question brainstorm with the user (Q1–Q4) that fixed the major design axes, then a three-approach architecture comparison (Approach 1–3) that fixed the runtime model. The decisions below ride into §3–§7 as load-bearing assumptions; revisiting them requires re-opening the brainstorm.

### 2.1 Brainstorm round (Q1–Q4)

| # | Question | Decision | Consequence |
|---|----------|----------|-------------|
| Q1 | Trigger scope — which agents auto-trigger audit? Just the three v3.6.7 downstream agents (A), Phase 2 + bibliography (B), or all stages (C)? | **A — v3.6.7-only.** Trigger only on `synthesis_agent`, `research_architect_agent` (survey-designer mode), `report_compiler_agent` (abstract-only mode). `bibliography_agent` patterns and other agents tracked separately. | §5 stage-transition gate fires only at the three v3.6.7 agents' exit transitions. The five `bibliography_agent` hallucination patterns documented in `feedback_ars_bibliography_agent_hallucination_patterns.md` are out of scope for v3.6.7; they are candidates for v3.6.8+ on their own subline. Future scope expansion follows the same artifact-as-contract structure but is not a Step 6 deliverable. |
| Q2 | Execution model — where does audit run? Inline orchestrator dispatch (A), external hook script (B), sub-agent dispatch (C), or artifact-as-contract (D)? | **D — artifact-as-contract.** Orchestrator does not execute codex; it verifies that an audit artifact exists in the passport, that it passes Layer 2 + Layer 3 anti-fake-audit checks, and reads its verdict. Audit execution is a deployment concern. | §4 specifies the wrapper script contract; §5 specifies the orchestrator block protocol. The orchestrator agent prompt grows by one new "Audit Artifact Gate" subsection (§5.6) and does not internalize codex CLI semantics. Token cost of audit becomes a deployment-side operational cost, not a per-pipeline-run LLM cost. |
| Q3 | Anti-fake-audit guard — how does the orchestrator detect a forged audit artifact? Existence check only (Layer 1), JSONL schema (Layer 2), sidecar metadata (Layer 3), user attestation (Layer 4), or cryptographic signing (Layer 5)? | **Layer 2 + Layer 3 + partial inversion.** Layer 2 validates codex 0.125+ `--json` event-stream shape (opens with `thread.started` + `turn.started`; closes with `turn.completed` carrying non-zero `usage` integers; the body interleaves `item.completed` `agent_message` events — codex thinking aloud and the final verdict — with `item.started` / `item.completed` pairs for any tool calls, in arbitrary order; canonical UUID `thread_id`; parseable verdict text in the **last** `agent_message` `item.completed` per audit template Section 6 — see §3.3 for the full schema, the tool-call event pair, and §3.7 family A row A7 for the stream-shape pairing invariant). Layer 3 validates a sidecar `<run_id>.meta.json` written by the wrapper script (CLI version, hostname, cwd, git SHA, timestamps, exit code, `jsonl_thread_id` matching the JSONL stream's `thread.started` event). Partial inversion: agent prompts retain the "DO NOT simulate any audit step" prohibition but remove sentences that reveal the audit pipeline exists downstream (e.g., "The orchestrator runs codex audit afterward" — those sentences trigger Pattern C3 sub-agent fake-audit hallucination per `feedback_subagent_tool_hallucination.md`). | §5.2 specifies the eleven gating verification checks (4 Layer 2 gates from L2-2/L2-3/L2-4/L2-5 + 7 Layer 3 gates from L3-2 through L3-8); two precondition slots L2-1/L3-1 are file/schema existence checks reported as "audit not conducted" rather than gating failures, so they are not counted in the eleven. §6 specifies the partial inversion sweep across the three downstream agent prompts. Layer 4 (user attestation) was rejected as violating the "automatic audit" goal; Layer 5 (signing) was rejected as over-engineering relative to the threat model. Two independent failure modes (Layer 2 + Layer 3) raise forgery cost to the point where running real codex is the economical path under the §1.2 threat model. |
| Q4 | Relation to v3.6.6 + Step 8 fixture shape. Is v3.6.6 generator/evaluator contract the same axis as Step 6 audit, and does Step 8 use single corpus (A), per-pattern micro-fixtures (B), or hybrid (C)? | **Orthogonal + Hybrid (C).** v3.6.6 (`evaluator_full` Schema 13.1 contract) is in-pipeline LLM self-discipline at the writer/evaluator pair; Step 6 audit is cross-model external codex verification at the deliverable boundary. They run in parallel: a deliverable can carry both an `evaluator_full` contract and an `audit_artifact` entry. Step 8 fixture: 18 per-pattern micro-fixtures + 1 chapter-level integration fixture. | §8 records the orthogonality with a one-paragraph distinction and an explicit "do not merge" non-goal. §7 specifies both fixture tiers; §7.6 wires CI to run unit-level + integration-level test scripts separately. The 18 micro-fixtures align with the existing 29-mutation lint suite's unit philosophy already shipping in v3.6.7 Step 1+2. |

### 2.2 Architecture choice (Approach 1–3)

After Q1–Q4 settled the axes, the runtime model still had three plausible shapes. The block-or-warn axis is load-bearing: it determines whether v3.6.7's "ship-quality target" goal has runtime teeth or is only an aspiration.

| # | Approach | Block-or-warn | Decision |
|---|----------|---------------|----------|
| 1 | **Strict Block** | Orchestrator refuses stage transition without a passing audit artifact. MATERIAL verdict blocks; PASS proceeds; MINOR (≤3 P3) escalates to user. | **Selected.** |
| 2 | Soft Warn | Orchestrator displays audit verdict in checkpoint but allows user to proceed regardless. | Rejected — anti-fake-audit guard has no teeth without a block; "ship-quality 0 P1+P2" goal becomes display-only. |
| 3 | Tiered (high blast radius blocks; low blast radius warns) | User-configurable tier. | Rejected as YAGNI — Q1 fixed trigger to three high-blast-radius agents; no Tier B caller exists today. Reopen if v3.6.8+ adds low-stakes triggers. |

Strict Block is the only approach where Layer 2 + Layer 3 verification cost (Q3) is recovered. Soft Warn is internally inconsistent: spec §5.3 of the v3.6.7 main spec mandates anti-fake-audit verification, which is meaningless if the verification result does not gate progression. Tiered would be a future-proofing choice without a current Tier B consumer; revisit only when a low-blast-radius trigger is actually added.

### 2.3 Deferred questions

These were raised during brainstorm or scope check but settling them needs schema or wrapper detail in §3–§7. Resolved in §9 as risks/open questions.

| # | Open question | Lands in |
|---|---------------|----------|
| L1 | Round upper bound — does Strict Block cap at 3 rounds (matches audit template Section 1 default `target_rounds`) or 5 rounds (matches `feedback_codex_iterative_spec_review_to_zero.md` "iterate to one zero-finding round" guidance)? Both are defensible. | §5.4 |
| L2 | Partial inversion sweep completeness — is the inversion rule applied only to the three v3.6.7 agents (Q1 scope) or across all ARS agent prompts that mention audit? Wider sweep is safer but is scope creep against Q1. | §6.3 |
| L3 | ARS_PASSPORT_RESET interaction — when a stage's audit artifact lives in passport at session A and the user resumes in session B, must session B re-verify the artifact or trust the passport? | §9 R4 |
| L4 | Wrapper script deployment friction — strict block means a user without the wrapper script installed cannot ship. How discoverable should this gate be? | §9 R1 |

---

## 3. Schema additions

Step 6 introduces one Schema 9 optional field plus four new standalone schemas under `shared/contracts/` (entry, JSONL, sidecar, verdict). None of the existing schemas (Schema 9 base shape, Schema 13/13.1, `literature_corpus_entry.schema.json`, `reset_ledger_entry.schema.json`) is modified — every change is additive.

### 3.1 Schema 9 `audit_artifact[]` field (new optional)

`shared/handoff_schemas.md` Schema 9 (Material Passport) gains one optional append-friendly field. Each entry records one audit run for one downstream agent's deliverable at one stage transition.

```yaml
audit_artifact:                            # optional, added v3.6.7 Step 6
  - stage: 2                               # pipeline stage at which audit fired
    agent: synthesis_agent                 # one of three v3.6.7 agents
    deliverable_path: chapter_4/synthesis.md
    deliverable_sha: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2  # SHA-256 of deliverable file at audit time (full 64-hex per audit_artifact_entry.schema.json regex)
    run_id: 2026-04-30T15-22-04Z-d8f3      # human-sortable run identifier
    bundle_id: phase2-chapter4-2026-04-30  # optional, links to other entries in same logical bundle
    bundle_manifest_sha: 9a8b7c6d5e4f3b2a1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9876  # SHA-256 over manifest of primary + supporting + template files (full 64-hex per schema regex)
    artifact_paths:
      jsonl: audit_artifacts/2026-04-30T15-22-04Z-d8f3.jsonl
      sidecar: audit_artifacts/2026-04-30T15-22-04Z-d8f3.meta.json
      verdict: audit_artifacts/2026-04-30T15-22-04Z-d8f3.verdict.yaml
    verdict:                               # parsed from verdict.yaml; mirrored here for fast reads
      status: MINOR                         # persisted enum: PASS | MINOR | MATERIAL (AUDIT_FAILED is proposal-arm only — see §3.2 Lifecycle-conditional fields). This example shows MINOR because p3=1; PASS requires all-zero per §3.2 cross-field rule
      round: 2                             # which audit round produced this verdict
      target_rounds: 3                     # cap; round must be <= target_rounds
      finding_counts:
        p1: 0
        p2: 0
        p3: 1
      verified_at: "2026-04-30T15:23:11.847Z"  # when orchestrator verified Layer 2+3 passed (persisted entry only); RFC 3339 UTC string, ms precision per §3.2 cross-section consistency rule (quoted in YAML so the schema's `string` + `rfc3339_ms_utc` regex match — unquoted ISO 8601 parses as a YAML datetime object and would fail the schema's `type: string` check)
      verified_by: pipeline_orchestrator_agent
```

This example shows a **persisted** entry (verified_at / verified_by present). Proposal entries emitted by the wrapper are structurally identical but omit verified_at / verified_by; see §4.9 lifecycle and §3.2 schema oneOf for the proposal-vs-persisted distinction. Schema 9 only ever stores persisted entries; orchestrator validates passport-side `audit_artifact[]` entries with `--mode persisted` (proposal-mode entries in passport are treated as malformed and rejected by lint).

**Field semantics:**

- `stage` is the integer **destination stage** the just-completed deliverable is about to enter (per §5.1 destination-stage convention). v3.6.7 hooks emit `stage: 2` for `synthesis_agent` exit (gate fires before Stage 1→2 transition), `stage: 2` for `research_architect_agent` survey-designer exit (gate fires before the survey instrument enters Material Passport at the Stage 2 boundary), and `stage: 5` for `report_compiler_agent` abstract-only exit (gate fires before Stage 5 FINALIZE format conversion). The canonical destination-stage table lives in §5.1.
- `agent` is one of `synthesis_agent | research_architect_agent | report_compiler_agent`. Other agent names are reserved for future versions and rejected by Schema 9 lint.
- `deliverable_sha` is the SHA-256 of the deliverable file at the moment audit was dispatched. Used by orchestrator to detect post-audit deliverable mutation (audit pass on file X, then file X edited, then ship attempt — orchestrator must reject and require re-audit).
- `run_id` is the canonical handle the wrapper script (§4) emits. Format: `<ISO-8601-Z>-<4-hex-suffix>`. The suffix is required to disambiguate runs at sub-second timestamp resolution.
- `artifact_paths.jsonl / sidecar / verdict` are repo-relative paths to the three artifact files. They are co-located by run_id (same prefix); sidecar and verdict are written atomically via tmp-file-rename per §4.4, while JSONL is streamed by codex CLI directly to its final path (intentionally non-atomic — see §4.4 atomicity guarantee for why; the proposal-last lifecycle rule ensures orchestrator never observes JSONL mid-write). Missing any of the three is treated as audit-not-conducted. The fourth file the wrapper produces, `<run_id>.audit_artifact_entry.json` (the proposal entry consumed by the §4.9 lifecycle), is NOT recorded under `artifact_paths` because the entry IS the proposal once orchestrator has merged it; pointing at the proposal file from inside the persisted entry would create a self-reference loop.
- `verdict` is mirrored from the verdict file for fast read. Source of truth is `verdict.yaml`; if mirror disagrees with file, file wins (lint catches drift).

**Append-friendly semantics:**

- Multiple `audit_artifact[]` entries for the same `(stage, agent, deliverable_sha)` tuple ARE allowed — they represent multiple audit rounds. Orchestrator reads the latest entry by `verified_at` for verdict.
- If `deliverable_sha` changes (deliverable mutated), prior entries become stale but are NOT deleted — they remain as audit history. Orchestrator only accepts entries whose `deliverable_sha` matches the current deliverable.
- This mirrors the v3.6.3 `reset_boundary[]` append-only ledger pattern: history is preserved, freshness is computed.

### 3.2 `shared/contracts/passport/audit_artifact_entry.schema.json` (new)

Standalone schema for one `audit_artifact[]` entry. Referenced from Schema 9 via `$ref`. JSON Schema draft 2020-12.

The schema describes **two lifecycle states** for the same logical entry:

- **`proposal` state** — emitted by the wrapper script (§4.9) at audit completion, before orchestrator verification. `verdict.verified_at` and `verdict.verified_by` MUST be absent; presence is treated as malformed (Pattern C3 attack surface).
- **`persisted` state** — appended to passport `audit_artifact[]` by the orchestrator after the eleven gating checks (§5.2) pass. `verdict.verified_at` and `verdict.verified_by` are now required and filled by the orchestrator.

Both states are validated against the same schema file via JSON Schema `oneOf`. This mirrors the v3.6.6 spec §3.3 D1 `allOf if mode startsWith reviewer_` conditional pattern: one schema, lifecycle-dependent constraints, idiomatic for state-machine entities.

**Common fields (required in both states):**

| Field | Type | Constraint |
|---|---|---|
| `stage` | integer | `1 <= stage <= 6` |
| `agent` | string | enum: `["synthesis_agent", "research_architect_agent", "report_compiler_agent"]` |
| `deliverable_path` | string | repo-relative POSIX path (no `..`, no leading `/`) |
| `deliverable_sha` | string | `^[a-f0-9]{64}$` (SHA-256 hex) |
| `run_id` | string | `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}Z-[0-9a-f]{4}$` |
| `bundle_manifest_sha` | string | `^[a-f0-9]{64}$`. SHA-256 over the canonical manifest of all bundle files (primary + supporting + template), per §3.6 freshness rule. |
| `artifact_paths.jsonl` | string | must end with `.jsonl` |
| `artifact_paths.sidecar` | string | must end with `.meta.json` |
| `artifact_paths.verdict` | string | must end with `.verdict.yaml` |
| `verdict.status` | string | enum in **proposal arm**: `["PASS", "MINOR", "MATERIAL", "AUDIT_FAILED"]`. Three completion states + AUDIT_FAILED for wrapper-side aborts (§4.6). AUDIT_FAILED proposals must pass schema validation in §5.6 Path B4 so Path B5 can short-circuit on them; rejecting AUDIT_FAILED at the schema layer would deadlock the failure-signaling channel. enum in **persisted arm**: `["PASS", "MINOR", "MATERIAL"]` (AUDIT_FAILED is excluded — see Lifecycle-conditional fields table below for the operational reason). Cross-field rule (lint-enforced) below limits AUDIT_FAILED to zero finding counts plus required `failure_reason`. |
| `verdict.failure_reason` | string | optional in proposal/persisted entries; required when `verdict.status == "AUDIT_FAILED"`, forbidden otherwise. One-line human-readable reason (matches §3.5 verdict file rule). |
| `verdict.round` | integer | `>= 1` |
| `verdict.target_rounds` | integer | `>= 1`, `>= verdict.round` (mirrors §3.5 verdict file `target_rounds` for cross-section consistency; resolves §5.4 cross-reference) |
| `verdict.finding_counts.{p1,p2,p3}` | integer | `>= 0` |
| `bundle_id` | string | optional; opaque tag shared by all entries that belong to one logical multi-file audit bundle (see §4.5). When present, MUST match the `bundle.bundle_id` value in the corresponding sidecar. |
| `acknowledgement` | object | optional; present only on persisted entries appended via §5.4 `ship_with_known_residue`. When present, MUST contain `finding_ids` (non-empty array of strings, each matching one `findings[].id` in the companion verdict file), `acknowledged_at` (RFC 3339 datetime, UTC, ms precision), and `acknowledged_by` (const: `"user"`). Forbidden in proposal entries (wrappers cannot acknowledge residue). See §5.4 escalation mechanics for how this field is populated and §3.7 family A row A4 + family B rows B8/B10 + family C row C3 for the full invariant set. |

**Lifecycle-conditional fields:**

| Field | `proposal` state | `persisted` state |
|---|---|---|
| `verdict.verified_at` | MUST be absent (`not.required`) | required; RFC 3339 datetime, UTC (`Z` suffix), millisecond precision (mirrors §3.4 sidecar `timing.*` precision so latest-by-`verified_at` ordering at §3.1 / §5.6 Path A has resolution ≥ 1 ms — see §5.4 acknowledgement append for the monotonic-bump rule that closes the residual same-millisecond tie) |
| `verdict.verified_by` | MUST be absent (`not.required`) | required; const: `"pipeline_orchestrator_agent"` |
| `verdict.status` | enum: `["PASS", "MINOR", "MATERIAL", "AUDIT_FAILED"]` | enum: `["PASS", "MINOR", "MATERIAL"]` (AUDIT_FAILED excluded) |

**Why persisted excludes AUDIT_FAILED:** AUDIT_FAILED is not an audit *result*; it is evidence that the audit boundary failed to produce a trustworthy verdict (codex aborted, JSONL truncated, network timeout, etc.). The passport is a ledger of **verified audit artifacts**, not a log of attempted audit executions. Letting AUDIT_FAILED entries persist would force every downstream consumer (§5.3 ship/block, §5.6 Path A latest-by-`verified_at` selection, future analytics) to reason about a fourth durable state that lifecycle prose says must not exist. Forensic clarity for failed audits is preserved by leaving the failed proposal file plus its sidecar / verdict / JSONL in `audit_artifacts/` (§4.9 step 9 also intentionally does not move AUDIT_FAILED proposal files into `consumed/`) and by surfacing `failure_reason` in the §5.6 block message. If a future ARS version needs durable forensic attempt history, the right shape is a separate `audit_attempt[]` ledger with weaker semantics, not overloading `audit_artifact[]`.

**JSON Schema sketch:**

```json
{
  "$id": "audit_artifact_entry.schema.json",
  "type": "object",
  "required": ["stage", "agent", "deliverable_path", "deliverable_sha", "run_id", "bundle_manifest_sha", "artifact_paths", "verdict"],
  "properties": { "...": "all common fields above" },
  "oneOf": [
    {
      "title": "proposal",
      "description": "Wrapper-emitted, pre-verification. acknowledgement is forbidden because wrappers cannot acknowledge residue — acknowledgement is exclusively orchestrator-written at §5.4 ship_with_known_residue.",
      "not": {
        "required": ["acknowledgement"]
      },
      "properties": {
        "verdict": {
          "type": "object",
          "not": {
            "anyOf": [
              {"required": ["verified_at"]},
              {"required": ["verified_by"]}
            ]
          }
        }
      }
    },
    {
      "title": "persisted",
      "description": "Orchestrator-merged, post-verification. AUDIT_FAILED excluded — see Lifecycle-conditional fields rationale.",
      "properties": {
        "verdict": {
          "type": "object",
          "required": ["verified_at", "verified_by"],
          "properties": {
            "status": {"enum": ["PASS", "MINOR", "MATERIAL"]}
          }
        }
      }
    }
  ]
}
```

Validators called from §4.9 step 4 (proposal validation) and §5.2 / §5.6 (persisted validation) accept a `--mode {proposal,persisted}` flag that selects the corresponding `oneOf` arm. Lint script `scripts/check_audit_artifact_consistency.py` (added in §10 Phase 6.3) reads the mode flag and dispatches accordingly.

**Cross-field rules (enforced by lint, not schema):** these are the entry-side per-artifact rules; see §3.7 family A for the authoritative cross-artifact index and §3.7 families B / C / D / E / F for rules that span entry plus other artifacts.

- `verdict.status == "PASS"` requires `verdict.finding_counts.{p1,p2,p3}` all zero AND `failure_reason` absent.
- `verdict.status == "MINOR"` requires `p1 == 0 AND p2 == 0 AND p3 <= 3` AND `failure_reason` absent.
- `verdict.status == "MATERIAL"` requires `p1 > 0 OR p2 > 0 OR p3 > 3` AND `failure_reason` absent.
- `verdict.status == "AUDIT_FAILED"` requires `p1 == 0 AND p2 == 0 AND p3 == 0` AND `failure_reason` is a non-empty one-line string. (See §3.5 + §4.6.) AUDIT_FAILED is reachable only in the proposal arm (per the Lifecycle-conditional fields table); a persisted entry carrying `status == "AUDIT_FAILED"` is rejected at `--mode persisted` schema validation.
- `verdict.round <= verdict.target_rounds` (lifecycle invariant; see §5.4 escalation mechanics).
- `acknowledgement` is allowed only when `verdict.status == "MATERIAL"` AND the entry is in the persisted arm (proposal arm forbids acknowledgement entirely per the JSON Schema sketch). A persisted entry carrying `acknowledgement` with `verdict.status` of `PASS` / `MINOR` is rejected at `--mode persisted` validation. This closes the hand-edit attack surface where someone manually adds an `acknowledgement` block to a non-MATERIAL persisted entry to claim user residue acknowledgement that was never solicited (the §5.4 prompt only fires on round-3 MATERIAL).

These rules live in `scripts/check_audit_artifact_consistency.py`.

### 3.3 `shared/contracts/audit/audit_jsonl.schema.json` (new — Layer 2)

Schema for the codex CLI JSONL output that the wrapper script produces. This is the **Layer 2** anti-fake-audit check from Q3: orchestrator validates the JSONL against this schema before reading any verdict.

**Codex 0.125+ `--json` event-stream shape (load-bearing).** Codex 0.125+ `--json` emits a typed event stream over stdout (verified compatible across 0.125 through 0.128): each line is a JSON object with a `type` field naming one of `thread.started`, `turn.started`, `item.started`, `item.completed`, `turn.completed`, or `error`. There is no per-row `model` field, no per-row `reasoning_effort` field, no `session_id` field, no `final_message` field, and no per-row `usage` field — those names belonged to a pre-0.125 draft and are retired here. The stable run identifier is `thread_id` carried on the opening `thread.started` event; `usage` lands on the closing `turn.completed`; the assistant verdict text lands inside an `item.completed` event whose `item.type == "agent_message"` and `item.text` carries the structured verdict (severity-bucket count summary per audit template Section 6).

**Tool-call events.** Whenever codex invokes a tool during the run (a `git diff`, a file read, etc.), the stream emits an `item.started` event when the tool call begins and a matching `item.completed` event when it returns. Both events carry an `item` block whose `item.type` names the tool kind (`command_execution`, `file_change`, etc.) — neither is an `agent_message`, so neither participates in verdict extraction. The audit prompt at `shared/templates/codex_audit_multifile_template.md` typically reads bundle files via tools, so most real audits emit at least one `item.started` / `item.completed` pair before the final `agent_message`; the no-tool case is reachable but rare (e.g., codex deciding the bundle context already in the prompt is sufficient and answering directly). L2-5 enforces only the pairing invariant — every observed `item.started` is matched 1:1 by a later `item.completed` sharing the same `item.id` (parallel tool starts complete in any order, see the schema-rule paragraph below) — not a minimum tool count, because requiring ≥1 tool pair would over-scope the anti-fake-audit guard (Q3 minimal-Layer-2 surface) and reject legitimate no-tool audits. Pre-0.125 drafts that enumerated only four events were wrong about the wire format; PR #52 round-4 surfaced the omission via empirical capture of `codex exec --json` against a live tool-using run.

A canonical no-tool run emits four events in order — this is the "minimum" pre-0.125 drafts described, and L2-4 validates against this minimum (the no-tool case is rare in practice but legitimate, per the preceding paragraph; the next paragraph shows the typical tool-using shape):

```
{"type":"thread.started","thread_id":"019de371-4c13-7521-8af7-fccf6bd23279"}
{"type":"turn.started"}
{"type":"item.completed","item":{"id":"item_0","type":"agent_message","text":"<verdict text>"}}
{"type":"turn.completed","usage":{"input_tokens":...,"cached_input_tokens":...,"output_tokens":...,"reasoning_output_tokens":...}}
```

A canonical tool-using run (the actual audit shape, since the audit template requires file reads) interleaves `item.started` / `item.completed` pairs around the assistant message:

```
{"type":"thread.started","thread_id":"019de371-4c13-7521-8af7-fccf6bd23279"}
{"type":"turn.started"}
{"type":"item.completed","item":{"id":"item_0","type":"agent_message","text":"<intermediate response>"}}
{"type":"item.started","item":{"id":"item_1","type":"command_execution"}}
{"type":"item.completed","item":{"id":"item_1","type":"command_execution"}}
{"type":"item.completed","item":{"id":"item_2","type":"agent_message","text":"<final verdict text>"}}
{"type":"turn.completed","usage":{"input_tokens":...,"cached_input_tokens":...,"output_tokens":...,"reasoning_output_tokens":...}}
```

Schema validates each event row by `type`. Required fields per event:

| Event `type` | Required additional fields | Constraint |
|---|---|---|
| `thread.started` | `thread_id` (string, UUID) | canonical `^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$` (8-4-4-4-12 layout — `^[0-9a-f-]{36}$` was too loose; 36 dashes or hex without separators would have passed) |
| `turn.started` | (none additional) | |
| `item.started` | `item.id`, `item.type` | tool-call begin marker (`command_execution`, `file_change`, etc.); carries no `text`; the matching `item.completed` also carries no `text` (only `agent_message` `item.completed` events carry `text`); does not participate in verdict extraction |
| `item.completed` | `item.id`, `item.type`, `item.text` (when `item.type == "agent_message"`) | `item.text` non-empty for agent_message items; non-agent_message completions (e.g. `command_execution`) carry no `text` |
| `turn.completed` | `usage.input_tokens`, `usage.cached_input_tokens`, `usage.output_tokens`, `usage.reasoning_output_tokens` (all integers) | each `>= 0`; `usage.input_tokens > 0` for non-trivial runs |
| `error` | `error.message` (string) | only present on failed runs; companion verdict MUST be `AUDIT_FAILED` |

Schema-level rules:

- The first event in the stream has `type == "thread.started"` and carries the run's `thread_id`. All subsequent events SHOULD NOT redeclare `thread_id` (codex emits it once at stream open).
- A clean run ends with `turn.completed`. A failed run may end with `error` (or be truncated by SIGKILL — see §4.4 Step 2a JSONL placeholder).
- The **last** `agent_message` `item.completed` event in the stream carries the verdict text. Tool-using runs may emit intermediate `agent_message` events between tool-call `item.started` / `item.completed` pairs (codex thinking aloud); the verdict-bearing event is always the last `agent_message` `item.completed`, but it is NOT the final stream event — `turn.completed` (carrying `usage`) is always emitted after it as the closing event. The wrapper extracts this via `parse_audit_verdict.py` (§4.4 Step 4); the verdict text format is contracted by `shared/templates/codex_audit_multifile_template.md` Section 6 (severity-bucket count summary), NOT by this schema. (Pre-PR-#52 drafts said "exactly one" `agent_message`; that was correct for the no-tool minimum but rejected the actual tool-using audit shape.)
- `item.started` events appear only in tool-using runs and pair 1:1 with later `item.completed` events sharing the same `item.id`. Codex may start multiple tools concurrently (e.g., `item_1`, `item_2`, `item_3` start in that order) and complete them in any order (e.g., `item_1`, `item_3`, `item_2`); pairing is by `item.id` only, not by completion-order FIFO. They are evidence that codex actually invoked tools (anti-fake-audit signal); verdict logic ignores them. **Pairing is a stream-level invariant, not a per-row schema rule** — Layer 2 (`audit_jsonl.schema.json`) validates each row's shape and §5.2 L2-3/L2-4 cover the canonical opening / closing / final-`agent_message` slots; the 1:1 `item.started` ↔ `item.completed` pairing check is enumerated in §3.7 family A row A7 and enforced by `scripts/check_audit_artifact_consistency.py` (Phase 6.3). Tool-event pairing was added to the canonical wire-format description here so implementers know the shape, but the gating burden stays per-row at Layer 2 by design (Q3 chose minimal Layer 2 surface; stream-level is Phase 6.3 territory). The §3.7 row makes the rule discoverable to the lint-script author without re-reading §3.3 prose.
- Model + reasoning effort enforcement is **invocation-side, not stream-side**: the wrapper invokes codex with `-m gpt-5.5 -c 'model_reasoning_effort="xhigh"'` per §4.4 Step 2b. There is no event-stream field that records these — they are properties of the CLI invocation captured in the sidecar's `prompt` block, not Layer 2 evidence per se. Layer 3 therefore cannot cross-check the stream against `model = "gpt-5.5"`; this is a known limit of the 0.125+ `--json` shape and is captured in §9.1 R2 motivated-forgery boundary (a forger with shell access could invoke codex with a different model and the JSONL alone would not betray them; deployment-side discipline per §3.7 E9 is the defense).

**Why these specific fields:** they are the events codex 0.125+ actually emits, validated for shape. A forger needs to fabricate a canonical UUID `thread_id` (8-4-4-4-12 layout), the canonical event ordering (with tool-call pairs if claiming a tool-using audit), `usage` integers on `turn.completed`, AND a syntactically-valid final `item.completed.item.text` `agent_message` that passes `parse_audit_verdict.py` (which itself enforces audit-template Section 6 schema). Layer 2 alone does not guarantee genuineness, but it raises the floor — `echo '{}' >> fake.jsonl` no longer passes; the canonical event sequence is the minimum forgery surface.

**`parse_audit_verdict.py` contract** (Phase 6.1 deliverable per §10): reads the JSONL stream, extracts the **last** `item.completed` event whose `item.type == "agent_message"` (intermediate `agent_message` events from codex thinking aloud between tool calls are skipped), and converts the audit-template Section 6 structured text into the `<run_id>.verdict.yaml` shape (§3.5). On parse failure (no agent_message event at all, malformed Section 6 text in the final agent_message, etc.), emits AUDIT_FAILED verdict with `failure_reason: "JSONL parse error: <reason>"` per §4.6 case (b). The wrapper invokes parser with `--probe` first to validate the JSONL has parseable shape; absence of parseable shape triggers the AUDIT_FAILED branch in §4.4 Step 4.

### 3.4 `shared/contracts/audit/audit_sidecar.schema.json` (new — Layer 3)

Schema for the sidecar metadata file. This is the **Layer 3** anti-fake-audit check: forging requires fabricating both the JSONL (Layer 2) AND a self-consistent sidecar.

```yaml
# <run_id>.meta.json structure (validated by Layer 3 schema)
run_id: 2026-04-30T15-22-04Z-d8f3
codex_cli_version: 0.128.0                 # from `codex --version`
runner:
  hostname: runner.example.local            # `uname -n`
  cwd: /path/to/academic-research-skills
  git_sha: b4fbffd                          # repo HEAD at audit start
  git_dirty: false                          # uncommitted changes flag
timing:
  started_at: "2026-04-30T15:22:04.123Z"
  ended_at: "2026-04-30T15:22:58.471Z"
  duration_seconds: 54.348
process:
  exit_code: 0
  stdout_path: audit_artifacts/2026-04-30T15-22-04Z-d8f3.stdout
  stderr_path: audit_artifacts/2026-04-30T15-22-04Z-d8f3.stderr
stream:
  jsonl_thread_id: 019de371-4c13-7521-8af7-fccf6bd23279    # MUST match the JSONL's `thread.started` event's `thread_id`
prompt:
  audit_template_path: shared/templates/codex_audit_multifile_template.md
  audit_template_sha: 7f4a8b2c3d5e6f1a9b0c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a
  bundle:
    bundle_id: phase2-chapter4-2026-04-30      # optional, opaque tag tying multi-file bundle entries
    bundle_manifest_sha: 9a8b7c6d5e4f3b2a1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9876
    primary_deliverables:
      - path: chapter_4/synthesis.md
        sha: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
    supporting_context:
      - path: chapter_4/bibliography.json
        sha: e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6
      - path: chapter_4/verification.md
        sha: c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3
```

Required field constraints:

| Field | Constraint |
|---|---|
| `run_id` | identical to file basename |
| `codex_cli_version` | semver `^[0-9]+\.[0-9]+\.[0-9]+$` |
| `runner.git_sha` | `^[a-f0-9]{7,40}$` |
| `timing.started_at`, `ended_at` | RFC 3339 with millisecond precision |
| `timing.duration_seconds` | `> 0`, must equal `ended_at - started_at` (lint check) |
| `process.exit_code` | integer, `0` for accepted artifact (non-zero rejected by orchestrator) |
| `stream.jsonl_thread_id` | UUID format AND MUST match the JSONL's single `thread.started` event's `thread_id` field (cross-file lint) WHEN the companion verdict's `status != "AUDIT_FAILED"`. WHEN `status == "AUDIT_FAILED"`, `jsonl_thread_id` is allowed to be `""` (empty string) because no usable JSONL thread exists; the UUID format constraint and cross-file rule 1 are both suspended for AUDIT_FAILED entries. Schema expresses this via JSON Schema conditional (`if/then` keyed on the companion verdict's `status`, resolved by Layer 3 lint when the two files are co-validated). Any other absence (missing key, null, non-string) is malformed regardless of verdict status. |
| `prompt.audit_template_path` | const `"shared/templates/codex_audit_multifile_template.md"` for v3.6.7 |
| `prompt.audit_template_sha` | SHA-256 of the template file as of audit time |
| `prompt.bundle.primary_deliverables[].sha` | MUST match `audit_artifact_entry.deliverable_sha` |

**Cross-file rules (Layer 3 verification):** these are the sidecar-anchored rules; see §3.7 family B for the full cross-artifact index (B1–B6 mirror rules 1–6 below; B7 mirrors rule 7 below; B8–B10 cover the acknowledgement / bundle_id / finding_ids rules that live elsewhere in §3 but apply to the same Layer 3 boundary).

The cross-file rules below apply **only when the companion verdict's `status != "AUDIT_FAILED"`**. AUDIT_FAILED entries short-circuit at orchestrator §5.6 Path B5 before Layer 3 verification runs and are not subject to rules 1–7. The sidecar still gets written for AUDIT_FAILED runs (per §4.6) so that postmortem tooling can read runner / timing / exit_code, but the orchestrator does not feed those entries through Layer 3.

1. `stream.jsonl_thread_id` matches the JSONL stream's single `thread.started` event's `thread_id`. (Suspended for AUDIT_FAILED — `jsonl_thread_id` may be `""` per the field constraint above.)
2. `prompt.bundle.primary_deliverables[].sha` matches the corresponding `audit_artifact_entry.deliverable_sha` AND matches the current SHA-256 of that file at verification time.
3. `prompt.bundle.bundle_manifest_sha` (per §3.6) matches the current bundle manifest computed from the union of `primary_deliverables[]`, `supporting_context[]`, and the audit template (`prompt.audit_template_path` + `prompt.audit_template_sha`).
4. `runner.git_sha` is a valid commit in the current repo (not a fabricated hash).
5. `timing.ended_at - timing.started_at == duration_seconds` within ±1 second tolerance.
6. `process.exit_code == 0`. A non-zero exit code means audit was attempted but failed; the sidecar still gets written (per §4.6) for postmortem, but the companion verdict for any non-zero-exit run MUST be `AUDIT_FAILED`, and orchestrator MUST reject any non-AUDIT_FAILED audit_artifact whose sidecar carries non-zero exit_code (defense in depth against a forger pairing exit_code != 0 with a fabricated PASS/MINOR/MATERIAL verdict).
7. `sidecar.run_id` equals the bare `<run_id>` basename of the sidecar file itself AND the bare `<run_id>` basename of every co-located artifact file (jsonl, verdict, plus the proposal entry file when observed at Path B before merge). The set of co-located artifacts differs by lifecycle — four files in proposal mode (jsonl + sidecar + verdict + proposal entry), three in persisted mode (proposal entry consumed at §4.9 step 9 and not recorded under `artifact_paths`); all co-located artifacts in the current lifecycle mode share one canonical bare `<run_id>` stem per §3.7 family F (F2/F3) — closes the "swap one co-located artifact for a different run's file" forgery seam (§3.7 family B row B7 carries the cross-artifact statement; this rule is the §3.4 sidecar-anchored half).

These seven cross-file checks are the Layer 3 contribution beyond Layer 2's per-event schema. A forger needs to: produce a syntactically-valid JSONL stream that opens with `thread.started` + `turn.started`, closes with `turn.completed`, and interleaves `agent_message` `item.completed` events with any claimed tool-call `item.started` / `item.completed` pairs (matched by `item.id`; parallel tool starts may complete in any order) per §3.3 (Layer 2), produce a sidecar whose `jsonl_thread_id` matches the `thread.started` event's `thread_id` (rule 1), pin the deliverable SHA AND the live file SHA (rule 2), compute and pin the bundle manifest SHA correctly across all files (rule 3), use a real repo commit (rule 4), keep timestamps arithmetically self-consistent (rule 5), ensure exit_code is 0 (rule 6), AND keep `sidecar.run_id` consistent with the basename of every co-located artifact file in the current lifecycle mode (rule 7 — defeats per-file forgery by binding all co-located artifacts to one identifier; four files in proposal mode, three in persisted mode). Layer 2 + Layer 3 raise forgery cost to a level where running the real codex CLI is the economical path; this is sufficient against the threat model declared in §1.2 (Pattern C3 inadvertent over-claims), and known-insufficient against motivated forgery (the boundary discussed at §1.2 closing paragraph; §9.1 R2 carries the full risk write-up).

### 3.5 `shared/contracts/audit/audit_verdict.schema.json` (new — verdict file)

Schema for the human-readable verdict file produced by the wrapper after parsing the JSONL stream's final `item.completed` event whose `item.type == "agent_message"` (per §3.3 event-stream contract — tool-using runs may interleave intermediate `agent_message` events between tool-call `item.started` / `item.completed` pairs; only the last such event is verdict-bearing). This is what the orchestrator reads for verdict status; the JSONL itself is treated as raw evidence for Layer 2 only, never directly parsed for verdict logic.

```yaml
# <run_id>.verdict.yaml — clean-completion shape (status PASS / MINOR / MATERIAL)
run_id: 2026-04-30T15-22-04Z-d8f3
verdict_status: MINOR                         # one of PASS | MINOR | MATERIAL | AUDIT_FAILED
round: 2
target_rounds: 3
finding_counts:
  p1: 0
  p2: 0
  p3: 1
findings:
  - id: F-007
    severity: P3
    dimension: "3.7"                        # string enum value; one of audit-template §3.1-§3.7 or "4(f)"
    file: chapter_4/synthesis.md
    line: 482
    description: "deictic temporal phrase 'currently' on reflexivity disclosure"
    suggested_fix: "replace with 'as of 2026-04-30' or 'former director'"
generated_at: "2026-04-30T15:22:58.471Z"
generated_by: scripts/run_codex_audit.sh
generator_version: 1.0.0                    # wrapper script semver
```

Required:

- `verdict_status` enum: `["PASS", "MINOR", "MATERIAL", "AUDIT_FAILED"]`. The fourth value `AUDIT_FAILED` exists for wrapper failure signaling per §4.6; semantics are "audit aborted, not completed", distinct from PASS/MINOR/MATERIAL (which all signify completed audit). Orchestrator BLOCKs on `AUDIT_FAILED` without running gating checks (per §5.6 Path B5).
- `verdict_status` consistent with `finding_counts` per §3.2 cross-field rules. `AUDIT_FAILED` requires `finding_counts.{p1,p2,p3} == 0` AND `failure_reason` set.
- `failure_reason` (string, one line): required when `verdict_status == "AUDIT_FAILED"`, forbidden otherwise. Human-readable reason ("codex exit 70: network timeout", "JSONL parse error at row 47").
- `findings[].severity` enum `["P1", "P2", "P3"]`
- `findings[].dimension` enum: `["3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "4(f)"]` matching audit template
- `round <= target_rounds`

**Cross-field rule — `finding_counts` MUST agree with `findings[]`** (verdict-file rule per §3.7 family A row A5; load-bearing for §5.3 ship/block decisions; lint-enforced):

- `finding_counts.p1 == count(findings[severity == "P1"])`
- `finding_counts.p2 == count(findings[severity == "P2"])`
- `finding_counts.p3 == count(findings[severity == "P3"])`
- When `verdict_status == "AUDIT_FAILED"`, `findings` MUST be `[]` (matches `finding_counts.{p1,p2,p3} == 0` from the AUDIT_FAILED rule above; the empty list is the canonical representation, not a rule about absence).

Without this invariant a verdict file could declare `finding_counts: {p1: 0, p2: 0, p3: 0}` while `findings[]` lists three P1 entries (or vice versa), and §5.3 ship/block decisions — which read `finding_counts` only — would silently disagree with the human-readable findings list. The invariant lives on the verdict file itself (the only artifact carrying `findings[]`); Schema 9 `audit_artifact[].verdict` is a counts-only mirror and is not in scope for this rule. Lint enforcement closes this gap on every wrapper-emitted verdict file; orchestrator §5.6 Path B verification re-runs the rule against the on-disk verdict file before merging the proposal entry into the passport.

**AUDIT_FAILED variant** (per §4.6 wrapper failure modes):

```yaml
# <run_id>.verdict.yaml — failure-mode shape (status AUDIT_FAILED)
run_id: 2026-04-30T15-22-04Z-d8f3
verdict_status: AUDIT_FAILED
round: 2
target_rounds: 3
finding_counts:
  p1: 0
  p2: 0
  p3: 0
failure_reason: "codex exit 70: network timeout after 600s"
findings: []
generated_at: "2026-04-30T15:22:58.471Z"
generated_by: scripts/run_codex_audit.sh
generator_version: 1.0.0
```

Both shapes share the same schema; the difference is `verdict_status` plus the `failure_reason` cross-field rule. Orchestrator §5.6 Path B5 short-circuits on `AUDIT_FAILED` without running the eleven gating checks.

The verdict file is the artifact orchestrator parses to make ship/block decisions. JSONL serves only as evidence that codex actually ran (Layer 2); sidecar serves as evidence that the runtime environment was real (Layer 3); verdict is the policy surface.

### 3.6 Bundle manifest hash (deliverable freshness extension)

`deliverable_sha` (§3.1) detects mutation of the **primary** deliverable only. A multi-file audit bundle (§4.5) typically also depends on supporting context (`bibliography.json`, `verification.md`, prior-round verdict, etc.). If any of those files change between audit time and ship time, the audit becomes stale even though `deliverable_sha` matches.

To close this gap, the wrapper computes a `bundle_manifest_sha` covering every file the audit prompt references — primary deliverable plus all `--supporting` paths plus the audit template itself.

**Manifest format (deterministic, line-oriented):**

```
<role>:<repo-relative-path>:<sha256-hex>
```

One line per file. Roles: `primary` | `supporting` | `template`. Sort lines lexicographically by `(role, path)` for determinism. SHA-256 over the manifest text (UTF-8, LF line separator, trailing LF) is `bundle_manifest_sha`.

**Example manifest text:**

```
primary:chapter_4/synthesis.md:a1b2c3d4...
supporting:chapter_4/bibliography.json:e5f6a7b8...
supporting:chapter_4/verification.md:c2d3e4f5...
template:shared/templates/codex_audit_multifile_template.md:9a8b7c6d...
```

**Where it lives:**

- Wrapper writes it to sidecar at `prompt.bundle.bundle_manifest_sha` (§3.4 amendment — see below).
- Wrapper writes it to `audit_artifact_entry.json` at `bundle_manifest_sha`.
- Orchestrator persists it in Schema 9 `audit_artifact[].bundle_manifest_sha` after verification.

**Freshness check (§5.2 will run this):** at stage transition, orchestrator recomputes the bundle manifest from current file contents (using the same `(role, path)` set the sidecar declares) and compares the resulting SHA-256 against the entry's `bundle_manifest_sha`. Mismatch on any path's SHA → manifest mismatch → audit stale → new audit round required.

**Why a manifest, not per-file SHA verification:** §5.2 stays a fixed-count check list (does not grow with bundle size); reproducibility check is one comparison per audit_artifact entry; humans can read the manifest text directly to debug staleness.

### 3.7 Schema invariants

Per consult Q1 + Q2: §3 describes four schemas (entry, JSONL, sidecar, verdict) plus a Schema 9 amendment, but the real object under specification is a **lifecycle state machine** spread across those four artifact files plus the passport. Local schema rules in §3.1–§3.5 describe each artifact's shape; this subsection lists the **cross-artifact invariants** in one authoritative place so reviewers can audit top-down. Without this index, an invariant that lives only in one schema's local rule (or only in §4 / §5 prose) is invisible to anyone reading another schema in isolation — the convergence trajectory across rounds 1–9 of this spec demonstrated the cost: each round surfaced new "rules that were never listed together" rather than re-finding the same issue.

The six tables below enumerate every invariant under one of six families. Each row carries: **ID** (stable handle for citation in lint scripts and review notes), **Rule** (the constraint), **Applies to** (which artifact files / passport state the rule covers), **Lifecycle states** (proposal / persisted / both / wrapper-only / orchestrator-only), **Enforcement point** (where the rule is checked at runtime), **Failure behavior** (what happens when it fails). All rules are also implemented in `scripts/check_audit_artifact_consistency.py` (added in §10 Phase 6.3); the table is the source of truth, the script is the executable mirror.

#### A. Per-artifact cross-field rules

Constraints that hold inside a single artifact file (no cross-file dependency).

| ID | Rule | Applies to | Lifecycle states | Enforcement point | Failure behavior |
|---|---|---|---|---|---|
| A1 | `verdict.status` enum agrees with `verdict.finding_counts.{p1,p2,p3}` per the four PASS / MINOR / MATERIAL / AUDIT_FAILED rules | entry, verdict file | both | lint at write time; `--mode {proposal,persisted}` re-check at orchestrator merge | malformed; rejected at the boundary that runs the validator |
| A2 | `verdict.failure_reason` required iff `verdict.status == "AUDIT_FAILED"` | entry, verdict file | both | lint at write time | malformed; rejected |
| A3 | `verdict.round <= verdict.target_rounds` | entry, verdict file | both | lint at write time; wrapper preflight on `--round`/`--target-rounds` (§4.2) | wrapper exits 64 EX_USAGE; lint rejects |
| A4 | `acknowledgement` allowed only when `verdict.status == "MATERIAL"` AND entry is in persisted arm; proposal arm forbids acknowledgement entirely (per JSON Schema sketch in §3.2) | entry | persisted only | `--mode persisted` schema validation; lint at acknowledgement-write time | rejected at validation boundary; orchestrator refuses to append the malformed entry |
| A5 | `verdict.finding_counts.pN == count(findings[severity == "PN"])` for N in {1,2,3} | verdict file (NOT entry — entry is a counts-only mirror per C1 below) | both | lint at wrapper write time; orchestrator §5.6 Path B re-check before passport merge | wrapper exits non-zero; orchestrator BLOCKs the merge |
| A6 | When `verdict.status == "AUDIT_FAILED"`, `findings == []` | verdict file | both | lint at wrapper write time | rejected |
| A7 | JSONL stream tool-event pairing — true 1:1 with start-before-completion order: for every `item.id` appearing on a non-`agent_message` `item.started` event, the stream contains **exactly one** `item.started` and **exactly one** `item.completed` event with that `item.id` (no duplicate starts, no duplicate completions), and the `item.completed` row index is strictly greater than the matching `item.started` row index (a tool completion never precedes its start). Equivalently: the multiset of non-`agent_message` `item.started` `item.id` values equals the multiset of non-`agent_message` `item.completed` `item.id` values; each `item.id` appears at most once in each; and for each id the completed-row-index exceeds the started-row-index. Matching is by `item.id` only — parallel tool starts may complete in any order (codex starts e.g. `item_1`, `item_2`, `item_3` then completes them in any permutation), but EACH id is paired exactly once and ordered start-before-completion. Orphan tool completions (a non-`agent_message` `item.completed` whose `item.id` never appeared earlier in an `item.started`) are rejected. **`agent_message` `item.completed` events are exempt from the prior-`item.started` requirement** — codex emits assistant messages as single completion events without an opening start, both for the final verdict and for intermediate "thinking aloud" responses between tool calls (per §3.3 canonical tool-using sequence); their `item.id` values are NOT counted in the multiset above. Stream-level invariant added to fill the L2-4 scope-defer (`audit_jsonl.schema.json` is per-row only; this is the only stream-shape rule that needs lint coverage in v3.6.7) | JSONL | both | `scripts/check_audit_artifact_consistency.py` (Phase 6.3) at orchestrator §5.2 read time | orchestrator BLOCKs with "audit fake-detected: tool event pairing violation: <details>" |

#### B. Cross-file rules (Layer 3 verification)

Constraints that span two or more of {entry, JSONL, sidecar, verdict file, on-disk source files}.

| ID | Rule | Applies to | Lifecycle states | Enforcement point | Failure behavior |
|---|---|---|---|---|---|
| B1 | `sidecar.stream.jsonl_thread_id` matches the JSONL stream's `thread.started` event's `thread_id` field (suspended when companion verdict's `status == "AUDIT_FAILED"` per §3.4 conditional) | sidecar, JSONL | both, plus AUDIT_FAILED suspension | §5.2 L3-2 gate check | orchestrator BLOCKs the merge with "audit fake-detected: jsonl_thread_id mismatch" |
| B2 | `sidecar.prompt.bundle.primary_deliverables[].sha == entry.deliverable_sha == current_file_SHA256(deliverable_path)` | sidecar, entry, on-disk deliverable file | both | §5.2 L3-3 gate check | orchestrator BLOCKs with "audit stale: deliverable mutated" or "audit fake-detected: sha mismatch" |
| B3 | `sidecar.prompt.bundle.bundle_manifest_sha == recomputed_bundle_manifest_sha` (recomputed per §3.6 over current SHA-256 of every primary + supporting + template file) | sidecar, on-disk bundle files | both | §5.2 L3-4 gate check | orchestrator BLOCKs with "audit stale: bundle file changed" or "audit fake-detected: manifest sha mismatch" |
| B4 | `sidecar.runner.git_sha` resolves to a real commit in the current repo | sidecar, repo `.git/` | both | §5.2 L3-5 gate check (`git cat-file -e <sha>^{commit}`) | orchestrator BLOCKs with "audit fake-detected: fabricated git_sha" |
| B5 | `sidecar.timing.ended_at - timing.started_at == duration_seconds` within ±1s | sidecar | both | §5.2 L3-6 gate check | orchestrator BLOCKs with "audit fake-detected: timing arithmetic" |
| B6 | `sidecar.process.exit_code == 0` for non-AUDIT_FAILED entries; non-zero exit_code permitted only when companion verdict's `status == "AUDIT_FAILED"` (per §3.4 rule 6 + F-027 conditional) | sidecar, verdict | both, plus AUDIT_FAILED conditional | §5.2 L3-7 gate check; AUDIT_FAILED suspension at §5.6 Path B5 short-circuit | orchestrator BLOCKs with "audit attempted but failed" or rejects forged non-AUDIT_FAILED + non-zero-exit pairing (a forger pairing exit_code != 0 with a fabricated PASS / MINOR / MATERIAL verdict) |
| B7 | `entry.run_id == sidecar.run_id` AND `sidecar.run_id` is identical to the bare `<run_id>` basename of every co-located artifact file. The set of co-located files differs by lifecycle: **proposal mode** = four files (`<run_id>.jsonl`, `<run_id>.meta.json`, `<run_id>.verdict.yaml`, `<run_id>.audit_artifact_entry.json`); **persisted mode** = three files (proposal entry file is consumed at §4.9 step 9 — moved to `consumed/` and not recorded under `artifact_paths`, see §3.1 closing note on why pointing at it would create a self-reference loop). One canonical filename convention throughout: bare `<run_id>` only, no stage / agent / deliverable prefix | sidecar (canonical source of `run_id`), entry, the three persisted artifact files plus the proposal entry file when in proposal mode | both, with lifecycle-asymmetric scope (4 files in proposal mode, 3 in persisted mode) | wrapper at write time uses `$run_id` for all paths (§4.4); §5.2 L3-1 precondition validates sidecar's own basename against its `run_id` field; §5.2 **L3-8** gating check cross-validates `entry.run_id == sidecar.run_id` AND the sidecar's `run_id` against the basenames of the three `artifact_paths` files (jsonl / sidecar / verdict) for both modes, plus the proposal entry file basename only when running on a Path B unmerged proposal (proposal-mode-only fourth check) — closes the "swap one artifact file for a different run's file" forgery seam | wrapper aborts with "internal: run_id mismatch"; orchestrator rejects at L3-1 (sidecar self-mismatch) or L3-8 (cross-file basename drift, including `entry.run_id` mismatch) with "audit fake-detected: artifact filename mismatch" |
| B8 | Persisted ack entries enforce `verdict.verified_at == acknowledgement.acknowledged_at` (the two timestamps share the same instant by construction per §5.4 strict-monotonic helper) | entry | persisted only | lint at acknowledgement-write time; §5.6 Path B persisted-mode re-check before passport merge | rejected at validation boundary |
| B9 | When `entry.bundle_id` is present, it equals `sidecar.prompt.bundle.bundle_id` | entry, sidecar | both | lint at wrapper write time | rejected |
| B10 | Persisted ack entry's `acknowledgement.finding_ids` satisfies all three: (1) **non-empty** array, (2) **every ID exists** in the companion verdict file's `findings[].id`, (3) **full coverage** — the set equals the set of every current `findings[].id` (no partial residue acknowledgement; rejected at write time, not at ship-decision time, so §5.3 "MATERIAL + acknowledgement" row never has to handle partial cases) | entry (acknowledgement block), verdict file (`findings[]`) | persisted only | lint at acknowledgement-write time (§5.4); §5.6 Path B persisted-mode re-check before passport merge | rejected at validation boundary; orchestrator surfaces "acknowledgement.finding_ids violates rule N" in the §5.6 BLOCK message |

#### C. Mirror rules (same field appearing in multiple artifacts)

The artifact-as-contract design (§2.2 Q2 = D) requires fields that appear in multiple files to agree. Each mirror row names the **source of truth** so disagreements have a deterministic resolution.

| ID | Rule | Source of truth | Mirror in | Enforcement point | Failure behavior |
|---|---|---|---|---|---|
| C1 | `entry.verdict.{status, round, target_rounds, finding_counts, failure_reason}` mirrors the verdict file's matching fields. On disagreement, **verdict file wins** (§3.1 line at "Source of truth is `verdict.yaml`") | verdict file (`<run_id>.verdict.yaml`) | passport entry's inline `verdict` block | lint at wrapper write time; orchestrator §5.6 Path A A5 drift check on persisted entries (mirrored fields must match the on-disk verdict file); orchestrator §5.6 Path B B7 drift check on proposal entries before merge (proposal-side mirror must match verdict.yaml exactly — drift treated as Pattern C3 evidence and BLOCKs before passport append) | orchestrator BLOCKs with "audit drift: persisted entry verdict disagrees with verdict file" (Path A) or "Pattern C3: proposal mirror drift from verdict.yaml" (Path B) |
| C2 | `entry.bundle_manifest_sha` mirrors `sidecar.prompt.bundle.bundle_manifest_sha` | sidecar (computed by wrapper) | passport entry | lint at wrapper write time | rejected |
| C3 | Acknowledgement append entry copies the latest persisted entry's `(stage, agent, deliverable_path, deliverable_sha, run_id, bundle_manifest_sha, artifact_paths)` and the inner verdict shape `(verdict.status, verdict.round, verdict.target_rounds, verdict.finding_counts, verdict.failure_reason)` byte-for-byte. The new entry's `verdict.verified_at` and `verdict.verified_by` are **freshly set by orchestrator via the strict-monotonic helper** (D3), NOT copied. C1's "verdict file wins" rule still applies — the new entry's mirrored verdict fields point at the same on-disk verdict file as the prior entry; C3 only governs which fields are copied versus refreshed during the append, not the source-of-truth direction | latest persisted entry (for copied fields); current UTC via D3 (for refreshed fields) | new ack entry | §5.4 ack mechanism (orchestrator-side); lint re-checks copied fields equal prior entry's | rejected at acknowledgement-write time |
| C4 | `entry.deliverable_sha == sidecar.prompt.bundle.primary_deliverables[].sha` for the matching primary deliverable (this is the entry-side half of B2; B2 is the cross-artifact-plus-disk version) | sidecar (computed at audit time) | passport entry | lint at wrapper write time | rejected |

#### D. Ordering rules

The passport is an append-only ledger (§3.1) and Path A selection (§5.6) reads "latest" entries. Two independent ordering mechanisms exist (`verified_at` for entries, `timing.started_at` for proposals); each rule below names which mechanism applies and why the alternatives were rejected.

| ID | Rule | Applies to | Mechanism | Enforcement point | Failure behavior |
|---|---|---|---|---|---|
| D1 | Latest persisted entry is selected by `max(verdict.verified_at)` over all entries matching the current `(stage, agent, deliverable_sha)` tuple, **conditional on D4: D1 applies only when no superseding higher-round proposal exists in `<output-dir>`**. Total order is guaranteed by D3 strict-monotonic. When multiple entries share the same `run_id` (only reachable via §5.4 acknowledgement append, where ack entry copies the original MATERIAL entry's `run_id`), D1 selects the latest by `verified_at` within that `run_id` group — D3 strict-monotonic guarantees the ack entry post-dates the original by ≥ 1 ms | passport `audit_artifact[]` entries | `verified_at` (RFC 3339 ms UTC per A1's `verdict.verified_at` constraint) | §5.6 Path A entry selection (after A1.5 supersession check); §5.3 ship/block read | tie is impossible by D3; if implementer's max() returns a non-deterministic tie due to bug, lint flags the duplicate `verified_at` |
| D2 | Path B proposal selection picks latest unmerged proposal by `max(sidecar.timing.started_at)` over proposals matching the tuple. `run_id` lex-max is the deterministic tie-breaker only on identical `started_at`. **`run_id` lex-max alone is NOT chronological** — the `<ISO-8601-Z>-<4-hex>` random suffix (sampled from `/dev/urandom` per §4.3) does not sort chronologically at sub-second resolution. In supersession mode (§5.6 A1.5 set the flag), B2 additionally filters to proposals whose `verdict.round > selected_persisted.verdict.round` per D4 | proposal files in `<output-dir>` | `sidecar.timing.started_at` primary, `run_id` lex-max tie-breaker; in supersession mode, additional `verdict.round > prior` filter | §5.6 Path B2 | orchestrator BLOCKs with "ambiguous proposal selection at <output-dir>" if multiple unverifiable sidecars share `started_at`; in supersession mode with no candidate surviving the higher-round filter (every candidate was lower-round or invalid at B2 selection time), B3 BLOCKs with "requested higher-round audit artifact is missing" — proposals that pass B2 but fail B6 / B7 / B8a get the proposal-specific BLOCK from P-PB-gate / P-PB-verdict-schema / P-PB-stale-late instead |
| D3 | Every orchestrator-side `verified_at` write (Path B8d normal merge, `another_round` re-merge, `ship_with_known_residue` ack append) goes through `_next_verified_at_ms(passport_audit_artifacts)` defined in §5.4 — guarantees `verified_at` strictly post-dates every prior persisted entry's `verified_at` regardless of clock granularity. Empty-ledger base case returns `now_ms` | passport `audit_artifact[]` entries | `t = max(now_ms, max_prior_verified_at + 1ms)`, or `now_ms` when no prior entries exist | orchestrator at every persisted-entry write | helper enforces invariant by construction; lint additionally verifies the result is `>` every prior entry as defense-in-depth |
| D4 | **Higher-round unmerged proposals supersede lower-round persisted entries for path selection (F-070 closure).** When orchestrator scans `<output-dir>` at §5.6 A1.5 and finds an unmerged proposal for the same `(stage, agent, deliverable_sha)` tuple whose `verdict.round` is greater than the A1-selected persisted entry's `verdict.round`, Path A is preempted and Path B runs with `supersession_required = true`. The signal is the wrapper artifact itself (round=N+1 written by `--round N+1` invocation), not a durable orchestrator state — preserves the artifact-as-contract design (Q2). Covers `another_round` user choice (§5.4), manual fresh wrapper run, byte-identical `abort_stage` re-audit, AND higher-round AUDIT_FAILED proposal (which preempts and BLOCKs with failure reason rather than silently falling back to prior MATERIAL) | passport `audit_artifact[]` entries + proposal files in `<output-dir>` | `verdict.round` comparison after B1a-style run_id de-dup excludes already-persisted leftovers from the proposal scan | §5.6 A1.5 (preflight) and Path B B2 (supersession-mode filter) | A1.5 forces Path B with supersession flag; B3 BLOCKs with "requested higher-round audit artifact is missing" if no candidate survives B2's higher-round filter (proposals that pass B2 but fail B6 / B7 / B8a get the proposal-specific BLOCK instead, NOT the supersede-missing diagnostic) |

#### E. Lifecycle ownership rules (who writes / who reads / who persists)

Constraints on which actor is allowed to perform each mutation. Violations of these rules are the primary attack surface for Pattern C3 (fake-audit forgery via direct passport writes).

| ID | Rule | Actor | Boundary | Enforcement point | Failure behavior |
|---|---|---|---|---|---|
| E1 | Wrapper writes only to its `--output-dir`; never to the passport file | wrapper script | filesystem | wrapper-side discipline (canonical wrapper ships in repo per §4.1; deployment-written wrappers risk this rule) | a deployment-written wrapper that writes to passport bypasses E2 — defended by §4.7 (wrapper not LLM-callable) plus deployment hygiene |
| E2 | Orchestrator is the only writer of `audit_artifact[]` entries into Schema 9 | orchestrator | code path | orchestrator agent prompt + §10 implementation | lint-detectable as "non-orchestrator writer modified passport" only post-hoc; primary defense is code-path discipline |
| E3 | `verdict.verified_at` and `verdict.verified_by` are set ONLY by the orchestrator on one of two write paths: (a) Path B8d normal proposal merge, (b) §5.4 `ship_with_known_residue` ack append. Both paths use D3's strict-monotonic helper | orchestrator | code path; schema | wrapper-emitted proposals carrying these fields are rejected at §5.6 Path B4 (`--mode proposal` schema rejection) | rejected as Pattern C3 attack surface |
| E4 | A wrapper-emitted proposal file with `verdict.verified_at` or `verdict.verified_by` filled is treated as malformed | wrapper output | schema | §5.6 Path B4 / §4.9 step 4 schema validation in `--mode proposal` | rejected; proposal file remains in `<output-dir>` (not moved to `consumed/`); user inspects |
| E5 | AUDIT_FAILED entries are never persisted into Schema 9 (proposal-arm only per A1's persisted-arm enum exclusion) | orchestrator | schema | `--mode persisted` schema validation rejects AUDIT_FAILED `verdict.status` | rejected at validation boundary; orchestrator surfaces `failure_reason` in §5.6 block message but does not append |
| E6 | Append-only ledger semantics: existing `audit_artifact[]` entries are never mutated. Multiple entries per `(stage, agent, deliverable_sha)` tuple are allowed and represent multi-round audit history. Acknowledgement is implemented as a NEW append (per C3) not as in-place mutation of the prior entry | orchestrator | code path | orchestrator agent prompt + §5.4 mechanism | a hand-edited mutation is detectable post-hoc by hash-chain verification (future v3.6.8+); for v3.6.7 this is discipline + code-review |
| E7 | Acknowledgement is a sibling annotation, not a `verdict.status` mutation. The new ack entry's `verdict.status` remains `MATERIAL` regardless of acknowledgement presence | orchestrator | C3 copy contract | §5.4 mechanism + B8 lint | rejected at write time if implementer mutates `verdict.status` to a synthetic "MATERIAL_ACKNOWLEDGED" or similar |
| E8 | The proposal entry file (`<run_id>.audit_artifact_entry.json`) is the LAST file the wrapper writes (after JSONL + sidecar + verdict are all on disk). This guarantees orchestrator never sees a proposal pointing at incomplete artifact paths | wrapper script | filesystem ordering | wrapper-side atomicity (tmp-file-rename per §4.4) | orchestrator that finds no proposal entry treats the run as not-conducted; no false PASS reachable through partial writes |
| E9 | Wrapper is **not invoked by an in-LLM Bash tool call from the same session producing the deliverable** (per §4.7). Allowed invokers: human interactive shell, CI workflow step, SubagentStop hook, second-terminal Bash from outside the LLM session. Same-session in-LLM invocation creates Pattern C3 exposure (the LLM that produced the deliverable has motive and means to fabricate audit metadata) — this is the structural attack-surface boundary that the artifact-as-contract design (Q2) was chosen to enforce | deployment + agent prompts | invocation-site discipline | spec-level: §6 partial inversion removes "the orchestrator runs codex audit afterward" sentences from the three downstream agent prompts so the agent has no awareness that a downstream audit exists (no trigger for Pattern C3 fabricated tool-call hallucination); deployment-level: audit runs in CI / SubagentStop hook / human-triggered out-of-band terminal | spec-level: a partial inversion regression (sentence re-added to an agent prompt) is caught by the §6 inversion-sweep lint; deployment-level: a same-session in-LLM call is undetectable from artifact evidence alone — the §1.2 motivated-forgery boundary applies and §9 R2 carries the residual risk discussion |

#### F. Naming convention rules

| ID | Rule | Applies to | Enforcement point | Failure behavior |
|---|---|---|---|---|
| F1 | `run_id` format: `<ISO-8601-Z>-<4-hex>` where the date-time component is RFC 3339 second precision and the 4-hex suffix is from `/dev/urandom` (per §4.3) | wrapper output, sidecar, entry, all artifact filenames | `audit_artifact_entry.schema.json` regex `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}Z-[0-9a-f]{4}$` | rejected as schema violation |
| F2 | All four artifact file basenames use the bare `<run_id>` stem with extensions `.jsonl`, `.meta.json`, `.verdict.yaml`, `.audit_artifact_entry.json`. No stage / agent / deliverable prefix | wrapper output | wrapper at write time uses `$run_id` directly per §4.4 pseudocode | wrapper aborts; lint rejects mis-named files |
| F3 | `sidecar.run_id` is identical to file basename (this is the artifact-side mirror of F2; B7 is the multi-file consistency version) | sidecar | `audit_sidecar.schema.json` field constraint | rejected |
| F4 | All §3.1 / §3.4 / §4.3 / §4.4 / §4.9 spec examples use the bare `<run_id>` filename pattern. Pre-Round-9 examples that included a `<stage>-<agent>-` prefix were retired in F-048 closure | spec text | review at spec edit time | spec drift caught by `scripts/check_audit_artifact_consistency.py` example-validation harness |

#### Why these specific groupings

Six families partition the rule space cleanly: A is local (one file), B is cross-file but synchronous-evidence (Layer 3 sees them all together), C is mirror (the same data appearing in multiple places needs an authoritative source), D is temporal ordering (the only rule family where bugs produce non-deterministic behavior rather than rejection), E is who-can-do-what (the attack-surface family), F is naming (the family that bugs in earlier rounds repeatedly missed because filename rules were spread across §3 examples vs §4 contract).

A reviewer auditing the spec end-to-end can read each table once and have full coverage of cross-artifact constraints. Rounds 1–9 of this spec demonstrated the cost of NOT having this index: F-030 (A5 was missing), F-032 (E5 was implicit), F-034 (C3 was undefined), F-039 (D1 had no tie-breaker), F-043 (D3 wasn't named), F-046 (D3's empty-ledger case was undefined), F-047 (D2 had no rule), F-048 (F2/F3/F4 disagreed) were all rules that no single §3.1–§3.5 reader would have known to check. Round 15 added F-070's escalation-deadlock fix (D4 superseding-proposal precedence) — the index made it cheap to add a new D-row and update D1/D2 with the supersession conditional rather than burying the rule in §5.6 prose. Future invariant additions (e.g., when v3.6.8 lands hash-chain verification per E6) get a new row in the appropriate family.

### 3.8 Schema additions summary

| Schema | Path | Purpose | Touches existing? |
|---|---|---|---|
| Schema 9 `audit_artifact[]` | `shared/handoff_schemas.md` | Append-friendly audit history per deliverable | Adds optional field; no rename, no required change |
| `audit_artifact_entry.schema.json` | `shared/contracts/passport/` | Per-entry shape for `audit_artifact[]` | New file |
| `audit_jsonl.schema.json` | `shared/contracts/audit/` | Layer 2 — codex JSONL row schema | New file |
| `audit_sidecar.schema.json` | `shared/contracts/audit/` | Layer 3 — sidecar metadata schema | New file |
| `audit_verdict.schema.json` | `shared/contracts/audit/` | Verdict file schema | New file |

The `shared/contracts/audit/` directory is new in v3.6.7. The README at `shared/contracts/README.md` (added v3.6.6 per generator-evaluator spec §1) gains one section documenting the audit/ directory's purpose, mirroring the v3.6.6 convention.

---

## 4. Wrapper script contract

The wrapper script is the boundary object between deployment-side audit execution and ARS-side artifact verification. ARS spec defines what the wrapper must produce (§3 schemas); deployment owns how the wrapper runs (codex CLI invocation, network access, retries). This separation is what makes Q2's artifact-as-contract execution model work — the orchestrator never needs to know what wrapper is, where codex lives, or whether the audit happens locally / on a build server / asynchronously.

### 4.1 Script identity and location

**Path:** `scripts/run_codex_audit.sh`
**Shell:** Bash 4+ (`#!/usr/bin/env bash`). The §4.4 pseudocode relies on Bash-only features — indexed arrays (`PRIMARY=(...)`, `${arr[@]}`, `${arr[*]}`), `declare -a`, `read -ra`, and here-strings (`<<<`) — so POSIX `sh` will not run this wrapper. Portable across macOS / Linux / WSL where Bash 4+ is available; macOS ships Bash 3.2 by default and users on stock macOS must install a newer Bash via Homebrew (`brew install bash`) or run on Linux/WSL. Exit code 64 (`EX_USAGE`) is emitted with a clear message if the wrapper detects `BASH_VERSION` < 4.
**Owner:** ARS repo. Maintained as part of the v3.6.7 deliverable; ships with the repo so users do not need to write their own.
**Versioned:** carries a top-of-file `# version: 1.0.0` comment that audit_verdict.schema.json field `generator_version` must match. Wrapper updates that change verdict shape MUST bump version and update CI fixtures.

**Required external commands** (wrapper preflights for each at startup; missing one exits 64 `EX_USAGE` with a "missing dependency: <name>" message before any artifact file is touched):

| Command | Used for | macOS availability | Linux/WSL availability |
|---|---|---|---|
| `bash` (>=4) | shell | Homebrew (`brew install bash`); stock 3.2 unsupported | distro default |
| `git` | `rev-parse --short HEAD`, `diff --quiet` | Xcode CLT or Homebrew | distro default |
| `awk` | column extraction in `_sha256` helper | BSD awk preinstalled | GNU awk preinstalled |
| `jq` | parse JSONL `thread.started` event's `thread_id` | Homebrew (`brew install jq`) | distro package |
| `od`, `tr` | run_id 4-hex suffix from `/dev/urandom` | preinstalled | preinstalled |
| `uname` | hostname (`uname -n`) | preinstalled | preinstalled |
| `sort` | deterministic ordering for the bundle manifest (`LC_ALL=C sort`) | preinstalled (BSD sort) | preinstalled (GNU sort) |
| `head` | extract first matching JSONL event's thread_id (`jq ... | head -1`) | preinstalled | preinstalled |
| `tee` | split codex `--json` stdout stream into the JSONL contract file plus the `<run_id>.stdout` diagnostic file in one pipeline (§4.4 Step 2b). Combined with `${PIPESTATUS[@]}` for tee-side error detection so a tee write failure surfaces as wrapper exit 73 rather than silently corrupting the JSONL artifact | preinstalled | preinstalled |
| `mv` | atomic tmp-file-rename for the three tmp-rename-bound contract files — sidecar, verdict, proposal entry (§4.4 atomicity guarantee). JSONL is intentionally exempt because codex streams it over the audit's runtime; see §4.4 for the proposal-last guarantee that makes JSONL's mid-write visibility unobservable to orchestrator | preinstalled | preinstalled |
| `python3` | fsync inside the §4.4 `_atomic_write` helper (`os.fsync(open(tmp).fileno())`); helper falls back to `sync(8)` when python3 is unavailable. Also assumed present by `parse_audit_verdict.py` shipped with the wrapper | preinstalled | distro default (Python 3.x in `/usr/bin/python3`) |
| `codex` | actual audit invocation | Homebrew (`brew install codex` or codex installer) | codex installer |
| SHA-256 helper (one of `sha256sum` OR `shasum`) | content hashing throughout §4.4 | macOS ships `shasum` only (`shasum -a 256`); `sha256sum` requires `brew install coreutils` | Linux/WSL ship `sha256sum` |

The §4.4 pseudocode shows `sha256sum` for readability; the actual wrapper defines a single `_sha256()` helper that prefers `sha256sum` when present and falls back to `shasum -a 256` otherwise (see §4.4 helper definition). All `sha256sum "$path" | awk '{print $1}'` call sites in the pseudocode therefore correspond to `_sha256 "$path"` in the actual script.

**Why a shipped wrapper, not deployment-written:** if every deployment writes its own wrapper, sidecar field semantics drift (different hostname conventions, different timing precision, different exit code mapping). Layer 3 cross-file rules then cease to be enforceable across deployments. Shipping the canonical wrapper guarantees sidecar uniformity.

### 4.2 Inputs

```sh
scripts/run_codex_audit.sh \
  --stage <stage>                   # required, integer 1-6
  --agent <agent_name>              # required, one of three v3.6.7 agents
  --deliverable <path>              # required, repo-relative path
  --supporting <path1,path2,...>    # optional, comma-separated paths
  --round <N>                       # required, integer >= 1
  --target-rounds <N>               # optional, integer >= 1, defaults 3 (matches audit template Section 1 default; orchestrator §5.4 round upper bound is the policy-side cap)
  --previous-findings <path>        # optional, prior round verdict file (for round > 1)
  --output-dir <dir>                # optional, defaults audit_artifacts/
  --bundle-id <opaque-string>       # optional, used to group multi-file Phase 2 audits
  --dry-run                         # optional, validates inputs without invoking codex
```

**Input validation rules (wrapper rejects with exit code 64 = `EX_USAGE`):**

- `--agent` must match the enum from `audit_artifact_entry.schema.json` §3.2.
- `--deliverable` must exist and be readable. Wrapper computes its SHA-256 and pins into sidecar.
- `--supporting` paths must exist (audit prompt cannot reference missing files).
- `--round` must be `<= --target-rounds`.
- `--previous-findings` is required when `--round > 1`; absent triggers reject (round 2+ without round-1 findings is per audit template Section 4(a) violation).
- `--bundle-id` must be the same value for all files in one multi-file Phase 2 audit (per §4.5 below).

### 4.3 Outputs (the contract)

For a successful audit run, the wrapper produces exactly four contract files in `--output-dir`. Three of them (sidecar, verdict, proposal entry) are written atomically via tmp-file-rename (each file fsynced and rename-committed before script returns); the fourth (JSONL) is streamed by codex CLI directly to its final path and may be observed mid-write — see §4.4 atomicity guarantee for why JSONL is exempt and why the proposal-last write order makes JSONL's mid-write visibility never reach orchestrator state:

| File | Schema | Purpose |
|---|---|---|
| `<run_id>.jsonl` | `audit_jsonl.schema.json` | Raw codex CLI output (Layer 2 evidence) |
| `<run_id>.meta.json` | `audit_sidecar.schema.json` | Wrapper-emitted runtime metadata (Layer 3 evidence) |
| `<run_id>.verdict.yaml` | `audit_verdict.schema.json` | Parsed verdict (orchestrator policy input) |
| `<run_id>.audit_artifact_entry.json` | `audit_artifact_entry.schema.json` (`--mode proposal`) | Proposal entry for orchestrator to merge into Schema 9 `audit_artifact[]` (§4.9 lifecycle) |

`run_id` format: `<ISO-8601-Z>-<4-hex-suffix>` per §3.1, generated by wrapper at script start. The 4-hex suffix is `od -An -N2 -tx1 < /dev/urandom | tr -d ' '` to disambiguate sub-second runs.

**Plus three non-required diagnostic files** (kept for debugging, not part of contract):

- `<run_id>.stdout` — codex CLI stdout
- `<run_id>.stderr` — codex CLI stderr (always written, even on success — codex emits warnings here)
- `<run_id>.manifest.txt` — the canonical manifest of primary / supporting / template entries hashed into `bundle_manifest_sha` (§4.4 Step 0b, §3.6 contract). Kept for audit-trail forensics so a future reader can see which files were in scope at audit time without re-deriving from `bundle_manifest_sha` alone.

These are referenced from the sidecar's `process.stdout_path` / `stderr_path` (and from §4.4 Step 0b for the manifest) but Layer 3 verification does NOT read them. Their existence is asserted by sidecar but their content is opaque to ARS.

### 4.4 Wrapper internal behavior

```bash
# Pseudocode — actual script implementation lives in scripts/run_codex_audit.sh
# Bash 4+ required (see §4.1): uses indexed arrays, read -ra, here-strings, declare -a.
# Required external commands enumerated in §4.1 dependency table; preflight runs first.

# Portable SHA-256 helper (see §4.1). Prefers GNU sha256sum, falls back to BSD
# shasum -a 256 (the only SHA-256 tool on stock macOS). Every "sha256sum X | awk
# '{print $1}'" pattern in this pseudocode is shorthand for "_sha256 X" in the
# actual script.
_sha256() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  else
    shasum -a 256 "$1" | awk '{print $1}'
  fi
}

# Crash-tolerant JSONL thread_id extractor (F-059 closure). Returns empty
# string when the JSONL file is missing, empty (codex killed before opening
# its output file — see Step 2a placeholder), or contains no parseable
# thread.started event with thread_id field. §3.4 conditional already permits
# empty stream.jsonl_thread_id when the companion verdict status is
# AUDIT_FAILED; this helper is the canonical path that emits the empty value
# cleanly without crashing.
#
# codex 0.125+ emits the thread_id only on the opening `thread.started` event
# (per §3.3 event-stream contract). Earlier draft parsed `.session_id` per
# every row — that field does not exist in 0.125+ output and the parse
# returned null on every clean run. The current jq filter selects only events
# whose `type == "thread.started"` and pulls their `thread_id`.
_extract_jsonl_thread_id() {
  local path="$1"
  if [ ! -s "$path" ]; then
    printf ''
    return
  fi
  jq -r 'select(.type == "thread.started") | .thread_id' "$path" 2>/dev/null \
    | head -1
}

# Extract semver from `codex --version` output. codex 0.125+ prints
# "codex-cli X.Y.Z" (e.g., "codex-cli 0.128.0"); §3.4 sidecar schema's `codex_cli_version` field is a
# bare semver string with regex constraint `^[0-9]+\.[0-9]+\.[0-9]+$`. Match
# the first dotted-triple in stdout and reject (EX_USAGE) if absent — defends
# against future CLI versions that print multi-line stdout or unexpected
# formats and would otherwise let malformed text leak into the sidecar.
_codex_version() {
  local v
  v=$(codex --version 2>/dev/null \
    | awk 'match($0, /[0-9]+\.[0-9]+\.[0-9]+/) { print substr($0, RSTART, RLENGTH); exit }')
  [ -n "$v" ] || exit 64
  printf '%s\n' "$v"
}

# Atomic write helper (§4.4 atomicity guarantee). Writes stdin to <path>.tmp,
# fsyncs the tmp file, then renames it over <path>. Used for sidecar, verdict,
# and proposal entry — the three contract files §4.4 guarantees orchestrator
# observes whole-or-not-at-all. JSONL is intentionally NOT routed through this
# helper because codex CLI streams it to its final path over the audit's
# runtime; the proposal-last write order makes JSONL's mid-write visibility
# unobservable to orchestrator. In the §4.4 pseudocode below, every redirection
# of the form `... > "$OUT_DIR/$run_id.{meta.json,verdict.yaml,
# audit_artifact_entry.json}"` is shorthand for `... | _atomic_write
# "$OUT_DIR/$run_id.<filename>"` — the actual script wraps each of those three
# writes in this helper.
_atomic_write() {
  local path="$1"
  local tmp="${path}.tmp"
  cat > "$tmp"
  # Best-effort fsync: prefer Python which is already required for parse
  # helpers; fall back to `sync` if Python is unavailable for some reason.
  if command -v python3 >/dev/null 2>&1; then
    python3 -c "import os,sys; f=open(sys.argv[1]); os.fsync(f.fileno()); f.close()" "$tmp"
  else
    sync
  fi
  mv -f "$tmp" "$path"
}

# Step 0a — dry-run early exit. `--dry-run` is contracted by §4.2 as input-
# validation only; per §10 Phase 6.1 verification gate it MUST NOT write any
# files under `--output-dir`. Earlier draft had no dry-run branch, so the
# wrapper would walk through run_id generation, manifest write, JSONL
# placeholder pre-touch, codex invocation, sidecar / verdict / proposal
# emission — creating a fake audit artifact at zero codex cost (the exact
# Pattern C3 attack surface §1.2 defends against). All input validation
# (--agent enum, --deliverable readable, --round <= --target-rounds, etc.)
# has already happened upstream in the §4.2 input parser; reaching this
# point means inputs are valid, so dry-run exits 0 with a one-line stdout
# diagnostic and never touches --output-dir.
if [ "$DRY_RUN" = true ]; then
  printf '[run_codex_audit] dry-run: inputs valid; no files written\n'
  exit 0
fi

run_id=$(generate_run_id)
sha_deliverable=$(_sha256 "$DELIVERABLE")
git_sha=$(git rev-parse --short HEAD)
git_dirty=$(git diff --quiet && echo false || echo true)

# Step 0 — normalize CLI inputs into bash arrays.
# §4.2 specifies --supporting as a comma-separated string; here we split
# into PRIMARY and SUPPORTING arrays for downstream iteration. The PRIMARY
# array always contains exactly one element (the deliverable); SUPPORTING
# may be empty, which is permitted.
PRIMARY=("$DELIVERABLE")
if [ -n "$SUPPORTING_CSV" ]; then
  IFS=',' read -ra SUPPORTING <<< "$SUPPORTING_CSV"
else
  SUPPORTING=()
fi

# Step 0b — snapshot bundle file SHAs BEFORE rendering the prompt or invoking
# codex (F-060 closure: TOCTOU race). The prompt embeds the at-render-time
# content of every primary + supporting + template file; the manifest written
# into the sidecar must reflect THAT content, not a later state. If a
# supporting file mutates between render time and Step 3a recompute, Step 3a
# detects it and the wrapper writes AUDIT_FAILED with a "bundle file mutated
# during audit" failure_reason — codex saw stale content and the sidecar
# manifest must not silently match the post-mutation state.
audit_template_path="shared/templates/codex_audit_multifile_template.md"
audit_template_sha_pre=$(_sha256 "$audit_template_path")
declare -a primary_shas_pre supporting_shas_pre
for path in "${PRIMARY[@]}"; do
  primary_shas_pre+=("$path:$(_sha256 "$path")")
done
for path in "${SUPPORTING[@]}"; do
  supporting_shas_pre+=("$path:$(_sha256 "$path")")
done

# Compute the canonical pre-codex bundle manifest (§3.6 deterministic format).
# This value is what gets written to sidecar.prompt.bundle.bundle_manifest_sha
# AND what L3-4 will recompute against current file contents at Path A/B
# verification time.
{
  for entry in "${primary_shas_pre[@]}"; do printf 'primary:%s\n' "$entry"; done
  for entry in "${supporting_shas_pre[@]}"; do printf 'supporting:%s\n' "$entry"; done
  printf 'template:%s:%s\n' "$audit_template_path" "$audit_template_sha_pre"
} | LC_ALL=C sort > "$OUT_DIR/$run_id.manifest.txt"
bundle_manifest_sha=$(_sha256 "$OUT_DIR/$run_id.manifest.txt")

# Step 1 — render audit prompt from template + bundle inputs
# Build a flag-repeated argument list for render_template's --supporting:
# each element of the SUPPORTING array becomes one repeated --supporting
# flag. Naive "$SUPPORTING" or "${SUPPORTING[*]}" would only forward the
# first element (or a single space-joined blob), which would silently drop
# every supporting file beyond the first from the audit prompt.
supporting_args=()
for path in "${SUPPORTING[@]}"; do
  supporting_args+=(--supporting "$path")
done
prompt=$(render_template "$audit_template_path" \
  --round "$ROUND" \
  --target-rounds "$TARGET_ROUNDS" \
  --primary "$DELIVERABLE" \
  "${supporting_args[@]}" \
  --previous-findings "$PREV_FINDINGS")

# Step 2a — pre-touch JSONL placeholder so the file exists even if codex is
# killed by SIGTERM / SIGKILL / OOM before opening its output file. Without this
# the AUDIT_FAILED path (Step 4 else branch) could synthesize a verdict whose
# proposal entry references a nonexistent JSONL, violating the "if proposal
# exists, all three artifacts it references exist" contract (§4.4 atomicity
# guarantee). Empty JSONL is treated by §5.6 Path B5 the same way as a partial
# JSONL — the AUDIT_FAILED short-circuit does not require valid Layer 2 content.
: > "$OUT_DIR/$run_id.jsonl"

# Step 2b — invoke codex CLI with supported flags. codex 0.125.0 dropped the
# pre-0.121 flag set; the current (and only) way to control reasoning effort
# is the `-c model_reasoning_effort=...` config override (TOML-quoted), and
# `--json` replaces the older `--output-format jsonl`. There are no
# `--output`, `--stdout-log`, or `--stderr-log` flags in 0.125+ — codex prints
# the event-stream to stdout, which we split via a real pipeline + tee into
# the JSONL contract file plus the <run_id>.stdout diagnostic file. Stderr
# goes to <run_id>.stderr at shell level.
#
# We use a pipeline with PIPESTATUS rather than process substitution
# `> >(tee ...)` because the latter:
#   1. Leaves tee's exit status outside `$?` (the wrapper sees only codex's
#      exit, never tee's — a tee write failure to a full disk would silently
#      corrupt the JSONL artifact),
#   2. Race-conditions on draining: orchestrator can Read the JSONL before
#      the tee subshell flushes, observing partial JSONL not because codex
#      is mid-stream but because tee hasn't written yet,
#   3. Has no clean way to reorder JSONL-write-then-stdout-log.
# The pipeline form below captures both stages via `${PIPESTATUS[@]}`:
# pipe[0] is codex's exit, pipe[1] is tee's. Tee failure (disk full, EIO)
# triggers EX_CANTCREAT (73) per §4.6.
#
# `set +e` is required because §4.1 `set -euo pipefail` would abort the
# wrapper on non-zero codex exit before `${PIPESTATUS[@]}` is captured; we
# capture locally then re-enable. Note: with `pipefail`, $? on a pipeline is
# the rightmost non-zero stage's exit — but we want codex's exit specifically
# (pipe[0]), not the rightmost, so PIPESTATUS is the canonical capture.
#
# This is `codex exec`, not `codex exec resume <thread_id>` — every audit
# run is a fresh thread; the wrapper never resumes a prior thread.
started_at=$(rfc3339_now_ms)
set +e
codex exec \
  -m gpt-5.5 \
  -c 'model_reasoning_effort="xhigh"' \
  --json \
  - \
  2> "$OUT_DIR/$run_id.stderr" \
  <<<"$prompt" \
  | tee "$OUT_DIR/$run_id.stdout" > "$OUT_DIR/$run_id.jsonl"
pipe=("${PIPESTATUS[@]}")
exit_code="${pipe[0]}"
tee_exit="${pipe[1]}"
set -e
ended_at=$(rfc3339_now_ms)

# Tee write failure is treated as EX_CANTCREAT (73): the wrapper cannot
# guarantee the JSONL contract file is intact. Cleanup partial artifacts so
# orchestrator never sees a sidecar / verdict / proposal pointing at a
# corrupt JSONL, then exit 73 per §4.6 row.
if [ "$tee_exit" -ne 0 ]; then
  rm -f "$OUT_DIR/$run_id.jsonl" "$OUT_DIR/$run_id.stdout" \
        "$OUT_DIR/$run_id.stderr" "$OUT_DIR/$run_id.manifest.txt"
  printf '[run_codex_audit] tee write failed (exit %s): cannot guarantee JSONL integrity\n' "$tee_exit" >&2
  exit 73
fi

# Step 3a — recompute bundle file SHAs and detect intra-audit mutation
# (F-060 closure: TOCTOU race detection). The pre-codex snapshot in Step 0b
# was the canonical bundle state at render-time. If any primary / supporting /
# template file mutated DURING the codex run (user edited in another terminal,
# IDE auto-save, CI build artifact regenerated), this recompute catches it
# and the wrapper falls into the AUDIT_FAILED branch at Step 4 with a
# "bundle file mutated during audit" failure_reason — codex reviewed the
# pre-mutation content and the audit verdict is stale.
declare -a primary_shas supporting_shas
for path in "${PRIMARY[@]}"; do
  primary_shas+=("$path:$(_sha256 "$path")")
done
for path in "${SUPPORTING[@]}"; do
  supporting_shas+=("$path:$(_sha256 "$path")")
done
audit_template_sha=$(_sha256 "$audit_template_path")

# Compare pre vs post arrays element-wise. Any mismatch indicates intra-audit
# mutation. bundle_mutation_detected=1 forces the AUDIT_FAILED branch in
# Step 4 even if codex itself exited cleanly.
bundle_mutation_detected=0
bundle_mutation_files=()
for i in "${!primary_shas[@]}"; do
  if [ "${primary_shas[i]}" != "${primary_shas_pre[i]}" ]; then
    bundle_mutation_detected=1
    bundle_mutation_files+=("${primary_shas[i]%%:*}")
  fi
done
for i in "${!supporting_shas[@]}"; do
  if [ "${supporting_shas[i]}" != "${supporting_shas_pre[i]}" ]; then
    bundle_mutation_detected=1
    bundle_mutation_files+=("${supporting_shas[i]%%:*}")
  fi
done
if [ "$audit_template_sha" != "$audit_template_sha_pre" ]; then
  bundle_mutation_detected=1
  bundle_mutation_files+=("$audit_template_path")
fi

# Step 3b — manifest is fixed at the pre-codex value (computed in Step 0b).
# Sidecar carries the pre-codex manifest because that is what codex actually
# saw. Post-codex SHAs above are diagnostic only (used to set
# bundle_mutation_detected); they do NOT update bundle_manifest_sha. Otherwise
# L3-4 at orchestrator verification time would compare current-state SHAs
# against post-mutation SHAs and silently accept the stale audit.

# Step 3c — write sidecar (Layer 3 evidence)
emit_sidecar \
  --run-id "$run_id" \
  --codex-version "$(_codex_version)" \
  --hostname "$(uname -n)" \
  --cwd "$(pwd)" \
  --git-sha "$git_sha" \
  --git-dirty "$git_dirty" \
  --started "$started_at" \
  --ended "$ended_at" \
  --exit-code "$exit_code" \
  --jsonl-thread-id "$(_extract_jsonl_thread_id "$OUT_DIR/$run_id.jsonl")" \
  --primary-shas "${primary_shas_pre[*]}" \
  --supporting-shas "${supporting_shas_pre[*]}" \
  --audit-template-path "$audit_template_path" \
  --audit-template-sha "$audit_template_sha_pre" \
  --bundle-manifest-sha "$bundle_manifest_sha" \
  --bundle-id "$BUNDLE_ID" \
  > "$OUT_DIR/$run_id.meta.json"

# Step 4 — produce verdict file. Three triggers force the AUDIT_FAILED branch:
# (a) codex exit_code != 0, (b) parse_audit_verdict.py --probe rejects the
# JSONL, (c) bundle_mutation_detected (Step 3a TOCTOU detection).
# wrapper_exit_code starts as a copy of codex's exit_code; the AUDIT_FAILED
# branch may override it so that wrapper exit status agrees with verdict status
# (§4.6 contract: exit 0 ↔ PASS/MINOR/MATERIAL; non-zero ↔ AUDIT_FAILED).
wrapper_exit_code=$exit_code
if [ "$exit_code" -eq 0 ] \
   && [ "$bundle_mutation_detected" -eq 0 ] \
   && scripts/parse_audit_verdict.py --probe "$OUT_DIR/$run_id.jsonl" >/dev/null 2>&1; then
  # Clean codex completion + bundle stable + parseable JSONL agent_message event → real verdict
  scripts/parse_audit_verdict.py \
    --jsonl "$OUT_DIR/$run_id.jsonl" \
    --round "$ROUND" \
    --target-rounds "$TARGET_ROUNDS" \
    > "$OUT_DIR/$run_id.verdict.yaml"
else
  # codex exit != 0 OR bundle mutated mid-audit OR JSONL is partial / missing
  # parseable agent_message event → AUDIT_FAILED. Synthesize the failure verdict directly; do
  # NOT run parse_audit_verdict.py against partial JSONL (it would either crash
  # or hallucinate findings).
  if [ "$bundle_mutation_detected" -eq 1 ]; then
    failure_reason="bundle file(s) mutated during audit run: ${bundle_mutation_files[*]}"
  else
    failure_reason=$(synthesize_failure_reason "$exit_code" "$OUT_DIR/$run_id.stderr")
  fi
  emit_audit_failed_verdict \
    --run-id "$run_id" \
    --round "$ROUND" \
    --target-rounds "$TARGET_ROUNDS" \
    --failure-reason "$failure_reason" \
    > "$OUT_DIR/$run_id.verdict.yaml"
  # If we entered this branch with codex exit 0 (parse-probe failure path OR
  # bundle-mutation path), override wrapper_exit_code to 70 (EX_SOFTWARE) so
  # the §4.6 contract holds: an AUDIT_FAILED verdict file MUST be paired with
  # non-zero wrapper exit. If codex itself already exited non-zero,
  # wrapper_exit_code already carries that value and the override is a no-op.
  if [ "$wrapper_exit_code" -eq 0 ]; then
    wrapper_exit_code=70
  fi
fi

# In the AUDIT_FAILED branch, sidecar's stream.jsonl_thread_id may be
# empty (no valid JSONL thread). Schema permits this for AUDIT_FAILED runs;
# orchestrator §5.6 Path B5 short-circuits before reading thread_id.

# Step 5 — emit proposal entry for orchestrator to merge (§4.9 lifecycle).
# Verdict block (status + round + target_rounds + finding_counts + optional
# failure_reason) is mirrored from the verdict.yaml produced in Step 4.
# verified_at and verified_by are NOT set (orchestrator fills them at merge time).
emit_proposal_entry \
  --run-id "$run_id" \
  --stage "$STAGE" \
  --agent "$AGENT" \
  --deliverable "$DELIVERABLE" \
  --deliverable-sha "$sha_deliverable" \
  --bundle-id "$BUNDLE_ID" \
  --bundle-manifest-sha "$bundle_manifest_sha" \
  --jsonl-path "$OUT_DIR/$run_id.jsonl" \
  --sidecar-path "$OUT_DIR/$run_id.meta.json" \
  --verdict-path "$OUT_DIR/$run_id.verdict.yaml" \
  --verdict-yaml "$OUT_DIR/$run_id.verdict.yaml" \
  > "$OUT_DIR/$run_id.audit_artifact_entry.json"

# Step 6 — exit. wrapper_exit_code reflects either codex's own exit code OR
# the parse-probe-failure override set in Step 4 (so wrapper exit status
# always agrees with verdict status per §4.6). Orchestrator additionally
# inspects the proposal's verdict.status to decide ship/block — the two
# signals (process exit code + verdict.status) are independently consumed.
[ "$wrapper_exit_code" -eq 0 ] && exit 0 || exit "$wrapper_exit_code"
```

**Atomicity guarantee:**

Three of the four contract files (sidecar, verdict, proposal entry) are written via the tmp-file-rename pattern: wrapper writes to `<file>.tmp`, fsyncs, then `mv <file>.tmp <file>`. The fourth file, JSONL, is intentionally exempt: codex 0.125+ `--json` writes its event stream to stdout (the CLI has no `--output` flag in 0.125+; see §3.3 + §4.4 Step 2b), and the wrapper splits stdout via a `tee | >` pipeline into `<run_id>.jsonl` (the contract artifact) and `<run_id>.stdout` (diagnostic copy). The pipeline runs over the audit's runtime (potentially minutes), and tmp-rename of a streamed file would defeat live debugging via `tail -f`. Step 2a additionally pre-touches an empty JSONL placeholder so the file exists at a known path even when codex is killed before emitting any events (F-059 closure). JSONL therefore may be observed mid-write or empty during an audit run, but **no orchestrator code path ever consumes JSONL until a proposal entry file references it** (see proposal-last guarantee below) — so JSONL's lack of tmp-rename atomicity is not observable to orchestrator. Step 2b's `${PIPESTATUS[@]}` capture additionally surfaces tee-side write failures (disk full / EIO during the streaming write) as wrapper exit 73 with cleanup of all partial artifacts, so a corrupted JSONL never reaches the proposal-write step. For AUDIT_FAILED proposals, §5.6 Path B5 short-circuits BLOCK before Layer 2 validation runs (gating against incomplete evidence is meaningless — see §5.6 B5). For PASS / MINOR / MATERIAL proposals, §5.2 L2-1 (file exists) and L2-2 (every event validates against `audit_jsonl.schema.json`) reject missing or partial JSONL at the gate, so a non-AUDIT_FAILED proposal whose JSONL is partially-written never ships.

If the wrapper crashes between any two writes, only `.tmp` artifacts (for the three tmp-renamed files), the empty/partial JSONL placeholder, and possibly `.stdout`/`.stderr` remain. Orchestrator finds no proposal entry → treats run as not-conducted (per §5 rule). No false PASS reachable through partial writes.

The proposal entry file is the **last** thing the wrapper writes (after JSONL + sidecar + verdict are all on disk and — for sidecar/verdict/proposal — atomically renamed). This is the load-bearing guarantee that lets JSONL skip tmp-rename: orchestrator never sees a proposal pointing at incomplete artifact paths, so JSONL's mid-write visibility never reaches orchestrator state.

### 4.5 Multi-file Phase 2 audit (per audit template §4.1 D1 lesson)

The audit template Section 4 already supports multi-file bundles (Phase 2 chapter deliverable: synthesis + verification + instrument together). Wrapper supports this via:

- One wrapper invocation per audit run, regardless of file count in bundle.
- `--deliverable` is the bundle's primary file (the one whose `audit_artifact[]` entry the orchestrator reads).
- `--supporting` carries the rest of the bundle (`bibliography.json`, `verification.md`, etc.).
- `--bundle-id` (CLI flag, kebab-case) populates the schema field `bundle_id` (snake_case, per §3.2) on the resulting `audit_artifact[]` entry and the sidecar `prompt.bundle.bundle_id` field. Same value for all files in the bundle. Orchestrator reads `bundle_id` to know "these N audit_artifact entries belong to one logical bundle."

For Phase 2 chapter ships, three `audit_artifact[]` entries (one per primary deliverable) all carry the same `bundle_id` for audit-trail grouping. Each entry's stage-transition gate fires independently when that agent's deliverable is produced (per §5.1 independent-gating semantics) — `bundle_id` does not collectively gate them.

### 4.6 Failure modes

| Wrapper exit code | Meaning | Files written | Orchestrator response |
|---|---|---|---|
| 0 | Audit completed cleanly | All four contract files (jsonl + sidecar + verdict + proposal entry); proposal carries verdict status PASS / MINOR / MATERIAL | Read verdict, proceed per §5.3 / §5.6 Path B |
| 64 (`EX_USAGE`) | Input validation failed | None | Block, surface error to user; orchestrator never sees a proposal |
| 70 (`EX_SOFTWARE`) | (Wrapper-originated.) Triggered by any of: (a) codex itself exited 70 [`EX_SOFTWARE`], (b) codex exited 0 but `parse_audit_verdict.py --probe` rejected the JSONL (no `agent_message` `item.completed` event in stream, missing closing `turn.completed` event, malformed Section 6 verdict text in the final agent_message, etc.), (c) bundle mutation detected — Step 3a's recompute revealed at least one primary / supporting / template file changed during the codex run (TOCTOU race per F-060). In cases (b) and (c) the §4.4 Step 4 `wrapper_exit_code` override raises codex's exit-0 to 70 so the wrapper's process exit always agrees with the AUDIT_FAILED verdict it just wrote (§4.6 contract: wrapper exit 0 ↔ PASS/MINOR/MATERIAL; wrapper exit non-zero ↔ AUDIT_FAILED) | jsonl (possibly partial; possibly empty placeholder from Step 2a if codex was killed before opening output — see F-059), sidecar (with `process.exit_code` carrying codex's actual exit — may be 0 in cases (b)/(c) since sidecar records codex's process exit; wrapper exit is a separate signal), verdict (carrying status `AUDIT_FAILED`), proposal entry (carrying `verdict.status: AUDIT_FAILED`, `finding_counts: {p1: 0, p2: 0, p3: 0}`, `verdict.failure_reason: <one-line>` — case (c) reason format: `"bundle file(s) mutated during audit run: <space-separated path list>"`) | §5.6 Path B5 catches `AUDIT_FAILED` proposal: BLOCK transition without running the eleven gating checks (audit did not complete; gating is meaningless) and without merging into passport |
| 73 (`EX_CANTCREAT`) | Cannot write to `--output-dir` | None or partial — wrapper aborts before any contract file is fsync-renamed | Block, surface filesystem error |
| 75 (`EX_TEMPFAIL`) | codex API rate-limited / transient (codex itself exited 75; wrapper preserves the code rather than normalizing to 70 so deployment can detect rate-limiting and apply backoff before retry) | Same artifact set as exit 70: jsonl (possibly partial), sidecar (with `process.exit_code: 75`), verdict (status `AUDIT_FAILED`), proposal entry (status `AUDIT_FAILED`, `failure_reason: "codex exit 75: rate-limited"` or similar) | Same as exit 70: §5.6 Path B5 BLOCK without gating |
| Other non-zero (codex's own exit code, preserved) | Codex exited with a code not enumerated above (e.g., 1, 2, 137 from SIGKILL). Wrapper preserves codex's exit code rather than normalizing — preserves diagnostic signal for deployment-side log analysis. The wrapper still produces the AUDIT_FAILED artifact set per the "wrapper writes sidecar + proposal even on codex failure" key invariant below | Same artifact set as exit 70 if wrapper reaches the post-codex step (sidecar `process.exit_code` carries codex's actual code, verdict status `AUDIT_FAILED`, proposal carries `failure_reason: "codex exit <N>: <synthesize_failure_reason output>"`) | Same as exit 70: §5.6 Path B5 BLOCK without gating |

**Key invariants:**

- Wrapper MUST always write a sidecar AND a proposal entry on completion, even on codex non-zero exit, EXCEPT when exit is 64 (input validation, before any work starts) or 73 (cannot write — disk error, no point retrying).
- A sidecar with `process.exit_code != 0` paired with a proposal carrying `verdict.status: AUDIT_FAILED` is the orchestrator's signal that audit was attempted but failed — distinct from "audit was never run" (no proposal at all).
- `AUDIT_FAILED` is a fourth verdict status added to the §3.5 verdict schema enum: `["PASS", "MINOR", "MATERIAL", "AUDIT_FAILED"]`. It exists for failure-mode signaling only; orchestrator never ships on `AUDIT_FAILED` and never runs gating against it (rule of §5.6 Path B5: `AUDIT_FAILED` short-circuits to BLOCK).
- `verdict.failure_reason` is required when `verdict.status == "AUDIT_FAILED"`, forbidden otherwise. One-line human-readable reason ("codex exit 70: network timeout after 600s", "JSONL parse error at row 47", etc.).
- Schema validation on proposal still applies: §3.2 cross-field rules accept `AUDIT_FAILED` as a status, but its semantics are "audit aborted" not "audit found no issues". Cross-field rule for `AUDIT_FAILED` is `finding_counts.{p1,p2,p3} == 0 AND failure_reason is set`.

This contract closes F-019 (round 3): orchestrator can distinguish three states cleanly — (1) no proposal = audit never ran, (2) `AUDIT_FAILED` proposal = audit ran but failed, (3) PASS/MINOR/MATERIAL proposal = audit completed and produced findings. State (1) and (2) both BLOCK transition; only state (3) reaches gating.

### 4.7 Wrapper is not LLM-callable

The wrapper is invoked by:

- A human running `scripts/run_codex_audit.sh ...` interactively
- A CI workflow step (`.github/workflows/audit.yml` — to be added in implementation)
- A SubagentStop hook configured by deployment (per `feedback_subagent_tool_hallucination.md` runtime bus pattern)
- A separate Bash-tool call from outside the LLM session (e.g., user opens a second terminal)

The wrapper is NOT invoked by an in-LLM Bash tool call from the same session producing the deliverable. This is a deliberate constraint, not a technical limitation: an LLM that produces a deliverable AND calls the audit wrapper is structurally susceptible to Pattern C3 (sub-agent fabricated audit metadata, see `feedback_subagent_tool_hallucination.md`). The artifact-as-contract design (Q2) is the structural fix; this rule is its enforcement.

Spec-level enforcement: the v3.6.7 main spec §6.x agent prompts retain the "DO NOT simulate any audit step" prohibition (already shipped). The Step 6 partial inversion (§6 of this spec) removes the sentence that reveals "the orchestrator runs codex audit afterward" — the agent is no longer told there is a downstream audit at all, removing the trigger for Pattern C3.

### 4.8 Wrapper version compatibility

`audit_verdict.schema.json` carries a `generator_version` field. Orchestrator reads this and applies version-specific verdict parsing rules. v3.6.7 ships wrapper version `1.0.0`; future versions may emit additional verdict fields, but core fields (`verdict_status`, `finding_counts`, `findings[]`) are stable across versions per semver.

If orchestrator encounters a `generator_version` it does not recognize (newer wrapper than orchestrator), it logs a warning but processes the verdict using the latest known schema version. If orchestrator encounters a wrapper version it has been told is broken (deny-list in `scripts/check_audit_artifact_consistency.py`), it rejects the artifact.

### 4.9 Passport entry lifecycle (who writes audit_artifact[] into Schema 9)

The wrapper produces four contract files (§4.3): three artifact files (jsonl / sidecar / verdict) plus the proposal entry file. Orchestrator is the sole writer of `audit_artifact[]` into Schema 9. This split prevents concurrency on the passport file (wrapper may run from CI / cron / background hook; passport may be open in an LLM session) and keeps Schema 9 mutation in the same code path that handles other Schema 9 fields (`reset_boundary[]`, `literature_corpus[]`, `compliance_history[]`).

**Lifecycle:**

| Step | Actor | Action |
|---|---|---|
| 1 | Wrapper | Produces three artifact files (jsonl / sidecar / verdict, §4.3) under `--output-dir`. Sidecar and verdict are written via tmp-file-rename (atomic); JSONL is streamed by codex directly to its final path (intentionally non-atomic per §4.4 — codex's runtime is potentially minutes and tmp-rename of a streamed file would defeat live debugging via `tail -f`). Verdict status is one of PASS / MINOR / MATERIAL / AUDIT_FAILED per §4.6 |
| 2 | Wrapper | Produces the fourth file `<run_id>.audit_artifact_entry.json` (proposal entry) — this is the LAST file the wrapper writes, ensuring orchestrator never sees a proposal pointing at incomplete artifact paths. `verdict.verified_at` and `verdict.verified_by` are UNSET (verification has not happened yet) |
| 3 | Orchestrator | At stage transition, attempts §5.6 Path A first (look up matching persisted entry by `(stage, agent, deliverable_sha)`). Path A succeeds = A1.5 found no superseding higher-round proposal in `<output-dir>` (otherwise Path A is preempted and Path B runs with `supersession_required = true` per D4) + entry valid + 11 gates pass + verdict schema valid + mirror match + A6 late freshness recheck passes. Failure at any sub-step falls through to Path B |
| 4 | Orchestrator (Path B) | Scans `<output-dir>` for unmerged proposal matching the tuple, picks the one with latest sidecar `timing.started_at` (chronological; lex-max `run_id` is the deterministic tie-breaker — see §5.6 B2 for why `run_id` alone is not chronological). Validates proposal against `audit_artifact_entry.schema.json --mode proposal` (rejects if `verdict.verified_at` / `verdict.verified_by` are pre-filled — Pattern C3 attack surface) |
| 5 | Orchestrator (Path B) | If proposal `verdict.status == "AUDIT_FAILED"`: BLOCK without gating, surface `failure_reason`. If status is PASS / MINOR / MATERIAL: continue to step 6 |
| 6 | Orchestrator | Runs the eleven gating checks (§5.2) using paths declared in the entry's `artifact_paths` |
| 7 | Orchestrator | Validates `<run_id>.verdict.yaml` against `audit_verdict.schema.json`. On Path A also confirms verdict file's mirrored fields match the persisted entry's mirror (drift = forgery evidence) |
| 8 | Orchestrator (Path B) | If all eleven + verdict schema pass: fills `verdict.verified_at` via the strict-monotonic helper (§5.4) and `verdict.verified_by = "pipeline_orchestrator_agent"`, re-validates against `--mode persisted`, appends to passport `audit_artifact[]` |
| 9 | Orchestrator (Path B) | Moves the proposal file to `<output-dir>/consumed/<run_id>.audit_artifact_entry.json` so it is not re-merged on a later transition. Files marked `AUDIT_FAILED` (step 5 short-circuit) are NOT moved — user may inspect |
| 10 | Orchestrator | If any check fails: leaves the proposal file in place (Path B) or falls back to Path B with surfaced reason (Path A failure), surfaces the failed check to user (per §5.6 block message), no passport mutation on the failed entry |

**Invariants:**

- Wrapper NEVER writes to the passport file directly. Wrapper writes only to its `--output-dir`.
- Orchestrator is the only writer of `audit_artifact[]` entries. This mirrors the existing pattern where `reset_boundary[]` and `literature_corpus[]` are also orchestrator-mediated (or user-adapter-mediated for corpus) but never wrapper-mediated.
- `verified_at` / `verified_by` are set ONLY by the orchestrator, on one of two write paths: (a) the normal proposal-merge at lifecycle step 8 (= §5.6 Path B8d), and (b) the §5.4 `ship_with_known_residue` acknowledgement append, which uses the same write contract (verified_at = current UTC ms, verified_by = "pipeline_orchestrator_agent") and the same strict-monotonic guarantee as Path B8d. Wrappers and any non-orchestrator writer remain forbidden — a wrapper-emitted proposal file with these fields filled is treated as malformed (Pattern C3 attack surface) and rejected at lifecycle step 4 schema validation (= §5.6 Path B4).
- Lifecycle steps 6 + 7 (gating + verdict-schema validation, = §5.6 Path B6 + B7 + B8a/b/c) happen BEFORE lifecycle step 8 mutation. A failed check leaves the passport untouched; the user can re-run the wrapper with corrections without garbage entries piling up in the ledger.

**Why a separate proposal file rather than wrapper writing directly to passport:**

1. Concurrency: passport may be open in an LLM session; wrapper running from CI cannot acquire a safe lock without coordinating with the LLM session.
2. Atomicity: wrapper completion is point-in-time; passport append is point-of-trust. Separating them means a wrapper that succeeds but produces an artifact that fails verification does NOT pollute the passport.
3. Threat model: a Pattern-C3-style fake wrapper could write directly to passport if given that privilege; a fake wrapper that can only write to `--output-dir` is bounded by orchestrator gating before reaching passport state.

**Wrapper proposal file shape (`<run_id>.audit_artifact_entry.json`):**

```json
{
  "stage": 2,
  "agent": "synthesis_agent",
  "deliverable_path": "chapter_4/synthesis.md",
  "deliverable_sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
  "run_id": "2026-04-30T15-22-04Z-d8f3",
  "bundle_id": "phase2-chapter4-2026-04-30",
  "bundle_manifest_sha": "9a8b7c6d5e4f3b2a1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9876",
  "artifact_paths": {
    "jsonl": "audit_artifacts/2026-04-30T15-22-04Z-d8f3.jsonl",
    "sidecar": "audit_artifacts/2026-04-30T15-22-04Z-d8f3.meta.json",
    "verdict": "audit_artifacts/2026-04-30T15-22-04Z-d8f3.verdict.yaml"
  },
  "verdict": {
    "status": "MINOR",
    "round": 2,
    "target_rounds": 3,
    "finding_counts": {"p1": 0, "p2": 0, "p3": 1}
  }
}
```

This example shows status `MINOR` because `finding_counts.p3 == 1` — a `PASS` proposal would require all three `finding_counts` keys to be `0` per the §3.2 cross-field rule, and pairing `PASS` with any nonzero count is a schema violation that lint catches at lifecycle step 4. `verdict.verified_at` and `verdict.verified_by` are intentionally absent. Schema validation at step 4 enforces their absence in proposal files via `--mode proposal`; their presence is treated as schema error.

**Proposal entry shape on AUDIT_FAILED** (per §4.6):

```json
{
  "stage": 2,
  "agent": "synthesis_agent",
  "deliverable_path": "chapter_4/synthesis.md",
  "deliverable_sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
  "run_id": "2026-04-30T15-22-04Z-d8f3",
  "bundle_id": "phase2-chapter4-2026-04-30",
  "bundle_manifest_sha": "9a8b7c6d5e4f3b2a1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9876",
  "artifact_paths": {
    "jsonl": "audit_artifacts/2026-04-30T15-22-04Z-d8f3.jsonl",
    "sidecar": "audit_artifacts/2026-04-30T15-22-04Z-d8f3.meta.json",
    "verdict": "audit_artifacts/2026-04-30T15-22-04Z-d8f3.verdict.yaml"
  },
  "verdict": {
    "status": "AUDIT_FAILED",
    "round": 2,
    "target_rounds": 3,
    "finding_counts": {"p1": 0, "p2": 0, "p3": 0},
    "failure_reason": "codex exit 70: network timeout after 600s"
  }
}
```

Both proposal shapes (PASS/MINOR/MATERIAL completed audits AND AUDIT_FAILED aborted audits) write all four contract files; the difference is in `verdict.status` and `verdict.failure_reason`. Orchestrator §5.6 Path B5 short-circuits to BLOCK on `AUDIT_FAILED` without running gating; PASS/MINOR/MATERIAL go through the eleven gates.

---

## 5. Orchestrator block protocol

This section specifies how `pipeline_orchestrator_agent` enforces the audit gate at stage transition. The orchestrator never runs codex; it reads the passport, finds the relevant `audit_artifact[]` entry, runs the verification checks, and decides ship-or-block based on verdict.

### 5.1 Stage-transition gate locations

The audit gate fires at exactly three transitions, one per v3.6.7 agent. These are the only points in the pipeline where Step 6 hooks intervene; all other transitions retain pre-v3.6.7 behavior unchanged.

| Trigger | Producing agent | Producing skill / mode | Gate fires before | `audit_artifact.stage` value |
|---|---|---|---|---|
| `synthesis_agent` exit | `synthesis_agent` | deep-research, full mode (Phase 2 synthesis stage) | Stage 1 → Stage 2 transition (deep-research → academic-paper handoff) | **2** (destination stage) |
| `research_architect_agent` survey-designer exit | `research_architect_agent` | academic-paper, full mode (when survey instrument is in scope) | Within-skill internal transition before instrument deliverable enters Material Passport | **2** (destination stage; the survey instrument enters passport at the Stage 2 boundary) |
| `report_compiler_agent` abstract-only exit | `report_compiler_agent` | academic-paper, abstract-only mode | Before Stage 5 (FINALIZE) format conversion | **5** (destination stage) |

**Convention — destination stage, not producing stage.** The `audit_artifact.stage` field (and §5.6 Path A's `stage` tuple match, and the wrapper's `--stage` flag) carry the **destination stage**, i.e., the stage the deliverable is about to enter after passing the gate. This matches Phase 6.1's self-test invocation (`--stage 2` for the synthesis-agent gate that fires before Stage 1→2 transition) and §7.1's fixture-to-pattern mapping table values. Earlier draft prose that referred to "the just-completed pipeline stage" should be read as "the destination stage that the just-completed deliverable is about to enter" — the fix is in this table; §5.6 A1 prose has been clarified to match.

**Why these three only:** Q1 fixed scope to v3.6.7-only agents. Other transitions (Stage 1→2 RQ-brief handoff, Stage 2.5 integrity, Stage 3 review, Stage 4 revision, Stage 4.5 final integrity) retain pre-v3.6.7 behavior. The audit gate is purely additive — it does NOT replace any existing checkpoint mechanism (Mode Recommendation, Mid-Entry Material Passport Check, integrity_verification_agent, collaboration_depth_agent observer all continue to fire as today).

**Bundle semantics — independent gating, shared audit trail:** when multiple v3.6.7 agents produce deliverables in one Phase 2 batch (typical: `synthesis_agent` + `research_architect_agent` survey both ship in one chapter run), each agent's deliverable triggers its own audit gate independently at its own stage transition. The `bundle_id` field is an audit-trail tag that lets users and future maintainers reconstruct "these N audit_artifact[] entries belong to one logical chapter run"; it does NOT define a gating set.

Rationale: ARS pipeline is sequential at stage level (a stage cannot complete with a missing v3.6.7 agent's deliverable — earlier stage-completion checks would already have blocked). A "bundle vacuously passes because it is incomplete" failure mode is structurally impossible: if an agent's deliverable is missing, the stage that produces it is itself incomplete, and the audit gate never fires for the missing entry. Each present entry passes its own eleven gating checks; absent entries are caught upstream by stage-completion logic, not by the audit gate.

This mirrors audit template §4.1 D1 (multi-file > sequential) at the **prompt** level (one codex audit invocation can review multiple files together for cross-section coherence) but keeps **gating** at the per-entry level (each entry has its own verdict, its own gate).

### 5.2 The eleven verification checks

For each `audit_artifact[]` entry that gates a transition, orchestrator runs eleven checks in order. The first failing check stops verification; orchestrator does NOT compose findings across checks. Reasoning: any check failure is sufficient cause to reject the artifact; running more checks just buries the diagnostic.

The eleven checks operationalize three §3 surfaces: the Layer 2 per-row schema (§3.3), the §3.7 family A row A7 stream-shape invariant, and the §3.4 cross-file rules. Each §3.4 cross-file rule maps to exactly one Layer 3 check below; counts agree across §3 and §5 by construction.

**Layer 2 checks (codex JSONL evidence — schema-level):**

| # | Check | Implementation | Maps to |
|---|---|---|---|
| L2-1 | JSONL file exists at path declared in `artifact_paths.jsonl` | Filesystem stat | precondition |
| L2-2 | Every JSONL row validates against `audit_jsonl.schema.json` | JSON Schema validator | §3.3 schema |
| L2-3 | JSONL stream contains exactly one `thread.started` event with a canonical UUID `thread_id`; the stream opens with `thread.started` as event #1 and `turn.started` as event #2 (per §3.3 / Q3 canonical opening) | Filter events by `type == "thread.started"`; assert single match; assert it is the first row; assert second row's `type == "turn.started"`; assert `thread_id` matches `^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$` (canonical 8-4-4-4-12 layout, not the looser `^[0-9a-f-]{36}$`) | §3.3 schema-level rule |
| L2-4 | JSONL stream contains at least one `item.completed` event whose `item.type == "agent_message"`; the last such event's `item.text` parses against the audit-template Section 6 verdict shape; stream ends with a `turn.completed` event carrying `usage` integers | Filter events by `type == "item.completed"` + `item.type == "agent_message"`, assert non-empty, take the LAST match (intermediate `agent_message` events are allowed in tool-using runs — codex thinking aloud between tool calls), hand its `item.text` to `parse_audit_verdict.py --probe`; assert final event has `type == "turn.completed"` with `usage.input_tokens > 0` and `usage.output_tokens >= 0` | §3.3 schema-level rule |
| L2-5 | JSONL stream tool-event 1:1 pairing with start-before-completion order per §3.7 A7: for every non-`agent_message` tool `item.id` the stream contains exactly one `item.started` and exactly one `item.completed` with that id (no duplicate starts, no duplicate completions, no orphan completions), and the completed event appears strictly later in the stream than the matching started event; parallel tool starts may complete in any order; `agent_message` `item.completed` events are exempt (codex emits assistant messages as single completion events) | Invoke `scripts/check_audit_artifact_consistency.py --mode jsonl-stream --jsonl <path>` (Phase 6.3 contract; exits 0 on pass, non-zero with offending `item.id` on violation) | §3.7 A7 |

**Layer 3 checks (sidecar evidence — cross-file rules):**

| # | Check | Implementation | Maps to §3.4 cross-file rule |
|---|---|---|---|
| L3-1 | Sidecar file exists at `artifact_paths.sidecar` AND validates against `audit_sidecar.schema.json` | Filesystem stat + JSON Schema validator | precondition |
| L3-2 | Sidecar `stream.jsonl_thread_id` matches the JSONL's single `thread.started` event's `thread_id` | String equality | rule 1 |
| L3-3 | `prompt.bundle.primary_deliverables[].sha` matches `audit_artifact_entry.deliverable_sha` AND matches current file SHA-256 | SHA-256 recompute on disk + equality | rule 2 |
| L3-4 | `prompt.bundle.bundle_manifest_sha` matches recomputed manifest hash (per §3.6) over current state of all primary + supporting files PLUS the audit template at `prompt.audit_template_path` | Manifest reconstruct (3 roles: primary/supporting/template) + SHA-256 + equality | rule 3 |
| L3-5 | Sidecar `runner.git_sha` resolves to a real commit in current repo | `git cat-file -e <sha>^{commit}` | rule 4 |
| L3-6 | Sidecar `timing.ended_at - timing.started_at == duration_seconds` within ±1s | Datetime arithmetic | rule 5 |
| L3-7 | Sidecar `process.exit_code == 0` | Integer equality | rule 6 |
| L3-8 | `entry.run_id == sidecar.run_id` AND `sidecar.run_id` equals the bare `<run_id>` basename of every path in `artifact_paths.{jsonl, sidecar, verdict}` (always, both lifecycle modes). When running on a Path B unmerged proposal, ADDITIONALLY equals the basename of the proposal entry file (`<run_id>.audit_artifact_entry.json`) — this fourth check is proposal-mode only because §4.9 step 9 moves the proposal file to `consumed/` after merge and §3.1 intentionally does NOT record it under `artifact_paths`. All co-located artifact files share one bare `<run_id>` stem per §3.7 family F (F2/F3) | String parse of basename + equality across all required paths (3 in persisted mode, 4 in proposal mode) | §3.4 rule 7 |

Total: 5 Layer 2 + 8 Layer 3 = **13 numbered slots, of which 11 are gating checks**. L2-1 and L3-1 are preconditions (file existence + schema validity); failure of either is reported as "audit not conducted" rather than "audit fake-detected", because either case is structurally indistinguishable from "audit never ran".

The eleven gating checks are L2-2, L2-3, L2-4, L2-5, L3-2, L3-3, L3-4, L3-5, L3-6, L3-7, L3-8.

**Composite forgery cost:** L2-3 ensures internal JSONL consistency. L2-5 closes the orphan-tool-completion forgery hole (a forger emitting a fabricated `command_execution` `item.completed` without a matching `item.started` would have evaded the per-row schema check). L3-2 cross-bridges JSONL ↔ sidecar. L3-3 + L3-4 pin all bundle file content. L3-5 anchors to repo history. L3-6 ensures temporal arithmetic self-consistency. L3-7 closes the "audit ran but failed" hole. L3-8 closes the "swap one of the four artifact files for a different run's file" hole — without L3-8 a forger could pair a real sidecar from run X with a fabricated verdict from run Y, since per-file schemas would still validate. Cumulative cost makes running real codex the economical path under the §1.2 threat model.

**Verdict file is read AFTER all eleven gating checks pass.** Orchestrator does NOT read `verdict.yaml` until Layer 2 + Layer 3 are clean; this prevents a forged verdict from leaking into orchestrator state via partial evidence.

### 5.3 Verdict semantics and ship/block decisions

Once all eleven gating checks pass, orchestrator validates `verdict.yaml` against `audit_verdict.schema.json` (§3.5). Schema-failed verdict files BLOCK with a diagnostic regardless of how cleanly Layer 2 + Layer 3 verified — schema validation is a separate trust boundary from artifact integrity. After schema validation passes, orchestrator decides per these rules:

**Rows are evaluated top-to-bottom; the first row whose Definition matches the latest entry wins.** This makes the acknowledgement override explicit rather than leaving an implementer to infer precedence between MATERIAL and MATERIAL + acknowledgement.

| Verdict | Definition | Orchestrator action |
|---|---|---|
| **PASS** | `finding_counts.{p1,p2,p3}` all zero | Proceed to next stage; emit FULL checkpoint with `[Audit: PASS at round N]` line |
| **MINOR** | `p1 == 0 AND p2 == 0 AND p3 <= 3` | MANDATORY checkpoint with finding details; user choice required (`continue` to ship, `iterate` to dispatch revision, `pause` to stop) |
| **MATERIAL + acknowledgement** *(higher-precedence override of the MATERIAL row below)* | latest entry's `verdict.status == "MATERIAL"` AND latest entry carries an `acknowledgement` object whose `finding_ids` covers EVERY current `findings[].id` from the companion verdict file | Proceed to next stage; emit FULL checkpoint with `[Audit: MATERIAL at round N, residue acknowledged by user at <acknowledged_at>]` line |
| **MATERIAL** *(no acknowledgement, or acknowledgement coverage incomplete)* | `p1 > 0 OR p2 > 0 OR p3 > 3` AND latest entry either has no `acknowledgement` object OR its `acknowledgement.finding_ids` does not cover every current `findings[].id` | Block; refuse stage transition; surface findings; require revision + new audit round. Note: the second branch (incomplete coverage) is unreachable under the lint rules at §5.4 (full coverage enforced at acknowledgement-write time, not at ship-decision time); it is named here for defense-in-depth so a hand-edited passport entry that violates the lint rule still fails closed |

**MATERIAL handling details:**

- Orchestrator emits a structured block notification (§5.6 template) listing the findings.
- The producing agent's mode (e.g., `synthesis_agent`) is re-invoked with a "revision based on audit findings" prompt that lists each P1/P2 finding with its dimension and suggested fix.
- After revision, deployment runs the wrapper again with `--round N+1 --previous-findings <prior verdict.yaml>` to produce the next round audit. Orchestrator picks up the new `audit_artifact[]` entry on the next transition attempt.

**MINOR handling details:**

- P3 (editorial) findings within the MINOR threshold (`p3 <= 3` per §5.3) do not block; they are surfaced to the user as a punchlist for author final pass. P3 findings exceeding the threshold (`p3 > 3`) trigger MATERIAL per §5.3 and follow the MATERIAL handling path.
- The MANDATORY checkpoint (not FULL) is used because P3 findings have direct user-action implications even when they don't block — bypassing user awareness with a SLIM auto-continue would lose the editorial punchlist.

**PASS handling details:**

- The `[Audit: PASS at round N]` line is appended to the FULL checkpoint's Flagged section, marked as informational. Pre-v3.6.7 Flagged behavior (integrity issues, metric anomalies) is preserved; audit verdict is additive.

### 5.4 Round upper bound (resolves L1 from §2.3)

**Decision:** default 3 rounds matching audit template Section 1 default `target_rounds`. Escalate to user after round 3 still MATERIAL.

**Rationale:** `feedback_codex_iterative_spec_review_to_zero.md` says "iterate to one zero-finding round" but does not bind the iteration count; `feedback_cross_model_review_cascade_inconsistency.md` and `feedback_codex_review_vs_resume_audit_scope.md` both observe round-3 as the typical convergence point under cascade-aware audits. Setting hard upper bound at 3 aligns with empirical convergence observation; a higher cap delays escalation without quality gain in observed runs.

**Escalation behavior at round 3 still MATERIAL:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ESCALATION] v3.6.7 audit gate at <stage>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Audit on <agent>'s deliverable at <deliverable_path> reached round 3
without convergence. Current verdict: MATERIAL with <P1> P1 + <P2> P2 + <P3> P3.

Per ARS feedback feedback_codex_review_vs_resume_audit_scope.md "stop
condition: N rounds OR 'add counter, not change rule' findings".

Findings (round 3):
<finding list>

Options:
1. ship_with_known_residue — Acknowledge findings, ship anyway (orchestrator
   appends a new `audit_artifact[]` entry whose `acknowledgement.finding_ids`
   carries the IDs the user accepted; not silent).
2. another_round — Override the 3-round cap, dispatch round 4 audit.
3. abort_stage — Return to producing agent, scrap deliverable, restart.

This decision requires explicit user input.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**`ship_with_known_residue` mechanism (preserves append-only ledger):** orchestrator does NOT mutate the existing MATERIAL entry. It appends a NEW `audit_artifact[]` entry that copies the latest persisted entry's `(stage, agent, deliverable_path, deliverable_sha, run_id, bundle_manifest_sha, artifact_paths)` and the inner verdict shape `(verdict.status, verdict.round, verdict.target_rounds, verdict.finding_counts, verdict.failure_reason)`, then sets `verdict.verified_at` to the current UTC and `verdict.verified_by` to `"pipeline_orchestrator_agent"` (the same fields orchestrator fills at §4.9 step 8 for normal merges — acknowledgement append uses the same write contract, not a copy of the prior verification timestamp), and adds the optional `acknowledgement` object defined in §3.2 (`{finding_ids, acknowledged_at: <same UTC>, acknowledged_by: "user"}`). Refreshing `verified_at` rather than copying it is load-bearing for §3.1's "Orchestrator reads the latest entry by `verified_at` for verdict" — without the refresh, the acknowledgement entry would tie with the original MATERIAL entry on `verified_at` and Path A selection would be ambiguous. With the refresh, the acknowledgement entry strictly post-dates every prior entry and Path A deterministically picks it.

**Atomicity for ack append:** the new `audit_artifact[]` entry is appended to the passport via the same tmp-write + fsync + atomic rename pattern §5.6 B9 specifies for Path B normal merges (write the new passport content to `<passport_path>.tmp`, fsync the tmp file, then `mv -f` over the live passport). This guarantees that a crash between ack-decision and passport-commit leaves the passport in its pre-ack state — the ack is either fully committed or not at all. Combined with §5.6 B1a / B8b idempotent run_id de-duplication, a partially-committed ack append cannot produce a duplicate persisted entry on resume.

**Strict-monotonic guarantee (single helper for every orchestrator-side append):** ms precision (§3.2 cross-section consistency rule on `verdict.verified_at`) gives 1 ms resolution, but a same-process append running faster than 1 ms could still tie with the latest persisted entry's `verified_at`. Every orchestrator-side `verified_at` write — Path B8d normal merges (§4.9 step 8 / §5.6 B8d), `another_round` re-merges, and `ship_with_known_residue` acknowledgement appends — goes through one helper, written here in pseudocode and shipped as `scripts/_next_verified_at_ms.py` (consumed by both the orchestrator and the lint script):

```
def _next_verified_at_ms(passport_audit_artifacts: list) -> str:
    now_ms = utc_now_ms()                        # RFC 3339 UTC ms precision
    if not passport_audit_artifacts:             # empty-ledger base case
        return now_ms                            # no prior entry to outrun
    latest_ms = max(entry["verdict"]["verified_at"]
                    for entry in passport_audit_artifacts)
    return max(now_ms, increment_ms(latest_ms, 1))  # 1 ms after latest if clock has not yet advanced
```

The acknowledgement append additionally writes the helper's return value to `acknowledgement.acknowledged_at` so the two timestamps share the same instant by construction (§3.7 family B row B8 carries the equality lint rule). Because `latest_ms` is the max over ALL prior persisted entries (not just those matching the current `(stage, agent, deliverable_sha)` tuple), the helper guarantees the new entry's `verified_at` is strictly greater than every prior persisted entry's `verified_at` regardless of whose tuple wrote them; Path A latest-by-`verified_at` selection is therefore total-order deterministic at passport scope. The new ack entry's `verdict.status` remains `MATERIAL` — acknowledgement is a sibling annotation, not a status mutation (§3.7 family E row E7). This preserves the v3.6.3 `reset_boundary[]` append-only-ledger pattern (§3.1 closing paragraph) and means a future reader can see both "audit said MATERIAL" and "user acknowledged residue X, Y, Z" as separate facts in the ledger. The three `acknowledgement.finding_ids` lint rules (non-empty / every ID exists in companion verdict file / full coverage of every current finding) live in §3.7 family B row B10; they are checked at acknowledgement-write time and re-checked at §5.6 Path B persisted-mode validation, and rule 3 (full coverage) is what §5.3's "MATERIAL + acknowledgement" row depends on so partial residue acknowledgement is rejected at write time and orchestrator never handles it at ship-decision time.

The `ship_with_known_residue` option therefore creates a non-silent paper trail: the passport carries both the original MATERIAL audit verdict and the user's explicit acknowledgement entry, anyone reading it sees both. This matches the v3.6.6 spec philosophy of "transparency over enforcement" for boundary cases the user must own.

**Override mechanics:** the user's `another_round` choice MUST be encoded as a new `(round, target_rounds)` pair where the wrapper is re-invoked with `--round N+1 --target-rounds N+1`. The schema invariant `round <= target_rounds` (§3.2 cross-field rule) and the wrapper input rule "round must be <= target-rounds" (§4.2) both hold. Every escalation is a fresh user-owned decision that explicitly raises the cap by 1; this prevents the user from accidentally extending iteration without acknowledging that the original 3-round target was missed. Multiple escalations append additional `audit_artifact[]` entries with monotonically increasing `round` and matching `target_rounds`. There is no path that drifts toward unbounded iteration without per-escalation user consent.

**`another_round` is committed by the wrapper artifact, not by orchestrator state (F-070 closure):** the user's `another_round` choice is durable only after the higher-round wrapper run produces a proposal in `<output-dir>` carrying `verdict.round = N+1` for the same `(stage, agent, deliverable_sha)` tuple. §5.6 A1.5's superseding-proposal preflight is what makes that proposal preempt the prior round-N MATERIAL persisted entry at the next gate — without A1.5, Path A would succeed on the prior entry and the user-dispatched higher-round proposal would never be merged. If the orchestrator session crashes between the user clicking `another_round` and the wrapper actually producing the higher-round proposal, the pending intent is intentionally NOT durable: on resume, Path A finds the round-N MATERIAL entry, runs A1.5 (no superseding proposal exists), succeeds at A7 with the prior MATERIAL verdict, and the §5.4 ESCALATION prompt fires again. This is "repeated authorization prompt", not "silent ship of stale verdict" — failing closed in a way the user can re-act on.

**Byte-identical `abort_stage` and manual fresh audits (F-070 generalization):** if the user picks `abort_stage`, the producing agent re-runs and either (a) produces a different deliverable byte-sequence — `deliverable_sha` changes, Path A finds no matching tuple, Path B runs fresh — or (b) produces the byte-identical deliverable. In case (b), the prior MATERIAL persisted entry still matches the tuple, and unless the wrapper is re-invoked with a higher round, A1.5 finds no superseding proposal and Path A returns the prior MATERIAL verdict. **If the user wants the byte-identical re-audit to supersede the prior verdict, the wrapper MUST be invoked with `--round N+1 --target-rounds N+1`** (same rule as `another_round`). The same rule applies to any deployment-side wrapper run dispatched outside the §5.4 escalation prompt: a fresh wrapper run that uses `--round 1` will not preempt a prior MATERIAL entry; only `--round N+1` (where N is the prior persisted entry's round) will trigger A1.5 supersession.

### 5.5 Pre-existing checkpoint co-occurrence

Step 6 audit gate must not collide with pre-v3.6.7 checkpoint mechanisms. Co-occurrence rules:

| Pre-existing mechanism | Audit gate co-occurrence rule |
|---|---|
| FULL checkpoint | Audit verdict appended to Decision Dashboard as informational line; does not change checkpoint type |
| MANDATORY checkpoint (integrity) | Audit gate runs FIRST. If MATERIAL, integrity checkpoint never fires (deliverable is rolled back to producing agent before reaching Stage 2.5/4.5). If PASS, integrity proceeds normally. |
| MANDATORY checkpoint (review decision) | Same: audit gate runs FIRST at the producing agent's exit; review checkpoint runs at Stage 3 (downstream). No collision. |
| collaboration_depth_agent observer | Observer fires on FULL/SLIM checkpoint dispatch as today; orchestrator's audit verification happens BEFORE observer dispatch. Observer does NOT see audit findings (per its v3.5 advisory-not-blocking design). |
| ARS_PASSPORT_RESET reset boundary | Audit_artifact[] entries serialize into passport per Schema 9 append-only ledger semantics, layered on top of the v3.6.3 reset-boundary protocol (`academic-pipeline/references/passport_as_reset_boundary.md` — the canonical contract for what `ARS_PASSPORT_RESET` and `resume_from_passport` mean and how they interact with the `reset_boundary[]` ledger). On `resume_from_passport=<hash>`, orchestrator re-reads audit_artifact[] from passport and re-runs the eleven gating verification checks — they MUST still pass even after session reset (note: L3-3 / L3-4 require recomputing SHAs against current file contents, so a deliverable mutated between original session and resume will correctly fail freshness). **On resume the orchestrator must also apply §5.6 A1.5 superseding-proposal preflight against `<output-dir>` before trusting any prior persisted entry — a higher-round wrapper run dispatched between sessions (e.g., the user clicked `another_round` in session A and the wrapper completed under CI before session B resumes) must preempt the prior entry per D4, otherwise resume would silently use the stale verdict (F-070 generalization across resume).** (Resolves L3 from §2.3 — see §9 R4 for full risk discussion.) |
| Mid-Entry Material Passport Check | Existing logic (verification_status / 24h freshness / version_label diff) runs as today. Audit_artifact[] is a separate gate downstream of this entry check. |

### 5.6 Pipeline orchestrator agent prompt update

Step 6 adds one new subsection (§3.5 Audit Artifact Gate) to `academic-pipeline/agents/pipeline_orchestrator_agent.md`, inserted between current §3 "Checkpoint Management" and §4 "Transition Management" — audit gate runs at transition time, so structurally it belongs in transition flow.

**Prompt-vs-spec split (load-bearing for Phase 6.6 implementers).** The fenced ` ```markdown ` block below is the **complete spec-side reference** (~347 lines) describing the orchestrator's runtime gate procedure. **It is NOT inserted verbatim into the orchestrator prompt.** Phase 6.6 ships a ~50-line decision-policy summary (trigger, ship/block decision rule, hard rules, cross-references, plus the P-PA-* / P-PB-* failure phase IDs as cross-references back here) into the orchestrator prompt; the procedural detail (Path A → Path B fall-through, A1–A7, B1–B11, A1.5 supersession preflight, B1a/B8b/B8c recovery, F-067 / F-069 / F-070 / F-072 closures, the 24-row Failure State Inventory at the end of this section — 7 P-PA-* rows + 17 P-PB-* rows) stays in this spec as the implementation contract. The closing prose after the fenced block, the §9.1 R3 risk entry, the §10 Phase 6.6 verification gate, and `docs/design/2026-05-05-phase-6.6-scoping-note.md` §3 Path 2 all describe the same split and must stay co-consistent. An implementer who reads only the fenced block and copies it into the prompt would blow the +60-line gate by ~580% — read §10 Phase 6.6 deliverable and the closing prose alongside the block before editing the orchestrator prompt.

```markdown
### 3.5 Audit Artifact Gate (v3.6.7 Step 6)

**Trigger.** At every stage transition where a v3.6.7 downstream agent
(`synthesis_agent` / `research_architect_agent` survey-designer mode /
`report_compiler_agent` abstract-only mode) just completed a deliverable.

**Procedure (Path A → Path B fall-through model).**

The orchestrator first attempts Path A (already-merged persisted entry). Path A's A1.5 step always scans `<output-dir>` for superseding higher-round proposals (per D4); if a superseding proposal exists, Path A is preempted and Path B runs with `supersession_required = true`. Otherwise Path A continues to A2-A7. If Path A succeeds end-to-end, the gate passes by reading the persisted entry's verdict (the wrapper output directory was scanned at A1.5 but no proposal was merged). If Path A finds no matching persisted entry OR finds one but it fails A3-A6 verification (stale SHAs, broken sidecar, etc.) OR is preempted by A1.5 supersession, orchestrator falls through to Path B (look for a fresh proposal that supersedes the failed/preempted entry). This ordering avoids the deadlock where a stale persisted entry blocks the user's freshly-run audit from being merged AND closes the F-070 escalation deadlock where a higher-round user-dispatched proposal would have been silently ignored.

**Path A — already-merged entry (re-verification on resume / re-transition):**

A1. Search passport `audit_artifact[]` for the latest persisted entry matching:
    - `stage` = the destination stage the just-completed deliverable is about
      to enter (per §5.1 destination-stage convention: 2 for `synthesis_agent`
      and `research_architect_agent` survey-designer; 5 for
      `report_compiler_agent` abstract-only)
    - `agent` = the just-completed v3.6.7 agent
    - `deliverable_sha` = SHA-256 of the just-completed deliverable file
    - latest by `verified_at` if multiple match (when multiple entries
      share the same `run_id` — possible only via §5.4
      `ship_with_known_residue` ack append, where the ack entry copies the
      original MATERIAL entry's `run_id` — pick the latest by `verified_at`
      within that `run_id` group; D3 strict-monotonic guarantees the ack
      entry post-dates the original by ≥ 1 ms, so this resolves
      deterministically).
A1.5. **Superseding proposal preflight (F-070 closure):** scan
    `<output-dir>` for unmerged proposal entries matching the same
    `(stage, agent, deliverable_sha)` tuple. After applying B1a-style
    `run_id` de-duplication (any proposal whose `run_id` already appears
    in passport `audit_artifact[]` for this tuple is a leftover from a
    prior session's post-B9 / pre-consume crash; move it to `consumed/`
    best-effort and exclude from this scan). If any remaining proposal's
    `verdict.round` is greater than the A1-selected persisted entry's
    `verdict.round`, GO TO Path B with `supersession_required = true`.
    Path A is preempted because the user (or deployment) has dispatched
    a higher-round audit that the spec contract requires the orchestrator
    to consider before trusting an older verdict — covers `another_round`
    user choice (§5.4), manual fresh wrapper run outside the §5.4
    prompt, byte-identical `abort_stage` re-audit, AND higher-round
    `AUDIT_FAILED` proposal (a higher-round AUDIT_FAILED proposal must
    preempt because falling back to the prior MATERIAL would silently
    erase the attempted escalation; Path B5 short-circuit then BLOCKs
    with the failure reason, which is the correct user-visible signal).
    If no superseding proposal exists, continue to A2 with the A1-
    selected entry.
A2. If no matching entry from A1 (and A1.5 found no superseding proposal): GO TO Path B (no Path A candidate).
A3. Validate the entry against `audit_artifact_entry.schema.json --mode persisted`
    (`verdict.verified_at` and `verdict.verified_by` MUST be present). On schema
    failure: GO TO Path B (Path A entry is malformed and a fresh proposal may
    supersede it).
A4. Re-run the eleven gating verification checks (§5.2). On resume the L3-3 / L3-4
    SHA recompute is what catches deliverable mutation since the original session.
    First failure: GO TO Path B (entry is stale; look for a fresh proposal that
    supersedes it).
A5. All eleven pass: read `<run_id>.verdict.yaml`, validate against
    `audit_verdict.schema.json`. On schema failure: GO TO Path B. On schema pass,
    confirm the verdict file's mirrored fields (`verdict_status`, `round`,
    `target_rounds`, `finding_counts`) match the persisted entry's mirror — drift
    is treated as Pattern C3 evidence (verdict file was forged or corrupted
    post-merge): GO TO Path B.
A6. **Late freshness barrier**: immediately before applying ship/block,
    re-run L3-3 (deliverable SHA) and L3-4 (bundle manifest SHA) against
    current on-disk file contents. The earlier A4 eleven-gate run captured
    the bundle state at gate-check time; a deliverable or supporting file
    that mutated between A4 and now would otherwise let orchestrator
    apply a ship/block decision on stale evidence. First failure here:
    GO TO Path B (the entry's audit is stale; look for a fresh proposal
    that supersedes it).
A7. All checks pass: apply ship/block per §5.3. **Do NOT append or mutate
    the entry** — it is already in passport. Path A succeeded; Path B is
    skipped.

**Path B — proposal file (first-time merge OR supersede a failed Path A entry):**

B1. Scan `<output-dir>` for an unmerged `<run_id>.audit_artifact_entry.json`
    matching the same `(stage, agent, deliverable_sha)` tuple. **Snapshot the
    candidate set** at scan start — record each candidate's `(filename,
    file_mtime, sidecar_mtime)` triple. The snapshot is what B2 selects
    against; later steps (B6 / B8c) will compare the snapshot's
    triples against current filesystem state and BLOCK if they differ
    (concurrent wrapper writes during orchestrator scan would otherwise
    create a TOCTOU race between selection time and verification time).
    Files in `consumed/` subdirectory are excluded — already merged.
B1a. **Idempotent run_id de-duplication**: for every candidate proposal in
    the B1 snapshot, check whether passport `audit_artifact[]` already
    contains a persisted entry with the same `run_id`. If yes, treat that
    proposal as already consumed and split by whether the duplicate
    persisted entry matches the current gate tuple `(stage, agent,
    deliverable_sha)`:
    - **Tuple matches** (the persisted entry IS an audit answer for
      this gate): branch by `supersession_required`:
      * **`supersession_required = false`** (no higher-round proposal
        in `<output-dir>` per A1.5): attempt to move the leftover
        proposal to `<output-dir>/consumed/<run_id>.audit_artifact_entry.json`
        (best-effort, log on failure but do not block), then **proceed
        as if Path A had selected this persisted entry — re-run Path A
        steps A3 (schema validation) → A4 (eleven gating checks) → A5
        (verdict file schema + mirror match) → A6 (late freshness
        barrier) against it before applying ship/block at A7**. This is
        what makes the tuple-match branch safe: a prior session committed
        the persisted entry, but between that commit and the current
        session the deliverable / bundle files / verdict file may have
        mutated, gone missing, or been hand-edited. Skipping straight to
        B10 (the original Round 13 closure) would let orchestrator
        apply a ship/block decision on a stale or untrusted entry.
        Re-running A3-A6 in this branch enforces the same trust boundary
        as a normal Path A entry.
      * **`supersession_required = true`** (A1.5 found a higher-round
        proposal that must preempt the prior persisted entry): the dup
        is a same-tuple already-persisted lower-or-equal-round entry
        (it may be the A1-selected latest entry, or it may be an older
        round entry whose leftover proposal was never consumed — e.g.,
        passport carries rounds 1, 2, 3 with A1 selecting round 3, while
        a round-2 leftover proposal sits in `<output-dir>` because that
        prior session never reached B9 consume). In either case, the
        dup's `verdict.round <= selected_persisted.verdict.round`, and
        the user-dispatched higher-round proposal MUST win. Move the
        leftover proposal to `consumed/` (best-effort) and **remove
        this dup from the B1 candidate set without re-running A3-A6**
        — re-validating and shipping the prior round verdict (whether
        round-N or older round-N-k) would silently override the user's
        `another_round` choice (F-072 closure). Continue B1a processing
        with remaining candidates; B2 supersession-mode filter then
        selects the higher-round
        proposal and the merge proceeds normally.
      If A3-A6 fails (only reachable in the supersession-false branch):
      remove ONLY this consumed duplicate from the B1 candidate set and
      continue B1a processing with any remaining candidates (those
      candidates may include fresh round-N+1 proposals that supersede
      the failed entry — see §5.4 `another_round` mechanism). If after
      B1a the candidate set is non-empty, proceed normally to B2
      selection. If after B1a the candidate set is empty (the only
      candidate was the failed-revalidation duplicate, and no fresh
      proposal exists), the procedure falls through to B3 BLOCK with
      the carried-forward failure reason: `[AUDIT GATE: prior persisted
      entry <run_id> failed re-validation: <reason>; please re-audit]`
      — same diagnostic shape as a normal Path A → Path B fall-through.
      Closes the false-BLOCK race the original Round 13 closure
      addressed AND closes the unsafe-trust window F-067 surfaced AND
      closes the F-069 multi-candidate cascade where a single failed
      re-validation would have prematurely BLOCKed even when other
      valid candidates existed AND closes the F-072 supersession
      short-circuit where a lower-round leftover dup would have used
      the prior verdict instead of yielding to the higher-round
      proposal.
    - **Tuple does not match** (the persisted entry is for a different
      gate, e.g., a stage / agent / deliverable that happens to share
      `run_id` — possible only under hand-edit since wrappers generate
      `run_id` randomly per `/dev/urandom`): the leftover proposal is
      not relevant to this gate. Best-effort move to `consumed/`, then
      remove it from the current B1 candidate set and continue B1
      processing with the remaining candidates (proceed normally to B2).
    Together these closures of the crash-window ensure the next session
    cannot re-merge the same proposal (no duplicate persisted entry) AND
    cannot false-BLOCK on a proposal that already has a committed audit
    answer in the passport.
B2. Selection from the candidate set:
    - **Default mode** (no `supersession_required` flag from A1.5): pick
      the proposal with the latest sidecar `timing.started_at` (RFC 3339
      ms precision per §3.4 — strictly chronological, independent of
      `run_id` random suffix). Tie-break on `run_id` lexicographic max
      as a deterministic secondary key (the `<ISO-8601-Z>-<4-hex>` random
      suffix is not chronologically meaningful at sub-second resolution
      because the suffix is sampled from `/dev/urandom` per §4.3 —
      lexicographic max on `run_id` alone is therefore not chronological
      and is reserved here only for total-order determinism on identical
      `started_at`). When Path A fell through on a stale entry, B2 selects
      the fresh proposal that supersedes the failed entry; the prior
      persisted entry remains in the append-only ledger as historical
      record.
    - **Supersession mode** (`supersession_required = true` from A1.5):
      filter the candidate set to only proposals whose `verdict.round`
      is greater than the A1-selected persisted entry's `verdict.round`.
      Then apply the same `started_at` primary / `run_id` lex-max
      tie-breaker selection within the filtered set. This guarantees the
      higher-round audit explicitly dispatched by the user (or deployment)
      is what gets merged, not an older same-tuple proposal that happened
      to be in `<output-dir>`.
    Reading `timing.started_at` requires opening the proposal's companion
    sidecar; proposals whose sidecar fails Layer 3 schema validation (B6
    below) are rejected at that stage rather than being selected and then
    rejected — but if multiple proposals tie on `started_at` AND share an
    unreadable sidecar, orchestrator BLOCKs with `[AUDIT GATE: ambiguous
    proposal selection at <output-dir>; multiple unverifiable sidecars
    share started_at]` rather than guessing.
B3. If no proposal file: behavior depends on whether A1.5 set
    `supersession_required`:
    - **No supersession**: BLOCK transition. Display
      `[AUDIT GATE BLOCKED: no audit artifact for <agent>/<deliverable>]`
      with the exact wrapper command the user can run:
      `scripts/run_codex_audit.sh --stage <N> --agent <A> --deliverable <P> --round 1`.
      If Path A fell through with a specific failure reason, also surface that:
      `[AUDIT GATE: prior persisted entry <run_id> failed Path A: <reason>; please re-audit]`.
    - **Supersession required but no eligible proposal survives B2's
      higher-round filter** (i.e., the candidate set after B2 filtering
      is empty — every candidate was either lower-round or invalid at
      B2 selection time): BLOCK with `[AUDIT GATE: requested
      higher-round audit artifact is missing; expected
      verdict.round > <prior_round> for tuple (stage=<N>, agent=<A>,
      deliverable_sha=<sha>); please re-audit at round <prior_round + 1>]`.
      (Note: a higher-round proposal that DOES pass B2 selection but
      then fails B6 eleven-gate or B7 verdict-schema is NOT this case — it
      gets the normal P-PB-gate / P-PB-verdict-schema BLOCK with the
      proposal-specific failure diagnostic, leaving the proposal in
      `<output-dir>` for re-audit.)
      Do NOT silently fall back to Path A reading the prior persisted
      entry — the user explicitly requested supersession via §5.4
      `another_round` (or the deployment dispatched a higher-round
      wrapper run), and silently using the prior verdict would erase
      that authorization.
B4. Validate the proposal against `audit_artifact_entry.schema.json --mode proposal`.
    Reject if `verdict.verified_at` / `verdict.verified_by` are pre-filled (Pattern
    C3 attack surface — wrapper must NEVER set these; only orchestrator does).
B5. **AUDIT_FAILED short-circuit**: if proposal carries
    `verdict.status == "AUDIT_FAILED"` (per §4.6), BLOCK transition WITHOUT
    running the eleven gating checks. The audit was attempted but did not produce
    a verdict; gating against incomplete evidence is meaningless. Surface the
    `verdict.failure_reason` to the user. Do not move proposal to `consumed/`
    (user may want to inspect). User must dispatch a fresh wrapper run.
B6. Run the eleven gating verification checks (§5.2) using the paths declared in
    the proposal. First failure stops; surface the failed check and leave the
    proposal file in place for re-audit.
B7. If all eleven pass: validate `<run_id>.verdict.yaml` against
    `audit_verdict.schema.json`. On schema failure, BLOCK with diagnostic.
    Then confirm proposal entry mirrored fields
    (`verdict.{status, round, target_rounds, finding_counts, failure_reason}`)
    match `verdict.yaml` exactly — drift between proposal mirror and verdict
    file is treated as Pattern C3 evidence (wrapper or hand-edit corrupted
    one of them) and BLOCKS. The mirror persisted into Schema 9 is sourced
    from `verdict.yaml`, not the proposal, so `verdict.yaml` wins on any tie.
B8a. **Late freshness barrier** (mirrors A6): immediately before mutating
    proposal → persisted, re-run L3-3 (deliverable SHA) and L3-4 (bundle
    manifest SHA) against current on-disk file contents. The B6 eleven-gate
    run captured the bundle state at gate-check time; a deliverable or
    supporting file that mutated between B6 and now would otherwise let
    orchestrator persist a verdict on stale evidence. First failure here:
    BLOCK with `[AUDIT GATE: bundle mutated post-gate, before persist;
    re-audit required]`, leave the proposal file in place for re-audit.
B8b. **Idempotent re-check** (covers a different window than B1a, despite
    the surface similarity): re-confirm passport `audit_artifact[]` does
    not already contain a persisted entry with this `run_id`. Defends
    against the narrow window where another orchestrator session merged
    the same proposal between B1a and B8b. **Unlike B1a, B8b does NOT
    re-run A3-A6 on the duplicate persisted entry**, because the current
    session has already validated the candidate proposal at B6 (eleven
    gating checks against current on-disk file state) + B7 (verdict file
    schema + mirror match) + B8a (late freshness recheck of L3-3/L3-4) —
    those checks established the same trust boundary A3-A6 would
    establish on the duplicate persisted entry, so re-running would
    duplicate work. If a duplicate is now present: skip the persist
    (treat as already-merged), move proposal to `consumed/`, GO TO B10
    reading the pre-existing persisted entry's verdict.
B8c. **Snapshot integrity check**: re-stat the proposal file and its
    sidecar; compare `(file_mtime, sidecar_mtime)` against the B1
    snapshot. If either mtime changed, BLOCK with `[AUDIT GATE: proposal
    or sidecar mutated between scan and persist; re-scan required]` and
    return to B1 for a fresh scan.
B8d. Construct the persisted entry **in memory only** by copying the proposal
    file's parsed object and adding `verdict.verified_at` (via §5.4's
    strict-monotonic helper) and `verdict.verified_by =
    "pipeline_orchestrator_agent"`. **MUST NOT rewrite the proposal file on
    disk** — the proposal file remains a pure proposal until B9's
    consume-move (or B1a/B8b idempotent move on the recovery path). This
    guarantee is load-bearing for crash recovery: a crash between B8d and
    B9 leaves the proposal file unchanged on disk, so the next session's
    B4 `--mode proposal` validation still accepts it for re-merge. If
    implementer rewrote the proposal file at B8d (filling verified_at /
    verified_by), the next-session B4 would reject it as "wrapper-emitted
    proposal with verified_at filled" (Pattern C3 attack surface) and the
    audit would be irrecoverably blocked. Re-validate the in-memory object
    against `audit_artifact_entry.schema.json --mode persisted`; on
    validation failure, BLOCK without proceeding to B9.
B9. Append the persisted entry to passport `audit_artifact[]` via tmp-write
    + fsync + atomic rename (write the new passport content to
    `<passport_path>.tmp`, fsync the tmp file, then rename over the live
    passport — same atomicity pattern §4.4 requires for wrapper output).
    On atomic-rename success, move proposal file to
    `<output-dir>/consumed/<run_id>.audit_artifact_entry.json` (best-effort;
    failure to move logs a warning but the persisted entry is committed —
    B1a's de-duplication catches the leftover proposal on the next session).
    Crash window: if orchestrator crashes between passport rename and
    proposal move, the next session sees the persisted entry AND the
    unmoved proposal; B1a de-duplication then idempotently moves the
    proposal to `consumed/` and skips the merge.
B10. Apply ship/block per §5.3:
    - PASS → proceed to next stage; append audit line to FULL checkpoint
    - MINOR → MANDATORY checkpoint with finding punchlist; await user choice
    - MATERIAL → BLOCK; surface findings; await re-audit (with bumped
      target_rounds if user selects `another_round`, per §5.4)
B11. After round == target_rounds rounds with MATERIAL: emit ESCALATION block per
    §5.4; await user ship_with_known_residue / another_round (bumps cap by 1) /
    abort_stage choice.

**Path selection invariants (revised under Path A → Path B fall-through and A1.5 superseding-proposal preflight):**
- Path A is attempted first whenever a matching persisted entry exists, BUT
  **Path A success is preempted by A1.5's superseding-proposal preflight**:
  if `<output-dir>` carries an unmerged proposal for the same tuple with
  `verdict.round > selected_persisted.verdict.round`, A1.5 forces Path B to
  run with `supersession_required = true` and Path A is skipped entirely.
  This is what closes F-070's `another_round` deadlock and equivalent
  user-dispatched higher-round flows (manual fresh wrapper run, byte-
  identical `abort_stage` re-audit, higher-round AUDIT_FAILED proposal).
- Outside the supersession case, Path A succeeds only when the entry
  validates AND the eleven gating checks pass AND the verdict file is
  schema-valid AND mirror fields match.
- Path A failure at any step (A2 / A3 / A4 / A5 / A6) falls through to Path B with
  the failure reason carried forward. This closes the deadlock: a stale
  persisted entry no longer blocks a fresh proposal from being merged.
- Path B's proposal selection (B2) is by latest sidecar `timing.started_at`
  (chronological, ms precision) with `run_id` lex-max as deterministic
  tie-breaker — guarantees the latest fresh proposal supersedes any prior
  failed entries even when same-second `run_id` random suffixes would have
  otherwise sorted incorrectly. In supersession mode (A1.5 set the flag),
  B2 additionally filters the candidate set to proposals whose
  `verdict.round > selected_persisted.verdict.round`.
- Path A never appends to passport (entry already there). Path B always appends
  exactly one persisted entry per successful merge — including when it
  supersedes a prior failed Path A entry. The append-only ledger preserves
  history of both the failed entry AND the superseding entry.
- Failed Path A entries are NOT deleted from passport (append-only). They
  remain as audit history. Future Path A attempts on the same entry will fall
  through again until a fresh proposal supersedes via Path B.

**Hard rules.**
- Audit gate cannot be skipped via mode switch. There is no "skip audit"
  option in checkpoint command vocabulary.
- Audit gate runs BEFORE collaboration_depth_agent observer dispatch
  and BEFORE integrity_verification_agent dispatch — it is the first
  transition-time check.
- A `verdict_status: PASS` does NOT imply integrity check is skipped.
  Stage 2.5 / 4.5 integrity gates remain mandatory per existing
  spec §3 "Hard boundaries" rule 9.

**Failure surfacing.** Any block message uses the standard FULL/MANDATORY
checkpoint visual (━━━ separator) so user attention is preserved.
Block message MUST include:
- Why blocked (which check failed, or which severity finding triggered)
- Where to look (file:line for findings; artifact path for verification failures)
- What to do next (re-audit command, revision dispatch, escalation options)

**Cross-references.**
- v3.6.7 Step 6 spec: docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md
- Audit template: shared/templates/codex_audit_multifile_template.md
- Schema: shared/contracts/passport/audit_artifact_entry.schema.json
- Wrapper: scripts/run_codex_audit.sh
```

The fenced block above is the **complete spec-side procedure** (~347 lines). The orchestrator prompt does NOT receive this verbatim — Phase 6.6 ships a **decision-policy summary** (~50 lines) that names the trigger, ship/block decision rule, hard rules, cross-references, and lists the P-PA-* / P-PB-* failure phase IDs as load-bearing references back to this spec section. The detailed Path A → Path B procedure (A1–A7, B1–B11, A1.5 supersession preflight, B1a tuple-match recovery, B8a/B8b/B8c late freshness barriers, F-067 / F-069 / F-070 / F-072 closures) is the **implementation contract** and remains in this spec. Orchestrator follows the procedure in §5.6 exactly; the prompt's role is to declare the gate, name the decision policy, and reference §5.6 as the procedure source. §9.1 R3 carries the prompt-bloat risk entry; the ~50-line summary addition is within budget for the existing ~580-line orchestrator prompt.

The split (procedure stays in spec; only decision-policy summary enters prompt) reflects the broader orchestrator design pattern: prompt is the LLM-facing decision contract, spec is the implementation contract. Crash-recovery transactional semantics (B1a / B8b / B8c invariants) are reviewer / lint concerns, not LLM-dispatch concerns. See `docs/design/2026-05-05-phase-6.6-scoping-note.md` §3 Path 2 for the resolution rationale; the scoping note discovered the §5.6 fenced block had grown from ~50 to ~347 lines across rounds (PR #50 → #53 cascade sweeps adding F-070 closure et al.) while §9.1 R3 + §10 Phase 6.6 budget claims inherited the original PR #50 footprint unchanged.

**Verification failure state inventory.** Path A and Path B above describe what orchestrator does on the happy path and where it falls through; this inventory enumerates what observable state exists after every distinct failure phase. Reviewers can read this table to answer "what has been read, what has been written, what remains in `<output-dir>`, and what message does the user see after step X fails?" without stitching together §5.2 + §5.6 + §4.9 prose. Each phase is a partial-execution boundary; the inventory is the state machine's failure-side contract.

| Failure phase | Trigger | Passport mutation | Proposal location | User-visible message | Path A/B fall-through |
|---|---|---|---|---|---|
| **P-PA-precond** | A1 finds no matching persisted entry | none | unchanged | (silent — go to Path B) | A2 → Path B |
| **P-PA-schema** | A3 entry fails `--mode persisted` schema validation | none | unchanged | logged: `[AUDIT GATE: stale persisted entry <run_id> failed schema; falling through to Path B]` | A3 → Path B |
| **P-PA-gate** | A4 eleven-gate failure (any L2-x or L3-x) | none | unchanged | logged: `[AUDIT GATE: persisted entry <run_id> failed gate L<N>: <reason>]` | A4 → Path B with reason carried |
| **P-PA-verdict-schema** | A5 verdict file fails `audit_verdict.schema.json` | none | unchanged | logged: `[AUDIT GATE: verdict file <path> schema-invalid]` | A5 → Path B |
| **P-PA-verdict-mirror** | A5 verdict file mirror disagrees with persisted entry mirror | none | unchanged | logged: `[AUDIT GATE: persisted entry <run_id> verdict drift from <path>]` (Pattern C3 evidence) | A5 → Path B |
| **P-PA-stale-late** | A6 late freshness recheck (L3-3 or L3-4) detects mutation | none | unchanged | logged: `[AUDIT GATE: persisted entry <run_id> went stale during verification — bundle mutated since A4]` | A6 → Path B |
| **P-PA-supersede-preempt** | A1.5 superseding-proposal preflight finds an unmerged proposal whose `verdict.round > selected_persisted.verdict.round` (F-070 closure: typical for `another_round` user choice; also for manual fresh wrapper run with bumped round, byte-identical `abort_stage` re-audit, higher-round `AUDIT_FAILED` proposal) | none yet — Path A is preempted before A3 | unchanged at this step (Path B will process the proposal next) | (silent — proceed to Path B with `supersession_required = true`) | continues at Path B with supersession flag |
| **P-PB-empty** | B1 finds no proposal (and Path A also fell through OR found none) | none | unchanged | BLOCK: `[AUDIT GATE BLOCKED: no audit artifact for <agent>/<deliverable>]` + wrapper command | terminal — user must re-audit |
| **P-PB-supersede-missing** | A1.5 set `supersession_required = true` but no eligible proposal survives B2's higher-round filter (every candidate was either lower-round or invalid at B2 selection time). A higher-round proposal that survives B2 but fails B6 / B7 / B8a is covered by P-PB-gate / P-PB-verdict-schema / P-PB-stale-late instead with the proposal-specific failure message | none | unchanged (the original lower-round proposals stay in `<output-dir>` for diagnostic) | BLOCK: `[AUDIT GATE: requested higher-round audit artifact is missing; expected verdict.round > <prior_round> for tuple ...; please re-audit at round <prior_round + 1>]` | terminal — user must re-audit at the requested round |
| **P-PB-ambig** | B2 multiple proposals tie on `started_at` AND share unverifiable sidecar | none | unchanged | BLOCK: `[AUDIT GATE: ambiguous proposal selection at <output-dir>; multiple unverifiable sidecars share started_at]` | terminal — user must inspect |
| **P-PB-proposal-schema** | B4 proposal fails `--mode proposal` schema validation (e.g., wrapper pre-filled `verified_at`) | none | proposal stays in `<output-dir>` (NOT moved to `consumed/`) for user inspection — Pattern C3 evidence | BLOCK: `[AUDIT GATE: proposal <run_id> rejected: <schema error>]` (Pattern C3 attack surface) | terminal — user must inspect |
| **P-PB-audit-failed** | B5 proposal carries `verdict.status: AUDIT_FAILED` | none | proposal stays in `<output-dir>` (NOT moved per §4.9 step 9) — user may inspect | BLOCK: `[AUDIT GATE: audit attempted but failed: <verdict.failure_reason>]` | terminal — user must dispatch fresh wrapper run |
| **P-PB-gate** | B6 eleven-gate failure (any L2-x or L3-x) | none | proposal stays in `<output-dir>` for re-audit | BLOCK: `[AUDIT GATE: proposal <run_id> failed gate L<N>: <reason>]` | terminal — user must re-audit |
| **P-PB-verdict-schema** | B7 verdict file fails schema | none | proposal stays in `<output-dir>` | BLOCK: `[AUDIT GATE: verdict file <path> schema-invalid]` | terminal — user must inspect |
| **P-PB-verdict-mirror** | B7 proposal mirror disagrees with verdict file | none | proposal stays in `<output-dir>` (Pattern C3 evidence) | BLOCK: `[AUDIT GATE: Pattern C3: proposal mirror drift from verdict.yaml]` | terminal — user must inspect |
| **P-PB-stale-late** | B8a late freshness recheck (L3-3 or L3-4) detects mutation | none | proposal stays in `<output-dir>` for re-audit | BLOCK: `[AUDIT GATE: bundle mutated post-gate, before persist; re-audit required]` | terminal — user must re-audit |
| **P-PB-dup-early** | B1a early idempotent recheck finds passport already has a candidate proposal's `run_id` AND the persisted entry's `(stage, agent, deliverable_sha)` matches the current gate tuple (typical recovery from a prior session's post-B9 / pre-consume crash). Behavior splits by `supersession_required` from A1.5 | none in this session (the duplicate was committed by the other session) | proposal moved to `consumed/` (best-effort); skip candidate selection. **`supersession_required = false`**: re-run Path A steps A3-A6 against the pre-existing persisted entry (F-067 closure: deliverable / bundle / verdict file may have mutated, no unconditional trust); on A3-A6 success: GO TO A7 ship/block; on A3-A6 failure: remove ONLY this consumed duplicate from the B1 candidate set and continue B1a processing with any remaining candidates (F-069 closure). **`supersession_required = true`**: do NOT re-run A3-A6 — the dup is a same-tuple lower-or-equal-round entry that the higher-round proposal is meant to preempt (it may be A1-selected or older — see B1a prose for multi-round-history case); remove it from the candidate set and continue B1a so B2 supersession-mode filter can select the higher-round proposal (F-072 closure: re-validating and shipping any prior round verdict here would silently override the user's `another_round` choice) | (silent on supersession-true case; silent on supersession-false A3-A6 success or A3-A6 failure with remaining candidates; on supersession-false A3-A6 failure with empty candidate set: B3 BLOCK with `[AUDIT GATE: prior persisted entry <run_id> failed re-validation: <reason>; please re-audit]`) | supersession-true: continues B1a/B2 with remaining (B2 supersession-mode filter selects higher-round proposal); supersession-false A3-A6 success: continues at A7; supersession-false A3-A6 failure with remaining candidates: continues B1a/B2; supersession-false A3-A6 failure with empty set: falls through to B3 |
| **P-PB-dup-other** | B1a finds passport already has a candidate proposal's `run_id` but the persisted entry is for a DIFFERENT gate tuple (only reachable under hand-edit since wrapper-generated `run_id` is random per `/dev/urandom`) | none in this session | proposal moved to `consumed/` (best-effort); proposal removed from candidate set; B1 processing continues with remaining candidates | (silent — continue to B2 with the remaining proposal candidates) | continues at B2 |
| **P-PB-dup-late** | B8b late idempotent recheck finds passport already has this `run_id` (concurrent merge that committed between B1a and B8b) | none in this session (the duplicate was committed by the other session) | proposal moved to `consumed/` (best-effort); skip persist; GO TO B10 reading the pre-existing persisted entry's verdict | (silent — proceed using the already-persisted entry's verdict) | continues at B10 |
| **P-PB-snapshot** | B8c snapshot integrity check (proposal or sidecar mtime changed since B1 scan) | none | proposal stays in `<output-dir>` | BLOCK: `[AUDIT GATE: proposal or sidecar mutated between scan and persist; re-scan required]` | restart at B1 |
| **P-PB-persisted-schema** | B8d `--mode persisted` re-validation fails (lint caught a contradiction the proposal-mode validation missed) | none — atomic-rename did not yet fire | proposal stays in `<output-dir>` | BLOCK: `[AUDIT GATE: persisted-mode re-validation failed: <reason>]` | terminal — user must inspect |
| **P-PB-passport-write** | B9 atomic rename of `<passport>.tmp` over live passport fails (filesystem error) | none — tmp-write/fsync/atomic rename is a transaction; partial failure leaves passport unchanged | proposal stays in `<output-dir>` | BLOCK: `[AUDIT GATE: passport write failed: <fs error>]` | terminal — user must check disk |
| **P-PB-consume-fail** | B9 passport rename succeeded but proposal-move to `consumed/` failed | persisted entry committed | proposal stays in `<output-dir>` (the unmoved file is the recovery signal — B1a on the next session moves it idempotently) | (silent — entry is committed, decision proceeds) | continues at B10 |
| **P-PB-crash** | Orchestrator crashes between any two B-steps after the B1 scan | depends on phase: passport committed iff B9 atomic rename succeeded; otherwise none | depends on phase: in `<output-dir>` if pre-B9 or post-B9-pre-move; in `consumed/` if post-move | none in the crashed session — recovery happens on the next session via Path A (finds the persisted entry if B9 succeeded) or Path B + B1a (idempotently moves leftover proposals if B9 succeeded but move did not, or re-merges from scratch if neither succeeded) | next session resumes at A1 |

**Why this inventory is load-bearing.** The Round 12 §4.4 control-flow audit surfaced two §4.4 P1s (F-059 SIGTERM, F-060 TOCTOU) that prior eleven rounds missed because no review walked the wrapper looking for crash / race / partial-state windows. §5.6 has the same complexity at orchestrator scope (multi-step process, side effects across passport + filesystem, can be interrupted by LLM session crash, can race with a second orchestrator session under multi-agent setups). The inventory makes the implicit transaction model explicit so a future review can audit each phase against actual procedure rather than re-deriving "what state should orchestrator be in after step X failed?" each time. New failure phases added in v3.6.8+ get new rows.

### 5.7 What this section does NOT change

To make the additive nature explicit:

- No change to FULL / SLIM / MANDATORY checkpoint type rules.
- No change to existing checkpoint command vocabulary (`continue` / `pause` / `adjust` / `redo` / `skip` / `abort`). Step 6 introduces audit-gate-specific user inputs that live in their own response namespace and do not enter the checkpoint command vocabulary: `iterate` (MINOR verdict response, §5.3 MINOR row), and `ship_with_known_residue` / `another_round` / `abort_stage` (round-3 MATERIAL escalation choices, §5.4). These four labels are responses to Step-6 prompts only; the checkpoint command vocabulary stays unchanged. Lint enforces that audit-gate prompts use these four labels exactly and do not redefine the existing six.
- No change to Skill Failure Fallback Matrix beyond adding one row for "audit gate MATERIAL after 3 rounds → ESCALATION block".
- No change to Resume Mode (`resume_from_passport`). Audit_artifact[] re-verification on resume is part of the existing ledger replay, not a new code path.
- No change to Mid-Entry Material Passport Check rules.
- No change to `Style Profile` carry-through, `Material Passport` versioning, or `verification_status` field semantics.

The Step 6 hook is structurally a new transition-time check that runs before existing transition logic. It has its own block conditions but does not alter existing block conditions.

---

## 6. Partial inversion rule (downstream agent prompt edits)

Q3's "Layer 2 + Layer 3 + partial inversion" decision (§2.1) has two halves. Layer 2 + Layer 3 are the orchestrator-side gating checks specified in §3 and §5. **Partial inversion is the prompt-side edit that complements them**: each downstream agent prompt keeps the explicit prohibition on simulated audit but stops describing the downstream audit pipeline that follows. The asymmetry is the load-bearing part — the agent must still know "do not fake an audit," but must NOT know "an audit is dispatched after my output is read." Without the second clause, sub-agent fake-audit hallucination (Pattern C3, per `feedback_subagent_tool_hallucination.md`) has no trigger surface.

This section specifies the rule, lists the four sentences to be edited across the three v3.6.7 downstream agent prompts, and defines the inversion sweep checklist that lint enforces in CI.

### 6.1 Rule statement

The partial inversion rule has two clauses, which MUST both apply uniformly across the three v3.6.7 downstream agent prompts:

**Clause 1 — Retain the prohibition.** Every PATTERN PROTECTION (v3.6.7) block MUST carry the verbatim line:

> DO NOT simulate any audit step. DO NOT claim to have run codex/external review. Output metadata must not claim audit-passed state.

This line names the failure mode (Pattern C3 fake-audit hallucination) without revealing that an actual audit pipeline exists downstream. The agent learns "do not invent audit results" as a category of forbidden behavior, not as a hint that its output will be audited.

The exact wording matters. The paired `codex/external review` phrasing names the forbidden category (so the agent knows which fabrications are off-limits) without naming the orchestrator or saying "my output will be audited later" — the agent learns *what not to claim* rather than *what runs downstream*. Earlier drafts that wrote "the orchestrator runs codex audit afterward" leaked the latter and trip-wired Pattern C3; the §6.3 sweep retires every variant of that leak.

**Clause 2 — Remove the pipeline disclosure.** Every PATTERN PROTECTION (v3.6.7) block MUST NOT carry any sentence that:

a. Names the orchestrator's audit dispatch, OR
b. References `codex_audit_multifile_template.md` audit dimensions as a downstream consumer ("Cross-model audit follows §3.1..."), OR
c. Names a future audit that will read this agent's output, OR
d. Hints that the agent's output is the input to a verification step (e.g., "downstream audit covers...").

Compliance with Clause 1 is necessary; Clause 2 is what makes inversion *partial* rather than total. A total inversion (removing Clause 1) would lose the prohibition and let unfettered audit hallucination through; a no-inversion baseline (keeping Clause 2 sentences) trips Pattern C3. The two clauses together define the only point in the design space that defends the boundary without trip-wiring it.

**Why this is a v3.6.7-specific rule, not a global one.** Per Q1=A, scope is restricted to the three v3.6.7 downstream agents. Other ARS agents (e.g., `bibliography_agent`, `socratic_mentor_agent`, `field_analyst_agent`) may legitimately reference codex / cross-model verification in their prompts because they are not the dispatch-point for the audit gate; their prompts are not Pattern C3 attack surfaces because they do not produce the deliverable that the orchestrator audits. The §6.3 sweep is correspondingly narrow — it lints exactly three files. Widening the sweep is the L2 deferred question (§9 L2); the answer for v3.6.7 is "do not widen" because every additional file in scope is one more file the lint must keep clean against ordinary editorial drift.

### 6.2 Sweep scope (the four sentences)

The Step 1+2 ship (PR #48, main `b4fbffd`) added PATTERN PROTECTION (v3.6.7) blocks to three downstream agent prompts. As of `main` HEAD `b76e626`, those blocks contain four sentences that violate Clause 2 of §6.1 plus one sentence that already aligns with Clause 1 in only one of the three prompts. Step 6 closes the gap.

| # | File | Line (at HEAD `b76e626`) | Existing sentence | §6 action |
|---|---|---|---|---|
| 1 | `deep-research/agents/synthesis_agent.md` | 164 | "Cross-model audit follows `shared/templates/codex_audit_multifile_template.md` audit dimensions §3.1, §3.2, §3.3, §3.4 and the bundle-specific Section 4(f) check." | **Remove sentence.** It violates Clause 2(b) and Clause 2(d) — it names the audit template the orchestrator dispatches against and frames the agent's output as that template's input. |
| 2 | `deep-research/agents/research_architect_agent.md` | 190 | "Cross-model audit covers these via dimension §3.5 (instrument quality) of `shared/templates/codex_audit_multifile_template.md`." | **Remove sentence.** Same Clause 2(b) and Clause 2(d) violation. |
| 3 | `deep-research/agents/report_compiler_agent.md` | 172 | "Cross-model audit covers these via dimension §3.7 (COI adequacy) plus the bundle-specific Section 4(f) check of `shared/templates/codex_audit_multifile_template.md`." | **Remove sentence.** Same Clause 2(b) and Clause 2(d) violation. |
| 4 | `deep-research/agents/report_compiler_agent.md` | 177 | "DO NOT simulate any audit step. DO NOT claim to have run codex/external review. **The orchestrator runs codex audit afterward.**" | **Trim trailing clause.** Replace with the canonical Clause 1 line (no trailing "The orchestrator runs codex audit afterward" sentence). The "orchestrator runs codex audit afterward" tail is the most direct Clause 2(a) violation in the inventory. |
| 5 | `deep-research/agents/report_compiler_agent.md` | 178 | "Output metadata must not claim audit-passed state." | **Keep.** This sentence is the persistence-side complement of the Clause 1 line and stays. The §6.3 sweep folds it into the canonical Clause 1 line so the same wording appears in all three prompts (the other two prompts add it in §6.2's add step below). |

Two prompts (`synthesis_agent.md`, `research_architect_agent.md`) currently have neither the prohibition nor the pipeline-disclosure tail; they have only the pipeline-disclosure sentence (#1, #2 above) without any "DO NOT simulate audit" line. Step 6 must therefore both **remove** the pipeline-disclosure sentence AND **add** the canonical Clause 1 line to those two prompts. The third prompt (`report_compiler_agent.md`) has both — Step 6 removes the disclosure (line 172) and trims the trailing clause (line 177) but keeps the leading prohibition by way of replacing it with the canonical Clause 1 line.

**Canonical Clause 1 line (final form to ship in all three prompts):**

> DO NOT simulate any audit step. DO NOT claim to have run codex/external review. Output metadata must not claim audit-passed state.

The line is one bullet in the PATTERN PROTECTION block, placed last in each block (after the pattern-specific bullets) so the prohibition is the closing instruction the agent reads.

**Net change to each prompt:**

- `synthesis_agent.md`: −1 sentence (line 164 disclosure) + 1 bullet (canonical Clause 1).
- `research_architect_agent.md`: −1 sentence (line 190 disclosure) + 1 bullet (canonical Clause 1).
- `report_compiler_agent.md`: −1 sentence (line 172 disclosure), line 177 trimmed and merged with line 178 into the canonical Clause 1 bullet (net −1 sentence, +0 bullets).

Total spec-side delta: 3 sentences removed, 2 bullets added, 1 bullet rewritten. The PATTERN PROTECTION block size grows by 0–1 lines per prompt; the "prompt bloat" risk (§9 R3) is bounded by this delta.

### 6.3 Inversion sweep checklist (lint enforcement)

The sweep is mechanically enforced by extending the existing `scripts/check_v3_6_7_pattern_protection.py` lint script (added in Step 1+2 PR #48). Step 6 adds three checks; failure of any check blocks CI on `.github/workflows/spec-consistency.yml`.

The lint script reads each of the three downstream agent prompts and verifies:

| Check ID | Rule | Implementation | Failure message |
|---|---|---|---|
| INV-1 | The PATTERN PROTECTION (v3.6.7) block contains exactly one bullet whose text matches the canonical Clause 1 line verbatim | Regex match against the literal sentence (whitespace-normalized) | `[INV-1] <file>: PATTERN PROTECTION block missing or duplicating the canonical Clause 1 line. Expected exactly one bullet matching: "DO NOT simulate any audit step. DO NOT claim to have run codex/external review. Output metadata must not claim audit-passed state."` |
| INV-2 | The PATTERN PROTECTION (v3.6.7) block contains zero sentences matching any Clause 2 violation pattern | Python `re` patterns compiled with `re.IGNORECASE`, applied to the block text: (a) `r"\bthe orchestrator\b.*\baudit\b"`, (b) `r"\bcross-model audit (?:follows\|covers)\b.*codex_audit_multifile_template"`, (c) `r"\baudit (?:afterwards?\|will be run\|is dispatched)\b"`, (d) `r"\bdownstream audit\b\|\bthis output (?:is\|will be) audited\b"`. Backslash-pipe (`\|`) inside Markdown table cells reads as a literal pipe alternation in the underlying regex — the lint script unescapes Markdown table-cell escaping before compiling the patterns | `[INV-2] <file>:<line>: Clause 2 violation: <matched sentence>. Sentence must be removed per docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md §6.2.` |
| INV-3 | No file outside the three v3.6.7 downstream agent prompts gains a Clause 1 line as a side effect of the sweep (defends against well-intentioned over-application that would mark the L2 deferred question (§9 L2) as decided) | Manifest-driven file list in `scripts/v3_6_7_inversion_manifest.json` (contains exactly three filenames); lint scans only Markdown prompt files under `deep-research/agents/` and `academic-pipeline/agents/` (excluding `docs/**`, `scripts/**`, `tests/**`, and any other directory — the canonical Clause 1 line legitimately appears in this spec at §6.1, §6.2 and in test fixtures, and scanning those would self-fail) and reports any hit outside the manifest | `[INV-3] <file>: canonical Clause 1 line found outside the v3.6.7 inversion manifest. If this is intentional widening, update scripts/v3_6_7_inversion_manifest.json AND open the L2 question per §9.` |

INV-1 + INV-2 are positive-and-negative checks that make the desired state machine-readable: every in-scope prompt must say the prohibition exactly once and must not say anything that names the downstream audit. INV-3 is the scope guard against accidental sweep widening — adding a fourth file to the manifest is a deliberate design choice that opens §9 L2, not a change a casual editor can make by copy-pasting the Clause 1 line into a new prompt.

**Manifest format** (`scripts/v3_6_7_inversion_manifest.json`):

```json
{
  "scope": "v3.6.7-only",
  "rationale_doc": "docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md#6-partial-inversion-rule-downstream-agent-prompt-edits",
  "files": [
    "deep-research/agents/synthesis_agent.md",
    "deep-research/agents/research_architect_agent.md",
    "deep-research/agents/report_compiler_agent.md"
  ]
}
```

Adding a fourth entry triggers an L2-resolution requirement: the PR description MUST cite the §9 L2 resolution rationale and update both this spec and the manifest in the same commit. CI does not enforce this PR-description rule; it is a code-review obligation backed by the §9 L2 forward reference. Future v3.6.8+ work that legitimately widens scope (e.g., when `bibliography_agent` patterns get their own protection layer) will land its own version-tagged manifest rather than retroactively widening v3.6.7's.

**Inversion sweep is not the same as audit-mention scrubbing.** Lint is narrow: it operates only on the PATTERN PROTECTION (v3.6.7) block. References to codex / audit / cross-model verification in OTHER sections of the same prompt (e.g., the agent's own `Output Format` section, generic audit-mode invocation instructions outside Step 6 scope) are out of scope. INV-2's regex set is anchored to PATTERN PROTECTION block boundaries via the lint script's section parser (already present from Step 1+2). This is what keeps INV-2 from false-positiving on legitimate audit-mode prompts that the agent files may carry for other purposes.

---

## 7. Step 8 evaluation case design

Step 8 of the v3.6.7 main spec §9 implementation table is "Add evaluation case (synthetic) demonstrating all 18 patterns triggered + protected." Per Q4=C this spec resolves Step 8 with a **hybrid fixture set**: per-pattern micro-fixtures that exercise each pattern in isolation, plus one chapter-level integration fixture that exercises the whole pipeline end-to-end. Per Q4 the hybrid is the only choice that simultaneously serves unit-level regression detection (granular failure attribution) and integration-level confidence (the runtime really does block when audit catches a finding).

The hybrid choice mirrors the existing 29-mutation lint suite shipped in Step 1+2: that suite ships unit-style mutations against the lint script alone; Step 8 fixtures ship paired BAD/GOOD pipeline traces against the full audit-gate runtime. Together they cover lint behavior + runtime behavior at proportionate granularity.

### 7.1 Pattern inventory and fixture count

The v3.6.7 main spec ([`2026-04-29-ars-v3.6.7-downstream-agent-pattern-protection-spec.md`](2026-04-29-ars-v3.6.7-downstream-agent-pattern-protection-spec.md)) §3 + §4 inventories **17 numbered pattern IDs** (5 narrative-side A1–A5, 5 instrument-side B1–B5, 3 publication-side C1–C3, 4 cross-cutting orchestration lessons D1–D4). The same spec's prose (§1, §2.1, §9 Step 8, §10) refers to "18 distinct patterns." This is a documented off-by-one in upstream prose: every numbered ID in the inventory is accounted for, and the "18" prose figure does not correspond to a missing 18th ID.

Step 8 fixtures track the **inventory**, not the prose:

- **17 micro-fixtures**, one per numbered ID (A1–A5, B1–B5, C1–C3, D1–D4).
- **1 chapter-level integration fixture** that triggers a curated subset of those 17 in one pipeline run.

Total: 18 fixture artifacts. The numerical match between "18 fixtures" and the upstream prose figure of "18 patterns" is coincidence (1 integration case happens to round the count to 18); it is NOT evidence that a hidden 18th pattern exists. The §10 implementation phase 6.8 also opens a follow-up docs ticket to retire the upstream "18 patterns" prose so future maintainers do not chase the phantom 18th. Step 8 itself does not edit the upstream main spec — that retirement is a docs-only follow-up tracked in §9.2 L-doc-1 (logged there so the discrepancy is not silently absorbed).

This also corrects four locations in this spec: line 6 Scope, line 17 Step 8 bullet, line 29 §1.2, and line 64 §2.1 Q4 row — all drafted before §7's inventory walk surfaced the off-by-one. All four shipped lines should be read as "17" rather than "18"; the shipped wording stays intact for now to preserve PR #50's squash-merge boundary, but L-doc-1 below carries all four locations alongside the upstream main spec lines as one docs-only follow-up.

### 7.2 Micro-fixture schema

Each micro-fixture is a self-contained directory under `tests/fixtures/v3_6_7_pattern_eval/<pattern_id>/` carrying a paired BAD-versus-GOOD deliverable plus the synthetic upstream context required to exercise the pattern. The directory schema is fixed across all 17 micro-fixtures.

**Micro-fixture directory contract** (named "fixture directory contract" rather than "Schema 13.1" to avoid namespace collision with v3.6.6's `evaluator_full` Schema 13.1 — Step 6 fixtures are §3 / §3.7-anchored and have no relation to v3.6.6's Schema 13 / 13.1):

```
tests/fixtures/v3_6_7_pattern_eval/<pattern_id>/
├── manifest.json                    # Schema-validated (see below)
├── upstream_context/                # Synthetic Material Passport snippet + prior-stage outputs
│   ├── passport_snippet.yaml        # Minimum passport state to make the agent dispatchable
│   └── prior_artifacts/             # Files referenced from passport (citations, prior chapter, etc.)
├── bad_run/                         # The BAD case — agent emits a deliverable triggering the pattern
│   ├── deliverable.<ext>            # Synthetic deliverable that exhibits the pattern
│   ├── expected_audit_findings.yaml # Findings codex SHOULD emit when auditing the BAD deliverable
│   └── expected_orchestrator_action.yaml  # PASS / MINOR / MATERIAL + which §5.6 phase fires
└── good_run/                        # The GOOD case — agent emits a clean deliverable
    ├── deliverable.<ext>            # Pattern-protected deliverable
    ├── expected_audit_findings.yaml # Empty (PASS) findings list
    └── expected_orchestrator_action.yaml  # PASS + Path A or B as appropriate
```

**`manifest.json` schema (one per fixture, validated by `scripts/check_pattern_eval_manifest.py` added in §10 Phase 6.8):**

```json
{
  "$id": "pattern_eval_manifest.schema.json",
  "type": "object",
  "required": ["pattern_id", "agent", "pattern_scope", "stage", "fixture_kind", "upstream_context", "bad_run", "good_run"],
  "properties": {
    "pattern_id": {
      "type": "string",
      "enum": ["A1", "A2", "A3", "A4", "A5",
               "B1", "B2", "B3", "B4", "B5",
               "C1", "C2", "C3",
               "D1", "D2", "D3", "D4"]
    },
    "agent": {
      "type": "string",
      "comment": "Must match audit_artifact_entry.schema.json §3.2 enum exactly so the harness can feed this value into the wrapper as --agent without §4.2 input validation rejection. cross_cutting D-rows still name a real gate agent here; the cross-cutting nature is recorded in pattern_scope below.",
      "enum": ["synthesis_agent", "research_architect_agent", "report_compiler_agent"]
    },
    "pattern_scope": {
      "type": "string",
      "enum": ["agent_specific", "cross_cutting"],
      "comment": "agent_specific for A1-C3 patterns. cross_cutting for D1-D4 lessons that are orchestration-level rather than per-agent; the agent field still names the gate agent under which the fixture exercises the cross-cutting concern."
    },
    "stage": {
      "type": "integer",
      "minimum": 1,
      "maximum": 6
    },
    "fixture_kind": {
      "const": "micro"
    },
    "bad_run": {
      "type": "object",
      "required": ["deliverable_path", "expected_audit_findings_path",
                   "expected_orchestrator_action_path"],
      "properties": {
        "deliverable_path": { "type": "string" },
        "expected_audit_findings_path": { "type": "string" },
        "expected_orchestrator_action_path": { "type": "string" }
      }
    },
    "good_run": {
      "type": "object",
      "required": ["deliverable_path", "expected_audit_findings_path",
                   "expected_orchestrator_action_path"],
      "properties": {
        "deliverable_path": { "type": "string" },
        "expected_audit_findings_path": { "type": "string" },
        "expected_orchestrator_action_path": { "type": "string" }
      }
    },
    "upstream_context": {
      "type": "object",
      "required": ["passport_snippet_path", "prior_artifacts_dir"],
      "properties": {
        "passport_snippet_path": { "type": "string" },
        "prior_artifacts_dir": { "type": "string" }
      }
    }
  }
}
```

**`expected_audit_findings.yaml` shape** (mirrors `audit_verdict.schema.json` from §3.5 exactly so the same validator can verify both the fixture's expectation and the runtime verdict file; field order, names, and dimension enum match §3.5 verbatim):

```yaml
run_id: 2026-04-30T15-00-00Z-0a01
verdict_status: MATERIAL
round: 1
target_rounds: 3
finding_counts:
  p1: 1
  p2: 0
  p3: 0
findings:
  - id: F-001
    severity: P1
    dimension: "3.1"
    file: bad_run/deliverable.md
    line: 42
    description: "Cross-section drift on legal-effect characterization of Source X"
    suggested_fix: "Pre-list source effect inventory; add explicit cross-section consistency check before output"
generated_at: "2026-04-30T15:00:58.471Z"
generated_by: scripts/run_codex_audit.sh
generator_version: 1.0.0
```

For GOOD runs `findings: []` and `verdict_status: PASS`.

**`expected_orchestrator_action.yaml` shape:**

```yaml
expected_path: B          # Path A or B per §5.6
expected_phase: B10       # Which §5.6 step the gate exits at, or which P-* phase from §5.6 inventory
expected_block_message: "<exact substring expected in the user-visible BLOCK message>"
expected_passport_mutation: "appended"  # appended | none
expected_run_id_format: "matches §3.7 family F F1 regex"
```

This shape lets the test harness (§10 Phase 6.8) compare exact orchestrator behavior against fixture expectations without requiring the harness to run a real codex CLI — the harness reads `expected_audit_findings.yaml` as the synthesized verdict the codex run *would have produced* and feeds it into the orchestrator's gate procedure.

**Fixture-to-pattern mapping** (one row per micro-fixture):

| pattern_id | agent | pattern_scope | stage | What BAD triggers | What GOOD avoids |
|---|---|---|---|---|---|
| A1 | synthesis_agent | agent_specific | 2 | Same source's legal effect drifts across two narrative sections | Pre-listed effect inventory + cross-section consistency check |
| A2 | synthesis_agent | agent_specific | 2 | Pending-verification entry treated as fact | Hedge wrap: "pending verification of X" |
| A3 | synthesis_agent | agent_specific | 2 | Citation mis-anchored to a paper that does not contain the claim | One-line anchor justification per substantive claim |
| A4 | synthesis_agent | agent_specific | 2 | Quoted phrase scope creep (verbatim quote extends beyond the verified phrase boundary) | Verbatim quote bounded; surrounding context paraphrased |
| A5 | synthesis_agent | agent_specific | 2 | Sibling-document fabrication (declarative claim about a chapter not in ground truth) | Conditional language ("if document X argues Y, ...") |
| B1 | research_architect_agent | agent_specific | 2 | Confidentiality / anonymity / pseudonymization terms used interchangeably in consent script | Each term passed through `irb_terminology_glossary.md` |
| B2 | research_architect_agent | agent_specific | 2 | Pseudo-reverse-coded item (different construct flagged as "reverse-coded") | One-line construct-equivalence justification |
| B3 | research_architect_agent | agent_specific | 2 | Calendar-anchored retrospective item without common event date | Event-anchored phrasing default |
| B4 | research_architect_agent | agent_specific | 2 | Leading-frame item phrasing imports chapter argument vocabulary | Neutral / balanced item phrasing |
| B5 | research_architect_agent | agent_specific | 2 | List-of-options item subsets / over-sets the primary-source list | Primary-source list declared and enumerated fully |
| C1 | report_compiler_agent | agent_specific | 5 | Compression overclaim (abstract drops protected hedge identified upstream) | Protected hedging phrases preserved per `protected_hedging_phrases.md` |
| C2 | report_compiler_agent | agent_specific | 5 | Reflexivity disclosure with deictic temporal phrase ("during this period") | Explicit year range / past-tense disambiguating verb / "former" prefix |
| C3 | report_compiler_agent | agent_specific | 5 | Output metadata claims audit-passed state (sub-agent fake-audit hallucination) | Canonical Clause 1 line obeyed (no audit-passed metadata) |
| D1 | synthesis_agent | cross_cutting | 2 | Multi-file deliverable audited file-by-file (sequential) misses cross-file inconsistency | Multi-file parallel audit per audit template §4.1 |
| D2 | synthesis_agent | cross_cutting | 2 | Single-round audit declares CLEAN (convergence theatre) | 3+ round iteration; CLEAN only after round-N zero-finding |
| D3 | synthesis_agent | cross_cutting | 2 | PARTIAL closure marked as CLOSED | PARTIAL stays PARTIAL until verdict file shows zero-finding |
| D4 | report_compiler_agent | cross_cutting | 5 | Word count uses regex hyphenated-as-1, busts publisher hard cap | Whitespace-split + 3–5% buffer per `word_count_conventions.md` |

D-row fixtures use `pattern_scope: cross_cutting` to record that the pattern is an orchestration lesson rather than a per-agent rule, while `agent` still names a real v3.6.7 gate agent so the wrapper's `--agent` input validation (§4.2) accepts the fixture as-is. D1–D3 attach to `synthesis_agent` (where cross-file Phase 2 audit, multi-round convergence, and PARTIAL→CLOSED behaviour all surface in practice); D4 attaches to `report_compiler_agent` (where publisher word-count enforcement applies). The harness exercises the cross-cutting concern by simulating the relevant stage's deliverable shape against the named gate agent.

### 7.3 Chapter-level integration fixture

The integration fixture lives at `tests/fixtures/v3_6_7_pattern_eval/integration/chapter_level_run/` and exercises the audit-gate pipeline end-to-end on a synthetic chapter that triggers a curated subset of patterns. Its purpose is NOT to exhaustively cover all 17 (the micro-fixtures already do that) but to verify the **full audit-gate pipeline** — Path A / Path B fall-through, multi-round escalation, ship_with_known_residue, ARS_PASSPORT_RESET interaction — using a realistic deliverable set.

**Curated trigger subset** (chosen to exercise three structural axes with one fixture):

| Axis | Pattern triggered | Why this pattern |
|---|---|---|
| 3-round MATERIAL convergence (§5.4) | A3 (mis-anchored citation, P1) | Forces round 1 → 2 → 3 escalation; round 3 still MATERIAL after partial fix triggers `ship_with_known_residue` user prompt |
| Path A vs Path B fall-through (§5.6) | C2 (reflexivity temporal ambiguity, P2) | After round 1 audit finds C2 then user re-runs, fixture exercises both proposal merge (Path B) and persisted re-verification (Path A on resume) |
| Cross-cutting + per-agent stack | D4 (word count) + C1 (compression overclaim) | Stage 5 abstract bundle exercises both publisher hard-cap arithmetic and protected-hedge preservation in one pass |

**Fixture artifacts** (integration fixture shape — extends the §7.2 micro-fixture directory contract with multi-round + escalation subdirectories):

```
tests/fixtures/v3_6_7_pattern_eval/integration/chapter_level_run/
├── manifest.json                       # fixture_kind: "integration"
├── upstream_context/                   # Multi-stage synthetic chapter
│   ├── passport_snippet.yaml
│   ├── chapter_body_v1.md              # Stage 4 hand-off body
│   ├── chapter_body_v2.md              # Post-revision body
│   └── prior_artifacts/                # Citation list, prior-chapter outputs
├── round_1/                            # First audit round — round=1, target_rounds=3
│   ├── synthesis_agent/                # Per-agent sub-fixture
│   │   ├── deliverable.md
│   │   ├── expected_audit_findings.yaml
│   │   └── expected_orchestrator_action.yaml
│   ├── research_architect_agent/
│   ├── report_compiler_agent/
│   └── expected_pipeline_state.yaml    # What passport / output-dir / checkpoint state should look like after round 1
├── round_2/                            # Post-revision audit — round=2, target_rounds=3
├── round_3/                            # Round 3 still MATERIAL — escalation prompt
└── escalation/                         # User picks ship_with_known_residue in round 3
    ├── user_response.yaml              # Synthetic user-input response
    ├── expected_passport_state.yaml    # acknowledgement entry appended
    └── expected_pipeline_outcome.yaml  # Stage proceeds, final passport state
```

**Integration manifest** is a separate JSON Schema keyed by `fixture_kind: "integration"`. It does NOT extend the §7.2 micro-fixture schema — the two shapes share a `fixture_kind` discriminator and a `pattern_id` enum but otherwise have disjoint required fields. The `check_pattern_eval_manifest.py` lint script (§10 Phase 6.8) branches on `fixture_kind` and applies the matching schema; this is what keeps the integration manifest clean of micro-fixture-specific fields like `pattern_scope`, `agent`, `stage`, and the BAD/GOOD pair (which the integration fixture decomposes into per-agent / per-round sub-fixtures inside the directory tree above):

```json
{
  "$id": "pattern_eval_integration_manifest.schema.json",
  "type": "object",
  "required": ["fixture_kind", "patterns_triggered", "rounds", "escalation", "rationale_doc"],
  "properties": {
    "fixture_kind": { "const": "integration" },
    "patterns_triggered": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string",
        "comment": "Same closed enum as the §7.2 micro-fixture pattern_id field — the 17 numbered pattern IDs.",
        "enum": ["A1", "A2", "A3", "A4", "A5",
                 "B1", "B2", "B3", "B4", "B5",
                 "C1", "C2", "C3",
                 "D1", "D2", "D3", "D4"]
      }
    },
    "rounds": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["round", "target_rounds", "expected_verdict"],
        "properties": {
          "round": { "type": "integer", "minimum": 1 },
          "target_rounds": { "type": "integer", "minimum": 1 },
          "expected_verdict": { "type": "string", "enum": ["PASS", "MINOR", "MATERIAL", "AUDIT_FAILED"] }
        }
      }
    },
    "escalation": {
      "type": "object",
      "required": ["user_choice"],
      "properties": {
        "user_choice": { "type": "string", "enum": ["ship_with_known_residue", "another_round", "abort_stage"] },
        "expected_acknowledgement_finding_ids": { "type": "array", "items": { "type": "string" } }
      }
    },
    "rationale_doc": { "type": "string" }
  }
}
```

Concrete fixture manifest:

```json
{
  "fixture_kind": "integration",
  "patterns_triggered": ["A3", "C2", "D4", "C1"],
  "rounds": [
    { "round": 1, "target_rounds": 3, "expected_verdict": "MATERIAL" },
    { "round": 2, "target_rounds": 3, "expected_verdict": "MATERIAL" },
    { "round": 3, "target_rounds": 3, "expected_verdict": "MATERIAL" }
  ],
  "escalation": {
    "user_choice": "ship_with_known_residue",
    "expected_acknowledgement_finding_ids": ["F-101", "F-103"]
  },
  "rationale_doc": "docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md#73-chapter-level-integration-fixture"
}
```

The harness runs the integration fixture by:

1. Loading round 1 deliverables + their `expected_audit_findings.yaml` as synthesized verdicts.
2. Driving the orchestrator's §5.6 procedure with each round's verdict in turn.
3. Asserting each round's `expected_pipeline_state.yaml` matches the actual orchestrator state.
4. At round 3 escalation, feeding `escalation/user_response.yaml` as the user's synthetic answer.
5. Asserting `expected_passport_state.yaml` matches actual passport state after escalation.

This exercises representative Path A / Path B / Path B-supersession happy-path and escalation code paths in §5.6 within one fixture, without requiring real codex execution. Coverage of failure-side phases (schema rejection, snapshot races, duplicate-recovery branches enumerated in §5.6's verification failure state inventory) is out of scope for the integration fixture; those phases are unit-tested by the lint script's negative cases (Phase 6.3) and by the §10 Phase 6.8 harness's per-phase synthetic injections, not by the integration fixture's chapter-level run.

### 7.4 Success criteria

A pattern is considered "demonstrated triggered + protected" by the Step 8 fixture set when ALL of the following hold:

1. **BAD case triggers the pattern-specific failure signal.** Running the harness on `<pattern_id>/bad_run/` produces an orchestrator decision matching `expected_orchestrator_action.yaml`. For 15 of 17 micro-fixtures the failure signal is a `MATERIAL` verdict with a finding in the expected dimension; for **C2** the failure signal is a `MINOR` verdict (one P3 reflexivity-temporal-ambiguity finding — sub-MATERIAL severity by design since C2's deictic temporal phrase is a hedge issue, not a hallucination); for **D2** the failure signal is a non-finding convergence-policy assertion ("round 1 PASS but D2 convergence-theatre trigger logged in expected_orchestrator_action.yaml"), since D2 is about whether the round cap mechanism actually iterates rather than emitting a P1 finding. The §7.4 success criterion is generic across all three shapes — the harness asserts the BAD case produces the expected pattern-specific signal (MATERIAL with P1 finding / MINOR with P3 finding / PASS with convergence assertion), not strictly an audit finding.
2. **GOOD case passes audit.** Running the harness on `<pattern_id>/good_run/` produces a `PASS` orchestrator decision and an empty `findings: []` list.
3. **§5.6 phase identified.** The harness asserts the orchestrator exits at the §5.6 phase named in `expected_orchestrator_action.yaml.expected_phase` (e.g., `B10` for normal MATERIAL, `P-PB-gate` for eleven-gate failure, `B11` for round-3 MATERIAL escalation per §5.4).
4. **Audit artifact lifecycle observed.** §5.6 persists PASS / MINOR / MATERIAL proposals at B8d/B9 BEFORE applying ship/block at B10, so the lifecycle test splits by failure phase plus duplicate-recovery state, not by ship/block outcome. The harness asserts the following inventory-driven rule:

   - **Fresh non-duplicate proposals** that pass B6 / B7 / B8a / B8c / B8d and whose B9 passport write succeeds reach B10 with exactly one new persisted `audit_artifact[]` entry appended (with `verified_at` populated by `_next_verified_at_ms`) before ship/block is applied. This covers all B10-bound paths whether the verdict is PASS, MINOR, or MATERIAL — BAD-case MATERIAL fixtures append an entry then BLOCK at B10 ship/block.
   - **Duplicate-recovery paths** that reach the decision step by reading an already-persisted entry — B8b / P-PB-dup-late, plus the B1a tuple-match recovery branches that re-run A3-A6 on the prior entry — verify **no new append in the current session**; B10 reads the pre-existing persisted entry from the prior session that committed it.
   - **Every §5.6 verification failure state inventory row whose `Passport mutation` column reads `none`** verifies no new persisted entry is appended at that phase. This covers selection/precondition failures (P-PA-precond, P-PA-supersede-preempt — though the latter continues to Path B), schema/gate/verdict-mirror/late-freshness failures (B4 / P-PB-proposal-schema, B5 / P-PB-audit-failed, B6 / P-PB-gate, B7 / P-PB-verdict-schema, P-PB-verdict-mirror, B8a / P-PB-stale-late, B8c / P-PB-snapshot, B8d / P-PB-persisted-schema), passport-write failures (B9 / P-PB-passport-write), and Path B-only terminal failures (P-PB-empty, P-PB-supersede-missing, P-PB-ambig). Continuation rows (P-PB-dup-other, P-PB-supersede-preempt) only append later if a subsequent selected candidate successfully merges; the harness asserts on the eventual final state, not on the intermediate continuation.
   - **The cross-check is mechanical:** the harness reads each fixture's `expected_orchestrator_action.yaml.expected_phase`, looks up the corresponding row in §5.6's inventory, and asserts the passport delta matches the row's `Passport mutation` column. This way the harness's assertions and §5.6's inventory stay synchronised by construction; adding a new failure phase to §5.6 in v3.6.8+ automatically extends the harness's coverage without code change.
5. **Inversion sweep clean.** The lint script (§6.3) passes on the three downstream agent prompts at the time the fixture run executes — i.e., the fixture suite is downstream of the inversion sweep, not a substitute for it.

Failure of ANY criterion above on ANY of the 17 micro-fixtures or the 1 integration fixture blocks CI on `.github/workflows/spec-consistency.yml`. CI green requires 18-of-18 fixtures green.

### 7.5 Fixture lifecycle and versioning

Fixtures are append-only at the v3.6.7 minor version. New patterns documented after v3.6.7 ships (e.g., v3.6.8+ when `bibliography_agent` patterns get their own protection layer per §6.1's "v3.6.7-specific rule" framing) get fixtures under their own version directory: `tests/fixtures/v3_6_8_pattern_eval/...`. Existing fixtures are not edited unless the pattern's protection rule itself changes; in that case the change ships under a new spec date and the fixture's manifest carries a `superseded_by` field pointing to the new fixture.

This mirrors the spec-versioning discipline already in place for `docs/design/`. It also keeps the §7.4 success criterion stable: "18-of-18 green" refers to v3.6.7's set; v3.6.8+ adds new fixtures with their own count.

**Fixture-to-pattern coverage gaps are surfaced explicitly.** The `manifest.json` `pattern_id` enum is closed: a fixture for an unenumerated pattern fails schema validation. Adding a new pattern to the enum requires updating the upstream main spec §3 / §4 inventory in the same PR, which keeps inventory and fixture set synchronized. The §10 Phase 6.8 lint script enforces this by cross-checking the fixture directory against the inventory's enumerated patterns and erroring on any pattern_id missing a fixture or any fixture missing a pattern_id.

### 7.6 CI wiring

Step 8 fixtures are wired into `.github/workflows/spec-consistency.yml` as two separate test jobs to make unit-vs-integration failure attribution legible:

| Job | Fixtures | Runtime | Failure surface |
|---|---|---|---|
| `pattern-eval-unit` | 17 micro-fixtures | ~10s (no codex; harness uses synthesized verdicts) | A specific pattern's BAD or GOOD case fails an assertion — narrow blame |
| `pattern-eval-integration` | 1 chapter-level integration fixture | ~30s (multi-round simulation) | Cross-pattern interaction failure or escalation-path failure — broader blame |

Both jobs run on every PR touching any of the following paths (path-filter completeness is load-bearing — a path that produces or consumes Step-6 artifacts but is omitted from the filter would let breaking changes ship without these jobs running):

- `deep-research/agents/synthesis_agent.md`
- `deep-research/agents/research_architect_agent.md`
- `deep-research/agents/report_compiler_agent.md`
- `academic-pipeline/agents/pipeline_orchestrator_agent.md`
- `scripts/run_codex_audit.sh`
- `scripts/check_audit_artifact_consistency.py`
- `scripts/test_check_audit_artifact_consistency.py`
- `scripts/check_v3_6_7_pattern_protection.py`
- `scripts/test_check_v3_6_7_pattern_protection.py`
- `scripts/check_pattern_eval_manifest.py`
- `scripts/test_pattern_eval_runtime.py`
- `scripts/_next_verified_at_ms.py`
- `scripts/test__next_verified_at_ms.py`
- `scripts/parse_audit_verdict.py`
- `scripts/v3_6_7_inversion_manifest.json`
- `shared/templates/codex_audit_multifile_template.md`
- `shared/contracts/audit/**`
- `shared/contracts/passport/audit_artifact_entry.schema.json`
- `shared/handoff_schemas.md`
- `academic-pipeline/references/passport_as_reset_boundary.md`
- `docs/PERFORMANCE.md`
- `tests/fixtures/v3_6_7_pattern_eval/**`
- `.github/workflows/spec-consistency.yml`

This is the same path-filter discipline `.github/workflows/pytest.yml` already uses for v3.6.4 corpus adapters; the list is enumerated exhaustively rather than via globs because `.github/workflows/spec-consistency.yml` itself is in the filter (a typo in the workflow file should re-trigger CI, otherwise the typo could ship).

The 17+1 split mirrors v3.6.7 Step 1+2's 29-mutation lint suite split between unit-style mutation tests (lint behavior) and integration-style fixture tests (the lint actually catches the right thing). Unit-fast / integration-broader is the same separation; unit-and-integration are the same kind of completeness target.

**Phase 6.8 CI deployment note (2026-05-05).** The "two separate test jobs" framing above is the design-level naming convention. The actual Phase 6.8 ship places `pattern-eval-unit` and `pattern-eval-integration` as two consecutive named **steps** within the existing `spec-consistency` job, not as two separate top-level jobs. This deviates from the literal "two separate jobs" wording but preserves the spec's intent — failure attribution remains step-name-legible (`Run v3.6.7 Step 8 pattern-eval-unit tests` vs `... pattern-eval-integration tests`), and the attribution surface in CI logs is identical to a job-split. The existing `spec-consistency.yml` runs unconditionally on push / PR (no `paths:` filter) — consistent with the 22 sibling lint steps already in the workflow — so the §7.6 path-filter list above is treated as descriptive enumeration of artifacts whose changes SHOULD trigger this job, satisfied by the no-filter (everything triggers it) deployment. A future v3.6.8+ workflow refactor that splits `spec-consistency.yml` into per-feature workflows with `paths:` filters would then promote `pattern-eval-unit` and `pattern-eval-integration` to top-level jobs at that boundary; until then, named-step deployment is the v3.6.7 ship contract.

---

## 8. Relation to v3.6.6 generator-evaluator contract

v3.6.6's generator-evaluator contract (Schema 13.1 `evaluator_full` mode, currently in design on branch `spec/v3.6.6-generator-evaluator-contract` — once merged, the spec lands under `docs/design/` per repo convention) and Step 6's audit-artifact gate are **orthogonal axes** of pipeline quality. Both can coexist on the same deliverable; neither subsumes the other.

| Axis | v3.6.6 generator-evaluator | v3.6.7 Step 6 audit gate |
|---|---|---|
| **Where the discipline lives** | Inside the writer/evaluator agent pair, same Claude session | Outside the LLM session entirely (codex CLI run by deployment) |
| **What it verifies** | Writer's draft satisfies an evaluator-derived rubric for in-pipeline self-criticism | Deliverable survives independent cross-model review at xhigh effort |
| **When it fires** | Per writer iteration, in-line during the writer agent's pass | Once per stage transition, at the boundary between agent and downstream consumer |
| **Trust model** | Same-session — writer and evaluator share LLM weights and may share blind spots | Cross-model — codex (gpt-5.5) is a different model family from the writer's Claude session |
| **Block behavior** | Schema 13.1 contract; writer iterates until evaluator passes | Strict Block (§2.2 Approach 1); MATERIAL refuses transition unless §5.4 ack |
| **Artifact** | `evaluator_full` envelope inside writer output | Schema 9 `audit_artifact[]` entry pointing at four standalone artifact files |
| **Threat surface** | Genuine self-criticism failure (writer cannot see its own blind spot) | Pattern C3 fake-audit hallucination + cross-model drift detection |

The two layers run sequentially on the same deliverable: a v3.6.7 downstream agent first satisfies its v3.6.6 generator-evaluator contract (in-session), then deployment runs codex audit out-of-session (per Q2=D the orchestrator does not execute codex; it verifies the resulting `audit_artifact[]` proposal at the next stage transition per §5.6). A passing v3.6.6 contract does NOT bypass the audit gate; a failing v3.6.6 contract never reaches the audit gate because the writer iteration loop blocks first. Either layer alone is insufficient: v3.6.6 catches what same-session reasoning can catch, audit gate catches what only a different-model perspective can catch (per `feedback_codex_xhigh_for_drift_audit.md` empirical lesson "codex翻案 3 段 Claude 判 'lean' 中 2 段").

**Explicit non-goals for Step 6 (clarifying what audit gate does NOT do):**

- Step 6 does NOT replace v3.6.6's generator-evaluator contract. Schema 13.1 `evaluator_full` continues to fire per writer iteration regardless of audit-gate presence.
- Step 6 does NOT extend the audit gate to non-v3.6.7 agents. `bibliography_agent`, `socratic_mentor_agent`, `field_analyst_agent`, `compliance_agent`, `collaboration_depth_agent`, `integrity_verification_agent`, `editorial_synthesizer_agent`, `literature_strategist_agent`, `citation_compliance_agent`, and every other ARS agent operate under pre-v3.6.7 trust rules. Per Q1=A, scope expansion is a v3.6.8+ concern.
- Step 6 does NOT introduce a "skip evaluator" path. Even a deliverable that has passed audit must still satisfy v3.6.6's generator-evaluator contract upstream of the gate. Audit verifies the deliverable, not the path that produced it.
- Step 6 does NOT define "passing v3.6.6 contract" as a precondition for audit dispatch. The wrapper script (§4) accepts any deliverable file; if a deliverable bypasses v3.6.6 entirely (e.g., hand-written by the user, deliberately fed through audit without writer iteration), the audit still runs. This is intentional — the audit gate is a deliverable-quality boundary, not a process-compliance check.
- Step 6 audit verdict does NOT feed back into the v3.6.6 evaluator's rubric. The two artifacts are siblings in the passport, not parent/child. A future v3.6.8+ proposal that wires audit findings into `evaluator_full`'s rubric is not part of v3.6.7 scope; if it lands, it will be a deliberate spec change with its own design round.

The orthogonality is what justifies running both at once. Merging the two layers into a single contract was rejected at Q4 brainstorm as a category error: in-pipeline self-criticism and cross-model independent review are different epistemic primitives. A single combined "evaluator+audit" contract would force one of two failure modes: (a) the in-pipeline evaluator pretends to be a cross-model auditor (Pattern C3 fake-audit hallucination, the very failure mode this spec defends against), or (b) the cross-model audit is reduced to whatever the evaluator can simulate in-session (eliminating the cross-model trust premise). Keeping the layers orthogonal preserves both primitives without compromise.

---

## 9. Risks and open questions

The §1–§8 design has accumulated four risks and five open-question entries (L1–L4 deferred from §2.3 plus one docs-only follow-up surfaced in §7.1) that did not have enough surface area to settle within their introducing sections. They are collected here so a single review pass can read all of them together; each carries the load-bearing forward references from earlier sections so the trail is not lost.

### 9.1 Risks

**R1 — Wrapper script deployment friction.** Strict Block (§2.2 Approach 1) means a user without `scripts/run_codex_audit.sh` installed and a working codex CLI cannot ship a deliverable through any of the three v3.6.7 stage transitions. This is intentional — the audit-as-contract design (Q2=D) requires the audit to actually run somewhere — but it changes the failure mode from "audit is recommended" to "audit is required for ship." Forward reference: §2.3 L4. The risk surface is concrete:

- A first-time user of v3.6.7 without codex CLI hits a hard BLOCK at the first synthesis stage with no audit artifact; the §5.6 BLOCK message gives the wrapper command but does not install codex CLI.
- A user with codex CLI installed but no `OPENAI_API_KEY` (or equivalent xhigh-effort credential) hits the same BLOCK with a different upstream cause (wrapper exits AUDIT_FAILED).
- A team running ARS in CI without provisioning codex CLI on the build agent ships breaks at the first PR that touches a v3.6.7 agent's deliverable.

Mitigation:

1. The §5.6 BLOCK message MUST include the wrapper command verbatim so the user can copy-paste at minimum. The current §5.6 spec already requires this.
2. `docs/PERFORMANCE.md` (added v3.4) gains a Step 6 onboarding subsection covering codex CLI installation, credential setup, and the wrapper's required environment variables (added alongside the wrapper itself in §10 Phase 6.1 — the docs and the script ship together so the BLOCK message's documentation pointer never lands on a missing page).
3. The wrapper's `--help` output (per §4.2) names every required environment variable and exits with EX_USAGE if any are missing — failure is loud and tells the user what to fix. This is preferred to a soft warning that lets the gate silently degrade.

R1 does NOT motivate a "skip audit" command (§5.7 hard rule). The friction is the cost of the artifact-as-contract design; partial mitigation via better diagnostics is acceptable, but escape hatches would re-open Pattern C3 attack surface.

**R2 — Motivated forgery boundary.** The §1.2 threat model declares Layer 2 + Layer 3 sufficient against inadvertent Pattern C3 over-claim but explicitly NOT against motivated forgery. This is a load-bearing scope decision; misunderstanding it in implementation or future spec work would invite scope creep into cryptographic signing infrastructure that the v3.6.7 timeline does not budget for. Forward reference: §1.2 threat-model statement, §3.7 family E row E9 (deployment-side discipline rule).

The risk: a future maintainer reads the eleven gating checks (§5.2) and assumes they defend against any audit-artifact tampering, then adds new features (e.g., "auto-resume on audit pass") that depend on stronger trust than Layer 2 + Layer 3 actually provide. Such a feature would be safe under the inadvertent-Pattern-C3 threat model but unsafe under the motivated-forgery model that real-world deployment may face.

**Concrete gap in 0.125+ stream evidence (load-bearing for §3.3).** Codex 0.125+ `--json` carries no `model` field and no `reasoning_effort` field anywhere in the event stream — both are invocation-side properties of the CLI flags (`-m gpt-5.5`, `-c 'model_reasoning_effort="xhigh"'`) rather than stream-side properties codex echoes back. Layer 2 therefore cannot verify which model actually ran; Layer 3 only records the wrapper-declared invocation in `sidecar.prompt`. A motivated actor with shell access could invoke `codex exec -m gpt-5.6 -c 'model_reasoning_effort="low"' ...` and write a sidecar declaring `model: gpt-5.5` / `reasoning_effort: xhigh`; the eleven gates would not detect that mismatch — every JSONL field they cross-check (`thread_id`, `usage` integers, the `agent_message` event's text) is unaffected by which model produced them. This gap stays inside the rejected motivated-forgery scope: it is exactly the case §3.7 family E row E9 (wrapper not LLM-callable from same session) and the §4.7 invocation-site discipline rule are designed to bound, and exactly the case Layer 5 (cryptographic signing on the codex CLI side) would close. The §1.2 closing paragraph already declares "Layer 5 was considered and rejected as over-engineering for the inadvertent-Pattern-C3 threat surface"; this paragraph names the specific gap that decision tolerates.

Mitigation:

1. Every §3 / §4 / §5 section MUST read consistently with §1.2's threat-model statement. The §3.4 closing paragraph and the §5.2 composite forgery-cost paragraph carry the Layer 2 / Layer 3 pointer back to §1.2; §3.7 family E row E9 carries the deployment-side pointer. Together they cover the three places (schema, runtime check, ownership rule) where §1.2's boundary must hold.
2. Future v3.6.8+ specs that propose Layer 5 (cryptographic signing) MUST cite §1.2 as the prior threat-model statement they are amending. This is a code-review obligation, not a CI rule.
3. Deployment hygiene rules in `docs/PERFORMANCE.md` Step 6 onboarding MUST name §1.2's threat boundary so deployment teams know the audit gate is one defense layer among several, not the only defense.

R2 is the rejected scope for v3.6.7. Layer 5 (cryptographic non-repudiation) is the natural escalation target if v3.6.8+ deployment scenarios require defending against motivated forgery. v3.6.7 ships with the inadvertent-threat-model boundary explicit so future scope expansion is a deliberate, traceable change.

**R3 — Prompt bloat across downstream agents.** §6 adds approximately one bullet to each of the three v3.6.7 downstream agent prompts (`synthesis_agent.md`, `research_architect_agent.md`, `report_compiler_agent.md`). §5.6 adds approximately 50 lines to the orchestrator prompt (`pipeline_orchestrator_agent.md`) **as a decision-policy summary; the full Path A → Path B procedure (~347 lines) stays in §5.6 as the implementation contract and is NOT inserted into the prompt verbatim** — see §5.6 closing prose for the prompt-vs-spec split rationale and `docs/design/2026-05-05-phase-6.6-scoping-note.md` §3 Path 2 for how the split was settled after the PR #50 → #53 cascade-expansion was discovered. The cumulative additions are bounded but not free — every line in an agent prompt is context the LLM processes per dispatch, and v3.6.7's PATTERN PROTECTION blocks already grew the three downstream prompts by 6–12 lines each at Step 1+2 ship. Forward reference: v3.6.7 main spec §8.1 risk "prompt bloat across downstream agents."

The risk concretely:

- Each downstream agent prompt gains 0–1 lines from §6.2 sweep (§6.2 net delta table).
- Orchestrator prompt gains ~50 lines from §5.6 — the decision-policy summary (trigger, ship/block rule, hard rules, cross-references, P-PA-* / P-PB-* phase ID references). The ~347-line procedural detail (A1–A7, B1–B11, A1.5 supersession preflight, B1a recovery, etc.) stays in §5.6 itself, not in the prompt. §5.6 closing paragraph documents the prompt-vs-spec split.
- Compounded with v3.6.7 Step 1+2 PATTERN PROTECTION blocks, the three downstream prompts now carry roughly 8–14 lines of v3.6.7-specific instruction each.

Mitigation:

1. The §6.2 sweep is the smallest possible change — it removes one disclosure sentence and adds one prohibition bullet per file. Sweep widening (§9 L2) is explicitly deferred.
2. The §5.6 orchestrator subsection is one new subsection (§3.5 Audit Artifact Gate) inserted into a structurally existing section sequence; it does NOT modify any pre-existing orchestrator instructions. A rollback path exists (delete §3.5) if the line budget proves load-bearing.
3. Every prompt line added by §6 / §5.6 has lint coverage (`scripts/check_v3_6_7_pattern_protection.py` for §6, the audit-artifact-consistency script for §5.6 references). A future "trim prompt" pass can verify the trimming did not break any check.

R3 is monitored, not blocked. v3.6.7 main spec §8.1 already accepted this risk class at Step 1+2 ship; Step 6 inherits the same risk envelope.

**R4 — ARS_PASSPORT_RESET interaction with audit artifacts.** v3.6.3 introduced `ARS_PASSPORT_RESET=1` and `resume_from_passport=<hash>` (canonical contract: `academic-pipeline/references/passport_as_reset_boundary.md`). Step 6's audit-artifact gate must remain compatible with reset-then-resume sessions. Forward reference: §2.3 L3, §5.5 last row of co-occurrence table.

The risk: a user runs an audit in session A, the session resets at a FULL checkpoint, the user resumes in session B, and the audit artifact's trust on resume is ambiguous. The settled answer (§5.5 row) is that orchestrator MUST re-run the eleven gating verification checks on resume — passport entries are not trusted "because they were verified once." But the design surface has implications:

- **Bundle file mutation between sessions:** if a primary or supporting file in the audit bundle changes between session A's audit and session B's resume, L3-3 / L3-4 SHA recompute correctly fails and orchestrator falls through to Path B. This is the desired behavior — a mutated deliverable cannot ride a stale audit pass — but it means a session B user may discover the audit gate has reset to "no audit artifact" without ever seeing the rejection of the prior audit. The §5.6 BLOCK message tells the user what to do (re-audit) but does NOT explain what changed.
- **Higher-round wrapper run between sessions:** if the user picked `another_round` in session A and the wrapper completed under CI before session B resumes, the round-N+1 proposal in `<output-dir>` MUST preempt the prior round-N persisted entry. §5.5's row already requires §5.6 A1.5 superseding-proposal preflight on resume; this closes the F-070 generalization across resume.
- **AUDIT_FAILED proposals on resume:** an AUDIT_FAILED proposal in `<output-dir>` from a prior session (wrapper exited non-zero, did not produce a clean verdict) is consumed at §4.9 step 9 by NOT being moved to `consumed/`. On resume, A1.5 may find a higher-round AUDIT_FAILED proposal that preempts a prior MATERIAL persisted entry; per §5.6 D4 closure, this BLOCKs with the failure reason rather than silently falling back. Verified at §5.6 phase P-PA-supersede-preempt + P-PB-audit-failed.

Mitigation:

1. §5.5's last row already specifies the resume re-verification rule; no new rule is needed.
2. §5.6's A1.5 preflight handles the cross-session higher-round case; no new code path is needed.
3. The `passport_as_reset_boundary.md` reference doc gains a paragraph in §10 Phase 6.5 (Schema 9 amendment) cross-linking audit-artifact[] to the reset-boundary contract so future maintainers see both rules together.

R4 is a confirmed-and-handled compatibility surface. The risk is documentation drift — if a future v3.6.8+ change to either reset-boundary or audit-artifact contract breaks the cross-link, the resume path becomes ambiguous. Mitigation 3 is the discoverability defense.

### 9.2 Open questions

These are deferred from §2.3 L1–L4 plus one new docs follow-up surfaced in §7.

**L1 — Round upper bound: 3 vs 5.** Resolved in §5.4 as "default 3 rounds, escalation prompt allows the user to bump cap by 1 per `another_round` choice." Forward reference: §2.3 L1 → §5.4. Status: **closed in §5.4.**

The 3-round default is empirically grounded in `feedback_cross_model_review_cascade_inconsistency.md` and `feedback_codex_review_vs_resume_audit_scope.md` observation that round-3 is the typical convergence point. The 5-round alternative would have aligned with `feedback_codex_iterative_spec_review_to_zero.md`'s "iterate to one zero-finding round" guidance but at the cost of delaying user escalation in cases where rounds 4–5 do not improve verdicts. The §5.4 escalation prompt makes the cap user-overridable, which preserves both empirical default and explicit-extension flexibility.

**L2 — Partial inversion sweep completeness: v3.6.7-only vs all ARS agent prompts.** Resolved in §6.1 as "v3.6.7-only." Forward reference: §2.3 L2 → §6.1, §6.3 INV-3 manifest. Status: **closed in §6.1; widening is a v3.6.8+ design decision.**

The narrow sweep is justified by the per-agent attack-surface argument (§6.1's "Why this is a v3.6.7-specific rule"): only the three v3.6.7 downstream agents are dispatch-points for the audit gate; other agents (e.g., `bibliography_agent`) do not produce deliverables that the orchestrator audits, so their codex/cross-model references in prompts are not Pattern C3 attack surfaces. Widening the sweep would add lint-maintenance cost without commensurate threat-surface reduction. The §6.3 INV-3 manifest pattern is what makes future widening a deliberate change.

**L3 — ARS_PASSPORT_RESET re-verification model.** Resolved in §5.5 as "re-run eleven gating verification checks on resume; do not trust prior verification by passport-presence alone." Forward reference: §2.3 L3 → §5.5, R4 above. Status: **closed in §5.5.**

The re-verification rule means session B does not inherit session A's audit trust by default. This is intentionally conservative — bundle files may have mutated between sessions, the user may have run a higher-round wrapper between sessions, the session A may have been a different model version. Re-running L3-3 / L3-4 against current on-disk content + L3-2 / L3-7 against the persisted sidecar provides resume-time fresh verification at low cost (the artifact files do not change between sessions; only the recompute is required).

**L4 — Wrapper script deployment friction discoverability.** Forward reference: §2.3 L4. Status: **resolved by R1 above** (mitigation 1–3). The R1 mitigation list is the forward-reference target for L4; both are the same design surface viewed from different entry points (L4 = "how visible is the gate?", R1 = "what is the cost of the gate's visibility?"). Treating them as one resolved item rather than two pending items keeps the cross-reference graph compact.

**L-doc-1 — "18 patterns" prose retirement (new in §7.1).** Two specs carry the off-by-one summary:
- v3.6.7 main spec ([`2026-04-29-ars-v3.6.7-downstream-agent-pattern-protection-spec.md`](2026-04-29-ars-v3.6.7-downstream-agent-pattern-protection-spec.md)) §1, §2.1, §9 Step 8, and §10 (four locations) — each refers to "18 distinct patterns."
- This spec at four locations: line 6 Scope ("all 18 patterns trigger and protect"), line 17 Step 8 bullet ("synthetic evaluation case demonstrating all 18 patterns triggered and protected"), line 29 §1.2 ("two-tier (18 micro + 1 integration)"), and line 64 §2.1 Q4 row ("18 per-pattern micro-fixtures + 1 chapter-level integration fixture") — all drafted before §7.1's inventory walk surfaced the off-by-one.

Both specs' inventories enumerate 17 numbered IDs (5 A + 5 B + 3 C + 4 D). Step 6 / Step 8 fixtures track the 17-ID inventory per §7.1. Forward reference: §7.1 → here. Status: **open; retirement is a docs-only follow-up.**

The retirement requires updating eight prose locations (four in the upstream main spec, four in this spec) to "17 distinct patterns" / "17 micro + 1 integration" without changing any of the 17 numbered IDs. The change is mechanical and ships under a separate docs-only PR after Step 6 lands; it is not a v3.6.7 spec amendment because the inventory itself is correct, only the summary count was off. The §10 Phase 6.8 implementation note logs this as a follow-up ticket so it does not silently absorb. **Phase 6.8 files this ticket as `docs/design/TODO-l-doc-1-18-patterns-prose-retirement.md`** — that file enumerates the eight retirement locations with current wording → target wording mapping and the procedure for the docs-only PR; deleting the TODO file after the retirement PR merges signals closure.

If a future review surfaces evidence that the upstream "18" figure was correct and an 18th pattern was dropped from the inventory between drafts, the right response is to amend the main spec inventory (re-add the 18th pattern) rather than the fixture set (which already aligns with the inventory). The fixture set is downstream of the inventory; mismatching them in either direction creates the §7.5 coverage-gap surface that the `pattern_id` enum closure already defends.

---

## 10. Implementation plan

The work in §3–§7 lands in eight phases. Each phase is one logical commit on the implementation branch; phases run sequentially because later phases depend on earlier phase outputs (Phase 6.2 schemas are imported by Phase 6.3 lint script; Phase 6.6 orchestrator prompt cites §3.7 invariant IDs that Phase 6.3 lint enforces; etc.). The phases align with the artifact list in `project_ars_v3_6_7_pattern_protection_wip.md` memory's implementation roadmap.

Each phase has a defined deliverable, a defined verification gate, and an explicit dependency on prior phases. Phases that can be parallelized are marked. The whole implementation is targeted as a single follow-up PR to land Step 6 + Step 8 together, mirroring the v3.6.7 main spec §9 plan that pairs them under one ship.

### Phase 6.1 — Wrapper script `scripts/run_codex_audit.sh`

**Deliverables:** `scripts/run_codex_audit.sh` AND `scripts/parse_audit_verdict.py` (the JSONL→verdict parser the wrapper invokes per §4.4 Step 4 to extract the **last** `item.completed.item.text` `agent_message` event's text from the codex 0.125+ event stream — intermediate `agent_message` events between tool-call `item.started` / `item.completed` pairs are skipped — and convert it into the `<run_id>.verdict.yaml` file per §3.5). Both implement §4 contract end-to-end.

**Includes:**
- Bash 4+ shebang and dependency check (`set -euo pipefail`).
- §4.2 input parsing exactly matching the contract: `--stage`, `--agent`, `--deliverable`, `--supporting`, `--round`, `--target-rounds`, `--bundle-id`, `--output-dir`, `--previous-findings`, optional `--dry-run`. EX_USAGE on missing required flags or on the §4.2 validation rules (`--round <= --target-rounds`, `--previous-findings` required when `--round > 1`, etc.). No `--bundle` or `--audit-template` flags — those names appeared in earlier drafts and are not part of §4.2.
- §4.3 output construction: `<run_id>` generation per F1 regex, four contract files written to `<output-dir>/<run_id>.{jsonl,meta.json,verdict.yaml,audit_artifact_entry.json}` plus the three non-contract diagnostic files (`<run_id>.stdout`, `<run_id>.stderr`, `<run_id>.manifest.txt`).
- §4.4 atomicity: tmp-file-rename for sidecar / verdict / proposal entry; JSONL streamed by codex CLI directly; proposal entry file is the LAST file written (E8).
- §4.4 helper functions: `_atomic_write`, `_sha256`, `_extract_jsonl_thread_id`, `_codex_version` (semver extractor — strips the `codex-cli ` prefix from `codex --version` output so the sidecar's `codex_cli_version` field stays bare-semver per §3.4), `_compute_bundle_manifest_sha` per §3.6 contract, `_now_rfc3339_ms`, `_random_4hex` from `/dev/urandom`.
- §4.4 SIGTERM trap that aborts with EX_TEMPFAIL and cleans up partial artifact files (F-059 closure).
- §4.4 TOCTOU detection: snapshot SHA-256 of every primary / supporting / template file at prompt-render time; recompute after codex returns; if any bundle file's SHA changed, emit `AUDIT_FAILED` with `failure_reason: "bundle file(s) mutated during audit run: <space-separated path list>"` and let the wrapper exit code rise to 70 per §4.6 (F-060 closure). The TOCTOU path produces the AUDIT_FAILED artifact set per §4.6 — it does NOT exit with EX_USAGE, because mid-run mutation is an audit-failure signal (orchestrator must see the proposal to BLOCK at §5.6 Path B5), not an input-validation error.
- §4.6 failure-mode handling: emit AUDIT_FAILED proposal + sidecar + verdict file for all enumerated non-zero codex exit codes (70 / 75 / other) per §4.6 table; still write the proposal entry last so orchestrator's lifecycle invariant E8 holds.
- §4.5 multi-file Phase 2 audit support via `--supporting` plus shared `--bundle-id` for cross-file bundle grouping; manifest hash computed by `_compute_bundle_manifest_sha` per §3.6.
- §4.7 enforcement: explicit comment block at the top of the script naming this rule (wrapper not LLM-callable from same session producing deliverable); deployment-side discipline reminder.
- `docs/PERFORMANCE.md` Step 6 onboarding subsection (per R1 mitigation 2): codex CLI installation, credential setup (`OPENAI_API_KEY`-equivalent), required environment variables, the §1.2 threat-model boundary, and the wrapper's exit-code contract from §4.6.

**Verification gate:** wrapper passes a self-test invocation (`scripts/run_codex_audit.sh --dry-run --stage 2 --agent synthesis_agent --deliverable <test-file> --round 1`) that validates inputs and exits 0 **without writing any contract artifacts** — `--dry-run` is an input-validation probe, not a synthetic audit, and writing a proposal entry there would create a fake audit artifact at zero codex cost (the exact Pattern C3 attack surface §1.2's threat model defends against). A separate non-dry-run synthetic smoke test (codex CLI mocked or invoked against a tiny fixture deliverable) produces a well-formed proposal entry that validates against the Phase 6.2 schemas in `--mode proposal`; the AUDIT_FAILED path is exercised by injecting a SHA mutation between Step 0b snapshot and Step 3a recompute. Full integration verification against the §7 fixture set defers to Phase 6.8.

**Dependencies:** none (Phase 6.1 is the foundation).

### Phase 6.2 — Four schema JSON files

**Deliverables:**
- `shared/contracts/passport/audit_artifact_entry.schema.json` — per §3.2.
- `shared/contracts/audit/audit_jsonl.schema.json` — per §3.3 (new directory).
- `shared/contracts/audit/audit_sidecar.schema.json` — per §3.4 (new directory).
- `shared/contracts/audit/audit_verdict.schema.json` — per §3.5 (new directory).

**Includes:**
- JSON Schema draft 2020-12 for each file.
- `oneOf` lifecycle states (proposal vs persisted) on `audit_artifact_entry.schema.json` per §3.2 lifecycle-conditional table.
- `$ref` from Schema 9 amendment (Phase 6.5) to `audit_artifact_entry.schema.json`.
- `shared/contracts/README.md` gains one section documenting the new `audit/` directory's purpose, mirroring the v3.6.6 convention.

**Verification gate:** all four schemas parse as valid JSON Schema 2020-12; example payloads in §3.1 / §3.3 / §3.4 / §3.5 validate against their respective schemas (positive examples) and a deliberately-malformed counter-example fails (negative case).

**Dependencies:** none structurally; can run in parallel with Phase 6.1, but lint script (Phase 6.3) imports these schemas so Phase 6.3 must come after Phase 6.2.

### Phase 6.3 — Lint script `scripts/check_audit_artifact_consistency.py`

**Deliverable:** `scripts/check_audit_artifact_consistency.py` consuming §3.7 invariants table.

**Includes:**
- Per-row implementation of §3.7 families A (A1–A7; note A7 is a stream-shape rule against the on-disk JSONL, distinct from A1–A6 which are per-artifact field rules), B (B1–B10), C (C1–C4), D (D1–D4), E (E1–E9 where lint-applicable; E1/E2/E6/E9 are discipline rules with limited lint surface — implement detectable cases like "non-orchestrator writer modified passport" via post-hoc passport-diff analysis), F (F1–F4).
- Three CLI modes:
  - `--mode proposal` (validates a proposal-state entry).
  - `--mode persisted` (validates a persisted-state entry).
  - `--mode jsonl-stream` (validates a JSONL stream against the §3.7 family A row A7 stream-shape invariant). Invoked by orchestrator §5.2 L2-5 as `scripts/check_audit_artifact_consistency.py --mode jsonl-stream --jsonl <path>`. Exits 0 on stream-shape pass, non-zero on pairing violation with stderr message naming the offending `item.id` and reason.
- `--passport-path <path>`, `--output-dir <path>`, and `--jsonl <path>` for cross-file / stream rule checks.
- `--example-validation-harness` mode that walks `docs/design/*.md` finding §3 example payloads and validating them — closes F4 (spec text drift).
- Test suite at `scripts/test_check_audit_artifact_consistency.py` with one test per invariant row (positive + negative cases).

**Verification gate:** lint passes on the Phase 6.2 schemas, on this spec's bundled §3.1 / §3.3 / §3.4 / §3.5 example payloads (via `--example-validation-harness`), and on the Phase 6.3 positive/negative unit fixtures shipped alongside the lint script. Test suite achieves 100% coverage over §3.7 family rows. **Full wrapper-output and orchestrator-prompt validation against the 17 micro-fixtures is Phase 6.8's responsibility, not Phase 6.3's** — Phase 6.3's gate must not depend on artifacts produced by Phase 6.6 / Phase 6.8 (which themselves depend on Phase 6.3's lint), or the phase-gate ordering becomes circular.

**Dependencies:** Phase 6.2 (imports schemas). Phase 6.3 ships before Phase 6.6 / Phase 6.7 / Phase 6.8 so those phases can use the lint as a verification surface.

### Phase 6.4 — Helper script `scripts/_next_verified_at_ms.py`

**Deliverable:** `scripts/_next_verified_at_ms.py` implementing the §5.4 strict-monotonic helper.

**Includes:**
- Pure function `next_verified_at_ms(passport_audit_artifacts: list) -> str` per §5.4 pseudocode.
- CLI mode for orchestrator-side invocation: `python scripts/_next_verified_at_ms.py --passport <path>` returns the next valid `verified_at` value as RFC 3339 UTC ms.
- Empty-ledger base case + clock-not-yet-advanced post-condition both covered.
- Unit tests at `scripts/test__next_verified_at_ms.py` with cases: (a) empty ledger, (b) clock fresh, (c) clock stale (helper bumps by 1 ms), (d) multiple prior entries (max selected, not last).

**Verification gate:** `_next_verified_at_ms()` always returns a string strictly greater than every prior `verified_at`; verified by property-based test.

**Dependencies:** Phase 6.2 (`audit_artifact_entry.schema.json` defines the `verdict.verified_at` shape this helper produces).

### Phase 6.5 — Schema 9 amendment in `shared/handoff_schemas.md`

**Deliverable:** `shared/handoff_schemas.md` Schema 9 gains the optional `audit_artifact[]` field per §3.1.

**Includes:**
- New section under Schema 9 documenting `audit_artifact[]` shape, semantics, and append-only ledger discipline.
- `$ref` to `audit_artifact_entry.schema.json` (Phase 6.2 must land first).
- One worked example showing a persisted entry with `MINOR` verdict (matching §3.1 example payload).
- Cross-link to `academic-pipeline/references/passport_as_reset_boundary.md` per R4 mitigation 3 — adds one paragraph to `passport_as_reset_boundary.md` explaining how `audit_artifact[]` re-verifies on resume.

**Verification gate:** `scripts/check_passport_reset_contract.py` (existing v3.6.3 lint) does not regress; `scripts/check_audit_artifact_consistency.py` (Phase 6.3) lint passes on the amendment's example payload.

**Dependencies:** Phase 6.2 (referenced schema must exist).

### Phase 6.6 — Orchestrator agent prompt update

**Deliverable:** `academic-pipeline/agents/pipeline_orchestrator_agent.md` gains §3.5 Audit Artifact Gate subsection per §5.6.

**Includes:**
- Insert a ~50-line decision-policy summary derived from §5.6 between current §3 "Checkpoint Management" and §4 "Transition Management" of the orchestrator prompt. The summary names the trigger and ship/block decision rule, declares hard rules, lists the P-PA-* / P-PB-* failure phase IDs as cross-references back to spec §5.6, and provides cross-references to the spec / audit template / schema / wrapper.
- Path A → Path B fall-through procedural detail (A1, A1.5, A2–A7, B1, B1a, B2–B11) is NOT inserted into the prompt verbatim — that procedure is the implementation contract and stays in spec §5.6. Orchestrator follows the §5.6 procedure exactly; the prompt's role is to declare the gate and reference §5.6 as the procedure source.
- Verification failure state inventory cross-reference (the inventory itself stays in this spec; the orchestrator prompt cites it as a load-bearing reference).
- Hard rules (audit gate cannot be skipped; runs BEFORE collaboration_depth_agent + integrity_verification_agent; PASS does not skip integrity).
- Cross-references to spec, audit template, schema, wrapper.

**Verification gate:** orchestrator prompt is no more than +60 lines vs pre-Step-6 baseline (R3 budget — the ~50-line decision-policy summary plus 5–10 lines of headroom); the §5.6 inventory's phase IDs (P-PA-* / P-PB-*) appear at least once each in the prompt **as cross-references to spec §5.6, not as inline procedural definitions** (the procedural definitions stay in §5.6).

**Dependencies:** Phase 6.2 (schema names) + Phase 6.3 (lint will check this prompt).

### Phase 6.7 — Three downstream agent prompt edits (§6 partial inversion sweep)

**Deliverable:** `synthesis_agent.md`, `research_architect_agent.md`, `report_compiler_agent.md` updated per §6.2 sweep table.

**Includes:**
- Remove the three Clause 2 violation sentences (lines 164 / 190 / 172 at HEAD `b76e626`).
- Trim line 177 of `report_compiler_agent.md` to retire the "The orchestrator runs codex audit afterward" tail.
- Add the canonical Clause 1 line as a bullet to all three PATTERN PROTECTION (v3.6.7) blocks (placed last in each block).
- Create `scripts/v3_6_7_inversion_manifest.json` with the three-file scope per §6.3.
- Extend `scripts/check_v3_6_7_pattern_protection.py` with INV-1 / INV-2 / INV-3 checks per §6.3.
- Add test cases to `scripts/test_check_v3_6_7_pattern_protection.py` for each new INV-x check (positive: prompt currently passing; negative: simulated regression that re-introduces a Clause 2 violation).

**Verification gate:** `scripts/check_v3_6_7_pattern_protection.py` passes with zero INV violations on all three prompts; test suite green.

**Dependencies:** none structurally (Phase 6.7 is independent of Phase 6.1–6.6 file outputs); can run in parallel with Phase 6.1–6.4. **Recommended: bundle with Phase 6.6 in one PR slice** because both touch agent prompts and the lint scripts that check them.

### Phase 6.8 — CI workflow + eval fixtures (§7 Step 8 deliverables)

**Deliverable:**
- 17 micro-fixtures + 1 integration fixture under `tests/fixtures/v3_6_7_pattern_eval/` per §7.
- `scripts/check_pattern_eval_manifest.py` validating each fixture's `manifest.json`. The script reads `fixture_kind` from each manifest and branches: `fixture_kind: "micro"` → validate against the §7.2 micro-fixture schema; `fixture_kind: "integration"` → validate against the §7.3 integration manifest schema. The two schemas share a `pattern_id` enum but have disjoint required fields per §7.3, and routing by `fixture_kind` is what prevents either schema from accidentally rejecting a valid fixture of the other kind.
- `scripts/test_pattern_eval_runtime.py` test harness — for `fixture_kind: "micro"` runs the orchestrator gate procedure against each fixture's BAD/GOOD pair; for `fixture_kind: "integration"` runs the §7.3 round/escalation scenario (the integration fixture has no top-level BAD/GOOD pair — its directory tree is `round_1/` / `round_2/` / `round_3/` / `escalation/` per §7.3, with per-agent sub-fixtures inside each round).
- `.github/workflows/spec-consistency.yml` extended with `pattern-eval-unit` + `pattern-eval-integration` jobs per §7.6.
- L-doc-1 follow-up ticket logged in `docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md` §9.2 (this spec) — the "18 patterns" → "17 patterns" prose retirement covering eight locations (four in the upstream v3.6.7 main spec and four in this spec) is tracked as an issue or TODO file note, not a v3.6.7 spec amendment.

**Includes:**
- 17 micro-fixture directories per the §7.2 schema, each with: `manifest.json`, `upstream_context/passport_snippet.yaml`, `upstream_context/prior_artifacts/`, `bad_run/{deliverable.<ext>,expected_audit_findings.yaml,expected_orchestrator_action.yaml}`, `good_run/{...}`.
- 1 integration fixture under `integration/chapter_level_run/` per §7.3 multi-round structure.
- Path-filtered triggers in `spec-consistency.yml` matching the file list in §7.6.
- Test harness uses synthesized verdicts (reads `expected_audit_findings.yaml` as if codex emitted it) — no real codex execution required for CI green.

**Verification gate:** all 17 micro-fixtures + 1 integration fixture green in `pattern-eval-unit` + `pattern-eval-integration` jobs. `scripts/check_pattern_eval_manifest.py` passes on every fixture. The cross-check between fixture set and pattern inventory (per §7.5) reports 17/17 enumerated patterns covered.

**Dependencies:** Phase 6.1 (wrapper) + Phase 6.2 (schemas) + Phase 6.3 (lint) + Phase 6.4 (strict-monotonic helper, exercised by integration fixture's escalation/ack append step) + Phase 6.5 (Schema 9 amendment, required for the synthetic passport snippet under each fixture's `upstream_context/`) + Phase 6.6 (orchestrator prompt) + Phase 6.7 (downstream prompts). Phase 6.8 is the integration phase that exercises everything earlier phases produced.

### Cross-phase verification

A successful Step 6 + Step 8 ship requires ALL of the following hold simultaneously after Phase 6.8 lands:

1. `.github/workflows/spec-consistency.yml` green: existing checks (`spec-consistency`, `freshness-check`, `pattern-protection`) plus new checks (`audit-artifact-consistency`, `pattern-eval-unit`, `pattern-eval-integration`).
2. `.github/workflows/pytest.yml` green (regression check on v3.6.4 corpus adapters; Step 6 should not touch these but lint script changes can collide).
3. Manual smoke test: the wrapper runs end-to-end against a synthetic deliverable, produces the four artifact files, the orchestrator merges via Path B, the persisted entry appears in the synthesized passport, the §5.6 BLOCK message renders correctly when MATERIAL.
4. Codex review (per `feedback_codex_review_per_schema_increment.md`) on each commit: schema commits (Phase 6.2 / Phase 6.5) and contract commits (Phase 6.6 / Phase 6.7) get incremental codex review; the final integration commit (Phase 6.8) gets a final convergence-to-zero codex review per `feedback_codex_iterative_spec_review_to_zero.md`.

### Sequencing

Recommended commit sequence (one PR with multiple commits, squash-merged):

```
1. Phase 6.2 — schemas (4 new JSON files + README section)
2. Phase 6.4 — helper script + tests
3. Phase 6.1 — wrapper script
4. Phase 6.3 — lint script + tests
5. Phase 6.5 — Schema 9 amendment + reset-boundary cross-link
6. Phase 6.6 — orchestrator prompt update
7. Phase 6.7 — three downstream prompt edits + manifest + lint extension
8. Phase 6.8 — fixtures + CI workflow + L-doc-1 ticket
```

Phases 6.1, 6.2, 6.4 can run in parallel branch-locally before merging into the PR sequence; the listed order is the dependency-resolved sequence for clean reviewability. The PR description carries the §10 phase table as the review roadmap so reviewers can audit phase-by-phase against this spec.

### Estimated commit footprint

| Phase | Files added | Files modified | LoC delta (approx) |
|---|---|---|---|
| 6.1 | `scripts/run_codex_audit.sh` | — | +800 (Bash incl. helpers + traps) |
| 6.2 | 4 schemas + 1 README section | `shared/contracts/README.md` | +400 |
| 6.3 | `scripts/check_audit_artifact_consistency.py` + test file | — | +1200 (lint + tests) |
| 6.4 | `scripts/_next_verified_at_ms.py` + test file | — | +150 |
| 6.5 | — | `shared/handoff_schemas.md`, `academic-pipeline/references/passport_as_reset_boundary.md` | +80 |
| 6.6 | — | `academic-pipeline/agents/pipeline_orchestrator_agent.md` | +60 |
| 6.7 | `scripts/v3_6_7_inversion_manifest.json` | 3 downstream prompts + `scripts/check_v3_6_7_pattern_protection.py` + test file | +50 (mostly lint extension) |
| 6.8 | 18 fixture directories + harness + manifest validator + workflow jobs | `.github/workflows/spec-consistency.yml` | +2500 (fixture data dominates) |

Estimated total: ~5300 LoC, of which ~3000 are fixture data + tests. The implementation budget is consistent with the v3.6.7 Step 1+2 ship envelope (~2800 LoC including the 29-mutation suite); Step 6 is roughly 1.9× the size, weighted toward Phase 6.1 (wrapper) and Phase 6.8 (fixtures).

---

## 11. Sign-off

This spec closes Step 6 (orchestrator hooks for automatic per-agent audit + anti-fake-audit guard) and Step 8 (synthetic evaluation case demonstrating the v3.6.7 patterns triggered + protected) of the v3.6.7 main spec ([`2026-04-29-ars-v3.6.7-downstream-agent-pattern-protection-spec.md`](2026-04-29-ars-v3.6.7-downstream-agent-pattern-protection-spec.md)) §9 implementation table. After Step 6 + Step 8 ship, v3.6.7 is structurally complete: prompt-level pattern protection (Step 1+2) + version sweep (Step 7) + runtime audit-artifact gate (Step 6) + synthetic evaluation case (Step 8) together deliver the "end-to-end deliverable set passes independent xhigh cross-model audit at 0 P1+P2 finding within three rounds" ship-quality target the v3.6.7 main spec §10 declared.

Step 6 + Step 8 land as one follow-up PR after the §1–§5 design (PR #50, main `b76e626`) is on main. The PR description carries §10's phase table as the review roadmap. Codex review per `feedback_codex_iterative_spec_review_to_zero.md` runs to convergence on each commit; the final integration commit (Phase 6.8) is the gate for ship.

The v3.6.7-only scope of §6.2's inversion sweep, §7.1's fixture set, and Step 6's audit gate is preserved; widening to additional agents (e.g., `bibliography_agent`'s five hallucination patterns documented in `feedback_ars_bibliography_agent_hallucination_patterns.md`) is v3.6.8+ work that will land its own spec round and its own version-tagged manifest.

---
<!-- SOURCE-CONTENT-END -->

<a id="source-scripts-run-codex-audit-sh"></a>

## SOURCE: scripts/run_codex_audit.sh

<!-- SOURCE-CONTENT-BEGIN bytes=47168 -->
#!/usr/bin/env bash
# version: 1.0.0
#
# This wrapper is NOT to be invoked by an in-LLM Bash tool call from the same
# session producing the audited deliverable. Allowed invokers: human interactive
# shell, CI workflow step, SubagentStop hook, second-terminal Bash from outside
# the LLM session. Same-session in-LLM invocation creates Pattern C3 exposure.
# See spec §4.7.
#
# Usage:
#   scripts/run_codex_audit.sh \
#     --stage <1-6> \
#     --agent <synthesis_agent|research_architect_agent|report_compiler_agent> \
#     --deliverable <repo-relative-path> \
#     --round <N> \
#     [--target-rounds <N>]       # default 3
#     [--supporting <p1,p2,...>]  # comma-separated repo-relative paths
#     [--previous-findings <path>] # required when --round > 1
#     [--bundle-id <string>]
#     [--output-dir <dir>]        # default audit_artifacts/
#     [--dry-run]                 # validate inputs only; write nothing
#
# Exit codes (§4.6):
#   0    Audit complete; verdict is PASS / MINOR / MATERIAL
#   64   EX_USAGE  — input validation failed (no files written)
#   70   EX_SOFTWARE — AUDIT_FAILED (JSONL parse error or bundle mutation)
#   73   EX_CANTCREAT — tee write failed; JSONL integrity not guaranteed
#   75   EX_TEMPFAIL — codex rate-limited / transient error (retry candidate)
#   other  codex non-zero exit (preserved as-is; AUDIT_FAILED artifact set written)

set -euo pipefail

# ---------------------------------------------------------------------------
# Bash version guard — §4.1 requires Bash 4+ for indexed arrays, read -ra, <<<
# ---------------------------------------------------------------------------
if [[ "${BASH_VERSINFO[0]}" -lt 4 ]]; then
  printf '[run_codex_audit] error: Bash 4+ required (found %s). On macOS: brew install bash\n' \
    "${BASH_VERSION}" >&2
  exit 64
fi

# ---------------------------------------------------------------------------
# Helper functions — defined before the dependency preflight so they are
# available for the _sha256 check itself.
# ---------------------------------------------------------------------------

# SHA-256 backend selection — cached once to avoid forking `command -v` per call
# (Step 0b + Step 3a together produce 8+ hash calls).
if command -v sha256sum >/dev/null 2>&1; then
  _SHA256_CMD=(sha256sum)
else
  _SHA256_CMD=(shasum -a 256)
fi

# _sha256 <path>
# Portable SHA-256 hex digest. Prefers GNU sha256sum (Linux / coreutils);
# falls back to BSD shasum -a 256 (macOS stock).
_sha256() {
  "${_SHA256_CMD[@]}" "$1" | awk '{print $1}'
}

# _sha256_str <string>
# SHA-256 of an in-memory string (for the bundle manifest).
_sha256_str() {
  printf '%s' "$1" | "${_SHA256_CMD[@]}" | awk '{print $1}'
}

# _atomic_write <dest-path>
# Reads stdin, writes to <dest>.tmp, fsyncs, then renames over <dest>.
# Used for sidecar, verdict, and proposal entry — the three files §4.4 §4.8
# guarantees orchestrator observes whole-or-not-at-all. JSONL is exempt
# because codex streams it over the audit's runtime; see §4.4 atomicity note.
#
# F-010 (§3.6): each sub-step (cat, fsync, mv) is explicitly error-checked.
# A raw cat/fsync/mv failure with set -euo pipefail would abort the wrapper
# before AUDIT_FAILED artifacts are written, violating §4.6 invariant E8.
# All three failure cases now emit a diagnostic and exit 73 (EX_CANTCREAT).
_atomic_write() {
  local path="$1"
  local tmp="${path}.tmp"
  if ! cat > "${tmp}" 2>/dev/null; then
    printf '[run_codex_audit] error: failed to write %s\n' "${tmp}" >&2
    exit 73
  fi
  if command -v python3 >/dev/null 2>&1; then
    if ! python3 -c "import os,sys; f=open(sys.argv[1],'rb'); os.fsync(f.fileno()); f.close()" "${tmp}" 2>/dev/null; then
      rm -f "${tmp}"
      printf '[run_codex_audit] error: fsync failed for %s\n' "${tmp}" >&2
      exit 73
    fi
  else
    sync
  fi
  if ! mv -f "${tmp}" "${path}" 2>/dev/null; then
    rm -f "${tmp}"
    printf '[run_codex_audit] error: rename failed for %s\n' "${path}" >&2
    exit 73
  fi
}

# _extract_jsonl_thread_id <jsonl-path>
# Returns the thread_id from the first thread.started event, or empty string
# when JSONL is missing / empty / lacks a parseable thread.started event.
# codex 0.125+ emits thread_id only on the opening thread.started event (§3.3).
#
# F-001 (§3.6): jq must be non-fatal. A SIGKILL'd or disk-full partial JSONL can
# make jq exit non-zero; with set -euo pipefail that would abort the wrapper BEFORE
# the mandatory AUDIT_FAILED sidecar/verdict/proposal trio is written, violating §4.6
# invariant E8. The `|| printf ''` ensures the function always returns success.
_extract_jsonl_thread_id() {
  local path="$1"
  if [[ ! -s "${path}" ]]; then
    printf ''
    return 0
  fi
  # F-015 (§3.1): jq emits the literal string "null" when thread_id is absent or
  # non-string; a malformed thread.started event would then propagate "null" into
  # the sidecar's stream.jsonl_thread_id, failing the schema UUID regex.
  # Chain select(type == "string") + UUID-pattern guard to degrade gracefully to
  # empty string (permitted by schema when companion verdict is AUDIT_FAILED).
  jq -r '
    select(.type == "thread.started")
    | .thread_id
    | select(type == "string")
    | select(test("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"))
  ' "${path}" 2>/dev/null \
    | head -1 \
    || printf ''
}

# _codex_version
# Extracts bare semver from `codex --version`. codex 0.125+ prints
# "codex-cli X.Y.Z" (e.g., "codex-cli 0.128.0"); we strip the prefix and return just the dotted-triple.
# Exits 64 if no semver-shaped token is found — guards against future CLI
# format changes silently leaking garbage into the sidecar's codex_cli_version.
_codex_version() {
  local v
  v=$(codex --version 2>/dev/null \
    | awk 'match($0, /[0-9]+\.[0-9]+\.[0-9]+/) { print substr($0, RSTART, RLENGTH); exit }')
  if [[ -z "${v}" ]]; then
    printf '[run_codex_audit] error: cannot parse semver from `codex --version`\n' >&2
    exit 64
  fi
  printf '%s\n' "${v}"
}

# _now_rfc3339_ms
# UTC timestamp with millisecond precision in RFC 3339 format.
# Format: YYYY-MM-DDTHH:MM:SS.mmmZ  (colons in time — JSON field format).
# This is the JSON/sidecar field format; run_id uses hyphens instead.
_now_rfc3339_ms() {
  python3 -c "
import datetime
now = datetime.datetime.now(datetime.timezone.utc)
ms = now.strftime('%Y-%m-%dT%H:%M:%S') + '.{:03d}Z'.format(now.microsecond // 1000)
print(ms)
"
}

# _random_4hex
# Four random lowercase hex characters from /dev/urandom.
# Used as the run_id suffix to disambiguate sub-second concurrent runs.
_random_4hex() {
  od -An -N2 -tx1 < /dev/urandom | tr -d ' \n'
}

# _make_run_id
# Generates a run_id per §3.1 / §3.7 F1 contract:
#   <ISO-8601-Z>-<4-hex>
# where the date-time portion uses HYPHENS in place of colons (filename safe).
# Example: 2026-04-30T15-22-04Z-d8f3
# Note: JSON field values (started_at, ended_at) use colons per RFC 3339.
_make_run_id() {
  local dt
  dt=$(python3 -c "
import datetime
now = datetime.datetime.now(datetime.timezone.utc)
print(now.strftime('%Y-%m-%dT%H-%M-%SZ'))
")
  printf '%s-%s\n' "${dt}" "$(_random_4hex)"
}

# _duration_seconds <started_at_rfc3339_ms> <ended_at_rfc3339_ms>
# Returns elapsed seconds as a float.
# F-009 (§3.1): clamp to minimum 0.001 — audit_sidecar.schema.json sets
# duration_seconds exclusiveMinimum: 0; very fast failures (codex exits before
# 1ms) would produce 0.000 which violates the schema constraint.
_duration_seconds() {
  python3 -c "
import datetime, sys
fmt = '%Y-%m-%dT%H:%M:%S.%fZ'
t0 = datetime.datetime.strptime(sys.argv[1], fmt)
t1 = datetime.datetime.strptime(sys.argv[2], fmt)
secs = (t1-t0).total_seconds()
# Clamp to schema exclusiveMinimum: 0
if secs <= 0:
    secs = 0.001
print('{:.3f}'.format(secs))
" "$1" "$2"
}

# _git_dirty
# Prints 'true' when the working tree is dirty, 'false' otherwise.
# Uses `--exit-code` so diff exits non-zero on dirty state; we catch that.
_git_dirty() {
  if git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null; then
    printf 'false'
  else
    printf 'true'
  fi
}

# _to_repo_relative <path>
# If <path> is absolute, strip the leading slash (unlikely — §4.2 says
# deliverable is repo-relative, but belt-and-suspenders). If it starts with
# ./ normalize that away. Does not validate ..; that is the caller's job.
_to_repo_relative() {
  local p="$1"
  # Remove leading ./
  p="${p#./}"
  printf '%s' "${p}"
}

# _validate_repo_relative <path> <flag-name>
# F-006 (§3.1): Validates the path satisfies the audit_sidecar.schema.json
# repo_relative_path constraint: no leading /, no whitespace, no .. segments.
# Absolute paths, .. traversals, or whitespace paths fail schema validation
# downstream (proposal entry artifact_paths.{jsonl,sidecar,verdict} regex).
# Exits EX_USAGE 64 on violation.
_validate_repo_relative() {
  local path="$1"
  local flag="$2"
  # Must not be empty
  if [[ -z "${path}" ]]; then
    printf '[run_codex_audit] error: %s path must not be empty\n' "${flag}" >&2
    exit 64
  fi
  # Must not be absolute (leading /)
  if [[ "${path}" == /* ]]; then
    printf '[run_codex_audit] error: %s path must be repo-relative (no leading /): %s\n' \
      "${flag}" "${path}" >&2
    exit 64
  fi
  # Must not contain whitespace
  if [[ "${path}" =~ [[:space:]] ]]; then
    printf '[run_codex_audit] error: %s path must not contain whitespace: %s\n' \
      "${flag}" "${path}" >&2
    exit 64
  fi
  # Must not contain .. segments (path traversal)
  if [[ "${path}" =~ (^|/)\.\.(/|$) ]]; then
    printf '[run_codex_audit] error: %s path must not contain .. segments: %s\n' \
      "${flag}" "${path}" >&2
    exit 64
  fi
}

# _json_escape <string>
# Minimal JSON string escaping (backslash, double-quote, control chars).
_json_escape() {
  python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$1"
}

# _yaml_escape_oneline <string>
# Produce a safe single-quoted YAML scalar. Single-quotes are escaped by
# doubling them per YAML spec.
_yaml_escape_oneline() {
  local s="$1"
  # Replace ' with '' for YAML single-quote escaping
  s="${s//\'/\'\'}"
  printf "'%s'" "${s}"
}

# ---------------------------------------------------------------------------
# Dependency preflight — exits 64 with "missing dependency: <name>" before
# any artifact write. Checked: bash (version already done above), git, awk,
# jq, od, tr, uname, sort, head, tee, mv, python3, codex, sha256sum|shasum.
# ---------------------------------------------------------------------------
_check_dep() {
  local cmd="$1"
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    printf '[run_codex_audit] error: missing dependency: %s\n' "${cmd}" >&2
    exit 64
  fi
}

for _dep in git awk jq od tr uname sort head tee mv python3 codex; do
  _check_dep "${_dep}"
done

# SHA-256 helper: need at least one of sha256sum or shasum
if ! command -v sha256sum >/dev/null 2>&1 && ! command -v shasum >/dev/null 2>&1; then
  printf '[run_codex_audit] error: missing dependency: sha256sum or shasum\n' >&2
  exit 64
fi

# ---------------------------------------------------------------------------
# Input parsing
# ---------------------------------------------------------------------------
STAGE=""
AGENT=""
DELIVERABLE=""
SUPPORTING_CSV=""
ROUND=""
TARGET_ROUNDS="3"
PREV_FINDINGS=""
OUT_DIR="audit_artifacts"
BUNDLE_ID=""
DRY_RUN=false

# F-005 (§3.5): require_arg guards all value-taking flags so a missing operand
# (e.g. `--stage --agent foo`) exits EX_USAGE 64, not set -u unbound-variable
# exit 1. Checks $# >= 2 AND next token doesn't look like a flag (^--).
_require_arg() {
  local flag="$1"
  # $# here is the caller's argument count after its own shift operations.
  # We receive $# from the while-loop via the special `shift` semantics below;
  # instead test the second positional ($2) of the calling while iteration.
  # Because this is called from within the case block, $2 is the while-loop's $2.
  if [[ $# -lt 3 || "$3" =~ ^-- ]]; then
    printf '[run_codex_audit] error: %s requires a value\n' "${flag}" >&2
    exit 64
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --stage)
      if [[ $# -lt 2 || "$2" =~ ^-- ]]; then
        printf '[run_codex_audit] error: --stage requires a value\n' >&2; exit 64
      fi
      STAGE="$2"; shift 2 ;;
    --agent)
      if [[ $# -lt 2 || "$2" =~ ^-- ]]; then
        printf '[run_codex_audit] error: --agent requires a value\n' >&2; exit 64
      fi
      AGENT="$2"; shift 2 ;;
    --deliverable)
      if [[ $# -lt 2 || "$2" =~ ^-- ]]; then
        printf '[run_codex_audit] error: --deliverable requires a value\n' >&2; exit 64
      fi
      DELIVERABLE="$2"; shift 2 ;;
    --supporting)
      if [[ $# -lt 2 || "$2" =~ ^-- ]]; then
        printf '[run_codex_audit] error: --supporting requires a value\n' >&2; exit 64
      fi
      SUPPORTING_CSV="$2"; shift 2 ;;
    --round)
      if [[ $# -lt 2 || "$2" =~ ^-- ]]; then
        printf '[run_codex_audit] error: --round requires a value\n' >&2; exit 64
      fi
      ROUND="$2"; shift 2 ;;
    --target-rounds)
      if [[ $# -lt 2 || "$2" =~ ^-- ]]; then
        printf '[run_codex_audit] error: --target-rounds requires a value\n' >&2; exit 64
      fi
      TARGET_ROUNDS="$2"; shift 2 ;;
    --previous-findings)
      if [[ $# -lt 2 || "$2" =~ ^-- ]]; then
        printf '[run_codex_audit] error: --previous-findings requires a value\n' >&2; exit 64
      fi
      PREV_FINDINGS="$2"; shift 2 ;;
    --output-dir)
      if [[ $# -lt 2 || "$2" =~ ^-- ]]; then
        printf '[run_codex_audit] error: --output-dir requires a value\n' >&2; exit 64
      fi
      OUT_DIR="$2"; shift 2 ;;
    --bundle-id)
      if [[ $# -lt 2 || "$2" =~ ^-- ]]; then
        printf '[run_codex_audit] error: --bundle-id requires a value\n' >&2; exit 64
      fi
      BUNDLE_ID="$2"; shift 2 ;;
    --dry-run)       DRY_RUN=true;       shift   ;;
    # Explicitly reject flags from early drafts that are NOT part of §4.2
    --bundle)
      printf '[run_codex_audit] error: --bundle is not a valid flag (use --bundle-id); see spec §4.2\n' >&2
      exit 64
      ;;
    --audit-template)
      printf '[run_codex_audit] error: --audit-template is not a valid flag; see spec §4.2\n' >&2
      exit 64
      ;;
    *)
      printf '[run_codex_audit] error: unknown flag: %s\n' "$1" >&2
      exit 64
      ;;
  esac
done

# ---------------------------------------------------------------------------
# Input validation (§4.2) — all failures → exit 64 EX_USAGE
# ---------------------------------------------------------------------------

# Required flags
for _flag_name in STAGE AGENT DELIVERABLE ROUND; do
  _flag_val="${!_flag_name}"
  if [[ -z "${_flag_val}" ]]; then
    _flag_cli=$(printf '%s' "${_flag_name}" | tr 'A-Z_' 'a-z-')
    printf '[run_codex_audit] error: --%s is required\n' "${_flag_cli}" >&2
    exit 64
  fi
done

# --stage: integer 1-6
if ! [[ "${STAGE}" =~ ^[1-6]$ ]]; then
  printf '[run_codex_audit] error: --stage must be an integer 1-6 (got: %s)\n' "${STAGE}" >&2
  exit 64
fi

# --agent: closed enum
case "${AGENT}" in
  synthesis_agent|research_architect_agent|report_compiler_agent) ;;
  *)
    printf '[run_codex_audit] error: --agent must be one of synthesis_agent, research_architect_agent, report_compiler_agent (got: %s)\n' "${AGENT}" >&2
    exit 64
    ;;
esac

# --deliverable: must exist and be readable
if [[ ! -f "${DELIVERABLE}" || ! -r "${DELIVERABLE}" ]]; then
  printf '[run_codex_audit] error: --deliverable not found or not readable: %s\n' "${DELIVERABLE}" >&2
  exit 64
fi

# --round: integer >= 1
if ! [[ "${ROUND}" =~ ^[0-9]+$ ]] || [[ "${ROUND}" -lt 1 ]]; then
  printf '[run_codex_audit] error: --round must be an integer >= 1 (got: %s)\n' "${ROUND}" >&2
  exit 64
fi

# --target-rounds: integer >= 1
if ! [[ "${TARGET_ROUNDS}" =~ ^[0-9]+$ ]] || [[ "${TARGET_ROUNDS}" -lt 1 ]]; then
  printf '[run_codex_audit] error: --target-rounds must be an integer >= 1 (got: %s)\n' "${TARGET_ROUNDS}" >&2
  exit 64
fi

# --round <= --target-rounds (§3.7 A3)
if [[ "${ROUND}" -gt "${TARGET_ROUNDS}" ]]; then
  printf '[run_codex_audit] error: --round (%s) must be <= --target-rounds (%s)\n' \
    "${ROUND}" "${TARGET_ROUNDS}" >&2
  exit 64
fi

# --previous-findings required when --round > 1 (audit template Section 4(a) violation)
if [[ "${ROUND}" -gt 1 && -z "${PREV_FINDINGS}" ]]; then
  printf '[run_codex_audit] error: --previous-findings is required when --round > 1\n' >&2
  exit 64
fi

if [[ -n "${PREV_FINDINGS}" && ! -f "${PREV_FINDINGS}" ]]; then
  printf '[run_codex_audit] error: --previous-findings not found: %s\n' "${PREV_FINDINGS}" >&2
  exit 64
fi

# --supporting: each path must exist
declare -a SUPPORTING=()
if [[ -n "${SUPPORTING_CSV}" ]]; then
  IFS=',' read -ra SUPPORTING <<< "${SUPPORTING_CSV}"
  for _sup_path in "${SUPPORTING[@]}"; do
    if [[ ! -f "${_sup_path}" ]]; then
      printf '[run_codex_audit] error: --supporting path not found: %s\n' "${_sup_path}" >&2
      exit 64
    fi
  done
fi

# ---------------------------------------------------------------------------
# F-017 (§3.6): inject --previous-findings into SUPPORTING before snapshot.
# Multi-round audits depend on the previous-findings file as context input.
# If it is NOT included in the bundle manifest, it can mutate between snapshot
# and codex invocation without detection — codex audits against different
# findings than the manifest claims.
#
# Fix: treat --previous-findings as a mandatory supporting file for round > 1.
# Inject it into the SUPPORTING array here (dedup by path so a user who also
# listed it in --supporting does not see duplicate content in the prompt).
# This preserves the §3.6 manifest role enum (primary | supporting | template)
# without adding a fourth role.
#
# audit_snapshot.py reads PREV_FINDINGS as part of the supporting bundle, so
# its bytes are snapshotted alongside other supporting files and its SHA enters
# the manifest — no live cat call after snapshot phase.
# ---------------------------------------------------------------------------
if [[ -n "${PREV_FINDINGS}" ]]; then
  _pf_already_in=0
  for _s in "${SUPPORTING[@]+"${SUPPORTING[@]}"}"; do
    if [[ "${_s}" = "${PREV_FINDINGS}" ]]; then
      _pf_already_in=1
      break
    fi
  done
  if [[ "${_pf_already_in}" -eq 0 ]]; then
    SUPPORTING+=("${PREV_FINDINGS}")
  fi
fi

# Audit template path — constant per §3.4 schema constraint
readonly AUDIT_TEMPLATE_PATH="shared/templates/codex_audit_multifile_template.md"
if [[ ! -f "${AUDIT_TEMPLATE_PATH}" ]]; then
  printf '[run_codex_audit] error: audit template not found: %s\n' "${AUDIT_TEMPLATE_PATH}" >&2
  exit 64
fi

# ---------------------------------------------------------------------------
# F-016 (§3.1): Normalize and validate all path inputs BEFORE the dry-run
# early-exit check.  Previously the _to_repo_relative + _validate_repo_relative
# calls came AFTER Step 0a, so --dry-run reported "inputs valid" even when
# an absolute or .. path would have failed EX_USAGE 64 on a real run.
# These calls are pure validation (no mkdir, no file writes), so reordering
# is safe and preserves the "dry-run is side-effect-free" invariant.
# ---------------------------------------------------------------------------
DELIVERABLE=$(_to_repo_relative "${DELIVERABLE}")
# F-006 (§3.1): validate deliverable and supporting paths satisfy repo_relative_path
# schema constraint (no leading /, no whitespace, no .. segments) AFTER normalization.
# Rejects /tmp/... or ../... paths that fail audit_artifact_entry schema validation.
_validate_repo_relative "${DELIVERABLE}" "--deliverable"
_norm_supporting=()
for _s in "${SUPPORTING[@]+"${SUPPORTING[@]}"}"; do
  _norm_sup=$(_to_repo_relative "${_s}")
  _validate_repo_relative "${_norm_sup}" "--supporting"
  _norm_supporting+=("${_norm_sup}")
done
SUPPORTING=("${_norm_supporting[@]+"${_norm_supporting[@]}"}")
# Normalize PREV_FINDINGS to match the normalized SUPPORTING entries (F-017):
# audit_snapshot.py dedupes PREV_FINDINGS against SUPPORTING by path equality,
# so paths must agree after _to_repo_relative normalization or both will be
# snapshotted as separate entries.
if [[ -n "${PREV_FINDINGS}" ]]; then
  PREV_FINDINGS=$(_to_repo_relative "${PREV_FINDINGS}")
fi
# F-014 (§3.1): validate --output-dir BEFORE mkdir -p to avoid creating a
# directory at an invalid path (absolute, .. traversal) before EX_USAGE 64 rejects it.
# "No side effects on input validation rejection" — mkdir must not fire first.
_validate_repo_relative "${OUT_DIR}" "--output-dir"

# ---------------------------------------------------------------------------
# Step 0a — dry-run early exit. §10 Phase 6.1 verification gate and §1.2
# threat model: writing artifacts at zero codex cost is Pattern C3 attack
# surface. --dry-run is input-validation only; nothing is written.
# (F-016: path validation runs above, before this check, so dry-run correctly
# rejects absolute/.. paths rather than reporting "inputs valid" for them.)
# ---------------------------------------------------------------------------
if [[ "${DRY_RUN}" = true ]]; then
  printf '[run_codex_audit] dry-run: inputs valid; no files written\n'
  exit 0
fi

# ---------------------------------------------------------------------------
# SIGTERM / SIGINT trap — F-059 closure.
# On termination: clean up partial artifacts (*.tmp + empty JSONL placeholder)
# and exit 75 (EX_TEMPFAIL). run_id may not be set yet when the trap fires,
# so we record it in a variable that the trap closure reads.
# ---------------------------------------------------------------------------
_CURRENT_RUN_ID=""
_OUT_DIR_FOR_TRAP=""

_cleanup_on_signal() {
  local rid="${_CURRENT_RUN_ID}"
  local odir="${_OUT_DIR_FOR_TRAP}"
  if [[ -n "${rid}" && -n "${odir}" ]]; then
    rm -f \
      "${odir}/${rid}.jsonl" \
      "${odir}/${rid}.meta.json" \
      "${odir}/${rid}.meta.json.tmp" \
      "${odir}/${rid}.verdict.yaml" \
      "${odir}/${rid}.verdict.yaml.tmp" \
      "${odir}/${rid}.audit_artifact_entry.json" \
      "${odir}/${rid}.audit_artifact_entry.json.tmp" \
      "${odir}/${rid}.stdout" \
      "${odir}/${rid}.stderr" \
      "${odir}/${rid}.manifest.txt" 2>/dev/null || true
  fi
  printf '[run_codex_audit] caught signal; cleaned up partial artifacts; exiting 75\n' >&2
  exit 75
}

trap '_cleanup_on_signal' SIGTERM SIGINT

# F-010 (§3.6): EXIT trap removes partial .tmp artifacts left by any aborted
# _atomic_write call. Preserves final contract files (no .tmp suffix).
# Coexists with SIGTERM/SIGINT trap above — EXIT fires after signal handler exits.
_cleanup_partials_on_exit() {
  if [[ -n "${run_id:-}" && -n "${OUT_DIR:-}" ]]; then
    rm -f "${OUT_DIR}/${run_id}".*.tmp 2>/dev/null || true
  fi
}
trap '_cleanup_partials_on_exit' EXIT

# ---------------------------------------------------------------------------
# Setup: run_id, output dir, codex version, git metadata
# ---------------------------------------------------------------------------
# Note: path normalization + validation (DELIVERABLE, SUPPORTING, OUT_DIR)
# was moved above Step 0a (F-016 fix) — paths are already normalized here.
run_id=$(_make_run_id)
_CURRENT_RUN_ID="${run_id}"

# F-010 (§3.6): normalize mkdir failure to EX_CANTCREAT 73.
# mkdir intentionally stays AFTER dry-run: dry-run must be side-effect-free.
if ! mkdir -p "${OUT_DIR}" 2>/dev/null; then
  printf '[run_codex_audit] error: cannot create output dir: %s\n' "${OUT_DIR}" >&2
  exit 73
fi
_OUT_DIR_FOR_TRAP="${OUT_DIR}"

CODEX_VERSION=$(_codex_version)
GIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || printf 'unknown')
GIT_DIRTY=$(_git_dirty)
HOSTNAME_VAL=$(uname -n)
CWD_VAL=$(pwd)

# Primary deliverable array (always exactly one element)
declare -a PRIMARY=("${DELIVERABLE}")

# ---------------------------------------------------------------------------
# F-018 (§3.6): Reject binary/NUL inputs before snapshot.
# ---------------------------------------------------------------------------
# Step 0b — snapshot bundle (DELEGATED TO scripts/audit_snapshot.py).
#
# Round 5 architectural redesign: the Bash-side snapshot helper had three
# structural failures across rounds 1-5 of codex review:
#
#   F-004 (5 rounds partial): Bash command substitution runs the helper in a
#     subshell, so global SHA assignment didn't propagate to the parent.
#   F-018 (Round 4 fix broke wrapper): grep -q $'\0' is empty pattern → all
#     non-empty files rejected as binary.
#   F-020 (trailing newline drift): $(cat file) strips \n; manifest SHA from
#     in-memory content drifts from sha256sum(file) → Step 3a false-positive.
#
# All three are eliminated by moving byte-exact operations to Python:
#   - Single read per file (no TOCTOU window)
#   - Binary-safe NUL detection (b"\0" in content)
#   - hashlib.sha256(file_bytes) matches sha256sum(file) exactly
#
# scripts/audit_snapshot.py snapshot mode:
#   - Reads all bundle files as bytes (binary-safe)
#   - Rejects NUL-containing files (exit 64)
#   - Computes per-file SHA-256 + bundle manifest SHA from same bytes
#   - Writes <run_id>.manifest.txt and <run_id>.prompt.txt
#   - Emits JSON summary to stdout for the wrapper to consume
#
# Step 3a uses scripts/audit_snapshot.py verify mode against the same manifest;
# their SHAs match exactly (no trailing-newline drift).
# ---------------------------------------------------------------------------

# F-021 (§3.6) closure: dedup --previous-findings against SUPPORTING after
# normalization (which the wrapper does upstream). audit_snapshot.py also
# dedupes internally; doing it here too prevents the manifest from listing
# the same file under both --supporting and --previous-findings paths.
if [[ -n "${PREV_FINDINGS}" ]]; then
  _already_in_supporting=0
  for _s in "${SUPPORTING[@]+"${SUPPORTING[@]}"}"; do
    if [[ "${_s}" = "${PREV_FINDINGS}" ]]; then
      _already_in_supporting=1
      break
    fi
  done
  if [[ "${_already_in_supporting}" -eq 0 ]]; then
    SUPPORTING+=("${PREV_FINDINGS}")
  fi
fi

# Build snapshot CLI args (--primary repeated, --supporting repeated)
_snap_args=()
for _p in "${PRIMARY[@]}"; do
  _snap_args+=("--primary" "${_p}")
done
for _s in "${SUPPORTING[@]+"${SUPPORTING[@]}"}"; do
  _snap_args+=("--supporting" "${_s}")
done

# Run snapshot helper. Capture JSON summary on stdout, errors on stderr.
SNAPSHOT_JSON_FILE="${OUT_DIR}/${run_id}.snapshot.tmp"
SNAPSHOT_STDERR_FILE="${OUT_DIR}/${run_id}.snapshot_stderr.tmp"
set +e
_prev_findings_arg=()
if [[ -n "${PREV_FINDINGS}" ]]; then
  _prev_findings_arg=(--previous-findings "${PREV_FINDINGS}")
fi

python3 scripts/audit_snapshot.py snapshot \
  "${_snap_args[@]}" \
  "${_prev_findings_arg[@]+"${_prev_findings_arg[@]}"}" \
  --audit-template "${AUDIT_TEMPLATE_PATH}" \
  --output-dir "${OUT_DIR}" \
  --run-id "${run_id}" \
  --round "${ROUND}" \
  --target-rounds "${TARGET_ROUNDS}" \
  --git-sha "${GIT_SHA}" \
  --stage "${STAGE}" \
  --agent "${AGENT}" \
  > "${SNAPSHOT_JSON_FILE}" \
  2> "${SNAPSHOT_STDERR_FILE}"
SNAPSHOT_EXIT=$?
set -e

if [[ "${SNAPSHOT_EXIT}" -ne 0 ]]; then
  # Forward Python error to user. exit 64 (NUL detection / bad args) propagates;
  # exit 2 (file not found / OSError) we surface as exit 73 (EX_CANTCREAT).
  cat "${SNAPSHOT_STDERR_FILE}" >&2
  rm -f "${SNAPSHOT_JSON_FILE}" "${SNAPSHOT_STDERR_FILE}"
  case "${SNAPSHOT_EXIT}" in
    64) exit 64 ;;
    2)  exit 73 ;;
    *)  exit "${SNAPSHOT_EXIT}" ;;
  esac
fi

# Parse JSON summary into Bash variables. Use python3 for reliable JSON access
# (jq might not be present; we already require python3 in §4.1 dependency table).
BUNDLE_MANIFEST_SHA=$(python3 -c "
import json, sys
d = json.load(open(sys.argv[1]))
print(d['manifest_sha'])
" "${SNAPSHOT_JSON_FILE}")

AUDIT_TEMPLATE_SHA_PRE=$(python3 -c "
import json, sys
d = json.load(open(sys.argv[1]))
print(d['audit_template_sha'])
" "${SNAPSHOT_JSON_FILE}")

SHA_DELIVERABLE=$(python3 -c "
import json, sys
d = json.load(open(sys.argv[1]))
print(d['primary_files'][0]['sha'])
" "${SNAPSHOT_JSON_FILE}")

SNAPSHOT_PROMPT_PATH="${OUT_DIR}/${run_id}.prompt.txt"
SNAPSHOT_MANIFEST_PATH="${OUT_DIR}/${run_id}.manifest.txt"

# Clean up temp files (manifest.txt and prompt.txt remain — they're contract artifacts)
rm -f "${SNAPSHOT_STDERR_FILE}"
# Keep SNAPSHOT_JSON_FILE for sidecar emission (need to enumerate primary/supporting).

# Initialize mutation state. Step 3a (post-codex SHA recompute) may set these.
# Declaring here ensures BUNDLE_MUTATION_FILES is always an array.
BUNDLE_MUTATION_DETECTED=0
declare -a BUNDLE_MUTATION_FILES=()

# ---------------------------------------------------------------------------
# Step 1 — prompt rendered by audit_snapshot.py (Step 0b above) into
# <run_id>.prompt.txt. The Bash wrapper feeds it to codex stdin via shell
# redirection in Step 2b. No template-rendering logic in Bash anymore — that
# moved to Python alongside the byte-exact snapshot, so the prompt embeds
# exactly the snapshotted bytes (no trailing-newline drift, no second cat).
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Step 0c — REMOVED in Round 5 architecture.
# Bash-side TOCTOU defenses (Steps 0b/0c partial across rounds 1-5) are gone.
# audit_snapshot.py reads each file ONCE and computes both SHA and prompt bytes
# from the same read — there is no second-read window to defend against.
# Step 3a (post-codex) still detects post-snapshot disk mutations.
# ---------------------------------------------------------------------------
PRE_CODEX_MUTATION_DETECTED=0  # no pre-codex check needed; kept for Step 2b gate

# ---------------------------------------------------------------------------
# Step 2a — pre-touch empty JSONL placeholder (F-059 closure).
# This ensures the file exists at its final path even if codex is killed before
# emitting any output. AUDIT_FAILED verdict referencing an empty JSONL is
# handled correctly by §5.6 Path B5 short-circuit without Layer 2 validation.
#
# F-010 (§3.6): guard the pre-touch; a failure here (permissions, disk full)
# means the JSONL path would never be created, breaking the artifact invariant
# E8.  Exit 73 (EX_CANTCREAT) to signal the output directory is unusable.
# ---------------------------------------------------------------------------
if ! : > "${OUT_DIR}/${run_id}.jsonl" 2>/dev/null; then
  printf '[run_codex_audit] error: cannot create jsonl placeholder: %s\n' \
    "${OUT_DIR}/${run_id}.jsonl" >&2
  exit 73
fi

# ---------------------------------------------------------------------------
# Step 2b — invoke codex CLI.
#
# Skipped when PRE_CODEX_MUTATION_DETECTED=1 (Step 0c, F-004): bundle was
# mutated between SHA snapshot and prompt render; no codex invocation needed
# since BUNDLE_MUTATION_DETECTED is already set and Step 4 will emit AUDIT_FAILED.
#
# We use a real pipeline + ${PIPESTATUS[@]}, NOT process substitution
# `> >(tee ...)`, because:
#   1. Process substitution hides tee's exit status (wrapper never knows if
#      tee failed — disk full / EIO would silently corrupt the JSONL artifact).
#   2. Process substitution races on draining: orchestrator can read the JSONL
#      before the tee subshell flushes.
#   3. PIPESTATUS captures both codex exit (pipe[0]) AND tee exit (pipe[1]).
#
# `set +e` is required because pipefail would abort on codex's non-zero exit
# before ${PIPESTATUS[@]} is captured. We re-enable after capture.
#
# This is `codex exec`, not `codex exec resume` — every audit run starts a
# fresh thread; the wrapper never resumes a prior thread.
# ---------------------------------------------------------------------------
STARTED_AT=$(_now_rfc3339_ms)
CODEX_EXIT=0
TEE_EXIT=0

if [[ "${PRE_CODEX_MUTATION_DETECTED}" -eq 0 ]]; then
  set +e
  codex exec \
    -m gpt-5.5 \
    -c 'model_reasoning_effort="xhigh"' \
    --json \
    - \
    2> "${OUT_DIR}/${run_id}.stderr" \
    < "${SNAPSHOT_PROMPT_PATH}" \
    | tee "${OUT_DIR}/${run_id}.stdout" > "${OUT_DIR}/${run_id}.jsonl"
  pipe=("${PIPESTATUS[@]}")
  CODEX_EXIT="${pipe[0]}"
  TEE_EXIT="${pipe[1]}"
  set -e
fi

ENDED_AT=$(_now_rfc3339_ms)

# tee write failure → EX_CANTCREAT (73): JSONL integrity not guaranteed.
# Clean up all partial artifacts so orchestrator never sees a sidecar/verdict/
# proposal pointing at a corrupt JSONL.
if [[ "${TEE_EXIT}" -ne 0 ]]; then
  rm -f \
    "${OUT_DIR}/${run_id}.jsonl" \
    "${OUT_DIR}/${run_id}.stdout" \
    "${OUT_DIR}/${run_id}.stderr" \
    "${OUT_DIR}/${run_id}.manifest.txt" 2>/dev/null || true
  printf '[run_codex_audit] error: tee write failed (exit %s); JSONL artifact may be corrupt\n' \
    "${TEE_EXIT}" >&2
  exit 73
fi

# ---------------------------------------------------------------------------
# Step 3a — detect post-snapshot disk mutation via audit_snapshot.py verify.
# Compares each manifest entry's recorded SHA against current file content.
# Round 5 redesign: byte-exact comparison via Python (hashlib reads disk bytes
# verbatim), so manifest SHA and recompute SHA agree on trailing-newline
# semantics — F-020 false-positive (Bash strips \n, sha256sum doesn't) is gone.
#
# Output: list of mutated paths to stdout (one per line) on exit 1; empty
# stdout on exit 0 (no mutation).
# ---------------------------------------------------------------------------
VERIFY_OUT_FILE="${OUT_DIR}/${run_id}.verify_stdout.tmp"
set +e
python3 scripts/audit_snapshot.py verify \
  --manifest "${SNAPSHOT_MANIFEST_PATH}" \
  > "${VERIFY_OUT_FILE}" \
  2>/dev/null
VERIFY_EXIT=$?
set -e

if [[ "${VERIFY_EXIT}" -eq 1 ]]; then
  # Mutation detected — read mutated paths from stdout.
  while IFS= read -r _mutated_path; do
    if [[ -n "${_mutated_path}" ]]; then
      BUNDLE_MUTATION_DETECTED=1
      BUNDLE_MUTATION_FILES+=("${_mutated_path}")
    fi
  done < "${VERIFY_OUT_FILE}"
elif [[ "${VERIFY_EXIT}" -ne 0 ]]; then
  # F-024 (P2, R6): verify internal error must NOT pass through to PASS/MINOR/MATERIAL.
  # If we cannot run the post-snapshot freshness check, treat the audit as
  # AUDIT_FAILED — orchestrator must not assume "no mutation" from "verify
  # could not run". §4.6 contract: AUDIT_FAILED proposal blocks transition.
  BUNDLE_MUTATION_DETECTED=1
  BUNDLE_MUTATION_FILES+=("(audit_snapshot.py verify failed: exit ${VERIFY_EXIT})")
  printf '[run_codex_audit] error: audit_snapshot verify failed (exit %s); forcing AUDIT_FAILED\n' "${VERIFY_EXIT}" >&2
fi
rm -f "${VERIFY_OUT_FILE}"

# Step 3b: bundle_manifest_sha stays pinned to the PRE-codex value (Step 0b).
# The orchestrator's L3-4 check compares current-state SHAs against the
# manifest written at audit time — updating it post-mutation would silently
# accept a stale audit.

# ---------------------------------------------------------------------------
# Step 3c — write sidecar (atomic). §3.4 / §4.3.
# All timestamps, versions, and bundle context captured here for Layer 3
# anti-fake-audit evidence.
# ---------------------------------------------------------------------------
DURATION_S=$(_duration_seconds "${STARTED_AT}" "${ENDED_AT}")
JSONL_THREAD_ID=$(_extract_jsonl_thread_id "${OUT_DIR}/${run_id}.jsonl")

# Build JSON arrays for primary and supporting deliverables.
# Sources from the SNAPSHOT_JSON_FILE (audit_snapshot.py output) — same shape
# the schema requires: [{path, sha}, ...].
_primary_deliverables_json() {
  python3 -c "
import json, sys
d = json.load(open(sys.argv[1]))
print(json.dumps([{'path': f['path'], 'sha': f['sha']} for f in d['primary_files']]))
" "${SNAPSHOT_JSON_FILE}"
}

_supporting_context_json() {
  python3 -c "
import json, sys
d = json.load(open(sys.argv[1]))
print(json.dumps([{'path': f['path'], 'sha': f['sha']} for f in d['supporting_files']]))
" "${SNAPSHOT_JSON_FILE}"
}

# stdout_path and stderr_path: repo-relative POSIX paths (no leading /, no ..)
# OUT_DIR may be absolute or relative; we normalise to repo-relative by
# stripping the CWD prefix if it matches, or using as-is if already relative.
_repo_relative_out_path() {
  local full="${OUT_DIR}/${run_id}.${1}"
  # If OUT_DIR starts with /, attempt to strip CWD prefix
  if [[ "${full}" == /* ]]; then
    local cwd_prefix="${CWD_VAL}/"
    full="${full#"${cwd_prefix}"}"
  fi
  # Remove leading ./ if present
  full="${full#./}"
  printf '%s' "${full}"
}

STDOUT_PATH=$(_repo_relative_out_path "stdout")
STDERR_PATH=$(_repo_relative_out_path "stderr")

# Optional bundle_id field in sidecar
_bundle_id_sidecar_field=""
if [[ -n "${BUNDLE_ID}" ]]; then
  _bundle_id_sidecar_field="\"bundle_id\":$(_json_escape "${BUNDLE_ID}"),"
fi

_sidecar_json() {
  cat <<EOF
{
  "run_id": $(_json_escape "${run_id}"),
  "codex_cli_version": $(_json_escape "${CODEX_VERSION}"),
  "runner": {
    "hostname": $(_json_escape "${HOSTNAME_VAL}"),
    "cwd": $(_json_escape "${CWD_VAL}"),
    "git_sha": $(_json_escape "${GIT_SHA}"),
    "git_dirty": ${GIT_DIRTY}
  },
  "timing": {
    "started_at": $(_json_escape "${STARTED_AT}"),
    "ended_at": $(_json_escape "${ENDED_AT}"),
    "duration_seconds": ${DURATION_S}
  },
  "process": {
    "exit_code": ${CODEX_EXIT},
    "stdout_path": $(_json_escape "${STDOUT_PATH}"),
    "stderr_path": $(_json_escape "${STDERR_PATH}")
  },
  "stream": {
    "jsonl_thread_id": $(_json_escape "${JSONL_THREAD_ID}")
  },
  "prompt": {
    "audit_template_path": $(_json_escape "${AUDIT_TEMPLATE_PATH}"),
    "audit_template_sha": $(_json_escape "${AUDIT_TEMPLATE_SHA_PRE}"),
    "bundle": {
      ${_bundle_id_sidecar_field}
      "bundle_manifest_sha": $(_json_escape "${BUNDLE_MANIFEST_SHA}"),
      "primary_deliverables": $(_primary_deliverables_json),
      "supporting_context": $(_supporting_context_json)
    }
  }
}
EOF
}

_sidecar_json | _atomic_write "${OUT_DIR}/${run_id}.meta.json"

# ---------------------------------------------------------------------------
# Step 4 — produce verdict file.
# Three triggers force the AUDIT_FAILED branch:
#   (a) codex exited non-zero
#   (b) parse_audit_verdict.py --probe rejects the JSONL
#   (c) bundle mutation detected in Step 3a
# wrapper_exit_code starts as codex's actual exit; AUDIT_FAILED path may
# raise it to 70 when codex itself exited 0 (cases b and c).
# ---------------------------------------------------------------------------
WRAPPER_EXIT_CODE="${CODEX_EXIT}"

# _truncate_failure_reason <string>
# F-008 (§3.1): failure_reason maxLength is 500 per audit_verdict.schema.json,
# and the schema regex rejects multi-line strings (^[^\n\r]+$). Truncate to 497
# chars with ellipsis and strip embedded newlines/carriage-returns.
_truncate_failure_reason() {
  local s="$1"
  # Strip newlines/CRs — schema regex ^[^\n\r]+$ rejects multi-line values
  s=$(printf '%s' "${s}" | tr -d '\n\r')
  if [[ "${#s}" -gt 500 ]]; then
    printf '%s...' "${s:0:497}"
  else
    printf '%s' "${s}"
  fi
}

# Helper: synthesize a failure reason from codex exit code + stderr tail
_synthesize_failure_reason() {
  local exit_code="$1"
  local stderr_path="$2"
  local tail_msg=""
  if [[ -s "${stderr_path}" ]]; then
    # Take last non-empty line as context
    tail_msg=$(grep -v '^[[:space:]]*$' "${stderr_path}" 2>/dev/null | tail -1 || true)
  fi
  local reason=""
  if [[ -n "${tail_msg}" ]]; then
    reason=$(printf 'codex exit %s: %s' "${exit_code}" "${tail_msg}")
  else
    reason=$(printf 'codex exit %s' "${exit_code}")
  fi
  # F-008: apply truncation and newline-strip before returning
  _truncate_failure_reason "${reason}"
}

# Helper: emit an AUDIT_FAILED verdict YAML.
# Reuses ENDED_AT (already captured post-codex) for generated_at to avoid a
# second python3 fork purely for timestamp generation.
_emit_audit_failed_verdict() {
  local failure_reason="$1"
  cat <<EOF
run_id: $(_yaml_escape_oneline "${run_id}")
verdict_status: AUDIT_FAILED
round: ${ROUND}
target_rounds: ${TARGET_ROUNDS}
finding_counts:
  p1: 0
  p2: 0
  p3: 0
findings: []
failure_reason: $(_yaml_escape_oneline "${failure_reason}")
generated_at: $(_yaml_escape_oneline "${ENDED_AT}")
generated_by: 'scripts/run_codex_audit.sh'
generator_version: '1.0.0'
EOF
}

# Helper: parse finding_counts from verdict YAML emitted by parse_audit_verdict.py
_parse_verdict_counts_from_yaml() {
  local verdict_path="$1"
  python3 -c "
import sys, re

content = open(sys.argv[1]).read()

def extract_int(key, text):
    m = re.search(r'^\s*' + key + r'\s*:\s*(\d+)', text, re.MULTILINE)
    return int(m.group(1)) if m else 0

p1 = extract_int('p1', content)
p2 = extract_int('p2', content)
p3 = extract_int('p3', content)

# Extract verdict_status
sm = re.search(r'^\s*verdict_status\s*:\s*(\S+)', content, re.MULTILINE)
status = sm.group(1).strip(\"'\") if sm else 'AUDIT_FAILED'

print('{} {} {} {}'.format(status, p1, p2, p3))
" "${verdict_path}"
}

AUDIT_FAILED_REASON=""

# F-007 (§3.6): capture probe stderr explicitly so the actual parser rejection
# reason (e.g. "no agent_message in stream", "stream contains error event") is
# preserved in AUDIT_FAILED_REASON rather than a hardcoded fallback string.
_probe_stderr=""
_probe_exit=0
_probe_stderr=$(python3 scripts/parse_audit_verdict.py \
  --probe "${OUT_DIR}/${run_id}.jsonl" 2>&1 >/dev/null) \
  || _probe_exit=$?

if [[ "${CODEX_EXIT}" -eq 0 ]] \
   && [[ "${BUNDLE_MUTATION_DETECTED}" -eq 0 ]] \
   && [[ "${_probe_exit}" -eq 0 ]]; then
  # Clean path: codex exited 0, bundle stable, JSONL probe passed.
  # F-003 (§3.6): capture full parser stdout/stderr/exit BEFORE piping to
  # _atomic_write. If full parse fails after probe passed (cross-validation
  # disagreement, malformed finding entry, etc.), fall through to AUDIT_FAILED
  # rather than writing a partial verdict.yaml.tmp and aborting mid-rename.
  _verdict_yaml_content=""
  # F-010 (§3.6) Round 3: eliminate mktemp dependency — use a deterministic path
  # under OUT_DIR so the file is (a) always writable when OUT_DIR is writable and
  # (b) cleaned up automatically by the EXIT trap (_cleanup_partials_on_exit removes
  # "${OUT_DIR}/${run_id}".*.tmp).  Round 2 used mktemp /tmp/... which could fail
  # with EX_CANTCREAT 73 when /tmp is full or permission-denied, aborting the wrapper
  # before AUDIT_FAILED artifacts are written — violating §4.6 invariant E8.
  _full_parse_stderr_file="${OUT_DIR}/${run_id}.parse_stderr.tmp"
  if _verdict_yaml_content=$(python3 scripts/parse_audit_verdict.py \
        --jsonl "${OUT_DIR}/${run_id}.jsonl" \
        --round "${ROUND}" \
        --target-rounds "${TARGET_ROUNDS}" \
        2>"${_full_parse_stderr_file}"); then
    printf '%s' "${_verdict_yaml_content}" | _atomic_write "${OUT_DIR}/${run_id}.verdict.yaml"
    rm -f "${_full_parse_stderr_file}"
  else
    _full_parse_stderr=$(cat "${_full_parse_stderr_file}" 2>/dev/null || true)
    rm -f "${_full_parse_stderr_file}"
    # F-003: full parse failed after probe passed — fall through to AUDIT_FAILED
    # so proposal entry is still written (invariant E8) and orchestrator sees a
    # complete artifact set instead of a missing verdict. F-008 truncation applied.
    AUDIT_FAILED_REASON=$(_truncate_failure_reason \
      "JSONL parse error: ${_full_parse_stderr:-full parse failed after probe passed}")
    _emit_audit_failed_verdict "${AUDIT_FAILED_REASON}" \
      | _atomic_write "${OUT_DIR}/${run_id}.verdict.yaml"
    if [[ "${WRAPPER_EXIT_CODE}" -eq 0 ]]; then
      WRAPPER_EXIT_CODE=70
    fi
  fi
else
  # AUDIT_FAILED path: determine failure reason
  if [[ "${BUNDLE_MUTATION_DETECTED}" -eq 1 ]]; then
    AUDIT_FAILED_REASON=$(_truncate_failure_reason \
      "bundle file(s) mutated during audit run: ${BUNDLE_MUTATION_FILES[*]}")
  elif [[ "${CODEX_EXIT}" -ne 0 ]]; then
    AUDIT_FAILED_REASON=$(_synthesize_failure_reason \
      "${CODEX_EXIT}" "${OUT_DIR}/${run_id}.stderr")
  else
    # F-007: codex exit 0 but --probe rejected the JSONL — use captured stderr
    # for the actual rejection message rather than a hardcoded fallback string.
    AUDIT_FAILED_REASON=$(_truncate_failure_reason \
      "JSONL parse error: ${_probe_stderr:-no parseable agent_message found in JSONL stream}")
  fi

  _emit_audit_failed_verdict "${AUDIT_FAILED_REASON}" \
    | _atomic_write "${OUT_DIR}/${run_id}.verdict.yaml"

  # When codex exited 0 but wrapper rejects (cases b and c), raise to 70
  # so wrapper's process exit always agrees with the AUDIT_FAILED verdict
  # it just wrote (§4.6 contract: exit 0 ↔ PASS/MINOR/MATERIAL only).
  if [[ "${WRAPPER_EXIT_CODE}" -eq 0 ]]; then
    WRAPPER_EXIT_CODE=70
  fi
fi

# ---------------------------------------------------------------------------
# Step 5 — emit proposal entry (LAST write per invariant E8).
# Verdict block mirrors the verdict.yaml just written.
# verified_at and verified_by are NOT set — orchestrator fills them at merge.
# Proposal entries carrying these fields are rejected at §5.6 Path B4
# as Pattern C3 attack surface.
# ---------------------------------------------------------------------------

# Read back the verdict status and finding counts from the just-written YAML
_verdict_info=$(_parse_verdict_counts_from_yaml "${OUT_DIR}/${run_id}.verdict.yaml")
read -r VERDICT_STATUS P1_COUNT P2_COUNT P3_COUNT <<< "${_verdict_info}"

_optional_bundle_id_entry_field=""
if [[ -n "${BUNDLE_ID}" ]]; then
  _optional_bundle_id_entry_field="\"bundle_id\":$(_json_escape "${BUNDLE_ID}"),"
fi

_optional_failure_reason_field=""
if [[ "${VERDICT_STATUS}" = "AUDIT_FAILED" ]]; then
  _optional_failure_reason_field="\"failure_reason\":$(_json_escape "${AUDIT_FAILED_REASON}"),"
fi

_proposal_entry_json() {
  cat <<EOF
{
  "stage": ${STAGE},
  "agent": $(_json_escape "${AGENT}"),
  "deliverable_path": $(_json_escape "${DELIVERABLE}"),
  "deliverable_sha": $(_json_escape "${SHA_DELIVERABLE}"),
  "run_id": $(_json_escape "${run_id}"),
  ${_optional_bundle_id_entry_field}
  "bundle_manifest_sha": $(_json_escape "${BUNDLE_MANIFEST_SHA}"),
  "artifact_paths": {
    "jsonl": $(_json_escape "$(_repo_relative_out_path "jsonl")"),
    "sidecar": $(_json_escape "$(_repo_relative_out_path "meta.json")"),
    "verdict": $(_json_escape "$(_repo_relative_out_path "verdict.yaml")")
  },
  "verdict": {
    "status": $(_json_escape "${VERDICT_STATUS}"),
    ${_optional_failure_reason_field}
    "round": ${ROUND},
    "target_rounds": ${TARGET_ROUNDS},
    "finding_counts": {
      "p1": ${P1_COUNT},
      "p2": ${P2_COUNT},
      "p3": ${P3_COUNT}
    }
  }
}
EOF
}

_proposal_entry_json | _atomic_write "${OUT_DIR}/${run_id}.audit_artifact_entry.json"

# ---------------------------------------------------------------------------
# Step 6 — exit with wrapper_exit_code (§4.6 contract).
# Orchestrator also reads proposal entry's verdict.status; the two signals
# are independently consumed. A zero exit iff PASS/MINOR/MATERIAL.
# ---------------------------------------------------------------------------
printf '[run_codex_audit] run_id=%s verdict=%s exit=%s\n' \
  "${run_id}" "${VERDICT_STATUS}" "${WRAPPER_EXIT_CODE}" >&2

[[ "${WRAPPER_EXIT_CODE}" -eq 0 ]] && exit 0 || exit "${WRAPPER_EXIT_CODE}"
<!-- SOURCE-CONTENT-END -->

<a id="source-scripts-audit-snapshot-py"></a>

## SOURCE: scripts/audit_snapshot.py

<!-- SOURCE-CONTENT-BEGIN bytes=24069 -->
#!/usr/bin/env python3
"""audit_snapshot.py — ARS v3.6.7 Step 6 Phase 6.1 byte-exact snapshot helper.

Reads bundle files (primary deliverable + supporting context + audit template +
optional previous-findings), validates them as text-only (rejects NUL bytes),
computes SHA-256 from in-memory bytes (single read per file — no TOCTOU window),
emits the canonical bundle manifest, and writes a JSON summary on stdout for
the wrapper to consume.

This script REPLACES the Bash-side `_snapshot_file` helper. The Bash version
had three structural issues (codex review rounds 1-5 surfaced these):

  F-004 (P1, 5 rounds partial): Bash command substitution runs the helper in a
    subshell. Variable assignments (e.g., `_LAST_SNAPSHOT_SHA`) made inside the
    subshell don't propagate to the parent. The wrapper saw empty SHAs.

  F-018 (P1): `grep -q $'\\0'` in Bash treats `$'\\0'` as an empty pattern,
    matching every non-empty file. Every text file was rejected as binary.

  F-020 (P1): `$(cat file)` strips trailing newlines and drops NUL bytes.
    Manifest SHA (computed from in-memory content) drifted from `sha256sum file`
    (computed from disk bytes). Step 3a always reported false mutation.

The Python implementation reads bytes verbatim, hashes from those exact bytes,
and emits both manifest and SHAs to the wrapper via JSON — no subshell, no
trailing-newline drift, binary-safe NUL detection. The wrapper consumes the
JSON via `python3 audit_snapshot.py ... | jq` or by reading from a tmp file.

CLI modes:

  --snapshot
    Compute snapshot for a bundle. Writes:
      - <output-dir>/<run_id>.manifest.txt (per spec §3.6)
      - <output-dir>/<run_id>.prompt.txt (rendered audit prompt)
      - JSON summary to stdout: {primary_shas, supporting_shas, template_sha,
        manifest_sha, bundle_files, prompt_path}

  --verify
    Recompute SHAs of bundle files and compare against manifest. Used by Step 3a
    of the wrapper to detect post-snapshot disk mutation. Exits 0 if no
    mutation, exits 1 with mutated paths on stdout otherwise.

Exit codes:
  0   success
  64  EX_USAGE — bad arguments or NUL-containing input
  1   verify mode: mutation detected (paths printed to stdout, one per line)
  2   internal error (file not found, JSON serialization failure, etc.)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def read_bytes_or_die(path: str) -> bytes:
    """Read a file's exact bytes. Exits 2 on missing/unreadable file."""
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        print(f"audit_snapshot: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except PermissionError:
        print(f"audit_snapshot: permission denied: {path}", file=sys.stderr)
        sys.exit(2)


def reject_if_binary(path: str, content: bytes) -> None:
    """Reject NUL-containing input (F-018 closure).

    Phase 6.1 audits are UTF-8 text deliverables (markdown, JSON, YAML).
    Bash command-substitution would silently strip NUL bytes; Python's
    binary-safe `b"\\0" in content` test catches them cleanly.
    """
    if b"\0" in content:
        print(
            f"audit_snapshot: file contains NUL bytes (binary not supported): {path}",
            file=sys.stderr,
        )
        sys.exit(64)


def sha256_hex(content: bytes) -> str:
    """SHA-256 hex digest from in-memory bytes."""
    return hashlib.sha256(content).hexdigest()


def _extract_template_sections(template_str: str, section_numbers: list[int]) -> str:
    """Extract specified Section blocks from the audit template.

    The template uses `## Section N — Title` headers with `---` separators.
    F-023 (P1, R6): we substitute Sections 1/2/4/5 with real round metadata
    above; the template's placeholder versions of those sections must not be
    embedded too, or codex sees `{N}` / `{git_sha}` literals in the prompt.

    F-026 (P2, R7): the LAST extracted section must terminate at the next
    top-level `## ` heading (e.g. `## Worked example`, `## Cross-references`),
    not at end-of-file. Without this guard, Section 7's extraction would pull
    the appendix worked example — which embeds a synthesis_agent 4(f) clause —
    into prompts dispatched for non-synthesis agents, contradicting the real
    Section 4(f) we substituted above.

    PR #78 codex round-1 P1: heading detection must skip headings inside
    fenced code blocks (```/~~~). The v3.7.1 Section 0 Scope Report contains
    a fenced sub-block whose first line starts with `## Codex Audit Round N
    — Scope Report`; without fence-awareness, that line was treated as the
    next H2 boundary and Section 0 was truncated mid-fence.

    Returns concatenated section text (with the leading `## Section N` header
    intact and the appendix excluded).
    """
    import re as _re

    # Mask fenced code blocks (```...``` and ~~~...~~~) with whitespace so
    # ## headings inside them don't count as section boundaries. Length is
    # preserved so match offsets stay aligned with the original string.
    def _mask_fences(s: str) -> str:
        fence_re = _re.compile(
            r"^([ \t]*)(```|~~~)[^\n]*\n.*?^\1\2[ \t]*$",
            _re.DOTALL | _re.MULTILINE,
        )
        def _repl(m: _re.Match[str]) -> str:
            return "".join(" " if ch != "\n" else "\n" for ch in m.group(0))
        return fence_re.sub(_repl, s)

    masked = _mask_fences(template_str)

    # Match either Section heading or any other top-level `## ` heading
    # (e.g. "## Worked example", "## Cross-references"); the latter terminate
    # the last extracted section.
    boundary_re = _re.compile(r"^## (?:Section (\d+)( —|$)|.+)", _re.MULTILINE)
    matches = list(boundary_re.finditer(masked))
    if not matches:
        return template_str  # no headings found — fall back to verbatim

    # Identify which matches are real Section N starts (group(1) populated)
    section_starts: list[tuple[int, int]] = []  # (section_num, match_index)
    for i, m in enumerate(matches):
        if m.group(1) is not None:
            section_starts.append((int(m.group(1)), i))

    requested = set(section_numbers)
    if not requested.issubset({n for n, _ in section_starts}):
        missing = requested - {n for n, _ in section_starts}
        raise ValueError(
            f"audit_snapshot: requested template sections {sorted(missing)} not found "
            f"(template has Sections {sorted({n for n, _ in section_starts})})"
        )

    parts: list[str] = []
    for sec_num, match_idx in section_starts:
        if sec_num not in requested:
            continue
        start = matches[match_idx].start()
        # End at the next `## ` heading of any kind (Section or appendix),
        # not just the next Section. This catches the post-Section-7 appendix.
        end = (
            matches[match_idx + 1].start()
            if match_idx + 1 < len(matches)
            else len(template_str)
        )
        parts.append(template_str[start:end].rstrip() + "\n\n")
    return "".join(parts)


_SECTION_4F_BY_AGENT = {
    "synthesis_agent": (
        "(f) Cross-section consistency check: for every source cited in 2+ "
        "sections of the primary deliverable, verify the source's "
        "characterization is compatible across sections; flag any pair of "
        "sections that pull the source's effect in incompatible directions "
        "(Pattern A1)."
    ),
    "research_architect_agent": (
        "(f) Construct-equivalence test: for every survey item labelled "
        "'reverse-coded', verify it meets the construct-equivalence "
        "definition in `shared/references/psychometric_terminology_glossary.md`."
    ),
    "report_compiler_agent": (
        "(f) Mandatory three-part check: (i) word count = "
        "`len(body.split())` <= publisher cap minus 3-5% buffer per "
        "`shared/references/word_count_conventions.md`; (ii) every entry of "
        "the upstream `protected_hedges` block per "
        "`shared/references/protected_hedging_phrases.md` appears verbatim "
        "in the abstract; (iii) no claim in the abstract is less hedged than "
        "its anchor in the body. Failure of any sub-check is a P1 finding."
    ),
}


def render_prompt(
    audit_template: bytes,
    primary_paths: list[str],
    primary_contents: list[bytes],
    supporting_paths: list[str],
    supporting_contents: list[bytes],
    round_n: int,
    target_rounds: int,
    git_sha: str,
    stage: int,
    agent: str,
    prior_findings: Optional[bytes],
) -> bytes:
    """Render the audit prompt sent to codex stdin.

    The prompt embeds the AT-SNAPSHOT-TIME bytes of every bundle file. Codex
    sees exactly the bytes whose SHA-256 went into the manifest — there is
    no second file read, no TOCTOU window.

    F-023 (P1, R6): the audit template at
    shared/templates/codex_audit_multifile_template.md contains placeholders
    in {curly_braces} that the orchestrator fills before sending to codex
    (Section 1 round metadata, Section 2 git_sha, Section 4(f) bundle-specific
    check). Round 5 redesign initially embedded the template verbatim,
    leaving placeholders unsubstituted — codex would see literal `{N}` in
    the prompt and either omit Section 4(f) entirely or produce an
    unparsable Section 6 verdict. This implementation now does explicit
    bundle-specific substitution and rebuilds Section 1, 2, and 4 around
    real values, while preserving Section 3 / 5 / 6 / 7 verbatim from the
    template (they describe codex's expected output, not the bundle).

    Returns bytes (not str) to preserve binary fidelity.
    """
    section_4f = _SECTION_4F_BY_AGENT.get(
        agent,
        f"(f) Bundle-specific check (no agent-specific clause registered for {agent}; "
        "treat 4(f) as N/A and run only (a)-(e)).",
    )

    if round_n <= 1:
        prior_summary = "none (first round, baseline audit)"
    elif prior_findings is not None:
        prior_summary = (
            "(prior findings attached as supporting context — see file listing "
            "below; verify each carries-forward / closes per (a) and (e))"
        )
    else:
        prior_summary = "(no previous-findings file provided)"

    primary_listing = "\n".join(f"- {p}" for p in primary_paths) or "- (none)"
    supporting_listing = (
        "\n".join(f"- {p}" for p in supporting_paths) if supporting_paths else "- (none)"
    )

    # Extract audit template Sections 0, 3, 6, 7 (verbatim — Section 0 is the
    # v3.7.1 D2 Scope Report block riding verbatim every round per spec §3.2;
    # Sections 3 / 6 / 7 describe codex's expected output / dimensions /
    # anti-fake guard). Sections 1, 2, 4, 5 are rendered below with real
    # values, so we skip the template's placeholder versions to avoid showing
    # codex two copies of the same section (one with placeholders, one
    # substituted) — F-023 closure also requires the placeholder text not
    # appear. Section 0 contains a `<N_total>` etc. placeholder set that codex
    # is expected to fill from bundle inventory at audit time, so it rides
    # verbatim alongside Sections 3 / 6 / 7 (codex round-1 PR #78 P1 closure).
    template_str = audit_template.decode("utf-8", errors="replace")
    section_0 = _extract_template_sections(template_str, [0])
    section_3_to_7 = _extract_template_sections(template_str, [3, 6, 7])

    rendered_intro = (
        f"# ARS v3.6.7 cross-model audit — round {round_n} of {target_rounds}\n"
        f"# Stage: {stage} | Agent: {agent}\n"
        f"# Git SHA at audit start: {git_sha}\n\n"
        f"{section_0}"
        f"## Section 1 — Round metadata\n\n"
        f"Audit round: {round_n} of {target_rounds}\n"
        f"Previous rounds: {prior_summary}\n"
        f"Bundle scope: Stage {stage} deliverable for {agent}\n\n"
        f"## Section 2 — Bundle inventory\n\n"
        f"Authoritative context (commit {git_sha}):\n\n"
        f"Primary deliverables (audit target):\n{primary_listing}\n\n"
        f"Supporting context (do not audit; reference only):\n{supporting_listing}\n\n"
        f"## Section 4 — Round {round_n} job\n\n"
        f"(a) Verify each round-{round_n - 1} finding closed correctly. List by ID.\n"
        f"(b) Audit for new issues introduced by round-{round_n - 1} corrections (cascade audit).\n"
        f"(c) Run the 7 audit dimensions (§3.1-§3.7) plus the bundle-specific Section 4(f) check on the primary deliverables. Report each finding with the dimension or `4(f)` that surfaced it.\n"
        f"(d) Anchoring-bias residual check on closed findings.\n"
        f"(e) PARTIAL-vs-CLOSED check.\n"
        f"{section_4f}\n\n"
        f"## Section 5 — Convergence target\n\n"
        f"Convergence target: ZERO findings of ANY severity in one round.\n\n"
    )

    parts: list[bytes] = []
    parts.append(rendered_intro.encode("utf-8"))
    parts.append(section_3_to_7.encode("utf-8"))
    parts.append(b"\n\n## Primary deliverables (audit target)\n\n")
    for path, content in zip(primary_paths, primary_contents):
        parts.append(f"--- PRIMARY: {path} ---\n".encode("utf-8"))
        parts.append(content)
        parts.append(b"\n")
    if supporting_paths:
        parts.append(b"\n## Supporting context (reference only)\n\n")
        for path, content in zip(supporting_paths, supporting_contents):
            parts.append(f"--- SUPPORTING: {path} ---\n".encode("utf-8"))
            parts.append(content)
            parts.append(b"\n")
    return b"".join(parts)


def write_manifest(
    out_path: str,
    primary_shas: list[tuple[str, str]],
    supporting_shas: list[tuple[str, str]],
    audit_template_path: str,
    audit_template_sha: str,
) -> str:
    """Write the canonical bundle manifest per §3.6.

    Format: <role>:<repo-relative-path>:<sha256-hex>, one line per file,
    sorted by (role, path) via the equivalent of `LC_ALL=C sort`.
    Returns the manifest's own SHA-256 (== `bundle_manifest_sha`).
    """
    lines: list[str] = []
    for path, sha in primary_shas:
        lines.append(f"primary:{path}:{sha}")
    for path, sha in supporting_shas:
        lines.append(f"supporting:{path}:{sha}")
    lines.append(f"template:{audit_template_path}:{audit_template_sha}")
    lines.sort()
    manifest_text = "\n".join(lines) + "\n"
    manifest_bytes = manifest_text.encode("utf-8")
    try:
        with open(out_path, "wb") as f:
            f.write(manifest_bytes)
    except OSError as e:
        print(f"audit_snapshot: manifest write failed: {e}", file=sys.stderr)
        sys.exit(2)
    return sha256_hex(manifest_bytes)


def write_prompt(out_path: str, prompt_bytes: bytes) -> None:
    """Write the rendered prompt to a file the wrapper feeds to codex stdin."""
    try:
        with open(out_path, "wb") as f:
            f.write(prompt_bytes)
    except OSError as e:
        print(f"audit_snapshot: prompt write failed: {e}", file=sys.stderr)
        sys.exit(2)


def dedupe_preserving_order(items: list[str]) -> list[str]:
    """Remove duplicates while preserving first occurrence order (F-021)."""
    seen: set[str] = set()
    out: list[str] = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


# ---------------------------------------------------------------------------
# CLI modes
# ---------------------------------------------------------------------------


def cmd_snapshot(args: argparse.Namespace) -> int:
    """Snapshot bundle files, write manifest + prompt, emit JSON summary."""
    primary = list(args.primary or [])
    supporting = list(args.supporting or [])
    if args.previous_findings:
        # Inject --previous-findings into supporting (preserves §3.6 3-role enum).
        # Dedup happens AFTER normalization (which the wrapper does upstream).
        supporting.append(args.previous_findings)
    supporting = dedupe_preserving_order(supporting)

    if not primary:
        print("audit_snapshot: --primary is required", file=sys.stderr)
        return 64
    if not args.audit_template:
        print("audit_snapshot: --audit-template is required", file=sys.stderr)
        return 64
    if not args.output_dir or not args.run_id:
        print("audit_snapshot: --output-dir and --run-id are required", file=sys.stderr)
        return 64

    audit_template_bytes = read_bytes_or_die(args.audit_template)
    reject_if_binary(args.audit_template, audit_template_bytes)
    audit_template_sha = sha256_hex(audit_template_bytes)

    primary_contents: list[bytes] = []
    primary_shas: list[tuple[str, str]] = []
    for p in primary:
        content = read_bytes_or_die(p)
        reject_if_binary(p, content)
        primary_contents.append(content)
        primary_shas.append((p, sha256_hex(content)))

    supporting_contents: list[bytes] = []
    supporting_shas: list[tuple[str, str]] = []
    for s in supporting:
        content = read_bytes_or_die(s)
        reject_if_binary(s, content)
        supporting_contents.append(content)
        supporting_shas.append((s, sha256_hex(content)))

    # F-029 (P3, R8): render the prompt BEFORE writing manifest/prompt to disk.
    # If _extract_template_sections raises ValueError (requested sections not
    # found in template), no partial artifact is left in --output-dir.
    # F-023 (P1, R6): pass stage/agent/prior_findings so render_prompt can
    # substitute audit-template placeholders and select the agent-specific
    # Section 4(f) clause.
    prior_findings_bytes: Optional[bytes] = None
    if args.previous_findings:
        # PREV_FINDINGS was just snapshotted as part of supporting; locate its content.
        for path, content in zip([s for s, _ in supporting_shas], supporting_contents):
            if path == args.previous_findings:
                prior_findings_bytes = content
                break

    try:
        prompt_bytes = render_prompt(
            audit_template_bytes,
            [p for p, _ in primary_shas],
            primary_contents,
            [s for s, _ in supporting_shas],
            supporting_contents,
            args.round,
            args.target_rounds,
            args.git_sha or "unknown",
            args.stage,
            args.agent,
            prior_findings_bytes,
        )
    except ValueError as e:
        # F-029: clean exit 64 with no partial artifact left behind.
        print(f"audit_snapshot: prompt render failed: {e}", file=sys.stderr)
        return 64

    # Now safe to write — render succeeded, no traceback path.
    manifest_path = os.path.join(args.output_dir, f"{args.run_id}.manifest.txt")
    bundle_manifest_sha = write_manifest(
        manifest_path,
        primary_shas,
        supporting_shas,
        args.audit_template,
        audit_template_sha,
    )
    prompt_path = os.path.join(args.output_dir, f"{args.run_id}.prompt.txt")
    write_prompt(prompt_path, prompt_bytes)

    summary = {
        "manifest_path": manifest_path,
        "manifest_sha": bundle_manifest_sha,
        "prompt_path": prompt_path,
        "audit_template_path": args.audit_template,
        "audit_template_sha": audit_template_sha,
        "primary_files": [{"path": p, "sha": sha} for p, sha in primary_shas],
        "supporting_files": [{"path": s, "sha": sha} for s, sha in supporting_shas],
    }
    json.dump(summary, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    """Verify bundle files against the snapshot manifest.

    Reads the manifest file written by --snapshot mode, recomputes each
    referenced file's SHA-256 from current disk content, and reports any
    mismatches. Used by the wrapper's Step 3a (post-codex mutation detection).
    """
    if not args.manifest:
        print("audit_snapshot: --manifest is required for --verify", file=sys.stderr)
        return 64

    try:
        with open(args.manifest, encoding="utf-8") as f:
            manifest_text = f.read()
    except OSError as e:
        print(f"audit_snapshot: manifest read failed: {e}", file=sys.stderr)
        return 2

    mutated_paths: list[str] = []
    for line in manifest_text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Format: <role>:<path>:<sha>
        # The path may contain colons (POSIX paths can include them, though
        # rare); split into 3 parts maximum from the left (role + path + sha)
        # but the SHA is always the LAST 64 hex chars after a colon.
        if ":" not in line:
            continue
        # Find the SHA suffix: last colon, then 64 hex chars.
        if len(line) < 65 or line[-65] != ":":
            continue
        path_with_role = line[:-65]
        expected_sha = line[-64:]
        # Split role:path
        role_sep = path_with_role.find(":")
        if role_sep == -1:
            continue
        # role = path_with_role[:role_sep]  # not needed for verify
        path = path_with_role[role_sep + 1 :]

        # Recompute SHA from current disk content
        try:
            with open(path, "rb") as f:
                actual_sha = sha256_hex(f.read())
        except FileNotFoundError:
            mutated_paths.append(path)
            continue
        if actual_sha != expected_sha:
            mutated_paths.append(path)

    if mutated_paths:
        for p in mutated_paths:
            print(p)
        return 1
    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="ARS v3.6.7 audit bundle snapshot helper. "
        "Modes: --snapshot (initial) or --verify (post-codex)."
    )
    sub = p.add_subparsers(dest="mode", required=True)

    snap = sub.add_parser("snapshot", help="Snapshot bundle, write manifest + prompt")
    snap.add_argument("--primary", action="append", required=True, help="Primary deliverable path (repeatable)")
    snap.add_argument("--supporting", action="append", default=[], help="Supporting context path (repeatable)")
    snap.add_argument("--previous-findings", help="Optional --previous-findings path (auto-injected into supporting with dedup)")
    snap.add_argument("--audit-template", required=True, help="Audit template path (single)")
    snap.add_argument("--output-dir", required=True, help="Where to write manifest.txt and prompt.txt")
    snap.add_argument("--run-id", required=True, help="Audit run identifier")
    snap.add_argument("--round", type=int, required=True, help="Current audit round")
    snap.add_argument("--target-rounds", type=int, required=True, help="Total target rounds")
    snap.add_argument("--git-sha", help="Repo HEAD short SHA (informational, embedded in prompt)")
    snap.add_argument("--stage", type=int, required=True, help="Stage transition (1-6) the audit gates")
    snap.add_argument(
        "--agent",
        required=True,
        choices=["synthesis_agent", "research_architect_agent", "report_compiler_agent"],
        help="Which v3.6.7 downstream agent produced the deliverable (selects Section 4(f) clause)",
    )

    ver = sub.add_parser("verify", help="Verify bundle files against snapshot manifest")
    ver.add_argument("--manifest", required=True, help="Path to <run_id>.manifest.txt")

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.mode == "snapshot":
        return cmd_snapshot(args)
    elif args.mode == "verify":
        return cmd_verify(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
<!-- SOURCE-CONTENT-END -->

<a id="source-scripts-parse-audit-verdict-py"></a>

## SOURCE: scripts/parse_audit_verdict.py

<!-- SOURCE-CONTENT-BEGIN bytes=32851 -->
#!/usr/bin/env python3
"""parse_audit_verdict.py — ARS v3.6.7 Step 6 Phase 6.1

Reads a codex CLI 0.125+ --json JSONL event stream and converts the structured
Section 6 verdict text (from the LAST agent_message item.completed event) into
a <run_id>.verdict.yaml file.

Two CLI modes:
  --probe <jsonl>                  Validate only; exit 0 on success, non-zero on failure.
  --jsonl <jsonl> --round N --target-rounds M  Parse + emit YAML to stdout.

Exit codes:
  0   success (probe passed OR full parse emitted YAML)
  non-zero  parse failure (reason on stderr, one line)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

GENERATED_BY = "scripts/run_codex_audit.sh"
GENERATOR_VERSION = "1.0.0"

# run_id filename pattern: YYYY-MM-DDTHH-MM-SSZ-XXXX  (hyphens, not colons)
RUN_ID_RE = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}Z-[0-9a-f]{4}$"
)

# F-019 (§3.3): canonical UUID regex for thread.started.thread_id validation.
# codex 0.125+ always emits a lowercase-hex UUID in this exact format.
# A non-matching value indicates a malformed or forged stream.
_THREAD_ID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)

# Valid dimension values (string enum per audit_verdict.schema.json)
VALID_DIMENSIONS = {"3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "4(f)"}

# ---------------------------------------------------------------------------
# JSONL parsing
# ---------------------------------------------------------------------------


def load_events(jsonl_path: str) -> list[dict]:
    """Read all JSONL rows from the given file path.

    Returns a list of parsed dicts.  Raises ParseError on file-level failures.
    """
    if not os.path.exists(jsonl_path):
        raise ParseError(f"jsonl file not found: {jsonl_path}")
    with open(jsonl_path, encoding="utf-8") as fh:
        raw = fh.read().strip()
    if not raw:
        raise ParseError(f"jsonl file is empty: {jsonl_path}")

    events: list[dict] = []
    for lineno, line in enumerate(raw.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ParseError(f"invalid JSON at row {lineno}: {exc}") from exc
        # F-027 (P3, R7): each row must be a JSON object so .get/[] work later.
        if not isinstance(row, dict):
            raise ParseError(
                f"jsonl row {lineno} is not an object: {type(row).__name__}"
            )
        events.append(row)
    return events


def validate_stream_shape(events: list[dict]) -> None:
    """Validate that the JSONL event stream has the expected clean-run shape.

    F-002 (§3.6) — Round 3 fix: anchors checks 6, 7, 8 on the FIRST
    turn.completed event (not the last).  Rounds 1-2 used last_turn_completed_idx
    throughout, which allowed the multi-turn.completed forgery:

        thread.started → turn.started → real_agent_message → turn.completed_1
            → forged_agent_message → turn.completed_2

    Under the Round 2 logic: last_turn_completed_idx pointed to turn.completed_2,
    so trailing = [] (nothing after TC_2, check 7 passed), and TC_2 < TC_2 was
    False (check 6 passed), but extract_verdict_text returned the forged message.

    Fix: locate the FIRST turn.completed.  Per §3.3 a clean run has exactly ONE
    turn.completed, at the end.  Check 7 (no trailing events after first TC) rejects
    any second TC as an illegal trailing event, and check 6 verifies the first TC
    appears after the last agent_message.  Both checks together enforce exactly-one-TC.

    Per §3.3 canonical no-tool run sequence:
      thread.started → turn.started → item.completed(agent_message) → turn.completed

    Checks:
      1. Exactly one thread.started event (multiple → forgery surface).
      2. First event is thread.started.
      3. Second event is turn.started (per §3.3 canonical sequence).
      4. No error event anywhere in the stream.
      5. Stream contains at least one agent_message.
      6. FIRST turn.completed appears after the last agent_message.
      7. No events after the FIRST turn.completed (clean run ends with first TC;
         any trailing event — including a second TC — is a forgery indicator).
      8. first turn.completed.usage.input_tokens > 0 (real codex always consumes input).
      9. thread.started.thread_id matches canonical UUID regex (F-019 §3.3).
     10. All four turn.completed.usage fields present, integers, >= 0 (F-019 §3.3).

    Raises ParseError if any check fails. Probe rejection cascades into the
    wrapper's AUDIT_FAILED branch per §4.6 case (b).
    """
    if not events:
        raise ParseError("stream is empty")

    # Check 1: exactly one thread.started event (§3.3: thread_id emitted ONCE)
    thread_started_count = sum(1 for ev in events if ev.get("type") == "thread.started")
    if thread_started_count == 0:
        raise ParseError(
            f"stream missing thread.started event (got first: {events[0].get('type')!r})"
        )
    if thread_started_count > 1:
        raise ParseError(
            f"stream has {thread_started_count} thread.started events; expected exactly 1"
        )

    # Check 2: first event is thread.started
    if events[0].get("type") != "thread.started":
        raise ParseError(
            f"stream first event is not thread.started (got: {events[0].get('type')!r})"
        )

    # Check 3: second event is turn.started (per §3.3 canonical sequence)
    if len(events) < 2 or events[1].get("type") != "turn.started":
        got = events[1].get("type") if len(events) >= 2 else "(stream too short)"
        raise ParseError(
            f"stream second event is not turn.started (got: {got!r})"
        )

    # Check 4: no error event anywhere in the stream
    if any(ev.get("type") == "error" for ev in events):
        raise ParseError("stream contains error event (codex was killed or errored mid-run)")

    # Locate the FIRST turn.completed (F-002 Round 3: must use FIRST, not last).
    # Per §3.3 a clean run has exactly one turn.completed at the stream end.
    # Using last_turn_completed_idx (Rounds 1-2) allowed a forged second TC to
    # make trailing[] appear empty while hiding a forged agent_message between TC_1
    # and TC_2.  Anchoring on FIRST TC collapses that window.
    first_turn_completed_idx = -1
    for idx, ev in enumerate(events):
        if ev.get("type") == "turn.completed":
            first_turn_completed_idx = idx
            break  # stop at FIRST occurrence

    # Locate the last agent_message (verdict-bearing event per §3.3 contract).
    # F-027 (P3, R7) + F-030 (P3, R8/R9): malformed `item` on item.started/
    # item.completed events is rejected outright. Per spec §3.3 schema, `item`
    # is an object with required `id` (non-empty string) + `type` (non-empty
    # string); object-shaped rows missing those keys are still malformed.
    last_agent_msg_idx = -1
    for idx, ev in enumerate(events):
        ev_type = ev.get("type")
        if ev_type not in ("item.completed", "item.started"):
            continue
        item = ev.get("item")
        if not isinstance(item, dict):
            raise ParseError(
                f"event {idx} ({ev_type}) has malformed item field: "
                f"{type(item).__name__}"
            )
        # F-030 R9 closure: enforce required item.id + item.type as non-empty strings.
        item_id = item.get("id")
        item_type = item.get("type")
        if not isinstance(item_id, str) or not item_id:
            raise ParseError(
                f"event {idx} ({ev_type}) item.id is not a non-empty string: {item_id!r}"
            )
        if not isinstance(item_type, str) or not item_type:
            raise ParseError(
                f"event {idx} ({ev_type}) item.type is not a non-empty string: {item_type!r}"
            )
        if ev_type == "item.completed" and item_type == "agent_message":
            last_agent_msg_idx = idx

    # Check 5: at least one agent_message present
    if last_agent_msg_idx == -1:
        raise ParseError("no agent_message in stream")

    # Check 6: FIRST turn.completed must exist and appear after the last agent_message.
    # (F-002 R3: anchored on first_turn_completed_idx, not last_turn_completed_idx)
    if first_turn_completed_idx == -1:
        raise ParseError(
            "stream missing turn.completed event (codex was killed mid-run)"
        )
    if first_turn_completed_idx < last_agent_msg_idx:
        raise ParseError(
            "turn.completed appears before last agent_message "
            "(stream truncated or forged; first turn.completed must follow all agent messages)"
        )

    # Check 7: NO events after the FIRST turn.completed.
    # (F-002 R3: anchored on first_turn_completed_idx, not last_turn_completed_idx)
    # This implicitly enforces exactly-one-TC: any second turn.completed would appear
    # here as a trailing event and be rejected.  Per §3.3 §line 284, a clean codex run
    # always ends at the single turn.completed event.
    trailing = events[first_turn_completed_idx + 1:]
    if trailing:
        trailing_types = [ev.get("type") for ev in trailing]
        raise ParseError(
            f"unexpected event(s) after turn.completed: {trailing_types!r} "
            f"(stream must end at first turn.completed per §3.3)"
        )

    # Check 9 (F-019 §3.3): thread_id must match canonical UUID format.
    # codex 0.125+ always emits a lowercase-hex UUID on the thread.started event.
    # A non-canonical value indicates a malformed or forged stream header.
    # F-025 (P3, R6): thread_id must be a string before regex match.
    # `events[0].get("thread_id", "")` returns None / list / int verbatim if
    # the key holds those types — feeding non-string to _THREAD_ID_RE.match
    # raises TypeError. Explicit type guard turns it into a clean ParseError.
    thread_id = events[0].get("thread_id")
    if not isinstance(thread_id, str):
        raise ParseError(
            f"thread.started.thread_id is not a string: {type(thread_id).__name__}"
        )
    if not _THREAD_ID_RE.match(thread_id):
        raise ParseError(
            f"thread.started.thread_id is not canonical UUID: {thread_id!r}"
        )

    # Check 10 (F-019 §3.3): all four usage fields must be present, integers,
    # and non-negative.  Type validation runs FIRST (F-022 §3.3) so non-int
    # values (e.g., "1" as string) raise a one-line ParseError instead of an
    # unhandled traceback in the input_tokens > 0 comparison below.
    turn_completed = events[first_turn_completed_idx]
    # F-025 (P3, R6): usage must be a dict before `in` / index operations.
    # JSONL with `usage: null` or `usage: []` would otherwise raise TypeError.
    usage = turn_completed.get("usage")
    if not isinstance(usage, dict):
        raise ParseError(
            f"turn.completed.usage is not an object: {type(usage).__name__}"
        )
    _USAGE_FIELDS = (
        "input_tokens",
        "cached_input_tokens",
        "output_tokens",
        "reasoning_output_tokens",
    )
    for fld in _USAGE_FIELDS:
        if fld not in usage:
            raise ParseError(f"turn.completed.usage missing field: {fld!r}")
        if not isinstance(usage[fld], int) or isinstance(usage[fld], bool):
            raise ParseError(
                f"turn.completed.usage.{fld} is not int: {usage[fld]!r}"
            )
        if usage[fld] < 0:
            raise ParseError(
                f"turn.completed.usage.{fld} is negative: {usage[fld]}"
            )

    # Check 8: first turn.completed.usage.input_tokens > 0 (§3.3 line 277, Q3 line 63).
    # Real codex always consumes input; zero → forgery indicator.
    # Runs AFTER Check 10 so input_tokens is guaranteed-int by this point.
    if usage["input_tokens"] <= 0:
        raise ParseError(
            f"turn.completed.usage.input_tokens is {usage['input_tokens']} "
            "(real codex runs always consume input tokens; zero indicates forgery)"
        )


def extract_verdict_text(events: list[dict]) -> str:
    """Return the text of the LAST item.completed agent_message event.

    Per §3.3 contract: tool-using runs emit intermediate agent_message events
    between tool calls; the verdict-bearing event is always the LAST one.

    F-027 (P3, R7): each event's `item` field must be a dict before .get;
    `item.text` for agent_message must be a non-empty string. Malformed types
    raise clean ParseError instead of TypeError tracebacks.
    """
    agent_messages: list[dict] = []
    for idx, row in enumerate(events):
        if row.get("type") != "item.completed":
            continue
        item = row.get("item")
        if not isinstance(item, dict):
            raise ParseError(
                f"event {idx} (item.completed) has malformed item field: "
                f"{type(item).__name__}"
            )
        if item.get("type") != "agent_message":
            continue
        agent_messages.append(row)
    if not agent_messages:
        raise ParseError("no agent_message in stream")
    last_item = agent_messages[-1].get("item", {})
    verdict_text = last_item.get("text")
    if not isinstance(verdict_text, str) or not verdict_text:
        raise ParseError(
            f"agent_message.item.text is not a non-empty string: "
            f"{type(verdict_text).__name__}"
        )
    return verdict_text


# ---------------------------------------------------------------------------
# Section 6 text parsing
# ---------------------------------------------------------------------------

# Summary line patterns (two canonical forms per audit template Section 6):
#
#   Form A (findings present):
#     "Round N: P1×n1 / P2×n2 / P3×n3 (M total)"
#   Form B (zero findings):
#     "Round N: 0 findings of any severity. Convergence reached."
#
# Both forms may be preceded by "Previous rounds: Round 1: ... ; all P1 ..." on
# the same or adjacent line — we anchor on the ROUND value passed via CLI to
# pick the authoritative summary line rather than a "previous rounds" recap.

# Matches: Round N: P1×n1 / P2×n2 / P3×n3 (M total)
#
# F-011 (§3.6) Round 2 fixes:
#   1. (M total) parenthetical is now MANDATORY (was optional "(?:...)?").
#      A summary line without the parenthetical is malformed per audit template
#      Section 6 line 160 and should cascade to "no parseable Section 6 summary"
#      → AUDIT_FAILED rather than silently accepting an unchecked total.
#   2. Anchored to start-of-line (^) and end-of-line ($) with re.MULTILINE to
#      prevent partial matches on lines containing "Round N:" as a substring
#      (e.g., finding entries that restate the round number in their description).
_SUMMARY_A = re.compile(
    r"^\s*Round\s+(\d+)\s*:\s*P1[×x×](\d+)\s*/\s*P2[×x×](\d+)\s*/\s*P3[×x×](\d+)"
    r"\s*\((\d+)\s*total\)\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# Matches: Round N: 0 findings of any severity. Convergence reached.
# F-011: anchored similarly for consistency — avoids substring hits in
# "Previous rounds: Round 1: 0 findings ..." recap lines.
_SUMMARY_B = re.compile(
    r"^\s*Round\s+(\d+)\s*:\s*0\s+findings\s+of\s+any\s+severity[.,]?\s*Convergence\s+reached.*$",
    re.IGNORECASE | re.MULTILINE,
)

# Finding entry pattern (tolerant of formatting variation):
#
# Codex emits lines like:
#   1. **F-007** P3 §3.7 chapter_4/synthesis.md:482 — description. Fix: fix text.
#   2. **F-001** P1 3.2 path/file.md:10 - description here. Fix: suggested fix.
#
# Groups: (list_num, finding_id, severity, dimension, file, line, description, fix_text)
#
# Strategy:
#   - Finding ID: **F-NNN** (bold markdown) or bare F-NNN
#   - Severity: P1 / P2 / P3 (standalone word)
#   - Dimension: §3.1–§3.7 (with or without § prefix) or 4(f)
#   - file:line anchor (greedy non-space path, colon, integer)
#   - Description and Fix separated by "Fix:" label (case-insensitive)
#
# We use a two-pass approach: first match the structural header (id/sev/dim/file:line),
# then extract description + fix from the tail.

_FINDING_HEADER = re.compile(
    r"^\s*\d+\.\s+"                          # numbered list item: "1. "
    r"\*{0,2}(F-[0-9]{3,})\*{0,2}"          # finding ID: **F-007** or F-007
    r"\s+"
    r"(P[123])"                              # severity: P1 P2 P3
    r"\s+"
    r"(?:§)?(3\.[1-7]|4\(f\))"              # dimension: §3.x or 4(f) (with or without §)
    r"\s+"
    r"([^\s:]+)"                             # file path (no spaces, stops before colon)
    r":([0-9]+)"                             # :line
    r"\s*[-—–]+\s*"                          # separator: — or - or –
    r"(.+)",                                 # rest of line (description + fix)
    re.IGNORECASE,
)

# Fix label separator within the rest-of-line tail
# e.g.: "deictic phrase. Fix: replace with ..."
#       "description here. Fix: suggested fix here."
_FIX_SEPARATOR = re.compile(r"\.\s*Fix\s*:\s*", re.IGNORECASE)


def _parse_dimension(raw: str) -> str:
    """Normalize raw dimension string to the schema enum value."""
    d = raw.lstrip("§").strip()
    if d in VALID_DIMENSIONS:
        return d
    raise ParseError(f"malformed finding entry: unknown dimension '{raw}'")


def _parse_finding_line(line: str) -> Optional[dict]:
    """Attempt to parse one numbered finding line.  Returns None if no match."""
    m = _FINDING_HEADER.match(line)
    if not m:
        return None

    finding_id, severity, dimension_raw, file_path, line_num, tail = m.groups()
    finding_id = finding_id.upper()
    severity = severity.upper()
    dimension = _parse_dimension(dimension_raw)
    line_int = int(line_num)

    # Split tail into description and suggested_fix at ". Fix: "
    fix_parts = _FIX_SEPARATOR.split(tail, maxsplit=1)
    if len(fix_parts) == 2:
        description = fix_parts[0].strip().rstrip(".")
        suggested_fix = fix_parts[1].strip().rstrip(".")
    else:
        # No "Fix:" separator found — description consumes entire tail,
        # suggested_fix is missing → malformed entry.
        raise ParseError(
            f"malformed finding entry: no 'Fix:' separator in line: {line!r}"
        )

    if not description:
        raise ParseError(f"malformed finding entry: empty description for {finding_id}")
    if not suggested_fix:
        raise ParseError(
            f"malformed finding entry: empty suggested_fix for {finding_id}"
        )

    return {
        "id": finding_id,
        "severity": severity,
        "dimension": dimension,
        "file": file_path,
        "line": line_int,
        "description": description,
        "suggested_fix": suggested_fix,
    }


def parse_section6(
    text: str,
    current_round: Optional[int] = None,
) -> tuple[dict, list[dict]]:
    """Parse Section 6 verdict text.

    Returns (finding_counts, findings_list) where:
      finding_counts  = {"p1": int, "p2": int, "p3": int}
      findings_list   = list of finding dicts

    Raises ParseError if no authoritative summary line is found or if
    finding_counts disagrees with the parsed findings list.

    current_round: when provided, use to locate the authoritative summary line
    (avoiding "Previous rounds: Round 1: …" recaps).  When None (probe mode),
    accept the last parseable summary line.
    """
    lines = text.splitlines()

    # ---- Step 1: locate the authoritative summary line -----
    # We scan ALL lines and collect all summary-line matches.
    # If current_round is known, we require the summary to match that round.
    # If not (probe), we accept any match and take the last one.

    summary_counts: Optional[tuple[int, int, int]] = None  # (p1, p2, p3)
    # F-011: track the authoritative summary line's text for last-line check
    _authoritative_summary_line: Optional[str] = None

    for line in lines:
        # Try Form B first (zero-findings convergence line)
        mb = _SUMMARY_B.search(line)
        if mb:
            r = int(mb.group(1))
            if current_round is None or r == current_round:
                summary_counts = (0, 0, 0)
                _authoritative_summary_line = line.strip()
                if current_round is not None:
                    break
            continue

        # Try Form A (P1×n / P2×n / P3×n)
        ma = _SUMMARY_A.search(line)
        if ma:
            r, n1, n2, n3 = (
                int(ma.group(1)),
                int(ma.group(2)),
                int(ma.group(3)),
                int(ma.group(4)),
            )
            if current_round is None or r == current_round:
                # F-011: cross-validate (N total) parenthetical when present.
                # "Round 2: P1×0 / P2×3 / P3×1 (5 total)" should reject because
                # 0+3+1=4 ≠ 5. group(5) is None when parenthetical is absent.
                total_group = ma.group(5)
                if total_group is not None:
                    total_claimed = int(total_group)
                    total_computed = n1 + n2 + n3
                    if total_claimed != total_computed:
                        raise ParseError(
                            f"summary line total {total_claimed} disagrees with "
                            f"bucket sum {total_computed} (P1×{n1}+P2×{n2}+P3×{n3})"
                        )
                summary_counts = (n1, n2, n3)
                _authoritative_summary_line = line.strip()
                if current_round is not None:
                    break

    if summary_counts is None:
        raise ParseError("no parseable Section 6 summary")

    # F-011: require the authoritative summary line to be the LAST non-empty
    # line of the verdict text. Audit template Section 6 format puts the summary
    # at the end; an interior summary line indicates a malformed or shadowed
    # verdict (e.g. "Previous rounds" recap in the wrong position).
    non_empty_lines = [ln.strip() for ln in lines if ln.strip()]
    if non_empty_lines and _authoritative_summary_line is not None:
        last_nonempty = non_empty_lines[-1]
        # The authoritative summary line must match the last non-empty line.
        # We do a substring check because the line may be embedded in a longer
        # line (e.g. with markdown emphasis markers around it).
        if _authoritative_summary_line not in last_nonempty and last_nonempty not in _authoritative_summary_line:
            raise ParseError(
                "summary line is not the last non-empty line of the verdict text "
                "(found interior summary; expected it at the end per audit template Section 6)"
            )

    # ---- Step 2: parse individual finding entries ----
    findings: list[dict] = []
    for line in lines:
        # Skip summary lines to avoid spurious matches
        if _SUMMARY_A.search(line) or _SUMMARY_B.search(line):
            continue
        result = _parse_finding_line(line)
        if result is not None:
            findings.append(result)

    # ---- Step 3: cross-validate counts vs parsed findings ----
    p1_exp, p2_exp, p3_exp = summary_counts
    p1_got = sum(1 for f in findings if f["severity"] == "P1")
    p2_got = sum(1 for f in findings if f["severity"] == "P2")
    p3_got = sum(1 for f in findings if f["severity"] == "P3")

    if (p1_got, p2_got, p3_got) != (p1_exp, p2_exp, p3_exp):
        raise ParseError(
            f"finding_counts disagrees with findings[] "
            f"(summary: P1×{p1_exp}/P2×{p2_exp}/P3×{p3_exp}, "
            f"parsed: P1×{p1_got}/P2×{p2_got}/P3×{p3_got})"
        )

    finding_counts = {"p1": p1_exp, "p2": p2_exp, "p3": p3_exp}
    return finding_counts, findings


# ---------------------------------------------------------------------------
# Status classification (§3.2 cross-field rule)
# ---------------------------------------------------------------------------


def classify_status(finding_counts: dict) -> str:
    """Derive verdict_status from finding_counts per spec §3.2 cross-field rules.

    F-012 (§3.2): original implementation omitted the p3 upper bound, classifying
    p3=4 as MINOR instead of MATERIAL.  Per spec lines 231-233:

      PASS:     p1 == 0 AND p2 == 0 AND p3 == 0
      MINOR:    p1 == 0 AND p2 == 0 AND 1 <= p3 <= 3
      MATERIAL: p1 > 0 OR p2 > 0 OR p3 > 3

    Contract-critical: a 4-P3-finding audit mis-classified as MINOR lets the
    orchestrator escalate to user instead of BLOCKing — silent severity downgrade.
    """
    p1, p2, p3 = finding_counts["p1"], finding_counts["p2"], finding_counts["p3"]
    if p1 == 0 and p2 == 0 and p3 == 0:
        return "PASS"
    if p1 == 0 and p2 == 0 and 1 <= p3 <= 3:
        return "MINOR"
    return "MATERIAL"


# ---------------------------------------------------------------------------
# YAML serialisation (hand-rolled — standard library only)
# ---------------------------------------------------------------------------


def _yaml_str(value: str) -> str:
    """Double-quote a string value to safely embed colons, brackets, and backslashes."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_verdict_yaml(
    run_id: str,
    verdict_status: str,
    round_num: int,
    target_rounds: int,
    finding_counts: dict,
    findings: list[dict],
    generated_at: str,
) -> str:
    """Serialize verdict fields to YAML string.

    Hand-rolled to avoid PyYAML dependency and to produce a deterministic,
    human-readable output matching the §3.5 example shape.
    """
    lines: list[str] = []

    lines.append(f"run_id: {run_id}")
    lines.append(f"verdict_status: {verdict_status}")
    lines.append(f"round: {round_num}")
    lines.append(f"target_rounds: {target_rounds}")
    lines.append("finding_counts:")
    lines.append(f"  p1: {finding_counts['p1']}")
    lines.append(f"  p2: {finding_counts['p2']}")
    lines.append(f"  p3: {finding_counts['p3']}")

    if findings:
        lines.append("findings:")
        for f in findings:
            lines.append(f"  - id: {f['id']}")
            lines.append(f"    severity: {f['severity']}")
            lines.append(f"    dimension: {_yaml_str(f['dimension'])}")
            lines.append(f"    file: {_yaml_str(f['file'])}")
            lines.append(f"    line: {f['line']}")
            lines.append(f"    description: {_yaml_str(f['description'])}")
            lines.append(f"    suggested_fix: {_yaml_str(f['suggested_fix'])}")
    else:
        lines.append("findings: []")

    # F-013 (§3.5): ISO 8601 timestamps are parsed as Python datetime objects by
    # PyYAML's default loader (Loader=FullLoader / SafeLoader), violating the
    # schema's type:string constraint.  Wrap in _yaml_str() to force YAML string.
    lines.append(f"generated_at: {_yaml_str(generated_at)}")
    lines.append(f"generated_by: {_yaml_str(GENERATED_BY)}")
    lines.append(f"generator_version: {_yaml_str(GENERATOR_VERSION)}")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Error type
# ---------------------------------------------------------------------------


class ParseError(Exception):
    """Raised when the JSONL stream or verdict text cannot be parsed."""


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def _now_rfc3339_ms() -> str:
    """Return current UTC timestamp with millisecond precision: YYYY-MM-DDTHH:MM:SS.mmmZ"""
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"


def _extract_run_id(jsonl_path: str) -> str:
    """Extract run_id from JSONL filename basename (strip .jsonl extension)."""
    basename = os.path.basename(jsonl_path)
    # Strip .jsonl extension (required)
    if basename.endswith(".jsonl"):
        run_id = basename[: -len(".jsonl")]
    else:
        run_id = basename
    if not RUN_ID_RE.match(run_id):
        raise ParseError(
            f"jsonl filename '{basename}' does not match run_id pattern "
            f"YYYY-MM-DDTHH-MM-SSZ-XXXX (got '{run_id}')"
        )
    return run_id


def cmd_probe(jsonl_path: str) -> int:
    """Run probe mode: validate JSONL has parseable agent_message + Section 6 summary.

    Exit 0 on success, non-zero on failure.  No YAML output.
    Per spec §4.4 Step 4 and §4.6 case (b): probe does not require
    --round / --target-rounds.  Cross-field count validation is deferred to
    full parse (requires --round to anchor the authoritative summary line).

    F-002 (§3.6): validates stream shape (thread.started first, no error event,
    turn.completed after last agent_message) before accepting PASS/MINOR/MATERIAL.
    """
    try:
        events = load_events(jsonl_path)
        # F-002: stream-shape sanity check before content parsing
        validate_stream_shape(events)
        verdict_text = extract_verdict_text(events)
        # Probe: accept any parseable summary line (current_round=None)
        parse_section6(verdict_text, current_round=None)
        return 0
    except ParseError as exc:
        print(str(exc), file=sys.stderr)
        return 1


def cmd_jsonl(
    jsonl_path: str,
    round_num: int,
    target_rounds: int,
) -> int:
    """Full parse mode: parse JSONL and emit verdict YAML to stdout.

    Exit 0 on success; non-zero on failure (reason on stderr).

    F-002 (§3.6): validates stream shape before classification to ensure a
    SIGKILL'd or errored codex run cannot yield PASS/MINOR/MATERIAL status.
    """
    try:
        run_id = _extract_run_id(jsonl_path)
        events = load_events(jsonl_path)
        # F-002: stream-shape sanity check before classification
        validate_stream_shape(events)
        verdict_text = extract_verdict_text(events)
        finding_counts, findings = parse_section6(verdict_text, current_round=round_num)
        verdict_status = classify_status(finding_counts)
        generated_at = _now_rfc3339_ms()

        yaml_out = render_verdict_yaml(
            run_id=run_id,
            verdict_status=verdict_status,
            round_num=round_num,
            target_rounds=target_rounds,
            finding_counts=finding_counts,
            findings=findings,
            generated_at=generated_at,
        )
        sys.stdout.write(yaml_out)
        return 0
    except ParseError as exc:
        print(str(exc), file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Parse codex CLI 0.125+ --json JSONL stream into verdict YAML.\n"
            "Modes: --probe (validate only) or --jsonl (emit YAML to stdout)."
        )
    )
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--probe",
        metavar="JSONL",
        dest="probe_path",
        help="Validate JSONL has parseable agent_message + Section 6 summary; "
        "exit 0 on success, non-zero on failure.  No YAML output.",
    )
    mode.add_argument(
        "--jsonl",
        metavar="JSONL",
        dest="jsonl_path",
        help="Parse JSONL and emit verdict YAML to stdout.  "
        "Requires --round and --target-rounds.",
    )
    p.add_argument(
        "--round",
        type=int,
        metavar="ROUND",
        help="Audit round number (required with --jsonl).",
    )
    p.add_argument(
        "--target-rounds",
        type=int,
        metavar="TARGET_ROUNDS",
        help="Total target rounds (required with --jsonl).",
    )
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.probe_path is not None:
        return cmd_probe(args.probe_path)

    # --jsonl mode: validate required companion flags
    if args.round is None or args.target_rounds is None:
        parser.error("--jsonl requires both --round and --target-rounds")

    if args.round < 1:
        parser.error("--round must be >= 1")
    if args.target_rounds < 1:
        parser.error("--target-rounds must be >= 1")
    if args.round > args.target_rounds:
        parser.error(f"--round ({args.round}) must be <= --target-rounds ({args.target_rounds})")

    return cmd_jsonl(
        jsonl_path=args.jsonl_path,
        round_num=args.round,
        target_rounds=args.target_rounds,
    )


if __name__ == "__main__":
    sys.exit(main())
<!-- SOURCE-CONTENT-END -->

<a id="source-scripts-check-audit-artifact-consistency-py"></a>

## SOURCE: scripts/check_audit_artifact_consistency.py

<!-- SOURCE-CONTENT-BEGIN bytes=106405 -->
#!/usr/bin/env python3
"""check_audit_artifact_consistency.py — ARS v3.6.7 Step 6 Phase 6.3 lint.

Implements every row of spec §3.7 invariant families A-F (cross-artifact
contract for the audit-artifact lifecycle). Reads a proposal/persisted entry
plus its companion JSONL / sidecar / verdict files (and optionally the
passport for D1/D3/E2/E6 ledger-level checks) and aggregates findings.

CLI modes:
  --mode proposal             — proposal-state entry validation (oneOf.proposal)
  --mode persisted            — persisted-state entry validation (oneOf.persisted)
  --mode jsonl-stream         — A7 stream-shape pairing only (orchestrator §5.2 L2-5)
  --example-validation-harness — F4: walk docs/design/*.md, validate spec example
                                 payloads against the audit/* schemas

Exit codes:
  0   no findings
  1   lint findings (printed to stdout, one per line)
  2   internal error (exception, missing file the rule cannot ignore)
  64  EX_USAGE — bad CLI arguments

Lifecycle ownership notes (E8/E9 — discipline rules with no lint surface):
  E8 — proposal entry file is the LAST file the wrapper writes (after JSONL +
       sidecar + verdict are all on disk). This is wrapper-side atomicity
       discipline; orchestrator has no lint signal beyond "proposal entry
       exists" (a partial wrapper write is invisible from the entry alone).
  E9 — wrapper is NOT invoked from an in-LLM Bash tool call from the same
       session producing the deliverable (deployment discipline; spec §4.7).
       A same-session in-LLM call is undetectable from artifact evidence;
       defense lives at deployment-level (CI / SubagentStop / out-of-band
       human terminal).

Reuse:
  - scripts/_test_helpers.load_json_schema / build_schema_validator (FORMAT_CHECKER)
  - scripts/_next_verified_at_ms.next_verified_at_ms (D3 monotonic helper)
  - audit_snapshot is the Phase 6.1 reference for argparse subcommand pattern.

The spec §3.7 table is the source of truth; this script is the executable
mirror. Each rule function is annotated with its rule id and one-line summary
so reviewers can grep both directions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError as e:  # pragma: no cover
    print(f"Missing dependency: {e}. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

# ---------------------------------------------------------------------------
# Constants — mirror the schema regexes so we don't depend on a JSON Schema
# load just to get a pattern. Keep regex pair in sync with shared/contracts/.
# ---------------------------------------------------------------------------

RUN_ID_RE = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}Z-[0-9a-f]{4}$"
)
RFC3339_MS_RE = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z$"
)
THREAD_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")

REPO_ROOT = Path(__file__).resolve().parent.parent
PASSPORT_SCHEMAS = REPO_ROOT / "shared/contracts/passport"
AUDIT_SCHEMAS = REPO_ROOT / "shared/contracts/audit"

ENTRY_SCHEMA_PATH = PASSPORT_SCHEMAS / "audit_artifact_entry.schema.json"
JSONL_SCHEMA_PATH = AUDIT_SCHEMAS / "audit_jsonl.schema.json"
SIDECAR_SCHEMA_PATH = AUDIT_SCHEMAS / "audit_sidecar.schema.json"
VERDICT_SCHEMA_PATH = AUDIT_SCHEMAS / "audit_verdict.schema.json"

# audit template path is a const in the sidecar schema — used by B3 to know
# which file is the "template" role in the bundle manifest computation.
AUDIT_TEMPLATE_PATH = "shared/templates/codex_audit_multifile_template.md"


def _load_parse_audit_verdict():
    """Load parse_audit_verdict module by file path via importlib.

    Codex round 5 P2 closure: a bare `from parse_audit_verdict import …`
    only resolves when scripts/ is on sys.path (typical for the CLI
    invocation `python scripts/check_audit_artifact_consistency.py …`).
    A package-style invocation `python -m
    scripts.check_audit_artifact_consistency` or import-from-package
    usage leaves scripts/ off sys.path, the import fails, and the
    fallback silently disabled the L2-3/L2-4 stream-shape gate. Loading
    by absolute file path via importlib makes the gate work in every
    invocation context. The module is co-located by repo convention; if
    it ever moves, this helper raises rather than degrading the gate.
    """
    import importlib.util as _ilu

    here = Path(__file__).resolve().parent
    target = here / "parse_audit_verdict.py"
    spec = _ilu.spec_from_file_location("parse_audit_verdict", target)
    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"could not load parse_audit_verdict from {target}; "
            "Phase 6.1 dependency missing — Phase 6.3 gate cannot run "
            "without the stream-shape validator"
        )
    module = _ilu.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_stream_shape_validator():
    """Backwards-compatible accessor returning (validate_stream_shape, ParseError)."""
    module = _load_parse_audit_verdict()
    return module.validate_stream_shape, module.ParseError


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class LintError:
    """One finding from a rule check.

    rule_id  — stable handle from spec §3.7 (e.g., "A1", "B7", "F2").
    message  — human-readable finding; should name the offending value.
    location — file path or logical location (e.g., "<entry>", "<jsonl>:row=12").
    severity — "error" (default; counts toward exit code 1) or "info"
               (printed to stderr but does not fail the run; used by the
               F4 harness for `...` placeholder rows that are intentional).
    """

    rule_id: str
    message: str
    location: str = "<unknown>"
    severity: str = "error"

    def render(self) -> str:
        prefix = self.rule_id if self.severity == "error" else f"{self.rule_id} info"
        return f"[{prefix}] {self.location}: {self.message}"


@dataclass
class LintContext:
    """Bundle of artifacts a check might want to read.

    Members are Optional because some modes don't need every artifact (e.g.,
    jsonl-stream mode only sees the JSONL). Each rule guards against the
    missing pieces it needs and skips silently if irrelevant; that lets the
    aggregator run every rule it can without short-circuiting.
    """

    mode: str  # "proposal" | "persisted" | "jsonl-stream" | "harness"
    entry: dict[str, Any] | None = None
    entry_path: Path | None = None
    sidecar: dict[str, Any] | None = None
    sidecar_path: Path | None = None
    verdict: dict[str, Any] | None = None
    verdict_path: Path | None = None
    jsonl_events: list[dict[str, Any]] | None = None
    jsonl_path: Path | None = None
    output_dir: Path | None = None
    passport_audit_artifacts: list[dict[str, Any]] | None = None
    passport_path: Path | None = None
    repo_root: Path = field(default_factory=lambda: REPO_ROOT)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sha256_file(path: Path) -> str | None:
    """SHA-256 hex of a file (None if unreadable)."""
    try:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def _safe_get(d: Any, *path: str) -> Any:
    """Dotted-path get on a dict tree; returns None if any segment missing."""
    for key in path:
        if not isinstance(d, dict):
            return None
        d = d.get(key)
        if d is None:
            return None
    return d


def _load_yaml_or_json(path: Path) -> Any:
    """Parse YAML/JSON keeping RFC 3339 timestamps as strings.

    PyYAML's safe_load auto-casts unquoted ISO-8601 datetimes to datetime
    objects (which fails our string-typed schema). We use a custom loader
    that disables the timestamp constructor so timestamps stay strings,
    while still parsing ints/floats/bools as native types — BaseLoader's
    str-only output broke C1 mirror checks comparing verdict_file (loaded
    as YAML, all-string) against entry (loaded as JSON, typed).
    """
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.load(text, Loader=_StrTimestampSafeLoader)


class _StrTimestampSafeLoader(yaml.SafeLoader):
    """SafeLoader variant that keeps timestamps as strings.

    Otherwise PyYAML auto-converts `2026-04-30T15:22:04.123Z` into a
    datetime object, which breaks string-typed schema validation and the
    C1 mirror equality check (entry side reads as str via JSON).
    """


def _yaml_str_timestamp_constructor(loader: yaml.Loader, node: yaml.Node) -> str:
    return loader.construct_scalar(node)


_StrTimestampSafeLoader.add_constructor(
    "tag:yaml.org,2002:timestamp", _yaml_str_timestamp_constructor
)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"jsonl row {lineno}: {e}") from e
            if not isinstance(row, dict):
                raise ValueError(f"jsonl row {lineno}: not a JSON object")
            out.append(row)
    return out


def _bare_run_id_from_basename(filename: str, ext: str) -> str | None:
    """Strip a known extension and return the bare <run_id>, or None on mismatch.

    We avoid Path.stem / .name parsing tricks to keep the rule legible: a
    sidecar named `2026-04-30T15-22-04Z-d8f3.meta.json` returns
    `2026-04-30T15-22-04Z-d8f3` only when ext='.meta.json'.
    """
    if not filename.endswith(ext):
        return None
    return filename[: -len(ext)]


# ---------------------------------------------------------------------------
# Family A — Per-artifact cross-field rules
# ---------------------------------------------------------------------------


def check_a1(entry: dict[str, Any] | None, verdict: dict[str, Any] | None,
             location: str = "<entry>") -> list[LintError]:
    """A1 — verdict.status agrees with finding_counts and failure_reason.

    Applies to BOTH the entry's verdict block and the verdict file. We
    check whichever is provided. Spec rules:
      PASS:           p1==0 AND p2==0 AND p3==0 AND failure_reason absent
      MINOR:          p1==0 AND p2==0 AND p3<=3 AND failure_reason absent
      MATERIAL:       (p1>0 OR p2>0 OR p3>3) AND failure_reason absent
      AUDIT_FAILED:   p1==0 AND p2==0 AND p3==0 AND failure_reason set non-empty
    """
    findings: list[LintError] = []
    for label, doc in (("entry.verdict", _safe_get(entry, "verdict")), ("verdict_file", verdict)):
        if doc is None:
            continue
        # verdict file uses verdict_status; entry.verdict uses status
        status = doc.get("status") if "status" in doc else doc.get("verdict_status")
        counts = doc.get("finding_counts") or {}
        p1 = counts.get("p1")
        p2 = counts.get("p2")
        p3 = counts.get("p3")
        if status is None or not all(isinstance(x, int) for x in (p1, p2, p3)):
            continue  # schema-level rejection; not A1's surface
        failure_reason = doc.get("failure_reason")
        has_failure = isinstance(failure_reason, str) and len(failure_reason) > 0

        loc = f"{location}:{label}"
        if status == "PASS":
            if not (p1 == 0 and p2 == 0 and p3 == 0):
                findings.append(LintError("A1",
                    f"PASS requires p1==p2==p3==0 (got p1={p1},p2={p2},p3={p3})", loc))
            if has_failure:
                findings.append(LintError("A1",
                    "PASS forbids failure_reason", loc))
        elif status == "MINOR":
            # Codex round 10 P2 closure: spec §3.2 cross-field rule for MINOR
            # is "p1==0 AND p2==0 AND p3<=3" — but PASS already covers
            # p3==0 case, and the wrapper / parse_audit_verdict.py classifies
            # zero findings as PASS not MINOR. A MINOR verdict with
            # p1=p2=p3=0 is malformed (status disagrees with the parser's
            # classification) and would let an inconsistent verdict file
            # send the orchestrator down the MINOR escalation path with
            # no findings to show. Require p3>=1 for MINOR — the lower
            # bound that distinguishes MINOR from PASS.
            if not (p1 == 0 and p2 == 0 and 1 <= p3 <= 3):
                findings.append(LintError("A1",
                    f"MINOR requires p1==0 AND p2==0 AND 1<=p3<=3 (got p1={p1},p2={p2},p3={p3}); "
                    f"zero-count MINOR is malformed — wrapper classifies zero findings as PASS",
                    loc))
            if has_failure:
                findings.append(LintError("A1",
                    "MINOR forbids failure_reason", loc))
        elif status == "MATERIAL":
            if not (p1 > 0 or p2 > 0 or p3 > 3):
                findings.append(LintError("A1",
                    f"MATERIAL requires p1>0 OR p2>0 OR p3>3 (got p1={p1},p2={p2},p3={p3})", loc))
            if has_failure:
                findings.append(LintError("A1",
                    "MATERIAL forbids failure_reason", loc))
        elif status == "AUDIT_FAILED":
            if not (p1 == 0 and p2 == 0 and p3 == 0):
                findings.append(LintError("A1",
                    f"AUDIT_FAILED requires p1==p2==p3==0 (got p1={p1},p2={p2},p3={p3})", loc))
            if not has_failure:
                findings.append(LintError("A1",
                    "AUDIT_FAILED requires failure_reason (non-empty)", loc))
    return findings


def check_a2(entry: dict[str, Any] | None, verdict: dict[str, Any] | None,
             location: str = "<entry>") -> list[LintError]:
    """A2 — failure_reason required iff status == AUDIT_FAILED.

    Mostly redundant with A1 when both sides provide a status, but A2
    surfaces the rule independently so partial documents still get flagged.
    """
    findings: list[LintError] = []
    for label, doc in (("entry.verdict", _safe_get(entry, "verdict")), ("verdict_file", verdict)):
        if doc is None:
            continue
        status = doc.get("status") if "status" in doc else doc.get("verdict_status")
        if status is None:
            continue
        failure_reason = doc.get("failure_reason")
        has_failure = isinstance(failure_reason, str) and len(failure_reason) > 0
        loc = f"{location}:{label}"
        if status == "AUDIT_FAILED" and not has_failure:
            findings.append(LintError("A2",
                "AUDIT_FAILED requires non-empty failure_reason", loc))
        if status != "AUDIT_FAILED" and has_failure:
            findings.append(LintError("A2",
                f"failure_reason forbidden when status={status!r}", loc))
    return findings


def check_a3(entry: dict[str, Any] | None, verdict: dict[str, Any] | None,
             location: str = "<entry>") -> list[LintError]:
    """A3 — round <= target_rounds (entry-side and verdict-file)."""
    findings: list[LintError] = []
    for label, doc in (("entry.verdict", _safe_get(entry, "verdict")), ("verdict_file", verdict)):
        if doc is None:
            continue
        rnd = doc.get("round")
        target = doc.get("target_rounds")
        if not isinstance(rnd, int) or not isinstance(target, int):
            continue
        if rnd > target:
            findings.append(LintError("A3",
                f"round={rnd} > target_rounds={target}", f"{location}:{label}"))
    return findings


def check_a4(entry: dict[str, Any] | None, mode: str,
             location: str = "<entry>") -> list[LintError]:
    """A4 — acknowledgement allowed only on persisted MATERIAL entries.

    Proposal arm forbids acknowledgement entirely (per JSON Schema sketch).
    Persisted PASS / MINOR with acknowledgement → reject.
    """
    if entry is None:
        return []
    if "acknowledgement" not in entry:
        return []
    findings: list[LintError] = []
    if mode == "proposal":
        findings.append(LintError("A4",
            "proposal arm forbids acknowledgement", location))
        return findings
    if mode != "persisted":
        return []
    status = _safe_get(entry, "verdict", "status")
    if status != "MATERIAL":
        findings.append(LintError("A4",
            f"acknowledgement requires verdict.status==MATERIAL (got {status!r})", location))
    return findings


def check_a5(verdict: dict[str, Any] | None,
             location: str = "<verdict>") -> list[LintError]:
    """A5 — verdict file's finding_counts.pN == count(findings[severity == PN]).

    Verdict-file rule only (entry's verdict block is a counts-only mirror per C1).
    """
    if verdict is None:
        return []
    counts = verdict.get("finding_counts") or {}
    findings_list = verdict.get("findings")
    if not isinstance(findings_list, list):
        return []
    out: list[LintError] = []
    actual = {"P1": 0, "P2": 0, "P3": 0}
    for f in findings_list:
        sev = f.get("severity") if isinstance(f, dict) else None
        if sev in actual:
            actual[sev] += 1
    for n in (1, 2, 3):
        declared = counts.get(f"p{n}")
        seen = actual[f"P{n}"]
        if isinstance(declared, int) and declared != seen:
            out.append(LintError("A5",
                f"finding_counts.p{n}={declared} disagrees with findings[severity==P{n}].count={seen}",
                location))
    return out


def check_a6(verdict: dict[str, Any] | None,
             location: str = "<verdict>") -> list[LintError]:
    """A6 — when verdict_status==AUDIT_FAILED, findings == []."""
    if verdict is None:
        return []
    status = verdict.get("verdict_status")
    findings_list = verdict.get("findings")
    if status == "AUDIT_FAILED" and isinstance(findings_list, list) and len(findings_list) > 0:
        return [LintError("A6",
            f"AUDIT_FAILED requires findings==[] (got {len(findings_list)} entries)",
            location)]
    return []


def check_a7(events: list[dict[str, Any]] | None,
             location: str = "<jsonl>") -> list[LintError]:
    """A7 — JSONL stream tool-event pairing.

    For every NON-agent_message item.started, exactly one matching
    item.completed with same item.id, completed-row > started-row, each id
    at most once on each side. agent_message item.completed events are
    EXEMPT from prior-item.started requirement (they don't have one).
    Orphan completions (non-agent_message item.completed without prior
    item.started) are rejected.
    """
    if events is None:
        return []
    findings: list[LintError] = []
    started: dict[str, int] = {}      # item.id -> row
    started_dups: list[tuple[str, int]] = []
    completed: dict[str, int] = {}    # item.id -> row (non-agent_message only)
    completed_dups: list[tuple[str, int]] = []

    for idx, ev in enumerate(events):
        ev_type = ev.get("type")
        if ev_type == "item.started":
            item = ev.get("item") or {}
            iid = item.get("id")
            itype = item.get("type")
            if not isinstance(iid, str):
                continue
            # agent_message starts shouldn't happen but be conservative
            if itype == "agent_message":
                continue
            if iid in started:
                started_dups.append((iid, idx))
            else:
                started[iid] = idx
        elif ev_type == "item.completed":
            item = ev.get("item") or {}
            iid = item.get("id")
            itype = item.get("type")
            if not isinstance(iid, str):
                continue
            if itype == "agent_message":
                continue  # exempt
            if iid in completed:
                completed_dups.append((iid, idx))
            else:
                completed[iid] = idx

    # Duplicates
    for iid, row in started_dups:
        findings.append(LintError("A7",
            f"duplicate item.started for item.id={iid!r} at row {row}", location))
    for iid, row in completed_dups:
        findings.append(LintError("A7",
            f"duplicate item.completed for item.id={iid!r} at row {row}", location))

    # Orphan completions (no prior started)
    for iid, row in completed.items():
        if iid not in started:
            findings.append(LintError("A7",
                f"orphan item.completed for item.id={iid!r} at row {row} (no prior item.started)",
                location))

    # Unmatched starts (no completion)
    for iid, row in started.items():
        if iid not in completed:
            findings.append(LintError("A7",
                f"unmatched item.started for item.id={iid!r} at row {row} (no item.completed)",
                location))
        else:
            # ordering — completed-row must exceed started-row
            crow = completed[iid]
            srow = started[iid]
            if crow <= srow:
                findings.append(LintError("A7",
                    f"item.completed (row {crow}) precedes or equals item.started (row {srow}) for id={iid!r}",
                    location))
    return findings


# ---------------------------------------------------------------------------
# Family B — Cross-file rules (Layer 3)
# ---------------------------------------------------------------------------


def check_b1(sidecar: dict[str, Any] | None, events: list[dict[str, Any]] | None,
             verdict: dict[str, Any] | None, location: str = "<sidecar/jsonl>") -> list[LintError]:
    """B1 — sidecar.stream.jsonl_thread_id matches JSONL's thread.started.thread_id.

    SUSPENDED when companion verdict.verdict_status == AUDIT_FAILED (per
    §3.4 conditional — empty string permitted there).
    """
    if sidecar is None or events is None:
        return []
    side_tid = _safe_get(sidecar, "stream", "jsonl_thread_id")
    # AUDIT_FAILED suspension
    v_status = (_safe_get(verdict, "verdict_status")
                if verdict is not None else None)
    if v_status == "AUDIT_FAILED":
        # rule suspended; empty string allowed
        return []
    # find first thread.started event
    jsonl_tid = None
    for ev in events:
        if ev.get("type") == "thread.started":
            jsonl_tid = ev.get("thread_id")
            break
    if side_tid is None or jsonl_tid is None:
        return [LintError("B1",
            f"missing thread_id (sidecar={side_tid!r}, jsonl={jsonl_tid!r})",
            location)]
    if side_tid != jsonl_tid:
        return [LintError("B1",
            f"sidecar.stream.jsonl_thread_id={side_tid!r} != JSONL.thread.started.thread_id={jsonl_tid!r}",
            location)]
    return []


def check_b2(entry: dict[str, Any] | None, sidecar: dict[str, Any] | None,
             repo_root: Path, location: str = "<entry/sidecar>") -> list[LintError]:
    """B2 — entry.deliverable_sha == sidecar's matching primary sha
    == current SHA-256 of deliverable file on disk."""
    if entry is None or sidecar is None:
        return []
    findings: list[LintError] = []
    entry_sha = entry.get("deliverable_sha")
    deliv_path = entry.get("deliverable_path")
    primaries = _safe_get(sidecar, "prompt", "bundle", "primary_deliverables") or []
    side_sha = None
    for p in primaries:
        if isinstance(p, dict) and p.get("path") == deliv_path:
            side_sha = p.get("sha")
            break
    if side_sha is None:
        return [LintError("B2",
            f"sidecar.prompt.bundle.primary_deliverables has no entry for {deliv_path!r}",
            location)]
    if entry_sha != side_sha:
        findings.append(LintError("B2",
            f"entry.deliverable_sha={entry_sha!r} != sidecar primary[{deliv_path!r}].sha={side_sha!r}",
            location))
    # Verify against on-disk file
    if isinstance(deliv_path, str):
        disk_path = repo_root / deliv_path
        if disk_path.exists():
            disk_sha = _sha256_file(disk_path)
            if disk_sha is not None and disk_sha != entry_sha:
                findings.append(LintError("B2",
                    f"current_file_SHA256({deliv_path!r})={disk_sha!r} != entry.deliverable_sha={entry_sha!r}",
                    location))
        # Missing file is not a B2 failure if entry/sidecar agree — caller
        # may be running against synthetic fixtures. Spec allows lint to
        # detect mutation; absence of file is a separate concern.
    return findings


def compute_bundle_manifest(primary: list[dict[str, Any]],
                            supporting: list[dict[str, Any]],
                            template_path: str,
                            template_sha: str) -> tuple[str, str]:
    """Compute (manifest_text, manifest_sha) per spec §3.6.

    Manifest format: '<role>:<path>:<sha>' lines, sorted lex by (role, path),
    LF separator, trailing LF, then SHA-256 of UTF-8 bytes.
    """
    lines: list[tuple[str, str, str]] = []
    for p in primary:
        if isinstance(p, dict) and "path" in p and "sha" in p:
            lines.append(("primary", str(p["path"]), str(p["sha"])))
    for p in supporting:
        if isinstance(p, dict) and "path" in p and "sha" in p:
            lines.append(("supporting", str(p["path"]), str(p["sha"])))
    lines.append(("template", template_path, template_sha))
    lines.sort(key=lambda t: (t[0], t[1]))
    text = "".join(f"{role}:{path}:{sha}\n" for role, path, sha in lines)
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return text, sha


def check_b3(sidecar: dict[str, Any] | None, repo_root: Path,
             location: str = "<sidecar>") -> list[LintError]:
    """B3 — sidecar.prompt.bundle.bundle_manifest_sha == recomputed_sha.

    Recomputes over the CURRENT on-disk SHA-256 of every primary +
    supporting + template file (per §3.6 manifest format).

    NOTE: this rule needs the actual files on disk. When fixtures use fake
    paths, we recompute using the SHAs the sidecar declared (so the rule
    still catches the case where the manifest_sha doesn't agree with the
    declared per-file SHAs even before live-disk verification). When the
    files DO exist on disk, we additionally verify that the live SHAs
    agree, raising the more specific finding if they don't.
    """
    if sidecar is None:
        return []
    bundle = _safe_get(sidecar, "prompt", "bundle")
    if not isinstance(bundle, dict):
        return []
    declared_sha = bundle.get("bundle_manifest_sha")
    primary = bundle.get("primary_deliverables") or []
    supporting = bundle.get("supporting_context") or []
    template_path = _safe_get(sidecar, "prompt", "audit_template_path") or AUDIT_TEMPLATE_PATH
    template_sha = _safe_get(sidecar, "prompt", "audit_template_sha")
    if template_sha is None:
        return [LintError("B3",
            "sidecar.prompt.audit_template_sha missing", location)]

    # Step 1 — recompute against the SHAs the sidecar itself declares.
    _, sha_from_declared = compute_bundle_manifest(primary, supporting, template_path, template_sha)
    findings: list[LintError] = []
    if declared_sha != sha_from_declared:
        findings.append(LintError("B3",
            f"declared bundle_manifest_sha={declared_sha!r} disagrees with manifest of declared file SHAs (computed={sha_from_declared!r})",
            location))

    # Step 2 — verify against live disk SHAs. Codex round 2 P2 closure:
    # a missing bundle file must NOT fall back to the sidecar-declared SHA
    # (that would let a deleted/moved file silently pass B3 because the
    # recomputed manifest would still match). Treat missing as
    # stale/unverifiable: emit B3 finding and skip live-manifest comparison
    # (no live manifest exists when files are gone). When repo_root has no
    # .git/ marker (synthetic fixtures in tmp_path), skip the live check
    # entirely — same convention as B4.
    if not (repo_root / ".git").exists():
        return findings  # Step 1 already ran; Step 2 needs a real repo

    live_primary: list[dict[str, Any]] = []
    live_supporting: list[dict[str, Any]] = []
    missing_bundle_files: list[str] = []
    for role, items, sink in (("primary", primary, live_primary), ("supporting", supporting, live_supporting)):
        for p in items:
            if not isinstance(p, dict):
                continue
            path = p.get("path")
            if not isinstance(path, str):
                continue
            disk_path = repo_root / path
            if disk_path.exists():
                disk_sha = _sha256_file(disk_path)
                sink.append({"path": path, "sha": disk_sha or p.get("sha")})
            else:
                missing_bundle_files.append(f"{role}:{path}")
    template_disk = repo_root / template_path
    if template_disk.exists():
        live_template_sha = _sha256_file(template_disk) or template_sha
    else:
        missing_bundle_files.append(f"template:{template_path}")
        live_template_sha = template_sha

    if missing_bundle_files:
        # File-level mutation evidence (deletion / move) — flag explicitly so
        # the auditor sees which file is gone, not just a manifest SHA mismatch.
        findings.append(LintError("B3",
            f"bundle file(s) missing on disk; cannot verify live manifest: "
            f"{missing_bundle_files} — treat as stale/unverifiable",
            location))
        return findings

    # All files present — recompute live manifest and compare.
    _, sha_live = compute_bundle_manifest(live_primary, live_supporting, template_path, live_template_sha)
    if declared_sha != sha_live:
        findings.append(LintError("B3",
            f"declared bundle_manifest_sha={declared_sha!r} disagrees with live bundle (computed={sha_live!r}) — bundle file changed since audit",
            location))
    return findings


def check_b4(sidecar: dict[str, Any] | None, repo_root: Path,
             location: str = "<sidecar>") -> list[LintError]:
    """B4 — sidecar.runner.git_sha resolves to a real commit."""
    if sidecar is None:
        return []
    git_sha = _safe_get(sidecar, "runner", "git_sha")
    if not isinstance(git_sha, str):
        return []
    # Skip live-git check when not in a real git repo (allows synthetic fixtures
    # with valid-looking but fictitious SHAs to pass B4 without false positive).
    git_dir = repo_root / ".git"
    if not git_dir.exists():
        return []
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "cat-file", "-e", f"{git_sha}^{{commit}}"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return [LintError("B4",
                f"runner.git_sha={git_sha!r} does not resolve to a real commit",
                location)]
    except (subprocess.SubprocessError, OSError) as e:
        # Internal — don't fail the whole lint over a git error
        return [LintError("B4",
            f"git resolve failed for {git_sha!r}: {e}", location)]
    return []


def check_b5(sidecar: dict[str, Any] | None,
             location: str = "<sidecar>") -> list[LintError]:
    """B5 — ended_at - started_at == duration_seconds (±1s)."""
    if sidecar is None:
        return []
    timing = sidecar.get("timing") or {}
    started = timing.get("started_at")
    ended = timing.get("ended_at")
    duration_raw = timing.get("duration_seconds")
    if not (isinstance(started, str) and isinstance(ended, str)):
        return []
    try:
        duration = float(duration_raw)
    except (TypeError, ValueError):
        return [LintError("B5",
            f"duration_seconds not numeric: {duration_raw!r}", location)]
    # Parse RFC3339 ms strings
    if not (RFC3339_MS_RE.match(started) and RFC3339_MS_RE.match(ended)):
        # Schema-level rejection territory; B5 still flags arithmetic mismatch
        # but only if we can parse. Skip non-RFC3339-ms here.
        return []
    from datetime import datetime, timezone
    fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    try:
        dt_s = datetime.strptime(started, fmt).replace(tzinfo=timezone.utc)
        dt_e = datetime.strptime(ended, fmt).replace(tzinfo=timezone.utc)
    except ValueError:
        return []
    delta = (dt_e - dt_s).total_seconds()
    if abs(delta - duration) > 1.0:
        return [LintError("B5",
            f"timing arithmetic: ended_at - started_at = {delta:.3f}s, duration_seconds = {duration:.3f}s (±1s tolerance exceeded)",
            location)]
    return []


def check_b6(sidecar: dict[str, Any] | None, verdict: dict[str, Any] | None,
             location: str = "<sidecar/verdict>") -> list[LintError]:
    """B6 — sidecar.process.exit_code == 0 for non-AUDIT_FAILED entries.

    Non-zero exit_code allowed only when verdict_status == AUDIT_FAILED.
    """
    if sidecar is None:
        return []
    exit_code = _safe_get(sidecar, "process", "exit_code")
    if not isinstance(exit_code, int):
        return []
    v_status = _safe_get(verdict, "verdict_status") if verdict else None
    if exit_code != 0 and v_status != "AUDIT_FAILED":
        return [LintError("B6",
            f"process.exit_code={exit_code} non-zero with verdict_status={v_status!r} (only AUDIT_FAILED permits non-zero exit)",
            location)]
    if exit_code == 0 and v_status == "AUDIT_FAILED":
        # Spec doesn't strictly forbid; AUDIT_FAILED can come from JSONL parse
        # error even when codex exited 0. Don't flag.
        pass
    return []


def check_b7(entry: dict[str, Any] | None, sidecar: dict[str, Any] | None,
             entry_path: Path | None, sidecar_path: Path | None,
             jsonl_path: Path | None, verdict_path: Path | None,
             mode: str, location: str = "<artifacts>",
             repo_root: Path | None = None,
             verdict: dict[str, Any] | None = None) -> list[LintError]:
    """B7 — entry.run_id == sidecar.run_id == verdict.run_id == bare basename of every co-located file.

    Proposal mode: 4 files (jsonl + meta.json + verdict.yaml + entry.json).
    Persisted mode: 3 files (entry consumed; not file-checked here).

    repo_root enables the round-8 P2 closure: cross-check that entry's
    recorded artifact_paths actually resolve to (and equal) the CLI-loaded
    files. Without this, an entry could record artifact_paths pointing at
    a missing or wrong directory while the CLI loads valid evidence from
    --output-dir; the orchestrator later follows the recorded paths.

    `verdict` enables the round-15 P1 closure: cross-check the verdict
    file's internal `run_id` field against entry+sidecar+basename. C1
    mirrors only the nested verdict block (status/round/counts/...) and
    skips the verdict-file-level run_id; without this check, swapping a
    valid verdict.yaml from a different run into the canonical filename
    slot would pass B7 (basenames match), C1 (counts mirror entry), and
    the rest of the gate as long as PASS/MINOR/MATERIAL counts agree.
    """
    if entry is None or sidecar is None:
        return []
    findings: list[LintError] = []
    entry_run_id = entry.get("run_id")
    side_run_id = sidecar.get("run_id")
    if entry_run_id != side_run_id:
        findings.append(LintError("B7",
            f"entry.run_id={entry_run_id!r} != sidecar.run_id={side_run_id!r}",
            location))
    # Codex round 15 P1 closure: also verify verdict.run_id matches.
    if verdict is not None:
        v_run_id = verdict.get("run_id")
        if v_run_id is not None and v_run_id != side_run_id:
            findings.append(LintError("B7",
                f"verdict.run_id={v_run_id!r} != sidecar.run_id={side_run_id!r} "
                f"(swap-one-verdict-file forgery seam — verdict file was renamed "
                f"into <run_id>.verdict.yaml but internal run_id belongs to a "
                f"different run)",
                location))

    # File basename checks (only when we have actual paths)
    canonical = side_run_id if isinstance(side_run_id, str) else entry_run_id
    if not isinstance(canonical, str):
        return findings

    files_to_check: list[tuple[Path, str, str]] = []
    if sidecar_path is not None:
        files_to_check.append((sidecar_path, ".meta.json", "sidecar"))
    if jsonl_path is not None:
        files_to_check.append((jsonl_path, ".jsonl", "jsonl"))
    if verdict_path is not None:
        files_to_check.append((verdict_path, ".verdict.yaml", "verdict"))
    if mode == "proposal" and entry_path is not None:
        files_to_check.append((entry_path, ".audit_artifact_entry.json", "entry"))

    for path, ext, role in files_to_check:
        bare = _bare_run_id_from_basename(path.name, ext)
        if bare is None:
            findings.append(LintError("B7",
                f"{role} file {path.name!r} does not end with {ext!r}",
                location))
        elif bare != canonical:
            findings.append(LintError("B7",
                f"{role} file basename stem={bare!r} != canonical run_id={canonical!r}",
                location))

    # Codex round 4 P2 closure: entry["artifact_paths"] is the contract the
    # orchestrator follows post-merge. A hand-edited entry that points its
    # artifact_paths at a different run's files (jsonl/sidecar/verdict)
    # would forge the swap-one-artifact-file attack seam (§3.7 B7). The
    # B7 cross-file check above only inspects the paths supplied to the
    # CLI; an explicit basename validation of the recorded artifact_paths
    # closes the gap regardless of how the lint was invoked.
    artifact_paths = entry.get("artifact_paths") if isinstance(entry, dict) else None
    cli_loaded_paths = {
        "jsonl": jsonl_path,
        "sidecar": sidecar_path,
        "verdict": verdict_path,
    }
    if isinstance(artifact_paths, dict):
        for key, ext in (("jsonl", ".jsonl"),
                         ("sidecar", ".meta.json"),
                         ("verdict", ".verdict.yaml")):
            recorded = artifact_paths.get(key)
            if not isinstance(recorded, str) or not recorded:
                continue  # schema validation already covers missing/non-str
            recorded_basename = recorded.rsplit("/", 1)[-1]
            bare = _bare_run_id_from_basename(recorded_basename, ext)
            if bare is None:
                findings.append(LintError("B7",
                    f"entry.artifact_paths.{key}={recorded!r} basename does not end with {ext!r}",
                    location))
                continue
            if bare != canonical:
                findings.append(LintError("B7",
                    f"entry.artifact_paths.{key}={recorded!r} basename stem={bare!r} "
                    f"!= canonical run_id={canonical!r} (artifact-paths forgery seam)",
                    location))
                continue
            # Codex round 8 P2 closure: basename match alone leaves the path
            # forgery seam open — entry can record paths pointing at a
            # missing or wrong directory while CLI loads valid files from
            # elsewhere. Resolve the recorded path against repo_root and
            # confirm (a) the file actually exists at that location, and
            # (b) it matches the CLI-loaded artifact for that role.
            if repo_root is not None:
                resolved = (repo_root / recorded).resolve()
                if not resolved.exists():
                    findings.append(LintError("B7",
                        f"entry.artifact_paths.{key}={recorded!r} resolves to "
                        f"{resolved} which does not exist on disk — recorded "
                        f"path is the contract orchestrator follows post-merge",
                        location))
                    continue
                cli_path = cli_loaded_paths.get(key)
                if cli_path is not None and cli_path.exists():
                    cli_resolved = cli_path.resolve()
                    if resolved != cli_resolved and not resolved.samefile(cli_resolved):
                        findings.append(LintError("B7",
                            f"entry.artifact_paths.{key}={recorded!r} resolves to "
                            f"{resolved} but CLI loaded {cli_resolved} — declared "
                            f"path is the evidence the orchestrator will verify; "
                            f"loading from a different location masks divergence",
                            location))
    return findings


def check_b8(entry: dict[str, Any] | None, mode: str,
             location: str = "<entry>") -> list[LintError]:
    """B8 — persisted ack: verdict.verified_at == acknowledgement.acknowledged_at."""
    if entry is None or mode != "persisted":
        return []
    ack = entry.get("acknowledgement")
    if not isinstance(ack, dict):
        return []
    verified_at = _safe_get(entry, "verdict", "verified_at")
    ack_at = ack.get("acknowledged_at")
    if verified_at != ack_at:
        return [LintError("B8",
            f"verified_at={verified_at!r} != acknowledgement.acknowledged_at={ack_at!r} (must be same instant by D3 construction)",
            location)]
    return []


def check_b9(entry: dict[str, Any] | None, sidecar: dict[str, Any] | None,
             location: str = "<entry/sidecar>") -> list[LintError]:
    """B9 — when entry.bundle_id present, equals sidecar.prompt.bundle.bundle_id."""
    if entry is None or sidecar is None:
        return []
    if "bundle_id" not in entry:
        return []
    entry_bid = entry.get("bundle_id")
    side_bid = _safe_get(sidecar, "prompt", "bundle", "bundle_id")
    if entry_bid != side_bid:
        return [LintError("B9",
            f"entry.bundle_id={entry_bid!r} != sidecar.prompt.bundle.bundle_id={side_bid!r}",
            location)]
    return []


def check_b10(entry: dict[str, Any] | None, verdict: dict[str, Any] | None,
              mode: str, location: str = "<entry/verdict>") -> list[LintError]:
    """B10 — persisted ack acknowledgement.finding_ids: non-empty, all exist
    in verdict.findings[].id, full coverage (set equality)."""
    if entry is None or verdict is None or mode != "persisted":
        return []
    ack = entry.get("acknowledgement")
    if not isinstance(ack, dict):
        return []
    declared = ack.get("finding_ids")
    if not isinstance(declared, list):
        return [LintError("B10",
            f"acknowledgement.finding_ids must be array (got {type(declared).__name__})",
            location)]
    if len(declared) == 0:
        return [LintError("B10",
            "acknowledgement.finding_ids must be non-empty", location)]
    findings_list = verdict.get("findings") or []
    real_ids = {f.get("id") for f in findings_list if isinstance(f, dict)}
    declared_set = set(declared)
    out: list[LintError] = []
    missing_in_real = declared_set - real_ids
    if missing_in_real:
        out.append(LintError("B10",
            f"acknowledgement.finding_ids contains unknown ids {sorted(missing_in_real)} (not in verdict.findings[].id)",
            location))
    missing_in_declared = real_ids - declared_set
    if missing_in_declared:
        out.append(LintError("B10",
            f"acknowledgement.finding_ids missing full coverage: {sorted(missing_in_declared)} not acknowledged",
            location))
    return out


# ---------------------------------------------------------------------------
# Family C — Mirror rules
# ---------------------------------------------------------------------------


def check_c1(entry: dict[str, Any] | None, verdict: dict[str, Any] | None,
             location: str = "<entry/verdict>") -> list[LintError]:
    """C1 — entry.verdict.{status, round, target_rounds, finding_counts, failure_reason}
    mirrors verdict file's matching fields (verdict file wins)."""
    if entry is None or verdict is None:
        return []
    ev = entry.get("verdict") or {}
    findings: list[LintError] = []

    pairs = [
        ("status", "verdict_status"),
        ("round", "round"),
        ("target_rounds", "target_rounds"),
        ("finding_counts", "finding_counts"),
        ("failure_reason", "failure_reason"),
    ]
    for entry_key, vfile_key in pairs:
        ev_val = ev.get(entry_key)
        vf_val = verdict.get(vfile_key)
        # failure_reason is conditional — present-or-absent on each side; we
        # compare presence consistency too.
        if entry_key == "failure_reason":
            if (ev_val is None) != (vf_val is None):
                findings.append(LintError("C1",
                    f"failure_reason presence drift: entry={ev_val!r}, verdict_file={vf_val!r}",
                    location))
            elif ev_val is not None and ev_val != vf_val:
                findings.append(LintError("C1",
                    f"failure_reason drift: entry={ev_val!r}, verdict_file={vf_val!r}",
                    location))
            continue
        if ev_val != vf_val:
            findings.append(LintError("C1",
                f"{entry_key} drift: entry={ev_val!r}, verdict_file={vf_val!r} (verdict file wins)",
                location))
    return findings


def check_c2(entry: dict[str, Any] | None, sidecar: dict[str, Any] | None,
             location: str = "<entry/sidecar>") -> list[LintError]:
    """C2 — entry.bundle_manifest_sha == sidecar.prompt.bundle.bundle_manifest_sha."""
    if entry is None or sidecar is None:
        return []
    e_sha = entry.get("bundle_manifest_sha")
    s_sha = _safe_get(sidecar, "prompt", "bundle", "bundle_manifest_sha")
    if e_sha != s_sha:
        return [LintError("C2",
            f"entry.bundle_manifest_sha={e_sha!r} != sidecar.bundle_manifest_sha={s_sha!r}",
            location)]
    return []


def check_c3(new_entry: dict[str, Any] | None, prior_entry: dict[str, Any] | None,
             location: str = "<entry/prior>") -> list[LintError]:
    """C3 — Acknowledgement append entry copies prior entry's
    (stage, agent, deliverable_path, deliverable_sha, run_id,
     bundle_manifest_sha, artifact_paths) AND inner verdict shape
    (status, round, target_rounds, finding_counts, failure_reason)
    byte-for-byte. verified_at and verified_by are FRESHLY set, NOT copied.
    """
    if new_entry is None or prior_entry is None:
        return []
    findings: list[LintError] = []
    copied_fields = ("stage", "agent", "deliverable_path", "deliverable_sha",
                     "run_id", "bundle_manifest_sha", "artifact_paths")
    for f in copied_fields:
        if new_entry.get(f) != prior_entry.get(f):
            findings.append(LintError("C3",
                f"ack entry must copy {f} byte-for-byte: prior={prior_entry.get(f)!r}, new={new_entry.get(f)!r}",
                location))
    # Inner verdict shape
    new_v = new_entry.get("verdict") or {}
    prior_v = prior_entry.get("verdict") or {}
    inner_fields = ("status", "round", "target_rounds", "finding_counts", "failure_reason")
    for f in inner_fields:
        if new_v.get(f) != prior_v.get(f):
            findings.append(LintError("C3",
                f"ack entry must copy verdict.{f} byte-for-byte: prior={prior_v.get(f)!r}, new={new_v.get(f)!r}",
                location))
    # verified_at must be FRESHLY SET (different from prior).
    if (new_v.get("verified_at") is not None and
        new_v.get("verified_at") == prior_v.get("verified_at")):
        findings.append(LintError("C3",
            f"ack entry verified_at={new_v.get('verified_at')!r} must be freshly set (>= prior + 1ms via D3); equals prior",
            location))
    return findings


def check_c4(entry: dict[str, Any] | None, sidecar: dict[str, Any] | None,
             location: str = "<entry/sidecar>") -> list[LintError]:
    """C4 — entry.deliverable_sha == sidecar primary_deliverables[].sha
    for matching primary deliverable (entry-side half of B2)."""
    # We reuse the same check as B2 minus the disk verification; emit C4 not B2.
    if entry is None or sidecar is None:
        return []
    findings: list[LintError] = []
    entry_sha = entry.get("deliverable_sha")
    deliv_path = entry.get("deliverable_path")
    primaries = _safe_get(sidecar, "prompt", "bundle", "primary_deliverables") or []
    side_sha = None
    for p in primaries:
        if isinstance(p, dict) and p.get("path") == deliv_path:
            side_sha = p.get("sha")
            break
    if side_sha is None:
        findings.append(LintError("C4",
            f"sidecar.prompt.bundle.primary_deliverables has no entry for {deliv_path!r}",
            location))
    elif entry_sha != side_sha:
        findings.append(LintError("C4",
            f"entry.deliverable_sha={entry_sha!r} != sidecar primary[{deliv_path!r}].sha={side_sha!r}",
            location))
    return findings


# ---------------------------------------------------------------------------
# Family D — Ordering rules
# ---------------------------------------------------------------------------


def check_d1(passport_audit_artifacts: list[dict[str, Any]] | None,
             location: str = "<passport>") -> list[LintError]:
    """D1 — Latest persisted entry by max(verdict.verified_at) per (stage, agent,
    deliverable_sha) tuple. Lint flags duplicate verified_at within group as
    ordering ambiguity (D3 should make this impossible).

    We report duplicates; selection logic itself isn't a runtime check.
    """
    if not passport_audit_artifacts:
        return []
    findings: list[LintError] = []
    seen: dict[tuple, list[str]] = {}
    for entry in passport_audit_artifacts:
        if not isinstance(entry, dict):
            continue
        key = (entry.get("stage"), entry.get("agent"),
               entry.get("deliverable_sha"), entry.get("run_id"))
        va = _safe_get(entry, "verdict", "verified_at")
        if va is None:
            continue
        seen.setdefault(key, []).append(va)
    for key, vas in seen.items():
        if len(vas) != len(set(vas)):
            findings.append(LintError("D1",
                f"duplicate verified_at in (stage,agent,sha,run_id)={key}: {vas} — D3 monotonic helper should prevent this",
                location))
    return findings


def check_d2(proposals: list[dict[str, Any]] | None,
             location: str = "<output-dir>") -> list[LintError]:
    """D2 — Path B proposal selection determinism check.

    Lint surface: detect proposals sharing identical sidecar.timing.started_at
    where run_id lex-max would be the only tie-breaker (legitimate but worth
    surfacing as ambiguity warning).
    """
    if not proposals:
        return []
    findings: list[LintError] = []
    by_started: dict[str, list[str]] = {}
    for p in proposals:
        st = _safe_get(p, "sidecar", "timing", "started_at")
        rid = _safe_get(p, "entry", "run_id")
        if not isinstance(st, str) or not isinstance(rid, str):
            continue
        by_started.setdefault(st, []).append(rid)
    for st, rids in by_started.items():
        if len(rids) > 1:
            findings.append(LintError("D2",
                f"proposals share started_at={st!r}: {sorted(rids)} — falling back to run_id lex-max tie-breaker",
                location))
    return findings


def check_d3(passport_audit_artifacts: list[dict[str, Any]] | None,
             location: str = "<passport>") -> list[LintError]:
    """D3 — every persisted verified_at strictly greater than every prior.

    Validates monotonicity over the ledger as ordered. A correctly-running
    orchestrator (using _next_verified_at_ms) emits monotonic verified_at;
    if the ledger is not in append order we instead check lex-max property:
    no entry's verified_at is < a later-indexed entry's verified_at.
    Strictly: each entry's verified_at must be > all earlier entries'.
    """
    if not passport_audit_artifacts:
        return []
    findings: list[LintError] = []
    seen: list[str] = []
    for idx, entry in enumerate(passport_audit_artifacts):
        if not isinstance(entry, dict):
            continue
        va = _safe_get(entry, "verdict", "verified_at")
        if not isinstance(va, str):
            continue
        for prior_idx, prior_va in enumerate(seen):
            if va <= prior_va:
                findings.append(LintError("D3",
                    f"audit_artifact[{idx}].verified_at={va!r} not > audit_artifact[{prior_idx}].verified_at={prior_va!r}",
                    location))
                break
        seen.append(va)
    return findings


def check_d4(persisted_round: int | None, proposal_round: int | None,
             location: str = "<entry>") -> list[LintError]:
    """D4 — higher-round unmerged proposals supersede lower-round persisted entries.

    Lint surface: when an unmerged proposal exists alongside a persisted
    entry for the same (stage, agent, deliverable_sha) tuple AND the
    proposal's round is greater than the persisted round, surface the
    supersession requirement (spec §3.7 family D row D4 + §5.6 A1.5).
    The orchestrator must preempt Path A and run Path B with
    supersession_required=true; persisted-mode lint flagging this lets
    the caller see the supersession before the orchestrator processes
    the artifacts.
    """
    if persisted_round is None or proposal_round is None:
        return []
    if proposal_round > persisted_round:
        return [LintError("D4",
            f"unmerged proposal round={proposal_round} supersedes persisted round={persisted_round} "
            f"— orchestrator must preempt Path A and run Path B with supersession_required=true",
            location)]
    return []


# ---------------------------------------------------------------------------
# Family E — Lifecycle ownership
# ---------------------------------------------------------------------------


def check_e1_e2_e6(passport_audit_artifacts: list[dict[str, Any]] | None,
                   location: str = "<passport>") -> list[LintError]:
    """E1/E2/E6 — post-hoc passport-shape checks.

    Detect non-orchestrator-emitted entries by looking for entries that lack
    the orchestrator-set fields (verified_at / verified_by). Also detect
    AUDIT_FAILED entries in the passport (E5/E2 — never persisted).
    """
    if not passport_audit_artifacts:
        return []
    findings: list[LintError] = []
    for idx, entry in enumerate(passport_audit_artifacts):
        if not isinstance(entry, dict):
            findings.append(LintError("E1/E2/E6",
                f"audit_artifact[{idx}] is not an object (type={type(entry).__name__})",
                location))
            continue
        verdict = entry.get("verdict") or {}
        if "verified_at" not in verdict:
            findings.append(LintError("E1/E2/E6",
                f"audit_artifact[{idx}].verdict missing verified_at — non-orchestrator writer suspected",
                location))
        if "verified_by" not in verdict:
            findings.append(LintError("E1/E2/E6",
                f"audit_artifact[{idx}].verdict missing verified_by — non-orchestrator writer suspected",
                location))
        elif verdict.get("verified_by") != "pipeline_orchestrator_agent":
            findings.append(LintError("E1/E2/E6",
                f"audit_artifact[{idx}].verdict.verified_by={verdict.get('verified_by')!r} not 'pipeline_orchestrator_agent'",
                location))
        # Codex round 3 P2 closure: §3.2 lifecycle-conditional table
        # excludes AUDIT_FAILED from the persisted arm. A hand-edited
        # passport entry with verified_at + verified_by + AUDIT_FAILED
        # status would otherwise pass E1/E2/E6's verified_at + verified_by
        # checks above (E5 lives at schema level for CLI modes via the
        # persisted oneOf arm; passport scan needs the same enforcement
        # because AUDIT_FAILED entries are forbidden in `audit_artifact[]`).
        if verdict.get("status") == "AUDIT_FAILED":
            findings.append(LintError("E5",
                f"audit_artifact[{idx}].verdict.status='AUDIT_FAILED' is forbidden in "
                f"passport audit_artifact[] (§3.2: AUDIT_FAILED is proposal-arm only; "
                f"persisted ledger never carries failed-audit entries)",
                location))
    return findings


def check_e3_e4(entry: dict[str, Any] | None, mode: str,
                location: str = "<entry>") -> list[LintError]:
    """E3/E4 — wrapper-emitted proposals carrying verified_at/verified_by are rejected.

    Defense-in-depth on top of schema oneOf.proposal arm.
    """
    if entry is None or mode != "proposal":
        return []
    findings: list[LintError] = []
    verdict = entry.get("verdict") or {}
    if "verified_at" in verdict:
        findings.append(LintError("E3/E4",
            "proposal entry carries verdict.verified_at (Pattern C3 attack surface)",
            location))
    if "verified_by" in verdict:
        findings.append(LintError("E3/E4",
            "proposal entry carries verdict.verified_by (Pattern C3 attack surface)",
            location))
    return findings


def check_e5(entry: dict[str, Any] | None, mode: str,
             location: str = "<entry>") -> list[LintError]:
    """E5 — --mode persisted rejects AUDIT_FAILED status."""
    if entry is None or mode != "persisted":
        return []
    status = _safe_get(entry, "verdict", "status")
    if status == "AUDIT_FAILED":
        return [LintError("E5",
            "persisted entry MUST NOT carry status=AUDIT_FAILED (proposal-arm only)",
            location)]
    return []


def check_e7(entry: dict[str, Any] | None, location: str = "<entry>") -> list[LintError]:
    """E7 — ack entry's verdict.status remains MATERIAL (not synthetic
    'MATERIAL_ACKNOWLEDGED' or similar)."""
    if entry is None:
        return []
    if "acknowledgement" not in entry:
        return []
    status = _safe_get(entry, "verdict", "status")
    if status != "MATERIAL":
        return [LintError("E7",
            f"ack entry must keep verdict.status='MATERIAL'; got {status!r} (no synthetic MATERIAL_ACKNOWLEDGED)",
            location)]
    return []


# ---------------------------------------------------------------------------
# Family F — Naming conventions
# ---------------------------------------------------------------------------


def check_f1(run_id: Any, location: str = "<entry>") -> list[LintError]:
    """F1 — run_id format <ISO-8601-Z>-<4-hex>."""
    if not isinstance(run_id, str):
        return [LintError("F1",
            f"run_id missing or not string (got {type(run_id).__name__})",
            location)]
    if not RUN_ID_RE.match(run_id):
        return [LintError("F1",
            f"run_id={run_id!r} does not match {RUN_ID_RE.pattern}",
            location)]
    return []


def check_f2(jsonl_path: Path | None, sidecar_path: Path | None,
             verdict_path: Path | None, entry_path: Path | None,
             mode: str, location: str = "<artifacts>") -> list[LintError]:
    """F2 — 4 (proposal) or 3 (persisted) artifact basenames use bare run_id stem with
    extensions .jsonl / .meta.json / .verdict.yaml / .audit_artifact_entry.json.
    No stage/agent/deliverable prefix.
    """
    findings: list[LintError] = []
    expectations: list[tuple[Path | None, str, str]] = [
        (jsonl_path, ".jsonl", "jsonl"),
        (sidecar_path, ".meta.json", "sidecar"),
        (verdict_path, ".verdict.yaml", "verdict"),
    ]
    if mode == "proposal":
        expectations.append((entry_path, ".audit_artifact_entry.json", "entry"))

    for path, ext, role in expectations:
        if path is None:
            continue
        if not path.name.endswith(ext):
            findings.append(LintError("F2",
                f"{role} file {path.name!r} does not end with {ext!r}",
                location))
            continue
        bare = path.name[: -len(ext)]
        if not RUN_ID_RE.match(bare):
            findings.append(LintError("F2",
                f"{role} file basename stem={bare!r} not bare run_id (no stage/agent prefix allowed)",
                location))
    return findings


def check_f3(sidecar: dict[str, Any] | None, sidecar_path: Path | None,
             location: str = "<sidecar>") -> list[LintError]:
    """F3 — sidecar.run_id == file basename (with .meta.json stripped)."""
    if sidecar is None or sidecar_path is None:
        return []
    side_run_id = sidecar.get("run_id")
    bare = _bare_run_id_from_basename(sidecar_path.name, ".meta.json")
    if bare is None:
        return [LintError("F3",
            f"sidecar file {sidecar_path.name!r} does not end with .meta.json",
            location)]
    if side_run_id != bare:
        return [LintError("F3",
            f"sidecar.run_id={side_run_id!r} != file basename stem={bare!r}",
            location)]
    return []


# ---------------------------------------------------------------------------
# Aggregation per mode
# ---------------------------------------------------------------------------


def run_checks(ctx: LintContext) -> list[LintError]:
    """Run every applicable rule for the given mode."""
    findings: list[LintError] = []
    mode = ctx.mode

    if mode == "jsonl-stream":
        findings.extend(check_a7(ctx.jsonl_events, location=str(ctx.jsonl_path or "<jsonl>")))
        return findings

    # Proposal / persisted modes — full sweep
    entry_loc = str(ctx.entry_path or "<entry>")
    verdict_loc = str(ctx.verdict_path or "<verdict>")
    sidecar_loc = str(ctx.sidecar_path or "<sidecar>")

    # Family A
    findings.extend(check_a1(ctx.entry, ctx.verdict, location=entry_loc))
    findings.extend(check_a2(ctx.entry, ctx.verdict, location=entry_loc))
    findings.extend(check_a3(ctx.entry, ctx.verdict, location=entry_loc))
    findings.extend(check_a4(ctx.entry, mode, location=entry_loc))
    findings.extend(check_a5(ctx.verdict, location=verdict_loc))
    findings.extend(check_a6(ctx.verdict, location=verdict_loc))
    if ctx.jsonl_events is not None:
        # Codex round 6 P2 closure: A7 tool-event pairing is suspended for
        # AUDIT_FAILED bundles. A failed audit's stream is legitimately
        # truncated — codex may be killed after an item.started but before
        # the matching item.completed — so unmatched starts are expected
        # evidence, not pairing violations. §3.4 suspends Layer 3 cross-
        # file rules for AUDIT_FAILED; the symmetric Layer 2 suspension
        # for stream-shape (round 3 closure) applies to A7 too.
        v_status_for_a7 = (ctx.verdict or {}).get("verdict_status")
        if v_status_for_a7 != "AUDIT_FAILED":
            findings.extend(check_a7(ctx.jsonl_events, location=str(ctx.jsonl_path or "<jsonl>")))
        # Codex round 3 P1 closure: A7 alone does not reject a JSONL that
        # ends after `thread.started + turn.started` (no item.started, so
        # no pairing violation). Phase 6.1's parse_audit_verdict.validate_
        # stream_shape covers L2-3/L2-4 stream-shape gates: exactly one
        # thread.started, second event is turn.started, exactly one
        # terminal turn.completed strictly after the last agent_message,
        # turn.completed.usage all integers >= 0 with input_tokens > 0,
        # canonical UUID thread_id, no error events. Reuse it here so a
        # truncated stream is rejected before the rest of the gate runs.
        # AUDIT_FAILED bundles legitimately have malformed streams (codex
        # was killed mid-run); §3.4 already suspends Layer 3 cross-file
        # rules for them, and we apply the same suspension here.
        v_status = (ctx.verdict or {}).get("verdict_status")
        if v_status != "AUDIT_FAILED":
            # Codex round 5 P2 closure: load parse_audit_verdict by file path
            # via importlib so the stream-shape gate runs regardless of how
            # this checker is invoked (CLI on sys.path, `python -m
            # scripts.check_audit_artifact_consistency`, or imported as
            # `scripts.check_audit_artifact_consistency` from elsewhere).
            # Silent ImportError degrade was hiding the gate from package
            # callers and letting truncated streams pass.
            module = _load_parse_audit_verdict()
            ParseError = module.ParseError
            try:
                module.validate_stream_shape(ctx.jsonl_events)
            except ParseError as e:
                findings.append(LintError(
                    "L2-3/L2-4",
                    f"jsonl stream-shape rejected: {e} — non-AUDIT_FAILED "
                    f"verdict requires a complete stream (thread.started → "
                    f"turn.started → … → turn.completed with valid usage)",
                    str(ctx.jsonl_path or "<jsonl>"),
                ))
            else:
                # Codex round 8 P1 closure: stream-shape alone validates
                # ordering / usage / canonical UUID but does NOT verify the
                # last agent_message contains a parseable Section 6 verdict.
                # A bundle whose JSONL ends with arbitrary text or no
                # verdict at all could pass stream-shape and exit 0 as long
                # as the separate verdict.yaml mirrored the entry. L2-4 in
                # spec §5.2 is `parse_audit_verdict.py --probe` — extract
                # the last agent_message and parse_section6 on its text.
                # cmd_probe in parse_audit_verdict already chains all three
                # checks; we replicate that chain here without invoking
                # the module's CLI (avoids subprocess overhead in lint
                # path) and capture each layer as its own LintError.
                try:
                    verdict_text = module.extract_verdict_text(ctx.jsonl_events)
                except ParseError as e:
                    findings.append(LintError(
                        "L2-4",
                        f"verdict text extraction failed: {e} — non-AUDIT_FAILED "
                        f"bundle requires a parseable agent_message in the JSONL",
                        str(ctx.jsonl_path or "<jsonl>"),
                    ))
                else:
                    try:
                        # Probe-style: pass current_round=None to accept any
                        # parseable summary; cross-field count validation is
                        # already covered by A5 against the verdict.yaml.
                        module.parse_section6(verdict_text, current_round=None)
                    except ParseError as e:
                        findings.append(LintError(
                            "L2-4",
                            f"verdict text Section 6 parse failed: {e} — "
                            f"agent_message did not contain a parseable "
                            f"audit-template Section 6 verdict block",
                            str(ctx.jsonl_path or "<jsonl>"),
                        ))

    # Codex round 9 P2 closure: §3.4 + §5.6 Path B5 + §3.7 family B note say
    # "Layer 3 verification is suspended for AUDIT_FAILED" — the orchestrator
    # short-circuits to BLOCK with failure_reason without running L3-2..L3-8
    # gates. A failed audit caused by bundle mutation legitimately has a
    # different live deliverable SHA from the recorded audit-time SHA;
    # treating that as a B2/B3 violation would reject the failure-signaling
    # artifact instead of letting the orchestrator surface failure_reason.
    # Same suspension extends to B4 git_sha, B5 timing arithmetic, B7
    # cross-file basename / path resolution: all are Layer 3 cross-file
    # verification rules that don't apply when the audit boundary itself
    # failed. B6 is suspended internally by its own AUDIT_FAILED branch
    # (spec §3.4 rule 6 + F-027); B1 has its own conditional handling.
    is_audit_failed = (ctx.verdict or {}).get("verdict_status") == "AUDIT_FAILED"

    # Family B
    findings.extend(check_b1(ctx.sidecar, ctx.jsonl_events, ctx.verdict, location=sidecar_loc))
    if not is_audit_failed:
        findings.extend(check_b2(ctx.entry, ctx.sidecar, ctx.repo_root, location=entry_loc))
        findings.extend(check_b3(ctx.sidecar, ctx.repo_root, location=sidecar_loc))
        findings.extend(check_b4(ctx.sidecar, ctx.repo_root, location=sidecar_loc))
        findings.extend(check_b5(ctx.sidecar, location=sidecar_loc))
    findings.extend(check_b6(ctx.sidecar, ctx.verdict, location=sidecar_loc))
    if not is_audit_failed:
        findings.extend(check_b7(ctx.entry, ctx.sidecar, ctx.entry_path, ctx.sidecar_path,
                                  ctx.jsonl_path, ctx.verdict_path, mode, location=entry_loc,
                                  repo_root=ctx.repo_root, verdict=ctx.verdict))
    findings.extend(check_b8(ctx.entry, mode, location=entry_loc))
    findings.extend(check_b9(ctx.entry, ctx.sidecar, location=entry_loc))
    findings.extend(check_b10(ctx.entry, ctx.verdict, mode, location=entry_loc))

    # Family C
    findings.extend(check_c1(ctx.entry, ctx.verdict, location=entry_loc))
    findings.extend(check_c2(ctx.entry, ctx.sidecar, location=entry_loc))
    # C3 needs prior_entry (passport scan) — skipped in single-entry mode unless
    # the caller passes a passport. For ack entries we'd compare against the latest
    # MATERIAL non-ack entry of the same (stage, agent, deliverable_sha).
    if mode == "persisted" and ctx.passport_audit_artifacts is not None and ctx.entry is not None:
        if "acknowledgement" in ctx.entry:
            prior = _find_latest_material_entry_for_ack(
                ctx.passport_audit_artifacts, ctx.entry)
            if prior is None:
                # Codex round 5 P1 closure: an ack entry without a prior
                # MATERIAL entry of the same (stage, agent, deliverable_sha,
                # run_id) tuple violates C3's copy contract by construction
                # — there is nothing to copy from. A standalone ack or one
                # whose copied fields were altered to break the tuple match
                # would silently pass C3 if `prior is None` skipped the
                # check. Surface as C3 finding.
                findings.append(LintError(
                    "C3",
                    f"acknowledgement entry has no prior MATERIAL entry to copy "
                    f"from: no passport entry matches "
                    f"(stage={ctx.entry.get('stage')!r}, "
                    f"agent={ctx.entry.get('agent')!r}, "
                    f"deliverable_sha={ctx.entry.get('deliverable_sha')!r}, "
                    f"run_id={ctx.entry.get('run_id')!r}) — §5.4 ack mechanism "
                    f"requires the prior MATERIAL entry to exist before append",
                    entry_loc,
                ))
            else:
                findings.extend(check_c3(ctx.entry, prior, location=entry_loc))
    findings.extend(check_c4(ctx.entry, ctx.sidecar, location=entry_loc))

    # Family D
    if ctx.passport_audit_artifacts is not None:
        findings.extend(check_d1(ctx.passport_audit_artifacts, location=str(ctx.passport_path or "<passport>")))
        findings.extend(check_d3(ctx.passport_audit_artifacts, location=str(ctx.passport_path or "<passport>")))
        findings.extend(check_e1_e2_e6(ctx.passport_audit_artifacts, location=str(ctx.passport_path or "<passport>")))

    # Codex round 13 P2 closure: D2/D4 supersession is only meaningful in
    # persisted mode (proposal mode is itself the unmerged proposal). When
    # --mode persisted runs with --output-dir present, scan the dir for
    # OTHER unmerged proposal entries matching the same (stage, agent,
    # deliverable_sha) tuple, then run:
    #   - D2: detect ambiguous proposal selection (proposals sharing
    #     started_at where run_id lex-max would be the only tie-breaker)
    #   - D4: detect supersession requirement — a higher-round unmerged
    #     proposal preempts the persisted entry's Path A selection
    if mode == "persisted" and ctx.output_dir is not None and ctx.output_dir.is_dir() and ctx.entry is not None:
        proposals = _scan_unmerged_proposals(ctx.output_dir, ctx.entry,
                                              exclude_path=ctx.entry_path)
        if proposals:
            findings.extend(check_d2(proposals, location=str(ctx.output_dir)))
            persisted_round = _safe_get(ctx.entry, "verdict", "round")
            for p in proposals:
                proposal_round = _safe_get(p, "entry", "verdict", "round")
                findings.extend(check_d4(
                    persisted_round if isinstance(persisted_round, int) else None,
                    proposal_round if isinstance(proposal_round, int) else None,
                    location=str(p.get("entry_path") or "<proposal-entry>"),
                ))

    # Family E
    findings.extend(check_e3_e4(ctx.entry, mode, location=entry_loc))
    findings.extend(check_e5(ctx.entry, mode, location=entry_loc))
    findings.extend(check_e7(ctx.entry, location=entry_loc))

    # Family F
    if ctx.entry is not None:
        findings.extend(check_f1(ctx.entry.get("run_id"), location=entry_loc))
    findings.extend(check_f2(ctx.jsonl_path, ctx.sidecar_path, ctx.verdict_path,
                              ctx.entry_path, mode, location=entry_loc))
    findings.extend(check_f3(ctx.sidecar, ctx.sidecar_path, location=sidecar_loc))

    return findings


def _find_latest_material_entry_for_ack(
    artifacts: list[dict[str, Any]], ack_entry: dict[str, Any]
) -> dict[str, Any] | None:
    """Find the prior MATERIAL entry (no acknowledgement) matching the ack
    entry's (stage, agent, deliverable_sha, run_id) tuple, latest by verified_at."""
    key = (ack_entry.get("stage"), ack_entry.get("agent"),
           ack_entry.get("deliverable_sha"), ack_entry.get("run_id"))
    candidates = []
    for e in artifacts:
        if not isinstance(e, dict):
            continue
        if "acknowledgement" in e:
            continue
        if (e.get("stage"), e.get("agent"), e.get("deliverable_sha"),
                e.get("run_id")) != key:
            continue
        if _safe_get(e, "verdict", "status") != "MATERIAL":
            continue
        candidates.append(e)
    if not candidates:
        return None
    return max(candidates, key=lambda e: _safe_get(e, "verdict", "verified_at") or "")


def _scan_unmerged_proposals(
    output_dir: Path, persisted_entry: dict[str, Any],
    exclude_path: Path | None = None,
) -> list[dict[str, Any]]:
    """Scan output_dir for unmerged proposal entries matching the persisted
    entry's (stage, agent, deliverable_sha) tuple.

    `exclude_path` is the persisted entry's own path (when present in
    output_dir, e.g. fixture smoke tests where the persisted entry hasn't
    been moved to consumed/ yet) — exclude it so we don't compare an
    entry against itself.

    Returns a list of dicts shaped {entry: <parsed entry>, sidecar: <parsed
    sidecar>, entry_path: <Path>} so D2/D4 callers can read both sides
    (entry has verdict.round; sidecar has timing.started_at).
    Errors loading any single proposal are silently skipped — D2/D4 are
    advisory checks; SCHEMA findings on those files would already fire
    via validate_against_schema if they were the target of --mode
    proposal in a separate invocation.
    """
    key = (persisted_entry.get("stage"), persisted_entry.get("agent"),
           persisted_entry.get("deliverable_sha"))
    proposals: list[dict[str, Any]] = []
    try:
        candidates = sorted(output_dir.glob("*.audit_artifact_entry.json"))
    except OSError:
        return proposals
    exclude_resolved = exclude_path.resolve() if exclude_path is not None else None
    for entry_path in candidates:
        if exclude_resolved is not None:
            try:
                if entry_path.resolve() == exclude_resolved:
                    continue
            except OSError:
                pass
        try:
            entry_data = json.loads(entry_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(entry_data, dict):
            continue
        # Proposal arm: no verified_at / verified_by
        verdict = entry_data.get("verdict") or {}
        if "verified_at" in verdict or "verified_by" in verdict:
            continue
        if (entry_data.get("stage"), entry_data.get("agent"),
                entry_data.get("deliverable_sha")) != key:
            continue
        # Try to load companion sidecar (for D2 started_at)
        sidecar_path = entry_path.parent / entry_path.name.replace(
            ".audit_artifact_entry.json", ".meta.json")
        sidecar_data: dict[str, Any] = {}
        if sidecar_path.exists():
            try:
                sidecar_data = _load_yaml_or_json(sidecar_path)
                if not isinstance(sidecar_data, dict):
                    sidecar_data = {}
            except Exception:
                sidecar_data = {}
        proposals.append({
            "entry": entry_data,
            "sidecar": sidecar_data,
            "entry_path": entry_path,
        })
    return proposals


# ---------------------------------------------------------------------------
# Schema validation (defense in depth — re-run schemas at lint time)
# ---------------------------------------------------------------------------


def validate_against_schema(doc: Any, schema_path: Path) -> list[LintError]:
    """Validate a document against a JSON Schema; return findings (one per error)."""
    try:
        from jsonschema import Draft202012Validator
        with schema_path.open("r", encoding="utf-8") as f:
            schema = json.load(f)
        validator = Draft202012Validator(
            schema, format_checker=Draft202012Validator.FORMAT_CHECKER
        )
        out: list[LintError] = []
        for err in validator.iter_errors(doc):
            out.append(LintError("SCHEMA",
                f"{err.message} (path={list(err.absolute_path)})",
                str(schema_path.name)))
        return out
    except Exception as e:  # pragma: no cover
        return [LintError("SCHEMA", f"validator error: {e}", str(schema_path.name))]


# ---------------------------------------------------------------------------
# §3.7 F4 example-validation harness
# ---------------------------------------------------------------------------


def run_example_harness(repo_root: Path) -> list[LintError]:
    """F4 — walk docs/design/*.md, find code-fenced example payloads, validate
    against the appropriate schema. Any spec drift emerges as findings.

    We look for fenced blocks marked ```yaml / ```json / ```jsonl. For each
    block, we apply heuristics: if it contains 'verdict_status:' it's a verdict
    file; 'audit_artifact:' is a Schema 9 list of entries; 'codex_cli_version:'
    is a sidecar; first event 'thread.started' is a JSONL stream.
    """
    findings: list[LintError] = []
    design_dir = repo_root / "docs/design"
    if not design_dir.exists():
        return [LintError("F4", f"docs/design not found at {design_dir}", str(design_dir))]

    fence_re = re.compile(r"^```(\w+)?\s*$")
    for md_path in sorted(design_dir.glob("*.md")):
        try:
            text = md_path.read_text(encoding="utf-8")
        except OSError as e:
            findings.append(LintError("F4", f"cannot read: {e}", str(md_path)))
            continue
        lines = text.splitlines()
        in_fence = False
        fence_lang = None
        fence_start = 0
        buffer: list[str] = []
        for lineno, line in enumerate(lines, start=1):
            m = fence_re.match(line)
            if m:
                if not in_fence:
                    in_fence = True
                    fence_lang = (m.group(1) or "").lower()
                    fence_start = lineno
                    buffer = []
                else:
                    block = "\n".join(buffer)
                    findings.extend(_classify_and_validate_block(
                        block, fence_lang, md_path, fence_start))
                    in_fence = False
                    fence_lang = None
                    buffer = []
            elif in_fence:
                buffer.append(line)
    return findings


def _classify_and_validate_block(
    block: str, lang: str | None, md_path: Path, fence_start: int
) -> list[LintError]:
    """Heuristically classify a fenced block and validate against the right schema."""
    out: list[LintError] = []
    location = f"{md_path}:{fence_start}"
    stripped = block.strip()
    if not stripped:
        return []

    # JSONL detection — multiple lines each starting with `{"type":`
    looks_like_jsonl = (
        ("\n" in stripped) and all(
            s.strip().startswith("{") for s in stripped.splitlines() if s.strip()
        )
    )
    # heuristic guard: at least one line looks like a JSON object with a "type" field
    if looks_like_jsonl and ('"type":"thread.started"' in stripped or
                             '"type":"turn.started"' in stripped or
                             '"type":"item.completed"' in stripped):
        # Validate each line against jsonl schema
        try:
            with JSONL_SCHEMA_PATH.open("r", encoding="utf-8") as fh:
                jsonl_schema = json.load(fh)
            from jsonschema import Draft202012Validator
            validator = Draft202012Validator(
                jsonl_schema, format_checker=Draft202012Validator.FORMAT_CHECKER
            )
            for ln_idx, line in enumerate(stripped.splitlines(), start=fence_start + 1):
                line = line.strip()
                if not line:
                    continue
                # Skip ellipsis-only schematic rows from the spec, e.g.
                # `..."input_tokens":...,...`
                if "..." in line:
                    # Mark as "schematic, not validated" if it contains literal '...'
                    out.append(LintError("F4",
                        f"schematic JSONL line contains '...' placeholder (skipped from validation)",
                        f"{md_path}:{ln_idx}",
                        severity="info"))
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as e:
                    out.append(LintError("F4",
                        f"invalid JSON in fenced JSONL: {e}",
                        f"{md_path}:{ln_idx}"))
                    continue
                for err in validator.iter_errors(row):
                    out.append(LintError("F4",
                        f"jsonl row drift from schema: {err.message}",
                        f"{md_path}:{ln_idx}"))
        except Exception as e:  # pragma: no cover
            out.append(LintError("F4", f"jsonl harness error: {e}", location))
        return out

    if lang == "yaml":
        # Cheap pre-filter: only parse blocks that LOOK like audit artifacts.
        # The harness's job is to surface drift in §3.1/§3.3/§3.4/§3.5
        # examples, not lint every YAML fence in every design doc.
        audit_signature_keys = (
            "audit_artifact:", "verdict_status:", "codex_cli_version:",
            "primary_deliverables:", "audit_template_path:",
        )
        if not any(sig in stripped for sig in audit_signature_keys):
            return out
        # parse as YAML — use timestamp-as-string loader so we don't double-flag
        # `2026-04-30T15:22:04.123Z` as a YAML datetime object (schema needs str).
        try:
            doc = yaml.load(stripped, Loader=_StrTimestampSafeLoader)
        except yaml.YAMLError as e:
            out.append(LintError("F4", f"yaml parse error: {e}", location))
            return out
        if not isinstance(doc, dict):
            return out
        # Classify
        if "verdict_status" in doc:
            # verdict file
            out.extend([_relabel(f, "F4") for f in
                        validate_against_schema(doc, VERDICT_SCHEMA_PATH)])
            out[-len(out) or 0:] = [_with_location(f, location) for f in out[-len(out) or 0:]]
        elif "codex_cli_version" in doc:
            # sidecar — but note this section may have hyphen drift in timestamps
            out.extend([_with_location(_relabel(f, "F4"), location) for f in
                        validate_against_schema(doc, SIDECAR_SCHEMA_PATH)])
        elif "audit_artifact" in doc:
            # Schema 9 list of persisted entries
            entries = doc.get("audit_artifact") or []
            if isinstance(entries, list):
                for idx, e in enumerate(entries):
                    if isinstance(e, dict):
                        loc = f"{location}:audit_artifact[{idx}]"
                        out.extend([_with_location(_relabel(f, "F4"), loc) for f in
                                    validate_against_schema(e, ENTRY_SCHEMA_PATH)])
        elif {"stage", "agent", "deliverable_path", "run_id"} <= set(doc.keys()):
            # bare entry block
            out.extend([_with_location(_relabel(f, "F4"), location) for f in
                        validate_against_schema(doc, ENTRY_SCHEMA_PATH)])
        return out

    if lang == "json":
        try:
            doc = json.loads(stripped)
        except json.JSONDecodeError:
            return out
        if not isinstance(doc, dict):
            return out
        # Same classification
        if "verdict_status" in doc:
            out.extend([_with_location(_relabel(f, "F4"), location) for f in
                        validate_against_schema(doc, VERDICT_SCHEMA_PATH)])
        elif "codex_cli_version" in doc:
            out.extend([_with_location(_relabel(f, "F4"), location) for f in
                        validate_against_schema(doc, SIDECAR_SCHEMA_PATH)])
        elif {"stage", "agent", "deliverable_path", "run_id"} <= set(doc.keys()):
            out.extend([_with_location(_relabel(f, "F4"), location) for f in
                        validate_against_schema(doc, ENTRY_SCHEMA_PATH)])
        return out

    return out


def _relabel(f: LintError, rule_id: str) -> LintError:
    return LintError(rule_id, f.message, f.location)


def _with_location(f: LintError, location: str) -> LintError:
    return LintError(f.rule_id, f.message, location)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


class _ExUsageParser(argparse.ArgumentParser):
    """ArgumentParser subclass enforcing the EX_USAGE=64 contract.

    Codex round 4 P3 closure: stock argparse calls sys.exit(2) on any
    parser-level failure (invalid --mode value, unknown option, missing
    required arg). The CLI contract documented at the top of this module
    promises 64 EX_USAGE for every bad-CLI-arg case. Override .error() so
    the exit code matches the contract.
    """

    def error(self, message: str) -> None:  # type: ignore[override]
        self.print_usage(sys.stderr)
        print(f"{self.prog}: error: {message}", file=sys.stderr)
        sys.exit(64)


def _build_parser() -> argparse.ArgumentParser:
    p = _ExUsageParser(
        description="Lint audit-artifact contract per ARS v3.6.7 §3.7 invariants.")
    p.add_argument("--mode", choices=("proposal", "persisted", "jsonl-stream"))
    p.add_argument("--example-validation-harness", action="store_true",
                   help="Walk docs/design/*.md and validate fenced example payloads.")
    p.add_argument("--entry", type=Path,
                   help="Path to entry JSON (proposal or persisted).")
    p.add_argument("--sidecar", type=Path,
                   help="Path to sidecar .meta.json. Auto-discovered via run_id when --output-dir given.")
    p.add_argument("--verdict", type=Path,
                   help="Path to verdict .verdict.yaml. Auto-discovered.")
    p.add_argument("--jsonl", type=Path,
                   help="Path to JSONL file. Auto-discovered, or explicitly required by jsonl-stream mode.")
    p.add_argument("--output-dir", type=Path,
                   help="Directory containing the four artifact files (used for auto-discovery).")
    p.add_argument("--passport-path", type=Path,
                   help="Passport YAML/JSON. Enables D1/D3/E2/E6 ledger checks.")
    p.add_argument("--run-id", type=str,
                   help="Used with --output-dir for auto-discovery.")
    p.add_argument("--repo-root", type=Path, default=REPO_ROOT,
                   help="Repo root for B2/B3/B4 disk verification.")
    return p


def _autodiscover(output_dir: Path | None, run_id: str | None,
                  jsonl: Path | None, sidecar: Path | None,
                  verdict: Path | None, entry: Path | None,
                  mode: str) -> tuple[Path | None, Path | None, Path | None, Path | None]:
    """Fill missing artifact paths from --output-dir + --run-id."""
    if output_dir is None:
        return jsonl, sidecar, verdict, entry
    if run_id is None and entry is not None and entry.exists():
        # peek run_id from entry
        try:
            data = json.loads(entry.read_text(encoding="utf-8"))
            run_id = data.get("run_id")
        except Exception:
            pass
    if run_id is None:
        return jsonl, sidecar, verdict, entry
    if jsonl is None:
        jsonl = output_dir / f"{run_id}.jsonl"
    if sidecar is None:
        sidecar = output_dir / f"{run_id}.meta.json"
    if verdict is None:
        verdict = output_dir / f"{run_id}.verdict.yaml"
    if entry is None:
        # Persisted mode entry files are conventionally moved to consumed/
        # at §4.9 step 9, but the CLI must still be able to read an entry
        # the caller has on disk. Default to the bare-run_id name; if not
        # found, fall back to consumed/<run_id>.audit_artifact_entry.json.
        candidate = output_dir / f"{run_id}.audit_artifact_entry.json"
        consumed = output_dir / "consumed" / f"{run_id}.audit_artifact_entry.json"
        if candidate.exists():
            entry = candidate
        elif consumed.exists():
            entry = consumed
        else:
            entry = candidate  # report the missing path in the loader error
    return jsonl, sidecar, verdict, entry


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    # Harness mode
    if args.example_validation_harness:
        repo_root = args.repo_root or REPO_ROOT
        findings = run_example_harness(repo_root)
        for f in findings:
            print(f.render())
        # Only error-severity findings drive a non-zero exit. Info findings
        # (e.g., schematic '...' placeholders the harness intentionally skips)
        # are surfaced but don't fail the run.
        return 1 if any(f.severity == "error" for f in findings) else 0

    if args.mode is None:
        # Phase 6.1 EX_USAGE convention is exit 64. argparse's parser.error()
        # calls sys.exit(2), which would silently downgrade our usage errors;
        # print + return 64 keeps the exit-code contract aligned with
        # scripts/audit_snapshot.py and scripts/run_codex_audit.sh.
        print("ERROR: either --mode or --example-validation-harness is required",
              file=sys.stderr)
        return 64

    # jsonl-stream mode — orchestrator §5.2 L2-5 invocation
    if args.mode == "jsonl-stream":
        if args.jsonl is None:
            print("ERROR: --mode jsonl-stream requires --jsonl", file=sys.stderr)
            return 64
        if not args.jsonl.exists():
            print(f"ERROR: jsonl not found: {args.jsonl}", file=sys.stderr)
            return 2
        try:
            events = _load_jsonl(args.jsonl)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2
        ctx = LintContext(mode="jsonl-stream", jsonl_events=events,
                          jsonl_path=args.jsonl, repo_root=args.repo_root or REPO_ROOT)
        findings = run_checks(ctx)
        # Per spec §5.2 L2-5 the orchestrator wants the offending item.id and
        # reason on stderr when pairing fails. We mirror to stdout too so the
        # CLI output is grep-friendly in interactive use.
        for f in findings:
            print(f.render())
            print(f.render(), file=sys.stderr)
        return 1 if any(f.severity == "error" for f in findings) else 0

    # proposal / persisted modes
    jsonl, sidecar, verdict, entry = _autodiscover(
        args.output_dir, args.run_id, args.jsonl, args.sidecar,
        args.verdict, args.entry, args.mode,
    )

    if entry is None:
        print(
            f"ERROR: --mode {args.mode} requires --entry (or --output-dir + --run-id)",
            file=sys.stderr,
        )
        return 64

    try:
        entry_data = json.loads(entry.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot load entry {entry}: {e}", file=sys.stderr)
        return 2

    # Codex round 5 traceback closure: a non-object entry payload (caller
    # passed `[]` / a scalar / null) would crash check_e3_e4 with
    # AttributeError on `entry.get(...)`. Surface as a SCHEMA finding
    # instead — schema validation below would also catch it, but bailing
    # early avoids the cross-field rules running on a non-dict and
    # producing tracebacks before the schema finding is rendered.
    if not isinstance(entry_data, dict):
        print(
            f"ERROR: entry {entry} is not a JSON object "
            f"(got {type(entry_data).__name__}); audit_artifact_entry must be "
            "an object per audit_artifact_entry.schema.json",
            file=sys.stderr,
        )
        return 2

    # Schema validation on the entry first (defense in depth — the oneOf
    # proposal/persisted arms enforce verified_at presence + AUDIT_FAILED
    # exclusion at this layer, before any cross-field rule fires).
    schema_findings: list[LintError] = list(
        validate_against_schema(entry_data, ENTRY_SCHEMA_PATH)
    )

    # Codex round 2 P1 closure: --mode persisted MUST enforce the persisted
    # oneOf arm specifically. JSON Schema oneOf accepts EITHER arm by
    # construction, so a proposal-shaped entry (no verified_at, no
    # verified_by, possibly AUDIT_FAILED status) would silently pass
    # `--mode persisted`. The mode flag is the lifecycle assertion the
    # caller is making about the entry; the lint must enforce it.
    # E3/E4 are the spec rules for proposal-mode rejection of orchestrator
    # fields; the symmetric rule for persisted mode lives here.
    verdict_block = entry_data.get("verdict") if isinstance(entry_data, dict) else None
    if isinstance(verdict_block, dict):
        if args.mode == "persisted":
            # persisted arm requires verified_at + verified_by, forbids AUDIT_FAILED
            if "verified_at" not in verdict_block:
                schema_findings.append(LintError(
                    "E3", "--mode persisted: entry.verdict.verified_at is required "
                          "(entry has proposal-arm shape; orchestrator-side fields missing)",
                    str(entry)))
            if "verified_by" not in verdict_block:
                schema_findings.append(LintError(
                    "E3", "--mode persisted: entry.verdict.verified_by is required "
                          "(entry has proposal-arm shape; orchestrator-side fields missing)",
                    str(entry)))
            if verdict_block.get("status") == "AUDIT_FAILED":
                schema_findings.append(LintError(
                    "E5", "--mode persisted: entry.verdict.status='AUDIT_FAILED' is "
                          "forbidden (AUDIT_FAILED entries are proposal-arm only per "
                          "§3.2 lifecycle-conditional table)",
                    str(entry)))
        elif args.mode == "proposal":
            # proposal arm forbids verified_at + verified_by + acknowledgement
            if "verified_at" in verdict_block:
                schema_findings.append(LintError(
                    "E4", "--mode proposal: entry.verdict.verified_at must be absent "
                          "(orchestrator-only field; wrapper-emitted proposal carrying it "
                          "is Pattern C3 attack surface)",
                    str(entry)))
            if "verified_by" in verdict_block:
                schema_findings.append(LintError(
                    "E4", "--mode proposal: entry.verdict.verified_by must be absent "
                          "(orchestrator-only field; Pattern C3 attack surface)",
                    str(entry)))
            if "acknowledgement" in entry_data:
                schema_findings.append(LintError(
                    "A4", "--mode proposal: entry.acknowledgement must be absent "
                          "(orchestrator-only write per §5.4)",
                    str(entry)))

    # Companion artifacts (sidecar + verdict + jsonl) are REQUIRED in
    # Codex round 16 P2 closure: spec §5.2 says the orchestrator follows
    # entry.artifact_paths, so when caller only passes `--entry` (and a
    # `--repo-root`), fall back to those declared paths to locate the
    # JSONL/sidecar/verdict before emitting "missing companion" errors.
    # The B7 path-resolution check (round 8) still verifies these match
    # the recorded paths; this just removes the ergonomic gap that
    # required redundant flags for a passport/proposal entry that
    # already declares its own artifact bundle.
    artifact_paths = entry_data.get("artifact_paths") if isinstance(entry_data, dict) else None
    if isinstance(artifact_paths, dict):
        repo_root = args.repo_root or REPO_ROOT
        if jsonl is None:
            recorded = artifact_paths.get("jsonl")
            if isinstance(recorded, str) and recorded:
                jsonl = (repo_root / recorded).resolve()
        if sidecar is None:
            recorded = artifact_paths.get("sidecar")
            if isinstance(recorded, str) and recorded:
                sidecar = (repo_root / recorded).resolve()
        if verdict is None:
            recorded = artifact_paths.get("verdict")
            if isinstance(recorded, str) and recorded:
                verdict = (repo_root / recorded).resolve()

    # proposal/persisted modes — they ARE the Layer 2/3 evidence Phase 6.3
    # is supposed to gate (codex round 1 P1: silently treating missing
    # files as None let valid-looking entries return exit 0 with no audit
    # evidence). When auto-discovered or explicitly given path doesn't
    # exist, surface as an artifact-incomplete finding (B7 family — the
    # bundle is supposed to be complete by §4.9 step 9).
    def _missing_companion(role: str, path: Path | None) -> None:
        if path is None:
            schema_findings.append(LintError(
                "B7",
                f"audit bundle missing {role} (auto-discover failed and no explicit "
                f"--{role} given) — proposal/persisted mode requires {role} for "
                f"Layer 2/3 verification",
                f"<{args.mode}>",
            ))
        elif not path.exists():
            schema_findings.append(LintError(
                "B7",
                f"audit bundle missing {role} at {path} — proposal/persisted mode "
                f"requires {role} for Layer 2/3 verification",
                str(path),
            ))

    _missing_companion("sidecar", sidecar)
    _missing_companion("verdict", verdict)
    _missing_companion("jsonl", jsonl)

    sidecar_data = None
    if sidecar is not None and sidecar.exists():
        try:
            sidecar_data = _load_yaml_or_json(sidecar)
        except Exception as e:
            print(f"ERROR: cannot load sidecar {sidecar}: {e}", file=sys.stderr)
            return 2
        # Codex round 6 P2 closure: a non-object companion artifact (e.g.,
        # `[]` parsed as YAML) records a SCHEMA finding via
        # validate_against_schema but `.get(...)` calls in cross-field
        # checks would still raise AttributeError before the finding
        # renders. Coerce non-dict to None so cross-field rules see "no
        # companion" and skip cleanly; the SCHEMA finding still surfaces
        # the rejection and exit code remains 1.
        schema_findings.extend(
            validate_against_schema(sidecar_data, SIDECAR_SCHEMA_PATH)
        )
        if not isinstance(sidecar_data, dict):
            sidecar_data = None

    verdict_data = None
    if verdict is not None and verdict.exists():
        try:
            verdict_data = _load_yaml_or_json(verdict)
        except Exception as e:
            print(f"ERROR: cannot load verdict {verdict}: {e}", file=sys.stderr)
            return 2
        schema_findings.extend(
            validate_against_schema(verdict_data, VERDICT_SCHEMA_PATH)
        )
        if not isinstance(verdict_data, dict):
            verdict_data = None

    events = None
    if jsonl is not None and jsonl.exists():
        # Codex round 11 P2 closure: AUDIT_FAILED bundles can have a
        # partial / non-JSON line at the end (codex was SIGKILL'd
        # mid-write); _load_jsonl() raises ValueError on those, returning
        # exit 2 as internal error and contradicting the round-9 schema
        # suspension immediately below. Decide on AUDIT_FAILED before
        # _load_jsonl runs so failure-signaling proposals with
        # partially-written streams are handled cleanly.
        verdict_status_for_jsonl = (
            verdict_data.get("verdict_status") if isinstance(verdict_data, dict) else None
        )
        if verdict_status_for_jsonl == "AUDIT_FAILED":
            # Skip per-row schema validation entirely; A7 / stream-shape
            # are also suspended in run_checks. Best-effort load still
            # populates events for the entry-side family A rules that
            # don't depend on stream completeness — but a hard parse
            # failure is acceptable evidence of "audit was killed mid-
            # write" rather than a lint-blocking error.
            try:
                events = _load_jsonl(jsonl)
            except ValueError:
                events = None  # forensic-only bundle; stream is unparseable
        else:
            try:
                events = _load_jsonl(jsonl)
            except ValueError as e:
                print(f"ERROR: cannot load jsonl {jsonl}: {e}", file=sys.stderr)
                return 2
            # Validate every JSONL row against the per-row schema. Stream-shape
            # rules (A7 + parse_audit_verdict.py probe-style stream invariants)
            # run separately in the family A check; the per-row schema gate
            # ensures malformed rows don't reach those stream checks.
            for row_idx, row in enumerate(events, start=1):
                schema_findings.extend([
                    LintError(err.rule_id, err.message,
                              f"{jsonl}:row={row_idx}")
                    for err in validate_against_schema(row, JSONL_SCHEMA_PATH)
                ])

    passport_audit_artifacts = None
    if args.passport_path is not None and args.passport_path.exists():
        try:
            passport_data = _load_yaml_or_json(args.passport_path)
            if isinstance(passport_data, dict):
                aa = passport_data.get("audit_artifact")
                if isinstance(aa, list):
                    passport_audit_artifacts = aa
        except Exception as e:
            print(f"ERROR: cannot load passport {args.passport_path}: {e}", file=sys.stderr)
            return 2

    ctx = LintContext(
        mode=args.mode,
        entry=entry_data, entry_path=entry,
        sidecar=sidecar_data, sidecar_path=sidecar,
        verdict=verdict_data, verdict_path=verdict,
        jsonl_events=events, jsonl_path=jsonl,
        output_dir=args.output_dir,
        passport_audit_artifacts=passport_audit_artifacts,
        passport_path=args.passport_path,
        repo_root=args.repo_root or REPO_ROOT,
    )

    # Codex round 12 P2 closure: when any schema-level finding fires, we
    # must NOT proceed into run_checks. Cross-field rules call .get() /
    # set() on nested fields assuming the schema-defined types — a value
    # that satisfies the top-level isinstance(dict) check (added round 5/6)
    # but has a malformed nested field (e.g. timing: [1] satisfies dict at
    # the root but timing.get(...) crashes; finding_ids: [{}] satisfies
    # array but `set(finding_ids)` crashes building a set of unhashable
    # dicts) would trace back instead of producing the documented lint
    # rejection. Short-circuit on any error-severity SCHEMA finding —
    # the schema rejection is itself the lint result; the cross-field
    # rules have nothing to add when the input doesn't match the schema
    # contract they presuppose.
    has_schema_error = any(
        f.rule_id == "SCHEMA" and f.severity == "error" for f in schema_findings
    )
    if has_schema_error:
        for f in schema_findings:
            print(f.render())
        return 1

    findings = schema_findings + run_checks(ctx)
    for f in findings:
        print(f.render())
    return 1 if any(f.severity == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
<!-- SOURCE-CONTENT-END -->
