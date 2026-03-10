# Homeostasis: Codex-Review Operational Angles

## Scope

Operational angles for `codex-review` in the `homeostasis` model, with optional cloud-worker expansion.

## Codex-Review Angles

1. Policy adjudicator
- Consume `introspect.skills.snapshot.json` and opponent findings.
- Emit per-skill decisions: `PASS|FAIL|UNKNOWN`.

2. Drift triage engine
- Classify findings into:
  - `contract_break`
  - `staleness`
  - `runtime_signal`
  - `doc_mismatch`

3. Evidence gate normalizer
- Enforce no actionable finding without `evidence_refs[]`.
- Reject low-quality findings from downstream mutation paths.

4. Opponent finding resolver
- Resolve `suspected_break` into `confirmed_break|no_break`.
- Attach rationale and confidence updates.

5. Action synthesis
- Generate follow-up artifacts:
  - `backlog.json` tasks
  - issue drafts
  - patch proposals

6. Feedback-loop tuner
- Track false positives/negatives.
- Recommend threshold/rule changes for `homeostasis` capabilities.

7. Skill lifecycle manager
- Recommend promotion/deprecation transitions:
  - `draft -> validated -> stable -> deprecated`

## Optional Cloud-Worker Angles

1. Parallel adversarial execution
- Run Hypothesis/jsonschema/pytest suites across many skills concurrently.

2. Heavy journal replay
- Offload expensive log correlation/pattern extraction jobs.

3. Cross-host federation
- Aggregate multiple snapshots to identify systemic drift.

4. Canary policy validation
- Shadow-test new gate policies before local enforcement.

5. Backfill analytics
- Compute trends: break-rate, staleness-rate, MTTR per skill.

## Governance Boundary

1. Keep gating authority local (`spawn` + `codex-review`).
2. Use cloud workers for compute-heavy verification only.
3. Keep mutation rights local; cloud outputs remain advisory/evidence-only.

## Recommended Near-Term Sequence

1. Start local-only codex-review adjudication.
2. Add cloud parallel execution for adversarial suites.
3. Keep cloud in shadow mode first, then promote selected checks.
