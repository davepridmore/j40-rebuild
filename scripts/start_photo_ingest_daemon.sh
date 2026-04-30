#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT_DIR/data/raw/imports/google_photos/daemon"
PID_FILE="$LOG_DIR/watch.pid"
STDOUT_LOG="$LOG_DIR/stdout.log"
STDERR_LOG="$LOG_DIR/stderr.log"
WATCH_SCRIPT="$ROOT_DIR/scripts/watch_takeout_and_ingest.sh"
DOWNLOADS_DIR="${DOWNLOADS_DIR:-$ROOT_DIR/data/inbox/takeout}"
POLL_SECONDS="${POLL_SECONDS:-300}"

mkdir -p "$LOG_DIR"
mkdir -p "$DOWNLOADS_DIR"

if [ -f "$PID_FILE" ]; then
  old_pid="$(cat "$PID_FILE" || true)"
  if [ -n "${old_pid:-}" ] && kill -0 "$old_pid" >/dev/null 2>&1; then
    echo "Photo ingest daemon already running (PID: $old_pid)"
    exit 0
  fi
fi

nohup env DOWNLOADS_DIR="$DOWNLOADS_DIR" POLL_SECONDS="$POLL_SECONDS" \
  "$WATCH_SCRIPT" >"$STDOUT_LOG" 2>"$STDERR_LOG" < /dev/null &

new_pid="$!"
echo "$new_pid" > "$PID_FILE"

echo "Started photo ingest daemon."
echo "PID: $new_pid"
echo "Downloads: $DOWNLOADS_DIR"
echo "Poll seconds: $POLL_SECONDS"
echo "Logs:"
echo "  $STDOUT_LOG"
echo "  $STDERR_LOG"
