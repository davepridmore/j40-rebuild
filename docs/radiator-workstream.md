# Radiator Workstream

- Created: 2026-05-29
- Workstream ID: `radiator`
- Parent phases: `05_mechanical_baseline`, `03b_chassis_fixing`
- Vehicle: 1978 Toyota Land Cruiser J40 with 2H/HJ47-style cooling layout as the working basis
- Primary gates: `RAD-RET-001`, `RAD-CAPTURE-001`, `RAD-SHOP-001`, `RAD-INSTALL-001`
- Related docs: [bilal-ganj-front-cooling-ac-purchase-list-20260714.md](bilal-ganj-front-cooling-ac-purchase-list-20260714.md), [engine-radiator-recore-release-20260529.md](engine-radiator-recore-release-20260529.md), [front-engine-bay-mounting-fabrication-plan-20260508.md](front-engine-bay-mounting-fabrication-plan-20260508.md), [fabrication-handoff-index.md](fabrication-handoff-index.md), [amir-refurbishment-video-gates-20260529.md](amir-refurbishment-video-gates-20260529.md), [photo-catalog.md](photo-catalog.md), [component-jobs-photo-reconciliation.md](component-jobs-photo-reconciliation.md)

## Decision

Treat the radiator as a dedicated workstream because it crosses three separate scopes: vehicle-side front-support fabrication, radiator shop recore/new-build decision, and final cooling-system fitment.

**Status update 2026-07-22:** the owner reports the second/right-side radiator retention arm has been welded in, and the current front-structure photo shows both upright arms. Close the fabrication action but keep installation acceptance open. Inspect the new weld and heat-affected metal, compare the arms for height/plane/hole alignment, dry-fit the actual radiator with rubber isolation, verify fan/shroud/hose/bonnet clearance, then restore primer/top protection. Do not re-fabricate the arm unless that inspection or dry fit finds a defect.

The reason for the front-of-car fabrication is to keep the radiator properly located in the vehicle. The immediate fabrication job was not a radiator-shop repair to the core or tanks; it was the missing/right-side vehicle-side retention piece that matches the existing side and holds the radiator in place. The earlier measurements and template remain the as-built checking basis rather than an instruction to make another arm.

The radiator body itself remains sample-controlled. Send the old engine radiator with Amir as the master pattern for pressure/flow testing. Recore it if the tanks, necks, drain, cap seat, and brackets are sound; otherwise build a new copper/brass radiator by sample. Do not buy a random listing radiator from year/model alone.

### Rev D Thermal Release — supersedes nominal stack assumptions

The current controlled fabrication handoff is [J40 Integrated Cooling Pack Fabricator Specification — Rev D](J40-integrated-cooling-pack-fabricator-specification-rev-c.md). It supersedes earlier nominal front-stack assumptions, including a fixed `530 × 435 × 64 mm` core, a dual-9-inch/free-air-fan target, and any arrangement that puts the turbo intercooler in front of the condenser/radiator.

Build the engine radiator and A/C condenser as a measured-fit **main path** only: grille → A/C pusher frame → condenser → `≥15 mm` gap → radiator → sealed full-face shroud → engine-driven puller. Final core selection must prove `≥115 kW` continuous heat rejection and `≥130 kW` for ten minutes at `50°C` dry-bulb grille inlet with A/C on; also prove a `52°C` ten-minute heat soak and hot restart. The engine-driven puller must deliver `≥9,000 m³/h` installed at `125 Pa` and `1,500 rpm`; the independently fused/relayed A/C pusher(s) must deliver `≥3,000 m³/h` installed at `75 Pa` and `13.5 V`.

The future turbo charge cooler is a separate side/wing system, not a third layer in the main pack: sealed fresh inlet → side charge cooler → dedicated `≥2,500 m³/h` installed fan at `75 Pa` → separate hot exit. Its release targets are `≥15 kW` rejection at the Rev D charge-air duty, manifold IAT `≤80°C`, and complete charge-route pressure loss `≤10 kPa` (target `≤7 kPa`). After all Rev D thermal/airflow gates pass, cooling must not force boost derate inside the `150 bhp` crank thermal-design envelope. This is not approval of 150 bhp, arbitrary boost, fuelling, turbo-map speed, EGT, drive-pressure or driveline capacity; turbo calibration still starts at `5-7 psi`, with `8-10 psi` only after logged evidence.

If the aluminium radiator route is already in play, it is accepted only after dry-fit proves the core, tanks, necks, cap, drain, fan clearance, and hose layout are correct. Any added metal part must be a removable rubber-isolated adapter/cradle between the vehicle support and radiator mounting ears/rails, not a hard leg welded or bolted to the tank/core.

## Active Fabricated Part: `RAD-RET-001`

Source package: [front_radiator_two_side_retention_rev_a](../data/manual/fabrication/front_radiator_two_side_retention_rev_a/README.md)

Function: vehicle-side front support retention. This part's job is to locate and restrain the radiator in the car so vibration, hose tension, fan clearance, and body movement are controlled by proper lower pads plus side/top retention, not by a loose wire, one-sided bracket, or a hard leg attached to the radiator body.

Fabricate one mirror-side radiator retention post from the existing-side datum:

| Item | Working basis |
| --- | --- |
| Material | `4.0 mm` mild steel; prefer `50 x 50 x 4 mm` 90-degree angle/L-section if one leg matches the measured face |
| Main face | `48 mm` measured template basis |
| Upright height | `410 mm` |
| Developed main-face length | `618 mm` |
| Top screw return | `58 mm`, carried full-depth across the formed angle section |
| Chassis bridge allowance | `70 mm`, verify on right-side dry-fit |
| Outer saddle leg | `80 mm` |
| Fixing method | As built on 2026-07-22: second arm reported welded to the vehicle structure; inspect the weld and geometry, then confirm the radiator fastener/isolator stack before acceptance |
| Isolation | Rubber washer/bush/grommet stack at radiator screw as needed |

Release holds before final steel drilling:

- Transfer the existing-side top screw location to the missing/right side.
- Confirm the radiator ear lands without pulling the radiator out of plane.
- Confirm chassis/front-support width, through-bolt route, washer/crush-tube/spacer need, and cleaned metal condition.
- Confirm fan, shroud, belt, upper/lower hose, bonnet-close, and radiator removal clearance after tightening.
- Photograph the cardboard or flat-bar dry-fit with ruler before final drilling/coating.

## Missing-Side Application Sequence — Historical Fit/QA Basis

The arm is now reported installed. Retain this sequence only as the datum and dry-fit checklist for checking the as-built work; do not fabricate a duplicate unless the current arm fails inspection.

1. Set the radiator in its intended position first, sitting on the correct lower pads or temporary rubber spacers. Do not use hose tension to pull it into place.
2. Use the existing/good side as the datum for height, front-back plane, and top screw relationship.
3. Hold a cardboard or flat-bar template on the missing side and mark the radiator ear/top screw position while the radiator is relaxed.
4. Mark the lower saddle around the actual chassis/front-support section on that same missing side.
5. Check the fan-to-radiator gap before drilling. The holder must keep the radiator in the existing safe plane, not move it closer to the fan or belt.
6. Drill the top screw hole only after the template lands naturally on the radiator ear with rubber isolation in place.
7. Drill the through-bolt route only after both saddle legs sit cleanly over sound metal and any crush tube/spacer need is decided.
8. Tighten the holder, then shake-test the radiator by hand. The radiator should not rock, twist, or flex at the tanks/core.
9. Recheck hose sweep, fan clearance, bonnet clearance, and radiator removal/service access after tightening.

Success condition: the missing side now holds the radiator in the same plane as the existing side, with load going through the vehicle-side holder and rubber isolation rather than through an added leg on the radiator body.

## Photo Intake Gate: `RAD-CAPTURE-001`

Use the Google Photos picker to pull in the fresh radiator-detail photos, then classify and reconcile them against the component jobs.

Required radiator photo details:

| Area | Capture required |
| --- | --- |
| Old radiator identity | Wide photos showing the complete radiator, tanks, core, cap/filler neck, upper and lower necks, overflow nipple, drain, side rails, and bracket ears |
| Fabricated/missing support | Existing good side, missing/right side, extra old fabricated leg, top screw area, lower saddle/pad landings, and any wire-held or one-sided retention evidence |
| Measurements | Overall radiator height/width/thickness, core height/width/thickness, neck OD/angle, cap position, drain position, bracket hole centres, fan-to-core clearance |
| Failure evidence | Leaks, corrosion, blocked fins, cracked solder, weak tank seams, bad previous repairs, bent ears, worn isolators, and tank/core stress marks |
| Fitment context | Fan, pulley, shroud if fitted, hose sweep, front support holes, lower pads, bonnet-close zone, and nearby battery/power-carrier clearance |

After intake, update or verify:

- [photo-catalog.md](photo-catalog.md)
- [component-jobs-photo-reconciliation.md](component-jobs-photo-reconciliation.md)
- `data/manual/photo_inventory.csv`
- `data/manual/component_jobs_photo_reconciliation.csv`

### 2026-05-29 Picker Result

Import run: `20260529T224315`

The picker added five radiator/front-support photos and the catalog now classifies them as radiator evidence. `engine_radiator_recore_or_new_20260529` now reconciles as `direct_photo_evidence`.

| File | Use |
| --- | --- |
| [20260529_205200_gp_8G6ZKKEQ.jpg](../photos/20260529_205200_gp_8G6ZKKEQ.jpg) | Removed radiator sample with tape across the core/tank width. Good for overall sample layout and approximate width reference. |
| [20260529_205224_gp_aQYpMUyg.jpg](../photos/20260529_205224_gp_aQYpMUyg.jpg) | Soft close-up of lower side/mounting area. Supports capture of the old added leg/lower mount zone, but not final dimensions. |
| [20260529_205232_gp_eHbRrOaw.jpg](../photos/20260529_205232_gp_eHbRrOaw.jpg) | Side tank/bracket height view with tape. Good as a side-bracket span reference. |
| [20260529_205240_gp_C2r8CMBQ.jpg](../photos/20260529_205240_gp_C2r8CMBQ.jpg) | Closer side tank/bracket tape view. Supports the same height/side-bracket reference. |
| [20260529_214147_gp_4gfuofYQ.jpg](../photos/20260529_214147_gp_4gfuofYQ.jpg) | In-vehicle front-support, fan, pulley, and radiator-plane measurement context. Use this to keep the retention bracket from moving the radiator into the fan/belt envelope. |

Current read from these photos:

- The selected photos do support the reason for the front-of-car fabrication: the radiator needs proper vehicle-side retention so it stays located against vibration, hose tension, and fan-clearance movement.
- The removed radiator has usable sample geometry for width, side tank/bracket span, and lower/side mounting reference.
- The images are not enough to release exact final dimensions. Several tape views are soft and appear to use inch-side tape; before cutting or shop payment, capture final dimensions in `mm` with a clear ruler/tape and the bracket ears visible square-on.
- The photos still do not prove pressure-test result, flow condition, drain thread/style, cap pressure, neck OD/angle, overflow nipple OD, or final fan clearance after the retention part is tightened.

### 2026-05-29 Second Picker Result

Import run: `20260529T230220`

The picker added eight closer radiator condition photos. These are now classified as `engine_radiator_condition_closeups`.

| File | Use |
| --- | --- |
| [20260529_230003_gp_rliSbRjA.jpg](../photos/20260529_230003_gp_rliSbRjA.jpg) | Close core/fin condition view; soft, but shows the core surface is aged and dirty. |
| [20260529_230009_gp_BLX8dSWA.jpg](../photos/20260529_230009_gp_BLX8dSWA.jpg) | Best core overview in this batch; visible widespread fin dirt/flattening/blocked-looking areas. |
| [20260529_230017_gp_L23OD4nw.jpg](../photos/20260529_230017_gp_L23OD4nw.jpg) | Top/side edge context with a hose/cable crossing; useful for tank/edge condition context. |
| [20260529_230022_gp_BLo8HLwg.jpg](../photos/20260529_230022_gp_BLo8HLwg.jpg) | Soft side/core condition support photo. |
| [20260529_230035_gp_5oB8otKw.jpg](../photos/20260529_230035_gp_5oB8otKw.jpg) | Best added-leg/lower-mount evidence. Shows the extra support leg as a workaround attached around the radiator/mounting area. |
| [20260529_230040_gp_B5P2K9FA.jpg](../photos/20260529_230040_gp_B5P2K9FA.jpg) | Soft side/tank/core condition support photo. |
| [20260529_230044_gp_I9psm6Dw.jpg](../photos/20260529_230044_gp_I9psm6Dw.jpg) | Lower edge and mounting overview with the added leg and mounting tabs visible. |
| [20260529_230050_gp_ZqjySFHg.jpg](../photos/20260529_230050_gp_ZqjySFHg.jpg) | Soft side/core supporting condition photo. |

Current read from the second batch:

- The added leg still reads as a bad previous mounting workaround, not a design feature to reproduce.
- The core/fin face looks old, dirty, and partly flattened/blocked in the photos. That does not prove leakage, but it weakens the case for simple reuse.
- Treat `recore original radiator` or `build new copper/brass by sample` as the practical default path unless the radiator shop proves the existing core has good flow, no leaks, and sound tanks/necks/brackets.
- The photos do not show enough clear filler neck, cap seat, drain, neck OD/angle, or solder/joint detail to approve reuse visually.
- If the radiator shop can reuse the tanks/brackets, recore is preferred. If the added leg has stressed, cracked, or distorted the side tank/bracket area, build new by sample rather than patching around that damage.

## Shop Gate: `RAD-SHOP-001`

The shop release remains controlled by [engine-radiator-recore-release-20260529.md](engine-radiator-recore-release-20260529.md):

1. Pressure-test and flow-test the old radiator.
2. Recore original copper/brass unit if the tanks, necks, drain, cap seat, and brackets are reliable.
3. Build a complete new copper/brass radiator by sample if those parts are weak.
4. Bench pressure-test before return.
5. Send Amir's required video evidence before deposit, payment, or final collection.

## Online Buy Picks - 2026-05-29

Do not buy a complete radiator online from listing photos. The old radiator sample and the vehicle-side front-support/fan-clearance measurements still control the final radiator.

Safe online picks are limited to generic consumables and only where the size matches the final sample:

| Item | Pick | Decision |
| --- | --- | --- |
| Radiator hose clamps | Daraz `DreamsMart Pack of 2pcs Clamp 2 inches (32-51mm) Taiwan Stainless Steel Worm Drive` | Candidate for upper/lower hose clamp positions if the fitted hose OD lands within `32-51 mm`. Buy `2-3` packs only after hose OD is measured. Do not overtighten on aluminium or thin brass necks. |
| Radiator cap | Daraz `F.E.W. R125 Radiator Cap 0.9 kg/cm / 88 kPa` | Candidate only if the radiator shop confirms the old cap/filler neck is R125-style and `0.9 kg/cm` is the correct pressure. Do not buy before cap seat type is confirmed. |
| Coolant | Daraz `Guard Anti Rust & Anti Freeze Coolant 4L Green` | Candidate final-fill coolant only after the system is fully flushed and the radiator shop confirms compatible coolant for the repaired/new radiator. Do not mix with unknown old coolant. |

Items to avoid online for now:

- Complete radiator: fitment is not released.
- Furniture/corner angle brackets: not structural enough for the front retention piece.
- Aluminium window angle: wrong material/use for the vehicle-side radiator support.
- Door/weather-strip rubber: not the correct radiator isolation material.

Buy locally/by sample instead:

- `50 x 50 x 4 mm` mild-steel angle/L-section, about `1 m`, for the retention post if the leg matches the `48-50 mm` measured face.
- `3-5 mm` EPDM/SBR rubber sheet or washers/bushes for radiator isolation.
- M8/M10 class `8.8` or better through-bolt hardware only after the bracket dry-fit confirms hole size, chassis thickness, and crush-tube/spacer need.

## Install Gate: `RAD-INSTALL-001`

Close the radiator workstream only when:

1. The mirror-side retention post or approved adapter/cradle is fabricated, deburred, protected, and dry-fitted.
2. The radiator sits on proper lower pads and side/top mounts, not on the extra fabricated leg from the bad previous installation.
3. Upper/lower hoses fit without kinks, rub, clamp-over-edge problems, or forced alignment.
4. Fan and belt clearance is safe after tightening and through engine movement.
5. New radiator cap, upper/lower hoses, overflow hose, and clamps are installed or explicitly staged with the radiator job.
6. System is filled, bled, warmed to thermostat opening, checked for leaks, and pressure-tested after install.
7. Final photos show bracket, radiator, hoses, cap, drain, fan clearance, and no tank/core stress.

## No-Go Conditions

- Final radiator install before the missing/right-side retention part is dry-fit and photographed.
- Copying the old extra fabricated leg as the main support design.
- Hard-clamping, drilling, or welding into an aluminium radiator tank/core without radiator-shop approval.
- Buying a random FJ40/BJ40/HJ47 radiator without proving hose-neck layout, cap position, drain, bracket locations, core envelope, and fan clearance.
- Coating the front support area before radiator saddle holes, through-bolt route, and needed bracket tabs are resolved.
