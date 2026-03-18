# Kundali

> Full birth chart report with 18 sections, North Indian diamond chart, and PDF export

## Commands

| Command  | Handler           | Description                          |
|----------|-------------------|--------------------------------------|
| `chart`  | `show_chart`      | Compute and display birth chart      |
| `report` | `generate_report` | Generate full interpretation report  |
| `save`   | `save_chart`      | Save chart for later reuse           |

## What It Does

The kundali plugin is the core product of the framework. It computes a full
Vedic birth chart and produces an 18-section report covering planetary
positions, house lords, yogas, doshas, Vimshottari Mahadasha timeline, current
dasha period, Ashtakavarga, and gemstone recommendations. Interpretation
sections (personality, career, finances, relationships, health, spirituality)
are available when an LLM backend is enabled.

The plugin renders a North Indian diamond-style chart in both text and visual
(PNG) formats. The PDF pipeline supports three formats: **summary** (2 pages),
**detailed** (12-15 pages with D9 Navamsha, graha table, dasha Gantt,
Ashtakavarga heatmap, Shadbala chart, and golden period analysis), and
**pandit** (adds D10 Dasamsha for professional use). All PDFs use a Sanatan
Dharma aesthetic with Hindi/Sanskrit headings via ReportLab.

## Data Flow

```
User input (name, DOB, TOB, place)
  -> apps/ CLI/Web/Telegram
    -> products/plugins/kundali/report.py  (18-section orchestrator)
    -> products/plugins/kundali/pdf.py     (PDF assembler)
      -> engine/compute/chart.py           (planetary positions)
      -> engine/compute/yoga.py            (yoga detection)
      -> engine/compute/dosha.py           (dosha detection)
      -> engine/compute/dasha.py           (Vimshottari dashas)
      -> engine/compute/ashtakavarga.py    (Sarva/Bhinna ashtakavarga)
      -> engine/compute/strength.py        (Shadbala)
      -> engine/compute/divisional.py      (Navamsha, Dasamsha)
  -> formatted text or PDF bytes
```

## Key Functions

- `report.generate_report(chart, sections, llm_backend) -> str` -- Build all 18 sections as formatted text.
- `pdf.generate_pdf(chart, output_path, fmt, body_weight_kg, chart_image_bytes) -> bytes | None` -- Assemble a complete PDF in summary/detailed/pandit format.

## Input / Output

**Input:** `ChartData` (computed birth chart with planetary positions, lagna, nakshatras).

**Output:** Formatted text report (18 sections) or PDF bytes/file. PDF includes
visual charts (D1, D9, D10), graha tables, dasha Gantt, Ashtakavarga heatmap,
Shadbala bar chart, yoga cards, gemstone cards, and an accuracy certificate.

## Safety Rules

- Gemstone section uses `build_lordship_context()` from `products/interpret/context.py`, sourced exclusively from `engine/knowledge/lordship_rules.yaml`.
- Prohibited stones are always listed with the prohibition reason.
- MARAKA planets (2nd/7th lords) are flagged with dual-nature warnings.

## Test Coverage

- `tests/products/plugins/kundali/test_kundali_plugin.py` -- report generation, section rendering
- `tests/products/plugins/kundali/test_pdf_assembler.py` -- PDF pipeline
- `tests/products/plugins/kundali/test_diamond_chart.py` -- D1 diamond chart rendering
- `tests/products/plugins/kundali/test_divisional_chart.py` -- D9/D10 charts
- `tests/products/plugins/kundali/test_graha_table.py` -- graha table rendering
- `tests/products/plugins/kundali/test_dasha_gantt.py` -- dasha Gantt chart
- `tests/products/plugins/kundali/test_ashtakavarga_heatmap.py` -- Ashtakavarga heatmap
- `tests/products/plugins/kundali/test_shadbala_chart.py` -- Shadbala bar chart
- `tests/products/plugins/kundali/test_yoga_cards.py` -- yoga card rendering
- `tests/products/plugins/kundali/test_gemstone_card.py` -- gemstone card rendering
- `tests/products/plugins/kundali/test_remaining_renderers.py` -- golden period, accuracy cert, prohibited stones
