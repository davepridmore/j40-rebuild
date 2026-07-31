# J40 RHD Centre 9-inch LCD / HVAC Fascia - Rev C

Rev C corrects LCD scale and the control count. It starts from the owner's actual RHD dashboard photograph, preserves the speedometer/instrument pressing and glovebox, and replaces only the centre radio/ashtray zone.

## Approved design intent

- Remove the ashtray and combine only the existing centre radio/ashtray openings behind one compact, nearly flush CNC fascia.
- Nominal quote envelope is `275 x 225 x 1.5 mm`; the vehicle template controls the outer contour. The panel covers the deleted ashtray.
- A 9-inch 16:9 active image is `199.2 x 112.1 mm`. The nominal `202 x 115 mm` aperture is a scale reference only; the actual LCD model controls bezel, aperture, rear body, mount and connector geometry.
- Fit seven purchased 22 mm Schneider Harmony-style rotary selectors: four in the original right-hand 2 x 2 positions and three on the removable strip below the LCD. Retain a separate red hazard button.
- Mount two compact directional eyeball A/C outlets on separate under-dash brackets, one on each side of the centre insert. Prefer `63.5 mm / 2.5 inch` hose necks after measuring the bought vents. This keeps vent apertures out of the original dash face.
- Paint the fascia body colour in low gloss; use a thin black LCD bezel and discreet black vent pods. The aim is an original dashboard with one restrained modern insert.

## Control allocation for the 1:1 mock-up

The inventory and electrical record agree: four 2-position selectors and three 3-position selectors. Provisional allocation is:

- 3-position: `WIPERS (OFF/LOW/HIGH)`, `LIGHTS (OFF/SIDE/HEAD)`, `BLOWER (OFF/LOW/HIGH)`.
- 2-position: `SPOTS`, `AUX`, `A/C REQUEST`, `FUEL STOP / CONTROL`.
- Right cluster: wipers, lights, spots and auxiliary. Centre strip: blower, A/C request and fuel-stop/control. Hazard is separate; indicators remain on the OEM stalk.

All selectors drive fused relay/control circuits rather than high-current loads. Keep relay baseline T1 blower low, T2 blower high, T3 horn, T4 condenser fan, T5 spots, B1 A/C clutch and B2 auxiliary. A/C request must pass the pressure/trinary safety chain before B1. Fuel-stop/control is a release HOLD until ignition-OFF behavior is proven live; retain the manual stop cable.

## CNC release rules

DXF layers named `HOLD_*` are not production toolpaths. They show nominal intent so the shop can quote and make a cheap template. Release them only after:

1. Tape/card-template the actual centre zone from both sides and record M1-M8.
2. Place the actual LCD, seven selectors, separate hazard and two vents on the 1:1 template.
3. Prove glovebox opening, instrument-panel rigidity, driver sight line, steering-column clearance, gear-lever clearance, wiring/connector sweep and duct bend radius.
4. Print the final DXF at 1:1, offer it to the vehicle, and obtain owner sign-off on every edge and centre.
5. Cut the vehicle undersize, trim progressively, radius/deburr every edge and epoxy-prime exposed steel before paint.

## HVAC rules

- Route evaporator/plenum air through two supported smooth-bore hoses to the under-dash outlets; no kinks or crushed bends.
- Keep ducts clear of the LCD heat sink/connectors, wiper linkage, steering column, heater controls, wiring and sharp edges.
- Provide strain relief at each vent and plenum neck. A hose must be service-removable without removing the glovebox or instrument panel.
- These are the two front face-level outlets. Preserve a separate windscreen demist path; do not allocate all conditioned air to face vents.

## Acceptance

- Glovebox and instrument/speedometer pressing are visually and structurally unchanged.
- No new hole or cut exists outside the original centre radio/ashtray zone, except reversible under-dash vent-bracket fixings approved on the template.
- LCD, switch strip and each vent can be removed independently from the cabin side.
- Screen remains readable from the right-hand driver's position without blocking the original speedometer.
- Full steering, gear-lever, wiper/heater linkage, wiring and hose sweeps have clearance and no chafe point.
- All circuits are fused/relayed correctly; vents aim and flow; finished assembly passes vibration/rattle and road tests.

## Files and release state

- `j40_dashboard_lcd_hvac_fascia_rev_c_shop_spec.pdf` - two-page CNC brief and actual-photo intent overlay.
- `dashboard_lcd_hvac_fascia_rev_c_dimensioned_front.svg` - nominal front layout.
- `dashboard_lcd_hvac_fascia_rev_c_photo_overlay.png` - edit of the owner's actual RHD dashboard; never scale.
- Five DXFs - quote/template blanks with explicit CUT and HOLD layers.
- `fabricator_cut_list.csv` and `measurement_and_release_schedule.csv` - shop controls.

**Ready to send for quotation, vehicle templating and a cardboard/cheap-sheet prototype. Not released for production cutting until M1-M8 are completed and signed.**
