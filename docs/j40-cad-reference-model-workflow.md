# J40 CAD Reference Model Workflow

## Current Setup

- FreeCAD 1.1.1 is installed at `/Applications/FreeCAD.app`.
- MeshLab 2025.07 is installed at `/Applications/MeshLab2025.07.app`.
- CloudCompare was downloaded as a source archive, not an installable app bundle.
- Blender was not found in `/Applications` or on `PATH`.
- The selected Sketchfab model is not yet present in the repo or `Downloads`; Sketchfab requires a logged-in download.
- A project-owned Rev A scaffold has been generated while waiting for the licensed ZIP.

## Source Asset

- Model: Toyota Land Cruiser FJ40 SoftTopInterior&Chassis
- URL: https://sketchfab.com/3d-models/toyota-land-cruiser-fj40-softtopinteriorchassis-aaf9547c5e8b478abd2ceb47f1f82340
- Author: dragosburian
- License: purchased/licensed project use; retain the original license terms with the downloaded asset.

## Intake Steps

1. Download the licensed model ZIP from Sketchfab/Fab while logged in.
2. Put the ZIP in `data/manual/cad/j40_reference_model/00_inbox/`.
3. Run `python3 scripts/j40_cad_intake.py`.
4. Review `data/manual/cad/j40_reference_model/05_reports/source_model_inventory.md`.
5. Use MeshLab or Blender to split, repair, and simplify the mesh into logical parts.
6. Put cleaned OBJ/STL/PLY files in `data/manual/cad/j40_reference_model/02_mesh_clean/`.
7. Run FreeCAD conversion on cleaned parts only.

## Generated Scaffold

The current scaffold is not a direct copy or extraction of the paid model. It is a parametric vehicle-scale reference built from published FJ40 dimensions and visible reference features.

- OpenSCAD source: `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_a/j40_full_vehicle_scaffold_rev_a.scad`
- FreeCAD macro: `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_a/j40_full_vehicle_scaffold_rev_a.FCMacro`
- Orthographic SVG/PNG/DXF: `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_a/`
- Part inventory: `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_a/j40_full_vehicle_scaffold_rev_a_parts.csv`

## FreeCAD Auto-Update

Run this macro in the FreeCAD GUI:

```text
/Users/davidpridmore/IdeaProjects/J40/data/manual/cad/j40_reference_model/freecad/J40ReferenceModelAutoUpdate.FCMacro
```

It refreshes the repo-generated CAD files, loads the generated scaffold macro, and starts a 30 second timer. When the licensed ZIP, cleaned meshes, or generator scripts change, the open FreeCAD view rebuilds on the next timer tick.

When real source geometry is present, the loader also runs:

```text
data/manual/cad/j40_reference_model/04_exports/source_mesh_reference/j40_source_mesh_reference.FCMacro
```

That macro loads source OBJ/STL/PLY files into the same FreeCAD document as transparent licensed-reference geometry. The scaffold remains as editable CAD until each source-derived part is remodelled properly.

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
- fuel tank, battery, fuse/relay board, HVAC, and loom routing envelopes
- spring hanger, shackle, bumper, and bracket hard points

Physical measurements from the actual truck remain the source of truth.
