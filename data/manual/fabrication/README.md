# J40 Fabrication Output Index

This directory contains the repo-native fabrication packages that can be sent to a local fabricator or used for first-article review.

All dimensional packages use millimetres. Send the `DXF` files for CAD/CAM cutting, the `SVG` files for quick visual review where present, the package PDF for non-CAD review, and the `*_3d_visualisation.html` files when a browser-based assembly read is useful.

## Current Release Packages

| Package | Workstream | Status | Primary PDF | Notes |
| --- | --- | --- | --- | --- |
| `rubber_recreation_rev_a` | Chassis rubbers | Quote and first article ready; final production has measurement holds | `rubber_recreation_rev_a/j40_rubber_recreation_rev_a_dimension_sheet.pdf` | Body-mount cushions, cup washer blanks, oval front-support pad, and strip quote/template blanks. |
| `suspension_wood_cribbing_rev_a` | Suspension setup | Current timber/workshop cut package | `suspension_wood_cribbing_rev_a/j40_suspension_wood_cribbing_rev_a_dimension_sheet.pdf` | Hardwood cribbing blocks and exact wedge chocks for suspension/brake support setup; includes interactive 3D visualisation. |
| `front_radiator_two_side_retention_rev_a` | Fabrication / chassis fixing | Template release with measurement hold | `front_radiator_two_side_retention_rev_a/j40_front_radiator_two_side_retention_rev_a_dimension_sheet.pdf` | Right-side radiator retention bracket derived from the measured left chassis-attached bracket; one 4 mm bolt-through saddle right-angle post with top screw return and interactive 3D visualisation. |
| `midi5_plate_mount_rev_c` | Electrical reset | Current recommended MIDI holder mount | `midi5_plate_mount_rev_c/j40_midi5_plate_mount_rev_c_dimension_sheet.pdf` | Open plate plus non-conductive subplate; replaces the boxed MIDI module concept; includes interactive 3D visualisation. |
| `battery_power_carrier_mount_rev_a` | Fabrication / chassis fixing / electrical reset | Prototype/mock-up release for chassis-mounted battery stand and integrated relay/fuse/cutoff carrier | `battery_power_carrier_mount_rev_a/j40_battery_power_carrier_mount_rev_a_dimension_sheet.pdf` | Single chassis pickup plate/upright bridge, full-height battery support tray/deck, backplane, hold-down crossbar, known Relay Rev C base field, MIDI Rev C base/subplate field, cutoff base/guard field, cable support holes, and 3D visualisation files. |
| `relay_mount_rev_c` | Electrical reset | Fallback standalone relay-box mount | `relay_mount_rev_c/j40_relay_mount_rev_c_dimension_sheet.pdf` | Aluminium relay carrier plus plastic rear guard; use only if the relay box is mounted separately from the integrated battery power carrier; includes interactive 3D visualisation. |
| `electrical_modules_rev_a` | Electrical reset | Provisional/reference package | `electrical_modules_rev_a/j40_electrical_modules_rev_a_dimension_sheet.pdf` | Earlier combined under-bonnet relay/power module package with interactive 3D visualisation. Use only if the combined module route is still desired. |

## Superseded Electrical Packages

| Package | Status | Replacement |
| --- | --- | --- |
| `midi5_module_rev_a` | Superseded boxed MIDI module | `midi5_plate_mount_rev_c` |
| `midi5_module_rev_b` | Superseded boxed MIDI module | `midi5_plate_mount_rev_c` |

## Generator Scripts

- `tools/generate_rubber_recreation_fabrication_pack.py`
- `tools/generate_suspension_wood_cribbing_rev_a.py`
- `tools/generate_front_radiator_two_side_retention_rev_a.py`
- `tools/generate_electrical_module_drawings.py`
- `tools/generate_midi5_plate_mount_rev_c.py`
- `tools/generate_fabrication_3d_visualisations.py`
- `tools/generate_battery_power_carrier_mount_rev_a.py`
- `tools/generate_relay_mount_rev_c.py`

The human handoff summary is `docs/fabrication-handoff-index.md`.

Raw material procurement estimate:
- `data/manual/fabrication_raw_material_estimates.csv`
- `docs/fabrication-raw-materials-procurement-estimate-20260513.md`

The raw-stock estimate adds procurement rows for mild-steel battery/radiator plate, aluminium and plastic electrical plate stock, small EPDM isolator sheet, and separate tub repair steel sheets/plates. Chassis-rubber materials remain controlled by the chassis-rubber/body-mount procurement rows rather than this Fabrication workstream.
