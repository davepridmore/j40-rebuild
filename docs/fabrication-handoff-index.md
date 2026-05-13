# Fabrication Handoff Index

Purpose: one send-out index for the ready-to-run non-rubber fabrication packages in this repository.

All package dimensions are in `mm`. For each package, send the package PDF for human review plus the listed `DXF` files for cutting. Keep the matching `SVG` files with the job if the shop wants a quick visual reference.

Dashboard UI: open the `Fabrication` workstream in `docs/project-control-ui/` for clickable package links, status gates, and first-article steps.

Raw material procurement: use [fabrication-raw-materials-procurement-estimate-20260513.md](fabrication-raw-materials-procurement-estimate-20260513.md) and `data/manual/fabrication_raw_material_estimates.csv`. The matching raw-stock rows have been added to the procurement ledger, including separate tub repair sheet/plate stock so battery/radiator fabrication steel is not consumed by body patches.

## Chassis Rubber Boundary

Chassis/body rubber order control is not owned here. Use [chassis-rubbers-workstream.md](chassis-rubbers-workstream.md) and [longman-rubber-order-spec-20260508.md](longman-rubber-order-spec-20260508.md) for body-mount pads, front-support isolators, bump stops, sleeves, shims, cup washers, and related Longman/first-article release holds.

The old rubber package files remain in the repository as supporting reference material, but the active Fabrication workstream should not send or close chassis-rubber orders independently.

## Battery Stand Power Carrier - Rev A

Directory: [data/manual/fabrication/battery_power_carrier_mount_rev_a](../data/manual/fabrication/battery_power_carrier_mount_rev_a/README.md)

Control spec: [front-engine-bay-mounting-fabrication-plan-20260508.md](front-engine-bay-mounting-fabrication-plan-20260508.md)

Primary files:
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/j40_battery_power_carrier_mount_rev_a_dimension_sheet.pdf`
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_power_carrier_mount_rev_a_assembled_3d_visualisation.html`
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_power_carrier_mount_rev_a_assembled_3d_visualisation.svg`
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_power_carrier_mount_rev_a_3d_visualisation.html`
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_power_carrier_mount_rev_a_3d_visualisation.svg`
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/fabricator_cut_list.csv`
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/inspection_checklist.csv`
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/component_layout.csv`

DXF files:
- `battery_power_carrier_backplane_rev_a.dxf` - steel backplane for known Relay Rev C, MIDI Rev C, and cutoff bases, qty `1`
- `battery_stand_top_tray_rev_a.dxf` - steel battery tray/deck with clamp and cable support fields, qty `1`
- `battery_stand_single_chassis_pickup_rev_a.dxf` - single vehicle-side chassis pickup plate, qty `1`
- `battery_stand_single_mount_upright_rev_a.dxf` - upright bridge side plate, qty `2 mirrored`
- `battery_stand_hold_down_crossbar_rev_a.dxf` - battery hold-down crossbar, qty `1`
- `battery_power_carrier_cutoff_guard_rev_a.dxf` - optional cutoff switch guard, qty `1`

Release position:
- Rev A is a prototype/mock-up release for the new steel chassis-mounted battery stand.
- The stand must mount from the one known chassis pickup plate and upright bridge, not the battery tray skin, radiator support strap, or unsupported inner wing.
- It supports a full-height battery and carries the already-fabricated Relay Rev C carrier base (`320 x 220 mm` face), MIDI Rev C mount plate/subplate (`190 x 150 mm` / `140 x 85 mm`), cutoff base/guard (`150 x 95 mm`), and cable support holes on one removable steel assembly.
- Final metal cutting/drilling still needs the battery-installed cardboard mock-up, the single chassis pickup measurement, cutoff body dimensions, cable lug sweep, bonnet-clearance checks, and steering/radiator/fan clearance checks.

## Front Radiator Two-Side Retention - Rev A

Directory: [data/manual/fabrication/front_radiator_two_side_retention_rev_a](../data/manual/fabrication/front_radiator_two_side_retention_rev_a/README.md)

Control spec: [front-engine-bay-mounting-fabrication-plan-20260508.md](front-engine-bay-mounting-fabrication-plan-20260508.md)

Primary files:
- `data/manual/fabrication/front_radiator_two_side_retention_rev_a/j40_front_radiator_two_side_retention_rev_a_dimension_sheet.pdf`
- `data/manual/fabrication/front_radiator_two_side_retention_rev_a/front_radiator_two_side_retention_rev_a_assembled_3d_visualisation.html`
- `data/manual/fabrication/front_radiator_two_side_retention_rev_a/front_radiator_two_side_retention_rev_a_assembled_3d_visualisation.svg`
- `data/manual/fabrication/front_radiator_two_side_retention_rev_a/front_radiator_two_side_retention_rev_a_3d_visualisation.html`
- `data/manual/fabrication/front_radiator_two_side_retention_rev_a/front_radiator_two_side_retention_rev_a_3d_visualisation.svg`
- `data/manual/fabrication/front_radiator_two_side_retention_rev_a/fabricator_cut_list.csv`
- `data/manual/fabrication/front_radiator_two_side_retention_rev_a/inspection_checklist.csv`

DXF files:
- `front_radiator_saddle_right_angle_post_rev_a.dxf` - 4 mm bolt-through saddle right-angle post, qty `1`

Release position:
- Rev A is a template release for one simple steel post: 90 degree top return with one radiator screw point, plus lower legs that straddle the chassis/front-support section.
- Final bending/drilling remains gated by right-side vehicle dry-fit, transferred left-bracket dimensions, screw size, radiator ear offset, chassis width, through-bolt route, crush-tube/spacer decision, rubber washer/bush stack, and fan clearance.
- The Bracket Analysis Register remains the evidence/action register; this package is the Fabrication handoff for making the bracket templates.

## Suspension Wood Cribbing - Rev A

Directory: [data/manual/fabrication/suspension_wood_cribbing_rev_a](../data/manual/fabrication/suspension_wood_cribbing_rev_a/README.md)

Control spec: [suspension-wood-cribbing-merchant-spec.md](suspension-wood-cribbing-merchant-spec.md)

Primary files:
- `data/manual/fabrication/suspension_wood_cribbing_rev_a/j40_suspension_wood_cribbing_rev_a_dimension_sheet.pdf`
- `data/manual/fabrication/suspension_wood_cribbing_rev_a/suspension_wood_cribbing_rev_a_3d_visualisation.html`
- `data/manual/fabrication/suspension_wood_cribbing_rev_a/suspension_wood_cribbing_rev_a_3d_visualisation.svg`
- `data/manual/fabrication/suspension_wood_cribbing_rev_a/fabricator_cut_list.csv`
- `data/manual/fabrication/suspension_wood_cribbing_rev_a/inspection_checklist.csv`

DXF files:
- `swc_rectangular_cribbing_block_rev_a.dxf` - rectangular hardwood cribbing block, qty `8`
- `swc_wedge_chock_rev_a.dxf` - wedge chock side/top/end profile, qty `4`

Release position:
- Drawing backup for the suspension-owned cribbing buy in [suspension-wood-cribbing-merchant-spec.md](suspension-wood-cribbing-merchant-spec.md).
- Control dimensions are metric: blocks `300 x 150 x 75 mm`; wedges `200 x 100 mm` base with `75 mm` rear height and `25 mm` nose height.
- These are supplemental cribbing/chocks only and must not be treated as substitutes for rated jack stands or axle support.

## Electrical Mounting Packages

### MIDI 5-Way Plate Mount - Rev C

Directory: [data/manual/fabrication/midi5_plate_mount_rev_c](../data/manual/fabrication/midi5_plate_mount_rev_c/README.md)

Primary files:
- `data/manual/fabrication/midi5_plate_mount_rev_c/j40_midi5_plate_mount_rev_c_dimension_sheet.pdf`
- `data/manual/fabrication/midi5_plate_mount_rev_c/midi5_plate_mount_rev_c_3d_visualisation.html`
- `data/manual/fabrication/midi5_plate_mount_rev_c/midi5_plate_mount_rev_c_3d_visualisation.svg`

DXF files:
- `midi5_mount_plate_rev_c.dxf` - `3.0 mm` 5052-H32 aluminium mount plate
- `midi5_holder_subplate_rev_c.dxf` - `5.0 mm` HDPE, ABS, G10, or phenolic holder board

Order definitions:
- Mount plate: `190 x 150 mm` flat plate with six `5.5 mm` subplate standoff holes, four site-fit vehicle mount slots, and five `6.5 mm` cable P-clip holes.
- Holder subplate: `140 x 85 mm` non-conductive board with ten `4.5 mm` holder holes on `20.2 mm` pitch / `44 mm` row separation, plus six `5.5 mm` standoff holes.

Release position: current recommended MIDI holder mount. The external plastic/CNC quote is only for the holder subplate; the aluminium mount plate is owner-made. Use `10-12 mm` spacers between the holder board and mount plate, and add cable support after final routing.

### Relay Mount - Rev C

Directory: [data/manual/fabrication/relay_mount_rev_c](../data/manual/fabrication/relay_mount_rev_c/README.md)

Primary files:
- `data/manual/fabrication/relay_mount_rev_c/j40_relay_mount_rev_c_dimension_sheet.pdf`
- `data/manual/fabrication/relay_mount_rev_c/relay_mount_rev_c_3d_visualisation.html`
- `data/manual/fabrication/relay_mount_rev_c/relay_mount_rev_c_3d_visualisation.svg`

DXF files:
- `relay_carrier_rev_c.dxf` - `3.0 mm` 5052-H32 aluminium relay carrier
- `relay_rear_guard_rev_c.dxf` - `3.0 mm` ABS, HDPE, or polypropylene rear guard

Order definitions:
- Relay carrier: `360 x 255 mm` flat pattern, finished face `320 x 220 mm`, `20 mm` side/bottom returns, `15 mm` top return, six `5.5 mm` guard/standoff holes, slotted relay/vehicle mounts, and lower loom slot.
- Rear guard: `280 x 185 mm` plastic guard with `120 x 25 mm` lower loom/drain opening and six `5.5 mm` standoff holes.

Release position: Relay Rev C defines the already-fabricated relay carrier base used by the current `battery_power_carrier_mount_rev_a` layout. Use the standalone relay-only installation as fallback only if the relay base is deliberately split away from the integrated carrier. Keep the bottom loom opening downward and do not fully seal the rear of the relay box.

### Electrical Modules - Rev A

Directory: [data/manual/fabrication/electrical_modules_rev_a](../data/manual/fabrication/electrical_modules_rev_a/README.md)

Primary files:
- `data/manual/fabrication/electrical_modules_rev_a/j40_electrical_modules_rev_a_dimension_sheet.pdf`
- `data/manual/fabrication/electrical_modules_rev_a/electrical_modules_rev_a_3d_visualisation.html`
- `data/manual/fabrication/electrical_modules_rev_a/electrical_modules_rev_a_3d_visualisation.svg`

DXF files:
- `relay_module_tray_rev_a.dxf` - relay-box shelf
- `power_module_box_rev_a.dxf` - breaker and grouped-MIDI side module
- `power_module_rear_insulator_rev_a.dxf` - non-metal rear shield

Release position: reference/provisional package for the earlier combined module route. For the current route, use `battery_power_carrier_mount_rev_a` for the chassis-mounted integrated carrier and `midi5_plate_mount_rev_c` for the MIDI holder/subplate mounted onto it.

## Electrical Underlay / Insulator Requirements

These are the three non-metal electrical underlays/guards to track separately from owner-made metal plates and brackets:

| Requirement | Package file | Definition | Status |
| --- | --- | --- | --- |
| MIDI holder insulating underlay / subplate | `midi5_plate_mount_rev_c/midi5_holder_subplate_rev_c.dxf` | `140 x 85 x 5.0 mm` HDPE/ABS/G10/phenolic board; ten `4.5 mm` holder holes; six `5.5 mm` standoff holes. | Current external plastic/CNC quote row. |
| Relay rear guard / underlay | `relay_mount_rev_c/relay_rear_guard_rev_c.dxf` | `280 x 185 x 3.0 mm` ABS/HDPE/polypropylene guard with `120 x 25 mm` lower loom/drain opening; six `5.5 mm` standoff holes. | Fallback only with standalone relay Rev C route unless the integrated carrier mock-up proves a separate rear guard is still needed. |
| Power module rear insulator | `electrical_modules_rev_a/power_module_rear_insulator_rev_a.dxf` | `210 x 130 x 3.0 mm` ABS/HDPE/polypropylene shield; two `28 x 8 mm` lower cable slots; six `4.5 mm` mounting holes. | Reference only unless the combined module route is reopened. |

## Superseded Electrical History

The boxed MIDI module packages remain in the repo as history, but should not be sent as the current fabrication route unless that older design is deliberately reopened:
- `data/manual/fabrication/midi5_module_rev_a`
- `data/manual/fabrication/midi5_module_rev_b`

## Shop Instructions

- Confirm material and thickness on the purchase order before cutting.
- Do not treat construction, bend, recess, register, insert, or template layers as through-cuts unless the package README says so.
- Wood cribbing DXFs are dimensional saw-cut/profile references for the timber/workshop package, not vehicle mounting parts.
- Deburr all metal parts and apply corrosion protection after forming.
- Trial-fit first articles before batch production or final loom/body closeout.
