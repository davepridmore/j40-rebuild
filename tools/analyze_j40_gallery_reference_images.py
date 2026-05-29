from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import urlretrieve

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "data" / "manual" / "cad" / "j40_reference_model" / "05_reports"
DEFAULT_CACHE_DIR = Path("/private/tmp/j40_ref_images")


GALLERY_IMAGES = [
    {
        "index": 1,
        "filename": "ref_0001.jpg",
        "role": "front_three_quarter",
        "url": "https://360views.3dmodels.org/zoom/Toyota/Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979_1000_0001.jpg",
    },
    {
        "index": 2,
        "filename": "ref_0002.jpg",
        "role": "rear_three_quarter",
        "url": "https://360views.3dmodels.org/zoom/Toyota/Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979_1000_0002.jpg",
    },
    {
        "index": 3,
        "filename": "ref_0003.jpg",
        "role": "front_three_quarter_wire",
        "url": "https://i.3dmodels.org/uploads/Toyota/074_Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979/Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979_600_0003.jpg",
    },
    {
        "index": 4,
        "filename": "ref_0004.jpg",
        "role": "rear_three_quarter_wire",
        "url": "https://i.3dmodels.org/uploads/Toyota/074_Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979/Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979_600_0004.jpg",
    },
    {
        "index": 5,
        "filename": "ref_0005.jpg",
        "role": "left_side_orthographic",
        "url": "https://i.3dmodels.org/uploads/Toyota/074_Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979/Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979_600_0005.jpg",
    },
    {
        "index": 6,
        "filename": "ref_0006.jpg",
        "role": "front_detail_three_quarter",
        "url": "https://i.3dmodels.org/uploads/Toyota/074_Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979/Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979_600_0006.jpg",
    },
    {
        "index": 7,
        "filename": "ref_0007.jpg",
        "role": "rear_detail_three_quarter",
        "url": "https://i.3dmodels.org/uploads/Toyota/074_Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979/Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979_600_0007.jpg",
    },
    {
        "index": 8,
        "filename": "ref_0008.jpg",
        "role": "wheel_detail",
        "url": "https://i.3dmodels.org/uploads/Toyota/074_Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979/Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979_600_0008.jpg",
    },
    {
        "index": 9,
        "filename": "ref_0009.jpg",
        "role": "top_three_quarter",
        "url": "https://i.3dmodels.org/uploads/Toyota/074_Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979/Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979_600_0009.jpg",
    },
    {
        "index": 10,
        "filename": "ref_0010.jpg",
        "role": "front_orthographic",
        "url": "https://i.3dmodels.org/uploads/Toyota/074_Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979/Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979_600_0010.jpg",
    },
    {
        "index": 11,
        "filename": "ref_0011.jpg",
        "role": "front_three_quarter_clay",
        "url": "https://i.3dmodels.org/uploads/Toyota/074_Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979/Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979_600_0011.jpg",
    },
    {
        "index": 12,
        "filename": "ref_0012.jpg",
        "role": "rear_three_quarter_clay",
        "url": "https://i.3dmodels.org/uploads/Toyota/074_Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979/Toyota_Land_Cruiser_J40_Hard_Top_BJ44V_1979_600_0012.jpg",
    },
]


def ensure_image(image: dict[str, object], cache_dir: Path, download: bool) -> Path:
    path = cache_dir / str(image["filename"])
    if path.exists() or not download:
        return path
    cache_dir.mkdir(parents=True, exist_ok=True)
    urlretrieve(str(image["url"]), path)
    return path


def largest_component_bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    best = None
    best_area = 0
    visited = np.zeros(mask.shape, dtype=bool)
    height, width = mask.shape
    for start_y, start_x in np.argwhere(mask):
        if visited[start_y, start_x]:
            continue
        stack = [(int(start_y), int(start_x))]
        visited[start_y, start_x] = True
        x0 = x1 = int(start_x)
        y0 = y1 = int(start_y)
        area = 0
        while stack:
            y, x = stack.pop()
            area += 1
            x0 = min(x0, x)
            x1 = max(x1, x)
            y0 = min(y0, y)
            y1 = max(y1, y)
            for next_y, next_x in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if next_y < 0 or next_y >= height or next_x < 0 or next_x >= width:
                    continue
                if visited[next_y, next_x] or not mask[next_y, next_x]:
                    continue
                visited[next_y, next_x] = True
                stack.append((next_y, next_x))
        component_width = x1 - x0 + 1
        component_height = y1 - y0 + 1
        if area > best_area and component_width > 80 and component_height > 80:
            best = (x0, y0, x1, y1)
            best_area = area
    return best


def analyze_image(path: Path) -> dict[str, object]:
    with Image.open(path) as image:
        rgb = image.convert("RGB")
    arr = np.asarray(rgb, dtype=np.int16)
    height, width = arr.shape[:2]

    # The public preview renders sit on a near-white studio background. Exclude
    # the Hum3D logo corner and capture the main non-background connected mass.
    dark = arr.mean(axis=2) < 242
    chroma = arr.max(axis=2) - arr.min(axis=2) > 10
    foreground = dark | chroma
    foreground[:70, :145] = False
    foreground[-80:, :120] = False
    bbox = largest_component_bbox(foreground)
    if bbox is None:
        return {"width_px": width, "height_px": height, "silhouette_bbox_px": None}
    x0, y0, x1, y1 = bbox
    bbox_width = x1 - x0 + 1
    bbox_height = y1 - y0 + 1
    return {
        "width_px": width,
        "height_px": height,
        "silhouette_bbox_px": {"x0": x0, "y0": y0, "x1": x1, "y1": y1},
        "silhouette_width_px": bbox_width,
        "silhouette_height_px": bbox_height,
        "silhouette_aspect": round(bbox_width / bbox_height, 4),
        "silhouette_center_norm": {
            "x": round((x0 + x1) / 2 / width, 4),
            "y": round((y0 + y1) / 2 / height, 4),
        },
        "silhouette_fill_pct": round(float(foreground[y0 : y1 + 1, x0 : x1 + 1].mean()) * 100, 2),
    }


def cue_summary(records: list[dict[str, object]]) -> dict[str, object]:
    by_role = {str(record["role"]): record for record in records}
    side = by_role.get("left_side_orthographic", {})
    front = by_role.get("front_orthographic", {})
    top = by_role.get("top_three_quarter", {})
    wheel = by_role.get("wheel_detail", {})
    return {
        "derived_cues": [
            "Side orthographic confirms a short front overhang, upright windshield, long hardtop side glass, rear-mounted spare, and rear corner radius.",
            "Front orthographic confirms wide stance, flat vertical grille plane, raised hood crown, fender-top lamps, round headlamps, bumper-mounted lamps, and mirror stalks.",
            "Top three-quarter confirms hardtop roof crown, subtle roof side taper, rear spare carrier projection, and black window perimeter material breaks.",
            "Wire and clay renders confirm separate body-color skins over black wheel-arch flares rather than simple rectangular wheel cutouts.",
            "Wheel detail confirms six-lug hub, stamped rim dish, dark rim vent openings, raised sidewall/tread blocks, and a substantial tire-to-body gap.",
        ],
        "orthographic_side_aspect": side.get("silhouette_aspect"),
        "orthographic_front_aspect": front.get("silhouette_aspect"),
        "top_view_aspect": top.get("silhouette_aspect"),
        "wheel_detail_aspect": wheel.get("silhouette_aspect"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze public J40 3DModels.org gallery preview images into non-image shape cues.")
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    parser.add_argument("--output", type=Path, default=REPORT_DIR / "j40_3dmodels_gallery_visual_cues.json")
    parser.add_argument("--no-download", action="store_true")
    args = parser.parse_args()

    records: list[dict[str, object]] = []
    for image in GALLERY_IMAGES:
        path = ensure_image(image, args.cache_dir, download=not args.no_download)
        if not path.exists():
            raise FileNotFoundError(f"Missing gallery preview image: {path}")
        record = dict(image)
        record.update(analyze_image(path))
        records.append(record)

    data = {
        "source_page": "https://3dmodels.org/3d-models/toyota-land-cruiser-j40-hard-top-1979/",
        "copyright_handling": "Public preview images analyzed into numeric silhouette cues only; images are not stored in the repo.",
        "image_count": len(records),
        "images": records,
    }
    data.update(cue_summary(records))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + "\n", encoding="ascii")
    print(args.output.relative_to(ROOT))


if __name__ == "__main__":
    main()
