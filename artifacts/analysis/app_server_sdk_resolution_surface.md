# App Server + SDK Resolution Surface

## Statement

The current `codex` investigation suggests that `App Server` plus the client `SDK` provides the missing centralized runtime control surface that originally pressured `dom0` toward a broader custom system role.

This does not eliminate `dom0`.

It changes what `dom0` should own.

## High-level conclusion

The likely stable split is:

- `App Server`
  - local runtime control plane
  - thread/turn lifecycle
  - approvals and tool mediation
  - multi-agent orchestration
  - rich interactive session control

- `SDK`
  - non-interactive automation surface
  - CI and batch-job control surface
  - programmable orchestration entrypoint for execution

- `MCP`
  - thinner interoperability boundary
  - adapter surface with semantic loss relative to App Server

- `dom0`
  - policy layer
  - observability layer
  - pipeline orchestration policy
  - admission and work-unit control
  - lineage and reporting authority

## What this resolves

`dom0` no longer needs to be treated as the place that reimplements:

- inner agent runtime control
- thread/session lifecycle control
- local multi-agent runtime mechanics
- approval/tool execution primitives
- generic batch execution substrate

Those concerns now have a plausible supported home in `App Server` and the SDK.

## What remains custom

The remaining justified custom layer is the outer control and policy surface:

- subscription and repo admission policy
- event authority
- work-unit identity
- replay and idempotency policy
- orchestration policy across repos and jobs
- artifact lineage
- publication and suppression policy
- observability projections and reporting

So the unresolved center of gravity becomes:

`policy -> observability -> cross-repo control topology`

not

`rebuild the agent runtime`

## Resulting architectural split

The clean target shape is:

```text
Codex App Server
  -> authoritative local runtime control surface

Codex SDK
  -> CI / batch / automation execution surface

dom0
  -> policy, admission, observability, lineage, orchestration authority
```

## Implication for dom0

`dom0` should contract from a broad runtime substitute into a narrower and more principled control layer.

That means:

- less emphasis on rebuilding runtime mechanics
- more emphasis on policy and accepted-state boundaries
- more emphasis on observability and replayable lineage
- more emphasis on cross-project and cross-repo orchestration decisions

## Immediate design consequence

When deciding whether a responsibility belongs in `dom0`, use this filter:

- if it is runtime session or agent control, prefer `App Server`
- if it is CI/batch execution control, prefer the SDK
- if it is interop with reduced semantics, treat MCP as secondary
- if it is admission, lineage, replay, publication, or cross-repo policy, it still belongs in `dom0`

## Related local context

- [git-repo-service.summary.md](/home/_404/src/ops/control_plane/dom0/git-repo-service.summary.md)
- [asset-control-model.summary.md](/home/_404/src/ops/proposal_register/asset-control-model.summary.md)
- [app-server.summary.md](/home/_404/src/ops/execution_plane/codex/app-server.summary.md)
- [README.md](/home/_404/src/ops/control_plane/codex-app/PLAN/README.md)
