# Old-Rubber Checks For 3D Model Closure

These checks are only needed when we are ready to release drilled holes, trim,
or mould details. The OpenSCAD files keep uncertain features as parameters.
For the main body pads, the remaining uncertainty is local vehicle fit only; it
does not reopen the released Toyota spacer basis, sleeve length, or 18.0 mm bore.

## Main Body Pad Bore Spec

The main body pads now have a released first-article bore. The rubber hole is
not the clamping feature; the bolt clamps through a steel crush sleeve, and the
rubber hole only clears that sleeve cleanly. The release bore is:

`final rubber hole = Toyota 90560-12009 style sleeve clearance, 18.0 mm nominal`

The best current release basis is Toyota `90560-12009`, the body-mount spacer
listed at `L=48.1 mm`. Field evidence from an original Toyota mount stack reports
the OE tube as slightly over `17 mm` OD and the matching lower cushion centre
hole as `18 mm`; aftermarket `16 mm` tube is specifically smaller/sloppier.

Use `18.0 mm` as the first-article rubber bore for the main body pads. Source
genuine Toyota `90560-12009` spacers if possible. If fabricated locally, copy an
old/OE spacer, not arbitrary tube stock, and reject `16 mm` OD tube unless a
dry-fit proves it does not let the stack wander.

The measurements to collect on the vehicle side are the ones only the old parts
can answer: whether this truck has the expected six-sleeve mount family, the
old/OE sleeve OD to copy if genuine spacers cannot be sourced, washer/cup imprints,
landing footprint, and one dry-fit stack check.

## Checks

- `BM-ISO-SM`: Local-fit check only: confirm Toyota 90560-12009 style spacer or old sleeve is present; caliper-check old/OE sleeve OD/ID only if a local machinist must copy it; measure top/bottom washer imprint diameter and whether the old stack was one-piece or split.
- `BM-ISO-LG`: Local-fit check only: confirm Toyota 90560-12009 style spacer or old sleeve is present; caliper-check old/OE sleeve OD/ID only if a local machinist must copy it; measure top/bottom washer imprint diameter and whether the old stack was one-piece or split.
- `FS-OVAL`: Confirm hole centre spacing, hole diameter, thickness, insert/boss OD, whether insert is bonded or loose, and whether the 36 x 18 relief is real or just deformation.
- `FS-STRIP-L`: Check whether old rubber has any real pierced holes or only retainer marks, whether ends are square or trimmed, actual thickness, and whether left/right are identical.
- `FS-STRIP-R`: Check whether old rubber has any real pierced holes or only retainer marks, whether ends are square or trimmed, actual thickness, and whether left/right are identical.
- `B-60010-LONG`: Caliper the May 29 removed samples and removed metal fixture: rubber body length/width, through-hole pitch/diameter, central fixture/channel size, vehicle bracket fit, strike-pad offset, loaded gap, and safe near-full-bump clearance.
- `B-60020-SHORT`: Caliper the May 29 removed samples and removed metal fixture: rubber body length/width, through-hole pitch/diameter, central fixture/channel size, vehicle bracket fit, strike-pad offset, loaded gap, and safe near-full-bump clearance.
- `B-60010-REAR-PAIR`: Caliper the May 29 removed samples and removed metal fixture: rubber body length/width, through-hole pitch/diameter, central fixture/channel size, vehicle bracket fit, strike-pad offset, loaded gap, and safe near-full-bump clearance.
- `EXH-HGR-90917`: If an old hanger exists, measure thickness, top hole, lower slot, side profile, reinforcement/insert, and installed pin/bracket spacing.
