"""FastAPI web application — stub for future implementation."""
from __future__ import annotations


def create_app():
    """Create FastAPI application."""
    try:
        from fastapi import FastAPI
    except ImportError:
        raise ImportError("Install with: pip install 'jyotish[web]'")

    app = FastAPI(title="Jyotish", version="1.0.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
