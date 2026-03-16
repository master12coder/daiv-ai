# VEDIC AI FRAMEWORK — PHASE 2 MASTER SPECIFICATION
# Engineering Standards + Architecture Audit + New Features Build
#
# INSTRUCTIONS FOR CLAUDE CODE:
# 1. Read this ENTIRE document first
# 2. Audit existing Phase 1 code against engineering standards
# 3. Refactor Phase 1 where needed
# 4. Build Phase 2 features with correct architecture
# 5. Work autonomously. Do not ask questions.

---

## SECTION 1: ENGINEERING STANDARDS (Apply to ALL code)

### 1.1 Architecture Pattern: Clean Architecture + Domain Driven Design

```
jyotish/
├── domain/              # Core business logic — ZERO external dependencies
│   ├── models/          # Dataclasses, value objects, entities
│   ├── rules/           # Business rules (lordship, yoga conditions, gemstone logic)
│   └── constants/       # All astrological constants
│
├── compute/             # Infrastructure: Swiss Ephemeris wrapper
│   ├── ephemeris.py     # Low-level Swiss Ephemeris calls ONLY
│   ├── chart.py         # Chart computation orchestrator
│   ├── dasha.py         # Dasha calculator
│   ├── divisional.py    # Varga chart computations
│   ├── yoga.py          # Yoga detection engine
│   ├── dosha.py         # Dosha checks
│   ├── panchang.py      # Panchang computation
│   ├── matching.py      # Ashtakoot matching
│   ├── transit.py       # Transit computation
│   ├── strength.py      # Shadbala computation
│   ├── ashtakavarga.py  # Ashtakavarga system
│   ├── bhava_chalit.py  # Bhava Chalit house system
│   ├── muhurta.py       # Muhurta computation
│   └── upagraha.py      # Shadow planets
│
├── knowledge/           # Static knowledge files (YAML)
│   ├── lordship_rules.yaml
│   ├── yoga_definitions.yaml
│   ├── gemstone_logic.yaml
│   ├── nakshatra_data.yaml
│   ├── remedy_rules.yaml
│   ├── combustion.yaml
│   ├── aspects.yaml
│   ├── dignity.yaml
│   ├── direction_mapping.yaml
│   └── weekly_routine.yaml
│
├── scriptures/          # [NEW] Classical text database
│   ├── scripture_db.py
│   ├── bphs/            # Brihat Parashara Hora Shastra rules
│   ├── brihat_jataka/
│   ├── phaladeepika/
│   └── lal_kitab/
│
├── interpret/           # LLM interpretation layer
│   ├── llm_backend.py   # LLM abstraction (Ollama/Groq/Claude/OpenAI)
│   ├── interpreter.py   # Orchestrator
│   ├── formatter.py     # Output formatting
│   └── prompts/         # Jinja2 prompt templates
│
├── learn/               # Pandit Ji learning system
│   ├── corrections.py   # Correction store
│   ├── validator.py     # 6-layer validation pipeline
│   ├── rule_extractor.py
│   ├── trust_scorer.py  # [NEW] Per-source trust scoring
│   ├── life_events_db.py # [NEW] SQLite life events database
│   ├── prediction_tracker.py # [NEW] Track prediction outcomes
│   └── audio_processor.py
│
├── deliver/             # Output delivery
│   ├── markdown_report.py
│   ├── json_export.py
│   └── telegram_bot.py
│
├── interfaces/          # Entry points
│   ├── cli.py           # Click CLI
│   └── api.py           # [FUTURE] FastAPI REST endpoint
│
├── utils/               # Shared utilities
│   ├── geo.py           # Geocoding
│   ├── datetime_utils.py
│   └── logging_config.py # [NEW] Structured logging
│
└── config/              # Configuration
    ├── settings.py      # Config loader (from YAML + env vars)
    └── default.yaml     # Default configuration

```

### 1.2 Coding Rules (MANDATORY)

RULE 1 — NO MAGIC NUMBERS:
```python
# WRONG:
if degree < 12:
    return "combust"

# RIGHT:
COMBUSTION_LIMITS = {"Moon": 12, "Mars": 17, ...}  # In constants
if degree < COMBUSTION_LIMITS[planet]:
    return "combust"
```

RULE 2 — NO FILE EXCEEDS 300 LINES:
If any file approaches 300 lines, split into focused modules.
Example: If yoga.py has 25 yoga functions = split into:
- yoga/panch_mahapurush.py (5 yogas)
- yoga/raj_yoga.py (Raj + Dhan + Vipreet)
- yoga/nabhasa_yoga.py (pattern yogas)
- yoga/detector.py (orchestrator that calls all sub-modules)

RULE 3 — TYPE HINTS ON EVERYTHING:
```python
def compute_navamsha(longitude: float) -> int:
    ...
def find_current_dasha(
    mahadashas: list[DashaPeriod],
    target_date: datetime
) -> tuple[DashaPeriod | None, DashaPeriod | None, DashaPeriod | None]:
    ...
```

RULE 4 — DATACLASSES FOR ALL DATA STRUCTURES:
No raw dicts flowing through the system. Every data structure is a typed dataclass.

RULE 5 — DEPENDENCY INJECTION FOR LLM:
```python
# WRONG:
class Interpreter:
    def __init__(self):
        self.llm = OllamaBackend()  # Hardcoded

# RIGHT:
class Interpreter:
    def __init__(self, llm: LLMBackend):
        self.llm = llm  # Injected
```

RULE 6 — CONFIGURATION FROM YAML + ENV VARS:
```python
# All tunable values in config/default.yaml
# Overridable via environment variables:
#   JYOTISH_LLM_BACKEND=claude
#   JYOTISH_LLM_MODEL=claude-sonnet-4-20250514
#   ANTHROPIC_API_KEY=sk-...
```

RULE 7 — STRUCTURED LOGGING:
```python
import logging
logger = logging.getLogger(__name__)

# Every significant operation logged:
logger.info("Computing chart", extra={"name": name, "dob": dob, "place": place})
logger.debug("Planet position", extra={"planet": "Jupiter", "longitude": 36.5})
logger.warning("Birth time near lagna boundary", extra={"lagna_degree": 29.8})
```

RULE 8 — ERROR HANDLING:
Custom exceptions for domain errors:
```python
class JyotishError(Exception): pass
class BirthTimeError(JyotishError): pass
class GeocodingError(JyotishError): pass
class LLMConnectionError(JyotishError): pass
class ScriptureNotFoundError(JyotishError): pass
class ValidationError(JyotishError): pass
```

RULE 9 — EVERY PUBLIC FUNCTION HAS DOCSTRING:
```python
def compute_shadbala(planet: str, chart: ChartData) -> ShadbalaResult:
    """
    Compute six-fold planetary strength (Shadbala) for a planet.

    Args:
        planet: Planet name (e.g., "Jupiter")
        chart: Computed chart data

    Returns:
        ShadbalaResult with all 6 components and total strength ratio.
        Ratio > 1.0 means planet is strong. < 1.0 means weak.

    Reference:
        BPHS Chapter 27-28 (Shadbala calculation)
    """
```

RULE 10 — TESTS FOR EVERY COMPUTE FUNCTION:
pytest with fixtures. Test against known verified values (DrikPanchang cross-checked).

---

## SECTION 2: AUDIT EXISTING PHASE 1 CODE

Before building Phase 2, audit ALL existing files.

### Audit Checklist:

For EVERY file in jyotish/:
1. [ ] File under 300 lines? If not → refactor/split
2. [ ] Type hints on all functions?
3. [ ] No magic numbers? All constants in constants module?
4. [ ] Dataclasses used (not raw dicts)?
5. [ ] Proper error handling?
6. [ ] Logging present?
7. [ ] Docstrings on public functions?
8. [ ] No duplicated logic across files?
9. [ ] Dependencies injected (not hardcoded)?
10. [ ] Config loaded from YAML (not hardcoded)?

### Likely Issues to Fix:

- compute/chart.py is probably too large (all constants + computation in one file)
  → Split: constants into domain/constants/, computation logic into focused modules
- knowledge/*.yaml files may have incomplete data
  → Verify all 12 lagnas, 27 nakshatras, 9 gemstones have COMPLETE entries
- LLM backend may have hardcoded model names
  → Move to config/default.yaml
- Tests may not cover edge cases
  → Add: lagna boundary test, nakshatra boundary test, dasha boundary test

### Refactoring Actions:

1. Extract ALL astrological constants into domain/constants/:
   - signs.py (sign names, lords, elements)
   - nakshatras.py (27 nakshatras, lords, spans)
   - planets.py (dignities, friendships, combustion limits, aspects)
   - dashas.py (sequence, years)
   
2. Extract all data models into domain/models/:
   - chart_models.py (PlanetPosition, ChartData, DashaPeriod)
   - yoga_models.py (YogaResult)
   - dosha_models.py (DoshaResult)
   - matching_models.py (MatchingResult)
   - panchang_models.py (PanchangData)

3. Create domain/rules/ for business rule lookups:
   - lordship.py (load from YAML, provide query functions)
   - gemstone_advisor.py (recommendation engine with contraindication logic)

4. Add config/settings.py:
   - Load from config/default.yaml
   - Override with environment variables
   - Provide typed Settings dataclass

5. Add utils/logging_config.py:
   - JSON structured logging
   - Log level from config
   - Separate loggers per module

---

## SECTION 3: BUILD PHASE 2 FEATURES

### Priority 1: Ashtakavarga (Most impactful for accuracy)

Create: jyotish/compute/ashtakavarga.py

Ashtakavarga is a point-based transit prediction system from BPHS chapters 66-72.

Implementation:
- 7 planets (Sun through Saturn) each contribute benefic points (bindus) to 12 signs
- Points contributed by: same planet + 6 other planets + Lagna = 8 sources ("ashta")
- Use standard BPHS bindu tables for each planet's Bhinnashtakavarga
- Sarvashtakavarga = sum across all 7 planets per sign
- Sarvashtakavarga total MUST equal 337 (verification check)
- Trikona Shodhana (reduction) for advanced analysis

Transit application:
- Planet transiting sign with 4+ bindus = favorable
- Planet transiting sign with 0-2 bindus = unfavorable
- This makes transit predictions MUCH more accurate than generic "Saturn in X house"

Output: AshtakavargaResult dataclass with 7 Bhinna tables + 1 Sarva table

### Priority 2: Bhava Chalit Chart

Create: jyotish/compute/bhava_chalit.py

Different from Rashi chart. Uses Placidus or Sripathi house cusps.
Planets can fall in different houses than Rashi chart.

Implementation:
- Compute house cusps using swe.houses(jd, lat, lon, b'P') for Placidus
- For each planet, determine which bhava (cusp-to-cusp range) it falls in
- Compare with Rashi house placement
- Flag "bhava shift" planets — these need special interpretation

Output: BhavaChartResult with rashi_house and bhava_house per planet

### Priority 3: Shadbala (Six-fold Strength)

Create: jyotish/compute/strength.py (or refactor existing)

6 components per planet (see PHASE2_SPEC.md Part A3 for full details):
1. Sthana Bala (positional) — from dignity, varga positions, house type
2. Dig Bala (directional) — from house position
3. Kala Bala (temporal) — from birth time, day/night, paksha
4. Cheshta Bala (motional) — from speed/retrogression
5. Naisargika Bala (natural) — fixed values per planet
6. Drik Bala (aspectual) — from aspects received

Total → Shadbala Ratio → Strong (>1) or Weak (<1)

### Priority 4: Scripture Database

Create: jyotish/scriptures/ directory

Structure rules from BPHS as YAML (see PHASE2_SPEC.md Part B for format).
Start with chapters most relevant to interpretation:
- Chapter 3: Nature of planets
- Chapter 5: Houses and their meanings
- Chapter 7: Planetary friendships
- Chapter 10: Yogas
- Chapter 19: Marriage
- Chapter 25-26: Dasha effects
- Chapter 66-72: Ashtakavarga
- Chapter 80: Gemstones
- Chapter 85: Remedies

Create scripture_db.py with query functions:
- query_by_planet(planet, house)
- query_by_topic(topic)
- validate_against_scripture(correction)

### Priority 5: 6-Layer Validation Safeguards

Update: jyotish/learn/validator.py

Implement all 6 layers as described in PHASE2_SPEC.md Part C:
1. Astronomical fact check (auto-reject if contradicts computation)
2. Scripture cross-reference (flag if contradicts BPHS)
3. Life event validation (strongest real-world evidence)
4. Multi-source consensus (single pandit ≠ truth)
5. Source trust scoring (per-pandit accuracy tracking)
6. Fact vs interpretation separation (computation is LOCKED)

Create: jyotish/learn/trust_scorer.py
- PanditTrustScore class with track record
- Levels: MASTER (0.8+), TRUSTED (0.6+), LEARNING (0.3+), UNVERIFIED (<0.3)

### Priority 6: Life Event Database

Create: jyotish/learn/life_events_db.py
- SQLite database (zero dependency)
- Tables: charts, events, predictions, remedies
- Methods: add_chart, add_event, find_similar, get_pattern_stats
- All chart data anonymizable

Create: jyotish/learn/prediction_tracker.py
- Log every prediction with confidence score
- Track outcomes: confirmed / not_occurred / opposite
- Accuracy dashboard by category

### Priority 7: Additional Varga Charts

Update: jyotish/compute/divisional.py
Add all 16 Shodashvarga charts (D1 through D60).
See PHASE2_SPEC.md Part A4 for division formulas.

### Priority 8: KP Sub-Lord

Create: jyotish/compute/kp.py
- 249 sub-divisions of zodiac
- For each planet: Nakshatra Lord, Sub Lord, Sub-Sub Lord
- Sub lord theory for result determination

### Priority 9: Additional Dasha Systems

Update or create: jyotish/compute/dasha.py or dasha/ module
- Yogini Dasha (36-year cycle)
- Ashtottari Dasha (108-year cycle)
- Chara Dasha (Jaimini, sign-based)

### Priority 10: Upagraha

Create: jyotish/compute/upagraha.py
- Gulika, Mandi (from Saturn)
- Dhuma, Vyatipata, Parivesha, Indrachapa, Upaketu (from Sun)

### Priority 11: Enhanced Prompts

Update all prompt templates to:
- Accept scripture_citations as template variable
- Accept statistical_patterns as template variable
- Include citations in output: "Saturn in 7th delays marriage (BPHS 19:8)"
- Include statistics: "73% of similar charts confirm this pattern"

Add new prompt templates:
- daily_suggestion.md (transit-based daily advice)
- pooja_planner.md (weekly/monthly worship schedule)
- remedy_tracker.md (track remedy effectiveness)

---

## SECTION 4: TESTING REQUIREMENTS

Every new feature needs tests:

```
tests/
├── compute/
│   ├── test_ashtakavarga.py    # Sarvashtakavarga total = 337
│   ├── test_bhava_chalit.py    # Verify bhava shifts for boundary cases
│   ├── test_shadbala.py        # Verify against known values
│   ├── test_divisional.py      # All 16 varga charts
│   ├── test_kp.py              # Sub-lord calculations
│   └── test_upagraha.py        # Shadow planet positions
├── scriptures/
│   ├── test_scripture_db.py    # Load, query, validate
│   └── test_citation.py        # Verify citations in output
├── learn/
│   ├── test_validator.py       # All 6 safeguard layers
│   ├── test_trust_scorer.py    # Trust score calculation
│   ├── test_life_events.py     # SQLite CRUD
│   └── test_prediction_tracker.py
└── integration/
    └── test_full_pipeline.py   # Birth details → full report with citations
```

Use Manish's chart (13/03/1989, 12:17 PM, Varanasi) as primary test fixture.
All positions verified against DrikPanchang.com output.

---

## SECTION 5: BUILD ORDER

Execute in this EXACT sequence:

PHASE 2A — Audit + Refactor (do this FIRST):
1. Audit all existing files against coding standards
2. Extract constants into domain/constants/
3. Extract models into domain/models/
4. Add config/settings.py with YAML loading
5. Add structured logging
6. Add custom exceptions
7. Refactor any file over 300 lines
8. Run pytest — all existing tests must still pass

PHASE 2B — Core Calculations:
9. Build Ashtakavarga
10. Build Bhava Chalit
11. Build Shadbala
12. Build all 16 Varga charts
13. Build KP Sub-Lord basics
14. Build Upagraha
15. Build additional Dasha systems
16. Run pytest — all tests must pass

PHASE 2C — Scripture + Learning:
17. Create scripture database structure
18. Digitize BPHS key chapters as YAML
19. Build scripture query engine
20. Build 6-layer validation pipeline
21. Build trust scoring system
22. Build life events SQLite database
23. Build prediction tracker
24. Run pytest — all tests must pass

PHASE 2D — Integration:
25. Update interpretation prompts with scripture citations
26. Update interpretation prompts with statistical patterns
27. Add daily suggestion prompt
28. Add pooja planner prompt
29. Update CLI with new commands
30. Final full test suite run
31. Update README.md with new features
32. Commit all changes

After each PHASE (2A, 2B, 2C, 2D), run full pytest suite.
Fix all failures before proceeding to next phase.
Commit after each phase with descriptive message.
