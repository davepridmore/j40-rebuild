from __future__ import annotations

from pathlib import Path

import generate_electrical_module_drawings as base


OUT_DIR = Path("/Users/davidpridmore/IdeaProjects/J40/data/manual/fabrication/midi5_module_rev_b")
base.OUT_DIR = OUT_DIR
base.PDF_NAME = "j40_midi5_module_rev_b_dimension_sheet.pdf"


def midi5_module_box() -> base.Drawing:
    # Compact shell around the measured five-holder pack.
    cut_polys = [
        base.Poly(
            [
                (20, 0),
                (200, 0),
                (200, 20),
                (220, 20),
                (220, 140),
                (200, 140),
                (200, 160),
                (20, 160),
                (20, 140),
                (0, 140),
                (0, 20),
                (20, 20),
            ]
        ),
        base.rounded_slot_poly(54, 6, 16, 8),
        base.rounded_slot_poly(150, 6, 16, 8),
        base.rounded_slot_poly(54, 146, 16, 8),
        base.rounded_slot_poly(150, 146, 16, 8),
        base.rounded_slot_poly(6, 72, 8, 16),
        base.rounded_slot_poly(206, 72, 8, 16),
    ]
    cut_rects: list[base.Rect] = []
    cut_circles = [
        # Subplate stand-off holes.
        base.Circle(35, 30, 2.25),
        base.Circle(90, 30, 2.25),
        base.Circle(145, 30, 2.25),
        base.Circle(35, 110, 2.25),
        base.Circle(90, 110, 2.25),
        base.Circle(145, 110, 2.25),
        # Rear-insulator attachment holes.
        base.Circle(30, 10, 2.25),
        base.Circle(110, 10, 2.25),
        base.Circle(190, 10, 2.25),
        base.Circle(30, 150, 2.25),
        base.Circle(110, 150, 2.25),
        base.Circle(190, 150, 2.25),
    ]
    bend_lines = [
        base.Line(20, 20, 200, 20),
        base.Line(20, 140, 200, 140),
        base.Line(20, 20, 20, 140),
        base.Line(200, 20, 200, 140),
    ]
    notes = [
        "5-way MIDI-only module box: 3.0 mm 5052-H32 aluminium. Finished face 180 x 120. Flanges 20 mm back.",
        "This Rev B shell is tightened around the measured five-holder pack; breaker/cutoff remains a separate part elsewhere.",
        "Six face holes mount the non-conductive holder subplate on stand-offs.",
        "Vehicle-side pickup slots remain slotted for site-fit to the repaired inner-wing / tray structure.",
    ]
    return base.Drawing("midi5_module_box_rev_b", 220, 160, cut_polys, cut_rects, cut_circles, bend_lines, notes)


def midi5_holder_subplate() -> base.Drawing:
    cut_polys = [base.Poly([(0, 0), (140, 0), (140, 85), (0, 85)])]
    cut_rects: list[base.Rect] = []
    # Photo-derived five-holder pitch: about 20 mm between positions over ~100 mm total body length.
    # The two ear rows are staggered by about half a pitch rather than directly opposite.
    left_row_xs = [11.0, 31.2, 51.4, 71.6, 91.8]
    right_row_xs = [21.0, 41.2, 61.4, 81.6, 101.8]
    cut_circles = []
    for x in left_row_xs:
        cut_circles.append(base.Circle(x, 20, 2.25))
    for x in right_row_xs:
        cut_circles.append(base.Circle(x, 64, 2.25))
    cut_circles.extend([
        # Board-to-box fixing holes.
        base.Circle(15, 10, 2.25),
        base.Circle(70, 10, 2.25),
        base.Circle(125, 10, 2.25),
        base.Circle(15, 75, 2.25),
        base.Circle(70, 75, 2.25),
        base.Circle(125, 75, 2.25),
    ])
    notes = [
        "Holder subplate: 5.0 mm HDPE, ABS, G10, or phenolic. This board carries the five linked MIDI holders.",
        "Ten holder fixing holes are based on the tape-photo measurements: five positions on about 20 mm pitch, with about 44 mm ear-row separation.",
        "The left and right ear rows are staggered by about 10 mm, matching the offset visible in the linked-holder photos.",
        "The fuse-holder ears are already slotted, so the board can use round 4.5 mm fixing holes.",
        "If your measured final pitch differs by more than 1 mm, update this board only; the metal shell can stay unchanged.",
    ]
    return base.Drawing("midi5_holder_subplate_rev_b", 140, 85, cut_polys, cut_rects, cut_circles, [], notes)


def midi5_module_rear_insulator() -> base.Drawing:
    cut_polys = [base.Poly([(0, 0), (170, 0), (170, 90), (0, 90)])]
    cut_rects: list[base.Rect] = []
    cut_circles = [
        base.Circle(15, 8, 2.25),
        base.Circle(85, 8, 2.25),
        base.Circle(155, 8, 2.25),
        base.Circle(15, 82, 2.25),
        base.Circle(85, 82, 2.25),
        base.Circle(155, 82, 2.25),
        # One main bus-bar feed and five separated branch outputs.
        base.Circle(142, 56, 10.0),  # 20 mm dia feed hole
        base.Circle(21.0, 26, 6.0),
        base.Circle(41.2, 26, 6.0),
        base.Circle(61.4, 26, 6.0),
        base.Circle(81.6, 26, 6.0),
        base.Circle(101.8, 26, 6.0),
    ]
    notes = [
        "Rear insulator panel: 3.0 mm ABS, HDPE, or polypropylene. Do not make this part from bare metal.",
        "Five 12 mm grommet pilot holes align with the five fused branch positions behind the linked holder row.",
        "One 20 mm grommet pilot hole is reserved for the single bus-bar feed into the linked MIDI bank.",
        "Hole diameters can still be opened up if your final cable and grommet combination needs more room.",
    ]
    return base.Drawing("midi5_module_rear_insulator_rev_b", 170, 90, cut_polys, cut_rects, cut_circles, [], notes)


def write_readme() -> None:
    text = """# J40 5-Way MIDI Module Fabrication Pack - Rev B

This pack finalizes the `5 linked MIDI fuse holder` module using the tape-photo measurements provided in-thread.

It still excludes the breaker/cutoff, which remains a separate bracket/module.

## Parts in this pack

1. `midi5_module_box_rev_b`
2. `midi5_holder_subplate_rev_b`
3. `midi5_module_rear_insulator_rev_b`

## What changed from Rev A

- The holder subplate is no longer generic.
- The five holder positions now use a photo-derived real pitch and real ear-row spacing.
- The module shell is reduced to match the actual five-holder pack instead of a generic oversized envelope.
- The rear insulator now aligns its five branch exits with the measured holder row.

## Dimension basis

- Linked 5-holder body length from tape photos: about `100 mm`
- Holder position pitch used in Rev B: about `20.2 mm`
- Ear-row separation used in Rev B: about `44 mm`
- Ear-row stagger used in Rev B: about `10 mm`
- Relay box housing confirmation remains `300 x 197 x 80 mm` from the DAIER listing and earlier photo check

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
