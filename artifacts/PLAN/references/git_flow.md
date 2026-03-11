# Local Git Flow Reference

## Baseline model

- Trunk branch is `main`.
- Work is composed in an integration worktree/branch from an immutable base SHA.
- One logical commit per micro-plan closure slice or artifact-family change set.
- Run gates per micro-plan before stacking the next one.
- Promote via squash into `main`.
- Preserve integration lineage with a branch/tag for audit.

## Trust boundary

- This plan trusts only `/home/_404/src/dom0`.
- Do not pull planning truth from sibling repos or external working trees during execution of this packet.
- Localize derived references, drafts, and proofs under `artifacts/PLAN/` or adjacent localized copies inside `dom0`.

## Command skeleton

```bash
cd /home/_404/src/dom0
git worktree add ../wt-int-root-homeostasis-acm -b int/root-homeostasis-acm "$(git rev-parse HEAD)"
```

## Micro-Plan Commit Conventions

- Commit trailer fields:
  - `Micro-Plan: MP-<nn>`
  - `Gate: pass|needs-human`
  - `Base-Ref: <sha>`

## Conflict handling

- Resolve conflicts on the integration branch.
- Re-run gates after conflict resolution.
- If scope grows, split the micro-plan slice again instead of broadening one commit.
