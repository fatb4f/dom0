#!/usr/bin/env python3
"""Derive an indexed first-degree term relationship graph."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_node(
    term: str,
    role: str,
    nodes: list[dict[str, Any]],
    node_index_by_term: dict[str, int],
) -> int:
    idx = node_index_by_term.get(term)
    if idx is None:
        idx = len(nodes)
        node_index_by_term[term] = idx
        nodes.append(
            {
                "index": idx,
                "term": term,
                "roles": [role],
            }
        )
        return idx

    roles = nodes[idx]["roles"]
    if role not in roles:
        roles.append(role)
        roles.sort()
    return idx


def build_graph(seed_map: dict[str, Any]) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    node_index_by_term: dict[str, int] = {}
    edges: list[dict[str, Any]] = []

    for seed in seed_map["seeds"]:
        seed_idx = ensure_node(seed["seed_term"], "seed", nodes, node_index_by_term)
        nodes[seed_idx]["seed_family"] = seed["family"]
        nodes[seed_idx]["seed_categories"] = seed["categories"]

        for lexical in seed["lexical_field"]:
            target_idx = ensure_node(lexical["term"], "lexical_field_term", nodes, node_index_by_term)
            edges.append(
                {
                    "index": len(edges),
                    "source_index": seed_idx,
                    "target_index": target_idx,
                    "relationship_type": "lexical_field",
                    "weight": lexical["cooccurrence_count"],
                }
            )

        for relation in seed["first_degree_entity_relationships"]:
            target_idx = ensure_node(relation["entity_term"], "entity_term", nodes, node_index_by_term)
            edges.append(
                {
                    "index": len(edges),
                    "source_index": seed_idx,
                    "target_index": target_idx,
                    "relationship_type": "first_degree_entity",
                    "weight": relation["evidence_count"],
                }
            )

    adjacency: list[dict[str, Any]] = []
    outbound: dict[int, list[int]] = {idx: [] for idx in range(len(nodes))}
    inbound: dict[int, list[int]] = {idx: [] for idx in range(len(nodes))}
    for edge in edges:
        outbound[edge["source_index"]].append(edge["index"])
        inbound[edge["target_index"]].append(edge["index"])

    for node in nodes:
        adjacency.append(
            {
                "node_index": node["index"],
                "outbound_edge_indices": outbound[node["index"]],
                "inbound_edge_indices": inbound[node["index"]],
            }
        )

    return {
        "kind": "term.relationship_graph.v1",
        "source_ref": "seed.lexical_field.relationship_map.json",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
        "adjacency": adjacency,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-map", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    payload = build_graph(load_json(args.seed_map))
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
