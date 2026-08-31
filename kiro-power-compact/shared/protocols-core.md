<a id="source-shared-artifact-reproducibility-pattern-md"></a>

## SOURCE: shared/artifact_reproducibility_pattern.md

<!-- SOURCE-CONTENT-BEGIN bytes=8921 -->
# Artifact Reproducibility Pattern (v3.3.5+)

## Why this exists

ARS produces research artifacts — draft papers, literature reviews, review reports. A year
from now, you may want to reproduce one. Today's Material Passport (Schema 9) captures WHO
produced the artifact and WHEN, but not WITH WHAT. Which LLM? Which ARS version? Which
skill files? Which session materials?

The `repro_lock` sub-block fills that gap.

When the Anthropic automated-w2s-researcher paper (2026) claimed "2 researchers × 7 days
vs 9 agents × 5 days," readers had no way to audit the conditions. This pattern ensures
that ARS-produced artifacts carry their configuration on record — not as a replay mechanism,
but as an honest documentation trail.

## What this pattern IS NOT (read this first)

This is non-negotiable. Every future user MUST read this section before assuming the lock
guarantees anything it does not.

1. **LLM outputs are not byte-reproducible even at temperature 0.** Model providers update
   weights without changing the model id. `model.weight_stable: false` acknowledges this
   explicitly. `model.id` is an identifier, not a weight hash.

2. **Live external API queries are recorded as protocol versions, not snapshots.** The S2
   API changes daily. A paper citing DOI 10.1000/x today may return different metadata
   tomorrow. `s2_api_protocol_version` records which VERSION of our query logic ran, not
   a snapshot of the response.

3. **Mid-skill prompt mutations are not captured.** `prompts.hash_timing: "skill-load"` is
   a declaration: hashes are taken when the skill loads, not per agent call. Late injection
   of user-provided reference files, conditional branches, and dynamic prompt modifications
   are NOT reflected in the hash. This is a known imprecision.

4. **`stochasticity_declaration` is required, not optional.** Omitting it makes the lock
   dishonest by implication. Every generated passport includes the declaration verbatim.

If you want deterministic replay, you are reading the wrong pattern. This pattern gives
you CONFIGURATION DOCUMENTATION sufficient to INVESTIGATE divergence — not to PREVENT it.

## The block at a glance

```yaml
repro_lock:
  schema_version: "1.0"                    # lock schema version
  stochasticity_declaration: "LLM outputs are not byte-reproducible. This lockfile documents configuration, not a deterministic replay guarantee."
  ars_version: "3.3.5"                     # suite version at run time

  model:
    family: claude                          # provider family
    id: claude-opus-4-7                    # model identifier (not weight hash)
    weight_stable: false                    # always false until signed attestation exists

  prompts:
    hash_timing: skill-load                 # when hashes were taken
    skill_md_hash: "sha256:..."            # hash of the skill SKILL.md file
    agents_bundle_hash: "sha256:..."       # hash of agent prompt bundle

  materials:
    list_hash: "sha256:..."                # hash of [{filename, sha256}, ...] manifest
    count: 8                               # number of session materials

  external_protocols:
    s2_api_protocol_version: "3.3"         # S2 query protocol version
    s2_snapshot_available: false           # whether a response cache exists

  cross_model:
    enabled: false                         # whether cross-model verification ran
    secondary_model_id: null               # secondary model id if enabled
```

The block lives as an optional child of the Material Passport (Schema 9 in
`shared/handoff_schemas.md`). A missing key fails the lint. A null value passes with a
warning. A populated block with all required sub-fields passes silently.

## Field-by-field rationale

### schema_version

`"1.0"` currently supported. Schema evolution policy: breaking changes bump major,
additions bump minor. Old readers fail loudly on unknown versions — `check_repro_lock.py`
will exit 1 if it encounters an unrecognized version, forcing the user to upgrade their
tooling or audit the change manually.

### ars_version

Suite version from CHANGELOG. This couples the prompt hashes to the release: changing
`ars_version` will change the bundle hash even if individual prompt files didn't change.
That coupling is intentional — version boundaries mark coordinated changes.

### model.weight_stable

Currently always `false`. Reserved for a future world where a provider guarantees weight
stability with a signed attestation. Not today. If you see `true`, treat it as suspicious
until a signed attestation mechanism exists.

### prompts.hash_timing

Fixed at `"skill-load"` in v1.0. A future `"per-call"` variant would require runtime
instrumentation not present today. The spec is left open for future work. For now, the
hash captures the state of files at skill initialization, not at every agent invocation.

### materials.list_hash

Hash of a sorted manifest: `[{filename, sha256}, ...]` sorted by filename. If the user
edits a session material between runs, the hash changes — which is the correct behavior.
An identical hash across two runs means the input materials were identical; different
hashes mean inputs diverged.

### external_protocols.s2_snapshot_available

Almost always `false` today. If a future version of the pipeline caches S2 responses per
run and stores them alongside the passport, this flag flips to `true` and the snapshot path
appears in the passport. Until that exists, S2 responses are live queries and are not
reproducible.

## How it composes with existing infrastructure

- Material Passport (Schema 9) is the PARENT document. `repro_lock` is an OPTIONAL CHILD
  field. A passport without `repro_lock` fails the v3.3.5+ lint; a passport with
  `repro_lock: null` passes with a warning (explicit opt-out).
- Existing passports with `repro_lock` absent fail the new lint. Existing passports with
  `repro_lock: null` pass with a warning. Populated blocks pass silently.
- The integrity gate (Stage 2.5, Stage 4.5 in the academic pipeline) does NOT read
  `repro_lock`. The lock is for post-hoc reproducibility investigation, not runtime
  validation. Adding it does not change pipeline behavior.
- `check_repro_lock.py` can be run standalone on any passport file. It is not wired into
  the CI lint suite by default — it validates on-demand against specific passport files.

## Red flags when reading a populated repro_lock

- `model.weight_stable: true` — this value is not implemented yet; if you see it, the
  passport author is claiming something the infrastructure cannot verify. Treat as
  suspicious until a signed attestation mechanism exists.
- `prompts.hash_timing` anything other than `"skill-load"` — this is an unknown variant
  that the current tooling does not understand. The lint will not flag it as invalid, but
  the semantics are undefined.
- Empty or stub hashes (`"sha256:"` prefix with no content, or a short placeholder string
  like `"sha256:abc123"`) — the generator was broken or the author filled in a placeholder.
  Hashes should be 64-character hex strings for SHA-256.
- `stochasticity_declaration` modified from the verbatim required string — the author is
  signalling they believe the lock is stronger than it is. Read the entire passport twice
  before trusting any claims about reproducibility.

## How to generate a lock (for agent authors)

At skill-load time, compute `skill_md_hash` over the SKILL.md content and
`agents_bundle_hash` over the concatenated agent prompts (canonical ordering). Build the
materials manifest by listing session files with their SHA-256 digests, sort by filename,
then hash the JSON serialization. Write the block to the passport before handing off to
downstream stages. The `stochasticity_declaration` must be included verbatim — do not
paraphrase or abbreviate it.

## Honesty red line (restate)

This pattern enables HONEST DOCUMENTATION. It does not enable REPLAY. Every field has a
reason and a limitation. Users who treat the lock as a replay guarantee will be burned.
Authors who publish passports without `stochasticity_declaration` are failing their readers.
The locked configuration tells you what ran; it cannot tell you what would run again.

The distinction matters: documentation lets a third party investigate what happened and
ask whether divergence is expected or alarming. Replay would require weight-frozen models,
deterministic schedulers, and cached external data — none of which ARS controls today.

## Future evolution

- v1.1: add `cache_snapshot_available: true` support once the pipeline caches S2 responses.
  The snapshot path would appear as a sibling field in `external_protocols`.
- v2.0: if weight-signed attestations exist, `model.weight_stable: true` becomes meaningful.
  Until then the field is reserved.
- Never: byte-level replay guarantees. LLMs don't work like that; no schema version will
  change that fact.
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-benchmark-report-pattern-md"></a>

## SOURCE: shared/benchmark_report_pattern.md

<!-- SOURCE-CONTENT-BEGIN bytes=8988 -->
# Benchmark Report Pattern (v3.3.5+)

**Status**: v3.3.5 — hub doc for benchmark disclosure schema  
**Schema**: `shared/benchmark_report.schema.json`  
**Validator**: `scripts/check_benchmark_report.py`  
**Template**: `examples/benchmark_report_template.json`

---

## Why this exists

The Anthropic automated-w2s-researcher (2026) paper headlined a performance comparison:
"2 researchers × 7 days (PGR=0.23) vs 9 agents × 5 days (PGR=0.97)."

Dramatic. Also: n=2, author-conducted, no independence, self-scored. Not a scientific
comparison — a presentation artifact. The authors knew what the agent would produce before
sitting down to do the human baseline; their "7 days" is implicitly benchmarked against
their own foreknowledge. Unaware external researchers doing the same task cold would
likely score higher. The gap may partly be a sandbagged human baseline.

ARS inherits this risk the moment a user publishes an "ARS beats manual" claim. This
pattern defines a mandatory schema for anyone publishing an ARS benchmark comparison.
Reports that don't satisfy the schema aren't "ARS benchmarks" — they're anecdotes.

---

## The schema at a glance

Six required top-level fields in `benchmark_report.schema.json`:

- **`ars_version`** — exact semver the benchmark ran against; ties results to a specific
  skill version so readers can check whether that version is still current.
- **`task_definition`** — description, task_type (outcome-gradable or open-ended), and
  outcome_gradable flag; distinguishes rubric-scored tasks from genuinely open-ended ones.
- **`human_baseline`** — the five provenance fields that determine whether the human side
  of the comparison is credible (see field-by-field rationale below).
- **`ars_run`** — cost, time, skills used, and declared data access level; lets readers
  check the "agents are cheap" or "agents are fast" claims against concrete numbers.
- **`metrics`** — primary metric name, numeric value, and scoring independence; forces
  explicit disclosure of who scored the outputs.
- **`caveats`** — non-empty array of known limitations; at least one honest statement is
  required by schema enforcement.

---

## Field-by-field rationale

### `human_baseline`

This block exists because the human side of a comparison is where benchmark credibility
lives or dies. A weak human baseline inflates an agent's apparent advantage.

- **`sample_size`** (integer, minimum 1): Schema rejects zero, forces an explicit number.
  n=1 or n=2 get a validator warning rather than a hard failure — some tasks are
  expert-bounded — but the number must be stated. Silence is worse than admitting n=1.

- **`author_independence`** (enum: author-conducted | author-blinded | third-party-conducted):
  `author-conducted` is the "2 authors did it themselves" trap: allowed, but the schema
  flags the downward-bias risk. Authors know what a good ARS output looks like; their
  human effort is calibrated against that prior. `author-blinded` (authors worked without
  seeing ARS outputs first) is better. `third-party-conducted` eliminates experimenter
  bias entirely.

- **`hours_spent`** (number, minimum 0): Lets third parties sanity-check the time claim.
  "7 days" reads differently against 20 papers versus 400.

- **`recruitment`** (non-empty string): One sentence forces self-description of selection
  bias. "Authors," "hired on Upwork," "convenience sample" are all honest. Blank is not
  permitted.

- **`tools_allowed`** (array of strings): "No tools" vs "ChatGPT allowed" is not the same
  comparison as ARS. If the human baseline used no AI assistance while ARS ran full
  pipeline, the comparison is testing infrastructure access, not cognitive quality.

### `ars_run`

- **`cost_usd`** (number, minimum 0): A run costing $500 in API tokens is not "cheap"
  just because it took 3 hours. Hours and cost together are needed for a fair comparison.

- **`data_access_level_declared`** (enum: raw | redacted | verified_only): If ARS ran
  on `raw` data while the human baseline used redacted data, the benchmark is testing
  data privilege, not skill. Cross-references ground-truth isolation from v3.3.2.

- **`skills_used`** (array, minItems 1): A benchmark running `academic-pipeline`
  full-mode is not comparable to one running only `deep-research`. Both are ARS;
  they're different scope claims.

### `metrics.scoring_independence`

Four enum values: `authors-scored`, `third-party-scored`, `blind-scored`, `self-scored`.

`self-scored` parses and exits 0, but the validator emits a warning to stderr. Self-scoring
is the worst-case alignment failure: the same agents that produced the output are being
asked whether the output is good. `blind-scored` (human raters without knowledge of which
output came from ARS versus human baseline) is the minimum credible standard for any
claim that will be shared publicly.

### `caveats`

Non-empty array, items non-empty strings, minItems 1. The schema physically prevents an
empty caveats field. A benchmark report with no caveats either has no known limitations
(implausible for any real-world evaluation) or the author didn't think about limitations
(which disqualifies the report more than any specific limitation would).

The caveats field is where sample size warnings, scorer bias, task-selection bias, and
tool-access asymmetries should land when they don't rise to schema errors. It is the
honest disclosure box.

---

## How to use

1. Copy `examples/benchmark_report_template.json` to your benchmark directory.
2. Fill every `FILL IN:` field with real values.
3. Set `human_baseline.sample_size` to the actual number (schema rejects 0).
4. Run: `python scripts/check_benchmark_report.py your-report.json`
5. Fix all `ERROR:` lines (schema violations, exit 1).
6. Read the `WARNING:` lines (stderr, exit 0). Either address them in your methodology or
   document them explicitly in the `caveats` array.
7. Publish the JSON file in your repository alongside the benchmark write-up. The
   machine-readable format lets future scripts cross-check version-specific claims.

---

## What this pattern is NOT

- **Not a quality gate for your methodology.** A report can be schema-valid and still be
  methodologically weak. The schema forces disclosure; it does not evaluate task choice,
  rubric validity, or baseline skill. Compliance is necessary but not sufficient.

- **Not a way to launder self-scored or n=2 comparisons.** `self-scored` and
  `sample_size: 2` produce a valid document. The warnings are loud. Schema compliance
  means the claim is honest about its weaknesses — not that the claim is strong.

- **Not a substitute for peer review.** The schema is the minimum bar for internal
  credibility. Peer review catches confounded variables, cherry-picked tasks, post-hoc
  metric selection — problems the schema cannot see.

- **Not frozen.** A benchmark declaring `ars_version: 3.3.5` is always checked against
  the v3.3.5 schema. Future versions may add fields without invalidating existing reports.

---

## Honesty red lines

These are behaviors the schema is specifically designed to make visible. They are not
prohibited — the schema accepts all of them — but they will appear in validator output
or be apparent to any reader of the JSON.

- **Omitting sample size.** The field is required. There is no valid ARS benchmark report
  without a stated `human_baseline.sample_size`. n=1 is worse than n=10, but it is
  infinitely better than unstated.

- **Author-conducted with no caveat disclosure.** Using `author-conducted` is allowed.
  Not noting it in `caveats` as a limitation is an editorial failure, not a schema
  failure — but reviewers will notice.

- **Self-scoring with no warning acknowledgment.** `self-scored` produces a warning on
  every validator run. If you publish a report with `self-scored` and don't address it
  in caveats, the omission is visible in the JSON to anyone who checks.

- **Empty or single-word caveats.** The schema requires `minLength: 1` per item and
  `minItems: 1` for the array. A caveat of `"none"` is technically valid but signals
  that the author did not engage seriously with limitations.

- **Claiming ARS advantage without disclosing cost_usd.** The field is required. A claim
  that "ARS completed this in 4 hours vs 40 human hours" without a dollar figure omits
  the dimension where the trade-off may be reversed.

---

## Future evolution

Per-skill benchmark templates (a `deep-research`-specific template, an
`academic-paper-reviewer`-specific template) are likely as v3.4 adds domain-specific
evaluation protocols. The `cost_usd` field may split into `cost_usd_api` and
`cost_usd_compute` once cloud execution costs become a factor. The
`data_access_level_declared` enum may expand to match the v3.4 ground-truth tier
vocabulary if that spec evolves. None of these changes will break existing v3.3.5
reports, which remain valid against the version they declared in `ars_version`.
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-collaboration-depth-rubric-md"></a>

## SOURCE: shared/collaboration_depth_rubric.md

<!-- SOURCE-CONTENT-BEGIN bytes=10810 -->
---
rubric_version: "1.0"
paper_citation: "Wang, S., & Zhang, H. (2026). Pedagogical partnerships with generative AI in higher education: how dual cognitive pathways paradoxically enable transformative learning. International Journal of Educational Technology in Higher Education, 23:11. DOI: 10.1186/s41239-026-00585-x"
license: CC-BY-NC 4.0
---

# Collaboration Depth Rubric

**Status**: v1.0 (introduced ARS v3.5, 2026-04-21)
**Source**: Wang, S., & Zhang, H. (2026). *IJETHE* 23:11. DOI [10.1186/s41239-026-00585-x](https://doi.org/10.1186/s41239-026-00585-x). Open Access, CC BY 4.0.
**Canonical location**: `shared/collaboration_depth_rubric.md` in `Imbad0202/academic-research-skills`. External consumers should reference by stable URL; do not vendor (bump the `rubric_version` field on any modification).

---

## Why this rubric exists

Wang & Zhang (2026) empirically show that student-GenAI collaboration on pedagogical partnership terms simultaneously activates two cognitive pathways — **vigilance** (critical evaluation of AI output) and **offloading** (strategic delegation of cognitive work) — and that **both** independently predict transformative learning. Counterintuitively, cognitive offloading is **positively** associated with deep learning (β = 0.333, p < 0.001), with U-shaped dynamics: shallow scattered use (Zone 2) produces worse outcomes than no AI use (Zone 1); substantial committed delegation (Zone 3) unlocks higher-order reflection (β-quadratic = 0.102, p < 0.001).

This rubric operationalizes their framework as a post-hoc observer signal for Claude Code agents. It is used by `academic-pipeline/agents/collaboration_depth_agent.md` to score dialogue logs and produce **advisory, non-blocking** feedback to the user on how their collaboration pattern is shaping learning depth.

The rubric is **descriptive, not prescriptive**. It does not gate user progression. It does not celebrate high scores. It does not suggest low scores are failures. Its purpose is to make collaboration mode visible, so the user can decide whether to change it.

---

## The four dimensions

### Delegation Intensity

**Paper construct**: Cognitive Offloading (CO). 6-item Likert scale; sample items: *"I delegate complex problem-solving tasks to generative AI"*, *"I transfer cognitive effort to generative AI to reduce mental workload"* (Wang & Zhang 2026, Table 1).

**What to score for**: whole-category handoffs versus scattered micro-asks. Count committed delegation of task *categories* (e.g., "AI, draft the entire literature review" or "AI, do the outline"), not individual prompts. Zone 2's "fixing sentences, checking facts, tidying paragraphs" pattern is **low** intensity even if prompt count is high.

**High-intensity signals**:
- User assigns a whole subtask to the agent and moves on (e.g., "draft literature review", "build argument skeleton", "generate first outline")
- User articulates a division-of-labor plan at intake
- User says "you handle X while I focus on Y"

**Low-intensity signals**:
- Many small single-prompt interactions, each touching a fragment
- No task-level commitment language; user holds full cognitive load and just nudges output
- User edits AI micro-outputs line-by-line rather than regenerating at task level

**Empirical anchor**: U-shape (β-quadratic = 0.102, p < 0.001). Low-to-moderate offloading has minimal learning impact; only above threshold does offloading accelerate transformative learning.

---

### Cognitive Vigilance

**Paper construct**: Cognitive Vigilance (CV). 6-item Likert scale; sample items: *"I critically evaluate the accuracy of AI-generated content"*, *"I verify AI-generated information through independent sources"*, *"I scrutinize AI outputs for potential errors"* (Wang & Zhang 2026, Table 1).

**What to score for**: whether the user actively challenges, verifies, and pushes back on AI output — or accepts it uncritically.

**High-vigilance signals**:
- User asks AI to justify a claim, cite a source, or defend a framing
- User catches an AI error and says so explicitly
- User refuses to accept a draft and asks for a different approach
- User requests source verification or cross-checks with another tool
- User counter-argues before accepting

**Low-vigilance signals**:
- User accepts all drafts without critique
- User never asks "where does this claim come from?"
- User forwards AI output unchanged
- No explicit challenges to AI reasoning in the dialogue

**Empirical anchor**: H2a β = 0.437, p < 0.001, f² = 0.243 — **the single highest-impact path** in Wang & Zhang's model. Also the dimension with highest IPMA importance (0.438) *and* lowest IPMA performance (56.7/100), identifying it as the top priority for pedagogical intervention. If a user scores low here, that is the signal the paper most strongly implicates as correctable.

---

### Cognitive Reallocation

**Paper construct**: Human-GenAI Pedagogical Partnership (HGP) → Transformative Learning Experience (TLE), mediated by cognitive offloading (H3b indirect path β = 0.117, p < 0.001). Paper's characterisation: "strategic offloading liberates mental resources for higher-order reflection"; Risko & Gilbert (2016) cognitive offloading framework extended to show delegation is only learning-productive when freed capacity is *reinvested* in higher-order work.

**What to score for**: when the user hands work to the agent, what does the user do with the freed capacity? Is it invested in reframing research questions, questioning assumptions, constructing original arguments, making judgment calls — or is it idle?

**High-reallocation signals**:
- After AI completes a subtask, user revisits higher-level framing (e.g., "looking at your draft, I now think the RQ should be X not Y")
- User produces original synthesis not present in AI output
- User introduces counter-arguments, frameworks, or perspectives the AI did not raise
- User makes judgment calls that require context only the human has (stakeholder intent, institutional history, personal aesthetic)

**Low-reallocation signals**:
- User accepts AI work and moves to next prompt without higher-order engagement
- No original synthesis; user's contribution is routing and aggregation only
- Time saved by offloading does not translate to any visible higher-order contribution

**Empirical anchor**: Paper's post-hoc quadratic: the offloading→TLE path only materialises above a threshold (β-quadratic = 0.102, p < 0.001). Delegation without reallocation is Zone 2; delegation *with* reallocation is Zone 3.

---

### Zone Classification

**Paper construct**: three-zone framework (Wang & Zhang 2026's primary conceptual contribution, synthesised from the dual-pathway SEM + fsQCA configurations + post-hoc U-shape analysis). Popularised in Hardman (2026-04-16) and Means (2026-04-20).

**Synthesis rule** (derived from the three dimensions above):

| Zone | Delegation Intensity | Cognitive Vigilance | Cognitive Reallocation | Description |
|---|---|---|---|---|
| **Zone 1 — No AI use** | Near 0 | N/A | N/A | User carries full cognitive load manually. Learning occurs but capacity-constrained. |
| **Zone 2 — Shallow / Scattered** | Low–Mid | Low | Low–Mid | "Half-measures worse than no AI at all." Coordination overhead without meaningful cognitive savings. Empirically the worst outcome zone. |
| **Zone 3 — Deep Partnership** | High | High | High | Committed strategic delegation **with** critical evaluation **and** reinvested higher-order reflection. The zone in which transformative learning empirically occurs. |

**Scoring rule**: Zone 3 requires **all three** sub-dimensions to be high. Zone 2 is the default when at least one of Delegation Intensity or Cognitive Vigilance is low while AI is being used. Zone 1 is the default when AI is essentially unused in the dialogue window.

**Honest calibration** (anti-sycophancy): Zone 3 is empirically **rare**. Wang & Zhang's IPMA performance scores for CV (56.7) and HGP (54.2) — the two Zone 3 prerequisites — sit in the 55–60 range out of 100. A consumer agent should not default to Zone 3; if an aggregate score trends toward Zone 3, re-audit the dialogue for counter-evidence before finalizing.

---

## Scoring

Each of the first three dimensions is scored **0–10** (integer). Zone Classification is a label derived from the three dimension scores.

**Threshold guidance** (consumer agents may adapt these bands):

| Score band | Label |
|---|---|
| 0–3 | Low |
| 4–6 | Mid |
| 7–10 | High |

**Zone synthesis**:
- All three dimension scores ≥ 7 → Zone 3
- Delegation Intensity or Cognitive Vigilance < 4, AI actively used in dialogue → Zone 2
- Delegation Intensity < 2 AND Cognitive Reallocation N/A (AI essentially unused) → Zone 1
- All other combinations → Zone 2 with narrative qualifier

---

## Anti-sycophancy discipline for consumer agents

Any agent consuming this rubric **must** enforce:

1. **Evidence requirement**: no dimension score ≥ 7 ("High") without at least one specific dialogue-turn citation from the scored session.
2. **Forced counter-enumeration**: before finalizing scores, the agent lists ≥ 2 moments where the user could have gone deeper (even in high-scoring sessions).
3. **Re-audit trigger**: if the aggregate Zone label comes out Zone 3, re-audit the dialogue for counter-evidence. Zone 3 is empirically rare; a fast Zone 3 call is usually wrong.
4. **Descriptive language only**: no "great job!", no "needs improvement!". Report observed pattern + specific citable evidence.
5. **Cross-model divergence flag**: if the consumer agent runs cross-model (e.g., via `ARS_CROSS_MODEL`), any dimension score disagreement > 2 points between models must be flagged in the output.

## Explicitly out of scope

This rubric does **not**:

- Gate user progression. Consumer agents must declare `blocking: false` in their frontmatter.
- Replace AI self-reflection protocols (e.g., `academic-pipeline` Stage 6's six-dimension Collaboration Quality Evaluation, which is AI-about-itself; this rubric is AI-about-user-collaboration).
- Detect user "orientation" (efficiency vs depth). Wang & Zhang (2026)'s H4 on efficiency orientation as amplifier is not operationalised here.
- Prescribe which tasks to delegate. That is a pedagogical decision the user owns; this rubric only describes what delegation pattern occurred.

---

## Versioning

`rubric_version` follows semver. Changes to dimension count, synthesis rule, or operationalisation language require a **minor** bump and a note in `CHANGELOG.md`. Example-refinement or phrasing changes are **patch** bumps.

If a future paper supersedes or materially revises Wang & Zhang (2026)'s constructs, a **major** bump is required and the `paper_citation` field must be updated accordingly.
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-ground-truth-isolation-pattern-md"></a>

## SOURCE: shared/ground_truth_isolation_pattern.md

<!-- SOURCE-CONTENT-BEGIN bytes=12649 -->
# Ground-Truth Isolation Pattern

**Status**: v3.3.2 — narrative hub doc; for declarative annotations see
`shared/handoff_schemas.md`

---

## § 1 — Why ground-truth isolation matters

When an agent can read the evaluation answer key while producing the candidate
output, it learns to optimize directly against the rubric rather than against
the underlying task. The result is inflated scores that do not transfer to
held-out data — a textbook case of reward hacking. The failure is not about
intent; it is architectural. An agent that can see what counts as a correct
answer will, over time, route toward surface features of correctness rather
than toward the underlying quality those features are supposed to signal.

The failure mode appears at different granularities: a single agent session
that reads a scoring key before generating; a pipeline stage that appends
expected outputs to the prompt as "negative examples"; a calibration setup
where the model has already processed the gold set before it reports confidence
estimates. In every case, the shared presence of ground-truth material and
candidate-output generation in the same context produces results that look
strong on paper and fail on genuinely held-out evaluation.

Two published cases make this concrete and directly inform the ARS design.

Anthropic's automated-w2s-researcher (2026) uses a three-tier sandbox: local
mode for development, docker-with-redacted-data for integration testing, and
RunPod with server-side ground truth as the only valid evaluation tier. The
architecture exists because earlier iterations without this separation produced
unreliable results. Their README explicitly warns that local-mode results
"might not be legit" because the agent can find `labeled_data` on the local
filesystem. The solution is structural: ground truth never coexists in the same
process or filesystem layer as the agent generating candidate answers.
Isolation is a property of the system design, not a prompt-level instruction
that can be added after the fact.

Lu et al. (2026, *Nature* 651:914-919) document a related failure mode at
pipeline scale, which they call "shortcut reliance." In their fully autonomous
AI research system — the first to pass blind peer review end-to-end — models
exploit spurious correlations in training data, achieve high scores on the
target benchmark, and write papers describing the results as a genuine
scientific solution. The failure is not dishonesty; the model optimizes
whatever measurable signal is available. If the measurable signal leaks
information about the evaluation criterion, the model finds that leak. The
paper looks like a solved problem. The underlying scientific question remains
open.

ARS's human-in-the-loop pipeline already enforces the spirit of this
isolation: researchers set their own research questions, review outputs at each
integrity gate, and supply calibration gold sets at runtime rather than
embedding them in the repository. This document makes the pattern explicit and
machine-checkable via the `data_access_level` annotation declared in every
top-level `SKILL.md`.

---

## § 2 — The three-layer mental model

Every artifact in ARS belongs to one of three layers, and the direction of
flow is strictly one-way. An artifact can be promoted from a lower layer to a
higher one by passing an integrity gate. It cannot move in the other direction.
Layer 3 material cannot appear as input to a process whose output is layer 1
or 2.

**Layer 1 — raw inputs** covers user queries, primary sources retrieved from
web or database search, and agent-assembled bibliographies before any
verification. Material at this layer is untrusted by default. It may be
hallucinated, adversarially crafted, outdated, or contain PII. A skill
operating at layer 1 must treat every factual claim as potentially wrong, flag
gaps rather than silently filling them from parametric memory, and pass nothing
downstream as verified fact without explicit gate passage. The `deep-research`
skill operates here.

**Layer 2 — verified artifacts** are outputs that have cleared an integrity
gate: Semantic Scholar API existence confirmation, anti-leakage checks
confirming claims came from session material rather than from the model's
training-time memory, citation existence proofs, or the
`integrity_verification_agent`'s seven-mode failure checklist at Stage 2.5 or
4.5. Once an artifact is at layer 2, downstream skills may treat it as
provisionally reliable for argument building and paper drafting. The provenance
chain must remain traceable through the Material Passport carried with each
artifact.

**Layer 3 — ground truth and evaluation rubrics** includes gold labels,
reviewer scoring rubrics, calibration sets, and any material that defines what
a correct output looks like. This layer is distinct in kind, not just degree.
The critical rule is that no agent operating on layer 1 or 2 inputs and
producing layer 1 or 2 outputs should ever have layer 3 material in its
context window. The boundary between layer 2 and layer 3 is not a quality
filter — it is an epistemological firewall.

The `data_access_level` annotation in `SKILL.md` frontmatter maps to this
model as follows:

| Value | Layer | Meaning |
|---|---|---|
| `raw` | Layer 1 | Operates on unverified sources; must assume adversarial or hallucinated input |
| `redacted` | Boundary 1→2 | Operates on sanitized material with no new raw ingestion |
| `verified_only` | Layer 2 | Runs only after upstream integrity gates have been passed |

No ARS skill operates on layer 3 inputs and produces layer 1 or 2 outputs.
The reviewer skill holds a rubric, but that rubric is either a structural
format guide (not an answer key) or a calibration gold set supplied by the
human researcher at runtime. The paper-writing agent never reads the rubric
before generating its candidate output.

---

## § 3 — Rules for adding a skill or agent

Isolation is a design-time decision. The time to reason about data layer
boundaries is before writing any agent prompt, not after a skill is already
in use.

**DO: Declare `data_access_level` truthfully.** The value must reflect the
dirtiest input the skill may legitimately consume across all its modes. If one
mode processes raw web search results and another processes verified artifacts,
the skill's declared level is `raw`. The annotation exists so pipeline authors
can reason about data-flow safety without reading every agent definition file.

**DO: Separate rubric files from skill input bundles.** Use `*/rubrics/` for
repo-tracked rubric files that describe output format or structural
requirements — not answer keys, not expected content. For calibration gold
sets, require the human researcher to supply a session file at runtime. Never
bundle gold labels into the repository or reference them from `SKILL.md` in a
way that loads them unconditionally.

**DO: Pass scores back through a reviewer agent that holds the rubric
privately.** The review workflow is: reviewer reads paper + rubric → reviewer
produces natural-language feedback → paper-writing agent reads paper +
feedback. The paper-writing agent's context must never contain the rubric text
or the expected scoring outcome before it produces its candidate output. The
two agents must be separate invocations, or separated by a stage boundary
where the context window does not carry rubric content forward.

**DON'T: Embed answer keys, scoring rubrics, or test-set labels in any file
an agent reads as part of normal context loading.** This applies to `SKILL.md`
frontmatter, agent definition files, reference files loaded unconditionally at
session start, and any file an agent accesses as background material. If the
file loads at session initialization, it is layer 1 or 2 material — not
layer 3.

**DON'T: Pass an evaluation prompt that includes the expected output to the
same agent that produces the candidate output.** The "negative example"
framing does not protect against this: models pattern-match toward examples
regardless of polarity labeling.

**DON'T: Use the same model session for both output generation and output
scoring without stripping rubric content from the generating context.** A
model that has seen rubric text in the conversation history will orient toward
it during generation even without explicit instruction. Separate invocations,
not just separate instructions, are required.

---

## § 4 — Today's implementation

The isolation pattern is already instantiated across the ARS codebase through
a set of narrowly scoped protocol files. This section is a navigational map —
not a duplication of their contents.

| Mechanism | Where it lives |
|---|---|
| Source verification (S2 API) | `deep-research/references/semantic_scholar_api_protocol.md` |
| Anti-leakage protocol | `academic-paper/references/anti_leakage_protocol.md` |
| Integrity gates (Stage 2.5/4.5) + 7-mode failure checklist | `academic-pipeline/references/ai_research_failure_modes.md` |
| Reviewer calibration mode (FNR/FPR with private gold set) | `academic-paper-reviewer/references/calibration_mode_protocol.md` |
| Cross-model verification | `shared/cross_model_verification.md` |
| Declarative posture | `shared/handoff_schemas.md` (`data_access_level` and `task_type` sections) |

This pattern document is the narrative rationale; those six reference files
are the implementation detail. If a specific rule here conflicts with language
in one of those files, the more specific file governs for that mechanism —
and that conflict should be surfaced as an issue so this document can be
updated.

---

## § 5 — What this pattern is NOT

**Not a runtime permission system.** Nothing in ARS enforces isolation at
execution time by blocking API calls, sandboxing the filesystem, or
intercepting prompt construction. The mechanism is convention, declarative
annotation, and CI lint via `scripts/check_data_access_level.py`. That script
confirms every `SKILL.md` carries a valid annotation; it does not inspect
context windows at runtime. A contributor who deliberately passes ground-truth
material into a raw-layer skill's context can do so — the pattern is a design
commitment and an audit surface, not a technical lock.

**Not a substitute for human review at integrity gates.** Stage 2.5 and
Stage 4.5 are the actual enforcement points in the pipeline. The human
researcher reviews the integrity agent's reports and makes go/no-go decisions
at each gate. This pattern document explains the design reasoning behind those
gates and the data-flow structure that makes them meaningful. Reading this
document does not grant confidence that any specific pipeline run was clean.
Only a passed integrity gate with a verified Material Passport does that.

**Not a benchmark protocol.** All current ARS skills are `task_type:
open-ended` because ARS targets humanities research, higher-education quality
assurance, and policy analysis — work whose quality depends on domain judgment
and interpretive context that no scalar metric fully captures. This pattern
keeps that posture honest by making it harder to accidentally introduce
benchmark-style optimization into the pipeline. It does not provide
infrastructure for running ARS outputs through automatic scoring against a
held-out test set, and that gap is intentional.

---

## § 6 — Future evolution (intentionally out of scope)

Version 3.3.2 ships the pattern document, the `data_access_level` annotation
across all four top-level `SKILL.md` files, and the `task_type` annotation.
The isolation pattern is fully stated at the declarative and documentation
level. Several natural extensions are foreseeable but explicitly out of scope
for this release: a server-side rubric endpoint that supplies evaluation
criteria to reviewer agents without exposing them in the local context window
(directly analogous to the RunPod tier in Anthropic's w2s sandbox); per-agent
rather than per-skill access levels, allowing a multi-mode skill to tag
individual agent definition files with the layer they operate on; runtime
verification that the Material Passport's declared `data_access_level` chain
is consistent with the actual handoff sequence before a consuming agent accepts
an artifact; and automated detection of rubric or gold-label content appearing
in a generating agent's context. These possibilities are listed here so future
contributors do not propose them as overlooked features — they are deferred,
not missing. If you want to pursue one, open an issue referencing this section
before writing code, so the tradeoffs can be discussed before implementation
begins.
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-mode-spectrum-md"></a>

## SOURCE: shared/mode_spectrum.md

<!-- SOURCE-CONTENT-BEGIN bytes=4047 -->
# Mode Spectrum: Fidelity vs Originality

**Status**: v3.2
**Source**: Lu et al. (2026, Nature 651:914-919) Figure 1c — template-based mode produces higher-quality, lower-variance papers; template-free mode produces more diverse outputs but lower mean quality and higher variance. ARS maps this finding onto its own mode taxonomy.

---

## Why this spectrum exists

Not all modes should treat templates and examples the same way. A `systematic-review` needs rigid structure (PRISMA checklist, predefined sections) — templates are load-bearing. A `socratic` dialogue needs room to wander — heavy templates kill exploration.

Lu et al.'s template-based vs template-free comparison gives us a language for this trade-off: **fidelity** (reproducible, template-heavy, lower variance) vs **originality** (exploratory, template-light, higher variance, higher ceiling on novelty).

ARS modes fall on a spectrum between these poles. This table is the reference for decisions about:
- How much template/example material to load at mode start
- Whether to inline templates in SKILL.md or load from sub-files on demand (v3.1 Phase 3)
- Whether to suggest the mode when the user's goal is "predictable output" vs "creative exploration"

---

## Mode spectrum table

| Skill | Mode | Spectrum position | Template load | Rationale |
|---|---|---|---|---|
| deep-research | `systematic-review` | Fidelity | Heavy | PRISMA protocol, predefined search strategy, reproducible steps |
| deep-research | `lit-review` | Fidelity | Heavy | Structured annotated bibliography, fixed output format |
| deep-research | `fact-check` | Fidelity | Heavy | Claim → evidence → verdict pipeline, no room for drift |
| deep-research | `quick` | Fidelity | Heavy | Time-boxed brief, fixed 3-section format |
| deep-research | `review` | Balanced | Medium | Review has structure but allows domain-specific adaptation |
| deep-research | `full` | Balanced | Medium | Structured output but methodology selection is exploratory |
| deep-research | `socratic` | Originality | Light | User-led dialogue, templates constrain exploration |
| academic-paper | `full` | Balanced | Medium | Section templates loaded, but writing adapts to argument |
| academic-paper | `outline-only` | Balanced | Medium | Structure templates needed, but outline is creative |
| academic-paper | `revision` | Fidelity | Heavy | R&R tracking template, point-by-point responses |
| academic-paper | `revision-coach` | Balanced | Medium | Coaching is semi-structured; roadmap template loaded |
| academic-paper | `abstract-only` | Fidelity | Heavy | Fixed abstract structure (background/method/results/conclusion) |
| academic-paper | `lit-review` | Fidelity | Heavy | Annotated bibliography format |
| academic-paper | `format-convert` | Fidelity | Heavy | Format conversion is purely mechanical |
| academic-paper | `citation-check` | Fidelity | Heavy | Citation audit is checklist-driven |
| academic-paper | `plan` | Originality | Light | Socratic planning dialogue, no forced chapter sequence |
| academic-paper | `disclosure` (v3.2) | Fidelity | Heavy | Venue policy database → templated output |
| academic-paper-reviewer | `full` | Balanced | Medium | Review rubric loaded, but reviewer perspectives are dynamic |
| academic-paper-reviewer | `re-review` | Fidelity | Heavy | R&R traceability matrix, checklist-driven |
| academic-paper-reviewer | `quick` | Fidelity | Heavy | Fixed EIC quick-assessment format |
| academic-paper-reviewer | `methodology-focus` | Fidelity | Heavy | Focused on statistical/methods rubric |
| academic-paper-reviewer | `guided` | Originality | Light | Socratic dialogue, adaptive to what the user needs |
| academic-paper-reviewer | `calibration` (v3.2) | Fidelity | Heavy | Fixed 5x ensembling protocol, no creative adaptation |

---

## Mode recommendation

- User wants "predictable" / "consistent" → suggest **Fidelity** modes
- User wants to "explore" / "think through" → suggest **Originality** modes
- Unclear → suggest **Balanced** modes as default
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-raise-framework-md"></a>

## SOURCE: shared/raise_framework.md

<!-- SOURCE-CONTENT-BEGIN bytes=7365 -->
---
title: RAISE Framework (v3.4.0 snapshot)
snapshot_date: "2025-07-17"
upstream_source: "https://eppi.ioe.ac.uk/CMS/Portals/0/RAISE%20ESG%20BPWG.pdf"
upstream_version: "NIHR ESG Best Practice Working Group consultation draft, 17 July 2025"
citation: "Thomas J, Flemyng E, Noel-Storr A, et al. Responsible Use of AI in Evidence Synthesis (RAISE). NIHR ESG Best Practice Working Group in AI/Automation, EPPI-Centre, UCL Social Research Institute. 17 July 2025."
related: "Position Statement on AI Use in Evidence Synthesis (Cochrane, Campbell, JBI, CEE), Campbell Systematic Reviews, 2025, doi:10.1002/cl2.70074"
---

# RAISE Framework

## Scope disclaimer (required, do not remove)

RAISE's official scope is **evidence synthesis** (systematic review, meta-analysis, scoping review, rapid review, evidence mapping). When ARS applies RAISE **principles** to non-evidence-synthesis work — e.g., `academic-paper full` on primary research — this is a **principle extension**, not official RAISE compliance. ARS's `compliance_agent` will only claim RAISE compliance for outputs produced in `systematic_review` or `other_evidence_synthesis` modes.

**Used by**: `compliance_agent` (Task 8).

## Four principles

Each principle carries a definition, ARS check procedure, and pass/warn/fail criteria. These are the universal kernel of RAISE and are checked in every mode.

### Principle 1 — Human oversight

**Definition:** AI and automation in evidence synthesis should be used with meaningful human oversight, not as an autonomous replacement.
**ARS check (Stage 2.5 focus):** At Stage 2.5, verify `methodology_blueprint` specifies reviewer count, qualifications, and adjudication mechanism. At Stage 4.5, verify manuscript describes the human oversight applied in practice.
**Pass:** Reviewer count + adjudication mechanism + qualifications all present, each with evidence path.
**Warn:** Any one missing, OR only present in vague form ("authors reviewed AI output").
**Fail:** Two or more missing.

### Principle 2 — Transparency

**Definition:** Any AI or automation use that makes or suggests judgements must be fully and transparently reported.
**ARS check (Stage 4.5 focus):** Verify manuscript lists every AI tool used, at what stage, with prompts/parameters/versions. Cross-reference against `user_metadata.ai_tools_used`.
**Pass:** All declared tools reported AND all reported tools declared.
**Warn:** Mismatch in ≤1 tool, or reporting lacks one of {stage, prompt, parameters, version}.
**Fail:** Multiple tools undeclared OR systematically missing prompts/parameters.

### Principle 3 — Reproducibility

**Definition:** AI-assisted evidence synthesis should be reproducible to a stated level.
**ARS check:** Verify presence of `passport.repro_lock` (v3.3.5 feature) OR equivalent manuscript description (model version, seeds, prompt, data access details). Stochasticity must be declared per `artifact_reproducibility_pattern.md`.
**Pass:** Repro_lock present AND stochasticity declared.
**Warn:** One of the two missing.
**Fail:** Both missing.

### Principle 4 — Fit-for-purpose

**Definition:** AI tools should be chosen and validated for specific tasks within the evidence synthesis, not applied generically.
**ARS check (Stage 2.5 focus):** Verify manuscript describes why each AI tool was chosen for its specific task. Look for pilot-phase evidence OR prior validation citation.
**Pass:** Per-tool justification + ≥1 validation reference.
**Warn:** Justification present without validation reference.
**Fail:** Generic "we used AI to save time" with no task-level justification.

## Full 8-role matrix (SR mode only)

Used when `raise.mode == "full"` (SR and other_evidence_synthesis). Each role carries 2–3 responsibilities extracted from the RAISE consultation PDF. The agent maps ARS users and ARS itself onto the roles they occupy.

**Default role attribution:**
- ARS user (the human running the skill): Evidence Synthesists
- ARS itself (the skill suite): AI Development Teams + Methodologists (dual role)

### Role 1 — Evidence Synthesists

1. Remain ultimately responsible for the evidence synthesis, regardless of AI assistance.
2. Report AI use in the evidence synthesis manuscript transparently.
3. Ensure ethical, legal, and regulatory standards are adhered to when using AI.

**ARS check:** manuscript contains author responsibility statement; AI-usage disclosure is present; ethics/IRB section addresses AI use.

### Role 2 — AI Development Teams

1. Adhere to open-science practices when designing, building, testing, and validating tools.
2. Be transparent about when AI works best, its limitations, and any interests.
3. Commit to continued learning, development, and monitoring.

**ARS self-declaration:** ARS is open-source (CC BY-NC 4.0); CHANGELOG tracks limitations; calibration results published per `calibration_mode_protocol.md`.

### Role 3 — Methodologists

1. Adhere to open science practice when researching and evaluating AI systems.
2. Commit to independent evaluations and validation of AI systems.

**ARS self-declaration:** ARS cross-model verification per `cross_model_verification.md` provides one form of independent validation; sixth-reviewer peer review remains planned.

### Role 4 — Publishers of evidence synthesis

1. Ensure best-practice standards for responsible AI use are clear and integrated into policies and guidelines for authors.
2. Request transparency and honesty from authors on their use of AI in evidence synthesis.

**ARS note:** Out of ARS's direct control; surfaced in compliance_report as stakeholder context.

### Role 5 — Users of evidence synthesis

1. Critically consider the potential influence of AI use in a synthesis before use.
2. Underscore the potential impacts of AI use in downstream documents and decision-making processes.
3. Communicate the need for transparent reporting of tool accuracy and biases.

**ARS note:** Out of direct scope; listed for ecosystem completeness.

### Role 6 — Trainers of evidence synthesis methods

1. Ensure best-practice standards for responsible AI are embedded within training materials.
2. Equip trainees with the knowledge they need to determine if an AI tool is appropriate.
3. Undertake continuous training and development to stay up to date with emerging AI tools.

**ARS note:** Out of direct scope.

### Role 7 — Organisations producing evidence synthesis

1. Ensure best-practice standards for responsible AI are clear and integrated into policies and guidelines.
2. Promote, guide, and support responsible AI use in evidence synthesis activities.
3. Monitor the development and use of AI within the organisation.

**ARS note:** Out of direct scope.

### Role 8 — Funders of evidence synthesis

1. Encourage the responsible use of AI.
2. Consider sustainability and generalisability of the products they support.

**ARS note:** Out of direct scope.

## Usage in compliance_agent

- SR mode: `raise.mode = "full"`, both principles AND roles populated
- primary_research mode: `raise.mode = "principles_only"`, `roles` field absent or empty
- other_evidence_synthesis mode: `raise.mode = "full"`, roles populated with adaptation noted in evidence paths

Block decisions follow tier semantics: any principle at `fail` status + `systematic_review` mode → `block`. `primary_research` mode **never** blocks.
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-style-calibration-protocol-md"></a>

## SOURCE: shared/style_calibration_protocol.md

<!-- SOURCE-CONTENT-BEGIN bytes=7085 -->
# Style Calibration Protocol

## Purpose

Learns the author's natural writing voice from past writing samples and applies it as a soft guide during paper drafting. The goal is **personalization**, not de-AI-ification — the author's voice should come through in the final text, within the boundaries of discipline conventions.

> **Design boundary**: This is NOT a humanizer. We do not aim to evade AI detectors. We aim to produce text that sounds like the author wrote it, because the author's judgment and style are part of scholarly identity.

---

## When to Use

- **Primary entry point**: `academic-paper/agents/intake_agent` Step 10 (optional)
- **Pipeline carry**: `academic-pipeline` Material Passport carries the Style Profile across all stages
- **Consumers**: `academic-paper/agents/draft_writer_agent`, `deep-research/agents/report_compiler_agent`

---

## Calibration Flow

### Step 1: Sample Collection

Ask the user:
> "Do you have past papers or writing samples you'd like me to learn your style from? Providing 3+ samples helps me match your natural voice. This is optional."

**Requirements**:
- Minimum 3 samples recommended (1-2 samples produce unreliable profiles)
- Samples should be the user's own writing (not co-authored sections they didn't write)
- Same language as the target paper preferred
- Same discipline preferred but not required

**Acceptable formats**: PDF, DOCX, Markdown, plain text, pasted excerpts

### Step 2: Dimension Extraction

Analyze each sample across 6 dimensions:

#### Dimension 1: Sentence Length Distribution
- Mean word count per sentence
- Standard deviation (captures variability)
- Rhythm pattern: does the author alternate short-long, or maintain steady length?
- Example profile: `{mean: 22, stddev: 8, rhythm: "variable — mixes 8-word punchy sentences with 35-word complex ones"}`

#### Dimension 2: Paragraph Length Distribution
- Mean sentences per paragraph
- Variation across sections (e.g., shorter paragraphs in Methods, longer in Discussion)
- Example profile: `{mean_sentences: 5, variation: "moderate — 3-7 sentences, shorter in Methods"}`

#### Dimension 3: Vocabulary Preferences
- **Hedging patterns**: which hedging words does the author prefer? ("suggests" vs "indicates" vs "implies")
- **Transition words**: preferred connectives ("However" vs "Nevertheless" vs "Yet")
- **Preferred verbs**: reporting verbs for citations ("found" vs "demonstrated" vs "showed")
- **Formality level**: where on the spectrum from conversational academic to highly formal
- Example profile: `{hedging: ["suggests", "appears to", "may"], transitions: ["However", "In contrast", "Yet"], reporting: ["found", "argued", "noted"], formality: "moderate-formal"}`

#### Dimension 4: Citation Integration Style
- Narrative ratio: how often does the author use "Smith (2024) found..." vs "(Smith, 2024)"
- Citation density: average citations per paragraph
- Citation placement: beginning of paragraph (context-setting) vs end (evidence-backing)
- Example profile: `{narrative_ratio: 0.4, density: 2.3, placement: "mixed — narrative for key claims, parenthetical for supporting"}`

#### Dimension 5: Modifier Style
- Minimal vs elaborate: does the author use many adjectives/adverbs, or keep it lean?
- Abstract vs concrete: preference for abstract concepts or concrete examples?
- Example profile: `{modifier_density: "minimal — lean prose, few adjectives", abstraction: "concrete — prefers specific examples over generalizations"}`

#### Dimension 6: Register Shifts
- How does tone change across paper sections?
- Typically: Methods (neutral/procedural) → Results (descriptive) → Discussion (interpretive/assertive)
- Does the author maintain consistent register or shift noticeably?
- Example profile: `{shifts: "noticeable — cautious in Methods, increasingly assertive in Discussion, most personal voice in Conclusion"}`

### Step 3: Profile Synthesis

Combine the 6 dimensions into a **Style Profile** artifact (see `shared/handoff_schemas.md` Schema 10).

Report to the user:
> "I've analyzed your writing style from [N] samples. Key traits:
> - [1-sentence summary of most distinctive trait]
> - [1-sentence summary of second distinctive trait]
> I'll use this as a soft guide — discipline conventions always take priority."

---

## Consumption Rules — Priority System

When the Style Profile is consumed during writing, apply the following priority hierarchy:

```
Priority 1 (HARD): Discipline conventions
  → Cannot be violated. E.g., if the discipline requires third-person,
    the author's preference for first-person is overridden.

Priority 2 (STRONG): Target journal conventions
  → If the user has specified a target journal, its style norms take precedence.
    E.g., Nature requires short paragraphs; author's preference for long paragraphs is overridden.

Priority 3 (SOFT): Author's personal style
  → Applied only where it does not conflict with Priority 1 or 2.
    E.g., the author's preferred transition words, hedging patterns,
    citation integration ratio — these are safe to apply.
```

### Conflict Resolution

When personal style conflicts with discipline or journal norms:

1. **Use the norm** (Priority 1 or 2 wins)
2. **Log the conflict** in Draft Metadata:
   ```
   Style conflict: Author prefers passive voice (72% in samples),
   but target discipline (Engineering) conventions favor active voice.
   → Using active voice per discipline convention.
   ```
3. **Notify the user** (once per draft, not per instance):
   > "Note: Your typical use of [trait] differs from [discipline/journal] convention. I've followed the convention, but you can adjust manually if you prefer your style here."

### Safe Dimensions (always applicable)

These dimensions rarely conflict with norms and can be applied freely:
- Preferred transition words (within academic register)
- Hedging word choices
- Reporting verb preferences
- Citation integration ratio (narrative vs parenthetical)
- Modifier density (as long as precision is maintained)
- Sentence length variability patterns

### Risky Dimensions (check before applying)

These dimensions may conflict with discipline/journal norms:
- Voice (active vs passive) — discipline-dependent
- Paragraph length — journal-dependent
- Person (first vs third) — discipline-dependent
- Formality level — journal-dependent

---

## Edge Cases

### Insufficient Samples
If user provides < 3 samples: generate a partial profile with a warning.
> "I have a preliminary style profile from [N] sample(s), but it may not be fully representative. I'll apply it cautiously."

### Mismatched Language
If samples are in a different language than the target paper: extract transferable dimensions only (paragraph structure, citation style, modifier density). Skip vocabulary preferences.

### Co-authored Samples
If user indicates samples are co-authored: ask which sections they wrote. Analyze only those sections.

### Style Evolution
If samples span many years: weight recent samples more heavily (2x weight for samples within 2 years).
<!-- SOURCE-CONTENT-END -->
