# Replacement Pipes Workstream

Start here for replacement pipes, hoses, tubes, hard lines, and the made-to-order cooling pipe sample.

Primary tracker: `replacement_pipes` in `data/manual/workstream_status.csv`.

Curated spec matrix: `data/manual/replacement_pipe_ordering_specs.csv`.

Photo intake checklist: `data/manual/replacement_pipe_photo_intake.csv`.

Order release matrix: `data/manual/replacement_pipe_order_release_specs.csv`.

Release actions: `data/manual/replacement_pipe_release_actions.csv`.

Circuit closure sheet: `data/manual/replacement_pipe_circuit_closure_sheet.csv`.

Order release handoff: `docs/replacement-pipe-order-release-plan-20260502.md`.

Made-to-order coolant pipe handoff: `docs/pipe-fabrication-spec-20260502.md`.

Latest pipe photo import: Google Photos run `20260502T164944`, six loose sample length photos for red/black hose or pipe sorting.

Dashboard table: open `Replacement Pipes` in `docs/project-control-ui/index.html`; the UI now shows requirements, photo intake shots, order release lines, release actions, and circuit closure with `spec_status`, `acquisition_status`, `installation_status`, and release-hold gates.

## Scope

This workstream is now intentionally narrow. It covers only:

- the place on the vehicle where a pipe/hose/line will be replaced
- the image evidence for that exact pipe/hose/line or location
- the recreation/order spec and the measurements still needed before fabrication or purchase

It excludes body-mount rubbers, window rubbers, grommet assortments, clamp-only rows, general engine cleaning photos, broad chassis status photos, and optional HVAC duct/drain work.

## Curated Pipe Locations

The full editable table is `data/manual/replacement_pipe_ordering_specs.csv`.

The import-facing shot list is `data/manual/replacement_pipe_photo_intake.csv`. Each imported pipe/hose photo should be attached there first by `media_id`, then promoted into `replacement_pipe_ordering_specs.csv` or `replacement_pipe_circuit_closure_sheet.csv` once the exact placement and measurement target are confirmed.

Status columns:

- `spec_status`: `spec_ready` for all current requirement rows; the release hold lives in the order/action/closure sheets
- `acquisition_status`: `not_acquired` or `acquired`
- `installation_status`: `not_installed` or `installed`

| ID | Location | Pipe / Line | Photo Status | Spec Status |
| --- | --- | --- | --- | --- |
| `RP-COOL-001` | Front top of engine bay | Upper radiator hose | `20260430_220004_gp_C9oYiYmA` | Spec-led molded EPDM hose; Toyota `16571-68020` / Dayco `DMH1342` / `CH1342` are cross-references only. Record old-hose free length and neck/clamp ODs in `mm`. |
| `RP-COOL-002` | Front lower engine bay | Lower radiator hose | `20260430_215957_gp_2iBbUagw`, `20260430_220004_gp_C9oYiYmA` | Spec-led molded EPDM hose; Toyota `16572-68020` is a cross-reference only. Record old-hose free length and lower radiator/engine inlet ODs in `mm`. |
| `RP-COOL-003` | Radiator overflow route | Overflow / breather hose | close photo needed | Small EPDM overflow hose; `600 mm` OE reference length, `1000 mm` local buy length, cut to measured route and nipple OD. |
| `RP-COOL-004` | Firewall/heater circuit | Heater inlet/outlet hoses | close photo needed | Inlet `400 mm`, outlet `280 mm`; expected `16 mm` / `5/8 in` ID EPDM heater hose but nipple ODs in `mm` control. |
| `RP-COOL-005` | Loose May 2 cooling sample | Formed metal coolant/radiator pipe | six May 2 template photos | `750 mm` minimum tube blank; final centerline length from physical sample. Measure OD, wall, bends, beads, clamp lands, and clocking in `mm`; pressure-test. |
| `RP-FUEL-001` | Fuel filter/injection pump/injectors | Diesel feed, return, leak-off hoses | `20260430_215957_gp_2iBbUagw` | `8 mm ID x 3000 mm` feed, `6 mm ID x 2000 mm` return, `3.2-3.5 mm ID x 1000 mm` leak-off; diesel-rated hose only. |
| `RP-FUEL-002` | Chassis rail fuel route | Low-pressure fuel hard lines | `20260422_004306_gp_vGlNr2UA`, `20260422_004311_gp_994KQ0Pw` | `8 mm OD x 5000 mm` feed allowance and `6 mm OD x 5000 mm` return allowance; final section lengths from route measurement. |
| `RP-VAC-001` | Vacuum pump/booster/breather | Vacuum and breather hoses | close photo needed | Reinforced `10-12 mm ID x 2000 mm` vacuum hose; oil-resistant `16-19 mm ID x 1000 mm` breather hose; confirm all barbs and route lengths in `mm`. |
| `RP-BRAKE-001` | Frame and axle hydraulic routes | Brake flex and hard lines | close fitting photos needed | Hard pipe allowance `4.75 mm / 3/16 in OD x 7600 mm / 25 ft`; match fittings, flare type, union thread, free length, final route length, and droop length in `mm`. |
| `RP-CLUTCH-001` | Bellhousing/clutch slave route | Clutch flex/hard line | `20260430_215939_gp_EjZ7u1ow` | Hard pipe allowance `1500 mm` if replacing; match master/slave ports, flare/thread style, hard-line OD, final route length, and flex length in `mm`. |

## Acquisition / Fabrication Spec

Use this section as the high-level handoff. For actual order and fabrication release, use `data/manual/replacement_pipe_order_release_specs.csv`. Photo evidence identifies the target location or sample; the old part or installed fittings supply final dimensions.

All rows below are spec-ready with controlled release holds. Do not treat the remaining measurements as missing specification; treat them as the final physical release actions before payment or fabrication.

| ID | Release Type | Acquisition / Fabrication Instruction | Must Measure Before Release | Acceptance Gate |
| --- | --- | --- | --- | --- |
| `RP-COOL-001` | Buy molded hose | Ask for a molded EPDM upper radiator hose by route and dimensions: HJ47/2H upper route, thermostat/radiator neck ODs in `mm`, hose OD for clamps in `mm`, old-hose free length in `mm` if available. Toyota `16571-68020` and Dayco `DMH1342` / `CH1342` are cross-references only. | Thermostat neck OD, radiator upper neck OD, old-hose free length, hose OD for clamps, fan/belt/radiator-support clearance. | Hose follows molded route with no kink/rub; cooling system pressure-test passes. |
| `RP-COOL-002` | Buy molded hose | Ask for a molded EPDM lower radiator hose by route and dimensions: HJ47/2H lower route, lower radiator/engine inlet ODs in `mm`, hose OD for clamps in `mm`, old-hose free length in `mm` if available. Toyota `16572-68020` is a cross-reference only. | Radiator lower outlet OD, engine/water-pump inlet OD, old-hose free length, bend clearance, hose OD for clamps. | No kink at lower bend; no fan/belt/front-crossmember rub; pressure-test passes. |
| `RP-COOL-003` | Cut-to-fit hose | Ask for small EPDM coolant overflow hose by size: `600 mm` OE reference length or `1000 mm` local buy length, cut to measured route from radiator neck to reserve bottle. | Radiator overflow nipple OD, reserve/overflow bottle nipple OD, finished route length. | Hose routes cleanly without kink, pinch, or sharp-edge contact. |
| `RP-COOL-004` | Cut-to-fit heater hose | Ask for EPDM heater hose by size: inlet `400 mm`, outlet `280 mm`, expected `16 mm` / `5/8 in` ID unless measured nipple ODs require another size. Toyota `99552` / `99556` numbers are cross-references only. | Engine heater nipple OD, heater-core nipple OD, inlet/outlet route length, rear-heater presence. | No exhaust contact, firewall chafe, or tight bend; leak-free hot run. |
| `RP-COOL-005` | Fabricate from sample | Send the old formed coolant pipe plus the six May 2 photos. Start with `750 mm` minimum tube blank, then trim to the physical sample's measured centerline length. Fabricator must copy tube OD, wall, bend radii, bend clocking, offsets, beaded ends, clamp lands, and hose overlap in `mm`. | Final centerline length, tube OD, hose ID, wall thickness, bend centerlines/radii, bead height, clamp land length, clearance to fan/belts/radiator/body. | Bench pressure-test before coating; vehicle dry-fit passes; coat only after fit approval. |
| `RP-FUEL-001` | Buy diesel hose | Ask for diesel-rated hose only: `8 mm ID x 3000 mm` feed, `6 mm ID x 2000 mm` return/bleed, `3.2-3.5 mm ID x 1000 mm` injector leak-off, plus rolled-edge fuel-injection clamps. | Fuel-filter barbs, injection-pump feed/return barbs, injector leak-off nipples, route lengths, hose OD for clamps. | No seepage, air ingress, belt/exhaust rub, or sharp clamp damage after prime/run. |
| `RP-FUEL-002` | Recreate hard line if needed | If corroded, recreate low-pressure feed/return hard lines: `8 mm OD x 5000 mm` feed allowance and `6 mm OD x 5000 mm` return allowance; cut to measured final section lengths and match original route, end style, and clip points. | Tube OD, full/section length, bend pattern, flare/union style, clip positions, pass-through protection. | Rubber-lined P-clips every `300-400 mm`; no chafe; leak-test after fuel prime. |
| `RP-VAC-001` | Buy hose / OEM if shaped | Ask for reinforced `10-12 mm ID x 2000 mm` vacuum hose and oil-resistant `16-19 mm ID x 1000 mm` breather hose. If the 2H vacuum pump oil outlet hose is fitted, source by fitted shape and mm measurements; Toyota/OEM `90923-02079` is only a reference. | Vacuum pump barb OD, booster/check-valve OD, check-valve direction, breather spigot OD, route length, heat/chafe exposure. | Brake assist holds vacuum; check valve works; breather hose does not swell/collapse. |
| `RP-BRAKE-001` | Buy/fabricate safety hydraulic lines | Flex hoses must match the current front-disc/rear-drum fittings plus free/full-droop length in `mm`. Hard lines must match `4.75 mm / 3/16 in` tube OD; order `7600 mm / 25 ft` coil allowance, then fabricate to measured route lengths, flare type, union thread, and original route. | Caliper/wheel-cylinder fitting type, master/proportioning fittings, tube OD, flare standard, union thread, route length, full-droop slack. | Pressure bleed and leak-test; no stretch at full droop; no tire/suspension contact. |
| `RP-CLUTCH-001` | Inspect then replace | Replace clutch flex/hard line if cracked, corroded, swollen, or leaking. If hard line is replaced, order `1500 mm` blank allowance and cut to measured route. Match master/slave ports, flare/thread style, hard-line OD, and flex length in `mm`. | Master/slave port thread, flare style, hard-line OD, route length, flex length, drivetrain movement clearance. | Clutch bleeds cleanly; no leak; no tension through drivetrain movement. |

## Curated Photos

Made-to-order coolant pipe sample:

- `photos/20260502_004044_gp_Hx4Yo0Qg.jpg`
- `photos/20260502_004106_gp_wlYlUahA.jpg`
- `photos/20260502_004120_gp_7Jw9Zyrg.jpg`
- `photos/20260502_004133_gp_ZEpqmARA.jpg`
- `photos/20260502_004139_gp_jt1dGw4A.jpg`
- `photos/20260502_004145_gp_e8soxsyA.jpg`

Installed pipe locations:

- `photos/20260430_220004_gp_C9oYiYmA.jpg`
- `photos/20260430_215957_gp_2iBbUagw.jpg`
- `photos/20260422_004306_gp_vGlNr2UA.jpg`
- `photos/20260422_004311_gp_994KQ0Pw.jpg`
- `photos/20260430_215939_gp_EjZ7u1ow.jpg`

Loose pipe/hose sample sorting:

- `photos/20260502_005740_gp_Qiat03EQ.jpg`
- `photos/20260502_160754_gp_Zd9UeENg.jpg`
- `photos/20260502_160855_gp_w3sghS8Q.jpg`
- `photos/20260502_160929_gp_exms2QzQ.jpg`
- `photos/20260502_160950_gp_5KW8RnDQ.jpg`
- `photos/20260502_161055_gp_lS8VRrWg.jpg`
- `photos/20260502_161214_gp_zc3zwXlg.jpg`

The loose-sample photos are not a fabrication or purchase release by themselves. They must be sorted against the vehicle location rows above, then each hose/pipe needs ID/OD measurement, both ends visible, and any printed hose markings readable.

## Measurement Rules

- Do not fabricate or buy from photos alone where the old part or vehicle fitting can be measured.
- Record every barb OD, nipple OD, tube OD, flare type, thread, bend route, free length, route length, and clamp/hose outside diameter in `mm`.
- Keep coolant, fuel, brake, clutch, vacuum, and oil/breather material specs separate.
- Do not fabricate high-pressure injector pipes from generic tube.
- Do not use bare copper for fuel or brake hard lines.
- Use rubber-lined P-clips for hard lines every `300-400 mm`.
- Dry-fit and pressure-test fabricated coolant pipes before coating.

## Next Photo Pass

Capture close-ups for:

- radiator overflow nipple and bottle route
- heater core/firewall nipples and engine heater nipples
- vacuum pump, brake booster hose, check valve, and breather route
- brake flex hose ends, hard-line unions, and axle/frame routing
- clutch master/slave fittings and line ends

The current dashboard is limited to the curated photos above; rubber recreation photos stay in the chassis-rubbers workstream.
