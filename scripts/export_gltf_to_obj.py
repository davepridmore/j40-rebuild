#!/usr/bin/env python3
"""Export a glTF 2.0 mesh scene to Wavefront OBJ/MTL.

This intentionally handles the subset used by the generated J40 scaffold:
embedded or external buffers, triangle primitives, POSITION/NORMAL accessors,
materials with PBR base colors, and ordinary glTF node transforms.
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import re
import struct
from pathlib import Path
from typing import Iterable


TYPE_COMPONENTS = {
    "SCALAR": 1,
    "VEC2": 2,
    "VEC3": 3,
    "VEC4": 4,
    "MAT4": 16,
}

COMPONENT_FORMATS = {
    5120: "b",
    5121: "B",
    5122: "h",
    5123: "H",
    5125: "I",
    5126: "f",
}


def clean_name(value: str, fallback: str) -> str:
    name = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    return name.strip("_") or fallback


def decode_data_uri(uri: str) -> bytes:
    if not uri.startswith("data:"):
        raise ValueError("not a data URI")
    _, encoded = uri.split(",", 1)
    return base64.b64decode(encoded)


def load_buffers(gltf: dict, source_path: Path) -> list[bytes]:
    buffers: list[bytes] = []
    for buffer_def in gltf.get("buffers", []):
        uri = buffer_def.get("uri")
        if not uri:
            raise ValueError("GLB binary chunks are not supported by this script")
        if uri.startswith("data:"):
            data = decode_data_uri(uri)
        else:
            data = (source_path.parent / uri).read_bytes()
        buffers.append(data)
    return buffers


def accessor_values(gltf: dict, buffers: list[bytes], accessor_index: int) -> list:
    accessor = gltf["accessors"][accessor_index]
    view = gltf["bufferViews"][accessor["bufferView"]]
    data = buffers[view["buffer"]]
    component_format = COMPONENT_FORMATS[accessor["componentType"]]
    component_count = TYPE_COMPONENTS[accessor["type"]]
    component_size = struct.calcsize("<" + component_format)
    item_size = component_size * component_count
    stride = view.get("byteStride", item_size)
    offset = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
    unpack_format = "<" + component_format * component_count
    values = []
    for item_index in range(accessor["count"]):
        item_offset = offset + item_index * stride
        unpacked = struct.unpack_from(unpack_format, data, item_offset)
        if component_count == 1:
            values.append(unpacked[0])
        else:
            values.append(unpacked)
    return values


def identity_matrix() -> list[list[float]]:
    return [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]


def multiply_matrix(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    return [
        [
            sum(left[row][inner] * right[inner][col] for inner in range(4))
            for col in range(4)
        ]
        for row in range(4)
    ]


def translation_matrix(values: Iterable[float]) -> list[list[float]]:
    x, y, z = values
    matrix = identity_matrix()
    matrix[0][3] = x
    matrix[1][3] = y
    matrix[2][3] = z
    return matrix


def scale_matrix(values: Iterable[float]) -> list[list[float]]:
    x, y, z = values
    matrix = identity_matrix()
    matrix[0][0] = x
    matrix[1][1] = y
    matrix[2][2] = z
    return matrix


def rotation_matrix(quaternion: Iterable[float]) -> list[list[float]]:
    x, y, z, w = quaternion
    xx = x * x
    yy = y * y
    zz = z * z
    xy = x * y
    xz = x * z
    yz = y * z
    wx = w * x
    wy = w * y
    wz = w * z
    return [
        [1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy), 0.0],
        [2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx), 0.0],
        [2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy), 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]


def gltf_matrix(flat: Iterable[float]) -> list[list[float]]:
    values = list(flat)
    return [[values[col * 4 + row] for col in range(4)] for row in range(4)]


def node_matrix(node: dict) -> list[list[float]]:
    if "matrix" in node:
        return gltf_matrix(node["matrix"])
    matrix = identity_matrix()
    if "translation" in node:
        matrix = multiply_matrix(matrix, translation_matrix(node["translation"]))
    if "rotation" in node:
        matrix = multiply_matrix(matrix, rotation_matrix(node["rotation"]))
    if "scale" in node:
        matrix = multiply_matrix(matrix, scale_matrix(node["scale"]))
    return matrix


def transform_point(matrix: list[list[float]], point: Iterable[float]) -> tuple[float, float, float]:
    x, y, z = point
    return (
        matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z + matrix[0][3],
        matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z + matrix[1][3],
        matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z + matrix[2][3],
    )


def transform_normal(matrix: list[list[float]], normal: Iterable[float]) -> tuple[float, float, float]:
    x, y, z = normal
    nx = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z
    ny = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z
    nz = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z
    length = math.sqrt(nx * nx + ny * ny + nz * nz)
    if length == 0:
        return (0.0, 0.0, 1.0)
    return (nx / length, ny / length, nz / length)


def material_name(gltf: dict, material_index: int | None) -> str:
    if material_index is None:
        return "default"
    material = gltf.get("materials", [])[material_index]
    return clean_name(material.get("name", f"material_{material_index}"), f"material_{material_index}")


def write_mtl(gltf: dict, mtl_path: Path) -> None:
    lines = [
        "# Generated from glTF materials.",
        "newmtl default",
        "Kd 0.800000 0.800000 0.800000",
        "d 1.000000",
        "",
    ]
    for index, material in enumerate(gltf.get("materials", [])):
        name = material_name(gltf, index)
        pbr = material.get("pbrMetallicRoughness", {})
        color = pbr.get("baseColorFactor", [0.8, 0.8, 0.8, 1.0])
        lines.extend(
            [
                f"newmtl {name}",
                f"Kd {color[0]:.6f} {color[1]:.6f} {color[2]:.6f}",
                f"d {color[3]:.6f}",
                "",
            ]
        )
    mtl_path.write_text("\n".join(lines), encoding="ascii")


def triangle_indices(mode: int, indices: list[int]) -> Iterable[tuple[int, int, int]]:
    if mode == 4:
        for offset in range(0, len(indices), 3):
            yield (indices[offset], indices[offset + 1], indices[offset + 2])
    elif mode == 5:
        for offset in range(len(indices) - 2):
            tri = (indices[offset], indices[offset + 1], indices[offset + 2])
            yield tri if offset % 2 == 0 else (tri[1], tri[0], tri[2])
    elif mode == 6:
        root = indices[0]
        for offset in range(1, len(indices) - 1):
            yield (root, indices[offset], indices[offset + 1])
    else:
        raise ValueError(f"unsupported primitive mode {mode}")


def scene_nodes(gltf: dict) -> list[int]:
    scene_index = gltf.get("scene", 0)
    return list(gltf["scenes"][scene_index].get("nodes", []))


def iter_node_tree(gltf: dict, node_indices: Iterable[int], parent_matrix: list[list[float]]):
    for node_index in node_indices:
        node = gltf["nodes"][node_index]
        matrix = multiply_matrix(parent_matrix, node_matrix(node))
        yield node_index, node, matrix
        yield from iter_node_tree(gltf, node.get("children", []), matrix)


def export_obj(source_path: Path, obj_path: Path, mtl_path: Path) -> dict:
    gltf = json.loads(source_path.read_text(encoding="utf-8"))
    buffers = load_buffers(gltf, source_path)
    write_mtl(gltf, mtl_path)

    stats = {
        "objects": 0,
        "vertices": 0,
        "normals": 0,
        "faces": 0,
        "skipped_primitives": 0,
    }
    vertex_offset = 1
    normal_offset = 1

    with obj_path.open("w", encoding="ascii", newline="\n") as obj:
        obj.write("# Generated from glTF for mesh editing.\n")
        obj.write(f"mtllib {mtl_path.name}\n\n")

        for _, node, world_matrix in iter_node_tree(gltf, scene_nodes(gltf), identity_matrix()):
            if "mesh" not in node:
                continue
            mesh = gltf["meshes"][node["mesh"]]
            object_name = clean_name(node.get("name") or mesh.get("name", ""), f"mesh_{node['mesh']}")
            group_name = clean_name(node.get("extras", {}).get("group", object_name), object_name)
            obj.write(f"o {object_name}\n")
            obj.write(f"g {group_name}\n")
            stats["objects"] += 1

            for primitive_index, primitive in enumerate(mesh.get("primitives", [])):
                mode = primitive.get("mode", 4)
                if mode not in {4, 5, 6}:
                    stats["skipped_primitives"] += 1
                    continue

                attrs = primitive["attributes"]
                positions = accessor_values(gltf, buffers, attrs["POSITION"])
                normals = (
                    accessor_values(gltf, buffers, attrs["NORMAL"])
                    if "NORMAL" in attrs
                    else []
                )
                has_normals = len(normals) == len(positions)
                indices = (
                    accessor_values(gltf, buffers, primitive["indices"])
                    if "indices" in primitive
                    else list(range(len(positions)))
                )

                obj.write(f"usemtl {material_name(gltf, primitive.get('material'))}\n")
                if primitive_index:
                    obj.write(f"g {group_name}_{primitive_index}\n")

                for point in positions:
                    x, y, z = transform_point(world_matrix, point)
                    obj.write(f"v {x:.9g} {y:.9g} {z:.9g}\n")
                stats["vertices"] += len(positions)

                if has_normals:
                    for normal in normals:
                        x, y, z = transform_normal(world_matrix, normal)
                        obj.write(f"vn {x:.9g} {y:.9g} {z:.9g}\n")
                    stats["normals"] += len(normals)

                for a, b, c in triangle_indices(mode, indices):
                    va = vertex_offset + a
                    vb = vertex_offset + b
                    vc = vertex_offset + c
                    if has_normals:
                        na = normal_offset + a
                        nb = normal_offset + b
                        nc = normal_offset + c
                        obj.write(f"f {va}//{na} {vb}//{nb} {vc}//{nc}\n")
                    else:
                        obj.write(f"f {va} {vb} {vc}\n")
                    stats["faces"] += 1

                vertex_offset += len(positions)
                if has_normals:
                    normal_offset += len(normals)
                obj.write("\n")

    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Input glTF file")
    parser.add_argument("output", type=Path, help="Output OBJ file")
    parser.add_argument("--mtl", type=Path, help="Output MTL file")
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    mtl = args.mtl.resolve() if args.mtl else output.with_suffix(".mtl")
    output.parent.mkdir(parents=True, exist_ok=True)
    stats = export_obj(source, output, mtl)
    print(
        "Exported {objects} objects, {vertices} vertices, {faces} faces "
        "to {output}".format(output=output, **stats)
    )
    if stats["skipped_primitives"]:
        print(f"Skipped {stats['skipped_primitives']} unsupported primitives")
    print(f"Wrote materials to {mtl}")


if __name__ == "__main__":
    main()
