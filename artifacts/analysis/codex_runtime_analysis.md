# Codex Runtime Analysis

## Purpose

This document does two things:

1. Mirrors the current layered runtime model established from the Codex App Server and multi-agent pilot work.
2. Expands that model into a broader capability analysis using the official OpenAI API docs, the OpenAI Agents SDK for TypeScript docs and repo, the OpenAI Agents SDK for Python repo, and the App Server / Codex harness material.

This is a capabilities and layering analysis, not yet a final integration decision.

## Mirrored Current Layer Model

The clean layered model is:

- `App Server` = Codex-native session/control plane
- `ACP/A2A` = interoperable session/control plane
- `Agents JS` = in-process orchestration runtime
- `Sessions` = orchestration memory layer
- `Guardrails` = policy/tripwire layer
- `Structured Outputs` = payload contract layer
- `codexTool()` = Codex actuator inside the orchestrator
- `MCP` = tool/interoperability boundary

That means `openai-agents-js` is highly relevant to the packet, but as an orchestration-side comparison surface, not as a replacement for the App Server investigation. The native baseline remains Codex App Server, and the local Codex app pilot has already validated that baseline end-to-end.

So the packet should evolve to something like:

- `D3a` App Server vs Agents JS orchestration surface
- `D3b` App Server vs ACP/A2A control-plane surface
- `D4` semantic projection/loss across MCP and ACP/A2A boundaries
- `D5` where Guardrails, Sessions, and Structured Outputs attach in that stack

The important consequence is:

- use `App Server` as the highest-fidelity native control-plane reference
- use `Agents JS` to study orchestration patterns, memory, guardrails, and Codex-as-tool embedding
- use `ACP/A2A/MCP` as bridge/export layers where semantic loss must be measured explicitly

The next best move after this analysis is a compact surface taxonomy artifact, then a lossiness matrix:

- native App Server semantics
- what survives in Agents JS + `codexTool()`
- what survives in ACP/A2A
- what survives in MCP
- where Structured Outputs and Guardrails can harden the gaps

## Capability Baseline

The capability space falls into four major families:

1. `OpenAI API platform capabilities`
2. `Codex-native harness capabilities`
3. `Agents SDK orchestration capabilities`
4. `Interoperability and boundary capabilities`

They overlap, but they are not equivalent.

## OpenAI API Platform Capabilities

### Core concepts

The official API docs center the platform around the `Responses API` and a small set of stateful/runtime concepts:

- model invocation and output items
- conversation state and continuation
- tool invocation
- structured response shaping
- streaming and long-running execution paths

Operationally, the key point is that the platform already supports:

- `function calling` for system/tool integration
- `Structured Outputs` for schema-constrained payloads
- `conversation state` for stateful multi-turn execution
- `background mode` for longer-running tasks

This gives a general-purpose agent runtime substrate even before Codex-specific layers are added.

### Agents

The official `Agents` docs frame agent systems in terms of:

- `models`
- `tools`
- `instructions`

And the platform-level agent surface now includes:

- agent construction/deployment primitives
- tool-enabled reasoning loops
- voice and realtime paths
- evaluation and optimization surfaces

This is the platform layer that both Codex-native and SDK-driven flows sit on top of.

### Tools

The official `Tools` docs make an important distinction:

- the model can choose whether and when to call tools
- tools can be OpenAI-hosted, function-based, or MCP-based

The current tool surface includes:

- function calling
- built-in / hosted tools
- local and remote `MCP` servers

This is the main place where external capability enters the runtime loop.

### Run and scale

The `Run and scale` material matters because it turns “one-shot execution” into “operational runtime”:

- `conversation state` for state continuity
- `background mode` for long-running tasks
- streaming/evented interaction
- response lifecycle management

That makes the base API stack much closer to a durable agent platform than a stateless completion API.

## Codex-Native Harness Capabilities

### App Server as native control plane

The Codex App Server sits above the general API platform as a richer Codex-native harness.

From the local pilot work and the official App Server / harness material, the App Server gives:

- long-lived thread hosting
- turn lifecycle
- typed item/event streams
- approvals
- config/auth surfaces
- thread persistence and reconnect semantics
- native collaboration and multi-agent event surfaces

This is the highest-fidelity native control plane we currently have for Codex semantics.

### What the local pilot proved

The local Linux-port and CLI-backed investigation established:

- the app uses local `codex app-server` over stdio as its first-hop rich-client backend
- core runtime behavior is exposed through App Server methods and notifications
- with `multi_agent = true`, real collaboration tool calls occur over that same runtime path

Validated live collaboration lifecycle:

- `spawnAgent`
- `sendInput`
- `wait`
- `resumeAgent`
- `closeAgent`

So App Server is not hypothetical here. It is the validated native execution/control surface for local Codex runtime behavior.

## Agents SDK Capabilities

### Agents JS

The OpenAI Agents SDK for TypeScript is best understood as an orchestration runtime.

Its small primitive set is:

- `Agents`
- `Agents as tools / handoffs`
- `Guardrails`

And its documented feature set includes:

- built-in `agent loop`
- TypeScript-first orchestration
- agents as tools / handoffs
- guardrails
- function tools with schema generation and validation
- MCP server tool integration
- `Sessions`
- `Human in the loop`
- `Tracing`
- `Realtime Agents`

This is a strong orchestration surface, but it is not the same thing as a native external control plane.

### Agents Python

The Python SDK is conceptually parallel to Agents JS:

- same high-level multi-agent/orchestration framing
- same emphasis on handoffs, tools, guardrails, sessions, tracing, and MCP compatibility
- different host language and packaging surface

For this analysis, the Python SDK reinforces that the `Agents SDK` layer is a language-level orchestration/runtime family, not a Codex-specific session protocol.

### Orchestration patterns

The Agents JS guide material makes several orchestration capabilities explicit:

- `agents as tools`
- `handoffs`
- manager-style orchestration
- routing
- parallelization
- deterministic flows layered around model-driven flows

This is why the SDK is important to compare against App Server: it is already a serious orchestration surface, just not the same kind of surface.

## Guardrails, Sessions, and Structured Outputs

These three are important because they are often confused with the control-plane layer.

### Guardrails

Guardrails are the `policy/tripwire` layer.

Agents JS documents:

- `input guardrails`
- `output guardrails`
- `tool guardrails`

And failed checks trip a `tripwire` and halt the run.

That makes guardrails ideal for:

- policy enforcement
- fail-fast validation
- constraining tool execution
- human-approval insertion points

But guardrails are not themselves a session protocol.

### Sessions

Sessions are the `orchestration memory` layer.

In Agents JS, sessions persist and rehydrate conversational history for the runner. Built-ins include:

- `OpenAIConversationsSession`
- `MemorySession`
- `OpenAIResponsesCompactionSession`

This is similar in purpose to App Server thread continuity, but it lives one layer higher:

- `Sessions` = memory inside the orchestrator
- `App Server` = external hosted session/control surface

### Structured Outputs

Structured Outputs is the `payload contract` layer.

It matters because it hardens:

- plans
- handoff envelopes
- approval payloads
- gate decisions
- evidence bundles
- agent-to-agent messages

Structured Outputs does not replace orchestration or transport. It constrains the payloads moving through them.

## Codex as Actuator: `codexTool()`

The experimental Codex tool in Agents JS is a bridge from the orchestration runtime into Codex execution.

This means:

- `Agents JS` can orchestrate
- `codexTool()` can delegate execution into Codex
- but the surrounding orchestration still belongs to the SDK layer

So:

- `codexTool()` is not the main control plane
- it is a `Codex actuator` inside another orchestration layer

That is why the layering matters:

- `Agents JS + codexTool()` can drive Codex execution
- `App Server` still remains the richer Codex-native session/control plane

## Interoperability and Boundary Capabilities

### MCP

`MCP` is the tool/interoperability boundary.

It is important because:

- the model/runtime can access external capabilities through MCP
- it creates a practical bridge between native systems and interoperable tool surfaces

But it is also a lossy boundary:

- tool availability survives
- richer native session/control semantics may not

### ACP / A2A

`ACP/A2A` belongs on the session/control-plane stratum, not the tool stratum.

It resembles App Server structurally because it is about:

- long-lived sessions
- streaming interaction
- delegated workflows
- human/application/agent communication

But it is an interoperability surface, not the native Codex harness.

This is why `App Server` and `ACP/A2A` should be compared directly:

- both carry sessionful control semantics
- but one is native/high-fidelity and one is cross-system/interoperable

## Surface Taxonomy

### Highest-fidelity native surface

- `App Server`

Why:

- full Codex-native thread semantics
- approvals
- typed event model
- collaboration tool/event model
- config/auth/runtime integration

### Orchestration surfaces

- `Agents JS`
- `Agents Python`

Why:

- rich in-process orchestration
- handoffs / agents-as-tools
- sessions
- guardrails
- tracing
- human-in-the-loop

### Actuator surface

- `codexTool()`

Why:

- exposes Codex execution as a tool to the orchestrator

### Boundary / bridge surfaces

- `MCP`
- `ACP/A2A`

Why:

- interoperability
- cross-system communication
- tool access and session transport at reduced or transformed semantic fidelity

### Contract layer

- `Structured Outputs`

Why:

- payload hardening
- schema adherence
- contract stability across orchestration/control boundaries

## Practical Implications

### What should be treated as the native reference

Use `App Server` as the native reference for Codex runtime semantics.

That means:

- thread lifecycle
- approvals
- collaboration lifecycle
- turn/item events
- persistence/reconnect behavior

should all be modeled first in App Server terms.

### What should be treated as orchestration comparators

Use `Agents JS` and `Agents Python` as orchestration comparators.

Questions they answer:

- how much of the desired multi-agent behavior can be expressed in-process?
- where do sessions, guardrails, and tracing naturally live?
- when is Codex best used as an embedded actuator vs the primary session/control plane?

### What should be treated as bridge-loss studies

Use `MCP` and `ACP/A2A` for semantic projection analysis.

Questions they answer:

- what native Codex semantics survive export?
- what collapses to a generic common subset?
- what must be restored using payload contracts, guardrails, or local policy?

## Recommended Analytical Slices

### `D3a` — App Server vs Agents SDK orchestration surface

Focus:

- thread/session semantics vs session-memory semantics
- native collab lifecycle vs handoffs/agents-as-tools
- approvals vs human-in-the-loop / tool guardrails
- native event stream vs tracing/runtime callbacks

### `D3b` — App Server vs ACP/A2A control-plane surface

Focus:

- session lifecycle
- pause/resume
- streaming
- agent-to-agent interaction
- what counts as native-only vs interoperable

### `D4` — Semantic loss across MCP and ACP/A2A boundaries

Focus:

- which App Server semantics survive as-is
- which require flattening
- which require reconstruction via schema/policy/tracing

### `D5` — Guardrails, Sessions, Structured Outputs placement

Focus:

- where policy should live
- where continuity should live
- where contracts should be enforced
- how to use these to harden lossy bridge paths

## Current Working Position

The current best-supported position is:

- `App Server` is the highest-fidelity native Codex control plane
- `Agents JS` and `Agents Python` are strong orchestration runtimes
- `codexTool()` lets those orchestrators use Codex as an actuator
- `Guardrails` and `Sessions` are runtime-orchestration layers, not control-plane replacements
- `Structured Outputs` hardens payloads, not transports
- `MCP` and `ACP/A2A` are bridge/export layers where semantic loss must be measured explicitly

## Sources

- OpenAI API docs: https://developers.openai.com/api/docs
- Agents guide: https://developers.openai.com/api/docs/guides/agents
- Tools guide: https://developers.openai.com/api/docs/guides/tools
- Conversation state guide: https://developers.openai.com/api/docs/guides/conversation-state
- Background mode guide: https://developers.openai.com/api/docs/guides/background
- Function calling guide: https://developers.openai.com/api/docs/guides/function-calling
- Structured Outputs guide: https://developers.openai.com/api/docs/guides/structured-outputs
- OpenAI Agents SDK for TypeScript docs: https://openai.github.io/openai-agents-js/
- Agents JS repo: https://github.com/openai/openai-agents-js
- Agents Python repo: https://github.com/openai/openai-agents-python
- App Server / Codex harness article: https://openai.com/index/unlocking-the-codex-harness/
