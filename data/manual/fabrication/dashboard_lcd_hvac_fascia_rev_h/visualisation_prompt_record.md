# Rev H visualisation prompt record

Mode: built-in `image_gen`, local-reference `precise-object-edit`.

## Straight-on bare-shell edit prompt

Precise object edit of this existing straight-on Toyota J40 dashboard visualization. Change only the two inner/centre silver circular A/C outlets and their body-colour rounded pods. Set the final inner-outlet position so their centres are visibly about 1.71 outlet-face diameters lower than the high outer-outlet centres in the dashboard plane, while preserving their exact left/right X positions, equal size, satin-silver rims, dark directional cores, and exact symmetry about the LCD. The final top of each inner silver rim must sit about 0.14 outlet-face diameter below the LCD bezel bottom (the nominal drawing ratio is 12.5/87), with clear body-colour separation. Extend each cream rounded pod downward locally so its bottom remains about 0.13 outlet-face diameter below the rim bottom (nominal ratio 11.5/87). Keep the outer two vents at their current high positions. Do not move, resize, restyle, replace, or redraw the true 9-inch LCD, original Toyota speedometer and auxiliary cluster in its factory opening, original glovebox and black plate, steering-column relief, seven rotary switches, red hazard, labels, vehicle, camera, colour, patina, background, or any other object. Keep exactly 4 vents, exactly 7 rotary selectors, and exactly 1 red hazard. No full-width downward dashboard extension; only the two local vent pods get deeper. Photorealistic, same resolution and composition. The image expresses ratios only; it is never scaled for CNC.

## Assembled driver-eye edit prompt

Precise object edit of this existing assembled driver-eye Toyota J40 dashboard visualization. Change only the two inner/centre silver circular A/C outlets and their body-colour rounded pods. Set the final inner-outlet position so their centres are about 1.71 outlet-face diameters lower than the high outer-outlet centres in the true dashboard plane, preserving their exact left/right X positions in the panel, equal physical size, satin-silver rims, dark directional cores, and exact symmetry about the true panel/LCD centreline despite perspective. The final top of each inner silver rim must sit about 0.14 outlet-face diameter below the LCD bezel bottom in the dashboard plane (nominal ratio 12.5/87), with clear body-colour separation. Extend each cream rounded pod downward locally so its bottom remains about 0.13 outlet-face diameter below the rim bottom (nominal ratio 11.5/87). Keep the outer two vents at their current high positions. Keep the right inner vent and its rear duct visibly clear of the original steering column and shroud. Do not move, resize, restyle, replace, or redraw the true 9-inch LCD, original Toyota speedometer and auxiliary cluster in its factory opening directly above the steering column, original glovebox and black plate, steering wheel, column, column shroud, stalks, seven rotary switches, red hazard, labels, vehicle, camera, colour, patina, background, or any other object. Keep exactly 4 vents, exactly 7 rotary selectors, and exactly 1 red hazard. No full-width downward dashboard extension; only the two local vent pods get deeper. Photorealistic, same resolution, camera and composition. The image expresses ratios only; it is never scaled for CNC.

The two approved outputs are copied into this package as the straight-on and assembled Rev H overlays. The supplied selector photograph is copied as `industrial_rotary_selector_reference.png`.

Generated overlays show visual intent only. The nominal drawing sets the inner vent centres at Y=20.0 mm and the pod bottoms at Y=-35.0 mm. Their nominal visible rim-to-LCD gap is 12.5 mm, but M9 requires at least 8 mm as built. DXF/CSV dimensions, direct vehicle traces, M1-M10 physical templates and bought-part measurements control fabrication; M1/M3/M7/M8/M9 must establish the installed column, duct, vent and driver clearances before production cutting.

## 2026-08-01 assembled V4 / steering-column correction record

Output: `layout_variants_20260801/layout_b_column_v4_clearance_assembled.png`.

Mode: built-in `image_gen`, local-reference `precise-object-edit`.

Correction intent: restore **only** the short horizontal matte-black steering-column/shroud section from the wheel hub into the existing factory lower-instrument relief. It must never become a wheel spoke or a diagonal tube. Lower the complete right-hand 2 x 4 control bank enough to show roughly one actual selector-head diameter between the V4 rim and its nearest selector head; preserve the complete control allocation, labels, right edge and all other dashboard identity. Freeze the original glovebox, original speedometer/cluster, true 9-inch LCD, four outlet sizes/finish, factory camera/vehicle, colour and patina. This is a visual correction record, not a dimensional release: the straight-on bare-shell overlay remains the visual placement control, and M6/M8/M9 establish the actual V4 selector and rear-duct clearances.

## 2026-08-01 V5 / visible installed steering-column pair

Outputs:

- `layout_variants_20260801/layout_b_column_v5_clear_assembled.png`
- `layout_variants_20260801/layout_b_column_v5_straight_on.png`

Mode: built-in `image_gen`, local-reference `precise-object-edit`.

Correction intent: use `photos/20260317_165113.jpg` and `photos/20260323_190047.jpg` as the original-column geometry controls. In the oblique view, show one uninterrupted near-horizontal matte-black column/shroud from the existing wheel hub into the factory radiused relief beneath the OEM cluster. In the straight-on view, install one original-scale right-hand-drive wheel and the same continuous column, with the hub/shaft centreline directly beneath the retained OEM meter. Freeze the approved true 9-inch LCD, original glovebox, four vents, and seven-selector-plus-red-hazard allocation. These images show placement and occlusion only; the signed vehicle trace and M1/M3/M8/M9 mock-up remain controlling.

## 2026-08-01 V6 / explicit column and centred compact control bank

Outputs:

- `layout_variants_20260801/layout_b_column_v6_switches_clear_assembled.png`
- `layout_variants_20260801/layout_b_column_v6_switches_straight_on.png`

Mode: built-in `image_gen`, local-reference `precise-object-edit`.

Correction intent: in the oblique view, make the original matte-black column/shroud mechanically explicit from the existing wheel hub to the factory relief directly below the OEM meter. Move the complete control allocation down and right as one compact 2 x 4 group in both views, without rearranging functions. The nominal model now uses columns X=(1120.0, 1160.0, 1200.0, 1240.0), rows Y=78/20, and a 40 mm horizontal pitch. That places the bank centrally inside its existing shallow Y=3 local channel; it does not increase overall dashboard height. Preserve exactly seven black selectors plus one separate red hazard, labelled WIPERS / LIGHTS / SPOTS / AUX. and BLOWER / A/C / ENGINE / HAZARD. Freeze the true 9-inch LCD, four vents, OEM speedometer, OEM glovebox, steering-wheel scale, camera and vehicle identity. The bought head and lever sweep still require the M6 full-size trial before any aperture is released.
