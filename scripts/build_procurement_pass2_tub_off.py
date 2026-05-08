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
    if re.search(r"masking|solvent-safe|lint-free|wipes?|tape", item_lower) or re.search(
        r"(thread|hole|tapered|rubber|silicone|plastic).{0,20}plugs?|plugs?.{0,20}(thread|hole|tapered|rubber|silicone|plastic)",
        item_lower,
    ):
        return "local_hardware_common"
    if workstream == "brake_system":
        if re.search(r"fluid|cleaner|cap|plug|consumable", item_lower):
            return "local_hardware_common"
        return "local_toyota_common"
    if re.search(r"wood|timber|cribbing|chock|support block", item_lower):
        return "local_hardware_common"
    if re.search(r"hot rod|21-circuit|harness|deutsch|relay box|fuse block", item_lower):
        return "import_or_specialty"
    if re.search(r"filter|belt|hose|spark|glow|heat plug|thermostat|radiator cap|engine mount|clutch|brake flexible", item_lower):
        return "local_toyota_common"
    if workstream in {"body_chassis", "interior_weatherproofing"} and re.search(
        (
            r"fastener|bolt|screw|washer|clip nut|speed nut|captive|rivnut|weld nut|"
            r"retaining clip|cotter|hairpin|circlip|r-clip|rubber|bumper|isolator|"
            r"spacer|sleeve|shoulder|pivot|bracket|retainer|plate"
        ),
        item_lower,
    ):
        return "local_fastener_hardware"
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
    status = row.get("status", "").strip().lower()
    procurement_stage = row.get("procurement_stage", "").strip().lower()

    if status == "cancelled" or procurement_stage.startswith("not_required") or prior.startswith("not_required"):
        return (
            prior or "not_required",
            "not_required",
            "not_required",
            "Entry is cancelled or not required in the active baseline.",
        )

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

    if entry_id == "part_mech_engine_mount_set" or prior == "defer_until_mount_failure_or_engine_lift_scope":
        return (
            "defer_until_mount_failure_or_engine_lift_scope",
            "no_engine_lift_baseline",
            "deferred_conditional",
            (
                "No engine-lift baseline: inspect mounts in place; defer purchase unless failed or "
                "engine is already being supported/lifted for another approved job. EPS column conversion does not require engine removal."
            ),
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

    if workstream == "body_chassis" and prior in {"confirm_price_then_buy", "buy_now"} and re.search(
        r"fastener|bolt|screw|clip nut|speed nut|captive|rivnut|weld nut|retaining clip|cotter|hairpin|circlip|r-clip",
        item,
        re.I,
    ):
        return (
            "buy_body_fastener_hardware_from_samples",
            "body_fastener_topup",
            "local_fastener_buy",
            "Buy exact plated body fastener/captive hardware from old samples; do not duplicate Millat-covered metric stock.",
        )

    if workstream == "body_chassis" and prior == "review" and re.search(
        r"rubber|bumper|isolator|spacer|sleeve|shoulder|pivot|bracket|retainer|plate",
        item,
        re.I,
    ):
        return (
            "capture_body_hardware_samples_then_order",
            "body_hardware_sample_sort",
            "local_body_hardware_release_hold",
            "Sort and measure old samples, then buy or fabricate only the body hardware not covered by Millat stock.",
        )

    if prior == "capture_body_hardware_samples_then_order":
        return (
            "capture_body_hardware_samples_then_order",
            "body_hardware_sample_sort",
            "local_body_hardware_release_hold",
            "Sort and measure old samples, then buy or fabricate only the body hardware not covered by Millat stock.",
        )

    if entry_id == "quote_hot_rod_wiring":
        return (
            "scope_audit_before_order",
            "pre_order_audit",
            "audit_then_order",
            "Electrical work is already advanced; verify current loom coverage before ordering more.",
        )

    if entry_id == "part_cabin_compact_fuse_boxes":
        return (
            "buy_compact_cabin_fuse_boxes",
            "electrical_closeout",
            "baseline_electrical_buy",
            "Cabin fuse protection is not ordered stock; provide 3 isolated under-dash input groups with 6 fuses each: constant battery, IGN/RUN, and ACC/part-way. A single OEM box is acceptable if the buses are isolated and mapped.",
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

    if entry_id == "part_suspension_wooden_cribbing_blocks":
        return (
            "buy_before_suspension_work",
            "pre_suspension_setup",
            "safety_support_buy",
            "Needed before the Ironman suspension swap so the chassis and axle can be supported safely with rated stands plus cribbing.",
        )

    if entry_id == "part_mech_heat_glow_plugs_set":
        return (
            "source_toyota_oe_glow_plugs_by_part_number",
            "post_tub_off_inspection",
            "local_toyota_oe_buy",
            "Buy exact Toyota-labelled plugs: 19850-68030 x6 for HJ47-style 2H 12V/8.5V, or 19850-68060 x6 only if old plug/system confirms 24V/superglow.",
        )

    if entry_id == "part_brake_fluid_bleed_consumables" or prior in {
        "buy_dot3_fluid_and_bleed_consumables",
        "buy_remaining_brake_bleed_consumables",
    }:
        return (
            "buy_remaining_brake_bleed_consumables",
            "pre_brake_hydraulic_opening",
            "safety_consumables_buy",
            "DOT 3 brake fluid is already ordered separately; hydraulics must not be opened until that sealed fluid and the remaining caps/plugs, cleaner, and bleed tools are available.",
        )

    if entry_id == "part_chassis_masking_plugs_tape_solvent_wipes":
        return (
            "buy_chassis_masking_consumables",
            "pre_chassis_coating",
            "small_consumables_buy",
            "Needed before solvent wipe, primer, seam sealer, and Raptor so threads, drains, grounds, body-mount faces, and line/fitting interfaces stay serviceable.",
        )

    if entry_id in {
        "part_mech_fuel_hose_and_clamps",
        "part_mech_heater_hose_set",
        "part_mech_radiator_hose_set",
        "part_mech_vacuum_hose_refresh",
    }:
        return (
            "hose_local_market_order_ready",
            "hose_local_market_order",
            "local_hose_order_ready",
            "Exact local-market order lengths are released in the hose order sheet; buy by material, ID/OD, rating, and stated length, then close final trim, clamp, chafe, and leak checks during installation.",
        )

    if entry_id == "part_mech_clutch_master_slave_refresh":
        return (
            "clutch_hydraulic_inspect_then_exact_order",
            "clutch_hydraulic_inspection",
            "hydraulic_exact_order_hold",
            "Inspect for leakage, pedal sink, seized seals, and line corrosion first; exact order is master refresh/replacement, slave refresh/replacement, clutch flex hose by end fittings if failed, and a 1500 mm 4.75 mm brake/clutch hard-line allowance only if the hard line is replaced.",
        )

    if entry_id == "part_mech_brake_flex_hose_set":
        return (
            "capture_brake_specs_then_order",
            "merged_suspension_brake_window",
            "brake_baseline_release_hold",
            "Complete crimped brake hose assemblies can be sourced online/local, but exact release waits for fitted end fittings, old samples, bracket retention, free length, and Ironman full-droop slack.",
        )

    if workstream == "brake_system" and prior == "capture_spec_then_buy":
        return (
            "capture_brake_specs_then_order",
            "merged_suspension_brake_window",
            "brake_baseline_release_hold",
            "Brake item is approved baseline scope, but exact purchase waits for fitted hardware, old samples, and full-droop clearance capture.",
        )

    if workstream == "brake_system" and prior == "inspect_confirm_then_buy_standard":
        return (
            "open_inspect_then_order_standard_brake_parts",
            "merged_suspension_brake_window",
            "brake_baseline_release_hold",
            "Standard brake service item is approved, but exact parts wait for drum/rotor/caliper inspection and measurements.",
        )

    if workstream in {"mechanical_baseline", "steering_brakes_suspension"} and prior in {"confirm_price_then_buy", "buy_now"}:
        return (
            "bundle_local_toyota_buy_after_inspection",
            "post_tub_off_inspection",
            "local_bundle_buy",
            "Common Toyota service items should be bought as a local bundle after tub-off inspection confirms exact spec.",
        )

    if prior == "hold_until_body_closed":
        return (
            "hold_until_body_closed",
            "body_sealed",
            "deferred",
            "Wait until panel/trim alignment and body sealing before buying exact finish hardware.",
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
    if decision in {
        "defer_as_non_baseline",
        "defer_until_baseline_closure",
        "defer_until_mount_failure_or_engine_lift_scope",
    }:
        return "No supplier action now."
    if decision == "track_in_flight_order":
        return "Already ordered; track delivery, receipt condition, and quantity/spec match before use."
    if decision == "capture_body_hardware_samples_then_order":
        return "Use Bilal Ganj/body hardware, rubber trim, fastener, or machine-shop suppliers after old samples are sorted and measured."
    if decision == "buy_body_fastener_hardware_from_samples":
        return "Use local fastener/body hardware suppliers; match old samples and buy plated or stainless replacements."
    if decision == "buy_compact_cabin_fuse_boxes":
        return "Use local electrical markets; require compact covered ATO/ATC blade-fuse boxes with secure lids."
    if decision in {"buy_bleed_consumables_before_opening_hydraulics", "buy_remaining_brake_bleed_consumables"}:
        return "Use a local brake supplier, Daraz/Autohub, or the workshop for caps/plugs, brake cleaner, bleed hose/bottle or bleeder kit, rags, gloves, and catch tray; do not rebuy DOT 3 fluid unless the Autohub order fails."
    if decision == "buy_chassis_masking_consumables":
        return "Use a local paint/bodywork supplier, hardware shop, or Daraz for automotive masking tape, assorted tapered plugs/caps, and solvent-safe lint-free wipes."
    if decision in {"hose_rubber_release_hold", "hose_local_market_order_ready"}:
        return "Use the hose local market order sheet with local hose, radiator, diesel, rubber, and hydraulic shops; order by material, ID/OD, rating, and listed buy length."
    if decision == "clutch_hydraulic_inspect_then_exact_order":
        return "Use a Toyota/clutch hydraulic supplier after inspection; match master/slave bore, port thread, flare/seat, pushrod style, and flex-hose end fittings before payment."
    if decision in {
        "capture_brake_specs_then_order",
        "open_inspect_then_order_standard_brake_parts",
    }:
        return "Use a brake/Toyota parts shop or the workshop's brake supplier after physical sample and fitting confirmation."
    if decision in {"stock_audit_then_local_topup", "local_topup_buy"}:
        return "Use Montgomery Road / local electrical markets for small top-ups after stock count."
    if decision == "source_toyota_oe_glow_plugs_by_part_number":
        return "Ask HYA/Hamza Younas Autos or Bilal Ganj Toyota diesel suppliers for Toyota 19850-68030 x6; use Toyota 19850-68060 x6 only after 24V/superglow confirmation."
    if mode == "local_toyota_common":
        return "Use local Toyota/common parts markets; buy as one batch after inspection."
    if mode == "local_hardware_common":
        return "Use local timber or hardware supplier; confirm sound hardwood/timber dimensions before purchase."
    if mode == "local_fastener_hardware":
        return "Use local fastener/body hardware suppliers; match M6/M8 samples, head style, length, and plated or stainless finish."
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
    if decision == "buy_compact_cabin_fuse_boxes":
        return "basket_compact_cabin_fuse_boxes"
    if decision == "bundle_local_toyota_buy_after_inspection":
        return "basket_mechanical_local_bundle"
    if decision == "inspect_then_local_decide":
        return "basket_condition_based_after_inspection"
    if decision == "defer_until_mount_failure_or_engine_lift_scope":
        return "basket_engine_mounts_later_if_failed"
    if decision == "track_in_flight_order":
        return "basket_in_flight_tracking"
    if decision == "buy_before_suspension_work":
        return "basket_suspension_setup"
    if decision == "source_toyota_oe_glow_plugs_by_part_number":
        return "basket_mechanical_local_bundle"
    if decision in {"capture_brake_specs_then_order", "open_inspect_then_order_standard_brake_parts"}:
        return "basket_merged_brake_suspension_window"
    if decision in {"buy_bleed_consumables_before_opening_hydraulics", "buy_remaining_brake_bleed_consumables"}:
        return "basket_brake_hydraulic_opening_prep"
    if decision == "buy_chassis_masking_consumables":
        return "basket_chassis_coating_consumables"
    if decision in {"hose_rubber_release_hold", "hose_local_market_order_ready"}:
        return "basket_hose_rubber_local_order_ready"
    if decision == "clutch_hydraulic_inspect_then_exact_order":
        return "basket_clutch_hydraulic_inspection"
    if decision in {"defer_as_non_baseline", "defer_until_baseline_closure", "hold_until_post_weld_primer", "hold_until_body_closed"}:
        return "basket_deferred"
    if decision.startswith("not_required"):
        return "basket_deferred"
    if decision in {"buy_body_fastener_hardware_from_samples", "capture_body_hardware_samples_then_order"}:
        return "basket_body_fastener_hardware"
    if mode == "local_fastener_hardware":
        return "basket_body_fastener_hardware"
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
        "basket_compact_cabin_fuse_boxes": ("Compact Cabin Fuse Boxes", "Buy or source compact cabin fuse protection with 3 isolated 6-fuse input groups."),
        "basket_mechanical_local_bundle": ("Mechanical Local Bundle", "Single local Toyota/common supplier batch after inspection."),
        "basket_condition_based_after_inspection": ("Condition-Based Replacements", "Buy only failed/worn parts after inspection."),
        "basket_engine_mounts_later_if_failed": ("Engine Mounts Later If Failed", "No engine lift in baseline; inspect in place before any purchase."),
        "basket_suspension_setup": ("Suspension Setup Support", "Buy support/cribbing items before suspension disassembly."),
        "basket_merged_brake_suspension_window": ("Merged Brake/Suspension Window", "Capture fitted hardware and old samples, then order exact brake parts for the Ironman install window."),
        "basket_brake_hydraulic_opening_prep": ("Brake Hydraulic Opening Prep", "Buy the remaining caps/plugs, brake cleaner, bleed hose/bottle or bleeder kit, rags, gloves, and catch tray before opening hydraulic lines; DOT 3 fluid is already ordered separately."),
        "basket_chassis_coating_consumables": ("Chassis Coating Consumables", "Buy or track masking tape and solvent-safe lint-free wipes before solvent wipe, primer, seam sealer, and Raptor; only buy separate tapered plugs if the on-hand grommet pack fails fit/solvent checks."),
        "basket_hose_rubber_local_order_ready": ("Hose/Rubber Local Order Ready", "Fuel, coolant, heater, vacuum, and breather stock rows have explicit local-market buy lengths; final trim, clamp, chafe, and leak checks remain install tasks."),
        "basket_clutch_hydraulic_inspection": ("Clutch Hydraulic Inspection", "Inspect master/slave/line condition first, then order exact hydraulic refresh parts only if failed."),
        "basket_body_fastener_hardware": ("Body Fastener Hardware", "Buy exact body fastener/captive hardware from old samples; track Millat-covered stock separately."),
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
        if (
            row["timing_window"] in {"tub_off_immediate", "in_flight_now"}
            and row["pass2_decision"] in {"buy_minimum_qty_now", "track_in_flight_order"}
        )
        or row["pass2_decision"] == "buy_remaining_brake_bleed_consumables"
        or row["pass2_decision"] == "buy_chassis_masking_consumables"
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
    lines.append("- Use the received body-chemistry stock after receipt/condition checks; do not rebuy solvent, seam sealer, cavity wax, or primer unless a received item fails inspection.")
    lines.append("- Move most electrical purchases to stock-audit/top-up mode.")
    lines.append("- Move mechanical baseline list into one local Toyota/common supplier bundle after inspection.")
    lines.append("- Keep DOT 3 brake-fluid opening prep purchase-ready before hydraulic lines are opened.")
    lines.append("- Track chassis masking tape and solvent-safe wipe delivery before primer/sealer/Raptor work; use on-hand grommets as temporary open-hole masking only after fit and solvent checks.")
    lines.append("- Move brake rows into the merged suspension/brake window: capture measurements and samples first, then order exact parts.")
    lines.append("- Move fuel/coolant/heater/vacuum hose rows to the local-market order sheet with explicit buy lengths, while keeping final trim, clamp, chafe, and leak checks at install.")
    lines.append("- Keep clutch hydraulics inspect-first, then buy exact master/slave/flex/hard-line parts only if failed.")
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
