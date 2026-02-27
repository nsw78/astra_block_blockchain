# ── Stage 1: build dependencies ──
FROM python:3.12-slim AS builder

WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: production image ──
FROM python:3.12-slim

# non-root user
RUN groupadd -r astra && useradd -r -g astra -d /app -s /sbin/nologin astra

WORKDIR /app

# copy installed packages from builder
COPY --from=builder /install /usr/local

# copy application code
COPY . /app

# create data dir owned by app user
RUN mkdir -p /app/data && chown -R astra:astra /app

USER astra

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENVIRONMENT=production

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/v1/health')"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1", "--log-level", "warning"]
