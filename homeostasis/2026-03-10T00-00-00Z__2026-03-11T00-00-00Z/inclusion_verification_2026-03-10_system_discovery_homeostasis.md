# Inclusion Verification: 2026-03-10

## Inputs

- Slice: `/home/_404/src/discussions/skills/homeostasis/2026-03-10T00-00-00Z__2026-03-11T00-00-00Z/session_log_slice_2026-03-10_system_discovery_homeostasis.jsonl`
- Formal doc: `/home/_404/src/discussions/skills/homeostasis/2026-03-10T00-00-00Z__2026-03-11T00-00-00Z/system_discovery_homeostasis.md`

## Method

1. Extract requirements from slice records.
2. Map requirements to formal-doc sections.
3. Classify coverage (`FULL|PARTIAL|OUT_OF_SCOPE`).

## Coverage Matrix

| Slice ID | Requirement Extract | Formal Mapping | Coverage | Notes |
|---|---|---|---|---|
| S001 | Yes. **Jsonnet still remains unrequired.** | `Near-Term Direction` | PARTIAL | The document carries forward bootstrap-family deferral, but it does not restate the Jsonnet decision explicitly. |
| S002 | Agreed. | `Near-Term Direction` | PARTIAL | The agreement survives indirectly through the same deferred-bootstrap framing. |
| S003 | Mapped against the provided `specify-proposal` register and the repo’s `json_tool` operator surface. | None | OUT_OF_SCOPE | The slice intentionally retains the pre-homeostasis transition context, but the formal doc does not restate the `specify-proposal` process map. |
| S004 | Using `specify-proposal` first and `tooling-policy` second. I’m checking the local skill constraints. | None | OUT_OF_SCOPE | Skill-routing commentary is process evidence, not part of the homeostasis model. |
| S005 | I’ve confirmed the local packet shape: `specify-proposal` is still minimal. | None | OUT_OF_SCOPE | Proposal-packet status is outside the formal scope of this document. |
| S006 | Your process map is directionally right. | None | OUT_OF_SCOPE | This is still about `specify-proposal` packet revision, not the discovery substrate. |
| S007 | Your map is correct against the current repo state, with three adjustments. | None | OUT_OF_SCOPE | Register-level adjustments were intentionally excluded from this formal document. |
| S008 | Consolidate | None | OUT_OF_SCOPE | This consolidation request applied to the earlier `specify-proposal` discussion, not to the homeostasis document. |
| S009 | **Consolidated Model** | `Near-Term Direction` | PARTIAL | The bootstrap-family deferral is preserved, but the rest of the `specify-proposal` register rewrite is not in scope here. |
| S010 | The operational substrate requires roots, state-space/FSM/service/asset definitions, and a tree rather than leaf-only thinking. | `Root Systems`; `Discovery Method`; `Live Substrates`; `Artifact Set` | PARTIAL | The document establishes roots and crawl-driven discovery, but it deliberately postpones frozen ontology definitions until after downstream crawl. |
| S011 | Correct. The bootstrap object family is still not the root. | `Root Systems`; `Near-Term Direction` | FULL | The document explicitly makes root-system discovery primary and bootstrap objects downstream. |
| S012 | 1. yes / 2. no. Once 1 is defined, we need to meticulously process-crawl downstream. | `Process-crawl downstream` | FULL | The document rejects detached abstract ontology-first work and adopts process crawl as the forcing function. |
| S013 | Roots first, then trunk by crawl. | `Discovery Method`; `What This Prevents` | FULL | Captured directly in the root-first, crawl-driven framing. |
| S014 | Bingo | `Near-Term Direction` | FULL | This is acceptance of the root-first direction that the document now formalizes. |
| S015 | The next correct proposal is a root-system packet that defines `host`, `codex`, and `spawn`. | `Root Systems`; `Near-Term Direction` | FULL | The document names those three roots and calls for a root-system discovery packet. |
| S016 | Scope the three candidate FSMs by identity; if a finding affects identity, trigger new applied-control analysis. | `Scope roots by identity`; `Test FSM fit`; `Trigger Rule` | FULL | This is one of the core mechanics captured verbatim in the formal model. |
| S017 | Scope is `identity-first`, not `leaf-first`. | `Scope roots by identity`; `What This Prevents` | FULL | The document explicitly says not to start from leaf artifacts. |
| S018 | IDENTITY is persisted as a JSON Schema derived from crawling and control-analysis findings. | `Identity substrate`; `Artifact Set` | FULL | The document records `identity.schema` as the promoted representation contract derived from crawl and control findings. |
| S019 | Persist canonical identity instance plus schema, findings, delta, and control report. | `Artifact Set`; `Closed Loops` | FULL | The artifact family and loop mechanics are represented directly. |
| S020 | Undisclosed operations become new unknowns that mutate live identity immediately and are not promotion-gated. | `Core Principle`; `Identity substrate`; `Promotion Boundary` | FULL | The live-fact / non-promotion-gated rule is explicit. |
| S021 | Correct. | `Core Principle`; `Promotion Boundary` | FULL | This acceptance is represented by the same live-fact split. |
| S022 | Only two promotion-gated deltas are valid: identity-schema fidelity and applied-control fidelity. | `Promotion Boundary` | FULL | The document names exactly those two promotion surfaces. |
| S023 | Yes. That is the right split. | `Promotion Boundary` | FULL | The acceptance is reflected by the same section. |
| S024 | Observable links and relationships must be added immediately to Neo4j or an evolving JSON relationship object. | `Relationship substrate` | FULL | The document defines `relationship.current.v1.json` plus Neo4j as a projection/query surface. |
| S025 | Yes. | `Relationship substrate` | FULL | The acceptance is represented by the same section. |
| S026 | `relationship.current.v1.json` is identity-mutating and creates a second closed loop. | `Live Substrates`; `Closed Loops` | FULL | The document explicitly models the relationship and identity loops as coupled. |
| S027 | Yes. | `Closed Loops` | FULL | The acceptance is represented by the same loop model. |
| S028 | Homeostasis | `Combined homeostatic loop`; `What Counts as Accuracy` | FULL | The document adopts homeostasis as the organizing concept. |
| S029 | Exactly. | `Combined homeostatic loop`; `What Counts as Accuracy` | FULL | The acceptance is represented by the same homeostatic framing. |
| S030 | Consolidate all of this into a document about discovery and keeping an accurate view. | `Purpose` | FULL | The document opens with exactly those two questions. |
| S031 | I’m checking the existing `discussions/` layout first so I can place the document correctly. | None | OUT_OF_SCOPE | File-placement work is process evidence, not formal content. |
| S032 | There’s already a `discussions/skills/homeostasis/` working area, so I’m placing the consolidation there. | None | OUT_OF_SCOPE | Repository placement is process evidence, not part of the model. |
| S033 | I’m writing a single working document under `discussions/skills/homeostasis/`. | None | OUT_OF_SCOPE | Writing-progress commentary is not part of the formal model. |
| S034 | The consolidation is written. I’m doing a quick readback pass. | None | OUT_OF_SCOPE | Editing progress is not formal content. |
| S035 | The schema-origin point needs to be stated explicitly. | `Identity substrate` | FULL | The formal doc now says `identity.schema` is derived from crawl and applied-control findings and can become known-incomplete. |
| S036 | Consolidated into `system_discovery_homeostasis.md`. | None | OUT_OF_SCOPE | Publication/status commentary is outside formal scope. |
| S037 | Use the `session-capture` process and attach raw conversation logs as a guardrail against lossy translation. | `Session Capture Evidence` | FULL | The formal doc now cites the source session JSONL, bounded slice, time window, and inclusion-verification artifact. |
| S038 | Using `session-capture` for this turn because you named that process explicitly. | None | OUT_OF_SCOPE | Skill-routing commentary is process evidence, not formal content. |
| S039 | The skill expects a bounded slice plus an inclusion-verification artifact. | `Session Capture Evidence` | FULL | The formal doc now carries those exact evidence artifacts. |
| S040 | Locate the exact session segment so the slice stays bounded to the relevant discussion. | `Session Capture Evidence` | PARTIAL | The bounded window is preserved, but the selection rationale is not restated in the formal doc. |
| S041 | The relevant window starts at `2026-03-10T19:31:03Z` and runs through the raw-log request. | `Session Capture Evidence` | FULL | The formal doc records the bounded evidence window explicitly. |
| S042 | Generate a bounded slice in `discussions/skills/homeostasis/`. | None | OUT_OF_SCOPE | File-generation progress is process evidence, not formal content. |
| S043 | The bounded slice is written and will be used with the formal doc to produce a real inclusion matrix. | `Session Capture Evidence` | PARTIAL | The evidence artifacts are represented, but the earlier interim record count is not restated. |
| S044 | The slice intentionally includes immediate pre-homeostasis transition context. | None | OUT_OF_SCOPE | That scoping rationale is preserved in the inclusion report, not in the formal doc itself. |
| S045 | The formal doc should cite the slice path and window. | `Session Capture Evidence` | FULL | The evidence section now cites both directly. |
| S046 | Check whether an established `session-capture-patterns.json` shape exists. | None | OUT_OF_SCOPE | Pattern-shape discovery is implementation evidence, not formal content. |
| S047 | Add the original source session JSONL to the evidence section as a guardrail. | `Session Capture Evidence` | FULL | The formal doc now cites the original session JSONL explicitly. |
| S048 | Replace the scaffolded matrix with explicit coverage judgments. | None | OUT_OF_SCOPE | Inclusion-matrix editing is verification work, not formal-doc content. |
| S049 | The inclusion matrix is filled and a minimal pattern file will be added. | None | OUT_OF_SCOPE | Verification progress and pattern generation are outside the formal scope. |
| S050 | Write a minimal pattern file from this slice. | None | OUT_OF_SCOPE | Pattern-file generation is a companion artifact, not formal-doc content. |
| S051 | Validate the JSON pattern file and inspect the resulting artifact set. | None | OUT_OF_SCOPE | Validation/logistics commentary is not formal content. |
| S052 | The session-capture companion set is in place with slice, inclusion, and patterns artifacts. | `Session Capture Evidence` | PARTIAL | The formal doc captures the slice and inclusion evidence directly, but not the full artifact summary line-for-line. |
| S053 | It should in fact define one, even if there isn't one. | `Scope roots by identity` | FULL | The formal doc now requires an explicit `scope_root` or `control_root` even when no enclosing git repository exists. |
| S054 | The model should define a workspace/control root even when no enclosing git repo exists. | `Scope roots by identity` | FULL | Captured directly in the new scope-anchor rule. |
| S055 | Extend the homeostasis doc and capture artifacts to record the correction explicitly. | `Scope roots by identity`; `Session Capture Evidence` | FULL | Both the scope-root rule and the refreshed evidence window were added. |

## Result

- `FULL`: 29
- `PARTIAL`: 7
- `OUT_OF_SCOPE`: 19

The out-of-scope records are retained deliberately as transition context from the earlier `specify-proposal` discussion and the session-capture implementation work into the root-first homeostasis model. The formal document begins at the point where the conversation pivots from proposal-packet design into system discovery, live identity, relationship mutation, control homeostasis, and explicit root anchoring without requiring `.git`.
