from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin
from pathlib import Path
from typing import Iterable, Sequence

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm as pdf_mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "manual" / "fabrication" / "rubber_recreation_rev_a"
PDF_NAME = "j40_rubber_recreation_rev_a_dimension_sheet.pdf"


@dataclass(frozen=True)
class Circle:
    x: float
    y: float
    r: float
    layer: str


@dataclass(frozen=True)
class Poly:
    points: Sequence[tuple[float, float]]
    layer: str


@dataclass(frozen=True)
class Line:
    x1: float
    y1: float
    x2: float
    y2: float
    layer: str


@dataclass(frozen=True)
class Drawing:
    name: str
    title: str
    width: float
    height: float
    qty: str
    material: str
    release_status: str
    circles: Sequence[Circle]
    polys: Sequence[Poly]
    lines: Sequence[Line]
    notes: Sequence[str]


def mm(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


LAYER_STYLES = {
    "CUT": {"svg": "cut", "color": "#111111", "dash": None},
    "CUT_BORE": {"svg": "cut", "color": "#111111", "dash": None},
    "CUT_RELIEF": {"svg": "relief", "color": "#111111", "dash": None},
    "DRILL": {"svg": "drill", "color": "#111111", "dash": None},
    "FORM": {"svg": "form", "color": "#0b5fff", "dash": (4, 3)},
    "RECESS": {"svg": "form", "color": "#0b5fff", "dash": (4, 3)},
    "INSERT_MARK": {"svg": "mark", "color": "#8a5a00", "dash": (3, 2)},
    "TEMPLATE": {"svg": "template", "color": "#7a1f8a", "dash": (5, 3)},
    "CENTER": {"svg": "center", "color": "#777777", "dash": (2, 2)},
}


def rounded_rect_poly(x: float, y: float, w: float, h: float, r: float, layer: str, segments: int = 8) -> Poly:
    r = min(r, w / 2, h / 2)
    points: list[tuple[float, float]] = []

    def add_arc(cx: float, cy: float, start: float, end: float) -> None:
        for idx in range(segments + 1):
            ang = start + ((end - start) * idx / segments)
            points.append((cx + r * cos(ang), cy + r * sin(ang)))

    add_arc(x + r, y + r, pi, 3 * pi / 2)
    add_arc(x + w - r, y + r, 3 * pi / 2, 2 * pi)
    add_arc(x + w - r, y + h - r, 0, pi / 2)
    add_arc(x + r, y + h - r, pi / 2, pi)
    return Poly(points, layer)


def capsule_poly(x: float, y: float, w: float, h: float, layer: str, segments: int = 18) -> Poly:
    r = min(w, h) / 2
    points: list[tuple[float, float]] = []

    if h >= w:
        cx = x + w / 2
        top_cy = y + r
        bottom_cy = y + h - r
        for idx in range(segments + 1):
            ang = pi + pi * idx / segments
            points.append((cx + r * cos(ang), top_cy + r * sin(ang)))
        for idx in range(segments + 1):
            ang = pi * idx / segments
            points.append((cx + r * cos(ang), bottom_cy + r * sin(ang)))
    else:
        cy = y + h / 2
        left_cx = x + r
        right_cx = x + w - r
        for idx in range(segments + 1):
            ang = pi / 2 + pi * idx / segments
            points.append((left_cx + r * cos(ang), cy + r * sin(ang)))
        for idx in range(segments + 1):
            ang = -pi / 2 + pi * idx / segments
            points.append((right_cx + r * cos(ang), cy + r * sin(ang)))
    return Poly(points, layer)


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


def add_dxf_line(lines: list[str], line: Line) -> None:
    lines.extend(
        [
            "0",
            "LINE",
            "8",
            line.layer,
            "10",
            mm(line.x1),
            "20",
            mm(line.y1),
            "11",
            mm(line.x2),
            "21",
            mm(line.y2),
        ]
    )


def add_dxf_circle(lines: list[str], circle: Circle) -> None:
    lines.extend(
        [
            "0",
            "CIRCLE",
            "8",
            circle.layer,
            "10",
            mm(circle.x),
            "20",
            mm(circle.y),
            "40",
            mm(circle.r),
        ]
    )


def add_dxf_poly(lines: list[str], poly: Poly) -> None:
    points = list(poly.points)
    for idx, (x1, y1) in enumerate(points):
        x2, y2 = points[(idx + 1) % len(points)]
        add_dxf_line(lines, Line(x1, y1, x2, y2, poly.layer))


def write_dxf(drawing: Drawing) -> None:
    lines = dxf_header()
    for poly in drawing.polys:
        add_dxf_poly(lines, poly)
    for circle in drawing.circles:
        add_dxf_circle(lines, circle)
    for line in drawing.lines:
        add_dxf_line(lines, line)
    lines.extend(dxf_footer())
    (OUT_DIR / f"{drawing.name}.dxf").write_text("\n".join(lines) + "\n", encoding="ascii")


def svg_poly(poly: Poly) -> str:
    cls = LAYER_STYLES.get(poly.layer, LAYER_STYLES["CUT"])["svg"]
    points = " ".join(f"{mm(x)},{mm(y)}" for x, y in poly.points)
    return f'<polygon class="{cls}" points="{points}" />'


def svg_circle(circle: Circle) -> str:
    cls = LAYER_STYLES.get(circle.layer, LAYER_STYLES["CUT"])["svg"]
    return f'<circle class="{cls}" cx="{mm(circle.x)}" cy="{mm(circle.y)}" r="{mm(circle.r)}" />'


def svg_line(line: Line) -> str:
    cls = LAYER_STYLES.get(line.layer, LAYER_STYLES["CUT"])["svg"]
    return (
        f'<line class="{cls}" x1="{mm(line.x1)}" y1="{mm(line.y1)}" '
        f'x2="{mm(line.x2)}" y2="{mm(line.y2)}" />'
    )


def write_svg(drawing: Drawing) -> None:
    margin = 24
    note_y = drawing.height + margin * 2 + 18
    width = drawing.width + margin * 2
    height = drawing.height + margin * 2 + 72
    elems = [
        *(svg_poly(poly) for poly in drawing.polys),
        *(svg_circle(circle) for circle in drawing.circles),
        *(svg_line(line) for line in drawing.lines),
    ]
    notes = [
        f'<text x="{margin}" y="{note_y + idx * 10}" class="note">{escape_xml(note)}</text>'
        for idx, note in enumerate(drawing.notes[:4])
    ]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{mm(width)}mm" height="{mm(height)}mm" viewBox="0 0 {mm(width)} {mm(height)}">
  <style>
    .cut {{ fill: none; stroke: #111; stroke-width: 0.5; }}
    .drill {{ fill: none; stroke: #111; stroke-width: 0.5; }}
    .relief {{ fill: none; stroke: #111; stroke-width: 0.5; }}
    .form {{ fill: none; stroke: #0b5fff; stroke-width: 0.4; stroke-dasharray: 4 3; }}
    .mark {{ fill: none; stroke: #8a5a00; stroke-width: 0.4; stroke-dasharray: 3 2; }}
    .template {{ fill: none; stroke: #7a1f8a; stroke-width: 0.45; stroke-dasharray: 5 3; }}
    .center {{ stroke: #777; stroke-width: 0.25; stroke-dasharray: 2 2; }}
    .title {{ font: 700 7px monospace; fill: #111; }}
    .note {{ font: 4.8px monospace; fill: #111; }}
  </style>
  <text x="{margin}" y="14" class="title">{escape_xml(drawing.title)} | qty {escape_xml(drawing.qty)} | units: mm</text>
  <g transform="translate({margin},{margin})">
  {"".join(elems)}
  </g>
  {"".join(notes)}
</svg>
"""
    (OUT_DIR / f"{drawing.name}.svg").write_text(svg, encoding="utf-8")


def escape_xml(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def bounds(drawing: Drawing) -> tuple[float, float, float, float]:
    xs: list[float] = []
    ys: list[float] = []
    for poly in drawing.polys:
        for x, y in poly.points:
            xs.append(x)
            ys.append(y)
    for circle in drawing.circles:
        xs.extend([circle.x - circle.r, circle.x + circle.r])
        ys.extend([circle.y - circle.r, circle.y + circle.r])
    for line in drawing.lines:
        xs.extend([line.x1, line.x2])
        ys.extend([line.y1, line.y2])
    return min(xs), max(xs), min(ys), max(ys)


def set_layer_style(c: canvas.Canvas, layer: str) -> None:
    style = LAYER_STYLES.get(layer, LAYER_STYLES["CUT"])
    c.setStrokeColor(HexColor(style["color"]))
    c.setLineWidth(0.7 if layer.startswith("CUT") or layer == "DRILL" else 0.45)
    dash = style["dash"]
    if dash:
        c.setDash(*dash)
    else:
        c.setDash()


def draw_poly(c: canvas.Canvas, poly: Poly, ox: float, oy: float, scale: float) -> None:
    set_layer_style(c, poly.layer)
    path = c.beginPath()
    points = list(poly.points)
    path.moveTo(ox + points[0][0] * scale, oy + points[0][1] * scale)
    for x, y in points[1:]:
        path.lineTo(ox + x * scale, oy + y * scale)
    path.close()
    c.drawPath(path, stroke=1, fill=0)


def draw_circle(c: canvas.Canvas, circle: Circle, ox: float, oy: float, scale: float) -> None:
    set_layer_style(c, circle.layer)
    c.circle(ox + circle.x * scale, oy + circle.y * scale, circle.r * scale, stroke=1, fill=0)


def draw_line(c: canvas.Canvas, line: Line, ox: float, oy: float, scale: float) -> None:
    set_layer_style(c, line.layer)
    c.line(ox + line.x1 * scale, oy + line.y1 * scale, ox + line.x2 * scale, oy + line.y2 * scale)


def draw_dimension_h(c: canvas.Canvas, x1: float, x2: float, y: float, text: str) -> None:
    c.setStrokeColor(HexColor("#444444"))
    c.setDash()
    c.setLineWidth(0.45)
    tick = 2.2 * pdf_mm
    c.line(x1, y, x2, y)
    c.line(x1, y - tick, x1, y + tick)
    c.line(x2, y - tick, x2, y + tick)
    c.setFont("Helvetica", 7)
    c.drawCentredString((x1 + x2) / 2, y + 2.8 * pdf_mm, text)


def draw_dimension_v(c: canvas.Canvas, x: float, y1: float, y2: float, text: str) -> None:
    c.setStrokeColor(HexColor("#444444"))
    c.setDash()
    c.setLineWidth(0.45)
    tick = 2.2 * pdf_mm
    c.line(x, y1, x, y2)
    c.line(x - tick, y1, x + tick, y1)
    c.line(x - tick, y2, x + tick, y2)
    c.saveState()
    c.translate(x - 4 * pdf_mm, (y1 + y2) / 2)
    c.rotate(90)
    c.setFont("Helvetica", 7)
    c.drawCentredString(0, 0, text)
    c.restoreState()


def draw_pdf_page(c: canvas.Canvas, drawing: Drawing) -> None:
    page_w, page_h = landscape(A4)
    margin = 13 * pdf_mm
    c.setFont("Helvetica-Bold", 15)
    c.drawString(margin, page_h - margin, drawing.title)
    c.setFont("Helvetica", 8)
    c.drawRightString(page_w - margin, page_h - margin, "Rev A | units: mm | rubber recreation fabrication pack")

    plot_w = 172 * pdf_mm
    plot_h = page_h - 64 * pdf_mm
    plot_x = margin
    plot_y = 38 * pdf_mm
    note_x = plot_x + plot_w + 10 * pdf_mm
    note_w = page_w - note_x - margin

    min_x, max_x, min_y, max_y = bounds(drawing)
    geom_w = max_x - min_x
    geom_h = max_y - min_y
    scale = min(plot_w / max(geom_w, 1), plot_h / max(geom_h, 1))
    ox = plot_x + (plot_w - geom_w * scale) / 2 - min_x * scale
    oy = plot_y + (plot_h - geom_h * scale) / 2 - min_y * scale

    c.setStrokeColor(HexColor("#111111"))
    c.setLineWidth(0.8)
    c.rect(plot_x, plot_y, plot_w, plot_h, stroke=1, fill=0)
    for poly in drawing.polys:
        draw_poly(c, poly, ox, oy, scale)
    for circle in drawing.circles:
        draw_circle(c, circle, ox, oy, scale)
    for line in drawing.lines:
        draw_line(c, line, ox, oy, scale)
    c.setDash()

    left = ox + min_x * scale
    right = ox + max_x * scale
    bottom = oy + min_y * scale
    top = oy + max_y * scale
    draw_dimension_h(c, left, right, bottom - 9 * pdf_mm, f"overall width {mm(geom_w)}")
    draw_dimension_v(c, left - 9 * pdf_mm, bottom, top, f"overall height {mm(geom_h)}")

    row_y = page_h - 28 * pdf_mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(note_x, row_y, "Part Control")
    c.setFont("Helvetica", 8.5)
    controls = [
        f"Quantity: {drawing.qty}",
        f"Material: {drawing.material}",
        f"Release: {drawing.release_status}",
        f"DXF: {drawing.name}.dxf",
        f"SVG: {drawing.name}.svg",
    ]
    row = 1
    for control in controls:
        c.drawString(note_x, row_y - row * 5 * pdf_mm, f"- {control}")
        row += 1

    c.setFont("Helvetica-Bold", 10)
    c.drawString(note_x, row_y - (row + 1) * 5 * pdf_mm, "Fabrication Notes")
    row += 2
    c.setFont("Helvetica", 8.5)
    for note in drawing.notes:
        for line in simpleSplit(f"- {note}", "Helvetica", 8.5, note_w):
            c.drawString(note_x, row_y - row * 5 * pdf_mm, line)
            row += 1
        row += 0.2

    c.setFont("Helvetica-Bold", 9)
    c.drawString(note_x, 29 * pdf_mm, "DXF layer meaning")
    c.setFont("Helvetica", 7.8)
    legend = [
        "CUT/CUT_BORE/DRILL: through cut or through hole",
        "RECESS/FORM/INSERT_MARK: mark, form, boss, or pocket control",
        "TEMPLATE: quote/trace guide, not final cut without physical trace",
        "CENTER: construction centerline only",
    ]
    for idx, item in enumerate(legend):
        c.drawString(note_x, (24 - idx * 4) * pdf_mm, f"- {item}")

    c.setFont("Helvetica", 7.5)
    c.drawString(margin, 8 * pdf_mm, "Prepared from May 2 rubber sample photos and rubber_recreation_* control tables.")
    c.drawRightString(page_w - margin, 8 * pdf_mm, f"Output: {PDF_NAME}")
    c.showPage()


def write_pdf(drawings: Sequence[Drawing]) -> None:
    c = canvas.Canvas(str(OUT_DIR / PDF_NAME), pagesize=landscape(A4))
    for drawing in drawings:
        draw_pdf_page(c, drawing)
    c.save()


def circular_mount(name: str, title: str, od: float, height: str, qty: str, status: str) -> Drawing:
    centre = od / 2
    return Drawing(
        name=name,
        title=title,
        width=od,
        height=od,
        qty=qty,
        material="Black EPDM or NR/SBR, Shore A 60 +/-5",
        release_status=status,
        circles=[
            Circle(centre, centre, od / 2, "CUT"),
            Circle(centre, centre, 16, "CUT_BORE"),
            Circle(centre, centre, 23, "RECESS"),
        ],
        polys=[],
        lines=[
            Line(centre, 0, centre, od, "CENTER"),
            Line(0, centre, od, centre, "CENTER"),
        ],
        notes=[
            f"Finished free height: {height}. The DXF is the top cut profile only; height is controlled by the PDF and cut list.",
            "Central through bore is 32 mm. The 46 mm register circle is a recess/seat control mark, not a through cut unless the physical sample proves otherwise.",
            "Outer load edge radius target R2-R3. Faces flat and parallel within 0.5 mm. Bore/register concentricity <=1.0 mm.",
            "Use same rubber compound batch for each matched family. Reject tyre rubber, crumb rubber, sponge, or unmarked offcuts.",
        ],
    )


def cup_washer(name: str, title: str, od: float, qty: str) -> Drawing:
    centre = od / 2
    return Drawing(
        name=name,
        title=title,
        width=od,
        height=od,
        qty=qty,
        material="2.5-3.0 mm steel, zinc plated or epoxy primed after forming",
        release_status="prototype/quote; confirm cup reuse and dish depth before batch",
        circles=[
            Circle(centre, centre, od / 2, "CUT"),
            Circle(centre, centre, 5.5, "DRILL"),
            Circle(centre, centre, 23, "FORM"),
        ],
        polys=[],
        lines=[
            Line(centre, 0, centre, od, "CENTER"),
            Line(0, centre, od, centre, "CENTER"),
        ],
        notes=[
            "M10 clearance hole is 11 mm through. The 46 mm circle is the register/dish forming line.",
            "Dish/register depth target is 2-3 mm after forming. Cup must seat the rubber without rocking.",
            "Reuse original cups only if flat, not thinned, and not cracked. Otherwise form new cups from these blanks.",
            "Deburr, plate/prime, and trial stack with the rubber cushion and sleeve before body installation.",
        ],
    )


def fs_oval() -> Drawing:
    return Drawing(
        name="fs_oval_front_support_pad_rev_a",
        title="FS-OVAL front support two-hole isolator pad",
        width=64,
        height=96,
        qty="2 matched pieces",
        material="Black EPDM or NR/SBR, Shore A 60 +/-5; reuse/bond steel insert if present",
        release_status="prototype/quote; caliper-confirm holes and insert before batch",
        polys=[
            capsule_poly(0, 0, 64, 96, "CUT"),
            rounded_rect_poly(14, 39, 36, 18, 3, "CUT_RELIEF"),
        ],
        circles=[
            Circle(32, 16, 6, "CUT_BORE"),
            Circle(32, 80, 6, "CUT_BORE"),
            Circle(32, 16, 14.5, "INSERT_MARK"),
        ],
        lines=[
            Line(32, 0, 32, 96, "CENTER"),
            Line(0, 16, 64, 16, "CENTER"),
            Line(0, 80, 64, 80, "CENTER"),
        ],
        notes=[
            "Overall 96 x 64 with two 12 mm holes on 64 mm centre spacing.",
            "The 36 x 18 R3 relief is shown as a cut/pocket control. Confirm whether it is through-cut or blind relief on the physical part.",
            "Top 29 mm insert/boss mark is not a through cut. Reuse or reproduce the metal insert if the original design uses one.",
            "Make the two pads as a matched pair and dry-fit the front support before accepting the batch.",
        ],
    )


def strip_template(name: str, title: str) -> Drawing:
    return Drawing(
        name=name,
        title=title,
        width=165,
        height=40,
        qty="1",
        material="8 mm base / 14 mm raised-load EPDM or NR/SBR strip, Shore A 60 +/-5",
        release_status="template required; this file is a quote blank, not final production geometry",
        polys=[
            rounded_rect_poly(0, 0, 165, 40, 4, "TEMPLATE"),
            rounded_rect_poly(12, 14.5, 16, 11, 5.5, "TEMPLATE"),
            rounded_rect_poly(137, 14.5, 16, 11, 5.5, "TEMPLATE"),
        ],
        circles=[],
        lines=[
            Line(0, 20, 165, 20, "CENTER"),
            Line(20, 0, 20, 40, "CENTER"),
            Line(145, 0, 145, 40, "CENTER"),
        ],
        notes=[
            "This is a stock and quote blank using 165 mm trace length and 38-42 mm working width.",
            "Final strip outline and hole centres must be traced from the physical rubber and metal carrier before cutting.",
            "Punch M10 clearance holes or 11 x 16 slots only where the carrier confirms them. Do not copy torn rubber holes.",
            "If bonded to metal, blast/degrease/prime the carrier and clamp flat through cure.",
        ],
    )


def drawings() -> list[Drawing]:
    return [
        circular_mount(
            "bm_sm_body_mount_cushion_rev_a",
            "BM-SM small circular body-mount cushion",
            64,
            "22 mm stack-equivalent; split-stack hold remains open",
            "10",
            "prototype/quote; production waits for one-piece vs split-stack decision",
        ),
        circular_mount(
            "bm_lg_body_mount_cushion_rev_a",
            "BM-LG large circular body-mount cushion",
            78,
            "24 mm",
            "2",
            "prototype/quote; caliper-confirm station and final stack before batch",
        ),
        cup_washer("bm_cup_small_seat_washer_rev_a", "BM-CUP small body-mount cup washer", 64, "10 working basis"),
        cup_washer("bm_cup_large_seat_washer_rev_a", "BM-CUP large body-mount cup washer", 78, "2 working basis"),
        fs_oval(),
        strip_template("fs_strip_left_template_blank_rev_a", "FS-STRIP-L front support strip quote/template blank"),
        strip_template("fs_strip_right_template_blank_rev_a", "FS-STRIP-R front support strip quote/template blank"),
    ]


def write_cut_list(drawings: Sequence[Drawing]) -> None:
    header = [
        "part_id",
        "drawing_file_base",
        "qty",
        "material",
        "source_spec",
        "dxf_file",
        "svg_file",
        "release_status",
        "shop_instruction",
    ]
    rows = [
        [
            drawing.name.split("_rev_a")[0].upper().replace("_", "-"),
            drawing.name,
            drawing.qty,
            drawing.material,
            "docs/rubber-recreation-fabrication-spec-20260502.md",
            f"{drawing.name}.dxf",
            f"{drawing.name}.svg",
            drawing.release_status,
            "Use DXF layers exactly: through cuts only on CUT/CUT_BORE/DRILL; marks/forms on RECESS/FORM/INSERT_MARK/TEMPLATE.",
        ]
        for drawing in drawings
    ]
    text = [",".join(header)]
    for row in rows:
        text.append(",".join(csv_escape(cell) for cell in row))
    (OUT_DIR / "fabricator_cut_list.csv").write_text("\n".join(text) + "\n", encoding="utf-8")


def write_inspection_sheet() -> None:
    rows = [
        ("BM-SM", "OD, height, bore, register OD/depth, hardness", "OD/ID +/-1.0; height +/-0.5; Shore A 55-65"),
        ("BM-LG", "OD, height, bore, register OD/depth, hardness", "OD/ID +/-1.0; height +/-0.5; Shore A 55-65"),
        ("BM-CUP-SM", "OD, 11 mm hole, dish/register depth, steel thickness", "OD +/-1.0; hole +0.3/-0.0; dish 2-3"),
        ("BM-CUP-LG", "OD, 11 mm hole, dish/register depth, steel thickness", "OD +/-1.0; hole +0.3/-0.0; dish 2-3"),
        ("FS-OVAL", "overall length/width, thickness, hole spacing, insert OD, hardness", "outer +/-1.0; holes +/-0.5; thickness +/-0.5"),
        ("FS-STRIP-L/R", "template match, thickness, hole/slot centres, bond quality", "physical template controls final cut"),
    ]
    header = "part_id,inspect_features,acceptance\n"
    body = "\n".join(",".join(csv_escape(value) for value in row) for row in rows)
    (OUT_DIR / "inspection_checklist.csv").write_text(header + body + "\n", encoding="utf-8")


def csv_escape(value: str) -> str:
    if any(ch in value for ch in ',\"\n'):
        return '"' + value.replace('"', '""') + '"'
    return value


def write_readme(drawings: Sequence[Drawing]) -> None:
    drawing_list = "\n".join(
        f"- `{drawing.name}.dxf` / `{drawing.name}.svg` - {drawing.title}, qty {drawing.qty}"
        for drawing in drawings
    )
    text = f"""# J40 Rubber Recreation Fabrication Pack - Rev A

This is the fabrication-output package for the body-mount and front-support rubber recreation workstream.

Use it with:

- `docs/rubber-recreation-fabrication-spec-20260502.md`
- `data/manual/rubber_recreation_fabrication_specs.csv`
- `data/manual/rubber_recreation_measurement_closure.csv`
- `data/manual/rubber_recreation_manufacturing_requirements.csv`

## Files To Send

- `{PDF_NAME}` - dimension and fabrication review sheet
- `fabricator_cut_list.csv` - file-by-file cut/form list
- `inspection_checklist.csv` - receiving and first-article inspection checks

## DXF / SVG Parts

{drawing_list}

## Layer Rules

- `CUT`, `CUT_BORE`, `CUT_RELIEF`, and `DRILL` are through-cut or through-hole geometry.
- `RECESS`, `FORM`, and `INSERT_MARK` are register, forming, boss, or pocket controls. Do not through-cut them unless the physical sample proves that construction.
- `TEMPLATE` is a trace/quote guide only. The strip rubbers still require physical template tracing before production cutting.
- `CENTER` is construction geometry only.

## Release Limits

The circular cushions, cup blanks, and oval pad are ready for quote and first article from these files. Full production still requires the hold dimensions in `data/manual/rubber_recreation_measurement_closure.csv`.

The strip files are not final production cut patterns. They define stock envelope, section, and hole/slot working basis, but the actual left/right strip outline and hole centres must be traced from the physical rubber and metal carrier.

## Material

Use new black automotive mount-grade solid rubber only: EPDM or NR/SBR, Shore A `60 +/-5`. Reject tyre rubber, crumb rubber, sponge foam, mixed offcuts, salvage rubber, and unmarked compound.

Steel cups must be `2.5-3.0 mm` steel, deburred and zinc plated or epoxy primed after forming. Sleeves are still controlled by stack dry-fit and are not released as a cut DXF.
"""
    (OUT_DIR / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    package_drawings = drawings()
    for drawing in package_drawings:
        write_dxf(drawing)
        write_svg(drawing)
    write_pdf(package_drawings)
    write_cut_list(package_drawings)
    write_inspection_sheet()
    write_readme(package_drawings)
    print(f"Wrote rubber fabrication pack: {OUT_DIR}")
    print(f"Drawings: {len(package_drawings)}")


if __name__ == "__main__":
    main()
