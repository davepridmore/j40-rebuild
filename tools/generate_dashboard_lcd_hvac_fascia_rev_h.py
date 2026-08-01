from __future__ import annotations

import csv
import math
import shutil
import textwrap
import zipfile
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle


ROOT = Path("/Users/davidpridmore/IdeaProjects/J40")
OUT = ROOT / "data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_h"
DELIVERABLE = ROOT / "deliverables/fabrication_packages/dashboard_lcd_hvac_fascia_rev_h.zip"
ASSEMBLED_BASE_PHOTO = ROOT / "photos/20260317_165113.jpg"
BARE_BASE_PHOTO = ROOT / "photos/20260413_040719.jpg"
ASSEMBLED_VIS_SOURCE = Path(
    "/Users/davidpridmore/.codex/generated_images/019fb8d3-8269-7eb0-b457-d806a3cefbd4/exec-2dc93f5f-cd29-452e-b333-f501e734231d.png"
)
BARE_VIS_SOURCE = Path(
    "/Users/davidpridmore/.codex/generated_images/019fb8d3-8269-7eb0-b457-d806a3cefbd4/exec-71453810-0872-46ae-a8d1-2791b0491835.png"
)
SWITCH_REFERENCE_SOURCE = Path(
    "/var/folders/2r/rbnydbl91t9_jcjfhssspzqw0000gn/T/codex-clipboard-ff07d5a4-279b-4983-a817-caf5c2c9b1ad.png"
)
CORRECTED_ASSEMBLED_VIS_RELATIVE = Path(
    "layout_variants_20260801/layout_b_column_v4_clearance_assembled.png"
)
COLUMN_V5_ASSEMBLED_VIS_RELATIVE = Path(
    "layout_variants_20260801/layout_b_column_v5_clear_assembled.png"
)
COLUMN_V5_STRAIGHT_VIS_RELATIVE = Path(
    "layout_variants_20260801/layout_b_column_v5_straight_on.png"
)
COLUMN_V6_ASSEMBLED_VIS_RELATIVE = Path(
    "layout_variants_20260801/layout_b_column_v6_switches_clear_assembled.png"
)
COLUMN_V6_STRAIGHT_VIS_RELATIVE = Path(
    "layout_variants_20260801/layout_b_column_v6_switches_straight_on.png"
)
LAYOUT_VARIANTS_README_RELATIVE = Path("layout_variants_20260801/README.md")

# Rev H is a full-width, one-piece visible face. Its normal lower edge is Y=50.
# The two end vents remain high. The two inner vents are deliberately lower and
# sit in identical local rounded pods, allowing their rear necks and elbows to
# project deeper without increasing the complete dashboard height. A separate
# shallow local channel carries the compact controls at the extreme right.
# These coordinates remain a quotation /
# template datum only; the physical vehicle trace at M1 controls the perimeter
# and every preserved structural edge.
PANEL_W = 1260.0
PANEL_H = 220.0
PANEL_CENTRELINE_X = PANEL_W / 2
MAIN_LOWER_Y = 50.0
PANEL_MIN_Y = -35.0
MATERIAL_THICKNESS = 1.5

# A public early-model reproduction-panel listing gives 1400 x 250 x 100 mm.
# That is useful as a broad vendor product envelope only: it is stated to the
# nearest centimetre and is not an installed RHD face drawing, perimeter trace,
# bend-line schedule or coordinate datum.  It therefore cannot replace M1.
PUBLIC_REPRO_PANEL_ENVELOPE = (1400.0, 250.0, 100.0)
PUBLIC_REPRO_PANEL_URL = "https://rebornfj.com/product-detail/for-toyota-land-cruiser-fj40-fj45_26995.html"
TOYOTA_EPC_URL = "https://www.megazip.net/zapchasti-dlya-avtomobilej/toyota/land-cruiser-38286/fj40-55808/fj40lv-kw-936553/instrument-panel-glove-compartment-18026590"

# A 9-inch / 16:9 active-image *reference* centred on the fascia.  The locally
# available Sehgal universal 9-inch unit does not publish chassis, cutout or
# mount dimensions: its manufacturer/supplier drawing and a physical sample
# supersede every aperture, bezel and rear-body nominal below.
LCD_ACTIVE_W = 199.2
LCD_ACTIVE_H = 112.1
LCD_CX = PANEL_CENTRELINE_X
LCD_CY = 144.0
LCD_BEZEL_W, LCD_BEZEL_H = 224.0, 136.0
LCD_APERTURE_W, LCD_APERTURE_H = 202.0, 115.0
LCD_BEZEL = (LCD_CX - LCD_BEZEL_W / 2, LCD_CY - LCD_BEZEL_H / 2, LCD_BEZEL_W, LCD_BEZEL_H)
LCD_APERTURE = (LCD_CX - LCD_APERTURE_W / 2, LCD_CY - LCD_APERTURE_H / 2, LCD_APERTURE_W, LCD_APERTURE_H)
LCD_ACTIVE = (
    LCD_CX - LCD_ACTIVE_W / 2,
    LCD_CY - LCD_ACTIVE_H / 2,
    LCD_ACTIVE_W,
    LCD_ACTIVE_H,
)

# Pakistan-cost-conscious generic silver/chrome ABS outlet family. Published
# listing dimensions are face Ø87 / panel opening Ø75, but generic variants
# differ in spigot and retention details.  The cut is explicitly HOLD until one
# matched four-piece batch has been received and calipered at M7.
# The end vents sit high and close to the usable ends of the front face, never
# in the folded side returns. The inner pair is centred symmetrically about the
# LCD and lowered until each complete Ø87 face sits below the LCD bezel. Their
# identical pods are the only deep downward extensions.
VENT_FACE_DIAMETER = 87.0
VENT_CORE_DIAMETER = 69.0
VENT_NECK_DIAMETER = 75.0
OUTER_VENT_CENTRE_INSET = 50.0
INNER_VENT_CENTRE_OFFSET = 166.0
OUTER_VENT_TOP_DATUM_Y = LCD_BEZEL[1] + LCD_BEZEL[3]
OUTER_VENT_CENTRE_Y = OUTER_VENT_TOP_DATUM_Y - VENT_FACE_DIAMETER / 2
INNER_VENT_CENTRE_Y = 20.0
INNER_VENT_POD_HALF_W = 56.0
INNER_VENT_POD_BOTTOM_Y = PANEL_MIN_Y
MIN_INNER_VENT_LCD_VISIBLE_GAP = 8.0
MIN_STATIC_REAR_CLEARANCE = 10.0
MIN_MOVING_COLUMN_CLEARANCE = 20.0
MIN_DUCT_ROUNDNESS_PERCENT = 90.0
# V4 (top-right outlet) remains at the far end of the face.  Its lower rim is
# 19 mm above the nominal top of the compacted control-bank envelope.  That is a
# useful *visual* datum from the accepted straight-on overlay, not evidence of
# a safe selector-head or rear-duct clearance.  Do not move it farther right:
# the visible rim/end land is already 6.5 mm and the Ø75 reference cut/end land
# is already 12.5 mm.  Actual head/label geometry must prove the larger visible
# separation below, and the actual retainer/neck/elbow must miss the contact
# stacks, terminals and wiring at full depth.
V4_CONTROL_ENVELOPE_NOMINAL_GAP = 19.0
MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE = 20.0
VENT_CENTRES = (
    (OUTER_VENT_CENTRE_INSET, OUTER_VENT_CENTRE_Y),
    (PANEL_CENTRELINE_X - INNER_VENT_CENTRE_OFFSET, INNER_VENT_CENTRE_Y),
    (PANEL_CENTRELINE_X + INNER_VENT_CENTRE_OFFSET, INNER_VENT_CENTRE_Y),
    (PANEL_W - OUTER_VENT_CENTRE_INSET, OUTER_VENT_CENTRE_Y),
)

# Reference envelopes only. Perspective and missing scale datums prevent the
# owner photos from becoming a dimensional drawing. The retained parts and
# factory openings are directly traced at M2/M3; these nominal envelopes exist
# only to test the surrounding layout and are never CNC release geometry.
GLOVEBOX_ENVELOPE = (152.0, 65.0, 210.0, 145.0)
SPEEDO_ENVELOPE = (785.0, 88.0, 290.0, 127.0)

# The RHD steering column passes through the lower edge directly beneath the
# retained cluster. This nominal relief and swept keep-out make the packaging
# constraint explicit, but M1/M3/M9 must replace them with a direct vehicle
# trace of the installed column, shroud, stalks, bracket and full movement.
STEERING_COLUMN_AXIS_X = SPEEDO_ENVELOPE[0] + SPEEDO_ENVELOPE[2] / 2
STEERING_COLUMN_RELIEF_HALF_W = 65.0
STEERING_COLUMN_RELIEF_RISE = 32.0
STEERING_COLUMN_KEEP_OUT = (
    STEERING_COLUMN_AXIS_X - STEERING_COLUMN_RELIEF_HALF_W,
    0.0,
    STEERING_COLUMN_RELIEF_HALF_W * 2,
    105.0,
)

# Exactly eight visible stations occupy a compact two-row bank at the extreme
# right: seven maintained selectors plus a separate hazard. Rev H V6 compacts
# the columns to 40 mm pitch and lowers both rows by 10 mm, centring the group
# within the existing Y=3 local channel without increasing dashboard height.
# Both rows remain wholly right of the nominal steering-column swept keep-out.
# Flange, lever sweep, anti-rotation, contact-block, duct and hand-clearance
# checks remain M6/M8/M9 HOLD until the actual parts are mocked up 1:1.
CONTROL_BANK = (1104.0, 3.0, 151.0, 103.0)

SELECTOR_DIAMETER = 22.5
HAZARD_DIAMETER = 16.0
CONTROL_COLUMNS = (1120.0, 1160.0, 1200.0, 1240.0)
CONTROL_TOP_Y = 78.0
CONTROL_BOTTOM_Y = 20.0
CONTROL_LABEL_Y_OFFSET = 19.0
SELECTOR_REAR_ENVELOPE = 68.0
V4_NOMINAL_SELECTOR_HEAD_CLEARANCE = (
    OUTER_VENT_CENTRE_Y
    - VENT_FACE_DIAMETER / 2
    - (CONTROL_TOP_Y + SELECTOR_DIAMETER / 2)
)
CONTROL_MAP = (
    ("S1", "WIPERS", "3-position maintained", "OFF / LOW / HIGH", "wiper interface; preserve automatic park"),
    ("S2", "LIGHTS", "3-position maintained", "OFF / SIDE / HEAD", "master lighting request; retained dip selects T1/T2"),
    ("S3", "SPOTS", "2-position maintained", "OFF / ON", "T5 spot-lamp relay command"),
    ("S4", "AUX.", "2-position maintained", "OFF / ON", "B2 reserved accessory relay command"),
    ("S5", "BLOWER", "3-position maintained", "OFF / LOW / HIGH", "low-current request to measured HVAC resistor/relay/PWM controller; never blower-motor current"),
    ("S6", "A/C", "2-position maintained", "OFF / ON", "B1 compressor request through evaporator thermostat/freeze control and trinary/pressure safeties"),
    ("S7", "ENGINE", "2-position maintained", "RUN / STOP", "low-current validated fuel-stop interface; key OFF authoritative; manual stop cable fallback"),
    ("S8", "HAZARD", "separate red pushbutton", "OFF / FLASH", "existing hazard/flasher circuit"),
)


def control_positions() -> list[tuple[float, float]]:
    """Top row S1-S4, then bottom row S5-S8, each left-to-right."""
    return [
        *((control_x, CONTROL_TOP_Y) for control_x in CONTROL_COLUMNS),
        *((control_x, CONTROL_BOTTOM_Y) for control_x in CONTROL_COLUMNS),
    ]


def steering_column_relief_points(segments: int = 18) -> list[tuple[float, float]]:
    """Right-to-left upper semicircle cut into the lower fascia edge."""
    return [
        (
            STEERING_COLUMN_AXIS_X + STEERING_COLUMN_RELIEF_HALF_W * math.cos(math.pi * index / segments),
            MAIN_LOWER_Y + STEERING_COLUMN_RELIEF_RISE * math.sin(math.pi * index / segments),
        )
        for index in range(segments + 1)
    ]


def inner_vent_pod_lower_points(center_x: float, segments: int = 18) -> list[tuple[float, float]]:
    """Right-to-left half-ellipse forming one local lower vent pod."""
    depth = MAIN_LOWER_Y - INNER_VENT_POD_BOTTOM_Y
    return [
        (
            center_x + INNER_VENT_POD_HALF_W * math.cos(math.pi * index / segments),
            MAIN_LOWER_Y - depth * math.sin(math.pi * index / segments),
        )
        for index in range(segments + 1)
    ]


def outer_profile_points() -> list[tuple[float, float]]:
    """Clockwise nominal outline with two vent pods and local cut-outs.

    The normal face ends at Y=50. The fascia rises around the RHD steering
    column in a radiused U-shaped relief beneath the retained cluster. The two
    inner-vent pods dip locally to Y=-35, while the compact two-row control bank
    at the extreme right extends locally to Y=3. Exact perimeter geometry
    remains M1/M3/M7/M9 HOLD.
    """
    left_inner_x = VENT_CENTRES[1][0]
    right_inner_x = VENT_CENTRES[2][0]
    control_x0, _, control_w, _ = CONTROL_BANK
    control_x1 = control_x0 + control_w
    return [
        (0, PANEL_H), (PANEL_W, PANEL_H),
        (PANEL_W, 12), (control_x1, 3), (control_x0, 3),
        (control_x0 - 8, 12), (control_x0 - 8, MAIN_LOWER_Y),
        *steering_column_relief_points(),
        (right_inner_x + INNER_VENT_POD_HALF_W, MAIN_LOWER_Y),
        *inner_vent_pod_lower_points(right_inner_x),
        (left_inner_x + INNER_VENT_POD_HALF_W, MAIN_LOWER_Y),
        *inner_vent_pod_lower_points(left_inner_x),
        (0, MAIN_LOWER_Y),
    ]


def glovebox_profile_points() -> list[tuple[float, float]]:
    return [(152, 75), (162, 65), (342, 65), (362, 78), (362, 190), (345, 208), (172, 210), (152, 195)]


def speedometer_profile_points() -> list[tuple[float, float]]:
    """Nominal visual envelope echoing the retained J40 cluster.

    This is deliberately not CNC geometry. The original cluster has one broad
    upper speedometer window and lower auxiliary windows; M3 direct transfer of
    the actual housing, mounts and rear stack controls every production feature.
    """
    x, y, w, h = SPEEDO_ENVELOPE
    shoulder = 15.0
    return [
        (x, y), (x, y + h - 28), (x + shoulder, y + h - 8),
        (x + 38, y + h), (x + w - 38, y + h),
        (x + w - shoulder, y + h - 8), (x + w, y + h - 28), (x + w, y),
    ]


def speedometer_window_rects() -> tuple[tuple[float, float, float, float], ...]:
    """Schematic internal windows derived from the nominal transfer envelope."""
    x, y, w, h = SPEEDO_ENVELOPE
    lower_w = (w - 44.0) / 2
    return (
        (x + 38.0, y + 55.0, w - 76.0, h - 69.0),
        (x + 16.0, y + 13.0, lower_w, 32.0),
        (x + 28.0 + lower_w, y + 13.0, lower_w, 32.0),
    )


def rounded_rect_points(x: float, y: float, w: float, h: float, radius: float, segments: int = 8) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for cx, cy, start in (
        (x + w - radius, y + radius, -90),
        (x + w - radius, y + h - radius, 0),
        (x + radius, y + h - radius, 90),
        (x + radius, y + radius, 180),
    ):
        for index in range(segments + 1):
            angle = math.radians(start + index * 90 / segments)
            points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return points


def dxf_header() -> list[str]:
    return ["0", "SECTION", "2", "HEADER", "9", "$INSUNITS", "70", "4", "0", "ENDSEC", "0", "SECTION", "2", "ENTITIES"]


def dxf_line(layer: str, x1: float, y1: float, x2: float, y2: float) -> list[str]:
    return ["0", "LINE", "8", layer, "10", f"{x1:.3f}", "20", f"{y1:.3f}", "30", "0", "11", f"{x2:.3f}", "21", f"{y2:.3f}", "31", "0"]


def dxf_circle(layer: str, x: float, y: float, radius: float) -> list[str]:
    return ["0", "CIRCLE", "8", layer, "10", f"{x:.3f}", "20", f"{y:.3f}", "30", "0", "40", f"{radius:.3f}"]


def dxf_text(layer: str, x: float, y: float, height: float, value: str) -> list[str]:
    return [
        "0", "TEXT", "8", layer, "10", f"{x:.3f}", "20", f"{y:.3f}", "30", "0",
        "40", f"{height:.3f}", "1", value, "72", "1", "73", "2",
        "11", f"{x:.3f}", "21", f"{y:.3f}", "31", "0",
    ]


def dxf_lwpoly(layer: str, points: list[tuple[float, float]], closed: bool = True) -> list[str]:
    result = ["0", "LWPOLYLINE", "8", layer, "90", str(len(points)), "70", "1" if closed else "0"]
    for x, y in points:
        result += ["10", f"{x:.3f}", "20", f"{y:.3f}"]
    return result


def write_dxf(path: Path, entities: list[list[str]]) -> None:
    rows = dxf_header()
    for entity in entities:
        rows += entity
    rows += ["0", "ENDSEC", "0", "EOF"]
    path.write_text("\n".join(rows) + "\n", encoding="ascii")


def add_component_geometry(entities: list[list[str]]) -> None:
    entities.append(dxf_line("HOLD_MAIN_LOWER_DATUM", 0, MAIN_LOWER_Y, PANEL_W, MAIN_LOWER_Y))
    entities.append(dxf_line("HOLD_CENTRELINES", PANEL_CENTRELINE_X, 0, PANEL_CENTRELINE_X, PANEL_H))
    kx, ky, kw, kh = STEERING_COLUMN_KEEP_OUT
    entities.append(dxf_lwpoly("HOLD_STEERING_COLUMN_RELIEF_EDGE", steering_column_relief_points(), closed=False))
    entities.append(dxf_lwpoly("HOLD_STEERING_COLUMN_SWEPT_KEEP_OUT", rounded_rect_points(kx, ky, kw, kh, 6)))
    entities.append(dxf_line("HOLD_STEERING_COLUMN_AXIS", STEERING_COLUMN_AXIS_X, ky, STEERING_COLUMN_AXIS_X, ky + kh))
    bx, by, bw, bh = LCD_BEZEL
    ax, ay, aw, ah = LCD_APERTURE
    vx, vy, vw, vh = LCD_ACTIVE
    entities.append(dxf_lwpoly("HOLD_LCD_BEZEL_ENVELOPE", rounded_rect_points(bx, by, bw, bh, 4)))
    entities.append(dxf_lwpoly("HOLD_LCD_APERTURE", rounded_rect_points(ax, ay, aw, ah, 3)))
    entities.append(dxf_lwpoly("HOLD_LCD_ACTIVE_REFERENCE", rounded_rect_points(vx, vy, vw, vh, 2)))
    for vent_x, vent_y in VENT_CENTRES:
        entities.append(dxf_circle("HOLD_VENT_FACE_ENVELOPE", vent_x, vent_y, VENT_FACE_DIAMETER / 2))
        entities.append(dxf_circle("HOLD_VENT_NECK_CUTOUT", vent_x, vent_y, VENT_NECK_DIAMETER / 2))
        entities.append(dxf_line("HOLD_CENTRELINES", vent_x - 6, vent_y, vent_x + 6, vent_y))
        entities.append(dxf_line("HOLD_CENTRELINES", vent_x, vent_y - 6, vent_x, vent_y + 6))
    entities.append(dxf_lwpoly("HOLD_GLOVEBOX_TRANSFER_ENVELOPE", glovebox_profile_points()))
    entities.append(dxf_lwpoly("HOLD_SPEEDOMETER_TRANSFER_ENVELOPE", speedometer_profile_points()))
    cx, cy, cw, ch = CONTROL_BANK
    entities.append(dxf_lwpoly("HOLD_CONTROL_BANK_ENVELOPE", rounded_rect_points(cx, cy, cw, ch, 5)))
    for (control_id, label, _, _, _), (control_x, control_y) in zip(CONTROL_MAP, control_positions()):
        if label == "HAZARD":
            entities.append(dxf_circle("HOLD_HAZARD_APERTURE", control_x, control_y, HAZARD_DIAMETER / 2))
        else:
            entities.append(dxf_circle("HOLD_SELECTOR_APERTURES", control_x, control_y, SELECTOR_DIAMETER / 2))
        entities.append(dxf_line("HOLD_CENTRELINES", control_x - 4, control_y, control_x + 4, control_y))
        entities.append(dxf_line("HOLD_CENTRELINES", control_x, control_y - 4, control_x, control_y + 4))
        entities.append(dxf_text("HOLD_ENGRAVE_LABELS", control_x, control_y + CONTROL_LABEL_Y_OFFSET, 3.0, label))


def make_dxfs() -> None:
    master = [dxf_lwpoly("HOLD_FASCIA_OUTER", outer_profile_points())]
    add_component_geometry(master)
    write_dxf(OUT / "full_width_fascia_master_rev_h.dxf", master)

    fit_template = [dxf_lwpoly("CUT_TEMPLATE_OUTER", outer_profile_points())]
    add_component_geometry(fit_template)
    fit_template.append(dxf_text("MARK_TEMPLATE_ID", PANEL_CENTRELINE_X, PANEL_H - 10, 5, "REV H FULL-WIDTH FIT TEMPLATE - NOT VEHICLE CUT DATA"))
    write_dxf(OUT / "full_width_fit_template_rev_h.dxf", fit_template)

    bank = [dxf_lwpoly("HOLD_CONTROL_BANK_OUTER", rounded_rect_points(0, 0, CONTROL_BANK[2], CONTROL_BANK[3], 5))]
    positions = [(x - CONTROL_BANK[0], y - CONTROL_BANK[1]) for x, y in control_positions()]
    for (control_id, label, _, _, _), (control_x, control_y) in zip(CONTROL_MAP, positions):
        layer = "HOLD_HAZARD_APERTURE" if label == "HAZARD" else "HOLD_SELECTOR_APERTURES"
        diameter = HAZARD_DIAMETER if label == "HAZARD" else SELECTOR_DIAMETER
        bank.append(dxf_circle(layer, control_x, control_y, diameter / 2))
        bank.append(dxf_text("HOLD_ENGRAVE_LABELS", control_x, control_y + CONTROL_LABEL_Y_OFFSET, 3, label))
    write_dxf(OUT / "right_control_bank_template_rev_h.dxf", bank)

    support = [
        dxf_lwpoly("HOLD_LCD_SUPPORT_OUTER", rounded_rect_points(0, 0, 246, 158, 5)),
        dxf_lwpoly("HOLD_LCD_REAR_BODY", rounded_rect_points(11, 11, 224, 136, 3)),
    ]
    for x, y in ((8, 8), (238, 8), (8, 150), (238, 150)):
        support.append(dxf_circle("HOLD_SUPPORT_MOUNTS", x, y, 2.5))
    write_dxf(OUT / "lcd_rear_support_reference_rev_h.dxf", support)


def svg_points(points: list[tuple[float, float]], scale: float, x0: float, y0: float) -> str:
    return " ".join(f"{x0 + x * scale:.2f},{y0 + (PANEL_H - y) * scale:.2f}" for x, y in points)


def write_svg() -> None:
    scale, x0, y0 = 0.92, 55.0, 116.0
    sx = lambda value: x0 + value * scale
    sy = lambda value: y0 + (PANEL_H - value) * scale
    vent_markup = []
    for index, (vent_x, vent_y) in enumerate(VENT_CENTRES, start=1):
        vent_markup += [
            f'<circle cx="{sx(vent_x):.2f}" cy="{sy(vent_y):.2f}" r="{VENT_FACE_DIAMETER/2*scale:.2f}" fill="url(#silver)" stroke="#5f666a" stroke-width="2"/>',
            f'<circle cx="{sx(vent_x):.2f}" cy="{sy(vent_y):.2f}" r="{VENT_CORE_DIAMETER/2*scale:.2f}" fill="#252b2f" stroke="#111" stroke-width="2"/>',
            f'<ellipse cx="{sx(vent_x):.2f}" cy="{sy(vent_y):.2f}" rx="{25*scale:.2f}" ry="{8*scale:.2f}" fill="#596166"/>',
            f'<text x="{sx(vent_x):.2f}" y="{sy(vent_y)+4:.2f}" text-anchor="middle" class="ventno">{index}</text>',
        ]
    controls = []
    for (control_id, label, _, _, _), (control_x, control_y) in zip(CONTROL_MAP, control_positions()):
        radius = HAZARD_DIAMETER / 2 if label == "HAZARD" else SELECTOR_DIAMETER / 2
        fill = "#ba2026" if label == "HAZARD" else "url(#silver)"
        controls.append(f'<circle cx="{sx(control_x):.2f}" cy="{sy(control_y):.2f}" r="{radius*scale:.2f}" fill="{fill}" stroke="#111" stroke-width="1.5"/>')
        if label != "HAZARD":
            controls.append(f'<line x1="{sx(control_x)-5:.2f}" y1="{sy(control_y)+5:.2f}" x2="{sx(control_x)+8:.2f}" y2="{sy(control_y)-8:.2f}" stroke="#171b1e" stroke-width="5" stroke-linecap="round"/>')
        controls.append(f'<text x="{sx(control_x):.2f}" y="{sy(control_y + CONTROL_LABEL_Y_OFFSET):.2f}" text-anchor="middle" class="control">{label}</text>')
    bx, by, bw, bh = LCD_BEZEL
    ax, ay, aw, ah = LCD_ACTIVE
    speedo_upper, speedo_lower_left, speedo_lower_right = speedometer_window_rects()
    speedo_x, speedo_y, speedo_w, speedo_h = SPEEDO_ENVELOPE
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="760" viewBox="0 0 1400 760">
<defs><linearGradient id="silver" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f3f4f4"/><stop offset=".5" stop-color="#b5bbbe"/><stop offset="1" stop-color="#71787c"/></linearGradient></defs>
<style>.title{{font:700 22px Verdana;fill:#20262b}}.subtitle{{font:14px Verdana;fill:#53606a}}.label{{font:700 13px Verdana;fill:#20262b}}.small{{font:12px Verdana;fill:#53606a}}.control{{font:700 9px Verdana;fill:#20262b}}.ventno{{font:700 11px Verdana;fill:#e8ecee}}.dim{{stroke:#9c2424;stroke-width:1.5;fill:none}}.hold{{stroke:#aa6500;stroke-width:2;fill:none;stroke-dasharray:7 5}}</style>
<rect width="1400" height="760" fill="#f7f8f9"/>
<text x="55" y="42" class="title">J40 RHD FULL-WIDTH 9-INCH LCD / FOUR-OUTLET FASCIA - REV H</text>
<text x="55" y="68" class="subtitle">170 mm normal face; high end outlets; lowered symmetric inner pair in local pods; RHD column relief; all interface geometry HOLD.</text>
<polygon points="{svg_points(outer_profile_points(), scale, x0, y0)}" fill="#e8e2cc" stroke="#111" stroke-width="2"/>
<line x1="{sx(0)}" y1="{sy(MAIN_LOWER_Y)}" x2="{sx(PANEL_W)}" y2="{sy(MAIN_LOWER_Y)}" class="hold"/>
<rect x="{sx(STEERING_COLUMN_KEEP_OUT[0]):.2f}" y="{sy(STEERING_COLUMN_KEEP_OUT[1] + STEERING_COLUMN_KEEP_OUT[3]):.2f}" width="{STEERING_COLUMN_KEEP_OUT[2]*scale:.2f}" height="{STEERING_COLUMN_KEEP_OUT[3]*scale:.2f}" rx="{6*scale:.2f}" class="hold"/>
<line x1="{sx(STEERING_COLUMN_AXIS_X):.2f}" y1="{sy(STEERING_COLUMN_KEEP_OUT[1]):.2f}" x2="{sx(STEERING_COLUMN_AXIS_X):.2f}" y2="{sy(STEERING_COLUMN_KEEP_OUT[1] + STEERING_COLUMN_KEEP_OUT[3]):.2f}" class="hold"/>
<polygon points="{svg_points(glovebox_profile_points(), scale, x0, y0)}" fill="#aeb2b2" stroke="#5d6264" stroke-width="2"/>
<circle cx="{sx(338)}" cy="{sy(140)}" r="7" fill="#24292d"/>
<text x="{sx(257)}" y="{sy(139)}" text-anchor="middle" class="label">RETAIN OEM GLOVEBOX</text>
<rect x="{sx(bx)}" y="{sy(by+bh)}" width="{bw*scale}" height="{bh*scale}" rx="5" fill="#11161a" stroke="#292f33" stroke-width="2"/>
<rect x="{sx(ax)}" y="{sy(ay+ah)}" width="{aw*scale}" height="{ah*scale}" rx="3" fill="#263e4d" stroke="#dae2e6"/>
<text x="{sx(LCD_CX)}" y="{sy(LCD_CY)-4}" text-anchor="middle" fill="#fff" font-family="Verdana" font-size="14" font-weight="700">9-INCH / 16:9 ACTIVE REFERENCE</text>
<text x="{sx(LCD_CX)}" y="{sy(LCD_CY)+14}" text-anchor="middle" fill="#d6e0e5" font-family="Verdana" font-size="10">199.2 × 112.1 mm | 228.6 mm diagonal | aperture HOLD</text>
<polygon points="{svg_points(speedometer_profile_points(), scale, x0, y0)}" fill="#bfc2bd" stroke="#0d0f10" stroke-width="2"/>
<rect x="{sx(speedo_upper[0])}" y="{sy(speedo_upper[1]+speedo_upper[3])}" width="{speedo_upper[2]*scale}" height="{speedo_upper[3]*scale}" rx="{14*scale}" fill="#292d2e" stroke="#16191b" stroke-width="2"/>
<rect x="{sx(speedo_lower_left[0])}" y="{sy(speedo_lower_left[1]+speedo_lower_left[3])}" width="{speedo_lower_left[2]*scale}" height="{speedo_lower_left[3]*scale}" rx="{4*scale}" fill="#292d2e" stroke="#16191b" stroke-width="2"/>
<rect x="{sx(speedo_lower_right[0])}" y="{sy(speedo_lower_right[1]+speedo_lower_right[3])}" width="{speedo_lower_right[2]*scale}" height="{speedo_lower_right[3]*scale}" rx="{4*scale}" fill="#292d2e" stroke="#16191b" stroke-width="2"/>
<rect x="{sx(STEERING_COLUMN_AXIS_X-3.5)}" y="{sy(speedo_y+29)}" width="{7*scale}" height="{16*scale}" rx="{2*scale}" fill="#ede8d7" stroke="#16191b" stroke-width="1"/>
<text x="{sx(STEERING_COLUMN_AXIS_X)}" y="{sy(speedo_y+80)}" text-anchor="middle" fill="#ede8d7" font-family="Verdana" font-size="10" font-weight="700">SPEED</text>
<text x="{sx(speedo_lower_left[0]+speedo_lower_left[2]/2)}" y="{sy(speedo_y+28)}" text-anchor="middle" fill="#ede8d7" font-family="Verdana" font-size="8">FUEL</text>
<text x="{sx(speedo_lower_right[0]+speedo_lower_right[2]/2)}" y="{sy(speedo_y+28)}" text-anchor="middle" fill="#ede8d7" font-family="Verdana" font-size="8">TEMP / AMP</text>
<text x="{sx(STEERING_COLUMN_AXIS_X)}" y="{sy(speedo_y+speedo_h+4)}" text-anchor="middle" class="control">RETAIN / DIRECT-TRANSFER ORIGINAL SPEEDOMETER ASSEMBLY</text>
{''.join(vent_markup)}
{''.join(controls)}
<line x1="{sx(0)}" y1="{sy(0)+40}" x2="{sx(PANEL_W)}" y2="{sy(0)+40}" class="dim"/>
<text x="{sx(PANEL_CENTRELINE_X)}" y="{sy(0)+62}" text-anchor="middle" class="label">{PANEL_W:.0f} NOMINAL REFERENCE ENVELOPE - M1 PHYSICAL DASH TRACE CONTROLS</text>
<line x1="{sx(0)}" y1="{sy(OUTER_VENT_TOP_DATUM_Y)}" x2="{sx(100)}" y2="{sy(OUTER_VENT_TOP_DATUM_Y)}" class="dim" stroke-dasharray="4 4"/>
<line x1="{sx(PANEL_W-100)}" y1="{sy(OUTER_VENT_TOP_DATUM_Y)}" x2="{sx(PANEL_W)}" y2="{sy(OUTER_VENT_TOP_DATUM_Y)}" class="dim" stroke-dasharray="4 4"/>
<line x1="{sx(VENT_CENTRES[1][0]-70)}" y1="{sy(INNER_VENT_CENTRE_Y)}" x2="{sx(VENT_CENTRES[1][0]+70)}" y2="{sy(INNER_VENT_CENTRE_Y)}" class="dim" stroke-dasharray="4 4"/>
<line x1="{sx(VENT_CENTRES[2][0]-70)}" y1="{sy(INNER_VENT_CENTRE_Y)}" x2="{sx(VENT_CENTRES[2][0]+70)}" y2="{sy(INNER_VENT_CENTRE_Y)}" class="dim" stroke-dasharray="4 4"/>
<line x1="{sx(PANEL_CENTRELINE_X)}" y1="{sy(0)}" x2="{sx(PANEL_CENTRELINE_X)}" y2="{sy(PANEL_H)}" class="hold"/>
<text x="{sx(PANEL_CENTRELINE_X)}" y="{sy(PANEL_H)-10}" text-anchor="middle" class="label">CL X={PANEL_CENTRELINE_X:.1f}: LCD CENTRE = INNER-VENT PAIR MIDPOINT</text>
<text x="{sx(PANEL_CENTRELINE_X)}" y="{sy(PANEL_MIN_Y)+28}" text-anchor="middle" class="label">INNER VENTS: CENTRES Y={INNER_VENT_CENTRE_Y:.1f}, ±{INNER_VENT_CENTRE_OFFSET:.0f} ABOUT CL; FACE TOP Y={INNER_VENT_CENTRE_Y+VENT_FACE_DIAMETER/2:.1f}, {LCD_BEZEL[1]-(INNER_VENT_CENTRE_Y+VENT_FACE_DIAMETER/2):.1f} BELOW LCD BEZEL | PODS TO Y={INNER_VENT_POD_BOTTOM_Y:.1f} | HOLD M7</text>
<rect x="55" y="500" width="1290" height="210" rx="9" fill="#fff" stroke="#c8d0d5"/>
<text x="78" y="535" class="label">RELEASE / FABRICATION INTENT</text>
<text x="78" y="563" class="small">• Full existing face removed only after M1 full-size template identifies structural cowl, A-pillar and steering-column boundaries.</text>
<text x="78" y="588" class="small">• Retained glovebox | centred LCD | retained cluster. End outlets stay high; only the inner pair drops into two identical rounded local pods.</text>
<text x="78" y="613" class="small">• LCD and inner-pair midpoint are exactly on fascia CL. Inner faces sit wholly below the LCD bezel and remain mirrored ±{INNER_VENT_CENTRE_OFFSET:.0f} mm.</text>
<text x="78" y="638" class="small">• RHD column axis X={STEERING_COLUMN_AXIS_X:.1f}; nominal 130 × 105 swept keep-out and U-relief are HOLD to direct M1/M3/M9 trace.</text>
<text x="78" y="663" class="small">• One-piece 1.5 mm CR4 visible face; rear screen carrier and stiffeners transfer load to retained dashboard structure.</text>
<text x="78" y="688" class="small">• Extreme-right two-row bank: WIPERS/LIGHTS/SPOTS/AUX. over BLOWER/A/C/ENGINE/HAZARD; all cuts HOLD.</text>
</svg>'''
    (OUT / "dashboard_lcd_hvac_fascia_rev_h_dimensioned_front.svg").write_text(svg, encoding="utf-8")


def draw_image_fit(c: canvas.Canvas, path: Path, x: float, y: float, max_w: float, max_h: float) -> None:
    if not path.exists():
        return
    image = ImageReader(str(path))
    source_w, source_h = image.getSize()
    scale = min(max_w / source_w, max_h / source_h)
    draw_w, draw_h = source_w * scale, source_h * scale
    c.drawImage(image, x + (max_w - draw_w) / 2, y + (max_h - draw_h) / 2, draw_w, draw_h, preserveAspectRatio=True)


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, width_chars: int = 92, font: str = "Helvetica", size: float = 8, leading_mm: float = 4.2) -> float:
    c.setFont(font, size)
    for line in textwrap.wrap(text, width=width_chars):
        c.drawString(x, y, line)
        y -= leading_mm * mm
    return y


def draw_panel(c: canvas.Canvas, x: float, y: float, scale: float) -> None:
    px = lambda value: x + value * scale * mm
    py = lambda value: y + value * scale * mm
    path = c.beginPath()
    points = outer_profile_points()
    path.moveTo(px(points[0][0]), py(points[0][1]))
    for point_x, point_y in points[1:]:
        path.lineTo(px(point_x), py(point_y))
    path.close()
    c.setFillColor(HexColor("#e8e2cc"))
    c.setStrokeColor(HexColor("#111111"))
    c.drawPath(path, fill=1, stroke=1)
    c.setStrokeColor(HexColor("#b16b00"))
    c.setDash(4, 3)
    c.line(px(0), py(MAIN_LOWER_Y), px(PANEL_W), py(MAIN_LOWER_Y))
    c.line(px(PANEL_CENTRELINE_X), py(0), px(PANEL_CENTRELINE_X), py(PANEL_H))
    kx, ky, kw, kh = STEERING_COLUMN_KEEP_OUT
    c.roundRect(px(kx), py(ky), kw * scale * mm, kh * scale * mm, 6 * scale * mm, fill=0, stroke=1)
    c.line(px(STEERING_COLUMN_AXIS_X), py(ky), px(STEERING_COLUMN_AXIS_X), py(ky + kh))
    c.setDash()
    gp = c.beginPath()
    glove_points = glovebox_profile_points()
    gp.moveTo(px(glove_points[0][0]), py(glove_points[0][1]))
    for point_x, point_y in glove_points[1:]:
        gp.lineTo(px(point_x), py(point_y))
    gp.close()
    c.setFillColor(HexColor("#aeb2b2"))
    c.setStrokeColor(HexColor("#5d6264"))
    c.drawPath(gp, fill=1, stroke=1)
    bx, by, bw, bh = LCD_BEZEL
    c.setFillColor(HexColor("#11161a"))
    c.roundRect(px(bx), py(by), bw * scale * mm, bh * scale * mm, 3 * scale * mm, fill=1, stroke=1)
    ax, ay, aw, ah = LCD_ACTIVE
    c.setFillColor(HexColor("#263e4d"))
    c.roundRect(px(ax), py(ay), aw * scale * mm, ah * scale * mm, 2 * scale * mm, fill=1, stroke=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", max(5, 20 * scale))
    c.drawCentredString(px(LCD_CX), py(LCD_CY) - 1.5 * mm, "9-INCH ACTIVE")
    speedo_points = speedometer_profile_points()
    sp = c.beginPath()
    sp.moveTo(px(speedo_points[0][0]), py(speedo_points[0][1]))
    for point_x, point_y in speedo_points[1:]:
        sp.lineTo(px(point_x), py(point_y))
    sp.close()
    c.setFillColor(HexColor("#bfc2bd"))
    c.setStrokeColor(HexColor("#111111"))
    c.drawPath(sp, fill=1, stroke=1)
    speedo_upper, speedo_lower_left, speedo_lower_right = speedometer_window_rects()
    c.setFillColor(HexColor("#292d2e"))
    c.roundRect(px(speedo_upper[0]), py(speedo_upper[1]), speedo_upper[2] * scale * mm, speedo_upper[3] * scale * mm, 14 * scale * mm, fill=1, stroke=1)
    c.roundRect(px(speedo_lower_left[0]), py(speedo_lower_left[1]), speedo_lower_left[2] * scale * mm, speedo_lower_left[3] * scale * mm, 4 * scale * mm, fill=1, stroke=1)
    c.roundRect(px(speedo_lower_right[0]), py(speedo_lower_right[1]), speedo_lower_right[2] * scale * mm, speedo_lower_right[3] * scale * mm, 4 * scale * mm, fill=1, stroke=1)
    c.setFillColor(HexColor("#ede8d7"))
    c.roundRect(px(STEERING_COLUMN_AXIS_X - 3.5), py(SPEEDO_ENVELOPE[1] + 13), 7 * scale * mm, 16 * scale * mm, 2 * scale * mm, fill=1, stroke=1)
    for vent_x, vent_y in VENT_CENTRES:
        c.setFillColor(HexColor("#bbc1c4"))
        c.setStrokeColor(HexColor("#5f666a"))
        c.circle(px(vent_x), py(vent_y), VENT_FACE_DIAMETER / 2 * scale * mm, fill=1, stroke=1)
        c.setFillColor(HexColor("#252b2f"))
        c.circle(px(vent_x), py(vent_y), VENT_CORE_DIAMETER / 2 * scale * mm, fill=1, stroke=1)
        c.setFillColor(HexColor("#596166"))
        c.ellipse(px(vent_x - 25), py(vent_y - 8), px(vent_x + 25), py(vent_y + 8), fill=1, stroke=0)
    for (control_id, label, _, _, _), (control_x, control_y) in zip(CONTROL_MAP, control_positions()):
        diameter = HAZARD_DIAMETER if label == "HAZARD" else SELECTOR_DIAMETER
        c.setFillColor(HexColor("#ba2026") if label == "HAZARD" else HexColor("#bbc1c4"))
        c.circle(px(control_x), py(control_y), diameter / 2 * scale * mm, fill=1, stroke=1)
        c.setFillColor(HexColor("#20262b"))
        c.setFont("Helvetica-Bold", max(3.7, 12 * scale))
        c.drawCentredString(px(control_x), py(control_y + CONTROL_LABEL_Y_OFFSET), label)


def write_pdf() -> None:
    pdf_path = OUT / "j40_dashboard_lcd_hvac_fascia_rev_h_shop_spec.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=landscape(A3))
    page_w, page_h = landscape(A3)
    c.setTitle("J40 RHD Full-width Dashboard Rev H")

    # Page 1 - dimensional front intent and release boundary.
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(15 * mm, page_h - 16 * mm, "J40 RHD full-width 9-inch LCD / four-outlet fascia - Rev H")
    c.setFont("Helvetica", 8.5)
    c.drawRightString(page_w - 15 * mm, page_h - 16 * mm, "Units mm | quotation + full-size template issue | all vehicle/metal geometry HOLD")
    draw_panel(c, 20 * mm, 113 * mm, 0.30)
    c.setFillColor(HexColor("#8b1e1e"))
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(page_w / 2, 106 * mm, f"Nominal X 0..{PANEL_W:.0f}, Y {PANEL_MIN_Y:.0f}..{PANEL_H:.0f}; normal face is 170 high and only the two vent pods descend {MAIN_LOWER_Y-PANEL_MIN_Y:.0f} - M1 physical trace controls")
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(15 * mm, 91 * mm, "LOCKED ARCHITECTURE")
    notes = [
        "Full existing visible dashboard face is replaced by one formed 1.5 mm CR4 face after structural boundaries are transferred; retain cowl, A-pillars, steering-column support and firewall structure.",
        "A 9-inch / 16:9 active-image reference is 199.2 x 112.1 mm = 228.6 mm diagonal. The Sehgal 9-inch listing publishes no chassis/cutout drawing: bezel, aperture, rear body and mounts are HOLD to a bought sample.",
        f"LCD centre X={PANEL_CENTRELINE_X:.1f}. Inner vents are exactly symmetric at X={VENT_CENTRES[1][0]:.1f}/{VENT_CENTRES[2][0]:.1f}, Y={INNER_VENT_CENTRE_Y:.1f}; each Ø87 face ends at Y={INNER_VENT_CENTRE_Y + VENT_FACE_DIAMETER/2:.1f}, {LCD_BEZEL[1]-(INNER_VENT_CENTRE_Y+VENT_FACE_DIAMETER/2):.1f} mm below the LCD bezel bottom Y={LCD_BEZEL[1]:.1f}.",
        "Four matching satin-silver generic vents: published face Ø87 and panel opening Ø75 reference; M7 sample/caliper gate controls the cut.",
        f"The normal face is {PANEL_H-MAIN_LOWER_Y:.0f} mm high. The two identical vent pods alone descend to Y={PANEL_MIN_Y:.0f}; prove their {MAIN_LOWER_Y-PANEL_MIN_Y:.0f} mm local projection against knees, levers and four rear ducts at M8/M9.",
        f"Outer vents remain high at Y={OUTER_VENT_CENTRE_Y:.1f}, with their tops at the LCD-top datum Y={OUTER_VENT_TOP_DATUM_Y:.1f}. Original glovebox and speedometer stay in their factory openings; M2/M3 direct traces override this schematic.",
        f"A nominal radiused U-relief at the schematic steering axis X={STEERING_COLUMN_AXIS_X:.1f} clears the RHD column; the installed factory position, trace and swept envelope are M1/M3/M9 HOLD.",
        "All controls sit fully right of the column keep-out in two compact rows: WIPERS/LIGHTS/SPOTS/AUX. above BLOWER/A/C/ENGINE/red HAZARD.",
        f"V4 is visually controlled by the straight-on overlay. The nominal Ø22.5 head-to-rim gap is {V4_NOMINAL_SELECTOR_HEAD_CLEARANCE:.2f} mm (>= {MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE:.0f}); the smaller {V4_CONTROL_ENVELOPE_NOMINAL_GAP:.0f} mm gap is to the conservative bank/label envelope. M6 verifies actual heads and M8/M9 prove >= {MIN_STATIC_REAR_CLEARANCE:.0f} rear clearance. Do not move V4 farther right: 6.5/12.5 end lands.",
    ]
    y = 84 * mm
    c.setFont("Helvetica", 7.2)
    for note in notes:
        c.drawString(18 * mm, y, "- " + note)
        y -= 6.3 * mm
    c.setFillColor(HexColor("#8b1e1e"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(15 * mm, 12 * mm, "DO NOT CUT VEHICLE METAL OR ANY HOLD_* APERTURE FROM NOMINAL COORDINATES. CUT ONLY THE DISPOSABLE FIT TEMPLATE BEFORE M1-M10 SIGN-OFF.")
    c.showPage()

    # Page 2 - owner-photo bases and the selected V6 visual pair.
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(15 * mm, page_h - 16 * mm, "Owner-photo basis and selected Rev H V6 visual intent")
    c.setFont("Helvetica", 8.5)
    c.drawRightString(page_w - 15 * mm, page_h - 16 * mm, "Images establish appearance only - never scale for CNC")
    labels = [
        ("ASSEMBLED RHD OWNER PHOTO", 15, 263), ("SELECTED REV H V6 OBLIQUE", 215, 263),
        ("BARE-SHELL OWNER PHOTO", 15, 148), ("SELECTED REV H V6 STRAIGHT-ON", 215, 148),
    ]
    c.setFont("Helvetica-Bold", 9)
    for label, x_pos, y_pos in labels:
        c.drawString(x_pos * mm, y_pos * mm, label)
    draw_image_fit(c, ASSEMBLED_BASE_PHOTO, 15 * mm, 166 * mm, 190 * mm, 88 * mm)
    draw_image_fit(c, OUT / COLUMN_V6_ASSEMBLED_VIS_RELATIVE, 215 * mm, 166 * mm, 190 * mm, 88 * mm)
    draw_image_fit(c, BARE_BASE_PHOTO, 15 * mm, 51 * mm, 190 * mm, 88 * mm)
    draw_image_fit(c, OUT / COLUMN_V6_STRAIGHT_VIS_RELATIVE, 215 * mm, 51 * mm, 190 * mm, 88 * mm)
    c.setFont("Helvetica", 7.5)
    c.drawString(15 * mm, 39 * mm, "Selected V6 pair: explicit continuous RHD column/shroud, true 9-inch centre screen, untouched OEM items and the compact control bank moved down/right.")
    c.drawString(15 * mm, 32 * mm, "The oblique driver view naturally foreshortens and partly masks the screen; M4 sample measurement, not apparent photo size, controls the LCD cut.")
    c.drawString(15 * mm, 25 * mm, f"V4 nominal Ø22.5-head gap={V4_NOMINAL_SELECTOR_HEAD_CLEARANCE:.2f} mm; {V4_CONTROL_ENVELOPE_NOMINAL_GAP:.0f} mm is to the bank/label envelope. Straight-on view + M6/M8/M9 control release.")
    c.setFillColor(HexColor("#8b1e1e"))
    c.setFont("Helvetica-Bold", 7.8)
    c.drawString(15 * mm, 14 * mm, "VISUALISATIONS ARE DESIGN INTENT ONLY. CNC RELEASE REQUIRES ACTUAL DASH, LCD, VENTS, CONTROLS AND A SIGNED FULL-SIZE TEMPLATE.")
    c.showPage()

    # Page 3 - exact controls and electrical implementation.
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(15 * mm, page_h - 16 * mm, "Exact extreme-right two-row control schedule and electrical boundaries")
    c.setFont("Helvetica", 8.5)
    c.drawRightString(page_w - 15 * mm, page_h - 16 * mm, "Exactly 7 industrial selectors + 1 separate red hazard")
    style = ParagraphStyle("cell", fontName="Helvetica", fontSize=6.2, leading=7.1, alignment=TA_LEFT, textColor=HexColor("#20262b"))
    header_style = ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=6.4, leading=7.3, textColor=colors.white)
    headers = ["ID", "CABIN POSITION", "LABEL", "HARDWARE / STATES", "PLAIN-LANGUAGE FUNCTION", "ELECTRICAL TARGET / CONSTRAINT"]
    table_rows = [[Paragraph(value, header_style) for value in headers]]
    locations = [
        "top row 1/4", "top row 2/4", "top row 3/4", "top row 4/4",
        "bottom row 1/4", "bottom row 2/4", "bottom row 3/4", "bottom row 4/4",
    ]
    actions = [
        "Parks the wipers in OFF and selects low or high wipe.",
        "Selects lights off, sidelights or headlamps; original dip remains.",
        "Turns auxiliary spot lamps off/on.",
        "Commands one reserved accessory circuit.",
        "Stops the cabin fan or selects low/high airflow.",
        "Requests compressor cooling when the safety chain permits.",
        "Selects engine RUN/STOP through the validated fuel-stop interface.",
        "Flashes all indicators without disturbing the indicator stalk.",
    ]
    for location, action, row in zip(locations, actions, CONTROL_MAP):
        control_id, label, hardware, states, electrical = row
        values = [control_id, location, label, f"{hardware}; {states}", action, electrical]
        table_rows.append([Paragraph(value, style) for value in values])
    table = Table(table_rows, colWidths=[18 * mm, 25 * mm, 24 * mm, 55 * mm, 91 * mm, 170 * mm], rowHeights=[11 * mm] + [20 * mm] * 8)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#30373d")),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#7d878f")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f1f3f4"), colors.white]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    table.wrapOn(c, page_w, page_h)
    table.drawOn(c, 15 * mm, 88 * mm)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(15 * mm, 76 * mm, "ELECTRICAL RULES")
    rules = [
        "Every selector carries only a fused relay/controller input. No selector directly carries lamp, wiper-motor, blower, compressor-clutch or accessory load current.",
        "Relay baseline: T1 low beam; T2 high beam; T3 horn; T4 condenser fan; T5 spots; B1 A/C request; B2 AUX. Assign a fuel-stop relay/output only after EEI-003 proves the engine logic.",
        "WIPERS must preserve automatic park; retain washer on its separate momentary/OEM input. LIGHTS is master OFF/SIDE/HEAD; HEAD retains side/tail/plate/instrument and the original dip selects low/high.",
        "BLOWER controller/fuse are sized after measured current. A/C reaches B1 only through thermostat and trinary/pressure safeties; prove condenser-fan logic.",
        "Cabin temperature/blend is not an eighth selector: retain the measured evaporator thermostat/controller, adding a separate control only if the delivered unit requires it.",
        "ENGINE is a low-current RUN/STOP command only. Key OFF remains authoritative and must stop the engine; retain the manual diesel stop cable as a mechanical fallback. Leave ENGINE unwired until EEI-003 identifies the fuel-stop component and safe logic.",
        "HAZARD requires the correct isolated flasher interface. Retain original indicator stalk, horn, keyed ignition, winch third lever and identified mechanical cables outside this bank.",
    ]
    y = 69 * mm
    c.setFont("Helvetica", 7.3)
    for rule in rules:
        c.drawString(18 * mm, y, "- " + rule)
        y -= 6.8 * mm
    draw_image_fit(c, OUT / "industrial_rotary_selector_reference.png", 357 * mm, 9 * mm, 48 * mm, 58 * mm)
    c.setFont("Helvetica", 6.5)
    c.drawRightString(352 * mm, 15 * mm, "Schneider-standard Ø22.5 cut / 68 mm rear envelope reference; confirm bought part code, bush, flange and stack at M6.")
    c.showPage()

    # Page 4 - shop construction, section intent and release sequence.
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(15 * mm, page_h - 16 * mm, "Fabrication construction, duct packaging and M1-M10 release sequence")
    c.setFont("Helvetica", 8.5)
    c.drawRightString(page_w - 15 * mm, page_h - 16 * mm, "One-piece visible face | separate concealed reinforcement permitted")
    columns = [
        (15, "VISIBLE FACE / STRUCTURE", [
            "1.5 mm CR4 mild-steel visible face; laser/waterjet and press-form after template sign-off.",
            "Low-gloss body-colour finish; deburr/radius every edge and epoxy-prime both sides before paint.",
            "Keep the face one visible piece. Concealed rear rails, vent rings, LCD carrier and local doublers may be separate.",
            "Use approx. 15 mm returns where the vehicle permits. Keep the visible lower edge shallow; use concealed rear rails/flanges where a continuous fold is impractical.",
            "Form a smooth radiused relief around the RHD steering column only from the signed M1/M3 trace. Never cut or relocate its support bracket.",
            "Screen mass goes into a rear bracket tied to retained structure, never the 1.5 mm skin alone.",
            "Provide hidden M5 fasteners at <=150 mm pitch where structure permits and allow cabin-side LCD/vent service removal.",
        ]),
        (147, "HVAC / PACKAGING", [
            "Exactly four matching generic silver outlets with published Ø87 faces / Ø75 panel-opening reference; M7 real-sample data controls.",
            f"Keep the two end outlets high with bezel tops at Y={OUTER_VENT_TOP_DATUM_Y:.1f}. Lower only the symmetric inner pair to centre Y={INNER_VENT_CENTRE_Y:.1f}, with their full faces below the LCD bezel.",
            f"Form two matching rounded body-colour pods around the inner outlets. Pods descend locally from the normal Y={MAIN_LOWER_Y:.0f} edge to Y={PANEL_MIN_Y:.0f}; do not extend the complete dashboard downward.",
            "Use four branches sized to the sampled vent spigot from a balanced plenum. Confirm hose ID and bend radius after M7; do not assume 3-inch duct.",
            "Do not crush hose or obstruct the glovebox, speedometer, column, wiring, LCD connectors, demist system or service paths.",
            f"Use the inner pods for extra rear neck/elbow depth. At M8/M9 prove both {MAIN_LOWER_Y-PANEL_MIN_Y:.0f} mm local drops, all four duct bends and the selector stacks against the cluster, column support, wiring, knees and levers.",
            f"M8/M9 acceptance minima: visible inner-rim/LCD gap >= {MIN_INNER_VENT_LCD_VISIBLE_GAP:.0f} mm; vent retainer/duct to fixed hardware >= {MIN_STATIC_REAR_CLEARANCE:.0f} mm; to signed moving column/shroud/stalk sweep >= {MIN_MOVING_COLUMN_CLEARANCE:.0f} mm; duct minor axis >= {MIN_DUCT_ROUNDNESS_PERCENT:.0f}% of round ID. Photograph the tightest point with ruler/feeler/caliper.",
            f"V4 does not move farther right: its end lands are only 6.5/12.5 mm. The nominal Ø22.5-head-to-rim gap is {V4_NOMINAL_SELECTOR_HEAD_CLEARANCE:.2f} mm and passes the >= {MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE:.0f} face-layout target; the smaller {V4_CONTROL_ENVELOPE_NOMINAL_GAP:.0f} mm figure is to the bank/label envelope. M6 verifies actual heads; M8/M9 prove V4 retainer/neck/elbow/duct >= {MIN_STATIC_REAR_CLEARANCE:.0f} mm to contact blocks, terminals and wiring.",
        ]),
        (279, "CUT / FINISH SEQUENCE", [
            "1. Cut the disposable full-size template only. Fit, trim and directly trace the column/shroud/stalk sweep plus all structural keep-outs on the actual vehicle.",
            "2. Mount real glovebox, cluster, LCD, four vents, seven selectors and hazard to the template or cheap-sheet prototype.",
            "3. Prove rear stacks, four ducts, steering/lever/knee clearance, sight lines, glovebox sweep and service removal.",
            "4. Owner signs the perimeter and every actual-part aperture. Fabricator converts approved trace to production toolpaths.",
            "5. Cut vehicle face initially undersize, trial-fit progressively, protect retained structure, deburr and prime immediately.",
            "6. Form, reinforce, paint, assemble, label, wire through fused relays/controllers, then complete M10 live tests.",
        ]),
    ]
    for x_mm, heading, rows in columns:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_mm * mm, 260 * mm, heading)
        y = 252 * mm
        c.setFont("Helvetica", 7.2)
        for row in rows:
            y = draw_wrapped(c, row, x_mm * mm, y, width_chars=53, size=7.2, leading_mm=3.8) - 2 * mm
    c.setStrokeColor(HexColor("#7d878f"))
    c.line(140 * mm, 91 * mm, 140 * mm, 264 * mm)
    c.line(272 * mm, 91 * mm, 272 * mm, 264 * mm)
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(15 * mm, 82 * mm, "M1-M10 RELEASE GATES")
    gates = [
        "M1 perimeter/structure plus column axis, shroud, stalk and sweep trace", "M2 OEM glovebox trace, hinge, latch and sweep",
        "M3 OEM cluster outline, depth, mounts, column relationship and sight line", "M4 LCD maker drawing, active area, aperture and bezel",
        "M5 LCD rear body, support, connectors and removal", f"M6 real selectors + hazard, including V4-to-nearest-head >= {MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE:.0f} mm",
        "M7 four matched vents: face, Ø75 cut, retainer, spigot and depth", "M8 duct mock-up: prove 10 mm fixed / 20 mm moving clearance and >=90% roundness",
        f"M9 signed prototype: V4 rear clearance >= {MIN_STATIC_REAR_CLEARANCE:.0f} mm plus driver, column, levers and service", "M10 continuity, labels, wiper park/washer, light truth table, blower, A/C safeties, ENGINE key-off/manual fallback, AUX/SPOTS/hazard tests",
    ]
    for index, gate in enumerate(gates):
        column = 0 if index < 5 else 1
        row = index if index < 5 else index - 5
        c.setFont("Helvetica", 7.2)
        c.drawString((18 + column * 196) * mm, (74 - row * 10) * mm, gate)
    c.setFillColor(HexColor("#8b1e1e"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(15 * mm, 14 * mm, "RELEASE NOW: quotation + CUT_TEMPLATE_OUTER disposable template only. ALL METAL, VEHICLE, LCD, VENT, OEM-TRANSFER, CONTROL AND SUPPORT GEOMETRY REMAINS HOLD.")
    c.showPage()
    c.save()


def write_csvs() -> None:
    with (OUT / "fabricator_cut_and_release_schedule.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["part", "qty", "material", "thickness_mm", "finish", "source_file", "release_status"])
        writer.writerows([
            ["full-width disposable fit template", 1, "MDF/card/cheap plastic", "3-6", "none", "full_width_fit_template_rev_h.dxf", "CUT_TEMPLATE_OUTER released for template only; no vehicle or metal cutting"],
            ["full-width one-piece visible fascia", 1, "CR4 mild steel", MATERIAL_THICKNESS, "low-gloss body colour both sides", "full_width_fascia_master_rev_h.dxf", "QUOTE/HOLD entire metal part until M1-M10; HOLD_* layers never production paths"],
            ["right control bank apertures/engraving", 1, "integral with visible fascia", MATERIAL_THICKNESS, "3 mm labels with black infill", "right_control_bank_template_rev_h.dxf", "QUOTE/HOLD pending all seven bought selectors, hazard and rear-stack fit"],
            ["LCD rear structural carrier", 1, "5052-H32 aluminium or CR4 steel", "2.0", "black", "lcd_rear_support_reference_rev_h.dxf", "QUOTE/HOLD all geometry pending selected LCD and vehicle structure"],
            ["rear full-width stiffener rails / local doublers", 1, "CR4 mild steel", "1.5-2.0", "epoxy prime + body colour/black", "shop-detail after M1", "QUOTE/HOLD; must transfer screen and control loads into retained structure"],
            ["HVAC vent retainers / sample-specific branch adaptors", 4, "supplier hardware / fabricated as needed", "supplier-specific", "concealed", "actual vent data", "QUOTE/HOLD pending M7-M8"],
        ])

    with (OUT / "fascia_coordinate_schedule.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["feature", "x_mm", "y_mm", "width_or_diameter_mm", "height_mm", "layer", "status_note"])
        rows = [
            ["nominal coordinate extent including local pods", 0, PANEL_MIN_Y, PANEL_W, PANEL_H - PANEL_MIN_Y, "HOLD_FASCIA_OUTER", f"{PANEL_H-PANEL_MIN_Y:.0f} mm total model extent exists only at local features; template coordinate system only; M1 physical trace controls"],
            ["fascia vertical centre datum", PANEL_CENTRELINE_X, PANEL_MIN_Y, "", PANEL_H - PANEL_MIN_Y, "HOLD_CENTRELINES", "master datum: LCD centre and midpoint of inner vent pair must remain coincident after M1 trace"],
            ["main lower datum", 0, MAIN_LOWER_Y, PANEL_W, "", "HOLD_MAIN_LOWER_DATUM", f"normal face is 170 mm high and ends at Y50; only two inner-vent pods descend {MAIN_LOWER_Y-PANEL_MIN_Y:.0f} mm to Y{PANEL_MIN_Y:.0f}, plus the local column relief/control edge"],
            ["left inner-vent pod envelope", VENT_CENTRES[1][0] - INNER_VENT_POD_HALF_W, PANEL_MIN_Y, 2 * INNER_VENT_POD_HALF_W, MAIN_LOWER_Y - PANEL_MIN_Y, "HOLD_FASCIA_OUTER", "rounded local projection only; M8/M9 knee, lever and duct mock-up required"],
            ["right inner-vent pod envelope", VENT_CENTRES[2][0] - INNER_VENT_POD_HALF_W, PANEL_MIN_Y, 2 * INNER_VENT_POD_HALF_W, MAIN_LOWER_Y - PANEL_MIN_Y, "HOLD_FASCIA_OUTER", "rounded local projection only; remains left of nominal steering keep-out; M8/M9 mock-up required"],
            ["LCD bezel envelope", LCD_BEZEL[0], LCD_BEZEL[1], LCD_BEZEL[2], LCD_BEZEL[3], "HOLD_LCD_BEZEL_ENVELOPE", "manufacturer drawing controls"],
            ["LCD aperture", LCD_APERTURE[0], LCD_APERTURE[1], LCD_APERTURE[2], LCD_APERTURE[3], "HOLD_LCD_APERTURE", "manufacturer drawing controls"],
            ["LCD active image", LCD_ACTIVE[0], LCD_ACTIVE[1], LCD_ACTIVE[2], LCD_ACTIVE[3], "HOLD_LCD_ACTIVE_REFERENCE", "9-inch / 16:9 mathematical reference only: 228.6 mm diagonal; sample controls"],
            ["OEM glovebox transfer envelope", GLOVEBOX_ENVELOPE[0], GLOVEBOX_ENVELOPE[1], GLOVEBOX_ENVELOPE[2], GLOVEBOX_ENVELOPE[3], "HOLD_GLOVEBOX_TRANSFER_ENVELOPE", "actual asymmetric lid/hinge/latch trace controls"],
            ["OEM speedometer transfer envelope", SPEEDO_ENVELOPE[0], SPEEDO_ENVELOPE[1], SPEEDO_ENVELOPE[2], SPEEDO_ENVELOPE[3], "HOLD_SPEEDOMETER_TRANSFER_ENVELOPE", "actual original assembly trace and mounts control"],
            ["steering-column axis", STEERING_COLUMN_AXIS_X, 0, "", STEERING_COLUMN_KEEP_OUT[3], "HOLD_STEERING_COLUMN_AXIS", "nominal alignment with retained cluster centre only; direct M1/M3/M9 trace controls"],
            ["steering-column swept keep-out", STEERING_COLUMN_KEEP_OUT[0], STEERING_COLUMN_KEEP_OUT[1], STEERING_COLUMN_KEEP_OUT[2], STEERING_COLUMN_KEEP_OUT[3], "HOLD_STEERING_COLUMN_SWEPT_KEEP_OUT", "nominal no-component envelope including shroud/stalk movement; not production geometry"],
            ["steering-column lower-edge relief", STEERING_COLUMN_AXIS_X - STEERING_COLUMN_RELIEF_HALF_W, MAIN_LOWER_Y, 2 * STEERING_COLUMN_RELIEF_HALF_W, STEERING_COLUMN_RELIEF_RISE, "HOLD_STEERING_COLUMN_RELIEF_EDGE", "radiused U-relief intent; replace with direct trace plus signed running clearance"],
            ["right control bank envelope", CONTROL_BANK[0], CONTROL_BANK[1], CONTROL_BANK[2], CONTROL_BANK[3], "HOLD_CONTROL_BANK_ENVELOPE", f"two rows at extreme right: S1-S4 top, S5-S8 bottom; exact 7 selectors + hazard; {CONTROL_COLUMNS[1]-CONTROL_COLUMNS[0]:.0f} mm horizontal and {CONTROL_TOP_Y-CONTROL_BOTTOM_Y:.0f} mm vertical pitch; V4 nominal rim-to-bank-envelope gap is {V4_CONTROL_ENVELOPE_NOMINAL_GAP:.0f} mm; M6/M8/M9 HOLD"],
        ]
        for index, (vent_x, vent_y) in enumerate(VENT_CENTRES, start=1):
            if index in (1, 4):
                face_note = f"high end outlet; Ø87 bezel top Y={OUTER_VENT_TOP_DATUM_Y:.1f}, aligned with LCD bezel top"
            else:
                face_note = f"lowered inner outlet in local pod; Ø87 face spans Y={vent_y-VENT_FACE_DIAMETER/2:.1f}..{vent_y+VENT_FACE_DIAMETER/2:.1f}, wholly below LCD bezel bottom Y={LCD_BEZEL[1]:.1f}"
            if index in (2, 3):
                face_note += f"; pair mirrored ±{INNER_VENT_CENTRE_OFFSET:.1f} about fascia/LCD centreline X={PANEL_CENTRELINE_X:.1f}; pod bottom Y={PANEL_MIN_Y:.1f}; M8/M9 clearance HOLD"
            if index in (1, 4):
                face_note += "; outer visible face is 6.5 mm from nominal usable-face end and Ø75 reference cut is 12.5 mm from it; M1/M7 control"
            if index == 4:
                face_note += f"; STRAIGHT-ON OVERLAY IS V4 VISUAL PLACEMENT CONTROL: nominal Ø22.5-head-to-rim gap={V4_NOMINAL_SELECTOR_HEAD_CLEARANCE:.2f} mm and passes the ≥{MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE:.0f} target; nominal lower-rim to bank/label envelope={V4_CONTROL_ENVELOPE_NOMINAL_GAP:.0f} mm, not production clearance; prove the actual head gap after M6 and ≥{MIN_STATIC_REAR_CLEARANCE:.0f} mm retainer/neck/elbow/duct to selector contact blocks, terminals and wiring at M8/M9; do not move V4 farther right because 6.5/12.5 mm end lands are already minimal"
            rows.append([f"vent {index} visible face", vent_x, vent_y, VENT_FACE_DIAMETER, "", "HOLD_VENT_FACE_ENVELOPE", face_note])
            rows.append([f"vent {index} panel-opening reference", vent_x, vent_y, VENT_NECK_DIAMETER, "", "HOLD_VENT_NECK_CUTOUT", "published generic reference only; M7 matched sample controls"])
        writer.writerows(rows)

    with (OUT / "switch_position_schedule.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "physical_position_viewed_from_cabin", "x_mm_nominal", "y_mm_nominal", "type", "engraved_label", "states", "function", "electrical_target", "release"])
        actions = [
            "park then low/high wipe", "off/sidelights/headlamps; retain dip", "auxiliary spot lamps", "reserved assigned accessory",
            "cabin fan off/low/high", "compressor cooling request when safe", "engine run/stop request through validated fuel-stop interface", "flash all indicators",
        ]
        for station_index, (row, (control_x, control_y), action) in enumerate(zip(CONTROL_MAP, control_positions(), actions), start=1):
            control_id, label, hardware, states, electrical = row
            release = "function locked; aperture and rear stack HOLD"
            if label == "ENGINE":
                release = "function/label locked; wiring HOLD until EEI-003 identifies fuel-stop logic and key-off/manual fallback tests pass"
            elif label == "HAZARD":
                release = "separate from seven selectors; aperture/part HOLD"
            row_name = "top" if station_index <= 4 else "bottom"
            row_station = station_index if station_index <= 4 else station_index - 4
            physical_position = f"extreme-right {row_name} row; station {row_station} of 4 left-to-right"
            writer.writerow([control_id, physical_position, control_x, control_y, hardware, label, states, action, electrical, release])

    with (OUT / "measurement_and_release_schedule.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["gate", "measurement_or_test", "nominal_intent", "required_evidence", "release_status"])
        writer.writerows([
            ["M1", "full-width dashboard perimeter; cowl/A-pillar/firewall structure; steering-column axis, installed angle, shroud OD, stalk/sweep and support; attachment flange; true usable-face centreline", f"{PANEL_H-MAIN_LOWER_Y:.0f} mm normal face; only two 112 mm-wide inner-vent pods descend {MAIN_LOWER_Y-PANEL_MIN_Y:.0f} mm, with separate local column/control shaping, inside nominal X0..{PANEL_W:.0f}/Y{PANEL_MIN_Y:.0f}..{PANEL_H:.0f}; none are vehicle dimensions", "rigid full-size template fitted and trimmed; direct column/shroud/sweep trace; front/rear ruler photos; centreline derived from signed usable face; owner-signed perimeter", "HOLD all metal and vehicle cuts"],
            ["M2", "OEM glovebox exact asymmetric outline, hinge/latch axes, knob, instruction plate, rear depth and full opening sweep", "preserve original appearance and operation", "direct trace/rubbing, mounted donor, sweep photos and clearance record", "HOLD"],
            ["M3", "OEM speedometer/cluster exact factory opening, outline, mounts, depth, cables/wiring, column-axis relationship and seated-driver sight line", f"retain original assembly without relocation; schematic placeholder cluster centre and column axis X={STEERING_COLUMN_AXIS_X:.1f} is not a vehicle dimension", "direct trace/rubbing of the existing factory opening and installed column relationship, rear depth gauge and driver-view photos; copied trace replaces every nominal cluster/axis coordinate", "HOLD"],
            ["M4", "LCD active area, aperture, bezel and corner radii", "9-inch 16:9 active 199.2 x 112.1; 228.6 diagonal; aperture 202 x 115 reference", "manufacturer mechanical drawing and caliper confirmation", "HOLD"],
            ["M5", "LCD rear body, mount centres, mass, connectors, cable bend, cooling and service removal", f"screen centre X{PANEL_CENTRELINE_X:.1f}/Y{LCD_CY:.1f}; exactly coincident with fascia centreline and inner-vent-pair midpoint; separate rear structural carrier", "rear-body rubbing, depth record, bracket mock-up, centreline check and cabin-side removal test", "HOLD"],
            ["M6", "seven bought Schneider-style selectors and separate hazard: part code, actual head/lever sweep, bush, flange, anti-rotation and contact-block stack", f"two rows of four; {CONTROL_COLUMNS[1]-CONTROL_COLUMNS[0]:.0f} mm horizontal and {CONTROL_TOP_Y-CONTROL_BOTTOM_Y:.0f} mm vertical pitch; selector panel cut Ø22.5; 68 mm rear envelope; hazard Ø16 reference; V4 nominal Ø22.5-head-to-rim gap={V4_NOMINAL_SELECTOR_HEAD_CLEARANCE:.2f} mm passes the ≥{MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE:.0f} face target, while the {V4_CONTROL_ENVELOPE_NOMINAL_GAP:.0f} mm figure is to the bank/label envelope; actual selector heads/labels still control", "part-code photo plus caliper sheet for every part, including actual head diameter/sweep and contact-block depth; 1:1 two-row extreme-right trial including the V4 visible-rim-to-nearest-selector-head measurement and hand/label clearance", "HOLD"],
            ["M7", "four matched generic vent faces, panel opening, retention, spigot OD and rear depth", "published silver/chrome ABS family: Ø87 face; Ø75 panel-opening reference; V4 must remain at the current far-right datum because its 6.5 mm visible-rim and 12.5 mm Ø75-cut end lands cannot be reduced", "one received four-piece batch, seller drawing/listing, caliper record and fitted retainer trial for all four, including V4 retainer/neck envelope", "HOLD"],
            ["M8", "four ducts, plenum balance, actual hose ID/bend radii, selector rear stacks, steering-column support and rear/service clearances", f"sampled vent spigot controls duct size; lowered inner outlets use two local pods down to Y={PANEL_MIN_Y:.0f}; ≥{MIN_STATIC_REAR_CLEARANCE:.0f} mm to fixed LCD/cluster/support parts, ≥{MIN_MOVING_COLUMN_CLEARANCE:.0f} mm to the signed moving column/shroud/stalk sweep, duct ovalisation no worse than {MIN_DUCT_ROUNDNESS_PERCENT:.0f}% of round ID, and V4 retainer/neck/elbow/duct ≥{MIN_STATIC_REAR_CLEARANCE:.0f} mm from selector contact blocks, terminals and wiring", f"full rear 1:1 mock-up with all four ducts, both {MAIN_LOWER_Y-PANEL_MIN_Y:.0f} mm local pod drops, actual V4 retainer/neck/elbow, selector contact stacks/terminals/wiring and column through full sweep; caliper/feeler photos at the worst points plus duct minor-axis measurements and blower-flow comparison", "HOLD until every stated minimum passes"],
            ["M9", "complete full-size prototype and driver/service clearances", f"one-piece shallow normal face with two lowered symmetric inner-vent pods; as-built visible V2/V3 rim-to-LCD gap ≥{MIN_INNER_VENT_LCD_VISIBLE_GAP:.0f} mm; V3 hardware/duct keeps ≥{MIN_STATIC_REAR_CLEARANCE:.0f} mm to fixed cluster parts and ≥{MIN_MOVING_COLUMN_CLEARANCE:.0f} mm to the signed column/shroud/stalk swept envelope; V4 must retain ≥{MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE:.0f} mm visible rim-to-nearest actual selector head and ≥{MIN_STATIC_REAR_CLEARANCE:.0f} mm rear clearance to control contact blocks/terminals/wiring; OEM glovebox/cluster remain in factory openings", "owner-signed full-depth prototype: seated-driver steering lock-to-lock/stalk sweep, reach, knee/gear/lever/column clearance at both pods, glovebox sweep, V4/selector visual clearance, rear V4 duct/control-stack clearance, centre/symmetry, visibility and removal checks; ruler/feeler photos proving each minimum at the tightest point", "HOLD until every stated minimum passes"],
            ["M10", "labels, continuity, relay/controller mapping and live functions", "exact switch schedule including ENGINE RUN/STOP; key OFF authoritative; manual stop cable retained", "continuity sheet and live wiper park plus washer, OFF/SIDE/HEAD truth table plus dip, measured blower, A/C safety/fan, spots, AUX, isolated hazard, ENGINE run/stop, key-off and manual-cable fallback tests", "HOLD until passed"],
        ])

    with (OUT / "dimensional_provenance_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["feature", "reference_value", "provenance", "confidence", "production_release", "required_gate", "source_url"])
        writer.writerows([
            ["public early replacement-panel product envelope", "1400 x 250 x 100 mm", "Reborn FJ 1968-1978 steel dashboard listing; centimetre-resolution product dimension, not installed RHD face datums, bends or aperture coordinates", "PUBLISHED_VENDOR_ENVELOPE", "NOT FOR CNC", "M1 physical full-width trace", PUBLIC_REPRO_PANEL_URL],
            ["full dashboard visible-face perimeter", f"nominal X0..{PANEL_W:.0f}, Y{PANEL_MIN_Y:.0f}..{PANEL_H:.0f}; 170 high normal face plus two local {MAIN_LOWER_Y-PANEL_MIN_Y:.0f} mm pods", "Rev H proportional design datum; public vendor envelope is broader product context only and Toyota EPC shows configuration-specific panels", "DESIGN_REFERENCE_ONLY", "HOLD", "M1 physical full-width trace", PUBLIC_REPRO_PANEL_URL],
            ["fascia/LCD/inner-vent common centreline", f"X={PANEL_CENTRELINE_X:.1f}; inner vents X={VENT_CENTRES[1][0]:.1f}/{VENT_CENTRES[2][0]:.1f}", f"parametric Rev H constraint: LCD centre equals fascia centreline; inner-pair midpoint equals same centreline; equal offsets ±{INNER_VENT_CENTRE_OFFSET:.1f}", "MATHEMATICALLY_EXACT_IN_NOMINAL_MODEL", "HOLD for physical transfer", "M1 + M5 + M9", ""],
            ["OEM glovebox", "210 mm nominal visual envelope = 16.67% of model width", "source-photo proportional measurement; Toyota parts fitment family provides no public 1978 RHD lid/hinge dimensional drawing", "VISUAL_RATIO_ONLY; PHYSICAL_TRANSFER_REQUIRED", "HOLD", "M2 direct trace and opening sweep", TOYOTA_EPC_URL],
            ["OEM speedometer / cluster", f"{SPEEDO_ENVELOPE[2]:.0f} mm schematic visual envelope = {100*SPEEDO_ENVELOPE[2]/PANEL_W:.2f}% of model width; {SPEEDO_ENVELOPE[2]/GLOVEBOX_ENVELOPE[2]:.2f} x glovebox envelope", "source-photo proportional placeholder only; perspective has no scale datum and Toyota parts fitment family provides no public 1978 RHD cluster dimensional drawing", "VISUAL_RATIO_ONLY; PHYSICAL_TRANSFER_REQUIRED", "HOLD", "M3 direct transfer of the existing factory opening, rear depth, mounts, column relationship and sight line; do not relocate", TOYOTA_EPC_URL],
            ["steering-column relief and swept keep-out", f"axis X={STEERING_COLUMN_AXIS_X:.1f}; relief width {2*STEERING_COLUMN_RELIEF_HALF_W:.0f}, rise {STEERING_COLUMN_RELIEF_RISE:.0f}; keep-out {STEERING_COLUMN_KEEP_OUT[2]:.0f} x {STEERING_COLUMN_KEEP_OUT[3]:.0f}", "Rev H packaging intent inferred from owner photo; no public vehicle-specific RHD column interface drawing located", "NOMINAL_LAYOUT_ONLY", "HOLD / DO NOT CNC", "M1 + M3 + M8 + M9 direct column/shroud/stalk/sweep trace and 1:1 mock-up", ""],
            ["LCD active-image reference", "199.2 x 112.1; 228.6 diagonal", "mathematical 9-inch 16:9 reference; Sehgal local listing states 9-inch but has no chassis/cutout drawing", "REFERENCE_ONLY", "HOLD", "M4-M5 bought sample and manufacturer drawing", "https://sehgalmotors.pk/products/universal-android-lcd-tab-9-inches-with-wiring-without-main-grip"],
            ["LCD bezel/aperture/support", "224 x 136 / 202 x 115 / 246 x 158 nominal", "design envelope only", "PHYSICAL_TRANSFER_REQUIRED", "HOLD", "M4-M5", ""],
            ["generic silver vent family", "face Ø87; panel opening Ø75", "Joom listing; cross-check only, generic variants have spigot/retainer variation", "PUBLISHED_LISTING_REFERENCE", "HOLD", "M7 received matched four-piece sample batch + calipers", "https://www.joom.com/en/products/68c8f9fa6dffb3012ca80d30"],
            ["high outer / lowered inner vent layout", f"centres={VENT_CENTRES}; outer bezel-top Y={OUTER_VENT_TOP_DATUM_Y:.1f}; inner face-top Y={INNER_VENT_CENTRE_Y+VENT_FACE_DIAMETER/2:.1f}; pod-bottom Y={PANEL_MIN_Y:.1f}", "Rev H layout decision; inner pair is exactly symmetric about LCD/fascia centreline and clears the LCD vertically; outer faces remain high near usable ends", "DESIGN_LOCKED_IN_NOMINAL_MODEL", "HOLD for vehicle, bought-part and driver-clearance transfer", "M1 + M7 + M8 + M9", ""],
            ["V4 right-outlet / control-bank relationship", f"nominal Ø22.5 head gap={V4_NOMINAL_SELECTOR_HEAD_CLEARANCE:.2f}; lower V4 rim to bank/label envelope={V4_CONTROL_ENVELOPE_NOMINAL_GAP:.0f}; end lands visible/cut=6.5/12.5", f"Straight-on bare-shell overlay controls visual placement only; the nominal head gap passes the ≥{MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE:.0f} face-layout target, while {V4_CONTROL_ENVELOPE_NOMINAL_GAP:.0f} mm is to the conservative bank/label envelope; V4 cannot move farther right without reducing already-minimal end lands", "NOMINAL_VISUAL_RELATION_ONLY", "HOLD", f"M6 actual selector head clearance ≥{MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE:.0f}; M7 vent sample; M8-M9 rear retainer/neck/elbow/duct clearance ≥{MIN_STATIC_REAR_CLEARANCE:.0f} to contact blocks/terminals/wiring", ""],
            ["extreme-right two-row control bank", f"columns X={CONTROL_COLUMNS}; top Y={CONTROL_TOP_Y}; bottom Y={CONTROL_BOTTOM_Y}; {CONTROL_COLUMNS[1]-CONTROL_COLUMNS[0]:.0f} mm horizontal / {CONTROL_TOP_Y-CONTROL_BOTTOM_Y:.0f} mm vertical pitch", "Rev H V6 packaging decision: S1-S4 top and S5-S8 bottom, compacted and centred in the existing shallow channel, wholly right of the nominal steering-column keep-out", "DESIGN_LOCKED_IN_NOMINAL_MODEL", "HOLD for physical part, lever sweep, duct, column and driver checks", "M6 + M8 + M9", ""],
            ["Schneider-style selector aperture", "Ø22.5", "Schneider Electric Harmony XB4 published mounting diameter", "VERIFIED_PRODUCT_STANDARD", "HOLD to bought-part confirmation", "M6 part-code photo + calipers", "https://shop.se.com/pro/us/en/product/selector-switch-harmony-xb4-black-22mm-3-positions-stay-put-2no/"],
            ["Schneider-style selector rear envelope", "68", "Schneider Electric Harmony XB4 published complete depth", "VERIFIED_PRODUCT_STANDARD", "HOLD to bought-part confirmation", "M6 part-code photo + rear-stack trial", "https://shop.se.com/pro/us/en/product/selector-switch-harmony-xb4-black-22mm-3-positions-stay-put-2no/"],
            ["hazard aperture", "Ø16 nominal", "no selected/published hazard part drawing", "REFERENCE_ONLY", "HOLD", "M6 actual part", ""],
        ])

    with (OUT / "visual_ratio_schedule.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "ratio_id", "numerator_feature", "numerator_mm", "denominator_feature",
            "denominator_mm", "ratio", "visual_use", "production_status",
        ])
        writer.writerows([
            ["R1", "LCD active width", LCD_ACTIVE_W, "LCD active height", LCD_ACTIVE_H, f"{LCD_ACTIVE_W/LCD_ACTIVE_H:.6f}", "true 16:9 active-image proportion", "M4 sample/drawing controls"],
            ["R2", "vent visible face", VENT_FACE_DIAMETER, "LCD bezel width", LCD_BEZEL_W, f"{VENT_FACE_DIAMETER/LCD_BEZEL_W:.6f}", "each vent must read as 38.84% of the screen bezel width", "vent face design lock; M4/M7 physical samples control"],
            ["R3", "LCD active width", LCD_ACTIVE_W, "vent visible face", VENT_FACE_DIAMETER, f"{LCD_ACTIVE_W/VENT_FACE_DIAMETER:.6f}", "screen active image reads 2.29 vent diameters wide", "visual check only"],
            ["R4", "selector panel cut", SELECTOR_DIAMETER, "vent visible face", VENT_FACE_DIAMETER, f"{SELECTOR_DIAMETER/VENT_FACE_DIAMETER:.6f}", "selector cut is 25.86% of vent face; visible head still sample-dependent", "M6 bought part controls"],
            ["R5", "control horizontal pitch", CONTROL_COLUMNS[1] - CONTROL_COLUMNS[0], "vent visible face", VENT_FACE_DIAMETER, f"{(CONTROL_COLUMNS[1]-CONTROL_COLUMNS[0])/VENT_FACE_DIAMETER:.6f}", "compact two-row spacing", "M6/M9 1:1 trial controls"],
            ["R6", "glovebox visual envelope", GLOVEBOX_ENVELOPE[2], "nominal panel width", PANEL_W, f"{GLOVEBOX_ENVELOPE[2]/PANEL_W:.6f}", "source-photo-calibrated visual proportion", "M2 direct trace controls"],
            ["R7", "cluster visual envelope", SPEEDO_ENVELOPE[2], "nominal panel width", PANEL_W, f"{SPEEDO_ENVELOPE[2]/PANEL_W:.6f}", "source-photo-calibrated visual proportion", "M3 direct trace controls"],
            ["R8", "cluster visual envelope", SPEEDO_ENVELOPE[2], "glovebox visual envelope", GLOVEBOX_ENVELOPE[2], f"{SPEEDO_ENVELOPE[2]/GLOVEBOX_ENVELOPE[2]:.6f}", f"schematic retained-item ratio {SPEEDO_ENVELOPE[2]/GLOVEBOX_ENVELOPE[2]:.2f}:1 only", "visual placeholder only; M2/M3 direct traces control"],
            ["R9", "steering-column relief width", 2 * STEERING_COLUMN_RELIEF_HALF_W, "nominal panel width", PANEL_W, f"{2*STEERING_COLUMN_RELIEF_HALF_W/PANEL_W:.6f}", "visible nominal relief intent under cluster", "HOLD; M1/M3/M9 direct trace controls"],
        ])

    with (OUT / "component_procurement_and_sample_plan.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["component", "preferred_path", "published_reference", "Pakistan_cost_availability_status", "fabrication_instruction", "source_url"])
        writer.writerows([
            ["9-inch LCD", "Sehgal Motors universal Android LCD Tab 8227 (baseline only)", "9-inch listing; no chassis/cutout/mount dimensions", "listed locally; obtain one sample or mechanical drawing before CNC", "Do not release bezel/aperture/carrier until M4-M5", "https://sehgalmotors.pk/products/universal-android-lcd-tab-9-inches-with-wiring-without-main-grip"],
            ["four silver A/C vents", "Pakistan automotive A/C parts counter: buy four matched generic 87/75 silver/chrome ABS units from one batch", "Joom generic reference: face Ø87, opening Ø75, 2-pack", "local sample route required; compare landed/local set cost before purchase", "Use only after M7 measures face, cut, retainer, spigot and depth; Ø75 is NOT a released cut", "https://www.joom.com/en/products/68c8f9fa6dffb3012ca80d30"],
            ["Daraz generic outlet lead", "do not specify", "listing is undimensioned and currently unavailable", "not an available procurement route", "Do not base drawing or price on this listing", "https://www.daraz.pk/products/hi-mall-dashboard-air-conditioner-outlet-vent-deflector-trim-universal-rotatable-round-for-cars-rvs-buses-i260429416.html"],
            ["premium exact-dimension vent fallback", "Restomod Air Diablo billet outlet", "face Ø95.25, panel hole Ø63.50, rear depth 50.80, 2-inch duct", "import/premium fallback, not cost baseline", "Only substitute after redesigning M7 aperture/duct detail to manufacturer data", "https://restomodair.com/shopproducts/diablo-with-cap-screws-salt-flat-billet-aluminum-a-c-vent/"],
            ["seven existing selectors", "purchased Schneider Harmony-style 22 mm selectors: 3 x three-position + 4 x two-position", "Schneider Harmony XB4 mounting Ø22.5; complete depth 68", "already bought per project records; part code/physical geometry still to confirm", "M6 caliper and rear-stack trial before cutting; provide exactly 7 selector holes plus separate hazard", "https://shop.se.com/pro/us/en/product/selector-switch-harmony-xb4-black-22mm-3-positions-stay-put-2no/"],
        ])

    with (OUT / "hvac_control_interface_schedule.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["item", "dashboard_input", "required_interface", "compatibility_status", "release_test", "instruction"])
        writer.writerows([
            ["ordered cabin evaporator/cool-heat unit", "none assumed", "retain delivered thermostat/controller and identify every terminal", "UNKNOWN_PENDING_DELIVERY: AliExpress order 3073062248277489 has no recorded manufacturer/model, wiring diagram, load data or control topology", "photograph labels/connectors; record blower/clutch/thermostat/blend pinout and current; bench test before panel closeout", "Do not delete or imitate its variable controller until the received unit proves what is required"],
            ["blower", "BLOWER 3-position maintained: OFF/LOW/HIGH", "low-current requests into a measured resistor pack, speed relays or compatible PWM controller", "CONDITIONALLY_COMPATIBLE: works only after the delivered blower/control topology is identified; selector never carries motor current", "measure motor inrush/running current; prove OFF/LOW/HIGH and fuse/relay/wire temperature", "If the unit uses a potentiometer, proprietary PCB or more than two speeds, retain its controller or design a measured interface; do not wire the selector directly"],
            ["compressor request", "A/C 2-position maintained: OFF/ON", "B1 request through evaporator thermostat/freeze protection plus low/high pressure chain", "FUNCTIONALLY_APPROPRIATE_AS_LOW_CURRENT_REQUEST_ONLY", "prove thermostat cutout, pressure cutout, clutch relay and no clutch operation with blower OFF if required by selected system", "No compressor-clutch current through the selector"],
            ["condenser fan", "no dashboard selector", "automatic T4 relay request from trinary pressure switch/system logic", "CORRECT_NOT_TO_ALLOCATE_A_VISIBLE_SWITCH", "prove fan cut-in/cut-out with pressure logic and fused measured load", "Do not use AUX or SPOTS as routine condenser-fan control"],
            ["cabin temperature / evaporator freeze control", "no variable dashboard input in the bought seven-selector set", "retain the delivered thermostat or mount a matched remote thermostat/controller in a discreet serviceable position", "NOT_REPLACEABLE_BY_A_2_POSITION_SELECTOR_WITHOUT_ENGINEERING", "temperature sweep and evaporator freeze-protection test", "This control is outside the seven-selector count"],
            ["heat / blend / water valve if the cool-heat unit actually provides heat", "no assigned selector", "retain delivered mechanical/electrical blend control or add its required separate matched control", "UNKNOWN_PENDING_PHYSICAL_INSPECTION", "prove full cold/full heat and safe valve/door operation", "Do not claim heat control from the A/C ON/OFF selector"],
            ["four fascia outlets", "direction set manually at each louver", "balanced four-branch plenum and sample-matched hose/adaptors", "MECHANICAL_HOLD_PENDING_M7_M8", "measure each vent/spigot and compare outlet flow", "All four faces are nominal Ø87 with Ø75 opening reference only"],
        ])


def write_prompt_record() -> None:
    text = f"""# Rev H visualisation prompt record

Mode: built-in `image_gen`, local-reference `precise-object-edit`.

## Straight-on bare-shell edit prompt

Precise object edit of this existing straight-on Toyota J40 dashboard visualization. Change only the two inner/centre silver circular A/C outlets and their body-colour rounded pods. Set the final inner-outlet position so their centres are visibly about 1.71 outlet-face diameters lower than the high outer-outlet centres in the dashboard plane, while preserving their exact left/right X positions, equal size, satin-silver rims, dark directional cores, and exact symmetry about the LCD. The final top of each inner silver rim must sit about 0.14 outlet-face diameter below the LCD bezel bottom (the nominal drawing ratio is 12.5/87), with clear body-colour separation. Extend each cream rounded pod downward locally so its bottom remains about 0.13 outlet-face diameter below the rim bottom (nominal ratio 11.5/87). Keep the outer two vents at their current high positions. Do not move, resize, restyle, replace, or redraw the true 9-inch LCD, original Toyota speedometer and auxiliary cluster in its factory opening, original glovebox and black plate, steering-column relief, seven rotary switches, red hazard, labels, vehicle, camera, colour, patina, background, or any other object. Keep exactly 4 vents, exactly 7 rotary selectors, and exactly 1 red hazard. No full-width downward dashboard extension; only the two local vent pods get deeper. Photorealistic, same resolution and composition. The image expresses ratios only; it is never scaled for CNC.

## Assembled driver-eye edit prompt

Precise object edit of this existing assembled driver-eye Toyota J40 dashboard visualization. Change only the two inner/centre silver circular A/C outlets and their body-colour rounded pods. Set the final inner-outlet position so their centres are about 1.71 outlet-face diameters lower than the high outer-outlet centres in the true dashboard plane, preserving their exact left/right X positions in the panel, equal physical size, satin-silver rims, dark directional cores, and exact symmetry about the true panel/LCD centreline despite perspective. The final top of each inner silver rim must sit about 0.14 outlet-face diameter below the LCD bezel bottom in the dashboard plane (nominal ratio 12.5/87), with clear body-colour separation. Extend each cream rounded pod downward locally so its bottom remains about 0.13 outlet-face diameter below the rim bottom (nominal ratio 11.5/87). Keep the outer two vents at their current high positions. Keep the right inner vent and its rear duct visibly clear of the original steering column and shroud. Do not move, resize, restyle, replace, or redraw the true 9-inch LCD, original Toyota speedometer and auxiliary cluster in its factory opening directly above the steering column, original glovebox and black plate, steering wheel, column, column shroud, stalks, seven rotary switches, red hazard, labels, vehicle, camera, colour, patina, background, or any other object. Keep exactly 4 vents, exactly 7 rotary selectors, and exactly 1 red hazard. No full-width downward dashboard extension; only the two local vent pods get deeper. Photorealistic, same resolution, camera and composition. The image expresses ratios only; it is never scaled for CNC.

The two approved outputs are copied into this package as the straight-on and assembled Rev H overlays. The supplied selector photograph is copied as `industrial_rotary_selector_reference.png`.

Generated overlays show visual intent only. The nominal drawing sets the inner vent centres at Y={INNER_VENT_CENTRE_Y:.1f} mm and the pod bottoms at Y={PANEL_MIN_Y:.1f} mm. Their nominal visible rim-to-LCD gap is {LCD_BEZEL[1]-(INNER_VENT_CENTRE_Y+VENT_FACE_DIAMETER/2):.1f} mm, but M9 requires at least {MIN_INNER_VENT_LCD_VISIBLE_GAP:.0f} mm as built. DXF/CSV dimensions, direct vehicle traces, M1-M10 physical templates and bought-part measurements control fabrication; M1/M3/M7/M8/M9 must establish the installed column, duct, vent and driver clearances before production cutting.

## 2026-08-01 assembled V4 / steering-column correction record

Output: `layout_variants_20260801/layout_b_column_v4_clearance_assembled.png`.

Mode: built-in `image_gen`, local-reference `precise-object-edit`.

Correction intent: restore **only** the short horizontal matte-black steering-column/shroud section from the wheel hub into the existing factory lower-instrument relief. It must never become a wheel spoke or a diagonal tube. Lower the complete right-hand 2 x 4 control bank enough to show roughly one actual selector-head diameter between the V4 rim and its nearest selector head; preserve the complete control allocation, labels, right edge and all other dashboard identity. Freeze the original glovebox, original speedometer/cluster, true 9-inch LCD, four outlet sizes/finish, factory camera/vehicle, colour and patina. This is a visual correction record, not a dimensional release: the straight-on bare-shell overlay remains the visual placement control, and M6/M8/M9 establish the actual V4 selector and rear-duct clearances.

## 2026-08-01 V5 / visible installed steering-column pair

Outputs:

- `layout_variants_20260801/layout_b_column_v5_clear_assembled.png`
- `layout_variants_20260801/layout_b_column_v5_straight_on.png`

Mode: built-in `image_gen`, local-reference `precise-object-edit`.

Correction intent: use `photos/20260317_165113.jpg` and `photos/20260323_190047.jpg` as the original-column geometry controls. In the oblique view, show one uninterrupted near-horizontal matte-black column/shroud from the existing wheel hub into the factory radiused relief beneath the OEM cluster. In the straight-on view, install one original-scale right-hand-drive wheel and the same continuous column, with the hub/shaft centreline directly beneath the retained OEM meter. Freeze the approved true 9-inch LCD, original glovebox, four vents, and seven-selector-plus-red-hazard allocation. These images show placement and occlusion only; the signed vehicle trace and M1/M3/M8/M9 mock-up remain controlling.

## 2026-08-01 V6 / explicit column and centred compact control bank

Outputs:

- `layout_variants_20260801/layout_b_column_v6_switches_clear_assembled.png`
- `layout_variants_20260801/layout_b_column_v6_switches_straight_on.png`

Mode: built-in `image_gen`, local-reference `precise-object-edit`.

Correction intent: in the oblique view, make the original matte-black column/shroud mechanically explicit from the existing wheel hub to the factory relief directly below the OEM meter. Move the complete control allocation down and right as one compact 2 x 4 group in both views, without rearranging functions. The nominal model now uses columns X={CONTROL_COLUMNS}, rows Y={CONTROL_TOP_Y:.0f}/{CONTROL_BOTTOM_Y:.0f}, and a {CONTROL_COLUMNS[1]-CONTROL_COLUMNS[0]:.0f} mm horizontal pitch. That places the bank centrally inside its existing shallow Y={CONTROL_BANK[1]:.0f} local channel; it does not increase overall dashboard height. Preserve exactly seven black selectors plus one separate red hazard, labelled WIPERS / LIGHTS / SPOTS / AUX. and BLOWER / A/C / ENGINE / HAZARD. Freeze the true 9-inch LCD, four vents, OEM speedometer, OEM glovebox, steering-wheel scale, camera and vehicle identity. The bought head and lever sweep still require the M6 full-size trial before any aperture is released.
"""
    (OUT / "visualisation_prompt_record.md").write_text(text, encoding="utf-8")


def write_rear_envelope_fit_audit() -> None:
    audit = f"""# Rev H rear-envelope fit audit — 2026-08-01

## Release decision

Rev H is a coherent **nominal visual/template layout**, not a production-cleared rear package. The complete dashboard face, LCD carrier, four vents/ducts, retained speedometer, glovebox, RHD steering column and right control bank remain **HOLD**. M1-M9 require a full-depth 1:1 mock-up using the actual vehicle and bought components before any metal or vehicle cut is released.

## V4 (top-right outlet) / selector-bank control

- The straight-on bare-shell overlay is the visual placement control for V4; the assembled view is useful only for correcting the column and driver-eye appearance. Neither image is scale evidence.
- With the reference Ø{SELECTOR_DIAMETER:.1f} selector head, the nominal visible V4-rim-to-nearest-head gap is **{V4_NOMINAL_SELECTOR_HEAD_CLEARANCE:.2f} mm**, so the face layout passes the **≥{MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE:.0f} mm** target. M6 must repeat this with the bought head and its lever sweep.
- The smaller lower-V4-rim to top-of-bank figure is **{V4_CONTROL_ENVELOPE_NOMINAL_GAP:.0f} mm**. It is to the conservative rectangular bank/label envelope, not to the selector head itself; actual label and hand clearance remain part of M6.
- Do not move V4 farther right. Its nominal visible-face land is already **6.5 mm** and its Ø75 opening-reference land is **12.5 mm** from the usable-face end. M1/M7 must confirm actual retained metal, return and retainer land.
- M6 must install the purchased selector heads and prove at least **{MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE:.0f} mm** from the visible V4 rim to the nearest actual selector head, including label and lever-sweep clearance.
- M8/M9 must prove at least **{MIN_STATIC_REAR_CLEARANCE:.0f} mm** from the V4 retainer, neck, elbow and duct to the actual selector contact blocks, terminals and wiring. Route and loom retention must be checked at full depth, not inferred from the face drawing.

## Other rear-envelope dependencies

- M1/M3/M9 must trace the installed RHD column, shroud, stalk sweep, support bracket and the factory cluster opening; the nominal column keep-out is not a vehicle measurement.
- M4/M5 must establish LCD chassis depth, connectors, cable bend, cooling and carrier load path. The 9-inch active-image calculation does not define its rear body.
- M7/M8 must use one received four-piece vent batch to establish actual retainer, spigot, elbow, hose ID and bend radius, then mock all four ducts with the speedometer, glovebox sweep, LCD carrier, column and control-bank rear stacks present.

## Project-photo rear-space observations

The project photographs corroborate the occupied zones behind the face, but none includes a reliable depth datum and therefore none releases rear packaging:

- `photos/20260323_190005.jpg` shows the existing under-dash A/C assembly and loose wiring below/behind the fascia. The central and lower dashboard volume is partitioned and occupied, not an unrestricted full-width cavity.
- `photos/20260323_190047.jpg` shows the installed RHD column/shroud, column support and loom consuming the inner-right/driver-side volume. This makes V3's neck/elbow/duct and the LCD/cluster carrier critical M8-M9 checks.
- `photos/20260413_040719.jpg` shows the stripped factory face and retained structure/bulkhead through the central and cluster openings. LCD depth, connector exit and carrier load path cannot be inferred from the visible aperture.
- `photos/20260422_074709_gp_o4wiXyjA.jpg` is useful for gross face placement only; it is not calibrated evidence for the rear depth or the glovebox/column sweep.
- `photos/20260320_191834.jpg`, `20260320_191846.jpg`, `20260320_192143.jpg`, `20260320_192148.jpg` and `20260320_192153.jpg` show the loom currently occupying or obscuring the exact rear zones. Loom routing and retention must be included in the full-depth mock-up.

## Zone-by-zone rear fit verdict

| Zone | Nominal face result | Rear-package verdict and release proof |
|---|---|---|
| Central 9-inch LCD | Active image and bezel fit the face layout. | **CONDITIONAL / HOLD.** Measure the bought chassis, rear connectors, bend radius, cooling and retained structure; prove a service-removable carrier at M4-M5/M9. |
| V1 left outer | Face and end land are coherent. | **CONDITIONAL / HOLD.** Prove retainer, neck and elbow against the original glovebox body, hinge/latch and full opening sweep at M2/M7-M9. |
| V2 left inner | Face clears the LCD; its nominal pod sits close to the glovebox placeholder. | **CRITICAL / HOLD.** The nominal envelopes have only about 1.5 mm vertical separation; directly mock the real glovebox sweep, vent retainer and duct at M2/M7-M9. |
| V3 right inner | Face clears the LCD and nominal column keep-out. | **CRITICAL / HOLD.** Prove the real column/shroud/stalk/support sweep with at least **{MIN_MOVING_COLUMN_CLEARANCE:.0f} mm** to moving parts and **{MIN_STATIC_REAR_CLEARANCE:.0f} mm** to fixed hardware at M1/M3/M8-M9. |
| V4 right outer + control bank | Visible rim to nominal Ø{SELECTOR_DIAMETER:.1f} head is **{V4_NOMINAL_SELECTOR_HEAD_CLEARANCE:.2f} mm**, passing the face target. | **CRITICAL / HOLD.** The outlet retainer/neck/elbow/duct must remain at least **{MIN_STATIC_REAR_CLEARANCE:.0f} mm** from the measured 68 mm-reference selector contact stacks, terminals, wiring and retained loom at M6/M8-M9. |
| OEM cluster / switch-bank boundary | Visible envelopes are adjacent but do not overlap. | **CONDITIONAL / HOLD.** Prove cluster plugs/harness service loops and every selector stack at full depth; nominal face spacing is not rear clearance. |

## Ordered HVAC unit status

The recorded candidate is AliExpress order `3073062248277489`, described as a universal four-hole 12 V cool/heat evaporator. The project record contains no manufacturer/model, installation drawing, cabinet dimensions, outlet/spigot geometry, wiring diagram, current data or control topology. No evaporator cabinet is assumed to fit inside the shallow fascia: the behind-face package covered here is the LCD body, four outlet necks/elbows/ducts, selector stacks, OEM cluster/glovebox and steering assembly. The evaporator needs a separately measured under-dash/bulkhead/tunnel mounting location and service-removal route. Its ability to occupy that location, feed four ducts or accept the specified two-/three-position commands **cannot be certified before delivery**. On receipt, photograph its labels and connectors; measure the complete cabinet, mounts, outlets and service-removal path; bench-identify blower/thermostat/blend/compressor-request behaviour; then include the physical cabinet and all four full-length ducts in the M8-M9 vehicle mock-up.

## Required evidence before production release

| Gates | Evidence required |
|---|---|
| M1-M3 | Full vehicle trace/template, factory glovebox/cluster/column transfer and rear-depth records. |
| M4-M5 | LCD manufacturer drawing or calipers, rear carrier and removal mock-up. |
| M6 | Actual selector-head/label/sweep and contact-stack measurements; 1:1 V4-to-selector clearance proof ≥{MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE:.0f} mm. |
| M7 | Four matched vent samples, retainer/neck measurements and confirmed end lands. |
| M8-M9 | Full-depth mock-up with all vents, ducts, LCD, controls, loom, retained components and full column/stalk sweep; V4 rear clearance proof ≥{MIN_STATIC_REAR_CLEARANCE:.0f} mm. |

No rendered image, nominal CSV coordinate or flat fit template substitutes for this evidence.
"""
    (OUT / "rear_envelope_fit_audit_20260801.md").write_text(audit, encoding="utf-8")


def write_readme() -> None:
    readme = f"""# J40 RHD full-width 9-inch LCD / four-outlet dashboard - Rev H

Rev H replaces the complete visible dashboard face with one restrained body-colour CNC-formed panel while retaining and transferring the original Toyota speedometer assembly and the original asymmetric glovebox lid, knob, hinges/latch and black instruction plate. The ashtray is deleted. A true 9-inch display reference sits centrally. Exactly four larger silver circular A/C outlets are used: the two end outlets remain high, while the symmetric inner pair sits wholly below the LCD in two local rounded pods. The normal lower edge is not dropped full-width. It rises around the right-hand-drive steering column in a radiused U-relief, and all controls sit in a compact two-row bank at the extreme right.

This package is ready to send for **quotation and a full-size disposable CNC template**. It is deliberately not a production vehicle-cut release: the nominal coordinate envelope is X=0…{PANEL_W:.0f} mm and Y={PANEL_MIN_Y:.0f}…{PANEL_H:.0f} mm ({PANEL_W:.0f} x {PANEL_H-PANEL_MIN_Y:.0f} mm overall only where the local pods project) and cannot replace a physical trace of this vehicle. Only `CUT_TEMPLATE_OUTER` in `full_width_fit_template_rev_h.dxf` may be cut now, and only in MDF/card/cheap plastic. Every metal or vehicle feature remains `HOLD_*` until M1-M10 are signed.

## Locked layout

- Right-hand drive. Passenger is left; driver is right.
- One full-width visible face in 1.5 mm CR4 mild steel, low-gloss body colour.
- Original glovebox and speedometer are retained/reinstalled; their exact shapes and mounts are direct-transfer features, not nominal CNC geometry. In every owner-photo visual they are also **visual no-touch regions**: preserve their original colour, finish, patina, markings, controls and location exactly. The bare-shell visual may add only the correct original cluster copied from the assembled owner-photo reference into its existing factory opening.
- Screen active-image reference: **199.2 x 112.1 mm**, **228.6 mm / 9.000 inch diagonal**, 16:9. Its centre is constrained to the fascia centreline at nominal **X{PANEL_CENTRELINE_X:.1f}/Y{LCD_CY:.1f}**. This does not establish a real LCD chassis: the local Sehgal 9-inch listing has no mechanical drawing, so its aperture, bezel, rear body, mounts and connectors are M4-M5 HOLD.
- Four matching generic vents: **Ø87 visible silver/chrome face** and **Ø75 panel-opening reference**, dark directional core, hidden retention. Nominal centres are {VENT_CENTRES}. V1/V4 remain high at **Y={OUTER_VENT_CENTRE_Y:.1f}**, with their Ø87 bezel tops at **Y={OUTER_VENT_TOP_DATUM_Y:.1f}**, aligned with the LCD-bezel top. V2/V3 are lowered to **Y={INNER_VENT_CENTRE_Y:.1f}**; each visible face spans Y={INNER_VENT_CENTRE_Y-VENT_FACE_DIAMETER/2:.1f}…{INNER_VENT_CENTRE_Y+VENT_FACE_DIAMETER/2:.1f} and therefore sits {LCD_BEZEL[1]-(INNER_VENT_CENTRE_Y+VENT_FACE_DIAMETER/2):.1f} mm below the nominal LCD-bezel bottom at Y={LCD_BEZEL[1]:.1f}. Their identical local pods descend to **Y={PANEL_MIN_Y:.1f}**, {MAIN_LOWER_Y-PANEL_MIN_Y:.0f} mm below the normal Y={MAIN_LOWER_Y:.1f} edge. The inner pair is exactly mirrored at **X={VENT_CENTRES[1][0]:.1f} / {VENT_CENTRES[2][0]:.1f}**, or **±{INNER_VENT_CENTRE_OFFSET:.1f} mm** about the LCD/fascia centreline. Ø75 is **not** a released production cut.
- The upper band remains **OEM glovebox | centred 9-inch LCD | OEM speedometer**. The outer vents occupy the far ends; the lowered inner pair uses otherwise empty space below and either side of the LCD without overlapping its bezel.
- The outer visible vent faces sit **6.5 mm** from the nominal usable-face ends; their Ø75 reference cuts retain **12.5 mm**. These tight lands are template/sample controlled and the outlets never move into the side returns.
- The nominal RHD steering-column axis is **X={STEERING_COLUMN_AXIS_X:.1f}**, aligned with the retained cluster centre. The lower edge has a **130 mm-wide x 32 mm-rise** radiused U-relief and a nominal **130 x 105 mm** swept keep-out. These dimensions communicate packaging intent only: M1/M3/M9 must directly trace the installed column, shroud, stalks, bracket and full movement before any production cut. No switch, duct, carrier or rear stack may enter the signed keep-out.
- At the extreme right, fully outside that keep-out, exactly seven industrial rotary selectors plus one separate red hazard form **two rows of four**. Nominal columns are **X={CONTROL_COLUMNS}**, with top **Y={CONTROL_TOP_Y:.0f}** and bottom **Y={CONTROL_BOTTOM_Y:.0f}**: {CONTROL_COLUMNS[1]-CONTROL_COLUMNS[0]:.0f} mm horizontal / {CONTROL_TOP_Y-CONTROL_BOTTOM_Y:.0f} mm vertical pitch. The V6 bank is compacted, shifted right and lowered within the same shallow Y={CONTROL_BANK[1]:.0f} control channel; dashboard height is unchanged. Schneider Harmony XB4 reference: **Ø22.5 panel cut** and **68 mm rear envelope**. Head/lever sweep, anti-rotation, right-outlet duct route, rear stacks and driver clearance remain M6/M8/M9 HOLD. Engrave labels 3 mm high with black infill.

## V4 / right-side rear-envelope control

The V6 straight-on installed view supersedes the earlier views for control-bank placement; the straight-on bare-shell overlay remains the visual placement control for the fixed top-right outlet (V4). With the nominal Ø{SELECTOR_DIAMETER:.1f} head, the drawn V4-rim-to-nearest-selector gap is **{V4_NOMINAL_SELECTOR_HEAD_CLEARANCE:.2f} mm**, so it passes the **≥{MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE:.0f} mm** face-layout target. The smaller **{V4_CONTROL_ENVELOPE_NOMINAL_GAP:.0f} mm** relationship is to the conservative rectangular bank/label envelope, not to the selector head. M6 must repeat the head, label and lever-sweep check using the bought controls. M8/M9 must prove at least **{MIN_STATIC_REAR_CLEARANCE:.0f} mm** from V4's actual retainer, neck, elbow and duct to selector contact blocks, terminals and wiring. V4 must not be moved farther right: its nominal end lands are already 6.5 mm visible-face / 12.5 mm Ø75 opening-reference. See `rear_envelope_fit_audit_20260801.md`; the full-depth M1-M9 mock-up controls release.

## Exact visible controls

| Position | Label | Hardware / states | What it does |
|---|---|---|---|
| Top 1/4 | WIPERS | 3-position: OFF / LOW / HIGH | Parks the wipers in OFF and selects low or high wipe. |
| Top 2/4 | LIGHTS | 3-position: OFF / SIDE / HEAD | Selects master exterior-light state; original dip/high-low remains. |
| Top 3/4 | SPOTS | 2-position: OFF / ON | Commands T5 spot-lamp relay. |
| Top 4/4 | AUX. | 2-position: OFF / ON | Commands reserved accessory relay B2. |
| Bottom 1/4 | BLOWER | 3-position: OFF / LOW / HIGH | Sends OFF/LOW/HIGH requests to the measured blower controller. |
| Bottom 2/4 | A/C | 2-position: OFF / ON | Requests B1 compressor cooling through thermostat/trinary/pressure safeties. |
| Bottom 3/4 | ENGINE | 2-position: RUN / STOP | Sends a low-current command through the validated fuel-stop interface; key OFF remains authoritative and the manual cable remains the fallback. |
| Bottom 4/4 | HAZARD | separate red pushbutton: OFF / FLASH | Operates the hazard/flasher circuit. |

The bank contains exactly **7 selectors + 1 hazard**. The formerly unallocated seventh selector is now `ENGINE`, with `RUN / STOP` engraving. It is a command device only: do not route stop-solenoid or motor current through it. Before wiring, EEI-003 must identify whether this vehicle uses an energise-to-run or energise-to-stop device and establish a fail-safe relay/controller interface. Key OFF must always stop the engine, and the original/manual diesel stop cable remains the independent mechanical fallback. The earlier concealed-needle fuel-stop plan is superseded; that part may remain uninstalled or be reassigned only after a separate security review. Also retain the original indicator stalk, dip/high-low control, horn actuation, keyed ignition, winch third lever and identified mechanical cables.

All selectors command fused relay/controller inputs only. No selector carries lamp, wiper-motor, blower, compressor-clutch, fuel-stop-device or accessory load current. Baseline mapping: T1 low beam, T2 high beam, T3 horn, T4 condenser fan, T5 spots, B1 A/C clutch request and B2 AUX. B3-B5 remain unassigned relay capacity until EEI-003 selects the correct ENGINE interface. Size the blower and A/C branches after actual current measurement. At M10 prove wiper park with washer retained separately, the complete OFF/SIDE/HEAD lighting truth table with original dip selection, measured blower control, A/C safety/fan logic, isolated hazard logic, and ENGINE RUN/STOP plus authoritative key-off and manual-cable fallback.

Cabin temperature/blend is deliberately outside the seven-selector allocation. Retain the delivered evaporator's measured thermostat/controller, and add a separate matched remote thermostat or heat/blend control only if physical inspection proves it is required. The visible `A/C` selector is compressor request only and remains interlocked through thermostat and pressure safeties.

## Construction intent

- Laser or waterjet the final face only after approved production geometry is derived from the signed template. Press-form returns after a cheap-sheet trial.
- Keep the visible face one piece. Concealed rear stiffener rails, local vent rings/doublers and the LCD carrier may be separate and welded, riveted or bolted as appropriate.
- Use approximately 15 mm returns where the vehicle permits. Where the compact right control channel prevents a continuous fold, use a concealed rear flange/doubler rather than exposed fasteners.
- Transfer LCD mass and control loads into retained cowl/dashboard structure through a rear carrier; never hang the display from the 1.5 mm skin alone.
- Use hidden M5 service fasteners at no more than 150 mm pitch where the physical structure permits. Allow cabin-side removal of the LCD and vents.
- Do not cut or weaken the cowl, A-pillars, firewall or steering-column support. Establish a continuous 20-25 mm attachment land where the vehicle permits.
- Cut approved vehicle sheet initially undersize, trim progressively, radius/deburr every edge and epoxy-prime exposed steel immediately.

## HVAC packaging

Use four branches from a balanced plenum, sized only after the received vent sample establishes the actual spigot OD and retention depth. Do not assume a 3-inch hose from the Ø75 face-cut reference. Do not crush ducts or block the glovebox, original instruments, steering column, loom, LCD connections, demist system or service removal. The lowered inner pods intentionally create extra rear neck/elbow depth, but their {MAIN_LOWER_Y-PANEL_MIN_Y:.0f} mm local projection is a packaging envelope, not a proved clearance. At M8/M9 mock the two inner vents, all four duct bends, LCD carrier, retained components, selector contact stacks, column/shroud through full sweep, driver knees and every gear/transfer/winch lever position. Acceptance requires an as-built visible V2/V3-rim-to-LCD gap of at least **{MIN_INNER_VENT_LCD_VISIBLE_GAP:.0f} mm**, at least **{MIN_STATIC_REAR_CLEARANCE:.0f} mm** between inner-vent retainers/ducts and fixed LCD/cluster/support hardware, at least **{MIN_MOVING_COLUMN_CLEARANCE:.0f} mm** to the signed moving column/shroud/stalk swept envelope, no duct minor axis below **{MIN_DUCT_ROUNDNESS_PERCENT:.0f}%** of its round ID, and the V4-specific selector/duct clearances in `rear_envelope_fit_audit_20260801.md`. Actual bought-vent drawings and the complete rear mock-up control every aperture, retainer, hose ID and bend radius.

## Procurement and dimensional provenance

- The cost-conscious reference is the common silver/chrome ABS **Ø87 face / Ø75 opening** generic outlet family. It is a reference listing, not a released part: buy four visually and mechanically matched outlets from a single batch at a local Pakistan automotive A/C counter, then complete M7 calipers before any vent holes are cut. The Joom listing records the published family dimensions; `component_procurement_and_sample_plan.csv` records the source and sample path.
- The matching Daraz lead is currently unavailable and publishes no usable dimensions, so it is not a source of truth. The Restomod Air Diablo billet outlet is retained only as a premium import fallback; it would require a different M7 cut/duct detail.
- Sehgal Motors' locally listed 9-inch universal LCD is the procurement baseline, but it publishes no chassis/cutout dimensions. Purchase/borrow a sample or obtain a manufacturer drawing before releasing M4-M5.
- A public 1968-1978 replacement-panel listing gives **1400 x 250 x 100 mm**, confirming that broad dashboard dimensions are publicly listed. It is a centimetre-resolution vendor product envelope—not an installed 1978 RHD face outline, bend schedule or aperture/datum drawing—and Toyota EPC records configuration-specific panels. Therefore the Rev H **X=0…{PANEL_W:.0f} / Y={PANEL_MIN_Y:.0f}…{PANEL_H:.0f}** coordinate model remains a proportional quote/template datum, not an OEM dimension. M1 physical trace/scan still controls production. `dimensional_provenance_audit.csv` records the source URL and every release boundary.

## CNC layer rules

- `CUT_TEMPLATE_OUTER`: released only for the disposable full-size fit template.
- Every layer beginning `HOLD_`: construction/reference geometry only; never send directly to a production toolpath.
- `HOLD_FASCIA_OUTER`: nominal one-piece shape used to quote and create the first template; replace with the signed M1 vehicle trace.
- OEM, LCD, vent, switch, hazard, mounting and support geometry remains HOLD until its named measurement gate passes.

## Production gates

`measurement_and_release_schedule.csv` defines M1-M10: full vehicle perimeter/structure; OEM glovebox; OEM speedometer; LCD face drawing; LCD rear package; seven selectors plus hazard; four real vents; four-duct mock-up; signed full-size prototype; then continuity and live functional tests. No production metal or vehicle cut is authorised before all applicable gates are signed.

## Package contents

- `j40_dashboard_lcd_hvac_fascia_rev_h_shop_spec.pdf` - four-page shop specification.
- `dashboard_lcd_hvac_fascia_rev_h_dimensioned_front.svg` - dimensioned front design/release diagram.
- Two paired owner-photo overlays and the bought-selector reference image.
- `full_width_fascia_master_rev_h.dxf` - all-HOLD metal master/reference.
- `full_width_fit_template_rev_h.dxf` - disposable template outer cut plus HOLD component references.
- `right_control_bank_template_rev_h.dxf` - exact eight visible stations, all HOLD.
- `lcd_rear_support_reference_rev_h.dxf` - reference only, all HOLD.
- Eight CSVs covering cut/release, fascia coordinates, switch positions, M1-M10 evidence, dimensional provenance, procurement/sample controls, HVAC control interfaces and visual ratios.
- `visualisation_prompt_record.md` - reproducible image-edit prompt set and mode.
- `rear_envelope_fit_audit_20260801.md` - V4/control-bank, column, LCD and four-duct rear-packaging hold points.
- `layout_variants_20260801/layout_b_column_v4_clearance_assembled.png` - visual correction record only; its position is not measured or CNC-released.

## Acceptance

The installed face reads as an original-adjacent J40 dashboard; the OEM glovebox and speedometer function normally and retain their original visible identity and factory openings; the display proves a 9-inch active diagonal and remains serviceable; the LCD centre lies exactly on the signed fascia centreline; the midpoint of the two lowered inner outlets lies on that same centreline with equal left/right offsets; exactly four matching large outlets receive unobstructed air; the two outer bezel tops align with the LCD-bezel top while both inner faces sit fully below the LCD; exactly seven labelled selectors plus the separate hazard occupy the signed two-row extreme-right bank and match the schedule; the normal lower edge remains at its original shallow datum except for the two local vent pods, column relief and compact control return; M8/M9 prove the {MAIN_LOWER_Y-PANEL_MIN_Y:.0f} mm pod projections, the V4 visible/rear clearances of {MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE:.0f}/{MIN_STATIC_REAR_CLEARANCE:.0f} mm and all stated {MIN_INNER_VENT_LCD_VISIBLE_GAP:.0f}/{MIN_STATIC_REAR_CLEARANCE:.0f}/{MIN_MOVING_COLUMN_CLEARANCE:.0f} mm clearance minima against the actual LCD, cluster, ducts, column, controls, knees and levers; no duct, rear switch stack or driver contact clashes; no retained structure is weakened; and every M10 electrical/functional test passes without interference, voltage drop, overheating, rattle or unintended operation.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")


def validate() -> None:
    diagonal = math.hypot(LCD_ACTIVE_W, LCD_ACTIVE_H)
    assert abs(diagonal - 228.6) < 0.1, diagonal
    assert LCD_CX == PANEL_CENTRELINE_X
    assert LCD_BEZEL[0] + LCD_BEZEL[2] / 2 == PANEL_CENTRELINE_X
    assert LCD_APERTURE[0] + LCD_APERTURE[2] / 2 == PANEL_CENTRELINE_X
    assert LCD_ACTIVE[0] + LCD_ACTIVE[2] / 2 == PANEL_CENTRELINE_X
    assert len(VENT_CENTRES) == 4
    assert VENT_CENTRES[0][1] == VENT_CENTRES[3][1] == OUTER_VENT_CENTRE_Y
    assert VENT_CENTRES[1][1] == VENT_CENTRES[2][1] == INNER_VENT_CENTRE_Y
    assert (VENT_CENTRES[1][0] + VENT_CENTRES[2][0]) / 2 == PANEL_CENTRELINE_X
    assert PANEL_CENTRELINE_X - VENT_CENTRES[1][0] == VENT_CENTRES[2][0] - PANEL_CENTRELINE_X
    assert VENT_FACE_DIAMETER == 87.0 and VENT_NECK_DIAMETER == 75.0
    assert VENT_CENTRES[0][0] == OUTER_VENT_CENTRE_INSET
    assert VENT_CENTRES[-1][0] == PANEL_W - OUTER_VENT_CENTRE_INSET
    assert VENT_CENTRES[0][0] - VENT_FACE_DIAMETER / 2 == 6.5
    assert PANEL_W - (VENT_CENTRES[-1][0] + VENT_FACE_DIAMETER / 2) == 6.5
    assert VENT_CENTRES[0][0] - VENT_NECK_DIAMETER / 2 == 12.5
    assert PANEL_W - (VENT_CENTRES[-1][0] + VENT_NECK_DIAMETER / 2) == 12.5
    assert SELECTOR_DIAMETER == 22.5 and SELECTOR_REAR_ENVELOPE == 68.0
    assert len([row for row in CONTROL_MAP if row[1] != "HAZARD"]) == 7
    assert len([row for row in CONTROL_MAP if row[1] == "HAZARD"]) == 1
    assert len([row for row in CONTROL_MAP if row[2].startswith("3-position")]) == 3
    assert len([row for row in CONTROL_MAP if row[2].startswith("2-position")]) == 4
    assert any(row[1] == "ENGINE" for row in CONTROL_MAP)
    assert not any(row[1] in {"SPARE", "FUEL STOP"} for row in CONTROL_MAP)
    assert MAIN_LOWER_Y == 50.0
    assert PANEL_MIN_Y == INNER_VENT_POD_BOTTOM_Y == -35.0
    assert MAIN_LOWER_Y - PANEL_MIN_Y == 85.0
    assert OUTER_VENT_TOP_DATUM_Y == LCD_BEZEL[1] + LCD_BEZEL[3]
    assert all(
        vent_y + VENT_FACE_DIAMETER / 2 == OUTER_VENT_TOP_DATUM_Y
        for _, vent_y in (VENT_CENTRES[0], VENT_CENTRES[3])
    )
    inner_face_bottom = INNER_VENT_CENTRE_Y - VENT_FACE_DIAMETER / 2
    inner_face_top = INNER_VENT_CENTRE_Y + VENT_FACE_DIAMETER / 2
    assert inner_face_bottom == -23.5
    assert INNER_VENT_POD_BOTTOM_Y < inner_face_bottom < MAIN_LOWER_Y
    assert inner_face_bottom - INNER_VENT_POD_BOTTOM_Y == 11.5
    assert inner_face_top < LCD_BEZEL[1]
    assert LCD_BEZEL[1] - inner_face_top == 12.5
    assert LCD_BEZEL[1] - inner_face_top >= MIN_INNER_VENT_LCD_VISIBLE_GAP
    assert INNER_VENT_POD_HALF_W > VENT_FACE_DIAMETER / 2
    assert LCD_BEZEL[0] - (VENT_CENTRES[1][0] + VENT_FACE_DIAMETER / 2) == 10.5
    assert (VENT_CENTRES[2][0] - VENT_FACE_DIAMETER / 2) - (LCD_BEZEL[0] + LCD_BEZEL[2]) == 10.5
    assert inner_face_top <= SPEEDO_ENVELOPE[1]
    assert SPEEDO_ENVELOPE[1] - inner_face_top == 24.5
    assert SPEEDO_ENVELOPE[1] - inner_face_top >= MIN_STATIC_REAR_CLEARANCE
    assert VENT_CENTRES[2][0] + VENT_FACE_DIAMETER / 2 <= STEERING_COLUMN_KEEP_OUT[0]
    assert STEERING_COLUMN_KEEP_OUT[0] - (VENT_CENTRES[2][0] + VENT_FACE_DIAMETER / 2) == 25.5
    assert STEERING_COLUMN_KEEP_OUT[0] - (VENT_CENTRES[2][0] + VENT_FACE_DIAMETER / 2) >= MIN_MOVING_COLUMN_CLEARANCE
    assert STEERING_COLUMN_AXIS_X == SPEEDO_ENVELOPE[0] + SPEEDO_ENVELOPE[2] / 2
    positions = control_positions()
    assert len(positions) == 8
    assert positions[:4] == [(x, CONTROL_TOP_Y) for x in CONTROL_COLUMNS]
    assert positions[4:] == [(x, CONTROL_BOTTOM_Y) for x in CONTROL_COLUMNS]
    assert all(CONTROL_COLUMNS[index + 1] - CONTROL_COLUMNS[index] == 40.0 for index in range(3))
    assert CONTROL_TOP_Y - CONTROL_BOTTOM_Y == 58.0
    assert CONTROL_BANK[0] > STEERING_COLUMN_KEEP_OUT[0] + STEERING_COLUMN_KEEP_OUT[2]
    assert SPEEDO_ENVELOPE[0] + SPEEDO_ENVELOPE[2] <= CONTROL_BANK[0]
    bank_x0, bank_y0, bank_w, bank_h = CONTROL_BANK
    bank_x1, bank_y1 = bank_x0 + bank_w, bank_y0 + bank_h
    for index, (control_x, control_y) in enumerate(positions):
        radius = (HAZARD_DIAMETER if index == 7 else SELECTOR_DIAMETER) / 2
        assert bank_x0 <= control_x - radius and control_x + radius <= bank_x1
        assert bank_y0 <= control_y - radius and control_y + radius <= bank_y1
    assert CONTROL_TOP_Y + CONTROL_LABEL_Y_OFFSET <= bank_y1
    assert CONTROL_BOTTOM_Y + CONTROL_LABEL_Y_OFFSET < CONTROL_TOP_Y - SELECTOR_DIAMETER / 2
    assert OUTER_VENT_CENTRE_Y - VENT_FACE_DIAMETER / 2 > CONTROL_TOP_Y + SELECTOR_DIAMETER / 2
    assert OUTER_VENT_CENTRE_Y - VENT_FACE_DIAMETER / 2 - bank_y1 == V4_CONTROL_ENVELOPE_NOMINAL_GAP
    assert V4_NOMINAL_SELECTOR_HEAD_CLEARANCE == 35.75
    assert V4_NOMINAL_SELECTOR_HEAD_CLEARANCE >= MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE
    assert V4_CONTROL_ENVELOPE_NOMINAL_GAP < MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE
    assert MIN_V4_VISIBLE_SELECTOR_HEAD_CLEARANCE >= MIN_MOVING_COLUMN_CLEARANCE
    profile = outer_profile_points()
    assert min(x for x, _ in profile) == 0 and max(x for x, _ in profile) == PANEL_W
    assert min(y for _, y in profile) == PANEL_MIN_Y and max(y for _, y in profile) == PANEL_H
    required = [
        "README.md", "full_width_fascia_master_rev_h.dxf", "full_width_fit_template_rev_h.dxf",
        "right_control_bank_template_rev_h.dxf", "lcd_rear_support_reference_rev_h.dxf",
        "dashboard_lcd_hvac_fascia_rev_h_dimensioned_front.svg",
        "dashboard_lcd_hvac_fascia_rev_h_photo_overlay_assembled.png",
        "dashboard_lcd_hvac_fascia_rev_h_photo_overlay_bare_shell.png",
        "fabricator_cut_and_release_schedule.csv", "fascia_coordinate_schedule.csv",
        "switch_position_schedule.csv", "measurement_and_release_schedule.csv",
        "dimensional_provenance_audit.csv", "component_procurement_and_sample_plan.csv",
        "hvac_control_interface_schedule.csv", "visual_ratio_schedule.csv",
        "industrial_rotary_selector_reference.png",
        "j40_dashboard_lcd_hvac_fascia_rev_h_shop_spec.pdf", "visualisation_prompt_record.md",
        "rear_envelope_fit_audit_20260801.md",
    ]
    for name in required:
        assert (OUT / name).exists(), name
    for relative in (
        CORRECTED_ASSEMBLED_VIS_RELATIVE,
        COLUMN_V5_ASSEMBLED_VIS_RELATIVE,
        COLUMN_V5_STRAIGHT_VIS_RELATIVE,
        COLUMN_V6_ASSEMBLED_VIS_RELATIVE,
        COLUMN_V6_STRAIGHT_VIS_RELATIVE,
        LAYOUT_VARIANTS_README_RELATIVE,
    ):
        assert (OUT / relative).exists(), relative


def package() -> None:
    DELIVERABLE.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DELIVERABLE, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(OUT.iterdir()):
            if path.is_file():
                archive.write(path, f"dashboard_lcd_hvac_fascia_rev_h/{path.name}")
        for relative in (
            LAYOUT_VARIANTS_README_RELATIVE,
            CORRECTED_ASSEMBLED_VIS_RELATIVE,
            COLUMN_V5_ASSEMBLED_VIS_RELATIVE,
            COLUMN_V5_STRAIGHT_VIS_RELATIVE,
            COLUMN_V6_ASSEMBLED_VIS_RELATIVE,
            COLUMN_V6_STRAIGHT_VIS_RELATIVE,
        ):
            archive.write(OUT / relative, f"dashboard_lcd_hvac_fascia_rev_h/{relative.as_posix()}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if ASSEMBLED_VIS_SOURCE.exists():
        shutil.copy2(ASSEMBLED_VIS_SOURCE, OUT / "dashboard_lcd_hvac_fascia_rev_h_photo_overlay_assembled.png")
    if BARE_VIS_SOURCE.exists():
        shutil.copy2(BARE_VIS_SOURCE, OUT / "dashboard_lcd_hvac_fascia_rev_h_photo_overlay_bare_shell.png")
    if SWITCH_REFERENCE_SOURCE.exists():
        shutil.copy2(SWITCH_REFERENCE_SOURCE, OUT / "industrial_rotary_selector_reference.png")
    make_dxfs()
    write_svg()
    write_csvs()
    write_prompt_record()
    write_rear_envelope_fit_audit()
    write_readme()
    write_pdf()
    validate()
    package()
    print(f"generated: {OUT}")
    print(f"archive:   {DELIVERABLE}")


if __name__ == "__main__":
    main()
