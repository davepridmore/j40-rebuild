# Rev I V32 image-generation record

Date: 2026-08-02
Tool: built-in OpenAI image generation
Use: controlled appearance study only; never scale this raster for CNC geometry

## Inputs

- Initial source: `dashboard_rev_i_v31_87mm_supplied_ac_outlets.png`
- Outlet appearance reference: `supplied_ac_outlet_87_75_22_reference.png`
- Intermediate generated source: `/Users/davidpridmore/.codex/generated_images/019fb8d3-8269-7eb0-b457-d806a3cefbd4/exec-8016cedb-c2c3-4f1c-8204-621264abf7e6.png`
- Final generated source: `/Users/davidpridmore/.codex/generated_images/019fb8d3-8269-7eb0-b457-d806a3cefbd4/exec-8c451d3f-c125-4946-9cc1-c93c9851e07d.png`
- Saved final: `dashboard_rev_i_v32_inboard_high_87mm_outlets.png`

## Pass 1 prompt

```text
Use case: precise-object-edit.
Asset type: straight-on J40 dashboard fabrication visualization, Rev I V32.

Edit the supplied V31 image only. Move exactly the two circular chrome-and-black A/C outlets; preserve their existing appearance, identical 87 mm visible face diameter, scale, perspective, orientation, silver ring, black directional core and broad horizontal vanes.

Position change: move the left outlet centre 0.20 outlet diameters inward (to the right) and 0.10 outlet diameters upward. Move the right outlet centre by the exact mirrored amount: 0.20 outlet diameters inward (to the left) and 0.10 outlet diameters upward. Their centres must remain on one common horizontal datum and symmetrical about the complete fascia centreline. This is approximately 17.4 mm inward and 8.7 mm upward per outlet. Keep both faces fully inside the original-height fixed fascia with visible body-colour metal around them. The left outlet must remain clear of the unchanged glovebox lid and its opening sweep; the right outlet must remain visibly clear above and outboard of the unchanged switch bank.

Preserve every other pixel-level design decision as closely as possible: exact vehicle/camera/crop, dashboard top and bottom edges and factory height, cream colour, upper screws and black hand screws, original asymmetric glovebox shape/size/colour/plate/knob, centred true 9-inch LCD and silver surround, original Toyota speedometer cluster and its low relationship to the steering column, factory steering-column scallop, steering column and MOMO wheel, all seven black selectors plus separate red hazard, the compact 4 x 2 switch layout, and exact labels WIPERS, LIGHTS, SPOTS, AUX, BLOWER, A/C, FUEL STOP, HAZARD. Do not move, resize, redraw, delete or add anything else. Exactly two A/C outlets total. No central or lower vents, no ashtray, no pods, no console extension, no annotations, no dimension lines, no logos or watermark.
```

## Pass 2 correction prompt

```text
Use case: precise-object-edit.
Asset type: straight-on J40 dashboard fabrication visualization, final Rev I V32.

Make one positional correction only to the supplied image. Move only the left/passenger-side circular A/C outlet horizontally outward to the left by approximately 0.27 of its own 87 mm visible diameter. Keep its vertical centre exactly unchanged. Keep the right/driver-side A/C outlet exactly fixed. The result must preserve both outlet centres on exactly the same high horizontal datum and make their horizontal positions visually mirrored about the geometric centreline of the complete cream fascia. Leave a clear, practical band of uninterrupted cream fascia between the left outlet's chrome outside edge and the unchanged glovebox-lid boundary; target about 15–20 mm of visible metal at real scale. The left outlet must still be modestly inboard from the outer end rather than at the extreme end.

Preserve the two outlets' exact existing visible diameter, silver ring, black core, broad horizontal vanes, scale, perspective and orientation. Preserve every other pixel-level design decision as closely as possible: vehicle and camera/crop, original factory dashboard height and complete boundaries, cream colour and texture, screws and black hand screws, exact large asymmetric glovebox, centred true 9-inch LCD, original Toyota cluster, steering column/scallop and MOMO wheel, compact 4 x 2 bank of seven black selectors plus separate red hazard, and the exact labels WIPERS, LIGHTS, SPOTS, AUX, BLOWER, A/C, FUEL STOP, HAZARD. Do not move, resize, redraw, delete or add anything else. Exactly two A/C outlets total. No ashtray, no annotations, no dimension lines, no logo or watermark.
```

## Interpretation

The final raster approves the slightly higher/inboard visual direction only. The passenger-side correction restored a practical visible band to the glovebox boundary. Production vent centres, apertures and rear clearances remain controlled by the signed vehicle trace, all-four-part M7 measurements, a same-material/same-finish fit coupon and a full-depth mock-up.
