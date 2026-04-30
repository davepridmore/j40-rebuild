#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE="${1:-pridmoredave-gphotos:}"
MAX_AGE="${MAX_AGE:-540d}"
DEST_DIR="${DEST_DIR:-$ROOT_DIR/photos}"
RUNS_DIR="$ROOT_DIR/data/raw/imports/google_photos/runs"

mkdir -p "$DEST_DIR" "$RUNS_DIR"

RUN_ID="$(date +%Y%m%dT%H%M%S)"
LOG_FILE="$RUNS_DIR/${RUN_ID}_sync.log"

{
  echo "[$(date +%F' '%T)] Starting Google Photos pull"
  echo "Remote: $REMOTE"
  echo "Destination: $DEST_DIR"
  echo "Max age: $MAX_AGE"
  echo "Note: Google Photos API may expose only media created by this OAuth client."
  echo "      For full-library import, use Google Takeout or the Picker on-demand script."

  rclone copy \
    "${REMOTE}media/all" \
    "$DEST_DIR" \
    --max-age "$MAX_AGE" \
    --ignore-existing \
    --transfers 8 \
    --checkers 16 \
    --fast-list

  echo "[$(date +%F' '%T)] Rebuilding catalog and analytics"
  python3 "$ROOT_DIR/scripts/build_photo_inventory.py"
  python3 "$ROOT_DIR/scripts/reconcile_component_jobs_photo_inventory.py"

  echo "[$(date +%F' '%T)] Completed"
} | tee "$LOG_FILE"

echo "Run log: $LOG_FILE"
