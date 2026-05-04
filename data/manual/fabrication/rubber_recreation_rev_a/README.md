# J40 Rubber Recreation Fabrication Pack - Rev A

This is the fabrication-output package for the body-mount and front-support rubber recreation workstream.

Use it with:

- `docs/rubber-recreation-fabrication-spec-20260502.md`
- `data/manual/rubber_recreation_fabrication_specs.csv`
- `data/manual/rubber_recreation_measurement_closure.csv`
- `data/manual/rubber_recreation_manufacturing_requirements.csv`

## Files To Send

- `j40_rubber_recreation_rev_a_dimension_sheet.pdf` - dimension and fabrication review sheet
- `machine_definitions.csv` / `machine_definitions.json` - CNC/shop geometry and controlled non-CNC purchase definitions
- `fabricator_cut_list.csv` - file-by-file cut/form list
- `inspection_checklist.csv` - receiving and first-article inspection checks

## DXF / SVG Parts

- `bm_sm_body_mount_cushion_rev_a.dxf` / `bm_sm_body_mount_cushion_rev_a.svg` - BM-SM small circular body-mount cushion, qty 10
- `bm_lg_body_mount_cushion_rev_a.dxf` / `bm_lg_body_mount_cushion_rev_a.svg` - BM-LG large circular body-mount cushion, qty 2
- `bm_cup_small_seat_washer_rev_a.dxf` / `bm_cup_small_seat_washer_rev_a.svg` - BM-CUP small body-mount cup washer, qty 10 working basis
- `bm_cup_large_seat_washer_rev_a.dxf` / `bm_cup_large_seat_washer_rev_a.svg` - BM-CUP large body-mount cup washer, qty 2 working basis
- `fs_oval_front_support_pad_rev_a.dxf` / `fs_oval_front_support_pad_rev_a.svg` - FS-OVAL front support two-hole isolator pad, qty 2 matched pieces
- `fs_strip_left_template_blank_rev_a.dxf` / `fs_strip_left_template_blank_rev_a.svg` - FS-STRIP-L front support strip quote/template blank, qty 1
- `fs_strip_right_template_blank_rev_a.dxf` / `fs_strip_right_template_blank_rev_a.svg` - FS-STRIP-R front support strip quote/template blank, qty 1
- `exh_hgr_90917_08004_teardrop_rev_a.dxf` / `exh_hgr_90917_08004_teardrop_rev_a.svg` - EXH-HGR-90917 Toyota 90917-08004 style exhaust cushion, qty as fitted

## Layer Rules

- `CUT`, `CUT_BORE`, `CUT_RELIEF`, and `DRILL` are through-cut or through-hole geometry.
- `RECESS`, `FORM`, and `INSERT_MARK` are register, forming, boss, or pocket controls. Do not through-cut them unless the physical sample proves that construction.
- `TEMPLATE` is a trace/quote guide only. The strip rubbers still require physical template tracing before production cutting.
- `CENTER` is construction geometry only.

## Release Limits

The circular cushions, cup blanks, and oval pad are ready for quote and first article from these files. Full production still requires the hold dimensions in `data/manual/rubber_recreation_measurement_closure.csv`.

The strip files are not final production cut patterns. They define stock envelope, section, and hole/slot working basis, but the actual left/right strip outline and hole centres must be traced from the physical rubber and metal carrier.

The exhaust holder is now controlled as the Toyota `90917-08004` / `17572-92000` teardrop cushion style. Buy the molded part where available; the CAD file is a local-copy control only and needs a genuine sample or intact original before a production mould is cut. Bump stops remain molded manufacturer/sample-matched parts unless a shop creates a proper mould from a physical sample or 3D scan.

## Material

Use new black automotive mount-grade solid rubber only: EPDM or NR/SBR, Shore A `60 +/-5`. Reject tyre rubber, crumb rubber, sponge foam, mixed offcuts, salvage rubber, and unmarked compound.

Steel cups must be `2.5-3.0 mm` steel, deburred and zinc plated or epoxy primed after forming. Sleeves are still controlled by stack dry-fit and are not released as a cut DXF.
