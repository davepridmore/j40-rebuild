#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
UI_DIR = ROOT / "docs" / "project-control-ui"
DEFAULT_OUTPUT_DIR = ROOT / ".deploy" / "project-control-ui-site"
DATA_PREFIX = "window.J40_DASHBOARD_DATA = "
DATA_SUFFIX = ";"
UI_FILES = ("index.html", "app.js", "styles.css")
STAGED_MEDIA_PATH = "assets/dashboard-media"
MISSING_MEDIA_FALLBACK = "./assets/image-needed.svg"
PUBLIC_FABRICATION_DIR = ROOT / "data" / "manual" / "fabrication"
PUBLIC_FABRICATION_DOCS = (
    ROOT / "docs" / "fabrication-handoff-index.md",
    ROOT / "docs" / "rubber-recreation-fabrication-spec-20260502.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stage the public Project Control UI deploy artifact."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to rebuild with the deployable static site.",
    )
    return parser.parse_args()


def load_dashboard_data() -> dict[str, Any]:
    data_path = UI_DIR / "data.js"
    raw = data_path.read_text(encoding="utf-8").strip()
    if not raw.startswith(DATA_PREFIX) or not raw.endswith(DATA_SUFFIX):
        raise ValueError(f"{data_path} is not in the expected generated data.js format")
    payload = raw[len(DATA_PREFIX) : -len(DATA_SUFFIX)]
    data = json.loads(payload)
    if not isinstance(data, dict):
        raise ValueError(f"{data_path} did not contain a dashboard data object")
    return data


def write_dashboard_data(data: dict[str, Any], output_dir: Path) -> None:
    target = output_dir / "docs" / "project-control-ui" / "data.js"
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = DATA_PREFIX + json.dumps(data, ensure_ascii=True, indent=2) + ";\n"
    target.write_text(payload, encoding="utf-8")


def walk_values(value: Any) -> Any:
    if isinstance(value, dict):
        for child in value.values():
            yield from walk_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_values(child)
    else:
        yield value


def walk_dicts(value: Any) -> Any:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_dicts(child)


def collect_media_ids(value: Any) -> set[str]:
    media_ids: set[str] = set()
    for row in walk_dicts(value):
        media_id = row.get("media_id")
        if isinstance(media_id, str) and media_id.strip():
            media_ids.add(media_id.strip())
    return media_ids


def collect_relative_asset_paths(value: Any) -> set[str]:
    paths: set[str] = set()
    for item in walk_values(value):
        if not isinstance(item, str):
            continue
        normalized = item.strip().replace("\\", "/")
        if normalized.startswith("../../"):
            paths.add(normalized)
    return paths


def rewrite_relative_asset_paths(value: Any, path_map: dict[str, str]) -> Any:
    if isinstance(value, dict):
        return {key: rewrite_relative_asset_paths(child, path_map) for key, child in value.items()}
    if isinstance(value, list):
        return [rewrite_relative_asset_paths(child, path_map) for child in value]
    if isinstance(value, str):
        normalized = value.strip().replace("\\", "/")
        return path_map.get(normalized, value)
    return value


def prune_dashboard_data(data: dict[str, Any]) -> dict[str, Any]:
    public_data = dict(data)

    # This only names internal CSV sources. It is useful locally, but does not
    # drive the browser UI and should not be part of the public artifact.
    public_data.pop("source_files", None)

    photo_lookup = public_data.get("photo_lookup")
    if isinstance(photo_lookup, dict):
        without_lookup = dict(public_data)
        without_lookup.pop("photo_lookup", None)
        referenced_ids = collect_media_ids(without_lookup)
        referenced_paths = collect_relative_asset_paths(without_lookup)

        pruned_lookup: dict[str, Any] = {}
        for key, row in photo_lookup.items():
            if not isinstance(row, dict):
                continue
            media_id = str(row.get("media_id") or key).strip()
            path = str(row.get("path") or "").strip().replace("\\", "/")
            if media_id in referenced_ids or path in referenced_paths:
                pruned_lookup[str(key)] = row
        public_data["photo_lookup"] = pruned_lookup

    return public_data


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def resolve_repo_path(relative_ui_path: str) -> Path:
    repo_relative = relative_ui_path.replace("\\", "/")
    while repo_relative.startswith("../"):
        repo_relative = repo_relative[3:]
    source = (ROOT / repo_relative).resolve()
    try:
        source.relative_to(ROOT)
    except ValueError as error:
        raise ValueError(f"Refusing to stage path outside repo: {relative_ui_path}") from error
    return source


def stage_static_ui(output_dir: Path) -> None:
    target_ui_dir = output_dir / "docs" / "project-control-ui"
    for name in UI_FILES:
        source = UI_DIR / name
        target = target_ui_dir / name
        copy_file(source, target)

    assets_dir = UI_DIR / "assets"
    if assets_dir.exists():
        shutil.copytree(assets_dir, target_ui_dir / "assets", dirs_exist_ok=True)

    index_path = target_ui_dir / "index.html"
    index_html = index_path.read_text(encoding="utf-8")
    index_html = index_html.replace(
        '    <p>Sources: <code>data/manual/workstream_status.csv</code>, <code>data/manual/reassembly_work_packages.csv</code>, <code>data/manual/expenses.csv</code>, <code>data/manual/photo_inventory.csv</code>, <code>data/manual/other_build_reference_media.csv</code>, <code>data/reference/other_j40_builds/</code></p>',
        "    <p>Published dashboard snapshot.</p>",
    )
    index_path.write_text(index_html, encoding="utf-8")

    redirect = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=./docs/project-control-ui/">
  <title>J40 Project Control UI</title>
</head>
<body>
  <p><a href="./docs/project-control-ui/">Open J40 Project Control UI</a></p>
</body>
</html>
"""
    (output_dir / "index.html").write_text(redirect, encoding="utf-8")


def stage_public_fabrication_assets(output_dir: Path) -> int:
    copied = 0
    if PUBLIC_FABRICATION_DIR.exists():
        target = output_dir / PUBLIC_FABRICATION_DIR.relative_to(ROOT)
        shutil.copytree(PUBLIC_FABRICATION_DIR, target, dirs_exist_ok=True)
        copied += sum(1 for path in target.rglob("*") if path.is_file())

    for source in PUBLIC_FABRICATION_DOCS:
        if not source.exists():
            continue
        copy_file(source, output_dir / source.relative_to(ROOT))
        copied += 1

    return copied


def staged_media_name(relative_ui_path: str, source: Path) -> str:
    digest = hashlib.sha1(relative_ui_path.encode("utf-8")).hexdigest()[:16]
    suffix = source.suffix.lower() or ".bin"
    return f"{digest}{suffix}"


def stage_referenced_assets(data: dict[str, Any], output_dir: Path) -> tuple[dict[str, Any], int, list[str]]:
    missing: list[str] = []
    path_map: dict[str, str] = {}
    copied = 0
    for relative_ui_path in sorted(collect_relative_asset_paths(data)):
        source = resolve_repo_path(relative_ui_path)
        staged_name = staged_media_name(relative_ui_path, source)
        rewritten_path = f"../../{STAGED_MEDIA_PATH}/{staged_name}"
        path_map[relative_ui_path] = rewritten_path
        target = output_dir / STAGED_MEDIA_PATH / staged_name
        if not source.exists():
            missing.append(relative_ui_path)
            path_map[relative_ui_path] = MISSING_MEDIA_FALLBACK
            continue
        copy_file(source, target)
        copied += 1
    return rewrite_relative_asset_paths(data, path_map), copied, missing


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir.resolve()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    data = prune_dashboard_data(load_dashboard_data())
    stage_static_ui(output_dir)
    copied_fabrication_assets = stage_public_fabrication_assets(output_dir)
    data, copied_assets, missing_assets = stage_referenced_assets(data, output_dir)
    write_dashboard_data(data, output_dir)

    print(f"Staged Project Control UI: {output_dir}")
    print(f"Copied fabrication assets: {copied_fabrication_assets}")
    print(f"Copied referenced media/assets: {copied_assets}")
    if missing_assets:
        print(f"Missing referenced media/assets: {len(missing_assets)}")
        for path in missing_assets[:20]:
            print(f"  - {path}")
        if len(missing_assets) > 20:
            print(f"  ... {len(missing_assets) - 20} more")


if __name__ == "__main__":
    main()
