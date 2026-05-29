from __future__ import annotations

import csv
import html
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
MANUAL_DIR = ROOT / "data" / "manual"
EXPENSES_PATH = MANUAL_DIR / "expenses.csv"
PROCUREMENT_QUEUE_PATH = MANUAL_DIR / "procurement_queue.csv"

URL_PATTERN = re.compile(r"https?://[^\s\"'<>|]+", flags=re.IGNORECASE)
PRODUCT_LABEL_PATTERN = re.compile(
    r"\b(?:exact\s+)?(?:product\s+links?|links?)\s*:",
    flags=re.IGNORECASE,
)
IMAGE_LABEL_PATTERN = re.compile(r"\bimages?\s*:", flags=re.IGNORECASE)
TRAILING_URL_CHARS = ".,;:)]}>\"'"

BOUGHT_OR_SELECTED_STAGES = {
    "ordered_pending_delivery",
    "ordered_partial_pending_delivery",
    "purchase_ready",
    "received",
    "received_candidate",
    "completed",
}
BOUGHT_OR_SELECTED_STATUSES = {
    "ordered",
    "paid",
    "purchased",
    "received",
    "installed",
    "received_candidate",
}
EXCLUDED_STAGES = {"not_required", "not_required_split_to_component_tool_rows"}
EXCLUDED_STATUS_PREFIXES = ("not_required", "deferred")
PRODUCT_DOMAINS = {
    "aliexpress.com",
    "www.aliexpress.com",
    "daraz.pk",
    "www.daraz.pk",
    "autohub.pk",
    "www.autohub.pk",
    "automize.pk",
    "www.automize.pk",
    "toolsmart.pk",
    "www.toolsmart.pk",
    "powerhouseexpress.com.pk",
    "www.powerhouseexpress.com.pk",
    "pakwheels.com",
    "www.pakwheels.com",
    "almirajtrading.com.pk",
    "www.almirajtrading.com.pk",
    "wellshop.pk",
    "www.wellshop.pk",
    "sehgalmotors.pk",
    "www.sehgalmotors.pk",
}
PRODUCT_PATH_HINTS = (
    "/i/",
    "/item/",
    "/items/",
    "/product/",
    "/products/",
    "/accessories-spare-parts/",
)
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg")


def clean(value: object) -> str:
    return str(value or "").strip()


def norm(value: object) -> str:
    return clean(value).lower()


def clean_url(value: str) -> str:
    return html.unescape(clean(value)).rstrip(TRAILING_URL_CHARS)


def extract_urls(value: str) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for match in URL_PATTERN.findall(clean(value)):
        url = clean_url(match)
        if not url or url in seen:
            continue
        seen.add(url)
        urls.append(url)
    return urls


def is_image_url(url: str) -> bool:
    parsed = urlparse(clean_url(url))
    path = parsed.path.lower()
    if path.endswith(IMAGE_EXTENSIONS):
        return True
    return parsed.netloc.lower().endswith("slatic.net")


def is_product_url(url: str) -> bool:
    url = clean_url(url)
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    if is_image_url(url):
        return False
    if host not in PRODUCT_DOMAINS:
        return False
    return any(hint in path for hint in PRODUCT_PATH_HINTS)


def merge_urls(*groups: list[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for group in groups:
        for url in group:
            clean_candidate = clean_url(url)
            if not clean_candidate or clean_candidate in seen:
                continue
            seen.add(clean_candidate)
            merged.append(clean_candidate)
    return merged


def labeled_product_links(text: str) -> list[str]:
    links: list[str] = []
    for label_match in PRODUCT_LABEL_PATTERN.finditer(clean(text)):
        segment = text[label_match.end() :]
        segment = segment.split("|", 1)[0]
        image_match = IMAGE_LABEL_PATTERN.search(segment)
        if image_match:
            segment = segment[: image_match.start()]
        links.extend(url for url in extract_urls(segment) if is_product_url(url))
    return merge_urls(links)


def row_can_use_unlabeled_product_links(row: dict[str, str]) -> bool:
    stage = norm(row.get("procurement_stage"))
    status = norm(row.get("status"))
    payment = norm(row.get("payment_status"))
    delivery = norm(row.get("delivery_status"))

    if stage in EXCLUDED_STAGES or any(stage.startswith(prefix) for prefix in EXCLUDED_STATUS_PREFIXES):
        return False
    if status in EXCLUDED_STAGES or any(status.startswith(prefix) for prefix in EXCLUDED_STATUS_PREFIXES):
        return False
    if delivery == "not_required":
        return False

    return (
        stage in BOUGHT_OR_SELECTED_STAGES
        or status in BOUGHT_OR_SELECTED_STATUSES
        or payment in {"paid", "cod"}
        or delivery in {"received", "installed", "completed"}
    )


def row_product_links(row: dict[str, str]) -> list[str]:
    existing_links = [url for url in extract_urls(row.get("product_link", "")) if is_product_url(url)]
    labeled_links = labeled_product_links(row.get("notes", ""))
    if labeled_links:
        return merge_urls(existing_links, labeled_links)

    if not row_can_use_unlabeled_product_links(row):
        return merge_urls(existing_links)

    evidence_links = []
    for field in ("evidence_ref", "source", "notes"):
        evidence_links.extend(extract_urls(row.get(field, "")))
    product_links = [url for url in evidence_links if is_product_url(url)]
    return merge_urls(existing_links, product_links)


def insert_field_before(fieldnames: list[str], field: str, before: str) -> list[str]:
    if field in fieldnames:
        return fieldnames
    output = list(fieldnames)
    try:
        index = output.index(before)
    except ValueError:
        output.append(field)
    else:
        output.insert(index, field)
    return output


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def populate_expenses() -> tuple[dict[str, str], int]:
    fieldnames, rows = read_csv(EXPENSES_PATH)
    fieldnames = insert_field_before(fieldnames, "product_link", "notes")
    product_link_by_entry_id: dict[str, str] = {}
    changed = 0

    for row in rows:
        links = row_product_links(row)
        product_link = " | ".join(links)
        if row.get("product_link", "") != product_link:
            changed += 1
        row["product_link"] = product_link
        if product_link:
            product_link_by_entry_id[clean(row.get("entry_id"))] = product_link

    write_csv(EXPENSES_PATH, fieldnames, rows)
    return product_link_by_entry_id, changed


def populate_procurement_queue(product_link_by_entry_id: dict[str, str]) -> int:
    if not PROCUREMENT_QUEUE_PATH.exists():
        return 0

    fieldnames, rows = read_csv(PROCUREMENT_QUEUE_PATH)
    fieldnames = insert_field_before(fieldnames, "product_link", "notes")
    changed = 0

    for row in rows:
        existing = clean(row.get("product_link"))
        product_link = product_link_by_entry_id.get(clean(row.get("entry_id"))) or " | ".join(row_product_links(row))
        if existing != product_link:
            changed += 1
        row["product_link"] = product_link

    write_csv(PROCUREMENT_QUEUE_PATH, fieldnames, rows)
    return changed


def main() -> None:
    product_link_by_entry_id, expenses_changed = populate_expenses()
    procurement_changed = populate_procurement_queue(product_link_by_entry_id)
    print(f"Populated product_link for {len(product_link_by_entry_id)} expense rows.")
    print(f"Expense rows changed: {expenses_changed}")
    print(f"Procurement queue rows changed: {procurement_changed}")


if __name__ == "__main__":
    main()
