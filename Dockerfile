# Stage 1: Builder
FROM python:3.11-slim-bookworm@sha256:061c190f3d5815b341a18dfe8a45771f8ba68c15a607ea56997fde3009ac4eec AS builder

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv

RUN /opt/venv/bin/pip install --no-cache-dir --upgrade pip setuptools

RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
RUN rm -rf /opt/venv/lib/python3.11/site-packages/pip \
    /opt/venv/lib/python3.11/site-packages/pip-*.dist-info \
    /opt/venv/bin/pip \
    /opt/venv/bin/pip3 \
    /opt/venv/bin/pip3.11
# Stage 2: Runtime
FROM python:3.11-slim-bookworm@sha256:061c190f3d5815b341a18dfe8a45771f8ba68c15a607ea56997fde3009ac4eec AS runtime

WORKDIR /app

RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade urllib3 msgpack \
    && /usr/local/bin/python -m pip uninstall -y setuptools wheel

ENV PATH="/opt/venv/bin:$PATH"

# Copy installed packages from the builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code and model
COPY src/ ./src/
COPY models/ ./models/

# Create a non-root user
RUN useradd --create-home --uid 10001 appuser

# Run the application as the non-root user
USER appuser

EXPOSE 8000

# Check whether the API is healthy
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"]

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]