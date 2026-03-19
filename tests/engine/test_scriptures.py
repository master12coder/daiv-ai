"""Tests for scripture database in new engine package."""

from __future__ import annotations

from daivai_engine.models.scripture import ScriptureReference
from daivai_engine.scriptures.query import (
    get_all_references,
    query_by_planet,
    query_by_topic,
    reload,
)


class TestScriptureDB:
    def test_loads_references(self) -> None:
        reload()
        refs = get_all_references()
        assert len(refs) >= 500

    def test_query_by_planet(self) -> None:
        reload()
        results = query_by_planet("Sun")
        assert len(results) > 0
        for r in results:
            assert "Sun" in r.planets

    def test_query_by_topic(self) -> None:
        reload()
        results = query_by_topic("marriage")
        assert len(results) > 0

    def test_scripture_reference_type(self) -> None:
        reload()
        refs = get_all_references()
        for r in refs[:10]:
            assert isinstance(r, ScriptureReference)
            assert r.book
            assert r.chapter >= 0
