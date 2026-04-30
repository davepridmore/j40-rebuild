#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  cat <<'EOF'
Usage: run_personal_photos_picker_on_demand.sh

Runs personal Google Photos Picker import, then:
1) rebuilds photo inventory
2) filters probable non-car media
3) rebuilds inventory (post-filter)
4) refreshes component/photo reconciliation

Environment overrides:
  CLIENT_SECRETS       OAuth desktop client JSON path
  TOKEN_FILE           Persisted token JSON path
  HISTORY_FILE         Import history CSV path
  RECENT_DAYS          Picker time filter after selection (default: 120)
  POLL_TIMEOUT_SECONDS Picker wait timeout (default: 1800)
  OPEN_BROWSER         1 to auto-open URLs, 0 otherwise (default: 1)
  INCLUDE_VIDEOS       1 to include videos (default: 1)
  MOVE_NON_CAR         1 to move probable non-car files to review folder (default: 1)
EOF
  exit 0
fi

CLIENT_SECRETS="${CLIENT_SECRETS:-$ROOT_DIR/../perception-infra/gcloud/oauth_client.json}"
TOKEN_FILE="${TOKEN_FILE:-$ROOT_DIR/data/raw/imports/google_photos/token_photospicker_personal.json}"
HISTORY_FILE="${HISTORY_FILE:-$ROOT_DIR/data/raw/imports/google_photos/import_history_personal.csv}"
RECENT_DAYS="${RECENT_DAYS:-120}"
POLL_TIMEOUT_SECONDS="${POLL_TIMEOUT_SECONDS:-1800}"
OPEN_BROWSER="${OPEN_BROWSER:-1}"
INCLUDE_VIDEOS="${INCLUDE_VIDEOS:-1}"
MOVE_NON_CAR="${MOVE_NON_CAR:-1}"

if [ ! -f "$CLIENT_SECRETS" ]; then
  echo "OAuth client secrets file not found: $CLIENT_SECRETS"
  echo "Set CLIENT_SECRETS to a valid personal OAuth desktop client JSON."
  exit 1
fi

picker_args=(
  "$ROOT_DIR/scripts/import_google_photos_picker.py"
  --auth-mode oauth-client
  --client-secrets "$CLIENT_SECRETS"
  --token-file "$TOKEN_FILE"
  --history-file "$HISTORY_FILE"
  --recent-days "$RECENT_DAYS"
  --poll-timeout-seconds "$POLL_TIMEOUT_SECONDS"
)

if [ "$OPEN_BROWSER" = "1" ]; then
  picker_args+=(--open-browser)
fi

if [ "$INCLUDE_VIDEOS" = "1" ]; then
  picker_args+=(--include-videos)
fi

python3 "${picker_args[@]}"

python3 "$ROOT_DIR/scripts/build_photo_inventory.py"
if [ "$MOVE_NON_CAR" = "1" ]; then
  python3 "$ROOT_DIR/scripts/filter_non_car_media.py" --apply
  python3 "$ROOT_DIR/scripts/build_photo_inventory.py"
else
  python3 "$ROOT_DIR/scripts/filter_non_car_media.py"
fi
python3 "$ROOT_DIR/scripts/reconcile_component_jobs_photo_inventory.py"

echo "Updated outputs:"
echo "- $ROOT_DIR/data/manual/photo_inventory.csv"
echo "- $ROOT_DIR/data/manual/photo_non_car_filter_report.csv"
echo "- $ROOT_DIR/docs/photo-catalog.md"
echo "- $ROOT_DIR/docs/component-jobs-photo-reconciliation.md"
