# System Discovery And Homeostasis Program DAG

Machine-readable equivalent:
- `artifacts/PLAN/assets/workflow.json`

## Program Model

- Program: `system_discovery_and_homeostasis`
- Planning unit: `micro_plan`
- Output unit: `artifact`
- Promotion unit: `schema_fidelity` and `applied_control_fidelity`
- Closure model: `temporary_epistemic_quiescence_under_current_evidence`
- Architectural form: `rooted_event_sourced_dual_loop_homeostatic_control_system`
- Discovery entrypoint: after `MP00_state_space_definition` and `MP01_five_plane_definition`

## State Space

- Ontic state: what is true in the world whether observed or not
- Evidentiary state: findings, provenance, evidence refs, confidence, timestamps
- Accepted relationship state: canonical relationship surface of the model
- Accepted identity state: deterministic materialized operational state estimate
- Applied-control state: current control interpretation derived from accepted identity
- Fidelity review state: schema and control quality review surfaces

## Planes

- Root plane: candidate root anchors, `scope_root`, `control_root`, root boundaries, crawl rules
- Observation plane: append-only findings, normalization, provenance, confidence, evidence refs, admission rules
- Relationship plane: canonical `relationship.current` and `relationship.delta`
- Identity plane: deterministic `identity.current` and `identity.delta` materialized views plus `entity_facts.current` and `fsm_fit.current`
- Control plane: `applied_control.current`, reports, controller arbitration, gap analysis, and fidelity entrypoints

## Nodes

1. `MP00_state_space_definition`
- Define the typed state space, admission rules, transition rules, authority rules, re-analysis triggers, and closure conditions.
- Outputs: `state_space.model`, `state_taxonomy.current`, `state_transition_rules.current`, `state_authority_rules.current`, `evidence_ingestion_rules.current`, `state_acceptance_rules.current`, `reanalysis_triggers.current`, `closure_conditions.current`.

2. `MP01_five_plane_definition`
- Map the accepted state taxonomy into the five operating planes and freeze projection boundaries.
- Outputs: `plane_mapping.current`, `plane_operating_model.current`, `plane_transition_constraints.current`, `projection_boundary_rules.current`.

3. `MP02_root_declaration`
- Resolve current candidate roots plus `scope_root`, `control_root`, root boundaries, and crawl rules.
- Outputs: `root_set.current`, `scope_root_map.current`, `control_root_map.current`, `root_boundary.current`, `root_crawl_rules.current`.

4. `MP03_root_controller_arbitration`
- Resolve controller precedence, invalid overlap, and tie-breaks across `host`, `codex`, and `spawn`.
- Outputs: controller arbitration artifacts.

5. `MP04_identity_scoping`
- Build the accepted identity estimate for each root candidate and assess FSM fit.
- Outputs: `entity_facts.current`, `identity.current`, `identity.delta`, `fsm_fit_assessment.current`.

6. `MP05_relationship_substrate_bootstrap`
- Normalize observations into evidentiary state, admit them into canonical relationships, and classify their identity effects.
- Outputs: `finding.log`, `finding.normalized`, `relationship.current`, `relationship.delta`, relationship capture rules.

7. `MP06_applied_control_gap_loop`
- Recompute applied-control understanding against accepted identity and relationship state.
- Outputs: `applied_control.current`, `applied_control.report`, control gap and re-analysis artifacts.

8. `MP07_fidelity_gates`
- Evaluate only the two promotion units: schema fidelity and applied-control fidelity, then derive workflow projection.
- Outputs: fidelity reviews plus `methodology_workflow_projection.current`.

9. `G00_program_review`
- Emit separate plan approval and implementation readiness states.

## Edges

- `MP00 -> MP01 -> MP02 -> MP03 -> MP04 -> MP05 -> MP06 -> MP07 -> G00`
- `MP01 -> MP00` when plane definition depends on unresolved state taxonomy, transition, or authority rules
- `MP02 -> MP01` when root discovery depends on unresolved plane mapping
- `MP03 -> MP02` when controller arbitration depends on unresolved root or scope-root declarations
- `MP04 -> MP03` when identity scoping depends on unresolved controller precedence
- `MP05 -> MP04` when relationship identity effects cannot be classified against accepted identity
- `MP06 -> MP04` when accepted identity changes during control analysis
- `MP06 -> MP05` when relationship findings introduce new identity-affecting edges
- `MP06 -> MP03` when control analysis discovers unresolved controller conflict or precedence drift
- `MP07 -> MP00` when fidelity review exposes missing state-space semantics
- `MP07 -> MP01` when accepted truth crosses planes without a defined host or boundary
- `MP07 -> MP04` when schema fidelity fails because accepted truth cannot be represented
- `MP07 -> MP06` when applied-control fidelity fails

## Reiteration Rule

- Any admitted delta that materially changes accepted identity reopens the relevant upstream micro-plan and re-triggers applied-control analysis.
- Observable relationships update `relationship.current` immediately and may reopen identity scoping.
- Temporary epistemic quiescence is lost as soon as an admitted identity-changing delta lands.

## Service Shape

- Always-on services:
  - finding intake
  - evidence admission reducer
  - relationship reducer
  - identity materializer
  - control analyzer
  - graph projector
- Supervisory services:
  - delta classifier
  - controller arbitrator
  - epistemic quiescence detector
  - promotion assessor

## Notes

- This program is static-analysis only.
- No sweep or runtime-liveliness collection is required for this objective.
- Plan approval does not imply implementation approval.
- Trust is localized to `/home/_404/src/dom0`; no external repo state participates in this program.
