#!/usr/bin/env bash
set -euo pipefail

CRON_MARKER="# J40_PHOTO_INGEST_CRON"

existing_cron="$(crontab -l 2>/dev/null || true)"
cleaned_cron="$(printf '%s\n' "$existing_cron" | sed "/$CRON_MARKER/d")"

if [ -n "$cleaned_cron" ]; then
  printf '%s\n' "$cleaned_cron" | crontab -
else
  crontab -r >/dev/null 2>&1 || true
fi

echo "Uninstalled photo ingest cron entry."
