# Longman Rubber Order Spec - 2026-05-08

Purpose: send one consolidated rubber-only manufacturing request to Longman for the current J40 body/front-support/chassis rubber batch.

Supplier fit: Longman Mills lists custom rubber parts, automobile parts, rubber-to-metal bonded parts, hose pipes, and rubber testing capability, so this pack asks them to quote the rubber pieces and advise what samples or steel inserts they need before final production.

Longman site references:

- https://www.longman.com.pk/
- https://www.longman.com.pk/products/
- https://www.longman.com.pk/about-us/
- https://www.longman.com.pk/automobile-parts/

## Release Position - 2026-05-28

The old-rubber photos and ruler measurements are accepted as the dimensional basis for quote and first articles. The remaining open items are station fit and stack-release checks, not missing rubber dimensions.

May 17 loose-strip ruler photos show the underfloor strip length at about `16.5 in` (`419 mm`), so the `FS-STRIP-L/R` first-article length is corrected to `420 mm`. Width and thickness remain `38 W x 8 T mm`; any end trim, holes, slots, bonding, or retainer remake still requires dry-fit or a direct retainer trace.

Use this distinction:

- `Released for quote / first article`: Longman can quote and make the part from the dimensions in this spec.
- `Station fit pending`: before full production or final trimming, the mechanic must map the part to its vehicle position and confirm footprint, sleeve/cup/shim stack, and dry-fit compression.
- `Hold`: do not quote or fabricate until a real sample, installed position, or full-length trace is identified.

For this Longman order, `BM-ISO-SM`, `BM-ISO-LG`, `FS-OVAL`, `FS-STRIP-L`, and `FS-STRIP-R` are released for quote and first article. The two bump-stop families are released for first-article discussion on height and Toyota-style construction, but their base, bolt pattern, and strike-face offsets remain vehicle-measured before mould release. `BODY-LINER-FULL-WIDTH-HOLD` and `EXH-HGR-90917` remain hold-only.

## Vehicle Location And Kit Check

The current Toyota GR Heritage 40-series list checked on 2026-05-28 does not expose a complete body/chassis rubber kit for this area. Toyota EPC-style body-mount rows and aftermarket suppliers do show normal NO.1-NO.5 body-mount cushion/spacer/shim families and early/late 40-series kit splits, but no checked source replaces the need to map this vehicle's stations, sleeves, cups, shims, and dry-stack height. Therefore the active route remains the single Longman custom rubber bundle unless the project deliberately switches to a complete matched OE/reproduction package.

Checked sources:

- Toyota GR Heritage Land Cruiser 40 parts list: https://toyotagazooracing.com/-/media/TMC/tgr/global/contents/gr/heritage/pdf/2024/Landcruiser40_en.pdf
- Toyota EPC-style BJ40 cab/body mounting row: https://toyota-general.epc-data.com/land_cruiser/bj40/8406/body/5251/52254/
- Toyota 90560-12009 body-mount spacer listing: https://www.toyotapartsdeal.com/oem/toyota~spacer~for~body~mount~no~2~cushion~90560-12009.html
- Example late-40 aftermarket body mount kit split: https://shop.cruiserparts.net/index.php?main_page=product_info&products_id=1821

Vehicle location controls:

- `BM-ISO-SM`: main tub-to-chassis small stations, currently expected at middle/rear small stations and any small front/cowl station after layout.
- `BM-ISO-LG`: main tub-to-chassis larger front or primary load stations; final side/station confirmed during layout.
- `FS-OVAL`: separate front support / nose-extension isolator positions, left and right, not the main tub body-mount stack.
- `FS-STRIP-L/R`: left and right underfloor front-support/body-support strip landings beside the front support pickups.
- `BUMP-60010-LONG`: front-left plus rear-left and rear-right axle-to-chassis bump-stop stations.
- `BUMP-60020-SHORT`: right-front axle-to-chassis bump-stop station only.
- `BODY-LINER-FULL-WIDTH-HOLD`: unknown full-width body/panel liner path; hold until a real strip or installed path proves it.
- `EXH-HGR-90917`: exhaust tailpipe/rear support hanger reference; hold until sample or fitted support geometry proves it.

Location and complete drawing previews are included in the handoff:

- `data/manual/fabrication/rubber_recreation_rev_a/chassis_rubber_location_map_rev_a.svg`
- `data/manual/fabrication/rubber_recreation_rev_a/chassis_rubber_all_drawings_preview_rev_a.svg`

## Copy/Paste Request

Need quote and manufacturing advice for custom new rubber parts for an older Toyota Land Cruiser J40 restoration. The body-to-chassis pieces are simple flat isolator pads, not precision socket-matched bushings. For the custom order, use square flat pads as the preferred shape because there is no visible molded chassis/tub socket that needs a round outside profile. The important controls are installed height, sleeve/hole fit, rubber firmness, flat bearing area, and no overhang onto bends, seams, weld lips, or thin/rusted edges.

Please quote the required rubber parts below, plus optional spares where listed. The measured old-rubber dimensions are the quote and first-article basis. Rubber must be new black solid automotive mount-grade compound. No tyre rubber, crumb rubber, sponge/foam, EVA, recycled offcuts, used rubber, or unknown old stock.

For the body/front-support isolators, target hardness is Shore A 60 +/-5. For axle bump stops, target hardness is Shore A 70 +/-5 rubber with the same progressive Toyota-style shape as rubber-only stretch-fit bolt-on parts.

Steel body-mount washers/cups, sleeves, shims, bolts, and fasteners are not part of this Longman order. Existing body-mount washers will be inspected separately. Bump-stop holes or short slots are through the rubber body and should be relaxed undersize so the stop stretches over/around the fitted bolts or studs during installation.

## Required Quote Table

| ID | Part | Required Qty | Optional Spare Qty | Rubber definition | 3D envelope | Edge/profile control | Hole / insert status | Material |
| --- | --- | ---: | ---: | --- | --- | --- | --- | --- |
| `BM-ISO-SM` | Main body isolator pad, small stations | `10` | `2` | Square flat body isolator pad; flat parallel top and bottom bearing faces. | `70 L x 70 W x 22 H mm`; production `18.0 mm` bore on centre. | Plan corners `R1.5`; top/bottom perimeter edge break or chamfer `1.0 mm` max; no ragged cut edges. | Production `18.0 mm` through bore for Toyota `90560-12009` style body-mount spacer. | Solid EPDM or NR/SBR, Shore A `60 +/-5`. |
| `BM-ISO-LG` | Main body isolator pad, large stations | `2` | `1` | Square flat body isolator pad; flat parallel top and bottom bearing faces. | `80 L x 80 W x 24 H mm`; production `18.0 mm` bore on centre. | Plan corners `R1.5`; top/bottom perimeter edge break or chamfer `1.0 mm` max; no ragged cut edges. | Production `18.0 mm` through bore for Toyota `90560-12009` style body-mount spacer. | Same batch/type as `BM-ISO-SM` where possible. |
| `FS-OVAL` | Two-hole front-support isolator pad | `2` | `0` | Oval/capsule front-support isolator pad. | `96 L x 64 W x 15 T mm`; capsule ends `R32`; two `12 mm` holes at `64 mm` centres; optional `36 x 18 R3` relief only if sample confirms. | Outer perimeter edge break `0.5-1.0 mm`; clean punched hole edges; relief edges `R3` if relief is released. | Confirm whether old insert/boss is bonded, loose, or just washer imprint before production. | Solid EPDM or NR/SBR, Shore A `60 +/-5`. |
| `FS-STRIP-L` | Underfloor body-support strip liner, left | `1` | `0` | Plain flat underfloor body-support strip; no stepped section. | `420 L x 38 W x 8 T mm`. | Plan corners `R1.5`; top/bottom perimeter edge break `0.5-1.0 mm`; smooth cut edges; flat parallel faces. | No through-holes in rubber by default. Reuse or trace the slotted steel retainer separately if needed. | Solid EPDM or NR/SBR strip, Shore A `60 +/-5`. |
| `FS-STRIP-R` | Underfloor body-support strip liner, right | `1` | `0` | Plain flat underfloor body-support strip; same blank as left unless dry-fit proves handed trim. | `420 L x 38 W x 8 T mm`. | Plan corners `R1.5`; top/bottom perimeter edge break `0.5-1.0 mm`; smooth cut edges; flat parallel faces. | Same retainer rule as left; do not invent slot geometry in the rubber. | Same batch/type as left strip. |
| `BUMP-60010-LONG` | Long axle-to-chassis bump stop: front-left and both rear | `3` | `0` | Rubber-only Toyota-style progressive stop with stretch-fit bolt-on holes or slots and flat rectangular strike face. | `70 H mm` released; rubber base `L x W`, bolt/stud pitch, relaxed hole/slot size, and strike-face `X/Y` are vehicle-measured before mould release. | Tapered/radiused rubber body; no sharp rectangular block edges; no metal saddle/backing plate. | Rubber hole/slot pitch, relaxed hole/slot size, base footprint, and strike-face offset come from vehicle measurements; rubber stretches over/around the fitted bolts or studs. | NR/SBR bump-stop rubber Shore A `70 +/-5`. |
| `BUMP-60020-SHORT` | Short right-front axle-to-chassis bump stop | `1` | `0` | Rubber-only Toyota-style progressive stop with stretch-fit bolt-on holes or slots and flat rectangular strike face. | `60 H mm` released; rubber base `L x W`, bolt/stud pitch, relaxed hole/slot size, and strike-face `X/Y` are vehicle-measured before mould release. | Tapered/radiused rubber body; no sharp rectangular block edges; no metal saddle/backing plate. | Same rubber base/contact rules as long stop; rubber stretches over/around the fitted bolts or studs. | Same compound family as long stops. |
| `BODY-LINER-FULL-WIDTH-HOLD` | Long/full-width flat body or panel liner strips | Hold | Hold | Not yet captured as orderable pieces. Quote only after the actual strips are found or the body/chassis station proves a continuous flat anti-squeak liner is required. | Hold: needs measured `L x W x T` and any holes/slots from actual piece or installed path. | Hold: edge radius/chamfer, end trim, and slot edges must come from actual trace. | Needs full-length trace, holes/slots, side/orientation labels, and installed location photos. | EPDM or NR/SBR flat strip, hardness by function after location is confirmed. |
| `EXH-HGR-90917` | Exhaust teardrop hanger cushion | Hold | Hold | Optional later teardrop rubber-metal exhaust cushion only if sample or installed geometry releases final shape. | Hold target `48 W x 86 H x 22 T mm`; top hole `9 mm`; lower hanger slot `16 x 22 mm` unless sample proves otherwise. | Radiused teardrop perimeter; clean radiused hole/slot edges; reinforcement/insert detail sample-controlled. | Needs old/genuine sample, installed support-point measurements, or a proper tracing before quoting production. | Heat/vibration-resistant exhaust-hanger rubber, Shore A `60 +/-5`. |

## Release Status Summary

| ID | Dimensional status | What can happen now | What must close before final production/install |
| --- | --- | --- | --- |
| `BM-ISO-SM` | Released from measured sample/photo basis and current square-pad envelope. | Quote and make one first article or the quoted batch with first-article signoff. | Confirm station count, landing footprint, sleeve/cup/shim stack, and dry-fit compression. |
| `BM-ISO-LG` | Released from measured sample/photo basis and current square-pad envelope. | Quote and make one first article or the quoted pair/spare with first-article signoff. | Confirm which station uses the large pair, landing footprint, sleeve/cup/shim stack, and dry-fit compression. |
| `FS-OVAL` | Released for quote/first article from the measured old front-support pad dimensions. | Quote and make one first article. | Caliper-check physical sample for hole centres, thickness, insert/boss, and whether the relief is real before making final pair. |
| `FS-STRIP-L/R` | Released for first article from May 17 measured old strips and installed-location photos. | Quote and make plain `420 x 38 x 8 mm` first articles. | Dry-fit on actual landings; apply only proven end trim; trace/reuse steel retainers separately. |
| `BUMP-60010-LONG` | Height and Toyota-style construction released; base/holes/contact are not released. | Quote/advice and one `70 mm` first article after vehicle bracket measurements. | Measure BL/BW/P/D/X-Y/G/F on vehicle and pass compression/fit tests. |
| `BUMP-60020-SHORT` | Height and Toyota-style construction released; base/holes/contact are not released. | Quote/advice and one `60 mm` first article after vehicle bracket measurements. | Measure right-front BL/BW/P/D/X-Y/G/F and pass compression/fit tests. |
| `BODY-LINER-FULL-WIDTH-HOLD` | Not released. | No supplier action. | Find the actual long/full-width strip or prove the installed path and dimensions. |
| `EXH-HGR-90917` | Reference shape only. | No Longman production unless a sample or installed support geometry is available. | Sample/trace thickness, insert/reinforcement, pin/slot geometry, and exhaust support alignment. |

## Body Isolator Rules

The body pads are not shape-matched to a molded chassis socket. The important controls are:

- Free height and installed compression.
- Matching hardness across the set.
- Central `18.0 mm` bore for Toyota `90560-12009` style body-mount spacer.
- Explicit 3D envelope (`L x W x H/T`) and edge profile for every released rubber line.
- Enough footprint to cover the tub/chassis landing faces.
- No overhang onto bends, seams, weld lips, captive nut repairs, or rust-thinned edges.
- Bolt clamps through the steel sleeve, not by crushing rubber until metal contact.

For initial quote, use the square dimensions in the table. If any station needs corner trimming or a relieved edge, release that exact trimmed shape after the landing-face photos are checked.

2D SVG/DXF controls for the current square body pads are `data/manual/fabrication/rubber_recreation_rev_a/bm_iso_sm_square_pad_rev_a.*` and `data/manual/fabrication/rubber_recreation_rev_a/bm_iso_lg_square_pad_rev_a.*`. The complete dashboard preview is `data/manual/fabrication/rubber_recreation_rev_a/chassis_rubber_all_drawings_preview_rev_a.svg`, and the vehicle-use map is `data/manual/fabrication/rubber_recreation_rev_a/chassis_rubber_location_map_rev_a.svg`. 3D model files for the current quote geometry are in `data/manual/fabrication/rubber_recreation_rev_a/models_3d/`. The body-pad models default to `hole_d = 18.0`, based on Toyota `90560-12009` spacer evidence. Production release uses the 18.0 mm bore; `hole_d = 0` is a non-release CAD override only.

## Bump Stop Shape

The current best local photo for the old bump-stop fragments is the image that was previously attached to the dashboard item `Front-support right strip / liner`:

<img src="../photos/20260502_004222_gp_PKRe5HSQ.jpg" width="260" alt="Old bump-stop fragments with tape reference">

Supporting vertical-scale view:

<img src="../photos/20260502_004201_gp_zfUSmKJg.jpg" width="260" alt="Old bump-stop fragment vertical scale reference">

Use those photos only as shape evidence. Combining the two remaining broken rubber pieces supports the Toyota-style rubber form: wider at the bracket/base face, tapered/radiused sides, and a smaller flat strike face. The photos do not safely release the rubber base footprint, stretch-fit hole pitch/size, or exact strike-face offset.

Provisional Longman quote shape for bump stops:

| Feature | Long `48304-60010` family | Short `48304-60020` family |
| --- | --- | --- |
| Quantity | `3` total: front-left, rear-left, rear-right | `1` total: front-right |
| Free height | `70 +/-1 mm` | `60 +/-1 mm` |
| Rubber mounting interface | Rubber base footprint, bolt/stud pitch, and relaxed hole/slot size copied from the cleaned vehicle bracket and fitted fasteners; rubber stretches over/around the bolts or studs | Same rule; right-front bracket controls any local difference |
| Rubber profile | Progressive taper, radiused sides, wider at mount/base than strike face | Same profile, reduced height |
| Strike face | Flat rectangular lower face, centred on axle strike pad within `+/-5 mm` | Same |
| Production release | One `70 mm` first article first, fitted to the vehicle bracket | One `60 mm` first article first, fitted to the vehicle bracket |

Reference controls checked:

- ToJo `48304-60010` lists the long stop for left-front and rear axle positions and gives `Height = 70mm`.
- ToJo `48304-60020` lists the right-front stop and gives `Height = 60mm`; it also warns some aftermarket right-front stops are wrongly made at `70mm`.
- Cruiser Corps describes the long stop as fitting both rear positions and the left front; for the right front it notes the shorter factory-spec stop.
- City Racer lists the set mapping as front-left `48304-60010`, front-right `48304-60020` shorter, rear-left `48304-60010`, rear-right `48304-60010`.
- Nengun confirms `48304-60010` as a genuine Toyota spring bumper reference with Land Cruiser 40 fitment.

Links:

- https://www.tojo4wdcentre.com.au/part-shop/view/2008/201/parts-suitable-for-landcruiser/landcruiser-hj45-troop-4-79-7-80/48304-60010-bumper-stop-front-lh-rear-axle-to-chassis-suitable-for-landcruiser-40-45-55-series
- https://www.tojo4wdcentre.com.au/part-shop/view/2009/85/parts-suitable-for-landcruiser/landcruiser-bj40-9-77-7-80/48304-60020-bumper-stop-front-rh-front-axle-to-chassis-suitable-for-landcruiser-40-45-series
- https://cruisercorps.com/products/axle-bump-stop-long
- https://www.cityracerllc.com/products/spring-bump-stop-for-58-to-80-land-cruiser-fj40
- https://www.nengun.com/oem/toyota/48304-60010

## Required Measurements Before Final Production

These are the exact photos/measurements to collect and send with the old parts.

### Body Isolator Stations

For every body-mount station:

- Label station: front-left, front-right, middle-left, middle-right, rear-left, rear-right, plus any extra cowl/front-support point.
- Square-on photo of tub-side landing face with ruler.
- Square-on photo of chassis-side landing face with ruler.
- Maximum flat footprint available before bends, seams, weld lips, captive-nut repairs, or rust-thinned edges.
- Desired rubber free height at that station, or old rubber height if a best sample survives.
- Bolt size and whether the station uses captive nut or through-bolt.
- Old crush-sleeve OD/ID if available, only to confirm the Toyota `90560-12009` family or give a local machinist the OD to copy.
- Confirm the released `18.0 mm` Longman bore clears the sleeve without allowing stack wander.
- Note whether square `70 x 70` or `80 x 80` pad fits, or which exact corners/edges need trimming.

These are local vehicle checks only. They do not reopen the body-pad bore or sleeve
length spec: quote production pads with an `18.0 mm` bore for Toyota `90560-12009`
style spacers, and use `48.1 mm` sleeves.

### Front Oval Pads

- Top photo of each old oval pad with ruler.
- Caliper length, width, and thickness.
- Hole edge-to-edge or centre-to-centre measurement for the two holes.
- Hole diameter.
- Photo/measurement of any metal insert, boss, or relief.
- Confirmation whether the rectangular relief is functional or only deformation from the old stack.

### Underfloor Body-Support Strip Pair

- Use the released rubber size `420 x 38 x 8 mm` as the first-article basis.
- Mark orientation, side, and any local end trim only after the first dry-fit on the actual crossmember landing.
- Reuse the original slotted steel retainers if they are serviceable; if not, trace them directly before remaking steel.
- Do not punch holes or slots through the rubber unless the installed sample proves the original rubber itself was pierced.

### Long / Full-Width Flat Liners

These are not yet released for order. If the longer flat pieces are found, collect this set before asking Longman to quote them:

- Location photo showing the full installed path: tub-to-chassis, front apron/nose support, floor crossmember, rear sill, or panel-to-panel joint.
- Full-length photo with tape measure visible end to end.
- Close photos of both ends, any holes/slots/notches, and the contact face marks.
- Quantity, side, orientation, and whether each piece is handed or full body width.
- Length, width at several points, thickness, hole/slot size, hole centre distances, and edge radii.
- Whether the rubber was loose, bonded, clipped, trapped under bolts, or glued.
- Compression gap or witness marks showing whether it acts as a body isolator, anti-squeak liner, seal, or packing strip.

### Bump Stops

For each station, take a new close photo set after cleaning:

- Wide station photo: front-left, front-right, rear-left, rear-right.
- Square-on bracket photo with ruler/caliper.
- Bolt/stud hole photo with ruler across centres.
- Side photo showing bracket face, axle strike pad, and current gap.
- Loaded ride-height gap after suspension is fitted.
- Safe near-full-bump photo or measurement to confirm the stop contacts before shock bottoming, tyre/body contact, spring/shackle bind, brake-hose strain, or metal contact.

Record these bump-stop values:

| ID | Measurement | Use |
| --- | --- | --- |
| `BL` | Vehicle bracket landing length | Rubber base length |
| `BW` | Vehicle bracket landing width | Rubber base width |
| `P` | Bolt/stud pitch centre-to-centre, measured from the vehicle bracket | Rubber stretch-fit hole/slot pattern |
| `D` | Hole diameter or stud/bolt thread, measured from the vehicle bracket and fitted fastener | Relaxed rubber hole/slot size for stretch-fit installation |
| `X/Y` | Strike-pad centre offset from bracket holes | Contact face location |
| `G` | Loaded stop gap | Ride-height clearance |
| `F` | Near-full-bump clearance | Confirms stop acts before hard limits |

## Acceptance Requirements

For the Longman batch:

- Supplier provides material declaration: compound family and Shore A target.
- Make one first article of `BM-ISO-SM`, one `BM-ISO-LG`, one `FS-OVAL`, one `BUMP-60010-LONG`, and one `BUMP-60020-SHORT` before full batch if moulding/custom cutting is required.
- Body/front-support pieces average `55-65 Shore A`.
- Bump-stop rubber averages `65-75 Shore A`.
- Faces on body pads are flat and parallel within `0.5 mm`.
- Holes are drilled/punched cleanly; no burnt, torn, or cracked hole edges.
- Bump-stop first articles stretch-fit over/around the bolts or studs without tearing, then pass 50 percent compression without cracking, hole breakout, or permanent collapse; after 30 minutes unloaded, height recovers to at least 90 percent.
- Parts are bagged/labeled by ID and side/station.

## Excluded From This Longman Rubber Order

- Body-mount cup/seat washers.
- Body-mount crush sleeves.
- Body shims/spacers.
- Bolts, nuts, weld nuts, and captive-thread repairs.
- Brake hoses, fuel hoses, coolant hoses, and formed metal pipes. Those are now controlled separately in `docs/longman-pipe-hose-order-spec-20260512.md`.
- Door/window/weatherstrip, hardtop/roof/tub seals, bonnet/apron bump rubbers, and rear ambulance/barn door seals. Those are now controlled separately in `data/manual/rubber_ordering_specs.csv` rows `RUB-018` through `RUB-021` and `RUB-029` through `RUB-032`.
- Exhaust hanger/cushion rubbers, unless a physical sample or installed support-point measurement set is available. Current exhaust rubber control is `RUB-022`; `EXH-HGR-90917` stays hold-only for this Longman batch.
