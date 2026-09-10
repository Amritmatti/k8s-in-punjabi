# AI Video Generator

Dockerized AI-style video generation platform for Instagram Reels.

## What it does

Upload an image, enter text, choose voice/language and duration, then generate a vertical Reel with:

- 9:16 vertical format
- 2160x3840 (4K UHD) output
- Smooth Ken Burns zoom/pan motion
- Text-to-speech narration
- Optional background music
- H.264 video + AAC audio in MP4
- Browser UI and REST API
- Job status and generated video download

> MVP note: this version creates smooth cinematic motion from the supplied image. The architecture keeps a video-generation provider interface so a true diffusion/video-model backend can be added later without changing the UI/API.

## Architecture

```text
Browser
  |
  v
FastAPI Web UI / API :8000
  |
  +--> Job worker
  |      |
  |      +--> TTS (Edge TTS)
  |      +--> FFmpeg motion compositor
  |      +--> 4K Reel encoder
  |
  +--> /data/uploads
  +--> /data/jobs
  +--> /data/output
```

## Run with Docker

```bash
git clone https://github.com/Amritmatti/k8s-in-punjabi.git
cd k8s-in-punjabi/ai-video-generator
cp .env.example .env
docker compose up --build
```

Open `http://localhost:8000`.

Generated files are persisted in `./data`.

## API

### Generate

```bash
curl -X POST http://localhost:8000/api/generate \
  -F 'image=@./my-image.jpg' \
  -F 'text=Welcome to my channel! Today we are learning something amazing.' \
  -F 'voice=en-US-AriaNeural' \
  -F 'duration=10'
```

Response:

```json
{"job_id":"...","status":"queued"}
```

Check status:

```bash
curl http://localhost:8000/api/jobs/<job_id>
```

Download:

```bash
curl -O http://localhost:8000/api/jobs/<job_id>/video
```

## Configuration

See `.env.example`.

- `OUTPUT_WIDTH=2160`
- `OUTPUT_HEIGHT=3840`
- `FPS=30`
- `CRF=18`
- `MAX_DURATION_SECONDS=60`
- `TTS_PROVIDER=edge`

For a GPU-based true AI video backend, implement the provider interface in `app/video_provider.py` and point the worker at your model/API. The rest of the platform remains unchanged.

## Instagram Reel target

Default output is **2160x3840, 30 FPS, H.264, AAC, 9:16**. For faster local generation, lower the output resolution or FPS in `.env`.

## Security / production notes

- Do not expose this service directly to the public internet without authentication and rate limiting.
- Put secrets in Docker/Kubernetes secrets rather than Git.
- Add object storage (S3/GCS) for production output.
- Add Redis + a dedicated worker for concurrent jobs.
- GPU video models require substantially more RAM/VRAM than this CPU MVP.
