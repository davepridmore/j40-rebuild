# J40 Full Vehicle CAD Scaffold Rev B - LHD Hardtop Gallery Shape Pass

This is a project-owned from-scratch CAD scaffold. It uses the CC-BY 1976 FJ40 Sketchfab model, the project photo inventory, and public 3DModels.org preview renders as visual references, without extracting or copying source mesh data.

## Basis

- Toyota representative FJ40 dimensions: 3840 mm length, 1665 mm width, 1950 mm height, 2285 mm wheelbase.
- Open-source visual reference: 1976 Toyota Land Cruiser FJ40 by tonielpro520 on Sketchfab, CC Attribution 4.0.
- Commercial visual benchmark only: Toyota Land Cruiser (J40) Hard Top 1979 on 3DModels.org, using the 12 public gallery renders visible on the product page for exterior silhouette and detail targets such as separated materials, grille/trim/lamp treatment, hardtop glazing, side vents, fender flares, rear-door hardware, spare-carrier presentation, roof crown, hood crown, fender crown, side taper, rear corner radius, and orthographic front/side/top checks. No mesh data, paid asset files, or source geometry are copied.
- Project-photo visual target: sand/beige diesel hardtop J40 with white roof, black bumper/trim, round auxiliary lamps, black window seals, side step boards, and mud-terrain tires.
- Driving layout: left-hand drive. Negative Y is the driver side in this coordinate system.
- This scaffold does not extract or reproduce hidden source mesh data.

## Outputs

- `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_b/j40_full_vehicle_scaffold_rev_b.scad`
- `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_b/j40_full_vehicle_scaffold_rev_b.FCMacro`
- `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_b/j40_full_vehicle_scaffold_rev_b_orthographic.svg`
- `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_b/j40_full_vehicle_scaffold_rev_b_orthographic.png`
- `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_b/j40_full_vehicle_scaffold_rev_b_orthographic.dxf`
- `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_b/j40_full_vehicle_scaffold_rev_b.gltf`
- `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_b/j40_full_vehicle_scaffold_rev_b_parts.csv`
- `data/manual/cad/j40_reference_model/05_reports/j40_3dmodels_gallery_visual_cues.json`

## Current CAD Level

- L0 envelope: boxes/cylinders that locate major vehicle systems.
- L1 reference: named CAD primitives for body, chassis, running gear, engine bay, hardtop, and interior.
- L2 visible-detail scaffold: grille slots/lights, bumper/tow points, hood ribs/latches, hardtop panels/windows/gutters, door hinges/handles/mirrors, LHD dashboard/gauges/switches, seats/belts/pedals, engine-bay accessories/hoses, suspension brackets, shocks, rims, tire lugs, hubs, and body pressings.
- L3 exterior material references: separated grille mesh and TOYOTA lettering, fender-top lamps, side louvers, beltline trim, hardtop sliding-window mullions, rubber window corner caps, faceted black fender flares, step-board tread strips, mud flaps, rear barn-door seals/hinges/handles, spare-wheel spoke/highlight parts, wiper hardware, roof-gutter rivets, wheel-face vents, tire sidewall ticks, bumper bolts, license-plate screws, rear lamps, and spare-carrier latch plates.
- L4 gallery-shaped surfaces: closed crowned hood, rolled hood lip, raked windshield surface, inset grille surround, sloped front fender skins, rolled fender crowns, tapered door/rear-quarter skins, tapered hardtop side skins, hardtop rear-corner facets, body-color wheel-arch facets, and crowned hardtop roof skin.
- Visual geometry pass: glTF and orbit-viewer box primitives use conservative chamfers on body, hardtop, front detail, interior, chassis, and running gear pieces to reduce the blocky placeholder look while preserving named part boundaries.
- LHD-specific references: left steering wheel/column, left pedal box, left-firewall brake booster/master cylinder, clutch master, lower steering shaft, steering box, pitman arm, drag link, tie rod, and steering damper.
- L3 specific-item references: rear parking-brake cable attachment hardware, equalizer, clevises, return springs, and frame/axle clips.
- Routing references: brake lines, parking-brake cables, battery cable, fuel line, filler neck, exhaust, prop shafts, and measurement datum bars.
- Not fabrication release: mounting holes, curvature, exact frame sweep, body flange geometry, and bracket datums still need physical measurements from the actual truck.

Total named parts: 1042
