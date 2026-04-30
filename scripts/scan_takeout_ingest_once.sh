#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOWNLOADS_DIR="${DOWNLOADS_DIR:-$ROOT_DIR/data/inbox/takeout}"
STATE_DIR="${STATE_DIR:-$ROOT_DIR/data/raw/imports/google_photos/watcher}"
LOG_DIR="${LOG_DIR:-$ROOT_DIR/data/raw/imports/google_photos/runs}"
PROCESSED_FILE="$STATE_DIR/processed_archives.tsv"
STATUS_FILE="$ROOT_DIR/docs/photo_ingest_automation_status.md"
IMPORT_SCRIPT="$ROOT_DIR/scripts/import_google_takeout_and_analyze.sh"
AUTO_ENABLED="${J40_PHOTO_INGEST_ENABLE:-0}"
ON_DEMAND_ENABLED="${J40_PHOTO_INGEST_ON_DEMAND:-0}"
AUTO_FLAG_FILE="$ROOT_DIR/data/config/photo_ingest_auto.flag"

mkdir -p "$STATE_DIR" "$LOG_DIR" "$DOWNLOADS_DIR"
touch "$PROCESSED_FILE"

if [ "$ON_DEMAND_ENABLED" != "1" ] && { [ "$AUTO_ENABLED" != "1" ] || [ ! -f "$AUTO_FLAG_FILE" ]; }; then
  exit 0
fi

find_candidates() {
  find "$DOWNLOADS_DIR" -maxdepth 1 -type f \
    \( -iname 'takeout-*.zip' -o -iname 'takeout-*.tgz' -o -iname 'takeout-*.tar.gz' \
       -o -iname '*Takeout*.zip' -o -iname '*Takeout*.tgz' -o -iname '*Takeout*.tar.gz' \
       -o -iname '*Google Photos*.zip' -o -iname '*Google Photos*.tgz' -o -iname '*Google Photos*.tar.gz' \) 2>/dev/null || true
}

already_processed() {
  local signature="$1"
  grep -Fqx "$signature" "$PROCESSED_FILE"
}

record_processed() {
  local signature="$1"
  echo "$signature" >> "$PROCESSED_FILE"
}

archive_signature() {
  local archive="$1"
  local size mtime
  size="$(stat -f '%z' "$archive")"
  mtime="$(stat -f '%m' "$archive")"
  printf '%s\t%s\t%s' "$archive" "$size" "$mtime"
}

write_status() {
  local now run_log processed_count
  now="$(date '+%Y-%m-%d %H:%M:%S %z')"
  processed_count="$(wc -l < "$PROCESSED_FILE" | tr -d ' ')"
  run_log="$1"

  cat > "$STATUS_FILE" <<EOF
# Photo Ingest Automation Status

- Updated: $now
- Watched ingest dir: \`$DOWNLOADS_DIR\`
- Processed archive signatures: \`$processed_count\`
- Last run log: \`$run_log\`
- Mode: \`single-pass ingest scanner (on-demand or scheduler-triggered)\`

## Flow

1. Detect new Google Takeout archive (\`.zip\`, \`.tgz\`, \`.tar.gz\`).
2. Run \`scripts/import_google_takeout_and_analyze.sh\` for that archive.
3. Rebuild photo inventory and component-job reconciliation outputs.
4. Persist processed signature to avoid duplicate reprocessing.
EOF
}

write_idle_status() {
  local now processed_count
  now="$(date '+%Y-%m-%d %H:%M:%S %z')"
  processed_count="$(wc -l < "$PROCESSED_FILE" | tr -d ' ')"

  cat > "$STATUS_FILE" <<EOF
# Photo Ingest Automation Status

- Updated: $now
- Watched ingest dir: \`$DOWNLOADS_DIR\`
- Processed archive signatures: \`$processed_count\`
- Last run log: \`(no archive processed in this scan)\`
- Mode: \`single-pass ingest scanner (on-demand or scheduler-triggered)\`
- Current state: \`waiting_for_takeout_archive\`

## Flow

1. Detect new Google Takeout archive (\`.zip\`, \`.tgz\`, \`.tar.gz\`).
2. Run \`scripts/import_google_takeout_and_analyze.sh\` for that archive.
3. Rebuild photo inventory and component-job reconciliation outputs.
4. Persist processed signature to avoid duplicate reprocessing.
EOF
}

candidates=()
while IFS= read -r line; do
  [ -n "$line" ] && candidates+=("$line")
done < <(find_candidates)

if [ ${#candidates[@]} -eq 0 ]; then
  write_idle_status
  exit 0
fi

archives=()
while IFS= read -r line; do
  [ -n "$line" ] && archives+=("$line")
done < <(ls -1t "${candidates[@]}")

for archive in "${archives[@]}"; do
  sig="$(archive_signature "$archive")"
  if already_processed "$sig"; then
    continue
  fi

  run_id="$(date +%Y%m%dT%H%M%S)"
  run_log="$LOG_DIR/${run_id}_cron_import.log"
  echo "[$(date '+%F %T')] Processing: $archive"

  if ARCHIVE_PATH="$archive" "$IMPORT_SCRIPT" >"$run_log" 2>&1; then
    record_processed "$sig"
    write_status "$run_log"
    echo "[$(date '+%F %T')] Completed: $archive"
  else
    echo "[$(date '+%F %T')] Failed: $archive (see $run_log)"
  fi
done
