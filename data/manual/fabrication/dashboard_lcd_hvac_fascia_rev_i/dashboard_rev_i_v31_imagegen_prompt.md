# V31 image-generation record

Tool: built-in OpenAI image generation, followed by a local deterministic correction of the rendered `FUEL STOP` label only.

Target image: `dashboard_rev_i_v30_windscreen_holder_screws.png`
Outlet appearance reference: `supplied_ac_outlet_87_75_22_reference.png`

## Exact generation prompt

```text
Use case: precise-object-edit
Asset type: straight-on final dashboard fabrication visualization
Input images:
- Image 1 is the edit target and controls the complete J40 dashboard, vehicle, camera, perspective, colour, dashboard height, original glovebox, original speedometer cluster, steering column and scallop, MOMO wheel, LCD, switches, fasteners, lighting and background.
- Image 2 is the exact purchased A/C outlet appearance reference.

Primary request: Replace only the two existing small circular A/C outlets in Image 1 with two identical copies matching Image 2. Make both outlet visible face outside diameters accurately represent 87 mm in the same front-face plane. The true 9-inch 16:9 LCD active image is 199.2 mm wide and 112.1 mm high, so each 87 mm outlet face must appear 43.7% of the active screen width and 77.6% of the active screen height. Both outlets are mounted flush, high on exactly the same horizontal centre datum, one near each fixed outer end of the fascia. Keep them wholly within the original-height fixed fascia, with practical visible metal clearance from the glovebox on the left and the switch bank on the right.
Outlet appearance: one bright satin-silver circular outer ring, black inner directional core with the two broad curved horizontal vanes exactly like Image 2, no visible screws, no extra rings. The hidden rear mounting diameter is 75 mm and hidden rear body depth is no more than 22 mm; do not show rear parts from the front.
Text: Change only the incorrect bottom-row third switch label to the exact words "FUEL STOP". Preserve the other switch labels and the 4 x 2 layout.
Constraints: Preserve every other pixel-level design decision from Image 1 as closely as possible. Do not move or resize the LCD, glovebox, cluster, steering axis, steering wheel, switches, fascia boundaries, lower edge, windscreen-holder tabs/black hand screws, or vehicle structure. Do not add central vents, lower vents, pods, ashtray, console extensions, annotations, dimensions, new controls, logos or watermark. Exactly two A/C outlets total.
```

The owner subsequently refined the provisional LCD active-image figures to 198.91 × 111.89 mm. The normalized Ø87 ratios are therefore 43.74% of active width and 77.76% of active height. This sub-percent change is below one display pixel at the generated front-face scale, so the V31 raster remains the accepted visual study; the revised figures control the written specification and CAD validation.
