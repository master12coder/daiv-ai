# Matching

> Ashtakoot 36-guna compatibility matching between two charts

## Commands

| Command | Handler     | Description                              |
|---------|-------------|------------------------------------------|
| `match` | `run_match` | Compatibility matching between two charts |

## What It Does

The matching plugin computes Ashtakoot (36-guna) compatibility between two
birth charts. This is the traditional Vedic method for evaluating marriage
compatibility, scoring 8 kootas (matching dimensions) for a maximum of 36
points. Each koota has a Hindi name, an obtained score, a maximum score, and a
textual description of the match quality.

The plugin is a thin wrapper around `engine/compute/matching.py`. It extracts
Moon nakshatra and sign indices from both charts, delegates to the engine's
`compute_ashtakoot` function, and formats the result into a human-readable
report with per-koota breakdown, total score, percentage, and a final
recommendation.

## Data Flow

```
User provides two birth details
  -> apps/ CLI/Web/Telegram
    -> products/plugins/matching/engine.py
      -> engine/compute/matching.py  (Ashtakoot algorithm)
      -> engine/models/matching.py   (MatchingResult, KootaScore)
  -> formatted compatibility report
```

## Key Functions

- `run_match(chart1, chart2) -> str` -- Run matching and return formatted report.
- `compute_match(chart1, chart2) -> MatchingResult` -- Compute raw Ashtakoot result.
- `format_result(result, name1, name2) -> str` -- Format MatchingResult into text.

## Input / Output

**Input:** Two `ChartData` objects (one per person). Moon data (nakshatra index,
sign index) must be present in both charts.

**Output:** Formatted text report listing all 8 kootas with Hindi names,
obtained/max scores, descriptions, total score out of 36, percentage, and a
recommendation string (e.g., "Highly Recommended", "Recommended with Remedies").

## Test Coverage

- `tests/products/plugins/matching/test_matching_plugin.py` -- koota scoring, edge cases, formatted output
