from __future__ import annotations

import csv
import shutil
import zipfile
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path("/Users/davidpridmore/IdeaProjects/J40")
OUT = ROOT / "data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_d"
DELIVERABLE = ROOT / "deliverables/fabrication_packages/dashboard_lcd_hvac_fascia_rev_d.zip"
CONCEPT_SOURCE = Path("/Users/davidpridmore/.codex/generated_images/019fb8d3-8269-7eb0-b457-d806a3cefbd4/exec-b63a5435-1f01-4ad8-ad49-468f2451bef8.png")
BASE_PHOTO = ROOT / "photos/20260413_040719.jpg"

# Quote/prototype envelope only. The vehicle template and actual bought parts
# control production geometry; see HOLD layers and release schedule.
FASCIA_W = 275.0
FASCIA_H = 225.0
CORNER_R = 6.0
# A nominal 9-inch 16:9 active image is 199.2 x 112.1 mm. The final aperture,
# outer bezel and rear body are controlled by the actual LCD manufacturer's drawing.
LCD_ACTIVE_W, LCD_ACTIVE_H = 199.2, 112.1
BEZEL_X, BEZEL_Y, BEZEL_W, BEZEL_H = 22.5, 72.0, 230.0, 132.0
SCREEN_X, SCREEN_Y, SCREEN_W, SCREEN_H = 36.5, 80.5, 202.0, 115.0
STRIP_X, STRIP_Y, STRIP_W, STRIP_H = 17.5, 20.0, 240.0, 40.0
SELECTOR_CENTRES = (52.5, 117.5, 182.5)
HAZARD_X = 232.5
SELECTOR_RADIUS = 11.15
UNDER_LABELS = ("BLOWER", "A/C REQUEST", "FUEL STOP / CONTROL")
RIGHT_MAP = (
    ("upper-left", "WIPERS", "3-position", "OFF / LOW / HIGH"),
    ("upper-right", "LIGHTS", "3-position", "OFF / SIDE / HEAD"),
    ("lower-left", "SPOTS", "2-position", "OFF / ON"),
    ("lower-right", "AUX", "2-position", "OFF / ON"),
)


def dxf_header() -> list[str]:
    return ["0", "SECTION", "2", "HEADER", "9", "$INSUNITS", "70", "4", "0", "ENDSEC", "0", "SECTION", "2", "ENTITIES"]


def dxf_line(layer: str, x1: float, y1: float, x2: float, y2: float) -> list[str]:
    return ["0", "LINE", "8", layer, "10", f"{x1:.3f}", "20", f"{y1:.3f}", "30", "0", "11", f"{x2:.3f}", "21", f"{y2:.3f}", "31", "0"]


def dxf_circle(layer: str, x: float, y: float, radius: float) -> list[str]:
    return ["0", "CIRCLE", "8", layer, "10", f"{x:.3f}", "20", f"{y:.3f}", "30", "0", "40", f"{radius:.3f}"]


def dxf_lwpoly(layer: str, points: list[tuple[float, float]], closed: bool = True) -> list[str]:
    rows = ["0", "LWPOLYLINE", "8", layer, "90", str(len(points)), "70", "1" if closed else "0"]
    for x, y in points:
        rows += ["10", f"{x:.3f}", "20", f"{y:.3f}"]
    return rows


def rounded_rect_points(x: float, y: float, w: float, h: float, r: float, segments: int = 8) -> list[tuple[float, float]]:
    import math

    pts: list[tuple[float, float]] = []
    for cx, cy, start in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
        for idx in range(segments + 1):
            angle = math.radians(start + idx * 90 / segments)
            pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts


def write_dxf(path: Path, entities: list[list[str]]) -> None:
    rows = dxf_header()
    for entity in entities:
        rows += entity
    rows += ["0", "ENDSEC", "0", "EOF"]
    path.write_text("\n".join(rows) + "\n", encoding="ascii")


def make_dxfs() -> None:
    fascia = [dxf_lwpoly("HOLD_VEHICLE_TEMPLATE", rounded_rect_points(0, 0, FASCIA_W, FASCIA_H, CORNER_R))]
    fascia.append(dxf_lwpoly("HOLD_LCD_BEZEL_ENVELOPE", rounded_rect_points(BEZEL_X, BEZEL_Y, BEZEL_W, BEZEL_H, 3)))
    fascia.append(dxf_lwpoly("HOLD_LCD_APERTURE", rounded_rect_points(SCREEN_X, SCREEN_Y, SCREEN_W, SCREEN_H, 3)))
    fascia.append(dxf_lwpoly("CUT_CONTROL_STRIP_APERTURE", rounded_rect_points(STRIP_X, STRIP_Y, STRIP_W, STRIP_H, 3)))
    for x, y in ((8, 8), (137.5, 8), (267, 8), (8, 212), (137.5, 212), (267, 212)):
        fascia.append(dxf_circle("HOLD_VEHICLE_TEMPLATE", x, y, 2.25))
    write_dxf(OUT / "centre_fascia_template_rev_d.dxf", fascia)

    strip = [dxf_lwpoly("CUT", rounded_rect_points(0, 0, STRIP_W, STRIP_H, 3))]
    for x in (35, 100, 165):
        strip.append(dxf_circle("HOLD_SELECTOR_APERTURES", x, STRIP_H / 2, SELECTOR_RADIUS))
    strip.append(dxf_circle("HOLD_HAZARD_APERTURE", 215, STRIP_H / 2, 8.0))
    for x in (6, STRIP_W - 6):
        strip.append(dxf_circle("CUT", x, STRIP_H / 2, 2.25))
    write_dxf(OUT / "centre_three_selector_strip_blank_rev_d.dxf", strip)

    right = [dxf_lwpoly("HOLD_VEHICLE_TRANSFER", rounded_rect_points(0, 0, 110, 90, 3))]
    for x, y in ((30, 65), (80, 65), (30, 25), (80, 25)):
        right.append(dxf_circle("HOLD_SELECTOR_APERTURES", x, y, SELECTOR_RADIUS))
        right.append(dxf_line("HOLD_CENTRELINES", x - 4, y, x + 4, y))
        right.append(dxf_line("HOLD_CENTRELINES", x, y - 4, x, y + 4))
    write_dxf(OUT / "right_cluster_four_selector_transfer_template_rev_d.dxf", right)

    clamp = [dxf_lwpoly("CUT", rounded_rect_points(0, 0, 250, 150, 3)), dxf_lwpoly("HOLD_LCD_REAR_BODY", rounded_rect_points(10, 10, 230, 130, 2))]
    for x, y in ((5, 5), (245, 5), (5, 145), (245, 145)):
        clamp.append(dxf_circle("CUT", x, y, 2.25))
    write_dxf(OUT / "lcd_rear_clamp_blank_rev_d.dxf", clamp)

    vent = [dxf_lwpoly("CUT", rounded_rect_points(0, 0, 82, 82, 5)), dxf_circle("HOLD_VENT_APERTURE", 41, 41, 31.75)]
    for x, y in ((8, 8), (74, 8)):
        vent.append(dxf_circle("CUT", x, y, 2.25))
    write_dxf(OUT / "underdash_eyeball_vent_bracket_blank_rev_d.dxf", vent)


def write_svg() -> None:
    s, x0, y0 = 2.15, 85, 130
    sx = lambda x: x0 + x * s
    sy = lambda y: y0 + (FASCIA_H - y) * s
    holes = "".join(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="5" class="hold"/>' for x, y in ((8,8),(137.5,8),(267,8),(8,212),(137.5,212),(267,212)))
    switches = "".join(
        f'<circle cx="{sx(x)}" cy="{sy(STRIP_Y+23)}" r="16" fill="#b8bec2" stroke="#161b1f" stroke-width="2"/>'
        f'<line x1="{sx(x)-7}" y1="{sy(STRIP_Y+23)+7}" x2="{sx(x)+11}" y2="{sy(STRIP_Y+23)-11}" stroke="#111" stroke-width="7" stroke-linecap="round"/>'
        for x in SELECTOR_CENTRES
    )
    under_labels = "".join(
        f'<text x="{sx(x)}" y="{sy(STRIP_Y+5)}" text-anchor="middle" class="label">{label}</text>'
        for x, label in zip(SELECTOR_CENTRES, UNDER_LABELS)
    )
    hazard = (
        f'<circle cx="{sx(HAZARD_X)}" cy="{sy(STRIP_Y+23)}" r="11" fill="#b51e23" stroke="#161b1f" stroke-width="2"/>'
        f'<text x="{sx(HAZARD_X)}" y="{sy(STRIP_Y+5)}" text-anchor="middle" class="label">HAZARD</text>'
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="760" viewBox="0 0 1180 760">
<style>.cut{{fill:none;stroke:#111;stroke-width:2}}.hold{{fill:#fff4df;stroke:#a85f00;stroke-width:2;stroke-dasharray:7 5}}.txt{{font:15px Arial;fill:#20262b}}.bold{{font:700 18px Arial;fill:#20262b}}.small{{font:13px Arial;fill:#53606a}}.label{{font:700 9px Arial;fill:#20262b}}.dim{{stroke:#aa2020;stroke-width:1.5}}</style>
<rect width="1180" height="760" fill="#f7f8f9"/><text x="55" y="44" class="bold">J40 RHD CENTRE LCD FASCIA - REV D</text><text x="55" y="70" class="small">Delete the entire ashtray and radio face; install one flat panel. Glovebox and speedometer pressing remain original.</text>
<rect x="{sx(0)}" y="{sy(FASCIA_H)}" width="{FASCIA_W*s}" height="{FASCIA_H*s}" rx="{CORNER_R*s}" fill="#e8e2cc" stroke="#a85f00" stroke-width="2" stroke-dasharray="7 5"/>
<rect x="{sx(BEZEL_X)}" y="{sy(BEZEL_Y+BEZEL_H)}" width="{BEZEL_W*s}" height="{BEZEL_H*s}" rx="7" fill="#11161a" stroke="#a85f00" stroke-width="2" stroke-dasharray="7 5"/>
<rect x="{sx(SCREEN_X)}" y="{sy(SCREEN_Y+SCREEN_H)}" width="{SCREEN_W*s}" height="{SCREEN_H*s}" rx="5" fill="#253846" stroke="#e8edf0" stroke-width="1"/>
<rect x="{sx(STRIP_X)}" y="{sy(STRIP_Y+STRIP_H)}" width="{STRIP_W*s}" height="{STRIP_H*s}" rx="6" fill="#e8e2cc" stroke="#111" stroke-width="2"/>{switches}{under_labels}{hazard}{holes}
<line x1="{sx(0)}" y1="{sy(0)+38}" x2="{sx(FASCIA_W)}" y2="{sy(0)+38}" class="dim"/><text x="{sx(112)}" y="{sy(0)+62}" class="bold">275 nominal</text>
<line x1="{sx(FASCIA_W)+35}" y1="{sy(FASCIA_H)}" x2="{sx(FASCIA_W)+35}" y2="{sy(0)}" class="dim"/><text x="{sx(FASCIA_W)+48}" y="{sy(105)}" class="bold">225 nominal</text>
<text x="{sx(57)}" y="{sy(137)}" fill="#fff" font-family="Arial" font-size="16">9-inch active image 199.2 x 112.1; 230 x 132 bezel envelope</text>
<rect x="750" y="105" width="390" height="535" rx="8" fill="#fff" stroke="#cbd2d7"/><text x="775" y="140" class="bold">FLAT-FACE SCOPE</text>
<text x="775" y="174" class="txt">Remove ashtray door, body, lip and seam.</text><text x="775" y="202" class="txt">Remove/cover the radio openings and surround.</text><text x="775" y="230" class="txt">One continuous flat body-colour face remains.</text><text x="775" y="258" class="txt">No ashtray feature survives in the finished face.</text>
<text x="775" y="302" class="bold">RIGHT OF SPEEDOMETER - 2 x 2</text>
<text x="790" y="337" class="small">UPPER LEFT</text><text x="970" y="337" class="small">UPPER RIGHT</text><text x="790" y="361" class="txt">WIPERS</text><text x="970" y="361" class="txt">LIGHTS</text>
<text x="790" y="401" class="small">LOWER LEFT</text><text x="970" y="401" class="small">LOWER RIGHT</text><text x="790" y="425" class="txt">SPOTS</text><text x="970" y="425" class="txt">AUX</text>
<text x="775" y="474" class="bold">UNDER LCD - LEFT TO RIGHT</text><text x="775" y="506" class="txt">BLOWER | A/C REQUEST | FUEL STOP / CONTROL</text><text x="775" y="532" class="small">Fuel-stop/control label is provisional pending live proof.</text>
<text x="775" y="576" class="bold">HVAC</text><text x="775" y="606" class="small">2 under-dash eyeball outlets; 63.5 mm hose target.</text>
<text x="55" y="710" class="small">Finish intent: body-colour cream, low gloss. DXF layers named HOLD are not production cut paths.</text></svg>'''
    (OUT / "dashboard_lcd_hvac_fascia_rev_d_dimensioned_front.svg").write_text(svg, encoding="utf-8")


def draw_image_fit(c: canvas.Canvas, path: Path, x: float, y: float, max_w: float, max_h: float) -> None:
    if not path.exists():
        return
    img = ImageReader(str(path))
    iw, ih = img.getSize()
    scale = min(max_w / iw, max_h / ih)
    draw_w, draw_h = iw * scale, ih * scale
    c.drawImage(img, x + (max_w - draw_w) / 2, y + (max_h - draw_h) / 2, draw_w, draw_h, preserveAspectRatio=True)


def write_pdf() -> None:
    path = OUT / "j40_dashboard_lcd_hvac_fascia_rev_d_shop_spec.pdf"
    c = canvas.Canvas(str(path), pagesize=landscape(A3))
    w, h = landscape(A3)
    c.setTitle("J40 RHD Centre LCD Fascia Rev D")

    # Page 1: nominal front geometry and locked scope.
    c.setFont("Helvetica-Bold", 18)
    c.drawString(16*mm, h-16*mm, "J40 RHD Centre 9-inch LCD / HVAC Fascia - Rev D")
    c.setFont("Helvetica", 9)
    c.drawRightString(w-16*mm, h-16*mm, "Units mm | Quote + 1:1 prototype | Production geometry HOLD")
    x, y = 18*mm, 31*mm
    c.setFillColor(HexColor("#e8e2cc"))
    c.setStrokeColor(HexColor("#a85f00"))
    c.setDash(5, 4)
    c.roundRect(x, y, FASCIA_W*mm, FASCIA_H*mm, CORNER_R*mm, fill=1, stroke=1)
    c.setFillColor(HexColor("#11161a"))
    c.roundRect(x+BEZEL_X*mm, y+BEZEL_Y*mm, BEZEL_W*mm, BEZEL_H*mm, 3*mm, fill=1, stroke=1)
    c.setDash()
    c.setFillColor(HexColor("#253846"))
    c.setStrokeColor(HexColor("#e8edf0"))
    c.roundRect(x+SCREEN_X*mm, y+SCREEN_Y*mm, SCREEN_W*mm, SCREEN_H*mm, 2*mm, fill=1, stroke=1)
    c.setFillColor(HexColor("#e8e2cc"))
    c.setStrokeColor(HexColor("#111111"))
    c.roundRect(x+STRIP_X*mm, y+STRIP_Y*mm, STRIP_W*mm, STRIP_H*mm, 3*mm, fill=1, stroke=1)
    for hx, label in zip(SELECTOR_CENTRES, UNDER_LABELS):
        c.setFillColor(HexColor("#b8bec2"))
        c.circle(x+hx*mm, y+(STRIP_Y+23)*mm, 6*mm, fill=1, stroke=1)
        c.setFillColor(HexColor("#20262b"))
        c.setFont("Helvetica-Bold", 5.7 if "FUEL" in label else 6.3)
        c.drawCentredString(x+hx*mm, y+(STRIP_Y+4.3)*mm, label)
    c.setFillColor(HexColor("#b51e23"))
    c.circle(x+HAZARD_X*mm, y+(STRIP_Y+23)*mm, 4.5*mm, fill=1, stroke=1)
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 5.8)
    c.drawCentredString(x+HAZARD_X*mm, y+(STRIP_Y+4.3)*mm, "HAZARD")
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(x+(FASCIA_W/2)*mm, y+137*mm, '9-inch active image: 199.2 x 112.1 (228.6 diagonal)')
    c.setFont("Helvetica", 7)
    c.drawCentredString(x+(FASCIA_W/2)*mm, y+126*mm, "Nominal aperture 202 x 115 | bezel envelope 230 x 132 | actual LCD drawing controls")

    nx, yy = 306*mm, h-34*mm
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(nx, yy, "FLAT-FACE CUTTING SCOPE")
    c.setFont("Helvetica", 8.2)
    for row in [
        "Remove the complete protruding ashtray: door, body, lip, seam and recess.",
        "Remove/cover the adjacent radio openings and their separate surround.",
        "Make one continuous flat body-colour face across the combined zone.",
        "No ashtray outline, knob, door, recess or separate blank remains.",
        "Preserve the glovebox/instruction panel and speedometer pressing unchanged.",
        "Nominal fascia envelope: 275 x 225 x 1.5 CR4 steel; template controls.",
    ]:
        yy -= 8*mm
        c.drawString(nx, yy, row)
    yy -= 6*mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(nx, yy, "EXACT SELECTOR POSITIONS")
    c.setFont("Helvetica", 8.2)
    for row in [
        "RIGHT OF SPEEDOMETER, viewed from cabin:",
        "  upper-left WIPERS | upper-right LIGHTS",
        "  lower-left SPOTS | lower-right AUX",
        "UNDER LCD, left to right:",
        "  BLOWER | A/C REQUEST | FUEL STOP / CONTROL (provisional)",
        "Separate red HAZARD; indicators stay on the OEM stalk.",
    ]:
        yy -= 7.5*mm
        c.drawString(nx, yy, row)
    yy -= 6*mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(nx, yy, "HVAC / RELEASE")
    c.setFont("Helvetica", 8.2)
    for row in [
        "Two directional eyeball outlets mount below the dash, not in this face.",
        "Target 63.5 / 2.5-inch hose neck; actual vent and duct trial controls.",
        "All orange/dashed and HOLD_* geometry is reference, not a cut path.",
        "Complete and sign M1-M8 before any final panel or vehicle cutting.",
    ]:
        yy -= 7.5*mm
        c.drawString(nx, yy, row)
    c.setFillColor(HexColor("#8b1e1e"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(18*mm, 14*mm, "QUOTE / TEMPLATE READY. DO NOT PRODUCTION-CUT THE PANEL OR VEHICLE UNTIL THE ACTUAL LCD, SELECTORS, VENTS AND 1:1 VEHICLE TEMPLATE ARE SIGNED.")
    c.showPage()

    # Page 2: source photograph, corrected overlay, and physical map.
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(16*mm, h-16*mm, "Actual-dashboard basis and locked control layout")
    c.setFont("Helvetica", 9)
    c.drawRightString(w-16*mm, h-16*mm, "Photographs establish intent only - do not scale")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(18*mm, h-31*mm, "BEFORE - OWNER'S RHD DASHBOARD")
    c.drawString(216*mm, h-31*mm, "REV D OVERLAY - ASHTRAY DELETED / FACE FLATTENED")
    draw_image_fit(c, BASE_PHOTO, 18*mm, 164*mm, 184*mm, 94*mm)
    overlay_path = OUT / "dashboard_lcd_hvac_fascia_rev_d_photo_overlay.png"
    draw_image_fit(c, overlay_path, 216*mm, 164*mm, 184*mm, 94*mm)
    c.setFont("Helvetica", 8.2)
    c.drawString(18*mm, 153*mm, "Preserve: glovebox, instruction plate, speedometer/instrument pressing and main dash character lines.")
    c.drawString(216*mm, 153*mm, "Replace: the whole protruding ashtray/radio zone with one flat cream face carrying the 9-inch LCD.")

    # Centre-strip map at actual nominal width.
    map_x, map_y = 18*mm, 48*mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(map_x, 137*mm, "UNDER THE SCREEN - LEFT TO RIGHT")
    c.setFillColor(HexColor("#e8e2cc"))
    c.setStrokeColor(HexColor("#111111"))
    c.roundRect(map_x, map_y, STRIP_W*mm, STRIP_H*mm, 3*mm, fill=1, stroke=1)
    for local_x, label, states in zip((35, 100, 165), UNDER_LABELS, ("OFF / LOW / HIGH", "OFF / ON", "PROVISIONAL")):
        c.setFillColor(HexColor("#b8bec2"))
        c.circle(map_x+local_x*mm, map_y+24*mm, 7*mm, fill=1, stroke=1)
        c.setFillColor(HexColor("#20262b"))
        c.setFont("Helvetica-Bold", 7 if "FUEL" not in label else 6.2)
        c.drawCentredString(map_x+local_x*mm, map_y+10*mm, label)
        c.setFont("Helvetica", 6.2)
        c.drawCentredString(map_x+local_x*mm, map_y+4.5*mm, states)
    c.setFillColor(HexColor("#b51e23"))
    c.circle(map_x+215*mm, map_y+24*mm, 5.5*mm, fill=1, stroke=1)
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(map_x+215*mm, map_y+10*mm, "HAZARD")
    c.setFont("Helvetica", 6.2)
    c.drawCentredString(map_x+215*mm, map_y+4.5*mm, "SEPARATE")

    # Right 2 x 2 map.
    rx, ry = 302*mm, 42*mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(rx, 137*mm, "RIGHT OF SPEEDOMETER - VIEWED FROM CABIN")
    c.setFillColor(HexColor("#f2f3f4"))
    c.roundRect(rx, ry, 94*mm, 86*mm, 3*mm, fill=1, stroke=1)
    for px, py, label, states in [
        (24, 61, "WIPERS", "OFF / LOW / HIGH"),
        (70, 61, "LIGHTS", "OFF / SIDE / HEAD"),
        (24, 22, "SPOTS", "OFF / ON"),
        (70, 22, "AUX", "OFF / ON"),
    ]:
        c.setFillColor(HexColor("#b8bec2"))
        c.circle(rx+px*mm, ry+py*mm, 7*mm, fill=1, stroke=1)
        c.setFillColor(HexColor("#20262b"))
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(rx+px*mm, ry+(py-12)*mm, label)
        c.setFont("Helvetica", 5.8)
        c.drawCentredString(rx+px*mm, ry+(py-17)*mm, states)
    c.setFont("Helvetica", 7.5)
    c.drawString(18*mm, 27*mm, "Two hose-fed A/C eyeball vents mount on separate reversible under-dash brackets, one each side of the centre insert.")
    c.drawString(18*mm, 20*mm, "The overlay uses the bought industrial selector style. Final 22.3 mm holes and anti-rotation details come from caliper measurement of all seven actual selectors.")
    c.showPage()

    # Page 3: electrical and production release schedule.
    c.setFont("Helvetica-Bold", 18)
    c.drawString(16*mm, h-16*mm, "Selector schedule, electrical constraints and production release")
    c.setFont("Helvetica", 9)
    c.drawRightString(w-16*mm, h-16*mm, "Function assignment locked except fuel-stop/control; all hole centres measured before cut")
    left = 15*mm
    top = h-34*mm
    col_widths = [30, 43, 30, 43, 51, 82, 108]
    headers = ["ID", "LOCATION", "TYPE", "FUNCTION", "STATES", "CONTROL / RELAY", "RELEASE NOTE"]
    rows = [
        ["R-UL", "right upper-left", "3-pos", "WIPERS", "OFF/LOW/HIGH", "existing wiper control", "Function locked; actual hole/stack HOLD"],
        ["R-UR", "right upper-right", "3-pos", "LIGHTS", "OFF/SIDE/HEAD", "T1 low + T2 high beam controls", "Function locked; prove headlamp logic"],
        ["R-LL", "right lower-left", "2-pos", "SPOTS", "OFF/ON", "T5 spot-lamp relay trigger", "Function and hole-3 allocation locked"],
        ["R-LR", "right lower-right", "2-pos", "AUX", "OFF/ON", "B2 auxiliary control", "Function locked; final accessory/load HOLD"],
        ["C-L", "under LCD left", "3-pos", "BLOWER", "OFF/LOW/HIGH", "dedicated HVAC control/relay", "Load, resistor and relay sizing HOLD"],
        ["C-C", "under LCD centre", "2-pos", "A/C REQUEST", "OFF/ON", "B1 through safety chain", "Pressure/trinary interlock mandatory"],
        ["C-R", "under LCD right", "2-pos", "FUEL STOP / CONTROL", "prove states", "ignition-linked stop control", "PROVISIONAL; retain manual cable"],
    ]
    row_h = 14*mm
    x_cursor = left
    c.setFillColor(HexColor("#30373d"))
    c.setStrokeColor(HexColor("#7d878f"))
    for width, header in zip(col_widths, headers):
        c.rect(x_cursor, top-row_h, width*mm, row_h, fill=1, stroke=1)
        c.setFillColor(HexColor("#ffffff"))
        c.setFont("Helvetica-Bold", 7)
        c.drawString(x_cursor+2*mm, top-8.5*mm, header)
        c.setFillColor(HexColor("#30373d"))
        x_cursor += width*mm
    y_cursor = top-row_h
    for ridx, row in enumerate(rows):
        x_cursor = left
        fill = HexColor("#f1f3f4") if ridx % 2 == 0 else HexColor("#ffffff")
        for cidx, (width, value) in enumerate(zip(col_widths, row)):
            c.setFillColor(fill)
            c.rect(x_cursor, y_cursor-row_h, width*mm, row_h, fill=1, stroke=1)
            c.setFillColor(HexColor("#20262b"))
            c.setFont("Helvetica-Bold" if cidx in (0, 3) else "Helvetica", 6.5)
            words = value.split()
            if len(value) <= 24:
                c.drawString(x_cursor+2*mm, y_cursor-8.3*mm, value)
            else:
                split_at = max(1, len(words)//2)
                c.drawString(x_cursor+2*mm, y_cursor-5.8*mm, " ".join(words[:split_at]))
                c.drawString(x_cursor+2*mm, y_cursor-10.6*mm, " ".join(words[split_at:]))
            x_cursor += width*mm
        y_cursor -= row_h

    note_y = y_cursor-10*mm
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(15*mm, note_y, "ELECTRICAL RULES")
    c.setFont("Helvetica", 8)
    for row in [
        "Selectors command fused relay/control circuits only; do not switch blower, lamps, clutch or other high-current loads directly.",
        "Frozen relay baseline: T1 LOW BEAM, T2 HIGH BEAM, T3 HORN, T4 CONDENSER FAN, T5 SPOTS, B1 A/C CLUTCH, B2 AUX.",
        "A/C REQUEST may energise B1 only through the thermostat / trinary / pressure-protection chain; T4 fan behaviour is proved with the selected HVAC hardware.",
        "BLOWER uses its dedicated measured HVAC control/relay/resistor circuit. T1 and T2 are lighting relays and must not be reassigned.",
        "FUEL STOP / CONTROL remains provisional until device identity, terminal behaviour and engine RUN-to-OFF shutdown are live-tested; retain the manual stop cable.",
        "Hazard is a separate red control. Left/right indicators remain on the original stalk.",
    ]:
        note_y -= 7*mm
        c.drawString(15*mm, note_y, row)
    note_y -= 6*mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(15*mm, note_y, "M1-M8 PRODUCTION HOLD GATES")
    c.setFont("Helvetica", 7.5)
    for row in [
        "M1 vehicle contour/flat lands + ashtray/radio removal boundary | M2 actual LCD active/aperture/bezel drawing | M3 LCD rear body, mount, connector and depth",
        "M4 all seven selector bushes, anti-rotation and rear stacks | M5 transfer actual four right-cluster centres | M6 actual vent face, neck, hose and rear depth",
        "M7 signed 1:1 prototype: glovebox, instruments, steering, gear lever, sight line, wiring and duct sweeps | M8 labels, continuity, relay map and live function tests",
    ]:
        note_y -= 7*mm
        c.drawString(15*mm, note_y, row)
    c.setFillColor(HexColor("#8b1e1e"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(15*mm, 20*mm, "RELEASE: quotation, card/acrylic template and cheap-sheet prototype only. Production metal and vehicle cutting remain HOLD until M1-M8 are signed.")
    c.setFillColor(HexColor("#53606a"))
    c.setFont("Helvetica", 6.7)
    c.drawString(15*mm, 13*mm, "Electrical basis: electrical_master.csv; electrical_diagram_reconciliation_20260518.csv; engine_electrical_inputs_reconciliation_20260517.csv; expenses.csv.")
    c.showPage()
    c.save()


def write_csvs() -> None:
    with (OUT / "fabricator_cut_list.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["part", "qty", "material", "thickness_mm", "finish", "file", "release"])
        w.writerows([
            ["centre flat-face fascia template", 1, "CR4 mild steel", 1.5, "body-colour low-gloss paint", "centre_fascia_template_rev_d.dxf", "QUOTE/PROTOTYPE ONLY; vehicle contour, LCD bezel/aperture and fixing points HOLD"],
            ["centre three-selector strip blank", 1, "5052-H32 aluminium", 2.0, "body-colour low-gloss paint", "centre_three_selector_strip_blank_rev_d.dxf", "outer/fasteners released; selector and hazard holes HOLD"],
            ["right-cluster four-selector transfer template", 1, "card/acrylic template", 2.0, "none", "right_cluster_four_selector_transfer_template_rev_d.dxf", "ALL GEOMETRY HOLD; transfer actual vehicle centres"],
            ["LCD rear clamp blank", 1, "5052-H32 aluminium", 2.0, "black", "lcd_rear_clamp_blank_rev_d.dxf", "outer/fasteners released; rear-body opening HOLD"],
            ["under-dash eyeball vent bracket blank", 2, "5052-H32 aluminium", 2.0, "satin black", "underdash_eyeball_vent_bracket_blank_rev_d.dxf", "outer/fasteners released; vent aperture HOLD"],
        ])
    with (OUT / "measurement_and_release_schedule.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["id", "measurement", "nominal_or_intent", "required_evidence", "status"])
        w.writerows([
            ["M1", "combined ashtray/radio removal boundary, centre contour and flat mounting lands", "275 x 225 envelope only; finished face has no ashtray feature", "1:1 card template plus front/rear ruler photos and signed removal line", "HOLD"],
            ["M2", "LCD active area/aperture/bezel/rear body/mount/connectors", "9-inch 16:9 active 199.2 x 112.1; aperture 202 x 115; bezel envelope 230 x 132 reference", "actual LCD model drawing and caliper dimensions", "HOLD"],
            ["M3", "LCD rear body/mount centres/depth/connector sweep", "supplier-specific", "rear rubbing, depth gauge and plug trial", "HOLD"],
            ["M4", "seven Schneider selector bushes/anti-rotation/contact blocks", "22.3 mm nominal aperture", "measure each bought selector and rear stack", "HOLD"],
            ["M5", "four original right-cluster hole centres and rear clearance", "reuse 2 x 2 positions", "vehicle transfer template and rear photo", "HOLD"],
            ["M6", "eyeball vent face/cutout/flange/neck OD/rear depth", "63.5 mm hose-neck target", "actual vent and hose trial", "HOLD"],
            ["M7", "rear clearance, glovebox, instruments, steering and gear lever", "unchanged/no contact", "signed 1:1 overlay and full physical sweep", "HOLD"],
            ["M8", "selector function/labels and electrical prove-out", "3 x 3-position plus 4 x 2-position", "continuity test, relay map, A/C interlock and fuel-stop test", "HOLD"],
        ])
    with (OUT / "switch_position_schedule.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "physical_location_viewed_from_cabin", "selector_type", "function", "states", "control_or_relay", "release"])
        w.writerows([
            ["R-UL", "right of speedometer upper-left", "3-position maintained", "WIPERS", "OFF / LOW / HIGH", "existing wiper control circuit", "function locked; aperture/rear stack HOLD"],
            ["R-UR", "right of speedometer upper-right", "3-position maintained", "LIGHTS", "OFF / SIDE / HEAD", "T1 low-beam and T2 high-beam control logic", "function locked; prove lighting logic"],
            ["R-LL", "right of speedometer lower-left", "2-position maintained", "SPOTS", "OFF / ON", "T5 spot-lamp relay trigger", "function and existing hole-3 allocation locked"],
            ["R-LR", "right of speedometer lower-right", "2-position maintained", "AUX", "OFF / ON", "B2 auxiliary control", "function locked; final accessory/load HOLD"],
            ["C-L", "under LCD left", "3-position maintained", "BLOWER", "OFF / LOW / HIGH", "dedicated HVAC control/relay/resistor", "function locked; final load and circuit sizing HOLD"],
            ["C-C", "under LCD centre", "2-position maintained", "A/C REQUEST", "OFF / ON", "B1 A/C clutch request through thermostat/trinary/pressure safety chain", "function locked; safety-chain prove-out HOLD"],
            ["C-R", "under LCD right", "2-position maintained", "FUEL STOP / CONTROL", "prove on vehicle", "ignition-linked stop/control with manual cable backup", "PROVISIONAL pending device identification and live key-OFF shutdown test"],
            ["H", "under LCD far-right", "separate red pushbutton", "HAZARD", "OFF / FLASH", "existing hazard circuit", "separate from seven selectors; indicators remain on OEM stalk"],
        ])


def write_readme() -> None:
    text = """# J40 RHD Centre 9-inch LCD / HVAC Fascia - Rev D

Rev D starts with the owner's actual right-hand-drive dashboard photograph and makes the centre change explicit: the entire protruding ashtray is removed, the adjacent radio openings are absorbed, and the combined zone becomes one continuous flat body-colour face. The glovebox/instruction panel and speedometer/instrument pressing stay original.

## Locked visual and fabrication scope

- Delete the complete ashtray door, body, lip, seam and recess. No ashtray outline or separate blank remains in the finished face.
- Remove or cover the separate radio openings and surround within the same centre-zone removal boundary.
- Form one flat, nearly flush CNC fascia across that combined zone. Nominal quotation envelope: 275 x 225 x 1.5 mm CR4 steel; the signed vehicle template controls the production contour.
- Use a true 9-inch 16:9 active-image reference: 199.2 x 112.1 mm, 228.6 mm diagonal. Nominal aperture: 202 x 115 mm. Nominal bezel envelope: 230 x 132 mm. The actual LCD manufacturer's drawing controls every final screen dimension.
- Fit the seven purchased 22 mm industrial rotary selectors: four in the original right-hand 2 x 2 positions and three below the LCD. Hazard remains a separate red pushbutton.
- Put two directional A/C eyeball outlets on separate reversible brackets below the dashboard, one each side of the centre insert. Preferred hose-neck target is 63.5 mm / 2.5 inch after actual vent and hose measurement.
- Finish the fascia in low-gloss body colour with a restrained thin black LCD bezel. Preserve the original dashboard character outside the centre removal boundary.

## Exact control positions

All positions are viewed from the cabin.

Right of the speedometer, original 2 x 2 cluster:

- Upper-left: WIPERS — 3-position, OFF / LOW / HIGH.
- Upper-right: LIGHTS — 3-position, OFF / SIDE / HEAD.
- Lower-left: SPOTS — 2-position, OFF / ON; existing right-dash hole 3 and relay T5.
- Lower-right: AUX — 2-position, OFF / ON; B2 auxiliary control.

Under the LCD, left to right:

- Left: BLOWER — 3-position, OFF / LOW / HIGH.
- Centre: A/C REQUEST — 2-position, OFF / ON.
- Right: FUEL STOP / CONTROL — 2-position, provisional pending device and live shutdown proof.
- Far-right: separate red HAZARD pushbutton; not one of the seven selectors.

Indicators remain on the OEM stalk.

## Electrical rules

- Every selector commands a protected relay/control circuit; no selector directly carries a high-current lamp, blower, clutch or accessory load.
- Frozen relay baseline is T1 low beam, T2 high beam, T3 horn, T4 condenser fan, T5 spot lamps, B1 A/C clutch and B2 auxiliary accessory.
- The blower uses a dedicated HVAC control/relay/resistor circuit sized from the selected blower's measured load. T1 and T2 are lighting relays and must not be used for blower speeds.
- A/C REQUEST may energise B1 only through the thermostat / trinary / pressure-protection chain. Condenser-fan behaviour through T4 is proved with the final HVAC hardware.
- FUEL STOP / CONTROL remains a release HOLD until the actual device and terminals are identified and key-OFF shutdown is proved with the engine running. Retain the manual diesel stop cable.

Evidence basis: data/manual/workbook_tabs/electrical_master.csv, data/manual/reference_projects_and_ideas.csv, data/manual/expenses.csv, data/manual/electrical_diagram_reconciliation_20260518.csv and data/manual/engine_electrical_inputs_reconciliation_20260517.csv.

## CNC release rules

DXF layers named HOLD_* are not production toolpaths. They provide nominal intent for quotation and cheap templates only.

1. Mark and photograph the exact ashtray/radio removal boundary, contour and flat lands from both sides.
2. Measure the actual LCD, all seven selector bushes and rear contact stacks, the hazard control, both vents and the hose.
3. Transfer the four existing right-cluster hole centres from the vehicle; never drill them from the nominal DXF.
4. Build a 1:1 card/acrylic or cheap-sheet prototype and install all actual parts.
5. Prove glovebox opening, instrument-panel rigidity, driver sight line, steering/gear-lever clearance, wiring and connector sweep, selector rear-stack clearance and duct bend radius.
6. Obtain owner sign-off on M1-M8, every cut edge and every centre before production cutting.
7. Cut the vehicle undersize, trim progressively, radius/deburr every edge and epoxy-prime all exposed steel before paint.

## Acceptance

- The complete protruding ashtray is gone and the ashtray/radio zone reads as one flat face.
- The 9-inch screen active area and bezel are verified against the actual LCD drawing, not inferred from the photograph.
- Glovebox, instruction panel and speedometer/instrument pressing remain visually and structurally unchanged.
- No new main-face vent opening exists; the two hose-fed outlets are below the dash on removable brackets.
- Screen, control strip and vents remain independently service-removable from the cabin side.
- All seven selector positions and labels match switch_position_schedule.csv.
- Wiring continuity, A/C safety logic, blower load, lighting logic, fuel-stop shutdown, vent flow and vibration/rattle tests pass.

## Package contents

- j40_dashboard_lcd_hvac_fascia_rev_d_shop_spec.pdf — three-page CNC brief, before/after actual-photo basis, exact selector map and electrical release schedule.
- dashboard_lcd_hvac_fascia_rev_d_dimensioned_front.svg — nominal front layout with 9-inch scale and labels.
- dashboard_lcd_hvac_fascia_rev_d_photo_overlay.png — corrected edit of the owner's actual RHD dashboard; do not scale.
- Five Rev D DXFs — quote/template blanks with explicit CUT and HOLD layers.
- fabricator_cut_list.csv, measurement_and_release_schedule.csv and switch_position_schedule.csv — production controls.

Ready to send for quotation, vehicle templating and a cardboard/acrylic or cheap-sheet prototype. Not released for production metal or vehicle cutting until M1-M8 are completed and signed.
"""
    (OUT / "README.md").write_text(text, encoding="utf-8")

def package() -> None:
    DELIVERABLE.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DELIVERABLE, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.iterdir()):
            z.write(p, f"dashboard_lcd_hvac_fascia_rev_d/{p.name}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if CONCEPT_SOURCE.exists():
        shutil.copy2(CONCEPT_SOURCE, OUT / "dashboard_lcd_hvac_fascia_rev_d_photo_overlay.png")
    make_dxfs(); write_svg(); write_csvs(); write_readme(); write_pdf(); package()
    print(OUT); print(DELIVERABLE)


if __name__ == "__main__":
    main()
