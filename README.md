# Poster Maker

Simple web app: pick one of 10 poster templates (1024×2048), enter product copy, get a PNG.

## Stack

- **Backend:** Python 3.12, FastAPI, Pillow — one render function per template in `backend/app/poster_templates.py`.
- **Frontend:** Vite + React — horizontal “Netflix-style” template row; modal form; rendered image + download.
- **Docker:** `frontend` (nginx + static build) and `backend` (uvicorn) on shared bridge network `poster-maker-net`. Browser calls `/api/...` on the frontend host; nginx proxies to the backend.

## Run with Docker

From this directory:

```bash
docker compose up --build -d
```

Open **http://localhost:8080**.

Stop and remove containers:

```bash
docker compose down
```

## Local development (without Docker)

**Backend** (Python 3.12 recommended; install system fonts similar to the image, or rely on Pillow defaults):

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 7000
```

**Frontend** (Node 20+):

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` to `http://127.0.0.1:7000`. Use **http://localhost:5173** with the API on port 7000.

## API (for reference)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/health` | Health check |
| GET | `/api/templates` | JSON list of templates |
| GET | `/api/templates/{id}/preview.png` | PNG preview (shared dummy copy + placeholder product image) |
| POST | `/api/templates/{id}/render.png` | `multipart/form-data`: `product_name`, `product_description` (max 180 chars), `price`, `product_image` (file). Image must be square (equal width & height), max 8MB → PNG |

Previews still use a built-in placeholder image; rendered posters use the uploaded square product photo. Uploads are auto-oriented (EXIF), and transparent pixels are composited on **white** before flattening—so outline-style PNGs show correctly instead of turning black when converted for the layout.
