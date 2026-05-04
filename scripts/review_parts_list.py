from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANUAL_DIR = ROOT / "data" / "manual"
DOCS_DIR = ROOT / "docs"

EXPENSES_PATH = MANUAL_DIR / "expenses.csv"
REVIEW_CSV_PATH = MANUAL_DIR / "parts_list_review.csv"
OVERLAP_CSV_PATH = MANUAL_DIR / "parts_overlap_candidates.csv"
REVIEW_MD_PATH = DOCS_DIR / "parts-list-review.md"


@dataclass(frozen=True)
class OverlapRule:
    group_id: str
    label: str
    pattern: re.Pattern[str]


OVERLAP_RULES: tuple[OverlapRule, ...] = (
    OverlapRule("wiring_kit_options", "Wiring kit options", re.compile(r"wiring harness|wiring kit|21-circuit|hot rod wiring", re.I)),
    OverlapRule("grommet_options", "Grommet options", re.compile(r"grommet", re.I)),
    OverlapRule(
        "wire_sleeving_options",
        "Wire sleeving options",
        re.compile(r"wire slee|loom slee|braided slee|split conduit|conduit|pet expandable braided|sleeve inventory", re.I),
    ),
    OverlapRule("primer_system_stack", "Primer system stack", re.compile(r"\bprimer\b|etching|epoxy|seam sealer|wax and grease", re.I)),
    OverlapRule("floor_finish_stack", "Floor/interior finish stack", re.compile(r"bedliner|bed lining|sound dampening|\bfoam\b|carpet", re.I)),
    OverlapRule("shock_options", "Shock options", re.compile(r"shock|nitrocharger|bilstein", re.I)),
    OverlapRule("switch_options", "Switch inventory", re.compile(r"switch|relay|headlight connector", re.I)),
)


def load_parts_rows() -> list[dict[str, str]]:
    with EXPENSES_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [row for row in rows if (row.get("bucket", "").strip().lower() == "parts")]


def action_bucket(row: dict[str, str]) -> str:
    procurement_stage = (row.get("procurement_stage") or "").strip().lower()
    status = (row.get("status") or "").strip().lower()
    delivery_status = (row.get("delivery_status") or "").strip().lower()

    if status == "cancelled" or delivery_status == "not_required" or procurement_stage.startswith("not_required"):
        return "cancelled_or_not_required"
    if status in {"installed", "received", "credited"} or procurement_stage in {"completed", "received"}:
        return "completed_or_received"
    if procurement_stage == "ordered_pending_delivery" or status == "ordered":
        return "ordered_waiting_arrival"
    if procurement_stage.startswith("purchase_ready"):
        if status == "quote":
            return "quote_decision_ready"
        return "buy_now"
    if procurement_stage == "researching":
        return "researching"
    if procurement_stage == "spec_ready_release_hold":
        return "spec_ready_release_hold"
    if procurement_stage == "spec_needed_before_order":
        return "needs_spec_before_order"
    if procurement_stage == "next_phase_purchase":
        return "next_phase"
    if procurement_stage.startswith("deferred") or procurement_stage in {"deferred_until_body_closed", "deferred_optional"}:
        return "deferred"
    if procurement_stage in {"needs_confirmation", "received_candidate"}:
        return "needs_confirmation"
    return "unclear"


def classify_overlap_group(item: str) -> tuple[str, str]:
    for rule in OVERLAP_RULES:
        if rule.pattern.search(item):
            return rule.group_id, rule.label
    return "", ""


def build_review_rows(parts_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    review_rows: list[dict[str, str]] = []
    for row in parts_rows:
        overlap_group_id, overlap_group_label = classify_overlap_group(row.get("item", ""))
        review_rows.append(
            {
                "entry_id": row.get("entry_id", ""),
                "phase": row.get("phase", ""),
                "workstream": row.get("workstream", ""),
                "item": row.get("item", ""),
                "status": row.get("status", ""),
                "procurement_stage": row.get("procurement_stage", ""),
                "action_bucket": action_bucket(row),
                "amount": row.get("amount", ""),
                "amount_status": row.get("amount_status", ""),
                "has_confirmed_amount": "yes" if (row.get("amount_status", "").strip().lower() == "confirmed") else "no",
                "vendor": row.get("vendor", ""),
                "evidence_ref": row.get("evidence_ref", ""),
                "overlap_group_id": overlap_group_id,
                "overlap_group_label": overlap_group_label,
            }
        )
    return review_rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_overlap_rows(review_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    labels: dict[str, str] = {}
    for row in review_rows:
        group_id = row["overlap_group_id"]
        if not group_id:
            continue
        if row["action_bucket"] in {"completed_or_received", "cancelled_or_not_required"}:
            continue
        grouped[group_id].append(row)
        labels[group_id] = row["overlap_group_label"]

    overlap_rows: list[dict[str, str]] = []
    for group_id, rows in sorted(grouped.items()):
        if len(rows) < 2:
            continue
        overlap_rows.append(
            {
                "overlap_group_id": group_id,
                "overlap_group_label": labels[group_id],
                "item_count": str(len(rows)),
                "entries": "|".join(sorted(row["entry_id"] for row in rows)),
                "items": "|".join(sorted(row["item"] for row in rows)),
                "action_buckets": "|".join(sorted({row["action_bucket"] for row in rows})),
            }
        )
    return overlap_rows


def write_markdown(review_rows: list[dict[str, str]], overlap_rows: list[dict[str, str]]) -> None:
    bucket_counts = Counter(row["action_bucket"] for row in review_rows)
    workstream_counts = Counter(row["workstream"] for row in review_rows)
    amount_counts = Counter(row["has_confirmed_amount"] for row in review_rows)

    buy_now_missing_price = [
        row for row in review_rows if row["action_bucket"] in {"buy_now", "quote_decision_ready"} and row["has_confirmed_amount"] == "no"
    ]
    buy_now_with_price = [
        row for row in review_rows if row["action_bucket"] in {"buy_now", "quote_decision_ready"} and row["has_confirmed_amount"] == "yes"
    ]

    lines: list[str] = []
    lines.append("# Parts List Review")
    lines.append("")
    lines.append(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Source: `data/manual/expenses.csv` (`bucket=parts`) -> {len(review_rows)} rows")
    lines.append("- Review CSV: `data/manual/parts_list_review.csv`")
    lines.append("- Overlap CSV: `data/manual/parts_overlap_candidates.csv`")
    lines.append("")
    lines.append("## Action Buckets")
    lines.append("")
    for key in sorted(bucket_counts):
        lines.append(f"- `{key}`: {bucket_counts[key]}")
    lines.append("")
    lines.append("## Workstream Split")
    lines.append("")
    for key, value in workstream_counts.most_common():
        lines.append(f"- `{key}`: {value}")
    lines.append("")
    lines.append("## Price Coverage")
    lines.append("")
    lines.append(f"- `has_confirmed_amount=yes`: {amount_counts.get('yes', 0)}")
    lines.append(f"- `has_confirmed_amount=no`: {amount_counts.get('no', 0)}")
    lines.append("")
    lines.append("## Buy-Now / Quote-Ready Missing Price")
    lines.append("")
    if not buy_now_missing_price:
        lines.append("- None")
    else:
        for row in sorted(buy_now_missing_price, key=lambda value: (value["workstream"], value["entry_id"])):
            lines.append(f"- `{row['entry_id']}` [{row['workstream']}] {row['item']}")
    lines.append("")
    lines.append("## Buy-Now / Quote-Ready With Confirmed Price")
    lines.append("")
    if not buy_now_with_price:
        lines.append("- None")
    else:
        for row in sorted(buy_now_with_price, key=lambda value: (value["workstream"], value["entry_id"])):
            lines.append(f"- `{row['entry_id']}` [{row['workstream']}] {row['item']} ({row['amount']})")
    lines.append("")
    lines.append("## Overlap Groups")
    lines.append("")
    if not overlap_rows:
        lines.append("- No overlap groups detected.")
    else:
        for row in overlap_rows:
            lines.append(
                f"- `{row['overlap_group_id']}` ({row['item_count']} rows): {row['overlap_group_label']} "
                f"[action buckets: {row['action_buckets']}]"
            )

    REVIEW_MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parts_rows = load_parts_rows()
    review_rows = build_review_rows(parts_rows)

    write_csv(
        REVIEW_CSV_PATH,
        review_rows,
        [
            "entry_id",
            "phase",
            "workstream",
            "item",
            "status",
            "procurement_stage",
            "action_bucket",
            "amount",
            "amount_status",
            "has_confirmed_amount",
            "vendor",
            "evidence_ref",
            "overlap_group_id",
            "overlap_group_label",
        ],
    )

    overlap_rows = build_overlap_rows(review_rows)
    write_csv(
        OVERLAP_CSV_PATH,
        overlap_rows,
        [
            "overlap_group_id",
            "overlap_group_label",
            "item_count",
            "entries",
            "items",
            "action_buckets",
        ],
    )

    write_markdown(review_rows, overlap_rows)

    print(f"Wrote review: {REVIEW_CSV_PATH.relative_to(ROOT)}")
    print(f"Wrote overlaps: {OVERLAP_CSV_PATH.relative_to(ROOT)}")
    print(f"Wrote report: {REVIEW_MD_PATH.relative_to(ROOT)}")
    print(f"Rows reviewed: {len(review_rows)}")


if __name__ == "__main__":
    main()
