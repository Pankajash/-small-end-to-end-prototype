# Short Technical Note (for reviewers)

## 1. Model choice

For a production‑ready version, I would use **Instant‑ID + SDXL** (or a similar
ID‑preserving adapter):

- Instant‑ID (built on top of ControlNet) lets me lock onto the child’s identity
  from a reference photo using facial landmarks + ID embeddings.
- SDXL gives strong base image quality and style control (storybook / 3D / 2D).
- The combination is widely adopted, easy to host on services like Replicate,
  and has a good ecosystem of examples for face‑personalised avatars.

In this prototype, the heavy model step is replaced by a light Pillow pipeline:

1. Detect + crop the face region (centre crop in code, but in a real version I
   would plug in **Mediapipe** or **InsightFace** for robust detection).
2. Apply a small "cartoon" style (posterisation + contrast).
3. Paste the processed face into the correct area of the provided template.

The structure of the code keeps this stylisation logic in a single function
(`stylise_and_compose`) so swapping in the real model later is easy.

## 2. Limitations I hit

- **No GPU / model weights in this repo**: To keep the submission light‑weight
  and easy to run on any laptop, I avoided bundling large diffusion checkpoints.
- **Simplified face detection**: The current version assumes the face is roughly
  centred in the photo. For edge cases (tilted heads, multiple faces,
  occlusions) a real detector is required.
- **Single template layout**: I hard‑coded one bounding box where the face is
  pasted. Multiple illustrations (different poses, camera angles) would need
  per‑template metadata.
- **No persistent storage or auth**: Every request is processed in memory.
  That’s fine for a demo but not enough for a real consumer app.

## 3. What I would improve in v2

1. **Real Instant‑ID integration**
   - Wrap the Instant‑ID + SDXL pipeline as a separate microservice.
   - Call it asynchronously from FastAPI (background task or queue) so the UI
     stays responsive.
   - Add simple controls (style preset, intensity) to the frontend.

2. **Better face handling**
   - Use Mediapipe / InsightFace to detect face bounding boxes and landmarks.
   - Auto‑align and crop the face before sending it to the model.
   - Store per‑template alignment configs (scale, rotation, offsets).

3. **More templates + personalisation options**
   - Allow multiple scenes (e.g., "garden", "space", "underwater") and let
     the child pick which one to appear in.
   - Extend to hair / skin‑tone prompts while keeping identity preserved.

4. **Deployable cloud setup**
   - Backend on Vercel / Fly.io / AWS Fargate.
   - Model inference on a GPU service (Replicate or a dedicated EC2 G instance).
   - Simple monitoring (request logs, latency, and error tracking).

5. **Safety & privacy**
   - Auto‑delete uploaded photos and generated images after a short TTL.
   - Blur or reject images containing adults or unsafe content.
   - Add a clear consent notice for parents in the UI.

This prototype is intentionally small but built so the real system can be
layered on top without rewriting the whole codebase.
