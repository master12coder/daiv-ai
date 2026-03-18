# Muhurta

> Auspicious date/time finder for life events

## Commands

| Command    | Handler        | Description            |
|------------|----------------|------------------------|
| `muhurta`  | `run_muhurta`  | Find auspicious dates  |
| `panchang` | `run_panchang` | Show today's panchang  |

## What It Does

The muhurta plugin helps users find auspicious dates and times for important
life events such as marriage, business launches, travel, and property
transactions. It searches a user-defined date range and returns ranked
candidates scored by multiple Vedic timing factors including nakshatra, tithi,
yoga, and Rahu Kaal.

The plugin also provides a panchang command for displaying the current day's
Hindu calendar information. The computational work is performed entirely by
`engine/compute/muhurta.py`, which evaluates each candidate date against
purpose-specific auspiciousness rules. The plugin handles date parsing,
parameter validation, and result formatting.

## Data Flow

```
User input (purpose, location, date range)
  -> apps/ CLI/Web/Telegram
    -> products/plugins/muhurta/engine.py
      -> engine/compute/muhurta.py   (find_muhurta algorithm)
      -> engine/models/muhurta.py    (MuhurtaCandidate)
  -> formatted list of auspicious dates
```

## Key Functions

- `find_dates(purpose, lat, lon, tz_name, from_date, to_date, max_results) -> str` -- Find auspicious dates and return formatted report.
- `format_candidates(candidates, purpose) -> str` -- Format MuhurtaCandidate list into text.

## Input / Output

**Input:** Event purpose (string), location (lat/lon/timezone), date range
(DD/MM/YYYY start and end), optional max results (default 5).

**Output:** Formatted text report listing ranked auspicious dates. Each entry
shows the date, day of week, score, nakshatra, tithi, yoga, Rahu Kaal timing,
and supporting reasons for the recommendation.

## Test Coverage

- `tests/products/plugins/muhurta/test_muhurta_plugin.py` -- date finding, formatting, edge cases
