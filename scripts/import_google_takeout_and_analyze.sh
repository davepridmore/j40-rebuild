#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOWNLOADS_DIR="${DOWNLOADS_DIR:-$ROOT_DIR/data/inbox/takeout}"
IMPORT_DIR="$ROOT_DIR/data/raw/imports/google_photos/takeout/latest"
PHOTOS_DIR="$ROOT_DIR/photos"
ARCHIVE_PATH="${ARCHIVE_PATH:-}"
WAIT_FOR_FILE="${WAIT_FOR_FILE:-0}"
WAIT_TIMEOUT_MINUTES="${WAIT_TIMEOUT_MINUTES:-180}"
WAIT_POLL_SECONDS="${WAIT_POLL_SECONDS:-30}"

echo "Project: $ROOT_DIR"
echo "Downloads: $DOWNLOADS_DIR"

mkdir -p "$IMPORT_DIR" "$PHOTOS_DIR"
rm -rf "$IMPORT_DIR"/*

find_candidates() {
  find "$DOWNLOADS_DIR" -maxdepth 1 -type f \
    \( -iname 'takeout-*.zip' -o -iname 'takeout-*.tgz' -o -iname 'takeout-*.tar.gz' \
       -o -iname '*Takeout*.zip' -o -iname '*Takeout*.tgz' -o -iname '*Takeout*.tar.gz' \
       -o -iname '*Google Photos*.zip' -o -iname '*Google Photos*.tgz' -o -iname '*Google Photos*.tar.gz' \) 2>/dev/null || true
}

load_candidates() {
  local line
  candidates=()
  while IFS= read -r line; do
    [ -n "$line" ] && candidates+=("$line")
  done < <(find_candidates)
}

if [ -n "$ARCHIVE_PATH" ]; then
  if [ ! -f "$ARCHIVE_PATH" ]; then
    echo "ARCHIVE_PATH does not exist: $ARCHIVE_PATH"
    exit 1
  fi
  candidates=("$ARCHIVE_PATH")
else
  load_candidates
fi

if [ ${#candidates[@]} -eq 0 ] && [ "$WAIT_FOR_FILE" = "1" ]; then
  echo "No archive found yet. Waiting for Takeout file in $DOWNLOADS_DIR ..."
  deadline=$(( $(date +%s) + WAIT_TIMEOUT_MINUTES * 60 ))
  while [ "$(date +%s)" -lt "$deadline" ]; do
    sleep "$WAIT_POLL_SECONDS"
    load_candidates
    if [ ${#candidates[@]} -gt 0 ]; then
      break
    fi
  done
fi

if [ ${#candidates[@]} -eq 0 ]; then
  echo "No Google Takeout archive found in $DOWNLOADS_DIR"
  echo "Expected one of: .zip / .tgz / .tar.gz"
  echo "Wait for the Takeout completion email, download the archive, then run this again."
  exit 1
fi

zips=()
while IFS= read -r line; do
  [ -n "$line" ] && zips+=("$line")
done < <(ls -1t "${candidates[@]}")

echo "Using archive file(s):"
printf '  %s\n' "${zips[@]}"

for z in "${zips[@]}"; do
  case "$z" in
    *.zip|*.ZIP)
      unzip -q -o "$z" -d "$IMPORT_DIR"
      ;;
    *.tgz|*.tar.gz)
      tar -xzf "$z" -C "$IMPORT_DIR"
      ;;
    *)
      echo "Skipping unsupported archive format: $z"
      ;;
  esac
done

while IFS= read -r -d '' file_path; do
  base_name="$(basename "$file_path")"
  target_path="$PHOTOS_DIR/$base_name"

  if [ -e "$target_path" ]; then
    short_hash="$(shasum -a 1 "$file_path" | awk '{print substr($1,1,8)}')"
    stem="${base_name%.*}"
    ext="${base_name##*.}"
    target_path="$PHOTOS_DIR/${stem}_${short_hash}.${ext}"
  fi

  cp "$file_path" "$target_path"
done < <(
  find "$IMPORT_DIR" -type f \
    \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.heic' -o -iname '*.heif' -o -iname '*.mp4' -o -iname '*.mov' \) \
    -print0
)

python3 "$ROOT_DIR/scripts/build_photo_inventory.py"
python3 "$ROOT_DIR/scripts/reconcile_component_jobs_photo_inventory.py"

echo "Done."
echo "Inventory: $ROOT_DIR/data/manual/photo_inventory.csv"
echo "Catalog:   $ROOT_DIR/docs/photo-catalog.md"
echo "Recon:     $ROOT_DIR/docs/component-jobs-photo-reconciliation.md"
