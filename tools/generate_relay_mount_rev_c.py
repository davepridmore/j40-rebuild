from __future__ import annotations

from pathlib import Path

import fabrication_drawing_base as base


OUT_DIR = Path("/Users/davidpridmore/IdeaProjects/J40/data/manual/fabrication/relay_mount_rev_c")
base.OUT_DIR = OUT_DIR
base.PDF_NAME = "j40_relay_mount_rev_c_dimension_sheet.pdf"


def relay_carrier() -> base.Drawing:
    # Folded carrier: 320 x 220 face, 20 mm side/bottom returns, 15 mm top return.
    cut_polys = [
        base.Poly(
            [
                (20, 0),
                (340, 0),
                (340, 15),
                (360, 15),
                (360, 235),
                (340, 235),
                (340, 255),
                (20, 255),
                (20, 235),
                (0, 235),
                (0, 15),
                (20, 15),
            ]
        ),
        # Vehicle-side site-fit slots.
        base.rounded_slot_poly(72, 3.5, 16, 8),
        base.rounded_slot_poly(272, 3.5, 16, 8),
        base.rounded_slot_poly(72, 243.5, 16, 8),
        base.rounded_slot_poly(272, 243.5, 16, 8),
        base.rounded_slot_poly(6, 118, 8, 16),
        base.rounded_slot_poly(346, 118, 8, 16),
        # Relay-box mounting slots, kept adjustable.
        base.rounded_slot_poly(34, 39.5, 18, 9),
        base.rounded_slot_poly(308, 39.5, 18, 9),
        base.rounded_slot_poly(34, 206.5, 18, 9),
        base.rounded_slot_poly(308, 206.5, 18, 9),
        # Main loom relief slot near lower center.
        base.rounded_slot_poly(100, 193, 140, 26),
    ]
    cut_rects: list[base.Rect] = []
    cut_circles = [
        # Rear guard spacer holes.
        base.Circle(55, 55, 2.75),
        base.Circle(160, 55, 2.75),
        base.Circle(265, 55, 2.75),
        base.Circle(55, 175, 2.75),
        base.Circle(160, 175, 2.75),
        base.Circle(265, 175, 2.75),
    ]
    bend_lines = [
        base.Line(20, 15, 340, 15),
        base.Line(20, 235, 340, 235),
        base.Line(20, 15, 20, 235),
        base.Line(340, 15, 340, 235),
    ]
    notes = [
        "Relay carrier: 3.0 mm 5052-H32 aluminium. Finished face 320 x 220 with 20 mm side/bottom returns and 15 mm top return.",
        "Relay-box mount pattern remains slotted on purpose, even with the published housing size confirmed.",
        "Use 5-10 mm stand-off spacing between the relay box and the rear guard zone so the loom is not crushed against the carrier.",
        "Vehicle-side mount slots remain site-fit to suit the repaired battery/tray structure and inner-wing support.",
    ]
    return base.Drawing("relay_carrier_rev_c", 360, 255, cut_polys, cut_rects, cut_circles, bend_lines, notes)


def relay_rear_guard() -> base.Drawing:
    # Flat plastic splash guard with bottom relief opening for loom drop and drainage.
    cut_polys = [
        base.Poly(
            [
                (0, 0),
                (280, 0),
                (280, 185),
                (200, 185),
                (200, 160),
                (80, 160),
                (80, 185),
                (0, 185),
            ]
        )
    ]
    cut_rects: list[base.Rect] = []
    cut_circles = [
        # These align to the six carrier spacer holes when the guard is centered on the 320 mm carrier face
        # with a 20 mm side inset and a 20 mm top inset.
        base.Circle(15, 20, 2.75),
        base.Circle(120, 20, 2.75),
        base.Circle(225, 20, 2.75),
        base.Circle(15, 140, 2.75),
        base.Circle(120, 140, 2.75),
        base.Circle(225, 140, 2.75),
    ]
    notes = [
        "Rear splash guard: 3.0 mm ABS, HDPE, or polypropylene. This sits behind the relay box on spacers.",
        "Open lower center section gives loom drop room and leaves a drain path; this guard is not meant to fully seal the relay-box rear.",
        "Guard-to-carrier holes match the six spacer locations in the aluminium carrier when the guard is centered on the carrier face.",
        "If you want more side splash coverage later, that should be added as simple clipped side flaps rather than sealing this panel in.",
    ]
    return base.Drawing("relay_rear_guard_rev_c", 280, 185, cut_polys, cut_rects, cut_circles, [], notes)


def write_readme() -> None:
    text = """# J40 Relay Mount Pack - Rev C

This pack is the recommended relay-box support arrangement for the DAIER prewired 10-way relay/fuse box.

## Parts in this pack

1. `relay_carrier_rev_c`
2. `relay_rear_guard_rev_c`

## Design intent

- The aluminium carrier is the structural part.
- The relay box bolts to the front face of the carrier.
- The plastic rear guard sits behind the relay box on spacers to protect the open-back side from splash and abrasion.

## Why this is not the same as the MIDI mount

The MIDI holders are exposed modular parts, so they need a non-conductive mounting board.
The relay box is already a plastic housing, so it should mount directly to aluminium and only use plastic as a rear guard.

## Materials

- Carrier: `3.0 mm 5052-H32 aluminium`
- Rear guard: `3.0 mm ABS, HDPE, or polypropylene`

## Installation notes

- Use `5-10 mm` spacers between the relay box and the rear guard zone.
- Use `10-12 mm` spacers between the rear guard and carrier if needed to clear the loom.
- Keep the bottom loom opening downward for drainage.
- Do not fully seal the back of the relay box.
"""
    (OUT_DIR / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    drawings = [
        relay_carrier(),
        relay_rear_guard(),
    ]
    for drawing in drawings:
        base.write_svg(drawing)
        base.write_dxf(drawing)
    base.write_pdf(drawings)
    write_readme()


if __name__ == "__main__":
    main()
