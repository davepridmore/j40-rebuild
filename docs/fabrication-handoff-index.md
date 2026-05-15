# Fabrication Handoff Index

Purpose: one send-out index for the ready-to-run non-rubber fabrication packages in this repository.

All package dimensions are in `mm`. For each package, send the package PDF for human review plus the listed `DXF` files for cutting. Keep the matching `SVG` files with the job if the shop wants a quick visual reference.

Dashboard UI: open the `Fabrication` workstream in `docs/project-control-ui/` for clickable package links, status gates, and first-article steps.

Raw material procurement: use [fabrication-raw-materials-procurement-estimate-20260513.md](fabrication-raw-materials-procurement-estimate-20260513.md), [fabrication-metal-stock-list-20260514.md](fabrication-metal-stock-list-20260514.md), and `data/manual/fabrication_raw_material_estimates.csv`. The matching raw-stock rows have been added to the procurement ledger, including the `3.0 mm` and `4.0 mm` pre-formed `90-degree` angle/L-section asks and separate tub repair sheet/plate stock so battery/radiator fabrication steel is not consumed by body patches.

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
- `battery_stand_compact_top_tray_rev_b.dxf` - steel compact `340 x 265 mm` battery tray/deck for a standard `318 x 180 x 230 mm` envelope with clamp, lift-out, and cable support fields, qty `1`
- `battery_stand_compact_single_chassis_pickup_rev_b.dxf` - formed chassis saddle over rail, qty `1`
- `battery_stand_compact_single_mount_upright_rev_b.dxf` - upright bridge side plate, qty `2 mirrored`
- `battery_stand_compact_hold_down_crossbar_rev_b.dxf` - service-removable `340 x 38 mm` battery hold-down crossbar, qty `1`
- `battery_power_compact_front_service_rail_rev_b.dxf` - widened `660 x 310 mm` front/radiator-side access ladder for the rotated outboard relay tray, plastic underlay, relay top power in/out clearances, relay front control-cable clearance, 80 mm wire gutter, MIDI Rev D enclosure shelf tabs, side-by-side MIDI/kill-switch shelf tabs, cutoff-output split clearance, and five-output MIDI cable fanout, qty `1`
- `battery_power_compact_cutoff_tab_rev_b.dxf` - folded 100A breaker/cutoff base/guard, qty `1`

Release position:
- Rev F standard-battery access update is a prototype/mock-up release for the steel chassis-mounted battery stand.
- The stand must mount from the one known formed chassis saddle and upright bridge, not the battery tray skin, radiator support strap, or unsupported inner wing.
- It supports a standard N70/27-class `318 x 180 x 230 mm` battery envelope on a removable hold-down tray and carries the covered relay-box tray field rotated to a `220 x 320 mm` face outside the battery footprint on the outboard/access edge, the relay plastic rear guard/underlay rotated to `185 x 280 mm` ahead of the folded metal tray, MIDI Rev D hinged enclosure (`210 x 165 x 65 mm` body / `230 x 185 mm` lid / `140 x 85 mm` insulating subplate) on a separated top-front shelf, the 100A breaker/cutoff base/guard (`170 x 110 mm` finished face), and cable support holes on one removable steel assembly.
- Battery positive must enter the side-mounted cutoff/kill switch first. The cutoff output then splits into two protected branches: one to the rotated relay top power input and one to the MIDI common feed at fuse 4 / the second-from-last holder. The relay box must keep top power in/out and front control-cable exits clear; the MIDI enclosure must keep five grommeted output holes, with the far-side output hole enlarged for two power cables.
- Final metal cutting/drilling still needs the battery-installed cardboard mock-up, hold-down-removed battery lift-out check, formed saddle rail-width/leg-depth/through-bolt measurement, cutoff body dimensions, battery-to-cutoff and cutoff-output cable-lug sweeps, bonnet-clearance checks, relay cover access, relay top/front exit clearances, MIDI fanout clearance, and steering/radiator/fan clearance checks.

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

### MIDI 5-Way Hinged Enclosure - Rev D

Directory: [data/manual/fabrication/midi5_enclosure_rev_d](../data/manual/fabrication/midi5_enclosure_rev_d/README.md)

Primary files:
- `data/manual/fabrication/midi5_enclosure_rev_d/j40_midi5_enclosure_rev_d_dimension_sheet.pdf`
- `data/manual/fabrication/midi5_enclosure_rev_d/midi5_enclosure_rev_d_3d_visualisation.html`
- `data/manual/fabrication/midi5_enclosure_rev_d/midi5_enclosure_rev_d_3d_visualisation.svg`

DXF files:
- `midi5_enclosure_body_rev_d.dxf` - `3.0 mm` 5052-H32 aluminium folded enclosure body
- `midi5_holder_subplate_rev_d.dxf` - `5.0 mm` HDPE, ABS, G10, or phenolic holder board
- `midi5_enclosure_lid_rev_d.dxf` - `2.0-3.0 mm` aluminium hinged lid

Order definitions:
- Enclosure body: finished floor `210 x 165 mm` with `65 mm` folded side walls, hinge holes on the input/bus side, latch holes on the output side, one `20 mm` input grommet pilot aligned to fuse 4 / the second-from-last holder, and five output-side grommet pilot holes.
- Far-side output hole: enlarged `28 mm` pilot for the output that carries `2` power cables. The other four output holes are `16 mm` pilots. Open every pilot to the final cable/grommet OD after measurement.
- Holder subplate: `140 x 85 mm` non-conductive board with ten `4.5 mm` holder holes on `20.2 mm` pitch / `44 mm` row separation, plus six `5.5 mm` standoff holes.
- Lid: `230 x 185 mm` aluminium cover panel with hinge holes on the input/bus side and latch holes on the output side.

Release position: current recommended MIDI holder route. The external plastic/CNC quote is still only for the holder subplate; the aluminium enclosure body and lid are owner-made or sheet-metal-shop parts. Use `10-12 mm` insulated/sleeved spacers between the holder board and enclosure floor, and fit rubber grommets before wiring.

### Electrical Device Models - Rev A

Directory: [data/manual/fabrication/electrical_device_models_rev_a](../data/manual/fabrication/electrical_device_models_rev_a/README.md)

Primary files:
- `data/manual/fabrication/electrical_device_models_rev_a/electrical_device_models_rev_a_3d_visualisation.html`
- `data/manual/fabrication/electrical_device_models_rev_a/electrical_device_models_rev_a_3d_visualisation.svg`
- `data/manual/fabrication/electrical_device_models_rev_a/device_measurement_basis.csv`

Release position: reference visual model only. This separates the relay/fuse box, 100A waterproof breaker/cutoff, active five-position MIDI holder bank inside the Rev D enclosure, and hidden/security needle switch reference before they are placed into the combined battery-side carrier. Use the current Rev D MIDI enclosure package for MIDI cut files; measure the actual 100A breaker body, mounting-hole centres, terminal-stud spacing, and cable-lug sweep before drilling final metal.

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

Release position: fallback standalone relay-only installation if the relay base is deliberately split away from the integrated carrier. Keep the bottom loom opening downward or side-down and do not fully seal the rear of the relay box.

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

Release position: reference/provisional package for the earlier combined module route. For the current route, use `battery_power_carrier_mount_rev_a` for the chassis-mounted integrated carrier and `midi5_enclosure_rev_d` for the MIDI holder enclosure mounted onto it.

## Electrical Underlay / Insulator Requirements

These non-metal electrical underlays/guards are tracked separately from owner-made metal plates and brackets:

| Requirement | Package file | Definition | Status |
| --- | --- | --- | --- |
| MIDI holder insulating underlay / subplate | `midi5_enclosure_rev_d/midi5_holder_subplate_rev_d.dxf` | `140 x 85 x 5.0 mm` HDPE/ABS/G10/phenolic board; ten `4.5 mm` holder holes; six `5.5 mm` standoff holes. | Current external plastic/CNC quote row. |
| Relay rear guard / underlay | `relay_mount_rev_c/relay_rear_guard_rev_c.dxf` | `280 x 185 x 3.0 mm` ABS/HDPE/polypropylene guard with `120 x 25 mm` lower loom/drain opening; six `5.5 mm` standoff holes. | Fallback only with standalone relay Rev C route unless the integrated carrier mock-up proves a separate rear guard is still needed. |
| Power module rear insulator | `electrical_modules_rev_a/power_module_rear_insulator_rev_a.dxf` | `210 x 130 x 3.0 mm` ABS/HDPE/polypropylene shield; two `28 x 8 mm` lower cable slots; six `4.5 mm` mounting holes. | Reference only unless the combined module route is reopened. |

## Superseded Electrical History

The older MIDI module packages remain in the repo as history, but should not be sent as the current fabrication route unless that older design is deliberately reopened:
- `data/manual/fabrication/midi5_module_rev_a`
- `data/manual/fabrication/midi5_module_rev_b`
- `data/manual/fabrication/midi5_plate_mount_rev_c`

## Shop Instructions

- Confirm material and thickness on the purchase order before cutting.
- Do not treat construction, bend, recess, register, insert, or template layers as through-cuts unless the package README says so.
- Wood cribbing DXFs are dimensional saw-cut/profile references for the timber/workshop package, not vehicle mounting parts.
- Deburr all metal parts and apply corrosion protection after forming.
- Trial-fit first articles before batch production or final loom/body closeout.
