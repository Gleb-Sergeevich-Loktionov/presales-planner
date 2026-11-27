FROM python:3.12-slim

# ffmpeg: faster-whisper decodes Telegram .ogg voice notes through it.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev

ENTRYPOINT ["./docker-entrypoint.sh"]
