from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import struct
import zipfile


ROOT = Path(__file__).resolve().parent.parent
CAD_ROOT = ROOT / "data" / "manual" / "cad" / "j40_reference_model"
INBOX_DIR = CAD_ROOT / "00_inbox"
SOURCE_DIR = CAD_ROOT / "01_source_mesh"
REPORT_DIR = CAD_ROOT / "05_reports"

MODEL_URL = "https://sketchfab.com/3d-models/toyota-land-cruiser-fj40-softtopinteriorchassis-aaf9547c5e8b478abd2ceb47f1f82340"
MODEL_UID = "aaf9547c5e8b478abd2ceb47f1f82340"
MODEL_AUTHOR = "dragosburian"
MODEL_LICENSE = "Purchased/licensed project use; retain original license terms with the asset"

MESH_EXTS = {
    ".blend",
    ".dae",
    ".fbx",
    ".glb",
    ".gltf",
    ".mtl",
    ".obj",
    ".ply",
    ".stl",
    ".usd",
    ".usdz",
}


def human_size(num_bytes: int) -> str:
    value = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{num_bytes} B"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_extract_zip(zip_path: Path, target_dir: Path) -> list[Path]:
    extracted: list[Path] = []
    target_dir.mkdir(parents=True, exist_ok=True)
    target_root = target_dir.resolve()

    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            member_path = target_dir / member.filename
            resolved = member_path.resolve()
            if not str(resolved).startswith(str(target_root)):
                raise ValueError(f"Refusing unsafe ZIP member path: {member.filename}")
            if member.is_dir():
                resolved.mkdir(parents=True, exist_ok=True)
                continue
            resolved.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as src, resolved.open("wb") as dst:
                dst.write(src.read())
            extracted.append(resolved)
    return extracted


def read_obj_stats(path: Path) -> dict[str, object]:
    stats: dict[str, object] = {
        "format": "obj",
        "vertices": 0,
        "texture_vertices": 0,
        "normals": 0,
        "faces": 0,
        "objects": [],
        "groups": [],
        "materials": [],
        "material_libraries": [],
    }
    objects: set[str] = set()
    groups: set[str] = set()
    materials: set[str] = set()
    material_libraries: set[str] = set()

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if line.startswith("v "):
                stats["vertices"] = int(stats["vertices"]) + 1
            elif line.startswith("vt "):
                stats["texture_vertices"] = int(stats["texture_vertices"]) + 1
            elif line.startswith("vn "):
                stats["normals"] = int(stats["normals"]) + 1
            elif line.startswith("f "):
                stats["faces"] = int(stats["faces"]) + 1
            elif line.startswith("o "):
                objects.add(line[2:].strip())
            elif line.startswith("g "):
                groups.add(line[2:].strip())
            elif line.startswith("usemtl "):
                materials.add(line[7:].strip())
            elif line.startswith("mtllib "):
                material_libraries.add(line[7:].strip())

    stats["objects"] = sorted(item for item in objects if item)
    stats["groups"] = sorted(item for item in groups if item)
    stats["materials"] = sorted(item for item in materials if item)
    stats["material_libraries"] = sorted(item for item in material_libraries if item)
    return stats


def read_stl_stats(path: Path) -> dict[str, object]:
    size = path.stat().st_size
    with path.open("rb") as handle:
        header = handle.read(84)

    if len(header) >= 84:
        triangles = struct.unpack("<I", header[80:84])[0]
        if 84 + (triangles * 50) == size:
            return {"format": "stl-binary", "triangles": triangles}

    facets = 0
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            if line.lstrip().startswith("facet normal"):
                facets += 1
    return {"format": "stl-ascii", "triangles": facets}


def mesh_stats(path: Path) -> dict[str, object]:
    suffix = path.suffix.lower()
    if suffix == ".obj":
        return read_obj_stats(path)
    if suffix == ".stl":
        return read_stl_stats(path)
    return {"format": suffix.removeprefix(".") or "unknown"}


def find_mesh_files() -> list[Path]:
    files: list[Path] = []
    for base in (INBOX_DIR, SOURCE_DIR):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in MESH_EXTS:
                files.append(path)
    return sorted(set(files))


def archive_entries() -> list[Path]:
    if not INBOX_DIR.exists():
        return []
    return sorted(path for path in INBOX_DIR.iterdir() if path.is_file() and path.suffix.lower() == ".zip")


def build_manifest(extracted: dict[str, list[str]]) -> dict[str, object]:
    archives = []
    for path in archive_entries():
        archives.append(
            {
                "path": str(path.relative_to(ROOT)),
                "size_bytes": path.stat().st_size,
                "size": human_size(path.stat().st_size),
                "sha256": sha256_file(path),
                "extracted_files": extracted.get(path.name, []),
            }
        )

    meshes = []
    for path in find_mesh_files():
        rel_path = path.relative_to(ROOT)
        record: dict[str, object] = {
            "path": str(rel_path),
            "size_bytes": path.stat().st_size,
            "size": human_size(path.stat().st_size),
            "sha256": sha256_file(path),
        }
        try:
            record["stats"] = mesh_stats(path)
        except Exception as exc:  # noqa: BLE001 - inventory should continue past malformed assets.
            record["stats_error"] = str(exc)
        meshes.append(record)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": {
            "uid": MODEL_UID,
            "url": MODEL_URL,
            "author": MODEL_AUTHOR,
            "license": MODEL_LICENSE,
        },
        "archives": archives,
        "mesh_files": meshes,
    }


def write_reports(manifest: dict[str, object]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = REPORT_DIR / "source_model_manifest.json"
    report_path = REPORT_DIR / "source_model_inventory.md"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    archives = list(manifest["archives"])
    meshes = list(manifest["mesh_files"])

    lines = [
        "# J40 Source Model Inventory",
        "",
        f"Generated: {manifest['generated_at']}",
        "",
        "## Source",
        "",
        f"- URL: {MODEL_URL}",
        f"- Author: {MODEL_AUTHOR}",
        f"- License: {MODEL_LICENSE}",
        "",
        "## Status",
        "",
    ]
    if not archives and not meshes:
        lines.extend(
            [
                "No Sketchfab source ZIP or mesh files were found yet.",
                "",
                f"Put the downloaded ZIP in `{INBOX_DIR.relative_to(ROOT)}/`, then rerun `python3 scripts/j40_cad_intake.py`.",
                "",
            ]
        )
    else:
        lines.append(f"- Archives found: {len(archives)}")
        lines.append(f"- Mesh files found: {len(meshes)}")
        lines.append("")

    if archives:
        lines.extend(["## Archives", ""])
        for archive in archives:
            lines.append(f"- `{archive['path']}`: {archive['size']}, sha256 `{str(archive['sha256'])[:12]}...`")
        lines.append("")

    if meshes:
        lines.extend(["## Mesh Files", ""])
        for mesh in meshes:
            stats = mesh.get("stats", {})
            stat_bits: list[str] = []
            if isinstance(stats, dict):
                for key in ("format", "vertices", "faces", "triangles"):
                    if key in stats:
                        stat_bits.append(f"{key}={stats[key]}")
            suffix = f" ({', '.join(stat_bits)})" if stat_bits else ""
            lines.append(f"- `{mesh['path']}`: {mesh['size']}{suffix}")
        lines.append("")

    lines.extend(
        [
            "## CAD Notes",
            "",
            "- Treat the Sketchfab asset as a reference mesh, not a dimensional source of truth.",
            "- Do not try to convert the whole vehicle into one solid body unless it has first been heavily cleaned and split into logical parts.",
            "- Convert or remodel only the useful pieces: body tub envelope, firewall, frame rails, spring hangers, dashboard, seats, brackets, and hard mounting points.",
            "- Final fabrication parts still need physical measurements from the actual J40.",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")


def extract_archives(force: bool) -> dict[str, list[str]]:
    extracted: dict[str, list[str]] = {}
    for zip_path in archive_entries():
        target = SOURCE_DIR / zip_path.stem
        if target.exists() and any(target.iterdir()) and not force:
            extracted[zip_path.name] = [str(path.relative_to(ROOT)) for path in target.rglob("*") if path.is_file()]
            continue
        files = safe_extract_zip(zip_path, target)
        extracted[zip_path.name] = [str(path.relative_to(ROOT)) for path in files]
    return extracted


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventory the J40 Sketchfab reference model intake.")
    parser.add_argument("--force-extract", action="store_true", help="re-extract ZIP archives even if output exists")
    args = parser.parse_args()

    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    extracted = extract_archives(args.force_extract)
    manifest = build_manifest(extracted)
    write_reports(manifest)
    print(f"Wrote {REPORT_DIR.relative_to(ROOT) / 'source_model_inventory.md'}")
    print(f"Wrote {REPORT_DIR.relative_to(ROOT) / 'source_model_manifest.json'}")


if __name__ == "__main__":
    main()
