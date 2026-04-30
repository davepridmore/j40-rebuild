from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANUAL_DIR = ROOT / "data" / "manual"

EXPENSES_PATH = MANUAL_DIR / "expenses.csv"
OUTPUT_PATH = MANUAL_DIR / "orders_receipts_audit_queue.csv"

GOODS_BUCKETS = {"parts", "tools"}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def load_goods_rows() -> list[dict[str, str]]:
    with EXPENSES_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [
        row
        for row in rows
        if (row.get("bucket", "").strip().lower() in GOODS_BUCKETS)
        and (row.get("status", "").strip().lower() != "cancelled")
        and (row.get("delivery_status", "").strip().lower() != "not_required")
        and not (row.get("procurement_stage", "").strip().lower().startswith("not_required"))
    ]


def quoted_terms(*values: str) -> str:
    terms = [value.strip() for value in values if value and value.strip()]
    return " ".join(f"\"{term}\"" for term in terms)


def build_queries(row: dict[str, str]) -> tuple[str, str]:
    base_terms = quoted_terms(row.get("transaction_number", ""), row.get("company", ""), row.get("item", ""))
    if not base_terms:
        return "", ""
    order_query = f"{base_terms} (order OR confirmation OR shipped OR dispatch OR tracking)"
    receipt_query = f"{base_terms} (receipt OR invoice OR paid OR payment)"
    return order_query, receipt_query


def classify_audit(row: dict[str, str]) -> tuple[str, str]:
    stage = (row.get("procurement_stage") or "").strip().lower()
    status = (row.get("status") or "").strip().lower()
    payment = (row.get("payment_status") or "").strip().lower()
    delivery = (row.get("delivery_status") or "").strip().lower()
    evidence = (row.get("evidence_ref") or "").strip()

    if stage in {"needs_confirmation", "received_candidate"} or delivery == "needs_confirmation":
        return "confirm_order_or_receipt", "high"
    if stage == "ordered_pending_delivery" or delivery == "pending_delivery":
        return "track_order_delivery", "high"
    if stage == "purchase_ready":
        return "find_order_or_quote_proof", "high"
    if payment == "paid" and delivery in {"received", "installed", "completed"}:
        return ("verify_receipt_reference", "medium") if evidence else ("attach_receipt_proof", "high")
    if status in {"quote", "planned"}:
        return "quote_or_plan_only", "medium"
    return "review_context", "low"


def build_output_rows(goods_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in goods_rows:
        audit_status, audit_priority = classify_audit(row)
        order_query, receipt_query = build_queries(row)
        rows.append(
            {
                "entry_id": row.get("entry_id", ""),
                "phase": row.get("phase", ""),
                "workstream": row.get("workstream", ""),
                "bucket": row.get("bucket", ""),
                "item": row.get("item", ""),
                "company": row.get("company", ""),
                "transaction_number": row.get("transaction_number", ""),
                "order_date": row.get("date", ""),
                "expected_delivery_date": row.get("expected_delivery_date", ""),
                "status": row.get("status", ""),
                "procurement_stage": row.get("procurement_stage", ""),
                "payment_status": row.get("payment_status", ""),
                "delivery_status": row.get("delivery_status", ""),
                "amount": row.get("amount", ""),
                "currency": row.get("currency", ""),
                "evidence_ref": row.get("evidence_ref", ""),
                "audit_status": audit_status,
                "audit_priority": audit_priority,
                "order_search_query": order_query,
                "receipt_search_query": receipt_query,
            }
        )
    rows.sort(
        key=lambda value: (
            PRIORITY_ORDER.get(value["audit_priority"], 99),
            value["workstream"],
            value["entry_id"],
        )
    )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "entry_id",
        "phase",
        "workstream",
        "bucket",
        "item",
        "company",
        "transaction_number",
        "order_date",
        "expected_delivery_date",
        "status",
        "procurement_stage",
        "payment_status",
        "delivery_status",
        "amount",
        "currency",
        "evidence_ref",
        "audit_status",
        "audit_priority",
        "order_search_query",
        "receipt_search_query",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    goods_rows = load_goods_rows()
    output_rows = build_output_rows(goods_rows)
    write_csv(OUTPUT_PATH, output_rows)

    priority_counts = Counter(row["audit_priority"] for row in output_rows)
    print(f"Wrote audit queue: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Rows: {len(output_rows)}")
    for key in ("high", "medium", "low"):
        print(f"{key}: {priority_counts.get(key, 0)}")


if __name__ == "__main__":
    main()
