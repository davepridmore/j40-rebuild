#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
MANUAL_DIR = ROOT / "data" / "manual"
UI_DIR = ROOT / "docs" / "project-control-ui"

WORKSTREAM_STATUS_PATH = MANUAL_DIR / "workstream_status.csv"
REASSEMBLY_PACKAGES_PATH = MANUAL_DIR / "reassembly_work_packages.csv"
COMPONENT_JOBS_PATH = MANUAL_DIR / "component_jobs.csv"
PHOTO_INVENTORY_PATH = MANUAL_DIR / "photo_inventory.csv"
REPLACEMENT_PIPE_SPECS_PATH = MANUAL_DIR / "replacement_pipe_ordering_specs.csv"
REPLACEMENT_PIPE_ORDER_RELEASE_SPECS_PATH = MANUAL_DIR / "replacement_pipe_order_release_specs.csv"
REPLACEMENT_PIPE_RELEASE_ACTIONS_PATH = MANUAL_DIR / "replacement_pipe_release_actions.csv"
REPLACEMENT_PIPE_CIRCUIT_CLOSURE_PATH = MANUAL_DIR / "replacement_pipe_circuit_closure_sheet.csv"
CHASSIS_RUBBER_REQUIREMENTS_PATH = MANUAL_DIR / "chassis_rubber_requirements.csv"
RUBBER_ORDERING_SPECS_PATH = MANUAL_DIR / "rubber_ordering_specs.csv"
BODY_MOUNT_ORDER_RELEASE_SPECS_PATH = MANUAL_DIR / "body_mount_order_release_specs.csv"
BODY_MOUNT_RELEASE_ACTIONS_PATH = MANUAL_DIR / "body_mount_release_actions.csv"
BODY_MOUNT_STATION_CLOSURE_PATH = MANUAL_DIR / "body_mount_station_closure_sheet.csv"
BRAKE_SYSTEM_REQUIREMENTS_PATH = MANUAL_DIR / "brake_system_requirements.csv"
EXPENSES_PATH = MANUAL_DIR / "expenses.csv"
BUY_NOW_PATH = MANUAL_DIR / "parts_buy_now_this_week.csv"
WORKBOOK_TOOLS_PATH = MANUAL_DIR / "workbook_tabs" / "tools.csv"
WORKBOOK_PARTS_PATH = MANUAL_DIR / "workbook_tabs" / "parts.csv"
WORKBOOK_SUBSTANCES_PATH = MANUAL_DIR / "workbook_tabs" / "substances.csv"
WORKBOOK_ELECTRICAL_MASTER_PATH = MANUAL_DIR / "workbook_tabs" / "electrical_master.csv"
WORKBOOK_ELECTRICAL_TEMPLATES_PATH = MANUAL_DIR / "workbook_tabs" / "electrical_templates.csv"
SELLING_SITE_MANIFEST_PATH = ROOT / "deliverables" / "selling_site_images" / "manifest.csv"
WHATSAPP_J40_CHAT_CANDIDATES_PATH = MANUAL_DIR / "whatsapp_j40_chat_candidates.csv"
WHATSAPP_J40_MEDIA_INDEX_PATH = ROOT / "data" / "processed" / "generated" / "mcp_whatsapp_j40_media_index.csv"
PAINT_REFINISH_MEDIA_QUEUE_PATH = MANUAL_DIR / "paint_refinish_media_queue.csv"
PAINT_REFINISH_WHATSAPP_MEDIA_QUEUE_PATH = MANUAL_DIR / "paint_refinish_whatsapp_media_queue.csv"
INVENTORY_IMAGE_OVERRIDES_PATH = MANUAL_DIR / "inventory_image_overrides.csv"
OUTPUT_DATA_JS_PATH = UI_DIR / "data.js"
LOCAL_ORDER_IMAGE_DIRS: tuple[Path, ...] = (
    ROOT / "photos",
    ROOT / "deliverables" / "selling_site_images" / "images",
)
LOCAL_ORDER_IMAGE_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png", ".webp"}
LOCAL_ORDER_IMAGE_INDEX: dict[str, Path] | None = None

PRIMARY_WORKSTREAM_IDS: tuple[str, ...] = (
    "stripdown_cataloguing",
    "body_chassis",
    "paint_refinish",
    "chassis_fixing",
    "chassis_rubbers",
    "interior_controls",
    "electrical_reset",
    "mechanical_baseline",
    "replacement_pipes",
    "brake_system",
    "eps_vitz_upgrade",
    "suspension_upgrade",
    "interior_weatherproofing",
    "final_assembly_validation",
)

WORKSTREAM_TITLE_OVERRIDES: dict[str, str] = {
    "brake_system": "Brakes",
    "chassis_rubbers": "Chassis Rubbers",
    "interior_controls": "Dashboard",
    "interior_weatherproofing": "Interior",
    "paint_refinish": "Paint",
    "replacement_pipes": "Replacement Pipes",
    "eps_vitz_upgrade": "Steering (EPS)",
    "suspension_upgrade": "Suspension",
}

WORKSTREAM_IMAGE_PROFILES: dict[str, dict[str, set[str]]] = {
    "stripdown_cataloguing": {
        "component_groups": {"removable_panels", "interior_cabin", "engine_bay", "body_exterior", "body_floor"},
        "stages": {"stripdown_cataloguing"},
        "keywords": {"stripdown", "removed", "panel", "interior", "tagged", "dashboard", "cabin", "door"},
    },
    "body_chassis": {
        "component_groups": {"body_floor", "body_exterior", "roof_and_gutters", "removable_panels"},
        "stages": {"rust_assessment"},
        "keywords": {"rust", "floor", "body", "wing", "lift", "gutter", "cargo", "seam"},
    },
    "paint_refinish": {
        "component_groups": {"removable_panels", "body_exterior", "roof_and_gutters", "documentation_reference"},
        "stages": {"removed_parts_cataloguing", "hardware_refinish", "stripdown_cataloguing", "reference_material"},
        "keywords": {"paint", "primer", "panel", "door", "wing", "refinish", "sanding", "send", "return", "bodywork"},
    },
    "interior_controls": {
        "component_groups": {"interior_cabin", "electrical_system", "body_floor"},
        "stages": {"electrical_rework", "rust_assessment", "stripdown_cataloguing"},
        "keywords": {"interior", "dash", "switch", "knob", "button", "control", "panel", "cabin"},
    },
    "chassis_fixing": {
        "component_groups": {"chassis_underside"},
        "stages": {"underside_inspection", "chassis_fixing"},
        "keywords": {"frame", "crossmember", "chassis", "mount", "steering", "bracket", "line", "hanger"},
    },
    "chassis_rubbers": {
        "component_groups": {"chassis_underside", "body_floor", "procurement_inventory"},
        "stages": {"underside_inspection", "rust_assessment", "procurement_reconciliation"},
        "keywords": {"body_mount", "rubber", "shim", "sleeve", "isolator"},
    },
    "electrical_reset": {
        "component_groups": {"electrical_system", "procurement_inventory"},
        "stages": {"electrical_rework", "procurement_reconciliation"},
        "keywords": {
            "wiring",
            "fuse",
            "relay",
            "harness",
            "firewall",
            "connector",
            "footwell",
            "ground",
            "switch",
            "grommet",
            "loom",
            "distribution",
            "power",
        },
    },
    "mechanical_baseline": {
        "component_groups": {"engine_bay", "chassis_underside"},
        "stages": {"baseline_walkaround", "underside_inspection", "mechanical_inspection", "mechanical_cleaning"},
        "keywords": {"engine", "service", "cooling", "maintenance", "hose", "bay", "mechanical"},
    },
    "replacement_pipes": {
        "component_groups": {"engine_bay", "chassis_underside"},
        "stages": {
            "mechanical_baseline",
            "mechanical_inspection",
            "mechanical_cleaning",
            "underside_inspection",
        },
        "keywords": {
            "pipe",
            "hose",
            "tube",
            "cooling",
            "radiator_hose",
            "metal_pipe",
            "fuel",
            "brake",
            "clutch",
            "vacuum",
            "breather",
            "hard_line",
            "hard_lines",
            "made_to_order",
            "measurement",
        },
    },
    "brake_system": {
        "component_groups": {"chassis_underside", "procurement_inventory"},
        "stages": {"underside_inspection", "procurement_reconciliation"},
        "keywords": {"brake", "disc", "drum", "caliper", "hydraulic", "master", "cylinder", "hose", "line", "bias"},
    },
    "eps_vitz_upgrade": {
        "component_groups": {"chassis_underside"},
        "stages": {"underside_inspection"},
        "keywords": {"eps", "vitz", "steering", "column", "motor", "ecu", "assist", "u-joint", "adapter", "mount"},
    },
    "suspension_upgrade": {
        "component_groups": {"chassis_underside", "procurement_inventory"},
        "stages": {"underside_inspection", "procurement_reconciliation"},
        "keywords": {"suspension", "ome", "leaf", "shackle", "shock", "bush", "damper", "ride", "alignment", "spring"},
    },
    "interior_weatherproofing": {
        "component_groups": {"interior_cabin", "body_floor", "roof_and_gutters"},
        "stages": {"rust_assessment"},
        "keywords": {"firewall", "interior", "sealing", "cabin", "gutter", "weatherproof"},
    },
    "final_assembly_validation": {
        "component_groups": {"body_exterior", "interior_cabin", "engine_bay", "chassis_underside"},
        "stages": {"baseline_walkaround"},
        "keywords": {"overview", "validation", "cabin", "engine", "frame", "wiring"},
    },
}

WORKSTREAM_MIN_IMAGE_SCORE: dict[str, int] = {
    "interior_controls": 24,
    "electrical_reset": 22,
    "chassis_fixing": 20,
    "chassis_rubbers": 18,
    "body_chassis": 18,
    "paint_refinish": 18,
    "mechanical_baseline": 18,
    "replacement_pipes": 18,
    "brake_system": 18,
    "eps_vitz_upgrade": 18,
    "suspension_upgrade": 18,
    "interior_weatherproofing": 18,
    "stripdown_cataloguing": 16,
    "final_assembly_validation": 16,
}

DEFAULT_WORKSTREAM_MIN_IMAGE_SCORE = 18
WORKSTREAM_MIN_KEYWORD_HITS: dict[str, int] = {
    "stripdown_cataloguing": 1,
    "body_chassis": 1,
    "paint_refinish": 1,
    "chassis_fixing": 2,
    "chassis_rubbers": 1,
    "electrical_reset": 1,
    "mechanical_baseline": 2,
    "replacement_pipes": 1,
    "brake_system": 2,
    "eps_vitz_upgrade": 2,
    "suspension_upgrade": 2,
    "interior_weatherproofing": 2,
    "final_assembly_validation": 0,
}
DEFAULT_WORKSTREAM_MIN_KEYWORD_HITS = 1
WORKSTREAM_ALLOW_STAGE_COMPONENT_FALLBACK: dict[str, bool] = {
    "stripdown_cataloguing": True,
    "body_chassis": True,
    "chassis_fixing": True,
    "chassis_rubbers": False,
    "electrical_reset": True,
    "mechanical_baseline": True,
    "replacement_pipes": True,
    "brake_system": False,
    "eps_vitz_upgrade": False,
    "suspension_upgrade": False,
    "interior_weatherproofing": False,
    "final_assembly_validation": True,
}
WORKBOOK_SECTION_HEADING_RE = re.compile(r"^\d+\)\s+")

REPLACEMENT_PIPE_MADE_TO_ORDER_MEDIA_IDS: tuple[str, ...] = (
    "20260502_004044_gp_Hx4Yo0Qg",
    "20260502_004106_gp_wlYlUahA",
    "20260502_004120_gp_7Jw9Zyrg",
    "20260502_004133_gp_ZEpqmARA",
    "20260502_004139_gp_jt1dGw4A",
    "20260502_004145_gp_e8soxsyA",
)
REPLACEMENT_PIPE_INSTALLED_LOCATION_MEDIA_IDS: tuple[str, ...] = (
    "20260430_220004_gp_C9oYiYmA",
    "20260430_215957_gp_2iBbUagw",
    "20260422_004306_gp_vGlNr2UA",
    "20260422_004311_gp_994KQ0Pw",
    "20260430_215939_gp_EjZ7u1ow",
)
REPLACEMENT_PIPE_SAMPLE_SORTING_MEDIA_IDS: tuple[str, ...] = (
    "20260502_005740_gp_Qiat03EQ",
)
REPLACEMENT_PIPE_CURATED_MEDIA_IDS: tuple[str, ...] = (
    *REPLACEMENT_PIPE_MADE_TO_ORDER_MEDIA_IDS,
    *REPLACEMENT_PIPE_INSTALLED_LOCATION_MEDIA_IDS,
    *REPLACEMENT_PIPE_SAMPLE_SORTING_MEDIA_IDS,
)
REAR_BRAKE_CABLE_LINE_MEDIA_IDS: tuple[str, ...] = (
    "20260501_194305_gp_EllBGvXA",
    "20260501_194313_gp_lfUqLibA",
    "20260501_194322_gp_XuRtjN4w",
    "20260324_004852",
    "20260324_004906",
    "20260324_004918",
    "20260324_004921_gp_bHLJcrEw",
    "20260422_004254_gp_SplHLSYA",
    "20260422_004257_gp_cxEZbZoQ",
    "20260422_004301_gp_SU89hisw",
)
DASHBOARD_ELECTRICAL_FOCUS_KEYWORDS: tuple[str, ...] = (
    "switch",
    "dash",
    "fuel stop",
    "ignition",
    "security",
    "selector",
    "panel",
)

DEFAULT_IMAGE_PROFILE = {
    "component_groups": {"body_exterior", "interior_cabin", "engine_bay", "body_floor", "chassis_underside"},
    "stages": {"baseline_walkaround", "stripdown_cataloguing", "underside_inspection", "rust_assessment"},
    "keywords": {"overview", "body", "engine", "frame", "floor"},
}

REFERENCE_IGNORE_PREFIXES: tuple[str, ...] = (
    "whatsapp_",
    "user_",
    "docs_",
    "repo_control",
    "photo_inventory",
    "annotated_issues_",
)

WORKSTREAM_REQUIRED_SEQUENCE: dict[str, list[tuple[str, str]]] = {
    "stripdown_cataloguing": [
        ("Tag and label every removed part", "Each removed component needs a unique label and matching photo before storage."),
        ("Record storage location per part group", "Update where each part is physically stored so reassembly can find it quickly."),
        ("Track outbound vendor jobs", "Any part sent out for refurbish/service must have vendor, date, and return status recorded."),
        ("Reconcile orphan items", "Close unmatched loose items by linking each one to a component job row."),
    ],
    "body_chassis": [
        ("Map and freeze weld boundaries", "Mark cut/fabrication boundaries per rust zone before any irreversible cuts."),
        ("Execute cut, fit, and weld sequence", "Run controlled welding with heat management and pinhole checks."),
        ("Close corrosion stack same window", "Apply primer, seam sealer, and top protection immediately after metal closure."),
        ("Capture refit interface evidence", "Photograph mount points and repaired zones before moving to refit."),
    ],
    "paint_refinish": [
        ("Lock outbound panel manifest", "Every panel/hardware piece sent to paint should be tagged with condition photos and vendor batch details."),
        ("Capture in-process painter evidence", "Keep videos/photos of sanding, prep, primer, and in-shop bodywork linked to each batch."),
        ("Reconcile returned painted parts", "Mark what has returned, where it is stored, and whether finish quality is acceptable."),
        ("Close paint quality gate", "Only close the track when all planned parts are returned and signed off for refit."),
    ],
    "interior_controls": [
        ("Classify and tag interior control hardware", "All dash switches, knobs, and control items should be tagged and catalogued."),
        ("Define switch function map", "Each control needs a confirmed function, label text, and circuit assignment."),
        ("Complete dash-fit and mounting checks", "Confirm hole sizes, clearances, and mechanical fit before final mounting."),
        ("Close wiring integration and test", "Wire each control into the final harness plan and verify operation."),
    ],
    "chassis_fixing": [
        ("Run mechanical cleanup sequence", "Wire cup non-flat geometry first, then strip/flap cleanup on flatter sections."),
        ("Complete structured defect checks", "Inspect rails, crossmembers, mounts, and brackets for cracks, pits, and thinning."),
        ("Close issue-specific inspections", "All opened chassis issue rows need photo evidence and explicit closeout."),
        ("Apply final protection stack", "Prime and protect approved metal only after defect closure and surface prep."),
    ],
    "chassis_rubbers": [
        ("Capture and label all removed mount samples", "Tag each old rubber, sleeve, washer, and shim position before replacement decisions."),
        ("Freeze rubber + sleeve + shim specification", "Define dimensions/material/hardness and exact quantity per mount position."),
        ("Lock sourcing path", "Decide local fabrication vs purchased kit and avoid duplicate/partial orders."),
        ("Complete dry-fit interface check", "Trial-fit the tub mount stack before final body fastening."),
    ],
    "electrical_reset": [
        ("Freeze baseline circuit scope", "Confirm exact baseline circuits before optional accessories are added."),
        ("Verify grounds and pass-throughs", "Clean earth points and confirm firewall passes are protected and grommeted."),
        ("Run fuse/relay function checks", "Validate start, charge, lights, horn, and wiper baseline behavior."),
        ("Close loom routing and labeling", "Finalize harness protection, routing clamps, and identification labels."),
    ],
    "mechanical_baseline": [
        ("Execute must-replace service pack", "Complete fluids, filters, ignition and cooling consumables on stripped access."),
        ("Run leak and condition checks", "Check cooling, fuel, vacuum, and visible engine leak points before refit."),
        ("Log post-service defects", "Record any unresolved mechanical issues for gated follow-up."),
        ("Close baseline gate before upgrades", "Do not start optional upgrades until baseline reliability is signed off."),
    ],
    "replacement_pipes": [
        ("Lock the replacement locations", "Keep only vehicle places where pipes, hoses, or hard lines will be replaced; exclude body rubbers and generic context photos."),
        ("Attach direct pipe photos", "Use curated pipe/location photos only, and mark missing close-ups explicitly for the next photo pass."),
        ("Fill recreation specs", "Use replacement_pipe_order_release_specs.csv for exact order lines, then record OD/ID, barb or flare style, route length, bend/template needs, material, and source reference before release."),
        ("Close circuit release holds", "Complete replacement_pipe_release_actions.csv and replacement_pipe_circuit_closure_sheet.csv before buying or fabricating held pipe lines."),
        ("Dry-fit and pressure-test replacements", "Confirm routing, clearance, clip support, and leak-free operation before closing the pipe replacement track."),
    ],
    "brake_system": [
        ("Confirm installed brake architecture", "Verify front/rear hardware family and capture evidence before ordering."),
        ("Close hydraulic refresh scope", "Freeze hoses, cylinders, and fluid-service items from condition evidence."),
        ("Lock brake-bias safety path", "Record baseline bias behavior and approved correction path if needed."),
        ("Close brake safety gate", "Do not progress to final validation until brake function is verified."),
    ],
    "eps_vitz_upgrade": [
        ("Capture donor EPS hardware baseline", "Record donor Vitz EPS unit dimensions, spline details, and connector/pinout references."),
        ("Freeze mount and shaft adapter geometry", "Confirm bracket positions, shaft phasing, and firewall/interior clearance before fabrication."),
        ("Lock EPS electrical integration strategy", "Define power feed, fuse/relay protection, ignition trigger, and fail-safe fallback behavior."),
        ("Run assist validation and safety checks", "Verify smooth steering assist across full lock, bump travel, and road-test conditions."),
    ],
    "suspension_upgrade": [
        ("Capture measured suspension baseline", "Record ride height, shackle angles, and current travel/clearance before parts lock."),
        ("Lock complete upgrade kit", "Freeze springs, shocks, bushes, shackles, and hardware as one coherent package."),
        ("Execute install with loaded-torque procedure", "Install and torque pivot hardware at loaded ride height to avoid premature bushing failure."),
        ("Close alignment and road-validation gate", "Complete alignment and road checks, then log residual tuning items before signoff."),
    ],
    "interior_weatherproofing": [
        ("Confirm floor and shell are dry and sealed", "No finish materials should be installed over unsealed or damp metal."),
        ("Apply weatherproofing layer order", "Run sealing and lining in the correct sequence for moisture control."),
        ("Install dampening and trim stack", "Only proceed with foam/carpet after sealing cure and inspection."),
        ("Close cabin weatherproof gate", "Document finished cabin condition before final assembly."),
    ],
    "final_assembly_validation": [
        ("Build full punch-list", "Compile open defects and remaining integration tasks before refit."),
        ("Run controlled reassembly", "Reassemble in dependency order with torque/spec checks."),
        ("Execute full functional checks", "Validate electrical, mechanical, and chassis functions end-to-end."),
        ("Close road-validation gate", "Road-check and log residual defects before declaring baseline complete."),
    ],
}

WORKSTREAM_SUBTASK_GUIDES: dict[str, dict[str, Any]] = {
    "stripdown_cataloguing": {
        "title": "Stripdown Control",
        "summary": "Part removal, tagging, storage, and vendor movement controls for the stripped vehicle.",
        "default_tools": [
            "Phone/camera with battery charged",
            "Permanent marker or label printer",
            "Socket/spanner set and trim tools",
            "Small trays for fasteners",
        ],
        "default_supplies": [
            "Masking labels or tie-on tags",
            "Zip bags in multiple sizes",
            "Cable ties",
            "Light oil or rust inhibitor for stored bare metal",
        ],
        "subtasks": [
            {
                "title": "Tag And Photograph Every Removed Part",
                "priority": "P0",
                "remaining": "active until stripdown closes",
                "instruction": "Every part comes off with a photo, label, and fastener bag before it leaves the vehicle area.",
                "process_steps": [
                    "Photograph the part installed from enough angles to show side, orientation, hardware, and routing.",
                    "Remove one component group at a time; do not mix unrelated fasteners in the same tray.",
                    "Create a label using workstream, component name, side, and sequence number.",
                    "Bag fasteners with the part label and note any broken, missing, or non-original hardware.",
                    "Take a final photo of the part, label, and fastener bag together before storage.",
                ],
                "tools": ["Camera", "Permanent marker", "Socket/spanner set", "Trim tools"],
                "supplies": ["Tie-on tags", "Zip bags", "Masking tape", "Cable ties"],
                "hold_point": "No removed part is allowed into storage without a visible label and matching photo.",
                "image_tokens": ["stripdown", "removed", "door", "panel", "dashboard", "cabin"],
            },
            {
                "title": "Record Storage Location",
                "priority": "P0",
                "remaining": "all loose items",
                "instruction": "Make storage searchable by component group before more parts come off.",
                "process_steps": [
                    "Group parts by workstream and physical location: shelf, crate, tray, or vendor box.",
                    "Write the storage location on the label and in the dashboard/source tracker.",
                    "Photograph each filled crate or shelf face with labels visible.",
                    "Separate reusable hardware, replacement-needed hardware, and unknown items.",
                    "Move fragile trim, glass, and electrical items away from welding/grinding dust.",
                ],
                "tools": ["Camera", "Marker", "Storage bins", "Parts trays"],
                "supplies": ["Storage labels", "Zip bags", "Bubble wrap or cloth wrap", "Desiccant where useful"],
                "hold_point": "A mechanic should be able to find each item from the dashboard entry alone.",
                "image_tokens": ["storage", "cataloguing", "removed", "parts"],
            },
            {
                "title": "Track Outbound Vendor Jobs",
                "priority": "P1",
                "remaining": "all painter/refurbisher/vendor items",
                "instruction": "Anything leaving the workspace needs a manifest, condition photo, vendor, and return gate.",
                "process_steps": [
                    "Lay out the outbound batch and photograph every item before packing.",
                    "Record vendor name, date sent, expected return, and agreed work.",
                    "Mark each item with a temporary ID that survives handling.",
                    "On return, photograph condition before storage and compare against the outbound manifest.",
                    "Record defects immediately, while vendor correction is still possible.",
                ],
                "tools": ["Camera", "Manifest/checklist", "Marker", "Measuring tape where fit is relevant"],
                "supplies": ["Tags", "Packing wrap", "Tape", "Vendor job sheet"],
                "hold_point": "Close only after returned condition and storage location are recorded.",
                "image_tokens": ["sent", "returned", "painter", "vendor", "refinish"],
            },
            {
                "title": "Reconcile Orphan Items",
                "priority": "P1",
                "remaining": "until no unknown loose items remain",
                "instruction": "Unknown parts must be identified or explicitly quarantined before final assembly.",
                "process_steps": [
                    "Collect all unlabelled items into one quarantine tray.",
                    "Photograph each item with scale and any markings visible.",
                    "Compare against removed-area photos and component jobs.",
                    "Assign the item to a workstream, storage location, or discard decision.",
                    "Update the tracker and mark any missing counterpart items.",
                ],
                "tools": ["Camera", "Calipers", "Magnet", "Reference photo set"],
                "supplies": ["Quarantine tray", "Labels", "Zip bags"],
                "hold_point": "Final assembly cannot begin with unknown structural, brake, steering, or electrical hardware loose.",
                "image_tokens": ["orphan", "unknown", "hardware", "fastener", "cataloguing"],
            },
        ],
    },
    "body_chassis": {
        "title": "Body And Welding Closure",
        "summary": "Body-off rust repair, fabrication, weld closure, and immediate corrosion protection.",
        "default_tools": [
            "MIG welder and welding PPE",
            "Angle grinder with cutting, grinding, and flap discs",
            "Clamps, magnets, and straight edge",
            "Body hammer/dolly set",
        ],
        "default_supplies": [
            "Sheet steel matched to repaired panel thickness",
            "Weld-through primer where joint design requires it",
            "2K epoxy primer system",
            "Seam sealer and cavity wax",
        ],
        "subtasks": [
            {
                "title": "Map And Freeze Weld Boundaries",
                "priority": "P0",
                "remaining": "all active rust zones",
                "instruction": "Mark repair limits before cutting so structural interfaces and refit points stay controlled.",
                "process_steps": [
                    "Clean the zone enough to see spot welds, seam edges, and the true corrosion boundary.",
                    "Probe suspect areas and mark cut lines outside weak metal, not through it.",
                    "Photograph the marked boundary before cutting.",
                    "Record mount points, brackets, holes, and edges that must not move.",
                    "Confirm repair order so adjacent panels are not weakened at the same time.",
                ],
                "tools": ["Inspection light", "Pick/probe", "Marker", "Straight edge", "Camera"],
                "supplies": ["Masking tape", "Panel markers", "Rust reference photos"],
                "hold_point": "No cut is made until the photo-marked boundary and refit interfaces are recorded.",
                "image_tokens": ["floor", "rust", "gutter", "body", "weld", "cut"],
            },
            {
                "title": "Cut, Fit, And Weld",
                "priority": "P0",
                "remaining": "zone by zone",
                "instruction": "Remove weak metal, fit repair pieces tightly, and weld with heat control.",
                "process_steps": [
                    "Cut only the approved zone and deburr the edge.",
                    "Template the patch, transfer to steel, and test fit with an even gap suitable for welding.",
                    "Prepare mating faces and apply weld-through primer only where it belongs inside a lap or closed joint.",
                    "Tack across the patch, skip around to control heat, then close the welds gradually.",
                    "Grind only enough to inspect the weld; do not thin surrounding metal.",
                    "Check pinholes with light/air and rework before primer.",
                ],
                "tools": ["Cut-off wheel", "MIG welder", "Welding clamps", "Hammer/dolly", "Flap disc"],
                "supplies": ["Sheet steel", "Welding wire", "Shielding gas", "Weld-through primer", "Grinding discs"],
                "hold_point": "Patch is fully welded, pinhole checked, and photographed before coating.",
                "image_tokens": ["floor", "body", "panel", "welding", "rust"],
            },
            {
                "title": "Close Corrosion Stack Same Window",
                "priority": "P0",
                "remaining": "after each welded zone",
                "instruction": "Do not leave newly repaired metal unprotected after welding and cleaning.",
                "process_steps": [
                    "Remove weld dust, loose scale, and surface contamination.",
                    "Use wax and grease remover after the panel is dry and cool.",
                    "Apply compatible 2K epoxy primer to bare approved metal.",
                    "Apply seam sealer after primer where the product system requires it.",
                    "Apply topcoat, liner, or cavity wax in the planned order after cure windows are met.",
                ],
                "tools": ["Blow gun", "Solvent-safe wipes", "Primer gun or aerosol system", "Seam-sealer gun"],
                "supplies": ["Wax and grease remover", "2K epoxy primer", "Seam sealer", "Topcoat or bedliner", "Cavity wax"],
                "hold_point": "No moisture, uncured converter, loose rust, or sanding dust is trapped under primer.",
                "image_tokens": ["primer", "sealer", "floor", "rust", "bodywork"],
            },
            {
                "title": "Capture Refit Interface Evidence",
                "priority": "P1",
                "remaining": "before tub refit",
                "instruction": "Prove that body mounts, holes, and panel interfaces are ready before the tub goes back on.",
                "process_steps": [
                    "Photograph repaired mount pads, captive nuts, and body-to-chassis interfaces.",
                    "Test threads and chase only where necessary.",
                    "Trial-fit critical bolts, sleeves, and brackets before paint hides access.",
                    "Measure shim needs and record any non-standard correction.",
                    "Update open issues for any interface that does not align cleanly.",
                ],
                "tools": ["Thread chasers/taps", "Calipers", "Torque wrench for trial checks", "Camera"],
                "supplies": ["Body mount hardware kit", "Anti-seize", "Temporary bolts", "Labels"],
                "hold_point": "The body can be lowered without discovering hidden thread, alignment, or missing-hardware problems.",
                "image_tokens": ["body_mount", "mount", "floor", "chassis", "refit"],
            },
        ],
    },
    "paint_refinish": {
        "title": "Paint And Refinish Control",
        "summary": "Panel send-out, in-process paint evidence, returned-parts reconciliation, and finish quality signoff.",
        "default_tools": ["Camera", "Paint quality checklist", "Panel tags", "Inspection light"],
        "default_supplies": ["Panel labels", "Masking tape", "Protective wrap", "Clean storage blankets"],
        "subtasks": [
            {
                "title": "Lock Outbound Panel Manifest",
                "priority": "P0",
                "remaining": "every painter batch",
                "instruction": "Every panel or hardware item sent to paint must be listed and photographed before handoff.",
                "process_steps": [
                    "Lay out the batch and photograph front, back, edges, existing damage, and label.",
                    "Record item name, side, current condition, required finish, and vendor batch.",
                    "Tag small hardware separately so it does not disappear in the paint shop.",
                    "Agree which dents, rust, holes, and filler areas the painter owns.",
                    "Keep a copy of the manifest with the vehicle records.",
                ],
                "tools": ["Camera", "Checklist", "Marker", "Inspection light"],
                "supplies": ["Tags", "Masking tape", "Packing wrap", "Vendor manifest sheet"],
                "hold_point": "No item leaves without a dashboard-visible before photo and batch entry.",
                "image_tokens": ["sent", "panel", "door", "wing", "paint", "painter"],
            },
            {
                "title": "Capture In-Process Painter Evidence",
                "priority": "P1",
                "remaining": "until primer/prep is verified",
                "instruction": "Track sanding, filler, primer, and correction work while the parts are still at the painter.",
                "process_steps": [
                    "Request photos or videos after stripping/sanding before filler hides defects.",
                    "Confirm rust, pinholes, and previous repairs are corrected before primer.",
                    "Capture primer stage and guide-coat/sanding progress where available.",
                    "Record any scope changes immediately with the affected item ID.",
                    "Keep progress media linked to the same outbound batch.",
                ],
                "tools": ["Phone/camera", "Paint defect checklist", "Shared media folder"],
                "supplies": ["Painter-approved primer/filler system", "Guide coat", "Masking materials"],
                "hold_point": "Primer/topcoat signoff waits until visible prep defects are either fixed or explicitly accepted.",
                "image_tokens": ["progress", "primer", "paint", "sanding", "filler", "painter"],
            },
            {
                "title": "Reconcile Returned Painted Parts",
                "priority": "P0",
                "remaining": "each returned batch",
                "instruction": "Return intake must catch missing items, paint defects, and storage risks immediately.",
                "process_steps": [
                    "Compare returned items against the outbound manifest before the vendor leaves.",
                    "Inspect edges, holes, hinge areas, fastener holes, and undersides.",
                    "Photograph any runs, chips, dry spray, poor coverage, or missed repairs.",
                    "Tag the returned item and move it to protected storage.",
                    "Update return status and open correction rows for defects.",
                ],
                "tools": ["Inspection light", "Camera", "Manifest", "Clean gloves"],
                "supplies": ["Soft wrap", "Foam/cardboard separators", "Labels", "Touch-up defect tags"],
                "hold_point": "No returned part is stacked or stored bare against another painted surface.",
                "image_tokens": ["returned", "painted", "refinished", "hinge", "bracket", "trim"],
            },
            {
                "title": "Close Paint Quality Gate",
                "priority": "P1",
                "remaining": "before refit",
                "instruction": "Finish quality must be accepted before painted parts go back onto the vehicle.",
                "process_steps": [
                    "Confirm all paint-scope items are returned or explicitly deferred.",
                    "Check visible face, hidden face, edges, and mounting points.",
                    "Confirm bolt holes are not clogged with paint where hardware must seat.",
                    "Record touch-up or correction needs before assembly damage can confuse responsibility.",
                    "Approve storage and refit readiness in the dashboard.",
                ],
                "tools": ["Inspection light", "Thread picks", "Camera", "Checklist"],
                "supplies": ["Touch-up plan", "Protective tape for refit edges", "Clean gloves"],
                "hold_point": "Refit starts only after finish defects and missing items are closed or accepted.",
                "image_tokens": ["returned", "quality", "paint", "refinish", "panel"],
            },
        ],
    },
    "interior_controls": {
        "title": "Dashboard And Controls",
        "summary": "Dash switch cataloguing, function assignment, fit-up, and electrical integration.",
        "default_tools": ["Multimeter", "Continuity tester", "Crimper", "Step drill", "Calipers"],
        "default_supplies": ["Heat shrink", "Terminals", "Loom tape", "Labels", "Grommets"],
        "subtasks": [
            {
                "title": "Classify And Tag Control Hardware",
                "priority": "P0",
                "remaining": "all dash controls",
                "instruction": "Identify each switch, knob, warning lamp, and control before drilling or wiring.",
                "process_steps": [
                    "Lay out all dashboard/control hardware and photograph labels, pins, and mounting hardware.",
                    "Assign each item a control ID and intended function.",
                    "Record hole diameter, mounting depth, connector type, and current condition.",
                    "Separate confirmed controls from unknown, duplicate, or optional controls.",
                    "Bag each control with its nut, bezel, and connector parts.",
                ],
                "tools": ["Camera", "Calipers", "Multimeter", "Marker"],
                "supplies": ["Labels", "Zip bags", "Contact cleaner", "Small parts tray"],
                "hold_point": "No dashboard holes or wiring branches are finalized for unknown controls.",
                "image_tokens": ["switch", "control", "dashboard", "button", "knob"],
            },
            {
                "title": "Define Switch Function Map",
                "priority": "P0",
                "remaining": "before harness build",
                "instruction": "Lock what each control does and which circuit it belongs to.",
                "process_steps": [
                    "List each required function: ignition, lights, hazards, wipers, heater, fuel stop/security, and accessories.",
                    "Assign one physical control to each function and mark optional controls as deferred.",
                    "Confirm switch rating, pinout, illumination behavior, and fuse/relay need.",
                    "Update the wiring tracker with wire size, fuse value source, and connector plan.",
                    "Label the control and matching loom branch with the same ID.",
                ],
                "tools": ["Multimeter", "Power supply/test battery with fuse", "Wiring tracker"],
                "supplies": ["Labels", "Heat shrink ID sleeves", "Fuses/relays as planned", "Connector housings"],
                "hold_point": "A circuit cannot be wired until its switch function, protection, and connector are defined.",
                "image_tokens": ["switch", "wiring", "dash", "control", "connector"],
            },
            {
                "title": "Complete Dash Fit And Mounting Checks",
                "priority": "P1",
                "remaining": "before fascia closeout",
                "instruction": "Check physical fit before paint, trim, or wiring makes rework expensive.",
                "process_steps": [
                    "Mock the switch/control layout in the actual dash panel or template.",
                    "Check rear clearance for wiring, nuts, heater ducts, column, and glovebox/trim.",
                    "Drill or file holes only after layout is approved.",
                    "Deburr, prime exposed metal edges, and fit grommets or edge protection where needed.",
                    "Install controls finger-tight and photograph final allocation.",
                ],
                "tools": ["Step drill", "Files", "Deburring tool", "Calipers", "Inspection mirror"],
                "supplies": ["Edge primer", "Grommets", "Control nuts/washers", "Protective tape"],
                "hold_point": "Controls mount without forcing, twisting wiring, or fouling the dash structure.",
                "image_tokens": ["dashboard", "fascia", "switch", "control", "fit"],
            },
            {
                "title": "Wire, Label, And Function Test",
                "priority": "P0",
                "remaining": "after harness branch build",
                "instruction": "Integrate controls into protected, labelled circuits and test before closeout.",
                "process_steps": [
                    "Build each branch with strain relief, heat shrink, and service loop.",
                    "Crimp with the correct die and tug-test each terminal.",
                    "Route wiring away from sharp edges, heater movement, pedals, and column movement.",
                    "Test continuity, switch function, fuse behavior, and relay operation.",
                    "Photograph final routing and label positions before trim covers them.",
                ],
                "tools": ["Ratchet crimper", "Heat gun", "Multimeter", "Test lamp", "Fuse-protected test lead"],
                "supplies": ["Automotive wire", "Terminals", "Heat shrink", "Loom sleeve", "Loom tape", "Labels"],
                "hold_point": "Every fitted control must work and be labelled before dash closure.",
                "image_tokens": ["wiring", "dashboard", "loom", "connector", "switch"],
            },
        ],
    },
    "chassis_rubbers": {
        "title": "Body Mount Rubber Stack",
        "summary": "Body-mount rubber, sleeve, washer, shim, and front-support isolation work.",
        "default_tools": ["Calipers", "Jack and axle stands", "Pry bars", "Socket set", "Torque wrench"],
        "default_supplies": ["Penetrating oil", "Rubber grease", "Anti-seize", "Temporary alignment bolts"],
        "subtasks": [
            {
                "title": "Capture Removed Mount Samples",
                "priority": "P0",
                "remaining": "all mount positions",
                "instruction": "Old rubbers and sleeves are measurement evidence, not scrap, until the new stack is locked.",
                "process_steps": [
                    "Remove one mount position at a time and keep upper/lower pieces together.",
                    "Photograph stack order, washers, sleeves, shims, and bolt orientation.",
                    "Measure outside diameter, height, sleeve length, bolt size, and hole condition.",
                    "Label the sample by vehicle position and side.",
                    "Record any crushed, missing, or mismatched pieces.",
                ],
                "tools": ["Calipers", "Camera", "Socket set", "Pry bar"],
                "supplies": ["Labels", "Zip bags", "Penetrating oil"],
                "hold_point": "No sample is discarded until replacement dimensions are confirmed.",
                "image_tokens": ["rubber", "body_mount", "mount", "sleeve", "shim"],
            },
            {
                "title": "Freeze Rubber, Sleeve, And Shim Specification",
                "priority": "P0",
                "remaining": "before order/fabrication",
                "instruction": "Define the full stack by position so the body returns to the intended height and alignment.",
                "process_steps": [
                    "Build a position-by-position table for rubbers, sleeves, cup washers, bolts, and shims.",
                    "Use docs/rubber-recreation-fabrication-spec-20260502.md as the fabrication handoff and close its hold dimensions.",
                    "Use data/manual/rubber_ordering_specs.csv as the cross-category rubber ordering matrix so body mounts, hoses, suspension bushes, weatherstrip, and HVAC rubber stay in the correct buy gates.",
                    "Use data/manual/body_mount_order_release_specs.csv for exact body-mount order lines, quantities, OE/reproduction candidates, local fabrication specs, shim packs, sleeves, and bolt packs.",
                    "Complete the open items in data/manual/body_mount_release_actions.csv before releasing any held order line.",
                    "Record station-by-station measurements and release status in data/manual/body_mount_station_closure_sheet.csv.",
                    "Use data/manual/rubber_recreation_toyota_oe_cross_reference.csv to reconcile Toyota NO.1-NO.5 station rows, OE part numbers, bolt families, and published shim/spacer thicknesses.",
                    "Use data/manual/rubber_recreation_aftermarket_dimension_crosscheck.csv as an external thickness sanity check, especially for tall, medium, seat, and short bushing construction.",
                    "Fill data/manual/rubber_recreation_measurement_closure.csv with caliper release values before final fabrication.",
                    "Compare old samples against chassis/body hole condition.",
                    "Specify rubber hardness/source and sleeve material before purchase.",
                    "Define shim pack thickness range and where adjustment is allowed.",
                    "Record any captive nut or mount repair needed before dry fit.",
                ],
                "tools": ["Calipers", "Straight edge", "Mount map", "Thread gauge"],
                "supplies": ["Spec sheet", "Rubber ordering matrix", "Body mount order release sheet", "Body mount action sheet", "OE cross-reference", "Aftermarket thickness cross-check", "Measurement closure sheet", "Sample rubbers", "Shim material", "Sleeve stock if fabricating"],
                "hold_point": "Final order or fabrication starts only after every mount position has a complete stack definition, the Toyota OE station rows have been reconciled against the physical vehicle, and the small-mount one-piece vs split-stack construction is resolved.",
                "image_tokens": ["body_mount", "rubber", "shim", "sleeve", "mount"],
            },
            {
                "title": "Lock Sourcing Path",
                "priority": "P1",
                "remaining": "avoid duplicate buys",
                "instruction": "Choose purchased kit, local fabrication, or mixed route before spending more.",
                "process_steps": [
                    "Check data/manual/rubber_ordering_specs.csv before any rubber purchase to confirm whether the item is buy-now, inspect-first, or deferred.",
                    "For body mounts, choose exactly one route in data/manual/body_mount_order_release_specs.csv: OE/reproduction purchase or local fabrication.",
                    "Check whether an available kit covers all required positions and sleeves.",
                    "Price any missing sleeves, washers, and shims separately.",
                    "Reject used/salvage rubber for structural body mounts.",
                    "Do not buy separate spring eye or shackle bushes here; those are gated by the Ironman kit receipt check.",
                    "Record vendor, delivery status, and expected fit risk.",
                    "Keep old samples available for supplier comparison until receipt check closes.",
                ],
                "tools": ["Parts list", "Camera", "Calipers"],
                "supplies": ["Body mount rubbers", "Sleeves", "Cup washers", "Shim pack", "Class-marked fasteners"],
                "hold_point": "Do not close procurement until the kit/fabrication route covers every mount position.",
                "image_tokens": ["rubber", "procurement", "inventory", "mount"],
            },
            {
                "title": "Dry-Fit Interface Check",
                "priority": "P0",
                "remaining": "before final body fastening",
                "instruction": "Trial-fit the mount stack before final paint-protected fastening.",
                "process_steps": [
                    "Clean mount faces and confirm primer/topcoat cure before fitting rubbers.",
                    "Install rubbers, sleeves, and temporary bolts without forcing the body into position.",
                    "Check bolt engagement, sleeve crush control, and washer seating.",
                    "Measure door/opening alignment and body level before final torque.",
                    "Mark required shims and update the final fastener list.",
                ],
                "tools": ["Jack/stands", "Alignment pins", "Torque wrench", "Measuring tape"],
                "supplies": ["New mount stack", "Temporary bolts", "Rubber grease", "Anti-seize"],
                "hold_point": "Final body fastening waits until the body sits naturally on the mount stack.",
                "image_tokens": ["body_mount", "chassis", "mount", "refit", "rubber"],
            },
        ],
    },
    "electrical_reset": {
        "title": "Electrical Baseline",
        "summary": "Baseline circuit scope, grounds, pass-through protection, fuse/relay function checks, and final loom routing.",
        "default_tools": ["Multimeter", "Test lamp", "Ratchet crimper", "Heat gun", "Fuse-protected test lead"],
        "default_supplies": ["Automotive wire", "Terminals", "Heat shrink", "Fuses and relays", "Loom sleeve"],
        "subtasks": [
            {
                "title": "Freeze Baseline Circuit Scope",
                "priority": "P0",
                "remaining": "before optional accessories",
                "instruction": "Separate must-work factory/baseline circuits from deferred accessories.",
                "process_steps": [
                    "List required baseline circuits: start, charge, ignition/fuel stop, lights, horn, wiper, gauges, brake lights, and grounds.",
                    "Mark accessories and audio as deferred unless required for safety or legal operation.",
                    "Assign each circuit to a fuse, relay, wire size, connector, and loom branch.",
                    "Check existing wires for brittle insulation, heat damage, bad splices, and unsupported routing.",
                    "Update the electrical tracker before buying optional parts.",
                ],
                "tools": ["Electrical tracker", "Multimeter", "Inspection light", "Camera"],
                "supplies": ["Labels", "Wire-size reference", "Fuse/relay plan"],
                "hold_point": "No optional circuit is added until the baseline circuit list is stable.",
                "image_tokens": ["wiring", "fuse", "relay", "dashboard", "firewall"],
            },
            {
                "title": "Verify Grounds And Pass-Throughs",
                "priority": "P0",
                "remaining": "all chassis/body grounds",
                "instruction": "Clean earth points and protect every body/firewall pass-through before loom closure.",
                "process_steps": [
                    "Identify battery, engine, chassis, body, dash, rear lighting, and accessory ground points.",
                    "Remove paint/rust only under the contact pad, then protect the surrounding metal.",
                    "Use star/serrated washers where a biting ground is required.",
                    "Fit grommets or bulkhead fittings at every firewall/body pass-through.",
                    "Voltage-drop test major grounds under load where possible.",
                ],
                "tools": ["Multimeter", "Wire brush", "Crimper", "Socket set"],
                "supplies": ["Star washers", "Ground straps", "Conductive anti-corrosion paste", "Grommets", "Heat shrink"],
                "hold_point": "No loom is tied down until grounds and pass-through protection are verified.",
                "image_tokens": ["ground", "firewall", "wiring", "grommet", "pass"],
            },
            {
                "title": "Run Fuse And Relay Function Checks",
                "priority": "P0",
                "remaining": "before battery-live closeout",
                "instruction": "Validate protection and switching before trim hides the loom.",
                "process_steps": [
                    "Check each fuse feed, fused output, relay trigger, and relay load wire separately.",
                    "Use a fuse-protected test feed for first energizing.",
                    "Confirm switch logic and relay orientation before connecting final loads.",
                    "Test lights, horn, wipers, charging warning, starter trigger, and fuel-stop/security behavior.",
                    "Record any warm wires, intermittent connections, or unexpected voltage drop.",
                ],
                "tools": ["Multimeter", "Test lamp", "Fuse-protected test lead", "Relay puller"],
                "supplies": ["Correct fuses", "Relays", "Spare terminals", "Contact cleaner"],
                "hold_point": "Circuits are not wrapped permanently until fuse and relay behavior is proven.",
                "image_tokens": ["fuse", "relay", "wiring", "switch", "connector"],
            },
            {
                "title": "Close Loom Routing And Labeling",
                "priority": "P1",
                "remaining": "after testing",
                "instruction": "Protect wiring from heat, abrasion, water, and future confusion.",
                "process_steps": [
                    "Route looms away from exhaust heat, sharp edges, pedals, steering movement, and water traps.",
                    "Add clips/P-clamps at sensible intervals without crushing the loom.",
                    "Wrap only after testing and after branch labels are fitted.",
                    "Leave service loops where switches, gauges, and fuse panels need future access.",
                    "Photograph final route before panels and trim cover it.",
                ],
                "tools": ["Crimper", "Heat gun", "Clip pliers", "Camera"],
                "supplies": ["Split conduit or braided sleeve", "Loom tape", "P-clamps", "Labels", "Cable ties"],
                "hold_point": "Final electrical closeout requires labelled, supported, and photographed routing.",
                "image_tokens": ["loom", "wiring", "connector", "dashboard", "firewall"],
            },
        ],
    },
    "mechanical_baseline": {
        "title": "Engine And Mechanical Baseline",
        "summary": "Controlled cleaning, stripped-access service work, leak inspection, defect logging, and baseline gate closure.",
        "default_tools": ["Socket/spanner set", "Drain pans", "Inspection light", "Torque wrench", "Pressure sprayer"],
        "default_supplies": ["DISS/APC cleaner", "GREZ OFF degreaser", "Rags", "Fluids", "Filters"],
        "subtasks": [
            {
                "title": "Clean Engine Bay And Powertrain Baseline",
                "priority": "P0",
                "remaining": "May 1 engine set queued",
                "instruction": "Clean enough to inspect leaks without forcing water into electrics, breathers, intake, or open lines.",
                "process_steps": [
                    "Photograph current oily and dusty areas before cleaning so leak paths are not lost.",
                    "Cover open intake, exposed electrics, alternator, fuse/relay areas, and open fluid ports.",
                    "Apply DISS/APC broadly with the Wadfow WRS1550 pressure sprayer; use GREZ OFF only on oily deposits.",
                    "Agitate with brushes, then rinse with controlled low to medium pressure and distance.",
                    "Blow dry seams, connectors, linkages, and low pockets; leave fully dry before starting or painting.",
                    "Re-photograph clean surfaces so new leaks can be identified after running.",
                ],
                "tools": ["Wadfow WRS1550 pressure sprayer", "Detail brushes", "Controlled pressure rinse", "Compressed air/blower"],
                "supplies": ["DISS/APC cleaner 5L", "GREZ OFF HD degreaser", "Masking plastic", "Rags", "Nitrile gloves"],
                "hold_point": "Engine is not run until water is cleared from electrics, breathers, and connector pockets.",
                "image_tokens": ["engine", "cleaning", "bay", "gearbox", "transmission"],
            },
            {
                "title": "Execute Must-Replace Service Pack",
                "priority": "P0",
                "remaining": "stripped-access service",
                "instruction": "Complete baseline consumables while access is open, before upgrades distract the work.",
                "process_steps": [
                    "Drain and inspect fluids for contamination before replacing them.",
                    "Replace filters, belts, suspect coolant hoses, fuel hose sections, clamps, and radiator cap as scoped.",
                    "Use hose sizes and ratings recorded in the engine hose specification; measure actual nipples before cutting hose.",
                    "Refill with correct fluids and bleed cooling/fuel systems as required.",
                    "Mark service date, fluids, parts used, and unresolved findings.",
                ],
                "tools": ["Drain pans", "Hose pick", "Clamp pliers", "Torque wrench", "Funnel"],
                "supplies": ["Engine oil", "Coolant", "Filters", "Fuel-rated hose/clamps", "Vacuum hose", "Radiator cap"],
                "hold_point": "Do not fabricate or replace high-pressure injector pipes with generic tube.",
                "image_tokens": ["engine", "hose", "cooling", "fuel", "service"],
            },
            {
                "title": "Run Leak And Condition Checks",
                "priority": "P0",
                "remaining": "after cleaning/service",
                "instruction": "Use the clean baseline to separate old grime from active faults.",
                "process_steps": [
                    "Pressure-test cooling system where equipment and access allow.",
                    "Inspect fuel feed, return, leak-off, filter, lift pump, and injector areas for wetness.",
                    "Check oil leaks around rocker cover, timing/front cover, sump, gearbox, and transfer case.",
                    "Check vacuum hoses, brake booster hose, and check valves for collapse or cracking.",
                    "Run the engine only after fluid levels and water-sensitive areas are safe, then recheck with bright light.",
                ],
                "tools": ["Cooling pressure tester", "Inspection light", "Mirror", "UV dye only if appropriate"],
                "supplies": ["Clean rags", "Hose clamps", "Replacement suspect hoses", "Leak marking tags"],
                "hold_point": "Active fuel, brake vacuum, coolant, or oil leaks become defect rows before refit.",
                "image_tokens": ["engine", "leak", "cooling", "fuel", "vacuum"],
            },
            {
                "title": "Log Post-Service Defects",
                "priority": "P1",
                "remaining": "after first run/check",
                "instruction": "Keep new findings visible as defects rather than burying them in general notes.",
                "process_steps": [
                    "Photograph each leak, damaged hose, noisy bearing, broken bracket, or missing clip.",
                    "Assign severity: safety hold, must fix before body, can fix after refit, or monitor.",
                    "Link each defect to a part, supply, or labor decision.",
                    "Order only confirmed baseline items; keep upgrade decisions separate.",
                    "Close defects with after-repair photos.",
                ],
                "tools": ["Camera", "Inspection light", "Defect checklist"],
                "supplies": ["Tags", "Paint marker", "Parts request list"],
                "hold_point": "No unresolved safety or access-critical mechanical defect is hidden by body refit.",
                "image_tokens": ["engine", "defect", "hose", "leak", "bracket"],
            },
            {
                "title": "Close Baseline Gate Before Upgrades",
                "priority": "P0",
                "remaining": "before optional upgrades",
                "instruction": "Baseline reliability must be known before power, steering, or accessory upgrades consume time and budget.",
                "process_steps": [
                    "Confirm fluids are filled, bled, and leak-checked.",
                    "Confirm service parts are installed or explicitly deferred with reason.",
                    "Confirm engine starts, idles, charges, and reaches temperature without new leaks.",
                    "Record residual defects and whether they block road validation.",
                    "Only then release optional mechanical upgrades.",
                ],
                "tools": ["Checklist", "Temperature gauge/IR thermometer", "Multimeter", "Camera"],
                "supplies": ["Fluid top-up stock", "Spare clamps", "Labels"],
                "hold_point": "Baseline closeout requires clean post-service evidence and an open-defect list.",
                "image_tokens": ["engine", "baseline", "service", "cleaning"],
            },
        ],
    },
    "brake_system": {
        "title": "Brake Safety Work",
        "summary": "Brake architecture confirmation, hydraulic refresh, bias/safety checks, and final brake gate.",
        "default_tools": ["Jack stands", "Brake line spanners", "Bleeder kit", "Torque wrench", "Inspection light"],
        "default_supplies": ["Brake cleaner", "Correct brake fluid", "Copper grease", "New copper washers", "Rags"],
        "subtasks": [
            {
                "title": "Confirm Installed Brake Architecture",
                "priority": "P0",
                "remaining": "before ordering more brake parts",
                "instruction": "Verify the actual front/rear hardware on the vehicle instead of ordering by assumption.",
                "process_steps": [
                    "Safely support the vehicle and remove wheels as needed.",
                    "Photograph front calipers/discs and rear drums/backing plates from both sides.",
                    "Record hose routing, hard-line condition, bleed screw access, and parking-brake linkage.",
                    "Identify pad/shoe type, cylinder/caliper family, and any missing hardware.",
                    "Update the parts list before buying pads, shoes, hoses, or cylinders.",
                ],
                "tools": ["Jack stands", "Wheel tools", "Inspection light", "Camera"],
                "supplies": ["Brake cleaner", "Paint marker", "Labels"],
                "hold_point": "No brake order is closed until hardware family is positively identified.",
                "image_tokens": ["brake", "disc", "drum", "caliper", "rear_axle"],
            },
            {
                "title": "Close Hydraulic Refresh Scope",
                "priority": "P0",
                "remaining": "safety-critical wear items",
                "instruction": "Replace age-critical hydraulic parts and any worn friction hardware during open access.",
                "process_steps": [
                    "Inspect flex hoses for cracking, swelling, chafing, and date/age risk.",
                    "Inspect hard lines for corrosion, flattening, poor clips, and wet unions.",
                    "Inspect pads/shoes, calipers/wheel cylinders, master cylinder, and fluid condition.",
                    "Replace confirmed hoses, copper washers, suspect cylinders, and friction material as scoped.",
                    "Bleed in the correct sequence using clean fluid and protect painted surfaces from spills.",
                ],
                "tools": ["Flare-nut spanners", "Bleeder bottle/vacuum bleeder", "Brake spring tools", "Torque wrench"],
                "supplies": ["Brake flex hose set", "Correct brake fluid", "Brake pads/shoes as confirmed", "Copper washers", "Copper grease"],
                "hold_point": "Any soft hose, leak, blocked bleeder, or uncertain cylinder/caliper keeps the brake gate open.",
                "image_tokens": ["brake", "hose", "hydraulic", "caliper", "drum"],
            },
            {
                "title": "Lock Brake-Bias Safety Path",
                "priority": "P1",
                "remaining": "after hardware baseline",
                "instruction": "Only change bias or conversion parts from evidence, not preference.",
                "process_steps": [
                    "Record current front/rear setup and tire/suspension changes that affect braking.",
                    "Inspect any proportioning/bias valve or factory balance hardware.",
                    "After hydraulic refresh, perform controlled low-speed brake checks.",
                    "Escalate to bias correction only if lockup, pull, or imbalance is observed.",
                    "Document the approved correction path before buying conversion parts.",
                ],
                "tools": ["Brake test checklist", "Pressure gauges if available", "Camera"],
                "supplies": ["Bias valve only if approved", "Line fittings only if scoped", "Brake fluid"],
                "hold_point": "No rear disc or bias modification proceeds without baseline brake behavior evidence.",
                "image_tokens": ["brake", "bias", "line", "rear", "front"],
            },
            {
                "title": "Close Brake Safety Gate",
                "priority": "P0",
                "remaining": "before road validation",
                "instruction": "Brakes must be leak-free, bled, adjusted, and proven before road use.",
                "process_steps": [
                    "Torque wheel and brake fasteners to workshop-manual spec.",
                    "Confirm firm pedal, no fluid drop, no visible leaks, and correct reservoir level.",
                    "Adjust rear drums/parking brake where applicable.",
                    "Run static hold, low-speed stop, pull check, and reinspection.",
                    "Photograph final hose routing, unions, and brake hardware before signoff.",
                ],
                "tools": ["Torque wrench", "Bleeder kit", "Inspection light", "Wheel chocks"],
                "supplies": ["Brake fluid", "Cleaner", "Paint marker", "Spare bleed caps"],
                "hold_point": "Any leak, pulling, soft pedal, seized adjuster, or uncertain torque blocks road validation.",
                "image_tokens": ["brake", "hose", "line", "wheel", "axle"],
            },
        ],
    },
    "eps_vitz_upgrade": {
        "title": "Vitz EPS Conversion",
        "summary": "Donor EPS baseline, mount/shaft geometry, protected electrical integration, and steering safety validation.",
        "default_tools": ["Calipers", "Angle finder", "Welder/fabrication tools", "Torque wrench", "Multimeter"],
        "default_supplies": ["Steel plate/brackets", "Class-marked fasteners", "Fused power cable", "Relays", "Loom protection"],
        "subtasks": [
            {
                "title": "Capture Donor EPS Hardware Baseline",
                "priority": "P0",
                "remaining": "before fabrication",
                "instruction": "Record donor column, motor, ECU, spline, and connector facts before cutting anything.",
                "process_steps": [
                    "Photograph the EPS motor, column sections, ECU, connectors, and labels.",
                    "Measure shaft lengths, spline counts, U-joint positions, and mounting points.",
                    "Record connector pinout references and which donor plugs are available.",
                    "Check motor clearance against pedals, dash, heater, and firewall.",
                    "Mark missing donor pieces before fabrication starts.",
                ],
                "tools": ["Calipers", "Angle finder", "Camera", "Marker"],
                "supplies": ["Labels", "Zip bags", "Reference pinout sheet"],
                "hold_point": "Fabrication waits until shaft, mount, and connector facts are recorded.",
                "image_tokens": ["eps", "vitz", "steering", "column", "motor"],
            },
            {
                "title": "Freeze Mount And Shaft Adapter Geometry",
                "priority": "P0",
                "remaining": "fabrication gate",
                "instruction": "Hold alignment, shaft phasing, and collapse/clearance as the main safety constraints.",
                "process_steps": [
                    "Mock the EPS position with the steering wheel, pedals, dash, and firewall clearance in place.",
                    "Keep U-joint angles reasonable and phase joints correctly.",
                    "Design brackets with service access and no flex at steering load.",
                    "Use class-marked fasteners and reinforcement where the body/firewall cannot carry load alone.",
                    "Trial-turn lock-to-lock before welding final brackets.",
                ],
                "tools": ["Welder", "Drill", "Angle finder", "Straight edge", "Torque wrench"],
                "supplies": ["Steel plate/tube", "Class 8.8 or better hardware", "Paint/primer for brackets", "Threadlocker"],
                "hold_point": "No final welding or cutting until lock-to-lock motion is smooth without binding.",
                "image_tokens": ["steering", "column", "mount", "adapter", "firewall"],
            },
            {
                "title": "Lock EPS Electrical Integration",
                "priority": "P0",
                "remaining": "after electrical baseline",
                "instruction": "EPS power and control must be fused, relay-controlled, grounded, and serviceable.",
                "process_steps": [
                    "Define battery feed, main fuse location, relay/ignition trigger, ground point, and wire size.",
                    "Keep EPS supply separate from weak old circuits.",
                    "Protect cable through bulkheads and near metal edges.",
                    "Mount ECU away from water, heat, and pedal/foot interference.",
                    "Test ignition-on behavior and fail-safe steering without assist.",
                ],
                "tools": ["Multimeter", "Crimper", "Heat gun", "Fuse-protected test lead"],
                "supplies": ["Heavy-gauge power cable", "Main fuse", "Relay", "Ground strap", "Heat shrink", "Loom sleeve"],
                "hold_point": "EPS cannot be energized permanently until fuse, relay, ground, and routing are documented.",
                "image_tokens": ["eps", "wiring", "relay", "fuse", "ground"],
            },
            {
                "title": "Run Assist Validation And Safety Checks",
                "priority": "P0",
                "remaining": "before road use",
                "instruction": "Validate steering mechanically and electrically before road testing.",
                "process_steps": [
                    "With front axle safely supported, turn lock-to-lock and check for binding, wire stretch, and contact.",
                    "Repeat with suspension at ride height and wheels on the ground.",
                    "Confirm steering returns consistently and assist is smooth without notchiness.",
                    "Check all fasteners after initial operation.",
                    "Road-test progressively only after manual fallback steering and braking are safe.",
                ],
                "tools": ["Jack stands", "Torque wrench", "Inspection light", "Checklist"],
                "supplies": ["Torque paint", "Threadlocker", "Spare fuses"],
                "hold_point": "Any bind, loose bracket, wiring strain, or unpredictable assist blocks road validation.",
                "image_tokens": ["steering", "eps", "linkage", "column", "suspension"],
            },
        ],
    },
    "suspension_upgrade": {
        "title": "Ironman Suspension Install",
        "summary": "Receipt check, baseline measurements, installation, loaded torque, alignment, and road validation for the ordered Ironman kit.",
        "default_tools": ["Jack and axle stands", "Torque wrench", "Breaker bar", "Pry bars", "Angle finder"],
        "default_supplies": ["Penetrating oil", "Anti-seize", "Threadlocker where specified", "Torque paint", "Marking tape"],
        "subtasks": [
            {
                "title": "Capture Measured Suspension Baseline",
                "priority": "P0",
                "remaining": "before parts removal",
                "instruction": "Record ride height and geometry before the Ironman kit changes the vehicle stance.",
                "process_steps": [
                    "Park on level ground and record tire pressure, fuel/load condition, and wheel/tire size.",
                    "Measure hub-to-arch or fixed chassis reference heights at all four corners.",
                    "Photograph shackle angles, spring pack condition, shock mounts, U-bolts, bump stops, and brake hose slack.",
                    "Check hanger holes for ovaling and cracks while the chassis prep photos are still fresh.",
                    "Record any existing lean, seized fasteners, or bent brackets.",
                ],
                "tools": ["Tape measure", "Angle finder", "Camera", "Inspection light"],
                "supplies": ["Paint marker", "Penetrating oil", "Measurement sheet"],
                "hold_point": "Do not remove springs until baseline heights and hanger condition are recorded.",
                "image_tokens": ["suspension", "leaf", "spring", "shackle", "shock"],
            },
            {
                "title": "Receive And Lock Complete Ironman Kit",
                "priority": "P0",
                "remaining": "main kit plus front dampers",
                "instruction": "Treat the Ironman order as incomplete until the main kit and separate front 24635FE dampers are counted.",
                "process_steps": [
                    "Lay out the shipment and photograph every box, label, part number, and hardware bag.",
                    "Check main kit contents against supplier list: springs, rear dampers, bushes, shackles/pins, U-bolts, and hardware.",
                    "Confirm separate front damper shipment includes 24635FE x2.",
                    "Close the RUB-007 ordering gate by confirming whether spring eye and shackle bushes are complete in the Ironman kit.",
                    "Reject duplicate alternate spring/shock buys unless the Ironman kit is confirmed incomplete.",
                    "Record missing/damaged pieces before starting installation.",
                ],
                "tools": ["Camera", "Parts checklist", "Calipers if hardware size is uncertain"],
                "supplies": ["Ironman Foamcell main kit", "Ironman 24635FE front dampers x2", "Labels", "Storage trays"],
                "hold_point": "Install waits until the complete kit and all hardware are physically verified.",
                "image_tokens": ["ironman", "suspension", "shock", "leaf", "procurement"],
            },
            {
                "title": "Install With Loaded-Torque Procedure",
                "priority": "P0",
                "remaining": "workshop install",
                "instruction": "Install safely and final-torque rubber pivot hardware only at loaded ride height.",
                "process_steps": [
                    "Support chassis and axle independently; never rely on a jack alone.",
                    "Soak old fasteners, remove shocks, release U-bolts, then remove one axle end/side in a controlled sequence.",
                    "Clean hanger and perch faces; repair cracks, oval holes, or damaged threads before new parts go in.",
                    "Install springs, bushes, shackles/pins, U-bolts, and shocks loosely according to the Ironman orientation instructions.",
                    "Set the vehicle on its weight, bounce/settle suspension, then torque pivots, U-bolts, and shocks to workshop-manual/Ironman spec.",
                    "Mark torqued fasteners and plan a re-torque after initial settling.",
                ],
                "tools": ["Jack stands", "Floor jack", "Torque wrench", "Breaker bar", "Pry bars", "Impact gun if available"],
                "supplies": ["Ironman springs/shocks/bushes/hardware", "Anti-seize", "Threadlocker only where specified", "Torque paint"],
                "hold_point": "Do not final-torque spring eye/shackle bushes while the axle is hanging.",
                "image_tokens": ["suspension", "leaf", "hanger", "u-bolt", "shock"],
            },
            {
                "title": "Close Alignment And Road Validation Gate",
                "priority": "P0",
                "remaining": "after body is on",
                "instruction": "Alignment is deliberately after body refit, but safety checks happen immediately after install.",
                "process_steps": [
                    "Immediately after install, check brake hose slack, steering/linkage clearance, shock travel, U-bolt seating, and shackle movement.",
                    "Recheck ride height after the vehicle settles and after the body is back on.",
                    "Complete professional alignment after body refit and loaded condition are stable.",
                    "Road-test progressively: slow steering/brake checks first, then short local drive, then re-torque inspection.",
                    "Log any lean, vibration, pull, clunk, or brake-hose strain as a defect.",
                ],
                "tools": ["Torque wrench", "Alignment booking/check sheet", "Inspection light", "Camera"],
                "supplies": ["Torque paint", "Spare split pins/clips if used", "Replacement brake hose/clip if stretch is found"],
                "hold_point": "Road validation cannot close until alignment, re-torque, and clearance checks are complete.",
                "image_tokens": ["suspension", "alignment", "shock", "leaf", "steering"],
            },
        ],
    },
    "interior_weatherproofing": {
        "title": "Interior Weatherproofing",
        "summary": "Dry shell confirmation, sealing order, dampening/trim stack, and cabin weatherproof gate.",
        "default_tools": ["Scraper", "Wire brush", "Seam roller", "Heat gun", "Caulking gun"],
        "default_supplies": ["Epoxy primer", "Seam sealer", "Sound deadener", "Closed-cell foam", "Bed/floor lining"],
        "subtasks": [
            {
                "title": "Confirm Floor And Shell Are Dry And Sealed",
                "priority": "P0",
                "remaining": "blocked by body closure",
                "instruction": "No insulation or trim goes over damp, rusty, or unsealed metal.",
                "process_steps": [
                    "Inspect floor, firewall, roof/gutters, window channels, and drain paths after body repair.",
                    "Confirm primer, seam sealer, and topcoat/liner have cured as required.",
                    "Water-test likely leak paths only after coatings are ready for exposure.",
                    "Dry fully and photograph any leak, pinhole, or unsealed seam.",
                    "Close body defects before installing deadener or trim.",
                ],
                "tools": ["Inspection light", "Moisture check by touch/cloth", "Camera", "Air blower"],
                "supplies": ["Clean rags", "Masking tape", "Leak marking tags"],
                "hold_point": "Weatherproofing remains blocked until the body shell is sealed and dry.",
                "image_tokens": ["floor", "firewall", "gutter", "rust", "cabin"],
            },
            {
                "title": "Apply Weatherproofing Layer Order",
                "priority": "P0",
                "remaining": "after primer/topcoat cure",
                "instruction": "Use the correct order so water cannot be trapped under finish materials.",
                "process_steps": [
                    "Clean and solvent-wipe only after coatings are cured and dry.",
                    "Apply seam sealer where specified, then allow cure.",
                    "Apply bed/floor lining or topcoat where planned.",
                    "Keep drains and bolt holes open; mask threads and captive nuts.",
                    "Photograph layer completion before sound deadening hides it.",
                ],
                "tools": ["Caulking gun", "Seam spreader", "Roller/brush", "Masking tools"],
                "supplies": ["Seam sealer", "Bed/floor lining", "Masking tape", "Solvent wipes"],
                "hold_point": "Sound deadener starts only after sealing and lining layers are finished and cured.",
                "image_tokens": ["sealer", "bed", "floor", "interior", "weatherproof"],
            },
            {
                "title": "Install Dampening And Trim Stack",
                "priority": "P1",
                "remaining": "after leak gate",
                "instruction": "Install noise and trim materials without blocking service access or drains.",
                "process_steps": [
                    "Apply sound deadener only to clean, dry, cured surfaces.",
                    "Roll each sheet firmly and avoid bridging over seams or water traps.",
                    "Use closed-cell foam where moisture resistance is needed; avoid absorbent foam on floors.",
                    "Keep seat, belt, drain, and access holes open.",
                    "Trial-fit carpet/vinyl/trim before adhesive finalization.",
                ],
                "tools": ["Seam roller", "Utility knife", "Heat gun", "Trim tools"],
                "supplies": ["Sound deadener", "Closed-cell foam", "Carpet/vinyl", "Adhesive suitable for automotive trim"],
                "hold_point": "No absorbent material is installed where future leaks could trap moisture.",
                "image_tokens": ["interior", "floor", "trim", "weatherproof", "cabin"],
            },
            {
                "title": "Close Cabin Weatherproof Gate",
                "priority": "P1",
                "remaining": "before final trim signoff",
                "instruction": "Document finished cabin condition before seats, belts, and trim obscure the work.",
                "process_steps": [
                    "Photograph finished floor, firewall, rear cargo area, and seams.",
                    "Confirm drains, seat/belt mounts, wiring grommets, and inspection points remain accessible.",
                    "Check for adhesive squeeze-out, loose edges, blocked holes, or sharp trim edges.",
                    "Record residual leak risks and later checks after rain/wash exposure.",
                    "Mark cabin ready for final assembly only after defects close.",
                ],
                "tools": ["Camera", "Inspection light", "Trim tools"],
                "supplies": ["Touch-up adhesive", "Edge tape", "Replacement clips"],
                "hold_point": "Final trim waits until sealing evidence and access points are confirmed.",
                "image_tokens": ["interior", "cabin", "floor", "trim", "weatherproof"],
            },
        ],
    },
    "final_assembly_validation": {
        "title": "Final Assembly And Validation",
        "summary": "Punch-list creation, controlled reassembly, full function checks, and road validation closeout.",
        "default_tools": ["Torque wrench", "Multimeter", "Inspection light", "Camera", "Checklists"],
        "default_supplies": ["Class-marked fasteners", "Anti-seize", "Threadlocker", "Fluids", "Labels"],
        "subtasks": [
            {
                "title": "Build Full Punch-List",
                "priority": "P0",
                "remaining": "before reassembly starts",
                "instruction": "Collect all open defects and dependencies before parts go back on.",
                "process_steps": [
                    "Export open workstream steps, issue jobs, and unresolved procurement rows.",
                    "Sort by dependency: body/chassis, mechanical, electrical, brake, suspension, interior, trim.",
                    "Flag safety blockers and access blockers separately.",
                    "Assign each item an owner, required part/tool, and closeout evidence requirement.",
                    "Freeze what is deferred so it does not block baseline completion later.",
                ],
                "tools": ["Dashboard checklist", "Camera", "Marker"],
                "supplies": ["Labels", "Fastener trays", "Defect tags"],
                "hold_point": "Reassembly starts only with a visible punch-list and known blockers.",
                "image_tokens": ["overview", "validation", "body", "engine", "frame"],
            },
            {
                "title": "Run Controlled Reassembly",
                "priority": "P0",
                "remaining": "dependency order",
                "instruction": "Reassemble in a sequence that preserves access for torque, wiring, fluids, and defect checks.",
                "process_steps": [
                    "Start with access-critical chassis/body interfaces and protected routing.",
                    "Install components loosely where alignment is still being set.",
                    "Use new class-marked hardware where structural fasteners were scoped for replacement.",
                    "Torque to workshop-manual/spec sheet values and mark completed fasteners.",
                    "Photograph hidden interfaces before they are covered.",
                ],
                "tools": ["Torque wrench", "Socket/spanner set", "Alignment pins", "Camera"],
                "supplies": ["Fastener kits", "Anti-seize", "Threadlocker where specified", "Torque paint"],
                "hold_point": "Covered areas need photo and torque signoff before the next layer goes on.",
                "image_tokens": ["assembly", "body", "chassis", "mount", "engine"],
            },
            {
                "title": "Execute Full Functional Checks",
                "priority": "P0",
                "remaining": "before road test",
                "instruction": "Validate systems statically before the vehicle moves under its own power.",
                "process_steps": [
                    "Check lights, horn, wipers, gauges, charging, start, fuel stop/security, and accessories.",
                    "Check engine fluids, cooling cycle, leaks, throttle return, clutch/gear selection, and idle behavior.",
                    "Check brake pedal, parking brake, steering lock-to-lock, suspension clearance, and wheel torque.",
                    "Check doors, latches, seats, belts, glass, and weather seals.",
                    "Record failures as punch-list items and retest after correction.",
                ],
                "tools": ["Multimeter", "Test lamp", "Torque wrench", "Inspection light", "Fluid pressure/bleed tools"],
                "supplies": ["Spare fuses", "Fluids", "Cleaner/rags", "Labels"],
                "hold_point": "Road test is blocked by any brake, steering, fuel leak, cooling, charging, or wheel-fastener fault.",
                "image_tokens": ["validation", "engine", "wiring", "brake", "steering"],
            },
            {
                "title": "Close Road-Validation Gate",
                "priority": "P0",
                "remaining": "after controlled road checks",
                "instruction": "Use staged road checks and reinspections before declaring baseline complete.",
                "process_steps": [
                    "Start with static and yard-speed brake/steering checks.",
                    "Run a short local drive and listen for clunks, vibration, pull, heat, smells, or fluid leaks.",
                    "Recheck wheel torque, suspension fasteners, brake leaks, fluid levels, and electrical charging.",
                    "Complete alignment confirmation and suspension re-torque where required.",
                    "Log residual defects and only close baseline when safety-critical items are clear.",
                ],
                "tools": ["Torque wrench", "Inspection light", "Road-test checklist", "Camera"],
                "supplies": ["Fluid top-ups", "Torque paint", "Spare fuses", "Defect tags"],
                "hold_point": "Baseline is complete only after road check and post-road inspection are recorded.",
                "image_tokens": ["validation", "road", "suspension", "brake", "engine"],
            },
        ],
    },
}

SUBTASK_IMAGE_STOPWORDS: set[str] = {
    "and",
    "the",
    "for",
    "with",
    "from",
    "this",
    "that",
    "before",
    "after",
    "where",
    "each",
    "until",
    "only",
    "work",
    "tool",
    "tools",
    "supply",
    "supplies",
    "process",
    "check",
    "checks",
    "close",
    "gate",
}

SUPPLY_STATUS_ORDER: tuple[str, ...] = ("previously", "in_process", "still_required")
INVENTORY_GROUP_ORDER: tuple[str, ...] = ("electrical", "mechanical", "tools", "parts", "substances")
PLACEHOLDER_IMAGE_PATH = "./assets/image-needed.svg"


def clean(value: Any) -> str:
    return str(value or "").strip()


def norm(value: Any) -> str:
    return clean(value).lower()


def split_pipe(value: str) -> list[str]:
    return [token.strip() for token in clean(value).split("|") if token.strip()]


def first_non_empty(row: dict[str, str], keys: list[str]) -> str:
    for key in keys:
        value = clean(row.get(key))
        if value:
            return value
    return ""


def humanize_token(value: str) -> str:
    token = clean(value).replace("|", ", ")
    return token.replace("_", " ").strip().title()


def title_from_id(value: str) -> str:
    return humanize_token(value)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_csv_optional(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return load_csv(path)


def workbook_row_has_values(row: dict[str, str], max_col: int = 14) -> bool:
    return any(clean(row.get(f"col_{index}")) for index in range(1, max_col + 1))


def workbook_section_rows(
    rows: list[dict[str, str]],
    section_heading: str,
    column_keys: list[str],
) -> list[dict[str, str]]:
    section_index: int | None = None
    section_heading_key = norm(section_heading)
    for index, row in enumerate(rows):
        if norm(row.get("col_1")).startswith(section_heading_key):
            section_index = index
            break
    if section_index is None:
        return []

    parsed: list[dict[str, str]] = []
    for row in rows[section_index + 2 :]:
        first_cell = clean(row.get("col_1"))
        if WORKBOOK_SECTION_HEADING_RE.match(first_cell):
            break
        if not workbook_row_has_values(row, max_col=max(9, len(column_keys))):
            continue

        parsed_row: dict[str, str] = {}
        has_value = False
        for column_index, key in enumerate(column_keys, start=1):
            value = clean(row.get(f"col_{column_index}"))
            parsed_row[key] = value
            if value:
                has_value = True
        if has_value:
            parsed.append(parsed_row)
    return parsed


def parse_electrical_master_metadata(master_rows: list[dict[str, str]]) -> dict[str, str]:
    title = ""
    last_updated = ""
    purpose = ""

    for row in master_rows:
        col_1 = clean(row.get("col_1"))
        if not col_1:
            continue
        col_1_key = norm(col_1)

        if not title and "electrical master" in col_1_key:
            title = col_1

        if "last updated:" in col_1_key or "purpose:" in col_1_key:
            for segment in [value.strip() for value in col_1.split("|")]:
                segment_key = segment.lower()
                if segment_key.startswith("last updated:"):
                    last_updated = segment.split(":", 1)[1].strip()
                elif segment_key.startswith("purpose:"):
                    purpose = segment.split(":", 1)[1].strip()

    return {
        "title": title or "Electrical Master - Clear Tracker (As-Built + Remaining Work)",
        "last_updated": last_updated,
        "purpose": purpose,
    }


def load_electrical_layout_templates(template_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    templates: list[dict[str, str]] = []
    seen_values: set[str] = set()

    for row in template_rows:
        excel_row = clean(row.get("excel_row"))
        for index in range(1, 15):
            value = clean(row.get(f"col_{index}"))
            if not value or value == "~":
                continue
            value_key = norm(value)
            if value_key in seen_values:
                continue
            seen_values.add(value_key)
            templates.append(
                {
                    "label": value,
                    "source_ref": f"workbook_electrical_templates#row_{excel_row}" if excel_row else "workbook_electrical_templates",
                }
            )
    return templates


def load_electrical_spec_layout() -> dict[str, Any]:
    master_rows = load_csv_optional(WORKBOOK_ELECTRICAL_MASTER_PATH)
    template_rows = load_csv_optional(WORKBOOK_ELECTRICAL_TEMPLATES_PATH)
    if not master_rows and not template_rows:
        return {}

    metadata = parse_electrical_master_metadata(master_rows)

    return {
        "scope": "full",
        "title": metadata["title"],
        "last_updated": metadata["last_updated"],
        "purpose": metadata["purpose"],
        "source_refs": [
            "data/manual/workbook_tabs/electrical_master.csv",
            "data/manual/workbook_tabs/electrical_templates.csv",
        ],
        "layout_templates": load_electrical_layout_templates(template_rows),
        "wiring_progress_tracker": workbook_section_rows(
            master_rows,
            "1) Wiring Progress Tracker",
            [
                "priority",
                "area",
                "task",
                "status",
                "done",
                "current_state",
                "next_action",
                "dependency",
                "parts_tools_impact",
            ],
        ),
        "locked_as_built_standards": workbook_section_rows(
            master_rows,
            "2) Locked As-Built Standards",
            [
                "standard",
                "decision",
                "why_locked",
                "revisit_trigger",
            ],
        ),
        "relay_quick_lookup": workbook_section_rows(
            master_rows,
            "3) Relay Quick Lookup",
            [
                "relay_pos",
                "function",
                "relay_colour",
                "power_code",
                "power_loom",
                "wire_size",
                "control_loom",
                "implementation_status",
            ],
        ),
        "connector_quick_lookup": workbook_section_rows(
            master_rows,
            "4) Connector Quick Lookup",
            [
                "connector",
                "type",
                "loom_or_branch",
                "terminated_circuits",
                "status",
                "notes",
            ],
        ),
        "loom_quick_lookup": workbook_section_rows(
            master_rows,
            "5) Loom Quick Lookup",
            [
                "loom_id",
                "loom_name",
                "build_makeup",
                "primary_role",
                "status",
            ],
        ),
        "minimum_electrical_gate": workbook_section_rows(
            master_rows,
            "6) Minimum Electrical Gate Before Tub Reinstall",
            [
                "step",
                "action",
                "target_stage",
                "status",
            ],
        ),
    }


def row_matches_keywords(values: list[str], keywords: tuple[str, ...]) -> bool:
    haystack = " ".join(norm(value) for value in values)
    return any(keyword in haystack for keyword in keywords)


def build_dashboard_electrical_spec_layout(full_layout: dict[str, Any]) -> dict[str, Any]:
    if not full_layout:
        return {}

    wiring_rows = list(full_layout.get("wiring_progress_tracker") or [])
    gate_rows = list(full_layout.get("minimum_electrical_gate") or [])
    connector_rows = list(full_layout.get("connector_quick_lookup") or [])
    loom_rows = list(full_layout.get("loom_quick_lookup") or [])

    dashboard_wiring_rows = [
        row
        for row in wiring_rows
        if row_matches_keywords(
            [row.get("area", ""), row.get("task", ""), row.get("current_state", ""), row.get("next_action", "")],
            DASHBOARD_ELECTRICAL_FOCUS_KEYWORDS,
        )
    ]
    dashboard_gate_rows = [
        row
        for row in gate_rows
        if row_matches_keywords([row.get("action", ""), row.get("target_stage", "")], DASHBOARD_ELECTRICAL_FOCUS_KEYWORDS)
    ]
    dashboard_connector_rows = [
        row
        for row in connector_rows
        if row_matches_keywords(
            [row.get("connector", ""), row.get("loom_or_branch", ""), row.get("notes", "")],
            DASHBOARD_ELECTRICAL_FOCUS_KEYWORDS,
        )
    ]
    dashboard_loom_rows = [row for row in loom_rows if norm(row.get("loom_id")) in {"l4", "l5a", "l5b"}]

    return {
        "scope": "dashboard_focus",
        "title": full_layout.get("title", ""),
        "last_updated": full_layout.get("last_updated", ""),
        "purpose": full_layout.get("purpose", ""),
        "source_refs": full_layout.get("source_refs", []),
        "layout_templates": list(full_layout.get("layout_templates") or []),
        "wiring_progress_tracker": dashboard_wiring_rows or wiring_rows[:8],
        "locked_as_built_standards": list(full_layout.get("locked_as_built_standards") or [])[:4],
        "relay_quick_lookup": list(full_layout.get("relay_quick_lookup") or [])[:4],
        "connector_quick_lookup": dashboard_connector_rows or connector_rows[:4],
        "loom_quick_lookup": dashboard_loom_rows or loom_rows[:3],
        "minimum_electrical_gate": dashboard_gate_rows or gate_rows[:4],
    }


def path_for_ui(relative_path: str) -> str:
    normalized = clean(relative_path).replace("\\", "/")
    if normalized.startswith("./"):
        normalized = normalized[2:]
    return f"../../{normalized}"


def image_caption(row: dict[str, str]) -> str:
    component = humanize_token(row.get("specific_component", ""))
    stage = humanize_token(row.get("stage", ""))
    date = clean(row.get("captured_date"))
    if component and stage:
        return f"{component} · {stage} · {date}"
    if component:
        return f"{component} · {date}"
    return clean(row.get("file_name"))


def is_photo_row(row: dict[str, str]) -> bool:
    if norm(row.get("media_type")) != "photo":
        return False
    relative_path = norm(row.get("relative_path"))
    if "non_car_review/" in relative_path:
        return False
    return True


def row_text_blob(row: dict[str, str]) -> str:
    return " ".join(
        [
            norm(row.get("media_id")),
            norm(row.get("file_name")),
            norm(Path(clean(row.get("file_name"))).stem),
            norm(row.get("relative_path")),
            norm(row.get("component_group")),
            norm(row.get("specific_component")),
            norm(row.get("stage")),
            norm(row.get("tags")),
            norm(row.get("notes")),
            norm(row.get("observed_state")),
        ]
    )


DASHBOARD_STRICT_SPECIFIC_COMPONENTS: set[str] = {
    "dashboard_switch_and_control_hardware",
    "dashboard_fascia_trim",
    "dashboard_shell_and_cabin",
    "dashboard_lower_structure",
    "dashboard_and_cabin_stripdown",
}

DASHBOARD_ALLOWED_SPECIFIC_TOKENS: tuple[str, ...] = (
    "switch",
    "control",
    "fascia",
    "panel",
    "button",
    "knob",
    "cluster",
)

DASHBOARD_EXCLUDED_MEDIA_IDS: set[str] = {
    # White front headlamp-surround panel and wing-mirror photos are paint/exterior items.
    "20260412_223534",
    "20260412_223539",
}

DASHBOARD_INCLUDED_MEDIA_IDS: set[str] = {
    # Baseline interior photos that clearly show dashboard/controls.
    "20260317_165113",
    "20260317_165114_gp_meA0ZqNA",
    "20260317_165157",
    "20260317_165157_gp_r5zl6uag",
    "20260321_235600",
    "20260329_122855",
    "20260329_122855_gp_B94NpLbg",
}


def is_dashboard_workstream_photo(row: dict[str, str]) -> bool:
    media_id = clean(row.get("media_id"))
    if media_id in DASHBOARD_INCLUDED_MEDIA_IDS:
        return True
    if media_id in DASHBOARD_EXCLUDED_MEDIA_IDS:
        return False

    specific = norm(row.get("specific_component"))
    component_group = norm(row.get("component_group"))
    stage = norm(row.get("stage"))
    tags = norm(row.get("tags"))

    # Keep dashboard workstream narrowly focused on explicit dashboard/control evidence.
    if specific in DASHBOARD_STRICT_SPECIFIC_COMPONENTS:
        return True
    if specific == "firewall_and_dash_wiring":
        return False
    if specific.startswith("dashboard_") and any(token in specific for token in DASHBOARD_ALLOWED_SPECIFIC_TOKENS):
        return True
    if (
        "dash" in tags
        and component_group == "interior_cabin"
        and stage in {"electrical_rework", "hardware_refinish"}
    ):
        return True
    return False


def normalize_media_stem(value: str) -> str:
    candidate = clean(value)
    if not candidate:
        return ""
    candidate = candidate.split("?", 1)[0].split("#", 1)[0]
    stem = Path(candidate).stem or candidate
    stem = re.sub(r"_gp_[a-zA-Z0-9]+(?:_\d+)?$", "", stem)
    stem = re.sub(r"_exported_\d+$", "", stem)
    return stem.lower()


def canonical_media_key(row: dict[str, str]) -> str:
    for field in ("media_id", "file_name", "relative_path", "path"):
        key = normalize_media_stem(row.get(field, ""))
        if key:
            return key
    return ""


def image_score(row: dict[str, str], profile: dict[str, set[str]]) -> int:
    if not is_photo_row(row):
        return -999

    component_group = norm(row.get("component_group"))
    stage = norm(row.get("stage"))
    specific_component = norm(row.get("specific_component"))
    text_blob = row_text_blob(row)
    confidence = norm(row.get("confidence"))
    component_match = component_group in profile["component_groups"]
    stage_match = stage in profile["stages"]

    score = 0

    if component_match:
        score += 14
    if stage_match:
        score += 24

    keyword_hits = 0
    for keyword in profile["keywords"]:
        if keyword in text_blob:
            keyword_hits += 1
    if keyword_hits:
        score += min(6, keyword_hits) * 3
    else:
        score -= 10

    if confidence == "high":
        score += 2
    elif confidence == "medium":
        score += 1

    if "documentation_reference" in component_group:
        score -= 30
    if not specific_component:
        score -= 2
    if not stage_match:
        score -= 22
    if not component_match:
        score -= 8
    if not stage_match and not component_match:
        score -= 30
    return score


def extract_reference_tokens(values: list[str]) -> set[str]:
    tokens: set[str] = set()
    for value in values:
        text = clean(value)
        if not text:
            continue
        for raw_token in re.split(r"[|,\s]+", text):
            token = raw_token.strip().strip("()[]{}")
            if not token:
                continue
            lowered = token.lower()
            if any(lowered.startswith(prefix) for prefix in REFERENCE_IGNORE_PREFIXES):
                continue
            if lowered.endswith((".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov", ".heic")):
                lowered = lowered.rsplit(".", 1)[0]
            if re.fullmatch(r"\d{8}", lowered):
                continue
            if len(lowered) < 6:
                continue
            if not any(ch.isdigit() for ch in lowered) and "_" not in lowered and "-" not in lowered:
                continue
            tokens.add(lowered)
    return tokens


def row_token_matches(row: dict[str, str], reference_tokens: set[str]) -> list[str]:
    if not reference_tokens:
        return []
    blob = row_text_blob(row)
    matches = [token for token in reference_tokens if token in blob]
    matches.sort(key=len, reverse=True)
    return matches[:6]


def image_payload(row: dict[str, str], matched_tokens: list[str]) -> dict[str, Any]:
    media_type = clean(row.get("media_type")) or "photo"
    return {
        "path": path_for_ui(clean(row.get("relative_path"))),
        "caption": image_caption(row),
        "captured_date": clean(row.get("captured_date")),
        "captured_time": clean(row.get("captured_time")),
        "media_type": media_type,
        "component_group": clean(row.get("component_group")),
        "specific_component": clean(row.get("specific_component")),
        "stage": clean(row.get("stage")),
        "media_id": clean(row.get("media_id")),
        "matched_tokens": matched_tokens,
    }


def rows_for_media_ids(photo_rows: list[dict[str, str]], media_ids: tuple[str, ...]) -> list[dict[str, str]]:
    rows_by_media_id = {
        clean(row.get("media_id")): row
        for row in photo_rows
        if is_photo_row(row) and clean(row.get("media_id"))
    }
    return [rows_by_media_id[media_id] for media_id in media_ids if media_id in rows_by_media_id]


def photo_rows_by_media_id(photo_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    rows_by_id: dict[str, dict[str, str]] = {}
    for row in photo_rows:
        if not is_photo_row(row):
            continue
        media_id = clean(row.get("media_id"))
        file_stem = Path(clean(row.get("file_name"))).stem
        if media_id:
            rows_by_id[media_id] = row
        if file_stem:
            rows_by_id[file_stem] = row
    return rows_by_id


def build_workstream_requirements(
    requirement_rows: list[dict[str, str]],
    photo_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    rows_by_id = photo_rows_by_media_id(photo_rows)
    requirements: list[dict[str, Any]] = []
    for row in requirement_rows:
        evidence_ids = split_pipe(row.get("photo_evidence", ""))
        evidence_images = [
            image_payload(rows_by_id[media_id], [])
            for media_id in evidence_ids
            if media_id in rows_by_id
        ]
        requirement_id = clean(row.get("requirement_id")) or clean(row.get("pipe_id")) or clean(row.get("part_id"))
        requirement_name = (
            clean(row.get("requirement_name"))
            or clean(row.get("pipe_or_line"))
            or clean(row.get("part_name"))
        )
        requirements.append(
            {
                "requirement_id": requirement_id,
                "requirement_name": requirement_name,
                "pipe_id": clean(row.get("pipe_id")),
                "vehicle_location": clean(row.get("vehicle_location")),
                "pipe_or_line": clean(row.get("pipe_or_line")),
                "replace_scope": clean(row.get("replace_scope")),
                "quantity": clean(row.get("quantity")) or clean(row.get("qty")),
                "photo_evidence": evidence_ids,
                "photo_status": clean(row.get("photo_status")),
                "spec_status": clean(row.get("spec_status")),
                "acquisition_status": clean(row.get("acquisition_status")),
                "installation_status": clean(row.get("installation_status")),
                "current_action": clean(row.get("current_action")),
                "exact_recreation_spec": clean(row.get("exact_recreation_spec")),
                "material_spec": clean(row.get("material_spec")),
                "critical_measurements": clean(row.get("critical_measurements")),
                "fit_and_test": clean(row.get("fit_and_test")),
                "source_ref": clean(row.get("source_ref")),
                "notes": clean(row.get("notes")),
                "evidence_images": dedupe_payload_images(evidence_images),
            }
        )
    return requirements


def build_replacement_pipe_requirements(
    requirement_rows: list[dict[str, str]],
    photo_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    return build_workstream_requirements(requirement_rows, photo_rows)


def replacement_pipe_order_release_payload(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    payload: list[dict[str, str]] = []
    for row in rows:
        release_state = clean(row.get("order_release_state"))
        payload.append(
            {
                "order_line_id": clean(row.get("order_line_id")),
                "route": clean(row.get("route")),
                "item": clean(row.get("item")),
                "part_number_or_code": clean(row.get("part_number_or_code")),
                "qty_required": clean(row.get("qty_required")),
                "qty_to_order": clean(row.get("qty_to_order")),
                "spec_status": "spec_ready",
                "order_release_state": release_state or "spec_ready",
                "exact_order_spec": clean(row.get("exact_order_spec")),
                "material_spec": clean(row.get("material_spec")),
                "source_basis": clean(row.get("source_basis")),
                "user_action_required": clean(row.get("user_action_required")),
                "do_not_order_if": clean(row.get("do_not_order_if")),
                "notes": clean(row.get("notes")),
            }
        )
    return payload


def replacement_pipe_release_action_payload(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "action_id": clean(row.get("action_id")),
            "priority": clean(row.get("priority")),
            "owner": clean(row.get("owner")),
            "action": clean(row.get("action")),
            "status": clean(row.get("status")),
            "blocks_order_lines": clean(row.get("blocks_order_lines")),
            "record_result_in": clean(row.get("record_result_in")),
            "why_it_matters": clean(row.get("why_it_matters")),
        }
        for row in rows
    ]


def replacement_pipe_circuit_closure_payload(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "circuit_id": clean(row.get("circuit_id")),
            "vehicle_location": clean(row.get("vehicle_location")),
            "pipe_or_line": clean(row.get("pipe_or_line")),
            "order_lines": clean(row.get("order_lines")),
            "photo_status": clean(row.get("photo_status")),
            "barb_or_fitting_a": clean(row.get("barb_or_fitting_a")),
            "barb_or_fitting_b": clean(row.get("barb_or_fitting_b")),
            "route_length_mm": clean(row.get("route_length_mm")),
            "tube_or_hose_od_id": clean(row.get("tube_or_hose_od_id")),
            "thread_or_flare": clean(row.get("thread_or_flare")),
            "bend_template_status": clean(row.get("bend_template_status")),
            "clip_support_status": clean(row.get("clip_support_status")),
            "release_status": clean(row.get("release_status")),
            "action_required": clean(row.get("action_required")),
            "notes": clean(row.get("notes")),
        }
        for row in rows
    ]


def body_mount_order_release_payload(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    payload: list[dict[str, str]] = []
    for row in rows:
        release_state = clean(row.get("order_release_state"))
        payload.append(
            {
                "order_line_id": clean(row.get("order_line_id")),
                "route": clean(row.get("route")),
                "item": clean(row.get("item")),
                "part_number_or_code": clean(row.get("part_number_or_code")),
                "qty_required": clean(row.get("qty_required")),
                "qty_to_order": clean(row.get("qty_to_order")),
                "spec_status": "spec_ready",
                "order_release_state": release_state or "spec_ready",
                "exact_order_spec": clean(row.get("exact_order_spec")),
                "material_spec": clean(row.get("material_spec")),
                "source_basis": clean(row.get("source_basis")),
                "user_action_required": clean(row.get("user_action_required")),
                "do_not_order_if": clean(row.get("do_not_order_if")),
                "notes": clean(row.get("notes")),
            }
        )
    return payload


def body_mount_release_action_payload(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "action_id": clean(row.get("action_id")),
            "priority": clean(row.get("priority")),
            "owner": clean(row.get("owner")),
            "action": clean(row.get("action")),
            "status": clean(row.get("status")),
            "blocks_order_lines": clean(row.get("blocks_order_lines")),
            "record_result_in": clean(row.get("record_result_in")),
            "why_it_matters": clean(row.get("why_it_matters")),
        }
        for row in rows
    ]


def body_mount_station_closure_payload(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "station_id": clean(row.get("station_id")),
            "vehicle_position": clean(row.get("vehicle_position")),
            "working_position_type": clean(row.get("working_position_type")),
            "candidate_toyota_station": clean(row.get("candidate_toyota_station")),
            "expected_rubber_family": clean(row.get("expected_rubber_family")),
            "expected_rubber_qty_at_position": clean(row.get("expected_rubber_qty_at_position")),
            "old_parts_present": clean(row.get("old_parts_present")),
            "shim_or_spacer_thickness_mm": clean(row.get("shim_or_spacer_thickness_mm")),
            "sleeve_id_mm": clean(row.get("sleeve_id_mm")),
            "sleeve_od_mm": clean(row.get("sleeve_od_mm")),
            "sleeve_length_mm": clean(row.get("sleeve_length_mm")),
            "bolt_pitch": clean(row.get("bolt_pitch")),
            "bolt_under_head_length_mm": clean(row.get("bolt_under_head_length_mm")),
            "captive_nut_depth_mm": clean(row.get("captive_nut_depth_mm")),
            "final_bolt_length_mm": clean(row.get("final_bolt_length_mm")),
            "release_status": clean(row.get("release_status")),
            "action_required": clean(row.get("action_required")),
            "notes": clean(row.get("notes")),
        }
        for row in rows
    ]


def build_procurement_evidence_images(photo_rows: list[dict[str, str]], max_images: int = 64) -> list[dict[str, Any]]:
    candidates = [
        row
        for row in photo_rows
        if is_photo_row(row)
        and norm(row.get("stage")) == "procurement_reconciliation"
    ]
    sorted_rows = sorted(
        candidates,
        key=lambda row: (
            clean(row.get("captured_date")),
            clean(row.get("captured_time")),
            clean(row.get("file_name")),
        ),
        reverse=True,
    )
    selected: list[dict[str, Any]] = []
    seen_media_keys: set[str] = set()
    for row in sorted_rows:
        media_key = canonical_media_key(row)
        if not media_key or media_key in seen_media_keys:
            continue
        seen_media_keys.add(media_key)
        payload = image_payload(row, [])
        payload["match_basis"] = "procurement_reconciliation"
        selected.append(payload)
        if len(selected) >= max_images:
            break
    return selected


def select_diverse_candidates(
    candidates: list[dict[str, Any]],
    max_images: int,
    per_component_limit: int,
    per_date_limit: int,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    seen_media_keys: set[str] = set()
    by_component: Counter[str] = Counter()
    by_date: Counter[str] = Counter()

    def try_add(candidate: dict[str, Any], enforce_limits: bool) -> None:
        if len(selected) >= max_images:
            return
        media_key = canonical_media_key(candidate["row"])
        if not media_key or media_key in seen_media_keys:
            return
        component_key = norm(candidate["row"].get("specific_component")) or norm(candidate["row"].get("component_group"))
        date_key = clean(candidate["row"].get("captured_date")) or "unknown"
        if enforce_limits:
            if by_component[component_key] >= per_component_limit:
                return
            if by_date[date_key] >= per_date_limit:
                return
        seen_media_keys.add(media_key)
        by_component[component_key] += 1
        by_date[date_key] += 1
        selected.append(candidate)

    for candidate in candidates:
        try_add(candidate, enforce_limits=True)
    if len(selected) < max_images:
        for candidate in candidates:
            try_add(candidate, enforce_limits=False)
    return selected


def merge_candidate_lists(candidate_lists: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    seen_media_keys: set[str] = set()
    for candidate_list in candidate_lists:
        for candidate in candidate_list:
            media_key = canonical_media_key(candidate["row"])
            if not media_key or media_key in seen_media_keys:
                continue
            seen_media_keys.add(media_key)
            merged.append(candidate)
    return merged


def dedupe_payload_images(images: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen_keys: set[str] = set()
    for image in images:
        media_id = clean(image.get("media_id")).lower()
        path = clean(image.get("path")).lower()
        file_name = clean(image.get("file_name")).lower()
        canonical_key = (
            normalize_media_stem(media_id)
            or normalize_media_stem(path)
            or normalize_media_stem(file_name)
        )
        # Prefer canonical stem-based dedupe so Google Photos `_gp_*` mirrors
        # and exported suffix variants collapse to one payload.
        key = canonical_key or path or media_id
        if not key or key in seen_keys:
            continue
        seen_keys.add(key)
        deduped.append(image)
    return deduped


def parse_timestamp_parts(timestamp: str) -> tuple[str, str]:
    value = clean(timestamp)
    if "T" in value:
        date_part, time_part = value.split("T", 1)
        return date_part, time_part.replace("Z", "")
    if " " in value:
        date_part, time_part = value.split(" ", 1)
        return date_part, time_part
    return value, ""


def paint_whatsapp_component_bucket(evidence_bucket: str) -> tuple[str, str]:
    bucket = norm(evidence_bucket)
    if bucket == "prepared_for_send_out":
        return "whatsapp_paint_sendout_media", "removed_parts_cataloguing"
    if bucket == "returned_from_painter":
        return "whatsapp_paint_returned_media", "hardware_refinish"
    return "whatsapp_paint_progress_media", "reference_material"


def paint_reference_tokens_from_row(row: dict[str, str]) -> list[str]:
    hits = split_pipe(row.get("keyword_hits", ""))
    if hits:
        return hits[:8]
    context = norm(row.get("context_excerpt"))
    tokens: list[str] = []
    for token in ("paint", "primer", "panel", "door", "wing", "refinish", "send", "returned", "rust"):
        if token in context:
            tokens.append(token)
    return tokens[:8]


PAINT_WHATSAPP_REASON_SIGNALS: set[str] = {
    "send_context",
    "return_context",
    "progress_context",
}

PAINT_WHATSAPP_STRONG_KEYWORD_HITS: set[str] = {
    "paint",
    "repaint",
    "primer",
    "bodywork",
    "refinish",
    "rechromed",
    "sanding",
    "spray",
    "filler",
    "sealer",
    "rust",
}

PAINT_WHATSAPP_WEAK_KEYWORD_HITS: set[str] = {
    "panel",
    "door",
    "roof",
    "wing",
    "bonnet",
    "send",
    "sent",
    "return",
    "returned",
    "hardware",
}

PAINT_WHATSAPP_EXCLUDED_CONTEXT_PHRASES: tuple[str, ...] = (
    "cnic",
    "model town",
    "transfer of docs",
    "license plate",
    "licemse plate",
    "vin",
    "chassis number",
    "door wires",
    "fuse box",
    "temp gauge",
)

PAINT_WHATSAPP_STRONG_CONTEXT_WORDS: set[str] = {
    "paint",
    "repaint",
    "primer",
    "bodywork",
    "refinish",
    "rechromed",
    "sanding",
    "spray",
    "filler",
    "sealer",
    "rust",
    "painter",
}


def paint_whatsapp_row_is_relevant(row: dict[str, str]) -> bool:
    relative_path = clean(row.get("relative_path"))
    if not relative_path:
        return False

    media_type = norm(row.get("media_type"))
    if media_type not in {"photo", "video"}:
        return False

    reason = norm(row.get("classification_reason"))
    keyword_hits = [norm(token) for token in split_pipe(row.get("keyword_hits", ""))]
    keyword_hit_tokens = {token for token in keyword_hits if token}

    strong_keyword_hit = bool(keyword_hit_tokens & PAINT_WHATSAPP_STRONG_KEYWORD_HITS)
    weak_keyword_hit = bool(keyword_hit_tokens & PAINT_WHATSAPP_WEAK_KEYWORD_HITS)

    context = norm(row.get("context_excerpt"))
    context_words = set(re.findall(r"[a-z0-9]+", context))
    strong_context_hit = bool(context_words & PAINT_WHATSAPP_STRONG_CONTEXT_WORDS)
    has_excluded_context_phrase = any(
        phrase in context for phrase in PAINT_WHATSAPP_EXCLUDED_CONTEXT_PHRASES
    )

    if strong_keyword_hit:
        return True

    if strong_context_hit and not has_excluded_context_phrase:
        return True

    if reason in PAINT_WHATSAPP_REASON_SIGNALS and weak_keyword_hit and not has_excluded_context_phrase:
        return True

    return False


def build_paint_workstream_evidence_sets(
    photo_rows: list[dict[str, str]],
    reference_tokens: set[str],
    paint_queue_rows: list[dict[str, str]],
    paint_whatsapp_rows: list[dict[str, str]],
) -> dict[str, Any]:
    paint_stages = {"removed_parts_cataloguing", "hardware_refinish", "rust_assessment"}
    paint_component_groups = {"removable_panels", "body_exterior", "roof_and_gutters", "body_floor"}
    removed_specific = {
        "detached_body_panels_and_doors",
        "detached_doors_and_panels",
        "rear_hatch_inner_panel",
        "body_shell_with_doors_removed",
        "rear_side_opening",
    }
    returned_specific = {
        "refinished_hinges_brackets_and_trim",
        "refinished_seat_or_mount_bracket",
        "wiper_arm_or_linkage_hardware",
        "dashboard_fascia_trim",
    }

    local_candidates: list[dict[str, str]] = []
    for row in photo_rows:
        if not is_photo_row(row):
            continue
        stage = norm(row.get("stage"))
        component_group = norm(row.get("component_group"))
        specific_component = norm(row.get("specific_component"))

        include_row = False
        if stage in paint_stages:
            include_row = True
        elif component_group in paint_component_groups and stage in {"reference_material"}:
            include_row = True

        if include_row:
            local_candidates.append(row)

    local_candidates = sorted(
        local_candidates,
        key=lambda row: (
            clean(row.get("captured_date")),
            clean(row.get("captured_time")),
            clean(row.get("file_name")),
        ),
        reverse=True,
    )

    local_all_images = [image_payload(row, row_token_matches(row, reference_tokens)) for row in local_candidates]
    local_send_images = [
        image_payload(row, row_token_matches(row, reference_tokens))
        for row in local_candidates
        if norm(row.get("stage")) == "removed_parts_cataloguing"
        and (
            norm(row.get("specific_component")) in removed_specific
            or norm(row.get("component_group")) == "removable_panels"
        )
    ]
    local_returned_images = [
        image_payload(row, row_token_matches(row, reference_tokens))
        for row in local_candidates
        if norm(row.get("stage")) == "hardware_refinish"
        or norm(row.get("specific_component")) in returned_specific
    ]
    local_issue_images = [
        image_payload(row, row_token_matches(row, reference_tokens))
        for row in local_candidates
        if norm(row.get("stage")) == "rust_assessment"
        or "corrosion" in norm(row.get("observed_state"))
    ]
    local_progress_images = [
        image_payload(row, row_token_matches(row, reference_tokens))
        for row in local_candidates
        if norm(row.get("stage")) == "stripdown_cataloguing"
    ]

    queue_all_media: list[dict[str, Any]] = []
    queue_send_media: list[dict[str, Any]] = []
    queue_returned_media: list[dict[str, Any]] = []
    queue_issue_media: list[dict[str, Any]] = []
    queue_progress_media: list[dict[str, Any]] = []
    queue_progress_videos: list[dict[str, Any]] = []
    for row in paint_queue_rows:
        if not clean(row.get("relative_path")):
            continue
        media_type = norm(row.get("media_type"))
        if media_type not in {"photo", "video"}:
            continue
        evidence_bucket = norm(row.get("evidence_bucket"))
        component_group = norm(row.get("component_group"))
        stage = norm(row.get("stage"))
        if evidence_bucket == "in_progress_photo" and (
            component_group not in {"removable_panels", "body_exterior", "roof_and_gutters"}
            and stage != "hardware_refinish"
        ):
            continue
        if evidence_bucket == "in_progress_video" and (
            component_group not in {"removable_panels", "body_exterior", "roof_and_gutters", "documentation_reference"}
        ):
            continue
        payload = image_payload(row, row_token_matches(row, reference_tokens))
        queue_all_media.append(payload)

        if evidence_bucket == "prepared_for_send_out":
            queue_send_media.append(payload)
        elif evidence_bucket == "returned_from_painter":
            queue_returned_media.append(payload)
        elif evidence_bucket == "issue_tracking":
            queue_issue_media.append(payload)
        else:
            queue_progress_media.append(payload)

        if media_type == "video":
            queue_progress_videos.append(payload)

    whatsapp_send_images: list[dict[str, Any]] = []
    whatsapp_returned_images: list[dict[str, Any]] = []
    whatsapp_progress_images: list[dict[str, Any]] = []
    whatsapp_progress_videos: list[dict[str, Any]] = []
    for row in paint_whatsapp_rows:
        if not paint_whatsapp_row_is_relevant(row):
            continue
        media_type = norm(row.get("media_type"))
        if media_type not in {"photo", "video"}:
            continue
        evidence_bucket = clean(row.get("evidence_bucket"))
        specific_component, stage = paint_whatsapp_component_bucket(evidence_bucket)
        payload = whatsapp_media_image_payload(
            row,
            paint_reference_tokens_from_row(row),
            match_basis=f"paint_whatsapp_{norm(evidence_bucket) or 'unclassified'}",
            match_score=0,
            component_group="paint_refinish_whatsapp",
            specific_component=specific_component,
            stage=stage,
        )
        if media_type == "video":
            whatsapp_progress_videos.append(payload)
            continue
        bucket = norm(evidence_bucket)
        if bucket == "prepared_for_send_out":
            whatsapp_send_images.append(payload)
        elif bucket == "returned_from_painter":
            whatsapp_returned_images.append(payload)
        else:
            whatsapp_progress_images.append(payload)

    all_media = dedupe_payload_images(
        local_all_images
        + queue_all_media
        + whatsapp_send_images
        + whatsapp_returned_images
        + whatsapp_progress_images
        + whatsapp_progress_videos
    )
    sent_media = dedupe_payload_images(local_send_images + queue_send_media + whatsapp_send_images)
    returned_media = dedupe_payload_images(local_returned_images + queue_returned_media + whatsapp_returned_images)
    issue_media = dedupe_payload_images(local_issue_images + queue_issue_media)
    progress_media = dedupe_payload_images(local_progress_images + queue_progress_media + whatsapp_progress_images + whatsapp_progress_videos)
    progress_video_media = dedupe_payload_images(queue_progress_videos + whatsapp_progress_videos)

    evidence_sets: list[dict[str, Any]] = [
        {
            "key": "all_paint_media",
            "title": "All Paint Media",
            "description": "Complete paint/refinish media set (photos + videos) across local and WhatsApp sources.",
            "images": all_media,
        },
        {
            "key": "sent_to_painter",
            "title": "Sent To Painter",
            "description": "Media showing parts/panels detached and sent/prepared for painter batches.",
            "images": sent_media,
        },
        {
            "key": "returned_from_painter",
            "title": "Returned From Painter",
            "description": "Media showing refinished/returned parts and hardware after paint/refinish work.",
            "images": returned_media,
        },
        {
            "key": "paint_issue_tracking",
            "title": "Paint Issues / Defects",
            "description": "Issue-focused media (rust/corrosion/problem areas) used to track paint-prep defects.",
            "images": issue_media,
        },
        {
            "key": "paint_progress_media",
            "title": "Paint Progress Media",
            "description": "In-progress painter/bodywork media while work is underway.",
            "images": progress_media,
        },
    ]
    if progress_video_media:
        evidence_sets.append(
            {
                "key": "paint_progress_videos",
                "title": "Paint Progress Videos",
                "description": "WhatsApp video references captured during painter/bodywork progress.",
                "images": progress_video_media,
            }
        )
    evidence_sets = [set_row for set_row in evidence_sets if set_row["images"]]

    return {
        "primary_images": all_media,
        "evidence_sets": evidence_sets,
    }


def build_workstream_evidence_sets(
    workstream_id: str,
    photo_rows: list[dict[str, str]],
    reference_tokens: set[str],
    paint_queue_rows: list[dict[str, str]],
    paint_whatsapp_rows: list[dict[str, str]],
) -> dict[str, Any]:
    if workstream_id == "interior_controls":
        dashboard_rows = [
            row
            for row in photo_rows
            if is_photo_row(row) and is_dashboard_workstream_photo(row)
        ]
        dashboard_rows_sorted = sorted(
            dashboard_rows,
            key=lambda row: (
                clean(row.get("captured_date")),
                clean(row.get("captured_time")),
                clean(row.get("file_name")),
            ),
            reverse=True,
        )
        dashboard_images = dedupe_payload_images([
            image_payload(row, row_token_matches(row, reference_tokens))
            for row in dashboard_rows_sorted
        ])
        evidence_sets = [
            {
                "key": "all_dashboard_images",
                "title": "All Dashboard Images",
                "description": "Complete dashboard image set from the imported photo inventory.",
                "images": dashboard_images,
            }
        ]
        return {
            "primary_images": dashboard_images,
            "evidence_sets": evidence_sets,
        }

    if workstream_id == "paint_refinish":
        return build_paint_workstream_evidence_sets(
            photo_rows,
            reference_tokens,
            paint_queue_rows,
            paint_whatsapp_rows,
        )

    if workstream_id == "replacement_pipes":
        all_pipe_rows = rows_for_media_ids(photo_rows, REPLACEMENT_PIPE_CURATED_MEDIA_IDS)
        made_to_order_rows = rows_for_media_ids(photo_rows, REPLACEMENT_PIPE_MADE_TO_ORDER_MEDIA_IDS)
        installed_location_rows = rows_for_media_ids(photo_rows, REPLACEMENT_PIPE_INSTALLED_LOCATION_MEDIA_IDS)
        sample_sorting_rows = rows_for_media_ids(photo_rows, REPLACEMENT_PIPE_SAMPLE_SORTING_MEDIA_IDS)

        primary_images = dedupe_payload_images(
            [image_payload(row, row_token_matches(row, reference_tokens)) for row in all_pipe_rows]
        )
        evidence_sets = [
            {
                "key": "curated_pipe_photos",
                "title": "Curated Pipe Photos",
                "description": "Only photos that show replacement-pipe locations or the made-to-order pipe sample; body rubbers and generic mechanical images are intentionally excluded.",
                "images": primary_images,
            },
            {
                "key": "made_to_order_coolant_pipe",
                "title": "Made-To-Order Coolant Pipe Sample",
                "description": "Selected May 2 photos for recreating the formed metal coolant/radiator pipe from the physical sample.",
                "images": dedupe_payload_images(
                    [image_payload(row, row_token_matches(row, reference_tokens)) for row in made_to_order_rows]
                ),
            },
            {
                "key": "installed_pipe_locations",
                "title": "Installed Pipe Locations",
                "description": "Current vehicle locations with visible hoses, hard lines, or hydraulic line routing that need measurement close-ups.",
                "images": dedupe_payload_images(
                    [image_payload(row, row_token_matches(row, reference_tokens)) for row in installed_location_rows]
                ),
            },
            {
                "key": "sample_sorting_photos",
                "title": "Loose Pipe Sample Sorting",
                "description": "Loose pipe/hose sample evidence that must be assigned to a vehicle location and measured before acquisition or fabrication.",
                "images": dedupe_payload_images(
                    [image_payload(row, row_token_matches(row, reference_tokens)) for row in sample_sorting_rows]
                ),
            },
        ]
        return {
            "primary_images": primary_images,
            "evidence_sets": evidence_sets,
        }

    profile = WORKSTREAM_IMAGE_PROFILES.get(workstream_id, DEFAULT_IMAGE_PROFILE)
    stripdown_paint_owned_media_ids: set[str] = set()
    if workstream_id == "stripdown_cataloguing":
        paint_owned_component_groups = {
            "removable_panels",
            "body_exterior",
            "roof_and_gutters",
            "body_floor",
            "documentation_reference",
        }
        stripdown_paint_owned_media_ids = {
            clean(row.get("media_id"))
            for row in paint_queue_rows
            if clean(row.get("media_id"))
            and norm(row.get("component_group")) in paint_owned_component_groups
        }
    min_image_score = WORKSTREAM_MIN_IMAGE_SCORE.get(workstream_id, DEFAULT_WORKSTREAM_MIN_IMAGE_SCORE)
    min_keyword_hits = WORKSTREAM_MIN_KEYWORD_HITS.get(workstream_id, DEFAULT_WORKSTREAM_MIN_KEYWORD_HITS)
    scored: list[dict[str, Any]] = []

    for row in photo_rows:
        if not is_photo_row(row):
            continue
        if stripdown_paint_owned_media_ids and clean(row.get("media_id")) in stripdown_paint_owned_media_ids:
            continue
        stage_match = norm(row.get("stage")) in profile["stages"]
        component_match = norm(row.get("component_group")) in profile["component_groups"]
        text_blob = row_text_blob(row)
        if workstream_row_is_excluded(workstream_id, row, text_blob):
            continue
        keyword_hits = sum(1 for keyword in profile["keywords"] if keyword in text_blob)
        base_score = image_score(row, profile)
        token_matches = row_token_matches(row, reference_tokens)
        if not stage_match:
            continue
        if keyword_hits < min_keyword_hits and not token_matches:
            continue
        if not component_match and keyword_hits < 2:
            continue
        if base_score < min_image_score and not token_matches:
            continue
        if base_score <= 0:
            continue

        score = base_score + (len(token_matches) * 2)
        scored.append(
            {
                "row": row,
                "base_score": base_score,
                "score": score,
                "token_matches": token_matches,
                "sort_score_key": (
                    score,
                    clean(row.get("captured_date")),
                    clean(row.get("captured_time")),
                    clean(row.get("file_name")),
                ),
                "sort_recent_key": (
                    clean(row.get("captured_date")),
                    clean(row.get("captured_time")),
                    score,
                    clean(row.get("file_name")),
                ),
            }
        )

    # Fallback only for broad profiles where strict filtering yields no rows.
    allow_stage_component_fallback = WORKSTREAM_ALLOW_STAGE_COMPONENT_FALLBACK.get(workstream_id, False)
    if not scored and allow_stage_component_fallback:
        for row in photo_rows:
            if not is_photo_row(row):
                continue
            if stripdown_paint_owned_media_ids and clean(row.get("media_id")) in stripdown_paint_owned_media_ids:
                continue
            if norm(row.get("stage")) not in profile["stages"]:
                continue
            if norm(row.get("component_group")) not in profile["component_groups"]:
                continue
            text_blob = row_text_blob(row)
            if workstream_row_is_excluded(workstream_id, row, text_blob):
                continue
            base_score = image_score(row, profile)
            if base_score <= 0:
                continue
            token_matches = row_token_matches(row, reference_tokens)
            score = base_score + (len(token_matches) * 2)
            scored.append(
                {
                    "row": row,
                    "base_score": base_score,
                    "score": score,
                    "token_matches": token_matches,
                    "sort_score_key": (
                        score,
                        clean(row.get("captured_date")),
                        clean(row.get("captured_time")),
                        clean(row.get("file_name")),
                    ),
                    "sort_recent_key": (
                        clean(row.get("captured_date")),
                        clean(row.get("captured_time")),
                        score,
                        clean(row.get("file_name")),
                    ),
                }
            )

    scored_by_score = sorted(scored, key=lambda candidate: candidate["sort_score_key"], reverse=True)
    scored_by_recent = sorted(scored, key=lambda candidate: candidate["sort_recent_key"], reverse=True)

    reference_candidates = [candidate for candidate in scored_by_score if candidate["token_matches"]]
    mapped_candidates = [candidate for candidate in scored_by_score if candidate["base_score"] >= max(18, min_image_score)]
    if not mapped_candidates:
        mapped_candidates = [candidate for candidate in scored_by_score if candidate["base_score"] > 0]
    recent_candidates = [candidate for candidate in scored_by_recent if candidate["base_score"] >= min_image_score]

    selected_reference = reference_candidates
    selected_mapped = mapped_candidates
    selected_recent = recent_candidates

    merged_primary = merge_candidate_lists([selected_reference, selected_mapped, selected_recent])
    selected_primary = merged_primary

    primary_images = dedupe_payload_images(
        [image_payload(candidate["row"], candidate["token_matches"]) for candidate in selected_primary]
    )
    evidence_sets: list[dict[str, Any]] = [
        {
            "key": "primary",
            "title": "Primary Evidence Set",
            "description": "Best-matched photos for this workstream from component/stage mapping and evidence references.",
            "images": primary_images,
        },
    ]

    if workstream_id == "chassis_fixing":
        may1_images = dedupe_payload_images(
            [image_payload(row, row_token_matches(row, reference_tokens)) for row in may1_chassis_status_rows(photo_rows)]
        )
        if may1_images:
            evidence_sets.insert(
                0,
                {
                    "key": "may1_chassis_status",
                    "title": "May 1 Chassis Status - All Images",
                    "description": "Complete May 1 chassis fixing set after wire brushing; use this before primer decisions.",
                    "images": may1_images,
                },
            )

    if workstream_id == "chassis_rubbers":
        rubber_recreation_images = dedupe_payload_images(
            [
                image_payload(row, row_token_matches(row, reference_tokens))
                for row in rubber_recreation_candidate_rows(photo_rows)
            ]
        )
        if rubber_recreation_images:
            evidence_sets.insert(
                0,
                {
                    "key": "rubber_recreation_candidates_20260502",
                    "title": "Rubber Recreation Candidate Photos - May 2",
                    "description": "Starter review collection for recreating body-mount/front-support rubbers, sleeves, shims, and sample stacks.",
                    "images": rubber_recreation_images,
                },
            )

    if workstream_id == "brake_system":
        rear_brake_images = dedupe_payload_images(
            [
                image_payload(row, row_token_matches(row, reference_tokens))
                for row in rows_for_media_ids(photo_rows, REAR_BRAKE_CABLE_LINE_MEDIA_IDS)
            ]
        )
        if rear_brake_images:
            evidence_sets.insert(
                0,
                {
                    "key": "rear_brake_cables_lines",
                    "title": "Rear Brake Cables And Lines",
                    "description": "Rear axle evidence for drum brakes, parking-brake cable/linkage, axle hard lines, center flex hose, and retaining clips.",
                    "images": rear_brake_images,
                },
            )

    if workstream_id == "mechanical_baseline":
        may1_engine_images = dedupe_payload_images(
            [image_payload(row, row_token_matches(row, reference_tokens)) for row in may1_engine_cleaning_rows(photo_rows)]
        )
        if may1_engine_images:
            evidence_sets.insert(
                0,
                {
                    "key": "may1_engine_cleaning",
                    "title": "May 1 Engine And Powertrain Cleaning Baseline",
                    "description": "Complete May 1 engine/gearbox/transfer cleaning baseline before degreasing and leak inspection.",
                    "images": may1_engine_images,
                },
            )

    return {
        "primary_images": primary_images,
        "evidence_sets": evidence_sets,
    }


def collect_workstreams(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_id = {clean(row.get("workstream_id")): row for row in rows}
    selected_ids: list[str] = [ws_id for ws_id in PRIMARY_WORKSTREAM_IDS if ws_id in by_id]

    if len(selected_ids) < 5:
        for row in rows:
            ws_id = clean(row.get("workstream_id"))
            if ws_id in selected_ids:
                continue
            if ws_id in {"site_setup", "legal_admin", "optional_upgrades"}:
                continue
            status = norm(row.get("current_status"))
            if status in {"in_progress", "queued", "blocked"}:
                selected_ids.append(ws_id)
            if len(selected_ids) >= 5:
                break

    selected_rows = [by_id[ws_id] for ws_id in selected_ids]
    if "interior_controls" not in {clean(row.get("workstream_id")) for row in selected_rows}:
        electrical_status = norm(by_id.get("electrical_reset", {}).get("current_status", ""))
        interior_status = norm(by_id.get("interior_weatherproofing", {}).get("current_status", ""))
        if electrical_status in {"in_progress", "queued", "blocked"} or interior_status in {"in_progress", "queued", "blocked"}:
            synthetic_status = "in_progress" if electrical_status == "in_progress" else ("queued" if interior_status in {"queued", "blocked"} else "queued")
            selected_rows.insert(
                3,
                {
                    "workstream_id": "interior_controls",
                    "phase": "07a_interior_controls",
                    "current_status": synthetic_status,
                    "priority": "high",
                    "primary_location": "home",
                    "owner_mode": "owner_led",
                    "depends_on": "electrical_reset|stripdown_cataloguing",
                    "next_action": "Track dash switches and interior controls as a dedicated stream; map function, mounting, and wiring integration.",
                    "exit_gate": "Interior controls are mounted, wired, labeled, and function-tested with evidence photos.",
                    "evidence_source": "photo_inventory|20260421_192813_gp_0jvYAo8g|20260421_194401_gp_1dY3fLdw",
                    "notes": "Dedicated interior-controls category to prevent dash switch/control evidence from being mixed into body-lift photos.",
                },
            )
    return selected_rows


def collect_workstream_reference_tokens(
    workstream_row: dict[str, str],
    linked_packages: list[dict[str, str]],
    jobs: list[dict[str, str]],
    issues: list[dict[str, str]],
) -> set[str]:
    token_sources = [workstream_row.get("evidence_source", "")]
    token_sources.extend(package.get("evidence_signal", "") for package in linked_packages)
    token_sources.extend(job.get("evidence_ref", "") for job in jobs)
    token_sources.extend(issue.get("evidence_ref", "") for issue in issues)
    return extract_reference_tokens(token_sources)


def is_closed_status(status: str) -> bool:
    return norm(status) in {"closed", "completed", "received", "installed", "reinstalled"}


DASHBOARD_PART_SIGNAL_TOKENS: tuple[str, ...] = (
    "dashboard",
    "dash",
    "switch",
    "toggle",
    "cutoff",
    "ignition",
    "selector",
    "knob",
    "button",
    "control",
    "fascia",
)


def is_dashboard_related_part_row(row: dict[str, str]) -> bool:
    workstream_key = norm(row.get("workstream"))
    if workstream_key == "interior_controls":
        return True
    if workstream_key not in {"electrical_reset", "interior_weatherproofing"}:
        return False

    text_blob = " ".join(
        [
            norm(row.get("item")),
            norm(row.get("category")),
            norm(row.get("notes")),
            norm(row.get("evidence_ref")),
        ]
    )
    return any(token in text_blob for token in DASHBOARD_PART_SIGNAL_TOKENS)


def split_legacy_steering_brakes_workstream(
    workstream: str,
    *,
    category: str = "",
    item: str = "",
    notes: str = "",
) -> str:
    workstream_value = clean(workstream)
    workstream_key = norm(workstream_value)
    category_key = norm(category)
    text_blob = " ".join([category_key, norm(item), norm(notes)])

    def text_contains_term(term: str) -> bool:
        term_key = norm(term)
        if not term_key:
            return False
        variants = {term_key, term_key.replace("_", " "), term_key.replace("-", " ")}
        for variant in variants:
            if " " in variant:
                if variant in text_blob.replace("_", " ").replace("-", " "):
                    return True
            elif re.search(rf"(?<![a-z0-9]){re.escape(variant)}(?![a-z0-9])", text_blob):
                return True
        return False

    if workstream_key == "body_chassis":
        if category_key == "body_mounts" or any(
            text_contains_term(token)
            for token in ("body mount", "body_mount", "rubber kit", "shim", "sleeve", "isolator")
        ):
            return "chassis_rubbers"

    if workstream_key != "steering_brakes_suspension":
        return workstream_value

    if category_key == "brakes" or any(
        text_contains_term(token)
        for token in ("brake", "disc", "drum", "caliper", "master", "cylinder", "hydraulic", "bleed")
    ):
        return "brake_system"

    if category_key == "suspension" or any(
        text_contains_term(token)
        for token in ("suspension", "leaf", "shackle", "shock", "spring", "bush", "u-bolt", "ubolt", "ironman", "ome")
    ):
        return "suspension_upgrade"

    if category_key == "steering" or any(
        text_contains_term(token)
        for token in ("steering", "eps", "vitz", "column", "u-joint", "ujoint", "assist", "power steering")
    ):
        return "eps_vitz_upgrade"

    # Legacy umbrella rows were predominantly suspension planning.
    return "suspension_upgrade"


def template_step_status(current_status: str, index: int) -> str:
    key = norm(current_status)
    if key in {"completed", "closed"}:
        return "completed"
    if key == "blocked":
        return "blocked" if index == 0 else "queued"
    if key in {"queued", "backlog"}:
        return "queued"
    return "in_progress" if index == 0 else "queued"


def workstream_steps(
    workstream_row: dict[str, str],
    linked_packages: list[dict[str, str]],
    jobs: list[dict[str, str]],
    issues: list[dict[str, str]],
    part_rows_for_workstream: list[dict[str, str]],
) -> list[dict[str, str]]:
    steps: list[dict[str, str]] = []

    current_status = clean(workstream_row.get("current_status"))
    next_action = clean(workstream_row.get("next_action"))
    exit_gate = clean(workstream_row.get("exit_gate"))

    steps.append(
        {
            "label": "Execute current workstream action",
            "status": current_status,
            "detail": next_action,
        }
    )

    template_steps = WORKSTREAM_REQUIRED_SEQUENCE.get(clean(workstream_row.get("workstream_id")), [])
    for index, (label, detail) in enumerate(template_steps):
        steps.append(
            {
                "label": label,
                "status": template_step_status(current_status, index),
                "detail": detail,
            }
        )

    for package in linked_packages:
        package_id = clean(package.get("work_package_id"))
        package_title = clean(package.get("title"))
        objective = clean(package.get("objective"))
        blocker = clean(package.get("blocker_summary"))
        package_gate = clean(package.get("gate_to_close"))
        procurement = clean(package.get("key_procurement_actions"))
        detail = objective
        if blocker:
            detail += f" Blocker: {blocker}"
        if procurement:
            detail += f" Procurement: {procurement}"
        if package_gate:
            detail += f" Gate: {package_gate}"
        steps.append(
            {
                "label": f"{package_id} · {package_title}",
                "status": clean(package.get("current_state")),
                "detail": detail,
            }
        )

    if issues:
        for issue in issues:
            issue_id = humanize_token(issue.get("component_job_id", "issue"))
            planned_action = clean(issue.get("planned_action"))
            issue_notes = clean(issue.get("notes"))
            issue_detail = planned_action
            if issue_notes:
                issue_detail += f" Notes: {issue_notes}"
            steps.append(
                {
                    "label": f"Issue Check · {issue_id}",
                    "status": clean(issue.get("current_status")),
                    "detail": issue_detail,
                }
            )
    else:
        steps.append(
            {
                "label": "Issue checks",
                "status": "completed",
                "detail": "No issue-specific checks are recorded for this workstream.",
            }
        )

    open_jobs = [job for job in jobs if not is_closed_status(clean(job.get("current_status")))]
    sorted_open_jobs = sorted(
        open_jobs,
        key=lambda job: (clean(job.get("current_status")), clean(job.get("component_job_id"))),
    )
    for job in sorted_open_jobs[:12]:
        job_id = humanize_token(job.get("component_job_id", "job"))
        planned_action = clean(job.get("planned_action"))
        job_notes = clean(job.get("notes"))
        job_detail = planned_action
        if job_notes:
            job_detail += f" Notes: {job_notes}"
        steps.append(
            {
                "label": f"Component Task · {job_id}",
                "status": clean(job.get("current_status")),
                "detail": job_detail,
            }
        )
    if len(sorted_open_jobs) > 12:
        remaining = len(sorted_open_jobs) - 12
        steps.append(
            {
                "label": "Additional open component tasks",
                "status": "in_progress",
                "detail": f"{remaining} more open component rows are linked to this workstream.",
            }
        )

    if part_rows_for_workstream:
        open_parts = [
            row
            for row in part_rows_for_workstream
            if not is_closed_status(clean(row.get("status")))
            and norm(row.get("procurement_stage")) not in {"received", "completed"}
        ]
        stage_counts = Counter(norm(row.get("procurement_stage")) or "unknown" for row in open_parts)
        purchase_ready_count = stage_counts.get("purchase_ready", 0)
        ordered_count = stage_counts.get("ordered_pending_delivery", 0)
        needs_confirmation_count = stage_counts.get("needs_confirmation", 0) + stage_counts.get("received_candidate", 0)

        steps.append(
            {
                "label": "Procurement · release purchase-ready rows",
                "status": "in_progress" if purchase_ready_count > 0 else "completed",
                "detail": f"{purchase_ready_count} part rows still require price confirmation/order placement.",
            }
        )
        steps.append(
            {
                "label": "Procurement · track in-flight deliveries",
                "status": "in_progress" if ordered_count > 0 else "completed",
                "detail": f"{ordered_count} part rows are ordered and awaiting delivery.",
            }
        )
        steps.append(
            {
                "label": "Procurement · resolve ambiguous stock/receipt rows",
                "status": "in_progress" if needs_confirmation_count > 0 else "completed",
                "detail": f"{needs_confirmation_count} rows still need confirmation before closeout.",
            }
        )

    package_states = {norm(row.get("current_state")) for row in linked_packages}
    if not linked_packages:
        package_status = "queued"
        package_detail = "No linked package rows found"
    elif package_states.issubset({"completed", "closed"}):
        package_status = "completed"
        package_detail = "All linked packages are closed"
    elif "blocked" in package_states:
        package_status = "blocked"
        package_detail = "At least one linked package is blocked"
    elif "in_progress" in package_states:
        package_status = "in_progress"
        package_detail = "Linked package execution is active"
    else:
        package_status = "queued"
        package_detail = "Linked package execution is queued"

    steps.append(
        {
            "label": "Close workstream exit gate",
            "status": package_status,
            "detail": f"{package_detail}. Exit gate: {exit_gate}",
        }
    )
    return steps


def parse_numeric_text(value: str) -> str:
    text = clean(value).replace(",", "")
    if not text:
        return ""
    if re.fullmatch(r"-?\d+(\.\d+)?", text):
        return text
    return ""


def workbook_flag_value(value: str) -> str:
    lowered = norm(value)
    if not lowered:
        return "unknown"
    if "cancel" in lowered:
        return "cancelled"
    if lowered in {"y", "yes", "true", "received"}:
        return "yes"
    if lowered in {"n", "no", "false"}:
        return "no"
    if lowered in {"cod", "paid"}:
        return "yes"
    if "included" in lowered and "total" in lowered:
        return "yes"
    return "unknown"


def supply_type_from_expense(row: dict[str, str]) -> str:
    bucket = norm(row.get("bucket"))
    category = norm(row.get("category"))
    item = norm(row.get("item"))
    if bucket == "tools":
        return "tool"
    if bucket == "parts":
        substance_keywords = {
            "primer",
            "sealer",
            "wax",
            "grease",
            "cleaner",
            "degreaser",
            "rust",
            "liner",
            "oil",
            "lubricant",
            "converter",
            "threadlocker",
            "contact cleaner",
            "evapo",
            "cavity",
            "anti seize",
            "tape",
        }
        if category in {"bodywork"}:
            return "substance"
        if any(keyword in item for keyword in substance_keywords):
            return "substance"
        return "part"
    return "part"


def infer_inventory_group(
    *,
    supply_type: str,
    item: str,
    workstream: str,
    category: str = "",
    inventory_token: str = "",
    notes: str = "",
) -> str:
    supply_type_key = norm(supply_type)
    if supply_type_key == "tool":
        return "tools"
    if supply_type_key == "substance":
        return "substances"

    workstream_key = norm(workstream)
    category_key = norm(category)
    inventory_key = norm(inventory_token)
    text_blob = " ".join(
        [
            norm(item),
            workstream_key,
            category_key,
            inventory_key,
            norm(notes),
        ]
    )

    electrical_workstreams = {"electrical_reset", "interior_controls"}
    electrical_categories = {"electrical", "wiring", "electrical_accessories"}
    electrical_keywords = (
        "electrical",
        "wire",
        "wiring",
        "connector",
        "relay",
        "switch",
        "loom",
        "fuse",
        "grommet",
        "battery",
        "alternator",
        "headlight",
    )
    if (
        workstream_key in electrical_workstreams
        or category_key in electrical_categories
        or "wiring" in inventory_key
        or any(keyword in text_blob for keyword in electrical_keywords)
    ):
        return "electrical"

    mechanical_workstreams = {
        "mechanical_baseline",
        "replacement_pipes",
        "chassis_rubbers",
        "brake_system",
        "eps_vitz_upgrade",
        "suspension_upgrade",
    }
    mechanical_categories = {
        "engine_service",
        "cooling",
        "fuel_system",
        "ignition",
        "engine_front",
        "suspension",
        "steering",
        "brakes",
        "body_mounts",
        "mounts",
        "clutch",
    }
    mechanical_keywords = (
        "engine",
        "cooling",
        "fuel",
        "spark",
        "radiator",
        "thermostat",
        "suspension",
        "leaf",
        "shock",
        "steering",
        "brake",
        "clutch",
        "bearing",
        "filter",
        "oil",
    )
    if (
        workstream_key in mechanical_workstreams
        or category_key in mechanical_categories
        or any(keyword in text_blob for keyword in mechanical_keywords)
    ):
        return "mechanical"

    return "parts"


def expense_supply_status_group(row: dict[str, str]) -> str:
    status = norm(row.get("status"))
    stage = norm(row.get("procurement_stage"))
    payment = norm(row.get("payment_status"))
    delivery = norm(row.get("delivery_status"))

    if status in {"received", "installed", "credited", "completed"} or stage in {"received", "completed"} or delivery in {
        "received",
        "installed",
        "completed",
    }:
        return "previously"

    if stage in {"ordered_pending_delivery", "needs_confirmation", "received_candidate", "researching"}:
        return "in_process"
    if delivery in {"pending_delivery", "needs_confirmation", "researching"}:
        return "in_process"
    if payment in {"paid", "cod"}:
        return "in_process"
    if status in {"ordered", "researching"}:
        return "in_process"

    return "still_required"


def workbook_supply_status_group(received_value: str, paid_value: str, status_token: str, notes_value: str) -> str:
    received_flag = workbook_flag_value(received_value)
    paid_flag = workbook_flag_value(paid_value)
    status_blob = " ".join([norm(status_token), norm(notes_value)])
    if any(
        token in status_blob
        for token in (
            "not ordered",
            "no order",
            "not_procured",
            "not procured",
            "no confirmed order",
            "not_required",
        )
    ):
        return "still_required"
    if received_flag == "yes":
        return "previously"
    if paid_flag == "yes":
        return "in_process"
    if any(
        token in status_blob
        for token in (
            "ordered",
            "in_flight",
            "in-flight",
            "pending_delivery",
            "awaiting",
            "track_in_flight",
            "track_delivery",
            "shipped",
            "sent",
            "transit",
            "needs_confirmation",
        )
    ):
        return "in_process"
    if received_flag == "cancelled" or paid_flag == "cancelled" or "cancel" in status_blob:
        return "still_required"
    return "still_required"


def load_workbook_supply_rows(path: Path, supply_type: str, source_name: str) -> list[dict[str, str]]:
    if not path.exists():
        return []
    rows = load_csv(path)
    normalized_rows: list[dict[str, str]] = []
    for row in rows:
        item = clean(row.get("col_1"))
        if not item or norm(item) == "item":
            continue
        if norm(item) in {"x", "labels", "jumnp leads", "jacks and stands"}:
            continue
        marker_blob = " ".join(
            [
                norm(row.get("col_6")),
                norm(row.get("col_7")),
                norm(row.get("col_8")),
                norm(row.get("col_9")),
                norm(row.get("col_10")),
                norm(row.get("col_11")),
                norm(row.get("col_12")),
            ]
        )
        if any(token in marker_blob for token in ("section_header", "duplicate", "not_required")):
            continue

        amount = parse_numeric_text(clean(row.get("col_2")))
        vendor = clean(row.get("col_3"))
        received = clean(row.get("col_4"))
        paid = clean(row.get("col_5"))
        status_token = first_non_empty(row, ["col_11", "col_6"])
        status_note = first_non_empty(row, ["col_12", "col_7"])
        inventory_token = first_non_empty(row, ["col_9", "col_8", "col_10"])
        status_group = workbook_supply_status_group(received, paid, status_token, status_note)
        normalized_rows.append(
            {
                "source": source_name,
                "source_ref": f"{source_name}#row_{clean(row.get('excel_row'))}",
                "supply_type": supply_type,
                "inventory_group": infer_inventory_group(
                    supply_type=supply_type,
                    item=item,
                    workstream="",
                    category=inventory_token,
                    inventory_token=inventory_token,
                    notes=status_note or status_token,
                ),
                "item": item,
                "vendor": vendor,
                "amount": amount,
                "currency": "PKR",
                "workstream": "",
                "status_group": status_group,
                "status_detail": "received" if status_group == "previously" else ("ordered_or_paid" if status_group == "in_process" else "needs_buy_or_check"),
                "procurement_stage": "",
                "payment_status": paid,
                "delivery_status": received,
                "evidence_ref": "",
                "notes": status_note or status_token,
            }
        )
    return normalized_rows


def build_supplies_inventory(expense_rows: list[dict[str, str]]) -> dict[str, Any]:
    expense_supply_rows: list[dict[str, str]] = []
    for row in expense_rows:
        bucket = norm(row.get("bucket"))
        if bucket not in {"parts", "tools"}:
            continue
        if norm(row.get("status")) == "cancelled" or norm(row.get("delivery_status")) == "not_required":
            continue
        supply_type = supply_type_from_expense(row)
        mapped_workstream = split_legacy_steering_brakes_workstream(
            clean(row.get("workstream")),
            category=clean(row.get("category")),
            item=clean(row.get("item")),
            notes=clean(row.get("notes")),
        )
        expense_supply_rows.append(
            {
                "source": "expenses",
                "source_ref": clean(row.get("entry_id")),
                "supply_type": supply_type,
                "inventory_group": infer_inventory_group(
                    supply_type=supply_type,
                    item=clean(row.get("item")),
                    workstream=mapped_workstream,
                    category=clean(row.get("category")),
                    notes=clean(row.get("notes")),
                ),
                "item": clean(row.get("item")),
                "vendor": clean(row.get("company")),
                "amount": clean(row.get("amount")),
                "currency": clean(row.get("currency")) or "PKR",
                "workstream": mapped_workstream,
                "status_group": expense_supply_status_group(row),
                "status_detail": clean(row.get("status")),
                "procurement_stage": clean(row.get("procurement_stage")),
                "payment_status": clean(row.get("payment_status")),
                "delivery_status": clean(row.get("delivery_status")),
                "evidence_ref": clean(row.get("evidence_ref")),
                "notes": clean(row.get("notes")),
            }
        )

    workbook_rows = []
    workbook_rows.extend(load_workbook_supply_rows(WORKBOOK_TOOLS_PATH, "tool", "workbook_tools"))
    workbook_rows.extend(load_workbook_supply_rows(WORKBOOK_PARTS_PATH, "part", "workbook_parts"))
    workbook_rows.extend(load_workbook_supply_rows(WORKBOOK_SUBSTANCES_PATH, "substance", "workbook_substances"))

    all_rows = expense_supply_rows + workbook_rows
    all_rows = [row for row in all_rows if clean(row.get("item"))]

    counts_by_type_status: dict[tuple[str, str], int] = Counter(
        (row["supply_type"], row["status_group"]) for row in all_rows
    )
    summary_by_type: list[dict[str, Any]] = []
    for supply_type in ("tool", "substance", "part"):
        summary_by_type.append(
            {
                "supply_type": supply_type,
                "previously": counts_by_type_status.get((supply_type, "previously"), 0),
                "in_process": counts_by_type_status.get((supply_type, "in_process"), 0),
                "still_required": counts_by_type_status.get((supply_type, "still_required"), 0),
                "total": sum(counts_by_type_status.get((supply_type, status), 0) for status in SUPPLY_STATUS_ORDER),
            }
        )

    rows_by_status: dict[str, list[dict[str, str]]] = {}
    for status_group in SUPPLY_STATUS_ORDER:
        rows_by_status[status_group] = sorted(
            [row for row in all_rows if row.get("status_group") == status_group],
            key=lambda row: (row.get("supply_type", ""), row.get("workstream", ""), row.get("item", "")),
        )

    return {
        "summary_by_type": summary_by_type,
        "rows_by_status": rows_by_status,
        "inventory_groups": list(INVENTORY_GROUP_ORDER),
        "all_rows": sorted(
            all_rows,
            key=lambda row: (row.get("status_group", ""), row.get("inventory_group", ""), row.get("supply_type", ""), row.get("item", "")),
        ),
    }


SEARCH_STOPWORDS: set[str] = {
    "with",
    "without",
    "pack",
    "piece",
    "set",
    "kit",
    "for",
    "from",
    "and",
    "the",
    "plus",
    "inch",
    "mm",
    "pcs",
}

GENERIC_INVENTORY_MATCH_TOKENS: set[str] = {
    "additional",
    "baseline",
    "driver",
    "electrical",
    "firewall",
    "front",
    "large",
    "left",
    "medium",
    "only",
    "part",
    "parts",
    "rear",
    "reference",
    "right",
    "rubber",
    "seal",
    "small",
    "through",
    "pass",
    "wire",
    "wiring",
}


def search_tokens(values: list[str], max_tokens: int = 16) -> list[str]:
    tokens: list[str] = []
    seen: set[str] = set()
    for value in values:
        for token in re.findall(r"[a-z0-9]{3,}", norm(value)):
            if token in SEARCH_STOPWORDS:
                continue
            if token in seen:
                continue
            seen.add(token)
            tokens.append(token)
            if len(tokens) >= max_tokens:
                return tokens
    return tokens


def extract_inventory_reference_tokens(values: list[str]) -> set[str]:
    tokens = set(extract_reference_tokens(values))
    for value in values:
        text = clean(value)
        if not text:
            continue
        for raw_token in re.split(r"[|,\s]+", text):
            token = raw_token.strip().strip("()[]{}")
            if not token:
                continue
            lowered = token.lower()
            if lowered.endswith((".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov", ".heic", ".gif")):
                lowered = lowered.rsplit(".", 1)[0]
            if not lowered:
                continue
            if lowered.startswith(("user_plan_", "user_update_", "docs_", "repo_control", "photo_inventory")):
                continue
            if len(lowered) >= 6 and (any(ch.isdigit() for ch in lowered) or "_" in lowered or "-" in lowered):
                tokens.add(lowered)
            for prefix in (
                "photo_",
                "gmail_order_",
                "gmail_msg_",
                "user_image_",
                "workbook_parts_",
                "workbook_tools_",
                "workbook_substances_",
            ):
                if lowered.startswith(prefix) and len(lowered) > len(prefix) + 3:
                    tokens.add(lowered[len(prefix) :])
            row_match = re.search(r"(?:^|_)row[_-]?(\d{1,5})", lowered)
            if row_match:
                row_number = row_match.group(1)
                tokens.add(f"row_{row_number}")
                tokens.add(row_number)
            for number in re.findall(r"\d{4,}", lowered):
                tokens.add(number)
    return {token for token in tokens if token}


LOW_SIGNAL_INVENTORY_REFERENCE_TOKENS: set[str] = {
    "photo",
    "photos",
    "image",
    "images",
    "screenshot",
    "inventory",
    "reference",
    "workstream",
    "docs",
    "user",
}


def inventory_reference_token_is_low_signal(token: str) -> bool:
    value = norm(token)
    if not value:
        return True
    if value in LOW_SIGNAL_INVENTORY_REFERENCE_TOKENS:
        return True
    if value.isdigit() and len(value) == 4 and value.startswith(("19", "20")):
        return True
    return False


CHASSIS_RUBBERS_IMAGE_SIGNAL_TOKENS: tuple[str, ...] = (
    "body_mount",
    "shim",
    "sleeve",
    "isolator",
)

CHASSIS_RUBBERS_SPECIFIC_COMPONENTS: set[str] = {
    "body_mount_and_crossmember_detail",
    "floor_seam_and_body_mount_rust",
    "frame_rail_body_mount_and_hard_line_detail",
}

CHASSIS_FIXING_SPECIFIC_COMPONENTS: set[str] = {
    "body_mount_and_crossmember_detail",
    "engine_bay_chassis_interface",
    "frame_and_mount_points",
    "frame_floor_underside_and_lines",
    "frame_rail_body_mount_and_crossmember_detail",
    "frame_rail_body_mount_and_hard_line_detail",
    "front_frame_horns_bumper_and_radiator_support",
    "front_frame_horns_bumper_and_steering_area",
    "full_chassis_frame_overview",
    "rear_axle_and_leaf_springs",
    "rear_axle_spring_hanger_and_crossmember",
    "rear_frame_crossmember_and_mounts",
    "rear_mid_frame_rail_and_hard_line_detail",
    "rear_shock_and_crossmember_view",
    "steering_and_suspension_linkages",
    "suspension_or_linkage_mount",
    "transmission_crossmember_and_driveline_mounts",
}

CHASSIS_FIXING_IMAGE_SIGNAL_TOKENS: tuple[str, ...] = (
    "body_mount",
    "bracket",
    "chassis",
    "crossmember",
    "frame",
    "frame_horn",
    "hanger",
    "hard_line",
    "leaf_spring",
    "mount",
    "rail",
    "spring_hanger",
)

EPS_IMAGE_SIGNAL_TOKENS: tuple[str, ...] = (
    "eps",
    "vitz",
    "electric power steering",
    "assist",
    "steering",
    "steering column",
    "steering_and_suspension_linkages",
    "column",
    "linkage",
    "u-joint",
    "ujoint",
    "adapter",
    "ecu",
    "motor",
)

SUSPENSION_IMAGE_SIGNAL_TOKENS: tuple[str, ...] = (
    "suspension",
    "leaf",
    "shackle",
    "shock",
    "damper",
    "bush",
    "spring",
    "ome",
    "alignment",
)

INTERIOR_WEATHERPROOFING_EXCLUDED_SPECIFIC_COMPONENTS: set[str] = {
    "floor_pan_rust_zones",
    "floor_seam_and_body_mount_rust",
}


def text_has_any(text: str, tokens: tuple[str, ...]) -> bool:
    return any(token in text for token in tokens)


def is_chassis_fixing_photo(row: dict[str, str], text_blob: str) -> bool:
    if norm(row.get("component_group")) != "chassis_underside":
        return False
    specific_component = norm(row.get("specific_component"))
    if specific_component in CHASSIS_FIXING_SPECIFIC_COMPONENTS:
        return True
    return text_has_any(text_blob, CHASSIS_FIXING_IMAGE_SIGNAL_TOKENS)


def is_chassis_rubbers_photo(row: dict[str, str], text_blob: str) -> bool:
    specific_component = norm(row.get("specific_component"))
    if specific_component in CHASSIS_RUBBERS_SPECIFIC_COMPONENTS:
        return True
    return text_has_any(text_blob, CHASSIS_RUBBERS_IMAGE_SIGNAL_TOKENS)


def workstream_row_is_excluded(workstream_id: str, row: dict[str, str], text_blob: str) -> bool:
    workstream_key = norm(workstream_id)
    if workstream_key == "stripdown_cataloguing" and is_dashboard_workstream_photo(row):
        return True

    if workstream_key == "chassis_fixing":
        return not is_chassis_fixing_photo(row, text_blob)

    if workstream_key == "chassis_rubbers":
        return not is_chassis_rubbers_photo(row, text_blob)

    if workstream_key == "eps_vitz_upgrade":
        return not text_has_any(text_blob, EPS_IMAGE_SIGNAL_TOKENS)

    if workstream_key == "suspension_upgrade":
        return not text_has_any(text_blob, SUSPENSION_IMAGE_SIGNAL_TOKENS)

    if workstream_key == "interior_weatherproofing":
        specific_component = norm(row.get("specific_component"))
        if specific_component in INTERIOR_WEATHERPROOFING_EXCLUDED_SPECIFIC_COMPONENTS:
            return True

    return False


def is_row_workstream_match(photo_row: dict[str, str], workstream_id: str) -> bool:
    profile = WORKSTREAM_IMAGE_PROFILES.get(workstream_id)
    if not profile:
        return False
    component_group = norm(photo_row.get("component_group"))
    stage = norm(photo_row.get("stage"))
    return component_group in profile["component_groups"] or stage in profile["stages"]


def may1_chassis_status_rows(photo_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(
        [
            row
            for row in photo_rows
            if is_photo_row(row)
            and clean(row.get("captured_date")) == "2026-05-01"
            and norm(row.get("component_group")) == "chassis_underside"
            and norm(row.get("stage")) == "chassis_fixing"
        ],
        key=lambda row: (
            clean(row.get("specific_component")),
            clean(row.get("captured_time")),
            clean(row.get("file_name")),
        ),
    )


def may1_engine_cleaning_rows(photo_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(
        [
            row
            for row in photo_rows
            if is_photo_row(row)
            and clean(row.get("captured_date")) == "2026-05-01"
            and norm(row.get("component_group")) == "engine_bay"
            and norm(row.get("stage")) == "mechanical_cleaning"
        ],
        key=lambda row: (
            clean(row.get("captured_time")),
            clean(row.get("file_name")),
        ),
    )


def rubber_recreation_candidate_rows(photo_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(
        [
            row
            for row in photo_rows
            if is_photo_row(row)
            and norm(row.get("specific_component")) == "rubber_parts_recreation_samples"
            and clean(row.get("captured_date")) == "2026-05-02"
        ],
        key=lambda row: (
            clean(row.get("captured_time")),
            clean(row.get("file_name")),
        ),
    )


def build_chassis_prime_readiness_panel(photo_rows: list[dict[str, str]]) -> dict[str, Any]:
    chassis_rows = may1_chassis_status_rows(photo_rows)
    counts_by_component = Counter(clean(row.get("specific_component")) for row in chassis_rows)
    return {
        "key": "chassis_prime_readiness",
        "title": "Before Primer",
        "summary": "Chassis is not ready for primer. May 1 evidence shows large exterior rail faces partly brushed, but edges, brackets, hard-line clips, mounts, and hidden faces still need detail cleanup and signoff.",
        "metrics": [
            {"label": "May 1 chassis images", "value": str(len(chassis_rows))},
            {"label": "Primer status", "value": "hold"},
            {"label": "Main blocker", "value": "detail prep"},
        ],
        "zones": [
            {
                "area": "Visible flat exterior rail faces",
                "remaining": "20-30%",
                "status": "in_progress",
                "work_required": "Feather chipped coating, remove loose rust and dust, leave hard-bonded paint in place where sound.",
                "evidence_count": str(sum(counts_by_component[name] for name in ("frame_rail_body_mount_and_crossmember_detail", "rear_mid_frame_rail_and_hard_line_detail"))),
            },
            {
                "area": "Top flanges, lower edges, holes, and seams",
                "remaining": "50-60%",
                "status": "pending_detail_brush",
                "work_required": "Wire-cup and hand-brush rail edges, holes, seam lips, and pitted edges until no loose corrosion remains.",
                "evidence_count": str(len(chassis_rows)),
            },
            {
                "area": "Brackets, weld toes, spring/shackle hangers, body mounts",
                "remaining": "50-60%",
                "status": "pending_detail_brush",
                "work_required": "Clean bracket roots and weld toes; inspect spring hangers, shackle mounts, body-mount pads, captive threads, and crossmember junctions.",
                "evidence_count": str(sum(counts_by_component[name] for name in ("rear_axle_spring_hanger_and_crossmember", "frame_rail_body_mount_and_crossmember_detail", "front_frame_horns_bumper_and_steering_area"))),
            },
            {
                "area": "Behind hard lines, clips, wiring, and steering/linkage obstructions",
                "remaining": "60-70%",
                "status": "access_limited",
                "work_required": "Release clips or move lines only where safe, then inspect under contact points before coating.",
                "evidence_count": str(counts_by_component["rear_mid_frame_rail_and_hard_line_detail"] + counts_by_component["front_frame_horns_bumper_and_steering_area"]),
            },
            {
                "area": "Front frame horns, bumper/winch brackets, steering-box area",
                "remaining": "50-60%",
                "status": "pending_inspection",
                "work_required": "Finish brushing and crack-check steering-box mount, front horns, bumper/winch brackets, and nearby crossmember joints.",
                "evidence_count": str(counts_by_component["front_frame_horns_bumper_and_steering_area"]),
            },
            {
                "area": "Rear axle, diff housing, leaf clamps, U-bolt zones",
                "remaining": "40-50% if coated now",
                "status": "scope_decision",
                "work_required": "Decide whether these are included in this coating cycle; if yes, brush and degrease them before primer/topcoat.",
                "evidence_count": str(counts_by_component["rear_axle_spring_hanger_and_crossmember"]),
            },
        ],
        "steps": [
            {
                "label": "Finish detail brushing",
                "status": "in_progress",
                "detail": "Complete edges, brackets, weld toes, body mounts, spring hangers, crossmember ends, steering-box area, hard-line clips, and holes.",
            },
            {
                "label": "Degrease and controlled rinse",
                "status": "queued",
                "detail": "Use DISS/APC for general grime and GREZ OFF for oily deposits; rinse carefully and avoid driving water into bearings, electrics, breathers, or open line ends.",
            },
            {
                "label": "Dry and inspect",
                "status": "queued",
                "detail": "Blow dry and leave fully dry; inspect with bright light and probe suspect pitting, cracks, soft metal, ovalized holes, and clip contact points.",
            },
            {
                "label": "Resolve defects before coating",
                "status": "queued",
                "detail": "Repair or explicitly approve steering-box mount, spring hangers, body mounts, crossmembers, and hard-line brackets before primer.",
            },
            {
                "label": "Treat only remaining rust",
                "status": "queued",
                "detail": "Use Evapo-Rust where practical or compatible converter only in remaining pits/seams; remove residue and do not convert clean steel unnecessarily.",
            },
            {
                "label": "Solvent wipe, epoxy prime, topcoat, cavity wax",
                "status": "queued",
                "detail": "Wax-and-grease wipe only after dry/cure; apply compatible 2K epoxy primer, then topcoat/chassis black, then cavity wax last.",
            },
        ],
        "materials": {
            "available": [
                "Evapo-Rust 5L",
                "DISS/APC cleaner 5L",
                "GREZ OFF HD degreaser",
                "Wadfow WRS1550 pressure sprayer ordered/pending delivery",
            ],
            "missing": [
                "Wax and grease remover",
                "2K epoxy primer system",
                "Compatible chassis topcoat/chassis black",
                "Seam sealer where lap joints need sealing",
                "Cavity wax with wand/nozzle",
                "Extra brushes, strip/flap discs, masking plugs/tape, solvent wipes",
            ],
        },
    }


def rows_by_specific_component(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[clean(row.get("specific_component"))].append(row)
    return grouped


def image_payloads_for_components(
    rows_by_component: dict[str, list[dict[str, str]]],
    components: tuple[str, ...],
) -> list[dict[str, Any]]:
    rows: list[dict[str, str]] = []
    for component in components:
        rows.extend(rows_by_component.get(component, []))
    rows = sorted(
        rows,
        key=lambda row: (
            clean(row.get("captured_time")),
            clean(row.get("file_name")),
        ),
    )
    return dedupe_payload_images([image_payload(row, []) for row in rows])


def slugify_task_id(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", norm(value)).strip("_")
    return slug or "subtask"


def unique_text_items(items: list[str]) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for item in items:
        item_clean = clean(item)
        if not item_clean:
            continue
        item_key = norm(item_clean)
        if item_key in seen:
            continue
        seen.add(item_key)
        output.append(item_clean)
    return output


def subtask_search_tokens(subtask: dict[str, Any]) -> set[str]:
    text_parts: list[str] = []
    for key in ("id", "title", "instruction", "hold_point", "remaining"):
        text_parts.append(clean(subtask.get(key)))
    for key in ("process_steps", "tools", "supplies", "parts", "image_tokens"):
        value = subtask.get(key)
        if isinstance(value, list):
            text_parts.extend(clean(item) for item in value)
    text = " ".join(text_parts)
    tokens = {
        token
        for token in re.findall(r"[a-z0-9]+", norm(text))
        if len(token) >= 4 and token not in SUBTASK_IMAGE_STOPWORDS
    }
    return tokens


def payload_blob(image: dict[str, Any]) -> str:
    return " ".join(
        [
            norm(image.get("caption")),
            norm(image.get("path")),
            norm(image.get("component_group")),
            norm(image.get("specific_component")),
            norm(image.get("stage")),
            norm(image.get("media_id")),
        ]
    )


def select_subtask_images_from_payloads(
    images: list[dict[str, Any]],
    tokens: set[str],
    *,
    max_images: int = 6,
) -> list[dict[str, Any]]:
    scored: list[tuple[int, str, str, dict[str, Any]]] = []
    for image in images:
        blob = payload_blob(image)
        if not blob:
            continue
        score = 0
        for token in tokens:
            if token in blob:
                score += 3 if token in norm(image.get("specific_component")) else 1
        if score <= 0:
            continue
        scored.append(
            (
                score,
                clean(image.get("captured_date")),
                clean(image.get("captured_time")),
                image,
            )
        )

    scored.sort(key=lambda item: (item[0], item[1], item[2]), reverse=True)
    selected = [item[3] for item in scored[:max_images]]
    if not selected:
        selected = images[:max_images]
    return dedupe_payload_images(selected)


def fallback_workstream_images_from_photo_rows(
    workstream_id: str,
    photo_rows: list[dict[str, str]],
    *,
    max_images: int = 36,
) -> list[dict[str, Any]]:
    profile = WORKSTREAM_IMAGE_PROFILES.get(workstream_id, DEFAULT_IMAGE_PROFILE)
    candidates: list[tuple[int, str, str, dict[str, str]]] = []
    for row in photo_rows:
        if not is_photo_row(row):
            continue
        text_blob = row_text_blob(row)
        if workstream_row_is_excluded(workstream_id, row, text_blob):
            continue
        component_match = norm(row.get("component_group")) in profile["component_groups"]
        stage_match = norm(row.get("stage")) in profile["stages"]
        keyword_hits = sum(1 for keyword in profile["keywords"] if keyword in text_blob)
        if not component_match and not stage_match and keyword_hits <= 0:
            continue
        score = (12 if component_match else 0) + (8 if stage_match else 0) + min(keyword_hits, 5) * 3
        candidates.append(
            (
                score,
                clean(row.get("captured_date")),
                clean(row.get("captured_time")),
                row,
            )
        )

    candidates.sort(key=lambda item: (item[0], item[1], item[2]), reverse=True)
    return dedupe_payload_images([image_payload(row, []) for _, _, _, row in candidates[:max_images]])


def registered_item_lines_for_subtask(
    part_rows: list[dict[str, str]],
    tokens: set[str],
    *,
    limit: int = 6,
) -> list[str]:
    if not part_rows or not tokens:
        return []
    scored: list[tuple[int, str, str]] = []
    for row in part_rows:
        item = clean(row.get("item"))
        if not item:
            continue
        blob = " ".join(
            [
                norm(item),
                norm(row.get("category")),
                norm(row.get("notes")),
                norm(row.get("evidence_ref")),
                norm(row.get("procurement_stage")),
                norm(row.get("delivery_status")),
            ]
        )
        score = sum(1 for token in tokens if token in blob)
        if score <= 0:
            continue
        status = clean(row.get("procurement_stage")) or clean(row.get("status")) or "tracked"
        delivery = clean(row.get("delivery_status"))
        amount_status = clean(row.get("amount_status"))
        detail_bits = [status]
        if delivery:
            detail_bits.append(f"delivery {delivery}")
        if amount_status:
            detail_bits.append(f"amount {amount_status}")
        scored.append((score, item, f"{item} ({'; '.join(detail_bits)})"))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [line for _, _, line in scored[:limit]]


def build_standard_workstream_subtask_group(
    workstream_id: str,
    workstream_row: dict[str, str],
    evidence_images: list[dict[str, Any]],
    part_rows_for_workstream: list[dict[str, str]],
) -> dict[str, Any] | None:
    guide = WORKSTREAM_SUBTASK_GUIDES.get(workstream_id)
    if not guide:
        return None

    subtasks: list[dict[str, Any]] = []
    current_status = clean(workstream_row.get("current_status"))
    default_tools = list(guide.get("default_tools") or [])
    default_supplies = list(guide.get("default_supplies") or [])
    for index, source_subtask in enumerate(guide.get("subtasks") or []):
        subtask = dict(source_subtask)
        subtask_id = clean(subtask.get("id")) or slugify_task_id(clean(subtask.get("title")))
        subtask["id"] = subtask_id
        subtask["status"] = clean(subtask.get("status")) or template_step_status(current_status, index)
        subtask["priority"] = clean(subtask.get("priority")) or clean(workstream_row.get("priority")) or "P1"
        subtask["process_steps"] = list(subtask.get("process_steps") or [])
        subtask_tools = list(subtask.get("tools") or []) or default_tools
        subtask_supplies = list(subtask.get("supplies") or []) or default_supplies
        subtask["tools"] = unique_text_items(subtask_tools)
        subtask["supplies"] = unique_text_items(subtask_supplies)
        subtask["parts"] = unique_text_items(list(subtask.get("parts") or []))
        tokens = subtask_search_tokens(subtask)
        subtask["images"] = select_subtask_images_from_payloads(evidence_images, tokens)
        subtask["registered_items"] = registered_item_lines_for_subtask(part_rows_for_workstream, tokens)
        subtasks.append(subtask)

    return {
        "key": slugify_task_id(clean(guide.get("title")) or workstream_id),
        "title": clean(guide.get("title")) or "Operation Sub-Tasks",
        "summary": clean(guide.get("summary")),
        "subtasks": subtasks,
    }


def build_workstream_subtask_groups(
    workstream_id: str,
    workstream_row: dict[str, str],
    evidence_images: list[dict[str, Any]],
    photo_rows: list[dict[str, str]],
    part_rows_for_workstream: list[dict[str, str]],
) -> list[dict[str, Any]]:
    if workstream_id == "chassis_fixing":
        return [build_chassis_before_primer_subtask_group(photo_rows)]

    image_pool = evidence_images or fallback_workstream_images_from_photo_rows(workstream_id, photo_rows)
    group = build_standard_workstream_subtask_group(
        workstream_id,
        workstream_row,
        image_pool,
        part_rows_for_workstream,
    )
    return [group] if group else []


def build_chassis_before_primer_subtask_group(photo_rows: list[dict[str, str]]) -> dict[str, Any]:
    chassis_rows = may1_chassis_status_rows(photo_rows)
    grouped = rows_by_specific_component(chassis_rows)
    side_rail_components = ("frame_rail_body_mount_and_crossmember_detail",)
    front_components = ("front_frame_horns_bumper_and_steering_area",)
    rear_mid_components = ("rear_mid_frame_rail_and_hard_line_detail",)
    rear_axle_components = ("rear_axle_spring_hanger_and_crossmember",)

    subtasks = [
        {
            "id": "side_rails_body_mounts_crossmembers",
            "title": "Side Rails, Body Mounts, Crossmember Detail",
            "priority": "P0",
            "status": "in_progress",
            "remaining": "20-30% flats; 50-60% edges/brackets",
            "instruction": "Feather sound paint, remove loose rust, wire-cup rail top/lower flanges, clean mount-pad perimeters, bolt holes, bracket roots, and crossmember joints.",
            "process_steps": [
                "Dry-brush loose dust first so the wire cup is working on metal/coating, not packed dirt.",
                "Use wire cup on rail faces and lower lips; switch to hand brushes or small wire wheels at bracket roots and tight holes.",
                "Feather sound paint edges without chasing every bonded coating patch to bare steel.",
                "Probe pitted mount pads, bracket roots, and crossmember seams after brushing.",
                "Blow out holes and seams, then take close-up signoff photos before any wet cleaning.",
            ],
            "tools": [
                "Angle grinder with wire cup",
                "Drill with small wire wheels",
                "Hand wire brushes and picks",
                "Inspection light",
                "Compressed air or blower",
            ],
            "supplies": [
                "Dust mask/respirator and eye protection",
                "Rags",
                "Masking plugs/tape for threads and holes",
                "Rust marking pen",
            ],
            "hold_point": "Each body-mount pad and bracket root has a close-up signoff photo after final dry brushing; captive threads are checked before primer.",
            "images": image_payloads_for_components(grouped, side_rail_components),
        },
        {
            "id": "front_horns_steering_box_bumper",
            "title": "Front Horns, Bumper/Winch Mounts, Steering Area",
            "priority": "P0",
            "status": "pending_inspection",
            "remaining": "50-60%",
            "instruction": "Clean steering-box mount and nearby hanger weld toes to inspection condition, then wire-cup front horns, bumper/winch brackets, bolt holes, and crossmember laps.",
            "process_steps": [
                "Degrease only if oil is hiding cracks; otherwise finish dry brushing before wet work.",
                "Detail-clean steering-box mount faces, bolt holes, weld toes, and nearby hanger roots.",
                "Clean front horn inner and outer faces, bumper/winch bracket laps, and crossmember ends.",
                "Inspect with bright light for cracks, oval holes, bent brackets, or thin metal.",
                "Mark any defect directly on the chassis and open/retain the issue row before coating.",
            ],
            "tools": [
                "Wire cup and narrow wire wheel",
                "Pick/probe",
                "Inspection mirror",
                "Bright inspection light",
                "Socket/thread-check tools",
            ],
            "supplies": [
                "DISS/APC for dirt if needed",
                "GREZ OFF only for oily deposits",
                "Rags",
                "Paint marker",
                "Thread masking plugs",
            ],
            "hold_point": "Steering-box mount, front hanger roots, front horn brackets, and any elongated/cracked holes are inspected and repair decisions are marked.",
            "images": image_payloads_for_components(grouped, front_components),
        },
        {
            "id": "rear_mid_rail_hard_lines",
            "title": "Rear/Mid Rail, Hard-Line Clips, Crossmember Edges",
            "priority": "P0",
            "status": "access_limited",
            "remaining": "50-70%",
            "instruction": "Mark every hard-line clip, release or lift clips only where safe, hand-brush under/around lines, wire-cup crossmember ends and lower rail lips, then probe for thinning.",
            "process_steps": [
                "Photograph current hard-line routing and clip positions before moving anything.",
                "Mark clips and only release/lift lines where it will not kink or stress them.",
                "Hand-brush under clips and behind lines; do not force a power wheel against hard lines.",
                "Wire-cup crossmember ends, lower rail lips, and visible bracket edges.",
                "Probe under-clip contact points and replace/log weak clips or suspect lines.",
                "After wet cleaning, blow dry under clips and between line/contact faces.",
            ],
            "tools": [
                "Hand wire brushes",
                "Small picks",
                "Line/clip tools",
                "Narrow wire wheel for open areas",
                "Compressed air or blower",
            ],
            "supplies": [
                "Rubber-lined P-clips if old clips fail",
                "Masking labels",
                "DISS/APC cleaner",
                "Rags",
                "Rust marking pen",
            ],
            "hold_point": "Under-clip contact areas are inspected, weak lines/clips are logged or replaced, and no wet cleaner remains trapped under clips before primer.",
            "images": image_payloads_for_components(grouped, rear_mid_components),
        },
        {
            "id": "rear_axle_spring_hangers",
            "title": "Rear Axle, Rear Spring Hangers, Leaf Mounts",
            "priority": "P1",
            "status": "scope_decision",
            "remaining": "40-50% if coated now",
            "instruction": "Clean rear spring hanger roots enough for crack/deformation inspection; decide whether axle/diff/leaf hardware is included in this coating cycle or deferred to suspension work.",
            "process_steps": [
                "Brush hanger roots, shackle areas, and nearby crossmember welds enough for inspection.",
                "Check spring/shackle holes for ovaling before the Ironman suspension install window.",
                "Inspect axle tube, U-bolt, and leaf clamp areas for leaks or trapped scale.",
                "Decide whether axle/spring hardware is coated now or deferred until suspension removal improves access.",
                "If deferred, protect only the chassis-ready surfaces and document the deferred axle/spring scope.",
            ],
            "tools": [
                "Wire cup",
                "Hand brushes",
                "Pick/probe",
                "Inspection light",
                "Angle finder/tape for suspension baseline if available",
            ],
            "supplies": [
                "Penetrating oil for future suspension fasteners",
                "DISS/APC cleaner",
                "GREZ OFF only for oily axle deposits",
                "Paint marker",
            ],
            "hold_point": "Rear hanger roots and shackle/spring holes are checked; no primer/topcoat is applied over active axle/brake leaks or inaccessible U-bolt areas.",
            "images": image_payloads_for_components(grouped, rear_axle_components),
        },
        {
            "id": "degrease_dry_rust_treatment_gate",
            "title": "Degrease, Dry, Rust Treatment, Primer Gate",
            "priority": "P0",
            "status": "queued",
            "remaining": "not started",
            "instruction": "After dry brushing, apply DISS/APC broadly and GREZ OFF only on oily zones, agitate, rinse with controlled pressure, blow dry seams/holes/clips, then treat only remaining rust in pits.",
            "process_steps": [
                "Confirm all dry brushing, probing, and defect decisions are complete before wet cleaning.",
                "Apply DISS/APC from bottom upward for general dirt; apply GREZ OFF only to oily deposits.",
                "Agitate with brushes and rinse with controlled pressure, avoiding bearings, breathers, electrics, and open line ends.",
                "Blow dry seams, clips, holes, boxed edges, and line contact areas; allow full dry time.",
                "Use Evapo-Rust where practical or compatible converter only in remaining pits; remove residue after cure.",
                "Wax/grease wipe, mask threads/holes, then apply the selected compatible 2K epoxy primer/topcoat/cavity-wax stack.",
            ],
            "tools": [
                "Wadfow WRS1550 pressure sprayer for cleaner application",
                "Controlled pressure rinse",
                "Detail brushes",
                "Compressed air or blower",
                "Solvent-safe wipes",
            ],
            "supplies": [
                "DISS/APC cleaner 5L - received",
                "GREZ OFF HD degreaser - received",
                "Evapo-Rust 5L - received",
                "Wax and grease remover - still required",
                "2K epoxy primer system - still required",
                "Compatible chassis topcoat/chassis black - still required",
                "Seam sealer and cavity wax - still required for final stack",
            ],
            "hold_point": "Chassis is fully dry, repair decisions are closed, converter residue is removed, wax/grease wipe is done, and compatible 2K epoxy primer/topcoat/cavity-wax stack is selected.",
            "images": dedupe_payload_images([image_payload(row, []) for row in chassis_rows]),
        },
    ]

    return {
        "key": "before_primer",
        "title": "Before Primer",
        "summary": "Sub-tasks that must be completed before chassis primer. Each sub-task is backed by the May 1 photo evidence for that area.",
        "subtasks": subtasks,
    }


def placeholder_image() -> dict[str, str]:
    return {
        "path": PLACEHOLDER_IMAGE_PATH,
        "caption": "Image required - add photo evidence",
        "captured_date": "",
        "captured_time": "",
        "media_type": "photo",
        "component_group": "",
        "specific_component": "",
        "stage": "",
        "media_id": "",
        "matched_tokens": [],
        "match_basis": "placeholder",
    }


def inventory_override_payload(row: dict[str, str], item: str) -> dict[str, Any] | None:
    notes = norm(row.get("notes"))
    source_ref = clean(row.get("source_ref"))
    if any(token in notes for token in ("image_disputed", "incorrect_image", "suppress_image")):
        payload = placeholder_image()
        payload["caption"] = clean(row.get("caption")) or f"{item} · image disputed - exact photo required"
        payload["matched_tokens"] = [source_ref] if source_ref else []
        payload["match_basis"] = "manual_image_disputed"
        payload["match_score"] = 999
        return payload

    image_path = clean(row.get("image_path")) or clean(row.get("path")) or clean(row.get("local_path"))
    if not image_path:
        return None
    caption = clean(row.get("caption")) or f"{item} · Manual image override"
    match_basis = "manual_override"
    if any(token in notes for token in ("exact_order_evidence", "order_evidence", "order_contactsheet")):
        match_basis = "exact_order_evidence"
    elif any(token in notes for token in ("local_received", "local_actual", "local_project")):
        match_basis = "local_inventory_evidence"
    return {
        "path": path_for_ui(image_path),
        "caption": caption,
        "captured_date": "",
        "captured_time": "",
        "media_type": "photo",
        "component_group": "procurement_inventory",
        "specific_component": "manual_override_reference",
        "stage": "procurement_reconciliation",
        "media_id": "",
        "matched_tokens": [clean(row.get("source_ref"))] if clean(row.get("source_ref")) else [],
        "match_basis": match_basis,
        "match_score": 999,
    }


def load_inventory_image_overrides(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    rows = load_csv_optional(path)
    overrides: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        source_ref_key = normalize_source_ref(clean(row.get("source_ref")))
        if not source_ref_key:
            continue
        source_key = norm(row.get("source"))
        overrides[(source_key, source_ref_key)] = row
        if not source_key:
            overrides[("", source_ref_key)] = row
    return overrides


def normalize_source_ref(value: str) -> str:
    token = norm(value)
    if "#" in token:
        token = token.split("#")[-1]
    return token


def add_local_order_image_index_key(index: dict[str, Path], key: str, path: Path) -> None:
    normalized = clean(key).lower().strip().strip("()[]{}\"'")
    if not normalized:
        return
    normalized = normalized.replace("\\", "/")
    index.setdefault(normalized, path)
    if normalized.startswith("photo_") and len(normalized) > 8:
        index.setdefault(normalized.removeprefix("photo_"), path)
    if "/photo_" in normalized:
        index.setdefault(normalized.replace("/photo_", "/"), path)


def local_order_image_keys(path: Path) -> set[str]:
    try:
        relative_path = path.relative_to(ROOT).as_posix()
    except ValueError:
        relative_path = path.as_posix()
    relative_path = relative_path.lower()
    filename = path.name.lower()
    stem = path.stem.lower()
    keys = {
        relative_path,
        relative_path.rsplit(".", 1)[0],
        filename,
        stem,
        f"photo_{filename}",
        f"photo_{stem}",
    }
    if relative_path.startswith("photos/"):
        without_photos = relative_path.removeprefix("photos/")
        keys.add(without_photos)
        keys.add(without_photos.rsplit(".", 1)[0])
        keys.add(f"photo_{without_photos}")
        keys.add(f"photo_{without_photos.rsplit('.', 1)[0]}")
    return {key for key in keys if key}


def build_local_order_image_index() -> dict[str, Path]:
    global LOCAL_ORDER_IMAGE_INDEX
    if LOCAL_ORDER_IMAGE_INDEX is not None:
        return LOCAL_ORDER_IMAGE_INDEX

    index: dict[str, Path] = {}
    for directory in LOCAL_ORDER_IMAGE_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in LOCAL_ORDER_IMAGE_EXTENSIONS:
                continue
            for key in local_order_image_keys(path):
                add_local_order_image_index_key(index, key, path)
    LOCAL_ORDER_IMAGE_INDEX = index
    return index


def local_order_image_reference_tokens(values: list[str]) -> list[str]:
    tokens: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = clean(value)
        if not text:
            continue
        for raw_token in re.split(r"[|,\s]+", text):
            token = raw_token.strip().strip("()[]{}\"'")
            if not token:
                continue
            token = token.split("?", 1)[0].split("#", 1)[0].replace("\\", "/").lower()
            candidates = {token}
            if token.endswith(tuple(LOCAL_ORDER_IMAGE_EXTENSIONS)):
                candidates.add(token.rsplit(".", 1)[0])
            basename = token.rsplit("/", 1)[-1]
            if basename and basename != token:
                candidates.add(basename)
                candidates.add(basename.rsplit(".", 1)[0])
            for candidate in list(candidates):
                if candidate.startswith("photo_") and len(candidate) > 8:
                    candidates.add(candidate.removeprefix("photo_"))
                elif (
                    candidate.endswith(tuple(LOCAL_ORDER_IMAGE_EXTENSIONS))
                    or re.search(r"\d{6,}", candidate)
                ):
                    candidates.add(f"photo_{candidate}")

            for candidate in candidates:
                if len(candidate) < 6:
                    continue
                if candidate not in seen:
                    seen.add(candidate)
                    tokens.append(candidate)
    tokens.sort(key=len, reverse=True)
    return tokens


def exact_order_image_payload(
    path: Path,
    *,
    item: str,
    vendor: str,
    matched_token: str,
    match_basis: str,
) -> dict[str, Any]:
    try:
        relative_path = path.relative_to(ROOT).as_posix()
    except ValueError:
        relative_path = path.as_posix()
    evidence_label = "exact order evidence" if match_basis == "exact_order_evidence" else "local inventory photo"
    caption = f"{item} · {evidence_label}" if item else humanize_token(evidence_label)
    if vendor:
        caption = f"{caption} · {vendor}"
    return {
        "path": path_for_ui(relative_path),
        "caption": caption,
        "captured_date": "",
        "captured_time": "",
        "media_type": "photo",
        "component_group": "procurement_inventory",
        "specific_component": match_basis,
        "stage": "procurement_reconciliation",
        "media_id": path.stem,
        "matched_tokens": [matched_token],
        "match_basis": match_basis,
        "match_score": 980,
    }


def direct_inventory_photo_match_basis(
    path: Path,
    *,
    matched_token: str,
    evidence_ref: str,
    notes: str,
    vendor: str,
) -> str:
    del notes
    blob = norm(" ".join([path.name, matched_token, evidence_ref, vendor]))
    if any(
        token in blob
        for token in (
            "order",
            "receipt",
            "gmail_order",
            "aliexpress",
            "daraz",
            "autohub",
            "autoxpert",
            "auto_xpert",
        )
    ):
        return "exact_order_evidence"
    return "local_inventory_evidence"


def choose_exact_order_image(
    *,
    item: str,
    vendor: str,
    evidence_ref: str,
    notes: str,
    source_ref: str,
) -> dict[str, Any] | None:
    image_index = build_local_order_image_index()
    for token in local_order_image_reference_tokens([evidence_ref, notes, source_ref]):
        path = image_index.get(token)
        if path is not None:
            match_basis = direct_inventory_photo_match_basis(
                path,
                matched_token=token,
                evidence_ref=evidence_ref,
                notes=notes,
                vendor=vendor,
            )
            return exact_order_image_payload(
                path,
                item=item,
                vendor=vendor,
                matched_token=token,
                match_basis=match_basis,
            )
    return None


def selling_site_image_payload(row: dict[str, str], matched_tokens: list[str]) -> dict[str, Any]:
    item = clean(row.get("item"))
    vendor = clean(row.get("vendor"))
    caption = item
    if vendor:
        caption = f"{caption} · {vendor} · Selling Site Image"
    else:
        caption = f"{caption} · Selling Site Image"
    return {
        "path": path_for_ui(clean(row.get("local_path"))),
        "caption": caption,
        "captured_date": "",
        "captured_time": "",
        "media_type": "photo",
        "component_group": "procurement_inventory",
        "specific_component": "selling_site_listing_reference",
        "stage": "procurement_reconciliation",
        "media_id": "",
        "matched_tokens": matched_tokens,
        "match_basis": "selling_site_match",
    }


def is_inventory_reference_photo_row(row: dict[str, str]) -> bool:
    if not is_photo_row(row):
        return False
    stage = norm(row.get("stage"))
    component_group = norm(row.get("component_group"))
    return stage in {"procurement_reconciliation", "reference_material"} or component_group in {
        "procurement_inventory",
        "documentation_reference",
    }


def choose_selling_site_image(
    manifest_rows: list[dict[str, str]],
    *,
    item: str,
    vendor: str,
    evidence_ref: str,
    notes: str,
    supply_type: str,
    source_table: str,
    source_ref: str,
) -> dict[str, Any] | None:
    source_table_key = norm(source_table)
    source_ref_key = normalize_source_ref(source_ref)
    reference_tokens = extract_inventory_reference_tokens([evidence_ref, notes])
    item_tokens = search_tokens([item], max_tokens=12)
    vendor_tokens = search_tokens([vendor], max_tokens=6)
    context_tokens = search_tokens([notes, evidence_ref], max_tokens=8)

    best_score = -999
    best_row: dict[str, str] | None = None
    best_matches: list[str] = []
    best_exact_match = False

    for row in manifest_rows:
        local_path = clean(row.get("local_path"))
        if not local_path:
            continue
        status = norm(row.get("status"))
        if status not in {"downloaded", "reused_cached_image", "copied_local"}:
            continue

        row_item_type = norm(row.get("item_type"))
        if supply_type == "tool" and row_item_type != "tool":
            continue
        if supply_type in {"part", "substance"} and row_item_type != "part":
            continue

        row_source_table = norm(row.get("source_table"))
        row_source_ref = normalize_source_ref(clean(row.get("source_ref")))
        row_blob = " ".join(
            [
                norm(row.get("item")),
                norm(row.get("vendor")),
                row_source_table,
                row_source_ref,
                norm(Path(local_path).stem),
                norm(row.get("listing_url")),
                norm(row.get("image_url")),
            ]
        )

        score = 0
        matches: list[str] = []
        source_match = False
        exact_source_match = False
        reference_hits = 0
        strong_reference_hits = 0

        if source_table_key and row_source_table == source_table_key:
            score += 20
            if source_ref_key and row_source_ref == source_ref_key:
                score += 140
                source_match = True
                exact_source_match = True
                strong_reference_hits += 1
                matches.append(source_ref_key)
        elif source_ref_key and row_source_ref == source_ref_key:
            score += 120
            source_match = True
            exact_source_match = True
            strong_reference_hits += 1
            matches.append(source_ref_key)

        for token in reference_tokens:
            if not token:
                continue
            if inventory_reference_token_is_low_signal(token):
                continue
            if token == row_source_ref:
                reference_hits += 1
                strong_reference_hits += 1
                score += 120
                source_match = True
                matches.append(token)
                continue
            if token in row_source_ref:
                reference_hits += 1
                strong_reference_hits += 1
                score += 44
                matches.append(token)
                continue
            if token in row_blob:
                reference_hits += 1
                if not token.isdigit() and len(token) >= 8:
                    strong_reference_hits += 1
                score += 24 if (not token.isdigit() and len(token) >= 8) else 8
                matches.append(token)

        item_hits = 0
        item_hit_tokens: list[str] = []
        for token in item_tokens:
            if token in row_blob:
                item_hits += 1
                item_hit_tokens.append(token)
                matches.append(token)
        score += min(item_hits, 5) * 12

        vendor_hits = 0
        for token in vendor_tokens:
            if token in row_blob:
                vendor_hits += 1
                matches.append(token)
        score += min(vendor_hits, 3) * 6

        context_hits = 0
        for token in context_tokens:
            if token in row_blob:
                context_hits += 1
                matches.append(token)
        score += min(context_hits, 4) * 3

        non_generic_item_hits = [token for token in item_hit_tokens if token not in GENERIC_INVENTORY_MATCH_TOKENS]
        if not source_match and strong_reference_hits == 0 and item_hits < 2:
            continue
        if not source_match and strong_reference_hits == 0 and item_hits >= 2 and not non_generic_item_hits:
            continue

        if status == "downloaded":
            score += 4
        elif status == "reused_cached_image":
            score += 3
        else:
            score += 2

        if score > best_score:
            best_score = score
            best_row = row
            best_matches = list(dict.fromkeys(matches))
            best_exact_match = exact_source_match

    if best_row is not None and (best_exact_match or best_score >= 32):
        selected = selling_site_image_payload(best_row, best_matches[:8])
        selected["match_score"] = best_score
        return selected
    return None


def whatsapp_media_image_payload(
    row: dict[str, str],
    matched_tokens: list[str],
    *,
    match_basis: str,
    match_score: int,
    component_group: str = "procurement_inventory",
    specific_component: str = "whatsapp_media_reference",
    stage: str = "procurement_reconciliation",
) -> dict[str, Any]:
    timestamp = clean(row.get("timestamp"))
    captured_date = ""
    captured_time = ""
    if "T" in timestamp:
        captured_date, captured_time = timestamp.split("T", 1)
    elif " " in timestamp:
        captured_date, captured_time = timestamp.split(" ", 1)

    chat_name = clean(row.get("chat_name")) or clean(row.get("source_name")) or "WhatsApp"
    caption = f"{chat_name} · WhatsApp media"
    if timestamp:
        caption = f"{caption} · {timestamp.replace('T', ' ')}"

    return {
        "path": path_for_ui(clean(row.get("relative_path"))),
        "caption": caption,
        "captured_date": captured_date,
        "captured_time": captured_time,
        "media_type": clean(row.get("media_type")) or "photo",
        "component_group": component_group,
        "specific_component": specific_component,
        "stage": stage,
        "media_id": clean(row.get("media_id")),
        "matched_tokens": matched_tokens,
        "match_basis": match_basis,
        "match_score": match_score,
    }


def choose_whatsapp_inventory_image(
    whatsapp_media_rows: list[dict[str, str]],
    *,
    item: str,
    vendor: str,
    evidence_ref: str,
    notes: str,
) -> dict[str, Any] | None:
    reference_tokens = extract_inventory_reference_tokens([evidence_ref, notes])
    item_tokens = search_tokens([item], max_tokens=10)
    context_tokens = search_tokens([vendor, notes, evidence_ref], max_tokens=12)

    best_score = -999
    best_row: dict[str, str] | None = None
    best_matches: list[str] = []
    for row in whatsapp_media_rows:
        if norm(row.get("media_type")) != "photo":
            continue
        relative_path = clean(row.get("relative_path"))
        if not relative_path:
            continue

        chat_name = norm(row.get("chat_name"))
        source_name = norm(row.get("source_name"))
        is_preferred_chat = chat_name in {"akber khan", "fj40"} or source_name in {"akber khan", "fj40"}

        blob = " ".join(
            [
                norm(row.get("media_id")),
                norm(row.get("message_id")),
                norm(row.get("raw_message_id")),
                chat_name,
                norm(row.get("file_name")),
                norm(Path(relative_path).stem),
                norm(row.get("timestamp")),
            ]
        )

        score = 0
        matches: list[str] = []
        reference_hits = 0

        for token in reference_tokens:
            if inventory_reference_token_is_low_signal(token):
                continue
            if token and token in blob:
                reference_hits += 1
                score += 48 if (not token.isdigit() and len(token) >= 8) else 18
                matches.append(token)

        item_hits = 0
        item_hit_tokens: list[str] = []
        for token in item_tokens:
            if token in blob:
                item_hits += 1
                item_hit_tokens.append(token)
                matches.append(token)
        score += min(item_hits, 4) * 8

        context_hits = 0
        for token in context_tokens:
            if token in blob:
                context_hits += 1
                matches.append(token)
        score += min(context_hits, 3) * 4

        if norm(row.get("is_relevant")) == "true":
            score += 8
        if is_preferred_chat:
            score += 6

        non_generic_item_hits = [token for token in item_hit_tokens if token not in GENERIC_INVENTORY_MATCH_TOKENS]
        if reference_hits == 0 and item_hits == 0 and context_hits == 0:
            continue
        if reference_hits == 0 and item_hits >= 2 and not non_generic_item_hits:
            continue

        if score > best_score:
            best_score = score
            best_row = row
            best_matches = list(dict.fromkeys(matches))

    if best_row is not None and best_score >= 26:
        return whatsapp_media_image_payload(
            best_row,
            best_matches[:8],
            match_basis="whatsapp_evidence_match",
            match_score=best_score,
        )

    return None


def choose_inventory_image(
    photo_rows: list[dict[str, str]],
    workstream_default_images: dict[str, dict[str, Any]],
    selling_site_manifest_rows: list[dict[str, str]],
    whatsapp_media_rows: list[dict[str, str]],
    inventory_image_overrides: dict[tuple[str, str], dict[str, str]],
    *,
    item: str,
    workstream: str,
    evidence_ref: str,
    notes: str,
    supply_type: str,
    vendor: str,
    source_table: str,
    source_ref: str,
) -> dict[str, Any]:
    source_table_key = norm(source_table)
    source_ref_key = normalize_source_ref(source_ref)
    override_row = (
        inventory_image_overrides.get((source_table_key, source_ref_key))
        or inventory_image_overrides.get(("", source_ref_key))
    )
    if override_row is not None:
        override_payload = inventory_override_payload(override_row, item)
        if override_payload is not None:
            return override_payload

    exact_order_image = choose_exact_order_image(
        item=item,
        vendor=vendor,
        evidence_ref=evidence_ref,
        notes=notes,
        source_ref=source_ref,
    )
    if exact_order_image is not None:
        return exact_order_image

    selling_site_image = choose_selling_site_image(
        selling_site_manifest_rows,
        item=item,
        vendor=vendor,
        evidence_ref=evidence_ref,
        notes=notes,
        supply_type=supply_type,
        source_table=source_table,
        source_ref=source_ref,
    )
    if selling_site_image is not None:
        return selling_site_image

    reference_tokens = extract_inventory_reference_tokens([evidence_ref, notes])
    item_tokens = search_tokens([item], max_tokens=12)
    context_tokens = search_tokens([notes, evidence_ref], max_tokens=12)
    best_score = -999
    best_row: dict[str, str] | None = None
    best_matches: list[str] = []

    for row in photo_rows:
        if not is_inventory_reference_photo_row(row):
            continue
        blob = row_text_blob(row)
        match_blob = blob
        score = 0
        matches: list[str] = []

        reference_hits = 0
        for token in reference_tokens:
            if inventory_reference_token_is_low_signal(token):
                continue
            if token in blob:
                reference_hits += 1
                score += 52 if (not token.isdigit() and len(token) >= 8) else 18
                matches.append(token)

        item_hits = 0
        item_hit_tokens: list[str] = []
        for token in item_tokens:
            if token in match_blob:
                item_hits += 1
                item_hit_tokens.append(token)
                matches.append(token)
        score += min(item_hits, 5) * 12

        context_hits = 0
        for token in context_tokens:
            if token in match_blob:
                context_hits += 1
                matches.append(token)
        score += min(context_hits, 4) * 4

        non_generic_item_hits = [token for token in item_hit_tokens if token not in GENERIC_INVENTORY_MATCH_TOKENS]
        if reference_hits == 0 and item_hits < 2:
            continue
        if reference_hits == 0 and item_hits >= 2 and not non_generic_item_hits:
            continue

        stage = norm(row.get("stage"))
        component_group = norm(row.get("component_group"))
        if stage == "procurement_reconciliation":
            score += 6
        if stage == "reference_material":
            score += 8 if reference_hits > 0 else 2
        if component_group == "documentation_reference" and reference_hits == 0 and item_hits < 3:
            continue

        if workstream and is_row_workstream_match(row, workstream):
            score += 8
        if supply_type == "substance" and any(k in blob for k in ("primer", "sealer", "wax", "rust", "cleaner", "grease")):
            score += 5
        if supply_type == "tool" and any(k in blob for k in ("hardware", "bracket", "mount", "tool")):
            score += 2
        if norm(row.get("confidence")) == "high":
            score += 2
        if "documentation_reference" in component_group and reference_hits == 0:
            score -= 12

        if score > best_score:
            best_score = score
            best_row = row
            best_matches = list(dict.fromkeys(matches))

    if best_row is not None and best_score >= 20:
        selected = image_payload(best_row, best_matches[:8])
        selected["match_basis"] = "inventory_match"
        selected["match_score"] = best_score
        return selected

    whatsapp_image = choose_whatsapp_inventory_image(
        whatsapp_media_rows,
        item=item,
        vendor=vendor,
        evidence_ref=evidence_ref,
        notes=notes,
    )
    if whatsapp_image is not None:
        return whatsapp_image

    selected = placeholder_image()
    if item:
        selected["caption"] = f"{item} · exact inventory image required"
    return selected


def attach_inventory_images(
    rows: list[dict[str, Any]],
    photo_rows: list[dict[str, str]],
    workstream_default_images: dict[str, dict[str, Any]],
    selling_site_manifest_rows: list[dict[str, str]],
    whatsapp_media_rows: list[dict[str, str]],
    inventory_image_overrides: dict[tuple[str, str], dict[str, str]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        updated = dict(row)
        source_table = clean(row.get("source"))
        source_ref = clean(row.get("source_ref"))
        entry_id = clean(row.get("entry_id"))
        if not source_table and entry_id:
            source_table = "expenses"
        if not source_ref:
            source_ref = entry_id
        updated["image"] = choose_inventory_image(
            photo_rows,
            workstream_default_images,
            selling_site_manifest_rows,
            whatsapp_media_rows,
            inventory_image_overrides,
            item=clean(row.get("item")),
            workstream=clean(row.get("workstream")),
            evidence_ref=clean(row.get("evidence_ref")),
            notes=clean(row.get("notes")),
            supply_type=clean(row.get("supply_type")) or "part",
            vendor=clean(row.get("vendor")),
            source_table=source_table,
            source_ref=source_ref,
        )
        output.append(updated)
    return output


def workstream_part_row_payload(row: dict[str, str]) -> dict[str, Any]:
    return {
        "entry_id": clean(row.get("entry_id")),
        "workstream": split_legacy_steering_brakes_workstream(
            clean(row.get("workstream")),
            category=clean(row.get("category")),
            item=clean(row.get("item")),
            notes=clean(row.get("notes")),
        ),
        "item": clean(row.get("item")),
        "status": clean(row.get("status")),
        "procurement_stage": clean(row.get("procurement_stage")),
        "payment_status": clean(row.get("payment_status")),
        "delivery_status": clean(row.get("delivery_status")),
        "amount": clean(row.get("amount")),
        "amount_status": clean(row.get("amount_status")),
        "currency": clean(row.get("currency")) or "PKR",
        "vendor": clean(row.get("company")),
        "supply_type": "part",
        "source": "expenses",
        "source_ref": clean(row.get("entry_id")),
        "evidence_ref": clean(row.get("evidence_ref")),
        "notes": clean(row.get("notes")),
    }


def build_dashboard_data() -> dict[str, Any]:
    workstream_rows = load_csv(WORKSTREAM_STATUS_PATH)
    package_rows = load_csv(REASSEMBLY_PACKAGES_PATH)
    component_rows = load_csv(COMPONENT_JOBS_PATH)
    photo_rows = load_csv(PHOTO_INVENTORY_PATH)
    replacement_pipe_requirement_rows = load_csv_optional(REPLACEMENT_PIPE_SPECS_PATH)
    replacement_pipe_order_release_rows = load_csv_optional(REPLACEMENT_PIPE_ORDER_RELEASE_SPECS_PATH)
    replacement_pipe_release_action_rows = load_csv_optional(REPLACEMENT_PIPE_RELEASE_ACTIONS_PATH)
    replacement_pipe_circuit_closure_rows = load_csv_optional(REPLACEMENT_PIPE_CIRCUIT_CLOSURE_PATH)
    chassis_rubber_requirement_rows = load_csv_optional(CHASSIS_RUBBER_REQUIREMENTS_PATH)
    body_mount_order_release_rows = load_csv_optional(BODY_MOUNT_ORDER_RELEASE_SPECS_PATH)
    body_mount_release_action_rows = load_csv_optional(BODY_MOUNT_RELEASE_ACTIONS_PATH)
    body_mount_station_closure_rows = load_csv_optional(BODY_MOUNT_STATION_CLOSURE_PATH)
    brake_system_requirement_rows = load_csv_optional(BRAKE_SYSTEM_REQUIREMENTS_PATH)
    paint_refinish_queue_rows = load_csv_optional(PAINT_REFINISH_MEDIA_QUEUE_PATH)
    paint_refinish_whatsapp_rows = load_csv_optional(PAINT_REFINISH_WHATSAPP_MEDIA_QUEUE_PATH)
    selling_site_manifest_rows = load_csv_optional(SELLING_SITE_MANIFEST_PATH)
    whatsapp_j40_chat_rows = load_csv_optional(WHATSAPP_J40_CHAT_CANDIDATES_PATH)
    whatsapp_j40_media_rows = load_csv_optional(WHATSAPP_J40_MEDIA_INDEX_PATH)
    inventory_image_overrides = load_inventory_image_overrides(INVENTORY_IMAGE_OVERRIDES_PATH)
    expense_rows = load_csv(EXPENSES_PATH)
    buy_now_rows = load_csv(BUY_NOW_PATH)
    supplies_inventory = build_supplies_inventory(expense_rows)
    electrical_spec_layout = load_electrical_spec_layout()
    electrical_spec_layout_by_workstream: dict[str, dict[str, Any]] = {}
    if electrical_spec_layout:
        electrical_spec_layout_by_workstream["electrical_reset"] = electrical_spec_layout
        electrical_spec_layout_by_workstream["interior_controls"] = build_dashboard_electrical_spec_layout(
            electrical_spec_layout
        )
    expense_by_entry_id = {clean(row.get("entry_id")): row for row in expense_rows}
    part_rows = [
        row
        for row in expense_rows
        if norm(row.get("bucket")) == "parts"
        and norm(row.get("status")) != "cancelled"
        and norm(row.get("delivery_status")) != "not_required"
        and not norm(row.get("procurement_stage")).startswith("not_required")
    ]
    part_rows_by_workstream: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in part_rows:
        ws_id = split_legacy_steering_brakes_workstream(
            clean(row.get("workstream")),
            category=clean(row.get("category")),
            item=clean(row.get("item")),
            notes=clean(row.get("notes")),
        )
        if ws_id:
            part_rows_by_workstream[ws_id].append(row)
    part_rows_by_workstream["interior_controls"] = [
        row
        for row in part_rows
        if is_dashboard_related_part_row(row)
    ]

    selected_workstreams = collect_workstreams(workstream_rows)
    selected_workstream_ids = [clean(row.get("workstream_id")) for row in selected_workstreams]

    packages_by_workstream: dict[str, list[dict[str, str]]] = defaultdict(list)
    for package in package_rows:
        linked_ids = split_pipe(package.get("linked_workstreams", ""))
        for ws_id in linked_ids:
            packages_by_workstream[ws_id].append(package)

    jobs_by_workstream: dict[str, list[dict[str, str]]] = defaultdict(list)
    issues_by_workstream: dict[str, list[dict[str, str]]] = defaultdict(list)
    for component in component_rows:
        ws_id = clean(component.get("target_workstream"))
        if not ws_id:
            continue
        job_id = clean(component.get("component_job_id"))
        if job_id.startswith("issue_"):
            issues_by_workstream[ws_id].append(component)
        else:
            jobs_by_workstream[ws_id].append(component)
    interior_component_jobs = sorted(
        [
            row
            for row in component_rows
            if norm(row.get("component_group"))
            in {"interior", "interior_cabin", "window_hardware", "electrical_accessories", "rubbers_and_seals"}
        ],
        key=lambda row: clean(row.get("component_job_id")),
    )

    workstreams: list[dict[str, Any]] = []
    for row in selected_workstreams:
        ws_id = clean(row.get("workstream_id"))
        if ws_id == "interior_controls":
            linked_packages = sorted(
                [
                    row
                    for row in package_rows
                    if clean(row.get("work_package_id")) in {"WP03", "WP03A", "WP03B", "WP05"}
                    or norm(row.get("lane")) in {"electrical", "interior", "interior_security"}
                ],
                key=lambda value: clean(value.get("work_package_id")),
            )
            jobs = [row for row in interior_component_jobs if not clean(row.get("component_job_id", "")).startswith("issue_")]
            issues = []
        else:
            linked_packages = sorted(
                packages_by_workstream.get(ws_id, []),
                key=lambda value: clean(value.get("work_package_id")),
            )
            jobs = sorted(
                jobs_by_workstream.get(ws_id, []),
                key=lambda value: clean(value.get("component_job_id")),
            )
            issues = sorted(
                issues_by_workstream.get(ws_id, []),
                key=lambda value: clean(value.get("component_job_id")),
            )
        reference_tokens = collect_workstream_reference_tokens(row, linked_packages, jobs, issues)
        evidence = build_workstream_evidence_sets(
            ws_id,
            photo_rows,
            reference_tokens,
            paint_refinish_queue_rows,
            paint_refinish_whatsapp_rows,
        )
        images = evidence["primary_images"]
        evidence_sets = evidence["evidence_sets"]
        parts_for_workstream = part_rows_by_workstream.get(ws_id, [])
        involved_parts_rows = sorted(
            [workstream_part_row_payload(part_row) for part_row in parts_for_workstream],
            key=lambda item: (
                norm(item.get("procurement_stage")),
                norm(item.get("status")),
                norm(item.get("item")),
            ),
        )
        operation_panels = []
        subtask_groups = build_workstream_subtask_groups(
            ws_id,
            row,
            images,
            photo_rows,
            parts_for_workstream,
        )
        requirements = []
        if ws_id == "replacement_pipes":
            requirements = build_replacement_pipe_requirements(replacement_pipe_requirement_rows, photo_rows)
        elif ws_id == "chassis_rubbers":
            requirements = build_workstream_requirements(chassis_rubber_requirement_rows, photo_rows)
        elif ws_id == "brake_system":
            requirements = build_workstream_requirements(brake_system_requirement_rows, photo_rows)
        pipe_requirements = requirements if ws_id == "replacement_pipes" else []
        replacement_pipe_order_release_specs = (
            replacement_pipe_order_release_payload(replacement_pipe_order_release_rows)
            if ws_id == "replacement_pipes"
            else []
        )
        replacement_pipe_release_actions = (
            replacement_pipe_release_action_payload(replacement_pipe_release_action_rows)
            if ws_id == "replacement_pipes"
            else []
        )
        replacement_pipe_circuit_closure = (
            replacement_pipe_circuit_closure_payload(replacement_pipe_circuit_closure_rows)
            if ws_id == "replacement_pipes"
            else []
        )
        chassis_rubber_requirements = requirements if ws_id == "chassis_rubbers" else []
        body_mount_order_release_specs = (
            body_mount_order_release_payload(body_mount_order_release_rows)
            if ws_id == "chassis_rubbers"
            else []
        )
        body_mount_release_actions = (
            body_mount_release_action_payload(body_mount_release_action_rows)
            if ws_id == "chassis_rubbers"
            else []
        )
        body_mount_station_closure = (
            body_mount_station_closure_payload(body_mount_station_closure_rows)
            if ws_id == "chassis_rubbers"
            else []
        )
        if ws_id == "chassis_fixing":
            operation_panels.append(build_chassis_prime_readiness_panel(photo_rows))

        workstreams.append(
            {
                "id": ws_id,
                "title": WORKSTREAM_TITLE_OVERRIDES.get(ws_id, title_from_id(ws_id)),
                "phase": clean(row.get("phase")),
                "status": clean(row.get("current_status")),
                "priority": clean(row.get("priority")),
                "primary_location": clean(row.get("primary_location")),
                "owner_mode": clean(row.get("owner_mode")),
                "depends_on": split_pipe(row.get("depends_on", "")),
                "next_action": clean(row.get("next_action")),
                "exit_gate": clean(row.get("exit_gate")),
                "notes": clean(row.get("notes")),
                "evidence_source": split_pipe(row.get("evidence_source", "")),
                "images": images,
                "evidence_sets": evidence_sets,
                "image_count": len(images),
                "reference_token_count": len(reference_tokens),
                "requirements": requirements,
                "pipe_requirements": pipe_requirements,
                "replacement_pipe_order_release_specs": replacement_pipe_order_release_specs,
                "replacement_pipe_release_actions": replacement_pipe_release_actions,
                "replacement_pipe_circuit_closure": replacement_pipe_circuit_closure,
                "chassis_rubber_requirements": chassis_rubber_requirements,
                "body_mount_order_release_specs": body_mount_order_release_specs,
                "body_mount_release_actions": body_mount_release_actions,
                "body_mount_station_closure": body_mount_station_closure,
                "linked_packages": [
                    {
                        "work_package_id": clean(package.get("work_package_id")),
                        "title": clean(package.get("title")),
                        "lane": clean(package.get("lane")),
                        "current_state": clean(package.get("current_state")),
                        "objective": clean(package.get("objective")),
                        "blocker_summary": clean(package.get("blocker_summary")),
                        "gate_to_close": clean(package.get("gate_to_close")),
                        "key_procurement_actions": clean(package.get("key_procurement_actions")),
                        "evidence_signal": clean(package.get("evidence_signal")),
                    }
                    for package in linked_packages
                ],
                "component_jobs": [
                    {
                        "component_job_id": clean(job.get("component_job_id")),
                        "component_group": clean(job.get("component_group")),
                        "current_status": clean(job.get("current_status")),
                        "planned_action": clean(job.get("planned_action")),
                        "evidence_ref": clean(job.get("evidence_ref")),
                        "notes": clean(job.get("notes")),
                    }
                    for job in jobs
                ],
                "issue_jobs": [
                    {
                        "component_job_id": clean(issue.get("component_job_id")),
                        "component_group": clean(issue.get("component_group")),
                        "current_status": clean(issue.get("current_status")),
                        "planned_action": clean(issue.get("planned_action")),
                        "evidence_ref": clean(issue.get("evidence_ref")),
                        "notes": clean(issue.get("notes")),
                    }
                    for issue in issues
                ],
                "steps": workstream_steps(row, linked_packages, jobs, issues, parts_for_workstream),
                "involved_parts": involved_parts_rows,
                "operation_panels": operation_panels,
                "subtask_groups": subtask_groups,
                "electrical_spec_layout": electrical_spec_layout_by_workstream.get(ws_id),
            }
        )

    project_steps = sorted(
        [
            {
                "work_package_id": clean(row.get("work_package_id")),
                "title": clean(row.get("title")),
                "lane": clean(row.get("lane")),
                "objective": clean(row.get("objective")),
                "current_state": clean(row.get("current_state")),
                "depends_on": split_pipe(row.get("depends_on", "")),
                "linked_workstreams": split_pipe(row.get("linked_workstreams", "")),
                "evidence_signal": clean(row.get("evidence_signal")),
                "blocker_summary": clean(row.get("blocker_summary")),
                "gate_to_close": clean(row.get("gate_to_close")),
                "key_procurement_actions": clean(row.get("key_procurement_actions")),
            }
            for row in package_rows
        ],
        key=lambda value: value["work_package_id"],
    )

    workstream_image_by_id: dict[str, list[dict[str, Any]]] = {row["id"]: row["images"] for row in workstreams}
    workstream_default_images: dict[str, dict[str, Any]] = {
        ws_id: images[0] for ws_id, images in workstream_image_by_id.items() if images
    }
    for step in project_steps:
        linked = step["linked_workstreams"]
        image: dict[str, str] | None = None
        for ws_id in linked:
            ws_images = workstream_image_by_id.get(ws_id, [])
            if ws_images:
                image = ws_images[0]
                break
        step["image"] = image

    for workstream in workstreams:
        involved_parts = list(workstream.get("involved_parts") or [])
        if not involved_parts:
            continue
        workstream["involved_parts"] = attach_inventory_images(
            involved_parts,
            photo_rows,
            workstream_default_images,
            selling_site_manifest_rows,
            whatsapp_j40_media_rows,
            inventory_image_overrides,
        )

    photo_taxonomy = {
        "component_groups": sorted({clean(row.get("component_group")) for row in photo_rows if is_photo_row(row)}),
        "specific_components": sorted({clean(row.get("specific_component")) for row in photo_rows if is_photo_row(row)}),
        "stages": sorted({clean(row.get("stage")) for row in photo_rows if is_photo_row(row)}),
        "observed_states": sorted({clean(row.get("observed_state")) for row in photo_rows if is_photo_row(row)}),
        "confidence_values": sorted({clean(row.get("confidence")) for row in photo_rows if is_photo_row(row)}),
    }
    photo_lookup: dict[str, dict[str, Any]] = {}
    for row in photo_rows:
        if not is_photo_row(row):
            continue
        media_id = clean(row.get("media_id"))
        if not media_id:
            continue
        photo_lookup[media_id] = {
            "media_id": media_id,
            "file_name": clean(row.get("file_name")),
            "path": path_for_ui(clean(row.get("relative_path"))),
            "captured_date": clean(row.get("captured_date")),
            "captured_time": clean(row.get("captured_time")),
            "media_type": clean(row.get("media_type")) or "photo",
            "component_group": clean(row.get("component_group")),
            "specific_component": clean(row.get("specific_component")),
            "stage": clean(row.get("stage")),
            "observed_state": clean(row.get("observed_state")),
            "confidence": clean(row.get("confidence")),
            "tags": clean(row.get("tags")),
            "notes": clean(row.get("notes")),
        }

    open_part_rows = [
        row
        for row in part_rows
        if norm(row.get("procurement_stage")) not in {"received", "completed"}
        and norm(row.get("status")) not in {"received", "installed", "credited"}
    ]

    ordered_pending_rows = [
        row
        for row in part_rows
        if norm(row.get("procurement_stage")) == "ordered_pending_delivery"
        or norm(row.get("delivery_status")) == "pending_delivery"
    ]

    counts_by_stage = Counter(clean(row.get("procurement_stage")) or "unknown" for row in open_part_rows)
    counts_by_workstream = Counter(
        split_legacy_steering_brakes_workstream(
            clean(row.get("workstream")),
            category=clean(row.get("category")),
            item=clean(row.get("item")),
            notes=clean(row.get("notes")),
        )
        or "unassigned"
        for row in open_part_rows
    )
    counts_by_next_action = Counter(clean(row.get("next_action")) or "unspecified" for row in buy_now_rows)

    parts_steps = [
        {
            "label": "Close spec-ready release holds",
            "status": "in_progress" if counts_by_stage.get("spec_ready_release_hold", 0) > 0 else "completed",
            "detail": f"{counts_by_stage.get('spec_ready_release_hold', 0)} spec-ready rows still need release actions before purchase.",
        },
        {
            "label": "Confirm price and place purchase-ready orders",
            "status": "in_progress" if counts_by_stage.get("purchase_ready", 0) > 0 else "completed",
            "detail": f"{counts_by_stage.get('purchase_ready', 0)} rows still in purchase_ready.",
        },
        {
            "label": "Place selected quote orders",
            "status": "in_progress" if counts_by_next_action.get("order_from_selected_quote", 0) > 0 else "completed",
            "detail": f"{counts_by_next_action.get('order_from_selected_quote', 0)} quote rows pending order.",
        },
        {
            "label": "Track paid / in-flight deliveries",
            "status": "in_progress" if len(ordered_pending_rows) > 0 else "completed",
            "detail": f"{len(ordered_pending_rows)} rows ordered and waiting to arrive.",
        },
    ]

    urgent_actions = sorted(
        [
            {
                "priority": clean(row.get("priority")),
                "entry_id": clean(row.get("entry_id")),
                "workstream": split_legacy_steering_brakes_workstream(
                    clean(row.get("workstream")),
                    category=clean(expense_by_entry_id.get(clean(row.get("entry_id")), {}).get("category")),
                    item=clean(row.get("item")),
                    notes=clean(expense_by_entry_id.get(clean(row.get("entry_id")), {}).get("notes")),
                ),
                "item": clean(row.get("item")),
                "status": clean(row.get("status")),
                "procurement_stage": clean(row.get("procurement_stage")),
                "next_action": clean(row.get("next_action")),
                "amount": clean(row.get("amount")),
                "amount_status": clean(row.get("amount_status")),
                "currency": clean(row.get("currency")) or "PKR",
                "vendor": clean(row.get("company")),
                "supply_type": "part",
                "evidence_ref": clean(row.get("evidence_ref")) or clean(expense_by_entry_id.get(clean(row.get("entry_id")), {}).get("evidence_ref")),
                "notes": clean(expense_by_entry_id.get(clean(row.get("entry_id")), {}).get("notes")),
            }
            for row in buy_now_rows
            if clean(row.get("priority")) == "P0" or clean(row.get("next_action")) in {"order_from_selected_quote", "track_delivery"}
        ],
        key=lambda row: (row["priority"], row["workstream"], row["item"]),
    )

    open_rows_for_table = sorted(
        [
            {
                "entry_id": clean(row.get("entry_id")),
                "workstream": split_legacy_steering_brakes_workstream(
                    clean(row.get("workstream")),
                    category=clean(row.get("category")),
                    item=clean(row.get("item")),
                    notes=clean(row.get("notes")),
                ),
                "item": clean(row.get("item")),
                "status": clean(row.get("status")),
                "procurement_stage": clean(row.get("procurement_stage")),
                "payment_status": clean(row.get("payment_status")),
                "delivery_status": clean(row.get("delivery_status")),
                "amount": clean(row.get("amount")),
                "amount_status": clean(row.get("amount_status")),
                "currency": clean(row.get("currency")) or "PKR",
                "vendor": clean(row.get("company")),
                "supply_type": "part",
                "evidence_ref": clean(row.get("evidence_ref")),
                "notes": clean(row.get("notes")),
            }
            for row in open_part_rows
        ],
        key=lambda row: (row["workstream"], row["procurement_stage"], row["item"]),
    )

    ordered_pending_table = sorted(
        [
            {
                "entry_id": clean(row.get("entry_id")),
                "workstream": split_legacy_steering_brakes_workstream(
                    clean(row.get("workstream")),
                    category=clean(row.get("category")),
                    item=clean(row.get("item")),
                    notes=clean(row.get("notes")),
                ),
                "item": clean(row.get("item")),
                "status": clean(row.get("status")),
                "procurement_stage": clean(row.get("procurement_stage")),
                "payment_status": clean(row.get("payment_status")),
                "delivery_status": clean(row.get("delivery_status")),
                "expected_delivery_date": clean(row.get("expected_delivery_date")),
                "amount": clean(row.get("amount")),
                "amount_status": clean(row.get("amount_status")),
                "currency": clean(row.get("currency")) or "PKR",
                "vendor": clean(row.get("company")),
                "supply_type": "part",
                "evidence_ref": clean(row.get("evidence_ref")),
                "notes": clean(row.get("notes")),
            }
            for row in ordered_pending_rows
        ],
        key=lambda row: (row["workstream"], row["item"]),
    )

    urgent_actions = attach_inventory_images(
        urgent_actions,
        photo_rows,
        workstream_default_images,
        selling_site_manifest_rows,
        whatsapp_j40_media_rows,
        inventory_image_overrides,
    )
    open_rows_for_table = attach_inventory_images(
        open_rows_for_table,
        photo_rows,
        workstream_default_images,
        selling_site_manifest_rows,
        whatsapp_j40_media_rows,
        inventory_image_overrides,
    )
    ordered_pending_table = attach_inventory_images(
        ordered_pending_table,
        photo_rows,
        workstream_default_images,
        selling_site_manifest_rows,
        whatsapp_j40_media_rows,
        inventory_image_overrides,
    )

    supplies_rows_by_status_with_images: dict[str, list[dict[str, Any]]] = {}
    for status_group, rows in supplies_inventory["rows_by_status"].items():
        supplies_rows_by_status_with_images[status_group] = attach_inventory_images(
            rows,
            photo_rows,
            workstream_default_images,
            selling_site_manifest_rows,
            whatsapp_j40_media_rows,
            inventory_image_overrides,
        )
    supplies_all_rows_with_images = attach_inventory_images(
        supplies_inventory["all_rows"],
        photo_rows,
        workstream_default_images,
        selling_site_manifest_rows,
        whatsapp_j40_media_rows,
        inventory_image_overrides,
    )
    supplies_inventory = {
        "summary_by_type": supplies_inventory["summary_by_type"],
        "rows_by_status": supplies_rows_by_status_with_images,
        "inventory_groups": supplies_inventory.get("inventory_groups", list(INVENTORY_GROUP_ORDER)),
        "all_rows": supplies_all_rows_with_images,
    }

    parts_workstream_cards = []
    for ws_id, count in sorted(counts_by_workstream.items(), key=lambda item: (-item[1], item[0])):
        ws_images = workstream_image_by_id.get(ws_id, [])
        parts_workstream_cards.append(
            {
                "workstream": ws_id,
                "open_count": count,
                "image": ws_images[0] if ws_images else None,
            }
        )
    procurement_evidence_images = build_procurement_evidence_images(photo_rows)

    whatsapp_selected_chats = [
        row
        for row in whatsapp_j40_chat_rows
        if norm(row.get("selected_for_import")) == "true"
    ]
    whatsapp_media_counts_by_type = Counter(
        clean(row.get("media_type")) or "unknown"
        for row in whatsapp_j40_media_rows
    )
    whatsapp_media_counts_by_profile = Counter(
        clean(row.get("source_profile")) or "unknown"
        for row in whatsapp_j40_media_rows
    )
    whatsapp_recent_media = sorted(
        [
            {
                "media_id": clean(row.get("media_id")),
                "source_profile": clean(row.get("source_profile")),
                "chat_name": clean(row.get("chat_name")),
                "timestamp": clean(row.get("timestamp")),
                "media_type": clean(row.get("media_type")),
                "file_name": clean(row.get("file_name")),
                "path": path_for_ui(clean(row.get("relative_path"))),
            }
            for row in whatsapp_j40_media_rows
            if clean(row.get("relative_path"))
        ],
        key=lambda value: (value["timestamp"], value["media_id"]),
        reverse=True,
    )[:24]

    data = {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "source_files": {
            "workstream_status": "data/manual/workstream_status.csv",
            "reassembly_work_packages": "data/manual/reassembly_work_packages.csv",
            "component_jobs": "data/manual/component_jobs.csv",
            "photo_inventory": "data/manual/photo_inventory.csv",
            "brake_system_requirements": "data/manual/brake_system_requirements.csv",
            "chassis_rubber_requirements": "data/manual/chassis_rubber_requirements.csv",
            "rubber_ordering_specs": "data/manual/rubber_ordering_specs.csv",
            "body_mount_order_release_specs": "data/manual/body_mount_order_release_specs.csv",
            "body_mount_release_actions": "data/manual/body_mount_release_actions.csv",
            "body_mount_station_closure_sheet": "data/manual/body_mount_station_closure_sheet.csv",
            "replacement_pipe_ordering_specs": "data/manual/replacement_pipe_ordering_specs.csv",
            "replacement_pipe_order_release_specs": "data/manual/replacement_pipe_order_release_specs.csv",
            "replacement_pipe_release_actions": "data/manual/replacement_pipe_release_actions.csv",
            "replacement_pipe_circuit_closure_sheet": "data/manual/replacement_pipe_circuit_closure_sheet.csv",
            "expenses": "data/manual/expenses.csv",
            "parts_buy_now_this_week": "data/manual/parts_buy_now_this_week.csv",
            "workbook_electrical_master": "data/manual/workbook_tabs/electrical_master.csv",
            "workbook_electrical_templates": "data/manual/workbook_tabs/electrical_templates.csv",
            "selling_site_manifest": "deliverables/selling_site_images/manifest.csv",
            "whatsapp_j40_chat_candidates": "data/manual/whatsapp_j40_chat_candidates.csv",
            "whatsapp_j40_media_index": "data/processed/generated/mcp_whatsapp_j40_media_index.csv",
        },
        "summary": {
            "workstreams_in_scope": len(workstreams),
            "workstreams_active": sum(1 for row in workstreams if norm(row["status"]) == "in_progress"),
            "workstream_evidence_images": sum(int(row.get("image_count", 0)) for row in workstreams),
            "parts_open_rows": len(open_rows_for_table),
            "parts_ordered_pending_delivery": len(ordered_pending_table),
            "urgent_part_actions": len(urgent_actions),
            "supply_rows_tracked": len(supplies_inventory["all_rows"]),
            "selling_site_images_loaded": sum(1 for row in selling_site_manifest_rows if clean(row.get("local_path"))),
            "whatsapp_j40_selected_chats": len(whatsapp_selected_chats),
            "whatsapp_j40_media_items": len(whatsapp_j40_media_rows),
            "whatsapp_j40_media_images": whatsapp_media_counts_by_type.get("photo", 0),
            "whatsapp_j40_media_videos": whatsapp_media_counts_by_type.get("video", 0),
        },
        "workstreams": workstreams,
        "project_steps": project_steps,
        "parts": {
            "steps": parts_steps,
            "counts_by_procurement_stage": [
                {"stage": stage, "count": count} for stage, count in sorted(counts_by_stage.items())
            ],
            "counts_by_next_action": [
                {"next_action": action, "count": count} for action, count in sorted(counts_by_next_action.items())
            ],
            "urgent_actions": urgent_actions,
            "ordered_pending_delivery": ordered_pending_table,
            "open_rows": open_rows_for_table,
            "open_counts_by_workstream": parts_workstream_cards,
            "procurement_evidence_images": procurement_evidence_images,
        },
        "supplies": supplies_inventory,
        "whatsapp_j40": {
            "selected_chats": sorted(
                [
                    {
                        "profile_server": clean(row.get("profile_server")),
                        "chat_name": clean(row.get("chat_name")),
                        "chat_id": clean(row.get("chat_id")),
                        "chat_type": clean(row.get("chat_type")),
                        "relevance_score": clean(row.get("relevance_score")),
                        "messages_fetched": clean(row.get("messages_fetched")),
                        "messages_count": clean(row.get("messages_count")),
                        "media_count": clean(row.get("media_count")),
                        "messages_fetch_error": clean(row.get("messages_fetch_error")),
                    }
                    for row in whatsapp_selected_chats
                ],
                key=lambda row: (
                    -(int(clean(row.get("relevance_score")) or "0")),
                    clean(row.get("profile_server")),
                    clean(row.get("chat_name")),
                ),
            ),
            "media_counts_by_type": [
                {"media_type": media_type, "count": count}
                for media_type, count in sorted(whatsapp_media_counts_by_type.items())
            ],
            "media_counts_by_profile": [
                {"source_profile": profile_name, "count": count}
                for profile_name, count in sorted(whatsapp_media_counts_by_profile.items())
            ],
            "recent_media": whatsapp_recent_media,
        },
        "photo_taxonomy": photo_taxonomy,
        "photo_lookup": photo_lookup,
        "meta": {
            "primary_workstream_ids": selected_workstream_ids,
            "workstream_image_profiles": {
                ws_id: {
                    "component_groups": sorted(profile["component_groups"]),
                    "stages": sorted(profile["stages"]),
                    "keywords": sorted(profile["keywords"]),
                }
                for ws_id, profile in WORKSTREAM_IMAGE_PROFILES.items()
            },
        },
    }
    return data


def write_data_js(data: dict[str, Any]) -> None:
    UI_DIR.mkdir(parents=True, exist_ok=True)
    payload = "window.J40_DASHBOARD_DATA = " + json.dumps(data, ensure_ascii=True, indent=2) + ";\n"
    OUTPUT_DATA_JS_PATH.write_text(payload, encoding="utf-8")


def main() -> None:
    data = build_dashboard_data()
    write_data_js(data)
    print(f"Wrote dashboard data: {OUTPUT_DATA_JS_PATH}")
    print(
        "Summary: "
        f"{data['summary']['workstreams_in_scope']} workstreams, "
        f"{data['summary']['parts_open_rows']} open parts rows, "
        f"{data['summary']['urgent_part_actions']} urgent part actions"
    )


if __name__ == "__main__":
    main()
