"""Poster maker API — list templates, preview with dummy data, render from form input."""

from __future__ import annotations

import io

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from PIL import Image

from .poster_templates import list_templates, render_template
from .render_utils import default_product_image, image_is_square, normalize_uploaded_product

DUMMY_NAME = "Velvet Ember Candle"
DUMMY_DESC = (
    "Hand-poured soy wax with cedar smoke and vanilla. Burns clean for 45 hours — "
    "the cozy glow your shelf deserves."
)
DUMMY_PRICE = "$34.00"

MAX_NAME_LEN = 80
MAX_DESC_CHARS = 180
MAX_PRICE_LEN = 32
MAX_IMAGE_BYTES = 8 * 1024 * 1024

app = FastAPI(title="Poster Maker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _png_bytes(img) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def _load_uploaded_image(data: bytes) -> Image.Image:
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=400, detail="Image file is too large (max 8MB).")
    try:
        img = Image.open(io.BytesIO(data))
        img.load()
    except OSError:
        raise HTTPException(status_code=400, detail="Invalid image file.")
    img = normalize_uploaded_product(img)
    if not image_is_square(img):
        raise HTTPException(
            status_code=400,
            detail="Product image must be square (equal width and height).",
        )
    return img


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/templates")
def get_templates():
    return {"templates": list_templates()}


@app.get("/api/templates/{template_id}/preview.png")
def preview_png(template_id: str):
    try:
        img = render_template(
            template_id,
            DUMMY_NAME,
            DUMMY_DESC,
            DUMMY_PRICE,
            default_product_image(),
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="Unknown template")
    return Response(content=_png_bytes(img), media_type="image/png")


@app.post("/api/templates/{template_id}/render.png")
async def render_png(
    template_id: str,
    product_name: str = Form(...),
    product_description: str = Form(...),
    price: str = Form(...),
    product_image: UploadFile = File(...),
):
    name = product_name.strip()
    desc = product_description.strip()
    price_s = price.strip()
    if not name or len(name) > MAX_NAME_LEN:
        raise HTTPException(status_code=400, detail="Invalid product name.")
    if not desc or len(desc) > MAX_DESC_CHARS:
        raise HTTPException(status_code=400, detail="Invalid product description.")
    if not price_s or len(price_s) > MAX_PRICE_LEN:
        raise HTTPException(status_code=400, detail="Invalid price.")

    raw = await product_image.read()
    pil_img = _load_uploaded_image(raw)

    try:
        out = render_template(template_id, name, desc, price_s, pil_img)
    except KeyError:
        raise HTTPException(status_code=404, detail="Unknown template")
    return Response(content=_png_bytes(out), media_type="image/png")
