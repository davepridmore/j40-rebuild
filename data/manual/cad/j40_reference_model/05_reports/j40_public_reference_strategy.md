# J40 Public Reference Strategy

- Generated: 2026-05-30T22:07:08.291015+00:00
- CSV: `data/manual/cad/j40_reference_model/05_reports/j40_public_reference_strategy.csv`

## Decision

Use a source hierarchy, not a large undifferentiated scrape. Official Toyota sources control names and applicability. Project photos and measured datums control this truck. CC/open 3D models control visual comparison only. Community CAD is a dimensional lead until verified against the truck.

## Source Hierarchy

### 100 - Toyota GR Heritage Land Cruiser 40 page

- URL: https://toyotagazooracing.com/gr/heritage/landcruiser40/
- Class: official Toyota current parts program
- Trust tier: A
- Permission basis: public Toyota page; factual product and parts-program information
- Best use: current official part names, availability signals, model applicability clues, and category vocabulary
- Do not use for: hidden geometry, CAD surfaces, or exact dimensions
- Next action: Keep linked as the official current reference and re-check before ordering or modelling newly reproduced parts.

### 98 - Land Cruiser 40 GR Heritage Parts List

- URL: https://toyotagazooracing.com/-/media/TMC/tgr/global/contents/gr/heritage/pdf/Landcruiser40_en.pdf
- Class: official Toyota parts PDF
- Trust tier: A
- Permission basis: public Toyota PDF; factual part names, part numbers, and application rows
- Best use: part naming, model/year applicability, RHD/LHD clues, brake, lamp, glass, grille, cable, and rubber identity checks
- Do not use for: drawing exact shape from the PDF or assuming every part applies to this specific truck
- Next action: Parse item names into model notes and use part applicability to challenge photo-based assumptions.

### 88 - Toyota EPC-data Land Cruiser FJ40 catalog mirror

- URL: https://toyota.epc-data.com/land_cruiser/
- Class: public EPC-style catalog
- Trust tier: B
- Permission basis: public catalog mirror; use as factual/service-reference cue, not redistributed content
- Best use: exploded group structure, part location vocabulary, fastener group names, body/interior/fuel/brake assemblies
- Do not use for: exact model geometry, unchecked part applicability, or image redistribution
- Next action: Use to split model groups into Toyota-style assemblies and add missing service-reference labels.

### 82 - Toyota Land Cruiser FJ40/FJ45 parts catalog scan

- URL: https://www.theoldcruiser.com/wp-content/uploads/2020/01/ToyotaLandCruiserFJ40-PartsCatalog-Nov1967-opt.pdf
- Class: public historical parts catalog scan
- Trust tier: B
- Permission basis: public scan; use only for factual part relationships and model applicability notes
- Best use: early hardtop/RHD parts relationships, assemblies, and naming cross-checks
- Do not use for: copying diagrams into the repo or treating 1967 details as correct for later BJ/FJ variants
- Next action: Use only when Toyota current/epc sources leave a naming or assembly ambiguity.

### 80 - 1976 Toyota Land Cruiser FJ40 by tonielpro520

- URL: https://sketchfab.com/3d-models/1976-toyota-land-cruiser-fj40-a4e58b09ce48444ca6164834c310880d
- Class: downloadable open 3D model
- Trust tier: B
- Permission basis: Creative Commons Attribution 4.0; author credit required; authenticated download needed
- Best use: overall hardtop silhouette, body-tub packaging, visual proportions, and manual remodelling reference
- Do not use for: uncredited redistribution, direct hidden mesh copying into fabrication release, or exact truck dimensions
- Next action: Download only through the authenticated workflow, place ZIP in 00_inbox, and keep attribution with derivatives.

### 76 - Toyota Land Cruiser by Game Garage

- URL: https://sketchfab.com/3d-models/toyota-land-cruiser-cbcbd901e8874205b5be294fa3dd3df2
- Class: downloadable game-ready open 3D model
- Trust tier: B
- Permission basis: Sketchfab Creative Commons Attribution listing; author credit required
- Best use: material separation, interior/trim cues, wheel/tire texture cues, and low-poly comparison geometry
- Do not use for: fabrication dimensions or uncredited redistribution
- Next action: Use as a second visual mesh after local download; compare only against project photos and measured datums.

### 72 - IH8MUD FJ40 frame CAD model thread

- URL: https://forum.ih8mud.com/threads/a-lot-of-people-have-been-asking-for-this-cad-model-for-fj40-frame.798358/
- Class: community CAD/dimensional lead
- Trust tier: B-
- Permission basis: public forum post; per-file rights and accuracy must be verified before local use
- Best use: candidate frame rail, crossmember, and bracket datums to compare against physical measurements
- Do not use for: blind import as authoritative geometry or redistribution without checking file permission
- Next action: Create a frame-datum comparison worksheet before using any geometry.

### 62 - IH8MUD chassis/frame dimensions discussion

- URL: https://forum.ih8mud.com/threads/chassis-frame-dimensions-fj40.499/
- Class: community dimensional lead
- Trust tier: C+
- Permission basis: public discussion; linked diagrams and claims are mixed confidence
- Best use: finding possible Toyota frame-chart leads and measurement targets
- Do not use for: final frame dimensions without physical verification
- Next action: Use as a search index for frame measurements, not as model truth.

### 60 - IH8MUD 40 Series 3D print and CAD file repository

- URL: https://forum.ih8mud.com/threads/3d-print-and-cad-file-repository-40-series.1281295/
- Class: community CAD/STL repository
- Trust tier: C+
- Permission basis: public forum links; per-file licenses vary
- Best use: small part modelling leads such as knobs, covers, bezels, hose separators, and license lamp covers
- Do not use for: assuming scale, side, or year correctness without checking each file
- Next action: Harvest only named small-parts after a per-file permission and fitment check.

### 48 - 3DModels.org Toyota Land Cruiser J40 Hard Top 1979 preview gallery

- URL: https://3dmodels.org/3d-models/toyota-land-cruiser-j40-hard-top-1979/
- Class: commercial model preview
- Trust tier: C
- Permission basis: commercial/public preview; project owner indicated commercial coverage, but local source files are not present
- Best use: orthographic visual cues, rounded rear glazing, grille/lamp proportions, and material breaks
- Do not use for: mesh extraction, redistribution, or fabrication dimensions
- Next action: Keep as visual benchmark only unless licensed files are added locally.

### 45 - CGTrader Toyota Land-Cruiser J40 Hard Top BJ44V 1979 printable listing

- URL: https://www.cgtrader.com/3d-print-models/hobby-diy/automotive/toyota-land-cruiser-j40-hard-top-bj44v-1979-df76b215-58fa-40f4-82f4-811350605600
- Class: commercial model listing
- Trust tier: C
- Permission basis: commercial listing; source asset not present locally
- Best use: part breakdown cues and open-hood/chassis visual targets
- Do not use for: unlicensed geometry use or exact dimensional claims
- Next action: Use only as a public visual/listing cue until purchased files are placed in the intake folder.

### 38 - FJ40 restoration suppliers and aftermarket body/frame references

- URL: https://www.fjparts.com/body.htm
- Class: supplier/reference catalog
- Trust tier: C
- Permission basis: public supplier pages; commercial catalog content
- Best use: body panel naming, availability, and practical restoration grouping
- Do not use for: drawing geometry or assuming aftermarket parts match this truck exactly
- Next action: Use as procurement/restoration vocabulary, not as geometry source.

## Build Rules

- Treat official Toyota part names and application rows as high-trust facts, but still check that the row applies to this truck.
- Treat public EPC and historical catalogs as assembly and naming references; do not copy diagrams into repo artifacts.
- Treat CC/open 3D models as visual reference meshes and attribution-bound source material, not fabrication-ready CAD.
- Treat forum CAD and dimension posts as measurement leads until checked against our chassis, tub, and Toyota dimensions.
- Treat commercial model galleries as visual benchmarks only unless licensed source files are placed in `00_inbox/`.
- Close exact geometry only with measured datums, known Toyota dimensions, or calibrated photogrammetry.

## Recommended Next Model Pass

1. Use Toyota GR/EPC names to normalize part labels in the scaffold and backlog.
2. Make a frame-datum worksheet from the IH8MUD frame CAD/dimension leads, then fill it with measurements from the actual truck.
3. Download the CC Sketchfab models locally through authenticated channels and compare them as visual overlays, preserving attribution.
4. Prioritize measurement closure for front disc brakes, frame rails/crossmembers, body mounts, roof/gutter apertures, firewall holes, and window/rubber channels.
5. Promote only measured or verified items from visual scaffold to fabrication-grade CAD.
