# J40 Relay and Fuse Back-Plates - CNC Specification Rev A

Units are millimetres. Scale all DXFs at `1:1`. This handoff consolidates the current Relay Rev D base/insulator and the five-way MIDI fuse-holder back-plate. It does not replace the enclosing relay-box cover or the MIDI enclosure.

## Order quantity and material

| Part ID | Quantity | Finished size | Material | Thickness | Source DXF |
| --- | ---: | --- | --- | ---: | --- |
| `J40-EBP-001` relay structural back-plate | 1 | `360 x 245` | 5052-H32 aluminium | `3.0` | `../relay_mount_rev_d/relay_base_plate_rev_d.dxf` |
| `J40-EBP-002` relay insulating back-plate | 1 | `300 x 197` | G10/FR-4 preferred; HDPE, ABS, polypropylene, or phenolic acceptable | `3.0` | `../relay_mount_rev_d/relay_insulating_sheet_rev_d.dxf` |
| `J40-EBP-003` five-way MIDI fuse-holder back-plate | 1 | `140 x 85` | G10/FR-4 preferred; HDPE, ABS, or phenolic acceptable | `5.0` | `../midi5_enclosure_rev_d/midi5_holder_subplate_rev_d.dxf` |

Material must be electrically non-conductive for parts `002` and `003`. Do not substitute aluminium or steel. G10/FR-4 is preferred in the hot engine bay; if a thermoplastic is used, confirm its continuous temperature rating and keep it away from exhaust heat.

## CNC geometry

Datum is the lower-left corner of each DXF, viewed from the component side. Coordinates are hole/slot centres unless stated otherwise.

### J40-EBP-001 - relay structural back-plate

- Rectangular outside profile: `360.0 x 245.0`.
- Four horizontal obround slots, each `34.0 x 10.0`, end radius `5.0`:
  - `(67.0, 12.0)`
  - `(293.0, 12.0)`
  - `(67.0, 233.0)`
  - `(293.0, 233.0)`
- Four vertical obround slots, each `10.0 x 34.0`, end radius `5.0`:
  - `(13.0, 103.0)`
  - `(13.0, 160.0)`
  - `(347.0, 103.0)`
  - `(347.0, 160.0)`
- Do **not** cut relay-box fixing holes yet. Clamp the actual relay enclosure and part `002` in their final orientation, transfer the enclosure's bottom fixing pattern, then drill the complete stack to suit the actual hardware.

### J40-EBP-002 - relay insulating back-plate

- Rectangular outside profile only: `300.0 x 197.0`.
- No CNC holes in this release. Transfer-drill with the actual relay enclosure and part `001` after orientation and cable-exit clearance are confirmed.
- The insulator must cover the complete uncovered `300 x 197` bottom footprint of the relay enclosure, with no metal swarf or sharp edges trapped beneath it.

### J40-EBP-003 - five-way MIDI fuse-holder back-plate

- Rectangular outside profile: `140.0 x 85.0`.
- Ten fuse-holder holes: diameter `4.5`.
  - Row 1: `(11.0, 20.0)`, `(31.2, 20.0)`, `(51.4, 20.0)`, `(71.6, 20.0)`, `(91.8, 20.0)`
  - Row 2: `(21.0, 64.0)`, `(41.2, 64.0)`, `(61.4, 64.0)`, `(81.6, 64.0)`, `(101.8, 64.0)`
- Six standoff holes: diameter `5.5`:
  - `(15.0, 10.0)`, `(70.0, 10.0)`, `(125.0, 10.0)`
  - `(15.0, 75.0)`, `(70.0, 75.0)`, `(125.0, 75.0)`
- Mount on `10-12 mm` insulated or fully sleeved standoffs inside the MIDI enclosure.

## Manufacturing requirements

- DXF model-space units: millimetres; import scale `1:1`.
- Profile tolerance: `+/-0.25 mm`; hole/slot position tolerance: `+/-0.20 mm`; hole diameter tolerance: `+0.15/-0.00 mm`.
- Keep parts flat within `0.5 mm` over the full diagonal.
- Break all edges `0.2-0.5 mm`; deburr both faces. No sharp edges, burrs, loose fibres, or conductive swarf.
- For aluminium, use a non-conductive corrosion barrier wherever it contacts dissimilar metal. Finish after transfer-drilling; clear all earth/contact locations only where the electrical design explicitly requires them.
- For G10/FR-4 or phenolic, use dust extraction and appropriate PPE. Do not flame-polish.
- Do not apply cutter compensation by altering the CAD geometry. Program compensation in CAM.
- Do not add countersinks, counterbores, threaded inserts, engraving, or extra holes without approval.

## Fit and release checks

1. Verify the DXF bounding box and one known pitch before cutting: `360 x 245` for `001`, `300 x 197` for `002`, and `20.2 mm` holder-hole pitch for `003`.
2. Dry-fit the relay cover, top power exits, end loom exits, and service access before transfer-drilling the relay stack.
3. Dry-fit all five MIDI holders and confirm stud/terminal clearance to the enclosure and lid.
4. Fit insulating boots/caps to live studs and rubber grommets to cable exits before wiring.
5. Reject any plate with warped stock, chipped insulation, elongated round holes, or burrs capable of damaging insulation.

## Release status

- `J40-EBP-001`: CNC-ready for outside profile and eight stand-attachment slots; relay-box holes are intentionally deferred.
- `J40-EBP-002`: CNC-ready for outside profile only; fixing holes are intentionally deferred.
- `J40-EBP-003`: CNC-ready as drawn, subject to a physical sample check of one MIDI holder before the full job is accepted.

