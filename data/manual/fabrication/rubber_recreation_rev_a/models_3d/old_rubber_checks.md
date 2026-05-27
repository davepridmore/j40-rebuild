# Old-Rubber Checks For 3D Model Closure

These checks are only needed when we are ready to release drilled holes, trim,
or mould details. The OpenSCAD files keep uncertain features as parameters.

## Why The Main Body Pads Are Undrilled

The main body pads are undrilled in the quote model because the rubber hole is
not the clamping feature. The bolt should clamp through a steel crush sleeve,
and the rubber hole only needs to clear that sleeve cleanly. The final bore is:

`final rubber hole = measured sleeve OD + 0.5 to 1.0 mm`

If the pad is drilled before the sleeve OD is known, a too-small hole can tear or
grab the sleeve, and a too-large hole can let the stack wander. A centre mark is
safe for quote/first article; final drilling is safe after the sleeve OD and
stack height are confirmed.

## Checks

- `BM-ISO-SM`: Measure old sleeve OD/ID/length, old rubber centre-hole diameter, whether the hole is centred or offset, top/bottom washer imprint diameter, and whether the old stack was one-piece or split.
- `BM-ISO-LG`: Measure old sleeve OD/ID/length, old rubber centre-hole diameter, whether the hole is centred or offset, top/bottom washer imprint diameter, and whether the old stack was one-piece or split.
- `FS-OVAL`: Confirm hole centre spacing, hole diameter, thickness, insert/boss OD, whether insert is bonded or loose, and whether the 36 x 18 relief is real or just deformation.
- `FS-STRIP-L`: Check whether old rubber has any real pierced holes or only retainer marks, whether ends are square or trimmed, actual thickness, and whether left/right are identical.
- `FS-STRIP-R`: Check whether old rubber has any real pierced holes or only retainer marks, whether ends are square or trimmed, actual thickness, and whether left/right are identical.
- `B-60010-LONG`: Do not use decayed rubber as the master. Measure bracket landing length/width, bolt pitch, bolt/hole size, strike-pad offset, loaded gap, and safe near-full-bump clearance.
- `B-60020-SHORT`: Do not use decayed rubber as the master. Measure bracket landing length/width, bolt pitch, bolt/hole size, strike-pad offset, loaded gap, and safe near-full-bump clearance.
- `B-60010-REAR-PAIR`: Do not use decayed rubber as the master. Measure bracket landing length/width, bolt pitch, bolt/hole size, strike-pad offset, loaded gap, and safe near-full-bump clearance.
- `EXH-HGR-90917`: If an old hanger exists, measure thickness, top hole, lower slot, side profile, reinforcement/insert, and installed pin/bracket spacing.
