from __future__ import annotations

from pathlib import Path

import fabrication_drawing_base as base


OUT_DIR = Path("/Users/davidpridmore/IdeaProjects/J40/data/manual/fabrication/midi5_plate_mount_rev_c")
base.OUT_DIR = OUT_DIR
base.PDF_NAME = "j40_midi5_plate_mount_rev_c_dimension_sheet.pdf"


def midi5_mount_plate() -> base.Drawing:
    cut_polys = [base.Poly([(0, 0), (190, 0), (190, 150), (0, 150)])]
    cut_rects: list[base.Rect] = []
    cut_circles = [
        # Vehicle-side mounting slots, generous for site-fit.
        base.Circle(15, 15, 0.0),
        # Subplate stand-off holes.
        base.Circle(32.5, 37.5, 2.75),
        base.Circle(95.0, 37.5, 2.75),
        base.Circle(157.5, 37.5, 2.75),
        base.Circle(32.5, 112.5, 2.75),
        base.Circle(95.0, 112.5, 2.75),
        base.Circle(157.5, 112.5, 2.75),
        # Cable support / P-clip holes.
        base.Circle(18, 30, 3.25),
        base.Circle(18, 70, 3.25),
        base.Circle(18, 110, 3.25),
        base.Circle(172, 35, 3.25),
        base.Circle(172, 115, 3.25),
    ]
    cut_polys.extend(
        [
            base.rounded_slot_poly(10, 10, 18, 8),
            base.rounded_slot_poly(162, 10, 18, 8),
            base.rounded_slot_poly(10, 132, 18, 8),
            base.rounded_slot_poly(162, 132, 18, 8),
        ]
    )
    # Remove placeholder zero-radius circle from bounds.
    cut_circles = [c for c in cut_circles if c.r > 0]
    notes = [
        "Open mount plate: 3.0 mm 5052-H32 aluminium. No rear box. This is intentional so the MIDI cables can leave in-plane without a forced rearward bend.",
        "Use 10-12 mm nylon or aluminium spacers between this plate and the holder subplate.",
        "The small 6.5 mm holes near the cable sides are for optional P-clips or saddle clamps to support heavy cables after they leave the holders.",
        "Corner mount slots remain site-fit because the truck-side support structure is still being repaired and located.",
    ]
    return base.Drawing("midi5_mount_plate_rev_c", 190, 150, cut_polys, cut_rects, cut_circles, [], notes)


def midi5_holder_subplate() -> base.Drawing:
    cut_polys = [base.Poly([(0, 0), (140, 0), (140, 85), (0, 85)])]
    cut_rects: list[base.Rect] = []
    left_row_xs = [11.0, 31.2, 51.4, 71.6, 91.8]
    right_row_xs = [21.0, 41.2, 61.4, 81.6, 101.8]
    cut_circles = []
    for x in left_row_xs:
        cut_circles.append(base.Circle(x, 20, 2.25))
    for x in right_row_xs:
        cut_circles.append(base.Circle(x, 64, 2.25))
    cut_circles.extend(
        [
            base.Circle(15, 10, 2.75),
            base.Circle(70, 10, 2.75),
            base.Circle(125, 10, 2.75),
            base.Circle(15, 75, 2.75),
            base.Circle(70, 75, 2.75),
            base.Circle(125, 75, 2.75),
        ]
    )
    notes = [
        "Holder subplate: 5.0 mm HDPE, ABS, G10, or phenolic. This board carries the five linked MIDI holders.",
        "Ten holder fixing holes are photo-derived from your measured linked-holder pack: about 20.2 mm pitch, about 44 mm row separation, about 10 mm row stagger.",
        "The six larger holes are for the standoffs that mount this board to the aluminium plate.",
        "Because the holder ears are already slotted, these can stay as round holes on the board.",
    ]
    return base.Drawing("midi5_holder_subplate_rev_c", 140, 85, cut_polys, cut_rects, cut_circles, [], notes)


def write_readme() -> None:
    text = """# J40 5-Way MIDI Plate Mount Pack - Rev C

This pack replaces the earlier boxed MIDI concept with an open plate-mount arrangement.

## Why Rev C exists

The earlier rear-panel concept implied the MIDI cables would have to leave rearward through a panel.
From your holder photos, that is not the natural cable path. These holders want the branch cables to leave
in-plane from the side, and the common bus feed to leave from its own side/end connection.

Rev C therefore uses:

1. `midi5_mount_plate_rev_c` - structural aluminium mount plate
2. `midi5_holder_subplate_rev_c` - non-conductive holder board

## Advantages

- No forced `90 degree` rearward cable exit
- Better space for heavy cable bend radius
- Easier service access to the fuse covers
- Simpler fabrication than a boxed enclosure
- Cable support can be added with P-clips after final routing is known

## Materials

- Mount plate: `3.0 mm 5052-H32 aluminium`
- Holder subplate: `5.0 mm HDPE, ABS, G10, or phenolic`

## Notes

- Use `10-12 mm` spacers between the holder board and the mount plate.
- Use the small side holes in the aluminium plate for cable P-clips or saddle clamps.
- Keep the common feed on the bus side and the five fused outputs on the branch side.
"""
    (OUT_DIR / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    drawings = [
        midi5_mount_plate(),
        midi5_holder_subplate(),
    ]
    for drawing in drawings:
        base.write_svg(drawing)
        base.write_dxf(drawing)
    base.write_pdf(drawings)
    write_readme()


if __name__ == "__main__":
    main()
