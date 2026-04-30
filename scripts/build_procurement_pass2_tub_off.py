from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANUAL_DIR = ROOT / "data" / "manual"
DOCS_DIR = ROOT / "docs"

INPUT_MATRIX_PATH = MANUAL_DIR / "procurement_decision_matrix.csv"
WORKBOOK_TIDY_PATH = MANUAL_DIR / "j40_costs_cost_tabs_tidy.csv"

PASS2_MATRIX_PATH = MANUAL_DIR / "procurement_decision_matrix_pass2.csv"
PASS2_BASKETS_PATH = MANUAL_DIR / "procurement_local_baskets_pass2.csv"
PASS2_REPORT_PATH = DOCS_DIR / "procurement-pass2-tub-off.md"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def get_wiring_stock_signal() -> tuple[int, int]:
    rows = load_csv(WORKBOOK_TIDY_PATH)
    wiring_rows = [
        row
        for row in rows
        if row.get("row_disposition") == "line_item"
        and (row.get("received_status") == "yes" or row.get("paid_status") in {"yes", "cod"})
        and (
            row.get("source_sheet", "").strip().lower() == "wiring"
            or "wiring_material" in f"{row.get('item', '')} {row.get('extra_notes', '')}".lower()
            or "migrated from wiring" in f"{row.get('item', '')} {row.get('extra_notes', '')}".lower()
        )
    ]
    connector_rows = [
        row
        for row in wiring_rows
        if re.search(r"connector|relay|fuse|lug|thimble|wire|sleev|grommet|washer", row.get("item", ""), re.I)
    ]
    return len(wiring_rows), len(connector_rows)


def sourcing_mode(item: str, workstream: str) -> str:
    item_lower = item.lower()
    if re.search(r"hot rod|21-circuit|harness|deutsch|relay box|fuse block", item_lower):
        return "import_or_specialty"
    if re.search(r"filter|belt|hose|spark|thermostat|radiator cap|engine mount|clutch|brake flexible", item_lower):
        return "local_toyota_common"
    if re.search(r"washer|bolt|nut|grommet|relay|connector|wire|sleev|fuse", item_lower):
        return "local_electrical_common"
    if workstream in {"mechanical_baseline", "steering_brakes_suspension"}:
        return "local_toyota_common"
    return "mixed_local_or_online"


def pass2_decision(row: dict[str, str], wiring_stock_count: int, wiring_connector_count: int) -> tuple[str, str, str, str]:
    entry_id = row.get("entry_id", "")
    item = row.get("item", "")
    workstream = row.get("workstream", "")
    prior = row.get("decision", "")
    overlap_status = row.get("overlap_status", "")

    if prior in {"defer_duplicate_overlap", "defer_optional"} or overlap_status == "deferred":
        return (
            "defer_as_non_baseline",
            "post_baseline_only",
            "deferred",
            "Entry is already explicitly deferred or duplicate against selected baseline.",
        )

    if prior == "track_ordered_delivery":
        return (
            "track_in_flight_order",
            "in_flight_now",
            "delivery_tracking",
            "Already ordered; do not rebuy.",
        )

    if entry_id == "part_bedliner_sprays":
        return (
            "hold_until_post_weld_primer",
            "post_rust_repair",
            "phase_gate_hold",
            "Bedliner belongs after weld/rust closure and primer, not at tub-lift start.",
        )

    if entry_id in {"part_primer", "part_metal_protection"}:
        return (
            "buy_minimum_qty_now",
            "tub_off_immediate",
            "minimal_buy",
            "Needed for immediate rust-exposed metal stabilization when tub comes off.",
        )

    if workstream == "body_chassis" and prior == "next_phase_gate" and re.search(
        r"epoxy|etching|primer|seam|wax|grease", item, re.I
    ):
        return (
            "post_rust_map_body_stack_bundle",
            "post_rust_repair",
            "stage_bundle_buy",
            "Body chemistry stack should be bought as one bundle after rust map and weld scope are finalized.",
        )

    if entry_id == "quote_hot_rod_wiring":
        return (
            "scope_audit_before_order",
            "pre_order_audit",
            "audit_then_order",
            "Electrical work is already advanced; verify current loom coverage before ordering more.",
        )

    if workstream == "electrical_reset" and prior in {"confirm_price_then_buy", "verify_stock_before_buy", "buy_now"}:
        if wiring_stock_count >= 25 and wiring_connector_count >= 15:
            return (
                "stock_audit_then_local_topup",
                "pre_order_audit",
                "audit_then_topup",
                "Workbook shows substantial wiring stock already received/paid; top up only missing sizes/connectors.",
            )
        return (
            "local_topup_buy",
            "electrical_closeout",
            "topup_buy",
            "Treat as local electrical top-up, not full fresh purchase.",
        )

    if workstream in {"mechanical_baseline", "steering_brakes_suspension"} and prior in {"confirm_price_then_buy", "buy_now"}:
        return (
            "bundle_local_toyota_buy_after_inspection",
            "post_tub_off_inspection",
            "local_bundle_buy",
            "Common Toyota service items should be bought as a local bundle after tub-off inspection confirms exact spec.",
        )

    if prior == "inspect_then_buy":
        return (
            "inspect_then_local_decide",
            "post_tub_off_inspection",
            "inspect_first",
            "Condition-dependent item; inspect first then buy local only if required.",
        )

    if prior == "research_compare_then_select":
        return (
            "defer_until_baseline_closure",
            "post_baseline_only",
            "deferred",
            "Upgrade/option item should wait until baseline reassembly scope is closed.",
        )

    if prior == "buy_now_from_quote":
        return (
            "scope_audit_before_order",
            "pre_order_audit",
            "audit_then_order",
            "Quote is available, but re-check necessity against current progress before spending.",
        )

    return (
        prior or "review",
        "review",
        "review",
        "No pass-2 override rule matched.",
    )


def supplier_hint(mode: str, decision: str) -> str:
    if decision in {"defer_as_non_baseline", "defer_until_baseline_closure"}:
        return "No supplier action now."
    if decision in {"stock_audit_then_local_topup", "local_topup_buy"}:
        return "Use Montgomery Road / local electrical markets for small top-ups after stock count."
    if mode == "local_toyota_common":
        return "Use local Toyota/common parts markets; buy as one batch after inspection."
    if mode == "local_electrical_common":
        return "Use local electrical markets first; avoid duplicate online orders."
    if mode == "import_or_specialty":
        return "Only order import/specialty after scope audit confirms gap."
    return "Prefer local sourcing first, then online if unavailable."


def basket_id_for_row(decision: str, mode: str, workstream: str) -> str:
    if decision == "buy_minimum_qty_now":
        return "basket_tub_off_rust_minimum"
    if decision == "post_rust_map_body_stack_bundle":
        return "basket_body_stack_after_rustmap"
    if decision in {"stock_audit_then_local_topup", "local_topup_buy", "scope_audit_before_order"} and workstream == "electrical_reset":
        return "basket_electrical_stock_audit_topup"
    if decision == "bundle_local_toyota_buy_after_inspection":
        return "basket_mechanical_local_bundle"
    if decision == "inspect_then_local_decide":
        return "basket_condition_based_after_inspection"
    if decision == "track_in_flight_order":
        return "basket_in_flight_tracking"
    if decision in {"defer_as_non_baseline", "defer_until_baseline_closure", "hold_until_post_weld_primer"}:
        return "basket_deferred"
    if mode == "import_or_specialty":
        return "basket_specialty_after_audit"
    return "basket_review"


def build_pass2(rows: list[dict[str, str]], wiring_stock_count: int, wiring_connector_count: int) -> list[dict[str, str]]:
    pass2_rows: list[dict[str, str]] = []
    for row in rows:
        item = row.get("item", "")
        workstream = row.get("workstream", "")
        mode = sourcing_mode(item, workstream)
        decision, timing, budget_mode, rationale = pass2_decision(row, wiring_stock_count, wiring_connector_count)
        basket_id = basket_id_for_row(decision, mode, workstream)

        pass2_rows.append(
            {
                "entry_id": row.get("entry_id", ""),
                "workstream": workstream,
                "item": item,
                "prior_decision": row.get("decision", ""),
                "sourcing_mode": mode,
                "timing_window": timing,
                "pass2_decision": decision,
                "budget_mode": budget_mode,
                "basket_id": basket_id,
                "supplier_hint": supplier_hint(mode, decision),
                "rationale": rationale,
            }
        )
    return pass2_rows


def build_baskets(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["basket_id"]].append(row)

    basket_meta = {
        "basket_tub_off_rust_minimum": ("Tub-Off Rust Minimum", "Immediate bare-metal stabilization only."),
        "basket_body_stack_after_rustmap": ("Body Stack After Rust Map", "Buy epoxy/etch/sealer/wax stack after repair scope is confirmed."),
        "basket_electrical_stock_audit_topup": ("Electrical Stock-Audit Top-Up", "Count existing wiring stock first; buy only shortages."),
        "basket_mechanical_local_bundle": ("Mechanical Local Bundle", "Single local Toyota/common supplier batch after inspection."),
        "basket_condition_based_after_inspection": ("Condition-Based Replacements", "Buy only failed/worn parts after inspection."),
        "basket_specialty_after_audit": ("Specialty/Import After Audit", "Order only if local/on-hand cannot cover."),
        "basket_in_flight_tracking": ("In-Flight Orders", "No rebuy; only track delivery/quality."),
        "basket_deferred": ("Deferred Scope", "Not baseline now."),
        "basket_review": ("Review", "Manual review required."),
    }

    output: list[dict[str, str]] = []
    for basket_id, basket_rows in sorted(grouped.items()):
        title, note = basket_meta.get(basket_id, ("Custom", ""))
        output.append(
            {
                "basket_id": basket_id,
                "basket_title": title,
                "row_count": str(len(basket_rows)),
                "timing_windows": "|".join(sorted({row["timing_window"] for row in basket_rows})),
                "sourcing_modes": "|".join(sorted({row["sourcing_mode"] for row in basket_rows})),
                "entries": "|".join(sorted(row["entry_id"] for row in basket_rows)),
                "notes": note,
            }
        )
    return output


def write_report(pass2_rows: list[dict[str, str]], basket_rows: list[dict[str, str]], wiring_stock_count: int, wiring_connector_count: int) -> None:
    decision_counts = Counter(row["pass2_decision"] for row in pass2_rows)
    timing_counts = Counter(row["timing_window"] for row in pass2_rows)

    immediate_now = [
        row
        for row in pass2_rows
        if row["timing_window"] in {"tub_off_immediate", "in_flight_now"}
        and row["pass2_decision"] in {"buy_minimum_qty_now", "track_in_flight_order"}
    ]

    lines: list[str] = []
    lines.append("# Procurement Pass 2 (Tub-Off, Pakistan Cost Reality)")
    lines.append("")
    lines.append(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("- Input matrix: `data/manual/procurement_decision_matrix.csv`")
    lines.append("- Pass-2 matrix: `data/manual/procurement_decision_matrix_pass2.csv`")
    lines.append("- Basket plan: `data/manual/procurement_local_baskets_pass2.csv`")
    lines.append("")
    lines.append("## Why This Pass")
    lines.append("")
    lines.append("- Objective: shrink the active list before tub-off and avoid overbuying.")
    lines.append(f"- Wiring stock signal from workbook: `{wiring_stock_count}` received/paid wiring rows (`{wiring_connector_count}` connectors/wiring-related).")
    lines.append("- Local Pakistan sourcing assumption: common Toyota service parts and hardware are cheaper and faster locally, so treat them as post-inspection bundles.")
    lines.append("")
    lines.append("## Decision Counts")
    lines.append("")
    for key in sorted(decision_counts):
        lines.append(f"- `{key}`: {decision_counts[key]}")
    lines.append("")
    lines.append("## Timing Windows")
    lines.append("")
    for key in sorted(timing_counts):
        lines.append(f"- `{key}`: {timing_counts[key]}")
    lines.append("")
    lines.append("## Immediate Actions (Now)")
    lines.append("")
    if not immediate_now:
        lines.append("- None")
    else:
        for row in immediate_now:
            lines.append(f"- `{row['entry_id']}` {row['item']} -> {row['pass2_decision']}")
    lines.append("")
    lines.append("## Practical Outcome")
    lines.append("")
    lines.append("- Keep only minimal rust-control buys immediate for tub-off.")
    lines.append("- Treat the full body chemistry stack as a post-rust-map bundle, not separate early purchases.")
    lines.append("- Move most electrical purchases to stock-audit/top-up mode.")
    lines.append("- Move mechanical baseline list into one local Toyota/common supplier bundle after inspection.")
    lines.append("- Keep duplicate/optional/upgrade items deferred to avoid scope creep and unnecessary spend.")

    PASS2_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    input_rows = load_csv(INPUT_MATRIX_PATH)
    wiring_stock_count, wiring_connector_count = get_wiring_stock_signal()

    pass2_rows = build_pass2(input_rows, wiring_stock_count, wiring_connector_count)
    basket_rows = build_baskets(pass2_rows)

    write_csv(
        PASS2_MATRIX_PATH,
        pass2_rows,
        [
            "entry_id",
            "workstream",
            "item",
            "prior_decision",
            "sourcing_mode",
            "timing_window",
            "pass2_decision",
            "budget_mode",
            "basket_id",
            "supplier_hint",
            "rationale",
        ],
    )

    write_csv(
        PASS2_BASKETS_PATH,
        basket_rows,
        [
            "basket_id",
            "basket_title",
            "row_count",
            "timing_windows",
            "sourcing_modes",
            "entries",
            "notes",
        ],
    )

    write_report(pass2_rows, basket_rows, wiring_stock_count, wiring_connector_count)

    print(f"Wrote pass-2 matrix: {PASS2_MATRIX_PATH.relative_to(ROOT)}")
    print(f"Wrote pass-2 baskets: {PASS2_BASKETS_PATH.relative_to(ROOT)}")
    print(f"Wrote pass-2 report: {PASS2_REPORT_PATH.relative_to(ROOT)}")
    print(f"Rows evaluated: {len(pass2_rows)}")


if __name__ == "__main__":
    main()
