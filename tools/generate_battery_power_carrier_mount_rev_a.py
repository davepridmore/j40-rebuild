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

TRAY_W = 340
TRAY_D = 265
BATTERY_W = 318
BATTERY_D = 180
BATTERY_H = 230
FRONT_LADDER_W = 660
FRONT_LADDER_H = 310


def integrated_backplane() -> base.Drawing:
    cut_polys = [
        base.Poly([(0, 0), (FRONT_LADDER_W, 0), (FRONT_LADDER_W, FRONT_LADDER_H), (0, FRONT_LADDER_H)]),
        # Rail-to-stand / front-cavity pickup slots. Final pitch follows the tray lip/upright mock-up.
        base.rounded_slot_poly(18, 22, 42, 16),
        base.rounded_slot_poly(600, 22, 42, 16),
        base.rounded_slot_poly(18, 270, 42, 16),
        base.rounded_slot_poly(600, 270, 42, 16),
        # Folded Relay Rev C tray attachment field, kept outboard so the covered box is not hidden by the battery.
        base.rounded_slot_poly(58, 58, 34, 12),
        base.rounded_slot_poly(218, 58, 34, 12),
        base.rounded_slot_poly(58, 226, 34, 12),
        base.rounded_slot_poly(218, 226, 34, 12),
        # Shelf/base pickup points for the MIDI plate and folded cutoff base, with space for the five MIDI output cables.
        base.rounded_slot_poly(438, 112, 28, 12),
        base.rounded_slot_poly(488, 112, 28, 12),
        base.rounded_slot_poly(438, 184, 28, 12),
        base.rounded_slot_poly(488, 184, 28, 12),
    ]
    cut_circles = [
        # Cable P-clip / saddle clamp holes, including three relay exits, direct feeds, and five MIDI output branches.
        base.Circle(74, 86, 3.25),
        base.Circle(132, 136, 3.25),
        base.Circle(74, 244, 3.25),
        base.Circle(392, 244, 3.25),
        base.Circle(427, 244, 3.25),
        base.Circle(462, 244, 3.25),
        base.Circle(497, 244, 3.25),
        base.Circle(532, 244, 3.25),
        base.Circle(497, 278, 3.25),
        base.Circle(566, 278, 3.25),
        base.Circle(610, 146, 3.25),
    ]
    notes = [
        f"Raised front/radiator-side access ladder: {FRONT_LADDER_W} x {FRONT_LADDER_H} x 3.0 mm mild steel. This wider Rev F ladder moves the covered relay box fully outside the standard battery envelope and keeps its cover openable with the battery installed.",
        "The Relay Rev C folded aluminium tray mounts on the outboard/access edge of this ladder, with the covered relay box face reachable without lifting the battery and the flat plastic rear guard/underlay between the relay box and the metal tray.",
        "Reserve three separate relay wire-exit clusters with modelled offsets and sizes: upper red harness, side braided loom boot, and lower auxiliary/secondary loom relief.",
        "MIDI Rev C stays as the known open 190 x 150 plate/subplate on a separated top/front shelf zone, with its leading edge aligned to the battery leading edge datum, one common feed entering one side, and five heavy output cables leaving the opposite side through a seated comb/gland strip.",
        "One MIDI output position must have an enlarged double-wire pass-through because one fuse output leaves with two wires; the comb, saddles, and backplate must be attached to the shelf, not floating.",
        "The folded cutoff base/guard stays top/front accessible, with its leading edge aligned to the battery leading edge datum. Model the cutoff output as a stacked ring-lug splitter feeding both the covered relay feed and the MIDI common feed directly.",
        "Keep at least an 80 mm cable fanout/gutter around all relay exits, cutoff lugs, MIDI common feed, and five MIDI output lugs. Do not cut final holes until the battery-cavity map proves radiator, hose, steering, bonnet, tool, battery removal, and cable-bend clearance.",
    ]
    return base.Drawing(
        "battery_power_compact_front_service_rail_rev_b",
        FRONT_LADDER_W,
        FRONT_LADDER_H,
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
        base.Poly([(0, 0), (TRAY_W, 0), (TRAY_W, TRAY_D), (0, TRAY_D)]),
        # Battery hold-down / clamp slots.
        base.rounded_slot_poly(24, 38, 14, 38),
        base.rounded_slot_poly(24, 190, 14, 38),
        base.rounded_slot_poly(301, 38, 14, 38),
        base.rounded_slot_poly(301, 190, 14, 38),
        # Upright/front ladder saddle slots. Electrical modules mount to the front service ladder, not engine-side panels.
        base.rounded_slot_poly(145, 42, 18, 40),
        base.rounded_slot_poly(181, 42, 18, 40),
        base.rounded_slot_poly(145, 180, 18, 40),
        base.rounded_slot_poly(181, 180, 18, 40),
    ]
    cut_circles = [
        # Drain/cable clip holes.
        base.Circle(56, 242, 3.25),
        base.Circle(106, 242, 3.25),
        base.Circle(156, 242, 3.25),
        base.Circle(206, 242, 3.25),
        base.Circle(256, 242, 3.25),
        base.Circle(306, 242, 3.25),
    ]
    notes = [
        f"Compact battery stand top tray: {TRAY_W} x {TRAY_D} x 3.0 mm mild steel tray/deck around a standard N70/27-class battery envelope up to {BATTERY_W} x {BATTERY_D} x {BATTERY_H} mm with service allowance.",
        "The battery must be clamped by a removable top crossbar and J-rods/vertical rods outside the terminal path. Remove the hold-down before lifting the battery vertically out of the tray.",
        "Add low end/side stops or a formed edge so the battery cannot slide, but keep them low enough that the case can still be lifted out when the hold-down is removed.",
        "Electrical equipment uses the raised front/radiator-side access ladder: Relay Rev C on the outboard/access edge, MIDI Rev C and cutoff on separated front/top shelf zones whose leading edges align to the battery leading edge, and direct feeds from cutoff to both relay and MIDI. Do not use tray skin or the engine-side gap as a large backplane.",
        "Final battery footprint, terminal side, clamp path, bonnet clearance, front-cavity clearance, and LHD steering-side clearance are vehicle-measurement holds.",
        "Add an acid-resistant battery mat after paint; do not allow battery case or terminals to touch live studs or sharp steel edges.",
    ]
    return base.Drawing(
        "battery_stand_compact_top_tray_rev_b",
        TRAY_W,
        TRAY_D,
        cut_polys,
        [],
        cut_circles,
        [],
        notes,
    )


def battery_hold_down_crossbar() -> base.Drawing:
    cut_polys = [
        base.Poly([(0, 0), (TRAY_W, 0), (TRAY_W, 38), (0, 38)]),
        base.rounded_slot_poly(18, 11, 42, 16),
        base.rounded_slot_poly(280, 11, 42, 16),
    ]
    notes = [
        f"Compact battery hold-down crossbar: {TRAY_W} x 38 x 3.0 mm mild steel or stainless. Length and slots cover the standard N70/27-class battery envelope but remain template values until the actual battery is measured.",
        "Use J-bolts or vertical rods that cannot touch battery terminals. Add insulated caps where needed.",
        "The crossbar is a service-removable restraint; the battery must lift out vertically after the crossbar and rods are removed.",
        "Do not over-tighten against a plastic battery case; retain the battery without distorting it.",
    ]
    return base.Drawing(
        "battery_stand_compact_hold_down_crossbar_rev_b",
        TRAY_W,
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
    elements.extend(iso_prism(82, 70, 340, 265, 72, 10, "plate-top", "plate-side", "plate-front"))
    elements.extend(iso_prism(92, 106, 318, 180, 82, 230, "battery-top", "battery-side", "battery-front"))
    elements.extend(iso_prism(82, 96, 340, 18, 318, 8, "hold-top", "hold-side", "hold-front"))
    elements.extend(iso_prism(82, 276, 340, 18, 318, 8, "hold-top", "hold-side", "hold-front"))
    elements.extend(iso_prism(-120, 20, 660, 10, 82, 310, "plate-top", "plate-side", "plate-front"))
    # Known fabricated component bases now share a raised front/radiator-side service ladder.
    elements.extend(iso_prism(-250, 38, 320, 8, 128, 220, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(-254, 24, 8, 28, 128, 220, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(66, 24, 8, 28, 128, 220, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(-250, 24, 320, 28, 120, 8, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(-250, 24, 320, 28, 348, 8, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(-230, 36, 280, 6, 145, 185, "midi-board-top", "midi-board-side", "midi-board-front"))
    elements.extend(iso_prism(-220, 44, 260, 38, 175, 125, "relay-fuse-top", "relay-fuse-side", "relay-fuse-front"))
    # MIDI/cutoff row starts from the same leading X datum as the battery envelope.
    elements.extend(iso_prism(92, 18, 190, 150, 292, 8, "midi-plate-top", "midi-plate-side", "midi-plate-front"))
    elements.extend(iso_prism(117, 44, 140, 85, 306, 10, "midi-board-top", "midi-board-side", "midi-board-front"))
    for idx in range(5):
        elements.extend(iso_prism(126 + idx * 24, 70, 18, 54, 322, 16, "fuse-top", "fuse-side", "fuse-front"))
    elements.extend(iso_prism(113, 42, 132, 12, 344, 8, "breaker-terminal", "breaker-terminal", "breaker-terminal"))
    elements.extend(iso_prism(122, 128, 150, 14, 344, 10, "breaker-lever-top", "breaker-lever-side", "breaker-lever-front"))
    elements.extend(iso_prism(92, 180, 110, 170, 292, 8, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(88, 180, 8, 170, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(202, 180, 8, 170, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(92, 176, 110, 8, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(92, 350, 110, 8, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    # Keep-clear zone for the inboard engine/LHD steering side.
    elements.extend(iso_prism(420, 72, 18, 230, 78, 225, "keepout-top", "keepout-side", "keepout-front"))
    elements.extend(iso_prism(106, 236, 82, 56, 314, 28, "breaker-body-top", "breaker-body-side", "breaker-body-front"))
    elements.extend(iso_prism(111, 242, 72, 44, 342, 6, "breaker-face-top", "breaker-face-side", "breaker-face-front"))
    elements.extend(iso_prism(117, 258, 46, 10, 350, 6, "breaker-lever-top", "breaker-lever-side", "breaker-lever-front"))
    for point in [(120, 248, 350), (174, 272, 350)]:
        x, y = iso_point(*point)
        elements.append(f'<circle class="breaker-terminal" cx="{x:.1f}" cy="{y:.1f}" r="5" />')
    elements.append(iso_polyline([(275, 108, 280), (160, 230, 334), (120, 248, 350)], "positive-cable"))
    elements.append(iso_polyline([(174, 272, 350), (156, 176, 346), (132, 54, 330)], "relay-feed"))
    elements.append(iso_polyline([(174, 272, 350), (20, 180, 346), (-120, 66, 308)], "relay-feed"))
    elements.append(iso_polyline([(-120, 66, 308), (-174, 42, 210), (-210, 44, 160)], "branch-cable"))
    elements.extend(iso_prism(88, 34, 410, 34, 330, 10, "keepout-top", "keepout-side", "keepout-front"))
    for point in [(214, 156, -50), (382, 156, -50), (214, 296, -50), (382, 296, -50)]:
        x, y = iso_point(*point)
        elements.append(f'<circle class="slot-marker" cx="{x:.1f}" cy="{y:.1f}" r="4" />')

    labels = [
        ("Formed chassis saddle", 126, 504),
        ("Single upright bridge", 166, 365),
        ("Compact battery tray / stand", 322, 434),
        ("Standard battery envelope on stand", 238, 214),
        ("Outboard relay cover access", 446, 230),
        ("Battery-aligned MIDI shelf", 430, 305),
        ("Battery-aligned cutoff tray", 430, 365),
        ("Cutoff splits direct to relay + MIDI", 532, 332),
        ("Engine/LHD side keep-clear", 570, 430),
    ]
    for text, x, y in labels:
        elements.append(f'<text class="label" x="{x}" y="{y}">{text}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="620" viewBox="0 0 920 620" role="img" aria-labelledby="title desc">
  <title id="title">Battery stand power carrier Rev F standard-battery access 3D visualisation</title>
  <desc id="desc">Isometric visualisation of a compact steel battery stand mounted by a formed saddle over the chassis rail, carrying a standard N70/27-class battery envelope on a removable hold-down tray with an outboard-access covered Relay Rev C box, three sized relay wire-exit clusters, plastic relay underlay ahead of the folded metal tray, MIDI Rev C and cutoff leading edges aligned to the battery datum, MIDI seated output comb/backplate with one enlarged double-wire pass-through, and a folded cutoff base/guard with a direct splitter feeding both relay and MIDI while the inboard engine/LHD side stays clear.</desc>
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
  <title>J40 Battery Stand Power Carrier Rev F Standard-Battery Access - 3D Visualisation</title>
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
    <h1>Battery Stand Power Carrier Rev F Standard-Battery Access Layout</h1>
    <div class="meta">
      <span class="chip">Steel chassis-bolted stand</span>
      <span class="chip">Formed chassis saddle</span>
      <span class="chip">Standard battery envelope</span>
      <span class="chip">Removable hold-down</span>
      <span class="chip">Outboard relay access</span>
      <span class="chip">Three relay wire exits</span>
      <span class="chip">Relay exit cluster sizes</span>
      <span class="chip">Covered relay box</span>
      <span class="chip">Battery-aligned MIDI/cutoff</span>
      <span class="chip">Direct cutoff feeds</span>
      <span class="chip">Seated MIDI output comb</span>
      <span class="chip">Five MIDI output cables</span>
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
          <dd>The compact battery tray mounts from one formed saddle over the chassis rail through a compact upright bridge and now carries a standard N70/27-class envelope with a removable hold-down.</dd>
        </div>
        <div>
          <dt>Power path</dt>
          <dd>The folded Relay Rev C tray sits outside the battery footprint with the cover openable and three wire-exit clusters represented with relative offsets and sizes. MIDI Rev C and the cutoff base now start on the battery leading-edge datum, with a seated output comb/backplate, one enlarged double-wire output hole, five heavy MIDI output leads, and a visible direct-feed splitter.</dd>
        </div>
        <div>
          <dt>Service intent</dt>
          <dd>The stand is removable from the chassis after coated pickup points are finished; final holes stay gated by actual battery measurement, hold-down/lift-out path, bonnet, engine/LHD steering-side, radiator/fan, hose, and cable-sweep checks.</dd>
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

    const baseCameraPosition = new THREE.Vector3(920, 780, 1280);
    const baseTarget = new THREE.Vector3(-170, 220, 95);
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
      box(`${name} plain removable front cover`, x, y, z - 78, 286, 183, 9, materials.black);
      box(`${name} shallow raised cover rim`, x, y, z - 86, 300, 197, 6, materials.relayDetail);
      cyl(`${name} upper cover screw`, x, y + 58, z - 94, 4, 8, materials.silver, Math.PI / 2);
      cyl(`${name} lower cover screw`, x, y - 58, z - 94, 4, 8, materials.silver, Math.PI / 2);
      box(`${name} upper red harness cluster 136 x 24 x 34 at relay offset X-62 Y+110 Z-58`, x - 62, y + 110, z - 58, 136, 24, 34, materials.cableRed);
      box(`${name} right braided loom cluster 42 x 118 x 42 at relay offset X+164 Y-10 Z-52`, x + 164, y - 10, z - 52, 42, 118, 42, materials.black);
      box(`${name} lower auxiliary cluster 96 x 24 x 30 at relay offset X-96 Y-110 Z-60`, x - 96, y - 110, z - 60, 96, 24, 30, materials.black);
      box(`${name} braided loom boot and service loop`, x + 202, y - 36, z - 52, 44, 104, 44, materials.black);
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
      box("Relay Rev C flat plastic rear guard / underlay before folded metal tray", x, y, z - 18, 280, 185, 6, materials.midiBoard);
      box("Relay cover removal volume in front of cover", x, y, z - 128, 360, 238, 56, materials.keepout);
      box("Relay upper red harness cluster keepout 164 x 52 x 54 at relay offset X-62 Y+148 Z-58", x - 62, y + 148, z - 58, 164, 52, 54, materials.keepout);
      box("Relay side braided loom cluster keepout 72 x 156 x 70 at relay offset X+202 Y-24 Z-52", x + 202, y - 24, z - 52, 72, 156, 70, materials.keepout);
      box("Relay lower auxiliary cluster keepout 132 x 52 x 54 at relay offset X-96 Y-148 Z-60", x - 96, y - 148, z - 60, 132, 52, 54, materials.keepout);
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
      box("Top-front MIDI common feed bus / single input side", x - 74, y + 62, z - 34, 34, 10, 18, materials.brass);
      box("Top-front MIDI output guide backplate attached between subplate and comb", x, y + 48, z + 51, 170, 22, 16, materials.plateEdge);
      box("Top-front MIDI output cable clamp comb bolted flush to guide backplate", x, y + 72, z + 60, 154, 18, 20, materials.plateEdge);
      box("Top-front MIDI output comb left support tab tied into shelf plate", x - 88, y + 48, z + 60, 12, 42, 20, materials.plateEdge);
      box("Top-front MIDI output comb right support tab tied into shelf plate", x + 88, y + 48, z + 60, 12, 42, 20, materials.plateEdge);
      for (let idx = 0; idx < 5; idx += 1) {
        midiHolderTop(`Top-front MIDI holder ${idx + 1}`, x - 54 + idx * 27, y, z);
        box(`Top-front MIDI output ${idx + 1} grommet saddle seated in attached comb`, x - 54 + idx * 27, y + 86, z + 60, idx === 2 ? 28 : 20, 14, idx === 2 ? 30 : 20, materials.black);
      }
      box("MIDI fuse 3 enlarged double-wire access hole cut through attached comb", x, y + 98, z + 60, 42, 8, 36, materials.silver);
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
    box("Compact battery stand top tray 340 x 265", -110, 68, 42, 340, 8, 265, materials.plate);
    box("Standard N70/27-class battery envelope 318 x 180 x 230", -120, 187, 32, 318, 230, 180, materials.battery);
    cyl("Battery positive terminal", -24, 310, -34, 9, 14, materials.brass, 0);
    cyl("Battery negative terminal", -210, 310, 98, 9, 14, materials.brass, 0);
    box("Removable battery hold-down crossbar front", -120, 310, -74, 340, 8, 18, materials.plateEdge);
    box("Removable battery hold-down crossbar rear", -120, 310, 138, 340, 8, 18, materials.plateEdge);
    box("Low battery front/end stop under lift-out path", -120, 88, -58, 330, 22, 12, materials.plateEdge);
    box("Low battery rear/end stop under lift-out path", -120, 88, 122, 330, 22, 12, materials.plateEdge);
    box("Battery vertical lift-out clearance envelope with hold-down removed", -120, 462, 32, 360, 290, 220, materials.keepout);
    box("Raised outboard access service ladder spine 660 x 310", -330, 205, 168, 660, 310, 8, materials.plate);
    knownRelayCarrierBase(-500, 238, 176);
    box("Battery leading-edge datum shared by MIDI and cutoff starts", -279, 326, 250, 6, 260, 18, materials.bendLine);
    knownMidiTopShelf(-184, 318, 198);
    cutoffSwitchTop("100A resettable breaker cutoff", -194, 318, 326);
    box("Inboard engine/LHD steering-side keep-clear envelope", 142, 150, 70, 16, 260, 270, materials.keepout);
    box("Relay cover removal clearance outside battery footprint", -500, 238, 92, 380, 250, 76, materials.keepout);
    box("Shared 80 mm power cable gutter above relay/MIDI/cutoff", -370, 392, 228, 660, 26, 92, materials.keepout);
    box("MIDI five-output heavy cable fanout clearance with one double-wire output", -184, 424, 278, 300, 106, 86, materials.keepout);
    cable("Battery positive to battery-aligned cutoff input", [[-24, 318, -34], [-112, 344, 126], [-230, 382, 295]], 7, materials.cableRed);
    box("Cutoff output stacked ring-lug splitter to relay and MIDI", -158, 386, 357, 34, 10, 34, materials.brass);
    const cutoffOutput = [-158, 386, 357];
    cable("Cutoff direct feed to battery-aligned MIDI common input side", [cutoffOutput, [-220, 390, 310], [-258, 382, 164]], 7, materials.cableRed);
    cable("Cutoff direct feed to covered relay common", [cutoffOutput, [-250, 374, 300], [-420, 332, 154], [-640, 300, 62]], 7, materials.cableRed);
    cable("Relay upper red harness exit to service gutter", [[-562, 348, 118], [-614, 396, 136], [-660, 404, 166]], 5, materials.cableRed);
    cable("Relay right braided loom exit down outboard service side", [[-296, 228, 116], [-320, 148, 132], [-360, 82, 152]], 6, materials.cableBlack);
    cable("Relay lower auxiliary wire exit to lower clip", [[-596, 128, 116], [-626, 100, 130], [-650, 84, 146]], 4, materials.cableBlack);
    const midiOutputXs = [-238, -211, -184, -157, -130];
    for (let idx = 0; idx < midiOutputXs.length; idx += 1) {
      const hx = midiOutputXs[idx];
      cable(`MIDI fuse ${idx + 1} heavy output cable through seated comb guide`, [[hx, 382, 228], [hx, 404, 258], [hx, 448, 298]], 6, materials.cableRed);
      if (idx === 2) {
        cable("MIDI fuse 3 second heavy output cable through enlarged comb access hole", [[hx + 8, 382, 228], [hx + 8, 406, 268], [hx + 28, 450, 312]], 5, materials.cableRed);
      }
    }

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
      const fitScale = aspect < 0.9 ? Math.min(2.8, 1.3 / Math.max(aspect, 0.45)) : 1.25;
      const nextPosition = baseTarget.clone().add(
        baseCameraPosition.clone().sub(baseTarget).multiplyScalar(fitScale)
      );
      camera.position.copy(nextPosition);
      controls.target.copy(baseTarget);
      controls.minDistance = Math.max(500, 600 * fitScale);
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
    elements.extend(iso_prism(82, 70, 340, 265, 72, 10, "plate-top", "plate-side", "plate-front"))
    elements.extend(iso_prism(92, 106, 318, 180, 82, 230, "battery-top", "battery-side", "battery-front"))
    elements.extend(iso_prism(82, 96, 340, 18, 318, 8, "hold-top", "hold-side", "hold-front"))
    elements.extend(iso_prism(82, 276, 340, 18, 318, 8, "hold-top", "hold-side", "hold-front"))
    elements.extend(iso_prism(-120, 20, 660, 10, 82, 310, "plate-top", "plate-side", "plate-front"))
    elements.extend(iso_prism(-250, 38, 320, 8, 128, 220, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(-254, 24, 8, 28, 128, 220, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(66, 24, 8, 28, 128, 220, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(-250, 24, 320, 28, 120, 8, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(-250, 24, 320, 28, 348, 8, "relay-tray-top", "relay-tray-side", "relay-tray-front"))
    elements.extend(iso_prism(-230, 36, 280, 6, 145, 185, "midi-board-top", "midi-board-side", "midi-board-front"))
    elements.extend(iso_prism(-220, 44, 260, 38, 175, 125, "relay-fuse-top", "relay-fuse-side", "relay-fuse-front"))
    # MIDI/cutoff row starts from the same leading X datum as the battery envelope.
    elements.extend(iso_prism(92, 18, 190, 150, 292, 8, "midi-plate-top", "midi-plate-side", "midi-plate-front"))
    elements.extend(iso_prism(117, 44, 140, 85, 306, 10, "midi-board-top", "midi-board-side", "midi-board-front"))
    for idx in range(5):
        elements.extend(iso_prism(126 + idx * 24, 70, 18, 54, 322, 16, "fuse-top", "fuse-side", "fuse-front"))
    elements.extend(iso_prism(113, 42, 132, 12, 344, 8, "breaker-terminal", "breaker-terminal", "breaker-terminal"))
    elements.extend(iso_prism(122, 128, 150, 14, 344, 10, "breaker-lever-top", "breaker-lever-side", "breaker-lever-front"))
    elements.extend(iso_prism(92, 180, 110, 170, 292, 8, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(88, 180, 8, 170, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(202, 180, 8, 170, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(92, 176, 110, 8, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(92, 350, 110, 8, 300, 22, "cutoff-base-top", "cutoff-base-side", "cutoff-base-front"))
    elements.extend(iso_prism(420, 72, 18, 230, 78, 225, "keepout-top", "keepout-side", "keepout-front"))
    elements.extend(iso_prism(106, 236, 82, 56, 314, 28, "breaker-body-top", "breaker-body-side", "breaker-body-front"))
    elements.extend(iso_prism(111, 242, 72, 44, 342, 6, "breaker-face-top", "breaker-face-side", "breaker-face-front"))
    elements.extend(iso_prism(117, 258, 46, 10, 350, 6, "breaker-lever-top", "breaker-lever-side", "breaker-lever-front"))
    for point in [(120, 248, 350), (174, 272, 350)]:
        x, y = iso_point(*point)
        elements.append(f'<circle class="breaker-terminal" cx="{x:.1f}" cy="{y:.1f}" r="5" />')
    elements.append(iso_polyline([(275, 108, 280), (160, 230, 334), (120, 248, 350)], "positive-cable"))
    elements.append(iso_polyline([(174, 272, 350), (156, 176, 346), (132, 54, 330)], "relay-feed"))
    elements.append(iso_polyline([(174, 272, 350), (20, 180, 346), (-120, 66, 308)], "relay-feed"))
    elements.append(iso_polyline([(-120, 66, 308), (-174, 42, 210), (-210, 44, 160)], "branch-cable"))
    elements.extend(iso_prism(88, 34, 410, 34, 330, 10, "keepout-top", "keepout-side", "keepout-front"))
    for point in [(214, 156, -50), (382, 156, -50), (214, 296, -50), (382, 296, -50)]:
        x, y = iso_point(*point)
        elements.append(f'<circle class="slot-marker" cx="{x:.1f}" cy="{y:.1f}" r="4" />')
    for text, x, y in (
        ("Attached compact battery stand assembly", 82, 84),
        ("Standard battery bolted on compact tray", 192, 214),
        ("Formed chassis saddle", 132, 508),
        ("Single upright bridge", 158, 364),
        ("Outboard relay cover service ladder", 500, 252),
        ("Battery-aligned MIDI/cutoff starts", 390, 340),
        ("Engine/LHD side kept clear", 548, 430),
    ):
        elements.append(f'<text class="label" x="{x}" y="{y}">{text}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="620" viewBox="0 0 920 620" role="img" aria-labelledby="title desc">
  <title id="title">Battery stand power carrier Rev F standard-battery assembled 3D visualisation</title>
  <desc id="desc">Attached assembly view of the compact steel battery stand with a formed saddle over the chassis rail, standard N70/27-class battery envelope on a removable hold-down tray, outboard-access covered Relay Rev C box with three sized wire-exit clusters and plastic relay underlay ahead of the folded metal tray, MIDI Rev C and cutoff leading edges aligned to the battery datum, MIDI seated output comb/backplate with enlarged double-wire pass-through, folded cutoff base/guard with a direct splitter feeding relay and MIDI, and the inboard engine/LHD side kept clear.</desc>
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
  <title>J40 Battery Stand Power Carrier Rev F Standard-Battery Access - Assembled 3D Visualisation</title>
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
    <h1>Assembled Battery Stand Power Carrier Rev F Standard-Battery Access Layout</h1>
    <div class="meta">
      <span class="chip">Attached assembly</span>
      <span class="chip">Formed chassis saddle</span>
      <span class="chip">Standard battery envelope</span>
      <span class="chip">Removable hold-down</span>
      <span class="chip">Outboard relay access</span>
      <span class="chip">Three relay wire exits</span>
      <span class="chip">Relay exit cluster sizes</span>
      <span class="chip">Covered relay box</span>
      <span class="chip">Battery-aligned MIDI/cutoff</span>
      <span class="chip">Direct cutoff feeds</span>
      <span class="chip">Seated MIDI output comb</span>
      <span class="chip">Five MIDI output cables</span>
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
        <div><dt>Load path</dt><dd>One formed saddle over the chassis rail and an upright bridge carry the compact steel battery tray, standard battery envelope, removable hold-down, and widened front access-ladder shelf/tab pickups.</dd></div>
        <div><dt>Integrated equipment</dt><dd>The standard N70/27-class battery envelope, outboard-access covered Relay Rev C tray with three sized exit clusters, MIDI Rev C open plate with a seated output comb/backplate and one double-wire access hole, and folded cutoff base/guard are shown attached as a front access-ladder layout with MIDI and cutoff starts aligned to the battery leading datum.</dd></div>
        <div><dt>Release hold</dt><dd>Final hole centres, holder positions, battery lift-out path, and cable paths still need battery-installed LHD mock-up photos before cutting final metal, with the inboard engine side treated as a service/clearance envelope.</dd></div>
      </dl>
    </aside>
  </main>
  <script type="module">
    import * as THREE from "three";
    import { OrbitControls } from "three/addons/controls/OrbitControls.js";

    const mount = document.getElementById("viewport");
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f6f7);
    const baseCameraPosition = new THREE.Vector3(920, 780, 1280);
    const baseTarget = new THREE.Vector3(-170, 220, 95);
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
      box(`${name} plain removable front cover`, x, y, z - 78, 286, 183, 9, materials.black);
      box(`${name} shallow raised cover rim`, x, y, z - 86, 300, 197, 6, materials.relayDetail);
      cyl(`${name} upper cover screw`, x, y + 58, z - 94, 4, 8, materials.silver, Math.PI / 2);
      cyl(`${name} lower cover screw`, x, y - 58, z - 94, 4, 8, materials.silver, Math.PI / 2);
      box(`${name} upper red harness cluster 136 x 24 x 34 at relay offset X-62 Y+110 Z-58`, x - 62, y + 110, z - 58, 136, 24, 34, materials.cableRed);
      box(`${name} right braided loom cluster 42 x 118 x 42 at relay offset X+164 Y-10 Z-52`, x + 164, y - 10, z - 52, 42, 118, 42, materials.black);
      box(`${name} lower auxiliary cluster 96 x 24 x 30 at relay offset X-96 Y-110 Z-60`, x - 96, y - 110, z - 60, 96, 24, 30, materials.black);
      box(`${name} braided loom boot and service loop`, x + 202, y - 36, z - 52, 44, 104, 44, materials.black);
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
      box("Relay Rev C flat plastic rear guard / underlay before folded metal tray", x, y, z - 18, 280, 185, 6, materials.midiBoard);
      box("Relay cover removal volume in front of cover", x, y, z - 128, 360, 238, 56, materials.keepout);
      box("Relay upper red harness cluster keepout 164 x 52 x 54 at relay offset X-62 Y+148 Z-58", x - 62, y + 148, z - 58, 164, 52, 54, materials.keepout);
      box("Relay side braided loom cluster keepout 72 x 156 x 70 at relay offset X+202 Y-24 Z-52", x + 202, y - 24, z - 52, 72, 156, 70, materials.keepout);
      box("Relay lower auxiliary cluster keepout 132 x 52 x 54 at relay offset X-96 Y-148 Z-60", x - 96, y - 148, z - 60, 132, 52, 54, materials.keepout);
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
      box("Top-front MIDI common feed bus / single input side", x - 74, y + 62, z - 34, 34, 10, 18, materials.brass);
      box("Top-front MIDI output guide backplate attached between subplate and comb", x, y + 48, z + 51, 170, 22, 16, materials.plateEdge);
      box("Top-front MIDI output cable clamp comb bolted flush to guide backplate", x, y + 72, z + 60, 154, 18, 20, materials.plateEdge);
      box("Top-front MIDI output comb left support tab tied into shelf plate", x - 88, y + 48, z + 60, 12, 42, 20, materials.plateEdge);
      box("Top-front MIDI output comb right support tab tied into shelf plate", x + 88, y + 48, z + 60, 12, 42, 20, materials.plateEdge);
      for (let idx = 0; idx < 5; idx += 1) {
        midiHolderTop(`Top-front MIDI holder ${idx + 1}`, x - 54 + idx * 27, y, z);
        box(`Top-front MIDI output ${idx + 1} grommet saddle seated in attached comb`, x - 54 + idx * 27, y + 86, z + 60, idx === 2 ? 28 : 20, 14, idx === 2 ? 30 : 20, materials.black);
      }
      box("MIDI fuse 3 enlarged double-wire access hole cut through attached comb", x, y + 98, z + 60, 42, 8, 36, materials.silver);
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
    box("Assembled compact battery stand top tray 340 x 265", -110, 68, 42, 340, 8, 265, materials.plate);
    box("Standard N70/27-class battery envelope 318 x 180 x 230", -120, 187, 32, 318, 230, 180, materials.battery);
    cyl("Battery positive terminal", -24, 310, -34, 9, 14, materials.brass, 0);
    cyl("Battery negative terminal", -210, 310, 98, 9, 14, materials.brass, 0);
    box("Removable battery hold-down crossbar front", -120, 310, -74, 340, 8, 18, materials.plateEdge);
    box("Removable battery hold-down crossbar rear", -120, 310, 138, 340, 8, 18, materials.plateEdge);
    box("Low battery front/end stop under lift-out path", -120, 88, -58, 330, 22, 12, materials.plateEdge);
    box("Low battery rear/end stop under lift-out path", -120, 88, 122, 330, 22, 12, materials.plateEdge);
    box("Battery vertical lift-out clearance envelope with hold-down removed", -120, 462, 32, 360, 290, 220, materials.keepout);
    for (const x of [-250, 10]) {
      cyl("Front hold-down rod to tray", x, 190, -70, 4, 238, materials.brass, 0);
      cyl("Rear hold-down rod to tray", x, 190, 134, 4, 238, materials.brass, 0);
    }
    box("Raised outboard access service ladder spine 660 x 310", -330, 205, 168, 660, 310, 8, materials.plate);
    knownRelayCarrierBase(-500, 238, 176);
    box("Battery leading-edge datum shared by MIDI and cutoff starts", -279, 326, 250, 6, 260, 18, materials.bendLine);
    knownMidiTopShelf(-184, 318, 198);
    cutoffSwitchTop("100A resettable breaker cutoff", -194, 318, 326);
    box("Inboard engine/LHD steering-side keep-clear envelope", 142, 150, 70, 16, 260, 270, materials.keepout);
    box("Relay cover removal clearance outside battery footprint", -500, 238, 92, 380, 250, 76, materials.keepout);
    box("Shared 80 mm power cable gutter above relay/MIDI/cutoff", -370, 392, 228, 660, 26, 92, materials.keepout);
    box("MIDI five-output heavy cable fanout clearance with one double-wire output", -184, 424, 278, 300, 106, 86, materials.keepout);
    cable("Battery positive to battery-aligned cutoff input", [[-24, 318, -34], [-112, 344, 126], [-230, 382, 295]], 7, materials.cableRed);
    box("Cutoff output stacked ring-lug splitter to relay and MIDI", -158, 386, 357, 34, 10, 34, materials.brass);
    const cutoffOutput = [-158, 386, 357];
    cable("Cutoff direct feed to battery-aligned MIDI common input side", [cutoffOutput, [-220, 390, 310], [-258, 382, 164]], 7, materials.cableRed);
    cable("Cutoff direct feed to covered relay common", [cutoffOutput, [-250, 374, 300], [-420, 332, 154], [-640, 300, 62]], 7, materials.cableRed);
    cable("Relay upper red harness exit to service gutter", [[-562, 348, 118], [-614, 396, 136], [-660, 404, 166]], 5, materials.cableRed);
    cable("Relay right braided loom exit down outboard service side", [[-296, 228, 116], [-320, 148, 132], [-360, 82, 152]], 6, materials.cableBlack);
    cable("Relay lower auxiliary wire exit to lower clip", [[-596, 128, 116], [-626, 100, 130], [-650, 84, 146]], 4, materials.cableBlack);
    const midiOutputXs = [-238, -211, -184, -157, -130];
    for (let idx = 0; idx < midiOutputXs.length; idx += 1) {
      const hx = midiOutputXs[idx];
      cable(`MIDI fuse ${idx + 1} heavy output cable through seated comb guide`, [[hx, 382, 228], [hx, 404, 258], [hx, 448, 298]], 6, materials.cableRed);
      if (idx === 2) {
        cable("MIDI fuse 3 second heavy output cable through enlarged comb access hole", [[hx + 8, 382, 228], [hx + 8, 406, 268], [hx + 28, 450, 312]], 5, materials.cableRed);
      }
    }

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
      const fitScale = aspect < 0.9 ? Math.min(2.8, 1.3 / Math.max(aspect, 0.45)) : 1.25;
      const nextPosition = baseTarget.clone().add(
        baseCameraPosition.clone().sub(baseTarget).multiplyScalar(fitScale)
      );
      camera.position.copy(nextPosition);
      controls.target.copy(baseTarget);
      controls.minDistance = Math.max(500, 600 * fitScale);
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
    text = """# J40 Battery Stand Power Carrier Pack - Rev F Standard-Battery Access Update

This package changes the battery-side plan into a compact steel chassis-bolted stand with a standard battery envelope, removable hold-down, and widened raised front/radiator-side access ladder. It supports and removes the battery first, keeps the inboard engine/LHD side clear, moves the covered relay box fully outside the battery footprint, aligns the MIDI and cutoff starts to the battery leading-edge datum, and reserves enough room for three sized relay wire-exit clusters, the cutoff splitter, one MIDI common feed, and five heavy MIDI output cables.

## Design Intent

- Mount the battery stand from the one known chassis pickup location using a compact formed saddle over the chassis rail plus an upright bridge.
- Support the battery on a compact `340 x 265 mm` tray around a standard N70/27-class envelope up to `318 x 180 x 230 mm`.
- Retain the battery with a removable top crossbar and J-rods/vertical rods outside the terminal path. The battery must lift vertically out once the hold-down is removed, without removing the relay box or MIDI shelf.
- Put Relay Rev C on the outboard/access edge of the raised front ladder: `320 x 220 mm` finished folded tray, `360 x 255 mm` flat pattern, `20 mm` side/bottom returns, and `15 mm` top return. The relay box is modelled as a plain covered enclosure; the flat plastic rear guard/underlay sits between the relay box and folded metal tray.
- Reserve three separate relay wire exits with explicit visual cluster sizes and offsets relative to the relay-box centre: upper red harness `136 x 24 x 34 mm` at `X-62 / Y+110 / Z-58`, side braided loom `42 x 118 x 42 mm` at `X+164 / Y-10 / Z-52`, and lower auxiliary `96 x 24 x 30 mm` at `X-96 / Y-110 / Z-60`.
- Put MIDI Rev C on a separated shallow top-front shelf using the known open `190 x 150 mm` aluminium plate plus `140 x 85 mm` insulating subplate. Its leading edge starts at the battery leading-edge datum; keep one common feed entering one side and five heavy protected output cables leaving the opposite side through a seated comb/gland strip tied back to the shelf.
- Provide one enlarged double-wire MIDI output access hole for the output that leaves with two wires. The output guide backplate, comb, saddles, and support tabs are modelled as attached pieces, not floating cable guides.
- Put the 100A breaker/cutoff on the top/front accessible corner with its leading edge also aligned to the battery leading-edge datum, on a folded aluminium base/guard: `210 x 150 mm` flat pattern, `170 x 110 mm` finished face, and `20 mm` lips bent upward toward the breaker/terminal side.
- Route the cutoff output as two direct protected branches: one to the relay feed and one to the MIDI common feed. Do not route the relay feed through the MIDI bank.
- Treat the inboard engine/LHD steering side as a keep-clear/service envelope except for protected cable clips and pass-through routing.
- Default to this widened raised front access-ladder split layout. Do not make a one-piece side carrier unless the filled cavity map proves it is smaller, clear, serviceable, and not in the engine-side envelope.

## Image-Based Chassis Pickup Estimate

The May 14 no-battery bay photo shows the existing battery pocket sitting well above the chassis rail and slightly wing-side/outboard from the visible chassis pickup line. Use these only as first cardboard/wood mock-up targets:

- Target tray support plane: keep the compact tray in the existing battery pocket plane, about `170-190 mm` above the top of the chassis rail. Use `180 mm` as the first mock-up rise from chassis top to tray underside.
- Vertical adjustment allowance: build the upright bridge with slotted/stepped adjustment from `150-210 mm` chassis-top-to-tray-underside so the tray can be lowered if bonnet/terminal clearance is tight or raised if the relay tray/cable exit needs more space.
- Sideways adjustment allowance: set the tray centre about `120 mm` wing-side/outboard from the chassis pickup centreline, with `90-150 mm` usable side adjustment. This keeps the battery in the original pocket rather than moving it engine-side.
- Chassis saddle allowance: mock the chassis fixing as a 4 mm mild-steel saddle with a top cap over the rail and two down-legs, not a flat plate beside the rail. Use a nominal `220 x 230 mm` flat pattern (`70 mm` near leg, measured rail-top cap nominal `90 mm`, `70 mm` far leg) until the actual rail width is measured.
- Battery/electrical package hold: mock up the full `318 x 180 x 230 mm` standard battery envelope plus removable hold-down, then add the widened front access-ladder cards. Do not final-drill the pickup or upright until the battery lift-out path, battery top, bonnet, fan/radiator, steering/hose, tool access, relay cover removal, three sized relay exit clusters, cutoff lug sweeps, and MIDI five-output cable fanout all pass.

## Parts In This Package

1. `battery_stand_compact_top_tray_rev_b` - 3 mm mild-steel compact battery tray/deck with clamp and cable-clip zones.
2. `battery_stand_compact_single_chassis_pickup_rev_b` - 4 mm mild-steel formed chassis saddle for the one chassis pickup location.
3. `battery_stand_compact_single_mount_upright_rev_b` - 4 mm mild-steel upright bridge side plate; make a mirrored pair if the mock-up needs side-to-side stiffness.
4. `battery_stand_compact_hold_down_crossbar_rev_b` - compact battery hold-down crossbar template.
5. `battery_power_compact_front_service_rail_rev_b` - 3 mm mild-steel widened `660 x 310 mm` front/radiator-side access ladder for the outboard relay tray, plastic underlay, three sized relay wire-exit clusters, 80 mm wire gutter, seated MIDI output comb/backplate, enlarged double-wire MIDI access hole, and separated top-front MIDI/cutoff shelf tabs aligned from the battery leading-edge datum.
6. `battery_power_compact_cutoff_tab_rev_b` - folded aluminium 100A breaker/cutoff base/guard with upward lips, top-front placement basis aligned from the battery leading-edge datum.

## 3D Visualisation

- `battery_power_carrier_mount_rev_a_3d_visualisation.svg` is the static compact fabrication-read view.
- `battery_power_carrier_mount_rev_a_3d_visualisation.html` is the interactive compact fabrication-read view.
- `battery_power_carrier_mount_rev_a_assembled_3d_visualisation.svg` is the static attached compact assembly view.
- `battery_power_carrier_mount_rev_a_assembled_3d_visualisation.html` is the interactive attached compact assembly view showing the formed chassis saddle over the rail, upright bridge, `340 x 265 mm` tray, standard battery envelope, removable hold-down, vertical battery lift-out clearance, outboard-access covered Relay Rev C tray with three sized wire-exit clusters and plastic rear guard/underlay ahead of the folded metal tray, top-front MIDI Rev C shelf with seated output comb/backplate and enlarged double-wire access hole, folded top-front cutoff base/guard with upward lips, MIDI/cutoff starts aligned to the battery leading-edge datum, keep-clear engine/LHD side envelope, and direct cutoff-to-relay / cutoff-to-MIDI cable paths installed together.

## Package Relationship

- The relay hardware uses the known Relay Rev C folded tray (`320 x 220 mm` finished face; `360 x 255 mm` flat pattern) plus the flat plastic rear guard/underlay (`280 x 185 mm`) in front of the folded metal tray. The latest photo shows a covered black relay enclosure, so the visual model now treats the internals as hidden, keeps the cover face reachable from the outboard/front service direction, and reserves three sized loom clusters rather than one generic loom slot.
- The MIDI holder hardware uses `midi5_plate_mount_rev_c` (`190 x 150 mm`) and `midi5_holder_subplate_rev_c` (`140 x 85 mm`). This is an open plate/subplate assembly with one common feed side and five heavy output cables on the opposite side, so the current route is a separated shallow top-front shelf whose leading edge aligns to the battery leading-edge datum, with a seated output comb/backplate and an 80 mm cable fanout/gutter on the same raised access ladder. One output is marked with an enlarged pass-through for two wires.
- The older `electrical_modules_rev_a` package includes bent/flanged aluminium tray/box concepts, but remains reference/fallback only.
- The cutoff folded base/guard gets only a pilot/opening allowance until the actual 100A breaker body size, mounting-hole centres, reset-lever access, terminal-stud spacing, and cable-lug sweep are measured. The lips fold upward to protect the breaker/lug envelope, not downward as hidden stiffeners.

## Compact Packaging Hold

- The latest battery-bay photos show no obvious full-size electrical mounting face beside the battery. The previous large sideways carrier is rejected for the active package.
- Before cutting final steel, make cardboard cards for the compact tray (`340 x 265 mm`), standard battery envelope (`318 x 180 x 230 mm`), widened front access ladder (`660 x 310 mm`), Relay Rev C folded tray (`320 x 220 mm` plus return/depth blocks), covered relay box face/removal space, relay plastic rear guard/underlay (`280 x 185 mm`), three relay wire-exit cluster cards with the sizes above, MIDI Rev C top shelf (`190 x 150 mm` plus subplate/depth), seated MIDI output comb/backplate/gland strip, enlarged double-wire MIDI output access hole, folded cutoff base/guard (`170 x 110 mm` finished face / `210 x 150 mm` flat pattern / `20 mm` upward lips), one MIDI common feed lug, five MIDI output cable lugs, and battery case.
- Test the front/radiator-side space first, with the relay tray shifted to the outboard/access edge and the MIDI/cutoff cards separated on the top-front shelf but both started from the battery leading-edge datum. Use inboard/lower/outboard space only after steering, hose, heat, splash, bonnet, and battery-service clearances are proven.
- Reject any placement that enters the engine/LHD steering shaft/box/service sweep, hydraulic line path, alternator service space, bonnet clearance, radiator/fan envelope, or safe battery terminal service area.

## Battery-Cavity Mapping Plan

Use the battery as the fixed exclusion block before placing any relays, MIDI fuses, or cutoff breaker. The current package uses a standard N70/27-class envelope up to `318 x 180 x 230 mm`; verify it against the actual installed battery and update the map if the real battery differs.

- Establish datums with the vehicle facing forward: front/radiator side, rear/firewall side, inboard engine/LHD steering side, outboard wing side, and vertical bonnet clearance.
- Put the battery or a full-size battery box in the tray and mark a no-go block around it: battery case, hold-down, terminals, terminal boots, and cable lug bend radius.
- Measure the cavity in slices at tray height, mid-battery height, battery-top height, and bonnet/terminal-service height.
- Record available rectangles to the front, inboard/engine side, outboard/wing side, and below the tray. Do not count space that requires the battery to be removed for fuse or relay service.
- Trial the known templates in cardboard in the active order: outboard/access Relay Rev C folded tray `320 x 220 mm`, covered relay box face/removal clearance, relay plastic rear guard/underlay `280 x 185 mm` ahead of the metal tray, three relay wire-exit cluster cards with relative offsets/sizes, MIDI Rev C open plate `190 x 150 mm` on the separated shallow top-front shelf started from the battery leading-edge datum, seated MIDI output comb/gland strip with one enlarged double-wire access hole, folded cutoff base/guard `170 x 110 mm` finished face / `210 x 150 mm` flat pattern with `20 mm` upward lips started from the same battery datum at the top/front accessible corner, one MIDI common feed lug, five MIDI output lugs, plus their real depth and cable lug sweep.
- Treat the front/radiator-side volume as the first candidate because both battery-in and battery-out photos suggest more usable space forward than sideways.
- Treat the inboard/engine-side gap as a keep-clear zone by default. It must stay clear of LHD steering shaft/box/service motion, hydraulic lines, hoses, alternator service, engine movement, and heat.
- Treat the lower void as cable support or shielded junction space only unless dry, serviceable, and protected from splash and heat.
- Split the layout by front elevation: relay outboard on the front access edge, MIDI on a separated top-front shelf started from the battery leading-edge datum, cutoff at the top/front accessible corner started from the same datum, cutoff output stacked ring-lug splitter feeding relay and MIDI directly, five MIDI branch outputs on the same side of the MIDI bank through the seated comb, one enlarged double-wire output pass-through, and P-clips on the stand/ladder rather than the engine-side gap.

Detailed measurement rows are in `cavity_mapping_plan.csv`.

## Materials

- Stand top tray/deck, widened raised front access ladder, top-front shelf tabs, and small steel tabs: `3.0 mm` mild steel.
- Tray/access-ladder angle-first stock: `25 x 25 x 3 mm` or `30 x 30 x 3 mm` pre-formed `90-degree` mild-steel angle for tray perimeter/upstands, ladder frame rails, shelf rails, and cable/P-clip tabs.
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
- Compact holder cards: outboard-access covered Relay Rev C tray, relay plastic rear guard/underlay, sized relay exit-cluster cards, MIDI Rev C top-front shelf, folded cutoff top/front base/guard with upward lips, battery-leading-edge datum line for MIDI/cutoff starts, direct cutoff-to-relay / cutoff-to-MIDI cable-lug depth, seated MIDI output comb/backplate, and five MIDI output cable bends must fit the measured front/radiator volume without touching the steering-side service envelope.
- Single chassis saddle: rail top width, leg depth, through-bolt pitch, crush-tube need, stand-off height, upright bridge height, side-jog from saddle centreline to tray centreline, and access for tools. Current image-based target is `180 mm` rise with `90-150 mm` wing-side/outboard adjustment.
- 100A breaker/cutoff: body length/width/height, mounting hole centres, reset lever access, terminal stud size/spacing, and cable-lug sweep.
- Relay Rev C base: final outboard/front service orientation, cover removal space, plastic-underlay order, standoff height, seal direction, and loom exit direction.
- MIDI Rev C base/subplate: final top-front shelf feed/output orientation, direct cutoff common-feed bend radius, and all five branch-output bend radii.
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
            "notes": "Compact 340 x 265 battery tray/deck for standard N70/27-class envelope up to 318 x 180 x 230, with removable hold-down slots, low end stops, battery lift-out path, and cable clip holes. Electrical holders mount on the raised front/radiator-side service ladder, not on engine-side panels.",
        },
        {
            "part_id": "BPCC-FRONT-RAIL-001",
            "drawing": "battery_power_compact_front_service_rail_rev_b.dxf",
            "qty": "1",
            "material": "mild steel",
            "thickness_mm": "3.0",
            "status": "cavity_map_required",
            "notes": "Widened 660 x 310 front/radiator-side access ladder: covered Relay Rev C mounts outside the battery footprint on the outboard/access edge with plastic rear guard/underlay ahead of the folded metal tray, three sized relay wire-exit cluster keepouts, separated top-front shelf/base pickups starting from the battery leading-edge datum, 80 mm cable gutter, seated MIDI output comb/backplate, enlarged double-wire MIDI output access hole, cutoff output splitter, direct relay/MIDI feeds, and five heavy MIDI output cables.",
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
            "acceptance_check": "Compact stand tray accepts the actual installed battery or the 318 x 180 x 230 standard envelope, retains it with a removable hold-down, and clears terminal clamp, vertical lift-out path, bonnet, radiator, fan/belt, LHD steering path, and alternator service sweep.",
            "required_evidence": "Cardboard/top-tray photo with battery installed and ruler in frame, plus a hold-down-removed lift-out clearance photo.",
        },
        {
            "check_id": "BPCC-CHECK-001A",
            "stage": "compact_cavity_cards",
            "acceptance_check": "Compact holder cards prove the Rev F access-ladder stack: standard battery envelope 318 x 180 x 230 with removable hold-down and lift-out clearance, covered Relay Rev C folded tray 320 x 220 shifted outside the battery footprint to the outboard/front access edge, relay plastic rear guard/underlay 280 x 185 ahead of the folded metal tray, three relay wire-exit clusters with offsets/sizes, MIDI open plate 190 x 150 on a separated top-front shelf with seated output comb/backplate and enlarged double-wire access hole, folded cutoff base/guard 170 x 110 finished face / 210 x 150 flat pattern with 20 mm upward lips, both MIDI and cutoff starts aligned to the battery leading-edge datum, direct cutoff-to-relay and cutoff-to-MIDI cable depth, and five heavy MIDI output cable bends clear of LHD steering/hose/fan/bonnet/battery service envelopes.",
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
            "acceptance_check": "Folded Relay Rev C tray, relay plastic underlay, MIDI open plate/subplate, seated MIDI output comb/backplate, and master cutoff folded base/guard all mount to the widened raised front/radiator-side access ladder without forced cable bends, floating cable guides, live-stud exposure, relay-cover obstruction, battery removal obstruction, or use of the inboard engine-side gap as a component face.",
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
            "w_mm": "318",
            "h_mm": "180",
            "z_height_mm": "230 standard envelope reference; measure actual battery",
            "notes": "Standard N70/27-class battery envelope inside compact 340 x 265 tray; final footprint, full case height, terminal side, and hold-down path follow actual battery.",
        },
        {
            "zone": "compact_top_tray",
            "x_mm": "0",
            "y_mm": "0",
            "w_mm": "340",
            "h_mm": "265",
            "z_height_mm": "3 mm steel tray/deck plus battery mat",
            "notes": "Compact battery support tray only; includes removable hold-down and low end-stop basis. Do not use the tray skin as a large electrical backplane.",
        },
        {
            "zone": "relay_rev_c_outboard_access_card",
            "x_mm": "front face, shifted outboard/wing-side from battery footprint",
            "y_mm": "outboard/front access edge of raised ladder",
            "w_mm": "320",
            "h_mm": "220",
            "z_height_mm": "finished face plus 20 mm side/bottom returns, 15 mm top return, 280 x 185 plastic underlay, covered relay box and loom depth measurement hold",
            "notes": "Active candidate is shifted outside the battery footprint to the outboard/front access edge so the covered relay box can be opened/reached with the battery installed and the inboard engine/LHD side stays clear. Reserve the three sized relay wire-exit clusters listed below.",
        },
        {
            "zone": "relay_upper_red_harness_cluster",
            "x_mm": "relay centre X-62",
            "y_mm": "relay centre Y+110",
            "w_mm": "136",
            "h_mm": "24",
            "z_height_mm": "cluster depth 34 mm at relay centre Z-58; keepout 164 x 52 x 54",
            "notes": "Upper red harness cluster modelled as a sized block on the covered relay box. Keep the matching clearance gutter open before final hole placement.",
        },
        {
            "zone": "relay_right_braided_loom_cluster",
            "x_mm": "relay centre X+164",
            "y_mm": "relay centre Y-10",
            "w_mm": "42",
            "h_mm": "118",
            "z_height_mm": "cluster depth 42 mm at relay centre Z-52; keepout 72 x 156 x 70",
            "notes": "Side braided loom boot/cluster modelled on the relay-box side with service-loop clearance. Confirm boot direction against the physical relay box before drilling.",
        },
        {
            "zone": "relay_lower_auxiliary_cluster",
            "x_mm": "relay centre X-96",
            "y_mm": "relay centre Y-110",
            "w_mm": "96",
            "h_mm": "24",
            "z_height_mm": "cluster depth 30 mm at relay centre Z-60; keepout 132 x 52 x 54",
            "notes": "Lower auxiliary/secondary loom relief modelled separately from the upper red harness and side braided loom so it is not swallowed by a generic relay cable slot.",
        },
        {
            "zone": "midi_rev_c_top_front_shelf_card",
            "x_mm": "leading edge aligned to battery leading-edge datum",
            "y_mm": "separated top-front shelf behind the cutoff card",
            "w_mm": "190",
            "h_mm": "150",
            "z_height_mm": "known 190 x 150 plate plus 140 x 85 subplate, seated output comb/backplate, and holder/cable depth",
            "notes": "Open plate/subplate assembly on a shallow top-front shelf; keep one direct cutoff common feed into one side, five heavy output cables from the opposite side through a seated comb/gland strip, one enlarged double-wire output access hole, and do not mount it on the engine-side face.",
        },
        {
            "zone": "cutoff_top_front_access_card",
            "x_mm": "leading edge aligned to battery leading-edge datum",
            "y_mm": "separated top-front shelf ahead of the MIDI card, not engine-side",
            "w_mm": "170",
            "h_mm": "110",
            "z_height_mm": "210 x 150 mm flat pattern, 170 x 110 mm finished face, 20 mm upward guard lips, plus 100A breaker body/reset lever/stud height measurement hold",
            "notes": "Folded aluminium base/guard at the most accessible top/front position; lips bend upward around the 100A breaker/terminal side. Route cutoff output directly to both covered relay and MIDI common feed. Open final mounting holes after measuring the real breaker and lug sweep.",
        },
        {
            "zone": "front_radiator_service_ladder_spine",
            "x_mm": "site_fit",
            "y_mm": "site_fit",
            "w_mm": "660",
            "h_mm": "310",
            "z_height_mm": "component and cable-lug depth measurement hold",
            "notes": "Vehicle-side widened raised ladder for the front stack; mounts relay outboard enough for cover service and provides top-front shelf/tab pickups, three sized relay wire-exit clearances, seated MIDI output comb/gland support, double-output access hole, cutoff splitter, battery-aligned MIDI/cutoff datum, and wire-gutter P-clips for MIDI, cutoff, direct relay/MIDI feeds, and five MIDI output cables.",
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
            "datum_basis": "Current package standard N70/27-class battery envelope 318 x 180 x 230 mm; verify actual installed battery before final layout.",
            "measurements_to_capture": "Actual battery length, width, case height, terminal height, terminal orientation, hold-down path, vertical lift-out path, and cable-lug bend radius.",
            "template_or_tool": "Battery installed or 318 x 180 x 230 cardboard/foam battery block plus tape/ruler.",
            "pass_rule": "Battery datum is marked on tray/frame before any relay, MIDI, cutoff, or cable support location is chosen.",
            "notes": "If the real battery exceeds the 318 x 180 x 230 mm envelope or terminal height changes the bonnet hold, update component_layout.csv and redraw any cardboard templates before cutting steel.",
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
            "template_or_tool": "Widened front access-ladder card set: 660 x 310 ladder, Relay Rev C 320 x 220 outboard/front vertical tray with return/depth block and covered box removal clearance, relay plastic rear guard/underlay 280 x 185, three sized relay wire-exit cards, MIDI 190 x 150 separated top-front shelf started from the battery leading-edge datum, seated MIDI output comb/gland strip, enlarged double-wire MIDI output hole, folded cutoff base/guard 170 x 110 finished face / 210 x 150 flat pattern / 20 mm upward lips started from the same battery datum, one MIDI common lug, five MIDI output lugs with 40-80 mm depth blocks, and an 80 mm minimum wire gutter.",
            "pass_rule": "Active candidate only if the outboard relay cover face, upper/side/lower relay exit clusters, battery-aligned top-front MIDI/cutoff shelves, cutoff splitter, direct cutoff-to-relay / cutoff-to-MIDI feeds, and five MIDI output cables fit with cable bends, no fan/radiator contact, bonnet clearance, battery lift-out clearance, and service access with battery installed.",
            "notes": "The May 15 component photos show a covered relay box with three exit areas and a crowded five-output MIDI cable side; this package makes a widened front access-ladder placement the active design.",
        },
        {
            "step_id": "CAV-004A",
            "zone_or_task": "chassis_pickup_height_and_side_jog",
            "datum_basis": "Top of visible chassis rail, chassis pickup centreline, and existing battery pocket/tray plane from the May 14 no-battery bay image.",
            "measurements_to_capture": "Chassis-top to tray-underside rise, saddle cap width over the rail, leg depth down both rail sides, through-bolt access, chassis pickup centreline to tray centreline side offset, and whether the upright bridge clears hose/steering/fan/radiator paths.",
            "template_or_tool": "Cardboard/plywood mock-up: 340 x 265 tray plane at 180 mm above chassis top with 318 x 180 x 230 battery block, removable hold-down, and lift-out path, plus a saddle card over both chassis sides and slotted side-jog trial marks at 90, 120, and 150 mm wing-side/outboard from the chassis pickup centreline.",
            "pass_rule": "Active estimate passes only if the formed saddle sits over both rail sides, the battery remains in the original pocket, bonnet/terminal clearance remains safe, and outboard relay plus battery-aligned MIDI/cutoff front-ladder cards fit without moving into the engine/LHD side envelope.",
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
            "measurements_to_capture": "Serviceable front-ladder rectangle, relay cover removal path, relay exit-cluster positions/sizes, top-front shelf height, direct cable length from cutoff to MIDI and relay, harness exit length from relay, and five MIDI output bend radii.",
            "template_or_tool": "Component cards in active stack order: Relay Rev C outboard/front 320 x 220 with 280 x 185 plastic underlay ahead of the metal tray and covered box clearance, three sized relay exit cards, MIDI top-front 190 x 150 started from the battery leading-edge datum, folded cutoff base/guard top-front 170 x 110 finished face / 210 x 150 flat pattern / 20 mm upward lips started from the same datum, plus depth/lug blocks and an 80 mm wire-gutter strip.",
            "pass_rule": "Choose the widened front access-ladder layout unless measured front space fails. Reopen split side/lower placement only with evidence that it is smaller, serviceable, and clear.",
            "notes": "Preferred order: cutoff top/front accessible and battery-aligned, direct branch to MIDI common, direct branch to covered relay feed, outboard relay cover access, five MIDI output cables through the seated comb on one side, P-clips on stand/ladder.",
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
