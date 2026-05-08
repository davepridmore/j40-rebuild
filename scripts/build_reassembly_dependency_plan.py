from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANUAL_DIR = ROOT / "data" / "manual"
DOCS_DIR = ROOT / "docs"

COMPONENT_JOBS_PATH = MANUAL_DIR / "component_jobs.csv"
COMPONENT_RECON_PATH = MANUAL_DIR / "component_jobs_photo_reconciliation.csv"
EXPENSES_PATH = MANUAL_DIR / "expenses.csv"
PARTS_WEEK_PATH = MANUAL_DIR / "parts_buy_now_this_week.csv"
PARTS_OVERLAP_RESOLUTION_PATH = MANUAL_DIR / "parts_overlap_resolution.csv"
WORKBOOK_TIDY_PATH = MANUAL_DIR / "j40_costs_cost_tabs_tidy.csv"
PHOTO_INVENTORY_PATH = MANUAL_DIR / "photo_inventory.csv"

REASSEMBLY_PACKAGES_PATH = MANUAL_DIR / "reassembly_work_packages.csv"
DEPENDENCY_EDGES_PATH = MANUAL_DIR / "reassembly_dependency_edges.csv"
COMPONENT_DISPOSITION_PATH = MANUAL_DIR / "component_disposition_plan.csv"
PROCUREMENT_DECISIONS_PATH = MANUAL_DIR / "procurement_decision_matrix.csv"
REPORT_PATH = DOCS_DIR / "reassembly-dependency-procurement-plan.md"


@dataclass(frozen=True)
class WorkPackage:
    work_package_id: str
    title: str
    lane: str
    objective: str
    depends_on: str
    linked_workstreams: str
    current_state: str
    evidence_signal: str
    blocker_summary: str
    gate_to_close: str
    key_procurement_actions: str


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize_text(text: str) -> str:
    lowered = text.lower()
    lowered = lowered.replace("&", " and ")
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, normalize_text(left), normalize_text(right)).ratio()


def meaningful_tokens(text: str) -> set[str]:
    tokens = set(normalize_text(text).split())
    stop = {
        "and",
        "for",
        "with",
        "kit",
        "set",
        "the",
        "plus",
        "high",
        "low",
        "front",
        "rear",
        "wire",
        "wires",
        "item",
        "part",
        "quote",
    }
    return {token for token in tokens if len(token) >= 4 and token not in stop}


def load_workbook_stock_rows() -> list[dict[str, str]]:
    rows = load_csv(WORKBOOK_TIDY_PATH)
    return [
        row
        for row in rows
        if row.get("row_disposition") == "line_item"
        and (row.get("received_status") == "yes" or row.get("paid_status") in {"yes", "cod"})
    ]


def is_electrical_stock_row(row: dict[str, str]) -> bool:
    source_sheet = (row.get("source_sheet") or "").strip().lower()
    text = f"{row.get('item', '')} {row.get('extra_notes', '')}".lower()
    return (
        source_sheet == "wiring"
        or "wiring_material" in text
        or "migrated from wiring" in text
    )


def best_stock_match(item: str, stock_rows: list[dict[str, str]]) -> tuple[float, int, dict[str, str] | None]:
    best_score = 0.0
    best_overlap = 0
    best_row: dict[str, str] | None = None
    item_tokens = meaningful_tokens(item)
    for row in stock_rows:
        candidate_item = row.get("item", "")
        score = similarity(item, candidate_item)
        overlap = len(item_tokens & meaningful_tokens(candidate_item))
        if score > best_score or (score == best_score and overlap > best_overlap):
            best_score = score
            best_overlap = overlap
            best_row = row
    return best_score, best_overlap, best_row


def load_overlap_decisions() -> dict[str, str]:
    rows = load_csv(PARTS_OVERLAP_RESOLUTION_PATH)
    decision_map: dict[str, str] = {}
    for row in rows:
        chosen = [value.strip() for value in (row.get("chosen_entries") or "").split("|") if value.strip()]
        deferred = [value.strip() for value in (row.get("deferred_entries") or "").split("|") if value.strip()]
        for entry_id in chosen:
            decision_map[entry_id] = "chosen"
        for entry_id in deferred:
            decision_map[entry_id] = "deferred"
    return decision_map


def build_procurement_decisions(
    expenses_rows: list[dict[str, str]],
    week_rows: list[dict[str, str]],
    stock_rows: list[dict[str, str]],
    overlap_decisions: dict[str, str],
) -> list[dict[str, str]]:
    week_action_map = {row.get("entry_id", ""): row.get("next_action", "") for row in week_rows}
    electrical_stock_count = sum(1 for row in stock_rows if is_electrical_stock_row(row))

    decisions: list[dict[str, str]] = []
    for row in expenses_rows:
        if row.get("bucket", "").strip().lower() != "parts":
            continue

        status = (row.get("status") or "").strip().lower()
        procurement_stage = (row.get("procurement_stage") or "").strip().lower()
        delivery_status = (row.get("delivery_status") or "").strip().lower()
        if status == "cancelled" or delivery_status == "not_required" or procurement_stage.startswith("not_required"):
            continue
        if status in {"installed", "received", "credited"} or procurement_stage in {"received", "completed"}:
            continue

        entry_id = row.get("entry_id", "")
        item = row.get("item", "")
        workstream = row.get("workstream", "")
        notes = row.get("notes", "")
        amount = row.get("amount", "")
        amount_status = row.get("amount_status", "")

        week_action = week_action_map.get(entry_id, "")
        overlap_status = overlap_decisions.get(entry_id, "")
        stock_score, stock_overlap, stock_row = best_stock_match(item, stock_rows)
        stock_signal = "none"
        stock_match_item = ""
        if stock_row and stock_score >= 0.74 and stock_overlap >= 1:
            stock_signal = "possible_on_hand"
            stock_match_item = stock_row.get("item", "")

        decision = "review"
        dependency_gate = "general"
        action = "review_line"
        reason = "No rule matched."

        if overlap_status == "deferred":
            decision = "defer_duplicate_overlap"
            dependency_gate = "selected_alternative"
            action = "do_not_buy_duplicate"
            reason = "Entry is explicitly deferred by overlap-resolution decision."
        elif procurement_stage == "ordered_pending_delivery":
            decision = "track_ordered_delivery"
            dependency_gate = "electrical_body_mechanical_as_needed"
            action = "confirm_delivery_and_quality"
            reason = "Item is already ordered and should be tracked through delivery."
        elif procurement_stage in {"deferred_optional"} or workstream == "optional_upgrades":
            decision = "defer_optional"
            dependency_gate = "after_baseline_validation"
            action = "hold_until_baseline_complete"
            reason = "Optional scope is intentionally deferred behind baseline completion."
        elif procurement_stage == "deferred_until_body_closed":
            decision = "hold_until_body_closed"
            dependency_gate = "body_sealed"
            action = "do_not_buy_yet"
            reason = "Material should be purchased only after floor/body sealing gate."
        elif procurement_stage == "spec_ready_release_hold":
            decision = "release_hold_measure_then_order"
            dependency_gate = "measurement_release_hold"
            action = "use_exact_spec_after_measurement_gate"
            reason = "Exact ordering basis exists, but payment/fabrication waits for sample, route, fitting, or station measurement release."
        elif procurement_stage == "researching":
            decision = "research_compare_then_select"
            dependency_gate = "scope_freeze"
            action = "close_options_and_select_one"
            reason = "Item is still in compare/research state."
        elif procurement_stage == "next_phase_purchase":
            decision = "next_phase_gate"
            dependency_gate = "after_current_phase_exit"
            action = "keep_visible_but_not_now"
            reason = "Planned for later phase once current gate closes."
        elif procurement_stage.startswith("purchase_ready"):
            if week_action == "order_from_selected_quote":
                decision = "buy_now_from_quote"
                dependency_gate = "baseline_electrical_or_mechanical"
                action = "place_order_now"
                reason = "Selected quote is already in this-week execution list."
            elif week_action == "confirm_price_then_order":
                if stock_signal == "possible_on_hand":
                    decision = "verify_stock_before_buy"
                    dependency_gate = "inventory_check"
                    action = "physically_check_stock_then_buy_if_missing"
                    reason = "Similar item appears as received/paid in workbook stock data."
                else:
                    decision = "confirm_price_then_buy"
                    dependency_gate = "baseline_execution"
                    action = "lock_vendor_price_and_order"
                    reason = "Item is buy-now but still missing confirmed amount."
            elif stock_signal == "possible_on_hand":
                decision = "verify_stock_before_buy"
                dependency_gate = "inventory_check"
                action = "confirm_on_hand_quantity"
                reason = "Similar item appears as received/paid in workbook stock data."
            else:
                decision = "buy_now"
                dependency_gate = "baseline_execution"
                action = "order_now"
                reason = "Marked purchase-ready with no deferral flags."
        elif procurement_stage == "needs_confirmation":
            decision = "confirm_order_state"
            dependency_gate = "evidence_reconciliation"
            action = "verify_invoice_or_delivery_proof"
            reason = "State is explicitly uncertain and needs evidence reconciliation."

        if "inspect then replace" in notes.lower():
            decision = "inspect_then_buy"
            dependency_gate = "mechanical_inspection"
            action = "inspect_condition_first"
            reason = "Notes explicitly require inspection before replacement decision."

        if "must replace" in notes.lower() and decision in {"review", "next_phase_gate"}:
            decision = "buy_for_baseline"
            dependency_gate = "mechanical_baseline"
            action = "buy_in_baseline_window"
            reason = "Notes mark item as baseline mandatory replacement."

        if (
            workstream == "electrical_reset"
            and procurement_stage == "purchase_ready"
            and decision in {"confirm_price_then_buy", "buy_now"}
            and week_action != "order_from_selected_quote"
            and re.search(r"wire|sleev|relay|connector|grommet|fuse", item, re.I)
            and electrical_stock_count >= 20
        ):
            decision = "verify_stock_before_buy"
            dependency_gate = "inventory_check"
            action = "physically_check_stock_then_buy_if_missing"
            reason = "Wiring stock tab already shows substantial received material; validate on-hand quantity before rebuy."

        if entry_id == "part_cabin_compact_fuse_boxes":
            decision = "confirm_price_then_buy"
            dependency_gate = "baseline_electrical"
            action = "confirm_compact_model_quantity_then_buy"
            reason = "Cabin fuse protection is not ordered stock; provide 3 isolated under-dash input groups with 6 fuses each: constant battery, IGN/RUN, and ACC/part-way. A single OEM box is acceptable if the buses are isolated and mapped."
        elif entry_id == "part_mech_engine_mount_set":
            decision = "defer_until_mount_failure_or_engine_lift_scope"
            dependency_gate = "in_place_mount_inspection"
            action = "inspect_in_place_no_engine_lift_purchase"
            reason = (
                "No engine-lift baseline: inspect mounts in place; defer purchase unless failed or "
                "another approved job already supports/lifts the engine. EPS column conversion does not require engine removal."
            )
        elif entry_id == "part_power_steering_upgrade":
            decision = "research_compare_then_select"
            dependency_gate = "market_scout"
            action = "complete_pre_payment_check"
            reason = "Quote and buy/no-buy decision only; use the SCP90/NCP90 EPS market scout spec."
        elif entry_id == "part_suspension_wooden_cribbing_blocks" and procurement_stage != "ordered_pending_delivery":
            decision = "confirm_price_then_buy"
            dependency_gate = "baseline_execution"
            action = "quote_against_wood_cut_list"
            reason = (
                "Merchant-facing cut list is ready; confirm price for 8 x 12x6x3 in hardwood blocks "
                "plus 4 tapered 8x4x3 in wedge chocks."
            )
        elif entry_id == "part_mech_heat_glow_plugs_set":
            decision = "confirm_price_then_buy"
            dependency_gate = "baseline_execution"
            action = "source_toyota_oe_by_part_number"
            reason = (
                "Buy exact Toyota-labelled glow plugs: 19850-68030 x6 for HJ47-style 2H 12V/8.5V, "
                "or 19850-68060 x6 only if old plug/system confirms 24V/superglow."
            )
        elif entry_id == "part_brake_fluid_bleed_consumables":
            decision = "buy_remaining_brake_bleed_consumables"
            dependency_gate = "hydraulic_opening_prep"
            action = "confirm_price_for_caps_bleed_cleaning_consumables"
            reason = "DOT 3 brake fluid is already ordered separately; hydraulics must not be opened until that sealed fluid and the remaining caps/plugs, cleaner, and bleed tools are physically on hand."
        elif entry_id == "part_mech_brake_flex_hose_set":
            decision = "capture_spec_then_buy"
            dependency_gate = "brake_identification_and_samples"
            action = "measure_label_keep_samples_then_order"
            reason = (
                "Complete crimped brake hose assemblies are baseline scope and can be quoted online/local, "
                "but final order waits for fitted end fittings, brackets, free length, and Ironman full-droop slack."
            )
        elif workstream == "brake_system" and procurement_stage == "spec_needed_before_order":
            decision = "capture_spec_then_buy"
            dependency_gate = "brake_identification_and_samples"
            action = "measure_label_keep_samples_then_order"
            reason = (
                "Brake item is baseline scope, but exact part release is gated by fitted hardware, "
                "old samples, fitting style, and Ironman full-droop clearance where applicable."
            )
        elif workstream == "body_chassis" and procurement_stage in {"spec_needed_before_order", "spec_ready_release_hold"}:
            decision = "capture_body_hardware_samples_then_order"
            dependency_gate = "body_hardware_sample_sorting"
            action = "sort_measure_label_samples_then_order_or_fabricate"
            reason = (
                "Body hardware/body-mount ordering basis is defined, but release waits for old-sample "
                "location, dimensions, thread, material, station height, and condition sorting."
            )
        elif workstream == "brake_system" and procurement_stage == "inspect_then_buy":
            decision = "inspect_confirm_then_buy_standard"
            dependency_gate = "brake_open_inspection"
            action = "open_measure_then_order_standard_service_parts"
            reason = (
                "Brake item is standard baseline service scope, but exact purchase waits for drum or rotor "
                "inspection and measured part family."
            )

        decisions.append(
            {
                "entry_id": entry_id,
                "workstream": workstream,
                "item": item,
                "status": status,
                "procurement_stage": procurement_stage,
                "amount": amount,
                "amount_status": amount_status,
                "week_plan_action": week_action,
                "overlap_status": overlap_status,
                "stock_signal": stock_signal,
                "stock_match_item": stock_match_item,
                "stock_match_score": f"{stock_score:.3f}" if stock_row else "",
                "decision": decision,
                "dependency_gate": dependency_gate,
                "recommended_action": action,
                "decision_reason": reason,
            }
        )

    return sorted(decisions, key=lambda row: (row["workstream"], row["decision"], row["entry_id"]))


def build_component_disposition(
    component_rows: list[dict[str, str]],
    recon_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    recon_map = {row.get("component_job_id", ""): row for row in recon_rows}
    output: list[dict[str, str]] = []

    for row in component_rows:
        component_id = row.get("component_job_id", "")
        status = row.get("current_status", "")
        recon = recon_map.get(component_id, {})

        direct_count = recon.get("direct_match_count", "")
        direct_components = recon.get("direct_specific_components", "")
        photo_status = recon.get("reconciliation_status", "no_reconciliation")

        disposition = "review"
        reuse_decision = "inspect_then_decide"
        pre_reassembly_action = "confirm_state_and_tag"
        dependency_lane = "body_and_trim"

        if status == "planned_send_out":
            disposition = "refurbish_send_out"
            reuse_decision = "reuse_after_refurbish"
            pre_reassembly_action = "confirm_vendor_scope_and_return_condition"
            dependency_lane = "body_and_weather_seal"
        elif status == "planned_separate_service":
            disposition = "refurbish_service_subcomponents"
            reuse_decision = "reuse_after_service"
            pre_reassembly_action = "service_mechanisms_and_rubbers_before_refit"
            dependency_lane = "body_and_weather_seal"
        elif status == "planned_strip":
            disposition = "clean_store_for_reuse"
            reuse_decision = "reuse_existing"
            pre_reassembly_action = "complete_tagging_and_damage_check"
            dependency_lane = "interior_refit"
        elif status == "partially_removed":
            disposition = "remove_nonbaseline_and_refit_clean"
            reuse_decision = "reuse_after_rewire"
            pre_reassembly_action = "finish_deletion_of_old_accessory_wiring"
            dependency_lane = "electrical"
        elif status == "pending_exposure_inspection":
            disposition = "repair_in_place"
            reuse_decision = "reuse_after_repair_and_seal"
            pre_reassembly_action = "close_floor_rust_map_and_repair_scope"
            dependency_lane = "body_structure"
        elif status == "planned_scope_lock" and row.get("storage_or_vendor", "") == "market_scout":
            pre_reassembly_action = "confirm_market_evidence"
            dependency_lane = "procurement"

        output.append(
            {
                "component_job_id": component_id,
                "component_group": row.get("component_group", ""),
                "current_status": status,
                "photo_reconciliation_status": photo_status,
                "direct_photo_count": direct_count,
                "direct_specific_components": direct_components,
                "recommended_disposition": disposition,
                "reuse_decision": reuse_decision,
                "pre_reassembly_action": pre_reassembly_action,
                "dependency_lane": dependency_lane,
                "evidence_ref": row.get("evidence_ref", ""),
            }
        )

    return output


def summarize_photo_stage_counts(photo_rows: list[dict[str, str]]) -> Counter[str]:
    return Counter((row.get("stage") or "").strip() for row in photo_rows if row.get("stage"))


def count_decision(decision_rows: list[dict[str, str]], *keys: str) -> int:
    allowed = set(keys)
    return sum(1 for row in decision_rows if row.get("decision") in allowed)


def count_mechanical_buy_actions(decision_rows: list[dict[str, str]]) -> int:
    actions = {
        "confirm_price_then_buy",
        "buy_now",
        "buy_for_baseline",
        "buy_now_from_quote",
        "buy_remaining_brake_bleed_consumables",
        "capture_spec_then_buy",
        "inspect_confirm_then_buy_standard",
    }
    return sum(
        1
        for row in decision_rows
        if row.get("workstream") in {"mechanical_baseline", "steering_brakes_suspension", "brake_system"} and row.get("decision") in actions
    )


def build_work_packages(
    stage_counts: Counter[str],
    decision_rows: list[dict[str, str]],
    component_disposition_rows: list[dict[str, str]],
) -> list[WorkPackage]:
    electrical_rework_photos = stage_counts.get("electrical_rework", 0)
    rust_photos = stage_counts.get("rust_assessment", 0)
    stripdown_photos = stage_counts.get("stripdown_cataloguing", 0)

    body_buy_now = sum(
        1
        for row in decision_rows
        if row.get("workstream") == "body_chassis"
        and row.get("decision")
        in {"confirm_price_then_buy", "buy_now", "buy_now_from_quote", "capture_body_hardware_samples_then_order"}
    )
    electrical_buy_now = sum(
        1
        for row in decision_rows
        if row.get("workstream") == "electrical_reset"
        and row.get("decision") in {"buy_now_from_quote", "buy_now", "confirm_price_then_buy", "track_ordered_delivery"}
    )
    electrical_verify_stock = sum(
        1 for row in decision_rows if row.get("workstream") == "electrical_reset" and row.get("decision") == "verify_stock_before_buy"
    )
    mech_buy_now = sum(
        1
        for row in decision_rows
        if row.get("workstream") in {"mechanical_baseline", "steering_brakes_suspension", "brake_system"}
        and row.get("decision") in {
            "confirm_price_then_buy",
            "buy_now",
            "buy_for_baseline",
            "buy_remaining_brake_bleed_consumables",
            "capture_spec_then_buy",
            "inspect_confirm_then_buy_standard",
        }
    )

    refurbish_scope = sum(
        1
        for row in component_disposition_rows
        if row.get("recommended_disposition") in {"refurbish_send_out", "refurbish_service_subcomponents"}
    )

    packages = [
        WorkPackage(
            work_package_id="WP01",
            title="Body Floor Rust Closure",
            lane="body_structure",
            objective="Close floor/rust repairs and welding scope before sealing products.",
            depends_on="stripdown_cataloguing_complete",
            linked_workstreams="body_chassis",
            current_state="in_progress" if rust_photos >= 8 else "queued",
            evidence_signal=f"rust_assessment_photos={rust_photos}, stripdown_photos={stripdown_photos}",
            blocker_summary=f"{body_buy_now} body material rows still need buy execution.",
            gate_to_close="Rust map signed off and repaired zones primed.",
            key_procurement_actions="Use received primer/prep/seam-sealer/cavity-wax stock and on-hand Raptor; track delivery of purchased masking tape/solvent-safe wipes; use on-hand grommets for temporary open-hole masking after fit/solvent check; no generic chassis-black or bed-lining duplicate buy.",
        ),
        WorkPackage(
            work_package_id="WP02",
            title="Panel + Seals Refurbishment Returns",
            lane="body_weather_seal",
            objective="Return removable panels, seals/windows, and vent/quarter window assemblies in refurb-ready condition for fit-up.",
            depends_on="WP01",
            linked_workstreams="stripdown_cataloguing|body_chassis",
            current_state="in_progress" if refurbish_scope >= 4 else "queued",
            evidence_signal=f"component_refurbish_candidates={refurbish_scope}",
            blocker_summary="Vendor scope/return status tracking must be explicit per component.",
            gate_to_close="Doors/hood/windows/rubbers mechanically serviceable, vent assemblies bench-checked, and tagged for refit.",
            key_procurement_actions="Only buy replacement seals/glass/mechanisms after refurbish inspection confirms non-reusable items.",
        ),
        WorkPackage(
            work_package_id="WP03",
            title="Electrical Baseline Finalization",
            lane="electrical",
            objective="Complete baseline harness termination, grounding, and fuse/relay validation.",
            depends_on="stripdown_cataloguing_complete",
            linked_workstreams="electrical_reset",
            current_state="in_progress" if electrical_rework_photos >= 30 else "queued",
            evidence_signal=f"electrical_rework_photos={electrical_rework_photos}",
            blocker_summary=f"{electrical_buy_now} electrical buy rows still open; {electrical_verify_stock} rows should be stock-verified before re-buy.",
            gate_to_close="Start/charge/lights/horn/wipers/gauges baseline passes functional checks.",
            key_procurement_actions="Order selected harness/sleeving path; verify on-hand connectors/relays before duplicate buys.",
        ),
        WorkPackage(
            work_package_id="WP04",
            title="Mechanical Service Baseline",
            lane="mechanical",
            objective="Execute reliability service pack, merged brake refresh prep, and document defects before upgrades.",
            depends_on="stripdown_cataloguing_complete",
            linked_workstreams="mechanical_baseline|steering_brakes_suspension|brake_system",
            current_state="queued",
            evidence_signal="engine_bay baseline evidence present; service pack and brake-system rows prepared",
            blocker_summary=f"{mech_buy_now} mechanical/brake safety rows need pricing, measurement capture, or order.",
            gate_to_close="Cooling/fuel/ignition/brake baseline complete with leak-free checks.",
            key_procurement_actions="Batch-buy must-replace consumables; run brake spec capture before exact brake orders; keep inspect-then-replace items gated to measured findings.",
        ),
        WorkPackage(
            work_package_id="WP05",
            title="Interior Weatherproofing Stack",
            lane="interior",
            objective="Apply sealing/lining/dampening/foam/carpet in moisture-safe sequence.",
            depends_on="WP01",
            linked_workstreams="interior_weatherproofing",
            current_state="blocked",
            evidence_signal="deferred rows indicate intentional hold until body closure",
            blocker_summary="Interior finish materials are deferred until floor/body sealing gate closes.",
            gate_to_close="Cabin sealed and dry before trim/final fit.",
            key_procurement_actions="Do not buy full interior finish stack early; release purchases by phase gate.",
        ),
        WorkPackage(
            work_package_id="WP06",
            title="Reassembly + Validation",
            lane="integration",
            objective="Controlled re-fit and end-to-end validation with punch-list closure.",
            depends_on="WP02|WP03|WP04|WP05",
            linked_workstreams="final_assembly_validation",
            current_state="queued",
            evidence_signal="Prerequisite work packages not yet gate-closed",
            blocker_summary="Needs closure of body, electrical, and mechanical baseline packages.",
            gate_to_close="Roadworthy baseline validation passed with residual defects logged.",
            key_procurement_actions="Only release optional upgrades after baseline validation sign-off.",
        ),
    ]
    return packages


def build_dependency_edges() -> list[dict[str, str]]:
    return [
        {"dependency_type": "hard", "from_work_package": "WP01", "to_work_package": "WP02", "rationale": "Panel/seal fit-up follows floor/body closure."},
        {"dependency_type": "hard", "from_work_package": "WP01", "to_work_package": "WP05", "rationale": "Interior weatherproofing must follow structural repair + sealing."},
        {"dependency_type": "hard", "from_work_package": "WP02", "to_work_package": "WP06", "rationale": "Body panels/windows/seals must be available for final fit."},
        {"dependency_type": "hard", "from_work_package": "WP03", "to_work_package": "WP06", "rationale": "Electrical baseline must pass before integration validation."},
        {"dependency_type": "hard", "from_work_package": "WP04", "to_work_package": "WP06", "rationale": "Mechanical safety baseline must close before road validation."},
        {"dependency_type": "hard", "from_work_package": "WP05", "to_work_package": "WP06", "rationale": "Interior finish closes before final integration."},
        {"dependency_type": "parallel", "from_work_package": "WP01", "to_work_package": "WP03", "rationale": "Body rust work and baseline wiring can run in parallel."},
        {"dependency_type": "parallel", "from_work_package": "WP01", "to_work_package": "WP04", "rationale": "Body closure and mechanical service can run in parallel."},
        {"dependency_type": "parallel", "from_work_package": "WP02", "to_work_package": "WP03", "rationale": "Panel refurbish return tracking can run while electrical finalization continues."},
    ]


def write_report(
    work_packages: list[WorkPackage],
    dependency_rows: list[dict[str, str]],
    component_rows: list[dict[str, str]],
    procurement_rows: list[dict[str, str]],
    stage_counts: Counter[str],
) -> None:
    decision_counts = Counter(row.get("decision", "") for row in procurement_rows)
    component_counts = Counter(row.get("recommended_disposition", "") for row in component_rows)
    lane_counts = Counter(package.lane for package in work_packages)

    lines: list[str] = []
    lines.append("# Reassembly, Dependency, and Procurement Plan")
    lines.append("")
    lines.append(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("- Work packages: `data/manual/reassembly_work_packages.csv`")
    lines.append("- Dependency edges: `data/manual/reassembly_dependency_edges.csv`")
    lines.append("- Component disposition: `data/manual/component_disposition_plan.csv`")
    lines.append("- Procurement decisions: `data/manual/procurement_decision_matrix.csv`")
    lines.append("")
    lines.append("## Current Evidence Snapshot")
    lines.append("")
    lines.append(f"- `electrical_rework` photos: {stage_counts.get('electrical_rework', 0)}")
    lines.append(f"- `rust_assessment` photos: {stage_counts.get('rust_assessment', 0)}")
    lines.append(f"- `stripdown_cataloguing` photos: {stage_counts.get('stripdown_cataloguing', 0)}")
    lines.append("")
    lines.append("## Bifurcated Dependency Lanes")
    lines.append("")
    for lane, count in sorted(lane_counts.items()):
        lines.append(f"- `{lane}`: {count} work package(s)")
    lines.append("")
    lines.append("## Procurement Decisions")
    lines.append("")
    for key in sorted(decision_counts):
        lines.append(f"- `{key}`: {decision_counts[key]}")
    lines.append("")
    lines.append("## Component Reuse/Refurbish Decisions")
    lines.append("")
    for key in sorted(component_counts):
        lines.append(f"- `{key}`: {component_counts[key]}")
    lines.append("")
    lines.append("## Immediate Execution Focus")
    lines.append("")
    lines.append(
        f"- Close `WP01` + `WP03` in parallel: body rust closure and electrical baseline finalization are both active and should keep moving."
    )
    lines.append(
        f"- Run `WP04` procurement now: {count_mechanical_buy_actions(procurement_rows)} mechanical rows still require buy execution."
    )
    lines.append(
        f"- Avoid duplicate buys: {decision_counts.get('verify_stock_before_buy', 0)} rows are flagged as likely already on hand and should be physically stock-checked first."
    )
    lines.append(
        "- Keep interior finish gated: bedliner application/sound/foam/carpet stay blocked until body sealing gate is formally closed, with no extra bed-lining purchase in the baseline."
    )

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    component_rows = load_csv(COMPONENT_JOBS_PATH)
    recon_rows = load_csv(COMPONENT_RECON_PATH)
    expenses_rows = load_csv(EXPENSES_PATH)
    week_rows = load_csv(PARTS_WEEK_PATH)
    stock_rows = load_workbook_stock_rows()
    overlap_decisions = load_overlap_decisions()
    photo_rows = load_csv(PHOTO_INVENTORY_PATH)

    procurement_rows = build_procurement_decisions(expenses_rows, week_rows, stock_rows, overlap_decisions)
    component_disposition_rows = build_component_disposition(component_rows, recon_rows)
    stage_counts = summarize_photo_stage_counts(photo_rows)
    work_packages = build_work_packages(stage_counts, procurement_rows, component_disposition_rows)
    dependency_rows = build_dependency_edges()

    write_csv(
        REASSEMBLY_PACKAGES_PATH,
        [package.__dict__ for package in work_packages],
        [
            "work_package_id",
            "title",
            "lane",
            "objective",
            "depends_on",
            "linked_workstreams",
            "current_state",
            "evidence_signal",
            "blocker_summary",
            "gate_to_close",
            "key_procurement_actions",
        ],
    )

    write_csv(
        DEPENDENCY_EDGES_PATH,
        dependency_rows,
        ["dependency_type", "from_work_package", "to_work_package", "rationale"],
    )

    write_csv(
        COMPONENT_DISPOSITION_PATH,
        component_disposition_rows,
        [
            "component_job_id",
            "component_group",
            "current_status",
            "photo_reconciliation_status",
            "direct_photo_count",
            "direct_specific_components",
            "recommended_disposition",
            "reuse_decision",
            "pre_reassembly_action",
            "dependency_lane",
            "evidence_ref",
        ],
    )

    write_csv(
        PROCUREMENT_DECISIONS_PATH,
        procurement_rows,
        [
            "entry_id",
            "workstream",
            "item",
            "status",
            "procurement_stage",
            "amount",
            "amount_status",
            "week_plan_action",
            "overlap_status",
            "stock_signal",
            "stock_match_item",
            "stock_match_score",
            "decision",
            "dependency_gate",
            "recommended_action",
            "decision_reason",
        ],
    )

    write_report(work_packages, dependency_rows, component_disposition_rows, procurement_rows, stage_counts)

    print(f"Wrote work packages: {REASSEMBLY_PACKAGES_PATH.relative_to(ROOT)}")
    print(f"Wrote dependencies: {DEPENDENCY_EDGES_PATH.relative_to(ROOT)}")
    print(f"Wrote component disposition: {COMPONENT_DISPOSITION_PATH.relative_to(ROOT)}")
    print(f"Wrote procurement decisions: {PROCUREMENT_DECISIONS_PATH.relative_to(ROOT)}")
    print(f"Wrote report: {REPORT_PATH.relative_to(ROOT)}")
    print(f"Work packages: {len(work_packages)}")
    print(f"Procurement rows evaluated: {len(procurement_rows)}")


if __name__ == "__main__":
    main()
