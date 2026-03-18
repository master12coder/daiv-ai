# Predictions

> Prediction tracking, accuracy dashboard, and life event logging

## Commands

| Command     | Handler         | Description                     |
|-------------|-----------------|----------------------------------|
| `events`    | `run_events`    | Life event tracking              |
| `dashboard` | `run_dashboard` | Prediction accuracy dashboard    |

## What It Does

The predictions plugin provides a feedback loop for the framework by tracking
predictions and measuring their accuracy over time. Every prediction is logged
with a category (career, health, marriage, finance, education), a confidence
score, and the dasha lord active at the time. Outcomes are recorded as
confirmed, not_occurred, opposite, or pending.

The accuracy dashboard aggregates results by category, showing per-category
accuracy percentages (confirmed vs. total decided) alongside overall accuracy
and pending counts. This data feeds back into the framework's self-improvement
cycle and gives users transparency into how well the system's interpretations
match real-life outcomes. The plugin stores data in a SQLite database via
`products/store/predictions.py`.

## Data Flow

```
User logs events or views dashboard
  -> apps/ CLI/Web/Telegram
    -> products/plugins/predictions/engine.py
      -> products/store/predictions.py  (PredictionTracker, SQLite)
  -> formatted dashboard or confirmation
```

## Key Functions

- `get_dashboard_stats(db_path) -> dict[str, Any]` -- Retrieve accuracy statistics from the prediction tracker database.
- `format_dashboard(stats) -> str` -- Format dashboard stats into a human-readable report.

## Models (Store Layer)

- `Prediction` -- A prediction record with id, chart_id, prediction_date, category, prediction text, confidence, dasha_lord, outcome, outcome_date, and notes.
- `PredictionTracker` -- SQLite-backed store with methods for adding predictions, recording outcomes, and computing accuracy dashboards.

## Input / Output

**Input:** Optional `db_path` for the SQLite database (defaults to `data/life_events.db`).

**Output:** Dashboard text report showing total predictions, pending count,
overall accuracy percentage, and per-category breakdown (accuracy, confirmed
count, total decided count).

## Test Coverage

- `tests/products/plugins/predictions/test_predictions_plugin.py` -- dashboard stats, formatting, empty database handling
