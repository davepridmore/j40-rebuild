from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANUAL_DIR = ROOT / "data" / "manual"

PHOTO_INVENTORY_PATH = MANUAL_DIR / "photo_inventory.csv"
OUTPUT_PATH = MANUAL_DIR / "paint_refinish_media_queue.csv"

PREPARED_SEND_COMPONENTS = {
    "detached_body_panels_and_doors",
    "detached_doors_and_panels",
    "rear_hatch_inner_panel",
}
RETURNED_COMPONENTS = {
    "rear_hatch_window_latch_mechanisms",
    "refinished_hinges_brackets_and_trim",
    "refinished_seat_or_mount_bracket",
    "wiper_arm_or_linkage_hardware",
}
IN_PROGRESS_VIDEO_COMPONENTS = {
    "wing_removal_and_body_lift_prep",
    "panel_detail_and_markings",
    "off_vehicle_workstation_reference_video",
}
PAINT_COMPONENT_GROUPS = {
    "removable_panels",
    "body_exterior",
    "roof_and_gutters",
    "body_floor",
    "interior_cabin",
}
PAINT_STAGES = {
    "removed_parts_cataloguing",
    "hardware_refinish",
    "rust_assessment",
    "stripdown_cataloguing",
    "reference_material",
}


def load_photo_inventory() -> list[dict[str, str]]:
    with PHOTO_INVENTORY_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def classify(row: dict[str, str]) -> str:
    specific_component = (row.get("specific_component") or "").strip().lower()
    stage = (row.get("stage") or "").strip().lower()
    component_group = (row.get("component_group") or "").strip().lower()
    media_type = (row.get("media_type") or "").strip().lower()

    if stage == "rust_assessment":
        return "issue_tracking"
    if stage == "removed_parts_cataloguing" and (specific_component in PREPARED_SEND_COMPONENTS or component_group in PAINT_COMPONENT_GROUPS):
        return "prepared_for_send_out"
    if stage == "hardware_refinish" and (specific_component in RETURNED_COMPONENTS or component_group in PAINT_COMPONENT_GROUPS):
        return "returned_from_painter"
    if media_type == "video" and (specific_component in IN_PROGRESS_VIDEO_COMPONENTS or stage in PAINT_STAGES):
        return "in_progress_video"
    if media_type == "photo" and stage == "stripdown_cataloguing" and component_group in PAINT_COMPONENT_GROUPS:
        return "in_progress_photo"
    return ""


def build_rows(photo_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []
    for row in photo_rows:
        evidence_bucket = classify(row)
        if not evidence_bucket:
            continue
        output_rows.append(
            {
                "media_id": row.get("media_id", ""),
                "file_name": row.get("file_name", ""),
                "relative_path": row.get("relative_path", ""),
                "captured_date": row.get("captured_date", ""),
                "captured_time": row.get("captured_time", ""),
                "media_type": row.get("media_type", ""),
                "evidence_bucket": evidence_bucket,
                "component_group": row.get("component_group", ""),
                "specific_component": row.get("specific_component", ""),
                "stage": row.get("stage", ""),
                "observed_state": row.get("observed_state", ""),
                "confidence": row.get("confidence", ""),
                "tags": row.get("tags", ""),
                "notes": row.get("notes", ""),
            }
        )
    output_rows.sort(key=lambda r: (r["captured_date"], r["captured_time"], r["media_id"]))
    return output_rows


def write_csv(rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "media_id",
        "file_name",
        "relative_path",
        "captured_date",
        "captured_time",
        "media_type",
        "evidence_bucket",
        "component_group",
        "specific_component",
        "stage",
        "observed_state",
        "confidence",
        "tags",
        "notes",
    ]
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    photo_rows = load_photo_inventory()
    output_rows = build_rows(photo_rows)
    write_csv(output_rows)
    print(f"Wrote paint queue: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Rows: {len(output_rows)}")


if __name__ == "__main__":
    main()
