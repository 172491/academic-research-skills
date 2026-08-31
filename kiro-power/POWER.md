---
name: academic-research-skills
description: "Academic research pipeline — literature search and synthesis, paper drafting, simulated peer review, revision, and citation-provenance checking. Four skills covering research, writing, review, and end-to-end orchestration."
displayName: "Academic Research Skills"
keywords: ["academic", "research", "deep research", "paper", "academic paper", "academic writing", "literature review", "systematic review", "meta-analysis", "PRISMA", "peer review", "manuscript review", "referee report", "citation check", "abstract", "outline", "revision", "fact-check", "研究", "深度研究", "學術論文", "論文寫作", "文獻回顧", "系統性回顧", "後設分析", "同儕審查", "審查意見", "引註查核", "摘要"]
---

## Academic Research Skills

Four skills for academic work. Each one lives in `skills/<name>/SKILL.md` inside this power and is read on demand — the files are large (24–37 KB each, plus references), so read a skill only once the task clearly falls to it, and read only the reference files that skill actually names.

### Which skill handles what

- `skills/deep-research/SKILL.md` — research before there is a draft: forming the research question, literature search, source verification, cross-source synthesis, fact-checking, systematic review with optional meta-analysis. 7 modes.
- `skills/academic-paper/SKILL.md` — producing text: planning, outlining, drafting, abstracts, literature-review sections, revision against reviewer comments, citation checking, format conversion. 10 modes.
- `skills/academic-paper-reviewer/SKILL.md` — reviewing an existing manuscript through five simulated reviewer personas, ending in an editorial decision and a revision roadmap.
- `skills/academic-pipeline/SKILL.md` — orchestration only, for the full research → write → review → revise → finalize sequence. It detects the stage and dispatches the other three; it does no substantive work itself.

When the request names a single stage, go to that skill directly rather than through `academic-pipeline`.

### Resolving paths inside this power

The skill documents were written for a repository checkout, so they cite paths relative to the repository root. Inside this power those paths map as follows:

- `shared/<...>` → `shared/<...>` (unchanged)
- `.claude/CLAUDE.md` → `CLAUDE.md` at the root of this power
- `academic-paper/<...>`, `academic-paper-reviewer/<...>`, `academic-pipeline/<...>`, `deep-research/<...>` → `skills/<same path>`

Cross-skill references follow the same rule, so `academic-paper/references/writing_quality_check.md` is at `skills/academic-paper/references/writing_quality_check.md`.

### Source and license

This power is a repackaging of the `academic-research-skills` repository for Kiro's Power format. The skill trees under `skills/`, `shared/`, and `CLAUDE.md` are byte-identical copies of that repository, taken from commit `88a7ef7` of `172491/academic-research-skills`, itself a fork of `Imbad0202/academic-research-skills` by Cheng-I Wu. The work is licensed CC-BY-NC-4.0; `LICENSE` and `NOTICE.md` in the source repository carry the terms.

### Regenerating this folder after the source changes

The copies here do not update themselves. From a checkout of the source repository:

```
rm -rf kiro-power/skills kiro-power/shared
mkdir -p kiro-power/skills
for s in academic-paper academic-paper-reviewer academic-pipeline deep-research; do
  cp -rL "skills/$s" "kiro-power/skills/$s"
done
cp -rL shared kiro-power/shared
cp .claude/CLAUDE.md kiro-power/CLAUDE.md
cp plugin.json kiro-power/plugin.json
```

Then update the commit hash recorded above, and re-upload the folder in Settings > Powers.
