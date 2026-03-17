"""Hindi language formatter for daily guidance."""
from __future__ import annotations

from jyotish_engine.compute.daily import DailySuggestion
from jyotish_engine.models.chart import ChartData

_VARA_HI = {
    "Sunday": "रविवार", "Monday": "सोमवार", "Tuesday": "मंगलवार",
    "Wednesday": "बुधवार", "Thursday": "गुरुवार",
    "Friday": "शुक्रवार", "Saturday": "शनिवार",
}

_DIGITS_HI = str.maketrans("0123456789", "०१२३४५६७८९")


def _to_hindi_num(n: int) -> str:
    """Convert number to Hindi digits."""
    return str(n).translate(_DIGITS_HI)


def format_hindi_simple(suggestion: DailySuggestion) -> str:
    """One-line Hindi format."""
    rating = _to_hindi_num(suggestion.day_rating)
    vara = _VARA_HI.get(suggestion.vara.split()[0], suggestion.vara)
    return f"{rating}/१० | {vara} | {suggestion.recommended_mantra} × ११"


def format_hindi_medium(suggestion: DailySuggestion, chart: ChartData) -> str:
    """Medium Hindi format for Telegram/WhatsApp."""
    vara = _VARA_HI.get(suggestion.vara.split()[0], suggestion.vara)
    rating = _to_hindi_num(suggestion.day_rating)
    stars = "⭐" * suggestion.day_rating

    lines = [
        f"📅 {suggestion.date} — {vara}",
        f"दिन रेटिंग: {stars} ({rating}/१०)",
        "",
        f"🎨 रंग: {suggestion.recommended_color}",
        f"🙏 मन्त्र: {suggestion.recommended_mantra}",
        "",
    ]

    if suggestion.good_for:
        lines.append("✅ शुभ कार्य:")
        for item in suggestion.good_for[:3]:
            lines.append(f"  • {item}")

    if suggestion.avoid:
        lines.append("❌ अशुभ कार्य:")
        for item in suggestion.avoid[:2]:
            lines.append(f"  • {item}")

    lines.append(f"\n⏰ राहु काल: {suggestion.rahu_kaal}")
    lines.append(f"🌟 नक्षत्र: {suggestion.nakshatra}")
    lines.append(f"📿 तिथि: {suggestion.tithi}")

    if suggestion.health_focus:
        lines.append(f"💪 स्वास्थ्य: {suggestion.health_focus}")

    return "\n".join(lines)
