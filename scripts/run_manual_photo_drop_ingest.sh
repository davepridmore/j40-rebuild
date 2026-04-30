#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INBOX_DIR="${INBOX_DIR:-$ROOT_DIR/data/inbox/manual_photo_drop}"
ARCHIVE_DIR="${ARCHIVE_DIR:-$ROOT_DIR/data/raw/imports/manual_photo_drop}"
COPY_ONLY="${COPY_ONLY:-0}"

mkdir -p "$INBOX_DIR" "$ARCHIVE_DIR"

import_args=(
  "$ROOT_DIR/scripts/import_manual_photo_drop.py"
  --inbox-dir "$INBOX_DIR"
  --archive-dir "$ARCHIVE_DIR"
)

if [ "$COPY_ONLY" = "1" ]; then
  import_args+=(--copy-only)
fi

python3 "${import_args[@]}"
python3 "$ROOT_DIR/scripts/build_photo_inventory.py"
python3 "$ROOT_DIR/scripts/filter_non_car_media.py" --apply
python3 "$ROOT_DIR/scripts/build_photo_inventory.py"
python3 "$ROOT_DIR/scripts/reconcile_component_jobs_photo_inventory.py"
python3 "$ROOT_DIR/scripts/build_project_control_ui.py"

echo "Manual photo drop ingest complete."
echo "Drop folder: $INBOX_DIR"
echo "Inventory: $ROOT_DIR/data/manual/photo_inventory.csv"
echo "Catalog: $ROOT_DIR/docs/photo-catalog.md"
echo "Dashboard data: $ROOT_DIR/docs/project-control-ui/data.js"
