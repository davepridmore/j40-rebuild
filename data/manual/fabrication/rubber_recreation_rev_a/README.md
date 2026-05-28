# J40 Rubber Recreation Fabrication Pack - Rev A

This is the fabrication-output package for the body-mount and front-support rubber recreation workstream.

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

- `bm_iso_sm_square_pad_rev_a.dxf` / `bm_iso_sm_square_pad_rev_a.svg` - BM-ISO-SM small square body isolator pad, qty 10 plus 2 spares
- `bm_iso_lg_square_pad_rev_a.dxf` / `bm_iso_lg_square_pad_rev_a.svg` - BM-ISO-LG large square body isolator pad, qty 2 plus 1 spare
- `bm_cup_small_seat_washer_rev_a.dxf` / `bm_cup_small_seat_washer_rev_a.svg` - BM-CUP small body-mount cup washer, qty 10 working basis
- `bm_cup_large_seat_washer_rev_a.dxf` / `bm_cup_large_seat_washer_rev_a.svg` - BM-CUP large body-mount cup washer, qty 2 working basis
- `fs_oval_front_support_pad_rev_a.dxf` / `fs_oval_front_support_pad_rev_a.svg` - FS-OVAL front support two-hole isolator pad, qty 2 matched pieces
- `fs_strip_left_template_blank_rev_a.dxf` / `fs_strip_left_template_blank_rev_a.svg` - FS-STRIP-L underfloor body-support strip first-article blank, qty 1
- `fs_strip_right_template_blank_rev_a.dxf` / `fs_strip_right_template_blank_rev_a.svg` - FS-STRIP-R underfloor body-support strip first-article blank, qty 1
- `exh_hgr_90917_08004_teardrop_rev_a.dxf` / `exh_hgr_90917_08004_teardrop_rev_a.svg` - EXH-HGR-90917 teardrop exhaust cushion, qty as fitted

## Layer Rules

- `CUT`, `CUT_BORE`, `CUT_RELIEF`, and `DRILL` are through-cut or through-hole geometry.
- `RECESS`, `FORM`, and `INSERT_MARK` are register, forming, boss, or pocket controls. Do not through-cut them unless the physical sample proves that construction.
- `TEMPLATE` is a trace/quote guide only when present. The current strip rubbers are released as plain `CUT` blanks.
- `CENTER` is construction geometry only.

## Release Limits

The square BM-ISO body pads, cup blanks, and oval pad are ready for quote and first article from these files. Full production still requires the hold dimensions in `data/manual/rubber_recreation_measurement_closure.csv`.

The current Longman rubber-order basis for the main body pads is square flat isolator pads, not the earlier circular placeholder. Use `bm_iso_sm_square_pad_rev_a.dxf` / `.svg`, `bm_iso_lg_square_pad_rev_a.dxf` / `.svg`, and the matching `models_3d/bm_iso_sm_square_pad.scad` / `models_3d/bm_iso_lg_square_pad.scad` files for the current envelope. They default to an `18.0 mm` bore, matching the Toyota `90560-12009` style body-mount sleeve basis. Production release uses the 18.0 mm bore; `hole_d = 0` is a non-release CAD override only. The old circular `BM-SM` / `BM-LG` drawings are legacy placeholders and are not active Longman body-pad controls.

The shim packs are controlled in `machine_definitions.csv` / `machine_definitions.json` as new flat steel thickness packs. They are not released as fixed DXF outlines until the original shim or mount-station footprint is traced in millimeters; do not substitute washer stacks.

The strip files are released plain first-article cut patterns at `420 x 38 x 8 mm`. The May 17 ruler photos show about `16.5 in` old-strip length, converted to `419 mm` and rounded to `420 mm`. Do not add holes, slots, bonding, raised-load pads, or handed trim unless the dry-fit and physical retainer prove them; trace/reuse the steel retainer separately if it must be remade.

The exhaust holder is controlled as a teardrop cushion style using Toyota `90917-08004` / `17572-92000` only as a reference shape. Source exact new molded stock if it is in hand; otherwise the CAD file is a local-copy control and needs a genuine sample or intact original before a production mould is cut.

Bump stops cannot rely on Toyota/manufacturer supply and the old rubbers are too decayed to copy. Public OEM/catalog sources checked confirm the Toyota numbers, application, and `70 mm`/`60 mm` height split, but not the Toyota mould drawing, compound recipe, or load/deflection curve. Use `docs/bump-stop-fabrication-spec-20260504.md`: long `48304-60010` positions are `70 mm` free height, the right-front `48304-60020` is `60 mm` free height, and the rubber base footprint, bolt/stud pitch, relaxed stretch-fit hole or slot size, and contact offsets are released from the actual cleaned vehicle brackets and axle strike pads. A NOS/genuine sample is the preferred master if found; otherwise reproduce the Toyota-style tapered/radiused progressive rubber body and flat rectangular strike face as a rubber-only stretch-fit bolt-on part. Do not make bump stops from simple cut rubber blocks, and do not include a steel saddle/backing plate.

## Material

Use new black automotive mount-grade solid rubber only: EPDM or NR/SBR, Shore A `60 +/-5`, for body/front-support rubbers. Bump stops use the separate higher-duty target in the bump-stop spec: NR/SBR automotive bump-stop rubber Shore A `70 +/-5` as rubber-only stretch-fit bolt-on parts, or cast PU Shore A `80 +/-5` only if the progressive geometry, stretch-fit installation, and rebound recovery are proven. Reject tyre rubber, crumb rubber, sponge foam, mixed offcuts, used rubber, salvage rubber, and unmarked compound.

Steel cups must be `2.5-3.0 mm` steel, deburred and zinc plated or epoxy primed after forming. Sleeves are still controlled by stack dry-fit and are not released as a cut DXF.
