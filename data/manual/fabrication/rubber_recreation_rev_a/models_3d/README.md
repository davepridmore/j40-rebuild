# J40 Rubber Recreation 3D Models

This folder contains parametric OpenSCAD models for the current Longman rubber
order and the related hold-only bump-stop/exhaust reference shapes.

Use these files as 3D conversation and first-article controls. They do not
replace the 2D DXF/SVG/PDF pack or the CSV release gates.

## Files

- `j40_rubber_models_master.scad` - includes all individual models.
- `model_manifest.csv` - model index, release status, and open old-part checks.
- `old_rubber_checks.md` - what to inspect on the original parts if needed.
- `bm_iso_sm_square_pad.scad` - `BM-ISO-SM` BM-ISO-SM main body isolator pad, small stations; first-article model with 18.0 mm bore for Toyota 90560-12009 style spacer
- `bm_iso_lg_square_pad.scad` - `BM-ISO-LG` BM-ISO-LG main body isolator pad, large stations; first-article model with 18.0 mm bore for Toyota 90560-12009 style spacer
- `fs_oval_front_support_pad.scad` - `FS-OVAL` FS-OVAL front support two-hole isolator pad; first-article model; relief/insert construction still sample-controlled
- `fs_strip_l_plain_strip.scad` - `FS-STRIP-L` FS-STRIP-L underfloor body-support strip liner left; first-article plain strip; local trim/holes only after dry-fit proves them
- `fs_strip_r_plain_strip.scad` - `FS-STRIP-R` FS-STRIP-R underfloor body-support strip liner right; first-article plain strip; local trim/holes only after dry-fit proves them
- `b_60010_long_measurement_model.scad` - `B-60010-LONG` BUMP-60010 long bump stop model, front-left and rear; rubber-only stretch-fit measurement model; bracket dimensions, relaxed hole/slot size, and strike offset required before mould release
- `b_60020_short_measurement_model.scad` - `B-60020-SHORT` BUMP-60020 short right-front bump stop model; rubber-only stretch-fit measurement model; bracket dimensions, relaxed hole/slot size, and strike offset required before mould release
- `b_60010_rear_pair_measurement_model.scad` - `B-60010-REAR-PAIR` BUMP-60010 rear pair bump stop model; rubber-only stretch-fit measurement model; bracket dimensions, relaxed hole/slot size, and strike offset required before mould release
- `exh_hgr_90917_teardrop_cushion.scad` - `EXH-HGR-90917` EXH-HGR-90917 teardrop exhaust cushion; hold-only; sample or installed support-point geometry required

## Critical Release Rules

- `BM-ISO-SM` and `BM-ISO-LG` default to `hole_d = 18.0`, matching the Toyota
  `90560-12009` spacer basis. Production release uses the 18.0 mm bore; `hole_d = 0`
  is a non-release CAD override only.
- `FS-OVAL` has optional `relief_depth`; the old part must prove whether the
  relief is real, blind, through-cut, or only deformation.
- `FS-STRIP-L/R` default to no holes; retainer slots are separate steel detail
  unless the old rubber proves the rubber itself was pierced.
- Bump-stop models are rubber-only stretch-fit measurement placeholders. Free
  height is known, but rubber base footprint, bolt/stud pitch, relaxed
  through-hole or slot size, and strike geometry must come from the cleaned
  vehicle brackets and axle strike pads.
- The exhaust hanger model is hold-only until a sample or installed support
  measurements release thickness, side profile, and reinforcement detail.
