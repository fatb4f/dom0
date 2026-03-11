#!/usr/bin/env python3
"""Build normalized/enriched terminology artifacts from dom0 sources."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "was",
    "we",
    "with",
}

SPEC_LEXICON: dict[str, list[str]] = {
    "root_scope": [
        "host",
        "codex",
        "spawn",
        "scope_root",
        "control_root",
        "state_space",
        "fsm",
        "service",
        "asset",
        "artifact",
    ],
    "authority_roles": [
        "authority",
        "subordinate",
        "controller",
        "actuator",
        "observer",
        "writer",
        "consumer",
        "owner",
    ],
    "control_surfaces": [
        "relationship.current",
        "identity.current",
        "identity_delta",
        "applied_control.current",
        "applied_control",
        "policy_surface",
        ".control",
        "bootstrap_manifest",
    ],
    "planes_and_boundaries": [
        "policy",
        "contract",
        "runtime",
        "plane",
        "promotion",
        "rollback",
        "boundary",
        "gate",
        "scope",
    ],
    "assurance_validation": [
        "assurance",
        "validation",
        "validator",
        "fidelity",
        "measure",
        "byproduct",
        "output",
        "trigger",
    ],
}

CONTROL_THEORY_LEXICON: dict[str, list[str]] = {
    "state_and_dynamics": [
        "state",
        "state_space",
        "transition",
        "fsm",
        "unknown",
        "undisclosed",
    ],
    "feedback_and_regulation": [
        "homeostasis",
        "feedback",
        "loop",
        "regulation",
        "reanalysis",
        "re-analysis",
        "trigger",
    ],
    "control_roles": [
        "controller",
        "actuator",
        "observer",
        "subordinate",
        "authority",
    ],
    "signals_and_observability": [
        "observation",
        "observable",
        "signal",
        "measure",
        "output",
        "byproduct",
        "evidence",
        "delta",
    ],
}

SECTION_HINTS: list[tuple[str, list[str]]] = [
    ("problem_set", ["host", "codex", "spawn", "homeostasis", "state_space", "scope_root", "control_root"]),
    ("scope", ["boundary", "scope", "control_root", "scope_root", "runtime", "policy", "contract"]),
    ("deliverables_D4", ["host", "codex", "spawn", "scope_root", "control_root", "state_space", "fsm", "service"]),
    ("deliverables_D5", ["relationship.current", "observation", "observable", "signal", "evidence"]),
    ("deliverables_D6", ["identity.current", "identity_delta", "identity", "unknown", "undisclosed"]),
    ("deliverables_D7", ["applied_control.current", "controller", "actuator", "measure", "byproduct", "fidelity", "promotion"]),
    ("deliverables_D8", ["homeostasis", "feedback", "loop", "reanalysis", "trigger", "workflow", "methodology"]),
    ("approval_gate", ["validation", "validator", "gate", "rollback", "fidelity", "promotion"]),
]

TERM_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_./-]{2,}")
BACKTICK_PATTERN = re.compile(r"`([^`]+)`")


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def token_set(text: str) -> set[str]:
    return {token.lower() for token in re.findall(r"[A-Za-z0-9_.]+", text)}


def contains_term(text_lc: str, term: str) -> bool:
    term_lc = term.lower()
    if any(ch in term_lc for ch in "._/"):
        return term_lc in text_lc
    return re.search(rf"(?<![A-Za-z0-9_]){re.escape(term_lc)}(?![A-Za-z0-9_])", text_lc) is not None


def match_lexicon(text: str, lexicon: dict[str, list[str]]) -> tuple[list[str], list[str]]:
    text_lc = text.lower()
    matched_terms: list[str] = []
    matched_categories: list[str] = []
    for category, terms in lexicon.items():
        category_hit = False
        for term in terms:
            if contains_term(text_lc, term):
                matched_terms.append(term)
                category_hit = True
        if category_hit:
            matched_categories.append(category)
    return sorted(set(matched_terms)), sorted(set(matched_categories))


def iter_json_strings(node: Any) -> list[str]:
    strings: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            strings.append(str(key))
            strings.extend(iter_json_strings(value))
    elif isinstance(node, list):
        for item in node:
            strings.extend(iter_json_strings(item))
    elif isinstance(node, str):
        strings.append(node)
    return strings


def collect_plan_strings(path: Path, root: Path) -> list[dict[str, str]]:
    rel = path.relative_to(root).as_posix()
    results: list[dict[str, str]] = []
    if path.suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        for text in iter_json_strings(payload):
            norm = normalize_text(text)
            if norm and len(norm) <= 120:
                results.append({"path": rel, "kind": "json_string", "text": norm})
        return results

    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = normalize_text(line)
        if not line:
            continue
        if line.startswith("#"):
            heading = normalize_text(line.lstrip("#").strip())
            if heading:
                results.append({"path": rel, "kind": "heading", "text": heading})
        for code in BACKTICK_PATTERN.findall(line):
            code = normalize_text(code)
            if code:
                results.append({"path": rel, "kind": "code_span", "text": code})
        for term in TERM_PATTERN.findall(line):
            if len(term) >= 3 and any(ch.isalpha() for ch in term):
                results.append({"path": rel, "kind": "term_like", "text": term})
    return results


def build_normalized_dedup(glossary: dict[str, Any]) -> dict[str, Any]:
    groups: dict[str, dict[str, Any]] = {}
    for source in glossary["sources"]:
        path = source["path"]
        for raw_index, raw_string in enumerate(source["raw_strings"]):
            norm = normalize_text(raw_string)
            if not norm:
                continue
            bucket = groups.setdefault(
                norm,
                {
                    "normalized_string": norm,
                    "occurrence_count": 0,
                    "source_paths": set(),
                    "raw_variants": set(),
                    "occurrences": [],
                },
            )
            bucket["occurrence_count"] += 1
            bucket["source_paths"].add(path)
            bucket["raw_variants"].add(raw_string)
            bucket["occurrences"].append({"path": path, "raw_string_index": raw_index})

    entries = []
    for key, bucket in groups.items():
        entries.append(
            {
                "normalized_string": key,
                "occurrence_count": bucket["occurrence_count"],
                "source_path_count": len(bucket["source_paths"]),
                "source_paths": sorted(bucket["source_paths"]),
                "raw_variant_count": len(bucket["raw_variants"]),
                "raw_variants": sorted(bucket["raw_variants"]),
                "occurrences": bucket["occurrences"],
            }
        )
    entries.sort(key=lambda e: (-e["source_path_count"], -e["occurrence_count"], e["normalized_string"]))

    return {
        "kind": "glossary.normalized.dedup.v1",
        "source_glossary_ref": "glossary.json",
        "normalization_policy": {
            "unicode_normalization": "NFKC",
            "whitespace": "collapse_internal_and_trim",
            "semantic_non_alteration": [
                "no_case_folding",
                "no_stemming",
                "no_lemmatization",
                "no_punctuation_stripping",
                "no_stopword_removal",
            ],
        },
        "source_count": len(glossary["sources"]),
        "raw_string_total": sum(source["raw_string_count"] for source in glossary["sources"]),
        "normalized_entry_count": len(entries),
        "entries": entries,
    }


def build_enriched_working_copy(normalized: dict[str, Any]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for entry in normalized["entries"]:
        text = entry["normalized_string"]
        spec_terms, spec_categories = match_lexicon(text, SPEC_LEXICON)
        control_terms, control_categories = match_lexicon(text, CONTROL_THEORY_LEXICON)
        enriched = dict(entry)
        enriched.update(
            {
                "matched_spec_terms": spec_terms,
                "matched_spec_categories": spec_categories,
                "matched_control_terms": control_terms,
                "matched_control_categories": control_categories,
                "is_spec_relevant": bool(spec_terms),
                "is_control_relevant": bool(control_terms),
                "match_score": len(spec_terms) + len(control_terms),
            }
        )
        entries.append(enriched)

    relevant_entries = [entry for entry in entries if entry["match_score"] > 0]
    relevant_entries.sort(
        key=lambda e: (-e["match_score"], -e["source_path_count"], -e["occurrence_count"], e["normalized_string"])
    )

    return {
        "kind": "glossary.normalized.dedup.enriched.working.v1",
        "source_normalized_ref": "glossary.normalized.dedup.json",
        "spec_lexicon": SPEC_LEXICON,
        "control_theory_lexicon": CONTROL_THEORY_LEXICON,
        "entry_count": len(entries),
        "relevant_entry_count": len(relevant_entries),
        "entries": entries,
        "relevant_entries": relevant_entries,
    }


def build_plan_key_terms(plan_dir: Path, glossary_terms: set[str]) -> dict[str, Any]:
    plan_files = [
        path
        for path in sorted(plan_dir.rglob("*"))
        if path.is_file() and "evidence" not in path.parts
    ]
    extractions: list[dict[str, str]] = []
    groups: dict[str, dict[str, Any]] = {}
    plan_text_lc_parts: list[str] = []

    for path in plan_files:
        for record in collect_plan_strings(path, plan_dir.parent):
            extractions.append(record)
            plan_text_lc_parts.append(record["text"].lower())
            norm = normalize_text(record["text"])
            if not norm:
                continue
            if record["kind"] == "term_like":
                if norm.lower() in STOPWORDS:
                    continue
                if not any(ch.isalpha() for ch in norm):
                    continue
            bucket = groups.setdefault(
                norm,
                {
                    "term": norm,
                    "sources": set(),
                    "extraction_kinds": set(),
                },
            )
            bucket["sources"].add(record["path"])
            bucket["extraction_kinds"].add(record["kind"])

    plan_text_lc = "\n".join(plan_text_lc_parts)
    for lexicon in (SPEC_LEXICON, CONTROL_THEORY_LEXICON):
        for terms in lexicon.values():
            for term in terms:
                if contains_term(plan_text_lc, term):
                    bucket = groups.setdefault(
                        term,
                        {
                            "term": term,
                            "sources": set(),
                            "extraction_kinds": set(),
                        },
                    )
                    bucket["sources"].add("PLAN/*")
                    bucket["extraction_kinds"].add("lexicon_scan")

    entries = []
    for term, bucket in groups.items():
        spec_terms, spec_categories = match_lexicon(term, SPEC_LEXICON)
        control_terms, control_categories = match_lexicon(term, CONTROL_THEORY_LEXICON)
        is_glossary_term = term in glossary_terms
        if (
            not spec_terms
            and not control_terms
            and not is_glossary_term
            and "code_span" not in bucket["extraction_kinds"]
            and "json_string" not in bucket["extraction_kinds"]
            and "heading" not in bucket["extraction_kinds"]
        ):
            continue
        entries.append(
            {
                "term": term,
                "source_count": len(bucket["sources"]),
                "sources": sorted(bucket["sources"]),
                "extraction_kinds": sorted(bucket["extraction_kinds"]),
                "matched_spec_terms": spec_terms,
                "matched_spec_categories": spec_categories,
                "matched_control_terms": control_terms,
                "matched_control_categories": control_categories,
                "present_in_glossary_dataset": is_glossary_term,
            }
        )

    entries.sort(
        key=lambda e: (
            -(len(e["matched_spec_terms"]) + len(e["matched_control_terms"])),
            -e["source_count"],
            e["term"],
        )
    )
    return {
        "kind": "plan.key_terminology.v1",
        "source_plan_root": plan_dir.as_posix(),
        "excluded_paths": ["PLAN/evidence/**"],
        "file_count": len(plan_files),
        "extracted_record_count": len(extractions),
        "term_count": len(entries),
        "terms": entries,
    }


def build_diff(enriched: dict[str, Any], plan_terms: dict[str, Any]) -> dict[str, Any]:
    glossary_map = {entry["normalized_string"]: entry for entry in enriched["relevant_entries"]}
    plan_map = {entry["term"]: entry for entry in plan_terms["terms"]}
    glossary_terms = set(glossary_map)
    plan_term_set = set(plan_map)
    overlap = sorted(glossary_terms & plan_term_set)
    glossary_only = sorted(glossary_terms - plan_term_set)
    plan_only = sorted(plan_term_set - glossary_terms)

    return {
        "kind": "terminology.diff.v1",
        "left_ref": "glossary.normalized.dedup.enriched.working.json",
        "right_ref": "plan.key_terminology.json",
        "overlap_count": len(overlap),
        "glossary_only_count": len(glossary_only),
        "plan_only_count": len(plan_only),
        "overlap_terms": overlap,
        "glossary_only_terms": glossary_only,
        "plan_only_terms": plan_only,
    }


def source_authority_score(entry: dict[str, Any]) -> int:
    score = 0
    for path in entry["source_paths"]:
        if path.startswith("asset-control-model/"):
            score += 3
        elif path.endswith("system_discovery_homeostasis.md"):
            score += 3
        elif path.endswith("core_ideas.md") or path.endswith("codex-review.md") or path.endswith("process_snapshot_report.md"):
            score += 2
        elif path.endswith(".jsonl") or "session_log_slice" in path:
            score += 0
        else:
            score += 1
    return score


def suggest_sections(entry: dict[str, Any]) -> list[str]:
    text = entry["normalized_string"].lower()
    suggested: list[str] = []
    for section, terms in SECTION_HINTS:
        if any(contains_term(text, term) for term in terms):
            suggested.append(section)
    return suggested or ["problem_set"]


def build_terminology_seeds(enriched: dict[str, Any], plan_terms: dict[str, Any]) -> dict[str, Any]:
    plan_term_set = {entry["term"].lower() for entry in plan_terms["terms"]}
    buckets: dict[tuple[str, str], dict[str, Any]] = {}

    for entry in enriched["relevant_entries"]:
        authority = source_authority_score(entry)
        samples = entry["raw_variants"][:3]
        for family, matched_terms, matched_categories in [
            ("spec_driven", entry["matched_spec_terms"], entry["matched_spec_categories"]),
            ("control_theory", entry["matched_control_terms"], entry["matched_control_categories"]),
        ]:
            for term in matched_terms:
                key = (family, term)
                bucket = buckets.setdefault(
                    key,
                    {
                        "family": family,
                        "term": term,
                        "categories": set(),
                        "source_paths": set(),
                        "supporting_entry_count": 0,
                        "occurrence_total": 0,
                        "authority_score": 0,
                        "supporting_examples": [],
                    },
                )
                bucket["categories"].update(matched_categories)
                bucket["source_paths"].update(entry["source_paths"])
                bucket["supporting_entry_count"] += 1
                bucket["occurrence_total"] += entry["occurrence_count"]
                bucket["authority_score"] = max(bucket["authority_score"], authority)
                for sample in samples:
                    if sample not in bucket["supporting_examples"] and len(bucket["supporting_examples"]) < 5:
                        bucket["supporting_examples"].append(sample)

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for (_family, _term), bucket in buckets.items():
        seed = {
            "term": bucket["term"],
            "family": bucket["family"],
            "categories": sorted(bucket["categories"]),
            "present_in_plan": bucket["term"].lower() in plan_term_set,
            "source_path_count": len(bucket["source_paths"]),
            "source_paths": sorted(bucket["source_paths"]),
            "supporting_entry_count": bucket["supporting_entry_count"],
            "occurrence_total": bucket["occurrence_total"],
            "authority_score": bucket["authority_score"],
            "supporting_examples": bucket["supporting_examples"],
        }
        groups[bucket["family"]].append(seed)

    group_payloads = []
    for family in sorted(groups):
        seeds = groups[family]
        seeds.sort(
            key=lambda item: (
                -item["authority_score"],
                -item["source_path_count"],
                -item["supporting_entry_count"],
                -item["occurrence_total"],
                item["term"],
            )
        )
        group_payloads.append(
            {
                "family": family,
                "seed_count": len(seeds),
                "seeds": seeds,
            }
        )

    return {
        "kind": "terminology.seeds.v1",
        "source_enriched_ref": "glossary.normalized.dedup.enriched.working.json",
        "source_plan_terms_ref": "plan.key_terminology.json",
        "group_count": len(group_payloads),
        "groups": group_payloads,
    }


def build_plan_enrichment_findings(diff: dict[str, Any], seeds: dict[str, Any]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    noisy_terms = {"assistant", "user", "timestamp", "message", "text", "role", "status", "output"}
    for group in seeds["groups"]:
        family = group["family"]
        for seed in group["seeds"]:
            if seed["present_in_plan"]:
                continue
            if seed["term"].lower() in noisy_terms:
                continue
            score = (
                seed["authority_score"] * 4
                + min(seed["source_path_count"], 5) * 3
                + min(seed["supporting_entry_count"], 5) * 2
                + min(seed["occurrence_total"], 10)
            )
            candidates.append(
                {
                    "term": seed["term"],
                    "family": family,
                    "categories": seed["categories"],
                    "priority_score": score,
                    "suggested_plan_sections": suggest_sections({"normalized_string": seed["term"]}),
                    "reason": {
                        "source_path_count": seed["source_path_count"],
                        "supporting_entry_count": seed["supporting_entry_count"],
                        "occurrence_total": seed["occurrence_total"],
                        "authority_score": seed["authority_score"],
                    },
                    "source_paths": seed["source_paths"],
                    "supporting_examples": seed["supporting_examples"],
                }
            )

    candidates.sort(key=lambda item: (-item["priority_score"], item["family"], item["term"]))
    return {
        "kind": "plan.enrichment.findings.v1",
        "source_diff_ref": "terminology.diff.json",
        "source_seed_ref": "terminology.seeds.json",
        "candidate_count": len(candidates),
        "top_candidates": candidates[:40],
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glossary", type=Path, required=True)
    parser.add_argument("--plan-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    glossary = json.loads(args.glossary.read_text(encoding="utf-8"))
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    normalized = build_normalized_dedup(glossary)
    enriched = build_enriched_working_copy(normalized)
    glossary_terms = {entry["normalized_string"] for entry in normalized["entries"]}
    plan_terms = build_plan_key_terms(args.plan_dir, glossary_terms)
    diff = build_diff(enriched, plan_terms)
    seeds = build_terminology_seeds(enriched, plan_terms)
    enrichment = build_plan_enrichment_findings(diff, seeds)

    write_json(output_dir / "glossary.normalized.dedup.json", normalized)
    write_json(output_dir / "glossary.normalized.dedup.enriched.working.json", enriched)
    write_json(output_dir / "plan.key_terminology.json", plan_terms)
    write_json(output_dir / "terminology.diff.json", diff)
    write_json(output_dir / "plan.enrichment.findings.json", enrichment)
    write_json(output_dir / "terminology.seeds.json", seeds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
