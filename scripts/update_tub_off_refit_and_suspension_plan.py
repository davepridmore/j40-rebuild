from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet


DEFAULT_WORKBOOK_PATH = Path("/Users/davidpridmore/Documents/J40_Costs.xlsx")
DEFAULT_REPORT_PATH = Path("docs/tub-off-refit-execution-plan.md")

HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True)


def autosize_columns(ws: Worksheet, max_width: int = 70) -> None:
    for col in range(1, ws.max_column + 1):
        letter = get_column_letter(col)
        width = 0
        for row in range(1, ws.max_row + 1):
            value = ws.cell(row=row, column=col).value
            if value is None:
                continue
            width = max(width, len(str(value)))
        ws.column_dimensions[letter].width = min(max(width + 2, 10), max_width)


def style_header_row(ws: Worksheet, row_idx: int) -> None:
    for col in range(1, ws.max_column + 1):
        cell = ws.cell(row=row_idx, column=col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT


def update_build_plan(workbook) -> None:
    ws = workbook["Build_Plan"]
    headers = [ws.cell(1, c).value for c in range(1, 9)]
    rows = []
    for r in range(2, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, 9)]
        if any(v not in (None, "") for v in vals):
            rows.append(vals)

    by_id = {str(r[1]): r for r in rows if r[1]}

    def upsert(record: list[object]) -> None:
        by_id[str(record[1])] = record

    upsert(
        [
            "work_package",
            "WP01A",
            "Tub Lift + Mount-Point Mapping",
            "body_structure",
            "queued",
            "stripdown_cataloguing_complete",
            "Tub lifted and every body/chassis mount point mapped before welding closure.",
            "Tag all mount points, captive nuts, shim positions, hole condition, and required repair action before refit planning.",
        ]
    )
    upsert(
        [
            "work_package",
            "WP01B",
            "Chassis/Tub Interface Weld Closure",
            "body_structure",
            "queued",
            "WP01A",
            "All mount interfaces weld-repaired, protected, and dimension-checked for refit.",
            "No final tub refit until all mount points pass straightness/fit and anti-corrosion prep checks.",
        ]
    )
    upsert(
        [
            "work_package",
            "WP02A",
            "Tub Refit Interface + Rubber Kit Control",
            "body_weather_seal",
            "queued",
            "WP01B",
            "Body mount rubbers, hardware, and shims selected and trial-fitted before final torque.",
            "Capture exact attachment points and shim stack plan before permanent tub-to-chassis fastening.",
        ]
    )
    upsert(
        [
            "work_package",
            "WP04B",
            "Tub-Off Engine Access Service + Inspection",
            "mechanical",
            "queued",
            "WP01A",
            "Engine-bay access inspection closed with condition-based replacement list.",
            "While tub is off: inspect mounts, hoses, lines, clamps, seals, linkage, and gearbox top-side service items.",
        ]
    )
    upsert(
        [
            "work_package",
            "WP04C",
            "Suspension Setup: Ironman Foamcell Ordered Kit",
            "steering_brakes_suspension",
            "queued",
            "WP01B",
            "Ironman Foamcell kit received, contents-checked, installed, and aligned.",
            "Track main kit shipment plus separate front 24635FE damper shipment; no alternate suspension buys.",
        ]
    )

    # Update WP06 dependency gate if present.
    if "WP06" in by_id:
        wp06 = by_id["WP06"]
        wp06[5] = "WP02|WP02A|WP03|WP04|WP04A|WP04B|WP04C|WP05"
        wp06[7] = (
            "Only release optional upgrades after baseline validation sign-off. "
            "Tub refit control and suspension setup must close first."
        )

    updated_rows = list(by_id.values())
    updated_rows.sort(key=lambda r: (0 if str(r[0]) == "work_package" else 1, str(r[1])))

    # Clear and rewrite.
    for r in range(2, ws.max_row + 1):
        for c in range(1, 9):
            ws.cell(r, c).value = None
    for idx, row in enumerate(updated_rows, start=2):
        for c, value in enumerate(row, start=1):
            ws.cell(idx, c).value = value

    for c, h in enumerate(headers, start=1):
        ws.cell(1, c).value = h


def update_procurement_pass2(workbook) -> None:
    if "Procurement_Pass2" not in workbook.sheetnames:
        return

    ws = workbook["Procurement_Pass2"]
    headers = [ws.cell(1, c).value for c in range(1, 12)]
    rows = []
    for r in range(2, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, 12)]
        if any(v not in (None, "") for v in vals):
            rows.append(vals)

    by_id = {str(r[0]): r for r in rows if r[0]}

    def upsert(record: list[object]) -> None:
        by_id[str(record[0])] = record

    for retired_id in {"part_local_leaf_springs_front", "part_local_leaf_springs_rear"}:
        by_id.pop(retired_id, None)

    # Track the ordered Ironman kit as two shipments.
    upsert(
        [
            "part_ironman_foamcell_suspension_kit",
            "steering_brakes_suspension",
            "Ironman Foamcell suspension kit - main shipment",
            "track_ordered_delivery",
            "import_or_specialty",
            "in_flight_now",
            "track_in_flight_order",
            "delivery_tracking",
            "basket_in_flight_tracking",
            "Track supplier shipment; do not rebuy suspension alternatives.",
            "Ordered 2026-05-01 for PKR 575000 after discount; front dampers tracked separately.",
        ]
    )
    upsert(
        [
            "part_ironman_front_dampers_separate_shipment",
            "steering_brakes_suspension",
            "Ironman Foamcell front damper pair - separate shipment (24635FE x2)",
            "track_ordered_delivery",
            "import_or_specialty",
            "in_flight_now",
            "track_in_flight_order",
            "delivery_tracking",
            "basket_in_flight_tracking",
            "Track separate front-damper shipment; amount included in main kit total.",
            "Verify 24635FE x2 on receipt before closing suspension procurement.",
        ]
    )
    upsert(
        [
            "part_body_mount_rubber_kit",
            "body_chassis",
            "Body-to-chassis mount rubber kit",
            "new_item",
            "local_rubber_or_landcruiser_supplier",
            "pre_tub_refit",
            "measure_then_buy_with_trial_fit",
            "critical_refit_buy",
            "basket_tub_refit_interface",
            "Local rubber/4x4 supplier or custom rubber fabricator if exact kit unavailable.",
            "Tub must not be bolted down until rubbers are test-fitted against mapped mount points.",
        ]
    )
    upsert(
        [
            "part_body_mount_hardware_kit",
            "body_chassis",
            "Body mount bolts, washers, sleeves, captive-nut repairs",
            "new_item",
            "local_fastener_and_fabrication",
            "pre_tub_refit",
            "grade_spec_then_buy",
            "critical_refit_buy",
            "basket_tub_refit_interface",
            "Use graded fasteners and include sleeve/spacer and captive-nut repair provision.",
            "Refit reliability depends on correct hardware grade and mount stack geometry.",
        ]
    )
    upsert(
        [
            "part_body_mount_shim_pack",
            "body_chassis",
            "Body mount shims/spacers alignment pack",
            "new_item",
            "local_fabrication",
            "pre_tub_refit",
            "prepare_before_trial_fit",
            "critical_refit_buy",
            "basket_tub_refit_interface",
            "Fabricate shim pack after mount-point map and weld closure dimensions are confirmed.",
            "Required to align tub seating and panel gaps before final torque.",
        ]
    )
    upsert(
        [
            "part_gearbox_top_service_items",
            "mechanical_baseline",
            "Gearbox top-cover service items (detents, bushes, shift-seat kit)",
            "new_item",
            "local_transmission_supplier",
            "post_tub_off_inspection",
            "inspect_then_local_decide",
            "inspect_first",
            "basket_condition_based_after_inspection",
            "Local transmission parts source; buy only against diagnosed wear.",
            "Targets disengagement/long-throw issue without committing to full rebuild.",
        ]
    )

    updated_rows = list(by_id.values())
    updated_rows.sort(key=lambda r: str(r[0]))

    for r in range(2, ws.max_row + 1):
        for c in range(1, 12):
            ws.cell(r, c).value = None
    for idx, row in enumerate(updated_rows, start=2):
        for c, value in enumerate(row, start=1):
            ws.cell(idx, c).value = value

    for c, h in enumerate(headers, start=1):
        ws.cell(1, c).value = h


def update_parts_estimates(workbook) -> None:
    if "Parts_Estimates" not in workbook.sheetnames:
        return

    ws = workbook["Parts_Estimates"]
    header = [ws.cell(1, c).value for c in range(1, 9)]
    rows = []
    for r in range(2, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, 9)]
        if any(v not in (None, "") for v in vals):
            rows.append(vals)

    # Remove superseded suspension estimate lines to avoid double counting.
    filtered = []
    for row in rows:
        item = str(row[2] or "").strip().lower()
        if any(token in item for token in {"old man emu", "local fabricated leaf springs", "nitrocharger"}):
            continue
        filtered.append(row)
    rows = filtered

    def upsert_by_item(new_row: list[object]) -> None:
        target = str(new_row[2]).strip().lower()
        for i, row in enumerate(rows):
            if str(row[2] or "").strip().lower() == target:
                rows[i] = new_row
                return
        # Insert near suspension section.
        insert_at = None
        for i, row in enumerate(rows):
            if str(row[0] or "").strip() == "Suspension":
                insert_at = i + 1
        if insert_at is None:
            rows.append(new_row)
        else:
            rows.insert(insert_at, new_row)

    upsert_by_item(
        [
            "Suspension",
            "Ordered Kit",
            "Ironman Foamcell suspension kit",
            "1 kit",
            "Ironman 4x4 supplier",
            "575000",
            "575000",
            "High",
        ]
    )
    upsert_by_item(
        [
            "Suspension",
            "Setup",
            "Spring setup, shims, and alignment labor",
            "1 lot",
            "Local suspension workshop",
            "30000-90000",
            "60000",
            "Medium",
        ]
    )
    upsert_by_item(
        [
            "Body / Chassis",
            "Mounts",
            "Body mount shim/spacer set",
            "1 set",
            "Local fabrication / fastener supplier",
            "5000-20000",
            "15000",
            "High",
        ]
    )

    # Rewrite sheet.
    for r in range(2, ws.max_row + 1):
        for c in range(1, 9):
            ws.cell(r, c).value = None
    for idx, row in enumerate(rows, start=2):
        for c, value in enumerate(row, start=1):
            ws.cell(idx, c).value = value
    for c, h in enumerate(header, start=1):
        ws.cell(1, c).value = h


def update_suspension_sheet(workbook) -> None:
    if "Suspension" not in workbook.sheetnames:
        return

    ws = workbook["Suspension"]
    for row_idx in range(2, 12):
        for col_idx in range(1, 5):
            ws.cell(row_idx, col_idx).value = None

    rows = [
        ("Kit", "IRONMAN-FOAMCELL", 1, "Ordered kit; main shipment tracked separately from front dampers."),
        ("Front Dampers", "24635FE", 2, "Separate shipment; verify both units on receipt."),
        ("Rear Dampers", "24636FE", 2, "Verify part numbers during main shipment content check."),
        ("Front Leaf Springs", "TOY001B", 2, "Verify spring orientation and center pins before install."),
        ("Rear Leaf Springs", "TOY002B", 2, "Verify spring orientation and final ride height after settling."),
    ]
    for offset, row in enumerate(rows, start=2):
        for col_idx, value in enumerate(row, start=1):
            ws.cell(offset, col_idx).value = value


def write_tub_off_refit_plan_sheet(workbook) -> None:
    sheet_name = "Tub_Off_Refit_Plan"
    if sheet_name in workbook.sheetnames:
        del workbook[sheet_name]
    ws = workbook.create_sheet(sheet_name)

    ws.append(["Tub-Off To Refit Control Plan"])
    ws.append(["Generated", datetime.now().isoformat(timespec="seconds")])
    ws.append(["Intent", "Control welding + engine-access service + correct tub reattachment + ordered Ironman Foamcell suspension kit."])
    ws.append([])
    ws.append(
        [
            "phase_id",
            "lane",
            "task",
            "depends_on",
            "inspection_or_measurement",
            "parts_or_materials",
            "decision_gate",
            "completion_signal",
        ]
    )
    style_header_row(ws, 5)

    rows = [
        [
            "TO1",
            "body_structure",
            "Pre-lift baseline capture and tagging",
            "stripdown_cataloguing_complete",
            "Photo and tag every mount point and spacer before separation.",
            "Tagging consumables, marker labels, template sheet",
            "No tub lift until tag-map is complete.",
            "Mount map and reference photos signed off.",
        ],
        [
            "TO2",
            "body_structure",
            "Tub lift and mount-point condition survey",
            "TO1",
            "Record hole ovality, captive-nut condition, and corrosion depth at each point.",
            "Inspection tools, rust-penetrant, borescope as needed",
            "No welding closure without per-point repair decision.",
            "Mount condition matrix completed.",
        ],
        [
            "TO3",
            "body_structure",
            "Welding and closure of mount interfaces",
            "TO2",
            "Confirm mount faces, hole centerlines, and plate thickness restoration.",
            "Repair plates, primer, metal protection",
            "No refit planning until weld closure and anti-corrosion prep are complete.",
            "All mount points dimension-checked and protected.",
        ],
        [
            "TO4",
            "mechanical",
            "Tub-off engine-bay access inspection and service list lock",
            "TO2",
            "Inspect mounts, lines, hoses, clamps, shift linkage/top service items.",
            "Service parts bundle + condition-based items",
            "Buy only confirmed-failed items for condition-based components.",
            "Inspection report with buy/no-buy per line item.",
        ],
        [
            "TO5",
            "steering_brakes_suspension",
            "Suspension install path: ordered Ironman Foamcell kit",
            "TO3",
            "Validate spring arch, shackle angle, pinion/caster behavior after trial load.",
            "Ironman main kit shipment; separate front damper shipment (24635FE x2)",
            "Do not final-torque suspension until both shipments are received, contents-checked, and ride-height/alignment checks pass.",
            "Suspension geometry check signed off.",
        ],
        [
            "TO6",
            "body_weather_seal",
            "Tub reattachment interface prep and trial fit",
            "TO3",
            "Dry trial fit with shim pack and rubber mounts before final bolt-up.",
            "Body mount rubber kit, hardware kit, shim/spacer pack",
            "No permanent tub fastening before successful trial seating.",
            "All attachment points align without forced fit.",
        ],
        [
            "TO7",
            "integration",
            "Final tub reattachment and torque map execution",
            "TO6|TO5|TO4",
            "Follow cross-pattern torque sequence and recheck after settling.",
            "Final hardware and thread treatment",
            "Gate to integration close only after torque recheck and gap alignment.",
            "Tub fixed at all correct points with verified torque log.",
        ],
        [
            "TO8",
            "integration",
            "Post-refit validation",
            "TO7",
            "Road/yard check for shift engagement, vibration, mount settling, and steering feel.",
            "None beyond completed assemblies",
            "Escalate only if disengagement or mount-settle issues remain.",
            "Vehicle moves to reassembly validation lane.",
        ],
    ]
    for row in rows:
        ws.append(row)

    autosize_columns(ws)


def write_report(path: Path) -> None:
    content = """# Tub-Off To Refit Execution Plan

- Keep welding scope separate, but lock interface control now.
- During tub-off, run a focused engine-access inspection and buy condition-based parts only.
- Before tub goes back, complete mount-point mapping, mount repairs, and trial fit using correct rubbers/hardware/shims.
- Suspension path is now fixed to: ordered Ironman Foamcell kit, with front dampers in a separate shipment.

## Key Procurement Adds

- Body-to-chassis mount rubber kit
- Body mount hardware and captive-nut repair provision
- Body mount shim/spacer alignment pack
- Ironman Foamcell suspension kit main shipment
- Ironman Foamcell front damper pair (`24635FE` x2), separate shipment
- Gearbox top-cover service items (condition-based)

## Gates

1. No tub lift without mount-point tag map.
2. No refit plan without weld/dimension closure.
3. No final tub fastening without dry trial fit using rubbers and shim plan.
4. No suspension final torque until geometry/ride-height checks pass.
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Update workbook with tub-off/refit control plan and suspension decision.")
    parser.add_argument("--workbook", type=Path, default=DEFAULT_WORKBOOK_PATH, help="Workbook path to update in-place.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT_PATH, help="Markdown report output path.")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = args.workbook.with_name(f"{args.workbook.stem}.tub_refit_plan_backup_{timestamp}{args.workbook.suffix}")
    shutil.copy2(args.workbook, backup)

    wb = load_workbook(args.workbook)
    update_build_plan(wb)
    update_procurement_pass2(wb)
    update_parts_estimates(wb)
    update_suspension_sheet(wb)
    write_tub_off_refit_plan_sheet(wb)
    wb.save(args.workbook)

    args.report.parent.mkdir(parents=True, exist_ok=True)
    write_report(args.report)

    print(f"Updated workbook: {args.workbook}")
    print(f"Backup saved: {backup}")
    print(f"Report written: {args.report}")


if __name__ == "__main__":
    main()
