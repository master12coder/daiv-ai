"""Scripture query interface — load and search classical text references."""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

from daivai_engine.models.scripture import ScriptureReference


logger = logging.getLogger(__name__)

_SCRIPTURES_DIR = Path(__file__).parent
_ALL_REFS: list[ScriptureReference] | None = None


def _load_yaml_rules(yaml_path: Path) -> list[ScriptureReference]:
    """Load scripture rules from a single YAML file."""
    if not yaml_path.exists():
        return []
    with open(yaml_path) as f:
        data = yaml.safe_load(f) or {}

    book = data.get("book", "BPHS")
    chapter = data.get("chapter", 0)
    rules = data.get("rules", [])

    refs = []
    for rule in rules:
        refs.append(
            ScriptureReference(
                book=book,
                chapter=chapter,
                verse=rule.get("verse"),
                topic=rule.get("topic", ""),
                planets=rule.get("planets", []),
                houses=rule.get("houses", []),
                text_sanskrit=rule.get("text_sanskrit", ""),
                text_english=rule.get("text_english", ""),
                text_hindi=rule.get("text_hindi", ""),
                rule_type=rule.get("rule_type", "general"),
            )
        )
    return refs


def _load_all() -> list[ScriptureReference]:
    """Load all scripture references from YAML files."""
    global _ALL_REFS
    if _ALL_REFS is not None:
        return _ALL_REFS

    _ALL_REFS = []
    for subdir in sorted(_SCRIPTURES_DIR.iterdir()):
        if subdir.is_dir() and not subdir.name.startswith("_"):
            for yaml_file in sorted(subdir.glob("*.yaml")):
                try:
                    refs = _load_yaml_rules(yaml_file)
                    _ALL_REFS.extend(refs)
                    logger.debug("Loaded %d rules from %s", len(refs), yaml_file.name)
                except Exception as e:
                    logger.warning("Error loading %s: %s", yaml_file.name, e)

    logger.info("Total scripture references loaded: %d", len(_ALL_REFS))
    return _ALL_REFS


def reload() -> None:
    """Force reload of all scripture data."""
    global _ALL_REFS
    _ALL_REFS = None
    _load_all()


def query_by_planet(planet: str, house: int | None = None) -> list[ScriptureReference]:
    """Query scripture references by planet and optionally house."""
    refs = _load_all()
    results = [r for r in refs if planet in r.planets]
    if house is not None:
        results = [r for r in results if house in r.houses or not r.houses]
    return results


def query_by_topic(topic: str) -> list[ScriptureReference]:
    """Query scripture references by topic keyword."""
    refs = _load_all()
    topic_lower = topic.lower()
    return [
        r for r in refs if topic_lower in r.topic.lower() or topic_lower in r.text_english.lower()
    ]


def query_by_chapter(book: str, chapter: int) -> list[ScriptureReference]:
    """Query by specific book and chapter."""
    refs = _load_all()
    return [r for r in refs if r.book == book and r.chapter == chapter]


def get_citation(ref: ScriptureReference) -> str:
    """Format a scripture reference as a citation string."""
    verse = f":{ref.verse}" if ref.verse else ""
    return f"{ref.book} {ref.chapter}{verse} — {ref.text_english[:80]}"


def get_all_references() -> list[ScriptureReference]:
    """Get all loaded scripture references."""
    return _load_all()
