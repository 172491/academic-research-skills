<a id="source-shared-benchmark-report-schema-json"></a>

## SOURCE: shared/benchmark_report.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=2789 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/benchmark_report.schema.json",
  "title": "ARS Benchmark Report",
  "type": "object",
  "required": [
    "ars_version",
    "task_definition",
    "human_baseline",
    "ars_run",
    "metrics",
    "caveats"
  ],
  "properties": {
    "ars_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Exact ARS version the benchmark was run against"
    },
    "task_definition": {
      "type": "object",
      "required": ["description", "task_type", "outcome_gradable"],
      "properties": {
        "description": { "type": "string", "minLength": 1 },
        "task_type": { "enum": ["outcome-gradable", "open-ended"] },
        "outcome_gradable": { "type": "boolean" }
      }
    },
    "human_baseline": {
      "type": "object",
      "required": ["sample_size", "author_independence", "hours_spent", "recruitment", "tools_allowed"],
      "properties": {
        "sample_size": { "type": "integer", "minimum": 1 },
        "author_independence": {
          "enum": ["author-conducted", "author-blinded", "third-party-conducted"],
          "description": "author-conducted means the benchmark creators also did the human baseline (downward bias risk)"
        },
        "hours_spent": { "type": "number", "minimum": 0 },
        "recruitment": { "type": "string", "minLength": 1 },
        "tools_allowed": {
          "type": "array",
          "items": { "type": "string", "minLength": 1 },
          "minItems": 1
        }
      }
    },
    "ars_run": {
      "type": "object",
      "required": ["hours_spent", "cost_usd", "skills_used", "data_access_level_declared"],
      "properties": {
        "hours_spent": { "type": "number", "minimum": 0 },
        "cost_usd": { "type": "number", "minimum": 0 },
        "skills_used": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 1
        },
        "data_access_level_declared": {
          "enum": ["raw", "redacted", "verified_only"]
        }
      }
    },
    "metrics": {
      "type": "object",
      "required": ["primary_metric", "primary_metric_value", "scoring_independence"],
      "properties": {
        "primary_metric": { "type": "string", "minLength": 1 },
        "primary_metric_value": { "type": "number" },
        "scoring_independence": {
          "enum": ["authors-scored", "third-party-scored", "blind-scored", "self-scored"]
        }
      }
    },
    "caveats": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 },
      "minItems": 1,
      "description": "Known limitations. Empty array not permitted — honest disclosure required."
    }
  }
}
```
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-compliance-report-schema-json"></a>

## SOURCE: shared/compliance_report.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=8314 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/compliance_report.schema.json",
  "title": "ARS Compliance Report (Schema 12)",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "mode",
    "stage",
    "generated_at",
    "raise",
    "overall_decision",
    "user_action_required"
  ],
  "properties": {
    "mode": {
      "enum": ["systematic_review", "primary_research", "other_evidence_synthesis"]
    },
    "stage": { "enum": ["2.5", "4.5"] },
    "generated_at": { "type": "string", "format": "date-time" },
    "prisma_trAIce": {
      "oneOf": [
        { "type": "null" },
        {
          "type": "object",
          "additionalProperties": false,
          "required": ["items_total", "by_tier", "block_decision"],
          "properties": {
            "items_total": { "const": 17 },
            "by_tier": {
              "type": "object",
              "additionalProperties": false,
              "required": ["mandatory", "highly_recommended", "recommended", "optional"],
              "properties": {
                "mandatory": { "$ref": "#/$defs/tier_bucket" },
                "highly_recommended": { "$ref": "#/$defs/tier_bucket" },
                "recommended": { "$ref": "#/$defs/tier_bucket" },
                "optional": { "$ref": "#/$defs/tier_bucket" }
              }
            },
            "block_decision": { "$ref": "#/$defs/decision" },
            "protocol_maturity": { "$ref": "#/$defs/protocol_maturity" }
          }
        }
      ]
    },
    "raise": {
      "type": "object",
      "additionalProperties": false,
      "required": ["mode", "principles", "principle_evidence", "block_decision"],
      "properties": {
        "mode": { "enum": ["full", "principles_only"] },
        "principles": {
          "type": "object",
          "required": ["human_oversight", "transparency", "reproducibility", "fit_for_purpose"],
          "additionalProperties": false,
          "properties": {
            "human_oversight": { "$ref": "#/$defs/principle_status" },
            "transparency": { "$ref": "#/$defs/principle_status" },
            "reproducibility": { "$ref": "#/$defs/principle_status" },
            "fit_for_purpose": { "$ref": "#/$defs/principle_status" }
          }
        },
        "principle_evidence": {
          "type": "object",
          "required": ["human_oversight", "transparency", "reproducibility", "fit_for_purpose"],
          "additionalProperties": false,
          "properties": {
            "human_oversight": { "type": "array", "items": { "type": "string" } },
            "transparency": { "type": "array", "items": { "type": "string" } },
            "reproducibility": { "type": "array", "items": { "type": "string" } },
            "fit_for_purpose": { "type": "array", "items": { "type": "string" } }
          }
        },
        "roles": {
          "type": "object",
          "additionalProperties": false,
          "description": "Present only when raise.mode == 'full'; see top-level allOf constraint.",
          "properties": {
            "evidence_synthesists": { "type": "array", "items": { "type": "string" } },
            "ai_development_teams": { "type": "array", "items": { "type": "string" } },
            "methodologists": { "type": "array", "items": { "type": "string" } },
            "publishers": { "type": "array", "items": { "type": "string" } },
            "users": { "type": "array", "items": { "type": "string" } },
            "trainers": { "type": "array", "items": { "type": "string" } },
            "organisations": { "type": "array", "items": { "type": "string" } },
            "funders": { "type": "array", "items": { "type": "string" } }
          }
        },
        "block_decision": { "$ref": "#/$defs/decision" }
      }
    },
    "overall_decision": { "$ref": "#/$defs/decision" },
    "user_action_required": { "type": "boolean" },
    "evidence": { "type": "array", "items": { "type": "string" } },
    "user_override": {
      "type": "object",
      "additionalProperties": false,
      "required": ["decision", "timestamp", "rationale", "scope"],
      "properties": {
        "decision": { "const": true },
        "timestamp": { "type": "string", "format": "date-time" },
        "rationale": { "type": "string", "minLength": 1 },
        "scope": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "string",
            "pattern": "^(T1|A1|I1|M([1-9]|10)|R[12]|D[12]|human_oversight|transparency|reproducibility|fit_for_purpose)$"
          }
        }
      }
    },
    "upstream_sync_status": { "enum": ["current", "stale"] }
  },
  "allOf": [
    {
      "if": { "properties": { "mode": { "const": "systematic_review" } }, "required": ["mode"] },
      "then": { "properties": { "prisma_trAIce": { "type": "object" } } }
    },
    {
      "if": { "properties": { "mode": { "const": "primary_research" } }, "required": ["mode"] },
      "then": { "properties": { "prisma_trAIce": { "type": "null" } } }
    },
    {
      "if": {
        "properties": { "raise": { "properties": { "mode": { "const": "full" } }, "required": ["mode"] } },
        "required": ["raise"]
      },
      "then": { "properties": { "raise": { "required": ["roles"] } } }
    }
  ],
  "$defs": {
    "decision": { "enum": ["block", "warn", "pass"] },
    "principle_status": { "enum": ["pass", "warn", "fail"] },
    "protocol_maturity": {
      "description": "Optional maturity-disclosure context for the PRISMA-trAIce protocol authority backing this report. Populated by compliance_agent from shared/prisma_trAIce_protocol.md: frontmatter `citation` and `snapshot_date` are the deterministic source for upstream_citation and snapshot_date; `status` is derived from the protocol authors' self-description (currently foundational_proposal per Holst et al. 2025); `caveat_summary` is composed from the protocol's framing (issue #93 / PR #94 add a `§ Status disclaimer` section as the canonical prose source — until that PR lands, agents derive the summary from the Holst 2025 framing). See handoff_schemas.md § Schema 12 and issue #95 for the contract narrative.",
      "type": "object",
      "additionalProperties": false,
      "required": ["status", "upstream_citation", "snapshot_date", "caveat_summary"],
      "properties": {
        "status": {
          "description": "Authors' self-described maturity stage. 'foundational_proposal' = pre-Delphi, immediately-adoptable-but-unvalidated (current Holst et al. 2025 status). 'delphi_consensus' = post-formal-consensus. 'empirically_validated' = items validated across diverse research contexts.",
          "enum": ["foundational_proposal", "delphi_consensus", "empirically_validated"]
        },
        "upstream_citation": {
          "description": "Citation string matching shared/prisma_trAIce_protocol.md frontmatter `citation` field.",
          "type": "string",
          "minLength": 1
        },
        "snapshot_date": {
          "description": "ISO 8601 date of the protocol snapshot consulted; matches shared/prisma_trAIce_protocol.md frontmatter `snapshot_date`.",
          "type": "string",
          "format": "date"
        },
        "caveat_summary": {
          "description": "One-paragraph summary of the maturity caveat, suitable for inclusion in the block message and the AI Self-Reflection Report compliance summary.",
          "type": "string",
          "minLength": 1
        }
      }
    },
    "tier_bucket": {
      "type": "object",
      "additionalProperties": false,
      "required": ["total", "pass", "fail"],
      "properties": {
        "total": { "type": "integer", "minimum": 0 },
        "pass": { "type": "integer", "minimum": 0 },
        "fail": { "type": "array", "items": { "type": "string" } },
        "gaps": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["item_id", "reason"],
            "properties": {
              "item_id": { "type": "string" },
              "reason": { "type": "string" },
              "evidence_path": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
```
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-sprint-contract-schema-json"></a>

## SOURCE: shared/sprint_contract.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=18954 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/sprint_contract.schema.json",
  "title": "ARS Sprint Contract (Schema 13.1)",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "contract_id",
    "mode",
    "stage",
    "baseline_version",
    "acceptance_dimensions",
    "failure_conditions"
  ],
  "$comment": "Schema 13.1 (v3.6.6) lifts measurement_procedure and panel_size out of top-level required into reviewer-conditional gates (allOf branches 3 + 10). The base required list therefore drops those two compared to Schema 13. measurement_procedure is re-required for reviewer modes via allOf branch 3; panel_size is re-required for reviewer modes via allOf branch 10. Writer / evaluator contracts do not carry either field.",
  "properties": {
    "contract_id": {
      "type": "string",
      "pattern": "^[a-z_]+/[a-z_]+/v\\d+$"
    },
    "mode": {
      "enum": [
        "reviewer_full",
        "reviewer_methodology_focus",
        "reviewer_re_review",
        "reviewer_calibration",
        "reviewer_guided",
        "writer_full",
        "evaluator_full"
      ]
    },
    "stage": { "type": "string", "minLength": 1 },
    "baseline_version": {
      "type": "string",
      "pattern": "^v\\d+\\.\\d+\\.\\d+$"
    },
    "panel_size": { "type": "integer", "minimum": 1 },
    "acceptance_dimensions": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "name", "description", "priority"],
        "properties": {
          "id": { "type": "string", "pattern": "^D[1-9][0-9]?$" },
          "name": { "type": "string", "pattern": "^[a-z][a-z0-9_]*$" },
          "description": { "type": "string", "minLength": 1 },
          "priority": { "$ref": "#/$defs/priority" }
        }
      }
    },
    "measurement_procedure": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "reviewer_must_output_before_paper",
        "scoring_plan_schema",
        "paraphrase_minimum_dimensions"
      ],
      "properties": {
        "reviewer_must_output_before_paper": {
          "type": "array",
          "minItems": 2,
          "items": { "type": "string", "minLength": 1 }
        },
        "scoring_plan_schema": {
          "type": "object",
          "additionalProperties": false,
          "required": ["required"],
          "properties": {
            "required": {
              "type": "array",
              "minItems": 4,
              "uniqueItems": true,
              "items": {
                "enum": [
                  "dimension_id",
                  "what_to_look_for",
                  "what_triggers_block",
                  "what_triggers_warn"
                ]
              },
              "$comment": "Codex P2-2: the four canonical Phase-1 fields are fixed by sprint_contract_protocol.md §4. minItems:4 + uniqueItems:true + enum-constrained items rejects empty lists, partial lists, and typoed entries (e.g. what_trigger_block) at CI time instead of letting them fail at runtime as Phase-1 lint."
            }
          }
        },
        "paraphrase_minimum_dimensions": {
          "anyOf": [
            { "const": "all" },
            { "type": "integer", "minimum": 1 }
          ]
        }
      }
    },
    "pre_commitment_artifacts": {
      "type": "object",
      "additionalProperties": false,
      "required": ["acceptance_criteria_paraphrase"],
      "$comment": "Schema 13.1 v3.6.6 §3.4.1 (writer-only). Carries only invariant, paper-agnostic policy: how many acceptance_dimensions the writer must paraphrase in Phase 4a paper-blind output. Everything paper-specific lives in upstream runtime artefacts and is read at Phase 4a / 4b runtime, not committed in the frozen contract baseline. Per-section word counts come from the Paper Configuration Record (intake_agent); section outline comes from the Structure Architect's approved outline (structure_architect_agent); CER chains come from the Argument Blueprint (argument_builder_agent). Writer dimensions D1 (section_completeness), D3 (argument_blueprint_fidelity), D4 (total_word_count), D5 (per_section_word_count) phrase their gates against those upstream artefacts rather than against contract-embedded values. Required for writer_full only (allOf branch 11).",
      "properties": {
        "acceptance_criteria_paraphrase": {
          "type": "object",
          "additionalProperties": false,
          "required": ["minimum_dimensions"],
          "$comment": "CONFIGURATION declaration, not the paraphrase content itself. Declares how many of the contract's acceptance_dimensions the writer must paraphrase in Phase 4a. The actual paraphrase text is a runtime artifact emitted by draft_writer_agent in its Phase 4a output (analogous to how reviewer paraphrase content lives in <phase1_output>, not in the contract). Mirrors reviewer measurement_procedure.paraphrase_minimum_dimensions semantics.",
          "properties": {
            "minimum_dimensions": {
              "anyOf": [
                { "const": "all" },
                { "type": "integer", "minimum": 1 }
              ],
              "$comment": "Default in shipped writer template: 'all'."
            }
          }
        }
      }
    },
    "disagreement_handling": {
      "type": "object",
      "additionalProperties": false,
      "required": ["paraphrase_minimum_dimensions", "scoring_plan", "pre_commitment_check_protocol", "disagreement_resolution"],
      "$comment": "Schema 13.1 v3.6.6 §3.4.2 (evaluator-only). Required for evaluator_full only (allOf branch 12).",
      "properties": {
        "paraphrase_minimum_dimensions": {
          "anyOf": [
            { "const": "all" },
            { "type": "integer", "minimum": 1 }
          ],
          "$comment": "How many of the contract's acceptance_dimensions the evaluator must paraphrase in Phase 6a paper-blind output (the contract_paraphrase artifact named in §1 design goal 2 / §4.3). Mirrors reviewer measurement_procedure.paraphrase_minimum_dimensions and writer pre_commitment_artifacts.acceptance_criteria_paraphrase.minimum_dimensions to keep the Phase-6a anti-drift gate hard-required at the schema layer rather than relying on prose-level commitments. Default in shipped evaluator template: 'all'."
        },
        "scoring_plan": {
          "type": "object",
          "additionalProperties": false,
          "required": ["per_dimension_criteria"],
          "properties": {
            "per_dimension_criteria": {
              "type": "array",
              "minItems": 1,
              "items": {
                "type": "object",
                "additionalProperties": false,
                "required": ["dimension_id", "what_to_look_for", "what_triggers_block", "what_triggers_warn"],
                "properties": {
                  "dimension_id": { "type": "string", "pattern": "^D[1-9][0-9]?$" },
                  "what_to_look_for": { "type": "string", "minLength": 1 },
                  "what_triggers_block": { "type": "string", "minLength": 1 },
                  "what_triggers_warn": { "type": "string", "minLength": 1 }
                },
                "$comment": "Mirrors reviewer measurement_procedure.scoring_plan_schema four-field structure. Evaluator commits these in Phase 6a paper-blind."
              }
            }
          }
        },
        "pre_commitment_check_protocol": {
          "type": "object",
          "additionalProperties": false,
          "required": ["check_writer_artifact"],
          "properties": {
            "check_writer_artifact": {
              "const": "pre_commitment_artifacts",
              "$comment": "Pinned to the single writer source for v3.6.6. Field shape exists (rather than inlining the const) for forward compatibility — when v3.6.7+ may add additional writer artifacts, this can relax to an enum without a breaking schema change."
            }
          }
        },
        "disagreement_resolution": {
          "type": "object",
          "additionalProperties": false,
          "required": ["on_dimension_disagreement", "on_structural_drift"],
          "$comment": "Both subfield enums use the fully-qualified evaluator_decision=* vocabulary so values can be passed directly into failure_conditions[].action without runtime transformation. Keeping a single canonical action vocabulary across §3.3.3 and §3.4.2 prevents drift between the two surfaces.",
          "properties": {
            "on_dimension_disagreement": {
              "enum": [
                "evaluator_decision=request_revision",
                "evaluator_decision=accept_with_dissent_note",
                "evaluator_decision=flag_for_reviewer_stage"
              ],
              "$comment": "What the evaluator does when its own paper-blind scoring plan flags a dimension during paper-visible evaluation (the dimension hits its pre-committed what_triggers_block or what_triggers_warn anchors). Default in shipped templates: 'evaluator_decision=request_revision' for mandatory dimensions; runtime evaluator may downgrade non-mandatory dimensions to 'accept_with_dissent_note' (see F4 in evaluator/full.json)."
            },
            "on_structural_drift": {
              "enum": [
                "evaluator_decision=request_revision",
                "evaluator_decision=accept_with_dissent_note",
                "evaluator_decision=flag_for_reviewer_stage"
              ],
              "$comment": "What the evaluator does when the actual draft structure deviates from the Structure Architect's approved outline (the upstream runtime artefact from structure_architect_agent that the writer follows in Phase 4b). Drift threshold lives in the evaluator's runtime judgement, not the schema; the contract carries only the default verdict to apply when drift is observed."
            }
          }
        }
      }
    },
    "failure_conditions": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["condition_id", "severity", "expression", "action"],
        "properties": {
          "condition_id": {
            "type": "string",
            "pattern": "^F(0|[1-9][0-9]?)$",
            "$comment": "F0 reserved for accept-grade conditions per shipped templates §6.1+§6.2; spec §3.2 line 174 mistakenly writes ^F[1-9][0-9]?$ — DO NOT 'align' the schema back. Leading-zero forms (F00, F01) rejected to keep ordinal-position tie-break (§3.2 severity precedence) unambiguous."
          },
          "severity": { "type": "integer", "minimum": 0, "maximum": 100 },
          "cross_reviewer_quantifier": { "enum": ["any", "majority", "all"] },
          "expression": { "type": "string", "minLength": 1 },
          "action": {
            "type": "string",
            "$comment": "Schema 13.1 v3.6.6 §3.3.3: base enum lifted; mode-conditional action enums enforced in allOf branches 4 (reviewer) / 5 (writer_full) / 6 (evaluator_full). The base property keeps only type:string as a structural placeholder so JSON Schema's intersection semantics do not block writer / evaluator action values."
          }
        }
      }
    },
    "override_ladder": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["round", "trigger", "required"],
        "properties": {
          "round": { "type": "integer", "enum": [1, 2, 3] },
          "trigger": { "type": "string", "minLength": 1 },
          "required": {
            "type": "array",
            "items": { "type": "string", "minLength": 1 }
          }
        }
      }
    },
    "agent_amendments": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "stage_specific_notes": { "type": "string", "maxLength": 500 },
        "additional_measurement_hints": {
          "type": "array",
          "items": { "type": "string", "minLength": 1 }
        }
      }
    },
    "generated_at": { "type": "string", "format": "date-time" }
  },
  "allOf": [
    {
      "$comment": "Branch 1 (existing Schema 13 §3.3): reviewer mode requires cross_reviewer_quantifier on every failure_conditions entry.",
      "if": {
        "properties": { "mode": { "pattern": "^reviewer_" } },
        "required": ["mode"]
      },
      "then": {
        "properties": {
          "failure_conditions": {
            "items": { "required": ["cross_reviewer_quantifier"] }
          }
        }
      }
    },
    {
      "$comment": "Branch 2 (existing Schema 13 §3.3): override_ladder three-round shape if present.",
      "if": { "required": ["override_ladder"] },
      "then": {
        "properties": {
          "override_ladder": {
            "minItems": 3,
            "maxItems": 3,
            "prefixItems": [
              { "properties": { "round": { "const": 1 } } },
              { "properties": { "round": { "const": 2 } } },
              { "properties": { "round": { "const": 3 } } }
            ]
          }
        }
      }
    },
    {
      "$comment": "Branch 3 (new v3.6.6 §3.3.1): reviewer mode requires measurement_procedure (lifted from base required).",
      "if": {
        "properties": { "mode": { "pattern": "^reviewer_" } },
        "required": ["mode"]
      },
      "then": {
        "required": ["measurement_procedure"]
      }
    },
    {
      "$comment": "Branch 4 (new v3.6.6 §3.3.3): reviewer mode pins failure_conditions[].action to editorial_decision=* enum (re-pins the Schema 13 base enum; structurally identical for reviewer contracts).",
      "if": {
        "properties": { "mode": { "pattern": "^reviewer_" } },
        "required": ["mode"]
      },
      "then": {
        "properties": {
          "failure_conditions": {
            "items": {
              "properties": {
                "action": {
                  "enum": [
                    "editorial_decision=accept",
                    "editorial_decision=minor_revision",
                    "editorial_decision=major_revision",
                    "editorial_decision=reject_or_major_revision",
                    "editorial_decision=reject"
                  ]
                }
              }
            }
          }
        }
      }
    },
    {
      "$comment": "Branch 5 (new v3.6.6 §3.3.3): writer_full pins failure_conditions[].action to writer_decision=* enum.",
      "if": {
        "properties": { "mode": { "const": "writer_full" } },
        "required": ["mode"]
      },
      "then": {
        "properties": {
          "failure_conditions": {
            "items": {
              "properties": {
                "action": {
                  "enum": [
                    "writer_decision=accept",
                    "writer_decision=revise_in_phase_4b",
                    "writer_decision=escalate_to_evaluator"
                  ]
                }
              }
            }
          }
        }
      }
    },
    {
      "$comment": "Branch 6 (new v3.6.6 §3.3.3): evaluator_full pins failure_conditions[].action to evaluator_decision=* enum.",
      "if": {
        "properties": { "mode": { "const": "evaluator_full" } },
        "required": ["mode"]
      },
      "then": {
        "properties": {
          "failure_conditions": {
            "items": {
              "properties": {
                "action": {
                  "enum": [
                    "evaluator_decision=accept",
                    "evaluator_decision=accept_with_dissent_note",
                    "evaluator_decision=request_revision",
                    "evaluator_decision=flag_for_reviewer_stage"
                  ]
                }
              }
            }
          }
        }
      }
    },
    {
      "$comment": "Branch 7 (new v3.6.6 §3.3.4): reviewer mode F0 contains action=editorial_decision=accept (re-pins the Schema 13 inline contains; structurally identical for reviewer contracts).",
      "if": {
        "properties": { "mode": { "pattern": "^reviewer_" } },
        "required": ["mode"]
      },
      "then": {
        "properties": {
          "failure_conditions": {
            "contains": {
              "type": "object",
              "properties": {
                "condition_id": { "const": "F0" },
                "action": { "const": "editorial_decision=accept" }
              },
              "required": ["condition_id", "action"]
            }
          }
        }
      }
    },
    {
      "$comment": "Branch 8 (new v3.6.6 §3.3.4): writer_full F0 contains action=writer_decision=accept.",
      "if": {
        "properties": { "mode": { "const": "writer_full" } },
        "required": ["mode"]
      },
      "then": {
        "properties": {
          "failure_conditions": {
            "contains": {
              "type": "object",
              "properties": {
                "condition_id": { "const": "F0" },
                "action": { "const": "writer_decision=accept" }
              },
              "required": ["condition_id", "action"]
            }
          }
        }
      }
    },
    {
      "$comment": "Branch 9 (new v3.6.6 §3.3.4): evaluator_full F0 contains action=evaluator_decision=accept.",
      "if": {
        "properties": { "mode": { "const": "evaluator_full" } },
        "required": ["mode"]
      },
      "then": {
        "properties": {
          "failure_conditions": {
            "contains": {
              "type": "object",
              "properties": {
                "condition_id": { "const": "F0" },
                "action": { "const": "evaluator_decision=accept" }
              },
              "required": ["condition_id", "action"]
            }
          }
        }
      }
    },
    {
      "$comment": "Branch 10 (new v3.6.6 §3.3.5): reviewer mode requires panel_size (lifted from base required).",
      "if": {
        "properties": { "mode": { "pattern": "^reviewer_" } },
        "required": ["mode"]
      },
      "then": {
        "required": ["panel_size"]
      }
    },
    {
      "$comment": "Branch 11 (new v3.6.6 §3.5): writer_full requires pre_commitment_artifacts.",
      "if": {
        "properties": { "mode": { "const": "writer_full" } },
        "required": ["mode"]
      },
      "then": {
        "required": ["pre_commitment_artifacts"]
      }
    },
    {
      "$comment": "Branch 12 (new v3.6.6 §3.5): evaluator_full requires disagreement_handling.",
      "if": {
        "properties": { "mode": { "const": "evaluator_full" } },
        "required": ["mode"]
      },
      "then": {
        "required": ["disagreement_handling"]
      }
    }
  ],
  "$defs": {
    "score": { "enum": ["block", "warn", "pass"] },
    "priority": { "enum": ["mandatory", "high", "normal"] }
  }
}
```
<!-- SOURCE-CONTENT-END -->
