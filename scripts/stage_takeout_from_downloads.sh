#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="${SOURCE_DIR:-$HOME/Downloads}"
TARGET_DIR="${TARGET_DIR:-$ROOT_DIR/data/inbox/takeout}"
AUTO_ENABLED="${J40_PHOTO_INGEST_ENABLE:-0}"
ON_DEMAND_ENABLED="${J40_PHOTO_INGEST_ON_DEMAND:-0}"
AUTO_FLAG_FILE="$ROOT_DIR/data/config/photo_ingest_auto.flag"

if [ "$ON_DEMAND_ENABLED" != "1" ] && { [ "$AUTO_ENABLED" != "1" ] || [ ! -f "$AUTO_FLAG_FILE" ]; }; then
  echo "Photo ingest auto-mode disabled; skipping stage."
  exit 0
fi

mkdir -p "$TARGET_DIR"

while IFS= read -r -d '' archive; do
    target="$TARGET_DIR/$(basename "$archive")"
    if [ -e "$target" ]; then
      continue
    fi
    cp "$archive" "$target"
    echo "Staged: $archive -> $target"
done < <(
  find "$SOURCE_DIR" -maxdepth 1 -type f \
    \( -iname 'takeout-*.zip' -o -iname 'takeout-*.tgz' -o -iname 'takeout-*.tar.gz' \
       -o -iname '*Takeout*.zip' -o -iname '*Takeout*.tgz' -o -iname '*Takeout*.tar.gz' \
       -o -iname '*Google Photos*.zip' -o -iname '*Google Photos*.tgz' -o -iname '*Google Photos*.tar.gz' \) \
    -print0 2>/dev/null || true
)

echo "Done. Ingest folder: $TARGET_DIR"
