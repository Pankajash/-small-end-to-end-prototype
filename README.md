# Pickabook – Story Illustration Personalisation Prototype

This repository contains a small end‑to‑end prototype for the Pickabook assignment.

The goal is to let a user upload a child's photo, run it through an AI‑style
personalisation pipeline, and insert the stylised face into a storybook
illustration.

## Tech choices

- **Frontend:** Plain React (via CDN) with a small single‑page UI.
- **Backend:** Python + FastAPI (chosen for quick API development and easy
  integration with Python‑based ML tooling).
- **Image work:** Pillow (PIL) for cropping, light "cartoon" stylisation and
  compositing.
- **Model strategy (conceptual):** Instant‑ID + SDXL (or a similar ID‑preserving
  adapter) running on a GPU service such as Replicate or a small internal
  inference server.

The current implementation keeps the heavy model call mocked so it can run
locally on CPU without extra dependencies.
