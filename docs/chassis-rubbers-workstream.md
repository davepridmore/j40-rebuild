# Chassis Rubbers Workstream

Date: 2026-05-08

Purpose: keep the chassis/body rubber order aligned with the current evidence. The current Longman order is rubber-only. Steel washers, cup/seat washers, crush sleeves, shims, bolts, and captive-thread repairs are inspected or ordered separately because they control the stack but are not custom rubber pieces.

Current supplier pack:

- [Longman rubber order spec](longman-rubber-order-spec-20260508.md)
- [Longman rubber order CSV](../data/manual/longman_rubber_order_specs.csv)
- [Parametric 3D rubber models](../data/manual/fabrication/rubber_recreation_rev_a/models_3d/README.md)
- [Bump-stop fabrication spec](bump-stop-fabrication-spec-20260504.md)

## Current Order Basis

The old release specs assumed cup/seat washers and a controlled crush sleeve. That remains true for stack control, but the tub/chassis photos do not prove a shaped rubber socket. Treat the main body mounts as function-first isolator pads.

Critical controls:

- Installed rubber height and final compression.
- Central `18.0 mm` bore for Toyota `90560-12009` style sleeve.
- Bolt clamps through the steel sleeve, not by crushing rubber until metal contact.
- Bearing area covers the landing faces without running onto bends, seams, weld lips, repairs, or rust-thinned edges.
- Similar hardness across the set, target Shore A `60 +/-5`.
- Solid new automotive rubber only: no tyre rubber, crumb rubber, sponge, foam, mixed offcuts, salvage rubber, or unmarked old stock.

Preferred custom shape for the main pads is square. Release trimming only if a later station photo proves a specific corner or edge needs relief.

## Rubber Order Lines

| ID | Status | Qty | Current spec | Release gate |
| --- | --- | ---: | --- | --- |
| `BM-ISO-SM` | First-article ready with OE spacer bore | `10 + 2 spares` | 3D envelope `70 L x 70 W x 22 H mm`; square flat pad; flat parallel faces; plan corners `R1.5`; top/bottom edge break or chamfer `1.0 mm` max; `18.0 mm` through bore; Shore A `60 +/-5`. | Confirm each station has enough flat footprint; sleeve basis is Toyota `90560-12009` style spacer. |
| `BM-ISO-LG` | First-article ready with OE spacer bore | `2 + 1 spare` | 3D envelope `80 L x 80 W x 24 H mm`; square flat pad; flat parallel faces; plan corners `R1.5`; top/bottom edge break or chamfer `1.0 mm` max; `18.0 mm` through bore; same compound batch as small pads if possible. | Confirm the large-pair station; sleeve basis is Toyota `90560-12009` style spacer. |
| `FS-OVAL` | Quote ready, caliper before production | `2` | 3D envelope `96 L x 64 W x 15 T mm`; capsule ends `R32`; outer edge break `0.5-1.0 mm`; two `12 mm` holes at `64 mm` centres; rectangular relief only if old sample confirms it is functional. | Confirm hole centres, thickness, insert/boss/relief construction. |
| `FS-STRIP-L` | Custom first article ready | `1` | 3D envelope `165 L x 38 W x 8 T mm`; plan corners `R1.5`; top/bottom edge break `0.5-1.0 mm`; no through-holes in the rubber by default; Shore A `60 +/-5`. | Dry-fit on the actual landing, then apply any side-specific end trim; reuse or trace the slotted steel retainer separately if needed. |
| `FS-STRIP-R` | Custom first article ready | `1` | Same flat strip spec as left: `165 L x 38 W x 8 T mm`, plan corners `R1.5`, top/bottom edge break `0.5-1.0 mm`. Use the same blank unless the right side proves a handed end trim. | Same first-article dry-fit and retainer rule as left. |
| `BUMP-60010-LONG` | First article required | `3` | Toyota-style long bump stop, free height `70 +/-1 mm`, progressive tapered/radiused body, two-ear steel saddle/backing, flat rectangular strike face. | Vehicle bracket controls BL/BW/P/D/X-Y/G/F; make one first article before remaining long stops. |
| `BUMP-60020-SHORT` | First article required | `1` | Toyota-style short right-front bump stop, free height `60 +/-1 mm`; do not make it `70 mm` unless a deliberate full-bump test releases trimming. | Right-front bracket and axle strike pad control base, hole pattern, and contact face. |
| `BODY-LINER-FULL-WIDTH-HOLD` | Not captured yet | Hold | Possible long/full-width flat body or panel liner strips. | Do not order until the pieces are found or a vehicle station proves a continuous flat anti-squeak liner is required. |
| `EXH-HGR-90917` | Optional later hold | Hold | Teardrop exhaust hanger cushion from sample or genuine part reference. | Needs intact sample/proper tracing before production. |

## Known vs Candidate Pieces

Known current rubber pieces:

- Main body isolator pads: required, but now specified as square flat custom pads instead of circular/register bushings.
- Two-hole front-support oval pads: required by old sample/photo trail, subject to caliper confirmation.
- Axle bump stops: required if missing/decayed; height split is externally controlled as `70 mm` long stops for front-left/rear pair and `60 mm` short stop for front-right.
- `FS-STRIP-L/R` flat strip pair: now evidenced by the May 17 loose-part photos plus installed-location photos. Treat these as custom underfloor body-support / anti-squeak strips, not generic body-mount biscuits.
- Rubber definitions must carry the 3D envelope and edge/profile control, not only a flat plan size.

Candidate or unproven pieces:

- Possible longer full-body-width flat pieces are not yet captured as orderable parts. They may be anti-squeak liners, panel-to-panel strips, packing pieces, or body support rubbers, but there is not enough evidence to assign quantity or dimensions.

## Photo Correction

The old strip rows had been mixed up with bump-stop evidence. The May 17 photo set resolves that:

- `20260502_004222_gp_PKRe5HSQ.jpg` and `20260502_004201_gp_zfUSmKJg.jpg` remain bump-stop evidence first.
- `20260517_194143_gp_CO7MuMdA`, `20260517_194633_gp_rAjY3gjg`, and `20260517_194706_gp_twKRWGFA` are the installed-location proof for the flat strip pair.
- `20260517_193503_gp_N9nHjqXw`, `20260517_193539_gp_E0cR9I0A`, `20260517_193559_gp_NEpk1hpg`, `20260517_193612_gp_JmbfR0Tw`, and `20260517_193616_gp_1ye19BZA` are the loose-part measurement references.

## External Control Notes

Open-catalog checks support custom recreation of the strip pair rather than substitution from a standard body-mount kit:

- ToyotaPartsDeal `Cab Mounting & Body Mounting` for a 1978 Land Cruiser exposes the normal cushion/spacer/shim/holder rows, but not an open-catalog equivalent to this short underfloor strip.
- SOR `Body Mounts` likewise focuses on the standard large/small body-mount families and hardware.
- Aqualu's early-frame note also reinforces that the common body-mount discussion is about separate mount pads, not this strip-retainer arrangement.

Use those sources only as context. The actual released strip geometry is controlled by the May 17 loose-part and installed-location photos plus the original samples.

## Separated Hardware

The following remain required for body-mount stack control but are excluded from the Longman rubber order:

- Body-mount cup/seat washers.
- Body-mount crush sleeves.
- Body shims/spacer plates.
- Bolts, nuts, weld nuts, repair tabs, and captive-thread repairs.

Inspect the existing washers/cups separately. Reuse only if they are flat where required, not thinned, not cracked, and still fit the rubber/sleeve stack. If new ones are needed, order them as steel hardware, not as rubber.

### Body-Mount Sleeve Spec

The sleeve release is Toyota `90560-12009`, listed in Toyota Heritage/parts data as the body-mount spacer with `L=48.1 mm` on late 40-series body mounts. Open kit instructions also show the standard body-mount pack uses six steel tubes.

The only direct OD evidence found so far is a physical field measurement on IH8MUD: all six original crush tubes were identified as Toyota `90560-12009`; the Toyota tube was described as a bit over `17 mm` OD, the lower Toyota bushing centre hole as `18 mm`, and a `16 mm` aftermarket tube as smaller/sloppier.

Use this as the exact best spec:

- Sleeve part: Toyota `90560-12009` style body-mount spacer, qty `6`.
- Sleeve length: `48.1 mm`.
- Sleeve ID: M10 clearance, `10.8-11.0 mm` if locally fabricated.
- Sleeve OD: copy a genuine/old `90560-12009`; do not choose arbitrary tube stock.
- Rubber bore: `18.0 mm` through for `BM-ISO-SM` and `BM-ISO-LG`.
- Reject: `16 mm` OD tube unless a dry-fit proves the stack cannot wander.
- Local fabrication route: machine one sample tube from old/OE dimensions, dry-fit with the `18.0 mm` rubber bore and cup/washer stack, then release the other five.

The open checks are local-fit checks only. They do not ask Longman or the machinist
to invent a dimension: the released spec remains Toyota `90560-12009`, `48.1 mm`
long, `18.0 mm` rubber bore, and OE/old-sleeve OD copied if a local sleeve has to
be made.

## Measurements To Collect

### Main Body Isolator Stations

For every station:

- Label station and side.
- Tub-side landing face photo with ruler.
- Chassis-side landing face photo with ruler.
- Maximum flat footprint before bends, seams, weld lips, repairs, or rust-thinned edges.
- Desired free height or best old-sample free height.
- Bolt size and captive nut or through-bolt arrangement.
- Old crush-sleeve OD/ID if available, only to confirm it matches the Toyota `90560-12009` family or to give a local machinist the OD to copy.
- Confirm the released `18.0 mm` rubber bore clears the sleeve without allowing the stack to wander.
- Whether the square `70 x 70` or `80 x 80` pad fits, or which exact corners/edges need trimming.

### Front-Support Oval Pads

- Top photo of each old oval pad with ruler.
- Length, width, thickness.
- Hole diameter and hole centre-to-centre.
- Photo/measurement of insert, boss, washer imprint, or relief.
- Confirmation whether the rectangular relief is functional or old deformation.

### Underfloor Body-Support Strip Pair

- Released first-article rubber size is `165 x 38 x 8 mm`.
- Confirm only the local handed end trim, if any, during dry-fit.
- Hole or slot geometry belongs to the steel retainer, not automatically to the rubber.
- Reuse or trace the original slotted steel retainers if they are not serviceable.

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
