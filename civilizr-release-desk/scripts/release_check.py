#!/usr/bin/env python3
"""Civilizr Release Desk — local /release-check logic.

Reads data/release.json, prints a threaded-style checklist + proposed IG
caption + READY/BLOCKED. Simulates a human ✅ with --approve (CLI only;
in Switch the human reacts or replies in the room).

Usage:
  python3 scripts/release_check.py
  python3 scripts/release_check.py --release data/release.json
  python3 scripts/release_check.py --approve --by alyx --note "ship it"
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RELEASE = ROOT / "data" / "release.json"
DEFAULT_LOG = ROOT / "data" / "approval-log.jsonl"

REQUIRED_ASSETS = (
    "audio_master",
    "cover_art",
    "lyrics",
    "distrokid_metadata",
)


def load_release(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def checklist(release: dict) -> tuple[list[str], list[str], str]:
    lines: list[str] = []
    blockers: list[str] = []
    assets = release.get("assets") or {}

    for key in REQUIRED_ASSETS:
        item = assets.get(key) or {}
        present = bool(item.get("present"))
        path = item.get("path", "?")
        mark = "✅" if present else "❌"
        lines.append(f"{mark} {key}: {path}")
        if not present:
            blockers.append(key)

    # optional but flagged
    for key, item in assets.items():
        if key in REQUIRED_ASSETS:
            continue
        present = bool(item.get("present"))
        path = item.get("path", "?")
        mark = "✅" if present else "⚠️"
        lines.append(f"{mark} {key} (optional): {path}")

    meta = release.get("metadata") or {}
    if not meta.get("isrc"):
        lines.append("⚠️ metadata.isrc: missing (optional for demo)")
    if not meta.get("upc"):
        lines.append("⚠️ metadata.upc: missing (optional for demo)")

    status = "BLOCKED" if blockers else "READY"
    return lines, blockers, status


def proposed_caption(release: dict) -> str:
    title = release.get("title", "Untitled")
    handle = release.get("handle", "@civilizresoterica")
    seeds = release.get("caption_seeds") or []
    seed = seeds[0] if seeds else "new release"
    return (
        f"{title} — {seed}.\n"
        f"Human-gated release desk: agents prep, I decide.\n"
        f"{handle}"
    )


def format_report(release: dict, lines: list[str], blockers: list[str], status: str) -> str:
    rid = release.get("release_id", "?")
    title = release.get("title", "?")
    target = release.get("target_date", "?")
    out = [
        f"**Release check — {title}** (`{rid}`)",
        f"Target: {target}",
        "",
        "Checklist:",
        *[f"  {line}" for line in lines],
        "",
        f"**Status: {status}**",
    ]
    if blockers:
        out.append("Blockers: " + ", ".join(blockers))
        out.append("Fix the ❌ items in release.json, then re-run /release-check.")
    else:
        out.append("All required assets present. React ✅ (or run with --approve) to write APPROVED.")
    out.extend(["", "Proposed IG caption:", "---", proposed_caption(release), "---"])
    return "\n".join(out)


def append_approval(log_path: Path, release: dict, by: str, note: str) -> str:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": "APPROVED",
        "release_id": release.get("release_id"),
        "title": release.get("title"),
        "by": by,
        "note": note,
        "simulates": "human ✅ reaction in Switch room",
    }
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return json.dumps(entry, indent=2)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Civilizr /release-check")
    p.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    p.add_argument("--log", type=Path, default=DEFAULT_LOG)
    p.add_argument(
        "--approve",
        action="store_true",
        help="Simulate human ✅: append APPROVED to approval-log.jsonl (only if READY)",
    )
    p.add_argument("--by", default="alyx", help="Who approved (for the log)")
    p.add_argument("--note", default="", help="Optional approval note")
    p.add_argument("--json", action="store_true", help="Machine-readable output")
    args = p.parse_args(argv)

    if not args.release.is_file():
        print(f"release file not found: {args.release}", file=sys.stderr)
        return 2

    release = load_release(args.release)
    lines, blockers, status = checklist(release)

    if args.json:
        payload = {
            "release_id": release.get("release_id"),
            "status": status,
            "blockers": blockers,
            "checklist": lines,
            "caption": proposed_caption(release),
        }
        print(json.dumps(payload, indent=2))
    else:
        print(format_report(release, lines, blockers, status))

    if args.approve:
        if status != "READY":
            print(
                f"\nRefusing --approve: status is {status}. Clear blockers first.",
                file=sys.stderr,
            )
            return 1
        entry = append_approval(args.log, release, args.by, args.note)
        print(f"\nWrote APPROVED to {args.log}:\n{entry}")

    return 0 if status == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
