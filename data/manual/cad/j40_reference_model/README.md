# J40 Reference Model CAD Intake

This folder is for the open-source Sketchfab Toyota Land Cruiser FJ40 model selected as the starting reference:

- Source page: https://sketchfab.com/3d-models/1976-toyota-land-cruiser-fj40-a4e58b09ce48444ca6164834c310880d
- Author: tonielpro520
- License: Creative Commons Attribution 4.0 (CC BY 4.0); author credit required; commercial use is allowed.
- Intended use here: reference mesh, packaging study, and manual remodelling into measured CAD parts.

## Folder Layout

- `00_inbox/`: put the downloaded Sketchfab ZIP here.
- `01_source_mesh/`: extracted source mesh files.
- `02_mesh_clean/`: repaired or simplified mesh exports from MeshLab/Blender.
- `03_freecad/`: FreeCAD `.FCStd` working files.
- `04_exports/`: OpenSCAD, FreeCAD macro, glTF, SVG/PNG, and supporting open exchange exports.
- `05_reports/`: generated inventory and status reports.

Large model files are intentionally ignored by git. Keep only small metadata, scripts, and notes in version control.

## First Run

After downloading the source model ZIP from Sketchfab while logged in, run:

```bash
python3 scripts/j40_cad_intake.py
```

Then inspect `05_reports/source_model_inventory.md` and decide which mesh pieces are useful enough to convert or remodel.

## FreeCAD Mesh Conversion

The supplied FreeCAD script can convert a mesh into a STEP/FCStd reference body:

```bash
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd scripts/freecad_mesh_to_cad.py \
  --source-dir data/manual/cad/j40_reference_model/02_mesh_clean \
  --out-dir data/manual/cad/j40_reference_model/03_freecad
```

This is not a true parametric remodel. It creates CAD containers around mesh-derived faces. Use it for reference, then rebuild real fabrication parts as sketches, pads, revolves, sweeps, sheet metal, or assemblies.

## Open 3D Viewing

Open this generated file in any glTF 2.0 viewer for a vendor-neutral 3D reference:

```text
data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_scaffold_rev_c.gltf
```

It is mesh geometry exported from the project-owned right-hand-drive scaffold in metre units. It is for visual inspection and packaging, not release-grade fabrication geometry.

The generated orbit viewer includes part search, part focus, single-part isolation, group toggles, classic rounded rear/back window geometry, and a cabin preset for zooming into the right-hand-drive interior.

Published Rev C viewer:

```text
https://dbvg4yfpnc4tj.cloudfront.net/data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_orbit_viewer.html
```
