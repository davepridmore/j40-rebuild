# Symmetric dashboard layout study — 2026-08-01

This folder contains the original paired Rev H four-outlet studies and the later standalone Rev I studies. **V15 is the current owner-selected straight-on appearance direction:** exactly two high outer/end outlets, the original Toyota speedometer and large asymmetric glovebox, a deleted/closed-over ashtray, a geometrically centred 9-inch LCD, the purchased MOMO wheel, the original-height visual target, the factory steering-column relief and the complete compact seven-selector-plus-hazard bank. V15 begins with the intact cluster-to-column relationship shown in the installed owner photograph and the scallop shown in the straight-on bare-shell photograph; it does not translate the cluster to make room for the screen. V9–V14 are superseded design history; the unpublished V14 intermediate was rejected because it retained the ashtray as if it were a second glovebox. The controlled current package and space audit are in the [Rev I specification](../../dashboard_lcd_hvac_fascia_rev_i/README.md).

These PNG files are photorealistic selection aids, not scale drawings. AI-edited pixels must never be measured or sent to a CNC toolpath. For Rev I, only bought-component measurements, a perpendicular full-face vehicle trace, a full-size/full-depth template and the M1–M10 release gates control geometry. The Rev H DXF/CSV files control the superseded Rev H record only and must not be reused as Rev I production coordinates.

## Common locked geometry — Rev H variants only; not V9–V15

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
- `layout_b_column_v9_momo_two_central_vent_oem_height_straight_on.png` — superseded Rev I study with two central outlets; retained for design history.
- `layout_b_column_v10_momo_two_outer_vent_factory_relief_straight_on.png` — superseded outer-vent study; cluster remained too high above the column shroud.
- `layout_b_column_v11_momo_two_outer_vent_lowered_oem_cluster_straight_on.png` — superseded correction study; improved the cluster/column relationship but did not yet reproduce the actual installed cluster height or exact LCD centre.
- `layout_b_column_v12_momo_two_outer_vent_actual_cluster_centered_lcd_straight_on.png` — superseded alignment study; established the lower cluster/column relationship but simplified the cluster identity and left the LCD fractionally high/right.
- `layout_b_column_v13_momo_two_outer_vent_oem_cluster_centered_lcd_straight_on.png` — superseded alignment study; improved the cluster/LCD relationship but rendered the passenger-side glovebox/ashtray identity incorrectly and left the visible face too deep.
- `layout_b_column_v15_momo_two_outer_vent_oem_glovebox_ashtray_delete_original_height_centered_lcd_straight_on.png` — **current Rev I visual baseline** with two high outer/end outlets, the large original glovebox correctly retained, the separate smaller ashtray deleted and closed over, the OEM cluster at the installed-photo relationship, the compact factory relief, the shallower original-height silhouette target and the 9-inch active image centred on the complete fascia.
- `layout_c_central_vent_sill_assembled.png`
- `layout_c_central_vent_sill_bare_shell.png`

## Selected B — factory steering-column correction

The two `layout_b_factory_column_relief_*` images revise the selected deep-low-twins study without changing its LCD, four-outlet, OEM-instrument, OEM-glovebox or seven-selector-plus-hazard layout.

- `layout_b_factory_column_relief_assembled.png` restores the wheel, hub, column, shroud, stalks, scale and shallow installed angle from owner photo `photos/20260317_165113.jpg`. The wheel projects leftward toward the camera, but the column entry at the dashboard plane is directly below the retained speedometer.
- `layout_b_factory_column_relief_bare_shell.png` restores the original lower instrument-aperture scallop using owner photo `photos/20260413_040719.jpg` as the visual control.
- Rev H continues to show a nominal column/cluster centre at X=930 mm, nominal relief X=865…995 mm (130 mm wide) and nominal 32 mm rise. These are packaging references only. The factory opening, installed column, shroud, stalk sweep and required running clearance must be directly traced at M1/M3/M9 before CNC release.
- The new one-piece fascia must wrap around the signed factory column passage; it must not bridge the opening with a continuous flat lower edge or force the column away from its original position.

## Selected B — historical OEM glovebox / left-outlet correction

The two `layout_b_glovebox_clear_*` images supersede the earlier selected-B visualization where the left outer outlet crossed the movable glovebox zone and the generated lid silhouette was not faithful to the vehicle. They are historical Rev H records and do not supersede V15.

- The owner photos `photos/20260413_040719.jpg`, `photos/20260323_185947.jpg` and `photos/20260323_190005.jpg` show two different original parts: the large asymmetric silver-grey door with the black Japanese instruction plate and upper black knob is the retained glovebox; the smaller silver pull-out immediately to its right is the ashtray. The glovebox is a visual and physical no-touch region. Rev I deletes and closes over the ashtray.
- V1 is fully outboard on fixed fascia metal. A continuous body-colour strip separates its complete silver bezel from the lid in both views; no portion of its aperture, retainer, duct or service land may enter the lid perimeter, hinge/latch hardware, opening or full sweep.
- The nominal model already encodes this relationship: the V1 Ø87 bezel ends at X=93.5 and the glovebox transfer envelope starts at X=152.0, a nominal 58.5 mm separation. Require at least 10 mm real fixed-metal land after the direct vehicle trace. The M2 trace, M7 bought sample and M8/M9 full rear mock-up control release.
- The assembled view preserves the factory wheel/column and natural occlusion. The paired bare-shell view remains the count and placement control for all four outlets.

## Rev H visualisation record — historical four-outlet variants; not V9–V15

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

## V9 / superseded Rev I two-central-outlet study

V9 was an intermediate owner-selected straight-on direction. V10 superseded it for outlet placement; V15 now controls the visual speedometer/column/lower-edge, glovebox/ashtray and LCD-centre relationships. V9 does not convert the superseded Rev H DXF/CSV coordinates into Rev I production geometry.

- Replace the visual factory wheel with the procured `INV-0005` MOMO carbon-fibre-pattern three-spoke wheel. The [archived vendor listing](https://www.pakwheels.com/accessories-spare-parts/momo-carbon-fiber-steering-wheel-11011689) identifies a nominal **350 mm diameter** and approximately **90 mm depth**; the actual wheel and required vehicle-specific boss/adapter must be measured on the column before packaging or steering-clearance release.
- Retain exactly **two** matched circular silver occupant outlets. They are level with one another and mirror-symmetric about the 9-inch LCD/fascia centreline. Delete both former end outlets and all four-outlet branch implications.
- Keep both outlet faces inside the original shallow full-width fascia-height envelope. V9 has no lower vent pods and no full-width downward extension; the factory steering-column passage remains the only local lower-edge relationship that must be transferred from the vehicle.
- Retain the original large asymmetric glovebox and speedometer identities and the centred 9-inch display; delete the separate smaller ashtray. Retain the complete far-right control allocation: `WIPERS | LIGHTS | SPOTS | AUX.` above `BLOWER | A/C | ENGINE | HAZARD`, comprising exactly seven black selectors plus one separate red hazard.
- The outlet centres, apertures, necks, rear elbows, LCD chassis, MOMO boss/adapter and switch contact stacks remain **HOLD** until the Rev I M1/M4/M6/M7/M8/M9 physical measurements and full-depth mock-up are signed. Do not measure pixels from this image and do not issue CNC paths from it.

V9 prompt intent: built-in `image_gen`, local-reference precise object editing; use the accepted V6 straight-on owner-photo composition, show the procured MOMO wheel, remove the two outer outlets and lower pods, place only the two remaining centre outlets on one horizontal datum at equal offsets from the LCD centreline, return the fascia to its original shallow height, move the unchanged eight-position control bank clear of wheel occlusion, and restore the OEM glovebox and complete four-lower-gauge Toyota meter identity directly from the accepted source. The generated image is a photorealistic design-selection aid, not a scale drawing.

## V10–V15 Rev I outer-outlet, factory-height study

V15 is the current visual baseline. V10 established the two-outer-outlet and original-height composition but left the cluster too high. V11 moved it closer to the installed relationship but still left excess body-colour land below the cluster. V12 improved the lower cluster/column relationship but simplified the original cluster and left the LCD fractionally high/right. V13 restored the taller OEM-cluster appearance and centred LCD, but merged/misread the passenger-side forms and left the visible face too deep. V14 separated the two original silver-grey forms but incorrectly retained the smaller ashtray. V15 preserves the installed cluster/column and centred LCD, restores the shallower normal lower edge, keeps the large plate-and-knob OEM glovebox, and deletes the smaller ashtray into smooth body-colour fascia.

- Use exactly **two** matched large circular silver occupant outlets, level at the high fixed outer ends. Their centres are controlled separately by the measured fixed end lands and rear duct packages; they do not establish, average or alter the LCD centre. There are no central outlets and no lower vent pods.
- Keep the true 9-inch landscape LCD central. Its active-image reference remains **199.2 × 112.1 mm**, **228.6 mm / 9.000-inch diagonal**. At M1, place the active-image centre at the midpoint of the signed complete front-face width and the midpoint between the signed top fold and normal lower edge at the LCD station; the shown bezel is a visual reference, not a released cutout.
- Preserve the original Toyota speedometer and large asymmetric glovebox identities and factory locations. The glovebox is the plate-and-upper-knob door; do not model the separate smaller ashtray as another glovebox. Close the ashtray aperture without a seam, lid or handle. The centre of the main speedometer dial, column relief, black column/shroud and steering-wheel hub must lie on the directly traced vehicle centreline.
- Preserve the original shallow normal lower edge. Only the compact upward-opening factory U/scallop wraps the column; do not add a broad column pod, circular collar or full-width lower extension.
- Retain exactly **seven black selectors plus one red hazard** in the compact 4 × 2 right bank: `WIPERS | LIGHTS | SPOTS | AUX.` above `BLOWER | A/C | ENGINE | HAZARD`. The selector cut reference is Ø22.5 mm, but the bought heads, anti-rotation features, 68 mm rear stacks, lever sweep and label lands remain M6/M8/M9 HOLD.
- The MOMO wheel is vendor-listed at nominal **350 mm diameter** and approximately **90 mm depth**. The actual wheel, boss/adapter and installed column position control clearance.

The photographs establish shape and alignment, not millimetre scale. In particular, the nominal 1260 mm face width, 170 mm normal face height, X=930 mm column axis, 130 × 32 mm relief and 130 × 105 mm sweep envelope remain layout assumptions only. Before a CNC metal release, M1 must capture a perpendicular physical trace of the top flange, both ends, normal lower edge, large glovebox and cluster openings, the former ashtray aperture, the complete installed cluster position and the original column scallop. M2 must separately trace the glovebox perimeter, hardware and full opening sweep before the ashtray aperture is closed in CAD. M3/M6/M8/M9 must then prove the installed column angle and full movement, retained cluster depth, switch rear stacks, two vent necks/ducts, screen body/connectors and service paths in a rigid full-size, full-depth mock-up. Do not derive dimensions, cluster artwork or cut geometry from V15 pixels.

V11 prompt intent: preserve the V10 composition and change only the cluster height; use the installed owner photo as the meter/column/lower-edge control and the bare-shell photo as the scallop-shape control; lower the complete original cluster immediately above the shroud; align the main dial, compact relief, column and hub; retain the shallow normal edge, original glovebox, central 9-inch LCD, two high outer vents, MOMO wheel and exact eight-device control allocation. The generated image is a selection and trace-planning aid, not CNC input.

V12 prompt intent: built-in `image_gen`, local-reference precise object editing; use the installed owner photograph as the immutable speedometer, column-opening and dashboard-height datum; keep the complete OEM cluster at that exact installed position and preserve the top and normal lower edges; move only the unchanged true-9-inch 16:9 LCD so its centre coincides with the midpoint between the two fixed outer vent centres and the complete fascia centre; retain the original glovebox, two high outer vents, MOMO wheel and exact seven-selector-plus-hazard allocation. The generated image is a selection and trace-planning aid, not CNC input.

V13 prompt intent: built-in `image_gen`, local-reference precise object editing; use `photos/20260317_165113.jpg` for intact cluster identity and cluster-to-column relationship, use `photos/20260413_040719.jpg` for the straight-on aperture and deep factory U/scallop, preserve the shallow fascia silhouette and normal lower edge, and move only the unchanged true-9-inch 16:9 LCD onto the complete-face geometric centre. The two end outlets remain governed independently by their measured fixed lands. The generated image is a selection and trace-planning aid; AI-rendered gauge lettering and pixels are not CNC evidence.

V15 prompt intent: built-in `image_gen`, local-reference precise object editing; preserve the accepted V14 composition, component scale, shallow top/lower edges, centred true-9-inch 16:9 LCD, installed OEM cluster/column relationship, MOMO wheel, two high outer vents and exact seven-selector-plus-hazard bank. Identify the plate-and-upper-knob asymmetric door as the sole retained glovebox; remove the separate smaller silver ashtray immediately to its right, including its pull, seam, recess and hardware, and close that area with uninterrupted body-colour fascia. Do not move or resize any other component. The generated image is a selection and trace-planning aid; the signed M1/M2 vehicle trace controls CNC geometry.
