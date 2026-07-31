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
OUT = ROOT / "data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_b"
DELIVERABLE = ROOT / "deliverables/fabrication_packages/dashboard_lcd_hvac_fascia_rev_b.zip"
CONCEPT_SOURCE = Path("/Users/davidpridmore/.codex/generated_images/019fb8d3-8269-7eb0-b457-d806a3cefbd4/exec-ced4d074-4f67-440b-9568-fec42a220cf1.png")

# Quote/prototype envelope only. The vehicle template and actual bought parts
# control production geometry; see HOLD layers and release schedule.
FASCIA_W = 275.0
FASCIA_H = 220.0
CORNER_R = 6.0
SCREEN_X, SCREEN_Y, SCREEN_W, SCREEN_H = 22.5, 72.0, 230.0, 132.0
STRIP_X, STRIP_Y, STRIP_W, STRIP_H = 22.5, 20.0, 230.0, 34.0


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
    fascia.append(dxf_lwpoly("HOLD_LCD_APERTURE", rounded_rect_points(SCREEN_X, SCREEN_Y, SCREEN_W, SCREEN_H, 3)))
    fascia.append(dxf_lwpoly("CUT_CONTROL_STRIP_APERTURE", rounded_rect_points(STRIP_X, STRIP_Y, STRIP_W, STRIP_H, 3)))
    for x, y in ((8, 8), (137.5, 8), (267, 8), (8, 212), (137.5, 212), (267, 212)):
        fascia.append(dxf_circle("HOLD_VEHICLE_TEMPLATE", x, y, 2.25))
    write_dxf(OUT / "centre_fascia_template_rev_b.dxf", fascia)

    strip = [dxf_lwpoly("CUT", rounded_rect_points(0, 0, STRIP_W, STRIP_H, 3))]
    for x in (40, 90, 140, 190):
        strip.append(dxf_circle("HOLD_SWITCH_APERTURES", x, STRIP_H / 2, 8.1))
    for x in (6, STRIP_W - 6):
        strip.append(dxf_circle("CUT", x, STRIP_H / 2, 2.25))
    write_dxf(OUT / "removable_control_strip_blank_rev_b.dxf", strip)

    clamp = [dxf_lwpoly("CUT", rounded_rect_points(0, 0, 250, 150, 3)), dxf_lwpoly("HOLD_LCD_REAR_BODY", rounded_rect_points(10, 10, 230, 130, 2))]
    for x, y in ((5, 5), (245, 5), (5, 145), (245, 145)):
        clamp.append(dxf_circle("CUT", x, y, 2.25))
    write_dxf(OUT / "lcd_rear_clamp_blank_rev_b.dxf", clamp)

    vent = [dxf_lwpoly("CUT", rounded_rect_points(0, 0, 82, 82, 5)), dxf_circle("HOLD_VENT_APERTURE", 41, 41, 31.75)]
    for x, y in ((8, 8), (74, 8)):
        vent.append(dxf_circle("CUT", x, y, 2.25))
    write_dxf(OUT / "underdash_eyeball_vent_bracket_blank_rev_b.dxf", vent)


def write_svg() -> None:
    s, x0, y0 = 2.15, 85, 130
    sx = lambda x: x0 + x * s
    sy = lambda y: y0 + (FASCIA_H - y) * s
    holes = "".join(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="5" class="hold"/>' for x, y in ((8,8),(137.5,8),(267,8),(8,212),(137.5,212),(267,212)))
    switches = "".join(f'<circle cx="{sx(x)}" cy="{sy(STRIP_Y+17)}" r="12" fill="#b8bec2" stroke="#161b1f" stroke-width="2"/>' for x in (62.5,112.5,162.5,212.5))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="760" viewBox="0 0 1180 760">
<style>.cut{{fill:none;stroke:#111;stroke-width:2}}.hold{{fill:#fff4df;stroke:#a85f00;stroke-width:2;stroke-dasharray:7 5}}.txt{{font:15px Arial;fill:#20262b}}.bold{{font:700 18px Arial;fill:#20262b}}.small{{font:13px Arial;fill:#53606a}}.dim{{stroke:#aa2020;stroke-width:1.5}}</style>
<rect width="1180" height="760" fill="#f7f8f9"/><text x="55" y="44" class="bold">J40 RHD CENTRE LCD FASCIA - REV B</text><text x="55" y="70" class="small">Original glovebox and speedometer/instrument pressing are excluded from the cut scope. All orange geometry is HOLD.</text>
<rect x="{sx(0)}" y="{sy(FASCIA_H)}" width="{FASCIA_W*s}" height="{FASCIA_H*s}" rx="{CORNER_R*s}" fill="#e8e2cc" stroke="#a85f00" stroke-width="2" stroke-dasharray="7 5"/>
<rect x="{sx(SCREEN_X)}" y="{sy(SCREEN_Y+SCREEN_H)}" width="{SCREEN_W*s}" height="{SCREEN_H*s}" rx="6" fill="#191d20" stroke="#a85f00" stroke-width="2" stroke-dasharray="7 5"/>
<rect x="{sx(STRIP_X)}" y="{sy(STRIP_Y+STRIP_H)}" width="{STRIP_W*s}" height="{STRIP_H*s}" rx="6" fill="#e8e2cc" stroke="#111" stroke-width="2"/>{switches}{holes}
<line x1="{sx(0)}" y1="{sy(0)+38}" x2="{sx(FASCIA_W)}" y2="{sy(0)+38}" class="dim"/><text x="{sx(112)}" y="{sy(0)+62}" class="bold">275 nominal</text>
<line x1="{sx(FASCIA_W)+35}" y1="{sy(FASCIA_H)}" x2="{sx(FASCIA_W)+35}" y2="{sy(0)}" class="dim"/><text x="{sx(FASCIA_W)+48}" y="{sy(105)}" class="bold">220 nominal</text>
<text x="{sx(64)}" y="{sy(137)}" fill="#fff" font-family="Arial" font-size="18">9-inch LCD - actual aperture HOLD</text>
<rect x="750" y="122" width="370" height="490" rx="8" fill="#fff" stroke="#cbd2d7"/><text x="775" y="157" class="bold">SCOPE LOCK</text>
<text x="775" y="193" class="txt">Vehicle: right-hand drive</text><text x="775" y="223" class="txt">Glovebox: preserve unchanged</text><text x="775" y="253" class="txt">Speedometer pressing: preserve unchanged</text><text x="775" y="283" class="txt">Right-side switch holes: preserve/reuse</text><text x="775" y="313" class="txt">Ashtray: remove</text><text x="775" y="343" class="txt">New metal: centre radio/ashtray zone only</text>
<text x="775" y="389" class="bold">SEPARATE UNDER-DASH HVAC</text><text x="775" y="421" class="txt">2 x directional eyeball outlets</text><text x="775" y="451" class="txt">2.5-inch hose neck preferred</text><text x="775" y="481" class="txt">No face cuts near glovebox or gauges</text>
<text x="775" y="527" class="bold">PRODUCTION HOLD</text><text x="775" y="559" class="small">Template actual centre pressing and measure</text><text x="775" y="580" class="small">LCD, switches, vent flange and rear depth.</text><text x="775" y="601" class="small">Owner approves 1:1 paper/card prototype.</text>
<text x="55" y="710" class="small">Finish intent: body-colour cream, low gloss. DXF layers named HOLD are not production cut paths.</text></svg>'''
    (OUT / "dashboard_lcd_hvac_fascia_rev_b_dimensioned_front.svg").write_text(svg, encoding="utf-8")


def write_pdf() -> None:
    path = OUT / "j40_dashboard_lcd_hvac_fascia_rev_b_shop_spec.pdf"
    c = canvas.Canvas(str(path), pagesize=landscape(A3))
    w, h = landscape(A3)
    c.setTitle("J40 RHD Centre LCD Fascia Rev B")
    c.setFont("Helvetica-Bold", 18); c.drawString(16*mm, h-16*mm, "J40 RHD Centre LCD / HVAC Fascia - Rev B")
    c.setFont("Helvetica", 9); c.drawRightString(w-16*mm, h-16*mm, "Units mm | Quote + template release | Vehicle cutting HOLD")
    x, y = 18*mm, 31*mm
    c.setFillColor(HexColor("#e8e2cc")); c.setStrokeColor(HexColor("#a85f00")); c.setDash(5, 4)
    c.roundRect(x, y, FASCIA_W*mm, FASCIA_H*mm, CORNER_R*mm, fill=1, stroke=1)
    c.setFillColor(HexColor("#191d20")); c.roundRect(x+SCREEN_X*mm, y+SCREEN_Y*mm, SCREEN_W*mm, SCREEN_H*mm, 3*mm, fill=1, stroke=1)
    c.setDash(); c.setFillColor(HexColor("#e8e2cc")); c.setStrokeColor(HexColor("#111111")); c.roundRect(x+STRIP_X*mm, y+STRIP_Y*mm, STRIP_W*mm, STRIP_H*mm, 3*mm, fill=1, stroke=1)
    for hx in (62.5, 112.5, 162.5, 212.5):
        c.setFillColor(HexColor("#b8bec2")); c.circle(x+hx*mm, y+(STRIP_Y+17)*mm, 6*mm, fill=1, stroke=1)
    nx = 306*mm; yy = h-35*mm
    c.setFillColor(HexColor("#20262b")); c.setFont("Helvetica-Bold", 12); c.drawString(nx, yy, "CONTROLLED SCOPE")
    rows = [
        "Right-hand-drive vehicle: instrument/speedometer pressing stays original.",
        "Left glovebox, instruction plate and small compartment stay original.",
        "Remove ashtray; modify only existing centre radio/ashtray footprint.",
        "Nominal fascia envelope 275 x 220 x 1.5 CR4 steel - template controlled.",
        "Nominal LCD opening 230 x 132 - actual screen controls final aperture.",
        "Removable 230 x 34 switch strip; four bought switch apertures measured.",
        "Two eyeball vents mount separately under dash; no new main-face vent cuts.",
        "Preferred vent connection: 63.5 / 2.5-inch hose after neck trial fit.",
    ]
    c.setFont("Helvetica", 8.7)
    for row in rows:
        yy -= 9*mm; c.drawString(nx, yy, row)
    yy -= 7*mm; c.setFont("Helvetica-Bold", 11); c.setFillColor(HexColor("#8b1e1e")); c.drawString(nx, yy, "HOLD BEFORE METAL OR VEHICLE CUT")
    c.setFillColor(HexColor("#20262b")); c.setFont("Helvetica", 8.7)
    for row in ["M1 actual centre-zone contour and usable lands", "M2 LCD visible aperture, rear body, mount pattern, plugs", "M3 switch bush diameter, anti-rotation and rear body depth", "M4 vent face, aperture, neck OD, rear depth and hose bend", "M5 full rear interference sweep and 1:1 owner-approved prototype"]:
        yy -= 8*mm; c.drawString(nx, yy, row)
    c.setFont("Helvetica-Bold", 9); c.drawString(18*mm, 14*mm, "Orange/dashed geometry and all HOLD_* DXF layers are reference only. Do not cut them until the release schedule is signed.")
    c.showPage()

    c.setFont("Helvetica-Bold", 18); c.drawString(16*mm, h-16*mm, "Design intent on owner's actual RHD dashboard")
    c.setFont("Helvetica", 9); c.drawRightString(w-16*mm, h-16*mm, "Concept overlay - do not scale")
    img_path = OUT / "dashboard_lcd_hvac_fascia_rev_b_photo_overlay.png"
    if img_path.exists():
        img = ImageReader(str(img_path)); iw, ih = img.getSize(); maxw, maxh = 275*mm, 220*mm
        scale = min(maxw/iw, maxh/ih); c.drawImage(img, 16*mm, 34*mm, iw*scale, ih*scale, preserveAspectRatio=True)
    tx, ty = 306*mm, h-42*mm
    c.setFont("Helvetica-Bold", 12); c.drawString(tx, ty, "WHAT CHANGES")
    c.setFont("Helvetica", 9)
    for row in ["1. Ashtray and centre radio openings become one body-colour CNC insert.", "2. Horizontal 9-inch LCD sits flush in the upper centre insert.", "3. Four bought industrial switches sit on a removable lower strip.", "4. Two small directional vents mount below the dash, outside the face cut."]:
        ty -= 11*mm; c.drawString(tx, ty, row)
    ty -= 8*mm; c.setFont("Helvetica-Bold", 12); c.drawString(tx, ty, "WHAT DOES NOT CHANGE")
    c.setFont("Helvetica", 9)
    for row in ["- Left glovebox and its instruction plate", "- Small original compartment beside glovebox", "- Right speedometer/instrument pressing and steering-column notch", "- Four original switch positions to the right of the instruments", "- Outer dash sheet metal and character lines"]:
        ty -= 10*mm; c.drawString(tx, ty, row)
    ty -= 8*mm; c.setFont("Helvetica-Bold", 11); c.setFillColor(HexColor("#8b1e1e")); c.drawString(tx, ty, "The photograph establishes intent, not dimensions.")
    c.setFillColor(HexColor("#20262b")); c.setFont("Helvetica", 8.5); ty -= 10*mm
    c.drawString(tx, ty, "Final geometry comes from the vehicle template and actual parts.")
    c.setFont("Helvetica", 8); c.drawString(16*mm, 14*mm, "Base: photos/20260413_040719.jpg. Overlay generated from that photograph; all unmodified areas are preservation references.")
    c.showPage(); c.save()


def write_csvs() -> None:
    with (OUT / "fabricator_cut_list.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["part", "qty", "material", "thickness_mm", "finish", "file", "release"])
        w.writerows([
            ["centre fascia template", 1, "CR4 mild steel", 1.5, "body-colour low-gloss paint", "centre_fascia_template_rev_b.dxf", "QUOTE/PROTOTYPE ONLY; outer and LCD geometry HOLD"],
            ["removable control strip blank", 1, "5052-H32 aluminium", 2.0, "body-colour low-gloss paint", "removable_control_strip_blank_rev_b.dxf", "outer/fasteners released; switch holes HOLD"],
            ["LCD rear clamp blank", 1, "5052-H32 aluminium", 2.0, "black", "lcd_rear_clamp_blank_rev_b.dxf", "outer/fasteners released; rear-body opening HOLD"],
            ["under-dash eyeball vent bracket blank", 2, "5052-H32 aluminium", 2.0, "satin black", "underdash_eyeball_vent_bracket_blank_rev_b.dxf", "outer/fasteners released; vent aperture HOLD"],
        ])
    with (OUT / "measurement_and_release_schedule.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["id", "measurement", "nominal_or_intent", "required_evidence", "status"])
        w.writerows([
            ["M1", "centre radio/ashtray replacement contour and flat mounting lands", "275 x 220 envelope only", "1:1 card template and front/rear ruler photos", "HOLD"],
            ["M2", "LCD visible aperture W x H", "230 x 132 reference", "actual LCD caliper dimensions/model drawing", "HOLD"],
            ["M3", "LCD rear body/mount centres/depth/connector sweep", "supplier-specific", "rear rubbing, depth gauge and plug trial", "HOLD"],
            ["M4", "industrial switch threaded bush/anti-rotation/rear depth", "16 mm class reference", "caliper each bought switch and data label", "HOLD"],
            ["M5", "eyeball vent face/cutout/flange/neck OD/rear depth", "63.5 mm hose-neck target", "actual vent and hose trial", "HOLD"],
            ["M6", "rear clearance to linkage/wiring/heater/structure", "no contact through full travel", "rear photos plus physical sweep", "HOLD"],
            ["M7", "glovebox, speedometer and steering clearances", "unchanged", "signed 1:1 dash overlay", "HOLD"],
        ])


def write_readme() -> None:
    text = """# J40 RHD Centre 9-inch LCD / HVAC Fascia - Rev B

Rev B supersedes the Rev A full-size replacement concept. It starts from the owner's actual dashboard photograph and preserves the original right-hand-drive instrument/speedometer pressing, steering-column notch, four switch holes to its right, left glovebox, instruction plate and small original compartment.

## Approved design intent

- Remove the ashtray and combine only the existing centre radio/ashtray openings behind one compact, nearly flush CNC fascia.
- Nominal quote envelope is `275 x 220 x 1.5 mm`; the actual vehicle template controls the outer contour. Do not extend the cut toward the glovebox or speedometer pressing.
- Fit the actual horizontal 9-inch LCD in the upper centre. The `230 x 132 mm` drawing aperture is reference-only until the LCD is measured.
- Put four of the bought compact industrial switches on a removable lower strip. Original functions can remain in/reuse the four factory holes to the right of the instrument panel; move only functions agreed during the labelled mock-up.
- Mount two compact directional eyeball A/C outlets on separate under-dash brackets, one on each side of the centre insert. Prefer `63.5 mm / 2.5 inch` hose necks after measuring the bought vents. This keeps vent apertures out of the original dash face.
- Paint the fascia body colour in low gloss; use a thin black LCD bezel and discreet black vent pods. The aim is an original dashboard with one restrained modern insert.

## Control allocation for the 1:1 mock-up

The four centre-strip positions are provisionally `blower`, `A/C enable`, `hazard`, and one moved auxiliary function. Final function/order is a label-and-reach trial, not a CNC assumption. Wipers, lights and safety-critical original controls should preferentially stay in the original right-side locations. Switches operate relays/controller inputs unless their protected load rating is explicitly engineered.

## CNC release rules

DXF layers named `HOLD_*` are not production toolpaths. They show nominal intent so the shop can quote and make a cheap template. Release them only after:

1. Tape/card-template the actual centre zone from both sides and record M1-M7.
2. Place the actual LCD, four switches and two vents on the 1:1 template.
3. Prove glovebox opening, instrument-panel rigidity, driver sight line, steering-column clearance, gear-lever clearance, wiring/connector sweep and duct bend radius.
4. Print the final DXF at 1:1, offer it to the vehicle, and obtain owner sign-off on every edge and centre.
5. Cut the vehicle undersize, trim progressively, radius/deburr every edge and epoxy-prime exposed steel before paint.

## HVAC rules

- Route evaporator/plenum air through two supported smooth-bore hoses to the under-dash outlets; no kinks or crushed bends.
- Keep ducts clear of the LCD heat sink/connectors, wiper linkage, steering column, heater controls, wiring and sharp edges.
- Provide strain relief at each vent and plenum neck. A hose must be service-removable without removing the glovebox or instrument panel.
- These are the two front face-level outlets. Preserve a separate windscreen demist path; do not allocate all conditioned air to face vents.

## Acceptance

- Glovebox and instrument/speedometer pressing are visually and structurally unchanged.
- No new hole or cut exists outside the original centre radio/ashtray zone, except reversible under-dash vent-bracket fixings approved on the template.
- LCD, switch strip and each vent can be removed independently from the cabin side.
- Screen remains readable from the right-hand driver's position without blocking the original speedometer.
- Full steering, gear-lever, wiper/heater linkage, wiring and hose sweeps have clearance and no chafe point.
- All circuits are fused/relayed correctly; vents aim and flow; finished assembly passes vibration/rattle and road tests.

## Files and release state

- `j40_dashboard_lcd_hvac_fascia_rev_b_shop_spec.pdf` - two-page CNC brief and actual-photo intent overlay.
- `dashboard_lcd_hvac_fascia_rev_b_dimensioned_front.svg` - nominal front layout.
- `dashboard_lcd_hvac_fascia_rev_b_photo_overlay.png` - image edit of the owner's actual RHD dashboard; never scale.
- Four DXFs - quote/template blanks with explicit CUT and HOLD layers.
- `fabricator_cut_list.csv` and `measurement_and_release_schedule.csv` - shop controls.

**Ready to send for quotation, vehicle templating and a cardboard/cheap-sheet prototype. Not released for production cutting of the vehicle, LCD aperture, switch apertures or vent apertures until M1-M7 are completed and signed.**
"""
    (OUT / "README.md").write_text(text, encoding="utf-8")


def package() -> None:
    DELIVERABLE.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DELIVERABLE, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.iterdir()):
            z.write(p, f"dashboard_lcd_hvac_fascia_rev_b/{p.name}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if CONCEPT_SOURCE.exists():
        shutil.copy2(CONCEPT_SOURCE, OUT / "dashboard_lcd_hvac_fascia_rev_b_photo_overlay.png")
    make_dxfs(); write_svg(); write_csvs(); write_readme(); write_pdf(); package()
    print(OUT); print(DELIVERABLE)


if __name__ == "__main__":
    main()
