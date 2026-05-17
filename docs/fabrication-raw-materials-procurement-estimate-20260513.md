# Fabrication Raw Materials Procurement Estimate - 2026-05-13

Purpose: give procurement a single raw-stock buy list for the active fabrication packages, while keeping chassis-rubber and tub/body repair ownership clear.

Source data: [fabrication_raw_material_estimates.csv](../data/manual/fabrication_raw_material_estimates.csv). Metal-only list: [fabrication-metal-stock-list-20260514.md](fabrication-metal-stock-list-20260514.md).

## Buy Now / Quote Rows

| Procurement row | Workstream | Material | Estimate |
| --- | --- | --- | --- |
| `part_fabrication_raw_mild_steel_plate_3mm_20260513` | Fabrication | `3.0 mm` mild-steel sheet/plate plus `90-degree` angle/L-section stock | 1 sheet at least `600 x 600 mm`; `1000 x 500 mm` is acceptable/preferred if similarly priced. Add `25 x 25 x 3 mm` or `30 x 30 x 3 mm` mild-steel angle, `3 m` total, for tray/access-ladder rails and upstands. |
| `part_fabrication_raw_mild_steel_plate_4mm_20260513` | Fabrication | `4.0 mm` mild-steel plate plus structural `90-degree` angle/L-section stock | 1 plate at least `700 x 450 mm`; nearest stock size `1000 x 500` is acceptable. Add `50 x 50 x 4 mm` angle, `1 m`, for the radiator post; `40 x 40 x 4 mm` angle, `2 m`, for battery stand/upright mock-up if available; final crush-tube sleeve stock waits for bolt-size confirmation. |
| `part_fabrication_raw_aluminium_plate_3mm_20260513` | Fabrication | `3.0 mm` 5052-H32 aluminium sheet | `600 x 600 mm` minimum for the current MIDI Rev D enclosure body/lid, Relay Rev D `360 x 245` flat base, and folded cutoff base/guard with `20 mm` upward lips. |
| `part_fabrication_raw_electrical_plastic_sheet_20260513` | Fabrication | Electrical insulating board/sheet | `5.0 mm` board at least `200 x 150 mm` for the MIDI subplate, plus `3.0 mm` sheet at least `350 x 250 mm` for the Relay Rev D insulating sheet. |
| `part_fabrication_raw_epdm_sheet_small_isolators_20260513` | Fabrication / chassis fixing | `3-5 mm` EPDM/SBR sheet | 1 small sheet at least `300 x 300 mm`. |
| `part_tub_repair_steel_sheet_1_2mm_20260513` | Body chassis | `1.2 mm` cold-rolled mild-steel sheet | 1 sheet about `1000 x 1000 mm` for tub skin, floor-pan, firewall lip, and small closure patches. |
| `part_tub_repair_steel_sheet_1_6mm_20260513` | Body chassis | `1.6 mm` cold-rolled mild-steel sheet | 1 sheet about `1000 x 500 mm` for heavier tub floor sections, flange returns, seat-box edges, and local patch plates. |
| `part_tub_mount_reinforcement_plate_3mm_20260513` | Body chassis | `3.0 mm` mild-steel plate | 1 plate about `500 x 500 mm` or `300 x 600 mm` for tub body-mount backing, captive-nut/weld-nut repair plates, and reinforcement coupons. |

## Existing Coverage

These are already in procurement and were not duplicated:

| Existing row | Material scope | Status |
| --- | --- | --- |
| `part_suspension_wooden_cribbing_blocks` | Seasoned hardwood cribbing blocks and wedge chocks | Received; price/payment, wood type, and received-condition photos still need capture. |
| `part_body_mount_rubber_kit` | Body mount rubber kit | Spec ready / release hold. |
| `part_body_mount_hardware_kit` | Body mount cups, sleeves, and related hardware | Spec ready / release hold. |
| `part_body_mount_shim_pack` | Body mount shim and spacer steel | Spec ready / release hold. |

## Guardrails

- Do not consume the battery/radiator fabrication steel for tub repair patches; the tub has separate sheet and plate rows.
- Do not fabricate the battery stand from aluminium. The current route is steel for the compact tray, widened front/radiator access-ladder spine, top-front shelf/pickup tabs, formed chassis saddle, upright bridge, and adjustable offset bars; the aluminium stock covers the MIDI Rev D enclosure body/lid, Relay Rev D flat base, and folded cutoff base/guard only.
- Use pre-formed `90-degree` steel angle/L-section wherever it simplifies tray edges, access-ladder rails, the radiator post, or stand bridge trials. Do not drop the flat sheet/plate requirement unless the deck, chassis saddle, and mounting faces are separately redesigned.
- Do not reopen chassis-rubber ordering under Fabrication. Chassis rubbers stay under the chassis-rubber/body-mount rows above.
- Final tub patch shapes remain measurement controlled after cleaning and rust-map photos.
