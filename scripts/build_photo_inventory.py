from __future__ import annotations

import csv
import os
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PHOTOS_DIR = ROOT / "photos"
MANUAL_DIR = ROOT / "data" / "manual"
DOCS_DIR = ROOT / "docs"
INDEX_DIR = PHOTOS_DIR / "index"

PHOTO_INVENTORY_PATH = MANUAL_DIR / "photo_inventory.csv"
PHOTO_SUMMARY_PATH = MANUAL_DIR / "photo_component_summary.csv"
CATALOG_PATH = DOCS_DIR / "photo-catalog.md"

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".heic", ".heif", ".mp4", ".mov", ".avi", ".mkv"}


@dataclass(frozen=True)
class Classification:
    component_group: str
    specific_component: str
    stage: str
    observed_state: str
    confidence: str
    tags: tuple[str, ...]
    notes: str = ""


def c(
    component_group: str,
    specific_component: str,
    stage: str,
    observed_state: str,
    confidence: str,
    tags: tuple[str, ...],
    notes: str = "",
) -> Classification:
    return Classification(component_group, specific_component, stage, observed_state, confidence, tags, notes)


DATE_DEFAULTS: dict[str, Classification] = {
    "20260314": c(
        "body_exterior",
        "fuel_filler_side_panel",
        "baseline_walkaround",
        "assembled",
        "high",
        ("exterior", "fuel", "panel"),
    ),
    "20260317": c(
        "interior_cabin",
        "cabin_overview",
        "baseline_walkaround",
        "assembled",
        "high",
        ("interior", "baseline"),
    ),
    "20260319": c(
        "removable_panels",
        "detached_doors_and_panels",
        "removed_parts_cataloguing",
        "removed_from_vehicle",
        "high",
        ("doors", "removed", "storage"),
    ),
    "20260320": c(
        "electrical_system",
        "firewall_and_dash_wiring",
        "electrical_rework",
        "under_rework",
        "high",
        ("wiring", "firewall", "dash"),
    ),
    "20260321": c(
        "interior_cabin",
        "floor_pan_and_firewall",
        "stripdown_cataloguing",
        "trim_removed",
        "high",
        ("floor_pan", "stripdown", "firewall"),
    ),
    "20260323": c(
        "interior_cabin",
        "dashboard_and_cabin_stripdown",
        "stripdown_cataloguing",
        "trim_removed",
        "high",
        ("dashboard", "stripdown", "interior"),
    ),
    "20260324": c(
        "chassis_underside",
        "rear_axle_and_leaf_springs",
        "underside_inspection",
        "inspection_in_progress",
        "high",
        ("axle", "suspension", "underside"),
    ),
    "20260328": c(
        "electrical_system",
        "pedal_box_wiring",
        "electrical_rework",
        "under_rework",
        "high",
        ("pedal_box", "wiring", "firewall"),
    ),
    "20260329": c(
        "body_exterior",
        "panel_detail_and_markings",
        "baseline_walkaround",
        "assembled",
        "medium",
        ("exterior", "detail"),
    ),
    "20260331": c(
        "chassis_underside",
        "frame_floor_underside_and_lines",
        "underside_inspection",
        "inspection_in_progress",
        "high",
        ("frame", "underside", "floor"),
    ),
    "20260401": c(
        "documentation_reference",
        "handwritten_notes",
        "reference_material",
        "reference_only",
        "high",
        ("notes", "reference"),
    ),
    "20260403": c(
        "procurement_inventory",
        "wiring_harness_and_fuse_distribution",
        "procurement_reconciliation",
        "bench_prep",
        "high",
        ("wiring", "fuse_box", "connectors", "package", "part_numbers"),
    ),
    "20260404": c(
        "procurement_inventory",
        "wiring_harness_and_fuse_distribution",
        "procurement_reconciliation",
        "bench_prep",
        "high",
        ("wiring", "fuse_box", "connectors", "package", "part_numbers"),
    ),
    "20260405": c(
        "chassis_underside",
        "frame_and_mount_points",
        "underside_inspection",
        "inspection_in_progress",
        "medium",
        ("frame", "mounts", "underside"),
    ),
    "20260406": c(
        "chassis_underside",
        "steering_and_suspension_linkages",
        "underside_inspection",
        "inspection_in_progress",
        "high",
        ("steering", "suspension", "underside"),
    ),
    "20260408": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "removed_parts_cataloguing",
        "removed_from_vehicle",
        "high",
        ("doors", "body_panels", "removed"),
    ),
    "20260410": c(
        "procurement_inventory",
        "wiring_harness_and_connectors",
        "procurement_reconciliation",
        "bench_prep",
        "high",
        ("wiring", "connectors", "loom", "package", "part_numbers"),
    ),
    "20260411": c(
        "procurement_inventory",
        "fuse_distribution_and_power_hardware",
        "procurement_reconciliation",
        "bench_prep",
        "high",
        ("fuse_box", "power_distribution", "electrical", "package", "part_numbers"),
    ),
    "20260412": c(
        "removable_panels",
        "refinished_hinges_brackets_and_trim",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("hardware", "refinish", "brackets"),
    ),
    "20260413": c(
        "body_floor",
        "floor_pan_rust_zones",
        "rust_assessment",
        "corrosion_visible",
        "high",
        ("floor_pan", "rust", "inspection"),
    ),
    "20260419": c(
        "body_exterior",
        "wing_removal_and_body_lift_prep",
        "stripdown_cataloguing",
        "components_removed_or_ready_for_lift",
        "medium",
        ("wing", "body_lift", "stripdown"),
    ),
    "20260420": c(
        "engine_bay",
        "engine_interior_and_stripdown_detail",
        "stripdown_cataloguing",
        "partially_disassembled",
        "medium",
        ("engine", "interior", "stripdown"),
    ),
    "20260421": c(
        "body_exterior",
        "wing_removal_and_body_lift_prep",
        "stripdown_cataloguing",
        "components_removed_or_ready_for_lift",
        "medium",
        ("body_lift", "body_shell", "stripdown"),
    ),
    "20260422": c(
        "chassis_underside",
        "frame_floor_underside_and_lines",
        "underside_inspection",
        "inspection_in_progress",
        "medium",
        ("body_off", "chassis", "frame", "inspection"),
    ),
    "other": c(
        "documentation_reference",
        "reference_media",
        "reference_material",
        "reference_only",
        "low",
        ("reference",),
    ),
}


FILE_OVERRIDES: dict[str, Classification] = {
    "20260317_165030.jpg": c(
        "body_exterior",
        "hood_and_front_windshield_overview",
        "baseline_walkaround",
        "assembled",
        "high",
        ("hood", "windshield", "wiper", "front_end"),
    ),
    "20260317_165203.jpg": c(
        "interior_cabin",
        "front_door_card",
        "baseline_walkaround",
        "assembled",
        "high",
        ("door_card", "interior"),
    ),
    "20260317_235150.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "stripdown_cataloguing",
        "partially_disassembled",
        "high",
        ("engine", "bay"),
    ),
    "20260317_235201.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "stripdown_cataloguing",
        "partially_disassembled",
        "high",
        ("engine", "bay"),
    ),
    "20260317_235216.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "stripdown_cataloguing",
        "partially_disassembled",
        "high",
        ("engine", "bay"),
    ),
    "20260317_235229.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "stripdown_cataloguing",
        "partially_disassembled",
        "high",
        ("engine", "bay"),
    ),
    "20260321_235501.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "stripdown_cataloguing",
        "partially_disassembled",
        "high",
        ("engine", "bay"),
    ),
    "20260321_235600.jpg": c(
        "interior_cabin",
        "driver_footwell_firewall_and_wiring",
        "stripdown_cataloguing",
        "trim_removed",
        "high",
        ("footwell", "firewall", "wiring"),
    ),
    "20260321_235605.jpg": c(
        "interior_cabin",
        "floor_pan_and_firewall",
        "stripdown_cataloguing",
        "trim_removed",
        "high",
        ("floor_pan", "firewall", "stripdown"),
    ),
    "20260323_185920.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "stripdown_cataloguing",
        "partially_disassembled",
        "high",
        ("engine", "bay"),
    ),
    "20260323_190005.jpg": c(
        "interior_cabin",
        "dashboard_lower_structure",
        "stripdown_cataloguing",
        "trim_removed",
        "high",
        ("dashboard", "stripdown"),
    ),
    "20260323_201950.jpg": c(
        "body_exterior",
        "body_shell_with_doors_removed",
        "removed_parts_cataloguing",
        "doors_removed",
        "high",
        ("body_shell", "doors_removed"),
    ),
    "20260323_201957.jpg": c(
        "body_exterior",
        "rear_side_opening",
        "removed_parts_cataloguing",
        "doors_removed",
        "high",
        ("body_shell", "rear_opening"),
    ),
    "20260323_202016.jpg": c(
        "body_floor",
        "rear_cargo_floor",
        "stripdown_cataloguing",
        "trim_removed",
        "high",
        ("cargo_floor", "interior"),
    ),
    "20260323_210944.jpg": c(
        "roof_and_gutters",
        "roof_gutter_and_window_channel",
        "rust_assessment",
        "corrosion_visible",
        "high",
        ("roof", "gutter", "rust"),
    ),
    "20260323_210954.jpg": c(
        "roof_and_gutters",
        "roof_gutter_and_window_channel",
        "rust_assessment",
        "corrosion_visible",
        "high",
        ("roof", "gutter", "rust"),
    ),
    "20260323_211003.jpg": c(
        "roof_and_gutters",
        "roof_gutter_and_window_channel",
        "rust_assessment",
        "corrosion_visible",
        "high",
        ("roof", "gutter", "rust"),
    ),
    "20260323_211027.jpg": c(
        "roof_and_gutters",
        "roof_gutter_and_window_channel",
        "rust_assessment",
        "corrosion_visible",
        "high",
        ("roof", "gutter", "rust"),
    ),
    "20260324_004812.jpg": c(
        "electrical_system",
        "driver_footwell_firewall_pass_through",
        "stripdown_cataloguing",
        "trim_removed",
        "high",
        ("firewall", "wiring", "front_cabin"),
    ),
    "20260324_004830.jpg": c(
        "wheels_and_tires",
        "wheel_and_tire_detail",
        "underside_inspection",
        "inspection_in_progress",
        "high",
        ("wheel", "tire"),
    ),
    "20260317_235152_gp_yJFNNGlA.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "baseline_walkaround",
        "assembled",
        "high",
        ("engine", "bay", "baseline"),
    ),
    "20260317_235204_gp_14hUn3XA.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "baseline_walkaround",
        "assembled",
        "high",
        ("engine", "bay", "baseline"),
    ),
    "20260317_235219_gp_rjDgGWZw.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "baseline_walkaround",
        "assembled",
        "high",
        ("engine", "bay", "baseline"),
    ),
    "20260317_235232_gp_3Ojs4Rag.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "baseline_walkaround",
        "assembled",
        "high",
        ("engine", "bay", "baseline"),
    ),
    "20260329_051754.jpg": c(
        "rubbers_and_seals",
        "window_rubber_seals_and_frames",
        "removed_parts_cataloguing",
        "removed_from_vehicle",
        "high",
        ("window", "rubber", "seal", "rear_hatch"),
    ),
    "20260329_095138.mp4": c(
        "documentation_reference",
        "off_vehicle_workstation_reference_video",
        "reference_material",
        "reference_only",
        "high",
        ("reference", "video"),
    ),
    "20260329_122723.jpg": c(
        "body_exterior",
        "exterior_badge_or_emblem_detail",
        "baseline_walkaround",
        "assembled",
        "high",
        ("badge", "emblem", "exterior"),
    ),
    "20260329_122855.jpg": c(
        "interior_cabin",
        "cabin_view_through_glass",
        "baseline_walkaround",
        "assembled",
        "high",
        ("interior", "window_view"),
    ),
    "20260403_202907.jpg": c(
        "documentation_reference",
        "electrical_reference_document",
        "reference_material",
        "reference_only",
        "high",
        ("electrical", "documentation"),
    ),
    "20260403_202920.jpg": c(
        "documentation_reference",
        "electrical_wiring_diagram",
        "reference_material",
        "reference_only",
        "high",
        ("electrical", "diagram"),
    ),
    "20260405_010322.jpg": c(
        "procurement_inventory",
        "fuse_distribution_and_wiring",
        "procurement_reconciliation",
        "bench_prep",
        "high",
        ("wiring", "fuse_box", "package", "part_numbers"),
    ),
    "20260405_234652.jpg": c(
        "body_floor",
        "floor_seam_and_body_mount_rust",
        "rust_assessment",
        "corrosion_visible",
        "high",
        ("floor", "seam", "rust"),
    ),
    "20260405_234541.jpg": c(
        "chassis_underside",
        "rear_frame_crossmember_and_mounts",
        "underside_inspection",
        "inspection_in_progress",
        "high",
        ("frame", "crossmember", "mounts"),
    ),
    "20260405_234546.jpg": c(
        "chassis_underside",
        "body_mount_and_crossmember_detail",
        "underside_inspection",
        "inspection_in_progress",
        "high",
        ("body_mount", "crossmember", "underside"),
    ),
    "20260405_234811.jpg": c(
        "chassis_underside",
        "rear_shock_and_crossmember_view",
        "underside_inspection",
        "inspection_in_progress",
        "high",
        ("shock", "crossmember", "underside"),
    ),
    "20260411_220207.jpg": c(
        "chassis_underside",
        "suspension_or_linkage_mount",
        "underside_inspection",
        "inspection_in_progress",
        "high",
        ("suspension", "underside"),
    ),
    "20260411_220214.jpg": c(
        "chassis_underside",
        "suspension_or_linkage_mount",
        "underside_inspection",
        "inspection_in_progress",
        "high",
        ("suspension", "underside"),
    ),
    "20260408_212832.jpg": c(
        "window_hardware",
        "rear_hatch_window_latch_mechanisms",
        "removed_parts_cataloguing",
        "removed_from_vehicle",
        "high",
        ("window", "latch", "mechanism", "rear_hatch"),
    ),
    "20260412_010623.jpg": c(
        "removable_panels",
        "refinished_seat_or_mount_bracket",
        "hardware_refinish",
        "refinished_off_vehicle",
        "medium",
        ("bracket", "hardware", "refinish"),
    ),
    "20260412_010713.jpg": c(
        "removable_panels",
        "wiper_arm_or_linkage_hardware",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("wiper", "hardware", "refinish"),
    ),
    "20260412_215136.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "stripdown_cataloguing",
        "partially_disassembled",
        "high",
        ("engine", "bay"),
    ),
    "20260412_215152.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "stripdown_cataloguing",
        "partially_disassembled",
        "high",
        ("engine", "bay"),
    ),
    "20260412_223216.jpg": c(
        "body_exterior",
        "front_panel_lighting_mount_area",
        "removed_parts_cataloguing",
        "panel_removed",
        "high",
        ("front_panel", "lighting", "removed"),
    ),
    "20260412_223534.jpg": c(
        "body_exterior",
        "front_panel_headlamp_surround",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("front_panel", "headlamp_surround", "refinish"),
    ),
    "20260412_223539.jpg": c(
        "body_exterior",
        "wing_mirror_set",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("wing_mirror", "mirror_housing", "refinish"),
    ),
    "20260413_040659.jpg": c(
        "body_floor",
        "rear_cargo_floor",
        "stripdown_cataloguing",
        "trim_removed",
        "high",
        ("cargo_floor", "stripdown"),
    ),
    "20260413_040719.jpg": c(
        "interior_cabin",
        "dashboard_shell_and_cabin",
        "stripdown_cataloguing",
        "trim_removed",
        "high",
        ("dashboard_shell", "stripdown"),
    ),
    "20260413_040739.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "stripdown_cataloguing",
        "partially_disassembled",
        "high",
        ("engine", "bay"),
    ),
    "20260420_201801_gp_NvXIaGBw.jpg": c(
        "procurement_inventory",
        "service_parts_and_order_confirmations",
        "procurement_reconciliation",
        "bench_prep",
        "high",
        ("service_parts", "filter", "package", "part_numbers", "order_confirmation"),
        "Received service part packaging confirmation (filter pack).",
    ),
    "20260420_201814_gp_IHb6FfXg.jpg": c(
        "procurement_inventory",
        "service_parts_and_order_confirmations",
        "procurement_reconciliation",
        "bench_prep",
        "high",
        ("service_parts", "thermostat", "package", "part_numbers", "order_confirmation"),
        "Received service part label confirmation (thermostat 90916-03118).",
    ),
    "20260420_221819_gp_YV69fbvA.jpg": c(
        "procurement_inventory",
        "hidden_diesel_cutoff_switch_hardware",
        "procurement_reconciliation",
        "bench_prep",
        "high",
        ("electrical", "switch", "hidden_diesel_cutoff", "package", "order_confirmation"),
        "Hidden diesel cutoff switch order part, received and awaiting installation.",
    ),
    "20260423_183408_gp_eCiJmZnA.jpg": c(
        "removable_panels",
        "detached_doors_and_panels",
        "removed_parts_cataloguing",
        "removed_from_vehicle",
        "high",
        ("body_panels", "removed", "storage"),
    ),
    "20260423_183448_gp_9MQfbmvQ.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "removed_parts_cataloguing",
        "removed_from_vehicle",
        "medium",
        ("body_panels", "removed", "storage"),
    ),
    "20260423_183514_gp_DyztXKcw.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "removed_parts_cataloguing",
        "removed_from_vehicle",
        "high",
        ("body_panels", "removed", "storage"),
    ),
    "20260423_183521_gp_pjVN2Ujw.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "removed_parts_cataloguing",
        "removed_from_vehicle",
        "high",
        ("body_panels", "removed", "storage"),
    ),
    "20260423_183540_gp_bhRdLpMg.jpg": c(
        "removable_panels",
        "detached_doors_and_panels",
        "removed_parts_cataloguing",
        "removed_from_vehicle",
        "medium",
        ("body_panels", "removed", "storage"),
    ),
    "20260423_183628_gp_SpWIfUnw.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "removed_parts_cataloguing",
        "removed_from_vehicle",
        "high",
        ("body_panels", "removed", "storage"),
    ),
    "20260423_183648_gp_ltd3AKwg.jpg": c(
        "roof_and_gutters",
        "roof_gutter_and_window_channel",
        "removed_parts_cataloguing",
        "removed_from_vehicle",
        "high",
        ("roof", "gutter", "panel_off_vehicle"),
    ),
    "20260423_183704_gp_a5qmyeOA.jpg": c(
        "body_floor",
        "floor_pan_rust_zones",
        "rust_assessment",
        "corrosion_visible",
        "high",
        ("floor_pan", "rust", "inspection"),
    ),
    "20260423_183712_gp_46OsAntA.jpg": c(
        "body_floor",
        "floor_pan_rust_zones",
        "rust_assessment",
        "corrosion_visible",
        "high",
        ("floor_pan", "rust", "inspection"),
    ),
    "20260421_192813_gp_0jvYAo8g.jpg": c(
        "interior_cabin",
        "dashboard_switch_and_control_hardware",
        "electrical_rework",
        "control_hardware_test_fit",
        "high",
        ("interior", "dash", "switch", "controls"),
    ),
    "20260421_194401_gp_1dY3fLdw.jpeg": c(
        "interior_cabin",
        "dashboard_switch_and_control_hardware",
        "electrical_rework",
        "control_hardware_test_fit",
        "high",
        ("interior", "dash", "switch", "controls"),
    ),
    "20260423_202614_gp_WU0G6duw.mp4": c(
        "documentation_reference",
        "off_vehicle_workstation_reference_video",
        "reference_material",
        "reference_only",
        "high",
        ("reference", "video", "non_car"),
    ),
    "20260423_232202_gp_ryYH6xZg.jpg": c(
        "chassis_underside",
        "frame_and_mount_points",
        "underside_inspection",
        "inspection_in_progress",
        "high",
        ("frame", "mounts", "underside"),
    ),
    "20260423_232220_gp_ezwEcH2g.jpg": c(
        "chassis_underside",
        "steering_and_suspension_linkages",
        "underside_inspection",
        "inspection_in_progress",
        "high",
        ("steering", "suspension", "underside"),
    ),
    "20260423_232236_gp_caYB252g.jpg": c(
        "chassis_underside",
        "steering_and_suspension_linkages",
        "underside_inspection",
        "inspection_in_progress",
        "high",
        ("steering", "suspension", "underside"),
    ),
    "20260423_232309_gp_rrFiL8og.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "stripdown_cataloguing",
        "partially_disassembled",
        "medium",
        ("engine", "bay", "inspection"),
    ),
    "20260423_232345_gp_jFn65JBQ.jpg": c(
        "chassis_underside",
        "frame_and_mount_points",
        "underside_inspection",
        "inspection_in_progress",
        "high",
        ("frame", "mounts", "underside"),
    ),
    "20260430_220004_gp_C9oYiYmA.jpg": c(
        "engine_bay",
        "cooling_hoses_fan_belt_and_radiator_support",
        "mechanical_inspection",
        "inspection_in_progress",
        "high",
        ("engine", "cooling", "radiator_hose", "fan_belt", "front_support", "inspection"),
        "Front engine bay inspection showing upper hose routing, hose clamps, fan belt, and radiator support area.",
    ),
    "20260430_215957_gp_2iBbUagw.jpg": c(
        "engine_bay",
        "cooling_hoses_fan_belt_and_radiator_support",
        "mechanical_inspection",
        "inspection_in_progress",
        "high",
        ("engine", "cooling", "radiator_hose", "fan_belt", "front_support", "inspection"),
        "Front engine bay inspection showing accessory belt path, hose routing, and radiator support condition.",
    ),
    "20260430_215939_gp_EjZ7u1ow.jpg": c(
        "engine_bay",
        "bellhousing_clutch_linkage_and_gearbox_case",
        "mechanical_inspection",
        "inspection_in_progress",
        "high",
        ("engine", "transmission", "bellhousing", "clutch_linkage", "wiring", "inspection"),
        "Close inspection of bellhousing/gearbox casing, linkage, and nearby wiring.",
    ),
    "20260430_215915_gp_ycQ395Gg.jpg": c(
        "engine_bay",
        "bellhousing_clutch_linkage_and_gearbox_case",
        "mechanical_inspection",
        "inspection_in_progress",
        "high",
        ("engine", "transmission", "bellhousing", "clutch_linkage", "inspection"),
        "Close inspection of gearbox/bellhousing casing and clutch linkage area.",
    ),
    "20260430_233755_gp_DO69MLAA.jpg": c(
        "engine_bay",
        "bellhousing_clutch_linkage_and_gearbox_case",
        "mechanical_inspection",
        "inspection_in_progress",
        "medium",
        ("engine", "transmission", "bellhousing", "clutch_linkage", "inspection"),
        "Additional detail view of gearbox/bellhousing casing and nearby linkage hardware.",
    ),
    "IMG-20260328-WA0017.jpeg": c(
        "removable_panels",
        "rear_hatch_inner_panel",
        "removed_parts_cataloguing",
        "removed_from_vehicle",
        "high",
        ("rear_hatch", "panel", "removed"),
    ),
    "IMG-20260331-WA0004.jpg": c(
        "engine_bay",
        "engine_bay_overview",
        "baseline_walkaround",
        "assembled",
        "high",
        ("engine", "bay"),
    ),
    "Screenshot_20260313_054936_PakWheels.jpg": c(
        "documentation_reference",
        "pakwheels_listing_screenshot",
        "reference_material",
        "reference_only",
        "high",
        ("listing", "screenshot", "reference"),
    ),
}


TIMESTAMP_RE = re.compile(r"^(?P<date>\d{8})_(?P<time>\d{6})")
IMG_DATE_RE = re.compile(r"^IMG-(?P<date>\d{8})-")
SCREENSHOT_DATE_RE = re.compile(r"^Screenshot_(?P<date>\d{8})_")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def detect_date_key(file_name: str) -> str:
    match = TIMESTAMP_RE.match(file_name)
    if match:
        return match.group("date")
    if IMG_DATE_RE.match(file_name):
        return IMG_DATE_RE.match(file_name).group("date")
    if SCREENSHOT_DATE_RE.match(file_name):
        return SCREENSHOT_DATE_RE.match(file_name).group("date")
    return "other"


def canonical_media_stem(file_name: str) -> str:
    stem = Path(file_name).stem
    stem = re.sub(r"_gp_[a-zA-Z0-9]+$", "", stem)
    stem = re.sub(r"_exported_\d+$", "", stem)
    return stem


def extract_captured_parts(file_name: str) -> tuple[str, str]:
    match = TIMESTAMP_RE.match(file_name)
    if match:
        date_raw = match.group("date")
        time_raw = match.group("time")
        captured_date = f"{date_raw[:4]}-{date_raw[4:6]}-{date_raw[6:]}"
        captured_time = f"{time_raw[:2]}:{time_raw[2:4]}:{time_raw[4:]}"
        return captured_date, captured_time

    for pattern in (IMG_DATE_RE, SCREENSHOT_DATE_RE):
        date_match = pattern.match(file_name)
        if date_match:
            date_raw = date_match.group("date")
            captured_date = f"{date_raw[:4]}-{date_raw[4:6]}-{date_raw[6:]}"
            return captured_date, ""

    return "", ""


def classify_file(file_name: str) -> Classification:
    if file_name in FILE_OVERRIDES:
        return FILE_OVERRIDES[file_name]

    canonical_stem = canonical_media_stem(file_name)
    canonical_matches = [
        classification
        for override_name, classification in FILE_OVERRIDES.items()
        if canonical_media_stem(override_name) == canonical_stem
    ]
    if canonical_matches:
        return canonical_matches[0]

    date_key = detect_date_key(file_name)
    if date_key in DATE_DEFAULTS:
        return DATE_DEFAULTS[date_key]

    return DATE_DEFAULTS["other"]


def clean_generated_index() -> None:
    if INDEX_DIR.exists():
        shutil.rmtree(INDEX_DIR)
    (INDEX_DIR / "by_component_group").mkdir(parents=True, exist_ok=True)
    (INDEX_DIR / "by_specific_component").mkdir(parents=True, exist_ok=True)
    (INDEX_DIR / "by_stage").mkdir(parents=True, exist_ok=True)


def build_photo_inventory() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for path in sorted(PHOTOS_DIR.iterdir(), key=lambda item: item.name.lower()):
        if not path.is_file():
            continue
        extension = path.suffix.lower()
        if extension not in SUPPORTED_EXTENSIONS:
            continue

        classification = classify_file(path.name)
        captured_date, captured_time = extract_captured_parts(path.name)

        row = {
            "media_id": path.stem,
            "file_name": path.name,
            "relative_path": f"photos/{path.name}",
            "captured_date": captured_date,
            "captured_time": captured_time,
            "media_type": "video" if extension in {".mp4", ".mov", ".avi", ".mkv"} else "photo",
            "component_group": classification.component_group,
            "specific_component": classification.specific_component,
            "stage": classification.stage,
            "observed_state": classification.observed_state,
            "confidence": classification.confidence,
            "tags": "|".join(classification.tags),
            "notes": classification.notes,
        }
        rows.append(row)

    return rows


def write_inventory_csv(rows: list[dict[str, str]]) -> None:
    MANUAL_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "media_id",
        "file_name",
        "relative_path",
        "captured_date",
        "captured_time",
        "media_type",
        "component_group",
        "specific_component",
        "stage",
        "observed_state",
        "confidence",
        "tags",
        "notes",
    ]
    with PHOTO_INVENTORY_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_component_summary(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    buckets: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (row["component_group"], row["specific_component"])
        buckets[key].append(row)

    summary_rows: list[dict[str, str]] = []
    for (component_group, specific_component), group_rows in sorted(buckets.items()):
        stages = sorted({row["stage"] for row in group_rows})
        dates = sorted({row["captured_date"] for row in group_rows if row["captured_date"]})
        date_range = ""
        if dates:
            date_range = dates[0] if len(dates) == 1 else f"{dates[0]} to {dates[-1]}"
        summary_rows.append(
            {
                "component_group": component_group,
                "specific_component": specific_component,
                "file_count": str(len(group_rows)),
                "stages_seen": "|".join(stages),
                "date_range": date_range,
                "example_file": group_rows[0]["file_name"],
            }
        )

    with PHOTO_SUMMARY_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "component_group",
                "specific_component",
                "file_count",
                "stages_seen",
                "date_range",
                "example_file",
            ],
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    return summary_rows


def write_lookup_symlinks(rows: list[dict[str, str]]) -> None:
    clean_generated_index()

    for row in rows:
        source = ROOT / row["relative_path"]
        if not source.exists():
            continue

        destinations = [
            INDEX_DIR / "by_component_group" / slugify(row["component_group"]) / row["file_name"],
            INDEX_DIR / "by_specific_component" / slugify(row["specific_component"]) / row["file_name"],
            INDEX_DIR / "by_stage" / slugify(row["stage"]) / row["file_name"],
        ]

        for link_path in destinations:
            link_path.parent.mkdir(parents=True, exist_ok=True)
            if link_path.exists() or link_path.is_symlink():
                link_path.unlink()
            relative_target = os.path.relpath(source, start=link_path.parent)
            link_path.symlink_to(relative_target)


def write_catalog_markdown(rows: list[dict[str, str]], summary_rows: list[dict[str, str]]) -> None:
    total_files = len(rows)
    total_photos = sum(1 for row in rows if row["media_type"] == "photo")
    total_videos = sum(1 for row in rows if row["media_type"] == "video")

    rows_by_stage: dict[str, int] = defaultdict(int)
    for row in rows:
        rows_by_stage[row["stage"]] += 1

    lines: list[str] = []
    lines.append("# Photo Catalog and Component Inventory")
    lines.append("")
    lines.append(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Total media files indexed: {total_files} ({total_photos} photos, {total_videos} videos)")
    lines.append("- Inventory CSV: `data/manual/photo_inventory.csv`")
    lines.append("- Component summary CSV: `data/manual/photo_component_summary.csv`")
    lines.append("")
    lines.append("## Quick Lookup")
    lines.append("")
    lines.append("- By component group: `photos/index/by_component_group/`")
    lines.append("- By specific component: `photos/index/by_specific_component/`")
    lines.append("- By stage: `photos/index/by_stage/`")
    lines.append("")
    lines.append("## Stage Distribution")
    lines.append("")
    lines.append("| Stage | File Count |")
    lines.append("| --- | ---: |")
    for stage, count in sorted(rows_by_stage.items()):
        lines.append(f"| `{stage}` | {count} |")
    lines.append("")
    lines.append("## Component Summary")
    lines.append("")
    lines.append("| Component Group | Specific Component | Files | Date Range | Example |")
    lines.append("| --- | --- | ---: | --- | --- |")
    for row in summary_rows:
        lines.append(
            f"| `{row['component_group']}` | `{row['specific_component']}` | {row['file_count']} | "
            f"{row['date_range'] or '-'} | `{row['example_file']}` |"
        )

    CATALOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_photo_inventory()
    if not rows:
        raise SystemExit("No supported media files found in photos/.")

    write_inventory_csv(rows)
    summary_rows = write_component_summary(rows)
    write_lookup_symlinks(rows)
    write_catalog_markdown(rows, summary_rows)

    print(f"Wrote inventory: {PHOTO_INVENTORY_PATH.relative_to(ROOT)}")
    print(f"Wrote summary: {PHOTO_SUMMARY_PATH.relative_to(ROOT)}")
    print(f"Wrote catalog: {CATALOG_PATH.relative_to(ROOT)}")
    print(f"Built lookup folders: {INDEX_DIR.relative_to(ROOT)}")
    print(f"Indexed files: {len(rows)}")


if __name__ == "__main__":
    main()
