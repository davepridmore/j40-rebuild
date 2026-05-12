# Chassis Bracket Analysis Register - 2026-05-08

Source CSV: [data/manual/chassis_bracket_analysis_register_20260508.csv](../data/manual/chassis_bracket_analysis_register_20260508.csv)

This is the actual bracket register seeded from current local photos. The May 12 user and Google Photos sets now include the measured left chassis-attached radiator bracket/upright, front-support hole-field, fan/belt, removed-radiator tab, and battery-side structure context. The front-support and battery-stand concepts can move into template work, but final release still needs labelled hole-centre, hole-diameter, and dry-fit photos.

## Current Register

| ID | Station | Function | Evidence state | Current read | Decision / gate |
| --- | --- | --- | --- | --- | --- |
| `CBR-001` | Front support, left chassis radiator side | Left chassis-attached radiator bracket | Direct measurement photo | May 12 21:31-21:32 images show the existing left-side bracket/upright height, top-tab offset, front opening, and fan/pulley clearance. | Use the measured left bracket as the datum for a similar right-side radiator bracket. Blocks final primer/Raptor until template release. |
| `CBR-010` | Front support, left chassis radiator side reference | Left radiator bracket measurement datum for right-side fabrication | Direct measurement photo | Dedicated left reference set is now visible in the Chassis Fixing register. | Build the right-side template from this reference, then validate actual right-side pickup metal before cutting steel. |
| `CBR-002` | Front support, right radiator side to fabricate | Right-side radiator retention bracket to fabricate | Direct context | The measured left bracket photos and removed-radiator tab photos now give a starting geometry; the right-side pickup condition still needs dry-fit proof. | Transfer the left geometry into a right-side template, verify isolator contact and clearance, then release or repair. |
| `CBR-003` | Front support, lower crossmember | Lower radiator support or lower pickup holes | Direct context | May 12 images show a usable-looking hole field; hole condition, metal thickness, and lower load path still need measurement. | Inspect and measure before using or repairing lower pickups. |
| `CBR-004` | Front support, radiator/fan side | Radiator/fan/belt/hose/steering/exhaust clearance envelope | Direct photo | Packaging constraints are clearer, including fan/pulley and battery-side steering/exhaust/alternator clearance. | Do not let new brackets pull the radiator toward the fan, stress hoses, or crowd steering/exhaust/service access. |
| `CBR-005` | Engine bay, battery-side inner wing | Battery top clamp or crossbar | Partial direct context | Battery-side structure context is better, but installed battery, top clamp path, and bonnet clearance still need checking. | Inspect top restraint after tray base support is proven. |
| `CBR-006` | Engine bay, battery-side inner wing | Battery tray base, feet, and support legs | Partial direct context | May 12 photo starts the tray/stand structure read, but underside feet, cracks, welds, and exact lower pickup points are not proven. | Build/reinforce a separate battery stand tied into real structure; still blocks coating if welded pickups are needed. |
| `CBR-007` | Engine bay, battery-side inner wing | MIDI fuse plate and master cutoff carrier pickups | Hardware and partial vehicle context | Hardware is documented and May 12 adds structure/clearance context; vehicle-side pickup remains unmeasured. | Mock up and design carrier tied into tray support/adjacent structure. Blocks coating if welded pickups are needed. |
| `CBR-008` | Front support | Auxiliary holes, tabs, and clip points | Direct context | Front-support hole fields are clearer, but each hole/tab still needs a proven function. | Assign every hole/tab before welding or deleting anything. |
| `CBR-009` | Front engine bay | Added structure layout for radiator retention and battery stand | New direct photo | May 12 images are enough to start a two-template concept: right-side radiator bracket from the measured left datum plus a separate battery tray stand. | Template in cardboard/flat bar before cutting steel; do not combine radiator and battery load paths into one flexible bracket. |

## Image Evidence Used

| Area | Useful photos | Register use |
| --- | --- | --- |
| Radiator/front support | `20260422_004423_gp_B1N5ThVw`, `20260422_004429_gp_4emWbTrA`, `20260422_004436_gp_yjCPMWTg`, `20260430_215957_gp_2iBbUagw`, `20260430_220004_gp_C9oYiYmA` | Direct enough to prove a front-support/radiator retention problem and define constraints. Still needs ruler photos for hole centres, offsets, side symmetry, and final clearance. |
| Left radiator bracket measurement datum | `20260512_213129_gp_IVnd8hWQ`, `20260512_213144_gp_2rlycKHA`, `20260512_213214_gp_xZKluAkg`, `20260512_100000_user_front_support_radiator_pickups_context` | Shows the existing left chassis-attached radiator bracket/upright with tape-measure height, top-tab offset, front opening, and fan plane. Use as the reference for the right-side bracket template. |
| May 12 radiator/upright context | `20260512_100000_user_front_support_radiator_pickups_context`, `20260512_073210_gp_zP427O2A`, `20260512_073303_gp_hNyAiN1g`, `20260512_073314_gp_GyAXZWBg`, `20260512_073547_gp_SNtwIVyA` | Shows radiator plane, fan/pulley clearance, vertical upright/top hole, front/lower support hole field, and engine-front packaging. Good enough for template layout; final hole centres and diameters still need confirmation. |
| Battery location / stand context | `20260317_235229`, `20260317_235232_gp_3Ojs4Rag`, `IMG-20260331-WA0004`, `20260512_100100_user_battery_side_tray_structure_context` | Enough to start the battery stand/load-path concept and clearance constraints. Still not enough to release tray feet, lower support legs, or welded pickup details. |
| MIDI/cutoff hardware | `20260411_143125`, `20260411_143135`, `20260420_221819_gp_YV69fbvA` | Hardware and packaging context for the battery-side carrier. Vehicle-side mounting points still require mock-up. |

## Measurements And Photos Still Required

Confirm these before any fabrication release:

1. Left reference bracket and radiator side flanges with labelled hole diameters, hole centres, edge distance, broken/missing tabs, and current wire path.
2. Right-side template dry-fit using the left reference geometry, with actual right-side pickup holes measured rather than blindly mirrored.
3. Front support and lower crossmember holes around the radiator, both sides, after cleaning enough to see cracks, oval holes, and thin edges; include the May 12 visible vertical upright top hole and its base attachment.
4. Closest fan-to-radiator clearance with radiator sitting in its current plane.
5. Battery length, width, height, terminal orientation, top clamp path, and bonnet clearance.
6. Battery tray top, side, front, rear, and underside with ruler: tray edges, feet, legs, cracks, rust, drain path, and possible lower brace route.
7. Battery stand template photos: cardboard or flat-bar tray perimeter, lower/inner pickup points, gusset directions, and clearance to steering shaft, alternator, exhaust, hoses, and service tools.
8. Cardboard mock-up for the `190 x 150 mm` MIDI plate plus cutoff body near the installed battery, including cable lug sweep and service access.
9. Every front-support auxiliary hole/tab labelled with intended function: radiator, line clip, harness clip, earth, exhaust, cable support, battery stand, no-refit, or unknown.

## Release State

The radiator job can proceed to right-side template layout now using the May 12 measured left bracket/upright reference, but it cannot be cut or welded until the right-side dry-fit, side-to-side pickup measurements, and lower-support ruler photos are captured.

The battery tray and battery-side MIDI/cutoff carrier can now move from pure location scouting to a tray-stand concept, but they still cannot be released from the current photos alone. The existing images improve the structure read; they do not prove tray strength, underside feet, or final pickup geometry.
