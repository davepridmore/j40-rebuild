from __future__ import annotations

from pathlib import Path
import json
from string import Template

from generate_j40_full_vehicle_cad_scaffold import BoxPart, CylinderPart, WheelPart, MODEL_TITLE, OUT_DIR, parts


ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = OUT_DIR / "j40_full_vehicle_orbit_viewer.html"


def part_payload() -> list[dict[str, object]]:
    payload: list[dict[str, object]] = []
    for part in parts():
        base = {
            "group": part.group,
            "name": part.name,
            "color": part.color,
            "confidence": part.confidence,
            "notes": part.notes,
        }
        if isinstance(part, BoxPart):
            base.update(
                {
                    "kind": "box",
                    "x": part.x,
                    "y": part.y,
                    "z": part.z,
                    "length": part.length,
                    "width": part.width,
                    "height": part.height,
                }
            )
        elif isinstance(part, WheelPart):
            base.update(
                {
                    "kind": "wheel",
                    "x": part.x,
                    "y": part.y,
                    "z": part.z,
                    "diameter": part.diameter,
                    "width": part.width,
                }
            )
        elif isinstance(part, CylinderPart):
            base.update(
                {
                    "kind": "cylinder",
                    "x": part.x,
                    "y": part.y,
                    "z": part.z,
                    "axis": part.axis,
                    "diameter": part.diameter,
                    "length": part.length,
                }
            )
        payload.append(base)
    return payload


HTML_TEMPLATE = Template(
    r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>J40 Orbit Viewer</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #111315;
      --panel: #181b1e;
      --panel-2: #202428;
      --border: #343a40;
      --text: #f2f4f5;
      --muted: #aeb7bf;
      --accent: #78b9c9;
    }
    * { box-sizing: border-box; }
    html, body {
      width: 100%;
      height: 100%;
      margin: 0;
      overflow: hidden;
      background: var(--bg);
      color: var(--text);
      font: 13px/1.35 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    #app {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 310px;
      width: 100%;
      height: 100%;
    }
    #stage {
      position: relative;
      min-width: 0;
      background: #111315;
    }
    canvas {
      display: block;
      width: 100%;
      height: 100%;
      cursor: grab;
      outline: none;
    }
    canvas:active { cursor: grabbing; }
    #toolbar {
      position: absolute;
      left: 16px;
      top: 14px;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
      padding: 8px;
      background: rgba(24,27,30,0.86);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 8px;
      backdrop-filter: blur(8px);
    }
    button {
      appearance: none;
      border: 1px solid var(--border);
      background: #262b30;
      color: var(--text);
      border-radius: 6px;
      padding: 7px 10px;
      font: inherit;
      cursor: pointer;
    }
    button:hover { border-color: var(--accent); }
    button.active {
      color: #091012;
      background: var(--accent);
      border-color: var(--accent);
    }
    #status {
      position: absolute;
      left: 16px;
      bottom: 14px;
      display: flex;
      gap: 12px;
      align-items: center;
      padding: 8px 10px;
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 8px;
      background: rgba(24,27,30,0.82);
      color: var(--muted);
      backdrop-filter: blur(8px);
      white-space: nowrap;
    }
    aside {
      min-width: 0;
      overflow: auto;
      border-left: 1px solid var(--border);
      background: var(--panel);
    }
    .section {
      padding: 14px 16px;
      border-bottom: 1px solid var(--border);
    }
    h1 {
      margin: 0 0 2px;
      font-size: 16px;
      font-weight: 700;
      letter-spacing: 0;
    }
    h2 {
      margin: 0 0 10px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0;
    }
    .meta {
      color: var(--muted);
      font-size: 12px;
    }
    .meta a {
      color: var(--accent);
      text-decoration: none;
    }
    .meta a:hover { text-decoration: underline; }
    .control {
      display: grid;
      gap: 6px;
      margin: 10px 0 0;
    }
    .control-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }
    input[type="range"] { width: 145px; accent-color: var(--accent); }
    .group-list {
      display: grid;
      gap: 7px;
    }
    label.group {
      display: grid;
      grid-template-columns: 18px 14px minmax(0, 1fr) auto;
      align-items: center;
      gap: 8px;
      padding: 6px 7px;
      border: 1px solid transparent;
      border-radius: 6px;
      background: var(--panel-2);
    }
    label.group:hover { border-color: #3c454d; }
    .swatch {
      width: 14px;
      height: 14px;
      border: 1px solid rgba(255,255,255,0.45);
    }
    .group-name {
      min-width: 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      text-transform: capitalize;
    }
    .count { color: var(--muted); font-size: 12px; }
    #partInfo {
      min-height: 112px;
      display: grid;
      gap: 5px;
      color: var(--muted);
    }
    #partInfo strong {
      display: block;
      color: var(--text);
      font-size: 14px;
      overflow-wrap: anywhere;
    }
    #partInfo .tag {
      display: inline-block;
      width: fit-content;
      margin-top: 2px;
      padding: 2px 6px;
      border: 1px solid var(--border);
      border-radius: 999px;
      color: var(--text);
      background: #111315;
      font-size: 11px;
      text-transform: capitalize;
    }
    #tooltip {
      position: absolute;
      pointer-events: none;
      display: none;
      max-width: 260px;
      padding: 7px 9px;
      border: 1px solid rgba(255,255,255,0.16);
      border-radius: 6px;
      background: rgba(10,12,14,0.9);
      color: var(--text);
      box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }
    @media (max-width: 900px) {
      #app { grid-template-columns: 1fr; grid-template-rows: minmax(0, 1fr) 260px; }
      aside { border-left: 0; border-top: 1px solid var(--border); }
      #toolbar { right: 16px; }
      #status { right: 16px; white-space: normal; }
    }
  </style>
</head>
<body>
  <div id="app">
    <main id="stage">
      <canvas id="viewer" tabindex="0" aria-label="J40 3D orbit viewer"></canvas>
      <div id="toolbar" aria-label="View controls">
        <button data-view="iso" class="active">Iso</button>
        <button data-view="side">Side</button>
        <button data-view="front">Front</button>
        <button data-view="top">Top</button>
        <button id="resetView">Reset</button>
      </div>
      <div id="status">
        <span id="drawCount"></span>
        <span>Drag orbit</span>
        <span>Wheel zoom</span>
        <span>Shift drag pan</span>
      </div>
      <div id="tooltip"></div>
    </main>
    <aside>
      <section class="section">
        <h1>$MODEL_TITLE</h1>
        <div class="meta">Left-hand-drive orbitable reference scaffold. Units: mm. Part count: <span id="partCount"></span>.</div>
        <div class="meta">Visual reference: <a href="https://sketchfab.com/3d-models/1976-toyota-land-cruiser-fj40-a4e58b09ce48444ca6164834c310880d">1976 Toyota Land Cruiser FJ40</a> by <a href="https://sketchfab.com/tonielpro520">tonielpro520</a>, licensed <a href="http://creativecommons.org/licenses/by/4.0/">CC-BY 4.0</a>. Generated scaffold is project-owned primitive geometry.</div>
      </section>
      <section class="section">
        <h2>Display</h2>
        <div class="control">
          <div class="control-row"><span>Explode</span><input id="explode" type="range" min="0" max="100" value="18"></div>
          <div class="control-row"><span>Opacity</span><input id="opacity" type="range" min="30" max="100" value="94"></div>
          <div class="control-row"><span>Wire overlay</span><input id="wire" type="checkbox" checked></div>
        </div>
      </section>
      <section class="section">
        <h2>Groups</h2>
        <div id="groups" class="group-list"></div>
      </section>
      <section class="section">
        <h2>Hover Part</h2>
        <div id="partInfo">
          <strong>No part selected</strong>
          <span>Move over the model to identify named scaffold parts.</span>
        </div>
      </section>
    </aside>
  </div>
<script>
const PARTS = $PARTS_JSON;

const canvas = document.getElementById("viewer");
const gl = canvas.getContext("webgl", { antialias: true, alpha: false });
if (!gl) {
  document.body.innerHTML = "<p style='padding:20px;color:white'>WebGL is not available in this browser.</p>";
  throw new Error("WebGL unavailable");
}

const CENTER_MM = [1920, 0, 850];
const SCALE = 0.001;
const CYLINDER_SEGMENTS = 24;
const GROUP_ORDER = [
  "body", "hard_top", "front_detail", "interior", "engine_bay",
  "chassis", "running_gear", "brake_system", "fuel_system", "exhaust", "datum"
];
const GROUP_EXPLODE = {
  body: [0.00, 0.10, 0.00],
  hard_top: [0.00, 0.55, 0.00],
  front_detail: [-0.55, 0.12, 0.00],
  interior: [0.00, 0.30, -0.16],
  engine_bay: [-0.32, 0.24, 0.10],
  chassis: [0.00, -0.22, 0.00],
  running_gear: [0.00, -0.52, 0.00],
  brake_system: [0.00, -0.74, -0.12],
  fuel_system: [0.36, -0.78, 0.16],
  exhaust: [0.00, -0.92, 0.22],
  datum: [0.00, -0.05, 0.00]
};

const state = {
  yaw: -0.82,
  pitch: 0.42,
  distance: 5.9,
  target: [0, 0, 0],
  explode: 0.18,
  opacity: 0.94,
  wire: true,
  visible: Object.fromEntries(GROUP_ORDER.map((group) => [group, true])),
  hover: null,
  mouse: [0, 0]
};

function hexToRgba(hex, alpha = 1) {
  const value = hex.replace("#", "");
  return [
    parseInt(value.slice(0, 2), 16) / 255,
    parseInt(value.slice(2, 4), 16) / 255,
    parseInt(value.slice(4, 6), 16) / 255,
    alpha
  ];
}

function modelToWorld(point) {
  return [
    (point[0] - CENTER_MM[0]) * SCALE,
    (point[2] - CENTER_MM[2]) * SCALE,
    (point[1] - CENTER_MM[1]) * SCALE
  ];
}

function modelVector(vec) {
  return [vec[0], vec[2], vec[1]];
}

function addVec(a, b) { return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]; }
function subVec(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
function mulVec(a, s) { return [a[0] * s, a[1] * s, a[2] * s]; }
function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
function cross(a, b) {
  return [
    a[1] * b[2] - a[2] * b[1],
    a[2] * b[0] - a[0] * b[2],
    a[0] * b[1] - a[1] * b[0]
  ];
}
function normalize(v) {
  const len = Math.hypot(v[0], v[1], v[2]) || 1;
  return [v[0] / len, v[1] / len, v[2] / len];
}

function pushVertex(out, p, n, color) {
  out.positions.push(p[0], p[1], p[2]);
  out.normals.push(n[0], n[1], n[2]);
  out.colors.push(color[0], color[1], color[2], color[3]);
}

function pushTriangle(out, a, b, c, normal, color) {
  pushVertex(out, a, normal, color);
  pushVertex(out, b, normal, color);
  pushVertex(out, c, normal, color);
}

function pushLine(out, a, b) {
  out.lines.push(a[0], a[1], a[2], b[0], b[1], b[2]);
}

function addFace(out, a, b, c, d, normal, color) {
  pushTriangle(out, a, b, c, normal, color);
  pushTriangle(out, a, c, d, normal, color);
  pushLine(out, a, b);
  pushLine(out, b, c);
  pushLine(out, c, d);
  pushLine(out, d, a);
}

function boxMesh(part, color) {
  const x0 = part.x;
  const x1 = part.x + part.length;
  const y0 = part.y - part.width / 2;
  const y1 = part.y + part.width / 2;
  const z0 = part.z;
  const z1 = part.z + part.height;
  const p000 = modelToWorld([x0, y0, z0]);
  const p001 = modelToWorld([x0, y0, z1]);
  const p010 = modelToWorld([x0, y1, z0]);
  const p011 = modelToWorld([x0, y1, z1]);
  const p100 = modelToWorld([x1, y0, z0]);
  const p101 = modelToWorld([x1, y0, z1]);
  const p110 = modelToWorld([x1, y1, z0]);
  const p111 = modelToWorld([x1, y1, z1]);
  const out = { positions: [], normals: [], colors: [], lines: [] };
  addFace(out, p100, p110, p111, p101, modelVector([1, 0, 0]), color);
  addFace(out, p000, p001, p011, p010, modelVector([-1, 0, 0]), color);
  addFace(out, p010, p011, p111, p110, modelVector([0, 1, 0]), color);
  addFace(out, p000, p100, p101, p001, modelVector([0, -1, 0]), color);
  addFace(out, p001, p101, p111, p011, modelVector([0, 0, 1]), color);
  addFace(out, p000, p010, p110, p100, modelVector([0, 0, -1]), color);
  return out;
}

function cylinderMesh(part, color, diameter, length, axis) {
  const radius = diameter / 2;
  const center = [part.x, part.y, part.z];
  let axisVec;
  let uVec;
  let vVec;
  if (axis === "x") {
    axisVec = [1, 0, 0]; uVec = [0, 1, 0]; vVec = [0, 0, 1];
  } else if (axis === "y") {
    axisVec = [0, 1, 0]; uVec = [1, 0, 0]; vVec = [0, 0, 1];
  } else {
    axisVec = [0, 0, 1]; uVec = [1, 0, 0]; vVec = [0, 1, 0];
  }
  const startCenter = addVec(center, mulVec(axisVec, -length / 2));
  const endCenter = addVec(center, mulVec(axisVec, length / 2));
  const startWorld = modelToWorld(startCenter);
  const endWorld = modelToWorld(endCenter);
  const axisNormal = normalize(modelVector(axisVec));
  const out = { positions: [], normals: [], colors: [], lines: [] };
  for (let i = 0; i < CYLINDER_SEGMENTS; i++) {
    const a0 = (i / CYLINDER_SEGMENTS) * Math.PI * 2;
    const a1 = ((i + 1) / CYLINDER_SEGMENTS) * Math.PI * 2;
    const radial0 = addVec(mulVec(uVec, Math.cos(a0) * radius), mulVec(vVec, Math.sin(a0) * radius));
    const radial1 = addVec(mulVec(uVec, Math.cos(a1) * radius), mulVec(vVec, Math.sin(a1) * radius));
    const s0 = modelToWorld(addVec(startCenter, radial0));
    const s1 = modelToWorld(addVec(startCenter, radial1));
    const e0 = modelToWorld(addVec(endCenter, radial0));
    const e1 = modelToWorld(addVec(endCenter, radial1));
    const n0 = normalize(modelVector(radial0));
    const n1 = normalize(modelVector(radial1));
    pushTriangle(out, s0, e0, e1, n0, color);
    pushTriangle(out, s0, e1, s1, n1, color);
    pushTriangle(out, startWorld, s1, s0, mulVec(axisNormal, -1), color);
    pushTriangle(out, endWorld, e0, e1, axisNormal, color);
    pushLine(out, s0, s1);
    pushLine(out, e0, e1);
    if (i % 3 === 0) pushLine(out, s0, e0);
  }
  return out;
}

function mergeMesh(target, source) {
  target.positions.push(...source.positions);
  target.normals.push(...source.normals);
  target.colors.push(...source.colors);
  target.lines.push(...source.lines);
}

function buildMesh(part) {
  const color = hexToRgba(part.color, 1);
  const mesh = { positions: [], normals: [], colors: [], lines: [] };
  if (part.kind === "box") {
    mergeMesh(mesh, boxMesh(part, color));
  } else if (part.kind === "cylinder") {
    mergeMesh(mesh, cylinderMesh(part, color, part.diameter, part.length, part.axis));
  } else if (part.kind === "wheel") {
    mergeMesh(mesh, cylinderMesh(part, hexToRgba("#151515", 1), part.diameter, part.width, "y"));
    mergeMesh(mesh, cylinderMesh(part, hexToRgba("#b8b8b8", 1), part.diameter * 0.52, part.width + 8, "y"));
    mergeMesh(mesh, cylinderMesh(part, hexToRgba("#252525", 1), part.diameter * 0.30, part.width + 14, "y"));
  }
  const center = part.kind === "box"
    ? modelToWorld([part.x + part.length / 2, part.y, part.z + part.height / 2])
    : modelToWorld([part.x, part.y, part.z]);
  return { part, mesh, center, group: part.group };
}

const objects = PARTS.map(buildMesh);
const groupStats = new Map();
for (const object of objects) {
  groupStats.set(object.group, (groupStats.get(object.group) || 0) + 1);
}

const vertexShaderSource = `
attribute vec3 aPosition;
attribute vec3 aNormal;
attribute vec4 aColor;
uniform mat4 uMvp;
uniform mat4 uModel;
uniform float uOpacity;
varying vec4 vColor;
varying float vLight;
void main() {
  vec3 n = normalize(mat3(uModel) * aNormal);
  float key = max(dot(n, normalize(vec3(-0.38, 0.72, 0.58))), 0.0);
  float fill = max(dot(n, normalize(vec3(0.55, 0.15, -0.7))), 0.0);
  vLight = 0.32 + 0.58 * key + 0.14 * fill;
  vColor = vec4(aColor.rgb, aColor.a * uOpacity);
  gl_Position = uMvp * uModel * vec4(aPosition, 1.0);
}`;

const fragmentShaderSource = `
precision mediump float;
varying vec4 vColor;
varying float vLight;
void main() {
  gl_FragColor = vec4(vColor.rgb * vLight, vColor.a);
}`;

const lineVertexSource = `
attribute vec3 aPosition;
uniform mat4 uMvp;
uniform mat4 uModel;
void main() {
  gl_Position = uMvp * uModel * vec4(aPosition, 1.0);
}`;

const lineFragmentSource = `
precision mediump float;
uniform vec4 uColor;
void main() { gl_FragColor = uColor; }`;

function shader(type, source) {
  const s = gl.createShader(type);
  gl.shaderSource(s, source);
  gl.compileShader(s);
  if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
    throw new Error(gl.getShaderInfoLog(s));
  }
  return s;
}

function program(vsSource, fsSource) {
  const p = gl.createProgram();
  gl.attachShader(p, shader(gl.VERTEX_SHADER, vsSource));
  gl.attachShader(p, shader(gl.FRAGMENT_SHADER, fsSource));
  gl.linkProgram(p);
  if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
    throw new Error(gl.getProgramInfoLog(p));
  }
  return p;
}

const solidProgram = program(vertexShaderSource, fragmentShaderSource);
const lineProgram = program(lineVertexSource, lineFragmentSource);

function makeBuffer(data) {
  const b = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, b);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data), gl.STATIC_DRAW);
  return b;
}

for (const object of objects) {
  object.positionBuffer = makeBuffer(object.mesh.positions);
  object.normalBuffer = makeBuffer(object.mesh.normals);
  object.colorBuffer = makeBuffer(object.mesh.colors);
  object.lineBuffer = makeBuffer(object.mesh.lines);
  object.vertexCount = object.mesh.positions.length / 3;
  object.lineCount = object.mesh.lines.length / 3;
}

function mat4Multiply(a, b) {
  const out = new Array(16).fill(0);
  for (let col = 0; col < 4; col++) {
    for (let row = 0; row < 4; row++) {
      for (let k = 0; k < 4; k++) {
        out[col * 4 + row] += a[k * 4 + row] * b[col * 4 + k];
      }
    }
  }
  return out;
}

function mat4Perspective(fovy, aspect, near, far) {
  const f = 1 / Math.tan(fovy / 2);
  return [
    f / aspect, 0, 0, 0,
    0, f, 0, 0,
    0, 0, (far + near) / (near - far), -1,
    0, 0, (2 * far * near) / (near - far), 0
  ];
}

function mat4LookAt(eye, center, up) {
  const z = normalize(subVec(eye, center));
  const x = normalize(cross(up, z));
  const y = cross(z, x);
  return [
    x[0], y[0], z[0], 0,
    x[1], y[1], z[1], 0,
    x[2], y[2], z[2], 0,
    -dot(x, eye), -dot(y, eye), -dot(z, eye), 1
  ];
}

function mat4Translate(v) {
  return [
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, 1, 0,
    v[0], v[1], v[2], 1
  ];
}

function transformPoint(m, p) {
  const x = p[0], y = p[1], z = p[2], w = 1;
  const tx = m[0] * x + m[4] * y + m[8] * z + m[12] * w;
  const ty = m[1] * x + m[5] * y + m[9] * z + m[13] * w;
  const tz = m[2] * x + m[6] * y + m[10] * z + m[14] * w;
  const tw = m[3] * x + m[7] * y + m[11] * z + m[15] * w;
  return [tx / tw, ty / tw, tz / tw];
}

function camera() {
  const cosPitch = Math.cos(state.pitch);
  const eye = [
    state.target[0] + Math.sin(state.yaw) * cosPitch * state.distance,
    state.target[1] + Math.sin(state.pitch) * state.distance,
    state.target[2] + Math.cos(state.yaw) * cosPitch * state.distance
  ];
  const view = mat4LookAt(eye, state.target, [0, 1, 0]);
  const proj = mat4Perspective(46 * Math.PI / 180, canvas.width / canvas.height, 0.05, 80);
  return { eye, view, proj, vp: mat4Multiply(proj, view) };
}

function groupOffset(group) {
  const base = GROUP_EXPLODE[group] || [0, 0, 0];
  return mulVec(base, state.explode);
}

function resize() {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const width = Math.max(1, Math.floor(canvas.clientWidth * dpr));
  const height = Math.max(1, Math.floor(canvas.clientHeight * dpr));
  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
  }
  gl.viewport(0, 0, canvas.width, canvas.height);
}

function setAttribute(programObject, name, buffer, size) {
  const loc = gl.getAttribLocation(programObject, name);
  if (loc < 0) return;
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, size, gl.FLOAT, false, 0, 0);
}

function draw() {
  resize();
  gl.clearColor(0.07, 0.08, 0.09, 1);
  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
  gl.enable(gl.DEPTH_TEST);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
  const cam = camera();
  let drawn = 0;

  gl.useProgram(solidProgram);
  const solidMvpLoc = gl.getUniformLocation(solidProgram, "uMvp");
  const solidModelLoc = gl.getUniformLocation(solidProgram, "uModel");
  const opacityLoc = gl.getUniformLocation(solidProgram, "uOpacity");
  gl.uniformMatrix4fv(solidMvpLoc, false, new Float32Array(cam.vp));
  gl.uniform1f(opacityLoc, state.opacity);
  for (const object of objects) {
    if (!state.visible[object.group]) continue;
    const model = mat4Translate(groupOffset(object.group));
    gl.uniformMatrix4fv(solidModelLoc, false, new Float32Array(model));
    setAttribute(solidProgram, "aPosition", object.positionBuffer, 3);
    setAttribute(solidProgram, "aNormal", object.normalBuffer, 3);
    setAttribute(solidProgram, "aColor", object.colorBuffer, 4);
    gl.drawArrays(gl.TRIANGLES, 0, object.vertexCount);
    drawn++;
  }

  if (state.wire) {
    gl.useProgram(lineProgram);
    gl.uniformMatrix4fv(gl.getUniformLocation(lineProgram, "uMvp"), false, new Float32Array(cam.vp));
    gl.uniform4fv(gl.getUniformLocation(lineProgram, "uColor"), new Float32Array([0.02, 0.025, 0.03, 0.34]));
    for (const object of objects) {
      if (!state.visible[object.group]) continue;
      const model = mat4Translate(groupOffset(object.group));
      gl.uniformMatrix4fv(gl.getUniformLocation(lineProgram, "uModel"), false, new Float32Array(model));
      setAttribute(lineProgram, "aPosition", object.lineBuffer, 3);
      gl.drawArrays(gl.LINES, 0, object.lineCount);
    }
  }

  document.getElementById("drawCount").textContent = `${drawn} visible parts`;
  updateHover(cam);
  requestAnimationFrame(draw);
}

function projectToScreen(v, vp) {
  const p = transformPoint(vp, v);
  return [
    (p[0] * 0.5 + 0.5) * canvas.clientWidth,
    (-p[1] * 0.5 + 0.5) * canvas.clientHeight,
    p[2]
  ];
}

function updateHover(cam) {
  let best = null;
  let bestDistance = 18;
  for (const object of objects) {
    if (!state.visible[object.group]) continue;
    const center = addVec(object.center, groupOffset(object.group));
    const screen = projectToScreen(center, cam.vp);
    if (screen[2] < -1 || screen[2] > 1) continue;
    const distance = Math.hypot(screen[0] - state.mouse[0], screen[1] - state.mouse[1]);
    if (distance < bestDistance) {
      bestDistance = distance;
      best = object;
    }
  }
  if (best !== state.hover) {
    state.hover = best;
    renderPartInfo(best);
  }
  const tooltip = document.getElementById("tooltip");
  if (best) {
    tooltip.style.display = "block";
    tooltip.style.left = `${Math.min(state.mouse[0] + 14, canvas.clientWidth - 270)}px`;
    tooltip.style.top = `${Math.max(8, state.mouse[1] + 14)}px`;
    tooltip.textContent = best.part.name.replaceAll("_", " ");
  } else {
    tooltip.style.display = "none";
  }
}

function renderPartInfo(object) {
  const panel = document.getElementById("partInfo");
  if (!object) {
    panel.innerHTML = "<strong>No part selected</strong><span>Move over the model to identify named scaffold parts.</span>";
    return;
  }
  const part = object.part;
  const dims = part.kind === "box"
    ? `${Math.round(part.length)} x ${Math.round(part.width)} x ${Math.round(part.height)} mm`
    : part.kind === "wheel"
      ? `${Math.round(part.diameter)} dia x ${Math.round(part.width)} mm`
      : `${Math.round(part.diameter)} dia x ${Math.round(part.length)} mm`;
  panel.innerHTML = `
    <strong>${part.name.replaceAll("_", " ")}</strong>
    <span class="tag">${part.group.replaceAll("_", " ")}</span>
    <span>${dims}</span>
    <span>${part.confidence}</span>
    <span>${part.notes || ""}</span>
  `;
}

function viewPreset(name) {
  for (const button of document.querySelectorAll("#toolbar button[data-view]")) {
    button.classList.toggle("active", button.dataset.view === name);
  }
  if (name === "iso") {
    state.yaw = -0.82; state.pitch = 0.42; state.distance = 5.9;
  } else if (name === "side") {
    state.yaw = -Math.PI / 2; state.pitch = 0.02; state.distance = 6.2;
  } else if (name === "front") {
    state.yaw = Math.PI; state.pitch = 0.02; state.distance = 5.0;
  } else if (name === "top") {
    state.yaw = -Math.PI / 2; state.pitch = Math.PI / 2 - 0.015; state.distance = 6.0;
  }
  state.target = [0, 0, 0];
}

function buildControls() {
  document.getElementById("partCount").textContent = PARTS.length;
  const groupContainer = document.getElementById("groups");
  const groupColors = new Map();
  for (const part of PARTS) {
    if (!groupColors.has(part.group)) groupColors.set(part.group, part.color);
  }
  for (const group of GROUP_ORDER.filter((name) => groupStats.has(name))) {
    const label = document.createElement("label");
    label.className = "group";
    label.innerHTML = `
      <input type="checkbox" checked data-group="${group}">
      <span class="swatch" style="background:${groupColors.get(group)}"></span>
      <span class="group-name">${group.replaceAll("_", " ")}</span>
      <span class="count">${groupStats.get(group)}</span>
    `;
    groupContainer.appendChild(label);
  }
  groupContainer.addEventListener("change", (event) => {
    const input = event.target;
    if (input && input.dataset && input.dataset.group) {
      state.visible[input.dataset.group] = input.checked;
    }
  });
  document.getElementById("explode").addEventListener("input", (event) => {
    state.explode = Number(event.target.value) / 100;
  });
  document.getElementById("opacity").addEventListener("input", (event) => {
    state.opacity = Number(event.target.value) / 100;
  });
  document.getElementById("wire").addEventListener("change", (event) => {
    state.wire = event.target.checked;
  });
  document.getElementById("resetView").addEventListener("click", () => viewPreset("iso"));
  for (const button of document.querySelectorAll("#toolbar button[data-view]")) {
    button.addEventListener("click", () => viewPreset(button.dataset.view));
  }
}

let dragging = false;
let dragMode = "orbit";
let last = [0, 0];
canvas.addEventListener("contextmenu", (event) => event.preventDefault());
canvas.addEventListener("pointerdown", (event) => {
  dragging = true;
  dragMode = event.shiftKey || event.button === 2 ? "pan" : "orbit";
  last = [event.clientX, event.clientY];
  canvas.setPointerCapture(event.pointerId);
});
canvas.addEventListener("pointermove", (event) => {
  const rect = canvas.getBoundingClientRect();
  state.mouse = [event.clientX - rect.left, event.clientY - rect.top];
  if (!dragging) return;
  const dx = event.clientX - last[0];
  const dy = event.clientY - last[1];
  last = [event.clientX, event.clientY];
  if (dragMode === "orbit") {
    state.yaw += dx * 0.006;
    state.pitch = Math.max(-1.45, Math.min(1.45, state.pitch + dy * 0.006));
  } else {
    const panScale = state.distance * 0.0015;
    state.target[0] -= dx * panScale;
    state.target[1] += dy * panScale;
  }
});
canvas.addEventListener("pointerup", (event) => {
  dragging = false;
  try { canvas.releasePointerCapture(event.pointerId); } catch (_) {}
});
canvas.addEventListener("wheel", (event) => {
  event.preventDefault();
  state.distance = Math.max(2.2, Math.min(13, state.distance * Math.exp(event.deltaY * 0.001)));
}, { passive: false });

buildControls();
requestAnimationFrame(draw);
</script>
</body>
</html>
"""
)


def write_viewer() -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html = HTML_TEMPLATE.safe_substitute(
        PARTS_JSON=json.dumps(part_payload(), separators=(",", ":")),
        MODEL_TITLE=MODEL_TITLE,
    )
    OUT_PATH.write_text(html, encoding="utf-8")
    return OUT_PATH


def main() -> None:
    print(write_viewer().relative_to(ROOT))


if __name__ == "__main__":
    main()
