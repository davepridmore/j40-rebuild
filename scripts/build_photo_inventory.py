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

RUBBER_RECREATION_20260517_FILES = (
    "20260517_193503_gp_N9nHjqXw.jpg",
    "20260517_193539_gp_E0cR9I0A.jpg",
    "20260517_193559_gp_NEpk1hpg.jpg",
    "20260517_193612_gp_JmbfR0Tw.jpg",
    "20260517_193616_gp_1ye19BZA.jpg",
)

WINDOW_REFURBISHMENT_20260517_FRONT_VENT_FILES = (
    "20260517_193803_gp_1KhFjceQ.jpg",
    "20260517_193837_gp_AERCJIrw.jpg",
)

WINDOW_REFURBISHMENT_20260517_SIDE_GLASS_FILES = (
    "20260517_193956_gp_jvKqbrzA.jpg",
    "20260517_194038_gp_WfGY4cSA.jpg",
)

BATTERY_POWER_CARRIER_20260517_BATTERY_FILES = (
    "20260517_194303_gp_5yuaRoaA.jpg",
    "20260517_194313_gp_HolDWYeQ.jpg",
)

BATTERY_POWER_CARRIER_20260517_MOUNT_FILES = (
    "20260517_194431_gp_4XVycxAg.jpg",
    "20260517_194439_gp_K63N2nJw.jpg",
    "20260517_194452_gp_ow8njPsw.jpg",
    "20260517_194511_gp_QI0Ua2yQ.jpg",
)

TUB_RUST_20260517_FLOOR_FILES = (
    "20260517_195032_gp_lrASxesw.jpg",
    "20260517_195057_gp_U6FxmsPQ.jpg",
    "20260517_195321_gp_4zDAINsA.jpg",
    "20260517_195330_gp_wrE9dLVw.jpg",
    "20260517_195341_gp_ZTYnpWUA.jpg",
)

TUB_RUST_20260517_CORNER_HINGE_FILES = (
    "20260517_195108_gp_elCiXzKw.jpg",
    "20260517_195123_gp_LxOfgsPA.jpg",
    "20260517_195241_gp_RzJdcAZg.jpg",
)

TUB_RUST_20260517_BODY_MOUNT_FILES = (
    "20260517_195406_gp_req8G3Bg.jpg",
    "20260517_195430_gp_VGGpRFOQ.jpg",
)

TUB_RUST_20260517_BODY_SHELL_FILES = (
    "20260517_195511_gp_iFvWFVNw.jpg",
    "20260517_195628_gp_Wog59oFg.jpg",
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
            "windows",
            "front_vent_window_assemblies",
            "window_refurbishment_intake",
            "measurement_reference_needs_refurbish",
            "high",
            (
                "window",
                "vent_window",
                "quarter_window",
                "glass",
                "rubber",
                "seal",
                "channel",
                "rust",
                "measurement",
                "refurbish",
            ),
            "May 17 user-selected window fix-up photo: paired vent/quarter assemblies with ruler context, aged rubbers, and rusted lower channels/tabs; use for the windows workstream intake and seal replacement decision.",
        )
        for file_name in WINDOW_REFURBISHMENT_20260517_FRONT_VENT_FILES
    }
)
FILE_OVERRIDES.update(
    {
        file_name: c(
            "windows",
            "side_window_glass_and_channels",
            "window_refurbishment_intake",
            "measurement_reference_needs_refurbish",
            "high",
            (
                "window",
                "side_window",
                "glass",
                "rubber",
                "seal",
                "weatherstrip",
                "channel",
                "felt",
                "rust",
                "measurement",
                "refurbish",
            ),
            "May 17 user-selected side-window glass/channel measurement photo; visible old rubber/channel material and rusted metal strip make this direct intake evidence for window repair and replacement rubber sourcing.",
        )
        for file_name in WINDOW_REFURBISHMENT_20260517_SIDE_GLASS_FILES
    }
)
FILE_OVERRIDES.update(
    {
        file_name: c(
            "engine_bay",
            "installed_battery_dimension_reference",
            "fabrication_measurement",
            "battery_installed_ruler_reference",
            "high",
            (
                "battery",
                "daewoo",
                "dls120",
                "dimension",
                "tape_reference",
                "terminal",
                "hold_down",
                "battery_power_carrier",
                "fabrication_reference",
            ),
            "May 17 user-selected installed battery measurement photo for the battery power carrier: Daewoo DLS120 case footprint, terminal orientation, and hold-down/clamp context must replace the provisional N70 envelope before final carrier cut release.",
        )
        for file_name in BATTERY_POWER_CARRIER_20260517_BATTERY_FILES
    }
)
FILE_OVERRIDES.update(
    {
        file_name: c(
            "engine_bay",
            "existing_battery_mount_tray_measurements",
            "fabrication_measurement",
            "existing_mount_ruler_reference",
            "high",
            (
                "battery",
                "battery_tray",
                "battery_mount",
                "tray_frame",
                "ruler",
                "dimension",
                "pickup",
                "support",
                "fabrication_reference",
                "battery_power_carrier",
            ),
            "May 17 user-selected existing battery mount measurement photo: tray opening, frame height, corrosion/edge condition, and candidate pickup constraints for the battery stand and power carrier mock-up.",
        )
        for file_name in BATTERY_POWER_CARRIER_20260517_MOUNT_FILES
    }
)
FILE_OVERRIDES.update(
    {
        file_name: c(
            "body_floor",
            "floor_pan_rust_zones",
            "rust_assessment",
            "corrosion_visible",
            "high",
            (
                "tub",
                "floor_pan",
                "rust",
                "corrosion",
                "surface_rust",
                "seam",
                "weld_repair",
                "body_chassis",
            ),
            "May 17 user-selected tub rust photo: floor pan and inner tub floor corrosion areas for body/chassis rust mapping before probing, cut/fab/weld release, primer, or seam sealer.",
        )
        for file_name in TUB_RUST_20260517_FLOOR_FILES
    }
)
FILE_OVERRIDES.update(
    {
        file_name: c(
            "body_exterior",
            "tub_corner_hinge_pin_repair",
            "rust_assessment",
            "cut_hinge_pin_and_corner_repair_required",
            "high",
            (
                "tub",
                "corner",
                "hinge",
                "hinge_pin",
                "cut_pin",
                "rust",
                "perforation",
                "corner_repair",
                "weld_repair",
                "body_chassis",
            ),
            "May 17 user-selected corner/hinge repair photo: hinge pin had to be cut off and the adjacent tub corner/hinge metal needs sorting, probing, backside access check, and repair-method release before primer or paint closure.",
        )
        for file_name in TUB_RUST_20260517_CORNER_HINGE_FILES
    }
)
FILE_OVERRIDES.update(
    {
        file_name: c(
            "body_floor",
            "floor_seam_and_body_mount_rust",
            "rust_assessment",
            "corrosion_visible",
            "high",
            (
                "tub",
                "body_mount",
                "captive_nut",
                "mount_plate",
                "hinge_point",
                "rust",
                "perforation",
                "weld_repair",
                "body_chassis",
            ),
            "May 17 user-selected tub rust detail: body-mount/captive fastener, hinge-edge, and seam corrosion areas that need station labels, probing, and backside access checks before refit or paint closure.",
        )
        for file_name in TUB_RUST_20260517_BODY_MOUNT_FILES
    }
)
FILE_OVERRIDES.update(
    {
        file_name: c(
            "body_exterior",
            "body_shell_with_doors_removed",
            "rust_assessment",
            "corrosion_visible",
            "high",
            (
                "tub",
                "body_shell",
                "door_opening",
                "side_panel",
                "aperture",
                "rust",
                "corrosion",
                "body_chassis",
            ),
            "May 17 user-selected tub rust overview: body-side aperture and side-shell context tying the close-up floor, mount, and seam corrosion photos back to their vehicle location.",
        )
        for file_name in TUB_RUST_20260517_BODY_SHELL_FILES
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
            "procurement_inventory",
            "rubber_parts_recreation_samples",
            "procurement_reconciliation",
            "measurement_reference",
            "high",
            (
                "rubber",
                "strip",
                "channel",
                "measurement",
                "tape_reference",
                "recreation",
                "fabrication",
            ),
            "May 17 user-selected long rubber strip/channel measurement reference for rubber fabrication; use as shape and scale evidence only until the physical part/location trace is confirmed.",
        )
        for file_name in RUBBER_RECREATION_20260517_FILES
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
        "20260512_211249_gp_MFXOIt2w.jpg": c(
            "interior_cabin",
            "j40_removed_steering_column_set",
            "eps_vitz_upgrade",
            "removed_column_reference",
            "high",
            (
                "j40",
                "steering",
                "steering_column",
                "column_switch",
                "wiring",
                "eps_conversion",
                "layout_reference",
            ),
            "Google Photos May 12 removed J40 steering column/switch assembly; use as vehicle-side reference for EPS column graft planning, wiring cleanup, and upper-column retention decisions.",
        ),
        "20260512_205417_gp_CzJNQsiA.jpg": c(
            "engine_bay",
            "front_support_radiator_measurement_set",
            "chassis_fixing",
            "radiator_removed_mounting_reference",
            "high",
            (
                "radiator",
                "radiator_mount",
                "mounting_tabs",
                "side_brackets",
                "lower_bracket",
                "fabrication",
                "measurement",
            ),
            "Google Photos May 12 radiator removed from vehicle; shows full core, side brackets, lower bracket, and mounting tab layout for front radiator retention fabrication.",
        ),
        "20260512_205434_gp_QnE3tLvQ.jpg": c(
            "engine_bay",
            "front_support_radiator_measurement_set",
            "chassis_fixing",
            "radiator_removed_mounting_reference",
            "high",
            (
                "radiator",
                "radiator_mount",
                "side_brackets",
                "lower_bracket",
                "hose_connection",
                "fabrication",
                "measurement",
            ),
            "Google Photos May 12 radiator reverse/side overview; confirms bracket positions and hose-side layout for the radiator retention template.",
        ),
        "20260512_212929_gp_pnlr6x5w.jpg": c(
            "engine_bay",
            "front_support_radiator_measurement_set",
            "chassis_fixing",
            "radiator_height_measurement",
            "high",
            (
                "radiator",
                "radiator_mount",
                "tape_measure",
                "height",
                "side_bracket",
                "fabrication",
                "measurement",
            ),
            "Google Photos May 12 tape-measure view along the radiator side/bracket; use as radiator height and side-bracket reference for the two-side retention template.",
        ),
        "20260512_212947_gp_AdvWGolg.jpg": c(
            "engine_bay",
            "front_support_radiator_measurement_set",
            "chassis_fixing",
            "radiator_side_bracket_measurement",
            "high",
            (
                "radiator",
                "radiator_mount",
                "tape_measure",
                "side_bracket",
                "lower_tank",
                "fabrication",
                "measurement",
            ),
            "Google Photos May 12 tape-measure close-up of radiator side tube/bracket and lower tank area; use for vertical bracket span and isolator/strap layout.",
        ),
        "20260512_213008_gp_1U5vulZw.jpg": c(
            "engine_bay",
            "front_support_radiator_measurement_set",
            "chassis_fixing",
            "radiator_lower_side_tab_measurement",
            "high",
            (
                "radiator",
                "radiator_mount",
                "tape_measure",
                "mounting_tab",
                "hose_connection",
                "fabrication",
                "measurement",
            ),
            "Google Photos May 12 lower radiator side tab and hose-side bracket with tape; use for lower pickup position and clearance planning.",
        ),
        "20260512_213027_gp_9Cy950Kw.jpg": c(
            "engine_bay",
            "front_support_radiator_measurement_set",
            "chassis_fixing",
            "radiator_complete_mounting_reference",
            "high",
            (
                "radiator",
                "radiator_mount",
                "mounting_tabs",
                "side_brackets",
                "lower_bracket",
                "fabrication",
                "measurement",
            ),
            "Google Photos May 12 full radiator mounting overview after measurement photos; confirms side tabs, lower bracket, and opposite-side pickup layout.",
        ),
        "20260512_213129_gp_IVnd8hWQ.jpg": c(
            "engine_bay",
            "front_support_radiator_pickups_context",
            "chassis_fixing",
            "front_upright_height_measurement",
            "high",
            (
                "front_support",
                "radiator",
                "radiator_mount",
                "tape_measure",
                "vertical_upright",
                "fan_clearance",
                "fabrication",
                "measurement",
            ),
            "Google Photos May 12 in-vehicle tape-measure view of the front support upright near the fan/belt plane; use for radiator bracket height and clearance constraints.",
        ),
        "20260512_213144_gp_2rlycKHA.jpg": c(
            "engine_bay",
            "front_support_radiator_pickups_context",
            "chassis_fixing",
            "front_upright_offset_measurement",
            "high",
            (
                "front_support",
                "radiator",
                "radiator_mount",
                "tape_measure",
                "top_tab",
                "offset",
                "fabrication",
                "measurement",
            ),
            "Google Photos May 12 close tape-measure view across the front support upright/top tab; use for bracket offset and tab-width planning.",
        ),
        "20260512_213214_gp_xZKluAkg.jpg": c(
            "engine_bay",
            "front_support_radiator_pickups_context",
            "chassis_fixing",
            "front_support_opening_measurement",
            "high",
            (
                "front_support",
                "radiator",
                "radiator_mount",
                "tape_measure",
                "fan_clearance",
                "front_crossmember",
                "fabrication",
                "measurement",
            ),
            "Google Photos May 12 in-vehicle tape-measure view across the front support/radiator opening and fan-belt area; use for radiator plane and clearance envelope.",
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
        "20260514_095907_gp_Ni1EUf4A.jpg": c(
            "chassis_underside",
            "frame_floor_underside_and_lines",
            "brake_system",
            "hydraulic_fitting_identification",
            "high",
            (
                "brake_hydraulic",
                "hard_line",
                "flare_nut",
                "junction_block",
                "master_or_proportioning_area",
            ),
            "Google Photos May 14 brake hydraulic hard-line close-up; shows installed flare-nut style and line routing around the master/proportioning area but not a bare pipe end.",
        ),
        "20260514_095856_gp_vjZG4NtQ.jpg": c(
            "chassis_underside",
            "rear_axle_and_leaf_springs",
            "brake_system",
            "rear_brake_line_identification",
            "high",
            (
                "rear_axle",
                "rear_brake",
                "hard_line",
                "flex_hose",
                "flare_nut",
                "parking_brake_cable",
            ),
            "Google Photos May 14 rear brake line/flex-hose area close-up; useful for rear axle hard-line and parking-brake routing before removal.",
        ),
        "20260514_095846_gp_a9olRp5g.jpg": c(
            "chassis_underside",
            "rear_axle_and_leaf_springs",
            "brake_system",
            "rear_brake_line_identification",
            "high",
            (
                "rear_axle",
                "rear_brake",
                "hard_line",
                "flex_hose",
                "line_route",
                "bracket",
            ),
            "Google Photos May 14 rear axle hard-line route view with nearby hose/bracket context; supports brake line recreation but still needs removed-line template.",
        ),
        "20260514_095836_gp_tmRy9fqg.jpg": c(
            "chassis_underside",
            "rear_axle_and_leaf_springs",
            "brake_system",
            "rear_brake_line_identification",
            "high",
            (
                "rear_axle",
                "rear_brake",
                "hard_line",
                "flex_hose",
                "parking_brake",
                "line_route",
            ),
            "Google Photos May 14 rear brake hard-line and parking-brake linkage context at the axle; useful for route and clearance checks.",
        ),
        "20260514_095826_gp_fg74oFMQ.jpg": c(
            "chassis_underside",
            "rear_axle_and_leaf_springs",
            "brake_system",
            "rear_wheel_cylinder_line_identification",
            "high",
            (
                "rear_axle",
                "rear_brake",
                "drum",
                "wheel_cylinder",
                "hard_line",
                "parking_brake",
            ),
            "Google Photos May 14 rear drum/backing-plate close-up with wheel-cylinder hard-line entry and parking-brake cable context.",
        ),
        "20260514_095820_gp_nuP5s76A.jpg": c(
            "chassis_underside",
            "rear_axle_and_leaf_springs",
            "brake_system",
            "rear_brake_line_identification",
            "high",
            (
                "rear_axle",
                "rear_brake",
                "drum",
                "hard_line",
                "line_clip",
                "parking_brake",
            ),
            "Google Photos May 14 rear axle/drum view showing brake hard-line route, clip/support context, and parking-brake linkage.",
        ),
        "20260514_095812_gp_5kblggGA.jpg": c(
            "chassis_underside",
            "rear_axle_and_leaf_springs",
            "brake_system",
            "rear_wheel_cylinder_line_identification",
            "high",
            (
                "rear_axle",
                "rear_brake",
                "drum",
                "wheel_cylinder",
                "hard_line",
                "backing_plate",
            ),
            "Google Photos May 14 rear wheel-cylinder hard-line entry close-up; supports fitting and route identification but not final flare-thread signoff.",
        ),
        "20260514_095926_gp_YBNOqh9A.jpg": c(
            "chassis_underside",
            "frame_floor_underside_and_lines",
            "brake_system",
            "master_cylinder_line_identification",
            "high",
            (
                "brake_master",
                "reservoir",
                "hard_line",
                "flare_nut",
                "hydraulic_port",
                "fitting_identification",
            ),
            "Google Photos May 14 master-cylinder/reservoir and hydraulic line fitting close-up; useful for port and flare-nut identification before exact parts release.",
        ),
        "20260514_095953_gp_BXoQkXnw.jpg": c(
            "chassis_underside",
            "rear_axle_and_leaf_springs",
            "brake_system",
            "rear_parking_brake_cable_identification",
            "high",
            (
                "rear_axle",
                "rear_brake",
                "drum",
                "parking_brake",
                "cable",
                "backing_plate",
            ),
            "Google Photos May 14 rear drum/backing-plate and parking-brake cable close-up; supports cable-end and routing capture.",
        ),
        "20260514_100003_gp_Vr2QI7ig.jpg": c(
            "chassis_underside",
            "rear_axle_and_leaf_springs",
            "brake_system",
            "rear_parking_brake_cable_identification",
            "medium",
            (
                "rear_axle",
                "rear_brake",
                "parking_brake",
                "cable",
                "bracket",
                "route",
            ),
            "Google Photos May 14 rear parking-brake cable/bracket route context; useful for cable replacement planning rather than hydraulic flare identification.",
        ),
        "20260514_100008_gp_bq1VQUXQ.jpg": c(
            "chassis_underside",
            "rear_axle_and_leaf_springs",
            "brake_system",
            "rear_wheel_cylinder_line_identification",
            "high",
            (
                "rear_axle",
                "rear_brake",
                "drum",
                "wheel_cylinder",
                "hard_line",
                "parking_brake",
            ),
            "Google Photos May 14 rear drum/wheel-cylinder hard-line and parking-brake close-up; supports rear hard-line and cable recreation.",
        ),
        "20260514_100647_gp_foDr3ymA.jpg": c(
            "chassis_underside",
            "frame_floor_underside_and_lines",
            "brake_system",
            "hydraulic_flare_nut_identification",
            "high",
            (
                "brake_hydraulic",
                "hard_line",
                "flex_hose",
                "flare_nut",
                "thread",
                "fitting_identification",
            ),
            "Google Photos May 14 close-up of a brake hard-line flare nut into a hydraulic fitting; strongest current photo for fitting style, but the flare face remains hidden while installed.",
        ),
        "20260514_111300_user_brake_flare_side_view.png": c(
            "chassis_underside",
            "brake_hard_line_flare_sample",
            "brake_system",
            "hydraulic_flare_side_view_identification",
            "high",
            (
                "brake_hydraulic",
                "hard_line",
                "flare",
                "double_inverted_flare_candidate",
                "thread_seat_confirmation_required",
                "fitting_identification",
            ),
            "User-provided May 14 side-view close-up of a brake hard-line flare. The raised folded lip supports the working double/inverted flare read, but the sealing face and port seat still need a straight-on/open-port confirmation before fabrication.",
        ),
        "20260515_112827_gp_kbx0JKSQ.jpg": c(
            "electrical_system",
            "battery_power_carrier_relay_box_cover",
            "electrical_reset",
            "component_reference_photo",
            "high",
            (
                "relay_box",
                "covered_box",
                "loom_exit",
                "battery_power_carrier",
                "fabrication_reference",
            ),
            "Google Photos May 15 relay/fuse box reference: plain covered black enclosure with cover screws and side/upper loom exits; use to simplify the relay visual model and keep cover access clear.",
        ),
        "20260515_112836_gp_sFdn9AyA.jpg": c(
            "electrical_system",
            "battery_power_carrier_100a_cutoff_breaker",
            "electrical_reset",
            "component_reference_photo",
            "high",
            (
                "100a_breaker",
                "cutoff",
                "ring_lug",
                "cable_boot",
                "battery_power_carrier",
                "fabrication_reference",
            ),
            "Google Photos May 15 100A waterproof resettable breaker/cutoff reference: large ring lugs and heavy cable boots confirm lug sweep and service-clearance hold.",
        ),
        "20260515_112907_gp_wtj4G8tQ.jpg": c(
            "electrical_system",
            "battery_power_carrier_midi_fuse_bank",
            "electrical_reset",
            "component_reference_photo",
            "high",
            (
                "midi_fuse",
                "five_output_side",
                "common_feed",
                "heavy_cable_fanout",
                "battery_power_carrier",
                "fabrication_reference",
            ),
            "Google Photos May 15 MIDI bank reference: red linked fuse holders with one common feed side and five heavy output cables on the opposite side; drives the widened cable gutter and fanout clearance.",
        ),
        "20260517_193305_gp_o1a6StwA.jpg": c(
            "roof_and_gutters",
            "roof_gutter_and_window_channel",
            "hardware_refinish",
            "refinished_off_vehicle",
            "high",
            (
                "roof",
                "gutter",
                "painted",
                "refinished",
                "post_paint",
                "returned",
            ),
            "Google Photos May 17 returned painted roof evidence selected by user; use to close the roof paint return against the earlier send-out roof image.",
        ),
    }
)

FILE_OVERRIDES.update(
    {
        file_name: c(
            "chassis_underside",
            "frame_floor_underside_and_lines",
            "underside_inspection",
            "underside_assessment_input",
            "high",
            (
                "chassis",
                "underside",
                "underbody",
                "frame",
                "floor",
                "assessment",
            ),
            "Google Photos May 14 chassis underside batch selected for underside assessment; use these as direct inspection inputs for frame/floor underside, line routing, brackets, and crossmember condition review.",
        )
        for file_name in (
            "20260514_131654_gp_X9nuzrAw.jpg",
            "20260514_131705_gp_1lBIZ23g.jpg",
            "20260514_131713_gp_vMeGm6hQ.jpg",
            "20260514_131719_gp_afzzZAdQ.jpg",
            "20260514_131726_gp_5bfPs4Vw.jpg",
            "20260514_131732_gp_jF6HwyFQ.jpg",
            "20260514_131739_gp_fiEuvooA.jpg",
            "20260514_131749_gp_pImh6gQQ.jpg",
            "20260514_131754_gp_DZoems5Q.jpg",
            "20260514_131802_gp_j8XssFqQ.jpg",
            "20260514_131810_gp_z0Z4XiNw.jpg",
            "20260514_131820_gp_1xufuqnA.jpg",
            "20260514_131828_gp_X2MxCSEQ.jpg",
            "20260514_131834_gp_V4LCu2hw.jpg",
            "20260514_131845_gp_ythUacVA.jpg",
        )
    }
)

FILE_OVERRIDES.update(
    {
        "20260517_230500_user_rear_differential_carrier_cover.png": c(
            "chassis_underside",
            "rear_differential_carrier_and_axle_housing",
            "mechanical_baseline",
            "inspection_plan_trigger",
            "high",
            (
                "rear_axle",
                "differential",
                "carrier",
                "pumpkin",
                "gear_oil",
                "breather",
                "brake_line",
                "leaf_spring",
                "inspection",
            ),
            "User-supplied May 17 differential carrier/pumpkin close-up; use as the trigger image for the rear differential/axle teardown inspection plan before axle coating, brake closeout, suspension alignment, or road validation.",
        ),
    }
)

FILE_OVERRIDES.update(
    {
        "20260517_204429_gp_yEAcUHBg.jpg": c(
            "electrical_system",
            "engine_starter_solenoid_and_ground_inputs",
            "electrical_refit",
            "existing_engine_input_identified_rework_required",
            "high",
            (
                "engine",
                "starter",
                "starter_solenoid",
                "battery_cable",
                "solenoid_trigger",
                "ground",
                "wiring",
                "electrical_refit",
            ),
            "Google Photos May 17 starter/solenoid area: heavy cable, solenoid trigger region, and nearby ground return need terminal cleanup, labels, and voltage-drop testing before final loom wrap.",
        ),
        "20260517_204445_gp_oaQKzDrA.jpg": c(
            "electrical_system",
            "engine_unidentified_two_wire_connector",
            "electrical_refit",
            "existing_engine_input_unverified",
            "medium",
            (
                "engine",
                "connector",
                "two_wire",
                "sensor",
                "switch",
                "unknown",
                "continuity_required",
                "electrical_refit",
            ),
            "Google Photos May 17 close-up of a two-wire inline engine/gearbox-area connector. Treat as unassigned until component end, key-state feed, and continuity path are proven.",
        ),
        "20260517_204504_gp_46p1VNCg.jpg": c(
            "electrical_system",
            "injection_pump_throttle_linkage_electrical_input",
            "electrical_refit",
            "existing_engine_input_identified_rework_required",
            "medium",
            (
                "engine",
                "injection_pump",
                "throttle_linkage",
                "fuel_stop",
                "idle_up",
                "edic",
                "connector",
                "verify_function",
                "electrical_refit",
            ),
            "Google Photos May 17 injection-pump/throttle-linkage electrical item. It may relate to fuel-stop, idle-up, or engine control; verify the device and wire function before assigning it to WP03B.",
        ),
        "20260517_204538_gp_9CERKvYA.jpg": c(
            "electrical_system",
            "engine_loose_connector_unassigned",
            "electrical_refit",
            "existing_engine_input_unverified",
            "medium",
            (
                "engine",
                "loose_connector",
                "connector",
                "sensor",
                "switch",
                "unknown",
                "continuity_required",
                "electrical_refit",
            ),
            "Google Photos May 17 loose engine-side connector. Do not reconnect blindly; trace both ends and decide repair, delete, or retain before final wrapping.",
        ),
        "20260517_204550_gp_kDsqLZQg.jpg": c(
            "electrical_system",
            "injection_pump_throttle_linkage_electrical_input",
            "electrical_refit",
            "existing_engine_input_route_context",
            "medium",
            (
                "engine",
                "injection_pump",
                "throttle_linkage",
                "loose_connector",
                "loom_route",
                "verify_function",
                "electrical_refit",
            ),
            "Google Photos May 17 wider context for the injection-pump/throttle-linkage connector branch and loose wiring route; use for routing, strain relief, and function reconciliation.",
        ),
        "20260517_204615_gp_wsn4bN8g.jpg": c(
            "electrical_system",
            "engine_sender_branch",
            "electrical_refit",
            "existing_engine_input_unverified",
            "medium",
            (
                "engine",
                "sender",
                "temperature_sender",
                "gauge",
                "warning_lamp",
                "green_red_wire",
                "continuity_required",
                "electrical_refit",
            ),
            "Google Photos May 17 engine-side sender branch with green/red wiring visible. Probable gauge or warning-lamp input, but sender type and dash endpoint must be verified electrically.",
        ),
        "20260517_204711_gp_jZ4tm3uQ.jpg": c(
            "electrical_system",
            "engine_sender_branch",
            "electrical_refit",
            "existing_engine_input_route_context",
            "medium",
            (
                "engine",
                "sender",
                "injection_pump",
                "loom_route",
                "hard_lines",
                "clearance",
                "continuity_required",
                "electrical_refit",
            ),
            "Google Photos May 17 wider engine-side view for the sender/injection-pump branch route near hard lines and linkage; use to prove clearance before final clipping.",
        ),
        "20260517_204725_gp_y7P6qvhQ.jpg": c(
            "electrical_system",
            "engine_input_loom_routing_context",
            "electrical_refit",
            "route_context_for_engine_inputs",
            "medium",
            (
                "engine",
                "injection_pump",
                "hard_lines",
                "loom_route",
                "clearance",
                "electrical_refit",
            ),
            "Google Photos May 17 injection-pump/injector-line top-side context. Use as route and clearance evidence for the engine input loom; no circuit assignment from this image alone.",
        ),
        "20260517_204740_gp_yI8f8DQw.jpg": c(
            "electrical_system",
            "alternator_charge_regulator_wiring",
            "electrical_refit",
            "existing_charge_wiring_rework_required",
            "high",
            (
                "engine",
                "alternator",
                "charging",
                "regulator",
                "exciter",
                "sense",
                "output",
                "wiring",
                "electrical_refit",
            ),
            "Google Photos May 17 alternator body and wiring. Reconcile charge output, exciter/warning, sense, and ground paths to the existing loom after reading actual terminal markings.",
        ),
        "20260517_204756_gp_xdOm3erw.jpg": c(
            "electrical_system",
            "alternator_charge_regulator_wiring",
            "electrical_refit",
            "existing_charge_wiring_rework_required",
            "high",
            (
                "engine",
                "alternator",
                "charging",
                "regulator",
                "exciter",
                "sense",
                "output",
                "ring_terminal",
                "electrical_refit",
            ),
            "Google Photos May 17 alternator rear/terminal-side evidence with aged taped terminations. Replace weak terminals and confirm charge, warning/excite, sense, and ground behavior before final protection.",
        ),
    }
)

FILE_OVERRIDES.update(
    {
        "20260517_194754_gp_vXLV7rzA.jpg": c(
            "electrical_system",
            "cabin_engine_firewall_pass_through_holes",
            "electrical_refit",
            "existing_hole_measurement_context",
            "medium",
            (
                "firewall",
                "cabin_to_engine",
                "pass_through",
                "hole",
                "grommet",
                "measurement",
                "routing",
                "electrical_refit",
            ),
            "Google Photos May 17 cabin/firewall pass-through context with tape reference; blurry image but useful with the sharper measurement photos for locating existing cabin-to-engine holes.",
        ),
        "20260517_194806_gp_eou5ctOQ.jpg": c(
            "electrical_system",
            "cabin_engine_firewall_pass_through_holes",
            "electrical_refit",
            "existing_hole_measurement_reference",
            "high",
            (
                "firewall",
                "cabin_to_engine",
                "pass_through",
                "hole",
                "grommet",
                "measurement",
                "rust",
                "routing",
                "electrical_refit",
            ),
            "Google Photos May 17 close-up of existing firewall/cabin pass-through holes with tape reference, paint loss, and rust at surrounding sheet metal. Use to size grommets and decide which holes are safe to reuse.",
        ),
        "20260517_194841_gp_eXh30voQ.jpg": c(
            "electrical_system",
            "cabin_engine_firewall_pass_through_holes",
            "electrical_refit",
            "existing_hole_route_and_measurement_reference",
            "high",
            (
                "firewall",
                "cabin_to_engine",
                "pass_through",
                "hole",
                "grommet",
                "steering_column",
                "measurement",
                "routing",
                "electrical_refit",
            ),
            "Google Photos May 17 wider cabin-side firewall pass-through view with tape reference, steering-column/boot context, and multiple existing openings. Use for route clearance before adding wiring or control-cable passes.",
        ),
        "20260517_194911_gp_jCrFS5PA.jpg": c(
            "electrical_system",
            "cabin_engine_firewall_pass_through_holes",
            "electrical_refit",
            "existing_hole_route_and_measurement_reference",
            "high",
            (
                "firewall",
                "cabin_to_engine",
                "pass_through",
                "hole",
                "grommet",
                "steering_column",
                "measurement",
                "routing",
                "electrical_refit",
            ),
            "Google Photos May 17 wide measurement photo across existing cabin-to-engine firewall openings. Use to map hole positions against steering, pedals, and planned loom or control-cable routing.",
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
