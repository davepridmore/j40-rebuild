# J40 RHD Centre 9-inch LCD / HVAC Fascia - Rev D

Rev D starts with the owner's actual right-hand-drive dashboard photograph and makes the centre change explicit: the entire protruding ashtray is removed, the adjacent radio openings are absorbed, and the combined zone becomes one continuous flat body-colour face. The glovebox/instruction panel and speedometer/instrument pressing stay original.

## Visual issue rule

Every dashboard design revision must be applied to both owner photographs: the assembled-dashboard view for original context, driver sight line and steering-wheel occlusion, and the straight-on bare-shell view for an unobstructed component-count and placement check. The two views must show the same fascia, LCD, seven-selector arrangement, hazard control and two A/C outlets. If a component is hidden by the steering wheel in the assembled view, the bare-shell view controls its location and count.

Both A/C outlets must be conspicuous in every issued visual: one removable, hose-fed directional eyeball vent below each lower corner of the centre fascia. They are separate under-dash brackets, not openings in the CNC fascia.

## Locked visual and fabrication scope

- Delete the complete ashtray door, body, lip, seam and recess. No ashtray outline or separate blank remains in the finished face.
- Remove or cover the separate radio openings and surround within the same centre-zone removal boundary.
- Form one flat, nearly flush CNC fascia across that combined zone. Nominal quotation envelope: 275 x 225 x 1.5 mm CR4 steel; the signed vehicle template controls the production contour.
- Use a true 9-inch 16:9 active-image reference: 199.2 x 112.1 mm, 228.6 mm diagonal. Nominal aperture: 202 x 115 mm. Nominal bezel envelope: 230 x 132 mm. The actual LCD manufacturer's drawing controls every final screen dimension.
- Fit the seven purchased 22 mm industrial rotary selectors: four in the original right-hand 2 x 2 positions and three below the LCD. Hazard remains a separate red pushbutton.
- Put two directional A/C eyeball outlets on separate reversible brackets below the dashboard, one each side of the centre insert. Preferred hose-neck target is 63.5 mm / 2.5 inch after actual vent and hose measurement.
- Finish the fascia in low-gloss body colour with a restrained thin black LCD bezel. Preserve the original dashboard character outside the centre removal boundary.

## Exact control positions

All positions are viewed from the cabin.

Right of the speedometer, original 2 x 2 cluster:

- Upper-left: WIPERS — 3-position, OFF / LOW / HIGH.
- Upper-right: LIGHTS — 3-position, OFF / SIDE / HEAD.
- Lower-left: SPOTS — 2-position, OFF / ON; existing right-dash hole 3 and relay T5.
- Lower-right: AUX — 2-position, OFF / ON; B2 auxiliary control.

Under the LCD, left to right:

- Left: BLOWER — 3-position, OFF / LOW / HIGH.
- Centre: A/C REQUEST — 2-position, OFF / ON.
- Right: FUEL STOP / CONTROL — 2-position, provisional pending device and live shutdown proof.
- Far-right: separate red HAZARD pushbutton; not one of the seven selectors.

Indicators remain on the OEM stalk.

## Electrical rules

- Every selector commands a protected relay/control circuit; no selector directly carries a high-current lamp, blower, clutch or accessory load.
- Frozen relay baseline is T1 low beam, T2 high beam, T3 horn, T4 condenser fan, T5 spot lamps, B1 A/C clutch and B2 auxiliary accessory.
- The blower uses a dedicated HVAC control/relay/resistor circuit sized from the selected blower's measured load. T1 and T2 are lighting relays and must not be used for blower speeds.
- A/C REQUEST may energise B1 only through the thermostat / trinary / pressure-protection chain. Condenser-fan behaviour through T4 is proved with the final HVAC hardware.
- FUEL STOP / CONTROL remains a release HOLD until the actual device and terminals are identified and key-OFF shutdown is proved with the engine running. Retain the manual diesel stop cable.

Evidence basis: data/manual/workbook_tabs/electrical_master.csv, data/manual/reference_projects_and_ideas.csv, data/manual/expenses.csv, data/manual/electrical_diagram_reconciliation_20260518.csv and data/manual/engine_electrical_inputs_reconciliation_20260517.csv.

## CNC release rules

DXF layers named HOLD_* are not production toolpaths. They provide nominal intent for quotation and cheap templates only.

1. Mark and photograph the exact ashtray/radio removal boundary, contour and flat lands from both sides.
2. Measure the actual LCD, all seven selector bushes and rear contact stacks, the hazard control, both vents and the hose.
3. Transfer the four existing right-cluster hole centres from the vehicle; never drill them from the nominal DXF.
4. Build a 1:1 card/acrylic or cheap-sheet prototype and install all actual parts.
5. Prove glovebox opening, instrument-panel rigidity, driver sight line, steering/gear-lever clearance, wiring and connector sweep, selector rear-stack clearance and duct bend radius.
6. Obtain owner sign-off on M1-M8, every cut edge and every centre before production cutting.
7. Cut the vehicle undersize, trim progressively, radius/deburr every edge and epoxy-prime all exposed steel before paint.

## Acceptance

- The complete protruding ashtray is gone and the ashtray/radio zone reads as one flat face.
- The 9-inch screen active area and bezel are verified against the actual LCD drawing, not inferred from the photograph.
- Glovebox, instruction panel and speedometer/instrument pressing remain visually and structurally unchanged.
- No new main-face vent opening exists; the two hose-fed outlets are below the dash on removable brackets.
- Screen, control strip and vents remain independently service-removable from the cabin side.
- All seven selector positions and labels match switch_position_schedule.csv.
- Wiring continuity, A/C safety logic, blower load, lighting logic, fuel-stop shutdown, vent flow and vibration/rattle tests pass.

## Package contents

- j40_dashboard_lcd_hvac_fascia_rev_d_shop_spec.pdf — three-page CNC brief, before/after actual-photo basis, exact selector map and electrical release schedule.
- dashboard_lcd_hvac_fascia_rev_d_dimensioned_front.svg — nominal front layout with 9-inch scale and labels.
- dashboard_lcd_hvac_fascia_rev_d_photo_overlay_assembled.png — latest concept applied to the assembled original dashboard, with both bracketed A/C vents visible; do not scale.
- dashboard_lcd_hvac_fascia_rev_d_photo_overlay_bare_shell.png — the same concept applied to the straight-on bare shell, with all seven selectors and both vents unobstructed; do not scale.
- dashboard_lcd_hvac_fascia_rev_d_photo_overlay.png — earlier single-view Rev D reference retained for traceability; superseded for visual review by the paired views above.
- Five Rev D DXFs — quote/template blanks with explicit CUT and HOLD layers.
- fabricator_cut_list.csv, measurement_and_release_schedule.csv and switch_position_schedule.csv — production controls.

Ready to send for quotation, vehicle templating and a cardboard/acrylic or cheap-sheet prototype. Not released for production metal or vehicle cutting until M1-M8 are completed and signed.
