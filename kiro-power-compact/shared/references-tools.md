<a id="source-shared-cross-model-verification-md"></a>

## SOURCE: shared/cross_model_verification.md

<!-- SOURCE-CONTENT-BEGIN bytes=11173 -->
# Cross-Model Verification Protocol (v3.0)

## Overview

This protocol enables optional cross-model verification for high-stakes AI judgments. When enabled, a second AI model independently reviews outputs from the primary model, reducing shared-bias blind spots.

**This is entirely optional.** All ARS skills work with Claude Opus 4.7 alone. Cross-model verification is an additional layer for users who want higher confidence in integrity checks, devil's advocate challenges, and review judgments.

## Why Cross-Model Verification

A stress test of 68 AI-generated citations found 31% had problems — and all passed three rounds of same-model integrity checks. The root cause: the verifying AI and the generating AI share the same training data distribution, so they share the same blind spots. A different model (trained on overlapping but not identical data, with different RLHF tuning) can catch errors that the primary model systematically misses.

**What it improves:** Error rate reduction (estimated 31% → ~5-10%). Different models catch different types of hallucination patterns.

**What it doesn't solve:** Frame-lock (all LLMs share most training data), sycophancy (all RLHF models have this tendency). These are degree improvements, not kind improvements.

## Supported Models

| Model | API ID | Provider | Best For |
|-------|--------|----------|----------|
| Claude Opus 4.7 | `claude-opus-4-7` | Anthropic | Primary model (default for all ARS skills) |
| GPT-5.4 Pro | `gpt-5.4-pro` | OpenAI | Cross-verification — strongest reasoning |
| GPT-5.4 | `gpt-5.4` | OpenAI | Cross-verification — balanced cost/performance |
| Gemini 3.1 Pro | `gemini-3.1-pro-preview` | Google | Cross-verification — strong at factual verification |

**Recommended cross-verification pair:** Claude Opus 4.7 (primary) + GPT-5.4 Pro or Gemini 3.1 Pro (verifier).

Using two non-Anthropic models as primary+verifier is possible but not tested with ARS prompts.

## Setup Guide

### Prerequisites

You need API keys from at least one additional provider. ARS itself runs inside Claude Code, so Claude is always available as the primary model.

### Step 1: Get API Keys

**OpenAI (GPT-5.4):**
1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key (starts with `sk-`)

**Google (Gemini 3.1 Pro):**
1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Create a new API key
3. Copy the key (starts with `AIza`)

### Step 2: Set Environment Variables

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
# Optional: Cross-model verification for ARS
export OPENAI_API_KEY="sk-your-key-here"
export GOOGLE_AI_API_KEY="AIza-your-key-here"

# Choose your preferred cross-verification model
# Options: gpt-5.4-pro, gpt-5.4, gemini-3.1-pro-preview
export ARS_CROSS_MODEL="gpt-5.4-pro"
```

Then reload: `source ~/.zshrc`

### Step 3: Verify Setup

In Claude Code, you can test by asking:
```
Check if cross-model verification is available for ARS
```

The system will check for the environment variables and report which models are available.

### Step 4: Enable Per-Session (Optional)

If you don't want cross-model verification running all the time, you can enable it per session:

```bash
# Enable for this session only
export ARS_CROSS_MODEL="gpt-5.4-pro"

# Disable for this session
unset ARS_CROSS_MODEL
```

## How It Works in Each Skill

### Integrity Verification (academic-pipeline, Stage 2.5 / 4.5)

**When `ARS_CROSS_MODEL` is set:**
- Primary model (Claude) runs full Phase A-E verification as normal
- After Phase A completes, a random 30% sample of references is sent to the cross-model for independent verification
- Cross-model receives only the reference text and paper context — not Claude's verification result (to prevent anchoring)
- Disagreements are flagged as `[CROSS-MODEL-DISAGREEMENT]` and prioritized for human review

**When `ARS_CROSS_MODEL` is not set:**
- Standard single-model verification (unchanged from v2.7+)

**Implementation for agents:**

When the integrity_verification_agent detects `ARS_CROSS_MODEL` in the environment, it should:

1. Complete Phase A verification normally
2. Select 30% of references randomly (minimum 5, maximum 15). If total references < 5, sample all of them.
3. Batch up to 5 references per API call to reduce latency (e.g., 15 sampled refs = 3 API calls). For each batch, construct a verification prompt:
   ```
   Verify each of these academic references independently. For each,
   check: Does it exist? Are the author names, year, title, journal,
   and DOI correct? Search the web to confirm.

   For each reference, respond with: VERIFIED / NOT_FOUND / MISMATCH (with details)

   Reference 1: [full reference text] — Context: [sentence where cited]
   Reference 2: [full reference text] — Context: [sentence where cited]
   ... (up to 5 per batch)
   ```
4. Send to the cross-model via the appropriate API (see API Call Patterns below)
5. Compare results: if Claude said VERIFIED but cross-model said NOT_FOUND or MISMATCH, flag as `[CROSS-MODEL-DISAGREEMENT]`
6. Include disagreements in the integrity report under a new section:
   ```markdown
   ### Cross-Model Verification Results
   - References sampled: X/Y (Z%)
   - Agreements: N
   - Disagreements: M (listed below, prioritized for human review)

   | # | Reference | Claude | Cross-Model | Status |
   |---|-----------|--------|-------------|--------|
   ```

### Devil's Advocate (deep-research + academic-paper-reviewer)

**When `ARS_CROSS_MODEL` is set:**
- After the DA completes its standard review/checkpoint, the cross-model receives the same material and generates an independent critique
- The DA then compares: any CRITICAL or MAJOR issues found by the cross-model but not by the DA are added as `[CROSS-MODEL-FINDING]`
- This directly addresses frame-lock — a different model may attack from a different angle

**When `ARS_CROSS_MODEL` is not set:**
- Standard single-model DA (unchanged)

**Implementation:**

The DA agent, after completing its checkpoint report, should:

1. Send the reviewed material + a simplified DA prompt to the cross-model:
   ```
   You are a devil's advocate reviewing this [research/paper].
   Find the 3 most serious weaknesses. For each, state:
   - What the weakness is
   - Why it matters
   - What the strongest counter-argument would be

   Material: [the reviewed content]
   ```
2. Compare cross-model findings with own findings
3. Any cross-model finding not already covered → add to report as `[CROSS-MODEL-FINDING]`
4. Log: `[CROSS-MODEL: X findings received, Y novel (not in primary DA report)]`

### Peer Review (academic-paper-reviewer) — Future

> **Status: Planned, not yet implemented.** No agent currently owns the 6th reviewer behavior. This will be added in a future version, likely as a cross-model section in `eic_agent.md`. For now, cross-model verification in peer review is limited to the DA's independent critique (above).

**Planned behavior when `ARS_CROSS_MODEL` is set:**
- Cross-model acts as an additional independent reviewer (6th reviewer)
- Its scores are shown separately, not averaged into the existing 5-reviewer consensus
- Significant score divergence (>15 points on any dimension) is flagged

## API Call Patterns

### OpenAI (GPT-5.4 / GPT-5.4 Pro)

In Claude Code, the agent can use the Bash tool to make API calls:

```bash
curl -s https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "'"$ARS_CROSS_MODEL"'",
    "messages": [
      {"role": "system", "content": "You are a verification assistant."},
      {"role": "user", "content": "'"$(echo "$PROMPT" | jq -Rs .)"'"}
    ],
    "temperature": 0.1,
    "max_tokens": 2000
  }' | jq -r '.choices[0].message.content'
```

### Google Gemini (Gemini 3.1 Pro)

```bash
# PROMPT must be set before calling. Use jq to JSON-escape it.
curl -s "https://generativelanguage.googleapis.com/v1beta/models/${ARS_CROSS_MODEL}:generateContent?key=$GOOGLE_AI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "'"$(echo "$PROMPT" | jq -Rs .)"'"}]}],
    "generationConfig": {"temperature": 0.1, "maxOutputTokens": 2000}
  }' | jq -r '.candidates[0].content.parts[0].text'
```

### Detecting Available Models

Agents should check at the start of a verification/review session:

```bash
# Check which cross-model APIs are available
# Requires: jq (for JSON parsing). Fallback: python3 -c "import sys,json; ..."
if ! command -v jq &>/dev/null; then
  echo "WARNING: jq not installed. Cross-model API calls will use python3 fallback."
fi

if [ -n "$ARS_CROSS_MODEL" ]; then
  case "$ARS_CROSS_MODEL" in
    gpt-5.4*) 
      [ -n "$OPENAI_API_KEY" ] && echo "CROSS_MODEL_AVAILABLE=openai" \
        || echo "WARNING: ARS_CROSS_MODEL=$ARS_CROSS_MODEL but OPENAI_API_KEY is not set" ;;
    gemini*) 
      [ -n "$GOOGLE_AI_API_KEY" ] && echo "CROSS_MODEL_AVAILABLE=google" \
        || echo "WARNING: ARS_CROSS_MODEL=$ARS_CROSS_MODEL but GOOGLE_AI_API_KEY is not set" ;;
    *) echo "WARNING: ARS_CROSS_MODEL=$ARS_CROSS_MODEL is not a supported model. Supported: gpt-5.4, gpt-5.4-pro, gemini-3.1-pro-preview"
       echo "CROSS_MODEL_AVAILABLE=none" ;;
  esac
else
  echo "CROSS_MODEL_AVAILABLE=none"
fi
```

If `ARS_CROSS_MODEL` is set but the corresponding API key is missing or the model name is unsupported, the agent should warn the user and proceed with single-model verification.

## Cost Considerations

Cross-model verification adds API costs from the second provider:

| Scenario | Additional Calls | Estimated Additional Cost |
|----------|-----------------|--------------------------|
| Integrity verification (30% of 60 refs, batched 5/call) | ~4 calls | ~$0.30-0.60 |
| DA cross-check (1 per checkpoint, 3 checkpoints) | 3 calls | ~$0.30-0.50 |
| Peer review (planned, not yet implemented) | — | — |
| **Full pipeline** | **~7 calls** | **~$0.60-1.10** |

These are rough estimates based on GPT-5.4 Pro pricing ($5/1M input, $20/1M output) and typical prompt sizes.

## Limitations

1. **Does not solve frame-lock fully.** All major LLMs share substantial training data. Cross-model catches different surface errors but may share deep structural biases.
2. **API latency.** Cross-model calls add 2-5 seconds per call. For integrity verification of 18 references, this adds ~1-2 minutes.
3. **Response format differences.** Different models structure responses differently. The agent must parse varied formats — keep verification prompts simple and structured to minimize parsing issues.
4. **Cost scales with paper size.** Longer papers with more references = more cross-model calls.

## Graceful Degradation

If cross-model verification fails (API error, rate limit, key expired):
- Log the failure: `[CROSS-MODEL-ERROR: reason]`
- Continue with single-model verification — never block the pipeline on cross-model failure
- Include a note in the report: "Cross-model verification was configured but unavailable for this run. Results are single-model only."
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-contracts-readme-md"></a>

## SOURCE: shared/contracts/README.md

<!-- SOURCE-CONTENT-BEGIN bytes=4761 -->
# ARS Shared Contracts

Schema files for cross-skill contracts: reviewer sprint contracts, Material Passport
ports, and (v3.6.7+) cross-model audit artifact pipelines.

## Sprint contracts (v3.6.2+)

Sprint contract templates for reviewer hard-gate orchestration.

Schema: `shared/sprint_contract.schema.json` (Schema 13).
Validator: `scripts/check_sprint_contract.py`.
Spec: `docs/design/2026-04-23-ars-v3.6.2-sprint-contract-design.md`.
Protocol: `academic-paper-reviewer/references/sprint_contract_protocol.md`.

### Shipped templates

**v3.6.2 (reviewer family)**:

- `reviewer/full.json` — panel 5, 5 dimensions, 4 failure conditions
- `reviewer/methodology_focus.json` — panel 2, 2 dimensions, 3 failure conditions

**v3.6.6 / suite v3.6.8 (generator-evaluator family)**:

- `writer/full.json` — single-agent writer, 7 dimensions (D1 section_completeness / D2 citation_density / D3 argument_blueprint_fidelity / D4 total_word_count / D5 per_section_word_count / D6 acknowledged_limitations / D7 register_consistency), 5 failure conditions (F1 / F4 / F2 / F3 / F0). No `scoring_plan` field.
- `evaluator/full.json` — single-agent evaluator, 5 dimensions (D1 originality / D2 methodological_rigor / D3 evidence_sufficiency / D4 argument_coherence / D5 writing_quality), 7 failure conditions (F1 / F2 / F3 / F6 / F4 / F5 / F0). Carries full `scoring_plan` + `disagreement_handling`.

Both writer + evaluator templates ship under Schema 13.1 (allOf branches 11/12 require `pre_commitment_artifacts` for `writer_full` and `disagreement_handling` for `evaluator_full`; branches 5/6 pin `failure_conditions[].action` to mode-specific enums; branches 8/9 pin F0 contains to the mode's accept variant). Orchestration block lives in `academic-paper/SKILL.md` § "v3.6.6 Generator-Evaluator Contract Protocol" + the writer/evaluator agent files.

### Reserved reviewer modes without shipped templates

`reviewer_re_review`, `reviewer_calibration`, `reviewer_guided` are in the schema enum
but ship without templates in v3.6.2. Those modes continue to operate in their existing
form (no contract, no hard-gate) until a follow-up patch release adds their templates.

### How to add a new template

1. Add the file under `shared/contracts/<domain>/<mode>.json`.
2. Run `python scripts/check_sprint_contract.py <path> --ars-version vX.Y.Z`; expect
   zero errors and zero soft warnings.
3. If `expression` strings use new phrasing, update `sprint_contract_protocol.md`
   and the synthesizer prompt's recognised-pattern list in the same PR.

## Passport contracts (v3.6.4+)

Schemas for Material Passport input ports.

- `passport/literature_corpus_entry.schema.json` (v3.6.4) — Schema 9 `literature_corpus[]`
  entries produced by user-written adapters.
- `passport/rejection_log.schema.json` (v3.6.4) — adapter output companion logging
  entries that could not be included in the corpus.
- `passport/reset_ledger_entry.schema.json` (v3.6.3) — `reset_boundary[]` ledger entries
  for the opt-in passport reset boundary protocol.
- `passport/audit_artifact_entry.schema.json` (v3.6.7 Step 6) — `audit_artifact[]` entries
  recording one cross-model audit run per downstream-agent deliverable. Two lifecycle
  states (proposal / persisted) share the schema via `oneOf`. Cross-artifact invariants
  are enforced by `scripts/check_audit_artifact_consistency.py`. Spec:
  `docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md` §3.1-§3.2.

## Audit artifact contracts (v3.6.7 Step 6)

The `audit/` directory carries the three wrapper-emitted artifact schemas that pair
with the passport-side `audit_artifact_entry.schema.json` above. Together they form
the four-schema contract that `scripts/run_codex_audit.sh` (Phase 6.1) writes and the
orchestrator agent reads at every per-agent audit gate.

- `audit/audit_jsonl.schema.json` — Layer 2 evidence: per-row schema for the codex CLI
  0.125+ `--json` event stream (`thread.started` / `turn.started` / `item.completed` /
  `turn.completed` / `error`). One JSONL line per event row.
- `audit/audit_sidecar.schema.json` — Layer 3 evidence: runner / timing / process /
  stream / prompt metadata. Cross-file rules linking sidecar fields to JSONL events,
  on-disk files, and passport entries (B1-B7 in spec §3.7 family B) are enforced by
  `scripts/check_audit_artifact_consistency.py` (Phase 6.3), not by this schema alone.
- `audit/audit_verdict.schema.json` — verdict file shape (PASS / MINOR / MATERIAL /
  AUDIT_FAILED). The artifact orchestrator parses for ship/block decisions; cross-field
  consistency with `finding_counts` and `failure_reason` is lint-enforced per
  spec §3.7 A1 / A2 / A5 / A6.

Spec: `docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md` §3.
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-references-intent-clarification-protocol-md"></a>

## SOURCE: shared/references/intent_clarification_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=10940 -->
# Intent Clarification Protocol (v3.9.2)

**Spec:** v3.9.2 hot-fix per `docs/design/2026-05-18-ars-v3.9.2-phase-boundary-spec.md`
**Issue:** #133 (phase scope inflation hot-fix)
**Forward note:** v3.10 active conductor (#134) will replace this clarification gate with structured intake + task envelope dispatch. v3.9.2 ships clarification-only as interim.

## Purpose

When ARS receives input that does not unambiguously identify the intended workflow, the main session **clarifies before dispatching any agent**. Auto-routing to a single-phase agent on cross-phase materials caused #133 (silent scope inflation).

This protocol defines:

1. When clarification fires (3 trigger classes)
2. How the clarification message is structured (a-d options in markdown body, NOT AskUserQuestion tool)
3. How the `[direct-mode]` escape hatch works
4. Worked examples

## Trigger condition table

| Condition | Routing class | Action |
|---|---|---|
| User invokes `/ars-*` slash command | Explicit | Route directly to named skill; no clarification |
| User uses unambiguous trigger keyword (e.g., "lit-review this", "review my paper") | Explicit | Route directly to matching skill; no clarification |
| User provides materials spanning ≥ 2 pipeline phases (e.g., abstract + literature, draft + reviewer comments + bibliography) | Cross-phase ambiguous | **Clarify** with a-d options |
| User provides no materials and no clear request | No materials ambiguous | **Clarify** with a-d options |
| User's first message begins with `[direct-mode]` (byte-0, case-insensitive) | Escape hatch | Strip prefix, skip clarification, route to whatever single agent matches the literal trigger; if no match, fall back to Explicit handling on the stripped message |

## Pipeline phase reference (for "cross-phase materials" detection)

| Phase | Typical artifact | File markers (heuristic) |
|---|---|---|
| 1 — Scoping | Research Question Brief, Methodology Blueprint | `phase1_*/` directory; `rq_brief.md`; `methodology.md` |
| 2 — Investigation | Annotated Bibliography, source list, literature_corpus passport entries | `phase2_*/`; `annotated_bib.md`; `literature.{yaml,json}`; `references.bib`; folders of PDFs |
| 3 — Analysis / Synthesis | Synthesis Report, claim-evidence mapping | `phase3_*/`; `synthesis.md` |
| 4 — Composition | Full draft, abstract, report body | `phase4_*/`; `draft.md`; `abstract.md` (or 5b for academic-paper) |
| 5 — Review | Editorial decision letter, reviewer comments, ethics report | `phase5_*/`; `review_*.md`; `editorial_decision.md` |
| 6 — Revision | Revision Roadmap, R&R response letter, revised draft | `phase6_*/`; `revision_roadmap.md`; `response_letter.md` |
| 0 / 7 / Plan | Intake config, format conversion, Socratic plan | `phase0_*/`; `phase7_*/`; Plan mode mid-conversation |

"Cross-phase" = the user-provided materials, taken together, would correspond to artifacts from ≥ 2 of these phases. Examples:

- Abstract + literature = Phase 4 + Phase 2 → cross-phase, clarify
- Draft + reviewer comments = Phase 4 + Phase 5 → cross-phase, clarify
- Literature only = Phase 2 → single-phase, no clarification needed
- Reviewer comments only = Phase 5 → single-phase, no clarification needed

## Clarification message template

When clarification fires, the main session emits a message in this shape (markdown body, multi-select a-d format per `feedback_telegram_conversation_style.md` discipline):

```markdown
I see you've provided <summary of materials>. To route correctly, could you confirm which workflow you want?

(a) **Full pipeline** — go from materials through to a complete deliverable (research + write + review + revise). Use `academic-pipeline` orchestrator (`/ars-full`).
(b) **<phase-specific workflow 1>** — <one-line description>. Use `<skill>` (`/ars-<mode>`).
(c) **<phase-specific workflow 2>** — <one-line description>. Use `<skill>` (`/ars-<mode>`).
(d) **Something else** — let me know what you're trying to do.

Pick a-d, or describe the target deliverable. If you want me to dispatch a specific agent directly without this clarification, prefix your message with `[direct-mode]`.
```

**Discipline rules:**

- 3-4 candidate options + open "something else"; never more than 4 (avoid choice paralysis)
- Each option names the destination skill / command so the user sees what gets invoked
- Last sentence mentions `[direct-mode]` so the user knows the escape hatch exists
- Do NOT call `AskUserQuestion` tool — options live in the markdown body of the chat response (per `feedback_no_askuserquestion_use_brainstorm.md`)

## `[direct-mode]` escape hatch

**Behavior:**

- **Position:** Token must be the first non-whitespace token of the user's first message. Leading whitespace (spaces, tabs, newlines) is stripped on parse — `[direct-mode] ...`, `  [direct-mode] ...`, and `\n[direct-mode] ...` all qualify. Token appearing mid-message (after any non-whitespace character) does NOT qualify.
- **Case:** Case-insensitive. `[direct-mode]`, `[Direct-Mode]`, `[DIRECT-MODE]` all accepted.
- **Bracket form:** Only the literal `[direct-mode]` (square brackets, hyphen between words) is recognized. Variants like `(direct-mode)`, `<direct-mode>`, `[direct mode]` (space instead of hyphen), or `[directmode]` (no separator) are NOT recognized.
- **Strip:** The literal `[direct-mode]` token (with surrounding whitespace) is stripped before any downstream agent sees the message. Dispatched agents receive only the post-strip content.
- **Effect:** Bypasses Routing Discipline Step 2 (cross-phase clarification). Main session routes the stripped message via Step 1 (explicit-intent handling).
- **Fallback:** If the stripped message itself has no clear skill named, Step 1 falls through to Step 3 clarification. (`[direct-mode]` is NOT a magic "always dispatch" flag — it bypasses cross-phase clarification, not all routing. If you want to bypass even ambiguous-intent clarification, you must name a specific skill or agent in the stripped message.)

**Examples:**

- `[direct-mode] /ars-lit-review on these papers` → dispatches academic-paper lit-review mode on the provided papers, no clarification
- `[direct-mode] run bibliography_agent` → dispatches bibliography_agent directly
- `[DIRECT-MODE] write me an abstract` → case-insensitive accepted; routes to abstract workflow without clarification

**Anti-patterns (escape hatch NOT honored):**

- `Please [direct-mode] dispatch X` — token not at byte-0 → ignored, clarification fires normally
- `[direct mode] ...` — missing hyphen, not the literal token → ignored
- `[direct-mode]` in second or later message of conversation — only first-message position counts

## Worked examples

### Example 1: cross-phase materials → clarify

**User input:**
> Here's an abstract and some literature, see what you can do.

**Materials detected:** Abstract (Phase 4) + literature (Phase 2) → cross-phase.

**Main session response:**
> I see you've provided an abstract and a literature collection. To route correctly, could you confirm which workflow you want?
>
> (a) **Full paper from existing scaffolding** — use your abstract as paper seed, expand literature into bibliography, draft full paper, then review/revise. Use `academic-pipeline` (`/ars-full`).
> (b) **Lit-review only** — produce an annotated bibliography matrix from the literature; don't touch your abstract. Use `academic-paper` (`/ars-lit-review`).
> (c) **Quality-check the abstract against the literature** — verify abstract claims are supported by the cited sources. Use `academic-paper-reviewer` (`/ars-citation-check`).
> (d) **Something else** — let me know what you're trying to do.
>
> Pick a-d, or describe the target deliverable. If you want me to dispatch a specific agent directly without this clarification, prefix your message with `[direct-mode]`.

### Example 2: single-phase material → proceed

**User input:**
> Here's a folder of 30 PDF papers. Build me a lit-review on AI in medical imaging.

**Materials detected:** Literature only (Phase 2). Explicit intent: lit-review.

**Main session response:** Routes directly to `academic-paper /ars-lit-review` on the provided PDFs. No clarification fires (explicit intent overrides materials check).

### Example 3: no materials + ambiguous → clarify

**User input:**
> Can you help me with my paper?

**Materials detected:** None. Intent: ambiguous.

**Main session response:**
> Of course. To route correctly, could you tell me what stage you're at?
>
> (a) **I have an idea but no clear research question** — Socratic mode to clarify direction. Use `deep-research` (`/ars-plan`).
> (b) **I have a question and need to do the research** — full research pipeline. Use `academic-pipeline` (`/ars-full`).
> (c) **I have research notes and need to write the paper** — drafting pipeline. Use `academic-paper`.
> (d) **I have a draft and want feedback** — peer-review simulation. Use `academic-paper-reviewer` (`/ars-review` equivalent).
>
> Pick a-d, or paste what you have so I can suggest a path.

### Example 4: `[direct-mode]` honored

**User input:**
> [direct-mode] run bibliography_agent on these 30 PDFs

**Stripped message:** `run bibliography_agent on these 30 PDFs`

**Main session response:** Dispatches `bibliography_agent` directly with the PDFs as input. No clarification fires.

### Example 5: `[direct-mode]` mid-message → NOT honored

**User input:**
> Hi, can you [direct-mode] just run bibliography_agent?

**Token position:** Not byte-0. Escape hatch ignored.

**Main session response:** Cross-phase or ambiguous check fires normally. May respond with clarification options.

## When this protocol does NOT apply

- **Within a skill that has already been routed.** If `academic-pipeline` is already running and the orchestrator is dispatching Phase 3 → Phase 4 internally, this protocol does not fire on every internal dispatch. It governs the **entry point** of an ARS session, not in-pipeline transitions.
- **In-conversation follow-up.** After clarification resolves and a workflow starts, subsequent user messages within that workflow are interpreted by the active skill, not re-classified at the routing level. To re-route, the user starts a new session or uses `[direct-mode]` at the start of a new message.

## v3.10 carry-over

When the active conductor architecture (#134) ships, this protocol's logic moves into the conductor's intake stage with structured task envelope dispatch. The conductor will:

- Classify intent deterministically with envelope schema rather than prompt-driven LLM judgment
- Hold pipeline state across turns (so cross-phase materials in workspace are treated as ongoing project state, not "user-provided ambiguous input")
- Eliminate the `[direct-mode]` escape hatch in favor of envelope-declared intent

Until v3.10 ships, v3.9.2's prompt-driven clarification gate is the source of truth.
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-references-irb-terminology-glossary-md"></a>

## SOURCE: shared/references/irb_terminology_glossary.md

<!-- SOURCE-CONTENT-BEGIN bytes=6933 -->
# IRB Terminology Glossary

**Spec:** v3.6.7 §7.1 — pattern protection reference for `research_architect_agent` (survey designer mode), Pattern B1.

**Audience:** Agents drafting consent / privacy language in survey instruments. Human authors reviewing instrument drafts.

**Why this exists:** In live ARS pipeline runs, survey instrument drafts repeatedly conflated four IRB terms that look adjacent in everyday English but carry distinct operational commitments. Conflation creates legal-effect drift in the consent script and can make the instrument unenforceable as informed consent. This reference is the canonical distinction the survey designer must pass through.

---

## The four terms

The four terms differ along two axes: (1) what is hidden — identity vs. content — and (2) whether re-identification is technically possible.

### Anonymity

**Operational definition:** The respondent's identity cannot be linked to their response by anyone, including the researcher. No identity key is created or stored.

**Necessary conditions:**
- No name, email, IP, device fingerprint, or directly-identifying field is collected.
- No code or token is created that could later be matched back to the respondent.
- Demographic combinations are coarse enough that no respondent is uniquely identifiable from the demographic combination alone (k-anonymity ≥ k for some agreed k, typically k ≥ 5).

**Example consent phrasing (correct):**
> "Your responses are anonymous. We do not collect your name, email, or any identifier that could link this survey to you. We cannot contact you about your responses, and we cannot remove your responses from the dataset after submission because we cannot identify which responses are yours."

**Common drift to flag:**
- Claiming "anonymous" while collecting email "for follow-up" — that is **confidential**, not anonymous.
- Claiming "anonymous" while assigning a respondent code that the researcher holds — that is **pseudonymous**, not anonymous.

### Confidentiality

**Operational definition:** The respondent's identity IS known to the researcher, but the researcher commits not to disclose it. Identity-response linkage exists in the research record.

**Necessary conditions:**
- A written commitment specifies who can see the identified data, for what purpose, and for how long.
- Storage and access controls match the commitment (encrypted at rest, access-logged, retention-bounded).
- Reporting layer aggregates or de-identifies before any external disclosure.

**Example consent phrasing (correct):**
> "Your responses are confidential. We will know your identity from the email you provide for follow-up. Your name will not appear in any report. Only the named research team will see identified data, and identified data will be deleted within 12 months of project close."

**Common drift to flag:**
- Promising "confidentiality" without specifying a retention boundary — IRB will reject; respondent cannot evaluate the commitment.
- Promising "confidentiality" while planning to publish identifiable case-study quotes — that is a contradiction; either the consent script needs an explicit case-study clause or the publication plan needs aggregation.

### De-identification

**Operational definition:** Direct identifiers have been removed from a dataset, and the link key created during data collection has been destroyed. The remaining record cannot be re-linked to the respondent.

**Necessary conditions:**
- Direct identifiers (HIPAA Safe Harbor's 18 fields or the project's equivalent list) are removed or transformed into non-reversible categories.
- Quasi-identifiers (zip + birth-date + gender, etc.) are evaluated for re-identification risk against plausible auxiliary datasets and reduced to acceptable risk threshold.
- The link key used during data collection is **destroyed**. Any retained re-link key — even one held by an independent custodian — falls under pseudonymization (next section), not de-identification, because re-identification remains technically possible.

**Example dataset description (correct):**
> "The released dataset is de-identified. Names, emails, exact dates, and institutional affiliation have been removed. Birth year is generalised to 5-year buckets. The collection-time link key was destroyed at the close of data collection."

**Common drift to flag:**
- Claiming "de-identified" while keeping the link key for "potential follow-up" — that is **pseudonymized**, not de-identified.
- Claiming "de-identified" without a quasi-identifier risk evaluation — k-anonymity unverified.

### Pseudonymization

**Operational definition:** Direct identifiers have been replaced by a pseudonym (code, token, hash). The pseudonym is reversible because the link key is preserved somewhere — typically by the data controller.

**Necessary conditions:**
- A documented pseudonymization scheme specifies the substitution method and the link-key custodian.
- The link key is held separately from the pseudonymized dataset, with separate access controls.
- Use cases (longitudinal follow-up, data subject access request, error correction) are pre-specified.

**Example dataset description (correct):**
> "The dataset is pseudonymized. Each participant is assigned an opaque code (e.g., P-0042). The mapping from code to participant identity is held by the principal investigator and is not shared with the analytic team. The mapping is retained for 24 months to support follow-up surveys, then destroyed."

**Common drift to flag:**
- Calling pseudonymized data "anonymized" — under GDPR, EU AI Act, and most modern IRB guidance, pseudonymized data remains personal data subject to the full data protection regime.

---

## Quick distinction table

| Term | Identity-response link exists? | Held by whom? | Reversible? |
|---|---|---|---|
| **Anonymity** | No | N/A | No |
| **Confidentiality** | Yes | Researcher | Yes (within research team) |
| **De-identification** | No (key destroyed) | N/A | No (assuming key destroyed and quasi-identifier risk acceptable) |
| **Pseudonymization** | Yes (via key) | Researcher / data controller | Yes |

---

## Where this glossary is enforced

The `research_architect_agent` survey designer mode prompt requires consent / privacy language to pass through this glossary before output. The authoritative protection clause lives in `deep-research/agents/research_architect_agent.md` under `PATTERN PROTECTION (v3.6.7)`. This file defines the four regimes and example phrasings; the agent prompt cites this file by path.

---

## References

- HHS HIPAA Safe Harbor de-identification (45 CFR 164.514(b)(2)) — primary source for direct-identifier list.
- GDPR Art. 4(5) — pseudonymization definition.
- EU AI Act Recital 27 + Art. 10(5) — pseudonymization vs. anonymization distinction in AI training contexts.
- ISO/IEC 27559:2022 — privacy-enhancing data de-identification framework.
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-references-protected-hedging-phrases-md"></a>

## SOURCE: shared/references/protected_hedging_phrases.md

<!-- SOURCE-CONTENT-BEGIN bytes=8489 -->
# Protected Hedging Phrases

**Spec:** v3.6.7 §7.1 — pattern protection reference for `report_compiler_agent` (abstract-only mode), Pattern C1.

**Audience:** Upstream calibration agents (academic-paper Stage 4, deep-research Phase 3 abstract handoff). The downstream `report_compiler_agent` reads this reference indirectly through the dispatch context that upstream calibration produces.

**Why this exists:** Live ARS pipeline runs surfaced a recurring failure where the abstract compiler, under hard word-count pressure (i.e., a fixed word budget set by the publisher), dropped epistemic hedges that the body of the paper depended on. The fix routes through a roster of protected hedging phrases that ride in the dispatch context to the compiler. A claim qualified by "may," "tentative," "preliminary," or "in this institutional context" in the body became unconditional in the abstract. The compression-driven drift created compression overclaim — the abstract no longer accurately represented the paper's epistemic stance, which is a publication-integrity failure.

The fix is to make hedging phrases **budget-protected**: upstream calibration marks specific phrases as protected, the protected list rides in the dispatch context to the abstract compiler, and the compiler honours the protection ahead of any other compression target.

---

## What counts as a protected hedging phrase

A phrase qualifies as protected when **dropping it changes the paper's truth-claim**, not merely its rhetorical register. Three categories cover most cases:

### 1. Epistemic hedges that bound the claim

Words and phrases that mark a claim as conditional, tentative, or under-evidenced. Removing them upgrades the claim to assertion.

**Examples:**
- "may," "might," "could" (modal hedges on causal or predictive claims)
- "tentative," "preliminary," "exploratory" (status hedges on findings)
- "suggests," "indicates," "is consistent with" (inferential hedges, distinct from "demonstrates," "proves," "establishes")
- "in our sample," "for this cohort," "under the conditions tested" (scope hedges)

**Why protected:** A reader who acts on an unconditional version of the claim takes on more risk than the evidence justifies. In academic abstracts this is overclaim; in policy abstracts this is misinformation.

### 2. Reflexivity / positionality markers

Phrases that disclose the author's relationship to the studied phenomenon. Removing them obscures the position from which the work was done.

**Examples:**
- "from a former evaluator's perspective" (positional)
- "as participants in the [year-range] reform" (involvement)
- "the authors served on the [committee] from [year] to [year]" (institutional role)
- "this analysis draws on the first author's experience as [role]" (experiential)

**Why protected:** Disclosure obligations under most journal policies (BMJ, Nature, social-science conventions) require positionality to ride in the abstract when it materially shapes interpretation. Stripping disclosure for word count violates the policy, not just the rhetorical norm.

### 3. Temporal disambiguation markers

Phrases that pin a claim or a positional statement to a specific time window. Removing them creates temporal ambiguity that downstream readers cannot resolve.

**Examples:**
- "between 2020 and 2024" (explicit year range)
- "during their term as [role] in [year]" (role-bounded period)
- "former [role]" (closed temporal status)
- "at the time of the [event]" — only protected when the event is named immediately adjacent; otherwise the deictic phrase is itself the failure mode (see `feedback_ars_phase2_phase3_downstream_agent_patterns.md`).

**Why protected:** Deictic temporal phrases ("during this period," "at the time," "currently") read differently when separated from their anchoring context. The abstract has no neighbouring context; an abstract-level deictic is unresolvable.

---

## Upstream calibration: how to mark phrases as protected

Upstream calibration runs at the end of paper drafting, after the body text is stable but before abstract compilation. The calibration agent walks the paper and identifies phrases in the three categories above, then emits a `protected_hedges` block in the dispatch payload to the abstract compiler.

### Dispatch block shape

```yaml
protected_hedges:
  epistemic:
    - phrase: "may"
      anchored_at: "Section 4, claim about institutional adoption rate"
      why: "claim is observational, not causal"
    - phrase: "tentative"
      anchored_at: "Section 5, conclusion about policy effect"
      why: "n=12 sites, no comparison group"
  reflexivity:
    - phrase: "as a former evaluator on the [committee] between 2020 and 2024"
      anchored_at: "Author note + Section 1"
      why: "BMJ-equivalent disclosure obligation; informs how reader weights argument"
  temporal:
    - phrase: "between 2020 and 2024"
      anchored_at: "Section 1, paragraph 2; Section 6, conclusion"
      why: "abstract-level deictic ('at the time') would be unresolvable"
```

### Calibration rules

1. **Conservative inclusion.** When in doubt, include the phrase. Calibration cannot recover a hedge it did not list — the compiler treats every entry on the list as non-negotiable, so omitting a phrase removes that protection regardless of intent.
2. **Anchor every entry.** Each protected phrase must cite where in the paper it operates and one-line why. Without the anchor, the abstract compiler cannot judge replacement-vs-preservation when budget is tight.
3. **No duplicates.** One entry per phrase. The compiler counts protected phrases against the budget once.
4. **Calibration is mode-specific.** Deep-research INSIGHT abstracts and academic-paper journal abstracts have different convention (see `word_count_conventions.md`). Calibration runs once per target mode, not once per paper.

---

## Abstract compiler: how protection is honoured

The `report_compiler_agent` abstract-only mode treats protected hedges as **non-negotiable budget**. Concretely:

1. **Budget allocation order.** Protected hedges are reserved before any other content competes for budget, because they are non-negotiable.
   - Step 1: Compute hard cap (whitespace-split, see `word_count_conventions.md`).
   - Step 2: Reserve 3–5% buffer.
   - Step 3: **Reserve words for protected hedges.** Sum the word count of every entry in `protected_hedges` (verbatim). This subtotal is non-negotiable budget.
   - Step 4: Allocate the remaining words to required structural slots (research question, method, finding, implication).
   - Step 5: Spend any words still remaining on rhetorical polish, transitions, secondary findings.

2. **Verbatim preservation rule.** A protected phrase rides verbatim into the abstract. The compiler does not paraphrase, compress, or substitute a synonym for a protected phrase. (A future v3.6.7+ extension may add an optional `approved_synonyms` field to the dispatch block; until then, verbatim only.)

3. **Cut order under budget pressure.** When the draft exceeds budget, cuts come from Step 5 first (rhetorical polish), then Step 4 (compress structural slots), **never** from Step 3 (protected hedges).

4. **Failure surface.** If the abstract cannot fit Steps 1–4 within hard cap, the compiler **reports the conflict** rather than dropping a protected hedge. The conflict goes back to upstream calibration to either renegotiate the protected list or the publisher's word cap.

---

## Where this protocol is enforced

The `report_compiler_agent` abstract-only mode prompt enforces the dispatch-context protocol and the budget allocation order. The authoritative protection clause lives in `deep-research/agents/report_compiler_agent.md` under `PATTERN PROTECTION (v3.6.7)`. This file defines what counts as a protected hedge, the upstream calibration shape, and the compiler's budget allocation order; the agent prompt cites this file by path. Cross-model audit covers protected-hedge preservation under the report_compiler bundle's Section 4(f) check in `shared/templates/codex_audit_multifile_template.md`.

---

## Cross-references

- `shared/references/word_count_conventions.md` — whitespace-split standard, 3–5% buffer rule, publisher conventions.
- `shared/templates/codex_audit_multifile_template.md` — audit dimensions including compression overclaim detection.
- `docs/design/2026-04-29-ars-v3.6.7-downstream-agent-pattern-protection-spec.md` §3.3 (C1) — pattern definition and provenance.
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-references-psychometric-terminology-glossary-md"></a>

## SOURCE: shared/references/psychometric_terminology_glossary.md

<!-- SOURCE-CONTENT-BEGIN bytes=8273 -->
# Psychometric Terminology Glossary

**Spec:** v3.6.7 §7.1 — pattern protection reference for `research_architect_agent` (survey designer mode), Pattern B2.

**Audience:** Agents drafting Likert / rating-scale items in survey instruments. Human authors reviewing instrument drafts before pilot testing.

**Why this exists:** Live ARS pipeline runs surfaced two recurring failures in instrument design: (a) items labelled "reverse-coded" that were actually contrast items measuring a different construct, and (b) acquiescence- and recall-bias mitigations that look in place but do not operate. Both failures pass casual peer review and surface only at scale validation, by which point the instrument has already been deployed. This reference defines the operational distinctions the survey designer must respect.

---

## True reverse-coded item vs. contrast item

These are distinct instrument-design tools that look identical to a casual reader. Conflating them invalidates the construct.

### True reverse-coded item

**Operational definition:** A negatively-keyed statement of the **same construct** along the **same Likert dimension**. After numeric reversal of the response value, it contributes to the same scale score as positively-keyed items.

**Necessary conditions:**
- Same construct: if the positive item probes "perceived institutional support," the reverse item probes the absence of perceived institutional support, not a different construct.
- Same dimension: agreement-disagreement remains the response axis; frequency or intensity does not get substituted in.
- Reverse-scoring is mechanically valid: a respondent with high construct standing should give high agreement on positive items and low agreement on the reverse item, such that the reverse item's reversed score aligns with the positive items.

**Correct example pair (construct: perceived institutional support):**
- Positive: "My institution provides the resources I need to do my work well." (1=strongly disagree → 5=strongly agree)
- True reverse: "My institution leaves me without the resources I need to do my work." (same scale; respondents high in perceived support disagree with this)

**Why this works:** Both items load on a single latent factor. Confirmatory factor analysis on a piloted dataset will show comparable factor loadings (after sign reversal) and similar item-total correlations.

### Contrast item

**Operational definition:** A statement that probes a **different construct** (or a different dimension of the same construct) and is included to measure something else — discriminant validity, related-but-distinct construct, social-desirability check.

**Why it is not reverse-coding:**
- A contrast item's score should NOT be combined with the focal scale's score. It belongs on its own scale or its own analysis.
- Reverse-scoring a contrast item produces a meaningless number.
- Treating a contrast item as a reverse-coded item dilutes the focal scale's reliability (Cronbach's alpha drops; factor loadings become incoherent).

**Example contrast (NOT a reverse-coded support item):**
- "I find my work intrinsically meaningful." — This probes intrinsic motivation, not perceived institutional support. It is contrast / divergent-validity, not a reverse item.

### Decision rule for the survey designer

For every item labelled "reverse-coded," the agent must produce a one-line construct-equivalence justification:

> "Item X is true reverse-coded relative to focal items Y because it probes the same construct (perceived institutional support) on the same Likert dimension (agreement). It is not a contrast item probing a related construct."

If that justification cannot be written without slipping into a different construct, the item is **not** reverse-coded — it is a contrast item, and it must either move to its own scale or be removed.

---

## Acquiescence-bias mitigation

**The bias:** Respondents systematically agree with statements regardless of content. Pure-positive scales over-estimate construct standing.

**The standard mitigation:** Mix positive and true-reverse-coded items so that an acquiescing respondent cannot maximise scale score by agreeing throughout.

**The failure mode flagged in v3.6.7 patterns:** "Pseudo-reverse" items that look reverse-coded but are actually contrast items, leaving the scale effectively pure-positive. The pseudo-mitigation is worse than no mitigation because it gives the appearance of having addressed acquiescence while leaving it operative.

**Designer requirement:** Apply the construct-equivalence justification rule (above) to every reverse-coded item. If any "reverse-coded" item fails the justification, that item is mislabelled — it is a contrast item and must either move to its own scale or be removed. A scale that ends up with no surviving reverse-coded item after this filter has not mitigated acquiescence bias and needs redesign before pilot.

---

## Recall-bias mitigation

**The bias:** Respondents misremember the timing or details of past events. Two failure modes are common:

1. **Calendar drift:** Asking "in the last 12 months" without anchoring to a salient event produces noisy recall — respondents reconstruct an approximate window, not a true 12-month boundary.
2. **Telescoping:** Memorable events get pulled forward in time ("that happened last year" when it happened 18 months ago), inflating recent-period rates.

**The standard mitigation:** Event-anchored phrasing — anchor the recall window to a salient, datable event the respondent's unit shares.

**Correct phrasing (event-anchored, generic):**
> "Thinking about the period immediately before [the unit-specific event] happened to your unit, how often did X occur?"

**Correct phrasing (event-anchored, project-specific):**
> "Thinking about the period before your institution announced the merger in [month-year], how often did you experience X?"

**Calendar-anchored phrasing — only acceptable when the entire sample shares a common event date:**
> "In the 6 months following the [common event] of [specific date], how often did you experience X?"

**Wrong phrasing (calendar-only, no event anchor):**
> "In the last 12 months, how often did X occur?" — This invites calendar drift and telescoping; the respondent has no shared anchor.

**Designer requirement:** Default retrospective items to event-anchored phrasing. Only use calendar-anchored phrasing when the sample provably shares a common event date and that date is named in the item. When the event-anchor is absent, the item is not recall-bias-mitigated, even if it superficially looks like a retrospective survey item.

---

## Quick decision table

| Designer choice | Operational test | Failure flag |
|---|---|---|
| Item is reverse-coded | One-line construct-equivalence justification holds | Pseudo-reverse (contrast item mislabeled) |
| Acquiescence mitigated | At least one true reverse-coded item per scale AND every item labelled reverse-coded passes the construct-equivalence test | Pure-positive scale or pseudo-reverse mitigation |
| Recall-bias mitigated | Item anchors recall to a salient event the unit shares | Calendar-anchored without shared event date |

---

## Where this glossary is enforced

The `research_architect_agent` survey designer mode prompt enforces construct-equivalence justification, acquiescence-bias counting, and event-anchored phrasing. The authoritative protection clause lives in `deep-research/agents/research_architect_agent.md` under `PATTERN PROTECTION (v3.6.7)`. This file defines the construct-equivalence test, the acquiescence-mitigation rule, and the event-anchoring decision rule; the agent prompt cites this file by path.

---

## References

- DeVellis, R. F. (2017). *Scale Development: Theory and Applications* (4th ed.). Sage. — reverse-coding and acquiescence bias.
- Tourangeau, R., Rips, L. J., & Rasinski, K. (2000). *The Psychology of Survey Response*. Cambridge. — recall bias and event anchoring.
- Loftus, E. F., & Marburger, W. (1983). Since the eruption of Mt. St. Helens, has anyone beaten you up? Improving the accuracy of retrospective reports with landmark events. *Memory & Cognition*, 11(2), 114–120. — primary empirical source for event-anchoring effect.
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-references-word-count-conventions-md"></a>

## SOURCE: shared/references/word_count_conventions.md

<!-- SOURCE-CONTENT-BEGIN bytes=7554 -->
# Word Count Conventions

**Spec:** v3.6.7 §7.1 — pattern protection reference for `report_compiler_agent` (abstract-only mode).

**Audience:** Agents budgeting word counts under a hard cap (abstract, executive summary, INSIGHT block). Human authors verifying that an agent's word count matches the publisher's.

**Why this exists:** Different word-count algorithms produce different totals on the same text. The differential is small per sentence but compounds: on a 250-word abstract, the choice between whitespace-split and hyphenated-as-1 can swing the total by ~12 words. An agent that uses a different algorithm than the publisher believes it is meeting the cap when it is over by 5%. This reference fixes a single canonical algorithm for ARS pipelines, documents how publishers diverge, and specifies the buffer rule that makes minor publisher variation safe.

---

## The canonical algorithm: whitespace-split

ARS pipelines count words as `len(body.split())` in Python — that is, splits on any whitespace run and counts the resulting non-empty tokens.

### Why whitespace-split

1. **Reproducible.** Anyone running `len(body.split())` on the same UTF-8 text gets the same number. No hidden tokenizer state.
2. **Matches Microsoft Word default.** Most authors check word count in Word, which uses a whitespace-equivalent algorithm. Aligning with the dominant authoring environment minimises surprise.
3. **Conservative under hyphenation.** "State-of-the-art" counts as 1 token under whitespace-split. Under hyphenated-as-N this would count as 4. Whitespace-split therefore systematically reports a lower total than hyphenated-as-N — which is the safer direction when chasing a hard cap.
4. **Language-neutral.** CJK text without spaces is a separate problem (see "Non-space-delimited languages" below), but for English / European languages, whitespace-split is the universal lower bound.

### What whitespace-split counts

| Token | Whitespace-split count |
|---|---|
| `state-of-the-art` | 1 |
| `2020-2024` | 1 |
| `Smith, John-Paul` | 2 (`Smith,` and `John-Paul`) |
| `e.g.,` | 1 |
| `123,456` | 1 |
| `(n=42)` | 1 |
| `https://example.org/path` | 1 |

### What whitespace-split does NOT count

- Whitespace runs collapse to one delimiter; they do not contribute tokens.
- Empty strings between consecutive whitespace characters are filtered by `split()` with no argument.
- Markdown formatting (`**bold**`, `*italic*`, `` `code` ``) is part of the surrounding token; the asterisks and backticks are not separate tokens.

---

## Publisher conventions and how to adapt

Most publishers use a whitespace-equivalent algorithm in practice but state different conventions in their author guidelines. The 3–5% buffer rule (below) makes ARS pipelines robust to the convention divergence without per-publisher adapters.

### Common publisher families

| Publisher / venue | Stated algorithm | Practical effect |
|---|---|---|
| Springer / Nature | whitespace-equivalent for abstract, no explicit definition | matches ARS canonical |
| IEEE | "approximately N words" — whitespace-equivalent in their submission tool | matches ARS canonical |
| ACM | whitespace-equivalent in CCS submission | matches ARS canonical |
| Elsevier (Cell, Lancet families) | whitespace-equivalent in EM submission | matches ARS canonical |
| Wiley | whitespace-equivalent | matches ARS canonical |
| arXiv | no hard cap on abstract; advisory ~250 words | guideline only |
| ICLR / NeurIPS / ACL workshop tracks | hyphenated-as-1 in their LaTeX `\abstract{}` counter | matches ARS canonical |
| Some social-science journals (variable) | "page-based" — abstract must fit visually on submission template | not a true word count; check template |

### When the publisher uses a stricter algorithm

Some non-English-medium publishers and a small number of style guides count hyphenated compounds as multiple words. If the publisher explicitly states "hyphenated words count as separate words":

1. Calibration should compute both totals: `len(body.split())` and the hyphenated-as-N variant.
2. The dispatch context to the abstract compiler should carry both numbers.
3. The compiler should use the stricter (higher) total when budgeting.

If the publisher's algorithm is ambiguous, default to ARS canonical (whitespace-split) plus the 3–5% buffer.

---

## The 3–5% buffer rule

ARS pipelines reserve **3–5% below the publisher's stated hard cap** as buffer. For a 250-word abstract:

- 3% buffer → target 242 words
- 5% buffer → target 237 words

### Why this range

1. **Algorithm divergence absorbs into the buffer.** Even if the publisher's tool counts ~3% higher than `len(body.split())`, the abstract still meets the cap.
2. **Editor-side trimming room.** Reviewers and copy editors occasionally request a phrase change that adds 2–3 words. Abstract that lands at exactly the cap forces a downstream cut; abstract that lands at cap minus 5% accommodates the change without cut.
3. **Title plus abstract pages.** Some publishers count the running title or running header; the buffer absorbs that too.

### When to use 3% vs. 5%

- **3%** when the calibration's `protected_hedges` block is large (≥10% of cap word budget). Tighter buffer keeps room for substantive content.
- **5%** when the publisher's algorithm is unstated or the protected hedges are minimal. Looser buffer absorbs more uncertainty.

### When NOT to use buffer

If the publisher imposes a strict character count instead of word count (rare, but happens with some Asian-language journals), the buffer rule does not apply directly. Calibration should compute character count under the publisher's stated encoding and apply a 1–2% buffer at the character level.

---

## Non-space-delimited languages

Mandarin, Japanese, Korean, Thai, and Lao do not delimit words with whitespace. ARS canonical algorithm produces meaningless totals on these texts.

For abstracts in non-space-delimited languages:

1. Use **character count**, not word count. Most publishers serving these languages specify character caps (e.g., Mandarin abstract often capped at 300 or 500 characters).
2. Apply 1–2% buffer at the character level.
3. The dispatch context to the abstract compiler should carry both `cap_unit: "character"` and the character cap, so the compiler does not erroneously apply word-budget logic.

For mixed-language abstracts (e.g., Mandarin abstract with English technical terms), count each segment in its native unit and report both numbers; the publisher's authoritative count usually applies the language-specific rule per segment.

---

## Where this convention is enforced

The `report_compiler_agent` abstract-only mode prompt enforces the canonical algorithm, the 3–5% buffer, and the post-draft re-verification step. The authoritative protection clause lives in `deep-research/agents/report_compiler_agent.md` under `PATTERN PROTECTION (v3.6.7)`. This file defines the algorithm, the buffer rationale, and the publisher-convention escape hatches; the agent prompt cites this file by path.

---

## Cross-references

- `shared/references/protected_hedging_phrases.md` — protected hedging phrases share the abstract budget; budget allocation order specified there.
- `shared/templates/codex_audit_multifile_template.md` — audit dimensions including word-count verification.
- ARS feedback memory `feedback_word_count_convention_mismatch.md` — original empirical observation of whitespace-split vs. hyphenated-as-1 differential (~12 words on a 250-word abstract).
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-templates-codex-audit-multifile-template-md"></a>

## SOURCE: shared/templates/codex_audit_multifile_template.md

<!-- SOURCE-CONTENT-BEGIN bytes=16968 -->
# Codex Multi-File Audit Prompt Template

**Spec:** v3.6.7 §7.2 — audit prompt template for downstream-agent deliverable cross-model audit.

**Audience:** ARS pipeline orchestrator (academic-pipeline, deep-research, academic-paper) producing codex audit prompts for Phase 2 / Phase 3 deliverables. Human authors running ad-hoc cross-model review on a deliverable bundle.

**Why this template exists:** Live ARS pipeline runs surfaced 18 downstream-agent hallucination/drift patterns (spec §3) that single-file or single-dimension audit could not catch. The patterns interact across files (synthesis_agent's effect-inventory drift surfaces only when comparing two narrative sections; report_compiler_agent's compression overclaim surfaces only when comparing abstract against body). A multi-file audit prompt with explicit dimensions makes the cross-file checks first-class. Spec §4.1 (Lesson D1) records the empirical observation that multi-file parallel audit catches more findings per round than sequential single-file audit at comparable token cost.

This template fixes a single audit-prompt structure so the orchestrator's audit hooks (spec §5) generate consistent, reproducible prompts.

---

## Template structure

A v3.7.1 multi-file audit prompt has eight sections in this order (Section 0 prepended additively per v3.7.1 D2; Sections 1–7 stay byte-equivalent to v3.6.7):

0. Scope Report (mandatory; rides verbatim in every round; v3.7.1 D2)
1. Round metadata
2. Bundle inventory
3. Audit dimensions (the 7 specified below)
4. Round-specific job
5. Convergence target
6. Output format
7. Anti-fake-audit guard (mandatory; rides verbatim in every audit dispatch)

The orchestrator fills the placeholders in `{curly_braces}`. Everything else rides verbatim. Section 0 is non-negotiable — its purpose is to disclose the audit's actual coverage so a "PASSED" verdict cannot mask un-retrieved sources (spec v3.7.1 §3.2 / Pattern D2). Section 7 is non-negotiable — omitting it leaves sub-agents free to fake audit-passed metadata, which is the failure mode v3.6.7 spec §5.3 + Pattern C3 + `feedback_subagent_tool_hallucination.md` exist to prevent.

---

## Section 0 — Scope Report (mandatory; v3.7.1 D2)

Every audit round MUST open with a Scope Report that quantifies how many of the audited entries had a retrieved original source vs. were verified only against derivative bibliography or self-consistency. The block below rides verbatim in every audit dispatch, ahead of any pass/fail summary.

```
## Codex Audit Round N — Scope Report

**Total entries audited:** <N_total>
**Entries with retrieved original source:** <N_with_source> (verified against original publication)
**Entries description-only (no retrieved source):** <N_without_source> (verified only against derivative bibliography or self-consistency)

**Audit scope warning:** <N_without_source> entries cannot be independently verified by this audit round. Their `verified` status reflects internal consistency between entry .md and the derivative bibliography source, NOT correctness against the original publication. These entries should be treated as **unverifiable until original sources are retrieved**.

**Affected refcodes (description-only):** <comma-separated list>
```

**Two firm rules (spec v3.7.1 §3.2):**

- The Scope Report block must appear **before** any pass/fail summary in the audit output.
- The aggregate verdict MUST be split into the following three reporting lines (the combined-aggregate "PASSED" verb is forbidden in the audit summary):
  - `verified-against-source: PASS | FAIL` (over the retrieved-source subset)
  - `description-internally-consistent: PASS | FAIL` (over the non-retrieved subset)
  - `unaudited-due-to-missing-source: <count>` (always reported, never hidden)

**Why this exists:** in the 2026-04-30 production session, a codex round-3 report stated "ADDRESSED" without disclosing that only 22 of 53 entries had retrieved original sources; the remaining 31 description-only entries inherited the "verified" verdict by aggregation. The Scope Report renders that split first-class so a reader cannot conflate self-consistency with retrieval-grounded verification.

---

## Section 1 — Round metadata

```
Audit round: {N} of {target_rounds}
Previous rounds: {summary_of_prior_findings_or "none (first round)"}
Bundle scope: {phase or stage label, e.g. "Phase 2 chapter deliverables" or "Phase 3 abstract + reflexivity disclosure"}
```

**Fill rules:**
- `target_rounds` defaults to 3 per spec §4.2 (Lesson D2: convergence requires 3+ rounds, not 1 or 2). Increase to 4–5 when prior round count exceeded 3 without convergence.
- `summary_of_prior_findings` cites finding counts by severity for each prior round, e.g. "Round 1: P1×4 / P2×5 / P3×1 (10 total). Round 2: P1×0 / P2×3 / P3×1 (4 total)."
- For first round, `Previous rounds: none (first round, baseline audit)`.

---

## Section 2 — Bundle inventory

```
Authoritative context (commit {git_sha}):

Primary deliverables (audit target):
- {file path 1 with one-line description}
- {file path 2 ...}

Supporting context (do not audit; reference only):
- {file path A with one-line role}
- {file path B ...}

Out-of-scope (do not read):
- {explicit exclusions, if any}
```

**Fill rules:**
- Pin the audit to a commit SHA so the audit is reproducible. Codex sometimes reads files at a slightly different state than the human reviewer expects; the SHA pins the boundary.
- Distinguish primary deliverables from supporting context. Primary gets audited; supporting answers questions but is not the audit target.
- Out-of-scope is optional but useful when the bundle sits inside a larger directory with files that look adjacent but are not part of this audit.

---

## Section 3 — Audit dimensions (the 7)

Codex evaluates the bundle along seven dimensions. Each dimension surfaces a specific class of pattern from spec §3:

### 3.1 Cross-reference integrity

**What to check:** Every claim cited to file X actually appears in file X at the cited location. Every back-pointer (file Y references file X) terminates at a real anchor. Wikilink-style references (`[[file]]` or `(file.md)`) resolve.

**Patterns surfaced:** Pattern A3 (mis-anchored citation), Pattern B5 (primary-source list mismatch).

### 3.2 Hallucination detection

**What to check:** Declarative claims about external entities (laws, decisions, sibling documents, prior studies) are checkable against ground truth provided in the bundle. Conditional claims about un-provided documents use conditional language, not declarative.

**Patterns surfaced:** Pattern A5 (sibling-document fabrication), Pattern A2 (pending-source assumed as fact), Pattern B5 (option-list overclaim), Pattern C1 (compression overclaim).

### 3.3 Primary-source integrity

**What to check:** Verbatim quotes match the primary source character-for-character within marked phrase boundaries. Quote scope does not creep beyond the verified anchor. Translations of foreign-language primary sources are independently verifiable.

**Patterns surfaced:** Pattern A4 (quote scope creep), and the cross-reference half of Pattern A3.

### 3.4 Internal coherence

**What to check:** A source cited in multiple sections receives compatible characterizations across sections. A claim qualified at one anchor is not contradicted at another anchor without explicit reconciliation. The bundle does not contain mutually-incompatible statements about the same proposition.

**Patterns surfaced:** Pattern A1 (legal-effect drift / cross-section internal contradiction).

### 3.5 Instrument quality (survey designer mode bundles only)

**What to check:** Items labelled "reverse-coded" pass the construct-equivalence test (see `psychometric_terminology_glossary.md`). IRB terminology in consent script matches the operational reality of data handling (see `irb_terminology_glossary.md`). Retrospective items use event-anchored phrasing when sample lacks a common date. Item phrasing is neutral and balanced.

**Patterns surfaced:** Pattern B1 (anonymity / confidentiality conflation), Pattern B2 (pseudo-reverse), Pattern B3 (calendar-anchored without shared event), Pattern B4 (leading items / chapter-vocabulary contamination).

### 3.6 Round-N framing

**What to check:** The audit's own framing is consistent with prior rounds. Findings closed in earlier rounds remain closed (no regression). New findings introduced by prior-round corrections are surfaced. Anchoring bias is named when the bundle has converged to a structure that resists fresh critique.

**Patterns surfaced:** Pattern D2 (convergence requires 3+ rounds), Pattern D3 (PARTIAL ≠ CLOSED).

### 3.7 COI adequacy (conflict-of-interest / disclosure adequacy)

**What to check:** Conflict-of-interest and reflexivity disclosures use explicit temporal bounds (year ranges, role-bounded periods, "former" prefix). Deictic temporal phrases ("during this period," "at the time," "currently") are absent or fully resolved by adjacent context. Disclosure obligations under publisher policy are met at abstract / executive-summary level, not only at body level.

**Patterns surfaced:** Pattern C2 (temporal ambiguity).

Note: word-count convention, 3–5% buffer adherence, and protected-hedge preservation against compression are **not** covered by §3.7. They are handled by the bundle-specific check in Section 4 (f) below — see the report_compiler_agent example for the expected `(f)` clause.

---

## Section 4 — Round-specific job

```
Round {N} job:
(a) Verify each round-{N-1} finding closed correctly. List by ID.
(b) Audit for new issues introduced by round-{N-1} corrections (cascade audit per feedback_cross_model_review_cascade_inconsistency.md).
(c) Run the 7 audit dimensions (§3.1–§3.7) plus the bundle-specific Section 4(f) check on the primary deliverables. Report each finding with the dimension or `4(f)` that surfaced it.
(d) Anchoring-bias residual check: for each finding closed in prior rounds, confirm the closure is not a wording change that left the failure mode operative (per feedback_lint_passes_but_prompt_silent.md).
(e) PARTIAL-vs-CLOSED check: every finding marked PARTIAL in prior rounds is either fully closed or remains open with a concrete remaining-work description.
(f) {bundle-specific check, e.g. "compression overclaim check: every claim in the abstract is at least as hedged as its anchor in the body"}
```

**Fill rules:**
- (a)–(e) ride verbatim every round (with N substitution).
- (f) is bundle-specific. The orchestrator picks the bundle-specific check based on which downstream agent produced the deliverable. For report_compiler_agent bundles, (f) is mandatory and combines three sub-checks; the others are single-check. Examples:
  - synthesis_agent bundle: cross-section consistency check on every source cited in 2+ sections.
  - research_architect_agent bundle: construct-equivalence test on every reverse-coded item.
  - report_compiler_agent bundle (mandatory three-part check): (i) word count = `len(body.split())` ≤ publisher cap minus 3–5% buffer per `word_count_conventions.md`; (ii) every entry of upstream `protected_hedges` block per `protected_hedging_phrases.md` appears verbatim in the abstract; (iii) no claim in the abstract is less hedged than its anchor in the body. Failure of any sub-check is a P1 finding.

---

## Section 5 — Convergence target

```
Convergence target: ZERO findings of ANY severity in one round.

Per feedback_codex_iterative_spec_review_to_zero.md: goal = 0 findings in a single round, NOT N rounds of "0 P1." A round with P2/P3 only still counts as un-converged. Iterate until one full round produces zero findings or until {fallback condition, e.g. "round 5 is reached and remaining findings are 'add counter, do not change rule' per feedback_codex_review_vs_resume_audit_scope.md"}.
```

**Fill rules:**
- The fallback condition is part of spec §5.2 stop conditions. Default fallback: "after 5 rounds, escalate remaining findings to user for ship-or-iterate decision."
- Do NOT loosen convergence to "0 P1+P2 findings" or "0 P1 findings" — those are weaker stop conditions that v3.6.7 replaces with the strict 0-anything bar.

---

## Section 6 — Output format

```
Output:
- Cumulative numbered findings (carry forward IDs from round 1; new findings get next available ID).
- For each finding: ID, severity (P1/P2/P3), dimension (one of §3.1–§3.7 or `4(f)` for bundle-specific failures), file:line anchor, one-line description, suggested fix.
- Do NOT propose fixes that change the spec; the spec is authoritative. Suggested fixes operate on the deliverables only.
- End with severity-bucket count summary: "Round {N}: P1×{n1} / P2×{n2} / P3×{n3} ({total} total)".
- If zero findings, end with: "Round {N}: 0 findings of any severity. Convergence reached."
```

**Fill rules:**
- The "do NOT propose fixes that change the spec" clause prevents codex from drifting into spec critique when the audit target is deliverables. If codex finds a spec issue, it should be raised separately, not folded into the deliverable audit.
- Severity bucket summary at the end is what the orchestrator parses to decide round-N+1 vs. ship.

---

## Section 7 — Anti-fake-audit guard (Pattern C3, mandatory)

**Critical clause that rides in every audit dispatch context:**

```
DO NOT simulate any audit step. DO NOT claim to have run codex/external review on your own output. The orchestrator runs codex audit afterward; output metadata must not claim audit-passed state. If you cannot complete a step, surface the gap explicitly rather than reporting a simulated pass.
```

**Why:** Sub-agents have been observed (see `feedback_subagent_tool_hallucination.md`) reporting that they ran codex audit and surfacing simulated findings, when in fact no audit ran. The deliverable then carries a fake audit-passed marker that downstream consumers trust. The guard above is verbatim what the agent prompts say, plus the orchestrator-side post-verification (spec §5.3) that reads audit transcript metadata and rejects deliverables claiming audit completion without matching transcript.

This guard rides in agent prompts AND in audit dispatch. The agent prompt forbids fake claims; the dispatch reminds the auditor not to accept fake claims at face value.

---

## Worked example: synthesis_agent Phase 2 audit, round 2

```
Audit round: 2 of 3
Previous rounds: Round 1: P1×3 / P2×7 / P3×2 (12 total); all P1 closed; 4 P2 closed; 3 P2 + 2 P3 carried.

Bundle scope: Phase 2 chapter deliverables — synthesis output for chapter 4

Authoritative context (commit a1b2c3d):

Primary deliverables (audit target):
- chapter4_synthesis.md (synthesis_agent output, 14k words across 6 sections)
- chapter4_evidence_inventory.md (effect inventory per source, synthesis_agent companion artefact)

Supporting context (do not audit; reference only):
- shared/contracts/passport/literature_corpus_entry.schema.json
- deep-research/agents/synthesis_agent.md (the agent prompt — for understanding patterns, not for audit)
- chapter4_bibliography.json (bibliography_agent output, V2_CLEAN — verified upstream)

Out-of-scope (do not read):
- chapter1-3 / chapter5+ deliverables (separate bundles)

Round 2 job:
(a) Verify each round-1 finding closed correctly. List by ID.
(b) Audit for new issues introduced by round-1 corrections.
(c) Run the 7 audit dimensions on the two primary deliverables.
(d) Anchoring-bias residual check on closed findings.
(e) PARTIAL-vs-CLOSED check.
(f) Cross-section consistency check: for every source cited in 2+ sections of chapter4_synthesis.md, verify the source's characterization is compatible across sections; flag any pair of sections that pull the source's effect in incompatible directions (Pattern A1).

Convergence target: ZERO findings of ANY severity in one round.
[+ standard fallback]

Output:
[+ standard output format]

DO NOT simulate any audit step. [+ standard Section 7 anti-fake-audit guard]
```

---

## Cross-references

- `shared/references/irb_terminology_glossary.md` — referenced by dimension §3.5.
- `shared/references/psychometric_terminology_glossary.md` — referenced by dimension §3.5.
- `shared/references/protected_hedging_phrases.md` — referenced by Section 4(f) report_compiler bundle check (sub-checks ii + iii).
- `shared/references/word_count_conventions.md` — referenced by Section 4(f) report_compiler bundle check (sub-check i).
- ARS feedback memory `feedback_codex_iterative_spec_review_to_zero.md` — convergence target rationale.
- ARS feedback memory `feedback_cross_model_review_cascade_inconsistency.md` — round-N+1 cascade audit rationale.
- ARS feedback memory `feedback_subagent_tool_hallucination.md` — anti-fake-audit guard rationale.
- ARS feedback memory `feedback_codex_xhigh_for_drift_audit.md` — model + reasoning-effort selection (gpt-5.5 + xhigh for high-blast-radius bundles).
<!-- SOURCE-CONTENT-END -->
