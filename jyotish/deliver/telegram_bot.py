"""Telegram bot for chart delivery (optional — needs python-telegram-bot)."""

from __future__ import annotations

from jyotish.config import get as cfg_get


def create_bot():
    """Create and configure the Telegram bot.

    Requires: pip install python-telegram-bot
    """
    try:
        from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
    except ImportError:
        raise RuntimeError(
            "python-telegram-bot not installed. Run: pip install python-telegram-bot\n"
            "Or install with: pip install vedic-ai-framework[telegram]"
        )

    token = cfg_get("daily.telegram_bot_token", "")
    if not token:
        raise RuntimeError(
            "Telegram bot token not configured. "
            "Set daily.telegram_bot_token in config.yaml or TELEGRAM_BOT_TOKEN env var."
        )

    app = ApplicationBuilder().token(token).build()

    async def start(update, context):
        await update.message.reply_text(
            "🙏 Namaste! I am Jyotish AI.\n\n"
            "Send me birth details in this format:\n"
            "CHART Name | DD/MM/YYYY | HH:MM | Place\n\n"
            "Example:\n"
            "CHART Rajesh Kumar | 15/08/1990 | 06:30 | Jaipur"
        )

    async def handle_chart_request(update, context):
        text = update.message.text
        if not text.startswith("CHART"):
            await update.message.reply_text("Send: CHART Name | DD/MM/YYYY | HH:MM | Place")
            return

        try:
            parts = text.replace("CHART ", "").split("|")
            name = parts[0].strip()
            dob = parts[1].strip()
            tob = parts[2].strip()
            place = parts[3].strip()

            from jyotish.compute.chart import compute_chart
            from jyotish.interpret.formatter import format_chart_terminal

            chart = compute_chart(name=name, dob=dob, tob=tob, place=place)
            report = format_chart_terminal(chart)

            # Telegram has 4096 char limit
            if len(report) > 4000:
                report = report[:4000] + "\n\n... (truncated)"

            await update.message.reply_text(report)
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chart_request))

    return app


def run_bot():
    """Start the Telegram bot."""
    app = create_bot()
    app.run_polling()
