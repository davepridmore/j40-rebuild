# J40 Rubber Recreation Fabrication Pack - Rev A

This is the fabrication-output package for the body-mount and front-support rubber recreation workstream.

Current release basis: the Longman order uses the square `BM-ISO-SM` and `BM-ISO-LG` body pads. Use the `bm_iso_*_square_pad_rev_a` SVG/DXF files for the 2D profile and the matching OpenSCAD files in `models_3d/` for the 3D envelope. The older circular `BM-SM` / `BM-LG` DXF files are retained as legacy photo-derived references only; do not use them as the active body-pad cut patterns unless the project deliberately reopens the circular profile.

Use it with:

- `docs/rubber-recreation-fabrication-spec-20260502.md`
- `data/manual/rubber_recreation_fabrication_specs.csv`
- `data/manual/rubber_recreation_measurement_closure.csv`
- `data/manual/rubber_recreation_manufacturing_requirements.csv`

## Files To Send

- `j40_rubber_recreation_rev_a_dimension_sheet.pdf` - dimension and fabrication review sheet
- `machine_definitions.csv` / `machine_definitions.json` - CNC/shop geometry, shim-pack controls, and controlled non-CNC purchase definitions
- `fabricator_cut_list.csv` - file-by-file cut/form list
- `inspection_checklist.csv` - receiving and first-article inspection checks
- `models_3d/` - parametric OpenSCAD 3D models and old-part closure questions

## DXF / SVG Parts

- `bm_iso_sm_square_pad_rev_a.dxf` / `bm_iso_sm_square_pad_rev_a.svg` - active BM-ISO-SM square body isolator pad, `70 x 70 x 22`, `18.0 mm` centre bore, qty `10 + 2 spares`
- `bm_iso_lg_square_pad_rev_a.dxf` / `bm_iso_lg_square_pad_rev_a.svg` - active BM-ISO-LG square body isolator pad, `80 x 80 x 24`, `18.0 mm` centre bore, qty `2 + 1 spare`
- `bm_sm_body_mount_cushion_rev_a.dxf` / `bm_sm_body_mount_cushion_rev_a.svg` - legacy BM-SM small circular body-mount reference, superseded for the current Longman order by `bm_iso_sm_square_pad_rev_a.*` and `models_3d/bm_iso_sm_square_pad.scad`
- `bm_lg_body_mount_cushion_rev_a.dxf` / `bm_lg_body_mount_cushion_rev_a.svg` - legacy BM-LG large circular body-mount reference, superseded for the current Longman order by `bm_iso_lg_square_pad_rev_a.*` and `models_3d/bm_iso_lg_square_pad.scad`
- `bm_cup_small_seat_washer_rev_a.dxf` / `bm_cup_small_seat_washer_rev_a.svg` - BM-CUP small body-mount cup washer, qty 10 working basis
- `bm_cup_large_seat_washer_rev_a.dxf` / `bm_cup_large_seat_washer_rev_a.svg` - BM-CUP large body-mount cup washer, qty 2 working basis
- `fs_oval_front_support_pad_rev_a.dxf` / `fs_oval_front_support_pad_rev_a.svg` - FS-OVAL front support two-hole isolator pad, qty 2 matched pieces
- `fs_strip_left_template_blank_rev_a.dxf` / `fs_strip_left_template_blank_rev_a.svg` - FS-STRIP-L underfloor body-support strip first-article blank, qty 1
- `fs_strip_right_template_blank_rev_a.dxf` / `fs_strip_right_template_blank_rev_a.svg` - FS-STRIP-R underfloor body-support strip first-article blank, qty 1
- `bump_stop_vehicle_measurement_control.dxf` / `bump_stop_vehicle_measurement_control.svg` - BUMP-F-L/F-R/R vehicle-measurement control drawing for saddle holes, pitch, and height; not a final mould/cut profile
- `exh_hgr_90917_08004_teardrop_rev_a.dxf` / `exh_hgr_90917_08004_teardrop_rev_a.svg` - EXH-HGR-90917 teardrop exhaust cushion, qty as fitted

## Layer Rules

- `CUT`, `CUT_BORE`, `CUT_RELIEF`, and `DRILL` are through-cut or through-hole geometry.
- `RECESS`, `FORM`, and `INSERT_MARK` are register, forming, boss, or pocket controls. Do not through-cut them unless the physical sample proves that construction.
- `TEMPLATE` is a trace/quote guide only. The plain strip rubber dimensions are released; only local end trim and separate steel retainer geometry remain dry-fit or trace controlled.
- `CENTER` is construction geometry only.

## Release Limits

The active Longman rubber lines are released for quote and first article from the current CSV/spec data: `BM-ISO-SM`, `BM-ISO-LG`, `FS-OVAL`, `FS-STRIP-L`, and `FS-STRIP-R`. The remaining closure rows in `data/manual/rubber_recreation_measurement_closure.csv` are station-fit, stack, caliper, and dry-fit gates before final production/install, not missing quote dimensions.

The current Longman rubber-order basis for the main body pads is square flat isolator pads, not the earlier circular placeholder. Use `bm_iso_sm_square_pad_rev_a.dxf` / `.svg` and `bm_iso_lg_square_pad_rev_a.dxf` / `.svg` for the current 2D profile, and use `models_3d/bm_iso_sm_square_pad.scad` / `models_3d/bm_iso_lg_square_pad.scad` for the 3D envelope. They default to `hole_d = 18.0`, matching the Toyota `90560-12009` style body-mount sleeve basis. Production release uses the 18.0 mm bore; `hole_d = 0` is a non-release CAD override only.

The shim packs are controlled in `machine_definitions.csv` / `machine_definitions.json` as new flat steel thickness packs. They are not released as fixed DXF outlines until the original shim or mount-station footprint is traced in millimeters; do not substitute washer stacks.

The strip rubber geometry is released as plain `165 x 38 x 8 mm` left/right first articles with no rubber holes by default. Dry-fit controls only local end trim and side orientation. Any slotted steel retainer is a separate steel part and must be reused or traced directly from the original retainer if remade.

The exhaust holder is controlled as a teardrop cushion style using Toyota `90917-08004` / `17572-92000` only as a reference shape. Source exact new molded stock if it is in hand; otherwise the CAD file is a local-copy control and needs a genuine sample or intact original before a production mould is cut.

Bump stops cannot rely on Toyota/manufacturer supply and the old rubbers are too decayed to copy. Public OEM/catalog sources checked confirm the Toyota numbers, application, and `70 mm`/`60 mm` height split, but not the Toyota mould drawing, compound recipe, or load/deflection curve. Use `docs/bump-stop-fabrication-spec-20260504.md`: long `48304-60010` positions are `70 mm` free height, the right-front `48304-60020` is `60 mm` free height, and all base footprints, bolt/stud patterns, and contact offsets are released from the actual cleaned vehicle brackets and axle strike pads. A NOS/genuine sample is the preferred master if found; otherwise reproduce the Toyota-style two-ear steel saddle/backing plate, tapered/radiused progressive rubber body, and flat rectangular strike face. Do not make bump stops from simple cut rubber blocks.

## Material

Use new black automotive mount-grade solid rubber only: EPDM or NR/SBR, Shore A `60 +/-5`, for body/front-support rubbers. Bump stops use the separate higher-duty target in the bump-stop spec: NR/SBR automotive bump-stop rubber Shore A `70 +/-5` bonded/captive to a new coated steel saddle, or cast PU Shore A `80 +/-5` only if the progressive geometry and captive steel mounting are held. Reject tyre rubber, crumb rubber, sponge foam, mixed offcuts, used rubber, salvage rubber, and unmarked compound.

Steel cups must be `2.5-3.0 mm` steel, deburred and zinc plated or epoxy primed after forming. Sleeves are controlled by the Toyota `90560-12009` style spacer basis and stack dry-fit, and are not released as a DXF rubber-shop cut pattern.
