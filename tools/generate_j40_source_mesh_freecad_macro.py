from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import re


ROOT = Path(__file__).resolve().parent.parent
CAD_ROOT = ROOT / "data" / "manual" / "cad" / "j40_reference_model"
OUT_DIR = CAD_ROOT / "04_exports" / "source_mesh_reference"
REPORT_DIR = CAD_ROOT / "05_reports"

SOURCE_DIRS = [
    CAD_ROOT / "00_inbox",
    CAD_ROOT / "01_source_mesh",
    CAD_ROOT / "02_mesh_clean",
]

FREECAD_MESH_EXTS = {".obj", ".stl", ".ply"}
KNOWN_BUT_SKIPPED_EXTS = {".blend", ".dae", ".fbx", ".glb", ".gltf", ".usd", ".usdz"}


@dataclass(frozen=True)
class SourceFile:
    path: Path
    status: str
    reason: str


def safe_name(path: Path) -> str:
    name = re.sub(r"[^A-Za-z0-9_]+", "_", path.stem).strip("_")
    return name[:80] or "source_mesh"


def source_files() -> list[SourceFile]:
    files: list[SourceFile] = []
    seen: set[Path] = set()
    for source_dir in SOURCE_DIRS:
        if not source_dir.exists():
            continue
        for path in sorted(source_dir.rglob("*")):
            if not path.is_file() or path.name == ".gitkeep":
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            suffix = path.suffix.lower()
            if suffix in FREECAD_MESH_EXTS:
                files.append(SourceFile(path, "freecad_mesh_load", "loadable by generated FreeCAD macro"))
            elif suffix in KNOWN_BUT_SKIPPED_EXTS:
                files.append(SourceFile(path, "needs_conversion", "convert to OBJ/STL/PLY first"))
    return files


def write_inventory(files: list[SourceFile]) -> Path:
    path = REPORT_DIR / "j40_source_mesh_reference_inventory.csv"
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "size_bytes", "status", "reason"])
        for source_file in files:
            writer.writerow(
                [
                    source_file.path.relative_to(ROOT),
                    source_file.path.stat().st_size,
                    source_file.status,
                    source_file.reason,
                ]
            )
    return path


def write_notes(files: list[SourceFile], macro_path: Path) -> Path:
    path = REPORT_DIR / "j40_source_mesh_reference_notes.md"
    loadable = [item for item in files if item.status == "freecad_mesh_load"]
    skipped = [item for item in files if item.status != "freecad_mesh_load"]
    lines = [
        "# J40 Source Mesh Reference",
        "",
        "This report describes the locally available CC-BY/open-source reference geometry that the FreeCAD loader can use.",
        "",
        f"- Loadable mesh files: {len(loadable)}",
        f"- Files needing conversion: {len(skipped)}",
        f"- Generated macro: `{macro_path.relative_to(ROOT)}`",
        "",
    ]
    if loadable:
        lines.extend(["## Loadable In FreeCAD", ""])
        for item in loadable:
            lines.append(f"- `{item.path.relative_to(ROOT)}`")
        lines.append("")
    if skipped:
        lines.extend(["## Needs Conversion First", ""])
        for item in skipped:
            lines.append(f"- `{item.path.relative_to(ROOT)}`: {item.reason}")
        lines.append("")
    if not files:
        lines.extend(
            [
                "No CC-BY source geometry is present yet.",
                "",
                "Put the downloaded Sketchfab ZIP or extracted OBJ/STL/PLY files in `data/manual/cad/j40_reference_model/00_inbox/`.",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="ascii")
    return path


def write_freecad_macro(files: list[SourceFile]) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    macro_path = OUT_DIR / "j40_source_mesh_reference.FCMacro"
    loadable = [item for item in files if item.status == "freecad_mesh_load"]

    lines = [
        "# Generated J40 source-mesh reference loader.",
        "# Run after the scaffold macro; it adds CC-BY reference meshes to the active FreeCAD document.",
        "from pathlib import Path",
        "import FreeCAD as App",
        "import Mesh",
        "",
        "try:",
        "    import FreeCADGui as Gui",
        "except Exception:",
        "    Gui = None",
        "",
        "doc = App.ActiveDocument or App.newDocument('j40_source_mesh_reference')",
        "group = doc.getObject('cc_by_source_mesh_reference')",
        "if group is None:",
        "    group = doc.addObject('App::DocumentObjectGroup', 'cc_by_source_mesh_reference')",
        "",
        "def add_mesh(name, path):",
        "    if doc.getObject(name) is not None:",
        "        doc.removeObject(name)",
        "    obj = doc.addObject('Mesh::Feature', name)",
        "    obj.Mesh = Mesh.Mesh(str(path))",
        "    group.addObject(obj)",
        "    if hasattr(obj, 'ViewObject'):",
        "        obj.ViewObject.ShapeColor = (1.0, 0.72, 0.18)",
        "        obj.ViewObject.Transparency = 45",
        "    return obj",
        "",
    ]

    if not loadable:
        lines.append("App.Console.PrintMessage('No loadable J40 source mesh files found yet.\\n')")
    else:
        lines.append(f"App.Console.PrintMessage('Loading {len(loadable)} J40 source mesh file(s).\\n')")
        used_names: set[str] = set()
        for idx, item in enumerate(loadable, start=1):
            name = safe_name(item.path)
            if name in used_names:
                name = f"{name}_{idx}"
            used_names.add(name)
            lines.append(f"add_mesh({name!r}, Path({str(item.path)!r}))")

    lines.extend(
        [
            "",
            "doc.recompute()",
            "if Gui is not None:",
            "    Gui.SendMsgToActiveView('ViewFit')",
            "",
        ]
    )
    macro_path.write_text("\n".join(lines), encoding="ascii")
    return macro_path


def main() -> None:
    files = source_files()
    macro_path = write_freecad_macro(files)
    inventory_path = write_inventory(files)
    notes_path = write_notes(files, macro_path)
    print(macro_path.relative_to(ROOT))
    print(inventory_path.relative_to(ROOT))
    print(notes_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
