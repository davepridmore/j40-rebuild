#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent.parent
MANUAL_DIR = ROOT / "data" / "manual"
WORKBOOK_TABS_DIR = MANUAL_DIR / "workbook_tabs"
OUTPUT_DIR = ROOT / "deliverables" / "selling_site_images"
OUTPUT_IMAGE_DIR = OUTPUT_DIR / "images"
MANIFEST_PATH = OUTPUT_DIR / "manifest.csv"
SUMMARY_PATH = OUTPUT_DIR / "summary.md"

URL_PATTERN = re.compile(r"https?://[^\s<>()\"']+")
IMAGE_URL_HINT = re.compile(r"\.(?:jpg|jpeg|png|webp|gif|bmp|avif)(?:\?|$)", re.IGNORECASE)
HTML_IMAGE_PATTERN = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']", re.IGNORECASE)
JSON_IMAGE_PATTERN = re.compile(r'"image"\s*:\s*"(https?://[^"]+)"', re.IGNORECASE)
JSON_IMAGE_LIST_PATTERN = re.compile(r'"image"\s*:\s*\[(.*?)\]', re.IGNORECASE | re.DOTALL)
STRING_URL_PATTERN = re.compile(r'"(https?://[^"]+)"')
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
REQUEST_TIMEOUT_SECONDS = 8
MAX_HTML_BYTES = 2_000_000
MAX_IMAGES_PER_LISTING = 1
ENABLE_DERIVED_VENDOR_SEARCH = False

LOCAL_CAPTURE_PATTERNS = (
    "blue_sea_5035*.jpg",
    "bluesea_5035*.jpg",
    "daraz_*.jpg",
    "ebay_*_photo.jpg",
    "junction_block*.png",
    ".tmp_toolsmart_order_contactsheet.jpg",
    "photos/Screenshot_*PakWheels*.jpg",
)

VENDOR_SEARCH_STOPWORDS = {
    "with",
    "without",
    "pack",
    "piece",
    "set",
    "kit",
    "for",
    "from",
    "and",
    "the",
    "plus",
    "inch",
    "mm",
    "pcs",
    "x",
}

EXACT_PRODUCT_PATH_HINTS = (
    "/product/",
    "/products/",
    "/item/",
    "/itm/",
    ".html",
)

SEARCH_OR_COLLECTION_HINTS = (
    "/catalog/",
    "/search",
    "/items/q",
    "/collections/",
    "/accessories-spare-parts/search",
)

SOURCE_URL_OVERRIDES: dict[tuple[str, str], tuple[str, ...]] = {
    (
        "workbook_parts",
        "row_64",
    ): (
        "https://fiaz.com.pk/wp-content/uploads/2024/12/i-y.jpeg.webp",
    ),
    (
        "workbook_parts",
        "row_65",
    ): (
        "https://fiaz.com.pk/wp-content/uploads/2024/12/ob.jpeg",
    ),
    (
        "workbook_parts",
        "row_66",
    ): (
        "https://fiaz.com.pk/wp-content/uploads/2024/12/i-b.jpeg",
    ),
    (
        "workbook_parts",
        "row_67",
    ): (
        "https://fiaz.com.pk/wp-content/uploads/2022/08/Insulated-Thimbles-female-lug.jpg",
    ),
    (
        "workbook_parts",
        "row_68",
    ): (
        "https://fiaz.com.pk/wp-content/uploads/2024/12/oc.jpeg",
    ),
    (
        "workbook_parts",
        "row_38",
    ): (
        "https://www.crescentelectric.com/product/609291/selector-switch-harmony-xb4-black-22mm-2-position-stay-put-1-no",
    ),
    (
        "workbook_parts",
        "row_39",
    ): (
        "https://www.crescentelectric.com/product/60230/selector-switch-harmony-xb4-metal-black-22mm-long-handle-3positions-stay-put-2no",
    ),
    (
        "expenses",
        "tool_powerhouse_ingco_wb30501_wire_cup_brush_x3",
    ): (
        "https://cdn.shopify.com/s/files/1/0726/3541/6891/files/ingco-wb30501-wire-cup-brush_compact_cropped.webp?v=1746223167",
    ),
    (
        "expenses",
        "tool_autohub_engine_detailing_brush_bundle_62191",
    ): (
        "https://cdn.shopify.com/s/files/1/0424/5433/products/images_41_medium.jpg?v=1628100978",
        "https://cdn.shopify.com/s/files/1/0424/5433/products/Detailing_Brush_313_medium.jpg?v=1579554135",
        "https://cdn.shopify.com/s/files/1/0424/5433/products/7691c2b9ca8b7d66b6c449e414abf235_medium.jpg?v=1574452742",
    ),
    (
        "expenses",
        "part_primer",
    ): (
        "https://pk-live-21.slatic.net/kf/Sb3943ecd4f6040c39d009641d24206143.jpg",
    ),
    (
        "expenses",
        "part_wax_and_grease_remover",
    ): (
        "https://cdn.shopify.com/s/files/1/0424/5433/files/3m-08983_medium.png?v=1709701797",
    ),
    (
        "expenses",
        "part_cavity_wax",
    ): (
        "https://cdn.shopify.com/s/files/1/0424/5433/files/WEB-900SPRi-Photoroom_1_medium.png?v=1731328302",
    ),
    (
        "expenses",
        "part_dot3_brake_fluid_autohub_6x354ml",
    ): (
        "https://cdn.shopify.com/s/files/1/0424/5433/files/BF-354_DOT_3_Brake_Fluid_12_Oz_medium.jpg?v=1700503745",
    ),
    (
        "expenses",
        "tool_daraz_75mm_knotted_cup_wire_brush_x2",
    ): (
        "https://static-01.daraz.pk/p/850e2884182b055b50caab1236d83335.jpg",
    ),
    (
        "expenses",
        "tool_daraz_mini_wire_brush_set_x2",
    ): (
        "https://static-01.daraz.pk/p/95852a2f111310f28a07fca1c54fe1e8.jpg",
    ),
    (
        "expenses",
        "tool_daraz_safety_goggles_cleanup",
    ): (
        "https://static-01.daraz.pk/p/6988bc488aa6f8214912cc5a51ec3f92.png",
    ),
    (
        "expenses",
        "part_daraz_jubilee_hose_clip_assortment_30pc",
    ): (
        "https://static-01.daraz.pk/p/ba3d027177170958c46096eff8c97f61.jpg",
    ),
    (
        "expenses",
        "tool_total_wrecking_bar_600mm_tht431242",
    ): (
        "https://www.toolsmart.pk/products/total-wrecking-bar-600mm-tht431242",
    ),
    (
        "expenses",
        "tool_wadfow_pressure_sprayer_wrs1550",
    ): (
        "https://www.toolsmart.pk/products/wadfow-pressure-sprayer-wrs1550",
    ),
    (
        "expenses",
        "tool_harden_spring_clamp_set_4in_6pc",
    ): (
        "https://www.toolsmart.pk/products/harden-6pc-x-4-spring-clamp-set",
    ),
    (
        "expenses",
        "tool_harden_white_rubber_mallet_700g_590437",
    ): (
        "https://www.toolsmart.pk/products/harden-white-rubber-mallet-with-firbregalss-handle-700g-590437",
    ),
    (
        "expenses",
        "tool_ingco_dead_blow_mallet_2lb_hdbm08028",
    ): (
        "https://www.toolsmart.pk/products/ingco-dead-blow-mallet-2lb-hdbm08028",
    ),
    (
        "expenses",
        "tool_wadfow_body_fender_hammer_set_whz1d07",
    ): (
        "https://www.toolsmart.pk/products/wadfow-7-pcs-body-and-fender-hammer-set-whz1d07",
    ),
    (
        "expenses",
        "tool_total_jack_stands_3ton_thjs0301_2pairs",
    ): (
        "https://www.toolsmart.pk/products/total-jack-stand-3ton-thjs0301",
    ),
    (
        "expenses",
        "tool_harden_3ton_trolley_jack_730213",
    ): (
        "https://www.toolsmart.pk/products/harden-3ton-hydraulic-trolley-jack-730213",
    ),
    (
        "expenses",
        "tool_total_round_steel_file_200mm_tht91386",
    ): (
        "https://www.toolsmart.pk/products/total-round-steel-file-tht91386",
    ),
    (
        "expenses",
        "tool_total_bi_metal_hole_saw_22mm_tac410221",
    ): (
        "https://www.toolsmart.pk/products/total-bi-metal-hole-saw-tac410221",
    ),
    (
        "expenses",
        "tool_harden_cup_wire_brush_100mm_m14",
    ): (
        "https://www.toolsmart.pk/products/harden-cup-wire-brush-with-nutsize100mm-x-m14x2-0",
    ),
    (
        "expenses",
        "tool_wadfow_abrasive_metal_grinding_disc_wac1353",
    ): (
        "https://www.toolsmart.pk/products/wadfow-abrasive-metal-grinding-disc-wac1353",
    ),
    (
        "expenses",
        "tool_harden_50lb_magnetic_welding_holder_765050",
    ): (
        "https://www.toolsmart.pk/products/harden-50lb-magnetic-welding-holder-765050",
    ),
    (
        "expenses",
        "tool_total_welding_leather_gloves_16_tsp15161",
    ): (
        "https://www.toolsmart.pk/products/total-welding-leather-gloves-16-tsp15161",
    ),
    (
        "expenses",
        "tool_wadfow_auto_darkening_welding_helmet_wwh3503",
    ): (
        "https://www.toolsmart.pk/products/wadfow-auto-darkening-welding-helmet-wwh3503",
    ),
    (
        "expenses",
        "tool_total_inverter_mma_welding_machine_tw220069",
    ): (
        "https://www.toolsmart.pk/products/total-inverter-mma-welding-machine-tw220069",
    ),
}


@dataclass
class SourceRow:
    item_type: str
    item: str
    vendor: str
    source_table: str
    source_ref: str
    text_blob: str
    explicit_urls: list[str] | None = None


def clean(value: object) -> str:
    return str(value or "").strip()


def clean_error(value: object) -> str:
    return str(value or "").rstrip()


def slugify(value: str) -> str:
    lowered = clean(value).lower()
    lowered = re.sub(r"[^a-z0-9]+", "_", lowered)
    lowered = re.sub(r"_+", "_", lowered).strip("_")
    return lowered or "item"


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def extract_urls(text: str) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for match in URL_PATTERN.findall(text):
        candidate = match.strip().rstrip(".,;:)]}>")
        if not candidate:
            continue
        if candidate in seen:
            continue
        seen.add(candidate)
        urls.append(candidate)
    return urls


def is_likely_exact_product_url(url: str) -> bool:
    parsed = urllib.parse.urlparse(clean(url))
    path = parsed.path.lower()
    if not parsed.scheme or not parsed.netloc:
        return False
    if IMAGE_URL_HINT.search(url):
        return True
    if any(hint in path for hint in SEARCH_OR_COLLECTION_HINTS):
        return False
    return any(hint in path for hint in EXACT_PRODUCT_PATH_HINTS)


def extract_ebay_reference_urls(page_text: str) -> list[str]:
    urls = extract_urls(page_text)
    filtered = [
        url
        for url in urls
        if "ebay." in url.lower() or "ebayimg." in url.lower()
    ]
    filtered = [url for url in filtered if not any(token in url.lower() for token in (".css", ".js", ".svg", ".woff", ".ttf"))]
    # Keep only the canonical listing page plus a small set of direct image candidates.
    listing_urls = [url for url in filtered if re.search(r"/itm/\d+", url)]
    image_urls = [url for url in filtered if IMAGE_URL_HINT.search(url)]
    output: list[str] = []
    seen: set[str] = set()
    for candidate in listing_urls[:2] + image_urls[:8]:
        if candidate in seen:
            continue
        seen.add(candidate)
        output.append(candidate)
    return output


def query_terms_from_item(item: str, max_terms: int = 8) -> str:
    tokens: list[str] = []
    for token in re.findall(r"[a-z0-9]+", item.lower()):
        if token in VENDOR_SEARCH_STOPWORDS:
            continue
        if len(token) < 2:
            continue
        tokens.append(token)
        if len(tokens) >= max_terms:
            break
    return " ".join(tokens)


def derived_vendor_urls(row: SourceRow) -> list[str]:
    vendor = clean(row.vendor).lower()
    item = clean(row.item)
    query = query_terms_from_item(item)
    if not query:
        return []

    encoded = urllib.parse.quote_plus(query)
    urls: list[str] = []

    if "toolsmart.pk" in vendor:
        urls.append(f"https://www.toolsmart.pk/search?type=product&q={encoded}")
    if any(domain in vendor for domain in ("fiaz.com.pk", "ngcotool.pk", "almirajtrading.com.pk", "purchaser.com.pk", "totaltool.pk")):
        domain_match = re.search(r"([a-z0-9.-]+\.[a-z]{2,})", vendor)
        if domain_match:
            domain = domain_match.group(1)
            urls.append(f"https://{domain}/?s={encoded}&post_type=product")
            urls.append(f"https://{domain}/search?q={encoded}")

    return list(dict.fromkeys(urls))


def read_source_rows() -> list[SourceRow]:
    rows: list[SourceRow] = []

    workbook_tools = load_csv(WORKBOOK_TABS_DIR / "tools.csv")
    for row in workbook_tools:
        item = clean(row.get("col_1"))
        if not item or item.lower() == "item":
            continue
        values = [clean(value) for value in row.values()]
        rows.append(
            SourceRow(
                item_type="tool",
                item=item,
                vendor=clean(row.get("col_3")),
                source_table="workbook_tools",
                source_ref=f"row_{clean(row.get('excel_row'))}",
                text_blob=" | ".join(values),
            )
        )

    workbook_parts = load_csv(WORKBOOK_TABS_DIR / "parts.csv")
    for row in workbook_parts:
        item = clean(row.get("col_1"))
        if not item or item.lower() == "item":
            continue
        values = [clean(value) for value in row.values()]
        rows.append(
            SourceRow(
                item_type="part",
                item=item,
                vendor=clean(row.get("col_3")),
                source_table="workbook_parts",
                source_ref=f"row_{clean(row.get('excel_row'))}",
                text_blob=" | ".join(values),
            )
        )

    link_tab_configs = (
        ("pk_buy_clean_direct", "col_2"),
        ("pk_quality_path", "col_2"),
        ("rubbers_exact_online", "col_1"),
        ("rubbers_kit_buy", "col_1"),
        ("rubbers_all_replace_links", "col_1"),
    )
    for source_table, item_column in link_tab_configs:
        for row in load_csv(WORKBOOK_TABS_DIR / f"{source_table}.csv"):
            item = clean(row.get(item_column))
            if not item or item.lower() in {"item", "item_group", "kit_name"}:
                continue
            values = [clean(value) for value in row.values()]
            exact_urls = [url for url in extract_urls(" | ".join(values)) if is_likely_exact_product_url(url)]
            if not exact_urls:
                continue
            rows.append(
                SourceRow(
                    item_type="part",
                    item=item,
                    vendor="workbook_link",
                    source_table=source_table,
                    source_ref=f"row_{clean(row.get('excel_row'))}",
                    text_blob=" | ".join(values),
                    explicit_urls=exact_urls,
                )
            )

    expenses = load_csv(MANUAL_DIR / "expenses.csv")
    expense_source_refs: set[str] = set()
    for row in expenses:
        bucket = clean(row.get("bucket")).lower()
        if bucket not in {"tools", "parts"}:
            continue
        entry_id = clean(row.get("entry_id"))
        if entry_id:
            expense_source_refs.add(entry_id)
        values = [clean(value) for value in row.values()]
        rows.append(
            SourceRow(
                item_type="tool" if bucket == "tools" else "part",
                item=clean(row.get("item")),
                vendor=clean(row.get("company")),
                source_table="expenses",
                source_ref=entry_id,
                text_blob=" | ".join(values),
            )
        )

    procurement_queue = load_csv(MANUAL_DIR / "procurement_queue.csv")
    for row in procurement_queue:
        entry_id = clean(row.get("entry_id"))
        if entry_id in expense_source_refs:
            continue
        item = clean(row.get("item"))
        if not item:
            continue
        rows.append(
            SourceRow(
                item_type="part",
                item=item,
                vendor=clean(row.get("company")),
                source_table="procurement_queue",
                source_ref=entry_id,
                text_blob=" | ".join(clean(value) for value in row.values()),
            )
        )

    daraz_urls_path = ROOT / "daraz_6way_urls.txt"
    if daraz_urls_path.exists():
        text = daraz_urls_path.read_text(encoding="utf-8", errors="ignore")
        rows.append(
            SourceRow(
                item_type="part",
                item="Daraz 6-way fuse box references",
                vendor="Daraz",
                source_table="daraz_6way_urls",
                source_ref="file",
                text_blob=text,
            )
        )

    ebay_page_path = ROOT / "ebay_yaris_cover.html"
    if ebay_page_path.exists():
        text = ebay_page_path.read_text(encoding="utf-8", errors="ignore")
        explicit_urls = extract_ebay_reference_urls(text)
        rows.append(
            SourceRow(
                item_type="part",
                item="eBay Yaris/Vitz fuse box cover reference",
                vendor="eBay",
                source_table="ebay_yaris_cover_html",
                source_ref="file",
                text_blob="",
                explicit_urls=explicit_urls,
            )
        )

    relevant_messages = load_csv(ROOT / "data" / "processed" / "generated" / "relevant_messages.csv")
    for row in relevant_messages:
        text = clean(row.get("text"))
        if not text:
            continue
        urls = extract_urls(text)
        if not urls:
            continue
        blob = " | ".join(clean(value) for value in row.values()).lower()
        if not any(token in blob for token in ("toolsmart", "toolsmart", "daraz", "ebay", "aliexpress", "pakwheels")):
            continue
        item_type = "tool" if any(token in blob for token in ("toolsmart", "toolsmart")) else "part"
        rows.append(
            SourceRow(
                item_type=item_type,
                item=text[:120],
                vendor="chat_reference",
                source_table="relevant_messages",
                source_ref=clean(row.get("message_id")),
                text_blob=text,
                explicit_urls=urls,
            )
        )

    return rows


def build_request(url: str) -> urllib.request.Request:
    return urllib.request.Request(
        url=url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/png,image/jpeg,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )


def fetch_bytes(url: str) -> tuple[bytes, str]:
    request = build_request(url)
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        content_type = clean(response.headers.get("Content-Type")).lower()
        payload = response.read(MAX_HTML_BYTES)
        return payload, content_type


def parse_meta_image_candidates(html_text: str) -> list[str]:
    candidates: list[str] = []
    seen: set[str] = set()

    meta_tags = re.findall(r"<meta\s+[^>]*>", html_text, re.IGNORECASE)
    for tag in meta_tags:
        lowered = tag.lower()
        if not any(token in lowered for token in ("og:image", "twitter:image", "itemprop=\"image\"", "itemprop='image'")):
            continue
        match = re.search(r'content=["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if not match:
            continue
        candidate = html.unescape(match.group(1)).strip()
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        candidates.append(candidate)

    for candidate in JSON_IMAGE_PATTERN.findall(html_text):
        unescaped = html.unescape(candidate).strip()
        if not unescaped or unescaped in seen:
            continue
        seen.add(unescaped)
        candidates.append(unescaped)

    for image_list_blob in JSON_IMAGE_LIST_PATTERN.findall(html_text):
        for candidate in STRING_URL_PATTERN.findall(image_list_blob):
            unescaped = html.unescape(candidate).strip()
            if not unescaped or unescaped in seen:
                continue
            seen.add(unescaped)
            candidates.append(unescaped)

    for candidate in HTML_IMAGE_PATTERN.findall(html_text):
        unescaped = html.unescape(candidate).strip()
        if not unescaped or unescaped.startswith("data:") or unescaped in seen:
            continue
        seen.add(unescaped)
        candidates.append(unescaped)

    return candidates


def score_image_url(url: str) -> tuple[int, int]:
    lowered = url.lower()
    score = 0
    if IMAGE_URL_HINT.search(lowered):
        score += 30
    if any(token in lowered for token in ("product", "listing", "ebayimg", "image", "gallery", "media")):
        score += 8
    if any(token in lowered for token in ("logo", "icon", "sprite", "avatar", "placeholder")):
        score -= 16
    if any(
        token in lowered
        for token in (
            "facebook",
            "youtube",
            "google-play",
            "qr",
            "qrcode",
            "cropped-",
            "favicon",
            "social",
        )
    ):
        score -= 28
    return score, -len(lowered)


def resolve_listing_image_urls(listing_url: str) -> tuple[list[str], str]:
    cleaned_url = clean(listing_url)
    if not cleaned_url:
        return [], "empty_url"
    if IMAGE_URL_HINT.search(cleaned_url):
        return [cleaned_url], "direct_image_url"

    payload, content_type = fetch_bytes(cleaned_url)
    if content_type.startswith("image/"):
        return [cleaned_url], "direct_image_response"

    text = payload.decode("utf-8", errors="ignore")
    raw_candidates = parse_meta_image_candidates(text)
    candidates: list[str] = []
    seen: set[str] = set()
    for candidate in raw_candidates:
        absolute = urllib.parse.urljoin(cleaned_url, candidate)
        if absolute in seen:
            continue
        if not absolute.startswith("http"):
            continue
        seen.add(absolute)
        candidates.append(absolute)

    candidates.sort(key=score_image_url, reverse=True)
    return candidates[:MAX_IMAGES_PER_LISTING], "html_extract"


def sniff_image_extension(payload: bytes) -> str:
    if payload.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if payload.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if payload.startswith(b"GIF87a") or payload.startswith(b"GIF89a"):
        return ".gif"
    if payload.startswith(b"RIFF") and payload[8:12] == b"WEBP":
        return ".webp"
    if b"ftypavif" in payload[:32]:
        return ".avif"
    return ""


def extension_for_content_type(content_type: str, fallback_url: str, payload: bytes = b"") -> str:
    sniffed = sniff_image_extension(payload)
    if sniffed:
        return sniffed
    lowered = clean(content_type).lower()
    if "image/jpeg" in lowered:
        return ".jpg"
    if "image/png" in lowered:
        return ".png"
    if "image/webp" in lowered:
        return ".webp"
    if "image/gif" in lowered:
        return ".gif"
    if "image/avif" in lowered:
        return ".avif"
    parsed = urllib.parse.urlparse(fallback_url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}:
        return ".jpg" if suffix == ".jpeg" else suffix
    return ".jpg"


def download_image(url: str) -> tuple[bytes, str]:
    payload, content_type = fetch_bytes(url)
    if not content_type.startswith("image/") and not IMAGE_URL_HINT.search(url):
        raise ValueError(f"non_image_response:{content_type or 'unknown'}")
    return payload, content_type


def copy_local_capture_images() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for pattern in LOCAL_CAPTURE_PATTERNS:
        for source_path in sorted(ROOT.glob(pattern)):
            if not source_path.is_file():
                continue
            target_name = source_path.name
            target_path = OUTPUT_IMAGE_DIR / target_name
            shutil.copy2(source_path, target_path)
            lowered_name = target_name.lower()
            item_type = "tool" if "toolsmart" in lowered_name else "part"
            if "pakwheels" in lowered_name or "blue_sea" in lowered_name or "ebay" in lowered_name or "daraz" in lowered_name:
                item_type = "part"
            records.append(
                {
                    "item_type": item_type,
                    "item": source_path.stem,
                    "vendor": "local_capture",
                    "source_table": "repo_local_capture",
                    "source_ref": clean(source_path.relative_to(ROOT)),
                    "listing_url": "",
                    "image_url": "",
                    "local_path": clean(target_path.relative_to(ROOT)),
                    "status": "copied_local",
                    "error": "",
                }
            )
    return records


def write_manifest(records: list[dict[str, str]]) -> list[dict[str, str]]:
    fieldnames = [
        "item_type",
        "item",
        "vendor",
        "source_table",
        "source_ref",
        "listing_url",
        "image_url",
        "local_path",
        "status",
        "error",
    ]
    deduped_records: list[dict[str, str]] = []
    seen: set[tuple[str, ...]] = set()
    for row in records:
        key = tuple(clean(row.get(fieldname)) for fieldname in fieldnames)
        if key in seen:
            continue
        seen.add(key)
        deduped_records.append(row)
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(deduped_records)
    return deduped_records


def write_summary(records: list[dict[str, str]], source_row_count: int, unique_url_count: int) -> None:
    by_status: dict[str, int] = defaultdict(int)
    by_item_type: dict[str, int] = defaultdict(int)
    for row in records:
        by_status[row["status"]] += 1
        by_item_type[row["item_type"]] += 1

    lines: list[str] = []
    lines.append("# Selling-Site Images Export")
    lines.append("")
    lines.append(f"- Source rows scanned: {source_row_count}")
    lines.append(f"- Unique listing URLs found: {unique_url_count}")
    lines.append(f"- Exported records: {len(records)}")
    lines.append("")
    lines.append("## Counts by Item Type")
    lines.append("")
    for item_type in sorted(by_item_type):
        lines.append(f"- `{item_type}`: {by_item_type[item_type]}")
    lines.append("")
    lines.append("## Counts by Status")
    lines.append("")
    for status in sorted(by_status):
        lines.append(f"- `{status}`: {by_status[status]}")
    lines.append("")
    lines.append("- Manifest: `deliverables/selling_site_images/manifest.csv`")
    lines.append("- Images folder: `deliverables/selling_site_images/images/`")
    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    OUTPUT_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    source_rows = read_source_rows()
    listing_contexts: dict[str, list[SourceRow]] = defaultdict(list)
    for row in source_rows:
        urls = row.explicit_urls if row.explicit_urls is not None else extract_urls(row.text_blob)
        override_urls = SOURCE_URL_OVERRIDES.get((row.source_table, row.source_ref), ())
        if override_urls:
            urls = list(dict.fromkeys(override_urls))
        if not urls and ENABLE_DERIVED_VENDOR_SEARCH:
            urls = derived_vendor_urls(row)
        for url in urls:
            listing_contexts[url].append(row)

    records: list[dict[str, str]] = []
    records.extend(copy_local_capture_images())

    listing_to_image_urls: dict[str, list[str]] = {}
    listing_resolution_mode: dict[str, str] = {}
    for listing_url in sorted(listing_contexts):
        try:
            image_urls, mode = resolve_listing_image_urls(listing_url)
            listing_to_image_urls[listing_url] = image_urls
            listing_resolution_mode[listing_url] = mode
        except Exception as error:  # noqa: BLE001
            listing_to_image_urls[listing_url] = []
            listing_resolution_mode[listing_url] = f"resolve_error:{type(error).__name__}"
            for ctx in listing_contexts[listing_url]:
                records.append(
                    {
                        "item_type": ctx.item_type,
                        "item": ctx.item,
                        "vendor": ctx.vendor,
                        "source_table": ctx.source_table,
                        "source_ref": ctx.source_ref,
                        "listing_url": listing_url,
                        "image_url": "",
                        "local_path": "",
                        "status": "resolve_failed",
                        "error": clean_error(error),
                    }
                )

    image_url_to_saved_path: dict[str, str] = {}
    content_hash_to_saved_path: dict[str, str] = {}

    for listing_url, contexts in sorted(listing_contexts.items()):
        image_urls = listing_to_image_urls.get(listing_url, [])
        if not image_urls:
            for ctx in contexts:
                if any(
                    row["listing_url"] == listing_url
                    and row["source_table"] == ctx.source_table
                    and row["source_ref"] == ctx.source_ref
                    and row["status"] in {"resolve_failed"}
                    for row in records
                ):
                    continue
                records.append(
                    {
                        "item_type": ctx.item_type,
                        "item": ctx.item,
                        "vendor": ctx.vendor,
                        "source_table": ctx.source_table,
                        "source_ref": ctx.source_ref,
                        "listing_url": listing_url,
                        "image_url": "",
                        "local_path": "",
                        "status": "no_image_found",
                        "error": listing_resolution_mode.get(listing_url, "no_candidates"),
                    }
                )
            continue

        for image_url in image_urls:
            if image_url in image_url_to_saved_path:
                saved_rel = image_url_to_saved_path[image_url]
                for ctx in contexts:
                    records.append(
                        {
                            "item_type": ctx.item_type,
                            "item": ctx.item,
                            "vendor": ctx.vendor,
                            "source_table": ctx.source_table,
                            "source_ref": ctx.source_ref,
                            "listing_url": listing_url,
                            "image_url": image_url,
                            "local_path": saved_rel,
                            "status": "reused_cached_image",
                            "error": "",
                        }
                    )
                continue

            try:
                payload, content_type = download_image(image_url)
                payload_hash = hashlib.sha256(payload).hexdigest()
                if payload_hash in content_hash_to_saved_path:
                    saved_rel = content_hash_to_saved_path[payload_hash]
                else:
                    ext = extension_for_content_type(content_type, image_url, payload)
                    contexts_slug = slugify(contexts[0].item)[:40]
                    source_slug = slugify(contexts[0].source_table)
                    name = f"{source_slug}_{contexts_slug}_{payload_hash[:12]}{ext}"
                    target_path = OUTPUT_IMAGE_DIR / name
                    target_path.write_bytes(payload)
                    saved_rel = clean(target_path.relative_to(ROOT))
                    content_hash_to_saved_path[payload_hash] = saved_rel
                image_url_to_saved_path[image_url] = saved_rel

                for ctx in contexts:
                    records.append(
                        {
                            "item_type": ctx.item_type,
                            "item": ctx.item,
                            "vendor": ctx.vendor,
                            "source_table": ctx.source_table,
                            "source_ref": ctx.source_ref,
                            "listing_url": listing_url,
                            "image_url": image_url,
                            "local_path": saved_rel,
                            "status": "downloaded",
                            "error": "",
                        }
                    )
            except Exception as error:  # noqa: BLE001
                for ctx in contexts:
                    records.append(
                        {
                            "item_type": ctx.item_type,
                            "item": ctx.item,
                            "vendor": ctx.vendor,
                            "source_table": ctx.source_table,
                            "source_ref": ctx.source_ref,
                            "listing_url": listing_url,
                            "image_url": image_url,
                            "local_path": "",
                            "status": "download_failed",
                            "error": clean_error(error),
                        }
                    )

    records.sort(
        key=lambda row: (
            row["item_type"],
            row["source_table"],
            row["source_ref"],
            row["item"].lower(),
            row["status"],
            row["listing_url"],
            row["image_url"],
        )
    )
    records = write_manifest(records)
    write_summary(records, source_row_count=len(source_rows), unique_url_count=len(listing_contexts))

    print(f"Wrote images folder: {OUTPUT_IMAGE_DIR.relative_to(ROOT)}")
    print(f"Wrote manifest: {MANIFEST_PATH.relative_to(ROOT)}")
    print(f"Wrote summary: {SUMMARY_PATH.relative_to(ROOT)}")
    print(f"Source rows scanned: {len(source_rows)}")
    print(f"Unique listing URLs: {len(listing_contexts)}")
    print(f"Manifest rows: {len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
