<a id="source-shared-contracts-audit-audit-jsonl-schema-json"></a>

## SOURCE: shared/contracts/audit/audit_jsonl.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=5518 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/audit/audit_jsonl.schema.json",
  "title": "Codex Audit JSONL Event",
  "description": "Schema for one row of the codex CLI 0.125+ --json event stream produced by scripts/run_codex_audit.sh (verified compatible across 0.125 through 0.128). Each JSONL line in <run_id>.jsonl validates against this schema. This is the Layer 2 anti-fake-audit check (§3.3): orchestrator validates the JSONL row-by-row before reading any verdict. Stream-level rules (first event must be thread.started; clean run ends with turn.completed; exactly one item.completed.agent_message carries the verdict text) live in scripts/check_audit_artifact_consistency.py (Phase 6.3), NOT in this schema. Codex 0.125 retired pre-0.125 fields (model, reasoning_effort, session_id, final_message, per-row usage); see §3.3 'Codex 0.125+ --json event-stream shape' for the load-bearing shape contract. NOTE: item.started events appear in tool-using runs (command_execution start, etc.) and are accepted here even though spec §3.3's enumerated four-event canonical run did not list them — empirical capture from codex 0.125+ confirms they precede every item.completed of types other than agent_message.",

  "type": "object",
  "required": ["type"],
  "properties": {
    "type": {
      "type": "string",
      "enum": ["thread.started", "turn.started", "item.started", "item.completed", "turn.completed", "error"]
    }
  },

  "oneOf": [
    {
      "title": "thread.started",
      "type": "object",
      "additionalProperties": false,
      "required": ["type", "thread_id"],
      "properties": {
        "type": { "const": "thread.started" },
        "thread_id": {
          "type": "string",
          "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
          "description": "Canonical UUID (8-4-4-4-12 hex layout) identifying this codex run. Per §3.3, codex emits this once at stream open; downstream events SHOULD NOT redeclare it. Tight pattern blocks Layer 2 forgery via 36-char garbage like '------------------------------------'."
        }
      }
    },
    {
      "title": "turn.started",
      "type": "object",
      "additionalProperties": false,
      "required": ["type"],
      "properties": {
        "type": { "const": "turn.started" }
      }
    },
    {
      "title": "item.started",
      "description": "Emitted in tool-using runs (e.g., command_execution begin) before the matching item.completed event. Carries no text yet — the completed event holds the result. Verdict logic only reads agent_message item.completed events; item.started rows are evidence that codex actually invoked tools. Closed against unknown top-level fields to match the rest of the event arms; per-tool fields belong inside `item`, not at the row root.",
      "type": "object",
      "additionalProperties": false,
      "required": ["type", "item"],
      "properties": {
        "type": { "const": "item.started" },
        "item": {
          "type": "object",
          "required": ["id", "type"],
          "properties": {
            "id": { "type": "string", "minLength": 1 },
            "type": { "type": "string", "minLength": 1 }
          }
        }
      }
    },
    {
      "title": "item.completed",
      "type": "object",
      "additionalProperties": false,
      "required": ["type", "item"],
      "properties": {
        "type": { "const": "item.completed" },
        "item": {
          "type": "object",
          "required": ["id", "type"],
          "properties": {
            "id": { "type": "string", "minLength": 1 },
            "type": { "type": "string", "minLength": 1 },
            "text": { "type": "string" }
          },
          "allOf": [
            {
              "description": "When item.type == 'agent_message', item.text is required and non-empty (§3.3 table row 'item.completed').",
              "if": {
                "properties": { "type": { "const": "agent_message" } },
                "required": ["type"]
              },
              "then": {
                "required": ["text"],
                "properties": {
                  "text": { "type": "string", "minLength": 1 }
                }
              }
            }
          ]
        }
      }
    },
    {
      "title": "turn.completed",
      "type": "object",
      "additionalProperties": false,
      "required": ["type", "usage"],
      "properties": {
        "type": { "const": "turn.completed" },
        "usage": {
          "type": "object",
          "additionalProperties": false,
          "required": ["input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens"],
          "properties": {
            "input_tokens": { "type": "integer", "minimum": 0 },
            "cached_input_tokens": { "type": "integer", "minimum": 0 },
            "output_tokens": { "type": "integer", "minimum": 0 },
            "reasoning_output_tokens": { "type": "integer", "minimum": 0 }
          }
        }
      }
    },
    {
      "title": "error",
      "type": "object",
      "additionalProperties": false,
      "required": ["type", "error"],
      "properties": {
        "type": { "const": "error" },
        "error": {
          "type": "object",
          "required": ["message"],
          "properties": {
            "message": { "type": "string", "minLength": 1 }
          }
        }
      }
    }
  ]
}
```
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-contracts-audit-audit-sidecar-schema-json"></a>

## SOURCE: shared/contracts/audit/audit_sidecar.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=7149 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/audit/audit_sidecar.schema.json",
  "title": "Codex Audit Sidecar Metadata",
  "description": "Schema for <run_id>.meta.json — the Layer 3 anti-fake-audit evidence file produced by scripts/run_codex_audit.sh. Captures runner / timing / process / stream / prompt context for one audit run. Cross-file rules linking sidecar fields to JSONL events / on-disk files / passport entries (B1-B7 in §3.7 family B) are lint-enforced by scripts/check_audit_artifact_consistency.py (Phase 6.3); this schema only enforces the per-file shape. AUDIT_FAILED conditional: when the companion verdict's status == 'AUDIT_FAILED', the JSON Schema 'if/then' below relaxes stream.jsonl_thread_id to allow empty string (no usable JSONL thread exists when codex aborted).",

  "type": "object",
  "additionalProperties": false,

  "required": [
    "run_id",
    "codex_cli_version",
    "runner",
    "timing",
    "process",
    "stream",
    "prompt"
  ],

  "properties": {
    "run_id": {
      "$ref": "#/$defs/run_id",
      "description": "Canonical run identifier; equals file basename (§3.7 F3). Cross-file basename consistency (B7) is lint-enforced."
    },
    "codex_cli_version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$",
      "description": "Bare semver. Wrapper strips the 'codex-cli ' prefix from `codex --version` output before writing here (§4.4 _codex_version helper)."
    },
    "runner": {
      "type": "object",
      "additionalProperties": false,
      "required": ["hostname", "cwd", "git_sha", "git_dirty"],
      "properties": {
        "hostname": { "type": "string", "minLength": 1 },
        "cwd": { "type": "string", "minLength": 1 },
        "git_sha": {
          "type": "string",
          "pattern": "^[a-f0-9]{7,40}$",
          "description": "Repo HEAD at audit start (7-40 hex; not a full SHA-256). Lint (B4) verifies this resolves to a real commit."
        },
        "git_dirty": { "type": "boolean" }
      }
    },
    "timing": {
      "type": "object",
      "additionalProperties": false,
      "required": ["started_at", "ended_at", "duration_seconds"],
      "properties": {
        "started_at": {
          "$ref": "#/$defs/rfc3339_ms_utc",
          "description": "RFC 3339 UTC, millisecond precision."
        },
        "ended_at": {
          "$ref": "#/$defs/rfc3339_ms_utc"
        },
        "duration_seconds": {
          "type": "number",
          "exclusiveMinimum": 0,
          "description": "Lint (B5) verifies duration_seconds == ended_at - started_at within +/- 1s."
        }
      }
    },
    "process": {
      "type": "object",
      "additionalProperties": false,
      "required": ["exit_code", "stdout_path", "stderr_path"],
      "properties": {
        "exit_code": { "type": "integer" },
        "stdout_path": { "$ref": "#/$defs/repo_relative_path" },
        "stderr_path": { "$ref": "#/$defs/repo_relative_path" }
      }
    },
    "stream": {
      "type": "object",
      "additionalProperties": false,
      "required": ["jsonl_thread_id"],
      "properties": {
        "jsonl_thread_id": {
          "type": "string",
          "description": "UUID matching the JSONL stream's single thread.started event's thread_id (B1, lint-enforced cross-file). When the companion verdict's status == 'AUDIT_FAILED', empty string '' is accepted because no usable JSONL thread exists; UUID format constraint and B1 are both suspended for AUDIT_FAILED entries (§3.4)."
        }
      }
    },
    "prompt": {
      "type": "object",
      "additionalProperties": false,
      "required": ["audit_template_path", "audit_template_sha", "bundle"],
      "properties": {
        "audit_template_path": {
          "const": "shared/templates/codex_audit_multifile_template.md",
          "description": "v3.6.7 ships a single canonical audit template; the path is constant. Future versions that add additional templates will widen this to enum."
        },
        "audit_template_sha": { "$ref": "#/$defs/sha256_hex" },
        "bundle": {
          "type": "object",
          "additionalProperties": false,
          "required": ["bundle_manifest_sha", "primary_deliverables", "supporting_context"],
          "properties": {
            "bundle_id": { "type": "string", "minLength": 1 },
            "bundle_manifest_sha": { "$ref": "#/$defs/sha256_hex" },
            "primary_deliverables": {
              "type": "array",
              "minItems": 1,
              "items": { "$ref": "#/$defs/file_ref" }
            },
            "supporting_context": {
              "type": "array",
              "items": { "$ref": "#/$defs/file_ref" }
            }
          }
        }
      }
    }
  },

  "allOf": [
    {
      "description": "When the companion verdict's status is NOT AUDIT_FAILED, jsonl_thread_id MUST match canonical UUID (8-4-4-4-12 hex). When status == 'AUDIT_FAILED', empty string is also acceptable. Pattern mirrors audit/audit_jsonl.schema.json#thread_id — keep in sync. Co-validation with the verdict file is performed by Layer 3 lint (Phase 6.3); this schema enforces the format-or-empty discipline so a sidecar file alone (without verdict context) still rejects garbage values like '------------------------------------'.",
      "properties": {
        "stream": {
          "properties": {
            "jsonl_thread_id": {
              "anyOf": [
                { "type": "string", "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$" },
                { "type": "string", "const": "" }
              ]
            }
          }
        }
      }
    }
  ],

  "$defs": {
    "sha256_hex": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$",
      "description": "Lowercase hex SHA-256. Mirrored from passport/audit_artifact_entry.schema.json $defs.sha256_hex; keep regex in sync."
    },
    "run_id": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}Z-[0-9a-f]{4}$",
      "description": "Mirrored from passport/audit_artifact_entry.schema.json $defs.run_id; F1 in §3.7. Keep regex in sync."
    },
    "rfc3339_ms_utc": {
      "type": "string",
      "format": "date-time",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{3}Z$",
      "description": "RFC 3339 UTC with millisecond precision. Mirrored from passport/audit_artifact_entry.schema.json $defs.rfc3339_ms_utc."
    },
    "repo_relative_path": {
      "type": "string",
      "minLength": 1,
      "pattern": "^[^/][^\\s]*$",
      "not": { "pattern": "(^|/)\\.\\.(/|$)" },
      "description": "Repo-relative POSIX path. Mirrored from passport/audit_artifact_entry.schema.json $defs.repo_relative_path; keep regex pair in sync."
    },
    "file_ref": {
      "type": "object",
      "additionalProperties": false,
      "required": ["path", "sha"],
      "properties": {
        "path": { "$ref": "#/$defs/repo_relative_path" },
        "sha": { "$ref": "#/$defs/sha256_hex" }
      }
    }
  }
}
```
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-contracts-audit-audit-verdict-schema-json"></a>

## SOURCE: shared/contracts/audit/audit_verdict.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=5548 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/audit/audit_verdict.schema.json",
  "title": "Codex Audit Verdict File",
  "description": "Schema for <run_id>.verdict.yaml — the human-readable verdict file produced by the wrapper after parsing the JSONL stream's single item.completed.agent_message event (per §3.3 / §3.5). This is the policy surface the orchestrator reads for ship/block decisions; JSONL is raw evidence (Layer 2) and sidecar is environmental evidence (Layer 3). Cross-field invariants (PASS/MINOR/MATERIAL/AUDIT_FAILED count consistency; finding_counts agrees with findings[]) are lint-enforced in scripts/check_audit_artifact_consistency.py (Phase 6.3 §3.7 family A rows A1/A2/A5/A6) — this schema enforces the per-file shape so wrapper-side lint can reject malformed verdicts before they reach the orchestrator.",

  "type": "object",
  "additionalProperties": false,

  "required": [
    "run_id",
    "verdict_status",
    "round",
    "target_rounds",
    "finding_counts",
    "findings",
    "generated_at",
    "generated_by",
    "generator_version"
  ],

  "properties": {
    "run_id": { "$ref": "#/$defs/run_id" },
    "verdict_status": {
      "type": "string",
      "enum": ["PASS", "MINOR", "MATERIAL", "AUDIT_FAILED"],
      "description": "Three completion states + AUDIT_FAILED for wrapper-side aborts (§4.6). Cross-field consistency with finding_counts and failure_reason is lint-enforced (§3.7 A1/A2)."
    },
    "round": { "type": "integer", "minimum": 1 },
    "target_rounds": { "type": "integer", "minimum": 1 },
    "finding_counts": {
      "type": "object",
      "additionalProperties": false,
      "required": ["p1", "p2", "p3"],
      "properties": {
        "p1": { "type": "integer", "minimum": 0 },
        "p2": { "type": "integer", "minimum": 0 },
        "p3": { "type": "integer", "minimum": 0 }
      }
    },
    "findings": {
      "type": "array",
      "items": { "$ref": "#/$defs/finding" },
      "description": "May be []. When verdict_status == 'AUDIT_FAILED', findings MUST be [] (lint-enforced per §3.7 A6). When non-empty, finding_counts must agree with severity tallies (§3.7 A5, lint-enforced)."
    },
    "failure_reason": {
      "type": "string",
      "minLength": 1,
      "maxLength": 500,
      "pattern": "^[^\\n\\r]+$",
      "description": "One-line human-readable reason. Required iff verdict_status == 'AUDIT_FAILED' (§3.7 A2; lint-enforced)."
    },
    "generated_at": {
      "type": "string",
      "format": "date-time"
    },
    "generated_by": {
      "type": "string",
      "minLength": 1,
      "description": "Path to the wrapper script that produced this verdict (canonical: 'scripts/run_codex_audit.sh')."
    },
    "generator_version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$",
      "description": "Wrapper script semver."
    }
  },

  "allOf": [
    {
      "title": "[doc-only] round vs target_rounds — enforced by lint, not schema",
      "description": "JSON Schema 2020-12 has no native cross-field comparison; round <= target_rounds (§3.7 A3) is enforced by scripts/check_audit_artifact_consistency.py (Phase 6.3) and by the wrapper's --round/--target-rounds preflight (§4.2). This clause carries the comment so future readers don't try to add a non-existent schema-level constraint here."
    },
    {
      "description": "AUDIT_FAILED requires failure_reason. Lint additionally enforces findings == [] and finding_counts all zero per §3.7 A2/A6.",
      "if": {
        "properties": { "verdict_status": { "const": "AUDIT_FAILED" } },
        "required": ["verdict_status"]
      },
      "then": {
        "required": ["failure_reason"]
      }
    },
    {
      "description": "Non-AUDIT_FAILED verdicts MUST NOT carry failure_reason (§3.7 A2 inverse direction).",
      "if": {
        "properties": {
          "verdict_status": {
            "type": "string",
            "enum": ["PASS", "MINOR", "MATERIAL"]
          }
        },
        "required": ["verdict_status"]
      },
      "then": {
        "not": { "required": ["failure_reason"] }
      }
    }
  ],

  "$defs": {
    "run_id": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}Z-[0-9a-f]{4}$",
      "description": "Mirrored from passport/audit_artifact_entry.schema.json $defs.run_id; F1 in §3.7. Keep regex in sync."
    },
    "finding": {
      "type": "object",
      "additionalProperties": false,
      "required": ["id", "severity", "dimension", "file", "line", "description", "suggested_fix"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^F-[0-9]{3,}$",
          "description": "Stable per-verdict-file identifier (e.g., 'F-007'). acknowledgement.finding_ids cross-references these (§3.7 B10)."
        },
        "severity": {
          "type": "string",
          "enum": ["P1", "P2", "P3"]
        },
        "dimension": {
          "type": "string",
          "enum": ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "4(f)"],
          "description": "Audit template Section 3 dimension or '4(f)' for report_compiler_agent abstract-only checks."
        },
        "file": { "type": "string", "minLength": 1 },
        "line": { "type": "integer", "minimum": 1 },
        "description": { "type": "string", "minLength": 1 },
        "suggested_fix": { "type": "string", "minLength": 1 }
      }
    }
  }
}
```
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-contracts-passport-audit-artifact-entry-schema-json"></a>

## SOURCE: shared/contracts/passport/audit_artifact_entry.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=11059 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/audit_artifact_entry.schema.json",
  "title": "Material Passport Audit Artifact Entry",
  "description": "One entry in Material Passport Schema 9 audit_artifact[]. Records one cross-model audit run for one downstream agent's deliverable. Two lifecycle states share this schema via oneOf: 'proposal' (wrapper-emitted, pre-verification) and 'persisted' (orchestrator-merged, post-verification). See docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md §3.1-§3.2 and §3.7 for cross-artifact invariants. Cross-field rules (PASS/MINOR/MATERIAL/AUDIT_FAILED counts; acknowledgement scoping; etc.) are lint-enforced in scripts/check_audit_artifact_consistency.py (Phase 6.3), NOT in this schema.",

  "type": "object",
  "additionalProperties": false,

  "required": [
    "stage",
    "agent",
    "deliverable_path",
    "deliverable_sha",
    "run_id",
    "bundle_manifest_sha",
    "artifact_paths",
    "verdict"
  ],

  "properties": {
    "stage": {
      "type": "integer",
      "minimum": 1,
      "maximum": 6,
      "description": "Destination stage the just-completed deliverable is about to enter (per §5.1). v3.6.7 hooks emit stage 2 for synthesis_agent / research_architect_agent exits and stage 5 for report_compiler_agent exit."
    },
    "agent": {
      "type": "string",
      "enum": [
        "synthesis_agent",
        "research_architect_agent",
        "report_compiler_agent"
      ],
      "description": "One of the three v3.6.7 audited agents. Other agent names are reserved for future versions and rejected by Schema 9 lint."
    },
    "deliverable_path": {
      "$ref": "#/$defs/repo_relative_path",
      "description": "Repo-relative POSIX path to the audited deliverable. No leading '/' and no '..' segments."
    },
    "deliverable_sha": {
      "$ref": "#/$defs/sha256_hex",
      "description": "SHA-256 (lowercase hex) of the deliverable file at the moment audit was dispatched. Used by orchestrator to detect post-audit deliverable mutation."
    },
    "run_id": {
      "$ref": "#/$defs/run_id",
      "description": "Canonical run identifier emitted by the wrapper. Format <ISO-8601-Z>-<4-hex>. Per §3.7 family F (F1)."
    },
    "bundle_id": {
      "type": "string",
      "minLength": 1,
      "description": "Optional opaque tag shared by all entries that belong to one logical multi-file audit bundle (§4.5). When present MUST equal the sidecar's prompt.bundle.bundle_id (§3.7 B9, lint-enforced)."
    },
    "bundle_manifest_sha": {
      "$ref": "#/$defs/sha256_hex",
      "description": "SHA-256 over the canonical bundle manifest of primary + supporting + template files (§3.6)."
    },
    "artifact_paths": {
      "type": "object",
      "additionalProperties": false,
      "required": ["jsonl", "sidecar", "verdict"],
      "properties": {
        "jsonl": {
          "allOf": [
            { "$ref": "#/$defs/repo_relative_path" },
            { "type": "string", "pattern": "\\.jsonl$" }
          ]
        },
        "sidecar": {
          "allOf": [
            { "$ref": "#/$defs/repo_relative_path" },
            { "type": "string", "pattern": "\\.meta\\.json$" }
          ]
        },
        "verdict": {
          "allOf": [
            { "$ref": "#/$defs/repo_relative_path" },
            { "type": "string", "pattern": "\\.verdict\\.yaml$" }
          ]
        }
      },
      "description": "All three paths are repo-relative POSIX (no leading '/', no '..' segments). Path B uses these to locate JSONL/sidecar/verdict evidence; an absolute or escaping path would let a forged proposal point verification outside the repo."
    },
    "verdict": { "$ref": "#/$defs/verdict_block" },
    "acknowledgement": { "$ref": "#/$defs/acknowledgement_block" }
  },

  "allOf": [
    {
      "title": "[A2] AUDIT_FAILED requires verdict.failure_reason; mirrors audit_verdict.schema.json",
      "description": "Entry-side mirror of the verdict-file rule (§3.7 A2). Without this, a wrapper-emitted AUDIT_FAILED proposal missing failure_reason passes Path B4 schema validation; Path B5 then short-circuits and tries to surface a non-existent reason in the BLOCK message. Mirror keeps the rule enforceable at the first artifact orchestrator reads (entry), not just at the verdict file.",
      "if": {
        "properties": {
          "verdict": {
            "properties": { "status": { "const": "AUDIT_FAILED" } },
            "required": ["status"]
          }
        },
        "required": ["verdict"]
      },
      "then": {
        "properties": {
          "verdict": { "required": ["failure_reason"] }
        }
      }
    },
    {
      "title": "[A2 inverse] non-AUDIT_FAILED proposals MUST NOT carry failure_reason",
      "if": {
        "properties": {
          "verdict": {
            "properties": {
              "status": { "type": "string", "enum": ["PASS", "MINOR", "MATERIAL"] }
            },
            "required": ["status"]
          }
        },
        "required": ["verdict"]
      },
      "then": {
        "properties": {
          "verdict": { "not": { "required": ["failure_reason"] } }
        }
      }
    }
  ],

  "oneOf": [
    {
      "title": "proposal",
      "description": "Wrapper-emitted, pre-verification. verdict.verified_at and verdict.verified_by MUST be absent (Pattern C3 attack surface defense per §3.2 / §3.7 E3+E4). acknowledgement is forbidden — orchestrator-only write per §5.4 / §3.7 A4.",
      "not": { "required": ["acknowledgement"] },
      "properties": {
        "verdict": {
          "type": "object",
          "not": {
            "anyOf": [
              { "required": ["verified_at"] },
              { "required": ["verified_by"] }
            ]
          }
        }
      }
    },
    {
      "title": "persisted",
      "description": "Orchestrator-merged, post-verification. AUDIT_FAILED excluded — see §3.2 'Why persisted excludes AUDIT_FAILED' rationale. acknowledgement is allowed only on MATERIAL entries — schema-level if/then below blocks the hand-edit attack where someone adds an acknowledgement block to a non-MATERIAL persisted entry to claim residue acknowledgement that was never solicited (§3.7 A4).",
      "properties": {
        "verdict": {
          "type": "object",
          "required": ["verified_at", "verified_by"],
          "properties": {
            "status": { "enum": ["PASS", "MINOR", "MATERIAL"] },
            "verified_at": {
              "$ref": "#/$defs/rfc3339_ms_utc",
              "description": "RFC 3339 UTC datetime, millisecond precision (mirrors §3.4 sidecar timing precision so D1 latest-by-verified_at ordering has resolution >= 1 ms; see §5.4 monotonic-bump rule)."
            },
            "verified_by": {
              "const": "pipeline_orchestrator_agent"
            }
          }
        }
      },
      "allOf": [
        {
          "title": "[A4] acknowledgement requires verdict.status == MATERIAL",
          "if": {
            "properties": {
              "verdict": {
                "properties": { "status": { "enum": ["PASS", "MINOR"] } },
                "required": ["status"]
              }
            },
            "required": ["verdict"]
          },
          "then": {
            "not": { "required": ["acknowledgement"] }
          }
        }
      ]
    }
  ],

  "$defs": {
    "repo_relative_path": {
      "type": "string",
      "minLength": 1,
      "pattern": "^[^/][^\\s]*$",
      "not": { "pattern": "(^|/)\\.\\.(/|$)" },
      "description": "Repo-relative POSIX path (no leading '/', no '..' segments). Sibling audit/* schemas duplicate this pattern; keep the regex pair in sync. Layer 3 lint reads these paths from disk for SHA-256 / git_sha verification — accepting absolute or escaping paths would let a forged proposal hash arbitrary files."
    },
    "sha256_hex": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$",
      "description": "Lowercase hex SHA-256 digest. Sibling audit/* schemas duplicate this pattern (cross-file $ref is operationally awkward without a registry resolver); keep regex in sync via §3.7 family F naming-convention review."
    },
    "run_id": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}Z-[0-9a-f]{4}$",
      "description": "<ISO-8601-Z>-<4-hex>. F1 in §3.7 naming family. Sibling audit/* schemas duplicate this pattern."
    },
    "rfc3339_ms_utc": {
      "type": "string",
      "format": "date-time",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{3}Z$",
      "description": "RFC 3339 UTC datetime with millisecond precision. Format keyword is advisory (validator must enable format_checker); regex is the load-bearing constraint."
    },
    "verdict_block": {
      "type": "object",
      "additionalProperties": false,
      "required": ["status", "round", "target_rounds", "finding_counts"],
      "properties": {
        "status": {
          "type": "string",
          "enum": ["PASS", "MINOR", "MATERIAL", "AUDIT_FAILED"],
          "description": "Proposal-arm enum; persisted arm narrows to {PASS,MINOR,MATERIAL} via oneOf override (§3.2 Lifecycle-conditional fields)."
        },
        "failure_reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 500,
          "pattern": "^[^\\n\\r]+$",
          "description": "One-line human-readable reason. Required iff status == AUDIT_FAILED (cross-field rule, lint-enforced per §3.7 A2)."
        },
        "round": { "type": "integer", "minimum": 1 },
        "target_rounds": { "type": "integer", "minimum": 1 },
        "finding_counts": {
          "type": "object",
          "additionalProperties": false,
          "required": ["p1", "p2", "p3"],
          "properties": {
            "p1": { "type": "integer", "minimum": 0 },
            "p2": { "type": "integer", "minimum": 0 },
            "p3": { "type": "integer", "minimum": 0 }
          }
        },
        "verified_at": {
          "type": "string",
          "format": "date-time"
        },
        "verified_by": {
          "type": "string",
          "minLength": 1
        }
      }
    },
    "acknowledgement_block": {
      "type": "object",
      "additionalProperties": false,
      "required": ["finding_ids", "acknowledged_at", "acknowledged_by"],
      "properties": {
        "finding_ids": {
          "type": "array",
          "minItems": 1,
          "items": { "type": "string", "minLength": 1 },
          "description": "Non-empty array; full coverage of every current findings[].id is enforced by lint (§3.7 B10)."
        },
        "acknowledged_at": {
          "$ref": "#/$defs/rfc3339_ms_utc",
          "description": "RFC 3339 UTC, millisecond precision. Equals verdict.verified_at by construction (§3.7 B8)."
        },
        "acknowledged_by": { "const": "user" }
      }
    }
  }
}
```
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-contracts-passport-claim-audit-result-schema-json"></a>

## SOURCE: shared/contracts/passport/claim_audit_result.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=6963 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/claim_audit_result.schema.json",
  "title": "Material Passport Claim Audit Result Entry",
  "description": "One entry in Material Passport Schema 9 claim_audit_results[] aggregate. Per-claim audit result emitted by claim_ref_alignment_audit_agent (v3.8.0) after the Cite-Time Provenance Finalizer pass at the Stage 4 -> Stage 5 boundary. Cross-field invariants INV-1..INV-18 are lint-enforced in scripts/check_claim_audit_consistency.py — JSON Schema cannot express the conditional matrix relating (judgment, audit_status, defect_stage, ref_retrieval_method). Three sibling entry-types ride in their own aggregates because they cannot satisfy the required-field shape of this schema: uncited_assertion (no ref_slug; §3.3), claim_drift (no judge invocation; §3.4), constraint_violation (uncited HIGH-WARN; §3.5). See docs/design/2026-05-15-issue-103-claim-alignment-audit-spec.md §3.1 + §5 for full rationale.",

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
    "claim_id": {
      "type": "string",
      "pattern": "^C-[0-9]{3,}$",
      "description": "Per-claim identifier scoped by scoped_manifest_id. The pair (scoped_manifest_id, claim_id) is the joinable key; bare claim_id alone collides across manifests in the same passport (M-INV-1 permits cross-manifest C-001 reuse)."
    },
    "scoped_manifest_id": {
      "type": "string",
      "pattern": "^M-[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z-[0-9a-f]{4}$",
      "description": "Points to the owning claim_intent_manifest.manifest_id. INV-15 enforces cross-array integrity. MANIFEST-MISSING fallback uses the sentinel value M-0000-00-00T00:00:00Z-0000."
    },
    "claim_text": { "type": "string", "minLength": 1, "maxLength": 2000 },
    "ref_slug": {
      "type": "string",
      "minLength": 1,
      "description": "Slug from the v3.7.3 <!--ref:slug--> marker the audited citation carries. Uncited claims do NOT emit into this aggregate; they ride in uncited_assertions[] (§3.3) or constraint_violations[] (§3.5)."
    },
    "anchor_kind": {
      "enum": ["quote", "page", "section", "paragraph", "none"],
      "description": "Carried from the v3.7.3 <!--anchor:<kind>:<value>--> marker. anchor_kind=none triggers INV-6 (firm-rule defense-in-depth surface)."
    },
    "anchor_value": {
      "type": "string",
      "description": "URL-decoded anchor value. When anchor_kind=none, MUST be the empty sentinel string (INV-6). When anchor_kind != none, INV-16 forbids empty values after whitespace strip."
    },
    "judgment": {
      "enum": ["SUPPORTED", "UNSUPPORTED", "AMBIGUOUS", "RETRIEVAL_FAILED"],
      "description": "Judge verdict per the §4 step 5 prompt template. RETRIEVAL_FAILED is NOT a judge label — it is set when retrieval / anchorless / tool-failure prevents the judge from running (per error-handling §4 step 9)."
    },
    "audit_status": {
      "enum": ["completed", "inconclusive"],
      "description": "completed = judge ran (or RETRIEVAL_FAILED with deterministic verdict like retrieval_existence). inconclusive = judge could not run and no deterministic verdict was reached."
    },
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
    "rationale": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2000,
      "description": "One-sentence judge rationale, OR a fault-class-tagged audit-infrastructure failure string for ref_retrieval_method=audit_tool_failure (INV-14), OR the canonical 'v3.7.3 R-L3-1-A violation ...' prefix for anchor_kind=none (INV-6)."
    },
    "judge_model": { "type": "string", "minLength": 1 },
    "judge_run_at": { "type": "string", "format": "date-time" },
    "ref_retrieval_method": {
      "enum": ["api", "manual_pdf", "failed", "not_attempted", "not_found", "audit_tool_failure"],
      "description": "Retrieval pathway. failed = paywall (permanent license restriction, LOW-WARN). not_attempted = anchor=none short-circuit (INV-11). not_found = fabricated reference (INV-12, HIGH-WARN). audit_tool_failure = transient infrastructure outage (INV-14, MED-WARN). See §4 step 9 error handling for the failed/audit_tool_failure permanence discriminator."
    },
    "upstream_owner_agent": {
      "enum": [
        "synthesis_agent",
        "draft_writer_agent",
        "report_compiler_agent",
        null
      ],
      "description": "Prose-producing agent that owns the audited claim. Mirrors emitted_by in claim_intent_manifest.schema.json; bibliography_agent is excluded (it never emits claim_audit_results[] entries)."
    },
    "violated_constraint_id": {
      "type": ["string", "null"],
      "pattern": "^(NC-C[0-9]{3,}-[0-9]+|MNC-[0-9]+)$",
      "description": "Required when defect_stage=negative_constraint_violation (INV-7). Null otherwise. Canonical parse rule per INV-17: NC-C{n}-{m} encodes the parent claim_id digits as {n} (NO inner hyphen between C and {n})."
    },
    "upstream_dispute": {
      "type": ["string", "null"],
      "maxLength": 1000,
      "description": "Free-form dispute log entry. INV-9: meaningful only when defect_stage is a substantive defect (not null, not not_applicable)."
    },
    "audit_run_id": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z-[0-9a-f]{4}$",
      "description": "Identifier for the audit run that produced this entry. Excluded from the cache key (see §4 step 3) so different audit runs over the same (claim, ref, anchor, source, constraint-set, judge_model) tuple share the cached verdict."
    }
  }
}
```
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-contracts-passport-claim-drift-schema-json"></a>

## SOURCE: shared/contracts/passport/claim_drift.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=3846 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/claim_drift.schema.json",
  "title": "Material Passport Claim Drift Entry",
  "description": "One entry in Material Passport Schema 9 claim_drifts[] aggregate. Per claim-intent-drift finding emitted by claim_ref_alignment_audit_agent §4 step 5 manifest set-diff. Rides in its own aggregate because claim-intent drift is detected by manifest set-diff (intended ≠ emitted), NOT by judge invocation — embedding drift findings as a defect_stage of claim_audit_result would force judgment=UNSUPPORTED to be recorded without the judge ever evaluating that claim, contaminating both the schema semantics and the calibration FNR/FPR metrics. Always LOW-WARN advisory at the finalizer (per D4-a — gate-refuse is reserved for explicit author negative constraints, not drift signals). Cross-field invariants D-INV-1..D-INV-4 are lint-enforced in scripts/check_claim_audit_consistency.py. See docs/design/2026-05-15-issue-103-claim-alignment-audit-spec.md §3.4.",

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
    "finding_id": {
      "type": "string",
      "pattern": "^CD-[0-9]{3,}$",
      "description": "Per-passport unique finding identifier for claim_drifts[]. D-INV-1 enforces uniqueness."
    },
    "drift_kind": {
      "enum": ["EMITTED_NOT_INTENDED", "INTENDED_NOT_EMITTED"],
      "description": "EMITTED_NOT_INTENDED: an emitted claim that was not in the manifest (the drafted prose introduced a claim the writer did not pre-commit to). INTENDED_NOT_EMITTED: a manifest claim that did not appear in the emitted prose (the writer dropped a pre-committed claim during drafting). Both are advisory — gate-refuse is reserved for negative_constraint_violation."
    },
    "claim_text": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2000,
      "description": "For EMITTED_NOT_INTENDED, the emitted sentence; for INTENDED_NOT_EMITTED, the manifest claim_text."
    },
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
    "rule_version": {
      "const": "D4-a-v1",
      "description": "Frozen literal for the v3.8.0 release. D-INV-3 enforces equality. Future rule revisions bump the constant and require re-lint."
    },
    "upstream_owner_agent": {
      "enum": ["synthesis_agent", "draft_writer_agent", "report_compiler_agent", null]
    }
  }
}
```
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-contracts-passport-claim-intent-manifest-schema-json"></a>

## SOURCE: shared/contracts/passport/claim_intent_manifest.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=5698 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/claim_intent_manifest.schema.json",
  "title": "Material Passport Claim Intent Manifest Entry",
  "description": "One entry in Material Passport Schema 9 claim_intent_manifests[] aggregate. Emitted by synthesis_agent / draft_writer_agent / report_compiler_agent after paper-visible context loads but before prose generation, per the 'Claim Intent Manifest Emission (v3.8)' sibling section added to each writing-stage agent. Acts as the pre-commitment baseline for the manifest set-diff in claim_ref_alignment_audit_agent §4 step 5 (intended vs emitted vs supported claims). Cross-field invariants M-INV-1..M-INV-4 are lint-enforced in scripts/check_claim_audit_consistency.py. See docs/design/2026-05-15-issue-103-claim-alignment-audit-spec.md §3.2.",

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
    "manifest_version": {
      "const": "1.0",
      "description": "Schema-internal version. v3.8.0 release ships 1.0. Future drafts bump this constant to drive an explicit migration."
    },
    "manifest_id": {
      "type": "string",
      "pattern": "^M-[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z-[0-9a-f]{4}$",
      "description": "Discriminator scoping all claim_id values inside this manifest. Format: M-<ISO-8601-Z>-<4-hex>. Required because a single passport may contain multiple claim_intent_manifests[] entries (e.g., one from synthesis_agent and one from draft_writer_agent on the same run); bare C-001 alone would collide. The pair (manifest_id, claim_id) is the joinable key — see claim_audit_result.scoped_manifest_id + INV-15 / D-INV-2 cross-array integrity. M-INV-4 enforces uniqueness across all claim_intent_manifests[] entries in the same passport."
    },
    "emitted_by": {
      "enum": ["synthesis_agent", "draft_writer_agent", "report_compiler_agent"],
      "description": "The writing-stage agent that emitted this manifest. Bibliography / audit / orchestrator agents do NOT emit manifests — only the three prose-producing agents pre-commit to claim intent."
    },
    "emitted_at": { "type": "string", "format": "date-time" },
    "session_id": {
      "type": "string",
      "description": "Optional opaque identifier for the dispatch run. Useful for cross-referencing with orchestrator logs; not part of the joinable key."
    },
    "claims": {
      "type": "array",
      "minItems": 1,
      "description": "MUST list at least one substantive claim per R-L3-2-A — an empty manifest is a degenerate pre-commitment that produces no drift signal (set-diff has nothing in Intended set) and silently defeats D6.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["claim_id", "claim_text", "intended_evidence_kind", "planned_refs"],
        "properties": {
          "claim_id": {
            "type": "string",
            "pattern": "^C-[0-9]{3,}$",
            "description": "Per-manifest claim identifier. Unique within this manifest (M-INV-1); cross-manifest collisions are PERMITTED and disambiguated via the scoping pair (manifest_id, claim_id)."
          },
          "claim_text": { "type": "string", "minLength": 1, "maxLength": 2000 },
          "intended_evidence_kind": {
            "enum": ["empirical", "theoretical", "definitional", "normative"],
            "description": "What kind of evidence the writer intends to back this claim with. Used by the audit agent's manifest cross-reference to discriminate drift from refinement."
          },
          "planned_refs": {
            "type": "array",
            "items": { "type": "string" },
            "minItems": 0,
            "description": "Ref slugs the writer intends to cite. Empty array MUST be permitted — definitional/normative claims may legitimately have no planned refs at manifest time."
          },
          "negative_constraints": {
            "type": "array",
            "items": {
              "type": "object",
              "additionalProperties": false,
              "required": ["constraint_id", "rule"],
              "properties": {
                "constraint_id": {
                  "type": "string",
                  "pattern": "^NC-C[0-9]{3,}-[0-9]+$",
                  "description": "Claim-level negative constraint. Format NC-C{n}-{m} where {n} matches the parent claim_id digits (M-INV-2 + INV-17). NO inner hyphen between 'C' and '{n}' — the joinable key is the digit sequence after stripping the leading 'C'."
                },
                "rule": { "type": "string", "minLength": 1, "maxLength": 500 }
              }
            }
          }
        }
      }
    },
    "manifest_negative_constraints": {
      "type": "array",
      "description": "Globally-scoped constraints. Apply to all claims in this manifest regardless of whether the claim entry redeclares them (M-INV-3 — claim-level can ADD, never DROP global).",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["constraint_id", "rule"],
        "properties": {
          "constraint_id": {
            "type": "string",
            "pattern": "^MNC-[0-9]+$",
            "description": "Manifest-level negative constraint. Format MNC-{m}. Globally applied; cannot be overridden by claim-level NC."
          },
          "rule": { "type": "string", "minLength": 1, "maxLength": 500 }
        }
      }
    }
  }
}
```
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-contracts-passport-constraint-violation-schema-json"></a>

## SOURCE: shared/contracts/passport/constraint_violation.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=3691 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/constraint_violation.schema.json",
  "title": "Material Passport Constraint Violation Entry",
  "description": "One entry in Material Passport Schema 9 constraint_violations[] aggregate. Per uncited claim that violates a manifest negative constraint, emitted by claim_ref_alignment_audit_agent §4 step 5 stream (d). Rides in its own aggregate because constraint violations on uncited claims are real HIGH-WARN gate-refuse blockers, but claim_audit_result.ref_slug is required and uncited_assertion is LOW-WARN advisory only — routing through uncited_assertions[] would silently downgrade a HIGH-WARN signal; routing through claim_audit_result would require a sentinel ref_slug. Drives the [HIGH-WARN-CONSTRAINT-VIOLATION-UNCITED ({violated_constraint_id})] formatter annotation; gate-refuse at the formatter hard gate alongside the other four HIGH-WARN classes. Cross-field invariants CV-INV-1..CV-INV-4 are lint-enforced in scripts/check_claim_audit_consistency.py. See docs/design/2026-05-15-issue-103-claim-alignment-audit-spec.md §3.5.",

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
    "finding_id": {
      "type": "string",
      "pattern": "^CV-[0-9]{3,}$",
      "description": "Per-passport unique finding identifier for constraint_violations[]. CV-INV-1 enforces uniqueness."
    },
    "claim_text": { "type": "string", "minLength": 1, "maxLength": 2000 },
    "section_path": {
      "type": "string",
      "minLength": 1,
      "description": "Hierarchical path from document root to the section containing the offending sentence."
    },
    "violated_constraint_id": {
      "type": "string",
      "pattern": "^(NC-C[0-9]{3,}-[0-9]+|MNC-[0-9]+)$",
      "description": "Identifier of the violated constraint. NC-C{n}-{m} = claim-level (per INV-17 canonical parse rule); MNC-{m} = manifest-level. CV-INV-2 enforces cross-array resolvability against the active manifest."
    },
    "scoped_manifest_id": {
      "type": "string",
      "pattern": "^M-[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z-[0-9a-f]{4}$",
      "description": "Points to the claim_intent_manifest.manifest_id owning the violated constraint. Required (no MANIFEST-MISSING sentinel admitted — constraints require an active manifest to exist)."
    },
    "manifest_claim_id": {
      "type": ["string", "null"],
      "pattern": "^C-[0-9]{3,}$",
      "description": "For NC-C{n}-{m} (claim-level constraint), the parent claim_id from the manifest. For MNC-{m} (global), null. CV-INV-3 enforces polarity match with the constraint id prefix."
    },
    "judge_verdict": {
      "const": "VIOLATED",
      "description": "Frozen literal: only VIOLATED outcomes from the §4 negative-constraint judge prompt emit an entry here. NOT_VIOLATED outcomes produce no entry."
    },
    "rationale": { "type": "string", "minLength": 1, "maxLength": 2000 },
    "judge_model": { "type": "string", "minLength": 1 },
    "judge_run_at": { "type": "string", "format": "date-time" },
    "rule_version": {
      "const": "D4-a-v1",
      "description": "Frozen literal for the v3.8.0 release. Future rule revisions bump the constant and require re-lint."
    },
    "upstream_owner_agent": {
      "enum": ["synthesis_agent", "draft_writer_agent", "report_compiler_agent", null]
    }
  }
}
```
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-contracts-passport-literature-corpus-entry-schema-json"></a>

## SOURCE: shared/contracts/passport/literature_corpus_entry.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=16652 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/literature_corpus_entry.schema.json",
  "title": "Material Passport Literature Corpus Entry",
  "description": "One entry in Material Passport Schema 9 literature_corpus[]. Represents a single piece of literature the user has included in their corpus. Produced by user-written adapters; see academic-pipeline/references/adapters/overview.md. ARS does NOT produce these entries itself.",

  "type": "object",
  "additionalProperties": false,

  "required": [
    "citation_key",
    "title",
    "authors",
    "year",
    "source_pointer"
  ],

  "properties": {
    "citation_key": {
      "type": "string",
      "minLength": 1,
      "pattern": "^[A-Za-z][A-Za-z0-9_:-]*$",
      "description": "Stable unique identifier for this entry within the passport. Typically BibTeX citekey (e.g., 'chen2024ai'). MUST be unique within literature_corpus[]. Uniqueness is enforced by the CI lint, not by JSON Schema."
    },
    "title": {
      "type": "string",
      "minLength": 1
    },
    "authors": {
      "type": "array",
      "minItems": 1,
      "items": { "$ref": "#/$defs/csl_name" },
      "description": "CSL-JSON name format. Each item is either a personal name ({family, given, ...}) or a corporate/institution name ({literal}). See CSL-JSON spec at https://docs.citationstyles.org/en/stable/specification.html#names."
    },
    "year": {
      "type": "integer",
      "minimum": 1000,
      "maximum": 2100,
      "description": "Publication year. If the adapter cannot determine a year, the entry MUST be rejected (go to rejection_log.yaml) rather than coerced to a placeholder."
    },
    "source_pointer": {
      "type": "string",
      "minLength": 1,
      "description": "Stable URI locating this work in the user's own KB. Examples: 'zotero://select/items/0_ABCD1234', 'obsidian://open?vault=kb&file=Chen2024', 'file:///path/to/refs/chen2024.pdf', 'https://doi.org/10.1234/xyz'. ARS does NOT dereference this; consumers that want the full text fetch it from the pointer themselves."
    },

    "venue":                  { "type": "string", "minLength": 1 },
    "doi": {
      "type": "string",
      "pattern": "^10\\.[0-9]{4,9}/[^\\s]+$",
      "description": "DOI without leading 'doi:' or URL prefix."
    },
    "tags": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 },
      "description": "User-assigned tags from the source KB. Adapter-specific; treat as free-form."
    },

    "obtained_via": {
      "type": "string",
      "enum": ["zotero-api", "zotero-bbt-export", "obsidian-vault", "folder-scan", "manual", "other"],
      "description": "Strongly recommended. Which adapter produced this entry. 'other' is permitted for user-written custom adapters; those SHOULD also set adapter_name. Note: v3.6.4 reference implementations only use 'zotero-bbt-export', 'obsidian-vault', and 'folder-scan'. The remaining enum values ('zotero-api', 'manual') are reserved for user-written adapters and are permitted in the schema so such adapters remain valid without schema extension."
    },
    "obtained_at": {
      "type": "string",
      "format": "date-time",
      "description": "Strongly recommended. ISO 8601 timestamp when the adapter produced this entry."
    },
    "adapter_name": {
      "type": "string",
      "minLength": 1,
      "description": "Optional. Required when obtained_via='other'."
    },
    "adapter_version": {
      "type": "string",
      "minLength": 1
    },

    "abstract": {
      "type": "string",
      "description": "PRIVATE FIELD. May contain publisher-copyrighted material. Do NOT share passports containing this field publicly without confirming your right to do so. ARS consumers treat this as optional input; absence never causes failure."
    },
    "user_notes": {
      "type": "string",
      "description": "PRIVATE FIELD. User's own annotations from their KB. May contain copyrighted excerpts. Same sharing caveat as abstract."
    },

    "source_acquired": {
      "type": "boolean",
      "description": "v3.7.1 trust-chain field (spec § 3.1, D1). True when the original source artifact (PDF / HTML / dataset) is actually retrieved into the user's KB or workspace. Distinguishes 'we have the file' from 'we cite the bibliography record'. Adapter-set or AI-set; user-orthogonal (the user-set human-read signal is recorded in the §3.6 peer file, NOT here)."
    },
    "source_acquisition_date": {
      "type": "string",
      "format": "date-time",
      "description": "v3.7.1 trust-chain field. ISO 8601 timestamp when the original source was acquired. Only meaningful when source_acquired=true."
    },
    "source_acquisition_path": {
      "type": "string",
      "minLength": 1,
      "description": "v3.7.1 trust-chain field. Repo-relative or absolute path to the acquired source file. Only meaningful when source_acquired=true."
    },
    "source_verified_against_original": {
      "type": "boolean",
      "description": "v3.7.1 trust-chain field. True when an AI agent has cross-checked the bibliography entry's authors / year / title / venue against the actual content of the acquired source (NOT just a derivative bibliography). Per spec §3.1 firm rule #1, this MUST NOT be true unless source_acquired=true AND source_verification_method names a real method (not 'none')."
    },
    "source_verification_method": {
      "type": "string",
      "enum": ["codex_audit", "manual_grep", "vision_check", "none"],
      "description": "v3.7.1 trust-chain field. Method used to verify the entry against the original source. 'none' means no verification was performed; entries with 'none' MUST NOT set source_verified_against_original=true (spec §3.1 firm rule #1, round-2 R2-007 amend: 'none' is a valid enum but is forbidden in conjunction with verified=true)."
    },
    "description_source": {
      "type": "string",
      "pattern": "^(original_pdf|bibliography_v[0-9]+|secondary_summary)$",
      "description": "v3.7.1 trust-chain field. Origin of the descriptive metadata (title / authors / abstract). 'original_pdf' = read directly off the acquired source; 'bibliography_v<n>' (any non-negative integer n) = lifted from a derivative bibliography revision; 'secondary_summary' = paraphrased from another work. Surfaces description provenance independently of source acquisition. Spec § 3.1 yaml uses the literal `bibliography_v<n>` template, so the pattern accepts any integer n rather than hard-coding a finite revision count."
    },
    "description_last_audit": {
      "type": ["string", "null"],
      "description": "v3.7.1 trust-chain field. Round identifier of the most recent codex / cross-model audit that examined this entry's description, or null / the literal string 'none' when no such audit has run. The field-level type permits both null and 'none' broadly, but per spec §3.1 firm rule #2 the rule-#2 then-branch in `allOf` tightens this to the LITERAL STRING 'none' only when source_acquired=false (no original means audit cannot be substantive — round-6 codex P2 closure). null remains valid only when source_acquired=true and the entry is simply unaudited."
    },
    "contamination_signals_backfilled_at": {
      "type": "string",
      "format": "date-time",
      "description": "v3.7.3 backfill provenance (issue #105). ISO-8601 UTC timestamp set by scripts/migrate_literature_corpus_to_v3_7_3.py when contamination_signals was computed post-hoc on a pre-v3.7.3 entry rather than at ingest time. Absence means signals were either computed at ingest by bibliography_agent v3.7.3+ or have not been computed yet. Backward compat: pre-v3.7.3 entries lack both contamination_signals and this field; ingest-time entries (v3.7.3+) lack only this field."
    },
    "contamination_signals": {
      "type": "object",
      "additionalProperties": false,
      "description": "v3.7.3 + v3.9.0 contaminated-source advisory field (spec v3.7.3 §3.2 + v3.9.0 §3.4–§3.5). Up to four optional boolean signals computed at ingest time by bibliography_agent: v3.7.3 Vector 1 (preprint_post_llm_inflection — heuristic), v3.7.3 Vector 2 (semantic_scholar_unmatched — S2 lookup), v3.9.0 (openalex_unmatched + crossref_unmatched — triangulation extension). Surfaces at cite-time finalizer as CONTAMINATED-... marker annotation suffix; advisory only — does NOT block emission. Absence of the object means signals were not computed (legacy entries or check skipped). Presence with all populated *_unmatched fields false means lookup-based contamination evidence is absent for the queried indexes; `preprint_post_llm_inflection: true` is an independent contamination signal that remains active regardless of lookup field values. Manual entries are exempt from the three lookup fields per spec v3.9.0 §3.1 not-rule but still carry preprint_post_llm_inflection (heuristic). External motivation: Zhao et al. arXiv:2605.07723 (2026-05) documents post-2024-mid hallucination inflection in preprint corpora and §3 cross-index triangulation as viable false-positive reduction.",
      "properties": {
        "preprint_post_llm_inflection": {
          "type": "boolean",
          "description": "True when entry year >= 2024 AND venue is a preprint server. The v3.7.3 closed list of 10 servers (expanded from 6 to 10 per codex F6 / gemini review closure): arXiv, bioRxiv, medRxiv, SSRN, Research Square, Preprints.org, ChemRxiv, EarthArXiv, OSF Preprints (covers SocArXiv / PsyArXiv / other OSF-hosted services), TechRxiv. Per spec §3.2 Vector 1; threshold year derived from Zhao et al. 2026-05 mid-2024 inflection point analysis. Adapters that compute this signal MUST use the full 10-venue list; partial implementations from the schema description alone would suppress CONTAMINATED-PREPRINT advisories on the 4 newer venues (v3.7.3 codex round-4 F13 closure)."
        },
        "semantic_scholar_unmatched": {
          "type": "boolean",
          "description": "True when a Semantic Scholar API lookup (per references/semantic_scholar_api_protocol.md) returned no match by either DOI or title. The check fires only when obtained_via != 'manual' (user-curated entries are exempted; user has vouched). Per spec §3.2 Vector 2."
        },
        "openalex_unmatched": {
          "type": "boolean",
          "description": "True when an OpenAlex API lookup (per references/openalex_api_protocol.md) returned no match by DOI (with title cross-check) or title. Mirrors semantic_scholar_unmatched semantics. The check fires only when obtained_via != 'manual'. Per spec v3.9.0 §3.4."
        },
        "crossref_unmatched": {
          "type": "boolean",
          "description": "True when a Crossref API lookup (per references/crossref_api_protocol.md) returned no match by DOI (with title cross-check) or title. Mirrors semantic_scholar_unmatched semantics. The check fires only when obtained_via != 'manual'. Per spec v3.9.0 §3.5."
        }
      }
    }
  },

  "allOf": [
    {
      "description": "When obtained_via='other' (user-written custom adapter), adapter_name MUST be set so consumers can attribute the entry. Reference adapters (folder-scan, zotero-bbt-export, obsidian-vault) and other enum values do not trigger this constraint.",
      "if": {
        "properties": { "obtained_via": { "const": "other" } },
        "required": ["obtained_via"]
      },
      "then": {
        "required": ["adapter_name"]
      }
    },
    {
      "description": "v3.7.1 spec §3.1 firm rule #1 (round-2 R2-007 amend): source_verified_against_original=true REQUIRES source_acquired=true AND source_verification_method ∈ {codex_audit, manual_grep, vision_check}. The 'none' method is enumerated for shape uniformity but is FORBIDDEN in conjunction with verified=true.",
      "if": {
        "properties": { "source_verified_against_original": { "const": true } },
        "required": ["source_verified_against_original"]
      },
      "then": {
        "required": ["source_acquired", "source_verification_method"],
        "properties": {
          "source_acquired": { "const": true },
          "source_verification_method": {
            "enum": ["codex_audit", "manual_grep", "vision_check"]
          }
        }
      }
    },
    {
      "description": "v3.7.1 spec §3.1 firm rule #2 (round-6 codex P2 closure): source_acquired=false REQUIRES `description_last_audit: \"none\"` — the literal sentinel string, NOT null. Spec line 120 reads 'REQUIRES description_last_audit: none' (literal 'none'); spec line 111 yaml shows the value vocabulary as `<round_id> | none` with no null alternative. Round-1 closure made the field strictly required (presence enforced); round-6 closure removes the null alternative the field-level type permitted, since spec firm rule #2 mandates the literal sentinel. The top-level `type: [string, null]` on the field stays — null is still legal when source_acquired=true and the entry simply hasn't been audited yet — but the rule-#2 then-branch tightens to the literal string only.",
      "if": {
        "properties": { "source_acquired": { "const": false } },
        "required": ["source_acquired"]
      },
      "then": {
        "required": ["description_last_audit"],
        "properties": {
          "description_last_audit": {
            "type": "string",
            "const": "none"
          }
        }
      }
    },
    {
      "description": "v3.7.3 spec §3.2 cross-field rule (gemini review F5 closure): preprint_post_llm_inflection=true REQUIRES year>=2024. The flag's definition is `year >= 2024 AND venue is a preprint server`, so setting the flag true with a pre-2024 year is logically contradictory and the schema rejects it. The reverse (year>=2024 AND flag=false) is legal — flag may be false because the venue is not a preprint server.",
      "if": {
        "properties": {
          "contamination_signals": {
            "type": "object",
            "properties": {
              "preprint_post_llm_inflection": { "const": true }
            },
            "required": ["preprint_post_llm_inflection"]
          }
        },
        "required": ["contamination_signals"]
      },
      "then": {
        "properties": {
          "year": { "minimum": 2024 }
        }
      }
    },
    {
      "description": "v3.9.0 spec §3.1 extends v3.7.3 §3.2 manual-entry exemption (codex round-3 F11 closure) symmetrically: when obtained_via='manual' the bibliography_agent SKIPS all three lookups (Semantic Scholar / OpenAlex / Crossref) and OMITS the three *_unmatched fields. The schema enforces this contract: a manual entry MUST NOT carry any of semantic_scholar_unmatched / openalex_unmatched / crossref_unmatched. Setting any to true on a manual entry would surface CONTAMINATED-* on a user-vouched reference. The asymmetry: preprint_post_llm_inflection IS still computed for manual entries (pure heuristic, no lookup) and is not in the exemption scope.",
      "if": {
        "properties": { "obtained_via": { "const": "manual" } },
        "required": ["obtained_via"]
      },
      "then": {
        "not": {
          "properties": {
            "contamination_signals": {
              "type": "object",
              "anyOf": [
                { "required": ["semantic_scholar_unmatched"] },
                { "required": ["openalex_unmatched"] },
                { "required": ["crossref_unmatched"] }
              ]
            }
          },
          "required": ["contamination_signals"]
        }
      }
    }
  ],

  "$defs": {
    "csl_name": {
      "oneOf": [
        { "$ref": "#/$defs/csl_personal_name" },
        { "$ref": "#/$defs/csl_literal_name" }
      ]
    },
    "csl_personal_name": {
      "type": "object",
      "additionalProperties": false,
      "required": ["family"],
      "properties": {
        "family":                { "type": "string", "minLength": 1 },
        "given":                 { "type": "string" },
        "suffix":                { "type": "string" },
        "dropping-particle":     { "type": "string" },
        "non-dropping-particle": { "type": "string" },
        "comma-suffix":          { "type": ["string", "boolean"] },
        "static-ordering":       { "type": ["string", "boolean"] },
        "parse-names":           { "type": ["string", "boolean"] }
      }
    },
    "csl_literal_name": {
      "type": "object",
      "additionalProperties": false,
      "required": ["literal"],
      "properties": {
        "literal": { "type": "string", "minLength": 1 }
      }
    }
  }
}
```
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-contracts-passport-rejection-log-schema-json"></a>

## SOURCE: shared/contracts/passport/rejection_log.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=3354 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/rejection_log.schema.json",
  "title": "Literature Corpus Rejection Log",
  "description": "Output companion to passport.yaml. Records entries that the adapter could not include in literature_corpus[]. Always emitted; empty when no rejections. Consumers are not required to read this; it exists for user debugging and audit.",

  "type": "object",
  "additionalProperties": false,

  "required": ["adapter_name", "adapter_version", "generated_at", "rejected"],

  "properties": {
    "adapter_name":   { "type": "string", "minLength": 1 },
    "adapter_version":{ "type": "string", "minLength": 1 },
    "generated_at":   { "type": "string", "format": "date-time" },
    "input_source": {
      "type": "string",
      "minLength": 1,
      "description": "Optional. Human-readable description of the adapter input (path, URL, etc.)."
    },
    "rejected": {
      "type": "array",
      "items": { "$ref": "#/$defs/rejection" }
    },
    "summary": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "total_input":    { "type": "integer", "minimum": 0 },
        "total_accepted": { "type": "integer", "minimum": 0 },
        "total_rejected": { "type": "integer", "minimum": 0 }
      }
    }
  },

  "$defs": {
    "rejection": {
      "type": "object",
      "additionalProperties": false,
      "required": ["source", "reason"],
      "properties": {
        "source": {
          "type": "string",
          "minLength": 1,
          "description": "Where the rejected item came from. Adapter-specific: filename for folder_scan, Zotero item key for zotero, .md path for obsidian."
        },
        "reason": {
          "type": "string",
          "enum": [
            "missing_required_field",
            "invalid_field_format",
            "duplicate_citation_key",
            "unresolvable_source_pointer",
            "year_unparseable",
            "authors_unparseable",
            "adapter_error",
            "other"
          ]
        },
        "detail": {
          "type": "string",
          "minLength": 1,
          "description": "Free-text explanation. Required when reason='other' (enforced by allOf below). Recommended otherwise. Must be non-empty when present — empty strings defeat the 'interpretable rejection' contract."
        },
        "raw": {
          "type": ["object", "string"],
          "description": "Optional. Adapter's best-effort reproduction of the original input item. Object for structured sources; string for raw filenames or text lines."
        },
        "missing_fields": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Optional but strongly recommended when reason='missing_required_field'."
        }
      },
      "allOf": [
        {
          "description": "When reason='other', detail MUST be provided so the rejection is interpretable. Categorical reason values are self-explanatory and do not require detail.",
          "if": {
            "properties": { "reason": { "const": "other" } },
            "required": ["reason"]
          },
          "then": {
            "required": ["detail"]
          }
        }
      ]
    }
  }
}
```
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-contracts-passport-reset-ledger-entry-schema-json"></a>

## SOURCE: shared/contracts/passport/reset_ledger_entry.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=7274 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/reset_ledger_entry.schema.json",
  "title": "Passport Reset Ledger Entry",
  "description": "One append-only ledger entry in reset_boundary[]. Two kinds: 'boundary' (recorded at a FULL checkpoint when ARS_PASSPORT_RESET=1) and 'resume' (recorded when resume_from_passport consumes a boundary entry). See academic-pipeline/references/passport_as_reset_boundary.md.",
  "oneOf": [
    { "$ref": "#/$defs/boundary" },
    { "$ref": "#/$defs/resume" }
  ],
  "$defs": {
    "boundary": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "kind",
        "hash",
        "stage",
        "next",
        "generated_at",
        "session_marker",
        "version_label"
      ],
      "properties": {
        "kind": {
          "const": "boundary",
          "description": "Discriminator. 'boundary' = reset emitted at a FULL checkpoint."
        },
        "hash": {
          "type": "string",
          "pattern": "^[0-9a-f]{12}$",
          "description": "First 12 lowercase hex characters of SHA-256 over the concatenated ledger (prior entries + this entry with hash set to the canonical placeholder '000000000000'). Placeholder rule is normative — see protocol doc §'The reset boundary protocol' step 2."
        },
        "stage": {
          "type": "string",
          "minLength": 1,
          "description": "Stage number or name that just completed (e.g., '1', '2', '2.5', 'RESEARCH')."
        },
        "next": {
          "type": ["string", "null"],
          "minLength": 1,
          "description": "Default next stage after resume. When pending_decision is unset, this is the authoritative route. When pending_decision is set, this field is advisory: the matched option's next_stage takes precedence, and next MAY be null (including when all branches terminate). The orchestrator MUST NOT auto-advance using next when pending_decision is present."
        },
        "generated_at": {
          "type": "string",
          "format": "date-time",
          "description": "ISO 8601 timestamp of boundary creation."
        },
        "session_marker": {
          "type": "string",
          "minLength": 1,
          "description": "Opaque identifier for the source session. Audit-only; not relied on for resume."
        },
        "version_label": {
          "type": "string",
          "minLength": 1,
          "description": "Monotonic version label for the passport state at this boundary (e.g., 'v1.0', 'v1.1-revised'). Stage re-runs bump this."
        },
        "mode": {
          "type": "string",
          "description": "Mode of the just-completed stage (e.g., 'full', 'systematic-review')."
        },
        "verification_status": {
          "type": "string",
          "enum": ["VERIFIED", "UNVERIFIED", "STALE"],
          "description": "Mirror of Schema 9 verification_status at this boundary. Copied for convenience; authoritative value lives in Schema 9 top-level."
        },
        "observer_snapshot_ref": {
          "type": "string",
          "description": "Optional path or ID of the collaboration_depth_agent observer output for this checkpoint. Audit-only."
        },
        "pending_decision": {
          "type": "object",
          "additionalProperties": false,
          "required": ["question", "options"],
          "properties": {
            "question": {
              "type": "string",
              "minLength": 1,
              "description": "Human-readable question the user must answer on resume (e.g., 'Stage 3 review outcome: revise, restructure, or abort?')."
            },
            "options": {
              "type": "array",
              "minItems": 2,
              "uniqueItems": true,
              "items": {
                "type": "object",
                "additionalProperties": false,
                "required": ["value", "next_stage"],
                "properties": {
                  "value": {
                    "type": "string",
                    "minLength": 1,
                    "description": "Branch identifier. Must be unique across the options array — chosen_branch on the resume entry matches this field."
                  },
                  "next_stage": {
                    "type": ["string", "null"],
                    "description": "Stage number or name to route to when this branch is chosen. null means terminate the pipeline."
                  },
                  "next_mode": {
                    "type": "string",
                    "minLength": 1,
                    "description": "Optional downstream mode override when this branch is chosen. Omit to use the default mode for next_stage."
                  }
                }
              },
              "description": "Enumerated decision branches. Each option carries its own routing: on resume, the orchestrator looks up chosen_branch in options[].value, then uses that entry's next_stage and next_mode to determine actual routing. The boundary entry's next field is advisory (best-guess default) and is superseded by the matched option's next_stage at resume time. CLI stage=/mode= overrides from resume_from_passport still win over option routing."
            }
          },
          "description": "Set when the boundary co-occurs with a MANDATORY user decision (Stage 3 rejection, Stage 5 finalization, etc.). When present, resume must re-prompt the user. Each option carries its own next_stage/next_mode routing; the boundary entry's 'next' field is advisory only and is overridden by the matched option's next_stage at resume time."
        }
      }
    },
    "resume": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "kind",
        "consumes_hash",
        "generated_at",
        "session_marker"
      ],
      "properties": {
        "kind": {
          "const": "resume",
          "description": "Discriminator. 'resume' = resume_from_passport consumed a prior boundary entry."
        },
        "consumes_hash": {
          "type": "string",
          "pattern": "^[0-9a-f]{12}$",
          "description": "Hash of the boundary entry this resume consumes. Append-only pointer — lets readers compute awaiting_resume state from the ledger alone."
        },
        "generated_at": {
          "type": "string",
          "format": "date-time",
          "description": "ISO 8601 timestamp of resume event."
        },
        "session_marker": {
          "type": "string",
          "minLength": 1,
          "description": "Opaque identifier for the resuming session."
        },
        "chosen_branch": {
          "type": "string",
          "description": "If the consumed boundary had pending_decision, record which option the user chose. Omit otherwise."
        },
        "user_override": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "stage": { "type": "string" },
            "mode": { "type": "string" }
          },
          "description": "Optional stage/mode overrides the user supplied on the resume command."
        }
      }
    }
  }
}
```
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-contracts-passport-uncited-assertion-schema-json"></a>

## SOURCE: shared/contracts/passport/uncited_assertion.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=3412 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/uncited_assertion.schema.json",
  "title": "Material Passport Uncited Assertion Entry",
  "description": "One entry in Material Passport Schema 9 uncited_assertions[] aggregate. Per uncited-assertion finding emitted by claim_ref_alignment_audit_agent §4 step 6 (D4-c three-condition token rule). Rides in its own aggregate because the finding has no ref_slug to evaluate — embedding it in claim_audit_result would either force a sentinel ref_slug value or relax claim_audit_result.required, both fighting that schema's grain. Always LOW-WARN advisory at the finalizer; gate-refuse is reserved for citation-level defects and constraint_violation. Cross-field invariants U-INV-1..U-INV-4 are lint-enforced in scripts/check_claim_audit_consistency.py. See docs/design/2026-05-15-issue-103-claim-alignment-audit-spec.md §3.3.",

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
    "finding_id": {
      "type": "string",
      "pattern": "^UA-[0-9]{3,}$",
      "description": "Per-passport unique finding identifier for uncited_assertions[]. U-INV-1 enforces uniqueness."
    },
    "sentence_text": { "type": "string", "minLength": 1, "maxLength": 2000 },
    "section_path": {
      "type": "string",
      "minLength": 1,
      "description": "Hierarchical path from document root to the section containing the sentence, e.g. '2. Methods > 2.3 Sampling'."
    },
    "trigger_tokens": {
      "type": "array",
      "minItems": 1,
      "items": { "type": "string" },
      "description": "Concrete tokens that matched D4-c condition 1 (quantifiers or empirical-claim verbs). E.g. ['67%', 'showed']. U-INV-2 enforces non-empty."
    },
    "detected_at": { "type": "string", "format": "date-time" },
    "rule_version": {
      "const": "D4-c-v1",
      "description": "Frozen literal for the v3.8.0 release. U-INV-3 enforces equality. Future rule revisions bump the constant and require re-lint."
    },
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
      "description": "Points to the claim_intent_manifest.manifest_id owning the referenced manifest_claim_id. The (scoped_manifest_id, manifest_claim_id) pair uniquely identifies which manifest's claim this uncited finding corresponds to, since C-001 may collide across manifests in the same passport. Required when manifest_claim_id != null (U-INV-4 cross-array integrity). Null when manifest_claim_id is null (the uncited sentence does not correspond to any manifest claim)."
    }
  }
}
```
<!-- SOURCE-CONTENT-END -->

<a id="source-shared-contracts-passport-uncited-audit-failure-schema-json"></a>

## SOURCE: shared/contracts/passport/uncited_audit_failure.schema.json

<!-- SOURCE-CONTENT-BEGIN bytes=4528 -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/Imbad0202/academic-research-skills/shared/contracts/passport/uncited_audit_failure.schema.json",
  "title": "Material Passport Uncited Audit Failure Entry",
  "description": "One entry in Material Passport Schema 9 uncited_audit_failures[] aggregate (v3.8.2 / #118). Per uncited-sentence × manifest pair where the constraint judge raised a JudgeInvocationError during §4 step 5 stream (d) judging. Rides in its own aggregate because the cited-path INV-14 audit_tool_failure row (a claim_audit_result entry carrying ref_retrieval_method=audit_tool_failure) cannot be reused — claim_audit_result.ref_slug is required and the uncited path has no ref to bind; uncited_assertion is LOW-WARN advisory and routing UAF through it would conflate D4-c detector signal with audit-time infrastructure failure. Drives the [CLAIM-AUDIT-TOOL-FAILURE-UNCITED — <fault-class>] formatter annotation at MED-WARN advisory tier; gate passes — retry-next-pass remediation. Pre-v3.8.2 behaviour silently substituted NOT_VIOLATED on JudgeInvocationError and suppressed HIGH-WARN constraint checks; v3.8.2 routes failures through this aggregate so operational signal surfaces without dropping audit coverage. Cross-field invariants UAF-INV-1..UAF-INV-6 are lint-enforced in scripts/check_claim_audit_consistency.py. See docs/design/2026-05-15-issue-103-claim-alignment-audit-spec.md §3.6.",

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
    "finding_id": {
      "type": "string",
      "pattern": "^UAF-[0-9]{3,}$",
      "description": "Per-passport unique finding identifier for uncited_audit_failures[]. UAF-INV-1 enforces uniqueness."
    },
    "claim_text": { "type": "string", "minLength": 1, "maxLength": 2000 },
    "section_path": {
      "type": "string",
      "minLength": 1,
      "description": "Hierarchical path from document root to the section containing the offending sentence. Mirrors uncited_assertion.section_path."
    },
    "scoped_manifest_id": {
      "type": "string",
      "pattern": "^M-[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z-[0-9a-f]{4}$",
      "description": "Points to the claim_intent_manifest.manifest_id whose MNC/NC-C set was being judged when the failure occurred. Required — no MANIFEST-MISSING sentinel admitted; UAF emission requires an active manifest scope. UAF-INV-2 enforces cross-array resolvability."
    },
    "manifest_claim_id": {
      "type": ["string", "null"],
      "pattern": "^C-[0-9]{3,}$",
      "description": "When the sentence was bound to a manifest claim (sentence carries manifest_claim_id per §4 step 5 stream (d) NC-C judging path), points to that claim. Null when the judge call was against MNCs only (manifest-wide constraints, no claim binding). UAF-INV-3 enforces (scoped_manifest_id, manifest_claim_id) pair integrity when non-null. Mirrors constraint_violation.manifest_claim_id polarity."
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
      "description": "Same closed enum as INV-14 fault-class taxonomy on the cited path. Sourced from JudgeInvocationError.fault_class at the raise site in claim_audit_pipeline.py."
    },
    "rationale": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2000,
      "description": "MUST begin with this row's fault_class value followed by ': ' and a free-form detail. UAF-INV-5 enforces the prefix match. Example: 'judge_timeout: judge timed out after 30s'. Mirrors INV-14 rationale format on the cited path."
    },
    "judge_model": { "type": "string", "minLength": 1 },
    "judge_run_at": { "type": "string", "format": "date-time" },
    "rule_version": {
      "const": "D4-c-v1-uaf-v1",
      "description": "Frozen literal for the v3.8.2 release. UAF surface version. Distinguishes from D4-c-v1 (uncited_assertion D4-c detector) and D4-a-v1 (constraint_violation). Future revisions bump the literal and require re-lint."
    },
    "upstream_owner_agent": {
      "enum": ["synthesis_agent", "draft_writer_agent", "report_compiler_agent", null]
    }
  }
}
```
<!-- SOURCE-CONTENT-END -->
