#!/usr/bin/env python3
"""Derive closure-oriented cycle artifacts from an indexed term graph."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def rotate_min(sequence: list[int]) -> list[int]:
    rotations = [sequence[i:] + sequence[:i] for i in range(len(sequence))]
    return min(rotations)


def canonical_cycle_key(node_cycle: list[int]) -> tuple[int, ...]:
    return tuple(rotate_min(node_cycle))


def strongly_connected_components(node_count: int, edges_by_source: dict[int, list[dict[str, Any]]]) -> list[list[int]]:
    index = 0
    stack: list[int] = []
    on_stack: set[int] = set()
    indices = [-1] * node_count
    lowlinks = [0] * node_count
    components: list[list[int]] = []

    def strongconnect(node: int) -> None:
        nonlocal index
        indices[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        for edge in edges_by_source.get(node, []):
            target = edge["target_index"]
            if indices[target] == -1:
                strongconnect(target)
                lowlinks[node] = min(lowlinks[node], lowlinks[target])
            elif target in on_stack:
                lowlinks[node] = min(lowlinks[node], indices[target])

        if lowlinks[node] == indices[node]:
            component: list[int] = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)
                if member == node:
                    break
            components.append(sorted(component))

    for node in range(node_count):
        if indices[node] == -1:
            strongconnect(node)

    return sorted(components, key=lambda members: (len(members), members))


def build_closure(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = graph["nodes"]
    edges = graph["edges"]

    edges_by_source: dict[int, list[dict[str, Any]]] = {}
    for edge in edges:
        edges_by_source.setdefault(edge["source_index"], []).append(edge)

    direct_self_loops: list[dict[str, Any]] = []
    for edge in edges:
        if edge["source_index"] == edge["target_index"]:
            direct_self_loops.append(
                {
                    "index": len(direct_self_loops),
                    "node_index": edge["source_index"],
                    "edge_index": edge["index"],
                    "relationship_type": edge["relationship_type"],
                    "weight": edge["weight"],
                }
            )

    two_hop_cycles: list[dict[str, Any]] = []
    two_hop_groups: dict[tuple[int, ...], dict[str, Any]] = {}
    for first_edge in edges:
        source_index = first_edge["source_index"]
        via_index = first_edge["target_index"]
        if source_index == via_index:
            continue
        for second_edge in edges_by_source.get(via_index, []):
            target_index = second_edge["target_index"]
            if target_index != source_index:
                continue

            node_cycle = [source_index, via_index]
            cycle = {
                "index": len(two_hop_cycles),
                "node_cycle": node_cycle,
                "path_edge_indices": [first_edge["index"], second_edge["index"]],
                "path_relationship_types": [
                    first_edge["relationship_type"],
                    second_edge["relationship_type"],
                ],
                "path_weight": first_edge["weight"] + second_edge["weight"],
            }
            two_hop_cycles.append(cycle)

            cycle_key = canonical_cycle_key(node_cycle)
            group = two_hop_groups.get(cycle_key)
            if group is None:
                group = {
                    "index": len(two_hop_groups),
                    "node_cycle": list(cycle_key),
                    "supporting_cycle_indices": [],
                }
                two_hop_groups[cycle_key] = group
            group["supporting_cycle_indices"].append(cycle["index"])

    three_hop_cycles: list[dict[str, Any]] = []
    three_hop_groups: dict[tuple[int, ...], dict[str, Any]] = {}
    for first_edge in edges:
        source_index = first_edge["source_index"]
        first_via = first_edge["target_index"]
        if source_index == first_via:
            continue

        for second_edge in edges_by_source.get(first_via, []):
            second_via = second_edge["target_index"]
            if second_via in {source_index, first_via}:
                continue

            for third_edge in edges_by_source.get(second_via, []):
                target_index = third_edge["target_index"]
                if target_index != source_index:
                    continue

                node_cycle = [source_index, first_via, second_via]
                cycle = {
                    "index": len(three_hop_cycles),
                    "node_cycle": node_cycle,
                    "path_edge_indices": [
                        first_edge["index"],
                        second_edge["index"],
                        third_edge["index"],
                    ],
                    "path_relationship_types": [
                        first_edge["relationship_type"],
                        second_edge["relationship_type"],
                        third_edge["relationship_type"],
                    ],
                    "path_weight": first_edge["weight"] + second_edge["weight"] + third_edge["weight"],
                }
                three_hop_cycles.append(cycle)

                cycle_key = canonical_cycle_key(node_cycle)
                group = three_hop_groups.get(cycle_key)
                if group is None:
                    group = {
                        "index": len(three_hop_groups),
                        "node_cycle": list(cycle_key),
                        "supporting_cycle_indices": [],
                    }
                    three_hop_groups[cycle_key] = group
                group["supporting_cycle_indices"].append(cycle["index"])

    sccs = strongly_connected_components(len(nodes), edges_by_source)
    self_loop_nodes = {loop["node_index"] for loop in direct_self_loops}
    component_payloads: list[dict[str, Any]] = []
    for component in sccs:
        if len(component) == 1 and component[0] not in self_loop_nodes:
            continue
        component_set = set(component)
        component_edges = [
            edge["index"]
            for edge in edges
            if edge["source_index"] in component_set and edge["target_index"] in component_set
        ]
        component_payloads.append(
            {
                "index": len(component_payloads),
                "node_indices": component,
                "edge_indices": sorted(component_edges),
                "term_count": len(component),
                "edge_count": len(component_edges),
            }
        )

    return {
        "kind": "term.closure_cycles.v1",
        "source_ref": "term.relationship_graph.json",
        "node_count": len(nodes),
        "direct_self_loop_count": len(direct_self_loops),
        "two_hop_cycle_count": len(two_hop_cycles),
        "two_hop_cycle_group_count": len(two_hop_groups),
        "three_hop_cycle_count": len(three_hop_cycles),
        "three_hop_cycle_group_count": len(three_hop_groups),
        "strongly_connected_component_count": len(component_payloads),
        "direct_self_loops": direct_self_loops,
        "two_hop_cycles": two_hop_cycles,
        "two_hop_cycle_groups": list(two_hop_groups.values()),
        "three_hop_cycles": three_hop_cycles,
        "three_hop_cycle_groups": list(three_hop_groups.values()),
        "strongly_connected_components": component_payloads,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    payload = build_closure(load_json(args.graph))
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
