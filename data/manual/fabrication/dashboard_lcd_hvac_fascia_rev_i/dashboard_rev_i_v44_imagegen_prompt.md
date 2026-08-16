# Rev I V44 ImageGen record

Mode: built-in `image_gen`, using two local image references. No fallback model was used.

## Final prompt

```text
Use case: precise-object-edit.
Asset type: realistic, straight-on Toyota J40 dashboard fabrication photomontage.

IMAGE ROLES
1. Image 1 is the edit target. Preserve its exact camera position, crop, workshop, vehicle, glovebox, speedometer/steering-column aperture, Pioneer 9-inch screen, seven black rocker controls plus one red hazard switch, and original cream body colour.
2. Image 2 is the structural reference and the source of truth for the original factory dashboard shell silhouette—especially the height and lower edge. Do not revert the centre layout to Image 2; use it only to restore the original shell geometry.

PRIMARY CORRECTION — CRITICAL
The generated Image 1 incorrectly makes the centre of the dashboard extend farther downward. Remove that apparent added apron, skirt, chin, lower band, or drop completely.
Restore and preserve the exact original factory lower dashboard edge shown in Image 2 across the whole dashboard. The new centre panel must fit entirely inside the original height of the metal dash face. Its bottom terminates exactly at the existing factory lower edge; it must not alter, lower, thicken, or extend that edge. Everything below the original edge remains open vehicle interior.

NEW PANEL GEOMETRY
- Retain a closed, balanced cream centre insert located only between the glovebox on the left and the speedometer aperture on the right.
- Preserve the left boundary seam alongside the glovebox and the right boundary seam ending at the top/left edge of the speedometer area. Never run the panel to the far right end of the dashboard.
- Make the panel visually symmetric/balanced around the screen/control bank.
- Round BOTH upper corners of the insert. Replace the sharp pointed/diagonal top junctions with smooth, generous OEM-style curved radii consistent with the upper corner radii of the glovebox lid and speedometer aperture. The top seam must flow into both side seams through matching rounded arcs.
- The side seams may taper inward mildly as they descend, but both must meet the unchanged factory lower edge cleanly. Do not invent a new horizontal lower seam or border.

COMPONENTS
Keep the Pioneer display recessed flush with the cream panel. Keep seven identical black rocker controls plus one red hazard switch in a neat single row directly beneath it, centered and fully contained above the unchanged factory lower edge. Do not add vents, knobs, gauges, trim, text, or extra controls.

INVARIANTS
Do not modify the dashboard top edge, total dashboard height, glovebox, glovebox opening/radius, speedometer opening, steering-column opening, side structures, workshop, perspective, exposure, or vehicle interior. Keep a plausible fabricated cream-painted steel finish and subtle realistic seams. The result must read as a removable centre panel fitted within the original Toyota J40 dash silhouette, not as a larger replacement dashboard.
```

Accepted output: `dashboard_rev_i_v44_factory_height_rounded_top_corners.png`.
