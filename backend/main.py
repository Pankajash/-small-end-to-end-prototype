import base64
import io
import os

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image, ImageOps

"""
FastAPI backend for the Pickabook illustration personalisation demo.

Notes
-----
- The actual face detection + Instant-ID style transfer step is intentionally
  simplified here to keep the prototype lightweight.
- In a real deployment I would replace the `stylise_and_compose` function
  with a call to a GPU-backed service (e.g. Replicate) running:
    * Instant-ID + SDXL
    * OR a custom ControlNet
"""

app = FastAPI(title="Pickabook Personalisation API")

# Basic CORS for local development with the static React page
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, lock this down.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to the provided illustration template
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "assets", "template.png")


def load_template() -> Image.Image:
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"Template illustration not found at {TEMPLATE_PATH}")
    return Image.open(TEMPLATE_PATH).convert("RGBA")


def centre_crop_face(source: Image.Image) -> Image.Image:
    """Very naive 'face crop' just for the demo.

    For the assignment write-up I explain that this should be replaced with a
    proper face detector such as Mediapipe or InsightFace. Here we just crop
    the central square region, assuming the user's face is roughly centered.
    """
    w, h = source.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return source.crop((left, top, left + side, top + side))


def stylise_and_compose(face: Image.Image, template: Image.Image) -> Image.Image:
    """Mock stylisation + composition.

    Instead of actually calling Instant-ID + SDXL, I simulate a cartoon
    effect and paste the face into a fixed region of the template.

    Implementation details:
    - Convert face to a smaller square, apply slight posterization to mimic a
      "stylised" look.
    - Paste it onto the template at a pre-defined bounding box.
    """
    # Resize face to fit a placeholder area on the template
    target_size = (260, 260)
    face = face.resize(target_size, Image.LANCZOS)

    # Quick 'cartoonish' effect using posterize + auto contrast
    face = ImageOps.posterize(face, bits=4)
    face = ImageOps.autocontrast(face)

    # Ensure RGBA for alpha-compositing
    if face.mode != "RGBA":
        face = face.convert("RGBA")

    composed = template.copy()

    # These coordinates represent where the child's head is in the template.
    # I eyeballed these numbers based on the reference image.
    x, y = 180, 120
    composed.alpha_composite(face, dest=(x, y))
    return composed


@app.post("/api/personalize")
async def personalize(photo: UploadFile = File(...)) -> JSONResponse:
    """Accept a child's photo and return a personalised illustration.

    Input: multipart/form-data with a single file field 'photo'.
    Output: JSON with a base64-encoded PNG image.
    """
    try:
        contents = await photo.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        # 1. "Detect" and crop the face (simplified).
        face_region = centre_crop_face(image)

        # 2. Load the illustration template.
        template = load_template()

        # 3. Stylise + compose.
        result = stylise_and_compose(face_region, template)

        # Encode as base64 PNG for the frontend.
        buffer = io.BytesIO()
        result.save(buffer, format="PNG")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

        return JSONResponse({"image_base64": image_base64})
    except Exception as exc:
        return JSONResponse(
            {"error": f"Failed to personalise image: {exc}"},
            status_code=500,
        )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
