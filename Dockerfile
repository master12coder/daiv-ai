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

# Install all packages + groq + telegram
RUN pip install --no-cache-dir \
    -e engine/ \
    -e "products/[groq]" \
    -e "apps/[telegram]"

# Create runtime directories
RUN mkdir -p data charts

# Copy chart if exists (for pre-built images)
COPY charts/ charts/

# Healthcheck
HEALTHCHECK --interval=60s --timeout=10s --retries=3 \
    CMD python -c "from jyotish_engine.compute.chart import compute_chart; print('ok')" || exit 1

# Default entrypoint
ENTRYPOINT ["python", "-m", "jyotish_app.cli.main"]
CMD ["--help"]
