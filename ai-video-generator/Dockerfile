FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
RUN mkdir -p /data/uploads /data/jobs /data/output

ENV DATA_DIR=/data
ENV OUTPUT_WIDTH=2160
ENV OUTPUT_HEIGHT=3840
ENV FPS=30
ENV CRF=18
ENV MAX_DURATION_SECONDS=60
ENV X264_PRESET=medium

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
