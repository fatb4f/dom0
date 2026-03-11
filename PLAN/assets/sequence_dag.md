# Root-Level Analysis Sequence DAG

Machine-readable equivalent:
- `assets/workflow.json`

## Nodes

1. `N0_objective`
- Input: approved problem statement from `PLAN/README.md`.
- Output: bounded analysis target and success criteria.

2. `N1_source_collection`
- Input: `dom0/homeostasis` 2026-03-06, 2026-03-07, 2026-03-10 artifacts and `dom0/asset-control-model` artifacts.
- Output: evidence-backed source inventory for terminology and control-model analysis.

3. `N2_homeostasis_terms`
- Input: collected source inventory.
- Output: D1 homeostasis term inventory.

4. `N3_acm_terms`
- Input: collected source inventory.
- Output: D2 ACM term inventory.

5. `N4_crosswalk`
- Input: D1 and D2.
- Output: D3 terminology crosswalk and gap register.

6. `N5_root_scope`
- Input: D3 plus ACM invariants.
- Output: D4 root candidate and scope semantics.

7. `N6_relationship_substrate`
- Input: D4.
- Output: D5 relationship substrate definition.

8. `N7_identity_substrate`
- Input: D5.
- Output: D6 identity substrate definition.

9. `N8_applied_control_substrate`
- Input: D6 plus ACM promotion semantics.
- Output: D7 applied-control and promotion-boundary definition.

10. `N9_methodology_workflow`
- Input: accepted D1-D7.
- Output: D8 strict methodology and workflow for operationalizing homeostasis.

11. `N10_gate_review`
- Input: D1-D8 deliverables and evidence tables.
- Output: implementation readiness decision.

## Edges

- `N0 -> N1 -> N2 -> N3 -> N4 -> N5 -> N6 -> N7 -> N8 -> N9 -> N10`
- `N4 -> N2|N3` if terminology collisions remain unresolved
- `N6 -> N5` if relationship semantics require undefined root scope
- `N7 -> N6` if identity semantics require unresolved relationship fields
- `N8 -> N7` if control semantics require unresolved identity semantics
- `N9 -> N5|N6|N7|N8` if workflow steps rely on undefined substrate concepts

## Notes

- This DAG is static-analysis only.
- No sweep or runtime-liveliness collection is required for this objective.
- Promotion is out of scope; this is a working-copy planning substrate.
- Trust is localized to `/home/_404/src/dom0`; no external repo state participates in this DAG.
