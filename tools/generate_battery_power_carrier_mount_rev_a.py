from __future__ import annotations

import csv
from pathlib import Path

import generate_electrical_module_drawings as base


OUT_DIR = Path("/Users/davidpridmore/IdeaProjects/J40/data/manual/fabrication/battery_power_carrier_mount_rev_a")
base.OUT_DIR = OUT_DIR
base.PDF_NAME = "j40_battery_power_carrier_mount_rev_a_dimension_sheet.pdf"

VISUAL_SVG_NAME = "battery_power_carrier_mount_rev_a_3d_visualisation.svg"
VISUAL_HTML_NAME = "battery_power_carrier_mount_rev_a_3d_visualisation.html"
ASSEMBLED_VISUAL_SVG_NAME = "battery_power_carrier_mount_rev_a_assembled_3d_visualisation.svg"
ASSEMBLED_VISUAL_HTML_NAME = "battery_power_carrier_mount_rev_a_assembled_3d_visualisation.html"


def integrated_backplane() -> base.Drawing:
    cut_polys = [
        base.Poly([(0, 0), (325, 0), (325, 120), (0, 120)]),
        # Rail-to-stand / front-cavity pickup slots. Final pitch follows the tray lip/upright mock-up.
        base.rounded_slot_poly(18, 22, 42, 16),
        base.rounded_slot_poly(265, 22, 42, 16),
        base.rounded_slot_poly(18, 82, 42, 16),
        base.rounded_slot_poly(265, 82, 42, 16),
        # Folded Relay Rev C tray attachment field, low on the front/radiator-side cassette.
        base.rounded_slot_poly(80, 18, 34, 12),
        base.rounded_slot_poly(210, 18, 34, 12),
        base.rounded_slot_poly(80, 88, 34, 12),
        base.rounded_slot_poly(210, 88, 34, 12),
        # Top-front shelf/base pickup points for the MIDI plate and folded cutoff base.
        base.rounded_slot_poly(130, 48, 28, 12),
        base.rounded_slot_poly(168, 48, 28, 12),
    ]
    cut_circles = [
        # Cable P-clip / saddle clamp holes.
        base.Circle(72, 60, 3.25),
        base.Circle(132, 60, 3.25),
        base.Circle(193, 60, 3.25),
        base.Circle(253, 60, 3.25),
    ]
    notes = [
        "Compact front/radiator-side service cassette spine: 325 x 120 x 3.0 mm mild steel. This supersedes the earlier large side/backplane route.",
        "The Relay Rev C folded aluminium tray mounts low on this front face so its 320 x 220 face stays inside the battery width envelope as far as practical.",
        "MIDI Rev C stays as the known open 190 x 150 plate/subplate, but moves to a shallow top-front shelf/tab rather than the inboard engine side.",
        "The folded cutoff base/guard moves to the top/front accessible corner, with lips bent upward around the 100A breaker/terminal side rather than downward as hidden stiffeners.",
        "Keep the inboard engine/LHD steering side as a keep-clear/service envelope except for protected cable clips. Do not cut final holes until the battery-cavity map proves radiator, hose, steering, bonnet, and cable-bend clearance.",
    ]
    return base.Drawing(
        "battery_power_compact_front_service_rail_rev_b",
        325,
        120,
        cut_polys,
        [],
        cut_circles,
        [],
        notes,
    )


def single_chassis_pickup_mount() -> base.Drawing:
    cut_polys = [
        base.Poly([(0, 0), (220, 0), (220, 230), (0, 230)]),
        # Lower leg through-bolt fields. Final hole pitch follows the actual chassis rail.
        base.rounded_slot_poly(24, 27, 44, 16),
        base.rounded_slot_poly(152, 27, 44, 16),
        # Upper leg through-bolt fields, mirrored so the bolt passes through both saddle legs and the chassis.
        base.rounded_slot_poly(24, 187, 44, 16),
        base.rounded_slot_poly(152, 187, 44, 16),
        # Top-cap upright/service-rail attach field.
        base.rounded_slot_poly(78, 92, 14, 42),
        base.rounded_slot_poly(128, 92, 14, 42),
    ]
    bend_lines = [
        base.Line(0, 70, 220, 70),
        base.Line(0, 160, 220, 160),
    ]
    notes = [
        "Compact single chassis saddle mount: nominal 220 x 230 x 4.0 mm mild steel flat pattern, formed over the one known chassis rail location.",
        "Bend blue lines 90 degrees downward to make a saddle: 70 mm near leg, measured chassis top cap nominal 90 mm, 70 mm far leg. Adjust the cap width after measuring the rail.",
        "Through-bolt both saddle legs and the chassis rail as one pickup location. Final slot pitch, bolt size, and crush-tube need are site-fit only.",
        "Top-cap slots take the upright/service-rail bridge. Do not add an independent second chassis fixing unless dry-fit proves the single-pickup route is not stiff enough.",
        "Deburr, radius leg bottoms, prime, isolate from fretting with an anti-chafe pad where appropriate, and protect before final assembly.",
    ]
    return base.Drawing(
        "battery_stand_compact_single_chassis_pickup_rev_b",
        220,
        230,
        cut_polys,
        [],
        [],
        bend_lines,
        notes,
    )


def single_mount_upright() -> base.Drawing:
    cut_polys = [
        base.Poly([(0, 0), (110, 0), (110, 220), (0, 220)]),
        base.rounded_slot_poly(18, 24, 16, 42),
        base.rounded_slot_poly(76, 24, 16, 42),
        base.rounded_slot_poly(18, 154, 16, 42),
        base.rounded_slot_poly(76, 154, 16, 42),
    ]
    cut_circles = [
        base.Circle(28, 102, 4.0),
        base.Circle(82, 102, 4.0),
        base.Circle(28, 128, 4.0),
        base.Circle(82, 128, 4.0),
    ]
    notes = [
        "Compact single-mount upright bridge side plate: 110 x 220 x 4.0 mm mild steel between the one chassis pickup and compact tray.",
        "Make two mirrored side plates around the single pickup bridge if the mock-up needs side-to-side stiffness. This is not a second chassis fixing location.",
        "Lower holes align to the formed chassis saddle top cap; upper holes align to the compact tray/front rail saddle.",
    ]
    return base.Drawing(
        "battery_stand_compact_single_mount_upright_rev_b",
        110,
        220,
        cut_polys,
        [],
        cut_circles,
        [],
        notes,
    )


def cutoff_guard() -> base.Drawing:
    cut_polys = [
        base.Poly(
            [
                (20, 0),
                (190, 0),
                (190, 20),
                (210, 20),
                (210, 130),
                (190, 130),
                (190, 150),
                (20, 150),
                (20, 130),
                (0, 130),
                (0, 20),
                (20, 20),
            ]
        ),
        # Hand/finger clearance window around the breaker reset lever and terminal side.
        base.rounded_slot_poly(64, 50, 82, 46),
    ]
    cut_circles = [
        base.Circle(38, 36, 3.25),
        base.Circle(172, 36, 3.25),
        base.Circle(38, 114, 3.25),
        base.Circle(172, 114, 3.25),
    ]
    bend_lines = [
        base.Line(20, 20, 190, 20),
        base.Line(20, 130, 190, 130),
        base.Line(20, 20, 20, 130),
        base.Line(190, 20, 190, 130),
    ]
    notes = [
        "Folded cutoff aluminium base/guard: 210 x 150 flat pattern, 170 x 110 finished face, 20 mm guard lips bent upward toward the 100A breaker/terminal side.",
        "Use 3.0 mm 5052-H32 aluminium unless dry-fit proves the cutoff must bolt to a steel structural tab instead.",
        "Open final breaker mounting holes only after the actual 100A breaker body, reset lever sweep, terminal studs, and cable-lug depth are measured.",
        "Guard lips must not trap water, block emergency access/reset operation, or foul the breaker body, cable lugs, bonnet, or battery terminal service envelope.",
    ]
    return base.Drawing(
        "battery_power_compact_cutoff_tab_rev_b",
        210,
        150,
        cut_polys,
        [],
        cut_circles,
        bend_lines,
        notes,
    )


def battery_stand_top_tray() -> base.Drawing:
    cut_polys = [
        base.Poly([(0, 0), (315, 0), (315, 265), (0, 265)]),
        # Battery hold-down / clamp slots.
        base.rounded_slot_poly(24, 38, 14, 38),
        base.rounded_slot_poly(24, 190, 14, 38),
        base.rounded_slot_poly(276, 38, 14, 38),
        base.rounded_slot_poly(276, 190, 14, 38),
        # Upright/front cassette saddle slots. Electrical modules mount to the front cassette, not engine-side panels.
        base.rounded_slot_poly(132, 42, 18, 40),
        base.rounded_slot_poly(168, 42, 18, 40),
        base.rounded_slot_poly(132, 180, 18, 40),
        base.rounded_slot_poly(168, 180, 18, 40),
    ]
    cut_circles = [
        # Drain/cable clip holes.
        base.Circle(56, 242, 3.25),
        base.Circle(106, 242, 3.25),
        base.Circle(156, 242, 3.25),
        base.Circle(206, 242, 3.25),
        base.Circle(256, 242, 3.25),
    ]
    notes = [
        "Compact battery stand top tray: 315 x 265 x 3.0 mm mild steel tray/deck around the 275 x 230 mm battery datum with service allowance.",
        "Electrical equipment uses the front/radiator-side service cassette: Relay Rev C low on the front face, MIDI Rev C on a top-front shelf, and cutoff on the top/front tab. Do not use tray skin or the engine-side gap as a large backplane.",
        "Final battery footprint, terminal side, clamp path, bonnet clearance, front-cavity clearance, and LHD steering-side clearance are vehicle-measurement holds.",
        "Add an acid-resistant battery mat after paint; do not allow battery case or terminals to touch live studs or sharp steel edges.",
    ]
    return base.Drawing(
        "battery_stand_compact_top_tray_rev_b",
        315,
        265,
        cut_polys,
        [],
        cut_circles,
        [],
        notes,
    )


def battery_hold_down_crossbar() -> base.Drawing:
    cut_polys = [
        base.Poly([(0, 0), (315, 0), (315, 38), (0, 38)]),
        base.rounded_slot_poly(18, 11, 42, 16),
        base.rounded_slot_poly(255, 11, 42, 16),
    ]
    notes = [
        "Compact battery hold-down crossbar: 315 x 38 x 3.0 mm mild steel or stainless. Length and slots are template values until the actual battery is measured.",
        "Use J-bolts or vertical rods that cannot touch battery terminals. Add insulated caps where needed.",
        "Do not over-tighten against a plastic battery case; retain the battery without distorting it.",
    ]
    return base.Drawing(
        "battery_stand_compact_hold_down_crossbar_rev_b",
        315,
        38,
        cut_polys,
        [],
        [],
        [],
        notes,
    )


def iso_point(x: float, y: float, z: float) -> tuple[float, float]:
    return 330 + (x - y) * 0.72, 110 + (x + y) * 0.33 - z * 1.05


def point_attr(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def iso_polygon(points: list[tuple[float, float, float]], css_class: str) -> str:
    return f'<polygon class="{css_class}" points="{point_attr([iso_point(*point) for point in points])}" />'


def iso_prism(
    x: float,
    y: float,
    w: float,
    d: float,
    z: float,
    h: float,
    top_class: str,
    right_class: str,
    front_class: str,
) -> list[str]:
    return [
        iso_polygon([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + h), (x + w, y, z + h)], right_class),
        iso_polygon([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + h), (x, y + d, z + h)], front_class),
        iso_polygon([(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)], top_class),
    ]


def iso_polyline(points: list[tuple[float, float, float]], css_class: str) -> str:
    return f'<polyline class="{css_class}" points="{point_attr([iso_point(*point) for point in points])}" />'


def write_static_3d_visualisation() -> None:
    elements: list[str] = []
    elements.append('<rect class="background" width="920" height="620" />')
    elements.append(iso_polygon([(-40, 385, -22), (610, 385, -22), (650, 438, -22), (0, 438, -22)], "shadow"))
    # Compact one-pickup stand with a formed saddle over the chassis rail.
    elements.extend(iso_prism(170, 178, 260, 100, -78, 54, "chassis-top", "chassis-side", "chassis-front"))
    elements.extend(iso_prism(188, 158, 220, 140, -28, 8, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(188, 150, 220, 10, -74, 48, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(188, 288, 220, 10, -74, 48, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(258, 190, 82, 70, -20, 92, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(220, 184, 24, 104, -24, 112, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(356, 184, 24, 104, -24, 112, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(82, 70, 315, 265, 72, 10, "plate-top", "plate-side", "plate-front"))
    elements.extend(iso_prism(102, 88, 275, 230, 82, 185, "battery-top", "battery-side", "battery-front"))
    elements.extend(iso_prism(94, 100, 315, 18, 274, 8, "hold-top", "hold-side", "hold-front"))
    elements.extend(iso_prism(94, 296, 315, 18, 274, 8, "hold-top", "hold-side", "hold-front"))
    elements.extend(iso_prism(72, 30, 325, 10, 82, 120, "plate-top", "plate-side", "plate-front"))
    # Known fabricated component bases now share a front/radiator-side service cassette.
    elements.extend(iso_prism(74, 38, 320, 8, 68, 220, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(70, 24, 8, 28, 68, 220, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(390, 24, 8, 28, 68, 220, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(74, 24, 320, 28, 60, 8, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(74, 24, 320, 28, 288, 8, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(104, 44, 260, 38, 105, 125, "relay-fuse-top", "relay-fuse-side", "relay-fuse-front"))
    elements.extend(iso_prism(92, 18, 190, 150, 292, 8, "midi-plate-top", "midi-plate-side", "midi-plate-front"))
    elements.extend(iso_prism(117, 44, 140, 85, 306, 10, "midi-board-top", "midi-board-side", "midi-board-front"))
    for idx in range(5):
        elements.extend(iso_prism(126 + idx * 24, 70, 18, 54, 322, 16, "fuse-top", "fuse-side", "fuse-front"))
    elements.extend(iso_prism(290, 18, 110, 170, 292, 8, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(286, 18, 8, 170, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(400, 18, 8, 170, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(290, 14, 110, 8, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(290, 188, 110, 8, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    # Keep-clear zone for the inboard engine/LHD steering side.
    elements.extend(iso_prism(420, 72, 18, 230, 78, 225, "keepout-top", "keepout-side", "keepout-front"))
    elements.extend(iso_prism(304, 74, 82, 56, 314, 28, "breaker-body-top", "breaker-body-side", "breaker-body-front"))
    elements.extend(iso_prism(309, 80, 72, 44, 342, 6, "breaker-face-top", "breaker-face-side", "breaker-face-front"))
    elements.extend(iso_prism(315, 96, 46, 10, 350, 6, "breaker-lever-top", "breaker-lever-side", "breaker-lever-front"))
    for point in [(318, 86, 350), (372, 110, 350)]:
        x, y = iso_point(*point)
        elements.append(f'<circle class="breaker-terminal" cx="{x:.1f}" cy="{y:.1f}" r="5" />')
    elements.append(iso_polyline([(275, 108, 280), (345, 98, 334), (318, 86, 350)], "positive-cable"))
    elements.append(iso_polyline([(372, 110, 350), (220, 86, 335), (180, 64, 322)], "relay-feed"))
    elements.append(iso_polyline([(180, 64, 322), (210, 42, 210), (170, 44, 160)], "branch-cable"))
    for point in [(214, 156, -50), (382, 156, -50), (214, 296, -50), (382, 296, -50)]:
        x, y = iso_point(*point)
        elements.append(f'<circle class="slot-marker" cx="{x:.1f}" cy="{y:.1f}" r="4" />')

    labels = [
        ("Formed chassis saddle", 126, 504),
        ("Single upright bridge", 166, 365),
        ("Compact battery tray / stand", 322, 434),
        ("Battery supported on stand", 252, 214),
        ("Front relay tray, low", 524, 230),
        ("Top-front MIDI shelf", 520, 305),
        ("100A breaker/cutoff tray", 568, 365),
        ("Engine/LHD side keep-clear", 570, 430),
    ]
    for text, x, y in labels:
        elements.append(f'<text class="label" x="{x}" y="{y}">{text}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="620" viewBox="0 0 920 620" role="img" aria-labelledby="title desc">
  <title id="title">Battery stand power carrier Rev C compact front-cassette 3D visualisation</title>
  <desc id="desc">Isometric visualisation of a compact steel battery stand mounted by a formed saddle over the chassis rail, carrying the battery on a reduced tray with the folded Relay Rev C tray low on the front face, MIDI Rev C on a top-front shelf, and a folded cutoff base/guard with upward lips at the top-front accessible corner while the inboard engine/LHD side stays clear.</desc>
  <style>
    .background {{ fill: #f6f7f8; }}
    .shadow {{ fill: #d9dde2; opacity: 0.55; }}
    .plate-top {{ fill: #cfd6dc; stroke: #4f5962; stroke-width: 1.4; }}
    .plate-side {{ fill: #9ca8b2; stroke: #4f5962; stroke-width: 1.2; }}
    .plate-front {{ fill: #b5bec7; stroke: #4f5962; stroke-width: 1.2; }}
    .tab-top {{ fill: #7f8992; stroke: #343b42; stroke-width: 1.2; }}
    .tab-side {{ fill: #515b64; stroke: #343b42; stroke-width: 1.1; }}
    .tab-front {{ fill: #66717a; stroke: #343b42; stroke-width: 1.1; }}
    .chassis-top {{ fill: #3b434a; stroke: #20262b; stroke-width: 1.2; }}
    .chassis-side {{ fill: #252c32; stroke: #20262b; stroke-width: 1.1; }}
    .chassis-front {{ fill: #303840; stroke: #20262b; stroke-width: 1.1; }}
    .battery-top {{ fill: #2f3942; stroke: #111820; stroke-width: 1.4; }}
    .battery-side {{ fill: #1d252c; stroke: #111820; stroke-width: 1.2; }}
    .battery-front {{ fill: #3d4852; stroke: #111820; stroke-width: 1.2; }}
    .hold-top {{ fill: #cfd6dc; stroke: #4f5962; stroke-width: 1.1; }}
    .hold-side {{ fill: #98a4ae; stroke: #4f5962; stroke-width: 0.9; }}
    .hold-front {{ fill: #b5bec7; stroke: #4f5962; stroke-width: 0.9; }}
    .relay-tray-top {{ fill: #aeb8c1; stroke: #4f5962; stroke-width: 1.2; }}
    .relay-tray-side {{ fill: #818d97; stroke: #4f5962; stroke-width: 1; }}
    .relay-tray-front {{ fill: #98a4ae; stroke: #4f5962; stroke-width: 1; }}
    .relay-fuse-top {{ fill: #384856; stroke: #1f2830; stroke-width: 0.8; }}
    .relay-fuse-side {{ fill: #26323d; stroke: #1f2830; stroke-width: 0.6; }}
    .relay-fuse-front {{ fill: #465867; stroke: #1f2830; stroke-width: 0.6; }}
    .relay-fuse-top {{ fill: #384856; stroke: #1f2830; stroke-width: 0.8; }}
    .relay-fuse-side {{ fill: #26323d; stroke: #1f2830; stroke-width: 0.6; }}
    .relay-fuse-front {{ fill: #465867; stroke: #1f2830; stroke-width: 0.6; }}
    .midi-plate-top {{ fill: #aeb8c1; stroke: #4f5962; stroke-width: 1.2; }}
    .midi-plate-side {{ fill: #818d97; stroke: #4f5962; stroke-width: 1; }}
    .midi-plate-front {{ fill: #98a4ae; stroke: #4f5962; stroke-width: 1; }}
    .midi-board-top {{ fill: #1f2930; stroke: #14191d; stroke-width: 1; }}
    .midi-board-side {{ fill: #161d22; stroke: #14191d; stroke-width: 0.9; }}
    .midi-board-front {{ fill: #2b363e; stroke: #14191d; stroke-width: 0.9; }}
    .fuse-top {{ fill: #b7302a; stroke: #6e1714; stroke-width: 0.8; }}
    .fuse-side {{ fill: #84201b; stroke: #6e1714; stroke-width: 0.7; }}
    .fuse-front {{ fill: #d14a43; stroke: #6e1714; stroke-width: 0.7; }}
    .cutoff-base-top {{ fill: #aeb8c1; stroke: #4f5962; stroke-width: 1.2; }}
    .cutoff-base-side {{ fill: #818d97; stroke: #4f5962; stroke-width: 1; }}
    .cutoff-base-front {{ fill: #98a4ae; stroke: #4f5962; stroke-width: 1; }}
    .keepout-top {{ fill: #d7dde2; stroke: #85909a; stroke-width: 1; stroke-dasharray: 6 4; opacity: 0.24; }}
    .keepout-side {{ fill: #c2cbd2; stroke: #85909a; stroke-width: 1; stroke-dasharray: 6 4; opacity: 0.18; }}
    .keepout-front {{ fill: #eef2f5; stroke: #85909a; stroke-width: 1; stroke-dasharray: 6 4; opacity: 0.14; }}
    .breaker-body-top {{ fill: #111820; stroke: #05080a; stroke-width: 1.2; }}
    .breaker-body-side {{ fill: #080c10; stroke: #05080a; stroke-width: 1; }}
    .breaker-body-front {{ fill: #202a33; stroke: #05080a; stroke-width: 1; }}
    .breaker-face-top {{ fill: #41515f; stroke: #1f2830; stroke-width: 1; }}
    .breaker-face-side {{ fill: #26323d; stroke: #1f2830; stroke-width: 0.9; }}
    .breaker-face-front {{ fill: #33424d; stroke: #1f2830; stroke-width: 0.9; }}
    .breaker-lever-top {{ fill: #d12828; stroke: #871313; stroke-width: 1; }}
    .breaker-lever-side {{ fill: #8f1717; stroke: #871313; stroke-width: 0.9; }}
    .breaker-lever-front {{ fill: #c41d1d; stroke: #871313; stroke-width: 0.9; }}
    .breaker-terminal {{ fill: #c4a35a; stroke: #6f5d2f; stroke-width: 1.1; }}
    .positive-cable {{ fill: none; stroke: #c41d1d; stroke-width: 8; stroke-linejoin: round; stroke-linecap: round; }}
    .relay-feed {{ fill: none; stroke: #a51515; stroke-width: 6; stroke-linejoin: round; stroke-linecap: round; }}
    .branch-cable {{ fill: none; stroke: #242b30; stroke-width: 6; stroke-linejoin: round; stroke-linecap: round; }}
    .slot-marker {{ fill: #eef3f7; stroke: #4f5962; stroke-width: 1.2; }}
    .label {{ font: 600 18px Arial, sans-serif; fill: #24313a; }}
  </style>
  {''.join(elements)}
</svg>
"""
    (OUT_DIR / VISUAL_SVG_NAME).write_text(svg, encoding="utf-8")


def write_interactive_3d_visualisation() -> None:
    html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>J40 Battery Stand Power Carrier Rev C Compact Front-Cassette - 3D Visualisation</title>
  <link rel="icon" href="data:,">
  <style>
    :root {
      color-scheme: light;
      font-family: Arial, Helvetica, sans-serif;
      background: #f5f6f7;
      color: #1d252c;
    }
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      grid-template-rows: auto 1fr;
    }
    body.embed {
      grid-template-rows: 1fr;
    }
    header {
      padding: 16px 22px 10px;
      background: #ffffff;
      border-bottom: 1px solid #d8dde2;
    }
    h1 {
      margin: 0;
      font-size: clamp(20px, 3vw, 30px);
      letter-spacing: 0;
    }
    .meta {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }
    .chip {
      border: 1px solid #c8d0d8;
      border-radius: 999px;
      padding: 5px 9px;
      background: #f8fafb;
      font-size: 13px;
    }
    main {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 300px;
      min-height: 0;
    }
    #viewport {
      position: relative;
      min-height: 560px;
      overflow: hidden;
    }
    canvas {
      display: block;
      width: 100%;
      height: 100%;
    }
    aside {
      border-left: 1px solid #d8dde2;
      background: #ffffff;
      padding: 18px;
    }
    h2 {
      margin: 0 0 12px;
      font-size: 18px;
      letter-spacing: 0;
    }
    dl {
      margin: 0;
      display: grid;
      gap: 12px;
    }
    dt {
      font-weight: 700;
    }
    dd {
      margin: 3px 0 0;
      color: #54616c;
      font-size: 14px;
      line-height: 1.45;
    }
    #fallback {
      position: absolute;
      inset: 0;
      display: grid;
      place-items: center;
      padding: 20px;
      background: #f5f6f7;
    }
    #fallback img {
      width: min(94vw, 920px);
      max-height: 82vh;
      object-fit: contain;
    }
    body.is-three-ready #fallback {
      display: none;
    }
    body.embed header,
    body.embed aside {
      display: none;
    }
    body.embed main {
      grid-template-columns: 1fr;
      min-height: 100vh;
      height: 100vh;
    }
    body.embed #viewport {
      min-height: 100vh;
      height: 100vh;
    }
    @media (max-width: 820px) {
      main {
        grid-template-columns: 1fr;
      }
      #viewport {
        min-height: 430px;
      }
      aside {
        border-left: 0;
        border-top: 1px solid #d8dde2;
      }
    }
  </style>
  <script type="importmap">
    {
      "imports": {
        "three": "https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js",
        "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.164.1/examples/jsm/"
      }
    }
  </script>
</head>
<body>
  <script>
    if (new URLSearchParams(window.location.search).has("embed")) {
      document.body.classList.add("embed");
    }
  </script>
  <header>
    <h1>Battery Stand Power Carrier Rev C Compact Front-Cassette Layout</h1>
    <div class="meta">
      <span class="chip">Steel chassis-bolted stand</span>
      <span class="chip">Formed chassis saddle</span>
      <span class="chip">Compact battery tray</span>
      <span class="chip">Front/radiator service cassette</span>
      <span class="chip">Low relay tray</span>
      <span class="chip">Top-front MIDI/cutoff</span>
      <span class="chip">Engine-side keep-clear</span>
      <span class="chip">Cavity-map gate</span>
    </div>
  </header>
  <main>
    <section id="viewport" aria-label="Interactive 3D battery power carrier visualisation">
      <div id="fallback">
        <img src="./battery_power_carrier_mount_rev_a_3d_visualisation.svg" alt="Isometric battery power carrier visualisation">
      </div>
    </section>
    <aside>
      <h2>Assembly Read</h2>
      <dl>
        <div>
          <dt>Load path</dt>
          <dd>The compact battery tray mounts from one formed saddle over the chassis rail through a compact upright bridge.</dd>
        </div>
        <div>
          <dt>Power path</dt>
          <dd>The folded Relay Rev C tray moves low on the front face; MIDI Rev C and the folded cutoff base/guard sit on shallow top-front shelves so the inboard engine/LHD side stays clear.</dd>
        </div>
        <div>
          <dt>Service intent</dt>
          <dd>The stand is removable from the chassis after coated pickup points are finished; final holes stay gated by battery, bonnet, engine/LHD steering-side, radiator/fan, hose, and cable-sweep checks.</dd>
        </div>
      </dl>
    </aside>
  </main>
  <script type="module">
    import * as THREE from "three";
    import { OrbitControls } from "three/addons/controls/OrbitControls.js";

    const mount = document.getElementById("viewport");
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f6f7);

    const baseCameraPosition = new THREE.Vector3(700, 620, 920);
    const baseTarget = new THREE.Vector3(-25, 145, 20);
    const camera = new THREE.PerspectiveCamera(34, 1, 1, 5200);
    camera.position.copy(baseCameraPosition);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, preserveDrawingBuffer: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    mount.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.copy(baseTarget);
    controls.enableDamping = true;
    controls.minDistance = 600;
    controls.maxDistance = 1500;
    controls.maxPolarAngle = Math.PI * 0.48;

    const root = new THREE.Group();
    scene.add(root);

    const materials = {
      plate: new THREE.MeshStandardMaterial({ color: 0xbfc8d1, metalness: 0.35, roughness: 0.38 }),
      plateEdge: new THREE.MeshStandardMaterial({ color: 0x8e9aa5, metalness: 0.25, roughness: 0.45 }),
      steel: new THREE.MeshStandardMaterial({ color: 0x59636c, metalness: 0.45, roughness: 0.5 }),
      chassis: new THREE.MeshStandardMaterial({ color: 0x2b3238, metalness: 0.35, roughness: 0.62 }),
      relay: new THREE.MeshStandardMaterial({ color: 0x202a33, roughness: 0.62 }),
      relayDetail: new THREE.MeshStandardMaterial({ color: 0x41515f, roughness: 0.58 }),
      midiBoard: new THREE.MeshStandardMaterial({ color: 0x1f2930, roughness: 0.7 }),
      fuseRed: new THREE.MeshStandardMaterial({ color: 0xb72e2a, roughness: 0.42 }),
      fuseBlue: new THREE.MeshStandardMaterial({ color: 0x2387d7, roughness: 0.3 }),
      fuseYellow: new THREE.MeshStandardMaterial({ color: 0xdfba21, roughness: 0.3 }),
      battery: new THREE.MeshStandardMaterial({ color: 0x2f3942, roughness: 0.62 }),
      brass: new THREE.MeshStandardMaterial({ color: 0xc4a35a, metalness: 0.4, roughness: 0.36 }),
      silver: new THREE.MeshStandardMaterial({ color: 0xd4d8dc, metalness: 0.35, roughness: 0.32 }),
      cutoff: new THREE.MeshStandardMaterial({ color: 0xd12828, roughness: 0.35 }),
      black: new THREE.MeshStandardMaterial({ color: 0x111820, roughness: 0.55 }),
      cableRed: new THREE.MeshStandardMaterial({ color: 0xc41d1d, roughness: 0.45 }),
      cableBlack: new THREE.MeshStandardMaterial({ color: 0x20262b, roughness: 0.5 }),
      keepout: new THREE.MeshStandardMaterial({ color: 0xb8c2ca, roughness: 0.75, transparent: true, opacity: 0.18 }),
      bendLine: new THREE.MeshStandardMaterial({ color: 0x2f3942, roughness: 0.55 }),
    };
    const edgeMaterial = new THREE.LineBasicMaterial({ color: 0x24313a, transparent: true, opacity: 0.48 });

    function addMeshEdges(mesh, material) {
      if (material === materials.bendLine || material === materials.keepout) {
        return;
      }
      const edges = new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry), edgeMaterial);
      edges.position.copy(mesh.position);
      edges.rotation.copy(mesh.rotation);
      edges.scale.copy(mesh.scale);
      root.add(edges);
    }

    function box(name, x, y, z, w, h, d, material) {
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
      mesh.name = name;
      mesh.position.set(x, y, z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      root.add(mesh);
      addMeshEdges(mesh, material);
      return mesh;
    }

    function cyl(name, x, y, z, radius, depth, material, rotationX = Math.PI / 2) {
      const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, depth, 48), material);
      mesh.name = name;
      mesh.rotation.x = rotationX;
      mesh.position.set(x, y, z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      root.add(mesh);
      addMeshEdges(mesh, material);
      return mesh;
    }

    function cable(name, points, radius, material) {
      const curve = new THREE.CatmullRomCurve3(points.map((p) => new THREE.Vector3(p[0], p[1], p[2])));
      const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, 48, radius, 14, false), material);
      mesh.name = name;
      mesh.castShadow = true;
      root.add(mesh);
      return mesh;
    }

    function singleChassisPickup() {
      box("Visible chassis rail under saddle", 0, -96, 70, 260, 72, 108, materials.chassis);
      box("Formed chassis saddle top cap", 0, -52, 70, 220, 8, 150, materials.steel);
      box("Formed chassis saddle near leg", 0, -96, -8, 220, 76, 8, materials.steel);
      box("Formed chassis saddle far leg", 0, -96, 148, 220, 76, 8, materials.steel);
      box("Compact single chassis upright pedestal", 0, 12, 70, 86, 118, 100, materials.steel);
      box("Compact tray saddle from formed chassis pickup", 0, 58, 70, 200, 22, 170, materials.steel);
      box("Left compact upright side plate 110 x 220", -72, 18, -8, 18, 140, 110, materials.steel);
      box("Right compact upright side plate 110 x 220", -72, 18, 148, 18, 140, 110, materials.steel);
      cyl("Forward saddle through-bolt", -72, -96, 70, 5, 172, materials.brass, Math.PI / 2);
      cyl("Rear saddle through-bolt", 72, -96, 70, 5, 172, materials.brass, Math.PI / 2);
    }
    function relayFuseBoxVertical(name, x, y, z) {
      box(`${name} housing 300 x 197 x 80`, x, y, z - 40, 300, 197, 64, materials.relay);
      box(`${name} raised front rim`, x, y, z - 78, 286, 183, 7, materials.relayDetail);
      box(`${name} relay bay backing`, x - 45, y, z - 84, 128, 176, 6, materials.black);
      box(`${name} blade fuse column backing`, x + 104, y, z - 84, 58, 176, 6, materials.black);
      box(`${name} lower loom boot`, x - 124, y - 82, z - 68, 46, 34, 34, materials.black);
      box(`${name} red output wire bundle`, x + 32, y - 92, z - 70, 92, 16, 26, materials.cableRed);
      const relayRows = [72, 36, 0, -36, -72];
      const fuseMaterials = [materials.fuseBlue, materials.fuseRed, materials.fuseBlue, materials.fuseYellow, materials.fuseYellow];
      for (let row = 0; row < relayRows.length; row += 1) {
        const ry = y + relayRows[row];
        for (const rx of [-70, -10]) {
          box(`${name} relay cube`, x + rx, ry, z - 100, 54, 29, 28, materials.relayDetail);
          box(`${name} relay printed legend`, x + rx, ry + 1, z - 116, 32, 4, 2, materials.silver);
        }
        box(`${name} blade fuse slot`, x + 104, ry, z - 100, 44, 28, 16, materials.black);
        box(`${name} blade fuse cap`, x + 104, ry + 3, z - 117, 34, 12, 7, fuseMaterials[row]);
        box(`${name} exposed fuse terminal pair`, x + 104, ry - 13, z - 117, 32, 5, 4, materials.silver);
      }
      for (const [sx, sy] of [[-124, 72], [-124, -72], [-10, 90], [-10, -90]]) {
        cyl(`${name} brass power stud`, x + sx, y + sy, z - 116, 6, 8, materials.brass, Math.PI / 2);
      }
    }
    function midiHolderVertical(name, x, y, z) {
      box(`${name} black linked base`, x, y, z - 28, 25, 82, 16, materials.black);
      box(`${name} red hinged cover`, x, y, z - 50, 24, 72, 26, materials.fuseRed);
      box(`${name} latch recess upper`, x, y + 23, z - 65, 13, 9, 4, materials.black);
      box(`${name} latch recess lower`, x, y - 23, z - 65, 13, 9, 4, materials.black);
      box(`${name} mounting ear feed side`, x - 17, y - 42, z - 32, 12, 18, 8, materials.black);
      box(`${name} mounting ear branch side`, x + 17, y + 42, z - 32, 12, 18, 8, materials.black);
      cyl(`${name} feed stud`, x, y - 30, z - 68, 4, 10, materials.brass, Math.PI / 2);
      cyl(`${name} branch stud`, x, y + 30, z - 68, 4, 10, materials.brass, Math.PI / 2);
    }
    function midiHolderTop(name, x, y, z) {
      box(`${name} black linked base`, x, y + 24, z, 25, 18, 82, materials.black);
      box(`${name} red hinged cover`, x, y + 44, z, 24, 26, 72, materials.fuseRed);
      box(`${name} latch recess front`, x, y + 59, z - 23, 13, 4, 9, materials.black);
      box(`${name} latch recess rear`, x, y + 59, z + 23, 13, 4, 9, materials.black);
      box(`${name} left mounting ear`, x - 17, y + 18, z - 42, 12, 8, 18, materials.black);
      box(`${name} right mounting ear`, x + 17, y + 18, z + 42, 12, 8, 18, materials.black);
      cyl(`${name} feed stud`, x, y + 62, z - 30, 4, 10, materials.brass, 0);
      cyl(`${name} branch stud`, x, y + 62, z + 30, 4, 10, materials.brass, 0);
    }
    function breakerCutoffVertical(name, x, y, z) {
      box(`${name} 100A waterproof resettable breaker body`, x, y, z - 35, 82, 56, 34, materials.black);
      box(`${name} raised breaker faceplate`, x, y, z - 58, 72, 44, 7, materials.relayDetail);
      box(`${name} red RESET lever`, x - 12, y + 2, z - 66, 46, 10, 7, materials.cutoff);
      box(`${name} red trip button`, x + 28, y - 17, z - 68, 15, 9, 5, materials.cutoff);
      cyl(`${name} input terminal stud`, x - 36, y - 31, z - 68, 5, 12, materials.brass, Math.PI / 2);
      cyl(`${name} output terminal stud`, x + 36, y + 31, z - 68, 5, 12, materials.brass, Math.PI / 2);
      box(`${name} input ring lug`, x - 36, y - 31, z - 75, 26, 18, 4, materials.silver);
      box(`${name} output ring lug`, x + 36, y + 31, z - 75, 26, 18, 4, materials.silver);
    }
    function breakerCutoffTop(name, x, y, z) {
      box(`${name} 100A waterproof resettable breaker body`, x, y + 32, z, 82, 34, 56, materials.black);
      box(`${name} raised breaker faceplate`, x, y + 53, z, 72, 7, 44, materials.relayDetail);
      box(`${name} red RESET lever`, x - 12, y + 61, z + 2, 46, 7, 10, materials.cutoff);
      box(`${name} red trip button`, x + 28, y + 63, z - 17, 15, 5, 9, materials.cutoff);
      cyl(`${name} input terminal stud`, x - 36, y + 64, z - 31, 5, 12, materials.brass, 0);
      cyl(`${name} output terminal stud`, x + 36, y + 64, z + 31, 5, 12, materials.brass, 0);
      box(`${name} input ring lug`, x - 36, y + 58, z - 31, 26, 4, 18, materials.silver);
      box(`${name} output ring lug`, x + 36, y + 58, z + 31, 26, 4, 18, materials.silver);
      box(`${name} red cable boot`, x - 62, y + 42, z - 42, 36, 18, 20, materials.cableRed);
      box(`${name} black cable boot`, x + 62, y + 42, z + 42, 36, 18, 20, materials.black);
    }
    function knownRelayCarrierBase(x, y, z) {
      box("Folded Relay Rev C carrier tray face 320 x 220", x, y, z, 320, 220, 8, materials.plateEdge);
      box("Folded Relay Rev C left return 20 mm", x - 164, y, z - 12, 8, 220, 28, materials.plateEdge);
      box("Folded Relay Rev C right return 20 mm", x + 164, y, z - 12, 8, 220, 28, materials.plateEdge);
      box("Folded Relay Rev C lower return 20 mm", x, y - 112, z - 12, 320, 8, 28, materials.plateEdge);
      box("Folded Relay Rev C upper return 15 mm", x, y + 112, z - 10, 320, 8, 22, materials.plateEdge);
      box("Folded Relay Rev C left bend crease", x - 160, y, z + 5, 3, 220, 4, materials.bendLine);
      box("Folded Relay Rev C right bend crease", x + 160, y, z + 5, 3, 220, 4, materials.bendLine);
      box("Folded Relay Rev C lower bend crease", x, y - 110, z + 5, 320, 3, 4, materials.bendLine);
      box("Folded Relay Rev C upper bend crease", x, y + 110, z + 5, 320, 3, 4, materials.bendLine);
      relayFuseBoxVertical("Relay/fuse box on fabricated base", x, y, z);
      for (const sx of [-135, 0, 135]) {
        cyl("Relay carrier standoff screw", x + sx, y + 90, z - 8, 4, 10, materials.brass, 0);
        cyl("Relay carrier standoff screw", x + sx, y - 90, z - 8, 4, 10, materials.brass, 0);
      }
    }
    function knownMidiBase(x, y, z) {
      box("Known MIDI Rev C mount plate 190 x 150", x, y, z, 190, 150, 8, materials.plateEdge);
      box("Known MIDI insulated subplate 140 x 85", x, y, z - 14, 140, 85, 12, materials.midiBoard);
      for (let idx = 0; idx < 5; idx += 1) {
        midiHolderVertical(`MIDI holder ${idx + 1} on known base`, x - 54 + idx * 27, y, z);
      }
    }
    function knownMidiTopShelf(x, y, z) {
      box("Top-front MIDI Rev C mount plate 190 x 150", x, y, z, 190, 8, 150, materials.plateEdge);
      box("Top-front MIDI insulated subplate 140 x 85", x, y + 14, z, 140, 12, 85, materials.midiBoard);
      for (let idx = 0; idx < 5; idx += 1) {
        midiHolderTop(`Top-front MIDI holder ${idx + 1}`, x - 54 + idx * 27, y, z);
      }
    }
    function cutoffSwitch(name, x, y, z) {
      box(`${name} folded aluminium cutoff base face 170 x 110`, x, y, z, 170, 110, 8, materials.plateEdge);
      box(`${name} cutoff base left 20 mm guard lip`, x - 89, y, z - 12, 8, 110, 28, materials.plateEdge);
      box(`${name} cutoff base right 20 mm guard lip`, x + 89, y, z - 12, 8, 110, 28, materials.plateEdge);
      box(`${name} cutoff base lower 20 mm guard lip`, x, y - 59, z - 12, 170, 8, 28, materials.plateEdge);
      box(`${name} cutoff base upper 20 mm guard lip`, x, y + 59, z - 12, 170, 8, 28, materials.plateEdge);
      box(`${name} cutoff base left bend crease`, x - 85, y, z + 5, 3, 110, 4, materials.bendLine);
      box(`${name} cutoff base right bend crease`, x + 85, y, z + 5, 3, 110, 4, materials.bendLine);
      box(`${name} cutoff base lower bend crease`, x, y - 55, z + 5, 170, 3, 4, materials.bendLine);
      box(`${name} cutoff base upper bend crease`, x, y + 55, z + 5, 170, 3, 4, materials.bendLine);
      breakerCutoffVertical(name, x, y, z);
    }
    function cutoffSwitchTop(name, x, y, z) {
      box(`${name} folded aluminium cutoff base face 170 x 110`, x, y, z, 170, 8, 110, materials.plateEdge);
      box(`${name} cutoff base left 20 mm upstand guard lip`, x - 89, y + 16, z, 8, 24, 110, materials.plateEdge);
      box(`${name} cutoff base right 20 mm upstand guard lip`, x + 89, y + 16, z, 8, 24, 110, materials.plateEdge);
      box(`${name} cutoff base front 20 mm upstand guard lip`, x, y + 16, z - 59, 170, 24, 8, materials.plateEdge);
      box(`${name} cutoff base rear 20 mm upstand guard lip`, x, y + 16, z + 59, 170, 24, 8, materials.plateEdge);
      box(`${name} cutoff base left bend crease`, x - 85, y + 5, z, 3, 4, 110, materials.bendLine);
      box(`${name} cutoff base right bend crease`, x + 85, y + 5, z, 3, 4, 110, materials.bendLine);
      box(`${name} cutoff base front bend crease`, x, y + 5, z - 55, 170, 4, 3, materials.bendLine);
      box(`${name} cutoff base rear bend crease`, x, y + 5, z + 55, 170, 4, 3, materials.bendLine);
      breakerCutoffTop(name, x, y, z);
    }

    singleChassisPickup();
    box("Compact battery stand top tray 315 x 265", -110, 68, 42, 315, 8, 265, materials.plate);
    box("Battery datum 275 x 230 x 190", -120, 167, 32, 275, 190, 230, materials.battery);
    cyl("Battery positive terminal", -24, 270, -34, 9, 14, materials.brass, 0);
    cyl("Battery negative terminal", -210, 270, 98, 9, 14, materials.brass, 0);
    box("Compact battery hold-down crossbar front", -120, 272, -92, 315, 8, 18, materials.plateEdge);
    box("Compact battery hold-down crossbar rear", -120, 272, 156, 315, 8, 18, materials.plateEdge);
    box("Compact front/radiator service cassette spine 325 x 120", -105, 124, 168, 325, 120, 8, materials.plate);
    knownRelayCarrierBase(-105, 154, 176);
    knownMidiTopShelf(-140, 282, 190);
    cutoffSwitchTop("100A resettable breaker cutoff", 70, 282, 212);
    box("Inboard engine/LHD steering-side keep-clear envelope", 142, 150, 70, 16, 260, 270, materials.keepout);
    cable("Battery positive to top-front cutoff", [[-24, 278, -34], [20, 306, 120], [32, 326, 180]], 7, materials.cableRed);
    cable("Cutoff to top-front MIDI common", [[108, 326, 244], [20, 322, 220], [-70, 318, 190]], 6, materials.cableRed);
    cable("Relay feed down front cassette", [[-70, 318, 190], [-102, 245, 180], [-105, 172, 148]], 5, materials.cableRed);
    cable("Fused branch exit along front rail", [[-70, 318, 190], [80, 300, 220], [170, 220, 226]], 5, materials.cableBlack);

    const ambient = new THREE.HemisphereLight(0xffffff, 0x98a1aa, 2.2);
    scene.add(ambient);
    const key = new THREE.DirectionalLight(0xffffff, 2.4);
    key.position.set(260, 420, 300);
    key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    scene.add(key);

    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(900, 680),
      new THREE.ShadowMaterial({ color: 0x000000, opacity: 0.12 })
    );
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -92;
    ground.receiveShadow = true;
    scene.add(ground);

    function resize() {
      const width = mount.clientWidth;
      const height = mount.clientHeight;
      renderer.setSize(width, height, false);
      camera.aspect = width / Math.max(1, height);
      const aspect = width / Math.max(1, height);
      const portraitScale = aspect < 0.9 ? Math.min(2.4, 1.1 / Math.max(aspect, 0.45)) : 1;
      const nextPosition = baseTarget.clone().add(
        baseCameraPosition.clone().sub(baseTarget).multiplyScalar(portraitScale)
      );
      camera.position.copy(nextPosition);
      controls.target.copy(baseTarget);
      controls.minDistance = Math.max(500, 600 * portraitScale);
      controls.maxDistance = Math.max(1500, baseTarget.distanceTo(nextPosition) * 1.35);
      camera.updateProjectionMatrix();
      controls.update();
    }

    function animate() {
      controls.update();
      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    }

    resize();
    window.addEventListener("resize", resize);
    document.body.classList.add("is-three-ready");
    animate();
  </script>
</body>
</html>
"""
    (OUT_DIR / VISUAL_HTML_NAME).write_text(html, encoding="utf-8")


def write_assembled_static_3d_visualisation() -> None:
    elements: list[str] = []
    elements.append('<rect class="background" width="920" height="620" />')
    elements.append(iso_polygon([(-45, 388, -22), (620, 388, -22), (660, 440, -22), (0, 440, -22)], "shadow"))
    elements.extend(iso_prism(170, 178, 260, 100, -78, 54, "chassis-top", "chassis-side", "chassis-front"))
    elements.extend(iso_prism(188, 158, 220, 140, -28, 8, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(188, 150, 220, 10, -74, 48, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(188, 288, 220, 10, -74, 48, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(258, 190, 82, 70, -20, 92, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(220, 184, 24, 104, -24, 112, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(356, 184, 24, 104, -24, 112, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(82, 70, 315, 265, 72, 10, "plate-top", "plate-side", "plate-front"))
    elements.extend(iso_prism(102, 88, 275, 230, 82, 185, "battery-top", "battery-side", "battery-front"))
    elements.extend(iso_prism(94, 100, 315, 18, 274, 8, "hold-top", "hold-side", "hold-front"))
    elements.extend(iso_prism(94, 296, 315, 18, 274, 8, "hold-top", "hold-side", "hold-front"))
    elements.extend(iso_prism(72, 30, 325, 10, 82, 120, "plate-top", "plate-side", "plate-front"))
    elements.extend(iso_prism(74, 38, 320, 8, 68, 220, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(70, 24, 8, 28, 68, 220, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(390, 24, 8, 28, 68, 220, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(74, 24, 320, 28, 60, 8, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(74, 24, 320, 28, 288, 8, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(104, 44, 260, 38, 105, 125, "relay-fuse-top", "relay-fuse-side", "relay-fuse-front"))
    elements.extend(iso_prism(92, 18, 190, 150, 292, 8, "midi-plate-top", "midi-plate-side", "midi-plate-front"))
    elements.extend(iso_prism(117, 44, 140, 85, 306, 10, "midi-board-top", "midi-board-side", "midi-board-front"))
    for idx in range(5):
        elements.extend(iso_prism(126 + idx * 24, 70, 18, 54, 322, 16, "fuse-top", "fuse-side", "fuse-front"))
    elements.extend(iso_prism(290, 18, 110, 170, 292, 8, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(286, 18, 8, 170, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(400, 18, 8, 170, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(290, 14, 110, 8, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(290, 188, 110, 8, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(420, 72, 18, 230, 78, 225, "keepout-top", "keepout-side", "keepout-front"))
    elements.extend(iso_prism(304, 74, 82, 56, 314, 28, "breaker-body-top", "breaker-body-side", "breaker-body-front"))
    elements.extend(iso_prism(309, 80, 72, 44, 342, 6, "breaker-face-top", "breaker-face-side", "breaker-face-front"))
    elements.extend(iso_prism(315, 96, 46, 10, 350, 6, "breaker-lever-top", "breaker-lever-side", "breaker-lever-front"))
    for point in [(318, 86, 350), (372, 110, 350)]:
        x, y = iso_point(*point)
        elements.append(f'<circle class="breaker-terminal" cx="{x:.1f}" cy="{y:.1f}" r="5" />')
    elements.append(iso_polyline([(275, 108, 280), (345, 98, 334), (318, 86, 350)], "positive-cable"))
    elements.append(iso_polyline([(372, 110, 350), (220, 86, 335), (180, 64, 322)], "relay-feed"))
    elements.append(iso_polyline([(180, 64, 322), (210, 42, 210), (170, 44, 160)], "branch-cable"))
    for point in [(214, 156, -50), (382, 156, -50), (214, 296, -50), (382, 296, -50)]:
        x, y = iso_point(*point)
        elements.append(f'<circle class="slot-marker" cx="{x:.1f}" cy="{y:.1f}" r="4" />')
    for text, x, y in (
        ("Attached compact battery stand assembly", 82, 84),
        ("Battery bolted down on compact tray", 212, 214),
        ("Formed chassis saddle", 132, 508),
        ("Single upright bridge", 158, 364),
        ("Front service cassette", 548, 252),
        ("Engine/LHD side kept clear", 548, 430),
    ):
        elements.append(f'<text class="label" x="{x}" y="{y}">{text}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="620" viewBox="0 0 920 620" role="img" aria-labelledby="title desc">
  <title id="title">Battery stand power carrier Rev C compact front-cassette assembled 3D visualisation</title>
  <desc id="desc">Attached assembly view of the compact steel battery stand with a formed saddle over the chassis rail, compact tray, hold-down crossbar, full-height battery, folded Relay Rev C tray low on the front face, MIDI Rev C on a top-front shelf, folded cutoff base/guard with upward lips at the top-front accessible corner, and the inboard engine/LHD side kept clear.</desc>
  <style>
    .background {{ fill: #f6f7f8; }}
    .shadow {{ fill: #d9dde2; opacity: 0.55; }}
    .plate-top {{ fill: #cfd6dc; stroke: #4f5962; stroke-width: 1.4; }}
    .plate-side {{ fill: #9ca8b2; stroke: #4f5962; stroke-width: 1.2; }}
    .plate-front {{ fill: #b5bec7; stroke: #4f5962; stroke-width: 1.2; }}
    .tab-top {{ fill: #7f8992; stroke: #343b42; stroke-width: 1.2; }}
    .tab-side {{ fill: #515b64; stroke: #343b42; stroke-width: 1.1; }}
    .tab-front {{ fill: #66717a; stroke: #343b42; stroke-width: 1.1; }}
    .chassis-top {{ fill: #3b434a; stroke: #20262b; stroke-width: 1.2; }}
    .chassis-side {{ fill: #252c32; stroke: #20262b; stroke-width: 1.1; }}
    .chassis-front {{ fill: #303840; stroke: #20262b; stroke-width: 1.1; }}
    .battery-top {{ fill: #2f3942; stroke: #111820; stroke-width: 1.4; }}
    .battery-side {{ fill: #1d252c; stroke: #111820; stroke-width: 1.2; }}
    .battery-front {{ fill: #3d4852; stroke: #111820; stroke-width: 1.2; }}
    .hold-top {{ fill: #cfd6dc; stroke: #4f5962; stroke-width: 1.1; }}
    .hold-side {{ fill: #98a4ae; stroke: #4f5962; stroke-width: 0.9; }}
    .hold-front {{ fill: #b5bec7; stroke: #4f5962; stroke-width: 0.9; }}
    .relay-tray-top {{ fill: #aeb8c1; stroke: #4f5962; stroke-width: 1.2; }}
    .relay-tray-side {{ fill: #818d97; stroke: #4f5962; stroke-width: 1; }}
    .relay-tray-front {{ fill: #98a4ae; stroke: #4f5962; stroke-width: 1; }}
    .midi-plate-top {{ fill: #aeb8c1; stroke: #4f5962; stroke-width: 1.2; }}
    .midi-plate-side {{ fill: #818d97; stroke: #4f5962; stroke-width: 1; }}
    .midi-plate-front {{ fill: #98a4ae; stroke: #4f5962; stroke-width: 1; }}
    .midi-board-top {{ fill: #1f2930; stroke: #14191d; stroke-width: 1; }}
    .midi-board-side {{ fill: #161d22; stroke: #14191d; stroke-width: 0.9; }}
    .midi-board-front {{ fill: #2b363e; stroke: #14191d; stroke-width: 0.9; }}
    .fuse-top {{ fill: #b7302a; stroke: #6e1714; stroke-width: 0.8; }}
    .fuse-side {{ fill: #84201b; stroke: #6e1714; stroke-width: 0.7; }}
    .fuse-front {{ fill: #d14a43; stroke: #6e1714; stroke-width: 0.7; }}
    .cutoff-base-top {{ fill: #aeb8c1; stroke: #4f5962; stroke-width: 1.2; }}
    .cutoff-base-side {{ fill: #818d97; stroke: #4f5962; stroke-width: 1; }}
    .cutoff-base-front {{ fill: #98a4ae; stroke: #4f5962; stroke-width: 1; }}
    .keepout-top {{ fill: #d7dde2; stroke: #85909a; stroke-width: 1; stroke-dasharray: 6 4; opacity: 0.24; }}
    .keepout-side {{ fill: #c2cbd2; stroke: #85909a; stroke-width: 1; stroke-dasharray: 6 4; opacity: 0.18; }}
    .keepout-front {{ fill: #eef2f5; stroke: #85909a; stroke-width: 1; stroke-dasharray: 6 4; opacity: 0.14; }}
    .breaker-body-top {{ fill: #111820; stroke: #05080a; stroke-width: 1.2; }}
    .breaker-body-side {{ fill: #080c10; stroke: #05080a; stroke-width: 1; }}
    .breaker-body-front {{ fill: #202a33; stroke: #05080a; stroke-width: 1; }}
    .breaker-face-top {{ fill: #41515f; stroke: #1f2830; stroke-width: 1; }}
    .breaker-face-side {{ fill: #26323d; stroke: #1f2830; stroke-width: 0.9; }}
    .breaker-face-front {{ fill: #33424d; stroke: #1f2830; stroke-width: 0.9; }}
    .breaker-lever-top {{ fill: #d12828; stroke: #871313; stroke-width: 1; }}
    .breaker-lever-side {{ fill: #8f1717; stroke: #871313; stroke-width: 0.9; }}
    .breaker-lever-front {{ fill: #c41d1d; stroke: #871313; stroke-width: 0.9; }}
    .breaker-terminal {{ fill: #c4a35a; stroke: #6f5d2f; stroke-width: 1.1; }}
    .positive-cable {{ fill: none; stroke: #c41d1d; stroke-width: 8; stroke-linejoin: round; stroke-linecap: round; }}
    .relay-feed {{ fill: none; stroke: #a51515; stroke-width: 6; stroke-linejoin: round; stroke-linecap: round; }}
    .branch-cable {{ fill: none; stroke: #242b30; stroke-width: 6; stroke-linejoin: round; stroke-linecap: round; }}
    .slot-marker {{ fill: #eef3f7; stroke: #4f5962; stroke-width: 1.2; }}
    .label {{ font: 600 18px Arial, sans-serif; fill: #24313a; }}
  </style>
  {''.join(elements)}
</svg>
"""
    (OUT_DIR / ASSEMBLED_VISUAL_SVG_NAME).write_text(svg, encoding="utf-8")


def write_assembled_interactive_3d_visualisation() -> None:
    html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>J40 Battery Stand Power Carrier Rev C Compact Front-Cassette - Assembled 3D Visualisation</title>
  <link rel="icon" href="data:,">
  <style>
    :root { color-scheme: light; font-family: Arial, Helvetica, sans-serif; background: #f5f6f7; color: #1d252c; }
    body { margin: 0; min-height: 100vh; display: grid; grid-template-rows: auto 1fr; }
    body.embed { grid-template-rows: 1fr; }
    header { padding: 16px 22px 10px; background: #ffffff; border-bottom: 1px solid #d8dde2; }
    h1 { margin: 0; font-size: clamp(20px, 3vw, 30px); letter-spacing: 0; }
    .meta { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
    .chip { border: 1px solid #c8d0d8; border-radius: 999px; padding: 5px 9px; background: #f8fafb; font-size: 13px; }
    main { display: grid; grid-template-columns: minmax(0, 1fr) 300px; min-height: 0; }
    #viewport { position: relative; min-height: 560px; overflow: hidden; }
    canvas { display: block; width: 100%; height: 100%; }
    aside { border-left: 1px solid #d8dde2; background: #ffffff; padding: 18px; }
    h2 { margin: 0 0 12px; font-size: 18px; letter-spacing: 0; }
    dl { margin: 0; display: grid; gap: 12px; }
    dt { font-weight: 700; }
    dd { margin: 3px 0 0; color: #54616c; font-size: 14px; line-height: 1.45; }
    #fallback { position: absolute; inset: 0; display: grid; place-items: center; padding: 20px; background: #f5f6f7; }
    #fallback img { width: min(94vw, 920px); max-height: 82vh; object-fit: contain; }
    body.is-three-ready #fallback { display: none; }
    body.embed header,
    body.embed aside { display: none; }
    body.embed main { grid-template-columns: 1fr; min-height: 100vh; height: 100vh; }
    body.embed #viewport { min-height: 100vh; height: 100vh; }
    @media (max-width: 820px) { main { grid-template-columns: 1fr; } #viewport { min-height: 430px; } aside { border-left: 0; border-top: 1px solid #d8dde2; } }
  </style>
  <script type="importmap">
    {"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.164.1/examples/jsm/"}}
  </script>
</head>
<body>
  <script>
    if (new URLSearchParams(window.location.search).has("embed")) {
      document.body.classList.add("embed");
    }
  </script>
  <header>
    <h1>Assembled Battery Stand Power Carrier Rev C Compact Front-Cassette Layout</h1>
    <div class="meta">
      <span class="chip">Attached assembly</span>
      <span class="chip">Formed chassis saddle</span>
      <span class="chip">Compact battery tray</span>
      <span class="chip">Front/radiator service cassette</span>
      <span class="chip">Low relay tray</span>
      <span class="chip">Top-front MIDI/cutoff</span>
      <span class="chip">Engine-side keep-clear</span>
      <span class="chip">Cavity-map hold</span>
    </div>
  </header>
  <main>
    <section id="viewport" aria-label="Interactive assembled 3D battery stand visualisation">
      <div id="fallback">
        <img src="./battery_power_carrier_mount_rev_a_assembled_3d_visualisation.svg" alt="Assembled battery stand power carrier visualisation">
      </div>
    </section>
    <aside>
      <h2>Assembly Read</h2>
      <dl>
        <div><dt>Load path</dt><dd>One formed saddle over the chassis rail and an upright bridge carry the compact steel battery tray and front-cassette shelf/tab pickups.</dd></div>
        <div><dt>Integrated equipment</dt><dd>The full-height battery, folded Relay Rev C tray, MIDI Rev C open plate, and folded cutoff base/guard are shown attached as a compact front-cassette layout.</dd></div>
        <div><dt>Release hold</dt><dd>Final hole centres, holder positions, and cable paths still need battery-installed LHD mock-up photos before cutting final metal, with the inboard engine side treated as a service/clearance envelope.</dd></div>
      </dl>
    </aside>
  </main>
  <script type="module">
    import * as THREE from "three";
    import { OrbitControls } from "three/addons/controls/OrbitControls.js";

    const mount = document.getElementById("viewport");
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f6f7);
    const baseCameraPosition = new THREE.Vector3(700, 620, 920);
    const baseTarget = new THREE.Vector3(-25, 145, 20);
    const camera = new THREE.PerspectiveCamera(34, 1, 1, 5200);
    camera.position.copy(baseCameraPosition);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, preserveDrawingBuffer: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    mount.appendChild(renderer.domElement);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.copy(baseTarget);
    controls.enableDamping = true;
    controls.minDistance = 600;
    controls.maxDistance = 1500;
    controls.maxPolarAngle = Math.PI * 0.5;
    const root = new THREE.Group();
    scene.add(root);
    const materials = {
      plate: new THREE.MeshStandardMaterial({ color: 0xbfc8d1, metalness: 0.35, roughness: 0.38 }),
      plateEdge: new THREE.MeshStandardMaterial({ color: 0x8e9aa5, metalness: 0.25, roughness: 0.45 }),
      steel: new THREE.MeshStandardMaterial({ color: 0x59636c, metalness: 0.45, roughness: 0.5 }),
      relay: new THREE.MeshStandardMaterial({ color: 0x202a33, roughness: 0.62 }),
      relayDetail: new THREE.MeshStandardMaterial({ color: 0x41515f, roughness: 0.58 }),
      midiBoard: new THREE.MeshStandardMaterial({ color: 0x1f2930, roughness: 0.7 }),
      fuseRed: new THREE.MeshStandardMaterial({ color: 0xb72e2a, roughness: 0.42 }),
      fuseBlue: new THREE.MeshStandardMaterial({ color: 0x2387d7, roughness: 0.3 }),
      fuseYellow: new THREE.MeshStandardMaterial({ color: 0xdfba21, roughness: 0.3 }),
      battery: new THREE.MeshStandardMaterial({ color: 0x2f3942, roughness: 0.62 }),
      brass: new THREE.MeshStandardMaterial({ color: 0xc4a35a, metalness: 0.4, roughness: 0.36 }),
      silver: new THREE.MeshStandardMaterial({ color: 0xd4d8dc, metalness: 0.35, roughness: 0.32 }),
      cutoff: new THREE.MeshStandardMaterial({ color: 0xd12828, roughness: 0.35 }),
      black: new THREE.MeshStandardMaterial({ color: 0x111820, roughness: 0.55 }),
      cableRed: new THREE.MeshStandardMaterial({ color: 0xc41d1d, roughness: 0.45 }),
      cableBlack: new THREE.MeshStandardMaterial({ color: 0x20262b, roughness: 0.5 }),
      chassis: new THREE.MeshStandardMaterial({ color: 0x2b3238, metalness: 0.35, roughness: 0.62 }),
      keepout: new THREE.MeshStandardMaterial({ color: 0xb8c2ca, roughness: 0.75, transparent: true, opacity: 0.18 }),
      bendLine: new THREE.MeshStandardMaterial({ color: 0x2f3942, roughness: 0.55 }),
    };
    const edgeMaterial = new THREE.LineBasicMaterial({ color: 0x24313a, transparent: true, opacity: 0.48 });
    function addMeshEdges(mesh, material) {
      if (material === materials.bendLine || material === materials.keepout) {
        return;
      }
      const edges = new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry), edgeMaterial);
      edges.position.copy(mesh.position);
      edges.rotation.copy(mesh.rotation);
      edges.scale.copy(mesh.scale);
      root.add(edges);
    }
    function box(name, x, y, z, w, h, d, material) {
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
      mesh.name = name;
      mesh.position.set(x, y, z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      root.add(mesh);
      addMeshEdges(mesh, material);
      return mesh;
    }
    function cyl(name, x, y, z, radius, depth, material, rotationX = Math.PI / 2) {
      const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, depth, 48), material);
      mesh.name = name;
      mesh.rotation.x = rotationX;
      mesh.position.set(x, y, z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      root.add(mesh);
      addMeshEdges(mesh, material);
      return mesh;
    }
    function cable(name, points, radius, material) {
      const curve = new THREE.CatmullRomCurve3(points.map((p) => new THREE.Vector3(p[0], p[1], p[2])));
      const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, 48, radius, 14, false), material);
      mesh.name = name;
      mesh.castShadow = true;
      root.add(mesh);
      return mesh;
    }
    function singleChassisPickup() {
      box("Assembled visible chassis rail under saddle", 0, -96, 70, 260, 72, 108, materials.chassis);
      box("Assembled formed chassis saddle top cap", 0, -52, 70, 220, 8, 150, materials.steel);
      box("Assembled formed chassis saddle near leg", 0, -96, -8, 220, 76, 8, materials.steel);
      box("Assembled formed chassis saddle far leg", 0, -96, 148, 220, 76, 8, materials.steel);
      box("Assembled compact single chassis upright pedestal", 0, 12, 70, 86, 118, 100, materials.steel);
      box("Assembled compact tray saddle from formed chassis pickup", 0, 58, 70, 200, 22, 170, materials.steel);
      box("Assembled left compact upright side plate 110 x 220", -72, 18, -8, 18, 140, 110, materials.steel);
      box("Assembled right compact upright side plate 110 x 220", -72, 18, 148, 18, 140, 110, materials.steel);
      cyl("Assembled forward saddle through-bolt", -72, -96, 70, 5, 172, materials.brass, Math.PI / 2);
      cyl("Assembled rear saddle through-bolt", 72, -96, 70, 5, 172, materials.brass, Math.PI / 2);
    }
    function relayFuseBoxVertical(name, x, y, z) {
      box(`${name} housing 300 x 197 x 80`, x, y, z - 40, 300, 197, 64, materials.relay);
      box(`${name} raised front rim`, x, y, z - 78, 286, 183, 7, materials.relayDetail);
      box(`${name} relay bay backing`, x - 45, y, z - 84, 128, 176, 6, materials.black);
      box(`${name} blade fuse column backing`, x + 104, y, z - 84, 58, 176, 6, materials.black);
      box(`${name} lower loom boot`, x - 124, y - 82, z - 68, 46, 34, 34, materials.black);
      box(`${name} red output wire bundle`, x + 32, y - 92, z - 70, 92, 16, 26, materials.cableRed);
      const relayRows = [72, 36, 0, -36, -72];
      const fuseMaterials = [materials.fuseBlue, materials.fuseRed, materials.fuseBlue, materials.fuseYellow, materials.fuseYellow];
      for (let row = 0; row < relayRows.length; row += 1) {
        const ry = y + relayRows[row];
        for (const rx of [-70, -10]) {
          box(`${name} relay cube`, x + rx, ry, z - 100, 54, 29, 28, materials.relayDetail);
          box(`${name} relay printed legend`, x + rx, ry + 1, z - 116, 32, 4, 2, materials.silver);
        }
        box(`${name} blade fuse slot`, x + 104, ry, z - 100, 44, 28, 16, materials.black);
        box(`${name} blade fuse cap`, x + 104, ry + 3, z - 117, 34, 12, 7, fuseMaterials[row]);
        box(`${name} exposed fuse terminal pair`, x + 104, ry - 13, z - 117, 32, 5, 4, materials.silver);
      }
      for (const [sx, sy] of [[-124, 72], [-124, -72], [-10, 90], [-10, -90]]) {
        cyl(`${name} brass power stud`, x + sx, y + sy, z - 116, 6, 8, materials.brass, Math.PI / 2);
      }
    }
    function midiHolderVertical(name, x, y, z) {
      box(`${name} black linked base`, x, y, z - 28, 25, 82, 16, materials.black);
      box(`${name} red hinged cover`, x, y, z - 50, 24, 72, 26, materials.fuseRed);
      box(`${name} latch recess upper`, x, y + 23, z - 65, 13, 9, 4, materials.black);
      box(`${name} latch recess lower`, x, y - 23, z - 65, 13, 9, 4, materials.black);
      box(`${name} mounting ear feed side`, x - 17, y - 42, z - 32, 12, 18, 8, materials.black);
      box(`${name} mounting ear branch side`, x + 17, y + 42, z - 32, 12, 18, 8, materials.black);
      cyl(`${name} feed stud`, x, y - 30, z - 68, 4, 10, materials.brass, Math.PI / 2);
      cyl(`${name} branch stud`, x, y + 30, z - 68, 4, 10, materials.brass, Math.PI / 2);
    }
    function midiHolderTop(name, x, y, z) {
      box(`${name} black linked base`, x, y + 24, z, 25, 18, 82, materials.black);
      box(`${name} red hinged cover`, x, y + 44, z, 24, 26, 72, materials.fuseRed);
      box(`${name} latch recess front`, x, y + 59, z - 23, 13, 4, 9, materials.black);
      box(`${name} latch recess rear`, x, y + 59, z + 23, 13, 4, 9, materials.black);
      box(`${name} left mounting ear`, x - 17, y + 18, z - 42, 12, 8, 18, materials.black);
      box(`${name} right mounting ear`, x + 17, y + 18, z + 42, 12, 8, 18, materials.black);
      cyl(`${name} feed stud`, x, y + 62, z - 30, 4, 10, materials.brass, 0);
      cyl(`${name} branch stud`, x, y + 62, z + 30, 4, 10, materials.brass, 0);
    }
    function breakerCutoffVertical(name, x, y, z) {
      box(`${name} 100A waterproof resettable breaker body`, x, y, z - 35, 82, 56, 34, materials.black);
      box(`${name} raised breaker faceplate`, x, y, z - 58, 72, 44, 7, materials.relayDetail);
      box(`${name} red RESET lever`, x - 12, y + 2, z - 66, 46, 10, 7, materials.cutoff);
      box(`${name} red trip button`, x + 28, y - 17, z - 68, 15, 9, 5, materials.cutoff);
      cyl(`${name} input terminal stud`, x - 36, y - 31, z - 68, 5, 12, materials.brass, Math.PI / 2);
      cyl(`${name} output terminal stud`, x + 36, y + 31, z - 68, 5, 12, materials.brass, Math.PI / 2);
      box(`${name} input ring lug`, x - 36, y - 31, z - 75, 26, 18, 4, materials.silver);
      box(`${name} output ring lug`, x + 36, y + 31, z - 75, 26, 18, 4, materials.silver);
    }
    function breakerCutoffTop(name, x, y, z) {
      box(`${name} 100A waterproof resettable breaker body`, x, y + 32, z, 82, 34, 56, materials.black);
      box(`${name} raised breaker faceplate`, x, y + 53, z, 72, 7, 44, materials.relayDetail);
      box(`${name} red RESET lever`, x - 12, y + 61, z + 2, 46, 7, 10, materials.cutoff);
      box(`${name} red trip button`, x + 28, y + 63, z - 17, 15, 5, 9, materials.cutoff);
      cyl(`${name} input terminal stud`, x - 36, y + 64, z - 31, 5, 12, materials.brass, 0);
      cyl(`${name} output terminal stud`, x + 36, y + 64, z + 31, 5, 12, materials.brass, 0);
      box(`${name} input ring lug`, x - 36, y + 58, z - 31, 26, 4, 18, materials.silver);
      box(`${name} output ring lug`, x + 36, y + 58, z + 31, 26, 4, 18, materials.silver);
      box(`${name} red cable boot`, x - 62, y + 42, z - 42, 36, 18, 20, materials.cableRed);
      box(`${name} black cable boot`, x + 62, y + 42, z + 42, 36, 18, 20, materials.black);
    }
    function knownRelayCarrierBase(x, y, z) {
      box("Folded Relay Rev C carrier tray face 320 x 220", x, y, z, 320, 220, 8, materials.plateEdge);
      box("Folded Relay Rev C left return 20 mm", x - 164, y, z - 12, 8, 220, 28, materials.plateEdge);
      box("Folded Relay Rev C right return 20 mm", x + 164, y, z - 12, 8, 220, 28, materials.plateEdge);
      box("Folded Relay Rev C lower return 20 mm", x, y - 112, z - 12, 320, 8, 28, materials.plateEdge);
      box("Folded Relay Rev C upper return 15 mm", x, y + 112, z - 10, 320, 8, 22, materials.plateEdge);
      box("Folded Relay Rev C left bend crease", x - 160, y, z + 5, 3, 220, 4, materials.bendLine);
      box("Folded Relay Rev C right bend crease", x + 160, y, z + 5, 3, 220, 4, materials.bendLine);
      box("Folded Relay Rev C lower bend crease", x, y - 110, z + 5, 320, 3, 4, materials.bendLine);
      box("Folded Relay Rev C upper bend crease", x, y + 110, z + 5, 320, 3, 4, materials.bendLine);
      relayFuseBoxVertical("Relay/fuse box on fabricated base", x, y, z);
      for (const sx of [-135, 0, 135]) {
        cyl("Relay carrier standoff screw", x + sx, y + 90, z - 8, 4, 10, materials.brass, 0);
        cyl("Relay carrier standoff screw", x + sx, y - 90, z - 8, 4, 10, materials.brass, 0);
      }
    }
    function knownMidiBase(x, y, z) {
      box("Known MIDI Rev C mount plate 190 x 150", x, y, z, 190, 150, 8, materials.plateEdge);
      box("Known MIDI insulated subplate 140 x 85", x, y, z - 14, 140, 85, 12, materials.midiBoard);
      for (let idx = 0; idx < 5; idx += 1) {
        midiHolderVertical(`MIDI holder ${idx + 1} on known base`, x - 54 + idx * 27, y, z);
      }
    }
    function knownMidiTopShelf(x, y, z) {
      box("Top-front MIDI Rev C mount plate 190 x 150", x, y, z, 190, 8, 150, materials.plateEdge);
      box("Top-front MIDI insulated subplate 140 x 85", x, y + 14, z, 140, 12, 85, materials.midiBoard);
      for (let idx = 0; idx < 5; idx += 1) {
        midiHolderTop(`Top-front MIDI holder ${idx + 1}`, x - 54 + idx * 27, y, z);
      }
    }
    function cutoffSwitch(name, x, y, z) {
      box(`${name} folded aluminium cutoff base face 170 x 110`, x, y, z, 170, 110, 8, materials.plateEdge);
      box(`${name} cutoff base left 20 mm guard lip`, x - 89, y, z - 12, 8, 110, 28, materials.plateEdge);
      box(`${name} cutoff base right 20 mm guard lip`, x + 89, y, z - 12, 8, 110, 28, materials.plateEdge);
      box(`${name} cutoff base lower 20 mm guard lip`, x, y - 59, z - 12, 170, 8, 28, materials.plateEdge);
      box(`${name} cutoff base upper 20 mm guard lip`, x, y + 59, z - 12, 170, 8, 28, materials.plateEdge);
      box(`${name} cutoff base left bend crease`, x - 85, y, z + 5, 3, 110, 4, materials.bendLine);
      box(`${name} cutoff base right bend crease`, x + 85, y, z + 5, 3, 110, 4, materials.bendLine);
      box(`${name} cutoff base lower bend crease`, x, y - 55, z + 5, 170, 3, 4, materials.bendLine);
      box(`${name} cutoff base upper bend crease`, x, y + 55, z + 5, 170, 3, 4, materials.bendLine);
      breakerCutoffVertical(name, x, y, z);
    }
    function cutoffSwitchTop(name, x, y, z) {
      box(`${name} folded aluminium cutoff base face 170 x 110`, x, y, z, 170, 8, 110, materials.plateEdge);
      box(`${name} cutoff base left 20 mm upstand guard lip`, x - 89, y + 16, z, 8, 24, 110, materials.plateEdge);
      box(`${name} cutoff base right 20 mm upstand guard lip`, x + 89, y + 16, z, 8, 24, 110, materials.plateEdge);
      box(`${name} cutoff base front 20 mm upstand guard lip`, x, y + 16, z - 59, 170, 24, 8, materials.plateEdge);
      box(`${name} cutoff base rear 20 mm upstand guard lip`, x, y + 16, z + 59, 170, 24, 8, materials.plateEdge);
      box(`${name} cutoff base left bend crease`, x - 85, y + 5, z, 3, 4, 110, materials.bendLine);
      box(`${name} cutoff base right bend crease`, x + 85, y + 5, z, 3, 4, 110, materials.bendLine);
      box(`${name} cutoff base front bend crease`, x, y + 5, z - 55, 170, 4, 3, materials.bendLine);
      box(`${name} cutoff base rear bend crease`, x, y + 5, z + 55, 170, 4, 3, materials.bendLine);
      breakerCutoffTop(name, x, y, z);
    }

    singleChassisPickup();
    box("Assembled compact battery stand top tray 315 x 265", -110, 68, 42, 315, 8, 265, materials.plate);
    box("Full-height battery attached on compact stand", -120, 167, 32, 275, 190, 230, materials.battery);
    cyl("Battery positive terminal", -24, 270, -34, 9, 14, materials.brass, 0);
    cyl("Battery negative terminal", -210, 270, 98, 9, 14, materials.brass, 0);
    box("Compact battery hold-down crossbar front", -120, 272, -92, 315, 8, 18, materials.plateEdge);
    box("Compact battery hold-down crossbar rear", -120, 272, 156, 315, 8, 18, materials.plateEdge);
    for (const x of [-250, 10]) {
      cyl("Front hold-down rod to tray", x, 172, -88, 4, 196, materials.brass, 0);
      cyl("Rear hold-down rod to tray", x, 172, 152, 4, 196, materials.brass, 0);
    }
    box("Compact front/radiator service cassette spine 325 x 120", -105, 124, 168, 325, 120, 8, materials.plate);
    knownRelayCarrierBase(-105, 154, 176);
    knownMidiTopShelf(-140, 282, 190);
    cutoffSwitchTop("100A resettable breaker cutoff", 70, 282, 212);
    box("Inboard engine/LHD steering-side keep-clear envelope", 142, 150, 70, 16, 260, 270, materials.keepout);
    cable("Battery positive to top-front cutoff", [[-24, 278, -34], [20, 306, 120], [32, 326, 180]], 7, materials.cableRed);
    cable("Cutoff to top-front MIDI common", [[108, 326, 244], [20, 322, 220], [-70, 318, 190]], 6, materials.cableRed);
    cable("Relay feed down front cassette", [[-70, 318, 190], [-102, 245, 180], [-105, 172, 148]], 5, materials.cableRed);
    cable("Fused branch exit along front rail", [[-70, 318, 190], [80, 300, 220], [170, 220, 226]], 5, materials.cableBlack);

    scene.add(new THREE.HemisphereLight(0xffffff, 0x98a1aa, 2.2));
    const key = new THREE.DirectionalLight(0xffffff, 2.4);
    key.position.set(260, 420, 300);
    key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    scene.add(key);
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(900, 680), new THREE.ShadowMaterial({ color: 0x000000, opacity: 0.12 }));
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -92;
    ground.receiveShadow = true;
    scene.add(ground);
    function resize() {
      const width = mount.clientWidth;
      const height = mount.clientHeight;
      renderer.setSize(width, height, false);
      camera.aspect = width / Math.max(1, height);
      const aspect = width / Math.max(1, height);
      const portraitScale = aspect < 0.9 ? Math.min(2.4, 1.1 / Math.max(aspect, 0.45)) : 1;
      const nextPosition = baseTarget.clone().add(
        baseCameraPosition.clone().sub(baseTarget).multiplyScalar(portraitScale)
      );
      camera.position.copy(nextPosition);
      controls.target.copy(baseTarget);
      controls.minDistance = Math.max(500, 600 * portraitScale);
      controls.maxDistance = Math.max(1500, baseTarget.distanceTo(nextPosition) * 1.35);
      camera.updateProjectionMatrix();
      controls.update();
    }
    function animate() {
      controls.update();
      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    }
    resize();
    window.addEventListener("resize", resize);
    document.body.classList.add("is-three-ready");
    animate();
  </script>
</body>
</html>
"""
    (OUT_DIR / ASSEMBLED_VISUAL_HTML_NAME).write_text(html, encoding="utf-8")


def write_readme() -> None:
    text = """# J40 Battery Stand Power Carrier Pack - Rev C Compact Front-Cassette Update

This package changes the battery-side plan into a compact steel chassis-bolted stand with a front/radiator-side service cassette. It supports the battery first, keeps the inboard engine/LHD side clear, and uses the already-fabricated electrical holders without spreading them around the battery bay.

## Design Intent

- Mount the battery stand from the one known chassis pickup location using a compact formed saddle over the chassis rail plus an upright bridge.
- Support the battery on a compact `315 x 265 mm` tray around the current `275 x 230 mm` battery datum.
- Put Relay Rev C low on the front/radiator-side cassette face: `320 x 220 mm` finished folded tray, `360 x 255 mm` flat pattern, `20 mm` side/bottom returns, and `15 mm` top return.
- Put MIDI Rev C on a shallow top-front shelf using the known open `190 x 150 mm` aluminium plate plus `140 x 85 mm` insulating subplate.
- Put the 100A breaker/cutoff on the top/front accessible corner on a folded aluminium base/guard: `210 x 150 mm` flat pattern, `170 x 110 mm` finished face, and `20 mm` lips bent upward toward the breaker/terminal side.
- Treat the inboard engine/LHD steering side as a keep-clear/service envelope except for protected cable clips and pass-through routing.
- Default to this front-cassette split layout. Do not make a one-piece side carrier unless the filled cavity map proves it is smaller, clear, serviceable, and not in the engine-side envelope.

## Image-Based Chassis Pickup Estimate

The May 14 no-battery bay photo shows the existing battery pocket sitting well above the chassis rail and slightly wing-side/outboard from the visible chassis pickup line. Use these only as first cardboard/wood mock-up targets:

- Target tray support plane: keep the compact tray in the existing battery pocket plane, about `170-190 mm` above the top of the chassis rail. Use `180 mm` as the first mock-up rise from chassis top to tray underside.
- Vertical adjustment allowance: build the upright bridge with slotted/stepped adjustment from `150-210 mm` chassis-top-to-tray-underside so the tray can be lowered if bonnet/terminal clearance is tight or raised if the relay tray/cable exit needs more space.
- Sideways adjustment allowance: set the tray centre about `120 mm` wing-side/outboard from the chassis pickup centreline, with `90-150 mm` usable side adjustment. This keeps the battery in the original pocket rather than moving it engine-side.
- Chassis saddle allowance: mock the chassis fixing as a 4 mm mild-steel saddle with a top cap over the rail and two down-legs, not a flat plate beside the rail. Use a nominal `220 x 230 mm` flat pattern (`70 mm` near leg, measured rail-top cap nominal `90 mm`, `70 mm` far leg) until the actual rail width is measured.
- Battery/electrical package hold: mock up the full `275 x 230 x 190 mm` battery block plus hold-down, then add the front cassette cards. Do not final-drill the pickup or upright until the battery top, bonnet, fan/radiator, steering/hose, and cable-lug sweeps all pass.

## Parts In This Package

1. `battery_stand_compact_top_tray_rev_b` - 3 mm mild-steel compact battery tray/deck with clamp and cable-clip zones.
2. `battery_stand_compact_single_chassis_pickup_rev_b` - 4 mm mild-steel formed chassis saddle for the one chassis pickup location.
3. `battery_stand_compact_single_mount_upright_rev_b` - 4 mm mild-steel upright bridge side plate; make a mirrored pair if the mock-up needs side-to-side stiffness.
4. `battery_stand_compact_hold_down_crossbar_rev_b` - compact battery hold-down crossbar template.
5. `battery_power_compact_front_service_rail_rev_b` - 3 mm mild-steel compact `325 x 120 mm` front/radiator-side service cassette spine for the relay tray and top-front MIDI/cutoff shelf tabs.
6. `battery_power_compact_cutoff_tab_rev_b` - folded aluminium 100A breaker/cutoff base/guard with upward lips, top-front placement basis.

## 3D Visualisation

- `battery_power_carrier_mount_rev_a_3d_visualisation.svg` is the static compact fabrication-read view.
- `battery_power_carrier_mount_rev_a_3d_visualisation.html` is the interactive compact fabrication-read view.
- `battery_power_carrier_mount_rev_a_assembled_3d_visualisation.svg` is the static attached compact assembly view.
- `battery_power_carrier_mount_rev_a_assembled_3d_visualisation.html` is the interactive attached compact assembly view showing the formed chassis saddle over the rail, upright bridge, compact tray, full-height battery, hold-down, low front Relay Rev C tray, top-front MIDI Rev C shelf, folded top-front cutoff base/guard with upward lips, keep-clear engine/LHD side envelope, and cable paths installed together.

## Package Relationship

- The relay hardware uses the known Relay Rev C folded tray (`320 x 220 mm` finished face; `360 x 255 mm` flat pattern). Its bent returns make a shallow tray, so the battery carrier must not duplicate that with a second large tray or move it onto the engine-side gap.
- The MIDI holder hardware uses `midi5_plate_mount_rev_c` (`190 x 150 mm`) and `midi5_holder_subplate_rev_c` (`140 x 85 mm`). This is an open plate/subplate assembly, so the current route is a shallow top-front shelf on the same cassette.
- The older `electrical_modules_rev_a` package includes bent/flanged aluminium tray/box concepts, but remains reference/fallback only.
- The cutoff folded base/guard gets only a pilot/opening allowance until the actual 100A breaker body size, mounting-hole centres, reset-lever access, terminal-stud spacing, and cable-lug sweep are measured. The lips fold upward to protect the breaker/lug envelope, not downward as hidden stiffeners.

## Compact Packaging Hold

- The latest battery-bay photos show no obvious full-size electrical mounting face beside the battery. The previous large sideways carrier is rejected for the active package.
- Before cutting final steel, make cardboard cards for the compact tray (`315 x 265 mm`), front service cassette spine (`325 x 120 mm`), Relay Rev C folded tray (`320 x 220 mm` plus return/depth blocks), MIDI Rev C top shelf (`190 x 150 mm` plus subplate/depth), folded cutoff base/guard (`170 x 110 mm` finished face / `210 x 150 mm` flat pattern / `20 mm` upward lips), cable lugs, and battery case.
- Test the front/radiator-side space first, with the relay tray low and the MIDI/cutoff cards on the top-front shelf. Use inboard/lower/outboard space only after steering, hose, heat, splash, bonnet, and battery-service clearances are proven.
- Reject any placement that enters the engine/LHD steering shaft/box/service sweep, hydraulic line path, alternator service space, bonnet clearance, radiator/fan envelope, or safe battery terminal service area.

## Battery-Cavity Mapping Plan

Use the battery as the fixed exclusion block before placing any relays, MIDI fuses, or cutoff breaker. The current package battery block is `275 x 230 x 190 mm`; verify it against the actual installed battery and update the map if the real battery differs.

- Establish datums with the vehicle facing forward: front/radiator side, rear/firewall side, inboard engine/LHD steering side, outboard wing side, and vertical bonnet clearance.
- Put the battery or a full-size battery box in the tray and mark a no-go block around it: battery case, hold-down, terminals, terminal boots, and cable lug bend radius.
- Measure the cavity in slices at tray height, mid-battery height, battery-top height, and bonnet/terminal-service height.
- Record available rectangles to the front, inboard/engine side, outboard/wing side, and below the tray. Do not count space that requires the battery to be removed for fuse or relay service.
- Trial the known templates in cardboard in the active order: Relay Rev C folded tray `320 x 220 mm` low on the front face, MIDI Rev C open plate `190 x 150 mm` on the shallow top-front shelf, folded cutoff base/guard `170 x 110 mm` finished face / `210 x 150 mm` flat pattern with `20 mm` upward lips at the top/front accessible corner, plus their real depth and cable lug sweep.
- Treat the front/radiator-side volume as the first candidate because both battery-in and battery-out photos suggest more usable space forward than sideways.
- Treat the inboard/engine-side gap as a keep-clear zone by default. It must stay clear of LHD steering shaft/box/service motion, hydraulic lines, hoses, alternator service, engine movement, and heat.
- Treat the lower void as cable support or shielded junction space only unless dry, serviceable, and protected from splash and heat.
- Split the layout by front elevation: relay low on the front vertical face, MIDI on the top-front shelf, cutoff at the top/front accessible corner, and P-clips on the stand/rail rather than the engine-side gap.

Detailed measurement rows are in `cavity_mapping_plan.csv`.

## Materials

- Stand top tray/deck, compact front cassette spine, top-front shelf tabs, and small steel tabs: `3.0 mm` mild steel.
- Tray/cassette angle-first stock: `25 x 25 x 3 mm` or `30 x 30 x 3 mm` pre-formed `90-degree` mild-steel angle for tray perimeter/upstands, cassette frame rails, shelf rails, and cable/P-clip tabs.
- Single chassis saddle and upright bridge flat interfaces: `4.0 mm` mild steel. Saddle flat-pattern allowance is nominal `220 x 230 mm` before rail-width measurement and bend allowance correction.
- Upright bridge angle-first stock: `40 x 40 x 4 mm` pre-formed `90-degree` mild-steel angle may replace straight bridge members if dry-fit keeps bolt access, service clearance, and battery/electrical layout clear.
- Battery hold-down crossbar: `3.0 mm` mild steel or stainless.
- Cutoff base/guard: `3.0 mm` 5052-H32 aluminium folded to a `170 x 110 mm` finished face with `20 mm` upstand lips around the 100A breaker/terminal side; use steel only if dry-fit proves the cutoff base must become a structural tab.
- Do not delete flat sheet/plate stock just because angle stock is available; the battery deck, chassis saddle, and electrical mounting faces still need controlled flat geometry.
- Use stainless or zinc-plated M6/M8/M10 hardware with star washers only where electrical bonding is intended. Otherwise isolate live hardware from the steel stand.

## Chassis Mounting Rules

- Pick up at the one known chassis attachment location with a formed saddle over the top of the chassis rail. The saddle must have legs down both rail sides and through-bolts through both legs/chassis; do not treat a flat side plate as the final fixing.
- Confirm rail top width, side height, bolt access, and crush-tube need before final saddle cutting. The nominal flat pattern is `70 mm` leg + measured rail-top cap + `70 mm` leg, shown as `220 x 230 mm` until measured.
- Do not add a second vehicle-side fixing unless the dry-fit proves the single-saddle route cannot carry the assembly safely.
- Do not drill or weld the chassis until the battery, bonnet, fan/belt, radiator, LHD steering-side, alternator-service, and cable-sweep clearances are checked.
- Use crush tubes if any pickup goes through boxed structure.
- The stand must remove from the chassis without cutting wires or removing unrelated radiator support pieces.

## Clearance Holds Before Cutting Final Metal

- Battery installed: length, width, full case height, terminal side, clamp path, and bonnet clearance.
- Compact holder cards: Relay Rev C low front tray, MIDI Rev C top-front shelf, folded cutoff top/front base/guard with upward lips, and cable-lug depth must fit the measured front/radiator volume without touching the steering-side service envelope.
- Single chassis saddle: rail top width, leg depth, through-bolt pitch, crush-tube need, stand-off height, upright bridge height, side-jog from saddle centreline to tray centreline, and access for tools. Current image-based target is `180 mm` rise with `90-150 mm` wing-side/outboard adjustment.
- 100A breaker/cutoff: body length/width/height, mounting hole centres, reset lever access, terminal stud size/spacing, and cable-lug sweep.
- Relay Rev C base: final low-front orientation, standoff height, seal direction, and loom exit direction.
- MIDI Rev C base/subplate: final top-front shelf feed/output orientation and cable bend radius.
- Cable support: P-clip positions every `150-200 mm` and near every direction change.

## Safety Notes

- No exposed positive stud may be able to touch the stand, bonnet, battery clamp, radiator support, or loose tools.
- Put insulating boots/caps over cutoff, MIDI, and relay feed studs.
- Keep the relay loom opening downward or side-down so water cannot pool.
- Route all heavy positive cables away from fan, belts, exhaust heat, steering movement, and sharp panel edges.
"""
    (OUT_DIR / "README.md").write_text(text, encoding="utf-8")


def write_cut_list() -> None:
    rows = [
        {
            "part_id": "BSTAND-TRAY-001",
            "drawing": "battery_stand_compact_top_tray_rev_b.dxf",
            "qty": "1",
            "material": "mild steel",
            "thickness_mm": "3.0",
            "status": "prototype_release_mockup_required",
            "notes": "Compact 315 x 265 battery tray/deck with battery clamp slots and cable clip holes. Electrical holders mount on the front/radiator-side cassette, not on engine-side panels.",
        },
        {
            "part_id": "BPCC-FRONT-RAIL-001",
            "drawing": "battery_power_compact_front_service_rail_rev_b.dxf",
            "qty": "1",
            "material": "mild steel",
            "thickness_mm": "3.0",
            "status": "cavity_map_required",
            "notes": "Compact 325 x 120 front/radiator-side service cassette spine: Relay Rev C mounts low on the front face, with shallow top-front shelf/base pickups for MIDI Rev C and the folded cutoff base/guard.",
        },
        {
            "part_id": "BSTAND-PICKUP-001",
            "drawing": "battery_stand_compact_single_chassis_pickup_rev_b.dxf",
            "qty": "1",
            "material": "mild steel",
            "thickness_mm": "4.0",
            "status": "site_fit",
            "notes": "Compact formed chassis saddle: nominal 220 x 230 flat pattern with 70 mm near leg, measured rail-top cap nominal 90 mm, and 70 mm far leg. Through-bolt both legs and chassis at the one known pickup location; use crush tubes/spacers where required.",
        },
        {
            "part_id": "BSTAND-UPRIGHT-001",
            "drawing": "battery_stand_compact_single_mount_upright_rev_b.dxf",
            "qty": "2 mirrored",
            "material": "mild steel",
            "thickness_mm": "4.0",
            "status": "site_fit",
            "notes": "Compact upright bridge side plates from the formed chassis saddle to tray/rail saddle; not a second chassis fixing location.",
        },
        {
            "part_id": "BSTAND-HOLD-001",
            "drawing": "battery_stand_compact_hold_down_crossbar_rev_b.dxf",
            "qty": "1",
            "material": "mild steel or stainless",
            "thickness_mm": "3.0",
            "status": "battery_measurement_hold",
            "notes": "Battery hold-down crossbar template; final slot spacing follows actual battery and clamp rod positions.",
        },
        {
            "part_id": "BPCC-CUTOFF-TAB-001",
            "drawing": "battery_power_compact_cutoff_tab_rev_b.dxf",
            "qty": "1",
            "material": "5052-H32 aluminium",
            "thickness_mm": "3.0",
            "status": "fit_after_switch_measurement",
            "notes": "Folded cutoff base/guard: 210 x 150 flat pattern, 170 x 110 finished face, 20 mm lips bent upward around the 100A breaker/terminal side. Open final breaker mounting holes only after the actual cutoff body, stud spacing, reset lever, and cable-lug sweep are measured.",
        },
    ]
    path = OUT_DIR / "fabricator_cut_list.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_inspection_checklist() -> None:
    rows = [
        {
            "check_id": "BPCC-CHECK-001",
            "stage": "mockup",
            "acceptance_check": "Compact stand tray clears installed battery, terminal clamp, bonnet, radiator, fan/belt, LHD steering path, and alternator service sweep.",
            "required_evidence": "Cardboard/top-tray photo with battery installed and ruler in frame.",
        },
        {
            "check_id": "BPCC-CHECK-001A",
            "stage": "compact_cavity_cards",
            "acceptance_check": "Compact holder cards prove the Rev C front-cassette stack: Relay Rev C folded tray 320 x 220 low on the front face, MIDI open plate 190 x 150 on a top-front shelf, folded cutoff base/guard 170 x 110 finished face / 210 x 150 flat pattern with 20 mm upward lips at the top/front accessible corner, with cable depth and lug sweep clear of LHD steering/hose/fan/bonnet/battery service envelopes.",
            "required_evidence": "Battery-installed LHD bay photos from top, engine side, wing side, and front with cardboard cards and cable-lug depth marked.",
        },
        {
            "check_id": "BPCC-CHECK-002",
            "stage": "chassis_pickup",
            "acceptance_check": "Battery and electrical load is taken by the one known chassis pickup through the formed saddle over the rail and upright bridge, not tray skin or unsupported inner wing.",
            "required_evidence": "Photos of the saddle over both chassis sides before and after drilling; note rail width, leg depth, bolt size, and crush-tube/spacer use.",
        },
        {
            "check_id": "BPCC-CHECK-003",
            "stage": "electrical_fit",
            "acceptance_check": "Folded Relay Rev C tray, MIDI open plate/subplate, and master cutoff folded base/guard all mount to the front/radiator-side cassette without forced cable bends, live-stud exposure, or use of the inboard engine-side gap as a component face.",
            "required_evidence": "Assembled bench photo and installed dry-fit photo with cable lugs mocked in.",
        },
        {
            "check_id": "BPCC-CHECK-004",
            "stage": "cable_support",
            "acceptance_check": "Main positive cable has insulated P-clips near direction changes and roughly every 150-200 mm.",
            "required_evidence": "Cable route photo showing clip holes/tabs and bend radius.",
        },
        {
            "check_id": "BPCC-CHECK-005",
            "stage": "coating",
            "acceptance_check": "Chassis saddle/upright bridge contact faces are deburred, primed, protected, and clear before final electrical hardware is installed.",
            "required_evidence": "Coated chassis saddle photo before mounting electrical parts.",
        },
    ]
    path = OUT_DIR / "inspection_checklist.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_layout_csv() -> None:
    rows = [
        {
            "zone": "battery_footprint",
            "x_mm": "20",
            "y_mm": "18",
            "w_mm": "275",
            "h_mm": "230",
            "z_height_mm": "190 visual reference; measure actual battery",
            "notes": "Current battery datum inside compact 315 x 265 tray; final footprint, full case height, and terminal side follow actual battery.",
        },
        {
            "zone": "compact_top_tray",
            "x_mm": "0",
            "y_mm": "0",
            "w_mm": "315",
            "h_mm": "265",
            "z_height_mm": "3 mm steel tray/deck plus battery mat",
            "notes": "Compact battery support tray only; do not use the tray skin as a large electrical backplane.",
        },
        {
            "zone": "relay_rev_c_low_front_card",
            "x_mm": "front face, centred to battery tray where possible",
            "y_mm": "low/front vertical cassette",
            "w_mm": "320",
            "h_mm": "220",
            "z_height_mm": "finished face plus 20 mm side/bottom returns, 15 mm top return, relay box and loom depth measurement hold",
            "notes": "Active candidate is low on the front/radiator-side cassette so it does not consume the inboard engine/LHD side gap.",
        },
        {
            "zone": "midi_rev_c_top_front_shelf_card",
            "x_mm": "top-front shelf, inside front cassette width",
            "y_mm": "above front relay tray if bonnet clearance passes",
            "w_mm": "190",
            "h_mm": "150",
            "z_height_mm": "known 190 x 150 plate plus 140 x 85 subplate and holder/cable depth",
            "notes": "Open plate/subplate assembly on a shallow top-front shelf; do not mount it on the engine-side face.",
        },
        {
            "zone": "cutoff_top_front_access_card",
            "x_mm": "top/front accessible corner",
            "y_mm": "adjacent to MIDI shelf, not engine-side",
            "w_mm": "170",
            "h_mm": "110",
            "z_height_mm": "210 x 150 mm flat pattern, 170 x 110 mm finished face, 20 mm upward guard lips, plus 100A breaker body/reset lever/stud height measurement hold",
            "notes": "Folded aluminium base/guard at the most accessible top/front position; lips bend upward around the 100A breaker/terminal side. Open final mounting holes after measuring the real breaker and lug sweep.",
        },
        {
            "zone": "front_radiator_service_cassette_spine",
            "x_mm": "site_fit",
            "y_mm": "site_fit",
            "w_mm": "325",
            "h_mm": "120",
            "z_height_mm": "component and cable-lug depth measurement hold",
            "notes": "Vehicle-side spine for the front-cassette stack; mounts relay low and provides top-front shelf/tab pickups for MIDI and cutoff.",
        },
        {
            "zone": "inboard_engine_lhd_keep_clear",
            "x_mm": "engine-side boundary from battery face",
            "y_mm": "full service height",
            "w_mm": "measurement_hold",
            "h_mm": "measurement_hold",
            "z_height_mm": "steering/hose/alternator/heat/service envelope",
            "notes": "Do not place relay, MIDI, or cutoff faces here by default. Use only protected cable clips/pass-throughs after steering, hose, heat, and service sweeps are proven.",
        },
        {
            "zone": "single_chassis_pickup",
            "x_mm": "site_fit",
            "y_mm": "site_fit",
            "w_mm": "220",
            "h_mm": "230 nominal developed pattern; adjust cap width to measured rail",
            "z_height_mm": "image estimate: 170-190 mm chassis-top-to-tray-underside target; adjustable 150-210 mm",
            "notes": "One 4 mm formed saddle goes over the chassis rail with legs down both sides and through-bolts at the known vehicle-side chassis location. May 14 no-battery bay photo suggests starting with 180 mm vertical rise from chassis top to tray underside.",
        },
        {
            "zone": "tray_side_jog_from_chassis_pickup",
            "x_mm": "image estimate: tray centre about 120 mm wing-side/outboard from chassis pickup centreline",
            "y_mm": "site_fit with battery in original pocket",
            "w_mm": "90-150 adjustment range",
            "h_mm": "n/a",
            "z_height_mm": "same tray plane as compact_top_tray",
            "notes": "Use slotted upper bridge holes or removable spacers/packers to tune side position. Keep the battery in the existing pocket and keep the engine/LHD side clear for steering, hose, and service sweep.",
        },
    ]
    path = OUT_DIR / "component_layout.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_cavity_mapping_plan() -> None:
    rows = [
        {
            "step_id": "CAV-001",
            "zone_or_task": "battery_datum",
            "datum_basis": "Current package battery block 275 x 230 x 190 mm; verify actual installed battery before final layout.",
            "measurements_to_capture": "Actual battery length, width, case height, terminal height, terminal orientation, hold-down path, and cable-lug bend radius.",
            "template_or_tool": "Battery installed or full-size cardboard/foam battery block plus tape/ruler.",
            "pass_rule": "Battery datum is marked on tray/frame before any relay, MIDI, cutoff, or cable support location is chosen.",
            "notes": "If the real battery differs from 275 x 230 x 190 mm, update component_layout.csv and redraw any cardboard templates before cutting steel.",
        },
        {
            "step_id": "CAV-002",
            "zone_or_task": "coordinate_system",
            "datum_basis": "Vehicle facing forward.",
            "measurements_to_capture": "Front/radiator side, rear/firewall side, inboard engine/LHD steering side, outboard wing side, tray plane, and bonnet/service height.",
            "template_or_tool": "Masking tape labels on tray, inner wing, front support, and engine-side obstruction line.",
            "pass_rule": "Every later measurement is recorded against the same front/rear/inboard/outboard/up datums.",
            "notes": "Avoid ambiguous left/right labels in the shop notes; use inboard/engine-side and outboard/wing-side.",
        },
        {
            "step_id": "CAV-003",
            "zone_or_task": "battery_no_go_block",
            "datum_basis": "Battery case plus service space.",
            "measurements_to_capture": "Minimum clearance around battery case, terminal boot height, clamp/crossbar sweep, and battery removal path.",
            "template_or_tool": "Tape outline around battery, 15-20 mm vibration allowance, 40 mm minimum terminal/service allowance, cable lug mock-ups.",
            "pass_rule": "No electrical module or bracket projects into the battery removal, hold-down, terminal, or cable-lug service envelope.",
            "notes": "Do not use space that only exists with the battery removed unless the part is a service-removable tray component.",
        },
        {
            "step_id": "CAV-004",
            "zone_or_task": "front_radiator_side_volume",
            "datum_basis": "Front edge of battery/tray to radiator/front-support obstruction.",
            "measurements_to_capture": "Clear width, height, depth, bolt access, radiator/fan clearance, hose sweep, and bonnet clearance.",
            "template_or_tool": "Front-cassette card set: 325 x 120 spine, Relay Rev C 320 x 220 low-front vertical tray with return/depth block, MIDI 190 x 150 top-front shelf, folded cutoff base/guard 170 x 110 finished face / 210 x 150 flat pattern / 20 mm upward lips, cable lugs with 40-80 mm depth blocks.",
            "pass_rule": "Active candidate only if the low relay face plus top-front MIDI/cutoff shelves fit with cable bends, no fan/radiator contact, bonnet clearance, and service access with battery installed.",
            "notes": "Both photos suggest the front volume is more realistic than the side gap; this package now makes front placement the active design.",
        },
        {
            "step_id": "CAV-004A",
            "zone_or_task": "chassis_pickup_height_and_side_jog",
            "datum_basis": "Top of visible chassis rail, chassis pickup centreline, and existing battery pocket/tray plane from the May 14 no-battery bay image.",
            "measurements_to_capture": "Chassis-top to tray-underside rise, saddle cap width over the rail, leg depth down both rail sides, through-bolt access, chassis pickup centreline to tray centreline side offset, and whether the upright bridge clears hose/steering/fan/radiator paths.",
            "template_or_tool": "Cardboard/plywood mock-up: 315 x 265 tray plane at 180 mm above chassis top, with a saddle card over both chassis sides and slotted side-jog trial marks at 90, 120, and 150 mm wing-side/outboard from the chassis pickup centreline.",
            "pass_rule": "Active estimate passes only if the formed saddle sits over both rail sides, the battery remains in the original pocket, bonnet/terminal clearance remains safe, and relay/MIDI/cutoff front-cassette cards fit without moving into the engine/LHD side envelope.",
            "notes": "Initial estimate only: target 180 mm rise and 120 mm wing-side/outboard jog; saddle flat pattern nominal 70 mm leg + measured rail top + 70 mm leg, with 150-210 mm vertical and 90-150 mm lateral adjustment before cutting final steel.",
        },
        {
            "step_id": "CAV-005",
            "zone_or_task": "inboard_engine_lhd_side_volume",
            "datum_basis": "Inboard/engine-side battery face to hoses, steering-side envelope, alternator/service path, and engine movement allowance.",
            "measurements_to_capture": "Usable vertical rectangle at tray/mid/top heights, steering shaft/box/service clearance, hose movement, heat exposure, and tool access.",
            "template_or_tool": "Keep-clear boundary tape plus cable/P-clip strip templates only; do not start with relay/MIDI/cutoff templates here.",
            "pass_rule": "Use for protected cable clips or pass-through routing only if it does not enter LHD steering/hose/service no-go space.",
            "notes": "Do not force relay, MIDI, or cutoff component faces into this side gap; the active component layout is front/radiator-side.",
        },
        {
            "step_id": "CAV-006",
            "zone_or_task": "lower_under_tray_volume",
            "datum_basis": "Bottom of tray/frame down to chassis, steering/hose runs, and splash/heat exposure.",
            "measurements_to_capture": "Height below tray, dry/splash exposure, service access, cable path, heat, and clamp points.",
            "template_or_tool": "Cable/P-clip templates first; electrical module templates only if fully protected and reachable.",
            "pass_rule": "Default to cable support or protected pass-through only; reject relay/MIDI/cutoff placement if wet, hot, or not serviceable.",
            "notes": "Lower space can help route cables but should not become the default place for live service parts.",
        },
        {
            "step_id": "CAV-007",
            "zone_or_task": "outboard_wing_side_volume",
            "datum_basis": "Battery outboard face to wing/side panel and bonnet side clearance.",
            "measurements_to_capture": "Side gap, vertical clearance, battery removal path, clamp access, panel strength, and water trap risk.",
            "template_or_tool": "Folded cutoff base/guard 170 x 110 finished face / 210 x 150 flat pattern / 20 mm upward lips and small cable-clamp templates.",
            "pass_rule": "Use only if it remains accessible with battery installed and does not block battery removal or bonnet/wing clearance.",
            "notes": "Likely useful for cable support or emergency cutoff access only if a clean panel exists.",
        },
        {
            "step_id": "CAV-008",
            "zone_or_task": "bonnet_and_terminal_height",
            "datum_basis": "Top of battery, terminals, relay/MIDI/cutoff depth, and bonnet closed/near-closed envelope.",
            "measurements_to_capture": "Clay/foam witness height above battery terminals, proposed module height, cable boots, and hold-down crossbar.",
            "template_or_tool": "Foam/clay stack or cardboard height blocks taped to battery and module templates.",
            "pass_rule": "No terminal, lug, fuse, relay, cutoff, or bracket touches bonnet or blocks safe terminal service clearance.",
            "notes": "This check decides whether top/front mounting is realistic or needs a lower stepped plate.",
        },
        {
            "step_id": "CAV-009",
            "zone_or_task": "split_layout_decision",
            "datum_basis": "Measured available rectangles from CAV-004 through CAV-008.",
            "measurements_to_capture": "Serviceable front-cassette rectangle, top-front shelf height, and cable length between battery, cutoff, MIDI, relay, and harness exit.",
            "template_or_tool": "Component cards in active stack order: Relay Rev C low-front 320 x 220, MIDI top-front 190 x 150, folded cutoff base/guard top-front 170 x 110 finished face / 210 x 150 flat pattern / 20 mm upward lips, plus depth/lug blocks.",
            "pass_rule": "Choose the front-cassette layout unless measured front space fails. Reopen split side/lower placement only with evidence that it is smaller, serviceable, and clear.",
            "notes": "Preferred order: cutoff top/front accessible, MIDI top/front short protected high-current path, relays low on front vertical face, P-clips on stand/cassette.",
        },
        {
            "step_id": "CAV-010",
            "zone_or_task": "evidence_closeout",
            "datum_basis": "Battery installed and battery removed photos.",
            "measurements_to_capture": "Top, front, inboard/engine-side, outboard/wing-side, lower, and near-closed bonnet photos with ruler and cardboard templates.",
            "template_or_tool": "Photo set plus filled cavity map; update component_layout.csv with measured clear rectangles.",
            "pass_rule": "No steel cutting for relay/MIDI/cutoff carrier until the filled cavity map proves at least one serviceable layout.",
            "notes": "Attach photos to the Fabrication workstream and keep original no-battery/battery-installed references with the map.",
        },
    ]
    path = OUT_DIR / "cavity_mapping_plan.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    drawings = [
        integrated_backplane(),
        battery_stand_top_tray(),
        single_chassis_pickup_mount(),
        single_mount_upright(),
        battery_hold_down_crossbar(),
        cutoff_guard(),
    ]
    for drawing in drawings:
        base.write_svg(drawing)
        base.write_dxf(drawing)
    base.write_pdf(drawings)
    write_readme()
    write_static_3d_visualisation()
    write_interactive_3d_visualisation()
    write_assembled_static_3d_visualisation()
    write_assembled_interactive_3d_visualisation()
    write_cut_list()
    write_inspection_checklist()
    write_layout_csv()
    write_cavity_mapping_plan()


if __name__ == "__main__":
    main()
