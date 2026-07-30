#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PHOTOS_DIR = ROOT / "photos"
DEFAULT_LIBRARY = Path.home() / "Pictures" / "Photos Library.photoslibrary"
DEFAULT_OUTPUT = ROOT / "data" / "manual" / "apple_photo_metadata.csv"
APPLE_EPOCH = datetime(2001, 1, 1, tzinfo=timezone.utc)
TIMESTAMP_RE = re.compile(r"^(?P<date>\d{8})_(?P<time>\d{6})")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Match project media to Apple Photos and export capture/GPS metadata without modifying the Photos library."
    )
    parser.add_argument("--library", type=Path, default=DEFAULT_LIBRARY)
    parser.add_argument("--photos-dir", type=Path, default=PHOTOS_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def apple_datetime(value: float | None, offset_seconds: int | None) -> datetime | None:
    if value is None:
        return None
    captured_utc = APPLE_EPOCH + timedelta(seconds=float(value))
    offset = int(offset_seconds or 0)
    return captured_utc.astimezone(timezone(timedelta(seconds=offset)))


def valid_coordinate(value: float | None) -> bool:
    return value is not None and -180.0 < float(value) < 180.0


def normalized_name(value: str | None) -> str:
    return Path(value or "").name.casefold()


def project_timestamp(file_name: str) -> str:
    match = TIMESTAMP_RE.match(file_name)
    if not match:
        return ""
    return f"{match.group('date')}_{match.group('time')}"


def read_assets(database: Path) -> list[dict[str, str]]:
    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            """
            SELECT
                a.ZUUID AS uuid,
                a.ZFILENAME AS filename,
                x.ZORIGINALFILENAME AS original_filename,
                a.ZDATECREATED AS date_created,
                x.ZTIMEZONEOFFSET AS timezone_offset,
                x.ZTIMEZONENAME AS timezone_name,
                a.ZLATITUDE AS latitude,
                a.ZLONGITUDE AS longitude
            FROM ZASSET a
            LEFT JOIN ZADDITIONALASSETATTRIBUTES x
              ON x.Z_PK = a.ZADDITIONALATTRIBUTES
            WHERE a.ZDATECREATED IS NOT NULL
              AND COALESCE(a.ZTRASHEDSTATE, 0) = 0
            """
        ).fetchall()
    finally:
        connection.close()

    assets: list[dict[str, str]] = []
    for row in rows:
        captured = apple_datetime(row["date_created"], row["timezone_offset"])
        if captured is None:
            continue
        latitude = row["latitude"]
        longitude = row["longitude"]
        has_location = valid_coordinate(latitude) and valid_coordinate(longitude)
        assets.append(
            {
                "apple_asset_uuid": str(row["uuid"] or ""),
                "apple_filename": str(row["filename"] or ""),
                "apple_original_filename": str(row["original_filename"] or ""),
                "captured_date": captured.strftime("%Y-%m-%d"),
                "captured_time": captured.strftime("%H:%M:%S"),
                "captured_at": captured.isoformat(timespec="seconds"),
                "timezone_name": str(row["timezone_name"] or ""),
                "timezone_offset_seconds": str(int(row["timezone_offset"] or 0)),
                "latitude": str(float(latitude)) if has_location else "",
                "longitude": str(float(longitude)) if has_location else "",
                "timestamp_key": captured.strftime("%Y%m%d_%H%M%S"),
            }
        )
    return assets


def match_assets(photos_dir: Path, assets: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[str]]:
    by_name: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_timestamp: dict[str, list[dict[str, str]]] = defaultdict(list)
    for asset in assets:
        for name in (asset["apple_filename"], asset["apple_original_filename"], asset["apple_asset_uuid"]):
            key = normalized_name(name)
            if key:
                by_name[key].append(asset)
        by_timestamp[asset["timestamp_key"]].append(asset)

    matches: list[dict[str, str]] = []
    ambiguous: list[str] = []
    for path in sorted(p for p in photos_dir.iterdir() if p.is_file()):
        candidates = by_name.get(path.name.casefold(), [])
        method = "exact_filename"
        if not candidates and path.stem.casefold() in by_name:
            candidates = by_name[path.stem.casefold()]
            method = "apple_uuid"
        if not candidates:
            timestamp = project_timestamp(path.name)
            candidates = by_timestamp.get(timestamp, []) if timestamp else []
            method = "unique_local_capture_timestamp"

        unique = {candidate["apple_asset_uuid"]: candidate for candidate in candidates}
        if len(unique) != 1:
            if len(unique) > 1:
                ambiguous.append(path.name)
            continue
        asset = next(iter(unique.values()))
        matches.append(
            {
                "file_name": path.name,
                "relative_path": f"photos/{path.name}",
                "captured_date": asset["captured_date"],
                "captured_time": asset["captured_time"],
                "captured_at": asset["captured_at"],
                "timezone_name": asset["timezone_name"],
                "timezone_offset_seconds": asset["timezone_offset_seconds"],
                "latitude": asset["latitude"],
                "longitude": asset["longitude"],
                "metadata_source": "apple_photos",
                "match_method": method,
                "apple_asset_uuid": asset["apple_asset_uuid"],
                "apple_original_filename": asset["apple_original_filename"],
            }
        )
    return matches, ambiguous


def write_csv(output: Path, rows: list[dict[str, str]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "file_name", "relative_path", "captured_date", "captured_time", "captured_at",
        "timezone_name", "timezone_offset_seconds", "latitude", "longitude",
        "metadata_source", "match_method", "apple_asset_uuid", "apple_original_filename",
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    database = args.library.expanduser().resolve() / "database" / "Photos.sqlite"
    photos_dir = args.photos_dir.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not database.is_file():
        raise SystemExit(f"Apple Photos database not found: {database}")
    if not photos_dir.is_dir():
        raise SystemExit(f"Project photos directory not found: {photos_dir}")

    assets = read_assets(database)
    matches, ambiguous = match_assets(photos_dir, assets)
    write_csv(output, matches)
    print(f"Apple assets read: {len(assets)}")
    print(f"Project files matched: {len(matches)}")
    print(f"Ambiguous matches skipped: {len(ambiguous)}")
    print(f"Wrote: {output}")
    if not matches:
        print("No project files matched. Ensure iCloud Photos has finished syncing originals and metadata to this Mac, then rerun.")


if __name__ == "__main__":
    main()
