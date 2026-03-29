import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import "./App.css";

type TemplateMeta = { id: string; title: string; blurb: string };

const DESC_MAX = 180;
const SQUARE_TOLERANCE = 0.02;

function previewSrc(id: string) {
  return `/api/templates/${id}/preview.png`;
}

function parseErrorDetail(detail: unknown): string {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (item && typeof item === "object" && "msg" in item) {
          return String((item as { msg: string }).msg);
        }
        return String(item);
      })
      .join("; ");
  }
  return "Request failed";
}

function validateSquareImage(file: File): Promise<string | null> {
  return new Promise((resolve) => {
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => {
      URL.revokeObjectURL(url);
      const w = img.naturalWidth;
      const h = img.naturalHeight;
      if (w <= 0 || h <= 0) {
        resolve("Invalid image.");
        return;
      }
      const diff = Math.abs(w - h);
      const maxDim = Math.max(w, h);
      if (diff / maxDim > SQUARE_TOLERANCE) {
        resolve("Please upload a square image (width and height must match).");
        return;
      }
      resolve(null);
    };
    img.onerror = () => {
      URL.revokeObjectURL(url);
      resolve("Could not read this image file.");
    };
    img.src = url;
  });
}

export default function App() {
  const [templates, setTemplates] = useState<TemplateMeta[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [submitting, setSubmitting] = useState(false);
  const [resultUrl, setResultUrl] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await fetch("/api/templates");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        if (!cancelled) setTemplates(data.templates ?? []);
      } catch (e) {
        if (!cancelled) setLoadError(e instanceof Error ? e.message : "Failed to load templates");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const active = useMemo(
    () => templates.find((t) => t.id === activeId) ?? null,
    [templates, activeId]
  );

  const clearImage = useCallback(() => {
    if (imagePreviewUrl) URL.revokeObjectURL(imagePreviewUrl);
    setImagePreviewUrl(null);
    setImageFile(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }, [imagePreviewUrl]);

  const openModal = (id: string) => {
    setActiveId(id);
    setName("");
    setDescription("");
    setPrice("");
    clearImage();
    setResultUrl(null);
    setFormError(null);
  };

  const closeModal = () => {
    if (resultUrl) URL.revokeObjectURL(resultUrl);
    if (imagePreviewUrl) URL.revokeObjectURL(imagePreviewUrl);
    setResultUrl(null);
    setImagePreviewUrl(null);
    setImageFile(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
    setActiveId(null);
    setFormError(null);
  };

  const onImageChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    setFormError(null);
    if (!file) {
      clearImage();
      return;
    }
    const err = await validateSquareImage(file);
    if (err) {
      setFormError(err);
      clearImage();
      e.target.value = "";
      return;
    }
    if (imagePreviewUrl) URL.revokeObjectURL(imagePreviewUrl);
    setImagePreviewUrl(URL.createObjectURL(file));
    setImageFile(file);
  };

  const onSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      if (!activeId) return;
      setFormError(null);
      if (!imageFile) {
        setFormError("Please upload a square product image.");
        return;
      }
      if (description.length > DESC_MAX) {
        setFormError(`Description must be at most ${DESC_MAX} characters.`);
        return;
      }
      setSubmitting(true);
      if (resultUrl) URL.revokeObjectURL(resultUrl);
      setResultUrl(null);
      try {
        const fd = new FormData();
        fd.append("product_name", name.trim());
        fd.append("product_description", description.trim());
        fd.append("price", price.trim());
        fd.append("product_image", imageFile);

        const res = await fetch(`/api/templates/${activeId}/render.png`, {
          method: "POST",
          body: fd,
        });
        if (!res.ok) {
          const text = await res.text();
          let message = `HTTP ${res.status}`;
          if (text) {
            try {
              const data = JSON.parse(text) as { detail?: unknown };
              if (data?.detail != null) message = parseErrorDetail(data.detail);
              else message = text;
            } catch {
              message = text;
            }
          }
          throw new Error(message);
        }
        const blob = await res.blob();
        setResultUrl(URL.createObjectURL(blob));
      } catch (err) {
        setFormError(err instanceof Error ? err.message : "Render failed");
      } finally {
        setSubmitting(false);
      }
    },
    [activeId, name, description, price, imageFile, resultUrl]
  );

  return (
    <>
      <div className="app-layout">
        <aside className="sidebar" aria-label="About this app">
          <div className="sidebar-intro">
            <h1 className="sidebar-title">POSTER MAKER</h1>
            <ul className="sidebar-points">
              <li>Zero Photoshop—pick a look, drop in your copy, steal the scroll.</li>
              <li>Tall, proud posters built for stories, reels, and “just dropped” energy.</li>
              <li>Fill out the form and get your image—ready to post or print.</li>
              <li>Previews use the same engine as export; no surprises when you hit download.</li>
              <li>For anyone who’d rather ship the product than wrestle a design tool.</li>
            </ul>
          </div>
          <p className="sidebar-credit">
            <span className="sidebar-credit-line">
              Made with <span role="img" aria-label="love">❤️</span>,
            </span>
            <span className="sidebar-credit-line sidebar-credit-by">
              —by <span className="sidebar-credit-name">Ninad</span>
            </span>
          </p>
        </aside>

        <div className="main-scroll" role="region" aria-label="Template library">
          <main className="main-pane">
            {loadError && <p className="banner error">{loadError}</p>}

            <section className="templates-section" aria-label="Templates">
              <div className="poster-grid" role="list">
                {templates.map((t) => (
                  <button
                    key={t.id}
                    type="button"
                    className="tile"
                    onClick={() => openModal(t.id)}
                    role="listitem"
                  >
                    <div className="tile-frame">
                      <img
                        className="tile-img"
                        src={previewSrc(t.id)}
                        alt=""
                        loading="lazy"
                        width={200}
                        height={400}
                      />
                    </div>
                    <span className="tile-label">{t.title}</span>
                  </button>
                ))}
              </div>
            </section>
          </main>
        </div>
      </div>

      {active && (
        <div className="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="modal-title">
          <div className="modal">
            <div className="modal-head">
              <h2 id="modal-title">{active.title}</h2>
              <button type="button" className="icon-btn" onClick={closeModal} aria-label="Close">
                ×
              </button>
            </div>
            <p className="modal-blurb">{active.blurb}</p>

            {!resultUrl ? (
              <form className="form" onSubmit={onSubmit}>
                <label className="field">
                  <span>Product image (square)</span>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/jpeg,image/png,image/webp,image/gif"
                    onChange={onImageChange}
                    className="field-file-input"
                  />
                  <small className="field-hint">
                    Required: 1×1 aspect ratio (same width and height). JPEG, PNG, WebP, or GIF.
                    Transparent areas are filled with white on the poster.
                  </small>
                  {imagePreviewUrl && (
                    <div className="image-preview-wrap">
                      <img src={imagePreviewUrl} alt="Product preview" className="image-preview-thumb" />
                    </div>
                  )}
                </label>
                <label className="field">
                  <span>Product name</span>
                  <input
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    maxLength={80}
                    required
                    placeholder="e.g. Velvet Ember Candle"
                    autoComplete="off"
                  />
                </label>
                <label className="field">
                  <span>
                    Short description
                    <small className="hint"> — max {DESC_MAX} characters</small>
                  </span>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    maxLength={DESC_MAX}
                    required
                    rows={4}
                    placeholder="What makes it special?"
                  />
                  <span className="counter">
                    {description.length}/{DESC_MAX}
                  </span>
                </label>
                <label className="field">
                  <span>Price</span>
                  <input
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                    maxLength={32}
                    required
                    placeholder="$34.00"
                    autoComplete="off"
                  />
                </label>
                {formError && <p className="form-error">{formError}</p>}
                <button type="submit" className="primary" disabled={submitting}>
                  {submitting ? "Rendering…" : "Submit"}
                </button>
              </form>
            ) : (
              <div className="result">
                <div className="result-preview">
                  <p className="result-caption">Your poster</p>
                  <img className="result-img" src={resultUrl} alt="Rendered poster" />
                </div>
                <div className="result-actions">
                  <a className="download" href={resultUrl} download={`poster-${active.id}.png`}>
                    Download poster
                  </a>
                  <button
                    type="button"
                    className="secondary"
                    onClick={() => {
                      URL.revokeObjectURL(resultUrl);
                      setResultUrl(null);
                    }}
                  >
                    Edit inputs
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}
