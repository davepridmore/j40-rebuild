#!/usr/bin/env python3
"""Downsample oversized raster images embedded in a DOCX.

The optimizer reads the image display dimensions recorded in the Word package
and retains a configurable effective DPI at the largest placement. All
non-image package parts are copied byte-for-byte, so document content and
layout are not otherwise rebuilt or reformatted.
"""

from __future__ import annotations

import argparse
import io
import math
import os
import posixpath
import stat
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree

from PIL import Image


EMU_PER_INCH = 914_400
NAMESPACES = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}
RELATIONSHIP_NAMESPACE = "http://schemas.openxmlformats.org/package/2006/relationships"
IMAGE_RELATIONSHIP = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
)
SUPPORTED_RASTER_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def _relationship_part_name(part_name: str) -> str:
    directory, filename = posixpath.split(part_name)
    return posixpath.join(directory, "_rels", f"{filename}.rels")


def _resolve_relationship_target(part_name: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(part_name), target))


def _image_placements(
    package: zipfile.ZipFile,
) -> dict[str, list[tuple[float, float]]]:
    """Return the displayed width and height, in inches, for each raster."""

    package_names = set(package.namelist())
    placements: dict[str, list[tuple[float, float]]] = defaultdict(list)

    for part_name in package_names:
        if not part_name.endswith(".xml"):
            continue
        relationship_name = _relationship_part_name(part_name)
        if relationship_name not in package_names:
            continue

        try:
            relationship_root = ElementTree.fromstring(package.read(relationship_name))
            part_root = ElementTree.fromstring(package.read(part_name))
        except ElementTree.ParseError:
            continue

        target_by_id: dict[str, str] = {}
        for relationship in relationship_root.findall(
            f"{{{RELATIONSHIP_NAMESPACE}}}Relationship"
        ):
            if relationship.get("Type") != IMAGE_RELATIONSHIP:
                continue
            if relationship.get("TargetMode") == "External":
                continue
            relationship_id = relationship.get("Id")
            target = relationship.get("Target")
            if relationship_id and target:
                target_by_id[relationship_id] = _resolve_relationship_target(
                    part_name, target
                )

        if not target_by_id:
            continue

        drawing_nodes = [
            *part_root.findall(".//wp:inline", NAMESPACES),
            *part_root.findall(".//wp:anchor", NAMESPACES),
        ]
        for drawing in drawing_nodes:
            extent = drawing.find("wp:extent", NAMESPACES)
            if extent is None:
                extent = drawing.find(".//wp:extent", NAMESPACES)
            if extent is None:
                continue
            try:
                width_inches = int(extent.get("cx", "0")) / EMU_PER_INCH
                height_inches = int(extent.get("cy", "0")) / EMU_PER_INCH
            except ValueError:
                continue
            if width_inches <= 0 or height_inches <= 0:
                continue

            for blip in drawing.findall(".//a:blip", NAMESPACES):
                relationship_id = blip.get(f"{{{NAMESPACES['r']}}}embed")
                target = target_by_id.get(relationship_id or "")
                if target:
                    placements[target].append((width_inches, height_inches))

    return placements


def _target_size(
    width: int,
    height: int,
    placements: list[tuple[float, float]],
    target_dpi: int,
    fallback_long_edge: int,
) -> tuple[int, int]:
    if placements:
        required_width = max(display_width * target_dpi for display_width, _ in placements)
        required_height = max(
            display_height * target_dpi for _, display_height in placements
        )
        scale = max(required_width / width, required_height / height)
    else:
        scale = fallback_long_edge / max(width, height)

    scale = min(1.0, scale)
    return (
        max(1, int(math.ceil(width * scale))),
        max(1, int(math.ceil(height * scale))),
    )


def _optimized_image_bytes(
    source: bytes,
    suffix: str,
    target_size: tuple[int, int],
    jpeg_quality: int,
) -> bytes:
    with Image.open(io.BytesIO(source)) as image:
        if image.size == target_size:
            return source

        resized = image.resize(target_size, Image.Resampling.LANCZOS)
        output = io.BytesIO()
        common_options = {}
        if image.info.get("icc_profile"):
            common_options["icc_profile"] = image.info["icc_profile"]
        if image.info.get("dpi"):
            common_options["dpi"] = image.info["dpi"]

        if suffix in {".jpg", ".jpeg"}:
            if resized.mode not in {"RGB", "L"}:
                resized = resized.convert("RGB")
            jpeg_options = {
                "format": "JPEG",
                "quality": jpeg_quality,
                "optimize": True,
                "progressive": True,
                **common_options,
            }
            if image.info.get("exif"):
                jpeg_options["exif"] = image.info["exif"]
            resized.save(output, **jpeg_options)
        else:
            resized.save(output, format="PNG", optimize=True, **common_options)

        optimized = output.getvalue()
        return optimized if len(optimized) < len(source) else source


def optimize_docx_images(
    input_path: Path,
    output_path: Path | None = None,
    *,
    target_dpi: int = 600,
    jpeg_quality: int = 85,
    fallback_long_edge: int = 2400,
) -> dict[str, int]:
    """Optimize a DOCX and return aggregate image statistics."""

    input_path = Path(input_path)
    output_path = Path(output_path) if output_path else input_path
    input_mode = stat.S_IMODE(input_path.stat().st_mode)
    if target_dpi <= 0:
        raise ValueError("target_dpi must be positive")
    if not 1 <= jpeg_quality <= 100:
        raise ValueError("jpeg_quality must be between 1 and 100")
    if fallback_long_edge <= 0:
        raise ValueError("fallback_long_edge must be positive")

    with zipfile.ZipFile(input_path, "r") as source_package:
        placements = _image_placements(source_package)
        source_infos = source_package.infolist()
        source_bytes = {
            info.filename: source_package.read(info.filename) for info in source_infos
        }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = tempfile.NamedTemporaryFile(
        prefix=f".{output_path.name}.",
        suffix=".tmp",
        dir=output_path.parent,
        delete=False,
    )
    temporary_path = Path(temporary.name)
    temporary.close()

    stats = {
        "images_seen": 0,
        "images_resized": 0,
        "original_image_bytes": 0,
        "optimized_image_bytes": 0,
    }
    try:
        with zipfile.ZipFile(temporary_path, "w") as output_package:
            for info in source_infos:
                data = source_bytes[info.filename]
                suffix = Path(info.filename).suffix.lower()
                if (
                    info.filename.startswith("word/media/")
                    and suffix in SUPPORTED_RASTER_EXTENSIONS
                ):
                    stats["images_seen"] += 1
                    stats["original_image_bytes"] += len(data)
                    with Image.open(io.BytesIO(data)) as image:
                        original_size = image.size
                    target_size = _target_size(
                        *original_size,
                        placements.get(info.filename, []),
                        target_dpi,
                        fallback_long_edge,
                    )
                    optimized = _optimized_image_bytes(
                        data, suffix, target_size, jpeg_quality
                    )
                    if optimized != data:
                        stats["images_resized"] += 1
                        data = optimized
                    stats["optimized_image_bytes"] += len(data)
                output_package.writestr(info, data)

        os.chmod(temporary_path, input_mode)
        os.replace(temporary_path, output_path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise

    return stats


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Downsample oversized raster images in a DOCX while preserving "
            "the document package and layout."
        )
    )
    parser.add_argument("input", type=Path, help="Input DOCX")
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        help="Output DOCX; omit to replace the input safely in place",
    )
    parser.add_argument(
        "--target-dpi",
        type=int,
        default=600,
        help="Effective DPI retained at each image's largest placement (default: 600)",
    )
    parser.add_argument(
        "--jpeg-quality",
        type=int,
        default=85,
        help="JPEG quality for resized images (default: 85)",
    )
    parser.add_argument(
        "--fallback-long-edge",
        type=int,
        default=2400,
        help="Maximum long edge when display size cannot be read (default: 2400)",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output = args.output or args.input
    stats = optimize_docx_images(
        args.input,
        output,
        target_dpi=args.target_dpi,
        jpeg_quality=args.jpeg_quality,
        fallback_long_edge=args.fallback_long_edge,
    )
    before_mib = stats["original_image_bytes"] / (1024 * 1024)
    after_mib = stats["optimized_image_bytes"] / (1024 * 1024)
    print(
        f"{output}: resized {stats['images_resized']}/{stats['images_seen']} images; "
        f"embedded raster data {before_mib:.1f} MiB -> {after_mib:.1f} MiB"
    )


if __name__ == "__main__":
    main()
