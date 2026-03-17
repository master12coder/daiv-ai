"""Telegram bot for daily companion delivery — stub."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


async def start_bot(token: str) -> None:
    """Start the Telegram bot."""
    try:
        from telegram.ext import ApplicationBuilder
    except ImportError:
        raise ImportError("Install with: pip install 'jyotish[telegram]'")

    logger.info("Starting Telegram bot...")
    app = ApplicationBuilder().token(token).build()
    # Handlers will be registered here
    await app.run_polling()
