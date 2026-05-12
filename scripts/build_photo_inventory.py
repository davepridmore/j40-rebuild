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
        "body_floor",
        "body_off_shell_floor_and_bulkhead",
        "rust_assessment",
        "corrosion_visible",
        "medium",
        ("body_off", "body_shell", "floor_pan", "bulkhead", "inspection"),
        "Body-off shell/floor photos from this date are not chassis evidence unless explicitly overridden.",
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
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("window", "latch", "mechanism", "rear_hatch", "refinished", "post_paint"),
        "Post-paint returned rear hatch/window hardware detail.",
    ),
    "20260408_211754.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("doors", "body_panels", "refinished", "post_paint"),
        "Post-paint returned panel/door set.",
    ),
    "20260408_211756_gp_UFEU6uIA.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("doors", "body_panels", "refinished", "post_paint"),
        "Post-paint returned panel/door set.",
    ),
    "20260408_211804.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("doors", "body_panels", "refinished", "post_paint"),
        "Post-paint returned panel/door set.",
    ),
    "20260408_211806_gp_TbbCJsoQ.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("doors", "body_panels", "refinished", "post_paint"),
        "Post-paint returned panel/door set.",
    ),
    "20260408_211812.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("doors", "body_panels", "refinished", "post_paint"),
        "Post-paint returned panel/door set.",
    ),
    "20260408_211814_gp_hJ3szRKQ.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("doors", "body_panels", "refinished", "post_paint"),
        "Post-paint returned panel/door set.",
    ),
    "20260408_212835_gp_nwY1TOwQ.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("doors", "body_panels", "refinished", "post_paint"),
        "Post-paint returned panel/door set.",
    ),
    "20260408_212839.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("doors", "body_panels", "refinished", "post_paint"),
        "Post-paint returned panel/door set.",
    ),
    "20260408_212841_gp_y9GxLOZg.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("doors", "body_panels", "refinished", "post_paint"),
        "Post-paint returned panel/door set.",
    ),
    "20260408_212846.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("doors", "body_panels", "refinished", "post_paint"),
        "Post-paint returned panel/door set.",
    ),
    "20260408_212849_gp_VJjse8gw.jpg": c(
        "removable_panels",
        "detached_body_panels_and_doors",
        "hardware_refinish",
        "refinished_off_vehicle",
        "high",
        ("doors", "body_panels", "refinished", "post_paint"),
        "Post-paint returned panel/door set.",
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


CHASSIS_20260422_OVERRIDES: dict[str, Classification] = {
    "20260422_004241_gp_hASLbowg.jpg": c(
        "chassis_underside",
        "full_chassis_frame_overview",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "frame", "overview"),
        "Full-length body-off chassis/frame overview.",
    ),
    "20260422_004254_gp_SplHLSYA.jpg": c(
        "chassis_underside",
        "rear_axle_spring_hanger_and_crossmember",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "rear_axle", "spring_hanger", "crossmember"),
        "Close-up of rear frame, axle, spring hanger, and crossmember area.",
    ),
    "20260422_004257_gp_cxEZbZoQ.jpg": c(
        "chassis_underside",
        "rear_axle_spring_hanger_and_crossmember",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "rear_axle", "spring_hanger", "crossmember"),
        "Rear chassis detail with axle, spring hanger, and crossmember visible.",
    ),
    "20260422_004301_gp_SU89hisw.jpg": c(
        "chassis_underside",
        "rear_axle_spring_hanger_and_crossmember",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "rear_axle", "leaf_spring", "crossmember"),
        "Rear axle and chassis rail/crossmember close-up.",
    ),
    "20260422_004306_gp_vGlNr2UA.jpg": c(
        "chassis_underside",
        "frame_rail_body_mount_and_hard_line_detail",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "frame_rail", "body_mount", "hard_lines"),
        "Frame rail, body mount, and hard-line routing detail.",
    ),
    "20260422_004311_gp_994KQ0Pw.jpg": c(
        "chassis_underside",
        "frame_rail_body_mount_and_hard_line_detail",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "frame_rail", "body_mount", "hard_lines"),
        "Close-up of chassis rail and nearby hard-line/bracket routing.",
    ),
    "20260422_004319_gp_Ttqz46Sw.jpg": c(
        "chassis_underside",
        "transmission_crossmember_and_driveline_mounts",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "transmission_crossmember", "driveline_mounts"),
        "Driveline and transmission-crossmember interface on exposed chassis.",
    ),
    "20260422_004323_gp_JD88KuWQ.jpg": c(
        "chassis_underside",
        "frame_rail_body_mount_and_hard_line_detail",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "frame_rail", "body_mount", "crossmember"),
        "Frame rail and body-mount pedestal close-up.",
    ),
    "20260422_004332_gp_7d5uYWQQ.jpg": c(
        "chassis_underside",
        "frame_rail_body_mount_and_hard_line_detail",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "frame_rail", "body_mount", "crossmember"),
        "Central frame rail and mount/crossmember detail.",
    ),
    "20260422_004338_gp_35uwfApA.jpg": c(
        "chassis_underside",
        "transmission_crossmember_and_driveline_mounts",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "transmission", "crossmember", "mounts"),
        "Transmission and chassis crossmember area with body removed.",
    ),
    "20260422_004347_gp_WIy0j6zw.jpg": c(
        "chassis_underside",
        "engine_bay_chassis_interface",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "front_frame", "engine_mount_area", "hard_lines"),
        "Front chassis and engine-bay frame interface detail.",
    ),
    "20260422_004356_gp_vTFgPfAQ.jpg": c(
        "chassis_underside",
        "engine_bay_chassis_interface",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "front_frame", "engine_mount_area", "hard_lines"),
        "Front frame/engine interface detail with body removed.",
    ),
    "20260422_004412_gp_OclpaTdg.jpg": c(
        "chassis_underside",
        "engine_bay_chassis_interface",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "front_frame", "engine_mount_area", "steering"),
        "Wide front chassis and engine-interface view.",
    ),
    "20260422_004423_gp_B1N5ThVw.jpg": c(
        "chassis_underside",
        "front_frame_horns_bumper_and_radiator_support",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "front_frame_horns", "bumper", "radiator_support"),
        "Front frame horns and bumper/radiator-support area.",
    ),
    "20260422_004429_gp_4emWbTrA.jpg": c(
        "chassis_underside",
        "front_frame_horns_bumper_and_radiator_support",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "front_frame_horns", "bumper", "radiator_support"),
        "Front chassis overview from bumper/frame-horn end.",
    ),
    "20260422_004436_gp_yjCPMWTg.jpg": c(
        "chassis_underside",
        "front_frame_horns_bumper_and_radiator_support",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "front_frame_horns", "bumper", "front_crossmember"),
        "Front bumper, frame horns, and front crossmember detail.",
    ),
    "20260422_054711_gp_V1EgU9oQ.jpg": c(
        "chassis_underside",
        "full_chassis_frame_overview",
        "underside_inspection",
        "body_removed_for_chassis_access",
        "high",
        ("body_off", "chassis", "frame", "overview"),
        "Full-length chassis overview after body removal.",
    ),
}

CHASSIS_20260501_ENGINE_CLEANING_FILES = (
    "20260501_194535_gp_mZ25Ou4A.jpg",
    "20260501_194508_gp_aSPxPLDw.jpg",
    "20260501_194458_gp_wd1x56gQ.jpg",
    "20260501_194451_gp_gDugUCjQ.jpg",
    "20260501_194435_gp_ewUJAfPA.jpg",
    "20260501_194427_gp_QjfOBtTQ.jpg",
    "20260501_194421_gp_toAeFYqg.jpg",
    "20260501_194414_gp_gdDllc8Q.jpg",
    "20260501_194402_gp_W9J4rcsw.jpg",
    "20260501_194344_gp_V7P0qatA.jpg",
    "20260501_194338_gp_81Nj4SVA.jpg",
    "20260501_194330_gp_CogcrEXA.jpg",
    "20260501_220352_gp_ZpTWaO5Q.jpg",
    "20260501_215603_gp_p8KX4pAw.jpg",
)

CHASSIS_20260501_REAR_AXLE_FILES = (
    "20260501_194322_gp_XuRtjN4w.jpg",
    "20260501_194313_gp_lfUqLibA.jpg",
    "20260501_194305_gp_EllBGvXA.jpg",
)

CHASSIS_20260501_REAR_MID_FRAME_FILES = (
    "20260501_194203_gp_9nXwy2XQ.jpg",
    "20260501_194151_gp_NqgqjDEQ.jpg",
    "20260501_194144_gp_P5PojIhw.jpg",
    "20260501_194137_gp_S1qvWECw.jpg",
    "20260501_194106_gp_e4CETkdg.jpg",
    "20260501_194101_gp_3xKjQSsQ.jpg",
    "20260501_194056_gp_p1erpz8w.jpg",
    "20260501_194041_gp_6zRIFJUw.jpg",
    "20260501_194026_gp_gjPjhxdA.jpg",
)

CHASSIS_20260501_FRONT_FRAME_FILES = (
    "20260501_194014_gp_nWBXweFA.jpg",
    "20260501_194006_gp_AU1Lw9GQ.jpg",
    "20260501_193958_gp_yhnX0HAQ.jpg",
    "20260501_193953_gp_XQtysikA.jpg",
    "20260501_193944_gp_smzZc4nw.jpg",
    "20260501_193935_gp_FPwZZHZA.jpg",
    "20260501_193924_gp_KK717O7g.jpg",
    "20260501_193915_gp_lII00tCA.jpg",
    "20260501_193904_gp_GgWYRulA.jpg",
    "20260501_193856_gp_M78kWBlQ.jpg",
    "20260501_193847_gp_uHWO7Bdw.jpg",
    "20260501_193841_gp_ZwpHFiMA.jpg",
)

CHASSIS_20260501_BODY_MOUNT_RAIL_FILES = (
    "20260501_193833_gp_Slpuijyg.jpg",
    "20260501_193826_gp_Qhz88J4g.jpg",
    "20260501_193811_gp_uv8kwbxw.jpg",
    "20260501_193805_gp_VgTc8wYQ.jpg",
    "20260501_193624_gp_ocLE7cMQ.jpg",
    "20260501_193755_gp_cuaY6sgg.jpg",
    "20260501_193618_gp_EFciJdww.jpg",
    "20260501_193609_gp_f5PDj87Q.jpg",
    "20260501_193554_gp_EU4bmOlg.jpg",
    "20260501_193603_gp_9zd2mD6w.jpg",
    "20260501_193542_gp_U7e0J0iA.jpg",
    "20260501_193533_gp_sDErdvGw.jpg",
)

RUBBER_RECREATION_20260502_FILES = (
    "20260502_004201_gp_zfUSmKJg.jpg",
    "20260502_004215_gp_evgCLjSw.jpg",
    "20260502_004222_gp_PKRe5HSQ.jpg",
    "20260502_004231_gp_CfosvPIg.jpg",
    "20260502_004254_gp_Hm9RR5DQ.jpg",
    "20260502_004314_gp_wuzpgNrA.jpg",
    "20260502_004337_gp_m2OagYpg.jpg",
    "20260502_004345_gp_yK8VYzMQ.jpg",
    "20260502_004401_gp_otUSjgGA.jpg",
    "20260502_004413_gp_Qno8OVRg.jpg",
    "20260502_004419_gp_ZPXJRBzg.jpg",
    "20260502_004429_gp_KJHxGcCA.jpg",
    "20260502_004437_gp_f1TySzww.jpg",
    "20260502_004442_gp_7WcFHjLQ.jpg",
)

PIPE_FABRICATION_20260502_FILES = (
    "20260502_004044_gp_Hx4Yo0Qg.jpg",
    "20260502_004106_gp_wlYlUahA.jpg",
    "20260502_004120_gp_7Jw9Zyrg.jpg",
    "20260502_004133_gp_ZEpqmARA.jpg",
    "20260502_004139_gp_jt1dGw4A.jpg",
    "20260502_004145_gp_e8soxsyA.jpg",
)

PIPE_SAMPLE_SORTING_20260502_FILES = (
    "20260502_005740_gp_Qiat03EQ.jpg",
)

PIPE_SAMPLE_SORTING_20260502_LENGTH_FILES = (
    "20260502_160754_gp_Zd9UeENg.jpg",
    "20260502_160855_gp_w3sghS8Q.jpg",
    "20260502_160929_gp_exms2QzQ.jpg",
    "20260502_160950_gp_5KW8RnDQ.jpg",
    "20260502_161055_gp_lS8VRrWg.jpg",
    "20260502_161214_gp_zc3zwXlg.jpg",
)

CHASSIS_20260501_OVERRIDES: dict[str, Classification] = {
    **{
        file_name: c(
            "engine_bay",
            "engine_powertrain_cleaning_baseline",
            "mechanical_cleaning",
            "dirty_cleaning_required",
            "high",
            ("body_off", "engine", "transmission", "cleaning", "pressure_sprayer_plan"),
            "May 1 body-off engine/powertrain baseline before degreaser, controlled pressure cleaning, leak check, and service inspection.",
        )
        for file_name in CHASSIS_20260501_ENGINE_CLEANING_FILES
    },
    **{
        file_name: c(
            "chassis_underside",
            "rear_axle_spring_hanger_and_crossmember",
            "chassis_fixing",
            "wire_brushed_partial_cleaning_in_progress",
            "high",
            ("body_off", "chassis", "rear_axle", "leaf_spring", "wire_brushed", "rust_prep"),
            "May 1 status photo after wire brushing; rear axle, spring hanger, and crossmember detail still need edge and bracket cleanup before coating.",
        )
        for file_name in CHASSIS_20260501_REAR_AXLE_FILES
    },
    **{
        file_name: c(
            "chassis_underside",
            "rear_mid_frame_rail_and_hard_line_detail",
            "chassis_fixing",
            "wire_brushed_partial_cleaning_in_progress",
            "high",
            ("body_off", "chassis", "frame_rail", "hard_lines", "crossmember", "wire_brushed", "rust_prep"),
            "May 1 status photo after wire brushing; rear/mid rail flats are partly cleaned but edges, weld toes, holes, and hard-line brackets remain inspection priorities.",
        )
        for file_name in CHASSIS_20260501_REAR_MID_FRAME_FILES
    },
    **{
        file_name: c(
            "chassis_underside",
            "front_frame_horns_bumper_and_steering_area",
            "chassis_fixing",
            "wire_brushed_partial_cleaning_in_progress",
            "high",
            ("body_off", "chassis", "front_frame_horns", "bumper", "steering", "wire_brushed", "rust_prep"),
            "May 1 status photo after wire brushing; front horns, steering area, bumper/winch brackets, and crossmember junctions need final detail cleanup and inspection.",
        )
        for file_name in CHASSIS_20260501_FRONT_FRAME_FILES
    },
    **{
        file_name: c(
            "chassis_underside",
            "frame_rail_body_mount_and_crossmember_detail",
            "chassis_fixing",
            "wire_brushed_partial_cleaning_in_progress",
            "high",
            ("body_off", "chassis", "frame_rail", "body_mount", "crossmember", "wire_brushed", "rust_prep"),
            "May 1 status photo after wire brushing; outer rail faces are mostly exposed, with remaining rust/dust concentrated at top flanges, lower edges, brackets, and body-mount pads.",
        )
        for file_name in CHASSIS_20260501_BODY_MOUNT_RAIL_FILES
    },
}

FILE_OVERRIDES.update(CHASSIS_20260422_OVERRIDES)
FILE_OVERRIDES.update(CHASSIS_20260501_OVERRIDES)
FILE_OVERRIDES.update(
    {
        "20260503_153832_gp_0FJJiLHg.jpg": c(
            "procurement_inventory",
            "mixed_fastener_hardware",
            "procurement_reconciliation",
            "fastener_sorting",
            "high",
            (
                "screws",
                "bolts",
                "washers",
                "clip_nuts",
                "self_tapping",
                "trim_screws",
                "retaining_clips",
                "cotter_pins",
                "rubber_bumpers",
                "isolators",
                "shoulder_pins",
                "brackets",
                "body_hardware",
                "sample_sorting",
            ),
            "User-selected May 3 loose screw/fastener pile; use to separate Millat-covered metric screws from missing self-tapping/trim screw, captive/clip-nut, retaining-clip, rubber/plastic isolator, shoulder-pin, sleeve/spacer, and bracket/retainer hardware.",
        ),
        "20260503_234035_front_vent_window_assemblies.png": c(
            "windows",
            "front_vent_window_assemblies",
            "removed_parts_cataloguing",
            "removed_from_vehicle_needs_refurbish",
            "high",
            ("window", "vent_window", "quarter_window", "glass", "rubber", "seal", "rust", "refurbish", "wp02"),
            "User-provided May 3 photo of paired off-vehicle vent/quarter window assemblies; old seals and rusted brackets/channels need teardown inspection before any replacement buy.",
        )
    }
)
FILE_OVERRIDES.update(
    {
        file_name: c(
            "procurement_inventory",
            "rubber_parts_recreation_samples",
            "procurement_reconciliation",
            "candidate_selection",
            "high",
            ("rubber", "body_mount", "sample", "sleeve", "shim", "recreation", "fabrication"),
            "May 2 starter collection for recreating body-mount/front-support rubber parts; user-selected candidate photo pending final selection and measurement tagging.",
        )
        for file_name in RUBBER_RECREATION_20260502_FILES
    }
)
FILE_OVERRIDES.update(
    {
        file_name: c(
            "engine_bay",
            "cooling_pipe_fabrication_samples",
            "mechanical_baseline",
            "fabrication_spec_capture",
            "high",
            ("cooling", "pipe", "radiator_hose", "metal_pipe", "sample", "fabrication", "made_to_order", "measurement"),
            "May 2 selected pipe fabrication sample set; use for made-to-order cooling/engine pipe spec with physical measurement hold points.",
        )
        for file_name in PIPE_FABRICATION_20260502_FILES
    }
)
FILE_OVERRIDES.update(
    {
        file_name: c(
            "engine_bay",
            "replacement_pipe_hose_sample_sorting",
            "mechanical_baseline",
            "sample_sorting_for_acquisition",
            "high",
            ("pipe", "hose", "sample", "replacement_pipe", "acquisition", "fabrication", "measurement"),
            "May 2 additional loose pipe/hose sample photo for replacement-pipes sorting; use only with physical measurement and installed-location assignment.",
        )
        for file_name in PIPE_SAMPLE_SORTING_20260502_FILES
    }
)
FILE_OVERRIDES.update(
    {
        file_name: c(
            "engine_bay",
            "replacement_pipe_hose_sample_sorting",
            "mechanical_baseline",
            "sample_length_and_route_identification",
            "high",
            ("pipe", "hose", "sample", "replacement_pipe", "sample_sorting", "measurement", "length", "rating_check"),
            "May 2 loose red/black pipe-hose sample length set; attach to replacement-pipes intake but keep release held until vehicle placement, ID/OD, and rating markings are confirmed.",
        )
        for file_name in PIPE_SAMPLE_SORTING_20260502_LENGTH_FILES
    }
)
FILE_OVERRIDES.update(
    {
        "20260422_003700_gp_gFb0LBcw.jpg": c(
            "procurement_inventory",
            "rust_remover_container",
            "procurement_reconciliation",
            "received_or_on_hand",
            "high",
            ("rust_remover", "container", "inventory"),
            "Product/container photo; not chassis evidence.",
        ),
        "20260422_015512_gp_BmYsVZ6w.jpg": c(
            "documentation_reference",
            "aftermarket_chassis_reference_image",
            "reference_material",
            "reference_only",
            "high",
            ("reference", "aftermarket", "chassis"),
            "Reference image only; not current-vehicle chassis evidence.",
        ),
        "20260422_034358_gp_Bg6nSlPw.jpg": c(
            "procurement_inventory",
            "rubber_grommet_assortment",
            "procurement_reconciliation",
            "received_item_evidence",
            "high",
            ("rubber", "grommet", "inventory", "received"),
            "User correction 2026-05-01: use as actual grommet assortment photo evidence, not a disputed placeholder.",
        ),
        "20260422_074709_gp_o4wiXyjA.jpg": c(
            "interior_cabin",
            "dashboard_shell_and_bulkhead",
            "stripdown_cataloguing",
            "body_removed_for_chassis_access",
            "high",
            ("dashboard", "bulkhead", "cabin", "body_off"),
            "Interior/dashboard shell view; not chassis evidence.",
        ),
    }
)

FILE_OVERRIDES.update(
    {
        "20260512_072723_gp_r9KEkOdg.jpg": c(
            "chassis_underside",
            "rear_axle_and_leaf_springs",
            "steering_brakes_suspension",
            "rear_brake_axle_baseline",
            "high",
            (
                "rear_axle",
                "rear_brake",
                "drum",
                "parking_brake",
                "brake_line",
                "leaf_spring",
                "u_bolt",
            ),
            "Google Photos May 12 rear wheel/drum close-up; useful for rear brake, parking-brake lever/cable, axle tube, U-bolt, and leaf-spring baseline before brake and suspension work.",
        ),
        "20260512_072730_gp_jSK3r3bg.jpg": c(
            "chassis_underside",
            "rear_axle_and_leaf_springs",
            "steering_brakes_suspension",
            "rear_axle_spring_baseline",
            "high",
            (
                "rear_axle",
                "leaf_spring",
                "u_bolt",
                "brake_line",
                "parking_brake_cable",
                "spring_plate",
            ),
            "Google Photos May 12 rear axle/leaf-spring view showing spring plate, U-bolts, axle tube, and adjacent brake/parking-brake routing.",
        ),
        "20260512_072742_gp_uSvGBUiA.jpg": c(
            "chassis_underside",
            "rear_axle_and_leaf_springs",
            "steering_brakes_suspension",
            "rear_axle_spring_brake_baseline",
            "high",
            (
                "rear_axle",
                "rear_brake",
                "drum",
                "leaf_spring",
                "brake_line",
                "shock_mount",
                "spring_hanger",
            ),
            "Google Photos May 12 rear axle/drum area with brake line/cable context and nearby spring or shock mount hardware.",
        ),
        "20260512_072755_gp_qXTHC8hw.jpg": c(
            "chassis_underside",
            "rear_axle_spring_hanger_and_crossmember",
            "steering_brakes_suspension",
            "rear_frame_spring_mount_baseline",
            "medium",
            (
                "rear_frame",
                "spring_hanger",
                "crossmember",
                "rear_axle",
                "brake_line",
                "body_off",
            ),
            "Google Photos May 12 rear frame/spring-mount context; supports spring hanger and nearby line-routing checks but still needs closer ruler photos before any bracket release.",
        ),
        "20260512_072812_gp_gZLxKAXA.jpg": c(
            "engine_bay",
            "engine_powertrain_cleaning_baseline",
            "mechanical_baseline",
            "pre_cleaning_baseline",
            "high",
            (
                "gearbox",
                "transmission",
                "powertrain",
                "chassis_rail",
                "linkage",
                "leak_check",
            ),
            "Google Photos May 12 gearbox/powertrain underside view for cleaning baseline and later leak-source inspection.",
        ),
        "20260512_072817_gp_MkI6uZkA.jpg": c(
            "engine_bay",
            "engine_powertrain_cleaning_baseline",
            "mechanical_baseline",
            "pre_cleaning_baseline",
            "high",
            (
                "gearbox",
                "transfer_case",
                "powertrain",
                "hard_lines",
                "chassis_rail",
                "leak_check",
            ),
            "Google Photos May 12 transmission/transfer and chassis-rail underside view, adding context for cleaning, line routing, and leak tracing.",
        ),
        "20260512_072828_gp_B7rDniBw.jpg": c(
            "chassis_underside",
            "front_frame_horns_bumper_and_steering_area",
            "chassis_fixing",
            "front_frame_steering_baseline",
            "high",
            (
                "front_frame",
                "steering_box",
                "steering_linkage",
                "hard_lines",
                "engine_bay",
                "bracket_scouting",
            ),
            "Google Photos May 12 front frame/steering-side engine-bay view; supports steering-box mount, hard-line routing, and front bracket scouting.",
        ),
        "20260512_072913_gp_g3iLrvfw.jpg": c(
            "chassis_underside",
            "steering_and_suspension_linkages",
            "steering_brakes_suspension",
            "front_linkage_brake_baseline",
            "high",
            (
                "front_axle",
                "steering_linkage",
                "tie_rod",
                "brake_hose",
                "brake_line",
                "front_brake",
            ),
            "Google Photos May 12 front wheel-side linkage/brake view showing steering arm/tie rod context and brake hose/line routing.",
        ),
        "20260512_072929_gp_bpHkNO2Q.jpg": c(
            "chassis_underside",
            "rear_axle_and_leaf_springs",
            "steering_brakes_suspension",
            "rear_axle_line_baseline",
            "high",
            (
                "rear_axle",
                "differential",
                "brake_line",
                "line_bracket",
                "leaf_spring",
                "u_bolt",
            ),
            "Google Photos May 12 rear axle/differential and line-bracket close-up for rear brake-line routing and rear suspension baseline.",
        ),
        "20260512_072947_gp_bNB9GvHA.jpg": c(
            "chassis_underside",
            "rear_axle_and_leaf_springs",
            "steering_brakes_suspension",
            "rear_brake_line_baseline",
            "high",
            (
                "rear_axle",
                "rear_brake",
                "drum",
                "backing_plate",
                "brake_hose",
                "brake_line",
                "line_bracket",
            ),
            "Google Photos May 12 rear drum/backing-plate area with hose/line routing visible; useful for rear brake baseline and hard-line refresh planning.",
        ),
        "20260512_073141_gp_xzy6KAzg.jpg": c(
            "interior_cabin",
            "floor_pan_rust_zones",
            "stripdown_cataloguing",
            "rust_repair_assessment",
            "high",
            (
                "floor_pan",
                "firewall",
                "rust",
                "pedal_area",
                "body_mount",
                "stripdown",
            ),
            "Google Photos May 12 stripped floor/firewall-side rust view with exposed holes, pedal/linkage area, and heavy surface corrosion; use for floor repair assessment, not chassis bracket release.",
        ),
        "20260512_073204_gp_sNfDSHdg.jpg": c(
            "engine_bay",
            "engine_powertrain_cleaning_baseline",
            "mechanical_baseline",
            "pre_cleaning_baseline",
            "high",
            (
                "engine",
                "injection_pump",
                "front_support",
                "cooling_hose",
                "powertrain",
                "leak_check",
            ),
            "Google Photos May 12 engine-side view around injection/ancillary hardware and front-support context for cleaning and hose routing baseline.",
        ),
        "20260512_073210_gp_zP427O2A.jpg": c(
            "engine_bay",
            "front_support_radiator_pickups_context",
            "chassis_fixing",
            "radiator_bracket_design_scouting",
            "high",
            (
                "front_support",
                "radiator",
                "radiator_mount",
                "front_crossmember",
                "pickup_holes",
                "bracket_scouting",
            ),
            "Google Photos May 12 front support and radiator pickup-area view; adds hole-field and support-face context for two-side radiator retention planning.",
        ),
        "20260512_073303_gp_hNyAiN1g.jpg": c(
            "chassis_underside",
            "front_frame_horns_bumper_and_radiator_support",
            "chassis_fixing",
            "front_support_radiator_baseline",
            "high",
            (
                "front_frame",
                "front_support",
                "radiator",
                "radiator_mount",
                "front_crossmember",
                "bracket_scouting",
            ),
            "Google Photos May 12 front frame/front-support view with radiator-support hole field and fan/pulley packaging context.",
        ),
        "20260512_073314_gp_GyAXZWBg.jpg": c(
            "engine_bay",
            "cooling_hoses_fan_belt_and_radiator_support",
            "mechanical_baseline",
            "cooling_routing_baseline",
            "high",
            (
                "engine_front",
                "fan_belt",
                "pulley",
                "alternator",
                "radiator_support",
                "cooling_hose",
            ),
            "Google Photos May 12 engine-front overview showing belt/pulley/alternator layout and radiator-support packaging for cooling and front-support planning.",
        ),
        "20260512_073344_gp_EH3pnE2Q.jpg": c(
            "engine_bay",
            "engine_powertrain_cleaning_baseline",
            "mechanical_baseline",
            "pre_cleaning_baseline",
            "high",
            (
                "gearbox",
                "transmission",
                "case",
                "driveline",
                "powertrain",
                "leak_check",
            ),
            "Google Photos May 12 gearbox/transmission case close-up for degreasing baseline and later leak or seal inspection.",
        ),
        "20260512_073402_gp_P6yrwLRw.jpg": c(
            "engine_bay",
            "cooling_hoses_fan_belt_and_radiator_support",
            "mechanical_baseline",
            "cooling_routing_baseline",
            "high",
            (
                "cooling",
                "radiator",
                "filler_neck",
                "hose",
                "thermostat",
                "front_support",
                "pipe_ordering",
            ),
            "Google Photos May 12 radiator/cooling filler-neck and hose-routing view; supports Longman hose/pipe specification and radiator support planning.",
        ),
        "20260512_073454_gp_9b25G28Q.jpg": c(
            "chassis_underside",
            "steering_and_suspension_linkages",
            "steering_brakes_suspension",
            "steering_box_linkage_baseline",
            "high",
            (
                "steering_box",
                "steering_linkage",
                "drag_link",
                "front_frame",
                "hard_lines",
                "mount_check",
            ),
            "Google Photos May 12 steering box/linkage and front-frame context for steering mount crack checks and EPS conversion planning.",
        ),
        "20260512_073502_gp_7qOudIgA.jpg": c(
            "chassis_underside",
            "front_frame_horns_bumper_and_steering_area",
            "steering_brakes_suspension",
            "steering_box_mount_baseline",
            "high",
            (
                "steering_box",
                "front_frame",
                "steering_column",
                "drag_link",
                "hard_lines",
                "mount_check",
            ),
            "Google Photos May 12 steering box/input and frame-side mount close-up; direct context for steering-box mount checks and future EPS column routing.",
        ),
        "20260512_073509_gp_NvDRwYrQ.jpg": c(
            "engine_bay",
            "engine_powertrain_cleaning_baseline",
            "mechanical_baseline",
            "pre_cleaning_baseline",
            "high",
            (
                "engine",
                "inlet",
                "manifold",
                "hard_lines",
                "front_frame",
                "leak_check",
            ),
            "Google Photos May 12 engine/line close-up that adds pre-cleaning and routing context around the front engine bay.",
        ),
        "20260512_073547_gp_SNtwIVyA.jpg": c(
            "engine_bay",
            "cooling_hoses_fan_belt_and_radiator_support",
            "mechanical_baseline",
            "engine_front_cooling_overview",
            "high",
            (
                "engine_front",
                "fan_belt",
                "pulley",
                "alternator",
                "radiator_support",
                "cooling",
                "engine_bay_overview",
            ),
            "Google Photos May 12 full engine-front overview showing belt drive, alternator, front support, and cooling-space context.",
        ),
        "20260512_100000_user_front_support_radiator_pickups_context.png": c(
            "engine_bay",
            "front_support_radiator_pickups_context",
            "chassis_fixing",
            "radiator_bracket_design_scouting",
            "high",
            (
                "front_support",
                "radiator",
                "radiator_mount",
                "front_crossmember",
                "vertical_upright",
                "fan_clearance",
                "battery_stand_context",
                "bracket_scouting",
            ),
            "User-provided May 12 front support/radiator-side context; shows the radiator plane, fan/pulley clearance, vertical upright/top hole, and front/lower support holes for two-side radiator retention design scouting.",
        ),
        "20260512_100100_user_battery_side_tray_structure_context.png": c(
            "engine_bay",
            "battery_side_tray_structure_context",
            "chassis_fixing",
            "battery_tray_structure_scouting",
            "high",
            (
                "battery_tray",
                "battery_stand",
                "front_support",
                "inner_wing",
                "midi_fuse_carrier",
                "cutoff_switch",
                "alternator_clearance",
                "steering_clearance",
                "exhaust_clearance",
                "bracket_scouting",
            ),
            "User-provided May 12 battery-side structure context; shows nearby rail/plate structure and engine-bay clearance constraints for the battery tray stand, MIDI/cutoff carrier, and cable support planning.",
        ),
        "20260512_110000_user_neolin_mt_tyre_tread_wheel_context.png": c(
            "wheels_and_tires",
            "wheel_tire_neolin_mt_tread_detail",
            "steering_brakes_suspension",
            "tyre_wheel_condition_assessment",
            "high",
            (
                "wheel",
                "tire",
                "tyre",
                "neolin",
                "mud_terrain",
                "tread",
                "sidewall",
                "steel_wheel",
                "roadworthiness_check",
            ),
            "User-provided May 12 tyre/wheel context; Neolin M/T tread appears deep in this view, but date code, inner sidewall, bead, rim runout, and matching-set condition still require physical inspection.",
        ),
        "20260512_110100_user_neolin_mt_tyre_sidewall_wheel_context.png": c(
            "wheels_and_tires",
            "wheel_tire_neolin_mt_sidewall_rim_detail",
            "steering_brakes_suspension",
            "tyre_wheel_condition_assessment",
            "high",
            (
                "wheel",
                "tire",
                "tyre",
                "neolin",
                "mud_terrain",
                "sidewall",
                "rim",
                "valve_stem",
                "wheel_weights",
                "roadworthiness_check",
            ),
            "User-provided May 12 tyre/wheel close-up; outer sidewall and Toyota six-lug steel wheel are visible, with valve stem and wheel weights present. Use for tyre/wheel assessment, not as roadworthy signoff.",
        ),
    }
)


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
    stem = re.sub(r"_gp_[a-zA-Z0-9]+(?:_\d+)?$", "", stem)
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
