from __future__ import annotations

from pathlib import Path

import generate_electrical_module_drawings as base


OUT_DIR = Path("/Users/davidpridmore/IdeaProjects/J40/data/manual/fabrication/relay_mount_rev_d")
base.OUT_DIR = OUT_DIR
base.PDF_NAME = "j40_relay_mount_rev_d_dimension_sheet.pdf"

RELAY_BOX_W = 300
RELAY_BOX_D = 197
BASE_W = 360
BASE_D = 245


def relay_base_plate() -> base.Drawing:
    cut_polys = [
        base.Poly([(0, 0), (BASE_W, 0), (BASE_W, BASE_D), (0, BASE_D)]),
        # Exposed base-plate slots for mounting the relay assembly to the battery-stand ladder.
        base.rounded_slot_poly(50, 7, 34, 10),
        base.rounded_slot_poly(276, 7, 34, 10),
        base.rounded_slot_poly(50, BASE_D - 17, 34, 10),
        base.rounded_slot_poly(276, BASE_D - 17, 34, 10),
        base.rounded_slot_poly(8, 86, 10, 34),
        base.rounded_slot_poly(BASE_W - 18, 86, 10, 34),
        base.rounded_slot_poly(8, 143, 10, 34),
        base.rounded_slot_poly(BASE_W - 18, 143, 10, 34),
    ]
    notes = [
        "Relay Rev D base plate: flat 3.0 mm 5052-H32 aluminium. No folded box or rear tray is required because the relay unit is already a covered plastic enclosure.",
        "Base plate is 360 x 245 mm, giving exposed mounting margins around the 300 x 197 mm relay-box footprint.",
        "The slotted holes are only for attaching this base plate to the battery stand / access ladder; final slot selection and bolt size are site-fit.",
        "Transfer any relay-box fixing holes from the actual relay box after placing the exact-size insulating sheet. Do not pre-drill relay housing holes from this drawing.",
    ]
    return base.Drawing("relay_base_plate_rev_d", BASE_W, BASE_D, cut_polys, [], [], [], notes)


def relay_insulating_sheet() -> base.Drawing:
    cut_polys = [base.Poly([(0, 0), (RELAY_BOX_W, 0), (RELAY_BOX_W, RELAY_BOX_D), (0, RELAY_BOX_D)])]
    notes = [
        "Relay Rev D insulating sheet: exact 300 x 197 mm relay-box footprint in 3.0 mm ABS, HDPE, polypropylene, G10, or phenolic.",
        "This sheet sits directly between the already-covered relay box and the aluminium base plate.",
        "Use the actual relay box to mark any through-fixing holes after confirming orientation. Keep the sheet full-size under the relay box.",
        "Deburr plastic edges and avoid a fully sealed water trap; the relay box remains the weather cover.",
    ]
    return base.Drawing("relay_insulating_sheet_rev_d", RELAY_BOX_W, RELAY_BOX_D, cut_polys, [], [], [], notes)


def write_readme() -> None:
    text = """# J40 Relay Mount Pack - Rev D

This pack supersedes the folded Rev C relay carrier as the current relay-box fabrication route.

The relay/fuse box is already a well-covered plastic enclosure, so Rev D only provides:

1. `relay_base_plate_rev_d` - flat aluminium base that extends beyond the relay box and bolts to the battery stand
2. `relay_insulating_sheet_rev_d` - exact relay-box-footprint insulating sheet between the box and aluminium base

## Dimensions

- Existing relay-box footprint / insulating sheet: `300 x 197 mm`
- Aluminium base plate: `360 x 245 mm`
- Base material: `3.0 mm 5052-H32 aluminium`
- Insulating sheet: `3.0 mm ABS, HDPE, polypropylene, G10, or phenolic`

## Installation Notes

- Mount the relay box on the exact-size insulating sheet, then mount both to the aluminium base plate.
- Use the exposed base-plate slots to attach the assembly to the battery stand or front access ladder.
- Transfer relay-box fixing holes from the actual relay enclosure after confirming the final orientation.
- Keep the relay box cover removable and keep top power exits / end-side loom exits clear.
- Do not add a folded carrier or rear tray unless the vehicle mock-up proves the flat base cannot be supported.
"""
    (OUT_DIR / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    drawings = [
        relay_base_plate(),
        relay_insulating_sheet(),
    ]
    for drawing in drawings:
        base.write_svg(drawing)
        base.write_dxf(drawing)
    base.write_pdf(drawings)
    write_readme()


if __name__ == "__main__":
    main()
