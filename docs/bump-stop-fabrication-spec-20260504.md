# J40 Bump Stop Fabrication Spec - 2026-05-04

Scope: replacement bump stops for the leaf-spring axle-to-chassis stops where Toyota supply cannot be relied on and the old rubber is too decayed to use as the mould master.

This is not a Toyota engineering/mould drawing. Toyota almost certainly had a formal drawing for `48304-60010` and `48304-60020`, but the public OEM/catalog pages checked do not expose the mould dimensions, compound recipe, bonded-plate construction, or load/deflection curve. Treat the Toyota numbers and known application/height data as external controls, then release the local mould from the current vehicle brackets, axle strike pads, and first-article tests.

If a Toyota dealer, NOS part, or genuine sample becomes available, use it as the preferred master before cutting a mould. Until then, the fabricator must reproduce the Toyota-style progressive stop, not invent a square rubber block.

## External Reference Controls

| Controlled part | Qty | Position | Toyota reference | Free height target | Source role |
| --- | ---: | --- | --- | ---: | --- |
| `BUMP-60010-FL` | `1` | Front left spring bump stop | `48304-60010` | `70 mm` | Long stop. Fits front-left on Land Cruiser 40/45 and rear axle pair. |
| `BUMP-60020-FR` | `1` | Front right spring bump stop | `48304-60020` | `60 mm` | Short right-front stop. Do not substitute the `70 mm` long stop unless a full bump-clearance test proves it must be trimmed to the right-front height. |
| `BUMP-60010-R` | `2` | Rear spring bump stops | `48304-60010` | `70 mm` | Matched rear pair using the long stop geometry. |

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

## Toyota-Style Shape To Reproduce

The correct fabrication target is an axle-to-chassis stop assembly, not just a rubber pad. Use the reference image `deliverables/selling_site_images/images/reference_catalog/bump_stop.jpg` and any usable old/NOS sample to control the visible form:

- A one-piece pressed/formed steel saddle or backing bracket with two mounting ears/holes.
- A bonded or mechanically captive rubber body under the saddle; no exposed rusty old backing plate is reused.
- A tapered, radiused, progressive rubber body: wider at the saddle/base, narrowing toward the axle strike face.
- A flat rectangular strike face on the lower rubber body that lands squarely on the axle strike pad.
- Radiused edges and fillets around the load path; no sharp-corner cuboid, tyre-rubber block, or stacked washers.
- If a shop cannot bond rubber to a steel saddle, it must propose an equivalent captive construction and prove it by first-article pull/peel/seat checks before production.

Fabricator deliverables before mould release:

1. Sketch or CAD view of the side profile, plan view, steel saddle, hole centres, and rubber strike face.
2. Material declaration: rubber/PU family, Shore A target, and whether the rubber is bonded, cast around, or mechanically captured to the steel.
3. Vehicle measurement sheet with `BL`, `BW`, `P`, `D`, `X/Y`, `G`, and `F` values for each station.
4. First-article photos on the vehicle and a basic compression/recovery test result.

## Fabrication Route

Use a molded or cast progressive bump stop with a steel saddle/backing plate. Do not cut a simple solid cuboid from sheet rubber.

Preferred material:

- New automotive bump-stop rubber, `NR/SBR` or equivalent suspension bump-stop compound.
- Hardness target `70 +/-5 Shore A`.
- Tensile strength target `>=10 MPa`.
- Elongation at break target `>=300%`.
- Compression set target `<=30%` after `22 h` at `70 C` and `25%` deflection if the compound supplier can certify it.
- Exterior underbody service: oil splash resistant enough for chassis use, ozone/weather protected, no tyre rubber, crumb rubber, sponge, mixed offcuts, salvage rubber, or unmarked compound.

Acceptable local fallback:

- Cast automotive polyurethane only if the fabricator cannot mould rubber and can keep the same progressive geometry.
- Hardness target `80 +/-5 Shore A` for PU.
- Make the four stops as one batch and trial-fit before accepting final production.
- PU fallback must still use the Toyota-style tapered body, steel saddle/captive mounting, correct height, and strike-face location. A cast square block is not acceptable.

## Vehicle-Controlled Mould Dimensions

The decayed old rubber is not the master. Release these values from the actual brackets and strike pads on the vehicle, in millimetres.

| Measurement ID | Measurement | How to take it | Controls |
| --- | --- | --- | --- |
| `BL` | Bracket landing length | Clean the bracket and measure the flat landing or metal backing outline with calipers. | Rubber/base plate length. |
| `BW` | Bracket landing width | Measure the usable bracket width at the mounting face. | Rubber/base plate width. |
| `P` | Bolt or stud pitch | Measure centre-to-centre between the bracket holes/studs. | Captive plate or through-hole pattern. |
| `D` | Hole diameter/thread | Measure hole diameter or identify the fitted bolt/stud thread with a thread gauge. | Bolt clearance, insert, or captive stud size. |
| `X/Y` | Strike-pad centre offset | With the axle under the stop, mark the centre of the axle contact pad relative to the bracket holes. | Rubber contact face location. |
| `G` | Loaded stop gap | With the Ironman suspension fitted, tyres on ground, normal vehicle load, measure bracket face to axle strike pad. | Ride-height clearance check. |
| `F` | Full-bump limiting clearance | Jack the axle upward safely until the earliest limit is near: shock bottoming, tyre/body contact, spring/shackle bind, brake hose strain, or metal contact. | Confirms the stop touches before any hard limit. |
| `C` | Compressed stop allowance | Compress first article on a press to `50%` height and check no cracking, delamination, or permanent collapse. | Progressive compression and rebound acceptance. |

Geometry release rules:

- Base footprint: `BL x BW` from the vehicle bracket, with `0.5-1.0 mm` edge clearance so the part fits without grinding the bracket.
- Mounting holes/studs: use vehicle `P` and `D`; hole location tolerance `+/-0.5 mm`; hole diameter `+0.5/-0.0 mm` for clearance holes.
- Rubber height: `70 +/-1 mm` for `BUMP-60010-FL` and both `BUMP-60010-R`; `60 +/-1 mm` for `BUMP-60020-FR`.
- Matched rear pair: rear left and rear right free height must match within `1 mm`, and hardness readings must be within `5 Shore A`.
- Contact face: centred on the axle strike pad within `+/-5 mm`; face must be radiused/tapered, not a sharp-edged block.
- Side profile: taper the body so compression is progressive and so the rubber does not foul the bracket, U-bolts, spring pack, shock, or tyre through axle movement.
- Steel saddle/backing plate: make new deburred corrosion-protected steel with the Toyota-style two-ear mounting layout. Measure thickness from a usable sample if one is found; otherwise the shop must size the steel so it does not bend in the 50% compression test. Do not bond new rubber to rusty old steel.

## First Article Test

Make one `70 mm` long stop first and one `60 mm` right-front stop first. Do not make the full set until both pass.

Acceptance:

1. Bolts or studs pass through by hand and the stop seats flat on the bracket.
2. Contact face lands on the axle strike pad within `+/-5 mm`.
3. Stop engages before shock bottoming, tyre/body contact, spring/shackle bind, brake hose strain, or metal-to-metal contact.
4. Compressed to `50%` of free height on a press, the rubber shows no cracking, tearing, delamination, plate separation, or permanent collapse.
5. After `30 min` unloaded at room temperature, height recovery is at least `90%`.
6. Installed stops do not foul brake hoses, hard lines, U-bolts, shocks, tyres, springs, or steering through the checked travel range.

Reject:

- Any `BUMP-60020-FR` made at `70 mm` unless it is deliberately trimmed/released from the vehicle full-bump test.
- Any simple cut block, square tyre-rubber pad, reused rubber, or universal stop whose contact point misses the axle pad.
- Any part with cracks, voids larger than `1 mm` on a load face, loose backing plate, visible filler chunks, oily bleed, tacky uncured surface, or mismatched height/hardness across an axle pair.
- Any part whose steel saddle bends, peels away, or can be separated from the rubber by hand after compression.

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

Before fabrication, take four new close photo sets: front-left, front-right, rear-left, rear-right, each with a ruler/caliper on the bracket holes and a side view of the axle strike pad.
