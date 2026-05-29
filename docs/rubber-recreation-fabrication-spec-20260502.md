# Rubber Recreation Fabrication Spec - 2026-05-02

Scope: custom recreation of the J40 body-mount/front-support rubber parts from the May 2 tape-measure photos.

Source image set: Google Photos import `20260502T013759`.

Data table: `data/manual/rubber_recreation_fabrication_specs.csv`.

Toyota OE/EPC cross-reference: `data/manual/rubber_recreation_toyota_oe_cross_reference.csv`.

Aftermarket dimension cross-check: `data/manual/rubber_recreation_aftermarket_dimension_crosscheck.csv`.

Exact measurement closure table: `data/manual/rubber_recreation_measurement_closure.csv`.

Manufacturing requirements table: `data/manual/rubber_recreation_manufacturing_requirements.csv`.

## Release Position

This is the supporting fabricator handoff spec for quotation, first-article cutting, and sample preparation. For the current supplier order, `docs/longman-rubber-order-spec-20260508.md` is the primary order document.

The old-rubber photos and ruler measurements are accepted as the dimensional basis for quote and first articles. Do not treat the remaining gates as missing rubber dimensions: they are station mapping, dry-stack, caliper, and final install checks before full production or final trimming.

Toyota-style catalog data has been checked and added as a control reference. It confirms OE part numbers, station codes, left/right required quantities, bolt families, and several shim/spacer thicknesses. It does not publish rubber cushion OD, ID, free height, durometer, or cup geometry, so the rubber fabrication dimensions remain image-derived and must be closed from the physical samples.

All dimensions are in `mm`.

## Fabrication Drawing Package

Ready-to-run Rev A drawing package: `data/manual/fabrication/rubber_recreation_rev_a/`.

Send these files to the rubber/steel fabricator:

1. `j40_rubber_recreation_rev_a_dimension_sheet.pdf` - human-readable drawing pack.
2. `machine_definitions.csv` and `machine_definitions.json` - CNC/shop geometry, coordinate systems, tolerances, and non-CNC purchase controls.
3. `fabricator_cut_list.csv` - part, quantity, material, file, and release-status list.
4. `inspection_checklist.csv` - receiving and first-article inspection checks.
5. All `*.dxf` files in the package - CAD/CAM cut geometry.
6. Matching `*.svg` files - visual reference copies.
7. `models_3d/*.scad` - parametric 3D models for current square-pad quote geometry and hold-only bump-stop/exhaust reference shapes.

Note: the May 8 Longman order supersedes the earlier circular body-pad placeholder for the main body isolators. The active quote basis is square `BM-ISO-SM` and `BM-ISO-LG` pads. Use `models_3d/bm_iso_sm_square_pad.scad` and `bm_iso_lg_square_pad.scad` for the current 3D envelopes. They default to the production `18.0 mm` bore for the Toyota `90560-12009` style body-mount sleeve.

Package contents:

| Part | DXF | Release Use |
| --- | --- | --- |
| `BM-ISO-SM` small square body pad | `models_3d/bm_iso_sm_square_pad.scad` | Active Longman quote/first article: `70 x 70 x 22`, `18.0` bore |
| `BM-ISO-LG` large square body pad | `models_3d/bm_iso_lg_square_pad.scad` | Active Longman quote/first article: `80 x 80 x 24`, `18.0` bore |
| `BM-SM` small circular cushion | `bm_sm_body_mount_cushion_rev_a.dxf` | Legacy reference only; superseded by square `BM-ISO-SM` unless circular profile is deliberately reopened |
| `BM-LG` large circular cushion | `bm_lg_body_mount_cushion_rev_a.dxf` | Legacy reference only; superseded by square `BM-ISO-LG` unless circular profile is deliberately reopened |
| `BM-CUP` small cup washer blank | `bm_cup_small_seat_washer_rev_a.dxf` | Quote/first article; confirm cup reuse and dish depth |
| `BM-CUP` large cup washer blank | `bm_cup_large_seat_washer_rev_a.dxf` | Quote/first article; confirm cup reuse and dish depth |
| `FS-OVAL` front-support pad | `fs_oval_front_support_pad_rev_a.dxf` | Quote/first article; confirm holes, thickness, and insert/boss |
| `FS-STRIP-L` strip blank | `fs_strip_left_template_blank_rev_a.dxf` | Released plain first-article strip: `420 x 38 x 8`; local end trim only after dry-fit |
| `FS-STRIP-R` strip blank | `fs_strip_right_template_blank_rev_a.dxf` | Released plain first-article strip: `420 x 38 x 8`; local end trim only after dry-fit |
| `EXH-HGR-90917` exhaust teardrop cushion | `exh_hgr_90917_08004_teardrop_rev_a.dxf` | Toyota `90917-08004` / `17572-92000` is a reference shape only; source exact new stock or locally mould from a genuine sample/intact original with side profile, insert depth, thickness, and reinforcement confirmed |
| `BUMP-F-L`, `BUMP-F-R`, `BUMP-R` bump stops | `bump_stop_vehicle_measurement_control.svg` | May 29 removed-sample mould release. Long `48304-60010` positions remain externally controlled at `70 mm`; right-front `48304-60020` remains `60 mm` unless vehicle testing says otherwise. Reproduce the sample-style molded rubber body with two through-holes in the rubber, central fixture/channel interface, broad rounded/tapered sides, and flat strike area. Rubber body outline, through-hole pattern, fixture/channel detail, and contact offset come from the May 29 samples, removed metal fixture, and vehicle. See `docs/bump-stop-fabrication-spec-20260504.md`. |

Common handoff index: `docs/fabrication-handoff-index.md`.

## Manufacturing Release Requirements

Use this section as the fabrication purchase-order language. The dimension tables below still control the nominal geometry, but production acceptance also requires the material, process, inspection, packaging, and rejection controls in this section and in `data/manual/rubber_recreation_manufacturing_requirements.csv`.

### Fabricator Deliverables

Before full production, the fabricator must provide:

1. A written quote listing each part ID, quantity, material, hardness, process route, and whether the part is cut, moulded, bonded, or formed.
2. A first-article set: one `BM-ISO-SM`, one `BM-ISO-LG`, one `FS-OVAL`, and one left/right strip trial.
3. A material declaration or supplier datasheet for the rubber compound, including base polymer family and Shore A hardness.
4. A one-page inspection report with part ID, quantity, key dimensions, durometer readings, visual result, date, and fabricator contact.
5. Labeled bags for every part family and side/station where applicable.
6. Return of all old samples, templates, and metal carriers after fabrication.

Do not approve the final batch until the first articles pass dimensional check, durometer check, bench dry-stack, and vehicle/carrier trial fit.

### Material Controls

Rubber pieces must be new black solid automotive mount-grade rubber. The acceptable base compound is `EPDM` or `NR/SBR` unless a measured original sample proves a different compound. Do not use tyre rubber, crumb/recycled rubber, sponge foam, mixed offcuts, used rubber, old salvage rubber, or unidentified compound.

Bump stops are the exception to the body/front-support hardness target. Use the separate bump-stop material control: `NR/SBR` automotive bump-stop rubber Shore A `70 +/-5`, or cast automotive PU Shore A `80 +/-5` only if the May 29 sample-style through-hole layout, central fixture/channel interface, progressive mould shape, and rebound recovery are held. The old bump-stop rubber is construction evidence, not a final dimension master; caliper the samples and removed fixture before mould release.

Required material targets:

| Property | Acceptance Requirement | Verification |
| --- | --- | --- |
| Hardness | Shore A `60 +/-5`; preferred matched family target `58-62` | Durometer check using ASTM `D2240` as the reference method |
| Compression set | Target `<=25%`; reject `>30%` after `22 h` at `70 C` and `25%` deflection | ASTM `D395` Method B certificate or same-compound supplier data |
| Tensile strength | Minimum `8 MPa` | ASTM `D412` certificate or rubber stock datasheet |
| Elongation at break | Minimum `250%` | ASTM `D412` certificate or rubber stock datasheet |
| Heat aging | No cracking/tackiness; hardness change within `+/-10` Shore A points after `70 h` at `70 C`; retain at least `70%` tensile/elongation where data is available | ASTM `D573` certificate, supplier data, or same-compound heated sample check |
| Ozone/weather resistance | Exterior automotive/mount-grade compound with antiozonant package; no visible cracking on supplier's stretched-sample data where available | ASTM `D1149` certificate where available or written compound declaration |

If the fabricator cannot perform the laboratory tests, require a compound supplier datasheet or written declaration. A local shop saying the rubber is "hard" or "good quality" is not enough for final release.

### Process Controls

- Keep each matched family from one compound batch and one cure/cutting setup: `BM-ISO-SM` set, `BM-ISO-LG` pair, `FS-OVAL` pair, and `FS-STRIP-L/R` pair.
- Measure finished rubber after curing, trimming, drilling/punching, and at least `24 h` relaxation at room temperature.
- Square body pads and flat strip liners must have flat, parallel faces; face parallelism must be `<=0.5`, and body-pad bore position must be within `+/-0.5`.
- Functional holes and slots must be punched, bored, or waterjet cut. Do not burn, tear, or rough hand-knife the holes.
- External load edges must be smooth. Circular cushion outer edges stay `R2-R3`; `FS-OVAL` relief corners stay `R3`; seating-face flash must be `<=0.5`.
- Steel sleeves, cups, shims, and inserts must be deburred and corrosion protected after cutting/forming.
- Sleeve final length is held until the rubber/cup stack is released. Cut sleeves to the released free stack height minus `3-4` target compression unless dry-fit proves another value.
- Cup/seat washers must be real formed seats, not thin generic flat washers.

### Bonded Parts

If either strip rubber or the `FS-OVAL` insert is bonded to metal:

1. Remove old rubber, rust, paint, oil, and loose adhesive from the carrier.
2. Blast or sand to clean metal, then degrease before primer.
3. Use a rubber-to-metal bonding system such as Chemlok `205/220` or local equivalent, applied per adhesive maker instructions.
4. Clamp the part flat through cure.
5. Reject visible edge lift, bubbles, loose corners, or glue-over repairs.

ASTM `D429` is the reference method if the fabricator or compound supplier can provide rubber-to-metal adhesion data. For this small local batch, a clean process record plus edge-lift inspection is acceptable if no lab coupon is available.

### Inspection And Rejection

Inspect every part visually and record critical dimensions. For this small batch, `100%` visual inspection is practical and required.

Reject any piece with:

- Cracks, cuts, tearing, delamination, or tacky/undercured surface.
- Voids larger than `1 mm` on a load face.
- Oily bleed, strong uncured smell, embedded metal/debris, or visible crumb/filler lumps.
- Rough functional holes, off-centre holes, or torn hole edges.
- Mixed hardness across a matched family.
- Wrong material, wrong side/hand, wrong thickness, or unapproved substitution.

The fabricator may not substitute material, hardness, pad construction, sleeve length, hole pattern, or bonding method without written approval before manufacture.

## Toyota OE / EPC Controls

Sources checked:
- [Toyota GR Heritage Parts - Land Cruiser 40](https://toyotagazooracing.com/gr/heritage/landcruiser40/) and its official parts list. This confirms the current official heritage-parts programme for Land Cruiser 40, but no body-mount rubber dimensions were found there.
- [1978 Toyota Land Cruiser Cab Mounting & Body Mounting listing](https://www.toyotapartsdeal.com/parts-list/1978-toyota-land_cruiser/body/cab_mounting_body_mounting.html). This is an OEM dealer/EPC-style listing, not a factory drawing.
- [Energy Suspension / EnergySuspensionParts `8.18105` reference page](https://www.energysuspensionparts.com/8.18105), which lists the `8.4104` body-mount set component thicknesses and counts. This is an aftermarket polyurethane reference, not Toyota rubber.
- Local downloaded historical scan: `docs/_tmp/toyota_oe/ToyotaLandCruiserFJ40-PartsCatalog-Nov1967-opt.pdf`. The scan has no usable text layer, so it is retained only as a historical reference unless manually reviewed page by page.
- ASTM reference pages checked for manufacturing controls: [`D2000`](https://store.astm.org/standards/d2000), [`D2240`](https://store.astm.org/standards/d2240), [`D395`](https://store.astm.org/standards/d395), [`D412`](https://store.astm.org/standards/d412), [`D573`](https://store.astm.org/Standards/d573.htm), [`D1149`](https://store.astm.org/standards/d1149), [`D3767`](https://store.astm.org/standards/d3767.htm), and [`D429`](https://store.astm.org/Standards/D429.htm).

Usable OE controls:

| Control Area | Toyota Data Found | Fabrication Impact |
| --- | --- | --- |
| Cushion station IDs | `NO.1` to `NO.5`, upper/lower rows, with left/right quantities | Do not release production until every old cushion is mapped to a Toyota station and vehicle side. |
| Cushion part numbers | `90540-16043`, `52204-35010`, `52202-30010`, `52022-60010`, `90540-17045`, `52023-60010`, `52209-60010` | Use these to label bags and verify which physical samples belong to which station. |
| Rubber dimensions | No OE OD/ID/free-height dimensions found in open official/OEM listing sources | Use the measured old-rubber/photo dimensions as the quote and first-article basis for `BM-ISO-SM`, `BM-ISO-LG`, `FS-OVAL`, and `FS-STRIP`; station fit and final caliper checks close before final install/production. |
| Body-mount bolts | `90105-10053` for `NO.1` to `NO.3`; `90101-10463` for `NO.4` to `NO.5` | Confirms bolt families, but final length and pitch still need direct vehicle confirmation. |
| Cushion spacers | `90560-12232`, `90560-12231`, `90560-12233`, `90560-12234` | Reuse/measure original spacers before reproducing because listing does not publish dimensions. |
| Shim/spacer thicknesses | `52212-90310 T=10`, `52216-90310 T=5.0`, `52217-90310 T=15`, `52033-90301 T=22.8`, `52033-90304 T=27.8` | Use these as legitimate Toyota thickness references. Do not improvise with washer stacks. |

## Aftermarket Dimension Cross-Check

Energy Suspension `8.4104` data is useful because it publishes exact thicknesses for a known FJ40 body-mount set. It is not an OEM Toyota rubber specification, and its SAE hardware should not replace the Toyota metric hardware plan without direct thread confirmation.

| Reference Component | Published Thickness | Metric | Count | Use |
| --- | ---: | ---: | ---: | --- |
| `4144` tall bushing | `0.950 in` | `24.13 mm` | `2` | Supports `BM-ISO-LG` height target of `24 mm`. |
| `4145` medium bushing | `0.450 in` | `11.43 mm` | `10` | Cross-check for small/medium stations if old pieces separate into spacer bushings. |
| `4146` bushing seat | `0.340 in` | `8.64 mm` | `12` | Cross-check for separate seat/bushing construction. |
| `4143` short bushing | `0.237 in` | `6.02 mm` | `2` | Conditional: identify only if matching short-position rubbers exist on this vehicle. |
| `4147` body mount bushing | `0.240 in` | `6.10 mm` | `2` | Conditional: identify only if matching physical samples/positions exist. |

Impact on this spec:
- `BM-ISO-LG` is released for quote/first article at `24 mm` height, because the photo-derived target and the published `4144` thickness agree.
- `BM-ISO-SM` is released for quote/first article as a square `22 mm` pad. The Energy split-stack reference remains useful only as a dry-stack/compression check before final install.
- Any short/extra mount pieces must be added only after they are found in the actual removed samples or on the vehicle. Do not add Energy kit pieces just because they appear in an aftermarket kit.

Reconciliation risk:
- The Toyota OE/EPC listing uses `NO.1` to `NO.5` station groups with left/right quantities. The current working fabrication set is based on the photographed physical pieces and the early `2 large + 10 small` rubber-family count.
- Treat this as a station-mapping hold, not as permission to change the fabrication count blindly. During dry-fit, label the chassis/body positions `FL`, `FR`, `ML`, `MR`, `RL`, `RR`, then map each physical rubber/cup/sleeve stack to the Toyota `NO.1` to `NO.5` rows that actually apply to this vehicle.
- If a Toyota station row is present on the vehicle but not represented in the May 2 photos, that missing rubber or spacer becomes a separate procurement/fabrication item before primer and body refit.

## Exact Spec Closure Rule

The current fabricator release spec exists in `docs/longman-rubber-order-spec-20260508.md`, `data/manual/longman_rubber_order_specs.csv`, and `data/manual/rubber_recreation_fabrication_specs.csv`. Use `data/manual/rubber_recreation_measurement_closure.csv` as the closure sheet for station-fit and final-production checks.

Release order:
1. Sort the old rubbers by vehicle station and side.
2. Split each stack into rubber, seat/cup, sleeve, shim, washer, and bolt.
3. Measure each feature with calipers, recording three readings for diameters and four readings for heights.
4. Dry-stack the square body pad, sleeve, cup/washer, shim, and bolt so the sleeve controls clamp load.
5. Update the closure table if dry-fit proves a station trim or a different final-production correction.
6. Approve full production only after first articles pass dimension, material, and vehicle-fit checks.

Longman can quote and make first articles from the measured old-rubber dimensions. Full production/final install still depends on sleeve length, station placement, cup/washer support, and compression checks.

## Evidence Map

| Ref | Photo | Use |
| --- | --- | --- |
| `RRB-20260502-001` | <img src="../photos/20260502_004201_gp_zfUSmKJg.jpg" width="180"> | Long strip/bracket rubber overview with vertical tape. |
| `RRB-20260502-002` | <img src="../photos/20260502_004215_gp_evgCLjSw.jpg" width="180"> | Long strip/bracket rubber length reference. |
| `RRB-20260502-003` | <img src="../photos/20260502_004222_gp_PKRe5HSQ.jpg" width="180"> | Long strip/bracket profile reference. |
| `RRB-20260502-004` | <img src="../photos/20260502_004231_gp_CfosvPIg.jpg" width="180"> | Best tape-scale reference for old body cushions/cups and oval pad. |
| `RRB-20260502-005` | <img src="../photos/20260502_004254_gp_Hm9RR5DQ.jpg" width="180"> | Long strip/bracket height reference. |
| `RRB-20260502-006` | <img src="../photos/20260502_004314_gp_wuzpgNrA.jpg" width="180"> | Strip/bracket side thickness reference. |
| `RRB-20260502-007` | <img src="../photos/20260502_004337_gp_m2OagYpg.jpg" width="180"> | Circular cushion edge/thickness reference. |
| `RRB-20260502-008` | <img src="../photos/20260502_004345_gp_yK8VYzMQ.jpg" width="180"> | Best top-face view of the two-hole oval pad. |
| `RRB-20260502-009` | <img src="../photos/20260502_004401_gp_otUSjgGA.jpg" width="180"> | Strip/bracket close side profile. |
| `RRB-20260502-010` | <img src="../photos/20260502_004413_gp_Qno8OVRg.jpg" width="180"> | Circular cushion top profile. |
| `RRB-20260502-011` | <img src="../photos/20260502_004419_gp_ZPXJRBzg.jpg" width="180"> | Circular cushion top profile. |
| `RRB-20260502-012` | <img src="../photos/20260502_004429_gp_KJHxGcCA.jpg" width="180"> | Circular cushion side profile. |
| `RRB-20260502-013` | <img src="../photos/20260502_004437_gp_f1TySzww.jpg" width="180"> | Cleaner old cushion/cup top reference. |
| `RRB-20260502-014` | <img src="../photos/20260502_004442_gp_7WcFHjLQ.jpg" width="180"> | Cleaner old cushion/cup top reference. |

## Material Standard

- Rubber: black EPDM or NR/SBR automotive mount rubber.
- Hardness: `Shore A 60 +/-5`.
- Finish: smooth cut/moulded faces, no torn knife edges, no exposed cord unless a fabric-reinforced part is intentionally reproduced.
- Do not use tyre rubber, crumb/recycled rubber, mixed offcuts, or random durometer material.
- Keep each family from one batch so hardness, thickness, and compression behaviour match side-to-side.
- If a rubber is bonded to a metal carrier, blast/clean the carrier and use a rubber-to-metal bonding system, for example Chemlok 205/220 or local equivalent.

## Fabrication Parts

| Part ID | Part | Qty | Nominal Dimensions | Status |
| --- | --- | ---: | --- | --- |
| `BM-ISO-SM` | Small station square body isolator pad | `10` | `70 L x 70 W x 22 H`, square flat pad, `18.0` centre bore for Toyota `90560-12009` style sleeve, plan corners `R1.5`, edge break/chamfer `1.0` max | Released for quote / first article |
| `BM-ISO-LG` | Large station square body isolator pad | `2` | `80 L x 80 W x 24 H`, square flat pad, `18.0` centre bore for Toyota `90560-12009` style sleeve, plan corners `R1.5`, edge break/chamfer `1.0` max | Released for quote / first article |
| `BM-SLV` | Main body-mount crush sleeve | `6` | `ID 10.8-11.0` for M10 bolt; OD and length held for caliper confirmation | Hold |
| `BM-CUP` | Body-mount cup/seat washer | `12` | small cup `OD 64`, large cup `OD 78`, M10 clearance hole `11`, dish/register depth `2-3`, steel `2.5-3.0` thick | Separate hardware inspect / quote if needed |
| `FS-OVAL` | Two-hole oval front-support isolator pad | `2` | length `96`, width `64`, thickness `15`, holes `12`, hole spacing `64`, relief `36 x 18 R3` if functional, insert/boss `OD 29` | Released for quote / first article |
| `FS-STRIP-L` | Underfloor body-support strip liner - left | `1` | flat strip `420 x 38 x 8`; no through-holes in rubber by default | First article / quote |
| `FS-STRIP-R` | Underfloor body-support strip liner - right | `1` | same blank as left unless installed sample proves handed end trim | First article / quote |

## Main Body Isolator Pads

Relevant images: `RRB-004`, `RRB-010`, `RRB-011`, `RRB-013`, `RRB-014`.

Fabricate two square flat body-pad families for the current Longman order:

| Dimension | `BM-ISO-SM` | `BM-ISO-LG` |
| --- | ---: | ---: |
| Quantity | `10` | `2` |
| Plan size | `70 x 70` | `80 x 80` |
| Free height | `22` | `24` |
| Through bore | `18.0` | `18.0` |
| Plan corner radius | `R1.5` | `R1.5` |
| Top/bottom edge break or chamfer | `1.0` max | `1.0` max |

Fabrication notes:
- Make the faces flat and parallel.
- Keep the bore centred within `+/-0.5`.
- The `18.0` bore is for the Toyota `90560-12009` style body-mount sleeve. The M10 bolt must pass through the steel sleeve, not clamp directly through raw rubber.
- The sleeve controls crush. Do not clamp the body mount by crushing raw rubber around the bolt.
- Station photos/dry-fit may release local corner trim, but the first article starts as a square pad.
- Tolerance: length/width `+/-1.0`; height `+/-0.5`; bore `+0.5/-0.0`; bore position `+/-0.5`.

## Sleeve And Cup Washer Interface

Relevant images: `RRB-004`, `RRB-012`, `RRB-013`, `RRB-014`.

Sleeves:
- Quantity: `6`.
- Bolt: M10 body-mount hardware, working basis `M10 x 1.25`.
- Sleeve ID: `10.8-11.0`.
- Sleeve OD: genuine Toyota `90560-12009` style spacer basis, or copy old/OE spacer if locally made.
- Sleeve length: set from the completed stack; target is free rubber stack height minus `3-4` of intended rubber compression.
- Material: steel tube, deburred, zinc plated or painted after cutting.

Cup/seat washers:
- Quantity: `12`.
- Steel thickness: `2.5-3.0`.
- Clearance hole: `11` for M10.
- Small station support footprint: must support the `70 x 70` square pad without rocking or cutting into the edge.
- Large station support footprint: must support the `80 x 80` square pad without rocking or cutting into the edge.
- Register/dish depth: `2-3`.
- Reuse original cups only if flat, not thinned, and not cracked. Otherwise press/form new cups.

## Two-Hole Oval Front-Support Pad

Relevant images: `RRB-004`, `RRB-008`.

Part ID: `FS-OVAL`.

Quantity: `2`.

Nominal geometry:
- Overall length: `96`.
- Maximum width: `64`.
- Free thickness: `15`.
- Top hole: `12`.
- Lower hole: `12`.
- Hole centre spacing: `64`.
- Rectangular relief: `36 x 18`, corner radius `R3`.
- Top insert/boss OD: `29`.

Fabrication notes:
- Make both pieces as a matched pair.
- Punch or machine the holes. Do not hand-knife the holes.
- If the old pad uses a steel insert or washer bonded into the rubber, reproduce that insert or clean/reuse the original insert.
- The rectangular relief must have clean edges so it does not tear from a rough cut.
- Tolerance: outside `+/-1.0`, hole location `+/-0.5`, thickness `+/-0.5`.

Hold before production:
- Confirm the two hole centres with calipers.
- Confirm whether the upper metal insert is bonded, loose, or part of the old washer stack.

## Flat Underfloor Body-Support Strip Pair

Relevant images: `20260517_194143_gp_CO7MuMdA`, `20260517_194633_gp_rAjY3gjg`, `20260517_194706_gp_twKRWGFA`, `20260517_193503_gp_N9nHjqXw`, `20260517_193539_gp_E0cR9I0A`, `20260517_193559_gp_NEpk1hpg`, `20260517_193612_gp_JmbfR0Tw`, `20260517_193616_gp_1ye19BZA`.

Part IDs: `FS-STRIP-L`, `FS-STRIP-R`.

Legacy note: the `FS-STRIP-*` IDs are retained for project continuity, but the May 17 installed-location photos show these are actual underfloor body-support / anti-squeak strip liners on the tub-side crossmember landing, not unproven front-apron pieces and not bump-stop fragments.

Quantity: `1` left, `1` right.

Released rubber geometry:
- Free length: `165`.
- Finished width: `38`.
- Free thickness: `8`.
- Edge break: `0.5-1.0` or light `R1-R2`.
- Holes in rubber: none by default.

Material and finish:
- Solid black `EPDM` or `NR/SBR` automotive mount-grade rubber.
- Hardness: `Shore A 60 +/-5`.
- Flat parallel faces; smooth cut edges; no torn knife finish, foam, sponge, tyre rubber, or crumb/recycled stock.

Release position:
- This is now strong enough for quotation and first-article manufacture.
- Make the rubber as a plain flat strip pair. Do not force the slotted metal retainer geometry into the rubber unless a direct install trial proves the original strip itself was pierced.

Steel retainer / carrier rule:
1. Reuse the original slotted steel retainers if they clean up and still clamp flat.
2. If a retainer must be remade, trace it directly from the original steel piece.
3. Do not derive steel slot length or pitch from torn rubber witness marks alone.

Fabrication method:
1. Cut two flat rubber strips to `420 x 38 x 8`.
2. Dress the long edges clean and keep the faces parallel.
3. Dry-fit one strip at the actual crossmember/body landing before making any side-specific trim.
4. If one side proves a local corner relief or handed end trim is needed, trim from the installed sample and duplicate that side only after confirmation.

First-article check before full batch:
- Strip sits flat between the tub underside landing and the support bracket with no overhang onto weld lips or thin rust edges.
- Clamp pressure is even and the strip does not buckle.
- The reused or remade steel retainer covers the same load path as the original piece.

## Tools Needed At Fabricator

- Vernier/digital calipers reading to `0.1 mm`.
- Steel rule and square.
- Radius gauge or round templates for edge radii.
- Hole punches: `11`, `12`, and `32`.
- Drill press or punch press for steel cups/inserts.
- Waterjet, punch, die cutter, mill, or clean band-knife setup for square/flat rubber.
- Clamps and flat plates for bonded strip parts.
- Durometer tester, Shore A.

## Supplies Needed

- EPDM or NR/SBR rubber stock, `Shore A 60 +/-5`.
- Rubber sheet `8`, `14`, `15`, `22`, and `24` as needed, or mould stock.
- Steel tube for sleeves, M10 clearance ID.
- Steel washer/cup blanks `2.5-3.0` thick.
- Rubber-to-metal bonding adhesive if carriers are reused.
- Zinc primer/paint or plating for steel sleeves/cups.
- Labels and bags for keeping left/right and station samples separate.

## Quality Gate

Before accepting the batch:
- Confirm the fabricator supplied the material declaration and inspection report.
- Confirm every bag is labeled by part ID, quantity, batch/date, and side/station where applicable.
- Confirm the first-article set passed before full production was released.
- Check every length, width, thickness, bore, hole, and height against the table.
- Check hardness on at least one piece from each rubber family.
- Test each sleeve through the rubber and cup with an M10 bolt.
- Confirm the sleeve prevents over-crush before final body fastening.
- Dry-fit the tub/front support without forcing alignment.
- Reject any piece with cracks, trapped debris, exposed crumb, rough holes, or mixed hardness.

## Production Holds

| Hold | Why | Must Be Confirmed With |
| --- | --- | --- |
| `BM-SLV` sleeve OD and length | Controls compression and final body height | Calipers on old sleeve or complete stack dry-fit |
| `BM-ISO-SM/BM-ISO-LG` station footprint | Square pad must sit on flat bearing area without rocking, edge overhang, or contact with weld/rust lips | Station photo and dry-fit |
| `BM-ISO-SM/BM-ISO-LG` sleeve/cup/shim stack | Sleeve must control clamp load without over-crushing the pad | Bench dry-stack and vehicle dry-fit |
| `FS-OVAL` hole spacing and insert OD | Off-plane top photo and corroded insert make image-only reading risky | Calipers on physical pad/insert |
| `FS-STRIP-L/R` local handed trim and steel retainer remake | Rubber size is now released, but any side-specific end trim or replacement steel retainer still comes from the physical sample | Dry-fit on the actual landing and direct trace from the original steel if the retainer must be remade |
| Station count and large-pair location | Pre-1/79 pattern is the working basis, but the car may have prior repairs | Mount map during tub dry-fit |
| Toyota `NO.1` to `NO.5` OE station mapping | OE listing does not reduce cleanly to the current `BM-ISO-SM/BM-ISO-LG` family count | Label every body/chassis mount position and reconcile against `data/manual/rubber_recreation_toyota_oe_cross_reference.csv` |
| OE shim/spacer thickness | Some Toyota spacer rows publish thickness, but most cushion spacers do not | Use Toyota thickness rows where available; measure original spacers and shims before copying |
