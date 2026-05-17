from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path("/Users/davidpridmore/IdeaProjects/J40")
FAB_DIR = ROOT / "data" / "manual" / "fabrication"


def relay_fuse_box_boxes(
    x: float,
    y: float,
    z: float,
    prefix: str,
    *,
    include_cable_exits: bool = True,
) -> list[dict[str, object]]:
    boxes: list[dict[str, object]] = [
        {
            "name": f"{prefix} rotated housing 197 x 300 x 80",
            "x": x,
            "y": y,
            "z": z,
            "w": 197,
            "h": 300,
            "d": 64,
            "color": "black",
        },
        {
            "name": f"{prefix} plain removable front cover",
            "x": x,
            "y": y,
            "z": z - 38,
            "w": 183,
            "h": 286,
            "d": 8,
            "color": "plastic",
        },
        {
            "name": f"{prefix} shallow raised cover rim",
            "x": x,
            "y": y,
            "z": z - 44,
            "w": 147,
            "h": 250,
            "d": 5,
            "color": "black",
        },
    ]
    if include_cable_exits:
        boxes.extend(
            [
                {
                    "name": f"{prefix} top power input cable boot 54 x 46 x 42 at relay offset X-42 Y+164 Z-52",
                    "x": x - 42,
                    "y": y + 164,
                    "z": z - 52,
                    "w": 54,
                    "h": 46,
                    "d": 42,
                    "color": "cableRed",
                },
                {
                    "name": f"{prefix} top power output cable boot 54 x 46 x 42 at relay offset X+42 Y+164 Z-52",
                    "x": x + 42,
                    "y": y + 164,
                    "z": z - 52,
                    "w": 54,
                    "h": 46,
                    "d": 42,
                    "color": "cableRed",
                },
                {
                    "name": f"{prefix} front-facing control cable cluster 170 x 34 x 24 at relay offset X-18 Y-120 Z-112",
                    "x": x - 18,
                    "y": y - 120,
                    "z": z - 112,
                    "w": 170,
                    "h": 34,
                    "d": 24,
                    "color": "rubber",
                },
                {
                    "name": f"{prefix} top power cable service-loop volume",
                    "x": x,
                    "y": y + 208,
                    "z": z - 52,
                    "w": 128,
                    "h": 42,
                    "d": 42,
                    "color": "rubber",
                },
            ]
        )
    return boxes


def relay_fuse_box_cylinders(x: float, y: float, z: float, prefix: str) -> list[dict[str, object]]:
    return [
        {"name": f"{prefix} upper cover screw", "x": x - 46, "y": y + 112, "z": z - 84, "r": 4, "h": 8, "color": "deepblack"},
        {"name": f"{prefix} lower cover screw", "x": x + 46, "y": y - 112, "z": z - 84, "r": 4, "h": 8, "color": "deepblack"},
        {"name": f"{prefix} carrier corner fixing", "x": x - 84, "y": y + 138, "z": z - 78, "r": 5, "h": 8, "color": "deepblack"},
        {"name": f"{prefix} carrier corner fixing", "x": x + 84, "y": y - 138, "z": z - 78, "r": 5, "h": 8, "color": "deepblack"},
    ]


def relay_bottom_mount_boxes(x: float, y: float, z: float, prefix: str) -> list[dict[str, object]]:
    return [
        {
            "name": f"{prefix} large uncovered bottom face seated on insulating sheet 300 x 197",
            "x": x,
            "y": y + 2,
            "z": z,
            "w": 300,
            "h": 4,
            "d": 197,
            "color": "deepblack",
        },
        {
            "name": f"{prefix} covered plastic enclosure above bottom face 300 x 197 x 80",
            "x": x,
            "y": y + 42,
            "z": z,
            "w": 300,
            "h": 76,
            "d": 197,
            "color": "black",
        },
        {
            "name": f"{prefix} removable cover kept accessible on upper face",
            "x": x,
            "y": y + 82,
            "z": z,
            "w": 286,
            "h": 8,
            "d": 183,
            "color": "plastic",
        },
        {
            "name": f"{prefix} shallow raised cover rim on upper face",
            "x": x,
            "y": y + 89,
            "z": z,
            "w": 250,
            "h": 5,
            "d": 147,
            "color": "black",
        },
    ]


def relay_bottom_mount_cylinders(x: float, y: float, z: float, prefix: str) -> list[dict[str, object]]:
    return [
        {"name": f"{prefix} upper cover screw on accessible cover", "x": x - 70, "y": y + 96, "z": z - 55, "r": 4, "h": 8, "color": "deepblack"},
        {"name": f"{prefix} lower cover screw on accessible cover", "x": x + 70, "y": y + 96, "z": z + 55, "r": 4, "h": 8, "color": "deepblack"},
        {"name": f"{prefix} transferred bottom fixing mark", "x": x - 120, "y": y + 12, "z": z - 72, "r": 4, "h": 8, "color": "deepblack"},
        {"name": f"{prefix} transferred bottom fixing mark", "x": x + 120, "y": y + 12, "z": z + 72, "r": 4, "h": 8, "color": "deepblack"},
    ]


def midi_bank_boxes(x: float, y: float, z: float, prefix: str, count: int = 5) -> list[dict[str, object]]:
    boxes: list[dict[str, object]] = [
        {"name": f"{prefix} 140 x 85 insulated subplate", "x": x, "y": y + 8, "z": z, "w": 140, "h": 12, "d": 85, "color": "deepblack"},
        {"name": f"{prefix} common feed bus single input side", "x": x, "y": y + 62, "z": z - 46, "w": 128, "h": 10, "d": 12, "color": "brass"},
        {"name": f"{prefix} output guide backplate attached between subplate and comb", "x": x, "y": y + 48, "z": z + 51, "w": 170, "h": 22, "d": 16, "color": "aluminium"},
        {"name": f"{prefix} seated output cable comb bolted flush to guide backplate", "x": x, "y": y + 72, "z": z + 60, "w": 154, "h": 18, "d": 20, "color": "aluminium"},
        {"name": f"{prefix} output comb left support tab tied into shelf plate", "x": x - 88, "y": y + 48, "z": z + 60, "w": 12, "h": 42, "d": 20, "color": "aluminium"},
        {"name": f"{prefix} output comb right support tab tied into shelf plate", "x": x + 88, "y": y + 48, "z": z + 60, "w": 12, "h": 42, "d": 20, "color": "aluminium"},
        {"name": f"{prefix} output 3 enlarged double-wire access hole cut through attached comb", "x": x, "y": y + 98, "z": z + 60, "w": 42, "h": 8, "d": 36, "color": "silver"},
    ]
    pitch = 27
    start = x - ((count - 1) * pitch) / 2
    for index in range(count):
        holder_x = start + index * pitch
        boxes.extend(
            [
                {
                    "name": f"{prefix} MIDI holder {index + 1} black linked base",
                    "x": holder_x,
                    "y": y + 22,
                    "z": z,
                    "w": 25,
                    "h": 18,
                    "d": 82,
                    "color": "deepblack",
                },
                {
                    "name": f"{prefix} MIDI holder {index + 1} red hinged cover",
                    "x": holder_x,
                    "y": y + 42,
                    "z": z,
                    "w": 24,
                    "h": 26,
                    "d": 72,
                    "color": "red",
                },
                {
                    "name": f"{prefix} MIDI holder {index + 1} latch recess front",
                    "x": holder_x,
                    "y": y + 57,
                    "z": z - 23,
                    "w": 13,
                    "h": 4,
                    "d": 9,
                    "color": "deepblack",
                },
                {
                    "name": f"{prefix} MIDI holder {index + 1} latch recess rear",
                    "x": holder_x,
                    "y": y + 57,
                    "z": z + 23,
                    "w": 13,
                    "h": 4,
                    "d": 9,
                    "color": "deepblack",
                },
                {
                    "name": f"{prefix} MIDI holder {index + 1} left mounting ear",
                    "x": holder_x - 17,
                    "y": y + 17,
                    "z": z - 42,
                    "w": 12,
                    "h": 8,
                    "d": 18,
                    "color": "deepblack",
                },
                {
                    "name": f"{prefix} MIDI holder {index + 1} right mounting ear",
                    "x": holder_x + 17,
                    "y": y + 17,
                    "z": z + 42,
                    "w": 12,
                    "h": 8,
                    "d": 18,
                    "color": "deepblack",
                },
                {
                    "name": f"{prefix} output {index + 1} grommet saddle seated in attached comb",
                    "x": holder_x,
                    "y": y + 86,
                    "z": z + 60,
                    "w": 28 if index == 2 else 20,
                    "h": 14,
                    "d": 30 if index == 2 else 20,
                    "color": "rubber",
                },
            ]
        )
    return boxes


def midi_enclosed_bank_boxes(x: float, y: float, z: float, prefix: str) -> list[dict[str, object]]:
    boxes: list[dict[str, object]] = [
        {"name": f"{prefix} 140 x 85 insulated subplate", "x": x, "y": y + 8, "z": z, "w": 140, "h": 12, "d": 85, "color": "deepblack"},
        {"name": f"{prefix} common feed bus single input side", "x": x, "y": y + 62, "z": z - 46, "w": 128, "h": 10, "d": 12, "color": "brass"},
    ]
    pitch = 27
    start = x - (4 * pitch) / 2
    for index in range(5):
        holder_x = start + index * pitch
        boxes.extend(
            [
                {"name": f"{prefix} MIDI holder {index + 1} black linked base", "x": holder_x, "y": y + 22, "z": z, "w": 25, "h": 18, "d": 82, "color": "deepblack"},
                {"name": f"{prefix} MIDI holder {index + 1} red hinged cover", "x": holder_x, "y": y + 42, "z": z, "w": 24, "h": 26, "d": 72, "color": "red"},
                {"name": f"{prefix} MIDI holder {index + 1} left mounting ear", "x": holder_x - 17, "y": y + 17, "z": z - 42, "w": 12, "h": 8, "d": 18, "color": "deepblack"},
                {"name": f"{prefix} MIDI holder {index + 1} right mounting ear", "x": holder_x + 17, "y": y + 17, "z": z + 42, "w": 12, "h": 8, "d": 18, "color": "deepblack"},
            ]
        )
    return boxes


def midi_enclosure_boxes(x: float, y: float, z: float, prefix: str) -> list[dict[str, object]]:
    holder_xs = [x - 54, x - 27, x, x + 27, x + 54]
    boxes: list[dict[str, object]] = [
        {"name": f"{prefix} folded aluminium enclosure floor 210 x 165", "x": x, "y": y + 3, "z": z, "w": 210, "h": 6, "d": 165, "color": "aluminium"},
        {"name": f"{prefix} input/bus side wall with fuse 4 feed grommet", "x": x, "y": y + 35, "z": z - 84, "w": 210, "h": 65, "d": 6, "color": "aluminium"},
        {"name": f"{prefix} output side wall with five grommeted branch exits", "x": x, "y": y + 35, "z": z + 84, "w": 210, "h": 65, "d": 6, "color": "aluminium"},
        {"name": f"{prefix} left end wall", "x": x - 108, "y": y + 35, "z": z, "w": 6, "h": 65, "d": 165, "color": "aluminium"},
        {"name": f"{prefix} right end wall", "x": x + 108, "y": y + 35, "z": z, "w": 6, "h": 65, "d": 165, "color": "aluminium"},
        {"name": f"{prefix} hinged lid shown open on input side", "x": x, "y": y + 112, "z": z - 118, "w": 230, "h": 6, "d": 185, "color": "aluminium"},
        {"name": f"{prefix} input-side hinge leaf", "x": x, "y": y + 72, "z": z - 91, "w": 180, "h": 8, "d": 8, "color": "silver"},
        {"name": f"{prefix} output-side latch tab pair", "x": x, "y": y + 72, "z": z + 91, "w": 90, "h": 8, "d": 8, "color": "silver"},
        {"name": f"{prefix} fuse 4 input grommet to common bus bar", "x": x + 27, "y": y + 43, "z": z - 89, "w": 26, "h": 20, "d": 8, "color": "rubber"},
        {"name": f"{prefix} far-side output 5 enlarged two-cable grommet", "x": holder_xs[-1], "y": y + 43, "z": z + 89, "w": 34, "h": 24, "d": 8, "color": "rubber"},
    ]
    for index, holder_x in enumerate(holder_xs[:-1]):
        boxes.append({"name": f"{prefix} output {index + 1} single-cable grommet", "x": holder_x, "y": y + 43, "z": z + 89, "w": 22, "h": 18, "d": 8, "color": "rubber"})
    return boxes


def midi_bank_cylinders(x: float, y: float, z: float, prefix: str, count: int = 5) -> list[dict[str, object]]:
    cylinders: list[dict[str, object]] = []
    pitch = 27
    start = x - ((count - 1) * pitch) / 2
    for index in range(count):
        holder_x = start + index * pitch
        cylinders.extend(
            [
                {"name": f"{prefix} holder {index + 1} feed stud", "x": holder_x, "y": y + 60, "z": z - 30, "r": 4, "h": 10, "color": "brass"},
                {"name": f"{prefix} holder {index + 1} branch stud", "x": holder_x, "y": y + 60, "z": z + 30, "r": 4, "h": 10, "color": "brass"},
            ]
        )
    return cylinders


def breaker_boxes(x: float, y: float, z: float, prefix: str) -> list[dict[str, object]]:
    return [
        {"name": f"{prefix} folded cutoff base face 170 x 110", "x": x, "y": y + 3, "z": z, "w": 170, "h": 6, "d": 110, "color": "aluminium"},
        {"name": f"{prefix} left 20 mm upstand lip", "x": x - 89, "y": y + 17, "z": z, "w": 8, "h": 28, "d": 110, "color": "aluminium"},
        {"name": f"{prefix} right 20 mm upstand lip", "x": x + 89, "y": y + 17, "z": z, "w": 8, "h": 28, "d": 110, "color": "aluminium"},
        {"name": f"{prefix} 100A waterproof resettable breaker body", "x": x, "y": y + 27, "z": z, "w": 82, "h": 34, "d": 56, "color": "black"},
        {"name": f"{prefix} breaker raised faceplate", "x": x, "y": y + 48, "z": z, "w": 72, "h": 7, "d": 44, "color": "plastic"},
        {"name": f"{prefix} red RESET lever", "x": x - 12, "y": y + 56, "z": z + 2, "w": 46, "h": 7, "d": 10, "color": "red"},
        {"name": f"{prefix} small red trip button", "x": x + 28, "y": y + 58, "z": z - 17, "w": 15, "h": 5, "d": 9, "color": "red"},
        {"name": f"{prefix} input ring lug", "x": x - 36, "y": y + 53, "z": z - 31, "w": 26, "h": 4, "d": 18, "color": "silver"},
        {"name": f"{prefix} output ring lug", "x": x + 36, "y": y + 53, "z": z + 31, "w": 26, "h": 4, "d": 18, "color": "silver"},
        {"name": f"{prefix} red cable boot", "x": x - 62, "y": y + 36, "z": z - 42, "w": 36, "h": 18, "d": 20, "color": "cableRed"},
        {"name": f"{prefix} black cable boot", "x": x + 62, "y": y + 36, "z": z + 42, "w": 36, "h": 18, "d": 20, "color": "rubber"},
    ]


def breaker_cylinders(x: float, y: float, z: float, prefix: str) -> list[dict[str, object]]:
    return [
        {"name": f"{prefix} input terminal stud", "x": x - 36, "y": y + 59, "z": z - 31, "r": 5, "h": 12, "color": "brass"},
        {"name": f"{prefix} output terminal stud", "x": x + 36, "y": y + 59, "z": z + 31, "r": 5, "h": 12, "color": "brass"},
        {"name": f"{prefix} left fixing screw", "x": x - 34, "y": y + 50, "z": z + 23, "r": 3, "h": 8, "color": "silver"},
        {"name": f"{prefix} right fixing screw", "x": x + 34, "y": y + 50, "z": z - 23, "r": 3, "h": 8, "color": "silver"},
    ]


SCENES = {
    "suspension_wood_cribbing_rev_a": {
        "title": "Suspension Wood Cribbing Rev A",
        "subtitle": "Eight hardwood cribbing blocks and four wedge chocks for suspension support setup.",
        "camera": [360, 300, 420],
        "target": [0, 20, 0],
        "size": "300 x 150 x 75 mm cribbing blocks; 200 x 100 mm wedge chocks",
        "load_path": "Timber stack spreads load under axle or chassis support zones during setup.",
        "service_intent": "Use as supplemental cribbing/chocks only; not a substitute for rated stands.",
        "boxes": [
            {"name": "Cribbing block", "x": -165, "y": 37, "z": -95, "w": 300, "h": 75, "d": 150, "color": "wood"},
            {"name": "Cribbing block", "x": 165, "y": 37, "z": -95, "w": 300, "h": 75, "d": 150, "color": "wood"},
            {"name": "Cribbing block", "x": -165, "y": 118, "z": 95, "w": 300, "h": 75, "d": 150, "color": "wood"},
            {"name": "Cribbing block", "x": 165, "y": 118, "z": 95, "w": 300, "h": 75, "d": 150, "color": "wood"},
            {"name": "Wedge chock", "x": -250, "y": 30, "z": 120, "w": 200, "h": 60, "d": 100, "color": "wedge"},
            {"name": "Wedge chock", "x": 250, "y": 30, "z": 120, "w": 200, "h": 60, "d": 100, "color": "wedge"},
        ],
    },
    "midi5_plate_mount_rev_c": {
        "title": "MIDI 5-Way Plate Mount Rev C",
        "subtitle": "Open aluminium MIDI holder plate with insulated subplate and photo-derived red covered MIDI holder bank.",
        "camera": [310, 260, 390],
        "target": [0, 22, 0],
        "size": "190 x 150 x 3 mm plate; 140 x 85 x 5 mm insulated holder subplate",
        "load_path": "The plate is the vehicle-side carrier; the non-conductive subplate isolates the MIDI holders.",
        "service_intent": "Leave cable exits and holder screws accessible for fuse and branch-feed service; output guide backplate, comb, and saddles are modelled as attached pieces.",
        "boxes": [
            {"name": "Aluminium mount plate", "x": 0, "y": 3, "z": 0, "w": 190, "h": 6, "d": 150, "color": "aluminium"},
            *midi_bank_boxes(0, 6, 0, "MIDI Rev C active five-way bank", count=5),
        ],
        "cylinders": [
            {"name": "Standoff", "x": -68, "y": 23, "z": -36, "r": 4, "h": 16, "color": "brass"},
            {"name": "Standoff", "x": 68, "y": 23, "z": -36, "r": 4, "h": 16, "color": "brass"},
            {"name": "Standoff", "x": -68, "y": 23, "z": 36, "r": 4, "h": 16, "color": "brass"},
            {"name": "Standoff", "x": 68, "y": 23, "z": 36, "r": 4, "h": 16, "color": "brass"},
            *midi_bank_cylinders(0, 6, 0, "MIDI Rev C active five-way bank", count=5),
        ],
    },

    "midi5_enclosure_rev_d": {
        "title": "MIDI 5-Way Hinged Enclosure Rev D",
        "subtitle": "Folded aluminium box around the full five-holder MIDI bank, with hinged lid and grommeted input/output sides.",
        "camera": [340, 290, 430],
        "target": [0, 45, 0],
        "size": "210 x 165 x 65 mm finished enclosure body; 230 x 185 mm hinged lid; 140 x 85 mm insulated holder subplate",
        "load_path": "The aluminium body is the vehicle-side carrier; the non-conductive subplate isolates the MIDI holders from the enclosure.",
        "service_intent": "Open the hinged lid for fuse service while the output wires remain held by five grommets; the far-side output grommet is enlarged for two power cables and the input grommet lands at fuse 4.",
        "boxes": [
            *midi_enclosure_boxes(0, 6, 0, "MIDI Rev D enclosure"),
            *midi_enclosed_bank_boxes(0, 12, 0, "MIDI Rev D active five-way bank"),
        ],
        "cylinders": [
            {"name": "Front left enclosure floor screw", "x": -82, "y": 16, "z": -62, "r": 3, "h": 8, "color": "silver"},
            {"name": "Front right enclosure floor screw", "x": 82, "y": 16, "z": -62, "r": 3, "h": 8, "color": "silver"},
            {"name": "Rear left enclosure floor screw", "x": -82, "y": 16, "z": 62, "r": 3, "h": 8, "color": "silver"},
            {"name": "Rear right enclosure floor screw", "x": 82, "y": 16, "z": 62, "r": 3, "h": 8, "color": "silver"},
            *midi_bank_cylinders(0, 12, 0, "MIDI Rev D active five-way bank", count=5),
        ],
    },
    "relay_mount_rev_c": {
        "title": "Relay Mount Rev C",
        "subtitle": "Fallback standalone folded relay-box carrier with rear guard and serviceable loom exit.",
        "camera": [430, 360, 520],
        "target": [0, 160, 0],
        "size": "360 x 255 mm carrier blank shown rotated; 320 x 220 mm finished face shown as 220 x 320; 280 x 185 mm rear guard shown as 185 x 280",
        "load_path": "The folded aluminium carrier is a vertical front-face support for the DAIER relay/fuse box if the split relay route is used.",
        "service_intent": "Show the relay box rotated on the carrier face, 20 mm side/bottom returns bent back, the 15 mm top return, the spaced rear guard, top power in/out exits, front control-cable exit, and service-loop clearance.",
        "boxes": [
            {"name": "Folded relay carrier front face 320 x 220 shown rotated to 220 x 320", "x": 0, "y": 160, "z": 0, "w": 220, "h": 320, "d": 8, "color": "aluminium"},
            {"name": "Left 20 mm 90-degree return bent back", "x": -114, "y": 160, "z": -14, "w": 8, "h": 320, "d": 28, "color": "aluminium"},
            {"name": "Right 20 mm 90-degree return bent back", "x": 114, "y": 160, "z": -14, "w": 8, "h": 320, "d": 28, "color": "aluminium"},
            {"name": "Bottom 20 mm 90-degree return bent back", "x": 0, "y": 0, "z": -14, "w": 220, "h": 8, "d": 28, "color": "aluminium"},
            {"name": "Top 15 mm 90-degree return bent back", "x": 0, "y": 324, "z": -11.5, "w": 220, "h": 8, "d": 23, "color": "aluminium"},
            {"name": "Left vertical bend crease", "x": -110, "y": 160, "z": 6, "w": 4, "h": 320, "d": 3, "color": "bendline"},
            {"name": "Right vertical bend crease", "x": 110, "y": 160, "z": 6, "w": 4, "h": 320, "d": 3, "color": "bendline"},
            {"name": "Bottom horizontal bend crease", "x": 0, "y": 4, "z": 6, "w": 220, "h": 4, "d": 3, "color": "bendline"},
            {"name": "Top horizontal bend crease", "x": 0, "y": 320, "z": 6, "w": 220, "h": 4, "d": 3, "color": "bendline"},
            *relay_fuse_box_boxes(0, 160, -42, "Relay/fuse box on carrier front face"),
            {"name": "Rear guard spaced behind loom side", "x": 0, "y": 160, "z": 28, "w": 185, "h": 280, "d": 5, "color": "plastic"},
        ],
        "cylinders": [
            *relay_fuse_box_cylinders(0, 160, -42, "Relay/fuse box on carrier front face"),
        ],
    },
    "relay_mount_rev_d": {
        "title": "Relay Mount Rev D",
        "subtitle": "Simplified relay-box support: flat base and insulating sheet under the relay's uncovered bottom face.",
        "camera": [420, 330, 500],
        "target": [0, 70, 0],
        "size": "360 x 245 x 3 mm aluminium base; 300 x 197 x 3 mm insulating sheet matching the relay bottom footprint",
        "load_path": "The flat aluminium base bolts to the battery-stand ladder through exposed slots; the insulating sheet sits directly under the relay box's large uncovered bottom face.",
        "service_intent": "Keep the covered/removable face accessible above the base, transfer bottom-face relay fixing holes from the actual box after orientation is confirmed, and use the base slots for stand attachment.",
        "boxes": [
            {"name": "Flat aluminium base plate 360 x 245 under relay bottom", "x": 0, "y": 3, "z": 0, "w": 360, "h": 6, "d": 245, "color": "aluminium"},
            {"name": "Exact relay-bottom insulating sheet 300 x 197", "x": 0, "y": 10, "z": 0, "w": 300, "h": 6, "d": 197, "color": "plastic"},
            *relay_bottom_mount_boxes(0, 13, 0, "Covered relay/fuse box on Rev D base"),
            {"name": "Exposed front stand-mount slot pair outside relay bottom", "x": 0, "y": 14, "z": -108, "w": 210, "h": 4, "d": 14, "color": "silver"},
            {"name": "Exposed rear stand-mount slot pair outside relay bottom", "x": 0, "y": 14, "z": 108, "w": 210, "h": 4, "d": 14, "color": "silver"},
        ],
        "cylinders": [
            *relay_bottom_mount_cylinders(0, 13, 0, "Covered relay/fuse box on Rev D base"),
        ],
    },
}


MATERIALS = {
    "aluminium": {"color": "#c1cbd3", "side": "#8d99a4"},
    "steel": {"color": "#717b84", "side": "#535d66"},
    "wood": {"color": "#b9874f", "side": "#8d6135"},
    "wedge": {"color": "#d2a263", "side": "#936739"},
    "black": {"color": "#202a33", "side": "#11181e"},
    "deepblack": {"color": "#111820", "side": "#080c10"},
    "plastic": {"color": "#2d3942", "side": "#1c252b"},
    "relayblock": {"color": "#2b333a", "side": "#151a1f"},
    "red": {"color": "#b7302a", "side": "#7e1e1a"},
    "cableRed": {"color": "#c51f1f", "side": "#8c1515"},
    "fuseblue": {"color": "#2387d7", "side": "#145888"},
    "fuseyellow": {"color": "#dfba21", "side": "#9b7e0e"},
    "fusered": {"color": "#d43a38", "side": "#8f1c1a"},
    "brass": {"color": "#c8a451", "side": "#8c6d2a"},
    "rubber": {"color": "#161a1d", "side": "#080a0c"},
    "silver": {"color": "#d4d8dc", "side": "#9aa3aa"},
    "white": {"color": "#f4f6f8", "side": "#cbd2d8"},
    "bendline": {"color": "#2f3942", "side": "#202830"},
}


def iso_point(x: float, z: float, y: float) -> tuple[float, float]:
    return 420 + (x - z) * 0.72, 100 + (x + z) * 0.32 - y * 1.1


def points_attr(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def polygon(points: list[tuple[float, float, float]], css_class: str) -> str:
    return f'<polygon class="{css_class}" points="{points_attr([iso_point(*point) for point in points])}" />'


def prism(box: dict[str, object], index: int) -> list[str]:
    x = float(box["x"]) - float(box["w"]) / 2
    z = float(box["z"]) - float(box["d"]) / 2
    y = float(box["y"])
    w = float(box["w"])
    d = float(box["d"])
    h = float(box["h"])
    color_key = str(box.get("color", "aluminium"))
    top_class = f"box-top-{index}"
    side_class = f"box-side-{index}"
    front_class = f"box-front-{index}"
    return [
        f".{top_class} {{ fill: {MATERIALS[color_key]['color']}; stroke: #38434c; stroke-width: 1.1; }}",
        f".{side_class}, .{front_class} {{ fill: {MATERIALS[color_key]['side']}; stroke: #38434c; stroke-width: 1; }}",
        polygon([(x + w, z, y), (x + w, z + d, y), (x + w, z + d, y + h), (x + w, z, y + h)], side_class),
        polygon([(x, z + d, y), (x + w, z + d, y), (x + w, z + d, y + h), (x, z + d, y + h)], front_class),
        polygon([(x, z, y + h), (x + w, z, y + h), (x + w, z + d, y + h), (x, z + d, y + h)], top_class),
    ]


def write_svg(package_id: str, scene: dict[str, object]) -> None:
    css: list[str] = []
    elems: list[str] = [
        '<rect class="background" width="920" height="620" />',
        '<ellipse class="shadow" cx="455" cy="430" rx="330" ry="74" />',
    ]
    for index, box in enumerate(scene.get("boxes", [])):
        parts = prism(box, index)
        css.extend(parts[:3])
        elems.extend(parts[3:])
    title = escape(str(scene["title"]))
    subtitle = escape(str(scene["subtitle"]))
    labels = [
        f'<text class="title" x="34" y="46">{title}</text>',
        f'<text class="subtitle" x="34" y="74">{subtitle}</text>',
        '<text class="label" x="34" y="556">Static assembly visual. Open the HTML file for rotate/zoom interaction.</text>',
    ]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="620" viewBox="0 0 920 620" role="img">
  <style>
    .background {{ fill: #f6f7f8; }}
    .shadow {{ fill: #d8dde2; opacity: 0.7; }}
    .title {{ font: 700 26px Arial, sans-serif; fill: #202a33; }}
    .subtitle, .label {{ font: 16px Arial, sans-serif; fill: #4f5d68; }}
    {''.join(css)}
  </style>
  {''.join(labels)}
  {''.join(elems)}
</svg>
"""
    out_dir = FAB_DIR / package_id
    (out_dir / f"{package_id}_3d_visualisation.svg").write_text(svg, encoding="utf-8")


def write_html(package_id: str, scene: dict[str, object]) -> None:
    scene_json = json.dumps(scene, separators=(",", ":"))
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(str(scene["title"]))} - 3D Visualisation</title>
  <link rel="icon" href="data:,">
  <style>
    :root {{ font-family: Arial, Helvetica, sans-serif; background: #f5f6f7; color: #1d252c; }}
    body {{ margin: 0; min-height: 100vh; display: grid; grid-template-rows: auto 1fr; }}
    body.embed {{ grid-template-rows: 1fr; }}
    header {{ padding: 16px 22px 10px; background: #fff; border-bottom: 1px solid #d8dde2; }}
    h1 {{ margin: 0; font-size: clamp(20px, 3vw, 30px); letter-spacing: 0; }}
    .meta {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}
    .chip {{ border: 1px solid #c8d0d8; border-radius: 999px; padding: 5px 9px; background: #f8fafb; font-size: 13px; }}
    main {{ display: grid; grid-template-columns: minmax(0, 1fr) 300px; min-height: 0; }}
    #viewport {{ position: relative; min-height: 560px; overflow: hidden; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
    aside {{ border-left: 1px solid #d8dde2; background: #fff; padding: 18px; }}
    h2 {{ margin: 0 0 12px; font-size: 18px; letter-spacing: 0; }}
    dl {{ margin: 0; display: grid; gap: 12px; }}
    dt {{ font-weight: 700; }}
    dd {{ margin: 3px 0 0; color: #54616c; font-size: 14px; line-height: 1.45; }}
    #fallback {{ position: absolute; inset: 0; display: grid; place-items: center; padding: 20px; background: #f5f6f7; }}
    #fallback img {{ width: min(94vw, 920px); max-height: 82vh; object-fit: contain; }}
    body.is-three-ready #fallback {{ display: none; }}
    body.embed header,
    body.embed aside {{ display: none; }}
    body.embed main {{ grid-template-columns: 1fr; min-height: 100vh; height: 100vh; }}
    body.embed #viewport {{ min-height: 100vh; height: 100vh; }}
    @media (max-width: 820px) {{ main {{ grid-template-columns: 1fr; }} #viewport {{ min-height: 430px; }} aside {{ border-left: 0; border-top: 1px solid #d8dde2; }} }}
  </style>
  <script type="importmap">{{"imports":{{"three":"https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.164.1/examples/jsm/"}}}}</script>
</head>
<body>
  <script>
    if (new URLSearchParams(window.location.search).has("embed")) {{
      document.body.classList.add("embed");
    }}
  </script>
  <header>
    <h1>{escape(str(scene["title"]))}</h1>
    <div class="meta">
      <span class="chip">{escape(str(scene["size"]))}</span>
      <span class="chip">Interactive rotate/zoom</span>
      <span class="chip">Fabrication package visual</span>
    </div>
  </header>
  <main>
    <section id="viewport" aria-label="Interactive 3D fabrication visualisation">
      <div id="fallback"><img src="./{package_id}_3d_visualisation.svg" alt="{escape(str(scene["title"]))} static visualisation"></div>
    </section>
    <aside>
      <h2>Assembly Read</h2>
      <dl>
        <div><dt>Package role</dt><dd>{escape(str(scene["subtitle"]))}</dd></div>
        <div><dt>Load path</dt><dd>{escape(str(scene["load_path"]))}</dd></div>
        <div><dt>Service intent</dt><dd>{escape(str(scene["service_intent"]))}</dd></div>
      </dl>
    </aside>
  </main>
  <script type="module">
    import * as THREE from "three";
    import {{ OrbitControls }} from "three/addons/controls/OrbitControls.js";

    const sceneData = {scene_json};
    const materialDefs = {{
      aluminium: [0xc1cbd3, 0.35, 0.38],
      steel: [0x59636c, 0.45, 0.5],
      wood: [0xb9874f, 0.1, 0.55],
      wedge: [0xd2a263, 0.1, 0.52],
      black: [0x202a33, 0.05, 0.62],
      deepblack: [0x111820, 0.04, 0.7],
      plastic: [0x2d3942, 0.02, 0.7],
      relayblock: [0x2b333a, 0.04, 0.58],
      red: [0xb7302a, 0.03, 0.42],
      cableRed: [0xc51f1f, 0.03, 0.45],
      fuseblue: [0x2387d7, 0.02, 0.28],
      fuseyellow: [0xdfba21, 0.02, 0.3],
      fusered: [0xd43a38, 0.02, 0.3],
      brass: [0xc4a35a, 0.4, 0.36],
      rubber: [0x161a1d, 0.02, 0.65],
      silver: [0xd4d8dc, 0.35, 0.32],
      white: [0xf4f6f8, 0.02, 0.3],
      bendline: [0x2f3942, 0.05, 0.58],
    }};
    const materials = Object.fromEntries(Object.entries(materialDefs).map(([key, value]) => [
      key,
      new THREE.MeshStandardMaterial({{ color: value[0], metalness: value[1], roughness: value[2] }})
    ]));
    const edgeMaterial = new THREE.LineBasicMaterial({{ color: 0x25313a, transparent: true, opacity: 0.48 }});

    const mount = document.getElementById("viewport");
    const threeScene = new THREE.Scene();
    threeScene.background = new THREE.Color(0xf5f6f7);
    const camera = new THREE.PerspectiveCamera(38, 1, 1, 4200);
    const baseCameraPosition = new THREE.Vector3(...sceneData.camera);
    const baseTarget = new THREE.Vector3(...sceneData.target);
    camera.position.copy(baseCameraPosition);
    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: false, preserveDrawingBuffer: true }});
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = true;
    mount.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.copy(baseTarget);
    controls.enableDamping = true;
    controls.minDistance = 260;
    controls.maxDistance = 1200;
    controls.maxPolarAngle = Math.PI * 0.48;

    const root = new THREE.Group();
    threeScene.add(root);

    function box(item) {{
      const mesh = new THREE.Mesh(
        new THREE.BoxGeometry(item.w, item.h, item.d),
        materials[item.color] || materials.aluminium
      );
      mesh.name = item.name;
      mesh.position.set(item.x, item.y, item.z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      root.add(mesh);
      if (item.color !== "bendline") {{
        const edges = new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry), edgeMaterial);
        edges.position.copy(mesh.position);
        edges.rotation.copy(mesh.rotation);
        edges.scale.copy(mesh.scale);
        root.add(edges);
      }}
    }}

    function cylinder(item) {{
      const mesh = new THREE.Mesh(
        new THREE.CylinderGeometry(item.r, item.r, item.h, 36),
        materials[item.color] || materials.aluminium
      );
      mesh.name = item.name;
      mesh.position.set(item.x, item.y, item.z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      root.add(mesh);
      const edges = new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry), edgeMaterial);
      edges.position.copy(mesh.position);
      edges.rotation.copy(mesh.rotation);
      root.add(edges);
    }}

    sceneData.boxes.forEach(box);
    (sceneData.cylinders || []).forEach(cylinder);

    threeScene.add(new THREE.HemisphereLight(0xffffff, 0x98a1aa, 2.2));
    const key = new THREE.DirectionalLight(0xffffff, 2.4);
    key.position.set(260, 420, 300);
    key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    threeScene.add(key);

    const ground = new THREE.Mesh(new THREE.PlaneGeometry(900, 680), new THREE.ShadowMaterial({{ color: 0x000000, opacity: 0.12 }}));
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -62;
    ground.receiveShadow = true;
    threeScene.add(ground);

    function resize() {{
      const width = mount.clientWidth;
      const height = mount.clientHeight;
      renderer.setSize(width, height, false);
      camera.aspect = width / Math.max(1, height);
      const aspect = width / Math.max(1, height);
      const portraitScale = aspect < 0.9 ? Math.min(3.2, 1.35 / Math.max(aspect, 0.38)) : 1;
      const nextPosition = baseTarget.clone().add(
        baseCameraPosition.clone().sub(baseTarget).multiplyScalar(portraitScale)
      );
      camera.position.copy(nextPosition);
      controls.target.copy(baseTarget);
      controls.minDistance = Math.max(220, 260 * portraitScale);
      controls.maxDistance = Math.max(1200, baseTarget.distanceTo(nextPosition) * 1.35);
      camera.updateProjectionMatrix();
      controls.update();
    }}
    function animate() {{
      controls.update();
      renderer.render(threeScene, camera);
      requestAnimationFrame(animate);
    }}
    resize();
    window.addEventListener("resize", resize);
    document.body.classList.add("is-three-ready");
    animate();
  </script>
</body>
</html>
"""
    out_dir = FAB_DIR / package_id
    (out_dir / f"{package_id}_3d_visualisation.html").write_text(html, encoding="utf-8")


def main() -> None:
    for package_id, scene in SCENES.items():
        out_dir = FAB_DIR / package_id
        out_dir.mkdir(parents=True, exist_ok=True)
        write_svg(package_id, scene)
        write_html(package_id, scene)


if __name__ == "__main__":
    main()
