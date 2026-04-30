#!/usr/bin/env bash
set -euo pipefail

CREDENTIALS_PATH="${GOOGLE_WORKSPACE_CREDENTIALS_PATH:-/Users/davidpridmore/IdeaProjects/J40/client_secret_969930271813-7128p3h5nduj101tvbapconlnif7mm0a.apps.googleusercontent.com.json}"
PROFILE="${GOOGLE_WORKSPACE_MCP_PROFILE:-j40-orders-receipts}"
SERVICES="${GOOGLE_WORKSPACE_SERVICES:-gmail,drive}"

if [ -z "${GOOGLE_CLIENT_ID:-}" ] || [ -z "${GOOGLE_CLIENT_SECRET:-}" ]; then
  if [ ! -f "${CREDENTIALS_PATH}" ]; then
    echo "Missing credentials file: ${CREDENTIALS_PATH}" >&2
    echo "Set GOOGLE_WORKSPACE_CREDENTIALS_PATH or GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET." >&2
    exit 1
  fi

  if ! command -v jq >/dev/null 2>&1; then
    echo "jq is required to parse credentials.json." >&2
    exit 1
  fi

  export GOOGLE_CLIENT_ID="${GOOGLE_CLIENT_ID:-$(jq -r '.installed.client_id // .client_id // empty' "${CREDENTIALS_PATH}")}"
  export GOOGLE_CLIENT_SECRET="${GOOGLE_CLIENT_SECRET:-$(jq -r '.installed.client_secret // .client_secret // empty' "${CREDENTIALS_PATH}")}"
fi

if [ -z "${GOOGLE_CLIENT_ID:-}" ] || [ -z "${GOOGLE_CLIENT_SECRET:-}" ]; then
  echo "Could not load GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET." >&2
  echo "Check ${CREDENTIALS_PATH} or export the env vars manually." >&2
  exit 1
fi

export GOOGLE_WORKSPACE_MCP_PROFILE="${PROFILE}"
export GOOGLE_WORKSPACE_SERVICES="${SERVICES}"

echo "Running OAuth auth flow for profile '${GOOGLE_WORKSPACE_MCP_PROFILE}' with services '${GOOGLE_WORKSPACE_SERVICES}'."
echo "A browser window should open for Google consent."
npx -y @dguido/google-workspace-mcp@3.4.4 auth

echo "Auth complete. You can now use MCP server 'google-orders-receipts' from .ai/mcp/mcp.json."
