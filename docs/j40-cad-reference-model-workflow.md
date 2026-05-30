# J40 CAD Reference Model Workflow

## Current Setup

- FreeCAD 1.1.1 is installed at `/Applications/FreeCAD.app`.
- MeshLab 2025.07 is installed at `/Applications/MeshLab2025.07.app`.
- CloudCompare was downloaded as a source archive, not an installable app bundle.
- Blender was not found in `/Applications` or on `PATH`.
- The selected Sketchfab model is a downloadable CC-BY reference, but the source archive still requires a logged-in Sketchfab download.
- A project-owned Rev C right-hand-drive scaffold now layers open-source references, commercial/online 3D representations covered for project use, Toyota parts representations, and the actual project photos into one procedural reference model.

## Source Asset

- Model: 1976 Toyota Land Cruiser FJ40
- URL: https://sketchfab.com/3d-models/1976-toyota-land-cruiser-fj40-a4e58b09ce48444ca6164834c310880d
- Author: tonielpro520
- License: Creative Commons Attribution 4.0 (CC BY 4.0); author credit required; commercial use is allowed.
- Sketchfab API facts captured 2026-05-29: downloadable, 96,681 vertices, 177,769 faces, 31 materials, 3 textures.

## Intake Steps

1. Download the source model ZIP from Sketchfab while logged in.
2. Put the ZIP in `data/manual/cad/j40_reference_model/00_inbox/`.
3. Run `python3 scripts/j40_cad_intake.py`.
4. Review `data/manual/cad/j40_reference_model/05_reports/source_model_inventory.md`.
5. Use MeshLab or Blender to split, repair, and simplify the mesh into logical parts.
6. Put cleaned OBJ/STL/PLY files in `data/manual/cad/j40_reference_model/02_mesh_clean/`.
7. Run FreeCAD conversion on cleaned parts only.

## Generated Scaffold

The current scaffold is not a direct copy or extraction of the Sketchfab model or any commercial model. It is a from-scratch parametric vehicle-scale reference built from representative FJ40 dimensions, CC-BY hardtop references, commercial/online model representations, Toyota parts representations, and project photos of the actual beige diesel hardtop truck.

- OpenSCAD source: `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_scaffold_rev_c.scad`
- FreeCAD macro: `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_scaffold_rev_c.FCMacro`
- Open 3D exchange: `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_scaffold_rev_c.gltf`
- Orbit viewer: `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_orbit_viewer.html`
- Orthographic SVG/PNG/DXF: `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/`
- Part inventory: `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_scaffold_rev_c_parts.csv`
- Online reference inventory: `data/manual/cad/j40_reference_model/05_reports/j40_full_vehicle_scaffold_rev_c_online_reference_inventory.csv`

The FreeCAD macro groups the model into chassis, running gear, body, front detail, hardtop, engine bay, interior, brake system, fuel system, exhaust, and datum references. It includes project-specific visual cues: sand/beige body, white hardtop roof, black bumpers/trim, hardtop side windows, classic rounded rear-quarter/back-door glazing, side step boards, diesel/fuel-filler references, mud-terrain tire lugs, rear parking-brake cable attachment hardware, right-hand-drive steering/pedal/firewall references, Rev C roof/rear ventilator detail, body mounts, bumper stays, tri-color rear lamp segmentation, hood underside/prop hardware, brake/fuel routing, and interior gauge/grab-handle detail.

The as-fitted route scope is now part of the CAD workflow. Use [j40-digital-twin-as-fitted-cable-scope-20260531.md](j40-digital-twin-as-fitted-cable-scope-20260531.md) and `data/manual/cad/j40_reference_model/05_reports/j40_as_fitted_route_model_scope_20260531.csv` to drive every cable, loom, hose, hard line, control cable, earth strap, A/C hose, brake/fuel line, and drivetrain-orientation verification into named model geometry. Route placeholders are visual only until the actual truck supplies endpoints, pass-throughs, supports, bend radius, and clearance measurements.

A left-hand-drive driver-side review variant is generated beside the RHD base under `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c_lhd_review/`. Use it only as a swap/packaging comparison. The RHD `scaffold_rev_c` model remains the default as-fitted truth model until the actual truck measurements prove a control-side swap.

For quick visual inspection, open the orbit viewer in a browser. It is self-contained and supports orbit, zoom, pan, group visibility toggles, exploded view, wire overlay, hover part readout, part search, part focus, single-part isolation, and a cabin preset for right-hand-drive interior inspection.

Published Rev C viewer: https://dbvg4yfpnc4tj.cloudfront.net/data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_orbit_viewer.html

Published dashboard: https://dbvg4yfpnc4tj.cloudfront.net/docs/project-control-ui/#vehicle-map

For open interchange, use the glTF file. It stores the full scaffold as vendor-neutral mesh geometry in metres, with group nodes for body, chassis, running gear, hardtop, engine bay, interior, brake system, fuel system, exhaust, and datum references.

## FreeCAD Auto-Update

Run this macro in the FreeCAD GUI:

```text
/Users/davidpridmore/IdeaProjects/J40/data/manual/cad/j40_reference_model/freecad/J40ReferenceModelAutoUpdate.FCMacro
```

It refreshes the repo-generated CAD files, loads the generated scaffold macro, and starts a 30 second timer. When the CC-BY ZIP, cleaned meshes, or generator scripts change, the open FreeCAD view rebuilds on the next timer tick.

When source/reference geometry is present, the loader also runs:

```text
data/manual/cad/j40_reference_model/04_exports/source_mesh_reference/j40_source_mesh_reference.FCMacro
```

That macro loads source OBJ/STL/PLY files into the same FreeCAD document as transparent CC-BY reference geometry. The scaffold remains editable CAD until each useful part is remodelled properly from measurements.

## Conversion Command

```bash
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd scripts/freecad_mesh_to_cad.py \
  --source-dir data/manual/cad/j40_reference_model/02_mesh_clean \
  --out-dir data/manual/cad/j40_reference_model/03_freecad \
  --tolerance 0.10 \
  --max-faces 80000
```

If a cleaned mesh is still too heavy, raise `--max-faces` or decimate/split it first. Avoid converting the entire vehicle as one body.

Note: the FreeCAD command-line binary exists, but in the Codex shell it currently exits with `Incompatible processor. This Qt build requires the following features: neon`. If that also happens in a normal Terminal, use the FreeCAD GUI for import/export or install a build that matches the machine/runtime.

## What "Full CAD" Means Here

The downloaded model is a visual mesh. A direct STEP export from it is only a CAD wrapper around triangles. For a fabrication-grade model, use the mesh as a spatial reference and rebuild the parts that matter as measured CAD:

- chassis rails and crossmember reference envelope
- body tub, firewall, floor, and transmission tunnel reference planes
- dashboard and steering column packaging
- seat and belt mounting zones
- fuel tank, battery, fuse/relay board, HVAC, and all as-fitted loom/cable/hose/line routing envelopes
- spring hanger, shackle, bumper, and bracket hard points
- drivetrain orientation, prop-shaft route, axle differential offsets, and steering linkage orientation checked against the actual truck

Physical measurements from the actual truck remain the source of truth.
