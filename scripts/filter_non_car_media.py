from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PHOTOS_DIR = ROOT / "photos"
INVENTORY_PATH = ROOT / "data" / "manual" / "photo_inventory.csv"
REPORT_PATH = ROOT / "data" / "manual" / "photo_non_car_filter_report.csv"
REVIEW_DIR = PHOTOS_DIR / "non_car_review"

CAR_KEYWORDS = {
    "j40",
    "fj40",
    "landcruiser",
    "land_cruiser",
    "toyota",
    "engine",
    "chassis",
    "frame",
    "axle",
    "gearbox",
    "weld",
    "rust",
    "floor",
    "tub",
    "wing",
    "hood",
    "dash",
    "brake",
    "suspension",
    "wiring",
    "radiator",
    "fuel",
    "body",
}

NON_CAR_KEYWORDS = {
    "invoice",
    "salary",
    "payroll",
    "rent",
    "manual",
    "receipt",
    "policy",
    "bank",
    "emergency kit",
    "wetransfer",
    "farmdar",
}


@dataclass(frozen=True)
class Decision:
    keep: bool
    reason: str


def decide(row: dict[str, str]) -> Decision:
    file_name = str(row.get("file_name") or "").lower()
    relative_path = str(row.get("relative_path") or "").lower()
    component_group = str(row.get("component_group") or "")
    stage = str(row.get("stage") or "")
    confidence = str(row.get("confidence") or "")
    observed_state = str(row.get("observed_state") or "")
    tags = str(row.get("tags") or "").lower()

    text = " ".join([file_name, relative_path, tags])
    if any(k in text for k in CAR_KEYWORDS):
        return Decision(True, "keyword_car_match")

    if any(k in text for k in NON_CAR_KEYWORDS):
        return Decision(False, "keyword_non_car_match")

    if component_group != "documentation_reference":
        return Decision(True, "component_group_not_reference")

    if stage != "reference_material":
        return Decision(True, "stage_not_reference_material")

    if observed_state != "reference_only":
        return Decision(True, "observed_state_not_reference_only")

    if confidence in {"high", "medium"}:
        return Decision(True, "reference_but_high_or_medium_confidence")

    return Decision(False, "reference_low_confidence")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Filter probable non-car media into review folder.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Move probable non-car files into photos/non_car_review. Without this, only report is generated.",
    )
    parser.add_argument(
        "--move-low-confidence-reference",
        action="store_true",
        help=(
            "Also move low-confidence reference-only rows. "
            "Default behavior is conservative: keep these files in place and only flag them in the report."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not INVENTORY_PATH.exists():
        raise SystemExit(f"Missing inventory: {INVENTORY_PATH}")

    rows = list(csv.DictReader(INVENTORY_PATH.open(newline="", encoding="utf-8")))
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    report_rows: list[dict[str, str]] = []
    moved = 0
    kept = 0
    flagged = 0

    for row in rows:
        decision = decide(row)
        rel = row.get("relative_path", "")
        src = ROOT / rel if rel else Path("")
        status = "keep"
        target_rel = ""

        if decision.keep:
            kept += 1
        else:
            flagged += 1
            status = "flagged_non_car"
            should_move = True
            if decision.reason == "reference_low_confidence" and not args.move_low_confidence_reference:
                should_move = False

            if args.apply and should_move and src.exists() and src.is_file():
                target = REVIEW_DIR / src.name
                if target.exists():
                    stem = target.stem
                    suffix = target.suffix
                    idx = 2
                    while True:
                        candidate = REVIEW_DIR / f"{stem}_{idx}{suffix}"
                        if not candidate.exists():
                            target = candidate
                            break
                        idx += 1
                src.rename(target)
                target_rel = f"photos/non_car_review/{target.name}"
                status = "moved_to_non_car_review"
                moved += 1

        report_rows.append(
            {
                "file_name": row.get("file_name", ""),
                "relative_path": rel,
                "component_group": row.get("component_group", ""),
                "stage": row.get("stage", ""),
                "confidence": row.get("confidence", ""),
                "decision": status,
                "reason": decision.reason,
                "target_relative_path": target_rel,
            }
        )

    with REPORT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "file_name",
                "relative_path",
                "component_group",
                "stage",
                "confidence",
                "decision",
                "reason",
                "target_relative_path",
            ],
        )
        writer.writeheader()
        writer.writerows(report_rows)

    print(f"Report written: {REPORT_PATH.relative_to(ROOT)}")
    print(f"Kept: {kept}")
    print(f"Flagged non-car: {flagged}")
    if args.apply:
        print(f"Moved to review: {moved}")


if __name__ == "__main__":
    main()
