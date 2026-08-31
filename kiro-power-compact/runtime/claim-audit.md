<a id="source-docs-design-2026-05-15-issue-103-claim-alignment-audit-spec-md"></a>

## SOURCE: docs/design/2026-05-15-issue-103-claim-alignment-audit-spec.md

<!-- SOURCE-CONTENT-BEGIN bytes=84545 -->
# ARS v3.8 — Issue #103 `claim_ref_alignment_audit_agent` Implementation Spec

**Date:** 2026-05-15
**Issue:** [#103](https://github.com/Imbad0202/academic-research-skills/issues/103)
**Companion decision doc:** `2026-05-15-issue-103-claim-alignment-audit-decision.md`
**Target release:** v3.8

This spec implements the eight decisions in the companion decision doc. Read the decision doc first — it carries the load-bearing reasons; this spec carries the executable surface.

---

## 1. In-scope deliverables

Numbered list aligned to the implementation surfaces in #103 issue body + decision-doc adjustments.

1. **`academic-pipeline/agents/claim_ref_alignment_audit_agent.md`** — new agent prompt. Estimated 350-500 lines.
2. **`shared/contracts/passport/claim_audit_result.schema.json`** — per-claim audit result entry schema (judge-evaluated citation-bound findings).
3. **`shared/contracts/passport/claim_intent_manifest.schema.json`** — per-agent-invocation manifest entry schema.
3a. **`shared/contracts/passport/uncited_assertion.schema.json`** — per uncited-sentence finding entry schema (separate from `claim_audit_result` because there's no `ref_slug` to bind).
3b. **`shared/contracts/passport/claim_drift.schema.json`** — per claim-intent-drift finding entry schema (separate from `claim_audit_result` because drift is detected by manifest set-diff, not by judge invocation; see §3.4 rationale).
3c. **`shared/contracts/passport/constraint_violation.schema.json`** — per uncited-claim-violates-constraint finding entry schema (separate from `claim_audit_result` because no `ref_slug` exists, but HIGH-WARN gate-refuse semantics differ from LOW-WARN `uncited_assertion`; see §3.5 rationale).
4. **`academic-pipeline/agents/pipeline_orchestrator_agent.md`** — new §3.6 "Claim-Faithfulness Audit Gate (v3.8)". Dispatch wiring for the new agent. Finalizer integration extended to 8-row + advisory tier.
5. **`academic-paper/agents/formatter_agent.md`** — Cite-Time Provenance Hard Gate extended with FIVE new HIGH-WARN refusal classes mirroring §5 finalizer matrix (8-row matrix + constraint_violations[] aggregate): HIGH-WARN-CLAIM-NOT-SUPPORTED, HIGH-WARN-NEGATIVE-CONSTRAINT-VIOLATION, HIGH-WARN-FABRICATED-REFERENCE, HIGH-WARN-CLAIM-AUDIT-ANCHORLESS, HIGH-WARN-CONSTRAINT-VIOLATION-UNCITED. The formatter's existing v3.7.1/v3.7.3 refusal rules remain unchanged; new classes append to the existing REFUSE list. §5 matrix + constraint_violations[] are the source of truth — any new HIGH-WARN class added in future revisions MUST be mirrored here, enforced by a §6 lint rule.
6. **`academic-paper/agents/draft_writer_agent.md`** + **`deep-research/agents/synthesis_agent.md`** + **`deep-research/agents/report_compiler_agent.md`** — new "Claim Intent Manifest Emission (v3.8)" sibling heading following the existing v3.7.3 "Three-Layer Citation Emission" heading. PATTERN PROTECTION (v3.6.7) blocks stay byte-equivalent.
7. **`academic-pipeline/references/claim_audit_calibration_protocol.md`** — new file (modeled on `shared/contracts/reviewer/` calibration convention).
8. **`scripts/check_claim_audit_consistency.py`** — new lint enforcing per-claim invariants (anchor presence, defect_stage presence, precedence rules, audit_status/defect_stage coherence).
9. **CI wiring** — extend `.github/workflows/spec-consistency.yml` (or matching workflow) to call the new lint.
10. **Tests** — `scripts/test_claim_audit_schema.py` covers both schema validation and `check_claim_audit_consistency.py` lint coverage via subprocess pattern (T-S1..T-S8 invariants); plus per-stage unittest modules (`scripts/test_claim_audit_pipeline.py`, `scripts/test_uncited_assertion.py`, `scripts/test_claim_intent_manifest.py`, `scripts/test_claim_audit_finalizer.py`, `scripts/test_e2e_claim_audit.py` for the 5-citation end-to-end synthetic-paper test, `scripts/test_claim_audit_calibration.py`).
11. **CHANGELOG entry** + ROADMAP §3.8 anchor + decision-log entry.

## 2. Out of scope

Restated from decision doc §4, for cross-reference:

- RubricEM reflection meta-policy (post-v3.8)
- Evolving rubric buffer (post-v3.8)
- Rubric discrimination-power audit (→ #89)
- `defect_stage` accuracy measurement (→ #89 / gold fixtures)
- L3-2 contamination signals (→ #105 closed / #102 v3.7.4)
- Cross-paper claim-graph analysis (no issue yet; post-v3.8)

## 3. Schemas

### 3.1 `claim_audit_result.schema.json`

Per-claim audit result. One entry per audited citation in the passport `claim_audit_results[]` aggregate array.

**Required fields:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/claim_audit_result.schema.json",
  "title": "Material Passport Claim Audit Result Entry",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "claim_id",
    "scoped_manifest_id",
    "claim_text",
    "ref_slug",
    "anchor_kind",
    "anchor_value",
    "judgment",
    "audit_status",
    "defect_stage",
    "rationale",
    "judge_model",
    "judge_run_at",
    "ref_retrieval_method"
  ],
  "properties": {
    "claim_id": { "type": "string", "pattern": "^C-[0-9]{3,}$" },
    "scoped_manifest_id": {
      "type": "string",
      "pattern": "^M-[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z-[0-9a-f]{4}$",
      "description": "Points to the owning claim_intent_manifest.manifest_id. The (scoped_manifest_id, claim_id) pair uniquely identifies the claim, since C-001 may collide across manifests in the same run. Enforced by INV-15 (cross-array integrity). For audits running in MANIFEST-MISSING fallback (no manifest present), scoped_manifest_id is the sentinel `M-0000-00-00T00:00:00Z-0000`."
    },
    "claim_text": { "type": "string", "minLength": 1, "maxLength": 2000 },
    "ref_slug": { "type": "string", "minLength": 1 },
    "anchor_kind": { "enum": ["quote", "page", "section", "paragraph", "none"] },
    "anchor_value": { "type": "string" },
    "judgment": { "enum": ["SUPPORTED", "UNSUPPORTED", "AMBIGUOUS", "RETRIEVAL_FAILED"] },
    "audit_status": { "enum": ["completed", "inconclusive"] },
    "defect_stage": {
      "comment": "Three categories of finding are intentionally NOT defect_stages of claim_audit_result and use their own §3.3/§3.4/§3.5 entry-type schemas: (a) uncited_assertion findings — no ref_slug to evaluate, see uncited_assertion.schema.json (§3.3); (b) claim_intent drift findings — detected by manifest set-diff not by judge, see claim_drift.schema.json (§3.4) (drift never produces a claim_audit_result row because the judge is never invoked for these — the only signal is intended ≠ emitted manifest-set difference); (c) uncited constraint violations — claim has no ref_slug AND violates an MNC/NC rule, see constraint_violation.schema.json (§3.5) (HIGH-WARN gate-refuse but no ref to bind into a claim_audit_result row). 8 values listed below.",
      "enum": [
        "retrieval_existence",
        "metadata",
        "source_description",
        "citation_anchor",
        "synthesis_overclaim",
        "negative_constraint_violation",
        "not_applicable",
        null
      ]
    },
    "rationale": { "type": "string", "minLength": 1, "maxLength": 2000 },
    "judge_model": { "type": "string", "minLength": 1 },
    "judge_run_at": { "type": "string", "format": "date-time" },
    "ref_retrieval_method": { "enum": ["api", "manual_pdf", "failed", "not_attempted", "not_found", "audit_tool_failure"] },
    "upstream_owner_agent": {
      "enum": [
        "synthesis_agent",
        "draft_writer_agent",
        "report_compiler_agent",
        null
      ]
    },
    "violated_constraint_id": {
      "type": ["string", "null"],
      "pattern": "^(NC-C[0-9]{3,}-[0-9]+|MNC-[0-9]+)$"
    },
    "upstream_dispute": {
      "type": ["string", "null"],
      "maxLength": 1000
    },
    "audit_run_id": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z-[0-9a-f]{4}$"
    }
  }
}
```

**Allowed (`judgment`, `audit_status`, `defect_stage`) matrix (enforced in `check_claim_audit_consistency.py`, NOT in schema). Any combination outside the table is a lint violation:**

| `judgment` | `audit_status` | `defect_stage` | Notes |
|---|---|---|---|
| SUPPORTED | completed | `null` | INV-1 |
| AMBIGUOUS | completed | source_description, citation_anchor, synthesis_overclaim, or `null` | drift never AMBIGUOUS; constraints binary |
| UNSUPPORTED | completed | source_description | wrong paraphrase of source content |
| UNSUPPORTED | completed | metadata | reference exists but author/year/title wrong |
| UNSUPPORTED | completed | citation_anchor | source correct, anchor points to wrong passage |
| UNSUPPORTED | completed | synthesis_overclaim | source correct, draft over-strengthens claim |
| UNSUPPORTED | completed | negative_constraint_violation | INV-8, requires `violated_constraint_id` |
| RETRIEVAL_FAILED | completed | retrieval_existence | reference genuinely does not exist (fabricated) |
| RETRIEVAL_FAILED | inconclusive | not_applicable | covers (a) anchor=none INV-6 and (b) paywalled INV-10 |

**`uncited_assertion` is NOT a `claim_audit_result` row** — uncited claims have no `ref_slug` to populate the required field. They emit into a separate aggregate `uncited_assertions[]` (schema in §3.3 below) and feed the same Stage 4→5 finalizer integration. This sidesteps a schema-vs-required-field deadlock: `claim_audit_result.ref_slug` stays required for citation-bound audits; `uncited_assertions[]` carries its own entry-type schema with no `ref_slug` field.

**Cross-field invariants:**

- INV-1: `judgment=SUPPORTED` → `defect_stage=null` AND `violated_constraint_id=null` AND `audit_status=completed`
- INV-2: `judgment=UNSUPPORTED` → `defect_stage` ∈ `{source_description, metadata, citation_anchor, synthesis_overclaim, negative_constraint_violation}` AND `defect_stage ≠ null` AND `audit_status=completed` (claim_intent intentionally absent — drift detection is set-diff over manifest, never a judge verdict; drift findings emit into `claim_drifts[]` per §3.4, not into `claim_audit_results[]`)
- INV-3: `judgment=AMBIGUOUS` → `defect_stage` ∈ `{source_description, citation_anchor, synthesis_overclaim, null}` AND `audit_status=completed` (drift excluded — drift is unambiguous when manifest exists; metadata excluded — bibliographic correctness is binary; constraint violations excluded — INV-8 binary)
- INV-4: `judgment=RETRIEVAL_FAILED` AND `audit_status=inconclusive` → `defect_stage=not_applicable`
- INV-5: `judgment=RETRIEVAL_FAILED` AND `audit_status=completed` → `defect_stage=retrieval_existence` (reference genuinely does not exist, distinct from tool failure)
- INV-6: `anchor_kind=none` → `judgment=RETRIEVAL_FAILED`, `audit_status=inconclusive`, `defect_stage=not_applicable`, `ref_retrieval_method=not_attempted`, rationale begins with `v3.7.3 R-L3-1-A violation` (per D1)
- INV-7: `defect_stage=negative_constraint_violation` → `violated_constraint_id ≠ null`
- INV-8: `defect_stage=negative_constraint_violation` → `judgment=UNSUPPORTED` (one-way; negative-constraint violations are always classified UNSUPPORTED, never AMBIGUOUS — explicit author rules are binary. The converse does NOT hold: UNSUPPORTED admits 6 other defect_stages per INV-2.)
- INV-9: `upstream_dispute ≠ null` → `defect_stage ≠ null` AND `defect_stage ≠ not_applicable` (disputes are only meaningful for substantive defect classifications)
- INV-10: `ref_retrieval_method=failed` → `judgment=RETRIEVAL_FAILED` AND `audit_status=inconclusive` AND `defect_stage=not_applicable` (paywall path)
- INV-11: `ref_retrieval_method=not_attempted` ↔ `anchor_kind=none` AND INV-6 holds (anchor=none skips retrieval)
- INV-12: `ref_retrieval_method=not_found` ↔ `judgment=RETRIEVAL_FAILED` AND `audit_status=completed` AND `defect_stage=retrieval_existence` (fabricated reference path)
- INV-13: `defect_stage=metadata` → `judgment=UNSUPPORTED` AND `audit_status=completed` AND `ref_retrieval_method` ∈ `{api, manual_pdf}` (retrieval succeeded but metadata mismatch identified during judging)
- INV-14: `ref_retrieval_method=audit_tool_failure` ↔ `judgment=RETRIEVAL_FAILED` AND `audit_status=inconclusive` AND `defect_stage=not_applicable` AND rationale begins with a fault-class tag in `{judge_timeout, judge_api_error, judge_parse_error, cache_corruption, retrieval_api_error, retrieval_timeout, retrieval_network_error}` followed by a colon and free-form detail (audit-infrastructure / transient failure distinct from access-restricted retrieval; finalizer emits `[CLAIM-AUDIT-TOOL-FAILURE]` MED-WARN advisory; gate passes — retry-next-pass remediation. Discriminator from `ref_retrieval_method=failed`: permanence — paywall/license is stable, API 5xx/timeout is transient.)
- INV-15: For every `claim_audit_result` entry, `(scoped_manifest_id, claim_id)` MUST either (a) match some `claims[].claim_id` in the `claim_intent_manifests[]` entry whose `manifest_id == scoped_manifest_id`, or (b) carry the sentinel `scoped_manifest_id = M-0000-00-00T00:00:00Z-0000` indicating the MANIFEST-MISSING fallback path. Dangling references (scoped_manifest_id present but no matching manifest entry, with non-sentinel value) are a lint violation.
- INV-16: For every `claim_audit_result` entry with `anchor_kind ≠ none`, the URL-decoded `anchor_value` MUST be non-empty (after stripping leading/trailing whitespace). A stale or malformed marker like `<!--anchor:page:-->` would otherwise validate as an auditable locator and bypass the anchorless gate, but v3.7.3 §3.1 firm rule R-L3-1-A treats empty non-`none` anchors as semantically equivalent to `none`. Empty non-`none` `anchor_value` is a lint violation. Per `anchor_kind=none` the value is `""` (sentinel) and INV-6 governs — INV-16 only applies when `anchor_kind ∈ {quote, page, section, paragraph}`.
- INV-17: Constraint id parse rule (canonical). `NC-C{n}-{m}` where `{n}` is the **same** digit sequence used in the corresponding `claim_id` (`C-{n}`). Example: `claim_id=C-001` pairs with constraint ids `NC-C001-1`, `NC-C001-2`, etc. The pattern intentionally does NOT include a hyphen between `C` and `{n}` (i.e., `NC-C001-1`, NOT `NC-C-001-1`) because the canonical claim_id form `C-001` already establishes `001` as the joinable key — lint splits the NC string on the SECOND `-` (after `NC`), strips the leading `C`, then matches against the claim_id digit suffix. M-INV-2 / CV-INV-2 / CV-INV-3 all resolve through this parse rule. Zero-padding is consistent across both forms (`C-001` ↔ `NC-C001-1`); pattern `^NC-C[0-9]{3,}-[0-9]+$` enforces ≥3 digits matching the claim_id zero-padding.
- INV-18 (inverse-rule for inconclusive not_applicable paths): When `judgment=RETRIEVAL_FAILED` AND `audit_status=inconclusive` AND `defect_stage=not_applicable`, `ref_retrieval_method` MUST be exactly one of `{not_attempted, failed, audit_tool_failure}`. Any other value (`api`, `manual_pdf`, `not_found`) is a lint violation. This is the **inverse-direction** check complementing INV-10/INV-11/INV-14: those three each guarantee their own method value implies the (RETRIEVAL_FAILED, inconclusive, not_applicable) row, but they don't collectively guarantee that any entry hitting that row uses one of those three methods. Without INV-18, a malformed entry with `(RETRIEVAL_FAILED, inconclusive, not_applicable, api)` passes the 3-tuple allowed-matrix check, passes INV-10/11/14 (none fire), but matches no finalizer row — silently losing its annotation. INV-18 closes that.

### 3.2 `claim_intent_manifest.schema.json`

One entry per generating-agent invocation. Emitted by `synthesis_agent` / `draft_writer_agent` / `report_compiler_agent` after paper-visible context loads but before prose generation.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/claim_intent_manifest.schema.json",
  "title": "Material Passport Claim Intent Manifest Entry",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "manifest_version",
    "manifest_id",
    "emitted_by",
    "emitted_at",
    "claims",
    "manifest_negative_constraints"
  ],
  "properties": {
    "manifest_version": { "const": "1.0" },
    "manifest_id": {
      "type": "string",
      "pattern": "^M-[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z-[0-9a-f]{4}$",
      "description": "Discriminator scoping all claim_id values inside this manifest. Format: M-<ISO-8601-Z>-<4-hex>. Required because a single passport may contain multiple claim_intent_manifests[] entries (e.g., one from synthesis_agent and one from draft_writer_agent on the same run); bare C-001 alone would collide. The pair (manifest_id, claim_id) is the joinable key — see claim_audit_result.scoped_manifest_id + INV-15 / D-INV-2 cross-array integrity."
    },
    "emitted_by": { "enum": ["synthesis_agent", "draft_writer_agent", "report_compiler_agent"] },
    "emitted_at": { "type": "string", "format": "date-time" },
    "session_id": { "type": "string" },
    "claims": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["claim_id", "claim_text", "intended_evidence_kind", "planned_refs"],
        "properties": {
          "claim_id": { "type": "string", "pattern": "^C-[0-9]{3,}$" },
          "claim_text": { "type": "string", "minLength": 1, "maxLength": 2000 },
          "intended_evidence_kind": { "enum": ["empirical", "theoretical", "definitional", "normative"] },
          "planned_refs": { "type": "array", "items": { "type": "string" }, "minItems": 0 },
          "negative_constraints": {
            "type": "array",
            "items": {
              "type": "object",
              "additionalProperties": false,
              "required": ["constraint_id", "rule"],
              "properties": {
                "constraint_id": { "type": "string", "pattern": "^NC-C[0-9]{3,}-[0-9]+$" },
                "rule": { "type": "string", "minLength": 1, "maxLength": 500 }
              }
            }
          }
        }
      }
    },
    "manifest_negative_constraints": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["constraint_id", "rule"],
        "properties": {
          "constraint_id": { "type": "string", "pattern": "^MNC-[0-9]+$" },
          "rule": { "type": "string", "minLength": 1, "maxLength": 500 }
        }
      }
    }
  }
}
```

**Cross-field invariants** (lint-enforced):
- M-INV-1: `claim_id` uniqueness within ONE manifest (scoped by `manifest_id`). Cross-manifest collision (C-001 in both manifest A and manifest B) is permitted — the joinable discriminator is the `(manifest_id, claim_id)` pair.
- M-INV-2: `constraint_id` of `NC-C{n}-{m}` form MUST appear under `claims[]` entry where `claim_id=C-{n}` (i.e., claim-level constraint scoping)
- M-INV-3: `MNC-{m}` constraints in `manifest_negative_constraints` are globally applied; cannot be overridden by claim-level NC (claim-level can ADD, never DROP global)
- M-INV-4: `manifest_id` uniqueness across ALL `claim_intent_manifests[]` in one passport. Two manifests sharing the same `manifest_id` is a lint violation — the orchestrator must allocate fresh M-* identifiers per agent invocation.

### 3.3 `uncited_assertion.schema.json`

Per uncited-assertion finding. One entry per sentence in the draft that the D4-c three-condition token rule flagged. Aggregated as `uncited_assertions[]` in the orchestrator passport-tracking, parallel to `claim_audit_results[]`.

The separate schema exists because `uncited_assertion` findings have no `ref_slug` to fill — they describe sentences that *should* have a citation but don't. Embedding them in `claim_audit_result` would either force a sentinel `ref_slug` value or relax the required-field rule, both of which fight the schema's grain.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/uncited_assertion.schema.json",
  "title": "Material Passport Uncited Assertion Entry",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "finding_id",
    "sentence_text",
    "section_path",
    "trigger_tokens",
    "detected_at",
    "rule_version"
  ],
  "properties": {
    "finding_id": { "type": "string", "pattern": "^UA-[0-9]{3,}$" },
    "sentence_text": { "type": "string", "minLength": 1, "maxLength": 2000 },
    "section_path": { "type": "string", "minLength": 1, "description": "Hierarchical path from document root to the section containing the sentence, e.g. '2. Methods > 2.3 Sampling'" },
    "trigger_tokens": {
      "type": "array",
      "minItems": 1,
      "items": { "type": "string" },
      "description": "Concrete tokens that matched D4-c condition 1 (quantifiers or empirical-claim verbs). E.g. ['67%', 'showed']."
    },
    "detected_at": { "type": "string", "format": "date-time" },
    "rule_version": { "const": "D4-c-v1" },
    "upstream_owner_agent": {
      "enum": ["synthesis_agent", "draft_writer_agent", "report_compiler_agent", null]
    },
    "manifest_claim_id": {
      "type": ["string", "null"],
      "pattern": "^C-[0-9]{3,}$",
      "description": "When the uncited sentence corresponds to a claim_id in the active claim_intent_manifest. Per D4-c last paragraph: manifest membership does NOT exempt a sentence from being flagged. When present, MUST be paired with scoped_manifest_id to disambiguate against C-001 collision across manifests."
    },
    "scoped_manifest_id": {
      "type": ["string", "null"],
      "pattern": "^M-[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z-[0-9a-f]{4}$",
      "description": "Points to the claim_intent_manifest.manifest_id owning the referenced manifest_claim_id. The (scoped_manifest_id, manifest_claim_id) pair uniquely identifies which manifest's claim this uncited finding corresponds to, since C-001 may collide across manifests in the same passport. Required when manifest_claim_id ≠ null (U-INV-4 cross-array integrity). Null when manifest_claim_id is null (the uncited sentence does not correspond to any manifest claim)."
    }
  }
}
```

**Cross-field invariants** (lint-enforced in `check_claim_audit_consistency.py`):
- U-INV-1: `finding_id` uniqueness across `uncited_assertions[]` in one passport
- U-INV-2: `trigger_tokens` non-empty (rule fires only when condition 1 matches)
- U-INV-3: `rule_version` must equal `D4-c-v1` for v3.8.0 release; future rule revisions bump the const and require re-lint
- U-INV-4: When `manifest_claim_id ≠ null`, `scoped_manifest_id ≠ null` AND the `(scoped_manifest_id, manifest_claim_id)` pair MUST match some `claim_intent_manifests[].manifest_id == scoped_manifest_id` whose `claims[].claim_id` contains the manifest_claim_id (cross-array consistency). When `manifest_claim_id = null`, `scoped_manifest_id MUST also = null` (no orphan manifest pointer).

### 3.4 `claim_drift.schema.json`

Per claim-intent-drift finding. One entry per emitted claim that the manifest set-diff in §4 step 5 flagged as having drifted away from the `claim_intent_manifests[]` baseline. Aggregated as `claim_drifts[]` in the orchestrator passport-tracking, parallel to `claim_audit_results[]` and `uncited_assertions[]`.

The separate schema exists because **claim-intent drift is detected by manifest set-diff, not by judge invocation** — no `judgment` / `audit_status` / `rationale` field would carry meaning for these entries, and the judge is never run for the drift detection path. Embedding drift findings as a `defect_stage` of `claim_audit_result` would force `judgment=UNSUPPORTED` to be recorded without the judge ever evaluating that claim, contaminating both the schema semantics (UNSUPPORTED means "judge said UNSUPPORTED") and the calibration FNR/FPR metrics (which are scoped to the judge's own SUPPORTED/UNSUPPORTED/AMBIGUOUS judgments).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/claim_drift.schema.json",
  "title": "Material Passport Claim Drift Entry",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "finding_id",
    "drift_kind",
    "claim_text",
    "detected_at",
    "rule_version"
  ],
  "properties": {
    "finding_id": { "type": "string", "pattern": "^CD-[0-9]{3,}$" },
    "drift_kind": {
      "enum": ["EMITTED_NOT_INTENDED", "INTENDED_NOT_EMITTED"],
      "description": "EMITTED_NOT_INTENDED: an emitted claim that was not in the manifest (the drafted prose introduced a claim the writer did not pre-commit to). INTENDED_NOT_EMITTED: a manifest claim that did not appear in the emitted prose (the writer dropped a pre-committed claim during drafting). Both are advisory — gate-refuse is reserved for negative_constraint_violation."
    },
    "claim_text": { "type": "string", "minLength": 1, "maxLength": 2000, "description": "For EMITTED_NOT_INTENDED, the emitted sentence; for INTENDED_NOT_EMITTED, the manifest claim_text." },
    "manifest_claim_id": {
      "type": ["string", "null"],
      "pattern": "^C-[0-9]{3,}$",
      "description": "For INTENDED_NOT_EMITTED, the dropped manifest claim_id (REQUIRED, conditional on drift_kind — enforced by D-INV-2). For EMITTED_NOT_INTENDED, null (drifted claim has no manifest_claim_id since it was never in the manifest). When present, MUST be paired with scoped_manifest_id."
    },
    "scoped_manifest_id": {
      "type": ["string", "null"],
      "pattern": "^M-[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z-[0-9a-f]{4}$",
      "description": "Points to the claim_intent_manifest.manifest_id owning the referenced manifest_claim_id. Required when drift_kind=INTENDED_NOT_EMITTED (paired with manifest_claim_id per D-INV-2 cross-array integrity, disambiguating C-001 collision across manifests). Null when drift_kind=EMITTED_NOT_INTENDED (the drifted claim has no manifest origin)."
    },
    "section_path": {
      "type": ["string", "null"],
      "minLength": 1,
      "description": "For EMITTED_NOT_INTENDED, hierarchical path from document root to the section containing the drifted sentence (mirrors uncited_assertion.section_path). Null for INTENDED_NOT_EMITTED (dropped claim has no draft location)."
    },
    "detected_at": { "type": "string", "format": "date-time" },
    "rule_version": { "const": "D4-a-v1" },
    "upstream_owner_agent": {
      "enum": ["synthesis_agent", "draft_writer_agent", "report_compiler_agent", null]
    }
  }
}
```

**Cross-field invariants** (lint-enforced in `check_claim_audit_consistency.py`):
- D-INV-1: `finding_id` uniqueness across `claim_drifts[]` in one passport.
- D-INV-2: `drift_kind=INTENDED_NOT_EMITTED` → `manifest_claim_id ≠ null` AND `scoped_manifest_id ≠ null` AND the `(scoped_manifest_id, manifest_claim_id)` pair MUST match some `claim_intent_manifests[].manifest_id == scoped_manifest_id` whose `claims[].claim_id` contains the manifest_claim_id (cross-array integrity, disambiguates C-001 collision across manifests). `drift_kind=EMITTED_NOT_INTENDED` → `manifest_claim_id = null` AND `scoped_manifest_id = null` AND `section_path ≠ null`.
- D-INV-3: `rule_version` must equal `D4-a-v1` for v3.8.0 release; future rule revisions bump the const and require re-lint.
- D-INV-4: A given emitted sentence may produce AT MOST ONE finding across `uncited_assertions[]` and `claim_drifts[]` combined. When a sentence is both uncited AND drifted, the `uncited_assertions[]` entry takes precedence (per §5 finalizer precedence rule 3 restated from issue body) — no companion `claim_drifts[]` entry emits for the same sentence.

### 3.5 `constraint_violation.schema.json`

Per uncited claim that violates a manifest negative constraint. One entry per emitted sentence WITHOUT a `<!--ref:slug-->` marker that triggers `VIOLATED` from the negative-constraint judge prompt. Aggregated as `constraint_violations[]` in the orchestrator passport-tracking, parallel to `claim_audit_results[]` / `uncited_assertions[]` / `claim_drifts[]`.

**The separate schema exists because constraint violations on uncited claims are real HIGH-WARN gate-refuse blockers, but `claim_audit_result.ref_slug` is required and `uncited_assertion` is LOW-WARN advisory only.** A claim like "we observed causality" with no citation, against an MNC rule "will NOT claim causality without RCT evidence", is a genuine MUST-NOT violation the user explicitly declared. Routing it through `uncited_assertions[]` would silently downgrade a HIGH-WARN signal to LOW-WARN; routing it through `claim_audit_result` would require a sentinel `ref_slug` value that doesn't exist. A dedicated entry-type preserves both the HIGH-WARN severity and the schema integrity of each existing aggregate.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/constraint_violation.schema.json",
  "title": "Material Passport Constraint Violation Entry",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "finding_id",
    "claim_text",
    "section_path",
    "violated_constraint_id",
    "scoped_manifest_id",
    "judge_verdict",
    "rationale",
    "judge_model",
    "judge_run_at",
    "rule_version"
  ],
  "properties": {
    "finding_id": { "type": "string", "pattern": "^CV-[0-9]{3,}$" },
    "claim_text": { "type": "string", "minLength": 1, "maxLength": 2000 },
    "section_path": { "type": "string", "minLength": 1, "description": "Hierarchical path from document root to the section containing the offending sentence." },
    "violated_constraint_id": { "type": "string", "pattern": "^(NC-C[0-9]{3,}-[0-9]+|MNC-[0-9]+)$" },
    "scoped_manifest_id": {
      "type": "string",
      "pattern": "^M-[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z-[0-9a-f]{4}$",
      "description": "Points to the claim_intent_manifest.manifest_id owning the violated constraint. Required (no MANIFEST-MISSING sentinel admitted — constraints require an active manifest to exist)."
    },
    "manifest_claim_id": {
      "type": ["string", "null"],
      "pattern": "^C-[0-9]{3,}$",
      "description": "For NC-C{n}-{m} (claim-level constraint), the parent claim_id from the manifest. For MNC-{m} (global), null."
    },
    "judge_verdict": { "const": "VIOLATED" },
    "rationale": { "type": "string", "minLength": 1, "maxLength": 2000 },
    "judge_model": { "type": "string", "minLength": 1 },
    "judge_run_at": { "type": "string", "format": "date-time" },
    "rule_version": { "const": "D4-a-v1" },
    "upstream_owner_agent": {
      "enum": ["synthesis_agent", "draft_writer_agent", "report_compiler_agent", null]
    }
  }
}
```

**Cross-field invariants** (lint-enforced in `check_claim_audit_consistency.py`):
- CV-INV-1: `finding_id` uniqueness across `constraint_violations[]` in one passport.
- CV-INV-2: `(scoped_manifest_id, violated_constraint_id)` MUST resolve in some `claim_intent_manifests[]` entry. For `MNC-*` ids, the matching manifest's `manifest_negative_constraints[]` must contain it. For `NC-C{n}-{m}` ids, the matching manifest's `claims[]` entry with `claim_id=C-{n}` must contain a `negative_constraints[].constraint_id` matching the NC-* id, AND `manifest_claim_id` MUST equal `C-{n}`.
- CV-INV-3: When `violated_constraint_id` starts with `MNC-`, `manifest_claim_id = null`; when it starts with `NC-`, `manifest_claim_id` MUST equal the `C-{n}` extracted from the NC-* id.
- CV-INV-4: An uncited sentence MAY appear in BOTH `uncited_assertions[]` AND `constraint_violations[]` simultaneously — these surface different aspects (advisory uncited token-rule + HIGH-WARN constraint violation by judge) and don't trip D-INV-4-style exclusivity. However, a SINGLE sentence MUST NOT appear in `constraint_violations[]` more than once per `(scoped_manifest_id, violated_constraint_id)` — i.e. the lint dedup key is `(scoped_manifest_id, section_path, claim_text_hash, violated_constraint_id)`. Per M-INV-4 each `manifest_id` is unique across the passport but constraint ids (`MNC-*` / `NC-*`) are only unique WITHIN a manifest, so two manifests in the same passport may legitimately carry colliding constraint ids — the same sentence text may then violate both, and the dedupe must respect manifest scope to preserve both findings (v3.8.1).

### 3.6 `uncited_audit_failure.schema.json`

Per uncited-sentence × manifest pair where the constraint judge raised a `JudgeInvocationError` during D6 stream (d) judging. One entry per (sentence, manifest) failure. Aggregated as `uncited_audit_failures[]` in the orchestrator passport-tracking, parallel to `claim_audit_results[]` / `uncited_assertions[]` / `claim_drifts[]` / `constraint_violations[]`.

**The separate schema exists because the cited-path INV-14 `audit_tool_failure` row (a `claim_audit_result` entry carrying `ref_retrieval_method=audit_tool_failure`) cannot be reused on the uncited path — `claim_audit_result.ref_slug` is required, and the uncited path has no ref to bind.** Without a dedicated surface, a transient judge outage on a constraint check would either be silently swallowed (the pre-v3.8.2 bug — `NOT_VIOLATED` substituted, HIGH-WARN constraint check suppressed) or would force the entire audit pass to abort (dropping coverage). This entry-type mirrors INV-14 semantics on the uncited path: MED-WARN advisory at finalizer, retry-next-pass remediation, surfaces the infrastructure failure distinctly from a substantive non-violation. Routing through `uncited_assertions[]` would conflate D4-c token-rule advisory signal with audit-time infrastructure failure (different `rule_version`, different fault model, different annotation tier).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/uncited_audit_failure.schema.json",
  "title": "Material Passport Uncited Audit Failure Entry",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "finding_id",
    "claim_text",
    "section_path",
    "scoped_manifest_id",
    "fault_class",
    "rationale",
    "judge_model",
    "judge_run_at",
    "rule_version"
  ],
  "properties": {
    "finding_id": { "type": "string", "pattern": "^UAF-[0-9]{3,}$" },
    "claim_text": { "type": "string", "minLength": 1, "maxLength": 2000 },
    "section_path": { "type": "string", "minLength": 1, "description": "Hierarchical path from document root to the section containing the offending sentence (mirrors uncited_assertion.section_path)." },
    "scoped_manifest_id": {
      "type": "string",
      "pattern": "^M-[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z-[0-9a-f]{4}$",
      "description": "Points to the claim_intent_manifest.manifest_id whose MNC/NC-C set was being judged when the failure occurred. Required — no MANIFEST-MISSING sentinel admitted; UAF emission requires an active manifest scope."
    },
    "manifest_claim_id": {
      "type": ["string", "null"],
      "pattern": "^C-[0-9]{3,}$",
      "description": "When the sentence was bound to a manifest claim (sentence carries `manifest_claim_id` per §4 step 5 stream (d) NC-C judging path), points to that claim. Null when the judge call was against MNCs only (manifest-wide constraints, no claim binding). Mirrors constraint_violation.manifest_claim_id polarity."
    },
    "fault_class": {
      "enum": [
        "judge_timeout",
        "judge_api_error",
        "judge_parse_error",
        "cache_corruption",
        "retrieval_api_error",
        "retrieval_timeout",
        "retrieval_network_error"
      ],
      "description": "Same closed enum as INV-14 fault-class taxonomy on the cited path. Sourced from JudgeInvocationError.fault_class at the raise site."
    },
    "rationale": { "type": "string", "minLength": 1, "maxLength": 2000, "description": "MUST begin with the fault_class tag followed by `: ` and a free-form detail. Mirrors INV-14 rationale format. Example: `judge_timeout: judge timed out after 30s`." },
    "judge_model": { "type": "string", "minLength": 1 },
    "judge_run_at": { "type": "string", "format": "date-time" },
    "rule_version": { "const": "D4-c-v1-uaf-v1", "description": "UAF surface version. Distinguishes from `D4-c-v1` (uncited_assertion D4-c detector) and `D4-a-v1` (constraint_violation). The `-uaf-v1` suffix marks this as a separate surface, not a D4-c revision." },
    "upstream_owner_agent": {
      "enum": ["synthesis_agent", "draft_writer_agent", "report_compiler_agent", null]
    }
  }
}
```

**Cross-field invariants** (lint-enforced in `check_claim_audit_consistency.py`):
- UAF-INV-1: `finding_id` uniqueness across `uncited_audit_failures[]` in one passport.
- UAF-INV-2: `scoped_manifest_id` MUST resolve in some `claim_intent_manifests[]` entry (cross-array reference integrity).
- UAF-INV-3: When `manifest_claim_id ≠ null`, the `(scoped_manifest_id, manifest_claim_id)` pair MUST match some `claims[].claim_id` in the referenced manifest. When `manifest_claim_id = null`, the failure was against MNCs only (no claim binding required). Mirrors U-INV-4 / CV-INV-2 cross-array integrity pattern.
- UAF-INV-4: Per-(sentence, manifest) dedup. The tuple `(scoped_manifest_id, section_path, claim_text_hash)` MUST be unique across the aggregate. A sentence judged once per manifest produces at most one UAF row per (sentence, manifest). Two manifests both failing on the same sentence emit two distinct rows (legitimate per-manifest scope, mirrors CV-INV-4 cross-manifest reasoning).
- UAF-INV-5: `rationale` MUST begin with the row's own `fault_class` value followed by `":"` (and a `" "` plus free-form detail when a detail is available — the trailing space is omitted when `detail` is empty so the rationale stays `minLength: 1`-valid). Mirrors INV-14 rationale prefix requirement on the cited path; the prefix must match this row's `fault_class` field, not just any known tag. Example with detail: `"judge_timeout: judge timed out after 30s"`. Example without detail: `"judge_timeout:"` (a 14-character minimum form when the upstream `JudgeInvocationError.detail` is empty).
- UAF-INV-6: **Cross-aggregate exclusivity.** A sentence MUST NOT appear in both `uncited_audit_failures[]` AND `constraint_violations[]` for the same `(scoped_manifest_id, section_path, claim_text_hash)` — VIOLATED and audit_tool_failure are mutually exclusive verdict states at per-(sentence, manifest) level (one is a positive verdict, the other is no verdict at all). Co-existence with `uncited_assertions[]` IS permitted (D4-c detector positives and audit-time judge failure are independent signals).

## 4. Agent prompt structure: `claim_ref_alignment_audit_agent.md`

Sections (in order):

1. **Purpose & v3.8 placement** — single paragraph naming L3 audit role, dependency on v3.7.3 anchor input, audit-not-arbitration boundary.
2. **PATTERN PROTECTION (v3.6.7)** — byte-equivalent block to existing audited-agents pattern protection convention. Prevents cascading edits.
3. **Input contract** — exact passport fields read; `claim_audit_config` keys consumed (max_claims_per_paper, judge_model, gold_set_path, cache_dir).

   **Sampling behavior when citation count N > max_claims_per_paper:** the agent MUST emit a single `audit_sampling_summary` entry (one per audit run) into the passport `audit_sampling_summaries[]` aggregate, schema below. The agent selects a **stratified sample** — divide the N citations into k buckets (where k = min(max_claims_per_paper, N)) and pick one citation from each bucket in document order. Other citations are not audited but the summary entry surfaces the skip rate so users see how many citations went unaudited. No silent skipping per D3(a). When N ≤ max_claims_per_paper, no summary entry is needed (or equivalently, an entry with `audited_count == total_citation_count` may be emitted for telemetry).

   **`audit_sampling_summary` entry schema** (minimal, no separate §3.x — small enough to inline here):
   ```json
   {
     "$schema": "https://json-schema.org/draft/2020-12/schema",
     "type": "object",
     "additionalProperties": false,
     "required": ["audit_run_id", "max_claims_per_paper", "total_citation_count", "audited_count", "audited_indices", "sampling_strategy", "emitted_at"],
     "properties": {
       "audit_run_id": { "type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z-[0-9a-f]{4}$" },
       "max_claims_per_paper": { "type": "integer", "minimum": 1 },
       "total_citation_count": { "type": "integer", "minimum": 0 },
       "audited_count": { "type": "integer", "minimum": 0 },
       "audited_indices": { "type": "array", "items": { "type": "integer", "minimum": 0 }, "description": "0-based document-order indices of the audited citations." },
       "sampling_strategy": { "const": "stratified_buckets_v1" },
       "emitted_at": { "type": "string", "format": "date-time" }
     }
   }
   ```

   **Sampling invariants:**
   - S-INV-1: `audited_count == |audited_indices|`.
   - S-INV-2: `audited_count ≤ max_claims_per_paper` AND `audited_count ≤ total_citation_count`.
   - S-INV-3: When `audited_count < total_citation_count`, the finalizer MUST emit a paper-level `[CLAIM-AUDIT-SAMPLED — k/N audited]` annotation in the AI Self-Reflection Report appendix.
   - S-INV-4: `audited_indices` are strictly ascending (no duplicates, document order).

   Lint rule 4c: validate `audit_sampling_summaries[]` against the inline schema + S-INV-1..S-INV-4.
4. **Audit pipeline (6 steps)**:
   - Step 1 — Anchor presence check (D1, INV-6 firm rule).
   - Step 2 — Reference retrieval (`api` → `manual_pdf` → `failed`/`not_found`). LOW-WARN on `failed` (D2 paywall). Sets `ref_retrieval_method` + carries `retrieved_excerpt` forward.
   - Step 3 — Cache lookup keyed by `(claim_text_hash, ref_slug, anchor_kind, anchor_value_hash, retrieved_excerpt_hash, active_constraints_hash, judge_model)`. The `active_constraints_hash` is SHA-256 over the JCS-encoded set of manifest constraints applicable to this claim at audit time. **Selection is scoped by `(scoped_manifest_id, claim_id)`, NOT bare `claim_id`** — per M-INV-1, cross-manifest C-001 collision is permitted, so selecting by bare claim_id would pick constraints from the wrong manifest. The set: top-level `manifest_negative_constraints[]` of the **specific** manifest whose `manifest_id == scoped_manifest_id` ∪ that manifest's `claims[].negative_constraints[]` entry whose `claim_id` matches the current claim, sorted by `constraint_id`. Lookup runs AFTER retrieval so the cached judgment is bound to the exact source text the judge will see, AND to the exact constraint set the judge would evaluate — if the user re-runs after uploading a manual PDF, correcting the corpus entry, OR adding/changing a negative constraint, the relevant hash changes and the cache miss forces fresh judging.

     **The cache stores only judge-verdict + source-bound fields, never run-local identifiers.** Cached fields: `judgment`, `audit_status`, `defect_stage`, `rationale`, `judge_model`, `judge_run_at`, `ref_retrieval_method`, `violated_constraint_id`. Excluded (must be rebuilt from current-run context on replay): `claim_id` (new manifest position), `audit_run_id` (new run), `upstream_owner_agent` (different emitting agent on a different draft), `upstream_dispute` (run-specific dispute log), `anchor_value` (already keyed but re-emitted from current marker). This separation is what allows a verdict for the same `(claim_text, ref, anchor, source-excerpt, constraint-set, judge_model)` to be reused across different drafts / manifests without misattribution.

     On hit: load cached judge-verdict + source-bound block; assemble a complete `claim_audit_result` by joining with current-run identifiers (current `claim_id`, current `audit_run_id`, current `upstream_owner_agent`). On miss: proceed to Step 4-5; write only the judge-verdict + source-bound block into the cache; emit the joined entry. The filesystem KV is `${ARS_CACHE_DIR}/claim_audit_v1/<cache_key_sha256>.json`. Cache-side metadata (mtime) lives on the filesystem, never inside the JSON body.
   - Step 4 — Passage location using anchor_value (quote = exact match; page/section/paragraph = scoped retrieval).
   - Step 5 — Judge invocation with prompt template. Output one of SUPPORTED/UNSUPPORTED/AMBIGUOUS, with rationale.
   - Step 6 — Defect_stage classification. Citation-bound results emit `claim_audit_result` entries with `defect_stage` ∈ 6 substantive categories `{retrieval_existence, metadata, source_description, citation_anchor, synthesis_overclaim, negative_constraint_violation}` plus 2 non-substantive `{not_applicable, null}`. Four out-of-band finding categories use separate entry types: (a) uncited-sentence findings emit `uncited_assertion` entries (§3.3); (b) claim-intent drift findings emit `claim_drift` entries (§3.4); (c) **cited** constraint violations (sentence carries `<!--ref:slug-->` AND judge says VIOLATED) emit `claim_audit_result` entries with `defect_stage=negative_constraint_violation`; (d) **uncited** constraint violations (no `<!--ref:slug-->` AND judge says VIOLATED against an MNC/NC rule in scope) emit `constraint_violation` entries (§3.5). (c) and (d) are the cited/uncited split routed by §4 Step 5 stream (c)/(d). Precedence rules from issue body restated in §5 finalizer integration.
5. **Manifest cross-reference (D6)** — three-set diff of `intended_claims` (manifest) vs `emitted_claims` (extracted from draft) vs `supported_claims` (post-judge SUPPORTED subset). The diff produces four streams: (a) `EMITTED_NOT_INTENDED` — emitted claims missing from manifest → `claim_drifts[]` entry with `drift_kind=EMITTED_NOT_INTENDED`, advisory LOW-WARN at finalizer. (b) `INTENDED_NOT_EMITTED` — manifest claims dropped from draft → `claim_drifts[]` entry with `drift_kind=INTENDED_NOT_EMITTED`, advisory LOW-WARN. (c) Manifest negative-constraint matches on **cited** claims (sentence has `<!--ref:slug-->`) — pass to judge via §4 negative-constraint prompt; VIOLATED outcomes emit `claim_audit_result` entries with `defect_stage=negative_constraint_violation` (judge IS invoked here, distinct from drift). (d) Manifest negative-constraint matches on **uncited** claims (sentence has no `<!--ref:slug-->` but matches MNC/NC scope) — also pass to judge via the same negative-constraint prompt; VIOLATED outcomes emit `constraint_violations[]` entries (§3.5), HIGH-WARN gate-refuse at finalizer. **`JudgeInvocationError` on this path emits `uncited_audit_failures[]` entries (§3.6) carrying the fault_class tag — MED-WARN advisory at finalizer; the pre-v3.8.2 synthetic NOT_VIOLATED substitution silently suppressed HIGH-WARN constraint checks and is fixed in v3.8.2 / #118 by this routing.** (c) and (d) BOTH escalate to HIGH-WARN on VIOLATED — explicit author MUST NOT rules block regardless of citation presence — but they use distinct entry-types to preserve the schema integrity of `claim_audit_result` (which requires `ref_slug`); the corresponding outage path uses an INV-14 row on (c) and a `uncited_audit_failures[]` entry on (d) for the same symmetric reason. (a) and (b) are pure manifest-set-diff signals never seen by the judge.
6. **Uncited-assertion detector (D4-c)** — 3-condition token rule. Pseudocode included.
7. **Output emission** — one `claim_audit_result` entry per audited citation, plus aggregate counts emitted in pipeline-orchestrator Stage 6 reflection report.
8. **Calibration mode** — opt-in flow per `claim_audit_calibration_protocol.md`. Gold-set ingestion → judge run → FNR/FPR computation → user-facing report.
9. **Error handling** — three failure surfaces with distinct semantics, so retrieval access restrictions and audit-tool outages don't collapse:
   - **Retrieval access restriction (verified paywall — HTTP 403/402, license-restricted, no full-text endpoint, reference exists but body not accessible):** emit `claim_audit_result` with `judgment=RETRIEVAL_FAILED`, `audit_status=inconclusive`, `defect_stage=not_applicable`, `ref_retrieval_method=failed`. INV-10 / D2 — LOW-WARN advisory. **NOTE:** transient API errors (5xx, timeouts, network failures) do NOT belong here — they map to `audit_tool_failure` below.
   - **Audit infrastructure / transient outage (judge timeout, judge API 5xx, retrieval API 5xx, retrieval timeout / network error, retrieval API DNS failure, cache corruption, JSON parse failure):** emit `claim_audit_result` with `judgment=RETRIEVAL_FAILED`, `audit_status=inconclusive`, `defect_stage=not_applicable`, `ref_retrieval_method=audit_tool_failure`. Per INV-14 — MED-WARN advisory at finalizer (`[CLAIM-AUDIT-TOOL-FAILURE — <fault-class>]`), surfaces the infrastructure problem distinctly from a paywall, but does NOT gate-refuse — retry on next pipeline pass is the remediation. Rationale MUST begin with a fault-class tag in `{judge_timeout, judge_api_error, judge_parse_error, cache_corruption, retrieval_api_error, retrieval_timeout, retrieval_network_error}` followed by `: <detail>`. The discriminator between `failed` and `audit_tool_failure` is permanence — a paywall is a stable property of the citation, an API 5xx is a transient property of the infrastructure.
   - **Fabricated reference (retrieval API reports not_found):** per INV-12 — `ref_retrieval_method=not_found`, `defect_stage=retrieval_existence`, `audit_status=completed`. HIGH-WARN gate-refuse.
   - **Uncited-path judge outage (v3.8.2 / #118):** when `_invoke_judge` raises `JudgeInvocationError` during D6 stream (d) constraint judging on an uncited sentence, emit an `uncited_audit_failure` entry (§3.6) carrying the fault_class tag. MED-WARN advisory at finalizer (`[CLAIM-AUDIT-TOOL-FAILURE-UNCITED — <fault-class>]`), gate passes — retry on next pipeline pass is the remediation. MUST NOT emit a synthetic `NOT_VIOLATED` verdict (silent suppression of HIGH-WARN constraint check is the bug fixed in v3.8.2). Mirrors INV-14 semantics on the cited path: judge outage is operational signal distinct from substantive non-violation, but the uncited path uses a dedicated aggregate because `claim_audit_result.ref_slug` is required.
10. **Cross-references** — Zhao 2026 §1, RubricEM Borrows 1+2, v3.7.3 anchor input contract, v3.6.7 PATTERN PROTECTION convention.

**Judge prompt template** (canonical form, embedded in agent prompt):

> Given this claim from a paper draft and this excerpt from the cited reference, does the reference support the claim?
>
> CLAIM: {claim_text}
> CITED REFERENCE EXCERPT: {retrieved_excerpt}
> ANCHOR KIND: {anchor_kind}
> ANCHOR VALUE: {anchor_value}
>
> Output ONE of:
> - SUPPORTED — the reference directly supports the claim
> - UNSUPPORTED — the reference does NOT support the claim (the cited source says something different or contradictory)
> - AMBIGUOUS — the reference is related but does not clearly support or contradict the claim
>
> Then output ONE SENTENCE rationale.
>
> Format: `JUDGMENT: <one-of>\nRATIONALE: <one sentence>`

**Negative-constraint judge prompt template** (extended form):

> Given this claim and the author's declared negative constraint, does the claim violate the constraint?
>
> CLAIM: {claim_text}
> CONSTRAINT: {constraint_rule}
>
> Output ONE of: VIOLATED, NOT_VIOLATED
> Then output ONE SENTENCE rationale.

VIOLATED → `judgment=UNSUPPORTED, defect_stage=negative_constraint_violation, violated_constraint_id={constraint_id}` per INV-8.

## 5. Orchestrator integration: `pipeline_orchestrator_agent.md` §3.6

New section "Claim-Faithfulness Audit Gate (v3.8)". Mirrors §3.5 Audit Artifact Gate structure but for claim-level audit.

**Trigger boundary:** Stage 4 → Stage 5 transition, in the same handoff slot as the v3.7.1 Cite-Time Provenance Finalizer. The audit dispatches AFTER the Cite-Time Provenance Finalizer pass (which resolves anchor-presence per v3.7.3 §3.1 and the 5-cell matrix) and BEFORE `formatter_agent` runs its hard gate at the start of Stage 5. This ordering mirrors §3.5 v3.6.7 audit gate (audit between deliverable completion and downstream consumption).

**Why not Stage 5→6:** `formatter_agent`'s terminal hard gate runs **during** Stage 5 (per orchestrator §"Cite-Time Provenance Finalizer (v3.7.1)" — formatter consumes finalizer output and refuses on `[UNVERIFIED CITATION ...]`). If the claim audit dispatches at Stage 5→6, `claim_audit_results[]` would be produced after the terminal gate has already passed; HIGH-WARN-CLAIM-NOT-SUPPORTED could not block output. The Stage 4→5 slot is the only place where (a) the draft prose with v3.7.3 anchors exists, (b) the cite finalizer has run so anchor presence is settled, and (c) the formatter hard gate has NOT yet run.

The audit agent receives:
- All in-text citations with their resolved `<!--ref:slug ...-->` + `<!--anchor:...-->` marker pairs (post-finalizer)
- The `claim_intent_manifests[]` aggregate from the writing-stage agents
- The `literature_corpus[]` aggregate (for retrieval)

**Outputs feeding formatter hard gate (same Stage 5 pass):**
- `claim_audit_results[]` array (one per audited citation) — drives the 8-row matrix annotations
- `constraint_violations[]` array (one per uncited-but-violates-MNC/NC sentence) — drives `[HIGH-WARN-CONSTRAINT-VIOLATION-UNCITED ({violated_constraint_id})]` annotation. **MUST be passed to formatter alongside `claim_audit_results[]`** — without this, uncited HIGH-WARN gate-refuse path silently disappears since no claim_audit_result row exists for uncited constraint violations (per §3.5 split). The formatter's REFUSE list per §1 deliverable 5 includes HIGH-WARN-CONSTRAINT-VIOLATION-UNCITED — this handoff is what makes that REFUSE check observable.
- `uncited_assertions[]` array — drives `[UNCITED-ASSERTION]` LOW-WARN advisory annotation (formatter renders, does NOT refuse).
- `uncited_audit_failures[]` array (v3.8.2 / #118 — one per uncited sentence × manifest where the constraint judge raised `JudgeInvocationError`) — drives `[CLAIM-AUDIT-TOOL-FAILURE-UNCITED — <fault-class>]` MED-WARN advisory annotation (formatter renders, does NOT refuse). Mirrors the cited-path INV-14 row but uses a dedicated aggregate per §3.6 because `claim_audit_result.ref_slug` is required.
- `claim_drifts[]` array — drives `[LOW-WARN-CLAIM-DRIFT — kind=...]` LOW-WARN advisory annotation (formatter renders, does NOT refuse).
- `audit_sampling_summaries[]` array — drives paper-level `[CLAIM-AUDIT-SAMPLED — k/N audited]` annotation when audited_count < total_citation_count (formatter renders in the AI Self-Reflection Report appendix; does NOT refuse).
- Per-citation/per-sentence annotations injected adjacent to the existing v3.7.1 finalizer annotations (HIGH-WARN classes block; MED/LOW-WARN advisory passes).

**Outputs feeding Stage 6 self-reflection:**
- Per-stage `defect_stage` histogram appendix (renders when ≥ 5 completed entries) — added to the existing Stage 6 AI Self-Reflection Report after gate pass

**Finalizer matrix extension (8-row):**

Existing v3.7.3 5-cell matrix (anchor presence + 4-cell trust state) gains a new finalizer pass that overlays per-citation audit annotations from `claim_audit_results[]`. The matrix discriminates the previously-conflated paywall vs anchorless cases by reading `ref_retrieval_method` alongside `(judgment, defect_stage)`. Rows are evaluated top-to-bottom, first match wins:

| `judgment` | `defect_stage` | `ref_retrieval_method` | Annotation | Severity Tier | Gate behavior |
|---|---|---|---|---|---|
| SUPPORTED | `null` | (any) | (no annotation) | — | pass |
| AMBIGUOUS | source_description / citation_anchor / synthesis_overclaim / null | (any) | `[CLAIM-AUDIT-AMBIGUOUS]` | LOW-WARN advisory | pass |
| UNSUPPORTED | source_description / metadata / citation_anchor / synthesis_overclaim | (any) | `[HIGH-WARN-CLAIM-NOT-SUPPORTED]` | HIGH-WARN | gate-refuse |
| UNSUPPORTED | negative_constraint_violation | (any) | `[HIGH-WARN-NEGATIVE-CONSTRAINT-VIOLATION ({violated_constraint_id})]` | HIGH-WARN | gate-refuse (per D4-a — explicit author rules are HIGH-WARN; drift findings emit into `claim_drifts[]` at LOW-WARN advisory tier — see below) |
| RETRIEVAL_FAILED | retrieval_existence | not_found | `[HIGH-WARN-FABRICATED-REFERENCE]` | HIGH-WARN | gate-refuse (retrieval-side detection — the cited reference does not exist in the retrieval API; fabrication is a retrieval finding, not a bibliographic-metadata finding) |
| RETRIEVAL_FAILED | not_applicable | **not_attempted** | `[HIGH-WARN-CLAIM-AUDIT-ANCHORLESS — v3.7.3 R-L3-1-A VIOLATION REACHED AUDIT]` | HIGH-WARN | gate-refuse (anchor=none should have been blocked by v3.7.3 finalizer; this row is a defense-in-depth surface against finalizer skip/stale paths) |
| RETRIEVAL_FAILED | not_applicable | **failed** | `[CLAIM-AUDIT-UNVERIFIED — REFERENCE FULL-TEXT NOT RETRIEVABLE]` | LOW-WARN advisory | pass (paywall — D2) |
| RETRIEVAL_FAILED | not_applicable | **audit_tool_failure** | `[CLAIM-AUDIT-TOOL-FAILURE — <fault-class>]` | MED-WARN advisory | pass (audit infrastructure failure after retrieval succeeded; surfaced distinctly from paywall per INV-14; retry next pipeline pass) |

**Why three rows for `(RETRIEVAL_FAILED, not_applicable)`:** anchor=none (INV-6/INV-11), paywall (INV-10), and audit-tool failure (INV-14) all emit this `(judgment, defect_stage)` pair, but mean three very different things — anchorless is a contract violation that already should have been gate-refused upstream by v3.7.3 (defense-in-depth row HIGH-WARN gate-refuse); paywall is a stable access restriction (legitimate tool/access failure, LOW-WARN advisory pass); audit_tool_failure is a transient infrastructure outage (judge timeout, retrieval 5xx, network error — MED-WARN advisory pass with retry-next-pass remediation). The `ref_retrieval_method` field discriminates them and their finalizer outcomes: `not_attempted` → HIGH-WARN gate-refuse; `failed` → LOW-WARN advisory; `audit_tool_failure` → MED-WARN advisory. INV-10 / INV-11 / INV-14 jointly enforce that these three are the only `(not_applicable)` paths AND they're mutually exclusive on `ref_retrieval_method` (each `(not_applicable)` entry MUST carry exactly one of the three method values).

**`uncited_assertion` entries** (separate aggregate `uncited_assertions[]`) emit at LOW-WARN tier with annotation `[UNCITED-ASSERTION]` next to the offending sentence. Always advisory; gate-refuse reserved for citation-level defects. See §3.3 for entry schema.

**`constraint_violation` entries** (separate aggregate `constraint_violations[]`) emit at HIGH-WARN tier with annotation `[HIGH-WARN-CONSTRAINT-VIOLATION-UNCITED ({violated_constraint_id})]` next to the offending sentence. Gate-refuse — explicit author MUST NOT rules block regardless of citation presence (parallels the gate-refuse behavior of cited constraint violations in the 8-row matrix; the entry-type split is purely a schema-integrity artifact, not a severity downgrade). The formatter hard gate MUST refuse output on this annotation alongside the four other HIGH-WARN classes (per §1 deliverable 5). See §3.5 for entry schema.

**`uncited_audit_failure` entries** (separate aggregate `uncited_audit_failures[]`, v3.8.2 / #118) emit at **MED-WARN advisory** tier with annotation `[CLAIM-AUDIT-TOOL-FAILURE-UNCITED — <fault-class>]` next to the offending sentence. Always advisory; gate passes — retry on next pipeline pass is the remediation. Mirrors INV-14 semantics on the uncited path: a transient judge outage on a constraint check is operational signal distinct from a substantive non-violation. Pre-v3.8.2 behavior synthesised a `NOT_VIOLATED` verdict on `JudgeInvocationError` and silently suppressed HIGH-WARN constraint checks; v3.8.2 routes these failures through this aggregate so the operational signal surfaces without dropping audit coverage (option 4 — re-raise and abort — was rejected for that exact coverage reason). The formatter's REFUSE list is unchanged — UAF is advisory and does not enter REFUSE. See §3.6 for entry schema.

**Why `claim_drifts[]` is separate from the 8-row matrix (per D4-a):** The decision doc rejected "manifest authority blocking" because normal drafting routinely refines claims away from manifest, and gate-refusing on drift would block valid revision passes. The §3.4 schema houses drift findings; they emit a `[LOW-WARN-CLAIM-DRIFT — kind={EMITTED_NOT_INTENDED|INTENDED_NOT_EMITTED}]` annotation next to the offending sentence (for EMITTED_NOT_INTENDED) or in the manifest-coverage appendix (for INTENDED_NOT_EMITTED). Always advisory; never gate-refusing. Source-level defects (source_description / metadata / citation_anchor / synthesis_overclaim) remain HIGH-WARN in the matrix because they indicate the prose is misrepresenting the cited source — the L3 faithfulness failure the audit exists to catch. Constraint violations remain HIGH-WARN because the author explicitly declared "MUST NOT".

**Uncited-assertion** results emit at LOW-WARN tier with annotation `[UNCITED-ASSERTION]` next to the offending sentence. Always advisory; gate-refuse reserved for citation-level defects.

**`/ars-mark-read` behavior:** Does NOT acknowledge HIGH-WARN-CLAIM-NOT-SUPPORTED or HIGH-WARN-NEGATIVE-CONSTRAINT-VIOLATION. Remediation: user fixes the prose (re-cites, drops claim, revises). Mirrors v3.7.3 R-L3-1-A asymmetry (locator is structural, not evidence-state).

**Mode flag:** Audit agent dispatch is **opt-in** per pipeline run, configurable in `academic-pipeline/SKILL.md` mode flags. Default OFF for v3.8.0; ramp-on plan deferred to post-calibration calibration evidence.

## 6. Lint: `scripts/check_claim_audit_consistency.py`

Coverage:

1. **Schema validation** — `claim_audit_result.schema.json`, `claim_intent_manifest.schema.json`, `uncited_assertion.schema.json`, `claim_drift.schema.json`, `constraint_violation.schema.json` all valid JSON Schema; sample passports validate. Inline `audit_sampling_summary` entry schema (§4 step 3) also validated.
2. **Cross-field invariants INV-1 through INV-18** — one test case per invariant, each with positive + negative fixture.
3. **Manifest invariants M-INV-1 through M-INV-4** — including M-INV-4 manifest_id uniqueness across passport (duplicate manifest_id rejected).
4. **Uncited-assertion invariants U-INV-1 through U-INV-4** — including cross-array `(scoped_manifest_id, manifest_claim_id)` integrity (uncited entry's referenced (M-*, C-*) pair must match some active manifest's claim).
4a. **Claim-drift invariants D-INV-1 through D-INV-4** — including cross-array integrity for `drift_kind=INTENDED_NOT_EMITTED` (the `(scoped_manifest_id, manifest_claim_id)` pair must match some `claim_intent_manifests[]` entry) and exclusivity rule D-INV-4 (a sentence cannot appear in both `uncited_assertions[]` and `claim_drifts[]`).
4b. **Constraint-violation invariants CV-INV-1 through CV-INV-4** — including cross-array integrity (CV-INV-2: `(scoped_manifest_id, violated_constraint_id)` MUST resolve in some active manifest entry; CV-INV-3: `manifest_claim_id` polarity must match constraint id prefix MNC/NC) and per-(manifest, sentence, constraint) dedup (CV-INV-4 — see §3.5 for the full dedup key shape `(scoped_manifest_id, section_path, claim_text_hash, violated_constraint_id)`).
4c. **Audit-sampling invariants S-INV-1 through S-INV-4** — including audited_count/audited_indices coherence (S-INV-1), cap respect (S-INV-2), finalizer annotation requirement when sampled (S-INV-3), and audited_indices ascending uniqueness (S-INV-4). Validates `audit_sampling_summaries[]` aggregate.
4d. **Uncited-audit-failure invariants UAF-INV-1 through UAF-INV-6** (v3.8.2 / #118) — schema validation against `uncited_audit_failure.schema.json`; finding_id uniqueness (UAF-INV-1); scoped_manifest_id cross-array integrity (UAF-INV-2); `(scoped_manifest_id, manifest_claim_id)` pair integrity (UAF-INV-3); per-(sentence, manifest) dedup with key `(scoped_manifest_id, section_path, claim_text_hash)` (UAF-INV-4); rationale fault_class prefix (UAF-INV-5); cross-aggregate exclusivity with `constraint_violations[]` (UAF-INV-6). Validates `uncited_audit_failures[]` aggregate.
5. **Allowed-matrix coverage** — every `(judgment, audit_status, defect_stage)` triple outside §3.1 table rejected; representative disallowed combinations (≥ 5) tested explicitly.
6. **Precedence rules** — negative_constraint_violation (HIGH-WARN claim_audit_result) > claim_drift (LOW-WARN claim_drifts[] entry) — per issue body rule 1; citation_anchor distinct from source_description (rule 2); uncited-sentence cases produce `uncited_assertions[]` entry, not a `claim_audit_result` row (rule 3 — uncited has no ref to evaluate). D-INV-4 also enforces: a sentence that's both uncited AND drifted emits only the `uncited_assertion` entry, no companion `claim_drift` entry. UAF-INV-6 (v3.8.2 / #118) enforces cross-aggregate exclusivity between `uncited_audit_failures[]` and `constraint_violations[]` — see §3.6 for the full rule.
7. **Acceptance check** — for any passport with ≥ 1 completed `claim_audit_result` whose `judgment=UNSUPPORTED`, ALL such rows must emit a `defect_stage` ≠ null AND ≠ not_applicable (100% emission per #103 acceptance criterion). AMBIGUOUS-with-null is explicitly permitted per INV-3 (judge unable to classify a related-but-unclear support level is a valid outcome); the issue body's "100% non-SUPPORTED" intent is narrower than literal reading suggests — it targets the UNSUPPORTED rows because those are the gate-refusing path, not the advisory tier.
8. **Coverage check** — sample passport with full 8-row finalizer matrix coverage (per §5); each annotation tier exercised at least once.

Lint exit codes: 0 (pass), 1 (one or more invariant violations; prints which + offending entry).

CI: invoked from `.github/workflows/spec-consistency.yml` (or matching workflow). Failure blocks merge.

## 7. TDD test plan

Tests written BEFORE production code per `superpowers:test-driven-development`. Order:

### 7.1 Schema validation tests (`tests/test_claim_audit_schema.py`)

- T-S1: Valid minimal entry validates (SUPPORTED, all required fields)
- T-S2: Each invariant INV-1..INV-18 covered by paired positive/negative fixture
- T-S3: `anchor_kind=none` entry that doesn't follow INV-6 fails lint (rationale missing prefix; `ref_retrieval_method ≠ not_attempted`)
- T-S4: Manifest M-INV-1 duplicate claim_id rejected
- T-S5: Manifest M-INV-2 dangling NC-C{n}-{m} (no parent claim) rejected
- T-S6: Manifest M-INV-3 claim-level constraint attempting to override MNC rejected
- T-S7: `uncited_assertion` U-INV-1..U-INV-4 covered by paired positive/negative fixture (rule_version literal; trigger_tokens non-empty; cross-array manifest_claim_id integrity)
- T-S8: `(judgment, audit_status, defect_stage)` allowed-matrix exhaustive coverage: each table row in §3.1 has a positive fixture, AND at least 5 representative disallowed combinations rejected (e.g., SUPPORTED + non-null defect_stage; UNSUPPORTED + null defect_stage; RETRIEVAL_FAILED + completed + not_applicable)

### 7.2 Audit-pipeline unit tests (`tests/test_claim_audit_pipeline.py`)

- T-P1: Step 1 — anchor=none input emits RETRIEVAL_FAILED/inconclusive/not_applicable + `ref_retrieval_method=not_attempted` with INV-6 rationale prefix, skips judge
- T-P2: Step 3 — cache hit (with matching `retrieved_excerpt_hash`) returns previously-judged result without invoking judge
- T-P3: Step 3 — cache miss (different `retrieved_excerpt_hash` after user uploads manual PDF) invokes judge then writes back
- T-P4: Step 2 — `ref_retrieval_method=failed` → LOW-WARN advisory path (D2 paywall)
- T-P5: Step 2 — `ref_retrieval_method=manual_pdf` accepted; `not_found` triggers `defect_stage=retrieval_existence`
- T-P6: Step 5 — judge VIOLATED → UNSUPPORTED + defect_stage=negative_constraint_violation + violated_constraint_id populated
- T-P7: Step 6 — 6 in-table defect_stage classifications each have a fixture mapping (`retrieval_existence`, `metadata`, `source_description`, `citation_anchor`, `synthesis_overclaim`, `negative_constraint_violation`). `uncited_assertion` is tested in §7.4 and `claim_drift` in a new §7.4a (both separate entry-types, not defect_stages of `claim_audit_result`); `not_applicable` is tested in T-P1 and T-P4.
- T-P8: Precedence rule 1 — claim that drifts AND violates a constraint → emits `claim_audit_result` with `defect_stage=negative_constraint_violation` (judge-evaluated, HIGH-WARN); the same claim does NOT additionally emit a `claim_drifts[]` entry — constraint violation absorbs the drift signal per D4 (a) explicit author rules > advisory drift surfaces.
- T-P9: Precedence rule 2 — citation_anchor distinct from source_description (anchor wrong, source description correct)
- T-P10: Precedence rule 3 — sentence that would be both an uncited_assertion AND a drifted manifest claim emits an `uncited_assertions[]` entry (no source-level evaluation, since there's no ref to evaluate). The same sentence may still appear in manifest diff diagnostics but does NOT produce a `claim_audit_result` row.
- T-P11: Cap sampling behavior — synthetic input with N=150 citations and `max_claims_per_paper=100` emits exactly 1 `audit_sampling_summary` entry with `audited_count=100`, `audited_indices` strictly ascending and of length 100, `sampling_strategy=stratified_buckets_v1`. Finalizer adds `[CLAIM-AUDIT-SAMPLED — 100/150 audited]` to the AI Self-Reflection Report. Variants: (a) N=50 and cap=100 → no summary entry OR summary with `audited_count == total_citation_count` (telemetry mode, finalizer adds NO sampling annotation per S-INV-3); (b) cap=0 input rejected as invalid configuration.

### 7.3 Manifest tests (`tests/test_claim_intent_manifest.py`)

- T-M1: Three-set diff — emitted ∩ intended ∩ supported, drift detection
- T-M2: Missing manifest → MANIFEST-MISSING advisory + claim-extraction-from-draft fallback, all defect_stages still emit
- T-M3: Constraint inheritance — MNC applies even when not redeclared at claim level

### 7.4 Uncited-assertion tests (`tests/test_uncited_assertion.py`)

- T-U1: Sentence with quantifier + no ref → uncited_assertion candidate
- T-U2: Definition sentence (contains "refers to") → NOT candidate
- T-U3: Methods boilerplate list → NOT candidate
- T-U4: Empirical claim ("showed X%") without ref → candidate
- T-U5: Claim in manifest but no ref → still candidate (D4-c last paragraph)

### 7.5 Finalizer integration tests (`tests/test_claim_audit_finalizer.py`)

- T-F1: 8-row matrix coverage keyed by the FULL 3-tuple (judgment, defect_stage, ref_retrieval_method) — each row maps to its specific annotation + severity tier + gate behavior. CRITICAL: `RETRIEVAL_FAILED + not_applicable` admits three distinct rows discriminated by `ref_retrieval_method` ∈ {not_attempted, failed, audit_tool_failure} — a test keyed only on (judgment, defect_stage) would let an implementation collapse these three into one and apply the wrong gate behavior. The test MUST assert each ref_retrieval_method value independently against its expected outcome:
  - T-F1a: SUPPORTED + null + any → no annotation, pass
  - T-F1b: AMBIGUOUS + {source_description, citation_anchor, synthesis_overclaim, null} + any → CLAIM-AUDIT-AMBIGUOUS, LOW-WARN advisory, pass
  - T-F1c: UNSUPPORTED + {source_description, metadata, citation_anchor, synthesis_overclaim} + any → HIGH-WARN-CLAIM-NOT-SUPPORTED, gate-refuse
  - T-F1d: UNSUPPORTED + negative_constraint_violation + any → HIGH-WARN-NEGATIVE-CONSTRAINT-VIOLATION, gate-refuse
  - T-F1e: RETRIEVAL_FAILED + retrieval_existence + not_found → HIGH-WARN-FABRICATED-REFERENCE, gate-refuse
  - T-F1f: RETRIEVAL_FAILED + not_applicable + **not_attempted** → HIGH-WARN-CLAIM-AUDIT-ANCHORLESS, **gate-refuse** (defense-in-depth; distinguishes from row T-F1g/T-F1h)
  - T-F1g: RETRIEVAL_FAILED + not_applicable + **failed** → LOW-WARN-CLAIM-AUDIT-UNVERIFIED, **pass** (paywall)
  - T-F1h: RETRIEVAL_FAILED + not_applicable + **audit_tool_failure** → MED-WARN-CLAIM-AUDIT-TOOL-FAILURE, **pass** (retry-next-pass)
- T-F2: HIGH-WARN-CLAIM-NOT-SUPPORTED triggers terminal gate refuse
- T-F3: `/ars-mark-read` does NOT clear HIGH-WARN-CLAIM-NOT-SUPPORTED (asymmetry preservation)
- T-F4: LOW-WARN-CLAIM-AUDIT-UNVERIFIED passes gate
- T-F5: Stage 6 reflection report renders histogram when ≥ 5 completed entries

### 7.6 End-to-end test (`tests/test_e2e_claim_audit.py`)

Synthetic 5-citation paper:
- Citation 1: real, SUPPORTED → no annotation
- Citation 2: real, AMBIGUOUS → LOW-WARN
- Citation 3: real but misused (source says inverse) → HIGH-WARN-CLAIM-NOT-SUPPORTED, gate refuses
- Citation 4: paywalled, retrieval fails → LOW-WARN-UNVERIFIED, passes gate
- Citation 5: violates declared negative constraint → HIGH-WARN-NEGATIVE-CONSTRAINT-VIOLATION, gate refuses

Test asserts: gate refuses output; only citations 3+5 are blockers; correcting them clears refusal.

### 7.7 Calibration mode test (`tests/test_claim_audit_calibration.py`)

Synthetic 20-tuple gold set covering alignment judgments (SUPPORTED/UNSUPPORTED/AMBIGUOUS/RETRIEVAL_FAILED) AND constraint judgments (VIOLATED/NOT_VIOLATED). Gold tuple shape per decision doc D3(c): `{tuple_kind, claim_text, ref_text_excerpt, anchor, expected_judgment, ...}` discriminated by `tuple_kind ∈ {alignment, constraint}`. For `tuple_kind=constraint`, REQUIRED fields: `constraint_under_test_id` AND (`constraint_under_test_rule_text` OR `manifest_fixture_path`). NOT_VIOLATED tuples MUST appear in the gold set (≥3 tuples; without them constraint FPR is unmeasurable). Suggested gold-set split: ~12 alignment tuples (covering 4 judgments) + ~8 constraint tuples (≥3 VIOLATED + ≥3 NOT_VIOLATED + remainder edge cases). Three-tier assertion:

- **T-C1 (threshold enforcement):** Test assert `FNR < 0.15 AND FPR < 0.10` against the synthetic gold set. Test FAILS when either threshold is exceeded. This is the unit of acceptance and aligns with reviewer-calibration convention (FNR/FPR thresholds are gates, not advisory). When the threshold is exceeded, CI fails — author must either curate a better gold set, tighten judge prompts, or update `judge_model`. (Issue body acceptance criterion + §9 acceptance bullet are binding.)
- **T-C2 (per-class FNR/FPR reporting):** Test asserts that FNR/FPR are computed AND surfaced per judgment-class (SUPPORTED vs UNSUPPORTED, AMBIGUOUS, violated-constraint) in the calibration report output. Reporting failure ≠ threshold failure — this catches calibration tooling regressions distinct from gold-set degradation.
- **T-C3 (gold-set shape integrity):** Test asserts: (a) Each tuple has a valid `tuple_kind ∈ {alignment, constraint}`. (b) `tuple_kind=alignment` tuples have `expected_judgment ∈ {SUPPORTED, UNSUPPORTED, AMBIGUOUS, RETRIEVAL_FAILED}` AND MUST NOT carry constraint fields. (c) `tuple_kind=constraint` tuples have `expected_judgment ∈ {VIOLATED, NOT_VIOLATED}` AND `constraint_under_test_id` MUST be present AND (`constraint_under_test_rule_text` OR `manifest_fixture_path`) MUST be present. (d) The gold set MUST contain ≥3 NOT_VIOLATED constraint tuples (else constraint FPR is unmeasurable and T-C1 cannot fail-on-threshold for the constraint line). Tuples violating any rule are REJECTED at calibration ingestion (lint-fail with diagnostic naming the violation). Prevents silent-skip regressions: missing rule text → judge evaluates against empty constraint → false NOT_VIOLATED → artificially low FNR; missing NOT_VIOLATED tuples → constraint FPR uncomputable → T-C1 silently bypassed.

Why three tiers: T-C2 catches infrastructure bugs (calibration script doesn't compute / doesn't write report); T-C3 catches gold-set authoring bugs (missing required rule text); T-C1 catches model/judge quality regression. All three must pass.

### 7.8 Regression test

Run existing 967+ test baseline (1107 unittest + 201 pytest adapters per session handoff). Zero regression required.

## 8. Cascade impact assessment

Files that may need touch:

| File | Why | Risk |
|---|---|---|
| `academic-pipeline/agents/pipeline_orchestrator_agent.md` | New §3.6 dispatch wiring | HIGH — already 712 lines; PATTERN PROTECTION block must stay byte-equivalent |
| `academic-paper/agents/formatter_agent.md` | Gate matrix extended to 8-row + HIGH-WARN classes | MED — 785 lines; v3.7.3 anchor logic preserved |
| `deep-research/agents/synthesis_agent.md` | New "Claim Intent Manifest Emission" sibling heading | MED — 220 lines; v3.7.3 Three-Layer heading stays |
| `deep-research/agents/report_compiler_agent.md` | Same | MED |
| `academic-paper/agents/draft_writer_agent.md` | Same | MED — 520 lines |
| `shared/contracts/passport/audit_artifact_entry.schema.json` | **NO TOUCH** (D5) | — |
| `shared/contracts/material_passport*` | No root schema exists; aggregate referenced through orchestrator | — |
| `shared/sprint_contract.schema.json` (Schema 13.1) | **NO TOUCH** (D6 zero-touch) | — |
| `scripts/check_audit_artifact_consistency.py` | **NO TOUCH** (D5 — separate lint) | — |
| `README.md` + `README.zh-TW.md` | v3.8 anchor + Zhao 2026 + RubricEM cite | LOW |
| `CHANGELOG.md` | v3.8 entry | LOW |
| `MODE_REGISTRY.md` | New mode flag for opt-in audit | LOW |

Boundary preservation lints (run as part of PR checks):
- `scripts/check_v3_6_7_pattern_protection.py` — verify PATTERN PROTECTION blocks unchanged
- `git diff main..HEAD -- shared/sprint_contract.schema.json` MUST be empty (v3.6.6 zero-touch)
- `git diff main..HEAD -- shared/contracts/passport/audit_artifact_entry.schema.json` MUST be empty (D5)

## 9. Acceptance criteria

Issue body acceptance + decision-doc-derived additions:

- [ ] Agent prompt passes ≥ 5 codex review rounds → 0 P1/P2 (new tool + IO, per harness convergence pattern)
- [ ] Schema + integration passes ≥ 1 gemini cross-model review round (docs-heavy fraction; see Codex 0.130 docs-review broken caveat — verify before invoking)
- [ ] Calibration mode tested with synthetic gold set (≥ 20 tuples) achieving FNR < 0.15 and FPR < 0.10
- [ ] End-to-end test (§7.6 above) passes
- [ ] Zero regression on existing 1107+ unittest + 201 pytest baseline
- [ ] All 18 cross-field invariants (INV-1..INV-18) + 4 manifest invariants (M-INV-1..M-INV-4) + 4 uncited-assertion invariants (U-INV-1..U-INV-4) + 4 claim-drift invariants (D-INV-1..D-INV-4) + 4 constraint-violation invariants (CV-INV-1..CV-INV-4) + 4 sampling invariants (S-INV-1..S-INV-4) covered by paired positive/negative fixture
- [ ] Allowed-matrix exhaustive test: every §3.1 table row positive + ≥5 disallowed combinations rejected
- [ ] `claim_intent_manifest` absent → `MANIFEST-MISSING` advisory + fallback flow exercised in test
- [ ] `audit_status=inconclusive` paths emit `defect_stage=not_applicable` (NOT `null`) — INV-4
- [ ] 100% of completed UNSUPPORTED findings emit a `defect_stage` ≠ null AND ≠ not_applicable (per #103 issue body acceptance criterion; AMBIGUOUS-null is permitted per INV-3 — stage accuracy deferred to #89)
- [ ] Stage 6 reflection report renders per-stage histogram when ≥ 5 completed audit results
- [ ] v3.6.6 Schema 13.1 zero-touch promise verified by git diff lint
- [ ] D5 `audit_artifact_entry.schema.json` zero-touch promise verified by git diff lint
- [ ] Precedence rules (3 rules per issue body) covered by test fixtures
- [ ] Public-repo boundary clean per personal-boundary deny list (run boundary scan before push)

## 10. Risks and open questions

The decision doc closed 8 OQs. Spec-level OQs (resolve during codex rounds, NOT before TDD):

- **S-OQ1** (codex round-1 candidate): cache eviction policy beyond manual rm. Tentative: rely on `judge_model` in cache key — model bumps naturally invalidate; users prune `${ARS_CACHE_DIR}/claim_audit_v1/` as needed.
- **S-OQ2** (codex round-1): retrieval API selection order (Semantic Scholar vs Crossref vs OpenAlex) and fallback ladder. Tentative: SS → Crossref → OpenAlex → manual_pdf, matching v3.6.x convention.
- **S-OQ3** (codex round-2): `claim_id` allocation — sequential per manifest or session-scoped UUID-prefix? Tentative: sequential per manifest (`C-001`, `C-002`...), uniqueness scope = single manifest entry. Cross-manifest collision tolerated (different agent invocations).
- **S-OQ4** (codex round-2): `audit_run_id` collision handling when two audits run within same second. Tentative: 4-hex random suffix (already in schema pattern) gives ~65k uniqueness per second; assume sufficient for ARS scale.
- **S-OQ5** (codex round-2+): manifest emission timing — exact lifecycle hook in `synthesis_agent` and `draft_writer_agent`. Tentative: emit AFTER `literature_corpus[]` consumption, BEFORE first prose block. Confirm during prompt-design rounds.

## 11. Convergence cost projection

Per session handoff harness data:
- doc-only PR = 1 round
- plumbing PR = 3-4 rounds
- new tool + IO PR = **5 rounds**
- scope-frozen follow-up = 3 rounds

#103 is **new tool + IO + new agent + 2 new schemas + new lint + 6 prompt edits**, larger than #105 (which was "new tool + IO migration"). Expected codex rounds: **5-7**.

Strategy: split into two PRs if Round-5 still has open P1/P2:
- PR-A: schemas + lint + agent prompt + tests (no orchestrator/formatter/synthesis_agent touch yet)
- PR-B: orchestrator §3.6 + finalizer 8-row + downstream agent integration

This mirrors #105 → #115 split pattern (production module first, integration follow-up).

## 12. Memory anchors

After ship, update:

- `~/.claude/projects/-Users-imbad/memory/project_ars_106_ai_disclosure_discovery.md` — lesson #22 (8-OQ compressed decision-doc pattern when issue body already has frozen design)
- `~/.claude/projects/-Users-imbad/memory/feedback_codex_round_convergence_by_scope.md` — new memory if not exists, record "new tool + IO + new agent" data point
- Consider new memory `feedback_audit_results_vs_audit_artifact_semantic_split.md` documenting D5 boundary

## 13. Implementation order (TDD-driven)

1. Write all 5 schema files up front (§3.1 claim_audit_result + §3.2 claim_intent_manifest + §3.3 uncited_assertion + §3.4 claim_drift + §3.5 constraint_violation) plus the inline `audit_sampling_summary` schema (§4 step 3). All five + inline are referenced by §6 schema-validation lint rule 1 + §7.1 schema tests; writing only §3.1/§3.2 first would make T-S1..T-S8 fail with "schema not found" diagnostics for the missing 3.
2. Write `tests/test_claim_audit_schema.py` — failing because schema not yet validated by lint
3. Write `scripts/check_claim_audit_consistency.py` — minimal code to pass schema tests
4. Write `tests/test_claim_audit_pipeline.py` (T-P1..T-P11) — failing, no agent yet
5. Write `claim_ref_alignment_audit_agent.md` Steps 1-6 — minimal text to pass pipeline tests via fixture-driven dispatch
6. Write `tests/test_uncited_assertion.py` + token-rule detector module
7. Write `tests/test_claim_intent_manifest.py` + emission helpers
8. Write `tests/test_claim_audit_finalizer.py` + orchestrator §3.6 + formatter 8-row extension
9. Write `tests/test_e2e_claim_audit.py` + synthetic 5-citation paper fixture
10. Write `tests/test_claim_audit_calibration.py` + calibration protocol doc
11. Regression run on full baseline; zero failures
12. `/simplify` parallel (reuse + quality + efficiency); fix findings
13. `/codex review --base=main`; iterate to 0 P1/P2
14. gemini cross-model round (verify Codex 0.130 docs-heavy caveat first per `feedback_codex_0_130_docs_review_broken.md`)
15. Public-repo boundary scan
16. Squash merge

Steps 4-5 are the highest-risk: agent prompt + pipeline are the load-bearing intersection. Plan for 2-3 codex rounds focused there.
<!-- SOURCE-CONTENT-END -->

<a id="source-scripts-claim-audit-pipeline-py"></a>

## SOURCE: scripts/claim_audit_pipeline.py

<!-- SOURCE-CONTENT-BEGIN bytes=62427 -->
"""claim_audit_pipeline — Python implementation of the §4 Step 1-6 pipeline.

This module is the executable face of `claim_ref_alignment_audit_agent.md`.
The agent prompt narrates the pipeline contract; this module runs it
under test so cross-field invariants and emission routing can be pinned
without dispatching the agent to a live model.

Retrieval and judge invocation are dependency-injected (`retrieve_fn` /
`judge_fn`) so tests can drive every error and decision path — paywall,
audit_tool_failure, not_found, SUPPORTED, UNSUPPORTED with each
defect_stage hint, VIOLATED. Production callers wire these to real
retrieval/judge clients in their own dispatch layer.

The full spec is in
docs/design/2026-05-15-issue-103-claim-alignment-audit-spec.md §4-§5.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable

# Allow both CLI invocations (`python3 scripts/claim_audit_pipeline.py`) AND
# package-style invocations (`python -m unittest scripts.test_*`) to resolve
# the shared constants module via the same import.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _claim_audit_constants import (  # noqa: E402
    DRIFT_RULE_VERSION,
    INV6_RATIONALE_PREFIX,
    RE_NC_CONSTRAINT,
    SAMPLING_STRATEGY,
    SENTINEL_MANIFEST_ID,
    UAF_RULE_VERSION,
    UNCITED_RULE_VERSION,
)

# Permitted UNSUPPORTED defect_stages for non-constraint paths (§3.1 matrix).
_UNSUPPORTED_NON_CONSTRAINT_DEFECTS = {
    "source_description",
    "metadata",
    "citation_anchor",
    "synthesis_overclaim",
}

# Permitted AMBIGUOUS defect_stages (§3.1 matrix).
_AMBIGUOUS_DEFECTS = {"source_description", "citation_anchor", "synthesis_overclaim", None}


# ---------------------------------------------------------------------------
# Cache helpers.
# ---------------------------------------------------------------------------


def _stable_json(value: Any) -> str:
    """JCS-style canonicalization sufficient for cache-key hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash_text(text: str | None) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def _active_constraints_for_claim(
    *,
    scoped_manifest_id: str,
    claim_id: str,
    claim_by_mc_id: dict[tuple[str, str], dict[str, Any]],
    mncs_by_manifest_id: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    """Return the manifest-scoped + claim-scoped negative-constraint set for a citation.

    Reads from pre-built indexes (built once per audit run in
    `run_audit_pipeline`) instead of rescanning the manifest tree per
    citation — at realistic workloads (~150 citations × ~100 manifest
    claims) that saves ~30k Python ops per run with no behavioral delta.
    """
    constraints: list[dict[str, Any]] = []
    for mnc in mncs_by_manifest_id.get(scoped_manifest_id, []):
        constraints.append({"constraint_id": mnc["constraint_id"], "rule": mnc["rule"], "scope": "MNC"})
    claim = claim_by_mc_id.get((scoped_manifest_id, claim_id))
    if claim is not None:
        for nc in claim.get("negative_constraints", []) or []:
            constraints.append(
                {"constraint_id": nc["constraint_id"], "rule": nc["rule"], "scope": "NC"}
            )
    constraints.sort(key=lambda c: c["constraint_id"])
    return constraints


def _cache_key(
    *,
    claim_text: str,
    ref_slug: str,
    anchor_kind: str,
    anchor_value: str,
    retrieved_excerpt: str | None,
    active_constraints: list[dict[str, Any]],
    judge_model: str,
) -> str:
    payload = {
        "claim_text_hash": _hash_text(claim_text),
        "ref_slug": ref_slug,
        "anchor_kind": anchor_kind,
        "anchor_value_hash": _hash_text(anchor_value),
        "retrieved_excerpt_hash": _hash_text(retrieved_excerpt),
        "active_constraints_hash": _hash_text(
            _stable_json([{"constraint_id": c["constraint_id"], "rule": c["rule"]} for c in active_constraints])
        ),
        "judge_model": judge_model,
    }
    return hashlib.sha256(_stable_json(payload).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Judge + retrieval invocation — wraps callables so transient failures become
# INV-14 audit_tool_failure rows instead of aborting the audit. Spec §4 step 2
# + INV-14 + Step 13 R1+R2 codex findings (transient errors on either external
# call must surface as MED-WARN advisory rows).
# ---------------------------------------------------------------------------

# Legal judge verdicts per path. claim_audit_result schema enum + constraint-side
# verdicts (VIOLATED / NOT_VIOLATED). Cited and uncited paths route different
# subsets — passing path-specific allow-lists into `_invoke_judge` rejects an
# off-path verdict at the invocation boundary instead of letting it propagate
# into _judge_result_entry where the ValueError would abort the audit
# (Step 13 R3 codex P2 #2).
_CITED_PATH_JUDGMENTS: frozenset[str] = frozenset(
    {"SUPPORTED", "UNSUPPORTED", "AMBIGUOUS", "VIOLATED"}
)
_UNCITED_PATH_JUDGMENTS: frozenset[str] = frozenset({"VIOLATED", "NOT_VIOLATED"})


class JudgeInvocationError(Exception):
    """Raised by `_invoke_judge` when judge_fn fails or returns malformed output.

    Carries the INV-14 fault-class tag + detail so the caller can emit a
    `RETRIEVAL_FAILED + inconclusive + not_applicable + audit_tool_failure`
    row per spec §4 step 2 + INV-14 instead of letting the exception abort the
    audit pass.
    """

    def __init__(self, fault_class: str, detail: str) -> None:
        super().__init__(f"{fault_class}: {detail}")
        self.fault_class = fault_class
        self.detail = detail


class RetrievalInvocationError(Exception):
    """Raised by `_invoke_retrieve` when retrieve_fn fails or returns malformed output.

    Mirrors JudgeInvocationError but tags faults with the INV-14 retrieval_*
    family (retrieval_api_error / retrieval_timeout / retrieval_network_error)
    so a transient retrieval outage surfaces as audit_tool_failure rather than
    aborting the audit pass (Step 13 R2 codex P2 finding).
    """

    def __init__(self, fault_class: str, detail: str) -> None:
        super().__init__(f"{fault_class}: {detail}")
        self.fault_class = fault_class
        self.detail = detail


def _validate_judge_dict(
    result: Any,
    *,
    allowed_judgments: frozenset[str],
    active_constraint_ids: frozenset[str],
    source: str = "judge_fn",
) -> dict[str, Any]:
    """Validate a judge-output dict (fresh or cache-hit).

    Raises `JudgeInvocationError` with the appropriate fault-class tag for any
    shape violation. Pulled out of `_invoke_judge` so cache hits can reuse the
    same validation surface — without it a malformed cache entry would crash
    `_judge_result_entry` and abort the audit (Step 13 R3 codex P2 #4).

    Validation surface:
      - non-dict                                  → judge_parse_error
      - missing `judgment` or `rationale`         → judge_parse_error
      - judgment not in `allowed_judgments`       → judge_parse_error
      - VIOLATED without non-blank string id      → judge_parse_error
      - VIOLATED id not in `active_constraint_ids`→ judge_parse_error
        (Step 13 R3 codex P2 #1 — prevents formatter gate-refuse on a
        hallucinated constraint the author never declared)
    """
    if not isinstance(result, dict):
        raise JudgeInvocationError(
            "judge_parse_error",
            f"{source} returned {type(result).__name__}, expected dict",
        )
    if "judgment" not in result or "rationale" not in result:
        raise JudgeInvocationError(
            "judge_parse_error",
            f"{source} returned dict missing required key(s); got keys={sorted(result)}",
        )
    judgment = result.get("judgment")
    # Step 13 R8 codex P2-3: guard isinstance(str) before set membership so a
    # malformed return like {"judgment": [1, 2], ...} surfaces as a clean
    # judge_parse_error instead of bubbling TypeError("unhashable type") out
    # past the translation boundary and aborting the audit.
    if not isinstance(judgment, str):
        raise JudgeInvocationError(
            "judge_parse_error",
            f"{source} returned non-string judgment={judgment!r} (type={type(judgment).__name__}); expected one of {sorted(allowed_judgments)}",
        )
    if judgment not in allowed_judgments:
        raise JudgeInvocationError(
            "judge_parse_error",
            f"{source} returned judgment={judgment!r}; expected one of {sorted(allowed_judgments)} on this path",
        )
    if judgment == "VIOLATED":
        vcid = result.get("violated_constraint_id")
        if not isinstance(vcid, str) or not vcid.strip():
            raise JudgeInvocationError(
                "judge_parse_error",
                f"{source} returned VIOLATED without a valid violated_constraint_id (got {vcid!r}); INV-7 requires non-null id",
            )
        if vcid not in active_constraint_ids:
            raise JudgeInvocationError(
                "judge_parse_error",
                f"{source} returned VIOLATED with violated_constraint_id={vcid!r} outside the active constraint set {sorted(active_constraint_ids)}; rejecting hallucinated id (Step 13 R3 codex P2 #1)",
            )
    return result


def _invoke_judge(
    judge_fn: Callable[..., dict[str, Any]],
    *,
    allowed_judgments: frozenset[str],
    active_constraint_ids: frozenset[str],
    **call_kwargs: Any,
) -> dict[str, Any]:
    """Invoke `judge_fn` and translate transient failures + malformed output into INV-14 tags.

    Exception → fault class mapping:
      - TimeoutError                          → judge_timeout
      - json.JSONDecodeError / ValueError     → judge_parse_error
      - any other Exception                   → judge_api_error

    Return-value validation delegates to `_validate_judge_dict` so cache hits
    reuse the same surface (Step 13 R3 codex P2 #4).

    `allowed_judgments` is path-specific: cited path passes
    `_CITED_PATH_JUDGMENTS`, uncited (constraint) path passes
    `_UNCITED_PATH_JUDGMENTS`. RETRIEVAL_FAILED / NOT_VIOLATED on the cited
    path is rejected here instead of crashing in `_judge_result_entry`
    (Step 13 R3 codex P2 #2).

    `active_constraint_ids` carries the in-scope MNC/NC ids for this call
    so a VIOLATED with a hallucinated id is rejected at the boundary
    (Step 13 R3 codex P2 #1).

    Does NOT swallow `SystemExit` / `KeyboardInterrupt`.
    """
    try:
        result = judge_fn(**call_kwargs)
    except TimeoutError as exc:
        raise JudgeInvocationError("judge_timeout", str(exc) or "judge timed out") from exc
    except (json.JSONDecodeError, ValueError) as exc:
        raise JudgeInvocationError("judge_parse_error", str(exc) or "judge returned malformed payload") from exc
    except Exception as exc:  # noqa: BLE001 — translation boundary; the source class is captured
        raise JudgeInvocationError("judge_api_error", f"{type(exc).__name__}: {exc}") from exc

    return _validate_judge_dict(
        result,
        allowed_judgments=allowed_judgments,
        active_constraint_ids=active_constraint_ids,
        source="judge_fn",
    )


def _invoke_retrieve(
    retrieve_fn: Callable[[dict[str, Any]], dict[str, Any]],
    citation: dict[str, Any],
) -> dict[str, Any]:
    """Invoke `retrieve_fn` and translate transient failures + malformed output into INV-14 retrieval_* tags.

    Exception → fault class mapping (mirrors `_invoke_judge`):
      - TimeoutError                          → retrieval_timeout
      - OSError / ConnectionError             → retrieval_network_error
      - json.JSONDecodeError / ValueError     → retrieval_api_error
      - any other Exception                   → retrieval_api_error

    Return-value validation:
      - non-dict                              → retrieval_api_error
      - missing `ref_retrieval_method` key    → retrieval_api_error
      - unknown `ref_retrieval_method` value  → retrieval_api_error

    Returns the retrieval dict on success; raises RetrievalInvocationError
    otherwise so the caller can map it to an audit_tool_failure row.
    """
    try:
        result = retrieve_fn(citation)
    except TimeoutError as exc:
        raise RetrievalInvocationError("retrieval_timeout", str(exc) or "retrieve_fn timed out") from exc
    except (ConnectionError, OSError) as exc:
        raise RetrievalInvocationError(
            "retrieval_network_error",
            f"{type(exc).__name__}: {exc}" if str(exc) else type(exc).__name__,
        ) from exc
    except (json.JSONDecodeError, ValueError) as exc:
        raise RetrievalInvocationError(
            "retrieval_api_error",
            str(exc) or "retrieve_fn returned malformed payload",
        ) from exc
    except Exception as exc:  # noqa: BLE001 — translation boundary
        raise RetrievalInvocationError("retrieval_api_error", f"{type(exc).__name__}: {exc}") from exc

    if not isinstance(result, dict):
        raise RetrievalInvocationError(
            "retrieval_api_error",
            f"retrieve_fn returned {type(result).__name__}, expected dict",
        )
    method = result.get("ref_retrieval_method")
    if method is None:
        raise RetrievalInvocationError(
            "retrieval_api_error",
            f"retrieve_fn return missing ref_retrieval_method; got keys={sorted(result)}",
        )
    # Step 13 R8 codex P2-4: guard isinstance(str) before set membership so a
    # malformed return like {"ref_retrieval_method": [...], ...} surfaces as a
    # clean retrieval_api_error instead of bubbling TypeError("unhashable type")
    # out past the translation boundary and aborting the audit (symmetric to
    # P2-3 on the judge side).
    if not isinstance(method, str):
        raise RetrievalInvocationError(
            "retrieval_api_error",
            f"retrieve_fn returned non-string ref_retrieval_method={method!r} (type={type(method).__name__})",
        )
    if method not in {"api", "manual_pdf", "failed", "not_found", "audit_tool_failure"}:
        raise RetrievalInvocationError(
            "retrieval_api_error",
            f"retrieve_fn returned unknown ref_retrieval_method={method!r}",
        )
    # Step 13 R3 codex P2 #3: a successful retrieval pathway MUST carry a
    # non-empty excerpt — otherwise the judge would be invoked with
    # `retrieved_excerpt=None`/empty and could mark a claim SUPPORTED with no
    # source text. Map this shape violation to retrieval_api_error so it
    # surfaces as audit_tool_failure instead of silently degrading the audit.
    if method in {"api", "manual_pdf"}:
        excerpt = result.get("retrieved_excerpt")
        if not isinstance(excerpt, str) or not excerpt.strip():
            raise RetrievalInvocationError(
                "retrieval_api_error",
                f"retrieve_fn returned ref_retrieval_method={method!r} with empty/missing retrieved_excerpt; successful retrievals must carry source text",
            )
    return result


# ---------------------------------------------------------------------------
# Emission helpers — each builds one entry dict.
# ---------------------------------------------------------------------------


def _anchorless_entry(citation: dict[str, Any], *, audit_run_id: str, now_iso: str, judge_model: str) -> dict[str, Any]:
    """§4 Step 1: anchor=none short-circuits to RETRIEVAL_FAILED+inconclusive+not_applicable+not_attempted.

    INV-6 sentinel: anchor_kind=none MUST carry anchor_value="" (empty sentinel
    per claim_audit_result.schema.json). We pin the empty string here rather
    than passing through citation.anchor_value — a stale residual anchor like
    "123" on an anchor_kind=none row violates the schema contract.
    """
    return {
        "claim_id": citation["claim_id"],
        "scoped_manifest_id": citation.get("scoped_manifest_id", SENTINEL_MANIFEST_ID),
        "claim_text": citation["claim_text"],
        "ref_slug": citation["ref_slug"],
        "anchor_kind": "none",
        "anchor_value": "",
        "judgment": "RETRIEVAL_FAILED",
        "audit_status": "inconclusive",
        "defect_stage": "not_applicable",
        "rationale": (
            f"{INV6_RATIONALE_PREFIX}: cited claim {citation['claim_id']} carries anchor=none; "
            "v3.7.3 finalizer should have gate-refused upstream — defense-in-depth row."
        ),
        "judge_model": judge_model,
        "judge_run_at": now_iso,
        "ref_retrieval_method": "not_attempted",
        "upstream_owner_agent": citation.get("upstream_owner_agent"),
        "audit_run_id": audit_run_id,
    }


def _retrieval_failure_entry(
    citation: dict[str, Any],
    *,
    method: str,
    audit_run_id: str,
    now_iso: str,
    judge_model: str,
    fault_class: str | None = None,
) -> dict[str, Any]:
    """§4 Step 2: retrieval-side failure routes that skip the judge."""
    if method == "failed":
        # D2 paywall — LOW-WARN advisory; INV-10.
        entry = {
            "judgment": "RETRIEVAL_FAILED",
            "audit_status": "inconclusive",
            "defect_stage": "not_applicable",
            "rationale": "Reference full text not retrievable (paywall / license-restricted access).",
        }
    elif method == "not_found":
        # Fabricated reference — HIGH-WARN; INV-12.
        entry = {
            "judgment": "RETRIEVAL_FAILED",
            "audit_status": "completed",
            "defect_stage": "retrieval_existence",
            "rationale": "Retrieval API reports the cited reference does not exist (suspected fabrication).",
        }
    elif method == "audit_tool_failure":
        # Transient infrastructure outage — MED-WARN; INV-14.
        tag = fault_class or "retrieval_api_error"
        entry = {
            "judgment": "RETRIEVAL_FAILED",
            "audit_status": "inconclusive",
            "defect_stage": "not_applicable",
            "rationale": f"{tag}: transient audit-infrastructure failure during retrieval; retry on next pipeline pass.",
        }
    else:  # pragma: no cover — should be unreachable given Step 2 caller dispatch
        raise ValueError(f"_retrieval_failure_entry called with non-failure method={method!r}")

    return {
        "claim_id": citation["claim_id"],
        "scoped_manifest_id": citation.get("scoped_manifest_id", SENTINEL_MANIFEST_ID),
        "claim_text": citation["claim_text"],
        "ref_slug": citation["ref_slug"],
        "anchor_kind": citation["anchor_kind"],
        "anchor_value": citation.get("anchor_value", ""),
        "judgment": entry["judgment"],
        "audit_status": entry["audit_status"],
        "defect_stage": entry["defect_stage"],
        "rationale": entry["rationale"],
        "judge_model": judge_model,
        "judge_run_at": now_iso,
        "ref_retrieval_method": method,
        "upstream_owner_agent": citation.get("upstream_owner_agent"),
        "audit_run_id": audit_run_id,
    }


def _judge_result_entry(
    citation: dict[str, Any],
    *,
    judge_result: dict[str, Any],
    ref_retrieval_method: str,
    audit_run_id: str,
    now_iso: str,
    judge_model: str,
) -> dict[str, Any]:
    """§4 Steps 5-6: route judge verdict to the right (judgment, defect_stage) row."""
    verdict = judge_result["judgment"]
    rationale = judge_result.get("rationale", "")

    if verdict == "SUPPORTED":
        judgment, defect_stage, violated_id = "SUPPORTED", None, None
    elif verdict == "AMBIGUOUS":
        hint = judge_result.get("defect_stage_hint")
        if hint not in _AMBIGUOUS_DEFECTS:
            hint = None  # AMBIGUOUS+disallowed defect → coerce to null (INV-3 protection)
        judgment, defect_stage, violated_id = "AMBIGUOUS", hint, None
    elif verdict == "UNSUPPORTED":
        hint = judge_result.get("defect_stage_hint") or "source_description"
        if hint not in _UNSUPPORTED_NON_CONSTRAINT_DEFECTS:
            hint = "source_description"
        judgment, defect_stage, violated_id = "UNSUPPORTED", hint, None
    elif verdict == "VIOLATED":
        # Cited constraint violation — INV-7/INV-8 path.
        judgment = "UNSUPPORTED"
        defect_stage = "negative_constraint_violation"
        violated_id = judge_result.get("violated_constraint_id")
    else:
        raise ValueError(f"unknown judge verdict: {verdict!r}")

    entry: dict[str, Any] = {
        "claim_id": citation["claim_id"],
        "scoped_manifest_id": citation.get("scoped_manifest_id", SENTINEL_MANIFEST_ID),
        "claim_text": citation["claim_text"],
        "ref_slug": citation["ref_slug"],
        "anchor_kind": citation["anchor_kind"],
        "anchor_value": citation.get("anchor_value", ""),
        "judgment": judgment,
        "audit_status": "completed",
        "defect_stage": defect_stage,
        "rationale": rationale or "(no rationale provided)",
        "judge_model": judge_model,
        "judge_run_at": now_iso,
        "ref_retrieval_method": ref_retrieval_method,
        "upstream_owner_agent": citation.get("upstream_owner_agent"),
        "audit_run_id": audit_run_id,
    }
    if violated_id is not None:
        entry["violated_constraint_id"] = violated_id
    return entry


def _uncited_audit_failure_entry(
    *,
    sentence: dict[str, Any],
    scoped_manifest_id: str,
    manifest_claim_id: str | None,
    fault_class: str,
    detail: str,
    finding_id: str,
    judge_model: str,
    now_iso: str,
) -> dict[str, Any]:
    """§3.6 (v3.8.2 / #118): uncited sentence × manifest pair where the
    constraint judge raised JudgeInvocationError. Mirrors INV-14 row on the
    cited path but rides in the uncited_audit_failures[] aggregate because
    claim_audit_result.ref_slug is required."""
    rationale = f"{fault_class}: {detail}" if detail else f"{fault_class}:"
    return {
        "finding_id": finding_id,
        "claim_text": sentence["sentence_text"],
        "section_path": sentence.get("section_path", ""),
        "scoped_manifest_id": scoped_manifest_id,
        "manifest_claim_id": manifest_claim_id,
        "fault_class": fault_class,
        "rationale": rationale,
        "judge_model": judge_model,
        "judge_run_at": now_iso,
        "rule_version": UAF_RULE_VERSION,
        "upstream_owner_agent": sentence.get("upstream_owner_agent"),
    }


def _constraint_violation_entry(
    *,
    sentence: dict[str, Any],
    judge_result: dict[str, Any],
    scoped_manifest_id: str,
    finding_id: str,
    judge_model: str,
    now_iso: str,
) -> dict[str, Any]:
    """§3.5 / §5 stream (d): uncited claim with VIOLATED judge verdict."""
    violated_id = judge_result.get("violated_constraint_id")
    manifest_claim_id = None
    if violated_id:
        nc_match = RE_NC_CONSTRAINT.match(violated_id)
        if nc_match:
            manifest_claim_id = f"C-{nc_match.group(1)}"
    return {
        "finding_id": finding_id,
        "claim_text": sentence["sentence_text"],
        "section_path": sentence.get("section_path", ""),
        "violated_constraint_id": violated_id,
        "scoped_manifest_id": scoped_manifest_id,
        "manifest_claim_id": manifest_claim_id,
        "judge_verdict": "VIOLATED",
        "rationale": judge_result.get("rationale", "Constraint violated by uncited claim."),
        "judge_model": judge_model,
        "judge_run_at": now_iso,
        "rule_version": DRIFT_RULE_VERSION,
        "upstream_owner_agent": sentence.get("upstream_owner_agent"),
    }


def _uncited_assertion_entry(
    *,
    sentence: dict[str, Any],
    finding_id: str,
    now_iso: str,
    trigger_tokens: list[str] | None = None,
) -> dict[str, Any]:
    # Resolve trigger_tokens with strict semantics: prefer the explicit
    # keyword arg, fall back to the sentence dict, and raise if both are
    # absent. The prior `["uncited"]` sentinel passed U-INV-2 minItems=1
    # but carried no semantic content — callers who skipped the detector
    # silently emitted meaningless tokens into the passport. Raise instead
    # so the contract is enforced at write-time, not discovered at audit-
    # read-time (per codex R1 P1-4).
    tokens = trigger_tokens or sentence.get("trigger_tokens")
    if not tokens:
        raise ValueError(
            f"_uncited_assertion_entry: finding_id={finding_id!r} has no "
            "trigger_tokens. Caller must pre-process draft sentences "
            "through detect_uncited_assertions (or supply trigger_tokens "
            "explicitly); the schema's U-INV-2 minItems=1 invariant is "
            "an audit-quality contract, not a placeholder slot."
        )
    manifest_claim_id = sentence.get("manifest_claim_id")
    # Step 7 codex R1 CO-3 / U-INV-4 pair rule: scoped_manifest_id is the
    # disambiguator for a specific manifest claim. When no claim_id is bound
    # (the uncited sentence is in scope for a manifest-level MNC but is NOT
    # itself a manifest claim — runtime contract for stream-d uncited
    # constraint-violation routing), the uncited_assertion row MUST drop the
    # manifest scope. The companion constraint_violations[] row owns the
    # manifest pointer in that case; carrying scope on both rows would fail
    # U-INV-4 (manifest_claim_id null ↔ scoped_manifest_id null).
    scoped_manifest_id = (
        sentence.get("scoped_manifest_id") if manifest_claim_id is not None else None
    )
    return {
        "finding_id": finding_id,
        "sentence_text": sentence["sentence_text"],
        "section_path": sentence.get("section_path", ""),
        "trigger_tokens": tokens,
        "detected_at": now_iso,
        "rule_version": UNCITED_RULE_VERSION,
        "upstream_owner_agent": sentence.get("upstream_owner_agent"),
        "manifest_claim_id": manifest_claim_id,
        "scoped_manifest_id": scoped_manifest_id,
    }


def _claim_drift_entry(
    *,
    drift_kind: str,
    claim_text: str,
    finding_id: str,
    now_iso: str,
    manifest_claim_id: str | None = None,
    scoped_manifest_id: str | None = None,
    section_path: str | None = None,
) -> dict[str, Any]:
    entry = {
        "finding_id": finding_id,
        "drift_kind": drift_kind,
        "claim_text": claim_text,
        "detected_at": now_iso,
        "rule_version": DRIFT_RULE_VERSION,
        "manifest_claim_id": manifest_claim_id,
        "scoped_manifest_id": scoped_manifest_id,
        "section_path": section_path,
    }
    return entry


# ---------------------------------------------------------------------------
# Sampling helper.
# ---------------------------------------------------------------------------


def _stratified_bucket_indices(total: int, cap: int) -> list[int]:
    """Pick `cap` indices in [0, total) via stratified buckets in document order.

    Divides [0, total) into `cap` equal-ish buckets and picks the first index of
    each bucket. The result is strictly ascending and has length min(cap, total).

    Why two-stage fill: a naive `int(i * width)` for `width = total / cap`
    silently collapses adjacent picks when `total/cap < 2` (e.g. N=101,
    cap=100 → `int(99 * 1.01) == int(100 * 1.0)`-class duplicates after
    dedup). The S-INV-1 invariant ties `audited_count` to `len(audited_indices)`
    so a silent dedup would shrink audited_count below cap with no surface.
    We dedup first, then fill the remaining slots from un-picked indices in
    ascending document order — keeping the bucket-first-pick bias for spread
    while honoring the contract that `audited_count == min(cap, N)` whenever
    that is achievable.
    """
    if total <= 0 or cap <= 0:
        return []
    k = min(cap, total)
    width = total / k
    picks: set[int] = set()
    for i in range(k):
        picks.add(int(i * width))
    # Fill missing slots from un-picked indices in ascending order so the
    # final result is exactly k strictly-ascending unique picks whenever
    # k ≤ total (which is guaranteed by `k = min(cap, total)`).
    if len(picks) < k:
        for j in range(total):
            if j not in picks:
                picks.add(j)
                if len(picks) == k:
                    break
    return sorted(picks)


# ---------------------------------------------------------------------------
# Drift detection (manifest set-diff).
# ---------------------------------------------------------------------------


def _detect_drifts(
    *,
    manifests: list[dict[str, Any]],
    emitted_citations: list[dict[str, Any]],
    uncited_sentence_texts: set[str],
    constraint_absorbed_claim_ids: set[tuple[str, str]],
    constraint_absorbed_manifest_scopes: set[str],
    now_iso: str,
    next_finding_id: Callable[[], str],
) -> list[dict[str, Any]]:
    """§4 step 5 manifest set-diff producing claim_drift entries.

    Precedence:
      - T-P8 + Step 13 R5 codex P3: constraint-violation absorbs drift in
        **full** for the violating manifest. `constraint_absorbed_claim_ids`
        captures (manifest, declared-claim-id) pairs; `constraint_absorbed_manifest_scopes`
        captures the manifest_id itself so a same-manifest citation with a
        drifted (non-manifest) claim_id is also suppressed — preserves the
        "absorbed in full" spec promise. A violation in manifest A does NOT
        silence drift in manifest B.
      - T-P10 / D-INV-4: uncited sentence takes precedence over drift — no
        drift entry whose claim_text matches an uncited sentence_text.

    MANIFEST-MISSING fallback (Step 13 R5 codex P2 #2): when no manifest
    carries any claims, there's no pre-commitment baseline to drift FROM —
    every emitted citation would be classified EMITTED_NOT_INTENDED, layering
    spurious LOW-WARN noise on top of the MANIFEST-MISSING advisory the
    formatter already surfaces. Short-circuit and return no drifts so the
    fallback run remains audit-only.
    """
    has_baseline = any((m.get("claims") or []) for m in manifests)
    if not has_baseline:
        return []
    drifts: list[dict[str, Any]] = []

    # Index emitted citations by (scoped_manifest_id, claim_id) — these are
    # the "supported" set candidates the prose actually produced. Use
    # .get(SENTINEL_MANIFEST_ID) so MANIFEST-MISSING callers that omit
    # scoped_manifest_id still build a coherent emitted_pairs set per the
    # sentinel fallback contract (Step 13 R4 codex P2 #3).
    emitted_pairs: set[tuple[str, str]] = {
        (c.get("scoped_manifest_id", SENTINEL_MANIFEST_ID), c.get("claim_id", ""))
        for c in emitted_citations
    }
    emitted_texts = {c.get("claim_text", "") for c in emitted_citations}

    # INTENDED_NOT_EMITTED — manifest claims missing from emitted set.
    # D6 defines Emitted as a set of claim_text values; the dropped-claim side
    # MUST mirror that. A stale or re-numbered claim_id where the claim_text
    # still appears in the draft would otherwise show up as INTENDED_NOT_EMITTED
    # even though the prose carries the claim — a false drift signal
    # (Step 13 R2 codex P2 finding).
    for m in manifests:
        mid = m.get("manifest_id")
        # If this manifest had any constraint violation, absorb ALL of its
        # drift — Step 13 R5 codex P3. The (mid, cid) pair-level absorption
        # below is preserved for backwards compat, but the scope-level skip
        # is the load-bearing rule per "absorbed in full".
        if mid in constraint_absorbed_manifest_scopes:
            continue
        for claim in m.get("claims", []) or []:
            cid = claim.get("claim_id")
            claim_text = claim.get("claim_text", "")
            if (mid, cid) in emitted_pairs:
                continue
            if claim_text and claim_text in emitted_texts:
                # The draft carries the claim under a different claim_id (e.g.
                # claim_id was re-numbered between manifest emission and prose).
                # D6 set-of-text semantics — not a drop.
                continue
            if (mid, cid) in constraint_absorbed_claim_ids:
                continue
            if claim_text in uncited_sentence_texts:
                # Step 7 codex R1 CO-1 / D-INV-4 cross-aggregate exclusivity:
                # when a manifest claim appears as an uncited sentence in the
                # draft, the uncited_assertion row takes priority. Emitting an
                # INTENDED_NOT_EMITTED drift alongside would fail the D-INV-4
                # consistency lint (one finding per sentence across both
                # aggregates). Mirrors the EMITTED_NOT_INTENDED skip in the
                # loop below.
                continue
            drifts.append(
                _claim_drift_entry(
                    drift_kind="INTENDED_NOT_EMITTED",
                    claim_text=claim_text,
                    finding_id=next_finding_id(),
                    now_iso=now_iso,
                    manifest_claim_id=cid,
                    scoped_manifest_id=mid,
                    section_path=None,
                )
            )

    # EMITTED_NOT_INTENDED — emitted citations whose claim_text is not in any
    # manifest's claim_text set. D6 defines Emitted as a SET of claim_text
    # values, so a drifted claim that carries multiple citations (e.g. one
    # sentence with two ref markers) MUST emit ONE drift row, not one per
    # citation. We dedupe by claim_text here while keeping the first
    # encountered section_path as the representative (Step 13 R1 codex P2).
    all_manifest_texts: set[str] = set()
    for m in manifests:
        for claim in m.get("claims", []) or []:
            text = claim.get("claim_text")
            if text:
                all_manifest_texts.add(text)

    seen_drift_texts: set[str] = set()
    for c in emitted_citations:
        text = c.get("claim_text", "")
        if text in all_manifest_texts:
            continue
        c_scope = c.get("scoped_manifest_id", SENTINEL_MANIFEST_ID)
        c_claim_id = c.get("claim_id", "")
        if c_scope in constraint_absorbed_manifest_scopes:
            # Step 13 R5 codex P3 — manifest scope absorbed in full when any
            # citation in it violated a negative constraint. Suppresses
            # same-manifest drift for emitted citations whose claim_id was
            # NOT in the manifest's declared claim set.
            continue
        if (c_scope, c_claim_id) in constraint_absorbed_claim_ids:
            continue
        if text in uncited_sentence_texts:
            # Precedence rule 3 / D-INV-4 — uncited takes priority.
            continue
        if text in seen_drift_texts:
            # D6 set semantics — one drift row per drifted claim_text.
            continue
        seen_drift_texts.add(text)
        drifts.append(
            _claim_drift_entry(
                drift_kind="EMITTED_NOT_INTENDED",
                claim_text=text,
                finding_id=next_finding_id(),
                now_iso=now_iso,
                manifest_claim_id=None,
                scoped_manifest_id=None,
                section_path=c.get("section_path", "unknown"),
            )
        )

    return drifts


# ---------------------------------------------------------------------------
# Public entry point.
# ---------------------------------------------------------------------------


def run_audit_pipeline(
    *,
    citations: list[dict[str, Any]],
    manifests: list[dict[str, Any]],
    # Reserved for the production retrieval-driver wiring per spec §4 step 2.
    # The current implementation injects retrieval via `retrieve_fn` so the
    # corpus is read inside that callback; keeping the parameter on the
    # signature lets the orchestrator pass corpus through without changing
    # the public API when the production retrieve_fn lands.
    corpus: list[dict[str, Any]] | None = None,
    config: dict[str, Any],
    retrieve_fn: Callable[[dict[str, Any]], dict[str, Any]],
    judge_fn: Callable[..., dict[str, Any]],
    audit_run_id: str,
    now_iso: str,
    cache: dict[str, Any] | None = None,
    uncited_sentences: list[dict[str, Any]] | None = None,
    all_uncited_sentences: list[dict[str, Any]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Run §4 Step 1-6 + manifest set-diff over caller-supplied inputs.

    Two uncited streams (Step 13 R4 codex P1 #2):

    - `uncited_sentences`: D4-c detector positives — output of
      `detect_uncited_assertions` (sentences matching the quantifier /
      empirical-trigger filter). Drives `uncited_assertions[]` LOW-WARN
      advisory emission only.
    - `all_uncited_sentences`: the full uncited sentence set (every draft
      sentence with no in-text citation marker). Drives stream (d) —
      constraint judging for `constraint_violations[]` HIGH-WARN. The full
      set is needed because a manifest negative constraint like "No causal
      language" can be violated by a sentence ("The program caused
      improvement") that the D4-c detector filters OUT (no quantifier, no
      empirical trigger token). Routing constraint judging through the
      D4-c-filtered subset silently drops those HIGH-WARN cases.

    When `all_uncited_sentences` is omitted, it defaults to
    `uncited_sentences` (legacy callers preserved — but a warning band:
    those callers miss the R4 P1 expansion and should pass both).

    The uncited token-rule detector
    (`scripts/uncited_assertion_detector.py`, §"Uncited-assertion detector
    (D4-c)" in claim_ref_alignment_audit_agent.md) is NOT invoked here.
    Callers pre-process the full uncited set through
    `detect_uncited_assertions` to get `uncited_sentences`; pass the raw
    full set as `all_uncited_sentences`. `scripts/test_e2e_claim_audit.py`
    exercises the full detector → pipeline → finalizer chain end-to-end.

    Sentence-dict shape:
      - `uncited_sentences[]`: `sentence_text` + `section_path` +
        `trigger_tokens` (non-empty per U-INV-2). D4-c output guarantees
        these fields.
      - `all_uncited_sentences[]`: `sentence_text` + `section_path` only.
        Constraint judging does not consult `trigger_tokens`.

    Returns:
        dict with six aggregate arrays keyed by passport-aggregate name:
        claim_audit_results, uncited_assertions, claim_drifts,
        constraint_violations, audit_sampling_summaries, plus
        claim_intent_manifests (echoed for downstream consumption).

    Raises:
        ValueError: when config validation fails (e.g. max_claims_per_paper <= 0).
    """
    # Intentional no-op: `corpus` is reserved for the production retrieval-driver
    # wiring (spec §4 step 2). Mark as read so static analysers (ruff ARG002,
    # mypy strict unused-arg) do not flag the forward-compat parameter.
    _ = corpus

    # ---- Config sanity ----
    cap = config.get("max_claims_per_paper", 100)
    if not isinstance(cap, int) or cap <= 0:
        raise ValueError(
            f"max_claims_per_paper must be positive integer; got {cap!r} "
            "(spec §4 step 3 + S-INV-2 / T-P11 cap=0 rejected)"
        )
    judge_model = config.get("judge_model", "gpt-5.5-xhigh")

    # Build the three lookup indexes once per run. Used by per-citation
    # constraint resolution + manifest-level absorption + drift detection.
    manifests_by_id: dict[str, dict[str, Any]] = {
        m["manifest_id"]: m for m in manifests if m.get("manifest_id")
    }
    claim_by_mc_id: dict[tuple[str, str], dict[str, Any]] = {
        (m["manifest_id"], claim["claim_id"]): claim
        for m in manifests
        if m.get("manifest_id")
        for claim in (m.get("claims") or [])
        if claim.get("claim_id")
    }
    mncs_by_manifest_id: dict[str, list[dict[str, Any]]] = {
        m["manifest_id"]: list(m.get("manifest_negative_constraints") or [])
        for m in manifests
        if m.get("manifest_id")
    }
    cache = cache if cache is not None else {}
    uncited_sentences = uncited_sentences or []
    # Step 13 R4 codex P1 #2: constraint judging needs the FULL uncited set,
    # not the D4-c-filtered subset. When the caller omits the full set we
    # fall back to the D4-c subset for backwards compatibility — but that
    # path silently drops constraint violations on sentences outside D4-c
    # trigger tokens. New callers should pass both.
    all_uncited_sentences = (
        all_uncited_sentences if all_uncited_sentences is not None else list(uncited_sentences)
    )

    # ---- Sampling decision ----
    total = len(citations)
    if total > cap:
        sampled_indices = _stratified_bucket_indices(total, cap)
        audited_citations = [citations[i] for i in sampled_indices]
        sampling_summaries = [
            {
                "audit_run_id": audit_run_id,
                "max_claims_per_paper": cap,
                "total_citation_count": total,
                "audited_count": len(sampled_indices),
                "audited_indices": sampled_indices,
                "sampling_strategy": SAMPLING_STRATEGY,
                "emitted_at": now_iso,
            }
        ]
    else:
        audited_citations = list(citations)
        sampling_summaries = []

    # ---- Per-citation §4 Step 1-6 ----
    claim_audit_results: list[dict[str, Any]] = []
    constraint_violations: list[dict[str, Any]] = []
    constraint_absorbed_claim_ids: set[tuple[str, str]] = set()
    # Step 13 R5 codex P3: track manifest_id scopes whose drift is absorbed
    # "in full". A constraint violation in manifest M suppresses ALL of M's
    # drift — declared claims (by id), the violating citation's pair (which
    # may itself be drifted), AND any other emitted citation in M with a
    # non-manifest claim_id.
    constraint_absorbed_manifest_scopes: set[str] = set()

    def _written_scope_for(citation: dict[str, Any]) -> str:
        """Return the scoped_manifest_id that goes onto the claim_audit_result row.

        Step 7 codex R1 CO-2: a drifted-cited citation's `claim_id` is not in
        any manifest, but the citation still arrives with the active
        `scoped_manifest_id` for runtime constraint resolution (so global MNCs
        still apply per M-INV-3). The row written to the passport, however,
        MUST carry the sentinel manifest id whenever the (scope, claim_id)
        pair is not present in the manifest index — otherwise INV-15 dangling
        check rejects the passport. Runtime constraint lookup stays untouched
        (it reads citation.scoped_manifest_id directly); only the persisted
        row is normalized.
        """
        runtime_scope = citation.get("scoped_manifest_id", SENTINEL_MANIFEST_ID)
        cid = citation.get("claim_id")
        if runtime_scope == SENTINEL_MANIFEST_ID:
            return SENTINEL_MANIFEST_ID
        if (runtime_scope, cid) in claim_by_mc_id:
            return runtime_scope
        return SENTINEL_MANIFEST_ID

    for citation in audited_citations:
        anchor_kind = citation.get("anchor_kind")
        scoped_manifest_id = citation.get("scoped_manifest_id", SENTINEL_MANIFEST_ID)
        claim_id = citation.get("claim_id")
        written_scope = _written_scope_for(citation)

        # Step 1 — anchor=none firm-rule short-circuit.
        if anchor_kind == "none":
            entry = _anchorless_entry(
                citation,
                audit_run_id=audit_run_id,
                now_iso=now_iso,
                judge_model=judge_model,
            )
            entry["scoped_manifest_id"] = written_scope
            claim_audit_results.append(entry)
            continue

        # Step 2 — retrieval. Wrap in `_invoke_retrieve` so transient failures
        # surface as INV-14 retrieval_* audit_tool_failure rows instead of
        # aborting the pass (Step 13 R2 codex P2 finding, symmetric to the
        # R1 _invoke_judge wrapper).
        try:
            retrieval = _invoke_retrieve(retrieve_fn, citation)
        except RetrievalInvocationError as ret_err:
            entry = _retrieval_failure_entry(
                citation,
                method="audit_tool_failure",
                audit_run_id=audit_run_id,
                now_iso=now_iso,
                judge_model=judge_model,
                fault_class=ret_err.fault_class,
            )
            entry["rationale"] = f"{ret_err.fault_class}: {ret_err.detail}"
            entry["scoped_manifest_id"] = written_scope
            claim_audit_results.append(entry)
            continue
        method = retrieval["ref_retrieval_method"]
        excerpt = retrieval.get("retrieved_excerpt")

        if method in {"failed", "not_found", "audit_tool_failure"}:
            entry = _retrieval_failure_entry(
                citation,
                method=method,
                audit_run_id=audit_run_id,
                now_iso=now_iso,
                judge_model=judge_model,
                fault_class=retrieval.get("fault_class"),
            )
            entry["scoped_manifest_id"] = written_scope
            claim_audit_results.append(entry)
            continue

        if method not in {"api", "manual_pdf"}:
            raise ValueError(f"unexpected ref_retrieval_method: {method!r}")

        # Step 3 — cache lookup. Active constraints scoped by (manifest, claim).
        active_constraints = _active_constraints_for_claim(
            scoped_manifest_id=scoped_manifest_id,
            claim_id=claim_id,
            claim_by_mc_id=claim_by_mc_id,
            mncs_by_manifest_id=mncs_by_manifest_id,
        )
        key = _cache_key(
            claim_text=citation["claim_text"],
            ref_slug=citation["ref_slug"],
            anchor_kind=anchor_kind,
            anchor_value=citation.get("anchor_value", ""),
            retrieved_excerpt=excerpt,
            active_constraints=active_constraints,
            judge_model=judge_model,
        )
        # In-scope constraint ids for this call. Both fresh judge invocations
        # AND cache hits validate VIOLATED ids against this set so a
        # hallucinated id never reaches `_judge_result_entry` (Step 13 R3
        # codex P2 #1).
        active_ids: frozenset[str] = frozenset(
            c["constraint_id"] for c in active_constraints if c.get("constraint_id")
        )

        cached = cache.get(key)
        try:
            if cached is not None:
                # Step 13 R3 codex P2 #4: cache may carry a corrupted/partial
                # dict from a prior session. Re-validate every hit through the
                # same surface as fresh invocations so a stale entry surfaces
                # as cache_corruption instead of crashing in
                # `_judge_result_entry`.
                judge_result = _validate_judge_dict(
                    cached,
                    allowed_judgments=_CITED_PATH_JUDGMENTS,
                    active_constraint_ids=active_ids,
                    source="cache",
                )
            else:
                # Step 4-5 — passage location is implicit (excerpt is the
                # located passage); invoke judge. Wrap in `_invoke_judge` so
                # transient failures surface as INV-14 `audit_tool_failure`
                # rows instead of aborting the audit (Step 13 R1 codex).
                judge_result = _invoke_judge(
                    judge_fn,
                    allowed_judgments=_CITED_PATH_JUDGMENTS,
                    active_constraint_ids=active_ids,
                    claim_text=citation["claim_text"],
                    retrieved_excerpt=excerpt,
                    anchor_kind=anchor_kind,
                    anchor_value=citation.get("anchor_value", ""),
                    active_constraints=active_constraints,
                    judge_model=judge_model,
                )
                cache[key] = judge_result
        except JudgeInvocationError as judge_err:
            # Cache-hit validation failures map to cache_corruption per INV-14.
            fault_class = "cache_corruption" if cached is not None else judge_err.fault_class
            entry = _retrieval_failure_entry(
                citation,
                method="audit_tool_failure",
                audit_run_id=audit_run_id,
                now_iso=now_iso,
                judge_model=judge_model,
                fault_class=fault_class,
            )
            entry["rationale"] = f"{fault_class}: {judge_err.detail}"
            entry["scoped_manifest_id"] = written_scope
            claim_audit_results.append(entry)
            continue

        # Step 6 — defect_stage routing + emission.
        entry = _judge_result_entry(
            citation,
            judge_result=judge_result,
            ref_retrieval_method=method,
            audit_run_id=audit_run_id,
            now_iso=now_iso,
            judge_model=judge_model,
        )
        entry["scoped_manifest_id"] = written_scope
        claim_audit_results.append(entry)

        # Precedence rule 1: cited constraint violation absorbs the drift signal.
        # Spec §6 lint rule 6 + §7.2 T-P8: when a citation in this manifest
        # judges VIOLATED, that manifest's drift findings are absorbed in
        # full — the constraint violation has already surfaced the L3
        # faithfulness failure at HIGH-WARN, so layering LOW-WARN drift
        # noise on top of it just reports the same paper-level problem twice.
        # Absorption is manifest-scoped (not global) so VIOLATED in
        # manifest A does NOT silence legitimate drift signal in manifest B.
        if entry["defect_stage"] == "negative_constraint_violation":
            manifest = manifests_by_id.get(scoped_manifest_id)
            if manifest is not None:
                for claim in manifest.get("claims", []) or []:
                    cid_in_manifest = claim.get("claim_id")
                    if cid_in_manifest:
                        constraint_absorbed_claim_ids.add(
                            (scoped_manifest_id, cid_in_manifest)
                        )
            # Also absorb the emitted citation's own (manifest, claim) pair
            # so a drifted-yet-violated citation does not produce a
            # companion EMITTED_NOT_INTENDED row.
            constraint_absorbed_claim_ids.add((scoped_manifest_id, claim_id))
            # Step 13 R5 codex P3 — record the full manifest scope so any
            # other emitted citation in M with a drifted claim_id is also
            # absorbed by the drift detector.
            constraint_absorbed_manifest_scopes.add(scoped_manifest_id)

    # ---- Stream (d): uncited constraint judging over FULL uncited set ----
    # Step 13 R4 codex P1 #2: constraint judging MUST see every uncited
    # sentence (not just D4-c detector positives). An MNC like "No causal
    # language" can be violated by an uncited sentence that the D4-c filter
    # drops (no quantifier, no empirical trigger token), so routing
    # constraint judging through the LOW-WARN advisory loop below would
    # silently miss HIGH-WARN cases. We run constraint judging here on
    # `all_uncited_sentences` and emit LOW-WARN uncited_assertion rows
    # separately on `uncited_sentences` (the D4-c subset).
    #
    # Step 13 R6 codex P1: the documented Stage 4 draft sentence shape carries
    # only `sentence_text` / `section_path` / optional `adjacent_text` — NOT
    # a sentence-level `scoped_manifest_id`. Pre-fix this loop required the
    # caller to populate scope on every sentence; absent that, the
    # constraint judge was skipped and the HIGH-WARN-CONSTRAINT-VIOLATION-UNCITED
    # gate was a no-op for orchestrator callers following the contract.
    # The runtime now derives a default scope set per sentence: if the caller
    # provides `scoped_manifest_id` on the sentence dict, only that manifest's
    # MNCs apply; otherwise the pipeline applies EVERY manifest's MNCs
    # (uncited sentences have no claim-level binding, so manifest-scoped
    # MNCs reach them universally per spec §3.5 D4-c stream (d) semantics).
    # Per-manifest constraint sets — MNCs (manifest-wide) PLUS, when the
    # sentence carries a `manifest_claim_id`, that claim's NC-C entries.
    # NC-C (claim-level) is the R7 codex P1 gap: spec §3.5 D4-c stream (d)
    # covers BOTH MNC and NC-C for uncited violations, but the R6 closure
    # only wired MNCs. We resolve NC-C from claim_by_mc_id at call time
    # when the sentence binds a claim_id.
    #
    # Step 13 R7 codex P2 also applies here: when MNC ids collide across
    # manifests (two manifests both have "MNC-1"), passing a flat list to
    # one judge call makes the returned `violated_constraint_id` ambiguous
    # — we'd have to first-match-wins which mis-attributes the row to the
    # wrong manifest. Solution: run the judge ONCE PER MANIFEST, with that
    # manifest's MNC + NC-C set. Each return is unambiguous by construction;
    # cost is N judge calls per sentence (cf. cited path where each
    # citation already takes one judge call).
    manifest_mncs_by_id: dict[str, list[dict[str, Any]]] = {}
    for m in manifests:
        mid = m.get("manifest_id")
        if not mid:
            continue
        mncs_for_mid: list[dict[str, Any]] = []
        for mnc in m.get("manifest_negative_constraints") or []:
            if mnc.get("constraint_id"):
                mncs_for_mid.append(
                    {"constraint_id": mnc["constraint_id"], "rule": mnc["rule"], "scope": "MNC"}
                )
        manifest_mncs_by_id[mid] = mncs_for_mid

    constraint_violation_texts: set[str] = set()
    cv_counter = 1
    # v3.8.2 / #118 — uncited_audit_failures[] aggregate for JudgeInvocationError
    # on the uncited constraint-judging path. Mirrors INV-14 audit_tool_failure
    # on the cited path. Pre-v3.8.2 the failure was silently substituted as
    # NOT_VIOLATED, suppressing HIGH-WARN constraint checks; the UAF aggregate
    # surfaces the operational signal at MED-WARN advisory tier without
    # dropping audit coverage (option 4 — re-raise and abort — was rejected
    # for that exact coverage reason). See spec §3.6.
    uncited_audit_failures: list[dict[str, Any]] = []
    uaf_counter = 1
    for sentence in all_uncited_sentences:
        scoped_manifest_id_for_sentence = sentence.get("scoped_manifest_id")
        sentence_claim_id = sentence.get("manifest_claim_id")

        # Decide which manifests this sentence is constraint-judged against.
        # Caller-pinned scope → that one manifest. Otherwise every manifest.
        if scoped_manifest_id_for_sentence:
            target_manifest_ids = [scoped_manifest_id_for_sentence] if scoped_manifest_id_for_sentence in manifest_mncs_by_id else []
        else:
            target_manifest_ids = list(manifest_mncs_by_id.keys())

        if not target_manifest_ids:
            continue

        # One judge call per (sentence, manifest) pair so MNC id collisions
        # across manifests cannot misattribute the violation (R7 codex P2).
        sentence_violation_recorded = False
        for mid in target_manifest_ids:
            per_manifest_constraints: list[dict[str, Any]] = list(manifest_mncs_by_id[mid])
            # R7 codex P1: also include NC-C for this manifest's bound claim.
            # v3.8.2 / #118 codex P2-2 + R2 P2-1: only set the UAF row's
            # manifest_claim_id when THIS manifest actually owns the claim
            # binding AND at least one NC constraint was added. When sentence
            # carries a sentence_claim_id but the current manifest doesn't
            # have that claim_id, OR the claim exists but has no NC entries
            # (so the failed judge call was MNC-only), the UAF row's
            # manifest_claim_id MUST stay null — the failure is MNC-only at
            # that point and a non-null binding would mislabel downstream
            # consumers about which constraint set the outage hit.
            uaf_manifest_claim_id: str | None = None
            if sentence_claim_id:
                claim = claim_by_mc_id.get((mid, sentence_claim_id))
                if claim is not None:
                    for nc in claim.get("negative_constraints") or []:
                        cid = nc.get("constraint_id")
                        if cid:
                            per_manifest_constraints.append(
                                {"constraint_id": cid, "rule": nc["rule"], "scope": "NC"}
                            )
                            # Only mark NC-C binding when at least one NC
                            # constraint actually entered the judge call.
                            uaf_manifest_claim_id = sentence_claim_id

            if not per_manifest_constraints:
                continue

            applicable_ids: frozenset[str] = frozenset(
                c["constraint_id"] for c in per_manifest_constraints if c.get("constraint_id")
            )
            # Wrap in `_invoke_judge` so transient failures don't abort the
            # uncited stream. v3.8.2 / #118 — JudgeInvocationError now routes
            # to an uncited_audit_failures[] row (MED-WARN advisory, gate
            # passes) instead of synthesising a NOT_VIOLATED verdict. The
            # synthesis substitution shipped pre-v3.8.2 was silently
            # suppressing HIGH-WARN constraint checks on transient judge
            # outage — see spec §3.6 + §4 step 9 fourth bullet for routing,
            # and the design memo at docs/superpowers/plans/2026-05-17-issue-118-*
            # for the option 1-4 trade-off analysis.
            try:
                judge_result = _invoke_judge(
                    judge_fn,
                    allowed_judgments=_UNCITED_PATH_JUDGMENTS,
                    active_constraint_ids=applicable_ids,
                    claim_text=sentence["sentence_text"],
                    retrieved_excerpt=None,
                    anchor_kind=None,
                    anchor_value=None,
                    active_constraints=per_manifest_constraints,
                    judge_model=judge_model,
                )
            except JudgeInvocationError as judge_err:
                uncited_audit_failures.append(
                    _uncited_audit_failure_entry(
                        sentence=sentence,
                        scoped_manifest_id=mid,
                        manifest_claim_id=uaf_manifest_claim_id,
                        fault_class=judge_err.fault_class,
                        detail=judge_err.detail,
                        finding_id=f"UAF-{uaf_counter:03d}",
                        judge_model=judge_model,
                        now_iso=now_iso,
                    )
                )
                uaf_counter += 1
                continue  # no fake NOT_VIOLATED, no CV row, skip to next manifest
            if judge_result.get("judgment") == "VIOLATED":
                constraint_violations.append(
                    _constraint_violation_entry(
                        sentence=sentence,
                        judge_result=judge_result,
                        scoped_manifest_id=mid,
                        finding_id=f"CV-{cv_counter:03d}",
                        judge_model=judge_model,
                        now_iso=now_iso,
                    )
                )
                cv_counter += 1
                sentence_violation_recorded = True

        if sentence_violation_recorded:
            constraint_violation_texts.add(sentence["sentence_text"])

    # ---- Step 6 stream (uncited_assertion LOW-WARN advisory) ----
    # D4-c detector positives only — uncited_sentences is the filtered set.
    uncited_assertions: list[dict[str, Any]] = []
    uncited_sentence_texts: set[str] = set()
    ua_counter = 1

    for sentence in uncited_sentences:
        uncited_sentence_texts.add(sentence["sentence_text"])
        # Always emit uncited_assertion (LOW-WARN advisory). CV-INV-4
        # explicitly permits a sentence to appear in both uncited_assertions[]
        # and constraint_violations[] simultaneously.
        uncited_assertions.append(
            _uncited_assertion_entry(
                sentence=sentence,
                finding_id=f"UA-{ua_counter:03d}",
                now_iso=now_iso,
            )
        )
        ua_counter += 1

    # Also surface uncited_sentence_texts for any constraint-violation
    # sentence text that wasn't a D4-c positive but did violate an MNC.
    # The drift detector reads `uncited_sentence_texts` to apply the
    # D-INV-4 uncited-takes-precedence rule; without including CV-text
    # entries here, a sentence outside D4-c but matching a manifest claim
    # would produce both a constraint_violation row AND a drift row,
    # violating D-INV-4.
    uncited_sentence_texts.update(constraint_violation_texts)

    # ---- Manifest set-diff drift detection ----
    cd_counter = 1

    def _next_cd() -> str:
        nonlocal cd_counter
        out = f"CD-{cd_counter:03d}"
        cd_counter += 1
        return out

    # Step 7 codex R1 CO-4: drift detection's emitted-side index MUST use
    # the FULL citation list, not the sampled subset. Sampling caps judge
    # invocations (spec §4 step 3) — it does NOT shrink the prose visible to
    # the manifest set-diff. Passing audited_citations here made every
    # unsampled-but-present citation look dropped from manifest, producing
    # false INTENDED_NOT_EMITTED rows in proportion to (total - cap).
    claim_drifts = _detect_drifts(
        manifests=manifests,
        emitted_citations=citations,
        uncited_sentence_texts=uncited_sentence_texts,
        constraint_absorbed_claim_ids=constraint_absorbed_claim_ids,
        constraint_absorbed_manifest_scopes=constraint_absorbed_manifest_scopes,
        now_iso=now_iso,
        next_finding_id=_next_cd,
    )

    return {
        "claim_intent_manifests": manifests,
        "claim_audit_results": claim_audit_results,
        "uncited_assertions": uncited_assertions,
        "claim_drifts": claim_drifts,
        "constraint_violations": constraint_violations,
        "audit_sampling_summaries": sampling_summaries,
        "uncited_audit_failures": uncited_audit_failures,
    }
<!-- SOURCE-CONTENT-END -->

<a id="source-scripts-claim-audit-finalizer-py"></a>

## SOURCE: scripts/claim_audit_finalizer.py

<!-- SOURCE-CONTENT-BEGIN bytes=19337 -->
"""ARS v3.8 claim-faithfulness finalizer — 8-row matrix annotations + Stage 6 histogram.

Implements the orchestrator `§3.6 Claim-Faithfulness Audit Gate (v3.8)` matrix
table in `pipeline_orchestrator_agent.md`, plus the Stage 6 reflection
report histogram (renders when ≥5 completed audit entries exist).

The module is invoked by the orchestrator at the Stage 4 → Stage 5 boundary,
AFTER the v3.7.1 Cite-Time Provenance Finalizer resolves anchor presence,
and BEFORE `formatter_agent` runs its hard gate. The classify_* functions
project each passport aggregate row to `{annotation, tier, gate_refuse}`;
`apply_finalizer` reduces over the full passport to produce the
passport-level gate decision + reason list that the formatter consumes.

Spec:
  docs/design/2026-05-15-issue-103-claim-alignment-audit-spec.md §5 (8-row
  matrix), §"Manifest cross-reference (D6)" (drift / constraint routing),
  §3.6 (orchestrator prose).

This module deliberately does NO file I/O — it operates on Python dicts
matching the passport aggregate schemas. The orchestrator handles passport
assembly; the formatter handles refusal surfacing. Single-responsibility
keeps the matrix logic unit-testable.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Any

from scripts._claim_audit_constants import (
    INV14_FAULT_CLASS_TAGS,
    SENTINEL_MANIFEST_ID,
)

# ---------------------------------------------------------------------------
# Severity tiers (per spec §5 finalizer matrix).
# ---------------------------------------------------------------------------

TIER_NONE = "none"
TIER_LOW_WARN = "low_warn"
TIER_MED_WARN = "med_warn"
TIER_HIGH_WARN = "high_warn"

# ---------------------------------------------------------------------------
# Annotation literals (canonical wording per spec §5 table + §"uncited" /
# §"constraint_violation" / §"claim_drifts" subsections + §"audit_sampling").
#
# These literals are the contract surface between the orchestrator and the
# formatter; `formatter_agent.md` REFUSE list reads them via string match.
# Changing a literal here MUST coordinate with the formatter prose update.
# ---------------------------------------------------------------------------

ANNOTATION_CLAIM_AUDIT_AMBIGUOUS = "[CLAIM-AUDIT-AMBIGUOUS]"
ANNOTATION_HIGH_WARN_CLAIM_NOT_SUPPORTED = "[HIGH-WARN-CLAIM-NOT-SUPPORTED]"
ANNOTATION_HIGH_WARN_NEGATIVE_CONSTRAINT_VIOLATION = (
    "[HIGH-WARN-NEGATIVE-CONSTRAINT-VIOLATION ({violated_constraint_id})]"
)
ANNOTATION_HIGH_WARN_FABRICATED_REFERENCE = "[HIGH-WARN-FABRICATED-REFERENCE]"
ANNOTATION_HIGH_WARN_ANCHORLESS = (
    "[HIGH-WARN-CLAIM-AUDIT-ANCHORLESS — v3.7.3 R-L3-1-A VIOLATION REACHED AUDIT]"
)
ANNOTATION_LOW_WARN_UNVERIFIED = (
    "[CLAIM-AUDIT-UNVERIFIED — REFERENCE FULL-TEXT NOT RETRIEVABLE]"
)
ANNOTATION_MED_WARN_TOOL_FAILURE = "[CLAIM-AUDIT-TOOL-FAILURE — {fault_class}]"
# v3.8.2 / #118 — UAF aggregate annotation. Same fault-class enum as the
# cited-path INV-14 row but routed through `uncited_audit_failures[]`
# because claim_audit_result.ref_slug is required.
ANNOTATION_MED_WARN_TOOL_FAILURE_UNCITED = "[CLAIM-AUDIT-TOOL-FAILURE-UNCITED — {fault_class}]"

ANNOTATION_UNCITED_ASSERTION = "[UNCITED-ASSERTION]"
ANNOTATION_HIGH_WARN_CONSTRAINT_VIOLATION_UNCITED = (
    "[HIGH-WARN-CONSTRAINT-VIOLATION-UNCITED ({violated_constraint_id})]"
)
ANNOTATION_LOW_WARN_CLAIM_DRIFT = "[LOW-WARN-CLAIM-DRIFT — kind={drift_kind}]"
ANNOTATION_SAMPLING = (
    "[CLAIM-AUDIT-SAMPLED — {audited_count}/{total_citation_count} audited]"
)

ANNOTATION_MANIFEST_MISSING = (
    "[CLAIM-AUDIT-MANIFEST-MISSING — audit ran without pre-commitment baseline]"
)

# Set of annotation prefixes that `/ars-mark-read` CANNOT clear — structural
# verdicts on prose faithfulness rather than acknowledgement-eligible trust
# states. Mirrors v3.7.3 R-L3-1-A asymmetry (locator is structural).
_UNCLEARABLE_HIGH_WARN_PREFIXES: tuple[str, ...] = (
    "[HIGH-WARN-CLAIM-NOT-SUPPORTED]",
    "[HIGH-WARN-NEGATIVE-CONSTRAINT-VIOLATION",
    "[HIGH-WARN-FABRICATED-REFERENCE]",
    "[HIGH-WARN-CLAIM-AUDIT-ANCHORLESS",
    "[HIGH-WARN-CONSTRAINT-VIOLATION-UNCITED",
)

# Permitted defect_stages for the source-level UNSUPPORTED row (T-F1c).
_UNSUPPORTED_SOURCE_LEVEL_DEFECTS: frozenset[str] = frozenset(
    {"source_description", "metadata", "citation_anchor", "synthesis_overclaim"}
)

# Rationale prefix regex for audit_tool_failure rows — the fault-class tag is
# the leading colon-terminated token per INV-14 (spec §"Error handling").
_RATIONALE_FAULT_CLASS_RE = re.compile(r"^([a-z_]+):")


def _classify_retrieval_failed(
    *,
    defect_stage: str | None,
    ref_retrieval_method: str,
    rationale: str,
) -> dict[str, Any]:
    """Discriminate the three (RETRIEVAL_FAILED, not_applicable) rows by method.

    Raises ValueError on (defect_stage, ref_retrieval_method) combinations not
    covered by the §5 matrix rows. The spec §6 consistency lint
    (`check_claim_audit_consistency.py`) is the authoritative upstream gate
    — it rejects malformed rows BEFORE they reach the finalizer. A raise
    here signals that an out-of-contract row escaped lint (e.g. INV-10 /
    INV-11 / INV-14 violation, or a passport assembled without lint
    validation). Coercing such rows to a default tier would silently mask
    the upstream bug; raising surfaces it.
    """
    if defect_stage == "retrieval_existence" and ref_retrieval_method == "not_found":
        return {
            "annotation": ANNOTATION_HIGH_WARN_FABRICATED_REFERENCE,
            "tier": TIER_HIGH_WARN,
            "gate_refuse": True,
        }
    if defect_stage == "not_applicable":
        if ref_retrieval_method == "not_attempted":
            return {
                "annotation": ANNOTATION_HIGH_WARN_ANCHORLESS,
                "tier": TIER_HIGH_WARN,
                "gate_refuse": True,
            }
        if ref_retrieval_method == "failed":
            return {
                "annotation": ANNOTATION_LOW_WARN_UNVERIFIED,
                "tier": TIER_LOW_WARN,
                "gate_refuse": False,
            }
        if ref_retrieval_method == "audit_tool_failure":
            match = _RATIONALE_FAULT_CLASS_RE.match(rationale)
            fault_class = (
                match.group(1)
                if match and match.group(1) in INV14_FAULT_CLASS_TAGS
                else "retrieval_api_error"
            )
            return {
                "annotation": ANNOTATION_MED_WARN_TOOL_FAILURE.format(fault_class=fault_class),
                "tier": TIER_MED_WARN,
                "gate_refuse": False,
            }
    raise ValueError(
        f"unexpected RETRIEVAL_FAILED row: defect_stage={defect_stage!r} "
        f"ref_retrieval_method={ref_retrieval_method!r}"
    )


def classify_claim_audit_result(entry: dict[str, Any]) -> dict[str, Any]:
    """Apply the §5 8-row matrix to a single claim_audit_result row.

    Returns `{"annotation": str | None, "tier": str, "gate_refuse": bool}`.
    `annotation=None` indicates the SUPPORTED pass row (no formatter output).
    """
    judgment = entry["judgment"]
    defect_stage = entry.get("defect_stage")
    ref_retrieval_method = entry.get("ref_retrieval_method", "not_attempted")
    rationale = entry.get("rationale", "")

    if judgment == "SUPPORTED":
        return {"annotation": None, "tier": TIER_NONE, "gate_refuse": False}

    if judgment == "AMBIGUOUS":
        # Spec §3.1 INV-3 permits {source_description, citation_anchor,
        # synthesis_overclaim, null} on AMBIGUOUS — the §6 consistency lint is
        # the authoritative gate for the allowed-matrix invariant. The matrix
        # row, however, ALWAYS emits the same annotation + tier regardless of
        # which permitted defect_stage the judge picked, so the local
        # `defect_stage` value never affects the return. The previous version
        # of this branch reassigned out-of-set values to None but never read
        # them back — dead code per Step 8 codex /simplify advisory.
        # Validation stays the lint's responsibility (§6 rule 5); this branch
        # produces the LOW-WARN advisory and trusts the schema-validated row.
        return {
            "annotation": ANNOTATION_CLAIM_AUDIT_AMBIGUOUS,
            "tier": TIER_LOW_WARN,
            "gate_refuse": False,
        }

    if judgment == "UNSUPPORTED":
        if defect_stage == "negative_constraint_violation":
            return {
                "annotation": ANNOTATION_HIGH_WARN_NEGATIVE_CONSTRAINT_VIOLATION.format(
                    violated_constraint_id=entry.get("violated_constraint_id", "?")
                ),
                "tier": TIER_HIGH_WARN,
                "gate_refuse": True,
            }
        if defect_stage in _UNSUPPORTED_SOURCE_LEVEL_DEFECTS:
            return {
                "annotation": ANNOTATION_HIGH_WARN_CLAIM_NOT_SUPPORTED,
                "tier": TIER_HIGH_WARN,
                "gate_refuse": True,
            }
        raise ValueError(
            f"UNSUPPORTED row carries unexpected defect_stage={defect_stage!r}; "
            "spec §3.1 INV-2 permits source_description / metadata / citation_anchor / "
            "synthesis_overclaim / negative_constraint_violation only"
        )

    if judgment == "RETRIEVAL_FAILED":
        return _classify_retrieval_failed(
            defect_stage=defect_stage,
            ref_retrieval_method=ref_retrieval_method,
            rationale=rationale,
        )

    raise ValueError(f"unknown judgment: {judgment!r}")


def classify_uncited_assertion(entry: dict[str, Any]) -> dict[str, Any]:
    """LOW-WARN advisory `[UNCITED-ASSERTION]` for every uncited_assertions[] row."""
    return {
        "annotation": ANNOTATION_UNCITED_ASSERTION,
        "tier": TIER_LOW_WARN,
        "gate_refuse": False,
    }


def classify_constraint_violation(entry: dict[str, Any]) -> dict[str, Any]:
    """HIGH-WARN gate-refuse for uncited claim that violates MNC/NC scope."""
    return {
        "annotation": ANNOTATION_HIGH_WARN_CONSTRAINT_VIOLATION_UNCITED.format(
            violated_constraint_id=entry.get("violated_constraint_id", "?")
        ),
        "tier": TIER_HIGH_WARN,
        "gate_refuse": True,
    }


def classify_claim_drift(entry: dict[str, Any]) -> dict[str, Any]:
    """LOW-WARN advisory for drift findings (per D4-a; never gate-refuses)."""
    return {
        "annotation": ANNOTATION_LOW_WARN_CLAIM_DRIFT.format(drift_kind=entry["drift_kind"]),
        "tier": TIER_LOW_WARN,
        "gate_refuse": False,
    }


def classify_uncited_audit_failure(entry: dict[str, Any]) -> dict[str, Any]:
    """MED-WARN advisory for uncited-path judge outage (v3.8.2 / #118).

    Mirrors INV-14 semantics on the uncited path: emits
    `[CLAIM-AUDIT-TOOL-FAILURE-UNCITED — <fault-class>]` next to the
    offending sentence. Gate passes — retry-next-pass remediation.
    UAF-INV-5 (lint) guarantees `fault_class` is one of the seven
    INV14_FAULT_CLASS_TAGS values; we surface the row's literal here.

    The `or "?"` fallback covers both missing-key (KeyError equivalent)
    and explicit-null (`"fault_class": null`) cases — without it a
    malformed row with explicit null would render as `[...— None]`
    (Gemini R2 P3, 2026-05-17). Schema validation rejects either form,
    but a defensive renderer is one less thing to think about.
    """
    return {
        "annotation": ANNOTATION_MED_WARN_TOOL_FAILURE_UNCITED.format(
            fault_class=entry.get("fault_class") or "?",
        ),
        "tier": TIER_MED_WARN,
        "gate_refuse": False,
    }


def classify_audit_sampling_summary(entry: dict[str, Any]) -> dict[str, Any]:
    """Paper-level LOW-WARN annotation when audited_count < total_citation_count (S-INV-3)."""
    if entry["audited_count"] >= entry["total_citation_count"]:
        return {"annotation": None, "tier": TIER_NONE, "gate_refuse": False}
    return {
        "annotation": ANNOTATION_SAMPLING.format(
            audited_count=entry["audited_count"],
            total_citation_count=entry["total_citation_count"],
        ),
        "tier": TIER_LOW_WARN,
        "gate_refuse": False,
    }


def apply_finalizer(passport: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Run the matrix across every passport aggregate; reduce to a gate decision.

    Returns:
        {
            "annotations": list of {entry_ref, annotation, tier},
            "gate_refuse": bool — True if any row has gate_refuse=True,
            "gate_refuse_reasons": list[str] — annotations that triggered refuse,
        }
    """
    annotations: list[dict[str, Any]] = []
    gate_refuse_reasons: list[str] = []

    routing: tuple[tuple[str, Any], ...] = (
        ("claim_audit_results", classify_claim_audit_result),
        ("uncited_assertions", classify_uncited_assertion),
        ("constraint_violations", classify_constraint_violation),
        ("claim_drifts", classify_claim_drift),
        # v3.8.2 / #118 — UAF aggregate routes to MED-WARN advisory.
        # Placed BEFORE audit_sampling_summaries so sentence-level
        # annotations group with the other line-item checks; the
        # paper-level sampling summary belongs at the tail (Gemini R2
        # P3, 2026-05-17). Without this entry, the schema/lint accept
        # UAF rows but the finalizer never surfaces them and the
        # formatter never sees the [CLAIM-AUDIT-TOOL-FAILURE-UNCITED — ...]
        # annotation (Codex R1 P2-1, 2026-05-17).
        ("uncited_audit_failures", classify_uncited_audit_failure),
        ("audit_sampling_summaries", classify_audit_sampling_summary),
    )

    for aggregate_key, classifier in routing:
        for entry in passport.get(aggregate_key, []):
            result = classifier(entry)
            if result["annotation"] is None:
                continue
            annotations.append(
                {
                    "aggregate": aggregate_key,
                    "entry": entry,
                    "annotation": result["annotation"],
                    "tier": result["tier"],
                }
            )
            if result["gate_refuse"]:
                gate_refuse_reasons.append(result["annotation"])

    # MANIFEST-MISSING paper-level advisory (spec §9 acceptance criterion;
    # Step 8 codex R1 P2 closure). Fires when the audit ran without a
    # pre-commitment baseline — both `claim_intent_manifests[]` is empty
    # AND at least one claim_audit_result carries the sentinel scope. The
    # second condition prevents firing on an empty passport (where there's
    # nothing to surface a warning about). Always advisory; never
    # gate-refuses (the audit completed, it just lacks the drift /
    # constraint-inheritance signal a manifest would have provided).
    if not passport.get("claim_intent_manifests"):
        has_sentinel_row = any(
            r.get("scoped_manifest_id") == SENTINEL_MANIFEST_ID
            for r in passport.get("claim_audit_results", [])
        )
        if has_sentinel_row:
            annotations.append(
                {
                    "aggregate": "paper_level",
                    "entry": None,
                    "annotation": ANNOTATION_MANIFEST_MISSING,
                    "tier": TIER_LOW_WARN,
                }
            )

    return {
        "annotations": annotations,
        "gate_refuse": bool(gate_refuse_reasons),
        "gate_refuse_reasons": gate_refuse_reasons,
    }


def render_stage6_histogram(
    claim_audit_results: list[dict[str, Any]],
    *,
    threshold: int = 5,
) -> str | None:
    """Render the per-defect_stage histogram for the AI Self-Reflection Report.

    Threshold is on `audit_status == "completed"` rows (per spec §"Outputs
    feeding Stage 6 self-reflection" literal "≥ 5 completed entries"). When
    fewer than `threshold` completed rows exist, returns None.

    When the threshold is met, the histogram counts rows by `defect_stage`,
    excluding null values (SUPPORTED rows). If every completed row is
    SUPPORTED (zero defects to plot), the histogram still emits — it
    surfaces "No defect stages recorded across N completed entries." so
    the Stage 6 appendix stays consistent and the user sees that the audit
    ran clean rather than wondering whether the histogram was suppressed.

    Step 8 codex R4 P2-1 closure: prior implementation gated the threshold
    on completed-with-defect rows, suppressing the appendix when the
    paper had ≥5 completed audits but ≤4 defect_stage entries. Spec
    literal is "≥ 5 completed entries"; common mostly-SUPPORTED papers
    must still surface the reflection block.

    The output is a stable plain-text rendering keyed by defect_stage; the
    orchestrator embeds it under the Stage 6 reflection appendix. Stage-6
    formatting (markdown headings, separators) is the orchestrator's
    responsibility; this module emits only the histogram block.
    """
    completed = [r for r in claim_audit_results if r.get("audit_status") == "completed"]
    if len(completed) < threshold:
        return None

    defects = [r["defect_stage"] for r in completed if r.get("defect_stage") is not None]
    n_completed = len(completed)

    if not defects:
        return (
            f"Claim-faithfulness defect_stage histogram (n={n_completed} completed entries):"
            f"\n  - No defect stages recorded across {n_completed} completed entries."
        )

    counts = Counter(defects)
    lines = [f"Claim-faithfulness defect_stage histogram (n={n_completed} completed entries):"]
    for stage in sorted(counts):
        lines.append(f"  - {stage}: {counts[stage]}")
    return "\n".join(lines)


def ars_mark_read_clears(*, annotation: str, tier: str) -> bool:
    """Return True iff `/ars-mark-read` can promote the annotation to cleared state.

    HIGH-WARN classes covering structural verdicts on prose faithfulness CANNOT
    be cleared by acknowledgement (T-F3 asymmetry, mirrors v3.7.3 R-L3-1-A).
    LOW-WARN paywall / advisory rows CAN — the user has accepted the
    unverifiable state and chosen to ship.

    The MED-WARN audit_tool_failure row is NOT acknowledgement-clearable
    either (the remediation is retry on next pipeline pass, not
    acknowledgement); it stays surfaced until a fresh audit pass resolves
    the underlying infrastructure problem or downgrades to LOW-WARN paywall.
    """
    if tier == TIER_HIGH_WARN:
        return False
    if tier == TIER_MED_WARN:
        return False
    # The HIGH-WARN-prefix check below is defense-in-depth against
    # caller bugs where a HIGH-WARN annotation arrives with mismatched
    # tier=TIER_LOW_WARN (e.g. a passport hand-edit or a downstream
    # consumer that lost the tier mapping). Well-formed inputs never
    # trigger this branch — every HIGH-WARN prefix is produced only by
    # the matrix paths that also set tier=TIER_HIGH_WARN. Keeping the
    # check rather than dropping it preserves the safety surface; a
    # silent True return on a mistyped HIGH-WARN would acknowledge a
    # gate-refuse-class violation as cleared.
    return tier == TIER_LOW_WARN and not any(
        annotation.startswith(prefix) for prefix in _UNCLEARABLE_HIGH_WARN_PREFIXES
    )
<!-- SOURCE-CONTENT-END -->

<a id="source-scripts-claim-audit-constants-py"></a>

## SOURCE: scripts/_claim_audit_constants.py

<!-- SOURCE-CONTENT-BEGIN bytes=8324 -->
"""Shared constants for v3.8 claim-faithfulness audit.

Single source of truth for the literals + regexes that appear in BOTH the
lint (`check_claim_audit_consistency.py`) and the pipeline runtime
(`claim_audit_pipeline.py`). Re-declaring these in both places opens a
drift hole — a spec bump that updates the lint without updating the
runtime would change one side silently. Tests cover both call sites; the
shared import binds them.

See docs/design/2026-05-15-issue-103-claim-alignment-audit-spec.md §3.1
(matrix + INV catalogue) and §4 step 3 (sampling) for canonical
definitions.
"""
from __future__ import annotations

import re

# Canonical sentinel for the MANIFEST-MISSING fallback path (spec §3.1 INV-15).
SENTINEL_MANIFEST_ID = "M-0000-00-00T00:00:00Z-0000"

# INV-6 canonical rationale prefix (v3.7.3 R-L3-1-A firm rule).
INV6_RATIONALE_PREFIX = "v3.7.3 R-L3-1-A violation"

# INV-14 audit-tool-failure rationale fault-class tags.
INV14_FAULT_CLASS_TAGS: tuple[str, ...] = (
    "judge_timeout",
    "judge_api_error",
    "judge_parse_error",
    "cache_corruption",
    "retrieval_api_error",
    "retrieval_timeout",
    "retrieval_network_error",
)

# Sampling strategy literal (S-INV schema constant).
SAMPLING_STRATEGY = "stratified_buckets_v1"

# rule_version literals for v3.8.0 release. Future revisions bump the literal
# and require re-lint per spec §3.3 / §3.4 / §3.5.
UNCITED_RULE_VERSION = "D4-c-v1"
DRIFT_RULE_VERSION = "D4-a-v1"
# v3.8.2 / #118 — uncited_audit_failure rule_version literal (§3.6).
# Distinct prefix from D4-c-v1 (uncited_assertion D4-c detector) and
# D4-a-v1 (constraint_violation) so the lint can route by literal.
UAF_RULE_VERSION = "D4-c-v1-uaf-v1"

# Constraint id parse rules (spec §3.2 + INV-17 canonical form).
RE_NC_CONSTRAINT = re.compile(r"^NC-C([0-9]{3,})-([0-9]+)$")
RE_MNC_CONSTRAINT = re.compile(r"^MNC-([0-9]+)$")
RE_CLAIM_ID = re.compile(r"^C-([0-9]{3,})$")

# Schema rejects this pattern, but for malformed-on-purpose fixtures the lint
# surfaces INV-17 explicitly before schema validation runs.
RE_NC_INNER_HYPHEN = re.compile(r"^NC-C-[0-9]+-[0-9]+$")

# ---------------------------------------------------------------------------
# D4-c uncited-assertion detector constants (spec §"Uncited-assertion
# detector (D4-c)" in claim_ref_alignment_audit_agent.md).
#
# Centralised here so pipeline runtime, lint, and detector share one source
# of truth — a spec bump touches one literal, not three.
# ---------------------------------------------------------------------------

# Condition 1: empirical-claim verbs (case-insensitive whole-word match).
# Spec list: showed, demonstrated, observed, proved, confirmed.
UNCITED_EMPIRICAL_VERBS: frozenset[str] = frozenset(
    {"showed", "demonstrated", "observed", "proved", "confirmed"}
)

# Condition 1: fuzzy English quantifier words (case-insensitive whole-word).
# Spec list: most, several, two-thirds. Kept literal; numerical / percent
# quantifiers are caught by RE_NUMERIC_QUANTIFIER below.
UNCITED_FUZZY_QUANTIFIERS: frozenset[str] = frozenset(
    {"most", "several", "two-thirds"}
)

# Condition 1: numerical quantifier regex. Spec line 250 lists three numeric
# classes — `numbers / percentages / explicit quantifiers (50%, 67 of 100)`.
# All three fire D4-c condition 1; the detector then applies a guard pass
# (RE_NUMERIC_QUANTIFIER_GUARD below) that rejects matches whose surrounding
# context proves them to be years, version triples, or section numbers
# instead of quantifiers. Splitting into match-broadly + guard-narrowly is
# easier to read and to test than stuffing every exclusion into a single
# regex's negative lookaheads. The detector concatenates the matched
# substring into trigger_tokens verbatim so the schema's minItems=1
# invariant holds.
RE_NUMERIC_QUANTIFIER = re.compile(
    # Order matters: longest-prefix-first so percent and "N of M" bind
    # before the bare-number branch swallows the leading digits.
    r"\b\d+(?:\.\d+)?%"                  # percent quantifier
    r"|\b\d+(?:\.\d+)?\s+of\s+\d+\b"     # "N of M" quantifier idiom
    r"|\b\d+(?:\.\d+)*\b"                # bare number, possibly dotted
                                          # (3+ segments routed to guard
                                          # as version/section)
)

# Condition 1 guard: rejects bare-number matches whose surrounding context
# identifies them as years, version triples, or section numbers — none of
# those are quantitative claims, and treating them as such produced
# false-positive LOW-WARN advisories before the guard landed (see codex
# R1 P1-3). Applied AFTER RE_NUMERIC_QUANTIFIER to the matched substring +
# its character offsets in the sentence; bare-number matches that satisfy
# any guard branch are dropped, percent and `N of M` matches always pass
# through.
#
# Guard branches:
#   1. Standalone 4-digit year in plausible academic range (1900-2099).
#   2. Version triple `X.Y.Z` (dotted form with 3+ segments — the broad
#      regex captures only the first two segments, so we re-scan).
#   3. Dotted section number `X.Y[.Z…]` (treated as section ref, not
#      quantifier). Distinguished from version by `section` / `§` /
#      `chapter` / `figure` / `table` cue word within a 24-char left
#      window, OR by `v` immediately preceding (version literal).
RE_BARE_NUMERIC_YEAR = re.compile(r"^(19|20)\d{2}$")
RE_DOTTED_TRIPLE_OR_MORE = re.compile(r"^\d+(?:\.\d+){2,}$")
RE_DOTTED_PAIR = re.compile(r"^\d+\.\d+$")
RE_SECTION_CUE = re.compile(
    r"(?:section|chapter|figure|table|fig\.|tbl\.|step|appendix|§)\s*$",
    re.IGNORECASE,
)
RE_VERSION_PREFIX = re.compile(r"v\s*$", re.IGNORECASE)
# Catches the case where Python's `\b` fails between a letter and a digit
# (both are \w characters) — e.g. `v3.7.3` has no \b between `v` and `3`,
# so RE_NUMERIC_QUANTIFIER starts matching from the SECOND segment (`7.3`)
# and the guard never sees the version-triple shape. This pattern detects
# a digit-then-dot prefix immediately attached to the left of the match.
# Requires exactly one digit-run + `.` ending the window — combined with
# the surrounding match (also dotted or bare number), this signals a
# multi-segment dotted form that should be treated as a version/section
# reference rather than a quantifier.
RE_NUMERIC_LEFT_ATTACHED = re.compile(r"\d+\.$")

# Condition 2: three-layer-citation ref-marker probe. Presence probe
# WITHIN the v3.7.3 ref-marker namespace — accepts any `<!--ref:...-->`
# shape where the slug payload begins with a non-whitespace character,
# rejects HTML comments that happen to start with `ref:` but use it as
# a label rather than a citation marker (e.g.
# `<!-- ref: $internal.notebook.cell -->`).
#
# Iteration history:
#   R0 `[^-]+`                                — rejected hyphenated slugs.
#   R1 `[A-Za-z][A-Za-z0-9_:-]* + 0-2 tokens` — rejected digit-leading
#                                                 slugs, plus-sign slugs,
#                                                 and 3+ status tokens.
#   R2 `[^>]*?`                                — too broad; matched
#                                                 `<!-- ref: $analysis -->`
#                                                 and similar code/internal
#                                                 ref comments (codex
#                                                 R3 P2-NEW-A).
#   R3 `[^\s>][^>]*?`                          — current. Slug must begin
#                                                 with a non-whitespace
#                                                 non-`>` character; the
#                                                 v3.7.3 strict validator
#                                                 in
#                                                 scripts/check_v3_7_3_three_layer_citation.py
#                                                 catches any remaining
#                                                 shape errors.
RE_REF_MARKER = re.compile(r"<!--\s*ref:[^\s>][^>]*?-->")

# Condition 3: definitional-phrase substrings (case-insensitive). Spec list:
# `refers to`, `is defined as`, `we define`, `for the purposes of`.
UNCITED_DEFINITION_PHRASES: tuple[str, ...] = (
    "refers to",
    "is defined as",
    "we define",
    "for the purposes of",
)
<!-- SOURCE-CONTENT-END -->

<a id="source-scripts-uncited-assertion-detector-py"></a>

## SOURCE: scripts/uncited_assertion_detector.py

<!-- SOURCE-CONTENT-BEGIN bytes=11912 -->
"""D4-c uncited-assertion token-rule detector.

Implements the three-condition rule pinned in
`academic-pipeline/agents/claim_ref_alignment_audit_agent.md`
§"Uncited-assertion detector (D4-c)" and exercised by
`scripts/test_uncited_assertion.py` (T-U1..T-U5).

A sentence becomes an `uncited_assertion` candidate iff ALL THREE hold:

  1. Quantifier-or-empirical-verb present
     (numbers `42 participants`, percentages `50%`, explicit quantifiers
     `most`/`several`/`two-thirds`, empirical verbs `showed`/`demonstrated`/
     `observed`/`proved`/`confirmed`). Bare-number matches are filtered by
     a guard pass that rejects years, version triples, and section numbers.
  2. No `<!--ref:slug-->` marker on the sentence.
  3. Not a definitional sentence (`refers to`/`is defined as`/`we define`/
     `for the purposes of`).

D4-c last paragraph: manifest membership does NOT exempt a sentence.
The wrapper `detect_uncited_assertions` preserves caller-supplied
`manifest_claim_id` / `scoped_manifest_id` on every finding so the
downstream pipeline can populate U-INV-4 cross-array integrity.

Cross-sentence / adjacent-clause check (Step 9 closure): the wrapper
`detect_uncited_assertions` accepts an optional `adjacent_text` field
on each sentence dict. When supplied, that surrounding-clause window
is scanned for a `<!--ref:slug-->` marker via the same condition-2
regex; if found, the candidate is filtered out. Callers supply the
window during the Step 9 e2e wiring (see
`scripts/test_e2e_claim_audit.py`). Without `adjacent_text` the
wrapper preserves the v3.8 Step 6 single-sentence behavior.

Detector outputs feed into the existing pipeline routing in
`scripts/claim_audit_pipeline.py::run_audit_pipeline`'s
`uncited_sentences` parameter — this module is the pre-processing
layer that turns raw draft sentences into the dicts the pipeline
expects.
"""
from __future__ import annotations

import re
from typing import Any, Iterable

from scripts._claim_audit_constants import (
    RE_BARE_NUMERIC_YEAR,
    RE_DOTTED_PAIR,
    RE_DOTTED_TRIPLE_OR_MORE,
    RE_NUMERIC_LEFT_ATTACHED,
    RE_NUMERIC_QUANTIFIER,
    RE_REF_MARKER,
    RE_SECTION_CUE,
    RE_VERSION_PREFIX,
    UNCITED_DEFINITION_PHRASES,
    UNCITED_EMPIRICAL_VERBS,
    UNCITED_FUZZY_QUANTIFIERS,
)

# Whole-word splitter for condition 1 fuzzy / verb matching. Strips
# punctuation so `"showed."` and `"showed,"` both match.
_RE_WORD = re.compile(r"[A-Za-z][A-Za-z-]*")

# Left-context window length for guard pass cue detection. 24 chars covers
# `cf. Section ` and `as shown in Figure ` while avoiding catching cue
# words from a previous clause separated by punctuation.
_GUARD_LEFT_WINDOW = 24


def _is_year_or_version_or_section(
    sentence: str, match_text: str, match_start: int
) -> bool:
    """Guard pass: return True when a bare-number match is NOT a quantifier.

    Four disqualifying shapes:
      1. 4-digit year in plausible academic range (1900-2099).
      2. Dotted X.Y.Z[.W...] form — version triple OR deep section number.
      3. Bare integer OR dotted X.Y form preceded by a section cue
         (`section`, `figure`, `chapter`, `table`, `fig.`, `tbl.`,
         `step`, `appendix`, `§`) — covers `Table 2`, `Section 5`,
         `Figure 3` (bare-integer cue refs) AND `Section 3.1`,
         `Figure 3.2` (dotted-pair cue refs). The bare-integer arm was
         missing in R3 and surfaced as codex R4 P2-NEW-C.
      3b. Dotted X.Y form preceded by `v` (version literal) — distinct
          from the section cue because a bare integer after `v ` is
          ambiguous (`v 5 participants` is gibberish in academic prose,
          so the version-prefix-bare-integer combination is not common
          enough to warrant a guard arm; the dotted-pair branch keeps
          `v3.7` rejection.
      4. Any match (bare or dotted) whose immediate left neighbour is a
         dotted-number suffix like `3.` — handles the case where Python's
         `\\b` does not fire between a letter and a digit (e.g. `v3.7.3`
         has no \\b between `v` and `3`, so RE_NUMERIC_QUANTIFIER starts
         from the SECOND segment `7.3`; this branch reattaches the prefix
         and classifies the full token as a version/section reference).

    Percent (`50%`) and `N of M` matches never reach this guard — the
    caller is responsible for routing only bare-number matches through.
    """
    if RE_BARE_NUMERIC_YEAR.match(match_text):
        return True
    if RE_DOTTED_TRIPLE_OR_MORE.match(match_text):
        # Three-or-more-segment dotted forms are unambiguously version
        # triples or deep section numbers; no quantitative claim ever
        # writes "50.3.1 of participants".
        return True
    # Branch 3: section cue applies to both bare integers and dotted pairs
    # (`Table 2` and `Section 3.1` are both section refs); the version
    # prefix applies only to dotted pairs (`v3.7` is a version literal,
    # but bare `v 5` is uncommon enough that the false-negative cost
    # outweighs the false-positive risk).
    left = sentence[max(0, match_start - _GUARD_LEFT_WINDOW) : match_start]
    if RE_SECTION_CUE.search(left):
        return True
    if RE_DOTTED_PAIR.match(match_text) and RE_VERSION_PREFIX.search(left):
        return True
    # Branch 4: reattach a left-side dotted-number prefix that Python's \b
    # failed to separate. RE_NUMERIC_QUANTIFIER consumed every dotted
    # segment to the right of the prefix already, so the only token that
    # can sit immediately before match_start and still belong to the same
    # logical version/section literal is `\d+\.`.
    #
    # Two reattachment shapes:
    #   (i)  Immediate (no whitespace between prefix and match): the
    #        canonical `v3.7.3` shape where the regex starts at `7.3`
    #        because Python's \b cannot separate `v` and `3`.
    #   (ii) Line-wrapped (whitespace between prefix and match): the
    #        codex R2 P1-NEW shape `v3.\n7.3`.
    #
    # Shape (ii) is restricted to dotted matches only — a bare integer
    # after whitespace after a period belongs to the NEXT sentence, not
    # the version triple. `"v3. 7 participants withdrew."` is two
    # statements: a version reference (the `v3.` is a section end) and
    # a quantitative claim about 7 participants. Without this restriction
    # branch 4 swallowed the legitimate 7-participant count (codex R3
    # P2-NEW-B).
    if match_start > 0:
        # Shape (i) — immediate left `.` always reattaches.
        if sentence[match_start - 1] == ".":
            left_search_start = max(0, match_start - _GUARD_LEFT_WINDOW)
            left = sentence[left_search_start:match_start]
            if RE_NUMERIC_LEFT_ATTACHED.search(left):
                return True
        # Shape (ii) — whitespace-separated only for dotted right tails.
        elif "." in match_text and sentence[match_start - 1].isspace():
            scan_idx = match_start - 1
            while scan_idx > 0 and sentence[scan_idx].isspace():
                scan_idx -= 1
            if sentence[scan_idx] == ".":
                left_search_start = max(0, scan_idx + 1 - _GUARD_LEFT_WINDOW)
                left = sentence[left_search_start : scan_idx + 1]
                if RE_NUMERIC_LEFT_ATTACHED.search(left):
                    return True
    return False


def detect_uncited(sentence: str) -> tuple[bool, list[str]]:
    """Return `(is_candidate, trigger_tokens)` for one sentence.

    Trigger tokens are returned in document order (left-to-right in the
    source sentence) so passport diffs and human review stay aligned with
    reader expectations. Duplicates are dropped via order-preserving
    dedup so `"showed ... showed ... showed"` produces one token.
    """
    # Condition 3 fires first — if the sentence is definitional we never
    # need to inspect quantifier tokens.
    lowered = sentence.lower()
    if any(phrase in lowered for phrase in UNCITED_DEFINITION_PHRASES):
        return False, []

    # Condition 2 — ref marker present means the sentence is properly
    # cited under v3.7.3 Three-Layer Citation Emission.
    if RE_REF_MARKER.search(sentence):
        return False, []

    # Condition 1 — collect every quantifier / verb match with its byte
    # offset so the final token list reflects document order regardless
    # of which regex / pass produced it.
    matches: list[tuple[int, str]] = []
    for m in RE_NUMERIC_QUANTIFIER.finditer(sentence):
        text = m.group(0)
        # Percent and `N of M` matches always pass through; only bare-
        # number matches need the year/version/section guard. The two
        # qualified shapes are distinguishable by character content:
        # percent ends with `%`, `N of M` contains ` of `.
        if "%" not in text and " of " not in text:
            if _is_year_or_version_or_section(sentence, text, m.start()):
                continue
        matches.append((m.start(), text))

    # Fuzzy quantifiers + empirical verbs match on lower-cased whole words.
    triggers = UNCITED_FUZZY_QUANTIFIERS | UNCITED_EMPIRICAL_VERBS
    for m in _RE_WORD.finditer(sentence):
        token = m.group(0).lower()
        if token in triggers:
            matches.append((m.start(), token))

    # Sort by source offset, then dedup preserving first occurrence.
    matches.sort(key=lambda pair: pair[0])
    trigger_tokens = list(dict.fromkeys(token for _, token in matches))
    return (bool(trigger_tokens), trigger_tokens)


def detect_uncited_assertions(
    sentences: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Filter raw draft sentences down to D4-c candidates.

    Each input dict MUST carry a non-empty string `sentence_text`. Missing
    or non-string `sentence_text` raises `ValueError` — silently treating
    bad input as empty would let upstream bugs masquerade as
    "no findings", which is the worst possible failure mode for an audit
    pipeline.

    Optional fields (`section_path`, `manifest_claim_id`,
    `scoped_manifest_id`, `upstream_owner_agent`) pass through unchanged.
    The detector enriches the candidate dict with `trigger_tokens`
    (non-empty per U-INV-2) and drops sentences that fail any of the
    three D4-c conditions.

    The wrapper does NOT mint `finding_id` / `detected_at` / `rule_version`
    — those are owned by `claim_audit_pipeline._uncited_assertion_entry`
    so the passport-write side stays the single point of authority over
    schema-required fields.
    """
    candidates: list[dict[str, Any]] = []
    for index, raw in enumerate(sentences):
        if "sentence_text" not in raw:
            raise ValueError(
                f"detect_uncited_assertions: sentences[{index}] missing "
                "required 'sentence_text' key"
            )
        sentence_text = raw["sentence_text"]
        if not isinstance(sentence_text, str):
            raise ValueError(
                f"detect_uncited_assertions: sentences[{index}]['sentence_text'] "
                f"must be str, got {type(sentence_text).__name__}"
            )
        is_candidate, tokens = detect_uncited(sentence_text)
        if not is_candidate:
            continue
        # Step-9 adjacent-clause filter. When the caller supplies an
        # `adjacent_text` window (the surrounding clause / preceding +
        # following sentence text per spec line 251), a ref marker inside
        # it owns the citation and the candidate is suppressed. Empty /
        # missing windows preserve v3.8 Step-6 single-sentence behavior.
        adjacent_text = raw.get("adjacent_text")
        if isinstance(adjacent_text, str) and RE_REF_MARKER.search(adjacent_text):
            continue
        enriched = dict(raw)
        enriched["trigger_tokens"] = tokens
        candidates.append(enriched)
    return candidates


__all__ = ["detect_uncited", "detect_uncited_assertions"]
<!-- SOURCE-CONTENT-END -->
