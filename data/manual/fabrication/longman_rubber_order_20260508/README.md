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

The OpenSCAD files are the source 3D controls. The HTML/SVG visual is for orientation and communication.

## Current Release

The measured old-rubber photos are the quote and first-article basis for the current Longman order. Remaining checks are station fit, dry-stack compression, final caliper confirmation for `FS-OVAL`, and local strip trim after dry-fit.

- `BM-ISO-SM`: 70 L x 70 W x 22 H square pad, 18.0 mm through bore, R1.5 plan corners, top/bottom edge break or chamfer.
- `BM-ISO-LG`: 80 L x 80 W x 24 H square pad, 18.0 mm through bore, same edge controls.
- `FS-OVAL`: 96 L x 64 W x 15 T capsule, R32 ends, two 12 mm holes, relief/insert details sample-controlled.
- `FS-STRIP-L/R`: 165 L x 38 W x 8 T plain strips, no rubber holes by default.
- Bump stops: height and Toyota-style construction are controlled; base, saddle, bolt, and strike geometry are vehicle-measurement controlled.

Steel sleeves, cup/seat washers, bolts, shims, and retainers are separate hardware controls, not Longman rubber mould geometry.

Hold-only items remain separate from the quote-ready rubber: full-width/body liner strips and exhaust hanger cushion production need an actual sample, installed path, or tracing before ordering.
