# Discovery-Phase Planning Process

## Purpose

This reference captures the reusable planning process implied by the plan-iteration dialogue, external review, and final revised plan.

It is not a runtime design document. It is a planning-method reference for discovery-heavy work where:

- the system is only partially understood,
- evidence can change the accepted model,
- control analysis must be rerun when accepted identity changes,
- and promotion hardens fidelity rather than blocking discovery.

## When To Use It

Use this process when all of the following are true:

- the problem is discovery-heavy rather than implementation-heavy,
- roots or scope anchors are still hypotheses,
- ontology is unstable,
- evidence can materially change the accepted model,
- and one-pass deliverables would hide reiteration rather than support it.

Do not use it as the default for straightforward implementation plans with stable inputs and known ownership.

## Core Inversion

Do not start by enumerating entities or leaf artifacts.

Start by defining:

1. the operational subsystem model,
2. the epistemic/governance state space,
3. the operating planes that host that state,
4. the admission logic for accepted-state mutation,
5. the anchor admissibility rules,
6. only then the discovery anchors and downstream crawl.

This prevents the plan from collapsing:

- evidence into accepted state,
- graph shape into identity,
- identity into control,
- and discovery into premature governance artifacts.

## Planning Unit

The planning unit is `micro_plan`.

The output unit is `artifact`.

Promotion units remain narrow:

- `schema_fidelity`
- `applied_control_fidelity`

So the process is not:

- finish a deliverable,
- move on,
- never revisit it.

It is:

- define a bounded question,
- emit the needed artifacts,
- reach temporary epistemic quiescence under current evidence,
- reopen when admitted deltas materially change the accepted model.

## Composed Model

The reusable model has two coupled parts.

### Operational subsystem model

- `runtime_environment`
- `codex_local_agent`
- `codex_cloud_worker`
- `orchestration_daemon`

This layer must define:

- hypothesis to entity mapping
- per-entity identity requirements
- state variables
- interfaces and channels
- lifecycle transitions
- disturbance and fault classes

### Epistemic / control / governance model

The reusable state model is:

```text
ontic_state
  -> evidentiary_state
  -> admission_or_reduction
  -> accepted_relationship_state
  -> accepted_identity_state
```

Supervisory overlays:

```text
accepted_identity_state
  -> applied_control_state

accepted_identity_state
  -> fidelity_review_state

applied_control_state
  -> fidelity_review_state
```

### Meaning of each layer

- `ontic_state`
  - what is actually happening in the world
- `evidentiary_state`
  - what has been observed, inferred, or reported with provenance
- `accepted_relationship_state`
  - the canonical relationship surface of the model
- `accepted_identity_state`
  - the accepted operational state estimate
- `applied_control_state`
  - the current control interpretation and gap model
- `fidelity_review_state`
  - schema/control review state used for hardening, not discovery gating, and treated as a supervisory overlay

`applied_control_state` and `fidelity_review_state` are supervisory states, not epistemic strata.

## Gate Model

This planning process assumes three gates, not two.

### 1. Ingestion gate

Question:

- can this finding enter the evidentiary layer?

### 2. Acceptance gate

Question:

- is this evidence strong and coherent enough to mutate accepted relationship or accepted identity state?

### 3. Promotion gate

Question:

- does schema fidelity or applied-control fidelity need to be accepted, rejected, or revised?

This is the minimum structure needed to avoid letting "live" findings bypass model discipline.

## Discovery Anchors

Discovery starts from candidate anchors, not metaphysical roots.

Examples from the current plan:

- `runtime_environment`
- `codex`

These are treated as:

- candidate scope roots,
- candidate control roots,
- bounded starting anchors for crawl,

not permanently settled ontology.

They may later be:

- confirmed,
- split,
- merged,
- reclassified,
- or retired.

`spawn` is not assumed to be a peer anchor at the start. It should emerge later as:

- a subordinate/control surface under `runtime_environment`,
- a subordinate/control surface under `codex`,
- or a separately admissible candidate only if the evidence forces that split.

## FSM Guidance

FSM fit is a probe, not the base ontology.

Use FSM interpretation only where a local region actually has:

- bounded named states,
- bounded transitions,
- guards,
- controllable transition paths,
- and observable outputs.

Otherwise keep the subject as:

- a rooted system,
- a supervisory loop,
- an asynchronous process cluster,
- or another non-FSM substrate.

## Recommended Micro-Plan Sequence

This sequence is reusable for discovery-phase work:

### MP-00 - State-space definition

Define:

- operational subsystem entities
- hypothesis/entity mapping
- operational state variables
- interfaces and channels
- operational transitions
- disturbance and fault taxonomy
- state taxonomy,
- transition rules,
- authority rules,
- ingestion rules,
- acceptance rules,
- re-analysis triggers,
- closure conditions.

### MP-01 - Plane definition and anchor admissibility

Define:

- plane mapping,
- plane operating model,
- plane transition constraints,
- projection boundaries,
- anchor admissibility rules.

### MP-02 - Candidate root declaration

Define:

- initial anchor hypotheses and admitted root candidates,
- `scope_root`,
- `control_root`,
- root boundaries,
- crawl rules.

### MP-03 - Controller arbitration

Define:

- controller catalog,
- control scope map,
- precedence rules,
- conflict matrix,
- tie-break rules.

### MP-04 - Identity scoping

Define:

- entity facts,
- provisional identity hypotheses,
- FSM-fit assessment,
- unresolved identity gaps.

### MP-05 - Relationship substrate bootstrap

Define:

- evidentiary normalization,
- relationship admission/reduction,
- accepted identity materialization,
- relationship deltas,
- identity-effect rules,
- projection rules.

### MP-06 - Applied-control gap loop

Define:

- applied-control current state,
- gap register,
- controller findings,
- re-analysis rules.

### MP-07 - Fidelity gates

Define:

- schema fidelity review,
- applied-control fidelity review,
- methodology/workflow projection,
- implementation readiness rules.

## Required Micro-Plan Fields

Each micro-plan should answer:

- question being resolved
- roots or anchors in scope
- current accepted-state assumptions
- discovery method or crawl path
- what evidence can change accepted state
- artifacts emitted
- reiteration triggers
- what is promotion-gated
- what allows temporary epistemic quiescence

## Closure Semantics

Do not say "done" when the process is only quiet.

Use:

- `temporarily closed under current evidence`
- or more precisely:
  - `temporary epistemic quiescence`

That means:

- no new admitted relationship delta,
- no new admitted identity delta,
- no new material applied-control delta

within the current scope window.

It does not mean the real system is stable or complete.

## Invariants

The reusable invariants are:

- define state space before ontology
- define planes before discovery
- keep the model layered and partially observable
- treat evidence ingestion as immediate
- mutate accepted state only through admission/reduction
- treat `relationship.current` as canonical inside the model, not reality
- treat `identity.current` as the accepted operational state estimate
- rerun applied-control analysis only on material accepted-identity delta
- treat graph storage as projection only
- keep promotion limited to fidelity hardening
- localize trust explicitly

## Anti-Patterns

Do not do the following:

- treat identity as world truth
- let raw findings directly rewrite accepted state
- treat relationship state as reality itself
- declare discovery anchors to be final roots too early
- assume the whole subject is an FSM before fit is proven
- describe temporary closure as equilibrium or stability

## Reuse Rule

This process is reusable when the planning problem is dominated by:

- discovery,
- correction,
- reiteration,
- and model hardening.

It should be simplified when:

- roots are settled,
- ownership is stable,
- evidence admission is already formalized,
- and the work is mostly implementation.
