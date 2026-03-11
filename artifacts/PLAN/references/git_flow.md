# Local Git Flow Reference

## Baseline model

- Trunk branch is `main`.
- Work is composed in an integration worktree/branch from an immutable base SHA.
- One logical commit per micro-deliverable.
- Run gates per micro-deliverable before stacking the next one.
- Promote via squash into `main`.
- Preserve integration lineage with a branch/tag for audit.

## Trust boundary

- This plan trusts only `/home/_404/src/dom0`.
- Do not pull planning truth from sibling repos or external working trees during execution of this packet.
- Localize derived references, drafts, and proofs under `PLAN/` or adjacent localized copies inside `dom0`.

## Command skeleton

```bash
cd /home/_404/src/dom0
git worktree add ../wt-int-root-homeostasis-acm -b int/root-homeostasis-acm "$(git rev-parse HEAD)"
```

## Deliverable commit conventions

- Commit trailer fields:
  - `Deliverable: D-<id>`
  - `Gate: pass|needs-human`
  - `Base-Ref: <sha>`

## Conflict handling

- Resolve conflicts on the integration branch.
- Re-run gates after conflict resolution.
- If scope grows, split the deliverable again instead of broadening one commit.
