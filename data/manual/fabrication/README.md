# J40 Fabrication Output Index

This directory contains the repo-native fabrication packages that can be sent to a local fabricator or used for first-article review.

All dimensional packages use millimetres. Send the `DXF` files for CAD/CAM cutting, the `SVG` files for quick visual review where present, the package PDF for non-CAD review, and the `*_3d_visualisation.html` files when a browser-based assembly read is useful.

## Current Release Packages

| Package | Workstream | Status | Primary PDF | Notes |
| --- | --- | --- | --- | --- |
| `dashboard_lcd_hvac_fascia_rev_i` | Dashboard / infotainment / A/C HVAC | Owner-selected V35 centre-cassette target; CNC quotation plus full-size/full-depth disposable template only; production geometry and cutting held for M1-M9, with M10 required before commissioned vehicle handoff | `dashboard_lcd_hvac_fascia_rev_i/README.md` | Centre-only removable cassette replacing the ashtray area while the OEM outer fascia, formed contours, large asymmetric plate-and-knob glovebox, complete Toyota speedometer and factory RHD column scallop remain unchanged. The cassette carries the true 9-inch LCD and a single line of seven bought selectors plus separate red Hazard; exactly two high outer/end chrome/silver outlets are separate retained-panel operations. Every final cut, aperture and behind-dash feature remains controlled by the vehicle trace and bought-component measurements. |
| `rubber_recreation_rev_a` | Chassis rubbers | Quote and first article ready; final production has station-fit gates | `rubber_recreation_rev_a/j40_rubber_recreation_rev_a_dimension_sheet.pdf` | Square body-pad 3D controls, cup washer blanks, oval front-support pad, and released plain underfloor strip drawings. |
| `suspension_wood_cribbing_rev_a` | Suspension setup | Current timber/workshop cut package | `suspension_wood_cribbing_rev_a/j40_suspension_wood_cribbing_rev_a_dimension_sheet.pdf` | Hardwood cribbing blocks and exact wedge chocks for suspension/brake support setup; includes interactive 3D visualisation. |
| `na_cooling_connector_arms_rev_p` | Fabrication / radiator / chassis fixing / A/C HVAC | Current measured and structural release HOLD | `na_cooling_connector_arms_rev_p/README.md` | Naturally aspirated package: matched connector-sized A0 arms, lower cradle, separate G0 removable-guard and radiator holders, independent carriers, one FS front A/C pusher and one FL rear puller. CL0 directly holds the complete G0 perimeter frame, FS frame/rotor datum and C0 usable-fin-field centreline within ±2 mm laterally of VCL; G0-to-fixed-body-aperture and FS-to-C0 local X/Z checks are separate and must not be tolerance-stacked. Final material and geometry await signed measurements and structural release. |
| `front_cooling_stack_rev_a` | Fabrication / radiator / A/C HVAC | Historical turbo-era mock-up; superseded by Rev P | `front_cooling_stack_rev_a/README.md` | Retained for provenance only. Do not use its full-height uprights, turbo/intercooler architecture or fan arrangement for current fabrication or procurement. |
| `midi5_enclosure_rev_d` | Electrical reset | Current recommended MIDI holder enclosure | `midi5_enclosure_rev_d/j40_midi5_enclosure_rev_d_dimension_sheet.pdf` | Folded aluminium box with hinged lid, insulating subplate, one fuse-4 input grommet, five output grommets, and enlarged far-side double-cable output hole; includes interactive 3D visualisation. |
| `relay_mount_rev_d` | Electrical reset | Current recommended relay-box base | `relay_mount_rev_d/j40_relay_mount_rev_d_dimension_sheet.pdf` | Simplified relay support: flat aluminium base plate plus exact relay-bottom-footprint insulating sheet under the existing relay box's large uncovered bottom face; includes interactive 3D visualisation. |
| `battery_power_carrier_mount_rev_a` | Fabrication / chassis fixing / electrical reset | Prototype/mock-up release for chassis-mounted battery stand and integrated relay/fuse/cutoff carrier | `battery_power_carrier_mount_rev_a/j40_battery_power_carrier_mount_rev_a_dimension_sheet.pdf` | Formed chassis saddle/upright bridge with configurable body-side offset bars, full-height battery support tray/deck, hold-down crossbar, raised front/radiator-side service ladder, vertical Relay Rev D flat base/insulator directly attached to the main sheet, top-front MIDI Rev D enclosure shelf, side-mounted 100A breaker/cutoff base/guard, battery-to-cutoff and cutoff-to-relay/MIDI cable paths, and 3D visualisation files. |

## Superseded Dashboard Packages

| Package | Status | Replacement |
| --- | --- | --- |
| `dashboard_lcd_hvac_fascia_rev_g` | Superseded four-outlet quotation/template record; do not use its V1-V4 apertures, coordinates or duct schedule for the current job | `dashboard_lcd_hvac_fascia_rev_i` |

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
- `tools/generate_dashboard_lcd_hvac_fascia_rev_g.py` — archive-only generator for the superseded four-outlet record

The human handoff summary is `docs/fabrication-handoff-index.md`.

Raw material procurement estimate:
- `data/manual/fabrication_metal_stock_requirements.csv`
- `data/manual/fabrication_raw_material_estimates.csv`
- `docs/fabrication-metal-stock-list-20260514.md`
- `docs/fabrication-raw-materials-procurement-estimate-20260513.md`

The raw-stock estimate adds procurement rows for mild-steel battery/radiator sheet, plate, pre-formed 90-degree angle/L-section stock, aluminium and plastic electrical plate stock, small EPDM isolator sheet, and separate tub repair steel sheets/plates. Chassis-rubber materials remain controlled by the chassis-rubber/body-mount procurement rows rather than this Fabrication workstream.
