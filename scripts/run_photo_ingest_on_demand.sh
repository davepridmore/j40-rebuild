#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

J40_PHOTO_INGEST_ON_DEMAND=1 /bin/bash "$ROOT_DIR/scripts/stage_takeout_from_downloads.sh"
J40_PHOTO_INGEST_ON_DEMAND=1 DOWNLOADS_DIR="$ROOT_DIR/data/inbox/takeout" /bin/bash "$ROOT_DIR/scripts/scan_takeout_ingest_once.sh"
python3 "$ROOT_DIR/scripts/filter_non_car_media.py" --apply
python3 "$ROOT_DIR/scripts/build_photo_inventory.py"
python3 "$ROOT_DIR/scripts/reconcile_component_jobs_photo_inventory.py"

echo "On-demand ingest scan completed."
echo "Status: $ROOT_DIR/docs/photo_ingest_automation_status.md"
