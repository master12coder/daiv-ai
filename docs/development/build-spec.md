# FINAL BUILD — ALL REMAINING PHASES
# One command. One night. Production-ready by morning.
#
# Claude Code: Read this ENTIRE document. Build EVERYTHING.
# Follow CLAUDE.md standards for every line of code.
# No empty files. No placeholder functions. No TODO comments.
# Every file must have real, working, tested code.
# Run pytest after each phase. Fix failures before moving on.
# Run `make audit` and `make safety-check` after each phase.
# Commit after each phase with descriptive conventional commit.

---

## PRE-BUILD AUDIT

Before building anything new, fix these critical issues first:

### Fix 1: Interpretation Safety (HIGHEST PRIORITY)
Read INTERPRETATION_FIX.md in the project root.
The current LLM interpretation does NOT inject lordship rules into prompts.
This causes DANGEROUS errors: recommending Yellow Sapphire for Mithuna lagna
where Jupiter is MARAKA.

Implementation:
1. Create jyotish/interpret/context/builder.py:
   - InterpretationContextBuilder class
   - Loads lordship_rules.yaml for the specific lagna
   - Loads gemstone_logic.yaml with contraindications
   - Queries scripture_db for relevant BPHS verses
   - Loads Pandit Ji learned rules
   - Returns InterpretationContext dataclass

2. Create jyotish/interpret/validation/safety_checker.py:
   - PostGenerationValidator class
   - scan_prohibited_stones(text, lagna) → list of violations
   - scan_maraka_errors(text, lagna) → list of violations
   - scan_generic_predictions(text) → list of violations
   - If violations found: log them, add warning banner to output

3. Update ALL prompt templates in interpret/prompts/:
   - Every template receives InterpretationContext
   - Every template has MANDATORY RULES section at top:
     ```
     ## MANDATORY RULES FOR {{lagna}} LAGNA
     Yogakaraka: {{context.yogakaraka}}
     Benefics: {{context.benefics}}
     Malefics: {{context.malefics}}
     MARAKA: {{context.maraka_planets}} — NEVER recommend their stones
     PROHIBITED STONES: {{context.prohibited_stones}}
     RECOMMENDED STONES: {{context.recommended_stones}}
     ```
   - Every template instructs LLM: "Do NOT recommend: {{prohibited_stones}}"
   - Remedy template has explicit gemstone decision framework injected

4. Update jyotish/interpret/interpreter.py:
   - Build context BEFORE every LLM call
   - Pass context to every prompt template
   - Run PostGenerationValidator on every LLM response
   - Log all validation results

5. Test with Manish's chart:
   - Panna (Emerald) = recommended as PRIMARY ✅
   - Pukhraj (Yellow Sapphire) = PROHIBITED with explanation ✅
   - Moonga (Red Coral) = PROHIBITED ✅
   - Moti (Pearl) = PROHIBITED ✅
   - Jupiter described as "7th+10th lord — MARAKA + career" ✅
   - Mercury described as "LAGNESH — most important planet" ✅

Commit: "fix(safety): inject lordship rules into all interpretation prompts"

### Fix 2: Architecture Compliance
Run `python3 scripts/architecture_audit.py`
Fix every violation found:
- Files over 300 lines → split
- Layer violations → fix imports
- Magic numbers → move to constants
- Missing type hints → add them
- Missing docstrings → add them

Run `python3 scripts/gemstone_safety_audit.py`
Fix every gap found.

Commit: "refactor: fix all architecture audit violations"

### Fix 3: Monorepo-Grade Project Structure
Ensure the project follows Python monorepo best practices:

```
vedic-ai-framework/
├── CLAUDE.md                     # ✅ exists
├── README.md                     # ✅ exists — verify comprehensive
├── LICENSE                       # ✅ exists
├── CONTRIBUTING.md               # ✅ exists
├── CHANGELOG.md                  # ✅ exists
├── SECURITY.md                   # ✅ exists
├── CODE_OF_CONDUCT.md            # ✅ exists
├── Makefile                      # ✅ exists
├── pyproject.toml                # ✅ exists — verify ruff/mypy/pytest configs
├── .editorconfig                 # ✅ exists
├── .python-version               # ✅ exists
├── .gitignore                    # ✅ exists — verify comprehensive
├── .gitattributes                # ✅ exists
│
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md  # ✅ exists
│   ├── ISSUE_TEMPLATE/           # ✅ exists
│   └── workflows/                # CREATE: CI/CD configs
│       ├── test.yml              # Run pytest on every push/PR
│       └── lint.yml              # Run ruff + mypy on every push/PR
│
├── config/
│   ├── default.yaml              # All defaults — verify complete
│   ├── .env.example              # ✅ exists
│   └── logging.yaml              # ✅ exists
│
├── docs/                         # ✅ exists — verify all populated
├── scripts/                      # ✅ exists — verify audit scripts work
├── examples/                     # Verify real examples, not stubs
├── data/                         # Runtime data directories
│   ├── pandit_corrections/
│   ├── charts/
│   └── life_events/
│
├── jyotish/                      # Main package
│   ├── __init__.py               # Version, package metadata
│   ├── domain/
│   ├── compute/
│   ├── knowledge/
│   ├── scriptures/
│   ├── interpret/
│   ├── learn/
│   ├── deliver/
│   ├── interfaces/
│   ├── utils/
│   └── config/
│
└── tests/                        # Mirror source structure
    ├── conftest.py               # Shared fixtures (Manish's chart)
    ├── compute/
    ├── interpret/
    ├── learn/
    ├── scriptures/
    └── integration/
```

Verify EVERY directory has real files. No empty __init__.py without purpose.
Every __init__.py should export the module's public API.

Commit: "chore: verify project structure, add CI workflows"

---

## PHASE 3: SCRIPTURE GROUNDING + STATISTICAL LEARNING

### 3A: Expand Scripture Database
Current: 8 BPHS chapters with ~127 rules.
Target: 20+ chapters with 500+ rules.

Add these BPHS chapters as structured YAML:
- Chapter 11-12: Planetary effects in each house (12 houses × 9 planets = 108 rules minimum)
- Chapter 13-14: Effects of house lords in different houses
- Chapter 15-18: Raja Yoga, Dhana Yoga formations
- Chapter 20-24: Effects of different Bhavas
- Chapter 34-45: Effects of Dashas (Vimshottari effects per planet)
- Chapter 47-50: Ashtakavarga effects
- Chapter 78-79: Gemstone prescription rules
- Chapter 81-84: Muhurta rules
- Chapter 93-97: Remedial measures

Each rule MUST have:
```yaml
- id: "BPHS-11-003"
  source: "Brihat Parashara Hora Shastra"
  chapter: 11
  verse: 3
  topic: "sun_in_houses"
  condition:
    planet: Sun
    house: 1
  prediction: "Strong personality, leadership qualities, good health"
  exceptions: ["If combust: reduced vitality", "If aspected by Saturn: delayed recognition"]
  cross_references: ["BJ-03-005"]
```

### 3B: Add Lal Kitab Remedies
Create jyotish/scriptures/lal_kitab/remedies.yaml
- Simple, practical remedies per planet per house
- 9 planets × 12 houses = 108 remedy sets
- Each remedy: what to do, when, cost (free/low), expected timeline
- Tag: source = "Lal Kitab"

### 3C: Scripture-Cited Interpretation
Update interpret/interpreter.py:
- For every section of interpretation, query scripture_db
- Pass matching rules to LLM prompt
- LLM MUST cite source: "Sun in 9th house brings fortune through father (BPHS 11:42)"
- If no scripture found for a claim → LLM must say "Based on traditional interpretation (no direct BPHS reference)"

### 3D: Life Events Database (Production-Ready)
Create/enhance jyotish/learn/life_events_db.py with SQLite:

Tables:
```sql
CREATE TABLE charts (
    id TEXT PRIMARY KEY,
    lagna_sign INTEGER,
    moon_sign INTEGER,
    moon_nakshatra INTEGER,
    planets_json TEXT,  -- JSON blob of all planet positions
    yogas_json TEXT,
    doshas_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE events (
    id TEXT PRIMARY KEY,
    chart_id TEXT REFERENCES charts(id),
    event_type TEXT,  -- marriage, child, career, health, death, financial, education
    event_date TEXT,
    description TEXT,
    mahadasha TEXT,
    antardasha TEXT,
    validated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE predictions (
    id TEXT PRIMARY KEY,
    chart_id TEXT REFERENCES charts(id),
    prediction TEXT,
    category TEXT,
    confidence REAL,
    basis TEXT,  -- "BPHS-11-42 + life_event_pattern + pandit_teaching"
    timeframe_start TEXT,
    timeframe_end TEXT,
    outcome TEXT,  -- NULL until verified, then: confirmed/not_occurred/opposite
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE remedies_applied (
    id TEXT PRIMARY KEY,
    chart_id TEXT REFERENCES charts(id),
    remedy_type TEXT,  -- gemstone, mantra, daan, behavioral
    remedy_details TEXT,
    started_date TEXT,
    effectiveness TEXT,  -- positive/neutral/negative/pending
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

CLI commands:
```bash
jyotish events add --chart "Manish" --type marriage --date "2017-11" --description "Arranged marriage"
jyotish events list --chart "Manish"
jyotish predict track --chart "Manish" --prediction "Job change by Aug 2027" --confidence 0.75
jyotish predict outcome --id P001 --outcome confirmed
jyotish stats accuracy                    # Overall prediction accuracy
jyotish stats accuracy --category career  # Per-category accuracy
jyotish stats patterns --planet Jupiter --house 12  # What happened to people with Jupiter in 12th?
```

### 3E: Prediction Tracker with Accuracy Dashboard
Create jyotish/learn/prediction_tracker.py:
- Auto-log every prediction the system makes
- Track: prediction_text, confidence, basis (scripture + pattern + pandit)
- After timeframe passes: user marks outcome
- Calculate accuracy: overall, per-category, per-lagna, per-dasha
- Identify weak areas: "Health predictions for Kanya lagna = 52% accuracy — needs improvement"

CLI:
```bash
jyotish dashboard                # Show accuracy stats
jyotish dashboard --format json  # Machine-readable
```

Commit: "feat: expanded scripture DB, life events database, prediction tracker"

---

## PHASE 4: MULTI-SYSTEM ASTROLOGY

### 4A: Jaimini System
Create jyotish/compute/jaimini/:
- chara_karaka.py: Calculate 7 Chara Karakas (AK, AmK, BK, MK, PK, GK, DK) from planet degrees
- chara_dasha.py: Sign-based dasha (not planet-based like Vimshottari)
- jaimini_aspects.py: Fixed sign aspects (different from Parashari)
- pada.py: Arudha Pada calculations (A1-A12)

### 4B: KP System Enhancement
Enhance jyotish/compute/kp.py:
- 249 sub-lord table (complete, accurate)
- Ruling planets at query time
- KP significators (planet → star lord → sub lord chain)
- KP-based Yes/No answer engine for Prashna

### 4C: Enhanced Divisional Charts
Verify all 16 Shodashvarga charts are computing correctly.
Add Shodashvarga strength table:
- Each planet gets points from each varga chart
- Total Shodashvarga strength = sum of varga points
- This supplements Shadbala for comprehensive strength assessment

### 4D: Ashtakavarga Transit Predictions
Create jyotish/compute/transit_predictions.py:
- For upcoming 12 months: compute each planet's transit
- Rate each transit using Ashtakavarga bindus
- Generate month-by-month forecast:
  "April 2026: Saturn transiting Kumbha (27 bindus — favorable for your lagna).
   Jupiter transiting Vrishabha (20 bindus — challenging, watch finances).
   Best week: April 14-20 (Jupiter+Saturn both in high-bindu signs)."

Commit: "feat: Jaimini system, enhanced KP, transit predictions with Ashtakavarga"

---

## PHASE 5: DAILY COMPANION + DELIVERY

### 5A: Daily Suggestion Engine
Create jyotish/compute/daily.py:
- compute_today(chart_data) → DailySuggestion
- Uses: current transit positions + natal chart + current dasha + day of week + hora
- Returns:
  ```python
  @dataclass
  class DailySuggestion:
      date: str
      vara: str  # Day name
      current_hora: str  # Which planet's hora right now
      transit_impact: list[TransitImpact]  # Each planet's transit on natal houses
      recommended_mantra: str
      recommended_color: str
      recommended_food: str
      good_for: list[str]  # Activities favored today
      avoid: list[str]  # Activities to avoid
      health_focus: str
      ashtakavarga_rating: int  # 1-10 overall day rating
  ```

### 5B: Weekly Pooja Planner
Create jyotish/compute/pooja_planner.py:
- generate_weekly_plan(chart_data) → WeeklyPlan
- Based on: current dasha lord + lagna lord + weak planets in chart
- Maps to: day → deity → mantra → daan → color → food → temple
- Personalized: "Your Saturn is 8th+9th lord in 7th house → Shani mantra on Saturday is BENEFICIAL (9th lord aspect). NOT harmful."

### 5C: Muhurta Engine (Production)
Enhance jyotish/compute/muhurta.py:
- find_muhurta(purpose, chart, date_range) → list[MuhurtaDate]
- Purposes: marriage, business_start, travel, property, vehicle, naming_ceremony, griha_pravesh
- Checks: Panchang (tithi, nakshatra, yoga), Rahu Kaal, Yamaghanda, Gulika
- Returns top 5 dates with reasoning and confidence score

### 5D: Report Generator (Multiple Formats)
Create/enhance jyotish/deliver/:
- markdown_report.py: Full report as .md file (save to disk)
- json_export.py: Complete chart data as .json (for integrations)
- html_report.py: Beautiful HTML report (viewable in browser)
- Create report templates in deliver/templates/:
  - full_report.html.j2 (complete reading)
  - daily_brief.html.j2 (one-page daily)
  - matching_report.html.j2 (compatibility)
  - gemstone_card.html.j2 (gemstone recommendation card)

### 5E: CLI Enhancements
Add to interfaces/cli.py:
```bash
# Daily suggestion
jyotish daily --chart charts/manish.json
jyotish daily --name "Manish" --dob "13/03/1989" --tob "12:17" --place "Varanasi"

# Weekly pooja plan
jyotish pooja --chart charts/manish.json

# Muhurta finding
jyotish muhurta --purpose marriage --chart charts/manish.json --from "01/04/2026" --to "30/06/2026"

# Save chart for reuse (avoid re-computation)
jyotish save --name "Manish" --dob "13/03/1989" --tob "12:17" --place "Varanasi" --output charts/manish.json

# Load and use saved chart
jyotish report --chart charts/manish.json --llm groq
jyotish daily --chart charts/manish.json
jyotish transit --chart charts/manish.json --months 12

# Family group
jyotish family add --name "Vaishali" --dob "20/08/1992" --tob "unknown" --place "Varanasi" --relation wife
jyotish family list
jyotish match --person1 charts/manish.json --person2 charts/vaishali.json

# Export reports
jyotish report --chart charts/manish.json --llm groq --output report.md
jyotish report --chart charts/manish.json --llm groq --format html --output report.html
jyotish report --chart charts/manish.json --llm groq --format json --output report.json
```

Commit: "feat: daily companion, pooja planner, muhurta engine, multi-format reports"

---

## PHASE 6: PANDIT NETWORK + ADVANCED LEARNING

### 6A: Enhanced Pandit Trust System
Enhance jyotish/learn/trust_scorer.py:
- Track per-pandit: total_corrections, validated_count, contradicted_count, scripture_aligned, specialties
- Trust levels: MASTER (0.8+), TRUSTED (0.6+), LEARNING (0.3+), UNVERIFIED (<0.3)
- Pandit profile: "Pandit Ji Varanasi — Trust: 0.87, Specialties: Mithuna lagna, gemstones, 47 corrections"

### 6B: Audio Processing Pipeline
Create jyotish/learn/audio_processor.py:
- Takes audio file path (Hindi/English)
- Transcribes via Whisper (Groq free tier or local)
- Extracts structured corrections using LLM:
  - Birth details mentioned
  - Predictions made
  - Remedies suggested
  - Disagreements with prior readings
- Returns list[PanditCorrection] with status="pending"
- CLI: `jyotish learn audio --file session.mp3 --chart "Manish" --pandit "Varanasi"`

### 6C: Statistical Pattern Engine
Create jyotish/learn/pattern_engine.py:
- Analyze life_events_db for patterns:
  - "Jupiter in 12th for Mithuna: 73% had career growth with financial drain"
  - "Gajakesari Yoga present: 81% achieved leadership positions"
  - "Neelam worn during Saturn dasha: 68% reported positive effects"
- Minimum 10 charts needed for any pattern to be considered
- Patterns injected into interpretation prompts as statistical backing

### 6D: Correction Comparison Report
Enhance learn/corrections.py:
- generate_comparison(chart_name) → formatted table
- Shows [=] AI agrees with Pandit, [+] Pandit added info, [≠] Disagreement
- Exportable as markdown or HTML

Commit: "feat: pandit trust system, audio processing, pattern engine"

---

## PHASE 7: FINAL POLISH + PRODUCTION READINESS

### 7A: GitHub Actions CI
Create .github/workflows/test.yml:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -e ".[dev]"
      - run: python -m pytest tests/ -v --tb=short
      - run: python scripts/architecture_audit.py
      - run: python scripts/gemstone_safety_audit.py
```

Create .github/workflows/lint.yml:
```yaml
name: Lint
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install ruff mypy
      - run: ruff check jyotish/
      - run: mypy jyotish/ --ignore-missing-imports
```

### 7B: Comprehensive README.md
Rewrite README.md to be GitHub showcase quality:
- Project logo/banner (ASCII art or simple)
- One-line description
- Badges: tests passing, Python version, license
- Quick start (3 commands to first chart)
- Architecture diagram (ASCII)
- Feature list with status (✅ done, 🔄 in progress, 📋 planned)
- Comparison table: this vs AstroTalk vs AstroSage vs generic AI
- Screenshot/example of CLI output
- Contributing guide link
- License

### 7C: Example Data
Create real, useful examples in examples/:
- sample_input.json: Complete birth details
- sample_events.json: 10 life events with dates
- sample_chart_output.json: Full computed chart (from Manish's data)
- sample_report_hindi.md: Full Hindi report (generated, reviewed)
- sample_report_technical.md: Full technical report
- sample_correction.json: Example Pandit Ji correction
- sample_daily.md: Example daily suggestion
- sample_matching.json: Example Ashtakoot matching result

### 7D: Pre-configured LLM Setup
Create config/llm_providers.yaml:
```yaml
providers:
  groq:
    name: "Groq (Free Cloud)"
    setup: "1. Go to console.groq.com 2. Sign up free 3. Create API key 4. export GROQ_API_KEY=gsk_..."
    models:
      - llama-3.1-8b-instant  # Fast, good
      - llama-3.1-70b-versatile  # Best free quality
    free_tier: true
    speed: "2-5 seconds"

  ollama:
    name: "Ollama (Free Local)"
    setup: "1. curl -fsSL https://ollama.com/install.sh | sh 2. ollama pull qwen3:4b"
    models:
      - qwen3:4b   # 8GB RAM (MacBook Air)
      - qwen3:8b   # 16GB RAM
      - llama3.1:8b # 16GB RAM
    free_tier: true
    speed: "15-60 seconds depending on hardware"
    min_ram: "8GB for 4b models, 16GB for 8b models"

  claude:
    name: "Claude API (Paid, Best Quality)"
    setup: "1. Go to console.anthropic.com 2. Add credits 3. Create API key 4. export ANTHROPIC_API_KEY=sk-..."
    models:
      - claude-sonnet-4-20250514  # Best price/quality
      - claude-opus-4-20250514    # Best quality
    free_tier: false
    cost: "~$0.03-0.15 per report"

  openai:
    name: "OpenAI (Paid)"
    setup: "1. Go to platform.openai.com 2. Add credits 3. Create API key 4. export OPENAI_API_KEY=sk-..."
    models:
      - gpt-4o
      - gpt-4o-mini
    free_tier: false
```

CLI command to show setup:
```bash
jyotish setup-llm          # Interactive: shows all options, helps configure
jyotish setup-llm --test   # Tests current configuration
```

### 7E: Docker Support (Future-Ready)
Create Dockerfile:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install ".[groq]"
COPY . .
ENTRYPOINT ["python", "-m", "jyotish.cli"]
```

Create docker-compose.yml:
```yaml
version: '3.8'
services:
  jyotish:
    build: .
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./data:/app/data
      - ./charts:/app/charts
```

### 7F: Final Test Suite
Ensure test count is 300+:
- Compute tests: chart, dasha, all varga charts, yogas, doshas, panchang, ashtakavarga, shadbala, bhava chalit, KP, upagraha, jaimini, transit, muhurta, daily
- Interpret tests: context builder, safety validator, prompt rendering
- Learn tests: corrections, validator (6 layers), trust scorer, life events DB, prediction tracker, pattern engine
- Scripture tests: DB loading, querying, citation generation
- Integration tests: full pipeline, saved chart loading, family matching, daily suggestion, report export
- Safety tests: prohibited stones, maraka detection, generic prediction detection

Run: `make all-checks` — must pass 100%.

### 7G: Final Audit
```bash
python3 scripts/architecture_audit.py  # 0 violations
python3 scripts/gemstone_safety_audit.py  # 0 errors
make lint       # 0 errors
make typecheck  # 0 errors
make test       # 300+ tests, 100% passing
```

Commit: "feat: production-ready v1.0 — CI, Docker, comprehensive tests, polished README"

---

## BUILD ORDER (Execute in this EXACT sequence)

1. Pre-Build Audit (Fix 1, 2, 3) → commit
2. Phase 3A-3B: Scripture expansion → commit
3. Phase 3C: Scripture-cited interpretation → commit  
4. Phase 3D-3E: Life events DB + prediction tracker → commit
5. Phase 4A-4D: Jaimini, KP, transit predictions → commit
6. Phase 5A-5B: Daily companion, pooja planner → commit
7. Phase 5C-5E: Muhurta, reports, CLI → commit
8. Phase 6A-6D: Pandit network, audio, patterns → commit
9. Phase 7A-7G: CI, README, examples, Docker, final audit → commit
10. Final: `make all-checks` → `git push`

After EACH commit:
- Run `pytest` — must pass 100%
- Run `make audit` — must pass
- Run `make safety-check` — must pass
- Check: no file over 300 lines
- Check: no magic numbers
- Check: type hints on all functions

---

## FINAL VERIFICATION CHECKLIST

When ALL phases are complete, verify:

```bash
# Core functionality
jyotish chart --name "Manish" --dob "13/03/1989" --tob "12:17" --place "Varanasi" --gender Male
jyotish report --name "Manish" --dob "13/03/1989" --tob "12:17" --place "Varanasi" --llm groq
jyotish ashtakavarga --name "Manish" --dob "13/03/1989" --tob "12:17" --place "Varanasi"
jyotish kp --name "Manish" --dob "13/03/1989" --tob "12:17" --place "Varanasi"

# Save and reuse
jyotish save --name "Manish" --dob "13/03/1989" --tob "12:17" --place "Varanasi" -o charts/manish.json
jyotish daily --chart charts/manish.json
jyotish pooja --chart charts/manish.json
jyotish transit --chart charts/manish.json --months 6
jyotish muhurta --purpose business --chart charts/manish.json --from "01/04/2026" --to "30/06/2026"

# Events and predictions
jyotish events add --chart charts/manish.json --type marriage --date "2017-11" --desc "Arranged marriage"
jyotish predict track --chart charts/manish.json --prediction "Promotion by Dec 2026" --confidence 0.7
jyotish dashboard

# Audits
make test              # 300+ tests passing
make audit             # 0 architecture violations
make safety-check      # 0 gemstone safety errors
make lint              # 0 lint errors

# Report generation
jyotish report --chart charts/manish.json --llm groq --output reports/manish_full.md
jyotish report --chart charts/manish.json --format json --output reports/manish_data.json
```

The project is DONE when ALL of the above commands work without errors.
