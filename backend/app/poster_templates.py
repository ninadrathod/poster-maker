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
    # Muted champagne linen + espresso type + bronze / antique gold accents
    canvas = "#DCD3C7"
    img = Image.new("RGB", (POSTER_W, POSTER_H), canvas)
    draw = ImageDraw.Draw(img)
    sq = _img_for_template(product).convert("RGB")
    frame_pad = 32
    frame_top = 64
    frame_bottom = frame_top + frame_pad + sq.height + frame_pad
    draw.rectangle((48, frame_top, POSTER_W - 48, frame_bottom), fill="#141210")
    img.paste(sq, (48 + frame_pad, frame_top + frame_pad))

    # Product story on canvas (below image): large serif italic + mono kicker
    desc_y = frame_bottom + 44
    font_kicker = load_font(40, mono=True)
    font_desc = load_font(56, serif=True, italic=True)
    kicker_text = "// PRODUCT STORY"
    kicker_x, kicker_y = 58, desc_y
    draw.text((kicker_x, kicker_y), kicker_text, font=font_kicker, fill=(88, 72, 60))
    kicker_bbox = draw.textbbox((kicker_x, kicker_y), kicker_text, font=font_kicker)
    gap_below_kicker = 36
    y = kicker_bbox[3] + gap_below_kicker
    desc_color = (42, 36, 32)
    line_height = 62
    for line in wrap_text(description, font_desc, POSTER_W - 116, draw)[:5]:
        draw.text((58, y), line, font=font_desc, fill=desc_color)
        y += line_height

    rule_y = y + 28
    draw.rectangle((58, rule_y, POSTER_W - 58, rule_y + 3), fill="#2A2420")
    draw.rectangle((58, rule_y + 8, POSTER_W - 220, rule_y + 14), fill="#8B6A4E")

    bottom_y = POSTER_H - 272
    draw.rectangle((0, bottom_y, POSTER_W, POSTER_H), fill="#12100E")
    font_name = load_font(70, bold=True, italic=True)
    draw.text((56, bottom_y + 32), name.upper(), font=font_name, fill="#D9CBB3")
    font_price_label = load_font(22, mono=True)
    draw.text((56, POSTER_H - 118), "PRICE", font=font_price_label, fill=(148, 136, 124))
    font_price = load_font(78, bold=True, mono=True)
    draw.text((POSTER_W - 56, POSTER_H - 108), price, font=font_price, fill="#C4A574", anchor="rm")

    draw.rectangle((POSTER_W - 220, 48, POSTER_W - 48, 120), fill="#6E5844", outline="#2A2420", width=4)
    draw.text((POSTER_W - 134, 84), "NEW", font=load_font(36, bold=True), fill="#EDE6DC", anchor="mm")
    return img


# --- 2. Swiss minimal -------------------------------------------------------
def template_swiss(name: str, description: str, price: str, product: Image.Image) -> Image.Image:
    img = Image.new("RGB", (POSTER_W, POSTER_H), "#F7F7F5")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 48, POSTER_H), fill="#E63946")
    sq = _img_for_template(product).convert("RGB")
    img.paste(sq, (120, 140))
    draw.line((120, 920, POSTER_W - 80, 920), fill="#111111", width=4)
    # Sans bold oblique headline + large serif-italic body + mono price (Swiss grid / editorial catalog)
    font_h = load_font(68, bold=True, italic=True)
    font_desc = load_font(42, serif=True, italic=True)
    font_price = load_font(62, bold=True, mono=True)
    name_x, name_y = 120, 960
    draw.text((name_x, name_y), name, font=font_h, fill="#111111")
    name_bbox = draw.textbbox((name_x, name_y), name, font=font_h)
    gap_after_name = 36
    y = name_bbox[3] + gap_after_name
    desc_line = 50
    for line in wrap_text(description, font_desc, POSTER_W - 200, draw)[:4]:
        draw.text((120, y), line, font=font_desc, fill=(52, 48, 46))
        y += desc_line
    draw.text((POSTER_W - 80, POSTER_H - 96), price, font=font_price, fill="#E63946", anchor="rm")
    draw.text((120, 80), "COLLECTION", font=load_font(24, mono=True), fill="#6B6B6B")
    return img


# --- 3. Retro sunset (twilight / luxe dusk) --------------------------------
def template_sunset(name: str, description: str, price: str, product: Image.Image) -> Image.Image:
    # Classy vertical gradient: warm stone → deep aubergine ink
    top_rgb = (218, 208, 198)
    bottom_rgb = (48, 44, 58)
    base = Image.new("RGB", (POSTER_W, POSTER_H))
    px = base.load()
    denom = max(POSTER_H - 1, 1)
    for y in range(POSTER_H):
        t = y / denom
        r = int(top_rgb[0] + (bottom_rgb[0] - top_rgb[0]) * t)
        g = int(top_rgb[1] + (bottom_rgb[1] - top_rgb[1]) * t)
        b = int(top_rgb[2] + (bottom_rgb[2] - top_rgb[2]) * t)
        for x in range(POSTER_W):
            px[x, y] = (r, g, b)
    img = base
    draw = ImageDraw.Draw(img)
    # Muted copper disc (sun)
    cy = int(POSTER_H * 0.4)
    draw.ellipse((POSTER_W // 2 - 170, cy - 170, POSTER_W // 2 + 170, cy + 170), fill=(176, 148, 118))
    sq = _img_for_template(product)
    sq = ImageOps.colorize(
        ImageOps.grayscale(sq),
        black="#1E1A18",
        white="#F4EDE4",
    ).convert("RGBA")
    rmask = rounded_rectangle_mask((sq.width, sq.height), 48)
    rounded = Image.new("RGBA", sq.size, (0, 0, 0, 0))
    rounded.paste(sq, (0, 0), rmask)
    img_y = 500
    img.paste(rounded, (POSTER_W // 2 - sq.width // 2, img_y), rounded)
    img_bottom = img_y + rounded.height
    gap_image_to_desc = 96
    font_t = load_font(78, bold=True, italic=True)
    shadow = (32, 28, 38)
    cx = POSTER_W // 2
    title_y = 188
    title_upper = name.upper()
    for dx, dy in [(-2, -2), (2, 2), (-2, 2), (2, -2)]:
        draw.text((cx + dx, title_y + dy), title_upper, font=font_t, fill=shadow, anchor="mm")
    draw.text((cx, title_y), title_upper, font=font_t, fill=(248, 242, 234), anchor="mm")
    font_b = load_font(44, serif=True, italic=True)
    font_kicker = load_font(26, mono=True)
    desc_y = img_bottom + gap_image_to_desc
    kicker = "— OVERVIEW —"
    draw.text((cx, desc_y), kicker, font=font_kicker, fill=(190, 178, 168), anchor="mm")
    kbb = draw.textbbox((cx, desc_y), kicker, font=font_kicker, anchor="mm")
    y = kbb[3] + 30
    desc_line = 54
    for line in wrap_text(description, font_b, POSTER_W - 140, draw)[:4]:
        draw.text((cx, y), line, font=font_b, fill=(232, 224, 216), anchor="mm")
        y += desc_line
    font_pr = load_font(74, bold=True, mono=True)
    draw.text((cx, POSTER_H - 128), price, font=font_pr, fill=(212, 184, 148), anchor="mm")
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
