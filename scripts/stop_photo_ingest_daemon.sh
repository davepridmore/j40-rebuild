#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$ROOT_DIR/data/raw/imports/google_photos/daemon/watch.pid"

if [ ! -f "$PID_FILE" ]; then
  echo "No daemon PID file found."
  exit 0
fi

pid="$(cat "$PID_FILE" || true)"
if [ -z "${pid:-}" ]; then
  echo "PID file is empty; removing."
  rm -f "$PID_FILE"
  exit 0
fi

if kill -0 "$pid" >/dev/null 2>&1; then
  kill "$pid"
  sleep 1
  if kill -0 "$pid" >/dev/null 2>&1; then
    kill -9 "$pid" >/dev/null 2>&1 || true
  fi
  echo "Stopped photo ingest daemon (PID: $pid)."
else
  echo "Process $pid not running."
fi

rm -f "$PID_FILE"
