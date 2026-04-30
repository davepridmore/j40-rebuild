from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from math import cos, pi, sin
from typing import Iterable, Sequence

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm as pdf_mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas


OUT_DIR = Path("/Users/davidpridmore/IdeaProjects/J40/data/manual/fabrication/electrical_modules_rev_a")


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    w: float
    h: float


@dataclass(frozen=True)
class Line:
    x1: float
    y1: float
    x2: float
    y2: float


@dataclass(frozen=True)
class Poly:
    points: Sequence[tuple[float, float]]


@dataclass(frozen=True)
class Circle:
    x: float
    y: float
    r: float


@dataclass(frozen=True)
class Drawing:
    name: str
    width: float
    height: float
    cut_polys: Sequence[Poly]
    cut_rects: Sequence[Rect]
    cut_circles: Sequence[Circle]
    bend_lines: Sequence[Line]
    notes: Sequence[str]


PDF_NAME = "j40_electrical_modules_rev_a_dimension_sheet.pdf"


def mm(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


def svg_rect(rect: Rect, layer: str) -> str:
    cls = "cut" if layer == "CUT" else "aux"
    return (
        f'<rect class="{cls}" x="{mm(rect.x)}" y="{mm(rect.y)}" '
        f'width="{mm(rect.w)}" height="{mm(rect.h)}" />'
    )


def svg_poly(poly: Poly) -> str:
    points = " ".join(f"{mm(x)},{mm(y)}" for x, y in poly.points)
    return f'<polygon class="cut" points="{points}" />'


def svg_circle(circle: Circle) -> str:
    return f'<circle class="cut" cx="{mm(circle.x)}" cy="{mm(circle.y)}" r="{mm(circle.r)}" />'


def svg_line(line: Line) -> str:
    return (
        f'<line class="bend" x1="{mm(line.x1)}" y1="{mm(line.y1)}" '
        f'x2="{mm(line.x2)}" y2="{mm(line.y2)}" />'
    )


def write_svg(drawing: Drawing) -> None:
    margin = 25
    width = drawing.width + margin * 2
    height = drawing.height + margin * 2 + 55
    poly_elems = "\n  ".join(svg_poly(p) for p in drawing.cut_polys)
    cut_elems = "\n  ".join(svg_rect(r, "CUT") for r in drawing.cut_rects)
    circle_elems = "\n  ".join(svg_circle(c) for c in drawing.cut_circles)
    bend_elems = "\n  ".join(svg_line(b) for b in drawing.bend_lines)
    note_y = drawing.height + margin * 2 + 20
    notes = []
    for idx, note in enumerate(drawing.notes):
        notes.append(
            f'<text x="{margin}" y="{note_y + idx * 12}" class="note">{note}</text>'
        )
    title = f"{drawing.name}  |  units: mm"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{mm(width)}mm" height="{mm(height)}mm" viewBox="0 0 {mm(width)} {mm(height)}">
  <style>
    .cut {{ fill: none; stroke: #111; stroke-width: 0.6; }}
    .aux {{ fill: none; stroke: #666; stroke-width: 0.35; }}
    .bend {{ stroke: #0b5fff; stroke-width: 0.4; stroke-dasharray: 3 2; }}
    .title {{ font: 700 9px monospace; fill: #111; }}
    .note {{ font: 6px monospace; fill: #111; }}
  </style>
  <text x="{margin}" y="14" class="title">{title}</text>
  <g transform="translate({margin},{margin})">
  {poly_elems}
  {cut_elems}
  {circle_elems}
  {bend_elems}
  </g>
  {"".join(notes)}
</svg>
"""
    (OUT_DIR / f"{drawing.name}.svg").write_text(svg, encoding="utf-8")


def dxf_header() -> list[str]:
    return [
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


def dxf_footer() -> list[str]:
    return ["0", "ENDSEC", "0", "EOF"]


def add_dxf_line(lines: list[str], x1: float, y1: float, x2: float, y2: float, layer: str) -> None:
    lines.extend(
        [
            "0",
            "LINE",
            "8",
            layer,
            "10",
            mm(x1),
            "20",
            mm(y1),
            "11",
            mm(x2),
            "21",
            mm(y2),
        ]
    )


def add_dxf_rect(lines: list[str], rect: Rect, layer: str) -> None:
    x1, y1 = rect.x, rect.y
    x2, y2 = rect.x + rect.w, rect.y + rect.h
    add_dxf_line(lines, x1, y1, x2, y1, layer)
    add_dxf_line(lines, x2, y1, x2, y2, layer)
    add_dxf_line(lines, x2, y2, x1, y2, layer)
    add_dxf_line(lines, x1, y2, x1, y1, layer)


def add_dxf_circle(lines: list[str], circle: Circle, layer: str) -> None:
    lines.extend(
        [
            "0",
            "CIRCLE",
            "8",
            layer,
            "10",
            mm(circle.x),
            "20",
            mm(circle.y),
            "40",
            mm(circle.r),
        ]
    )


def add_dxf_poly(lines: list[str], poly: Poly, layer: str) -> None:
    pts = list(poly.points)
    for idx in range(len(pts)):
        x1, y1 = pts[idx]
        x2, y2 = pts[(idx + 1) % len(pts)]
        add_dxf_line(lines, x1, y1, x2, y2, layer)


def write_dxf(drawing: Drawing) -> None:
    lines = dxf_header()
    for poly in drawing.cut_polys:
        add_dxf_poly(lines, poly, "CUT")
    for rect in drawing.cut_rects:
        add_dxf_rect(lines, rect, "CUT")
    for circle in drawing.cut_circles:
        add_dxf_circle(lines, circle, "CUT")
    for bend in drawing.bend_lines:
        add_dxf_line(lines, bend.x1, bend.y1, bend.x2, bend.y2, "BEND")
    lines.extend(dxf_footer())
    (OUT_DIR / f"{drawing.name}.dxf").write_text("\n".join(lines) + "\n", encoding="ascii")


def rounded_slot_poly(x: float, y: float, w: float, h: float, segments: int = 8) -> Poly:
    r = min(w, h) / 2
    points: list[tuple[float, float]] = []

    def add_arc(cx: float, cy: float, start: float, end: float) -> None:
        for idx in range(segments + 1):
            ang = start + ((end - start) * idx / segments)
            points.append((cx + r * cos(ang), cy + r * sin(ang)))

    add_arc(x + r, y + r, pi, 3 * pi / 2)
    add_arc(x + w - r, y + r, 3 * pi / 2, 2 * pi)
    add_arc(x + w - r, y + h - r, 0, pi / 2)
    add_arc(x + r, y + h - r, pi / 2, pi)
    return Poly(points)


def drawing_bounds(drawing: Drawing) -> tuple[float, float, float, float]:
    xs: list[float] = []
    ys: list[float] = []
    for poly in drawing.cut_polys:
        for x, y in poly.points:
            xs.append(x)
            ys.append(y)
    for rect in drawing.cut_rects:
        xs.extend([rect.x, rect.x + rect.w])
        ys.extend([rect.y, rect.y + rect.h])
    for circle in drawing.cut_circles:
        xs.extend([circle.x - circle.r, circle.x + circle.r])
        ys.extend([circle.y - circle.r, circle.y + circle.r])
    if not xs or not ys:
        return 0.0, drawing.width, 0.0, drawing.height
    return min(xs), max(xs), min(ys), max(ys)


def draw_poly(c: canvas.Canvas, poly: Poly, ox: float, oy: float, scale: float) -> None:
    path = c.beginPath()
    points = list(poly.points)
    start_x, start_y = points[0]
    path.moveTo(ox + start_x * scale, oy + start_y * scale)
    for x, y in points[1:]:
        path.lineTo(ox + x * scale, oy + y * scale)
    path.close()
    c.drawPath(path)


def draw_rect(c: canvas.Canvas, rect: Rect, ox: float, oy: float, scale: float) -> None:
    c.rect(ox + rect.x * scale, oy + rect.y * scale, rect.w * scale, rect.h * scale, stroke=1, fill=0)


def draw_circle(c: canvas.Canvas, circle: Circle, ox: float, oy: float, scale: float) -> None:
    c.circle(ox + circle.x * scale, oy + circle.y * scale, circle.r * scale, stroke=1, fill=0)


def draw_dimension_h(c: canvas.Canvas, x1: float, x2: float, y: float, text: str) -> None:
    ext = 8 * pdf_mm
    tick = 2.5 * pdf_mm
    c.setStrokeColor(HexColor("#444444"))
    c.setLineWidth(0.5)
    c.line(x1, y, x2, y)
    c.line(x1, y - tick, x1, y + tick)
    c.line(x2, y - tick, x2, y + tick)
    c.line(x1, y, x1, y + ext)
    c.line(x2, y, x2, y + ext)
    c.setFont("Helvetica", 8)
    c.drawCentredString((x1 + x2) / 2, y + 3.5 * pdf_mm, text)


def draw_dimension_v(c: canvas.Canvas, x: float, y1: float, y2: float, text: str) -> None:
    ext = 8 * pdf_mm
    tick = 2.5 * pdf_mm
    c.setStrokeColor(HexColor("#444444"))
    c.setLineWidth(0.5)
    c.line(x, y1, x, y2)
    c.line(x - tick, y1, x + tick, y1)
    c.line(x - tick, y2, x + tick, y2)
    c.line(x, y1, x - ext, y1)
    c.line(x, y2, x - ext, y2)
    c.saveState()
    c.translate(x - 4.5 * pdf_mm, (y1 + y2) / 2)
    c.rotate(90)
    c.setFont("Helvetica", 8)
    c.drawCentredString(0, 0, text)
    c.restoreState()


def draw_pdf_page(c: canvas.Canvas, drawing: Drawing) -> None:
    page_w, page_h = landscape(A4)
    margin = 14 * pdf_mm
    title_y = page_h - margin
    if "_rev_c" in drawing.name:
        rev_label = "Rev C"
    elif "_rev_b" in drawing.name:
        rev_label = "Rev B"
    else:
        rev_label = "Rev A"
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, title_y, drawing.name)
    c.setFont("Helvetica", 9)
    c.drawRightString(page_w - margin, title_y, f"{rev_label} | Units: mm | Site-fit fabrication sheet")

    gap = 8 * pdf_mm
    plot_w = 184 * pdf_mm
    notes_w = page_w - (margin * 2) - plot_w - gap
    plot_x = margin
    plot_y = 40 * pdf_mm
    plot_h = page_h - 62 * pdf_mm

    min_x, max_x, min_y, max_y = drawing_bounds(drawing)
    geom_w = max_x - min_x
    geom_h = max_y - min_y
    scale = min(plot_w / geom_w, plot_h / geom_h)
    ox = plot_x + (plot_w - geom_w * scale) / 2 - min_x * scale
    oy = plot_y + (plot_h - geom_h * scale) / 2 - min_y * scale

    c.setStrokeColor(HexColor("#111111"))
    c.setLineWidth(1)
    c.rect(plot_x, plot_y, plot_w, plot_h, stroke=1, fill=0)

    c.setStrokeColor(HexColor("#111111"))
    c.setLineWidth(0.8)
    for poly in drawing.cut_polys:
        draw_poly(c, poly, ox, oy, scale)
    for rect in drawing.cut_rects:
        draw_rect(c, rect, ox, oy, scale)
    for circle in drawing.cut_circles:
        draw_circle(c, circle, ox, oy, scale)

    c.setStrokeColor(HexColor("#0b5fff"))
    c.setLineWidth(0.6)
    c.setDash(4, 3)
    for bend in drawing.bend_lines:
        c.line(
            ox + bend.x1 * scale,
            oy + bend.y1 * scale,
            ox + bend.x2 * scale,
            oy + bend.y2 * scale,
        )
    c.setDash()

    # Overall dimensions.
    left = ox + min_x * scale
    right = ox + max_x * scale
    bottom = oy + min_y * scale
    top = oy + max_y * scale
    draw_dimension_h(c, left, right, bottom - 10 * pdf_mm, f"overall width {mm(geom_w)}")
    draw_dimension_v(c, left - 10 * pdf_mm, bottom, top, f"overall height {mm(geom_h)}")

    # Drawing-specific secondary dimensions.
    if drawing.name == "relay_module_tray_rev_a":
        draw_dimension_h(c, ox + 20 * scale, ox + 340 * scale, oy + 240 * scale + 6 * pdf_mm, "tray floor width 320")
        draw_dimension_v(c, ox + 340 * scale + 10 * pdf_mm, oy + 20 * scale, oy + 240 * scale, "tray floor depth 220")
        draw_dimension_h(c, ox + 90 * scale, ox + 270 * scale, oy + 115 * scale - 8 * pdf_mm, "loom slot 180")
        draw_dimension_v(c, ox + 270 * scale + 10 * pdf_mm, oy + 115 * scale, oy + 145 * scale, "loom slot 30")
    elif drawing.name == "power_module_box_rev_a":
        draw_dimension_h(c, ox + 20 * scale, ox + 240 * scale, oy + 160 * scale + 6 * pdf_mm, "box face width 220")
        draw_dimension_v(c, ox + 240 * scale + 10 * pdf_mm, oy + 20 * scale, oy + 160 * scale, "box face height 140")
        draw_dimension_h(c, ox + 25 * scale, ox + 155 * scale, oy + 48 * scale - 8 * pdf_mm, "MIDI slot length 130")
        draw_dimension_v(c, ox + 183.5 * scale + 10 * pdf_mm, oy + 42 * scale, oy + 68 * scale, "breaker slot 26")
    elif drawing.name == "power_module_rear_insulator_rev_a":
        draw_dimension_h(c, ox, ox + 210 * scale, oy + 130 * scale + 6 * pdf_mm, "panel width 210")
        draw_dimension_v(c, ox + 210 * scale + 10 * pdf_mm, oy, oy + 130 * scale, "panel height 130")
        draw_dimension_h(c, ox + 42 * scale, ox + 70 * scale, oy + 116 * scale - 8 * pdf_mm, "cable slot 28")
        draw_dimension_v(c, ox + 70 * scale + 10 * pdf_mm, oy + 116 * scale, oy + 124 * scale, "cable slot 8")
    elif drawing.name == "midi5_module_box_rev_a":
        draw_dimension_h(c, ox + 20 * scale, ox + 280 * scale, oy + 160 * scale + 6 * pdf_mm, "box face width 260")
        draw_dimension_v(c, ox + 280 * scale + 10 * pdf_mm, oy + 20 * scale, oy + 160 * scale, "box face height 140")
        draw_dimension_h(c, ox + 45 * scale, ox + 215 * scale, oy + 30 * scale - 8 * pdf_mm, "holder-board hole span 170")
        draw_dimension_v(c, ox + 215 * scale + 10 * pdf_mm, oy + 30 * scale, oy + 110 * scale, "holder-board hole span 80")
    elif drawing.name == "midi5_holder_subplate_rev_a":
        draw_dimension_h(c, ox, ox + 230 * scale, oy + 100 * scale + 6 * pdf_mm, "board width 230")
        draw_dimension_v(c, ox + 230 * scale + 10 * pdf_mm, oy, oy + 100 * scale, "board height 100")
        draw_dimension_h(c, ox + 15 * scale, ox + 185 * scale, oy + 10 * scale - 8 * pdf_mm, "mount-hole span 170")
        draw_dimension_v(c, ox + 185 * scale + 10 * pdf_mm, oy + 10 * scale, oy + 90 * scale, "mount-hole span 80")
        draw_dimension_h(c, ox + 25 * scale, ox + 185 * scale, oy + 18 * scale - 16 * pdf_mm, "holder slot-field span 160")
        draw_dimension_v(c, ox + 199 * scale + 10 * pdf_mm, oy + 21 * scale, oy + 79 * scale, "slot-row span 58")
    elif drawing.name == "midi5_module_rear_insulator_rev_a":
        draw_dimension_h(c, ox, ox + 220 * scale, oy + 100 * scale + 6 * pdf_mm, "panel width 220")
        draw_dimension_v(c, ox + 220 * scale + 10 * pdf_mm, oy, oy + 100 * scale, "panel height 100")
        draw_dimension_h(c, ox + 55 * scale, ox + 195 * scale, oy + 25 * scale - 8 * pdf_mm, "5-output spread 140")
        draw_dimension_v(c, ox + 28 * scale + 18 * pdf_mm, oy + 55.5 * scale, oy + 80.5 * scale, "main feed hole dia 25")
        draw_dimension_v(c, ox + 195 * scale + 10 * pdf_mm, oy + 17 * scale, oy + 33 * scale, "branch hole dia 16")
    elif drawing.name == "midi5_module_box_rev_b":
        draw_dimension_h(c, ox + 20 * scale, ox + 200 * scale, oy + 140 * scale + 6 * pdf_mm, "box face width 180")
        draw_dimension_v(c, ox + 200 * scale + 10 * pdf_mm, oy + 20 * scale, oy + 140 * scale, "box face height 120")
        draw_dimension_h(c, ox + 35 * scale, ox + 145 * scale, oy + 30 * scale - 8 * pdf_mm, "subplate mount span 110")
        draw_dimension_v(c, ox + 145 * scale + 10 * pdf_mm, oy + 30 * scale, oy + 110 * scale, "subplate mount span 80")
    elif drawing.name == "midi5_holder_subplate_rev_b":
        draw_dimension_h(c, ox, ox + 140 * scale, oy + 85 * scale + 6 * pdf_mm, "board width 140")
        draw_dimension_v(c, ox + 140 * scale + 10 * pdf_mm, oy, oy + 85 * scale, "board height 85")
        draw_dimension_h(c, ox + 11.0 * scale, ox + 91.8 * scale, oy + 20 * scale - 12 * pdf_mm, "left-row pitch span 80.8")
        draw_dimension_h(c, ox + 21.0 * scale, ox + 101.8 * scale, oy + 64 * scale - 12 * pdf_mm, "right-row pitch span 80.8")
        draw_dimension_v(c, ox + 101.8 * scale + 10 * pdf_mm, oy + 20 * scale, oy + 64 * scale, "ear-row span 44")
        draw_dimension_h(c, ox + 11.0 * scale, ox + 21.0 * scale, oy + 42 * scale + 10 * pdf_mm, "row stagger 10")
    elif drawing.name == "midi5_module_rear_insulator_rev_b":
        draw_dimension_h(c, ox, ox + 170 * scale, oy + 90 * scale + 6 * pdf_mm, "panel width 170")
        draw_dimension_v(c, ox + 170 * scale + 10 * pdf_mm, oy, oy + 90 * scale, "panel height 90")
        draw_dimension_h(c, ox + 21 * scale, ox + 101.8 * scale, oy + 26 * scale - 8 * pdf_mm, "5-output spread 80.8")
        draw_dimension_v(c, ox + 142 * scale + 18 * pdf_mm, oy + 46 * scale, oy + 66 * scale, "main feed hole dia 20")
        draw_dimension_v(c, ox + 101.8 * scale + 10 * pdf_mm, oy + 20 * scale, oy + 32 * scale, "branch hole dia 12")
    elif drawing.name == "midi5_mount_plate_rev_c":
        draw_dimension_h(c, ox, ox + 190 * scale, oy + 150 * scale + 6 * pdf_mm, "plate width 190")
        draw_dimension_v(c, ox + 190 * scale + 10 * pdf_mm, oy, oy + 150 * scale, "plate height 150")
        draw_dimension_h(c, ox + 32.5 * scale, ox + 157.5 * scale, oy + 37.5 * scale - 10 * pdf_mm, "standoff span 125")
        draw_dimension_v(c, ox + 157.5 * scale + 10 * pdf_mm, oy + 37.5 * scale, oy + 112.5 * scale, "standoff span 75")
    elif drawing.name == "midi5_holder_subplate_rev_c":
        draw_dimension_h(c, ox, ox + 140 * scale, oy + 85 * scale + 6 * pdf_mm, "board width 140")
        draw_dimension_v(c, ox + 140 * scale + 10 * pdf_mm, oy, oy + 85 * scale, "board height 85")
        draw_dimension_h(c, ox + 11.0 * scale, ox + 91.8 * scale, oy + 20 * scale - 12 * pdf_mm, "left-row pitch span 80.8")
        draw_dimension_h(c, ox + 21.0 * scale, ox + 101.8 * scale, oy + 64 * scale - 12 * pdf_mm, "right-row pitch span 80.8")
        draw_dimension_v(c, ox + 101.8 * scale + 10 * pdf_mm, oy + 20 * scale, oy + 64 * scale, "ear-row span 44")
        draw_dimension_h(c, ox + 11.0 * scale, ox + 21.0 * scale, oy + 42 * scale + 10 * pdf_mm, "row stagger 10")
    elif drawing.name == "relay_carrier_rev_c":
        draw_dimension_h(c, ox + 20 * scale, ox + 340 * scale, oy + 235 * scale + 6 * pdf_mm, "carrier face width 320")
        draw_dimension_v(c, ox + 340 * scale + 10 * pdf_mm, oy + 15 * scale, oy + 235 * scale, "carrier face height 220")
        draw_dimension_h(c, ox + 100 * scale, ox + 240 * scale, oy + 193 * scale - 10 * pdf_mm, "loom slot 140")
        draw_dimension_v(c, ox + 240 * scale + 10 * pdf_mm, oy + 193 * scale, oy + 219 * scale, "loom slot 26")
    elif drawing.name == "relay_rear_guard_rev_c":
        draw_dimension_h(c, ox, ox + 280 * scale, oy + 185 * scale + 6 * pdf_mm, "guard width 280")
        draw_dimension_v(c, ox + 280 * scale + 10 * pdf_mm, oy, oy + 185 * scale, "guard height 185")
        draw_dimension_h(c, ox + 80 * scale, ox + 200 * scale, oy + 160 * scale - 10 * pdf_mm, "bottom opening width 120")
        draw_dimension_v(c, ox + 200 * scale + 10 * pdf_mm, oy + 160 * scale, oy + 185 * scale, "bottom opening depth 25")

    # Right-hand notes column.
    notes_x = plot_x + plot_w + gap
    notes_y = page_h - 26 * pdf_mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(notes_x, notes_y, "Fabrication Notes")
    c.setFont("Helvetica", 9)
    row = 0

    def draw_wrapped_bullet(text: str) -> None:
        nonlocal row
        wrapped = simpleSplit(f"- {text}", "Helvetica", 9, notes_w)
        for line in wrapped:
            c.drawString(notes_x, notes_y - (row + 1) * 5.3 * pdf_mm, line)
            row += 1
        row += 0.2

    for note in drawing.notes:
        draw_wrapped_bullet(note)
    extra_notes = [
        "Truck-side pickup slots stay provisional until tray repair and site-fit.",
        "Confirm actual component hole positions against the parts in hand before final paint or powder.",
    ]
    if drawing.bend_lines:
        extra_notes.insert(0, "Bend all blue dashed lines to 90 degrees.")
    else:
        extra_notes.insert(0, "No bends in this part.")
    for note in extra_notes:
        draw_wrapped_bullet(note)

    c.setFont("Helvetica-Bold", 11)
    c.drawString(notes_x, notes_y - (row + 2) * 5.3 * pdf_mm, "Output Files")
    c.setFont("Helvetica", 9)
    c.drawString(notes_x, notes_y - (row + 3) * 5.3 * pdf_mm, f"- DXF: {drawing.name}.dxf")
    c.drawString(notes_x, notes_y - (row + 4) * 5.3 * pdf_mm, f"- SVG: {drawing.name}.svg")

    c.setFont("Helvetica", 8)
    c.drawString(margin, 9 * pdf_mm, "Prepared from J40 bay photos and product dimensions gathered in-thread.")
    c.drawRightString(page_w - margin, 9 * pdf_mm, f"Output: {PDF_NAME}")
    c.showPage()


def write_pdf(drawings: Sequence[Drawing]) -> None:
    pdf_path = OUT_DIR / PDF_NAME
    c = canvas.Canvas(str(pdf_path), pagesize=landscape(A4))
    for drawing in drawings:
        draw_pdf_page(c, drawing)
    c.save()


def relay_module_tray() -> Drawing:
    # Blank: 360 x 260, made as a cross with 20 mm flanges around a 320 x 220 tray floor.
    cut_polys = [
        Poly(
            [
                (20, 0),
                (340, 0),
                (340, 20),
                (360, 20),
                (360, 240),
                (340, 240),
                (340, 260),
                (20, 260),
                (20, 240),
                (0, 240),
                (0, 20),
                (20, 20),
            ]
        )
    ]
    cut_rects: list[Rect] = []
    cut_polys.extend(
        [
            rounded_slot_poly(34, 42, 18, 9),
            rounded_slot_poly(308, 42, 18, 9),
            rounded_slot_poly(34, 209, 18, 9),
            rounded_slot_poly(308, 209, 18, 9),
            rounded_slot_poly(90, 115, 180, 30),
            rounded_slot_poly(72, 6, 16, 8),
            rounded_slot_poly(272, 6, 16, 8),
            rounded_slot_poly(72, 246, 16, 8),
            rounded_slot_poly(272, 246, 16, 8),
            rounded_slot_poly(6, 122, 8, 16),
            rounded_slot_poly(346, 122, 8, 16),
        ]
    )
    bend_lines = [
        Line(20, 20, 340, 20),
        Line(20, 240, 340, 240),
        Line(20, 20, 20, 240),
        Line(340, 20, 340, 240),
    ]
    notes = [
        "Relay module tray: 3.0 mm 5052-H32 aluminium. Finished tray floor 320 x 220. Flanges 20 mm down.",
        "Relay slots are provisional image-derived pattern for DAIER RB-R10F10-W1; verify with actual box before final bend.",
        "Main loom opening is now a radiused slot to reduce chafing risk at the relay-box cable exit.",
        "All vehicle-side mount slots are intentionally generic for site-fit to the repaired tray/front rail/inner-wing structure.",
    ]
    return Drawing("relay_module_tray_rev_a", 360, 260, cut_polys, cut_rects, [], bend_lines, notes)


def power_module_box() -> Drawing:
    # Blank: 260 x 180, 20 mm flanges around a 220 x 140 front face.
    cut_polys = [
        Poly(
            [
                (20, 0),
                (240, 0),
                (240, 20),
                (260, 20),
                (260, 160),
                (240, 160),
                (240, 180),
                (20, 180),
                (20, 160),
                (0, 160),
                (0, 20),
                (20, 20),
            ]
        )
    ]
    cut_rects: list[Rect] = []
    cut_polys.extend(
        [
            rounded_slot_poly(25, 48, 130, 6),
            rounded_slot_poly(25, 102, 130, 6),
            rounded_slot_poly(176.5, 42, 7, 26),
            rounded_slot_poly(176.5, 92, 7, 26),
            rounded_slot_poly(62, 6, 16, 8),
            rounded_slot_poly(182, 6, 16, 8),
            rounded_slot_poly(62, 166, 16, 8),
            rounded_slot_poly(182, 166, 16, 8),
            rounded_slot_poly(6, 82, 8, 16),
            rounded_slot_poly(246, 82, 8, 16),
        ]
    )
    cut_circles = [
        Circle(60, 10, 2.25),
        Circle(200, 10, 2.25),
        Circle(60, 170, 2.25),
        Circle(200, 170, 2.25),
        Circle(10, 90, 2.25),
        Circle(250, 90, 2.25),
    ]
    bend_lines = [
        Line(20, 20, 240, 20),
        Line(20, 160, 240, 160),
        Line(20, 20, 20, 160),
        Line(240, 20, 240, 160),
    ]
    notes = [
        "Power module box: 3.0 mm 5052-H32 aluminium. Finished face 220 x 140. Flanges 20 mm back.",
        "Left slot pair is a universal MIDI mounting field for the grouped bank. Use clamp strips and M5 hardware after physical test-fit.",
        "Right slot pair is a universal breaker field. Confirm stud and hole geometry on the actual 100 A breaker before paint.",
        "Rear cover screw positions are now shown as true 4.5 mm circular holes rather than square placeholders.",
    ]
    return Drawing("power_module_box_rev_a", 260, 180, cut_polys, cut_rects, cut_circles, bend_lines, notes)


def power_module_rear_insulator() -> Drawing:
    cut_polys = [Poly([(0, 0), (210, 0), (210, 130), (0, 130)])]
    cut_rects: list[Rect] = []
    cut_polys.extend(
        [
            rounded_slot_poly(42, 116, 28, 8),
            rounded_slot_poly(140, 116, 28, 8),
        ]
    )
    cut_circles = [
        Circle(35, 5, 2.25),
        Circle(175, 5, 2.25),
        Circle(35, 125, 2.25),
        Circle(175, 125, 2.25),
        Circle(5, 65, 2.25),
        Circle(205, 65, 2.25),
    ]
    notes = [
        "Power module rear insulator: 3.0 mm ABS, HDPE, or polypropylene. Do not make this part from bare metal.",
        "Mount on 10-12 mm nylon spacers behind the power-module box to shield live studs while leaving a bottom drain gap.",
        "Bottom cable exits are radiused slots rather than sharp-edged notches to reduce loom abrasion.",
    ]
    return Drawing("power_module_rear_insulator_rev_a", 210, 130, cut_polys, cut_rects, cut_circles, [], notes)


def write_readme(drawings: Iterable[Drawing]) -> None:
    text = """# J40 Electrical Module Fabrication Pack - Rev A

This pack is a provisional fabrication set for two under-bonnet electrical modules:

1. `relay_module_tray_rev_a`
2. `power_module_box_rev_a`
3. `power_module_rear_insulator_rev_a`

All dimensions are in millimetres.

## Recommended file to send to the fabricator

Send the `DXF` files for cutting, the matching `SVG` files for human review, and the PDF sheet for non-CAD review.

## Design intent

- `relay_module_tray_rev_a` is the relay-box shelf ahead of the battery.
- `power_module_box_rev_a` is the smaller side module for the breaker and grouped MIDI bank.
- `power_module_rear_insulator_rev_a` is the non-metal rear shield for the power module.

## Material callouts

- Relay tray: `3.0 mm 5052-H32 aluminium`
- Power module box: `3.0 mm 5052-H32 aluminium`
- Rear insulator: `3.0 mm ABS, HDPE, or polypropylene`

## Bend notes

- Bend all bend-line flanges to `90 degrees`.
- Target inside bend radius: `3 mm` nominal.
- Corner relief is open-corner style by design; no corner welding is required.

## Hardware assumptions

- Relay box housing used for sizing: `300 x 197 x 80 mm`
- Relay box mount pattern remains image-derived and is therefore slotted on purpose.
- Breaker body used for sizing: `74 x 49 x 45 mm`
- MIDI grouped bank is treated as a slotted universal field because the exact AliExpress mounting pattern was not published.

## Vehicle-side fitment

The truck-side pickup points are intentionally slotted rather than final-drilled because:

- the battery tray shown in the photos is not yet a trusted structural reference
- the final repaired tray and inner-wing support positions need to be confirmed on the truck
- a fabricator can site-fit tabs or stand-offs after mock-up

## Installation guidance

- Rebuild or brace the battery tray before installing the relay tray.
- Mount the relay tray with at least `3` structural pickups: tray/front-rail, inner-wing side, and one forward support if available.
- Mount the power module on the inner-fender side of the battery area with the breaker reset lever facing upward.
- Use insulated boots on all live studs.
- Use clamp strips with the MIDI slot field if the supplied fuse bank does not have a strong mounting flange.

## Source basis

- Relay box dimensions from the DAIER / AliExpress relay-box listing used earlier in this thread.
- Breaker body dimensions from the Mughal Electronics product page used earlier in this thread.
- MIDI holder sizing informed by Littelfuse MIDI-Flex holder dimensions (`78.4 x 29.9 x 38.3 mm`) and a 5-position grouped layout.
"""
    (OUT_DIR / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    drawings = [
        relay_module_tray(),
        power_module_box(),
        power_module_rear_insulator(),
    ]
    for drawing in drawings:
        write_svg(drawing)
        write_dxf(drawing)
    write_pdf(drawings)
    write_readme(drawings)


if __name__ == "__main__":
    main()
