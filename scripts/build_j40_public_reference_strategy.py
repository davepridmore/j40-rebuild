#!/usr/bin/env python3
"""Write the public-source strategy for the J40 digital twin."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "data" / "manual" / "cad" / "j40_reference_model" / "05_reports"
STRATEGY_CSV = REPORT_DIR / "j40_public_reference_strategy.csv"
STRATEGY_MD = REPORT_DIR / "j40_public_reference_strategy.md"


@dataclass(frozen=True)
class Source:
    source_id: str
    title: str
    url: str
    source_class: str
    trust_tier: str
    score: int
    permission_basis: str
    best_use: str
    do_not_use_for: str
    next_action: str


SOURCES = [
    Source(
        "toyota-gr-heritage-40-page",
        "Toyota GR Heritage Land Cruiser 40 page",
        "https://toyotagazooracing.com/gr/heritage/landcruiser40/",
        "official Toyota current parts program",
        "A",
        100,
        "public Toyota page; factual product and parts-program information",
        "current official part names, availability signals, model applicability clues, and category vocabulary",
        "hidden geometry, CAD surfaces, or exact dimensions",
        "Keep linked as the official current reference and re-check before ordering or modelling newly reproduced parts.",
    ),
    Source(
        "toyota-gr-heritage-40-parts-list-2026",
        "Land Cruiser 40 GR Heritage Parts List",
        "https://toyotagazooracing.com/-/media/TMC/tgr/global/contents/gr/heritage/pdf/Landcruiser40_en.pdf",
        "official Toyota parts PDF",
        "A",
        98,
        "public Toyota PDF; factual part names, part numbers, and application rows",
        "part naming, model/year applicability, RHD/LHD clues, brake, lamp, glass, grille, cable, and rubber identity checks",
        "drawing exact shape from the PDF or assuming every part applies to this specific truck",
        "Parse item names into model notes and use part applicability to challenge photo-based assumptions.",
    ),
    Source(
        "toyota-epc-data-fj40",
        "Toyota EPC-data Land Cruiser FJ40 catalog mirror",
        "https://toyota.epc-data.com/land_cruiser/",
        "public EPC-style catalog",
        "B",
        88,
        "public catalog mirror; use as factual/service-reference cue, not redistributed content",
        "exploded group structure, part location vocabulary, fastener group names, body/interior/fuel/brake assemblies",
        "exact model geometry, unchecked part applicability, or image redistribution",
        "Use to split model groups into Toyota-style assemblies and add missing service-reference labels.",
    ),
    Source(
        "oldcruiser-1967-fj40-parts-catalog",
        "Toyota Land Cruiser FJ40/FJ45 parts catalog scan",
        "https://www.theoldcruiser.com/wp-content/uploads/2020/01/ToyotaLandCruiserFJ40-PartsCatalog-Nov1967-opt.pdf",
        "public historical parts catalog scan",
        "B",
        82,
        "public scan; use only for factual part relationships and model applicability notes",
        "early hardtop/RHD parts relationships, assemblies, and naming cross-checks",
        "copying diagrams into the repo or treating 1967 details as correct for later BJ/FJ variants",
        "Use only when Toyota current/epc sources leave a naming or assembly ambiguity.",
    ),
    Source(
        "sketchfab-tonielpro520-1976-fj40",
        "1976 Toyota Land Cruiser FJ40 by tonielpro520",
        "https://sketchfab.com/3d-models/1976-toyota-land-cruiser-fj40-a4e58b09ce48444ca6164834c310880d",
        "downloadable open 3D model",
        "B",
        80,
        "Creative Commons Attribution 4.0; author credit required; authenticated download needed",
        "overall hardtop silhouette, body-tub packaging, visual proportions, and manual remodelling reference",
        "uncredited redistribution, direct hidden mesh copying into fabrication release, or exact truck dimensions",
        "Download only through the authenticated workflow, place ZIP in 00_inbox, and keep attribution with derivatives.",
    ),
    Source(
        "sketchfab-game-garage-fj40",
        "Toyota Land Cruiser by Game Garage",
        "https://sketchfab.com/3d-models/toyota-land-cruiser-cbcbd901e8874205b5be294fa3dd3df2",
        "downloadable game-ready open 3D model",
        "B",
        76,
        "Sketchfab Creative Commons Attribution listing; author credit required",
        "material separation, interior/trim cues, wheel/tire texture cues, and low-poly comparison geometry",
        "fabrication dimensions or uncredited redistribution",
        "Use as a second visual mesh after local download; compare only against project photos and measured datums.",
    ),
    Source(
        "ih8mud-fj40-frame-cad-thread",
        "IH8MUD FJ40 frame CAD model thread",
        "https://forum.ih8mud.com/threads/a-lot-of-people-have-been-asking-for-this-cad-model-for-fj40-frame.798358/",
        "community CAD/dimensional lead",
        "B-",
        72,
        "public forum post; per-file rights and accuracy must be verified before local use",
        "candidate frame rail, crossmember, and bracket datums to compare against physical measurements",
        "blind import as authoritative geometry or redistribution without checking file permission",
        "Create a frame-datum comparison worksheet before using any geometry.",
    ),
    Source(
        "ih8mud-frame-dimensions-thread",
        "IH8MUD chassis/frame dimensions discussion",
        "https://forum.ih8mud.com/threads/chassis-frame-dimensions-fj40.499/",
        "community dimensional lead",
        "C+",
        62,
        "public discussion; linked diagrams and claims are mixed confidence",
        "finding possible Toyota frame-chart leads and measurement targets",
        "final frame dimensions without physical verification",
        "Use as a search index for frame measurements, not as model truth.",
    ),
    Source(
        "ih8mud-40-series-cad-repository",
        "IH8MUD 40 Series 3D print and CAD file repository",
        "https://forum.ih8mud.com/threads/3d-print-and-cad-file-repository-40-series.1281295/",
        "community CAD/STL repository",
        "C+",
        60,
        "public forum links; per-file licenses vary",
        "small part modelling leads such as knobs, covers, bezels, hose separators, and license lamp covers",
        "assuming scale, side, or year correctness without checking each file",
        "Harvest only named small-parts after a per-file permission and fitment check.",
    ),
    Source(
        "3dmodels-1979-j40-hard-top",
        "3DModels.org Toyota Land Cruiser J40 Hard Top 1979 preview gallery",
        "https://3dmodels.org/3d-models/toyota-land-cruiser-j40-hard-top-1979/",
        "commercial model preview",
        "C",
        48,
        "commercial/public preview; project owner indicated commercial coverage, but local source files are not present",
        "orthographic visual cues, rounded rear glazing, grille/lamp proportions, and material breaks",
        "mesh extraction, redistribution, or fabrication dimensions",
        "Keep as visual benchmark only unless licensed files are added locally.",
    ),
    Source(
        "cgtrader-bj44v-1979-printable",
        "CGTrader Toyota Land-Cruiser J40 Hard Top BJ44V 1979 printable listing",
        "https://www.cgtrader.com/3d-print-models/hobby-diy/automotive/toyota-land-cruiser-j40-hard-top-bj44v-1979-df76b215-58fa-40f4-82f4-811350605600",
        "commercial model listing",
        "C",
        45,
        "commercial listing; source asset not present locally",
        "part breakdown cues and open-hood/chassis visual targets",
        "unlicensed geometry use or exact dimensional claims",
        "Use only as a public visual/listing cue until purchased files are placed in the intake folder.",
    ),
    Source(
        "supplier-restoration-reference",
        "FJ40 restoration suppliers and aftermarket body/frame references",
        "https://www.fjparts.com/body.htm",
        "supplier/reference catalog",
        "C",
        38,
        "public supplier pages; commercial catalog content",
        "body panel naming, availability, and practical restoration grouping",
        "drawing geometry or assuming aftermarket parts match this truck exactly",
        "Use as procurement/restoration vocabulary, not as geometry source.",
    ),
]


def write_csv() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "rank",
        "source_id",
        "title",
        "url",
        "source_class",
        "trust_tier",
        "score",
        "permission_basis",
        "best_use",
        "do_not_use_for",
        "next_action",
    ]
    ordered = sorted(SOURCES, key=lambda source: (-source.score, source.source_id))
    with STRATEGY_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for rank, source in enumerate(ordered, start=1):
            writer.writerow({"rank": rank, **source.__dict__})


def write_markdown() -> None:
    ordered = sorted(SOURCES, key=lambda source: (-source.score, source.source_id))
    lines = [
        "# J40 Public Reference Strategy",
        "",
        f"- Generated: {datetime.now(timezone.utc).isoformat()}",
        f"- CSV: `{STRATEGY_CSV.relative_to(ROOT)}`",
        "",
        "## Decision",
        "",
        "Use a source hierarchy, not a large undifferentiated scrape. Official Toyota sources control names and applicability. Project photos and measured datums control this truck. CC/open 3D models control visual comparison only. Community CAD is a dimensional lead until verified against the truck.",
        "",
        "## Source Hierarchy",
        "",
    ]
    for source in ordered:
        lines.extend(
            [
                f"### {source.score} - {source.title}",
                "",
                f"- URL: {source.url}",
                f"- Class: {source.source_class}",
                f"- Trust tier: {source.trust_tier}",
                f"- Permission basis: {source.permission_basis}",
                f"- Best use: {source.best_use}",
                f"- Do not use for: {source.do_not_use_for}",
                f"- Next action: {source.next_action}",
                "",
            ]
        )
    lines.extend(
        [
            "## Build Rules",
            "",
            "- Treat official Toyota part names and application rows as high-trust facts, but still check that the row applies to this truck.",
            "- Treat public EPC and historical catalogs as assembly and naming references; do not copy diagrams into repo artifacts.",
            "- Treat CC/open 3D models as visual reference meshes and attribution-bound source material, not fabrication-ready CAD.",
            "- Treat forum CAD and dimension posts as measurement leads until checked against our chassis, tub, and Toyota dimensions.",
            "- Treat commercial model galleries as visual benchmarks only unless licensed source files are placed in `00_inbox/`.",
            "- Close exact geometry only with measured datums, known Toyota dimensions, or calibrated photogrammetry.",
            "",
            "## Recommended Next Model Pass",
            "",
            "1. Use Toyota GR/EPC names to normalize part labels in the scaffold and backlog.",
            "2. Make a frame-datum worksheet from the IH8MUD frame CAD/dimension leads, then fill it with measurements from the actual truck.",
            "3. Download the CC Sketchfab models locally through authenticated channels and compare them as visual overlays, preserving attribution.",
            "4. Prioritize measurement closure for front disc brakes, frame rails/crossmembers, body mounts, roof/gutter apertures, firewall holes, and window/rubber channels.",
            "5. Promote only measured or verified items from visual scaffold to fabrication-grade CAD.",
        ]
    )
    STRATEGY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    write_csv()
    write_markdown()
    print(f"Wrote {STRATEGY_CSV.relative_to(ROOT)}")
    print(f"Wrote {STRATEGY_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
