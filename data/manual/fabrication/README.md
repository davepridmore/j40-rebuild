# J40 Fabrication Output Index

This directory contains the repo-native fabrication packages that can be sent to a local fabricator or used for first-article review.

All dimensional packages use millimetres. Send the `DXF` files for CAD/CAM cutting, the `SVG` files for quick visual review where present, and the package PDF for non-CAD review.

## Current Release Packages

| Package | Workstream | Status | Primary PDF | Notes |
| --- | --- | --- | --- | --- |
| `rubber_recreation_rev_a` | Chassis rubbers | Quote and first article ready; final production has measurement holds | `rubber_recreation_rev_a/j40_rubber_recreation_rev_a_dimension_sheet.pdf` | Body-mount cushions, cup washer blanks, oval front-support pad, and strip quote/template blanks. |
| `midi5_plate_mount_rev_c` | Electrical reset | Current recommended MIDI holder mount | `midi5_plate_mount_rev_c/j40_midi5_plate_mount_rev_c_dimension_sheet.pdf` | Open plate plus non-conductive subplate; replaces the boxed MIDI module concept. |
| `relay_mount_rev_c` | Electrical reset | Current recommended relay-box mount | `relay_mount_rev_c/j40_relay_mount_rev_c_dimension_sheet.pdf` | Aluminium relay carrier plus plastic rear guard. |
| `electrical_modules_rev_a` | Electrical reset | Provisional/reference package | `electrical_modules_rev_a/j40_electrical_modules_rev_a_dimension_sheet.pdf` | Earlier combined under-bonnet relay/power module package. Use only if the combined module route is still desired. |

## Superseded Electrical Packages

| Package | Status | Replacement |
| --- | --- | --- |
| `midi5_module_rev_a` | Superseded boxed MIDI module | `midi5_plate_mount_rev_c` |
| `midi5_module_rev_b` | Superseded boxed MIDI module | `midi5_plate_mount_rev_c` |

## Generator Scripts

- `tools/generate_rubber_recreation_fabrication_pack.py`
- `tools/generate_electrical_module_drawings.py`
- `tools/generate_midi5_plate_mount_rev_c.py`
- `tools/generate_relay_mount_rev_c.py`

The human handoff summary is `docs/fabrication-handoff-index.md`.
