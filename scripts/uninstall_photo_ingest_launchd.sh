#!/usr/bin/env bash
set -euo pipefail

AGENT_LABEL="com.j40.photo-ingest"
PLIST_PATH="$HOME/Library/LaunchAgents/${AGENT_LABEL}.plist"

launchctl bootout "gui/$(id -u)/$AGENT_LABEL" >/dev/null 2>&1 || true
launchctl disable "gui/$(id -u)/$AGENT_LABEL" >/dev/null 2>&1 || true

if [ -f "$PLIST_PATH" ]; then
  rm -f "$PLIST_PATH"
fi

echo "Uninstalled launchd agent: $AGENT_LABEL"
