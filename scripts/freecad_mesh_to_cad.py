from __future__ import annotations

import argparse
from pathlib import Path
import re

import FreeCAD as App
import Mesh
import Part


MESH_EXTS = {".obj", ".stl", ".ply"}


def safe_name(path: Path) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", path.stem).strip("_") or "mesh_reference"


def convert_mesh(mesh_path: Path, out_dir: Path, tolerance: float, max_faces: int | None) -> dict[str, object]:
    mesh = Mesh.Mesh(str(mesh_path))
    face_count = mesh.CountFacets
    if max_faces is not None and face_count > max_faces:
        return {
            "mesh": str(mesh_path),
            "status": "skipped",
            "reason": f"{face_count} mesh faces exceeds --max-faces {max_faces}",
        }

    name = safe_name(mesh_path)
    doc = App.newDocument(name)
    mesh_obj = doc.addObject("Mesh::Feature", f"{name}_source_mesh")
    mesh_obj.Mesh = mesh

    shape = Part.Shape()
    shape.makeShapeFromMesh(mesh.Topology, tolerance)

    body_obj = doc.addObject("Part::Feature", f"{name}_mesh_shape")
    try:
        shell = Part.makeShell(shape.Faces)
        solid = Part.makeSolid(shell)
        body_obj.Shape = solid.removeSplitter()
        body_kind = "solid"
    except Exception:
        body_obj.Shape = shape
        body_kind = "shell"

    doc.recompute()
    out_dir.mkdir(parents=True, exist_ok=True)
    fcstd_path = out_dir / f"{name}.FCStd"
    step_path = out_dir / f"{name}.step"
    brep_path = out_dir / f"{name}.brep"

    doc.saveAs(str(fcstd_path))
    Part.export([body_obj], str(step_path))
    body_obj.Shape.exportBrep(str(brep_path))
    App.closeDocument(doc.Name)

    return {
        "mesh": str(mesh_path),
        "status": "converted",
        "faces": face_count,
        "body_kind": body_kind,
        "fcstd": str(fcstd_path),
        "step": str(step_path),
        "brep": str(brep_path),
    }


def source_meshes(source_dir: Path) -> list[Path]:
    if source_dir.is_file() and source_dir.suffix.lower() in MESH_EXTS:
        return [source_dir]
    return sorted(path for path in source_dir.rglob("*") if path.is_file() and path.suffix.lower() in MESH_EXTS)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert cleaned mesh files into FreeCAD reference CAD files.")
    parser.add_argument("--source-dir", required=True, help="mesh file or directory containing OBJ/STL/PLY files")
    parser.add_argument("--out-dir", required=True, help="output directory for FCStd/STEP/BREP files")
    parser.add_argument("--tolerance", type=float, default=0.10, help="mesh to shape tolerance in model units")
    parser.add_argument("--max-faces", type=int, default=80000, help="skip meshes above this face count; use 0 for no limit")
    args = parser.parse_args()

    max_faces = None if args.max_faces == 0 else args.max_faces
    meshes = source_meshes(Path(args.source_dir))
    if not meshes:
        raise SystemExit(f"No supported mesh files found under {args.source_dir}")

    for mesh_path in meshes:
        result = convert_mesh(mesh_path, Path(args.out_dir), args.tolerance, max_faces)
        print(result)


if __name__ == "__main__":
    main()

