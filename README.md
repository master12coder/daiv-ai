# Vedic AI Framework

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)

**AI-powered Vedic astrology — Swiss Ephemeris precision + LLM interpretation**

Compute birth charts, detect yogas/doshas, calculate dashas, match compatibility, generate personalized PDF reports with visual charts — all offline, all free.

```
┌──────────────────────────────────────┐
│  apps/        CLI, Web, Telegram     │  Users interact here
│  (Layer 3)    Format + Deliver       │
└──────────────┬───────────────────────┘
               │ imports
┌──────────────▼───────────────────────┐
│  products/    7 Plugins + LLM Layer  │  AI interprets here
│  (Layer 2)    Interpret + Validate   │
└──────────────┬───────────────────────┘
               │ imports
┌──────────────▼───────────────────────┐
│  engine/      Compute + Knowledge    │  Math happens here
│  (Layer 1)    Swiss Ephemeris + YAML │
└──────────────────────────────────────┘

   engine/ → ZERO dependencies on products/ or apps/
   products/ → ZERO dependencies on apps/
```

## Features

- **Precise Chart Computation** — Swiss Ephemeris (NASA JPL DE431), Lahiri ayanamsha, 0.001° precision
- **157 Yoga Detection** — Panch Mahapurush, Raj, Dhan, Gajakesari, Vipreet, and more
- **4 Dasha Systems** — Vimshottari (MD/AD/PD), Yogini, Ashtottari, Chara
- **Full Shadbala** — Six-fold planetary strength with ratios
- **Ashtakavarga** — Bhinnashtakavarga + Sarvashtakavarga (337 bindus)
- **16 Divisional Charts** — D1 through D60 (all Shodashvarga)
- **Dosha Analysis** — Mangal, Kaal Sarp, Sadesati, Pitra with cancellation checks
- **Ashtakoot Matching** — 36-guna compatibility scoring
- **Jaimini + KP Systems** — Chara Karakas, Arudha Padas, KP sub-lords
- **10-Factor Gemstone Engine** — Personalized weight using chart-based factors
- **Visual PDF Reports** — 14-section kundali with diamond charts, dasha Gantt, heatmaps
- **LLM Interpretation** — Ollama (free/local), Groq (free), Claude, OpenAI
- **Pandit Ji Learning** — Record corrections, validate, inject rules into prompts
- **Hindi + English** — Bilingual output with Devanagari, NotoSansDevanagari font bundled

## Quick Start

```bash
# Clone and install
git clone https://github.com/master12coder/vedic-ai-framework.git
cd vedic-ai-framework
uv sync                   # or: pip install -e engine/ -e products/ -e apps/

# Compute a birth chart
jyotish chart --name "Manish" --dob "13/03/1989" --tob "12:17" --place "Varanasi" --gender Male

# Generate visual PDF kundali (14 pages)
jyotish kundali --name "Manish" --dob "13/03/1989" --tob "12:17" --place "Varanasi" \
  --gender Male --weight 78 --format detailed -o kundali.pdf

# Daily guidance
jyotish daily --name "Manish" --dob "13/03/1989" --tob "12:17" --place "Varanasi"

# Gemstone weight analysis
jyotish gemstone --name "Manish" --dob "13/03/1989" --tob "12:17" --place "Varanasi" --weight 78
```

### Python Library

```python
from jyotish_engine.compute.chart import compute_chart
from jyotish_engine.compute.dasha import find_current_dasha
from jyotish_engine.compute.yoga import detect_all_yogas

chart = compute_chart(
    name="Manish", dob="13/03/1989", tob="12:17",
    lat=25.3176, lon=83.0067, tz_name="Asia/Kolkata", gender="Male",
)

print(f"Lagna: {chart.lagna_sign} ({chart.lagna_sign_en})")
print(f"Moon: {chart.planets['Moon'].nakshatra}, Pada {chart.planets['Moon'].pada}")

md, ad, pd = find_current_dasha(chart)
print(f"Current Dasha: {md.lord} > {ad.lord} > {pd.lord}")

for y in detect_all_yogas(chart):
    if y.is_present:
        print(f"  {y.name} ({y.name_hindi}): {y.description}")
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `jyotish chart` | Compute and display birth chart with yogas, doshas |
| `jyotish save` | Save chart as JSON for reuse |
| `jyotish report` | Full text report (18 sections), optional LLM interpretation |
| `jyotish kundali` | Visual PDF report (summary/detailed/pandit formats) |
| `jyotish daily` | Today's personalized guidance (rating, color, mantra) |
| `jyotish transit` | Current transits overlaid on natal chart |
| `jyotish muhurta` | Find auspicious dates for life events |
| `jyotish pooja` | Weekly personalized pooja plan |
| `jyotish gemstone` | 10-factor gemstone weight analysis |
| `jyotish events add` | Log a life event for prediction tracking |
| `jyotish dashboard` | Prediction accuracy stats |
| `jyotish family add` | Add a family member's chart |
| `jyotish family list` | List all family members |
| `jyotish family daily` | Daily guidance for entire family |
| `jyotish web` | Start the web dashboard |

## Architecture

```
vedic-ai-framework/
├── engine/src/jyotish_engine/     # Package 1: Pure computation (zero AI)
│   ├── compute/                   # 21 modules: chart, dasha, yoga, dosha, strength...
│   ├── models/                    # 20 Pydantic v2 models
│   ├── knowledge/                 # 11 YAML rule files (lordship, gemstones, yogas...)
│   ├── scriptures/                # 18 BPHS chapters + Lal Kitab (YAML)
│   ├── constants.py               # All magic numbers, one file
│   └── exceptions.py              # Error hierarchy, one file
│
├── products/src/jyotish_products/ # Package 2: AI + business logic
│   ├── interpret/                 # LLM layer: 5 backends, prompts, validator
│   ├── plugins/                   # 7 product plugins (isolated, no cross-imports)
│   │   ├── kundali/               # 14-section PDF with visual chart renderers
│   │   ├── daily/                 # 3-level daily guidance + Hindi mode
│   │   ├── remedies/              # Gemstone weight engine + recommendations
│   │   ├── matching/              # Ashtakoot 36-guna compatibility
│   │   ├── muhurta/               # Auspicious date finder
│   │   ├── predictions/           # Life event tracking + accuracy dashboard
│   │   └── pandit/                # Professional corrections + learning
│   └── store/                     # JSON + SQLite persistence
│
├── apps/src/jyotish_app/          # Package 3: Delivery (thin adapters)
│   ├── cli/                       # Click CLI (15+ commands)
│   ├── web/                       # FastAPI dashboard
│   └── telegram/                  # Bot + 5:30 AM scheduler
│
├── assets/fonts/                  # NotoSansDevanagari.ttf (bundled)
├── tests/                         # 530+ tests (pytest)
├── scripts/                       # Import boundary + safety audits
├── docs/                          # Architecture, product specs, design system
├── CLAUDE.md                      # Engineering rules (read first every session)
└── Makefile                       # make test | make lint | make audit | make all
```

## LLM Backends

| Backend | Cost | Speed | Quality | Setup |
|---------|------|-------|---------|-------|
| **Ollama** | Free | Medium | Good | `ollama pull qwen3:8b` |
| **Groq** | Free tier | Fast | Good | Set `GROQ_API_KEY` |
| **Claude** | Paid | Medium | Best | Set `ANTHROPIC_API_KEY` |
| **OpenAI** | Paid | Fast | Good | Set `OPENAI_API_KEY` |
| **None** | Free | Instant | N/A | Computation only, no interpretation |

## Development

```bash
make test       # pytest (530+ tests)
make lint       # ruff check + format
make typecheck  # mypy engine/src/ products/src/
make audit      # import boundaries + plugin contracts + safety audit
make all        # all of the above (run before every commit)
```

## License

AGPL-3.0 License — see [LICENSE](LICENSE)

## Author

Manish Chaurasia

---

*Built with Swiss Ephemeris precision and Parashari Jyotish tradition.*
