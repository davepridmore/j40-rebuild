# J40 Bump Stop Fabrication Spec - 2026-05-04

Scope: replacement bump stops for the leaf-spring axle-to-chassis stops where Toyota supply cannot be relied on and the old rubber is too decayed to use as the mould master.

Status correction `2026-07-22`: a new four-stop set is in hand from the July 12 intake, but installation is not reported or scheduled. The owner's front/rear installation update referred to the separate vehicle bumpers. This document remains the received-part identity, dimensional, fixture, and eventual full-bump acceptance control; local fabrication is a fallback only if a received part fails those checks. When fitted, mount the stops through the correct separate chassis-side brackets/metal fixtures above the axles, not under the spring packs or U-bolt plates.

This is not a Toyota engineering/mould drawing. Toyota almost certainly had a formal drawing for `48304-60010` and `48304-60020`, but the public OEM/catalog pages checked do not expose the mould dimensions, compound recipe, internal reinforcement detail, metal fixture relationship, or load/deflection curve. Treat the Toyota numbers and known application/height data as external controls. The May 31 exact front bump-stop photos now control the visible local shape: a broad molded rubber body with two through-holes in the rubber, rounded/asymmetric sides, a central metal fixture/insert interface, and a flat strike face. Rear/back stops use the same front-stop shape and fixture pattern, made longer to the `70 mm` family height. Final station release still comes from calipers, the removed metal fixture, current vehicle brackets, axle strike pads, and first-article tests.

If a Toyota dealer, NOS part, or genuine sample becomes available, use it as the preferred master before cutting a mould. Until then, the fabricator must reproduce the Toyota-style progressive stop, not invent a square rubber block.

## External Reference Controls

| Controlled part | Qty | Position | Toyota reference | Free height target | Source role |
| --- | ---: | --- | --- | ---: | --- |
| `BUMP-60010-FL` | `1` | Front left spring bump stop | `48304-60010` | `70 mm` | Same May 31 front-stop shape family, made to the long height. |
| `BUMP-60020-FR` | `1` | Front right spring bump stop | `48304-60020` | `60 mm` | Exact front-stop shape from the May 31 photos at the short height. Do not substitute the `70 mm` long stop unless a full bump-clearance test proves it must be trimmed to the right-front height. |
| `BUMP-60010-R` | `2` | Rear spring bump stops | `48304-60010` | `70 mm` | Matched rear/back pair using the same front-stop body and fixture pattern, made longer. |

External references used:

- Nengun `48304-60010`: lists `SPRING BUMPER 48304-60010` as a genuine Toyota OEM part and shows Toyota Land Cruiser catalog fitment.
- ToJo 4WD Centre `48304-60010`: lists the left-front and rear axle application and `Height = 70mm`.
- ToJo 4WD Centre `48304-60020`: lists the right-front application and `Height = 60mm`, and warns that some aftermarket `48304-60020` stops are incorrectly made at the same `70 mm` height as `48304-60010`.
- Cruiser Corps long bump stop listing: states the long stop fits both rear positions and the left front, while the right-front position uses a shorter stop.

Links:

- https://www.nengun.com/oem/toyota/48304-60010
- https://www.tojo4wdcentre.com.au/part-shop/view/2008/201/parts-suitable-for-landcruiser/landcruiser-hj45-troop-4-79-7-80/48304-60010-bumper-stop-front-lh-rear-axle-to-chassis-suitable-for-landcruiser-40-45-55-series
- https://www.tojo4wdcentre.com.au/part-shop/view/2009/85/parts-suitable-for-landcruiser/landcruiser-bj40-9-77-7-80/48304-60020-bumper-stop-front-rh-front-axle-to-chassis-suitable-for-landcruiser-40-45-series
- https://cruisercorps.com/products/axle-bump-stop-long

## Sample-Controlled Shape To Reproduce

The correct fabrication target is now the exact front-stop photo set shown in `photos/20260531_171824_gp_HmSS2ChQ.jpg`, `photos/20260531_171833_gp_Vw96I7Mg.jpg`, `photos/20260531_171859_gp_i6bRyQKA.jpg`, `photos/20260531_171903_gp_jNI1gfYA.jpg`, and `photos/20260531_171935_gp_BYfhqiWg.jpg`. The May 29 removed-sample photos are supporting fixture and construction evidence only. The rear/back stops are the same body, through-hole layout, fixture/channel interface, and strike-face design made longer to the `70 mm` family height. It is not a plain rubber block, and it is not the earlier placeholder rubber bonded to a separate flat backing plate with holes only in steel. Use the May 31 front-stop photos, the May 29 fixture-support photos, the removed metal fixture, the cleaned vehicle brackets, the axle strike pads, and any usable NOS/genuine sample to control the visible form:

- Molded rubber body with two through-holes visible in the rubber body. The holes are now part of the rubber design because the removed samples prove them.
- Broad low body with rounded/asymmetric plan corners and battered/tapered sides copied from the better surviving sample faces, then cleaned up into a mouldable shape.
- Central metal fixture/insert interface or raised channel visible in the side view; trace the removed metal fixture and reproduce the rubber channel/relief that receives it.
- Flat/worn strike area on the lower rubber body that must land squarely on the axle strike pad.
- Radiused edges and fillets around the load path; no sharp-corner cuboid, tyre-rubber block, or stacked washers.
- Metal fixture/bracket hardware is a separate trace/reuse item. Do not replace the sample with the earlier flat-back-plate placeholder unless the actual fixture proves that construction at the vehicle.

Fabricator deliverables before mould release:

1. Sketch or CAD view of the side profile, plan view, rubber-through-hole layout, central fixture channel/insert interface, removed metal fixture trace, and rubber strike face.
2. Material declaration: rubber/PU family, Shore A target, any internal metal/reinforcement or fixture-retention method, and expected recovery.
3. Removed-sample plus vehicle measurement sheet with `BL`, `BW`, `P`, `D`, `X/Y`, `G`, `F`, and central fixture/channel values for each station.
4. First-article photos on the vehicle and a basic compression/recovery test result.

## Fabrication Route

Use a molded or cast progressive bump-stop rubber copied from the May 31 exact front-stop photo set, with the sample-proven rubber through-holes and central metal fixture/insert interface. Rear/back stops use that same shape family at the longer `70 mm` height. Do not cut a simple solid cuboid from sheet rubber and do not rely on ordinary glue-only attachment.

Preferred material:

- New automotive bump-stop rubber, `NR/SBR` or equivalent suspension bump-stop compound.
- Hardness target `70 +/-5 Shore A`.
- Tensile strength target `>=10 MPa`.
- Elongation at break target `>=300%`.
- Compression set target `<=30%` after `22 h` at `70 C` and `25%` deflection if the compound supplier can certify it.
- Exterior underbody service: oil splash resistant enough for chassis use, ozone/weather protected, no tyre rubber, crumb rubber, sponge, mixed offcuts, salvage rubber, or unmarked compound.

Acceptable local fallback:

- Cast automotive polyurethane only if the fabricator cannot mould rubber and can keep the same progressive geometry, fixture/captive construction, and rebound recovery.
- Hardness target `80 +/-5 Shore A` for PU.
- Make the four stops as one batch and trial-fit before accepting final production.
- PU fallback must still use the May 31 front-stop rounded/tapered body, rubber through-holes, central fixture/interface detail, correct height, and strike-face location. A cast square block is not acceptable.

## Vehicle-Controlled Mould Dimensions

The old rubber is now construction evidence, not a finished dimension master. Release these values from the May 31 exact front-stop photos, the May 29 fixture-support photos, the removed metal fixture, the actual vehicle brackets, and the strike pads, in millimetres.

| Measurement ID | Measurement | How to take it | Controls |
| --- | --- | --- | --- |
| `BL` | Rubber body / fixture landing length | Caliper the better surviving sample, the removed metal fixture, and cleaned bracket landing. | Rubber body outline, mould base, and fixture seat. |
| `BW` | Rubber body / fixture landing width | Caliper the better surviving sample and usable bracket/fixture width at the seating face. | Rubber body width and central fixture/channel clearance. |
| `P` | Rubber through-hole and fixture bolt/stud pitch | Measure centre-to-centre across the sample rubber holes and confirm against the removed metal fixture and vehicle bracket holes/studs. | Rubber hole pattern plus fixture alignment. |
| `D` | Rubber through-hole diameter and fitted bolt/stud/thread size | Measure the sample rubber holes and identify the fitted bolt/stud thread with a thread gauge. | Rubber clearance and fixture fastener control. |
| `X/Y` | Strike-pad centre offset | With the axle under the stop, mark the centre of the axle contact pad relative to the rubber through-holes and fixture/bracket bolt features. | Rubber contact face location. |
| `G` | Loaded stop gap | With the Ironman suspension fitted, tyres on ground, normal vehicle load, measure mount face to axle strike pad. | Ride-height clearance check. |
| `F` | Full-bump limiting clearance | Jack the axle upward safely until the earliest limit is near: shock bottoming, tyre/body contact, spring/shackle bind, brake hose strain, or metal contact. | Confirms the stop touches before any hard limit. |
| `C` | Compressed stop allowance | Compress first article on a press to `50%` height and check no cracking, delamination, or permanent collapse. | Progressive compression and rebound acceptance. |

Geometry release rules:

- The `P` and `D` dimensions on `data/manual/fabrication/rubber_recreation_rev_a/bump_stop_vehicle_measurement_control.svg` / `.dxf` are now rubber-through-hole plus fixture/bracket controls. These drawings are measurement controls only; they are not a released final cut profile until the samples, fixture, and bracket values are recorded.
- Base footprint: copy the May 31 exact front-stop family, then confirm it seats with the removed metal fixture and vehicle bracket with `0.5-1.0 mm` practical edge clearance where needed.
- Mounting holes/studs: use the sample rubber holes, removed metal fixture, and vehicle `P` and `D`; feature location tolerance `+/-0.5 mm`. Holes belong through the rubber because the removed samples prove that construction.
- Rubber height: `70 +/-1 mm` for `BUMP-60010-FL` and both `BUMP-60010-R`; `60 +/-1 mm` for `BUMP-60020-FR`. Height changes only stretch the same front-stop body family; do not create a separate rear shape.
- Matched rear pair: rear left and rear right free height must match within `1 mm`, and hardness readings must be within `5 Shore A`.
- Contact face: centred on the axle strike pad within `+/-5 mm`; face must be radiused/tapered, not a sharp-edged block.
- Side profile: taper the body so compression is progressive and so the rubber does not foul the mount, U-bolts, spring pack, shock, or tyre through axle movement.
- Vehicle bracket and removed metal fixture: clean and inspect before mould release. Repair chassis/bracket/fixture metal only under a separate metal-fabrication release; the bump-stop part itself is the molded rubber sample family with its proven through-holes and central fixture interface.

## First Article Test

Make one `70 mm` long stop first and one `60 mm` right-front stop first. Do not make the full set until both pass.

Acceptance:

1. The rubber through-holes align with the removed metal fixture and vehicle bracket, bolts/studs pass by hand, and the central fixture/interface is captured without tearing or rocking.
2. Contact face lands on the axle strike pad within `+/-5 mm`.
3. Stop engages before shock bottoming, tyre/body contact, spring/shackle bind, brake hose strain, or metal-to-metal contact.
4. Compressed to `50%` of free height on a press, the rubber shows no cracking, tearing, bond/captive failure, or permanent collapse.
5. After `30 min` unloaded at room temperature, height recovery is at least `90%`.
6. Installed stops do not foul brake hoses, hard lines, U-bolts, shocks, tyres, springs, or steering through the checked travel range.

Reject:

- Any `BUMP-60020-FR` made at `70 mm` unless it is deliberately trimmed/released from the vehicle full-bump test.
- Any simple cut block, square tyre-rubber pad, reused rubber, or universal stop whose contact point misses the axle pad.
- Any part with cracks, voids larger than `1 mm` on a load face, loose retention feature, visible filler chunks, oily bleed, tacky uncured surface, or mismatched height/hardness across an axle pair.
- Any part whose fixture interface tears, whose rubber separates from any retained insert/fixture, whose holes do not match the sample/vehicle pitch, or whose molded body reverts to the earlier flat-plate placeholder.

## Photo And Measurement Capture

For each station, take these before ordering the mould:

1. Wide photo showing which station it is: front-left, front-right, rear-left, rear-right.
2. Square-on photo of the cleaned mounting bracket with a ruler/caliper visible.
3. Close photo of the bolt holes/studs with the ruler across the centres.
4. Side photo showing bracket face, axle strike pad, and current gap.
5. Photo at axle-jacked near-full-bump showing the stop path and nearby shock, brake hose, spring, and tyre clearance.

Record the values in `data/manual/bump_stop_fabrication_specs.csv` or on the shop drawing before mould release.

## Existing Project Photos To Use

Use these only as station/context references. They are not dimension masters; final measurements still require ruler/caliper photos at each bracket.

| Photo | Use |
| --- | --- |
| `photos/20260501_193841_gp_ZwpHFiMA.jpg` | Current chassis/axle context after brushing; use to locate bracket and strike-pad area before close measurement. |
| `photos/20260501_193847_gp_uHWO7Bdw.jpg` | Second current-chassis angle for front/rear axle travel path context. |
| `photos/20260422_004254_gp_SplHLSYA.jpg` | Body-off underside context for spring/shackle/axle clearance. |
| `photos/20260422_004423_gp_B1N5ThVw.jpg` | Front frame-horn and suspension context; use only for orientation. |
| `photos/20260531_171824_gp_HmSS2ChQ.jpg` | Exact front bump-stop face/width measurement with tape; active mould-shape reference. |
| `photos/20260531_171833_gp_Vw96I7Mg.jpg` | Companion exact front bump-stop face/width measurement. |
| `photos/20260531_171859_gp_i6bRyQKA.jpg` | Exact front bump-stop base/fixture plate length and through-hole landing measurement. |
| `photos/20260531_171903_gp_jNI1gfYA.jpg` | Companion exact front bump-stop base/fixture plate measurement. |
| `photos/20260531_171935_gp_BYfhqiWg.jpg` | Exact front bump-stop side height/profile measurement; rear/back stops use this same shape made longer. |
| `photos/20260529_223605_gp_CklgF0cQ.jpg` | Supporting removed-sample face/plan view after unscrewing from metal fixture; confirms rubber through-holes and broad rounded body. |
| `photos/20260529_223701_gp_wYPExcAA.jpg` | Supporting removed-sample side view for central fixture/channel interface, not the active shape master. |

Before mould release, take station-fit photo sets for front-left, front-right, rear-left, and rear-right, each with a ruler/caliper on the bracket holes and a side view of the axle strike pad. These photos verify mounting and clearance; they do not replace the May 31 front-stop shape master.
