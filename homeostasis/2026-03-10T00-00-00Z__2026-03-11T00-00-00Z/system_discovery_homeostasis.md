# System Discovery and Accuracy Homeostasis

## Purpose

This document answers two questions:

1. How are we going to discover our system?
2. How are we going to keep an accurate view of what it is?

The answer is a root-first, crawl-driven, homeostatic model:

- start from the real root systems,
- crawl downstream through observable processes and relationships,
- update live identity immediately when reality changes,
- re-run applied-control analysis when identity changes,
- promote only representation fidelity and control fidelity.

This is not a static documentation workflow. It is a continuous operational truth-maintenance loop.

## Session Capture Evidence

- Source session JSONL: `/home/_404/.config/codex/sessions/2026/03/10/rollout-2026-03-10T12-45-08-019cd8a3-559c-75c0-b2a0-1e72a85737b3.jsonl`
- Slice JSONL: `discussions/skills/homeostasis/2026-03-10T00-00-00Z__2026-03-11T00-00-00Z/session_log_slice_2026-03-10_system_discovery_homeostasis.jsonl`
- Slice Markdown: `discussions/skills/homeostasis/2026-03-10T00-00-00Z__2026-03-11T00-00-00Z/session_log_slice_2026-03-10_system_discovery_homeostasis.md`
- Window: `2026-03-10T19:31:03.051Z -> 2026-03-10T20:32:44.907Z`
- Inclusion verification: `discussions/skills/homeostasis/2026-03-10T00-00-00Z__2026-03-11T00-00-00Z/inclusion_verification_2026-03-10_system_discovery_homeostasis.md`

## Root Systems

The initial root candidates are:

1. `host`
2. `codex`
3. `spawn`

These are not assumed to be FSMs yet. They are first treated as root systems. Each root may later prove to be:

- an FSM,
- a system containing multiple FSMs,
- or a mixed control/runtime substrate that only becomes legible after downstream crawl.

We do not start from leaf artifacts. We start from roots and crawl outward.

## Core Principle

Reality updates the model immediately.

If a finding documents an undisclosed operation, undisclosed controller, new actuator, new subordinate, new state surface, or any other identity-changing fact, that finding mutates the live model immediately. It is not blocked behind promotion because it is a live fact.

Promotion is reserved for two things only:

1. `identity schema fidelity`
2. `applied-control fidelity`

Everything else belongs to the live operational loop.

## Discovery Method

### 1. Scope roots by identity

For each root, build `IDENTITY` from identifiable aspects:

- `scope_root` or `control_root`
- boundary
- purpose
- authority owner
- subordinates
- controllers
- actuators
- observers
- writers
- persistent state surfaces
- produced artifacts
- consumers
- ingress
- egress
- external dependencies

Every scoped system must define a root anchor even if no enclosing git repository exists.

If a git root exists, it can be used as the scope anchor.

If no git root exists, define an explicit `scope_root` or `control_root` anyway, anchored by:

- canonical path or identifier
- declared scope boundary
- authority owner
- control reach

The absence of `.git` is a finding. It is not the absence of a root.

### 2. Test FSM fit

For each root, ask:

- does it have bounded named states?
- does it have bounded transitions?
- does it have guards?
- does it have controllers or actuators that move state?
- does it have observable outputs tied to transitions?

If yes, treat it as an FSM.

If no, keep it as a root system and continue crawling downstream until the internal FSMs or stateful subsystems become clear.

### 3. Process-crawl downstream

Once the root identity is defined, crawl downstream meticulously through:

- services
- operations
- controllers
- actuators
- observers
- runtime paths
- state surfaces
- artifacts
- dependencies
- consumers
- gates
- rollback paths

At each step record:

- what exists
- what it does
- who owns it
- what state it carries
- what transitions it permits
- what it produces
- what consumes it
- what relationship it introduces
- what control is applied
- what control is missing

The crawl is the mechanism that forces the ontology into existence. We do not try to finalize a detached abstract ontology before crawl.

## Live Substrates

The operational substrate has three coupled live surfaces:

1. `relationship.current`
2. `identity.current`
3. `applied_control.current`

These are live truth surfaces, not just review artifacts.

### Relationship substrate

If something is observable, it is added immediately to a relationship substrate:

- canonical portable form: `relationship.current.v1.json`
- graph/query projection: `neo4j` or equivalent

`neo4j` is a projection and traversal surface, not the authority by itself.

Minimum relationship fields:

- `subject`
- `predicate`
- `object`
- `observed_at`
- `source_ref`
- `evidence_ref`
- `observation_mode`
- `status`
- `confidence`
- `affects_identity`
- `affects_control`
- `identity_effect`

Useful `status` values:

- `observed`
- `inferred`
- `undisclosed`
- `superseded`
- `invalidated`

Useful `identity_effect` values:

- `none`
- `expand`
- `reclassify`
- `retire`
- `unknown`

### Identity substrate

`identity.current` is the accepted live operational identity of a root or downstream scoped system.

It is not merely authored prose. It is a materialized operational truth surface derived from findings and relationships.

Conceptually:

`identity.current = f(findings, relationship.current, accepted observations)`

An undisclosed operation immediately becomes:

- observed,
- identity-changing,
- unknown in control space,
- and requiring re-analysis.

`identity.schema` is the promoted representation contract derived from crawl findings and applied-control findings. If live identity outruns the current schema, the schema is known-incomplete until updated.

### Applied-control substrate

`applied_control.current` describes what control exists over the current live identity:

- what is controlled,
- how it is controlled,
- through which controller and actuator,
- with what measures,
- with what intended outputs and byproducts,
- and what remains uncontrolled or ambiguous.

## Closed Loops

### Loop 1: Relationship loop

`finding -> relationship.current mutation -> relationship_delta`

This loop captures newly observed structure as soon as it is seen.

### Loop 2: Identity loop

`relationship.current -> identity.current -> identity_delta`

Relationships are identity-bearing. A new or changed relationship can expand, reclassify, retire, or destabilize the known identity.

### Loop 3: Control loop

`identity.current mutation -> applied_control analysis -> applied_control delta`

When identity changes, control must be re-evaluated against the new truth.

### Combined homeostatic loop

`finding -> relationship mutation -> identity mutation -> control reassessment -> restored operational understanding`

This is homeostasis. Stability does not mean nothing changes. Stability means changes are absorbed and the system returns to a known state of understanding.

## Trigger Rule

The trigger rule is strict:

If a new finding affects accepted identity, run a new applied-control analysis.

Identity-changing findings include:

- new authority owner
- new subordinate
- new controller
- new actuator
- new observer
- new state surface
- new transition
- new service
- new produced artifact class
- new dependency that changes control boundaries
- undisclosed operation

Better evidence for an already-known fact does not trigger re-analysis by itself unless it changes the accepted identity.

## Promotion Boundary

Promotion does not gate live facts.

Promotion gates only these deltas:

1. `mutated identity schema update`
   - does the schema represent the mutated live identity with high fidelity?

2. `applied-control update`
   - does control do what it is meant to do,
   - the way it is meant to do it,
   - with the intended measures,
   - outputs,
   - and byproducts?

This yields two separate domains:

- live truth maintenance:
  - findings,
  - relationships,
  - live identity,
  - live control analysis

- promoted fidelity surfaces:
  - identity schema,
  - applied-control quality expectations

## Artifact Set

Minimum working artifact family:

- `finding.current.v1.json`
- `relationship.current.v1.json`
- `relationship.delta.v1.json`
- `identity.current.v1.json`
- `identity.delta.v1.json`
- `identity.schema.v1.json`
- `applied_control.current.v1.json`
- `applied_control.report.v1.json`

Intended roles:

- `finding.current`
  - raw observed facts and evidence-backed discoveries

- `relationship.current`
  - current relationship graph in portable canonical form

- `relationship.delta`
  - explicit change record between prior and current relationship state

- `identity.current`
  - live accepted operational identity

- `identity.delta`
  - explicit identity change record and re-analysis trigger

- `identity.schema`
  - promoted contract for representing identity faithfully

- `applied_control.current`
  - current control mapping against the live identity

- `applied_control.report`
  - reviewable and comparable control findings

## Discovery-to-Accuracy Procedure

For each root (`host`, `codex`, `spawn`):

1. establish initial identity from directly identifiable aspects
2. start downstream process crawl
3. emit findings
4. update `relationship.current`
5. materialize `identity.current`
6. compute `identity.delta`
7. if identity changed, run `applied_control` analysis
8. emit `applied_control.current` and `applied_control.report`
9. continue crawl until no new identity-changing findings are observed for the current scope window

This does not mean the system is finished. It means the current scope has reached temporary homeostasis.

## What Counts as Accuracy

An accurate view of the system means:

- observable relationships are represented quickly,
- live identity matches observed reality,
- unknowns are explicit rather than hidden,
- undisclosed operations become visible immediately,
- control is reassessed whenever identity changes,
- schemas faithfully represent the live identity,
- and graph projections remain aligned with canonical JSON relationship state.

Accuracy is not static completeness. Accuracy is truthful, continuously maintained alignment with the real system.

## What This Prevents

This model prevents:

- leaf-first modeling without roots
- stale documentation pretending to be operational truth
- promotion-gating of live observations
- hidden undisclosed operations
- control analysis running against obsolete identity
- graph stores becoming accidental authority surfaces

## Near-Term Direction

The next packet should define the root-system discovery substrate for:

1. `host`
2. `codex`
3. `spawn`

Its job is to make the downstream crawl explicit and bounded, not to jump ahead to leaf contracts.

Once root discovery is stable, the missing bootstrap object family can be defined against the discovered structure instead of speculation.
