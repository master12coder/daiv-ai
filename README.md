# Vedic AI Framework

**AI-powered Vedic astrology computation and interpretation engine**

A comprehensive Python framework for Vedic (Jyotish) astrology that combines Swiss Ephemeris precision with LLM-powered interpretation. Compute birth charts, detect yogas/doshas, calculate dashas, match compatibility, and generate personalized reports — all offline, all free.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    VEDIC AI FRAMEWORK                               │
│                                                                     │
│  ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐    │
│  │  COMPUTE   │──▶│ KNOWLEDGE │──▶│ INTERPRET  │──▶│  DELIVER   │   │
│  │           │   │           │   │           │   │           │    │
│  │Swiss Ephem│   │YAML Rules │   │LLM Engine │   │MD/JSON/PDF│    │
│  │Chart/Dasha│   │Lordships  │   │Ollama/Groq│   │Telegram   │    │
│  │Yoga/Dosha │   │Nakshatras │   │Claude/GPT │   │Reports    │    │
│  │Panchang   │   │Gemstones  │   │Prompts    │   │           │    │
│  └───────────┘   └───────────┘   └───────────┘   └───────────┘    │
│                         │                                           │
│                    ┌────┴────┐                                      │
│                    │  LEARN   │                                      │
│                    │Pandit Ji │                                      │
│                    │Corrections│                                     │
│                    │Audio→Text │                                     │
│                    └──────────┘                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Features

- **Precise Chart Computation** — Swiss Ephemeris (NASA JPL DE431) with Lahiri ayanamsha
- **30+ Yoga Detection** — Panch Mahapurush, Raj, Dhan, Gajakesari, and more
- **Vimshottari Dasha** — MD/AD/PD calculation with date ranges
- **Dosha Analysis** — Mangal, Kaal Sarp, Sadesati, Pitra dosha with cancellation checks
- **Ashtakoot Matching** — Full 36-guna compatibility scoring
- **Divisional Charts** — D9 Navamsha, D10 Dasamsha, D7, D12
- **Panchang** — Tithi, Nakshatra, Yoga, Karana, Vara, Rahu Kaal
- **Muhurta** — Auspicious date finder for marriage, business, travel, property
- **LLM Interpretation** — Ollama (free/local), Groq (free), Claude, OpenAI
- **Pandit Ji Learning** — Record corrections, validate, extract rules over time
- **Hindi + English** — Bilingual output with Devanagari script
- **Offline-First** — Core computation needs zero internet

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/vedic-ai-framework.git
cd vedic-ai-framework

# Install (basic — computation only, no LLM)
pip install -e ".[dev]"

# Install with Ollama support (free local LLM)
pip install -e ".[dev,ollama]"
```

### Compute a Birth Chart

```bash
# CLI
jyotish chart --name "Rajesh Kumar" --dob "15/08/1990" --tob "06:30" --place "Jaipur" --gender Male

# JSON output
jyotish chart --name "Rajesh Kumar" --dob "15/08/1990" --tob "06:30" --place "Jaipur" --format json
```

### Full Report with LLM Interpretation

```bash
# With Ollama (free, local)
jyotish report --name "Rajesh" --dob "15/08/1990" --tob "06:30" --place "Jaipur" --llm ollama

# Without LLM (computation only)
jyotish report --name "Rajesh" --dob "15/08/1990" --tob "06:30" --place "Jaipur" --llm none

# Save to file
jyotish report --name "Rajesh" --dob "15/08/1990" --tob "06:30" --place "Jaipur" --output report.md
```

### Python Library

```python
from jyotish.compute.chart import compute_chart
from jyotish.compute.dasha import find_current_dasha
from jyotish.compute.yoga import detect_all_yogas

# Compute chart
chart = compute_chart(
    name="Rajesh Kumar",
    dob="15/08/1990",
    tob="06:30",
    place="Jaipur",
    gender="Male",
)

print(f"Lagna: {chart.lagna_sign} ({chart.lagna_sign_en})")
print(f"Moon: {chart.planets['Moon'].nakshatra}, Pada {chart.planets['Moon'].pada}")

# Current dasha
md, ad, pd = find_current_dasha(chart)
print(f"Current: {md.lord}-{ad.lord}-{pd.lord}")

# Yogas
yogas = detect_all_yogas(chart)
for y in yogas:
    if y.is_present:
        print(f"  {y.name}: {y.description}")
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `jyotish chart` | Compute and display birth chart |
| `jyotish report` | Full report with LLM interpretation |
| `jyotish transit` | Current transits for a saved chart |
| `jyotish daily` | Daily suggestion based on transits |
| `jyotish match` | Ashtakoot (36 guna) compatibility matching |
| `jyotish muhurta` | Find auspicious dates |
| `jyotish panchang` | Panchang for any date and place |
| `jyotish correct` | Add a Pandit Ji correction |
| `jyotish learn-audio` | Process Pandit Ji audio recording |
| `jyotish rules` | Show learned rules |
| `jyotish export` | Export chart as JSON or Markdown |

## Architecture

```
vedic-ai-framework/
├── jyotish/
│   ├── compute/          # Layer 1: Deterministic computation
│   │   ├── chart.py      # Swiss Ephemeris chart engine
│   │   ├── dasha.py      # Vimshottari Dasha (MD/AD/PD)
│   │   ├── divisional.py # D1, D9, D10, D7, D12
│   │   ├── yoga.py       # 30+ yoga detection
│   │   ├── dosha.py      # Mangal, Kaal Sarp, Sadesati, Pitra
│   │   ├── panchang.py   # Tithi, Nakshatra, Yoga, Karana
│   │   ├── matching.py   # Ashtakoot 36-guna matching
│   │   ├── transit.py    # Transit overlay on natal chart
│   │   ├── muhurta.py    # Auspicious timing finder
│   │   └── strength.py   # Shadbala (basic)
│   ├── knowledge/        # Layer 2: YAML knowledge files
│   │   ├── lordship_rules.yaml    # 12 lagnas, complete data
│   │   ├── yoga_definitions.yaml  # 30+ yogas
│   │   ├── nakshatra_data.yaml    # 27 nakshatras
│   │   ├── gemstone_logic.yaml    # 9 gemstones + contraindications
│   │   └── ...
│   ├── interpret/        # Layer 3: LLM interpretation
│   │   ├── llm_backend.py         # Ollama/Groq/Claude/OpenAI
│   │   ├── interpreter.py         # Orchestrator
│   │   └── prompts/               # Jinja2 prompt templates
│   ├── learn/            # Layer 4: Pandit Ji learning
│   │   ├── corrections.py         # Correction store
│   │   ├── validator.py           # Multi-source validation
│   │   └── audio_processor.py     # Whisper transcription
│   └── deliver/          # Layer 5: Output delivery
│       ├── markdown_report.py
│       ├── json_export.py
│       └── pdf_report.py
├── tests/                # pytest test suite
├── examples/             # Sample inputs and outputs
└── config.yaml           # All configuration
```

## LLM Backends

| Backend | Cost | Speed | Quality | Setup |
|---------|------|-------|---------|-------|
| **Ollama** (default) | Free | Medium | Good | `ollama pull qwen3:8b` |
| **Groq** | Free tier | Fast | Good | Set `GROQ_API_KEY` |
| **Claude** | Paid | Medium | Best | Set `ANTHROPIC_API_KEY` |
| **OpenAI** | Paid | Fast | Good | Set `OPENAI_API_KEY` |
| **None** | Free | Instant | N/A | No LLM, raw data only |

## Knowledge Files

All astrological rules are stored as human-readable YAML:

- **lordship_rules.yaml** — Complete data for all 12 lagnas (yogakaraka, benefics, malefics, marakas, gemstones)
- **yoga_definitions.yaml** — 30+ yogas with formation conditions, cancellation, and effects
- **nakshatra_data.yaml** — 27 nakshatras with deity, gana, animal, psychological profile
- **gemstone_logic.yaml** — 9 gemstones with contraindications and wearing vidhan
- **remedy_rules.yaml** — Mantras, daan, behavioral remedies per planet
- **weekly_routine.yaml** — Day-planet-color-food-temple mapping

## Pandit Ji Learning System

The unique learning system captures a Pandit Ji's wisdom over time:

1. **Record** — After each consultation, log corrections via CLI or audio
2. **Validate** — Cross-check with second opinions, life events, or computation
3. **Learn** — Validated corrections become rules injected into future prompts
4. **Improve** — Each session makes the system smarter for that specific lagna + planet combination

```bash
# Add a correction
jyotish correct --chart-name "Rajesh" --category gemstone \
  --ai-said "Wear pukhraj" --pandit-said "Avoid pukhraj, it's maraka for Mithuna"

# Process audio recording
jyotish learn-audio --file panditji_session.mp3 --chart-name "Rajesh"

# View learned rules
jyotish rules --lagna Mithuna
```

## Running Tests

```bash
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest tests/test_chart.py  # Single file
pytest --cov=jyotish      # With coverage
```

## Configuration

All settings in `config.yaml`:

```yaml
ayanamsha: lahiri          # Lahiri/Raman/KP
house_system: whole_sign   # Whole sign houses
llm:
  default_backend: ollama  # Default LLM
  ollama:
    model: qwen3:8b        # Model for interpretation
```

## Contributing

1. Fork the repository
2. Add YAML knowledge (new yogas, regional remedies, Lal Kitab rules)
3. Submit a PR

The YAML knowledge files are designed to grow through community contributions.

## License

MIT License — see [LICENSE](LICENSE)

## Author

Manish Chaurasia

---

*Built with Swiss Ephemeris precision and Parashari Jyotish tradition.*
