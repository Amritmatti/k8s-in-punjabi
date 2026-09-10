import os
import shutil
import uuid
from pathlib import Path
from threading import Lock, Thread

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from .pipeline import generate_video

BASE = Path(os.getenv("DATA_DIR", "/data"))
UPLOADS = BASE / "uploads"
OUTPUT = BASE / "output"
for p in (UPLOADS, OUTPUT):
    p.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="AI Video Generator", version="0.1.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
JOBS = {}
LOCK = Lock()

ALLOWED = {".jpg", ".jpeg", ".png", ".webp"}


def run_job(job_id: str, image_path: str, text: str, voice: str, duration: int):
    with LOCK:
        JOBS[job_id]["status"] = "processing"
    try:
        out = generate_video(job_id, Path(image_path), text, voice, duration)
        with LOCK:
            JOBS[job_id].update(status="completed", video=f"/api/jobs/{job_id}/video")
    except Exception as exc:
        with LOCK:
            JOBS[job_id].update(status="failed", error=str(exc))


@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("app/static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/generate")
async def generate(
    image: UploadFile = File(...),
    text: str = Form(...),
    voice: str = Form("en-US-AriaNeural"),
    duration: int = Form(10),
):
    if not text.strip():
        raise HTTPException(400, "Text is required")
    if duration < 3 or duration > int(os.getenv("MAX_DURATION_SECONDS", "60")):
        raise HTTPException(400, "Invalid duration")
    ext = Path(image.filename or "image.jpg").suffix.lower()
    if ext not in ALLOWED:
        raise HTTPException(400, "Use JPG, PNG or WEBP")

    job_id = uuid.uuid4().hex
    image_path = UPLOADS / f"{job_id}{ext}"
    with image_path.open("wb") as f:
        shutil.copyfileobj(image.file, f)

    with LOCK:
        JOBS[job_id] = {"status": "queued", "video": None, "error": None}
    Thread(target=run_job, args=(job_id, str(image_path), text, voice, duration), daemon=True).start()
    return {"job_id": job_id, "status": "queued"}


@app.get("/api/jobs/{job_id}")
def status(job_id: str):
    with LOCK:
        job = JOBS.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return {"job_id": job_id, **job}


@app.get("/api/jobs/{job_id}/video")
def video(job_id: str):
    path = OUTPUT / f"{job_id}.mp4"
    if not path.exists():
        raise HTTPException(404, "Video is not ready")
    return FileResponse(path, media_type="video/mp4", filename=f"reel-{job_id}.mp4")
