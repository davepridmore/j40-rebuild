# Symmetric dashboard layout study — 2026-08-01

This folder contains three paired visual studies applied to both locked owner-photo views. They preserve the right-hand-drive arrangement, original Toyota speedometer/instrument assembly, original glovebox, centred 9-inch LCD, four equal circular silver outlets, and the compact seven-selector-plus-hazard bank.

These PNG files are photorealistic selection aids, not scale drawings. AI-edited pixels must never be measured or sent to a CNC toolpath. The Rev H DXF/CSV geometry, bought-component measurements, full-size template, vehicle trace and M1–M10 release gates remain controlling.

## Common locked geometry

- Nominal fascia coordinate width: 1260 mm; centreline: X=630 mm.
- LCD active image: 199.2 × 112.1 mm, 228.6 mm / 9.000-inch diagonal, 16:9.
- LCD bezel reference: 224 × 136 mm, centred at X=630 mm / Y=144 mm.
- Four matching outlets: Ø87 mm visible silver face, Ø75 mm opening reference.
- Outer outlet centres: X=50 mm and X=1210 mm, Y=168.5 mm.
- Right controls: exactly seven Ø22.5 mm industrial rotary selectors plus one separate red hazard in a compact 4 × 2 grid.
- Control labels: WIPERS, LIGHTS, SPOTS, AUX. / BLOWER, A/C, ENGINE, HAZARD.

## Variants

| Variant | Inner outlet centres | Lower treatment | Purpose / trade-off |
|---|---|---|---|
| A — wide low twins | X=458.5 / 801.5 mm, Y=20 mm | Two 112 mm-wide local pods to Y=-35 mm | Best overall balance. Exact mirror spacing about X=630, 12.5 mm nominal vertical LCD clearance and about 16 mm horizontal side clearance. |
| B — deep low twins | X=458.5 / 801.5 mm, Y=8 mm | Two 112 mm-wide local pods to Y=-47 mm | Gives 24.5 mm nominal vertical LCD clearance and more rear neck/elbow depth, but creates the deepest local projection. In the assembled camera view, the steering wheel naturally partly hides the left-inner outlet. |
| C — central vent sill | X=480 / 780 mm, Y=20 mm | One continuous rounded sill, approximately X=418…842 mm to Y=-35 mm | Strongest visual symmetry and a single calm lower form; requires the most careful rear sill, duct and steering-column mock-up. |

The rejected high-inner-outlet arrangement is intentionally absent: the right inner outlet would overlap the retained OEM speedometer envelope.

## Files

- `comparison_assembled.png` — the three driver-eye views side by side.
- `comparison_bare_shell.png` — the three straight-on views side by side.
- `layout_a_wide_low_twins_assembled.png`
- `layout_a_wide_low_twins_bare_shell.png`
- `layout_b_deep_low_twins_assembled.png`
- `layout_b_deep_low_twins_bare_shell.png`
- `layout_b_factory_column_relief_assembled.png`
- `layout_b_factory_column_relief_bare_shell.png`
- `layout_b_glovebox_clear_assembled.png`
- `layout_b_glovebox_clear_bare_shell.png`
- `layout_b_column_v4_clearance_assembled.png` — assembled correction record; not a scale drawing or CNC input.
- `layout_b_column_v5_clear_assembled.png` — oblique installed view with the original column/shroud visibly continuous from hub to factory relief.
- `layout_b_column_v5_straight_on.png` — matching frontal installed view with the RHD hub/shaft centreline beneath the original meter.
- `layout_b_column_v6_switches_clear_assembled.png` — selected oblique V6 view with the full column visually explicit and the complete compact control bank shifted down/right.
- `layout_b_column_v6_switches_straight_on.png` — matching frontal V6 view with the same revised control-bank location and natural wheel occlusion.
- `layout_c_central_vent_sill_assembled.png`
- `layout_c_central_vent_sill_bare_shell.png`

## Selected B — factory steering-column correction

The two `layout_b_factory_column_relief_*` images revise the selected deep-low-twins study without changing its LCD, four-outlet, OEM-instrument, OEM-glovebox or seven-selector-plus-hazard layout.

- `layout_b_factory_column_relief_assembled.png` restores the wheel, hub, column, shroud, stalks, scale and shallow installed angle from owner photo `photos/20260317_165113.jpg`. The wheel projects leftward toward the camera, but the column entry at the dashboard plane is directly below the retained speedometer.
- `layout_b_factory_column_relief_bare_shell.png` restores the original lower instrument-aperture scallop using owner photo `photos/20260413_040719.jpg` as the visual control.
- Rev H continues to show a nominal column/cluster centre at X=930 mm, nominal relief X=865…995 mm (130 mm wide) and nominal 32 mm rise. These are packaging references only. The factory opening, installed column, shroud, stalk sweep and required running clearance must be directly traced at M1/M3/M9 before CNC release.
- The new one-piece fascia must wrap around the signed factory column passage; it must not bridge the opening with a continuous flat lower edge or force the column away from its original position.

## Selected B — OEM glovebox / left-outlet correction

The two `layout_b_glovebox_clear_*` images supersede the earlier selected-B visualization where the left outer outlet crossed the movable glovebox zone and the generated lid silhouette was not faithful to the vehicle.

- The owner photos `photos/20260317_165113.jpg` and `photos/20260413_040719.jpg` control the glovebox's original shallow rounded outline, position, knob/latch, black instruction plate, colour and patina. The lid is a visual and physical no-touch region.
- V1 is fully outboard on fixed fascia metal. A continuous body-colour strip separates its complete silver bezel from the lid in both views; no portion of its aperture, retainer, duct or service land may enter the lid perimeter, hinge/latch hardware, opening or full sweep.
- The nominal model already encodes this relationship: the V1 Ø87 bezel ends at X=93.5 and the glovebox transfer envelope starts at X=152.0, a nominal 58.5 mm separation. Require at least 10 mm real fixed-metal land after the direct vehicle trace. The M2 trace, M7 bought sample and M8/M9 full rear mock-up control release.
- The assembled view preserves the factory wheel/column and natural occlusion. The paired bare-shell view remains the count and placement control for all four outlets.

## Visualisation record

Mode: built-in `image_gen`, local-reference `precise-object-edit`.

Prompt intent: preserve both original photographs, camera viewpoints, cream colour and patina; preserve the OEM speedometer and glovebox; keep a true 9-inch 16:9 LCD centred at the fascia centreline; use four equal Ø87 silver circular outlets with the two outer outlets at the far ends and the inner pair exactly mirrored about the LCD; retain exactly seven black rotary selectors plus one red hazard at the extreme right; change only the inner-outlet spacing, vertical location and local pod/sill treatment for each variant.

Factory-column correction prompt intent: treat `photos/20260317_165113.jpg` as the immutable assembled camera/steering base, the accepted B image as the dashboard-layout control and `photos/20260413_040719.jpg` as the lower-edge/cutout control; preserve the factory-size wheel and shallow column angle; keep the accepted LCD, four-outlet and control allocation; align the column entry beneath the OEM speedometer; and restore the original rounded U/scalloped relief with shroud clearance. In the assembled view, the wheel naturally hides most of the left-inner outlet; the paired bare-shell view records all four outlet positions clearly.

Glovebox-clearance correction prompt intent: make only a local edit around the OEM glovebox and V1; restore the exact owner-photo lid identity and hardware; move the complete Ø87-style V1 face outboard onto fixed fascia with visible body-colour separation; keep its rear package outside the full glovebox opening sweep; and freeze the accepted LCD, cluster, column, inner outlets, V4 and seven-selector-plus-hazard allocation.

The assembled images show perspective and genuine steering-wheel occlusion. The straight-on bare-shell images are the clearer layout-comparison views. Neither view proves millimetre accuracy.

## V4 / steering-column assembled correction

`layout_b_column_v4_clearance_assembled.png` is a precise-object-edit correction record. It restores only the short horizontal matte-black steering-column/shroud segment from the hub into the factory lower-instrument relief; it must not be interpreted as a spoke or diagonal tube. It also lowers the complete 2 × 4 control bank enough to show approximately one actual selector-head diameter between V4 and the nearest selector. All other dashboard identity is frozen.

The V6 straight-on view now supersedes the earlier views for control-bank placement. With the nominal Ø22.5 selector head, the revised model gives **35.75 mm** vertical separation from the V4 lower rim to the nearest nominal head datum and **19 mm** to the conservative bank/label envelope. The generated `../rear_envelope_fit_audit_20260801.md` and M6/M8/M9 still require the bought parts to prove ≥20 mm visible-head clearance and ≥10 mm rear V4 retainer/neck/elbow/duct clearance to the real contact blocks, terminals and wiring. Do not move V4 farther right: its nominal visible-face / Ø75-reference end lands are already 6.5 / 12.5 mm.

## V5 / installed steering-column pair

The V5 pair makes the column relationship explicit in both useful viewpoints without changing the selected Rev H allocation.

- `layout_b_column_v5_clear_assembled.png` shows one continuous near-horizontal matte-black original-style column/shroud from the wheel hub into the factory radiused lower-instrument relief.
- `layout_b_column_v5_straight_on.png` is the matching square-on installed view. The steering hub and shaft are aligned directly beneath the retained OEM meter on the right-hand-drive side; the large original-style wheel naturally occludes portions of the right inner outlet and control area.
- Both views retain the original glovebox identity, the original meter identity, the central true-9-inch visual reference, four outlets and exactly seven black selectors plus the separate red hazard.
- These are photorealistic placement/occlusion records only. They do not supersede the Rev H coordinates, the original vehicle column/opening trace, or the M1/M3/M8/M9 full-depth physical checks.

V5 prompt intent: built-in `image_gen`, local-reference `precise-object-edit`; treat owner photos `photos/20260317_165113.jpg` and `photos/20260323_190047.jpg` as the steering geometry controls, visibly connect the hub to the factory relief, align the straight-on hub/shaft beneath the OEM meter, and freeze all approved dashboard components and counts.

## V6 / explicit side-view column and centred compact controls

The V6 pair supersedes V5 as the selected installed visualization.

- The oblique view makes the original matte-black steering column/shroud unambiguous from the existing wheel hub to the retained factory relief directly beneath the OEM speedometer.
- In both views the complete bank moves as one unit—no function is rearranged—and remains exactly seven black selectors plus one separate red hazard.
- Nominal control centres are X=1120 / 1160 / 1200 / 1240 mm and Y=78 / 20 mm. The 40 mm horizontal pitch compacts the group and shifts its visual centre right; both rows are 10 mm lower than V5.
- The bank is centred in a 151 × 103 mm local envelope at X=1104 / Y=3. The lowest dashboard datum remains Y=3 in this zone, so the change uses the existing control channel and adds no dashboard height.
- Labels remain WIPERS, LIGHTS, SPOTS, AUX. / BLOWER, A/C, ENGINE, HAZARD. The M6 1:1 trial must confirm the bought selector-head diameter, lever sweep, hand clearance and engraving before apertures are released.

V6 prompt intent: built-in `image_gen`, local-reference `precise-object-edit`; preserve all approved components and vehicle identity, change only side-view column legibility and the whole switch-bank translation/compaction, and retain natural steering-wheel occlusion in the straight-on view.
