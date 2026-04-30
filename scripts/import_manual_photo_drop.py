#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PHOTOS_DIR = ROOT / "photos"
DEFAULT_INBOX_DIR = ROOT / "data" / "inbox" / "manual_photo_drop"
DEFAULT_ARCHIVE_DIR = ROOT / "data" / "raw" / "imports" / "manual_photo_drop"

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".heic",
    ".heif",
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
}

SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._-]+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import user-dropped photos into photos/ with exact-hash deduplication.")
    parser.add_argument(
        "--inbox-dir",
        default=str(DEFAULT_INBOX_DIR),
        help="Directory where new photo/video files are dropped.",
    )
    parser.add_argument(
        "--archive-dir",
        default=str(DEFAULT_ARCHIVE_DIR),
        help="Archive root for imported/duplicate source files and run manifest.",
    )
    parser.add_argument(
        "--copy-only",
        action="store_true",
        help="Keep files in inbox (copy mode). Default behavior is move files to archive run folders.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview decisions without copying/moving files.",
    )
    return parser.parse_args()


def now_run_id() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y%m%dT%H%M%S")


def file_sha1(path: Path) -> str:
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean_filename(name: str) -> str:
    cleaned = SAFE_NAME_RE.sub("_", name).strip("._")
    return cleaned or "media_file"


def ensure_unique_target_name(base_name: str, photos_dir: Path) -> str:
    candidate = photos_dir / base_name
    if not candidate.exists():
        return base_name

    stem = candidate.stem
    suffix = candidate.suffix
    index = 2
    while True:
        next_name = f"{stem}_{index}{suffix}"
        if not (photos_dir / next_name).exists():
            return next_name
        index += 1


def indexed_existing_hashes(photos_dir: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    if not photos_dir.exists():
        return hashes

    for path in sorted(photos_dir.iterdir(), key=lambda item: item.name.lower()):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        digest = file_sha1(path)
        hashes[digest] = path.name
    return hashes


def all_inbox_files(inbox_dir: Path) -> list[Path]:
    if not inbox_dir.exists():
        return []
    return sorted(
        [
            path
            for path in inbox_dir.rglob("*")
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
        ],
        key=lambda item: str(item).lower(),
    )


def archive_source_file(
    source_path: Path,
    *,
    inbox_dir: Path,
    run_dir: Path,
    bucket: str,
    copy_only: bool,
) -> str:
    relative = source_path.relative_to(inbox_dir)
    destination = run_dir / bucket / relative
    destination.parent.mkdir(parents=True, exist_ok=True)

    if copy_only:
        shutil.copy2(source_path, destination)
    else:
        source_path.rename(destination)

    return str(destination.relative_to(ROOT))


def write_manifest(manifest_path: Path, rows: list[dict[str, str]]) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "source_file",
        "source_relative",
        "file_size_bytes",
        "sha1",
        "target_file",
        "target_relative",
        "status",
        "notes",
        "archived_source_relative",
    ]
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def remove_empty_dirs(root_dir: Path) -> None:
    if not root_dir.exists():
        return
    for path in sorted([p for p in root_dir.rglob("*") if p.is_dir()], key=lambda p: len(p.parts), reverse=True):
        try:
            path.rmdir()
        except OSError:
            continue


def main() -> None:
    args = parse_args()
    inbox_dir = Path(args.inbox_dir).expanduser().resolve()
    archive_dir = Path(args.archive_dir).expanduser().resolve()
    run_id = now_run_id()
    run_dir = archive_dir / run_id

    PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
    inbox_dir.mkdir(parents=True, exist_ok=True)

    candidates = all_inbox_files(inbox_dir)
    if not candidates:
        print(f"No supported files found in inbox: {inbox_dir}")
        print(f"Drop files here and rerun: {inbox_dir}")
        return

    existing_hashes = indexed_existing_hashes(PHOTOS_DIR)
    batch_hashes: dict[str, str] = {}

    manifest_rows: list[dict[str, str]] = []
    imported = 0
    duplicate_existing = 0
    duplicate_batch = 0
    errors = 0

    for source_path in candidates:
        source_relative = str(source_path.relative_to(inbox_dir))
        target_name = ""
        target_relative = ""
        archived_source_relative = ""
        notes = ""
        status = ""
        digest = ""

        try:
            digest = file_sha1(source_path)
            file_size = source_path.stat().st_size
            existing_target = existing_hashes.get(digest, "")
            batch_target = batch_hashes.get(digest, "")

            if existing_target:
                status = "duplicate_existing_exact_hash"
                notes = f"Matches existing photos/{existing_target}"
                target_name = existing_target
                target_relative = f"photos/{existing_target}"
                duplicate_existing += 1
                if not args.dry_run:
                    archived_source_relative = archive_source_file(
                        source_path,
                        inbox_dir=inbox_dir,
                        run_dir=run_dir,
                        bucket="duplicates_existing",
                        copy_only=args.copy_only,
                    )
            elif batch_target:
                status = "duplicate_within_batch_exact_hash"
                notes = f"Matches imported file {batch_target}"
                target_name = batch_target
                target_relative = f"photos/{batch_target}"
                duplicate_batch += 1
                if not args.dry_run:
                    archived_source_relative = archive_source_file(
                        source_path,
                        inbox_dir=inbox_dir,
                        run_dir=run_dir,
                        bucket="duplicates_batch",
                        copy_only=args.copy_only,
                    )
            else:
                base_name = clean_filename(source_path.name)
                if "." not in base_name:
                    base_name = f"{base_name}{source_path.suffix.lower()}"
                if not Path(base_name).suffix:
                    base_name = f"{base_name}{source_path.suffix.lower()}"

                target_name = ensure_unique_target_name(base_name, PHOTOS_DIR)
                target_path = PHOTOS_DIR / target_name

                if not args.dry_run:
                    shutil.copy2(source_path, target_path)
                    archived_source_relative = archive_source_file(
                        source_path,
                        inbox_dir=inbox_dir,
                        run_dir=run_dir,
                        bucket="imported_sources",
                        copy_only=args.copy_only,
                    )

                status = "imported"
                target_relative = f"photos/{target_name}"
                batch_hashes[digest] = target_name
                existing_hashes[digest] = target_name
                imported += 1

            manifest_rows.append(
                {
                    "source_file": source_path.name,
                    "source_relative": source_relative,
                    "file_size_bytes": str(file_size),
                    "sha1": digest,
                    "target_file": target_name,
                    "target_relative": target_relative,
                    "status": status,
                    "notes": notes,
                    "archived_source_relative": archived_source_relative,
                }
            )
        except Exception as exc:  # noqa: BLE001
            errors += 1
            manifest_rows.append(
                {
                    "source_file": source_path.name,
                    "source_relative": source_relative,
                    "file_size_bytes": "",
                    "sha1": digest,
                    "target_file": target_name,
                    "target_relative": target_relative,
                    "status": "error",
                    "notes": str(exc),
                    "archived_source_relative": archived_source_relative,
                }
            )

    summary = {
        "run_id": run_id,
        "inbox_dir": str(inbox_dir),
        "archive_dir": str(archive_dir),
        "dry_run": bool(args.dry_run),
        "copy_only": bool(args.copy_only),
        "processed_files": len(candidates),
        "imported": imported,
        "duplicate_existing_exact_hash": duplicate_existing,
        "duplicate_within_batch_exact_hash": duplicate_batch,
        "errors": errors,
    }

    if not args.dry_run:
        run_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = run_dir / "manifest.csv"
        write_manifest(manifest_path, manifest_rows)
        (run_dir / "run_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        remove_empty_dirs(inbox_dir)
        print(f"Run manifest: {manifest_path.relative_to(ROOT)}")
        print(f"Run summary: {(run_dir / 'run_summary.json').relative_to(ROOT)}")
    else:
        print("Dry-run mode: no files copied/moved.")

    print("Import summary:")
    for key, value in summary.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
