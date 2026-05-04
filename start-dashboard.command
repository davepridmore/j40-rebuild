#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dashboard="$repo_root/docs/project-control-ui/index.html"
python_bin="${PYTHON_BIN:-python3}"
preferred_port="${PORT:-8765}"

if [[ ! -f "$dashboard" ]]; then
  echo "Dashboard HTML not found: $dashboard" >&2
  exit 1
fi

if ! command -v "$python_bin" >/dev/null 2>&1; then
  echo "Python not found: $python_bin" >&2
  echo "Set PYTHON_BIN=/path/to/python3 or install python3." >&2
  exit 1
fi

port="$("$python_bin" - "$preferred_port" <<'PY'
import socket
import sys

preferred = int(sys.argv[1])
for candidate in (preferred, 0):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", candidate))
        except OSError:
            continue
        print(sock.getsockname()[1])
        raise SystemExit(0)

raise SystemExit("Could not find a free local port")
PY
)"

url="http://127.0.0.1:$port/docs/project-control-ui/"
log_file="${TMPDIR:-/tmp}/j40-dashboard-$port.log"

"$python_bin" -m http.server "$port" --bind 127.0.0.1 --directory "$repo_root" >"$log_file" 2>&1 &
server_pid=$!
trap 'kill "$server_pid" 2>/dev/null || true' EXIT INT TERM

sleep 0.4
if ! kill -0 "$server_pid" 2>/dev/null; then
  echo "Dashboard server failed to start. Log:" >&2
  echo "$log_file" >&2
  exit 1
fi

if [[ "${NO_OPEN:-0}" != "1" ]]; then
  case "$(uname -s)" in
    Darwin)
      open "$url"
      ;;
    Linux)
      xdg-open "$url"
      ;;
    CYGWIN*|MINGW*|MSYS*)
      start "" "$url"
      ;;
    *)
      echo "Open this URL in your browser:" >&2
      echo "$url"
      ;;
  esac
fi

echo "Serving J40 dashboard at $url"
echo "Press Ctrl+C to stop the local dashboard server."
wait "$server_pid"
