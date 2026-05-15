# J40 Electrical Device Models - Rev A

This is a reference visualisation pack for the physical electrical devices used by the battery-side fabrication layouts.
It separates the devices from the carrier brackets so the relay box, 100A breaker/cutoff, and MIDI fuse holders can be checked as objects before judging the combined battery power carrier view.

## Modelled Devices

- Relay/fuse box: photo-informed covered black enclosure with plain removable front cover, two cover screws, left-hand heavy power input/output boots, top control-cable relief, and left-side service-loop volume. The released sizing basis remains `300 x 197 x 80 mm`; internals are hidden by the fitted cover. The modelled exit blocks are left power input `46 x 54 x 42 mm` at relay offset `X-164 / Y+42 / Z-52`, left power output `46 x 54 x 42 mm` at `X-164 / Y-42 / Z-52`, and top control cables `170 x 24 x 34 mm` at `X-18 / Y+110 / Z-58`.
- 100A breaker/cutoff: photo-informed waterproof resettable breaker with black body, raised faceplate, red reset lever/button, two terminal studs, ring lugs, and cable boots. Exact body/stud centres remain a caliper hold before final drilling.
- MIDI fuse holder bank: active five-position fabrication model on the known `140 x 85 mm` insulated subplate, using red hinged covers, black linked bases, side mounting ears, latch recesses, paired studs, a single common-feed side, and a seated five-output cable comb/gland strip attached to a guide backplate and support tabs. Output 3 is marked with an enlarged pass-through because that output carries two wires. The received photo shows a larger linked bank; the active fabrication package is still the five-way Rev C plate.
- Hidden/security needle switch: shown only as a small reference object, because it belongs to the cabin/security wiring path rather than the battery-side power carrier.

## Evidence Basis

- Relay/fuse box photos: `photos/20260411_143125.jpg`, `photos/20260515_112827_gp_kbx0JKSQ.jpg`
- 100A breaker/cutoff photos: `photos/20260411_071153.jpg`, `photos/20260515_112836_gp_sFdn9AyA.jpg`
- MIDI holder close-ups: `photos/20260411_143135.jpg`, `photos/20260515_112907_gp_wtj4G8tQ.jpg`
- Hidden/security needle switch photo: `photos/20260420_221819_gp_YV69fbvA.jpg`

## Release Notes

These models are visual envelopes, not fabrication drawings. Use them to check packaging and service access in the S3 dashboard. Use the existing Rev C fabrication packages for cut files, and measure the actual breaker body, mounting-hole centres, stud spacing, and cable-lug sweep before drilling metal.
