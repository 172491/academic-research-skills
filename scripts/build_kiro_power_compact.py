#!/usr/bin/env python3
"""Build and verify the deterministic 42-file compact Kiro Power.

The builder preserves every canonical source byte inside either a direct copy or a
length-delimited SOURCE section. It deliberately excludes the empty pipeline
adapter .gitkeep and fails when the canonical source inventory changes, forcing
this explicit thematic mapping to be reviewed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import shutil
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUTPUT = REPO / "kiro-power-compact"
SKILLS = (
    "academic-paper",
    "academic-paper-reviewer",
    "academic-pipeline",
    "deep-research",
)
EMPTY_EXCLUSION = "skills/academic-pipeline/references/adapters/.gitkeep"
DIRECT_ANCHOR = "whole-file"
SKILL_SHARED_RAW_COUNT = 199
SKILL_SHARED_INCLUDED_COUNT = 198
ADDITIONAL_SOURCE_COUNT = 13
INCLUDED_SOURCE_COUNT = 211
OUTPUT_FILE_COUNT = 42
BEGIN_RE = re.compile(rb"<!-- SOURCE-CONTENT-BEGIN bytes=(\d+) -->\n")
PATH_REFERENCE_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"(?P<path>"
    r"(?:"
    r"(?:\.\.?/)+(?:(?:skills/)?(?:academic-paper|academic-paper-reviewer|academic-pipeline|deep-research)/)?|"
    r"skills/(?:academic-paper|academic-paper-reviewer|academic-pipeline|deep-research)/|"
    r"(?:academic-paper|academic-paper-reviewer|academic-pipeline|deep-research)/"
    r")?"
    r"(?:"
    r"agents/[A-Za-z0-9_./{}*?<>\[\]-]+\.md|"
    r"references/[A-Za-z0-9_./{}*?<>\[\]-]+\.(?:md|json)|"
    r"templates/[A-Za-z0-9_./{}*?<>\[\]-]+\.(?:md|tex)|"
    r"examples/[A-Za-z0-9_./{}*?<>\[\]-]+\.md"
    r")"
    r")"
)
PLACEHOLDER_CHARS = frozenset("{}*?<>[]")

PAPER_PLANNING = (
    "intake_agent.md",
    "literature_strategist_agent.md",
    "structure_architect_agent.md",
    "argument_builder_agent.md",
    "socratic_mentor_agent.md",
    "revision_coach_agent.md",
)
PAPER_WRITING_REFS = (
    "abstract_writing_guide.md",
    "academic_writing_style.md",
    "apa7_chinese_citation_guide.md",
    "apa7_extended_guide.md",
    "citation_format_switcher.md",
    "credit_authorship_guide.md",
    "funding_statement_guide.md",
    "hei_domain_glossary.md",
    "journal_submission_guide.md",
    "latex_template_reference.md",
    "paper_structure_patterns.md",
    "policy_anchor_table.md",
    "statistical_visualization_standards.md",
    "venue_disclosure_policies.md",
    "writing_judgment_framework.md",
    "writing_quality_check.md",
)
PAPER_WORKFLOW_REFS = (
    "anti_leakage_protocol.md",
    "changelog.md",
    "disclosure_mode_protocol.md",
    "failure_paths.md",
    "mode_selection_guide.md",
    "plan_mode_protocol.md",
    "policy_anchor_disclosure_protocol.md",
    "vlm_figure_verification.md",
    "workflow_phase_details.md",
)
REVIEWER_PANEL = (
    "eic_agent.md",
    "methodology_reviewer_agent.md",
    "domain_reviewer_agent.md",
    "perspective_reviewer_agent.md",
    "devils_advocate_reviewer_agent.md",
)
PIPELINE_ORCHESTRATION = (
    "pipeline_orchestrator_agent.md",
    "state_tracker_agent.md",
    "collaboration_depth_agent.md",
)
PIPELINE_STATE_REFS = (
    "changelog.md",
    "literature_corpus_consumers.md",
    "mode_advisor.md",
    "passport_as_reset_boundary.md",
    "pipeline_state_machine.md",
    "process_summary_protocol.md",
    "progress_dashboard_template.md",
    "reinforcement_content.md",
    "score_trajectory_protocol.md",
    "team_collaboration_protocol.md",
    "adapters/overview.md",
)
PIPELINE_INTEGRITY_REFS = (
    "ai_research_failure_modes.md",
    "claim_audit_calibration_protocol.md",
    "claim_verification_protocol.md",
    "external_review_protocol.md",
    "integrity_review_protocol.md",
    "plagiarism_detection_protocol.md",
    "reproducibility_audit.md",
    "two_stage_review_protocol.md",
)
DEEP_RETRIEVAL = (
    "research_question_agent.md",
    "research_architect_agent.md",
    "bibliography_agent.md",
    "source_verification_agent.md",
)
DEEP_SYNTHESIS = (
    "synthesis_agent.md",
    "risk_of_bias_agent.md",
    "meta_analysis_agent.md",
    "report_compiler_agent.md",
)
DEEP_SYSTEMATIC_REFS = (
    "cross_agent_quality_definitions.md",
    "equator_reporting_guidelines.md",
    "literature_monitoring_strategies.md",
    "methodology_patterns.md",
    "preregistration_guide.md",
    "source_quality_hierarchy.md",
    "systematic_review_protocol.md",
    "systematic_review_toolkit.md",
)
FROZEN_CONTRACTS = (
    "shared/contracts/reviewer/full.json",
    "shared/contracts/reviewer/methodology_focus.json",
    "shared/contracts/writer/full.json",
    "shared/contracts/evaluator/full.json",
)
AUDIT_ARTIFACT_GATE_SOURCES = (
    "docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md",
    "scripts/run_codex_audit.sh",
    "scripts/audit_snapshot.py",
    "scripts/parse_audit_verdict.py",
    "scripts/check_audit_artifact_consistency.py",
)
CLAIM_AUDIT_SOURCES = (
    "docs/design/2026-05-15-issue-103-claim-alignment-audit-spec.md",
    "scripts/claim_audit_pipeline.py",
    "scripts/claim_audit_finalizer.py",
    "scripts/_claim_audit_constants.py",
    "scripts/uncited_assertion_detector.py",
)
RUNTIME_SOURCES = AUDIT_ARTIFACT_GATE_SOURCES + CLAIM_AUDIT_SOURCES


def rel_files(directory: str) -> list[str]:
    base = REPO / directory
    return sorted(
        path.relative_to(REPO).as_posix()
        for path in base.iterdir()
        if path.is_file()
    )


def prefixed(directory: str, names: tuple[str, ...] | list[str]) -> list[str]:
    return [f"{directory}/{name}" for name in names]


def complement(directory: str, selected_names: tuple[str, ...]) -> list[str]:
    selected = set(prefixed(directory, selected_names))
    return [path for path in rel_files(directory) if path not in selected]


def anchor_for(source: str) -> str:
    return "source-" + re.sub(r"[^a-z0-9]+", "-", source.lower()).strip("-")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_inventory() -> tuple[list[str], list[str]]:
    raw: list[str] = []
    for skill in SKILLS:
        raw.extend(
            path.relative_to(REPO).as_posix()
            for path in (REPO / "skills" / skill).rglob("*")
            if path.is_file()
        )
    raw.extend(
        path.relative_to(REPO).as_posix()
        for path in (REPO / "shared").rglob("*")
        if path.is_file()
    )
    raw.sort()
    if len(raw) != SKILL_SHARED_RAW_COUNT:
        raise RuntimeError(
            f"expected {SKILL_SHARED_RAW_COUNT} skill/shared files, found {len(raw)}"
        )
    empty = [path for path in raw if not (REPO / path).read_bytes()]
    if empty != [EMPTY_EXCLUSION]:
        raise RuntimeError(f"unexpected empty source inventory: {empty!r}")
    included = [path for path in raw if path != EMPTY_EXCLUSION]
    if len(included) != SKILL_SHARED_INCLUDED_COUNT:
        raise RuntimeError(
            f"expected {SKILL_SHARED_INCLUDED_COUNT} non-empty skill/shared files, "
            f"found {len(included)}"
        )
    return raw, included


def source_mapping() -> tuple[dict[str, list[str]], dict[str, str]]:
    bundles: dict[str, list[str]] = {
        "LEGAL.md": ["LICENSE", "NOTICE.md"],
        "runtime/audit-artifact-gate.md": list(AUDIT_ARTIFACT_GATE_SOURCES),
        "runtime/claim-audit.md": list(CLAIM_AUDIT_SOURCES),
        "bundles/academic-paper/agents-planning.md": prefixed(
            "skills/academic-paper/agents", PAPER_PLANNING
        ),
        "bundles/academic-paper/agents-production.md": complement(
            "skills/academic-paper/agents", PAPER_PLANNING
        ),
        "bundles/academic-paper/references-writing.md": prefixed(
            "skills/academic-paper/references", PAPER_WRITING_REFS
        ),
        "bundles/academic-paper/references-workflow.md": prefixed(
            "skills/academic-paper/references", PAPER_WORKFLOW_REFS
        ),
        "bundles/academic-paper/templates.md": [
            path
            for path in rel_files("skills/academic-paper/templates")
            if not path.endswith("latex_article_template.tex")
        ],
        "bundles/academic-paper/examples.md": rel_files(
            "skills/academic-paper/examples"
        ),
        "bundles/reviewer/agents-panel.md": prefixed(
            "skills/academic-paper-reviewer/agents", REVIEWER_PANEL
        ),
        "bundles/reviewer/agents-editorial.md": complement(
            "skills/academic-paper-reviewer/agents", REVIEWER_PANEL
        ),
        "bundles/reviewer/references.md": rel_files(
            "skills/academic-paper-reviewer/references"
        ),
        "bundles/reviewer/assets.md": (
            rel_files("skills/academic-paper-reviewer/templates")
            + rel_files("skills/academic-paper-reviewer/examples")
        ),
        "bundles/pipeline/agents-orchestration.md": prefixed(
            "skills/academic-pipeline/agents", PIPELINE_ORCHESTRATION
        ),
        "bundles/pipeline/agents-integrity-audit.md": complement(
            "skills/academic-pipeline/agents", PIPELINE_ORCHESTRATION
        ),
        "bundles/pipeline/references-state-handoff.md": prefixed(
            "skills/academic-pipeline/references", PIPELINE_STATE_REFS
        ),
        "bundles/pipeline/references-integrity-review.md": prefixed(
            "skills/academic-pipeline/references", PIPELINE_INTEGRITY_REFS
        ),
        "bundles/pipeline/summary-assets.md": (
            rel_files("skills/academic-pipeline/templates")
            + rel_files("skills/academic-pipeline/examples")
        ),
        "bundles/deep-research/agents-retrieval.md": prefixed(
            "skills/deep-research/agents", DEEP_RETRIEVAL
        ),
        "bundles/deep-research/agents-synthesis.md": prefixed(
            "skills/deep-research/agents", DEEP_SYNTHESIS
        ),
        "bundles/deep-research/agents-review.md": complement(
            "skills/deep-research/agents", DEEP_RETRIEVAL + DEEP_SYNTHESIS
        ),
        "bundles/deep-research/references-systematic.md": prefixed(
            "skills/deep-research/references", DEEP_SYSTEMATIC_REFS
        ),
        "bundles/deep-research/references-foundations.md": complement(
            "skills/deep-research/references", DEEP_SYSTEMATIC_REFS
        ),
        "bundles/deep-research/assets.md": (
            rel_files("skills/deep-research/templates")
            + rel_files("skills/deep-research/examples")
        ),
        "shared/protocols-core.md": [
            "shared/artifact_reproducibility_pattern.md",
            "shared/benchmark_report_pattern.md",
            "shared/collaboration_depth_rubric.md",
            "shared/ground_truth_isolation_pattern.md",
            "shared/mode_spectrum.md",
            "shared/raise_framework.md",
            "shared/style_calibration_protocol.md",
        ],
        "shared/protocols-compliance.md": [
            "shared/agents/compliance_agent.md",
            "shared/compliance_checkpoint_protocol.md",
            "shared/prisma_trAIce_protocol.md",
            "shared/policy_data/nature_policy.md",
        ],
        "shared/handoff-schemas.md": ["shared/handoff_schemas.md"],
        "shared/references-tools.md": [
            "shared/cross_model_verification.md",
            "shared/contracts/README.md",
            *rel_files("shared/references"),
            "shared/templates/codex_audit_multifile_template.md",
        ],
        "shared/schemas-core.md": [
            "shared/benchmark_report.schema.json",
            "shared/compliance_report.schema.json",
            "shared/sprint_contract.schema.json",
        ],
        "shared/schemas-passport-audit.md": (
            rel_files("shared/contracts/audit")
            + rel_files("shared/contracts/passport")
        ),
    }
    direct = {
        "CLAUDE.md": ".claude/CLAUDE.md",
        "skills/academic-paper/SKILL.md": "skills/academic-paper/SKILL.md",
        "skills/academic-paper-reviewer/SKILL.md": "skills/academic-paper-reviewer/SKILL.md",
        "skills/academic-pipeline/SKILL.md": "skills/academic-pipeline/SKILL.md",
        "skills/deep-research/SKILL.md": "skills/deep-research/SKILL.md",
        "bundles/academic-paper/latex_article_template.tex": (
            "skills/academic-paper/templates/latex_article_template.tex"
        ),
        "shared/contracts/reviewer/full.json": "shared/contracts/reviewer/full.json",
        "shared/contracts/reviewer/methodology_focus.json": (
            "shared/contracts/reviewer/methodology_focus.json"
        ),
        "shared/contracts/writer/full.json": "shared/contracts/writer/full.json",
        "shared/contracts/evaluator/full.json": "shared/contracts/evaluator/full.json",
    }
    return bundles, direct


def expected_outputs(bundles: dict[str, list[str]], direct: dict[str, str]) -> set[str]:
    return {
        "POWER.md",
        "CLAUDE.md",
        "LEGAL.md",
        "SOURCE-MANIFEST.md",
        *direct.keys(),
        *bundles.keys(),
    }


def validate_mapping(
    included_skill_shared: list[str],
    bundles: dict[str, list[str]],
    direct: dict[str, str],
) -> list[str]:
    expected_sources = sorted(
        [
            *included_skill_shared,
            ".claude/CLAUDE.md",
            "LICENSE",
            "NOTICE.md",
            *RUNTIME_SOURCES,
        ]
    )
    assigned = [source for sources in bundles.values() for source in sources]
    assigned.extend(direct.values())
    counts = Counter(assigned)
    duplicates = sorted(source for source, count in counts.items() if count != 1)
    missing = sorted(set(expected_sources) - set(assigned))
    unexpected = sorted(set(assigned) - set(expected_sources))
    if duplicates or missing or unexpected or len(assigned) != INCLUDED_SOURCE_COUNT:
        raise RuntimeError(
            "invalid source mapping: "
            f"assigned={len(assigned)}, duplicates={duplicates}, "
            f"missing={missing}, unexpected={unexpected}"
        )
    outputs = expected_outputs(bundles, direct)
    if len(outputs) != OUTPUT_FILE_COUNT:
        raise RuntimeError(
            f"expected exact {OUTPUT_FILE_COUNT}-file layout, mapping yields {len(outputs)}"
        )
    return expected_sources


def resolve_skill_reference(source: str, reference: str) -> str:
    """Resolve a skill-document path using the runtime POWER rules."""
    parts = source.split("/")
    if len(parts) < 3 or parts[0] != "skills" or parts[1] not in SKILLS:
        raise RuntimeError(f"not a skill source: {source}")
    selected_skill = parts[1]
    if reference.startswith(("./", "../")):
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), reference))
    elif reference.startswith("skills/"):
        resolved = posixpath.normpath(reference)
    elif reference.split("/", 1)[0] in SKILLS:
        resolved = posixpath.normpath(f"skills/{reference}")
    else:
        resolved = posixpath.normpath(f"skills/{selected_skill}/{reference}")
    if resolved == ".." or resolved.startswith("../") or resolved.startswith("/"):
        raise RuntimeError(
            f"skill reference escapes the canonical repository root: {source}: {reference}"
        )
    return resolved


def verify_runtime_reachability(expected_sources: list[str]) -> dict[str, int]:
    """Require explicit runtime paths in every included skill source to be mapped.

    Placeholder and wildcard examples are intentionally ignored because they do not
    identify a real canonical file; the ignored count is reported by verification.
    """
    mapped_sources = set(expected_sources)
    extracted = 0
    resolved_count = 0
    ignored_placeholders = 0
    unresolved: list[str] = []
    for source in expected_sources:
        if not source.startswith("skills/"):
            continue
        text = (REPO / source).read_text(encoding="utf-8")
        for match in PATH_REFERENCE_RE.finditer(text):
            extracted += 1
            reference = match.group("path")
            if any(char in reference for char in PLACEHOLDER_CHARS):
                ignored_placeholders += 1
                continue
            resolved = resolve_skill_reference(source, reference)
            if resolved not in mapped_sources:
                unresolved.append(f"{source}: {reference} -> {resolved}")
            else:
                resolved_count += 1
    if unresolved:
        raise RuntimeError(
            "runtime skill references are absent from the 211-source mapping:\n- "
            + "\n- ".join(unresolved)
        )
    return {
        "runtime_references_extracted": extracted,
        "runtime_references_resolved": resolved_count,
        "runtime_reference_placeholders_or_wildcards_ignored": ignored_placeholders,
    }


def source_section(source: str) -> bytes:
    content = (REPO / source).read_bytes()
    anchor = anchor_for(source)
    header = (
        f'<a id="{anchor}"></a>\n\n'
        f"## SOURCE: {source}\n\n"
        f"<!-- SOURCE-CONTENT-BEGIN bytes={len(content)} -->\n"
    ).encode("utf-8")
    if source.endswith(".json"):
        payload = b"```json\n" + content
        if not content.endswith(b"\n"):
            payload += b"\n"
        payload += b"```\n"
    else:
        payload = content
        if not content.endswith(b"\n"):
            payload += b"\n"
    return header + payload + b"<!-- SOURCE-CONTENT-END -->\n"


def render_bundle(sources: list[str]) -> bytes:
    return b"\n".join(source_section(source) for source in sources)


def manifest_row(source: str, target: str, anchor: str) -> str:
    digest = sha256((REPO / source).read_bytes())
    anchor_cell = (
        "`whole-file`"
        if anchor == DIRECT_ANCHOR
        else f"[`{anchor}`]({target}#{anchor})"
    )
    return f"| `{source}` | `{target}` | {anchor_cell} | `{digest}` |"


def manifest_markdown(
    bundles: dict[str, list[str]], direct: dict[str, str]
) -> bytes:
    reverse: dict[str, tuple[str, str]] = {}
    for target, sources in bundles.items():
        for source in sources:
            reverse[source] = (target, anchor_for(source))
    for target, source in direct.items():
        reverse[source] = (target, DIRECT_ANCHOR)

    lines = [
        "# Compact Power Source Manifest",
        "",
        "This deterministic manifest maps every included canonical source to exactly one compact target. SHA-256 values are computed from the original source bytes before bundling.",
        "",
        f"- Canonical files under the four `skills/` trees plus `shared/`: **{SKILL_SHARED_RAW_COUNT}**",
        f"- Excluded empty source: `{EMPTY_EXCLUSION}`",
        f"- Included non-empty `skills/` + `shared/` sources: **{SKILL_SHARED_INCLUDED_COUNT}**",
        "- Additional included sources: `.claude/CLAUDE.md`, `LICENSE`, `NOTICE.md`, plus 10 load-bearing design/script sources preserved in the two `runtime/` bundles",
        f"- Total included canonical sources: **{INCLUDED_SOURCE_COUNT}**, each assigned exactly once",
        f"- Compact upload files: **{OUTPUT_FILE_COUNT}**, all plain UTF-8 text",
        "- Anchor value `whole-file` means the target is a byte-for-byte standalone copy and therefore contains no injected HTML anchor.",
        "",
        "| Original path | Target file | Anchor | SHA-256 |",
        "|---|---|---|---|",
    ]
    for source in sorted(reverse):
        target, anchor = reverse[source]
        lines.append(manifest_row(source, target, anchor))
    lines.append("")
    return "\n".join(lines).encode("utf-8")


def power_markdown() -> bytes:
    text = """---
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
"""
    return text.encode("utf-8")


def write_tree(
    root: Path, bundles: dict[str, list[str]], direct: dict[str, str]
) -> None:
    payloads: dict[str, bytes] = {
        "POWER.md": power_markdown(),
        "SOURCE-MANIFEST.md": manifest_markdown(bundles, direct),
    }
    payloads.update({target: render_bundle(sources) for target, sources in bundles.items()})
    payloads.update(
        {target: (REPO / source).read_bytes() for target, source in direct.items()}
    )
    for relative_path in sorted(payloads):
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payloads[relative_path])


def recover_section(target_bytes: bytes, source: str) -> bytes:
    anchor = anchor_for(source).encode("utf-8")
    heading = (
        b'<a id="' + anchor + b'"></a>\n\n## SOURCE: ' + source.encode("utf-8") + b"\n\n"
    )
    start = target_bytes.find(heading)
    if start < 0 or target_bytes.find(heading, start + 1) >= 0:
        raise RuntimeError(f"source heading missing or duplicated for {source}")
    begin = BEGIN_RE.match(target_bytes, start + len(heading))
    if not begin:
        raise RuntimeError(f"length marker missing for {source}")
    length = int(begin.group(1))
    payload_start = begin.end()
    if source.endswith(".json"):
        fence = b"```json\n"
        if target_bytes[payload_start : payload_start + len(fence)] != fence:
            raise RuntimeError(f"JSON fence missing for {source}")
        payload_start += len(fence)
    return target_bytes[payload_start : payload_start + length]


def parse_and_validate_frontmatter(power: bytes) -> dict[str, object]:
    text = power.decode("utf-8")
    if not text.startswith("---\n"):
        raise RuntimeError("POWER.md frontmatter is missing")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise RuntimeError("POWER.md frontmatter is unterminated")
    raw_fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.fullmatch(r"([A-Za-z][A-Za-z0-9]*):(?: (.*))?", line)
        if not match:
            raise RuntimeError(f"invalid POWER frontmatter line: {line!r}")
        key, raw_value = match.group(1), match.group(2) or ""
        if key in raw_fields:
            raise RuntimeError(f"duplicate POWER frontmatter field: {key}")
        raw_fields[key] = raw_value

    required_fields = {"name", "description", "displayName", "keywords"}
    if set(raw_fields) != required_fields:
        raise RuntimeError(
            f"POWER frontmatter fields differ: {sorted(raw_fields)}"
        )
    name = raw_fields["name"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise RuntimeError("POWER frontmatter name must be non-empty kebab-case")

    parsed: dict[str, object] = {"name": name}
    for key in ("description", "displayName"):
        try:
            value = json.loads(raw_fields[key])
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"POWER frontmatter {key} must be a JSON string") from exc
        if not isinstance(value, str) or not value.strip():
            raise RuntimeError(f"POWER frontmatter {key} must be a non-empty string")
        parsed[key] = value

    try:
        keywords = json.loads(raw_fields["keywords"])
    except json.JSONDecodeError as exc:
        raise RuntimeError("POWER frontmatter keywords must be a JSON string array") from exc
    if (
        not isinstance(keywords, list)
        or not keywords
        or not all(isinstance(keyword, str) and keyword for keyword in keywords)
    ):
        raise RuntimeError(
            "POWER frontmatter keywords must be a non-empty JSON string array"
        )
    parsed["keywords"] = keywords
    return parsed


def verify_tree(
    root: Path,
    expected_sources: list[str],
    bundles: dict[str, list[str]],
    direct: dict[str, str],
) -> dict[str, int | str]:
    paths = sorted(path for path in root.rglob("*") if path.is_file() or path.is_symlink())
    files = [path for path in paths if path.is_file()]
    symlinks = [path for path in paths if path.is_symlink()]
    relative_files = {path.relative_to(root).as_posix() for path in files}
    expected = expected_outputs(bundles, direct)
    if len(files) != OUTPUT_FILE_COUNT or relative_files != expected:
        raise RuntimeError(
            f"layout mismatch: files={len(files)}, missing={sorted(expected-relative_files)}, "
            f"unexpected={sorted(relative_files-expected)}"
        )
    if symlinks:
        raise RuntimeError(f"symlinks are forbidden: {symlinks}")

    empty: list[str] = []
    for path in files:
        data = path.read_bytes()
        if not data:
            empty.append(path.relative_to(root).as_posix())
        if b"\0" in data:
            raise RuntimeError(f"NUL byte in compact output: {path}")
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise RuntimeError(f"non-UTF-8 compact output: {path}") from exc
    if empty:
        raise RuntimeError(f"empty compact outputs: {empty}")

    recovered: dict[str, bytes] = {}
    for target, sources in bundles.items():
        target_bytes = (root / target).read_bytes()
        if target_bytes.count(b"## SOURCE: ") != len(sources):
            raise RuntimeError(f"SOURCE section count mismatch in {target}")
        for source in sources:
            recovered[source] = recover_section(target_bytes, source)
    for target, source in direct.items():
        recovered[source] = (root / target).read_bytes()

    if set(recovered) != set(expected_sources) or len(recovered) != INCLUDED_SOURCE_COUNT:
        raise RuntimeError(
            f"recovered source set does not match {INCLUDED_SOURCE_COUNT}-source inventory"
        )
    for source in expected_sources:
        original = (REPO / source).read_bytes()
        if recovered[source] != original:
            raise RuntimeError(f"byte recovery mismatch: {source}")

    for target, source in direct.items():
        if (root / target).read_bytes() != (REPO / source).read_bytes():
            raise RuntimeError(f"direct-copy mismatch: {source}")
    json_sources = [source for source in expected_sources if source.endswith(".json")]
    for source in json_sources:
        json.loads(recovered[source].decode("utf-8"))
    schema_sources = [source for source in json_sources if source.endswith(".schema.json")]
    for source in schema_sources:
        json.loads(recovered[source].decode("utf-8"))
    for frozen in FROZEN_CONTRACTS:
        if direct.get(frozen) != frozen:
            raise RuntimeError(f"frozen JSON contract is not an independent copy: {frozen}")
        json.loads((root / frozen).read_text(encoding="utf-8"))

    frontmatter = parse_and_validate_frontmatter((root / "POWER.md").read_bytes())

    manifest = (root / "SOURCE-MANIFEST.md").read_text(encoding="utf-8")
    manifest_rows = [line for line in manifest.splitlines() if line.startswith("| `")]
    expected_manifest: dict[str, tuple[str, str]] = {}
    for target, sources in bundles.items():
        for source in sources:
            expected_manifest[source] = (target, anchor_for(source))
    for target, source in direct.items():
        expected_manifest[source] = (target, DIRECT_ANCHOR)
    expected_rows = [
        manifest_row(source, *expected_manifest[source]) for source in expected_sources
    ]
    if manifest_rows != expected_rows:
        raise RuntimeError("manifest rows do not exactly match source/target/anchor/hash mapping")

    tree_hasher = hashlib.sha256()
    for path in files:
        relative = path.relative_to(root).as_posix().encode("utf-8")
        data = path.read_bytes()
        tree_hasher.update(len(relative).to_bytes(4, "big"))
        tree_hasher.update(relative)
        tree_hasher.update(len(data).to_bytes(8, "big"))
        tree_hasher.update(data)

    reachability = verify_runtime_reachability(expected_sources)

    result: dict[str, int | str] = {
        "output_files": len(files),
        "output_tree_sha256": tree_hasher.hexdigest(),
        "symlinks": len(symlinks),
        "empty_files": len(empty),
        "utf8_text_files": len(files),
        "canonical_skill_shared_files": SKILL_SHARED_RAW_COUNT,
        "excluded_empty_gitkeep": 1,
        "included_skill_shared_sources": SKILL_SHARED_INCLUDED_COUNT,
        "additional_sources": ADDITIONAL_SOURCE_COUNT,
        "included_sources": len(recovered),
        "byte_exact_recoveries": len(recovered),
        "json_sources_parsed": len(json_sources),
        "schema_json_sources_parsed": len(schema_sources),
        "frozen_json_parsed_independently": len(FROZEN_CONTRACTS),
        "power_frontmatter_fields": ",".join(sorted(frontmatter)),
    }
    result.update(reachability)
    return result


def build() -> dict[str, int | str]:
    _, included_skill_shared = canonical_inventory()
    bundles, direct = source_mapping()
    expected_sources = validate_mapping(included_skill_shared, bundles, direct)
    temporary = Path(tempfile.mkdtemp(prefix=".kiro-power-compact.tmp-", dir=REPO))
    try:
        write_tree(temporary, bundles, direct)
        verification = verify_tree(temporary, expected_sources, bundles, direct)
        if OUTPUT.exists():
            shutil.rmtree(OUTPUT)
        temporary.replace(OUTPUT)
        return verification
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def check() -> dict[str, int | str]:
    _, included_skill_shared = canonical_inventory()
    bundles, direct = source_mapping()
    expected_sources = validate_mapping(included_skill_shared, bundles, direct)
    if not OUTPUT.is_dir():
        raise RuntimeError(f"compact output does not exist: {OUTPUT}")

    temporary = Path(tempfile.mkdtemp(prefix=".kiro-power-compact.check-", dir=REPO))
    try:
        write_tree(temporary, bundles, direct)
        verify_tree(temporary, expected_sources, bundles, direct)
        compared = 0
        for relative_path in sorted(expected_outputs(bundles, direct)):
            rendered_path = temporary / relative_path
            existing_path = OUTPUT / relative_path
            if not existing_path.is_file():
                raise RuntimeError(
                    f"rendered output is missing from existing tree: {relative_path}"
                )
            if rendered_path.read_bytes() != existing_path.read_bytes():
                raise RuntimeError(f"generated output drift: {relative_path}")
            compared += 1
        verification = verify_tree(OUTPUT, expected_sources, bundles, direct)
        verification["rendered_files_byte_compared"] = compared
        return verification
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="re-render, byte-compare, and verify the existing output without modifying it",
    )
    args = parser.parse_args()
    result = check() if args.check else build()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
