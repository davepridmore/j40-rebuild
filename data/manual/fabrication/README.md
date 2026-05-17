# J40 Fabrication Output Index

This directory contains the repo-native fabrication packages that can be sent to a local fabricator or used for first-article review.

All dimensional packages use millimetres. Send the `DXF` files for CAD/CAM cutting, the `SVG` files for quick visual review where present, the package PDF for non-CAD review, and the `*_3d_visualisation.html` files when a browser-based assembly read is useful.

## Current Release Packages

| Package | Workstream | Status | Primary PDF | Notes |
| --- | --- | --- | --- | --- |
| `rubber_recreation_rev_a` | Chassis rubbers | Quote and first article ready; final production has measurement holds | `rubber_recreation_rev_a/j40_rubber_recreation_rev_a_dimension_sheet.pdf` | Body-mount cushions, cup washer blanks, oval front-support pad, and strip quote/template blanks. |
| `suspension_wood_cribbing_rev_a` | Suspension setup | Current timber/workshop cut package | `suspension_wood_cribbing_rev_a/j40_suspension_wood_cribbing_rev_a_dimension_sheet.pdf` | Hardwood cribbing blocks and exact wedge chocks for suspension/brake support setup; includes interactive 3D visualisation. |
| `front_radiator_two_side_retention_rev_a` | Fabrication / chassis fixing | Template release with measurement hold | `front_radiator_two_side_retention_rev_a/j40_front_radiator_two_side_retention_rev_a_dimension_sheet.pdf` | Right-side radiator retention bracket derived from the measured left chassis-attached bracket; one 4 mm bolt-through saddle right-angle post with top screw return and interactive 3D visualisation. |
| `midi5_enclosure_rev_d` | Electrical reset | Current recommended MIDI holder enclosure | `midi5_enclosure_rev_d/j40_midi5_enclosure_rev_d_dimension_sheet.pdf` | Folded aluminium box with hinged lid, insulating subplate, one fuse-4 input grommet, five output grommets, and enlarged far-side double-cable output hole; includes interactive 3D visualisation. |
| `relay_mount_rev_d` | Electrical reset | Current recommended relay-box base | `relay_mount_rev_d/j40_relay_mount_rev_d_dimension_sheet.pdf` | Simplified relay support: flat aluminium base plate plus exact relay-bottom-footprint insulating sheet under the existing relay box's large uncovered bottom face; includes interactive 3D visualisation. |
| `battery_power_carrier_mount_rev_a` | Fabrication / chassis fixing / electrical reset | Prototype/mock-up release for chassis-mounted battery stand and integrated relay/fuse/cutoff carrier | `battery_power_carrier_mount_rev_a/j40_battery_power_carrier_mount_rev_a_dimension_sheet.pdf` | Formed chassis saddle/upright bridge with configurable body-side offset bars, full-height battery support tray/deck, hold-down crossbar, raised front/radiator-side service ladder, vertical Relay Rev D flat base/insulator directly attached to the main sheet, top-front MIDI Rev D enclosure shelf, side-mounted 100A breaker/cutoff base/guard, battery-to-cutoff and cutoff-to-relay/MIDI cable paths, and 3D visualisation files. |

## Reference / Fallback Electrical Packages

| Package | Workstream | Status | Primary PDF | Notes |
| --- | --- | --- | --- | --- |
| `relay_mount_rev_c` | Electrical reset | Superseded fallback standalone relay-box mount | `relay_mount_rev_c/j40_relay_mount_rev_c_dimension_sheet.pdf` | Folded aluminium relay carrier plus plastic rear guard; use only if the Rev D flat-base route is deliberately rejected; includes interactive 3D visualisation. |

## Superseded Electrical Packages

| Package | Status | Replacement |
| --- | --- | --- |
| `midi5_module_rev_a` | Superseded boxed MIDI module | `midi5_enclosure_rev_d` |
| `midi5_module_rev_b` | Superseded boxed MIDI module | `midi5_enclosure_rev_d` |
| `midi5_plate_mount_rev_c` | Superseded open MIDI plate | `midi5_enclosure_rev_d` |
| `relay_mount_rev_c` | Superseded folded relay carrier | `relay_mount_rev_d` |

## Generator Scripts

- `tools/generate_rubber_recreation_fabrication_pack.py`
- `tools/generate_suspension_wood_cribbing_rev_a.py`
- `tools/generate_front_radiator_two_side_retention_rev_a.py`
- `tools/generate_midi5_plate_mount_rev_c.py`
- `tools/generate_midi5_enclosure_rev_d.py`
- `tools/generate_relay_mount_rev_c.py`
- `tools/generate_relay_mount_rev_d.py`
- `tools/generate_fabrication_3d_visualisations.py`
- `tools/generate_battery_power_carrier_mount_rev_a.py`

The human handoff summary is `docs/fabrication-handoff-index.md`.

Raw material procurement estimate:
- `data/manual/fabrication_metal_stock_requirements.csv`
- `data/manual/fabrication_raw_material_estimates.csv`
- `docs/fabrication-metal-stock-list-20260514.md`
- `docs/fabrication-raw-materials-procurement-estimate-20260513.md`

The raw-stock estimate adds procurement rows for mild-steel battery/radiator sheet, plate, pre-formed 90-degree angle/L-section stock, aluminium and plastic electrical plate stock, small EPDM isolator sheet, and separate tub repair steel sheets/plates. Chassis-rubber materials remain controlled by the chassis-rubber/body-mount procurement rows rather than this Fabrication workstream.
