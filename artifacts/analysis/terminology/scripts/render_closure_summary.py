#!/usr/bin/env python3
"""Resolve closure-cycle indices to terms and render summary artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_terms(indices: list[int], terms_by_index: dict[int, str]) -> list[str]:
    return [terms_by_index[index] for index in indices]


def build_summary(graph: dict[str, Any], closure: dict[str, Any]) -> dict[str, Any]:
    terms_by_index = {node["index"]: node["term"] for node in graph["nodes"]}

    direct_self_loops = [
        {
            **loop,
            "node_term": terms_by_index[loop["node_index"]],
        }
        for loop in closure["direct_self_loops"]
    ]

    two_hop_cycle_groups = [
        {
            **group,
            "node_terms": resolve_terms(group["node_cycle"], terms_by_index),
            "supporting_cycle_count": len(group["supporting_cycle_indices"]),
        }
        for group in closure["two_hop_cycle_groups"]
    ]

    three_hop_cycle_groups = [
        {
            **group,
            "node_terms": resolve_terms(group["node_cycle"], terms_by_index),
            "supporting_cycle_count": len(group["supporting_cycle_indices"]),
        }
        for group in closure["three_hop_cycle_groups"]
    ]

    strongly_connected_components = [
        {
            **component,
            "node_terms": resolve_terms(component["node_indices"], terms_by_index),
        }
        for component in closure["strongly_connected_components"]
    ]

    dominant_component = None
    if strongly_connected_components:
        dominant_component = max(
            strongly_connected_components,
            key=lambda component: (component["term_count"], component["edge_count"]),
        )

    return {
        "kind": "term.closure_summary.v1",
        "source_refs": [
            "term.relationship_graph.json",
            "term.closure_cycles.json",
        ],
        "node_count": graph["node_count"],
        "overview": {
            "direct_self_loop_count": closure["direct_self_loop_count"],
            "two_hop_cycle_count": closure["two_hop_cycle_count"],
            "two_hop_cycle_group_count": closure["two_hop_cycle_group_count"],
            "three_hop_cycle_count": closure["three_hop_cycle_count"],
            "three_hop_cycle_group_count": closure["three_hop_cycle_group_count"],
            "strongly_connected_component_count": closure["strongly_connected_component_count"],
        },
        "dominant_component": dominant_component,
        "direct_self_loops": direct_self_loops,
        "two_hop_cycle_groups": two_hop_cycle_groups,
        "three_hop_cycle_groups": three_hop_cycle_groups,
        "strongly_connected_components": strongly_connected_components,
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Term Closure Summary",
        "",
        "## Overview",
        "",
        f"- Nodes: {summary['node_count']}",
        f"- Direct self-loops: {summary['overview']['direct_self_loop_count']}",
        f"- Two-hop cycles: {summary['overview']['two_hop_cycle_count']} paths across {summary['overview']['two_hop_cycle_group_count']} groups",
        f"- Three-hop cycles: {summary['overview']['three_hop_cycle_count']} paths across {summary['overview']['three_hop_cycle_group_count']} groups",
        f"- Strongly connected components: {summary['overview']['strongly_connected_component_count']}",
        "",
    ]

    dominant = summary["dominant_component"]
    if dominant is not None:
        lines.extend(
            [
                "## Dominant Closure Component",
                "",
                f"- Node indices: {dominant['node_indices']}",
                f"- Terms: {', '.join(dominant['node_terms'])}",
                f"- Internal edges: {dominant['edge_count']}",
                "",
            ]
        )

    lines.extend(["## Strongly Connected Components", ""])
    for component in summary["strongly_connected_components"]:
        lines.append(
            f"- SCC {component['index']}: {', '.join(component['node_terms'])} "
            f"(nodes={component['term_count']}, edges={component['edge_count']})"
        )
    lines.append("")

    lines.extend(["## Two-Hop Cycle Groups", ""])
    for group in summary["two_hop_cycle_groups"]:
        lines.append(
            f"- Group {group['index']}: {' -> '.join(group['node_terms'])} -> {group['node_terms'][0]} "
            f"(supporting_paths={group['supporting_cycle_count']})"
        )
    lines.append("")

    lines.extend(["## Three-Hop Cycle Groups", ""])
    for group in summary["three_hop_cycle_groups"]:
        lines.append(
            f"- Group {group['index']}: {' -> '.join(group['node_terms'])} -> {group['node_terms'][0]} "
            f"(supporting_paths={group['supporting_cycle_count']})"
        )
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--closure", type=Path, required=True)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--md-output", type=Path, required=True)
    args = parser.parse_args()

    summary = build_summary(load_json(args.graph), load_json(args.closure))
    args.json_output.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    args.md_output.write_text(render_markdown(summary), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
