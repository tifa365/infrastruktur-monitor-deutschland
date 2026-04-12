#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = "data/schwimmbaeder.js"
HISTORY_PATH = "status_history.md"
DATA_PREFIX = "window.SCHWIMMBAEDER_DATEN = "
RELEVANT_FIELDS = ("status", "begruendung", "zeitraum")


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        text=True,
        capture_output=True,
    )


def staged_paths() -> set[str]:
    result = git("diff", "--cached", "--name-only")
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def read_git_file(ref: str, path: str) -> str | None:
    result = git("show", f"{ref}:{path}", check=False)
    if result.returncode != 0:
      return None
    return result.stdout


def parse_js_entries(payload: str) -> dict[int, dict]:
    if not payload.startswith(DATA_PREFIX):
        raise ValueError(f"Unexpected data payload in {DATA_PATH}")
    text = payload[len(DATA_PREFIX):].strip()
    if text.endswith(";"):
        text = text[:-1]
    entries = json.loads(text)
    return {entry["id"]: entry for entry in entries}


def relevant_changes(old: dict[int, dict], new: dict[int, dict]) -> list[str]:
    changed_names = []
    for entry_id, new_entry in new.items():
        old_entry = old.get(entry_id)
        if not old_entry:
            continue
        if any(old_entry.get(field) != new_entry.get(field) for field in RELEVANT_FIELDS):
            changed_names.append(new_entry["name"])
            continue
        old_source = old_entry.get("quelle", {})
        new_source = new_entry.get("quelle", {})
        if (
            old_source.get("titel") != new_source.get("titel")
            or old_source.get("url") != new_source.get("url")
        ):
            changed_names.append(new_entry["name"])
    return changed_names


def main() -> int:
    staged = staged_paths()
    if DATA_PATH not in staged:
        print("History check skipped: staged data file unchanged.")
        return 0

    head_payload = read_git_file("HEAD", DATA_PATH)
    if head_payload is None:
        print("History check skipped: no HEAD version of data file yet.")
        return 0

    staged_payload = read_git_file("", DATA_PATH)
    if staged_payload is None:
        print("History check failed: staged data file could not be read.", file=sys.stderr)
        return 1

    old_entries = parse_js_entries(head_payload)
    new_entries = parse_js_entries(staged_payload)
    changed_names = relevant_changes(old_entries, new_entries)

    if not changed_names:
        print("History check passed: no tracked status changes.")
        return 0

    if HISTORY_PATH not in staged:
        print("History check failed:", file=sys.stderr)
        print(
            f"- Relevant status changes detected for {', '.join(changed_names)}, but {HISTORY_PATH} is not staged.",
            file=sys.stderr,
        )
        print(f'Update {HISTORY_PATH} and stage it before committing.', file=sys.stderr)
        return 1

    history_text = read_git_file("", HISTORY_PATH)
    if history_text is None:
        print("History check failed: staged history file could not be read.", file=sys.stderr)
        return 1

    missing = [name for name in changed_names if name not in history_text]
    if missing:
        print("History check failed:", file=sys.stderr)
        for name in missing:
            print(f"- {name}: no matching entry found in staged {HISTORY_PATH}", file=sys.stderr)
        return 1

    print(f"History check OK for {len(changed_names)} entr{'y' if len(changed_names) == 1 else 'ies'}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
