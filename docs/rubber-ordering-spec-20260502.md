# Rubber Ordering Spec - 2026-05-02

Purpose: consolidate every rubber-related row into one orderable matrix so chassis, safety, powertrain, suspension, body sealing, and HVAC rubbers are not bought twice or bought before their measurements are known.

Primary order matrix: [rubber_ordering_specs.csv](../data/manual/rubber_ordering_specs.csv).

Related source lists:
- [rubbers_exact_online.csv](../data/manual/workbook_tabs/rubbers_exact_online.csv)
- [rubbers_kit_buy.csv](../data/manual/workbook_tabs/rubbers_kit_buy.csv)
- [chassis_rubber_requirements.csv](../data/manual/chassis_rubber_requirements.csv)
- [rubber-recreation-fabrication-spec-20260502.md](rubber-recreation-fabrication-spec-20260502.md)
- [body_mount_order_release_specs.csv](../data/manual/body_mount_order_release_specs.csv)
- [body_mount_release_actions.csv](../data/manual/body_mount_release_actions.csv)
- [body_mount_station_closure_sheet.csv](../data/manual/body_mount_station_closure_sheet.csv)

## Ordering Position

Use `data/manual/rubber_ordering_specs.csv` as the current source of truth for ordering. The older workbook tabs remain source evidence and budget/procurement context, but the order matrix controls the next action and pre-order gates.

## Buy Or Lock Now

| Order ID | Item | Action | Gate |
| --- | --- | --- | --- |
| `RUB-001` | Body-to-chassis mount rubber package | Quote/prototype now; final fabricate/buy only after caliper closure | Resolve small-mount one-piece vs split-stack construction and map every station |
| `RUB-002` | Body mount sleeves, cups, shims, and hardware | Prepare local steel/fastener order | Confirm thread pitch, bolt length, sleeve length, cup geometry, and original shim positions |
| `RUB-003` | Firewall/column/wiper/rear wiring grommet top-up | Audit existing grommet kit, then top up by measured hole sizes | Do not buy another bulk kit until existing inventory is matched |
| `RUB-009` | Brake flexible hose set | Buy new safety assemblies | Confirm end fittings and hose length with Ironman lift/droop clearance in mind |
| `RUB-011` | Fuel feed/return/vent hoses and clamps | Buy new fuel-rated hose and clamps | Measure ID/lengths; do not substitute coolant, vacuum, or generic hose |

## Inspect Before Buying

| Order ID | Item | Action | Gate |
| --- | --- | --- | --- |
| `RUB-004` | Steering column firewall boot/seal | Buy or fabricate only if current seal fails | Trial-fit column/firewall first |
| `RUB-005` | Engine mounts | Inspect under load, then buy diesel-compatible mounts by bracket pattern | Reject gasoline-only listings unless physically identical |
| `RUB-006` | Gearbox/transfer mounts and top-cover rubbers | Inspect after degreasing, then sample-match | Confirm transmission/transfer combination |
| `RUB-007` | Leaf spring eye and shackle bushes | Do not order separately yet | Count Ironman kit contents first |
| `RUB-008` | Steering bushings | Buy only if measurable play/cracking remains | Diagnose play source first |
| `RUB-010` | Clutch flex hose | Buy if aged, cracked, leaking, or unknown | Match hydraulic end fittings and length |
| `RUB-012` | Tank strap pads, sender seal, tank rubbers | Buy if tank is dropped or rubbers fail | Measure sender flange, strap width, and filler/vent sizes |
| `RUB-013` to `RUB-016` | Heater/coolant/reservoir/vacuum hoses | Buy by condition, routing, and diameter | Confirm engine, radiator, heater, and vacuum routing |
| `RUB-022` | Exhaust hanger rubbers | Buy by dimension if failed | Measure pin diameter and hole spacing |
| `RUB-026` | Bump stops | Inspect during Ironman work | Confirm loaded ride height and axle travel |

## Defer Until Body Or HVAC Stage

| Order ID | Item | Reason To Defer |
| --- | --- | --- |
| `RUB-017` | Floor plugs/drain plugs/body hole plugs | Holes may change during body repair and coating |
| `RUB-018` | Door weatherstrip set | Door gaps, repaired apertures, and paint stage control fit |
| `RUB-019` | Windscreen rubber/base seal | Glass/frame condition and seal profile must be known |
| `RUB-020` | Vent/flap/cowl seals | Variant risk is high before body hardware mock-up |
| `RUB-021` | Window rubbers/channels/sliding-window seals | Requires window hardware and glass audit |
| `RUB-023` | Pedal rubbers | Low urgency; confirm pedal plate profile later |
| `RUB-024` | A/C barrier hoses, drain hoses, O-rings | Final hose lengths depend on HVAC layout |
| `RUB-025` | HVAC duct/defrost hoses | Dash, heater box, and vent locations must be fixed |

## Non-Negotiable Material Rules

- Brake hoses must be complete crimped hydraulic brake hose assemblies, `DOT/SAE J1401` or OEM-equivalent. Do not fabricate from generic rubber hose.
- Fuel hoses must be diesel/fuel rated. Use `SAE J30 R9` where possible for feed/pressure exposure; use lower-pressure hose only where the circuit is confirmed low-pressure return/vent.
- Coolant and heater hoses must be EPDM coolant/heater hose, not fuel, vacuum, washer, or generic water hose.
- A/C O-rings must be refrigerant-compatible, normally HNBR for an `R134a` system.
- Body mount rubber must be one matched automotive mount-grade batch. Do not mix old/new, rubber/polyurethane, or different hardnesses side to side.
- Do not order separate leaf spring or shackle bushes until the Ironman kit is physically counted.

## Measurement Pack To Take To Supplier

For each rubber order, take:
1. The old sample if available.
2. A photo of its vehicle position.
3. Measured OD/ID/height/length/hole spacing as applicable.
4. Material requirement from `rubber_ordering_specs.csv`.
5. Quantity and required side/station labels.

For body mounts specifically, take the fabrication sheet and closure table:
- [body_mount_order_release_specs.csv](../data/manual/body_mount_order_release_specs.csv)
- [body_mount_release_actions.csv](../data/manual/body_mount_release_actions.csv)
- [body_mount_station_closure_sheet.csv](../data/manual/body_mount_station_closure_sheet.csv)
- [rubber_recreation_fabrication_specs.csv](../data/manual/rubber_recreation_fabrication_specs.csv)
- [rubber_recreation_measurement_closure.csv](../data/manual/rubber_recreation_measurement_closure.csv)
- [rubber_recreation_toyota_oe_cross_reference.csv](../data/manual/rubber_recreation_toyota_oe_cross_reference.csv)

## Source Controls Already Checked

- Toyota GR Heritage Parts programme for Land Cruiser 40: confirms official heritage support, but no open body-mount rubber dimensions were found.
- Toyota EPC-style cab/body mounting listings: useful for station labels, part numbers, bolt families, and shim/spacer references, but not rubber OD/ID/free-height.
- Energy Suspension `8.4104`/`8.18105` data: useful aftermarket thickness sanity check only; it is not a Toyota rubber specification and must not override physical sample measurement.
