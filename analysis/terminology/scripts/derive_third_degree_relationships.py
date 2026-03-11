#!/usr/bin/env python3
"""Derive all third-degree relationships from an indexed term graph."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def is_simple_path(source_index: int, via_indices: list[int], target_index: int) -> bool:
    path_nodes = [source_index, *via_indices, target_index]
    return len(path_nodes) == len(set(path_nodes))


def build_third_degree(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = graph["nodes"]
    edges = graph["edges"]

    edges_by_source: dict[int, list[dict[str, Any]]] = {}
    for edge in edges:
        edges_by_source.setdefault(edge["source_index"], []).append(edge)

    relationships: list[dict[str, Any]] = []
    aggregated_pairs: dict[tuple[int, int], dict[str, Any]] = {}
    adjacency_targets: dict[int, set[int]] = {node["index"]: set() for node in nodes}

    for first_edge in edges:
        first_via_index = first_edge["target_index"]
        for second_edge in edges_by_source.get(first_via_index, []):
            second_via_index = second_edge["target_index"]
            for third_edge in edges_by_source.get(second_via_index, []):
                source_index = first_edge["source_index"]
                target_index = third_edge["target_index"]
                via_indices = [first_via_index, second_via_index]

                if not is_simple_path(source_index, via_indices, target_index):
                    continue

                relationship = {
                    "index": len(relationships),
                    "source_index": source_index,
                    "via_indices": via_indices,
                    "target_index": target_index,
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
                relationships.append(relationship)
                adjacency_targets[source_index].add(target_index)

                pair_key = (source_index, target_index)
                pair = aggregated_pairs.get(pair_key)
                if pair is None:
                    pair = {
                        "index": len(aggregated_pairs),
                        "source_index": source_index,
                        "target_index": target_index,
                        "via_paths": [],
                        "supporting_relationship_indices": [],
                    }
                    aggregated_pairs[pair_key] = pair

                via_path = relationship["via_indices"]
                if via_path not in pair["via_paths"]:
                    pair["via_paths"].append(via_path)
                    pair["via_paths"].sort()
                pair["supporting_relationship_indices"].append(relationship["index"])

    adjacency = []
    for node in nodes:
        adjacency.append(
            {
                "node_index": node["index"],
                "third_degree_target_indices": sorted(adjacency_targets[node["index"]]),
                "outbound_relationship_indices": sorted(
                    relationship["index"]
                    for relationship in relationships
                    if relationship["source_index"] == node["index"]
                ),
                "inbound_relationship_indices": sorted(
                    relationship["index"]
                    for relationship in relationships
                    if relationship["target_index"] == node["index"]
                ),
            }
        )

    return {
        "kind": "term.third_degree_relationships.v1",
        "source_ref": "term.relationship_graph.json",
        "node_count": len(nodes),
        "third_degree_relationship_count": len(relationships),
        "third_degree_pair_count": len(aggregated_pairs),
        "third_degree_relationships": relationships,
        "third_degree_pairs": list(aggregated_pairs.values()),
        "adjacency": adjacency,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    payload = build_third_degree(load_json(args.graph))
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
