from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANUAL_DIR = ROOT / "data" / "manual"
DOCS_DIR = ROOT / "docs"

COMPONENT_JOBS_PATH = MANUAL_DIR / "component_jobs.csv"
PHOTO_INVENTORY_PATH = MANUAL_DIR / "photo_inventory.csv"
OUTPUT_CSV_PATH = MANUAL_DIR / "component_jobs_photo_reconciliation.csv"
OUTPUT_MD_PATH = DOCS_DIR / "component-jobs-photo-reconciliation.md"
NON_COMPONENT_EVIDENCE_STAGES: set[str] = {"procurement_reconciliation"}

TUB_RUST_20260517_MEDIA_IDS: tuple[str, ...] = (
    "20260517_195032_gp_lrASxesw",
    "20260517_195057_gp_U6FxmsPQ",
    "20260517_195108_gp_elCiXzKw",
    "20260517_195123_gp_LxOfgsPA",
    "20260517_195241_gp_RzJdcAZg",
    "20260517_195321_gp_4zDAINsA",
    "20260517_195330_gp_wrE9dLVw",
    "20260517_195341_gp_ZTYnpWUA",
    "20260517_195406_gp_req8G3Bg",
    "20260517_195430_gp_VGGpRFOQ",
    "20260517_195511_gp_iFvWFVNw",
    "20260517_195628_gp_Wog59oFg",
)

ENGINE_ELECTRICAL_INPUTS_20260517_MEDIA_IDS: tuple[str, ...] = (
    "20260517_204429_gp_yEAcUHBg",
    "20260517_204445_gp_oaQKzDrA",
    "20260517_204504_gp_46p1VNCg",
    "20260517_204538_gp_9CERKvYA",
    "20260517_204550_gp_kDsqLZQg",
    "20260517_204615_gp_wsn4bN8g",
    "20260517_204711_gp_jZ4tm3uQ",
    "20260517_204725_gp_y7P6qvhQ",
    "20260517_204740_gp_yI8f8DQw",
    "20260517_204756_gp_xdOm3erw",
)

CABIN_ENGINE_FIREWALL_HOLES_20260517_MEDIA_IDS: tuple[str, ...] = (
    "20260517_194754_gp_vXLV7rzA",
    "20260517_194806_gp_eou5ctOQ",
    "20260517_194841_gp_eXh30voQ",
    "20260517_194911_gp_jCrFS5PA",
)


@dataclass(frozen=True)
class EvidenceRule:
    direct_specific_components: tuple[str, ...]
    indirect_specific_components: tuple[str, ...]
    notes: str = ""
    direct_media_ids: tuple[str, ...] = ()
    indirect_media_ids: tuple[str, ...] = ()


RULES: dict[str, EvidenceRule] = {
    "roof_shell": EvidenceRule(
        direct_specific_components=("roof_gutter_and_window_channel",),
        indirect_specific_components=(),
        notes="Roof channel/rain gutter photos are direct evidence of roof shell condition.",
    ),
    "back_doors": EvidenceRule(
        direct_specific_components=("detached_body_panels_and_doors", "detached_doors_and_panels"),
        indirect_specific_components=("front_door_card",),
        notes="Detached door panels are direct; interior door card is supporting context.",
    ),
    "front_windows": EvidenceRule(
        direct_specific_components=("hood_and_front_windshield_overview",),
        indirect_specific_components=("cabin_view_through_glass", "cabin_overview", "side_window_glass_and_channels"),
        notes="Front windshield is explicitly captured in dedicated front overview shots; May 17 side-window glass photos support the broader windows workstream.",
    ),
    "front_vent_window_assemblies": EvidenceRule(
        direct_specific_components=("front_vent_window_assemblies",),
        indirect_specific_components=("window_rubber_seals_and_frames", "cabin_view_through_glass", "side_window_glass_and_channels"),
        notes="Detached paired vent/quarter window assemblies are directly documented and should close through the windows refurbishment gate.",
    ),
    "hood": EvidenceRule(
        direct_specific_components=("hood_and_front_windshield_overview",),
        indirect_specific_components=("front_exterior_walkaround", "engine_bay_overview", "front_panel_lighting_mount_area"),
        notes="Hood panel/latches are explicitly visible in front overview shots.",
    ),
    "back_cabin": EvidenceRule(
        direct_specific_components=("rear_cargo_floor", "body_shell_with_doors_removed", "rear_side_opening", "dashboard_shell_and_cabin"),
        indirect_specific_components=("detached_body_panels_and_doors",),
        notes="Rear cabin/body section is directly visible in multiple strip-down shots.",
    ),
    "window_mechanisms": EvidenceRule(
        direct_specific_components=("rear_hatch_window_latch_mechanisms", "front_vent_window_assemblies"),
        indirect_specific_components=("wiper_arm_or_linkage_hardware", "side_window_glass_and_channels"),
        notes="Rear hatch latch hardware and vent-window latch/pivot assemblies are directly documented; wiper/linkage remains supporting evidence.",
    ),
    "body_rubbers": EvidenceRule(
        direct_specific_components=("window_rubber_seals_and_frames", "front_vent_window_assemblies", "side_window_glass_and_channels"),
        indirect_specific_components=("roof_gutter_and_window_channel", "cabin_view_through_glass"),
        notes="Detached window assemblies, channels, and rubber surrounds are directly documented; non-window body-mount rubber remains controlled separately.",
    ),
    "window_rubbers_weatherstrips": EvidenceRule(
        direct_specific_components=("window_rubber_seals_and_frames", "front_vent_window_assemblies", "side_window_glass_and_channels"),
        indirect_specific_components=("roof_gutter_and_window_channel", "cabin_view_through_glass"),
        notes="Window rubber/weatherstrip replacement is supported by May 17 removed window assembly measurements plus earlier window-seal context.",
    ),
    "interior": EvidenceRule(
        direct_specific_components=(
            "cabin_overview",
            "dashboard_and_cabin_stripdown",
            "dashboard_lower_structure",
            "dashboard_shell_and_cabin",
            "driver_footwell_firewall_and_wiring",
            "floor_pan_and_firewall",
            "rear_cargo_floor",
        ),
        indirect_specific_components=("dashboard_fascia_trim", "front_door_card", "cabin_view_through_glass"),
        notes="Interior strip-down and cabin state are well documented.",
    ),
    "old_accessory_wiring": EvidenceRule(
        direct_specific_components=(
            "wiring_harness_and_connectors",
            "wiring_harness_and_fuse_distribution",
            "fuse_distribution_and_power_hardware",
            "fuse_distribution_and_wiring",
            "firewall_and_dash_wiring",
            "driver_footwell_firewall_pass_through",
            "driver_footwell_firewall_and_wiring",
            "pedal_box_wiring",
        ),
        indirect_specific_components=("electrical_reference_document", "electrical_wiring_diagram"),
        notes="Accessory/electrical removal and rebuild work has strong direct photo coverage.",
    ),
    "engine_electrical_inputs_reconciliation_20260517": EvidenceRule(
        direct_specific_components=(
            "engine_starter_solenoid_and_ground_inputs",
            "alternator_charge_regulator_wiring",
            "injection_pump_throttle_linkage_electrical_input",
            "engine_sender_branch",
            "engine_unidentified_two_wire_connector",
            "engine_loose_connector_unassigned",
            "engine_input_loom_routing_context",
        ),
        indirect_specific_components=("engine_bay_overview", "engine_powertrain_cleaning_baseline"),
        notes="May 17 selected photos are the active engine electrical input reconciliation set; starter, alternator, sender, injection-pump/throttle-linked, and unknown connector branches must be labelled and electrically proven before final wrap.",
        direct_media_ids=ENGINE_ELECTRICAL_INPUTS_20260517_MEDIA_IDS,
    ),
    "cabin_engine_firewall_holes_survey_20260517": EvidenceRule(
        direct_specific_components=("cabin_engine_firewall_pass_through_holes",),
        indirect_specific_components=(
            "driver_footwell_firewall_pass_through",
            "driver_footwell_firewall_and_wiring",
            "pedal_box_wiring",
            "firewall_and_dash_wiring",
        ),
        notes="May 17 selected photos are the active cabin-to-engine firewall hole survey; size, edge condition, grommet availability, and routing assignment must be logged before reusing or closing any opening.",
        direct_media_ids=CABIN_ENGINE_FIREWALL_HOLES_20260517_MEDIA_IDS,
    ),
    "floor_pan": EvidenceRule(
        direct_specific_components=("floor_pan_and_firewall", "floor_pan_rust_zones", "floor_seam_and_body_mount_rust"),
        indirect_specific_components=("frame_floor_underside_and_lines", "rear_cargo_floor"),
        notes="Floor pan rust/condition is directly evidenced with dedicated close-ups; May 17 adds tub floor, seam, and body-mount rust details.",
    ),
    "tub_rust_damage_survey_20260517": EvidenceRule(
        direct_specific_components=(),
        indirect_specific_components=("rear_cargo_floor", "body_shell_with_doors_removed", "rear_side_opening"),
        notes="May 17 selected photos are the active tub rust-damage intake set; each still needs station labels, probe results, and repair release decisions.",
        direct_media_ids=TUB_RUST_20260517_MEDIA_IDS,
    ),
    "tub_corner_hinge_pin_repair_20260517": EvidenceRule(
        direct_specific_components=("tub_corner_hinge_pin_repair",),
        indirect_specific_components=("floor_seam_and_body_mount_rust", "body_shell_with_doors_removed"),
        notes="The May 17 re-selected close-ups isolate the corner/hinge repair issue where the hinge pin had to be cut off; release requires side/location labels, probe results, hinge hardware decision, and repair-method signoff.",
    ),
    "rear_fuel_tank": EvidenceRule(
        direct_specific_components=("fuel_filler_side_panel", "rear_cargo_floor"),
        indirect_specific_components=("frame_floor_underside_and_lines",),
        notes="Fuel tank-out context and tank-area access are documented in filler-side and rear-floor images.",
    ),
    "front_wings": EvidenceRule(
        direct_specific_components=(),
        indirect_specific_components=("wing_removal_and_body_lift_prep", "front_panel_lighting_mount_area", "hood_and_front_windshield_overview"),
        notes="Front wings are tracked to paint from the April 23 send-day detached-parts batch; wing-removal photos are supporting context only.",
        direct_media_ids=(
            "20260423_183408_gp_eCiJmZnA",
            "20260423_183448_gp_9MQfbmvQ",
            "20260423_183514_gp_DyztXKcw",
            "20260423_183521_gp_pjVN2Ujw",
            "20260423_183540_gp_bhRdLpMg",
            "20260423_183628_gp_SpWIfUnw",
        ),
    ),
    "paint_sendout_panels_manifest": EvidenceRule(
        direct_specific_components=("detached_body_panels_and_doors", "detached_doors_and_panels", "rear_hatch_inner_panel"),
        indirect_specific_components=("body_shell_with_doors_removed", "rear_side_opening"),
        notes="Detached panel/door batches and the April 23 roof image provide direct send-out evidence for painting.",
        direct_media_ids=("20260423_183648_gp_ltd3AKwg",),
    ),
    "paint_returned_panels_refinished": EvidenceRule(
        direct_specific_components=("refinished_hinges_brackets_and_trim", "refinished_seat_or_mount_bracket", "wiper_arm_or_linkage_hardware"),
        indirect_specific_components=("panel_detail_and_markings", "front_panel_lighting_mount_area"),
        notes="Off-vehicle refinished hardware/panel photos and the May 17 returned roof image provide direct evidence of returned painted parts.",
        direct_media_ids=("20260517_193305_gp_o1a6StwA",),
    ),
    "paint_workshop_progress_media": EvidenceRule(
        direct_specific_components=("panel_detail_and_markings", "off_vehicle_workstation_reference_video"),
        indirect_specific_components=("detached_body_panels_and_doors", "detached_doors_and_panels"),
        notes="In-progress workshop videos and panel-handling shots track painting/bodywork activity between send-out and return; stripdown wing-removal photos are not direct paint evidence.",
    ),
    "chassis_frame_and_crossmembers": EvidenceRule(
        direct_specific_components=(
            "frame_floor_underside_and_lines",
            "frame_and_mount_points",
            "rear_frame_crossmember_and_mounts",
            "frame_rail_body_mount_and_crossmember_detail",
            "front_frame_horns_bumper_and_steering_area",
            "rear_mid_frame_rail_and_hard_line_detail",
        ),
        indirect_specific_components=("rear_axle_and_leaf_springs", "rear_axle_spring_hanger_and_crossmember", "steering_and_suspension_linkages"),
        notes="Body-off underside shots and May 1 post-brushing photos provide direct evidence for rails/crossmembers and supporting suspension context.",
    ),
    "body_mount_points_and_captive_nuts": EvidenceRule(
        direct_specific_components=("body_mount_and_crossmember_detail", "frame_and_mount_points", "frame_rail_body_mount_and_crossmember_detail"),
        indirect_specific_components=("frame_floor_underside_and_lines",),
        notes="Mount pedestal and frame-mount photos support thread/captive-nut condition checks before refit.",
    ),
    "chassis_hard_lines_and_brackets": EvidenceRule(
        direct_specific_components=("frame_floor_underside_and_lines", "rear_mid_frame_rail_and_hard_line_detail"),
        indirect_specific_components=("rear_axle_and_leaf_springs", "front_frame_horns_bumper_and_steering_area", "steering_and_suspension_linkages"),
        notes="Underbody routing photos and May 1 hard-line/rail shots give direct visibility to line paths/brackets and nearby support hardware.",
    ),
    "issue_steering_box_mount_crack_check": EvidenceRule(
        direct_specific_components=("steering_and_suspension_linkages", "front_frame_horns_bumper_and_steering_area"),
        indirect_specific_components=("suspension_or_linkage_mount", "frame_and_mount_points"),
        notes="Steering linkage and nearby mount photos are the baseline evidence set for steering-box mount crack checks.",
    ),
    "issue_front_spring_hanger_crack_check": EvidenceRule(
        direct_specific_components=("rear_axle_and_leaf_springs", "rear_axle_spring_hanger_and_crossmember", "suspension_or_linkage_mount"),
        indirect_specific_components=("frame_and_mount_points",),
        notes="Spring and hanger views provide direct evidence for crack/deformation checks around hanger brackets.",
    ),
    "issue_crossmember_end_thinning_check": EvidenceRule(
        direct_specific_components=("rear_frame_crossmember_and_mounts", "body_mount_and_crossmember_detail", "frame_rail_body_mount_and_crossmember_detail", "rear_mid_frame_rail_and_hard_line_detail"),
        indirect_specific_components=("frame_and_mount_points", "frame_floor_underside_and_lines", "front_frame_horns_bumper_and_steering_area"),
        notes="Crossmember and mount-detail photos are used to inspect end-wall thinning and edge corrosion.",
    ),
    "issue_body_mount_captive_thread_repair": EvidenceRule(
        direct_specific_components=("body_mount_and_crossmember_detail", "frame_and_mount_points", "frame_rail_body_mount_and_crossmember_detail"),
        indirect_specific_components=("frame_floor_underside_and_lines",),
        notes="Body-mount pedestal and mount-point photos cover captive-nut and sleeve/thread repair planning.",
    ),
    "issue_brake_fuel_line_clip_corrosion": EvidenceRule(
        direct_specific_components=("frame_floor_underside_and_lines", "rear_mid_frame_rail_and_hard_line_detail"),
        indirect_specific_components=("rear_axle_and_leaf_springs", "front_frame_horns_bumper_and_steering_area", "steering_and_suspension_linkages"),
        notes="Underbody line-routing photos and May 1 rail/hard-line details are the primary evidence for clip/bracket corrosion and hard-line condition checks.",
    ),
    "brake_system_evidence_pack": EvidenceRule(
        direct_specific_components=(
            "frame_and_mount_points",
            "frame_floor_underside_and_lines",
            "rear_axle_and_leaf_springs",
            "steering_and_suspension_linkages",
        ),
        indirect_specific_components=("suspension_or_linkage_mount",),
        notes="Brake evidence pack combines direct front/rear axle hardware views with underbody hard-line photos and supporting underside context.",
    ),
    "front_brake_disc_baseline": EvidenceRule(
        direct_specific_components=("steering_and_suspension_linkages",),
        indirect_specific_components=("frame_and_mount_points", "suspension_or_linkage_mount"),
        notes="Steering-linkage underside photos are the closest grouped direct evidence, with frame/mount shots providing supporting context for the current front disc inference.",
    ),
    "rear_brake_drum_baseline": EvidenceRule(
        direct_specific_components=("rear_axle_and_leaf_springs",),
        indirect_specific_components=("frame_floor_underside_and_lines",),
        notes="Rear axle underside shots are the main evidence set for drum hardware and parking-brake linkage condition.",
    ),
    "rear_brake_cable_line_refresh": EvidenceRule(
        direct_specific_components=("rear_axle_and_leaf_springs",),
        indirect_specific_components=("frame_floor_underside_and_lines", "rear_mid_frame_rail_and_hard_line_detail", "rear_axle_spring_hanger_and_crossmember"),
        notes="Rear axle/drum photos directly show the parking-brake cable/linkage and axle-end hard-line routing; release still needs labelled removal photos and old parts kept as templates.",
    ),
    "rear_differential_axle_inspection_20260517": EvidenceRule(
        direct_specific_components=("rear_differential_carrier_and_axle_housing", "rear_axle_and_leaf_springs"),
        indirect_specific_components=("rear_axle_spring_hanger_and_crossmember", "frame_floor_underside_and_lines", "rear_mid_frame_rail_and_hard_line_detail"),
        notes="User-supplied May 17 differential carrier/pumpkin close-up triggers a rear differential/axle teardown inspection plan; existing rear axle, brake-line, and spring photos provide supporting route and access context. Closure needs DIFF-CAPTURE-001 with oil/debris, breather, carrier sealing, gear teeth, axle seal/bearing, fill, and leak-check evidence.",
        direct_media_ids=("20260517_230500_user_rear_differential_carrier_cover",),
    ),
    "brake_hydraulic_refresh_and_bias_decision": EvidenceRule(
        direct_specific_components=("frame_floor_underside_and_lines",),
        indirect_specific_components=("rear_axle_and_leaf_springs", "steering_and_suspension_linkages"),
        notes="Hard-line routing photos are direct evidence for hose/line refresh planning, with axle-end hardware views supporting brake-bias and wear decisions.",
    ),
    "suspension_upgrade_spec_and_kit_lock": EvidenceRule(
        direct_specific_components=(),
        indirect_specific_components=("rear_axle_and_leaf_springs", "rear_axle_spring_hanger_and_crossmember", "steering_and_suspension_linkages"),
        notes="Vehicle-side suspension photos support fitment constraints only; the kit lock still needs part-number, quantity, and arrived-condition photos for the actual suspension kit.",
    ),
    "suspension_upgrade_fitment_and_alignment": EvidenceRule(
        direct_specific_components=("rear_axle_and_leaf_springs", "rear_axle_spring_hanger_and_crossmember", "steering_and_suspension_linkages"),
        indirect_specific_components=("front_frame_horns_bumper_and_steering_area", "frame_and_mount_points"),
        notes="Rear spring/U-bolt and front linkage photos provide direct fitment context; final alignment release still needs installed-kit and ride-height/alignment photos.",
    ),
    "eps_vitz_column_layout_measurement": EvidenceRule(
        direct_specific_components=("j40_removed_steering_column_set", "driver_footwell_firewall_and_wiring", "front_frame_horns_bumper_and_steering_area", "steering_and_suspension_linkages"),
        indirect_specific_components=("dashboard_lower_structure", "floor_pan_and_firewall", "floor_pan_rust_zones"),
        notes="Existing cab/firewall, removed J40 column, and steering-box-side photos provide the vehicle-side EPS layout baseline; close this only with ruler photos, donor EPS mock-up, motor envelope, and column centerline checks.",
    ),
    "eps_vitz_support_bracket_design": EvidenceRule(
        direct_specific_components=("driver_footwell_firewall_and_wiring", "dashboard_lower_structure", "floor_pan_rust_zones"),
        indirect_specific_components=("front_frame_horns_bumper_and_steering_area",),
        notes="Cab/firewall and dash-structure photos support bracket design context, but final support plates need measured templates and dry-fit photos before fabrication.",
    ),
    "eps_vitz_shaft_u_joint_adaptation": EvidenceRule(
        direct_specific_components=("front_frame_horns_bumper_and_steering_area", "steering_and_suspension_linkages"),
        indirect_specific_components=("driver_footwell_firewall_and_wiring",),
        notes="Steering-box/input and linkage photos provide direct vehicle-side shaft-routing context; release still needs donor shaft, U-joint, spline, engagement, and phasing evidence.",
    ),
    "eps_vitz_controller_mount_and_wiring": EvidenceRule(
        direct_specific_components=("fuse_distribution_and_power_hardware", "driver_footwell_firewall_and_wiring", "firewall_and_dash_wiring"),
        indirect_specific_components=("wiring_harness_and_fuse_distribution", "pedal_box_wiring", "driver_footwell_firewall_pass_through"),
        notes="Existing wiring and footwell photos support controller and power-route planning; close only after the matched ECU/controller, plugs, fuse feed, ground, and ignition-trigger wiring are photographed and labelled.",
    ),
    "issue_chassis_ground_points_refresh": EvidenceRule(
        direct_specific_components=("frame_floor_underside_and_lines", "frame_rail_body_mount_and_crossmember_detail"),
        indirect_specific_components=("front_frame_horns_bumper_and_steering_area", "steering_and_suspension_linkages", "driver_footwell_firewall_and_wiring"),
        notes="Frame and lower bay views provide context for grounding point cleanup and re-termination planning.",
    ),
    "chassis_wire_brush_status_20260501": EvidenceRule(
        direct_specific_components=(
            "frame_rail_body_mount_and_crossmember_detail",
            "front_frame_horns_bumper_and_steering_area",
            "rear_axle_spring_hanger_and_crossmember",
            "rear_mid_frame_rail_and_hard_line_detail",
        ),
        indirect_specific_components=("engine_powertrain_cleaning_baseline",),
        notes="May 1 photos directly document the current post-wire-brushing chassis state and the remaining rust-prep closeout zones.",
    ),
    "chassis_missing_welded_bracket_survey_20260508": EvidenceRule(
        direct_specific_components=(
            "front_frame_horns_bumper_and_radiator_support",
            "front_frame_horns_bumper_and_steering_area",
            "frame_rail_body_mount_and_crossmember_detail",
            "frame_rail_body_mount_and_hard_line_detail",
            "rear_mid_frame_rail_and_hard_line_detail",
        ),
        indirect_specific_components=("engine_bay_chassis_interface", "engine_powertrain_cleaning_baseline"),
        notes="Existing body-off chassis photos provide the survey baseline, but the task remains open until current close-ups label every missing, wire-tied, or required bracket.",
    ),
    "chassis_bracket_analysis_register_20260508": EvidenceRule(
        direct_specific_components=(
            "front_support_radiator_pickups_context",
            "battery_side_tray_structure_context",
            "front_frame_horns_bumper_and_radiator_support",
            "front_frame_horns_bumper_and_steering_area",
            "frame_rail_body_mount_and_crossmember_detail",
            "frame_rail_body_mount_and_hard_line_detail",
            "rear_mid_frame_rail_and_hard_line_detail",
        ),
        indirect_specific_components=("engine_bay_chassis_interface", "engine_powertrain_cleaning_baseline"),
        notes="Use the existing body-off chassis photos as baseline evidence, then close this row only after a station-by-station bracket register records function, condition, evidence, and coating impact.",
    ),
    "chassis_bracket_design_release_20260508": EvidenceRule(
        direct_specific_components=(
            "front_support_radiator_pickups_context",
            "battery_side_tray_structure_context",
            "front_frame_horns_bumper_and_radiator_support",
            "front_frame_horns_bumper_and_steering_area",
            "frame_rail_body_mount_and_hard_line_detail",
            "rear_mid_frame_rail_and_hard_line_detail",
        ),
        indirect_specific_components=("frame_rail_body_mount_and_crossmember_detail", "engine_bay_chassis_interface", "engine_bay_overview"),
        notes="Location photos support the bracket design baseline, but released sketches/templates with material, hole/stud, bend, datum, and clearance decisions are still required before fabrication.",
    ),
    "chassis_bracket_fabrication_install_20260508": EvidenceRule(
        direct_specific_components=(
            "front_frame_horns_bumper_and_radiator_support",
            "front_frame_horns_bumper_and_steering_area",
            "frame_rail_body_mount_and_hard_line_detail",
            "rear_mid_frame_rail_and_hard_line_detail",
        ),
        indirect_specific_components=("engine_bay_chassis_interface", "engine_powertrain_cleaning_baseline"),
        notes="Current photos provide pre-work baseline only; closure needs post-install labelled photos and trial-fit evidence before primer/Raptor.",
    ),
    "chassis_bracket_validation_release_20260508": EvidenceRule(
        direct_specific_components=(
            "front_frame_horns_bumper_and_radiator_support",
            "front_frame_horns_bumper_and_steering_area",
            "frame_rail_body_mount_and_crossmember_detail",
            "frame_rail_body_mount_and_hard_line_detail",
            "rear_mid_frame_rail_and_hard_line_detail",
        ),
        indirect_specific_components=("engine_bay_chassis_interface", "engine_powertrain_cleaning_baseline"),
        notes="Baseline photos support the validation checklist; final release still requires labelled installed-bracket photos and dry-fit checks for radiator, battery, line/harness/ground, and exhaust interfaces.",
    ),
    "front_radiator_bracket_repair_20260508": EvidenceRule(
        direct_specific_components=("front_support_radiator_pickups_context", "front_frame_horns_bumper_and_radiator_support", "cooling_hoses_fan_belt_and_radiator_support"),
        indirect_specific_components=("engine_bay_chassis_interface", "engine_bay_overview"),
        notes="Front support and cooling-route photos are the baseline for the wire-held radiator support repair; the May 12 upright/crossmember view starts the pickup layout, but closure still needs ruler photos, trial-fit, and bracket close-ups.",
    ),
    "front_radiator_two_side_retention_fabrication_20260508": EvidenceRule(
        direct_specific_components=("front_support_radiator_pickups_context", "front_frame_horns_bumper_and_radiator_support", "cooling_hoses_fan_belt_and_radiator_support"),
        indirect_specific_components=("engine_bay_chassis_interface", "engine_bay_overview"),
        notes="Radiator/front-support photos directly show the radiator support location and fan-clearance context; the May 12 view adds the visible upright and crossmember hole field, while final hole centres and bracket offsets still need ruler photos or dry-fit.",
    ),
    "battery_tray_holder_bracket_repair_20260508": EvidenceRule(
        direct_specific_components=(
            "battery_side_tray_structure_context",
            "installed_battery_dimension_reference",
            "existing_battery_mount_tray_measurements",
        ),
        indirect_specific_components=("engine_bay_overview", "engine_bay_chassis_interface", "engine_powertrain_cleaning_baseline"),
        notes="Engine-bay overview photos show the battery-side location; May 17 adds actual installed-battery dimension and existing tray/mount ruler evidence, while underside foot condition and dry-fit pickup templates still need closure.",
    ),
    "battery_power_carrier_mount_fabrication_20260508": EvidenceRule(
        direct_specific_components=(
            "battery_side_tray_structure_context",
            "installed_battery_dimension_reference",
            "existing_battery_mount_tray_measurements",
        ),
        indirect_specific_components=("engine_bay_overview", "engine_bay_chassis_interface"),
        notes="Procurement photos document the MIDI/cutoff hardware separately; May 17 battery and existing tray measurements now provide the real carrier datum, but cardboard/flat-bar mock-up and final pickup release photos are still required before cutting.",
    ),
    "engine_bay_mounting_scouting_pass_20260508": EvidenceRule(
        direct_specific_components=(
            "front_support_radiator_pickups_context",
            "battery_side_tray_structure_context",
            "installed_battery_dimension_reference",
            "existing_battery_mount_tray_measurements",
            "front_frame_horns_bumper_and_radiator_support",
            "cooling_hoses_fan_belt_and_radiator_support",
            "engine_bay_overview",
        ),
        indirect_specific_components=("engine_bay_chassis_interface", "fuse_distribution_and_power_hardware", "hidden_diesel_cutoff_switch_hardware"),
        notes="Current photos are enough to start the radiator/battery/power-carrier plan; May 17 imports actual battery and tray/mount measurements, while cardboard mock-up, cable sweep, and pickup release checks remain open.",
    ),
    "auxiliary_chassis_tabs_and_clip_brackets_20260508": EvidenceRule(
        direct_specific_components=("frame_rail_body_mount_and_hard_line_detail", "rear_mid_frame_rail_and_hard_line_detail"),
        indirect_specific_components=("front_frame_horns_bumper_and_steering_area", "engine_bay_chassis_interface"),
        notes="Hard-line and frame-rail photos show existing clip/tab areas; current audit photos are still required before deciding which auxiliary tabs to weld.",
    ),
    "exhaust_mockup_brackets_before_coating_20260508": EvidenceRule(
        direct_specific_components=(),
        indirect_specific_components=("engine_bay_chassis_interface", "engine_powertrain_cleaning_baseline", "frame_rail_body_mount_and_crossmember_detail"),
        notes="Current photo inventory has no dedicated exhaust mock-up evidence; chassis and engine-bay photos only support routing context.",
    ),
    "engine_powertrain_cleaning_20260501": EvidenceRule(
        direct_specific_components=("engine_powertrain_cleaning_baseline",),
        indirect_specific_components=("front_frame_horns_bumper_and_steering_area", "rear_mid_frame_rail_and_hard_line_detail"),
        notes="May 1 engine, gearbox, transfer, steering, and driveline photos directly document the cleaning baseline before degreasing and leak inspection.",
    ),
    "wheel_tyre_condition_assessment_20260512": EvidenceRule(
        direct_specific_components=("wheel_tire_neolin_mt_tread_detail", "wheel_tire_neolin_mt_sidewall_rim_detail"),
        indirect_specific_components=("wheel_and_tire_detail", "steering_and_suspension_linkages"),
        notes="May 12 tyre/wheel photos show deep Neolin M/T tread and outer rim/sidewall condition, but roadworthy release still needs all-wheel DOT/date-code capture, inner sidewall inspection, bead/rim corrosion and runout check, pressure leak test, balance, and lug-seat/nut inspection.",
    ),
    "engine_cooling_pipe_fabrication_samples": EvidenceRule(
        direct_specific_components=("cooling_pipe_fabrication_samples",),
        indirect_specific_components=("cooling_hoses_fan_belt_and_radiator_support", "engine_powertrain_cleaning_baseline"),
        notes="May 2 selected pipe photos directly document the made-to-order cooling pipe sample set; engine-bay routing photos provide supporting context.",
    ),
    "replacement_pipe_ordering_matrix": EvidenceRule(
        direct_specific_components=(),
        indirect_specific_components=(),
        notes="Replacement pipe ordering is limited to selected pipe sample photos and close pipe/hose/line location evidence; body rubbers and broad chassis/mechanical context are excluded.",
        direct_media_ids=(
            "20260502_004044_gp_Hx4Yo0Qg",
            "20260502_004106_gp_wlYlUahA",
            "20260502_004120_gp_7Jw9Zyrg",
            "20260502_004133_gp_ZEpqmARA",
            "20260502_004139_gp_jt1dGw4A",
            "20260502_004145_gp_e8soxsyA",
            "20260430_220004_gp_C9oYiYmA",
            "20260430_215957_gp_2iBbUagw",
            "20260422_004306_gp_vGlNr2UA",
            "20260422_004311_gp_994KQ0Pw",
            "20260430_215939_gp_EjZ7u1ow",
            "20260502_005740_gp_Qiat03EQ",
        ),
    ),
    "tub_refit_rubber_hardware_shim_stack": EvidenceRule(
        direct_specific_components=("body_mount_and_crossmember_detail", "floor_seam_and_body_mount_rust"),
        indirect_specific_components=("frame_and_mount_points", "frame_floor_underside_and_lines"),
        notes="Mount-detail and tub-side body-mount rust photos give refit context; May 17 adds current tub-side captive/mount corrosion details, but final rubber/sample dimensions still need physical measurement.",
    ),
}


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def date_range(rows: list[dict[str, str]]) -> str:
    dates = sorted({row["captured_date"] for row in rows if row.get("captured_date")})
    if not dates:
        return ""
    if len(dates) == 1:
        return dates[0]
    return f"{dates[0]} to {dates[-1]}"


def reconcile() -> list[dict[str, str]]:
    component_jobs = load_csv(COMPONENT_JOBS_PATH)
    photo_rows = [
        row
        for row in load_csv(PHOTO_INVENTORY_PATH)
        if row.get("stage", "").strip().lower() not in NON_COMPONENT_EVIDENCE_STAGES
    ]

    by_specific: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_media_id: dict[str, dict[str, str]] = {}
    for row in photo_rows:
        by_specific[row["specific_component"]].append(row)
        media_id = row.get("media_id", "").strip()
        file_stem = Path(row.get("file_name", "")).stem
        if media_id:
            by_media_id[media_id] = row
        if file_stem:
            by_media_id[file_stem] = row

    output_rows: list[dict[str, str]] = []
    for job in component_jobs:
        job_id = job["component_job_id"]
        rule = RULES.get(job_id, EvidenceRule((), (), "No explicit rule configured."))

        direct_matches: list[dict[str, str]] = []
        indirect_matches: list[dict[str, str]] = []

        for component in rule.direct_specific_components:
            direct_matches.extend(by_specific.get(component, []))
        for component in rule.indirect_specific_components:
            indirect_matches.extend(by_specific.get(component, []))
        for media_id in rule.direct_media_ids:
            row = by_media_id.get(media_id)
            if row:
                direct_matches.append(row)
        for media_id in rule.indirect_media_ids:
            row = by_media_id.get(media_id)
            if row:
                indirect_matches.append(row)

        direct_unique = {row["file_name"]: row for row in direct_matches}
        # Remove indirect duplicates that already appear in direct.
        indirect_unique = {
            row["file_name"]: row
            for row in indirect_matches
            if row["file_name"] not in direct_unique
        }

        if direct_unique:
            reconciliation_status = "direct_photo_evidence"
        elif indirect_unique:
            reconciliation_status = "indirect_photo_evidence_only"
        else:
            reconciliation_status = "no_photo_evidence"

        direct_rows = list(direct_unique.values())
        indirect_rows = list(indirect_unique.values())

        output_rows.append(
            {
                "component_job_id": job_id,
                "component_group": job["component_group"],
                "current_status": job["current_status"],
                "reconciliation_status": reconciliation_status,
                "direct_match_count": str(len(direct_rows)),
                "indirect_match_count": str(len(indirect_rows)),
                "direct_specific_components": "|".join(sorted({row["specific_component"] for row in direct_rows})),
                "indirect_specific_components": "|".join(sorted({row["specific_component"] for row in indirect_rows})),
                "direct_date_range": date_range(direct_rows),
                "indirect_date_range": date_range(indirect_rows),
                "example_direct_files": "|".join(sorted(row["file_name"] for row in direct_rows)[:8]),
                "example_indirect_files": "|".join(sorted(row["file_name"] for row in indirect_rows)[:8]),
                "notes": rule.notes,
            }
        )

    return output_rows


def write_csv(rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "component_job_id",
        "component_group",
        "current_status",
        "reconciliation_status",
        "direct_match_count",
        "indirect_match_count",
        "direct_specific_components",
        "indirect_specific_components",
        "direct_date_range",
        "indirect_date_range",
        "example_direct_files",
        "example_indirect_files",
        "notes",
    ]
    with OUTPUT_CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    status_order = {
        "no_photo_evidence": 0,
        "indirect_photo_evidence_only": 1,
        "direct_photo_evidence": 2,
    }
    sorted_rows = sorted(rows, key=lambda row: (status_order[row["reconciliation_status"]], row["component_job_id"]))

    lines: list[str] = []
    lines.append("# Component Jobs vs Photo Inventory Reconciliation")
    lines.append("")
    lines.append(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("- Source component jobs: `data/manual/component_jobs.csv`")
    lines.append("- Source photo inventory: `data/manual/photo_inventory.csv`")
    lines.append("- Output CSV: `data/manual/component_jobs_photo_reconciliation.csv`")
    lines.append("")
    lines.append("## Status Summary")
    lines.append("")
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        counts[row["reconciliation_status"]] += 1
    for key in ("direct_photo_evidence", "indirect_photo_evidence_only", "no_photo_evidence"):
        lines.append(f"- `{key}`: {counts.get(key, 0)}")
    lines.append("")
    lines.append("## Per-Component Results")
    lines.append("")
    lines.append("| Component Job | Status | Direct | Indirect | Direct Components | Notes |")
    lines.append("| --- | --- | ---: | ---: | --- | --- |")
    for row in sorted_rows:
        lines.append(
            f"| `{row['component_job_id']}` | `{row['reconciliation_status']}` | "
            f"{row['direct_match_count']} | {row['indirect_match_count']} | "
            f"`{row['direct_specific_components'] or '-'}` | {row['notes']} |"
        )

    OUTPUT_MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = reconcile()
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote reconciliation CSV: {OUTPUT_CSV_PATH.relative_to(ROOT)}")
    print(f"Wrote reconciliation report: {OUTPUT_MD_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
