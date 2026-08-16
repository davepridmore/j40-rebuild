#!/usr/bin/env python3
"""Build the Rev R fabrication-reference cooling-pack restoration plan PDF."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image as PILImage
from reportlab.graphics.shapes import Circle, Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    LongTable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "j40-cooling-pack-restoration-plan-rev-r.pdf"
TMP = ROOT / "tmp" / "pdfs"

ASSETS = ROOT / "data" / "manual" / "fabrication" / "front_cooling_stack_rev_c" / "work_document_assets"
PORTAL = ROOT / "docs" / "project-control-ui" / "assets" / "cooling-na-rev-p"

OLD_R0 = ASSETS / "rev_k_r01_actual_removed_radiator_reference.jpg"
OLD_R0_DAMAGE = ROOT / "photos" / "20260529_230009_gp_BLX8dSWA.jpg"
OLD_R0_LEG = ROOT / "photos" / "20260529_230035_gp_5oB8otKw.jpg"
OLD_C0 = ASSETS / "rev_k_r02_actual_full_face_condenser_reference.jpg"
OLD_C0_DRIER = ROOT / "photos" / "20260512_212947_gp_AdvWGolg.jpg"
OLD_G0 = ASSETS / "rev_k_r05_actual_stone_guard_reference.jpg"
OLD_FS = ASSETS / "rev_l_r13_small_electric_fan.jpg"
OLD_FL = ASSETS / "rev_l_r12_large_electric_fan.jpg"
OLD_CHASSIS = ROOT / "photos" / "20260512_100000_user_front_support_radiator_pickups_context.png"

RENEW_INSTALLED = PORTAL / "na-stack-short-connector-arms-finished.png"
RENEW_BENCH = PORTAL / "na-connector-arm-holder-parts-bench.png"
RENEW_DRYFIT = PORTAL / "na-short-arm-chassis-dry-fit.png"
RENEW_HOLDERS = PORTAL / "na-guard-radiator-holder-detail.png"

PAGE_W, PAGE_H = A4
MARGIN = 15 * mm
CONTENT_W = PAGE_W - (2 * MARGIN)

NAVY = colors.HexColor("#102C3C")
TEAL = colors.HexColor("#1D776E")
COPPER = colors.HexColor("#A45B35")
INK = colors.HexColor("#20282D")
MUTED = colors.HexColor("#5D6B72")
PAPER = colors.HexColor("#F4F1EB")
PALE_BLUE = colors.HexColor("#E9F1F4")
PALE_TEAL = colors.HexColor("#E7F2EF")
PALE_AMBER = colors.HexColor("#F6EBD8")
PALE_RED = colors.HexColor("#F5E4E1")
LINE = colors.HexColor("#C7D0D3")
WHITE = colors.white
RED = colors.HexColor("#A53F3F")
GREEN = colors.HexColor("#3F7757")


def P(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def image_fit(path: Path, max_w: float, max_h: float) -> Image:
    with PILImage.open(path) as im:
        w, h = im.size
    scale = min(max_w / w, max_h / h)
    return Image(str(path), width=w * scale, height=h * scale)


def page_title(title: str, deck: str, styles: dict[str, ParagraphStyle]):
    return [
        P(title, styles["section"]),
        P(deck, styles["deck"]),
        Spacer(1, 3 * mm),
        HRFlowable(width="100%", thickness=1.2, color=TEAL),
        Spacer(1, 4 * mm),
    ]


def callout(title: str, body: str, styles: dict[str, ParagraphStyle], color=PALE_BLUE):
    box = Table(
        [[P(title, styles["callout_title"])], [P(body, styles["body"]) ]],
        colWidths=[CONTENT_W],
    )
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), color),
                ("BOX", (0, 0), (-1, -1), 0.7, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return box


def photo_card(
    path: Path,
    label: str,
    caption: str,
    width: float,
    height: float,
    styles: dict[str, ParagraphStyle],
    renewed: bool = False,
):
    label_color = TEAL if renewed else COPPER
    img = image_fit(path, width - 8, height)
    rows = [
        [P(label, styles["photo_label"])],
        [img],
        [P(caption, styles["caption"])],
    ]
    table = Table(rows, colWidths=[width], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), label_color),
                ("TEXTCOLOR", (0, 0), (0, 0), WHITE),
                ("BACKGROUND", (0, 1), (0, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.7, LINE),
                ("ALIGN", (0, 1), (0, 1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def data_table(
    rows: list[list[str]],
    widths: list[float],
    styles: dict[str, ParagraphStyle],
    header_color=NAVY,
    font_style="table",
    repeat_rows=1,
    row_backgrounds: bool = True,
):
    parsed = []
    for r_idx, row in enumerate(rows):
        parsed.append(
            [P(cell, styles["table_header"] if r_idx == 0 else styles[font_style]) for cell in row]
        )
    table = LongTable(parsed, colWidths=widths, repeatRows=repeat_rows, hAlign="LEFT")
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), header_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if row_backgrounds:
        for idx in range(1, len(rows)):
            if idx % 2 == 0:
                commands.append(("BACKGROUND", (0, idx), (-1, idx), colors.HexColor("#F7F8F7")))
    table.setStyle(TableStyle(commands))
    return table


def bullets(items: list[str], styles: dict[str, ParagraphStyle], level=0):
    out = []
    for item in items:
        out.append(P(f"- {item}", styles["bullet"] if level == 0 else styles["small"]))
    return out


def numbered(items: list[str], styles: dict[str, ParagraphStyle]):
    return [P(f"{i}. {item}", styles["bullet"]) for i, item in enumerate(items, start=1)]


def diagram_row(labels: list[str], styles: dict[str, ParagraphStyle], color=PALE_TEAL):
    cells = []
    widths = []
    for idx, label in enumerate(labels):
        cells.append(P(label, styles["diagram"]))
        widths.append((CONTENT_W - (len(labels) - 1) * 12) / len(labels))
        if idx < len(labels) - 1:
            cells.append(P(">", styles["diagram_arrow"]))
            widths.append(12)
    table = Table([cells], colWidths=widths)
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]
    for idx in range(0, len(cells), 2):
        commands.extend(
            [
                ("BACKGROUND", (idx, 0), (idx, 0), color),
                ("BOX", (idx, 0), (idx, 0), 0.7, TEAL),
                ("TOPPADDING", (idx, 0), (idx, 0), 7),
                ("BOTTOMPADDING", (idx, 0), (idx, 0), 7),
            ]
        )
    table.setStyle(TableStyle(commands))
    return table


def d_text(
    drawing: Drawing,
    x: float,
    y: float,
    text: str,
    size: float = 6.6,
    color=INK,
    anchor: str = "middle",
    bold: bool = False,
    angle: float = 0,
):
    drawing.add(
        String(
            x,
            y,
            text,
            fontName="Helvetica-Bold" if bold else "Helvetica",
            fontSize=size,
            fillColor=color,
            textAnchor=anchor,
            angle=angle,
        )
    )


def d_arrow(
    drawing: Drawing,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color=COPPER,
    width: float = 1.2,
    head: float = 4.5,
):
    drawing.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=width))
    angle = math.atan2(y2 - y1, x2 - x1)
    left = (
        x2 - head * math.cos(angle) + head * 0.55 * math.sin(angle),
        y2 - head * math.sin(angle) - head * 0.55 * math.cos(angle),
    )
    right = (
        x2 - head * math.cos(angle) - head * 0.55 * math.sin(angle),
        y2 - head * math.sin(angle) + head * 0.55 * math.cos(angle),
    )
    drawing.add(Polygon([x2, y2, left[0], left[1], right[0], right[1]], fillColor=color, strokeColor=color))


def d_double_arrow(drawing: Drawing, x1: float, y1: float, x2: float, y2: float, color=COPPER):
    d_arrow(drawing, x1, y1, x2, y2, color=color, width=0.9, head=3.8)
    d_arrow(drawing, x2, y2, x1, y1, color=color, width=0.9, head=3.8)


def d_dimension_h(drawing: Drawing, x1: float, x2: float, y: float, source_y: float, label: str):
    drawing.add(Line(x1, source_y, x1, y, strokeColor=COPPER, strokeWidth=0.55))
    drawing.add(Line(x2, source_y, x2, y, strokeColor=COPPER, strokeWidth=0.55))
    d_double_arrow(drawing, x1, y, x2, y)
    d_text(drawing, (x1 + x2) / 2, y + 4, label, 6.2, COPPER, bold=True)


def d_dimension_v(drawing: Drawing, x: float, y1: float, y2: float, source_x: float, label: str):
    drawing.add(Line(source_x, y1, x, y1, strokeColor=COPPER, strokeWidth=0.55))
    drawing.add(Line(source_x, y2, x, y2, strokeColor=COPPER, strokeWidth=0.55))
    d_double_arrow(drawing, x, y1, x, y2)
    d_text(drawing, x - 5, (y1 + y2) / 2, label, 6.2, COPPER, bold=True, angle=90)


def d_watermark(drawing: Drawing):
    d_text(
        drawing,
        drawing.width - 4,
        4,
        "ILLUSTRATIVE - NOT TO SCALE - VERIFY ON VEHICLE",
        5.2,
        colors.HexColor("#8A969B"),
        anchor="end",
        bold=True,
    )


def front_datum_diagram(width=CONTENT_W, height=67 * mm):
    d = Drawing(width, height)
    cx = width * 0.50
    base_y = 23
    aperture_w, aperture_h = width * 0.68, height * 0.68
    ax = cx - aperture_w / 2
    ay = base_y
    d.add(Rect(ax, ay, aperture_w, aperture_h, fillColor=colors.HexColor("#EFF2F3"), strokeColor=NAVY, strokeWidth=2))
    d.add(Rect(ax + 12, ay + 10, aperture_w - 24, aperture_h - 20, fillColor=None, strokeColor=TEAL, strokeWidth=2))
    d.add(Rect(ax + 32, ay + 24, aperture_w - 64, aperture_h - 48, fillColor=colors.HexColor("#E7F2EF"), strokeColor=GREEN, strokeWidth=1.3))
    fan_r = min(aperture_h * 0.26, aperture_w * 0.14)
    d.add(Circle(cx, ay + aperture_h / 2, fan_r, fillColor=colors.HexColor("#D9E6EA"), strokeColor=NAVY, strokeWidth=1.5))
    d.add(Rect(cx - fan_r * 1.18, ay + aperture_h / 2 - fan_r * 1.18, fan_r * 2.36, fan_r * 2.36, fillColor=None, strokeColor=NAVY, strokeWidth=0.8))
    d.add(Line(cx, 12, cx, height - 7, strokeColor=RED, strokeWidth=1.2, strokeDashArray=[4, 3]))
    d.add(Line(ax - 18, ay + aperture_h / 2, ax + aperture_w + 18, ay + aperture_h / 2, strokeColor=COPPER, strokeWidth=0.8, strokeDashArray=[3, 3]))
    d_text(d, cx + 5, height - 13, "D00 VCL - project independently", 6.5, RED, anchor="start", bold=True)
    d_text(d, ax - 20, ay + aperture_h / 2 + 4, "Z0", 6.3, COPPER, anchor="end", bold=True)
    d_text(d, ax + 4, ay + aperture_h + 5, "Fixed body grille usable aperture", 6.4, NAVY, anchor="start", bold=True)
    d_text(d, ax + 16, ay + aperture_h - 5, "G0 repaired perimeter frame", 6.2, TEAL, anchor="start", bold=True)
    d_text(d, cx, ay + aperture_h / 2 + 2, "FS rotor axis", 6.1, NAVY, bold=True)
    d_text(d, cx, ay + 29, "C0 usable fin field", 6.1, GREEN, bold=True)
    d_dimension_h(d, ax, ax + aperture_w, 14, ay, "W0: hard edge to hard edge at top / mid / bottom")
    d_dimension_v(d, ax - 12, ay, ay + aperture_h, ax, "H0: hard edge to hard edge")
    d_double_arrow(d, cx, ay + aperture_h / 2 + fan_r + 6, cx + 35, ay + aperture_h / 2 + fan_r + 6, RED)
    d_text(d, cx + 18, ay + aperture_h / 2 + fan_r + 10, "signed lateral offset to VCL", 5.7, RED)
    d_watermark(d)
    return d


def side_stack_diagram(width=CONTENT_W, height=67 * mm):
    d = Drawing(width, height)
    y0, h = 35, height * 0.55
    xs = [48, 93, 141, 213, 302, 385, 447]
    labels = ["Body grille", "G0", "FS", "C0", "R0", "FL", "Engine"]
    fills = [colors.HexColor("#E3E7E9"), PALE_TEAL, PALE_BLUE, colors.HexColor("#DDEDE7"), PALE_AMBER, colors.HexColor("#D9E6EA"), colors.HexColor("#E8E0D8")]
    depths = [7, 9, 15, 12, 25, 24, 28]
    for x, label, fill, dw in zip(xs, labels, fills, depths):
        d.add(Rect(x - dw / 2, y0, dw, h, fillColor=fill, strokeColor=NAVY if label in {"Body grille", "FS", "FL", "Engine"} else TEAL, strokeWidth=1.2))
        d_text(d, x, y0 + h + 7, label, 6.2, NAVY, bold=True)
        d.add(Line(x, 20, x, y0, strokeColor=COPPER, strokeWidth=0.55, strokeDashArray=[2, 2]))
    d_arrow(d, 28, y0 + h / 2, width - 22, y0 + h / 2, GREEN, 2.0, 7)
    d_text(d, width / 2, y0 + h / 2 + 7, "AIRFLOW: FRONT TO ENGINE", 6.4, GREEN, bold=True)
    d.add(Line(25, 17, 25, y0 + h + 7, strokeColor=RED, strokeWidth=1.2, strokeDashArray=[4, 3]))
    d_text(d, 29, 9, "D00 Y datum", 6.1, RED, anchor="start", bold=True)
    for idx in range(1, len(xs) - 1):
        d_double_arrow(d, 25, 17, xs[idx], 17, COPPER)
        d_text(d, (25 + xs[idx]) / 2, 10 + (idx % 2) * 6, f"Y{idx}", 5.5, COPPER, bold=True)
    d.add(Rect(372, y0 - 10, 72, h + 20, fillColor=None, strokeColor=RED, strokeWidth=0.9, strokeDashArray=[4, 3]))
    d_text(d, 408, y0 - 7, "engine movement + tool envelope", 5.6, RED)
    d_text(d, width / 2, height - 9, "Measure every plane directly from D00; never add nominal gaps in a chain", 7.0, NAVY, bold=True)
    d_watermark(d)
    return d


def support_datum_diagram(width=CONTENT_W, height=70 * mm):
    d = Drawing(width, height)
    cx = width / 2
    floor_y = 30
    cross_y = 58
    rad_w, rad_h = 230, 112
    rad_x, rad_y = cx - rad_w / 2, cross_y + 18
    d.add(Rect(rad_x, rad_y, rad_w, rad_h, fillColor=PALE_AMBER, strokeColor=TEAL, strokeWidth=1.6))
    d_text(d, cx, rad_y + rad_h / 2, "R0 naturally seated", 8, TEAL, bold=True)
    for sx in (rad_x + 42, rad_x + rad_w - 42):
        d.add(Circle(sx, cross_y + 10, 10, fillColor=colors.HexColor("#38434A"), strokeColor=NAVY, strokeWidth=1))
        d.add(Rect(sx - 17, cross_y, 34, 7, fillColor=COPPER, strokeColor=NAVY, strokeWidth=0.8))
        d_text(d, sx, cross_y - 10, "S0 / R1 / X1", 5.9, NAVY, bold=True)
    d.add(Rect(cx - 165, cross_y - 8, 330, 14, fillColor=colors.HexColor("#DCE4E6"), strokeColor=NAVY, strokeWidth=1.4))
    d_text(d, cx, cross_y - 3, "X0 lower crossmember", 6.2, NAVY, bold=True)
    for x, side in ((cx - 165, "L"), (cx + 165, "R")):
        d.add(Rect(x - 14, floor_y, 28, cross_y - floor_y, fillColor=colors.HexColor("#E7E1D9"), strokeColor=COPPER, strokeWidth=1.3))
        d.add(Rect(x - 24, floor_y - 8, 48, 8, fillColor=colors.HexColor("#C8D0D3"), strokeColor=NAVY, strokeWidth=1.2))
        d_text(d, x, floor_y + 9, f"A0-{side}", 6.2, COPPER, bold=True)
        d_text(d, x, floor_y - 17, f"A0-D-{side} connector bearing plane", 5.4, NAVY)
    d_dimension_h(d, cx - 165, cx + 165, 20, floor_y - 8, "L0: released connector / end-envelope span")
    d_dimension_v(d, cx + 188, floor_y, cross_y + 6, cx + 165, "arm height: bearing plane to X0 interface")
    d.add(Line(rad_x + 22, rad_y + rad_h - 12, rad_x - 35, rad_y + rad_h - 12, strokeColor=COPPER, strokeWidth=1))
    d.add(Line(rad_x + rad_w - 22, rad_y + rad_h - 12, rad_x + rad_w + 35, rad_y + rad_h - 12, strokeColor=COPPER, strokeWidth=1))
    d_text(d, cx, rad_y + rad_h + 6, "B0 upper keeper axes - transfer only after natural saddle seating", 6.2, COPPER, bold=True)
    d_arrow(d, cx, rad_y + 30, cx, cross_y + 12, GREEN, 1.6, 6)
    d_text(d, cx + 7, rad_y + 35, "MR weight", 6.1, GREEN, anchor="start", bold=True)
    d_watermark(d)
    return d


def step_visual(step: int, width=CONTENT_W, height=37 * mm):
    d = Drawing(width, height)
    mid = height / 2
    if step == 1:
        x_positions = [45, 122, 199, 276, 353, 430]
        ids = ["R0", "C0", "G0", "FS", "FL", "A0"]
        for idx, (x, part_id) in enumerate(zip(x_positions, ids)):
            d.add(Rect(x - 24, mid - 22, 48, 44, fillColor=PALE_BLUE if idx % 2 else PALE_AMBER, strokeColor=NAVY, strokeWidth=1.1))
            d_text(d, x, mid + 2, part_id, 8, NAVY, bold=True)
            d_text(d, x, mid - 10, "TAG + PHOTO", 5.3, MUTED, bold=True)
        d.add(Circle(70, mid + 29, 7, fillColor=PALE_RED, strokeColor=RED, strokeWidth=1))
        d_text(d, 70, mid + 27, "!", 7, RED, bold=True)
        d_arrow(d, 26, 14, 456, 14, TEAL, 1.2, 5)
        d_text(d, width / 2, 5, "identify -> cap ports -> inspect -> baseline test -> signed decision", 6.2, TEAL, bold=True)
    elif step == 2:
        d.add(Rect(55, 25, 350, 66, fillColor=colors.HexColor("#F0F2F3"), strokeColor=NAVY, strokeWidth=1.3))
        d.add(Line(width / 2, 12, width / 2, height - 8, strokeColor=RED, strokeWidth=1.2, strokeDashArray=[4, 3]))
        d.add(Line(25, 58, width - 25, 58, strokeColor=COPPER, strokeWidth=0.9, strokeDashArray=[3, 3]))
        d_text(d, width / 2 + 5, height - 15, "D00 VCL", 6.4, RED, anchor="start", bold=True)
        d_text(d, 25, 63, "Z0", 6.2, COPPER, anchor="start", bold=True)
        for x, ref in ((85, "A0-D"), (156, "S0"), (238, "CL0"), (326, "B0"), (390, "G0-H")):
            d.add(Circle(x, 58, 4, fillColor=TEAL, strokeColor=NAVY, strokeWidth=0.7))
            d_text(d, x, 40 if x % 2 else 73, ref, 5.8, NAVY, bold=True)
        d_text(d, width / 2, 7, "record instrument, origin, XYZ, method, repeatability and dated witness photo", 6.1, TEAL, bold=True)
    elif step == 3:
        d.add(Rect(28, 30, 88, 54, fillColor=PALE_RED, strokeColor=RED, strokeWidth=1.2))
        d_text(d, 72, 57, "OLD CORE", 7, RED, bold=True)
        for x in range(35, 111, 8):
            d.add(Line(x, 34, x, 80, strokeColor=RED, strokeWidth=0.35))
        d_arrow(d, 124, 57, 174, 57, COPPER, 1.5, 6)
        d.add(Rect(181, 74, 94, 14, fillColor=PALE_AMBER, strokeColor=TEAL, strokeWidth=1.1))
        d.add(Rect(181, 25, 94, 14, fillColor=PALE_AMBER, strokeColor=TEAL, strokeWidth=1.1))
        d_text(d, 228, 61, "RETAIN SOUND", 6.4, TEAL, bold=True)
        d_text(d, 228, 51, "TANKS / HEADERS", 6.1, TEAL, bold=True)
        d_arrow(d, 284, 57, 330, 57, COPPER, 1.5, 6)
        d.add(Rect(338, 25, 112, 63, fillColor=PALE_TEAL, strokeColor=GREEN, strokeWidth=1.4))
        d_text(d, 394, 57, "NEW CORE", 7.5, GREEN, bold=True)
        d_text(d, width / 2, 7, "jig -> strip -> clean/tin -> recore -> pressure + flow -> thin heat-exchanger coating", 6.0, NAVY, bold=True)
    elif step == 4:
        d.add(Rect(28, 25, 190, 65, fillColor=PALE_BLUE, strokeColor=NAVY, strokeWidth=1.2))
        for x in range(36, 210, 9):
            d.add(Line(x, 30, x, 84, strokeColor=TEAL, strokeWidth=0.35))
        d_text(d, 123, 58, "C0", 9, NAVY, bold=True)
        d_text(d, 123, 39, "neutral clean + fin comb + specialist leak test", 5.6, NAVY)
        d.add(Rect(262, 25, 190, 65, fillColor=PALE_TEAL, strokeColor=TEAL, strokeWidth=1.2))
        d.add(Rect(273, 35, 168, 45, fillColor=None, strokeColor=TEAL, strokeWidth=2))
        d_text(d, 357, 58, "G0", 9, TEAL, bold=True)
        d_text(d, 357, 39, "jig perimeter + repair mesh + removal check", 5.6, TEAL)
        d_text(d, width / 2, 7, "fixed body grille is not G0; keep C0 ports capped and G0 mesh open", 6.1, NAVY, bold=True)
    elif step == 5:
        d.add(Circle(105, 60, 36, fillColor=PALE_BLUE, strokeColor=NAVY, strokeWidth=1.4))
        d.add(Circle(365, 60, 44, fillColor=PALE_TEAL, strokeColor=TEAL, strokeWidth=1.4))
        d_text(d, 105, 60, "FS", 10, NAVY, bold=True)
        d_text(d, 365, 60, "FL", 10, TEAL, bold=True)
        for yy in (44, 60, 76):
            d_arrow(d, 35, yy, 165, yy, GREEN, 1.3, 5)
            d_arrow(d, 300, yy, 435, yy, GREEN, 1.3, 5)
        d_text(d, 105, 103, "ONE FRONT PUSHER", 6.2, NAVY, bold=True)
        d_text(d, 365, 111, "ONE REAR PULLER", 6.2, TEAL, bold=True)
        d_text(d, 235, 82, "relay + fuse + earth", 5.8, COPPER, bold=True)
        d_text(d, 235, 51, "relay + fuse + earth", 5.8, COPPER, bold=True)
        d.add(Line(183, 78, 287, 78, strokeColor=COPPER, strokeWidth=1))
        d.add(Line(183, 47, 287, 47, strokeColor=COPPER, strokeWidth=1))
        d_text(d, width / 2, 7, "bench-test direction and current; size each protected branch from measured values", 6.1, NAVY, bold=True)
    elif step == 6:
        d.add(Rect(42, 17, 42, 22, fillColor=colors.HexColor("#C9D0D3"), strokeColor=NAVY, strokeWidth=1.1))
        d.add(Rect(width - 84, 17, 42, 22, fillColor=colors.HexColor("#C9D0D3"), strokeColor=NAVY, strokeWidth=1.1))
        d.add(Rect(54, 39, 24, 43, fillColor=PALE_AMBER, strokeColor=COPPER, strokeWidth=1.2))
        d.add(Rect(width - 78, 39, 24, 43, fillColor=PALE_AMBER, strokeColor=COPPER, strokeWidth=1.2))
        d.add(Rect(66, 73, width - 132, 15, fillColor=PALE_BLUE, strokeColor=NAVY, strokeWidth=1.3))
        d_text(d, width / 2, 78, "X0", 7, NAVY, bold=True)
        d_text(d, 66, 53, "A0-L", 5.8, COPPER, bold=True)
        d_text(d, width - 66, 53, "A0-R", 5.8, COPPER, bold=True)
        d_dimension_h(d, 66, width - 66, 101, 88, "L0 actual span")
        d_arrow(d, width / 2, 115, width / 2, 89, GREEN, 1.5, 6)
        d_text(d, width / 2 + 7, 109, "R0 load", 6, GREEN, anchor="start", bold=True)
        d_text(d, width / 2, 7, "template connector bearing planes first; bench-cut loose arms; structural release controls metal", 6.1, NAVY, bold=True)
    elif step == 7:
        group_x = [58, 175, 300, 420]
        titles = ["G1/G2", "R1/X1 + R3", "C1/F1", "F2/E1"]
        for x, title in zip(group_x, titles):
            d.add(Rect(x - 45, 26, 90, 66, fillColor=colors.white, strokeColor=TEAL, strokeWidth=1.1))
            d_text(d, x, 82, title, 6.7, TEAL, bold=True)
        d.add(Rect(36, 42, 44, 28, fillColor=PALE_TEAL, strokeColor=NAVY, strokeWidth=1))
        d.add(Line(28, 35, 88, 35, strokeColor=COPPER, strokeWidth=4))
        d_text(d, 58, 50, "G0 frame", 5.3, NAVY)
        d.add(Circle(160, 42, 10, fillColor=colors.HexColor("#38434A"), strokeColor=NAVY))
        d.add(Rect(145, 32, 30, 7, fillColor=COPPER, strokeColor=NAVY))
        d.add(Line(190, 43, 190, 73, strokeColor=COPPER, strokeWidth=3))
        d_text(d, 175, 62, "lower load /", 5.2, NAVY)
        d_text(d, 175, 53, "upper neutral", 5.2, NAVY)
        d.add(Rect(270, 39, 60, 38, fillColor=PALE_BLUE, strokeColor=NAVY))
        d.add(Circle(300, 58, 18, fillColor=None, strokeColor=TEAL, strokeWidth=1.2))
        d_text(d, 300, 31, "independent", 5.2, NAVY)
        d.add(Rect(389, 38, 62, 40, fillColor=PALE_AMBER, strokeColor=NAVY))
        d.add(Rect(395, 44, 50, 28, fillColor=None, strokeColor=TEAL, strokeWidth=1.4))
        d_text(d, 420, 31, "seal + service", 5.2, NAVY)
        d_text(d, width / 2, 7, "broad replaceable EPDM contacts; no core, tank, fin, mesh or cross-component load", 6.0, NAVY, bold=True)
    elif step == 8:
        xs = [50, 99, 148, 210, 290, 370]
        labels = ["grille", "G0", "FS", "C0", "R0", "FL"]
        for idx, (x, label) in enumerate(zip(xs, labels)):
            d.add(Rect(x - 7, 27, 14 if label not in {"R0", "FL"} else 22, 67, fillColor=PALE_TEAL if idx % 2 else PALE_BLUE, strokeColor=NAVY, strokeWidth=1))
            d_text(d, x, 101, label, 5.8, NAVY, bold=True)
        d.add(Rect(397, 20, 60, 80, fillColor=None, strokeColor=RED, strokeWidth=1, strokeDashArray=[4, 3]))
        d_text(d, 427, 65, "engine", 6.1, RED, bold=True)
        d_text(d, 427, 55, "movement", 6.1, RED, bold=True)
        d_arrow(d, 28, 60, 455, 60, GREEN, 1.5, 6)
        for x in (99, 148, 210):
            d.add(Line(x, 15, x, 106, strokeColor=COPPER, strokeWidth=0.5, strokeDashArray=[2, 2]))
        d_text(d, width / 2, 7, "opaque 1:1 stack: actual rubbers, plugs, hose/pipe bends, tools, removal vectors and VCL", 6.0, NAVY, bold=True)
    elif step == 9:
        d.add(Rect(106, 28, 270, 15, fillColor=PALE_BLUE, strokeColor=NAVY, strokeWidth=1.3))
        for x in (160, 322):
            d.add(Circle(x, 50, 10, fillColor=colors.HexColor("#38434A"), strokeColor=NAVY))
            d_arrow(d, x, 96, x, 62, COPPER, 2, 7)
            d_text(d, x, 101, "released share of 2 x MR", 5.8, COPPER, bold=True)
            d.add(Line(x + 18, 44, x + 18, 82, strokeColor=RED, strokeWidth=1))
            d.add(Circle(x + 18, 88, 7, fillColor=colors.white, strokeColor=RED, strokeWidth=1))
        d_text(d, width / 2, 35, "X0 / A0 / connector proof fixture", 6.5, NAVY, bold=True)
        d_text(d, width / 2, 7, "record pre/post datums; 10 minutes; no local point load; proof is not fatigue design", 6.1, NAVY, bold=True)
    elif step == 10:
        d.add(Rect(30, 35, 116, 58, fillColor=PALE_AMBER, strokeColor=TEAL, strokeWidth=1.2))
        d_text(d, 88, 66, "R0 / 2H", 7.5, TEAL, bold=True)
        d_arrow(d, 40, 100, 136, 100, GREEN, 1.3, 5)
        d_arrow(d, 136, 28, 40, 28, GREEN, 1.3, 5)
        d_text(d, 88, 105, "upper hose", 5.8, GREEN, bold=True)
        d_text(d, 88, 18, "lower hose", 5.8, GREEN, bold=True)
        d.add(Rect(184, 35, 86, 58, fillColor=PALE_BLUE, strokeColor=NAVY, strokeWidth=1.2))
        d_text(d, 227, 66, "C0 A/C", 7.5, NAVY, bold=True)
        d_text(d, 227, 48, "new drier + HNBR", 5.5, NAVY)
        for y, label in ((81, "FS branch"), (49, "FL branch")):
            d.add(Rect(319, y - 10, 128, 20, fillColor=PALE_TEAL, strokeColor=NAVY, strokeWidth=1))
            d_text(d, 383, y - 1, label + ": fuse / relay / earth", 5.7, NAVY, bold=True)
        d_text(d, width / 2, 7, "bleed -> individual fan tests -> hot-idle A/C -> road/load log -> cool-down reinspection", 6.0, NAVY, bold=True)
    d_watermark(d)
    return d


def step_work_card(step: int, title: str, measure: str, work: str, passed: str, styles):
    details = Table(
        [
            [P("MEASURE / RECORD", styles["table_header"]), P("WORK", styles["table_header"]), P("PASS / RELEASE", styles["table_header"])],
            [P(measure, styles["table"]), P(work, styles["table"]), P(passed, styles["table"])],
        ],
        colWidths=[55 * mm, 60 * mm, 55 * mm],
    )
    details.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (-1, 1), colors.white),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return KeepTogether(
        [
            P(f"Step {step} - {title}", styles["h2"]),
            step_visual(step),
            Spacer(1, 1.5 * mm),
            details,
            Spacer(1, 3 * mm),
        ]
    )


def styles_for_doc():
    base = getSampleStyleSheet()
    return {
        "cover_kicker": ParagraphStyle(
            "cover_kicker", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=8.5,
            leading=10, textColor=TEAL, spaceAfter=5, tracking=0.8,
        ),
        "cover_title": ParagraphStyle(
            "cover_title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=25,
            leading=27.5, textColor=NAVY, alignment=TA_LEFT, spaceAfter=7,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", parent=base["Normal"], fontName="Helvetica", fontSize=11,
            leading=14, textColor=MUTED, spaceAfter=10,
        ),
        "section": ParagraphStyle(
            "section", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=18,
            leading=21, textColor=NAVY, spaceAfter=3,
        ),
        "deck": ParagraphStyle(
            "deck", parent=base["Normal"], fontName="Helvetica", fontSize=9.5,
            leading=12, textColor=MUTED,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=11.5,
            leading=14, textColor=TEAL, spaceBefore=5, spaceAfter=4,
        ),
        "h3": ParagraphStyle(
            "h3", parent=base["Heading3"], fontName="Helvetica-Bold", fontSize=9.4,
            leading=11.5, textColor=NAVY, spaceBefore=4, spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "body", parent=base["BodyText"], fontName="Helvetica", fontSize=8.8,
            leading=11.5, textColor=INK, spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=base["BodyText"], fontName="Helvetica", fontSize=8.6,
            leading=11.1, leftIndent=9, firstLineIndent=-7, textColor=INK, spaceAfter=2.5,
        ),
        "small": ParagraphStyle(
            "small", parent=base["BodyText"], fontName="Helvetica", fontSize=7.4,
            leading=9.2, textColor=INK, spaceAfter=2,
        ),
        "caption": ParagraphStyle(
            "caption", parent=base["BodyText"], fontName="Helvetica", fontSize=6.9,
            leading=8.5, textColor=MUTED,
        ),
        "photo_label": ParagraphStyle(
            "photo_label", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=6.8,
            leading=8, textColor=WHITE, alignment=TA_LEFT,
        ),
        "callout_title": ParagraphStyle(
            "callout_title", parent=base["Heading3"], fontName="Helvetica-Bold", fontSize=9.2,
            leading=11, textColor=NAVY, spaceAfter=2,
        ),
        "table_header": ParagraphStyle(
            "table_header", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=7.1,
            leading=8.4, textColor=WHITE,
        ),
        "table": ParagraphStyle(
            "table", parent=base["Normal"], fontName="Helvetica", fontSize=6.9,
            leading=8.4, textColor=INK,
        ),
        "table_small": ParagraphStyle(
            "table_small", parent=base["Normal"], fontName="Helvetica", fontSize=6.2,
            leading=7.4, textColor=INK,
        ),
        "diagram": ParagraphStyle(
            "diagram", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=7.2,
            leading=8.5, textColor=NAVY, alignment=TA_CENTER,
        ),
        "diagram_arrow": ParagraphStyle(
            "diagram_arrow", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11,
            leading=12, textColor=COPPER, alignment=TA_CENTER,
        ),
        "sign": ParagraphStyle(
            "sign", parent=base["Normal"], fontName="Helvetica", fontSize=8,
            leading=10, textColor=INK,
        ),
    }


def header_footer(canvas, doc):
    canvas.saveState()
    page = doc.page
    if page > 1:
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, PAGE_H - 10.5 * mm, PAGE_W - MARGIN, PAGE_H - 10.5 * mm)
        canvas.setFont("Helvetica-Bold", 7)
        canvas.setFillColor(NAVY)
        canvas.drawString(MARGIN, PAGE_H - 8 * mm, "J40 NATURALLY ASPIRATED COOLING PACK")
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 8 * mm, "REV R FABRICATION-REFERENCE WORKSHOP PLAN")
    canvas.setStrokeColor(LINE)
    canvas.line(MARGIN, 10 * mm, PAGE_W - MARGIN, 10 * mm)
    canvas.setFont("Helvetica", 6.7)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, 6.8 * mm, "Rev R workshop plan; Rev P remains technical authority | No photograph or estimate releases fabrication")
    canvas.drawRightString(PAGE_W - MARGIN, 6.8 * mm, f"Page {page}")
    canvas.restoreState()


def build_story(styles):
    story = []

    # Cover
    story += [
        Spacer(1, 5 * mm),
        P("CONTROLLED WORKSHOP PLAN | REV Q", styles["cover_kicker"]),
        P("J40 cooling pack restoration", styles["cover_title"]),
        P("Old-to-renewed refurbishment, recoring, fabricated mounts, fittings, chemicals, testing and release", styles["cover_sub"]),
        photo_card(
            RENEW_INSTALLED,
            "PHOTOREALISTIC RENEWED TARGET - NON-DIMENSIONAL",
            "Naturally aspirated arrangement with the complete G0 guard frame and single front A/C pusher centred directly on the vehicle longitudinal centre plane. The image is non-dimensional; CL0 measurements and signed drawings control every bracket.",
            CONTENT_W,
            91 * mm,
            styles,
            renewed=True,
        ),
        Spacer(1, 5 * mm),
        callout(
            "Configuration locked for this plan",
            "Toyota 2H naturally aspirated. No turbocharger, no intercooler/K0, no charge-air pipework and no second small front fan. There are two fans in total: one FS front A/C pusher and one FL rear radiator puller/shroud.",
            styles,
            PALE_TEAL,
        ),
        Spacer(1, 4 * mm),
        data_table(
            [
                ["Document basis", "Fabrication state", "Prepared"],
                ["Rev R fabrication-reference plan; Rev P technical guide", "Measured structural release HOLD", "16 Aug 2026"],
            ],
            [60 * mm, 70 * mm, 40 * mm],
            styles,
            header_color=TEAL,
        ),
        Spacer(1, 3 * mm),
        P("Use this PDF as the workshop sequence and inspection record. Actual measurements, rigid templates and signed fabrication drawings remain the controlling technical authority; photographs and planning allowances do not release fabrication.", styles["small"]),
        PageBreak(),
    ]

    # Architecture
    story += page_title(
        "1. Configuration, alignment and load paths",
        "A single, serviceable cooling stack with separate supports and a lower-only radiator weight path.",
        styles,
    )
    story += [
        P("Released air path", styles["h2"]),
        diagram_row(["Fixed body grille opening", "G0 removable guard", "One FS A/C pusher", "C0 condenser", "R0 radiator", "FL rear puller", "Engine"], styles),
        Spacer(1, 5 * mm),
        P("Radiator weight path", styles["h2"]),
        diagram_row(["R0 lower locators", "Two R1 saddles", "X1 seats", "X0 crossmember", "A0/A1 short arms", "Chassis connectors"], styles, PALE_AMBER),
        Spacer(1, 5 * mm),
        P("Non-negotiable rules", styles["h2"]),
        *bullets(
            [
                "The two lower locator/saddle points carry all filled-radiator weight. Tanks, seams, fins, soldered joints and upper ears carry none.",
                "R3-U upper keepers locate and restrain only; sleeve length controls EPDM compression and tightening must not unload either saddle.",
                "G0, C0, FS and FL use independent removable carriers. No heat exchanger or guard supports another.",
                "G1/G2 touch the repaired G0 perimeter frame only, never the mesh. F2 carries the FL shroud without loading R0 tanks or core.",
                "A0-L/R are loose parts: shorten or replace them on the bench to match actual connectors. No Rev A 410 mm / 4 mm dimensions, no Rev N X2 adapters and no unused tall projection.",
            ],
            styles,
        ),
        Spacer(1, 3 * mm),
        P("CL0 central alignment", styles["h2"]),
        data_table(
            [
                ["Interface", "Controlled centre", "Acceptance"],
                ["G0 to VCL", "Complete repaired G0 perimeter-frame outer-envelope centre vs vehicle longitudinal centre plane", "Lateral offset <= 2 mm"],
                ["FS to VCL", "Complete mounted FS frame/rotor datum vs vehicle longitudinal centre plane", "Lateral offset <= 2 mm"],
                ["C0 to VCL", "C0 usable-fin-field lateral centre vs vehicle longitudinal centre plane", "Lateral offset <= 2 mm"],
                ["Local G0 fit", "G0 perimeter-frame centre vs fixed body grille usable-aperture centre", "Offset <= 2 mm in X and Z"],
                ["Local FS fit", "FS frame/rotor datum vs C0 usable-fin-field centre", "Offset <= 2 mm in X and Z"],
            ],
            [41 * mm, 88 * mm, 41 * mm],
            styles,
            header_color=TEAL,
        ),
        Spacer(1, 4 * mm),
        callout("STOP condition", "Prove the G0 and FS direct VCL limits independently; do not tolerance-stack through the grille opening or C0. Show every tab, guard, plug, cable bend and service envelope, but do not substitute any of them for the specified frame/rotor centring datum. If CL0 cannot be met, revise the carriers.", styles, PALE_RED),
        PageBreak(),
    ]

    # Retained parts condition
    col = (CONTENT_W - 8) / 2
    story += page_title(
        "2. Retained parts - real condition evidence",
        "These photographs identify the actual retained parts and their starting condition. They are not dimensional evidence.",
        styles,
    )
    first_row = Table(
        [[
            photo_card(OLD_R0, "REAL BEFORE - R0 RADIATOR", "Removed copper/brass radiator. Retain tanks, headers, filler/cap neck, rails, ears and lower locators only where sound; replace the tired core.", col, 55 * mm, styles),
            photo_card(OLD_C0, "REAL BEFORE - C0 CONDENSER", "Full-face A/C condenser with pipes, drier and brackets. Clean, straighten and specialist leak-test; the old receiver-drier is reference geometry only.", col, 55 * mm, styles),
        ]],
        colWidths=[col, col],
    )
    first_row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    story += [first_row, Spacer(1, 4 * mm)]
    second_row = Table(
        [[
            photo_card(OLD_G0, "REAL BEFORE - G0 GUARD", "Original expanded-mesh guard and perimeter frame. Jig and repair the frame, preserve mesh open area and build new rubber-faced G1/G2 holders.", col, 55 * mm, styles),
            photo_card(OLD_R0_DAMAGE, "REAL DETAIL - R0 CORE", "Dirty, flattened and locally damaged fins support recoring rather than cosmetic repainting. Radiator-shop pressure/flow results control the retained-metal decision.", col, 55 * mm, styles),
        ]],
        colWidths=[col, col],
    )
    second_row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    story += [second_row, Spacer(1, 5 * mm)]
    story += [
        data_table(
            [
                ["Part", "Retain after", "Renewal work", "Release evidence"],
                ["R0", "Sound copper/brass tanks, headers, neck, rails, locators and classified ears", "Recore, compatible solder repair, R0-E work as released, thin heat-exchanger coating", "Before/after pressure and flow reports; R0-H map"],
                ["C0", "Sound body, pipes, ports and brackets after specialist assessment", "Neutral clean, fin comb, dry-nitrogen/forming-gas leak test, new drier and HNBR seals", "Written leak/cleanliness report; C0 map"],
                ["G0", "Sound repaired perimeter and acceptable open mesh", "Jig, straighten, repair, edge protect, thin satin/semi-gloss finish", "G0-H map, removal path and CL0 record"],
            ],
            [18 * mm, 50 * mm, 62 * mm, 40 * mm],
            styles,
        ),
        PageBreak(),
    ]

    # Fans/chassis condition
    story += page_title(
        "3. Fans and chassis interfaces - real evidence",
        "FS remains the one front A/C pusher candidate; FL remains the rear radiator puller/shroud.",
        styles,
    )
    fan_col = 57 * mm
    context_col = CONTENT_W - (fan_col * 2) - 8
    fan_grid = Table(
        [[
            photo_card(OLD_FS, "REAL BEFORE - FS", "Small front fan candidate. Retain only after complete-frame, polarity, current, rotation, direction and airflow checks.", fan_col, 72 * mm, styles),
            photo_card(OLD_FL, "REAL BEFORE - FL", "Large electric rear fan and shroud. Verify puller direction, frame depth, current and installed seal map.", fan_col, 72 * mm, styles),
            photo_card(OLD_CHASSIS, "REAL CONTEXT - HISTORICAL", "Front support and earlier tall-post context. Use only to understand the envelope. Rev P technical authority records the current arms as loose and unattached.", context_col, 72 * mm, styles),
        ]],
        colWidths=[fan_col, fan_col, context_col],
    )
    fan_grid.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    story += [fan_grid, Spacer(1, 5 * mm)]
    story += [
        callout(
            "Fan count",
            "One front A/C pusher does not mean one fan total. The controlled build retains one FS upstream of C0 and one FL puller behind R0. Each has a separate carrier, relay, fuse and earth branch.",
            styles,
            PALE_TEAL,
        ),
        Spacer(1, 5 * mm),
        P("Arm ownership correction", styles["h2"]),
        *bullets(
            [
                "Photograph both loose arm blanks before work and record left/right identity, section, thickness, straightness, corrosion, holes, cracks and prior heat damage.",
                "Make A0-D-L/R rigid templates from the intended structural chassis connector bearing planes and hole groups.",
                "Shorten loose parts on the bench, or replace with a certified matched steel pair. Never scale the historical photograph and never cut an installed chassis member as part of this work.",
                "Each finished A0 arm mates directly through its A1 connector end and stops at the highest assigned interface. No decorative post or water-trapping projection remains.",
            ],
            styles,
        ),
        Spacer(1, 4 * mm),
        callout("HOLD", "Arm grade, section, thickness, length, holes, bends, gussets, weld sizes, fasteners and torque remain on structural-drawing HOLD until the real connectors and loads are measured.", styles, PALE_AMBER),
        PageBreak(),
    ]

    # Renewed bench
    story += page_title(
        "4. Renewed target - complete parts set",
        "A photorealistic shop-layout concept showing the component families to restore, fabricate and buy.",
        styles,
    )
    story += [
        photo_card(RENEW_BENCH, "PHOTOREALISTIC RENEWED TARGET - NON-DIMENSIONAL", "Top row: G0, one FS, C0 with new drier, restored R0, and FL/shroud. Lower row: X0/X1, short A0/A1 arms, G1/G2, R3 holders, saddles, sleeved bushes, class 8.8 hardware and EPDM sealing. The render proposes appearance and organisation only.", CONTENT_W, 98 * mm, styles, renewed=True),
        Spacer(1, 5 * mm),
        data_table(
            [
                ["Disposition", "Parts"],
                ["Retain and professionally restore", "R0 copper/brass radiator, C0 full-face condenser, G0 guard, one FS pusher, FL puller/shroud"],
                ["Fabricate after measured release", "X0, X1-L/R, A0-L/R with A1-L/R, G1-L/R, G2-L/R, applicable R0-E, R3-U, optional R3-L, C1, F1, F2, E1"],
                ["Buy new", "R1 saddles, R2/R3-I EPDM and sleeves, H1 fasteners, S1 seals/edge trim, drier, seals, hoses, clamps, cap, thermostat, coolant and two fan circuits"],
            ],
            [43 * mm, 127 * mm],
            styles,
            header_color=TEAL,
        ),
        Spacer(1, 4 * mm),
        P("Appearance target: straight open fins, neat solder work, satin/semi-gloss coated steel, thin radiator-shop coating, clean zinc hardware, replaceable black EPDM interfaces, visible drainage and accessible service fasteners.", styles["body"]),
        PageBreak(),
    ]

    # Ten step plan
    story += page_title(
        "5. Ten-step execution plan",
        "Do not skip gates. Parts move to the next stage only when the named evidence is signed.",
        styles,
    )
    plan_rows = [
        ["Step", "Workshop action", "Evidence gate"],
        ["1", "Identify, tag, photograph and baseline-test R0, C0, G0, FS, FL, arm blanks and brackets. Cap all open ports.", "Signed retain / repair / replace decisions"],
        ["2", "Establish independent D00 first; then create A0-D, B0, S0, CL0, G0-H, R0-H, L0/MR, component maps, vehicle envelope and opaque 1:1 stack. Project VCL at the G0, FS and C0 mounting planes.", "Every bracket has a measured interface and assigned function"],
        ["3", "Jig R0; remove old core; clean/tin; fit naturally aspirated-duty core; complete R0-E work; pressure/flow test; thin coat.", "Square, tight, free-flowing R0 with written shop results"],
        ["4", "Neutral-clean and fin-comb C0; specialist dry-nitrogen/forming-gas leak test; cap ports; fit new drier and HNBR seals at assembly.", "Written clean/leak result"],
        ["5", "Repair G0 perimeter; qualify one FS and FL/shroud; establish direct G0-to-VCL, FS-to-VCL and C0-to-VCL datums plus the separate local fit checks.", "Safe direction/current and independent <= 2 mm CL0 results"],
        ["6", "Structurally design and fabricate X0/X1 plus short A0/A1 arms directly to actual connector templates.", "Competent-person signed structural drawing"],
        ["7", "Fabricate G1/G2, R3 and independent C1/F1/F2/E1 carriers with sleeved EPDM isolation.", "Tagged, independent, removable parts"],
        ["8", "Bare-metal full-stack dry fit using actual rubbers, fasteners, plugs, bends, hoses, pipes and service tools; measure every direct and local CL0 offset without tolerance stacking.", "Signed drawing, CL0 coordinate record and datum-referenced photos"],
        ["9", "Apply total 2 x MR proof for 10 minutes using released distribution/fixture; inspect; then deburr and coat.", "No set, crack, movement, displacement or distortion"],
        ["10", "Install cooling/A-C plumbing and two independent fan circuits; heat-cycle, hot-idle A/C test, road/load log and first-journey reinspection.", "No leak, rub, boil, purge, thermal escalation or witness-mark movement"],
    ]
    story += [
        data_table(plan_rows, [12 * mm, 105 * mm, 53 * mm], styles, font_style="table"),
        Spacer(1, 5 * mm),
        callout("Overall release status", "FINAL FIT + FABRICATION + PERFORMANCE RELEASE HOLD until all measurement, structural, proof, finish and commissioning gates pass.", styles, PALE_RED),
        PageBreak(),
    ]

    # Measurement controls
    story += page_title(
        "6. Steps 1-2 - baseline and measurement controls",
        "Measure complete parts from fixed vehicle datums before cutting final metal, buying final hoses, drilling, welding or coating.",
        styles,
    )
    measurement_rows = [
        ["Record", "Must capture", "Blocks"],
        ["D00", "Independent vehicle master datum: VCL plus fixed chassis X/Y/Z origin projected at the G0, FS, C0 and A0 planes; instrument, setup, method, repeatability and dated witness marks", "Every coordinate, centre offset and carrier"],
        ["A0-D-L/R", "Connector XYZ, bearing faces, hole centres/diameters, section/condition, thickness, bolt access, obstacles, drainage and removal sweep", "A0/A1 outline, holes and connection"],
        ["B0", "Upper radiator locating axes, planes, diameters and access", "R3-U geometry"],
        ["S0", "R0 lower locators, saddle centres/diameters and installed R1 height", "X1 geometry"],
        ["CL0", "VCL projected at G0, FS and C0 planes; complete G0 perimeter-frame outer-envelope centre; complete FS frame/rotor datum; C0 usable-fin-field centre; fixed body grille usable-aperture centre; separate direct and local offsets", "G1/G2, C1 and F1 alignment"],
        ["G0-H", "Complete removable guard frame envelope, sound contact lengths, planes/holes, mesh-to-fixed-vehicle-grille clearance, drainage and removal vector", "G1/G2"],
        ["R0-H", "Every ear, tab, rail and locator: XYZ, plane, hole, material/condition, original/added class, clearance and function", "R0-E, R3 and F2"],
        ["L0 / MR", "X0 clear span including A0/A1 envelopes; filled/capped installed radiator mass", "X0 structural design and proof load"],
        ["R0/C0/FS/FL", "Complete bodies, fittings, ports, tabs, motors, plugs, bends, seals and tool sweeps", "All carriers, hoses and wiring"],
        ["VEH", "Grille, bumper, bonnet/latch, steering, suspension, tow, support steel, engine movement, hoses, pipes, wiring and tools", "All fabrication"],
    ]
    story += [
        data_table(measurement_rows, [25 * mm, 100 * mm, 45 * mm], styles, font_style="table_small"),
        Spacer(1, 5 * mm),
        P("Baseline test sheet", styles["h2"]),
        data_table(
            [
                ["Item", "Record before work", "Retain decision"],
                ["R0", "Cold pressure, flow restriction, leak locations, fin/core condition, tank/header/neck/rail/ear state", "Radiator-shop signed retain/repair/recore scope"],
                ["C0", "External condition, contamination, fin damage, port/pipe/drier state, specialist test route", "A/C-shop clean/test/repair or replace decision"],
                ["FS / FL", "Voltage, start/run current, polarity, rotation, airflow direction, bearing noise, wobble, rub, plug/cable state", "Retain only if safe and suitable"],
                ["G0 / arms", "Frame/mesh soundness; arm material/section, straightness, corrosion, cracks, old holes and heat damage", "Repair/rework or replace decision"],
            ],
            [25 * mm, 99 * mm, 46 * mm],
            styles,
        ),
        Spacer(1, 4 * mm),
        callout("Required format", "Set D00 from fixed chassis references, not from the grille opening or another cooling component. Use a laser, tram bar, plumb/level or equivalent method capable of repeatable readings of 0.5 mm or better. Record three readings where practical. Use rigid, non-racking templates and a dated common-datum drawing. Photographs and renders can identify parts, but must never be scaled for cutting.", styles, PALE_AMBER),
        PageBreak(),
    ]

    # Measurement datum atlas
    story += page_title(
        "6A. Measurement datum atlas - front view",
        "Establish one independent vehicle centre plane, then measure each component directly to it.",
        styles,
    )
    story += [
        front_datum_diagram(),
        Spacer(1, 4 * mm),
        data_table(
            [
                ["Ref", "Put the measuring points here", "Record"],
                ["D00-VCL", "Project from fixed, repeatable chassis reference points at the G0, FS and C0 mounting planes. Do not derive VCL from the body opening, G0, C0 or fan.", "Origin points, instrument, setup, repeatability, signed distance to each plane"],
                ["W0", "Touch the left and right hard edges of the usable fixed body aperture at top, mid-height and bottom. Exclude rubber, mesh and temporary trim.", "Three widths plus edge condition; use the smallest usable width for packaging"],
                ["H0", "Touch the lower and upper hard edges at left, VCL and right. Record bonnet/latch and bumper/grille removal envelopes separately.", "Three heights plus obstacles and removal direction"],
                ["G0", "Measure outside-to-outside of the repaired perimeter frame at top/mid/bottom and left/centre/right. Do not measure the expanded mesh as the mounting datum.", "Frame W/H, diagonals, straight contact lengths, hole/plane map and centre"],
                ["FS", "Use the rotor axis and defined complete-frame datum. Separately record every tab, guard, plug and cable bend as an envelope.", "Rotor centre XYZ, frame envelope W/H/D and direct signed lateral offset to VCL"],
                ["C0", "Use the edges of the usable fin field for centre; then measure body, brackets, pipes, ports and tool sweep independently.", "Fin-field W/H and centre; total installed envelope W/H/D; direct lateral offset to VCL"],
                ["CL0 local", "Measure G0 centre to fixed-aperture centre, and FS frame/rotor datum to C0 fin-field centre. These are local checks, not substitutes for VCL.", "Separate signed X/Z offsets; each <= 2 mm; no chained calculation"],
            ],
            [23 * mm, 92 * mm, 55 * mm],
            styles,
            font_style="table_small",
        ),
        Spacer(1, 4 * mm),
        callout("Front-view acceptance", "G0 perimeter-frame centre, FS frame/rotor datum and C0 usable-fin-field lateral centre must each be within 2 mm of D00-VCL by separate direct measurements. Record the raw left/right readings as well as the calculated signed offset.", styles, PALE_TEAL),
        PageBreak(),
    ]

    story += page_title(
        "6A. Measurement datum atlas - side stack",
        "Locate every installed face directly from one fore/aft datum; never build the stack by adding estimated gaps.",
        styles,
    )
    story += [
        side_stack_diagram(),
        Spacer(1, 4 * mm),
        data_table(
            [
                ["Measure", "Exact endpoints / method", "Why it matters"],
                ["Y-G0 / Y-FS / Y-C0 / Y-R0 / Y-FL", "Perpendicular from D00-Y to the foremost and rearmost hard point of each complete installed assembly at left, VCL and right.", "Reveals tilt, depth and the true stack envelope without tolerance stacking"],
                ["Component depth", "Foremost-to-rearmost hard point of the complete assembly including frame, tabs, motor, plug, cable bend, neck, pipes and drier as applicable.", "Carrier position, bonnet/grille fit, fan and tool clearance"],
                ["Face gaps", "At the closest actual points between G0-FS, FS-C0, C0-R0 and R0-FL after final rubber and seals are fitted.", "Avoids rub, blocked fins and false nominal air gaps"],
                ["Service sweep", "From every cap, hose clip, fastener, A/C port, drier, plug and removal vector to the nearest fixed obstruction.", "Confirms tools and each component can be removed independently"],
                ["Engine movement", "From FL/shroud, hoses and wiring to the engine/fan-belt movement envelope under torque and through service removal.", "Prevents hot or moving contact"],
                ["Air seal", "Measure the FL shroud seal land around the sound R0 frame, including corner gaps and compression after fastener torque.", "Seals airflow without loading tanks, core or soldered joints"],
            ],
            [33 * mm, 94 * mm, 43 * mm],
            styles,
            font_style="table_small",
        ),
        Spacer(1, 4 * mm),
        callout("Record rule", "Enter each Y coordinate from D00, then calculate gaps as a check. Do not calculate a later plane from an earlier plane plus a nominal component depth or spacer.", styles, PALE_AMBER),
        PageBreak(),
    ]

    story += page_title(
        "6A. Measurement datum atlas - support and load path",
        "Measure the chassis connector bearing planes, saddles and radiator keeper axes only in their true loaded sequence.",
        styles,
    )
    story += [
        support_datum_diagram(),
        Spacer(1, 4 * mm),
        data_table(
            [
                ["Ref", "Where to measure", "Sequence / actual field"],
                ["A0-D-L/R", "Connector bearing face to D00 XYZ; every released hole centre and diameter from two orthogonal edges; local parent section/thickness; bolt head/nut/tool sweep.", "Template L ____  R ____  Date ____"],
                ["L0", "Between released left/right connector/end-envelope limit planes at the X0 level, including the A1 connection envelopes - not simply body width.", "Actual clear span ____ mm"],
                ["S0", "Centre and diameter of each R0 lower locator; centre and installed height of each final R1 saddle; left/right loaded seating plane.", "L XYZ ____  R XYZ ____  R1 height ____ mm"],
                ["MR", "Weigh the finished, capped R0 filled to installed operating level, including cap and retained fittings; record the scale and uncertainty.", "MR ____ kg; proof total = 2 x MR = ____ kg-equivalent"],
                ["B0", "With R0 naturally sharing weight across both R1 saddles, transfer each sound upper keeper interface axis/plane to fixed structure.", "L XYZ ____  R XYZ ____; no forced pull"],
                ["A0 height", "Connector bearing plane to X0 interface and to the highest released functional interface on each side. The finished arm stops there with no unused projection.", "L ____ mm  R ____ mm; derive after S0/B0"],
                ["R3 neutral witness", "After final torque, witness saddle seating at both R1 locations and measure any gap/load indication at R3-U; repeat after proof and first heat cycle.", "Both saddles loaded [ ]  Upper keeper neutral [ ]"],
            ],
            [25 * mm, 101 * mm, 44 * mm],
            styles,
            font_style="table_small",
        ),
        Spacer(1, 4 * mm),
        callout("Load-path hold", "The 2 x MR / 10 minute static proof is an acceptance test only. A competent structural release must separately cover vertical, fore/aft and lateral road loads, shock, vibration, fatigue, connector bearing, welds, fasteners and torque.", styles, PALE_RED),
        PageBreak(),
    ]

    # Provisional size schedule
    story += page_title(
        "6B. Provisional size schedule - component envelopes",
        "These estimates are for layout, cardboard/foam templates, shop discussion and quotation only. Replace every value with an actual reading.",
        styles,
    )
    story += [
        callout("DO NOT CUT OR ORDER FROM ESTIMATES", "No estimate on these pages releases metal cutting, drilling, welding, core ordering, hose selection, A/C pipework, fan cable/fuse sizing or coating. The actual stripped component, D00 coordinate record, rigid template and signed drawing always win.", styles, PALE_RED),
        Spacer(1, 4 * mm),
        data_table(
            [
                ["Item", "Planning estimate", "Confidence / source", "Take the actual measurement here", "Actual"],
                ["Fixed body opening W0", "640-670 mm usable width; height MEASURE", "Low; earlier packaging range", "Hard left/right edges at top, middle, bottom; upper/lower edges at left, VCL, right", "W top ____  mid ____  lower ____ mm; H ____"],
                ["R0 complete", "~635 mm wide x ~610 mm body high; cap/highest point ~635 mm; planning depth 70-100 mm", "Medium W/H from prior photo-measured mock-up; depth low-confidence allowance", "Outermost sound rails/tanks; base-to-body top and base-to-cap; foremost/rearmost hard points", "W ____ H ____ Hcap ____ D ____ mm"],
                ["R0 active face", "~590 x 510 mm", "Low-medium visual estimate", "First-to-last open tube/fin area, excluding tanks, headers and rails", "W ____ H ____ mm"],
                ["C0 body", "~540 x 465 mm; planning depth 20-30 mm", "Medium W/H from retained-part mock-up; depth allowance only", "Body edges, then separate overall bracket/drier/pipe/port/tool envelope", "Body W ____ H ____ D ____; overall ____"],
                ["G0 complete", "Planning envelope 620-650 x 570-610 x 15-30 mm", "Low; inferred only for card layout", "Repaired outer perimeter frame, not mesh; three widths/heights, diagonals and maximum depth", "W ____ H ____ D ____ diag ____ / ____ mm"],
                ["FS complete", "240-255 mm rotor ring; frame/tabs up to ~280 mm; planning depth 60-80 mm", "Medium ring/frame; depth low-confidence allowance", "Rotor diameter/axis; outermost frame/tabs/guard; motor/plug/cable-bend depth", "Ring ____ Frame W/H ____ / ____ D ____ mm"],
                ["FL complete", "450-480 mm ring; shroud height about 610 mm; planning depth 80-110 mm", "Medium ring/height; depth low-confidence allowance", "Ring, full shroud W/H/D, all tabs, plug/cable bend and seal land", "Ring ____ W ____ H ____ D ____ mm"],
                ["Initial C0-R0 spacer", "10-15 mm for opaque mock-up only", "Earlier packaging start value; not final clearance", "Closest point around full faces with pipes, brackets and final isolators installed", "Min L ____ C ____ R ____ mm"],
            ],
            [25 * mm, 39 * mm, 36 * mm, 45 * mm, 25 * mm],
            styles,
            font_style="table_small",
        ),
        Spacer(1, 4 * mm),
        P("Confidence legend: medium = prior photo-measured mock-up but still provisional; low = packaging allowance or visual inference. Neither is fabrication evidence.", styles["small"]),
        PageBreak(),
    ]

    story += page_title(
        "6B. Provisional size schedule - fabricated-part mock-ups",
        "Use these only to prepare card, plywood or foamboard trials and to estimate workshop effort; final metal details remain HOLD.",
        styles,
    )
    story += [
        data_table(
            [
                ["Ref", "Planning mock-up envelope", "Final measurement endpoints", "Final release remains"],
                ["X0", "Span planning range 640-700 mm. 40 x 40 x 3 mm mild-steel SHS may be used only as conditional mock-up stock if actual L0 <= 700 mm and MR <= 35 kg.", "A0/A1 released end-envelope plane to plane at X0 level; include X1 seats and drainage", "Section, span, end joints, welds and fasteners by structural drawing"],
                ["A0/A1 pair", "Start with 150-220 mm high x 50-70 mm wide card envelopes per side; no metal thickness or hole estimate", "Connector bearing plane/hole group to X0 interface and highest required interface, separately L/R", "Material/section, cut length, blank, bends, holes, welds, edge distance and torque"],
                ["X1-L/R", "60-80 mm square card footprint per saddle", "Final R1 base/support footprint, locator axis, drainage, X0 interface and loaded seat plane", "Plate/section, weld size and reinforcement"],
                ["G1-L/R", "70 x 50 mm folded-card blank; aim for 30-50 mm broad frame contact", "Sound straight G0 frame contact length/plane, escape lip, tool and withdrawal path", "Material, thickness, blank, bends, holes, EPDM and fasteners"],
                ["G2-L/R", "60 x 40 mm card blank; aim for 25-40 mm broad frame contact", "G0-H upper/side frame plane, removal vector and accessible positive-retention point", "Material, thickness, holes, EPDM, sleeve and fasteners"],
                ["R3-U-L/R", "60 x 40 mm card envelope; no hole or sleeve estimate", "B0 axis after R0 is seated, sound R0-H interface, rubber stack and tool sweep", "Section/thickness, hole, sleeve length, bolt, torque and neutral-load verification"],
                ["R3-L-L/R", "No part unless dry fit proves need; if needed, begin with 60 x 40 mm card", "Released side restraint interface and zero-vertical-load geometry", "Written need, material, joint, sleeve, fasteners and proof"],
                ["C1 / F1", "C1 local reach allowance 40-100 mm; F1 frame envelope about 280 mm; card tabs 30-60 mm reach", "C0/FS complete frame/tab maps, D00 planes, pipes/plugs, tool sweep and independent removal", "All material, sections, holes, joints, isolation and torque"],
                ["F2 / E1", "F2 perimeter mock-up about R0 outer envelope; E1 box sized only after actual relays/fuses/connectors", "R0 sound-frame seal map, FL tabs/depth; electrical component dimensions, bends and drainage", "Carrier section/joints/seal compression; E1 material, lid, glands and fixings"],
                ["EPDM trial pieces", "3-5 mm sheet/strip may be tried in mock-up; do not set sleeve length from nominal sheet", "Measure compressed stack with selected automotive EPDM sample and actual joint hardware", "Compound, hardness, thickness, compression, shoulder/crush sleeve and torque"],
            ],
            [21 * mm, 52 * mm, 55 * mm, 42 * mm],
            styles,
            font_style="table_small",
        ),
        Spacer(1, 4 * mm),
        callout("Revision method", "Write each actual value into the field sheets, update the 1:1 templates and revise the drawing register. Strike through superseded estimates - do not silently carry them into a cut list.", styles, PALE_AMBER),
        PageBreak(),
    ]

    # Visual work cards for every step
    work_cards = [
        (1, "Identify, protect and baseline", "Part ID, orientation, all ports, damage map and baseline pressure/flow/electrical readings.", "Tag L/R and front/rear; photograph; cap ports; inspect; test; decide retain/repair/replace.", "Every retained item has a signed condition decision and traceable before record."),
        (2, "Establish D00 and make templates", "Independent VCL/X/Y/Z, A0-D, B0, S0, CL0, G0-H, R0-H, L0/MR and complete envelopes.", "Project datums, take repeat readings, make rigid templates and an opaque 1:1 stack.", "Every bracket has direct measured endpoints; repeatability <= 0.5 mm; no scaled-photo value."),
        (3, "Recore and restore R0", "Tank/header/rail/neck geometry, locator map, core seat, pressure and flow before/after.", "Jig, desolder old core, clean/tin, repair sound retained metal, fit core, test, thin-coat.", "Square, leak-free, free-flowing R0; written shop report; no tank/core attachment load."),
        (4, "Restore C0 and G0", "C0 body/pipe/drier/tool envelope; G0 frame widths/heights/diagonals/contact lengths/removal vector.", "Neutral-clean and fin-comb C0; specialist leak test. Jig/repair G0; preserve mesh open area.", "C0 clean/capped/tested; G0 straight, central, rattle-free and independently removable."),
        (5, "Qualify and centre both fans", "FS/FL full frames, axes, tabs, depth, plug bends, direction, start/run current and direct CL0.", "Bench-test; keep FS pusher and FL puller; design separate carriers and protected circuits.", "One FS + one FL; correct direction; safe condition/current; FS directly within 2 mm of VCL."),
        (6, "Fabricate X0/X1 and short A0/A1", "Connector bearing planes/hole groups, L0, S0, B0, MR, arm height and road/service envelopes.", "Template first; structurally design; bench-cut loose arms; jig pair; weld/bolt to released drawing.", "Direct fit without force; no unused projection; signed structural release and inspection."),
        (7, "Fabricate all independent holders", "G0-H, R0-H, C0/FS/FL maps, contact/seal lengths, EPDM stack and removal/tool sweeps.", "Make G1/G2, R3, C1, F1, F2 and E1; sleeve clamped rubber; keep load paths separate.", "Broad replaceable contacts; R3-U neutral; no load through mesh, core, tank, fin or another component."),
        (8, "Complete opaque 1:1 dry fit", "Every direct D00 coordinate, face gap, clearance, service sweep, plug/hose/pipe bend and removal vector.", "Assemble in bare metal with actual rubbers and hardware; exercise bonnet, tools and engine movement envelope.", "All direct/local CL0 checks pass; no rub, force, slot, spacer stack or blocked service path."),
        (9, "Proof, inspect and finish", "MR, released saddle load split, pre/post datum readings, deflection, cracks/movement and coating exclusions.", "Apply total 2 x MR for 10 min without point loading; inspect; only then deburr, prep and coat.", "No permanent set/movement/damage; proof sheet signed; drains, earths, threads, cores and rubber seats uncoated."),
        (10, "Plumb, wire and commission", "Finished neck/port routes, hose and cable runs, measured fan current, voltage drop and thermal/A-C behaviour.", "Fit new hoses/drier/seals; two protected fan branches; bleed, heat-cycle, hot-idle A/C and road/load test.", "No leak/rub/purge/thermal escalation; currents stable; witness marks unchanged after first journey."),
    ]
    for card_index in range(0, len(work_cards), 2):
        pair = work_cards[card_index:card_index + 2]
        story += page_title(
            f"6C. Visual work cards - steps {pair[0][0]}-{pair[-1][0]}",
            "Diagrammatic sequence only; use the measurement atlas, actual parts and signed drawings for dimensions.",
            styles,
        )
        for step, title, measure, work, passed in pair:
            story.append(step_work_card(step, title, measure, work, passed, styles))
        story.append(PageBreak())

    # R0 recore
    story += page_title(
        "7. Step 3 - R0 radiator recore and restoration",
        "Recoring replaces the tube-and-fin core while preserving sound original copper/brass tanks, headers, neck, rails, locators and released ears.",
        styles,
    )
    r0_grid = Table(
        [[
            photo_card(OLD_R0_LEG, "REAL BEFORE - LOWER R0 DETAIL", "Historical added leg/lower support is a pattern/problem, not an approved new load path. Classify it through R0-H before shop rework; do not reproduce it.", col, 62 * mm, styles),
            photo_card(RENEW_HOLDERS, "RENEWED HOLDER TARGET - NON-DIMENSIONAL", "Target relationship: R0 rests in two lower rubber saddles; short sleeved upper keepers locate only; any R0-E ear work belongs to the radiator shop.", col, 62 * mm, styles, renewed=True),
        ]],
        colWidths=[col, col],
    )
    r0_grid.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    story += [r0_grid, Spacer(1, 4 * mm), P("What the radiator shop must do", styles["h2"])]
    story += numbered(
        [
            "Photograph, tag and baseline pressure/flow-test the complete R0; record retained-metal and interface condition.",
            "Build a rigid jig around tanks, headers, filler/cap neck, drain, side rails, lower locators and R0-H ear geometry.",
            "Desolder and remove the tired tube-and-fin core without distorting the retained parts.",
            "Clean and inspect tanks, headers, seams, neck, rails and locators; repair only sound copper/brass with inhibited solder-compatible chemistry.",
            "Have the recore specialist source or make a new naturally aspirated-duty copper/brass core after stripping and measuring the actual headers and tanks. Require an itemised construction and test quote; never buy a nominal catalogue core from a photograph.",
            "Tin and solder the new core squarely in the jig. Keep cap, drain, hose necks, lower locators and R0-H interfaces fixed.",
            "Retain, repair or reproduce R0-E side-rail ears only to the released R0-H class. Attach to sound rail/header support, never tank skin, tube, fin pack or core face.",
            "Complete all hot work before final testing. No chassis fabricator arc-welds to R0.",
            "Repeat pressure and flow tests, record results, straighten open fins and verify cap/neck/drain service access.",
            "Mask threads, neck seats, locators, earths and rubber interfaces; apply only a thin radiator-shop heat-exchanger coating. No powder coat, filler or thick primer.",
        ],
        styles,
    )
    story += [
        Spacer(1, 3 * mm),
        callout("R0 acceptance", "Square and dimensionally stable in the R0-H jig; pressure-tight; free-flowing; clean solder; straight open fins; sound released ears; written before/after pressure and flow results.", styles, PALE_TEAL),
        PageBreak(),
    ]

    # C0 and G0
    story += page_title(
        "8. Steps 4-5 - condenser and stone guard",
        "Restore both components independently; preserve full face area, direct VCL alignment, drainage and removal access.",
        styles,
    )
    cg_grid = Table(
        [[
            photo_card(OLD_C0, "REAL BEFORE - C0", "Retain the full-face condenser only after specialist cleaning and leak assessment. The old drier is never reused.", col, 54 * mm, styles),
            photo_card(OLD_G0, "REAL BEFORE - G0", "Repair the perimeter in a jig and preserve mesh open area. New holders act only on sound frame sections.", col, 54 * mm, styles),
        ]],
        colWidths=[col, col],
    )
    cg_grid.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    story += [cg_grid, Spacer(1, 4 * mm)]
    two_col = Table(
        [[
            [
                P("C0 specialist process", styles["h2"]),
                *bullets([
                    "Record the complete body, tabs, ports, pipes, drier, cable/tool/service envelope and C0 usable-fin-field centre.",
                    "Use neutral aluminium-safe coil cleaner, low-pressure clean-side rinse and a fin comb. Never use harsh brightener or a pressure jet.",
                    "Leak-test with dry nitrogen or forming gas at the applicable service pressure. Never use oxygen or wet shop air.",
                    "Cap clean ports. Fit a new compatible receiver-drier and new HNBR O-rings/seals/caps only at final assembly with the identified refrigerant oil.",
                    "Support C0 on independent C1 brackets with released isolation. Do not hang it from R0 or crop the full-face unit.",
                ], styles),
            ],
            [
                P("G0 repair process", styles["h2"]),
                *bullets([
                    "Measure G0-H first: full perimeter, straight sound contact lengths, frame planes/holes, mesh clearance, drainage, fixed-body-grille clearance and removal vector.",
                    "Jig and repair the perimeter frame; straighten/secure the mesh without reducing open area or leaving sharp edges.",
                    "Prepare rust locally and apply a thin compatible satin/semi-gloss black system. Keep mesh apertures, drains and fastener interfaces open.",
                    "Fit edge trim/anti-chafe where needed. G1/G2 must be removable and must never use point screws, self-tappers or through-core ties.",
                    "Use CL0 to place the complete repaired G0 perimeter-frame outer-envelope centre within 2 mm laterally of VCL. Separately keep it within 2 mm X/Z of the fixed body grille usable-aperture centre; do not tolerance-stack these checks.",
                ], styles),
            ],
        ]],
        colWidths=[col, col],
    )
    two_col.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("BOX", (0, 0), (-1, -1), 0.6, LINE), ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE)]))
    story += [two_col, Spacer(1, 5 * mm), callout("Acceptance", "C0: clean open fins, capped ports and written leak result. G0: straight sound perimeter, acceptable open mesh, central fit, rattle-free retention and unobstructed removal path.", styles, PALE_TEAL), PageBreak()]

    # Fans
    story += page_title(
        "9. Step 5 - one FS A/C pusher plus FL radiator puller",
        "Qualify both complete assemblies before final carriers or electrical sizing are released.",
        styles,
    )
    fan_rows = [
        ["Check", "FS front A/C pusher", "FL rear radiator puller/shroud"],
        ["Identity and structure", "Complete frame, tabs, guard, motor, label, plug and cable bend; exactly one FS", "Complete shroud, ring, tabs, motor, label, plug, cable bend and seal land"],
        ["Electrical", "Polarity, start current, stabilised current, voltage drop, connector temperature and earth", "Same checks on its own independent branch"],
        ["Mechanical", "No cracked blades/frame, rub, wobble, bearing noise or unsafe guard", "No crack, rub, wobble or bearing noise; secure independent shroud carrier"],
        ["Direction", "Pushes air rearward through C0 in its designed rotation", "Pulls air engineward through R0 in its designed rotation; do not casually reverse polarity"],
        ["Alignment", "Complete FS frame/rotor datum within 2 mm laterally of VCL and, separately, within 2 mm X/Z of C0 usable-fin-field centre; no tolerance stacking", "Seal to R0 frame without tank/core load; preserve hose, cap, drain and tool access"],
        ["Retention", "F1 removable carrier; no through-core ties", "F2 removable carrier with closed-cell EPDM perimeter seal"],
    ]
    story += [data_table(fan_rows, [28 * mm, 71 * mm, 71 * mm], styles)]
    story += [Spacer(1, 5 * mm)]
    check_col = CONTENT_W / 2
    checks = Table(
        [[
            [
                P("Bench test record", styles["h2"]),
                *bullets([
                    "Supply voltage at fan terminals",
                    "Start current and stabilised run current",
                    "Polarity and rotation",
                    "Airflow direction and credible installed airflow",
                    "Vibration, bearing noise, rub and motor temperature",
                    "Plug, terminal, seal and cable-bend condition",
                ], styles),
            ],
            [
                P("Installation record", styles["h2"]),
                *bullets([
                    "Independent carrier and service removal",
                    "Separate sealed relay, fuse and earth",
                    "Cable sizing from measured current and run length",
                    "Voltage drop and current at operating temperature",
                    "No contact through engine movement or fan run-on",
                    "Labels, vents, blades, motors, plugs and rubber unpainted",
                ], styles),
            ],
        ]],
        colWidths=[check_col, check_col],
    )
    checks.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOX", (0, 0), (-1, -1), 0.6, LINE), ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story += [checks, Spacer(1, 5 * mm), callout("Retain gate", "Both fans must have safe current and direction, no crack/wobble/rub, serviceable connectors and credible installed airflow. Replace any unsafe or unverified assembly before carrier release.", styles, PALE_AMBER), PageBreak()]

    # Arms fabrication
    story += page_title(
        "10. Step 6 - crossmember and shortened connector arms",
        "Purpose-size the loose arms to the real connector bearing planes and the highest required functional interface.",
        styles,
    )
    story += [
        photo_card(RENEW_DRYFIT, "PHOTOREALISTIC BARE-METAL DRY-FIT TARGET - NON-DIMENSIONAL", "Short mirror-handed A0/A1 arms mate directly at measured chassis connectors and support X0/X1. No tall unused upright and no X2 adapter. The visible shapes are concept only; A0-D, S0, L0/MR and a signed structural drawing control fabrication.", CONTENT_W, 82 * mm, styles, renewed=True),
        Spacer(1, 4 * mm),
    ]
    arm_steps = [
        ["Stage", "Fabrication requirement"],
        ["Template", "Make rigid A0-D-L/R connector templates and a full-size arm/card template from fixed chassis datums."],
        ["Inspect blanks", "Record material, actual section/thickness, straightness, corrosion, cracks, old holes and prior heat damage. Reject or replace if uncertain."],
        ["Mark", "Mark connector bearing plane, X0 centreline, highest assigned interface and final cut line on each loose blank."],
        ["Shorten", "Bench-cut only. Remove redundant returns, holes and projection. Provide a released closure/drain arrangement for any tubular cut."],
        ["A1 ends", "Form or fit integral drawing-released connector shoes. No improvised side tab, loose spacer stack, new chassis hole, slotting, reaming or forced pull."],
        ["Jig and join", "Jig the mirror-handed pair from fixed datums. Use verified parent steel, matching consumables and the approved WPS."],
        ["Inspect", "Inspect weld profile/HAZ and connector bearing/edge distance. Trial-fit using the final hardware stack without forced alignment."],
        ["Release", "Competent automotive structural review must cover vertical, fore/aft and lateral road loads, shock, vibration, fatigue, material, connector bearing, welds, fasteners, torque and proof fixture."],
    ]
    story += [data_table(arm_steps, [28 * mm, 142 * mm], styles), Spacer(1, 4 * mm)]
    story += [callout("X0 provisional stock rule", "40 x 40 x 3 mm mild-steel SHS is mock-up stock only if measured L0 <= 700 mm and MR <= 35 kg. Final X0 section, span and end connections still require structural release.", styles, PALE_AMBER), PageBreak()]

    # Guard holders
    story += page_title(
        "11. Step 7 - new grille/stone-guard holders",
        "G1/G2 hold only the sound repaired G0 perimeter, centre it directly on VCL, prevent rattle and preserve quick removal.",
        styles,
    )
    story += [
        photo_card(RENEW_HOLDERS, "PHOTOREALISTIC HOLDER DETAIL - NON-DIMENSIONAL", "The left side illustrates rubber-faced guard cradles/keepers; the right side illustrates the separate radiator and shroud holder systems. Use the image to communicate function, not cut sizes.", CONTENT_W, 78 * mm, styles, renewed=True),
        Spacer(1, 4 * mm),
    ]
    holder_rows = [
        ["Ref", "Function", "Fabrication specification", "Control / acceptance"],
        ["G1-L/R", "Two lower guard-frame cradles", "Mirror-handed removable folded brackets; broad EPDM-lined contact; formed return/lip against fore/aft escape; low-point drainage; locate complete G0 frame directly from VCL", "G0-H sound straight perimeter only; G0-to-VCL and local aperture checks pass; no denting, mesh clamp, point screw, self-tapper or through-core tie"],
        ["G2-L/R", "Two upper/side keepers", "Removable positive retention with captive/locking hardware; replaceable EPDM and edge trim; fasteners accessible through released service sequence; preserve direct VCL position", "No rattle or lift; complete guard withdraws along G0-H vector without fixed-grille/fan interference"],
        ["Carrier points", "Independent front support", "Mount to released front-support/A0 carrier points, independent of R0, C0 and both fans", "No heat exchanger/core/mesh carries another part"],
        ["Material", "Default shop route", "Folded coated mild steel; aluminium only under a galvanically isolated signed design", "Exact material, thickness, blank, bends, holes and fasteners remain HOLD"],
        ["Alignment", "Centre complete G0", "Reference VCL directly on the holder drawing and set the complete repaired perimeter-frame outer envelope, not the mesh insert", "G0 centre within 2 mm laterally of VCL and separately within 2 mm X/Z of fixed body grille usable-aperture centre; no stacking"],
    ]
    story += [data_table(holder_rows, [18 * mm, 34 * mm, 69 * mm, 49 * mm], styles, font_style="table_small"), Spacer(1, 4 * mm)]
    story += [callout("Finish requirement", "Deburr all edges, preserve drains and tool paths, coat with the released compatible system and fit replaceable EPDM only after full cure. Do not coat threads, bearing faces or rubber seats.", styles, PALE_TEAL), PageBreak()]

    # Radiator holders
    story += page_title(
        "12. Step 7 - new radiator and rear-shroud holders",
        "R0 remains lower-supported and naturally seated; upper and side devices restrain without adding vertical load.",
        styles,
    )
    rad_rows = [
        ["Ref", "Qty", "Required design", "Critical prohibition / gate"],
        ["R1-L/R", "2 bought", "New J40-pattern lower rubber saddles matched to locator diameter, cup depth, installed height, load area and compound", "Old rubber is pattern only; both saddles must fully seat and share weight"],
        ["X1-L/R", "2 make", "Released structural seats for the selected R1 samples with drainage and correct saddle support", "No metal contact to locator/tank/core; geometry from S0"],
        ["R0-E", "As needed", "Radiator-shop retain/repair/reproduce only a released sound side-rail/header-support ear in the R0-H jig", "Never attach to tank skin, tube, fin pack or core face; hot work before final pressure/flow test"],
        ["R3-U-L/R", "2 make", "Short vehicle-side keepers with EPDM bush, fitted steel crush sleeve, broad washer, released zinc class 8.8 bolt and locknut", "Locator/restraint only; tightening must not lift, pull, rack, twist or unload R1"],
        ["R3-L-L/R", "0 or 2", "Optional sleeved-EPDM lower-side stabilisers only when R0-H and dry fit prove need", "Fore/aft/lateral restraint only; no vertical load; historical added leg is not reproduced"],
        ["F2", "1 set", "Independent removable FL/shroud carrier aligned to R0 side-rail/seal map with closed-cell EPDM perimeter seal", "No tank, core, soldered-ear or fin load; cap, drain, hoses, fins and tools remain serviceable"],
    ]
    story += [data_table(rad_rows, [19 * mm, 18 * mm, 87 * mm, 46 * mm], styles, font_style="table_small")]
    story += [Spacer(1, 5 * mm), P("Assembly order", styles["h2"])]
    story += numbered(
        [
            "Fit final R1 samples in X1 and confirm S0 locator/saddle geometry.",
            "Lower R0 naturally onto both saddles with no metal, tank, seam or core contact.",
            "Confirm equal seating and weight sharing before transferring B0/R0-H to R3-U.",
            "Fit crush-sleeved EPDM joints and tighten to the released stack/torque without compressing rubber beyond sleeve control.",
            "Witness-check that neither saddle unloads and R0 does not rack, twist or rise.",
            "Add R3-L only with written justification; fit F2 independently and seal the shroud to the R0 frame.",
        ],
        styles,
    )
    story += [Spacer(1, 4 * mm), callout("No spacer stacks", "Do not correct alignment with loose washers or improvised spacers. Correct the released bracket or connector geometry and repeat the dry fit.", styles, PALE_RED), PageBreak()]

    # Dry fit proof finish
    story += page_title(
        "13. Steps 8-9 - 1:1 dry fit, proof and finish",
        "Complete every fit, clearance and load check in bare metal before irreversible coating or final assembly.",
        styles,
    )
    story += [
        photo_card(RENEW_DRYFIT, "PHOTOREALISTIC DRY-FIT TARGET - NON-DIMENSIONAL", "The temporary vertical datum illustrates VCL through the G0 frame and FS rotor. It is not measurement proof. Use actual parts, rubbers, final hardware, service envelopes and a recorded physical CL0 datum for release.", CONTENT_W, 70 * mm, styles, renewed=True),
        Spacer(1, 4 * mm),
    ]
    dry_rows = [
        ["Dry-fit check", "Pass condition"],
        ["Weight path", "Both R1 saddles share R0 weight; R3-U stays neutral; R3-L is N/A or unloaded vertically"],
        ["CL0", "G0 frame, FS frame/rotor and C0 fin field each meet their independent <= 2 mm lateral VCL limit; separate G0-to-fixed-grille and FS-to-C0 X/Z offsets each meet <= 2 mm; no tolerance stacking"],
        ["Air and seals", "FS pushes rearward; FL pulls engineward; FL shroud seals to R0 frame without blocking fins"],
        ["Clearance", "Grille, bumper, bonnet/latch, steering, suspension, tow, engine movement, hoses, pipes, wiring and tools clear"],
        ["Service", "G0, C0, R0, FS and FL remove independently in the documented sequence; cap/drain/hoses/fasteners accessible"],
        ["Alignment", "No forced pull, new chassis holes, slotting, reaming, loose spacer stacks or distorted rubber"],
    ]
    story += [data_table(dry_rows, [40 * mm, 130 * mm], styles), Spacer(1, 5 * mm)]
    proof_box = Table(
        [[P("PROOF LOAD", styles["callout_title"]), P("Apply a total static load of 2 x MR, distributed between the two S0 saddle centres in the released loaded-radiator distribution, for 10 minutes. The released fixture must avoid local point-loading.", styles["body"])],
         [P("FAIL FOR", styles["callout_title"]), P("Permanent set, crack, connector or fastener movement, saddle displacement, arm distortion, looseness or loss of alignment.", styles["body"])]],
        colWidths=[28 * mm, 142 * mm],
    )
    proof_box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE_AMBER), ("BOX", (0, 0), (-1, -1), 0.9, COPPER), ("INNERGRID", (0, 0), (-1, -1), 0.5, COPPER), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story += [proof_box, Spacer(1, 5 * mm), P("Finish sequence after proof passes", styles["h2"])]
    story += bullets(
        [
            "Deburr and radius exposed edges; dress only as allowed by the released drawing and weld acceptance.",
            "Degrease; isolate/localise ferrous rust preparation; preserve drains and cavity access.",
            "Apply compatible 2K epoxy and 2K polyurethane satin/semi-gloss to steel. Use professional spray controls and follow SDS.",
            "Apply cavity wax only to eligible closed steel after full cure and without blocking drainage.",
            "Keep threads, earths, connector bearing faces, rubber seats, cores, fins, labels, motors and seals free of coating.",
        ],
        styles,
    )
    story += [PageBreak()]

    # Plumbing, wiring, commissioning
    story += page_title(
        "14. Step 10 - plumbing, A/C, wiring and commissioning",
        "Use new service parts sized from the measured finished stack and keep the two fan circuits independent.",
        styles,
    )
    install_rows = [
        ["System", "Install new", "Control / verification"],
        ["Engine cooling", "Measured moulded upper/lower hoses, overflow hose, constant-tension clamps, approved cap, Toyota 2H thermostat/seal, one compatible long-life coolant family and deionised water as required", "No unknown donor cap/stat/hoses; route clear of fan, belt, sharp edges and engine movement; pressure/heat-cycle and bleed to maker procedure"],
        ["A/C", "Compatible receiver-drier, new HNBR O-rings/seals/caps and exact matched refrigerant oil", "Specialist evacuation/charge; no reused old drier, mixed oil, oxygen/wet-air test or refrigerant venting"],
        ["FS circuit", "Sealed relay, fuse, measured cable, terminals/connectors, earth hardware, heat-shrink, grommets, loom and P-clips", "Separate branch sized from measured FS current/run length; voltage-drop/current/direction/temperature record"],
        ["FL circuit", "Separate sealed relay, fuse and equivalent complete branch", "No shared unprotected feed; verify puller direction and shroud seal at operating temperature"],
        ["E1 carrier", "Splash-resistant removable cover and rear/down cable exits", "Drainable orientation, accessible fuses/relays and protected bends; no water-trapping side annex"],
    ]
    story += [data_table(install_rows, [31 * mm, 78 * mm, 61 * mm], styles, font_style="table_small")]
    story += [Spacer(1, 5 * mm), P("Commissioning sequence", styles["h2"])]
    story += numbered(
        [
            "Cold static inspection: torques, witness marks, earths, clamps, drain access, clearance and fan guards.",
            "Pressure-check cooling system, evacuate/charge A/C professionally and confirm capped/clean service ports.",
            "Run FS and FL separately: record terminal voltage, voltage drop, start/run current, direction, noise, vibration and connector temperature.",
            "Heat-cycle the 2H, bleed to the coolant maker procedure and inspect every hose, seam, drain, cap and bracket through cool-down.",
            "Hot-idle with A/C at intended ambient: require stable coolant and A/C high-side behaviour with no rub, purge or wiring heat.",
            "Road/load log the naturally aspirated vehicle; recheck after cool-down and after the first loaded journey.",
        ],
        styles,
    )
    story += [Spacer(1, 4 * mm), callout("Final operating gate", "No leak, rub, boil, purge, progressive coolant rise, progressive A/C high-side escalation, abnormal fan current/temperature or witness-mark movement.", styles, PALE_TEAL), PageBreak()]

    # Fabricated parts schedule
    story += page_title(
        "15. Fabricated parts schedule",
        "All final numerical dimensions, materials, welds, fasteners and torques remain HOLD until their named controls and signed drawings are complete.",
        styles,
    )
    make_rows = [
        ["Ref", "Qty", "Make", "Provisional guidance", "Final control"],
        ["X0", "1", "Full-width lower crossmember", "40 x 40 x 3 mild-steel SHS only as conditional mock-up stock", "L0/MR and structural drawing release section, span and A0 connections"],
        ["X1-L/R", "2", "Lower saddle seats", "Released structural steel plate/section", "S0, selected R1, drainage and calculation"],
        ["A0-L/R", "2 assys", "Shortened connector arms", "Verified loose blanks or certified weldable structural steel", "A0-D, L0, R0-H, connector and road-load calculation"],
        ["A1-L/R", "2", "Integral connector shoes/end fittings", "Released matching structural steel", "Connector bearing/hole map, edge distance and weld/bolt design"],
        ["G1-L/R", "2", "Lower G0 frame cradles", "Folded coated mild steel by default; thickness HOLD", "G0-H; direct G0-frame-to-VCL plus separate fixed-aperture CL0 checks; drainage/removal"],
        ["G2-L/R", "2", "Upper/side G0 keepers", "Compatible coated section with EPDM contact", "Preserve direct G0-to-VCL position and accessible positive retention"],
        ["R0-E", "As reqd", "Radiator-side ear/tab work", "Radiator-shop copper/brass-compatible process", "R0-H jig; post-hot-work pressure/flow test"],
        ["R3-U-L/R", "2", "Upper radiator keepers", "Released coated mild-steel plate/section", "B0/R0-H after natural seating on final R1"],
        ["R3-L-L/R", "0 or 2", "Optional lower-side stabilisers", "Released coated mild-steel plate/section", "R0-H plus dry-fit justification; no vertical load"],
        ["C1", "Measured", "Independent condenser brackets", "Compatible isolated steel/aluminium", "C0 map; direct C0-fin-field-to-VCL CL0; ports, pipes and tool sweep"],
        ["F1", "1 set", "Single-FS carrier", "Released compatible section", "Direct complete-FS-frame/rotor-to-VCL plus separate FS-to-C0 CL0 checks; no stacking"],
        ["F2", "1 set", "FL carrier and seal land", "Released compatible section", "FL/R0-H seal maps; zero tank/core load"],
        ["E1", "1", "Relay/fuse carrier", "Coated metal with removable splash-resistant cover", "Electrical/service/drainage map"],
    ]
    story += [data_table(make_rows, [17 * mm, 15 * mm, 43 * mm, 49 * mm, 46 * mm], styles, font_style="table_small"), Spacer(1, 4 * mm)]
    story += [callout("Drawing issue requirement", "Every fabricated item must carry a unique revision, material, quantity, hole/bend/weld definition, finish, interface reference and inspection point. Do not release a cut list from this PDF alone.", styles, PALE_RED), PageBreak()]

    # Buy schedule
    story += page_title(
        "16. Bought core, fittings and service parts",
        "Use a shop-measured replacement core plus new automotive-grade isolation, hardware, seals, hoses and electrical parts selected from the measured finished assembly.",
        styles,
    )
    buy_rows = [
        ["Ref / group", "Qty", "Buy new", "Selection control"],
        ["R0 core / recore service", "1", "Radiator-shop-sourced copper/brass core, soldering, pressure test and flow test", "Order only after strip/measurement of actual tanks and headers; itemise construction, duty basis and written before/after test results"],
        ["R1-L/R", "2", "Toyota/J40-pattern lower radiator rubber saddles", "Actual locator diameter, cup depth, installed height, load area and compound"],
        ["R2/R3-I", "As drawn", "Automotive EPDM bushes/strips plus fitted crush and shoulder sleeves", "Every clamped rubber stack positively sleeve-controlled; compatible with heat/coolant/finish"],
        ["H1", "1 set", "Zinc-plated class 8.8 bolts, broad washers and positive/prevailing locknuts", "Released diameter, pitch, grip length, torque and locking; do not mix unidentified grades"],
        ["S1", "Measured", "Closed-cell automotive EPDM shroud seal, guard anti-chafe and edge trim", "No fin/drain/fastener blockage; serviceable and replaceable"],
        ["Cooling service", "Measured", "Moulded coolant hoses, overflow hose, constant-tension clamps, cap, 2H thermostat/seal, compatible coolant and DI water", "Final R0 neck map, pressure rating, routing and one known coolant family"],
        ["A/C service", "1 set", "Compatible receiver-drier, HNBR seals/caps and identified refrigerant oil", "C0/A-C system identity; new drier only"],
        ["FS electrical", "1 branch", "Sealed relay/fuse, cable, terminals/connectors, earth, loom, heat-shrink, grommets and P-clips", "Measured FS current, run length, voltage drop, environment and service access"],
        ["FL electrical", "1 branch", "Separate equivalent protected branch", "Measured FL current and run length; independent protection and earth"],
    ]
    story += [data_table(buy_rows, [26 * mm, 19 * mm, 72 * mm, 53 * mm], styles, font_style="table_small")]
    story += [Spacer(1, 5 * mm), P("Hardware stack rules", styles["h2"])]
    story += bullets(
        [
            "Use broad washers against released bracket faces and positive/prevailing locking exactly as drawn.",
            "Crush-sleeve length controls rubber compression; bolt torque must not crush EPDM or distort a holder.",
            "Keep grip length through the joint; avoid threads bearing in critical shear planes unless the signed design permits it.",
            "Use compatible isolation where aluminium and steel meet. Keep bearing faces clean and dry unless the drawing specifies otherwise.",
            "Mark final torques and apply visible witness marks after acceptance.",
        ],
        styles,
    )
    story += [Spacer(1, 4 * mm), callout("Procurement hold", "Do not buy the core, final hoses, sleeves or bracket hardware from nominal dimensions. Purchase against the stripped/measured R0 and the released R0/C0/FS/FL maps and joint drawings.", styles, PALE_AMBER), PageBreak()]

    # Chemicals
    story += page_title(
        "17. Chemicals, coatings and consumables",
        "Use only substrate-compatible products with current SDS and the correct professional controls.",
        styles,
    )
    chem_rows = [
        ["Product class", "Use", "Selection / control", "Never"],
        ["Water-based degreaser", "Steel, guard, washable externals", "Substrate-compatible; pH-neutral around aluminium", "Immerse motors/connectors or leave ports open"],
        ["Inhibited radiator cleaner/descaler", "R0 shop clean", "Explicit copper/brass and actual-solder compatibility", "DIY strong acid/caustic or abrasive blast"],
        ["Neutral condenser cleaner", "C0 fins", "Aluminium-safe, low residue, low-pressure clean-side rinse", "Harsh brightener or pressure jet"],
        ["70-90% IPA", "Compatible bracket wipe", "Spot-test and allow full evaporation", "Soak rubber, labels, motors or electrics"],
        ["Phosphoric steel prep", "Local isolated ferrous rust", "Use within one compatible coating system", "Contact aluminium, cores, copper/brass, solder or rubber"],
        ["2K epoxy + 2K polyurethane", "A0/X0/X1/G1/G2/R3 and carriers", "Compatible satin/semi-gloss system; professional controls and SDS", "Coat fins, threads, earths, drains, bearing faces or rubber seats"],
        ["Thin radiator coating", "R0 only", "Radiator-shop heat-exchanger product and application", "Powder coat, filler or thick primer"],
        ["Cavity wax", "Eligible closed steel after cure", "Drain-aware compatible wand product", "Earths, rubbers, threads, cores or uncured paint"],
        ["EPDM-safe assembly aid", "Rubber assembly", "Verified compatible; minimal residue", "Petroleum grease on EPDM"],
        ["Dielectric grease", "Connector seal lips/boots", "Light film after sound crimping", "Between electrical contact faces"],
        ["Identified refrigerant oil", "New HNBR seals", "Exact refrigerant/oil match", "Mix oils or reuse old drier"],
        ["Compatible long-life coolant", "Final fill", "One known family and maker procedure", "Mix unknown coolant families"],
    ]
    story += [data_table(chem_rows, [35 * mm, 35 * mm, 60 * mm, 40 * mm], styles, font_style="table_small"), Spacer(1, 4 * mm)]
    story += [
        callout("Workshop safety", "Use weld consumables matched to verified parent steel and the approved WPS. Never weld near chlorinated-cleaner residue, pressure-test A/C with oxygen, vent refrigerant or spray 2K products without the specified professional controls and respiratory protection.", styles, PALE_RED),
        PageBreak(),
    ]

    # Release and sources
    story += page_title(
        "18. Release checklist, sign-off and provenance",
        "All seven release gates must be signed before the build is treated as final.",
        styles,
    )
    release_rows = [
        ["Gate", "Pass requirement", "Evidence", "Status / initials"],
        ["1. Components", "R0 pressure/flow; C0 leak/cleanliness; FS/FL electrical, direction and condition pass", "Shop reports and baseline sheets", "[ ]"],
        ["2. Measurements", "Independent D00, A0-D, B0, S0, CL0, G0-H, R0-H, L0/MR and all envelopes signed; direct G0/FS/C0-to-VCL and separate local <= 2 mm offsets pass without stacking", "Templates, coordinate table, instrument/repeatability record and dated datum-referenced drawings/photos", "[ ]"],
        ["3. Structure", "X0/X1/A0/A1, connectors, welds, fasteners, torque and proof fixture released", "Competent-person signed calculation/drawing", "[ ]"],
        ["4. Holders", "G1/G2 touch only G0 frame; R3 uses sound R0 interfaces; all carriers independent and removable; no core load", "Holder drawings and dry-fit witness", "[ ]"],
        ["5. Fit and proof", "Opaque bare-metal dry fit passes; total 2 x MR / 10 min proof passes", "Signed photos, proof sheet and before/after measurements", "[ ]"],
        ["6. Finish and assembly", "Finish, hardware, plumbing and separate fan circuits pass", "Finish, torque and electrical inspection sheets", "[ ]"],
        ["7. Performance", "Hot-idle A/C, naturally aspirated road/load cooling and first-journey reinspection pass", "Logged commissioning and reinspection", "[ ]"],
    ]
    story += [data_table(release_rows, [22 * mm, 86 * mm, 45 * mm, 17 * mm], styles, font_style="table_small")]
    story += [Spacer(1, 5 * mm)]
    sign_rows = [
        ["Role", "Name", "Signature", "Date"],
        ["Owner", "", "", ""],
        ["Radiator shop", "", "", ""],
        ["A/C specialist", "", "", ""],
        ["Fabricator", "", "", ""],
        ["Structural reviewer", "", "", ""],
        ["Commissioning witness", "", "", ""],
    ]
    sign_table = Table([[P(c, styles["table_header"] if r == 0 else styles["sign"]) for c in row] for r, row in enumerate(sign_rows)], colWidths=[42 * mm, 43 * mm, 55 * mm, 30 * mm], rowHeights=[8 * mm] + [10 * mm] * 6)
    sign_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE), ("GRID", (0, 0), (-1, -1), 0.55, LINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    story += [sign_table, Spacer(1, 5 * mm)]
    story += [P("Controlled sources and image provenance", styles["h2"])]
    story += bullets(
        [
            "This Rev Q illustrated measurement plan supplements, but does not supersede, technical authority docs/J40-naturally-aspirated-cooling-pack-restoration-guide-rev-p-20260816.md.",
            "Fabrication handoff: data/manual/fabrication/na_cooling_connector_arms_rev_p/README.md, fabricator_cut_list.csv, measurement_basis.csv and inspection_checklist.csv.",
            "Real condition images: retained R0, C0, G0, FS and FL photo references in the controlled front-cooling-stack asset set, plus dated project photos for R0 core and chassis context.",
            "Renewed images: Rev P photorealistic portal assets. The installed views deliberately show the direct-centreline intent, but remain explanatory and non-dimensional; only CL0 records prove alignment.",
            "Superseded: Rev A nominal 410 mm / 4 mm upright package; Rev N X2-adapter arrangement; turbo/intercooler/K0 and second-front-fan layouts.",
        ],
        styles,
    )
    story += [Spacer(1, 4 * mm), callout("Controlled final status", "FINAL FIT + FABRICATION + PERFORMANCE RELEASE HOLD until every row above is signed and the evidence package is complete.", styles, PALE_RED)]
    return story


def build_story_rev_r(styles):
    """Fabrication-focused issue using real evidence and blank actual-measurement fields."""
    story = []
    col = (CONTENT_W - 8) / 2

    # Cover: real retained parts, not a concept render.
    story += [
        Spacer(1, 4 * mm),
        P("CONTROLLED WORKSHOP PLAN | REV R", styles["cover_kicker"]),
        P("J40 cooling-pack refurbishment and fabrication", styles["cover_title"]),
        P("Actual-part references, measurement capture, recoring and restoration steps, fabricated mounting interfaces, finish controls and budget", styles["cover_sub"]),
    ]
    cover_photos = Table(
        [[
            photo_card(
                OLD_R0,
                "ACTUAL RETAINED R0",
                "Removed copper/brass radiator. The old core is not the dimensional authority for a replacement until the radiator shop strips and measures the tanks and headers.",
                col,
                64 * mm,
                styles,
            ),
            photo_card(
                OLD_C0,
                "ACTUAL RETAINED C0",
                "Removed full-face condenser. The complete installed envelope includes brackets, pipes, ports and the receiver-drier, not just the fin field.",
                col,
                64 * mm,
                styles,
            ),
        ]],
        colWidths=[col, col],
    )
    cover_photos.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story += [
        cover_photos,
        Spacer(1, 5 * mm),
        callout(
            "Configuration",
            "Toyota 2H naturally aspirated. No turbocharger, intercooler/K0, charge-air pipework or second small front fan. The finished pack has one central FS front A/C pusher and one FL rear radiator puller/shroud.",
            styles,
            PALE_TEAL,
        ),
        Spacer(1, 4 * mm),
        callout(
            "Dimensional status",
            "The project record contains no released actual R0, C0, G0, FS, FL, chassis-interface, arm or holder dimensions. Rev R therefore removes the former planning estimates. Blank ACTUAL fields below must be completed from the stripped parts and vehicle before any final cutting, drilling, welding, core order or hose order.",
            styles,
            PALE_RED,
        ),
        Spacer(1, 4 * mm),
        data_table(
            [
                ["Technical authority", "Fabrication state", "Issue date"],
                ["Rev P naturally aspirated cooling-pack guide and Rev P handoff package", "MEASURED STRUCTURAL RELEASE HOLD", "16 Aug 2026"],
            ],
            [82 * mm, 58 * mm, 30 * mm],
            styles,
            header_color=TEAL,
        ),
        PageBreak(),
    ]

    story += page_title(
        "1. What is controlled now",
        "These are acceptance requirements or conditional starting rules. They are not measurements of the retained parts.",
        styles,
    )
    controlled_rows = [
        ["Control", "Numeric requirement", "Meaning / fabrication consequence"],
        ["Direct centreline", "G0, FS and C0 each within 2 mm of VCL", "Measure each independently from the fixed chassis master datum. Do not derive one component centre from another."],
        ["Local alignment", "G0-to-fixed grille aperture and FS-to-C0 each within 2 mm in X and Z", "Separate local checks; they do not replace the direct VCL readings and cannot be tolerance-stacked."],
        ["Measurement capability", "0.5 mm repeatability or better recommended", "The method must resolve a 2 mm acceptance limit. Record instrument, setup and three readings where practical."],
        ["Static proof", "Total 2 x MR for 10 minutes", "Distribute at the two S0 saddle centres in the released loaded-radiator distribution. This is not road-load/fatigue design release."],
        ["X0 trial stock only", "40 x 40 x 3 mm mild-steel SHS only if L0 is no more than 700 mm and MR no more than 35 kg", "Permitted only as a mock-up/starting rule. Final section, joints and welds require structural calculation and signed drawing."],
        ["FL moving clearance", "At least 20 mm radiator-to-blade static and 15 mm blade-to-shroud radial", "Functional minimums to verify on the real installed assembly; they do not define shroud or carrier dimensions."],
    ]
    story += [
        data_table(controlled_rows, [38 * mm, 52 * mm, 80 * mm], styles, font_style="table_small"),
        Spacer(1, 5 * mm),
        P("Actual dimensions still required", styles["h2"]),
        data_table(
            [
                ["Assembly", "Missing actual record", "Do not release until"],
                ["R0 radiator", "Complete W/H/D; active face; core pack; tank/header joint; necks; cap seat; drain; rails; every ear/hole; lower locators", "R0-H and S0/B0 sheets are signed and the radiator shop has stripped/measured the sample"],
                ["C0 condenser", "Fin field; complete W/H/D; drier; brackets; pipes; ports; tool and removal sweep", "C0 map and specialist retain/replace decision are signed"],
                ["G0 guard", "Perimeter frame W/H/D; diagonals; sound contact lengths; holes; mesh clearance; removal vector", "G0-H rigid template and CL0 readings are signed"],
                ["FS / FL", "Rotor axes; complete frames/tabs/guards; motors; plugs; cable bends; current; installed depth", "Electrical/airflow tests and component maps pass"],
                ["Vehicle / mounts", "VCL origin; connector faces and holes; L0; MR; S0/B0; all obstructions and service sweeps", "D00, A0-D-L/R, S0, B0, L0/MR and VEH records are signed"],
            ],
            [31 * mm, 91 * mm, 48 * mm],
            styles,
            font_style="table_small",
        ),
        Spacer(1, 4 * mm),
        callout("No photo scaling", "Tape-in-frame photographs identify measurement locations and condition only. Perspective, tape angle and hidden hard points make them unsuitable for a cut list or replacement-core order.", styles, PALE_AMBER),
        PageBreak(),
    ]

    story += page_title(
        "2. Actual R0 radiator - condition and restoration",
        "Retain the original copper/brass hard parts only where the radiator shop finds them sound; replace the tired heat-transfer core.",
        styles,
    )
    r0_photos = Table(
        [[
            photo_card(OLD_R0_DAMAGE, "ACTUAL CORE DAMAGE", "Dirt, flattened fins and local damage. This is evidence for recoring and shop testing, not a cosmetic-only repaint.", col, 61 * mm, styles),
            photo_card(OLD_R0_LEG, "ACTUAL LOWER-EDGE DETAIL", "Historical added support/leg and lower area. Classify every added piece on R0-H before removal, repair or rejection; do not reproduce it automatically.", col, 61 * mm, styles),
        ]],
        colWidths=[col, col],
    )
    r0_photos.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    story += [r0_photos, Spacer(1, 4 * mm)]
    r0_steps = [
        ["Step", "Radiator-shop instruction", "Evidence / pass"],
        ["R0-1", "Photograph and tag all faces; record cold pressure, flow restriction, leaks, damaged fins, seams, neck, drain, rails, ears and locators.", "Signed incoming condition sheet"],
        ["R0-2", "Build a rigid jig from the sound tank/header/rail relationships before unsoldering. Record complete actual dimensions and R0-H/S0/B0 interfaces.", "Dated jig record and actual measurement sheet"],
        ["R0-3", "Desolder and remove the old core without twisting tanks or rails. Chemically clean using a copper/brass-and-solder-compatible inhibited process.", "Bare parts inspected; no thinning, cracks or blocked passages"],
        ["R0-4", "Repair sound tanks, headers, filler/cap neck, drain, rails and approved ears. Any R0-E hot work is radiator-shop-only and occurs before final tests.", "Retain/repair/reject decision for each hard part"],
        ["R0-5", "Order the new copper/brass core from the stripped physical sample and stated naturally aspirated duty. Record tube/fin construction and finished core dimensions supplied by the shop.", "Core purchase record tied to R0 serial/tag"],
        ["R0-6", "Jig, solder and square the assembly without loading tanks/core through future brackets. Pressure-test and flow-test after all hot work.", "Written before/after pressure and flow results"],
        ["R0-7", "Apply only a thin radiator-shop heat-exchanger coating; keep fins open and cap seat, necks, drain, threads, earths and rubber lands clean.", "Straight/open fins, clean interfaces and final dimensions recorded"],
    ]
    story += [data_table(r0_steps, [16 * mm, 111 * mm, 43 * mm], styles, font_style="table_small"), PageBreak()]

    story += page_title(
        "3. Actual C0 condenser and receiver-drier",
        "The large canister is the existing receiver-drier. It supplies the geometry reference only; install a new sealed compatible unit at final assembly.",
        styles,
    )
    c0_photos = Table(
        [[
            photo_card(OLD_C0, "ACTUAL C0 COMPLETE ASSEMBLY", "Measure the complete condenser including pipes, brackets, ports and tool sweep. The fin field alone does not define the installed envelope.", col, 66 * mm, styles),
            photo_card(OLD_C0_DRIER, "ACTUAL RECEIVER-DRIER LOCATION", "Tall black can beside C0. It filters debris, absorbs moisture and provides a liquid-refrigerant reserve. Keep the old unit only as a port, bracket and routing sample.", col, 66 * mm, styles),
        ]],
        colWidths=[col, col],
    )
    c0_photos.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    story += [c0_photos, Spacer(1, 4 * mm)]
    story += [
        data_table(
            [
                ["Step", "A/C specialist instruction", "Evidence / pass"],
                ["C0-1", "Cap ports, tag every pipe/bracket and record actual fin-field and complete installed envelope dimensions before disassembly.", "C0 map with drier/port/tool/removal envelopes"],
                ["C0-2", "Use neutral aluminium-safe cleaner, low pressure and a correct fin comb. Do not use harsh brightener or a pressure jet.", "Clean, open fins with no new tube damage"],
                ["C0-3", "Specialist leak/pressure and contamination assessment using the specified safe test medium and pressure for the identified condenser.", "Written retain/repair/replace decision"],
                ["C0-4", "Retain sound C0 only if it passes. Otherwise commission a matched parallel-flow replacement from the complete physical envelope and port map.", "Replacement drawing/sample comparison if required"],
                ["C0-5", "Fit a new sealed compatible receiver-drier, new HNBR O-rings/seals/caps and the identified refrigerant oil during final specialist assembly.", "Drier part ID, oil/refrigerant identity and evacuation record"],
                ["C0-6", "Mount C0 on independent C1 brackets with isolators and shoulder/crush sleeves; preserve pipe and tool sweep.", "No load transferred to R0, G0 or another heat exchanger"],
            ],
            [16 * mm, 111 * mm, 43 * mm],
            styles,
            font_style="table_small",
        ),
        PageBreak(),
    ]

    story += page_title(
        "4. Actual G0 guard, FS pusher and FL puller",
        "Restore and test the retained parts first. Replace a fan only if the complete tested assembly cannot meet the measured installation.",
        styles,
    )
    third = (CONTENT_W - 12) / 3
    part_photos = Table(
        [[
            photo_card(OLD_G0, "ACTUAL G0", "Removable expanded-mesh guard and frame. Hold only the perimeter frame; never clamp the mesh.", third, 67 * mm, styles),
            photo_card(OLD_FS, "ACTUAL FS", "The one central front A/C pusher candidate. The complete frame/rotor datum, not blade diameter alone, controls F1.", third, 67 * mm, styles),
            photo_card(OLD_FL, "ACTUAL FL", "Large rear puller and shroud. F2 supports the shroud independently and seals to the sound R0 frame.", third, 67 * mm, styles),
        ]],
        colWidths=[third, third, third],
    )
    part_photos.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    story += [part_photos, Spacer(1, 4 * mm)]
    story += [
        data_table(
            [
                ["Part", "Restoration / test", "Fabrication interface"],
                ["G0", "Jig; clean; straighten/repair perimeter; repair or replace damaged mesh while preserving open area; deburr; apply thin compatible satin/semi-gloss finish and edge trim.", "G1 lower cradles and G2 accessible keepers contact broad, sound perimeter lengths through EPDM; preserve drainage and a documented removal vector."],
                ["FS", "Record maker/label, polarity, rotation, push direction, start/run current, voltage drop, bearing noise, wobble, rub, plug/cable and installed airflow before retain decision.", "One independent F1 carrier. Complete frame/rotor datum is measured directly to VCL and separately to C0. Own relay, fuse and earth."],
                ["FL", "Record maker/label, polarity, pull direction, start/run current, bearing/rub, complete shroud, plug/cable bend, seal land and installed airflow.", "Independent F2 carrier and replaceable EPDM seal to the sound R0 frame; maintain moving clearances and zero tank/core load. Own relay, fuse and earth."],
            ],
            [19 * mm, 78 * mm, 73 * mm],
            styles,
            font_style="table_small",
        ),
        Spacer(1, 4 * mm),
        callout("Alignment", "The complete repaired G0 perimeter-frame centre, complete mounted FS frame/rotor datum and C0 usable-fin-field centre each require their own direct reading to VCL within 2 mm. Then record G0-to-fixed-aperture and FS-to-C0 X/Z offsets separately within 2 mm.", styles, PALE_TEAL),
        PageBreak(),
    ]

    story += page_title(
        "5. Where to take the actual measurements",
        "Create D00 first from fixed chassis references; every coordinate and centre offset is then measured directly from it.",
        styles,
    )
    measure_photo = Table(
        [[
            photo_card(OLD_CHASSIS, "ACTUAL VEHICLE CONTEXT", "Record the intended structural connector bearing face and hole group on each side. Do not scale this photograph and do not use steering, suspension, bumper, tow or thin sheet as a pickup.", col, 65 * mm, styles),
            photo_card(OLD_R0, "ACTUAL COMPONENT DATUM", "Use hard, repeatable rails, tank/header edges, neck axes, locator axes and sound ear planes. Record complete hard points and service sweeps.", col, 65 * mm, styles),
        ]],
        colWidths=[col, col],
    )
    measure_photo.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    story += [measure_photo, Spacer(1, 4 * mm)]
    story += [
        data_table(
            [
                ["Record", "Measurement points / method", "Actual result"],
                ["D00", "VCL plus fixed chassis X/Y/Z origin, projected at G0, FS, C0 and A0 planes. Record origin marks, instrument, setup and repeatability.", "Origin: __________  Method: __________  Repeatability: ____ mm"],
                ["A0-D-L", "Left connector bearing face XYZ; every hole centre/diameter from two orthogonal edges; local section/thickness; bolt/nut/tool/removal sweep.", "Template ID: ______  Face XYZ: __________  Holes: __________"],
                ["A0-D-R", "Right connector bearing face and hole group by the same method; do not mirror-assume.", "Template ID: ______  Face XYZ: __________  Holes: __________"],
                ["L0", "Clear span between released A0/A1 end-envelope limit planes at X0 level, including joint/tool/drainage envelopes.", "L0 = ______ mm"],
                ["MR", "Finished, capped R0 filled to installed level, including retained fittings; record scale and uncertainty.", "MR = ______ kg  Scale: ______  Uncertainty: ______"],
                ["S0-L/R", "R0 lower locator centres/diameters plus final R1 saddle centres, cup depths and installed loaded heights.", "L XYZ/dia/height: __________  R: __________"],
                ["B0-L/R", "With R0 naturally seated and sharing weight across both R1 saddles, transfer sound upper keeper axes/planes to fixed structure.", "L XYZ/plane: __________  R: __________"],
            ],
            [22 * mm, 91 * mm, 57 * mm],
            styles,
            font_style="table_small",
        ),
        PageBreak(),
    ]

    story += page_title(
        "6. Component and alignment measurement sheet",
        "Complete every blank from the actual repaired part, including all brackets, plugs, pipes, cable bends and removal/tool envelopes.",
        styles,
    )
    actual_rows = [
        ["Record", "Required actual readings", "Actual / template / date"],
        ["R0 complete", "W/H/D; active face W/H; core pack; body-to-cap height; upper/lower/overflow neck OD/axis; drain; rails; each R0-H ear/hole/plane; lower locators", "W ____ H ____ D ____ mm; map/template __________"],
        ["C0 complete", "Fin field W/H/centre; body W/H/D; complete W/H/D including drier, pipes, ports and brackets; tool and removal sweep", "Fin ____ x ____ mm; total ____ x ____ x ____ mm; map ______"],
        ["G0-H", "Frame W top/mid/bottom; H left/centre/right; maximum D; both diagonals; sound contact lengths/planes/holes; mesh-to-fixed-grille clearance; removal vector", "W ____/____/____; H ____/____/____; D ____; diag ____/____ mm"],
        ["FS", "Rotor diameter/axis; complete frame W/H/D; tabs/guard; motor/plug/cable bend; current/voltage/airflow/direction", "Rotor ____; frame ____ x ____ x ____ mm; test sheet ______"],
        ["FL", "Rotor diameter/axis; shroud W/H/D; tabs; motor/plug/cable bend; seal land; static/radial moving clearances; current/airflow/direction", "Rotor ____; shroud ____ x ____ x ____ mm; clearances ____/____ mm"],
        ["CL0 direct", "Signed lateral offset from D00-VCL to G0 frame centre, FS frame/rotor datum and C0 fin-field centre, each independently", "G0 ____ mm  FS ____ mm  C0 ____ mm; each PASS [ ]"],
        ["CL0 local", "Signed X/Z G0 frame-to-fixed-aperture and FS frame/rotor-to-C0 fin field; raw left/right/top/bottom readings retained", "G0 X/Z ____/____ mm; FS X/Z ____/____ mm; PASS [ ]"],
        ["VEH", "Fixed grille, bonnet/latch, bumper, steering, suspension, tow, support steel, engine movement, hoses, pipes, wiring, tools and independent removal paths", "Envelope drawing/template ID __________"],
    ]
    story += [
        data_table(actual_rows, [24 * mm, 101 * mm, 45 * mm], styles, font_style="table_small"),
        Spacer(1, 4 * mm),
        callout("Measurement release", "Fabricator and owner sign the common-datum coordinate sheet and rigid templates. Record raw readings, not only calculated centres. Left and right parts are measured separately; neither side is assumed symmetric.", styles, PALE_AMBER),
        Spacer(1, 5 * mm),
        P("Measurement sign-off", styles["h2"]),
        data_table(
            [
                ["Role", "Name", "Instrument / template IDs", "Signature / date"],
                ["Measurer", "", "", ""],
                ["Fabricator", "", "", ""],
                ["Owner witness", "", "", ""],
            ],
            [35 * mm, 42 * mm, 55 * mm, 38 * mm],
            styles,
        ),
        PageBreak(),
    ]

    story += page_title(
        "7. Fabrication reference schedule",
        "Each part is drawn from its named measured interface. Rev R contains no bracket cut size, hole size, material thickness, weld size or torque release.",
        styles,
    )
    fab_rows = [
        ["Ref / qty", "Function and attachment", "Required inputs", "Issued fabrication evidence"],
        ["X0 / 1", "Full-width lower crossmember between A0/A1 ends; carries X1 saddle seats", "L0, MR, A0-D, S0, road/shock/fatigue loads, drainage and service", "Signed structural plan/elevation/sections, section, joints, welds, finish"],
        ["X1-L/R / 2", "R1 saddle seats on X0; carry all filled-R0 vertical weight", "S0, selected R1 cup/base/loaded height, locator map and drainage", "Seat/gusset details and weld/inspection plan"],
        ["A0-L/R + A1-L/R / 2 assys", "Short arms and connector ends mating directly to actual chassis connector bearing faces", "A0-D-L/R rigid templates, L0, X0 interface, local parent section, tool/removal envelope", "Separate LH/RH drawings; material, cut, bends, holes, edge distance, weld/bolts and torque"],
        ["G1-L/R / 2", "Broad EPDM-faced lower cradles on sound G0 perimeter frame only", "G0-H contact lengths/planes, G0 centre, CL0, drainage and withdrawal path", "Blank/bend/section, sleeve-controlled hardware and finish"],
        ["G2-L/R / 2", "Accessible upper/side positive keepers on G0 frame only", "G0-H, final G1 seating, CL0 and removal/tool sweep", "Keeper/escape-lip and anti-chafe detail"],
        ["R0-E / as required", "Radiator-side ear/tab repair or replacement on sound rail/header only", "R0-H classification, jig and tank/core clearance", "Radiator-shop drawing/process; pressure/flow test after hot work"],
        ["R3-U / 2", "Upper locating keepers; restraint only and neutral in vertical load", "B0 after final R1/X1 seating, R0-H and EPDM/crush-sleeve stack", "Keeper drawing, compression control and neutral-load witness method"],
        ["R3-L / 0 or 2", "Optional side stabilisers; zero vertical load", "Dry-fit justification, R0-H sound interfaces and service sweep", "Issued only if required; otherwise N/A"],
        ["C1 / measured", "Independent removable C0 brackets with isolation", "Complete C0 map, ports/pipes/drier/tool sweep and C0-to-VCL", "Bracket and shoulder/crush-sleeve joint drawings"],
        ["F1 / 1 set", "Independent central FS carrier upstream of C0", "Complete FS map, current/airflow, FS-to-VCL and FS-to-C0", "Carrier, guard/plug/cable clearance and removable joint drawing"],
        ["F2 / 1 set", "Independent FL shroud support and R0 frame seal land", "FL and R0-H maps, moving clearances, engine/service envelope", "Frame, EPDM seal compression and zero-core-load detail"],
        ["E1 / 1", "Splash-resistant removable relay/fuse carrier", "FS/FL currents, cable runs, earths, drainage and service access", "Electrical layout and enclosure/carrier drawing"],
    ]
    story += [
        data_table(fab_rows, [27 * mm, 55 * mm, 51 * mm, 37 * mm], styles, font_style="table_small"),
        Spacer(1, 4 * mm),
        callout("Drawing rule", "Every issued drawing carries a unique revision, quantity, material and standard, dimensions/tolerances, hole/bend/weld definition, fastener and torque, finish, interface reference and inspection point. This PDF is the scope and measurement record, not the cut drawing.", styles, PALE_RED),
        PageBreak(),
    ]

    story += page_title(
        "8. Lower cradle and short connector arms",
        "The retained arms are loose and unattached: shorten or replace them on the bench so the finished pair ends at the highest required interface with no unused upright projection.",
        styles,
    )
    story += [
        photo_card(OLD_CHASSIS, "ACTUAL INTERFACE CONTEXT - VERIFY ON VEHICLE", "Historical front-support view only. Resolve the true current connector bearing planes and hole groups with A0-D-L/R templates before design. No photograph establishes the finished arm height.", CONTENT_W, 88 * mm, styles),
        Spacer(1, 4 * mm),
        data_table(
            [
                ["Sequence", "Fabrication instruction", "Hold / inspection"],
                ["A", "Identify and inspect each loose arm blank. Record grade evidence, section, wall/plate thickness, straightness, corrosion, old holes, cracks and previous heat damage.", "Replace with certified matched steel if grade/condition/weldability is not released"],
                ["B", "Template the actual LH/RH connector bearing faces and hole groups separately. Model bolt head, nut, socket and removal clearance.", "No mirror assumption; no new chassis holes, slots, reaming or forced alignment"],
                ["C", "Set final R1/X1/R0 seating, B0 keeper planes and X0 level. Derive each arm height between its connector bearing plane, X0 interface and highest assigned functional interface.", "No unused upper projection and no tank/core load"],
                ["D", "Competent person designs X0/X1/A0/A1 for vertical, fore/aft, lateral, shock, vibration and fatigue loads, plus welds, bolts, bearing and corrosion/drainage.", "The 2 x MR proof does not replace calculation"],
                ["E", "Make a tack/temporary steel or rigid template assembly; dry-fit actual saddles, rubbers, fasteners and R0. Correct the drawing, then fabricate and inspect the released parts.", "Final dimensions come only from the signed drawing"],
            ],
            [16 * mm, 108 * mm, 46 * mm],
            styles,
            font_style="table_small",
        ),
        Spacer(1, 4 * mm),
        callout("Conditional X0 starting rule", "40 x 40 x 3 mm mild-steel SHS is permitted only as mock-up/starting stock when measured L0 is no more than 700 mm and measured MR is no more than 35 kg. It is not a final structural selection.", styles, PALE_AMBER),
        PageBreak(),
    ]

    story += page_title(
        "9. Guard, radiator and fan-holder fabrication",
        "Holder geometry follows repaired-part templates. Use broad rubber-faced contacts, controlled compression, drainage and independent removal.",
        styles,
    )
    holders_photos = Table(
        [[
            photo_card(OLD_G0, "G0-H SOURCE", "Measure sound straight perimeter-frame lengths and planes for G1/G2. Mesh is not a bearing surface.", col, 62 * mm, styles),
            photo_card(OLD_R0, "R0-H SOURCE", "Classify rails, headers, ears and locators. R0-E/R3/F2 may use only sound released interfaces and never tank/core/fin surfaces.", col, 62 * mm, styles),
        ]],
        colWidths=[col, col],
    )
    holders_photos.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    story += [holders_photos, Spacer(1, 4 * mm)]
    story += [
        data_table(
            [
                ["Holder", "Specific construction requirement", "Acceptance"],
                ["G1", "Two lower frame cradles with broad replaceable EPDM contact, positive lateral control, open drainage and no mesh contact.", "G0 rests without twist; direct G0-to-VCL and local aperture offsets pass"],
                ["G2", "Two accessible upper/side keepers with sleeve-controlled EPDM compression and a positive escape lip/retention feature.", "No preload distortion; G0 removes by the documented vector without disturbing C0/FS"],
                ["R3-U", "Two short keepers at B0 using new EPDM and fitted crush sleeves. Tightening locates/restrains only.", "Both R1 saddles remain loaded; documented post-torque neutral-load witness"],
                ["R3-L", "Add only if dry fit proves side restraint is required; use a sound R0-H interface and no vertical support.", "N/A or zero vertical load recorded"],
                ["F1", "One central FS carrier with complete-frame tabs, guard, motor, plug and cable bends represented. Independent of G0/C0/R0.", "Direct FS-to-VCL and local FS-to-C0 offsets pass; serviceable fasteners"],
                ["F2", "Carrier supports the full FL shroud and replaceable seal land; no through-core ties or tank/core loads.", "Shroud seals to sound R0 frame; moving/engine/tool clearances pass"],
            ],
            [20 * mm, 101 * mm, 49 * mm],
            styles,
            font_style="table_small",
        ),
        PageBreak(),
    ]

    story += page_title(
        "10. Ten-stage restoration and fabrication sequence",
        "Each stage ends with named evidence. Do not paint or order final hoses until the bare-metal full-stack dry fit passes.",
        styles,
    )
    sequence_rows = [
        ["Stage", "Work", "Release evidence"],
        ["1. Inventory", "Tag and photograph R0/C0/G0/FS/FL, loose arms and all brackets. Cap ports. Baseline-test R0, C0 and both fans.", "Signed retain / repair / replace decisions"],
        ["2. Measure", "Establish D00; capture A0-D, B0, S0, CL0, G0-H, R0-H, L0/MR, complete component and vehicle envelopes with rigid templates.", "Signed raw readings, common-datum sheet and templates"],
        ["3. R0", "Jig, strip, clean, repair, order/fix core by sample, complete approved R0-E hot work, pressure/flow test and thin coat.", "Radiator-shop job sheet and final measured R0 map"],
        ["4. C0", "Neutral clean, fin-comb, specialist leak/contamination test; retain or replace by complete sample; new drier/HNBR at assembly.", "A/C specialist result and final C0 map"],
        ["5. G0/fans", "Repair G0 frame/mesh; test FS and FL identity, direction, current, bearings, complete frame, wiring and installed airflow.", "G0-H and fan test sheets"],
        ["6. Structure", "Engineer and fabricate X0/X1/A0/A1 to actual connector, saddle and load records.", "Signed structural drawings and weld/fastener inspection"],
        ["7. Holders", "Fabricate G1/G2/R3/C1/F1/F2/E1 from their named actual templates with sleeved EPDM isolation.", "Tagged parts, drawings and bench inspection"],
        ["8. Bare dry fit", "Assemble the opaque full stack with actual rubbers, hardware, pipes, plugs, cable bends, hoses and tools. Record direct and local CL0 values.", "No forced alignment; all clearances/removal paths and centre checks pass"],
        ["9. Proof/finish", "Apply released total 2 x MR / 10 minute proof, reinspect datums and joints, then deburr, clean, prime, finish and cavity-protect eligible steel.", "No set/crack/movement; coating and drainage inspection"],
        ["10. Assemble/test", "Fit cooling/A/C plumbing and two independent fan circuits; pressure/evacuate/charge, heat-cycle, hot-idle A/C, road/load and reinspection.", "No leak/rub/boil/purge/thermal escalation or witness movement"],
    ]
    story += [
        data_table(sequence_rows, [21 * mm, 102 * mm, 47 * mm], styles, font_style="table_small"),
        Spacer(1, 4 * mm),
        callout("Stop-work rule", "If a retained interface is cracked, thinned, distorted, unidentifiable or would force misalignment, stop and revise the drawing or replace the part. Do not solve fit with slots, reaming, loose washer stacks, self-tappers or through-core ties.", styles, PALE_RED),
        PageBreak(),
    ]

    story += page_title(
        "11. Proof, finishing and final assembly",
        "Proof the accepted bare-metal structure before coating. Keep heat-exchanger, rubber and electrical interfaces free of unsuitable finish.",
        styles,
    )
    story += [
        data_table(
            [
                ["Operation", "Specific method", "Pass / record"],
                ["Dry fit", "Fit all actual components, rubbers, sleeves, fasteners, pipes, plugs, hoses and tool envelopes. Check bonnet/latch, grille, bumper, steering, suspension, tow and engine movement.", "Independent removal paths; no contact, forced pull or distorted rubber"],
                ["Static proof", "Apply a total static load of 2 x MR, distributed between S0 saddle centres in the released loaded-radiator distribution for 10 minutes using a fixture that avoids point loading.", "No permanent set, crack, connector/fastener movement, saddle displacement, arm distortion or alignment loss"],
                ["Post-proof", "Repeat A0-D/S0/B0/CL0 critical readings, inspect welds/bolts/connectors and verify R3-U remains neutral while both saddles carry weight.", "Signed before/after sheet and witness photographs"],
                ["Steel preparation", "Deburr/radius; degrease; local ferrous rust treatment within one compatible system; preserve drains, bearing faces, earths, threads and rubber seats.", "Clean, keyed, dry substrate and open drains"],
                ["Steel finish", "Professional 2K epoxy primer plus compatible 2K polyurethane satin/semi-gloss; cavity wax only after cure in eligible closed sections.", "Continuous thin finish, correct cure, no blocked drainage or coated interfaces"],
                ["Heat exchangers", "R0 gets thin radiator-shop coating only; C0 fins stay open and clean. Do not powder coat, fill or thick-prime cores.", "Open fins and readable labels/ports"],
                ["Final hardware", "Use released class/grade, broad washers, positive/prevailing locks, grip length and fitted crush/shoulder sleeves; torque and witness-mark as drawn.", "Torque sheet, sleeve-controlled rubber compression and visible witness marks"],
            ],
            [28 * mm, 99 * mm, 43 * mm],
            styles,
            font_style="table_small",
        ),
        Spacer(1, 5 * mm),
        P("Final installation checks", styles["h2"]),
        *bullets([
            "Use new measured coolant hoses, overflow hose, constant-tension clamps, approved cap, Toyota 2H thermostat/seal and one compatible long-life coolant family.",
            "Use a new sealed compatible receiver-drier, HNBR seals/caps and the identified refrigerant oil; evacuation and charging are A/C-specialist work.",
            "Give FS and FL separate sealed relays, fuses and earths sized from measured start/run current and route length; record voltage drop and connector temperature.",
            "Heat-cycle and bleed; hot-idle with A/C; road/load test the naturally aspirated vehicle; reinspect after cool-down and the first loaded journey.",
        ], styles),
        PageBreak(),
    ]

    story += page_title(
        "12. Parts, chemicals and consumables",
        "Buy wear, sealing and service parts new. Retain major assemblies only after the tests above; fabricate every holder from the signed actual interface drawings.",
        styles,
    )
    parts_rows = [
        ["Group", "Required parts / consumables", "Control"],
        ["Radiator", "Shop-sourced copper/brass core, compatible solder/flux, thin heat-exchanger coating, R1 saddles, approved cap, 2H thermostat/seal, measured moulded hoses, overflow hose, constant-tension clamps and coolant", "Core, necks and hoses from stripped/final R0; no catalogue guess"],
        ["A/C", "New compatible receiver-drier, HNBR O-rings/seals/caps and identified refrigerant oil", "Match final C0 and refrigerant system; never reuse old drier"],
        ["Mounting", "Automotive EPDM strips/bushes, fitted crush/shoulder sleeves, edge trim, shroud seal, released plated fasteners, broad washers and positive/prevailing locknuts", "Rubber compression is sleeve-controlled; no loose spacer stacks"],
        ["Electrical", "Two separate sealed relay/fuse branches, measured cable, terminals/connectors, earth hardware, heat-shrink, grommets, loom and P-clips", "Size after actual FS/FL current and route-length tests"],
        ["Cleaning", "Water-based degreaser; copper/brass-and-solder-compatible inhibited radiator cleaner; neutral aluminium-safe condenser cleaner; 70-90% IPA for compatible bracket wipe", "Follow current SDS; cap ports; no motor immersion, harsh acid/caustic or pressure jet"],
        ["Steel coating", "One compatible 2K epoxy and 2K polyurethane satin/semi-gloss system; local phosphoric steel prep; compatible cavity wax after cure", "Professional controls/PPE; isolate from aluminium, copper/brass, solder, cores, rubber, earths and threads"],
        ["Assembly", "EPDM-safe assembly aid and light dielectric grease for connector seal lips/boots", "No petroleum grease on EPDM and no dielectric grease between contact faces"],
    ]
    story += [
        data_table(parts_rows, [29 * mm, 96 * mm, 45 * mm], styles, font_style="table_small"),
        Spacer(1, 4 * mm),
        callout("Specialist safety", "Use weld consumables matched to verified parent steel and an approved WPS. Never weld near chlorinated-cleaner residue, pressure-test A/C with oxygen, vent refrigerant or spray 2K products without the specified professional respiratory and workshop controls.", styles, PALE_RED),
        Spacer(1, 5 * mm),
        P("Quality finish target", styles["h2"]),
        P("Straight, open fins; neat and fully cleaned solder work; satin/semi-gloss coated steel; thin heat-exchanger coating; clean plated hardware; replaceable black EPDM; visible drainage; accessible service fasteners; labelled wiring and capped ports.", styles["body"]),
        PageBreak(),
    ]

    story += page_title(
        "13. Example renewed finish - appearance only",
        "This single example image communicates cleanliness and organisation. It is deliberately excluded from every dimensional and fabrication decision.",
        styles,
    )
    story += [
        photo_card(
            RENEW_BENCH,
            "EXAMPLE FINISH ONLY - ILLUSTRATIVE AND NON-DIMENSIONAL",
            "A tidy bench presentation of restored heat exchangers, guard, one FS, one FL, fabricated supports, isolators and hardware. The rendered drier finish, bracket shapes, hole patterns, arm proportions, pipe routes and component spacing are not evidence of the actual parts and must not be copied.",
            CONTENT_W,
            112 * mm,
            styles,
            renewed=True,
        ),
        Spacer(1, 5 * mm),
        data_table(
            [
                ["Use this image for", "Do not use this image for"],
                ["Finish quality; part cleanliness; organised hardware; replaceable rubber; serviceable presentation", "Dimensions; cut lengths; material thickness; hole locations; drier proportions; brackets; pipes; wiring; fan spacing; centreline proof"],
            ],
            [85 * mm, 85 * mm],
            styles,
            header_color=TEAL,
        ),
        Spacer(1, 5 * mm),
        callout("Fabrication evidence hierarchy", "1) Actual tagged component and vehicle. 2) Signed D00/common-datum readings and rigid templates. 3) Released component maps and specialist reports. 4) Signed structural and fabrication drawings. This example render and all photographs sit outside the dimensional evidence chain.", styles, PALE_AMBER),
        PageBreak(),
    ]

    story += page_title(
        "14. Release checklist",
        "The work is final only when every applicable line has evidence, initials and date.",
        styles,
    )
    release_rows = [
        ["Gate", "Pass requirement", "Evidence / sign-off"],
        ["Parts", "R0 pressure/flow; C0 specialist test; G0 condition; FS/FL identity, electrical, direction, bearing and airflow decisions complete", "Reports / initials: __________________"],
        ["Actual measurements", "D00, A0-D-L/R, B0, S0, CL0, G0-H, R0-H, L0/MR, R0/C0/FS/FL and VEH sheets complete with raw readings and templates", "Measurer / owner / date: __________________"],
        ["Drawings", "X0/X1/A0/A1 structural release plus G1/G2/R0-E/R3/C1/F1/F2/E1 drawings issued at named revisions", "Drawing register: __________________"],
        ["Fabrication", "Material certificates/identification, cuts, bends, holes, welds, fasteners, torque provisions, sleeves, drainage and finish access inspected", "Fabricator / inspector: __________________"],
        ["Dry fit", "One FS + one FL; all direct/local centre checks pass; independent supports/removal; all vehicle, engine, pipe, hose, wire and tool envelopes clear", "CL0 and fit sheet: __________________"],
        ["Proof", "Released total 2 x MR / 10 minute test passes; critical readings repeated; R3-U remains neutral and both saddles loaded", "Structural witness: __________________"],
        ["Finish / assembly", "Coating, drainage, hardware, rubbers, hoses, A/C seals/drier and both protected fan branches pass", "Finish/torque/electrical sheets: __________"],
        ["Performance", "Cooling pressure/bleed/heat-cycle, A/C evacuation/charge/hot-idle, road/load and first-journey reinspection pass", "Commissioning record: __________________"],
    ]
    story += [
        data_table(release_rows, [28 * mm, 104 * mm, 38 * mm], styles, font_style="table_small"),
        Spacer(1, 5 * mm),
        callout("Controlled final status", "FINAL FIT + FABRICATION + PERFORMANCE RELEASE HOLD until the actual measurement fields, specialist tests, drawings, proof and commissioning records above are complete.", styles, PALE_RED),
        Spacer(1, 6 * mm),
        P("Controlled references", styles["h2"]),
        *bullets([
            "Technical guide: docs/J40-naturally-aspirated-cooling-pack-restoration-guide-rev-p-20260816.md.",
            "Fabrication handoff: data/manual/fabrication/na_cooling_connector_arms_rev_p/README.md, measurement_basis.csv, fabricator_cut_list.csv and inspection_checklist.csv.",
            "Actual image evidence: the controlled front-cooling-stack work-document assets plus the dated project photographs identified in this PDF.",
            "Superseded and excluded: Rev A 410 mm / 4 mm tall uprights; Rev N X2 adapters; turbo/intercooler/K0 and second-front-fan layouts; every Rev Q provisional envelope estimate.",
        ], styles),
        PageBreak(),
    ]

    # Cost estimate must remain the final section/page.
    baseline = [
        ("Measurement, rigid templates, drawings and structural review", "D00/component capture, LH/RH templates, issued fabrication drawings", 15000, 35000),
        ("R0 strip, repair, recore and tests", "Reuse sound tanks/headers/necks/rails; new copper/brass core", 40000, 80000),
        ("C0 clean/test plus new drier and HNBR seals", "Assumes retained condenser passes specialist test", 15000, 35000),
        ("G0 repair, mesh/frame finish and edge protection", "Retain/re-mesh by actual template", 8000, 20000),
        ("FS and FL test/service", "Assumes both retained motors/frames remain usable", 10000, 25000),
        ("Fabricate all released mounts and carriers", "X0/X1/A0/A1/G1/G2/R0-E/R3/C1/F1/F2/E1", 45000, 95000),
        ("Blast/prep, 2K primer and satin/semi-gloss finish", "Steel parts only; professional 2K controls", 15000, 35000),
        ("Cooling service parts", "Hoses, clamps, cap, thermostat/seal and coolant", 15000, 35000),
        ("Fan electrical parts", "Two separate relay/fuse/wire/connector/earth branches", 12000, 30000),
        ("A/C evacuation, charge and final specialist work", "Excludes major compressor/evaporator repair", 10000, 25000),
    ]
    low_sub = sum(row[2] for row in baseline)
    high_sub = sum(row[3] for row in baseline)
    low_cont = round(low_sub * 0.15 / 1000) * 1000
    high_cont = round(high_sub * 0.15 / 1000) * 1000
    low_total = low_sub + low_cont
    high_total = high_sub + high_cont
    cost_rows = [["Baseline scope", "Assumption", "Low PKR", "High PKR"]]
    cost_rows.extend([[name, note, f"{low:,}", f"{high:,}"] for name, note, low, high in baseline])
    cost_rows.extend([
        ["Baseline subtotal", "Before contingency", f"{low_sub:,}", f"{high_sub:,}"],
        ["Contingency", "15% for hidden damage, rework and price movement", f"{low_cont:,}", f"{high_cont:,}"],
        ["PLANNING TOTAL", "Hybrid refurbishment, retained major parts passing tests", f"{low_total:,}", f"{high_total:,}"],
    ])
    optional = [
        ("New matched C0 condenser if retained C0 fails", 25000, 50000),
        ("Quality new FS pusher if candidate fails", 15000, 45000),
        ("Quality new FL/shroud if retained unit fails", 20000, 55000),
        ("Complete bespoke copper/brass R0 instead of recore - incremental", 40000, 90000),
    ]
    opt_low = sum(r[1] for r in optional)
    opt_high = sum(r[2] for r in optional)
    story += page_title(
        "15. Cost estimate - PKR planning allowance",
        "Budget range at 16 Aug 2026. This is a planning estimate, not a supplier quotation; actual measurements and specialist condition reports control scope.",
        styles,
    )
    story += [
        data_table(cost_rows, [60 * mm, 68 * mm, 21 * mm, 21 * mm], styles, font_style="table_small"),
        Spacer(1, 5 * mm),
        P("Optional failure-case replacements", styles["h2"]),
        data_table(
            [["Optional addition", "Low PKR", "High PKR"]]
            + [[name, f"{low:,}", f"{high:,}"] for name, low, high in optional]
            + [["Maximum optional increment", f"{opt_low:,}", f"{opt_high:,}"],
               ["Worst-case planning envelope", f"{low_total + opt_low:,}", f"{high_total + opt_high:,}"]],
            [116 * mm, 27 * mm, 27 * mm],
            styles,
            font_style="table_small",
            header_color=COPPER,
        ),
        Spacer(1, 4 * mm),
        callout(
            "Budget assumptions",
            "Ranges include local parts, specialist work and fabrication labour allowances but exclude imported freight/duties, engine-bay repairs outside the cooling pack, compressor/evaporator replacement and sales tax treatment not included by a quoted shop. Obtain three itemised quotations after the actual measurement and retain/replace sheets are signed.",
            styles,
            PALE_AMBER,
        ),
        Spacer(1, 3 * mm),
        P(
            "Retail anchors checked 16 Aug 2026: <link href='https://www.daraz.pk/products/car-ac-fan-12v-i422740946-s2000653044.html'><u>generic 12 V fan</u></link> PKR 1,999; <link href='https://www.ubuy.com.pk/en/product/FXYKFNS-mishimoto-slim-electric-fan-14'><u>imported quality 14-inch fan</u></link> PKR 40,231 before shipping/customs; <link href='https://matchingpaint.com/shop/2k-automotive-clear/'><u>2K clear</u></link> PKR 2,850; <link href='https://woodemotions.pk/products/ik332-77-2k-acrylic-primer-ps370t'><u>2K primer</u></link> PKR 12,000; 4 L coolant listings roughly PKR 2,095-4,900. These anchors explain the wide ranges; they are not approved parts.",
            styles["small"],
        ),
        Spacer(1, 3 * mm),
        callout("Recommended procurement route", "Recore R0; test and conditionally retain C0, G0, FS and FL; fabricate the mounts from actual templates; buy all service consumables, receiver-drier, seals, isolation, fasteners and wiring new. A complete new pack is sensible only as a bespoke sample-built commission, not an off-the-shelf listing.", styles, PALE_TEAL),
    ]
    return story


def main():
    TMP.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    required = [
        OLD_R0,
        OLD_R0_DAMAGE,
        OLD_R0_LEG,
        OLD_C0,
        OLD_C0_DRIER,
        OLD_G0,
        OLD_FS,
        OLD_FL,
        OLD_CHASSIS,
        RENEW_INSTALLED,
        RENEW_BENCH,
        RENEW_DRYFIT,
        RENEW_HOLDERS,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing source assets:\n" + "\n".join(missing))

    styles = styles_for_doc()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        rightMargin=MARGIN,
        leftMargin=MARGIN,
        topMargin=16 * mm,
        bottomMargin=15 * mm,
        title="J40 Cooling Pack Restoration and Fabrication Plan - Rev R",
        author="J40 restoration project",
        subject="Fabrication-reference naturally aspirated cooling pack restoration plan with actual-measurement capture and cost estimate",
        creator="ReportLab",
    )
    doc.build(build_story_rev_r(styles), onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUT)


if __name__ == "__main__":
    main()
