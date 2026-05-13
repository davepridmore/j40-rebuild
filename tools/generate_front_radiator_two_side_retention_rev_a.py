from __future__ import annotations

import csv
from pathlib import Path
from typing import Sequence

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm as pdf_mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

import generate_electrical_module_drawings as base


OUT_DIR = Path("/Users/davidpridmore/IdeaProjects/J40/data/manual/fabrication/front_radiator_two_side_retention_rev_a")
PDF_NAME = "j40_front_radiator_two_side_retention_rev_a_dimension_sheet.pdf"
VISUAL_SVG_NAME = "front_radiator_two_side_retention_rev_a_3d_visualisation.svg"
VISUAL_HTML_NAME = "front_radiator_two_side_retention_rev_a_3d_visualisation.html"
ASSEMBLED_VISUAL_SVG_NAME = "front_radiator_two_side_retention_rev_a_assembled_3d_visualisation.svg"
ASSEMBLED_VISUAL_HTML_NAME = "front_radiator_two_side_retention_rev_a_assembled_3d_visualisation.html"

MAIN_FACE_WIDTH_MM = 48
TOP_RETURN_MM = 58
UPRIGHT_HEIGHT_MM = 410
CHASSIS_BRIDGE_MM = 70
FAR_SADDLE_LEG_MM = 80
DEVELOPED_TEMPLATE_LENGTH_MM = TOP_RETURN_MM + UPRIGHT_HEIGHT_MM + CHASSIS_BRIDGE_MM + FAR_SADDLE_LEG_MM


def saddle_right_angle_post() -> base.Drawing:
    bridge_start = TOP_RETURN_MM + UPRIGHT_HEIGHT_MM
    bridge_end = bridge_start + CHASSIS_BRIDGE_MM
    near_bolt_y = TOP_RETURN_MM + UPRIGHT_HEIGHT_MM - 50
    far_bolt_y = bridge_end + 25
    cut_polys = [
        base.Poly([(0, 0), (MAIN_FACE_WIDTH_MM, 0), (MAIN_FACE_WIDTH_MM, DEVELOPED_TEMPLATE_LENGTH_MM), (0, DEVELOPED_TEMPLATE_LENGTH_MM)]),
        # Top screw slot on the bent return. Final diameter/slot follows the radiator screw and isolator stack.
        base.rounded_slot_poly(17, 18, 14, 32),
        # Through-bolt slots for the two chassis-straddling legs. Final alignment follows a cardboard wrap.
        base.rounded_slot_poly(14, near_bolt_y, 20, 34),
        base.rounded_slot_poly(14, far_bolt_y, 20, 34),
    ]
    bend_lines = [
        base.Line(0, TOP_RETURN_MM, MAIN_FACE_WIDTH_MM, TOP_RETURN_MM),
        base.Line(0, bridge_start, MAIN_FACE_WIDTH_MM, bridge_start),
        base.Line(0, bridge_end, MAIN_FACE_WIDTH_MM, bridge_end),
    ]
    notes = [
        "Single-piece radiator saddle/post main-face template: 48 x 618 x 4.0 mm mild steel, based on the existing-side radiator bracket measurement set.",
        "Form or use a mild-steel angle section so the 48 mm measured face has a perpendicular return flange; the final upright is not a flat strap.",
        "Bend 90 degrees at the top datum so the measured 58 mm return becomes the radiator screw tab in the same formed angle section, with the top return carried back to the far edge of the angle return flange.",
        "Bend around the chassis/front-support section so the lower portion forms an inverted-U saddle from the formed angle: near-side leg, chassis top bridge, and far-side clamp leg.",
        "Measured bend basis is 58 mm top return, 410 mm upright/post height, 70 mm chassis bridge allowance, and 80 mm far-side saddle leg.",
        "The top slot is a transfer template from the existing-side bracket. Open final screw diameter/slot after right-side dry-fit confirms radiator ear offset and rubber washer stack.",
        "Through-bolt slots are site-fit fields for a bolt through the two saddle legs and the chassis/front-support section. Use crush tube/spacer practice if the chassis section is boxed.",
        "Do not weld this bracket as the default route. It is retained by the two legs straddling the chassis and the through-bolt.",
    ]
    return base.Drawing(
        "front_radiator_saddle_right_angle_post_rev_a",
        MAIN_FACE_WIDTH_MM,
        DEVELOPED_TEMPLATE_LENGTH_MM,
        cut_polys,
        [],
        [],
        bend_lines,
        notes,
    )


def drawings() -> list[base.Drawing]:
    return [saddle_right_angle_post()]


def write_pdf(drawing_set: Sequence[base.Drawing]) -> None:
    pdf_path = OUT_DIR / PDF_NAME
    c = canvas.Canvas(str(pdf_path), pagesize=landscape(A4))
    page_w, page_h = landscape(A4)
    margin = 14 * pdf_mm

    for drawing in drawing_set:
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin, page_h - margin, drawing.name)
        c.setFont("Helvetica", 9)
        c.drawRightString(page_w - margin, page_h - margin, "Rev A | Units: mm | Bolt-through radiator saddle/post template")

        gap = 8 * pdf_mm
        plot_w = 184 * pdf_mm
        notes_w = page_w - (margin * 2) - plot_w - gap
        plot_x = margin
        plot_y = 40 * pdf_mm
        plot_h = page_h - 62 * pdf_mm

        min_x, max_x, min_y, max_y = base.drawing_bounds(drawing)
        geom_w = max_x - min_x
        geom_h = max_y - min_y
        scale = min(plot_w / geom_w, plot_h / geom_h)
        ox = plot_x + (plot_w - geom_w * scale) / 2 - min_x * scale
        oy = plot_y + (plot_h - geom_h * scale) / 2 - min_y * scale

        c.setStrokeColor(HexColor("#111111"))
        c.setLineWidth(1)
        c.rect(plot_x, plot_y, plot_w, plot_h, stroke=1, fill=0)

        c.setLineWidth(0.8)
        for poly in drawing.cut_polys:
            base.draw_poly(c, poly, ox, oy, scale)
        for rect in drawing.cut_rects:
            base.draw_rect(c, rect, ox, oy, scale)
        for circle in drawing.cut_circles:
            base.draw_circle(c, circle, ox, oy, scale)

        c.setStrokeColor(HexColor("#0b5fff"))
        c.setLineWidth(0.6)
        c.setDash(4, 3)
        for bend in drawing.bend_lines:
            c.line(ox + bend.x1 * scale, oy + bend.y1 * scale, ox + bend.x2 * scale, oy + bend.y2 * scale)
        c.setDash()

        left = ox + min_x * scale
        right = ox + max_x * scale
        bottom = oy + min_y * scale
        top = oy + max_y * scale
        base.draw_dimension_h(c, left, right, bottom - 10 * pdf_mm, f"overall width {base.mm(geom_w)}")
        base.draw_dimension_v(c, left - 10 * pdf_mm, bottom, top, f"template length {base.mm(geom_h)}")
        bend_top = oy + TOP_RETURN_MM * scale
        bend_bridge_start = oy + (TOP_RETURN_MM + UPRIGHT_HEIGHT_MM) * scale
        bend_bridge_end = oy + (TOP_RETURN_MM + UPRIGHT_HEIGHT_MM + CHASSIS_BRIDGE_MM) * scale
        base.draw_dimension_v(c, right + 8 * pdf_mm, bottom, bend_top, "top return 58")
        base.draw_dimension_v(c, right + 16 * pdf_mm, bend_top, bend_bridge_start, "upright/post height 410")
        base.draw_dimension_v(c, right + 24 * pdf_mm, bend_bridge_start, bend_bridge_end, "chassis bridge 70")
        base.draw_dimension_v(c, right + 32 * pdf_mm, bend_bridge_end, top, "far saddle leg 80")

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
        draw_wrapped_bullet("Blue dashed lines are the imported existing-side bend datums. The 410 mm value is the upright height, not the total developed length. Confirm right-side chassis bridge width and fold direction with a cardboard wrap before cutting steel.")
        draw_wrapped_bullet("Final release still needs right-side dry-fit photos with ruler, radiator ear offset, through-bolt route, rubber stack, and fan clearance recorded.")

        c.setFont("Helvetica-Bold", 11)
        c.drawString(notes_x, notes_y - (row + 2) * 5.3 * pdf_mm, "Output Files")
        c.setFont("Helvetica", 9)
        c.drawString(notes_x, notes_y - (row + 3) * 5.3 * pdf_mm, f"- DXF: {drawing.name}.dxf")
        c.drawString(notes_x, notes_y - (row + 4) * 5.3 * pdf_mm, f"- SVG: {drawing.name}.svg")

        c.setFont("Helvetica", 8)
        c.drawString(margin, 9 * pdf_mm, "Prepared from the left-side right-angle radiator bracket photo and bolt-through saddle update.")
        c.drawRightString(page_w - margin, 9 * pdf_mm, f"Output: {PDF_NAME}")
        c.showPage()
    c.save()


def write_static_3d_visualisation() -> None:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="920" height="620" viewBox="0 0 920 620" role="img" aria-labelledby="title desc">
  <title id="title">Front radiator formed-angle saddle post Rev A 3D visualisation</title>
  <desc id="desc">Single-piece steel formed-angle post with a top screw point and a bolt-through saddle wrapped over the chassis/front-support section.</desc>
  <style>
    .bg { fill: #f5f6f7; }
    .shadow { fill: #d7dde2; opacity: 0.55; }
    .chassis { fill: #59636c; stroke: #2b343b; stroke-width: 2; }
    .bracket { fill: #bfc8d1; stroke: #59636c; stroke-width: 2; }
    .bracket-side { fill: #93a0aa; stroke: #59636c; stroke-width: 2; }
    .bolt { fill: #c4a35a; stroke: #6f5d2f; stroke-width: 1.2; }
    .hole { fill: #f5f6f7; stroke: #59636c; stroke-width: 2; }
    .label { font: 700 17px Arial, sans-serif; fill: #1d252c; }
    .small { font: 13px Arial, sans-serif; fill: #54616c; }
  </style>
  <rect class="bg" width="920" height="620" />
  <ellipse class="shadow" cx="470" cy="458" rx="230" ry="48" />
  <polygon class="chassis" points="390,286 520,326 636,282 506,242" />
  <polygon class="chassis" points="390,286 520,326 520,430 390,390" />
  <polygon class="chassis" points="520,326 636,282 636,386 520,430" />
  <polygon class="bracket" points="430,54 468,66 468,286 430,274" />
  <polygon class="bracket-side" points="468,66 490,56 490,276 468,286" />
  <polygon class="bracket-side" points="430,54 292,104 330,116 468,66" />
  <polygon class="bracket" points="330,116 386,94 490,56 468,66" />
  <polygon class="bracket-side" points="326,92 364,104 364,126 326,114" />
  <circle class="hole" cx="319" cy="110" r="8" />
  <polygon class="bracket-side" points="428,274 520,302 558,290 466,262" />
  <polygon class="bracket" points="466,262 488,252 574,278 558,290" />
  <polygon class="bracket-side" points="466,262 558,290 558,314 466,286" />
  <polygon class="bracket" points="428,274 466,286 466,384 428,372" />
  <polygon class="bracket" points="558,290 596,302 596,394 558,382" />
  <line x1="426" y1="360" x2="594" y2="402" stroke="#c4a35a" stroke-width="10" stroke-linecap="round" />
  <circle class="bolt" cx="426" cy="360" r="8" />
  <circle class="bolt" cx="594" cy="402" r="8" />
  <text class="label" x="90" y="82">Right-angle saddle post Rev A</text>
  <text class="small" x="90" y="111">4 mm formed angle section: 410 mm upright height, 618 mm developed template length.</text>
  <text class="label" x="244" y="116">Full-depth 90 deg top screw tab</text>
  <text class="label" x="486" y="168">410 mm formed-angle upright</text>
  <text class="label" x="590" y="274">Far saddle leg</text>
  <text class="label" x="330" y="520">Saddle bridge sits over both chassis sides and is through-bolted</text>
</svg>
"""
    (OUT_DIR / VISUAL_SVG_NAME).write_text(svg, encoding="utf-8")


def interactive_html(*, assembled: bool) -> str:
    title = "Right-Angle Saddle Post Attached To Chassis Rev A" if assembled else "Right-Angle Saddle Post Rev A"
    fallback = ASSEMBLED_VISUAL_SVG_NAME if assembled else VISUAL_SVG_NAME
    bracket_name = "Attached right-angle saddle post" if assembled else "Right-angle saddle post"
    view_label = "Chassis-attached view" if assembled else "Part geometry view"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} - 3D Visualisation</title>
  <link rel="icon" href="data:,">
  <style>
    :root {{ font-family: Arial, Helvetica, sans-serif; background: #f5f6f7; color: #1d252c; }}
    body {{ margin: 0; min-height: 100vh; display: grid; grid-template-rows: auto 1fr; }}
    body.embed {{ grid-template-rows: 1fr; }}
    header {{ padding: 16px 22px 10px; background: #ffffff; border-bottom: 1px solid #d8dde2; }}
    h1 {{ margin: 0; font-size: clamp(20px, 3vw, 30px); letter-spacing: 0; }}
    .meta {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}
    .chip {{ border: 1px solid #c8d0d8; border-radius: 999px; padding: 5px 9px; background: #f8fafb; font-size: 13px; }}
    main {{ display: grid; grid-template-columns: minmax(0, 1fr) 300px; min-height: 0; }}
    #viewport {{ position: relative; min-height: 560px; overflow: hidden; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
    aside {{ border-left: 1px solid #d8dde2; background: #ffffff; padding: 18px; }}
    h2 {{ margin: 0 0 12px; font-size: 18px; letter-spacing: 0; }}
    dl {{ margin: 0; display: grid; gap: 12px; }}
    dt {{ font-weight: 700; }}
    dd {{ margin: 3px 0 0; color: #54616c; font-size: 14px; line-height: 1.45; }}
    #fallback {{ position: absolute; inset: 0; display: grid; place-items: center; padding: 20px; background: #f5f6f7; }}
    #fallback img {{ width: min(94vw, 920px); max-height: 82vh; object-fit: contain; }}
    body.is-three-ready #fallback {{ display: none; }}
    body.embed header, body.embed aside {{ display: none; }}
    body.embed main {{ grid-template-columns: 1fr; min-height: 100vh; }}
    body.embed #viewport {{ min-height: 100vh; }}
    @media (max-width: 820px) {{ main {{ grid-template-columns: 1fr; }} #viewport {{ min-height: 430px; }} aside {{ border-left: 0; border-top: 1px solid #d8dde2; }} }}
  </style>
  <script type="importmap">
    {{"imports":{{"three":"https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.164.1/examples/jsm/"}}}}
  </script>
</head>
<body>
  <script>
    if (new URLSearchParams(window.location.search).has("embed")) {{
      document.body.classList.add("embed");
    }}
  </script>
  <header>
    <h1>{title}</h1>
    <div class="meta">
      <span class="chip">{view_label}</span>
      <span class="chip">Single formed angle section</span>
      <span class="chip">410 mm upright</span>
      <span class="chip">618 mm developed template</span>
      <span class="chip">Saddle over chassis</span>
      <span class="chip">Top screw point</span>
    </div>
  </header>
  <main>
    <section id="viewport" aria-label="Interactive 3D radiator saddle bracket visualisation">
      <div id="fallback"><img src="./{fallback}" alt="Static radiator saddle bracket visualisation"></div>
    </section>
    <aside>
      <h2>Assembly Read</h2>
      <dl>
        <div><dt>Shape</dt><dd>One formed 4 mm steel angle section: 48 mm main face with a perpendicular return flange, 410 mm upright height, 618 mm developed main-face template length, full-depth 58 mm top return, top bridge over the chassis, and clean saddle legs down both chassis sides.</dd></div>
        <div><dt>Chassis attachment</dt><dd>The saddle bridge sits on the top face of the chassis/front-support section. The near-side lower continuation of the upright and the far-side saddle leg drop down both chassis sides without extra side ears.</dd></div>
        <div><dt>Release hold</dt><dd>Final top hole transfer, chassis bridge width, through-bolt route, and rubber washer stack follow the existing-side measurements and right-side dry-fit.</dd></div>
      </dl>
    </aside>
  </main>
  <script type="module">
    import * as THREE from "three";
    import {{ OrbitControls }} from "three/addons/controls/OrbitControls.js";

    const mount = document.getElementById("viewport");
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f6f7);
    const camera = new THREE.PerspectiveCamera(36, 1, 1, 1800);
    camera.position.set(430, 480, 880);
    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: false, preserveDrawingBuffer: true }});
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = true;
    mount.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(0, 225, 0);
    controls.enableDamping = true;
    controls.minDistance = 280;
    controls.maxDistance = 1250;
    controls.maxPolarAngle = Math.PI * 0.52;

    const root = new THREE.Group();
    scene.add(root);
    const materials = {{
      steel: new THREE.MeshStandardMaterial({{ color: 0xbfc8d1, metalness: 0.35, roughness: 0.38 }}),
      steelSide: new THREE.MeshStandardMaterial({{ color: 0x8f9ba5, metalness: 0.35, roughness: 0.4 }}),
      darkSteel: new THREE.MeshStandardMaterial({{ color: 0x59636c, metalness: 0.45, roughness: 0.5 }}),
      brass: new THREE.MeshStandardMaterial({{ color: 0xc4a35a, metalness: 0.4, roughness: 0.36 }}),
      hole: new THREE.MeshStandardMaterial({{ color: 0xf5f6f7, roughness: 0.5 }}),
    }};

    function box(name, x, y, z, w, h, d, material) {{
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
      mesh.name = name;
      mesh.position.set(x, y, z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      root.add(mesh);
      return mesh;
    }}
    function cyl(name, x, y, z, radius, depth, material, rotationX = Math.PI / 2) {{
      const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, depth, 48), material);
      mesh.name = name;
      mesh.rotation.x = rotationX;
      mesh.position.set(x, y, z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      root.add(mesh);
      return mesh;
    }}
    function angleVertical(name, x, y, z, height) {{
      box(name + " main flange", x, y, z, 6, height, 48, materials.steel);
      box(name + " visible perpendicular return flange", x + 24, y, z + 21, 48, height, 6, materials.steelSide);
    }}
    function angleHorizontalX(name, x, y, z, length) {{
      box(name + " horizontal flange", x, y, z, length, 6, 48, materials.steel);
      box(name + " visible perpendicular return flange", x, y - 24, z + 21, length, 48, 6, materials.steelSide);
    }}
    function saddleLegVertical(name, x, y, z, height) {{
      box(name + " clean down-leg face", x, y, z, 6, height, 48, materials.steel);
    }}

    box("Chassis/front support section", 0, 55, 0, 70, 70, 130, materials.darkSteel);
    angleVertical("{bracket_name} formed angle upright/post height 410 mm", -40, 295, 0, 410);
    angleHorizontalX("{bracket_name} full-depth formed angle 90 degree top screw return 58 mm", -48, 503, 0, 112);
    cyl("Top screw point through 90 degree tab", -94, 507, 0, 6, 8, materials.hole, 0);
    saddleLegVertical("{bracket_name} clean near-side saddle leg down chassis side", -40, 50, 0, 80);
    angleHorizontalX("{bracket_name} flush formed angle top saddle bridge between the saddle legs", 0, 93, 0, 86);
    saddleLegVertical("{bracket_name} clean far-side saddle leg down chassis side", 40, 50, 0, 80);
    box("Through-bolt across both saddle legs and chassis", 0, 50, 0, 112, 8, 8, materials.brass);
    cyl("Near-side saddle through-bolt washer", -55, 50, 0, 11, 5, materials.brass, 0);
    cyl("Far-side saddle through-bolt washer", 55, 50, 0, 11, 5, materials.brass, 0);

    scene.add(new THREE.HemisphereLight(0xffffff, 0x98a1aa, 2.2));
    const key = new THREE.DirectionalLight(0xffffff, 2.4);
    key.position.set(260, 420, 300);
    key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    scene.add(key);
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(650, 520), new THREE.ShadowMaterial({{ color: 0x000000, opacity: 0.12 }}));
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -86;
    ground.receiveShadow = true;
    scene.add(ground);

    function resize() {{
      const width = mount.clientWidth;
      const height = mount.clientHeight;
      renderer.setSize(width, height, false);
      camera.aspect = width / Math.max(1, height);
      camera.updateProjectionMatrix();
    }}
    function animate() {{
      controls.update();
      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    }}
    resize();
    window.addEventListener("resize", resize);
    document.body.classList.add("is-three-ready");
    animate();
  </script>
</body>
</html>
"""


def write_interactive_3d_visualisation() -> None:
    (OUT_DIR / VISUAL_HTML_NAME).write_text(interactive_html(assembled=False), encoding="utf-8")


def write_assembled_static_3d_visualisation() -> None:
    svg = (OUT_DIR / VISUAL_SVG_NAME).read_text(encoding="utf-8")
    svg = svg.replace(
        "Front radiator right-angle saddle post Rev A 3D visualisation",
        "Front radiator right-angle saddle post Rev A chassis-attached visualisation",
    ).replace(
        "Single-piece steel right-angle post with a top screw point and a bolt-through saddle wrapped over the chassis/front-support section.",
        "Chassis-attached view of the single right-angle saddle post with the through-bolt installed.",
    ).replace(
        "Right-angle saddle post Rev A",
        "Right-angle saddle post attached to chassis",
    )
    (OUT_DIR / ASSEMBLED_VISUAL_SVG_NAME).write_text(svg, encoding="utf-8")


def write_assembled_interactive_3d_visualisation() -> None:
    (OUT_DIR / ASSEMBLED_VISUAL_HTML_NAME).write_text(interactive_html(assembled=True), encoding="utf-8")


def write_readme() -> None:
    text = """# J40 Front Radiator Two-Side Retention Pack - Rev A

This package now uses a single 4 mm mild-steel formed-angle radiator post with a chassis-straddling saddle at the bottom. The existing-side radiator bracket measurements are imported; the remaining hold is right-side transfer and dry-fit, not the basic bracket dimensions.

## Design Intent

- Replace the wire-held or one-sided radiator support condition with a simple bolt-through formed-angle post: upright leg, full-depth top screw tab, chassis bridge, and two chassis-side saddle legs.
- Avoid welding to the chassis as the default route. The two lower legs straddle the chassis/front-support section and are retained by a through-bolt.
- Preserve the radiator plane and fan clearance unless a dry-fit proves a correction is needed.
- Use rubber washers/bushes at the radiator screw as required, but do not fabricate a separate large rubber pad for this bracket unless the vehicle dry-fit proves it is needed.
- Use crush-tube/spacer practice if the through-bolt passes through boxed chassis/front-support metal.

## Part In This Package

1. `front_radiator_saddle_right_angle_post_rev_a` - 4 mm mild-steel formed angle section using the measured `48 mm` main face and `410 mm` upright height. The developed template length is now `618 mm`: `58 mm` top return, `410 mm` upright, `70 mm` chassis bridge, and `80 mm` far-side leg. The upright lower continuation is the near-side saddle leg.

## Existing-Side Measurement Basis

- Existing-side measurement photos are the basis for the main-face template and bends.
- Measured main face width: `48 mm`; the released 3D view now shows the perpendicular return flange so the post reads as a formed angle section rather than a flat strap.
- Upright/post height: `410 mm`; this is the height basis visible in the in-vehicle tape-measure photo, not the whole developed length.
- Developed main-face template length: `618 mm`.
- Top screw return: `58 mm`.
- Chassis bridge allowance: `70 mm`; verify this against the right-side chassis/front-support width before cutting final steel.
- Outer saddle leg: `80 mm`.
- Measurement basis rows are in `measurement_basis.csv`.

## 3D Visualisation

- `front_radiator_two_side_retention_rev_a_3d_visualisation.svg` is the static fabrication-read view.
- `front_radiator_two_side_retention_rev_a_3d_visualisation.html` is the interactive fabrication-read view.
- `front_radiator_two_side_retention_rev_a_assembled_3d_visualisation.svg` is the static attached assembly view.
- `front_radiator_two_side_retention_rev_a_assembled_3d_visualisation.html` is the interactive attached assembly view with the formed-angle return flange, full-depth top return, clean near/far saddle legs, through-bolt, and top screw shown together.

## Right-Side Holds Before Final Metal

- Transfer the existing-side top screw location to the right side and verify the radiator ear lands without pulling the radiator out of plane.
- Confirm right-side chassis/front-support width, cleaned metal condition, through-bolt route, and whether a crush tube/spacer is needed.
- Rubber washer/bush stack at the top screw.
- Fan-to-radiator clearance after the bracket is tightened.
- Hose sweep, bonnet closure, radiator service removal, and coating access.

## Fabrication Rules

- Use `4.0 mm` mild steel for the released template.
- Form a perpendicular return flange or use equivalent 4 mm stock angle before final transverse bends; mitre/relieve the bend points as needed so the angle section can form the top return and lower saddle cleanly.
- Bend the top return to match the left-side bracket direction and offset; the top return should continue back to the far edge of the formed angle section rather than stopping at the upright face.
- Bend the lower saddle around the actual chassis/front-support width so the near-side and far-side saddle legs sit down both chassis sides without added side ears or tabs.
- Through-bolt both saddle legs and chassis/front support; do not weld this bracket unless the bolted saddle route fails dry-fit.
- The top slot is a transfer aid from the existing-side bracket. Open the final screw hole after the right-side radiator ear and washer/bush stack are dry-fit.
- Deburr all edges, radius the top tab corners, and protect every cut edge before final assembly.

## Release State

This is ready for cardboard/flat-bar dry-fit and fabricator discussion using the imported existing-side dimensions. It does not release blind drilling of the final right-side holes until the dry-fit proves the transfer.
"""
    (OUT_DIR / "README.md").write_text(text, encoding="utf-8")


def write_cut_list() -> None:
    rows = [
        {
            "part_id": "RAD-SADDLE-POST-R",
            "file": "front_radiator_saddle_right_angle_post_rev_a.dxf",
            "qty": "1",
            "material": "4.0 mm mild steel",
            "process": "cut/form mild-steel angle section with 48 mm measured main face and 618 mm developed template length, bend full-depth 90 deg top return, wrap lower saddle over both chassis/front-support sides, drill final top screw and through-bolt fields after dry-fit",
            "notes": "Single-piece formed-angle saddle/post bracket from existing-side measurements: 48 mm measured main face, 410 mm upright height, perpendicular return flange, and 58/468/538 transverse bend datums. Near-side and far-side saddle legs straddle the chassis and a through-bolt retains the bracket; no welding by default.",
        },
    ]
    with (OUT_DIR / "fabricator_cut_list.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_inspection_checklist() -> None:
    rows = [
        {
            "check_id": "RAD-001",
            "stage": "measured_template_transfer",
            "acceptance": "Existing-side measurement basis is checked against measurement_basis.csv; right-side saddle wrap and top screw transfer are confirmed with cardboard or flat-bar dry-fit photographed with ruler.",
        },
        {
            "check_id": "RAD-002",
            "stage": "through_bolt",
            "acceptance": "Through-bolt passes through both saddle legs and sound chassis/front-support metal with correct washer/crush-tube/spacer support.",
        },
        {
            "check_id": "RAD-003",
            "stage": "top_screw",
            "acceptance": "Top screw, radiator ear, and rubber washer/bush stack fit without pulling the radiator out of plane.",
        },
        {
            "check_id": "RAD-004",
            "stage": "clearance",
            "acceptance": "Fan, shroud, belt, upper/lower hose, bonnet close, and radiator service-removal clearance pass after bracket is tightened.",
        },
        {
            "check_id": "RAD-005",
            "stage": "coating",
            "acceptance": "Cut edges and drilled holes are deburred, cleaned, primed/top-protected, and do not create a water trap.",
        },
    ]
    with (OUT_DIR / "inspection_checklist.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_measurement_basis() -> None:
    rows = [
        {
            "measurement_id": "RAD-MEAS-001",
            "source": "existing-side radiator bracket measurement set; photos 20260512_205417 through 20260512_213214",
            "dimension": "measured_main_face_width",
            "value_mm": "48",
            "status": "imported_existing_side_basis",
            "notes": "Measured visible face width for the formed angle section; do not treat the final upright as a flat strap.",
        },
        {
            "measurement_id": "RAD-MEAS-001A",
            "source": "existing-side radiator bracket measurement set; photos 20260512_205417 through 20260512_213214",
            "dimension": "formed_angle_return_flange",
            "value_mm": "visualised_perpendicular_return",
            "status": "imported_existing_side_basis",
            "notes": "Visual and release intent is an L-shaped formed angle section; exact return flange depth follows the existing-side measurement read and fabricator dry-fit.",
        },
        {
            "measurement_id": "RAD-MEAS-002",
            "source": "existing-side radiator bracket measurement set; photos 20260512_205417 through 20260512_213214",
            "dimension": "upright_post_height",
            "value_mm": "410",
            "status": "imported_existing_side_basis",
            "notes": "Measured upright height basis from the in-vehicle tape-measure view. Do not subtract the top return/bridge/leg from this value.",
        },
        {
            "measurement_id": "RAD-MEAS-003",
            "source": "existing-side radiator bracket measurement set; photos 20260512_205417 through 20260512_213214",
            "dimension": "top_screw_return",
            "value_mm": "58",
            "status": "imported_existing_side_basis",
            "notes": "First bend datum; forms the 90 degree top screw tab. The top tab should carry the formed angle back to the far edge of the return flange.",
        },
        {
            "measurement_id": "RAD-MEAS-004",
            "source": "existing-side radiator bracket measurement set; photos 20260512_205417 through 20260512_213214",
            "dimension": "developed_main_face_template_length",
            "value_mm": "618",
            "status": "derived_from_bend_stack",
            "notes": "Top return 58 + upright height 410 + chassis bridge 70 + far saddle leg 80.",
        },
        {
            "measurement_id": "RAD-MEAS-005",
            "source": "right-side chassis/front-support wrap required",
            "dimension": "chassis_bridge_allowance",
            "value_mm": "70",
            "status": "right_side_dry_fit_confirm",
            "notes": "Template allowance between lower saddle bend datums; verify against the actual right-side chassis/front-support width.",
        },
        {
            "measurement_id": "RAD-MEAS-006",
            "source": "existing-side radiator bracket measurement set; photos 20260512_205417 through 20260512_213214",
            "dimension": "outer_saddle_leg",
            "value_mm": "80",
            "status": "imported_existing_side_basis",
            "notes": "Far-side clamp leg after the chassis bridge; near-side leg is the lower continuation of the upright/post.",
        },
        {
            "measurement_id": "RAD-MEAS-007",
            "source": "right-side dry-fit transfer required",
            "dimension": "top_slot_template",
            "value_mm": "14 x 32 slot at x17 y18 on main face template",
            "status": "right_side_dry_fit_confirm",
            "notes": "Transfer aid only; open final hole after radiator ear, screw, and rubber stack are confirmed.",
        },
    ]
    with (OUT_DIR / "measurement_basis.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    base.OUT_DIR = OUT_DIR
    drawing_set = drawings()
    for drawing in drawing_set:
        base.write_svg(drawing)
        base.write_dxf(drawing)
    write_pdf(drawing_set)
    write_static_3d_visualisation()
    write_interactive_3d_visualisation()
    write_assembled_static_3d_visualisation()
    write_assembled_interactive_3d_visualisation()
    write_readme()
    write_cut_list()
    write_inspection_checklist()
    write_measurement_basis()


if __name__ == "__main__":
    main()
