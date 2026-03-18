# Daily

> Personalized daily guidance based on chart + transits -- 3 levels

## Commands

| Command | Handler     | Description                      |
|---------|-------------|----------------------------------|
| `daily` | `run_daily` | Get today's personalized guidance |

## What It Does

The daily plugin delivers personalized day-ahead guidance by combining a
native's birth chart with current planetary transits. It computes a day rating
(1-10), recommended color, mantra, Rahu Kaal timing, health focus, and
categorized good-for/avoid lists.

Output is available at three detail levels. **Simple** is a single line ideal
for notifications: rating, color, mantra, and Rahu Kaal. **Medium** is a 5-7
line format designed for WhatsApp or Telegram messages with icons and
categories. **Detailed** is a full transit analysis report including per-planet
transit impacts with Ashtakavarga bindus, nakshatra, tithi, and current dasha
context.

The plugin delegates all astronomical computation to `engine/compute/daily.py`,
which returns a `DailySuggestion` model. The plugin's engine module handles
formatting only.

## Data Flow

```
User requests daily guidance
  -> apps/ CLI/Web/Telegram
    -> products/plugins/daily/engine.py
      -> engine/compute/daily.py  (transit computation, DailySuggestion)
      -> engine/compute/dasha.py  (current dasha context, detailed level)
  -> formatted text (simple / medium / detailed)
```

## Key Functions

- `run_daily(chart, level) -> str` -- Generate daily guidance at the specified level.
- `format_simple(suggestion) -> str` -- One-line format: rating, color, mantra, Rahu Kaal.
- `format_medium(suggestion, chart) -> str` -- 5-7 line format for messaging apps.
- `format_detailed(suggestion, chart) -> str` -- Full transit analysis report.

## Input / Output

**Input:** `ChartData` (computed birth chart), `DailyLevel` enum (simple/medium/detailed).

**Output:** Formatted text string. Simple level returns one line; medium returns
5-7 lines; detailed returns a multi-section report with transit impacts, good/avoid
lists, Rahu Kaal, health focus, and dasha context.

## Test Coverage

- `tests/products/plugins/daily/test_daily_plugin.py` -- all three format levels, edge cases
