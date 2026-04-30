#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CRON_SCRIPT="$ROOT_DIR/scripts/scan_takeout_ingest_once.sh"
STAGE_SCRIPT="$ROOT_DIR/scripts/stage_takeout_from_downloads.sh"
CRON_LOG_DIR="$ROOT_DIR/data/raw/imports/google_photos/cron"
CRON_STDOUT="$CRON_LOG_DIR/stdout.log"
CRON_STDERR="$CRON_LOG_DIR/stderr.log"
CRON_MARKER="# J40_PHOTO_INGEST_CRON"
CRON_LINE="*/5 * * * * J40_PHOTO_INGEST_ENABLE=1 /bin/bash \"$STAGE_SCRIPT\" >>\"$CRON_STDOUT\" 2>>\"$CRON_STDERR\"; J40_PHOTO_INGEST_ENABLE=1 DOWNLOADS_DIR=\"$ROOT_DIR/data/inbox/takeout\" /bin/bash \"$CRON_SCRIPT\" >>\"$CRON_STDOUT\" 2>>\"$CRON_STDERR\" $CRON_MARKER"

mkdir -p "$CRON_LOG_DIR" "$ROOT_DIR/data/inbox/takeout"

existing_cron="$(crontab -l 2>/dev/null || true)"
cleaned_cron="$(printf '%s\n' "$existing_cron" | sed "/$CRON_MARKER/d")"

{
  printf '%s\n' "$cleaned_cron"
  printf '%s\n' "$CRON_LINE"
} | awk 'NF' | crontab -

echo "Installed cron job for photo ingest."
echo "Runs every 5 minutes."
echo "Ingest folder: $ROOT_DIR/data/inbox/takeout"
echo "Logs:"
echo "  $CRON_STDOUT"
echo "  $CRON_STDERR"
