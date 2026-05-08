# Chassis Rubbers Workstream

Date: 2026-05-08

Purpose: keep the chassis/body rubber order aligned with the current evidence. The current Longman order is rubber-only. Steel washers, cup/seat washers, crush sleeves, shims, bolts, and captive-thread repairs are inspected or ordered separately because they control the stack but are not custom rubber pieces.

Current supplier pack:

- [Longman rubber order spec](longman-rubber-order-spec-20260508.md)
- [Longman rubber order CSV](../data/manual/longman_rubber_order_specs.csv)
- [Bump-stop fabrication spec](bump-stop-fabrication-spec-20260504.md)

## Current Order Basis

The old release specs assumed cup/seat washers and a controlled crush sleeve. That remains true for stack control, but the tub/chassis photos do not prove a shaped rubber socket. Treat the main body mounts as function-first isolator pads.

Critical controls:

- Installed rubber height and final compression.
- Central hole/sleeve fit once the sleeve OD is known.
- Bolt clamps through the steel sleeve, not by crushing rubber until metal contact.
- Bearing area covers the landing faces without running onto bends, seams, weld lips, repairs, or rust-thinned edges.
- Similar hardness across the set, target Shore A `60 +/-5`.
- Solid new automotive rubber only: no tyre rubber, crumb rubber, sponge, foam, mixed offcuts, salvage rubber, or unmarked old stock.

Preferred custom shape for the main pads is square. Release trimming only if a later station photo proves a specific corner or edge needs relief.

## Rubber Order Lines

| ID | Status | Qty | Current spec | Release gate |
| --- | --- | ---: | --- | --- |
| `BM-ISO-SM` | Quote ready, drill after sleeve measurement | `10 + 2 spares` | Square pad `70 x 70 x 22 mm`, flat parallel faces, light edge radius/chamfer, Shore A `60 +/-5`. | Confirm each station has enough flat footprint; final hole = sleeve OD + `0.5-1.0 mm`. |
| `BM-ISO-LG` | Quote ready, drill after sleeve measurement | `2 + 1 spare` | Square pad `80 x 80 x 24 mm`, flat parallel faces, light edge radius/chamfer, same compound batch as small pads if possible. | Confirm the large-pair station; final hole = sleeve OD + `0.5-1.0 mm`. |
| `FS-OVAL` | Quote ready, caliper before production | `2` | Oval/capsule pad `96 x 64 x 15 mm`, two `12 mm` holes at `64 mm` centres; rectangular relief only if old sample confirms it is functional. | Confirm hole centres, thickness, insert/boss/relief construction. |
| `FS-STRIP-L` | Hold, candidate only | Hold | Working quote envelope `165 x 40 mm`; base `8 mm`; raised/load pad `14 mm`. | Must be confirmed by physical front-support carrier or installed location trace before cutting. Current image evidence is mixed with bump-stop fragments. |
| `FS-STRIP-R` | Hold, candidate only | Hold | Mirror of left only if the right-side carrier proves symmetric. | Same hold as left; mark handedness and hole centres from carrier, not torn rubber. |
| `BUMP-60010-LONG` | First article required | `3` | Toyota-style long bump stop, free height `70 +/-1 mm`, progressive tapered/radiused body, two-ear steel saddle/backing, flat rectangular strike face. | Vehicle bracket controls BL/BW/P/D/X-Y/G/F; make one first article before remaining long stops. |
| `BUMP-60020-SHORT` | First article required | `1` | Toyota-style short right-front bump stop, free height `60 +/-1 mm`; do not make it `70 mm` unless a deliberate full-bump test releases trimming. | Right-front bracket and axle strike pad control base, hole pattern, and contact face. |
| `BODY-LINER-FULL-WIDTH-HOLD` | Not captured yet | Hold | Possible long/full-width flat body or panel liner strips. | Do not order until the pieces are found or a vehicle station proves a continuous flat anti-squeak liner is required. |
| `EXH-HGR-90917` | Optional later hold | Hold | Teardrop exhaust hanger cushion from sample or genuine part reference. | Needs intact sample/proper tracing before production. |

## Known vs Candidate Pieces

Known current rubber pieces:

- Main body isolator pads: required, but now specified as square flat custom pads instead of circular/register bushings.
- Two-hole front-support oval pads: required by old sample/photo trail, subject to caliper confirmation.
- Axle bump stops: required if missing/decayed; height split is externally controlled as `70 mm` long stops for front-left/rear pair and `60 mm` short stop for front-right.

Candidate or unproven pieces:

- `FS-STRIP-L/R` front-support strip/liner pieces are not production-released. The loose-part photo trail suggests a possible strip or bonded liner, but the dashboard image currently used for the right strip is also the best evidence for broken bump stops. Treat the strip rows as a measurement hold until a physical carrier, installed location, or clean old strip proves them.
- Possible longer full-body-width flat pieces are not yet captured as orderable parts. They may be anti-squeak liners, panel-to-panel strips, packing pieces, or body support rubbers, but there is not enough evidence to assign quantity or dimensions.

## Photo Correction

The current dashboard page had the front-support strip/liner rows mixed up with bump-stop fragments:

- `20260502_004222_gp_PKRe5HSQ.jpg` should be treated as bump-stop fragment evidence first, not a released right strip/liner master.
- `20260502_004201_gp_zfUSmKJg.jpg` supports the bump-stop vertical/scale view and should not release the left strip/liner shape on its own.
- `FS-STRIP-L/R` should use the blank template/trace route until a clean physical trace exists.

Use these bump-stop photos only as broken-shape evidence. They do not release the bolt pitch, base footprint, or strike-face offset.

## Separated Hardware

The following remain required for body-mount stack control but are excluded from the Longman rubber order:

- Body-mount cup/seat washers.
- Body-mount crush sleeves.
- Body shims/spacer plates.
- Bolts, nuts, weld nuts, repair tabs, and captive-thread repairs.

Inspect the existing washers/cups separately. Reuse only if they are flat where required, not thinned, not cracked, and still fit the rubber/sleeve stack. If new ones are needed, order them as steel hardware, not as rubber.

## Measurements To Collect

### Main Body Isolator Stations

For every station:

- Label station and side.
- Tub-side landing face photo with ruler.
- Chassis-side landing face photo with ruler.
- Maximum flat footprint before bends, seams, weld lips, repairs, or rust-thinned edges.
- Desired free height or best old-sample free height.
- Bolt size and captive nut or through-bolt arrangement.
- Old crush-sleeve ID, OD, and length if available.
- Final sleeve OD; rubber hole should be sleeve OD + `0.5-1.0 mm`.
- Whether the square `70 x 70` or `80 x 80` pad fits, or which exact corners/edges need trimming.

### Front-Support Oval Pads

- Top photo of each old oval pad with ruler.
- Length, width, thickness.
- Hole diameter and hole centre-to-centre.
- Photo/measurement of insert, boss, washer imprint, or relief.
- Confirmation whether the rectangular relief is functional or old deformation.

### Front-Support Strip/Liner Holds

- Photo of the physical carrier or installed location proving the strip exists.
- Trace of left and right pieces on card or acetate.
- Orientation marks: side, front/rear, up/down.
- Total length, width at three points, base thickness, raised-pad height.
- Hole centres from the steel carrier, not the torn rubber.
- Bonded/loose/clipped status and cleaned carrier photos if bonded.

### Long / Full-Width Flat Liner Holds

If longer flat pieces are found:

- Location photo showing full installed path.
- Full-length photo with tape measure end to end.
- Close photos of both ends, holes, slots, notches, and witness/contact marks.
- Quantity, side, handedness, and whether the part is full body width.
- Length, width at several points, thickness, hole/slot size, hole centre distances, and edge radii.
- Whether it was loose, bonded, clipped, trapped under bolts, or glued.
- Evidence of function: isolator, anti-squeak liner, seal, or packing strip.

### Bump Stops

For front-left, front-right, rear-left, and rear-right:

- Wide station photo.
- Clean bracket photo with ruler/caliper.
- Bolt/stud hole photo with centre-to-centre measurement.
- Side photo showing bracket face, axle strike pad, and current gap.
- Loaded ride-height gap after suspension is fitted.
- Near-full-bump measurement confirming the stop contacts before shocks, tyres, springs, shackles, brake hoses, or metal hard limits.

Record:

| ID | Measurement | Use |
| --- | --- | --- |
| `BL` | Bracket landing length | Saddle/base length |
| `BW` | Bracket landing width | Saddle/base width |
| `P` | Bolt/stud pitch centre-to-centre | Saddle hole pattern |
| `D` | Hole diameter or stud/bolt thread | Hole/insert size |
| `X/Y` | Strike-pad centre offset from bracket holes | Contact face location |
| `G` | Loaded stop gap | Ride-height clearance |
| `F` | Near-full-bump clearance | Confirms stop acts before hard limits |

## Acceptance

- Longman provides compound family and Shore A target.
- Body/front-support rubber averages Shore A `55-65`.
- Bump-stop rubber averages Shore A `65-75`, or PU `75-85` only if the steel saddle/captive mounting and progressive shape are correct.
- Faces on body pads are flat and parallel within `0.5 mm`.
- Holes are clean, not burnt or torn.
- First bump-stop articles seat flat, bolt by hand, contact the strike pad within `+/-5 mm`, survive 50 percent compression without cracking or saddle/bond failure, and recover to at least 90 percent height after 30 minutes unloaded.
- Parts are bagged and labeled by ID and side/station.
