from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys


TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import generate_j40_full_vehicle_cad_scaffold as scaffold  # noqa: E402


CAD_ROOT = ROOT / "data" / "manual" / "cad" / "j40_reference_model"
VARIANT_OUT_DIR = CAD_ROOT / "04_exports" / "scaffold_rev_c_lhd_review"

NAME_REPLACEMENTS = [
    ("right_hand_drive", "left_hand_drive"),
    ("pitman_arm_right", "pitman_arm_left"),
    ("front_drag_link_right", "front_drag_link_left"),
    ("steering_box_right_frame", "steering_box_left_frame"),
    ("front_hard_line_right_frame", "front_hard_line_left_frame"),
    ("rear_hard_line_right_frame", "rear_hard_line_left_frame"),
    ("rhd_", "lhd_"),
]

NOTE_REPLACEMENTS = [
    ("right-hand-drive", "left-hand-drive"),
    ("Right-hand-drive", "Left-hand-drive"),
    ("RHD", "LHD"),
    ("right frame rail", "left frame rail"),
    ("right rail", "left rail"),
    ("right-firewall", "left-firewall"),
    ("right footwell", "left footwell"),
]


def configure_lhd_review() -> None:
    scaffold.OUT_DIR = VARIANT_OUT_DIR
    scaffold.MODEL_NAME = "j40_full_vehicle_scaffold_rev_c_lhd_review"
    scaffold.MODEL_TITLE = "J40 Full Vehicle CAD Scaffold Rev C - LHD Driver-Side Review Variant"
    scaffold.MODEL_SHORT_TITLE = "J40 full vehicle CAD scaffold Rev C LHD review"
    scaffold.DETAIL_REVISION = "lhd_review_mirrored_driver_controls_as_fitted_route_scope"
    scaffold.DRIVER_LAYOUT = "left-hand drive"
    scaffold.TRAFFIC_SIDE = "right-side traffic"
    scaffold.DRIVER_SIDE = "left"
    scaffold.DRIVER_Y_SIGN = -1
    scaffold.DRIVER_Y = -420
    scaffold.PASSENGER_Y = 420
    scaffold.DRIVER_Y_DIRECTION = "negative"
    scaffold.DRIVER_LAYOUT_NOTE = (
        f"{scaffold.DRIVER_LAYOUT.capitalize()} review layout for {scaffold.TRAFFIC_SIDE}; "
        f"{scaffold.DRIVER_Y_DIRECTION} Y is the driver side."
    )


def relabel_driver_side(part: scaffold.PartType) -> scaffold.PartType:
    name = part.name
    notes = part.notes
    for old, new in NAME_REPLACEMENTS:
        name = name.replace(old, new)
    for old, new in NOTE_REPLACEMENTS:
        notes = notes.replace(old, new)
    return replace(part, name=name, notes=notes)


def main() -> None:
    configure_lhd_review()
    scaffold.OUT_DIR.mkdir(parents=True, exist_ok=True)
    scaffold.REPORT_DIR.mkdir(parents=True, exist_ok=True)
    model_parts = [relabel_driver_side(part) for part in scaffold.parts()]

    outputs = [
        scaffold.write_scad(model_parts),
        scaffold.write_freecad_macro(model_parts),
        scaffold.write_svg(model_parts),
        scaffold.write_png_preview(model_parts),
        scaffold.write_dxf(model_parts),
        scaffold.write_gltf(model_parts),
        scaffold.write_inventory(model_parts),
        scaffold.write_online_reference_inventory(),
    ]
    gallery_cues = scaffold.REPORT_DIR / "j40_3dmodels_gallery_visual_cues.json"
    if gallery_cues.exists():
        outputs.append(gallery_cues)

    original_parts = scaffold.parts
    scaffold.parts = lambda: list(model_parts)  # type: ignore[assignment]
    try:
        import generate_j40_orbit_viewer as viewer

        viewer.OUT_DIR = scaffold.OUT_DIR
        viewer.OUT_PATH = scaffold.OUT_DIR / "j40_full_vehicle_orbit_viewer.html"
        viewer.MODEL_TITLE = scaffold.MODEL_TITLE
        viewer.DRIVER_LAYOUT = scaffold.DRIVER_LAYOUT
        viewer.TRAFFIC_SIDE = scaffold.TRAFFIC_SIDE
        viewer.parts = scaffold.parts
        outputs.append(viewer.write_viewer())
    finally:
        scaffold.parts = original_parts  # type: ignore[assignment]

    notes = scaffold.write_notes(model_parts, outputs)
    manifest = scaffold.write_manifest(outputs + [notes], model_parts)
    for output in outputs + [notes, manifest]:
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
