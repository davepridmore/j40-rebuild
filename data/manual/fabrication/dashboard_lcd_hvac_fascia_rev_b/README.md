# J40 RHD Centre 9-inch LCD / HVAC Fascia - Rev B

Rev B supersedes the Rev A full-size replacement concept. It starts from the owner's actual dashboard photograph and preserves the original right-hand-drive instrument/speedometer pressing, steering-column notch, four switch holes to its right, left glovebox, instruction plate and small original compartment.

## Approved design intent

- Remove the ashtray and combine only the existing centre radio/ashtray openings behind one compact, nearly flush CNC fascia.
- Nominal quote envelope is `275 x 220 x 1.5 mm`; the actual vehicle template controls the outer contour. Do not extend the cut toward the glovebox or speedometer pressing.
- Fit the actual horizontal 9-inch LCD in the upper centre. The `230 x 132 mm` drawing aperture is reference-only until the LCD is measured.
- Put four of the bought compact industrial switches on a removable lower strip. Original functions can remain in/reuse the four factory holes to the right of the instrument panel; move only functions agreed during the labelled mock-up.
- Mount two compact directional eyeball A/C outlets on separate under-dash brackets, one on each side of the centre insert. Prefer `63.5 mm / 2.5 inch` hose necks after measuring the bought vents. This keeps vent apertures out of the original dash face.
- Paint the fascia body colour in low gloss; use a thin black LCD bezel and discreet black vent pods. The aim is an original dashboard with one restrained modern insert.

## Control allocation for the 1:1 mock-up

The four centre-strip positions are provisionally `blower`, `A/C enable`, `hazard`, and one moved auxiliary function. Final function/order is a label-and-reach trial, not a CNC assumption. Wipers, lights and safety-critical original controls should preferentially stay in the original right-side locations. Switches operate relays/controller inputs unless their protected load rating is explicitly engineered.

## CNC release rules

DXF layers named `HOLD_*` are not production toolpaths. They show nominal intent so the shop can quote and make a cheap template. Release them only after:

1. Tape/card-template the actual centre zone from both sides and record M1-M7.
2. Place the actual LCD, four switches and two vents on the 1:1 template.
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

- `j40_dashboard_lcd_hvac_fascia_rev_b_shop_spec.pdf` - two-page CNC brief and actual-photo intent overlay.
- `dashboard_lcd_hvac_fascia_rev_b_dimensioned_front.svg` - nominal front layout.
- `dashboard_lcd_hvac_fascia_rev_b_photo_overlay.png` - image edit of the owner's actual RHD dashboard; never scale.
- Four DXFs - quote/template blanks with explicit CUT and HOLD layers.
- `fabricator_cut_list.csv` and `measurement_and_release_schedule.csv` - shop controls.

**Ready to send for quotation, vehicle templating and a cardboard/cheap-sheet prototype. Not released for production cutting of the vehicle, LCD aperture, switch apertures or vent apertures until M1-M7 are completed and signed.**
