# J40 Electrical Module Fabrication Pack - Rev A

This pack is a provisional fabrication set for two under-bonnet electrical modules:

1. `relay_module_tray_rev_a`
2. `power_module_box_rev_a`
3. `power_module_rear_insulator_rev_a`

All dimensions are in millimetres.

## Recommended file to send to the fabricator

Send the `DXF` files for cutting, the matching `SVG` files for human review, and the PDF sheet for non-CAD review.

For assembly review, open `electrical_modules_rev_a_3d_visualisation.html`. The matching static fallback is `electrical_modules_rev_a_3d_visualisation.svg`.

## Design intent

- `relay_module_tray_rev_a` is the relay-box shelf ahead of the battery.
- `power_module_box_rev_a` is the smaller side module for the breaker and grouped MIDI bank.
- `power_module_rear_insulator_rev_a` is the non-metal rear shield for the power module.

## Material callouts

- Relay tray: `3.0 mm 5052-H32 aluminium`
- Power module box: `3.0 mm 5052-H32 aluminium`
- Rear insulator: `3.0 mm ABS, HDPE, or polypropylene`

## Bend notes

- Bend all bend-line flanges to `90 degrees`.
- Target inside bend radius: `3 mm` nominal.
- Corner relief is open-corner style by design; no corner welding is required.

## Hardware assumptions

- Relay box housing used for sizing: `300 x 197 x 80 mm`
- Relay box mount pattern remains image-derived and is therefore slotted on purpose.
- Breaker body used for sizing: `74 x 49 x 45 mm`
- MIDI grouped bank is treated as a slotted universal field because the exact AliExpress mounting pattern was not published.

## Vehicle-side fitment

The truck-side pickup points are intentionally slotted rather than final-drilled because:

- the battery tray shown in the photos is not yet a trusted structural reference
- the final repaired tray and inner-wing support positions need to be confirmed on the truck
- a fabricator can site-fit tabs or stand-offs after mock-up

## Installation guidance

- Rebuild or brace the battery tray before installing the relay tray.
- Mount the relay tray with at least `3` structural pickups: tray/front-rail, inner-wing side, and one forward support if available.
- Mount the power module on the inner-fender side of the battery area with the breaker reset lever facing upward.
- Use insulated boots on all live studs.
- Use clamp strips with the MIDI slot field if the supplied fuse bank does not have a strong mounting flange.

## Source basis

- Relay box dimensions from the DAIER / AliExpress relay-box listing used earlier in this thread.
- Breaker body dimensions from the Mughal Electronics product page used earlier in this thread.
- MIDI holder sizing informed by Littelfuse MIDI-Flex holder dimensions (`78.4 x 29.9 x 38.3 mm`) and a 5-position grouped layout.
