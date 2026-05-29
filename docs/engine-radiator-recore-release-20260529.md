# Engine Radiator Recore / Replacement Release - 2026-05-29

Purpose: lock the repair route for the engine coolant radiator after the removed radiator was clarified separately from the A/C condenser.

## Decision

Use the old engine radiator as the master pattern and send it with Amir to a radiator shop for pressure/flow testing. The preferred repair is:

1. If the tanks, filler neck, hose necks, drain, and mounting brackets are sound: recore the original radiator with a new heavy-duty copper/brass core.
2. If the tanks, necks, or brackets are weak, cracked, plastic, badly corroded, or poorly repaired: build a complete new copper/brass radiator from the old radiator as the pattern.
3. Do not buy a random FJ40/BJ40/HJ47 radiator by listing photo alone. The fitted 2H/HJ47-style hose layout, fan clearance, cap position, and bracket locations control the part.

Important fitment finding: the front-of-car fabrication is required to keep the radiator properly located in the vehicle. The extra fabricated support leg on the old radiator is evidence that the radiator was not installed correctly. Use the old radiator for hose-neck, tank, cap, drain, core-envelope, and bracket-location reference, but do not blindly copy the extra leg as the final support design. Final installation should sit on the proper lower pads and side/top mounts; if the vehicle-side mounts are missing, bent, or misaligned, fix the vehicle bracket/retention separately.

## If The Aluminium Radiator Has Already Been Bought

Do not fabricate another random leg just because the aluminium radiator does not land on the existing supports. The safe contingency is a removable adapter/cradle tied into the existing radiator retention work.

Use this order:

1. Test-fit the aluminium radiator with no forced bolts and no hose tension.
2. If the lower pads, side mounts, and top restraint line up: use the existing/fabricated two-side retention arms with rubber isolation.
3. If the radiator is close but the tabs/ears do not land: fabricate a separate bolt-on adapter plate, crossbar, saddle, or spacer bracket between the vehicle support and the radiator mount. This adapter must be rubber-isolated and removable.
4. If the radiator core, tanks, necks, cap, drain, fan clearance, or hose layout are wrong: reject the radiator for this vehicle rather than building structure around it.

The adapter/cradle must support the radiator body without loading the aluminium tanks or core. Do not weld or drill the radiator unless a radiator fabricator approves the exact reinforced mounting area.

Payment/release is blocked until Amir sends the required video evidence in [amir-refurbishment-video-gates-20260529.md](amir-refurbishment-video-gates-20260529.md).

## Shop Instruction

Amir should give the shop the old radiator and ask for this exact scope:

```text
Please pressure-test and flow-test this engine radiator. Use it as the exact pattern for a 1978 Toyota Land Cruiser J40 with 2H/HJ47-style cooling layout.

If the tanks, filler neck, hose necks, drain, and brackets are reusable, recore it with a new heavy-duty copper/brass core. If any tank/neck/bracket is not reliable, quote a complete new copper/brass radiator made from this sample.

Keep the same overall height, width, thickness envelope, upper/lower hose neck positions and diameters, radiator cap/filler neck position, overflow nipple, drain plug, mounting tabs, lower rubber/pad landings, and fan/shroud clearance. Bench pressure-test before return.

Note: the added fabricated support leg on the old radiator is a warning sign from the bad previous installation, not a feature to copy as the main support. Show how the repaired/new radiator will locate on the proper lower pads and side/top mounts. If the car-side support is wrong, quote that as a separate vehicle bracket fix.
```

## Video Before Payment

Before any deposit, payment, or final collection, Amir must send the radiator videos defined in [amir-refurbishment-video-gates-20260529.md](amir-refurbishment-video-gates-20260529.md): old sample identity, measurements, shop decision, pressure/leak test, core/build proof, and final acceptance video.

## Required Measurements / Photos

Capture these before the radiator leaves the vehicle/workshop:

| Check | Requirement |
| --- | --- |
| Overall envelope | Height, width, and thickness in mm |
| Core | Core height, width, row/thickness, and fin condition |
| Upper neck | OD, angle, center position from top/side datums |
| Lower neck | OD, angle, center position from bottom/side datums |
| Filler neck | Cap seat type, cap pressure, cap position |
| Overflow | Nipple OD and direction |
| Drain | Drain plug presence, position, thread/style |
| Mounts | Side tabs, top holes, lower pad landings, shroud holes |
| Extra fabricated leg | Photograph and measure it as evidence of the bad old installation, but do not treat it as the intended final mounting method |
| Clearance | Fan blade to core/tank clearance after dry-fit |

## Acceptance Criteria

- No leaks on bench pressure test.
- Flow-test passes, or shop confirms the new core removes the blockage risk.
- Radiator dry-fits without pulling the front support bracket out of alignment.
- Radiator is retained by proper lower pads and side/top mounts, not by the extra fabricated leg from the bad old installation.
- If an aluminium radiator is used, any added metal piece is a removable rubber-isolated adapter/cradle between the vehicle support and radiator mount, not a hard leg attached to the tank/core.
- Fan and belt clearance remains safe through engine movement.
- Upper/lower hoses fit without kinks, rub, or clamp-over-edge problems.
- New radiator cap, upper/lower hoses, overflow hose, and clamps are installed with the radiator job.
- Cooling system is filled, bled, warmed to thermostat opening, checked for leaks, and pressure-tested after install.

## Linked Work

- `radiator`: dedicated control workstream in [radiator-workstream.md](radiator-workstream.md).
- `part_mech_radiator_hose_set`: upper/lower/overflow hose and formed coolant pipe package.
- `part_mech_radiator_cap`: replace with the radiator job.
- `front_radiator_two_side_retention_fabrication_20260508`: dry-fit before final radiator release so the radiator is retained on both sides without stressing the tanks.
- `engine_cooling_pipe_fabrication_samples`: keep the formed coolant pipe dry-fit/pressure-test separate from the radiator shop scope.

## Local Quote Route

Amir should quote Lahore radiator shops first, using the old radiator as the sample. Master Radiators and Kor Tech Radiator are candidate quote routes, but any capable local radiator shop is acceptable if they can recore/build copper/brass by sample and bench pressure-test before return.
