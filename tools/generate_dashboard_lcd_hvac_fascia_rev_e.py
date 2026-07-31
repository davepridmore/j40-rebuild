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
OUT = ROOT / "data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_e"
DELIVERABLE = ROOT / "deliverables/fabrication_packages/dashboard_lcd_hvac_fascia_rev_e.zip"
CONCEPT_ASSEMBLED_SOURCE = Path(
    "/Users/davidpridmore/.codex/generated_images/019fb8d3-8269-7eb0-b457-d806a3cefbd4/exec-e3219d76-5a5b-46c6-80f1-d952a52e5c5c.png"
)
CONCEPT_BARE_SOURCE = Path(
    "/Users/davidpridmore/.codex/generated_images/019fb8d3-8269-7eb0-b457-d806a3cefbd4/exec-60de0e87-1074-4f03-80e1-6ffe35da8820.png"
)
ASSEMBLED_BASE_PHOTO = ROOT / "photos/20260317_165113.jpg"
BARE_BASE_PHOTO = ROOT / "photos/20260413_040719.jpg"

# Released rectangular fascia blank. The owner authorises cutting the centre dash
# as required, while the original speedometer pressing and glovebox remain protected.
FASCIA_W = 410.0
FASCIA_H = 225.0
CORNER_R = 6.0
VEHICLE_CUT_X, VEHICLE_CUT_Y = 18.0, 18.0
VEHICLE_CUT_W, VEHICLE_CUT_H = 374.0, 189.0
VEHICLE_CUT_R = 3.0
# A nominal 9-inch 16:9 active image is 199.2 x 112.1 mm. The final aperture,
# outer bezel and rear body are controlled by the actual LCD manufacturer's drawing.
LCD_ACTIVE_W, LCD_ACTIVE_H = 199.2, 112.1
BEZEL_X, BEZEL_Y, BEZEL_W, BEZEL_H = 90.0, 72.0, 230.0, 132.0
SCREEN_X, SCREEN_Y, SCREEN_W, SCREEN_H = 104.0, 80.5, 202.0, 115.0
STRIP_X, STRIP_Y, STRIP_W, STRIP_H = 90.0, 20.0, 230.0, 40.0
SELECTOR_CENTRES = (120.0, 185.0, 250.0)
HAZARD_X = 300.0
SELECTOR_RADIUS = 11.15
VENT_CENTRES = ((52.0, 51.0), (358.0, 51.0))
VENT_FACE_RADIUS = 35.0
VENT_CUTOUT_RADIUS = 33.0
VENT_HOSE_TARGET_DIAMETER = 63.5
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
    fascia = [dxf_lwpoly("CUT_FASCIA_OUTER", rounded_rect_points(0, 0, FASCIA_W, FASCIA_H, CORNER_R))]
    fascia.append(
        dxf_lwpoly(
            "MARK_PROPOSED_VEHICLE_CUT",
            rounded_rect_points(VEHICLE_CUT_X, VEHICLE_CUT_Y, VEHICLE_CUT_W, VEHICLE_CUT_H, VEHICLE_CUT_R),
        )
    )
    fascia.append(dxf_lwpoly("HOLD_LCD_BEZEL_ENVELOPE", rounded_rect_points(BEZEL_X, BEZEL_Y, BEZEL_W, BEZEL_H, 3)))
    fascia.append(dxf_lwpoly("HOLD_LCD_APERTURE", rounded_rect_points(SCREEN_X, SCREEN_Y, SCREEN_W, SCREEN_H, 3)))
    fascia.append(dxf_lwpoly("HOLD_CONTROL_STRIP_APERTURE", rounded_rect_points(STRIP_X, STRIP_Y, STRIP_W, STRIP_H, 3)))
    for vent_x, vent_y in VENT_CENTRES:
        fascia.append(dxf_circle("HOLD_VENT_FACE_ENVELOPE", vent_x, vent_y, VENT_FACE_RADIUS))
        fascia.append(dxf_circle("HOLD_VENT_NECK_CUTOUT", vent_x, vent_y, VENT_CUTOUT_RADIUS))
        fascia.append(dxf_line("HOLD_CENTRELINES", vent_x - 5, vent_y, vent_x + 5, vent_y))
        fascia.append(dxf_line("HOLD_CENTRELINES", vent_x, vent_y - 5, vent_x, vent_y + 5))
    for x, y in ((9, 9), (205, 9), (401, 9), (9, 216), (205, 216), (401, 216)):
        fascia.append(dxf_circle("HOLD_MOUNTING_HOLES", x, y, 2.25))
    write_dxf(OUT / "centre_fascia_template_rev_e.dxf", fascia)

    strip = [dxf_lwpoly("CUT", rounded_rect_points(0, 0, STRIP_W, STRIP_H, 3))]
    for x in (30, 95, 160):
        strip.append(dxf_circle("HOLD_SELECTOR_APERTURES", x, STRIP_H / 2, SELECTOR_RADIUS))
    strip.append(dxf_circle("HOLD_HAZARD_APERTURE", 210, STRIP_H / 2, 8.0))
    for x in (6, STRIP_W - 6):
        strip.append(dxf_circle("CUT", x, STRIP_H / 2, 2.25))
    write_dxf(OUT / "centre_three_selector_strip_blank_rev_e.dxf", strip)

    right = [dxf_lwpoly("HOLD_VEHICLE_TRANSFER", rounded_rect_points(0, 0, 110, 90, 3))]
    for x, y in ((30, 65), (80, 65), (30, 25), (80, 25)):
        right.append(dxf_circle("HOLD_SELECTOR_APERTURES", x, y, SELECTOR_RADIUS))
        right.append(dxf_line("HOLD_CENTRELINES", x - 4, y, x + 4, y))
        right.append(dxf_line("HOLD_CENTRELINES", x, y - 4, x, y + 4))
    write_dxf(OUT / "right_cluster_four_selector_transfer_template_rev_e.dxf", right)

    clamp = [dxf_lwpoly("CUT", rounded_rect_points(0, 0, 250, 150, 3)), dxf_lwpoly("HOLD_LCD_REAR_BODY", rounded_rect_points(10, 10, 230, 130, 2))]
    for x, y in ((5, 5), (245, 5), (5, 145), (245, 145)):
        clamp.append(dxf_circle("CUT", x, y, 2.25))
    write_dxf(OUT / "lcd_rear_clamp_blank_rev_e.dxf", clamp)



def write_svg() -> None:
    s, x0, y0 = 1.72, 55, 112
    sx = lambda x: x0 + x * s
    sy = lambda y: y0 + (FASCIA_H - y) * s
    holes = "".join(
        f'<circle cx="{sx(x)}" cy="{sy(y)}" r="4" class="hold"/>'
        for x, y in ((9, 9), (205, 9), (401, 9), (9, 216), (205, 216), (401, 216))
    )
    switches = "".join(
        f'<circle cx="{sx(x)}" cy="{sy(STRIP_Y+23)}" r="13" fill="#b8bec2" stroke="#161b1f" stroke-width="2"/>'
        f'<line x1="{sx(x)-6}" y1="{sy(STRIP_Y+23)+6}" x2="{sx(x)+9}" y2="{sy(STRIP_Y+23)-9}" stroke="#111" stroke-width="6" stroke-linecap="round"/>'
        for x in SELECTOR_CENTRES
    )
    under_labels = "".join(
        f'<text x="{sx(x)}" y="{sy(STRIP_Y+5)}" text-anchor="middle" class="label">{label}</text>'
        for x, label in zip(SELECTOR_CENTRES, UNDER_LABELS)
    )
    hazard = (
        f'<circle cx="{sx(HAZARD_X)}" cy="{sy(STRIP_Y+23)}" r="10" fill="#b51e23" stroke="#161b1f" stroke-width="2"/>'
        f'<text x="{sx(HAZARD_X)}" y="{sy(STRIP_Y+5)}" text-anchor="middle" class="label">HAZARD</text>'
    )
    vents = "".join(
        f'<circle cx="{sx(x)}" cy="{sy(y)}" r="{VENT_FACE_RADIUS*s}" fill="url(#silver)" stroke="#6d7377" stroke-width="2"/>'
        f'<circle cx="{sx(x)}" cy="{sy(y)}" r="{26*s}" fill="#292e31" stroke="#101315" stroke-width="2"/>'
        f'<ellipse cx="{sx(x)}" cy="{sy(y)}" rx="{20*s}" ry="{8*s}" fill="#4a5155" stroke="#111" stroke-width="2"/>'
        for x, y in VENT_CENTRES
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="760" viewBox="0 0 1180 760">
<defs><linearGradient id="silver" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f5f5"/><stop offset="0.45" stop-color="#b8bec1"/><stop offset="1" stop-color="#72797d"/></linearGradient></defs>
<style>.cut{{fill:none;stroke:#111;stroke-width:2}}.hold{{fill:#fff4df;stroke:#a85f00;stroke-width:2;stroke-dasharray:7 5}}.txt{{font:15px Arial;fill:#20262b}}.bold{{font:700 18px Arial;fill:#20262b}}.small{{font:13px Arial;fill:#53606a}}.label{{font:700 8px Arial;fill:#20262b}}.dim{{stroke:#aa2020;stroke-width:1.5}}</style>
<rect width="1180" height="760" fill="#f7f8f9"/><text x="55" y="42" class="bold">J40 RHD CENTRE LCD / INTEGRATED A/C FASCIA - REV E</text><text x="55" y="68" class="small">One flat centre face over the deleted ashtray/radio zone. OEM glovebox and speedometer pressing remain unchanged.</text>
<rect x="{sx(0)}" y="{sy(FASCIA_H)}" width="{FASCIA_W*s}" height="{FASCIA_H*s}" rx="{CORNER_R*s}" fill="#e8e2cc" stroke="#111" stroke-width="2"/>
<rect x="{sx(VEHICLE_CUT_X)}" y="{sy(VEHICLE_CUT_Y+VEHICLE_CUT_H)}" width="{VEHICLE_CUT_W*s}" height="{VEHICLE_CUT_H*s}" rx="{VEHICLE_CUT_R*s}" fill="none" stroke="#aa2020" stroke-width="2" stroke-dasharray="10 6"/>
<rect x="{sx(BEZEL_X)}" y="{sy(BEZEL_Y+BEZEL_H)}" width="{BEZEL_W*s}" height="{BEZEL_H*s}" rx="7" fill="#11161a" stroke="#a85f00" stroke-width="2" stroke-dasharray="7 5"/>
<rect x="{sx(SCREEN_X)}" y="{sy(SCREEN_Y+SCREEN_H)}" width="{SCREEN_W*s}" height="{SCREEN_H*s}" rx="5" fill="#253846" stroke="#e8edf0" stroke-width="1"/>
<rect x="{sx(STRIP_X)}" y="{sy(STRIP_Y+STRIP_H)}" width="{STRIP_W*s}" height="{STRIP_H*s}" rx="6" fill="#e8e2cc" stroke="#111" stroke-width="2"/>{vents}{switches}{under_labels}{hazard}{holes}
<line x1="{sx(0)}" y1="{sy(0)+32}" x2="{sx(FASCIA_W)}" y2="{sy(0)+32}" class="dim"/><text x="{sx(150)}" y="{sy(0)+58}" class="bold">410 RELEASED OUTER BLANK</text>
<line x1="{sx(FASCIA_W)+20}" y1="{sy(FASCIA_H)}" x2="{sx(FASCIA_W)+20}" y2="{sy(0)}" class="dim"/><text x="{sx(FASCIA_W)+30}" y="{sy(105)}" class="bold">225</text>
<text x="{sx(112)}" y="{sy(139)}" fill="#fff" font-family="Arial" font-size="14">TRUE 9-INCH ACTIVE IMAGE 199.2 x 112.1 mm</text>
<text x="{sx(136)}" y="{sy(126)}" fill="#d7e0e5" font-family="Arial" font-size="11">202 x 115 aperture | 230 x 132 bezel envelope | HOLD</text>
<text x="{sx(112)}" y="{sy(214)}" fill="#8b1e1e" font-family="Arial" font-size="12" font-weight="700">PROPOSED DASH OPENING 374 x 189 - OWNER AUTHORISES CENTRE CUT</text>
<rect x="805" y="100" width="335" height="520" rx="8" fill="#fff" stroke="#cbd2d7"/><text x="828" y="135" class="bold">REV E SCOPE</text>
<text x="828" y="168" class="txt">Ashtray fully deleted; radio zone flattened.</text><text x="828" y="195" class="txt">One wider body-colour CNC fascia.</text><text x="828" y="222" class="txt">Glovebox and speedometer pressing untouched.</text><text x="828" y="245" class="small">Outer blank released; dash opening located by template.</text>
<text x="828" y="267" class="bold">INTEGRATED A/C OUTLETS</text><text x="828" y="300" class="txt">Two circular satin-silver directional vents.</text><text x="828" y="327" class="txt">Flush to +0.5 mm; hidden rear retention.</text><text x="828" y="354" class="txt">Face Ø70 MAX | cutout Ø66 REF.</text><text x="828" y="381" class="txt">Hose neck target Ø63.5 (2.5 inch).</text><text x="828" y="408" class="small">Both vent circles remain HOLD until measured.</text>
<text x="828" y="453" class="bold">CONTROLS</text><text x="828" y="485" class="txt">Under LCD: BLOWER | A/C | FUEL CONTROL</text><text x="828" y="512" class="txt">Separate red HAZARD at far right.</text><text x="828" y="539" class="small">Right of speedometer: WIPERS / LIGHTS</text><text x="828" y="562" class="small">over SPOTS / AUX in original 2 x 2 zone.</text>
<text x="55" y="695" class="small">Finish: low-gloss body-colour fascia; brushed/satin-silver vent bezels; black directional cores permitted.</text>
<text x="55" y="720" class="small">Black outer profile is released. Red dash-opening mark is fitted by template. HOLD_* LCD, selector, vent and mounting geometry awaits actual-part measurement.</text></svg>'''
    (OUT / "dashboard_lcd_hvac_fascia_rev_e_dimensioned_front.svg").write_text(svg, encoding="utf-8")


def draw_image_fit(c: canvas.Canvas, path: Path, x: float, y: float, max_w: float, max_h: float) -> None:
    if not path.exists():
        return
    img = ImageReader(str(path))
    iw, ih = img.getSize()
    scale = min(max_w / iw, max_h / ih)
    draw_w, draw_h = iw * scale, ih * scale
    c.drawImage(img, x + (max_w - draw_w) / 2, y + (max_h - draw_h) / 2, draw_w, draw_h, preserveAspectRatio=True)


def write_pdf() -> None:
    path = OUT / "j40_dashboard_lcd_hvac_fascia_rev_e_shop_spec.pdf"
    c = canvas.Canvas(str(path), pagesize=landscape(A3))
    w, h = landscape(A3)
    c.setTitle("J40 RHD Centre LCD Fascia Rev E")

    # Page 1: nominal front geometry and locked scope. The model is reduced to
    # fit beside the notes; every model-space dimension remains stated in mm.
    c.setFont("Helvetica-Bold", 18)
    c.drawString(16*mm, h-16*mm, "J40 RHD Centre 9-inch LCD / Integrated A/C Fascia - Rev E")
    c.setFont("Helvetica", 9)
    c.drawRightString(w-16*mm, h-16*mm, "Units mm | Quote + 1:1 prototype | Production geometry HOLD")
    x, y, ds = 14*mm, 33*mm, 0.67
    px = lambda value: x + value * ds * mm
    py = lambda value: y + value * ds * mm
    c.setFillColor(HexColor("#e8e2cc"))
    c.setStrokeColor(HexColor("#111111"))
    c.roundRect(x, y, FASCIA_W*ds*mm, FASCIA_H*ds*mm, CORNER_R*ds*mm, fill=1, stroke=1)
    c.setStrokeColor(HexColor("#aa2020"))
    c.setDash(6, 4)
    c.roundRect(
        px(VEHICLE_CUT_X), py(VEHICLE_CUT_Y), VEHICLE_CUT_W*ds*mm, VEHICLE_CUT_H*ds*mm,
        VEHICLE_CUT_R*ds*mm, fill=0, stroke=1,
    )
    c.setFillColor(HexColor("#11161a"))
    c.roundRect(px(BEZEL_X), py(BEZEL_Y), BEZEL_W*ds*mm, BEZEL_H*ds*mm, 3*ds*mm, fill=1, stroke=1)
    c.setDash()
    c.setFillColor(HexColor("#253846"))
    c.setStrokeColor(HexColor("#e8edf0"))
    c.roundRect(px(SCREEN_X), py(SCREEN_Y), SCREEN_W*ds*mm, SCREEN_H*ds*mm, 2*ds*mm, fill=1, stroke=1)
    c.setFillColor(HexColor("#e8e2cc"))
    c.setStrokeColor(HexColor("#111111"))
    c.roundRect(px(STRIP_X), py(STRIP_Y), STRIP_W*ds*mm, STRIP_H*ds*mm, 3*ds*mm, fill=1, stroke=1)
    for vent_x, vent_y in VENT_CENTRES:
        c.setFillColor(HexColor("#bfc4c7"))
        c.setStrokeColor(HexColor("#62696d"))
        c.circle(px(vent_x), py(vent_y), VENT_FACE_RADIUS*ds*mm, fill=1, stroke=1)
        c.setFillColor(HexColor("#292e31"))
        c.circle(px(vent_x), py(vent_y), 26*ds*mm, fill=1, stroke=1)
        c.setFillColor(HexColor("#555d61"))
        c.ellipse(px(vent_x)-20*ds*mm, py(vent_y)-7*ds*mm, px(vent_x)+20*ds*mm, py(vent_y)+7*ds*mm, fill=1, stroke=1)
    for hx, label in zip(SELECTOR_CENTRES, UNDER_LABELS):
        c.setFillColor(HexColor("#b8bec2"))
        c.circle(px(hx), py(STRIP_Y+23), 6*ds*mm, fill=1, stroke=1)
        c.setFillColor(HexColor("#20262b"))
        c.setFont("Helvetica-Bold", 4.4 if "FUEL" in label else 5.0)
        c.drawCentredString(px(hx), py(STRIP_Y+4.3), label)
    c.setFillColor(HexColor("#b51e23"))
    c.circle(px(HAZARD_X), py(STRIP_Y+23), 4.5*ds*mm, fill=1, stroke=1)
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 4.6)
    c.drawCentredString(px(HAZARD_X), py(STRIP_Y+4.3), "HAZARD")
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(px(FASCIA_W/2), py(137), "true 9-inch active image: 199.2 x 112.1 (228.6 diagonal)")
    c.setFont("Helvetica", 5.8)
    c.drawCentredString(px(FASCIA_W/2), py(125), "202 x 115 aperture | 230 x 132 bezel envelope | actual LCD drawing controls")
    c.setFillColor(HexColor("#8b1e1e"))
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(px(FASCIA_W/2), y+FASCIA_H*ds*mm+5*mm, "410 x 225 RELEASED FASCIA BLANK | PROPOSED DASH OPENING 374 x 189")

    nx, yy = 302*mm, h-34*mm
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(nx, yy, "FLAT-FACE / PRESERVATION SCOPE")
    c.setFont("Helvetica", 7.4)
    for row in [
        "Delete the complete ashtray: door, body, lip, seam and recess.",
        "Absorb the adjacent radio openings into one flat body-colour face.",
        "Preserve glovebox/instruction panel and speedometer pressing unchanged.",
        "Cut the fascia outer blank 410 x 225 x 1.5 CR4 with R6 corners.",
        "Owner authorises centre-dash cutting; proposed opening is 374 x 189.",
        "Locate the opening by 1:1 template clear of the two preserved pressings.",
    ]:
        yy -= 7*mm
        c.drawString(nx, yy, row)
    yy -= 5*mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(nx, yy, "INTEGRATED SILVER A/C OUTLETS")
    c.setFont("Helvetica", 7.4)
    for row in [
        "Two circular, directional outlets integrated in the lower fascia.",
        "Centre coordinates: (52,51) and (358,51) from local lower-left.",
        "Satin/brushed silver face Ø70 MAX; black directional core allowed.",
        "Visible face flush to +0.5 max; hidden rear retainer; no front screws.",
        "Reference neck cutout Ø66; target hose neck Ø63.5 / 2.5 inch.",
        "Face, cutout, retainer and rear depth remain HOLD until measured.",
    ]:
        yy -= 6.5*mm
        c.drawString(nx, yy, row)
    yy -= 5*mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(nx, yy, "EXACT SELECTOR POSITIONS")
    c.setFont("Helvetica", 7.4)
    for row in [
        "RIGHT OF SPEEDOMETER: WIPERS / LIGHTS over SPOTS / AUX.",
        "UNDER LCD: BLOWER | A/C REQUEST | FUEL STOP / CONTROL.",
        "Separate red HAZARD at far-right; indicators remain on OEM stalk.",
        "Black CUT_FASCIA_OUTER is released; red dash-opening mark is a template.",
        "HOLD_* part apertures wait for actual hardware; complete M1-M8.",
    ]:
        yy -= 6.5*mm
        c.drawString(nx, yy, row)
    c.setFillColor(HexColor("#8b1e1e"))
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(14*mm, 14*mm, "OUTER BLANK RELEASED. DASH CUT AUTHORISED AFTER TEMPLATE LOCATION; LCD, SELECTOR, VENT AND MOUNTING APERTURES REMAIN HOLD UNTIL ACTUAL PARTS ARE MEASURED.")
    c.showPage()

    # Page 2: both required owner photographs and their matching Rev E overlays.
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(16*mm, h-16*mm, "Paired actual-dashboard basis and Rev E visual intent")
    c.setFont("Helvetica", 9)
    c.drawRightString(w-16*mm, h-16*mm, "Photographs establish intent only - do not scale")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(15*mm, 262*mm, "ASSEMBLED DRIVER VIEW - OWNER PHOTO")
    c.drawString(215*mm, 262*mm, "ASSEMBLED DRIVER VIEW - REV E OVERLAY")
    draw_image_fit(c, ASSEMBLED_BASE_PHOTO, 15*mm, 165*mm, 190*mm, 88*mm)
    draw_image_fit(c, OUT / "dashboard_lcd_hvac_fascia_rev_e_photo_overlay_assembled.png", 215*mm, 165*mm, 190*mm, 88*mm)
    c.drawString(15*mm, 147*mm, "STRAIGHT-ON BARE-SHELL VIEW - OWNER PHOTO")
    c.drawString(215*mm, 147*mm, "STRAIGHT-ON BARE-SHELL VIEW - REV E OVERLAY")
    draw_image_fit(c, BARE_BASE_PHOTO, 15*mm, 50*mm, 190*mm, 88*mm)
    draw_image_fit(c, OUT / "dashboard_lcd_hvac_fascia_rev_e_photo_overlay_bare_shell.png", 215*mm, 50*mm, 190*mm, 88*mm)
    c.setFont("Helvetica", 7.6)
    c.drawString(15*mm, 38*mm, "Visual issue rule: every future revision must be checked on both owner views; neither view alone is approval to cut.")
    c.drawString(15*mm, 31*mm, "Preserve the OEM glovebox/instruction panel and speedometer pressing. Delete the ashtray and flatten the combined centre zone.")
    c.drawString(15*mm, 24*mm, "Rev E intent: two matched circular satin-silver outlets sit flush in the fascia; no hanging pod, black bracket or exposed front screw.")
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
        "M1 locate proposed 374 x 189 dash opening clear of preserved pressings; fascia outer blank is released 410 x 225 R6 | M2 actual LCD drawing | M3 LCD rear body/mount/depth",
        "M4 all seven selector bushes, anti-rotation and rear stacks | M5 transfer actual four right-cluster centres | M6 both vent faces/cutouts/retainers/necks/depth",
        "M7 signed 1:1 prototype: glovebox, instruments, steering, gear lever, sight line, wiring and duct sweeps | M8 labels, continuity, relay map and live function tests",
    ]:
        note_y -= 7*mm
        c.drawString(15*mm, note_y, row)
    c.setFillColor(HexColor("#8b1e1e"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(15*mm, 20*mm, "RELEASE: 410 x 225 R6 fascia outer blank may be cut. Centre-dash opening is authorised after M1 template placement; all actual-part apertures remain HOLD until measured.")
    c.setFillColor(HexColor("#53606a"))
    c.setFont("Helvetica", 6.7)
    c.drawString(15*mm, 13*mm, "Electrical basis: electrical_master.csv; electrical_diagram_reconciliation_20260518.csv; engine_electrical_inputs_reconciliation_20260517.csv; expenses.csv.")
    c.showPage()
    c.save()


def write_csvs() -> None:
    with (OUT / "fabricator_cut_list.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["part", "qty", "material", "thickness_mm", "finish", "file", "release"])
        w.writerows([
            ["wide centre flat-face fascia with integrated vent references", 1, "CR4 mild steel", 1.5, "body-colour low-gloss paint", "centre_fascia_template_rev_e.dxf", "CUT_FASCIA_OUTER 410 x 225 R6 RELEASED; MARK_PROPOSED_VEHICLE_CUT 374 x 189 located by fitted template; mounting, LCD, control-strip and both vent circles HOLD"],
            ["centre three-selector strip blank", 1, "5052-H32 aluminium", 2.0, "body-colour low-gloss paint", "centre_three_selector_strip_blank_rev_e.dxf", "outer/fasteners released; selector and hazard holes HOLD"],
            ["right-cluster four-selector transfer template", 1, "card/acrylic template", 2.0, "none", "right_cluster_four_selector_transfer_template_rev_e.dxf", "ALL GEOMETRY HOLD; transfer actual vehicle centres"],
            ["LCD rear clamp blank", 1, "5052-H32 aluminium", 2.0, "black", "lcd_rear_clamp_blank_rev_e.dxf", "outer/fasteners released; rear-body opening HOLD"],
        ])
    with (OUT / "measurement_and_release_schedule.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["id", "measurement", "nominal_or_intent", "required_evidence", "status"])
        w.writerows([
            ["M1", "locate the authorised centre-dash opening while protecting speedometer pressing and glovebox/instruction panel", "released fascia blank 410 x 225 R6; proposed vehicle opening 374 x 189; finished face has no ashtray feature", "1:1 fascia template fitted to vehicle plus front/rear ruler photos and signed opening line", "HOLD - opening location only"],
            ["M2", "LCD active area/aperture/bezel/rear body/mount/connectors", "9-inch 16:9 active 199.2 x 112.1; aperture 202 x 115; bezel envelope 230 x 132 reference", "actual LCD model drawing and caliper dimensions", "HOLD"],
            ["M3", "LCD rear body/mount centres/depth/connector sweep", "supplier-specific", "rear rubbing, depth gauge and plug trial", "HOLD"],
            ["M4", "seven Schneider selector bushes/anti-rotation/contact blocks", "22.3 mm nominal aperture", "measure each bought selector and rear stack", "HOLD"],
            ["M5", "four original right-cluster hole centres and rear clearance", "reuse 2 x 2 positions", "vehicle transfer template and rear photo", "HOLD"],
            ["M6", "both integrated vent faces, cutouts, retainers, neck OD and rear depth", "satin-silver circular face 70 mm maximum; 66 mm reference cutout; 63.5 mm hose-neck target; flush to +0.5 mm", "caliper measurement of both bought vents, rear-retainer installation trial, hose trial and duct sweep", "HOLD"],
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
    text = """# J40 RHD Centre 9-inch LCD / Integrated A/C Fascia - Rev E

Rev E uses both owner photographs as the visual basis. It replaces the complete ashtray/radio zone with one wider flat body-colour fascia carrying a true 9-inch LCD, three lower selectors, a separate hazard control and two flush circular satin-silver A/C outlets. The original glovebox/instruction panel and speedometer/instrument pressing remain unchanged.

## Owner-authorised cut-and-replace scope

- The centre dash may be cut as required. Delete the complete ashtray door, body, lip, seam and recess and absorb the radio openings into the same opening.
- Release the fascia outer blank at 410 x 225 x 1.5 mm CR4 mild steel with R6 corners (`CUT_FASCIA_OUTER`).
- Use the red 374 x 189 mm R3 line as the proposed vehicle opening. Locate that opening with the 1:1 fascia template before cutting so it clears the two protected OEM pressings.
- Preserve only the stated original features: glovebox/instruction panel and speedometer/instrument pressing. Do not drill, cover, distort or trim either one.
- Finish the fascia in low-gloss body colour, with a restrained black LCD bezel and satin/brushed silver outlet bezels.

## Nominal local geometry

Datum is the lower-left corner of the 410 x 225 fascia blank; all dimensions are millimetres.

| Feature | X | Y | Size / note |
|---|---:|---:|---|
| Proposed vehicle opening | 18 | 18 | 374 x 189, R3; locate by fitted template |
| LCD bezel envelope | 90 | 72 | 230 x 132; HOLD to actual LCD |
| LCD aperture | 104 | 80.5 | 202 x 115; HOLD to actual LCD |
| Lower control strip | 90 | 20 | 230 x 40 |
| Left silver outlet centre | 52 | 51 | face Ø70 max; cutout Ø66 reference |
| Right silver outlet centre | 358 | 51 | face Ø70 max; cutout Ø66 reference |
| Lower selector centres | 120 / 185 / 250 | 43 | BLOWER / A/C REQUEST / FUEL CONTROL |
| Hazard centre | 300 | 43 | separate red control |

The 9-inch reference is a 199.2 x 112.1 mm 16:9 active image, 228.6 mm diagonal. The actual LCD manufacturer's mechanical drawing controls the bezel, aperture, rear body, mount and connector clearances.

## Integrated A/C outlets

- Use two matched circular directional outlets with satin/brushed silver face bezels. A black directional core is acceptable.
- Visible face diameter is Ø70 mm maximum. Installed face must be flush to +0.5 mm maximum relative to the fascia.
- Use the bought vent's hidden rear nut, spring ring or clamp. No exposed front screws, pods or hanging brackets.
- Target a Ø63.5 mm / 2.5-inch hose neck. The nominal DXF shows `HOLD_VENT_FACE_ENVELOPE` Ø70 and `HOLD_VENT_NECK_CUTOUT` Ø66.
- Do not production-cut the vent apertures until both bought vents have been measured for face, cutout, retainer, neck OD and rear depth and trialled with the actual hose.

## Exact control positions

All positions are viewed from the cabin.

Right of the speedometer, original 2 x 2 zone:

- Upper-left: WIPERS — 3-position, OFF / LOW / HIGH.
- Upper-right: LIGHTS — 3-position, OFF / SIDE / HEAD.
- Lower-left: SPOTS — 2-position, OFF / ON; relay T5.
- Lower-right: AUX — 2-position, OFF / ON; B2 auxiliary control.

Under the LCD, left to right:

- BLOWER — 3-position, OFF / LOW / HIGH.
- A/C REQUEST — 2-position, OFF / ON.
- FUEL STOP / CONTROL — 2-position, provisional pending device and live shutdown proof.
- Separate red HAZARD at far right; not one of the seven selectors.

Indicators remain on the OEM stalk.

## Electrical rules

- Every selector commands a fused relay/control circuit; no selector directly carries a high-current lamp, blower, clutch or accessory load.
- Frozen relay baseline: T1 low beam, T2 high beam, T3 horn, T4 condenser fan, T5 spot lamps, B1 A/C clutch and B2 auxiliary accessory.
- BLOWER uses a dedicated measured HVAC control/relay/resistor circuit. T1 and T2 remain lighting relays.
- A/C REQUEST may energise B1 only through the thermostat / trinary / pressure-protection chain. Prove T4 condenser-fan behaviour with the final HVAC hardware.
- FUEL STOP / CONTROL remains HOLD until the actual device and terminals are identified and key-OFF shutdown is proved with the engine running. Retain the manual stop cable.

Evidence basis: `data/manual/workbook_tabs/electrical_master.csv`, `data/manual/reference_projects_and_ideas.csv`, `data/manual/expenses.csv`, `data/manual/electrical_diagram_reconciliation_20260518.csv` and `data/manual/engine_electrical_inputs_reconciliation_20260517.csv`.

## CNC release rules

- `CUT_FASCIA_OUTER` is released for the 410 x 225 R6 outer blank.
- `MARK_PROPOSED_VEHICLE_CUT` is a 1:1 placement/cut template. The owner authorises the centre cut, but template location must keep the glovebox and speedometer pressing intact.
- Every layer beginning `HOLD_` is reference geometry, not a production toolpath.
- Measure the actual LCD, all seven selector bushes and rear stacks, the hazard control, both vents and hose before releasing their apertures.
- Transfer the four existing right-cluster centres from the vehicle; do not drill them from nominal artwork.
- Trial-fit a 1:1 card/acrylic or cheap-sheet prototype with all actual parts. Prove glovebox operation, instrument rigidity, driver sight line, steering/gear-lever clearance, rear stacks, wiring and duct sweeps.
- Cut the vehicle opening slightly undersize, trim progressively, deburr/radius all edges and epoxy-prime exposed steel before paint.

## Paired-view visual issue rule

Every design revision must be applied to and checked on both owner images:

1. assembled driver view, showing the right-hand-drive steering relationship; and
2. straight-on bare-shell view, showing the complete fascia, glovebox and speedometer boundaries.

The images establish appearance and placement intent only; do not scale them for CNC work.

## Acceptance

- Complete ashtray removal and one flat ashtray/radio replacement face.
- Actual LCD proves a true 9-inch active area and fits its released aperture and clamp.
- Glovebox/instruction panel and speedometer/instrument pressing remain visually and structurally unchanged.
- Two matched silver circular directional outlets read as integrated dashboard features, sit flush to +0.5 mm, and have no exposed bracket or front screw.
- Screen, lower control strip and both vents remain independently service-removable from the cabin side.
- All seven selector assignments match `switch_position_schedule.csv`.
- Wiring continuity, A/C safety logic, blower load, lighting logic, fuel-stop shutdown, vent flow and vibration/rattle tests pass.

## Package contents

- `j40_dashboard_lcd_hvac_fascia_rev_e_shop_spec.pdf` — three-page CNC/shop brief with both owner-photo pairs, geometry, selector schedule and release gates.
- `dashboard_lcd_hvac_fascia_rev_e_dimensioned_front.svg` — dimensioned front layout.
- `dashboard_lcd_hvac_fascia_rev_e_photo_overlay_assembled.png` and `..._bare_shell.png` — paired Rev E visualisations; do not scale.
- Four Rev E DXFs — fascia, lower selector strip, right-cluster transfer template and LCD rear clamp.
- `fabricator_cut_list.csv`, `measurement_and_release_schedule.csv` and `switch_position_schedule.csv` — release controls.

Ready to send for CNC quotation. The fascia outer blank is released. The centre-dash cut is owner-authorised after 1:1 template placement; actual-part apertures remain HOLD until M1-M8 evidence is completed.
"""
    (OUT / "README.md").write_text(text, encoding="utf-8")

def package() -> None:
    DELIVERABLE.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DELIVERABLE, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.iterdir()):
            z.write(p, f"dashboard_lcd_hvac_fascia_rev_e/{p.name}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if CONCEPT_ASSEMBLED_SOURCE.exists():
        shutil.copy2(
            CONCEPT_ASSEMBLED_SOURCE,
            OUT / "dashboard_lcd_hvac_fascia_rev_e_photo_overlay_assembled.png",
        )
    if CONCEPT_BARE_SOURCE.exists():
        shutil.copy2(
            CONCEPT_BARE_SOURCE,
            OUT / "dashboard_lcd_hvac_fascia_rev_e_photo_overlay_bare_shell.png",
        )
    make_dxfs(); write_svg(); write_csvs(); write_readme(); write_pdf(); package()
    print(OUT); print(DELIVERABLE)


if __name__ == "__main__":
    main()
