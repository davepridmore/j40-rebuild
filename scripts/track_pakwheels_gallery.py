#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAKWHEELS_DIR = ROOT / "data" / "pakwheels"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)

GALLERY_URL_RE = re.compile(
    r'data-sub-html="#contact-user-info"[^>]*\sdata-src="(https://cache[0-9]\.pakwheels\.com/ad_pictures/[0-9]+/[^"]+)"'
)


@dataclass
class HistoryRow:
    image_key: str
    first_seen: str
    last_seen: str
    active: str
    image_url: str
    archived_file: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Track PakWheels listing gallery changes over time.",
    )
    parser.add_argument(
        "--url",
        required=True,
        help="PakWheels listing URL.",
    )
    parser.add_argument(
        "--listing-id",
        help="Optional listing id. If omitted, inferred from URL.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="HTTP timeout in seconds. Default: 20.",
    )
    return parser.parse_args()


def infer_listing_id(listing_url: str) -> str:
    parsed = urllib.parse.urlparse(listing_url)
    slug = parsed.path.rstrip("/").split("/")[-1]
    match = re.search(r"-(\d+)$", slug)
    if not match:
        raise ValueError(f"Could not infer listing id from URL path: {parsed.path}")
    return match.group(1)


def fetch_text(url: str, timeout: int) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def extract_gallery_urls(html: str) -> list[str]:
    seen: set[str] = set()
    urls: list[str] = []
    for url in GALLERY_URL_RE.findall(html):
        if url in seen:
            continue
        seen.add(url)
        urls.append(url)
    return urls


def url_exists(url: str, timeout: int) -> bool:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status == 200
    except urllib.error.HTTPError as error:
        if error.code not in {403, 405}:
            return False
    except urllib.error.URLError:
        return False

    # Fallback for servers that block HEAD.
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status == 200
    except (urllib.error.HTTPError, urllib.error.URLError):
        return False


def select_preferred_url(url: str, timeout: int) -> str:
    if url.lower().endswith(".webp"):
        jpg_url = re.sub(r"\.webp$", ".jpg", url, flags=re.IGNORECASE)
        if url_exists(jpg_url, timeout):
            return jpg_url
    return url


def parse_image_key(image_url: str) -> str:
    clean = image_url.split("?", 1)[0]
    return Path(clean).stem


def download_file(url: str, destination: Path, timeout: int) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        destination.write_bytes(response.read())


def read_history(path: Path) -> dict[str, HistoryRow]:
    if not path.exists():
        return {}

    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    history: dict[str, HistoryRow] = {}
    for row in rows:
        image_key = row.get("image_key", "").strip()
        if not image_key:
            continue
        history[image_key] = HistoryRow(
            image_key=image_key,
            first_seen=row.get("first_seen", ""),
            last_seen=row.get("last_seen", ""),
            active=row.get("active", "false"),
            image_url=row.get("image_url", ""),
            archived_file=row.get("archived_file", ""),
        )
    return history


def write_history(path: Path, history: dict[str, HistoryRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["image_key", "first_seen", "last_seen", "active", "image_url", "archived_file"],
        )
        writer.writeheader()
        for image_key in sorted(history):
            row = history[image_key]
            writer.writerow(
                {
                    "image_key": row.image_key,
                    "first_seen": row.first_seen,
                    "last_seen": row.last_seen,
                    "active": row.active,
                    "image_url": row.image_url,
                    "archived_file": row.archived_file,
                }
            )


def append_run_log(
    runs_path: Path,
    run_time: str,
    listing_url: str,
    image_count: int,
    new_count: int,
    removed_count: int,
) -> None:
    runs_path.parent.mkdir(parents=True, exist_ok=True)
    exists = runs_path.exists()
    with runs_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "run_time",
                "listing_url",
                "image_count",
                "new_images",
                "removed_images",
            ],
        )
        if not exists:
            writer.writeheader()
        writer.writerow(
            {
                "run_time": run_time,
                "listing_url": listing_url,
                "image_count": image_count,
                "new_images": new_count,
                "removed_images": removed_count,
            }
        )


def write_lines(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def write_snapshot_manifest(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["image_key", "image_url", "archived_file", "new_in_run"],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    listing_id = args.listing_id or infer_listing_id(args.url)

    run_time = datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()
    run_label = run_time.replace(":", "").replace("+", "_").replace("-", "")

    listing_dir = PAKWHEELS_DIR / listing_id
    archive_dir = listing_dir / "archive"
    snapshots_dir = listing_dir / "snapshots" / run_label
    history_path = listing_dir / "gallery_history.csv"
    runs_path = listing_dir / "gallery_runs.csv"
    latest_urls_path = listing_dir / "latest_urls.txt"
    latest_meta_path = listing_dir / "latest_snapshot.json"
    snapshot_urls_path = snapshots_dir / "urls.txt"
    snapshot_manifest_path = snapshots_dir / "manifest.csv"

    html = fetch_text(args.url, timeout=args.timeout)
    raw_urls = extract_gallery_urls(html)
    if not raw_urls:
        raise RuntimeError("No gallery images found on listing page.")

    preferred_urls = [select_preferred_url(url, timeout=args.timeout) for url in raw_urls]
    image_keys = [parse_image_key(url) for url in preferred_urls]
    current_keys = set(image_keys)

    history = read_history(history_path)
    previous_active_keys = {key for key, row in history.items() if row.active.lower() == "true"}

    new_keys: set[str] = set()
    manifest_rows: list[dict] = []

    for image_url in preferred_urls:
        image_key = parse_image_key(image_url)
        suffix = Path(image_url.split("?", 1)[0]).suffix.lower() or ".bin"
        archive_name = f"{image_key}{suffix}"
        archive_file = archive_dir / archive_name
        if not archive_file.exists():
            download_file(image_url, archive_file, timeout=args.timeout)

        row = history.get(image_key)
        if row is None:
            new_keys.add(image_key)
            history[image_key] = HistoryRow(
                image_key=image_key,
                first_seen=run_time,
                last_seen=run_time,
                active="true",
                image_url=image_url,
                archived_file=str(archive_file.relative_to(listing_dir)),
            )
        else:
            row.last_seen = run_time
            row.active = "true"
            row.image_url = image_url
            row.archived_file = str(archive_file.relative_to(listing_dir))

        manifest_rows.append(
            {
                "image_key": image_key,
                "image_url": image_url,
                "archived_file": str(archive_file.relative_to(listing_dir)),
                "new_in_run": "true" if image_key in new_keys else "false",
            }
        )

    removed_keys: set[str] = set()
    for image_key, row in history.items():
        if image_key not in current_keys and row.active.lower() == "true":
            row.active = "false"
            removed_keys.add(image_key)

    write_lines(latest_urls_path, preferred_urls)
    write_lines(snapshot_urls_path, preferred_urls)
    write_snapshot_manifest(snapshot_manifest_path, manifest_rows)
    write_history(history_path, history)
    append_run_log(
        runs_path=runs_path,
        run_time=run_time,
        listing_url=args.url,
        image_count=len(preferred_urls),
        new_count=len(new_keys),
        removed_count=len(removed_keys),
    )

    latest_meta_path.write_text(
        json.dumps(
            {
                "run_time": run_time,
                "listing_id": listing_id,
                "listing_url": args.url,
                "image_count": len(preferred_urls),
                "new_images": sorted(new_keys),
                "removed_images": sorted(removed_keys),
                "snapshot_dir": str(snapshots_dir.relative_to(listing_dir)),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Listing {listing_id}: tracked {len(preferred_urls)} images")
    print(f"New images: {len(new_keys)} | Removed images: {len(removed_keys)}")
    print(f"History: {history_path}")
    print(f"Latest snapshot: {latest_meta_path}")


if __name__ == "__main__":
    main()
