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
IMAGE_URL_HINT = re.compile(r"\.(?:jpg|jpeg|png|webp|gif|bmp)(?:\?|$)", re.IGNORECASE)
HTML_IMAGE_PATTERN = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']", re.IGNORECASE)
JSON_IMAGE_PATTERN = re.compile(r'"image"\s*:\s*"(https?://[^"]+)"', re.IGNORECASE)
JSON_IMAGE_LIST_PATTERN = re.compile(r'"image"\s*:\s*\[(.*?)\]', re.IGNORECASE | re.DOTALL)
STRING_URL_PATTERN = re.compile(r'"(https?://[^"]+)"')
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
REQUEST_TIMEOUT_SECONDS = 20
MAX_HTML_BYTES = 2_000_000
MAX_IMAGES_PER_LISTING = 3

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

SOURCE_URL_OVERRIDES: dict[tuple[str, str], tuple[str, ...]] = {
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

    expenses = load_csv(MANUAL_DIR / "expenses.csv")
    for row in expenses:
        bucket = clean(row.get("bucket")).lower()
        if bucket not in {"tools", "parts"}:
            continue
        values = [clean(value) for value in row.values()]
        rows.append(
            SourceRow(
                item_type="tool" if bucket == "tools" else "part",
                item=clean(row.get("item")),
                vendor=clean(row.get("company")),
                source_table="expenses",
                source_ref=clean(row.get("entry_id")),
                text_blob=" | ".join(values),
            )
        )

    procurement_queue = load_csv(MANUAL_DIR / "procurement_queue.csv")
    for row in procurement_queue:
        item = clean(row.get("item"))
        if not item:
            continue
        rows.append(
            SourceRow(
                item_type="part",
                item=item,
                vendor=clean(row.get("company")),
                source_table="procurement_queue",
                source_ref=clean(row.get("entry_id")),
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
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
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


def extension_for_content_type(content_type: str, fallback_url: str) -> str:
    lowered = clean(content_type).lower()
    if "image/jpeg" in lowered:
        return ".jpg"
    if "image/png" in lowered:
        return ".png"
    if "image/webp" in lowered:
        return ".webp"
    if "image/gif" in lowered:
        return ".gif"
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


def write_manifest(records: list[dict[str, str]]) -> None:
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
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


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
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    source_rows = read_source_rows()
    listing_contexts: dict[str, list[SourceRow]] = defaultdict(list)
    for row in source_rows:
        urls = row.explicit_urls if row.explicit_urls is not None else extract_urls(row.text_blob)
        override_urls = SOURCE_URL_OVERRIDES.get((row.source_table, row.source_ref), ())
        if override_urls:
            urls = list(dict.fromkeys([*urls, *override_urls]))
        if not urls:
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
                        "error": str(error),
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
                    ext = extension_for_content_type(content_type, image_url)
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
                            "error": str(error),
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
    write_manifest(records)
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
