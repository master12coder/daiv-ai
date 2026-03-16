FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir ".[groq]"

# Copy application
COPY . .

# Create data directories
RUN mkdir -p data/pandit_corrections data/charts

ENTRYPOINT ["python", "-m", "jyotish.cli"]
CMD ["--help"]
