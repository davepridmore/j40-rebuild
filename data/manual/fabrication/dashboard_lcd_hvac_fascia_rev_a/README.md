# J40 Dashboard 9-inch LCD / HVAC Fascia — Rev A

This package is ready to send to the CNC/fabrication shop for quotation, vehicle templating, a 1:1 paper plot and fabrication of the released blank/carrier architecture. It intentionally does **not** authorize cutting the vehicle or the bought-part apertures until the actual 9-inch LCD, vents, industrial switches and dashboard have been measured and dry-fitted.

## Design decision

- Remove a large nominal `440 × 280 mm` middle dashboard section only after a cardboard template proves the boundary.
- Fit a `480 × 320 × 1.5 mm` CNC-cut main fascia with `20 mm` nominal overlap, radiused corners and eight M5 service fasteners.
- Back it with a `460 × 300 × 2.0 mm` stiffening ring. The screen must also have two rear support rails/tabs tied into the dashboard structure; the face sheet must not carry screen mass alone.
- Use a removable `310 × 200 × 2.0 mm` LCD carrier. Its nominal `233 × 135 mm` screen aperture is a HOLD reference, not a production cut.
- Use two removable vent carriers below the screen. Their internal openings follow the actual directional louver, with `63.5 mm / 2.5 inch` hose necks preferred.
- Fasten the LCD carrier at four corners and each vent carrier at four corners with M4 low-profile screws into captive nuts/nutplates. The matching Ø4.5 mm holes are released in both the fascia and carrier blanks.
- Put the two HVAC selectors (`blower OFF/LOW/HIGH` and `A/C enable OFF/ON`) and the red hazard button in the lower center strip.
- Replace the four original pull switches beside the gauge cluster with the bought `22 mm` industrial selectors in the existing positions after centres and rear contact-block clearance are transferred from the vehicle. Do not move them into the screen fascia.

## Control allocation

| Position | Function | Device |
| --- | --- | --- |
| Driver cluster 1 | Wipers OFF/LOW/HIGH | 3-position maintained industrial selector |
| Driver cluster 2 | Lights OFF/PARK/HEAD | 3-position maintained industrial selector |
| Driver cluster 3 | Spot lamps OFF/ON | 2-position maintained selector, relay control only |
| Driver cluster 4 | Auxiliary accessory OFF/ON | 2-position maintained selector, relay control only |
| Center lower left | Blower OFF/LOW/HIGH | 3-position maintained selector |
| Center lower middle | Hazards | Red 16 mm latching illuminated pushbutton |
| Center lower right | A/C enable OFF/ON | 2-position maintained selector, relay control only |
| Near ignition / separate | Diesel fuel stop RUN/STOP | Dedicated selector; retain manual cable backup |

Switches command relays or controller inputs; do not carry lamp, blower, clutch or accessory current directly unless the switch contact rating and protection are engineered for that load.

## HVAC and rear-envelope rules

- Preferred airflow path: evaporator/plenum → smooth `2.5 inch` flexible duct → vent neck. Keep hose runs short, supported and free of kinks.
- Prove at least `140 mm` usable depth behind the LCD zone including plug bend radius and `110 mm` behind each vent zone including hose clamp and bend.
- Keep duct clear of screen heat sink, wiring, sharp cut edges, wiper linkage and heater controls.
- Provide a demist strategy before assigning all evaporator outlets to face vents. The broader four-outlet plan remains in `docs/hvac-dashboard-vent-duct-layout-20260602.md`.

## Fabrication sequence

1. Remove loose trim and expose both sides of the proposed cut. Photograph wiring, braces and seams.
2. Make a full-size cardboard fascia and rear-depth buck from this drawing. Confirm sight line, gear-lever/steering clearance, glovebox opening and screen glare angle.
3. Place the actual LCD, vents and selectors on the buck. Record M1–M10 in `measurement_and_release_schedule.csv`.
4. Print the SVG/PDF at 1:1 and obtain owner sign-off on the actual cut line and component centres.
5. CNC/laser cut the fascia and rear frame; form only if the vehicle template proves a crown or flange is needed. Tack nutplates/rivnuts on the rear frame away from visible metal.
6. Cut the removable carrier apertures from the actual component rubbings/drawings. Dry assemble the complete module on the bench.
7. Cut the vehicle undersize, trim to the template, seal all raw edges, install the rear frame, then the fascia. No welding near installed electronics, ducts or upholstery.
8. Bond the fascia electrically to body earth; fuse/relay circuits separately; label the rear harness; leave a removable service loop.

## Acceptance

- Dashboard structure, gauge cluster and glovebox remain rigid and undistorted.
- LCD is removable without removing the whole dash; connectors can be reached and cannot chafe.
- Carrier fasteners engage captive threads fully, sit flush/low-profile and remain accessible from the cabin side.
- Each vent rotates/aims and can accept/remove its hose with the fascia installed.
- All selectors have anti-rotation features, correct legends and at least `10 mm` clearance around rear contact blocks/wiring.
- No sharp edge is reachable; all cut steel is epoxy-primed; visible finish is even satin black.
- Full electrical functional test, blower airflow test, A/C clutch logic test and road vibration/rattle test pass.

## Files

- `dashboard_main_fascia_rev_a.dxf` — released main plate geometry.
- `dashboard_rear_stiffening_frame_rev_a.dxf` — rear reinforcing ring.
- `lcd_carrier_blank_rev_a.dxf` — outer blank released; orange/reference screen aperture remains HOLD.
- `hvac_vent_carrier_blank_rev_a.dxf` — make two; inner vent aperture remains HOLD.
- `dashboard_lcd_hvac_fascia_rev_a_dimensioned_front.svg` and PDF — shop drawing/visualisation.
- `dashboard_lcd_hvac_fascia_rev_a_concept.png` — realistic intent only; never scale it.

## Release state

**Ready for CNC shop quotation, vehicle scan/template, cardboard/cheap-sheet prototype and the released outer blanks. Not released for final dashboard cut or screen/vent carrier apertures until M1–M10 are recorded and signed.**
