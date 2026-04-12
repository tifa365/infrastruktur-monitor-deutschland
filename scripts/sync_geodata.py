#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "schwimmbaeder.js"
PREFIX = "window.SCHWIMMBAEDER_DATEN = "
PHOTON_URL = "https://photon.komoot.io/api/"
ZOOM = 17

# Some entries need a more specific search phrase than their stored address.
QUERY_OVERRIDES = {
    13: ["Jahnallee 17, 76437 Rastatt, Deutschland"],
    25: ["Freibad Amecke Sundern Deutschland"],
    35: ["Schwimmbad Drelsdorf, 25853 Drelsdorf, Deutschland"],
}


def load_entries() -> list[dict]:
    text = DATA_FILE.read_text()
    if not text.startswith(PREFIX):
        raise ValueError(f"Unexpected data format in {DATA_FILE}")
    payload = text[len(PREFIX):].strip()
    if payload.endswith(";"):
        payload = payload[:-1]
    return json.loads(payload)


def save_entries(entries: list[dict]) -> None:
    payload = json.dumps(entries, ensure_ascii=False, indent=2)
    DATA_FILE.write_text(f"{PREFIX}{payload};\n")


def build_osm_url(lat: float, lon: float) -> str:
    return (
        f"https://www.openstreetmap.org/?mlat={lat:.6f}&mlon={lon:.6f}"
        f"#map={ZOOM}/{lat:.6f}/{lon:.6f}"
    )


def build_queries(entry: dict) -> list[str]:
    queries = QUERY_OVERRIDES.get(entry["id"], []).copy()
    queries.extend([
        f'{entry["name"]}, {entry["adresse"]}, {entry["bundesland"]}, Deutschland',
        f'{entry["adresse"]}, {entry["bundesland"]}, Deutschland',
        f'{entry["name"]}, {entry["region"]}, {entry["bundesland"]}, Deutschland',
    ])

    deduped = []
    seen = set()
    for query in queries:
        if query not in seen:
            deduped.append(query)
            seen.add(query)
    return deduped


def geocode_query(query: str) -> dict | None:
    url = PHOTON_URL + "?" + urllib.parse.urlencode({"q": query, "limit": 1})
    with urllib.request.urlopen(url, timeout=20) as response:
        data = json.load(response)
    features = data.get("features") or []
    return features[0] if features else None


def sync_entries(entries: list[dict], refresh: bool = False) -> int:
    updated = 0
    for entry in entries:
        current_karte = entry.get("karte", "")
        needs_sync = refresh or not all(key in entry for key in ("lat", "lon")) or not str(current_karte).startswith(
            "https://www.openstreetmap.org/?mlat="
        )
        if not needs_sync:
            continue

        feature = None
        query_used = None
        for query in build_queries(entry):
            feature = geocode_query(query)
            if feature:
                query_used = query
                break
            time.sleep(0.2)

        if not feature:
            raise RuntimeError(f'No Photon geocode result for "{entry["name"]}"')

        lon, lat = feature["geometry"]["coordinates"]
        lat = round(float(lat), 6)
        lon = round(float(lon), 6)
        entry["lat"] = lat
        entry["lon"] = lon
        entry["karte"] = build_osm_url(lat, lon)
        updated += 1
        print(f'Synced {entry["name"]} via "{query_used}"')
        time.sleep(0.2)
    return updated


def validate_entries(entries: list[dict]) -> list[str]:
    errors = []
    for entry in entries:
        name = entry.get("name", "<unknown>")
        missing = [field for field in ("lat", "lon", "karte") if field not in entry]
        if missing:
            errors.append(f"{name}: missing {', '.join(missing)}")
            continue

        try:
            lat = float(entry["lat"])
            lon = float(entry["lon"])
        except (TypeError, ValueError):
            errors.append(f"{name}: lat/lon must be numeric")
            continue

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            errors.append(f"{name}: invalid coordinate bounds {lat}, {lon}")

        expected = build_osm_url(lat, lon)
        if entry["karte"] != expected:
            errors.append(f"{name}: karte must equal {expected}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync and validate OSM geodata for pool entries.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync", help="Geocode entries and write lat/lon + OSM links.")
    sync_parser.add_argument("--refresh", action="store_true", help="Re-geocode every entry, not just missing ones.")

    subparsers.add_parser("check", help="Fail if any entry is missing geodata or uses a non-OSM link.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    entries = load_entries()

    if args.command == "sync":
        updated = sync_entries(entries, refresh=args.refresh)
        save_entries(entries)
        print(f"Updated {updated} entr{'y' if updated == 1 else 'ies'}.")
        return 0

    errors = validate_entries(entries)
    if errors:
        print("Geodata check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        print('Run "uv run scripts/sync_geodata.py sync" to repair missing OSM links.', file=sys.stderr)
        return 1

    print(f"Geodata OK for {len(entries)} entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
