# Replacement Pipe Order Release Plan - 2026-05-02

This is the order/fabrication release layer for the Replacement Pipes workstream.

Primary data files:

- `data/manual/replacement_pipe_ordering_specs.csv`
- `data/manual/replacement_pipe_order_release_specs.csv`
- `data/manual/replacement_pipe_release_actions.csv`
- `data/manual/replacement_pipe_circuit_closure_sheet.csv`

Dashboard location: `docs/project-control-ui/index.html` -> `Replacement Pipes`.

## Release State

All ten replacement-pipe requirement rows are now `spec_ready`.

That does not mean every item should be ordered immediately. It means the exact order/fabrication basis is defined, and the remaining work is a controlled release hold: final measurements, close-up photos, or circuit verification before payment/fabrication.

## Spec-Ready Order Lines

| Group | Order Lines | Status |
| --- | --- | --- |
| Radiator hoses | `RPO-COOL-001`, `RPO-COOL-002` | Molded hose part numbers ready; measure radiator/engine neck ODs before payment. |
| Overflow hose | `RPO-COOL-003` | Toyota length basis ready; close photo and nipple OD measurements still required. |
| Heater hoses | `RPO-COOL-004A`, `RPO-COOL-004B` | Toyota length basis ready; expected 16 mm / 5/8 in ID but nipple measurement controls. |
| Formed coolant pipe | `RPO-COOL-005` | Fabrication basis ready; physical template measurement is the release hold. |
| Diesel rubber hoses | `RPO-FUEL-001A`, `RPO-FUEL-001B`, `RPO-FUEL-001C` | 8 mm feed x3 m, 6 mm return x2 m, 3.2-3.5 mm leak-off x1 m; measure barbs before purchase. |
| Fuel hard lines | `RPO-FUEL-002A`, `RPO-FUEL-002B` | 8 mm feed and 6 mm return working basis; replace only corroded/weak sections after inspection. |
| Vacuum/breather | `RPO-VAC-001A`, `RPO-VAC-001B`, `RPO-VAC-001C` | Working hose sizes ready; close photos and fitted-hose confirmation required. |
| Brake hydraulics | `RPO-BRAKE-001A`, `RPO-BRAKE-001B` | Safety-line basis ready; fitting/flare/thread confirmation is mandatory before order/fabrication. |
| Clutch hydraulics | `RPO-CLUTCH-001A`, `RPO-CLUTCH-001B` | Inspect-first replacement basis ready; port/fitting measurements required if replacing. |
| Supports | `RPO-CLIP-001` | Rubber-lined P-clips and pass-through protection ready; size to measured line OD. |

## Active Procurement Holds

The active buy-now parts below are now marked `spec_ready` with `spec_ready_release_hold`:

- `part_mech_radiator_hose_set`
- `part_mech_heater_hose_set`
- `part_mech_fuel_hose_and_clamps`
- `part_mech_vacuum_hose_refresh`
- `part_mech_brake_flex_hose_set`

Next action for all five: `complete_replacement_pipe_release_actions_then_order`.

## Workshop Measurement Sequence

1. Photograph and label every route before removal.
2. Measure coolant/heater/overflow/fuel/vacuum/breather barbs and nipples with calipers.
3. Flat-lay the formed metal coolant pipe and record tube OD, wall, centerline lengths, bend radii, clocking, beads, and clamp lands.
4. Read markings on loose hose samples and assign each sample to the correct circuit.
5. Inspect hard fuel lines under clips and decide keep, section repair, or full replacement.
6. Photograph brake fittings, unions, banjos, flare nuts, brackets, and full-droop hose slack.
7. Confirm brake tube OD, flare standard, fitting thread, and old-line bend templates before fabrication.
8. Confirm clutch fitting thread/flare, flex length, hard-line OD, and movement clearance if replacing.
9. Confirm vacuum pump, booster, check valve, breather routing, and oil exposure.
10. Dry-fit and test each circuit before closing the workstream.

## Hard Rules

- Do not fabricate high-pressure injector pipes from generic tube.
- Do not use bare copper for fuel or brake hard lines.
- Do not buy brake hydraulic parts until fitting, thread, flare, and full-droop checks are recorded.
- Do not coat the fabricated coolant pipe until it has passed bench pressure test and vehicle dry-fit.
- Use rubber-lined P-clips for permanent hard-line support, with spacing around 300-400 mm.
