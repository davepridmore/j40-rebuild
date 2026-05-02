# Rubber Recreation Fabrication Spec - 2026-05-02

Scope: custom recreation of the J40 body-mount/front-support rubber parts from the May 2 tape-measure photos.

Source image set: Google Photos import `20260502T013759`.

Data table: `data/manual/rubber_recreation_fabrication_specs.csv`.

Toyota OE/EPC cross-reference: `data/manual/rubber_recreation_toyota_oe_cross_reference.csv`.

Aftermarket dimension cross-check: `data/manual/rubber_recreation_aftermarket_dimension_crosscheck.csv`.

Exact measurement closure table: `data/manual/rubber_recreation_measurement_closure.csv`.

## Release Position

This is the fabricator handoff spec for quotation, prototype cutting, and sample preparation.

Because several samples are crushed, split, curled, or photographed off-plane, do not approve full production until the hold dimensions in this sheet are checked with calipers on the physical parts. The dimensions below are the image-derived nominal targets to the nearest millimetre.

Toyota-style catalog data has been checked and added as a control reference. It confirms OE part numbers, station codes, left/right required quantities, bolt families, and several shim/spacer thicknesses. It does not publish rubber cushion OD, ID, free height, durometer, or cup geometry, so the rubber fabrication dimensions remain image-derived and must be closed from the physical samples.

All dimensions are in `mm`.

## Toyota OE / EPC Controls

Sources checked:
- [Toyota GR Heritage Parts - Land Cruiser 40](https://toyotagazooracing.com/gr/heritage/landcruiser40/) and its official parts list. This confirms the current official heritage-parts programme for Land Cruiser 40, but no body-mount rubber dimensions were found there.
- [1978 Toyota Land Cruiser Cab Mounting & Body Mounting listing](https://www.toyotapartsdeal.com/parts-list/1978-toyota-land_cruiser/body/cab_mounting_body_mounting.html). This is an OEM dealer/EPC-style listing, not a factory drawing.
- [Energy Suspension / EnergySuspensionParts `8.18105` reference page](https://www.energysuspensionparts.com/8.18105), which lists the `8.4104` body-mount set component thicknesses and counts. This is an aftermarket polyurethane reference, not Toyota rubber.
- Local downloaded historical scan: `docs/_tmp/toyota_oe/ToyotaLandCruiserFJ40-PartsCatalog-Nov1967-opt.pdf`. The scan has no usable text layer, so it is retained only as a historical reference unless manually reviewed page by page.

Usable OE controls:

| Control Area | Toyota Data Found | Fabrication Impact |
| --- | --- | --- |
| Cushion station IDs | `NO.1` to `NO.5`, upper/lower rows, with left/right quantities | Do not release production until every old cushion is mapped to a Toyota station and vehicle side. |
| Cushion part numbers | `90540-16043`, `52204-35010`, `52202-30010`, `52022-60010`, `90540-17045`, `52023-60010`, `52209-60010` | Use these to label bags and verify which physical samples belong to which station. |
| Rubber dimensions | No OE OD/ID/free-height dimensions found in open official/OEM listing sources | Keep `BM-SM`, `BM-LG`, `FS-OVAL`, and `FS-STRIP` dimensions as image-derived until caliper confirmation. |
| Body-mount bolts | `90105-10053` for `NO.1` to `NO.3`; `90101-10463` for `NO.4` to `NO.5` | Confirms bolt families, but final length and pitch still need direct vehicle confirmation. |
| Cushion spacers | `90560-12232`, `90560-12231`, `90560-12233`, `90560-12234` | Reuse/measure original spacers before reproducing because listing does not publish dimensions. |
| Shim/spacer thicknesses | `52212-90310 T=10`, `52216-90310 T=5.0`, `52217-90310 T=15`, `52033-90301 T=22.8`, `52033-90304 T=27.8` | Use these as legitimate Toyota thickness references. Do not improvise with washer stacks. |

## Aftermarket Dimension Cross-Check

Energy Suspension `8.4104` data is useful because it publishes exact thicknesses for a known FJ40 body-mount set. It is not an OEM Toyota rubber specification, and its SAE hardware should not replace the Toyota metric hardware plan without direct thread confirmation.

| Reference Component | Published Thickness | Metric | Count | Use |
| --- | ---: | ---: | ---: | --- |
| `4144` tall bushing | `0.950 in` | `24.13 mm` | `2` | Supports `BM-LG` height target of `24 mm`. |
| `4145` medium bushing | `0.450 in` | `11.43 mm` | `10` | Cross-check for small/medium stations if old pieces separate into spacer bushings. |
| `4146` bushing seat | `0.340 in` | `8.64 mm` | `12` | Cross-check for separate seat/bushing construction. |
| `4143` short bushing | `0.237 in` | `6.02 mm` | `2` | Conditional: identify only if matching short-position rubbers exist on this vehicle. |
| `4147` body mount bushing | `0.240 in` | `6.10 mm` | `2` | Conditional: identify only if matching physical samples/positions exist. |

Impact on this spec:
- `BM-LG` is strong enough for quote/prototype at `24 mm` height, because the photo-derived target and the published `4144` thickness agree.
- `BM-SM` must not be blindly released as a one-piece `22 mm` part. The external reference suggests a common split stack of `11.43 + 8.64 = 20.07 mm`, so the physical old part must prove whether the custom piece is one moulded cushion or a separate seat plus spacer bushing.
- Any short/extra mount pieces must be added only after they are found in the actual removed samples or on the vehicle. Do not add Energy kit pieces just because they appear in an aftermarket kit.

Reconciliation risk:
- The Toyota OE/EPC listing uses `NO.1` to `NO.5` station groups with left/right quantities. The current working fabrication set is based on the photographed physical pieces and the early `2 large + 10 small` rubber-family count.
- Treat this as a station-mapping hold, not as permission to change the fabrication count blindly. During dry-fit, label the chassis/body positions `FL`, `FR`, `ML`, `MR`, `RL`, `RR`, then map each physical rubber/cup/sleeve stack to the Toyota `NO.1` to `NO.5` rows that actually apply to this vehicle.
- If a Toyota station row is present on the vehicle but not represented in the May 2 photos, that missing rubber or spacer becomes a separate procurement/fabrication item before primer and body refit.

## Exact Spec Closure Rule

We can produce the exact fabricator release spec, but the final release values must be written from direct measurement of the physical samples. Use `data/manual/rubber_recreation_measurement_closure.csv` as the closure sheet.

Release order:
1. Sort the old rubbers by vehicle station and side.
2. Split each stack into rubber, seat/cup, sleeve, shim, washer, and bolt.
3. Measure each feature with calipers, recording three readings for diameters and four readings for heights.
4. Decide whether `BM-SM` is a single one-piece cushion or a split seat-plus-spacer stack.
5. Update the `release_value_mm` column in the closure table.
6. Only then approve production quantity and final cut/mould dimensions.

No fabricator should be asked to make the final batch from photos alone. The photos are strong enough for quote and prototype, but not for final release of sleeve length, centre register fit, or split-stack construction.

## Evidence Map

| Ref | Photo | Use |
| --- | --- | --- |
| `RRB-20260502-001` | <img src="../photos/20260502_004201_gp_zfUSmKJg.jpg" width="180"> | Long strip/bracket rubber overview with vertical tape. |
| `RRB-20260502-002` | <img src="../photos/20260502_004215_gp_evgCLjSw.jpg" width="180"> | Long strip/bracket rubber length reference. |
| `RRB-20260502-003` | <img src="../photos/20260502_004222_gp_PKRe5HSQ.jpg" width="180"> | Long strip/bracket profile reference. |
| `RRB-20260502-004` | <img src="../photos/20260502_004231_gp_CfosvPIg.jpg" width="180"> | Best tape-scale reference for circular cushions/cups and oval pad. |
| `RRB-20260502-005` | <img src="../photos/20260502_004254_gp_Hm9RR5DQ.jpg" width="180"> | Long strip/bracket height reference. |
| `RRB-20260502-006` | <img src="../photos/20260502_004314_gp_wuzpgNrA.jpg" width="180"> | Strip/bracket side thickness reference. |
| `RRB-20260502-007` | <img src="../photos/20260502_004337_gp_m2OagYpg.jpg" width="180"> | Circular cushion edge/thickness reference. |
| `RRB-20260502-008` | <img src="../photos/20260502_004345_gp_yK8VYzMQ.jpg" width="180"> | Best top-face view of the two-hole oval pad. |
| `RRB-20260502-009` | <img src="../photos/20260502_004401_gp_otUSjgGA.jpg" width="180"> | Strip/bracket close side profile. |
| `RRB-20260502-010` | <img src="../photos/20260502_004413_gp_Qno8OVRg.jpg" width="180"> | Circular cushion top profile. |
| `RRB-20260502-011` | <img src="../photos/20260502_004419_gp_ZPXJRBzg.jpg" width="180"> | Circular cushion top profile. |
| `RRB-20260502-012` | <img src="../photos/20260502_004429_gp_KJHxGcCA.jpg" width="180"> | Circular cushion side profile. |
| `RRB-20260502-013` | <img src="../photos/20260502_004437_gp_f1TySzww.jpg" width="180"> | Cleaner circular annular cushion top reference. |
| `RRB-20260502-014` | <img src="../photos/20260502_004442_gp_7WcFHjLQ.jpg" width="180"> | Cleaner circular annular cushion top reference. |

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
| `BM-SM` | Small circular body-mount cushion / stack-equivalent | `10` | `OD 64`, photo stack height `22`, bore `32`, centre register `OD 46 x depth 2`, edge radius `R2-R3`; split-stack check required | Prototype/quote |
| `BM-LG` | Large circular body-mount cushion | `2` | `OD 78`, height `24`, bore `32`, centre register `OD 46 x depth 2`, edge radius `R2-R3` | Prototype/quote |
| `BM-SLV` | Main body-mount crush sleeve | `6` | `ID 10.8-11.0` for M10 bolt; OD and length held for caliper confirmation | Hold |
| `BM-CUP` | Body-mount cup/seat washer | `12` | small cup `OD 64`, large cup `OD 78`, M10 clearance hole `11`, dish/register depth `2-3`, steel `2.5-3.0` thick | Prototype/quote |
| `FS-OVAL` | Two-hole oval front-support isolator pad | `2` | length `96`, width `64`, thickness `15`, holes `12`, hole spacing `64`, relief `36 x 18 R3`, insert/boss `OD 29` | Prototype/quote |
| `FS-STRIP-L` | Long front-support/bracket strip rubber - left | `1` | trace length `165`, width `38-42`, base thickness `8`, raised/load pad `14`, hole/slot `11` or `11 x 16` where shown | Template required |
| `FS-STRIP-R` | Long front-support/bracket strip rubber - right | `1` | mirror `FS-STRIP-L` unless the physical sample proves asymmetry | Template required |

## Circular Body-Mount Cushions

Relevant images: `RRB-004`, `RRB-010`, `RRB-011`, `RRB-013`, `RRB-014`.

Fabricate two circular families:

| Dimension | `BM-SM` | `BM-LG` |
| --- | ---: | ---: |
| Quantity | `10` | `2` |
| Outside diameter | `64` | `78` |
| Free height / stack height | `22` photo stack-equivalent; verify one-piece vs split `11.43 + 8.64` construction | `24`; cross-check `24.13` |
| Central bore | `32` | `32` |
| Centre register / raised lip OD | `46` | `46` |
| Centre register depth | `2` | `2` |
| Outer edge radius | `R2-R3` | `R2-R3` |

Fabrication notes:
- Make the faces flat and parallel.
- Keep the bore concentric within `1 mm`.
- The central bore is a rubber/cup register, not the M10 bolt hole itself. The bolt must pass through a steel sleeve.
- The sleeve controls crush. Do not clamp the body mount by crushing raw rubber around the bolt.
- Before production, prove whether the small mount is one moulded cushion or a split seat plus spacer. If split, fabricate the two pieces separately rather than making a single `22 mm` block.
- Tolerance: OD/ID `+/-1.0`; height `+/-0.5`; concentricity `<=1.0`.

## Sleeve And Cup Washer Interface

Relevant images: `RRB-004`, `RRB-012`, `RRB-013`, `RRB-014`.

Sleeves:
- Quantity: `6`.
- Bolt: M10 body-mount hardware, working basis `M10 x 1.25`.
- Sleeve ID: `10.8-11.0`.
- Sleeve OD: match the final rubber bore/cup register after caliper confirmation.
- Sleeve length: set from the completed stack; target is free rubber stack height minus `3-4` of intended rubber compression.
- Material: steel tube, deburred, zinc plated or painted after cutting.

Cup/seat washers:
- Quantity: `12`.
- Steel thickness: `2.5-3.0`.
- Clearance hole: `11` for M10.
- Small station OD: `64`, or matched to `BM-SM`.
- Large station OD: `78`, or matched to `BM-LG`.
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

## Long Front-Support / Bracket Strip Rubbers

Relevant images: `RRB-001`, `RRB-002`, `RRB-003`, `RRB-005`, `RRB-006`, `RRB-009`.

Part IDs: `FS-STRIP-L`, `FS-STRIP-R`.

Quantity: `1` left, `1` right.

Nominal section:
- Overall trace length: `165`.
- Working strip width: `38-42`.
- Base sheet thickness: `8`.
- Raised/load pad height: `14`.
- Bolt holes: `11` for M10 clearance, or `11 x 16` slot where the old part shows an elongated hole.

Required fabrication method:
1. Keep the physical old strip and any metal carrier.
2. Clean the rubber enough to see edges, but do not sand or trim the sample before tracing.
3. Trace the actual old part and the metal carrier on card or acetate.
4. Mark hole centres from the metal carrier, not from torn rubber.
5. Cut the new rubber from sheet or mould it against the carrier.
6. Punch holes with a proper punch.
7. If bonded to metal, blast the carrier, prime/bond, clamp flat, and cure before trimming.

Hold before production:
- These two strip rubbers are not reliable as photo-only cut patterns because the old samples are curled, split, and torn.
- Use the dimensions above to prepare stock and quote the job, then cut final pieces from a physical template.

## Tools Needed At Fabricator

- Vernier/digital calipers reading to `0.1 mm`.
- Steel rule and square.
- Radius gauge or round templates for edge radii.
- Hole punches: `11`, `12`, and `32`.
- Drill press or punch press for steel cups/inserts.
- Lathe, boring tool, waterjet, die cutter, or clean band-knife setup for circular rubber.
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
- Check every OD, ID, and height against the table.
- Check hardness on at least one piece from each rubber family.
- Test each sleeve through the rubber and cup with an M10 bolt.
- Confirm the sleeve prevents over-crush before final body fastening.
- Dry-fit the tub/front support without forcing alignment.
- Reject any piece with cracks, trapped debris, exposed crumb, rough holes, or mixed hardness.

## Production Holds

| Hold | Why | Must Be Confirmed With |
| --- | --- | --- |
| `BM-SLV` sleeve OD and length | Controls compression and final body height | Calipers on old sleeve or complete stack dry-fit |
| `BM-SM/BM-LG` centre bore | Must match sleeve/cup register | Calipers on old bore and cup boss |
| `BM-SM` one-piece vs split-stack construction | External `8.4104` reference separates `4145` medium bushings from `4146` bushing seats | Disassemble/inspect old sample and measure pieces individually |
| `FS-OVAL` hole spacing and insert OD | Off-plane top photo and corroded insert make image-only reading risky | Calipers on physical pad/insert |
| `FS-STRIP-L/R` final outline and hole centres | Old strip is curled and torn | Physical template from sample and metal carrier |
| Station count and large-pair location | Pre-1/79 pattern is the working basis, but the car may have prior repairs | Mount map during tub dry-fit |
| Toyota `NO.1` to `NO.5` OE station mapping | OE listing does not reduce cleanly to the current photo-only `BM-SM/BM-LG` family count | Label every body/chassis mount position and reconcile against `data/manual/rubber_recreation_toyota_oe_cross_reference.csv` |
| OE shim/spacer thickness | Some Toyota spacer rows publish thickness, but most cushion spacers do not | Use Toyota thickness rows where available; measure original spacers and shims before copying |
