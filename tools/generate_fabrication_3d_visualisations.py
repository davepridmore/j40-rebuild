from __future__ import annotations

import os
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


def rubber_order_boxes(prefix: str = "Longman rubber") -> list[dict[str, object]]:
    boxes: list[dict[str, object]] = [
        {
            "name": f"{prefix} BM-ISO-80 single 80 x 80 x 24 body pad order item",
            "x": -115,
            "y": 12,
            "z": -210,
            "w": 80,
            "h": 24,
            "d": 80,
            "color": "rubber",
            "shape": "rounded_rect",
            "corner_r": 1.5,
            "holes": [{"x": 0, "z": 0, "r": 9}],
            "label": "80 BODY PAD x30",
            "label_dx": -58,
            "label_dy": -18,
        },
        {
            "name": f"{prefix} BM-ISO-80 representative second stacked pad from same order",
            "x": -15,
            "y": 36,
            "z": -210,
            "w": 80,
            "h": 24,
            "d": 80,
            "color": "rubber",
            "shape": "rounded_rect",
            "corner_r": 1.5,
            "holes": [{"x": 0, "z": 0, "r": 9}],
            "label": "STACK 2 WHERE NEEDED",
            "label_dx": -78,
            "label_dy": -18,
        },
        {
            "name": f"{prefix} BM-ISO-80 representative lower stacked pad from same order",
            "x": -15,
            "y": 12,
            "z": -210,
            "w": 80,
            "h": 24,
            "d": 80,
            "color": "rubber",
            "shape": "rounded_rect",
            "corner_r": 1.5,
            "holes": [{"x": 0, "z": 0, "r": 9}],
        },
    ]
    for index, oval_x in enumerate([35, 145]):
        boxes.append(
            {
                "name": f"{prefix} FS-OVAL purchase pad {index + 1} of 2",
                "x": oval_x,
                "y": 7.5,
                "z": -140,
                "w": 96,
                "h": 15,
                "d": 64,
                "color": "rubber",
                "shape": "capsule",
                "holes": [{"x": -32, "z": 0, "r": 6}, {"x": 32, "z": 0, "r": 6}],
                "label": "FS-OVAL x2" if index == 1 else "",
                "label_dx": 44,
                "label_dy": -10,
            }
        )
    boxes.extend(
        [
            {"name": f"{prefix} FS-STRIP-STOCK 38 x 8 strip stock order length", "x": 0, "y": 4, "z": 26, "w": 420, "h": 8, "d": 38, "color": "rubber", "label": "38x8 STRIP STOCK 2m", "label_dx": -172, "label_dy": -12},
        ]
    )
    boxes.extend(
        [
            {"name": f"{prefix} BUMP-60010-LONG fixture base plate representative of 3", "x": -150, "y": 0, "z": 165, "w": 128, "h": 6, "d": 58, "color": "rust", "shape": "capsule", "holes": [{"x": -50, "z": 0, "r": 7}, {"x": 50, "z": 0, "r": 7}]},
            {"name": f"{prefix} BUMP-60010-LONG tapered rubber body representative of 3", "x": -150, "y": 6, "z": 165, "w": 92, "h": 70, "d": 52, "top_w": 70, "top_d": 38, "color": "rubber", "shape": "tapered_bump_stop", "corner_r": 10, "top_corner_r": 8, "label": "BUMP LONG x3", "label_dx": -54, "label_dy": -8},
            {"name": f"{prefix} BUMP-60010-LONG flat worn strike face representative of 3", "x": -150, "y": 76, "z": 165, "w": 70, "h": 2, "d": 38, "color": "rubberWorn", "shape": "rounded_rect", "corner_r": 8},
            {"name": f"{prefix} BUMP-60020-SHORT fixture base plate 1 of 1", "x": 148, "y": 0, "z": 165, "w": 128, "h": 6, "d": 58, "color": "rust", "shape": "capsule", "holes": [{"x": -50, "z": 0, "r": 7}, {"x": 50, "z": 0, "r": 7}]},
            {"name": f"{prefix} BUMP-60020-SHORT tapered rubber body 1 of 1", "x": 148, "y": 6, "z": 165, "w": 90, "h": 60, "d": 50, "top_w": 68, "top_d": 36, "color": "rubber", "shape": "tapered_bump_stop", "corner_r": 10, "top_corner_r": 8, "label": "BUMP SHORT x1", "label_dx": 44, "label_dy": -8},
            {"name": f"{prefix} BUMP-60020-SHORT flat worn strike face", "x": 148, "y": 66, "z": 165, "w": 68, "h": 2, "d": 36, "color": "rubberWorn", "shape": "rounded_rect", "corner_r": 8},
        ]
    )
    return boxes


def rubber_order_cylinders(prefix: str = "Longman rubber") -> list[dict[str, object]]:
    return []


def photo(label: str, src: str, caption: str) -> dict[str, str]:
    return {"label": label, "src": src, "caption": caption}


def rubber_body_mount_images() -> list[dict[str, str]]:
    return [
        photo("RRB-004", "photos/20260502_004231_gp_CfosvPIg.jpg", "Body-mount/cup stack tape-scale context for the active 80 mm square rubber family; not bump-stop evidence."),
        photo("RRB-007", "photos/20260502_004337_gp_m2OagYpg.jpg", "Old body cushion edge and thickness context for the 80 mm square first article."),
        photo("RRB-010", "photos/20260502_004413_gp_Qno8OVRg.jpg", "Old body cushion/cup top context; square 80 mm pad remains the active design."),
        photo("RRB-011", "photos/20260502_004419_gp_ZPXJRBzg.jpg", "Second body cushion/cup top context; kept separate from bump-stop evidence."),
        photo("RRB-012", "photos/20260502_004429_gp_KJHxGcCA.jpg", "Body cushion side/lip/free-height context for sleeve and cup stack checks."),
        photo("RRB-013", "photos/20260502_004437_gp_f1TySzww.jpg", "Cleaner body cushion/cup top reference for 80 mm square pad context."),
        photo("RRB-014", "photos/20260502_004442_gp_7WcFHjLQ.jpg", "Alternate clean body cushion/cup top reference for 80 mm square pad context."),
        photo("May 28 body cup A", "photos/20260528_193054_gp_UFyTb44w.jpg", "Loose body-mount rubber/cup stack measurement context for the 80 mm rubber family."),
        photo("May 28 body cup B", "photos/20260528_193143_gp_Cn3OWzZQ.jpg", "Loose body-mount rubber/cup stack alternate view; not bump-stop evidence."),
        photo("May 28 body cup C", "photos/20260528_193228_gp_PLATNsFQ.jpg", "Loose body-mount cup/washer/round-pad context for 80 mm pad stack release."),
    ]


def rubber_oval_images() -> list[dict[str, str]]:
    return [
        photo("RRB-004", "photos/20260502_004231_gp_CfosvPIg.jpg", "Shared tape-scale image for old body cushions/cups and oval pad."),
        photo("RRB-008", "photos/20260502_004345_gp_yK8VYzMQ.jpg", "Best top-face view of the two-hole oval front-support pad."),
    ]


def rubber_strip_images() -> list[dict[str, str]]:
    return [
        photo("RRB-001", "photos/20260502_004201_gp_zfUSmKJg.jpg", "Long strip/bracket rubber overview with vertical tape."),
        photo("RRB-002", "photos/20260502_004215_gp_evgCLjSw.jpg", "Long strip/bracket rubber length reference."),
        photo("RRB-003", "photos/20260502_004222_gp_PKRe5HSQ.jpg", "Long strip/bracket profile reference."),
        photo("RRB-005", "photos/20260502_004254_gp_Hm9RR5DQ.jpg", "Long strip/bracket height reference."),
        photo("RRB-006", "photos/20260502_004314_gp_wuzpgNrA.jpg", "Strip/bracket side thickness reference."),
        photo("RRB-009", "photos/20260502_004401_gp_otUSjgGA.jpg", "Strip/bracket close side profile."),
        photo("May 17 strip length", "photos/20260517_193503_gp_N9nHjqXw.jpg", "Full-length tape view; released strip length rounds to 420 mm."),
        photo("May 17 strip end", "photos/20260517_193539_gp_E0cR9I0A.jpg", "End and width reference for strip/channel."),
        photo("May 17 strip width", "photos/20260517_193559_gp_NEpk1hpg.jpg", "Close strip width/edge profile view."),
        photo("May 17 curved end", "photos/20260517_193612_gp_JmbfR0Tw.jpg", "Curved/end section measurement reference."),
        photo("May 17 curved close", "photos/20260517_193616_gp_1ye19BZA.jpg", "Companion curved/end close-up."),
        photo("May 17 installed A", "photos/20260517_194143_gp_CO7MuMdA.jpg", "Installed-location proof for flat strip landing."),
        photo("May 17 installed B", "photos/20260517_194633_gp_rAjY3gjg.jpg", "Second installed-location proof for flat strip landing."),
        photo("May 17 installed C", "photos/20260517_194706_gp_twKRWGFA.jpg", "Third installed-location proof for flat strip landing."),
        photo("May 28 retainer A", "photos/20260528_185826_gp_FoyeBPUg.jpg", "Strip/retainer landing context only."),
        photo("May 28 retainer B", "photos/20260528_185833_gp_gZBjUjPg.jpg", "Strip/retainer landing companion view."),
        photo("May 28 section A", "photos/20260528_193200_gp_HICSdovA.jpg", "Loose rectangular strip/block section context."),
        photo("May 28 section B", "photos/20260528_193253_gp_f0eQuSFA.jpg", "Loose rectangular strip/block section companion view."),
    ]


def bump_stop_images() -> list[dict[str, str]]:
    return [
        photo("May 31 front width A", "photos/20260531_171824_gp_HmSS2ChQ.jpg", "Exact front bump-stop face/width measurement with tape; active mould reference."),
        photo("May 31 front width B", "photos/20260531_171833_gp_Vw96I7Mg.jpg", "Companion exact front bump-stop face/width measurement."),
        photo("May 31 front base A", "photos/20260531_171859_gp_i6bRyQKA.jpg", "Exact front bump-stop metal/fixture base length and end bolt-hole measurement."),
        photo("May 31 front base B", "photos/20260531_171903_gp_jNI1gfYA.jpg", "Companion exact front bump-stop base plate and rubber-body taper measurement."),
        photo("May 31 front height", "photos/20260531_171935_gp_BYfhqiWg.jpg", "Exact front bump-stop side height/profile measurement; rear/back uses same body shape stretched longer."),
        photo("May 29 fixture face", "photos/20260529_223605_gp_CklgF0cQ.jpg", "Supporting removed-sample face/plan view; confirms the end-hole fixture/base relationship."),
        photo("May 29 fixture side", "photos/20260529_223701_gp_wYPExcAA.jpg", "Supporting side view for the central fixture/channel interface; May 31 front photos control the active shape."),
    ]


def rubber_order_sections() -> list[dict[str, object]]:
    body_images = rubber_body_mount_images()
    strip_images = rubber_strip_images()
    bump_images = bump_stop_images()
    return [
        {
            "id": "BM-ISO-80",
            "title": "Single 80 mm square body rubber",
            "quantity": "30 pieces",
            "spec": "80 L x 80 W x 24 H mm, 18.0 mm centre bore, R1.5 plan corners, 1.0 mm max edge break/chamfer. Smaller 22 mm body-rubber line is removed from the active order. Quote 30 of the same simple 80 mm pad so any station that proves low can use two stacked pads, with spare flat square pads left for trim and test fitting.",
            "design_matches": ["BM-ISO-80"],
            "model_file": "data/manual/fabrication/rubber_recreation_rev_a/models_3d/bm_iso_lg_square_pad.scad",
            "images": body_images,
        },
        {
            "id": "FS-OVAL",
            "title": "Two-hole front-support isolator pad",
            "quantity": "2",
            "spec": "96 L x 64 W x 15 T mm capsule, two 12 mm holes at 64 mm centres; relief/insert stays sample-controlled.",
            "design_matches": ["FS-OVAL"],
            "model_file": "data/manual/fabrication/rubber_recreation_rev_a/models_3d/fs_oval_front_support_pad.scad",
            "images": rubber_oval_images(),
        },
        {
            "id": "FS-STRIP-L",
            "title": "Left underfloor body-support strip liner",
            "quantity": "1",
            "spec": "Cut one 420 L x 38 W x 8 T mm plain strip from the same 38 x 8 mm stock order after dry-fit. Ask for 2 m total stock because the installed run may not be perfectly straight and will need trim allowance.",
            "design_matches": ["FS-STRIP-L"],
            "model_file": "data/manual/fabrication/rubber_recreation_rev_a/models_3d/fs_strip_l_plain_strip.scad",
            "images": strip_images,
        },
        {
            "id": "FS-STRIP-R",
            "title": "Right underfloor body-support strip liner",
            "quantity": "1",
            "spec": "Cut one 420 L x 38 W x 8 T mm plain strip from the same 38 x 8 mm stock order after dry-fit unless the side proves a handed/non-straight trim. No rubber holes unless the sample proves them.",
            "design_matches": ["FS-STRIP-R"],
            "model_file": "data/manual/fabrication/rubber_recreation_rev_a/models_3d/fs_strip_r_plain_strip.scad",
            "images": strip_images,
        },
        {
            "id": "BUMP-60010-LONG",
            "title": "Rear/back bump stop - same front shape, longer",
            "quantity": "3",
            "spec": "70 H mm rear/back long-family stop: same May 31 front-stop family, stretched taller. Show a tapered rubber body on the metal/fixture base plate with two end bolt holes, rounded sides, and flat strike face.",
            "design_matches": ["long bump-stop"],
            "model_file": "data/manual/fabrication/rubber_recreation_rev_a/models_3d/b_60010_long_measurement_model.scad",
            "images": bump_images,
        },
        {
            "id": "BUMP-60020-SHORT",
            "title": "Exact front bump stop - short height",
            "quantity": "1",
            "spec": "60 H mm right-front/front stop copied from the exact May 31 photos: tapered rubber body on the metal/fixture base plate with end bolt holes, rounded sides, and flat strike face.",
            "design_matches": ["short right-front"],
            "model_file": "data/manual/fabrication/rubber_recreation_rev_a/models_3d/b_60020_short_measurement_model.scad",
            "images": bump_images,
        },
        {
            "id": "EXH-HGR-90917",
            "title": "Teardrop exhaust hanger hold reference",
            "quantity": "hold",
            "spec": "Hold-only nominal 48 x 86 x 22 mm teardrop; needs intact sample or installed support-point measurements.",
            "design_matches": ["exhaust hanger"],
            "model_file": "data/manual/fabrication/rubber_recreation_rev_a/models_3d/exh_hgr_90917_teardrop_cushion.scad",
            "images": [
                photo(
                    "Hold drawing",
                    "data/manual/fabrication/rubber_recreation_rev_a/exh_hgr_90917_08004_teardrop_rev_a.svg",
                    "No confirmed old local rubber photo yet; SVG is the hold-only reference shape.",
                )
            ],
        },
    ]


def rubber_order_item_images() -> list[dict[str, str]]:
    flattened: list[dict[str, str]] = []
    seen: set[str] = set()
    for section in rubber_order_sections():
        for image in section["images"]:
            source = str(image["src"])
            if source in seen:
                continue
            seen.add(source)
            flattened.append(image)
    return flattened


ORDER_GROUPS = [
    {
        "label": "1",
        "title": "80 mm body pads",
        "summary": "single 80 x 80 body pad x30; stack two where needed",
    },
    {
        "label": "2",
        "title": "Front support rubbers",
        "summary": "FS-OVAL x2 plus 38 x 8 strip stock, 2 m",
    },
    {
        "label": "3",
        "title": "Bump stops",
        "summary": "BUMP-60010-LONG x3 and BUMP-60020-SHORT x1",
    },
]


SCENES = {
    "longman_rubber_order_20260508": {
        "title": "Longman Rubber Order 2026-05-08",
        "subtitle": "Three supplier order groups: simple 80 mm body pads, front-support/body-support rubbers, and bump stops; hold references excluded from ordering.",
        "camera": [430, 290, 470],
        "target": [0, 32, 20],
        "size": "Single 80 x 80 body pad line with 18 mm bore, x30; stack two where needed; FS-OVAL 96 x 64 x 15; 38 x 8 strip stock, 2 m",
        "height_callouts": [
            "Body pads: 80 L x 80 W x 24 H, x30; same pad can stack 2 high",
            "FS-OVAL: 96 L x 64 W x 15 T",
            "FS-STRIP stock: 38 W x 8 T, order 2 m; cut 2 x 420 L",
            "BUMP rear/back: same front shape at 70 H; BUMP front/right: exact front stop at 60 H",
        ],
        "load_path": "Order thing 1 is the single simple 80 x 80 body-pad line, quoted as a generous x30 batch so low stations can use two stacked pads. The smaller 22 mm body pad is removed. Order thing 2 is front-support/body-support rubber. Order thing 3 is bump stops from the May 31 exact front-stop shape, with rear/back stops made longer. Hold-only reference parts are excluded from this purchase view.",
        "service_intent": "Use the visual for package orientation, then use the OpenSCAD files for exact 3D envelope, edge break, hole, and release-state controls. Detailed IDs below are drawing controls inside the 3 order groups.",
        "order_groups": ORDER_GROUPS,
        "item_images": rubber_order_item_images(),
        "rubber_sections": rubber_order_sections(),
        "boxes": rubber_order_boxes("Longman order"),
        "cylinders": rubber_order_cylinders("Longman order"),
    },
    "rubber_recreation_rev_a": {
        "title": "Rubber Recreation Rev A",
        "subtitle": "3D purchase view for the current rubber recreation and Longman supplier controls.",
        "camera": [430, 290, 470],
        "target": [0, 32, 20],
        "size": "OpenSCAD source models in models_3d carry exact envelopes, bores, relief options, and measurement placeholders",
        "height_callouts": [
            "Body pads: 80 L x 80 W x 24 H, x30; same pad can stack 2 high",
            "FS-OVAL: 96 L x 64 W x 15 T",
            "FS-STRIP stock: 38 W x 8 T, order 2 m; cut 2 x 420 L",
            "BUMP rear/back: same front shape at 70 H; BUMP front/right: exact front stop at 60 H",
        ],
        "load_path": "The order is grouped into 3 things: a single 80 x 80 body-pad line quoted as x30 with two-pad stacking allowed where dry-fit proves it, front-support/body-support rubbers, and bump stops. The smaller 22 mm body-rubber line is removed. Hardware, sleeves, cups, and hold-only reference rubbers are separate.",
        "service_intent": "Use this dashboard visual for orientation only; OpenSCAD and CSV controls remain the fabrication source of truth. Detailed part cards stay visible so each order group keeps its exact image and 3D control.",
        "order_groups": ORDER_GROUPS,
        "item_images": rubber_order_item_images(),
        "rubber_sections": rubber_order_sections(),
        "boxes": rubber_order_boxes("Rubber recreation"),
        "cylinders": rubber_order_cylinders("Rubber recreation"),
    },
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
        "load_path": "The flat aluminium base bolts through exposed slots to a removable electrical plate carried by the structural radiator/cooling-stack frame; the insulating sheet sits directly under the relay box's large uncovered bottom face.",
        "service_intent": "Keep the covered/removable face accessible, transfer bottom-face fixing holes from the actual box after orientation is confirmed, and do not attach the plate to radiator core, fins, tanks, necks, seams, or through-core rods.",
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
    "rubberWorn": {"color": "#2b2d2a", "side": "#171915"},
    "rust": {"color": "#6c4935", "side": "#3b2920"},
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


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


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


def box_static_label(box: dict[str, object]) -> str:
    label = str(box.get("label", "")).strip()
    if not label:
        return ""
    px, py = iso_point(float(box["x"]), float(box["z"]), float(box["y"]) + float(box["h"]))
    lx = clamp(px + float(box.get("label_dx", 0)), 44, 850)
    ly = clamp(py + float(box.get("label_dy", -18)), 96, 520)
    return (
        f'<line class="callout" x1="{px:.1f}" y1="{py:.1f}" x2="{lx:.1f}" y2="{ly - 12:.1f}" />'
        f'<text class="part-label" x="{lx:.1f}" y="{ly:.1f}">{escape(label)}</text>'
    )


def height_callout_legend(scene: dict[str, object]) -> str:
    rows = [str(row).strip() for row in scene.get("height_callouts", []) if str(row).strip()]
    if not rows:
        return ""
    x = 610
    y = 102
    width = 276
    height = 34 + len(rows) * 22
    text_rows = [
        f'<text class="legend-title" x="{x + 16}" y="{y + 24}">Height / Thickness</text>'
    ]
    for index, row in enumerate(rows):
        text_rows.append(
            f'<text class="legend-text" x="{x + 16}" y="{y + 50 + index * 22}">{escape(row)}</text>'
        )
    return (
        f'<rect class="legend-box" x="{x}" y="{y}" width="{width}" height="{height}" rx="6" />'
        + "".join(text_rows)
    )


def order_group_rows(scene: dict[str, object]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for raw in scene.get("order_groups", []):
        if not isinstance(raw, dict):
            continue
        label = str(raw.get("label", "")).strip()
        title = str(raw.get("title", "")).strip()
        summary = str(raw.get("summary", "")).strip()
        if title and summary:
            rows.append({"label": label, "title": title, "summary": summary})
    return rows


def order_group_legend(scene: dict[str, object]) -> str:
    rows = order_group_rows(scene)
    if not rows:
        return ""
    x = 610
    y = 282
    width = 276
    height = 24 + len(rows) * 42
    parts = [
        f'<rect class="order-box" x="{x}" y="{y}" width="{width}" height="{height}" rx="6" />',
        f'<text class="order-title" x="{x + 16}" y="{y + 24}">3 Things To Order</text>',
    ]
    for index, row in enumerate(rows):
        row_y = y + 50 + index * 42
        parts.extend(
            [
                f'<circle class="order-dot" cx="{x + 24}" cy="{row_y - 5}" r="10" />',
                f'<text class="order-dot-text" x="{x + 24}" y="{row_y}">{escape(row["label"])}</text>',
                f'<text class="order-text" x="{x + 42}" y="{row_y - 7}">{escape(row["title"])}</text>',
                f'<text class="order-subtext" x="{x + 42}" y="{row_y + 10}">{escape(row["summary"])}</text>',
            ]
        )
    return "".join(parts)


def order_groups_html(scene: dict[str, object]) -> str:
    rows = order_group_rows(scene)
    if not rows:
        return ""
    items = []
    for row in rows:
        items.append(
            '<div class="order-group-row">'
            f'<span class="order-group-index">{escape(row["label"])}</span>'
            '<span>'
            f'<strong>{escape(row["title"])}</strong>'
            f'<small>{escape(row["summary"])}</small>'
            '</span>'
            '</div>'
        )
    return (
        '        <div><dt>3 things to order</dt><dd>'
        '<div class="order-groups">'
        + "".join(items)
        + "</div></dd></div>\n"
    )


def order_groups_overlay_html(scene: dict[str, object]) -> str:
    rows = order_group_rows(scene)
    if not rows:
        return ""
    items = []
    for row in rows:
        items.append(
            '<div class="order-overlay-row">'
            f'<span>{escape(row["label"])}</span>'
            f'<strong>{escape(row["title"])}</strong>'
            f'<small>{escape(row["summary"])}</small>'
            '</div>'
        )
    return (
        '<div class="order-overlay" aria-label="Three things to order">'
        '<h2>3 Things To Order</h2>'
        + "".join(items)
        + "</div>"
    )


def html_attr(value: object) -> str:
    return escape(str(value), {'"': "&quot;"})


def relative_asset(source: str, out_dir: Path) -> str:
    source_path = Path(source)
    absolute_source = source_path if source_path.is_absolute() else ROOT / source_path
    return os.path.relpath(absolute_source, out_dir).replace(os.sep, "/")


def matching_design_boxes(section: dict[str, object], scene: dict[str, object]) -> list[dict[str, object]]:
    matches = [str(item).lower() for item in section.get("design_matches", [])]
    if not matches:
        return []
    selected: list[dict[str, object]] = []
    for box in scene.get("boxes", []):
        haystack = f"{box.get('name', '')} {box.get('label', '')}".lower()
        if any(match in haystack for match in matches):
            selected.append(box)
    return selected


def design_preview_svg(section: dict[str, object], scene: dict[str, object]) -> str:
    boxes = matching_design_boxes(section, scene)
    if not boxes:
        return (
            '<div class="design-empty">No 3D design preview is assigned yet.</div>'
        )

    def raw_iso(point: tuple[float, float, float]) -> tuple[float, float]:
        x, z, y = point
        return (x - z) * 0.72, (x + z) * 0.32 - y * 1.1

    box_polygons: list[tuple[dict[str, object], list[list[tuple[float, float, float]]]]] = []
    raw_points: list[tuple[float, float]] = []
    for box in boxes:
        x0 = float(box["x"]) - float(box["w"]) / 2
        z0 = float(box["z"]) - float(box["d"]) / 2
        y0 = float(box["y"])
        w = float(box["w"])
        d = float(box["d"])
        h = float(box["h"])
        polygons = [
            [(x0 + w, z0, y0), (x0 + w, z0 + d, y0), (x0 + w, z0 + d, y0 + h), (x0 + w, z0, y0 + h)],
            [(x0, z0 + d, y0), (x0 + w, z0 + d, y0), (x0 + w, z0 + d, y0 + h), (x0, z0 + d, y0 + h)],
            [(x0, z0, y0 + h), (x0 + w, z0, y0 + h), (x0 + w, z0 + d, y0 + h), (x0, z0 + d, y0 + h)],
        ]
        box_polygons.append((box, polygons))
        for polygon_points in polygons:
            raw_points.extend(raw_iso(point) for point in polygon_points)

    min_x = min(point[0] for point in raw_points)
    max_x = max(point[0] for point in raw_points)
    min_y = min(point[1] for point in raw_points)
    max_y = max(point[1] for point in raw_points)
    width = max(max_x - min_x, 1)
    height = max(max_y - min_y, 1)
    pad = 18
    scale = min((360 - 2 * pad) / width, (206 - 2 * pad) / height)

    def local_points(points: list[tuple[float, float, float]]) -> str:
        projected: list[str] = []
        for point in points:
            px, py = raw_iso(point)
            x = pad + (px - min_x) * scale
            y = pad + (py - min_y) * scale
            projected.append(f"{x:.1f},{y:.1f}")
        return " ".join(projected)

    elems: list[str] = ['<rect class="design-bg" width="360" height="206" rx="6" />']
    for index, (box, polygons) in enumerate(box_polygons):
        color_key = str(box.get("color", "rubber"))
        top = MATERIALS[color_key]["color"]
        side = MATERIALS[color_key]["side"]
        elems.append(f'<polygon class="design-side" style="fill:{side}" points="{local_points(polygons[0])}" />')
        elems.append(f'<polygon class="design-side" style="fill:{side}" points="{local_points(polygons[1])}" />')
        elems.append(f'<polygon class="design-top" style="fill:{top}" points="{local_points(polygons[2])}" />')
        label = str(box.get("label", "")).strip()
        if label and index == 0:
            elems.append(f'<text class="design-label" x="14" y="194">{escape(label)}</text>')

    return f"""<svg class="design-preview" viewBox="0 0 360 206" role="img" aria-label="{html_attr(section.get('id', 'rubber'))} 3D design preview">
  <style>
    .design-bg {{ fill: #f7f9fa; }}
    .design-top, .design-side {{ stroke: #303941; stroke-width: 1; }}
    .design-label {{ font: 700 12px Arial, sans-serif; fill: #1d252c; }}
  </style>
  {''.join(elems)}
</svg>"""


def rubber_sections_html(scene: dict[str, object], out_dir: Path) -> str:
    sections = [
        section
        for section in scene.get("rubber_sections", [])
        if isinstance(section, dict)
    ]
    if not sections:
        return ""

    section_rows: list[str] = []
    for section in sections:
        section_id = html_attr(section.get("id", "rubber"))
        title = escape(str(section.get("title", "")))
        quantity = escape(str(section.get("quantity", "")))
        spec = escape(str(section.get("spec", "")))
        images = [
            image
            for image in section.get("images", [])
            if isinstance(image, dict) and str(image.get("src", "")).strip()
        ]
        image_rows: list[str] = []
        for image in images:
            source = str(image.get("src", "")).strip()
            relative_source = relative_asset(source, out_dir)
            label = escape(str(image.get("label", "")).strip() or Path(source).stem)
            caption = escape(str(image.get("caption", "")).strip())
            image_rows.append(
                f'<figure class="item-photo"><img src="{html_attr(relative_source)}" alt="{label}" loading="lazy">'
                f'<figcaption><strong>{label}</strong>{("<br>" + caption) if caption else ""}</figcaption></figure>'
            )
        image_detail = (
            '<div class="photo-grid">'
            + "".join(image_rows)
            + "</div>"
            if image_rows
            else '<div class="empty-note">No confirmed old rubber images are attached to this line yet.</div>'
        )
        model_file = str(section.get("model_file", "")).strip()
        model_link = ""
        if model_file:
            model_link = (
                f'<a class="model-link" href="{html_attr(relative_asset(model_file, out_dir))}">'
                "OpenSCAD source</a>"
            )
        section_rows.append(
            f"""      <section class="rubber-section" id="{section_id}">
        <div class="rubber-header">
          <div>
            <h3>{section_id}</h3>
            <p>{title}</p>
          </div>
          <span>{quantity}</span>
        </div>
        <div class="rubber-content">
          <div class="rubber-gallery">
            <h4>Known Existing Rubber Images ({len(image_rows)})</h4>
            {image_detail}
          </div>
          <div class="rubber-design">
            <h4>3D Design</h4>
            {design_preview_svg(section, scene)}
            <p>{spec}</p>
            {model_link}
          </div>
        </div>
      </section>"""
        )

    return (
        '      <h2 class="photos-heading">Rubber Evidence And Design</h2>\n'
        '      <div class="rubber-sections">\n'
        + "\n".join(section_rows)
        + "\n      </div>\n"
    )


def write_svg(package_id: str, scene: dict[str, object]) -> None:
    css: list[str] = []
    elems: list[str] = [
        '<rect class="background" width="920" height="620" />',
        '<ellipse class="shadow" cx="455" cy="430" rx="330" ry="74" />',
    ]
    part_labels: list[str] = []
    for index, box in enumerate(scene.get("boxes", [])):
        parts = prism(box, index)
        css.extend(parts[:2])
        elems.extend(parts[2:])
        label = box_static_label(box)
        if label:
            part_labels.append(label)
    title = escape(str(scene["title"]))
    subtitle = escape(str(scene["subtitle"]))
    labels = [
        f'<text class="title" x="34" y="46">{title}</text>',
        f'<text class="subtitle" x="34" y="74">{subtitle}</text>',
        '<text class="label" x="34" y="556">Static assembly visual. Open the HTML file for rotate/zoom interaction.</text>',
        *part_labels,
        height_callout_legend(scene),
        order_group_legend(scene),
    ]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="620" viewBox="0 0 920 620" role="img">
  <style>
    .background {{ fill: #f6f7f8; }}
    .shadow {{ fill: #d8dde2; opacity: 0.7; }}
    .title {{ font: 700 26px Arial, sans-serif; fill: #202a33; }}
    .subtitle, .label {{ font: 16px Arial, sans-serif; fill: #4f5d68; }}
    .part-label {{ font: 700 13px Arial, sans-serif; fill: #111820; stroke: #ffffff; stroke-width: 4px; paint-order: stroke; }}
    .callout {{ stroke: #111820; stroke-width: 1.1; opacity: 0.78; }}
    .legend-box {{ fill: #ffffff; stroke: #c8d0d8; stroke-width: 1; opacity: 0.96; }}
    .legend-title {{ font: 700 15px Arial, sans-serif; fill: #202a33; }}
    .legend-text {{ font: 13px Arial, sans-serif; fill: #27323a; }}
    .order-box {{ fill: #ffffff; stroke: #c8d0d8; stroke-width: 1; opacity: 0.96; }}
    .order-title {{ font: 700 15px Arial, sans-serif; fill: #202a33; }}
    .order-dot {{ fill: #202a33; }}
    .order-dot-text {{ font: 700 11px Arial, sans-serif; fill: #ffffff; text-anchor: middle; }}
    .order-text {{ font: 700 12px Arial, sans-serif; fill: #202a33; }}
    .order-subtext {{ font: 11px Arial, sans-serif; fill: #4f5d68; }}
    {''.join(css)}
  </style>
  {''.join(elems)}
  {''.join(labels)}
</svg>
"""
    out_dir = FAB_DIR / package_id
    (out_dir / f"{package_id}_3d_visualisation.svg").write_text(svg, encoding="utf-8")


def write_html(package_id: str, scene: dict[str, object]) -> None:
    scene_json = json.dumps(scene, separators=(",", ":"))
    height_rows = [str(row).strip() for row in scene.get("height_callouts", []) if str(row).strip()]
    height_detail = ""
    if height_rows:
        height_detail = (
            "        <div><dt>Height / thickness</dt><dd>"
            + "<br>".join(escape(row) for row in height_rows)
            + "</dd></div>\n"
        )
    order_group_detail = order_groups_html(scene)
    order_group_overlay = order_groups_overlay_html(scene)
    out_dir = FAB_DIR / package_id
    rubber_section_detail = rubber_sections_html(scene, out_dir)
    item_images = [
        image
        for image in scene.get("item_images", [])
        if isinstance(image, dict) and str(image.get("src", "")).strip()
    ]
    item_image_detail = ""
    if rubber_section_detail:
        item_image_detail = rubber_section_detail
    elif item_images:
        image_rows = []
        for image in item_images:
            source = str(image.get("src", "")).strip()
            relative_source = relative_asset(source, out_dir)
            label = escape(str(image.get("label", "")).strip() or Path(source).stem)
            caption = escape(str(image.get("caption", "")).strip())
            image_rows.append(
                f'<figure class="item-photo"><img src="{html_attr(relative_source)}" alt="{label}" loading="lazy">'
                f'<figcaption><strong>{label}</strong>{("<br>" + caption) if caption else ""}</figcaption></figure>'
            )
        item_image_detail = (
            '      <h2 class="photos-heading">Item Photos</h2>\n'
            '      <div class="photo-grid">\n'
            + "\n".join(f"        {row}" for row in image_rows)
            + "\n      </div>\n"
        )
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
    main {{ display: grid; grid-template-columns: minmax(420px, 1fr) minmax(420px, 520px); align-items: start; min-height: 0; }}
    #viewport {{ position: sticky; top: 0; height: calc(100vh - 134px); min-height: 560px; max-height: 860px; overflow: hidden; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
    .order-overlay {{ position: absolute; z-index: 3; left: 18px; top: 18px; width: min(340px, calc(100% - 36px)); padding: 12px; border: 1px solid #c8d0d8; border-radius: 8px; background: rgba(255, 255, 255, 0.94); box-shadow: 0 10px 30px rgba(20, 30, 40, 0.12); pointer-events: none; }}
    .order-overlay h2 {{ margin: 0 0 8px; font-size: 14px; }}
    .order-overlay-row {{ display: grid; grid-template-columns: 22px 1fr; column-gap: 8px; row-gap: 2px; align-items: start; padding: 7px 0; border-top: 1px solid #e4e8eb; }}
    .order-overlay-row:first-of-type {{ border-top: 0; }}
    .order-overlay-row span {{ display: grid; place-items: center; width: 20px; height: 20px; border-radius: 50%; background: #202a33; color: #fff; font-size: 11px; font-weight: 700; }}
    .order-overlay-row strong {{ font-size: 13px; line-height: 1.2; }}
    .order-overlay-row small {{ grid-column: 2; color: #54616c; font-size: 12px; line-height: 1.25; }}
    aside {{ border-left: 1px solid #d8dde2; background: #fff; padding: 18px; overflow: auto; }}
    h2 {{ margin: 0 0 12px; font-size: 18px; letter-spacing: 0; }}
    dl {{ margin: 0; display: grid; gap: 12px; }}
    dt {{ font-weight: 700; }}
    dd {{ margin: 3px 0 0; color: #54616c; font-size: 14px; line-height: 1.45; }}
    .order-groups {{ display: grid; gap: 8px; }}
    .order-group-row {{ display: grid; grid-template-columns: 26px 1fr; gap: 9px; align-items: start; color: #1d252c; }}
    .order-group-index {{ display: grid; place-items: center; width: 24px; height: 24px; border-radius: 50%; background: #202a33; color: #fff; font-size: 12px; font-weight: 700; }}
    .order-group-row strong {{ display: block; color: #1d252c; font-size: 13px; }}
    .order-group-row small {{ display: block; color: #54616c; font-size: 12px; line-height: 1.3; }}
    .photos-heading {{ margin-top: 22px; }}
    .photo-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }}
    .item-photo {{ margin: 0; min-width: 0; }}
    .item-photo img {{ display: block; width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border: 1px solid #d8dde2; border-radius: 6px; background: #f5f6f7; }}
    .item-photo figcaption {{ margin-top: 4px; color: #54616c; font-size: 12px; line-height: 1.25; }}
    .item-photo strong {{ color: #1d252c; }}
    .rubber-sections {{ display: grid; gap: 16px; }}
    .rubber-section {{ border: 1px solid #cfd7de; border-radius: 8px; background: #fff; overflow: hidden; }}
    .rubber-header {{ display: flex; justify-content: space-between; gap: 12px; align-items: flex-start; padding: 13px 14px; background: #f8fafb; border-bottom: 1px solid #d8dde2; }}
    .rubber-header h3 {{ margin: 0; font-size: 16px; letter-spacing: 0; }}
    .rubber-header p {{ margin: 4px 0 0; color: #54616c; font-size: 13px; line-height: 1.35; }}
    .rubber-header span {{ white-space: nowrap; border: 1px solid #c8d0d8; border-radius: 999px; padding: 4px 8px; background: #fff; font-size: 12px; color: #33414c; }}
    .rubber-content {{ display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(170px, 0.95fr); gap: 14px; padding: 14px; }}
    .rubber-gallery h4,
    .rubber-design h4 {{ margin: 0 0 9px; font-size: 13px; text-transform: uppercase; letter-spacing: .04em; color: #46545f; }}
    .rubber-design p {{ margin: 9px 0 0; color: #46545f; font-size: 13px; line-height: 1.4; }}
    .design-preview {{ display: block; width: 100%; border: 1px solid #d8dde2; border-radius: 7px; background: #f7f9fa; }}
    .design-empty,
    .empty-note {{ border: 1px dashed #c8d0d8; border-radius: 7px; color: #667580; background: #f8fafb; padding: 12px; font-size: 13px; line-height: 1.4; }}
    .model-link {{ display: inline-flex; margin-top: 10px; color: #174b7a; font-size: 13px; font-weight: 700; text-decoration: none; }}
    .model-link:hover {{ text-decoration: underline; }}
    #fallback {{ position: absolute; inset: 0; display: grid; place-items: center; padding: 20px; background: #f5f6f7; }}
    #fallback img {{ width: min(94vw, 920px); max-height: 82vh; object-fit: contain; }}
    body.is-three-ready #fallback {{ display: none; }}
    body.embed header,
    body.embed aside {{ display: none; }}
    body.embed main {{ grid-template-columns: 1fr; min-height: 100vh; height: 100vh; }}
    body.embed #viewport {{ min-height: 100vh; height: 100vh; }}
    @media (max-width: 1060px) {{ main {{ grid-template-columns: 1fr; }} #viewport {{ position: relative; top: auto; height: 430px; min-height: 430px; max-height: none; }} aside {{ border-left: 0; border-top: 1px solid #d8dde2; }} .order-overlay {{ max-width: 300px; }} }}
    @media (max-width: 640px) {{ .rubber-content {{ grid-template-columns: 1fr; }} .photo-grid {{ grid-template-columns: 1fr; }} }}
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
      {order_group_overlay}
    </section>
    <aside>
      <h2>Assembly Read</h2>
      <dl>
        <div><dt>Package role</dt><dd>{escape(str(scene["subtitle"]))}</dd></div>
        <div><dt>Load path</dt><dd>{escape(str(scene["load_path"]))}</dd></div>
{order_group_detail}
{height_detail}        <div><dt>Service intent</dt><dd>{escape(str(scene["service_intent"]))}</dd></div>
      </dl>
{item_image_detail}
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
      rubberWorn: [0x2b2d2a, 0.01, 0.82],
      rust: [0x6c4935, 0.18, 0.78],
      silver: [0xd4d8dc, 0.35, 0.32],
      void: [0xf5f6f7, 0.0, 0.85],
      white: [0xf4f6f8, 0.02, 0.3],
      bendline: [0x2f3942, 0.05, 0.58],
    }};
    const materials = Object.fromEntries(Object.entries(materialDefs).map(([key, value]) => [
      key,
      new THREE.MeshStandardMaterial({{ color: value[0], metalness: value[1], roughness: value[2] }})
    ]));
    const edgeMaterial = new THREE.LineBasicMaterial({{ color: 0x25313a, transparent: true, opacity: 0.48 }});
    const holeEdgeMaterial = new THREE.LineBasicMaterial({{ color: 0x8a949d, transparent: true, opacity: 0.92 }});

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

    function roundedRectShape(width, depth, radius = 0) {{
      const halfW = width / 2;
      const halfD = depth / 2;
      const r = Math.min(radius, halfW, halfD);
      const shape = new THREE.Shape();
      shape.moveTo(-halfW + r, -halfD);
      shape.lineTo(halfW - r, -halfD);
      shape.quadraticCurveTo(halfW, -halfD, halfW, -halfD + r);
      shape.lineTo(halfW, halfD - r);
      shape.quadraticCurveTo(halfW, halfD, halfW - r, halfD);
      shape.lineTo(-halfW + r, halfD);
      shape.quadraticCurveTo(-halfW, halfD, -halfW, halfD - r);
      shape.lineTo(-halfW, -halfD + r);
      shape.quadraticCurveTo(-halfW, -halfD, -halfW + r, -halfD);
      return shape;
    }}

    function capsuleShape(length, width) {{
      const r = width / 2;
      const endOffset = Math.max(0, (length - width) / 2);
      const shape = new THREE.Shape();
      shape.moveTo(-endOffset, -r);
      shape.lineTo(endOffset, -r);
      shape.absarc(endOffset, 0, r, -Math.PI / 2, Math.PI / 2, false);
      shape.lineTo(-endOffset, r);
      shape.absarc(-endOffset, 0, r, Math.PI / 2, Math.PI * 1.5, false);
      return shape;
    }}

    function teardropShape() {{
      const points = [
        [24.0, 0.0], [31.5, 1.2], [38.1, 4.8], [43.2, 10.0],
        [46.8, 16.5], [48.0, 24.0], [44.8, 38.4], [38.0, 50.0],
        [38.0, 70.0], [32.0, 84.0], [16.0, 84.0], [10.0, 70.0],
        [10.0, 50.0], [3.2, 38.4], [0.0, 24.0], [1.2, 16.5],
        [4.8, 10.0], [9.9, 4.8], [16.5, 1.2],
      ];
      return new THREE.Shape(points.map(([x, z]) => new THREE.Vector2(x - 24, z - 42)));
    }}

    function roundedRectOutline(width, depth, radius = 0, segments = 56) {{
      const points = roundedRectShape(width, depth, radius).getSpacedPoints(segments);
      if (points.length > 1 && points[0].distanceTo(points[points.length - 1]) < 0.001) {{
        points.pop();
      }}
      return points;
    }}

    function taperedBumpStopGeometry(item) {{
      const bottom = roundedRectOutline(item.w, item.d, item.corner_r || 0, 64);
      const top = roundedRectOutline(item.top_w || item.w * 0.78, item.top_d || item.d * 0.75, item.top_corner_r || item.corner_r || 0, 64);
      const count = Math.min(bottom.length, top.length);
      const vertices = [];
      for (let index = 0; index < count; index += 1) {{
        vertices.push(bottom[index].x, 0, bottom[index].y);
      }}
      for (let index = 0; index < count; index += 1) {{
        vertices.push(top[index].x, item.h, top[index].y);
      }}
      vertices.push(0, 0, 0);
      vertices.push(0, item.h, 0);
      const bottomCenter = count * 2;
      const topCenter = count * 2 + 1;
      const indices = [];
      for (let index = 0; index < count; index += 1) {{
        const next = (index + 1) % count;
        indices.push(index, next, count + next);
        indices.push(index, count + next, count + index);
        indices.push(bottomCenter, next, index);
        indices.push(topCenter, count + index, count + next);
      }}
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute("position", new THREE.Float32BufferAttribute(vertices, 3));
      geometry.setIndex(indices);
      geometry.computeVertexNormals();
      return geometry;
    }}

    function planShape(item) {{
      if (item.shape === "capsule") return capsuleShape(item.w, item.d);
      if (item.shape === "teardrop") return teardropShape();
      return roundedRectShape(item.w, item.d, item.corner_r || 0);
    }}

    function extrudedPlanGeometry(item) {{
      const shape = planShape(item);
      (item.holes || []).forEach((hole) => {{
        const path = new THREE.Path();
        path.absarc(hole.x || 0, hole.z || 0, hole.r || 1, 0, Math.PI * 2, true);
        shape.holes.push(path);
      }});
      const geometry = new THREE.ExtrudeGeometry(shape, {{
        depth: item.h,
        bevelEnabled: false,
        curveSegments: 48,
        steps: 1,
      }});
      geometry.rotateX(Math.PI / 2);
      geometry.translate(0, item.h / 2, 0);
      geometry.computeVertexNormals();
      return geometry;
    }}

    function addHoleVisuals(item) {{
      (item.holes || []).forEach((hole) => {{
        if (!hole.marker) return;
        const markerHeight = hole.marker_h || 0.8;
        const geometry = new THREE.CylinderGeometry(hole.r * 0.96, hole.r * 0.96, markerHeight, 48);
        const cutout = new THREE.Mesh(geometry, materials.void);
        cutout.name = `${{item.name}} visible hole marker`;
        cutout.position.set(item.x + (hole.x || 0), item.y + item.h + markerHeight / 2 + 0.04, item.z + (hole.z || 0));
        cutout.castShadow = false;
        cutout.receiveShadow = false;
        root.add(cutout);

        const edges = new THREE.LineSegments(new THREE.EdgesGeometry(geometry), holeEdgeMaterial);
        edges.position.copy(cutout.position);
        root.add(edges);
      }});
    }}

    function box(item) {{
      const geometry = item.shape === "tapered_bump_stop"
        ? taperedBumpStopGeometry(item)
        : item.shape
        ? extrudedPlanGeometry(item)
        : new THREE.BoxGeometry(item.w, item.h, item.d);
      const mesh = new THREE.Mesh(
        geometry,
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
      addHoleVisuals(item);
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
    (out_dir / f"{package_id}_3d_visualisation.html").write_text(html, encoding="utf-8")


def main() -> None:
    for package_id, scene in SCENES.items():
        out_dir = FAB_DIR / package_id
        out_dir.mkdir(parents=True, exist_ok=True)
        write_svg(package_id, scene)
        write_html(package_id, scene)


if __name__ == "__main__":
    main()
