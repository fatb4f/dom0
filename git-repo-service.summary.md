# Git Repo Service Summary

## What it is

This is the current shorthand for the proposed repo-activity intelligence/control-plane system.

The intended subject is a bounded repo set, not an unbounded webhook sink.

## Core model

The system should operate as:

`repo observation -> raw event ledger -> normalized repo event -> accepted work unit -> control decision -> worker actuation -> published result -> lineage`

That means the service is best understood as:

- an event-driven control plane
- over a defined repo set
- with asynchronous worker actuation
- and a first-class observability/lineage substrate

## Current architecture split

- source adapters
  - GitHub App webhooks
  - local git-hook relay
  - optional dirty-worktree detector
- base service layer
  - ingress/auth
  - normalization
  - subscription/policy lookup
  - context resolution
  - orchestration
  - result routing
- intelligence workers
  - Codex analysis
  - classification
  - artifact generation
- observability and lineage
  - event ledger
  - traces
  - repo timeline
  - findings index
  - artifact registry
  - ops metrics

## Control-theory framing

The important control objects are:

- `repo_set.current`
- raw evidentiary event state
- accepted normalized event state
- accepted work-unit state
- applied-control state
- governance/lineage state

The key invariants are:

- raw ingress is not canonical state
- local mutable work requires snapshot-manifest identity
- app-originated GitHub checks must not self-trigger
- the event ledger is authoritative for replay/dedup
- artifacts must carry lineage

## Current maturity

This is still a control sketch, not a fully assetized implementation model.

The highest-value next move is to define explicit controlled assets and then baseline them against ACM one by one, starting with the normalized repo-event surface.

Primary discussion sources live outside this repo:

- `/home/_404/src/discussions/repo-activity-intelligence/readme.md`
- `/home/_404/src/discussions/repo-activity-intelligence/control_model.md`
- `/home/_404/src/discussions/repo-activity-intelligence/acm_baseline.md`
