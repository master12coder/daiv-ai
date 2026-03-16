# VEDIC AI FRAMEWORK — COMPLETE BUILD SPECIFICATION
# Feed this entire file to Claude Code to build the project autonomously.
#
# USAGE:
#   1. Create empty folder: mkdir vedic-ai-framework && cd vedic-ai-framework
#   2. Save this file as BUILD_SPEC.md in that folder
#   3. Run: claude
#   4. Paste: "Read BUILD_SPEC.md and build the entire project following every instruction exactly. Work autonomously. Create all files, install all dependencies, run tests to verify. Do not skip any section."
#   5. Go to sleep. Wake up to a working project.

---

## PROJECT IDENTITY

Name: vedic-ai-framework
Description: AI-powered Vedic astrology computation and interpretation engine
Language: Python 3.11+
License: MIT
Author: Manish Chaurasia
GitHub: https://github.com/[USERNAME]/vedic-ai-framework

---

## ARCHITECTURE PRINCIPLES

1. SEPARATION OF CONCERNS: Compute (deterministic math) | Knowledge (YAML rules) | Interpret (LLM) | Learn (corrections) | Deliver (output)
2. LLM-AGNOSTIC: Default = Ollama (free, local). Also supports Groq (free), Claude API, OpenAI. Switch with one flag.
3. OFFLINE-FIRST: Core computation needs zero internet. LLM can run locally via Ollama.
4. NO BOILERPLATE: Every file has a clear purpose. No empty __init__.py files with no content. No unnecessary abstractions.
5. EASILY UPGRADABLE: Swap LLM models, add new YAML rules, add new prompt templates — all without touching core code.
6. HINDI + ENGLISH: All user-facing output supports both languages. Internal code/comments in English.
7. CONFIGURATION OVER CODE: All tunable parameters in config.yaml. No hardcoded values scattered in code.
8. TYPE HINTS EVERYWHERE: Full Python type hints. Use dataclasses for all data structures.
9. TESTABLE: Every compute function has unit tests. Run with pytest.
10. CLI-FIRST: Main interface is CLI. Can also be imported as Python library.

---

## DIRECTORY STRUCTURE (Create exactly this)

```
vedic-ai-framework/
├── CLAUDE.md                      # Claude Code project instructions
├── README.md                      # GitHub landing page (comprehensive, with architecture diagram)
├── SYSTEM_DESIGN.md               # Full system design document
├── LICENSE                        # MIT License
├── pyproject.toml                 # Modern Python packaging (NOT setup.py)
├── config.yaml                    # All configuration in one place
├── .gitignore
│
├── jyotish/                       # Main package
│   ├── __init__.py                # Package init with version
│   ├── cli.py                     # CLI entry point (click-based)
│   ├── config.py                  # Config loader
│   │
│   ├── compute/                   # LAYER 1: Deterministic computation
│   │   ├── __init__.py
│   │   ├── chart.py               # Main chart computation (Swiss Ephemeris)
│   │   ├── dasha.py               # Vimshottari Dasha calculator (MD/AD/PD)
│   │   ├── divisional.py          # D1, D9 Navamsha, D10 Dasamsha, D7, D12
│   │   ├── yoga.py                # 30+ yoga detection engine
│   │   ├── dosha.py               # Mangal, Kaal Sarp, Sadesati, Pitra dosha
│   │   ├── panchang.py            # Tithi, Nakshatra, Yoga, Karana, Vara
│   │   ├── matching.py            # Ashtakoot (36 guna) matching
│   │   ├── transit.py             # Current/future transit computation
│   │   ├── strength.py            # Shadbala, Ashtakavarga (basic)
│   │   └── muhurta.py             # Muhurta/auspicious timing finder
│   │
│   ├── knowledge/                 # LAYER 2: Structured Jyotish rules
│   │   ├── lordship_rules.yaml    # Per-lagna benefic/malefic/yogakaraka/maraka
│   │   ├── yoga_definitions.yaml  # 30+ yogas with conditions and effects
│   │   ├── gemstone_logic.yaml    # Stone-planet-finger-metal + contraindications
│   │   ├── remedy_rules.yaml      # Mantra, daan, behavioral remedies per planet
│   │   ├── nakshatra_data.yaml    # 27 nakshatras: lords, deity, nature, gana, animal
│   │   ├── combustion.yaml        # Combustion limits per planet (normal + retrograde)
│   │   ├── aspects.yaml           # Special aspect rules (Saturn 3/7/10, Jupiter 5/7/9, Mars 4/7/8)
│   │   ├── dignity.yaml           # Exaltation, debilitation, own sign, mooltrikona per planet
│   │   ├── direction_mapping.yaml # House to compass direction mapping
│   │   └── weekly_routine.yaml    # Day-planet-color-food-temple mapping
│   │
│   ├── interpret/                 # LAYER 3: LLM interpretation
│   │   ├── __init__.py
│   │   ├── llm_backend.py         # LLM abstraction factory (Ollama/Groq/Claude/OpenAI)
│   │   ├── interpreter.py         # Main interpretation orchestrator
│   │   ├── formatter.py           # Output formatting (markdown, JSON, terminal)
│   │   └── prompts/               # Modular prompt templates
│   │       ├── system_prompt.md           # Master system identity
│   │       ├── chart_overview.md          # Lagna analysis, strongest/weakest planet
│   │       ├── career_analysis.md         # 10th house, career timeline
│   │       ├── financial_analysis.md      # 2nd/11th house, dhan yoga
│   │       ├── health_analysis.md         # 6th house, planet-body mapping
│   │       ├── relationship_analysis.md   # 7th house, marriage, children
│   │       ├── spiritual_profile.md       # Moon nakshatra, psychological profile
│   │       ├── life_event_validation.md   # Match events to dashas
│   │       ├── remedy_generation.md       # Gemstones, mantras, weekly routine
│   │       ├── timeline_summary.md        # 10-year forecast, monthly breakdown
│   │       └── daily_suggestion.md        # Today's transit-based advice
│   │
│   ├── learn/                     # LAYER 4: Pandit Ji learning system
│   │   ├── __init__.py
│   │   ├── corrections.py         # Correction store (JSON-based)
│   │   ├── validator.py           # Multi-source validation logic
│   │   ├── rule_extractor.py      # Extract learned rules from validated corrections
│   │   └── audio_processor.py     # Whisper integration for Hindi audio transcription
│   │
│   ├── deliver/                   # LAYER 5: Output delivery
│   │   ├── __init__.py
│   │   ├── pdf_report.py          # PDF generation (reportlab or weasyprint)
│   │   ├── markdown_report.py     # Markdown report generation
│   │   ├── json_export.py         # JSON export for integrations
│   │   └── telegram_bot.py        # Telegram bot (optional, needs python-telegram-bot)
│   │
│   └── utils/                     # Shared utilities
│       ├── __init__.py
│       ├── geo.py                 # Place name → lat/lon/timezone resolution
│       ├── datetime_utils.py      # IST conversion, Julian Day helpers
│       └── constants.py           # All astrological constants in one place
│
├── data/                          # Runtime data (gitignored except examples)
│   ├── pandit_corrections/        # Pandit Ji corrections (JSON files)
│   │   └── .gitkeep
│   └── charts/                    # Saved chart computations
│       └── .gitkeep
│
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── conftest.py                # Shared fixtures
│   ├── test_chart.py              # Test chart computation against known values
│   ├── test_dasha.py              # Test dasha calculation
│   ├── test_yoga.py               # Test yoga detection
│   ├── test_dosha.py              # Test dosha checks
│   ├── test_matching.py           # Test Ashtakoot matching
│   ├── test_panchang.py           # Test panchang computation
│   ├── test_llm_backend.py        # Test LLM backend factory
│   └── test_corrections.py        # Test Pandit Ji correction system
│
├── examples/                      # Example inputs and outputs
│   ├── sample_input.json          # Example birth details input
│   ├── sample_events.json         # Example life events for validation
│   ├── sample_chart_output.json   # What computation produces
│   ├── sample_report_hindi.md     # Example Hindi report
│   ├── sample_report_technical.md # Example technical report
│   └── sample_correction.json     # Example Pandit Ji correction
│
└── scripts/                       # Utility scripts
    ├── setup_ollama.sh            # One-command Ollama setup
    ├── test_chart.py              # Quick chart test script
    └── daily_transit.py           # Standalone daily transit script
```

---

## CONFIGURATION (config.yaml)

Create config.yaml with these contents:

```yaml
# Vedic AI Framework Configuration
# All tunable parameters in one place

# Ayanamsha setting
ayanamsha: lahiri  # Options: lahiri, raman, krishnamurti, yukteshwar

# House system
house_system: whole_sign  # Options: whole_sign, placidus, equal

# Default LLM backend
llm:
  default_backend: ollama  # Options: ollama, groq, claude, openai, none
  ollama:
    model: qwen3:8b  # Best for Hindi+English. Alternatives: llama3.1:8b, mistral:7b
    base_url: http://localhost:11434
  groq:
    model: llama-3.1-8b-instant
    # api_key: set via GROQ_API_KEY env var
  claude:
    model: claude-sonnet-4-20250514
    # api_key: set via ANTHROPIC_API_KEY env var
  openai:
    model: gpt-4o
    # api_key: set via OPENAI_API_KEY env var

# Default timezone for India
default_timezone_offset: 5.5

# Output preferences
output:
  language: both  # Options: hindi, english, both
  format: markdown  # Options: markdown, json, pdf, terminal

# Pandit Ji learning system
learning:
  data_dir: data/pandit_corrections
  min_confidence_for_rule: 0.5
  max_rules_in_prompt: 5

# Daily suggestions
daily:
  enabled: false
  notification_time: "07:00"  # IST
  telegram_bot_token: ""  # Set if using Telegram delivery
  telegram_chat_id: ""

# Chart computation
compute:
  include_outer_planets: false  # Uranus/Neptune/Pluto (not used in Vedic)
  true_node: true  # true = True Node (Rahu), false = Mean Node
  compute_upagrahas: false  # Gulika, Mandi etc. (advanced, future feature)
```

---

## CORE COMPUTATION REQUIREMENTS

### compute/chart.py — Main Chart Engine

This is the heart of the system. Must compute:

1. LAGNA (Ascendant): Sidereal longitude using Lahiri ayanamsha, Whole Sign houses
2. ALL 9 GRAHAS: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu (True Node), Ketu
   - For each: sidereal longitude, sign (0-11), degree in sign, nakshatra (0-26), pada (1-4), nakshatra lord, house number (1-12 from lagna), retrograde status, speed, dignity (exalted/debilitated/own/mooltrikona/neutral), avastha (Bala/Kumara/Yuva/Vriddha/Mruta), combustion check
3. Use pyswisseph library. Set Lahiri ayanamsha via swe.set_sid_mode(swe.SIDM_LAHIRI)
4. All positions must be sidereal (tropical - ayanamsha)

Coordinate lookup for birth place:
- Use geopy.geocoders.Nominatim for place → lat/lon
- Use timezonefinder for place → timezone
- Cache results to avoid repeated API calls

### compute/dasha.py — Vimshottari Dasha

Calculate from Moon's nakshatra at birth:
- Dasha sequence: Ketu(7), Venus(20), Sun(6), Moon(10), Mars(7), Rahu(18), Jupiter(16), Saturn(19), Mercury(17) = 120 years
- Calculate balance of first dasha from Moon's position within nakshatra
- Nested: Mahadasha → Antardasha → Pratyantardasha (3 levels)
- Function to find current MD/AD/PD for any given date
- Return as list of DashaPeriod dataclasses with start/end datetime

### compute/divisional.py — Divisional Charts

Implement at minimum:
- D1 (Rasi) — the main chart (already in chart.py)
- D9 (Navamsha) — marriage/dharma. 30° ÷ 9 = 3.333° per division
  - Fire signs (0,4,8) start from Aries
  - Earth signs (1,5,9) start from Capricorn
  - Air signs (2,6,10) start from Libra
  - Water signs (3,7,11) start from Cancer
- D10 (Dasamsha) — career. 30° ÷ 10 = 3° per division
  - Odd signs count from same sign
  - Even signs count from 9th sign
- Check Vargottam: planet in same sign in both D1 and D9

### compute/yoga.py — Yoga Detection

Detect these yogas (minimum 25):

PANCH MAHAPURUSH YOGAS (5):
- Hamsa (Jupiter in own/exalted in kendra)
- Malavya (Venus in own/exalted in kendra)
- Sasa (Saturn in own/exalted in kendra)
- Ruchaka (Mars in own/exalted in kendra)
- Bhadra (Mercury in own/exalted in kendra)

RAJ YOGAS:
- Trikona lord conjunct kendra lord
- Yogakaraka planet (owns both kendra + trikona) in strong position
- 9th lord + 10th lord conjunction/mutual aspect

DHAN YOGAS:
- 2nd lord + 11th lord conjunction
- 5th lord + 9th lord conjunction
- Jupiter in 2nd or 11th in good dignity

OTHER IMPORTANT YOGAS:
- Gajakesari (Jupiter in kendra from Moon)
- Budhaditya (Sun-Mercury conjunction)
- Chandra-Mangal (Moon-Mars conjunction)
- Vipreet Raj Yoga (6th/8th/12th lord in another dusthana)
- Neech Bhanga Raj Yoga (debilitated planet with cancellation)
- Kemdrum (no planet in 2nd/12th from Moon)
- Saraswati (Jupiter/Venus/Mercury in kendra/trikona)
- Amala Yoga (benefic in 10th from lagna or Moon)
- Adhi Yoga (benefics in 6th/7th/8th from Moon)
- Lakshmi Yoga (9th lord in own/exalted in kendra)
- Dharma Karmadhipati (9th lord + 10th lord connected)

Each yoga returns: name, name_hindi, is_present, planets_involved, houses_involved, description, effect (benefic/malefic/mixed)

### compute/dosha.py — Dosha Detection

- MANGAL DOSHA: Mars in 1/2/4/7/8/12 from lagna. Include cancellation checks (Mars in own sign, Mars in Aries/Scorpio/Capricorn, benefic aspect on Mars, same dosha in both charts)
- KAAL SARP DOSHA: All 7 planets hemmed between Rahu-Ketu axis. Partial Kaal Sarp if one planet escapes.
- SADESATI: Saturn transiting 12th/1st/2nd from Moon sign (compute for current date + next occurrence)
- PITRA DOSHA: Sun conjunct Rahu, or 9th lord afflicted by Rahu/Ketu/Saturn

### compute/matching.py — Ashtakoot (36 Guna Milan)

All 8 kootas with proper lookup tables:
1. Varna (1 point) — based on Moon sign element
2. Vasya (2 points) — sign-based compatibility table
3. Tara (3 points) — nakshatra distance modulo 9
4. Yoni (4 points) — nakshatra animal compatibility (14 animals)
5. Graha Maitri (5 points) — planetary friendship between Moon nakshatra lords
6. Gana (6 points) — Deva/Manushya/Rakshasa from nakshatra
7. Bhakoot (7 points) — Moon sign distance (avoid 2/12, 6/8, 5/9 negative combos)
8. Nadi (8 points) — Aadi/Madhya/Antya from nakshatra (same = 0 points)

Return: total/36, percentage, per-koota breakdown, recommendation text

### compute/panchang.py — Panchang

For any given date + location:
- Tithi (1-30, from Moon-Sun angular distance / 12)
- Paksha (Shukla/Krishna)
- Nakshatra (Moon's current nakshatra)
- Yoga (Sun+Moon longitude / 13.333)
- Karana (half-tithi)
- Vara (day of week)
- Rahu Kaal (calculate from sunrise for the location)

### compute/transit.py — Transit Analysis

For any target date:
- Compute all 9 planet positions
- Overlay on natal chart (which transit houses they activate)
- Flag major transits: Saturn over natal Moon (Sadesati), Jupiter over natal houses, Rahu-Ketu transit

### compute/muhurta.py — Auspicious Timing

Given a purpose (marriage, business start, travel, property purchase):
- Scan upcoming dates
- Filter by: favorable nakshatra, tithi, yoga, day of week
- Exclude: Rahu Kaal, Yamaghanda, Gulika
- Return top 5 dates with reasoning

---

## KNOWLEDGE YAML FILES

### lordship_rules.yaml
For ALL 12 lagnas, specify:
- sign_lord
- yogakaraka (with reasoning)
- functional_benefics (list)
- functional_malefics (list)
- maraka planets (with house number and reasoning)
- gemstone_recommendation per planet (wear/avoid/test/neutral with reasoning)

Reference the complete data from the project instructions document. Every lagna must have complete data.

### yoga_definitions.yaml
For each yoga:
```yaml
gajakesari:
  name_en: "Gajakesari Yoga"
  name_hi: "गजकेसरी योग"
  type: "benefic"
  formation:
    condition: "Jupiter in kendra (1/4/7/10) from Moon"
    planets: ["Jupiter", "Moon"]
  cancellation:
    - "Jupiter combust"
    - "Jupiter debilitated without Neech Bhanga"
  effects:
    general: "Wisdom, fame, long life, leadership"
    career: "Rise to prominent positions"
    finance: "Wealth accumulation"
  strength_factors:
    - "Jupiter in own/exalted sign = strongest"
    - "Jupiter in friend's sign = moderate"
    - "Jupiter retrograde = delayed but effective"
```

### gemstone_logic.yaml
```yaml
gemstones:
  Sun:
    primary: {name_en: "Ruby", name_hi: "माणिक्य (Manikya)", substitute: "Garnet"}
    finger: "Ring finger"
    hand: "Right"
    metal: "Gold"
    day: "Sunday"
    hora: "Sun hora (first hour after sunrise on Sunday)"
    mantra: "ओम् ह्रां ह्रीं ह्रौम् सः सूर्याय नमः"
    mantra_count: 7000  # For siddhi (energizing)
    weight_formula: "body_weight_kg / 10 in ratti (minimum 3 ratti)"
  # ... all 9 planets with complete data

decision_framework:
  always_safe:
    - "Lagnesh stone"
    - "Yogakaraka stone"
    - "Current beneficial Mahadasha lord stone"
  use_caution:
    - "Debilitated planet stone"
    - "Combust planet stone"
    - "8th+9th mixed lord stone"
  never_wear:
    - "Pure 6th lord stone (unless also trikona lord)"
    - "Maraka planet stone during health-vulnerable dasha"
    - "Stones from shatru (enemy) planetary groups simultaneously"

contraindications:
  - "Never wear Ruby + Blue Sapphire (Sun enemy of Saturn)"
  - "Never wear Pearl + Hessonite (Moon enemy of Rahu)"
  - "Never wear Red Coral + Emerald (Mars enemy of Mercury) — debatable"

planetary_friendships:
  friends:
    Sun: [Moon, Mars, Jupiter]
    Moon: [Sun, Mercury]
    Mars: [Sun, Moon, Jupiter]
    Mercury: [Sun, Venus]
    Jupiter: [Sun, Moon, Mars]
    Venus: [Mercury, Saturn]
    Saturn: [Mercury, Venus]
  enemies:
    Sun: [Saturn, Venus]
    Moon: [Rahu, Ketu]
    Mars: [Mercury]
    Mercury: [Moon]
    Jupiter: [Mercury, Venus]
    Venus: [Sun, Moon]
    Saturn: [Sun, Moon, Mars]
```

### nakshatra_data.yaml
All 27 nakshatras with:
- name (English + Devanagari)
- span (start-end degrees)
- lord (dasha lord)
- deity
- symbol
- gana (Deva/Manushya/Rakshasa)
- nature (Fixed/Movable/Sharp/Soft/etc.)
- animal (for yoni matching)
- element
- body_part
- psychological_profile (2-3 sentences)

### weekly_routine.yaml
```yaml
monday:
  planet: Moon
  deity: Shiva
  color: White
  food: Rice kheer, milk products
  fasting: "Optional — milk/fruit fast"
  mantra: "ओम् नमः शिवाय"
  daan: "White items — rice, milk, sugar, white cloth"
  activity: "Good for: starting new studies, mental work, water-related activities"
  avoid: "Property deals, confrontations"
# ... all 7 days
```

---

## LLM BACKEND (interpret/llm_backend.py)

Factory pattern. All backends implement same interface:

```python
class LLMBackend(Protocol):
    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str: ...
    def name(self) -> str: ...
    def is_available(self) -> bool: ...
```

Implementations:
1. OllamaBackend — uses `ollama` Python package. Default model: qwen3:8b
2. GroqBackend — uses `groq` Python package. Free tier.
3. ClaudeBackend — uses `anthropic` Python package.
4. OpenAIBackend — uses `openai` Python package.
5. NoLLMBackend — returns raw JSON data, no interpretation.

Factory function: `get_backend(name, model=None, api_key=None) -> LLMBackend`

Each backend must:
- Have clear error messages if not configured (e.g., "Ollama not running. Start with: ollama serve")
- Be independently installable (only install ollama package if using ollama)
- Support streaming (optional, nice-to-have)

---

## PROMPT TEMPLATES (interpret/prompts/)

Each .md file is a Jinja2-compatible template that receives chart data and produces a section of the report.

### system_prompt.md
The master system identity. Include:
- "You are Jyotish AI, a computational Vedic astrologer"
- Reference Parashari tradition
- Hindi+English bilingual
- Every statement must reference specific chart factors
- Tone: supportive but direct, never vague
- Include the relevant learned rules from Pandit Ji (injected dynamically)

### life_event_validation.md
Template that takes: chart data + list of life events
Produces: table matching each event to the dasha running, with explanation and match rating

### remedy_generation.md
Template that takes: chart data + current dasha + existing practices
Produces: gemstone recommendations (with full vidhan), weekly routine, mantras, behavioral remedies
Must include contraindication logic from gemstone_logic.yaml

### daily_suggestion.md
Template for one-line daily advice:
"Today is Wednesday. Wear green. Budh mantra recommended. Good for: document work, communication. Avoid: major financial decisions (Moon transiting 8th house)."

---

## PANDIT JI LEARNING SYSTEM (learn/)

### corrections.py
- PanditCorrection dataclass with: id, pandit_name, date, chart_name, category, ai_said, pandit_said, pandit_reasoning, correction_type, planets_involved, houses_involved, lagna, status, confidence, audio_file, transcript
- PanditCorrectionStore: file-based JSON store
- Methods: add_correction, validate_correction, get_relevant_rules, get_prompt_additions, get_stats, generate_comparison_table

### validator.py
- MultiSourceValidator: validates corrections against DrikPanchang, second pandit, life events
- Confidence scoring: +0.3 per validation, -0.2 per dispute
- Status transitions: pending → validated/disputed → learned/rejected

### rule_extractor.py
- Groups validated corrections by (category, lagna, planets)
- Extracts LearnedRule when confidence >= threshold
- Generates prompt_addition text for each rule
- Only learns from validated corrections (NEVER from pending)

### audio_processor.py
- Takes Hindi audio file path
- Uses Whisper (via groq API or local whisper.cpp)
- Transcribes to text
- Extracts structured corrections using LLM
- Returns list of PanditCorrection objects (status=pending, for human review)

---

## CLI (jyotish/cli.py)

Use `click` library. Commands:

```bash
# Compute chart
jyotish chart --name "Rajesh Kumar" --dob "15/08/1990" --tob "06:30" --place "Jaipur" --gender Male

# Full report (chart + interpretation)
jyotish report --name "Rajesh Kumar" --dob "15/08/1990" --tob "06:30" --place "Jaipur" --gender Male --llm ollama --output report.md

# With life events
jyotish report --name "Rajesh Kumar" --dob "15/08/1990" --tob "06:30" --place "Jaipur" --events events.json

# Today's transit for a saved chart
jyotish transit --chart charts/rajesh.json

# Daily suggestion
jyotish daily --chart charts/rajesh.json

# Ashtakoot matching
jyotish match --person1 charts/rajesh.json --person2 charts/priya.json

# Muhurta
jyotish muhurta --purpose marriage --person charts/rajesh.json --from "01/04/2026" --to "30/06/2026"

# Pandit Ji correction
jyotish correct --chart "Rajesh Kumar" --category gemstone --ai-said "Wear pukhraj" --pandit-said "Pukhraj for Mithuna is maraka stone, avoid"

# Process Pandit Ji audio
jyotish learn-audio --file panditji_session.mp3 --chart "Rajesh Kumar"

# Show learned rules
jyotish rules --lagna Mithuna

# Panchang for today
jyotish panchang --place "Varanasi"

# Export chart as JSON
jyotish export --name "Rajesh Kumar" --dob "15/08/1990" --tob "06:30" --place "Jaipur" --format json
```

---

## TESTING (tests/)

### test_chart.py
Test against KNOWN verified chart (Manish Chaurasia):
- DOB: 13/03/1989, Time: 12:17 PM, Place: Varanasi (25.3176, 83.0067)
- Expected Lagna: Mithuna (Gemini)
- Expected Moon: Vrishabha (Taurus), Rohini nakshatra, 2nd pada
- Verify all planet positions are within 1 degree of known values
- Verify houses are correct for whole sign

### test_dasha.py
- For Moon in Rohini: first dasha lord should be Moon
- Verify dasha sequence: Moon → Mars → Rahu → Jupiter → Saturn → Mercury → Ketu → Venus → Sun
- Verify current dasha for date 15/03/2026 (should be in Jupiter Mahadasha)

### test_yoga.py
- Create a chart with Jupiter in Cancer (exalted) in 1st house → should detect Hamsa Yoga
- Create a chart with Jupiter in kendra from Moon → should detect Gajakesari
- Create a chart with all planets between Rahu-Ketu → should detect Kaal Sarp Dosha

### test_matching.py
- Test same nakshatra matching → Nadi should be 0 points
- Test compatible nakshatras → verify total score

---

## DEPENDENCIES (pyproject.toml)

```toml
[project]
name = "vedic-ai-framework"
version = "0.1.0"
description = "AI-powered Vedic astrology computation and interpretation"
requires-python = ">=3.11"
license = {text = "MIT"}
dependencies = [
    "pyswisseph>=2.10.0",
    "pyyaml>=6.0",
    "click>=8.0",
    "geopy>=2.4.0",
    "timezonefinder>=6.0",
    "pytz>=2024.1",
    "jinja2>=3.0",
    "rich>=13.0",
]

[project.optional-dependencies]
ollama = ["ollama>=0.4.0"]
groq = ["groq>=0.9.0"]
claude = ["anthropic>=0.39.0"]
openai = ["openai>=1.50.0"]
pdf = ["reportlab>=4.0"]
telegram = ["python-telegram-bot>=21.0"]
whisper = ["openai-whisper>=20231117"]
all = ["vedic-ai-framework[ollama,groq,claude,openai,pdf,telegram]"]
dev = ["pytest>=8.0", "pytest-cov>=5.0"]

[project.scripts]
jyotish = "jyotish.cli:main"

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"
```

---

## CLAUDE.md (For Claude Code to understand the project)

Create this file in root:

```markdown
# Vedic AI Framework

## Commands
- `pytest` — run all tests
- `jyotish --help` — CLI help
- `pip install -e ".[dev,ollama]"` — install for development

## Architecture
- compute/ — deterministic Swiss Ephemeris calculations. NEVER use LLM for computation.
- knowledge/ — YAML files with Parashari Jyotish rules. Editable by humans.
- interpret/ — LLM-powered interpretation. Default: Ollama (free, local).
- learn/ — Pandit Ji correction and learning system.
- deliver/ — Output formatting and delivery.

## Conventions
- Python 3.11+, type hints on all functions
- Dataclasses for all data structures, no dicts
- config.yaml for all configuration, no hardcoded values
- Hindi text in Devanagari script, English text in plain ASCII
- All YAML knowledge files are the source of truth for astrological rules
- Swiss Ephemeris positions are NEVER approximated — always computed via pyswisseph
- Every prompt template is a standalone .md file in interpret/prompts/
- Tests use pytest, fixtures in conftest.py

## Key Patterns
- LLM backend is selected via factory: get_backend("ollama")
- Chart data flows as ChartData dataclass through the entire pipeline
- Pandit Ji corrections are JSON files in data/pandit_corrections/
- All astrological constants are in utils/constants.py, NOT scattered in code
```

---

## WHAT TO BUILD FIRST (Priority Order)

1. utils/constants.py — All astrological constants
2. compute/chart.py — Core chart computation
3. compute/dasha.py — Dasha calculator
4. compute/divisional.py — D9 Navamsha
5. compute/yoga.py — Yoga detection
6. compute/dosha.py — Dosha checks
7. compute/panchang.py — Panchang
8. compute/matching.py — Ashtakoot
9. knowledge/*.yaml — All knowledge files (complete data)
10. interpret/llm_backend.py — LLM factory
11. interpret/prompts/*.md — All prompt templates
12. interpret/interpreter.py — Orchestrator
13. learn/corrections.py — Pandit Ji system
14. cli.py — CLI entry point
15. tests/ — All tests
16. README.md — GitHub landing page
17. config.yaml — Configuration
18. pyproject.toml — Packaging

After building each file, run the relevant tests to verify correctness.

---

## FINAL CHECKLIST (Verify before marking complete)

- [ ] `pip install -e ".[dev,ollama]"` succeeds
- [ ] `pytest` passes all tests
- [ ] `jyotish chart --name "Test" --dob "13/03/1989" --tob "12:17" --place "Varanasi"` produces Mithuna lagna
- [ ] `jyotish report --name "Test" --dob "13/03/1989" --tob "12:17" --place "Varanasi" --llm none` produces JSON chart
- [ ] All 12 lagnas have complete lordship data in YAML
- [ ] All 27 nakshatras have complete data in YAML
- [ ] All 9 gemstones have complete data in YAML
- [ ] Yoga detection finds at least 5 yogas in a typical chart
- [ ] Dasha calculation matches known timeline for Manish (Moon dasha at birth → current Jupiter dasha)
- [ ] Navamsha computation produces valid sign indices (0-11)
- [ ] Ashtakoot matching returns score out of 36
- [ ] Pandit Ji correction system stores and retrieves corrections
- [ ] LLM backend factory returns correct backend for each option
- [ ] README.md is comprehensive with architecture diagram, quick start, examples
- [ ] .gitignore excludes data/, __pycache__, .env, *.pyc, dist/, *.egg-info/
