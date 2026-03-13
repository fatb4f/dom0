# OpenAI Codex Control Surfaces

Date: 2026-03-12

## Purpose

This note summarizes the control surfaces OpenAI currently recommends around Codex and adjacent agent protocols, and places the downstream concepts and tools under the right surface.

The main question is:

> which surfaces are meant to carry rich Codex control, which are thinner interoperability layers, and which are adjacent ecosystem protocols rather than the primary Codex control plane?

## High-level read

OpenAI's current recommendation is centered on `App Server`.

The clean stack is:

- `App Server`
  - the recommended rich Codex control plane
- `codex-app` / IDE clients / local clients
  - clients of that control plane
- `Codex web`
  - cloud worker plus App Server runtime
- `Codex Exec` and `SDK`
  - automation, CI, and batch execution surfaces
- `MCP`
  - thinner interoperability surface with semantic loss
- `Apps SDK`, `Agents SDK`, `ACP`, `A2A`
  - adjacent ecosystem surfaces, not the primary Codex control surface

## Matrix

| Surface | OpenAI-recommended role | Best for | Preserves full Codex session semantics? | Main limits / caveats | Downstream concepts and tools |
|---|---|---|---|---|---|
| `Codex App Server` | Primary rich integration surface | Full local or hosted Codex control, rich UI clients, thread/turn lifecycle, approvals, multi-agent control, streaming events | Yes, this is the main harness surface | Requires a client; protocol/client work is heavier than a plain SDK | threads, turns, approvals, config/auth, diffs, skills, MCP integrations, multi-agent events |
| `codex-app` | Desktop client over App Server | Interactive multi-agent use, worktrees, rich review flows, automations, coordination | Mostly yes, as a client of App Server | GUI product surface; not the protocol authority itself | worktrees, skills, automations, rich review UX |
| `codex-cli` | Terminal client and utility surface | Local terminal usage, TUI workflows, `app-server`, `exec`, `mcp-server`, schema generation | Partly; some CLI modes expose the harness directly, others are thinner command surfaces | Public CLI commands do not equal the full app feature surface | `codex app-server`, `codex exec`, `codex mcp-server`, schema generation, features, local config |
| `Codex web` | Hosted/cloud Codex runtime | Background tasks, cloud execution, repo-connected environments, PR-oriented workflows | Yes at runtime, but surfaced through web/backend rather than local stdio | Hosted environment and backend mediation; not the local authority surface | cloud tasks, PRs, background runs, containerized workspaces |
| `Codex Exec` | Lightweight non-interactive execution surface | CI, scripts, single-run automation, batch-like local task execution | No, not the full rich session model | One-off completion-oriented surface, not a full client protocol | logs, exit codes, automation hooks |
| `Codex SDK` | Programmatic automation surface | Server-side tooling, CI/batch orchestration, embedding Codex into other systems | No, smaller surface than App Server | Narrower than App Server; not the full UI/event/control surface | local agent control from code, CI jobs, automation orchestration |
| `MCP` / `codex mcp-server` | Interop surface | Using Codex from existing MCP ecosystems and tools | No | OpenAI explicitly treats it as a thinner surface; richer Codex semantics can collapse or be lost | tool calls, MCP clients, lighter external integrations |
| `Apps SDK` | ChatGPT app extension surface built on MCP | Extending ChatGPT apps with app/tool integrations | No | Not the primary Codex harness; app-extension surface instead | ChatGPT apps, MCP-backed app tools |
| `Agents SDK` | Adjacent programmable agent-building surface | Building broader agent systems; can interoperate with MCP surfaces | No | Broader agent ecosystem surface, not the preferred full Codex harness | agent orchestration, MCP-client usage, external systems |
| `ACP` | Domain protocol | Agentic commerce scenarios | No | Domain-specific protocol, not the recommended Codex primary control plane | commerce workflows, external protocol interoperability |
| `A2A` | Neutral cross-agent interoperability concept | Future cross-provider agent coordination | No current Codex-first recommendation | Not presented as the main Codex control surface | cross-agent interoperability, external ecosystems |

## Recommended hierarchy

### 1. Use App Server first when you need full Codex control

OpenAI's current architecture writing places `App Server` at the center of the Codex harness.

Use it when you need:

- thread lifecycle
- turn lifecycle
- approvals
- tool mediation
- config/auth
- multi-agent behavior
- stable rich-client event streams

### 2. Use `codex-app` and other clients as App Server clients

The app is not the protocol authority. It is the richest user-facing client over the underlying harness.

This is where OpenAI currently concentrates:

- multi-agent coordination UX
- worktrees
- automations
- rich review and supervision flows

### 3. Use `Codex web` when the execution substrate should be hosted

`Codex web` should be understood as:

- a cloud/container runtime
- hosting App Server inside the worker
- surfacing those results through web/backend channels

So it is the right place for:

- background runs
- hosted repo-connected execution
- PR and cloud task workflows

### 4. Use `Exec` and the `SDK` for automation, CI, and batch

This is the recommended programmable/non-interactive path.

Use these when you want:

- single-run automation
- CI jobs
- batch execution
- embedding Codex into existing server-side workflows

### 5. Use MCP only when MCP compatibility is the priority

OpenAI's recommendation is not "use MCP as the main Codex control plane."

It is:

- use App Server for the full harness
- use MCP when you need MCP compatibility

That means MCP should be treated as a thinner adapter boundary that may lose:

- fine-grained session semantics
- richer diff/progress behavior
- some Codex-specific control surfaces

## Downstream concepts and tools

These concepts fit under the surfaces above.

### Under App Server / Codex clients

- threads
- turns
- approvals
- diffs
- auth/config
- review mode
- multi-agent control
- thread persistence and rollback

### Under app/product clients

- worktrees
- automations
- app-level multi-agent supervision
- richer review UX
- desktop/web orchestration views

### Under automation surfaces

- CI tasks
- batch jobs
- scripted execution
- server-side orchestration

### Under shared instruction/customization surfaces

- `AGENTS.md`
- skills
- local/user config
- repo-local policy hints

### Under interoperability surfaces

- MCP tool servers
- ChatGPT app integrations
- external agent/tool adapters

## Practical recommendation

If the goal is to build around OpenAI's recommended control surfaces, the best default stack is:

1. `App Server` for rich Codex control
2. `codex-app` or another client for human-facing interaction
3. `Exec` and `SDK` for automation, CI, and batch
4. `MCP` only where interoperability matters more than full Codex semantics
5. treat `ACP` and `A2A` as adjacent protocol/ecosystem concerns, not the primary Codex control plane

## dom0 implication

This reinforces the current `dom0` conclusion:

- do not rebuild inner agent/runtime control if OpenAI already provides it through `App Server` and the SDK
- keep custom effort concentrated in:
  - policy
  - admission
  - observability
  - lineage
  - orchestration

## Sources

- OpenAI: [Unlocking the Codex harness: how we built the App Server](https://openai.com/index/unlocking-the-codex-harness/)
- OpenAI Developers: [Codex App Server](https://developers.openai.com/codex/app-server/)
- OpenAI Developers: [Codex web](https://developers.openai.com/codex/cloud/)
- OpenAI: [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/)
- OpenAI: [Codex is now generally available](https://openai.com/index/codex-now-generally-available/)
- OpenAI: [OpenAI co-founds the Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation)
- OpenAI Developers: [OpenAI for developers](https://developers.openai.com/)
