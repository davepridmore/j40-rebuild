from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANUAL_DIR = ROOT / "data" / "manual"
DOCS_DIR = ROOT / "docs"

EXPENSES_PATH = MANUAL_DIR / "expenses.csv"
OVERLAP_REVIEW_PATH = MANUAL_DIR / "parts_overlap_candidates.csv"

OUTPUT_RESOLUTION_PATH = MANUAL_DIR / "parts_overlap_resolution.csv"
OUTPUT_BUY_NOW_PATH = MANUAL_DIR / "parts_buy_now_this_week.csv"
OUTPUT_REPORT_PATH = DOCS_DIR / "parts-buy-now-this-week.md"


@dataclass(frozen=True)
class OverlapDecision:
    group_id: str
    chosen_entries: tuple[str, ...]
    deferred_entries: tuple[str, ...]
    rationale: str


OVERLAP_DECISIONS: tuple[OverlapDecision, ...] = (
    OverlapDecision(
        group_id="wiring_kit_options",
        chosen_entries=("quote_hot_rod_wiring",),
        deferred_entries=("quote_wiring_harness", "quote_universal_21_circuit_kit", "part_wiring_kit"),
        rationale="Hot-rod path is already installed per user update; keep alternatives deferred unless rewiring scope reopens.",
    ),
    OverlapDecision(
        group_id="grommet_options",
        chosen_entries=(
            "part_rubber_grommet_set",
            "part_firewall_grommet_set_small_medium",
            "part_firewall_grommet_set_large_power",
        ),
        deferred_entries=("quote_rubber_grommet_set_chat",),
        rationale="Base grommet set is received; keep supplemental firewall sizes and suppress duplicate quote-only alternatives.",
    ),
    OverlapDecision(
        group_id="wire_sleeving_options",
        chosen_entries=("quote_pet_braided_sleeving", "part_cable_sleeve_protection"),
        deferred_entries=(
            "part_split_conduit_braided_sleeve_small",
            "part_split_conduit_braided_sleeve_medium",
            "part_split_conduit_braided_sleeve_large",
        ),
        rationale="Use braided sleeving as the primary finish path; keep already-received sleeves as stock.",
    ),
    OverlapDecision(
        group_id="switch_options",
        chosen_entries=("part_horn_relay", "part_h4_ceramic_headlight_connector_high"),
        deferred_entries=("part_spotlight_switch", "part_toggle_switch", "part_winch_switch"),
        rationale="Prioritize baseline safety/lighting electricals; defer optional accessory controls.",
    ),
    OverlapDecision(
        group_id="floor_finish_stack",
        chosen_entries=("part_bedliner_sprays",),
        deferred_entries=("part_bed_lining", "part_sound_dampening_sheets", "part_foam", "part_carpet"),
        rationale="Buy only rust-protection floor coating now; defer comfort layers until body closure is complete.",
    ),
    OverlapDecision(
        group_id="shock_options",
        chosen_entries=("part_old_man_emu_shocks",),
        deferred_entries=("part_bilstein_shocks",),
        rationale="OME path is active for the current tub-off rebuild and Bilstein stays as deferred alternative.",
    ),
    OverlapDecision(
        group_id="primer_system_stack",
        chosen_entries=("part_primer", "part_self_etching_primer", "part_epoxy_primer", "part_seam_sealer", "part_wax_and_grease_remover"),
        deferred_entries=(),
        rationale="Treat primer stack as complementary stages, not mutually exclusive alternatives.",
    ),
)


WORKSTREAM_PRIORITY = {
    "body_chassis": "P0",
    "electrical_reset": "P0",
    "mechanical_baseline": "P1",
    "steering_brakes_suspension": "P1",
    "interior_weatherproofing": "P2",
    "optional_upgrades": "P3",
}


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_resolution_rows(expenses_parts: list[dict[str, str]]) -> list[dict[str, str]]:
    by_entry = {row["entry_id"]: row for row in expenses_parts}
    rows: list[dict[str, str]] = []
    for decision in OVERLAP_DECISIONS:
        chosen_existing = [entry for entry in decision.chosen_entries if entry in by_entry]
        deferred_existing = [entry for entry in decision.deferred_entries if entry in by_entry]
        rows.append(
            {
                "overlap_group_id": decision.group_id,
                "chosen_entries": "|".join(chosen_existing),
                "deferred_entries": "|".join(deferred_existing),
                "chosen_items": "|".join(by_entry[entry]["item"] for entry in chosen_existing),
                "deferred_items": "|".join(by_entry[entry]["item"] for entry in deferred_existing),
                "rationale": decision.rationale,
            }
        )
    return rows


def classify_action(row: dict[str, str]) -> str:
    procurement_stage = (row.get("procurement_stage") or "").strip().lower()
    status = (row.get("status") or "").strip().lower()
    amount_confirmed = (row.get("amount_status") or "").strip().lower() == "confirmed"

    if procurement_stage == "ordered_pending_delivery" or status == "ordered":
        return "track_delivery"

    if procurement_stage == "purchase_ready":
        if status == "quote":
            return "order_from_selected_quote" if amount_confirmed else "confirm_quote_then_order"
        return "order_now" if amount_confirmed else "confirm_price_then_order"

    return "not_this_week"


def build_buy_now_rows(expenses_parts: list[dict[str, str]]) -> list[dict[str, str]]:
    deferred_entries = {entry for decision in OVERLAP_DECISIONS for entry in decision.deferred_entries}
    chosen_entries = {entry for decision in OVERLAP_DECISIONS for entry in decision.chosen_entries}

    rows: list[dict[str, str]] = []
    for row in expenses_parts:
        entry_id = row["entry_id"]
        if entry_id in deferred_entries:
            continue

        action = classify_action(row)
        if action == "not_this_week":
            continue

        overlap_resolution = "selected_in_overlap_group" if entry_id in chosen_entries else "non_overlap_or_unique"
        priority = WORKSTREAM_PRIORITY.get((row.get("workstream") or "").strip(), "P2")

        rows.append(
            {
                "priority": priority,
                "entry_id": entry_id,
                "workstream": row.get("workstream", ""),
                "item": row.get("item", ""),
                "status": row.get("status", ""),
                "procurement_stage": row.get("procurement_stage", ""),
                "order_date": row.get("date", ""),
                "amount": row.get("amount", ""),
                "currency": row.get("currency", ""),
                "amount_status": row.get("amount_status", ""),
                "transaction_number": row.get("transaction_number", ""),
                "expected_delivery_date": row.get("expected_delivery_date", ""),
                "payment_status": row.get("payment_status", ""),
                "delivery_status": row.get("delivery_status", ""),
                "next_action": action,
                "overlap_resolution": overlap_resolution,
                "company": row.get("company", ""),
                "evidence_ref": row.get("evidence_ref", ""),
            }
        )

    rows.sort(key=lambda value: (value["priority"], value["workstream"], value["entry_id"]))
    return rows


def write_markdown(resolution_rows: list[dict[str, str]], buy_now_rows: list[dict[str, str]]) -> None:
    action_counts = Counter(row["next_action"] for row in buy_now_rows)
    priority_counts = Counter(row["priority"] for row in buy_now_rows)

    lines: list[str] = []
    lines.append("# Parts Buy-Now Plan (This Week)")
    lines.append("")
    lines.append(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("- Source ledger: `data/manual/expenses.csv` (`bucket=parts`)")
    lines.append("- Overlap resolution table: `data/manual/parts_overlap_resolution.csv`")
    lines.append("- This-week list: `data/manual/parts_buy_now_this_week.csv`")
    lines.append("")
    lines.append("## This-Week Counts")
    lines.append("")
    lines.append(f"- Rows in this-week list: {len(buy_now_rows)}")
    for key in sorted(action_counts):
        lines.append(f"- `{key}`: {action_counts[key]}")
    lines.append("")
    lines.append("## Priority Split")
    lines.append("")
    for key in sorted(priority_counts):
        lines.append(f"- `{key}`: {priority_counts[key]}")
    lines.append("")
    lines.append("## Overlap Decisions Applied")
    lines.append("")
    for row in resolution_rows:
        lines.append(f"- `{row['overlap_group_id']}`: keep `{row['chosen_entries'] or '-'}`; defer `{row['deferred_entries'] or '-'}`")
    lines.append("")
    lines.append("## Immediate Actions")
    lines.append("")
    for action in ("order_from_selected_quote", "order_now", "confirm_price_then_order", "confirm_quote_then_order", "track_delivery"):
        subset = [row for row in buy_now_rows if row["next_action"] == action]
        if not subset:
            continue
        lines.append(f"- `{action}` ({len(subset)}):")
        for row in subset:
            if row["amount"]:
                amount_text = f"{row['amount']} {row['currency']}".strip()
            else:
                amount_text = "price_tbd"
            order_date = row["order_date"] or "order_date_tbd"
            expected_delivery = row["expected_delivery_date"] or "delivery_date_tbd"
            delivery_status = row["delivery_status"] or "delivery_status_tbd"
            payment_status = row["payment_status"] or "payment_status_tbd"
            lines.append(
                f"  - `{row['entry_id']}` [{row['priority']}] {row['item']} "
                f"(price: {amount_text}; order_date: {order_date}; "
                f"delivery_eta: {expected_delivery}; delivery_status: {delivery_status}; payment_status: {payment_status})"
            )

    OUTPUT_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    expenses_rows = load_csv(EXPENSES_PATH)
    expenses_parts = [row for row in expenses_rows if (row.get("bucket", "").strip().lower() == "parts")]

    # Ensure overlap review exists (not strictly required for logic, but keeps flow explicit).
    if not OVERLAP_REVIEW_PATH.exists():
        raise SystemExit("Missing parts overlap review. Run scripts/review_parts_list.py first.")

    resolution_rows = build_resolution_rows(expenses_parts)
    buy_now_rows = build_buy_now_rows(expenses_parts)

    write_csv(
        OUTPUT_RESOLUTION_PATH,
        resolution_rows,
        [
            "overlap_group_id",
            "chosen_entries",
            "deferred_entries",
            "chosen_items",
            "deferred_items",
            "rationale",
        ],
    )

    write_csv(
        OUTPUT_BUY_NOW_PATH,
        buy_now_rows,
        [
            "priority",
            "entry_id",
            "workstream",
            "item",
            "status",
            "procurement_stage",
            "order_date",
            "amount",
            "currency",
            "amount_status",
            "transaction_number",
            "expected_delivery_date",
            "payment_status",
            "delivery_status",
            "next_action",
            "overlap_resolution",
            "company",
            "evidence_ref",
        ],
    )

    write_markdown(resolution_rows, buy_now_rows)

    print(f"Wrote overlap resolution: {OUTPUT_RESOLUTION_PATH.relative_to(ROOT)}")
    print(f"Wrote buy-now list: {OUTPUT_BUY_NOW_PATH.relative_to(ROOT)}")
    print(f"Wrote report: {OUTPUT_REPORT_PATH.relative_to(ROOT)}")
    print(f"This-week rows: {len(buy_now_rows)}")


if __name__ == "__main__":
    main()
