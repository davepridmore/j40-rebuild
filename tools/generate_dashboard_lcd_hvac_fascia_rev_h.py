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
    "/Users/davidpridmore/.codex/generated_images/019fb8d3-8269-7eb0-b457-d806a3cefbd4/exec-ac094ef4-d7bc-4092-9939-00fc081013bc.png"
)
BARE_VIS_SOURCE = Path(
    "/Users/davidpridmore/.codex/generated_images/019fb8d3-8269-7eb0-b457-d806a3cefbd4/exec-ed9c376b-c959-44e7-8db5-2730ce307fe8.png"
)
SWITCH_REFERENCE_SOURCE = Path(
    "/var/folders/2r/rbnydbl91t9_jcjfhssspzqw0000gn/T/codex-clipboard-ff07d5a4-279b-4983-a817-caf5c2c9b1ad.png"
)

# Rev H is a full-width, one-piece visible face.  Its main face stops at Y=50.
# All four vents have now been raised so their visible bezels share the LCD
# bezel's upper datum and fit wholly in the main face.  Only a shallow rounded service channel carrying the
# compact controls beneath the OEM cluster extends locally below that edge.
# This avoids both low vent lobes and a separate full-height switch column.
# These coordinates remain a quotation /
# template datum only; the physical vehicle trace at M1 controls the perimeter
# and every preserved structural edge.
PANEL_W = 1260.0
PANEL_H = 220.0
PANEL_CENTRELINE_X = PANEL_W / 2
MAIN_LOWER_Y = 50.0
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
# The end vents sit close to the usable ends of the front face, never in the
# folded side returns.  The inner pair is centred symmetrically about the LCD.
# All four outlet tops align with the top of the LCD bezel. They fit in the main
# face and no longer require lower vent lobes.
VENT_FACE_DIAMETER = 87.0
VENT_CORE_DIAMETER = 69.0
VENT_NECK_DIAMETER = 75.0
OUTER_VENT_CENTRE_INSET = 50.0
INNER_VENT_CENTRE_OFFSET = 166.0
VENT_TOP_DATUM_Y = LCD_BEZEL[1] + LCD_BEZEL[3]
VENT_CENTRE_DATUM_Y = VENT_TOP_DATUM_Y - VENT_FACE_DIAMETER / 2
VENT_CENTRES = (
    (OUTER_VENT_CENTRE_INSET, VENT_CENTRE_DATUM_Y),
    (PANEL_CENTRELINE_X - INNER_VENT_CENTRE_OFFSET, VENT_CENTRE_DATUM_Y),
    (PANEL_CENTRELINE_X + INNER_VENT_CENTRE_OFFSET, VENT_CENTRE_DATUM_Y),
    (PANEL_W - OUTER_VENT_CENTRE_INSET, VENT_CENTRE_DATUM_Y),
)

# Reference envelopes only. Exact OEM outlines, hinge/latch axes and mounting
# holes are transferred from the retained parts during the M1-M3 template stage.
# The upper components sit in the 170 mm-high main face. Their nominal outlines
# are visual/clearance envelopes; M2/M3 direct transfers control real geometry.
GLOVEBOX_ENVELOPE = (97.0, 58.0, 315.0, 157.0)
SPEEDO_ENVELOPE = (850.0, 58.0, 210.0, 157.0)

# Exactly eight visible stations occupy one labelled row in the right lower
# vent/service channel: seven maintained selectors plus a separate hazard.
# A one-row arrangement is the lowest-height packaging; flange, anti-rotation,
# contact-block, steering-column and hand-clearance checks remain M6/M9 HOLD.
CONTROL_BANK = (842.0, 4.0, 309.0, 46.0)

SELECTOR_DIAMETER = 22.5
HAZARD_DIAMETER = 16.0
CONTROL_XS = tuple(860.0 + 39.0 * index for index in range(8))
CONTROL_Y = 24.0
CONTROL_LABEL_Y_OFFSET = 19.0
SELECTOR_REAR_ENVELOPE = 68.0
CONTROL_MAP = (
    ("S1", "WIPERS", "3-position maintained", "OFF / LOW / HIGH", "wiper interface; preserve automatic park"),
    ("S2", "LIGHTS", "3-position maintained", "OFF / SIDE / HEAD", "master lighting request; retained dip selects T1/T2"),
    ("S3", "SPOTS", "2-position maintained", "OFF / ON", "T5 spot-lamp relay command"),
    ("S4", "AUX", "2-position maintained", "OFF / ON", "B2 reserved accessory relay command"),
    ("S5", "BLOWER", "3-position maintained", "OFF / LOW / HIGH", "low-current request to measured HVAC resistor/relay/PWM controller; never blower-motor current"),
    ("S6", "A/C", "2-position maintained", "OFF / ON", "B1 compressor request through evaporator thermostat/freeze control and trinary/pressure safeties"),
    ("S7", "ENGINE", "2-position maintained", "RUN / STOP", "low-current validated fuel-stop interface; key OFF authoritative; manual stop cable fallback"),
    ("S8", "HAZARD", "separate red pushbutton", "OFF / FLASH", "existing hazard/flasher circuit"),
)


def control_positions() -> list[tuple[float, float]]:
    """Passenger/left-to-driver/right order in the single lower channel row."""
    return [(control_x, CONTROL_Y) for control_x in CONTROL_XS]


def outer_profile_points() -> list[tuple[float, float]]:
    """Clockwise nominal template outline with one local control channel.

    The normal face ends at Y=50. All four raised vents fit wholly above this
    datum. A compact rounded right-hand channel alone extends to Y=0 for the
    eight visible control stations beneath the OEM cluster. The overall
    envelope stays 220 mm while most of the face is only 170 mm high. Curves
    are deliberately faceted quotation geometry until M1.
    """
    return [
        (0, PANEL_H), (PANEL_W, PANEL_H),
        (PANEL_W, MAIN_LOWER_Y), (1168, MAIN_LOWER_Y),
        (1166, 28), (1156, 10), (1138, 0),
        (850, 0), (832, 10), (822, 28), (820, MAIN_LOWER_Y),
        (0, MAIN_LOWER_Y),
    ]


def glovebox_profile_points() -> list[tuple[float, float]]:
    return [(97, 72), (107, 58), (392, 58), (412, 74), (412, 192), (395, 212), (117, 215), (97, 198)]


def speedometer_profile_points() -> list[tuple[float, float]]:
    """Nominal visual envelope echoing the retained J40 cluster.

    This is deliberately not CNC geometry. The original cluster has one broad
    upper speedometer window and lower auxiliary windows; M3 direct transfer of
    the actual housing, mounts and rear stack controls every production feature.
    """
    return [(850, 58), (850, 180), (861, 202), (885, 215), (1023, 215), (1047, 202), (1060, 180), (1060, 58)]


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
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="760" viewBox="0 0 1400 760">
<defs><linearGradient id="silver" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f3f4f4"/><stop offset=".5" stop-color="#b5bbbe"/><stop offset="1" stop-color="#71787c"/></linearGradient></defs>
<style>.title{{font:700 22px Verdana;fill:#20262b}}.subtitle{{font:14px Verdana;fill:#53606a}}.label{{font:700 13px Verdana;fill:#20262b}}.small{{font:12px Verdana;fill:#53606a}}.control{{font:700 9px Verdana;fill:#20262b}}.ventno{{font:700 11px Verdana;fill:#e8ecee}}.dim{{stroke:#9c2424;stroke-width:1.5;fill:none}}.hold{{stroke:#aa6500;stroke-width:2;fill:none;stroke-dasharray:7 5}}</style>
<rect width="1400" height="760" fill="#f7f8f9"/>
<text x="55" y="42" class="title">J40 RHD FULL-WIDTH 9-INCH LCD / FOUR-OUTLET FASCIA - REV H</text>
<text x="55" y="68" class="subtitle">170 mm main face with four raised outlets; only the compact labelled right control channel extends locally; all vehicle/interface geometry HOLD.</text>
<polygon points="{svg_points(outer_profile_points(), scale, x0, y0)}" fill="#e8e2cc" stroke="#111" stroke-width="2"/>
<line x1="{sx(0)}" y1="{sy(MAIN_LOWER_Y)}" x2="{sx(PANEL_W)}" y2="{sy(MAIN_LOWER_Y)}" class="hold"/>
<polygon points="{svg_points(glovebox_profile_points(), scale, x0, y0)}" fill="#aeb2b2" stroke="#5d6264" stroke-width="2"/>
<circle cx="{sx(363)}" cy="{sy(130)}" r="7" fill="#24292d"/>
<text x="{sx(255)}" y="{sy(139)}" text-anchor="middle" class="label">RETAIN OEM GLOVEBOX SHAPE / KNOB / PLATE</text>
<rect x="{sx(bx)}" y="{sy(by+bh)}" width="{bw*scale}" height="{bh*scale}" rx="5" fill="#11161a" stroke="#292f33" stroke-width="2"/>
<rect x="{sx(ax)}" y="{sy(ay+ah)}" width="{aw*scale}" height="{ah*scale}" rx="3" fill="#263e4d" stroke="#dae2e6"/>
<text x="{sx(LCD_CX)}" y="{sy(LCD_CY)-4}" text-anchor="middle" fill="#fff" font-family="Verdana" font-size="14" font-weight="700">9-INCH / 16:9 ACTIVE REFERENCE</text>
<text x="{sx(LCD_CX)}" y="{sy(LCD_CY)+14}" text-anchor="middle" fill="#d6e0e5" font-family="Verdana" font-size="10">199.2 × 112.1 mm | 228.6 mm diagonal | aperture HOLD</text>
<polygon points="{svg_points(speedometer_profile_points(), scale, x0, y0)}" fill="#bfc2bd" stroke="#0d0f10" stroke-width="2"/>
<rect x="{sx(870)}" y="{sy(126+72)}" width="{170*scale}" height="{72*scale}" rx="{18*scale}" fill="#292d2e" stroke="#16191b" stroke-width="2"/>
<rect x="{sx(866)}" y="{sy(71+39)}" width="{70*scale}" height="{39*scale}" rx="{4*scale}" fill="#292d2e" stroke="#16191b" stroke-width="2"/>
<rect x="{sx(947)}" y="{sy(71+39)}" width="{98*scale}" height="{39*scale}" rx="{4*scale}" fill="#292d2e" stroke="#16191b" stroke-width="2"/>
<rect x="{sx(939)}" y="{sy(90+16)}" width="{7*scale}" height="{16*scale}" rx="{2*scale}" fill="#ede8d7" stroke="#16191b" stroke-width="1"/>
<text x="{sx(955)}" y="{sy(158)}" text-anchor="middle" fill="#ede8d7" font-family="Verdana" font-size="10" font-weight="700">SPEED</text>
<text x="{sx(901)}" y="{sy(87)}" text-anchor="middle" fill="#ede8d7" font-family="Verdana" font-size="8">FUEL</text>
<text x="{sx(996)}" y="{sy(87)}" text-anchor="middle" fill="#ede8d7" font-family="Verdana" font-size="8">TEMP / AMP</text>
<text x="{sx(955)}" y="{sy(219)}" text-anchor="middle" class="control">RETAIN / TRANSFER ORIGINAL SPEEDOMETER ASSEMBLY</text>
{''.join(vent_markup)}
{''.join(controls)}
<line x1="{sx(0)}" y1="{sy(0)+40}" x2="{sx(PANEL_W)}" y2="{sy(0)+40}" class="dim"/>
<text x="{sx(PANEL_CENTRELINE_X)}" y="{sy(0)+62}" text-anchor="middle" class="label">{PANEL_W:.0f} NOMINAL REFERENCE ENVELOPE - M1 PHYSICAL DASH TRACE CONTROLS</text>
<line x1="{sx(35)}" y1="{sy(VENT_CENTRE_DATUM_Y)}" x2="{sx(PANEL_W-35)}" y2="{sy(VENT_CENTRE_DATUM_Y)}" class="dim" stroke-dasharray="4 4"/>
<line x1="{sx(PANEL_CENTRELINE_X)}" y1="{sy(0)}" x2="{sx(PANEL_CENTRELINE_X)}" y2="{sy(PANEL_H)}" class="hold"/>
<text x="{sx(PANEL_CENTRELINE_X)}" y="{sy(PANEL_H)-10}" text-anchor="middle" class="label">CL X={PANEL_CENTRELINE_X:.1f}: LCD CENTRE = INNER-VENT PAIR MIDPOINT</text>
<text x="{sx(PANEL_CENTRELINE_X)}" y="{sy(VENT_CENTRE_DATUM_Y)-58}" text-anchor="middle" class="label">FOUR VENT TOPS ALIGN WITH LCD BEZEL: TOP Y={VENT_TOP_DATUM_Y:.1f} / CENTRES Y={VENT_CENTRE_DATUM_Y:.1f} | INNER PAIR ±{INNER_VENT_CENTRE_OFFSET:.0f} ABOUT CL | HOLD M7</text>
<rect x="55" y="500" width="1290" height="210" rx="9" fill="#fff" stroke="#c8d0d5"/>
<text x="78" y="535" class="label">RELEASE / FABRICATION INTENT</text>
<text x="78" y="563" class="small">• Full existing face removed only after M1 full-size template identifies structural cowl, A-pillar and steering-column boundaries.</text>
<text x="78" y="588" class="small">• Retained glovebox | centred LCD | retained cluster. Four raised outlets occupy otherwise-free side gaps without crossing those components.</text>
<text x="78" y="613" class="small">• LCD is exactly on fascia CL; inner vents are mirrored ±{INNER_VENT_CENTRE_OFFSET:.0f} mm. Four vent-bezel tops align with the LCD bezel at Y={VENT_TOP_DATUM_Y:.1f}.</text>
<text x="78" y="638" class="small">• One shallow right control channel carries 7 selectors + red hazard in a single labelled row; Ø22.5 / 68 rear ref; M6/M9 HOLD.</text>
<text x="78" y="663" class="small">• One-piece 1.5 mm CR4 visible face; rear screen carrier and stiffeners transfer load to retained dashboard structure.</text>
<text x="78" y="688" class="small">• Orange/dashed/HOLD geometry is quotation and transfer reference only. Production metal cutting awaits M1-M10 sign-off.</text>
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
    c.setFillColor(HexColor("#292d2e"))
    c.roundRect(px(870), py(126), 170 * scale * mm, 72 * scale * mm, 18 * scale * mm, fill=1, stroke=1)
    c.roundRect(px(866), py(71), 70 * scale * mm, 39 * scale * mm, 4 * scale * mm, fill=1, stroke=1)
    c.roundRect(px(947), py(71), 98 * scale * mm, 39 * scale * mm, 4 * scale * mm, fill=1, stroke=1)
    c.setFillColor(HexColor("#ede8d7"))
    c.roundRect(px(939), py(90), 7 * scale * mm, 16 * scale * mm, 2 * scale * mm, fill=1, stroke=1)
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
    c.drawCentredString(page_w / 2, 106 * mm, f"{PANEL_W:.0f} x {PANEL_H:.0f} nominal coordinate envelope only - the M1 physical dash trace controls the final one-piece perimeter")
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(15 * mm, 91 * mm, "LOCKED ARCHITECTURE")
    notes = [
        "Full existing visible dashboard face is replaced by one formed 1.5 mm CR4 face after structural boundaries are transferred; retain cowl, A-pillars, steering-column support and firewall structure.",
        "A 9-inch / 16:9 active-image reference is 199.2 x 112.1 mm = 228.6 mm diagonal. The Sehgal 9-inch listing publishes no chassis/cutout drawing: bezel, aperture, rear body and mounts are HOLD to a bought sample.",
        f"LCD centre X={PANEL_CENTRELINE_X:.1f}. Inner vent centres X={VENT_CENTRES[1][0]:.1f}/{VENT_CENTRES[2][0]:.1f}; their midpoint is exactly X={PANEL_CENTRELINE_X:.1f} and offsets are equal at ±{INNER_VENT_CENTRE_OFFSET:.1f}. All four vent centres share Y={VENT_CENTRE_DATUM_Y:.1f}; their Ø87 bezel tops align with the LCD bezel at Y={VENT_TOP_DATUM_Y:.1f}.",
        "Four matching satin-silver generic vents: published face Ø87 and panel opening Ø75 reference; M7 sample/caliper gate controls the cut.",
        f"The normal face is {PANEL_H-MAIN_LOWER_Y:.0f} mm high. All four raised vents fit within it; only the compact driver-side control channel extends to the {PANEL_H:.0f} mm overall envelope.",
        "Original asymmetric glovebox | true 9-inch central LCD | original speedometer. Four raised vents use otherwise-free side gaps and top-align with the LCD bezel.",
        "One shallow channel beneath the speedometer carries a passenger-to-driver row: WIPERS, LIGHTS, SPOTS, AUX, BLOWER, A/C, ENGINE and separate red HAZARD.",
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

    # Page 2 - both owner photographs and matched overlays.
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(15 * mm, page_h - 16 * mm, "Owner-photo basis and matching Rev H visual intent")
    c.setFont("Helvetica", 8.5)
    c.drawRightString(page_w - 15 * mm, page_h - 16 * mm, "Images establish appearance only - never scale for CNC")
    labels = [
        ("ASSEMBLED RHD OWNER PHOTO", 15, 263), ("ASSEMBLED REV H OVERLAY", 215, 263),
        ("BARE-SHELL OWNER PHOTO", 15, 148), ("BARE-SHELL REV H OVERLAY", 215, 148),
    ]
    c.setFont("Helvetica-Bold", 9)
    for label, x_pos, y_pos in labels:
        c.drawString(x_pos * mm, y_pos * mm, label)
    draw_image_fit(c, ASSEMBLED_BASE_PHOTO, 15 * mm, 166 * mm, 190 * mm, 88 * mm)
    draw_image_fit(c, OUT / "dashboard_lcd_hvac_fascia_rev_h_photo_overlay_assembled.png", 215 * mm, 166 * mm, 190 * mm, 88 * mm)
    draw_image_fit(c, BARE_BASE_PHOTO, 15 * mm, 51 * mm, 190 * mm, 88 * mm)
    draw_image_fit(c, OUT / "dashboard_lcd_hvac_fascia_rev_h_photo_overlay_bare_shell.png", 215 * mm, 51 * mm, 190 * mm, 88 * mm)
    c.setFont("Helvetica", 7.5)
    c.drawString(15 * mm, 39 * mm, "Visual check: four raised vents top-aligned with the LCD bezel, shallow right control channel, true 9-inch centre screen, and untouched OEM cluster/glovebox.")
    c.drawString(15 * mm, 32 * mm, "The oblique driver view naturally foreshortens and partly masks the screen; M4 sample measurement, not apparent photo size, controls the LCD cut.")
    c.drawString(15 * mm, 25 * mm, f"All four Ø87 bezel tops share Y={VENT_TOP_DATUM_Y:.1f}; centres are Y={VENT_CENTRE_DATUM_Y:.1f}. Outer faces retain 6.5 mm nominal end land. Only controls use the lower channel.")
    c.setFillColor(HexColor("#8b1e1e"))
    c.setFont("Helvetica-Bold", 7.8)
    c.drawString(15 * mm, 14 * mm, "VISUALISATIONS ARE DESIGN INTENT ONLY. CNC RELEASE REQUIRES ACTUAL DASH, LCD, VENTS, CONTROLS AND A SIGNED FULL-SIZE TEMPLATE.")
    c.showPage()

    # Page 3 - exact controls and electrical implementation.
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(15 * mm, page_h - 16 * mm, "Exact right-channel control schedule and electrical boundaries")
    c.setFont("Helvetica", 8.5)
    c.drawRightString(page_w - 15 * mm, page_h - 16 * mm, "Exactly 7 industrial selectors + 1 separate red hazard")
    style = ParagraphStyle("cell", fontName="Helvetica", fontSize=6.2, leading=7.1, alignment=TA_LEFT, textColor=HexColor("#20262b"))
    header_style = ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=6.4, leading=7.3, textColor=colors.white)
    headers = ["ID", "CABIN POSITION", "LABEL", "HARDWARE / STATES", "PLAIN-LANGUAGE FUNCTION", "ELECTRICAL TARGET / CONSTRAINT"]
    table_rows = [[Paragraph(value, header_style) for value in headers]]
    locations = [f"single row station {index}/8" for index in range(1, 9)]
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
            "Screen mass goes into a rear bracket tied to retained structure, never the 1.5 mm skin alone.",
            "Provide hidden M5 fasteners at <=150 mm pitch where structure permits and allow cabin-side LCD/vent service removal.",
        ]),
        (147, "HVAC / PACKAGING", [
            "Exactly four matching generic silver outlets with published Ø87 faces / Ø75 panel-opening reference; M7 real-sample data controls.",
            f"Raise all four outlets into the unused side gaps and align their visible bezel tops with the LCD bezel. Transfer the Y={VENT_TOP_DATUM_Y:.1f} top datum from one laser/level line; no vent lobe is required.",
            "Use four branches sized to the sampled vent spigot from a balanced plenum. Confirm hose ID and bend radius after M7; do not assume 3-inch duct.",
            "Do not crush hose or obstruct the glovebox, speedometer, column, wiring, LCD connectors, demist system or service paths.",
            "Create vent-neck depth rearward within the main face. Verify all four duct bends plus the lower right-channel selector rear stacks against the cluster, column, wiring, knee and levers in the complete mock-up.",
        ]),
        (279, "CUT / FINISH SEQUENCE", [
            "1. Cut the disposable full-size template only. Fit, trim and mark structural keep-outs on the actual vehicle.",
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
        "M1 full-width perimeter/structural trace", "M2 OEM glovebox trace, hinge, latch and sweep",
        "M3 OEM cluster outline, depth, mounts and driver sight line", "M4 LCD maker drawing, active area, aperture and bezel",
        "M5 LCD rear body, support, connectors and removal", "M6 seven real selectors + hazard: part code, Ø22.5 bush/cut, flange, anti-rotation and 68 mm rear envelope",
        "M7 four matched vents: face, Ø75 cut, retainer, spigot and depth", "M8 four-duct mock-up, actual hose ID/bend radii, flow and all rear clearances",
        "M9 signed full-size prototype: driver, controls, glovebox, column, levers and service", "M10 continuity, labels, wiper park/washer, light truth table, blower, A/C safeties, ENGINE key-off/manual fallback, AUX/SPOTS/hazard tests",
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
            ["nominal full-width envelope", 0, 0, PANEL_W, PANEL_H, "HOLD_FASCIA_OUTER", "template coordinate system only; M1 physical trace controls"],
            ["fascia vertical centre datum", PANEL_CENTRELINE_X, 0, "", PANEL_H, "HOLD_CENTRELINES", "master datum: LCD centre and midpoint of inner vent pair must remain coincident after M1 trace"],
            ["main lower datum", 0, MAIN_LOWER_Y, PANEL_W, "", "HOLD_MAIN_LOWER_DATUM", "normal face ends at Y50; only the compact right control channel extends locally to Y0; all four vents remain wholly in the main face"],
            ["LCD bezel envelope", LCD_BEZEL[0], LCD_BEZEL[1], LCD_BEZEL[2], LCD_BEZEL[3], "HOLD_LCD_BEZEL_ENVELOPE", "manufacturer drawing controls"],
            ["LCD aperture", LCD_APERTURE[0], LCD_APERTURE[1], LCD_APERTURE[2], LCD_APERTURE[3], "HOLD_LCD_APERTURE", "manufacturer drawing controls"],
            ["LCD active image", LCD_ACTIVE[0], LCD_ACTIVE[1], LCD_ACTIVE[2], LCD_ACTIVE[3], "HOLD_LCD_ACTIVE_REFERENCE", "9-inch / 16:9 mathematical reference only: 228.6 mm diagonal; sample controls"],
            ["OEM glovebox transfer envelope", GLOVEBOX_ENVELOPE[0], GLOVEBOX_ENVELOPE[1], GLOVEBOX_ENVELOPE[2], GLOVEBOX_ENVELOPE[3], "HOLD_GLOVEBOX_TRANSFER_ENVELOPE", "actual asymmetric lid/hinge/latch trace controls"],
            ["OEM speedometer transfer envelope", SPEEDO_ENVELOPE[0], SPEEDO_ENVELOPE[1], SPEEDO_ENVELOPE[2], SPEEDO_ENVELOPE[3], "HOLD_SPEEDOMETER_TRANSFER_ENVELOPE", "actual original assembly trace and mounts control"],
            ["right control bank envelope", CONTROL_BANK[0], CONTROL_BANK[1], CONTROL_BANK[2], CONTROL_BANK[3], "HOLD_CONTROL_BANK_ENVELOPE", "one passenger-to-driver row S1-S8 in lower right channel; exact 7 selectors + hazard; 39 mm pitch; M6/M9 HOLD"],
        ]
        for index, (vent_x, vent_y) in enumerate(VENT_CENTRES, start=1):
            face_note = f"centre coordinate; all four Y={VENT_CENTRE_DATUM_Y:.1f} exactly; Ø87 bezel top Y={VENT_TOP_DATUM_Y:.1f}, aligned with LCD bezel top"
            if index in (2, 3):
                face_note += f"; inner pair mirrored ±{INNER_VENT_CENTRE_OFFSET:.1f} about fascia/LCD centreline X={PANEL_CENTRELINE_X:.1f}"
            if index in (1, 4):
                face_note += "; outer visible face is 6.5 mm from nominal usable-face end and Ø75 reference cut is 12.5 mm from it; M1/M7 control"
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
            physical_position = f"single lower-right channel row; station {station_index} of 8 passenger-to-driver"
            writer.writerow([control_id, physical_position, control_x, control_y, hardware, label, states, action, electrical, release])

    with (OUT / "measurement_and_release_schedule.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["gate", "measurement_or_test", "nominal_intent", "required_evidence", "release_status"])
        writer.writerows([
            ["M1", "full-width dashboard face perimeter, cowl/A-pillar/column/firewall structural keep-outs, attachment flange and true usable-face centreline", f"{PANEL_H-MAIN_LOWER_Y:.0f} mm normal face plus only the compact right control channel within a {PANEL_W:.0f} x {PANEL_H:.0f} coordinate envelope; not a vehicle dimension", "rigid full-size template fitted and trimmed; front/rear ruler photos; centreline derived from signed usable face; owner-signed perimeter", "HOLD all metal and vehicle cuts"],
            ["M2", "OEM glovebox exact asymmetric outline, hinge/latch axes, knob, instruction plate, rear depth and full opening sweep", "preserve original appearance and operation", "direct trace/rubbing, mounted donor, sweep photos and clearance record", "HOLD"],
            ["M3", "OEM speedometer/cluster exact outline, mounts, depth, cables/wiring and seated-driver sight line", "retain original assembly; relocate only as signed", "direct trace/rubbing, rear depth gauge and driver-view photos", "HOLD"],
            ["M4", "LCD active area, aperture, bezel and corner radii", "9-inch 16:9 active 199.2 x 112.1; 228.6 diagonal; aperture 202 x 115 reference", "manufacturer mechanical drawing and caliper confirmation", "HOLD"],
            ["M5", "LCD rear body, mount centres, mass, connectors, cable bend, cooling and service removal", f"screen centre X{PANEL_CENTRELINE_X:.1f}/Y{LCD_CY:.1f}; exactly coincident with fascia centreline and inner-vent-pair midpoint; separate rear structural carrier", "rear-body rubbing, depth record, bracket mock-up, centreline check and cabin-side removal test", "HOLD"],
            ["M6", "seven bought Schneider-style selectors and separate hazard: part code, head/lever sweep, bush, flange, anti-rotation and contact-block stack", "single horizontal row; 39 mm pitch; selector panel cut Ø22.5; 68 mm rear envelope; hazard Ø16 reference", "part-code photo plus caliper sheet for every part and 1:1 horizontal right-channel trial including hand clearance", "HOLD"],
            ["M7", "four matched generic vent faces, panel opening, retention, spigot OD and rear depth", "published silver/chrome ABS family: Ø87 face; Ø75 panel-opening reference", "one received four-piece batch, seller drawing/listing, caliper record and fitted retainer trial for all four", "HOLD"],
            ["M8", "four ducts, plenum balance, actual hose ID/bend radii, selector rear stacks and rear/service clearances", "sampled vent spigot controls duct size; no crushed hose or selector/duct/cluster/column clash", "full rear mock-up, obstruction photos and blower-flow comparison", "HOLD"],
            ["M9", "complete full-size prototype and driver/service clearances", "one-piece shallow face with only a compact right control channel; OEM glovebox/cluster; LCD and inner-vent-pair midpoint exactly on fascia centreline; all four vent tops aligned with LCD bezel top", "owner-signed seated-driver reach plus knee/lever/column clearance, glovebox sweep, centre/symmetry, top-datum, visibility and removal checks", "HOLD"],
            ["M10", "labels, continuity, relay/controller mapping and live functions", "exact switch schedule including ENGINE RUN/STOP; key OFF authoritative; manual stop cable retained", "continuity sheet and live wiper park plus washer, OFF/SIDE/HEAD truth table plus dip, measured blower, A/C safety/fan, spots, AUX, isolated hazard, ENGINE run/stop, key-off and manual-cable fallback tests", "HOLD until passed"],
        ])

    with (OUT / "dimensional_provenance_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["feature", "reference_value", "provenance", "confidence", "production_release", "required_gate", "source_url"])
        writer.writerows([
            ["public early replacement-panel product envelope", "1400 x 250 x 100 mm", "Reborn FJ 1968-1978 steel dashboard listing; centimetre-resolution product dimension, not installed RHD face datums, bends or aperture coordinates", "PUBLISHED_VENDOR_ENVELOPE", "NOT FOR CNC", "M1 physical full-width trace", PUBLIC_REPRO_PANEL_URL],
            ["full dashboard visible-face perimeter", f"{PANEL_W:.0f} x {PANEL_H:.0f} nominal coordinate envelope", "Rev H proportional design datum; public vendor envelope is broader product context only and Toyota EPC shows configuration-specific panels", "DESIGN_REFERENCE_ONLY", "HOLD", "M1 physical full-width trace", PUBLIC_REPRO_PANEL_URL],
            ["fascia/LCD/inner-vent common centreline", f"X={PANEL_CENTRELINE_X:.1f}; inner vents X={VENT_CENTRES[1][0]:.1f}/{VENT_CENTRES[2][0]:.1f}", f"parametric Rev H constraint: LCD centre equals fascia centreline; inner-pair midpoint equals same centreline; equal offsets ±{INNER_VENT_CENTRE_OFFSET:.1f}", "MATHEMATICALLY_EXACT_IN_NOMINAL_MODEL", "HOLD for physical transfer", "M1 + M5 + M9", ""],
            ["OEM glovebox", "nominal only envelope in drawing", "Toyota parts fitment family only; no public 1978 RHD lid/hinge dimensional drawing found", "PHYSICAL_TRANSFER_REQUIRED", "HOLD", "M2 direct trace and opening sweep", TOYOTA_EPC_URL],
            ["OEM speedometer / cluster", "nominal only envelope in drawing", "Toyota parts fitment family only; no public 1978 RHD cluster dimensional drawing found", "PHYSICAL_TRANSFER_REQUIRED", "HOLD", "M3 direct trace, rear depth, mounts and sight line", TOYOTA_EPC_URL],
            ["LCD active-image reference", "199.2 x 112.1; 228.6 diagonal", "mathematical 9-inch 16:9 reference; Sehgal local listing states 9-inch but has no chassis/cutout drawing", "REFERENCE_ONLY", "HOLD", "M4-M5 bought sample and manufacturer drawing", "https://sehgalmotors.pk/products/universal-android-lcd-tab-9-inches-with-wiring-without-main-grip"],
            ["LCD bezel/aperture/support", "224 x 136 / 202 x 115 / 246 x 158 nominal", "design envelope only", "PHYSICAL_TRANSFER_REQUIRED", "HOLD", "M4-M5", ""],
            ["generic silver vent family", "face Ø87; panel opening Ø75", "Joom listing; cross-check only, generic variants have spigot/retainer variation", "PUBLISHED_LISTING_REFERENCE", "HOLD", "M7 received matched four-piece sample batch + calipers", "https://www.joom.com/en/products/68c8f9fa6dffb3012ca80d30"],
            ["vent x/y centres and common upper alignment", f"centres={VENT_CENTRES}; bezel-top Y={VENT_TOP_DATUM_Y:.1f}", "Rev H layout decision; inner pair is exactly symmetric about LCD/fascia centreline; all four Ø87 bezel tops align with the LCD bezel top; outer faces remain close to usable ends and clear of side returns", "DESIGN_LOCKED", "HOLD for actual vehicle transfer", "M1 + M7 + M9", ""],
            ["right-channel control row", f"centres X={CONTROL_XS}; Y={CONTROL_Y}; 39 mm pitch", "Rev H compact packaging decision: seven selectors plus hazard in one passenger-to-driver row between the two right vents", "DESIGN_LOCKED_IN_NOMINAL_MODEL", "HOLD for physical part, duct and driver checks", "M6 + M8 + M9", ""],
            ["Schneider-style selector aperture", "Ø22.5", "Schneider Electric Harmony XB4 published mounting diameter", "VERIFIED_PRODUCT_STANDARD", "HOLD to bought-part confirmation", "M6 part-code photo + calipers", "https://shop.se.com/pro/us/en/product/selector-switch-harmony-xb4-black-22mm-3-positions-stay-put-2no/"],
            ["Schneider-style selector rear envelope", "68", "Schneider Electric Harmony XB4 published complete depth", "VERIFIED_PRODUCT_STANDARD", "HOLD to bought-part confirmation", "M6 part-code photo + rear-stack trial", "https://shop.se.com/pro/us/en/product/selector-switch-harmony-xb4-black-22mm-3-positions-stay-put-2no/"],
            ["hazard aperture", "Ø16 nominal", "no selected/published hazard part drawing", "REFERENCE_ONLY", "HOLD", "M6 actual part", ""],
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

Mode: built-in image generation, local-reference image editing.

## Authoritative architecture

Upper band from passenger/left to driver/right: **original glovebox | centred 9-inch LCD | original speedometer**. Exactly four matching vents occupy the side gaps: one at each extreme and a symmetric inner pair flanking the LCD laterally. Raise all four so the tops of their visible silver bezels align with the top of the LCD bezel. The vents remain wholly in the main face; only one compact right-hand control channel extends below it.

## Bare-shell owner-photo edit

Edit the supplied straight-on bare-shell J40 dashboard photograph in place. Preserve the workshop, camera, right-hand-drive body, windscreen/cowl and everything outside the dashboard face. The original glovebox is a visual no-touch region: keep its exact source-photo position, outline, size, colour, silver finish, patina, knob and black instruction plate; do not repaint, clean up, restyle, recolour or move it. The bare-shell photo has no cluster fitted, so copy the correct original Toyota cluster from the assembled owner-photo reference into the existing factory opening, preserving its exact silver bezel, patina, markings, black gauge faces, glass, needles and lower auxiliary windows; do not invent a different meter or alter the opening. Replace only the remaining visible face with one shallow cream/body-colour CNC sheet-metal panel. Remove and cover the ashtray. Install a visibly true 9-inch 16:9 LCD centred at X={PANEL_CENTRELINE_X:.0f}; do not shrink it.

Use exactly four matching large satin-silver circular directional outlets, approximately Ø87 face. Put one close to each usable face end and the inner two symmetrically to the left and right of the LCD so their midpoint equals the LCD/panel centreline. Raise all four so the top edges of their silver bezels share the LCD-bezel top datum; keep the inner pair outside the LCD with clear metal between. Do not create vent lobes or a lower vent channel. Most of the fascia remains only {PANEL_H-MAIN_LOWER_Y:.0f} mm high; only the compact right control channel uses the {PANEL_H:.0f} mm overall envelope.

Inside the compact right-hand channel beneath the original speedometer, fit one horizontal passenger-to-driver row using the supplied long-paddle industrial selector reference. Exact order: **WIPERS | LIGHTS | SPOTS | AUX | BLOWER | A/C | ENGINE | red HAZARD**. There are exactly seven chrome/black rotary selectors plus one separate red hazard—not eight selectors. Use small legible engraved labels and no toggles, square plates, spare switches or variable knobs. Do not add extra gauges, vents, screens, ashtrays or a full-width downward extension.

## Assembled owner-photo edit

Apply exactly that approved straight-on fascia to the supplied assembled oblique RHD owner photograph. Preserve perspective, steering wheel/column, seats, pedals, doors, workshop and all non-dashboard content. Treat both retained OEM items as visual no-touch regions: preserve the glovebox and speedometer/auxiliary cluster exactly as photographed, including their source-photo positions, outlines, sizes, colours, silver finish, patina, knob/black plate, markings, gauge faces, glass and needles. Do not repaint, clean up, restyle, recolour, relocate or reinterpret either item. Maintain the exact four top-aligned outlets, true-size central screen, shallow right control channel and single labelled control row. Natural perspective and steering-wheel occlusion are allowed; component count, ordering and relative size are not. Photorealistic owner-vehicle fabrication concept.

Final approved generated sources are copied into this package as the straight-on and assembled Rev H overlays. The supplied selector photograph is copied as `industrial_rotary_selector_reference.png`.

Generated overlays show visual intent only. DXF/CSV dimensions, M1-M10 physical templates and bought-part measurements control fabrication.
"""
    (OUT / "visualisation_prompt_record.md").write_text(text, encoding="utf-8")


def write_readme() -> None:
    readme = f"""# J40 RHD full-width 9-inch LCD / four-outlet dashboard - Rev H

Rev H replaces the complete visible dashboard face with one restrained body-colour CNC-formed panel while retaining and transferring the original Toyota speedometer assembly and the original asymmetric glovebox lid, knob, hinges/latch and black instruction plate. The ashtray is deleted. A true 9-inch display reference sits centrally. Exactly four larger silver circular A/C outlets are raised so their bezel tops align with the LCD bezel. All vents remain wholly in the normal {PANEL_H-MAIN_LOWER_Y:.0f} mm-high face; only a compact driver-side control channel extends lower.

This package is ready to send for **quotation and a full-size disposable CNC template**. It is deliberately not a production vehicle-cut release: the nominal {PANEL_W:.0f} x {PANEL_H:.0f} coordinate envelope cannot replace a physical trace of this vehicle. Only `CUT_TEMPLATE_OUTER` in `full_width_fit_template_rev_h.dxf` may be cut now, and only in MDF/card/cheap plastic. Every metal or vehicle feature remains `HOLD_*` until M1-M10 are signed.

## Locked layout

- Right-hand drive. Passenger is left; driver is right.
- One full-width visible face in 1.5 mm CR4 mild steel, low-gloss body colour.
- Original glovebox and speedometer are retained/reinstalled; their exact shapes and mounts are direct-transfer features, not nominal CNC geometry. In every owner-photo visual they are also **visual no-touch regions**: preserve their original colour, finish, patina, markings, controls and location exactly. The bare-shell visual may add only the correct original cluster copied from the assembled owner-photo reference into its existing factory opening.
- Screen active-image reference: **199.2 x 112.1 mm**, **228.6 mm / 9.000 inch diagonal**, 16:9. Its centre is constrained to the fascia centreline at nominal **X{PANEL_CENTRELINE_X:.1f}/Y{LCD_CY:.1f}**. This does not establish a real LCD chassis: the local Sehgal 9-inch listing has no mechanical drawing, so its aperture, bezel, rear body, mounts and connectors are M4-M5 HOLD.
- Four matching generic vents: **Ø87 visible silver/chrome face** and **Ø75 panel-opening reference**, dark directional core, hidden retention. Centre coordinates are {VENT_CENTRES}; all four centres share exactly **Y={VENT_CENTRE_DATUM_Y:.1f}**, placing every Ø87 bezel top at **Y={VENT_TOP_DATUM_Y:.1f}**, exactly aligned with the nominal LCD-bezel top. The inner pair is exactly mirrored at **X={VENT_CENTRES[1][0]:.1f} / {VENT_CENTRES[2][0]:.1f}**, or **±{INNER_VENT_CENTRE_OFFSET:.1f} mm** about the LCD/fascia centreline. Ø75 is **not** a released production cut.
- The upper band is **OEM glovebox | 9-inch LCD | OEM speedometer**. The four vents occupy the unused side gaps: one near each end and an inner pair symmetric about the LCD. Their visible top edges form one upper datum with the LCD bezel.
- The outer visible vent faces sit **6.5 mm** from the nominal usable-face ends; their Ø75 reference cuts retain **12.5 mm**. These tight lands are template/sample controlled and the outlets never move into the side returns.
- One shallow right control channel beneath the speedometer carries exactly seven industrial rotary selectors plus one separate red hazard in **one horizontal row**. Nominal centres are **39 mm pitch**, passenger-to-driver; Schneider Harmony XB4 reference: **Ø22.5 panel cut** and **68 mm rear envelope**. Head diameter, lever sweep, anti-rotation, rear stack, all four duct paths and driver clearance remain M6/M8/M9 HOLD. Engrave labels 3 mm high with black infill.

## Exact visible controls

| Position (passenger-to-driver) | Label | Hardware / states | What it does |
|---|---|---|---|
| Station 1 | WIPERS | 3-position: OFF / LOW / HIGH | Parks the wipers in OFF and selects low or high wipe. |
| Station 2 | LIGHTS | 3-position: OFF / SIDE / HEAD | Selects master exterior-light state; original dip/high-low remains. |
| Station 3 | SPOTS | 2-position: OFF / ON | Commands T5 spot-lamp relay. |
| Station 4 | AUX | 2-position: OFF / ON | Commands reserved accessory relay B2. |
| Station 5 | BLOWER | 3-position: OFF / LOW / HIGH | Sends OFF/LOW/HIGH requests to the measured blower controller. |
| Station 6 | A/C | 2-position: OFF / ON | Requests B1 compressor cooling through thermostat/trinary/pressure safeties. |
| Station 7 | ENGINE | 2-position: RUN / STOP | Sends a low-current command through the validated fuel-stop interface; key OFF remains authoritative and the manual cable remains the fallback. |
| Station 8 | HAZARD | separate red pushbutton: OFF / FLASH | Operates the hazard/flasher circuit. |

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

Use four branches from a balanced plenum, sized only after the received vent sample establishes the actual spigot OD and retention depth. Do not assume a 3-inch hose from the Ø75 face-cut reference. Do not crush ducts or block the glovebox, original instruments, steering column, loom, LCD connections, demist system or service removal. Prove that the raised vent necks and all four duct bends clear the LCD carrier, retained components and structure. In the lower right channel, prove that selector contact stacks and lever/head sweep clear both right-hand ducts, cluster, column and driver. Verify knee and lever clearance around the only local extension. Actual bought-vent drawings and the complete rear mock-up control every aperture, retainer, hose ID and bend radius.

## Procurement and dimensional provenance

- The cost-conscious reference is the common silver/chrome ABS **Ø87 face / Ø75 opening** generic outlet family. It is a reference listing, not a released part: buy four visually and mechanically matched outlets from a single batch at a local Pakistan automotive A/C counter, then complete M7 calipers before any vent holes are cut. The Joom listing records the published family dimensions; `component_procurement_and_sample_plan.csv` records the source and sample path.
- The matching Daraz lead is currently unavailable and publishes no usable dimensions, so it is not a source of truth. The Restomod Air Diablo billet outlet is retained only as a premium import fallback; it would require a different M7 cut/duct detail.
- Sehgal Motors' locally listed 9-inch universal LCD is the procurement baseline, but it publishes no chassis/cutout dimensions. Purchase/borrow a sample or obtain a manufacturer drawing before releasing M4-M5.
- A public 1968-1978 replacement-panel listing gives **1400 x 250 x 100 mm**, confirming that broad dashboard dimensions are publicly listed. It is a centimetre-resolution vendor product envelope—not an installed 1978 RHD face outline, bend schedule or aperture/datum drawing—and Toyota EPC records configuration-specific panels. Therefore the **{PANEL_W:.0f} x {PANEL_H:.0f}** Rev H coordinate model remains a proportional quote/template datum, not an OEM dimension. M1 physical trace/scan still controls production. `dimensional_provenance_audit.csv` records the source URL and every release boundary.

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
- Seven CSVs covering cut/release, fascia coordinates, switch positions, M1-M10 evidence, dimensional provenance, procurement/sample controls and the HVAC control interface.
- `visualisation_prompt_record.md` - reproducible image-edit prompt set and mode.

## Acceptance

The installed face reads as an original-adjacent J40 dashboard; the OEM glovebox and speedometer function normally and retain their original visible identity; the display proves a 9-inch active diagonal and remains serviceable; the LCD centre lies exactly on the signed fascia centreline; the midpoint of the two inner outlets lies on that same centreline with equal left/right offsets; exactly four matching large outlets receive unobstructed air and their visible bezel tops align with the LCD-bezel top datum; exactly seven labelled selectors plus the separate hazard occupy the signed one-row channel and match the schedule; the main lower edge remains shallow except for the compact right control channel; no duct, rear switch stack or driver contact clashes; no retained structure is weakened; and every M10 electrical/functional test passes without interference, voltage drop, overheating, rattle or unintended operation.
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
    assert {y for _, y in VENT_CENTRES} == {VENT_CENTRE_DATUM_Y}
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
    assert VENT_TOP_DATUM_Y == LCD_BEZEL[1] + LCD_BEZEL[3]
    assert all(vent_y + VENT_FACE_DIAMETER / 2 == VENT_TOP_DATUM_Y for _, vent_y in VENT_CENTRES)
    assert all(vent_y - VENT_FACE_DIAMETER / 2 > MAIN_LOWER_Y for _, vent_y in VENT_CENTRES)
    assert LCD_BEZEL[0] - (VENT_CENTRES[1][0] + VENT_FACE_DIAMETER / 2) == 10.5
    assert (VENT_CENTRES[2][0] - VENT_FACE_DIAMETER / 2) - (LCD_BEZEL[0] + LCD_BEZEL[2]) == 10.5
    assert GLOVEBOX_ENVELOPE[0] - (VENT_CENTRES[0][0] + VENT_FACE_DIAMETER / 2) == 3.5
    assert (VENT_CENTRES[1][0] - VENT_FACE_DIAMETER / 2) - (GLOVEBOX_ENVELOPE[0] + GLOVEBOX_ENVELOPE[2]) == 8.5
    assert SPEEDO_ENVELOPE[0] - (VENT_CENTRES[2][0] + VENT_FACE_DIAMETER / 2) == 10.5
    positions = control_positions()
    assert len(positions) == 8
    assert all(abs(positions[index + 1][0] - positions[index][0] - 39.0) < 0.001 for index in range(7))
    assert all(y == CONTROL_Y for _, y in positions)
    assert CONTROL_Y + CONTROL_LABEL_Y_OFFSET < MAIN_LOWER_Y
    assert positions[0][0] - SELECTOR_DIAMETER / 2 - (VENT_CENTRES[2][0] + VENT_FACE_DIAMETER / 2) == 9.25
    assert (VENT_CENTRES[3][0] - VENT_FACE_DIAMETER / 2) - (positions[-1][0] + HAZARD_DIAMETER / 2) == 25.5
    assert CONTROL_BANK[0] <= positions[0][0] - SELECTOR_DIAMETER / 2
    assert CONTROL_BANK[0] + CONTROL_BANK[2] >= positions[-1][0] + HAZARD_DIAMETER / 2
    required = [
        "README.md", "full_width_fascia_master_rev_h.dxf", "full_width_fit_template_rev_h.dxf",
        "right_control_bank_template_rev_h.dxf", "lcd_rear_support_reference_rev_h.dxf",
        "dashboard_lcd_hvac_fascia_rev_h_dimensioned_front.svg",
        "dashboard_lcd_hvac_fascia_rev_h_photo_overlay_assembled.png",
        "dashboard_lcd_hvac_fascia_rev_h_photo_overlay_bare_shell.png",
        "fabricator_cut_and_release_schedule.csv", "fascia_coordinate_schedule.csv",
        "switch_position_schedule.csv", "measurement_and_release_schedule.csv",
        "dimensional_provenance_audit.csv", "component_procurement_and_sample_plan.csv",
        "hvac_control_interface_schedule.csv",
        "j40_dashboard_lcd_hvac_fascia_rev_h_shop_spec.pdf", "visualisation_prompt_record.md",
    ]
    for name in required:
        assert (OUT / name).exists(), name


def package() -> None:
    DELIVERABLE.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DELIVERABLE, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(OUT.iterdir()):
            if path.is_file():
                archive.write(path, f"dashboard_lcd_hvac_fascia_rev_h/{path.name}")


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
    write_readme()
    write_pdf()
    validate()
    package()
    print(f"generated: {OUT}")
    print(f"archive:   {DELIVERABLE}")


if __name__ == "__main__":
    main()
