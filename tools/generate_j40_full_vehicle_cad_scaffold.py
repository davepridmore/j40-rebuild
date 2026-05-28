from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import html
import json

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "manual" / "cad" / "j40_reference_model" / "04_exports" / "scaffold_rev_a"
REPORT_DIR = ROOT / "data" / "manual" / "cad" / "j40_reference_model" / "05_reports"

MODEL_NAME = "j40_full_vehicle_scaffold_rev_a"


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
    "body_blue": "#78b9c9",
    "canvas": "#d8c3a5",
    "frame": "#2d3033",
    "rubber": "#1d1d1d",
    "metal": "#b8b8b8",
    "interior": "#b87b55",
    "glass": "#6fa5b8",
    "engine": "#3f4245",
    "spring": "#222222",
    "reference": "#e8e8e8",
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
    front_axle_x = 735
    rear_axle_x = front_axle_x + 2285
    track_half = 705
    wheel_z = 395

    # Chassis and running gear.
    box("chassis", "left_frame_rail", 360, -390, 430, 3140, 85, 120, COLORS["frame"], notes="straight ladder-frame reference rail")
    box("chassis", "right_frame_rail", 360, 390, 430, 3140, 85, 120, COLORS["frame"], notes="straight ladder-frame reference rail")
    for idx, x in enumerate([450, 980, 1660, 2420, 3230], start=1):
        box("chassis", f"crossmember_{idx}", x, 0, 455, 85, 880, 95, COLORS["frame"], notes="crossmember station placeholder")
    box("chassis", "front_bumper", 20, 0, 525, 165, 1620, 120, COLORS["metal"], notes="front bumper and tow-eye envelope")
    box("chassis", "rear_bumper", 3665, 0, 530, 145, 1550, 110, COLORS["metal"], notes="rear bumper envelope")
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
    for x, label in [(front_axle_x, "front"), (rear_axle_x, "rear")]:
        cyl("running_gear", f"{label}_left_shock_body", x + 185, -520, 620, "z", 58, 460, COLORS["metal"], notes="shock absorber body reference")
        cyl("running_gear", f"{label}_right_shock_body", x + 185, 520, 620, "z", 58, 460, COLORS["metal"], notes="shock absorber body reference")
        cyl("running_gear", f"{label}_left_hub_cap", x, -840, wheel_z, "y", 220, 80, COLORS["metal"], notes="wheel hub cap detail")
        cyl("running_gear", f"{label}_right_hub_cap", x, 840, wheel_z, "y", 220, 80, COLORS["metal"], notes="wheel hub cap detail")

    # Body lower structure.
    box("body", "floor_pan", 890, 0, 615, 2550, 1330, 55, COLORS["body_blue"], notes="main floor and rear tub floor envelope")
    box("body", "left_rocker_sill", 1000, -720, 665, 2050, 95, 155, COLORS["body_blue"], notes="left rocker/sill envelope")
    box("body", "right_rocker_sill", 1000, 720, 665, 2050, 95, 155, COLORS["body_blue"], notes="right rocker/sill envelope")
    box("body", "left_rear_quarter_panel", 2140, -760, 725, 1270, 70, 610, COLORS["body_blue"], notes="rear tub side panel below soft top")
    box("body", "right_rear_quarter_panel", 2140, 760, 725, 1270, 70, 610, COLORS["body_blue"], notes="rear tub side panel below soft top")
    box("body", "tailgate_panel", 3400, 0, 720, 70, 1430, 650, COLORS["body_blue"], notes="tailgate/rear body closing panel")
    box("body", "firewall", 1135, 0, 690, 80, 1420, 780, COLORS["body_blue"], notes="firewall plane and cowl station")
    box("body", "cowl_top", 1085, 0, 1260, 190, 1460, 110, COLORS["body_blue"], notes="scuttle/cowl top envelope")
    box("body", "grille_panel", 170, 0, 790, 80, 1410, 520, COLORS["body_blue"], notes="front grille plane")
    box("front_detail", "white_grille_surround", 125, 0, 795, 35, 1120, 365, COLORS["reference"], notes="white front grille surround visible in reference")
    box("front_detail", "black_grille_mesh", 105, 0, 910, 30, 640, 155, COLORS["rubber"], notes="black mesh grille area")
    cyl("front_detail", "left_headlamp", 92, -445, 985, "x", 225, 38, COLORS["reference"], notes="round front headlamp")
    cyl("front_detail", "right_headlamp", 92, 445, 985, "x", 225, 38, COLORS["reference"], notes="round front headlamp")
    cyl("front_detail", "left_indicator_lamp", 84, -720, 845, "x", 105, 30, COLORS["interior"], notes="front amber indicator")
    cyl("front_detail", "right_indicator_lamp", 84, 720, 845, "x", 105, 30, COLORS["interior"], notes="front amber indicator")
    cyl("front_detail", "left_fog_lamp", 25, -360, 620, "x", 165, 36, COLORS["reference"], notes="bumper-mounted round fog lamp")
    cyl("front_detail", "right_fog_lamp", 25, 360, 620, "x", 165, 36, COLORS["reference"], notes="bumper-mounted round fog lamp")
    box("body", "hood_closed_reference", 230, 0, 1215, 920, 1390, 55, COLORS["body_blue"], notes="closed hood reference envelope")
    box("body", "hood_open_visual_reference", 420, 0, 1420, 1180, 1390, 35, COLORS["body_blue"], "visual only", "viewer shows hood open; this is a non-kinematic slab reference")
    cyl("body", "hood_left_hinge_axis", 1030, -540, 1288, "y", 28, 230, COLORS["metal"], notes="hood hinge axis placeholder")
    cyl("body", "hood_right_hinge_axis", 1030, 540, 1288, "y", 28, 230, COLORS["metal"], notes="hood hinge axis placeholder")
    box("body", "left_front_fender", 270, -720, 760, 860, 270, 260, COLORS["body_blue"], notes="front wing/fender envelope")
    box("body", "right_front_fender", 270, 720, 760, 860, 270, 260, COLORS["body_blue"], notes="front wing/fender envelope")
    box("body", "left_inner_fender", 290, -520, 800, 800, 70, 420, COLORS["body_blue"], notes="engine-bay inner fender placeholder")
    box("body", "right_inner_fender", 290, 520, 800, 800, 70, 420, COLORS["body_blue"], notes="engine-bay inner fender placeholder")

    # Cabin and soft-top.
    box("body", "windshield_frame", 1155, 0, 1315, 80, 1480, 520, COLORS["body_blue"], notes="upright windshield frame envelope")
    box("body", "windshield_glass", 1160, 0, 1380, 35, 1300, 410, COLORS["glass"], notes="transparent windshield opening reference")
    cyl("body", "windshield_left_wiper", 1110, -250, 1370, "y", 24, 430, COLORS["rubber"], notes="windshield wiper reference")
    cyl("body", "windshield_right_wiper", 1110, 250, 1370, "y", 24, 430, COLORS["rubber"], notes="windshield wiper reference")
    box("soft_top", "canvas_roof", 1210, 0, 1845, 2290, 1540, 100, COLORS["canvas"], notes="soft-top roof envelope")
    box("soft_top", "left_canvas_side", 1240, -790, 1320, 2200, 55, 590, COLORS["canvas"], notes="left soft-top side skin with window openings to be cut later")
    box("soft_top", "right_canvas_side", 1240, 790, 1320, 2200, 55, 590, COLORS["canvas"], notes="right soft-top side skin with window openings to be cut later")
    box("soft_top", "left_front_canvas_window", 1370, -823, 1430, 500, 18, 320, COLORS["glass"], notes="front side soft-top window aperture/glass reference")
    box("soft_top", "left_rear_canvas_window", 2120, -823, 1430, 610, 18, 320, COLORS["glass"], notes="rear side soft-top window aperture/glass reference")
    box("soft_top", "right_front_canvas_window", 1370, 823, 1430, 500, 18, 320, COLORS["glass"], notes="front side soft-top window aperture/glass reference")
    box("soft_top", "right_rear_canvas_window", 2120, 823, 1430, 610, 18, 320, COLORS["glass"], notes="rear side soft-top window aperture/glass reference")
    box("soft_top", "rear_canvas_panel", 3440, 0, 1320, 55, 1540, 590, COLORS["canvas"], notes="rear soft-top panel")
    for x, label in [(1290, "front"), (1960, "middle"), (2640, "rear")]:
        box("soft_top", f"{label}_soft_top_bow", x, 0, 1740, 45, 1510, 75, COLORS["metal"], notes="soft-top bow/tube station")
    for idx, x in enumerate([1460, 1740, 2020, 2300, 2580, 2860, 3140], start=1):
        box("soft_top", f"left_canvas_tie_down_{idx}", x, -835, 1180, 35, 26, 105, COLORS["rubber"], notes="soft-top tie-down strap visible on side")
        box("soft_top", f"right_canvas_tie_down_{idx}", x, 835, 1180, 35, 26, 105, COLORS["rubber"], notes="soft-top tie-down strap visible on side")
    box("body", "left_door_open_reference", 1180, -910, 760, 800, 70, 850, COLORS["body_blue"], "visual only", "viewer shows door open; final hinge arc requires real model/measurements")
    box("body", "right_door_closed_reference", 1180, 760, 760, 800, 70, 850, COLORS["body_blue"], notes="right door closed envelope")
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
    box("interior", "steering_column", 1315, -360, 935, 520, 60, 60, COLORS["metal"], notes="steering column envelope, left-hand-drive visual")
    cyl("interior", "steering_wheel", 1240, -420, 1210, "x", 380, 32, COLORS["rubber"], notes="steering wheel disk placeholder")
    cyl("interior", "steering_wheel_hub", 1230, -420, 1210, "x", 135, 55, COLORS["metal"], notes="steering wheel hub")
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
        "// J40 full vehicle CAD scaffold Rev A",
        "// Units: millimetres. Coordinate system: X front to rear, Y centreline left/right, Z ground up.",
        "// Generated by tools/generate_j40_full_vehicle_cad_scaffold.py.",
        "// This is a project-owned reference scaffold, not a direct extraction of the licensed mesh.",
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
        "# J40 full vehicle CAD scaffold Rev A",
        "# Units: millimetres. Run inside FreeCAD.",
        "# Generated by tools/generate_j40_full_vehicle_cad_scaffold.py.",
        "import FreeCAD as App",
        "import Part",
        "",
        "doc = App.newDocument('j40_full_vehicle_scaffold_rev_a')",
        "",
        "def set_color(obj, rgb):",
        "    if hasattr(obj, 'ViewObject'):",
        "        obj.ViewObject.ShapeColor = rgb",
        "",
        "def add_box(name, x, y_center, z, length, width, height, rgb):",
        "    shape = Part.makeBox(length, width, height, App.Vector(x, y_center - width / 2, z))",
        "    obj = doc.addObject('Part::Feature', name)",
        "    obj.Shape = shape",
        "    set_color(obj, rgb)",
        "    return obj",
        "",
        "def add_cylinder(name, x, y, z, axis, diameter, length, rgb):",
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
        "    set_color(obj, rgb)",
        "    return obj",
        "",
        "def add_wheel(name, x, y_center, z, diameter, width):",
        "    tire = doc.addObject('Part::Feature', name + '_tire')",
        "    tire.Shape = Part.makeCylinder(diameter / 2, width, App.Vector(x, y_center - width / 2, z), App.Vector(0, 1, 0))",
        "    set_color(tire, (0.03, 0.03, 0.03))",
        "    rim = doc.addObject('Part::Feature', name + '_rim')",
        "    rim.Shape = Part.makeCylinder(diameter * 0.26, width + 8, App.Vector(x, y_center - (width + 8) / 2, z), App.Vector(0, 1, 0))",
        "    set_color(rim, (0.72, 0.72, 0.72))",
        "    hub = doc.addObject('Part::Feature', name + '_hub')",
        "    hub.Shape = Part.makeCylinder(diameter * 0.15, width + 14, App.Vector(x, y_center - (width + 14) / 2, z), App.Vector(0, 1, 0))",
        "    set_color(hub, (0.10, 0.10, 0.10))",
        "    return tire",
        "",
    ]
    for part in model_parts:
        safe = part.name.replace("-", "_").replace(" ", "_")
        if isinstance(part, BoxPart):
            color = hex_to_fc_color(part.color)
            lines.append(
                "add_box("
                f"{safe!r}, {part.x:g}, {part.y:g}, {part.z:g}, {part.length:g}, {part.width:g}, {part.height:g}, "
                f"({color[0]:.3f}, {color[1]:.3f}, {color[2]:.3f}))"
            )
        elif isinstance(part, WheelPart):
            lines.append(
                f"add_wheel({safe!r}, {part.x:g}, {part.y:g}, {part.z:g}, {part.diameter:g}, {part.width:g})"
            )
        else:
            color = hex_to_fc_color(part.color)
            lines.append(
                "add_cylinder("
                f"{safe!r}, {part.x:g}, {part.y:g}, {part.z:g}, {part.axis!r}, {part.diameter:g}, {part.length:g}, "
                f"({color[0]:.3f}, {color[1]:.3f}, {color[2]:.3f}))"
            )
    lines.extend(["", "doc.recompute()", "Gui.SendMsgToActiveView('ViewFit') if 'Gui' in globals() else None", ""])
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
    width = 1600
    height = 1120
    scale = 0.24
    panels = {
        "plan": (40, 95, "PLAN X/Y"),
        "side": (40, 500, "SIDE X/Z"),
        "front": (1120, 500, "FRONT Y/Z"),
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
        '<rect x="0" y="0" width="1600" height="1120" fill="#ffffff"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;font-size:14px;fill:#202124}.label{font-size:10px;fill:#333}.title{font-size:22px;font-weight:700}</style>',
        '<text class="title" x="40" y="32">J40 Full Vehicle CAD Scaffold Rev A</text>',
        '<text x="40" y="52">Units mm. Reference scaffold only; refine after licensed mesh and vehicle measurements arrive.</text>',
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
    width = 1600
    height = 1120
    scale = 0.24
    image = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image, "RGBA")
    font = ImageFont.load_default()
    panels = {
        "plan": (40, 95, "PLAN X/Y"),
        "side": (40, 500, "SIDE X/Z"),
        "front": (1120, 500, "FRONT Y/Z"),
    }

    def tx(view: str, x: float, y: float) -> tuple[float, float]:
        ox, oy, _ = panels[view]
        if view == "plan":
            return ox + x * scale, oy + (900 - y) * scale
        if view == "side":
            return ox + x * scale, oy + (2050 - y) * scale
        return ox + (900 + x) * scale, oy + (2050 - y) * scale

    draw.text((40, 18), "J40 Full Vehicle CAD Scaffold Rev A", fill=(32, 33, 36, 255), font=font)
    draw.text(
        (40, 38),
        "Units mm. Reference scaffold only; refine after licensed mesh and vehicle measurements arrive.",
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
        "# J40 Full Vehicle CAD Scaffold Rev A",
        "",
        "This is a project-owned CAD scaffold built before the licensed paid model ZIP is available.",
        "",
        "## Basis",
        "",
        "- Toyota representative FJ40 dimensions: 3840 mm length, 1665 mm width, 1950 mm height, 2285 mm wheelbase.",
        "- Visible Sketchfab reference: soft-top FJ40 with open hood, open driver door, detailed interior, chassis, engine, suspension, and brakes.",
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
            "- L1 reference: named CAD primitives for body, chassis, running gear, engine bay, soft top, and interior.",
            "- L2 visible-detail scaffold: grille/lights, bumper/tow points, hood hinges, soft-top windows/straps, door hinges/handles, dashboard/gauges, steering wheel, shifters, engine-bay hoses/stacks, shocks, and hub caps.",
            "- Not fabrication release: mounting holes, curvature, exact frame sweep, body flange geometry, and bracket datums still need licensed mesh and vehicle measurements.",
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
        "units": "mm",
        "coordinate_system": "X front bumper to rear, Y centreline left/right, Z ground up",
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
        write_inventory(model_parts),
    ]
    notes = write_notes(model_parts, outputs)
    manifest = write_manifest(outputs + [notes], model_parts)
    for output in outputs + [notes, manifest]:
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
