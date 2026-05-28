# Longman Rubber Order 2026-05-08

This folder is the supplier-facing fabrication handoff for the current Longman chassis/body rubber order.

Use it with:

- `docs/longman-rubber-order-spec-20260508.md`
- `data/manual/longman_rubber_order_specs.csv`
- `docs/chassis-rubbers-workstream.md`
- `data/manual/fabrication/rubber_recreation_rev_a/models_3d/`

## 3D Fabrication Assets

- `longman_rubber_order_20260508_3d_visualisation.html` - interactive browser visual for the current order bundle.
- `longman_rubber_order_20260508_3d_visualisation.svg` - static fallback visual.
- `../rubber_recreation_rev_a/models_3d/j40_rubber_models_master.scad` - OpenSCAD master that includes all rubber models.
- `../rubber_recreation_rev_a/models_3d/model_manifest.csv` - part-by-part 3D model index and release status.
- `../rubber_recreation_rev_a/models_3d/old_rubber_checks.md` - old-part checks needed before closing uncertain features.
- `../rubber_recreation_rev_a/bm_iso_sm_square_pad_rev_a.dxf` / `.svg` - BM-ISO-SM square pad 2D control.
- `../rubber_recreation_rev_a/bm_iso_lg_square_pad_rev_a.dxf` / `.svg` - BM-ISO-LG square pad 2D control.
- `../rubber_recreation_rev_a/bump_stop_vehicle_measurement_control.dxf` / `.svg` - bump-stop steel-saddle hole, pitch, height, and vehicle-measurement control.
- `../rubber_recreation_rev_a/chassis_rubber_location_map_rev_a.svg` - vehicle-location map for the rubber families in this order.
- `../rubber_recreation_rev_a/chassis_rubber_all_drawings_preview_rev_a.svg` - complete SVG preview showing the active and hold/reference chassis-rubber controls together.

The OpenSCAD files are the source 3D controls. The SVG/DXF files are the 2D shop controls. The HTML/SVG bundle visual is for orientation and communication.

## Current Release

The measured old-rubber photos are the quote and first-article basis for the current Longman order. Remaining checks are station fit, dry-stack compression, final caliper confirmation for `FS-OVAL`, and local strip trim after dry-fit.

- `BM-ISO-SM`: 70 L x 70 W x 22 H square pad, 18.0 mm through bore, R1.5 plan corners, top/bottom edge break or chamfer.
- `BM-ISO-LG`: 80 L x 80 W x 24 H square pad, 18.0 mm through bore, same edge controls.
- `FS-OVAL`: 96 L x 64 W x 15 T capsule, R32 ends, two 12 mm holes, relief/insert details sample-controlled.
- `FS-STRIP-L/R`: 165 L x 38 W x 8 T plain strips, no rubber holes by default.
- Bump stops: height and Toyota-style construction are controlled; steel-saddle base/bolt holes and strike geometry are vehicle-measurement controlled. Do not add through-holes in the rubber body unless a genuine sample proves them.

Steel sleeves, cup/seat washers, bolts, shims, and retainers are separate hardware controls, not Longman rubber mould geometry.

Vehicle location is controlled by `../rubber_recreation_rev_a/chassis_rubber_location_map_rev_a.svg`: main body pads sit in the tub-to-chassis mount stack, `FS-OVAL` and `FS-STRIP-L/R` sit at the separate front-support/body-support landings, long bump stops cover front-left and both rear axle stations, and the short bump stop is right-front only.

Hold-only items remain separate from the quote-ready rubber: full-width/body liner strips and exhaust hanger cushion production need an actual sample, installed path, or tracing before ordering.
