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
