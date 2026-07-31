# J40 RHD Compact 9-inch LCD / Four-outlet Dashboard - Rev F

Rev F is the compact arrangement shown on both owner photographs. The ashtray is removed and the centre zone becomes a shallow body-colour CNC fascia containing only a true 9-inch LCD and two large circular A/C outlets. A matching outlet is integrated at each end of the dashboard, giving four outlets total. All seven bought industrial selectors are consolidated in one labelled 4 x 2 bank to the right of the original speedometer; the separate red hazard switch occupies the eighth position. The original speedometer/instrument pressing and glovebox/instruction panel remain unchanged.

## Locked visual and packaging intent

- Keep the dashboard recognisably original: preserve its full-width painted pressing, original speedometer opening and original glovebox/instruction panel.
- Delete the complete ashtray door, body, lip, seam and recess. Flatten only the combined centre radio/ashtray zone needed by the new fascia.
- Do not extend the centre dashboard downwards for controls. The centre fascia is 410 x 148 mm, 77 mm (34%) shallower than Rev E.
- Finish new metal in matching low-gloss body colour. Use a restrained black LCD bezel and four matching satin/brushed-silver directional outlet bezels with dark cores.
- Engrave every right-bank control label 3 mm high and fill black.

## Nominal centre-fascia geometry

Datum is the lower-left corner of the 410 x 148 mm fascia blank. Dimensions are millimetres.

| Feature | X | Y | Size / status |
|---|---:|---:|---|
| Released fascia outer | 0 | 0 | 410 x 148, R6; `CUT_FASCIA_OUTER` only |
| Vehicle opening envelope behind fascia | 18 | 12 | 374 x 124, R3; `HOLD_VEHICLE_OPENING`, not a fascia cut |
| LCD bezel envelope | 96 | 10 | 218 x 128; HOLD to actual LCD |
| LCD aperture | 104 | 16.5 | 202 x 115; HOLD to actual LCD |
| Centre outlet 2 | 49 | 74 | face Ø82 max; rear cut Ø66 reference; HOLD |
| Centre outlet 3 | 361 | 74 | face Ø82 max; rear cut Ø66 reference; HOLD |

The screen reference is a true 9-inch 16:9 active image: 199.2 x 112.1 mm and 228.6 mm diagonal. The actual LCD mechanical drawing controls the front aperture, bezel, rear body, mounting, connector and removal clearances.

The nominal central geometry has been checked: each Ø82 face has 8 mm side margin, a 6 mm visible gap to the LCD bezel, and the Ø66 cut has a 14 mm ligament to the bezel. The bezel has 10 mm top and bottom land. These checks show feasibility only; the actual bought parts still control production holes.

## Four integrated A/C outlets

Numbering is passenger to driver on this right-hand-drive dashboard:

1. Far passenger-side/left dash end — positioned using the outer-vent transfer template.
2. Left side of the centre fascia at (49,74).
3. Right side of the centre fascia at (361,74).
4. Far driver-side/right dash end — positioned using the outer-vent transfer template.

All four outlets must match: satin/brushed-silver circular directional face, Ø82 mm maximum visible diameter, dark directional core permitted, face flush to +0.5 mm maximum, hidden rear nut/spring ring/clamp and no exposed front screw. The reference rear cut is Ø66 and target flexible-hose neck is Ø63.5 mm / 2.5 inch.

The 374 x 124 vehicle-opening rectangle lies behind the new fascia and is not a fascia toolpath. Its nominal side edges do not fully clear the two Ø66 centre vent cuts, so the final vehicle opening needs measured rear-relief scallops or a revised profile. Establish that profile only after a 1:1 fascia, real vents and real duct hose are mocked up from behind. Route four hoses from the selected HVAC plenum without crushed bends or contact with the glovebox, instruments, steering, wiring or screen.

## Consolidated right-side control bank

Reference envelope is 190 x 88 mm. Hole centres are x = 24, 71, 118, 165 and y = 64 (top) / 24 (bottom), giving 47 mm horizontal and 40 mm vertical pitch. Nominal selector apertures are Ø22.3; the red hazard aperture is Ø16 reference. The minimum nominal hole-edge land is 12.85 mm. Entire bank geometry and vehicle position remain HOLD until the actual switches and a 1:1 template are fitted right of the speedometer.

| Position | Label | Hardware / states | What it does |
|---|---|---|---|
| R1-C1 | WIPERS | 3-position: OFF / LOW / HIGH | Parks the wipers in OFF and selects low or high wipe speed. |
| R1-C2 | LIGHTS | 3-position: OFF / SIDE / HEAD | Turns lights off, selects sidelights or enables headlamps; retained dip selects low/high. |
| R1-C3 | SPOTS | 2-position: OFF / ON | Commands spot-lamp relay T5. |
| R1-C4 | AUX | 2-position: OFF / ON | Commands reserved accessory relay/output B2; final accessory is not selected. |
| R2-C1 | BLOWER | 3-position: OFF / LOW / HIGH | Stops the cabin fan or selects low/high airflow. |
| R2-C2 | A/C | 2-position: OFF / ON | Requests compressor cooling through the thermostat/trinary/pressure safety chain. |
| R2-C3 | FUEL STOP | 2-position: RUN / STOP | Maintains engine run or requests shutdown; provisional until live-tested. |
| R2-C4 | HAZARD | separate red pushbutton: OFF / FLASH | Flashes all indicators; original left/right indicator stalk remains. |

The purchased-selector allocation is three 3-position units (WIPERS, LIGHTS, BLOWER) and four 2-position units (SPOTS, AUX, A/C, FUEL STOP). HAZARD is a separate eighth control, not another selector.

## Electrical implementation

- Every selector commands a fused relay or controller input only. Do not carry lamp, blower, clutch, wiper-motor or accessory load current through a selector contact.
- Relay baseline: T1 low beam, T2 high beam, T3 horn, T4 condenser fan, T5 spots, B1 A/C clutch, B2 AUX and B3 spare.
- WIPERS requires an interface that preserves automatic park when the selector returns to OFF.
- LIGHTS is OFF/SIDE/HEAD master selection; retain the separate dip function that selects T1 low beam or T2 high beam.
- BLOWER uses a dedicated measured relay/controller and resistor or PWM circuit sized after the actual motor load is measured.
- A/C may request B1 only through thermostat, trinary/pressure protection and the selected HVAC controls. Prove T4 condenser-fan logic before operation.
- FUEL STOP is provisional until the actual stop device, contact sense and terminals are identified and RUN-to-OFF shutdown is proved with the engine running. Retain the manual stop cable.

Evidence basis: `data/manual/workbook_tabs/electrical_master.csv`, `data/manual/expenses.csv`, `data/manual/electrical_diagram_reconciliation_20260518.csv` and `data/manual/engine_electrical_inputs_reconciliation_20260517.csv`.

## CNC layer and release rules

- `CUT_FASCIA_OUTER` is the only released metal toolpath: 410 x 148 x 1.5 mm CR4, R6 corners.
- Every layer beginning `HOLD_` is construction/reference geometry and must not be sent to a production cut path.
- `HOLD_VEHICLE_OPENING` is the proposed void in the original dashboard behind the overlay fascia; it is not a cut through the new fascia.
- `CUT_TEMPLATE_OUTER` applies only to the disposable outer-vent transfer template, never to vehicle metal.
- Quote the right control bank, outer-vent templates and LCD clamp now, but do not production-cut them until M1-M9 evidence is complete.
- Cut any approved vehicle opening initially undersize, trim progressively, deburr/radius all edges and epoxy-prime exposed steel before paint.

## M1-M9 production gates

See `measurement_and_release_schedule.csv`. In summary: fit the centre template and define vent relief; obtain the LCD drawing and rear clearances; measure every control; fit the 4 x 2 bank template; measure all four vents; mock up all four ducts; sign off the full-size physical dashboard; then prove labels, continuity, relays, wiper park, lights, blower, A/C protection, fuel shutdown and hazard operation.

## Paired-view visual rule

Every future design revision must be applied to both owner images: the assembled right-hand-drive driver view and the straight-on bare-shell view. The images establish appearance and placement intent only and must never be scaled for CNC work.

## Acceptance

- Original glovebox/instruction panel and speedometer/instrument pressing remain visually and structurally unchanged.
- Centre fascia does not extend below the original dashboard lower line more than required for its return/mounting lip.
- Actual screen proves a true 9-inch active area and is service-removable.
- Four matching Ø82-max silver directional outlets are integrated, secure, serviceable and supplied by unobstructed ducting.
- All seven selectors and separate hazard control are together right of the speedometer and carry the scheduled engraved labels.
- All operational and safety tests in M9 pass without overheating, voltage drop, interference, rattle or unintended function.

## Package contents

- `j40_dashboard_lcd_hvac_fascia_rev_f_shop_spec.pdf` — three-page CNC/shop brief.
- `dashboard_lcd_hvac_fascia_rev_f_dimensioned_front.svg` — centre fascia and 4 x 2 control-bank drawing.
- Two owner-photo visualisations — assembled and bare-shell views; do not scale.
- Four DXFs — centre fascia, right control bank, outer-vent pair transfer template and LCD rear-clamp reference.
- Three CSV schedules — cut list, M1-M9 measurement/release gates and complete control/electrical mapping.

This package is ready to send for quotation and template work. Only the centre-fascia outer blank is released for metal cutting; all vehicle cuts and actual-part apertures remain HOLD until the recorded fit and measurement gates are signed off.
