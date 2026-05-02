# Replacement Pipes Workstream

Start here for replacement pipes, hoses, tubes, hard lines, and the made-to-order cooling pipe sample.

Primary tracker: `replacement_pipes` in `data/manual/workstream_status.csv`.

Curated spec matrix: `data/manual/replacement_pipe_ordering_specs.csv`.

Order release matrix: `data/manual/replacement_pipe_order_release_specs.csv`.

Release actions: `data/manual/replacement_pipe_release_actions.csv`.

Circuit closure sheet: `data/manual/replacement_pipe_circuit_closure_sheet.csv`.

Order release handoff: `docs/replacement-pipe-order-release-plan-20260502.md`.

Made-to-order coolant pipe handoff: `docs/pipe-fabrication-spec-20260502.md`.

Latest pipe photo import: Google Photos run `20260502T030647`, file `photos/20260502_005740_gp_Qiat03EQ.jpg`.

Dashboard table: open `Replacement Pipes` in `docs/project-control-ui/index.html`; the UI now shows requirements, order release lines, release actions, and circuit closure with `spec_status`, `acquisition_status`, `installation_status`, and release-hold gates.

## Scope

This workstream is now intentionally narrow. It covers only:

- the place on the vehicle where a pipe/hose/line will be replaced
- the image evidence for that exact pipe/hose/line or location
- the recreation/order spec and the measurements still needed before fabrication or purchase

It excludes body-mount rubbers, window rubbers, grommet assortments, clamp-only rows, general engine cleaning photos, broad chassis status photos, and optional HVAC duct/drain work.

## Curated Pipe Locations

The full editable table is `data/manual/replacement_pipe_ordering_specs.csv`.

Status columns:

- `spec_status`: `spec_ready` for all current requirement rows; the release hold lives in the order/action/closure sheets
- `acquisition_status`: `not_acquired` or `acquired`
- `installation_status`: `not_installed` or `installed`

| ID | Location | Pipe / Line | Photo Status | Spec Status |
| --- | --- | --- | --- | --- |
| `RP-COOL-001` | Front top of engine bay | Upper radiator hose | `20260430_220004_gp_C9oYiYmA` | Toyota `16571-68020`; Dayco `DMH1342` / `CH1342`; measure neck ODs before purchase. |
| `RP-COOL-002` | Front lower engine bay | Lower radiator hose | `20260430_215957_gp_2iBbUagw`, `20260430_220004_gp_C9oYiYmA` | Toyota `16572-68020`; measure lower radiator and engine inlet ODs. |
| `RP-COOL-003` | Radiator overflow route | Overflow / breather hose | close photo needed | Toyota `90445-12078`, `L=600`; match nipple OD and route length. |
| `RP-COOL-004` | Firewall/heater circuit | Heater inlet/outlet hoses | close photo needed | Toyota `99552-30500 L=400` and `99552-30300 L=280`; expected 16 mm / 5/8 in ID but measure. |
| `RP-COOL-005` | Loose May 2 cooling sample | Formed metal coolant/radiator pipe | six May 2 template photos | Recreate from physical sample; match OD, wall, bends, beads, clamp lands, and clocking; pressure-test. |
| `RP-FUEL-001` | Fuel filter/injection pump/injectors | Diesel feed, return, leak-off hoses | `20260430_215957_gp_2iBbUagw` | 8 mm feed, 6 mm return, 3.2-3.5 mm leak-off working basis; diesel-rated hose only. |
| `RP-FUEL-002` | Chassis rail fuel route | Low-pressure fuel hard lines | `20260422_004306_gp_vGlNr2UA`, `20260422_004311_gp_994KQ0Pw` | 8 mm OD feed, 6 mm OD return working basis; match route, ends, clips, and bends. |
| `RP-VAC-001` | Vacuum pump/booster/breather | Vacuum and breather hoses | close photo needed | Reinforced 10-12 mm vacuum working basis; breather 16-19 mm working basis; confirm all barbs. |
| `RP-BRAKE-001` | Frame and axle hydraulic routes | Brake flex and hard lines | close fitting photos needed | Match actual disc/drum fittings, tube OD, flare type, union thread, and droop length. |
| `RP-CLUTCH-001` | Bellhousing/clutch slave route | Clutch flex/hard line | `20260430_215939_gp_EjZ7u1ow` | Match master/slave ports, flare/thread style, hard-line OD, route, and flex length. |

## Acquisition / Fabrication Spec

Use this section as the high-level handoff. For actual order and fabrication release, use `data/manual/replacement_pipe_order_release_specs.csv`. Photo evidence identifies the target location or sample; the old part or installed fittings supply final dimensions.

All rows below are spec-ready with controlled release holds. Do not treat the remaining measurements as missing specification; treat them as the final physical release actions before payment or fabrication.

| ID | Release Type | Acquisition / Fabrication Instruction | Must Measure Before Release | Acceptance Gate |
| --- | --- | --- | --- | --- |
| `RP-COOL-001` | Buy molded hose | Ask for upper radiator hose for Toyota Land Cruiser HJ47 2H: Toyota `16571-68020`, Dayco `DMH1342` / `CH1342`. Buy 1 hose plus correct smooth-band/constant-tension clamps. | Thermostat neck OD, radiator upper neck OD, hose OD for clamps, fan/belt/radiator-support clearance. | Hose follows molded route with no kink/rub; cooling system pressure-test passes. |
| `RP-COOL-002` | Buy molded hose | Ask for lower radiator hose for Toyota Land Cruiser HJ47 2H: Toyota `16572-68020`. Buy 1 hose plus correct clamps. | Radiator lower outlet OD, engine/water-pump inlet OD, bend clearance, hose OD for clamps. | No kink at lower bend; no fan/belt/front-crossmember rub; pressure-test passes. |
| `RP-COOL-003` | Cut-to-fit hose | Ask for EPDM coolant overflow hose equivalent to Toyota `90445-12078`, `L=600`; buy 1 m and cut to route. | Radiator overflow nipple OD, reserve/overflow bottle nipple OD, finished route length. | Hose routes cleanly without kink, pinch, or sharp-edge contact. |
| `RP-COOL-004` | Cut-to-fit heater hose | Ask for EPDM heater hose equivalent to Toyota `99552-30500 L=400` and `99552-30300 L=280`; substitute family `99556`. Expected ID is 16 mm / 5/8 in, but measurement controls. | Engine heater nipple OD, heater-core nipple OD, inlet/outlet route length, rear-heater presence. | No exhaust contact, firewall chafe, or tight bend; leak-free hot run. |
| `RP-COOL-005` | Fabricate from sample | Send the old formed coolant pipe plus the six May 2 photos. Fabricator must copy tube OD, wall, centerline length, bend radii, bend clocking, offsets, beaded ends, clamp lands, and hose overlap. | Tube OD, hose ID, wall thickness, bend centerlines/radii, bead height, clamp land length, clearance to fan/belts/radiator/body. | Bench pressure-test before coating; vehicle dry-fit passes; coat only after fit approval. |
| `RP-FUEL-001` | Buy diesel hose | Ask for diesel-rated hose only: 8 mm ID feed x 3 m, 6 mm ID return/bleed x 2 m, 3.2-3.5 mm injector leak-off x 1 m, plus rolled-edge fuel-injection clamps. | Fuel-filter barbs, injection-pump feed/return barbs, injector leak-off nipples, route lengths, hose OD for clamps. | No seepage, air ingress, belt/exhaust rub, or sharp clamp damage after prime/run. |
| `RP-FUEL-002` | Recreate hard line if needed | If corroded, recreate low-pressure feed/return hard lines: 8 mm OD feed and 6 mm OD return working basis; match original route, end style, and clip points. | Tube OD, full/section length, bend pattern, flare/union style, clip positions, pass-through protection. | Rubber-lined P-clips every `300-400 mm`; no chafe; leak-test after fuel prime. |
| `RP-VAC-001` | Buy hose / OEM if shaped | Ask for reinforced vacuum hose that will not collapse, commonly 10-12 mm ID; if fitted, source 2H vacuum pump oil outlet hose Toyota/OEM `90923-02079`; breather hose must be oil-resistant, commonly 16-19 mm ID. | Vacuum pump barb OD, booster/check-valve OD, check-valve direction, breather spigot OD, route length, heat/chafe exposure. | Brake assist holds vacuum; check valve works; breather hose does not swell/collapse. |
| `RP-BRAKE-001` | Buy/fabricate safety hydraulic lines | Flex hoses must match the current front-disc/rear-drum fittings and full-droop length. Hard lines must match tube OD, flare type, union thread, and original route. | Caliper/wheel-cylinder fitting type, master/proportioning fittings, tube OD, flare standard, union thread, route length, full-droop slack. | Pressure bleed and leak-test; no stretch at full droop; no tire/suspension contact. |
| `RP-CLUTCH-001` | Inspect then replace | Replace clutch flex/hard line if cracked, corroded, swollen, or leaking. Match master/slave ports, flare/thread style, hard-line OD, route, and flex length. | Master/slave port thread, flare style, hard-line OD, route length, flex length, drivetrain movement clearance. | Clutch bleeds cleanly; no leak; no tension through drivetrain movement. |

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

The loose-sample photo is not a fabrication release by itself. It must be sorted against the vehicle location rows above, then each hose/pipe needs a flat-lay photo with a ruler/tape, both ends visible, and any printed hose markings readable.

## Measurement Rules

- Do not fabricate or buy from photos alone where the old part or vehicle fitting can be measured.
- Record every barb OD, nipple OD, tube OD, flare type, thread, bend route, and clamp/hose outside diameter.
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
