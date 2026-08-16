# Rev I V43 ImageGen record

Mode: built-in `image_gen`, using three local image references. No fallback model was used.

## Final correction prompt

```text
Use case: precise-object-edit.
Asset type: realistic straight-on Toyota J40 dashboard fabrication photomontage.

IMAGE PRIORITY:
1. Image 1 is the EDIT TARGET. Preserve its exact straight-on camera, crop, workshop, vehicle, body colour, unchanged silver OEM glovebox, Pioneer screen, exactly seven black controls followed by one red hazard, original dashboard height and speedometer/column aperture.
2. Image 2 demonstrates the desired clearly visible RIGHT-HAND diagonal service seam ending at the speedometer. Use only that seam logic; do not copy its other geometry or crop.
3. Image 3 is structural truth for the original dashboard silhouette, glovebox perimeter, speedometer aperture, steering-column scallop and factory lower edge.

Make one geometric correction: turn the body-colour replacement into a clearly bounded, visually symmetrical centre panel between the glovebox and speedometer. It must NOT continue across the speedometer or to the far right end of the dashboard.

BOUNDARY GEOMETRY — CRITICAL:
- The panel TOP edge is the existing factory upper fold, beginning exactly at the OEM glovebox's upper-right corner and ending exactly at the TOP-LEFT / UPPER START of the speedometer aperture.
- The LEFT side seam sits immediately beside and follows the OEM glovebox door's right-hand curved/sloping edge, with only a narrow 2–3 mm-looking gap. From the upper-left corner it slopes inward toward the panel centre as it descends and meets the untouched original lower dashboard edge. Preserve the glovebox completely unchanged.
- The RIGHT side seam must be equally clear and must mirror the overall angle of the left seam: it starts at the top-left corner of the speedometer aperture, slopes inward toward the panel centre as it descends, and meets the untouched original lower dashboard edge. The two side cuts should form a balanced, approximately symmetrical trapezoidal centre panel around the display and switch row, adapted only as necessary to the real glovebox and speedometer shapes.
- Show a continuous narrow shadow/service gap on BOTH side seams, so it is unmistakable that the replacement ends at the speedometer-side seam. To the right of that seam, retain the original cream dashboard metal, original speedometer aperture, steering-column scallop, four small holes and far-right dashboard end exactly as Image 3.
- The panel bottom is only the existing factory lower dashboard edge between the two side seams. Do not add any lower line, drop, step, apron, chin, console, or metal below it.
- Keep the Pioneer screen and control bank horizontally centred and visually balanced inside this bounded trapezoidal panel. Do not enlarge the panel to the right to achieve centring.

INVARIANTS:
Keep the Pioneer display shallow and flush. Keep exactly seven black selectors followed by one red hazard in one straight row. The old ashtray, central rectangular opening and lower slot remain fully eliminated within the new panel. No vents, labels, new holes, extra controls, decorative trim, red markup or arrows. Change no unrelated rust, openings, levers, floor, lighting or background.
```

Accepted output: `dashboard_rev_i_v43_symmetric_glovebox_to_speedo_no_drop.png`.
