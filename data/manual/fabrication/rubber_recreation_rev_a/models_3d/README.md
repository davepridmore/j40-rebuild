# J40 Rubber Recreation 3D Models

This folder contains parametric OpenSCAD models for the current Longman rubber
order and the related hold-only bump-stop/exhaust reference shapes.

Use these files as 3D conversation and first-article controls. They do not
replace the 2D DXF/SVG/PDF pack or the CSV release gates.

## Files

- `j40_rubber_models_master.scad` - includes all individual models.
- `model_manifest.csv` - model index, release status, and open old-part checks.
- `old_rubber_checks.md` - what to inspect on the original parts if needed.
- `bm_iso_sm_square_pad.scad` - `BM-ISO-SM` BM-ISO-SM main body isolator pad, small-height stations; first-article model with 18.0 mm bore for Toyota 90560-12009 style spacer
- `bm_iso_lg_square_pad.scad` - `BM-ISO-LG` BM-ISO-LG main body isolator pad, large stations; first-article model with 18.0 mm bore for Toyota 90560-12009 style spacer
- `fs_oval_front_support_pad.scad` - `FS-OVAL` FS-OVAL front support two-hole isolator pad; first-article model; relief/insert construction still sample-controlled
- `fs_strip_l_plain_strip.scad` - `FS-STRIP-L` FS-STRIP-L underfloor body-support strip liner left; first-article plain strip; local trim/holes only after dry-fit proves them
- `fs_strip_r_plain_strip.scad` - `FS-STRIP-R` FS-STRIP-R underfloor body-support strip liner right; first-article plain strip; local trim/holes only after dry-fit proves them
- `b_60010_long_measurement_model.scad` - `B-60010-LONG` BUMP-60010 rear/back long stop model, same front shape; May 31 front-stop measurement model; sample calipers, fixture fit, bracket fit, and strike offset required before mould release
- `b_60020_short_measurement_model.scad` - `B-60020-SHORT` BUMP-60020 exact front/right-front stop model; May 31 front-stop measurement model; sample calipers, fixture fit, bracket fit, and strike offset required before mould release
- `b_60010_rear_pair_measurement_model.scad` - `B-60010-REAR-PAIR` BUMP-60010 rear pair same front-shape model; May 31 front-stop measurement model; sample calipers, fixture fit, bracket fit, and strike offset required before mould release
- `exh_hgr_90917_teardrop_cushion.scad` - `EXH-HGR-90917` EXH-HGR-90917 teardrop exhaust cushion; hold-only; sample or installed support-point geometry required

## Critical Release Rules

- `BM-ISO-SM` and `BM-ISO-LG` default to `hole_d = 18.0`, matching the Toyota
  `90560-12009` spacer basis. Production release uses the 18.0 mm bore; `hole_d = 0`
  is a non-release CAD override only.
- The 80 x 80 body pads are deliberately simple. Extra BM-ISO pieces cover
  dry-fit stacking or station proof where two pads are needed; do not create
  new ribbed or shaped body-rubber variants without a station trace.
- `FS-OVAL` has optional `relief_depth`; the old part must prove whether the
  relief is real, blind, through-cut, or only deformation.
- `FS-STRIP-L/R` default to no holes; retainer slots are separate steel detail
  unless the old rubber proves the rubber itself was pierced.
- Bump-stop models use the May 31 exact front-stop photos as the visible shape
  master. Free height is known; the rear/back stop is the same shape stretched
  to the longer height. Rubber body outline, through-hole pitch/diameter,
  central fixture/channel detail, and strike geometry must still be checked
  against sample calipers, the removed metal fixture, cleaned vehicle brackets,
  and axle strike pads.
- The exhaust hanger model is hold-only until a sample or installed support
  measurements release thickness, side profile, and reinforcement detail.
