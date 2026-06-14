from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
CAD_ROOT = ROOT / "data" / "manual" / "cad" / "j40_reference_model"
REPORT_DIR = CAD_ROOT / "05_reports"
STAMP_PATH = REPORT_DIR / "j40_cad_reference_update_stamp.json"
SCAFFOLD_MANIFEST_PATH = REPORT_DIR / "j40_full_vehicle_scaffold_rev_c_manifest.json"
LHD_REVIEW_MANIFEST_PATH = REPORT_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review_manifest.json"
SCAFFOLD_DIR = CAD_ROOT / "04_exports" / "scaffold_rev_c"
LHD_REVIEW_DIR = CAD_ROOT / "04_exports" / "scaffold_rev_c_lhd_review"
AS_FITTED_ROUTE_SCOPE = REPORT_DIR / "j40_as_fitted_route_model_scope_20260531.csv"
PAKISTAN_ROUTE_PURCHASE_BOM = ROOT / "data" / "manual" / "j40_as_fitted_route_pakistan_purchase_bom_20260531.csv"

INPUT_DIRS = [
    CAD_ROOT / "00_inbox",
    CAD_ROOT / "01_source_mesh",
    CAD_ROOT / "02_mesh_clean",
]
INPUT_FILES = [
    ROOT / "data" / "manual" / "photo_inventory.csv",
    ROOT / "data" / "manual" / "component_jobs.csv",
    ROOT / "data" / "manual" / "component_jobs_photo_reconciliation.csv",
    AS_FITTED_ROUTE_SCOPE,
    PAKISTAN_ROUTE_PURCHASE_BOM,
    ROOT / "scripts" / "update_j40_cad_reference.py",
    ROOT / "scripts" / "j40_cad_intake.py",
    ROOT / "scripts" / "freecad_mesh_to_cad.py",
    ROOT / "scripts" / "export_gltf_to_obj.py",
    ROOT / "scripts" / "export_gltf_to_3d_dxf.py",
    ROOT / "scripts" / "build_j40_public_reference_strategy.py",
    ROOT / "scripts" / "build_j40_digital_twin_evidence.py",
    ROOT / "tools" / "generate_j40_full_vehicle_cad_scaffold.py",
    ROOT / "tools" / "generate_j40_driver_layout_variant.py",
    ROOT / "tools" / "generate_j40_orbit_viewer.py",
    ROOT / "tools" / "generate_j40_source_mesh_freecad_macro.py",
]
EXPECTED_OUTPUTS = [
    SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c.FCMacro",
    SCAFFOLD_DIR / "j40_full_vehicle_orbit_viewer.html",
    CAD_ROOT / "04_exports" / "source_mesh_reference" / "j40_source_mesh_reference.FCMacro",
    SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c.scad",
    SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c_orthographic.dxf",
    SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c_3d_autocad.dxf",
    SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c.gltf",
    SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c_orthographic.png",
    SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c_parts.csv",
    SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c_editable.obj",
    SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c_editable.mtl",
    LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review.FCMacro",
    LHD_REVIEW_DIR / "j40_full_vehicle_orbit_viewer.html",
    LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review.scad",
    LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review_orthographic.dxf",
    LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review_3d_autocad.dxf",
    LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review.gltf",
    LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review_orthographic.png",
    LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review_parts.csv",
    LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review_editable.obj",
    LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review_editable.mtl",
    CAD_ROOT / "05_reports" / "source_model_inventory.md",
    CAD_ROOT / "05_reports" / "j40_source_mesh_reference_inventory.csv",
    CAD_ROOT / "05_reports" / "j40_full_vehicle_scaffold_rev_c_online_reference_inventory.csv",
    CAD_ROOT / "05_reports" / "j40_as_fitted_route_model_coverage_20260531.csv",
    CAD_ROOT / "05_reports" / "j40_full_vehicle_scaffold_rev_c_manifest.json",
    CAD_ROOT / "05_reports" / "j40_full_vehicle_scaffold_rev_c_lhd_review_online_reference_inventory.csv",
    CAD_ROOT / "05_reports" / "j40_full_vehicle_scaffold_rev_c_lhd_review_manifest.json",
    CAD_ROOT / "05_reports" / "j40_full_vehicle_scaffold_rev_c_lhd_review_notes.md",
    CAD_ROOT / "05_reports" / "j40_public_reference_strategy.csv",
    CAD_ROOT / "05_reports" / "j40_public_reference_strategy.md",
    CAD_ROOT / "05_reports" / "j40_digital_twin_evidence_matrix.csv",
    CAD_ROOT / "05_reports" / "j40_digital_twin_measurement_backlog.csv",
    CAD_ROOT / "05_reports" / "j40_digital_twin_build_notes.md",
    CAD_ROOT / "ATTRIBUTION.md",
]

SCAFFOLD_MANIFEST_EXTRA_OUTPUTS = [
    SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c_3d_autocad.dxf",
    SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c_editable.obj",
    SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c_editable.mtl",
]
LHD_REVIEW_MANIFEST_EXTRA_OUTPUTS = [
    LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review_3d_autocad.dxf",
    LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review_editable.obj",
    LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review_editable.mtl",
]


def file_record(path: Path) -> dict[str, object]:
    stat = path.stat()
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return {
        "path": str(path.relative_to(ROOT)),
        "size": stat.st_size,
        "sha256": digest.hexdigest(),
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


def sync_manifest_outputs(manifest_path: Path, extra_outputs: list[Path]) -> None:
    if not manifest_path.exists():
        return
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    outputs = data.setdefault("outputs", [])
    if not isinstance(outputs, list):
        return
    changed = False
    for path in extra_outputs:
        if not path.exists():
            continue
        relative_path = str(path.relative_to(ROOT))
        if relative_path not in outputs:
            outputs.append(relative_path)
            changed = True
    if changed:
        manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def sync_scaffold_manifest_outputs() -> None:
    sync_manifest_outputs(SCAFFOLD_MANIFEST_PATH, SCAFFOLD_MANIFEST_EXTRA_OUTPUTS)
    sync_manifest_outputs(LHD_REVIEW_MANIFEST_PATH, LHD_REVIEW_MANIFEST_EXTRA_OUTPUTS)


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
    run_step([sys.executable, str(ROOT / "tools" / "generate_j40_driver_layout_variant.py")])
    run_step([sys.executable, str(ROOT / "tools" / "generate_j40_source_mesh_freecad_macro.py")])
    run_step(
        [
            sys.executable,
            str(ROOT / "scripts" / "export_gltf_to_3d_dxf.py"),
            str(SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c.gltf"),
            str(SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c_3d_autocad.dxf"),
        ]
    )
    run_step(
        [
            sys.executable,
            str(ROOT / "scripts" / "export_gltf_to_3d_dxf.py"),
            str(LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review.gltf"),
            str(LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review_3d_autocad.dxf"),
        ]
    )
    run_step(
        [
            sys.executable,
            str(ROOT / "scripts" / "export_gltf_to_obj.py"),
            str(SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c.gltf"),
            str(SCAFFOLD_DIR / "j40_full_vehicle_scaffold_rev_c_editable.obj"),
        ]
    )
    run_step(
        [
            sys.executable,
            str(ROOT / "scripts" / "export_gltf_to_obj.py"),
            str(LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review.gltf"),
            str(LHD_REVIEW_DIR / "j40_full_vehicle_scaffold_rev_c_lhd_review_editable.obj"),
        ]
    )
    run_step([sys.executable, str(ROOT / "scripts" / "build_j40_public_reference_strategy.py")])
    run_step([sys.executable, str(ROOT / "scripts" / "build_j40_digital_twin_evidence.py")])
    sync_scaffold_manifest_outputs()
    after = input_signature()
    write_stamp(after, changed=not unchanged)
    print(f"J40 CAD reference updated. Stamp: {STAMP_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
