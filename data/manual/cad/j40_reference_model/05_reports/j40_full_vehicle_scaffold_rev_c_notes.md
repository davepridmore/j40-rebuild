# J40 Full Vehicle CAD Scaffold Rev C - RHD Digital Twin Evidence Pass

This is a project-owned from-scratch CAD scaffold. It uses the CC-BY FJ40 Sketchfab references, the project photo inventory, public/commercial 3D model representations covered for project use, and Toyota online parts representations as visual and service-reference cues. Source files are not redistributed here unless a licensed/local asset is placed in the intake folder.

## Basis

- Toyota representative FJ40 dimensions: 3840 mm length, 1665 mm width, 1950 mm height, 2285 mm wheelbase.
- Open-source visual reference: 1976 Toyota Land Cruiser FJ40 by tonielpro520 on Sketchfab, CC Attribution 4.0.
- Additional open visual reference: Toyota Land Cruiser by Game Garage on Sketchfab, listed as Creative Commons Attribution, used for high-density material and interior/detail cues.
- Commercial visual/reference benchmarks: 3DModels.org Toyota Land Cruiser (J40) Hard Top 1979 and CGTrader Toyota Land-Cruiser J40 Hard Top BJ44V 1979 printable listing. Commercial coverage was confirmed by the project owner; this generator stores only project-owned procedural geometry and provenance metadata unless licensed assets are added locally.
- Toyota online parts representations: EPC body/interior groups and GR Heritage 40 parts list, used for factual part-name cues such as roof/rear ventilators, body mounts, bumper stays, rear combination lamp segmentation, brake tubes, wiper caps, mirror packing, and fuel inlet hose.
- Project-photo visual target: sand/beige diesel hardtop J40 with white roof, black bumper/trim, round auxiliary lamps, black window seals, side step boards, and mud-terrain tires.
- Project-specific identity cues: Punjab BSN 453 front plate stroke reference, front disc/Sumitomo-style caliper package from May 29 brake photos, and raised mud-terrain sidewall lettering panels.
- Driving layout: right-hand drive for left-side traffic. Positive Y is the driver side in this coordinate system.
- This scaffold does not extract or reproduce hidden source mesh data.
- Source inventory: `data/manual/cad/j40_reference_model/05_reports/j40_full_vehicle_scaffold_rev_c_online_reference_inventory.csv`.

## Outputs

- `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_scaffold_rev_c.scad`
- `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_scaffold_rev_c.FCMacro`
- `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_scaffold_rev_c_orthographic.svg`
- `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_scaffold_rev_c_orthographic.png`
- `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_scaffold_rev_c_orthographic.dxf`
- `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_scaffold_rev_c.gltf`
- `data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_scaffold_rev_c_parts.csv`
- `data/manual/cad/j40_reference_model/05_reports/j40_full_vehicle_scaffold_rev_c_online_reference_inventory.csv`
- `data/manual/cad/j40_reference_model/05_reports/j40_as_fitted_route_model_coverage_20260531.csv`
- `data/manual/cad/j40_reference_model/05_reports/j40_3dmodels_gallery_visual_cues.json`

## Current CAD Level

- L0 envelope: boxes/cylinders that locate major vehicle systems.
- L1 reference: named CAD primitives for body, chassis, running gear, engine bay, hardtop, and interior.
- L2 visible-detail scaffold: grille slots/lights, bumper/tow points, hood ribs/latches, hardtop panels/windows/gutters, door hinges/handles/mirrors, right-hand drive dashboard/gauges/switches, seats/belts/pedals, engine-bay accessories/hoses, suspension brackets, shocks, rims, tire lugs, hubs, and body pressings.
- L3 exterior material references: separated grille mesh and TOYOTA lettering, fender-top lamps, side louvers, beltline trim, hardtop sliding-window mullions, classic rounded rear-quarter/back-door glass, rubber window radius gaskets, faceted black fender flares, step-board tread strips, mud flaps, rear barn-door seals/hinges/handles, spare-wheel spoke/highlight parts, wiper hardware, roof-gutter rivets, wheel-face vents, tire sidewall ticks, bumper bolts, license-plate screws, rear lamps, and spare-carrier latch plates.
- L4 gallery-shaped surfaces: closed crowned hood, rolled hood lip, raked windshield surface, inset grille surround, sloped front fender skins, rolled fender crowns, tapered door/rear-quarter skins, tapered hardtop side skins, hardtop rear-corner facets, body-color wheel-arch facets, and crowned hardtop roof skin.
- Rev C online-reference details: roof ventilator lid/hinge/handle, rear hardtop ventilator louvers, classic rounded rear hardtop side windows and split rear-door glass, hardtop-to-body joins, front clip/tub joins, body-mount pucks and stands, front/rear bumper stays, hood underside bracing and prop rod, hood lock receiver, brake proportioning valve and tube clips, fuel sub-inlet/vent hoses, separated amber/red/clear rear combination lamp lenses, and interior gauge/grab-handle detail.
- Digital-twin evidence pass: front disc rotors, Sumitomo-style caliper envelopes, caliper hose/fitting datums, BSN 453 plate strokes, and sidewall lettering panels are tied to project photos rather than generic J40 references.
- Measurement-photo datum pass: cooling-pipe fabrication sample, radiator/front-support pickups, installed battery, battery tray, and removed bump-stop sample evidence now has named datum geometry for follow-up measurement closure.
- Visual geometry pass: glTF and orbit-viewer box primitives use conservative chamfers on body, hardtop, front detail, interior, chassis, and running gear pieces to reduce the blocky placeholder look while preserving named part boundaries.
- Right-hand drive references: right-side steering wheel/column, right pedal box, right-firewall brake booster/master cylinder, clutch master, lower steering shaft, steering box, pitman arm, drag link, tie rod, steering damper, and driver-side handbrake reach. The pedal order remains clutch-brake-accelerator across the right footwell.
- L3 specific-item references: rear parking-brake cable attachment hardware, equalizer, clevises, return springs, and frame/axle clips.
- As-fitted route scope: every route row from `data/manual/cad/j40_reference_model/05_reports/j40_as_fitted_route_model_scope_20260531.csv` has a visible named placeholder or support/clearance primitive covering electrical power, starter/charging, engine controls, front lighting, A/C electrical, cabin HVAC, bulkhead, rear body loom, brake hydraulics, parking brake, fuel, A/C refrigerant, cooling, control cables, speedometer cable, drains, exhaust heat, and shared routing supports.
- Route generator coverage: 28 of 28 as-fitted route rows are represented by 43 named `as_fitted_routes` parts. Coverage report: `data/manual/cad/j40_reference_model/05_reports/j40_as_fitted_route_model_coverage_20260531.csv`.
- Pakistan purchase BOM: 30 route-linked buy rows from `data/manual/j40_as_fitted_route_pakistan_purchase_bom_20260531.csv` are read into generated route notes so the 3D model carries the local buy IDs/specs.
- Mechanical-soundness references: fan/radiator, steering-lock/brake-hose, prop-shaft, exhaust heat, and pedal/column/HVAC clearance volumes are visible as non-release L2 checks.
- Routing references: brake lines, parking-brake cables, battery cable, fuel line, filler neck, exhaust, prop shafts, and measurement datum bars.
- Not fabrication release: mounting holes, curvature, exact frame sweep, body flange geometry, and bracket datums still need physical measurements from the actual truck.

Total named parts: 1298
