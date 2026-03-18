# Pandit

> Professional tools -- corrections, trust scoring, comparison reports

## Commands

| Command   | Handler       | Description                  |
|-----------|---------------|------------------------------|
| `correct` | `run_correct` | Add a Pandit Ji correction   |
| `rules`   | `run_rules`   | Show learned rules           |

## What It Does

The pandit plugin enables professional astrologers (Pandit Ji) to submit
corrections when the AI interpretation diverges from their expert judgment.
Each correction records the chart name, category (gemstone, house_reading,
dasha, remedy, yoga, dosha), what the pandit says, and their reasoning. This
creates a structured feedback mechanism where human expertise refines the
system over time.

Corrections are persisted as individual JSON files via
`products/store/corrections.py` and tracked through a lifecycle: pending,
validated, disputed, learned, or rejected. The plugin supports listing
corrections with filters by status and category. Each correction can optionally
include planets involved, houses involved, lagna, correction type
(override/refinement/addition), audio file path, and transcript for
voice-based corrections.

## Data Flow

```
Pandit Ji submits correction
  -> apps/ CLI/Web/Telegram
    -> products/plugins/pandit/engine.py
      -> products/store/corrections.py  (PanditCorrectionStore, JSON files)
  -> confirmation with correction ID

Pandit Ji reviews rules
  -> products/plugins/pandit/engine.py
    -> products/store/corrections.py  (list with status/category filters)
  -> formatted corrections list
```

## Key Functions

- `add_correction(chart_name, category, what, reasoning, data_dir) -> str` -- Add a new pandit correction; returns confirmation with correction ID.
- `list_corrections(data_dir, status, category) -> str` -- List corrections with optional status and category filters.

## Models (Store Layer)

- `PanditCorrection` -- A correction record with id, pandit_name, date, chart_name, category, ai_said, pandit_said, pandit_reasoning, correction_type, planets_involved, houses_involved, lagna, status, confidence, audio_file, and transcript.
- `PanditCorrectionStore` -- File-based JSON store with add, get, list, and filter operations.

## Input / Output

**Input:** Chart name (string), category (string), correction content (string),
reasoning (string), optional data directory path.

**Output:** For `correct`: confirmation string with the correction ID. For
`rules`: formatted list of corrections showing ID, category, chart name,
status, and a truncated summary of what the pandit said.

## Test Coverage

- `tests/products/plugins/pandit/test_pandit_plugin.py` -- correction lifecycle, listing, filtering
