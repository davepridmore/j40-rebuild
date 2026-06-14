# Longman Rubber Order 2026-05-08

This folder is the supplier-facing fabrication handoff for the current Longman chassis/body rubber order.

Order it as three supplier-facing things:

1. Simple `80 x 80` body pads: one active `80 x 80 x 24` size, x30, with extras for two-pad stacks where dry-fit proves them. The smaller `22 mm` body-rubber line is removed.
2. Front support / body-support rubbers: `FS-OVAL` x2 plus `2 m` of `38 x 8` strip stock, with `FS-STRIP-L/R` cut as two `420 mm` strips from that stock after dry-fit.
3. Bump stops: `BUMP-60010-LONG` x3 and `BUMP-60020-SHORT` x1.

The part IDs remain the drawing and first-article controls inside those three order groups.

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
- `../rubber_recreation_rev_a/bm_iso_lg_square_pad_rev_a.dxf` / `.svg` - single active `80 x 80 x 24` body-pad 2D control; the smaller BM-ISO-SM / 22 mm line is removed from this order.
- `../rubber_recreation_rev_a/bump_stop_vehicle_measurement_control.dxf` / `.svg` - bump-stop May 31 front-shape, rubber through-hole, central fixture/channel, height, and vehicle-measurement control.
- `chassis_rubber_current_order_preview_rev_a.svg` - active Longman order preview sheet; current quote/first-article lines only.
- `../rubber_recreation_rev_a/chassis_rubber_location_map_rev_a.svg` - vehicle-location map for the rubber families in this order.
- `../rubber_recreation_rev_a/chassis_rubber_all_drawings_preview_rev_a.svg` - complete SVG preview showing the active and hold/reference chassis-rubber controls together.

The OpenSCAD files are the source 3D controls. The SVG/DXF files are the 2D shop controls. The HTML/SVG bundle visual is for orientation and communication.

## Current Release

The measured old-rubber photos are the quote and first-article basis for the current Longman order. Remaining checks are station fit, dry-stack compression, any proven two-pad body station, final caliper confirmation for `FS-OVAL`, and local strip trim after dry-fit.

- Body pads: 80 L x 80 W x 24 H square pad, x30, 18.0 mm through bore, R1.5 plan corners, top/bottom edge break or chamfer. Same flat square pad can be doubled only where dry-fit proves extra height is needed. Smaller 22 mm body pad is removed from the order.
- `FS-OVAL`: 96 L x 64 W x 15 T capsule, R32 ends, two 12 mm holes, relief/insert details sample-controlled.
- `FS-STRIP-L/R`: cut two 420 L x 38 W x 8 T plain strips from a 2 m order of 38 x 8 strip stock after dry-fit; allow for the landing path not being perfectly straight; no rubber holes by default.
- Bump stops: height and May 31 exact front-stop construction are controlled. Copy the broad rounded/tapered rubber body, two rubber through-holes, central fixture/channel interface, and flat strike area from the front-stop photos/sample; rear/back stops use the same shape made longer. Trace or reuse the metal fixture separately and confirm strike geometry on the vehicle.

Steel sleeves, cup/seat washers, bolts, shims, and retainers are separate hardware controls, not Longman rubber mould geometry.

Vehicle location is controlled by `../rubber_recreation_rev_a/chassis_rubber_location_map_rev_a.svg`: main body pads sit in the tub-to-chassis mount stack, `FS-OVAL` and `FS-STRIP-L/R` sit at the separate front-support/body-support landings, long bump stops cover front-left and both rear axle stations, and the short bump stop is right-front only.

Hold-only items remain separate from the quote-ready rubber: full-width/body liner strips and exhaust hanger cushion production need an actual sample, installed path, or tracing before ordering.
