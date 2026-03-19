FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies for pyswisseph (C extension)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy package definitions first (Docker layer caching)
COPY engine/pyproject.toml engine/pyproject.toml
COPY products/pyproject.toml products/pyproject.toml
COPY apps/pyproject.toml apps/pyproject.toml

# Copy source code
COPY engine/ engine/
COPY products/ products/
COPY apps/ apps/
COPY assets/ assets/

# Install all packages (web + telegram + groq)
RUN pip install --no-cache-dir \
    -e engine/ \
    -e "products/[groq]" \
    -e "apps/[web,telegram]" \
    gunicorn

# Create runtime directories
RUN mkdir -p data charts

# Copy charts if they exist
COPY charts/ charts/ 2>/dev/null || true

# Healthcheck via HTTP
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Expose web port
EXPOSE 8000

# Default: run web server
CMD ["gunicorn", "jyotish_app.web.app:create_app()", \
     "-w", "2", "-k", "uvicorn.workers.UvicornWorker", \
     "-b", "0.0.0.0:8000", "--timeout", "120"]
