# Rev H cooling-pack AI visual record

**Issue:** 1 August 2026

**Purpose:** visual explanation for the J40 website and Pakistan fabricator handoff
**Status:** illustrative only; do not scale or release fabrication from an AI image

## Controlled relationship

The Rev H written specification, surveyed vehicle centreline C0, the actual vehicle, physical samples, deterministic drawings, full-size dummy and signed measurement/release gates control manufacture. The generated images are appearance and interface aids only.

Rev H retains these Rev G views because their layout purpose is unchanged:

- `work_document_assets/rev_g_ph01_complete_wide_exploded_v2.png` — wide component split-out;
- `work_document_assets/rev_g_ph02_toyota_donor_assembled.png` — off-vehicle assembled pack;
- `work_document_assets/rev_g_ph04_direct_side_ear_closeup.png` — existing-hole/direct-ear detail; and
- `work_document_assets/rev_g_ph05_independent_electrical_mounts.png` — separate Relay/MIDI box concept.

Rev H uses three complementary installed views:

- `work_document_assets/rev_h_ph03a_interface_opaque_centered.png` — normal fully opaque front-installed appearance, **1280 × 659 px**;
- `work_document_assets/rev_h_ph03b_opaque_engine_side_rear.png` — normal fully opaque engine-side rear appearance, **1280 × 720 px**; and
- `work_document_assets/rev_h_ph03_interface_cutaway_centered_final.png` — controlled cutaway explaining the normally hidden layers and centring, **1280 × 660 px**.

PH03A and PH03B are the normal assembled views. PH03C is deliberately retained as an explanatory cutaway. PH03A cannot show the rear mechanical puller through an opaque radiator, while PH03B cannot show the two grille-side electric pushers through that same opaque stack.

## PH03C controlled cutaway record

Rev H replaces the earlier installed cutaway with:

- input: `work_document_assets/rev_g_ph03_complete_stack_cutaway_v2.png`;
- final correction input: `~/.codex/generated_images/019fab7d-e720-7a31-8ba2-a2774a1ebe12/exec-e2be654d-26aa-4bcb-bd93-c610bf56d7df.png`;
- final generated source: `~/.codex/generated_images/019fab7d-e720-7a31-8ba2-a2774a1ebe12/exec-e5f5ea4d-fbda-4908-b52c-9b8abfb674d5.png`;
- controlled web/document copy: `work_document_assets/rev_h_ph03_interface_cutaway_centered_final.png`;
- controlled copy size: **1280 × 660 px**; and
- generation mode: built-in image generation, **precise-object-edit**.

## Base PH03 prompt

```text
Use case: precise-object-edit.
Asset type: photorealistic installed Toyota J40 cooling-pack proposal for a project website and Pakistan fabricator handoff.
Input image: edit this image only; retain its later J40 bare-chassis workshop setting, camera viewpoint, complete three-core stack, all mounts and all visible service connections.

Primary change: make the two equal front electric pusher fans unmistakably horizontally central to the CAR, not merely central on a cropped panel. Establish the vehicle/chassis longitudinal centreline halfway between the left and right radiator uprights. Keep the two fan centres level, with equal left/right offsets from that vehicle centreline and equal uncovered fin bands. The midpoint between the two fan hubs must coincide visually with the vehicle centreline. The fan pair centre-to-centre spacing remains 266 mm in the controlled specification. Shift/rebuild only the removable black twin-fan shroud as needed; do not shift the radiator, condenser, charge cooler, chassis uprights or rear mechanical fan.

Preserve without omission:
- exactly two identical 248 mm front electric pusher fans;
- exactly one large centred engine-driven mechanical puller behind the radiator, visible through the controlled cutaway;
- exactly two large 57 mm beaded aluminium charge-air elbows, one at each end of the slim black horizontal charge cooler;
- exactly two visibly smaller A/C refrigerant fittings on the silver condenser manifold, one #8 upper inlet and one #6 lower outlet;
- exactly two large radiator coolant hose necks on the copper/brass radiator, one upper and one lower, both visibly distinct and temporarily capped;
- radiator filler/cap position, small overflow nipple and lowest drain cock;
- both direct original top-hole M8 mount stacks, short independent ears, radiator side rails and lower weight-carrying saddles;
- all cores, ports, shroud and fans inside the existing two-upright silhouette.

Composition: wide landscape, slightly elevated front three-quarter view, both chassis uprights and enough surrounding vehicle structure visible to judge the car centreline. Natural workshop lighting, credible copper, aluminium, black powder-coated steel, rubber and aged chassis materials.

Constraints: exactly three cores and exactly three fans total; no side radiator, no side fan, no extra-width annex, no transverse carrier, no shared electrical tray, no hoses that hide ports, no people.

Avoid: off-centre fan pair; unequal fan sizes; cropped upright; extra fan; duplicate/missing port; labels, letters, numbers, centreline graphic, arrows, diagram style, fantasy hardware, text or watermark.
```

## Final C0 correction pass

```text
PRECISE OBJECT EDIT of the supplied installed-on-chassis cooling-pack render. Keep the entire image, camera, crop, lighting, chassis rails and uprights, tyres, crossmember, all three heat-exchanger cores, copper radiator end tank and pipe ports, top mounting ears/holes, lower saddles, rear large engine-driven mechanical fan, wiring and every other component pixel-for-pixel unchanged as far as possible. ONLY translate the complete black FRONT twin-electric-fan shroud assembly (both identical round fans, their rings, guards and the shared rectangular shroud as one rigid object) 12 pixels LEFT in this 1746 x 901 source image. Do not resize, rotate, distort or separate the two fans. Their hub centres should finish at approximately x=693 and x=1053, same y, giving an exact pair midpoint x=873 which coincides with the visible vehicle/chassis centreline and rear mechanical-fan hub. Equal left/right spacing about C0 is mandatory. Do not add, remove, duplicate or alter components. The final result must unmistakably show two equal front pusher fans horizontally central to the car, with the large mechanical puller behind the radiator still partially visible.
```

Read-only visual QA on the 1746 × 901 generated source estimated the front hub centres at x ≈ 695 and x ≈ 1056, pair midpoint x ≈ 875.5, and visible vehicle C0 at x ≈ 873–875 from the rear-fan hub and paired chassis references. The render therefore reads centred within approximately 1–3 pixels. This pixel check accepts the explanatory image only; it does not replace the ±2 mm physical fabrication control.

## PH03A normal opaque front-installed view

- edit input: `work_document_assets/rev_h_ph03_interface_cutaway_centered_final.png`;
- final generated source: `~/.codex/generated_images/019fab7d-e720-7a31-8ba2-a2774a1ebe12/exec-39afe805-6a29-4cd7-9038-a3358a29303c.png`;
- controlled web/document copy: `work_document_assets/rev_h_ph03a_interface_opaque_centered.png`;
- controlled copy size: **1280 × 659 px**; and
- generation mode: built-in image generation, **precise-object-edit**.

The accepted edit brief was to preserve the later-J40 chassis, camera, compact installed stack, existing-hole mounts, connections and two equal front fans while rebuilding only the transparent/cutaway area as normal opaque radiator, tanks, shrouds and metalwork. The front pair remains level and visually centred on the car. The large rear mechanical puller remains installed behind the radiator but is naturally hidden in this direction. No transparency, ghosting, exploded spacing, added fan, label, dimension, arrow or watermark was permitted.

PH03A is an appearance aid, not C0 measurement evidence. PH03C/D10/F1 and the physical chassis survey control the **C0 − 133 mm / C0 + 133 mm** fan centres and ±2 mm tolerances.

## PH03B normal opaque engine-side rear view

- reference inputs: `work_document_assets/rev_g_ph01_complete_wide_exploded_v2.png` and `work_document_assets/rev_h_ph03_interface_cutaway_centered_final.png`;
- final generated source: `~/.codex/generated_images/019fab7d-e720-7a31-8ba2-a2774a1ebe12/exec-0726f939-e26e-467f-8751-b26acf688bf3.png`;
- controlled web/document copy: `work_document_assets/rev_h_ph03b_opaque_engine_side_rear.png`;
- controlled copy size: **1280 × 720 px**; and
- generation mode: built-in image generation, **product-mockup / controlled engineering visualization**, followed by **precise-object-edit** for the fuse enclosure.

### Accepted PH03B generation prompt

```text
Use case: product-mockup / controlled engineering visualization.

Create a NEW photorealistic, fully opaque, fully assembled ENGINE-SIDE REAR view of the same Toyota J40 integrated cooling pack represented by the references.

The camera must be physically inside the engine bay, between the engine and radiator, looking FORWARD toward the grille. Use a modest elevated rear three-quarter angle, approximately 25–30 degrees off the vehicle longitudinal axis. The image is looking directly at the rear face of the radiator shroud. Do not show the grille-side/front faces of the heat exchangers.

Dominant visible object:
- one large black existing Toyota 2H engine-driven mechanical puller fan, its complete blades and metal hub plainly visible face-on;
- the fan is exactly centred on vehicle C0 within a full-face sealed black rear shroud;
- the copper/brass coolant radiator is immediately in front of this fan, so only its top tank, side tank/rails and stack thickness may be visible around/alongside the rear shroud;
- the mechanical fan is larger than either individual 248 mm electric fan but remains inside the radiator/shroud envelope.

Installed but hidden:
- the silver A/C condenser, black 500 × 180 × 50 mm charge-air cooler, and common black shroud carrying two equal centred 248 mm electric pusher fans are all installed on the grille side, in front of the radiator;
- because every core and shroud is opaque, the two small electric fans must NOT be visible face-on and must NOT be visible through the radiator;
- at most, a narrow side-edge/profile of the front stack may appear at the far edge to communicate its compact depth;
- only ONE fan face should be visible in this engine-side image: the large mechanical fan.

Installation:
- show both existing tall black Toyota J40 radiator side support brackets and their inward top-return holes;
- show short direct radiator ears attached at those existing holes with vertical M8/washer/sleeved-isolator stacks;
- show lower rubber-isolated saddles carrying radiator weight;
- keep all layers within the original two-upright width;
- keep the covered relay and MIDI fuse enclosures in the existing upper/rear electrical zone without widening the pack.

Composition and style:
- wide landscape 16:9;
- realistic workshop/engine-bay surroundings, credible aged J40 chassis and Toyota 2H engine context;
- natural workshop light; copper/brass, aluminium, black powder-coated steel and rubber;
- normal opaque product photograph, compact and fabrication-plausible.

Critical prohibitions:
- no transparent, translucent or ghosted materials;
- no cutaway opening, removed panel, x-ray or exploded spacing;
- do not show the two front electric fan faces;
- do not vertically stagger separate cores as if side-by-side;
- no fourth fan, side radiator, side fan, extra-width annex or exposed fuse;
- no labels, dimensions, arrows, text, logos or watermark.
```

### Final closed-MIDI correction prompt

```text
Use case: precise-object-edit.

Edit the supplied photorealistic engine-side rear view of the Toyota J40 cooling pack. Keep the entire image, camera, crop, lighting, chassis, engine-bay surroundings, radiator, mounts, hoses, copper tanks, full-face black rear shroud, large centred mechanical fan, relay box and all other components unchanged as closely as possible.

Make one localized correction only: replace the upper-right electrical item that currently shows four brass fuse elements with a fully closed, opaque, gasketed black MIDI fuse enclosure. The lid must be shut and solid black; no fuse, fuse holder, bus bar, live stud or internal metal may be visible through it. Preserve its same compact upper/rear location, within the radiator-upright width, aligned behind/next to the relay enclosure rather than widening the cooling package. It should read as a serviceable weather-protected automotive fuse box with a subtle lid seam and fasteners, not a transparent window.

Critical invariants: fully opaque normally assembled view; exactly one visible fan face, the large engine-driven mechanical puller; the two front electric pushers remain hidden on the grille side; no cutaway, transparency, ghosting, exploded spacing, text, labels, arrows or watermark.
```

PH03B confirms the normal engine-side appearance and the existence of the rear puller. It does not prove exact diameter, fan-to-engine clearance, port angle, hose route or bracket dimension. R0, BRKT, P0, the physical engine/fan, full-size dummy and release gates remain controlling.

## Fabricator reading rule

The image deliberately shows the three circuit types as visually different:

1. two large 57 mm charge-air elbows on the black charge cooler;
2. two smaller refrigerant fittings on the silver A/C condenser; and
3. two large engine-coolant necks, plus filler/overflow/drain, on the copper/brass radiator.

The exact final port thread, side, angle and hose route remain physical-sample-first. Fan centres are not taken from the pixels: set them from surveyed C0 at **C0 − 133 mm** and **C0 + 133 mm**, with pair midpoint and height within the tolerances in the Rev H specification.
