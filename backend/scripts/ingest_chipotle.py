"""Ingest a Chipotle JSON export into the configured database.

Usage:
    python scripts/ingest_chipotle.py --input chipotle.json --source-url URL
"""

import argparse
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from db.session import SessionLocal  # noqa: E402
from ingestion.chipotle import ingest_chipotle, parse_chipotle_payload  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest a Chipotle JSON menu snapshot")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path, help="Path to the source JSON export")
    source.add_argument("--url", help="Public JSON URL to fetch")
    parser.add_argument("--source-url", help="Public URL where the data was verified; defaults to --url")
    args = parser.parse_args()

    source_url = args.source_url or args.url
    if args.input:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    else:
        request = Request(args.url, headers={"User-Agent": "BiteWise ingestion/1.0"})
        with urlopen(request, timeout=30) as response:
            payload = json.load(response)

    snapshot = parse_chipotle_payload(payload, source_url)
    with SessionLocal() as db:
        restaurant, item_count = ingest_chipotle(db, snapshot)
    print(f"Ingested {restaurant.name}: {item_count} menu items, {len(snapshot.locations)} locations")


if __name__ == "__main__":
    main()