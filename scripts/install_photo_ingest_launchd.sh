#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WATCH_SCRIPT="$ROOT_DIR/scripts/watch_takeout_and_ingest.sh"
AGENT_LABEL="com.j40.photo-ingest"
AGENT_DIR="$HOME/Library/LaunchAgents"
PLIST_PATH="$AGENT_DIR/${AGENT_LABEL}.plist"
LOG_DIR="$ROOT_DIR/data/raw/imports/google_photos/launchd"
INGEST_DIR="$ROOT_DIR/data/inbox/takeout"

mkdir -p "$AGENT_DIR" "$LOG_DIR" "$INGEST_DIR"

cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$AGENT_LABEL</string>

  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>$WATCH_SCRIPT</string>
  </array>

  <key>EnvironmentVariables</key>
  <dict>
    <key>DOWNLOADS_DIR</key>
    <string>$INGEST_DIR</string>
    <key>POLL_SECONDS</key>
    <string>300</string>
  </dict>

  <key>RunAtLoad</key>
  <true/>

  <key>KeepAlive</key>
  <true/>

  <key>StandardOutPath</key>
  <string>$LOG_DIR/stdout.log</string>
  <key>StandardErrorPath</key>
  <string>$LOG_DIR/stderr.log</string>
</dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)/$AGENT_LABEL" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$PLIST_PATH"
launchctl enable "gui/$(id -u)/$AGENT_LABEL"
launchctl kickstart -k "gui/$(id -u)/$AGENT_LABEL"

echo "Installed and started launchd agent: $AGENT_LABEL"
echo "Plist: $PLIST_PATH"
echo "Watched ingest dir: $INGEST_DIR"
echo "Logs:"
echo "  $LOG_DIR/stdout.log"
echo "  $LOG_DIR/stderr.log"
