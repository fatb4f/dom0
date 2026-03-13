# MP-00 State Space Model

## Purpose

This document defines the foundational composed state model for discovery-phase work under `dom0`.

It exists to prevent the discovery process from collapsing:

- ontic state into model state,
- evidence into accepted state,
- relationship state into identity,
- identity into applied control,
- accepted model state into promotion-gated fidelity review,
- and the operational subsystem itself into a purely epistemic sketch.

## Composed Foundation

`MP-00` defines two coupled models:

1. an operational subsystem model for:
   - `runtime_environment`
   - `codex_local_agent`
   - `codex_cloud_worker`
   - `orchestration_daemon`
2. an epistemic/control/governance model that tracks evidence, accepted relationships, accepted identity, applied control, and fidelity review about that operational system

The operational subsystem model is carried by:

- `system_entities.current`
- `hypothesis_entity_mapping.current`
- `operational_state_variables.current`
- `interface_and_channel_model.current`
- `operational_transition_model.current`
- `disturbance_fault_taxonomy.current`

The epistemic/control/governance model is carried by:

- `state_taxonomy.current`
- `state_transition_rules.current`
- `state_authority_rules.current`
- `evidence_ingestion_rules.current`
- `state_acceptance_rules.current`
- `reanalysis_triggers.current`
- `closure_conditions.current`
- `operational_epistemic_model_bridge.current`

## Operational Subsystem Model

The operational subsystem model makes the plant decomposition explicit and first-class. It does not yet admit discovery anchors; it defines the entity, variable, interface, transition, and disturbance surfaces that later discovery work will map into.

## Epistemic / Control / Governance Model

The system is modeled as a layered, partially observable operational state space:

```text
ontic_state
  -> evidentiary_state
  -> admission_or_reduction
  -> accepted_relationship_state
  -> accepted_identity_state

accepted_identity_state
  -> applied_control_state

accepted_identity_state
  -> fidelity_review_state

applied_control_state
  -> fidelity_review_state
```

Feedback path:

```text
applied_control_findings
  -> admission_or_reduction
  -> accepted_relationship_state
  -> accepted_identity_state
```

## Strata

### Ontic state

What is actually happening in the world whether or not the model has observed it.

### Evidentiary state

What has been observed, inferred, or reported with provenance.

### Accepted relationship state

The canonical relationship surface of the model after admission and reduction.

### Accepted identity state

The current justified operational state estimate derived from accepted lower-layer state.

### Applied-control state

The current control interpretation derived from accepted identity, controller rules, observed effects, unresolved unknowns, and control conflicts.

### Fidelity review state

The governance layer that reviews schema fidelity and applied-control fidelity without blocking evidence ingestion. It is a supervisory overlay, not the terminal layer of plant state.

## Gates

### Ingestion gate

Determines whether a finding may enter evidentiary state.

### Acceptance gate

Determines whether evidentiary state may mutate accepted relationship or accepted identity state.

### Promotion gate

Determines whether fidelity-review artifacts may be accepted, rejected, or revised.

## Authority

- Ontic state is real, but not directly authoritative inside the model.
- Evidentiary state is the canonical evidence ledger.
- Accepted relationship state is authoritative inside the model for relationships.
- Accepted identity state is the accepted operational state estimate, not world truth.
- Applied-control state is the canonical current control interpretation.
- Fidelity review state governs representation/control quality only and remains parallel to accepted/control state rather than replacing them.
- Projection systems such as Neo4j are never authority surfaces.

## Invariants

- Evidence ingestion is immediate.
- Accepted-state mutation is never raw; it always passes through admission or reduction.
- `relationship.current` is canonical inside the model, not reality itself.
- `identity.current` is derived, not freely authored.
- Applied control is rerun only on material accepted-identity delta.
- Temporary closure means temporary epistemic quiescence under current evidence, not equilibrium of the real system.
- Operational entities, variables, interfaces, lifecycle transitions, and disturbance classes must exist explicitly before discovery can claim a full state-space model.

## Discovery Boundary

No discovery anchor may be admitted before:

- the state strata are frozen enough to host it,
- the operating planes are defined,
- and anchor-admissibility rules exist.
