# Replacement Pipe Order Release Plan - 2026-05-02

This is the order/fabrication release layer for the Replacement Pipes workstream.

Primary data files:

- `data/manual/replacement_pipe_ordering_specs.csv`
- `data/manual/replacement_pipe_order_release_specs.csv`
- `data/manual/replacement_pipe_release_actions.csv`
- `data/manual/replacement_pipe_circuit_closure_sheet.csv`

Dashboard location: `docs/project-control-ui/index.html` -> `Replacement Pipes`.

## Release State

All replacement-pipe requirement rows are now defined, including the connector-hose row added after the rubber visual audit on 2026-05-03.

The standard coolant/heater/fuel/vacuum/breather hose rows are now local-market order-ready with explicit buy lengths. Remaining controls are install/safety controls: molded-hose sample match, final trim from released stock, formed-pipe dry-fit/pressure test, fuel prime leak test, brake/clutch hydraulic fitting match, bleed/pressure test, and final chafe checks.

## Spec-Ready Order Lines

| Group | Order Lines | Status |
| --- | --- | --- |
| Radiator hoses | `RPO-COOL-001`, `RPO-COOL-002` | Molded hose order ready; Toyota/Dayco numbers are cross-references only. Sample-match and dry-fit on receipt. |
| Overflow hose | `RPO-COOL-003` | Buy `1000 mm` local EPDM hose and cut to route. |
| Heater hoses | `RPO-COOL-004A`, `RPO-COOL-004B` | Buy `1000 mm` of `16 mm / 5/8 in` EPDM heater hose stock; cut `400 mm` inlet and `280 mm` outlet from that stock during install. |
| Formed coolant pipe | `RPO-COOL-005` | Order one `28-30 mm OD`, `1.2-1.6 mm` wall tube blank; buy/quote `1000 mm` shop stock if sold by meter, with `750 mm` as the absolute minimum blank before bending/trimming. Beads `1.5-2.0 mm`; clamp lands `25-30 mm`. |
| Formed pipe connector hoses | `RPO-COOL-006A`, `RPO-COOL-006B` | Buy two `500 mm` EPDM connector blanks on `28-30 mm` ID exact order basis; cut by sample and dry-fit. |
| Diesel rubber hoses | `RPO-FUEL-001A`, `RPO-FUEL-001B`, `RPO-FUEL-001C` | Buy `8 mm ID x 3000 mm` feed, `6 mm ID x 2000 mm` return, and `3.2-3.5 mm ID x 1000 mm` leak-off diesel-rated stock. |
| Fuel hard lines | `RPO-FUEL-002A`, `RPO-FUEL-002B` | `8 mm OD x 5000 mm` feed pipe allowance and `6 mm OD x 5000 mm` return pipe allowance; final section lengths only after corrosion inspection and route measurement. |
| Vacuum/breather | `RPO-VAC-001A`, `RPO-VAC-001B`, `RPO-VAC-001C` | Buy `10-12 mm ID x 2000 mm` reinforced vacuum hose and `16-19 mm ID x 1000 mm` oil-resistant breather hose; oil-outlet molded hose is conditional on fitted presence. |
| Brake hydraulics | `RPO-BRAKE-001A`, `RPO-BRAKE-001B` | Quote `3` complete brake flex assemblies copied from old samples/current fittings; hard-line stock is `4.75 mm / 3/16 in x 7600 mm / 25 ft` brake tube coil allowance. |
| Clutch hydraulics | `RPO-CLUTCH-001A`, `RPO-CLUTCH-001B` | New replacement basis ready; quote `1` complete clutch flex assembly and `1500 mm` brake/clutch-rated hard-line blank for the replacement line. |
| Supports | `RPO-CLIP-001` | Rubber-lined P-clips and pass-through protection ready; size to `4.75 mm`, `6 mm`, and `8 mm` measured line ODs with `300-400 mm` support spacing. |

## Active Procurement Position

The active hose/rubber parts below are now marked purchase-ready / local-market-order-ready:

- `part_mech_radiator_hose_set`
- `part_mech_heater_hose_set`
- `part_mech_fuel_hose_and_clamps`
- `part_mech_vacuum_hose_refresh`

`part_mech_brake_flex_hose_set` is quote-ready as complete hydraulic assemblies and brake tube stock, but remains safety-held for fitting match, bleed, pressure test, and clearance.

## Workshop Measurement Sequence

1. Photograph and label every route before removal.
2. Buy the released coolant/heater/overflow/fuel/vacuum/breather stock lengths, then final-trim and choose clamps during dry-fit.
3. Flat-lay the formed metal coolant pipe and record tube OD, wall, final centerline length, bend radii, clocking, beads, and clamp lands in `mm`; the orderable stock is `28-30 mm OD`, `1.2-1.6 mm` wall, `1000 mm` shop stock preferred or `750 mm` absolute minimum blank.
4. Keep both formed-pipe rubber connector hoses with the sample; measure each connector ID/OD, free/cut length, overlap, pipe-end OD/bead, mating spigot OD, clamp OD, and bend/kink clearance in `mm`.
5. Read markings on loose hose samples for sorting/reference only; this no longer blocks the standard stock order.
6. Inspect hard fuel lines under clips and decide keep, section repair, or full replacement; order allowances are `5000 mm` feed and `5000 mm` return, with final section lengths and clip spacing recorded in `mm`.
7. Photograph brake fittings, unions, banjos, flare nuts, brackets, free hose length, and route clearance in `mm`.
8. Confirm brake tube OD, flare standard, fitting thread, individual route lengths, and old-line bend templates before fabrication; default order allowance is `7600 mm / 25 ft`.
9. Confirm clutch fitting thread/flare, flex length in `mm`, hard-line OD, final route length in `mm`, and movement clearance if replacing; hard-line blank allowance is `1500 mm`.
10. Confirm 2H vacuum pump oil outlet fitted presence before buying that molded hose; standard vacuum/breather stock is already released.
11. Dry-fit and test each circuit before closing the workstream.

## Hard Rules

- Do not fabricate high-pressure injector pipes from generic tube.
- Do not use bare copper for fuel or brake hard lines.
- Do not buy generic brake or clutch hose; flex hoses must be complete crimped hydraulic assemblies copied from old samples or matched to fitted vehicle hardware.
- Do not coat the fabricated coolant pipe until it has passed bench pressure test and vehicle dry-fit.
- Do not reuse old rubber connector hoses on the fabricated coolant pipe. Old couplers are trim/sample references only; final connectors are new `RPO-COOL-006A/B` parts.
- Use rubber-lined P-clips for permanent hard-line support, with spacing around 300-400 mm.
