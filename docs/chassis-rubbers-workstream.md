# Chassis Rubbers Workstream

Date: 2026-05-08

Purpose: keep the chassis/body rubber order aligned with the current evidence. The current Longman order is custom rubber, with bump-stop rubber now controlled by the May 31 exact front-stop photos. Rear/back stops use the same front-stop shape and fixture pattern, made longer to the `70 mm` family height. Body-mount steel washers, cup/seat washers, crush sleeves, shims, bolts, and captive-thread repairs are inspected or ordered separately because they control the stack but are not custom rubber pieces.

The Chassis Rubbers dashboard section now also carries the complete J40 rubber coverage matrix from [rubber_ordering_specs.csv](../data/manual/rubber_ordering_specs.csv). Treat the Longman pack as the body/chassis custom-rubber subset, and treat the all-rubbers matrix as the guardrail that keeps hoses, grommets, bushes, mounts, weatherstrips, HVAC rubber, seals, plugs, and hangers in their own buy gates.

Current supplier pack:

- [Longman rubber order spec](longman-rubber-order-spec-20260508.md)
- [Longman rubber order CSV](../data/manual/longman_rubber_order_specs.csv)
- [Current order preview](../data/manual/fabrication/rubber_recreation_rev_a/chassis_rubber_current_order_preview_rev_a.svg)
- [Chassis rubber location map](../data/manual/fabrication/rubber_recreation_rev_a/chassis_rubber_location_map_rev_a.svg)
- [Complete chassis rubber SVG preview](../data/manual/fabrication/rubber_recreation_rev_a/chassis_rubber_all_drawings_preview_rev_a.svg)
- [Parametric 3D rubber models](../data/manual/fabrication/rubber_recreation_rev_a/models_3d/README.md)
- [Bump-stop fabrication spec](bump-stop-fabrication-spec-20260504.md)
- [All-rubbers ordering matrix](../data/manual/rubber_ordering_specs.csv)

## Complete J40 Rubber Coverage

Use the all-rubbers matrix before any rubber purchase, even when the immediate work is the body/chassis mount stack. It prevents a body-mount supplier quote from absorbing unrelated items that should be inspected, sample-matched, receipt-checked, or deferred.

| Coverage group | Rows | Current position |
| --- | --- | --- |
| Body/chassis mount and hardware | `RUB-001` to `RUB-002` | Current Chassis Rubbers workstream. `RUB-001` is the Longman custom-rubber pack; `RUB-002` is separate sleeves/cups/shims/hardware. |
| Grommets and pass-through seals | `RUB-003` to `RUB-004`, `RUB-017` | Buy/top-up only by measured firewall/body holes and current inventory; floor/body plugs defer until repair and coating are stable. |
| Powertrain, steering, suspension, and intake rubber | `RUB-005` to `RUB-008`, `RUB-026` to `RUB-027` | Engine mounts are no-active-purchase; gearbox mounts, steering bushes, bump stops, and intake ducting are inspect/sample-match gates; Ironman bushes are receipt-check first. |
| Brake, clutch, fuel, coolant, vacuum, and formed-pipe rubber | `RUB-009` to `RUB-016`, `RUB-028` | Safety/fluids stay in rated-hose gates. Brake hoses must be complete crimped assemblies, fuel hose must be fuel-rated, and coolant/heater hose must be EPDM coolant/heater hose. |
| Exhaust, pedal, HVAC, and duct rubber | `RUB-022` to `RUB-025` | Exhaust hanger/cushion rubber waits for final support geometry; pedal rubber is later; HVAC barrier hose, drain, O-rings, duct, and defrost hose are current HVAC refit items. |
| Body, window, roof, bonnet, and rear-door weatherstrip | `RUB-018` to `RUB-021`, `RUB-029` to `RUB-032` | Deferred until body/window/hardtop/rear-closure fit is known; do not roll these into the Longman chassis mount quote. |

Current count: `32` all-rubber rows across `16` workstream categories. `9` rows are buy/lock-now or receipt-check work, `10` are current-build required, and the remaining rows are inspect-first, conditional, no-active-purchase, or deferred.

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

- Single `80 x 80 x 24` body pad: main tub-to-chassis mount stack, ordered as a generous flat-square batch so any station that proves low can use two stacked pads.
- `FS-OVAL`: separate left/right front support / nose-extension isolators.
- `FS-STRIP-L/R`: left/right underfloor front-support/body-support strip landings.
- `BUMP-60010-LONG`: rear/back long-family axle-to-chassis bump-stop stations, plus any Toyota-controlled front-left long station if confirmed on this vehicle.
- `BUMP-60020-SHORT`: exact front/right-front axle-to-chassis bump-stop station.
- `BODY-LINER-FULL-WIDTH-HOLD` and `EXH-HGR-90917`: hold/reference controls only, excluded from the purchase 3D view.

Main body rubbers stay deliberately simple: the active route is one plain `80 x 80 x 24` square body-pad size. The smaller `22 mm` body-rubber line is removed from the order. The Longman quote now carries `30` flat square pads so there is enough stock for stations that prove they need two stacked pads, not a release for new ribbed or shaped body-rubber variants.

## Three Things To Order

The Longman request should be presented as three supplier-facing order groups, with the part IDs below retained as drawing and first-article controls:

| Order group | What to order | Qty |
| --- | --- | --- |
| 1. Simple `80 x 80` body pads | Single `80 x 80 x 24` body-pad size; smaller `22 mm` pad line removed | `30` body pads |
| 2. Front support / body-support rubbers | `FS-OVAL` plus `38 x 8` strip stock for the left/right underfloor strips | `2` oval pads, `2 m` of strip stock; cut `2 x 420 mm` strips after dry-fit |
| 3. Bump stops | Long rear/back bump stops plus short exact front/right-front stop | `3` long stops and `1` short stop |

## Rubber Order Lines

| ID | Status | Qty | Current spec | Release gate |
| --- | --- | ---: | --- | --- |
| `BM-ISO-LG` | Released for quote / first article as the single active body-pad size | `12 base + 18 stacking/trim spares` | 3D envelope `80 L x 80 W x 24 H mm`; square flat pad; flat parallel faces; plan corners `R1.5`; top/bottom edge break or chamfer `1.0 mm` max; `18.0 mm` through bore; smaller `22 mm` line removed from order; use a second identical pad only where dry-fit proves extra height is needed. | Station mapping, footprint check, sleeve/cup/shim dry-stack, any two-pad station proof, and compression check before final install. |
| `FS-OVAL` | Released for quote / first article | `2` | 3D envelope `96 L x 64 W x 15 T mm`; capsule ends `R32`; outer edge break `0.5-1.0 mm`; two `12 mm` holes at `64 mm` centres; rectangular relief only if old sample confirms it is functional. | Caliper-confirm hole centres, thickness, insert/boss/relief construction before final pair. |
| `FS-STRIP-L` | Released for quote / first article | `1 cut from stock` | Cut `420 L x 38 W x 8 T mm` from a shared `2 m` order of `38 x 8 mm` plain strip stock after dry-fit; plan corners `R1.5`; top/bottom edge break `0.5-1.0 mm`; no through-holes in the rubber by default; Shore A `60 +/-5`. | Dry-fit on the actual landing, allow for a non-perfectly-straight run, then apply only proven end/edge trim; keep spare stock for similar strip landings; reuse or trace the slotted steel retainer separately if needed. |
| `FS-STRIP-R` | Released for quote / first article | `1 cut from stock` | Same `420 L x 38 W x 8 T mm` cut piece from the shared `38 x 8 mm` stock unless the right side proves a handed or non-straight trim. | Same first-article dry-fit and retainer rule as left. |
| `BUMP-60010-LONG` | First article required | `3` | Same May 31 front-stop family: broad rounded/tapered rubber body on a metal backing/fixture with two exposed mounting ears and a flat strike area. Photo-survey nominals are `70 mm` long-family height, `110 mm` metal fixture length, `65 mm` rubber span along the hole axis, and `90 mm` metal mounting-hole pitch. | Treat the photo values as identification and first-fit dimensions to roughly the nearest `5 mm`, not manufacturing tolerances. Directly measure hole diameter, holder thread, fixture width/thickness/channel, vehicle bracket and axle strike-pad `X/Y/G/F`; make one first article before the remaining long stops. |
| `BUMP-60020-SHORT` | First article required | `1` | Exact front/right-front member of the same metal-backed family at the separately controlled `60 +/-1 mm` height; use the provisional `110 mm` fixture length, `65 mm` rubber span and `90 mm` metal-hole pitch only for first-fit screening. | The photographed `~70 mm` worn sample does not release the short height. Confirm the right-front station, hole diameter, holder thread, fixture/channel and full-bump clearance directly before manufacture or installation. |
| `BODY-LINER-FULL-WIDTH-HOLD` | Not captured yet | Hold | Possible long/full-width flat body or panel liner strips. | Do not order until the pieces are found or a vehicle station proves a continuous flat anti-squeak liner is required. |
| `EXH-HGR-90917` | Optional later hold | Hold | Teardrop exhaust hanger cushion from sample or genuine part reference. | Needs intact sample/proper tracing before production. |

## Known vs Candidate Pieces

Known current rubber pieces:

- Main body isolator pads: required, but now specified as square flat custom pads instead of circular/register bushings.
- Two-hole front-support oval pads: required by old sample/photo trail, subject to caliper confirmation.
- Axle bump stops: required if missing/decayed; May 31 front-stop photos control the active shape, and the rear/back stops are the same shape made longer. Height split is externally controlled as `70 mm` long family and `60 mm` front/right-front short family unless vehicle testing says otherwise.
- `FS-STRIP-L/R` flat strip pair: now evidenced by the May 17 loose-part photos plus installed-location photos. Treat these as custom underfloor body-support / anti-squeak strips, not generic body-mount biscuits.
- Rubber definitions must carry the 3D envelope and edge/profile control, not only a flat plan size.

Candidate or unproven pieces:

- Possible longer full-body-width flat pieces are not yet captured as orderable parts. They may be anti-squeak liners, panel-to-panel strips, packing pieces, or body support rubbers, but there is not enough evidence to assign quantity or dimensions.

## Photo Correction

The old strip rows and body-rubber rows had been mixed up with bump-stop evidence. The current split is:

- `20260502_004222_gp_PKRe5HSQ.jpg` and `20260502_004201_gp_zfUSmKJg.jpg` are strip/historical context only and are excluded from the active bump-stop gallery.
- `20260517_194143_gp_CO7MuMdA`, `20260517_194633_gp_rAjY3gjg`, and `20260517_194706_gp_twKRWGFA` are the installed-location proof for the flat strip pair.
- `20260517_193503_gp_N9nHjqXw`, `20260517_193539_gp_E0cR9I0A`, `20260517_193559_gp_NEpk1hpg`, `20260517_193612_gp_JmbfR0Tw`, and `20260517_193616_gp_1ye19BZA` are the loose-part measurement references.
- `20260528_185826_gp_FoyeBPUg` and `20260528_185833_gp_gZBjUjPg` are strip/retainer landing context only. They do not release rubber holes, slots, bonding, handed trim, or bump-stop geometry.
- `20260528_193054_gp_UFyTb44w`, `20260528_193143_gp_Cn3OWzZQ`, and `20260528_193228_gp_PLATNsFQ` are loose body-mount rubber/cup stack context only. They show round/cup fragments with tape, but the photo angles do not reopen the active single `80 x 80 x 24` square pad route.
- `20260528_193200_gp_HICSdovA` and `20260528_193253_gp_f0eQuSFA` are loose rectangular strip/block section context only. They do not release a new length, hole pattern, slot pattern, bonding, or handed trim.
- `20260531_171824_gp_HmSS2ChQ`, `20260531_171859_gp_i6bRyQKA`, `20260531_171903_gp_jNI1gfYA`, and `20260531_171935_gp_BYfhqiWg` are the usable exact front-stop measurement photos. They support provisional photo-survey nominals of `65 mm` molded-rubber span along the mounting-hole axis, `110 mm` metal backing/fixture length, `90 mm` metal mounting-hole pitch, and `70 mm` long-family sample height. These readings are to roughly the nearest `5 mm` and require direct verification before manufacture.
- `20260531_171833_gp_Vw96I7Mg` is an unrelated laptop image and is excluded from bump-stop evidence.
- `20260529_223605_gp_CklgF0cQ` and `20260529_223701_gp_wYPExcAA` are supporting removed-fixture evidence. They confirm the broad rounded body, metal-backed mounting arrangement, and central fixture/channel interface, but the usable May 31 front-stop photos are the active shape master.

## Photo Measurement Audit

Checked on 2026-05-28:

- May 17 loose strip ruler photos show the underfloor strip length at about `16.5 in`, which converts to `419 mm`. The released first-article length is therefore corrected to `420 mm`, with the existing `38 W x 8 T mm` strip section retained.
- The visible elongated slots and rust-stained channel features belong to the steel retainer or witness marks. They are not released as rubber holes; the strip remains plain unless dry-fit proves otherwise.
- May 28 loose body-mount/cup photos were checked against the current body-pad design. They add useful stack context, but no reliable new OD/height dimension replaces the active single `80 x 80 x 24` square first article.
- May 28 loose rectangular rubber close-ups support only the strip/section context. The active strip design remains the plain `420 x 38 x 8 mm` first article with no holes or slots by default.
- May 31 front-stop photos now control the active bump-stop shape. They replace the old strip/photo mix and the prior flat-back-plate-only placeholder. May 29 removed-fixture photos remain supporting construction evidence only. The external height controls remain `70 mm` long-family and `60 mm` front/right-front short until vehicle testing says otherwise.
- May 2 body-pad/cup photos support the current pad thickness range and washer/cup context, but do not prove a round rubber outside profile. The single square `80 x 80 x 24` body pad remains the active Longman route and stays separate from bump-stop evidence.

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
- Rubber bore: `18.0 mm` through for the single `80 x 80 x 24` body pad.
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
- Whether the released square `80 x 80` pad fits, or which exact corners/edges need trimming.

### Front-Support Oval Pads

- Top photo of each old oval pad with ruler.
- Length, width, thickness.
- Hole diameter and hole centre-to-centre.
- Photo/measurement of insert, boss, washer imprint, or relief.
- Confirmation whether the rectangular relief is functional or old deformation.

### Underfloor Body-Support Strip Pair

- Order `2 m` of `38 x 8 mm` strip stock and cut the released `420 x 38 x 8 mm` first articles from that stock after dry-fit because the landing path may not be perfectly straight.
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
| `BL` | Metal fixture overall length (`~110 mm` from the photo survey) | Fixture envelope and bracket landing |
| `BW` | Rubber body / fixture landing width | Rubber body width and central fixture/channel clearance |
| `RB` | Molded-rubber span along the mounting-hole axis (`~65 mm` from the photo survey) | Rubber body identification and mould-envelope screening |
| `P` | Metal fixture-ear mounting-hole pitch centre-to-centre (`~90 mm` from the photo survey) | Fixture alignment; verify directly before drilling or manufacture |
| `D` | Metal fixture-ear hole diameter and internally threaded holder size/pitch | Fastener control; not released by the photographs |
| `X/Y` | Strike-pad centre offset from fixture/bracket features | Contact face location |
| `G` | Loaded stop gap | Ride-height clearance |
| `F` | Near-full-bump clearance | Confirms stop acts before hard limits |

## Acceptance

- Longman provides compound family and Shore A target.
- Body/front-support rubber averages Shore A `55-65`.
- Bump-stop rubber averages Shore A `65-75`, or PU `75-85` only if the May 31 metal-backed fixture-ear mounting layout, central fixture/channel interface, rebound recovery, and progressive shape are correct.
- Faces on body pads are flat and parallel within `0.5 mm`.
- Holes are clean, not burnt or torn.
- Bump-stop first articles pass 50 percent compression without cracking, retention failure, or permanent collapse; after 30 minutes unloaded, height recovers to at least 90 percent.
- Parts are bagged and labeled by ID and side/station.
