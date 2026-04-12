#!/usr/bin/env python3

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META_FILE = ROOT / "data" / "meta.js"
PREFIX = "window.APP_META = "


def main() -> int:
    payload = {
        "lastUpdated": date.today().isoformat(),
    }
    META_FILE.write_text(f"{PREFIX}{json.dumps(payload, ensure_ascii=False, indent=2)};\n")
    print(f"Updated {META_FILE} to {payload['lastUpdated']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
