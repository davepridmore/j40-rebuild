# J40 Reference Model CAD Intake

This folder is for the licensed Sketchfab Toyota Land Cruiser FJ40 model selected as the starting reference:

- Source page: https://sketchfab.com/3d-models/toyota-land-cruiser-fj40-softtopinteriorchassis-aaf9547c5e8b478abd2ceb47f1f82340
- Author: dragosburian
- License: purchased/licensed project use; retain the original license terms with the downloaded asset.
- Intended use here: reference mesh, packaging study, and manual remodelling into measured CAD parts.

## Folder Layout

- `00_inbox/`: put the downloaded Sketchfab ZIP here.
- `01_source_mesh/`: extracted source mesh files.
- `02_mesh_clean/`: repaired or simplified mesh exports from MeshLab/Blender.
- `03_freecad/`: FreeCAD `.FCStd` working files.
- `04_exports/`: STEP/STL/DXF exports made from CAD work.
- `05_reports/`: generated inventory and status reports.

Large model files are intentionally ignored by git. Keep only small metadata, scripts, and notes in version control.

## First Run

After downloading the licensed model ZIP from Sketchfab/Fab, run:

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
