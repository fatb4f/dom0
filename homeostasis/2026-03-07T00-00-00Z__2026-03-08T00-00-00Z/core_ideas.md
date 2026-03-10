# Homeostasis Meta-Skill: Core Ideas

## Purpose

`homeostasis` is an umbrella meta-skill for continuous repository/runtime self-checking driven by `spawn`.

It keeps skill metadata, runtime signals, and review readiness current without requiring manual sweeps.

## Core Model

1. `spawn` runs `homeostasis` periodically in the background.
2. `homeostasis` executes focused capabilities (for now: `introspect-skills`).
3. Capabilities produce contract-shaped artifacts.
4. Downstream reviewers (e.g. `codex-review`) consume artifacts to decide actions.

## Capability: introspect-skills

`introspect-skills` should:

1. On timer:
- parse/serialize `../discussions`,
- parse/serialize bounded `system-journal` signals,
- parse/serialize each skill under `../skills` (at minimum: `SKILL.md`, `assets/*`, `references/*`, `scripts/*` metadata).

2. Emit one contract-defined artifact for review handoff:
- `introspect.skills.snapshot.json` (name can be finalized later).

## Operating Principles

1. Periodic and incremental:
- timer-driven execution,
- cursor/hash-based updates (avoid full rescans each run).

2. Bounded observability:
- journal input must be scoped by time window, units, and severity.

3. Separation of concerns:
- `homeostasis/introspect` collects and normalizes.
- review skills/pipelines decide policy and mutation.

4. Evidence-first outputs:
- every flagged drift/risk includes `evidence_refs`.

## Suggested Snapshot Contract (v0)

- `meta`: version, generated_at, host, profile.
- `sources`: discussions refs, skills refs, journal window.
- `skills_inventory`: discovered skills + structural metadata.
- `signals`: normalized runtime/journal events relevant to skills.
- `drift`: missing/invalid/stale fields and changed contracts.
- `review_candidates`: items for `codex-review` with priority + reason + evidence refs.
- `status`: `PASS|FAIL|UNKNOWN`.

## Why This Helps

1. Moves recurring introspection from ad-hoc terminal usage to deterministic background maintenance.
2. Keeps skill quality and runtime context synchronized as metadata/events evolve.
3. Establishes a stable substrate for contextual/working-memory upgrades in `spawn`.

## Pattern Alignment

`homeostasis` is aligned with `Skill Library Evolution` and the `Feedback Loops` category:

1. Skill Library Evolution alignment:
- treats skills as evolving assets (`draft -> validated -> stable -> deprecated`),
- enforces periodic validation and curation,
- supports progressive disclosure by prioritizing metadata and loading deep context only when needed.

2. Feedback Loops alignment:
- detection: capture drift/signals from skills + journal + discussions,
- evaluation: `verify/gate` with tri-state decisions (`VALID|INVALID|UNKNOWN`),
- action: create review candidates and controlled follow-up actions,
- learning: update patterns/contracts from outcomes and evidence.

## Homeostasis Capability Additions

To operationalize the pattern mapping:

1. Add `skill_health` capability:
- validates frontmatter/contract completeness,
- tracks staleness and last-validated timestamps,
- emits promotion/deprecation recommendations.

2. Add `feedback_loop` capability:
- maintains retry budgets and terminal states (`green|blocked|needs-human`),
- records incident-to-eval candidates from repeated failures,
- emits evidence-backed recommendations for `codex-review`.

3. Keep mutation boundaries explicit:
- `homeostasis` collects/evaluates only,
- downstream review/execution flows apply changes.

## Todo Contract Integration

`todo*` artifacts should be contract-based and skill-managed:

1. `backlog.json` is SSOT state.
2. `backlog contract (not yet defined)` defines the contract.
3. `backlog.md` is derived/non-authoritative output.

`homeostasis` should treat todo management as a dedicated writer capability (`todo-write` or equivalent), with:
- schema validation on each change,
- controlled status transitions,
- evidence-linked updates for `blocked/done`,
- deterministic `backlog.md` render from `backlog.json`.

## Adversarial Validation Capability (Opponent Timer)

Add a second background timer capability under `homeostasis`:

1. `opponent_validate` purpose:
- intentionally seek policy breaks against per-skill SSOT definitions,
- act as adversarial reviewer, not as mutator.

2. Operating mode:
- read-only challenge generation from latest skill/state artifacts,
- attempt to produce contradiction cases, missing-contract cases, stale-evidence cases,
- emit only evidence-backed findings.

3. Correlation contract:
- each opponent output must reference `introspect.skills.snapshot` by `snapshot_id`,
- each finding includes `skill_id`, `policy_ref`, `attack_case_id`, `evidence_refs[]`, `severity`, `confidence`.

4. Decision semantics:
- findings classified as `confirmed_break | suspected_break | no_break`,
- `suspected_break` maps to `UNKNOWN` gate pressure until validated.

5. Safety boundary:
- no direct writes to skills/config/runtime from opponent capability,
- all remediation proposals flow through review/execution gates.

This gives an adversarial-driven development loop while preserving deterministic governance.

## Opponent Tool Bindings

Bind `opponent_validate` to deterministic tooling so findings are reproducible:

1. `hypothesis`:
- generate adversarial property-based inputs against skill contracts,
- target boundary/missing-field/invalid-transition cases.

2. `jsonschema`:
- validate positive and negative fixture corpora against SSOT schemas,
- detect drift between declared contract and emitted artifacts.

3. `pytest`:
- package each `attack_case_id` as a runnable test,
- persist stable pass/fail evidence for correlation with snapshot IDs.

### Opponent finding payload (minimum)

- `snapshot_id`
- `skill_id`
- `policy_ref`
- `attack_case_id`
- `tool` (`hypothesis|jsonschema|pytest`)
- `result` (`confirmed_break|suspected_break|no_break`)
- `severity`
- `confidence`
- `evidence_refs[]`

All tool-bound runs stay read-only; remediation remains downstream.

## Source References

- `https://github.com/nibzard/awesome-agentic-patterns/blob/main/patterns/skill-library-evolution.md`
- `https://github.com/nibzard/awesome-agentic-patterns?tab=readme-ov-file#feedback-loops`
