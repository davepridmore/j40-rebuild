# FreeCAD Auto-Update Setup

Use `J40ReferenceModelAutoUpdate.FCMacro` in the FreeCAD GUI.

What it does:

- Runs `scripts/update_j40_cad_reference.py --skip-if-unchanged`.
- Loads the generated `j40_full_vehicle_scaffold_rev_a.FCMacro`.
- Loads any extracted/source OBJ, STL, or PLY files through `j40_source_mesh_reference.FCMacro`.
- Rebuilds the FreeCAD document when the update stamp changes.
- Starts a 30 second GUI timer, so the open FreeCAD view refreshes after the source ZIP, cleaned meshes, or generator scripts change.

The macro does not require FreeCAD's command-line binary, which currently fails in the Codex shell on this machine.

## Manual Use

1. Open FreeCAD.
2. Open Macro Manager.
3. Run:

```text
/Users/davidpridmore/IdeaProjects/J40/data/manual/cad/j40_reference_model/freecad/J40ReferenceModelAutoUpdate.FCMacro
```

## Background Repo Watcher

For a Terminal-side watcher independent of FreeCAD:

```bash
python3 scripts/watch_j40_cad_reference.py --interval 10
```

The watcher refreshes the intake inventory and generated CAD files whenever the repo inputs change.

## Source File Rule

The rebuild is source-file driven. The viewer page is only reference. Put the licensed ZIP or extracted mesh files in:

```text
/Users/davidpridmore/IdeaProjects/J40/data/manual/cad/j40_reference_model/00_inbox/
```

OBJ, STL, and PLY files are loaded directly in FreeCAD. BLEND, DAE, FBX, GLB, and GLTF are inventoried as needing conversion first.
