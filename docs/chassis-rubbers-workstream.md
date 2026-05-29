# Chassis Rubbers Workstream

Date: 2026-05-08

Purpose: keep the chassis/body rubber order aligned with the current evidence. The current Longman order is custom rubber, with bump-stop rubber now controlled by the May 29 removed samples after unscrewing from the metal fixture. Body-mount steel washers, cup/seat washers, crush sleeves, shims, bolts, and captive-thread repairs are inspected or ordered separately because they control the stack but are not custom rubber pieces.

Current supplier pack:

- [Longman rubber order spec](longman-rubber-order-spec-20260508.md)
- [Longman rubber order CSV](../data/manual/longman_rubber_order_specs.csv)
- [Current order preview](../data/manual/fabrication/rubber_recreation_rev_a/chassis_rubber_current_order_preview_rev_a.svg)
- [Chassis rubber location map](../data/manual/fabrication/rubber_recreation_rev_a/chassis_rubber_location_map_rev_a.svg)
- [Complete chassis rubber SVG preview](../data/manual/fabrication/rubber_recreation_rev_a/chassis_rubber_all_drawings_preview_rev_a.svg)
- [Parametric 3D rubber models](../data/manual/fabrication/rubber_recreation_rev_a/models_3d/README.md)
- [Bump-stop fabrication spec](bump-stop-fabrication-spec-20260504.md)

## Current Order Basis

The old release specs assumed cup/seat washers and a controlled crush sleeve. That remains true for stack control, but the tub/chassis photos do not prove a shaped rubber socket. Treat the main body mounts as function-first isolator pads.

The measured old-rubber photos are no longer being treated as an unknown-dimension problem. They are the quote and first-article basis for the current Longman rubber pieces. The remaining open work is station mapping and dry-fit release:

- Which measured part belongs at which vehicle station.
- Whether the square pad footprint clears the actual landing face at that station.
- Whether the sleeve/cup/shim/bolt stack clamps through the sleeve without over-crushing the rubber.
- Whether any first article needs local corner/end trimming after it is placed on the vehicle.

Critical controls:

- Installed rubber height and final compression.
- Central `18.0 mm` bore for Toyota `90560-12009` style sleeve.
- Bolt clamps through the steel sleeve, not by crushing rubber until metal contact.
- Bearing area covers the landing faces without running onto bends, seams, weld lips, repairs, or rust-thinned edges.
- Similar hardness across the set, target Shore A `60 +/-5`.
- Solid new automotive rubber only: no tyre rubber, crumb rubber, sponge, foam, mixed offcuts, salvage rubber, or unmarked old stock.

Preferred custom shape for the main pads is square. Release trimming only if a later station photo proves a specific corner or edge needs relief.

## Location And Coverage Check

The current Toyota GR Heritage 40-series list checked on 2026-05-28 does not expose a complete body/chassis rubber kit for this scope. EPC-style Toyota listings and aftermarket suppliers do confirm the usual body-mount cushion/spacer/shim families and early/late 40-series kit splits. That confirms the required families exist, but it does not replace this vehicle's station map, dry-stack checks, or the current Longman square-pad route. The source links are recorded in [Longman rubber order spec](longman-rubber-order-spec-20260508.md).

Use `../data/manual/fabrication/rubber_recreation_rev_a/chassis_rubber_location_map_rev_a.svg` as the dashboard/install location guide:

- `BM-ISO-SM` and `BM-ISO-LG`: main tub-to-chassis mount stack.
- `FS-OVAL`: separate left/right front support / nose-extension isolators.
- `FS-STRIP-L/R`: left/right underfloor front-support/body-support strip landings.
- `BUMP-60010-LONG`: front-left and both rear axle-to-chassis bump-stop stations.
- `BUMP-60020-SHORT`: right-front axle-to-chassis bump-stop station only.
- `BODY-LINER-FULL-WIDTH-HOLD` and `EXH-HGR-90917`: visible in the preview only as hold/reference controls.

## Rubber Order Lines

| ID | Status | Qty | Current spec | Release gate |
| --- | --- | ---: | --- | --- |
| `BM-ISO-SM` | Released for quote / first article | `10 + 2 spares` | 3D envelope `70 L x 70 W x 22 H mm`; square flat pad; flat parallel faces; plan corners `R1.5`; top/bottom edge break or chamfer `1.0 mm` max; `18.0 mm` through bore; Shore A `60 +/-5`. | Station mapping, footprint check, sleeve/cup/shim dry-stack, and compression check before final install. |
| `BM-ISO-LG` | Released for quote / first article | `2 + 1 spare` | 3D envelope `80 L x 80 W x 24 H mm`; square flat pad; flat parallel faces; plan corners `R1.5`; top/bottom edge break or chamfer `1.0 mm` max; `18.0 mm` through bore; same compound batch as small pads if possible. | Confirm the large-pair station, footprint, sleeve/cup/shim dry-stack, and compression check before final install. |
| `FS-OVAL` | Released for quote / first article | `2` | 3D envelope `96 L x 64 W x 15 T mm`; capsule ends `R32`; outer edge break `0.5-1.0 mm`; two `12 mm` holes at `64 mm` centres; rectangular relief only if old sample confirms it is functional. | Caliper-confirm hole centres, thickness, insert/boss/relief construction before final pair. |
| `FS-STRIP-L` | Released for quote / first article | `1` | 3D envelope `420 L x 38 W x 8 T mm`; plan corners `R1.5`; top/bottom edge break `0.5-1.0 mm`; no through-holes in the rubber by default; Shore A `60 +/-5`. | Dry-fit on the actual landing, then apply only proven end trim; reuse or trace the slotted steel retainer separately if needed. |
| `FS-STRIP-R` | Released for quote / first article | `1` | Same flat strip spec as left: `420 L x 38 W x 8 T mm`, plan corners `R1.5`, top/bottom edge break `0.5-1.0 mm`. Use the same blank unless the right side proves a handed end trim. | Same first-article dry-fit and retainer rule as left. |
| `BUMP-60010-LONG` | First article required | `3` | Sample-style long bump-stop rubber copied from the May 29 removed samples: two through-holes in the rubber, central fixture/channel interface, broad rounded/tapered body, and flat strike area; external long-family height target remains `70 +/-1 mm` pending caliper/vehicle release. | May 29 samples plus removed metal fixture, vehicle bracket, and axle strike pad control BL/BW/P/D/X-Y/G/F and fixture-channel dimensions; make one first article before remaining long stops. |
| `BUMP-60020-SHORT` | First article required | `1` | Same sample-style construction as the long stop, applied to the right-front station; external short-family height target remains `60 +/-1 mm` unless vehicle full-bump testing releases another height. | May 29 samples plus right-front bracket and axle strike pad control rubber footprint, through-hole pattern, fixture/channel interface, and contact face. |
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

- `20260502_004222_gp_PKRe5HSQ.jpg` and `20260502_004201_gp_zfUSmKJg.jpg` remain historical bump-stop context only; the May 29 removed samples supersede them for active construction.
- `20260517_194143_gp_CO7MuMdA`, `20260517_194633_gp_rAjY3gjg`, and `20260517_194706_gp_twKRWGFA` are the installed-location proof for the flat strip pair.
- `20260517_193503_gp_N9nHjqXw`, `20260517_193539_gp_E0cR9I0A`, `20260517_193559_gp_NEpk1hpg`, `20260517_193612_gp_JmbfR0Tw`, and `20260517_193616_gp_1ye19BZA` are the loose-part measurement references.
- `20260528_185826_gp_FoyeBPUg` and `20260528_185833_gp_gZBjUjPg` are strip/retainer landing context only. They do not release rubber holes, slots, bonding, handed trim, or bump-stop geometry.
- `20260528_193054_gp_UFyTb44w`, `20260528_193143_gp_Cn3OWzZQ`, and `20260528_193228_gp_PLATNsFQ` are loose body-mount rubber/cup stack context only. They show round/cup fragments with tape, but the photo angles do not reopen the active square `BM-ISO-SM` / `BM-ISO-LG` pad route.
- `20260528_193200_gp_HICSdovA` and `20260528_193253_gp_f0eQuSFA` are loose rectangular strip/block section context only. They do not release a new length, hole pattern, slot pattern, bonding, or handed trim.
- `20260529_223605_gp_CklgF0cQ` and `20260529_223701_gp_wYPExcAA` supersede the old flat-back-plate bump-stop placeholder. They show the bump stops after unscrewing from the metal fixture and release the construction concept for both stops: rubber through-holes, broad rounded body, and central fixture/channel interface. Final dimensions still need calipers and vehicle/fixture confirmation.

## Photo Measurement Audit

Checked on 2026-05-28:

- May 17 loose strip ruler photos show the underfloor strip length at about `16.5 in`, which converts to `419 mm`. The released first-article length is therefore corrected to `420 mm`, with the existing `38 W x 8 T mm` strip section retained.
- The visible elongated slots and rust-stained channel features belong to the steel retainer or witness marks. They are not released as rubber holes; the strip remains plain unless dry-fit proves otherwise.
- May 28 loose body-mount/cup photos were checked against the current body-pad designs. They add useful stack context, but no reliable new OD/height dimension replaces the current `70 x 70 x 22` and `80 x 80 x 24` square first articles.
- May 28 loose rectangular rubber close-ups support only the strip/section context. The active strip design remains the plain `420 x 38 x 8 mm` first article with no holes or slots by default.
- May 29 bump-stop photos after fixture removal now control the construction concept. They prove rubber through-holes and a central fixture/channel interface rather than the prior flat-back-plate-only placeholder. They do not release final dimensions; caliper the samples, removed fixture, and vehicle bracket before mould release. The external height controls remain `70 mm` long and `60 mm` right-front short until vehicle testing says otherwise.
- May 2 body-pad/cup photos support the current pad thickness range and washer/cup context, but do not prove a round rubber outside profile. The square `BM-ISO-SM` and `BM-ISO-LG` first articles remain the active Longman route.

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

These measurements are not asking for the rubber dimensions again; those are already in the spec above. They are the vehicle-fit checks needed to prevent a correct rubber part being installed in the wrong station or wrong stack.

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

- Released first-article rubber size is `420 x 38 x 8 mm`.
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
- Square-on bracket photo with ruler/caliper.
- Bolt/stud/retainer feature photo with centre-to-centre measurement.
- Side photo showing mount face, axle strike pad, and current gap.
- Loaded ride-height gap after suspension is fitted.
- Near-full-bump measurement confirming the stop contacts before shocks, tyres, springs, shackles, brake hoses, or metal hard limits.

Record:

| ID | Measurement | Use |
| --- | --- | --- |
| `BL` | Rubber body / fixture landing length | Rubber body outline, mould base, and fixture seat |
| `BW` | Rubber body / fixture landing width | Rubber body width and central fixture/channel clearance |
| `P` | Rubber through-hole and fixture bolt/stud pitch centre-to-centre | Rubber hole pattern plus fixture alignment |
| `D` | Rubber through-hole diameter or stud/bolt thread | Rubber clearance and fixture fastener control |
| `X/Y` | Strike-pad centre offset from rubber-hole/fixture/bracket features | Contact face location |
| `G` | Loaded stop gap | Ride-height clearance |
| `F` | Near-full-bump clearance | Confirms stop acts before hard limits |

## Acceptance

- Longman provides compound family and Shore A target.
- Body/front-support rubber averages Shore A `55-65`.
- Bump-stop rubber averages Shore A `65-75`, or PU `75-85` only if the sample-style through-hole layout, central fixture/channel interface, rebound recovery, and progressive shape are correct.
- Faces on body pads are flat and parallel within `0.5 mm`.
- Holes are clean, not burnt or torn.
- Bump-stop first articles pass 50 percent compression without cracking, retention failure, or permanent collapse; after 30 minutes unloaded, height recovers to at least 90 percent.
- Parts are bagged and labeled by ID and side/station.
