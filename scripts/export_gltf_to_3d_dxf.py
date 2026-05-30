#!/usr/bin/env python3
"""Export a glTF 2.0 triangle scene to an AutoCAD-friendly 3D DXF.

The output uses 3DFACE entities in millimetres. It is intentionally aimed at
the generated J40 scaffold and shares the glTF parsing helpers used by the OBJ
exporter.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from export_gltf_to_obj import (
    accessor_values,
    clean_name,
    identity_matrix,
    iter_node_tree,
    load_buffers,
    material_name,
    scene_nodes,
    transform_point,
    triangle_indices,
)


MATERIAL_ACI = {
    "body_sand": 40,
    "body_shadow": 8,
    "body_highlight": 50,
    "roof_white": 7,
    "black_trim": 250,
    "frame": 251,
    "rubber": 250,
    "metal": 9,
    "chrome": 9,
    "interior": 30,
    "glass": 4,
    "glass_dark": 151,
    "engine": 8,
    "spring": 250,
    "reference": 7,
    "electrical": 1,
    "amber": 30,
    "grille_yellow": 2,
    "fluid": 3,
    "brass": 30,
    "datum": 5,
}


def dxf_num(value: float) -> str:
    return f"{value:.6f}".rstrip("0").rstrip(".") or "0"


def dxf_pair(code: int | str, value: int | float | str) -> list[str]:
    if isinstance(value, float):
        return [str(code), dxf_num(value)]
    return [str(code), str(value)]


def layer_name(group_name: str, object_name: str) -> str:
    prefix = clean_name(group_name, "model")
    suffix = clean_name(object_name, "part")
    name = f"{prefix}__{suffix}"
    return name[:240].rstrip("._-") or "model"


def triangle_area_mm2(points: tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]) -> float:
    a, b, c = points
    ab = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    ac = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    cross = (
        ab[1] * ac[2] - ab[2] * ac[1],
        ab[2] * ac[0] - ab[0] * ac[2],
        ab[0] * ac[1] - ab[1] * ac[0],
    )
    return 0.5 * math.sqrt(cross[0] ** 2 + cross[1] ** 2 + cross[2] ** 2)


def material_color_index(gltf: dict, material_index: int | None) -> int:
    if material_index is None:
        return 7
    name = material_name(gltf, material_index)
    if name in MATERIAL_ACI:
        return MATERIAL_ACI[name]
    return 7


def collect_faces(source_path: Path, scale: float) -> tuple[list[dict[str, object]], dict[str, int], dict[str, int]]:
    gltf = json.loads(source_path.read_text(encoding="utf-8"))
    buffers = load_buffers(gltf, source_path)
    faces: list[dict[str, object]] = []
    layer_colors: dict[str, int] = {}
    stats = {
        "objects": 0,
        "faces": 0,
        "skipped_primitives": 0,
        "skipped_degenerate_faces": 0,
    }

    for _, node, world_matrix in iter_node_tree(gltf, scene_nodes(gltf), identity_matrix()):
        if "mesh" not in node:
            continue
        mesh = gltf["meshes"][node["mesh"]]
        object_name = clean_name(node.get("name") or mesh.get("name", ""), f"mesh_{node['mesh']}")
        group_name = clean_name(node.get("extras", {}).get("group", object_name), object_name)
        layer = layer_name(group_name, object_name)
        stats["objects"] += 1

        for primitive in mesh.get("primitives", []):
            mode = primitive.get("mode", 4)
            if mode not in {4, 5, 6}:
                stats["skipped_primitives"] += 1
                continue

            attrs = primitive["attributes"]
            positions = accessor_values(gltf, buffers, attrs["POSITION"])
            indices = (
                accessor_values(gltf, buffers, primitive["indices"])
                if "indices" in primitive
                else list(range(len(positions)))
            )
            layer_colors.setdefault(layer, material_color_index(gltf, primitive.get("material")))

            for a, b, c in triangle_indices(mode, indices):
                points = tuple(
                    tuple(axis * scale for axis in transform_point(world_matrix, positions[index]))
                    for index in (a, b, c)
                )
                if triangle_area_mm2(points) < 0.0001:
                    stats["skipped_degenerate_faces"] += 1
                    continue
                faces.append(
                    {
                        "layer": layer,
                        "object": object_name,
                        "group": group_name,
                        "points": points,
                    }
                )
                stats["faces"] += 1

    return faces, layer_colors, stats


def write_dxf(output_path: Path, faces: list[dict[str, object]], layer_colors: dict[str, int]) -> None:
    coords = [
        coordinate
        for face in faces
        for point in face["points"]  # type: ignore[index]
        for coordinate in point
    ]
    ext_min = [min(coords[index::3]) for index in range(3)] if coords else [0.0, 0.0, 0.0]
    ext_max = [max(coords[index::3]) for index in range(3)] if coords else [0.0, 0.0, 0.0]
    lines: list[str] = [
        "999",
        "Generated 3D DXF from J40 glTF scaffold. Units are millimetres.",
        "0",
        "SECTION",
        "2",
        "HEADER",
        *dxf_pair(9, "$ACADVER"),
        *dxf_pair(1, "AC1015"),
        *dxf_pair(9, "$INSUNITS"),
        *dxf_pair(70, 4),
        *dxf_pair(9, "$MEASUREMENT"),
        *dxf_pair(70, 1),
        *dxf_pair(9, "$EXTMIN"),
        *dxf_pair(10, ext_min[0]),
        *dxf_pair(20, ext_min[1]),
        *dxf_pair(30, ext_min[2]),
        *dxf_pair(9, "$EXTMAX"),
        *dxf_pair(10, ext_max[0]),
        *dxf_pair(20, ext_max[1]),
        *dxf_pair(30, ext_max[2]),
        "0",
        "ENDSEC",
        "0",
        "SECTION",
        "2",
        "TABLES",
        "0",
        "TABLE",
        "2",
        "LAYER",
        "70",
        str(len(layer_colors) + 1),
        "0",
        "LAYER",
        "2",
        "0",
        "70",
        "0",
        "62",
        "7",
        "6",
        "CONTINUOUS",
    ]
    for layer in sorted(layer_colors):
        lines.extend(
            [
                "0",
                "LAYER",
                "2",
                layer,
                "70",
                "0",
                "62",
                str(layer_colors[layer]),
                "6",
                "CONTINUOUS",
            ]
        )
    lines.extend(["0", "ENDTAB", "0", "ENDSEC", "0", "SECTION", "2", "ENTITIES"])

    last_object = ""
    for face in faces:
        object_name = str(face["object"])
        if object_name != last_object:
            lines.extend(["999", f"object {object_name}"])
            last_object = object_name
        points = face["points"]  # type: ignore[assignment]
        p1, p2, p3 = points
        p4 = p3
        lines.extend(
            [
                "0",
                "3DFACE",
                "8",
                str(face["layer"]),
                *dxf_pair(10, p1[0]),
                *dxf_pair(20, p1[1]),
                *dxf_pair(30, p1[2]),
                *dxf_pair(11, p2[0]),
                *dxf_pair(21, p2[1]),
                *dxf_pair(31, p2[2]),
                *dxf_pair(12, p3[0]),
                *dxf_pair(22, p3[1]),
                *dxf_pair(32, p3[2]),
                *dxf_pair(13, p4[0]),
                *dxf_pair(23, p4[1]),
                *dxf_pair(33, p4[2]),
            ]
        )

    lines.extend(["0", "ENDSEC", "0", "EOF"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Input glTF file")
    parser.add_argument("output", type=Path, help="Output 3D DXF file")
    parser.add_argument("--scale", type=float, default=1000.0, help="coordinate scale; default converts generated metres to millimetres")
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    faces, layer_colors, stats = collect_faces(source, args.scale)
    write_dxf(output, faces, layer_colors)
    print(
        "Exported {objects} objects, {faces} 3DFACE entities across {layers} layers "
        "to {output}".format(output=output, layers=len(layer_colors), **stats)
    )
    if stats["skipped_primitives"]:
        print(f"Skipped {stats['skipped_primitives']} unsupported primitives")
    if stats["skipped_degenerate_faces"]:
        print(f"Skipped {stats['skipped_degenerate_faces']} degenerate faces")


if __name__ == "__main__":
    main()
