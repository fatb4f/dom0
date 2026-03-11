#!/usr/bin/env python3
"""Derive lexical fields and first-degree entity relationships for seed terms."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ENTITY_CATEGORY_HINTS = {"root_scope", "authority_roles", "control_surfaces", "control_roles"}
NON_ENTITY_TERMS = {
    "policy",
    "contract",
    "runtime",
    "validation",
    "promotion",
    "boundary",
    "feedback",
    "signal",
    "measure",
    "assurance",
    "unknown",
    "undisclosed",
    "delta",
    "state",
    "loop",
    "trigger",
    "transition",
    "fidelity",
    "scope",
    "plane",
    "gate",
    "evidence",
}
EXPLICIT_ENTITY_TERMS = {
    "host",
    "codex",
    "spawn",
    "service",
    "scope_root",
    "control_root",
    "writer",
    "subordinate",
    "observer",
    "controller",
    "actuator",
    "owner",
    "authority",
    "relationship.current",
    "identity.current",
    "applied_control",
    "applied_control.current",
    "policy_surface",
    "bootstrap_manifest",
    "identity_delta",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_seed_index(seeds: dict[str, Any]) -> tuple[dict[tuple[str, str], dict[str, Any]], dict[str, dict[str, Any]]]:
    by_family_term: dict[tuple[str, str], dict[str, Any]] = {}
    by_term: dict[str, dict[str, Any]] = {}
    for group in seeds["groups"]:
        family = group["family"]
        for seed in group["seeds"]:
            key = (family, seed["term"])
            by_family_term[key] = seed
            agg = by_term.setdefault(
                seed["term"],
                {
                    "term": seed["term"],
                    "families": set(),
                    "categories": set(),
                    "present_in_plan": False,
                    "source_paths": set(),
                    "authority_score": 0,
                },
            )
            agg["families"].add(family)
            agg["categories"].update(seed["categories"])
            agg["present_in_plan"] = agg["present_in_plan"] or seed["present_in_plan"]
            agg["source_paths"].update(seed["source_paths"])
            agg["authority_score"] = max(agg["authority_score"], seed["authority_score"])

    normalized: dict[str, dict[str, Any]] = {}
    for term, meta in by_term.items():
        normalized[term] = {
            "term": term,
            "families": sorted(meta["families"]),
            "categories": sorted(meta["categories"]),
            "present_in_plan": meta["present_in_plan"],
            "source_paths": sorted(meta["source_paths"]),
            "authority_score": meta["authority_score"],
        }
    return by_family_term, normalized


def is_entity_term(term: str, meta: dict[str, Any] | None) -> bool:
    if term in EXPLICIT_ENTITY_TERMS:
        return True
    if term in NON_ENTITY_TERMS:
        return False
    if not meta:
        return False
    return bool(set(meta["categories"]) & ENTITY_CATEGORY_HINTS)


def supporting_entries_for_term(enriched: dict[str, Any], family: str, term: str) -> list[dict[str, Any]]:
    key = "matched_spec_terms" if family == "spec_driven" else "matched_control_terms"
    return [entry for entry in enriched["entries"] if term in entry[key]]


def derive_map(enriched: dict[str, Any], seeds: dict[str, Any], findings: dict[str, Any]) -> dict[str, Any]:
    by_family_term, by_term = build_seed_index(seeds)
    seed_maps: list[dict[str, Any]] = []

    for candidate in findings["top_candidates"]:
        family = candidate["family"]
        term = candidate["term"]
        supporting_entries = supporting_entries_for_term(enriched, family, term)
        lexical_counter: Counter[str] = Counter()
        relation_counter: Counter[str] = Counter()
        lexical_examples: dict[str, list[str]] = defaultdict(list)
        relation_examples: dict[str, list[str]] = defaultdict(list)

        for entry in supporting_entries:
            related_terms = sorted(
                set(entry["matched_spec_terms"] + entry["matched_control_terms"]) - {term}
            )
            for related in related_terms:
                lexical_counter[related] += 1
                if len(lexical_examples[related]) < 3:
                    lexical_examples[related].append(entry["normalized_string"])
                related_meta = by_term.get(related)
                if is_entity_term(related, related_meta):
                    relation_counter[related] += 1
                    if len(relation_examples[related]) < 3:
                        relation_examples[related].append(entry["normalized_string"])

        lexical_field = []
        for related, count in lexical_counter.most_common(20):
            meta = by_term.get(related, {"families": [], "categories": [], "present_in_plan": False, "authority_score": 0})
            lexical_field.append(
                {
                    "term": related,
                    "cooccurrence_count": count,
                    "families": meta["families"],
                    "categories": meta["categories"],
                    "present_in_plan": meta["present_in_plan"],
                    "authority_score": meta["authority_score"],
                    "examples": lexical_examples[related],
                }
            )

        first_degree = []
        for related, count in relation_counter.most_common(20):
            meta = by_term.get(related, {"families": [], "categories": [], "present_in_plan": False, "authority_score": 0})
            first_degree.append(
                {
                    "entity_term": related,
                    "relationship_type": "first_degree_cooccurrence",
                    "evidence_count": count,
                    "families": meta["families"],
                    "categories": meta["categories"],
                    "present_in_plan": meta["present_in_plan"],
                    "authority_score": meta["authority_score"],
                    "examples": relation_examples[related],
                }
            )

        seed_maps.append(
            {
                "seed_term": term,
                "family": family,
                "categories": candidate["categories"],
                "present_in_plan": False,
                "supporting_entry_count": len(supporting_entries),
                "source_path_count": candidate["reason"]["source_path_count"],
                "source_paths": candidate["source_paths"],
                "lexical_field": lexical_field,
                "first_degree_entity_relationships": first_degree,
            }
        )

    return {
        "kind": "seed.lexical_field.relationship_map.v1",
        "source_refs": {
            "enriched_glossary": "glossary.normalized.dedup.enriched.working.json",
            "seed_terms": "terminology.seeds.json",
            "plan_enrichment": "plan.enrichment.findings.json",
        },
        "seed_count": len(seed_maps),
        "seeds": seed_maps,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--enriched", type=Path, required=True)
    parser.add_argument("--seeds", type=Path, required=True)
    parser.add_argument("--findings", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    payload = derive_map(load_json(args.enriched), load_json(args.seeds), load_json(args.findings))
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
