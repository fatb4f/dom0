# MP-00 Operational / Epistemic Bridge

`MP-00` now defines two coupled models rather than one flattened state chain.

## 1. Operational Subsystem Model

This model makes the plant decomposition explicit:

- `runtime_environment`
- `codex_local_agent`
- `codex_cloud_worker`
- `orchestration_daemon`

It defines:

- hypothesis/entity mapping
- entity identity requirements
- per-entity operational state variables
- interfaces and channels
- operational lifecycle transitions
- disturbance and fault classes

## 2. Epistemic / Control / Governance Model

This model governs how the system learns about, accepts, interprets, and reviews the operational system:

- `ontic_state`
- `evidentiary_state`
- `accepted_relationship_state`
- `accepted_identity_state`
- `applied_control_state`
- `fidelity_review_state`

The critical boundary is:

- operational entities are what discovery is about
- epistemic/control/governance state is how discovery is admitted, materialized, interpreted, and reviewed

## Coupling Rules

- observations from operational entities enter evidentiary state immediately
- accepted relationship and identity state mutate only through admission and reduction
- applied control is derived from accepted identity plus controller rules, observed effects, unresolved unknowns, and control conflicts
- fidelity review is a supervisory overlay, not the terminal layer of plant state
- projection systems are never canonical authority

## Result

`MP-00` should now be read as a composed foundation:

1. operational subsystem decomposition
2. epistemic/control/governance state model
3. coupling rules between them

That is the minimum honest basis for later discovery of `runtime_environment`, `codex`, and any later emergent candidates such as `spawn`.
