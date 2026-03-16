"""Test LLM backend factory."""

import pytest
from jyotish.interpret.llm_backend import (
    get_backend, list_backends,
    NoLLMBackend, OllamaBackend, GroqBackend, ClaudeBackend, OpenAIBackend,
)


class TestLLMBackendFactory:
    def test_get_none_backend(self):
        backend = get_backend("none")
        assert isinstance(backend, NoLLMBackend)
        assert backend.name() == "none"
        assert backend.is_available()

    def test_none_backend_returns_input(self):
        backend = get_backend("none")
        result = backend.generate("system", "user prompt data")
        assert result == "user prompt data"

    def test_get_ollama_backend(self):
        backend = get_backend("ollama")
        assert isinstance(backend, OllamaBackend)
        assert "ollama" in backend.name()

    def test_get_groq_backend(self):
        backend = get_backend("groq")
        assert isinstance(backend, GroqBackend)
        assert "groq" in backend.name()

    def test_get_claude_backend(self):
        backend = get_backend("claude")
        assert isinstance(backend, ClaudeBackend)
        assert "claude" in backend.name()

    def test_get_openai_backend(self):
        backend = get_backend("openai")
        assert isinstance(backend, OpenAIBackend)
        assert "openai" in backend.name()

    def test_unknown_backend_raises(self):
        with pytest.raises(ValueError, match="Unknown backend"):
            get_backend("nonexistent")

    def test_list_backends(self):
        backends = list_backends()
        assert "ollama" in backends
        assert "groq" in backends
        assert "claude" in backends
        assert "openai" in backends
        assert "none" in backends

    def test_custom_model(self):
        backend = get_backend("ollama", model="llama3:8b")
        assert "llama3:8b" in backend.name()
