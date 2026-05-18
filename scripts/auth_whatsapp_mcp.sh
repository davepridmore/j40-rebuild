#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="/Users/davidpridmore/IdeaProjects/J40"
PROFILE="${1:-}"
USE_TMP_USER_DIR="${WHATSAPP_MCP_USE_TMP_USER_DIR:-1}"
TMP_AUTH_PATH=""
AUTH_RUN_PATH=""
LOCAL_WWEB_MCP_MAIN="${PROJECT_ROOT}/tools/wweb-mcp-local/dist/main.js"
CHROME_EXEC_DEFAULT="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

if [[ -z "${PROFILE}" ]]; then
  echo "Usage: bash scripts/auth_whatsapp_mcp.sh <1|2>" >&2
  echo "Example: bash scripts/auth_whatsapp_mcp.sh 1" >&2
  exit 1
fi

case "${PROFILE}" in
  1)
    SERVER_NAME="whatsapp-number-1"
    AUTH_PATH="${PROJECT_ROOT}/.ai/mcp/auth/whatsapp-number-1"
    MEDIA_PATH="${PROJECT_ROOT}/data/raw/imports/mcp_whatsapp_number_1"
    API_PORT="3011"
    ;;
  2)
    SERVER_NAME="whatsapp-number-2"
    AUTH_PATH="${PROJECT_ROOT}/.ai/mcp/auth/whatsapp-number-2"
    MEDIA_PATH="${PROJECT_ROOT}/data/raw/imports/mcp_whatsapp_number_2"
    API_PORT="3012"
    ;;
  *)
    echo "Invalid profile: ${PROFILE}. Expected 1 or 2." >&2
    exit 1
    ;;
esac

mkdir -p "${AUTH_PATH}" "${MEDIA_PATH}"
AUTH_RUN_PATH="${AUTH_PATH}"

if [[ "${USE_TMP_USER_DIR}" == "1" ]]; then
  TMP_ROOT="${PROJECT_ROOT}/.ai/mcp/tmp_userdir"
  mkdir -p "${TMP_ROOT}"
  TMP_AUTH_PATH="$(mktemp -d "${TMP_ROOT}/${SERVER_NAME}.XXXXXX")"
  if [[ -d "${AUTH_PATH}" && -n "$(ls -A "${AUTH_PATH}" 2>/dev/null)" ]]; then
    if command -v rsync >/dev/null 2>&1; then
      rsync -a "${AUTH_PATH}/" "${TMP_AUTH_PATH}/"
    else
      cp -R "${AUTH_PATH}/." "${TMP_AUTH_PATH}/"
    fi
  fi
  AUTH_RUN_PATH="${TMP_AUTH_PATH}"
fi

sync_tmp_auth_back() {
  local exit_code=$?

  if [[ -n "${TMP_AUTH_PATH}" && -d "${TMP_AUTH_PATH}" ]]; then
    if [[ -n "$(ls -A "${TMP_AUTH_PATH}" 2>/dev/null)" ]]; then
      mkdir -p "${AUTH_PATH}"
      if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${TMP_AUTH_PATH}/" "${AUTH_PATH}/"
      else
        rm -rf "${AUTH_PATH}"
        mkdir -p "${AUTH_PATH}"
        cp -R "${TMP_AUTH_PATH}/." "${AUTH_PATH}/"
      fi
      echo "Synced auth data into ${AUTH_PATH}"
    fi
    rm -rf "${TMP_AUTH_PATH}"
  fi

  exit "${exit_code}"
}

trap sync_tmp_auth_back EXIT

echo "Starting WhatsApp auth for MCP server '${SERVER_NAME}'."
echo "Scan the QR code with the WhatsApp account for number profile ${PROFILE}."
echo "After login is confirmed, press Ctrl+C to stop this auth process."
if [[ "${USE_TMP_USER_DIR}" == "1" ]]; then
  echo "Using temporary userDir/auth path: ${AUTH_RUN_PATH}"
fi

if [[ -x "${CHROME_EXEC_DEFAULT}" && -z "${PUPPETEER_EXECUTABLE_PATH:-}" ]]; then
  export PUPPETEER_EXECUTABLE_PATH="${CHROME_EXEC_DEFAULT}"
fi

if [[ -f "${LOCAL_WWEB_MCP_MAIN}" ]]; then
  node "${LOCAL_WWEB_MCP_MAIN}" \
    -m whatsapp-api \
    -s local \
    -a "${AUTH_RUN_PATH}" \
    --media-storage-path "${MEDIA_PATH}" \
    --api-port "${API_PORT}" \
    -l info
else
  npx -y wweb-mcp@0.2.3 \
    -m whatsapp-api \
    -s local \
    -a "${AUTH_RUN_PATH}" \
    --media-storage-path "${MEDIA_PATH}" \
    --api-port "${API_PORT}" \
    -l info
fi
