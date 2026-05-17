from __future__ import annotations

from pathlib import Path

import fabrication_drawing_base as base


OUT_DIR = Path("/Users/davidpridmore/IdeaProjects/J40/data/manual/fabrication/midi5_enclosure_rev_d")
base.OUT_DIR = OUT_DIR
base.PDF_NAME = "j40_midi5_enclosure_rev_d_dimension_sheet.pdf"

FLOOR_W = 210
FLOOR_D = 165
WALL = 65
FLOOR_X = WALL
FLOOR_Y = WALL


def midi5_enclosure_body() -> base.Drawing:
    cut_polys = [
        base.Poly(
            [
                (WALL, 0),
                (WALL + FLOOR_W, 0),
                (WALL + FLOOR_W, WALL),
                (WALL + FLOOR_W + WALL, WALL),
                (WALL + FLOOR_W + WALL, WALL + FLOOR_D),
                (WALL + FLOOR_W, WALL + FLOOR_D),
                (WALL + FLOOR_W, WALL + FLOOR_D + WALL),
                (WALL, WALL + FLOOR_D + WALL),
                (WALL, WALL + FLOOR_D),
                (0, WALL + FLOOR_D),
                (0, WALL),
                (WALL, WALL),
            ]
        )
    ]
    cut_rects: list[base.Rect] = []

    # Floor slots are deliberately generous because the final battery-carrier shelf is still a mock-up hold.
    cut_polys.extend(
        [
            base.rounded_slot_poly(FLOOR_X + 18, FLOOR_Y + 18, 28, 10),
            base.rounded_slot_poly(FLOOR_X + FLOOR_W - 46, FLOOR_Y + 18, 28, 10),
            base.rounded_slot_poly(FLOOR_X + 18, FLOOR_Y + FLOOR_D - 28, 28, 10),
            base.rounded_slot_poly(FLOOR_X + FLOOR_W - 46, FLOOR_Y + FLOOR_D - 28, 28, 10),
        ]
    )

    subplate_x = FLOOR_X + (FLOOR_W - 140) / 2
    subplate_y = FLOOR_Y + (FLOOR_D - 85) / 2
    cut_circles = [
        # Insulating holder subplate standoff holes.
        base.Circle(subplate_x + 15, subplate_y + 10, 2.75),
        base.Circle(subplate_x + 70, subplate_y + 10, 2.75),
        base.Circle(subplate_x + 125, subplate_y + 10, 2.75),
        base.Circle(subplate_x + 15, subplate_y + 75, 2.75),
        base.Circle(subplate_x + 70, subplate_y + 75, 2.75),
        base.Circle(subplate_x + 125, subplate_y + 75, 2.75),
        # Input/bus side hinge holes.
        base.Circle(FLOOR_X + 45, 12, 2.25),
        base.Circle(FLOOR_X + 105, 12, 2.25),
        base.Circle(FLOOR_X + 165, 12, 2.25),
        # Output side latch holes.
        base.Circle(FLOOR_X + 72, WALL + FLOOR_D + 53, 2.25),
        base.Circle(FLOOR_X + 138, WALL + FLOOR_D + 53, 2.25),
        # Single cutoff-switched input aligned to the second-from-last MIDI holder / fuse 4 bus bar.
        base.Circle(FLOOR_X + 132, WALL / 2, 10.0),
    ]

    output_xs = [FLOOR_X + x for x in (51, 78, 105, 132, 159)]
    for index, x in enumerate(output_xs):
        cut_circles.append(base.Circle(x, WALL + FLOOR_D + WALL / 2, 14.0 if index == 4 else 8.0))

    bend_lines = [
        base.Line(FLOOR_X, FLOOR_Y, FLOOR_X + FLOOR_W, FLOOR_Y),
        base.Line(FLOOR_X, FLOOR_Y + FLOOR_D, FLOOR_X + FLOOR_W, FLOOR_Y + FLOOR_D),
        base.Line(FLOOR_X, FLOOR_Y, FLOOR_X, FLOOR_Y + FLOOR_D),
        base.Line(FLOOR_X + FLOOR_W, FLOOR_Y, FLOOR_X + FLOOR_W, FLOOR_Y + FLOOR_D),
    ]
    notes = [
        "MIDI Rev D enclosure body: 3.0 mm 5052-H32 aluminium. Finished floor 210 x 165 with 65 mm folded side walls.",
        "This replaces the open Rev C plate route with a covered aluminium box around the full five-holder MIDI bank.",
        "Output side has five grommet pilot holes: four 16 mm holes plus one far-side 28 mm hole for the output that carries two power cables.",
        "Input/bus side has one 20 mm grommet pilot hole aligned to the second-from-last holder, where the cutoff-switched feed lands on the bus bar.",
        "Open pilot holes only as far as needed for the final cable and rubber grommet OD; deburr both sides and fit edge-safe grommets before wiring.",
        "Hinge holes are on the input/bus side; latch holes are on the output side so the lid can open without disturbing the branch wires.",
    ]
    return base.Drawing("midi5_enclosure_body_rev_d", FLOOR_W + WALL * 2, FLOOR_D + WALL * 2, cut_polys, cut_rects, cut_circles, bend_lines, notes)


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
        "Holder subplate: 5.0 mm HDPE, ABS, G10, or phenolic. This board keeps the MIDI holders insulated from the aluminium enclosure.",
        "Ten holder fixing holes reuse the measured linked-holder pattern from Rev C: about 20.2 mm pitch, 44 mm row separation, and 10 mm row stagger.",
        "The six larger holes mount the subplate to the enclosure floor on 10-12 mm insulated standoffs.",
        "The second-from-last holder is the planned power input/bus-bar feed position; the opposite side carries five fused outputs.",
    ]
    return base.Drawing("midi5_holder_subplate_rev_d", 140, 85, cut_polys, cut_rects, cut_circles, [], notes)


def midi5_enclosure_lid() -> base.Drawing:
    cut_polys = [base.Poly([(0, 0), (230, 0), (230, 185), (0, 185)])]
    cut_rects: list[base.Rect] = []
    cut_circles = [
        # Continuous hinge or small hinge leaf on the input/bus side.
        base.Circle(42, 12, 2.25),
        base.Circle(115, 12, 2.25),
        base.Circle(188, 12, 2.25),
        # Output-side latch / M4 thumb-screw positions.
        base.Circle(80, 173, 2.25),
        base.Circle(150, 173, 2.25),
    ]
    notes = [
        "Hinged lid: 2.0-3.0 mm aluminium. Finished panel 230 x 185 gives about 10 mm overlap around the Rev D box body.",
        "Hinge edge is the input/bus side; latch or thumb-screw edge is the output side.",
        "Use a small continuous hinge or two compact hinges. Keep hinge screws clear of the input cable grommet and bus-bar feed lug.",
        "Add thin closed-cell foam or rubber edge strip if rattle or splash sealing becomes an issue; do not seal so tightly that water cannot drain.",
    ]
    return base.Drawing("midi5_enclosure_lid_rev_d", 230, 185, cut_polys, cut_rects, cut_circles, [], notes)


def write_readme() -> None:
    text = """# J40 5-Way MIDI Hinged Enclosure Pack - Rev D

This pack supersedes the open Rev C MIDI plate as the active MIDI fuse-holder route.

Rev D keeps the proven five-holder insulating subplate pattern, but puts the whole MIDI bank inside a folded aluminium enclosure with a hinged lid and grommeted cable exits.

## Parts In This Pack

1. `midi5_enclosure_body_rev_d` - folded aluminium body with side-wall cable/grommet holes
2. `midi5_holder_subplate_rev_d` - non-conductive holder board inside the enclosure
3. `midi5_enclosure_lid_rev_d` - hinged aluminium cover panel

## Cable Plan

- Output side: `5` grommeted holes for the fused outputs.
- Far-side output: enlarged `28 mm` pilot hole for the output that carries `2` power cables.
- Input/bus side: one `20 mm` grommeted input hole aligned to the second-from-last holder, where the cutoff-switched feed lands on the MIDI bus bar.
- All hole sizes are pilots. Open them to match the actual cable OD and grommet OD before paint or final assembly.

## Materials

- Enclosure body: `3.0 mm 5052-H32 aluminium`
- Lid: `2.0-3.0 mm aluminium`
- Holder subplate: `5.0 mm HDPE, ABS, G10, or phenolic`
- Standoffs: `10-12 mm` insulated or sleeved standoffs

## Fabrication Notes

- Bend all body side walls to `90 degrees`.
- Deburr every cable hole and fit rubber grommets before pulling cables through the box.
- Keep the hinge on the input/bus side and the latch on the output side so the five output wires are not moved during fuse service.
- Add insulating boots or caps over all live studs inside the aluminium enclosure.
- Provide a small drain path at the lowest edge after the final installed orientation is known.
"""
    (OUT_DIR / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    drawings = [
        midi5_enclosure_body(),
        midi5_holder_subplate(),
        midi5_enclosure_lid(),
    ]
    for drawing in drawings:
        base.write_svg(drawing)
        base.write_dxf(drawing)
    base.write_pdf(drawings)
    write_readme()


if __name__ == "__main__":
    main()
