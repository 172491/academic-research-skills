---
name: academic-research-skills-compact
description: "Compact, source-complete academic research Power for research, paper writing, peer review, and pipeline orchestration."
displayName: "Academic Research Skills — Compact"
keywords: ["academic research", "paper writing", "literature review", "systematic review", "peer review", "citation verification", "research pipeline", "research", "deep research", "academic paper", "manuscript review", "fact-check", "研究", "深度研究", "學術論文", "学术论文", "論文寫作", "论文写作", "文獻回顧", "文献综述", "系統性回顧", "系统综述", "同儕審查", "同行评审", "引註查核", "引文核查"]
---

# Academic Research Skills — Compact

This upload is a deterministic, source-complete repackaging of four canonical skills and their load-bearing audit dependencies. The directory contains exactly **42 plain-text UTF-8 files**.

## First-hop routing

Choose exactly one first-hop skill from the user's immediate intent:

- `deep-research`: research-question formation, retrieval, fact-checking, evidence synthesis, or a systematic review.
- `academic-paper`: outlining, drafting, abstracts, writing a literature-review section, citation formatting, or directly revising a manuscript in response to reviewer comments.
- `academic-paper-reviewer`: evaluating an existing manuscript, simulating peer review, or re-reviewing whether revisions adequately answer prior comments.
- `academic-pipeline`: only when the user explicitly requests the complete research → write → review → revise workflow.

For the two common overlaps: use `deep-research` to retrieve and synthesize literature, but `academic-paper` to write the literature-review section; use `academic-paper` to make requested revisions, but `academic-paper-reviewer` to judge whether those revisions answer the review. If the first hop remains unclear, ask exactly one clarifying question.

## Loading discipline

1. First read only the applicable `skills/<skill>/SKILL.md`.
2. Use `SOURCE-MANIFEST.md` to resolve the named legacy source path, then read one relevant agent bundle and only the necessary reference or asset bundle.
3. Do **not** read every bundle by default. Expand context only when the selected skill or current task requires it.

Single-stage requests should use the matching skill directly. Use `academic-pipeline` only for the explicit full workflow above. The user's original work specifications, supplied materials, constraints, and requested mode take precedence over generic workflow defaults in these bundled sources.

## Legacy path resolution

Canonical documents retain their original repository-relative references. Resolve them through `SOURCE-MANIFEST.md`:

- `academic-paper/<...>`, `academic-paper-reviewer/<...>`, `academic-pipeline/<...>`, or `deep-research/<...>` means the manifest source path with a leading `skills/`.
- `skills/<...>` and `shared/<...>` are already canonical source paths; locate their target file and source anchor in the manifest.
- In **every skill document**, a bare `agents/<...>`, `references/<...>`, `templates/<...>`, or `examples/<...>` path is always rooted at `skills/<selected-skill>/`, regardless of the original source file's subdirectory or compact bundle location.
- Only a path explicitly beginning with `./` or `../` is relative to the original canonical source file's parent directory. Normalize that canonical path before looking it up in the manifest.
- `.claude/CLAUDE.md` maps to the standalone `CLAUDE.md`.
- `LICENSE` and `NOTICE.md` are preserved as separate source sections in `LEGAL.md`.

A manifest `whole-file` entry is a byte-for-byte standalone copy. Other entries point to an HTML source anchor followed by `## SOURCE: original/path`; the original body is preserved in the length-delimited source section.

## Schemas and frozen contracts

`shared/schemas-core.md` and `shared/schemas-passport-audit.md` carry original JSON Schema source bytes inside fenced `json` source sections for reading and extraction. The four files under `shared/contracts/{reviewer,writer,evaluator}/` are different: they are frozen runnable contract instances copied byte-for-byte as standalone JSON files.

## Audit runtime boundary

`runtime/audit-artifact-gate.md` and `runtime/claim-audit.md` preserve the full text of selected load-bearing specifications and implementation sources. This Kiro Web custom Power cannot safely execute the external codex wrapper, and the bundled source sections are not standalone executables. When the complete `academic-pipeline` reaches a non-skippable audit gate, it must block unless a qualifying audit artifact has been produced by an external environment; it must never claim that the gate passed without that artifact. Single-stage `deep-research`, `academic-paper`, and `academic-paper-reviewer` requests are not subject to this external gate.

## Package boundary

The compact package has no independent executable `scripts/` tree or standalone `docs/` tree. Selected script and design source texts are preserved inside the two `runtime/` bundles for provenance and implementation reference; all other capabilities remain limited to files and tools actually available in the host environment.

See `SOURCE-MANIFEST.md` for source provenance and SHA-256 values, and `LEGAL.md` for the complete license and notice text.
