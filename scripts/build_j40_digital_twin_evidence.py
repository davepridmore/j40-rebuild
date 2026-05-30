#!/usr/bin/env python3
"""Build the evidence matrix that drives the J40 digital-twin model."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
CAD_ROOT = ROOT / "data" / "manual" / "cad" / "j40_reference_model"
REPORT_DIR = CAD_ROOT / "05_reports"
PHOTO_INVENTORY = ROOT / "data" / "manual" / "photo_inventory.csv"
COMPONENT_JOBS = ROOT / "data" / "manual" / "component_jobs.csv"
COMPONENT_JOB_RECON = ROOT / "data" / "manual" / "component_jobs_photo_reconciliation.csv"
MODEL_PARTS = CAD_ROOT / "04_exports" / "scaffold_rev_c" / "j40_full_vehicle_scaffold_rev_c_parts.csv"

EVIDENCE_MATRIX = REPORT_DIR / "j40_digital_twin_evidence_matrix.csv"
MEASUREMENT_BACKLOG = REPORT_DIR / "j40_digital_twin_measurement_backlog.csv"
BUILD_NOTES = REPORT_DIR / "j40_digital_twin_build_notes.md"

MODEL_GROUP_HINTS = {
    "body_exterior": {"body", "front_detail", "hard_top", "chassis"},
    "body_floor": {"body", "chassis", "fuel_system"},
    "body_tub": {"body", "chassis", "hard_top"},
    "brake_system": {"brake_system", "running_gear"},
    "chassis_underside": {"chassis", "running_gear", "brake_system", "fuel_system", "exhaust"},
    "documentation_reference": {"body", "front_detail", "hard_top", "chassis", "running_gear"},
    "electrical_system": {"engine_bay", "interior", "body", "chassis"},
    "engine_bay": {"engine_bay", "brake_system", "fuel_system", "exhaust"},
    "fuel_system": {"fuel_system", "body", "chassis"},
    "interior_cabin": {"interior", "body"},
    "removable_panels": {"body", "front_detail", "hard_top"},
    "roof_and_gutters": {"hard_top", "body"},
    "rubbers_and_seals": {"body", "hard_top", "running_gear"},
    "window_hardware": {"hard_top", "body"},
    "windows": {"hard_top", "body"},
    "wheels_and_tires": {"running_gear", "brake_system"},
}

STOPWORDS = {
    "and",
    "area",
    "baseline",
    "context",
    "detail",
    "details",
    "for",
    "front",
    "left",
    "lower",
    "photo",
    "photos",
    "rear",
    "reference",
    "right",
    "sample",
    "samples",
    "side",
    "the",
    "upper",
    "view",
    "with",
}

MEASUREMENT_TERMS = {
    "aperture",
    "bracket",
    "caliper",
    "channel",
    "crossmember",
    "diameter",
    "firewall",
    "floor",
    "frame",
    "gutter",
    "hinge",
    "hole",
    "mount",
    "panel",
    "rotor",
    "rubber",
    "seal",
    "spring",
    "support",
    "window",
}


@dataclass(frozen=True)
class PartRow:
    group: str
    name: str
    confidence: str
    notes: str


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def tokens(value: str) -> set[str]:
    return {
        token
        for token in re.split(r"[^a-z0-9]+", value.lower())
        if len(token) >= 3 and token not in STOPWORDS
    }


def date_range(rows: list[dict[str, str]]) -> str:
    dates = sorted({row.get("captured_date", "") for row in rows if row.get("captured_date")})
    if not dates:
        return ""
    if dates[0] == dates[-1]:
        return dates[0]
    return f"{dates[0]} to {dates[-1]}"


def stage_counts(rows: list[dict[str, str]]) -> str:
    counts = Counter(row.get("stage", "") for row in rows if row.get("stage"))
    return "|".join(f"{name}:{count}" for name, count in counts.most_common(4))


def example_files(rows: list[dict[str, str]], limit: int = 8) -> str:
    examples: list[str] = []
    for row in rows:
        name = row.get("file_name") or Path(row.get("relative_path", "")).name
        if name and name not in examples:
            examples.append(name)
        if len(examples) >= limit:
            break
    return "|".join(examples)


def model_part_matches(component_group: str, specific_component: str, parts: list[PartRow]) -> list[PartRow]:
    group_hints = MODEL_GROUP_HINTS.get(component_group, set())
    component_tokens = tokens(f"{component_group} {specific_component}")
    scored: list[tuple[int, PartRow]] = []
    for part in parts:
        score = 0
        if part.group in group_hints:
            score += 3
        part_tokens = tokens(f"{part.group} {part.name} {part.notes}")
        overlap = component_tokens & part_tokens
        score += len(overlap) * 2
        if part.group in group_hints and overlap:
            score += 2
        if score >= 4:
            scored.append((score, part))
    scored.sort(key=lambda item: (-item[0], item[1].group, item[1].name))
    return [part for _, part in scored[:12]]


def readiness(rows: list[dict[str, str]], matches: list[PartRow], specific_component: str) -> str:
    if not matches:
        return "photos_only_needs_model_geometry"
    if any("measurement" in row.get("stage", "") for row in rows):
        return "measurement_photo_available_needs_cad_datum"
    if any(part.confidence.startswith(("L0", "L1")) for part in matches):
        return "represented_needs_measurement_refinement"
    if any(term in tokens(specific_component) for term in MEASUREMENT_TERMS):
        return "represented_needs_dimension_check"
    return "visual_reference_modelled"


def backlog_priority(photo_count: int, readiness_value: str) -> str:
    if readiness_value == "photos_only_needs_model_geometry" and photo_count >= 10:
        return "P1"
    if "measurement" in readiness_value or photo_count >= 20:
        return "P1"
    if photo_count >= 5:
        return "P2"
    return "P3"


def load_parts() -> list[PartRow]:
    rows = read_csv(MODEL_PARTS)
    return [
        PartRow(
            group=row.get("group", ""),
            name=row.get("name", ""),
            confidence=row.get("confidence", ""),
            notes=row.get("notes", ""),
        )
        for row in rows
    ]


def job_lookup() -> dict[tuple[str, str], dict[str, str]]:
    jobs = read_csv(COMPONENT_JOBS)
    by_group: dict[str, list[dict[str, str]]] = defaultdict(list)
    for job in jobs:
        by_group[job.get("component_group", "")].append(job)
    lookup: dict[tuple[str, str], dict[str, str]] = {}
    for group, group_jobs in by_group.items():
        for job in group_jobs:
            key = (group, job.get("component_job_id", ""))
            lookup[key] = job
    return lookup


def reconciliation_lookup() -> dict[str, dict[str, str]]:
    return {row.get("component_job_id", ""): row for row in read_csv(COMPONENT_JOB_RECON)}


def build_matrix() -> list[dict[str, str]]:
    photos = read_csv(PHOTO_INVENTORY)
    parts = load_parts()
    jobs = job_lookup()
    recon = reconciliation_lookup()
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in photos:
        if row.get("media_type") not in {"photo", "video"}:
            continue
        grouped[(row.get("component_group", ""), row.get("specific_component", ""))].append(row)

    output_rows: list[dict[str, str]] = []
    for (component_group, specific_component), rows in sorted(grouped.items()):
        matches = model_part_matches(component_group, specific_component, parts)
        matched_confidence = Counter(part.confidence for part in matches)
        readiness_value = readiness(rows, matches, specific_component)
        related_job = jobs.get((component_group, specific_component), {})
        related_recon = recon.get(specific_component, {})
        output_rows.append(
            {
                "component_group": component_group,
                "specific_component": specific_component,
                "photo_count": str(len(rows)),
                "video_count": str(sum(1 for row in rows if row.get("media_type") == "video")),
                "date_range": date_range(rows),
                "stage_counts": stage_counts(rows),
                "example_files": example_files(rows),
                "model_groups": "|".join(sorted({part.group for part in matches})),
                "model_part_count": str(len(matches)),
                "model_part_examples": "|".join(part.name for part in matches[:8]),
                "model_confidence_mix": "|".join(f"{key}:{value}" for key, value in matched_confidence.most_common()),
                "digital_twin_readiness": readiness_value,
                "measurement_priority": backlog_priority(len(rows), readiness_value),
                "job_status": related_job.get("current_status", ""),
                "job_action": related_job.get("planned_action", ""),
                "reconciliation_status": related_recon.get("reconciliation_status", ""),
            }
        )
    return output_rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_notes(matrix_rows: list[dict[str, str]], backlog_rows: list[dict[str, str]]) -> None:
    group_counts = Counter(row["component_group"] for row in matrix_rows)
    readiness_counts = Counter(row["digital_twin_readiness"] for row in matrix_rows)
    photo_total = sum(int(row["photo_count"]) for row in matrix_rows)
    p1_rows = [row for row in backlog_rows if row["measurement_priority"] == "P1"]
    lines = [
        "# J40 Digital Twin Build Notes",
        "",
        f"- Generated: {datetime.now(timezone.utc).isoformat()}",
        f"- Photo/video evidence rows: {len(matrix_rows)} component slices, {photo_total} media references.",
        f"- Current scaffold parts: {sum(1 for _ in read_csv(MODEL_PARTS))}.",
        f"- Evidence matrix: `{EVIDENCE_MATRIX.relative_to(ROOT)}`",
        f"- Measurement backlog: `{MEASUREMENT_BACKLOG.relative_to(ROOT)}`",
        "",
        "## Readiness Summary",
        "",
    ]
    for name, count in readiness_counts.most_common():
        lines.append(f"- `{name}`: {count}")
    lines.extend(["", "## Strongest Photo Coverage", ""])
    for group, count in group_counts.most_common(12):
        media = sum(int(row["photo_count"]) for row in matrix_rows if row["component_group"] == group)
        lines.append(f"- `{group}`: {count} component slices, {media} media items")
    lines.extend(["", "## P1 Measurement Work", ""])
    for row in p1_rows[:18]:
        lines.append(
            "- `{component_group}/{specific_component}`: {photo_count} photos, {digital_twin_readiness}; examples `{example_files}`".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Build Rule",
            "",
            "The model can be a faithful visual digital twin from photos and source references, but exact fabrication geometry requires measured datums. Treat every L0/L1 part as approximate until tied to a tape measure, known Toyota dimension, or calibrated photogrammetry solve.",
            "",
            "Primary datums still needed: wheel/tire size, front disc rotor diameter/thickness, caliper mounting ear spacing, frame rail hole stations, body mount heights, door/roof aperture dimensions, firewall hole diameters, bumper/fog-lamp bracket offsets, and glass/rubber channel profiles.",
        ]
    )
    BUILD_NOTES.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    matrix_rows = build_matrix()
    matrix_fields = [
        "component_group",
        "specific_component",
        "photo_count",
        "video_count",
        "date_range",
        "stage_counts",
        "example_files",
        "model_groups",
        "model_part_count",
        "model_part_examples",
        "model_confidence_mix",
        "digital_twin_readiness",
        "measurement_priority",
        "job_status",
        "job_action",
        "reconciliation_status",
    ]
    write_csv(EVIDENCE_MATRIX, matrix_rows, matrix_fields)
    backlog_rows = [
        row
        for row in matrix_rows
        if row["digital_twin_readiness"] != "visual_reference_modelled"
        and row["component_group"] not in {"documentation_reference", "procurement_inventory"}
    ]
    backlog_rows.sort(key=lambda row: (row["measurement_priority"], -int(row["photo_count"]), row["component_group"], row["specific_component"]))
    write_csv(MEASUREMENT_BACKLOG, backlog_rows, matrix_fields)
    write_notes(matrix_rows, backlog_rows)
    print(f"Wrote {EVIDENCE_MATRIX.relative_to(ROOT)}")
    print(f"Wrote {MEASUREMENT_BACKLOG.relative_to(ROOT)}")
    print(f"Wrote {BUILD_NOTES.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
