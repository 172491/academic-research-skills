<a id="source-skills-academic-pipeline-references-changelog-md"></a>

## SOURCE: skills/academic-pipeline/references/changelog.md

<!-- SOURCE-CONTENT-BEGIN bytes=5919 -->
# Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.8 | 2026-04-21 | **Collaboration Depth Observer (v3.3.0)**: New `collaboration_depth_agent` (Agent Team grows from 3 to 4). Reads dialogue logs at every FULL/SLIM checkpoint and at pipeline completion; scores user-AI collaboration on 4 dimensions (Delegation Intensity / Cognitive Vigilance / Cognitive Reallocation / Zone Classification) per `shared/collaboration_depth_rubric.md` (rubric v1.0, canonical, CC-BY-NC 4.0). **Advisory only — never blocks.** MANDATORY checkpoints (2.5 / 4.5) do NOT invoke the observer (integrity gates preserved). Cross-model divergence flagged (not silently averaged) when `ARS_CROSS_MODEL` set. Rubric credits Wang, S., & Zhang, H. (2026). *IJETHE* 23:11. DOI 10.1186/s41239-026-00585-x. New lint: `scripts/check_collaboration_depth_rubric.py`. State tracker gains `dialogue_log_ref` per stage + `collaboration_depth_history[]` append-only. Reinforcement row added for checkpoint transitions. |
| 2.7 | 2026-03-27 | **Style Profile in Material Passport**: Pipeline orchestrator now carries optional Style Profile (Schema 10 in `shared/handoff_schemas.md`) through all stages. Produced by academic-paper intake Step 10 when user provides past writing samples. Consumed by draft_writer (Stage 2) and report_compiler (Stage 1) as soft writing voice guide. Does not affect integrity verification or review stages. Coordinates with deep-research v2.4 and academic-paper v2.5 |
| 2.6 | 2026-03-08 | **Handoff Data Schema**: Enhanced `shared/handoff_schemas.md` with 9 comprehensive schemas (RQ Brief, Bibliography, Synthesis, Paper Draft, Integrity Report, Review Report, Revision Roadmap, Response to Reviewers, Material Passport) with full field definitions, type constraints, and validation rules; orchestrator validates output against schemas before each transition. **Adaptive Checkpoint System**: Replaced static checkpoint template with 3-tier system (FULL/SLIM/MANDATORY) based on stage criticality and user engagement; FULL checkpoints include decision dashboard with metrics; SLIM auto-continues for experienced users; MANDATORY cannot be bypassed at integrity/review/finalization boundaries; awareness guard after 4+ auto-continues. **Mode Advisor**: New `references/mode_advisor.md` with unified cross-skill decision tree, common misconceptions table, user archetype recommendations, decision flowchart, and anti-patterns guide. **Team Collaboration Protocol**: New `references/team_collaboration_protocol.md` with 5 role definitions, per-transition handoff procedures, git branching/tagging strategy, conflict resolution matrix, and communication templates; state tracker extended with `assigned_to`, `approval_gate`, `team_notes` per stage and `schema_validation_log`. **Phase E Claim Verification**: New `references/claim_verification_protocol.md` with E1 claim extraction, E2 source tracing, E3 cross-referencing; verdict taxonomy (VERIFIED / MINOR_DISTORTION / MAJOR_DISTORTION / UNVERIFIABLE / UNVERIFIABLE_ACCESS); severity mapping (MAJOR_DISTORTION -> SERIOUS, UNVERIFIABLE -> SERIOUS, MINOR_DISTORTION -> MINOR, UNVERIFIABLE_ACCESS -> MEDIUM); integrated into integrity_verification_agent Mode 1 (30% spot-check) and Mode 2 (100%); pass/fail criteria updated to include Phase E verdicts. **Mid-Entry Material Passport Check**: Pipeline orchestrator now validates Material Passport on mid-entry; decision tree checks verification_status, freshness (< 24 hours), and content modification (version_label comparison); offers skip/spot-check/full re-verify options for Stage 2.5 when passport is valid; passport freshness validation rules added to `shared/handoff_schemas.md` |
| 2.5 | 2026-03-08 | External Review Protocol: structured intake of real journal reviewer feedback (text/PDF/DOCX); 4-step workflow (parse -> strategic coaching -> revise + Response to Reviewers -> completeness check); differentiated behavior from internal simulated review (no default "accept all", risk assessment per comment, user confirmation of parsed items); explicit capability boundaries (AI verification ≠ reviewer satisfaction) |
| 2.4 | 2026-03-08 | Stage 6 PROCESS SUMMARY: post-pipeline paper creation process record; asks user preferred language (zh/en/both); generates structured MD summarizing full human-AI collaboration history with user quotes, key decisions, iteration details, and lessons learned; mandatory final chapter: **Collaboration Quality Evaluation** (6 dimensions scored 1-100, bar chart visualization, What Worked Well / Missed Opportunities / Recommendations / Human vs AI Value-Add / Claude's Self-Reflection); compiles to PDF via LaTeX + tectonic; outputs `paper_creation_process_zh.pdf` + `paper_creation_process_en.pdf` |
| 2.3 | 2026-03-08 | Stage 5 FINALIZE: mandatory formatting style prompt (APA 7.0 / Chicago / IEEE); PDF must compile from LaTeX via tectonic (no HTML-to-PDF); APA 7.0 uses `apa7` document class (`man` mode) with XeCJK for bilingual support; font stack: Times New Roman + Source Han Serif TC VF + Courier New |
| 2.2 | 2026-03-05 | Checkpoint confirmation semantics (6 user commands with precise actions); mode switching rules (safe/dangerous/prohibited matrix); skill failure fallback matrix (per-stage degradation strategies); state ownership protocol (single source of truth with write access control); material version control (versioned artifacts with audit trail); cross-skill reference to `shared/handoff_schemas.md` |
| 2.1 | 2026-03 | Added plagiarism detection protocol (Phase D); enhanced integrity_verification_agent with originality verification (D1 WebSearch, D2 self-plagiarism); updated both verification modes |
| 2.0 | 2026-02 | Added Stage 2.5/4.5 integrity checks, two-stage review, mandatory checkpoints, Devil's Advocate, reproducibility guarantees, integrity_verification_agent |
| 1.0 | 2026-02 | Initial version: 5+1 stage pipeline |
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-literature-corpus-consumers-md"></a>

## SOURCE: skills/academic-pipeline/references/literature_corpus_consumers.md

<!-- SOURCE-CONTENT-BEGIN bytes=10080 -->
# Consumer Protocol — `literature_corpus[]` Reading

**Status**: Released in v3.6.5 (both Phase 1 consumers wired)
**Applies to**: any agent in this repo that reads `literature_corpus[]` from a Material Passport
**Authoritative spec**: [`docs/design/2026-04-26-ars-v3.6.5-consumer-integration-design.md`](../../docs/design/2026-04-26-ars-v3.6.5-consumer-integration-design.md)

## What this document covers

This is the contract every literature-reading consumer agent must follow. The v3.6.4 input port (`shared/contracts/passport/literature_corpus_entry.schema.json`) defines what enters a Material Passport; this document defines how Phase 1 agents read it.

The `corpus-first, search-fills-gap` flow has five steps; the four Iron Rules are non-negotiable; the PRE-SCREENED block is the reproducibility surface; failures are surfaced honestly via the `[CORPUS PARSE FAILURE: <cause>]` graceful fallback.

## Reading flow (shared by every consumer)

```
Step 0: Detect literature_corpus[] presence and minimal shape
Step 1: Pre-screen corpus against current RQ
Step 2: Search-fills-gap — case A / B / B' / C
Step 3: Merge included + external_included for downstream
Step 4: Emit Search Strategy Report with PRE-SCREENED block
```

The full flow specification lives in spec §3.1. Each consumer agent's `agent.md` must include the full Step 0–4 description and all four Step 2 case markers (case A / case B / case B' / case C). The lint enforces presence (L6).

## PRE-SCREENED block template

Every consumer emits the block in this exact shape (alphabetical ordering for citation_keys; truncate at 50 entries with appendix file). Spec §3.2 has the complete template plus truncation rules.

```markdown
PRE-SCREENED FROM USER CORPUS:
- Adapter: <obtained_via enum value | "<unspecified>" | "mixed (...)">
                                          # e.g., zotero-bbt-export, or "<unspecified>" per F4a,
                                          # or "<value> (N of M entries declared)" per F4b,
                                          # or "mixed (zotero-bbt-export: K, ..., undeclared: U)" per F4c
- Snapshot date: <max(obtained_at)>        # ISO 8601, or "<unspecified>" per F4d,
                                          # or "<date> (M of N entries declared)" per F4e,
                                          # or append "(spans <N> days; corpus may not be a single snapshot)" per F4f
- Total entries scanned: <N>
- Pre-screening result:
  - Included: <K> entries
    citation_keys:
      - <k1>
      - <k2>
  - Excluded by inclusion / exclusion criteria: <E> entries
    citation_keys:
      - <e1>
    (omit this sub-block if 0)
  - Skipped (criteria cannot be applied): <S> entries
    citation_keys with reasons:
      - <key>: <reason>
    (omit this sub-block if 0)
- Zero-hit note (emit per F3 only when Included: 0):
  Zero-hit note (corpus non-empty, 0 included after screening): possible
  causes are (a) corpus is stale relative to current RQ, (b) RQ has
  shifted away from what the user originally curated, (c) adapter
  exported entries unrelated to this RQ.
- Note: presence in corpus does not imply inclusion;
  same criteria applied to corpus and external sources.
```

## The four Iron Rules

### Iron Rule 1 — Same criteria

Apply the same Inclusion / Exclusion criteria to corpus entries and external database results. No exceptions. A corpus entry is not "pre-approved"; it must clear the same screening as a fresh database hit.

### Iron Rule 2 — No silent skip

Any skipped corpus entry must be recorded in the PRE-SCREENED block's skipped sub-section with a reason. Silently dropping an entry is a prompt-layer violation. The lint enforces structural markers; behaviour is enforced by the BAD / GOOD example pair below and observed in real runs.

<!-- BAD -->
```
[corpus has 5 entries]
agent includes 3, excludes 1 (off-topic), and silently drops 1 with empty
abstract because "I cannot evaluate it".

PRE-SCREENED block reports:
- Total entries scanned: 5
- Included: 3 entries
- Excluded: 1 entry
(no Skipped sub-block)

(1 entry silently disappeared from the pipeline: 3 + 1 ≠ 5 — Iron Rule 2 violation.)
```

<!-- GOOD -->
```
[corpus has 5 entries]
agent excludes 1 (off-topic), keeps 3 in pre_screened_included[].
agent records 1 with empty abstract as Skipped: "abstract empty after privacy clearing; criteria reference research method but only title is present, criteria cannot be applied".

PRE-SCREENED block reports:
- Included: 3 entries
- Excluded by inclusion / exclusion criteria: 1 entry
- Skipped (criteria cannot be applied): 1 entry
  - smith2024foo: abstract empty after privacy clearing; criteria reference research method but only title is present
- Note: presence in corpus does not imply inclusion;
  same criteria applied to corpus and external sources.
```

### Iron Rule 3 — No corpus mutation

Consumer agents never modify, backfill, or derive new content into `literature_corpus[]`. Read only. The Material Passport's corpus is the user's curated list; any rewriting belongs to the user's adapter (v3.6.4 input port), not Phase 1 prompt-layer agents.

### Iron Rule 4 — Graceful fallback on parse failure

Consumer agents do NOT re-validate schema, do NOT parse JSON Schema at runtime, and do NOT dereference `source_pointer` URIs. The v3.6.4 input-port lint validates adapter output, but a passport may reach a Phase 1 agent through other paths (hand-edits, `resume_from_passport`, assembled passports). When a consumer cannot parse `literature_corpus[]`, emit `[CORPUS PARSE FAILURE: <cause>]` in the Search Strategy Report and fall back to external-DB-only flow. Do not abort Phase 1, do not attempt schema repair, do not invent contents.

## Zero-hit and provenance reporting (F3 / F4)

Two reproducibility surfaces sit inside the PRE-SCREENED block. Every consumer agent must emit each one when the corresponding trigger fires; both are non-blocking and independent of which Step 2 case dispatches next.

**Zero-hit note (F3).** When `pre_screened_included[]` is empty after Step 1 — corpus is non-empty but no entry survived screening — the consumer emits a zero-hit note inside the PRE-SCREENED block listing the three plausible causes:

```
- Zero-hit note (corpus non-empty, 0 included after screening): possible causes
  are (a) corpus is stale relative to current RQ, (b) RQ has shifted away from
  what the user originally curated, (c) adapter exported entries unrelated to
  this RQ.
```

The note appears regardless of which Step 2 case fires next. Step 2 dispatch follows F3 in spec §4.1.

**Provenance reporting (F4a–F4f).** `obtained_via` and `obtained_at` are optional in v3.6.4 schema. The PRE-SCREENED block's `Adapter:` and `Snapshot date:` lines reflect actual coverage; consumers never invent enum values or guess timestamps.

| Sub-case | Trigger | `Adapter:` line content |
|---|---|---|
| F4a | Zero entries declare `obtained_via` | `Adapter: <unspecified>` + trailing note `Adapter origin not declared; user-written adapter should populate obtained_via per v3.6.4 schema recommendation.` |
| F4b | At least one entry declares; all declared share single value | `Adapter: <enum value> (N of M entries declared)` |
| F4c | Two or more distinct enum values among declared entries | `Adapter: mixed (zotero-bbt-export: K, obsidian-vault: L, ..., undeclared: U)` |

| Sub-case | Trigger | `Snapshot date:` line content |
|---|---|---|
| F4d | Zero entries declare `obtained_at` | `Snapshot date: <unspecified>` + trailing note `Snapshot date not declared; reproducibility is reduced. Adapter should populate obtained_at per v3.6.4 schema recommendation.` |
| F4e | Partial coverage | `Snapshot date: <max(obtained_at)> (M of N entries declared)` |
| F4f | Wide spread (>90 days between min and max) | append `(spans <N> days; corpus may not be a single snapshot)`. Composes with F4e. |

F4a/b/c are mutually exclusive by trigger. F4d applies only when zero entries declare `obtained_at`; F4e and F4f compose. See spec §4.2 for the full precedence reasoning.

## Consumer: bibliography_agent

**Status**: Wired in v3.6.5
**Skill**: deep-research
**Phase**: 1 (literature search and curation)
**Agent file**: [`deep-research/agents/bibliography_agent.md`](../../deep-research/agents/bibliography_agent.md)

The deep-research bibliography agent applies the corpus-first flow during its systematic literature search. The PRE-SCREENED block sits inside the Search Strategy section of its Annotated Bibliography output (per the agent's existing Output Format), preceding the existing DATABASES / Inclusion-Exclusion / RESULTS structure.

When `literature_corpus[]` is non-empty and parses cleanly, the agent enters Step 1 pre-screening. When the corpus is absent, empty, or fails the minimal shape check, the agent runs its existing external-DB-only flow (Iron Rule 4 graceful fallback for the failure cases).

## Consumer: literature_strategist_agent

**Status**: Wired in v3.6.5
**Skill**: academic-paper
**Phase**: 1 (literature search and curation)
**Agent file**: [`academic-paper/agents/literature_strategist_agent.md`](../../academic-paper/agents/literature_strategist_agent.md)

The academic-paper literature strategist agent applies the corpus-first flow during its literature search strategy phase. The PRE-SCREENED block sits inside the Search Strategy section of the Literature Search Report (per the agent's existing Output Format), immediately before the `Databases` line. The merged `final_included` set feeds the agent's downstream Annotated Bibliography, Literature Matrix, Research Gap Identification, and Recommended Sources by Paper Section outputs without altering their formats.

When `literature_corpus[]` is non-empty and parses cleanly, the agent enters Step 1 pre-screening, and Step 2 search-fills-gap dispatches the external 4-Layer Progressive Strategy. When the corpus is absent, empty, or fails the minimal shape check, the agent runs its existing 4-Layer external-DB-only flow unchanged (Iron Rule 4 graceful fallback for the failure cases).
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-mode-advisor-md"></a>

## SOURCE: skills/academic-pipeline/references/mode_advisor.md

<!-- SOURCE-CONTENT-BEGIN bytes=8025 -->
# Mode Advisor — Unified Cross-Skill Decision Tree

## Purpose

Helps users (and the pipeline orchestrator) select the right skill and mode for their current situation. Eliminates the most common routing mistakes by mapping user intent to the optimal entry point.

---

## Quick Decision Matrix

| What do you want? | How far along? | Time? | Skill + Mode |
|-------------------|---------------|-------|--------------|
| Explore a topic | Starting fresh | 30 min | deep-research quick |
| Explore a topic | Starting fresh | 2+ hr | deep-research full |
| Think through a research idea | Have vague idea | Any | deep-research socratic |
| Systematic review | Have clear PICO | 3+ hr | deep-research systematic-review |
| Verify claims | Have specific claims | 30 min | deep-research fact-check |
| Write a paper | Have research done | 2+ hr | academic-paper full |
| Plan a paper step by step | Have RQ, need structure | 1+ hr | academic-paper plan |
| Fix citations | Have draft | 30 min | academic-paper citation-check |
| Convert format | Have final draft | 15 min | academic-paper format-convert |
| Review a paper | Have paper to evaluate | 1 hr | academic-paper-reviewer full |
| Check revision quality | Have revised draft | 30 min | academic-paper-reviewer re-review |
| Full pipeline (zero to publication) | Starting fresh | 5+ hr | academic-pipeline |
| Handle real reviewer feedback | Have review comments | 1+ hr | academic-pipeline (Stage 4 entry) |

---

## Common Misconceptions

| User Says | They Probably Need | Why |
|-----------|-------------------|-----|
| "Write me a paper on X" | deep-research first, THEN academic-paper | Writing without research produces shallow papers with unsupported claims |
| "Review my paper" (but no draft exists) | academic-paper plan mode | They need to write first, not review |
| "Check my citations" (but paper isn't done) | academic-paper full mode | Finish writing first, then check citations as a separate pass |
| "I need a systematic review" | deep-research systematic-review mode | NOT academic-paper lit-review structure (different methodology: PRISMA vs narrative) |
| "Just give me a quick paper" | deep-research quick + academic-paper full | Quick research is fine, but paper writing still needs the full mode for quality |
| "Format my paper as APA" | academic-paper format-convert mode | Not a rewrite; purely formatting transformation |
| "I got reviewer comments" | academic-pipeline Stage 4 entry (External Review) | Needs structured intake + strategic coaching, not just "fix what they said" |

---

## User Archetype Recommendations

| Archetype | Recommended Workflow | Rationale |
|-----------|---------------------|-----------|
| Graduate student (first paper) | deep-research socratic -> academic-paper plan -> full pipeline | Socratic mode builds research thinking; plan mode structures the paper incrementally; pipeline ensures quality gates |
| Experienced researcher (submission prep) | academic-pipeline (full, from Stage 1 or mid-entry) | Knows what they want; benefits from the automated quality assurance and integrity checks |
| Advisor reviewing student work | academic-paper-reviewer full | Provides structured multi-perspective feedback the advisor can use in mentoring |
| Quick literature scan | deep-research quick or lit-review | Fast turnaround; no need for full pipeline overhead |
| Journal revision response | academic-pipeline (Stage 4 entry with review comments) | External Review Protocol handles real reviewer feedback with strategic coaching |
| Conference paper (short deadline) | deep-research quick -> academic-paper full (conference type) | Compressed timeline; quick research + full writing with conference structure |
| Thesis chapter | deep-research full -> academic-paper full | Each chapter treated as a standalone paper; full depth needed |
| Policy brief | deep-research quick -> academic-paper full (policy_brief type) | Evidence-based but concise; quick research sufficient for policy scope |

---

## Skill Capability Boundaries

Understanding what each skill can and cannot do prevents misrouting:

| Skill | Can Do | Cannot Do |
|-------|--------|-----------|
| deep-research | Literature search, synthesis, RQ refinement, fact-checking | Write papers, review papers, format documents |
| academic-paper | Write papers, revise papers, format documents, check citations | Conduct original research, review papers (as reviewer), verify integrity |
| academic-paper-reviewer | Review papers (5-person panel), re-review revisions | Write papers, conduct research, fix issues (only identifies them) |
| academic-pipeline | Orchestrate all stages, manage transitions, track state | Perform any substantive work (purely dispatching and coordinating) |
| integrity_verification_agent | Verify references, citations, data, originality | Fix issues (only identifies them), review paper quality |

---

## Decision Flowchart

```
START: What does the user want?
  |
  +--> "I want to research/explore/investigate"
  |      |
  |      +--> Have specific claims to verify? --> deep-research fact-check
  |      +--> Have clear PICO/systematic question? --> deep-research systematic-review
  |      +--> Want guided exploration? --> deep-research socratic
  |      +--> Want direct results, have time? --> deep-research full
  |      +--> Want direct results, short on time? --> deep-research quick
  |
  +--> "I want to write a paper"
  |      |
  |      +--> Have research/literature ready? --> academic-paper (plan or full)
  |      +--> No research done yet? --> deep-research FIRST, then academic-paper
  |      +--> Want full quality assurance? --> academic-pipeline (from Stage 1)
  |
  +--> "I want someone to review my paper"
  |      |
  |      +--> Have a complete draft? --> academic-paper-reviewer full
  |      +--> Want integrity check + review? --> academic-pipeline (Stage 2.5 entry)
  |      +--> No draft yet? --> academic-paper first
  |
  +--> "I need to revise based on feedback"
  |      |
  |      +--> From AI reviewers (pipeline)? --> Continue pipeline (Stage 4)
  |      +--> From real journal reviewers? --> academic-pipeline Stage 4 entry (External Review)
  |
  +--> "I want the full treatment (research to publication)"
         |
         +--> academic-pipeline (Stage 1 entry)
```

---

## Pipeline Stage Entry Points

For users entering the pipeline mid-stream, this table clarifies what materials are needed:

| Entry Point | Required Materials | What Gets Skipped | Integrity Implications |
|------------|-------------------|-------------------|----------------------|
| Stage 1 (RESEARCH) | None | Nothing | Full pipeline |
| Stage 2 (WRITE) | RQ Brief + Bibliography | Stage 1 | Full pipeline from Stage 2 |
| Stage 2.5 (INTEGRITY) | Paper draft | Stages 1-2 | Integrity check runs on provided draft |
| Stage 3 (REVIEW) | Verified paper + integrity report | Stages 1-2.5 | User must provide integrity evidence |
| Stage 4 (REVISE) | Paper + review comments | Stages 1-3 | Pipeline runs Stage 4 -> 3' -> 4' -> 4.5 -> 5 |
| Stage 5 (FINALIZE) | Paper + integrity pass report | Stages 1-4.5 | Must show Stage 4.5 passed |

---

## Anti-Patterns

These are common workflow mistakes to avoid:

| Anti-Pattern | Problem | Correct Approach |
|-------------|---------|-----------------|
| Skipping research | Paper lacks evidence depth | Always do at least deep-research quick |
| Writing then researching | Confirmation bias in source selection | Research first, write second |
| Reviewing before integrity check | Wasted review effort on fabricated citations | Always Stage 2.5 before Stage 3 |
| Accepting all reviewer comments blindly | May introduce inconsistencies or weaken valid arguments | Use External Review Protocol's strategic coaching |
| Running pipeline for a 1-page abstract | Overhead far exceeds benefit | Use academic-paper full directly |
| Using fact-check mode for literature review | Different purpose and methodology | Use deep-research full or systematic-review |
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-passport-as-reset-boundary-md"></a>

## SOURCE: skills/academic-pipeline/references/passport_as_reset_boundary.md

<!-- SOURCE-CONTENT-BEGIN bytes=17364 -->
# Passport as Reset Boundary (v3.6.3)

## Purpose

Defines how `pipeline_orchestrator_agent` converts FULL checkpoints into reset boundaries when `ARS_PASSPORT_RESET=1` is set. This is the authoritative protocol; any divergent behavior in agent prompts is a bug.

## When this protocol applies

| Flag state | Mode | Behavior at FULL checkpoint |
|------------|------|-----------------------------|
| `ARS_PASSPORT_RESET` unset / `=0` | any | Continuation (pre-v3.6.3 default). No reset tag emitted. |
| `ARS_PASSPORT_RESET=1` | `systematic-review` | **Mandatory reset** at every FULL checkpoint. |
| `ARS_PASSPORT_RESET=1` | any other mode | **Strong-default reset** at every FULL checkpoint. User `continue` response overrides back to continuation for the next stage only. |

MANDATORY checkpoints (integrity Stage 2.5 / 4.5, review decisions, Stage 5 finalization) are orthogonal: reset can co-occur with MANDATORY. SLIM checkpoints never trigger reset.

## The reset boundary protocol

When the orchestrator reaches a FULL checkpoint with the flag ON:

1. **Freeze state.** `state_tracker` stages the current stage's deliverables and prepares a new `kind: boundary` ledger entry — but does NOT yet write `hash` (append happens in Step 2 after hash is known).
2. **Compute hash.** Canonical byte serialization is normative; two implementations must produce the same bytes from the same ledger:
   - Each entry is serialized as **JSON Canonical Form (RFC 8785 / JCS)**: UTF-8, no insignificant whitespace, keys sorted ASCII-ascending at every object level, numbers in JCS canonical form.
   - Entries are separated by a single `\x0a` (LF) byte. The first entry has no leading separator; the last entry has a trailing LF.
   - The new entry is serialized with `hash` set to the canonical placeholder `"000000000000"` and all other fields populated; concatenated AFTER every prior entry (each already carrying its own finalized `hash`).
   - SHA-256 the byte stream. Take the lowercase hex digest. Take the first 12 characters. That IS the new entry's `hash`. Overwrite the placeholder before appending to the ledger.
   - **Iron rule (see §Iron rules 2 + 7):** never hash an entry that already contains a non-placeholder `hash` for itself; never reorder prior entries; never include `kind: resume` entries in a boundary hash computation.
3. **Emit reset tag.** In the checkpoint notification block, append a machine-stable line:
   ```
   [PASSPORT-RESET: hash=<hash>, stage=<completed>, next=<next>]
   ```
4. **Emit human instruction.** In the same checkpoint notification, include a `### Resume Instruction` subsection with:
   - Passport file path (absolute or repo-relative)
   - The exact resume command the user pastes into a fresh session:
     ```
     resume_from_passport=<hash>
     ```
   - A one-line note that the next stage should be invoked in a fresh Claude Code session to realize the token-savings intent.
5. **Halt after emission.** The orchestrator stops after emitting the reset boundary and awaits resume in a fresh session.
6. **In-session override (non-SR modes).** If the user pastes `continue` in the same session, the orchestrator acknowledges but treats the passport as the only input to the next stage. Working-memory content from prior turns is non-authoritative and must not be replayed.
7. **Systematic-review hard stop.** In `systematic-review` mode, in-session continuation is refused outright. The orchestrator repeats the Resume Instruction and asks the user to start a fresh session.
8. **Pending MANDATORY decision.** If the reset co-occurs with a MANDATORY checkpoint that requires a user decision with multiple valid branches (e.g., Stage 3 review outcome: `revise` / `restructure` / `abort`; Stage 5 finalization format choice), the orchestrator sets `pending_decision` on the ledger entry. Each option is an object with required fields `value` (branch identifier) and `next_stage` (stage to route to, or `null` to terminate), plus optional `next_mode` for downstream mode override. On resume, the orchestrator looks up the user's chosen `value` in `options[]` and uses that entry's `next_stage`/`next_mode` to determine actual routing. The boundary entry's `next` field is populated as a best-guess default only; it is advisory and is superseded by the matched option's `next_stage` at resume time. `next` must NOT be used to auto-advance when `pending_decision` is present. `next` MAY be `null` when all branches of `pending_decision` terminate or when no sensible default exists.

## `resume_from_passport` mode contract

Invocation shape (prompt-layer, user-pasted or auto-dispatched in a new session):

```
resume_from_passport=<hash> [stage=<stage_number_or_name>] [mode=<downstream_mode>]
```

Required:
- `resume_from_passport=<hash>` — must match the 12-hex `hash` from a `[PASSPORT-RESET: ...]` tag emitted in a prior session. Orchestrator verifies the hash against the passport ledger on disk; mismatch is a hard error.

Optional:
- `stage=<stage_number_or_name>` — override the `next=` recorded in the reset tag. Useful when the user wants to re-run a stage rather than proceed. If omitted, the orchestrator uses `next=` from the reset tag.
- `mode=<downstream_mode>` — override the mode of the next stage (e.g., swap `full` for `quick`). Orchestrator validates the override against Mode Advisor rules.

Orchestrator obligations on resume:
- Locate the target `kind: boundary` entry by matching `hash`. Hard error if no match, or if a later `kind: resume` entry already carries `consumes_hash == <hash>` (double-resume is forbidden).
- Do NOT ask the user to re-summarize prior stages; the passport is authoritative. Load artifacts by reference (paths or IDs recorded in the entry).
- Honor the `verification_status` field. If `STALE` or `UNVERIFIED`, display a warning and prompt the user to re-verify before continuing. If `VERIFIED`, proceed without prompting.
- If `pending_decision` is set on the ledger entry, re-prompt the user for that decision BEFORE invoking any downstream stage. Display `pending_decision.question` and each option's `value`. After the user picks, look up the matching entry in `options[]` by `value`, then use that entry's `next_stage` and `next_mode` to determine actual routing. Record the chosen `value` as `chosen_branch` on the new `resume` entry. `next` on the boundary entry is advisory and is superseded by the matched option's `next_stage`. A user-supplied `stage=<n>` override on the resume command does NOT satisfy `pending_decision` — the decision prompt always fires when `pending_decision` is present. CLI `stage=`/`mode=` overrides still win over option routing if the user supplies them after the decision prompt.
- Emit a `### Resume Acknowledged` section at the start of the new session with: hash, source session `session_marker` + `generated_at`, recovered stage, and next-stage plan.
- Append a new `kind: resume` entry to `reset_boundary[]` with `consumes_hash = <hash>`, fresh `generated_at` and `session_marker`, and (if applicable) `chosen_branch` + `user_override`. This is how resume leaves an append-only trace and lets downstream readers compute `awaiting_resume` from the ledger alone.

## Append-only ledger semantics

Material Passport ledger (`compliance_history[]` + new `reset_boundary` entries) is append-only:
- Every checkpoint with the flag ON appends one `reset_boundary` entry of kind `boundary` under Schema 9's `reset_boundary` field.
- Re-running a stage (e.g., after a review rejection) appends a new entry with `version_label` bumped (`v1.0 → v1.1-revised`).
- `resume_from_passport` consumption appends one entry of kind `resume` to the same ledger, carrying the `consumes_hash` pointer to the `boundary` entry it resolves. This is how resume leaves a trace — no mutation of prior entries.
- Prior entries are never deleted, reordered, or mutated.
- Stage-re-run cases produce adjacent entries for the same `stage`; both are preserved.

### Computing `awaiting_resume` from the ledger

A `boundary` entry with hash `H` is considered **awaiting resume** iff no `resume` entry exists later in the ledger with `consumes_hash == H`. Downstream readers (state machine, observers, external audit tools) compute this by a single pass over `reset_boundary[]` — no out-of-band state required.

## Concurrency model

Resume consumption is a three-step read-modify-write on the passport ledger:

1. Read the ledger and locate the target `boundary` entry by `hash`.
2. Verify no `resume` entry later in the ledger carries `consumes_hash` equal to that hash.
3. Append a new `resume` entry.

Without coordination, two processes can complete step 2 in parallel before either reaches step 3, both observe "no prior resume", and both append. The append-only-ledger invariant survives, but the "one boundary, one resume" invariant breaks. To prevent this, every compliant orchestrator implementation MUST hold an exclusive advisory lock on the passport file for the entire read-check-append sequence.

**POSIX requirement.** On POSIX systems the lock is an `fcntl` exclusive advisory lock (`fcntl.flock(fd, fcntl.LOCK_EX)` in Python, `flock(fd, LOCK_EX)` in C). Acquire before step 1, release after step 3. Do not release between steps under any circumstance. Releasing between steps 2 and 3 reopens the exact race this rule prevents.

**Lock timeout.** Acquisition MUST use a bounded timeout not exceeding 60 seconds; 30 seconds is RECOMMENDED. The passport write is a few-KB append and fsync, so this bound is two orders of magnitude above any reasonable write latency. 60 s is the hard ceiling because a user waiting longer will assume the orchestrator hung; 30 s leaves slack for slow fsync on NFS or sandboxed filesystems. A timeout at this scale indicates a stuck or crashed peer rather than lock contention. Timeout is a hard error; the orchestrator surfaces it to the user with a "passport locked by another session" message and does NOT retry automatically.

**Non-POSIX (Windows).** `fcntl` is unavailable. Compliant implementations use `msvcrt.locking` with `LK_NBLCK`/`LK_LOCK`, or a cross-platform library like `portalocker`. Implementations that cannot provide OS-level exclusion MUST fail loudly on resume with a "concurrency protection unavailable on this platform" error and refuse to consume the boundary. Silent best-effort is forbidden.

**Observability.** The lock is advisory: external readers that don't honor the protocol can still read the passport. Only cooperating writers get safety. This is acceptable because the passport is intended to be consumed by one tool family (ARS-compatible orchestrators).

## Iron rules

1. Flag OFF is pre-v3.6.3 behavior, bit-for-bit.
2. Ledger is append-only. No exception, no "clean up" operation.
3. Reset tag is the sole machine-stable handoff. Human-readable `### Resume Instruction` is for user ergonomics; consumers parse the tag.
4. `systematic-review` with flag ON refuses in-session continuation across FULL checkpoints.
5. Hash mismatch on resume is a hard error; orchestrator never proceeds on a guessed or coerced hash.
6. MANDATORY checkpoints are not downgraded by reset; they co-occur.
7. Hash is computed over the entry with the canonical placeholder `"000000000000"` in the `hash` field, serialized per the byte rules in §"The reset boundary protocol" step 2. `kind: resume` entries are never included in a `boundary` hash computation — the hash covers only prior `boundary` entries plus the new boundary entry itself. Any other convention (exclude-field, variable-length placeholder, post-hoc mutation, including resume entries) breaks cross-implementation interoperability and is forbidden.
8. A `boundary` entry is "consumed" only by appending a `resume` entry with matching `consumes_hash`. If a `boundary` entry has `pending_decision` set, the orchestrator MUST re-prompt the user on resume and MUST NOT auto-advance using `next`. Each option in `pending_decision.options[]` carries its own routing (`next_stage`/`next_mode`); the boundary entry's `next` field is advisory only and MAY be `null` when all branches terminate or no sensible default exists. Actual routing on resume comes from the matched option's `next_stage`/`next_mode`, not from the boundary `next` field.
9. Resume consumption MUST hold an exclusive advisory lock on the passport file for the entire read-check-append sequence. Releasing the lock between the no-prior-resume check and the resume-entry append reopens the double-resume race the rule exists to prevent. Non-POSIX implementations that cannot provide OS-level exclusion MUST refuse to resume rather than degrade silently.

## Interaction with existing features

- **Collaboration Depth Observer (v3.5.0):** fires on FULL/SLIM as before. Observer output is included in the checkpoint notification regardless of reset state. Observer state does NOT carry across resets; each fresh session observes only its own stage.
- **Compliance agent (v3.4.0):** `compliance_history[]` remains append-only and is consumed from the passport on resume. No change to Schema 12.
- **Sprint contract (v3.6.2):** reviewer sprint contracts load from the passport on resume (Phase 1 paper-content-blind stage remains valid across the reset boundary because the contract + paper metadata are carried in the passport).
- **Socratic reading probe (v3.5.1):** reading probe fires at most once per session. Across a reset boundary, the probe counter resets — the next session may fire its own probe. This is by design: each session is its own Socratic unit.
- **Audit artifact ledger (v3.6.7):** Schema 9's `audit_artifact[]` ledger ([`shared/handoff_schemas.md`](../../shared/handoff_schemas.md) "Audit Artifact Ledger") is also append-only and survives reset by the same mechanism as `reset_boundary[]` and `compliance_history[]` — the passport carries it intact across the session break. On `resume_from_passport`, the orchestrator does NOT replay prior audit runs; it re-verifies on demand at each gate transition. Per [`docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md`](../../docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md) §5.6, the orchestrator first runs Path A — selecting the latest `audit_artifact[]` entry matching the current gate's `(stage, agent, deliverable_sha)` tuple by `verified_at` — after the §5.6 A1.5 superseding-proposal preflight against `<output-dir>` (which preempts the selected entry if a higher-`verdict.round` proposal exists, e.g., from a between-session `another_round` wrapper run). Path A then re-runs the §5.2 verification sequence against the selected entry: L2-1 / L3-1 file-existence + schema preconditions over `artifact_paths.{jsonl,sidecar}`, followed by the eleven Layer 2 + Layer 3 gating checks (L2-2 / L2-3 / L2-4 / L2-5 + L3-2 through L3-8) over the JSONL stream, sidecar metadata, and the current on-disk deliverable + bundle files. After the §5.2 sequence passes, §5.6 Path A step A5 separately validates the verdict file against `audit_verdict.schema.json` and reconciles its mirror in the persisted entry (the verdict file is NOT inside the eleven §5.2 gates — it is A5's responsibility). The selected entry falls through to Path B (fresh proposal merge) on any §5.2 precondition / gate failure or A5 verdict-validation failure: e.g., a missing or schema-invalid jsonl/sidecar (L2-1 / L2-2 / L3-1), the JSONL `thread.started` `thread_id` drifting from the sidecar's `stream.jsonl_thread_id` (L3-2), the on-disk deliverable's SHA-256 drifting from the entry's `deliverable_sha` (L3-3, the canonical "deliverable mutated since audit" trigger), the bundle manifest hash recomputed over current primary + supporting + template files drifting from `bundle_manifest_sha` (L3-4), or the verdict file failing its schema/mirror check at A5. Stale or non-selected historical entries remain in the ledger as audit history and do NOT block unrelated future transitions; only the gate currently being audited must reach a fresh PASS / MINOR / MATERIAL verdict. This closes the post-reset attack surface where a forged passport carries `verified_at` / `verified_by` timestamps but no recoverable evidence behind them.

## What this protocol does NOT do

- Does not define Zotero / Obsidian / folder-scan adapter shapes (defined in [`academic-pipeline/references/adapters/overview.md`](adapters/overview.md) from v3.6.4+).
- Does not define `literature_corpus` entry shape (defined in [`shared/contracts/passport/literature_corpus_entry.schema.json`](../../shared/contracts/passport/literature_corpus_entry.schema.json) from v3.6.4+).
- Does not add runtime CLI tooling. Passport resolution is the user's responsibility — the orchestrator loads from the path the user provides.
- Does not claim specific token savings numbers. Empirical measurement goes in `docs/PERFORMANCE.md` only after real runs.

## Related references

- [`shared/handoff_schemas.md`](../../shared/handoff_schemas.md) — Schema 9 definition
- [`academic-pipeline/agents/pipeline_orchestrator_agent.md`](../agents/pipeline_orchestrator_agent.md) — orchestrator integration
- [`academic-pipeline/references/pipeline_state_machine.md`](pipeline_state_machine.md) — state transitions
- [`docs/PERFORMANCE.md`](../../docs/PERFORMANCE.md) — long-running session guidance
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-pipeline-state-machine-md"></a>

## SOURCE: skills/academic-pipeline/references/pipeline_state_machine.md

<!-- SOURCE-CONTENT-BEGIN bytes=15718 -->
# Pipeline State Machine v2.0 — Complete Definition

This document defines all legal states, transition conditions, transition actions, and exception handling for academic-pipeline v2.0.

---

## State Definitions

### Stage States

| State | Description |
|-------|------------|
| `pending` | Not yet started, waiting for prerequisite stage to complete |
| `in_progress` | Currently executing |
| `completed` | Completed, deliverables recorded |
| `skipped` | User chose to skip (only for non-mandatory stages) |
| `blocked` | Preconditions not met (e.g., integrity check FAIL) |

### Pipeline Global States

| State | Description |
|-------|------------|
| `initializing` | Detecting entry point and materials |
| `running` | Pipeline executing (at least one stage is in_progress) |
| `awaiting_confirmation` | Stage complete, waiting for user to confirm checkpoint |
| `paused` | User paused, can resume at any time |
| `completed` | All required stages complete, final paper produced |
| `aborted` | User abandoned (e.g., chose to abandon after Reject) |

---

## State Transition Diagram (ASCII)

```
                        +-------------+
                        | INITIALIZING|
                        +------+------+
                               |
                    [Detect entry point & materials]
                               |
         +----------+----------+----------+----------+
         |          |          |          |          |
         v          v          v          v          v
    +--------+ +--------+ +--------+ +--------+ +--------+
    |Stage 1 | |Stage 2 | |Stg 2.5 | |Stage 3 | |Stage 4 |
    |RESEARCH| | WRITE  | |INTEGRIT| | REVIEW | | REVISE |
    +---+----+ +---+----+ +---+----+ +---+----+ +---+----+
        |          |          |          |          |
   [checkpoint]   [checkpoint]   |     [checkpoint]  |
        |          |          |          |          |
        v          v          v          v          v
   +--------+ +--------+ +---+----+    |          |
   |Stage 2 | |Stg 2.5 | |PASS?   |    |          |
   | WRITE  | |INTEGRIT| +---+----+    |          |
   +---+----+ +---+----+     |         |          |
                         +----+----+    |          |
                         |         |    |          |
                        Yes       No    |          |
                         |     [Fix]    |          |
                         |   [Re-verify]|          |
                    [checkpoint]   |    |          |
                         |         |    |          |
                         v         |    |          |
                    +--------+     |    |          |
                    |Stage 3 | <---+    |          |
                    | REVIEW |          |          |
                    +---+----+          |          |
                        |               |          |
                   [DECISION]           |          |
                        |               |          |
              +---------+---------+     |          |
              |         |         |     |          |
            Accept    Minor     Major   |          |
              |       Revision  Revision|          |
              |         |         |     |          |
              |    [checkpoint]  [checkpoint]      |
              |         |         |     |          |
              |         v         v     |          |
              |    +--------+ +--------+|          |
              |    |Stage 4 | |Stage 4 ||          |
              |    | REVISE | | REVISE ||          |
              |    +---+----+ +---+----+|          |
              |        |          |     |          |
              |   [checkpoint]   [checkpoint]      |
              |        |          |     |          |
              |        v          v     |          |
              |    +--------+ +--------+           |
              |    |Stg 3'  | |Stg 3'  |           |
              |    |RE-REV. | |RE-REV. |           |
              |    +---+----+ +---+----+           |
              |        |          |                 |
              |   [DECISION]  [DECISION]            |
              |        |          |                 |
              |     Accept      Major               |
              |     /Minor        |                 |
              |        |     [checkpoint]           |
              |        |          |                 |
              |        |          v                 |
              |        |     +--------+             |
              |        |     |Stg 4'  |             |
              |        |     |RE-REVIS|             |
              |        |     +---+----+             |
              |        |          |                 |
              |   [checkpoint]  [checkpoint]        |
              |        |          |                 |
              v        v          v                 |
         +----+--------+----------+-----+           |
         |     Stage 4.5                |           |
         |   FINAL INTEGRITY            |           |
         +----------+------------------+           |
                    |                               |
               [PASS? Zero issues]                  |
                    |                               |
              +-----+-----+                         |
              |           |                         |
             Yes         No                         |
              |        [Fix]                         |
              |      [Re-verify]                     |
         [checkpoint]     |                         |
              |           |                         |
              v           |                         |
         +--------+       |                         |
         |Stage 5 | <-----+                         |
         |FINALIZE|                                 |
         +---+----+                                 |
             |                                      |
             v                                      |
         +-------+                                  |
         |  END  |                                  |
         +-------+                                  |
```

---

## Legal State Transitions

### Normal Flow Transitions

| From | To | Precondition | Action |
|------|----|-------------|--------|
| INIT | Stage 1 | User confirms starting from Stage 1 | Detect mode preference, launch deep-research |
| INIT | Stage 2 | User has research materials, confirms skipping Stage 1 | Detect materials, launch academic-paper |
| INIT | Stage 2.5 | User has complete paper | Launch integrity_verification_agent |
| INIT | Stage 3 | User has verified paper + integrity report | Confirm paper language/domain, launch reviewer |
| INIT | Stage 4 | User has review comments | Confirm paper + review comments, launch revision |
| INIT | Stage 5 | User has final draft for format conversion | Confirm format requirements, launch format-convert |
| Stage 1 | **checkpoint** | Stage 1 completed | Wait for user confirmation |
| checkpoint | Stage 2 | User confirms | handoff RQ Brief + Bibliography + Synthesis |
| Stage 2 | **checkpoint** | Stage 2 completed, Paper Draft produced | Wait for user confirmation |
| checkpoint | Stage 2.5 | User confirms | Pass Paper Draft to integrity agent |
| Stage 2.5 | **checkpoint** | PASS | Wait for user confirmation |
| Stage 2.5 | Stage 2.5 (retry) | FAIL | Fix issues, re-verify (max 3 rounds) |
| checkpoint | Stage 3 | User confirms | Pass verified paper to reviewer |
| Stage 3 | **checkpoint** | Decision produced | Wait for user confirmation |
| checkpoint | Stage 4 | Decision = Minor/Major, user confirms | Pass Revision Roadmap |
| checkpoint | Stage 4.5 | Decision = Accept, user confirms | Skip revision, go directly to final verification |
| Stage 4 | **checkpoint** | Stage 4 completed | Wait for user confirmation |
| checkpoint | Stage 3' | User confirms | Pass Revised Draft + Response to Reviewers |
| Stage 3' | **checkpoint** | Decision produced | Wait for user confirmation |
| checkpoint | Stage 4.5 | Decision = Accept/Minor, user confirms | Pass final draft to final verification |
| checkpoint | Stage 4' | Decision = Major, user confirms | Pass new Revision Roadmap |
| Stage 4' | **checkpoint** | Stage 4' completed | Wait for user confirmation |
| checkpoint | Stage 4.5 | User confirms | Pass revised draft to final verification |
| Stage 4.5 | **checkpoint** | PASS (zero issues) | Wait for user confirmation |
| Stage 4.5 | Stage 4.5 (retry) | FAIL | Fix issues, re-verify (max 3 rounds) |
| checkpoint | Stage 5 | User confirms | Pass final accepted draft |

### Special Flow Transitions

| From | To | Precondition | Action |
|------|----|-------------|--------|
| Stage 3 (Reject) | Stage 2 | User chooses to restructure | Clear Stage 2-3 state, preserve Stage 1 materials, restart Stage 2 |
| Stage 3 (Reject) | ABORT | User chooses to abandon | Save all produced materials, mark pipeline aborted |
| Stage 3' (Major) | Stage 4' | User confirms | Last revision opportunity |
| Stage 4' | Stage 4.5 | Revision complete | Go directly to final verification (no return to review) |
| Any stage | PAUSED | User says "pause" or "stop here" | Save pipeline state |
| PAUSED | Previous stage | User returns to continue | Restore pipeline state, display Dashboard |

### Prohibited Transitions (Illegal)

| From | To | Reason |
|------|----|--------|
| Stage 1 | Stage 3 | Cannot skip Stage 2 and 2.5 (unless mid-entry + has paper) |
| Stage 2 | Stage 3 | **Cannot skip Stage 2.5 (integrity check is mandatory)** |
| Stage 4 | Stage 5 | Cannot skip RE-REVIEW (revision must be re-reviewed) |
| Stage 3' | Stage 5 | **Cannot skip Stage 4.5 (final integrity check is mandatory)** |
| Stage 4' | Stage 3' | Cannot return to RE-REVIEW (max 1 round of RE-REVISE) |
| Stage 5 | Stage 3 | Cannot roll back (no review after FINALIZE) |
| completed | in_progress | Completed stages cannot restart |

---

## Material Dependency Matrix

| Material | Produced At | Consumed At | Required/Recommended |
|----------|-----------|-------------|---------------------|
| RQ Brief | Stage 1 | Stage 2 (Phase 0) | Recommended |
| Methodology Blueprint | Stage 1 | Stage 2 (Phase 0) | Recommended |
| Bibliography | Stage 1 | Stage 2 (Phase 1) | Recommended |
| Synthesis Report | Stage 1 | Stage 2 (Phase 3) | Recommended |
| Paper Draft | Stage 2 | Stage 2.5 (input) | **Required** |
| **Integrity Report (Pre)** | **Stage 2.5** | **Stage 3 (prerequisite)** | **Required** |
| **Verified Paper Draft** | **Stage 2.5** | **Stage 3 (Phase 0)** | **Required** |
| Review Reports (x5) | Stage 3 | Stage 4 (input) | Required |
| Editorial Decision | Stage 3 | Stage 4 (input) | Required |
| Revision Roadmap | Stage 3 | Stage 4 (input) | Required |
| Revised Draft | Stage 4 | Stage 3' (Phase 0) | Required |
| Response to Reviewers | Stage 4 | Stage 3' (input) | Recommended |
| **Re-Review Report** | **Stage 3'** | **Stage 4' (input)** | **Required (if Major)** |
| **Re-Revised Draft** | **Stage 4'** | **Stage 4.5 (input)** | **Required (if executed)** |
| **Integrity Report (Final)** | **Stage 4.5** | **Stage 5 (prerequisite)** | **Required** |
| Final Paper | Stage 5 | END (delivery) | Required |

---

## Exception State Handling

### Timeout

If a stage shows no progress for an extended period (e.g., Socratic mode exceeds 15 rounds without convergence):
1. state_tracker marks the stage as `stalled`
2. orchestrator provides options:
   - Switch mode (socratic -> full)
   - Narrow scope
   - Skip this stage (non-mandatory stages only)

### Missing Materials

If required materials are found missing during transition:
1. state_tracker reports the material gap
2. orchestrator suggests returning to the stage that produces that material
3. User can choose: backfill / skip (at own risk, but cannot skip integrity checks)

### Integrity Check FAIL Loop

If Stage 2.5 or 4.5 corrections exceed 3 rounds without passing:
1. List all unverifiable items
2. User decides:
   - Manually handle unverifiable items
   - Remove unverifiable citations
   - Continue to next stage (with "partially unverified" warning)

### Session Interruption

If the user leaves and returns:
1. orchestrator displays Progress Dashboard
2. Confirm whether to continue from breakpoint
3. Check if any outdated materials need refreshing

---

## Revision Loop Rules (v2.0)

### Simplified Revision Cycle

```
v2.0's revision cycle is simpler and more explicit than v1.0:

Stage 3 (First REVIEW)
  -> Decision: Accept -> Stage 4.5
  -> Decision: Minor/Major -> Stage 4
      -> Stage 4 (REVISE)
          -> Stage 3' (RE-REVIEW, verification)
              -> Decision: Accept/Minor -> Stage 4.5
              -> Decision: Major -> Stage 4' (last revision)
                  -> Stage 4.5 (go directly to final verification, no return to review)

Maximum 1 round of RE-REVISE, no infinite loops.
Unresolved issues -> Acknowledged Limitations.
```

### Differences from v1.0

| v1.0 | v2.0 |
|------|------|
| Max 2 review-revise cycles | Fixed 2 reviews (Stage 3 + Stage 3') + max 1 RE-REVISE |
| No integrity check | Mandatory Pre-review + Final integrity check |
| 4 reviewers | 5 reviewers (+Devil's Advocate) |
| Can skip any stage | Stage 2.5 and 4.5 cannot be skipped |
| No mandatory checkpoints | Every stage requires a checkpoint |

## Reset-boundary transitions (v3.6.3, flag-gated)

When `ARS_PASSPORT_RESET=1`, every FULL checkpoint carries an implicit state transition to a terminal `awaiting_resume` state. The next stage only starts when a new session posts `resume_from_passport=<hash>`.

Transition semantics:

```
Stage N [working]
  -> FULL checkpoint
    -> [flag OFF]  Stage N+1 [working]           (pre-v3.6.3 continuation)
    -> [flag ON]   append boundary entry -> awaiting_resume
         -> resume_from_passport=<hash>
              -> append resume entry (consumes_hash=<hash>)
              -> Stage N+1 [working]              (fresh session, passport-loaded)
```

Iron rules:

- `awaiting_resume` is not persisted in `state_tracker`; it is computed from the passport ledger. A `boundary` entry with hash `H` is awaiting resume iff no later `resume` entry in `reset_boundary[]` carries `consumes_hash == H`. Single pass over the ledger, no out-of-band state.
- `systematic-review` under flag ON cannot transition `Stage N → Stage N+1` without a fresh-session resume. In-session continuation is refused.
- Other modes under flag ON allow in-session continuation as a fallback, but the orchestrator must still load Stage N+1 input strictly from the passport (no replay of prior turns).
- SLIM checkpoints never enter `awaiting_resume`.
- MANDATORY checkpoints enter `awaiting_resume` when they are also FULL and flag is ON. Integrity gates remain MANDATORY; the reset does not downgrade them. The `### Resume Instruction` subsection emitted alongside `[PASSPORT-RESET: ...]` carries the passport file path and resume command — it does NOT carry the user decision prompt. The decision prompt happens on resume, after the fresh session loads the passport (see next rule).
- If a `boundary` entry carries `pending_decision`, `next` is advisory only. The user's branch choice happens AFTER `resume_from_passport=<hash>` in the fresh session, never in the reset checkpoint itself. The orchestrator re-prompts the user in the new session before transitioning to any `Stage N+1`. The `resume` entry records the chosen branch via `chosen_branch`. Actual routing comes from the matched option's `next_stage`/`next_mode`; `next` is a fallback default only.

See [`passport_as_reset_boundary.md`](passport_as_reset_boundary.md) for the full protocol.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-process-summary-protocol-md"></a>

## SOURCE: skills/academic-pipeline/references/process_summary_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=12420 -->
# Stage 6: Process Summary Protocol (Added in v2.4)

**Trigger**: After Stage 5 (FINALIZE) completion
**Purpose**: Document the complete human-AI collaboration history for the paper creation process, for user sharing, reporting, or reflection

## Workflow

```
1. Ask user language preference:
   "Which language version of the process record would you like to generate first?"
   - Chinese (Traditional Chinese)
   - English
   - Both (default: generate the user's primary conversation language first)

2. Review session history and compile the following:
   - User's initial instructions (verbatim quote)
   - Key decision points and user interventions at each stage
   - Direction correction moments and reasons
   - Iteration count and review result summaries
   - Intellectual insights raised by the user (e.g., questions that spawned new chapters)
   - Quality requirement evolution (e.g., formatting, tone adjustments)
   - Pipeline statistics (stage count, review rounds, integrity verification count, etc.)

3. Generate Markdown version (paper_creation_process.md / paper_creation_process_en.md)

4. Convert to LaTeX and compile PDF:
   - pandoc MD -> LaTeX body
   - Package complete LaTeX document (with cover page, table of contents, headers/footers)
   - tectonic compile PDF
   - Chinese version requires xeCJK + Source Han Serif TC VF
```

## Required Content in Process Record

| Section | Content |
|---------|---------|
| Paper Information | Title, final deliverables list |
| Stage-by-Stage Process | Input/output/key decisions for each stage, with verbatim user quotes |
| Iteration Details | Review comment summaries, revision items, re-review results |
| Interaction Pattern Summary | User role, Claude role, intervention count, key turning points — statistics table |
| User Key Decisions | Chronological list of every important decision made by the user |
| Key Lessons | Reusable lessons learned from the process |
| **Collaboration Quality Evaluation** | **Final chapter: 1-100 score + dimensional analysis + improvement suggestions** (see below) |

## Collaboration Quality Evaluation (Final Chapter, Mandatory)

The final chapter of the process record is a "Collaboration Quality Evaluation" that honestly and constructively assesses the user's performance in the human-AI collaboration. Format follows the Claude Code CLI `/insight` feature.

### Scoring Dimensions (each 1-100, weighted average for overall score)

```
+--------------------------------------------------+
|  Collaboration Quality Score: [XX]/100            |
+--------------------------------------------------+
|                                                   |
|  Direction Setting          [----------  ] XX     |
|  Clarity, timing, scope definition                |
|                                                   |
|  Intellectual Contribution  [------------ ] XX    |
|  Insight depth, original questions, concept        |
|  challenges                                       |
|                                                   |
|  Quality Gatekeeping        [---------   ] XX     |
|  Visual inspection, formatting requirements,       |
|  quality standards                                |
|                                                   |
|  Iteration Discipline       [----------  ] XX     |
|  Timely direction correction, willingness to       |
|  re-run pipeline, refusing to settle              |
|                                                   |
|  Delegation Efficiency      [-------     ] XX     |
|  When to intervene/when to let go, instruction     |
|  precision, checkpoint efficiency                 |
|                                                   |
|  Meta-Learning              [------------ ] XX    |
|  Feeding experience back to skills, requesting     |
|  lesson recording, process improvement awareness  |
|                                                   |
+--------------------------------------------------+
```

### Scoring Criteria

| Score Range | Meaning |
|------------|---------|
| 90-100 | Exceptional — User intervention significantly elevated the paper's intellectual quality beyond what AI could produce independently |
| 75-89 | Excellent — User made correct directional decisions and effectively leveraged the pipeline's iteration capabilities |
| 60-74 | Good — User completed necessary decisions but some opportunities were missed |
| 40-59 | Basic — User primarily served as a "continue" button with little substantive intervention |
| 1-39 | Needs Improvement — User intervention may have disrupted the workflow or lacked critical quality gatekeeping |

### Required Subsections

1. **Overall Score**: Total score + one-sentence evaluation
2. **What Worked Well**: 2-4 specific behaviors, with verbatim user quotes
3. **Missed Opportunities**: 1-3 things the user could have done but didn't
4. **Recommendations for Next Time**: 3-5 specific, actionable improvement suggestions
5. **Human vs AI Value-Add**: Clearly identify which aspects of the final paper quality came from user intervention (not achievable by AI independently)

### Evaluation Principles

- **Honesty first**: No inflation, no pleasantries. If the user only pressed "continue," reflect that truthfully
- **Evidence-based**: Every score is supported by specific behaviors or conversation records
- **Constructive**: Every criticism must include actionable improvement suggestions
- **Acknowledge uncertainty**: If certain dimensions cannot be evaluated (e.g., mid-entry skipped the research stage), mark as N/A
- **Bidirectional reflection**: Also candidly point out Claude's shortcomings during the process (e.g., areas requiring multiple corrections)

## AI Self-Reflection Report (Mandatory)

The second-to-last chapter of the process record is an "AI Self-Reflection Report" that honestly documents AI's own behavioral patterns during the pipeline. This complements the Collaboration Quality Evaluation (which assesses the user) by assessing the AI.

### Tracked Metrics

All metrics below are derived from existing agent logs (`[DA-DECISION]`, `[DA-REBUTTAL]`, `[HEALTH-CHECK]`, state tracker JSON) — no additional per-stage instrumentation is required. The orchestrator aggregates these at Stage 6 by scanning the dialogue transcript:

```
+--------------------------------------------------+
|  AI Self-Reflection Report                        |
+--------------------------------------------------+
|                                                   |
|  DA Concession Rate           X/Y (Z%)           |
|  (concessions / total rebuttals received)         |
|                                                   |
|  DA Consecutive Concessions   [list if any]       |
|  (violations of no-consecutive rule)              |
|                                                   |
|  Checkpoints Skipped          X/Y                 |
|  (SLIM or user-skipped / total checkpoints)       |
|                                                   |
|  User Overrides               X                   |
|  (times user overruled AI recommendation)         |
|                                                   |
|  Dialogue Health Alerts       X                   |
|  (health check interventions triggered)           |
|  - Persistent Agreement:      X                   |
|  - Conflict Avoidance:        X                   |
|  - Premature Convergence:     X                   |
|                                                   |
|  Intent Mode Transitions      X                   |
|  (exploratory ↔ goal-oriented switches)           |
|                                                   |
|  Cross-Model Disagreements    X (if enabled)      |
|  (integrity + DA combined)                        |
|                                                   |
+--------------------------------------------------+
```

### Required Subsections

1. **Behavioral Summary**: One paragraph describing the overall AI behavioral pattern during this pipeline run
2. **Sycophancy Risk Assessment**: Screening thresholds based on concession rate and health alerts — LOW (concession <50%, 0 health alerts) / MEDIUM (50-65% or 1-2 alerts) / HIGH (>65% or 3+ alerts). These are screening thresholds, not diagnostic criteria — a MEDIUM rating means the metrics warrant human review, not that sycophancy occurred (a high concession rate may reflect genuinely strong rebuttals). If HIGH, include a warning: "AI may have been too accommodating in this run. Human review of DA findings and integrity results is strongly recommended."
3. **Frame-Lock Incidents**: List any `[CROSS-MODEL-FINDING]` that the primary DA missed (if cross-model was enabled), or any frame-lock detections triggered during checkpoints. If none, state "No frame-lock incidents detected — note this could mean either good coverage or undetected frame-lock."
4. **Convergence Pattern**: In Socratic dialogue stages, was intent correctly detected? Did the mentor try to converge prematurely? Report mode transitions and any premature-convergence health alerts.
5. **What AI Got Wrong**: Candid list of AI errors or shortcomings during the run — corrections needed, checkpoint failures, integrity issues found. This is not a failure report; it is evidence that quality gates are working.
6. **Failure Mode Audit Log** (v3.2): For each of the 7 AI research failure modes from the Stage 2.5 / 4.5 checklist (see `references/ai_research_failure_modes.md`), report (a) final status at 4.5 — `CLEAR` / `OVERRIDDEN`, (b) history — was it ever `SUSPECTED` during the pipeline? At which stage? How was it resolved? (c) if `OVERRIDDEN`, the user's recorded reasoning. This makes the failure-mode defences part of the permanent process record. Modes with no history can be listed as `CLEAR (no flags)` in one line; expand only on modes that were flagged.
- **Reading Probe Outcomes (if present)** — transcribes the `### Reading Probe Outcomes` subsection from the Research Plan Summary verbatim, with a one-line note that the AI did not verify paraphrase accuracy. If the Research Plan Summary has no such subsection (i.e., `ARS_SOCRATIC_READING_PROBE` was unset), this item is omitted entirely (no "not applicable" noise). Pickup rule (two sources, either sufficient): (a) copy the entire `### Reading Probe Outcomes` subsection body verbatim — this is the authoritative human-readable record; (b) additionally grep for `[READING-PROBE: status=..., paper=..., outcome=..., turn=...]` which the Mentor emits once in the summary as a machine-stable anchor (including for `not_fired_*` statuses). If both are present use (a) as the display source and keep (b) as the final line of the transcribed block so downstream tooling can still parse it. If only raw inline tags from dialogue turns (`[READING-PROBE: paper=..., outcome=..., turn=...]` without the `status=` field) are found and no subsection exists, the Mentor compilation step was skipped — log this as a pipeline anomaly rather than silently dropping the probe data.

### Output Length Guidance

For dimensions with no findings, state the null result in one sentence. Expand only when issues are detected. The real risk is generating verbose "everything is fine" paragraphs for empty subsections — resist this.

### Principles

- **Self-honesty**: AI must not minimize its own shortcomings. If the DA conceded too easily, say so.
- **Not self-flagellation**: The purpose is transparency, not performative humility. Report facts with interpretation.
- **Actionable**: Every finding should suggest what could be done differently next time (e.g., "Consider enabling cross-model verification for the next run" or "The user might want to push back harder on DA concessions")
- **The irony is noted**: This self-reflection is itself produced by the same AI that may have been sycophantic during the pipeline. The user should read it with that awareness. This caveat must be stated in the report.

## Output Specifications

- **Filename**: `paper_creation_process.md` (Chinese) / `paper_creation_process_en.md` (English)
- **PDF**: `paper_creation_process_zh.pdf` / `paper_creation_process_en.pdf`
- **LaTeX template**: `article` class, 12pt, A4, Times New Roman + Source Han Serif TC VF
- **Includes table of contents**: `\tableofcontents`
- **Header**: left = document title (italic), right = date
- **Compilation**: tectonic (same toolchain as Stage 5)
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-progress-dashboard-template-md"></a>

## SOURCE: skills/academic-pipeline/references/progress_dashboard_template.md

<!-- SOURCE-CONTENT-BEGIN bytes=1524 -->
# Progress Dashboard

Users can say "status" or "pipeline status" at any time to view:

```
+=============================================+
|   Academic Pipeline Status                   |
+=============================================+
| Topic: Impact of AI on Higher Education     |
|        Quality Assurance                    |
+---------------------------------------------+

  Stage 1   RESEARCH          [v] Completed
  Stage 2   WRITE             [v] Completed
  Stage 2.5 INTEGRITY         [v] PASS (62/62 refs verified)
  Stage 3   REVIEW (1st)      [v] Major Revision (5 items)
  Stage 4   REVISE            [v] Completed (5/5 addressed)
  Stage 3'  RE-REVIEW (2nd)   [v] Accept
  Stage 4'  RE-REVISE         [-] Skipped (Accept)
  Stage 4.5 FINAL INTEGRITY   [..] In Progress
  Stage 5   FINALIZE          [ ] Pending
  Stage 6   PROCESS SUMMARY   [ ] Pending

+---------------------------------------------+
| Integrity Verification:                     |
|   Pre-review:  PASS (0 issues)              |
|   Final:       In progress...               |
| Compliance (v3.4.0):                        |
|   PRISMA-trAIce: pass (17/17)               |
|   RAISE principles: pass (4/4)              |
+---------------------------------------------+
| Review History:                             |
|   Round 1: Major Revision (5 required)      |
|   Round 2: Accept                           |
+=============================================+
```

See `templates/pipeline_status_template.md` for the output template.
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-reinforcement-content-md"></a>

## SOURCE: skills/academic-pipeline/references/reinforcement_content.md

<!-- SOURCE-CONTENT-BEGIN bytes=1338 -->
# Mid-Conversation Reinforcement Content

Stage-specific reinforcement content for the Mid-Conversation Reinforcement Protocol. At every stage transition, the orchestrator injects the relevant row from this table into the reinforcement template.

| Transition | Reinforcement Focus |
|-----------|-------------------|
| Stage 1→2 | IRON RULE: Every claim must have a citation. Anti-Pattern: Fabricated citations. |
| Stage 2→2.5 | IRON RULE: Gray zone = FAIL. Anti-Pattern: Treating "difficult to verify" as acceptable. |
| Stage 2.5→3 | IRON RULE: Reviewers are READ-ONLY. Anti-Pattern: Fabricating review comments. |
| Stage 3→4 | IRON RULE: Max 2 revision loops. Anti-Pattern: Sycophantic revision. |
| Stage 4→3' | IRON RULE: Each concern independently verified. Anti-Pattern: Rubber-stamp re-review. |
| Stage 3'→4' | IRON RULE: Max 2 revision loops. Anti-Pattern: Silently dropping reviewer concerns. |
| Stage 4/4'→4.5 | IRON RULE: Must PASS with zero issues. Anti-Pattern: Re-verifying only known issues. |
| Stage 4.5→5 | IRON RULE: PDF from LaTeX only. Anti-Pattern: Orchestrator doing substantive work. |
| Any FULL/SLIM checkpoint | IRON RULE: `collaboration_depth_agent` output is **advisory only** and never blocks progression. Anti-Pattern: treating the observer's Zone/scores as a gate or a leaderboard. |
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-score-trajectory-protocol-md"></a>

## SOURCE: skills/academic-pipeline/references/score_trajectory_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=3758 -->
# Score Trajectory Protocol

**Status**: v3.3
**Used by**: `pipeline_orchestrator_agent`, `editorial_synthesizer_agent`
**Applies at**: Stage 3' (RE-REVIEW) and Stage 4' (RE-REVISE)

---

## Purpose

Tracks how rubric scores change across revision rounds. Detects score regressions — dimensions where the revised paper scores lower than the original — which indicate that a revision fix inadvertently damaged another aspect of the paper.

Inspired by PaperOrchestra's Content Refinement Agent (Song et al., 2026), which accepts revisions only when overall score increases and reverts when any sub-axis shows net negative gain.

---

## How it works

### At Stage 3 (REVIEW)

The `editorial_synthesizer_agent` produces dimension scores in the Review Report (Schema 6). These are the **baseline scores**.

### At Stage 3' (RE-REVIEW)

The `editorial_synthesizer_agent` produces new dimension scores. The `pipeline_orchestrator_agent` computes deltas:

```
For each dimension d in {originality, methodological_rigor, evidence_sufficiency,
  argument_coherence, writing_quality, literature_integration, significance_impact, overall}:
  delta[d] = score_re_review[d] - score_review[d]

Note: Dimensions match the 7 universal review dimensions from
academic-paper-reviewer/references/review_criteria_framework.md plus overall.
```

### Decision rules

| Condition | Action |
|-----------|--------|
| All deltas >= 0 | Normal: revision improved or maintained all dimensions |
| Any delta < 0 but >= -3 | Warning: "Dimension X decreased slightly (delta = Y). Verify this is acceptable." Surface at checkpoint. |
| Any delta < -3 | **Regression detected**: "Dimension X regressed significantly (delta = Y). The revision may have damaged this aspect." Trigger MANDATORY checkpoint. |
| Overall delta < 3 AND no P0 issues | Early-stop eligible (existing v3.2 criterion). Suggest stopping revision loop. |

### Regression checkpoint

When regression is detected, the MANDATORY checkpoint presents:
1. The dimension(s) that regressed and by how much
2. The reviewer's comments on those dimensions (from the re-review report)
3. Three options:
   - **Proceed**: Accept the regression as a tradeoff (recorded in Stage 6 audit)
   - **Targeted fix**: Return to Stage 4' to fix only the regressed dimension(s)
   - **Revert**: Restore the pre-revision version for the regressed section(s)

---

## Integration with existing early-stopping

The v3.2 early-stopping criterion (delta < 3 + no P0) remains unchanged. Score trajectory extends it:
- Early-stopping checks the **overall** delta
- Trajectory tracking checks **per-dimension** deltas
- Both can fire at the same checkpoint: "Overall improvement is small (suggest stopping) AND dimension X regressed (suggest investigating)"

---

## Stage 6 reporting

The Process Summary includes a "Score Trajectory" subsection showing all rounds:

```markdown
### Score Trajectory

| Dimension | Review (Stage 3) | Re-Review (Stage 3') | Delta | Status |
|-----------|-------------------|----------------------|-------|--------|
| Originality | 3.5 | 3.8 | +0.3 | Improved |
| Methodological Rigor | 4.2 | 4.0 | -0.2 | Warning |
| Evidence Sufficiency | 3.0 | 3.8 | +0.8 | Improved |
| Argument Coherence | 2.8 | 3.5 | +0.7 | Improved |
| Writing Quality | 3.5 | 3.6 | +0.1 | Improved |
| Literature Integration | 3.8 | 4.0 | +0.2 | Improved |
| Significance & Impact | 3.0 | 3.2 | +0.2 | Improved |
| Overall | 3.4 | 3.7 | +0.3 | Improved |

Regressions detected: 1 (Methodological Rigor, -0.2, within tolerance)
Early-stop eligible: No (overall delta = 4 >= 3)
```

---

## References

- Song, Y. et al. (2026). PaperOrchestra. *arXiv:2604.05018*. — Section 4 Step 5 (Content Refinement Agent: score-driven accept/revert).
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-team-collaboration-protocol-md"></a>

## SOURCE: skills/academic-pipeline/references/team_collaboration_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=9127 -->
# Team Collaboration Protocol

## Purpose

Guidelines for coordinating multi-person academic research teams using the pipeline. Claude Code runs as a single-user session; this protocol documents the **human coordination layer** that wraps around pipeline executions.

---

## Role Definitions

| Role | Pipeline Stages | Responsibilities |
|------|----------------|-----------------|
| Research Lead | Stage 1 (RESEARCH) | Defines RQ, manages literature search, approves synthesis, sets theoretical framework |
| Lead Author | Stage 2 (WRITE), Stage 4/4' (REVISE) | Writes/revises paper, makes final content decisions, owns the manuscript |
| Methods Specialist | Stage 1 (methodology), Stage 2 (methods section) | Ensures methodological rigor, validates statistical analysis, reviews data integrity |
| Review Coordinator | Stage 3/3' (REVIEW) | Manages simulated review process, distributes feedback, facilitates revision coaching |
| Integration Lead | All stages | Ensures consistency across stages, manages handoffs, resolves cross-stage conflicts |

### Role Assignment Rules

- One person may hold multiple roles (common in small teams)
- Research Lead and Lead Author are the minimum required roles (can be the same person)
- Integration Lead is recommended for teams of 3+
- Methods Specialist is strongly recommended for empirical papers
- All role assignments should be documented at pipeline intake

---

## Handoff Protocol

For each stage transition, the following handoff procedure applies:

### Stage 1 -> Stage 2 (Research -> Write)

| Item | Detail |
|------|--------|
| **Who hands off** | Research Lead |
| **Who receives** | Lead Author |
| **Materials** | RQ Brief, Bibliography, Synthesis Report (conforming to Schemas 1-3 in `shared/handoff_schemas.md`) |
| **Approval needed** | Research Lead confirms synthesis is complete and RQ is finalized |
| **Handoff checklist** | All Material Passports (Schema 9) attached; Bibliography minimum source count met; Synthesis has 3+ themes |

### Stage 2 -> Stage 2.5 (Write -> Integrity)

| Item | Detail |
|------|--------|
| **Who hands off** | Lead Author |
| **Who receives** | Integration Lead (or Lead Author if no Integration Lead) |
| **Materials** | Paper Draft (conforming to Schema 4) |
| **Approval needed** | Lead Author confirms draft is ready for verification |
| **Handoff checklist** | All sections complete; reference list formatted; word count within target range |

### Stage 2.5 -> Stage 3 (Integrity -> Review)

| Item | Detail |
|------|--------|
| **Who hands off** | Integration Lead |
| **Who receives** | Review Coordinator |
| **Materials** | Verified Paper Draft + Integrity Report (Schema 5) |
| **Approval needed** | Integrity verdict is PASS; any PASS_WITH_CONDITIONS items acknowledged |
| **Handoff checklist** | Integrity Report attached; all SERIOUS/MEDIUM issues resolved |

### Stage 3 -> Stage 4 (Review -> Revise)

| Item | Detail |
|------|--------|
| **Who hands off** | Review Coordinator |
| **Who receives** | Lead Author + Methods Specialist (if methodology issues) |
| **Materials** | Review Report (Schema 6) + Revision Roadmap (Schema 7) |
| **Approval needed** | Review Coordinator confirms roadmap is complete; Lead Author reviews before starting |
| **Handoff checklist** | All revision items categorized and prioritized; coaching session completed (or skipped by Lead Author) |

### Stage 4 -> Stage 3' (Revise -> Re-Review)

| Item | Detail |
|------|--------|
| **Who hands off** | Lead Author |
| **Who receives** | Review Coordinator |
| **Materials** | Revised Draft + Response to Reviewers (Schema 8) |
| **Approval needed** | Lead Author confirms all addressable items are handled |
| **Handoff checklist** | Response to Reviewers covers every roadmap item; new references verified |

### Stage 4.5 -> Stage 5 (Final Integrity -> Finalize)

| Item | Detail |
|------|--------|
| **Who hands off** | Integration Lead |
| **Who receives** | Lead Author |
| **Materials** | Final Verified Draft + Final Integrity Report |
| **Approval needed** | Integrity verdict PASS with zero issues |
| **Handoff checklist** | All previous integrity issues confirmed resolved; Material Passport updated to VERIFIED |

---

## Version Control

### Git Branching Strategy

```
main
  |-- paper/draft-v1          (Stage 2 output)
  |-- paper/post-integrity-v1 (Stage 2.5 output)
  |-- paper/post-review-v1    (Stage 4 output)
  |-- paper/final-v1          (Stage 5 output)
```

### Tagging Convention

| Tag | When | Example |
|-----|------|---------|
| `v0.1-draft` | After Stage 2 completion | First complete draft |
| `v0.2-post-integrity` | After Stage 2.5 PASS | Draft verified for integrity |
| `v0.3-post-review` | After Stage 4 completion | First revision complete |
| `v0.4-post-rereview` | After Stage 4' completion (if applicable) | Second revision complete |
| `v1.0-final` | After Stage 5 completion | Final manuscript |

### Rules

- Never overwrite; always create a new version
- All versions are preserved for audit trail
- Version labels must match the Material Passport `version_label` field (Schema 9 in `shared/handoff_schemas.md`)
- Each team member's changes should be attributable (use git author info)

---

## Conflict Resolution

| Conflict Type | Resolution Authority | Escalation Path |
|--------------|---------------------|-----------------|
| Content disagreements | Lead Author has final say | If unresolved: Research Lead mediates |
| Methodological disagreements | Methods Specialist has final say | If unresolved: cite literature precedent |
| Scope disagreements | Research Lead has final say | If unresolved: team vote |
| Formatting/style disagreements | Lead Author has final say | Follow target journal guidelines |
| Integrity findings disagreements | Integration Lead has final say | Cannot override SERIOUS findings |

### Disagreement Documentation

All disagreements must be documented in the revision tracking:

```markdown
## Disagreement Record

**Date**: [date]
**Stage**: [stage]
**Parties**: [who disagreed]
**Issue**: [what the disagreement was about]
**Resolution**: [how it was resolved]
**Authority**: [who made the final call]
**Rationale**: [why this decision was made]
```

---

## Communication Templates

### 1. Handoff Notification

```markdown
## Handoff: Stage [X] -> Stage [Y]

**From**: [Role] ([Name])
**To**: [Role] ([Name])
**Date**: [date]

**Materials Delivered**:
- [Material 1] (version: [version_label])
- [Material 2] (version: [version_label])

**Status Summary**:
[1-2 sentence summary of what was accomplished and any open items]

**Action Required**:
[What the receiving person needs to do next]

**Deadline**: [if applicable]
```

### 2. Review Request

```markdown
## Review Request: [Paper Title]

**From**: [Review Coordinator]
**To**: [Team / External Reviewer]
**Date**: [date]

**Paper Version**: [version_label]
**Word Count**: [N]
**Review Type**: [Internal simulated / External journal / Team peer review]

**Focus Areas**:
1. [specific area to focus on]
2. [specific area to focus on]

**Deadline**: [date]
**Return Format**: [Use Schema 6 format from shared/handoff_schemas.md]
```

### 3. Revision Assignment

```markdown
## Revision Assignment: [Paper Title]

**From**: [Review Coordinator]
**To**: [Lead Author / Methods Specialist]
**Date**: [date]

**Revision Round**: [N]
**Total Items**: [N] (must_fix: [N], should_fix: [N], consider: [N])

**Your Assignments**:
- [REV-001]: [brief description] — assigned to [name]
- [REV-003]: [brief description] — assigned to [name]

**Deadline**: [date]
**Coordination Notes**: [any dependencies between revision items]
```

---

## Workflow for Teams

### Small Team (2-3 people)

```
Person A (Research Lead + Lead Author):
  - Runs Stage 1 (RESEARCH) with their Claude session
  - Runs Stage 2 (WRITE) with their Claude session
  - Receives revision items, runs Stage 4/4'
  - Runs Stage 5 (FINALIZE)

Person B (Methods Specialist + Review Coordinator):
  - Reviews Stage 1 methodology output
  - Reviews Stage 2 methods section
  - Manages Stage 3/3' review process
  - Handles specific methodology revision items

Handoff: via shared folder or git repo
Materials: conform to schemas in shared/handoff_schemas.md
```

### Large Team (4+ people)

```
Add Integration Lead role:
  - Monitors all stage transitions
  - Validates handoff completeness
  - Resolves cross-stage inconsistencies
  - Maintains pipeline state document (shared with all team members)
```

---

## Limitations

- Claude Code runs as a single-user session; this protocol documents the HUMAN coordination layer
- Each team member runs their own pipeline stages independently in separate Claude sessions
- Handoff materials (conforming to schemas in `shared/handoff_schemas.md`) ensure consistency across sessions
- Real-time co-editing is not supported; use git or shared documents for synchronization
- Pipeline state tracking is per-session; the Integration Lead must manually synchronize state across sessions
- The pipeline does not enforce team role permissions; discipline is maintained by convention
<!-- SOURCE-CONTENT-END -->

<a id="source-skills-academic-pipeline-references-adapters-overview-md"></a>

## SOURCE: skills/academic-pipeline/references/adapters/overview.md

<!-- SOURCE-CONTENT-BEGIN bytes=9713 -->
# Adapter Contract — Producing `literature_corpus[]` Entries

**Status**: Stable as of ARS v3.6.4
**Applies to**: any adapter that produces a Material Passport `literature_corpus[]` field
**Authoritative schemas**:
- [`shared/contracts/passport/literature_corpus_entry.schema.json`](../../../shared/contracts/passport/literature_corpus_entry.schema.json)
- [`shared/contracts/passport/rejection_log.schema.json`](../../../shared/contracts/passport/rejection_log.schema.json)

## 1. What an adapter is

An **adapter** is a program (in any language) that reads a user-owned corpus source — a Zotero export, an Obsidian vault, a folder of PDFs, a Notion database, a custom SQLite library — and produces:

1. **`passport.yaml`** with a top-level `literature_corpus` array conforming to `literature_corpus_entry.schema.json`.
2. **`rejection_log.yaml`** conforming to `rejection_log.schema.json`, always emitted (empty when no rejections).

ARS provides three Python reference adapters in [`scripts/adapters/`](../../../scripts/adapters/). Users are expected to write their own adapters for non-reference sources. The three reference adapters are starting points, not production tools.

## 2. Why a contract, not a plugin API

ARS deliberately does NOT run adapter code itself. The adapter runs in the user's environment, reads the user's data, and emits YAML files. ARS reads those YAML files. Rationale:

- Each corpus source (Zotero, Obsidian, custom) has its own versioning, auth, and data quirks. Pinning one plugin API would force ARS to track all of them.
- Keeping the boundary at "YAML files on disk" means a user can use any language, any scheduling mechanism, and any privacy posture without touching ARS internals.
- ARS remains a writing/review-layer tool; corpus integration stays in user-owned code.

## 3. Entry field reference

Refer to the [`literature_corpus_entry` schema](../../../shared/contracts/passport/literature_corpus_entry.schema.json) for the authoritative contract. The field tables below are generated from that schema and must not drift.

<!-- GENERATED:LITERATURE_CORPUS_REQUIRED:START -->
| Field | Type | Description (first sentence) |
|---|---|---|
| `authors` | array | CSL-JSON name format. |
| `citation_key` | string | Stable unique identifier for this entry within the passport. |
| `source_pointer` | string | Stable URI locating this work in the user's own KB. |
| `title` | string | — |
| `year` | integer | Publication year. |
<!-- GENERATED:LITERATURE_CORPUS_REQUIRED:END -->

<!-- GENERATED:LITERATURE_CORPUS_OPTIONAL:START -->
| Field | Type | Description (first sentence) |
|---|---|---|
| `abstract` | string | PRIVATE FIELD. |
| `adapter_name` | string | Optional. |
| `adapter_version` | string | — |
| `contamination_signals` | object | v3.7.3 + v3.9.0 contaminated-source advisory field (spec v3.7.3 §3.2 + v3.9.0 §3.4–§3.5). |
| `contamination_signals_backfilled_at` | string | v3.7.3 backfill provenance (issue #105). |
| `description_last_audit` | null \| string | v3.7.1 trust-chain field. |
| `description_source` | string | v3.7.1 trust-chain field. |
| `doi` | string | DOI without leading 'doi:' or URL prefix. |
| `obtained_at` | string | Strongly recommended. |
| `obtained_via` | string | Strongly recommended. |
| `source_acquired` | boolean | v3.7.1 trust-chain field (spec § 3.1, D1). |
| `source_acquisition_date` | string | v3.7.1 trust-chain field. |
| `source_acquisition_path` | string | v3.7.1 trust-chain field. |
| `source_verification_method` | string | v3.7.1 trust-chain field. |
| `source_verified_against_original` | boolean | v3.7.1 trust-chain field. |
| `tags` | array | User-assigned tags from the source KB. |
| `user_notes` | string | PRIVATE FIELD. |
| `venue` | string | — |
<!-- GENERATED:LITERATURE_CORPUS_OPTIONAL:END -->

### 3.1 `authors` format (CSL-JSON names)

Each entry in `authors[]` is one of:

- **Personal name**: `{family: "Chen", given: "Cindy"}`. `family` is required; `given` and CSL particles (`suffix`, `dropping-particle`, `non-dropping-particle`, `comma-suffix`, `static-ordering`, `parse-names`) are optional.
- **Institution / corporate name**: `{literal: "World Health Organization"}`. `literal` is required; no other fields.

Adapters SHOULD preserve the upstream distinction (personal vs. institution). See [CSL-JSON name spec](https://docs.citationstyles.org/en/stable/specification.html#names) for edge cases.

### 3.2 Privacy caveat for `abstract` and `user_notes`

Publishers typically retain rights to abstracts; user notes often quote copyrighted material. The schema marks these fields as PRIVATE and does NOT enforce anything at the CI level. **If you publish a passport (e.g., commit it to a public repo or share it on the web), you are responsible for removing or clearing these fields.** ARS consumers treat both fields as optional; omitting them never causes failure.

## 4. Rejection log

Whenever an adapter cannot produce a valid `literature_corpus_entry` for an input item, it MUST push a rejection into `rejection_log.yaml.rejected[]` and MUST NOT silently drop the item.

The `reason` field uses a closed enum of categorical values:

| `reason` | When |
|----------|------|
| `missing_required_field` | One or more required fields (citation_key / title / authors / year / source_pointer) cannot be derived. Adapter SHOULD also populate `missing_fields`. |
| `invalid_field_format` | A field is present but fails schema format (e.g., DOI pattern mismatch). |
| `duplicate_citation_key` | Another entry already used this citekey and the adapter cannot disambiguate. |
| `unresolvable_source_pointer` | The source URI points to something that does not exist. Adapters typically do not check this; use only if the adapter actually tries to resolve. |
| `year_unparseable` | Year cannot be extracted from the source field ("n.d.", "forthcoming", "Spring 2024"). |
| `authors_unparseable` | Authors field is empty, contains only non-author creators, or has unparseable content. |
| `adapter_error` | Adapter-internal bug, not an input data problem. Use sparingly. |
| `other` | Anything else. When `reason=other`, `detail` is REQUIRED. |

The `raw` field, when present, MUST be either an object (structured input) or a string (filename or text line). Arrays, numbers, booleans, and null are disallowed so downstream viewers can assume printable shapes.

## 5. Error handling (fail-soft)

**Entry-level problems** → push to rejection log, continue.
**Adapter-level problems** (input file missing, unreadable, malformed at the root) → write nothing, print a clear error to stderr, exit with code 1.

Do NOT emit a partial passport. Either the passport represents a complete scan of the user's input, or the adapter failed loudly.

## 6. Determinism

Running an adapter twice on identical input MUST produce byte-identical output except for:

- `generated_at` in the rejection log
- `obtained_at` on each entry

Achieve this by:

- Sorting `literature_corpus[]` by `citation_key`
- Sorting `rejection_log.rejected[]` by `source`
- Serializing YAML with sorted keys

## 7. Provenance

Each `literature_corpus` entry SHOULD carry `obtained_via` and `obtained_at`. The `rejection_log` MUST carry `adapter_name`, `adapter_version`, and `generated_at`. These fields let downstream users trace which adapter version produced which entry — useful when a library's schema or a source KB layout changes.

## 8. Extension points for user-written adapters

Custom adapters are welcome and expected. Recommended conventions:

- Set `obtained_via: "other"` on each entry, and set `adapter_name` to a clear string (e.g., `"notion-adapter-v1"`, `"my-custom-sqlite-reader"`).
- Set `adapter_version` to a semver-ish string so downstream tools can diagnose output changes.
- Follow the same CLI shape as the three reference adapters (`--input`, `--passport`, `--rejection-log`) if you want to slot into similar tooling.

Common user-written adapter families include:

- **Zotero Web API**: one that calls `api.zotero.org` with a user API token. Not shipped with ARS by design (auth and rate-limit management would pull ARS into data-layer territory).
- **Notion / Readwise / Airtable**: each has its own SDK; the adapter's job is only to map the source's book/article objects into `literature_corpus_entry` shape.
- **Cross-source merger**: reads multiple sources and emits a combined passport. Handle citekey collisions explicitly.

## 9. Testing your adapter

Before committing passport output to any workflow:

1. Validate against the schema: `python scripts/check_literature_corpus_schema.py --passport <your_passport.yaml> --rejection-log <your_rejection_log.yaml>`.
2. Run your adapter twice on the same input and diff the outputs (after stripping `generated_at` / `obtained_at`). Any non-timestamp difference is a determinism bug.
3. Feed a known-bad entry to confirm it lands in the rejection log rather than silently vanishing or crashing.

The three reference adapters have pytest coverage under `scripts/adapters/tests/` — copying that pattern for your own adapter is a good starting point.

## 10. Relationship to other ARS artifacts

- [`shared/handoff_schemas.md`](../../../shared/handoff_schemas.md) Schema 9: the `literature_corpus[]` field lives inside the Material Passport.
- [`academic-pipeline/references/passport_as_reset_boundary.md`](../passport_as_reset_boundary.md): `literature_corpus[]` is consumed across reset boundaries like any other passport field.
- ARS agents that consume `literature_corpus[]` are **deferred** to v3.6.5+. As of v3.6.4, the field is a defined input port with no runtime consumer; adapters produce it, future ARS versions read it.
<!-- SOURCE-CONTENT-END -->
