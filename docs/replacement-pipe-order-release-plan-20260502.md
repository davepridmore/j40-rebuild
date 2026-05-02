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
| Radiator hoses | `RPO-COOL-001`, `RPO-COOL-002` | Spec-led molded hose order ready; Toyota/Dayco numbers are cross-references only. Record old-hose free length in `mm` if available and measure neck/clamp ODs in `mm` before payment. |
| Overflow hose | `RPO-COOL-003` | `600 mm` OE reference length; buy `1000 mm` local EPDM hose and cut to measured route after nipple OD measurements. |
| Heater hoses | `RPO-COOL-004A`, `RPO-COOL-004B` | `400 mm` inlet and `280 mm` outlet cut lengths; expected `16 mm` / `5/8 in` ID but nipple measurement controls. |
| Formed coolant pipe | `RPO-COOL-005` | `750 mm` minimum tube blank for ordering/fabrication; final centerline length comes from the physical template. Visible planning envelope roughly `400 mm` height and `250-300 mm` offset. |
| Diesel rubber hoses | `RPO-FUEL-001A`, `RPO-FUEL-001B`, `RPO-FUEL-001C` | `8 mm ID x 3000 mm` feed, `6 mm ID x 2000 mm` return, `3.2-3.5 mm ID x 1000 mm` leak-off; measure barbs before purchase. |
| Fuel hard lines | `RPO-FUEL-002A`, `RPO-FUEL-002B` | `8 mm OD x 5000 mm` feed pipe allowance and `6 mm OD x 5000 mm` return pipe allowance; final section lengths only after corrosion inspection and route measurement. |
| Vacuum/breather | `RPO-VAC-001A`, `RPO-VAC-001B`, `RPO-VAC-001C` | `10-12 mm ID x 2000 mm` vacuum hose and `16-19 mm ID x 1000 mm` breather hose; oil-outlet molded hose needs fitted confirmation and mm measurements if sourced locally. |
| Brake hydraulics | `RPO-BRAKE-001A`, `RPO-BRAKE-001B` | Brake flex hoses need free/full-droop length in `mm`; hard lines use `4.75 mm / 3/16 in` tube with `7600 mm / 25 ft` coil allowance, then measured individual route lengths, flare, and thread before fabrication. |
| Clutch hydraulics | `RPO-CLUTCH-001A`, `RPO-CLUTCH-001B` | Inspect-first replacement basis ready; clutch hard pipe allowance is `1500 mm` if replacing. Record flex length, hard-line OD, final route length, port thread, and flare/seat in `mm`. |
| Supports | `RPO-CLIP-001` | Rubber-lined P-clips and pass-through protection ready; size to `4.75 mm`, `6 mm`, and `8 mm` measured line ODs with `300-400 mm` support spacing. |

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
2. Measure coolant/heater/overflow/fuel/vacuum/breather barbs and nipples with calipers in `mm`; record route length and old-hose free length where available.
3. Flat-lay the formed metal coolant pipe and record tube OD, wall, final centerline length, bend radii, clocking, beads, and clamp lands in `mm`; the orderable blank allowance is `750 mm`.
4. Read markings on loose hose samples and assign each sample to the correct circuit.
5. Inspect hard fuel lines under clips and decide keep, section repair, or full replacement; order allowances are `5000 mm` feed and `5000 mm` return, with final section lengths and clip spacing recorded in `mm`.
6. Photograph brake fittings, unions, banjos, flare nuts, brackets, free hose length, and full-droop hose slack in `mm`.
7. Confirm brake tube OD, flare standard, fitting thread, individual route lengths, and old-line bend templates before fabrication; default order allowance is `7600 mm / 25 ft`.
8. Confirm clutch fitting thread/flare, flex length in `mm`, hard-line OD, final route length in `mm`, and movement clearance if replacing; hard-line blank allowance is `1500 mm`.
9. Confirm vacuum pump, booster, check valve, breather routing, and oil exposure.
10. Dry-fit and test each circuit before closing the workstream.

## Hard Rules

- Do not fabricate high-pressure injector pipes from generic tube.
- Do not use bare copper for fuel or brake hard lines.
- Do not buy brake hydraulic parts until fitting, thread, flare, and full-droop checks are recorded.
- Do not coat the fabricated coolant pipe until it has passed bench pressure test and vehicle dry-fit.
- Use rubber-lined P-clips for permanent hard-line support, with spacing around 300-400 mm.
