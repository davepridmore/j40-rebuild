#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
GENERATED_DIR = ROOT / "data" / "processed" / "generated"

MESSAGES_CSV_PATH = GENERATED_DIR / "mcp_whatsapp_j40_messages.csv"
MEDIA_CSV_PATH = GENERATED_DIR / "mcp_whatsapp_j40_media_index.csv"

PROJECT_CHAT_HINTS = {"fj40", "j50", "fj50", "akbar", "akber", "uk david"}
EXCLUDED_CHAT_NAME_TERMS = {
    "support engineer placement",
    "andy pointon bell",
}

PROJECT_TERMS = {
    "fj40",
    "j40",
    "j50",
    "fj50",
    "land cruiser",
    "landcruiser",
    "chassis",
    "bodyshop",
    "suspension",
    "leaf spring",
    "spring",
    "shackle",
    "steering",
    "wiring",
    "loom",
    "connector",
    "headlight",
    "taillight",
    "brake",
    "clutch",
    "radiator",
    "hose",
    "engine",
    "2f",
    "gearbox",
    "paint",
    "primer",
    "epoxy",
    "rust",
    "weld",
    "welding",
    "dashboard",
    "firewall",
    "fuse",
    "relay",
    "ground strap",
    "harness",
    "battery",
    "alternator",
    "shock",
    "coil",
    "winch",
    "axle",
    "differential",
    "driveshaft",
    "body mount",
    "bench grinder",
    "grease gun",
}

SUPPLIER_TERMS = {
    "supplier",
    "quote",
    "quotation",
    "order",
    "invoice",
    "purchase",
    "payment",
    "paid",
    "transfer",
    "account title",
    "account number",
    "iban",
    "toolsmart",
    "daraz",
    "aliexpress",
    "autohub",
    "happilac",
    "ironman",
    "coolsun",
    "carnation",
    "walton",
    "auto xpert",
}

PAYMENT_TERMS = {
    "account title",
    "account number",
    "iban",
    "bank",
    "payment",
    "paid",
    "transfer",
    "deposit",
    "balance",
    "receipt",
    "advance",
    "pkr",
    "rs",
}

PURCHASE_TERMS = {
    "product",
    "quantity",
    "total",
    "price",
    "cart",
    "checkout",
    "order list",
    "buy now",
    "shopping list",
}

TASK_TERMS = {
    "need to",
    "please can you",
    "please",
    "can you",
    "check",
    "follow up",
    "arrange",
    "send",
    "confirm",
    "order",
    "buy",
    "get this",
    "do this",
}

STATUS_TERMS = {
    "done",
    "completed",
    "pending",
    "in progress",
    "waiting",
    "arrived",
    "delivered",
    "received",
    "updated",
    "progress",
    "next step",
    "tomorrow",
    "today",
}

STRONG_EXCLUSION_TERMS = {
    "hsbc",
    "companies house",
    "company house",
    "hmrc",
    "corporation tax",
    "tax return",
    "self assessment",
    "vat return",
    "opening hours",
    "company hours",
    "business hours",
    "band transactions",
    "bank transaction entry",
}

SOFT_EXCLUSION_TERMS = {
    "statement entry",
    "salary",
    "payroll",
    "mortgage",
    "credit card payment",
    "utility bill",
}

EXAMPLE_TERMS = {
    "example",
    "reference",
    "inspiration",
    "other car",
    "another car",
    "for sale",
    "listing",
    "white car",
    "black car",
    "pakwheels",
    "look at this",
    "see this",
    "this guy",
    "import houses",
    "interiors",
    "upholstery",
    "like this",
    "similar build",
}

EXAMPLE_CONTEXT_TERMS = {"build", "restoration", "project", "chassis", "suspension"}

PART_NUMBER_PATTERNS = [
    re.compile(r"\b[A-Z]{1,4}-?\d{2,}[A-Z0-9-]*\b", re.IGNORECASE),
    re.compile(r"\b(?:M\d{1,2}|AWG\s?\d{1,2})\b", re.IGNORECASE),
    re.compile(r"\b\d+(?:\.\d+)?\s?(?:mm|cm|inch|inches|l|liters?|pcs?|pc|amp|a|w|v)\b", re.IGNORECASE),
    re.compile(r"\b(?:OEM|SKU|PN|P/N)\s*[:#-]?\s*[A-Z0-9-]{3,}\b", re.IGNORECASE),
]

CURRENCY_PATTERN = re.compile(r"(?:(?:^|\\b)(?:rs\\.?|pkr|usd|gbp|eur)(?:\\b|$)|[$£€])", re.IGNORECASE)
ACCOUNT_PATTERN = re.compile(r"\b(account(?: title| number)?|iban|swift|bank)\b", re.IGNORECASE)


def clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def norm(value: Any) -> str:
    return clean(value).lower()


def clean_text(value: Any) -> str:
    return " ".join(clean(value).replace("\u200e", " ").split())


def has_term(text: str, term: str) -> bool:
    if not term:
        return False
    if " " in term:
        return term in text
    return re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", text) is not None


def term_hits(text: str, terms: set[str]) -> list[str]:
    return sorted({term for term in terms if has_term(text, term)})


def detect_part_number_hits(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in PART_NUMBER_PATTERNS:
        if pattern.search(text):
            hits.append("part_number_pattern")
            break
    return hits


def choose_baseline_messages_csv(explicit_path: str | None) -> Path | None:
    if explicit_path:
        candidate = Path(explicit_path)
        return candidate if candidate.exists() else None

    snapshots = sorted(GENERATED_DIR.glob("mcp_whatsapp_j40_messages.before*.csv"), reverse=True)
    if snapshots:
        return snapshots[0]
    return None


def load_csv_rows(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def classify_message(row: dict[str, Any]) -> tuple[str, str, list[str]] | None:
    text_raw = clean_text(row.get("clean_text") or row.get("body"))
    if not text_raw:
        return None

    text = norm(text_raw)
    chat_name = norm(row.get("chat_name"))
    if chat_name.startswith("+971") or any(term in chat_name for term in EXCLUDED_CHAT_NAME_TERMS):
        return None
    project_chat = any(hint in chat_name for hint in PROJECT_CHAT_HINTS)

    project_hits = term_hits(text, PROJECT_TERMS)
    supplier_hits = term_hits(text, SUPPLIER_TERMS)
    payment_hits = term_hits(text, PAYMENT_TERMS)
    purchase_hits = term_hits(text, PURCHASE_TERMS)
    task_hits = term_hits(text, TASK_TERMS)
    status_hits = term_hits(text, STATUS_TERMS)
    exclusion_hits = term_hits(text, STRONG_EXCLUSION_TERMS) + term_hits(text, SOFT_EXCLUSION_TERMS)
    part_hits = detect_part_number_hits(text)

    has_currency = bool(CURRENCY_PATTERN.search(text))
    has_account_detail = bool(ACCOUNT_PATTERN.search(text))
    has_positive_signal = bool(project_hits or supplier_hits or payment_hits or purchase_hits or part_hits)
    has_contextual_signal = bool(task_hits or status_hits)

    if not has_positive_signal and not (project_chat and has_contextual_signal):
        return None

    if exclusion_hits and not (project_hits or supplier_hits or payment_hits or purchase_hits or part_hits):
        return None

    matched_terms = sorted(
        set(project_hits + supplier_hits + payment_hits + purchase_hits + task_hits + status_hits + part_hits)
    )

    if (payment_hits or has_account_detail or (has_currency and "total" in text)) and (project_chat or supplier_hits or project_hits):
        subcategory = "supplier_payment" if has_account_detail else "financial_update"
        return "payment_detail", subcategory, matched_terms

    if supplier_hits:
        return "supplier_communication", "order_quote_tracking", matched_terms

    if purchase_hits and (project_chat or project_hits or supplier_hits):
        return "product_purchase", "purchase_list", matched_terms

    if part_hits or ("spec" in text and (project_chat or project_hits)):
        return "parts_specification", "part_number_or_spec", matched_terms

    if task_hits and (project_chat or project_hits or supplier_hits):
        return "additional_task", "action_item", matched_terms

    if status_hits and (project_chat or project_hits or supplier_hits):
        return "status_update", "progress_update", matched_terms

    return "project_update", "discussion", matched_terms


def main() -> None:
    parser = argparse.ArgumentParser(description="Build strict project-only WhatsApp extracts.")
    parser.add_argument("--date", dest="date_tag", default=date.today().isoformat(), help="Output date tag YYYY-MM-DD")
    parser.add_argument("--baseline-csv", dest="baseline_csv", default="", help="Optional baseline messages CSV")
    args = parser.parse_args()

    messages = load_csv_rows(MESSAGES_CSV_PATH)
    media_rows = load_csv_rows(MEDIA_CSV_PATH)

    baseline_path = choose_baseline_messages_csv(args.baseline_csv or None)
    baseline_ids: set[str] = set()
    if baseline_path:
        baseline_ids = {clean(row.get("message_id")) for row in load_csv_rows(baseline_path)}

    project_rows: list[dict[str, Any]] = []
    messages_by_id: dict[str, dict[str, Any]] = {}
    messages_by_chat: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in messages:
        message_id = clean(row.get("message_id"))
        if not message_id:
            continue
        messages_by_id[message_id] = row
        messages_by_chat[clean(row.get("chat_id"))].append(row)

        classified = classify_message(row)
        if not classified:
            continue

        category, subcategory, matched_terms = classified
        is_new = message_id not in baseline_ids if baseline_ids else False
        scope = "new_since_rerun" if is_new else "existing"
        text_excerpt = clean_text(row.get("clean_text") or row.get("body"))[:4000]

        project_rows.append(
            {
                "scope": scope,
                "is_new": "true" if is_new else "false",
                "message_id": message_id,
                "timestamp": clean(row.get("timestamp")),
                "source_profile": clean(row.get("source_profile")),
                "chat_name": clean(row.get("chat_name")),
                "author": clean(row.get("author")),
                "category": category,
                "subcategory": subcategory,
                "text": text_excerpt,
                "matched_terms": "|".join(matched_terms[:30]),
            }
        )

    # Deduplicate project rows by message_id while preserving first classification.
    dedup_project_rows: list[dict[str, Any]] = []
    seen_message_ids: set[str] = set()
    for row in project_rows:
        message_id = row["message_id"]
        if message_id in seen_message_ids:
            continue
        seen_message_ids.add(message_id)
        dedup_project_rows.append(row)
    project_rows = dedup_project_rows

    # Build a short context window to identify other-car example media.
    for chat_id, rows in messages_by_chat.items():
        rows.sort(key=lambda row: clean(row.get("timestamp")))
        messages_by_chat[chat_id] = rows

    media_example_rows: list[dict[str, Any]] = []
    for media in media_rows:
        media_type = clean(media.get("media_type"))
        if media_type not in {"photo", "video"}:
            continue
        message_id = clean(media.get("message_id"))
        message = messages_by_id.get(message_id)
        if not message:
            continue

        chat_id = clean(media.get("chat_id"))
        chat_messages = messages_by_chat.get(chat_id, [])
        idx = next((i for i, item in enumerate(chat_messages) if clean(item.get("message_id")) == message_id), -1)
        window = chat_messages[max(0, idx - 4) : idx + 5] if idx >= 0 else [message]
        context_text = " ".join(clean_text(item.get("clean_text") or item.get("body")) for item in window if item)
        context_norm = norm(context_text)
        example_hits = term_hits(context_norm, EXAMPLE_TERMS)
        context_hits = term_hits(context_norm, EXAMPLE_CONTEXT_TERMS)

        reasons = set(example_hits)
        include_example = bool(example_hits)
        if media_type == "video":
            include_example = True
            reasons.add("video_reference_candidate")
        if not include_example and "car" in context_norm and context_hits:
            include_example = True
            reasons.add("car_build_context")
            reasons.update(context_hits)

        if not include_example:
            continue

        media_example_rows.append(
            {
                "media_id": clean(media.get("media_id")),
                "timestamp": clean(media.get("timestamp")),
                "source_profile": clean(media.get("source_profile")),
                "chat_name": clean(media.get("chat_name")),
                "author": clean(media.get("author")),
                "media_type": media_type,
                "file_name": clean(media.get("file_name")),
                "relative_path": clean(media.get("relative_path")),
                "example_reason": "|".join(sorted(reasons)[:20]),
                "context_excerpt": context_text[:800],
            }
        )

    # Deduplicate media rows by media_id.
    dedup_media_rows: list[dict[str, Any]] = []
    seen_media_ids: set[str] = set()
    for row in media_example_rows:
        media_id = row["media_id"]
        if media_id in seen_media_ids:
            continue
        seen_media_ids.add(media_id)
        dedup_media_rows.append(row)
    media_example_rows = dedup_media_rows

    project_rows.sort(key=lambda row: (row["timestamp"], row["source_profile"], row["chat_name"], row["message_id"]))
    media_example_rows.sort(key=lambda row: (row["timestamp"], row["source_profile"], row["chat_name"], row["media_id"]))

    project_out = GENERATED_DIR / f"whatsapp_project_relevant_{args.date_tag}.csv"
    examples_out = GENERATED_DIR / f"whatsapp_examples_media_{args.date_tag}.csv"
    summary_out = GENERATED_DIR / f"whatsapp_project_relevant_{args.date_tag}_summary.json"

    with project_out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "scope",
                "is_new",
                "message_id",
                "timestamp",
                "source_profile",
                "chat_name",
                "author",
                "category",
                "subcategory",
                "text",
                "matched_terms",
            ],
        )
        writer.writeheader()
        for row in project_rows:
            writer.writerow(row)

    with examples_out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "media_id",
                "timestamp",
                "source_profile",
                "chat_name",
                "author",
                "media_type",
                "file_name",
                "relative_path",
                "example_reason",
                "context_excerpt",
            ],
        )
        writer.writeheader()
        for row in media_example_rows:
            writer.writerow(row)

    categories = Counter(row["category"] for row in project_rows)
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_messages_csv": str(MESSAGES_CSV_PATH.relative_to(ROOT)),
        "source_media_csv": str(MEDIA_CSV_PATH.relative_to(ROOT)),
        "baseline_messages_csv": str(baseline_path.relative_to(ROOT)) if baseline_path else "",
        "messages": {
            "project_rows_total": len(project_rows),
            "project_rows_new_since_rerun": sum(1 for row in project_rows if row["is_new"] == "true"),
            "categories": dict(categories),
        },
        "examples_media": {
            "rows_total": len(media_example_rows),
            "photos": sum(1 for row in media_example_rows if row["media_type"] == "photo"),
            "videos": sum(1 for row in media_example_rows if row["media_type"] == "video"),
        },
        "exclusions": {
            "strong_exclusion_terms": sorted(STRONG_EXCLUSION_TERMS),
            "soft_exclusion_terms": sorted(SOFT_EXCLUSION_TERMS),
        },
        "outputs": {
            "project_messages_csv": str(project_out.relative_to(ROOT)),
            "examples_media_csv": str(examples_out.relative_to(ROOT)),
        },
    }
    summary_out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote project messages: {project_out.relative_to(ROOT)}")
    print(f"Wrote example media: {examples_out.relative_to(ROOT)}")
    print(f"Wrote summary: {summary_out.relative_to(ROOT)}")
    print(
        f"Counts: {len(project_rows)} project rows, "
        f"{summary['messages']['project_rows_new_since_rerun']} new, "
        f"{len(media_example_rows)} example media"
    )


if __name__ == "__main__":
    main()
