#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dashboard="$repo_root/docs/project-control-ui/index.html"

if [[ ! -f "$dashboard" ]]; then
  echo "Dashboard HTML not found: $dashboard" >&2
  exit 1
fi

case "$(uname -s)" in
  Darwin)
    open "$dashboard"
    ;;
  Linux)
    xdg-open "$dashboard"
    ;;
  CYGWIN*|MINGW*|MSYS*)
    start "" "$dashboard"
    ;;
  *)
    echo "Open this file in your browser:" >&2
    echo "$dashboard"
    ;;
esac
