from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path("/Users/davidpridmore/IdeaProjects/J40")
FAB_DIR = ROOT / "data" / "manual" / "fabrication"


SCENES = {
    "suspension_wood_cribbing_rev_a": {
        "title": "Suspension Wood Cribbing Rev A",
        "subtitle": "Eight hardwood cribbing blocks and four wedge chocks for suspension support setup.",
        "camera": [360, 300, 420],
        "target": [0, 20, 0],
        "size": "300 x 150 x 75 mm cribbing blocks; 200 x 100 mm wedge chocks",
        "load_path": "Timber stack spreads load under axle or chassis support zones during setup.",
        "service_intent": "Use as supplemental cribbing/chocks only; not a substitute for rated stands.",
        "boxes": [
            {"name": "Cribbing block", "x": -165, "y": 37, "z": -95, "w": 300, "h": 75, "d": 150, "color": "wood"},
            {"name": "Cribbing block", "x": 165, "y": 37, "z": -95, "w": 300, "h": 75, "d": 150, "color": "wood"},
            {"name": "Cribbing block", "x": -165, "y": 118, "z": 95, "w": 300, "h": 75, "d": 150, "color": "wood"},
            {"name": "Cribbing block", "x": 165, "y": 118, "z": 95, "w": 300, "h": 75, "d": 150, "color": "wood"},
            {"name": "Wedge chock", "x": -250, "y": 30, "z": 120, "w": 200, "h": 60, "d": 100, "color": "wedge"},
            {"name": "Wedge chock", "x": 250, "y": 30, "z": 120, "w": 200, "h": 60, "d": 100, "color": "wedge"},
        ],
    },
    "midi5_plate_mount_rev_c": {
        "title": "MIDI 5-Way Plate Mount Rev C",
        "subtitle": "Open aluminium MIDI holder plate with insulated subplate and five fuse holders.",
        "camera": [310, 260, 390],
        "target": [0, 22, 0],
        "size": "190 x 150 x 3 mm plate; 140 x 85 x 5 mm insulated holder subplate",
        "load_path": "The plate is the vehicle-side carrier; the non-conductive subplate isolates the MIDI holders.",
        "service_intent": "Leave cable exits and holder screws accessible for fuse and branch-feed service.",
        "boxes": [
            {"name": "Aluminium mount plate", "x": 0, "y": 3, "z": 0, "w": 190, "h": 6, "d": 150, "color": "aluminium"},
            {"name": "Insulated holder subplate", "x": 0, "y": 15, "z": 0, "w": 140, "h": 10, "d": 85, "color": "black"},
            {"name": "MIDI holder", "x": -54, "y": 35, "z": 0, "w": 20, "h": 26, "d": 62, "color": "red"},
            {"name": "MIDI holder", "x": -27, "y": 35, "z": 0, "w": 20, "h": 26, "d": 62, "color": "red"},
            {"name": "MIDI holder", "x": 0, "y": 35, "z": 0, "w": 20, "h": 26, "d": 62, "color": "red"},
            {"name": "MIDI holder", "x": 27, "y": 35, "z": 0, "w": 20, "h": 26, "d": 62, "color": "red"},
            {"name": "MIDI holder", "x": 54, "y": 35, "z": 0, "w": 20, "h": 26, "d": 62, "color": "red"},
        ],
        "cylinders": [
            {"name": "Standoff", "x": -68, "y": 23, "z": -36, "r": 4, "h": 16, "color": "brass"},
            {"name": "Standoff", "x": 68, "y": 23, "z": -36, "r": 4, "h": 16, "color": "brass"},
            {"name": "Standoff", "x": -68, "y": 23, "z": 36, "r": 4, "h": 16, "color": "brass"},
            {"name": "Standoff", "x": 68, "y": 23, "z": 36, "r": 4, "h": 16, "color": "brass"},
        ],
    },
    "relay_mount_rev_c": {
        "title": "Relay Mount Rev C",
        "subtitle": "Fallback standalone folded relay-box carrier with rear guard and serviceable loom exit.",
        "camera": [380, 310, 460],
        "target": [0, 30, 0],
        "size": "360 x 255 mm carrier blank; 320 x 220 mm finished face; 280 x 185 mm rear guard",
        "load_path": "The 90-degree folded aluminium carrier supports the DAIER relay/fuse box if the split relay route is used.",
        "service_intent": "Show the 20 mm side/bottom returns and 15 mm top return; keep the rear guard spaced and the lower loom opening downward.",
        "boxes": [
            {"name": "Folded relay carrier face", "x": 0, "y": 3, "z": 0, "w": 320, "h": 8, "d": 220, "color": "aluminium"},
            {"name": "Left 20 mm 90-degree return", "x": -170, "y": -18, "z": 0, "w": 20, "h": 42, "d": 220, "color": "aluminium"},
            {"name": "Right 20 mm 90-degree return", "x": 170, "y": -18, "z": 0, "w": 20, "h": 42, "d": 220, "color": "aluminium"},
            {"name": "Bottom 20 mm 90-degree return", "x": 0, "y": -18, "z": 120, "w": 320, "h": 42, "d": 20, "color": "aluminium"},
            {"name": "Top 15 mm 90-degree return", "x": 0, "y": -16, "z": -117.5, "w": 320, "h": 38, "d": 15, "color": "aluminium"},
            {"name": "Left bend crease", "x": -160, "y": 12, "z": 0, "w": 4, "h": 4, "d": 220, "color": "bendline"},
            {"name": "Right bend crease", "x": 160, "y": 12, "z": 0, "w": 4, "h": 4, "d": 220, "color": "bendline"},
            {"name": "Bottom bend crease", "x": 0, "y": 12, "z": 110, "w": 320, "h": 4, "d": 4, "color": "bendline"},
            {"name": "Top bend crease", "x": 0, "y": 12, "z": -110, "w": 320, "h": 4, "d": 4, "color": "bendline"},
            {"name": "Relay/fuse box", "x": 0, "y": 48, "z": -5, "w": 295, "h": 62, "d": 170, "color": "black"},
            {"name": "Rear guard", "x": 0, "y": -20, "z": 0, "w": 280, "h": 5, "d": 185, "color": "plastic"},
        ],
    },
    "electrical_modules_rev_a": {
        "title": "Electrical Modules Rev A",
        "subtitle": "Earlier reference route with folded relay tray, folded power module box, and rear insulator.",
        "camera": [430, 330, 520],
        "target": [0, 28, 0],
        "size": "Relay module tray plus power module box and rear insulator",
        "load_path": "Reference combined-module arrangement only; the aluminium tray and box use 90-degree folded flanges.",
        "service_intent": "Use this page for visual reference if the combined route is reopened; bend-line flanges are shown folded, not flat.",
        "boxes": [
            {"name": "Relay tray floor 320 x 220", "x": -150, "y": 3, "z": 0, "w": 320, "h": 8, "d": 220, "color": "aluminium"},
            {"name": "Relay tray left 20 mm 90-degree flange", "x": -320, "y": -18, "z": 0, "w": 20, "h": 42, "d": 220, "color": "aluminium"},
            {"name": "Relay tray right 20 mm 90-degree flange", "x": 20, "y": -18, "z": 0, "w": 20, "h": 42, "d": 220, "color": "aluminium"},
            {"name": "Relay tray front 20 mm 90-degree flange", "x": -150, "y": -18, "z": 120, "w": 320, "h": 42, "d": 20, "color": "aluminium"},
            {"name": "Relay tray rear 20 mm 90-degree flange", "x": -150, "y": -18, "z": -120, "w": 320, "h": 42, "d": 20, "color": "aluminium"},
            {"name": "Relay tray left bend crease", "x": -310, "y": 12, "z": 0, "w": 4, "h": 4, "d": 220, "color": "bendline"},
            {"name": "Relay tray right bend crease", "x": 10, "y": 12, "z": 0, "w": 4, "h": 4, "d": 220, "color": "bendline"},
            {"name": "Relay tray front bend crease", "x": -150, "y": 12, "z": 110, "w": 320, "h": 4, "d": 4, "color": "bendline"},
            {"name": "Relay tray rear bend crease", "x": -150, "y": 12, "z": -110, "w": 320, "h": 4, "d": 4, "color": "bendline"},
            {"name": "Relay box", "x": -150, "y": 50, "z": 0, "w": 250, "h": 64, "d": 150, "color": "black"},
            {"name": "Power module box face 220 x 140", "x": 160, "y": 3, "z": 0, "w": 220, "h": 8, "d": 140, "color": "aluminium"},
            {"name": "Power module left 20 mm 90-degree flange", "x": 40, "y": -18, "z": 0, "w": 20, "h": 42, "d": 140, "color": "aluminium"},
            {"name": "Power module right 20 mm 90-degree flange", "x": 280, "y": -18, "z": 0, "w": 20, "h": 42, "d": 140, "color": "aluminium"},
            {"name": "Power module lower 20 mm 90-degree flange", "x": 160, "y": -18, "z": 80, "w": 220, "h": 42, "d": 20, "color": "aluminium"},
            {"name": "Power module upper 20 mm 90-degree flange", "x": 160, "y": -18, "z": -80, "w": 220, "h": 42, "d": 20, "color": "aluminium"},
            {"name": "Power module left bend crease", "x": 50, "y": 12, "z": 0, "w": 4, "h": 4, "d": 140, "color": "bendline"},
            {"name": "Power module right bend crease", "x": 270, "y": 12, "z": 0, "w": 4, "h": 4, "d": 140, "color": "bendline"},
            {"name": "Power module lower bend crease", "x": 160, "y": 12, "z": 70, "w": 220, "h": 4, "d": 4, "color": "bendline"},
            {"name": "Power module upper bend crease", "x": 160, "y": 12, "z": -70, "w": 220, "h": 4, "d": 4, "color": "bendline"},
            {"name": "Breaker/MIDI module", "x": 160, "y": 42, "z": 0, "w": 170, "h": 55, "d": 100, "color": "red"},
            {"name": "Rear insulator", "x": 160, "y": -18, "z": 0, "w": 210, "h": 5, "d": 130, "color": "plastic"},
        ],
    },
}


MATERIALS = {
    "aluminium": {"color": "#c1cbd3", "side": "#8d99a4"},
    "steel": {"color": "#717b84", "side": "#535d66"},
    "wood": {"color": "#b9874f", "side": "#8d6135"},
    "wedge": {"color": "#d2a263", "side": "#936739"},
    "black": {"color": "#202a33", "side": "#11181e"},
    "plastic": {"color": "#2d3942", "side": "#1c252b"},
    "red": {"color": "#b7302a", "side": "#7e1e1a"},
    "brass": {"color": "#c8a451", "side": "#8c6d2a"},
    "bendline": {"color": "#2f3942", "side": "#202830"},
}


def iso_point(x: float, z: float, y: float) -> tuple[float, float]:
    return 420 + (x - z) * 0.72, 100 + (x + z) * 0.32 - y * 1.1


def points_attr(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def polygon(points: list[tuple[float, float, float]], css_class: str) -> str:
    return f'<polygon class="{css_class}" points="{points_attr([iso_point(*point) for point in points])}" />'


def prism(box: dict[str, object], index: int) -> list[str]:
    x = float(box["x"]) - float(box["w"]) / 2
    z = float(box["z"]) - float(box["d"]) / 2
    y = float(box["y"])
    w = float(box["w"])
    d = float(box["d"])
    h = float(box["h"])
    color_key = str(box.get("color", "aluminium"))
    top_class = f"box-top-{index}"
    side_class = f"box-side-{index}"
    front_class = f"box-front-{index}"
    return [
        f".{top_class} {{ fill: {MATERIALS[color_key]['color']}; stroke: #38434c; stroke-width: 1.1; }}",
        f".{side_class}, .{front_class} {{ fill: {MATERIALS[color_key]['side']}; stroke: #38434c; stroke-width: 1; }}",
        polygon([(x + w, z, y), (x + w, z + d, y), (x + w, z + d, y + h), (x + w, z, y + h)], side_class),
        polygon([(x, z + d, y), (x + w, z + d, y), (x + w, z + d, y + h), (x, z + d, y + h)], front_class),
        polygon([(x, z, y + h), (x + w, z, y + h), (x + w, z + d, y + h), (x, z + d, y + h)], top_class),
    ]


def write_svg(package_id: str, scene: dict[str, object]) -> None:
    css: list[str] = []
    elems: list[str] = [
        '<rect class="background" width="920" height="620" />',
        '<ellipse class="shadow" cx="455" cy="430" rx="330" ry="74" />',
    ]
    for index, box in enumerate(scene.get("boxes", [])):
        parts = prism(box, index)
        css.extend(parts[:3])
        elems.extend(parts[3:])
    title = escape(str(scene["title"]))
    subtitle = escape(str(scene["subtitle"]))
    labels = [
        f'<text class="title" x="34" y="46">{title}</text>',
        f'<text class="subtitle" x="34" y="74">{subtitle}</text>',
        '<text class="label" x="34" y="556">Static assembly visual. Open the HTML file for rotate/zoom interaction.</text>',
    ]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="620" viewBox="0 0 920 620" role="img">
  <style>
    .background {{ fill: #f6f7f8; }}
    .shadow {{ fill: #d8dde2; opacity: 0.7; }}
    .title {{ font: 700 26px Arial, sans-serif; fill: #202a33; }}
    .subtitle, .label {{ font: 16px Arial, sans-serif; fill: #4f5d68; }}
    {''.join(css)}
  </style>
  {''.join(labels)}
  {''.join(elems)}
</svg>
"""
    out_dir = FAB_DIR / package_id
    (out_dir / f"{package_id}_3d_visualisation.svg").write_text(svg, encoding="utf-8")


def write_html(package_id: str, scene: dict[str, object]) -> None:
    scene_json = json.dumps(scene, separators=(",", ":"))
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(str(scene["title"]))} - 3D Visualisation</title>
  <link rel="icon" href="data:,">
  <style>
    :root {{ font-family: Arial, Helvetica, sans-serif; background: #f5f6f7; color: #1d252c; }}
    body {{ margin: 0; min-height: 100vh; display: grid; grid-template-rows: auto 1fr; }}
    body.embed {{ grid-template-rows: 1fr; }}
    header {{ padding: 16px 22px 10px; background: #fff; border-bottom: 1px solid #d8dde2; }}
    h1 {{ margin: 0; font-size: clamp(20px, 3vw, 30px); letter-spacing: 0; }}
    .meta {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}
    .chip {{ border: 1px solid #c8d0d8; border-radius: 999px; padding: 5px 9px; background: #f8fafb; font-size: 13px; }}
    main {{ display: grid; grid-template-columns: minmax(0, 1fr) 300px; min-height: 0; }}
    #viewport {{ position: relative; min-height: 560px; overflow: hidden; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
    aside {{ border-left: 1px solid #d8dde2; background: #fff; padding: 18px; }}
    h2 {{ margin: 0 0 12px; font-size: 18px; letter-spacing: 0; }}
    dl {{ margin: 0; display: grid; gap: 12px; }}
    dt {{ font-weight: 700; }}
    dd {{ margin: 3px 0 0; color: #54616c; font-size: 14px; line-height: 1.45; }}
    #fallback {{ position: absolute; inset: 0; display: grid; place-items: center; padding: 20px; background: #f5f6f7; }}
    #fallback img {{ width: min(94vw, 920px); max-height: 82vh; object-fit: contain; }}
    body.is-three-ready #fallback {{ display: none; }}
    body.embed header,
    body.embed aside {{ display: none; }}
    body.embed main {{ grid-template-columns: 1fr; min-height: 100vh; }}
    body.embed #viewport {{ min-height: 100vh; }}
    @media (max-width: 820px) {{ main {{ grid-template-columns: 1fr; }} #viewport {{ min-height: 430px; }} aside {{ border-left: 0; border-top: 1px solid #d8dde2; }} }}
  </style>
  <script type="importmap">{{"imports":{{"three":"https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.164.1/examples/jsm/"}}}}</script>
</head>
<body>
  <script>
    if (new URLSearchParams(window.location.search).has("embed")) {{
      document.body.classList.add("embed");
    }}
  </script>
  <header>
    <h1>{escape(str(scene["title"]))}</h1>
    <div class="meta">
      <span class="chip">{escape(str(scene["size"]))}</span>
      <span class="chip">Interactive rotate/zoom</span>
      <span class="chip">Fabrication package visual</span>
    </div>
  </header>
  <main>
    <section id="viewport" aria-label="Interactive 3D fabrication visualisation">
      <div id="fallback"><img src="./{package_id}_3d_visualisation.svg" alt="{escape(str(scene["title"]))} static visualisation"></div>
    </section>
    <aside>
      <h2>Assembly Read</h2>
      <dl>
        <div><dt>Package role</dt><dd>{escape(str(scene["subtitle"]))}</dd></div>
        <div><dt>Load path</dt><dd>{escape(str(scene["load_path"]))}</dd></div>
        <div><dt>Service intent</dt><dd>{escape(str(scene["service_intent"]))}</dd></div>
      </dl>
    </aside>
  </main>
  <script type="module">
    import * as THREE from "three";
    import {{ OrbitControls }} from "three/addons/controls/OrbitControls.js";

    const sceneData = {scene_json};
    const materialDefs = {{
      aluminium: [0xc1cbd3, 0.35, 0.38],
      steel: [0x59636c, 0.45, 0.5],
      wood: [0xb9874f, 0.1, 0.55],
      wedge: [0xd2a263, 0.1, 0.52],
      black: [0x202a33, 0.05, 0.62],
      plastic: [0x2d3942, 0.02, 0.7],
      red: [0xb7302a, 0.03, 0.42],
      brass: [0xc4a35a, 0.4, 0.36],
      bendline: [0x2f3942, 0.05, 0.58],
    }};
    const materials = Object.fromEntries(Object.entries(materialDefs).map(([key, value]) => [
      key,
      new THREE.MeshStandardMaterial({{ color: value[0], metalness: value[1], roughness: value[2] }})
    ]));

    const mount = document.getElementById("viewport");
    const threeScene = new THREE.Scene();
    threeScene.background = new THREE.Color(0xf5f6f7);
    const camera = new THREE.PerspectiveCamera(38, 1, 1, 2200);
    camera.position.set(...sceneData.camera);
    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: false, preserveDrawingBuffer: true }});
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = true;
    mount.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(...sceneData.target);
    controls.enableDamping = true;
    controls.minDistance = 260;
    controls.maxDistance = 1200;
    controls.maxPolarAngle = Math.PI * 0.48;

    const root = new THREE.Group();
    threeScene.add(root);

    function box(item) {{
      const mesh = new THREE.Mesh(
        new THREE.BoxGeometry(item.w, item.h, item.d),
        materials[item.color] || materials.aluminium
      );
      mesh.name = item.name;
      mesh.position.set(item.x, item.y, item.z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      root.add(mesh);
    }}

    function cylinder(item) {{
      const mesh = new THREE.Mesh(
        new THREE.CylinderGeometry(item.r, item.r, item.h, 36),
        materials[item.color] || materials.aluminium
      );
      mesh.name = item.name;
      mesh.position.set(item.x, item.y, item.z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      root.add(mesh);
    }}

    sceneData.boxes.forEach(box);
    (sceneData.cylinders || []).forEach(cylinder);

    threeScene.add(new THREE.HemisphereLight(0xffffff, 0x98a1aa, 2.2));
    const key = new THREE.DirectionalLight(0xffffff, 2.4);
    key.position.set(260, 420, 300);
    key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    threeScene.add(key);

    const ground = new THREE.Mesh(new THREE.PlaneGeometry(900, 680), new THREE.ShadowMaterial({{ color: 0x000000, opacity: 0.12 }}));
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -62;
    ground.receiveShadow = true;
    threeScene.add(ground);

    function resize() {{
      const width = mount.clientWidth;
      const height = mount.clientHeight;
      renderer.setSize(width, height, false);
      camera.aspect = width / Math.max(1, height);
      camera.updateProjectionMatrix();
    }}
    function animate() {{
      controls.update();
      renderer.render(threeScene, camera);
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
    out_dir = FAB_DIR / package_id
    (out_dir / f"{package_id}_3d_visualisation.html").write_text(html, encoding="utf-8")


def main() -> None:
    for package_id, scene in SCENES.items():
        out_dir = FAB_DIR / package_id
        out_dir.mkdir(parents=True, exist_ok=True)
        write_svg(package_id, scene)
        write_html(package_id, scene)


if __name__ == "__main__":
    main()
