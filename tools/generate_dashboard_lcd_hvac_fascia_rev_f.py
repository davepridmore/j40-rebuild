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
OUT = ROOT / "data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_f"
DELIVERABLE = ROOT / "deliverables/fabrication_packages/dashboard_lcd_hvac_fascia_rev_f.zip"
CONCEPT_ASSEMBLED_SOURCE = Path(
    "/Users/davidpridmore/.codex/generated_images/019fb8d3-8269-7eb0-b457-d806a3cefbd4/exec-a3ab1aa3-1636-495e-a24e-34dc1394748a.png"
)
CONCEPT_BARE_SOURCE = Path(
    "/Users/davidpridmore/.codex/generated_images/019fb8d3-8269-7eb0-b457-d806a3cefbd4/exec-823ec583-d11d-404e-98c7-efccc7d0bba3.png"
)
ASSEMBLED_BASE_PHOTO = ROOT / "photos/20260317_165113.jpg"
BARE_BASE_PHOTO = ROOT / "photos/20260413_040719.jpg"

# Released rectangular fascia blank. The owner authorises cutting the centre dash
# as required, while the original speedometer pressing and glovebox remain protected.
FASCIA_W = 410.0
FASCIA_H = 148.0
CORNER_R = 6.0
VEHICLE_CUT_X, VEHICLE_CUT_Y = 18.0, 12.0
VEHICLE_CUT_W, VEHICLE_CUT_H = 374.0, 124.0
VEHICLE_CUT_R = 3.0
# A nominal 9-inch 16:9 active image is 199.2 x 112.1 mm. The final aperture,
# outer bezel and rear body are controlled by the actual LCD manufacturer's drawing.
LCD_ACTIVE_W, LCD_ACTIVE_H = 199.2, 112.1
BEZEL_X, BEZEL_Y, BEZEL_W, BEZEL_H = 96.0, 10.0, 218.0, 128.0
SCREEN_X, SCREEN_Y, SCREEN_W, SCREEN_H = 104.0, 16.5, 202.0, 115.0
SELECTOR_RADIUS = 11.15
VENT_CENTRES = ((49.0, 74.0), (361.0, 74.0))
VENT_FACE_RADIUS = 41.0
VENT_CORE_RADIUS = 31.0
VENT_CUTOUT_RADIUS = 33.0
VENT_HOSE_TARGET_DIAMETER = 63.5
RIGHT_BANK_W, RIGHT_BANK_H = 190.0, 88.0
RIGHT_BANK_XS = (24.0, 71.0, 118.0, 165.0)
RIGHT_BANK_YS = (64.0, 24.0)
RIGHT_BANK_MAP = (
    ("R1-C1", "WIPERS", "3-position", "OFF / LOW / HIGH"),
    ("R1-C2", "LIGHTS", "3-position", "OFF / SIDE / HEAD"),
    ("R1-C3", "SPOTS", "2-position", "OFF / ON"),
    ("R1-C4", "AUX", "2-position", "OFF / ON"),
    ("R2-C1", "BLOWER", "3-position", "OFF / LOW / HIGH"),
    ("R2-C2", "A/C", "2-position", "OFF / ON"),
    ("R2-C3", "FUEL STOP", "2-position", "RUN / STOP"),
    ("R2-C4", "HAZARD", "pushbutton", "OFF / FLASH"),
)


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
            "HOLD_VEHICLE_OPENING",
            rounded_rect_points(VEHICLE_CUT_X, VEHICLE_CUT_Y, VEHICLE_CUT_W, VEHICLE_CUT_H, VEHICLE_CUT_R),
        )
    )
    fascia.append(dxf_lwpoly("HOLD_LCD_BEZEL_ENVELOPE", rounded_rect_points(BEZEL_X, BEZEL_Y, BEZEL_W, BEZEL_H, 3)))
    fascia.append(dxf_lwpoly("HOLD_LCD_APERTURE", rounded_rect_points(SCREEN_X, SCREEN_Y, SCREEN_W, SCREEN_H, 3)))
    for vent_x, vent_y in VENT_CENTRES:
        fascia.append(dxf_circle("HOLD_VENT_FACE_ENVELOPE", vent_x, vent_y, VENT_FACE_RADIUS))
        fascia.append(dxf_circle("HOLD_VENT_NECK_CUTOUT", vent_x, vent_y, VENT_CUTOUT_RADIUS))
        fascia.append(dxf_line("HOLD_CENTRELINES", vent_x - 5, vent_y, vent_x + 5, vent_y))
        fascia.append(dxf_line("HOLD_CENTRELINES", vent_x, vent_y - 5, vent_x, vent_y + 5))
    for x, y in ((9, 9), (205, 9), (401, 9), (9, 139), (205, 139), (401, 139)):
        fascia.append(dxf_circle("HOLD_MOUNTING_HOLES", x, y, 2.25))
    write_dxf(OUT / "centre_fascia_template_rev_f.dxf", fascia)

    right = [dxf_lwpoly("HOLD_CONTROL_BANK_OUTER", rounded_rect_points(0, 0, RIGHT_BANK_W, RIGHT_BANK_H, 3))]
    for index, ((_, label, _, _), x, y) in enumerate(
        zip(RIGHT_BANK_MAP, RIGHT_BANK_XS + RIGHT_BANK_XS, (RIGHT_BANK_YS[0],) * 4 + (RIGHT_BANK_YS[1],) * 4)
    ):
        radius = 8.0 if label == "HAZARD" else SELECTOR_RADIUS
        layer = "HOLD_HAZARD_APERTURE" if label == "HAZARD" else "HOLD_SELECTOR_APERTURES"
        right.append(dxf_circle(layer, x, y, radius))
        right.append(dxf_line("HOLD_CENTRELINES", x - 4, y, x + 4, y))
        right.append(dxf_line("HOLD_CENTRELINES", x, y - 4, x, y + 4))
        label_y = 45.0 if index < 4 else 5.5
        right.append(dxf_text("HOLD_ENGRAVE_LABELS", x, label_y, 3.0, label))
    write_dxf(OUT / "right_control_bank_eight_position_template_rev_f.dxf", right)

    outer_vents = []
    for offset, mark in ((0.0, "OUTER LEFT"), (120.0, "OUTER RIGHT")):
        outer_vents.append(dxf_lwpoly("CUT_TEMPLATE_OUTER", rounded_rect_points(offset, 0, 100, 100, 3)))
        outer_vents.append(dxf_circle("HOLD_VENT_FACE_ENVELOPE", offset + 50, 50, VENT_FACE_RADIUS))
        outer_vents.append(dxf_circle("HOLD_VENT_NECK_CUTOUT", offset + 50, 50, VENT_CUTOUT_RADIUS))
        outer_vents.append(dxf_line("HOLD_CENTRELINES", offset + 45, 50, offset + 55, 50))
        outer_vents.append(dxf_line("HOLD_CENTRELINES", offset + 50, 45, offset + 50, 55))
        outer_vents.append(dxf_text("MARK_TEMPLATE_ID", offset + 50, 5.5, 3.0, mark))
    write_dxf(OUT / "outer_dash_vent_pair_transfer_template_rev_f.dxf", outer_vents)

    clamp = [
        dxf_lwpoly("HOLD_CLAMP_OUTER", rounded_rect_points(0, 0, 238, 140, 3)),
        dxf_lwpoly("HOLD_LCD_REAR_BODY", rounded_rect_points(5, 5, 228, 130, 2)),
    ]
    for x, y in ((6, 6), (232, 6), (6, 134), (232, 134)):
        clamp.append(dxf_circle("HOLD_CLAMP_MOUNTS", x, y, 2.25))
    write_dxf(OUT / "lcd_rear_clamp_blank_rev_f.dxf", clamp)



def write_svg() -> None:
    s, x0, y0 = 1.55, 55.0, 100.0
    sx = lambda x: x0 + x * s
    sy = lambda y: y0 + (FASCIA_H - y) * s
    holes = "".join(
        f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="3.5" class="hold"/>'
        for x, y in ((9, 9), (205, 9), (401, 9), (9, 139), (205, 139), (401, 139))
    )
    vents = "".join(
        f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="{VENT_FACE_RADIUS*s:.1f}" fill="url(#silver)" stroke="#62696d" stroke-width="2"/>'
        f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="{VENT_CORE_RADIUS*s:.1f}" fill="#292e31" stroke="#101315" stroke-width="2"/>'
        f'<ellipse cx="{sx(x):.1f}" cy="{sy(y):.1f}" rx="{24*s:.1f}" ry="{9.5*s:.1f}" fill="#51595d" stroke="#111" stroke-width="2"/>'
        for x, y in VENT_CENTRES
    )

    bs, bx0, by0 = 2.45, 55.0, 438.0
    bsx = lambda x: bx0 + x * bs
    bsy = lambda y: by0 + (RIGHT_BANK_H - y) * bs
    bank_controls: list[str] = []
    positions = list(zip(RIGHT_BANK_XS + RIGHT_BANK_XS, (RIGHT_BANK_YS[0],) * 4 + (RIGHT_BANK_YS[1],) * 4))
    for index, ((_, label, _, _), (cx, cy)) in enumerate(zip(RIGHT_BANK_MAP, positions)):
        radius = 8.0 if label == "HAZARD" else SELECTOR_RADIUS
        fill = "#b51e23" if label == "HAZARD" else "url(#silver)"
        bank_controls.append(
            f'<circle cx="{bsx(cx):.1f}" cy="{bsy(cy):.1f}" r="{radius*bs:.1f}" fill="{fill}" stroke="#161b1f" stroke-width="2"/>'
        )
        if label != "HAZARD":
            bank_controls.append(
                f'<line x1="{bsx(cx)-7:.1f}" y1="{bsy(cy)+7:.1f}" x2="{bsx(cx)+10:.1f}" y2="{bsy(cy)-10:.1f}" stroke="#111" stroke-width="7" stroke-linecap="round"/>'
            )
        label_y = 45.0 if index < 4 else 5.5
        bank_controls.append(
            f'<text x="{bsx(cx):.1f}" y="{bsy(label_y):.1f}" text-anchor="middle" class="banklabel">{label}</text>'
        )
    bank_controls_svg = "".join(bank_controls)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="760" viewBox="0 0 1180 760">
<defs><linearGradient id="silver" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f5f5"/><stop offset="0.45" stop-color="#b8bec1"/><stop offset="1" stop-color="#72797d"/></linearGradient></defs>
<style>.hold{{fill:none;stroke:#a85f00;stroke-width:2;stroke-dasharray:7 5}}.txt{{font:15px Arial;fill:#20262b}}.bold{{font:700 18px Arial;fill:#20262b}}.small{{font:13px Arial;fill:#53606a}}.banklabel{{font:700 10px Arial;fill:#20262b}}.dim{{stroke:#aa2020;stroke-width:1.5}}</style>
<rect width="1180" height="760" fill="#f7f8f9"/>
<text x="55" y="40" class="bold">J40 RHD COMPACT 9-INCH LCD / FOUR-OUTLET DASH - REV F</text>
<text x="55" y="66" class="small">Centre fascia carries only LCD + two outlets. All seven selectors and the separate hazard control form one bank right of the speedometer.</text>

<rect x="{sx(0):.1f}" y="{sy(FASCIA_H):.1f}" width="{FASCIA_W*s:.1f}" height="{FASCIA_H*s:.1f}" rx="{CORNER_R*s:.1f}" fill="#e8e2cc" stroke="#111" stroke-width="2"/>
<rect x="{sx(VEHICLE_CUT_X):.1f}" y="{sy(VEHICLE_CUT_Y+VEHICLE_CUT_H):.1f}" width="{VEHICLE_CUT_W*s:.1f}" height="{VEHICLE_CUT_H*s:.1f}" rx="{VEHICLE_CUT_R*s:.1f}" fill="none" stroke="#aa2020" stroke-width="2" stroke-dasharray="10 6"/>
<rect x="{sx(BEZEL_X):.1f}" y="{sy(BEZEL_Y+BEZEL_H):.1f}" width="{BEZEL_W*s:.1f}" height="{BEZEL_H*s:.1f}" rx="7" fill="#11161a" stroke="#a85f00" stroke-width="2" stroke-dasharray="7 5"/>
<rect x="{sx(SCREEN_X):.1f}" y="{sy(SCREEN_Y+SCREEN_H):.1f}" width="{SCREEN_W*s:.1f}" height="{SCREEN_H*s:.1f}" rx="5" fill="#253846" stroke="#e8edf0" stroke-width="1"/>
{vents}{holes}
<text x="{sx(FASCIA_W/2):.1f}" y="{sy(76):.1f}" text-anchor="middle" fill="#fff" font-family="Arial" font-size="13" font-weight="700">TRUE 9-INCH LCD</text>
<text x="{sx(FASCIA_W/2):.1f}" y="{sy(63):.1f}" text-anchor="middle" fill="#d7e0e5" font-family="Arial" font-size="10">active 199.2 x 112.1 | aperture 202 x 115 HOLD</text>
<text x="{sx(49):.1f}" y="{sy(17):.1f}" text-anchor="middle" class="banklabel">OUTLET 2 / 4</text>
<text x="{sx(361):.1f}" y="{sy(17):.1f}" text-anchor="middle" class="banklabel">OUTLET 3 / 4</text>
<line x1="{sx(0):.1f}" y1="{sy(0)+25:.1f}" x2="{sx(FASCIA_W):.1f}" y2="{sy(0)+25:.1f}" class="dim"/>
<text x="{sx(FASCIA_W/2):.1f}" y="{sy(0)+47:.1f}" text-anchor="middle" class="bold">410 mm RELEASED OUTER BLANK</text>
<line x1="{sx(FASCIA_W)+18:.1f}" y1="{sy(FASCIA_H):.1f}" x2="{sx(FASCIA_W)+18:.1f}" y2="{sy(0):.1f}" class="dim"/>
<text x="{sx(FASCIA_W)+28:.1f}" y="{sy(69):.1f}" class="bold">148</text>

<text x="55" y="418" class="bold">RIGHT-OF-SPEEDOMETER CONTROL BANK - 190 x 88 mm REFERENCE ENVELOPE</text>
<rect x="{bsx(0):.1f}" y="{bsy(RIGHT_BANK_H):.1f}" width="{RIGHT_BANK_W*bs:.1f}" height="{RIGHT_BANK_H*bs:.1f}" rx="8" fill="#e8e2cc" stroke="#111" stroke-width="2"/>
{bank_controls_svg}
<text x="55" y="690" class="small">Top L→R: WIPERS / LIGHTS / SPOTS / AUX. Bottom L→R: BLOWER / A/C / FUEL STOP / HAZARD.</text>
<text x="55" y="715" class="small">Engrave every label 3 mm high with black infill. Switch/hazard apertures and final vehicle position remain HOLD to actual parts and 1:1 trial.</text>

<rect x="735" y="92" width="405" height="625" rx="8" fill="#fff" stroke="#cbd2d7"/>
<text x="758" y="128" class="bold">COMPACT PRESERVATION SCOPE</text>
<text x="758" y="158" class="txt">Delete ashtray and flatten only the centre zone.</text>
<text x="758" y="183" class="txt">Keep original speedometer pressing and glovebox.</text>
<text x="758" y="208" class="txt">No control strip below the LCD.</text>
<text x="758" y="233" class="small">148 mm high: 77 mm / 34% shallower than Rev E.</text>

<text x="758" y="273" class="bold">FOUR INTEGRATED SILVER OUTLETS</text>
<text x="758" y="303" class="txt">1: far passenger-side dash end</text>
<text x="758" y="328" class="txt">2 + 3: flanking the LCD in this fascia</text>
<text x="758" y="353" class="txt">4: far driver-side dash end</text>
<text x="758" y="380" class="small">Each face Ø82 MAX | rear cut Ø66 REF</text>
<text x="758" y="403" class="small">Hose-neck target Ø63.5 / 2.5 inch</text>
<text x="758" y="426" class="small">Flush face; hidden rear retainer; no front screws.</text>

<text x="758" y="466" class="bold">WHAT THE SEVEN SELECTORS DO</text>
<text x="758" y="494" class="small">WIPERS: park / low / high.</text>
<text x="758" y="517" class="small">LIGHTS: off / sidelights / headlamps.</text>
<text x="758" y="540" class="small">SPOTS: energises spot-lamp relay T5.</text>
<text x="758" y="563" class="small">AUX: reserved accessory relay B2.</text>
<text x="758" y="586" class="small">BLOWER: cabin fan off / low / high.</text>
<text x="758" y="609" class="small">A/C: compressor request through safety chain.</text>
<text x="758" y="632" class="small">FUEL STOP: run / stop intent; live test required.</text>
<text x="758" y="655" class="small">HAZARD: separate red control; flashes all indicators.</text>
<text x="758" y="693" class="small">Only CUT_FASCIA_OUTER is released. All HOLD_ geometry</text>
<text x="758" y="711" class="small">must be replaced from measured parts/templates before cutting.</text>
</svg>'''
    (OUT / "dashboard_lcd_hvac_fascia_rev_f_dimensioned_front.svg").write_text(svg, encoding="utf-8")


def draw_image_fit(c: canvas.Canvas, path: Path, x: float, y: float, max_w: float, max_h: float) -> None:
    if not path.exists():
        return
    img = ImageReader(str(path))
    iw, ih = img.getSize()
    scale = min(max_w / iw, max_h / ih)
    draw_w, draw_h = iw * scale, ih * scale
    c.drawImage(img, x + (max_w - draw_w) / 2, y + (max_h - draw_h) / 2, draw_w, draw_h, preserveAspectRatio=True)


def write_pdf() -> None:
    path = OUT / "j40_dashboard_lcd_hvac_fascia_rev_f_shop_spec.pdf"
    c = canvas.Canvas(str(path), pagesize=landscape(A3))
    w, h = landscape(A3)
    c.setTitle("J40 RHD Compact Dashboard Rev F")

    def draw_note_block(x_pos: float, y_pos: float, heading: str, rows: list[str]) -> float:
        c.setFillColor(HexColor("#20262b"))
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(x_pos, y_pos, heading)
        c.setFont("Helvetica", 7.2)
        for row in rows:
            y_pos -= 5.8*mm
            c.drawString(x_pos, y_pos, row)
        return y_pos - 5*mm

    # Page 1: compact centre fascia, separate consolidated right bank, and release scope.
    c.setFont("Helvetica-Bold", 18)
    c.drawString(16*mm, h-16*mm, "J40 RHD Compact 9-inch LCD / Four-outlet Dashboard - Rev F")
    c.setFont("Helvetica", 8.5)
    c.drawRightString(w-16*mm, h-16*mm, "Units mm | Quotation + 1:1 prototype issue | actual-part geometry HOLD")

    x, y, ds = 14*mm, 119*mm, 0.60
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
    c.setDash()
    c.setFillColor(HexColor("#11161a"))
    c.setStrokeColor(HexColor("#a85f00"))
    c.roundRect(px(BEZEL_X), py(BEZEL_Y), BEZEL_W*ds*mm, BEZEL_H*ds*mm, 3*ds*mm, fill=1, stroke=1)
    c.setFillColor(HexColor("#253846"))
    c.setStrokeColor(HexColor("#e8edf0"))
    c.roundRect(px(SCREEN_X), py(SCREEN_Y), SCREEN_W*ds*mm, SCREEN_H*ds*mm, 2*ds*mm, fill=1, stroke=1)
    for vent_x, vent_y in VENT_CENTRES:
        c.setFillColor(HexColor("#bfc4c7"))
        c.setStrokeColor(HexColor("#62696d"))
        c.circle(px(vent_x), py(vent_y), VENT_FACE_RADIUS*ds*mm, fill=1, stroke=1)
        c.setFillColor(HexColor("#292e31"))
        c.circle(px(vent_x), py(vent_y), VENT_CORE_RADIUS*ds*mm, fill=1, stroke=1)
        c.setFillColor(HexColor("#555d61"))
        c.ellipse(
            px(vent_x)-23*ds*mm, py(vent_y)-8*ds*mm,
            px(vent_x)+23*ds*mm, py(vent_y)+8*ds*mm,
            fill=1, stroke=1,
        )
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(px(FASCIA_W/2), py(75), "TRUE 9-INCH LCD - ACTIVE 199.2 x 112.1")
    c.setFont("Helvetica", 5.8)
    c.drawCentredString(px(FASCIA_W/2), py(63), "202 x 115 aperture | 218 x 128 bezel envelope | HOLD to actual screen")
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(px(FASCIA_W/2), y+FASCIA_H*ds*mm+5*mm, "CENTRE FASCIA 410 x 148 R6 - 77 mm / 34% SHALLOWER THAN REV E")
    c.setFillColor(HexColor("#8b1e1e"))
    c.setFont("Helvetica", 6.4)
    c.drawCentredString(px(FASCIA_W/2), y-6*mm, "Dashed 374 x 124 line = HOLD vehicle-opening envelope behind fascia; it is NOT a fascia toolpath")

    # Consolidated 4 x 2 bank, shown larger than the centre fascia for legibility.
    bx, by, bds = 20*mm, 22*mm, 1.05
    bpx = lambda value: bx + value * bds * mm
    bpy = lambda value: by + value * bds * mm
    c.setFillColor(HexColor("#e8e2cc"))
    c.setStrokeColor(HexColor("#111111"))
    c.roundRect(bx, by, RIGHT_BANK_W*bds*mm, RIGHT_BANK_H*bds*mm, 3*bds*mm, fill=1, stroke=1)
    positions = list(zip(RIGHT_BANK_XS + RIGHT_BANK_XS, (RIGHT_BANK_YS[0],) * 4 + (RIGHT_BANK_YS[1],) * 4))
    for index, ((_, label, _, _), (control_x, control_y)) in enumerate(zip(RIGHT_BANK_MAP, positions)):
        radius = 8.0 if label == "HAZARD" else SELECTOR_RADIUS
        c.setFillColor(HexColor("#b51e23") if label == "HAZARD" else HexColor("#b8bec2"))
        c.circle(bpx(control_x), bpy(control_y), radius*bds*mm, fill=1, stroke=1)
        label_y = 45.0 if index < 4 else 5.5
        c.setFillColor(HexColor("#20262b"))
        c.setFont("Helvetica-Bold", 6.5)
        c.drawCentredString(bpx(control_x), bpy(label_y)-1.5*mm, label)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(bx, by+RIGHT_BANK_H*bds*mm+5*mm, "ALL CONTROLS RIGHT OF SPEEDOMETER - 190 x 88 REFERENCE ENVELOPE")
    c.setFont("Helvetica", 6.6)
    c.drawString(bx, by-6*mm, "Top: WIPERS | LIGHTS | SPOTS | AUX     Bottom: BLOWER | A/C | FUEL STOP | HAZARD")

    nx, yy = 273*mm, h-34*mm
    yy = draw_note_block(nx, yy, "PRESERVATION / PACKAGING", [
        "Delete the ashtray and flatten the centre radio/ashtray zone.",
        "Preserve glovebox/instruction panel and speedometer pressing.",
        "Centre fascia carries screen + two vents only; no lower extension.",
        "Fit all seven selectors + hazard in the bank shown at right.",
    ])
    yy = draw_note_block(nx, yy, "FOUR INTEGRATED DASH OUTLETS", [
        "Outlet 1: far passenger-side dash end, located by template.",
        "Outlets 2/3: centre fascia at (49,74) and (361,74).",
        "Outlet 4: far driver-side dash end, located by template.",
        "All four: satin-silver directional face, Ø82 MAX.",
        "Reference rear cut Ø66; target neck Ø63.5 / 2.5 inch.",
        "Flush face +0.5 max; hidden rear retainer; no front screws.",
    ])
    yy = draw_note_block(nx, yy, "GEOMETRY CHECK", [
        "Centre faces have 8 mm side margin and 6 mm bezel gap.",
        "Ø66 cut-to-bezel ligament is 14 mm; LCD top/bottom land 10 mm.",
        "Right bank pitch: 47 horizontal / 40 vertical; min land 12.85.",
        "Final dash opening needs vent-neck relief proved by duct mock-up.",
    ])
    draw_note_block(nx, yy, "RELEASE STATUS", [
        "CUT_FASCIA_OUTER 410 x 148 R6 is the only metal cut released.",
        "HOLD_* layers are references, never production toolpaths.",
        "Right bank, outer vents, LCD and all holes await measured parts.",
        "Quote complete package now; production release follows M1-M9.",
    ])
    c.setFillColor(HexColor("#8b1e1e"))
    c.setFont("Helvetica-Bold", 7.8)
    c.drawString(14*mm, 8*mm, "DO NOT CUT THE VEHICLE OR ANY HOLD_* APERTURE FROM THIS NOMINAL DRAWING. FIT THE 1:1 TEMPLATE AND ACTUAL PARTS FIRST.")
    c.showPage()

    # Page 2: both required owner photographs and their matching final visualisations.
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(16*mm, h-16*mm, "Paired original-dashboard basis and Rev F visual intent")
    c.setFont("Helvetica", 9)
    c.drawRightString(w-16*mm, h-16*mm, "Photographs establish intent only - do not scale")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(15*mm, 262*mm, "ASSEMBLED DRIVER VIEW - OWNER PHOTO")
    c.drawString(215*mm, 262*mm, "ASSEMBLED DRIVER VIEW - REV F OVERLAY")
    draw_image_fit(c, ASSEMBLED_BASE_PHOTO, 15*mm, 165*mm, 190*mm, 88*mm)
    draw_image_fit(c, OUT / "dashboard_lcd_hvac_fascia_rev_f_photo_overlay_assembled.png", 215*mm, 165*mm, 190*mm, 88*mm)
    c.drawString(15*mm, 147*mm, "STRAIGHT-ON BARE-SHELL VIEW - OWNER PHOTO")
    c.drawString(215*mm, 147*mm, "STRAIGHT-ON BARE-SHELL VIEW - REV F OVERLAY")
    draw_image_fit(c, BARE_BASE_PHOTO, 15*mm, 50*mm, 190*mm, 88*mm)
    draw_image_fit(c, OUT / "dashboard_lcd_hvac_fascia_rev_f_photo_overlay_bare_shell.png", 215*mm, 50*mm, 190*mm, 88*mm)
    c.setFont("Helvetica", 7.6)
    c.drawString(15*mm, 38*mm, "Visual rule: every revision is checked on both owner photographs; neither image is dimensional approval to cut.")
    c.drawString(15*mm, 31*mm, "Four matching Ø82 silver outlets: one at each dash end plus two flanking the LCD. Preserve glovebox and speedometer pressing.")
    c.drawString(15*mm, 24*mm, "All seven selectors are consolidated in the labelled 4 x 2 bank right of the speedometer; red hazard occupies the eighth position.")
    c.showPage()

    # Page 3: complete control mapping, electrical constraints and production gates.
    c.setFont("Helvetica-Bold", 18)
    c.drawString(16*mm, h-16*mm, "Right-bank control schedule, electrical constraints and production gates")
    c.setFont("Helvetica", 9)
    c.drawRightString(w-16*mm, h-16*mm, "Seven bought selectors + separate red hazard | relay/control-current switching only")
    left = 15*mm
    top = h-34*mm
    col_widths = [22, 29, 22, 28, 34, 65, 72, 106]
    headers = ["ID", "POSITION", "TYPE", "LABEL", "STATES", "PLAIN-LANGUAGE ACTION", "CONTROL / RELAY", "RELEASE NOTE"]
    rows = [
        ["R1-C1", "top 1", "3-pos", "WIPERS", "OFF/LOW/HIGH", "Parks, then selects low or high wipe.", "Wiper interface controller/relays.", "Function fixed; hole, stack and park logic HOLD."],
        ["R1-C2", "top 2", "3-pos", "LIGHTS", "OFF/SIDE/HEAD", "Turns off, sidelights on, or headlamps on.", "Master request; retained dip drives T1/T2.", "Function fixed; prove side/head/dip logic."],
        ["R1-C3", "top 3", "2-pos", "SPOTS", "OFF/ON", "Turns auxiliary spot lamps off/on.", "T5 spot-lamp relay trigger.", "Function and relay assignment fixed; hole HOLD."],
        ["R1-C4", "top 4", "2-pos", "AUX", "OFF/ON", "Controls one reserved accessory circuit.", "B2 auxiliary relay/control output.", "Function fixed; actual accessory/load remains HOLD."],
        ["R2-C1", "bottom 1", "3-pos", "BLOWER", "OFF/LOW/HIGH", "Stops or selects cabin-fan low/high.", "Dedicated HVAC controller/relay/resistor.", "Function fixed; measure load and size circuit."],
        ["R2-C2", "bottom 2", "2-pos", "A/C", "OFF/ON", "Requests compressor cooling when safe.", "B1 via thermostat/trinary/pressure chain.", "Function fixed; safety chain and T4 fan test HOLD."],
        ["R2-C3", "bottom 3", "2-pos", "FUEL STOP", "RUN/STOP", "Keeps engine running or requests shutdown.", "Stop-device control after identification.", "PROVISIONAL; live shutdown test; retain manual cable."],
        ["R2-C4", "bottom 4", "red push", "HAZARD", "OFF/FLASH", "Flashes all indicators for warning.", "Existing hazard/flasher circuit.", "Separate from seven selectors; OEM indicator stalk retained."],
    ]
    row_h = 13*mm
    x_cursor = left
    c.setFillColor(HexColor("#30373d"))
    c.setStrokeColor(HexColor("#7d878f"))
    for width, header in zip(col_widths, headers):
        c.rect(x_cursor, top-row_h, width*mm, row_h, fill=1, stroke=1)
        c.setFillColor(HexColor("#ffffff"))
        c.setFont("Helvetica-Bold", 6.2)
        c.drawString(x_cursor+1.5*mm, top-8.2*mm, header)
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
            c.setFont("Helvetica-Bold" if cidx in (0, 3) else "Helvetica", 5.8)
            max_chars = max(7, int(width * 0.95))
            words = value.split()
            lines: list[str] = []
            current = ""
            for word in words:
                candidate = word if not current else f"{current} {word}"
                if len(candidate) <= max_chars:
                    current = candidate
                else:
                    lines.append(current)
                    current = word
            if current:
                lines.append(current)
            for line_index, line in enumerate(lines[:3]):
                c.drawString(x_cursor+1.5*mm, y_cursor-(4.5+3.4*line_index)*mm, line)
            x_cursor += width*mm
        y_cursor -= row_h

    note_y = y_cursor-8*mm
    c.setFillColor(HexColor("#20262b"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(15*mm, note_y, "ELECTRICAL RULES")
    c.setFont("Helvetica", 8)
    for row in [
        "All selectors command fused relay/control circuits only; no selector carries lamp, blower, clutch, motor or accessory load current directly.",
        "Baseline: T1 LOW BEAM, T2 HIGH BEAM, T3 HORN, T4 CONDENSER FAN, T5 SPOTS, B1 A/C CLUTCH, B2 AUX, B3 SPARE.",
        "WIPERS must retain automatic park in OFF. LIGHTS is the master OFF/SIDE/HEAD request; the retained dip control selects T1 low or T2 high beam.",
        "A/C may request B1 only through thermostat/trinary/pressure protection. Prove T4 fan logic with the selected HVAC system before operation.",
        "BLOWER requires its own measured controller/relay/resistor or PWM circuit. FUEL STOP remains provisional until RUN-to-OFF is live-tested.",
        "Retain the manual engine-stop cable. The separate red HAZARD control must not disturb the original left/right indicator stalk operation.",
    ]:
        note_y -= 6.2*mm
        c.drawString(15*mm, note_y, row)
    note_y -= 5*mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(15*mm, note_y, "M1-M9 PRODUCTION HOLD GATES")
    c.setFont("Helvetica", 7.5)
    for row in [
        "M1 fit fascia/vehicle-opening template clear of preserved pressings and establish vent-neck relief | M2 actual LCD drawing | M3 LCD rear body, mount, depth and connector sweep",
        "M4 measure seven selector assemblies + hazard | M5 fit 190 x 88 right-bank template and prove rear stacks | M6 measure all four vent faces, cutouts, retainers and necks",
        "M7 prove four hose routes and bend radii | M8 signed 1:1 prototype: glovebox, instruments, steering, gear lever, sight line, service removal | M9 continuity, labels and live tests",
    ]:
        note_y -= 6.2*mm
        c.drawString(15*mm, note_y, row)
    c.setFillColor(HexColor("#8b1e1e"))
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(15*mm, 18*mm, "RELEASE: only the 410 x 148 R6 centre-fascia outer blank. Vehicle cuts, control bank, four vent cuts, LCD, mounting and clamp geometry remain HOLD.")
    c.setFillColor(HexColor("#53606a"))
    c.setFont("Helvetica", 6.7)
    c.drawString(15*mm, 11*mm, "Electrical basis: electrical_master.csv; electrical_diagram_reconciliation_20260518.csv; engine_electrical_inputs_reconciliation_20260517.csv; expenses.csv.")
    c.showPage()
    c.save()


def write_csvs() -> None:
    with (OUT / "fabricator_cut_list.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["part", "qty", "material", "thickness_mm", "finish", "file", "release"])
        w.writerows([
            ["compact centre fascia", 1, "CR4 mild steel", 1.5, "low-gloss body colour", "centre_fascia_template_rev_f.dxf", "CUT_FASCIA_OUTER 410 x 148 R6 RELEASED; HOLD_VEHICLE_OPENING is behind-fascia reference only; LCD, two central vents and mounting holes HOLD"],
            ["right-side eight-position control bank", 1, "CR4 mild steel", 1.5, "low-gloss body colour; 3 mm labels black infill", "right_control_bank_eight_position_template_rev_f.dxf", "QUOTE/HOLD entire part pending 1:1 vehicle fit, seven actual selectors, hazard and rear-stack check"],
            ["outer dash vent pair transfer template", 1, "card or clear acrylic", 2.0, "none", "outer_dash_vent_pair_transfer_template_rev_f.dxf", "TEMPLATE ONLY; both vehicle positions and Ø66 apertures HOLD pending actual vents and duct sweep"],
            ["LCD rear clamp reference blank", 1, "5052-H32 aluminium", 2.0, "black", "lcd_rear_clamp_blank_rev_f.dxf", "QUOTE/HOLD all geometry pending actual LCD body, mounts, connectors and service-removal trial"],
        ])
    with (OUT / "measurement_and_release_schedule.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["id", "measurement", "nominal_or_intent", "required_evidence", "status"])
        w.writerows([
            ["M1", "fit centre fascia and establish vehicle opening/relief while protecting original speedometer pressing and glovebox", "fascia 410 x 148 R6; HOLD envelope 374 x 124 at x18/y12; final opening may need vent-neck scallops", "1:1 template on vehicle, front/rear ruler photos, signed cut line and vent-neck trial", "HOLD vehicle cut"],
            ["M2", "LCD active area, front aperture and bezel", "true 9-inch 16:9 active 199.2 x 112.1; aperture 202 x 115; bezel envelope 218 x 128", "manufacturer mechanical drawing plus caliper check", "HOLD"],
            ["M3", "LCD rear body, mount centres, depth, connectors and removal path", "supplier-specific; rear clamp drawing is reference only", "rear rubbing, depth gauge, plug trial and cabin-side removal trial", "HOLD"],
            ["M4", "seven bought industrial selectors plus red hazard bush, anti-rotation and contact-block stacks", "selectors Ø22.3 nominal; hazard Ø16 reference; 3 x 3-position + 4 x 2-position", "measure every bought control and record front flange/rear stack", "HOLD"],
            ["M5", "right-side 4 x 2 bank location and envelope", "190 x 88 reference; x=24/71/118/165 and y=64/24; pitch 47 x 40", "1:1 bank template fitted right of speedometer with rear-stack, steering and sight-line checks", "HOLD"],
            ["M6", "all four vent faces, cutouts, retainers, neck OD and rear depth", "satin-silver face Ø82 maximum; cutout Ø66 reference; neck target Ø63.5; flush to +0.5", "caliper record for all four vents, installed retainer trial and four position templates", "HOLD"],
            ["M7", "four HVAC hose routes, plenum branches, bend radii and service access", "no crushed hose or interference with glovebox, instruments, steering or wiring", "full rear mock-up, blower-flow trial and photos from behind dash", "HOLD"],
            ["M8", "complete dashboard 1:1 prototype and operational clearances", "original glovebox/speedometer unchanged; no unnecessary downward extension", "signed physical fit with glovebox, instruments, steering, gear lever, sight line and service-removal sweep", "HOLD"],
            ["M9", "labels, continuity, relay mapping and live functional tests", "seven selector assignments plus separate hazard exactly as scheduled", "continuity sheet, fused relay map, wiper park, lights, HVAC interlock, fuel-stop and hazard tests", "HOLD"],
        ])
    with (OUT / "switch_position_schedule.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "physical_location_viewed_from_cabin", "selector_type", "panel_label", "states", "plain_language_action", "control_or_relay", "release"])
        w.writerows([
            ["R1-C1", "right bank top row column 1", "3-position maintained", "WIPERS", "OFF / LOW / HIGH", "Parks the wipers in OFF and selects low or high wipe speed", "wiper interface controller/relays; no motor current through selector", "function locked; aperture/rear stack and park logic HOLD"],
            ["R1-C2", "right bank top row column 2", "3-position maintained", "LIGHTS", "OFF / SIDE / HEAD", "Turns lights off, selects sidelights or enables headlamps", "master lighting request; retained dip control selects T1 low or T2 high beam", "function locked; side/head/dip logic proof HOLD"],
            ["R1-C3", "right bank top row column 3", "2-position maintained", "SPOTS", "OFF / ON", "Turns the auxiliary spot lamps off or on", "T5 spot-lamp relay trigger", "function and relay allocation locked; aperture HOLD"],
            ["R1-C4", "right bank top row column 4", "2-position maintained", "AUX", "OFF / ON", "Turns one reserved future accessory circuit off or on", "B2 auxiliary relay/control output", "function locked; selected accessory and load remain HOLD"],
            ["R2-C1", "right bank bottom row column 1", "3-position maintained", "BLOWER", "OFF / LOW / HIGH", "Stops the cabin fan or selects low or high airflow", "dedicated measured HVAC controller/relay/resistor or PWM", "function locked; load measurement and circuit sizing HOLD"],
            ["R2-C2", "right bank bottom row column 2", "2-position maintained", "A/C", "OFF / ON", "Requests compressor cooling when the safety chain permits", "B1 A/C clutch request through thermostat/trinary/pressure chain; prove T4 fan", "function locked; protection and fan-logic test HOLD"],
            ["R2-C3", "right bank bottom row column 3", "2-position maintained", "FUEL STOP", "RUN / STOP", "Maintains engine run or requests engine shutdown", "final stop-device control after device/terminal identification", "PROVISIONAL pending live RUN-to-OFF test; retain manual stop cable"],
            ["R2-C4", "right bank bottom row column 4", "separate red pushbutton", "HAZARD", "OFF / FLASH", "Flashes all direction indicators as a warning", "existing hazard/flasher circuit", "separate from seven selectors; original indicator stalk retained"],
        ])


def write_readme() -> None:
    text = """# J40 RHD Compact 9-inch LCD / Four-outlet Dashboard - Rev F

Rev F is the compact arrangement shown on both owner photographs. The ashtray is removed and the centre zone becomes a shallow body-colour CNC fascia containing only a true 9-inch LCD and two large circular A/C outlets. A matching outlet is integrated at each end of the dashboard, giving four outlets total. All seven bought industrial selectors are consolidated in one labelled 4 x 2 bank to the right of the original speedometer; the separate red hazard switch occupies the eighth position. The original speedometer/instrument pressing and glovebox/instruction panel remain unchanged.

## Locked visual and packaging intent

- Keep the dashboard recognisably original: preserve its full-width painted pressing, original speedometer opening and original glovebox/instruction panel.
- Delete the complete ashtray door, body, lip, seam and recess. Flatten only the combined centre radio/ashtray zone needed by the new fascia.
- Do not extend the centre dashboard downwards for controls. The centre fascia is 410 x 148 mm, 77 mm (34%) shallower than Rev E.
- Finish new metal in matching low-gloss body colour. Use a restrained black LCD bezel and four matching satin/brushed-silver directional outlet bezels with dark cores.
- Engrave every right-bank control label 3 mm high and fill black.

## Nominal centre-fascia geometry

Datum is the lower-left corner of the 410 x 148 mm fascia blank. Dimensions are millimetres.

| Feature | X | Y | Size / status |
|---|---:|---:|---|
| Released fascia outer | 0 | 0 | 410 x 148, R6; `CUT_FASCIA_OUTER` only |
| Vehicle opening envelope behind fascia | 18 | 12 | 374 x 124, R3; `HOLD_VEHICLE_OPENING`, not a fascia cut |
| LCD bezel envelope | 96 | 10 | 218 x 128; HOLD to actual LCD |
| LCD aperture | 104 | 16.5 | 202 x 115; HOLD to actual LCD |
| Centre outlet 2 | 49 | 74 | face Ø82 max; rear cut Ø66 reference; HOLD |
| Centre outlet 3 | 361 | 74 | face Ø82 max; rear cut Ø66 reference; HOLD |

The screen reference is a true 9-inch 16:9 active image: 199.2 x 112.1 mm and 228.6 mm diagonal. The actual LCD mechanical drawing controls the front aperture, bezel, rear body, mounting, connector and removal clearances.

The nominal central geometry has been checked: each Ø82 face has 8 mm side margin, a 6 mm visible gap to the LCD bezel, and the Ø66 cut has a 14 mm ligament to the bezel. The bezel has 10 mm top and bottom land. These checks show feasibility only; the actual bought parts still control production holes.

## Four integrated A/C outlets

Numbering is passenger to driver on this right-hand-drive dashboard:

1. Far passenger-side/left dash end — positioned using the outer-vent transfer template.
2. Left side of the centre fascia at (49,74).
3. Right side of the centre fascia at (361,74).
4. Far driver-side/right dash end — positioned using the outer-vent transfer template.

All four outlets must match: satin/brushed-silver circular directional face, Ø82 mm maximum visible diameter, dark directional core permitted, face flush to +0.5 mm maximum, hidden rear nut/spring ring/clamp and no exposed front screw. The reference rear cut is Ø66 and target flexible-hose neck is Ø63.5 mm / 2.5 inch.

The 374 x 124 vehicle-opening rectangle lies behind the new fascia and is not a fascia toolpath. Its nominal side edges do not fully clear the two Ø66 centre vent cuts, so the final vehicle opening needs measured rear-relief scallops or a revised profile. Establish that profile only after a 1:1 fascia, real vents and real duct hose are mocked up from behind. Route four hoses from the selected HVAC plenum without crushed bends or contact with the glovebox, instruments, steering, wiring or screen.

## Consolidated right-side control bank

Reference envelope is 190 x 88 mm. Hole centres are x = 24, 71, 118, 165 and y = 64 (top) / 24 (bottom), giving 47 mm horizontal and 40 mm vertical pitch. Nominal selector apertures are Ø22.3; the red hazard aperture is Ø16 reference. The minimum nominal hole-edge land is 12.85 mm. Entire bank geometry and vehicle position remain HOLD until the actual switches and a 1:1 template are fitted right of the speedometer.

| Position | Label | Hardware / states | What it does |
|---|---|---|---|
| R1-C1 | WIPERS | 3-position: OFF / LOW / HIGH | Parks the wipers in OFF and selects low or high wipe speed. |
| R1-C2 | LIGHTS | 3-position: OFF / SIDE / HEAD | Turns lights off, selects sidelights or enables headlamps; retained dip selects low/high. |
| R1-C3 | SPOTS | 2-position: OFF / ON | Commands spot-lamp relay T5. |
| R1-C4 | AUX | 2-position: OFF / ON | Commands reserved accessory relay/output B2; final accessory is not selected. |
| R2-C1 | BLOWER | 3-position: OFF / LOW / HIGH | Stops the cabin fan or selects low/high airflow. |
| R2-C2 | A/C | 2-position: OFF / ON | Requests compressor cooling through the thermostat/trinary/pressure safety chain. |
| R2-C3 | FUEL STOP | 2-position: RUN / STOP | Maintains engine run or requests shutdown; provisional until live-tested. |
| R2-C4 | HAZARD | separate red pushbutton: OFF / FLASH | Flashes all indicators; original left/right indicator stalk remains. |

The purchased-selector allocation is three 3-position units (WIPERS, LIGHTS, BLOWER) and four 2-position units (SPOTS, AUX, A/C, FUEL STOP). HAZARD is a separate eighth control, not another selector.

## Electrical implementation

- Every selector commands a fused relay or controller input only. Do not carry lamp, blower, clutch, wiper-motor or accessory load current through a selector contact.
- Relay baseline: T1 low beam, T2 high beam, T3 horn, T4 condenser fan, T5 spots, B1 A/C clutch, B2 AUX and B3 spare.
- WIPERS requires an interface that preserves automatic park when the selector returns to OFF.
- LIGHTS is OFF/SIDE/HEAD master selection; retain the separate dip function that selects T1 low beam or T2 high beam.
- BLOWER uses a dedicated measured relay/controller and resistor or PWM circuit sized after the actual motor load is measured.
- A/C may request B1 only through thermostat, trinary/pressure protection and the selected HVAC controls. Prove T4 condenser-fan logic before operation.
- FUEL STOP is provisional until the actual stop device, contact sense and terminals are identified and RUN-to-OFF shutdown is proved with the engine running. Retain the manual stop cable.

Evidence basis: `data/manual/workbook_tabs/electrical_master.csv`, `data/manual/expenses.csv`, `data/manual/electrical_diagram_reconciliation_20260518.csv` and `data/manual/engine_electrical_inputs_reconciliation_20260517.csv`.

## CNC layer and release rules

- `CUT_FASCIA_OUTER` is the only released metal toolpath: 410 x 148 x 1.5 mm CR4, R6 corners.
- Every layer beginning `HOLD_` is construction/reference geometry and must not be sent to a production cut path.
- `HOLD_VEHICLE_OPENING` is the proposed void in the original dashboard behind the overlay fascia; it is not a cut through the new fascia.
- `CUT_TEMPLATE_OUTER` applies only to the disposable outer-vent transfer template, never to vehicle metal.
- Quote the right control bank, outer-vent templates and LCD clamp now, but do not production-cut them until M1-M9 evidence is complete.
- Cut any approved vehicle opening initially undersize, trim progressively, deburr/radius all edges and epoxy-prime exposed steel before paint.

## M1-M9 production gates

See `measurement_and_release_schedule.csv`. In summary: fit the centre template and define vent relief; obtain the LCD drawing and rear clearances; measure every control; fit the 4 x 2 bank template; measure all four vents; mock up all four ducts; sign off the full-size physical dashboard; then prove labels, continuity, relays, wiper park, lights, blower, A/C protection, fuel shutdown and hazard operation.

## Paired-view visual rule

Every future design revision must be applied to both owner images: the assembled right-hand-drive driver view and the straight-on bare-shell view. The images establish appearance and placement intent only and must never be scaled for CNC work.

## Acceptance

- Original glovebox/instruction panel and speedometer/instrument pressing remain visually and structurally unchanged.
- Centre fascia does not extend below the original dashboard lower line more than required for its return/mounting lip.
- Actual screen proves a true 9-inch active area and is service-removable.
- Four matching Ø82-max silver directional outlets are integrated, secure, serviceable and supplied by unobstructed ducting.
- All seven selectors and separate hazard control are together right of the speedometer and carry the scheduled engraved labels.
- All operational and safety tests in M9 pass without overheating, voltage drop, interference, rattle or unintended function.

## Package contents

- `j40_dashboard_lcd_hvac_fascia_rev_f_shop_spec.pdf` — three-page CNC/shop brief.
- `dashboard_lcd_hvac_fascia_rev_f_dimensioned_front.svg` — centre fascia and 4 x 2 control-bank drawing.
- Two owner-photo visualisations — assembled and bare-shell views; do not scale.
- Four DXFs — centre fascia, right control bank, outer-vent pair transfer template and LCD rear-clamp reference.
- Three CSV schedules — cut list, M1-M9 measurement/release gates and complete control/electrical mapping.

This package is ready to send for quotation and template work. Only the centre-fascia outer blank is released for metal cutting; all vehicle cuts and actual-part apertures remain HOLD until the recorded fit and measurement gates are signed off.
"""
    (OUT / "README.md").write_text(text, encoding="utf-8")

def package() -> None:
    DELIVERABLE.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DELIVERABLE, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.iterdir()):
            z.write(p, f"dashboard_lcd_hvac_fascia_rev_f/{p.name}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if CONCEPT_ASSEMBLED_SOURCE.exists():
        shutil.copy2(
            CONCEPT_ASSEMBLED_SOURCE,
            OUT / "dashboard_lcd_hvac_fascia_rev_f_photo_overlay_assembled.png",
        )
    if CONCEPT_BARE_SOURCE.exists():
        shutil.copy2(
            CONCEPT_BARE_SOURCE,
            OUT / "dashboard_lcd_hvac_fascia_rev_f_photo_overlay_bare_shell.png",
        )
    make_dxfs(); write_svg(); write_csvs(); write_readme(); write_pdf(); package()
    print(OUT); print(DELIVERABLE)


if __name__ == "__main__":
    main()
