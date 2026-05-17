from __future__ import annotations

from pathlib import Path

import fabrication_drawing_base as base


OUT_DIR = Path("/Users/davidpridmore/IdeaProjects/J40/data/manual/fabrication/midi5_module_rev_a")
base.OUT_DIR = OUT_DIR
base.PDF_NAME = "j40_midi5_module_rev_a_dimension_sheet.pdf"


def midi5_module_box() -> base.Drawing:
    # 260 x 140 face with 20 mm return flanges.
    cut_polys = [
        base.Poly(
            [
                (20, 0),
                (280, 0),
                (280, 20),
                (300, 20),
                (300, 160),
                (280, 160),
                (280, 180),
                (20, 180),
                (20, 160),
                (0, 160),
                (0, 20),
                (20, 20),
            ]
        ),
        base.rounded_slot_poly(72, 6, 16, 8),
        base.rounded_slot_poly(212, 6, 16, 8),
        base.rounded_slot_poly(72, 166, 16, 8),
        base.rounded_slot_poly(212, 166, 16, 8),
        base.rounded_slot_poly(6, 82, 8, 16),
        base.rounded_slot_poly(286, 82, 8, 16),
    ]
    cut_rects: list[base.Rect] = []
    cut_circles = [
        # Front holder-board attachment holes.
        base.Circle(45, 30, 2.25),
        base.Circle(130, 30, 2.25),
        base.Circle(215, 30, 2.25),
        base.Circle(45, 110, 2.25),
        base.Circle(130, 110, 2.25),
        base.Circle(215, 110, 2.25),
        # Rear insulator screw holes on top and bottom flanges.
        base.Circle(60, 10, 2.25),
        base.Circle(150, 10, 2.25),
        base.Circle(240, 10, 2.25),
        base.Circle(60, 170, 2.25),
        base.Circle(150, 170, 2.25),
        base.Circle(240, 170, 2.25),
    ]
    bend_lines = [
        base.Line(20, 20, 280, 20),
        base.Line(20, 160, 280, 160),
        base.Line(20, 20, 20, 160),
        base.Line(280, 20, 280, 160),
    ]
    notes = [
        "5-way MIDI-only module box: 3.0 mm 5052-H32 aluminium. Finished face 260 x 140. Flanges 20 mm back.",
        "This module is for the 5 linked bus-bar MIDI holders only; breaker/cutoff is intentionally omitted from this variant.",
        "Six face holes mount a separate non-conductive holder board. Final fuse-holder ear holes belong in that board after measurement confirmation.",
        "Vehicle-side pickup slots remain site-fit because the repaired tray and side structure are not yet fixed.",
    ]
    return base.Drawing("midi5_module_box_rev_a", 300, 180, cut_polys, cut_rects, cut_circles, bend_lines, notes)


def midi5_holder_subplate() -> base.Drawing:
    cut_polys = [base.Poly([(0, 0), (230, 0), (230, 100), (0, 100)])]
    slot_xs = [18, 58, 98, 138, 178]
    for x in slot_xs:
        cut_polys.append(base.rounded_slot_poly(x, 18, 14, 6))
        cut_polys.append(base.rounded_slot_poly(x, 76, 14, 6))
    cut_rects: list[base.Rect] = []
    cut_circles = [
        base.Circle(15, 10, 2.25),
        base.Circle(100, 10, 2.25),
        base.Circle(185, 10, 2.25),
        base.Circle(15, 90, 2.25),
        base.Circle(100, 90, 2.25),
        base.Circle(185, 90, 2.25),
    ]
    notes = [
        "Holder subplate: 5.0 mm HDPE, ABS, G10, or phenolic. This is the sacrificial non-conductive board for the five linked holders.",
        "A provisional 5-position slot field is included: two adjustable slots per holder location, sized for site-fit before the exact ear pitch is confirmed.",
        "Replace the provisional slot field with the measured final ear-hole pattern in Rev B once the linked-holder assembly is measured.",
        "Using an insulating board avoids mounting the modular holders directly to aluminium and makes later drilling/replacement easier.",
    ]
    return base.Drawing("midi5_holder_subplate_rev_a", 230, 100, cut_polys, cut_rects, cut_circles, [], notes)


def midi5_module_rear_insulator() -> base.Drawing:
    cut_polys = [base.Poly([(0, 0), (220, 0), (220, 100), (0, 100)])]
    cut_rects: list[base.Rect] = []
    cut_circles = [
        # Rear-panel fixing holes.
        base.Circle(20, 5, 2.25),
        base.Circle(110, 5, 2.25),
        base.Circle(200, 5, 2.25),
        base.Circle(20, 95, 2.25),
        base.Circle(110, 95, 2.25),
        base.Circle(200, 95, 2.25),
        # Cable exits. These are grommet pilot holes and can be enlarged to suit actual loom sizes.
        base.Circle(28, 68, 12.5),   # single main feed entry
        base.Circle(55, 25, 8.0),
        base.Circle(90, 25, 8.0),
        base.Circle(125, 25, 8.0),
        base.Circle(160, 25, 8.0),
        base.Circle(195, 25, 8.0),
    ]
    notes = [
        "Rear insulator panel: 3.0 mm ABS, HDPE, or polypropylene. Do not make this part from bare metal.",
        "One larger grommet hole is for the single bus-bar feed into the linked MIDI bank.",
        "Five smaller grommet holes are for the separated fused branch outputs leaving the module.",
        "Grommet-hole diameters are provisional in Rev A and can be opened up to match the final cable and grommet sizes.",
    ]
    return base.Drawing("midi5_module_rear_insulator_rev_a", 220, 100, cut_polys, cut_rects, cut_circles, [], notes)


def write_readme() -> None:
    text = """# J40 5-Way MIDI Module Fabrication Pack - Rev A

This pack is a dedicated module for the `5 linked MIDI fuse holders` only.

It intentionally excludes the breaker/cutoff, which can be mounted elsewhere later.

## Parts in this pack

1. `midi5_module_box_rev_a`
2. `midi5_holder_subplate_rev_a`
3. `midi5_module_rear_insulator_rev_a`

## Design intent

- The aluminium box is the structural shell mounted in the engine bay.
- The holder subplate is the non-conductive board that the five interlocked fuse holders mount to.
- The rear insulator panel closes the back of the box and carries the cable exits.

## Cable plan

- `1` main feed into the linked bus bar
- `5` separated fused outputs leaving the module
- all cable exits are intended to use rubber grommets

## Why the holder board uses provisional slots in Rev A

The linked MIDI holders are modular and each holder has its own mounting ears.
Rev A therefore uses a provisional 5-position adjustable slot field in the plastic subplate.
That gives the fabricator a usable part now, while still leaving room to tighten the pattern in Rev B
once the real linked-holder pitch and ear-hole positions are measured.

## Materials

- Module box: `3.0 mm 5052-H32 aluminium`
- Holder subplate: `5.0 mm HDPE, ABS, G10, or phenolic`
- Rear insulator: `3.0 mm ABS, HDPE, or polypropylene`

## Send to fabricator

Send the `DXF` files for cutting and the PDF sheet for review.
"""
    (OUT_DIR / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    drawings = [
        midi5_module_box(),
        midi5_holder_subplate(),
        midi5_module_rear_insulator(),
    ]
    for drawing in drawings:
        base.write_svg(drawing)
        base.write_dxf(drawing)
    base.write_pdf(drawings)
    write_readme()


if __name__ == "__main__":
    main()
