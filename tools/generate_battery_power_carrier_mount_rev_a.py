from __future__ import annotations

import csv
from pathlib import Path

import generate_electrical_module_drawings as base


OUT_DIR = Path("/Users/davidpridmore/IdeaProjects/J40/data/manual/fabrication/battery_power_carrier_mount_rev_a")
base.OUT_DIR = OUT_DIR
base.PDF_NAME = "j40_battery_power_carrier_mount_rev_a_dimension_sheet.pdf"

VISUAL_SVG_NAME = "battery_power_carrier_mount_rev_a_3d_visualisation.svg"
VISUAL_HTML_NAME = "battery_power_carrier_mount_rev_a_3d_visualisation.html"
ASSEMBLED_VISUAL_SVG_NAME = "battery_power_carrier_mount_rev_a_assembled_3d_visualisation.svg"
ASSEMBLED_VISUAL_HTML_NAME = "battery_power_carrier_mount_rev_a_assembled_3d_visualisation.html"


def integrated_backplane() -> base.Drawing:
    cut_polys = [
        base.Poly([(0, 0), (340, 0), (340, 90), (0, 90)]),
        # Rail-to-stand / front-cavity pickup slots.
        base.rounded_slot_poly(18, 20, 42, 16),
        base.rounded_slot_poly(280, 20, 42, 16),
        base.rounded_slot_poly(18, 54, 42, 16),
        base.rounded_slot_poly(280, 54, 42, 16),
        # Folded relay tray / compact module bracket attachment field.
        base.rounded_slot_poly(92, 16, 34, 12),
        base.rounded_slot_poly(214, 16, 34, 12),
        base.rounded_slot_poly(92, 62, 34, 12),
        base.rounded_slot_poly(214, 62, 34, 12),
    ]
    cut_circles = [
        # Cable P-clip / saddle clamp holes.
        base.Circle(78, 45, 3.25),
        base.Circle(142, 45, 3.25),
        base.Circle(198, 45, 3.25),
        base.Circle(262, 45, 3.25),
    ]
    notes = [
        "Compact front service rail: 340 x 90 x 3.0 mm mild steel. This replaces the earlier large one-piece backplane.",
        "Use the folded aluminium relay carrier as its own tray; this steel rail only provides a compact vehicle-side pickup/brace if the front cavity map proves room.",
        "MIDI Rev C remains its own open 190 x 150 plate/subplate assembly; mount it on a small measured bracket or rails, not on a shared large backplane.",
        "Cutoff mounts on its own compact tab so it can be placed at the most accessible front/top position after cavity mapping.",
        "Do not cut final holes until the battery-cavity map proves the front/radiator-side volume, cable bend radius, and LHD clearance.",
    ]
    return base.Drawing(
        "battery_power_compact_front_service_rail_rev_b",
        340,
        90,
        cut_polys,
        [],
        cut_circles,
        [],
        notes,
    )


def single_chassis_pickup_mount() -> base.Drawing:
    cut_polys = [
        base.Poly([(0, 0), (220, 0), (220, 140), (0, 140)]),
        # Chassis-side field: one vehicle pickup location, final pitch taken from the chassis.
        base.rounded_slot_poly(20, 28, 38, 16),
        base.rounded_slot_poly(162, 28, 38, 16),
        base.rounded_slot_poly(20, 96, 38, 16),
        base.rounded_slot_poly(162, 96, 38, 16),
        # Upright/service-rail attach field.
        base.rounded_slot_poly(84, 28, 14, 34),
        base.rounded_slot_poly(122, 28, 14, 34),
        base.rounded_slot_poly(84, 80, 14, 34),
        base.rounded_slot_poly(122, 80, 14, 34),
    ]
    notes = [
        "Compact single chassis pickup mount: 220 x 140 x 4.0 mm mild steel base plate for the one known vehicle-side chassis attachment location.",
        "Chassis slots are site-fit only. Record the actual chassis hole pitch, metal thickness, and access before cutting final steel.",
        "Upright/service-rail slots take the carrier stand; do not add an independent second chassis fixing unless dry-fit proves the single-pickup route is not stiff enough.",
        "Use crush tubes/spacers if bolting through boxed structure. Deburr, prime, and protect before final assembly.",
    ]
    return base.Drawing(
        "battery_stand_compact_single_chassis_pickup_rev_b",
        220,
        140,
        cut_polys,
        [],
        [],
        [],
        notes,
    )


def single_mount_upright() -> base.Drawing:
    cut_polys = [
        base.Poly([(0, 0), (110, 0), (110, 220), (0, 220)]),
        base.rounded_slot_poly(18, 24, 16, 42),
        base.rounded_slot_poly(76, 24, 16, 42),
        base.rounded_slot_poly(18, 154, 16, 42),
        base.rounded_slot_poly(76, 154, 16, 42),
    ]
    cut_circles = [
        base.Circle(28, 102, 4.0),
        base.Circle(82, 102, 4.0),
        base.Circle(28, 128, 4.0),
        base.Circle(82, 128, 4.0),
    ]
    notes = [
        "Compact single-mount upright bridge side plate: 110 x 220 x 4.0 mm mild steel between the one chassis pickup and compact tray.",
        "Make two mirrored side plates around the single pickup bridge if the mock-up needs side-to-side stiffness. This is not a second chassis fixing location.",
        "Lower holes align to the single chassis pickup mount; upper holes align to the compact tray/front rail saddle.",
    ]
    return base.Drawing(
        "battery_stand_compact_single_mount_upright_rev_b",
        110,
        220,
        cut_polys,
        [],
        cut_circles,
        [],
        notes,
    )


def cutoff_guard() -> base.Drawing:
    cut_polys = [
        base.Poly([(0, 0), (170, 0), (170, 110), (0, 110)]),
        # Hand/finger clearance window around the cutoff knob/key.
        base.rounded_slot_poly(44, 30, 82, 46),
    ]
    cut_circles = [
        base.Circle(18, 16, 3.25),
        base.Circle(152, 16, 3.25),
        base.Circle(18, 94, 3.25),
        base.Circle(152, 94, 3.25),
    ]
    notes = [
        "Compact cutoff tab/guard: 170 x 110 x 2.0-3.0 mm aluminium or plastic; place independently in the most accessible front/top cavity.",
        "Open the switch hole only after the actual switch body, key/knob sweep, terminal studs, and cable-lug depth are measured.",
        "Guard must not trap water, block emergency access, or sit where the bonnet or battery terminal service envelope can contact it.",
    ]
    return base.Drawing(
        "battery_power_compact_cutoff_tab_rev_b",
        170,
        110,
        cut_polys,
        [],
        cut_circles,
        [],
        notes,
    )


def battery_stand_top_tray() -> base.Drawing:
    cut_polys = [
        base.Poly([(0, 0), (315, 0), (315, 265), (0, 265)]),
        # Battery hold-down / clamp slots.
        base.rounded_slot_poly(24, 38, 14, 38),
        base.rounded_slot_poly(24, 190, 14, 38),
        base.rounded_slot_poly(276, 38, 14, 38),
        base.rounded_slot_poly(276, 190, 14, 38),
        # Upright/front rail saddle slots. Electrical modules mount to their own compact trays/tabs.
        base.rounded_slot_poly(132, 42, 18, 40),
        base.rounded_slot_poly(168, 42, 18, 40),
        base.rounded_slot_poly(132, 180, 18, 40),
        base.rounded_slot_poly(168, 180, 18, 40),
    ]
    cut_circles = [
        # Drain/cable clip holes.
        base.Circle(56, 242, 3.25),
        base.Circle(106, 242, 3.25),
        base.Circle(156, 242, 3.25),
        base.Circle(206, 242, 3.25),
        base.Circle(256, 242, 3.25),
    ]
    notes = [
        "Compact battery stand top tray: 315 x 265 x 3.0 mm mild steel tray/deck around the 275 x 230 mm battery datum with service allowance.",
        "Electrical equipment uses its own compact carriers: folded relay tray, open MIDI plate/subplate, and independent cutoff tab. Do not use tray skin as a large backplane.",
        "Final battery footprint, terminal side, clamp path, bonnet clearance, front-cavity clearance, and LHD steering-side clearance are vehicle-measurement holds.",
        "Add an acid-resistant battery mat after paint; do not allow battery case or terminals to touch live studs or sharp steel edges.",
    ]
    return base.Drawing(
        "battery_stand_compact_top_tray_rev_b",
        315,
        265,
        cut_polys,
        [],
        cut_circles,
        [],
        notes,
    )


def battery_hold_down_crossbar() -> base.Drawing:
    cut_polys = [
        base.Poly([(0, 0), (315, 0), (315, 38), (0, 38)]),
        base.rounded_slot_poly(18, 11, 42, 16),
        base.rounded_slot_poly(255, 11, 42, 16),
    ]
    notes = [
        "Compact battery hold-down crossbar: 315 x 38 x 3.0 mm mild steel or stainless. Length and slots are template values until the actual battery is measured.",
        "Use J-bolts or vertical rods that cannot touch battery terminals. Add insulated caps where needed.",
        "Do not over-tighten against a plastic battery case; retain the battery without distorting it.",
    ]
    return base.Drawing(
        "battery_stand_compact_hold_down_crossbar_rev_b",
        315,
        38,
        cut_polys,
        [],
        [],
        [],
        notes,
    )


def iso_point(x: float, y: float, z: float) -> tuple[float, float]:
    return 330 + (x - y) * 0.72, 110 + (x + y) * 0.33 - z * 1.05


def point_attr(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def iso_polygon(points: list[tuple[float, float, float]], css_class: str) -> str:
    return f'<polygon class="{css_class}" points="{point_attr([iso_point(*point) for point in points])}" />'


def iso_prism(
    x: float,
    y: float,
    w: float,
    d: float,
    z: float,
    h: float,
    top_class: str,
    right_class: str,
    front_class: str,
) -> list[str]:
    return [
        iso_polygon([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + h), (x + w, y, z + h)], right_class),
        iso_polygon([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + h), (x, y + d, z + h)], front_class),
        iso_polygon([(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)], top_class),
    ]


def iso_polyline(points: list[tuple[float, float, float]], css_class: str) -> str:
    return f'<polyline class="{css_class}" points="{point_attr([iso_point(*point) for point in points])}" />'


def write_static_3d_visualisation() -> None:
    elements: list[str] = []
    elements.append('<rect class="background" width="920" height="620" />')
    elements.append(iso_polygon([(-40, 385, -22), (610, 385, -22), (650, 438, -22), (0, 438, -22)], "shadow"))
    # Compact one-pickup stand with a reduced tray and measured rail/tab carriers.
    elements.extend(iso_prism(188, 158, 220, 140, -42, 18, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(258, 190, 82, 70, -24, 96, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(220, 184, 24, 104, -24, 112, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(356, 184, 24, 104, -24, 112, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(82, 70, 315, 265, 72, 10, "plate-top", "plate-side", "plate-front"))
    elements.extend(iso_prism(102, 88, 275, 230, 82, 185, "battery-top", "battery-side", "battery-front"))
    elements.extend(iso_prism(94, 100, 315, 18, 274, 8, "hold-top", "hold-side", "hold-front"))
    elements.extend(iso_prism(94, 296, 315, 18, 274, 8, "hold-top", "hold-side", "hold-front"))
    elements.extend(iso_prism(64, 32, 340, 8, 112, 90, "plate-top", "plate-side", "plate-front"))
    # Known fabricated component bases now sit on their own compact trays/tabs.
    elements.extend(iso_prism(74, 38, 320, 8, 132, 220, "relay-top", "relay-side", "relay-front"))
    elements.extend(iso_prism(104, 44, 260, 38, 170, 125, "relay-fuse-top", "relay-fuse-side", "relay-fuse-front"))
    elements.extend(iso_prism(420, 120, 8, 150, 112, 190, "midi-plate-top", "midi-plate-side", "midi-plate-front"))
    elements.extend(iso_prism(428, 138, 8, 85, 132, 140, "midi-board-top", "midi-board-side", "midi-board-front"))
    for idx in range(5):
        elements.extend(iso_prism(436, 144 + idx * 16, 16, 10, 146, 34, "fuse-top", "fuse-side", "fuse-front"))
    elements.extend(iso_prism(420, 40, 8, 110, 236, 170, "guard-top", "guard-side", "guard-front"))
    cx, cy = iso_point(430, 92, 338)
    elements.append(f'<ellipse class="cutoff-body" cx="{cx:.1f}" cy="{cy:.1f}" rx="30" ry="18" />')
    elements.append(f'<ellipse class="cutoff-knob" cx="{cx:.1f}" cy="{cy - 11:.1f}" rx="20" ry="12" />')
    for point in [(430, 76, 280), (430, 114, 280)]:
        x, y = iso_point(*point)
        elements.append(f'<circle class="cutoff-terminal" cx="{x:.1f}" cy="{y:.1f}" r="5" />')
    elements.append(iso_polyline([(290, 108, 280), (430, 92, 350), (430, 76, 280)], "positive-cable"))
    elements.append(iso_polyline([(430, 92, 350), (432, 160, 245), (438, 164, 170)], "relay-feed"))
    elements.append(iso_polyline([(432, 160, 245), (330, 78, 230), (170, 44, 190)], "branch-cable"))
    for point in [(198, 168, -18), (398, 168, -18), (198, 286, -18), (398, 286, -18)]:
        x, y = iso_point(*point)
        elements.append(f'<circle class="slot-marker" cx="{x:.1f}" cy="{y:.1f}" r="4" />')

    labels = [
        ("Single chassis pickup", 126, 504),
        ("Single upright bridge", 166, 365),
        ("Compact battery tray / stand", 322, 434),
        ("Battery supported on stand", 252, 214),
        ("Folded relay tray 320 x 220", 548, 210),
        ("Cutoff tab 170 x 110", 622, 306),
        ("MIDI open plate 190 x 150", 610, 382),
    ]
    for text, x, y in labels:
        elements.append(f'<text class="label" x="{x}" y="{y}">{text}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="620" viewBox="0 0 920 620" role="img" aria-labelledby="title desc">
  <title id="title">Battery stand power carrier Rev B compact 3D assembly visualisation</title>
  <desc id="desc">Isometric visualisation of a compact steel battery stand on one chassis pickup, carrying the battery on a reduced tray with the folded Relay Rev C tray, MIDI Rev C open plate, and cutoff tab on separate compact rail/tab pickups.</desc>
  <style>
    .background {{ fill: #f6f7f8; }}
    .shadow {{ fill: #d9dde2; opacity: 0.55; }}
    .plate-top {{ fill: #cfd6dc; stroke: #4f5962; stroke-width: 1.4; }}
    .plate-side {{ fill: #9ca8b2; stroke: #4f5962; stroke-width: 1.2; }}
    .plate-front {{ fill: #b5bec7; stroke: #4f5962; stroke-width: 1.2; }}
    .tab-top {{ fill: #7f8992; stroke: #343b42; stroke-width: 1.2; }}
    .tab-side {{ fill: #515b64; stroke: #343b42; stroke-width: 1.1; }}
    .tab-front {{ fill: #66717a; stroke: #343b42; stroke-width: 1.1; }}
    .battery-top {{ fill: #2f3942; stroke: #111820; stroke-width: 1.4; }}
    .battery-side {{ fill: #1d252c; stroke: #111820; stroke-width: 1.2; }}
    .battery-front {{ fill: #3d4852; stroke: #111820; stroke-width: 1.2; }}
    .hold-top {{ fill: #cfd6dc; stroke: #4f5962; stroke-width: 1.1; }}
    .hold-side {{ fill: #98a4ae; stroke: #4f5962; stroke-width: 0.9; }}
    .hold-front {{ fill: #b5bec7; stroke: #4f5962; stroke-width: 0.9; }}
    .relay-top {{ fill: #202a33; stroke: #12171c; stroke-width: 1.4; }}
    .relay-side {{ fill: #151c22; stroke: #12171c; stroke-width: 1.2; }}
    .relay-front {{ fill: #26323c; stroke: #12171c; stroke-width: 1.2; }}
    .relay-fuse-top {{ fill: #384856; stroke: #1f2830; stroke-width: 0.8; }}
    .relay-fuse-side {{ fill: #26323d; stroke: #1f2830; stroke-width: 0.6; }}
    .relay-fuse-front {{ fill: #465867; stroke: #1f2830; stroke-width: 0.6; }}
    .relay-fuse-top {{ fill: #384856; stroke: #1f2830; stroke-width: 0.8; }}
    .relay-fuse-side {{ fill: #26323d; stroke: #1f2830; stroke-width: 0.6; }}
    .relay-fuse-front {{ fill: #465867; stroke: #1f2830; stroke-width: 0.6; }}
    .midi-plate-top {{ fill: #aeb8c1; stroke: #4f5962; stroke-width: 1.2; }}
    .midi-plate-side {{ fill: #818d97; stroke: #4f5962; stroke-width: 1; }}
    .midi-plate-front {{ fill: #98a4ae; stroke: #4f5962; stroke-width: 1; }}
    .midi-board-top {{ fill: #1f2930; stroke: #14191d; stroke-width: 1; }}
    .midi-board-side {{ fill: #161d22; stroke: #14191d; stroke-width: 0.9; }}
    .midi-board-front {{ fill: #2b363e; stroke: #14191d; stroke-width: 0.9; }}
    .fuse-top {{ fill: #b7302a; stroke: #6e1714; stroke-width: 0.8; }}
    .fuse-side {{ fill: #84201b; stroke: #6e1714; stroke-width: 0.7; }}
    .fuse-front {{ fill: #d14a43; stroke: #6e1714; stroke-width: 0.7; }}
    .guard-top {{ fill: #d9b65d; stroke: #806626; stroke-width: 1; opacity: 0.92; }}
    .guard-side {{ fill: #a98536; stroke: #806626; stroke-width: 0.9; opacity: 0.92; }}
    .guard-front {{ fill: #c99f45; stroke: #806626; stroke-width: 0.9; opacity: 0.92; }}
    .cutoff-body {{ fill: #111820; stroke: #05080a; stroke-width: 2; }}
    .cutoff-knob {{ fill: #d12828; stroke: #871313; stroke-width: 2; }}
    .cutoff-terminal {{ fill: #c4a35a; stroke: #6f5d2f; stroke-width: 1.1; }}
    .positive-cable {{ fill: none; stroke: #c41d1d; stroke-width: 8; stroke-linejoin: round; stroke-linecap: round; }}
    .relay-feed {{ fill: none; stroke: #a51515; stroke-width: 6; stroke-linejoin: round; stroke-linecap: round; }}
    .branch-cable {{ fill: none; stroke: #242b30; stroke-width: 6; stroke-linejoin: round; stroke-linecap: round; }}
    .slot-marker {{ fill: #eef3f7; stroke: #4f5962; stroke-width: 1.2; }}
    .label {{ font: 600 18px Arial, sans-serif; fill: #24313a; }}
  </style>
  {''.join(elements)}
</svg>
"""
    (OUT_DIR / VISUAL_SVG_NAME).write_text(svg, encoding="utf-8")


def write_interactive_3d_visualisation() -> None:
    html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>J40 Battery Stand Power Carrier Rev B Compact - 3D Visualisation</title>
  <link rel="icon" href="data:,">
  <style>
    :root {
      color-scheme: light;
      font-family: Arial, Helvetica, sans-serif;
      background: #f5f6f7;
      color: #1d252c;
    }
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      grid-template-rows: auto 1fr;
    }
    body.embed {
      grid-template-rows: 1fr;
    }
    header {
      padding: 16px 22px 10px;
      background: #ffffff;
      border-bottom: 1px solid #d8dde2;
    }
    h1 {
      margin: 0;
      font-size: clamp(20px, 3vw, 30px);
      letter-spacing: 0;
    }
    .meta {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }
    .chip {
      border: 1px solid #c8d0d8;
      border-radius: 999px;
      padding: 5px 9px;
      background: #f8fafb;
      font-size: 13px;
    }
    main {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 300px;
      min-height: 0;
    }
    #viewport {
      position: relative;
      min-height: 560px;
      overflow: hidden;
    }
    canvas {
      display: block;
      width: 100%;
      height: 100%;
    }
    aside {
      border-left: 1px solid #d8dde2;
      background: #ffffff;
      padding: 18px;
    }
    h2 {
      margin: 0 0 12px;
      font-size: 18px;
      letter-spacing: 0;
    }
    dl {
      margin: 0;
      display: grid;
      gap: 12px;
    }
    dt {
      font-weight: 700;
    }
    dd {
      margin: 3px 0 0;
      color: #54616c;
      font-size: 14px;
      line-height: 1.45;
    }
    #fallback {
      position: absolute;
      inset: 0;
      display: grid;
      place-items: center;
      padding: 20px;
      background: #f5f6f7;
    }
    #fallback img {
      width: min(94vw, 920px);
      max-height: 82vh;
      object-fit: contain;
    }
    body.is-three-ready #fallback {
      display: none;
    }
    body.embed header,
    body.embed aside {
      display: none;
    }
    body.embed main {
      grid-template-columns: 1fr;
      min-height: 100vh;
    }
    body.embed #viewport {
      min-height: 100vh;
    }
    @media (max-width: 820px) {
      main {
        grid-template-columns: 1fr;
      }
      #viewport {
        min-height: 430px;
      }
      aside {
        border-left: 0;
        border-top: 1px solid #d8dde2;
      }
    }
  </style>
  <script type="importmap">
    {
      "imports": {
        "three": "https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js",
        "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.164.1/examples/jsm/"
      }
    }
  </script>
</head>
<body>
  <script>
    if (new URLSearchParams(window.location.search).has("embed")) {
      document.body.classList.add("embed");
    }
  </script>
  <header>
    <h1>Battery Stand Power Carrier Rev B Compact Layout</h1>
    <div class="meta">
      <span class="chip">Steel chassis-bolted stand</span>
      <span class="chip">Compact battery tray</span>
      <span class="chip">Folded Relay Rev C tray</span>
      <span class="chip">MIDI open plate</span>
      <span class="chip">Compact cutoff tab</span>
      <span class="chip">Cavity-map gate</span>
    </div>
  </header>
  <main>
    <section id="viewport" aria-label="Interactive 3D battery power carrier visualisation">
      <div id="fallback">
        <img src="./battery_power_carrier_mount_rev_a_3d_visualisation.svg" alt="Isometric battery power carrier visualisation">
      </div>
    </section>
    <aside>
      <h2>Assembly Read</h2>
      <dl>
        <div>
          <dt>Load path</dt>
          <dd>The compact battery tray mounts from one chassis pickup location through a compact upright bridge.</dd>
        </div>
        <div>
          <dt>Power path</dt>
          <dd>The folded Relay Rev C tray, MIDI Rev C open plate/subplate, and cutoff tab mount on measured compact rails/tabs.</dd>
        </div>
        <div>
          <dt>Service intent</dt>
          <dd>The stand is removable from the chassis after coated pickup points are finished; final holes stay gated by battery, bonnet, LHD steering-side, radiator, and cable-sweep checks.</dd>
        </div>
      </dl>
    </aside>
  </main>
  <script type="module">
    import * as THREE from "three";
    import { OrbitControls } from "three/addons/controls/OrbitControls.js";

    const mount = document.getElementById("viewport");
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f6f7);

    const camera = new THREE.PerspectiveCamera(38, 1, 1, 2400);
    camera.position.set(470, 500, 640);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, preserveDrawingBuffer: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    mount.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(20, 125, 70);
    controls.enableDamping = true;
    controls.minDistance = 420;
    controls.maxDistance = 1100;
    controls.maxPolarAngle = Math.PI * 0.48;

    const root = new THREE.Group();
    scene.add(root);

    const materials = {
      plate: new THREE.MeshStandardMaterial({ color: 0xbfc8d1, metalness: 0.35, roughness: 0.38 }),
      plateEdge: new THREE.MeshStandardMaterial({ color: 0x8e9aa5, metalness: 0.25, roughness: 0.45 }),
      steel: new THREE.MeshStandardMaterial({ color: 0x59636c, metalness: 0.45, roughness: 0.5 }),
      relay: new THREE.MeshStandardMaterial({ color: 0x202a33, roughness: 0.62 }),
      relayDetail: new THREE.MeshStandardMaterial({ color: 0x41515f, roughness: 0.58 }),
      midiBoard: new THREE.MeshStandardMaterial({ color: 0x1f2930, roughness: 0.7 }),
      fuseRed: new THREE.MeshStandardMaterial({ color: 0xb72e2a, roughness: 0.42 }),
      battery: new THREE.MeshStandardMaterial({ color: 0x2f3942, roughness: 0.62 }),
      brass: new THREE.MeshStandardMaterial({ color: 0xc4a35a, metalness: 0.4, roughness: 0.36 }),
      cutoff: new THREE.MeshStandardMaterial({ color: 0xd12828, roughness: 0.35 }),
      black: new THREE.MeshStandardMaterial({ color: 0x111820, roughness: 0.55 }),
      cableRed: new THREE.MeshStandardMaterial({ color: 0xc41d1d, roughness: 0.45 }),
      cableBlack: new THREE.MeshStandardMaterial({ color: 0x20262b, roughness: 0.5 }),
    };

    function box(name, x, y, z, w, h, d, material) {
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
      mesh.name = name;
      mesh.position.set(x, y, z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      root.add(mesh);
      return mesh;
    }

    function cyl(name, x, y, z, radius, depth, material, rotationX = Math.PI / 2) {
      const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, depth, 48), material);
      mesh.name = name;
      mesh.rotation.x = rotationX;
      mesh.position.set(x, y, z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      root.add(mesh);
      return mesh;
    }

    function cable(name, points, radius, material) {
      const curve = new THREE.CatmullRomCurve3(points.map((p) => new THREE.Vector3(p[0], p[1], p[2])));
      const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, 48, radius, 14, false), material);
      mesh.name = name;
      mesh.castShadow = true;
      root.add(mesh);
      return mesh;
    }

    function singleChassisPickup() {
      box("Compact single chassis pickup base plate 220 x 140", 0, -54, 70, 220, 18, 140, materials.steel);
      box("Compact single chassis upright pedestal", 0, 12, 70, 86, 118, 100, materials.steel);
      box("Compact tray saddle from single chassis pickup", 0, 58, 70, 200, 22, 170, materials.steel);
      box("Left compact upright side plate 110 x 220", -72, 18, -8, 18, 140, 110, materials.steel);
      box("Right compact upright side plate 110 x 220", -72, 18, 148, 18, 140, 110, materials.steel);
      for (const z of [10, 130]) {
        cyl("Single chassis pickup bolt", -86, -54, z, 5, 24, materials.brass, Math.PI / 2);
        cyl("Single chassis pickup bolt", 86, -54, z, 5, 24, materials.brass, Math.PI / 2);
      }
    }
    function knownRelayCarrierBase(x, y, z) {
      box("Folded Relay Rev C carrier tray face 320 x 220", x, y, z, 320, 220, 8, materials.plateEdge);
      box("Folded Relay Rev C left return 20 mm", x - 164, y, z - 12, 8, 220, 28, materials.plateEdge);
      box("Folded Relay Rev C right return 20 mm", x + 164, y, z - 12, 8, 220, 28, materials.plateEdge);
      box("Folded Relay Rev C lower return 20 mm", x, y - 112, z - 12, 320, 8, 28, materials.plateEdge);
      box("Folded Relay Rev C upper return 15 mm", x, y + 112, z - 10, 320, 8, 22, materials.plateEdge);
      box("Relay/fuse assembly on fabricated base", x, y, z - 28, 285, 155, 48, materials.relay);
      box("Relay carrier lower loom relief", x, y - 82, z - 58, 120, 24, 18, materials.black);
      for (const sx of [-135, 0, 135]) {
        cyl("Relay carrier standoff screw", x + sx, y + 90, z - 8, 4, 10, materials.brass, 0);
        cyl("Relay carrier standoff screw", x + sx, y - 90, z - 8, 4, 10, materials.brass, 0);
      }
    }
    function knownMidiBase(x, y, z) {
      box("Known MIDI Rev C mount plate 190 x 150", x, y, z, 190, 150, 8, materials.plateEdge);
      box("Known MIDI insulated subplate 140 x 85", x, y, z - 14, 140, 85, 12, materials.midiBoard);
      for (let idx = 0; idx < 5; idx += 1) {
        const fx = x - 54 + idx * 27;
        box("MIDI holder on known base", fx, y, z - 32, 20, 62, 24, materials.fuseRed);
        cyl("MIDI holder stud", fx, y - 24, z - 46, 4, 8, materials.brass, 0);
        cyl("MIDI holder stud", fx, y + 24, z - 46, 4, 8, materials.brass, 0);
      }
    }
    function cutoffSwitch(name, x, y, z) {
      box(`${name} compact cutoff tab/guard 170 x 110`, x, y, z, 170, 110, 8, materials.brass);
      cyl(`${name} black switch body`, x, y, z - 28, 34, 32, materials.black, Math.PI / 2);
      cyl(`${name} red rotary knob`, x, y, z - 64, 24, 18, materials.cutoff, Math.PI / 2);
      cyl(`${name} input terminal stud`, x - 38, y - 32, z - 44, 4, 22, materials.brass, 0);
      cyl(`${name} output terminal stud`, x + 38, y + 32, z - 44, 4, 22, materials.brass, 0);
      box(`${name} input lug`, x - 38, y - 42, z - 52, 18, 26, 6, materials.brass);
      box(`${name} output lug`, x + 38, y + 42, z - 52, 18, 26, 6, materials.brass);
    }

    singleChassisPickup();
    box("Compact battery stand top tray 315 x 265", -110, 68, 42, 315, 8, 265, materials.plate);
    box("Battery datum 275 x 230 x 190", -120, 167, 32, 275, 190, 230, materials.battery);
    cyl("Battery positive terminal", -24, 270, -34, 9, 14, materials.brass, 0);
    cyl("Battery negative terminal", -210, 270, 98, 9, 14, materials.brass, 0);
    box("Compact battery hold-down crossbar front", -120, 272, -92, 315, 8, 18, materials.plateEdge);
    box("Compact battery hold-down crossbar rear", -120, 272, 156, 315, 8, 18, materials.plateEdge);
    box("Compact front service rail 340 x 90", -100, 160, -108, 340, 90, 8, materials.plate);
    knownRelayCarrierBase(-100, 210, -116);
    knownMidiBase(150, 122, 172);
    cutoffSwitch("Master cutoff switch", 150, 260, -116);
    cable("Battery positive to cutoff", [[-24, 278, -34], [90, 292, -60], [150, 260, -80]], 7, materials.cableRed);
    cable("Cutoff to MIDI common", [[150, 260, -80], [150, 178, 70], [150, 122, 142]], 6, materials.cableRed);
    cable("Relay feed", [[150, 122, 142], [40, 180, 20], [-100, 210, -88]], 5, materials.cableRed);
    cable("Fused branch exit", [[150, 122, 138], [230, 102, 162], [270, 90, 172]], 5, materials.cableBlack);

    const ambient = new THREE.HemisphereLight(0xffffff, 0x98a1aa, 2.2);
    scene.add(ambient);
    const key = new THREE.DirectionalLight(0xffffff, 2.4);
    key.position.set(260, 420, 300);
    key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    scene.add(key);

    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(900, 680),
      new THREE.ShadowMaterial({ color: 0x000000, opacity: 0.12 })
    );
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -92;
    ground.receiveShadow = true;
    scene.add(ground);

    function resize() {
      const width = mount.clientWidth;
      const height = mount.clientHeight;
      renderer.setSize(width, height, false);
      camera.aspect = width / Math.max(1, height);
      camera.updateProjectionMatrix();
    }

    function animate() {
      controls.update();
      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    }

    resize();
    window.addEventListener("resize", resize);
    document.body.classList.add("is-three-ready");
    animate();
  </script>
</body>
</html>
"""
    (OUT_DIR / VISUAL_HTML_NAME).write_text(html, encoding="utf-8")


def write_assembled_static_3d_visualisation() -> None:
    elements: list[str] = []
    elements.append('<rect class="background" width="920" height="620" />')
    elements.append(iso_polygon([(-45, 388, -22), (620, 388, -22), (660, 440, -22), (0, 440, -22)], "shadow"))
    elements.extend(iso_prism(188, 158, 220, 140, -42, 18, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(258, 190, 82, 70, -24, 96, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(220, 184, 24, 104, -24, 112, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(356, 184, 24, 104, -24, 112, "tab-top", "tab-side", "tab-front"))
    elements.extend(iso_prism(82, 70, 315, 265, 72, 10, "plate-top", "plate-side", "plate-front"))
    elements.extend(iso_prism(102, 88, 275, 230, 82, 185, "battery-top", "battery-side", "battery-front"))
    elements.extend(iso_prism(94, 100, 315, 18, 274, 8, "hold-top", "hold-side", "hold-front"))
    elements.extend(iso_prism(94, 296, 315, 18, 274, 8, "hold-top", "hold-side", "hold-front"))
    elements.extend(iso_prism(64, 32, 340, 8, 112, 90, "plate-top", "plate-side", "plate-front"))
    elements.extend(iso_prism(74, 38, 320, 8, 132, 220, "relay-top", "relay-side", "relay-front"))
    elements.extend(iso_prism(104, 44, 260, 38, 170, 125, "relay-fuse-top", "relay-fuse-side", "relay-fuse-front"))
    elements.extend(iso_prism(420, 120, 8, 150, 112, 190, "midi-plate-top", "midi-plate-side", "midi-plate-front"))
    elements.extend(iso_prism(428, 138, 8, 85, 132, 140, "midi-board-top", "midi-board-side", "midi-board-front"))
    for idx in range(5):
        elements.extend(iso_prism(436, 144 + idx * 16, 16, 10, 146, 34, "fuse-top", "fuse-side", "fuse-front"))
    elements.extend(iso_prism(420, 40, 8, 110, 236, 170, "guard-top", "guard-side", "guard-front"))
    cx, cy = iso_point(430, 92, 338)
    elements.append(f'<ellipse class="cutoff-body" cx="{cx:.1f}" cy="{cy:.1f}" rx="30" ry="18" />')
    elements.append(f'<ellipse class="cutoff-knob" cx="{cx:.1f}" cy="{cy - 11:.1f}" rx="20" ry="12" />')
    for point in [(430, 76, 280), (430, 114, 280)]:
        x, y = iso_point(*point)
        elements.append(f'<circle class="cutoff-terminal" cx="{x:.1f}" cy="{y:.1f}" r="5" />')
    elements.append(iso_polyline([(290, 108, 280), (430, 92, 350), (430, 76, 280)], "positive-cable"))
    elements.append(iso_polyline([(430, 92, 350), (432, 160, 245), (438, 164, 170)], "relay-feed"))
    elements.append(iso_polyline([(432, 160, 245), (330, 78, 230), (170, 44, 190)], "branch-cable"))
    for point in [(198, 168, -18), (398, 168, -18), (198, 286, -18), (398, 286, -18)]:
        x, y = iso_point(*point)
        elements.append(f'<circle class="slot-marker" cx="{x:.1f}" cy="{y:.1f}" r="4" />')
    for text, x, y in (
        ("Attached compact battery stand assembly", 82, 84),
        ("Battery bolted down on compact tray", 212, 214),
        ("Single chassis pickup", 132, 508),
        ("Single upright bridge", 158, 364),
        ("Compact split holders mounted", 548, 282),
    ):
        elements.append(f'<text class="label" x="{x}" y="{y}">{text}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="620" viewBox="0 0 920 620" role="img" aria-labelledby="title desc">
  <title id="title">Battery stand power carrier Rev B compact assembled 3D visualisation</title>
  <desc id="desc">Attached assembly view of the compact steel battery stand with one chassis pickup, compact tray, hold-down crossbar, full-height battery, folded Relay Rev C tray, MIDI Rev C open plate, cutoff tab, and cable paths installed together.</desc>
  <style>
    .background {{ fill: #f6f7f8; }}
    .shadow {{ fill: #d9dde2; opacity: 0.55; }}
    .plate-top {{ fill: #cfd6dc; stroke: #4f5962; stroke-width: 1.4; }}
    .plate-side {{ fill: #9ca8b2; stroke: #4f5962; stroke-width: 1.2; }}
    .plate-front {{ fill: #b5bec7; stroke: #4f5962; stroke-width: 1.2; }}
    .tab-top {{ fill: #7f8992; stroke: #343b42; stroke-width: 1.2; }}
    .tab-side {{ fill: #515b64; stroke: #343b42; stroke-width: 1.1; }}
    .tab-front {{ fill: #66717a; stroke: #343b42; stroke-width: 1.1; }}
    .battery-top {{ fill: #2f3942; stroke: #111820; stroke-width: 1.4; }}
    .battery-side {{ fill: #1d252c; stroke: #111820; stroke-width: 1.2; }}
    .battery-front {{ fill: #3d4852; stroke: #111820; stroke-width: 1.2; }}
    .hold-top {{ fill: #cfd6dc; stroke: #4f5962; stroke-width: 1.1; }}
    .hold-side {{ fill: #98a4ae; stroke: #4f5962; stroke-width: 0.9; }}
    .hold-front {{ fill: #b5bec7; stroke: #4f5962; stroke-width: 0.9; }}
    .relay-top {{ fill: #202a33; stroke: #12171c; stroke-width: 1.4; }}
    .relay-side {{ fill: #151c22; stroke: #12171c; stroke-width: 1.2; }}
    .relay-front {{ fill: #26323c; stroke: #12171c; stroke-width: 1.2; }}
    .midi-plate-top {{ fill: #aeb8c1; stroke: #4f5962; stroke-width: 1.2; }}
    .midi-plate-side {{ fill: #818d97; stroke: #4f5962; stroke-width: 1; }}
    .midi-plate-front {{ fill: #98a4ae; stroke: #4f5962; stroke-width: 1; }}
    .midi-board-top {{ fill: #1f2930; stroke: #14191d; stroke-width: 1; }}
    .midi-board-side {{ fill: #161d22; stroke: #14191d; stroke-width: 0.9; }}
    .midi-board-front {{ fill: #2b363e; stroke: #14191d; stroke-width: 0.9; }}
    .fuse-top {{ fill: #b7302a; stroke: #6e1714; stroke-width: 0.8; }}
    .fuse-side {{ fill: #84201b; stroke: #6e1714; stroke-width: 0.7; }}
    .fuse-front {{ fill: #d14a43; stroke: #6e1714; stroke-width: 0.7; }}
    .guard-top {{ fill: #d9b65d; stroke: #806626; stroke-width: 1; opacity: 0.92; }}
    .guard-side {{ fill: #a98536; stroke: #806626; stroke-width: 0.9; opacity: 0.92; }}
    .guard-front {{ fill: #c99f45; stroke: #806626; stroke-width: 0.9; opacity: 0.92; }}
    .cutoff-body {{ fill: #111820; stroke: #05080a; stroke-width: 2; }}
    .cutoff-knob {{ fill: #d12828; stroke: #871313; stroke-width: 2; }}
    .cutoff-terminal {{ fill: #c4a35a; stroke: #6f5d2f; stroke-width: 1.1; }}
    .positive-cable {{ fill: none; stroke: #c41d1d; stroke-width: 8; stroke-linejoin: round; stroke-linecap: round; }}
    .relay-feed {{ fill: none; stroke: #a51515; stroke-width: 6; stroke-linejoin: round; stroke-linecap: round; }}
    .branch-cable {{ fill: none; stroke: #242b30; stroke-width: 6; stroke-linejoin: round; stroke-linecap: round; }}
    .slot-marker {{ fill: #eef3f7; stroke: #4f5962; stroke-width: 1.2; }}
    .label {{ font: 600 18px Arial, sans-serif; fill: #24313a; }}
  </style>
  {''.join(elements)}
</svg>
"""
    (OUT_DIR / ASSEMBLED_VISUAL_SVG_NAME).write_text(svg, encoding="utf-8")


def write_assembled_interactive_3d_visualisation() -> None:
    html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>J40 Battery Stand Power Carrier Rev B Compact - Assembled 3D Visualisation</title>
  <link rel="icon" href="data:,">
  <style>
    :root { color-scheme: light; font-family: Arial, Helvetica, sans-serif; background: #f5f6f7; color: #1d252c; }
    body { margin: 0; min-height: 100vh; display: grid; grid-template-rows: auto 1fr; }
    body.embed { grid-template-rows: 1fr; }
    header { padding: 16px 22px 10px; background: #ffffff; border-bottom: 1px solid #d8dde2; }
    h1 { margin: 0; font-size: clamp(20px, 3vw, 30px); letter-spacing: 0; }
    .meta { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
    .chip { border: 1px solid #c8d0d8; border-radius: 999px; padding: 5px 9px; background: #f8fafb; font-size: 13px; }
    main { display: grid; grid-template-columns: minmax(0, 1fr) 300px; min-height: 0; }
    #viewport { position: relative; min-height: 560px; overflow: hidden; }
    canvas { display: block; width: 100%; height: 100%; }
    aside { border-left: 1px solid #d8dde2; background: #ffffff; padding: 18px; }
    h2 { margin: 0 0 12px; font-size: 18px; letter-spacing: 0; }
    dl { margin: 0; display: grid; gap: 12px; }
    dt { font-weight: 700; }
    dd { margin: 3px 0 0; color: #54616c; font-size: 14px; line-height: 1.45; }
    #fallback { position: absolute; inset: 0; display: grid; place-items: center; padding: 20px; background: #f5f6f7; }
    #fallback img { width: min(94vw, 920px); max-height: 82vh; object-fit: contain; }
    body.is-three-ready #fallback { display: none; }
    body.embed header,
    body.embed aside { display: none; }
    body.embed main { grid-template-columns: 1fr; min-height: 100vh; }
    body.embed #viewport { min-height: 100vh; }
    @media (max-width: 820px) { main { grid-template-columns: 1fr; } #viewport { min-height: 430px; } aside { border-left: 0; border-top: 1px solid #d8dde2; } }
  </style>
  <script type="importmap">
    {"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.164.1/examples/jsm/"}}
  </script>
</head>
<body>
  <script>
    if (new URLSearchParams(window.location.search).has("embed")) {
      document.body.classList.add("embed");
    }
  </script>
  <header>
    <h1>Assembled Battery Stand Power Carrier Rev B Compact Layout</h1>
    <div class="meta">
      <span class="chip">Attached assembly</span>
      <span class="chip">Single chassis pickup</span>
      <span class="chip">Compact battery tray</span>
      <span class="chip">Folded relay tray</span>
      <span class="chip">Separate MIDI/cutoff tabs</span>
      <span class="chip">Cavity-map hold</span>
    </div>
  </header>
  <main>
    <section id="viewport" aria-label="Interactive assembled 3D battery stand visualisation">
      <div id="fallback">
        <img src="./battery_power_carrier_mount_rev_a_assembled_3d_visualisation.svg" alt="Assembled battery stand power carrier visualisation">
      </div>
    </section>
    <aside>
      <h2>Assembly Read</h2>
      <dl>
        <div><dt>Load path</dt><dd>One chassis pickup mount and upright bridge carry the compact steel battery tray and service rail/tab pickups.</dd></div>
        <div><dt>Integrated equipment</dt><dd>The full-height battery, folded Relay Rev C tray, MIDI Rev C open plate, and cutoff tab are shown attached as a compact split layout.</dd></div>
        <div><dt>Release hold</dt><dd>Final hole centres, compact holder positions, and cable paths still need battery-installed LHD mock-up photos before cutting final metal.</dd></div>
      </dl>
    </aside>
  </main>
  <script type="module">
    import * as THREE from "three";
    import { OrbitControls } from "three/addons/controls/OrbitControls.js";

    const mount = document.getElementById("viewport");
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f6f7);
    const camera = new THREE.PerspectiveCamera(38, 1, 1, 2400);
    camera.position.set(470, 500, 640);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, preserveDrawingBuffer: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    mount.appendChild(renderer.domElement);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(20, 125, 70);
    controls.enableDamping = true;
    controls.minDistance = 420;
    controls.maxDistance = 1100;
    controls.maxPolarAngle = Math.PI * 0.5;
    const root = new THREE.Group();
    scene.add(root);
    const materials = {
      plate: new THREE.MeshStandardMaterial({ color: 0xbfc8d1, metalness: 0.35, roughness: 0.38 }),
      plateEdge: new THREE.MeshStandardMaterial({ color: 0x8e9aa5, metalness: 0.25, roughness: 0.45 }),
      steel: new THREE.MeshStandardMaterial({ color: 0x59636c, metalness: 0.45, roughness: 0.5 }),
      relay: new THREE.MeshStandardMaterial({ color: 0x202a33, roughness: 0.62 }),
      relayDetail: new THREE.MeshStandardMaterial({ color: 0x41515f, roughness: 0.58 }),
      midiBoard: new THREE.MeshStandardMaterial({ color: 0x1f2930, roughness: 0.7 }),
      fuseRed: new THREE.MeshStandardMaterial({ color: 0xb72e2a, roughness: 0.42 }),
      battery: new THREE.MeshStandardMaterial({ color: 0x2f3942, roughness: 0.62 }),
      brass: new THREE.MeshStandardMaterial({ color: 0xc4a35a, metalness: 0.4, roughness: 0.36 }),
      cutoff: new THREE.MeshStandardMaterial({ color: 0xd12828, roughness: 0.35 }),
      black: new THREE.MeshStandardMaterial({ color: 0x111820, roughness: 0.55 }),
      cableRed: new THREE.MeshStandardMaterial({ color: 0xc41d1d, roughness: 0.45 }),
      cableBlack: new THREE.MeshStandardMaterial({ color: 0x20262b, roughness: 0.5 }),
    };
    function box(name, x, y, z, w, h, d, material) {
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
      mesh.name = name;
      mesh.position.set(x, y, z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      root.add(mesh);
      return mesh;
    }
    function cyl(name, x, y, z, radius, depth, material, rotationX = Math.PI / 2) {
      const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, depth, 48), material);
      mesh.name = name;
      mesh.rotation.x = rotationX;
      mesh.position.set(x, y, z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      root.add(mesh);
      return mesh;
    }
    function cable(name, points, radius, material) {
      const curve = new THREE.CatmullRomCurve3(points.map((p) => new THREE.Vector3(p[0], p[1], p[2])));
      const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, 48, radius, 14, false), material);
      mesh.name = name;
      mesh.castShadow = true;
      root.add(mesh);
      return mesh;
    }
    function singleChassisPickup() {
      box("Assembled compact single chassis pickup base plate 220 x 140", 0, -54, 70, 220, 18, 140, materials.steel);
      box("Assembled compact single chassis upright pedestal", 0, 12, 70, 86, 118, 100, materials.steel);
      box("Assembled compact tray saddle from single chassis pickup", 0, 58, 70, 200, 22, 170, materials.steel);
      box("Assembled left compact upright side plate 110 x 220", -72, 18, -8, 18, 140, 110, materials.steel);
      box("Assembled right compact upright side plate 110 x 220", -72, 18, 148, 18, 140, 110, materials.steel);
      for (const z of [10, 130]) {
        cyl("Single chassis pickup bolt", -86, -54, z, 5, 24, materials.brass, Math.PI / 2);
        cyl("Single chassis pickup bolt", 86, -54, z, 5, 24, materials.brass, Math.PI / 2);
      }
    }
    function knownRelayCarrierBase(x, y, z) {
      box("Folded Relay Rev C carrier tray face 320 x 220", x, y, z, 320, 220, 8, materials.plateEdge);
      box("Folded Relay Rev C left return 20 mm", x - 164, y, z - 12, 8, 220, 28, materials.plateEdge);
      box("Folded Relay Rev C right return 20 mm", x + 164, y, z - 12, 8, 220, 28, materials.plateEdge);
      box("Folded Relay Rev C lower return 20 mm", x, y - 112, z - 12, 320, 8, 28, materials.plateEdge);
      box("Folded Relay Rev C upper return 15 mm", x, y + 112, z - 10, 320, 8, 22, materials.plateEdge);
      box("Relay/fuse assembly on fabricated base", x, y, z - 28, 285, 155, 48, materials.relay);
      box("Relay carrier lower loom relief", x, y - 82, z - 58, 120, 24, 18, materials.black);
      for (const sx of [-135, 0, 135]) {
        cyl("Relay carrier standoff screw", x + sx, y + 90, z - 8, 4, 10, materials.brass, 0);
        cyl("Relay carrier standoff screw", x + sx, y - 90, z - 8, 4, 10, materials.brass, 0);
      }
    }
    function knownMidiBase(x, y, z) {
      box("Known MIDI Rev C mount plate 190 x 150", x, y, z, 190, 150, 8, materials.plateEdge);
      box("Known MIDI insulated subplate 140 x 85", x, y, z - 14, 140, 85, 12, materials.midiBoard);
      for (let idx = 0; idx < 5; idx += 1) {
        const fx = x - 54 + idx * 27;
        box("MIDI holder on known base", fx, y, z - 32, 20, 62, 24, materials.fuseRed);
        cyl("MIDI holder stud", fx, y - 24, z - 46, 4, 8, materials.brass, 0);
        cyl("MIDI holder stud", fx, y + 24, z - 46, 4, 8, materials.brass, 0);
      }
    }
    function cutoffSwitch(name, x, y, z) {
      box(`${name} compact cutoff tab/guard 170 x 110`, x, y, z, 170, 110, 8, materials.brass);
      cyl(`${name} black switch body`, x, y, z - 28, 34, 32, materials.black, Math.PI / 2);
      cyl(`${name} red rotary knob`, x, y, z - 64, 24, 18, materials.cutoff, Math.PI / 2);
      cyl(`${name} input terminal stud`, x - 38, y - 32, z - 44, 4, 22, materials.brass, 0);
      cyl(`${name} output terminal stud`, x + 38, y + 32, z - 44, 4, 22, materials.brass, 0);
      box(`${name} input lug`, x - 38, y - 42, z - 52, 18, 26, 6, materials.brass);
      box(`${name} output lug`, x + 38, y + 42, z - 52, 18, 26, 6, materials.brass);
    }

    singleChassisPickup();
    box("Assembled compact battery stand top tray 315 x 265", -110, 68, 42, 315, 8, 265, materials.plate);
    box("Full-height battery attached on compact stand", -120, 167, 32, 275, 190, 230, materials.battery);
    cyl("Battery positive terminal", -24, 270, -34, 9, 14, materials.brass, 0);
    cyl("Battery negative terminal", -210, 270, 98, 9, 14, materials.brass, 0);
    box("Compact battery hold-down crossbar front", -120, 272, -92, 315, 8, 18, materials.plateEdge);
    box("Compact battery hold-down crossbar rear", -120, 272, 156, 315, 8, 18, materials.plateEdge);
    for (const x of [-250, 10]) {
      cyl("Front hold-down rod to tray", x, 172, -88, 4, 196, materials.brass, 0);
      cyl("Rear hold-down rod to tray", x, 172, 152, 4, 196, materials.brass, 0);
    }
    box("Compact front service rail 340 x 90", -100, 160, -108, 340, 90, 8, materials.plate);
    knownRelayCarrierBase(-100, 210, -116);
    knownMidiBase(150, 122, 172);
    cutoffSwitch("Master cutoff switch", 150, 260, -116);
    cable("Battery positive to cutoff", [[-24, 278, -34], [90, 292, -60], [150, 260, -80]], 7, materials.cableRed);
    cable("Cutoff to MIDI common", [[150, 260, -80], [150, 178, 70], [150, 122, 142]], 6, materials.cableRed);
    cable("Relay feed", [[150, 122, 142], [40, 180, 20], [-100, 210, -88]], 5, materials.cableRed);
    cable("Fused branch exit", [[150, 122, 138], [230, 102, 162], [270, 90, 172]], 5, materials.cableBlack);

    scene.add(new THREE.HemisphereLight(0xffffff, 0x98a1aa, 2.2));
    const key = new THREE.DirectionalLight(0xffffff, 2.4);
    key.position.set(260, 420, 300);
    key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    scene.add(key);
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(900, 680), new THREE.ShadowMaterial({ color: 0x000000, opacity: 0.12 }));
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -92;
    ground.receiveShadow = true;
    scene.add(ground);
    function resize() {
      const width = mount.clientWidth;
      const height = mount.clientHeight;
      renderer.setSize(width, height, false);
      camera.aspect = width / Math.max(1, height);
      camera.updateProjectionMatrix();
    }
    function animate() {
      controls.update();
      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    }
    resize();
    window.addEventListener("resize", resize);
    document.body.classList.add("is-three-ready");
    animate();
  </script>
</body>
</html>
"""
    (OUT_DIR / ASSEMBLED_VISUAL_HTML_NAME).write_text(html, encoding="utf-8")


def write_readme() -> None:
    text = """# J40 Battery Stand Power Carrier Pack - Rev B Compact Update

This package changes the battery-side plan into a compact steel chassis-bolted stand that supports the battery first, then uses measured rail/tab pickups for the already-fabricated electrical holders. It deliberately supersedes the earlier large shared backplane.

## Design Intent

- Mount the battery stand from the one known chassis pickup location using a compact single pickup plate and upright bridge.
- Support the battery on a compact `315 x 265 mm` tray around the current `275 x 230 mm` battery datum.
- Treat Relay Rev C as the folded aluminium tray it already is: `320 x 220 mm` finished face, `360 x 255 mm` flat pattern, `20 mm` side/bottom returns, and `15 mm` top return.
- Treat MIDI Rev C as an open `190 x 150 mm` aluminium plate plus `140 x 85 mm` insulating subplate, not a folded tray.
- Put the cutoff switch on its own compact `170 x 110 mm` tab/guard so it can move to the most accessible front/top position.
- Default to split/stepped compact holders. Do not make a one-piece carrier unless the filled cavity map proves it.

## Parts In This Package

1. `battery_stand_compact_top_tray_rev_b` - 3 mm mild-steel compact battery tray/deck with clamp and cable-clip zones.
2. `battery_stand_compact_single_chassis_pickup_rev_b` - 4 mm mild-steel base plate for the one chassis pickup location.
3. `battery_stand_compact_single_mount_upright_rev_b` - 4 mm mild-steel upright bridge side plate; make a mirrored pair if the mock-up needs side-to-side stiffness.
4. `battery_stand_compact_hold_down_crossbar_rev_b` - compact battery hold-down crossbar template.
5. `battery_power_compact_front_service_rail_rev_b` - 3 mm mild-steel compact front service rail for a measured Relay/MIDI/cable pickup.
6. `battery_power_compact_cutoff_tab_rev_b` - compact cutoff switch tab/guard.

## 3D Visualisation

- `battery_power_carrier_mount_rev_a_3d_visualisation.svg` is the static compact fabrication-read view.
- `battery_power_carrier_mount_rev_a_3d_visualisation.html` is the interactive compact fabrication-read view.
- `battery_power_carrier_mount_rev_a_assembled_3d_visualisation.svg` is the static attached compact assembly view.
- `battery_power_carrier_mount_rev_a_assembled_3d_visualisation.html` is the interactive attached compact assembly view showing the single chassis pickup, upright bridge, compact tray, full-height battery, hold-down, folded Relay Rev C tray, MIDI Rev C open plate/subplate, cutoff tab/guard, and cable paths installed together.

## Package Relationship

- The relay hardware uses the known Relay Rev C folded tray (`320 x 220 mm` finished face; `360 x 255 mm` flat pattern). Its bent returns make a shallow tray, so the battery carrier must not duplicate that with a second large tray.
- The MIDI holder hardware uses `midi5_plate_mount_rev_c` (`190 x 150 mm`) and `midi5_holder_subplate_rev_c` (`140 x 85 mm`). This is an open plate/subplate assembly, so mount it on measured tabs/rails.
- The older `electrical_modules_rev_a` package includes bent/flanged aluminium tray/box concepts, but remains reference/fallback only.
- The cutoff pilot hole must be opened only after the actual battery master switch panel-hole size, body depth, terminal-stud spacing, and cable-lug sweep are measured.

## Compact Packaging Hold

- The latest battery-bay photos show no obvious full-size electrical mounting face beside the battery. The previous large sideways carrier is not the active design.
- Before cutting final steel, make cardboard cards for the compact tray (`315 x 265 mm`), Relay Rev C folded tray (`320 x 220 mm` plus return/depth blocks), MIDI Rev C plate (`190 x 150 mm` plus subplate/depth), cutoff tab (`170 x 110 mm`), cable lugs, and battery case.
- Test the front/radiator-side space first. Use inboard/lower/outboard space only after steering, hose, heat, splash, bonnet, and battery-service clearances are proven.
- Reject any placement that enters the steering shaft/box/service sweep, hydraulic line path, alternator service space, bonnet clearance, radiator/fan envelope, or safe battery terminal service area.

## Battery-Cavity Mapping Plan

Use the battery as the fixed exclusion block before placing any relays, MIDI fuses, or cutoff switch. The current package battery block is `275 x 230 x 190 mm`; verify it against the actual installed battery and update the map if the real battery differs.

- Establish datums with the vehicle facing forward: front/radiator side, rear/firewall side, inboard engine/LHD steering side, outboard wing side, and vertical bonnet clearance.
- Put the battery or a full-size battery box in the tray and mark a no-go block around it: battery case, hold-down, terminals, terminal boots, and cable lug bend radius.
- Measure the cavity in slices at tray height, mid-battery height, battery-top height, and bonnet/terminal-service height.
- Record available rectangles to the front, inboard/engine side, outboard/wing side, and below the tray. Do not count space that requires the battery to be removed for fuse or relay service.
- Trial the known templates in cardboard: Relay Rev C folded tray `320 x 220 mm`, MIDI Rev C open plate `190 x 150 mm`, cutoff tab/guard `170 x 110 mm`, plus their real depth and cable lug sweep.
- Treat the front/radiator-side volume as the first candidate because both battery-in and battery-out photos suggest more usable space forward than sideways.
- Treat the inboard/engine-side gap as a cautious candidate only. It must clear LHD steering shaft/box/service motion, hydraulic lines, hoses, alternator service, and heat.
- Treat the lower void as cable support or shielded junction space only unless dry, serviceable, and protected from splash and heat.
- Split the layout by default: cutoff in the most accessible top/front spot, MIDI on the shortest protected high-current path, relays on a separate forward/vertical tray, and P-clips on the stand.

Detailed measurement rows are in `cavity_mapping_plan.csv`.

## Materials

- Stand top tray/deck, compact front rail, and small steel tabs: `3.0 mm` mild steel.
- Single chassis pickup plate and upright bridge: `4.0 mm` mild steel.
- Battery hold-down crossbar: `3.0 mm` mild steel or stainless.
- Cutoff tab/guard: `2.0-3.0 mm` aluminium, plastic, or 3.0 mm mild steel if it becomes a structural steel tab.
- Use stainless or zinc-plated M6/M8/M10 hardware with star washers only where electrical bonding is intended. Otherwise isolate live hardware from the steel stand.

## Chassis Mounting Rules

- Pick up at the one known chassis attachment location. Do not add a second vehicle-side fixing unless the dry-fit proves the single-pickup route cannot carry the assembly safely.
- Do not drill or weld the chassis until the battery, bonnet, fan/belt, radiator, LHD steering-side, alternator-service, and cable-sweep clearances are checked.
- Use crush tubes if any pickup goes through boxed structure.
- The stand must remove from the chassis without cutting wires or removing unrelated radiator support pieces.

## Clearance Holds Before Cutting Final Metal

- Battery installed: length, width, full case height, terminal side, clamp path, and bonnet clearance.
- Compact holder cards: Relay Rev C folded tray, MIDI Rev C open plate/subplate, cutoff tab, and cable-lug depth must fit the measured front/inboard/lower/outboard volume without touching the steering-side service envelope.
- Single chassis pickup: hole pitch, stand-off height, upright bridge height, and access for tools.
- Cutoff switch: panel-hole diameter, body depth, key/knob sweep, terminal stud size, and cable-lug sweep.
- Relay Rev C base: final carrier orientation, standoff height, seal direction, and loom exit direction.
- MIDI Rev C base/subplate: final feed/output orientation and cable bend radius.
- Cable support: P-clip positions every `150-200 mm` and near every direction change.

## Safety Notes

- No exposed positive stud may be able to touch the stand, bonnet, battery clamp, radiator support, or loose tools.
- Put insulating boots/caps over cutoff, MIDI, and relay feed studs.
- Keep the relay loom opening downward or side-down so water cannot pool.
- Route all heavy positive cables away from fan, belts, exhaust heat, steering movement, and sharp panel edges.
"""
    (OUT_DIR / "README.md").write_text(text, encoding="utf-8")


def write_cut_list() -> None:
    rows = [
        {
            "part_id": "BSTAND-TRAY-001",
            "drawing": "battery_stand_compact_top_tray_rev_b.dxf",
            "qty": "1",
            "material": "mild steel",
            "thickness_mm": "3.0",
            "status": "prototype_release_mockup_required",
            "notes": "Compact 315 x 265 battery tray/deck with battery clamp slots and cable clip holes. Electrical holders mount on separate compact rails/tabs.",
        },
        {
            "part_id": "BPCC-FRONT-RAIL-001",
            "drawing": "battery_power_compact_front_service_rail_rev_b.dxf",
            "qty": "1",
            "material": "mild steel",
            "thickness_mm": "3.0",
            "status": "cavity_map_required",
            "notes": "Compact 340 x 90 front service rail for folded Relay Rev C tray or measured front-cavity bracket; replaces the earlier large shared carrier.",
        },
        {
            "part_id": "BSTAND-PICKUP-001",
            "drawing": "battery_stand_compact_single_chassis_pickup_rev_b.dxf",
            "qty": "1",
            "material": "mild steel",
            "thickness_mm": "4.0",
            "status": "site_fit",
            "notes": "Compact single vehicle-side chassis pickup plate. Use crush tubes/spacers where required; final slot pitch follows the actual chassis location.",
        },
        {
            "part_id": "BSTAND-UPRIGHT-001",
            "drawing": "battery_stand_compact_single_mount_upright_rev_b.dxf",
            "qty": "2 mirrored",
            "material": "mild steel",
            "thickness_mm": "4.0",
            "status": "site_fit",
            "notes": "Compact upright bridge side plates from the single chassis pickup to tray/rail saddle; not a second chassis fixing location.",
        },
        {
            "part_id": "BSTAND-HOLD-001",
            "drawing": "battery_stand_compact_hold_down_crossbar_rev_b.dxf",
            "qty": "1",
            "material": "mild steel or stainless",
            "thickness_mm": "3.0",
            "status": "battery_measurement_hold",
            "notes": "Battery hold-down crossbar template; final slot spacing follows actual battery and clamp rod positions.",
        },
        {
            "part_id": "BPCC-CUTOFF-TAB-001",
            "drawing": "battery_power_compact_cutoff_tab_rev_b.dxf",
            "qty": "1",
            "material": "aluminium or plastic",
            "thickness_mm": "2.0-3.0",
            "status": "fit_after_switch_measurement",
            "notes": "Compact 170 x 110 tab/knock guard for master cutoff; must not block emergency access.",
        },
    ]
    path = OUT_DIR / "fabricator_cut_list.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_inspection_checklist() -> None:
    rows = [
        {
            "check_id": "BPCC-CHECK-001",
            "stage": "mockup",
            "acceptance_check": "Compact stand tray clears installed battery, terminal clamp, bonnet, radiator, fan/belt, LHD steering path, and alternator service sweep.",
            "required_evidence": "Cardboard/top-tray photo with battery installed and ruler in frame.",
        },
        {
            "check_id": "BPCC-CHECK-001A",
            "stage": "compact_cavity_cards",
            "acceptance_check": "Compact holder cards for Relay Rev C folded tray 320 x 220, MIDI open plate 190 x 150, cutoff tab 170 x 110, cable depth, and lug sweep fit measured front/inboard/lower/outboard volumes without entering LHD steering/hose/fan/bonnet/battery service envelopes.",
            "required_evidence": "Battery-installed LHD bay photos from top, engine side, wing side, and front with cardboard cards and cable-lug depth marked.",
        },
        {
            "check_id": "BPCC-CHECK-002",
            "stage": "chassis_pickup",
            "acceptance_check": "Battery and electrical load is taken by the one known chassis pickup through the single pickup plate and upright bridge, not tray skin or unsupported inner wing.",
            "required_evidence": "Photos of pickup points before and after drilling/welding; note bolt size or weld length.",
        },
        {
            "check_id": "BPCC-CHECK-003",
            "stage": "electrical_fit",
            "acceptance_check": "Folded Relay Rev C tray, MIDI open plate/subplate, and master cutoff tab/guard all mount on compact rails/tabs without forced cable bends or live-stud exposure.",
            "required_evidence": "Assembled bench photo and installed dry-fit photo with cable lugs mocked in.",
        },
        {
            "check_id": "BPCC-CHECK-004",
            "stage": "cable_support",
            "acceptance_check": "Main positive cable has insulated P-clips near direction changes and roughly every 150-200 mm.",
            "required_evidence": "Cable route photo showing clip holes/tabs and bend radius.",
        },
        {
            "check_id": "BPCC-CHECK-005",
            "stage": "coating",
            "acceptance_check": "Chassis pickup plate/upright bridge contact faces are deburred, primed, protected, and clear before final electrical hardware is installed.",
            "required_evidence": "Coated chassis pickup photo before mounting electrical parts.",
        },
    ]
    path = OUT_DIR / "inspection_checklist.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_layout_csv() -> None:
    rows = [
        {
            "zone": "battery_footprint",
            "x_mm": "20",
            "y_mm": "18",
            "w_mm": "275",
            "h_mm": "230",
            "z_height_mm": "190 visual reference; measure actual battery",
            "notes": "Current battery datum inside compact 315 x 265 tray; final footprint, full case height, and terminal side follow actual battery.",
        },
        {
            "zone": "compact_top_tray",
            "x_mm": "0",
            "y_mm": "0",
            "w_mm": "315",
            "h_mm": "265",
            "z_height_mm": "3 mm steel tray/deck plus battery mat",
            "notes": "Compact battery support tray only; do not use the tray skin as a large electrical backplane.",
        },
        {
            "zone": "relay_rev_c_folded_tray_card",
            "x_mm": "site_fit",
            "y_mm": "site_fit",
            "w_mm": "320",
            "h_mm": "220",
            "z_height_mm": "finished face plus 20 mm side/bottom returns, 15 mm top return, relay box and loom depth measurement hold",
            "notes": "First candidate is the front/radiator-side cavity. Treat as its own folded tray and mount to a measured compact rail/tab.",
        },
        {
            "zone": "midi_rev_c_open_plate_card",
            "x_mm": "site_fit",
            "y_mm": "site_fit",
            "w_mm": "190",
            "h_mm": "150",
            "z_height_mm": "known 190 x 150 plate plus 140 x 85 subplate and holder/cable depth",
            "notes": "Open plate/subplate assembly, not a folded tray. Place only after the protected high-current path is measured.",
        },
        {
            "zone": "cutoff_compact_tab_card",
            "x_mm": "site_fit",
            "y_mm": "site_fit",
            "w_mm": "170",
            "h_mm": "110",
            "z_height_mm": "switch body/knob/stud height measurement hold",
            "notes": "Place at the most accessible front/top position; open final switch hole after measuring real switch.",
        },
        {
            "zone": "compact_front_service_rail",
            "x_mm": "site_fit",
            "y_mm": "site_fit",
            "w_mm": "340",
            "h_mm": "90",
            "z_height_mm": "component and cable-lug depth measurement hold",
            "notes": "Vehicle-side rail only if front cavity fit is proven. Mounts folded relay tray or a measured compact bracket.",
        },
        {
            "zone": "single_chassis_pickup",
            "x_mm": "site_fit",
            "y_mm": "site_fit",
            "w_mm": "220",
            "h_mm": "140",
            "z_height_mm": "upright bridge height site-fit",
            "notes": "One 4 mm chassis pickup plate bolts the stand to the known vehicle-side chassis location.",
        },
    ]
    path = OUT_DIR / "component_layout.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_cavity_mapping_plan() -> None:
    rows = [
        {
            "step_id": "CAV-001",
            "zone_or_task": "battery_datum",
            "datum_basis": "Current package battery block 275 x 230 x 190 mm; verify actual installed battery before final layout.",
            "measurements_to_capture": "Actual battery length, width, case height, terminal height, terminal orientation, hold-down path, and cable-lug bend radius.",
            "template_or_tool": "Battery installed or full-size cardboard/foam battery block plus tape/ruler.",
            "pass_rule": "Battery datum is marked on tray/frame before any relay, MIDI, cutoff, or cable support location is chosen.",
            "notes": "If the real battery differs from 275 x 230 x 190 mm, update component_layout.csv and redraw any cardboard templates before cutting steel.",
        },
        {
            "step_id": "CAV-002",
            "zone_or_task": "coordinate_system",
            "datum_basis": "Vehicle facing forward.",
            "measurements_to_capture": "Front/radiator side, rear/firewall side, inboard engine/LHD steering side, outboard wing side, tray plane, and bonnet/service height.",
            "template_or_tool": "Masking tape labels on tray, inner wing, front support, and engine-side obstruction line.",
            "pass_rule": "Every later measurement is recorded against the same front/rear/inboard/outboard/up datums.",
            "notes": "Avoid ambiguous left/right labels in the shop notes; use inboard/engine-side and outboard/wing-side.",
        },
        {
            "step_id": "CAV-003",
            "zone_or_task": "battery_no_go_block",
            "datum_basis": "Battery case plus service space.",
            "measurements_to_capture": "Minimum clearance around battery case, terminal boot height, clamp/crossbar sweep, and battery removal path.",
            "template_or_tool": "Tape outline around battery, 15-20 mm vibration allowance, 40 mm minimum terminal/service allowance, cable lug mock-ups.",
            "pass_rule": "No electrical module or bracket projects into the battery removal, hold-down, terminal, or cable-lug service envelope.",
            "notes": "Do not use space that only exists with the battery removed unless the part is a service-removable tray component.",
        },
        {
            "step_id": "CAV-004",
            "zone_or_task": "front_radiator_side_volume",
            "datum_basis": "Front edge of battery/tray to radiator/front-support obstruction.",
            "measurements_to_capture": "Clear width, height, depth, bolt access, radiator/fan clearance, hose sweep, and bonnet clearance.",
            "template_or_tool": "Folded Relay Rev C tray 320 x 220 with return/depth block, MIDI open plate 190 x 150, cutoff tab 170 x 110 cardboard templates with 40-80 mm depth blocks.",
            "pass_rule": "First-choice candidate only if templates fit with cable bends, no fan/radiator contact, and service access with battery installed.",
            "notes": "Both photos suggest the front volume may be the most realistic place to find usable electrical mounting area.",
        },
        {
            "step_id": "CAV-005",
            "zone_or_task": "inboard_engine_lhd_side_volume",
            "datum_basis": "Inboard/engine-side battery face to hoses, steering-side envelope, alternator/service path, and engine movement allowance.",
            "measurements_to_capture": "Usable vertical rectangle at tray/mid/top heights, steering shaft/box/service clearance, hose movement, heat exposure, and tool access.",
            "template_or_tool": "Narrow strip templates plus relay/MIDI/cutoff templates only if a clear rectangle exists.",
            "pass_rule": "Use for cables, P-clips, or a small high-mounted module only if it does not enter LHD steering/hose/service no-go space.",
            "notes": "Do not force a shared large carrier into this side gap; use measured compact tabs/rails only.",
        },
        {
            "step_id": "CAV-006",
            "zone_or_task": "lower_under_tray_volume",
            "datum_basis": "Bottom of tray/frame down to chassis, steering/hose runs, and splash/heat exposure.",
            "measurements_to_capture": "Height below tray, dry/splash exposure, service access, cable path, heat, and clamp points.",
            "template_or_tool": "Cable/P-clip templates first; electrical module templates only if fully protected and reachable.",
            "pass_rule": "Default to cable support or protected pass-through only; reject relay/MIDI/cutoff placement if wet, hot, or not serviceable.",
            "notes": "Lower space can help route cables but should not become the default place for live service parts.",
        },
        {
            "step_id": "CAV-007",
            "zone_or_task": "outboard_wing_side_volume",
            "datum_basis": "Battery outboard face to wing/side panel and bonnet side clearance.",
            "measurements_to_capture": "Side gap, vertical clearance, battery removal path, clamp access, panel strength, and water trap risk.",
            "template_or_tool": "Cutoff 170 x 110 and small cable-clamp templates.",
            "pass_rule": "Use only if it remains accessible with battery installed and does not block battery removal or bonnet/wing clearance.",
            "notes": "Likely useful for cable support or emergency cutoff access only if a clean panel exists.",
        },
        {
            "step_id": "CAV-008",
            "zone_or_task": "bonnet_and_terminal_height",
            "datum_basis": "Top of battery, terminals, relay/MIDI/cutoff depth, and bonnet closed/near-closed envelope.",
            "measurements_to_capture": "Clay/foam witness height above battery terminals, proposed module height, cable boots, and hold-down crossbar.",
            "template_or_tool": "Foam/clay stack or cardboard height blocks taped to battery and module templates.",
            "pass_rule": "No terminal, lug, fuse, relay, cutoff, or bracket touches bonnet or blocks safe terminal service clearance.",
            "notes": "This check decides whether top/front mounting is realistic or needs a lower stepped plate.",
        },
        {
            "step_id": "CAV-009",
            "zone_or_task": "split_layout_decision",
            "datum_basis": "Measured available rectangles from CAV-004 through CAV-008.",
            "measurements_to_capture": "Largest serviceable rectangle in each zone and cable length between battery, cutoff, MIDI, relay, and harness exit.",
            "template_or_tool": "Component cards: Relay Rev C folded tray 320 x 220, MIDI open plate 190 x 150, cutoff tab 170 x 110, plus depth/lug blocks.",
            "pass_rule": "Choose split/stepped compact holders unless the measured cavity proves a single face is actually smaller, serviceable, and clear.",
            "notes": "Preferred split order: cutoff most accessible, MIDI shortest protected high-current path, relays on forward/vertical protected plate, P-clips on stand.",
        },
        {
            "step_id": "CAV-010",
            "zone_or_task": "evidence_closeout",
            "datum_basis": "Battery installed and battery removed photos.",
            "measurements_to_capture": "Top, front, inboard/engine-side, outboard/wing-side, lower, and near-closed bonnet photos with ruler and cardboard templates.",
            "template_or_tool": "Photo set plus filled cavity map; update component_layout.csv with measured clear rectangles.",
            "pass_rule": "No steel cutting for relay/MIDI/cutoff carrier until the filled cavity map proves at least one serviceable layout.",
            "notes": "Attach photos to the Fabrication workstream and keep original no-battery/battery-installed references with the map.",
        },
    ]
    path = OUT_DIR / "cavity_mapping_plan.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    drawings = [
        integrated_backplane(),
        battery_stand_top_tray(),
        single_chassis_pickup_mount(),
        single_mount_upright(),
        battery_hold_down_crossbar(),
        cutoff_guard(),
    ]
    for drawing in drawings:
        base.write_svg(drawing)
        base.write_dxf(drawing)
    base.write_pdf(drawings)
    write_readme()
    write_static_3d_visualisation()
    write_interactive_3d_visualisation()
    write_assembled_static_3d_visualisation()
    write_assembled_interactive_3d_visualisation()
    write_cut_list()
    write_inspection_checklist()
    write_layout_csv()
    write_cavity_mapping_plan()


if __name__ == "__main__":
    main()
