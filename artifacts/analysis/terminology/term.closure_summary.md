# Term Closure Summary

## Overview

- Nodes: 41
- Direct self-loops: 0
- Two-hop cycles: 52 paths across 7 groups
- Three-hop cycles: 12 paths across 2 groups
- Strongly connected components: 3

## Dominant Closure Component

- Node indices: [0, 4, 6, 21, 22]
- Terms: policy, service, assurance, state_space, fsm
- Internal edges: 20

## Strongly Connected Components

- SCC 0: undisclosed, unknown (nodes=2, edges=2)
- SCC 1: policy_surface, bootstrap_manifest (nodes=2, edges=4)
- SCC 2: policy, service, assurance, state_space, fsm (nodes=5, edges=20)

## Two-Hop Cycle Groups

- Group 0: policy -> service -> policy (supporting_paths=4)
- Group 1: policy -> assurance -> policy (supporting_paths=2)
- Group 2: undisclosed -> unknown -> undisclosed (supporting_paths=2)
- Group 3: service -> assurance -> service (supporting_paths=4)
- Group 4: service -> state_space -> service (supporting_paths=16)
- Group 5: service -> fsm -> service (supporting_paths=16)
- Group 6: policy_surface -> bootstrap_manifest -> policy_surface (supporting_paths=8)

## Three-Hop Cycle Groups

- Group 0: policy -> service -> assurance -> policy (supporting_paths=6)
- Group 1: policy -> assurance -> service -> policy (supporting_paths=6)
