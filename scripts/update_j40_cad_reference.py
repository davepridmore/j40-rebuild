from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
CAD_ROOT = ROOT / "data" / "manual" / "cad" / "j40_reference_model"
REPORT_DIR = CAD_ROOT / "05_reports"
STAMP_PATH = REPORT_DIR / "j40_cad_reference_update_stamp.json"

INPUT_DIRS = [
    CAD_ROOT / "00_inbox",
    CAD_ROOT / "02_mesh_clean",
]
INPUT_FILES = [
    ROOT / "scripts" / "j40_cad_intake.py",
    ROOT / "scripts" / "freecad_mesh_to_cad.py",
    ROOT / "tools" / "generate_j40_full_vehicle_cad_scaffold.py",
    ROOT / "tools" / "generate_j40_orbit_viewer.py",
    ROOT / "tools" / "generate_j40_source_mesh_freecad_macro.py",
]
EXPECTED_OUTPUTS = [
    CAD_ROOT / "04_exports" / "scaffold_rev_b" / "j40_full_vehicle_scaffold_rev_b.FCMacro",
    CAD_ROOT / "04_exports" / "scaffold_rev_b" / "j40_full_vehicle_orbit_viewer.html",
    CAD_ROOT / "04_exports" / "source_mesh_reference" / "j40_source_mesh_reference.FCMacro",
    CAD_ROOT / "04_exports" / "scaffold_rev_b" / "j40_full_vehicle_scaffold_rev_b.scad",
    CAD_ROOT / "04_exports" / "scaffold_rev_b" / "j40_full_vehicle_scaffold_rev_b_orthographic.dxf",
    CAD_ROOT / "04_exports" / "scaffold_rev_b" / "j40_full_vehicle_scaffold_rev_b.gltf",
    CAD_ROOT / "04_exports" / "scaffold_rev_b" / "j40_full_vehicle_scaffold_rev_b_orthographic.png",
    CAD_ROOT / "04_exports" / "scaffold_rev_b" / "j40_full_vehicle_scaffold_rev_b_parts.csv",
    CAD_ROOT / "05_reports" / "source_model_inventory.md",
    CAD_ROOT / "05_reports" / "j40_source_mesh_reference_inventory.csv",
    CAD_ROOT / "05_reports" / "j40_full_vehicle_scaffold_rev_b_manifest.json",
    CAD_ROOT / "ATTRIBUTION.md",
]


def file_record(path: Path) -> dict[str, object]:
    stat = path.stat()
    return {
        "path": str(path.relative_to(ROOT)),
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
    }


def input_signature() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for input_file in INPUT_FILES:
        if input_file.exists():
            records.append(file_record(input_file))
    for input_dir in INPUT_DIRS:
        if not input_dir.exists():
            continue
        for path in sorted(input_dir.rglob("*")):
            if path.is_file() and path.name != ".gitkeep":
                records.append(file_record(path))
    return records


def load_stamp() -> dict[str, object] | None:
    if not STAMP_PATH.exists():
        return None
    try:
        return json.loads(STAMP_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def outputs_ready() -> bool:
    return all(path.exists() for path in EXPECTED_OUTPUTS)


def run_step(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def write_stamp(signature: list[dict[str, object]], changed: bool) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "changed": changed,
        "input_signature": signature,
        "outputs": [str(path.relative_to(ROOT)) for path in EXPECTED_OUTPUTS if path.exists()],
    }
    STAMP_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh the J40 CAD reference scaffold and intake reports.")
    parser.add_argument("--force", action="store_true", help="regenerate even when inputs appear unchanged")
    parser.add_argument("--skip-if-unchanged", action="store_true", help="skip regeneration when inputs and outputs are current")
    args = parser.parse_args()

    before = input_signature()
    stamp = load_stamp()
    unchanged = bool(stamp and stamp.get("input_signature") == before and outputs_ready())

    if args.skip_if_unchanged and unchanged and not args.force:
        print("J40 CAD reference is current; no regeneration needed.")
        return

    run_step([sys.executable, str(ROOT / "scripts" / "j40_cad_intake.py")])
    run_step([sys.executable, str(ROOT / "tools" / "generate_j40_full_vehicle_cad_scaffold.py")])
    run_step([sys.executable, str(ROOT / "tools" / "generate_j40_orbit_viewer.py")])
    run_step([sys.executable, str(ROOT / "tools" / "generate_j40_source_mesh_freecad_macro.py")])
    after = input_signature()
    write_stamp(after, changed=not unchanged)
    print(f"J40 CAD reference updated. Stamp: {STAMP_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
