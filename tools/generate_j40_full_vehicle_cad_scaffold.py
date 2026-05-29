from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path
import csv
import html
import json
import math
import struct

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "manual" / "cad" / "j40_reference_model" / "04_exports" / "scaffold_rev_b"
REPORT_DIR = ROOT / "data" / "manual" / "cad" / "j40_reference_model" / "05_reports"

MODEL_NAME = "j40_full_vehicle_scaffold_rev_b"
MODEL_TITLE = "J40 Full Vehicle CAD Scaffold Rev B - LHD Hardtop Detail Pass"
MODEL_SHORT_TITLE = "J40 full vehicle CAD scaffold Rev B"
DETAIL_REVISION = "lhd_detail_pass"
DRIVER_SIDE = "left"
DRIVER_Y_SIGN = -1
DRIVER_Y = -420
PASSENGER_Y = 420


@dataclass(frozen=True)
class BoxPart:
    group: str
    name: str
    x: float
    y: float
    z: float
    length: float
    width: float
    height: float
    color: str
    confidence: str
    notes: str


@dataclass(frozen=True)
class WheelPart:
    group: str
    name: str
    x: float
    y: float
    z: float
    diameter: float
    width: float
    color: str
    confidence: str
    notes: str


@dataclass(frozen=True)
class CylinderPart:
    group: str
    name: str
    x: float
    y: float
    z: float
    axis: str
    diameter: float
    length: float
    color: str
    confidence: str
    notes: str


PartType = BoxPart | WheelPart | CylinderPart


COLORS = {
    "body_sand": "#cfc6aa",
    "roof_white": "#f1eee4",
    "black_trim": "#111315",
    "frame": "#2d3033",
    "rubber": "#1d1d1d",
    "metal": "#b8b8b8",
    "interior": "#b87b55",
    "glass": "#6fa5b8",
    "engine": "#3f4245",
    "spring": "#222222",
    "reference": "#e8e8e8",
    "electrical": "#d64737",
    "fluid": "#4f7f55",
    "brass": "#c49a3d",
    "datum": "#7c6fcb",
}


def parts() -> list[PartType]:
    p: list[PartType] = []

    def box(
        group: str,
        name: str,
        x: float,
        y: float,
        z: float,
        length: float,
        width: float,
        height: float,
        color: str,
        confidence: str = "L0 envelope",
        notes: str = "",
    ) -> None:
        p.append(BoxPart(group, name, x, y, z, length, width, height, color, confidence, notes))

    def wheel(name: str, x: float, y: float, z: float, notes: str) -> None:
        p.append(
            WheelPart(
                "running_gear",
                name,
                x,
                y,
                z,
                790,
                250,
                COLORS["rubber"],
                "L0 envelope",
                notes,
            )
        )

    def cyl(
        group: str,
        name: str,
        x: float,
        y: float,
        z: float,
        axis: str,
        diameter: float,
        length: float,
        color: str,
        confidence: str = "L1 visible-detail primitive",
        notes: str = "",
    ) -> None:
        p.append(CylinderPart(group, name, x, y, z, axis, diameter, length, color, confidence, notes))

    # Published representative FJ40 dimensions from Toyota: 3840 L, 1665 W, 1950 H, 2285 WB.
    # Coordinate system: X front bumper to rear, Y centerline left/right, Z ground up, units mm.
    # This truck is modelled as left-hand drive: negative Y is the driver's side.
    front_axle_x = 735
    rear_axle_x = front_axle_x + 2285
    track_half = 705
    wheel_z = 395

    # Chassis and running gear.
    box("chassis", "left_frame_rail", 360, -390, 430, 3140, 85, 120, COLORS["frame"], notes="straight ladder-frame reference rail")
    box("chassis", "right_frame_rail", 360, 390, 430, 3140, 85, 120, COLORS["frame"], notes="straight ladder-frame reference rail")
    for idx, x in enumerate([450, 980, 1660, 2420, 3230], start=1):
        box("chassis", f"crossmember_{idx}", x, 0, 455, 85, 880, 95, COLORS["frame"], notes="crossmember station placeholder")
    box("chassis", "front_bumper", 20, 0, 525, 165, 1620, 120, COLORS["black_trim"], notes="black front bumper from project photos")
    box("chassis", "rear_bumper", 3665, 0, 530, 145, 1550, 110, COLORS["black_trim"], notes="black rear bumper envelope")
    cyl("chassis", "front_left_tow_ring", 75, -430, 450, "x", 115, 28, COLORS["metal"], notes="front bumper tow ring reference")
    cyl("chassis", "front_right_tow_ring", 75, 430, 450, "x", 115, 28, COLORS["metal"], notes="front bumper tow ring reference")
    box("running_gear", "front_axle_tube", front_axle_x, 0, 395, 90, 1560, 90, COLORS["metal"], notes="front live axle tube envelope")
    box("running_gear", "rear_axle_tube", rear_axle_x, 0, 395, 90, 1560, 90, COLORS["metal"], notes="rear live axle tube envelope")
    for x, label in [(front_axle_x, "front"), (rear_axle_x, "rear")]:
        box("running_gear", f"{label}_left_leaf_spring", x - 520, -430, 335, 1050, 65, 55, COLORS["spring"], notes="leaf spring pack envelope")
        box("running_gear", f"{label}_right_leaf_spring", x - 520, 430, 335, 1050, 65, 55, COLORS["spring"], notes="leaf spring pack envelope")
    wheel("front_left_tire", front_axle_x, -track_half, wheel_z, "tire/wheel cylinder, nominal 31 inch class")
    wheel("front_right_tire", front_axle_x, track_half, wheel_z, "tire/wheel cylinder, nominal 31 inch class")
    wheel("rear_left_tire", rear_axle_x, -track_half, wheel_z, "tire/wheel cylinder, nominal 31 inch class")
    wheel("rear_right_tire", rear_axle_x, track_half, wheel_z, "tire/wheel cylinder, nominal 31 inch class")
    for axle_x, axle_name in [(front_axle_x, "front"), (rear_axle_x, "rear")]:
        for side_name, y_sign in [("left", -1), ("right", 1)]:
            face_y = track_half * y_sign
            for lug_idx in range(16):
                angle = math.tau * lug_idx / 16
                lug_x = axle_x + math.cos(angle) * 375
                lug_z = wheel_z + math.sin(angle) * 375
                box(
                    "running_gear",
                    f"{axle_name}_{side_name}_mud_tire_outer_lug_{lug_idx + 1}",
                    lug_x,
                    face_y,
                    lug_z,
                    95,
                    48,
                    58,
                    COLORS["rubber"],
                    "L2 visible-detail primitive",
                    "blocky mud-terrain tread lug visible on project photos and Sketchfab reference",
                )
    for x, label in [(front_axle_x, "front"), (rear_axle_x, "rear")]:
        cyl("running_gear", f"{label}_left_shock_body", x + 185, -520, 620, "z", 58, 460, COLORS["metal"], notes="shock absorber body reference")
        cyl("running_gear", f"{label}_right_shock_body", x + 185, 520, 620, "z", 58, 460, COLORS["metal"], notes="shock absorber body reference")
        cyl("running_gear", f"{label}_left_hub_cap", x, -840, wheel_z, "y", 220, 80, COLORS["metal"], notes="wheel hub cap detail")
        cyl("running_gear", f"{label}_right_hub_cap", x, 840, wheel_z, "y", 220, 80, COLORS["metal"], notes="wheel hub cap detail")

    # Body lower structure.
    box("body", "floor_pan", 890, 0, 615, 2550, 1330, 55, COLORS["body_sand"], notes="main floor and rear tub floor envelope")
    box("body", "left_rocker_sill", 1000, -720, 665, 2050, 95, 155, COLORS["body_sand"], notes="left rocker/sill envelope")
    box("body", "right_rocker_sill", 1000, 720, 665, 2050, 95, 155, COLORS["body_sand"], notes="right rocker/sill envelope")
    box("body", "left_rear_quarter_panel", 2140, -760, 725, 1270, 70, 610, COLORS["body_sand"], notes="rear tub side panel below hardtop")
    box("body", "right_rear_quarter_panel", 2140, 760, 725, 1270, 70, 610, COLORS["body_sand"], notes="rear tub side panel below hardtop")
    box("body", "tailgate_panel", 3400, 0, 720, 70, 1430, 650, COLORS["body_sand"], notes="tailgate/rear body closing panel")
    box("body", "firewall", 1135, 0, 690, 80, 1420, 780, COLORS["body_sand"], notes="firewall plane and cowl station")
    box("body", "cowl_top", 1085, 0, 1260, 190, 1460, 110, COLORS["body_sand"], notes="scuttle/cowl top envelope")
    box("body", "grille_panel", 170, 0, 790, 80, 1410, 520, COLORS["body_sand"], notes="front grille plane")
    box("front_detail", "white_grille_surround", 125, 0, 795, 35, 1120, 365, COLORS["reference"], notes="white front grille surround visible in reference")
    box("front_detail", "black_grille_mesh", 105, 0, 910, 30, 640, 155, COLORS["rubber"], notes="black mesh grille area")
    cyl("front_detail", "left_headlamp", 92, -445, 985, "x", 225, 38, COLORS["reference"], notes="round front headlamp")
    cyl("front_detail", "right_headlamp", 92, 445, 985, "x", 225, 38, COLORS["reference"], notes="round front headlamp")
    cyl("front_detail", "left_indicator_lamp", 84, -720, 845, "x", 105, 30, COLORS["interior"], notes="front amber indicator")
    cyl("front_detail", "right_indicator_lamp", 84, 720, 845, "x", 105, 30, COLORS["interior"], notes="front amber indicator")
    cyl("front_detail", "left_fog_lamp", 25, -360, 620, "x", 165, 36, COLORS["reference"], notes="bumper-mounted round fog lamp")
    cyl("front_detail", "right_fog_lamp", 25, 360, 620, "x", 165, 36, COLORS["reference"], notes="bumper-mounted round fog lamp")
    box("body", "hood_closed_reference", 230, 0, 1215, 920, 1390, 55, COLORS["body_sand"], notes="closed hood reference envelope")
    box("body", "hood_open_visual_reference", 420, 0, 1420, 1180, 1390, 35, COLORS["body_sand"], "visual only", "viewer can show hood-open context; this is a non-kinematic slab reference")
    cyl("body", "hood_left_hinge_axis", 1030, -540, 1288, "y", 28, 230, COLORS["metal"], notes="hood hinge axis placeholder")
    cyl("body", "hood_right_hinge_axis", 1030, 540, 1288, "y", 28, 230, COLORS["metal"], notes="hood hinge axis placeholder")
    box("body", "left_front_fender", 270, -720, 760, 860, 270, 260, COLORS["body_sand"], notes="front wing/fender envelope")
    box("body", "right_front_fender", 270, 720, 760, 860, 270, 260, COLORS["body_sand"], notes="front wing/fender envelope")
    box("body", "left_inner_fender", 290, -520, 800, 800, 70, 420, COLORS["body_sand"], notes="engine-bay inner fender placeholder")
    box("body", "right_inner_fender", 290, 520, 800, 800, 70, 420, COLORS["body_sand"], notes="engine-bay inner fender placeholder")

    # Cabin and hardtop.
    box("body", "windshield_frame", 1155, 0, 1315, 80, 1480, 520, COLORS["body_sand"], notes="upright windshield frame envelope")
    box("body", "windshield_glass", 1160, 0, 1380, 35, 1300, 410, COLORS["glass"], notes="transparent windshield opening reference")
    cyl("body", "windshield_left_wiper", 1110, -250, 1370, "y", 24, 430, COLORS["rubber"], notes="windshield wiper reference")
    cyl("body", "windshield_right_wiper", 1110, 250, 1370, "y", 24, 430, COLORS["rubber"], notes="windshield wiper reference")
    box("hard_top", "white_hardtop_roof", 1210, 0, 1845, 2290, 1540, 110, COLORS["roof_white"], notes="white hardtop roof from project photos and CC-BY reference")
    box("hard_top", "left_hardtop_side_panel", 1240, -790, 1320, 2200, 55, 590, COLORS["body_sand"], notes="left hardtop side shell")
    box("hard_top", "right_hardtop_side_panel", 1240, 790, 1320, 2200, 55, 590, COLORS["body_sand"], notes="right hardtop side shell")
    box("hard_top", "left_front_hardtop_window", 1420, -823, 1435, 500, 20, 320, COLORS["glass"], notes="left sliding/side hardtop window glass")
    box("hard_top", "left_rear_hardtop_window", 2190, -823, 1435, 610, 20, 320, COLORS["glass"], notes="left rear hardtop side window glass")
    box("hard_top", "right_front_hardtop_window", 1420, 823, 1435, 500, 20, 320, COLORS["glass"], notes="right sliding/side hardtop window glass")
    box("hard_top", "right_rear_hardtop_window", 2190, 823, 1435, 610, 20, 320, COLORS["glass"], notes="right rear hardtop side window glass")
    box("hard_top", "rear_hardtop_panel", 3440, 0, 1320, 55, 1540, 590, COLORS["body_sand"], notes="rear hardtop panel")
    box("hard_top", "roof_front_gutter", 1160, 0, 1810, 70, 1575, 46, COLORS["roof_white"], notes="hardtop gutter at windshield header")
    box("hard_top", "roof_left_gutter", 2250, -830, 1815, 2200, 58, 42, COLORS["roof_white"], notes="left roof gutter")
    box("hard_top", "roof_right_gutter", 2250, 830, 1815, 2200, 58, 42, COLORS["roof_white"], notes="right roof gutter")
    box("body", "left_door_open_reference", 1180, -910, 760, 800, 70, 850, COLORS["body_sand"], "visual only", "project photos show the left door removed/open during rebuild; final hinge arc requires measurements")
    box("body", "right_door_closed_reference", 1180, 760, 760, 800, 70, 850, COLORS["body_sand"], notes="right door closed envelope")
    box("body", "left_door_window_glass", 1280, -948, 1210, 520, 22, 345, COLORS["glass"], notes="open door window glass/reference aperture")
    box("body", "right_door_window_glass", 1280, 798, 1210, 520, 22, 345, COLORS["glass"], notes="closed door window glass/reference aperture")
    cyl("body", "left_upper_door_hinge", 1135, -955, 1180, "z", 38, 145, COLORS["metal"], notes="door hinge barrel reference")
    cyl("body", "left_lower_door_hinge", 1135, -955, 850, "z", 38, 145, COLORS["metal"], notes="door hinge barrel reference")
    cyl("body", "right_upper_door_hinge", 1135, 805, 1180, "z", 38, 145, COLORS["metal"], notes="door hinge barrel reference")
    cyl("body", "right_lower_door_hinge", 1135, 805, 850, "z", 38, 145, COLORS["metal"], notes="door hinge barrel reference")
    box("body", "left_door_handle", 1575, -955, 1045, 160, 30, 40, COLORS["metal"], notes="door handle reference")
    box("body", "right_door_handle", 1575, 805, 1045, 160, 30, 40, COLORS["metal"], notes="door handle reference")

    # Engine bay and interior placeholders.
    box("engine_bay", "engine_block", 460, 0, 720, 520, 420, 430, COLORS["engine"], notes="inline-six engine block envelope")
    box("engine_bay", "valve_cover", 510, 0, 1080, 460, 180, 70, COLORS["metal"], notes="visible valve cover reference")
    box("engine_bay", "radiator", 235, 0, 820, 75, 980, 520, COLORS["engine"], notes="radiator support package")
    box("engine_bay", "air_filter", 760, -235, 1120, 210, 210, 150, COLORS["engine"], notes="air-filter canister envelope")
    box("engine_bay", "battery_tray_reference", 600, 430, 760, 330, 220, 220, COLORS["reference"], notes="battery/package reference, placement to verify")
    for idx, y in enumerate([-165, -99, -33, 33, 99, 165], start=1):
        cyl("engine_bay", f"inline_six_intake_stack_{idx}", 470, y, 1160, "z", 46, 180, COLORS["metal"], notes="inline-six visible engine top detail")
    cyl("engine_bay", "upper_radiator_hose", 330, -185, 1110, "x", 72, 430, COLORS["rubber"], notes="upper radiator hose placeholder")
    cyl("engine_bay", "exhaust_downpipe_reference", 615, 255, 845, "z", 82, 460, COLORS["metal"], notes="engine bay pipe reference")
    box("interior", "dashboard", 1235, 0, 1080, 120, 1320, 220, COLORS["interior"], notes="dashboard envelope from visible interior")
    box("interior", "steering_column", 1135, DRIVER_Y, 935, 590, 60, 60, COLORS["metal"], notes="steering column envelope, left-hand-drive driver side")
    cyl("interior", "steering_wheel", 1240, DRIVER_Y, 1210, "x", 380, 32, COLORS["rubber"], notes="steering wheel disk placeholder on left-hand-drive side")
    cyl("interior", "steering_wheel_hub", 1230, DRIVER_Y, 1210, "x", 135, 55, COLORS["metal"], notes="steering wheel hub")
    for idx, y in enumerate([-560, -470, -380, -290], start=1):
        cyl("interior", f"dashboard_gauge_{idx}", 1222, y, 1175, "x", 72, 24, COLORS["reference"], notes="round dashboard gauge")
    cyl("interior", "transfer_case_lever", 1580, -120, 820, "z", 36, 285, COLORS["metal"], notes="transfer-case lever")
    cyl("interior", "gearshift_lever", 1500, -35, 820, "z", 38, 330, COLORS["metal"], notes="gearshift lever")
    box("interior", "front_left_seat_base", 1660, -310, 700, 420, 410, 130, COLORS["interior"], notes="front seat base")
    box("interior", "front_left_seat_back", 1850, -310, 820, 95, 410, 620, COLORS["interior"], notes="front seat back")
    cyl("interior", "front_left_headrest", 1905, -310, 1435, "y", 150, 300, COLORS["interior"], notes="front headrest")
    box("interior", "front_right_seat_base", 1660, 310, 700, 420, 410, 130, COLORS["interior"], notes="front seat base")
    box("interior", "front_right_seat_back", 1850, 310, 820, 95, 410, 620, COLORS["interior"], notes="front seat back")
    cyl("interior", "front_right_headrest", 1905, 310, 1435, "y", 150, 300, COLORS["interior"], notes="front headrest")
    box("interior", "rear_bench_base", 2510, 0, 720, 610, 1080, 135, COLORS["interior"], notes="rear bench lower cushion")
    box("interior", "rear_bench_back", 2920, 0, 840, 105, 1080, 560, COLORS["interior"], notes="rear bench back")
    cyl("interior", "rear_bench_left_headrest", 2975, -350, 1390, "y", 140, 270, COLORS["interior"], notes="rear headrest")
    cyl("interior", "rear_bench_right_headrest", 2975, 350, 1390, "y", 140, 270, COLORS["interior"], notes="rear headrest")

    # Detail pass. These are still reference primitives, but they turn the
    # scaffold into a usable subsystem map instead of a simple envelope model.
    side_pairs = [("left", -1, -1.0), ("right", 1, 1.0)]

    # Chassis hard points, outriggers, spring mounts, and underside packaging.
    for side, sign, y_sign in side_pairs:
        rail_y = 390 * y_sign
        outer_y = 615 * y_sign
        hanger_y = 475 * y_sign
        box("chassis", f"{side}_front_frame_horn_top_plate", 120, rail_y, 555, 500, 95, 24, COLORS["frame"], "L2 bracket reference", "front frame horn top reinforcement")
        box("chassis", f"{side}_front_frame_horn_side_web", 120, rail_y + 58 * y_sign, 440, 500, 18, 150, COLORS["frame"], "L2 bracket reference", "front frame horn outside web")
        box("chassis", f"{side}_rear_frame_horn_top_plate", 3230, rail_y, 555, 420, 95, 24, COLORS["frame"], "L2 bracket reference", "rear frame horn top reinforcement")
        box("chassis", f"{side}_rear_frame_horn_side_web", 3230, rail_y + 58 * y_sign, 440, 420, 18, 145, COLORS["frame"], "L2 bracket reference", "rear frame horn outside web")
        for idx, x in enumerate([740, 1135, 1610, 2250, 2920], start=1):
            box("chassis", f"{side}_body_mount_outrigger_{idx}", x, 525 * y_sign, 525, 280, 70, 55, COLORS["frame"], "L2 bracket reference", "body mount outrigger arm")
            cyl("chassis", f"{side}_body_mount_rubber_biscuit_{idx}", x + 225, outer_y, 610, "z", 118, 42, COLORS["rubber"], "L2 service datum", "rubber body mount stack placeholder")
            cyl("chassis", f"{side}_body_mount_center_bolt_{idx}", x + 225, outer_y, 632, "z", 30, 70, COLORS["metal"], "L2 service datum", "body mount bolt datum")
        for label, x in [
            ("front_fixed", front_axle_x - 525),
            ("front_shackle", front_axle_x + 545),
            ("rear_fixed", rear_axle_x - 525),
            ("rear_shackle", rear_axle_x + 545),
        ]:
            box("chassis", f"{side}_{label}_spring_hanger_outer_plate", x, hanger_y, 360, 105, 28, 180, COLORS["frame"], "L2 bracket reference", "leaf spring hanger side plate")
            box("chassis", f"{side}_{label}_spring_hanger_inner_plate", x, rail_y, 360, 105, 28, 180, COLORS["frame"], "L2 bracket reference", "leaf spring hanger inner plate")
            cyl("chassis", f"{side}_{label}_spring_pin", x + 52, (hanger_y + rail_y) / 2, 430, "y", 42, 130, COLORS["metal"], "L2 service datum", "leaf spring pin or shackle bolt")
        for idx, x in enumerate([980, 1660, 2420], start=1):
            box("chassis", f"{side}_crossmember_{idx}_gusset_front", x - 82, rail_y, 465, 38, 230, 90, COLORS["frame"], "L2 bracket reference", "crossmember gusset plate")
            box("chassis", f"{side}_crossmember_{idx}_gusset_rear", x + 126, rail_y, 465, 38, 230, 90, COLORS["frame"], "L2 bracket reference", "crossmember gusset plate")
        box("running_gear", f"{side}_front_upper_shock_mount", front_axle_x + 210, 575 * y_sign, 875, 115, 110, 135, COLORS["frame"], "L2 bracket reference", "front shock tower envelope")
        box("running_gear", f"{side}_rear_upper_shock_mount", rear_axle_x + 165, 575 * y_sign, 875, 115, 110, 135, COLORS["frame"], "L2 bracket reference", "rear shock tower envelope")
        cyl("running_gear", f"{side}_front_shock_piston_rod", front_axle_x + 185, 520 * y_sign, 850, "z", 24, 280, COLORS["metal"], "L2 visible-detail primitive", "shock absorber polished rod")
        cyl("running_gear", f"{side}_rear_shock_piston_rod", rear_axle_x + 185, 520 * y_sign, 850, "z", 24, 280, COLORS["metal"], "L2 visible-detail primitive", "shock absorber polished rod")
        box("running_gear", f"{side}_front_bump_stop", front_axle_x - 95, 495 * y_sign, 540, 115, 80, 72, COLORS["rubber"], "L2 service datum", "front axle bump stop")
        box("running_gear", f"{side}_rear_bump_stop", rear_axle_x - 95, 495 * y_sign, 540, 115, 80, 72, COLORS["rubber"], "L2 service datum", "rear axle bump stop")

    box("chassis", "transfer_case_crossmember", 1710, 0, 500, 260, 940, 120, COLORS["frame"], "L2 bracket reference", "transmission and transfer case support")
    box("chassis", "skid_plate_transfer_case", 1600, 0, 315, 520, 620, 42, COLORS["metal"], "L2 underbody reference", "transfer-case skid plate")
    box("running_gear", "transfer_case", 1640, 0, 575, 410, 360, 265, COLORS["engine"], "L2 underbody reference", "transfer case envelope")
    box("running_gear", "gearbox_tail_housing", 1325, 0, 610, 430, 300, 260, COLORS["engine"], "L2 underbody reference", "gearbox tail housing")
    cyl("running_gear", "front_prop_shaft", 1120, 0, 465, "x", 82, 900, COLORS["metal"], "L2 underbody reference", "front prop shaft envelope")
    cyl("running_gear", "rear_prop_shaft", 2180, 0, 465, "x", 82, 1360, COLORS["metal"], "L2 underbody reference", "rear prop shaft envelope")
    cyl("running_gear", "front_diff_pumpkin", front_axle_x, 0, 420, "y", 360, 300, COLORS["metal"], "L2 visible-detail primitive", "front differential housing")
    cyl("running_gear", "rear_diff_pumpkin", rear_axle_x, 0, 420, "y", 380, 320, COLORS["metal"], "L2 visible-detail primitive", "rear differential housing")
    cyl("running_gear", "front_pinion_nose", front_axle_x + 185, 0, 430, "x", 145, 310, COLORS["metal"], "L2 visible-detail primitive", "front differential pinion nose")
    cyl("running_gear", "rear_pinion_nose", rear_axle_x - 240, 0, 430, "x", 145, 310, COLORS["metal"], "L2 visible-detail primitive", "rear differential pinion nose")
    box("chassis", "left_hand_drive_steering_box", 535, -515, 610, 245, 175, 230, COLORS["metal"], "L2 service datum", "left-hand-drive steering box on left frame rail")
    box("chassis", "steering_box_left_frame_mount_plate", 500, -445, 600, 295, 28, 260, COLORS["frame"], "L2 bracket reference", "steering box mounting plate on left rail")
    cyl("running_gear", "pitman_arm_left_hand_drive", 675, -555, 565, "z", 62, 250, COLORS["metal"], "L2 service datum", "pitman arm below LHD steering box")
    cyl("running_gear", "front_drag_link_left_hand_drive", 875, -555, 505, "x", 34, 620, COLORS["metal"], "L2 routing reference", "drag link from LHD steering box toward front axle")
    cyl("running_gear", "front_tie_rod", front_axle_x, 0, 505, "y", 32, 1420, COLORS["metal"], "L2 routing reference", "front axle tie rod across knuckles")
    cyl("running_gear", "steering_damper", 905, -350, 480, "x", 58, 520, COLORS["metal"], "L2 service datum", "front steering damper package")
    box("running_gear", "front_left_steering_knuckle_arm", front_axle_x + 120, -690, 475, 150, 58, 60, COLORS["metal"], "L2 service datum", "left steering knuckle arm")
    box("running_gear", "front_right_steering_knuckle_arm", front_axle_x + 120, 690, 475, 150, 58, 60, COLORS["metal"], "L2 service datum", "right steering knuckle arm")
    for axle_x, axle_name in [(front_axle_x, "front"), (rear_axle_x, "rear")]:
        cyl("running_gear", f"{axle_name}_left_brake_backing_plate", axle_x, -750, wheel_z, "y", 365, 55, COLORS["metal"], "L2 service datum", "brake backing plate at hub")
        cyl("running_gear", f"{axle_name}_right_brake_backing_plate", axle_x, 750, wheel_z, "y", 365, 55, COLORS["metal"], "L2 service datum", "brake backing plate at hub")
        for side, sign, y_sign in side_pairs:
            for leaf_idx, z in enumerate([305, 323, 341], start=1):
                box("running_gear", f"{axle_name}_{side}_leaf_spring_layer_{leaf_idx}", axle_x - 520, 430 * y_sign, z, 1050 - leaf_idx * 115, 78, 14, COLORS["spring"], "L2 visible-detail primitive", "stacked leaf spring layer")
            for u_idx, offset in enumerate([-65, 65], start=1):
                cyl("running_gear", f"{axle_name}_{side}_u_bolt_{u_idx}", axle_x + offset, 430 * y_sign, 405, "z", 24, 210, COLORS["metal"], "L2 service datum", "axle U-bolt reference")

    # Wheels: backing detail, lug nuts, and valve stems so each wheel is identifiable in FreeCAD.
    for axle_x, axle_name in [(front_axle_x, "front"), (rear_axle_x, "rear")]:
        for side_name, face_y, y_sign in [("left", -845, -1), ("right", 845, 1)]:
            cyl("running_gear", f"{axle_name}_{side_name}_outer_rim_ring", axle_x, face_y, wheel_z, "y", 455, 34, COLORS["metal"], "L2 visible-detail primitive", "outer wheel rim ring")
            cyl("running_gear", f"{axle_name}_{side_name}_inner_rim_shadow", axle_x, face_y + 10 * y_sign, wheel_z, "y", 315, 22, COLORS["rubber"], "L2 visible-detail primitive", "dark rim recess")
            cyl("running_gear", f"{axle_name}_{side_name}_valve_stem", axle_x + 130, face_y + 25 * y_sign, wheel_z + 145, "y", 22, 50, COLORS["rubber"], "L2 visible-detail primitive", "tire valve stem")
            for lug_idx, angle_deg in enumerate([0, 60, 120, 180, 240, 300], start=1):
                angle = math.radians(angle_deg)
                lug_x = axle_x + math.cos(angle) * 92
                lug_z = wheel_z + math.sin(angle) * 92
                cyl("running_gear", f"{axle_name}_{side_name}_lug_nut_{lug_idx}", lug_x, face_y + 32 * y_sign, lug_z, "y", 32, 36, COLORS["metal"], "L2 service datum", "six-lug wheel nut datum")

    # Brake and parking-brake routing, including the specific rear cable hardware now tracked separately.
    cyl("brake_system", "front_hard_line_left_frame_run", 1180, -338, 575, "x", 18, 1650, COLORS["metal"], "L2 routing reference", "front brake hard-line run along left rail")
    cyl("brake_system", "rear_hard_line_left_frame_run", 2320, -338, 575, "x", 18, 1500, COLORS["metal"], "L2 routing reference", "rear brake hard-line run along left rail")
    cyl("brake_system", "rear_axle_brake_line", rear_axle_x, 0, 520, "y", 18, 1280, COLORS["metal"], "L2 routing reference", "rear axle brake hard-line across axle")
    cyl("brake_system", "parking_brake_front_cable", 1630, -145, 545, "x", 22, 650, COLORS["rubber"], "L2 routing reference", "parking-brake front cable")
    box("brake_system", "parking_brake_equalizer_bar", 2295, 0, 548, 175, 46, 24, COLORS["metal"], "L3 specific item reference", "rear parking-brake cable equalizer hardware")
    cyl("brake_system", "parking_brake_equalizer_pivot_pin", 2380, 0, 548, "y", 26, 120, COLORS["metal"], "L3 specific item reference", "equalizer pivot pin datum")
    for side, sign, y_sign in side_pairs:
        cyl("brake_system", f"{side}_rear_parking_brake_cable", 2685, 360 * y_sign, 535, "x", 22, 760, COLORS["rubber"], "L3 specific item reference", "rear parking-brake cable branch")
        box("brake_system", f"{side}_parking_brake_clevis", 3035, 520 * y_sign, 548, 66, 32, 34, COLORS["brass"], "L3 specific item reference", "parking-brake clevis at rear brake arm")
        cyl("brake_system", f"{side}_parking_brake_return_spring", 2945, 520 * y_sign, 602, "x", 34, 170, COLORS["spring"], "L3 specific item reference", "parking-brake return spring envelope")
        box("brake_system", f"{side}_parking_brake_cable_clip_1", 2485, 430 * y_sign, 545, 38, 30, 34, COLORS["metal"], "L3 specific item reference", "parking-brake cable frame clip")
        box("brake_system", f"{side}_parking_brake_cable_clip_2", 2805, 470 * y_sign, 545, 38, 30, 34, COLORS["metal"], "L3 specific item reference", "parking-brake cable axle clip")

    # Body shell detail: floor ribs, wheel tubs, apertures, tailgate hardware, and rear spare carrier.
    box("body", "transmission_tunnel", 1250, 0, 660, 1100, 360, 235, COLORS["body_sand"], "L2 visible-detail primitive", "central transmission tunnel envelope")
    box("body", "rear_load_floor", 2060, 0, 690, 1180, 1230, 42, COLORS["body_sand"], "L2 visible-detail primitive", "rear load floor sheet")
    for idx, y in enumerate([-420, -210, 0, 210, 420], start=1):
        box("body", f"rear_floor_longitudinal_rib_{idx}", 2050, y, 740, 1230, 38, 42, COLORS["body_sand"], "L2 panel rib reference", "pressed rear floor longitudinal rib")
    for idx, x in enumerate([980, 1280, 1730, 2140, 2570, 3020], start=1):
        box("body", f"floor_cross_pressing_{idx}", x, 0, 735, 42, 1260, 34, COLORS["body_sand"], "L2 panel rib reference", "floor cross pressing")
    for side, sign, y_sign in side_pairs:
        box("body", f"{side}_front_wheel_arch_shadow", front_axle_x - 370, 735 * y_sign, 745, 740, 34, 405, COLORS["rubber"], "L2 visual aperture reference", "front wheel arch opening shadow")
        box("body", f"{side}_rear_wheel_arch_shadow", rear_axle_x - 330, 735 * y_sign, 745, 690, 34, 410, COLORS["rubber"], "L2 visual aperture reference", "rear wheel arch opening shadow")
        box("body", f"{side}_rear_inner_wheel_tub", rear_axle_x - 365, 505 * y_sign, 755, 750, 280, 385, COLORS["body_sand"], "L2 panel reference", "rear inner wheel tub envelope")
        box("body", f"{side}_tub_top_capping", 1960, 805 * y_sign, 1322, 1530, 105, 58, COLORS["body_sand"], "L2 panel reference", "rear tub top capping rail")
        box("body", f"{side}_door_outer_skin_lower_pressing", 1235, 790 * y_sign, 845, 725, 34, 105, COLORS["body_sand"], "L2 panel rib reference", "door lower pressed panel line")
        box("body", f"{side}_door_vertical_shut_gap_front", 1130, 824 * y_sign, 780, 18, 28, 780, COLORS["rubber"], "L2 aperture reference", "door front shut gap")
        box("body", f"{side}_door_vertical_shut_gap_rear", 1940, 824 * y_sign, 780, 18, 28, 780, COLORS["rubber"], "L2 aperture reference", "door rear shut gap")
        box("body", f"{side}_mirror_arm", 1210, 884 * y_sign, 1240, 210, 26, 32, COLORS["metal"], "L2 visible-detail primitive", "door mirror arm")
        box("body", f"{side}_door_mirror_head", 1405, 930 * y_sign, 1195, 135, 42, 110, COLORS["reference"], "L2 visible-detail primitive", "door mirror head")
        cyl("body", f"{side}_fuel_or_body_plug_reference", 2935, 812 * y_sign, 1065, "y", 115, 28, COLORS["metal"], "L2 visible-detail primitive", "round side body plug/filler datum to verify")
    for idx, y in enumerate([-610, -430, 430, 610], start=1):
        cyl("body", f"tailgate_hinge_or_chain_anchor_{idx}", 3450, y, 800 if abs(y) > 500 else 1185, "x", 54, 42, COLORS["metal"], "L2 tailgate reference", "tailgate hinge/chain anchor datum")
    box("body", "tailgate_lower_pressed_panel", 3438, 0, 800, 38, 1190, 135, COLORS["body_sand"], "L2 panel rib reference", "tailgate lower pressing")
    box("body", "tailgate_upper_pressed_panel", 3438, 0, 1115, 38, 1190, 120, COLORS["body_sand"], "L2 panel rib reference", "tailgate upper pressing")
    cyl("body", "rear_spare_tire", 3605, 0, 1020, "x", 720, 230, COLORS["rubber"], "L2 visible-detail primitive", "rear-mounted spare tire")
    cyl("body", "rear_spare_wheel_rim", 3615, 0, 1020, "x", 385, 245, COLORS["metal"], "L2 visible-detail primitive", "rear spare rim")
    box("body", "spare_wheel_carrier_vertical", 3520, 0, 800, 55, 72, 580, COLORS["metal"], "L2 bracket reference", "spare wheel carrier vertical support")
    box("body", "spare_wheel_carrier_crossbar", 3515, 0, 1015, 55, 560, 55, COLORS["metal"], "L2 bracket reference", "spare wheel carrier crossbar")
    cyl("body", "left_rear_tail_lamp", 3470, -675, 930, "x", 98, 38, COLORS["electrical"], "L2 visible-detail primitive", "rear tail lamp")
    cyl("body", "right_rear_tail_lamp", 3470, 675, 930, "x", 98, 38, COLORS["electrical"], "L2 visible-detail primitive", "rear tail lamp")
    box("body", "rear_license_plate", 3505, 0, 695, 24, 360, 170, COLORS["reference"], "L2 visible-detail primitive", "rear licence plate envelope")

    # Front sheet metal, grille, lamps, bonnet fixtures, and windshield details.
    for idx, y in enumerate([-300, -200, -100, 0, 100, 200, 300], start=1):
        box("front_detail", f"vertical_grille_slot_{idx}", 82, y, 842, 26, 42, 230, COLORS["rubber"], "L2 visible-detail primitive", "FJ40 vertical grille slot")
    for y in [-495, 495]:
        cyl("front_detail", f"headlamp_bezel_{'left' if y < 0 else 'right'}", 80, y, 985, "x", 270, 28, COLORS["metal"], "L2 visible-detail primitive", "round headlamp bezel")
        cyl("front_detail", f"side_marker_{'left' if y < 0 else 'right'}", 188, y * 1.38, 1005, "y", 82, 26, COLORS["electrical"], "L2 visible-detail primitive", "front fender side marker")
    box("front_detail", "front_license_plate", 5, 0, 650, 22, 360, 170, COLORS["reference"], "L2 visible-detail primitive", "front licence plate envelope")
    box("front_detail", "front_bumper_left_end_cap", 40, -780, 525, 150, 115, 130, COLORS["metal"], "L2 visible-detail primitive", "front bumper end cap")
    box("front_detail", "front_bumper_right_end_cap", 40, 780, 525, 150, 115, 130, COLORS["metal"], "L2 visible-detail primitive", "front bumper end cap")
    box("body", "hood_center_raised_rib", 320, 0, 1277, 760, 180, 48, COLORS["body_sand"], "L2 panel rib reference", "hood centre raised rib")
    box("body", "hood_left_outer_rib", 330, -470, 1265, 730, 52, 38, COLORS["body_sand"], "L2 panel rib reference", "hood side rib")
    box("body", "hood_right_outer_rib", 330, 470, 1265, 730, 52, 38, COLORS["body_sand"], "L2 panel rib reference", "hood side rib")
    for side, sign, y_sign in side_pairs:
        box("body", f"{side}_hood_latch", 810, 610 * y_sign, 1210, 88, 50, 58, COLORS["metal"], "L2 visible-detail primitive", "hood side latch")
        box("body", f"{side}_cowl_vent_slot", 1020, 350 * y_sign, 1335, 150, 42, 26, COLORS["rubber"], "L2 visible-detail primitive", "cowl vent slot")
        box("body", f"{side}_windshield_outer_seal", 1122, 548 * y_sign, 1370, 30, 55, 470, COLORS["rubber"], "L2 visible-detail primitive", "windshield side rubber seal")
    box("body", "windshield_top_seal", 1122, 0, 1798, 30, 1320, 45, COLORS["rubber"], "L2 visible-detail primitive", "windshield top rubber seal")
    box("body", "windshield_bottom_seal", 1122, 0, 1360, 30, 1320, 42, COLORS["rubber"], "L2 visible-detail primitive", "windshield lower rubber seal")

    # Hardtop frame, gutters, side/rear window seals, and roof ribs.
    for x, label in [(1290, "front"), (1960, "middle"), (2640, "rear"), (3300, "tail")]:
        box("hard_top", f"{label}_hardtop_roof_rib", x, 0, 1810, 45, 1510, 42, COLORS["roof_white"], "L2 visible-detail primitive", "hardtop roof rib station")
        for side, sign, y_sign in side_pairs:
            cyl("hard_top", f"{label}_{side}_hardtop_vertical_frame", x, 765 * y_sign, 1450, "z", 34, 640, COLORS["metal"], "L2 visible-detail primitive", "hardtop side frame/post")
    for side, sign, y_sign in side_pairs:
        box("hard_top", f"{side}_hardtop_lower_retainer_rail", 1240, 830 * y_sign, 1288, 2200, 42, 46, COLORS["metal"], "L2 bracket reference", "hardtop lower retainer rail")
        box("hard_top", f"{side}_front_window_rubber_seal", 1420, 842 * y_sign, 1435, 535, 28, 355, COLORS["rubber"], "L2 visible-detail primitive", "hardtop front side window seal")
        box("hard_top", f"{side}_rear_window_rubber_seal", 2190, 842 * y_sign, 1435, 650, 28, 355, COLORS["rubber"], "L2 visible-detail primitive", "hardtop rear side window seal")
        for idx, x in enumerate([1320, 1820, 2500, 3180], start=1):
            box("hard_top", f"{side}_hardtop_vertical_joint_{idx}", x, 826 * y_sign, 1320, 22, 28, 570, COLORS["rubber"], "L2 visible-detail primitive", "hardtop vertical joint/seal")
        box("body", f"{side}_side_step_board", 1540, 865 * y_sign, 620, 1120, 210, 55, COLORS["roof_white"], "L2 visible-detail primitive", "painted side step board from project photos")
        box("body", f"{side}_diesel_badge", 2925, 822 * y_sign, 980, 120, 24, 42, COLORS["metal"], "L2 visible-detail primitive", "DIESEL side badge datum from project photos")
    box("hard_top", "rear_window_rubber_seal", 3470, 0, 1460, 28, 850, 330, COLORS["rubber"], "L2 visible-detail primitive", "rear hardtop window seal")
    box("hard_top", "rear_hardtop_window", 3485, 0, 1470, 18, 780, 275, COLORS["glass"], "L2 visible-detail primitive", "rear hardtop window")
    for y in [-555, -275, 275, 555]:
        box("hard_top", f"rear_corner_glass_or_seal_{int(y + 600)}", 3500, y, 1415, 28, 170, 300, COLORS["glass"], "L2 visible-detail primitive", "rear corner hardtop glass/seal datum")

    # Interior: controls, seat structure, belts, floor mats, and dash detail.
    box("interior", "dashboard_glovebox_door", 1212, PASSENGER_Y, 1115, 35, 335, 150, COLORS["reference"], "L2 visible-detail primitive", "glovebox door on passenger/right side for LHD cabin")
    box("interior", "dash_instrument_cluster_plate", 1208, DRIVER_Y, 1128, 36, 330, 170, COLORS["reference"], "L2 visible-detail primitive", "instrument cluster plate on left-hand-drive side")
    for idx, y in enumerate([-535, -480, -425, -370, -315], start=1):
        cyl("interior", f"dash_switch_knob_{idx}", 1200, y, 1050, "x", 34, 26, COLORS["metal"], "L2 visible-detail primitive", "dash switch knob")
    for idx, y in enumerate([90, 155, 220, 285], start=1):
        cyl("interior", f"heater_control_knob_{idx}", 1200, y, 1048, "x", 30, 24, COLORS["metal"], "L2 visible-detail primitive", "heater/control knob")
    for spoke_idx, y in enumerate([DRIVER_Y - 90, DRIVER_Y, DRIVER_Y + 90], start=1):
        box("interior", f"steering_wheel_spoke_{spoke_idx}", 1216, y, 1205, 34, 170, 18, COLORS["metal"], "L2 visible-detail primitive", "steering wheel spoke reference")
    for pedal_idx, (name, y) in enumerate([("clutch", DRIVER_Y - 100), ("brake", DRIVER_Y - 20), ("accelerator", DRIVER_Y + 70)], start=1):
        box("interior", f"{name}_pedal_pad", 1340, y, 705, 90, 45, 110, COLORS["rubber"], "L2 visible-detail primitive", "pedal pad")
        cyl("interior", f"{name}_pedal_arm", 1300, y, 820, "z", 22, 240, COLORS["metal"], "L2 visible-detail primitive", "pedal arm")
    box("interior", "lhd_pedal_box_reinforcement", 1195, DRIVER_Y - 45, 850, 95, 285, 250, COLORS["metal"], "L2 service datum", "left-hand-drive pedal box reinforcement at driver firewall")
    box("interior", "lhd_steering_column_dash_bracket", 1215, DRIVER_Y, 1040, 62, 210, 66, COLORS["metal"], "L2 service datum", "left-hand-drive steering column dash support bracket")
    cyl("interior", "steering_column_firewall_boot", 1142, DRIVER_Y, 1020, "x", 130, 48, COLORS["rubber"], "L2 visible-detail primitive", "rubber boot where LHD steering column passes through firewall")
    cyl("interior", "brake_pedal_pivot_bar", 1260, DRIVER_Y - 20, 960, "y", 32, 180, COLORS["metal"], "L2 service datum", "LHD brake pedal pivot bar")
    cyl("interior", "clutch_pedal_pivot_bar", 1260, DRIVER_Y - 100, 960, "y", 32, 170, COLORS["metal"], "L2 service datum", "LHD clutch pedal pivot bar")
    box("interior", "accelerator_linkage_pivot", 1225, DRIVER_Y + 95, 875, 52, 42, 125, COLORS["metal"], "L2 service datum", "LHD accelerator linkage pivot on driver side")
    cyl("interior", "steering_column_indicator_stalk", 1225, DRIVER_Y - 185, 1220, "y", 22, 165, COLORS["metal"], "L2 visible-detail primitive", "left-hand-drive steering column stalk reference")
    box("interior", "driver_side_floor_dimmer_switch", 1290, DRIVER_Y - 230, 735, 70, 55, 34, COLORS["rubber"], "L2 visible-detail primitive", "floor dimmer/switch placeholder on LHD driver footwell")
    cyl("interior", "handbrake_lever", 1760, -250, 790, "z", 32, 360, COLORS["metal"], "L2 visible-detail primitive", "handbrake lever")
    cyl("interior", "gearshift_knob", 1500, -35, 1160, "z", 86, 60, COLORS["rubber"], "L2 visible-detail primitive", "gearshift knob")
    cyl("interior", "transfer_case_knob", 1580, -120, 1110, "z", 76, 55, COLORS["rubber"], "L2 visible-detail primitive", "transfer case knob")
    for side, sign, y_sign in side_pairs:
        for row, x0 in [("front", 1515), ("rear", 2350)]:
            box("interior", f"{row}_{side}_seat_left_rail", x0, (250 + 170) * y_sign, 675, 545, 36, 42, COLORS["metal"], "L2 service datum", "seat mounting rail")
            box("interior", f"{row}_{side}_seat_right_rail", x0, (250 + 470) * y_sign, 675, 545, 36, 42, COLORS["metal"], "L2 service datum", "seat mounting rail")
        box("interior", f"{side}_front_seat_belt_buckle", 1730, 90 * y_sign, 850, 62, 42, 145, COLORS["electrical"], "L2 visible-detail primitive", "front seat belt buckle")
        box("interior", f"{side}_front_seat_back_seam", 1848, 310 * y_sign, 1080, 24, 390, 28, COLORS["rubber"], "L2 visible-detail primitive", "front seat back seam")
        box("interior", f"{side}_front_floor_mat", 1350, 310 * y_sign, 723, 760, 500, 22, COLORS["rubber"], "L2 visible-detail primitive", "front rubber floor mat")
    box("interior", "rear_floor_mat", 2220, 0, 748, 1050, 1020, 22, COLORS["rubber"], "L2 visible-detail primitive", "rear cargo/interior mat")
    box("interior", "rear_bench_seat_seam", 2510, 0, 845, 610, 1010, 24, COLORS["rubber"], "L2 visible-detail primitive", "rear bench cushion seam")

    # Engine-bay layout: accessories, hoses, battery, brake master, and visible service items.
    cyl("engine_bay", "cooling_fan_hub", 300, 0, 1010, "x", 135, 62, COLORS["metal"], "L2 visible-detail primitive", "cooling fan hub")
    for blade_idx, angle_deg in enumerate([0, 60, 120, 180, 240, 300], start=1):
        blade_y = math.cos(math.radians(angle_deg)) * 210
        blade_z = 1010 + math.sin(math.radians(angle_deg)) * 210
        box("engine_bay", f"cooling_fan_blade_{blade_idx}", 286, blade_y, blade_z - 18, 38, 250, 36, COLORS["metal"], "L2 visible-detail primitive", "cooling fan blade envelope")
    cyl("engine_bay", "crank_pulley", 385, 0, 850, "x", 145, 60, COLORS["metal"], "L2 visible-detail primitive", "front crank pulley")
    cyl("engine_bay", "water_pump_pulley", 360, 0, 1010, "x", 125, 54, COLORS["metal"], "L2 visible-detail primitive", "water pump pulley")
    box("engine_bay", "fan_belt_upper_run", 350, 0, 1010, 26, 38, 270, COLORS["rubber"], "L2 visible-detail primitive", "fan belt upper run")
    box("engine_bay", "fan_belt_lower_run", 385, 0, 850, 26, 38, 235, COLORS["rubber"], "L2 visible-detail primitive", "fan belt lower run")
    cyl("engine_bay", "alternator_body", 565, 325, 1010, "x", 190, 220, COLORS["metal"], "L2 visible-detail primitive", "alternator body")
    cyl("engine_bay", "starter_motor", 730, 265, 680, "x", 155, 310, COLORS["metal"], "L2 visible-detail primitive", "starter motor")
    box("engine_bay", "intake_manifold", 560, -260, 995, 460, 90, 115, COLORS["metal"], "L2 visible-detail primitive", "intake manifold envelope")
    box("engine_bay", "exhaust_manifold", 575, 260, 900, 500, 95, 145, COLORS["engine"], "L2 visible-detail primitive", "exhaust manifold envelope")
    cyl("engine_bay", "carburetor_body", 745, -220, 1165, "z", 120, 170, COLORS["metal"], "L2 visible-detail primitive", "carburetor body")
    cyl("engine_bay", "round_air_cleaner_lid", 760, -235, 1250, "z", 260, 68, COLORS["metal"], "L2 visible-detail primitive", "round air cleaner lid")
    cyl("engine_bay", "brake_booster", 1075, -520, 1060, "x", 260, 145, COLORS["metal"], "L2 service datum", "brake booster package")
    cyl("engine_bay", "master_cylinder", 945, -520, 1060, "x", 92, 230, COLORS["metal"], "L2 service datum", "brake master cylinder")
    box("engine_bay", "clutch_master_cylinder", 945, -350, 1035, 210, 82, 76, COLORS["metal"], "L2 service datum", "clutch master cylinder")
    box("engine_bay", "lhd_firewall_pedal_box_outer_plate", 1112, DRIVER_Y - 55, 895, 42, 350, 300, COLORS["metal"], "L2 service datum", "left-hand-drive pedal box outer reinforcement on firewall")
    box("engine_bay", "brake_booster_firewall_bracket", 1110, -520, 1015, 48, 300, 250, COLORS["metal"], "L2 service datum", "LHD brake booster firewall bracket")
    cyl("engine_bay", "brake_master_reservoir", 875, -520, 1165, "z", 110, 105, COLORS["reference"], "L2 service datum", "brake fluid reservoir on left-hand-drive master cylinder")
    cyl("engine_bay", "brake_master_reservoir_cap", 875, -520, 1225, "z", 82, 24, COLORS["brass"], "L2 visible-detail primitive", "brake master reservoir cap")
    cyl("engine_bay", "brake_booster_vacuum_hose", 820, -430, 1130, "x", 34, 470, COLORS["rubber"], "L2 routing reference", "vacuum hose from engine to LHD brake booster")
    cyl("engine_bay", "clutch_master_reservoir_cap", 910, -350, 1130, "z", 70, 26, COLORS["brass"], "L2 service datum", "clutch master reservoir cap")
    cyl("engine_bay", "clutch_hydraulic_line_firewall_run", 830, -350, 980, "x", 14, 520, COLORS["metal"], "L2 routing reference", "clutch hydraulic line from LHD master cylinder")
    cyl("engine_bay", "steering_column_lower_firewall_shaft", 1010, DRIVER_Y, 980, "x", 44, 340, COLORS["metal"], "L2 routing reference", "LHD steering shaft leaving firewall toward steering box")
    cyl("engine_bay", "steering_column_lower_universal_joint", 840, DRIVER_Y - 10, 955, "x", 76, 58, COLORS["metal"], "L2 service datum", "lower steering universal joint")
    cyl("engine_bay", "steering_intermediate_shaft", 690, DRIVER_Y - 35, 850, "x", 40, 360, COLORS["metal"], "L2 routing reference", "intermediate steering shaft to left steering box")
    box("engine_bay", "battery_case", 570, 430, 765, 310, 205, 205, COLORS["rubber"], "L2 service datum", "battery case")
    cyl("engine_bay", "battery_positive_terminal", 622, 355, 985, "z", 34, 46, COLORS["electrical"], "L2 service datum", "battery positive terminal")
    cyl("engine_bay", "battery_negative_terminal", 812, 505, 985, "z", 34, 46, COLORS["metal"], "L2 service datum", "battery negative terminal")
    cyl("engine_bay", "positive_battery_cable_run", 710, 405, 1015, "x", 24, 520, COLORS["electrical"], "L2 routing reference", "positive battery cable")
    cyl("engine_bay", "radiator_top_tank", 205, 0, 1095, "y", 95, 1030, COLORS["metal"], "L2 visible-detail primitive", "radiator top tank")
    cyl("engine_bay", "radiator_bottom_tank", 205, 0, 720, "y", 85, 1030, COLORS["metal"], "L2 visible-detail primitive", "radiator bottom tank")
    cyl("engine_bay", "radiator_cap", 218, 260, 1155, "z", 54, 36, COLORS["brass"], "L2 visible-detail primitive", "radiator cap")
    box("engine_bay", "washer_bottle", 795, 535, 850, 160, 105, 210, COLORS["reference"], "L2 service datum", "washer bottle")
    box("engine_bay", "engine_bay_fuse_relay_board_reference", 930, 610, 930, 240, 75, 220, COLORS["electrical"], "L2 packaging reference", "engine bay fuse/relay board packaging placeholder")
    cyl("engine_bay", "dipstick_loop", 840, 130, 1030, "z", 46, 28, COLORS["brass"], "L2 visible-detail primitive", "oil dipstick loop")

    # Fuel system and exhaust references.
    box("fuel_system", "rear_underfloor_fuel_tank", 2870, 0, 405, 650, 930, 260, COLORS["fluid"], "L2 underbody reference", "rear underfloor fuel tank")
    for idx, x in enumerate([2780, 3020], start=1):
        box("fuel_system", f"fuel_tank_retaining_strap_{idx}", x, 0, 555, 42, 980, 38, COLORS["metal"], "L2 service datum", "fuel tank retaining strap")
    cyl("fuel_system", "fuel_filler_neck", 3000, -690, 940, "z", 76, 410, COLORS["metal"], "L2 routing reference", "fuel filler neck to left rear quarter")
    cyl("fuel_system", "fuel_line_frame_run", 1880, 330, 560, "x", 16, 2070, COLORS["brass"], "L2 routing reference", "fuel hard-line run")
    cyl("exhaust", "front_exhaust_pipe", 870, 310, 520, "x", 68, 950, COLORS["metal"], "L2 routing reference", "front exhaust pipe")
    cyl("exhaust", "centre_exhaust_pipe", 1700, 330, 470, "x", 68, 1020, COLORS["metal"], "L2 routing reference", "centre exhaust pipe")
    cyl("exhaust", "rear_exhaust_pipe", 2750, 330, 470, "x", 62, 1220, COLORS["metal"], "L2 routing reference", "rear exhaust pipe")
    cyl("exhaust", "muffler_body", 2260, 330, 465, "x", 250, 650, COLORS["metal"], "L2 visible-detail primitive", "muffler body")
    for idx, x in enumerate([1020, 2180, 3040], start=1):
        box("exhaust", f"exhaust_hanger_{idx}", x, 330, 590, 52, 58, 135, COLORS["rubber"], "L2 service datum", "exhaust hanger rubber")

    # Measurement datum bars make the model more useful while the mesh is absent.
    cyl("datum", "wheelbase_datum_line_left", (front_axle_x + rear_axle_x) / 2, -925, 285, "x", 18, 2285, COLORS["datum"], "measurement datum", "wheelbase datum line on left side")
    cyl("datum", "wheelbase_datum_line_right", (front_axle_x + rear_axle_x) / 2, 925, 285, "x", 18, 2285, COLORS["datum"], "measurement datum", "wheelbase datum line on right side")
    cyl("datum", "front_track_datum_line", front_axle_x, 0, 260, "y", 18, 1410, COLORS["datum"], "measurement datum", "front track datum line")
    cyl("datum", "rear_track_datum_line", rear_axle_x, 0, 260, "y", 18, 1410, COLORS["datum"], "measurement datum", "rear track datum line")

    return p


def hex_to_scad_color(hex_color: str) -> str:
    value = hex_color.lstrip("#")
    r = int(value[0:2], 16) / 255
    g = int(value[2:4], 16) / 255
    b = int(value[4:6], 16) / 255
    return f"[{r:.3f}, {g:.3f}, {b:.3f}, 0.80]"


def hex_to_fc_color(hex_color: str) -> tuple[float, float, float]:
    value = hex_color.lstrip("#")
    return (int(value[0:2], 16) / 255, int(value[2:4], 16) / 255, int(value[4:6], 16) / 255)


def write_scad(model_parts: list[PartType]) -> Path:
    lines = [
        f"// {MODEL_SHORT_TITLE}",
        "// Units: millimetres. Coordinate system: X front to rear, Y centreline left/right, Z ground up.",
        "// Left-hand drive: negative Y is the driver side.",
        "// Generated by tools/generate_j40_full_vehicle_cad_scaffold.py.",
        "// This is a project-owned reference scaffold, not a direct extraction of the CC-BY mesh.",
        "",
        "$fn = 64;",
        "",
        "module box_part(x, y_center, z, length, width, height) {",
        "  translate([x, y_center - width / 2, z]) cube([length, width, height], center = false);",
        "}",
        "",
        "module wheel_part(x, y_center, z, diameter, width) {",
        "  color([0.03, 0.03, 0.03, 1.0])",
        "    translate([x, y_center, z]) rotate([90, 0, 0]) cylinder(d = diameter, h = width, center = true);",
        "  color([0.72, 0.72, 0.72, 1.0])",
        "    translate([x, y_center, z]) rotate([90, 0, 0]) cylinder(d = diameter * 0.52, h = width + 8, center = true);",
        "  color([0.10, 0.10, 0.10, 1.0])",
        "    translate([x, y_center, z]) rotate([90, 0, 0]) cylinder(d = diameter * 0.30, h = width + 14, center = true);",
        "}",
        "",
        "module cylinder_part(x, y, z, axis, diameter, length) {",
        "  translate([x, y, z])",
        "    if (axis == \"x\") rotate([0, 90, 0]) cylinder(d = diameter, h = length, center = true);",
        "    else if (axis == \"y\") rotate([90, 0, 0]) cylinder(d = diameter, h = length, center = true);",
        "    else cylinder(d = diameter, h = length, center = true);",
        "}",
        "",
    ]
    for part in model_parts:
        lines.append(f"// {part.group}: {part.name} - {part.confidence}")
        if isinstance(part, BoxPart):
            lines.append(f"color({hex_to_scad_color(part.color)})")
            lines.append(
                f"  box_part({part.x:g}, {part.y:g}, {part.z:g}, {part.length:g}, {part.width:g}, {part.height:g});"
            )
        else:
            if isinstance(part, WheelPart):
                lines.append(f"wheel_part({part.x:g}, {part.y:g}, {part.z:g}, {part.diameter:g}, {part.width:g});")
            else:
                lines.append(f"color({hex_to_scad_color(part.color)})")
                lines.append(
                    f"  cylinder_part({part.x:g}, {part.y:g}, {part.z:g}, \"{part.axis}\", {part.diameter:g}, {part.length:g});"
                )
        lines.append("")
    path = OUT_DIR / f"{MODEL_NAME}.scad"
    path.write_text("\n".join(lines), encoding="ascii")
    return path


def write_freecad_macro(model_parts: list[PartType]) -> Path:
    lines = [
        f"# {MODEL_SHORT_TITLE}",
        "# Units: millimetres. Run inside FreeCAD.",
        "# Left-hand drive: negative Y is the driver side.",
        "# Generated by tools/generate_j40_full_vehicle_cad_scaffold.py.",
        "import FreeCAD as App",
        "import Part",
        "",
        "try:",
        "    import FreeCADGui as Gui",
        "except Exception:",
        "    Gui = None",
        "",
        f"doc = App.newDocument({MODEL_NAME!r})",
        "groups = {}",
        "",
        "TRANSPARENCY_BY_GROUP = {",
        "    'glass': 60,",
        "    'hard_top': 18,",
        "    'datum': 45,",
        "}",
        "",
        "def group_for(group_name):",
        "    group = groups.get(group_name)",
        "    if group is None:",
        "        group = doc.addObject('App::DocumentObjectGroup', group_name)",
        "        group.Label = group_name.replace('_', ' ').title()",
        "        groups[group_name] = group",
        "    return group",
        "",
        "def set_color(obj, rgb, group_name):",
        "    if hasattr(obj, 'ViewObject'):",
        "        obj.ViewObject.ShapeColor = rgb",
        "        obj.ViewObject.Transparency = TRANSPARENCY_BY_GROUP.get(group_name, 0)",
        "",
        "def add_to_group(obj, group_name):",
        "    group_for(group_name).addObject(obj)",
        "    return obj",
        "",
        "def add_box(group_name, name, x, y_center, z, length, width, height, rgb):",
        "    shape = Part.makeBox(length, width, height, App.Vector(x, y_center - width / 2, z))",
        "    obj = doc.addObject('Part::Feature', name)",
        "    obj.Shape = shape",
        "    obj.Label = name.replace('_', ' ')",
        "    set_color(obj, rgb, group_name)",
        "    return add_to_group(obj, group_name)",
        "",
        "def add_cylinder(group_name, name, x, y, z, axis, diameter, length, rgb):",
        "    if axis == 'x':",
        "        vector = App.Vector(1, 0, 0)",
        "        base = App.Vector(x - length / 2, y, z)",
        "    elif axis == 'y':",
        "        vector = App.Vector(0, 1, 0)",
        "        base = App.Vector(x, y - length / 2, z)",
        "    else:",
        "        vector = App.Vector(0, 0, 1)",
        "        base = App.Vector(x, y, z - length / 2)",
        "    obj = doc.addObject('Part::Feature', name)",
        "    obj.Shape = Part.makeCylinder(diameter / 2, length, base, vector)",
        "    obj.Label = name.replace('_', ' ')",
        "    set_color(obj, rgb, group_name)",
        "    return add_to_group(obj, group_name)",
        "",
        "def add_wheel(group_name, name, x, y_center, z, diameter, width):",
        "    tire = doc.addObject('Part::Feature', name + '_tire')",
        "    tire.Shape = Part.makeCylinder(diameter / 2, width, App.Vector(x, y_center - width / 2, z), App.Vector(0, 1, 0))",
        "    tire.Label = name.replace('_', ' ') + ' tire'",
        "    set_color(tire, (0.03, 0.03, 0.03), group_name)",
        "    add_to_group(tire, group_name)",
        "    rim = doc.addObject('Part::Feature', name + '_rim')",
        "    rim.Shape = Part.makeCylinder(diameter * 0.26, width + 8, App.Vector(x, y_center - (width + 8) / 2, z), App.Vector(0, 1, 0))",
        "    rim.Label = name.replace('_', ' ') + ' rim'",
        "    set_color(rim, (0.72, 0.72, 0.72), group_name)",
        "    add_to_group(rim, group_name)",
        "    hub = doc.addObject('Part::Feature', name + '_hub')",
        "    hub.Shape = Part.makeCylinder(diameter * 0.15, width + 14, App.Vector(x, y_center - (width + 14) / 2, z), App.Vector(0, 1, 0))",
        "    hub.Label = name.replace('_', ' ') + ' hub'",
        "    set_color(hub, (0.10, 0.10, 0.10), group_name)",
        "    add_to_group(hub, group_name)",
        "    return tire",
        "",
    ]
    for part in model_parts:
        safe = part.name.replace("-", "_").replace(" ", "_")
        if isinstance(part, BoxPart):
            color = hex_to_fc_color(part.color)
            lines.append(
                "add_box("
                f"{part.group!r}, {safe!r}, {part.x:g}, {part.y:g}, {part.z:g}, {part.length:g}, {part.width:g}, {part.height:g}, "
                f"({color[0]:.3f}, {color[1]:.3f}, {color[2]:.3f}))"
            )
        elif isinstance(part, WheelPart):
            lines.append(
                f"add_wheel({part.group!r}, {safe!r}, {part.x:g}, {part.y:g}, {part.z:g}, {part.diameter:g}, {part.width:g})"
            )
        else:
            color = hex_to_fc_color(part.color)
            lines.append(
                "add_cylinder("
                f"{part.group!r}, {safe!r}, {part.x:g}, {part.y:g}, {part.z:g}, {part.axis!r}, {part.diameter:g}, {part.length:g}, "
                f"({color[0]:.3f}, {color[1]:.3f}, {color[2]:.3f}))"
            )
    lines.extend(["", "doc.recompute()", "Gui.SendMsgToActiveView('ViewFit') if Gui is not None else None", ""])
    path = OUT_DIR / f"{MODEL_NAME}.FCMacro"
    path.write_text("\n".join(lines), encoding="ascii")
    return path


def project_rect(part: PartType, view: str) -> tuple[float, float, float, float] | None:
    if isinstance(part, CylinderPart):
        if part.axis == "x":
            bounds = (part.x - part.length / 2, part.y - part.diameter / 2, part.z - part.diameter / 2, part.length, part.diameter, part.diameter)
        elif part.axis == "y":
            bounds = (part.x - part.diameter / 2, part.y - part.length / 2, part.z - part.diameter / 2, part.diameter, part.length, part.diameter)
        else:
            bounds = (part.x - part.diameter / 2, part.y - part.diameter / 2, part.z - part.length / 2, part.diameter, part.diameter, part.length)
        bx, by, bz, bl, bw, bh = bounds
        if view == "plan":
            return (bx, by, bl, bw)
        if view == "side":
            return (bx, bz, bl, bh)
        if view == "front":
            return (by, bz, bw, bh)
        return None
    if isinstance(part, WheelPart):
        if view == "plan":
            return (part.x - part.diameter / 2, part.y - part.width / 2, part.diameter, part.width)
        if view == "side":
            return (part.x - part.diameter / 2, part.z - part.diameter / 2, part.diameter, part.diameter)
        if view == "front":
            return (part.y - part.width / 2, part.z - part.diameter / 2, part.width, part.diameter)
        return None
    if view == "plan":
        return (part.x, part.y - part.width / 2, part.length, part.width)
    if view == "side":
        return (part.x, part.z, part.length, part.height)
    if view == "front":
        return (part.y - part.width / 2, part.z, part.width, part.height)
    return None


def write_svg(model_parts: list[PartType]) -> Path:
    width = 1680
    height = 1260
    scale = 0.24
    panels = {
        "plan": (40, 95, "PLAN X/Y"),
        "side": (40, 620, "SIDE X/Z"),
        "front": (1120, 620, "FRONT Y/Z"),
    }

    def tx(view: str, x: float, y: float) -> tuple[float, float]:
        ox, oy, _ = panels[view]
        if view == "plan":
            return ox + x * scale, oy + (900 - y) * scale
        if view == "side":
            return ox + x * scale, oy + (2050 - y) * scale
        return ox + (900 + x) * scale, oy + (2050 - y) * scale

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;font-size:14px;fill:#202124}.label{font-size:10px;fill:#333}.title{font-size:22px;font-weight:700}</style>',
        f'<text class="title" x="40" y="32">{MODEL_TITLE}</text>',
        '<text x="40" y="52">Units mm. LHD reference scaffold only; refine after CC-BY mesh and vehicle measurements arrive.</text>',
    ]

    for view, (ox, oy, title) in panels.items():
        svg.append(f'<text x="{ox}" y="{oy - 16}" font-weight="700">{title}</text>')
        for part in model_parts:
            rect = project_rect(part, view)
            if rect is None:
                continue
            x, y, w, h = rect
            x0, y0 = tx(view, x, y + h)
            x1, y1 = tx(view, x + w, y)
            rx = min(x0, x1)
            ry = min(y0, y1)
            rw = abs(x1 - x0)
            rh = abs(y1 - y0)
            opacity = "0.55" if isinstance(part, (WheelPart, CylinderPart)) else "0.38"
            svg.append(
                f'<rect x="{rx:.2f}" y="{ry:.2f}" width="{rw:.2f}" height="{rh:.2f}" '
                f'fill="{part.color}" fill-opacity="{opacity}" stroke="#1f1f1f" stroke-width="0.6"/>'
            )
        # overall envelope
        if view == "plan":
            x0, y0 = tx(view, 0, -832.5)
            x1, y1 = tx(view, 3840, 832.5)
        elif view == "side":
            x0, y0 = tx(view, 0, 0)
            x1, y1 = tx(view, 3840, 1950)
        else:
            x0, y0 = tx(view, -832.5, 0)
            x1, y1 = tx(view, 832.5, 1950)
        svg.append(
            f'<rect x="{min(x0, x1):.2f}" y="{min(y0, y1):.2f}" width="{abs(x1-x0):.2f}" '
            f'height="{abs(y1-y0):.2f}" fill="none" stroke="#d33" stroke-width="1.2" stroke-dasharray="8 5"/>'
        )

    legend_x = 1120
    legend_y = 60
    svg.append(f'<text x="{legend_x}" y="{legend_y}" font-weight="700">Layers</text>')
    for idx, (name, color) in enumerate(COLORS.items()):
        y = legend_y + 24 + idx * 22
        svg.append(f'<rect x="{legend_x}" y="{y - 13}" width="18" height="14" fill="{color}" stroke="#333"/>')
        svg.append(f'<text x="{legend_x + 26}" y="{y}">{html.escape(name)}</text>')
    svg.append("</svg>")
    path = OUT_DIR / f"{MODEL_NAME}_orthographic.svg"
    path.write_text("\n".join(svg), encoding="ascii")
    return path


def rgba(hex_color: str, alpha: int) -> tuple[int, int, int, int]:
    value = hex_color.lstrip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), alpha)


def write_png_preview(model_parts: list[PartType]) -> Path:
    width = 1680
    height = 1260
    scale = 0.24
    image = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image, "RGBA")
    font = ImageFont.load_default()
    panels = {
        "plan": (40, 95, "PLAN X/Y"),
        "side": (40, 620, "SIDE X/Z"),
        "front": (1120, 620, "FRONT Y/Z"),
    }

    def tx(view: str, x: float, y: float) -> tuple[float, float]:
        ox, oy, _ = panels[view]
        if view == "plan":
            return ox + x * scale, oy + (900 - y) * scale
        if view == "side":
            return ox + x * scale, oy + (2050 - y) * scale
        return ox + (900 + x) * scale, oy + (2050 - y) * scale

    draw.text((40, 18), MODEL_TITLE, fill=(32, 33, 36, 255), font=font)
    draw.text(
        (40, 38),
        "Units mm. LHD reference scaffold only; refine after CC-BY mesh and vehicle measurements arrive.",
        fill=(32, 33, 36, 255),
        font=font,
    )

    for view, (ox, oy, title) in panels.items():
        draw.text((ox, oy - 20), title, fill=(32, 33, 36, 255), font=font)
        for part in model_parts:
            rect = project_rect(part, view)
            if rect is None:
                continue
            x, y, w, h = rect
            x0, y0 = tx(view, x, y + h)
            x1, y1 = tx(view, x + w, y)
            fill = rgba(part.color, 145 if isinstance(part, (WheelPart, CylinderPart)) else 95)
            draw.rectangle((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)), fill=fill, outline=(31, 31, 31, 180))
        if view == "plan":
            x0, y0 = tx(view, 0, -832.5)
            x1, y1 = tx(view, 3840, 832.5)
        elif view == "side":
            x0, y0 = tx(view, 0, 0)
            x1, y1 = tx(view, 3840, 1950)
        else:
            x0, y0 = tx(view, -832.5, 0)
            x1, y1 = tx(view, 832.5, 1950)
        draw.rectangle((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)), outline=(210, 50, 50, 255), width=2)

    legend_x = 1120
    legend_y = 60
    draw.text((legend_x, legend_y), "Layers", fill=(32, 33, 36, 255), font=font)
    for idx, (name, color) in enumerate(COLORS.items()):
        y = legend_y + 24 + idx * 22
        draw.rectangle((legend_x, y - 13, legend_x + 18, y + 1), fill=rgba(color, 255), outline=(51, 51, 51, 255))
        draw.text((legend_x + 26, y - 12), name, fill=(32, 33, 36, 255), font=font)

    path = OUT_DIR / f"{MODEL_NAME}_orthographic.png"
    image.convert("RGB").save(path)
    return path


def dxf_num(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def add_dxf_line(lines: list[str], x1: float, y1: float, x2: float, y2: float, layer: str) -> None:
    lines.extend(["0", "LINE", "8", layer, "10", dxf_num(x1), "20", dxf_num(y1), "11", dxf_num(x2), "21", dxf_num(y2)])


def add_dxf_rect(lines: list[str], x: float, y: float, w: float, h: float, layer: str) -> None:
    add_dxf_line(lines, x, y, x + w, y, layer)
    add_dxf_line(lines, x + w, y, x + w, y + h, layer)
    add_dxf_line(lines, x + w, y + h, x, y + h, layer)
    add_dxf_line(lines, x, y + h, x, y, layer)


def write_dxf(model_parts: list[PartType]) -> Path:
    lines = [
        "0",
        "SECTION",
        "2",
        "HEADER",
        "9",
        "$INSUNITS",
        "70",
        "4",
        "0",
        "ENDSEC",
        "0",
        "SECTION",
        "2",
        "ENTITIES",
    ]
    origins = {"plan": (0, 0), "side": (0, 2500), "front": (5000, 2500)}
    for view, (ox, oy) in origins.items():
        for part in model_parts:
            rect = project_rect(part, view)
            if rect is None:
                continue
            x, y, w, h = rect
            add_dxf_rect(lines, ox + x, oy + y, w, h, part.group.upper())
        if view == "plan":
            add_dxf_rect(lines, ox + 0, oy - 832.5, 3840, 1665, "OVERALL")
        elif view == "side":
            add_dxf_rect(lines, ox + 0, oy + 0, 3840, 1950, "OVERALL")
        else:
            add_dxf_rect(lines, ox - 832.5, oy + 0, 1665, 1950, "OVERALL")
    lines.extend(["0", "ENDSEC", "0", "EOF"])
    path = OUT_DIR / f"{MODEL_NAME}_orthographic.dxf"
    path.write_text("\n".join(lines), encoding="ascii")
    return path


def vec_add(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vec_mul(a: tuple[float, float, float], scale: float) -> tuple[float, float, float]:
    return (a[0] * scale, a[1] * scale, a[2] * scale)


def vec_neg(a: tuple[float, float, float]) -> tuple[float, float, float]:
    return (-a[0], -a[1], -a[2])


def add_gltf_triangle(
    positions: list[tuple[float, float, float]],
    normals: list[tuple[float, float, float]],
    p1: tuple[float, float, float],
    p2: tuple[float, float, float],
    p3: tuple[float, float, float],
    n1: tuple[float, float, float],
    n2: tuple[float, float, float] | None = None,
    n3: tuple[float, float, float] | None = None,
) -> None:
    positions.extend([p1, p2, p3])
    normals.extend([n1, n2 or n1, n3 or n1])


def add_gltf_quad(
    positions: list[tuple[float, float, float]],
    normals: list[tuple[float, float, float]],
    p1: tuple[float, float, float],
    p2: tuple[float, float, float],
    p3: tuple[float, float, float],
    p4: tuple[float, float, float],
    normal: tuple[float, float, float],
) -> None:
    add_gltf_triangle(positions, normals, p1, p2, p3, normal)
    add_gltf_triangle(positions, normals, p1, p3, p4, normal)


def gltf_box_mesh(part: BoxPart) -> tuple[list[tuple[float, float, float]], list[tuple[float, float, float]]]:
    positions: list[tuple[float, float, float]] = []
    normals: list[tuple[float, float, float]] = []
    x0 = part.x
    x1 = part.x + part.length
    y0 = part.y - part.width / 2
    y1 = part.y + part.width / 2
    z0 = part.z
    z1 = part.z + part.height
    p000 = (x0, y0, z0)
    p001 = (x0, y0, z1)
    p010 = (x0, y1, z0)
    p011 = (x0, y1, z1)
    p100 = (x1, y0, z0)
    p101 = (x1, y0, z1)
    p110 = (x1, y1, z0)
    p111 = (x1, y1, z1)
    for face, normal in [
        ((p100, p110, p111, p101), (1.0, 0.0, 0.0)),
        ((p000, p001, p011, p010), (-1.0, 0.0, 0.0)),
        ((p010, p011, p111, p110), (0.0, 1.0, 0.0)),
        ((p000, p100, p101, p001), (0.0, -1.0, 0.0)),
        ((p001, p101, p111, p011), (0.0, 0.0, 1.0)),
        ((p000, p010, p110, p100), (0.0, 0.0, -1.0)),
    ]:
        add_gltf_quad(positions, normals, *face, normal)
    return positions, normals


def gltf_cylinder_mesh(
    x: float,
    y: float,
    z: float,
    axis: str,
    diameter: float,
    length: float,
    segments: int = 32,
) -> tuple[list[tuple[float, float, float]], list[tuple[float, float, float]]]:
    positions: list[tuple[float, float, float]] = []
    normals: list[tuple[float, float, float]] = []
    center = (x, y, z)
    radius = diameter / 2
    if axis == "x":
        axis_vec = (1.0, 0.0, 0.0)
        u_vec = (0.0, 1.0, 0.0)
        v_vec = (0.0, 0.0, 1.0)
    elif axis == "y":
        axis_vec = (0.0, 1.0, 0.0)
        u_vec = (1.0, 0.0, 0.0)
        v_vec = (0.0, 0.0, 1.0)
    else:
        axis_vec = (0.0, 0.0, 1.0)
        u_vec = (1.0, 0.0, 0.0)
        v_vec = (0.0, 1.0, 0.0)
    start_center = vec_add(center, vec_mul(axis_vec, -length / 2))
    end_center = vec_add(center, vec_mul(axis_vec, length / 2))
    for index in range(segments):
        a0 = index / segments * math.tau
        a1 = (index + 1) / segments * math.tau
        radial0 = vec_add(vec_mul(u_vec, math.cos(a0) * radius), vec_mul(v_vec, math.sin(a0) * radius))
        radial1 = vec_add(vec_mul(u_vec, math.cos(a1) * radius), vec_mul(v_vec, math.sin(a1) * radius))
        s0 = vec_add(start_center, radial0)
        s1 = vec_add(start_center, radial1)
        e0 = vec_add(end_center, radial0)
        e1 = vec_add(end_center, radial1)
        radial0_normal = (radial0[0] / radius, radial0[1] / radius, radial0[2] / radius)
        radial1_normal = (radial1[0] / radius, radial1[1] / radius, radial1[2] / radius)
        add_gltf_triangle(positions, normals, s0, e0, e1, radial0_normal, radial0_normal, radial1_normal)
        add_gltf_triangle(positions, normals, s0, e1, s1, radial0_normal, radial1_normal, radial1_normal)
        add_gltf_triangle(positions, normals, start_center, s1, s0, vec_neg(axis_vec))
        add_gltf_triangle(positions, normals, end_center, e0, e1, axis_vec)
    return positions, normals


def hex_to_rgba_factor(hex_color: str, alpha: float = 1.0) -> list[float]:
    color = hex_color.lstrip("#")
    return [int(color[index : index + 2], 16) / 255 for index in (0, 2, 4)] + [alpha]


def gltf_render_items(
    model_parts: list[PartType],
) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    for part in model_parts:
        if isinstance(part, BoxPart):
            positions, normals = gltf_box_mesh(part)
            items.append(
                {
                    "group": part.group,
                    "name": part.name,
                    "color": part.color,
                    "confidence": part.confidence,
                    "notes": part.notes,
                    "positions": positions,
                    "normals": normals,
                }
            )
        elif isinstance(part, CylinderPart):
            positions, normals = gltf_cylinder_mesh(part.x, part.y, part.z, part.axis, part.diameter, part.length)
            items.append(
                {
                    "group": part.group,
                    "name": part.name,
                    "color": part.color,
                    "confidence": part.confidence,
                    "notes": part.notes,
                    "positions": positions,
                    "normals": normals,
                }
            )
        else:
            for suffix, diameter, width, color, note in [
                ("tire", part.diameter, part.width, part.color, part.notes),
                ("rim", part.diameter * 0.52, part.width + 8, COLORS["metal"], "wheel rim reference"),
                ("hub", part.diameter * 0.30, part.width + 14, COLORS["black_trim"], "wheel hub reference"),
            ]:
                positions, normals = gltf_cylinder_mesh(part.x, part.y, part.z, "y", diameter, width)
                items.append(
                    {
                        "group": part.group,
                        "name": f"{part.name}_{suffix}",
                        "color": color,
                        "confidence": part.confidence,
                        "notes": note,
                        "positions": positions,
                        "normals": normals,
                    }
                )
    return items


def write_gltf(model_parts: list[PartType]) -> Path:
    buffer = bytearray()
    buffer_views: list[dict[str, object]] = []
    accessors: list[dict[str, object]] = []
    materials: list[dict[str, object]] = []
    material_lookup: dict[str, int] = {}
    meshes: list[dict[str, object]] = []
    nodes: list[dict[str, object]] = []

    def align_buffer() -> None:
        while len(buffer) % 4:
            buffer.append(0)

    def add_float_vec3_accessor(values: list[tuple[float, float, float]], *, target: int, include_bounds: bool) -> int:
        align_buffer()
        byte_offset = len(buffer)
        converted = [(x * 0.001, y * 0.001, z * 0.001) if include_bounds else (x, y, z) for x, y, z in values]
        for x, y, z in converted:
            buffer.extend(struct.pack("<fff", x, y, z))
        byte_length = len(buffer) - byte_offset
        buffer_views.append({"buffer": 0, "byteOffset": byte_offset, "byteLength": byte_length, "target": target})
        accessor: dict[str, object] = {
            "bufferView": len(buffer_views) - 1,
            "componentType": 5126,
            "count": len(values),
            "type": "VEC3",
        }
        if include_bounds and converted:
            accessor["min"] = [min(point[index] for point in converted) for index in range(3)]
            accessor["max"] = [max(point[index] for point in converted) for index in range(3)]
        accessors.append(accessor)
        return len(accessors) - 1

    def material_for(color: str) -> int:
        if color not in material_lookup:
            alpha = 0.45 if color == COLORS["glass"] else 1.0
            material: dict[str, object] = {
                "name": next((name for name, value in COLORS.items() if value == color), color),
                "pbrMetallicRoughness": {
                    "baseColorFactor": hex_to_rgba_factor(color, alpha),
                    "metallicFactor": 0.0,
                    "roughnessFactor": 0.72,
                },
            }
            if alpha < 1.0:
                material["alphaMode"] = "BLEND"
                material["doubleSided"] = True
            material_lookup[color] = len(materials)
            materials.append(material)
        return material_lookup[color]

    group_nodes: dict[str, int] = {}
    for group in sorted({part.group for part in model_parts}):
        group_nodes[group] = len(nodes)
        nodes.append({"name": group.replace("_", " ").title(), "children": []})

    for item in gltf_render_items(model_parts):
        positions = item["positions"]
        normals = item["normals"]
        if not isinstance(positions, list) or not isinstance(normals, list):
            continue
        position_accessor = add_float_vec3_accessor(positions, target=34962, include_bounds=True)
        normal_accessor = add_float_vec3_accessor(normals, target=34962, include_bounds=False)
        material = material_for(str(item["color"]))
        meshes.append(
            {
                "name": item["name"],
                "primitives": [
                    {
                        "attributes": {"POSITION": position_accessor, "NORMAL": normal_accessor},
                        "material": material,
                        "mode": 4,
                    }
                ],
            }
        )
        node_index = len(nodes)
        nodes.append(
            {
                "name": item["name"],
                "mesh": len(meshes) - 1,
                "extras": {
                    "group": item["group"],
                    "confidence": item["confidence"],
                    "notes": item["notes"],
                },
            }
        )
        nodes[group_nodes[str(item["group"])]]["children"].append(node_index)

    encoded = base64.b64encode(buffer).decode("ascii")
    gltf = {
        "asset": {
            "version": "2.0",
            "generator": "J40 project CAD scaffold generator",
            "copyright": "Project-owned generated geometry; Sketchfab CC-BY reference attribution retained separately.",
        },
        "scene": 0,
        "scenes": [{"name": "J40 reference scaffold", "nodes": list(group_nodes.values())}],
        "nodes": nodes,
        "meshes": meshes,
        "materials": materials,
        "buffers": [{"uri": f"data:application/octet-stream;base64,{encoded}", "byteLength": len(buffer)}],
        "bufferViews": buffer_views,
        "accessors": accessors,
        "extras": {
            "units": "meters",
            "source_units": "millimetres",
            "scale_factor_m_per_mm": 0.001,
            "source": "generated from project CAD scaffold primitives",
            "detail_revision": DETAIL_REVISION,
            "drive_side": "left-hand drive",
            "driver_side_y_sign": DRIVER_Y_SIGN,
            "part_count": len(model_parts),
        },
    }
    path = OUT_DIR / f"{MODEL_NAME}.gltf"
    path.write_text(json.dumps(gltf, separators=(",", ":")) + "\n", encoding="ascii")
    return path


def write_inventory(model_parts: list[PartType]) -> Path:
    path = OUT_DIR / f"{MODEL_NAME}_parts.csv"
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "group",
                "name",
                "kind",
                "x_mm",
                "y_center_mm",
                "z_mm",
                "length_or_diameter_mm",
                "width_mm",
                "height_mm",
                "confidence",
                "notes",
            ]
        )
        for part in model_parts:
            if isinstance(part, BoxPart):
                writer.writerow(
                    [
                        part.group,
                        part.name,
                        "box",
                        part.x,
                        part.y,
                        part.z,
                        part.length,
                        part.width,
                        part.height,
                        part.confidence,
                        part.notes,
                    ]
                )
            elif isinstance(part, WheelPart):
                writer.writerow(
                    [
                        part.group,
                        part.name,
                        "wheel_cylinder",
                        part.x,
                        part.y,
                        part.z,
                        part.diameter,
                        part.width,
                        "",
                        part.confidence,
                        part.notes,
                    ]
                )
            else:
                writer.writerow(
                    [
                        part.group,
                        part.name,
                        f"cylinder_{part.axis}",
                        part.x,
                        part.y,
                        part.z,
                        part.diameter,
                        part.length,
                        "",
                        part.confidence,
                        part.notes,
                    ]
                )
    return path


def write_notes(model_parts: list[PartType], outputs: list[Path]) -> Path:
    path = REPORT_DIR / f"{MODEL_NAME}_notes.md"
    lines = [
        f"# {MODEL_TITLE}",
        "",
        "This is a project-owned from-scratch CAD scaffold. It uses the CC-BY 1976 FJ40 Sketchfab model and the project photo inventory as visual references, without extracting or copying source mesh data.",
        "",
        "## Basis",
        "",
        "- Toyota representative FJ40 dimensions: 3840 mm length, 1665 mm width, 1950 mm height, 2285 mm wheelbase.",
        "- Open-source visual reference: 1976 Toyota Land Cruiser FJ40 by tonielpro520 on Sketchfab, CC Attribution 4.0.",
        "- Project-photo visual target: sand/beige diesel hardtop J40 with white roof, black bumper/trim, round auxiliary lamps, black window seals, side step boards, and mud-terrain tires.",
        "- Driving layout: left-hand drive. Negative Y is the driver side in this coordinate system.",
        "- This scaffold does not extract or reproduce hidden source mesh data.",
        "",
        "## Outputs",
        "",
    ]
    for output in outputs:
        lines.append(f"- `{output.relative_to(ROOT)}`")
    lines.extend(
        [
            "",
            "## Current CAD Level",
            "",
            "- L0 envelope: boxes/cylinders that locate major vehicle systems.",
            "- L1 reference: named CAD primitives for body, chassis, running gear, engine bay, hardtop, and interior.",
            "- L2 visible-detail scaffold: grille slots/lights, bumper/tow points, hood ribs/latches, hardtop panels/windows/gutters, door hinges/handles/mirrors, LHD dashboard/gauges/switches, seats/belts/pedals, engine-bay accessories/hoses, suspension brackets, shocks, rims, tire lugs, hubs, and body pressings.",
            "- LHD-specific references: left steering wheel/column, left pedal box, left-firewall brake booster/master cylinder, clutch master, lower steering shaft, steering box, pitman arm, drag link, tie rod, and steering damper.",
            "- L3 specific-item references: rear parking-brake cable attachment hardware, equalizer, clevises, return springs, and frame/axle clips.",
            "- Routing references: brake lines, parking-brake cables, battery cable, fuel line, filler neck, exhaust, prop shafts, and measurement datum bars.",
            "- Not fabrication release: mounting holes, curvature, exact frame sweep, body flange geometry, and bracket datums still need physical measurements from the actual truck.",
            "",
            f"Total named parts: {len(model_parts)}",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="ascii")
    return path


def write_manifest(outputs: list[Path], model_parts: list[PartType]) -> Path:
    path = REPORT_DIR / f"{MODEL_NAME}_manifest.json"
    data = {
        "model": MODEL_NAME,
        "detail_revision": DETAIL_REVISION,
        "units": "mm",
        "coordinate_system": "X front bumper to rear, Y centreline left/right, Z ground up",
        "drive_side": "left-hand drive",
        "driver_side_y_sign": DRIVER_Y_SIGN,
        "driver_side": DRIVER_SIDE,
        "basis_dimensions_mm": {"length": 3840, "width": 1665, "height": 1950, "wheelbase": 2285},
        "part_count": len(model_parts),
        "outputs": [str(output.relative_to(ROOT)) for output in outputs],
    }
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="ascii")
    return path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    model_parts = parts()
    outputs = [
        write_scad(model_parts),
        write_freecad_macro(model_parts),
        write_svg(model_parts),
        write_png_preview(model_parts),
        write_dxf(model_parts),
        write_gltf(model_parts),
        write_inventory(model_parts),
    ]
    notes = write_notes(model_parts, outputs)
    manifest = write_manifest(outputs + [notes], model_parts)
    for output in outputs + [notes, manifest]:
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
