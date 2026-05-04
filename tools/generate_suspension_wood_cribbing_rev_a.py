#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm as pdf_mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "manual" / "fabrication" / "suspension_wood_cribbing_rev_a"
PDF_NAME = "j40_suspension_wood_cribbing_rev_a_dimension_sheet.pdf"


@dataclass(frozen=True)
class Line:
    x1: float
    y1: float
    x2: float
    y2: float
    layer: str = "CUT_PROFILE"


@dataclass(frozen=True)
class Poly:
    points: tuple[tuple[float, float], ...]
    layer: str = "CUT_PROFILE"


@dataclass(frozen=True)
class View:
    label: str
    origin_x: float
    origin_y: float
    lines: tuple[Line, ...]
    polys: tuple[Poly, ...] = ()


@dataclass(frozen=True)
class PartDrawing:
    name: str
    title: str
    qty: int
    material: str
    views: tuple[View, ...]
    notes: tuple[str, ...]


def fmt(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


def rect_lines(x: float, y: float, w: float, h: float, layer: str = "CUT_PROFILE") -> tuple[Line, ...]:
    return (
        Line(x, y, x + w, y, layer),
        Line(x + w, y, x + w, y + h, layer),
        Line(x + w, y + h, x, y + h, layer),
        Line(x, y + h, x, y, layer),
    )


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
            fmt(line.x1),
            "20",
            fmt(line.y1),
            "11",
            fmt(line.x2),
            "21",
            fmt(line.y2),
        ]
    )


def add_dxf_poly(lines: list[str], poly: Poly) -> None:
    points = list(poly.points)
    for idx, (x1, y1) in enumerate(points):
        x2, y2 = points[(idx + 1) % len(points)]
        add_dxf_line(lines, Line(x1, y1, x2, y2, poly.layer))


def write_dxf(drawing: PartDrawing) -> None:
    lines = dxf_header()
    for view in drawing.views:
        for poly in view.polys:
            moved = Poly(tuple((x + view.origin_x, y + view.origin_y) for x, y in poly.points), poly.layer)
            add_dxf_poly(lines, moved)
        for line in view.lines:
            add_dxf_line(
                lines,
                Line(
                    line.x1 + view.origin_x,
                    line.y1 + view.origin_y,
                    line.x2 + view.origin_x,
                    line.y2 + view.origin_y,
                    line.layer,
                ),
            )
    lines.extend(dxf_footer())
    (OUT_DIR / f"{drawing.name}.dxf").write_text("\n".join(lines) + "\n", encoding="ascii")


def svg_line(line: Line) -> str:
    cls = "profile" if line.layer == "CUT_PROFILE" else "reference"
    return (
        f'<line class="{cls}" x1="{fmt(line.x1)}" y1="{fmt(line.y1)}" '
        f'x2="{fmt(line.x2)}" y2="{fmt(line.y2)}" />'
    )


def svg_poly(poly: Poly) -> str:
    cls = "profile" if poly.layer == "CUT_PROFILE" else "reference"
    points = " ".join(f"{fmt(x)},{fmt(y)}" for x, y in poly.points)
    return f'<polygon class="{cls}" points="{points}" />'


def svg_text(x: float, y: float, text: str, cls: str = "note") -> str:
    escaped = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
    return f'<text x="{fmt(x)}" y="{fmt(y)}" class="{cls}">{escaped}</text>'


def write_svg(drawing: PartDrawing) -> None:
    max_x = 0.0
    max_y = 0.0
    for view in drawing.views:
        for poly in view.polys:
            for x, y in poly.points:
                max_x = max(max_x, view.origin_x + x)
                max_y = max(max_y, view.origin_y + y)
        for line in view.lines:
            max_x = max(max_x, view.origin_x + line.x1, view.origin_x + line.x2)
            max_y = max(max_y, view.origin_y + line.y1, view.origin_y + line.y2)
    note_y = max_y + 22
    width = max(390, int(max_x + 22))
    height = int(note_y + min(len(drawing.notes), 5) * 10 + 18)
    elems: list[str] = [
        svg_text(12, 16, f"{drawing.title} | qty {drawing.qty} | units: mm", "title")
    ]
    for view in drawing.views:
        elems.append(svg_text(view.origin_x, view.origin_y - 5, view.label, "label"))
        for poly in view.polys:
            moved = Poly(tuple((x + view.origin_x, y + view.origin_y) for x, y in poly.points), poly.layer)
            elems.append(svg_poly(moved))
        for line in view.lines:
            elems.append(
                svg_line(
                    Line(
                        line.x1 + view.origin_x,
                        line.y1 + view.origin_y,
                        line.x2 + view.origin_x,
                        line.y2 + view.origin_y,
                        line.layer,
                    )
                )
            )
    elems.extend(svg_text(12, note_y + idx * 10, note) for idx, note in enumerate(drawing.notes[:5]))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}mm" height="{height}mm" viewBox="0 0 {width} {height}">
  <style>
    .profile {{ fill: none; stroke: #111111; stroke-width: 0.7; }}
    .reference {{ fill: none; stroke: #666666; stroke-width: 0.4; stroke-dasharray: 4 3; }}
    .title {{ font: 700 8px monospace; fill: #111111; }}
    .label {{ font: 700 6px monospace; fill: #333333; }}
    .note {{ font: 5.6px monospace; fill: #111111; }}
  </style>
  {"".join(elems)}
</svg>
"""
    (OUT_DIR / f"{drawing.name}.svg").write_text(svg, encoding="utf-8")


def page_title(c: canvas.Canvas, title: str, part_id: str) -> None:
    page_w, page_h = landscape(A4)
    margin = 14 * pdf_mm
    c.setFont("Helvetica-Bold", 15)
    c.drawString(margin, page_h - margin, title)
    c.setFont("Helvetica", 9)
    c.drawRightString(page_w - margin, page_h - margin, f"{part_id} | Rev A | Units: mm")


def draw_dim_h(c: canvas.Canvas, x1: float, x2: float, y: float, text: str) -> None:
    tick = 2.5 * pdf_mm
    c.setStrokeColor(HexColor("#444444"))
    c.setLineWidth(0.5)
    c.line(x1, y, x2, y)
    c.line(x1, y - tick, x1, y + tick)
    c.line(x2, y - tick, x2, y + tick)
    c.setFont("Helvetica", 8)
    c.drawCentredString((x1 + x2) / 2, y + 3.2 * pdf_mm, text)


def draw_dim_v(c: canvas.Canvas, x: float, y1: float, y2: float, text: str) -> None:
    tick = 2.5 * pdf_mm
    c.setStrokeColor(HexColor("#444444"))
    c.setLineWidth(0.5)
    c.line(x, y1, x, y2)
    c.line(x - tick, y1, x + tick, y1)
    c.line(x - tick, y2, x + tick, y2)
    c.saveState()
    c.translate(x - 4.5 * pdf_mm, (y1 + y2) / 2)
    c.rotate(90)
    c.setFont("Helvetica", 8)
    c.drawCentredString(0, 0, text)
    c.restoreState()


def draw_notes(c: canvas.Canvas, x: float, y: float, notes: Iterable[str], width: float) -> None:
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y, "Shop notes")
    c.setFont("Helvetica", 8.5)
    row = 0
    for note in notes:
        for line in simpleSplit(f"- {note}", "Helvetica", 8.5, width):
            c.drawString(x, y - (row + 1) * 4.8 * pdf_mm, line)
            row += 1
        row += 0.25


def draw_rect(c: canvas.Canvas, x: float, y: float, w: float, h: float) -> None:
    c.rect(x, y, w, h, stroke=1, fill=0)


def draw_poly(c: canvas.Canvas, points: tuple[tuple[float, float], ...], ox: float, oy: float, scale: float) -> None:
    path = c.beginPath()
    x0, y0 = points[0]
    path.moveTo(ox + x0 * scale, oy + y0 * scale)
    for x, y in points[1:]:
        path.lineTo(ox + x * scale, oy + y * scale)
    path.close()
    c.drawPath(path, stroke=1, fill=0)


def draw_rectangular_pdf_page(c: canvas.Canvas) -> None:
    page_w, page_h = landscape(A4)
    margin = 14 * pdf_mm
    page_title(c, "Rectangular Hardwood Cribbing Block", "SWC-BLOCK-001")
    c.setFont("Helvetica", 9)
    c.drawString(margin, page_h - 23 * pdf_mm, "Quantity: 8 pieces. Finished size: 300 L x 150 W x 75 H.")

    sx, sy = 22 * pdf_mm, 128 * pdf_mm
    scale = 0.36 * pdf_mm
    side_w = 300 * scale
    side_h = 75 * scale
    draw_rect(c, sx, sy, side_w, side_h)
    draw_dim_h(c, sx, sx + side_w, sy - 9 * pdf_mm, "300 length")
    draw_dim_v(c, sx - 8 * pdf_mm, sy, sy + side_h, "75 height")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(sx, sy + side_h + 4 * pdf_mm, "Side view")

    tx, ty = sx, 48 * pdf_mm
    top_h = 150 * scale
    draw_rect(c, tx, ty, side_w, top_h)
    draw_dim_h(c, tx, tx + side_w, ty - 9 * pdf_mm, "300 length")
    draw_dim_v(c, tx - 8 * pdf_mm, ty, ty + top_h, "150 width")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(tx, ty + top_h + 4 * pdf_mm, "Top view")

    ex, ey = 150 * pdf_mm, 92 * pdf_mm
    end_w = 150 * scale
    end_h = 75 * scale
    draw_rect(c, ex, ey, end_w, end_h)
    draw_dim_h(c, ex, ex + end_w, ey - 9 * pdf_mm, "150 width")
    draw_dim_v(c, ex - 8 * pdf_mm, ey, ey + end_h, "75 height")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(ex, ey + end_h + 4 * pdf_mm, "End view")

    notes = (
        "Control dimensions are metric. A 12 x 6 x 3 inch merchant cut is acceptable only if the finished piece is not smaller than tolerance.",
        "Tolerance: length +/-5 mm, width +/-3 mm, height +/-3 mm.",
        "Grain must run along the 300 mm length.",
        "Faces must be flat, parallel, and stable on a flat floor with no rocking.",
        "Light 3-5 mm edge chamfer is allowed; keep broad bearing faces flat.",
    )
    draw_notes(c, 214 * pdf_mm, 155 * pdf_mm, notes, page_w - 228 * pdf_mm)
    c.setFont("Helvetica", 8)
    c.drawRightString(page_w - margin, 9 * pdf_mm, f"Output: {PDF_NAME}")
    c.showPage()


def draw_wedge_pdf_page(c: canvas.Canvas) -> None:
    page_w, page_h = landscape(A4)
    margin = 14 * pdf_mm
    page_title(c, "Hardwood Wedge Chock", "SWC-CHOCK-001")
    c.setFont("Helvetica", 9)
    c.drawString(
        margin,
        page_h - 23 * pdf_mm,
        "Quantity: 4 pieces. Finished size: 200 L x 100 W, 75 rear height, 25 nose height.",
    )

    scale = 0.55 * pdf_mm
    sx, sy = 22 * pdf_mm, 126 * pdf_mm
    wedge = ((0, 0), (200, 0), (200, 75), (0, 25))
    draw_poly(c, wedge, sx, sy, scale)
    draw_dim_h(c, sx, sx + 200 * scale, sy - 9 * pdf_mm, "200 base length")
    draw_dim_v(c, sx + 200 * scale + 9 * pdf_mm, sy, sy + 75 * scale, "75 rear")
    draw_dim_v(c, sx - 8 * pdf_mm, sy, sy + 25 * scale, "25 nose")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(sx, sy + 75 * scale + 4 * pdf_mm, "Side profile")
    c.setFont("Helvetica", 8)
    c.drawString(sx + 42 * pdf_mm, sy + 24 * pdf_mm, "straight taper, approx 14 degrees")

    tx, ty = sx, 44 * pdf_mm
    draw_rect(c, tx, ty, 200 * scale, 100 * scale)
    draw_dim_h(c, tx, tx + 200 * scale, ty - 9 * pdf_mm, "200 length")
    draw_dim_v(c, tx - 8 * pdf_mm, ty, ty + 100 * scale, "100 width")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(tx, ty + 100 * scale + 4 * pdf_mm, "Top view")

    rx, ry = 150 * pdf_mm, 100 * pdf_mm
    draw_rect(c, rx, ry, 100 * scale, 75 * scale)
    draw_dim_h(c, rx, rx + 100 * scale, ry - 9 * pdf_mm, "100 width")
    draw_dim_v(c, rx - 8 * pdf_mm, ry, ry + 75 * scale, "75 rear")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(rx, ry + 75 * scale + 4 * pdf_mm, "Rear end")

    nx, ny = 150 * pdf_mm, 48 * pdf_mm
    draw_rect(c, nx, ny, 100 * scale, 25 * scale)
    draw_dim_h(c, nx, nx + 100 * scale, ny - 9 * pdf_mm, "100 width")
    draw_dim_v(c, nx - 8 * pdf_mm, ny, ny + 25 * scale, "25 nose")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(nx, ny + 25 * scale + 4 * pdf_mm, "Nose end")

    notes = (
        "Control dimensions are metric. This is a blunt-nose wedge, not a feather-edge wedge.",
        "Tolerance: length +/-5 mm, width +/-3 mm, rear height +/-3 mm, nose height +/-3 mm.",
        "Cut from a 200 x 100 x 75 mm solid hardwood blank, or from an 8 x 4 x 3 inch blank if using inch stock.",
        "Flat bottom must sit stable across the full 100 mm width.",
        "If the timber merchant cannot cut the taper cleanly, buy four extra 200 x 100 x 75 mm blanks and let the workshop cut them.",
    )
    draw_notes(c, 214 * pdf_mm, 160 * pdf_mm, notes, page_w - 228 * pdf_mm)
    c.setFont("Helvetica", 8)
    c.drawRightString(page_w - margin, 9 * pdf_mm, f"Output: {PDF_NAME}")
    c.showPage()


def write_pdf() -> None:
    c = canvas.Canvas(str(OUT_DIR / PDF_NAME), pagesize=landscape(A4))
    draw_rectangular_pdf_page(c)
    draw_wedge_pdf_page(c)
    c.save()


def rectangular_drawing() -> PartDrawing:
    return PartDrawing(
        name="swc_rectangular_cribbing_block_rev_a",
        title="SWC-BLOCK-001 rectangular hardwood cribbing block",
        qty=8,
        material="Seasoned solid hardwood",
        views=(
            View("side: 300 x 75", 18, 40, rect_lines(0, 0, 300, 75)),
            View("top: 300 x 150", 18, 130, rect_lines(0, 0, 300, 150)),
            View("end: 150 x 75", 330, 40, rect_lines(0, 0, 150, 75)),
        ),
        notes=(
            "Finished size: 300 L x 150 W x 75 H mm.",
            "Qty 8. Tolerance: length +/-5, width +/-3, height +/-3 mm.",
            "Grain runs along 300 mm length. Faces flat and parallel.",
            "Raw unfinished hardwood. Light 3-5 mm edge chamfer allowed.",
            "Use with rated stands only; not a stand substitute.",
        ),
    )


def wedge_drawing() -> PartDrawing:
    wedge_poly = Poly(((0, 0), (200, 0), (200, 75), (0, 25)))
    return PartDrawing(
        name="swc_wedge_chock_rev_a",
        title="SWC-CHOCK-001 hardwood wedge chock",
        qty=4,
        material="Seasoned solid hardwood",
        views=(
            View("side profile: 200 base, 75 rear, 25 nose", 18, 55, (), (wedge_poly,)),
            View("top: 200 x 100", 18, 145, rect_lines(0, 0, 200, 100)),
            View("rear end: 100 x 75", 245, 55, rect_lines(0, 0, 100, 75)),
            View("nose end: 100 x 25", 245, 145, rect_lines(0, 0, 100, 25)),
        ),
        notes=(
            "Finished size: 200 L x 100 W, 75 rear height, 25 nose height.",
            "Qty 4. Tolerance: length +/-5, width +/-3, heights +/-3 mm.",
            "Straight top taper, approx 14 degrees. No feather edge.",
            "Flat bottom across full width; grain runs along 200 mm length.",
            "Use as chocks/stabilizers only; not primary support.",
        ),
    )


def write_cut_list() -> None:
    text = """part_id,item,qty,finished_size_mm,shop_equivalent,material,tolerance,grain,edge_finish,acceptance_check,release_status
SWC-BLOCK-001,Rectangular hardwood cribbing block,8,300 L x 150 W x 75 H,12 x 6 x 3 in nominal if not undersize,"Seasoned solid hardwood: sheesham/shisham, kikar/acacia, oak, ash, or equivalent dense hardwood","Length +/-5 mm; width +/-3 mm; height +/-3 mm",Grain along 300 mm length,"Raw unfinished; optional 3-5 mm edge chamfer; keep bearing faces flat","Sits flat without rocking; no split ends; no deep knots on bearing faces; no bow/twist",purchase_and_fabrication_ready
SWC-CHOCK-001,Hardwood wedge chock,4,200 L x 100 W x 75 rear H x 25 nose H,8 x 4 x 3 in blank tapered to 1 in nose,"Same seasoned solid hardwood batch as SWC-BLOCK-001","Length +/-5 mm; width +/-3 mm; rear/nose height +/-3 mm",Grain along 200 mm length,"Raw unfinished; no feather-thin nose; keep bottom flat","Flat bottom across full 100 mm width; straight taper; no split grain through taper",purchase_and_fabrication_ready
SWC-CHOCK-BLANK-ALT,Alternate wedge blank if merchant cannot taper,4,200 L x 100 W x 75 H,8 x 4 x 3 in nominal if not undersize,"Same seasoned solid hardwood batch as SWC-BLOCK-001","Length +/-5 mm; width +/-3 mm; height +/-3 mm",Grain along 200 mm length,Raw unfinished,"Buy only instead of finished wedges; workshop cuts taper to SWC-CHOCK-001",fallback_only
"""
    (OUT_DIR / "fabricator_cut_list.csv").write_text(text, encoding="utf-8")


def write_inspection_checklist() -> None:
    text = """check_id,applies_to,inspection,pass_condition,reject_condition
SWC-INSP-001,all,Material check,"Seasoned dense solid hardwood; dry and heavy for size","Wet/green wood, softwood, plywood, MDF, chipboard, laminated/glued board, oily or painted offcut"
SWC-INSP-002,SWC-BLOCK-001,Rectangular block dimensions,"300 x 150 x 75 mm within tolerance","Undersize beyond tolerance, bowed faces, twisted block, non-square ends"
SWC-INSP-003,SWC-CHOCK-001,Wedge dimensions,"200 x 100 mm base, 75 mm rear, 25 mm nose within tolerance","Feather-edge nose, uneven taper, split grain, unstable bottom"
SWC-INSP-004,all,Stability on flat floor,"Each piece sits flat without rocking","Rocks, has rounded bearing face, wane, or unstable cut"
SWC-INSP-005,all,Defect check,"No cracks through thickness; no large knots on bearing faces; no insect damage","Split ends, loose knots, large deep knots, visible rot or insect tunneling"
SWC-INSP-006,all,Use control,"Marked as supplemental cribbing/chocks only","Supplier or workshop treats blocks as a substitute for rated jack stands"
"""
    (OUT_DIR / "inspection_checklist.csv").write_text(text, encoding="utf-8")


def write_readme() -> None:
    text = """# J40 Suspension Wood Cribbing Pack - Rev A

This is the controlled cut package for the hardwood support blocks and wedge chocks needed before the Ironman suspension and brake work window.

## Send To Scout / Timber Merchant

- `j40_suspension_wood_cribbing_rev_a_dimension_sheet.pdf`
- `fabricator_cut_list.csv`
- `inspection_checklist.csv`

Plain request:

> I need 8 seasoned solid hardwood blocks, finished 300 x 150 x 75 mm, plus 4 solid hardwood wedge chocks, finished 200 x 100 mm base with 75 mm rear height and 25 mm nose height. Use dry dense hardwood such as sheesham/shisham, kikar/acacia, oak, ash, or equivalent. Raw unfinished wood, flat faces, no plywood/MDF/softwood/wet/cracked/painted pieces.

## Send To Fabricator / Workshop

- Use the same PDF as the control drawing.
- Use `swc_wedge_chock_rev_a.dxf` if the workshop will cut the wedge taper from rectangular blanks.
- Use the SVG files as quick visual references.

## Parts

| ID | Qty | Finished size |
| --- | ---: | --- |
| SWC-BLOCK-001 | 8 | 300 L x 150 W x 75 H mm |
| SWC-CHOCK-001 | 4 | 200 L x 100 W base, 75 mm rear height, 25 mm nose height |

If the timber merchant cannot cut the wedge taper cleanly, buy 4 extra 200 x 100 x 75 mm hardwood blanks and have the workshop cut them to `SWC-CHOCK-001`.

## Safety Position

These blocks are supplemental cribbing and chocks for a controlled suspension/brake work setup. They are not a substitute for rated jack stands, a rated trolley jack, or proper axle support.
"""
    (OUT_DIR / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    drawings = (rectangular_drawing(), wedge_drawing())
    for drawing in drawings:
        write_dxf(drawing)
        write_svg(drawing)
    write_pdf()
    write_cut_list()
    write_inspection_checklist()
    write_readme()


if __name__ == "__main__":
    main()
