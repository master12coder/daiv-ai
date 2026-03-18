# Remedies

> Gemstone recommendations, multi-factor weight engine, weekly pooja plan, Lal Kitab remedies

## Commands

| Command    | Handler        | Description                                  |
|------------|----------------|----------------------------------------------|
| `remedies` | `run_remedies` | Get personalized remedy recommendations      |
| `gemstone` | `run_gemstone` | Compute gemstone weight with 10 chart factors |
| `pooja`    | `run_pooja`    | Generate weekly pooja plan                   |

## What It Does

The remedies plugin provides three services: gemstone recommendations with
safety validation, a multi-factor gemstone weight engine, and weekly pooja
plans. The gemstone recommendation engine classifies all 9 planetary stones
into RECOMMENDED, TEST WITH CAUTION, and PROHIBITED categories based on
lagna-specific lordship rules loaded from `engine/knowledge/lordship_rules.yaml`.
MARAKA planets (2nd/7th lords) are always flagged with dual-nature warnings.

The gemstone weight engine computes personalized ratti (carat) recommendations
using 10 chart-based factors: body weight, avastha (planetary age), Ashtakavarga
bindus, dignity, combustion, retrograde status, current dasha period, lordship
quality, stone energy density, and purpose (protection/growth/maximum). Results
include website comparisons, light/medium/heavy pros-cons, and free alternatives
(mantra, daan, color therapy) for every stone including prohibited ones. A
dedicated formatter produces detailed text reports with factor breakdown tables.

## Data Flow

```
User input (chart + optional body weight)
  -> apps/ CLI/Web/Telegram
    -> products/plugins/remedies/engine.py     (recommendations)
    -> products/plugins/remedies/gemstone.py   (weight computation)
    -> products/plugins/remedies/formatter.py  (text report)
      -> products/interpret/context.py         (lordship rules)
      -> engine/compute/ashtakavarga.py        (bindus for weight factors)
      -> engine/compute/dasha.py               (current dasha for weight factors)
  -> formatted text report
```

## Key Functions

- `engine.get_gemstone_recommendations(chart) -> str` -- Lagna-based gemstone recommendations with safety checks.
- `gemstone.compute_gemstone_weights(chart, body_weight_kg, purpose) -> list[GemstoneWeightResult]` -- 10-factor weight computation for all 9 stones.
- `formatter.format_gemstone_report(results, body_weight_kg, lagna_sign, name) -> str` -- Full text report with factor tables, website comparisons, and alternatives.

## Models

- `WeightFactor` -- One factor (name, raw_value, multiplier, explanation).
- `GemstoneWeightResult` -- Full recommendation for one stone (status, base/recommended ratti, factors, website comparisons, pros/cons, free alternatives).

## Input / Output

**Input:** `ChartData` (birth chart), optional `body_weight_kg` (float), optional `purpose` (protection/growth/maximum).

**Output:** Formatted text report. Gemstone weight results include per-stone
factor breakdowns, website comparison tables (GemPundit, BrahmaGems, etc.),
light/medium/heavy weight options with pros/cons, and free alternatives
(mantra count, daan, color therapy).

## Safety Rules

- All gemstone classifications come exclusively from `engine/knowledge/lordship_rules.yaml`.
- Prohibited stones always show the prohibition reason and free alternatives.
- MARAKA planets flagged with "dual-nature: acknowledge both positive and negative effects".
- Report footer includes Shastra disclaimer: no classical text prescribes exact gemstone weight.
- "Discuss with your Pandit Ji" section with 5 consultation questions.

## Test Coverage

- `tests/products/plugins/remedies/test_remedies_plugin.py` -- recommendation engine, safety checks
- `tests/products/plugins/remedies/test_gemstone_weight.py` -- 10-factor weight computation, prohibited stone handling
