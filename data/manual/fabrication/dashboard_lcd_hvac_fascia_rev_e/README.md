# J40 RHD Centre 9-inch LCD / Integrated A/C Fascia - Rev E

Rev E uses both owner photographs as the visual basis. It replaces the complete ashtray/radio zone with one wider flat body-colour fascia carrying a true 9-inch LCD, three lower selectors, a separate hazard control and two flush circular satin-silver A/C outlets. The original glovebox/instruction panel and speedometer/instrument pressing remain unchanged.

## Owner-authorised cut-and-replace scope

- The centre dash may be cut as required. Delete the complete ashtray door, body, lip, seam and recess and absorb the radio openings into the same opening.
- Release the fascia outer blank at 410 x 225 x 1.5 mm CR4 mild steel with R6 corners (`CUT_FASCIA_OUTER`).
- Use the red 374 x 189 mm R3 line as the proposed vehicle opening. Locate that opening with the 1:1 fascia template before cutting so it clears the two protected OEM pressings.
- Preserve only the stated original features: glovebox/instruction panel and speedometer/instrument pressing. Do not drill, cover, distort or trim either one.
- Finish the fascia in low-gloss body colour, with a restrained black LCD bezel and satin/brushed silver outlet bezels.

## Nominal local geometry

Datum is the lower-left corner of the 410 x 225 fascia blank; all dimensions are millimetres.

| Feature | X | Y | Size / note |
|---|---:|---:|---|
| Proposed vehicle opening | 18 | 18 | 374 x 189, R3; locate by fitted template |
| LCD bezel envelope | 90 | 72 | 230 x 132; HOLD to actual LCD |
| LCD aperture | 104 | 80.5 | 202 x 115; HOLD to actual LCD |
| Lower control strip | 90 | 20 | 230 x 40 |
| Left silver outlet centre | 52 | 51 | face Ø70 max; cutout Ø66 reference |
| Right silver outlet centre | 358 | 51 | face Ø70 max; cutout Ø66 reference |
| Lower selector centres | 120 / 185 / 250 | 43 | BLOWER / A/C REQUEST / FUEL CONTROL |
| Hazard centre | 300 | 43 | separate red control |

The 9-inch reference is a 199.2 x 112.1 mm 16:9 active image, 228.6 mm diagonal. The actual LCD manufacturer's mechanical drawing controls the bezel, aperture, rear body, mount and connector clearances.

## Integrated A/C outlets

- Use two matched circular directional outlets with satin/brushed silver face bezels. A black directional core is acceptable.
- Visible face diameter is Ø70 mm maximum. Installed face must be flush to +0.5 mm maximum relative to the fascia.
- Use the bought vent's hidden rear nut, spring ring or clamp. No exposed front screws, pods or hanging brackets.
- Target a Ø63.5 mm / 2.5-inch hose neck. The nominal DXF shows `HOLD_VENT_FACE_ENVELOPE` Ø70 and `HOLD_VENT_NECK_CUTOUT` Ø66.
- Do not production-cut the vent apertures until both bought vents have been measured for face, cutout, retainer, neck OD and rear depth and trialled with the actual hose.

## Exact control positions

All positions are viewed from the cabin.

Right of the speedometer, original 2 x 2 zone:

- Upper-left: WIPERS — 3-position, OFF / LOW / HIGH.
- Upper-right: LIGHTS — 3-position, OFF / SIDE / HEAD.
- Lower-left: SPOTS — 2-position, OFF / ON; relay T5.
- Lower-right: AUX — 2-position, OFF / ON; B2 auxiliary control.

Under the LCD, left to right:

- BLOWER — 3-position, OFF / LOW / HIGH.
- A/C REQUEST — 2-position, OFF / ON.
- FUEL STOP / CONTROL — 2-position, provisional pending device and live shutdown proof.
- Separate red HAZARD at far right; not one of the seven selectors.

Indicators remain on the OEM stalk.

## Electrical rules

- Every selector commands a fused relay/control circuit; no selector directly carries a high-current lamp, blower, clutch or accessory load.
- Frozen relay baseline: T1 low beam, T2 high beam, T3 horn, T4 condenser fan, T5 spot lamps, B1 A/C clutch and B2 auxiliary accessory.
- BLOWER uses a dedicated measured HVAC control/relay/resistor circuit. T1 and T2 remain lighting relays.
- A/C REQUEST may energise B1 only through the thermostat / trinary / pressure-protection chain. Prove T4 condenser-fan behaviour with the final HVAC hardware.
- FUEL STOP / CONTROL remains HOLD until the actual device and terminals are identified and key-OFF shutdown is proved with the engine running. Retain the manual stop cable.

Evidence basis: `data/manual/workbook_tabs/electrical_master.csv`, `data/manual/reference_projects_and_ideas.csv`, `data/manual/expenses.csv`, `data/manual/electrical_diagram_reconciliation_20260518.csv` and `data/manual/engine_electrical_inputs_reconciliation_20260517.csv`.

## CNC release rules

- `CUT_FASCIA_OUTER` is released for the 410 x 225 R6 outer blank.
- `MARK_PROPOSED_VEHICLE_CUT` is a 1:1 placement/cut template. The owner authorises the centre cut, but template location must keep the glovebox and speedometer pressing intact.
- Every layer beginning `HOLD_` is reference geometry, not a production toolpath.
- Measure the actual LCD, all seven selector bushes and rear stacks, the hazard control, both vents and hose before releasing their apertures.
- Transfer the four existing right-cluster centres from the vehicle; do not drill them from nominal artwork.
- Trial-fit a 1:1 card/acrylic or cheap-sheet prototype with all actual parts. Prove glovebox operation, instrument rigidity, driver sight line, steering/gear-lever clearance, rear stacks, wiring and duct sweeps.
- Cut the vehicle opening slightly undersize, trim progressively, deburr/radius all edges and epoxy-prime exposed steel before paint.

## Paired-view visual issue rule

Every design revision must be applied to and checked on both owner images:

1. assembled driver view, showing the right-hand-drive steering relationship; and
2. straight-on bare-shell view, showing the complete fascia, glovebox and speedometer boundaries.

The images establish appearance and placement intent only; do not scale them for CNC work.

## Acceptance

- Complete ashtray removal and one flat ashtray/radio replacement face.
- Actual LCD proves a true 9-inch active area and fits its released aperture and clamp.
- Glovebox/instruction panel and speedometer/instrument pressing remain visually and structurally unchanged.
- Two matched silver circular directional outlets read as integrated dashboard features, sit flush to +0.5 mm, and have no exposed bracket or front screw.
- Screen, lower control strip and both vents remain independently service-removable from the cabin side.
- All seven selector assignments match `switch_position_schedule.csv`.
- Wiring continuity, A/C safety logic, blower load, lighting logic, fuel-stop shutdown, vent flow and vibration/rattle tests pass.

## Package contents

- `j40_dashboard_lcd_hvac_fascia_rev_e_shop_spec.pdf` — three-page CNC/shop brief with both owner-photo pairs, geometry, selector schedule and release gates.
- `dashboard_lcd_hvac_fascia_rev_e_dimensioned_front.svg` — dimensioned front layout.
- `dashboard_lcd_hvac_fascia_rev_e_photo_overlay_assembled.png` and `..._bare_shell.png` — paired Rev E visualisations; do not scale.
- Four Rev E DXFs — fascia, lower selector strip, right-cluster transfer template and LCD rear clamp.
- `fabricator_cut_list.csv`, `measurement_and_release_schedule.csv` and `switch_position_schedule.csv` — release controls.

Ready to send for CNC quotation. The fascia outer blank is released. The centre-dash cut is owner-authorised after 1:1 template placement; actual-part apertures remain HOLD until M1-M8 evidence is completed.
