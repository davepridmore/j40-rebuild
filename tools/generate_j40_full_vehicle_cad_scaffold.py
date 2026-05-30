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
OUT_DIR = ROOT / "data" / "manual" / "cad" / "j40_reference_model" / "04_exports" / "scaffold_rev_c"
REPORT_DIR = ROOT / "data" / "manual" / "cad" / "j40_reference_model" / "05_reports"
AS_FITTED_ROUTE_SCOPE = REPORT_DIR / "j40_as_fitted_route_model_scope_20260531.csv"
AS_FITTED_ROUTE_MODEL_COVERAGE = REPORT_DIR / "j40_as_fitted_route_model_coverage_20260531.csv"

MODEL_NAME = "j40_full_vehicle_scaffold_rev_c"
MODEL_TITLE = "J40 Full Vehicle CAD Scaffold Rev C - RHD Digital Twin Evidence Pass"
MODEL_SHORT_TITLE = "J40 full vehicle CAD scaffold Rev C"
DETAIL_REVISION = "rhd_classic_rear_glazing_project_digital_twin_evidence_pass"
DRIVER_LAYOUT = "right-hand drive"
TRAFFIC_SIDE = "left-side traffic"
DRIVER_SIDE = "right"
DRIVER_Y_SIGN = 1
DRIVER_Y = 420
PASSENGER_Y = -420
DRIVER_Y_DIRECTION = "positive" if DRIVER_Y_SIGN > 0 else "negative"
DRIVER_LAYOUT_NOTE = f"{DRIVER_LAYOUT.capitalize()} layout for {TRAFFIC_SIDE}; {DRIVER_Y_DIRECTION} Y is the driver side."

ONLINE_REFERENCE_ROWS = [
    {
        "source_id": "sketchfab-tonielpro520-1976-fj40",
        "title": "1976 Toyota Land Cruiser FJ40",
        "url": "https://sketchfab.com/3d-models/1976-toyota-land-cruiser-fj40-a4e58b09ce48444ca6164834c310880d",
        "source_type": "downloadable 3D model",
        "permission_basis": "Creative Commons Attribution 4.0; author credit required; commercial use allowed",
        "rev_c_use": "overall hardtop silhouette, body tub packaging, material separation, and project-owned remodelling reference",
    },
    {
        "source_id": "sketchfab-game-garage-fj40",
        "title": "Toyota Land Cruiser",
        "url": "https://sketchfab.com/3d-models/toyota-land-cruiser-cbcbd901e8874205b5be294fa3dd3df2",
        "source_type": "downloadable game-ready 3D model",
        "permission_basis": "Creative Commons Attribution listing; author credit required",
        "rev_c_use": "high-density material/texture cue set for window rubber, lights, trim, wheels, and visible interior detail",
    },
    {
        "source_id": "3dmodels-1979-j40-hard-top",
        "title": "Toyota Land Cruiser (J40) Hard Top 1979",
        "url": "https://3dmodels.org/3d-models/toyota-land-cruiser-j40-hard-top-1979/",
        "source_type": "commercial 3D model preview gallery",
        "permission_basis": "commercial use covered by project owner; public previews used for reference cues",
        "rev_c_use": "front/rear orthographic proportions, classic rounded rear hardtop glazing, grille/lamp treatment, wheel/tire material breaks, spare carrier",
    },
    {
        "source_id": "cgtrader-hard-top-bj44v-1979-print",
        "title": "TOYOTA LAND-CRUISER J40 HARD TOP BJ44V 1979",
        "url": "https://www.cgtrader.com/3d-print-models/hobby-diy/automotive/toyota-land-cruiser-j40-hard-top-bj44v-1979-df76b215-58fa-40f4-82f4-811350605600",
        "source_type": "commercial printable 3D model listing",
        "permission_basis": "commercial use covered by project owner; listing cues used unless local files are placed in inbox",
        "rev_c_use": "separate-body/open-hood/chassis/wheel/glass part breakdown and hood-understructure targets",
    },
    {
        "source_id": "toyota-epc-fj40-body-interior",
        "title": "Toyota Land Cruiser FJ40-KC Body and Interior Parts Groups",
        "url": "https://toyota.epc-data.com/land_cruiser/fj40/61645/body/",
        "source_type": "online parts catalog representation",
        "permission_basis": "parts group names used as factual service-reference cues",
        "rev_c_use": "cab/body mounting, bumper stays, grille, hood lock/hinge, cowl/front ventilator, side/roof/rear ventilators, spare carrier",
    },
    {
        "source_id": "toyota-gr-heritage-40-current-page",
        "title": "Toyota GR Heritage Land Cruiser 40",
        "url": "https://toyotagazooracing.com/gr/heritage/landcruiser40/",
        "source_type": "official Toyota heritage parts program",
        "permission_basis": "public Toyota product and parts-program page used for factual availability and naming cues",
        "rev_c_use": "current official parts program vocabulary, order timing cues, and category cross-checks",
    },
    {
        "source_id": "toyota-gr-heritage-40-parts-list-2026",
        "title": "Land Cruiser 40 GR Heritage Parts List",
        "url": "https://toyotagazooracing.com/-/media/TMC/tgr/global/contents/gr/heritage/pdf/Landcruiser40_en.pdf",
        "source_type": "official Toyota heritage parts list",
        "permission_basis": "public Toyota parts list used for factual part-name cues",
        "rev_c_use": "parking brake, rear brake tubes, wiper pivot caps, mirror packing, fuel inlet hose, rear combination lamp segmentation",
    },
    {
        "source_id": "ih8mud-fj40-frame-cad-thread",
        "title": "A lot of people have been asking for this, CAD model for FJ40 frame",
        "url": "https://forum.ih8mud.com/threads/a-lot-of-people-have-been-asking-for-this-cad-model-for-fj40-frame.798358/",
        "source_type": "community CAD and dimensional lead",
        "permission_basis": "public forum reference; per-file rights and accuracy must be verified before local use",
        "rev_c_use": "candidate frame rail, crossmember, and bracket datum leads for comparison against measured truck geometry",
    },
    {
        "source_id": "ih8mud-40-series-cad-file-repository",
        "title": "3D Print and CAD File Repository - 40 Series",
        "url": "https://forum.ih8mud.com/threads/3d-print-and-cad-file-repository-40-series.1281295/",
        "source_type": "community CAD/STL repository",
        "permission_basis": "public forum index; per-file licenses vary and must be checked",
        "rev_c_use": "small part modelling leads such as knobs, covers, bezels, hose separators, and license lamp covers",
    },
]


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


@dataclass(frozen=True)
class MeshPart:
    group: str
    name: str
    vertices: tuple[tuple[float, float, float], ...]
    faces: tuple[tuple[int, ...], ...]
    color: str
    confidence: str
    notes: str


PartType = BoxPart | WheelPart | CylinderPart | MeshPart


COLORS = {
    "body_sand": "#cfc6aa",
    "body_shadow": "#9d967e",
    "body_highlight": "#e4dcc7",
    "roof_white": "#f1eee4",
    "black_trim": "#111315",
    "frame": "#2d3033",
    "rubber": "#1d1d1d",
    "metal": "#b8b8b8",
    "chrome": "#d9d5c8",
    "interior": "#b87b55",
    "glass": "#6fa5b8",
    "glass_dark": "#26383f",
    "engine": "#3f4245",
    "spring": "#222222",
    "reference": "#e8e8e8",
    "electrical": "#d64737",
    "amber": "#d97824",
    "grille_yellow": "#d6bf47",
    "fluid": "#4f7f55",
    "brass": "#c49a3d",
    "datum": "#7c6fcb",
    "route_power": "#d64737",
    "route_fluid": "#3a78c2",
    "route_control": "#7b5a3a",
    "clearance": "#b596e3",
}


def read_as_fitted_route_scope() -> dict[str, dict[str, str]]:
    if not AS_FITTED_ROUTE_SCOPE.exists():
        return {}
    with AS_FITTED_ROUTE_SCOPE.open(newline="", encoding="utf-8-sig") as handle:
        return {row.get("route_id", ""): row for row in csv.DictReader(handle) if row.get("route_id")}


def as_fitted_route_model_matches(model_parts: list[PartType]) -> dict[str, list[PartType]]:
    route_scope = read_as_fitted_route_scope()
    matches: dict[str, list[PartType]] = {route_id: [] for route_id in route_scope}
    for part in model_parts:
        if part.group != "as_fitted_routes":
            continue
        for route_id in route_scope:
            if route_id in part.notes:
                matches[route_id].append(part)
    return matches


def as_fitted_route_metrics(model_parts: list[PartType]) -> dict[str, int]:
    route_scope = read_as_fitted_route_scope()
    matches = as_fitted_route_model_matches(model_parts)
    return {
        "scope_rows": len(route_scope),
        "represented_rows": sum(1 for route_id in route_scope if matches.get(route_id)),
        "route_part_count": sum(1 for part in model_parts if part.group == "as_fitted_routes"),
        "clearance_part_count": sum(1 for part in model_parts if part.group == "mechanical_clearance"),
    }


def slug(value: str) -> str:
    token = value.lower().replace("-", "_").replace("/", "_")
    return "".join(char if char.isalnum() or char == "_" else "_" for char in token).strip("_")


def parts() -> list[PartType]:
    p: list[PartType] = []
    route_scope = read_as_fitted_route_scope()

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

    def mesh(
        group: str,
        name: str,
        vertices: list[tuple[float, float, float]],
        faces: list[tuple[int, ...]],
        color: str,
        confidence: str = "L3 reference-shaped surface",
        notes: str = "",
    ) -> None:
        p.append(MeshPart(group, name, tuple(vertices), tuple(faces), color, confidence, notes))

    def plate_text(
        group: str,
        prefix: str,
        x: float,
        y_center: float,
        z_center: float,
        text: str,
        color: str,
        confidence: str,
        notes: str,
    ) -> None:
        char_width = 34.0
        char_height = 72.0
        gap = 9.0
        stroke = 7.0
        total_width = len(text) * char_width + (len(text) - 1) * gap
        y_start = y_center - total_width / 2 + char_width / 2
        z_top = z_center + char_height / 2 - stroke / 2
        z_bottom = z_center - char_height / 2 + stroke / 2
        segment_defs = {
            "top": (0.0, z_top - z_center, char_width, stroke),
            "mid": (0.0, 0.0, char_width, stroke),
            "bottom": (0.0, z_bottom - z_center, char_width, stroke),
            "ul": (-(char_width - stroke) / 2, char_height / 4, stroke, char_height / 2),
            "ur": ((char_width - stroke) / 2, char_height / 4, stroke, char_height / 2),
            "ll": (-(char_width - stroke) / 2, -char_height / 4, stroke, char_height / 2),
            "lr": ((char_width - stroke) / 2, -char_height / 4, stroke, char_height / 2),
            "center": (0.0, 0.0, stroke, char_height),
        }
        patterns = {
            "0": ("top", "bottom", "ul", "ur", "ll", "lr"),
            "1": ("ur", "lr"),
            "2": ("top", "ur", "mid", "ll", "bottom"),
            "3": ("top", "ur", "mid", "lr", "bottom"),
            "4": ("ul", "ur", "mid", "lr"),
            "5": ("top", "ul", "mid", "lr", "bottom"),
            "6": ("top", "ul", "mid", "ll", "lr", "bottom"),
            "7": ("top", "ur", "lr"),
            "8": ("top", "mid", "bottom", "ul", "ur", "ll", "lr"),
            "9": ("top", "mid", "bottom", "ul", "ur", "lr"),
            "B": ("top", "mid", "bottom", "ul", "ll", "ur", "lr"),
            "S": ("top", "mid", "bottom", "ul", "lr"),
            "N": ("ul", "ll", "ur", "lr", "center"),
        }
        for char_idx, char in enumerate(text.upper()):
            char_y = y_start + char_idx * (char_width + gap)
            for segment in patterns.get(char, ()):
                offset_y, offset_z, width, height = segment_defs[segment]
                box(
                    group,
                    f"{prefix}_{char_idx + 1}_{char}_{segment}",
                    x,
                    char_y + offset_y,
                    z_center + offset_z,
                    8,
                    width,
                    height,
                    color,
                    confidence,
                    notes,
                )

    def route_notes(route_id: str, fallback: str) -> str:
        row = route_scope.get(route_id, {})
        if not row:
            return f"{route_id}: {fallback}; route scope row not found."
        fields = [
            f"{route_id} {row.get('route_name', fallback)}",
            f"target {row.get('model_level_target', '')}",
            f"capture {row.get('geometry_to_capture', '')}",
            f"clearance {row.get('clearance_checks', '')}",
            f"release {row.get('release_gate', '')}",
            f"status {row.get('status', '')}",
        ]
        return "; ".join(field for field in fields if field and not field.endswith(" "))

    def route_segment(
        route_id: str,
        segment_name: str,
        x: float,
        y: float,
        z: float,
        axis: str,
        diameter: float,
        length: float,
        color: str,
        confidence: str = "L1 as-fitted route scope",
    ) -> None:
        row = route_scope.get(route_id, {})
        name = f"{slug(route_id)}_{slug(row.get('route_name', segment_name))}_{slug(segment_name)}"
        cyl("as_fitted_routes", name, x, y, z, axis, diameter, length, color, confidence, route_notes(route_id, segment_name))

    def route_clip(route_id: str, segment_name: str, x: float, y: float, z: float, color: str = COLORS["metal"]) -> None:
        row = route_scope.get(route_id, {})
        name = f"{slug(route_id)}_{slug(row.get('route_name', segment_name))}_{slug(segment_name)}_clip"
        box("as_fitted_routes", name, x, y, z, 42, 34, 34, color, "L2 route support placeholder", route_notes(route_id, segment_name))

    def rounded_rect_profile(width: float, height: float, radius: float, segments: int = 5) -> list[tuple[float, float]]:
        half_width = width / 2
        half_height = height / 2
        corner_radius = min(radius, half_width - 1, half_height - 1)
        profile: list[tuple[float, float]] = []
        corners = [
            (half_width - corner_radius, half_height - corner_radius, 0, 90),
            (-half_width + corner_radius, half_height - corner_radius, 90, 180),
            (-half_width + corner_radius, -half_height + corner_radius, 180, 270),
            (half_width - corner_radius, -half_height + corner_radius, 270, 360),
        ]
        for cx, cz, start_deg, end_deg in corners:
            for step in range(segments + 1):
                if profile and step == 0:
                    continue
                angle = math.radians(start_deg + (end_deg - start_deg) * step / segments)
                profile.append((cx + math.cos(angle) * corner_radius, cz + math.sin(angle) * corner_radius))
        return profile

    def rounded_side_window_mesh(
        name: str,
        x_center: float,
        y_center: float,
        z_center: float,
        width: float,
        height: float,
        thickness: float,
        radius: float,
        color: str,
        confidence: str,
        notes: str,
    ) -> None:
        profile = rounded_rect_profile(width, height, radius)
        vertices = [(x_center + dx, y_center - thickness / 2, z_center + dz) for dx, dz in profile]
        vertices.extend((x_center + dx, y_center + thickness / 2, z_center + dz) for dx, dz in profile)
        count = len(profile)
        faces: list[tuple[int, ...]] = [tuple(range(count)), tuple(range(count, count * 2))[::-1]]
        faces.extend((idx, (idx + 1) % count, (idx + 1) % count + count, idx + count) for idx in range(count))
        mesh("hard_top", name, vertices, faces, color, confidence, notes)

    def rounded_rear_window_mesh(
        name: str,
        x_center: float,
        y_center: float,
        z_center: float,
        width: float,
        height: float,
        thickness: float,
        radius: float,
        color: str,
        confidence: str,
        notes: str,
    ) -> None:
        profile = rounded_rect_profile(width, height, radius)
        vertices = [(x_center - thickness / 2, y_center + dy, z_center + dz) for dy, dz in profile]
        vertices.extend((x_center + thickness / 2, y_center + dy, z_center + dz) for dy, dz in profile)
        count = len(profile)
        faces: list[tuple[int, ...]] = [tuple(range(count)), tuple(range(count, count * 2))[::-1]]
        faces.extend((idx, (idx + 1) % count, (idx + 1) % count + count, idx + count) for idx in range(count))
        mesh("hard_top", name, vertices, faces, color, confidence, notes)

    def wedge_mesh(
        group: str,
        name: str,
        x_front: float,
        x_rear: float,
        y_left: float,
        y_right: float,
        z_front_low: float,
        z_rear_low: float,
        z_front_high: float,
        z_rear_high: float,
        color: str,
        confidence: str,
        notes: str,
    ) -> None:
        vertices = [
            (x_front, y_left, z_front_low),
            (x_front, y_right, z_front_low),
            (x_rear, y_right, z_rear_low),
            (x_rear, y_left, z_rear_low),
            (x_front, y_left, z_front_high),
            (x_front, y_right, z_front_high),
            (x_rear, y_right, z_rear_high),
            (x_rear, y_left, z_rear_high),
        ]
        faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
        mesh(group, name, vertices, faces, color, confidence, notes)

    def crowned_panel_mesh(
        group: str,
        name: str,
        x_front: float,
        x_rear: float,
        y_left: float,
        y_right: float,
        z_edge_front: float,
        z_edge_rear: float,
        crown_mm: float,
        thickness: float,
        color: str,
        confidence: str,
        notes: str,
    ) -> None:
        y_mid = (y_left + y_right) / 2
        vertices = [
            (x_front, y_left, z_edge_front),
            (x_front, y_mid, z_edge_front + crown_mm),
            (x_front, y_right, z_edge_front),
            (x_rear, y_left, z_edge_rear),
            (x_rear, y_mid, z_edge_rear + crown_mm),
            (x_rear, y_right, z_edge_rear),
            (x_front, y_left, z_edge_front - thickness),
            (x_front, y_mid, z_edge_front + crown_mm - thickness),
            (x_front, y_right, z_edge_front - thickness),
            (x_rear, y_left, z_edge_rear - thickness),
            (x_rear, y_mid, z_edge_rear + crown_mm - thickness),
            (x_rear, y_right, z_edge_rear - thickness),
        ]
        faces = [
            (0, 3, 4, 1),
            (1, 4, 5, 2),
            (6, 7, 10, 9),
            (7, 8, 11, 10),
            (0, 1, 7, 6),
            (1, 2, 8, 7),
            (3, 9, 10, 4),
            (4, 10, 11, 5),
            (0, 6, 9, 3),
            (2, 5, 11, 8),
        ]
        mesh(group, name, vertices, faces, color, confidence, notes)

    # Published representative FJ40 dimensions from Toyota: 3840 L, 1665 W, 1950 H, 2285 WB.
    # Coordinate system: X front bumper to rear, Y centerline left/right, Z ground up, units mm.
    # This truck is modelled as right-hand drive: positive Y is the driver's side.
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
    box("body", "hood_closed_reference", 230, 0, 1215, 920, 1390, 38, COLORS["body_sand"], notes="closed hood lower envelope")
    crowned_panel_mesh(
        "body",
        "hood_crowned_closed_skin",
        135,
        1058,
        -642,
        642,
        1230,
        1296,
        26,
        20,
        COLORS["body_sand"],
        "L4 gallery-shaped surface",
        "closed hood crown and rear rise shaped from public front, side, top, wire, and clay gallery renders",
    )
    wedge_mesh(
        "body",
        "hood_front_rolled_lip_surface",
        96,
        150,
        -610,
        610,
        1204,
        1218,
        1248,
        1254,
        COLORS["body_shadow"],
        "L4 gallery-shaped surface",
        "rolled front hood lip visible above the grille in the front renders",
    )
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
    box("hard_top", "white_hardtop_roof", 1210, 0, 1838, 2290, 1540, 58, COLORS["roof_white"], notes="hardtop roof lower envelope under crowned skin")
    crowned_panel_mesh(
        "hard_top",
        "white_hardtop_crowned_roof_skin",
        1125,
        3440,
        -760,
        760,
        1886,
        1896,
        46,
        26,
        COLORS["roof_white"],
        "L4 gallery-shaped surface",
        "thin crowned hardtop roof and slight rear lift shaped from top, side, rear, wire, and clay gallery renders",
    )
    box("hard_top", "left_hardtop_side_panel", 1240, -790, 1320, 2200, 55, 590, COLORS["body_sand"], notes="left hardtop side shell")
    box("hard_top", "right_hardtop_side_panel", 1240, 790, 1320, 2200, 55, 590, COLORS["body_sand"], notes="right hardtop side shell")
    box("hard_top", "left_front_hardtop_window", 1420, -823, 1435, 500, 20, 320, COLORS["glass"], notes="left sliding/side hardtop window glass")
    box("hard_top", "right_front_hardtop_window", 1420, 823, 1435, 500, 20, 320, COLORS["glass"], notes="right sliding/side hardtop window glass")
    rounded_side_window_mesh("left_rear_hardtop_window", 2190, -832, 1595, 610, 320, 24, 92, COLORS["glass"], "L1 visible-detail primitive", "left classic rounded rear hardtop side window glass")
    rounded_side_window_mesh("right_rear_hardtop_window", 2190, 832, 1595, 610, 320, 24, 92, COLORS["glass"], "L1 visible-detail primitive", "right classic rounded rear hardtop side window glass")
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
    box("interior", "steering_column", 1135, DRIVER_Y, 935, 590, 60, 60, COLORS["metal"], notes=f"steering column envelope, {DRIVER_LAYOUT} driver side")
    cyl("interior", "steering_wheel", 1240, DRIVER_Y, 1210, "x", 380, 32, COLORS["rubber"], notes=f"steering wheel disk placeholder on {DRIVER_LAYOUT} side")
    cyl("interior", "steering_wheel_hub", 1230, DRIVER_Y, 1210, "x", 135, 55, COLORS["metal"], notes="steering wheel hub")
    for idx, y in enumerate([DRIVER_Y + offset * DRIVER_Y_SIGN for offset in (140, 50, -40, -130)], start=1):
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

    # Gallery shaping pass from the 12 public 3DModels.org preview renders:
    # perspective front/rear, wire, side, top, front orthographic, and clay views.
    wedge_mesh(
        "body",
        "windshield_raked_glass_surface",
        1110,
        1148,
        -602,
        602,
        1378,
        1378,
        1722,
        1700,
        COLORS["glass"],
        "L4 gallery-shaped surface",
        "single raked windshield plane replacing a flat envelope impression from front, side, and clay renders",
    )
    wedge_mesh(
        "front_detail",
        "front_grille_inset_rounded_surround_surface",
        56,
        106,
        -585,
        585,
        802,
        820,
        1125,
        1100,
        COLORS["reference"],
        "L4 gallery-shaped surface",
        "slightly inset grille surround shaped from front, wire, and clay renders",
    )
    wedge_mesh(
        "chassis",
        "front_bumper_swept_main_face",
        -18,
        92,
        -760,
        760,
        484,
        520,
        608,
        620,
        COLORS["black_trim"],
        "L4 gallery-shaped surface",
        "swept front bumper face from front orthographic and front three-quarter renders",
    )
    wedge_mesh(
        "chassis",
        "rear_bumper_swept_main_face",
        3638,
        3750,
        -730,
        730,
        492,
        520,
        604,
        612,
        COLORS["black_trim"],
        "L4 gallery-shaped surface",
        "swept rear bumper face from rear orthographic and rear three-quarter renders",
    )
    crowned_panel_mesh(
        "hard_top",
        "front_roof_header_overhang_skin",
        1092,
        1208,
        -786,
        786,
        1808,
        1852,
        26,
        16,
        COLORS["roof_white"],
        "L4 gallery-shaped surface",
        "front roof header overhang lip visible in front, side, top, and clay renders",
    )
    crowned_panel_mesh(
        "hard_top",
        "rear_roof_overhang_skin",
        3360,
        3508,
        -776,
        776,
        1862,
        1848,
        28,
        18,
        COLORS["roof_white"],
        "L4 gallery-shaped surface",
        "rear hardtop roof overhang lip and slight crown from top and rear renders",
    )
    crowned_panel_mesh(
        "hard_top",
        "rear_barn_door_left_subtle_crown",
        3484,
        3534,
        -690,
        -18,
        920,
        924,
        18,
        16,
        COLORS["body_sand"],
        "L4 gallery-shaped surface",
        "left rear barn-door skin has a slight crown instead of a flat slab in rear and clay renders",
    )
    crowned_panel_mesh(
        "hard_top",
        "rear_barn_door_right_subtle_crown",
        3484,
        3534,
        18,
        690,
        920,
        924,
        18,
        16,
        COLORS["body_sand"],
        "L4 gallery-shaped surface",
        "right rear barn-door skin has a slight crown instead of a flat slab in rear and clay renders",
    )
    for side, sign, y_sign in side_pairs:
        side_name = "left" if y_sign < 0 else "right"
        y_inner = 646 * y_sign
        y_outer = 846 * y_sign
        y0 = min(y_inner, y_outer)
        y1 = max(y_inner, y_outer)
        wedge_mesh(
            "body",
            f"{side_name}_front_fender_sloped_outer_skin",
            118,
            1035,
            y0,
            y1,
            706,
            744,
            1048,
            1242,
            COLORS["body_sand"],
            "L4 gallery-shaped surface",
            "front wing side skin slopes up to the cowl instead of reading as a rectangular block",
        )
        wedge_mesh(
            "chassis",
            f"{side_name}_front_bumper_swept_return",
            24,
            128,
            min(720 * y_sign, 846 * y_sign),
            max(720 * y_sign, 846 * y_sign),
            500,
            548,
            610,
            620,
            COLORS["black_trim"],
            "L4 gallery-shaped surface",
            "front bumper side return shaped from front and three-quarter renders",
        )
        wedge_mesh(
            "chassis",
            f"{side_name}_rear_bumper_swept_return",
            3628,
            3735,
            min(695 * y_sign, 812 * y_sign),
            max(695 * y_sign, 812 * y_sign),
            502,
            540,
            604,
            612,
            COLORS["black_trim"],
            "L4 gallery-shaped surface",
            "rear bumper side return shaped from rear and three-quarter renders",
        )
        wedge_mesh(
            "body",
            f"{side_name}_front_fender_rolled_upper_crown",
            155,
            1015,
            min(560 * y_sign, 754 * y_sign),
            max(560 * y_sign, 754 * y_sign),
            1062,
            1238,
            1110,
            1268,
            COLORS["body_highlight"],
            "L4 gallery-shaped surface",
            "rolled front fender crown visible in front, side, top, and wire renders",
        )
        wedge_mesh(
            "body",
            f"{side_name}_cowl_side_blend_surface",
            960,
            1165,
            min(660 * y_sign, 815 * y_sign),
            max(660 * y_sign, 815 * y_sign),
            1116,
            1214,
            1340,
            1410,
            COLORS["body_sand"],
            "L4 gallery-shaped surface",
            "cowl-to-windshield side blend guided by front, side, and clay renders",
        )
        wedge_mesh(
            "body",
            f"{side_name}_door_outer_skin_tapered_surface",
            1128,
            1938,
            min(734 * y_sign, 824 * y_sign),
            max(734 * y_sign, 824 * y_sign),
            748,
            748,
            1270,
            1308,
            COLORS["body_sand"],
            "L4 gallery-shaped surface",
            "door skin follows the upright but slightly crowned BJ44 side profile in the side and clay renders",
        )
        wedge_mesh(
            "body",
            f"{side_name}_rear_quarter_waist_tapered_surface",
            1942,
            3385,
            min(730 * y_sign, 830 * y_sign),
            max(730 * y_sign, 830 * y_sign),
            724,
            746,
            1305,
            1278,
            COLORS["body_sand"],
            "L4 gallery-shaped surface",
            "rear tub side taper and waist line shaped from side, rear, top, wire, and clay renders",
        )
        wedge_mesh(
            "hard_top",
            f"{side_name}_hardtop_side_tapered_upper_skin",
            1212,
            3425,
            min(748 * y_sign, 820 * y_sign),
            max(748 * y_sign, 820 * y_sign),
            1308,
            1300,
            1790,
            1782,
            COLORS["body_sand"],
            "L4 gallery-shaped surface",
            "hardtop upper side panel tapers under the roof gutter in side, rear, wire, and clay renders",
        )
        wedge_mesh(
            "hard_top",
            f"{side_name}_hardtop_lower_side_roll_surface",
            1225,
            3415,
            min(742 * y_sign, 812 * y_sign),
            max(742 * y_sign, 812 * y_sign),
            1260,
            1258,
            1345,
            1332,
            COLORS["body_shadow"],
            "L4 gallery-shaped surface",
            "rolled hardtop lower side break below windows from side and rear renders",
        )
        wedge_mesh(
            "hard_top",
            f"{side_name}_hardtop_rear_corner_radius_facet",
            3365,
            3470,
            min(650 * y_sign, 806 * y_sign),
            max(650 * y_sign, 806 * y_sign),
            1300,
            1308,
            1780,
            1762,
            COLORS["body_shadow"],
            "L4 gallery-shaped surface",
            "faceted rear hardtop corner radius from rear, top, wire, and clay renders",
        )
        for arch_idx, (axle_name, axle_x, radius, z_base) in enumerate(
            [("front", front_axle_x, 405, 760), ("rear", rear_axle_x, 390, 748)],
            start=1,
        ):
            for facet_idx, angle_deg in enumerate([30, 48, 66, 84, 102, 120, 138], start=1):
                angle = math.radians(angle_deg)
                x_mid = axle_x + math.cos(angle) * radius - 34
                z_mid = wheel_z + math.sin(angle) * radius
                wedge_mesh(
                    "body",
                    f"{side_name}_{axle_name}_outer_arch_rounded_skin_facet_{facet_idx}",
                    x_mid - 36,
                    x_mid + 36,
                    min(734 * y_sign, 846 * y_sign),
                    max(734 * y_sign, 846 * y_sign),
                    max(z_base - 60, z_mid - 24),
                    max(z_base - 60, z_mid - 24),
                    z_mid + 28,
                    z_mid + 28,
                    COLORS["body_sand"],
                    "L4 gallery-shaped surface",
                    "body-color wheel-arch crown facet under the black flare, guided by side and wire renders",
                )

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
    box("chassis", "right_hand_drive_steering_box", 535, 515 * DRIVER_Y_SIGN, 610, 245, 175, 230, COLORS["metal"], "L2 service datum", "right-hand-drive steering box on right frame rail")
    box("chassis", "steering_box_right_frame_mount_plate", 500, 445 * DRIVER_Y_SIGN, 600, 295, 28, 260, COLORS["frame"], "L2 bracket reference", "steering box mounting plate on right rail")
    cyl("running_gear", "pitman_arm_right_hand_drive", 675, 555 * DRIVER_Y_SIGN, 565, "z", 62, 250, COLORS["metal"], "L2 service datum", "pitman arm below RHD steering box")
    cyl("running_gear", "front_drag_link_right_hand_drive", 875, 555 * DRIVER_Y_SIGN, 505, "x", 34, 620, COLORS["metal"], "L2 routing reference", "drag link from RHD steering box toward front axle")
    cyl("running_gear", "front_tie_rod", front_axle_x, 0, 505, "y", 32, 1420, COLORS["metal"], "L2 routing reference", "front axle tie rod across knuckles")
    cyl("running_gear", "steering_damper", 905, 350 * DRIVER_Y_SIGN, 480, "x", 58, 520, COLORS["metal"], "L2 service datum", "front steering damper package")
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

    for side, sign, y_sign in side_pairs:
        cyl(
            "brake_system",
            f"front_{side}_vented_disc_rotor",
            front_axle_x,
            738 * y_sign,
            wheel_z,
            "y",
            405,
            42,
            COLORS["metal"],
            "project-photo evidence",
            "front disc rotor visible in 2026-05-29 front brake photo set; exact diameter/thickness still needs measurement",
        )
        box(
            "brake_system",
            f"front_{side}_sumitomo_disc_caliper_body",
            front_axle_x + 92,
            760 * y_sign,
            wheel_z + 82,
            140,
            94,
            225,
            COLORS["metal"],
            "project-photo evidence",
            "large Sumitomo-style front caliper body from 20260529_183947_gp_lSYuESVg and related photos",
        )
        box(
            "brake_system",
            f"front_{side}_disc_caliper_bridge",
            front_axle_x + 46,
            787 * y_sign,
            wheel_z + 188,
            92,
            68,
            52,
            COLORS["metal"],
            "project-photo evidence",
            "caliper upper bridge/ear envelope from May 29 brake photos",
        )
        cyl(
            "brake_system",
            f"front_{side}_caliper_bleeder_screw",
            front_axle_x + 122,
            824 * y_sign,
            wheel_z + 222,
            "y",
            18,
            42,
            COLORS["brass"],
            "project-photo evidence",
            "visible bleeder/pipe fitting on front caliper; service datum only",
        )
        cyl(
            "brake_system",
            f"front_{side}_flex_hose_to_caliper",
            front_axle_x + 85,
            652 * y_sign,
            wheel_z + 185,
            "y",
            22,
            245,
            COLORS["rubber"],
            "project-photo evidence",
            "front flexible brake hose route to caliper from May 29 brake photos",
        )

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
            box(
                "running_gear",
                f"{axle_name}_{side_name}_mud_terrain_sidewall_lettering_panel",
                axle_x + 190,
                face_y + 54 * y_sign,
                wheel_z - 292,
                165,
                18,
                34,
                COLORS["body_shadow"],
                "project-photo evidence",
                "raised mud-terrain tire sidewall lettering from project photos; exact tire make/size still needs measurement",
            )

    # Brake and parking-brake routing, including the specific rear cable hardware now tracked separately.
    cyl("brake_system", "front_hard_line_right_frame_run", 1180, 338 * DRIVER_Y_SIGN, 575, "x", 18, 1650, COLORS["metal"], "L2 routing reference", "front brake hard-line run along right rail")
    cyl("brake_system", "rear_hard_line_right_frame_run", 2320, 338 * DRIVER_Y_SIGN, 575, "x", 18, 1500, COLORS["metal"], "L2 routing reference", "rear brake hard-line run along right rail")
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
    plate_text(
        "body",
        "rear_license_plate_bsn453",
        3522,
        0,
        695,
        "BSN453",
        COLORS["black_trim"],
        "project-photo evidence",
        "matching BSN 453 plate identity propagated from front baseline photos pending rear plate confirmation",
    )

    # Front sheet metal, grille, lamps, bonnet fixtures, and windshield details.
    for idx, y in enumerate([-300, -200, -100, 0, 100, 200, 300], start=1):
        box("front_detail", f"vertical_grille_slot_{idx}", 82, y, 842, 26, 42, 230, COLORS["rubber"], "L2 visible-detail primitive", "FJ40 vertical grille slot")
    for y in [-495, 495]:
        cyl("front_detail", f"headlamp_bezel_{'left' if y < 0 else 'right'}", 80, y, 985, "x", 270, 28, COLORS["metal"], "L2 visible-detail primitive", "round headlamp bezel")
        cyl("front_detail", f"side_marker_{'left' if y < 0 else 'right'}", 188, y * 1.38, 1005, "y", 82, 26, COLORS["electrical"], "L2 visible-detail primitive", "front fender side marker")
    box("front_detail", "front_license_plate", 5, 0, 650, 22, 360, 170, COLORS["reference"], "L2 visible-detail primitive", "front licence plate envelope")
    plate_text(
        "front_detail",
        "front_license_plate_bsn453",
        -10,
        0,
        650,
        "BSN453",
        COLORS["black_trim"],
        "project-photo evidence",
        "front Punjab plate BSN 453 visible in baseline walkaround photos; stroke text is visual reference, not legal plate typography",
    )
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
        rounded_side_window_mesh(f"{side}_rear_window_rubber_seal", 2190, 842 * y_sign, 1595, 676, 382, 30, 118, COLORS["rubber"], "L2 visible-detail primitive", "classic rounded hardtop rear side window rubber gasket")
        for idx, x in enumerate([1320, 1820, 2500, 3180], start=1):
            box("hard_top", f"{side}_hardtop_vertical_joint_{idx}", x, 826 * y_sign, 1320, 22, 28, 570, COLORS["rubber"], "L2 visible-detail primitive", "hardtop vertical joint/seal")
        box("body", f"{side}_side_step_board", 1540, 865 * y_sign, 620, 1120, 210, 55, COLORS["roof_white"], "L2 visible-detail primitive", "painted side step board from project photos")
        box("body", f"{side}_diesel_badge", 2925, 822 * y_sign, 980, 120, 24, 42, COLORS["metal"], "L2 visible-detail primitive", "DIESEL side badge datum from project photos")
    rounded_rear_window_mesh("rear_left_window_rubber_seal", 3470, -250, 1600, 400, 330, 30, 88, COLORS["rubber"], "L2 visible-detail primitive", "left split rear-door rounded window rubber gasket")
    rounded_rear_window_mesh("rear_right_window_rubber_seal", 3470, 250, 1600, 400, 330, 30, 88, COLORS["rubber"], "L2 visible-detail primitive", "right split rear-door rounded window rubber gasket")
    rounded_rear_window_mesh("rear_left_hardtop_window", 3485, -250, 1600, 340, 275, 20, 70, COLORS["glass"], "L2 visible-detail primitive", "left split rear-door classic rounded back window glass")
    rounded_rear_window_mesh("rear_right_hardtop_window", 3485, 250, 1600, 340, 275, 20, 70, COLORS["glass"], "L2 visible-detail primitive", "right split rear-door classic rounded back window glass")
    for y in [-555, -275, 275, 555]:
        box("hard_top", f"rear_corner_glass_or_seal_{int(y + 600)}", 3500, y, 1415, 28, 170, 300, COLORS["glass"], "L2 visible-detail primitive", "rear corner hardtop glass/seal datum")

    # Exterior fidelity pass guided by the 1979 hard-top reference: separated
    # paint, trim, glass, lamp, and seal objects rather than a single shell.
    for idx, z in enumerate([860, 895, 930, 965], start=1):
        box("front_detail", f"front_grille_black_mesh_horizontal_texture_{idx}", 64, 0, z, 18, 560, 12, COLORS["glass_dark"], "L3 exterior material reference", "separate grille mesh row from hard-top reference render")
    for idx, y in enumerate([-260, -170, -80, 80, 170, 260], start=1):
        box("front_detail", f"front_grille_black_mesh_vertical_texture_{idx}", 62, y, 852, 20, 12, 145, COLORS["glass_dark"], "L3 exterior material reference", "separate grille mesh column from hard-top reference render")
    for idx, y in enumerate([-325, -230, 230, 325], start=1):
        cyl("front_detail", f"grille_surround_screw_{idx}", 58, y, 812 if abs(y) > 300 else 1008, "x", 28, 20, COLORS["chrome"], "L3 exterior material reference", "front grille surround screw/head datum")

    def grille_badge_bar(name: str, y: float, z: float, width: float, height: float) -> None:
        box("front_detail", f"toyota_grille_letter_{name}", 52, y, z, 16, width, height, COLORS["grille_yellow"], "L3 exterior material reference", "raised yellow TOYOTA grille lettering reference")

    grille_badge_bar("t_top", -190, 940, 58, 12)
    grille_badge_bar("t_stem", -190, 895, 13, 54)
    for suffix, y_center in [("o1", -98), ("o2", 98)]:
        grille_badge_bar(f"{suffix}_top", y_center, 938, 52, 12)
        grille_badge_bar(f"{suffix}_bottom", y_center, 893, 52, 12)
        grille_badge_bar(f"{suffix}_left", y_center - 23, 900, 11, 42)
        grille_badge_bar(f"{suffix}_right", y_center + 23, 900, 11, 42)
    grille_badge_bar("y_left_upper", -21, 928, 18, 12)
    grille_badge_bar("y_right_upper", 21, 928, 18, 12)
    grille_badge_bar("y_stem", 0, 895, 12, 42)
    grille_badge_bar("a_left", 184, 895, 11, 55)
    grille_badge_bar("a_right", 228, 895, 11, 55)
    grille_badge_bar("a_top", 206, 938, 52, 12)
    grille_badge_bar("a_bar", 206, 915, 42, 10)

    for side, sign, y_sign in side_pairs:
        side_name = "left" if y_sign < 0 else "right"
        # Front fender top indicators and lamps are separate amber/chrome objects on the reference render.
        box("front_detail", f"{side_name}_front_fender_turn_signal_base", 290, 642 * y_sign, 1058, 155, 80, 24, COLORS["chrome"], "L3 exterior material reference", "front fender turn signal chrome base")
        cyl("front_detail", f"{side_name}_front_fender_turn_signal_lens", 298, 642 * y_sign, 1075, "z", 78, 32, COLORS["amber"], "L3 exterior material reference", "front fender amber turn-signal lens")
        cyl("front_detail", f"{side_name}_headlamp_glass_highlight", 64, 445 * y_sign, 1035, "x", 126, 18, COLORS["body_highlight"], "L3 exterior material reference", "headlamp glass highlight disk")
        cyl("front_detail", f"{side_name}_headlamp_mount_screw_upper", 58, 445 * y_sign - 70 * y_sign, 1094, "x", 22, 18, COLORS["chrome"], "L3 exterior material reference", "headlamp bezel screw datum")
        cyl("front_detail", f"{side_name}_headlamp_mount_screw_lower", 58, 445 * y_sign + 70 * y_sign, 876, "x", 22, 18, COLORS["chrome"], "L3 exterior material reference", "headlamp bezel screw datum")

        # Side vents, badges, trim strips, door outlines, and weather seals.
        for vent_idx, z in enumerate([890, 925, 960, 995, 1030], start=1):
            box("body", f"{side_name}_front_quarter_louver_slot_{vent_idx}", 885, 826 * y_sign, z, 175, 24, 14, COLORS["glass_dark"], "L3 exterior material reference", "stacked side louver slot behind front fender")
            box("body", f"{side_name}_front_quarter_louver_highlight_{vent_idx}", 880, 812 * y_sign, z + 16, 160, 16, 8, COLORS["body_highlight"], "L3 exterior material reference", "raised louver upper edge")
        box("body", f"{side_name}_beltline_trim_front_door", 1140, 834 * y_sign, 1118, 780, 22, 28, COLORS["chrome"], "L3 exterior material reference", "thin beltline trim along front door")
        box("body", f"{side_name}_beltline_trim_rear_tub", 1965, 834 * y_sign, 1118, 1390, 22, 28, COLORS["chrome"], "L3 exterior material reference", "thin beltline trim along rear quarter")
        box("body", f"{side_name}_door_outer_skin_upper_pressing", 1235, 789 * y_sign, 1040, 725, 34, 70, COLORS["body_shadow"], "L3 exterior material reference", "recessed upper door skin panel shadow")
        box("body", f"{side_name}_door_skin_lower_recess_shadow", 1235, 789 * y_sign, 885, 725, 32, 76, COLORS["body_shadow"], "L3 exterior material reference", "recessed lower door skin panel shadow")
        box("body", f"{side_name}_door_window_front_vertical_frame", 1115, 812 * y_sign, 1192, 34, 35, 385, COLORS["black_trim"], "L3 exterior material reference", "front door window vertical frame")
        box("body", f"{side_name}_door_window_rear_vertical_frame", 1642, 812 * y_sign, 1192, 34, 35, 385, COLORS["black_trim"], "L3 exterior material reference", "front door window rear frame")
        box("body", f"{side_name}_door_window_top_frame", 1115, 812 * y_sign, 1546, 560, 35, 34, COLORS["black_trim"], "L3 exterior material reference", "front door window top frame")
        box("body", f"{side_name}_door_window_bottom_frame", 1115, 812 * y_sign, 1186, 560, 35, 30, COLORS["black_trim"], "L3 exterior material reference", "front door window bottom frame")
        cyl("body", f"{side_name}_door_lock_cylinder", 1645, 835 * y_sign, 1032, "y", 36, 22, COLORS["chrome"], "L3 exterior material reference", "round door lock cylinder")
        for hinge_idx, z in enumerate([820, 930, 1180, 1290], start=1):
            cyl("body", f"{side_name}_door_hinge_pin_cap_{hinge_idx}", 1126, 843 * y_sign, z, "y", 32, 26, COLORS["chrome"], "L3 exterior material reference", "visible exterior hinge screw/cap")

        # Hard-top glass has separate rubber seals, sliding window split lines, and rounded corner caps.
        for window_name, x_center, window_length in [("front", 1420, 500), ("rear", 2190, 610)]:
            box("hard_top", f"{side_name}_hardtop_{window_name}_window_upper_inner_shadow", x_center, 854 * y_sign, 1732, window_length, 18, 22, COLORS["glass_dark"], "L3 exterior material reference", "dark hardtop window upper interior shadow")
            box("hard_top", f"{side_name}_hardtop_{window_name}_window_lower_inner_shadow", x_center, 854 * y_sign, 1360, window_length, 18, 22, COLORS["glass_dark"], "L3 exterior material reference", "dark hardtop window lower interior shadow")
            box("hard_top", f"{side_name}_hardtop_{window_name}_window_sliding_mullion", x_center + window_length * 0.18, 858 * y_sign, 1438, 28, 24, 300, COLORS["black_trim"], "L3 exterior material reference", "sliding hardtop side-window mullion")
            for corner_idx, (dx, dz) in enumerate([(-window_length / 2, 0), (window_length / 2, 0), (-window_length / 2, 320), (window_length / 2, 320)], start=1):
                cyl("hard_top", f"{side_name}_hardtop_{window_name}_window_rounded_corner_{corner_idx}", x_center + dx, 862 * y_sign, 1360 + dz, "y", 54, 24, COLORS["rubber"], "L3 exterior material reference", "rounded rubber window corner approximation")
        rounded_side_window_mesh(f"{side_name}_classic_rear_quarter_window_dark_inner_inset", 2190, 866 * y_sign, 1595, 548, 260, 16, 74, COLORS["glass_dark"], "L4 online-reference detail", "dark inset inside the classic rounded rear hardtop side glass")
        box("hard_top", f"{side_name}_classic_rear_quarter_window_upper_glare_arc", 2190, 876 * y_sign, 1695, 440, 16, 18, COLORS["body_highlight"], "L4 online-reference detail", "thin pale reflection band following rounded rear quarter glass")
        box("hard_top", f"{side_name}_classic_rear_quarter_window_lower_shadow_arc", 2190, 878 * y_sign, 1488, 470, 16, 16, COLORS["glass_dark"], "L4 online-reference detail", "lower dark reflection band in rounded rear quarter glass")
        box("hard_top", f"{side_name}_roof_drip_rail_outer_shadow", 1235, 862 * y_sign, 1784, 2275, 28, 30, COLORS["body_shadow"], "L3 exterior material reference", "drip rail shadow under white roof gutter")
        for rib_idx, x in enumerate([1420, 1840, 2260, 2680, 3100], start=1):
            box("hard_top", f"{side_name}_roof_side_panel_subtle_vertical_pressing_{rib_idx}", x, 804 * y_sign, 1325, 20, 18, 520, COLORS["body_shadow"], "L3 exterior material reference", "subtle hardtop side panel vertical pressing")

        # Black fender flares are approximated with short separated arc facets.
        for axle_name, axle_x, arch_radius in [("front", front_axle_x, 378), ("rear", rear_axle_x, 365)]:
            for arc_idx, angle_deg in enumerate([24, 38, 52, 66, 80, 94, 108, 122, 136, 150], start=1):
                angle = math.radians(angle_deg)
                x = axle_x + math.cos(angle) * arch_radius - 34
                z = wheel_z + math.sin(angle) * arch_radius
                box("body", f"{side_name}_{axle_name}_black_fender_flare_arc_{arc_idx}", x, 823 * y_sign, z, 68, 46, 34, COLORS["black_trim"], "L3 exterior material reference", "faceted black wheel-arch flare from hard-top reference")

        # Step boards and mud flaps have separate tread/slat and bracket details.
        for tread_idx, x in enumerate([1120, 1320, 1520, 1720, 1920], start=1):
            box("body", f"{side_name}_side_step_tread_strip_{tread_idx}", x, 872 * y_sign, 674, 130, 162, 12, COLORS["chrome"], "L3 exterior material reference", "ribbed step-board tread strip")
        for bracket_idx, x in enumerate([1180, 1540, 1900], start=1):
            box("body", f"{side_name}_side_step_drop_bracket_{bracket_idx}", x, 760 * y_sign, 530, 52, 38, 155, COLORS["frame"], "L3 exterior material reference", "side-step drop bracket")
        box("body", f"{side_name}_front_mud_flap", front_axle_x - 315, 780 * y_sign, 190, 42, 135, 280, COLORS["rubber"], "L3 exterior material reference", "front rubber mud flap")
        box("body", f"{side_name}_rear_mud_flap", rear_axle_x + 330, 780 * y_sign, 185, 42, 135, 300, COLORS["rubber"], "L3 exterior material reference", "rear rubber mud flap")

    # Rear hard-top and spare-carrier details visible in the back-view render.
    box("hard_top", "rear_split_door_center_seal", 3505, 0, 1180, 30, 36, 650, COLORS["rubber"], "L3 exterior material reference", "rear barn-door center seal")
    rounded_rear_window_mesh("rear_door_left_glass_dark_inset", 3502, -250, 1600, 285, 225, 22, 58, COLORS["glass_dark"], "L3 exterior material reference", "dark inset inside left rounded rear door glass")
    rounded_rear_window_mesh("rear_door_right_glass_dark_inset", 3502, 250, 1600, 285, 225, 22, 58, COLORS["glass_dark"], "L3 exterior material reference", "dark inset inside right rounded rear door glass")
    box("hard_top", "rear_door_window_center_mullion", 3496, 0, 1462, 34, 34, 304, COLORS["black_trim"], "L3 exterior material reference", "rear window center mullion")
    for side_name, y_sign in [("left", -1), ("right", 1)]:
        for hinge_idx, z in enumerate([1180, 1510], start=1):
            cyl("hard_top", f"rear_{side_name}_door_hinge_barrel_{hinge_idx}", 3520, 650 * y_sign, z, "z", 42, 165, COLORS["chrome"], "L3 exterior material reference", "rear door hinge barrel")
        box("hard_top", f"rear_{side_name}_door_pull_handle", 3526, 110 * y_sign, 1205, 28, 120, 44, COLORS["chrome"], "L3 exterior material reference", "rear door pull handle")
        cyl("hard_top", f"rear_{side_name}_door_lock_button", 3536, 190 * y_sign, 1190, "x", 38, 22, COLORS["chrome"], "L3 exterior material reference", "rear door lock button")
    cyl("body", "rear_spare_sidewall_highlight_ring", 3628, 0, 1020, "x", 585, 18, COLORS["body_shadow"], "L3 exterior material reference", "rear spare sidewall highlight ring")
    for spoke_idx, angle_deg in enumerate([0, 60, 120, 180, 240, 300], start=1):
        y = math.cos(math.radians(angle_deg)) * 142
        z = 1020 + math.sin(math.radians(angle_deg)) * 142
        box("body", f"rear_spare_wheel_spoke_{spoke_idx}", 3650, y, z - 12, 28, 205, 24, COLORS["chrome"], "L3 exterior material reference", "rear spare wheel spoke")

    # Second reference-detail pass: more of the separated exterior hardware and
    # material breaks visible on the 1979 hard-top reference model.
    box("body", "windshield_center_divider_bar", 1116, 0, 1570, 30, 42, 420, COLORS["black_trim"], "L3 exterior material reference", "split windshield center divider bar")
    box("body", "windshield_upper_inner_glare_band", 1112, 0, 1588, 20, 1210, 28, COLORS["glass_dark"], "L3 exterior material reference", "dark upper reflection band across windshield glass")
    box("body", "windshield_lower_inner_glare_band", 1112, 0, 1420, 20, 1185, 24, COLORS["glass_dark"], "L3 exterior material reference", "dark lower reflection band across windshield glass")
    box("body", "hood_front_lip_shadow", 42, 0, 1222, 36, 1320, 34, COLORS["body_shadow"], "L3 exterior material reference", "front hood lip shadow above grille")
    box("body", "hood_rear_cowl_gap_shadow", 1012, 0, 1287, 28, 1310, 28, COLORS["rubber"], "L3 exterior material reference", "hood-to-cowl panel gap")
    box("body", "front_apron_lower_shadow", 92, 0, 710, 28, 1280, 42, COLORS["body_shadow"], "L3 exterior material reference", "lower front apron crease below grille")
    box("front_detail", "front_license_plate_upper_screw_left", -8, -155, 730, 18, 24, 24, COLORS["chrome"], "L3 exterior material reference", "front license plate screw head")
    box("front_detail", "front_license_plate_upper_screw_right", -8, 155, 730, 18, 24, 24, COLORS["chrome"], "L3 exterior material reference", "front license plate screw head")
    box("front_detail", "front_license_plate_lower_screw_left", -8, -155, 585, 18, 24, 24, COLORS["chrome"], "L3 exterior material reference", "front license plate screw head")
    box("front_detail", "front_license_plate_lower_screw_right", -8, 155, 585, 18, 24, 24, COLORS["chrome"], "L3 exterior material reference", "front license plate screw head")
    for bolt_idx, y in enumerate([-680, -485, 485, 680], start=1):
        cyl("front_detail", f"front_bumper_face_bolt_{bolt_idx}", 4, y, 558, "x", 34, 20, COLORS["chrome"], "L3 exterior material reference", "front bumper face bolt")
    for bolt_idx, y in enumerate([-660, -360, 360, 660], start=1):
        cyl("body", f"rear_bumper_face_bolt_{bolt_idx}", 3742, y, 558, "x", 34, 20, COLORS["chrome"], "L3 exterior material reference", "rear bumper face bolt")

    for side, sign, y_sign in side_pairs:
        side_name = "left" if y_sign < 0 else "right"
        # Windshield, cowl, and hood perimeter hardware.
        cyl("body", f"{side_name}_windshield_wiper_pivot", 1100, 358 * y_sign, 1372, "x", 42, 26, COLORS["chrome"], "L3 exterior material reference", "round wiper pivot cap")
        box("body", f"{side_name}_windshield_wiper_blade_rubber", 1092, 165 * y_sign, 1508, 24, 480, 16, COLORS["rubber"], "L3 exterior material reference", "separate black windshield wiper blade")
        box("body", f"{side_name}_windshield_wiper_arm_chrome", 1094, 252 * y_sign, 1456, 18, 340, 14, COLORS["chrome"], "L3 exterior material reference", "thin chrome windshield wiper arm")
        cyl("body", f"{side_name}_cowl_vent_screw_front", 1044, 278 * y_sign, 1360, "z", 20, 12, COLORS["chrome"], "L3 exterior material reference", "cowl vent screw head")
        cyl("body", f"{side_name}_cowl_vent_screw_rear", 1018, 422 * y_sign, 1360, "z", 20, 12, COLORS["chrome"], "L3 exterior material reference", "cowl vent screw head")
        box("body", f"{side_name}_hood_side_gap_shadow", 420, 684 * y_sign, 1235, 760, 24, 24, COLORS["body_shadow"], "L3 exterior material reference", "hood side panel gap above fender")
        cyl("body", f"{side_name}_hood_latch_round_pin", 820, 645 * y_sign, 1238, "y", 28, 22, COLORS["chrome"], "L3 exterior material reference", "round hood latch pin cap")

        # Fender, lamp, mirror, and side-panel fasteners.
        cyl("front_detail", f"{side_name}_front_fender_turn_signal_screw_front", 238, 642 * y_sign, 1078, "z", 18, 12, COLORS["chrome"], "L3 exterior material reference", "fender turn-signal screw head")
        cyl("front_detail", f"{side_name}_front_fender_turn_signal_screw_rear", 350, 642 * y_sign, 1078, "z", 18, 12, COLORS["chrome"], "L3 exterior material reference", "fender turn-signal screw head")
        cyl("front_detail", f"{side_name}_side_marker_chrome_bezel", 190, 682 * y_sign, 1005, "y", 112, 18, COLORS["chrome"], "L3 exterior material reference", "side marker chrome bezel ring")
        cyl("front_detail", f"{side_name}_fog_lamp_inner_glass", 16, 360 * y_sign, 620, "x", 118, 18, COLORS["body_highlight"], "L3 exterior material reference", "fog lamp inner glass highlight")
        box("front_detail", f"{side_name}_fog_lamp_drop_bracket", 42, 360 * y_sign, 548, 38, 34, 85, COLORS["frame"], "L3 exterior material reference", "fog lamp mounting bracket")
        for screw_idx, (x, z) in enumerate([(1328, 1248), (1328, 1142), (1484, 1248), (1484, 1142)], start=1):
            cyl("body", f"{side_name}_mirror_mount_screw_{screw_idx}", x, 842 * y_sign, z, "y", 20, 16, COLORS["chrome"], "L3 exterior material reference", "door mirror base screw head")
        box("body", f"{side_name}_door_handle_shadow_gap", 1575, 834 * y_sign, 1016, 175, 18, 18, COLORS["body_shadow"], "L3 exterior material reference", "door handle recess shadow")
        box("body", f"{side_name}_door_handle_chrome_face", 1575, 858 * y_sign, 1055, 140, 18, 22, COLORS["chrome"], "L3 exterior material reference", "separate chrome face on door handle")
        box("body", f"{side_name}_front_door_lower_weather_strip", 1228, 836 * y_sign, 742, 760, 20, 22, COLORS["rubber"], "L3 exterior material reference", "door lower rubber weather strip")
        box("body", f"{side_name}_rear_quarter_vertical_rear_seam", 2828, 832 * y_sign, 980, 24, 20, 560, COLORS["rubber"], "L3 exterior material reference", "rear quarter vertical panel seam")
        cyl("body", f"{side_name}_fuel_filler_outer_ring", 2935, 842 * y_sign, 1065, "y", 145, 18, COLORS["chrome"], "L3 exterior material reference", "round fuel/body plug outer trim ring")

        # Hardtop gutter fasteners and sliding-window screws.
        for rivet_idx, x in enumerate([1240, 1485, 1730, 1975, 2220, 2465, 2710, 2955, 3200], start=1):
            cyl("hard_top", f"{side_name}_roof_gutter_rivet_{rivet_idx}", x, 864 * y_sign, 1828, "y", 18, 16, COLORS["chrome"], "L3 exterior material reference", "roof gutter rivet/fastener")
        for x_center, window_name, window_length in [(1420, "front", 500), (2190, "rear", 610)]:
            for screw_idx, dx in enumerate([-window_length / 2 + 70, window_length / 2 - 70], start=1):
                cyl("hard_top", f"{side_name}_hardtop_{window_name}_window_upper_screw_{screw_idx}", x_center + dx, 870 * y_sign, 1724, "y", 18, 16, COLORS["chrome"], "L3 exterior material reference", "hardtop sliding-window frame screw")
                cyl("hard_top", f"{side_name}_hardtop_{window_name}_window_lower_screw_{screw_idx}", x_center + dx, 870 * y_sign, 1368, "y", 18, 16, COLORS["chrome"], "L3 exterior material reference", "hardtop sliding-window frame screw")
            box("hard_top", f"{side_name}_hardtop_{window_name}_window_center_track", x_center, 868 * y_sign, 1435, window_length - 70, 14, 18, COLORS["chrome"], "L3 exterior material reference", "bright sliding-window track")
        box("hard_top", f"{side_name}_roof_gutter_front_end_cap", 1128, 862 * y_sign, 1812, 52, 34, 42, COLORS["chrome"], "L3 exterior material reference", "front roof gutter end cap")
        box("hard_top", f"{side_name}_roof_gutter_rear_end_cap", 3358, 862 * y_sign, 1812, 52, 34, 42, COLORS["chrome"], "L3 exterior material reference", "rear roof gutter end cap")

        # Wheels: separated rim slots and tire sidewall ticks keep the silhouette from reading as a plain cylinder.
        for axle_x, axle_name in [(front_axle_x, "front"), (rear_axle_x, "rear")]:
            face_y = 860 * y_sign
            for slot_idx, angle_deg in enumerate([30, 90, 150, 210, 270, 330], start=1):
                angle = math.radians(angle_deg)
                slot_x = axle_x + math.cos(angle) * 165
                slot_z = wheel_z + math.sin(angle) * 165
                box("running_gear", f"{axle_name}_{side_name}_rim_vent_slot_{slot_idx}", slot_x, face_y, slot_z, 54, 20, 34, COLORS["glass_dark"], "L3 exterior material reference", "dark wheel rim vent slot")
            for tick_idx, angle_deg in enumerate(range(15, 360, 30), start=1):
                angle = math.radians(angle_deg)
                tick_x = axle_x + math.cos(angle) * 336
                tick_z = wheel_z + math.sin(angle) * 336
                box("running_gear", f"{axle_name}_{side_name}_tire_sidewall_tick_{tick_idx}", tick_x, face_y + 5 * y_sign, tick_z, 38, 18, 18, COLORS["body_shadow"], "L3 exterior material reference", "raised tire sidewall tick detail")
            cyl("running_gear", f"{axle_name}_{side_name}_hub_cap_center_button", axle_x, face_y + 48 * y_sign, wheel_z, "y", 74, 24, COLORS["chrome"], "L3 exterior material reference", "bright hub-cap center button")

    # Rear door, lighting, license plate, and spare carrier hardware.
    box("hard_top", "rear_left_window_upper_inner_shadow", 3492, -250, 1688, 20, 260, 22, COLORS["glass_dark"], "L3 exterior material reference", "dark upper reflection band in left rounded rear glass")
    box("hard_top", "rear_right_window_upper_inner_shadow", 3492, 250, 1688, 20, 260, 22, COLORS["glass_dark"], "L3 exterior material reference", "dark upper reflection band in right rounded rear glass")
    box("hard_top", "rear_left_window_lower_inner_shadow", 3492, -250, 1496, 20, 275, 20, COLORS["glass_dark"], "L3 exterior material reference", "dark lower reflection band in left rounded rear glass")
    box("hard_top", "rear_right_window_lower_inner_shadow", 3492, 250, 1496, 20, 275, 20, COLORS["glass_dark"], "L3 exterior material reference", "dark lower reflection band in right rounded rear glass")
    box("hard_top", "rear_left_window_pale_glare_strip", 3508, -250, 1698, 16, 230, 14, COLORS["body_highlight"], "L4 online-reference detail", "pale reflection strip on left classic rounded back window")
    box("hard_top", "rear_right_window_pale_glare_strip", 3508, 250, 1698, 16, 230, 14, COLORS["body_highlight"], "L4 online-reference detail", "pale reflection strip on right classic rounded back window")
    for hinge_idx, y in enumerate([-620, -520, 520, 620], start=1):
        box("hard_top", f"rear_door_hinge_mount_plate_{hinge_idx}", 3528, y, 1510 if abs(y) > 570 else 1180, 24, 84, 96, COLORS["chrome"], "L3 exterior material reference", "rear door hinge mounting plate")
    for screw_idx, (y, z) in enumerate([(-590, 1555), (-590, 1470), (590, 1555), (590, 1470), (-590, 1225), (-590, 1138), (590, 1225), (590, 1138)], start=1):
        cyl("hard_top", f"rear_door_hinge_plate_screw_{screw_idx}", 3544, y, z, "x", 18, 16, COLORS["chrome"], "L3 exterior material reference", "rear hinge plate screw")
    box("body", "rear_spare_carrier_latch_plate", 3530, 315, 1042, 36, 132, 92, COLORS["metal"], "L3 exterior material reference", "spare carrier latch plate")
    cyl("body", "rear_spare_carrier_latch_pin", 3552, 315, 1042, "x", 28, 36, COLORS["chrome"], "L3 exterior material reference", "spare carrier latch pin")
    box("body", "rear_spare_carrier_lower_hinge_plate", 3528, -320, 760, 36, 126, 88, COLORS["metal"], "L3 exterior material reference", "spare carrier lower hinge plate")
    box("body", "rear_spare_carrier_upper_hinge_plate", 3528, -320, 1088, 36, 126, 88, COLORS["metal"], "L3 exterior material reference", "spare carrier upper hinge plate")
    for screw_idx, (y, z) in enumerate([(-320, 724), (-320, 796), (-320, 1052), (-320, 1124), (315, 1006), (315, 1078)], start=1):
        cyl("body", f"rear_spare_carrier_hardware_screw_{screw_idx}", 3550, y, z, "x", 18, 16, COLORS["chrome"], "L3 exterior material reference", "spare carrier hardware screw")
    box("body", "rear_license_plate_upper_lamp_left", 3508, -145, 810, 28, 90, 34, COLORS["chrome"], "L3 exterior material reference", "rear license plate lamp")
    box("body", "rear_license_plate_upper_lamp_right", 3508, 145, 810, 28, 90, 34, COLORS["chrome"], "L3 exterior material reference", "rear license plate lamp")
    for screw_idx, (y, z) in enumerate([(-160, 770), (160, 770), (-160, 630), (160, 630)], start=1):
        cyl("body", f"rear_license_plate_screw_{screw_idx}", 3534, y, z, "x", 18, 16, COLORS["chrome"], "L3 exterior material reference", "rear license plate screw")
    for side_name, y_sign in [("left", -1), ("right", 1)]:
        cyl("body", f"rear_{side_name}_tail_lamp_chrome_bezel", 3488, 675 * y_sign, 930, "x", 122, 18, COLORS["chrome"], "L3 exterior material reference", "rear tail lamp chrome bezel")
        cyl("body", f"rear_{side_name}_tail_lamp_inner_lens", 3502, 675 * y_sign, 930, "x", 72, 18, COLORS["electrical"], "L3 exterior material reference", "rear tail lamp inner lens")

    # Rev C online-representation detail pass: adds cues that are visible in
    # commercial model part breakdowns and Toyota online parts representations.
    box("hard_top", "roof_ventilator_lid_panel", 1885, 0, 1882, 520, 520, 30, COLORS["roof_white"], "L4 online-reference detail", "roof ventilator lid from Toyota roof/rear ventilator parts representation")
    box("hard_top", "roof_ventilator_front_hinge_bar", 1625, 0, 1898, 36, 540, 34, COLORS["chrome"], "L4 online-reference detail", "roof ventilator front hinge bar")
    box("hard_top", "roof_ventilator_rear_pull_handle", 2140, 0, 1905, 46, 210, 34, COLORS["chrome"], "L4 online-reference detail", "roof ventilator pull handle")
    box("hard_top", "roof_ventilator_shadow_gap", 1885, 0, 1858, 560, 560, 24, COLORS["body_shadow"], "L4 online-reference detail", "shadow line around raised roof ventilator lid")
    for screw_idx, (x, y) in enumerate([(1642, -220), (1642, 220), (2115, -185), (2115, 185)], start=1):
        cyl("hard_top", f"roof_ventilator_screw_{screw_idx}", x, y, 1918, "z", 18, 14, COLORS["chrome"], "L4 online-reference detail", "roof ventilator screw head")

    for side, sign, y_sign in side_pairs:
        side_name = "left" if y_sign < 0 else "right"
        box("hard_top", f"{side_name}_rear_quarter_ventilator_frame", 3065, 846 * y_sign, 1548, 270, 24, 255, COLORS["black_trim"], "L4 online-reference detail", "rear hardtop side ventilator frame from Toyota rear ventilator parts group")
        for vent_idx, z in enumerate([1488, 1534, 1580, 1626], start=1):
            box("hard_top", f"{side_name}_rear_quarter_ventilator_louver_{vent_idx}", 3065, 872 * y_sign, z, 225, 18, 18, COLORS["glass_dark"], "L4 online-reference detail", "stacked rear ventilator louver slat")
        box("hard_top", f"{side_name}_hardtop_to_tub_join_shadow", 2200, 822 * y_sign, 1262, 2190, 24, 34, COLORS["rubber"], "L4 online-reference detail", "hardtop-to-body joint line visible across commercial model breakdown")
        box("body", f"{side_name}_front_clip_to_tub_join_line", 1018, 823 * y_sign, 958, 22, 22, 510, COLORS["rubber"], "L4 online-reference detail", "front clip/body tub seam from printable body part breakdown")
        box("body", f"{side_name}_rear_tub_top_flange", 2325, 805 * y_sign, 1235, 1360, 42, 36, COLORS["body_highlight"], "L4 online-reference detail", "rear tub top flange below removable hardtop")

    for mount_idx, (x, y) in enumerate([(710, -525), (710, 525), (1310, -560), (1310, 560), (2230, -575), (2230, 575), (3060, -545), (3060, 545)], start=1):
        cyl("chassis", f"cab_body_mount_rubber_puck_{mount_idx}", x, y, 560, "z", 112, 42, COLORS["rubber"], "L4 service-reference detail", "cab/body mounting rubber puck from Toyota body-mounting parts group")
        box("chassis", f"cab_body_mount_stand_{mount_idx}", x, y, 500, 135, 120, 52, COLORS["frame"], "L4 service-reference detail", "body mount bracket stand")

    for side, sign, y_sign in side_pairs:
        side_name = "left" if y_sign < 0 else "right"
        box("chassis", f"{side_name}_front_bumper_stay_outer_plate", 190, 585 * y_sign, 505, 310, 44, 88, COLORS["frame"], "L4 service-reference detail", "front bumper stay plate from Toyota bumper-stay parts group")
        box("chassis", f"{side_name}_front_bumper_stay_inner_plate", 188, 430 * y_sign, 487, 285, 38, 72, COLORS["frame"], "L4 service-reference detail", "inner front bumper stay plate")
        box("chassis", f"{side_name}_rear_bumper_stay_outer_plate", 3475, 585 * y_sign, 505, 320, 44, 88, COLORS["frame"], "L4 service-reference detail", "rear bumper stay plate from Toyota bumper-stay parts group")
        box("chassis", f"{side_name}_rear_bumper_stay_inner_plate", 3482, 430 * y_sign, 488, 290, 38, 72, COLORS["frame"], "L4 service-reference detail", "inner rear bumper stay plate")
        for bolt_idx, x in enumerate([105, 250], start=1):
            cyl("chassis", f"{side_name}_front_bumper_stay_bolt_{bolt_idx}", x, 620 * y_sign, 550, "y", 28, 22, COLORS["chrome"], "L4 service-reference detail", "front bumper stay bolt head")
        for bolt_idx, x in enumerate([3415, 3570], start=1):
            cyl("chassis", f"{side_name}_rear_bumper_stay_bolt_{bolt_idx}", x, 620 * y_sign, 550, "y", 28, 22, COLORS["chrome"], "L4 service-reference detail", "rear bumper stay bolt head")

    box("body", "hood_underside_front_crossbrace", 285, 0, 1194, 760, 52, 34, COLORS["body_shadow"], "L4 online-reference detail", "hood underside bracing from open-hood printable model representation")
    box("body", "hood_underside_rear_crossbrace", 930, 0, 1260, 520, 48, 32, COLORS["body_shadow"], "L4 online-reference detail", "rear hood underside crossbrace")
    for side_name, y_sign in [("left", -1), ("right", 1)]:
        box("body", f"{side_name}_hood_underside_diagonal_brace", 575, 330 * y_sign, 1224, 650, 36, 30, COLORS["body_shadow"], "L4 online-reference detail", "diagonal hood underside brace approximation")
        box("body", f"{side_name}_hood_hinge_mount_plate", 1015, 540 * y_sign, 1278, 116, 76, 24, COLORS["chrome"], "L4 service-reference detail", "hood hinge mount plate from Toyota hood lock/hinge representation")
        cyl("body", f"{side_name}_hood_hinge_mount_screw_front", 986, 540 * y_sign, 1298, "z", 18, 12, COLORS["chrome"], "L4 service-reference detail", "hood hinge mount screw")
        cyl("body", f"{side_name}_hood_hinge_mount_screw_rear", 1044, 540 * y_sign, 1298, "z", 18, 12, COLORS["chrome"], "L4 service-reference detail", "hood hinge mount screw")
    cyl("body", "hood_prop_rod_stowed", 650, -585, 1170, "x", 18, 690, COLORS["chrome"], "L4 online-reference detail", "stowed hood prop rod from open-hood reference")
    box("body", "hood_prop_rod_retaining_clip", 972, -585, 1182, 42, 34, 28, COLORS["chrome"], "L4 online-reference detail", "hood prop retaining clip")
    box("body", "hood_lock_receiver_plate", 118, 0, 1166, 58, 250, 46, COLORS["chrome"], "L4 service-reference detail", "hood lock receiver at grille header")

    box("brake_system", "proportioning_bypass_valve_body", 1505, 338 * DRIVER_Y_SIGN, 608, 135, 82, 58, COLORS["brass"], "L4 service-reference detail", "Toyota GR Heritage proportioning/bypass valve cue on RHD brake-line side")
    cyl("brake_system", "proportioning_valve_front_tube", 1398, 338 * DRIVER_Y_SIGN, 610, "x", 14, 210, COLORS["brass"], "L4 service-reference detail", "front brake tube to proportioning valve")
    cyl("brake_system", "proportioning_valve_rear_tube", 1610, 338 * DRIVER_Y_SIGN, 610, "x", 14, 220, COLORS["brass"], "L4 service-reference detail", "rear brake tube from proportioning valve")
    for clip_idx, x in enumerate([1835, 2140, 2445, 2750], start=1):
        box("brake_system", f"rear_brake_tube_frame_clip_{clip_idx}", x, 338 * DRIVER_Y_SIGN, 590, 36, 32, 30, COLORS["chrome"], "L4 service-reference detail", "rear brake tube frame clip from Toyota tube parts cues")
    cyl("fuel_system", "fuel_tank_sub_inlet_hose", 3020, -612, 745, "z", 46, 320, COLORS["rubber"], "L4 service-reference detail", "fuel tank sub-inlet hose from Toyota GR Heritage parts list")
    for clamp_idx, z in enumerate([622, 850], start=1):
        cyl("fuel_system", f"fuel_tank_sub_inlet_hose_clamp_{clamp_idx}", 3020, -612, z, "z", 58, 14, COLORS["chrome"], "L4 service-reference detail", "fuel hose clamp")
    cyl("fuel_system", "fuel_tank_vent_hose", 2870, -515, 720, "x", 26, 470, COLORS["rubber"], "L4 service-reference detail", "fuel tank vent hose datum")

    for side_name, y_sign in [("left", -1), ("right", 1)]:
        for segment_name, z, color in [("amber_upper", 982, COLORS["amber"]), ("red_center", 930, COLORS["electrical"]), ("clear_lower", 878, COLORS["reference"])]:
            box("body", f"rear_{side_name}_tail_lamp_{segment_name}_lens", 3512, 675 * y_sign, z, 24, 88, 42, color, "L4 service-reference detail", "rear combination lamp separated amber/red/clear lens cue from Toyota GR Heritage list")
        for screw_idx, z in enumerate([1016, 842], start=1):
            cyl("body", f"rear_{side_name}_tail_lamp_body_screw_{screw_idx}", 3530, 724 * y_sign, z, "x", 16, 14, COLORS["chrome"], "L4 service-reference detail", "rear lamp body screw")

    gauge_positions = [
        ("speedometer", DRIVER_Y, 128),
        ("fuel", DRIVER_Y + 108 * DRIVER_Y_SIGN, 72),
        ("temperature", DRIVER_Y - 108 * DRIVER_Y_SIGN, 72),
        ("oil_pressure", DRIVER_Y - 200 * DRIVER_Y_SIGN, 58),
        ("ammeter", DRIVER_Y + 200 * DRIVER_Y_SIGN, 58),
    ]
    for gauge_name, y, diameter in gauge_positions:
        cyl("interior", f"dash_{gauge_name}_chrome_bezel", 1190, y, 1148, "x", diameter, 18, COLORS["chrome"], "L4 online-reference detail", "separate dash gauge bezel from high-density online interior representation")
        cyl("interior", f"dash_{gauge_name}_dark_face", 1180, y, 1148, "x", diameter - 20, 12, COLORS["glass_dark"], "L4 online-reference detail", "dark gauge face")
    box("interior", "dash_passenger_grab_handle_left_mount", 1190, PASSENGER_Y - 172 * DRIVER_Y_SIGN, 1170, 38, 36, 74, COLORS["chrome"], "L4 online-reference detail", "passenger dash grab handle mount")
    box("interior", "dash_passenger_grab_handle_right_mount", 1190, PASSENGER_Y + 175 * DRIVER_Y_SIGN, 1170, 38, 36, 74, COLORS["chrome"], "L4 online-reference detail", "passenger dash grab handle mount")
    cyl("interior", "dash_passenger_grab_handle_bar", 1184, PASSENGER_Y, 1198, "y", 32, 330, COLORS["chrome"], "L4 online-reference detail", "passenger dash grab handle")

    # Interior: controls, seat structure, belts, floor mats, and dash detail.
    box("interior", "dashboard_glovebox_door", 1212, PASSENGER_Y, 1115, 35, 335, 150, COLORS["reference"], "L2 visible-detail primitive", f"glovebox door on passenger/{'left' if DRIVER_SIDE == 'right' else 'right'} side for {DRIVER_LAYOUT} cabin")
    box("interior", "dash_instrument_cluster_plate", 1208, DRIVER_Y, 1128, 36, 330, 170, COLORS["reference"], "L2 visible-detail primitive", f"instrument cluster plate on {DRIVER_LAYOUT} side")
    for idx, y in enumerate([value * DRIVER_Y_SIGN for value in [535, 480, 425, 370, 315]], start=1):
        cyl("interior", f"dash_switch_knob_{idx}", 1200, y, 1050, "x", 34, 26, COLORS["metal"], "L2 visible-detail primitive", "dash switch knob")
    for idx, y in enumerate([value * -DRIVER_Y_SIGN for value in [90, 155, 220, 285]], start=1):
        cyl("interior", f"heater_control_knob_{idx}", 1200, y, 1048, "x", 30, 24, COLORS["metal"], "L2 visible-detail primitive", "heater/control knob")
    for spoke_idx, y in enumerate([DRIVER_Y - 90 * DRIVER_Y_SIGN, DRIVER_Y, DRIVER_Y + 90 * DRIVER_Y_SIGN], start=1):
        box("interior", f"steering_wheel_spoke_{spoke_idx}", 1216, y, 1205, 34, 170, 18, COLORS["metal"], "L2 visible-detail primitive", "steering wheel spoke reference")
    pedal_layout = [("clutch", DRIVER_Y - 70 * DRIVER_Y_SIGN), ("brake", DRIVER_Y + 20 * DRIVER_Y_SIGN), ("accelerator", DRIVER_Y + 100 * DRIVER_Y_SIGN)]
    for pedal_idx, (name, y) in enumerate(pedal_layout, start=1):
        box("interior", f"{name}_pedal_pad", 1340, y, 705, 90, 45, 110, COLORS["rubber"], "L2 visible-detail primitive", "pedal pad")
        cyl("interior", f"{name}_pedal_arm", 1300, y, 820, "z", 22, 240, COLORS["metal"], "L2 visible-detail primitive", "pedal arm")
    box("interior", "rhd_pedal_box_reinforcement", 1195, DRIVER_Y + 45 * DRIVER_Y_SIGN, 850, 95, 285, 250, COLORS["metal"], "L2 service datum", "right-hand-drive pedal box reinforcement at driver firewall")
    box("interior", "rhd_steering_column_dash_bracket", 1215, DRIVER_Y, 1040, 62, 210, 66, COLORS["metal"], "L2 service datum", "right-hand-drive steering column dash support bracket")
    cyl("interior", "steering_column_firewall_boot", 1142, DRIVER_Y, 1020, "x", 130, 48, COLORS["rubber"], "L2 visible-detail primitive", f"rubber boot where {DRIVER_LAYOUT} steering column passes through firewall")
    cyl("interior", "brake_pedal_pivot_bar", 1260, DRIVER_Y + 20 * DRIVER_Y_SIGN, 960, "y", 32, 180, COLORS["metal"], "L2 service datum", "RHD brake pedal pivot bar")
    cyl("interior", "clutch_pedal_pivot_bar", 1260, DRIVER_Y - 70 * DRIVER_Y_SIGN, 960, "y", 32, 170, COLORS["metal"], "L2 service datum", "RHD clutch pedal pivot bar")
    box("interior", "accelerator_linkage_pivot", 1225, DRIVER_Y + 118 * DRIVER_Y_SIGN, 875, 52, 42, 125, COLORS["metal"], "L2 service datum", "RHD accelerator linkage pivot on driver side")
    cyl("interior", "steering_column_indicator_stalk", 1225, DRIVER_Y + 185 * DRIVER_Y_SIGN, 1220, "y", 22, 165, COLORS["metal"], "L2 visible-detail primitive", "right-hand-drive steering column stalk reference")
    box("interior", "driver_side_floor_dimmer_switch", 1290, DRIVER_Y + 230 * DRIVER_Y_SIGN, 735, 70, 55, 34, COLORS["rubber"], "L2 visible-detail primitive", "floor dimmer/switch placeholder on RHD driver footwell")
    cyl("interior", "handbrake_lever", 1760, 250 * DRIVER_Y_SIGN, 790, "z", 32, 360, COLORS["metal"], "L2 visible-detail primitive", f"handbrake lever biased toward {DRIVER_LAYOUT} driver side")
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
    cyl("engine_bay", "brake_booster", 1075, 520 * DRIVER_Y_SIGN, 1060, "x", 260, 145, COLORS["metal"], "L2 service datum", "RHD brake booster package")
    cyl("engine_bay", "master_cylinder", 945, 520 * DRIVER_Y_SIGN, 1060, "x", 92, 230, COLORS["metal"], "L2 service datum", "RHD brake master cylinder")
    box("engine_bay", "clutch_master_cylinder", 945, 350 * DRIVER_Y_SIGN, 1035, 210, 82, 76, COLORS["metal"], "L2 service datum", "RHD clutch master cylinder")
    box("engine_bay", "rhd_firewall_pedal_box_outer_plate", 1112, DRIVER_Y + 55 * DRIVER_Y_SIGN, 895, 42, 350, 300, COLORS["metal"], "L2 service datum", "right-hand-drive pedal box outer reinforcement on firewall")
    box("engine_bay", "brake_booster_firewall_bracket", 1110, 520 * DRIVER_Y_SIGN, 1015, 48, 300, 250, COLORS["metal"], "L2 service datum", "RHD brake booster firewall bracket")
    cyl("engine_bay", "brake_master_reservoir", 875, 520 * DRIVER_Y_SIGN, 1165, "z", 110, 105, COLORS["reference"], "L2 service datum", "brake fluid reservoir on right-hand-drive master cylinder")
    cyl("engine_bay", "brake_master_reservoir_cap", 875, 520 * DRIVER_Y_SIGN, 1225, "z", 82, 24, COLORS["brass"], "L2 visible-detail primitive", "brake master reservoir cap")
    cyl("engine_bay", "brake_booster_vacuum_hose", 820, 430 * DRIVER_Y_SIGN, 1130, "x", 34, 470, COLORS["rubber"], "L2 routing reference", "vacuum hose from engine to RHD brake booster")
    cyl("engine_bay", "clutch_master_reservoir_cap", 910, 350 * DRIVER_Y_SIGN, 1130, "z", 70, 26, COLORS["brass"], "L2 service datum", "clutch master reservoir cap")
    cyl("engine_bay", "clutch_hydraulic_line_firewall_run", 830, 350 * DRIVER_Y_SIGN, 980, "x", 14, 520, COLORS["metal"], "L2 routing reference", "clutch hydraulic line from RHD master cylinder")
    cyl("engine_bay", "steering_column_lower_firewall_shaft", 1010, DRIVER_Y, 980, "x", 44, 340, COLORS["metal"], "L2 routing reference", "RHD steering shaft leaving firewall toward steering box")
    cyl("engine_bay", "steering_column_lower_universal_joint", 840, DRIVER_Y + 10 * DRIVER_Y_SIGN, 955, "x", 76, 58, COLORS["metal"], "L2 service datum", "lower steering universal joint")
    cyl("engine_bay", "steering_intermediate_shaft", 690, DRIVER_Y + 35 * DRIVER_Y_SIGN, 850, "x", 40, 360, COLORS["metal"], "L2 routing reference", "intermediate steering shaft to right steering box")
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

    # As-fitted route scope. These named centerlines are release-gate placeholders
    # from j40_as_fitted_route_model_scope_20260531.csv; physical endpoints,
    # supports, and bend radii still need truck measurements before L3 release.
    route_segment("J40-RT-001", "engine_gearbox_transfer_centerline", 1640, 0, 642, "x", 20, 2600, COLORS["datum"], "L2 orientation check")
    route_segment("J40-RT-001", "front_output_to_front_pinion", 1188, -82, 468, "x", 20, 920, COLORS["datum"], "L2 orientation check")
    route_segment("J40-RT-001", "rear_output_to_rear_pinion", 2235, 70, 468, "x", 20, 1430, COLORS["datum"], "L2 orientation check")
    route_segment("J40-RT-002", "battery_to_cutoff_sweep", 735, 432, 1032, "x", 28, 430, COLORS["route_power"])
    route_segment("J40-RT-003", "cutoff_to_relay_feed", 850, 540, 1040, "x", 24, 430, COLORS["route_power"])
    route_segment("J40-RT-004", "cutoff_to_midi_common", 860, 624, 980, "x", 26, 470, COLORS["route_power"])
    route_segment("J40-RT-005", "midi_output_fanout", 1030, 670, 950, "y", 18, 360, COLORS["route_power"])
    route_segment("J40-RT-006", "battery_negative_to_engine", 695, 310, 930, "x", 24, 520, COLORS["metal"])
    route_segment("J40-RT-006", "body_chassis_ground_strap", 1115, 520 * DRIVER_Y_SIGN, 760, "z", 22, 280, COLORS["metal"])
    route_segment("J40-RT-007", "starter_main_cable", 720, 286, 760, "x", 24, 550, COLORS["route_power"])
    route_segment("J40-RT-007", "starter_solenoid_trigger", 780, 236, 820, "x", 12, 460, COLORS["route_power"])
    route_segment("J40-RT-008", "alternator_charge_branch", 625, 325, 1065, "x", 20, 590, COLORS["route_power"])
    route_segment("J40-RT-009", "engine_sender_injection_pump_branch", 745, -165, 1085, "x", 16, 760, COLORS["route_power"])
    route_segment("J40-RT-010", "front_lamp_cross_loom", 145, 0, 735, "y", 18, 1280, COLORS["route_power"])
    route_segment("J40-RT-011", "compressor_pressure_fan_branch", 500, 485, 970, "x", 16, 720, COLORS["route_power"])
    route_segment("J40-RT-012", "under_dash_evaporator_feed", 1230, PASSENGER_Y, 985, "y", 18, 520, COLORS["route_power"])
    route_segment("J40-RT-013", "main_firewall_pass_through_band", 1120, 0, 995, "y", 22, 1160, COLORS["route_control"])
    route_segment("J40-RT-014", "rear_body_tail_fuel_sender_loom", 2835, -520, 700, "x", 18, 1160, COLORS["route_power"])
    route_segment("J40-RT-015", "front_brake_master_to_crossmember", 980, 338 * DRIVER_Y_SIGN, 650, "x", 16, 920, COLORS["route_fluid"])
    route_segment("J40-RT-015", "front_brake_flex_sweep_left", front_axle_x + 85, -650, wheel_z + 185, "y", 20, 250, COLORS["route_fluid"])
    route_segment("J40-RT-015", "front_brake_flex_sweep_right", front_axle_x + 85, 650, wheel_z + 185, "y", 20, 250, COLORS["route_fluid"])
    route_segment("J40-RT-016", "rear_axle_brake_pipe_and_center_flex", rear_axle_x, 0, 548, "y", 18, 1330, COLORS["route_fluid"])
    route_segment("J40-RT-017", "parking_brake_equalizer_to_axle", 2505, 0, 568, "x", 22, 980, COLORS["route_control"])
    route_segment("J40-RT-018", "fuel_supply_return_frame_pair", 1880, 306, 542, "x", 18, 2100, COLORS["route_fluid"])
    route_segment("J40-RT-019", "filler_neck_and_vent_pair", 3000, -650, 865, "z", 42, 440, COLORS["route_fluid"])
    route_segment("J40-RT-020", "ac_discharge_compressor_to_condenser", 470, 535, 1080, "x", 24, 680, COLORS["route_fluid"])
    route_segment("J40-RT-021", "ac_condenser_to_drier_liquid_line", 330, -520, 915, "y", 18, 930, COLORS["route_fluid"])
    route_segment("J40-RT-022", "ac_firewall_to_evaporator_suction_pair", 980, PASSENGER_Y, 1035, "x", 26, 650, COLORS["route_fluid"])
    route_segment("J40-RT-023", "radiator_heater_overflow_hose_bundle", 395, -230, 1075, "x", 38, 620, COLORS["route_fluid"])
    route_segment("J40-RT-024", "throttle_choke_fuel_stop_control_cables", 1050, DRIVER_Y - 70 * DRIVER_Y_SIGN, 915, "x", 18, 560, COLORS["route_control"])
    route_segment("J40-RT-025", "speedometer_cable_cluster_to_transfer", 1460, DRIVER_Y - 185 * DRIVER_Y_SIGN, 820, "x", 18, 780, COLORS["route_control"])
    route_segment("J40-RT-026", "evaporator_condensate_drain", 1235, PASSENGER_Y - 135 * DRIVER_Y_SIGN, 660, "z", 24, 430, COLORS["route_fluid"])
    route_segment("J40-RT-027", "exhaust_heat_route_reference", 1910, 330, 610, "x", 36, 2260, COLORS["clearance"], "L2 heat-clearance check")
    route_segment("J40-RT-028", "routing_supports_spine", 1860, 430 * DRIVER_Y_SIGN, 620, "x", 14, 2240, COLORS["chrome"])

    for clip_idx, x in enumerate([650, 930, 1210, 1510, 1830, 2160, 2480, 2800, 3130], start=1):
        route_clip("J40-RT-028", f"shared_route_support_{clip_idx}", x, 430 * DRIVER_Y_SIGN, 620)
    for clearance_name, x, y, z, length, width, height, notes in [
        ("fan_radiator_clearance_envelope", 275, 0, 990, 150, 720, 510, "fan, shroud, radiator, and condenser clearance volume"),
        ("front_steering_lock_sweep_left", front_axle_x + 20, -705, 500, 420, 260, 250, "left front wheel/brake hose steering-lock movement sweep"),
        ("front_steering_lock_sweep_right", front_axle_x + 20, 705, 500, 420, 260, 250, "right front wheel/brake hose steering-lock movement sweep"),
        ("front_prop_shaft_clearance_tunnel", 1120, 0, 438, 980, 260, 210, "front prop-shaft movement and exhaust/routing no-foul envelope"),
        ("rear_prop_shaft_clearance_tunnel", 2180, 0, 438, 1480, 280, 220, "rear prop-shaft movement and parking-brake/fuel-line no-foul envelope"),
        ("pedal_column_hvac_clearance_zone", 1215, DRIVER_Y, 900, 420, 390, 420, "pedal, steering-column, HVAC, and firewall route service clearance zone"),
    ]:
        box("mechanical_clearance", clearance_name, x, y, z, length, width, height, COLORS["clearance"], "L2 mechanical soundness clearance check", notes)

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
        f"// {DRIVER_LAYOUT_NOTE}",
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
        elif isinstance(part, WheelPart):
            lines.append(f"wheel_part({part.x:g}, {part.y:g}, {part.z:g}, {part.diameter:g}, {part.width:g});")
        elif isinstance(part, CylinderPart):
            lines.append(f"color({hex_to_scad_color(part.color)})")
            lines.append(
                f"  cylinder_part({part.x:g}, {part.y:g}, {part.z:g}, \"{part.axis}\", {part.diameter:g}, {part.length:g});"
            )
        else:
            points = "[" + ", ".join(f"[{x:g}, {y:g}, {z:g}]" for x, y, z in part.vertices) + "]"
            faces = "[" + ", ".join("[" + ", ".join(str(index) for index in face) + "]" for face in part.faces) + "]"
            lines.append(f"color({hex_to_scad_color(part.color)})")
            lines.append(f"  polyhedron(points = {points}, faces = {faces}, convexity = 4);")
        lines.append("")
    path = OUT_DIR / f"{MODEL_NAME}.scad"
    path.write_text("\n".join(lines), encoding="ascii")
    return path


def write_freecad_macro(model_parts: list[PartType]) -> Path:
    lines = [
        f"# {MODEL_SHORT_TITLE}",
        "# Units: millimetres. Run inside FreeCAD.",
        f"# {DRIVER_LAYOUT_NOTE}",
        "# Generated by tools/generate_j40_full_vehicle_cad_scaffold.py.",
        "import FreeCAD as App",
        "import Part",
        "import Mesh",
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
        "    'as_fitted_routes': 15,",
        "    'mechanical_clearance': 72,",
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
        "def add_mesh(group_name, name, vertices, faces, rgb):",
        "    mesh = Mesh.Mesh()",
        "    for face in faces:",
        "        if len(face) < 3:",
        "            continue",
        "        first = App.Vector(*vertices[face[0]])",
        "        for index in range(1, len(face) - 1):",
        "            mesh.addFacet(first, App.Vector(*vertices[face[index]]), App.Vector(*vertices[face[index + 1]]))",
        "    obj = doc.addObject('Mesh::Feature', name)",
        "    obj.Mesh = mesh",
        "    obj.Label = name.replace('_', ' ')",
        "    set_color(obj, rgb, group_name)",
        "    return add_to_group(obj, group_name)",
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
        elif isinstance(part, CylinderPart):
            color = hex_to_fc_color(part.color)
            lines.append(
                "add_cylinder("
                f"{part.group!r}, {safe!r}, {part.x:g}, {part.y:g}, {part.z:g}, {part.axis!r}, {part.diameter:g}, {part.length:g}, "
                f"({color[0]:.3f}, {color[1]:.3f}, {color[2]:.3f}))"
            )
        else:
            color = hex_to_fc_color(part.color)
            vertices = "[" + ", ".join(f"({x:g}, {y:g}, {z:g})" for x, y, z in part.vertices) + "]"
            faces = "[" + ", ".join("(" + ", ".join(str(index) for index in face) + ")" for face in part.faces) + "]"
            lines.append(
                "add_mesh("
                f"{part.group!r}, {safe!r}, {vertices}, {faces}, "
                f"({color[0]:.3f}, {color[1]:.3f}, {color[2]:.3f}))"
            )
    lines.extend(["", "doc.recompute()", "Gui.SendMsgToActiveView('ViewFit') if Gui is not None else None", ""])
    path = OUT_DIR / f"{MODEL_NAME}.FCMacro"
    path.write_text("\n".join(lines), encoding="ascii")
    return path


def project_rect(part: PartType, view: str) -> tuple[float, float, float, float] | None:
    if isinstance(part, MeshPart):
        xs = [point[0] for point in part.vertices]
        ys = [point[1] for point in part.vertices]
        zs = [point[2] for point in part.vertices]
        bounds = (min(xs), min(ys), min(zs), max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
        bx, by, bz, bl, bw, bh = bounds
        if view == "plan":
            return (bx, by, bl, bw)
        if view == "side":
            return (bx, bz, bl, bh)
        if view == "front":
            return (by, bz, bw, bh)
        return None
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
        f'<text x="40" y="52">Units mm. {DRIVER_LAYOUT.capitalize()} reference scaffold only; refine after CC-BY mesh and vehicle measurements arrive.</text>',
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
            if part.group == "mechanical_clearance":
                svg.append(
                    f'<rect x="{rx:.2f}" y="{ry:.2f}" width="{rw:.2f}" height="{rh:.2f}" '
                    f'fill="none" stroke="{part.color}" stroke-width="1.2" stroke-dasharray="7 4"/>'
                )
                continue
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
        f"Units mm. {DRIVER_LAYOUT.capitalize()} reference scaffold only; refine after CC-BY mesh and vehicle measurements arrive.",
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
            if part.group == "mechanical_clearance":
                draw.rectangle(
                    (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)),
                    outline=rgba(part.color, 230),
                    width=2,
                )
                continue
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


def vec_normalize(a: tuple[float, float, float]) -> tuple[float, float, float]:
    length = math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])
    if length <= 0:
        return (0.0, 0.0, 1.0)
    return (a[0] / length, a[1] / length, a[2] / length)


def box_bevel_mm(part: BoxPart) -> float:
    min_dimension = min(part.length, part.width, part.height)
    if min_dimension < 28 or part.group in {"datum", "brake_system", "fuel_system", "exhaust"}:
        return 0.0
    if "datum" in part.confidence.lower() or "routing" in part.confidence.lower():
        return 0.0
    group_bevels = {
        "body": 36.0,
        "hard_top": 38.0,
        "front_detail": 18.0,
        "interior": 20.0,
        "engine_bay": 12.0,
        "chassis": 10.0,
        "running_gear": 8.0,
    }
    target = group_bevels.get(part.group, 8.0)
    return min(target, min_dimension * 0.42)


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


def add_gltf_chamfer_quad(
    positions: list[tuple[float, float, float]],
    normals: list[tuple[float, float, float]],
    points: tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]],
    normal: tuple[float, float, float],
) -> None:
    add_gltf_quad(positions, normals, *points, vec_normalize(normal))


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
    bevel = box_bevel_mm(part)
    x0 = part.x
    x1 = part.x + part.length
    y0 = part.y - part.width / 2
    y1 = part.y + part.width / 2
    z0 = part.z
    z1 = part.z + part.height
    if bevel > 0:
        cx = (x0 + x1) / 2
        cy = part.y
        cz = (z0 + z1) / 2
        hx = part.length / 2
        hy = part.width / 2
        hz = part.height / 2
        bevel = min(bevel, hx * 0.42, hy * 0.42, hz * 0.42)
        if bevel <= 0:
            return positions, normals

        def point(x: float, y: float, z: float) -> tuple[float, float, float]:
            return (cx + x, cy + y, cz + z)

        # Six broad faces.
        add_gltf_chamfer_quad(
            positions,
            normals,
            (point(hx, -hy + bevel, -hz + bevel), point(hx, hy - bevel, -hz + bevel), point(hx, hy - bevel, hz - bevel), point(hx, -hy + bevel, hz - bevel)),
            (1.0, 0.0, 0.0),
        )
        add_gltf_chamfer_quad(
            positions,
            normals,
            (point(-hx, -hy + bevel, -hz + bevel), point(-hx, -hy + bevel, hz - bevel), point(-hx, hy - bevel, hz - bevel), point(-hx, hy - bevel, -hz + bevel)),
            (-1.0, 0.0, 0.0),
        )
        add_gltf_chamfer_quad(
            positions,
            normals,
            (point(-hx + bevel, hy, -hz + bevel), point(-hx + bevel, hy, hz - bevel), point(hx - bevel, hy, hz - bevel), point(hx - bevel, hy, -hz + bevel)),
            (0.0, 1.0, 0.0),
        )
        add_gltf_chamfer_quad(
            positions,
            normals,
            (point(-hx + bevel, -hy, -hz + bevel), point(hx - bevel, -hy, -hz + bevel), point(hx - bevel, -hy, hz - bevel), point(-hx + bevel, -hy, hz - bevel)),
            (0.0, -1.0, 0.0),
        )
        add_gltf_chamfer_quad(
            positions,
            normals,
            (point(-hx + bevel, -hy + bevel, hz), point(hx - bevel, -hy + bevel, hz), point(hx - bevel, hy - bevel, hz), point(-hx + bevel, hy - bevel, hz)),
            (0.0, 0.0, 1.0),
        )
        add_gltf_chamfer_quad(
            positions,
            normals,
            (point(-hx + bevel, -hy + bevel, -hz), point(-hx + bevel, hy - bevel, -hz), point(hx - bevel, hy - bevel, -hz), point(hx - bevel, -hy + bevel, -hz)),
            (0.0, 0.0, -1.0),
        )

        # Twelve edge chamfers.
        for sx in (-1.0, 1.0):
            for sy in (-1.0, 1.0):
                add_gltf_chamfer_quad(
                    positions,
                    normals,
                    (
                        point(sx * hx, sy * (hy - bevel), -hz + bevel),
                        point(sx * (hx - bevel), sy * hy, -hz + bevel),
                        point(sx * (hx - bevel), sy * hy, hz - bevel),
                        point(sx * hx, sy * (hy - bevel), hz - bevel),
                    ),
                    (sx, sy, 0.0),
                )
        for sx in (-1.0, 1.0):
            for sz in (-1.0, 1.0):
                add_gltf_chamfer_quad(
                    positions,
                    normals,
                    (
                        point(sx * hx, -hy + bevel, sz * (hz - bevel)),
                        point(sx * (hx - bevel), -hy + bevel, sz * hz),
                        point(sx * (hx - bevel), hy - bevel, sz * hz),
                        point(sx * hx, hy - bevel, sz * (hz - bevel)),
                    ),
                    (sx, 0.0, sz),
                )
        for sy in (-1.0, 1.0):
            for sz in (-1.0, 1.0):
                add_gltf_chamfer_quad(
                    positions,
                    normals,
                    (
                        point(-hx + bevel, sy * hy, sz * (hz - bevel)),
                        point(-hx + bevel, sy * (hy - bevel), sz * hz),
                        point(hx - bevel, sy * (hy - bevel), sz * hz),
                        point(hx - bevel, sy * hy, sz * (hz - bevel)),
                    ),
                    (0.0, sy, sz),
                )

        # Eight corner chamfers.
        for sx in (-1.0, 1.0):
            for sy in (-1.0, 1.0):
                for sz in (-1.0, 1.0):
                    add_gltf_triangle(
                        positions,
                        normals,
                        point(sx * hx, sy * (hy - bevel), sz * (hz - bevel)),
                        point(sx * (hx - bevel), sy * hy, sz * (hz - bevel)),
                        point(sx * (hx - bevel), sy * (hy - bevel), sz * hz),
                        vec_normalize((sx, sy, sz)),
                    )
        return positions, normals

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


def face_normal(points: list[tuple[float, float, float]]) -> tuple[float, float, float]:
    if len(points) < 3:
        return (0.0, 0.0, 1.0)
    a = points[0]
    b = points[1]
    c = points[2]
    ab = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    ac = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    return vec_normalize(
        (
            ab[1] * ac[2] - ab[2] * ac[1],
            ab[2] * ac[0] - ab[0] * ac[2],
            ab[0] * ac[1] - ab[1] * ac[0],
        )
    )


def gltf_mesh_part_mesh(part: MeshPart) -> tuple[list[tuple[float, float, float]], list[tuple[float, float, float]]]:
    positions: list[tuple[float, float, float]] = []
    normals: list[tuple[float, float, float]] = []
    for face in part.faces:
        if len(face) < 3:
            continue
        points = [part.vertices[index] for index in face]
        normal = face_normal(points)
        for index in range(1, len(points) - 1):
            add_gltf_triangle(positions, normals, points[0], points[index], points[index + 1], normal)
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
        elif isinstance(part, MeshPart):
            positions, normals = gltf_mesh_part_mesh(part)
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
            metallic = 0.0
            roughness = 0.72
            if color in {COLORS["metal"], COLORS["chrome"], COLORS["brass"]}:
                metallic = 0.75
                roughness = 0.34 if color == COLORS["chrome"] else 0.48
            elif color in {COLORS["black_trim"], COLORS["rubber"], COLORS["glass_dark"]}:
                roughness = 0.88
            elif color in {COLORS["body_sand"], COLORS["body_shadow"], COLORS["body_highlight"], COLORS["roof_white"]}:
                roughness = 0.58
            elif color in {COLORS["amber"], COLORS["electrical"], COLORS["grille_yellow"]}:
                roughness = 0.42
            material: dict[str, object] = {
                "name": next((name for name, value in COLORS.items() if value == color), color),
                "pbrMetallicRoughness": {
                    "baseColorFactor": hex_to_rgba_factor(color, alpha),
                    "metallicFactor": metallic,
                    "roughnessFactor": roughness,
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
            "drive_side": DRIVER_LAYOUT,
            "traffic_side": TRAFFIC_SIDE,
            "driver_side_y_sign": DRIVER_Y_SIGN,
            "driver_side": DRIVER_SIDE,
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
            elif isinstance(part, CylinderPart):
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
            else:
                xs = [point[0] for point in part.vertices]
                ys = [point[1] for point in part.vertices]
                zs = [point[2] for point in part.vertices]
                writer.writerow(
                    [
                        part.group,
                        part.name,
                        "mesh",
                        min(xs),
                        (min(ys) + max(ys)) / 2,
                        min(zs),
                        max(xs) - min(xs),
                        max(ys) - min(ys),
                        max(zs) - min(zs),
                        part.confidence,
                        part.notes,
                    ]
                )
    return path


def write_online_reference_inventory() -> Path:
    path = REPORT_DIR / f"{MODEL_NAME}_online_reference_inventory.csv"
    with path.open("w", newline="", encoding="ascii") as handle:
        fieldnames = ["source_id", "title", "url", "source_type", "permission_basis", "rev_c_use"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ONLINE_REFERENCE_ROWS)
    return path


def write_route_model_coverage(model_parts: list[PartType]) -> Path:
    matches = as_fitted_route_model_matches(model_parts)
    route_scope = read_as_fitted_route_scope()
    path = AS_FITTED_ROUTE_MODEL_COVERAGE
    with path.open("w", newline="", encoding="ascii") as handle:
        fieldnames = [
            "route_id",
            "system",
            "route_name",
            "model_level_target",
            "coverage_status",
            "model_part_count",
            "model_part_names",
            "geometry_to_capture",
            "clearance_checks",
            "release_gate",
            "scope_status",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for route_id, row in sorted(route_scope.items()):
            parts_for_route = matches.get(route_id, [])
            writer.writerow(
                {
                    "route_id": route_id,
                    "system": row.get("system", ""),
                    "route_name": row.get("route_name", ""),
                    "model_level_target": row.get("model_level_target", ""),
                    "coverage_status": "represented_in_generator" if parts_for_route else "missing_model_geometry",
                    "model_part_count": len(parts_for_route),
                    "model_part_names": "|".join(part.name for part in parts_for_route),
                    "geometry_to_capture": row.get("geometry_to_capture", ""),
                    "clearance_checks": row.get("clearance_checks", ""),
                    "release_gate": row.get("release_gate", ""),
                    "scope_status": row.get("status", ""),
                }
            )
    return path


def write_notes(model_parts: list[PartType], outputs: list[Path]) -> Path:
    path = REPORT_DIR / f"{MODEL_NAME}_notes.md"
    route_metrics = as_fitted_route_metrics(model_parts)
    lines = [
        f"# {MODEL_TITLE}",
        "",
        "This is a project-owned from-scratch CAD scaffold. It uses the CC-BY FJ40 Sketchfab references, the project photo inventory, public/commercial 3D model representations covered for project use, and Toyota online parts representations as visual and service-reference cues. Source files are not redistributed here unless a licensed/local asset is placed in the intake folder.",
        "",
        "## Basis",
        "",
        "- Toyota representative FJ40 dimensions: 3840 mm length, 1665 mm width, 1950 mm height, 2285 mm wheelbase.",
        "- Open-source visual reference: 1976 Toyota Land Cruiser FJ40 by tonielpro520 on Sketchfab, CC Attribution 4.0.",
        "- Additional open visual reference: Toyota Land Cruiser by Game Garage on Sketchfab, listed as Creative Commons Attribution, used for high-density material and interior/detail cues.",
        "- Commercial visual/reference benchmarks: 3DModels.org Toyota Land Cruiser (J40) Hard Top 1979 and CGTrader Toyota Land-Cruiser J40 Hard Top BJ44V 1979 printable listing. Commercial coverage was confirmed by the project owner; this generator stores only project-owned procedural geometry and provenance metadata unless licensed assets are added locally.",
        "- Toyota online parts representations: EPC body/interior groups and GR Heritage 40 parts list, used for factual part-name cues such as roof/rear ventilators, body mounts, bumper stays, rear combination lamp segmentation, brake tubes, wiper caps, mirror packing, and fuel inlet hose.",
        "- Project-photo visual target: sand/beige diesel hardtop J40 with white roof, black bumper/trim, round auxiliary lamps, black window seals, side step boards, and mud-terrain tires.",
        "- Project-specific identity cues: Punjab BSN 453 front plate stroke reference, front disc/Sumitomo-style caliper package from May 29 brake photos, and raised mud-terrain sidewall lettering panels.",
        f"- Driving layout: {DRIVER_LAYOUT} for {TRAFFIC_SIDE}. {DRIVER_Y_DIRECTION.capitalize()} Y is the driver side in this coordinate system.",
        "- This scaffold does not extract or reproduce hidden source mesh data.",
        "- Source inventory: `data/manual/cad/j40_reference_model/05_reports/j40_full_vehicle_scaffold_rev_c_online_reference_inventory.csv`.",
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
            "- L2 visible-detail scaffold: grille slots/lights, bumper/tow points, hood ribs/latches, hardtop panels/windows/gutters, door hinges/handles/mirrors, right-hand-drive dashboard/gauges/switches, seats/belts/pedals, engine-bay accessories/hoses, suspension brackets, shocks, rims, tire lugs, hubs, and body pressings.",
            "- L3 exterior material references: separated grille mesh and TOYOTA lettering, fender-top lamps, side louvers, beltline trim, hardtop sliding-window mullions, classic rounded rear-quarter/back-door glass, rubber window radius gaskets, faceted black fender flares, step-board tread strips, mud flaps, rear barn-door seals/hinges/handles, spare-wheel spoke/highlight parts, wiper hardware, roof-gutter rivets, wheel-face vents, tire sidewall ticks, bumper bolts, license-plate screws, rear lamps, and spare-carrier latch plates.",
            "- L4 gallery-shaped surfaces: closed crowned hood, rolled hood lip, raked windshield surface, inset grille surround, sloped front fender skins, rolled fender crowns, tapered door/rear-quarter skins, tapered hardtop side skins, hardtop rear-corner facets, body-color wheel-arch facets, and crowned hardtop roof skin.",
            "- Rev C online-reference details: roof ventilator lid/hinge/handle, rear hardtop ventilator louvers, classic rounded rear hardtop side windows and split rear-door glass, hardtop-to-body joins, front clip/tub joins, body-mount pucks and stands, front/rear bumper stays, hood underside bracing and prop rod, hood lock receiver, brake proportioning valve and tube clips, fuel sub-inlet/vent hoses, separated amber/red/clear rear combination lamp lenses, and interior gauge/grab-handle detail.",
            "- Digital-twin evidence pass: front disc rotors, Sumitomo-style caliper envelopes, caliper hose/fitting datums, BSN 453 plate strokes, and sidewall lettering panels are tied to project photos rather than generic J40 references.",
            "- Visual geometry pass: glTF and orbit-viewer box primitives use conservative chamfers on body, hardtop, front detail, interior, chassis, and running gear pieces to reduce the blocky placeholder look while preserving named part boundaries.",
            "- Right-hand-drive references: right-side steering wheel/column, right pedal box, right-firewall brake booster/master cylinder, clutch master, lower steering shaft, steering box, pitman arm, drag link, tie rod, steering damper, and driver-side handbrake reach. The pedal order remains clutch-brake-accelerator across the right footwell.",
            "- L3 specific-item references: rear parking-brake cable attachment hardware, equalizer, clevises, return springs, and frame/axle clips.",
            "- As-fitted route scope: every route row from `data/manual/cad/j40_reference_model/05_reports/j40_as_fitted_route_model_scope_20260531.csv` has a visible named placeholder or support/clearance primitive covering electrical power, starter/charging, engine controls, front lighting, A/C electrical, cabin HVAC, bulkhead, rear body loom, brake hydraulics, parking brake, fuel, A/C refrigerant, cooling, control cables, speedometer cable, drains, exhaust heat, and shared routing supports.",
            f"- Route generator coverage: {route_metrics['represented_rows']} of {route_metrics['scope_rows']} as-fitted route rows are represented by {route_metrics['route_part_count']} named `as_fitted_routes` parts. Coverage report: `data/manual/cad/j40_reference_model/05_reports/j40_as_fitted_route_model_coverage_20260531.csv`.",
            "- Mechanical-soundness references: fan/radiator, steering-lock/brake-hose, prop-shaft, exhaust heat, and pedal/column/HVAC clearance volumes are visible as non-release L2 checks.",
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
    route_metrics = as_fitted_route_metrics(model_parts)
    data = {
        "model": MODEL_NAME,
        "detail_revision": DETAIL_REVISION,
        "units": "mm",
        "coordinate_system": "X front bumper to rear, Y centreline left/right, Z ground up",
        "drive_side": DRIVER_LAYOUT,
        "traffic_side": TRAFFIC_SIDE,
        "driver_side_y_sign": DRIVER_Y_SIGN,
        "driver_side": DRIVER_SIDE,
        "basis_dimensions_mm": {"length": 3840, "width": 1665, "height": 1950, "wheelbase": 2285},
        "visual_benchmarks": [
            "https://sketchfab.com/3d-models/1976-toyota-land-cruiser-fj40-a4e58b09ce48444ca6164834c310880d",
            "https://sketchfab.com/3d-models/toyota-land-cruiser-cbcbd901e8874205b5be294fa3dd3df2",
            "https://3dmodels.org/3d-models/toyota-land-cruiser-j40-hard-top-1979/",
            "https://www.cgtrader.com/3d-print-models/hobby-diy/automotive/toyota-land-cruiser-j40-hard-top-bj44v-1979-df76b215-58fa-40f4-82f4-811350605600",
            "https://toyota.epc-data.com/land_cruiser/fj40/61645/body/",
            "https://toyotagazooracing.com/gr/heritage/landcruiser40/",
            "https://toyotagazooracing.com/-/media/TMC/tgr/global/contents/gr/heritage/pdf/Landcruiser40_en.pdf",
            "https://forum.ih8mud.com/threads/a-lot-of-people-have-been-asking-for-this-cad-model-for-fj40-frame.798358/",
            "https://forum.ih8mud.com/threads/3d-print-and-cad-file-repository-40-series.1281295/",
        ],
        "part_count": len(model_parts),
        "as_fitted_route_scope": str(AS_FITTED_ROUTE_SCOPE.relative_to(ROOT)),
        "as_fitted_route_model_coverage": str(AS_FITTED_ROUTE_MODEL_COVERAGE.relative_to(ROOT)),
        "as_fitted_route_scope_rows": route_metrics["scope_rows"],
        "as_fitted_route_rows_represented": route_metrics["represented_rows"],
        "as_fitted_route_part_count": route_metrics["route_part_count"],
        "mechanical_clearance_part_count": route_metrics["clearance_part_count"],
        "reference_gallery_image_count": 12,
        "online_reference_inventory": f"data/manual/cad/j40_reference_model/05_reports/{MODEL_NAME}_online_reference_inventory.csv",
        "outputs": [str(output.relative_to(ROOT)) for output in outputs],
    }
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="ascii")
    return path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    model_parts = parts()
    gallery_cues = REPORT_DIR / "j40_3dmodels_gallery_visual_cues.json"
    outputs = [
        write_scad(model_parts),
        write_freecad_macro(model_parts),
        write_svg(model_parts),
        write_png_preview(model_parts),
        write_dxf(model_parts),
        write_gltf(model_parts),
        write_inventory(model_parts),
        write_online_reference_inventory(),
        write_route_model_coverage(model_parts),
    ]
    if gallery_cues.exists():
        outputs.append(gallery_cues)
    notes = write_notes(model_parts, outputs)
    manifest = write_manifest(outputs + [notes], model_parts)
    for output in outputs + [notes, manifest]:
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
