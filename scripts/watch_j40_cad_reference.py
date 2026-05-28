from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parent.parent
UPDATE_SCRIPT = ROOT / "scripts" / "update_j40_cad_reference.py"


def run_update(force: bool) -> None:
    command = [sys.executable, str(UPDATE_SCRIPT), "--skip-if-unchanged"]
    if force:
        command.append("--force")
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Watch and refresh the J40 CAD reference scaffold.")
    parser.add_argument("--interval", type=float, default=10.0, help="poll interval in seconds")
    parser.add_argument("--once", action="store_true", help="run one update check and exit")
    parser.add_argument("--force", action="store_true", help="force the first update")
    args = parser.parse_args()

    first = True
    while True:
        run_update(force=args.force and first)
        first = False
        if args.once:
            return
        time.sleep(args.interval)


if __name__ == "__main__":
    main()

