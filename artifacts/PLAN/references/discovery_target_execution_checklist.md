# Discovery Target Execution Checklist

## Purpose

This checklist turns the discovery-phase planning model into an execution procedure for a single target hypothesis.

It should be used only after:

- `MP-00` is temporarily closed under current evidence,
- `MP-01` is temporarily closed under current evidence,
- `system_entities.current`, `operational_state_variables.current`, and `interface_and_channel_model.current` exist,
- `hypothesis_entity_mapping.current` exists,
- and `anchor_admissibility_rules.current` exists.

## Initial Target Set

Start with:

1. `runtime_environment`
2. `codex`

Do not start with `spawn` as a peer target by default. Test `spawn` later only if the discovery crawl forces a separate admission.

Entities that are not current root targets must still remain modeled as supporting or subordinate operational entities during discovery.

## Per-Target Procedure

### 1. Establish target hypothesis

Record:

- target name
- why it is being tested
- current hypothesis class
  - candidate scope root
  - candidate control root
  - subordinate/control surface
  - unresolved

### 2. Run anchor admissibility test

Check whether the target can be admitted against:

- `system_entities.current`
- `hypothesis_entity_mapping.current`
- `operational_state_variables.current`
- state taxonomy
- plane mapping
- projection boundary rules
- anchor admissibility rules

Possible outcomes:

- admitted as candidate root
- rejected as candidate root
- deferred pending more evidence
- reclassified as subordinate/control surface

### 3. Bound the admitted target

If admitted, define:

- `scope_root`
- `control_root`
- root boundary
- crawl boundary
- initial crawl rules

### 4. Arbitrate controllers

Collect and classify:

- controllers
- actuators
- shared control surfaces
- precedence rules
- invalid overlaps
- tie-break requirements

### 5. Run identity-first crawl

Capture:

- boundary
- purpose
- authority owner
- subordinates
- controllers
- actuators
- observers
- writers
- state surfaces
- produced artifacts
- ingress/egress
- dependencies

Also test FSM fit only where local evidence justifies it.

### 6. Ingest findings

Append findings into evidentiary state:

- raw finding
- source ref
- evidence ref
- confidence
- observation mode
- timestamp

Do not mutate accepted state directly at this step.

### 7. Apply admission and reduction

Decide for each finding:

- evidentiary only
- mutates accepted relationship state
- mutates accepted identity state
- rejected from accepted-state mutation

Emit:

- `relationship.current`
- `relationship.delta`
- `identity.current`
- `identity.delta`

### 8. Recompute applied control

Compute current control understanding from:

- accepted identity
- controller rules
- observed effects
- unresolved unknowns
- control conflicts
- relationship state

Emit:

- `applied_control.current`
- `applied_control.report`
- control gaps
- controller findings

### 9. Check reiteration triggers

Reopen upstream work if discovery produced:

- new admissible root candidate
- scope/control root correction
- controller conflict drift
- material identity delta
- material relationship delta
- material applied-control delta

### 10. Evaluate temporary epistemic quiescence

The target reaches temporary epistemic quiescence only when:

- no new admitted relationship delta is pending,
- no new admitted identity delta is pending,
- no new material applied-control delta is pending,
- and unresolved unknowns are explicit rather than hidden.

## Suggested Artifact Bundle Per Target

- `target_hypothesis.current.json`
- `anchor_admissibility_assessment.current.json`
- `root_boundary.current.json`
- `root_crawl_rules.current.json`
- `controller_catalog.current.json`
- `identity.current.json`
- `identity.delta.json`
- `relationship.current.json`
- `relationship.delta.json`
- `applied_control.current.json`
- `applied_control.report.json`
- `target_quiescence_assessment.current.json`

## Initial Target Notes

### `runtime_environment`

Start by mapping:

- execution context
- process surfaces
- filesystem/state/config paths
- env surfaces
- supervisors
- timers
- buses
- external dependencies

### `codex`

Start by mapping:

- session surfaces
- prompt/context surfaces
- skills
- CLI and cloud delegation surfaces
- local state paths
- controllers
- actuators
- produced artifacts

### `spawn`

Do not admit `spawn` as a peer root candidate unless the earlier discovery shows it cannot be modeled cleanly as:

- a subordinate/control surface under `runtime_environment`, or
- a subordinate/control surface under `codex`

Admit it separately only if the evidence forces that split.
