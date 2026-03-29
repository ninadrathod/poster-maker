"""Ten creative 1024×2048 poster template renderers."""

from __future__ import annotations

import random
from typing import Callable

from PIL import Image, ImageDraw, ImageFilter, ImageOps

from .render_utils import (
    POSTER_H,
    POSTER_W,
    default_product_image,
    ensure_square_rgba,
    load_font,
    rounded_rectangle_mask,
    wrap_text,
)

TemplateFn = Callable[[str, str, str, Image.Image], Image.Image]


def _img_for_template(product: Image.Image) -> Image.Image:
    return ensure_square_rgba(product, 720)


# --- 1. Brutalist stack -----------------------------------------------------
def template_brutalist(name: str, description: str, price: str, product: Image.Image) -> Image.Image:
    img = Image.new("RGB", (POSTER_W, POSTER_H), "#FCEE21")
    draw = ImageDraw.Draw(img)
    sq = _img_for_template(product).convert("RGB")
    draw.rectangle((48, 64, POSTER_W - 48, 64 + 720), fill="#111111")
    img.paste(sq, (48 + 32, 64 + 32))
    draw.rectangle((0, POSTER_H - 280, POSTER_W, POSTER_H), fill="#111111")
    font_title = load_font(72, bold=True)
    font_body = load_font(32)
    font_price = load_font(96, bold=True)
    draw.text((56, POSTER_H - 260), name.upper(), font=font_title, fill="#FCEE21")
    y = POSTER_H - 180
    for line in wrap_text(description, font_body, POSTER_W - 120, draw)[:3]:
        draw.text((56, y), line, font=font_body, fill="#CCCCCC")
        y += 38
    draw.text((POSTER_W - 56, POSTER_H - 120), price, font=font_price, fill="#FCEE21", anchor="rm")
    draw.rectangle((POSTER_W - 220, 48, POSTER_W - 48, 120), fill="#FF0055", outline="#111111", width=6)
    draw.text((POSTER_W - 134, 84), "NEW", font=load_font(36, bold=True), fill="#111111", anchor="mm")
    return img


# --- 2. Swiss minimal -------------------------------------------------------
def template_swiss(name: str, description: str, price: str, product: Image.Image) -> Image.Image:
    img = Image.new("RGB", (POSTER_W, POSTER_H), "#F7F7F5")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 48, POSTER_H), fill="#E63946")
    sq = _img_for_template(product).convert("RGB")
    img.paste(sq, (120, 140))
    draw.line((120, 920, POSTER_W - 80, 920), fill="#111111", width=4)
    font_h = load_font(64, bold=True)
    font_p = load_font(42, bold=True)
    font_b = load_font(28)
    draw.text((120, 960), name, font=font_h, fill="#111111")
    y = 1050
    for line in wrap_text(description, font_b, POSTER_W - 200, draw)[:4]:
        draw.text((120, y), line, font=font_b, fill="#444444")
        y += 36
    draw.text((POSTER_W - 80, POSTER_H - 100), price, font=font_p, fill="#E63946", anchor="rm")
    draw.text((120, 80), "COLLECTION", font=load_font(22), fill="#888888")
    return img


# --- 3. Retro sunset --------------------------------------------------------
def template_sunset(name: str, description: str, price: str, product: Image.Image) -> Image.Image:
    base = Image.new("RGB", (POSTER_W, POSTER_H))
    px = base.load()
    for y in range(POSTER_H):
        t = y / POSTER_H
        r = int(255 * (0.95 - t * 0.4))
        g = int(120 + t * 80)
        b = int(60 + t * 140)
        for x in range(POSTER_W):
            px[x, y] = (r, g, b)
    img = base
    draw = ImageDraw.Draw(img)
    # Sun
    cy = int(POSTER_H * 0.42)
    draw.ellipse((POSTER_W // 2 - 180, cy - 180, POSTER_W // 2 + 180, cy + 180), fill="#FF9F1C")
    sq = _img_for_template(product)
    sq = ImageOps.colorize(
        ImageOps.grayscale(sq),
        black="#2B0F0A",
        white="#FFF5E6",
    ).convert("RGBA")
    rmask = rounded_rectangle_mask((sq.width, sq.height), 48)
    rounded = Image.new("RGBA", sq.size, (0, 0, 0, 0))
    rounded.paste(sq, (0, 0), rmask)
    img.paste(rounded, (POSTER_W // 2 - sq.width // 2, 520), rounded)
    font_t = load_font(68, bold=True)
    font_b = load_font(30)
    font_pr = load_font(56, bold=True)
    shadow = (40, 40, 40)
    for dx, dy in [(-2, -2), (2, 2), (-2, 2), (2, -2)]:
        draw.text((POSTER_W // 2 + dx, 200 + dy), name.upper(), font=font_t, fill=shadow, anchor="mm")
    draw.text((POSTER_W // 2, 200), name.upper(), font=font_t, fill="#FFF8E7", anchor="mm")
    y = 1320
    for line in wrap_text(description, font_b, POSTER_W - 160, draw)[:3]:
        draw.text((POSTER_W // 2, y), line, font=font_b, fill="#2D1B2E", anchor="mm")
        y += 40
    draw.text((POSTER_W // 2, POSTER_H - 140), price, font=font_pr, fill="#FF006E", anchor="mm")
    return img


# --- 4. Editorial magazine --------------------------------------------------
def template_editorial(name: str, description: str, price: str, product: Image.Image) -> Image.Image:
    img = Image.new("RGB", (POSTER_W, POSTER_H), "#1a1a1a")
    sq = _img_for_template(product).convert("RGB")
    img.paste(sq, (POSTER_W // 2 - sq.width // 2, 100))
    overlay = Image.new("RGBA", (POSTER_W, 720), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, POSTER_W, 720), fill=(0, 0, 0, 200))
    img.paste(overlay, (0, POSTER_H - 720), overlay)
    draw = ImageDraw.Draw(img)
    font_t = load_font(56, bold=True, serif=True)
    font_b = load_font(28, serif=True)
    font_p = load_font(48, bold=True)
    draw.text((72, POSTER_H - 640), name, font=font_t, fill="#F5F0E8")
    y = POSTER_H - 560
    for line in wrap_text(description, font_b, POSTER_W - 144, draw)[:4]:
        draw.text((72, y), line, font=font_b, fill="#C4B8A8")
        y += 34
    draw.text((72, POSTER_H - 120), price, font=font_p, fill="#C9A962")
    draw.text((POSTER_W - 72, 72), "ISSUE 01", font=load_font(20), fill="#666666", anchor="rt")
    return img


# --- 5. Neon night ----------------------------------------------------------
def template_neon(name: str, description: str, price: str, product: Image.Image) -> Image.Image:
    img = Image.new("RGB", (POSTER_W, POSTER_H), "#0D0221")
    draw = ImageDraw.Draw(img)
    for i in range(0, POSTER_H, 40):
        draw.line((0, i, POSTER_W, i), fill="#1a0a2e", width=1)
    sq = ensure_square_rgba(product, 680)
    glow = Image.new("RGBA", (sq.width + 40, sq.height + 40), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle((0, 0, glow.width, glow.height), 24, outline=(0, 255, 255, 180), width=8)
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    gx = POSTER_W // 2 - glow.width // 2
    gy = 380
    img.paste(glow, (gx, gy), glow)
    img.paste(sq.convert("RGB"), (POSTER_W // 2 - sq.width // 2, 400))
    font_t = load_font(64, bold=True, mono=True)
    font_b = load_font(26, mono=True)
    font_p = load_font(52, bold=True, mono=True)
    for ox, col in [(3, "#FF00FF"), (-3, "#00FFF0"), (0, "#FFFFFF")]:
        draw.text((POSTER_W // 2 + ox, 200), name.upper(), font=font_t, fill=col, anchor="mm")
    y = 1120
    for line in wrap_text(description, font_b, POSTER_W - 100, draw)[:3]:
        draw.text((POSTER_W // 2, y), line, font=font_b, fill="#B8FFF9", anchor="mm")
        y += 34
    draw.text((POSTER_W // 2, POSTER_H - 130), price, font=font_p, fill="#FF4DFF", anchor="mm")
    return img


# --- 6. Pastel dream --------------------------------------------------------
def template_pastel(name: str, description: str, price: str, product: Image.Image) -> Image.Image:
    img = Image.new("RGB", (POSTER_W, POSTER_H), "#FFF0F5")
    draw = ImageDraw.Draw(img)
    draw.ellipse((-120, 200, 380, 700), fill="#FFD6E8")
    draw.ellipse((700, 1200, POSTER_W + 100, 1900), fill="#D6E8FF")
    draw.ellipse((500, 300, 900, 700), fill="#E8FFD6")
    sq = _img_for_template(product).convert("RGB")
    rmask = rounded_rectangle_mask((sq.width, sq.height), 64)
    rounded = Image.new("RGBA", sq.size, (0, 0, 0, 0))
    rounded.paste(sq, (0, 0), rmask)
    img.paste(rounded, (POSTER_W // 2 - sq.width // 2, 320), rounded)
    font_t = load_font(62, bold=True)
    font_b = load_font(28)
    font_p = load_font(48, bold=True)
    draw.text((POSTER_W // 2, 1080), name, font=font_t, fill="#5C4A6B", anchor="mm")
    y = 1160
    for line in wrap_text(description, font_b, POSTER_W - 140, draw)[:3]:
        draw.text((POSTER_W // 2, y), line, font=font_b, fill="#7A6B8C", anchor="mm")
        y += 36
    draw.rounded_rectangle(
        (POSTER_W // 2 - 140, POSTER_H - 130, POSTER_W // 2 + 140, POSTER_H - 60),
        radius=28,
        fill="#FFB7C5",
        outline="#5C4A6B",
        width=2,
    )
    draw.text((POSTER_W // 2, POSTER_H - 95), price, font=font_p, fill="#3D3550", anchor="mm")
    return img


# --- 7. Bauhaus -------------------------------------------------------------
def template_bauhaus(name: str, description: str, price: str, product: Image.Image) -> Image.Image:
    img = Image.new("RGB", (POSTER_W, POSTER_H), "#F4F1E8")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, POSTER_W, 180), fill="#1D3557")
    draw.rectangle((0, 180, 220, POSTER_H), fill="#E63946")
    draw.ellipse((POSTER_W - 280, POSTER_H - 400, POSTER_W - 40, POSTER_H - 160), fill="#F4D35E")
    draw.rectangle((40, POSTER_H - 120, 200, POSTER_H - 40), fill="#1D3557")
    sq = ensure_square_rgba(product, 560)
    img.paste(sq.convert("RGB"), (POSTER_W // 2 - sq.width // 2 + 60, 360))
    font_t = load_font(52, bold=True)
    font_b = load_font(26)
    font_p = load_font(44, bold=True)
    draw.text((POSTER_W // 2, 90), "BAUHAUS", font=load_font(28, bold=True), fill="#F4F1E8", anchor="mm")
    draw.text((POSTER_W // 2, 1020), name.upper(), font=font_t, fill="#1D3557", anchor="mm")
    y = 1100
    for line in wrap_text(description, font_b, POSTER_W - 180, draw)[:3]:
        draw.text((POSTER_W // 2, y), line, font=font_b, fill="#444444", anchor="mm")
        y += 34
    draw.text((POSTER_W - 80, POSTER_H - 80), price, font=font_p, fill="#E63946", anchor="rm")
    return img


# --- 8. Luxury gold ---------------------------------------------------------
def template_luxury(name: str, description: str, price: str, product: Image.Image) -> Image.Image:
    img = Image.new("RGB", (POSTER_W, POSTER_H), "#0A0A0A")
    draw = ImageDraw.Draw(img)
    margin = 36
    draw.rectangle(
        (margin, margin, POSTER_W - margin, POSTER_H - margin),
        outline="#C9A962",
        width=6,
    )
    draw.line((margin, 200, POSTER_W - margin, 200), fill="#C9A962", width=2)
    sq = _img_for_template(product).convert("RGB")
    img.paste(sq, (POSTER_W // 2 - sq.width // 2, 240))
    font_t = load_font(58, bold=True, serif=True)
    font_b = load_font(26, serif=True)
    font_p = load_font(52, bold=True)
    draw.text((POSTER_W // 2, 140), name, font=font_t, fill="#E8DCC4", anchor="mm")
    y = 1020
    for line in wrap_text(description, font_b, POSTER_W - 120, draw)[:4]:
        draw.text((POSTER_W // 2, y), line, font=font_b, fill="#9A8F7A", anchor="mm")
        y += 32
    draw.text((POSTER_W // 2, POSTER_H - 120), price, font=font_p, fill="#C9A962", anchor="mm")
    return img


# --- 9. Newsprint -----------------------------------------------------------
def template_newsprint(name: str, description: str, price: str, product: Image.Image) -> Image.Image:
    img = Image.new("RGB", (POSTER_W, POSTER_H), "#F2EDE4")
    draw = ImageDraw.Draw(img)
    random.seed(42)
    for _ in range(1200):
        x, y = random.randint(0, POSTER_W - 1), random.randint(0, POSTER_H - 1)
        c = random.randint(200, 230)
        draw.point((x, y), fill=(c, c - 5, c - 10))
    draw.rectangle((48, 48, POSTER_W - 48, 160), outline="#111111", width=3)
    draw.text((72, 72), "THE DAILY DROP", font=load_font(36, bold=True), fill="#111111")
    draw.text((72, 118), "VOL. 12 — SPECIAL", font=load_font(22), fill="#333333")
    sq = _img_for_template(product).convert("L")
    sq = ImageOps.colorize(sq, "#222222", "#F2EDE4").convert("RGB")
    img.paste(sq, (POSTER_W // 2 - sq.width // 2, 200))
    font_t = load_font(54, bold=True)
    font_b = load_font(28)
    font_p = load_font(46, bold=True)
    draw.text((POSTER_W // 2, 980), name.upper(), font=font_t, fill="#111111", anchor="mm")
    y = 1060
    for line in wrap_text(description, font_b, POSTER_W - 100, draw)[:3]:
        draw.text((POSTER_W // 2, y), line, font=font_b, fill="#333333", anchor="mm")
        y += 36
    draw.line((80, POSTER_H - 160, POSTER_W - 80, POSTER_H - 160), fill="#111111", width=2)
    draw.text((POSTER_W // 2, POSTER_H - 120), price, font=font_p, fill="#111111", anchor="mm")
    return img


# --- 10. Pop art halftone ----------------------------------------------------
def template_pop_art(name: str, description: str, price: str, product: Image.Image) -> Image.Image:
    img = Image.new("RGB", (POSTER_W, POSTER_H), "#FFF200")
    draw = ImageDraw.Draw(img)
    spacing = 14
    for y in range(0, POSTER_H, spacing):
        for x in range(0, POSTER_W, spacing):
            phase = (x + y) % (spacing * 3)
            r = max(2, spacing // 2 - phase // 6)
            draw.ellipse((x - r, y - r, x + r, y + r), fill="#FF00AA")
    # Clear band for product
    band = Image.new("RGB", (POSTER_W - 80, 900), "#FFF200")
    img.paste(band, (40, 280))
    sq = _img_for_template(product).convert("RGB")
    img.paste(sq, (POSTER_W // 2 - sq.width // 2, 320))
    font_t = load_font(64, bold=True)
    font_b = load_font(28)
    font_p = load_font(56, bold=True)
    draw.rectangle((40, 1240, POSTER_W - 40, 1380), fill="#00B4D8", outline="#111111", width=4)
    draw.text((POSTER_W // 2, 1310), name.upper(), font=font_t, fill="#111111", anchor="mm")
    y = 1420
    for line in wrap_text(description, font_b, POSTER_W - 100, draw)[:3]:
        draw.text((POSTER_W // 2, y), line, font=font_b, fill="#111111", anchor="mm")
        y += 36
    draw.text((POSTER_W // 2, POSTER_H - 100), price, font=font_p, fill="#111111", anchor="mm")
    return img


TEMPLATE_REGISTRY: dict[str, tuple[str, str, TemplateFn]] = {
    "1": ("Brutalist Stack", "Bold blocks, high contrast, sticker energy.", template_brutalist),
    "2": ("Swiss Rail", "Clean grid, red spine, museum-shop minimal.", template_swiss),
    "3": ("Retro Sunset", "Gradient sky, duotone product, poolside vibes.", template_sunset),
    "4": ("Editorial Night", "Magazine cover, serif type, gold price.", template_editorial),
    "5": ("Neon Grid", "Dark mode, cyan glow, terminal chic.", template_neon),
    "6": ("Pastel Dream", "Soft blobs, rounded photo, candy button.", template_pastel),
    "7": ("Bauhaus Lab", "Primary shapes, asymmetric layout.", template_bauhaus),
    "8": ("Midnight Gold", "Thin gold frame, luxury serif.", template_luxury),
    "9": ("Newsprint", "Grainy paper, headline rail, grayscale photo.", template_newsprint),
    "10": ("Pop Halftone", "Magenta dots, poster yellow, loud type.", template_pop_art),
}


def list_templates() -> list[dict]:
    return [
        {"id": tid, "title": meta[0], "blurb": meta[1]}
        for tid, meta in sorted(TEMPLATE_REGISTRY.items(), key=lambda x: int(x[0]))
    ]


def render_template(template_id: str, name: str, description: str, price: str, product: Image.Image | None) -> Image.Image:
    if template_id not in TEMPLATE_REGISTRY:
        raise KeyError(template_id)
    fn = TEMPLATE_REGISTRY[template_id][2]
    pic = product if product is not None else default_product_image()
    return fn(name, description, price, pic)
