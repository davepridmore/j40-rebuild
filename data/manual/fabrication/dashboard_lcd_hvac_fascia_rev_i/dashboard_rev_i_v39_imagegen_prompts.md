# V39 image-generation prompt log

Mode: built-in `image_gen` editing; no fallback image pipeline was used.

The outputs are appearance studies only. They are not dimensional evidence and must not be traced for fabrication.

## V39A body-colour centre bay

Base image: `dashboard_rev_i_v37_flush_inset_screen.png`

Output: `dashboard_rev_i_v39a_glovebox_line_body_colour.png`

```text
Make a highly constrained panel-seam edit to this exact 1840 × 853 straight-on dashboard image. Preserve all existing content, component geometry and positions exactly. Do not repaint or change any area outside the explicitly defined centre panel.

Define one removable centre panel only within the existing central band between the glovebox and cluster. Use these approximate source-image landmarks to prevent drift: its upper-left begins around (595,125), immediately beside the glovebox's right upper shoulder; its left edge tracks the glovebox's existing curved/sloping right-hand perimeter down to about (610,345), then reaches the original lower dash edge near (610,395). Its upper-right begins around (1165,125), immediately beside the instrument pod's left upper shoulder; its right edge tracks the pod's curved/sloping left-hand perimeter down to about (1105,345), then reaches the original lower dash edge near (1105,395). Join the upper endpoints along the existing upper dashboard line and the lower endpoints along the existing full-width lower dashboard line. This creates one irregular four-sided centre-bay insert. Absolutely no part of the insert may appear to the left of the glovebox's right edge, above or behind the glovebox, to the right of the cluster's left edge, above or behind the cluster, or around either OEM assembly.

Finish the centre insert in matching warm ivory/cream metal. Show its exact perimeter with a thin continuous 2–3 mm charcoal service gap, including the edge that runs alongside the glovebox and the edge alongside the cluster. Do not draw a rectangle around the screen. The screen and full control row remain flush-mounted through this larger bay panel exactly where they are. No rounded plaque, no colour block behind the glovebox or cluster, no added vents, no visible screws, no changed labels or controls, no relocation or resizing of anything.
```
## V39B charcoal finish

Base image: V39A generated output.

Output: `dashboard_rev_i_v39b_glovebox_line_charcoal.png`

```text
Create a finish-only variant of this exact dashboard concept. Preserve the entire image, camera, geometry, panel outline, continuous service-gap line, glovebox, instrument cluster, screen, all controls, labels, levers, vents, background and lighting exactly. Do not change the context-shaped centre-panel perimeter in any way.

Recolour only the material inside the existing outlined removable centre panel—the irregular four-sided bay panel whose left edge runs alongside the glovebox and whose right edge runs alongside the cluster—to fine-texture low-gloss satin charcoal-black powder-coated metal. Retain the existing thin warm-cream perimeter service gap. Keep the screen flush and coplanar. Do not colour any dashboard area outside the existing outline, do not put black behind the glovebox or cluster, and do not add or remove anything.
```

## V39C walnut finish

Base image: V39A generated output.

Output: `dashboard_rev_i_v39c_glovebox_line_walnut.png`

```text
Create a finish-only variant of this exact dashboard concept. Preserve the entire image, camera, geometry, panel outline, continuous service-gap line, glovebox, instrument cluster, screen, all controls, labels, levers, vents, background and lighting exactly. Do not change the context-shaped centre-panel perimeter in any way.

Change only the face material inside the existing outlined removable centre panel—the irregular four-sided bay panel whose left edge runs immediately alongside the glovebox and whose right edge runs immediately alongside the cluster—to thin warm medium-walnut automotive veneer bonded to a rigid metal carrier. Use subtle straight horizontal grain, medium brown colour and a restrained low-gloss satin clear coat; it must look like thin veneer, not thick carved wood. Retain a narrow dark metal edge band and the existing 2–3 mm cream service gap around the exact perimeter. Keep the screen flush and coplanar and all controls passing through the same panel. Do not apply wood outside the outlined centre panel, do not put wood behind the glovebox or cluster, and do not add, remove, move or resize anything.
```
