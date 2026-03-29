"""Shared helpers for 1024×2048 poster templates."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont, ImageOps

POSTER_W = 1024
POSTER_H = 2048

# Max relative difference between width and height to count as square (2%).
SQUARE_ASPECT_TOLERANCE = 0.02


def image_is_square(img: Image.Image, tolerance: float = SQUARE_ASPECT_TOLERANCE) -> bool:
    w, h = img.size
    if w <= 0 or h <= 0:
        return False
    return abs(w - h) / max(w, h) <= tolerance


def normalize_uploaded_product(img: Image.Image) -> Image.Image:
    """Apply EXIF orientation, flatten transparency onto white, return RGBA.

    Without this, RGBA → RGB uses black for transparent pixels (solid black blocks on posters).
    """
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGBA")
    base = Image.new("RGBA", img.size, (255, 255, 255, 255))
    return Image.alpha_composite(base, img)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
FONT_SANS = FONT_DIR / "DejaVuSans.ttf"
FONT_SANS_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
FONT_SERIF = FONT_DIR / "DejaVuSerif.ttf"
FONT_SERIF_BOLD = FONT_DIR / "DejaVuSerif-Bold.ttf"
FONT_MONO = FONT_DIR / "DejaVuSansMono-Bold.ttf"


def load_font(size: int, bold: bool = False, serif: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    if mono and FONT_MONO.exists():
        return ImageFont.truetype(str(FONT_MONO), size)
    if serif:
        path = FONT_SERIF_BOLD if bold else FONT_SERIF
        if path.exists():
            return ImageFont.truetype(str(path), size)
    path = FONT_SANS_BOLD if bold else FONT_SANS
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def ensure_square_rgba(img: Image.Image, side: int) -> Image.Image:
    img = img.convert("RGBA")
    w, h = img.size
    s = min(w, h)
    left = (w - s) // 2
    top = (h - s) // 2
    img = img.crop((left, top, left + s, top + s))
    return img.resize((side, side), Image.Resampling.LANCZOS)


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = (" ".join(current + [word])).strip()
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def default_product_image(side: int = 512) -> Image.Image:
    """Placeholder square when no upload is provided."""
    img = Image.new("RGBA", (side, side), (45, 52, 64, 255))
    d = ImageDraw.Draw(img)
    for i in range(side):
        t = i / max(side - 1, 1)
        c = int(80 + t * 80)
        d.line([(0, i), (side, i)], fill=(c, c + 20, c + 40, 255))
    font = load_font(side // 6, bold=True)
    d.text((side // 2, side // 2), "★", font=font, fill=(255, 220, 100, 255), anchor="mm")
    font2 = load_font(side // 14)
    d.text((side // 2, side // 2 + side // 5), "PRODUCT", font=font2, fill=(255, 255, 255, 230), anchor="mm")
    return img


def rounded_rectangle_mask(size: Tuple[int, int], radius: int) -> Image.Image:
    w, h = size
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
    return mask
