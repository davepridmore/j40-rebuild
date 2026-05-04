# Fabrication Handoff Index

Purpose: one send-out index for the ready-to-run fabrication packages in this repository.

All package dimensions are in `mm`. For each package, send the package PDF for human review plus the listed `DXF` files for cutting. Keep the matching `SVG` files with the job if the shop wants a quick visual reference.

Dashboard UI: open the `Fabrication` workstream in `docs/project-control-ui/` for clickable package links, status gates, and first-article steps.

## Rubber Recreation - Rev A

Directory: [data/manual/fabrication/rubber_recreation_rev_a](../data/manual/fabrication/rubber_recreation_rev_a/README.md)

Control spec: [rubber-recreation-fabrication-spec-20260502.md](rubber-recreation-fabrication-spec-20260502.md)

Primary files:
- `data/manual/fabrication/rubber_recreation_rev_a/j40_rubber_recreation_rev_a_dimension_sheet.pdf`
- `data/manual/fabrication/rubber_recreation_rev_a/fabricator_cut_list.csv`
- `data/manual/fabrication/rubber_recreation_rev_a/inspection_checklist.csv`

DXF files:
- `bm_sm_body_mount_cushion_rev_a.dxf` - small circular body-mount cushion, qty `10`
- `bm_lg_body_mount_cushion_rev_a.dxf` - large circular body-mount cushion, qty `2`
- `bm_cup_small_seat_washer_rev_a.dxf` - small body-mount cup washer blank, qty `10` working basis
- `bm_cup_large_seat_washer_rev_a.dxf` - large body-mount cup washer blank, qty `2` working basis
- `fs_oval_front_support_pad_rev_a.dxf` - two-hole oval front-support isolator pad, qty `2`
- `fs_strip_left_template_blank_rev_a.dxf` - left strip quote/template blank, qty `1`
- `fs_strip_right_template_blank_rev_a.dxf` - right strip quote/template blank, qty `1`

Release position:
- Circular cushions, cup blanks, and the oval pad are ready for quote and first article.
- Final batch production still waits for the hold fields in `data/manual/rubber_recreation_measurement_closure.csv`.
- Strip files are stock-envelope/template blanks only. Trace the physical left/right strip rubbers and metal carriers before production cutting.

## Suspension Wood Cribbing - Rev A

Directory: [data/manual/fabrication/suspension_wood_cribbing_rev_a](../data/manual/fabrication/suspension_wood_cribbing_rev_a/README.md)

Control spec: [suspension-wood-cribbing-merchant-spec.md](suspension-wood-cribbing-merchant-spec.md)

Primary files:
- `data/manual/fabrication/suspension_wood_cribbing_rev_a/j40_suspension_wood_cribbing_rev_a_dimension_sheet.pdf`
- `data/manual/fabrication/suspension_wood_cribbing_rev_a/fabricator_cut_list.csv`
- `data/manual/fabrication/suspension_wood_cribbing_rev_a/inspection_checklist.csv`

DXF files:
- `swc_rectangular_cribbing_block_rev_a.dxf` - rectangular hardwood cribbing block, qty `8`
- `swc_wedge_chock_rev_a.dxf` - wedge chock side/top/end profile, qty `4`

Release position:
- Drawing backup for the local-market timber buy in [local-market-procurement-workstream.md](local-market-procurement-workstream.md).
- Control dimensions are metric: blocks `300 x 150 x 75 mm`; wedges `200 x 100 mm` base with `75 mm` rear height and `25 mm` nose height.
- These are supplemental cribbing/chocks only and must not be treated as substitutes for rated jack stands or axle support.

## Electrical Mounting Packages

### MIDI 5-Way Plate Mount - Rev C

Directory: [data/manual/fabrication/midi5_plate_mount_rev_c](../data/manual/fabrication/midi5_plate_mount_rev_c/README.md)

Primary PDF:
- `data/manual/fabrication/midi5_plate_mount_rev_c/j40_midi5_plate_mount_rev_c_dimension_sheet.pdf`

DXF files:
- `midi5_mount_plate_rev_c.dxf` - `3.0 mm` 5052-H32 aluminium mount plate
- `midi5_holder_subplate_rev_c.dxf` - `5.0 mm` HDPE, ABS, G10, or phenolic holder board

Release position: current recommended MIDI holder mount. Use `10-12 mm` spacers between the holder board and mount plate, and add cable support after final routing.

### Relay Mount - Rev C

Directory: [data/manual/fabrication/relay_mount_rev_c](../data/manual/fabrication/relay_mount_rev_c/README.md)

Primary PDF:
- `data/manual/fabrication/relay_mount_rev_c/j40_relay_mount_rev_c_dimension_sheet.pdf`

DXF files:
- `relay_carrier_rev_c.dxf` - `3.0 mm` 5052-H32 aluminium relay carrier
- `relay_rear_guard_rev_c.dxf` - `3.0 mm` ABS, HDPE, or polypropylene rear guard

Release position: current recommended support for the DAIER prewired 10-way relay/fuse box. Keep the bottom loom opening downward and do not fully seal the rear of the relay box.

### Electrical Modules - Rev A

Directory: [data/manual/fabrication/electrical_modules_rev_a](../data/manual/fabrication/electrical_modules_rev_a/README.md)

Primary PDF:
- `data/manual/fabrication/electrical_modules_rev_a/j40_electrical_modules_rev_a_dimension_sheet.pdf`

DXF files:
- `relay_module_tray_rev_a.dxf` - relay-box shelf
- `power_module_box_rev_a.dxf` - breaker and grouped-MIDI side module
- `power_module_rear_insulator_rev_a.dxf` - non-metal rear shield

Release position: reference/provisional package for the earlier combined module route. For the current split route, use `midi5_plate_mount_rev_c` and `relay_mount_rev_c`.

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
