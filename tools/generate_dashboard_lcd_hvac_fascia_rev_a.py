from __future__ import annotations

import csv
import shutil
import zipfile
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


ROOT = Path("/Users/davidpridmore/IdeaProjects/J40")
OUT = ROOT / "data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_a"
DELIVERABLE = ROOT / "deliverables/fabrication_packages/dashboard_lcd_hvac_fascia_rev_a.zip"

PANEL_W = 480.0
PANEL_H = 320.0
CORNER_R = 8.0
DASH_CUT_W = 440.0
DASH_CUT_H = 280.0


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


def rounded_rect_points(x: float, y: float, w: float, h: float, r: float, segments: int = 6) -> list[tuple[float, float]]:
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
    # Released main fascia geometry. Accessory openings accept removable carriers;
    # actual bought-part apertures are deliberately isolated from this part.
    entities = [dxf_lwpoly("CUT", rounded_rect_points(0, 0, PANEL_W, PANEL_H, CORNER_R))]
    entities.append(dxf_lwpoly("CUT", rounded_rect_points(95, 124, 290, 180, 4)))
    entities.append(dxf_lwpoly("CUT", rounded_rect_points(82, 49, 145, 62, 3)))
    entities.append(dxf_lwpoly("CUT", rounded_rect_points(253, 49, 145, 62, 3)))
    # Matching M4 carrier fasteners. Centres sit 5 mm clear of the carrier
    # apertures, leaving a serviceable removable screen/vent subassembly.
    for x, y in ((90, 119), (390, 119), (90, 309), (390, 309)):
        entities.append(dxf_circle("CUT", x, y, 2.25))
    for x, y in ((77, 44), (232, 44), (77, 116), (232, 116),
                 (248, 44), (403, 44), (248, 116), (403, 116)):
        entities.append(dxf_circle("CUT", x, y, 2.25))
    for x, y in ((18, 18), (240, 18), (462, 18), (18, 160), (462, 160), (18, 302), (240, 302), (462, 302)):
        entities.append(dxf_circle("CUT", x, y, 2.75))
    for x in (185, 295):
        entities.append(dxf_circle("CUT", x, 25, 11.25))
    entities.append(dxf_circle("CUT", 240, 25, 8.10))
    write_dxf(OUT / "dashboard_main_fascia_rev_a.dxf", entities)

    lcd = [dxf_lwpoly("CUT", rounded_rect_points(0, 0, 310, 200, 4))]
    for x, y in ((5, 5), (305, 5), (5, 195), (305, 195)):
        lcd.append(dxf_circle("CUT", x, y, 2.25))
    # Reference only: never cut this nominal 9-inch aperture until the actual screen is measured.
    lcd.append(dxf_lwpoly("HOLD_SCREEN_APERTURE", rounded_rect_points(38.5, 32.5, 233, 135, 2)))
    write_dxf(OUT / "lcd_carrier_blank_rev_a.dxf", lcd)

    vent = [dxf_lwpoly("CUT", rounded_rect_points(0, 0, 165, 82, 3))]
    for x, y in ((5, 5), (160, 5), (5, 77), (160, 77)):
        vent.append(dxf_circle("CUT", x, y, 2.25))
    vent.append(dxf_lwpoly("HOLD_VENT_APERTURE", rounded_rect_points(20, 16, 125, 50, 2)))
    write_dxf(OUT / "hvac_vent_carrier_blank_rev_a.dxf", vent)

    frame = [dxf_lwpoly("CUT", rounded_rect_points(0, 0, 460, 300, 6)), dxf_lwpoly("CUT", rounded_rect_points(20, 20, 420, 260, 3))]
    for x, y in ((10, 10), (230, 10), (450, 10), (10, 150), (450, 150), (10, 290), (230, 290), (450, 290)):
        frame.append(dxf_circle("CUT", x, y, 3.25))
    write_dxf(OUT / "dashboard_rear_stiffening_frame_rev_a.dxf", frame)


def write_svg() -> None:
    scale = 1.55
    x0, y0 = 115, 135
    def sx(x: float) -> float: return x0 + x * scale
    def sy(y: float) -> float: return y0 + (PANEL_H - y) * scale
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="760" viewBox="0 0 1120 760">
<style>.cut{{fill:none;stroke:#111;stroke-width:2}}.hold{{fill:#fff4df;stroke:#a85f00;stroke-width:2;stroke-dasharray:8 6}}.dim{{stroke:#ba1b1b;stroke-width:1.4;fill:none}}.txt{{font:15px Arial;fill:#20262b}}.bold{{font:700 17px Arial;fill:#20262b}}.small{{font:13px Arial;fill:#53606a}}.metal{{fill:#e7ebee;stroke:#111;stroke-width:2}}.black{{fill:#1c2226;stroke:#111;stroke-width:2}}</style>
<rect width="1120" height="760" fill="#f7f8f9"/><text x="55" y="45" class="bold">J40 DASHBOARD LCD / HVAC REPLACEMENT FASCIA — REV A</text><text x="55" y="71" class="small">Units mm · released main plate geometry · orange apertures require bought-part transfer before their carrier is cut</text>
<rect x="{sx(0)}" y="{sy(PANEL_H)}" width="{PANEL_W*scale}" height="{PANEL_H*scale}" rx="{CORNER_R*scale}" class="metal"/>
<rect x="{sx(95)}" y="{sy(304)}" width="{290*scale}" height="{180*scale}" rx="6" class="hold"/><text x="{sx(150)}" y="{sy(218)}" class="bold">REMOVABLE LCD CARRIER</text><text x="{sx(151)}" y="{sy(195)}" class="small">nominal screen aperture 233 × 135 — HOLD</text>
<rect x="{sx(82)}" y="{sy(111)}" width="{145*scale}" height="{62*scale}" rx="5" class="hold"/><rect x="{sx(253)}" y="{sy(111)}" width="{145*scale}" height="{62*scale}" rx="5" class="hold"/><text x="{sx(107)}" y="{sy(77)}" class="small">VENT CARRIER</text><text x="{sx(278)}" y="{sy(77)}" class="small">VENT CARRIER</text>
<circle cx="{sx(185)}" cy="{sy(25)}" r="{11.25*scale}" class="black"/><circle cx="{sx(240)}" cy="{sy(25)}" r="{8.1*scale}" fill="#b51d1d" stroke="#111" stroke-width="2"/><circle cx="{sx(295)}" cy="{sy(25)}" r="{11.25*scale}" class="black"/>
<text x="{sx(162)}" y="{sy(3)}" class="small">BLOWER</text><text x="{sx(222)}" y="{sy(3)}" class="small">HAZARD</text><text x="{sx(282)}" y="{sy(3)}" class="small">A/C</text>
''' + ''.join(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="4.2" fill="#fff" stroke="#111" stroke-width="2"/>' for x,y in ((18,18),(240,18),(462,18),(18,160),(462,160),(18,302),(240,302),(462,302))) + ''.join(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="3.5" fill="#fff" stroke="#365b78" stroke-width="1.7"/>' for x,y in ((90,119),(390,119),(90,309),(390,309),(77,44),(232,44),(77,116),(232,116),(248,44),(403,44),(248,116),(403,116))) + f'''
<line x1="{sx(0)}" y1="{sy(PANEL_H)+530}" x2="{sx(PANEL_W)}" y2="{sy(PANEL_H)+530}" class="dim"/><text x="{sx(214)}" y="{sy(PANEL_H)+553}" class="bold">480 overall</text>
<line x1="{sx(PANEL_W)+45}" y1="{sy(PANEL_H)}" x2="{sx(PANEL_W)+45}" y2="{sy(0)}" class="dim"/><text x="{sx(PANEL_W)+57}" y="{sy(162)}" class="bold">320 overall</text>
<rect x="820" y="130" width="255" height="405" rx="8" fill="#fff" stroke="#cbd2d7"/><text x="842" y="162" class="bold">CONTROLLED INTERFACES</text>
<text x="842" y="198" class="txt">Main fascia: 480 × 320 × 1.5</text><text x="842" y="225" class="txt">Dash rough cut: 440 × 280 nominal</text><text x="842" y="252" class="txt">Overlap: 20 all sides nominal</text><text x="842" y="279" class="txt">Rear frame: 460 × 300 × 2.0</text><text x="842" y="306" class="txt">8 × M5 fascia fasteners</text><text x="842" y="333" class="txt">12 × Ø4.5 M4 carrier fasteners</text><text x="842" y="360" class="txt">LCD carrier: 310 × 200 × 2.0</text><text x="842" y="387" class="txt">2 × vent carrier: 165 × 82 × 2.0</text><text x="842" y="414" class="txt">Controls: 2 × Ø22.5 + 1 × Ø16.2</text><text x="842" y="457" class="bold">DO NOT SCALE PHOTO</text><text x="842" y="484" class="small">Measure actual LCD, vents, switches,</text><text x="842" y="504" class="small">dashboard opening and rear envelope.</text><text x="842" y="524" class="small">Cut carriers only after sign-off.</text>
<text x="55" y="708" class="small">Finish: deburr, edge-radius, zinc-rich epoxy primer, satin black powder coat. Earth screen chassis separately. No sharp duct/wiring edges.</text></svg>'''
    (OUT / "dashboard_lcd_hvac_fascia_rev_a_dimensioned_front.svg").write_text(svg, encoding="utf-8")


def write_pdf() -> None:
    path = OUT / "j40_dashboard_lcd_hvac_fascia_rev_a_dimension_sheet.pdf"
    c = canvas.Canvas(str(path), pagesize=landscape(A3))
    w, h = landscape(A3)
    c.setTitle("J40 Dashboard LCD HVAC Fascia Rev A")
    c.setFont("Helvetica-Bold", 18)
    c.drawString(18*mm, h-18*mm, "J40 Dashboard LCD / HVAC Replacement Fascia — Rev A")
    c.setFont("Helvetica", 9)
    c.drawRightString(w-18*mm, h-18*mm, "Units: mm | Main fascia released; bought-part carrier apertures HOLD")
    x, y = 24*mm, 33*mm
    maxw, maxh = 480*mm*0.42, 320*mm*0.42
    s = min(maxw/480, maxh/320)
    c.setFillColor(HexColor("#e7ebee")); c.setStrokeColor(HexColor("#111111")); c.roundRect(x,y,480*s,320*s,8*s,fill=1,stroke=1)
    c.setFillColor(HexColor("#fff4df")); c.setStrokeColor(HexColor("#a85f00")); c.setDash(5,4)
    c.roundRect(x+95*s,y+124*s,290*s,180*s,4*s,fill=1,stroke=1)
    c.roundRect(x+82*s,y+49*s,145*s,62*s,3*s,fill=1,stroke=1); c.roundRect(x+253*s,y+49*s,145*s,62*s,3*s,fill=1,stroke=1); c.setDash()
    c.setFillColor(HexColor("#ffffff")); c.setStrokeColor(HexColor("#111111"))
    for hx,hy in ((18,18),(240,18),(462,18),(18,160),(462,160),(18,302),(240,302),(462,302)):
        c.circle(x+hx*s,y+hy*s,2.75*s,fill=1,stroke=1)
    c.setStrokeColor(HexColor("#365b78"))
    for hx,hy in ((90,119),(390,119),(90,309),(390,309),(77,44),(232,44),(77,116),(232,116),(248,44),(403,44),(248,116),(403,116)):
        c.circle(x+hx*s,y+hy*s,2.25*s,fill=1,stroke=1)
    c.setStrokeColor(HexColor("#111111"))
    c.setFillColor(HexColor("#1c2226")); c.circle(x+185*s,y+25*s,11.25*s,fill=1,stroke=1); c.circle(x+295*s,y+25*s,11.25*s,fill=1,stroke=1)
    c.setFillColor(HexColor("#b51d1d")); c.circle(x+240*s,y+25*s,8.1*s,fill=1,stroke=1)
    c.setFillColor(HexColor("#20262b")); c.setFont("Helvetica-Bold",11); c.drawCentredString(x+240*s,y+210*s,"REMOVABLE 9-INCH LCD CARRIER")
    c.setFont("Helvetica",8); c.drawCentredString(x+240*s,y+194*s,"Nominal 233 × 135 aperture is reference only")
    nx = 270*mm
    c.setFont("Helvetica-Bold",12); c.drawString(nx,h-45*mm,"Released geometry")
    rows=[("Main fascia","480 × 320 × 1.5 CR4 mild steel; R8 corners"),("Dashboard rough cut","440 × 280 nominal; transfer actual shape in vehicle"),("Rear stiffener","460 × 300 × 2.0 mild steel ring"),("LCD carrier","310 × 200 × 2.0; actual screen aperture HOLD"),("Vent carriers","2 × 165 × 82 × 2.0; actual vent aperture HOLD"),("HVAC controls","2 × Ø22.5, confirm bought selector thread/body"),("Hazard","Ø16.2, confirm bought pushbutton thread/body"),("Carrier mounting","12 × Ø4.5 for M4 low-profile screws + captive nuts"),("Fascia mounting","8 × Ø5.5 for M5 button-head screws + rivnuts/nutplates")]
    yy=h-57*mm
    for a,b in rows:
        c.setFont("Helvetica-Bold",9); c.drawString(nx,yy,a); c.setFont("Helvetica",9); c.drawString(nx+40*mm,yy,b); yy-=8*mm
    c.setFillColor(HexColor("#8b1e1e")); c.setFont("Helvetica-Bold",12); c.drawString(nx,yy-3*mm,"PRODUCTION HOLD POINTS")
    c.setFillColor(HexColor("#20262b")); c.setFont("Helvetica",9)
    for note in ["1. Scan or cardboard-template the actual dash cut boundary; preserve gauge and glovebox structure.","2. Caliper-measure LCD visible face, rear body, connector sweep and fixing pattern.","3. Measure vent face, flange, neck OD and total rear depth; prove 63.5 mm hose connection.","4. Dry-fit screen, carriers, ducts and switch contact blocks; steering/wiper/heater interference must clear.","5. Owner signs the 1:1 paper plot before cutting the vehicle or the final carrier apertures."]:
        yy-=7*mm; c.drawString(nx,yy,note)
    c.setFont("Helvetica-Bold",10); c.drawString(18*mm,15*mm,"DO NOT SCALE THE CONCEPT IMAGE. DXF is authoritative for released plate geometry; orange carrier apertures remain HOLD.")
    c.showPage(); c.save()


def write_csvs() -> None:
    with (OUT / "fabricator_cut_list.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["part","qty","material","thickness_mm","finish","file","release"])
        w.writerows([
            ["main fascia",1,"CR4 mild steel",1.5,"satin black powder coat","dashboard_main_fascia_rev_a.dxf","RELEASED after vehicle template confirms 480 x 320 fits"],
            ["rear stiffening frame",1,"mild steel",2.0,"epoxy primer + satin black","dashboard_rear_stiffening_frame_rev_a.dxf","RELEASED after rear clearance check"],
            ["LCD carrier blank",1,"aluminium 5052-H32",2.0,"satin black powder coat","lcd_carrier_blank_rev_a.dxf","OUTER/HOLES released; inner aperture HOLD"],
            ["HVAC vent carrier blank",2,"aluminium 5052-H32",2.0,"satin black powder coat","hvac_vent_carrier_blank_rev_a.dxf","OUTER/HOLES released; inner aperture HOLD"],
        ])
    with (OUT / "measurement_and_release_schedule.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["id","measurement","nominal_mm","required_evidence","status"])
        w.writerows([
            ["M1","usable flat dashboard area W x H","at least 480 x 320","cardboard template + ruler photos","HOLD"],
            ["M2","proposed dashboard cut W x H","440 x 280","inside/outside marked photos; check seams/flanges","HOLD"],
            ["M3","LCD visible face W x H","about 229 x 145","caliper/tape photos and model label","HOLD"],
            ["M4","LCD rear chassis W x H x D","supplier-specific","caliper/tape photos including plugs","HOLD"],
            ["M5","LCD mounting centres/thread","supplier-specific","rear-face rubbing or drawing","HOLD"],
            ["M6","vent flange and cutout W x H","carrier ref 125 x 50","actual part and tape photos","HOLD"],
            ["M7","vent hose neck OD and rear depth","63.5 OD target","actual part + hose trial","HOLD"],
            ["M8","selector threaded bush/body","22 mm class; Ø22.5 cut","caliper actual bought switch","HOLD"],
            ["M9","hazard threaded bush/body","16 mm class; Ø16.2 cut","caliper actual bought switch","HOLD"],
            ["M10","rear clear depth at screen/vents","140 min target","straightedge/depth-gauge photos","HOLD"],
        ])


def write_readme() -> None:
    text = """# J40 Dashboard 9-inch LCD / HVAC Fascia — Rev A

This package is ready to send to the CNC/fabrication shop for quotation, vehicle templating, a 1:1 paper plot and fabrication of the released blank/carrier architecture. It intentionally does **not** authorize cutting the vehicle or the bought-part apertures until the actual 9-inch LCD, vents, industrial switches and dashboard have been measured and dry-fitted.

## Design decision

- Remove a large nominal `440 × 280 mm` middle dashboard section only after a cardboard template proves the boundary.
- Fit a `480 × 320 × 1.5 mm` CNC-cut main fascia with `20 mm` nominal overlap, radiused corners and eight M5 service fasteners.
- Back it with a `460 × 300 × 2.0 mm` stiffening ring. The screen must also have two rear support rails/tabs tied into the dashboard structure; the face sheet must not carry screen mass alone.
- Use a removable `310 × 200 × 2.0 mm` LCD carrier. Its nominal `233 × 135 mm` screen aperture is a HOLD reference, not a production cut.
- Use two removable vent carriers below the screen. Their internal openings follow the actual directional louver, with `63.5 mm / 2.5 inch` hose necks preferred.
- Fasten the LCD carrier at four corners and each vent carrier at four corners with M4 low-profile screws into captive nuts/nutplates. The matching Ø4.5 mm holes are released in both the fascia and carrier blanks.
- Put the two HVAC selectors (`blower OFF/LOW/HIGH` and `A/C enable OFF/ON`) and the red hazard button in the lower center strip.
- Replace the four original pull switches beside the gauge cluster with the bought `22 mm` industrial selectors in the existing positions after centres and rear contact-block clearance are transferred from the vehicle. Do not move them into the screen fascia.

## Control allocation

| Position | Function | Device |
| --- | --- | --- |
| Driver cluster 1 | Wipers OFF/LOW/HIGH | 3-position maintained industrial selector |
| Driver cluster 2 | Lights OFF/PARK/HEAD | 3-position maintained industrial selector |
| Driver cluster 3 | Spot lamps OFF/ON | 2-position maintained selector, relay control only |
| Driver cluster 4 | Auxiliary accessory OFF/ON | 2-position maintained selector, relay control only |
| Center lower left | Blower OFF/LOW/HIGH | 3-position maintained selector |
| Center lower middle | Hazards | Red 16 mm latching illuminated pushbutton |
| Center lower right | A/C enable OFF/ON | 2-position maintained selector, relay control only |
| Near ignition / separate | Diesel fuel stop RUN/STOP | Dedicated selector; retain manual cable backup |

Switches command relays or controller inputs; do not carry lamp, blower, clutch or accessory current directly unless the switch contact rating and protection are engineered for that load.

## HVAC and rear-envelope rules

- Preferred airflow path: evaporator/plenum → smooth `2.5 inch` flexible duct → vent neck. Keep hose runs short, supported and free of kinks.
- Prove at least `140 mm` usable depth behind the LCD zone including plug bend radius and `110 mm` behind each vent zone including hose clamp and bend.
- Keep duct clear of screen heat sink, wiring, sharp cut edges, wiper linkage and heater controls.
- Provide a demist strategy before assigning all evaporator outlets to face vents. The broader four-outlet plan remains in `docs/hvac-dashboard-vent-duct-layout-20260602.md`.

## Fabrication sequence

1. Remove loose trim and expose both sides of the proposed cut. Photograph wiring, braces and seams.
2. Make a full-size cardboard fascia and rear-depth buck from this drawing. Confirm sight line, gear-lever/steering clearance, glovebox opening and screen glare angle.
3. Place the actual LCD, vents and selectors on the buck. Record M1–M10 in `measurement_and_release_schedule.csv`.
4. Print the SVG/PDF at 1:1 and obtain owner sign-off on the actual cut line and component centres.
5. CNC/laser cut the fascia and rear frame; form only if the vehicle template proves a crown or flange is needed. Tack nutplates/rivnuts on the rear frame away from visible metal.
6. Cut the removable carrier apertures from the actual component rubbings/drawings. Dry assemble the complete module on the bench.
7. Cut the vehicle undersize, trim to the template, seal all raw edges, install the rear frame, then the fascia. No welding near installed electronics, ducts or upholstery.
8. Bond the fascia electrically to body earth; fuse/relay circuits separately; label the rear harness; leave a removable service loop.

## Acceptance

- Dashboard structure, gauge cluster and glovebox remain rigid and undistorted.
- LCD is removable without removing the whole dash; connectors can be reached and cannot chafe.
- Carrier fasteners engage captive threads fully, sit flush/low-profile and remain accessible from the cabin side.
- Each vent rotates/aims and can accept/remove its hose with the fascia installed.
- All selectors have anti-rotation features, correct legends and at least `10 mm` clearance around rear contact blocks/wiring.
- No sharp edge is reachable; all cut steel is epoxy-primed; visible finish is even satin black.
- Full electrical functional test, blower airflow test, A/C clutch logic test and road vibration/rattle test pass.

## Files

- `dashboard_main_fascia_rev_a.dxf` — released main plate geometry.
- `dashboard_rear_stiffening_frame_rev_a.dxf` — rear reinforcing ring.
- `lcd_carrier_blank_rev_a.dxf` — outer blank released; orange/reference screen aperture remains HOLD.
- `hvac_vent_carrier_blank_rev_a.dxf` — make two; inner vent aperture remains HOLD.
- `dashboard_lcd_hvac_fascia_rev_a_dimensioned_front.svg` and PDF — shop drawing/visualisation.
- `dashboard_lcd_hvac_fascia_rev_a_concept.png` — realistic intent only; never scale it.

## Release state

**Ready for CNC shop quotation, vehicle scan/template, cardboard/cheap-sheet prototype and the released outer blanks. Not released for final dashboard cut or screen/vent carrier apertures until M1–M10 are recorded and signed.**
"""
    (OUT / "README.md").write_text(text, encoding="utf-8")


def package() -> None:
    DELIVERABLE.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DELIVERABLE, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.iterdir()):
            z.write(p, f"dashboard_lcd_hvac_fascia_rev_a/{p.name}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    make_dxfs(); write_svg(); write_pdf(); write_csvs(); write_readme()
    concept_src = Path("/Users/davidpridmore/.codex/generated_images/019fb8d3-8269-7eb0-b457-d806a3cefbd4/exec-7f40e883-f434-4524-9741-1de3167bfd32.png")
    if concept_src.exists():
        shutil.copy2(concept_src, OUT / "dashboard_lcd_hvac_fascia_rev_a_concept.png")
    package()
    print(OUT)
    print(DELIVERABLE)


if __name__ == "__main__":
    main()
