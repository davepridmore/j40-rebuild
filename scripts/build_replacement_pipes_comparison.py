#!/usr/bin/env python3
"""Build the documentary old/new replacement-pipes comparison image."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
OLD_PHOTO = ROOT / "photos/20260502_004044_gp_Hx4Yo0Qg.jpg"
NEW_PHOTO = ROOT / "photos/20260712_012946_gp_GJur42bg.jpg"
OUTPUT = ROOT / "docs/generated/replacement-pipes-old-new-comparison-20260816.png"

FONT_REGULAR = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def fitted_photo(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as source:
        photo = ImageOps.exif_transpose(source).convert("RGB")
    photo.thumbnail(size, Image.Resampling.LANCZOS)
    stage = Image.new("RGB", size, "#dedbd2")
    x = (size[0] - photo.width) // 2
    y = (size[1] - photo.height) // 2
    stage.paste(photo, (x, y))
    return stage


def draw_panel(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    x: int,
    label: str,
    detail: str,
    photo_path: Path,
    photo_ref: str,
) -> None:
    panel_y = 320
    panel_w = 1080
    panel_h = 980
    draw.rounded_rectangle(
        (x, panel_y, x + panel_w, panel_y + panel_h),
        radius=28,
        fill="#ffffff",
        outline="#cbc5b8",
        width=3,
    )
    draw.text((x + 30, panel_y + 28), label, font=font(FONT_BOLD, 48), fill="#17232a")
    draw.text((x + 30, panel_y + 88), detail, font=font(FONT_REGULAR, 30), fill="#536067")

    photo = fitted_photo(photo_path, (1020, 765))
    photo_x = x + 30
    photo_y = panel_y + 145
    canvas.paste(photo, (photo_x, photo_y))
    draw.rectangle(
        (photo_x, photo_y, photo_x + 1020, photo_y + 765),
        outline="#b7b0a3",
        width=2,
    )
    draw.text(
        (x + 30, panel_y + 932),
        photo_ref,
        font=font(FONT_REGULAR, 25),
        fill="#6b716f",
    )


def main() -> None:
    for path in (OLD_PHOTO, NEW_PHOTO):
        if not path.exists():
            raise FileNotFoundError(path)

    canvas = Image.new("RGB", (2400, 1500), "#f3efe6")
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle((80, 50, 570, 102), radius=22, fill="#217a52")
    draw.ellipse((104, 67, 122, 85), fill="#ffffff")
    draw.text((140, 60), "ACQUISITION CLOSED", font=font(FONT_BOLD, 30), fill="#ffffff")

    draw.text((80, 125), "Replacement pipes — old / new", font=font(FONT_BOLD, 72), fill="#17232a")
    draw.text(
        (80, 220),
        "Original assemblies retained as patterns · Replacement pipe, hose and clamp set received",
        font=font(FONT_REGULAR, 36),
        fill="#536067",
    )

    draw_panel(
        canvas,
        draw,
        80,
        "OLD",
        "Original assemblies / pattern set",
        OLD_PHOTO,
        "Evidence: 2026-05-02 · 20260502_004044_gp_Hx4Yo0Qg",
    )
    draw_panel(
        canvas,
        draw,
        1240,
        "NEW",
        "Received replacement pipe / hose / clamp set",
        NEW_PHOTO,
        "Evidence: 2026-07-12 · 20260712_012946_gp_GJur42bg",
    )

    draw.text(
        (80, 1360),
        "Boundary: circuit mapping, fitment, installation and pressure/service validation remain open.",
        font=font(FONT_BOLD, 32),
        fill="#8a4c22",
    )
    draw.text(
        (80, 1410),
        "Documentary comparison only — source photos are unaltered apart from scaling and layout.",
        font=font(FONT_REGULAR, 28),
        fill="#6b716f",
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT, quality=95)
    print(OUTPUT)


if __name__ == "__main__":
    main()
