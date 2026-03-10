#!/usr/bin/env python3
"""Build a generated 24h last-write view over direct children of a source root."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


WINDOW_SECONDS = 24 * 60 * 60


@dataclass(frozen=True)
class EntrySnapshot:
    name: str
    source_path: Path
    kind: str
    last_write_epoch: int
    last_write_at: str
    window_start_epoch: int
    window_start_at: str
    window_end_at: str

    @property
    def window_dir_name(self) -> str:
        start = self.window_start_at.replace(":", "-")
        end = self.window_end_at.replace(":", "-")
        return f"{start}__{end}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default="/home/_404/src/discussions/skills/homeostasis",
        help="Source root to bucket by last-write window.",
    )
    parser.add_argument(
        "--out",
        default="",
        help="Generated view root. Defaults to <root>/_last_write_24h.",
    )
    return parser.parse_args()


def iso_utc(epoch: int) -> str:
    return datetime.fromtimestamp(epoch, tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def recursive_last_write_epoch(path: Path) -> int:
    latest = int(path.stat().st_mtime)
    if path.is_dir():
        for child in path.rglob("*"):
            try:
                child_epoch = int(child.stat().st_mtime)
            except OSError:
                continue
            if child_epoch > latest:
                latest = child_epoch
    return latest


def entry_snapshot(path: Path) -> EntrySnapshot:
    latest = recursive_last_write_epoch(path)
    window_start = latest - (latest % WINDOW_SECONDS)
    window_end = window_start + WINDOW_SECONDS
    kind = "directory" if path.is_dir() else "file"
    return EntrySnapshot(
        name=path.name,
        source_path=path.resolve(),
        kind=kind,
        last_write_epoch=latest,
        last_write_at=iso_utc(latest),
        window_start_epoch=window_start,
        window_start_at=iso_utc(window_start),
        window_end_at=iso_utc(window_end),
    )


def collect_entries(root: Path, out_root: Path) -> list[EntrySnapshot]:
    entries: list[EntrySnapshot] = []
    for child in sorted(root.iterdir()):
        if child.name.startswith("."):
            continue
        if child.resolve() == out_root.resolve():
            continue
        entries.append(entry_snapshot(child))
    return entries


def relative_link_target(source: Path, link_parent: Path) -> Path:
    return Path(os.path.relpath(source, start=link_parent))


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_readme(path: Path, root: Path, entry_count: int, window_count: int) -> None:
    label = root.name or str(root)
    command_path = Path(__file__).resolve()
    lines = [
        f"# {label}/_last_write_24h",
        "",
        "Generated view over direct children of the source root grouped by recursive last-write time in fixed 24-hour UTC windows.",
        "",
        f"- source root: `{root}`",
        f"- entry count: `{entry_count}`",
        f"- window count: `{window_count}`",
        "- entry definition: direct child of source root",
        "- grouping rule: recursive latest mtime of each entry",
        "- window size: `24h`",
        "- window alignment: `UTC midnight buckets`",
        "- link mode: `relative symlink`",
        "",
        "Do not edit this tree by hand. Regenerate it with:",
        "",
        "```bash",
        f"python3 {command_path}",
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def build_view(root: Path, out_root: Path) -> None:
    entries = collect_entries(root, out_root)

    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    windows: dict[str, list[EntrySnapshot]] = {}
    for entry in entries:
        windows.setdefault(entry.window_dir_name, []).append(entry)

    manifest_windows: list[dict[str, object]] = []
    for window_dir_name in sorted(windows):
        bucket_dir = out_root / window_dir_name
        bucket_dir.mkdir(parents=True, exist_ok=True)
        bucket_entries = sorted(windows[window_dir_name], key=lambda item: item.name)
        bucket_payload_entries: list[dict[str, object]] = []
        for entry in bucket_entries:
            link_path = bucket_dir / entry.name
            link_target = relative_link_target(entry.source_path, bucket_dir)
            link_path.symlink_to(link_target)
            bucket_payload_entries.append(
                {
                    "name": entry.name,
                    "kind": entry.kind,
                    "source_path": str(entry.source_path),
                    "last_write_at": entry.last_write_at,
                }
            )
        first = bucket_entries[0]
        window_payload = {
            "kind": "discussions.last_write_window.v1",
            "window_start_at": first.window_start_at,
            "window_end_at": first.window_end_at,
            "window_seconds": WINDOW_SECONDS,
            "entries": bucket_payload_entries,
        }
        write_json(bucket_dir / "window.v1.json", window_payload)
        manifest_windows.append(
            {
                "window_dir": window_dir_name,
                "window_start_at": first.window_start_at,
                "window_end_at": first.window_end_at,
                "entry_count": len(bucket_entries),
                "entries": [entry.name for entry in bucket_entries],
            }
        )

    manifest = {
        "kind": "discussions.last_write_index.v1",
        "generated_at": datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_root": str(root.resolve()),
        "output_root": str(out_root.resolve()),
        "window_seconds": WINDOW_SECONDS,
        "entry_definition": "direct child of source root",
        "entry_count": len(entries),
        "window_count": len(manifest_windows),
        "windows": manifest_windows,
    }
    write_json(out_root / "manifest.v1.json", manifest)
    write_readme(out_root / "README.md", root.resolve(), len(entries), len(manifest_windows))


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    out_root = Path(args.out).expanduser().resolve() if args.out else root / "_last_write_24h"
    build_view(root, out_root)
    print(out_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
