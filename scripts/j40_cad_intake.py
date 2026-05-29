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

MODEL_NAME = "1976 Toyota Land Cruiser FJ40"
MODEL_URL = "https://sketchfab.com/3d-models/1976-toyota-land-cruiser-fj40-a4e58b09ce48444ca6164834c310880d"
MODEL_UID = "a4e58b09ce48444ca6164834c310880d"
MODEL_AUTHOR = "tonielpro520"
MODEL_AUTHOR_URL = "https://sketchfab.com/tonielpro520"
MODEL_LICENSE = "Creative Commons Attribution 4.0 (CC BY 4.0); author credit required; commercial use allowed"
MODEL_LICENSE_URL = "http://creativecommons.org/licenses/by/4.0/"
MODEL_SOURCE = "Sketchfab"
MODEL_IS_DOWNLOADABLE = True
MODEL_VERTEX_COUNT = 96681
MODEL_FACE_COUNT = 177769
MODEL_MATERIAL_COUNT = 31
MODEL_TEXTURE_COUNT = 3
MODEL_THUMBNAIL_URL = "https://media.sketchfab.com/models/a4e58b09ce48444ca6164834c310880d/thumbnails/bf7cb5bb6e3f46d48005187a7be2149c/ec0f310299a84fdba897c982290af85e.jpeg"

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
            "name": MODEL_NAME,
            "uid": MODEL_UID,
            "url": MODEL_URL,
            "author": MODEL_AUTHOR,
            "author_url": MODEL_AUTHOR_URL,
            "license": MODEL_LICENSE,
            "license_url": MODEL_LICENSE_URL,
            "source": MODEL_SOURCE,
            "is_downloadable": MODEL_IS_DOWNLOADABLE,
            "vertex_count": MODEL_VERTEX_COUNT,
            "face_count": MODEL_FACE_COUNT,
            "material_count": MODEL_MATERIAL_COUNT,
            "texture_count": MODEL_TEXTURE_COUNT,
            "thumbnail_url": MODEL_THUMBNAIL_URL,
        },
        "archives": archives,
        "mesh_files": meshes,
    }


def write_attribution() -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = CAD_ROOT / "ATTRIBUTION.md"
    lines = [
        "# J40 CAD Reference Attribution",
        "",
        "## Open Source Reference Model",
        "",
        f"- Model: {MODEL_NAME}",
        f"- Source: {MODEL_URL}",
        f"- Author: [{MODEL_AUTHOR}]({MODEL_AUTHOR_URL})",
        f"- License: [{MODEL_LICENSE}]({MODEL_LICENSE_URL})",
        "- Use in this repo: visual reference and optional local source mesh for manual remodelling into measured CAD.",
        "",
        "The generated scaffold is project-owned geometry built from simple CAD primitives, project photos, and representative FJ40 dimensions. It is not a redistribution of the Sketchfab source mesh.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


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
        f"- Model: {MODEL_NAME}",
        f"- URL: {MODEL_URL}",
        f"- Author: {MODEL_AUTHOR}",
        f"- License: {MODEL_LICENSE}",
        f"- License URL: {MODEL_LICENSE_URL}",
        f"- Downloadable: {'yes' if MODEL_IS_DOWNLOADABLE else 'no'}",
        f"- Mesh stats from Sketchfab API: {MODEL_VERTEX_COUNT:,} vertices, {MODEL_FACE_COUNT:,} faces, {MODEL_MATERIAL_COUNT} materials, {MODEL_TEXTURE_COUNT} textures",
        "",
        "## Status",
        "",
    ]
    if not archives and not meshes:
        lines.extend(
            [
                "No Sketchfab source ZIP or mesh files were found yet.",
                "",
                "Sketchfab marks this model downloadable, but the download endpoint requires a logged-in/authenticated request.",
                "",
                f"Download the source archive while logged in, put the ZIP in `{INBOX_DIR.relative_to(ROOT)}/`, then rerun `python3 scripts/j40_cad_intake.py`.",
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
            "- Keep the CC-BY attribution with any derivative reference package.",
            "- Do not try to convert the whole vehicle into one solid body unless it has first been heavily cleaned and split into logical parts.",
            "- Convert or remodel only the useful pieces: body tub envelope, firewall, frame rails, spring hangers, dashboard, seats, brackets, and hard mounting points.",
            "- Final fabrication parts still need physical measurements from the actual J40.",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")
    write_attribution()


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
