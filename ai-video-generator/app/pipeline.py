import asyncio
import os
import subprocess
from pathlib import Path

import edge_tts


def run(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-4000:])


def make_audio(text: str, voice: str, output: Path):
    async def _save():
        await edge_tts.Communicate(text, voice).save(str(output))
    asyncio.run(_save())


def generate_video(job_id: str, image: Path, text: str, voice: str, duration: int) -> Path:
    work = Path(os.getenv("DATA_DIR", "/data")) / "jobs" / job_id
    work.mkdir(parents=True, exist_ok=True)
    audio = work / "voice.mp3"
    output = Path(os.getenv("DATA_DIR", "/data")) / "output" / f"{job_id}.mp4"

    make_audio(text, voice, audio)

    width = int(os.getenv("OUTPUT_WIDTH", "2160"))
    height = int(os.getenv("OUTPUT_HEIGHT", "3840"))
    fps = int(os.getenv("FPS", "30"))
    crf = os.getenv("CRF", "18")

    # Subtle continuous zoom plus horizontal drift creates smooth motion from one image.
    frames = duration * fps
    vf = (
        f"scale={width*2}:{height*2}:force_original_aspect_ratio=increase,"
        f"crop={width*2}:{height*2},"
        f"zoompan=z='min(zoom+0.00035,1.12)':"
        f"x='iw/2-(iw/zoom/2)+sin(on/25)*35':"
        f"y='ih/2-(ih/zoom/2)+cos(on/31)*25':"
        f"d=1:s={width}x{height}:fps={fps},"
        f"format=yuv420p"
    )

    run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(image),
        "-i", str(audio),
        "-t", str(duration),
        "-vf", vf,
        "-c:v", "libx264", "-preset", os.getenv("X264_PRESET", "medium"),
        "-crf", crf,
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart",
        str(output),
    ])
    return output
