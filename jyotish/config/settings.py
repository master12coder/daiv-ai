"""Config loader — reads from YAML + environment variable overrides."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class LLMConfig:
    """LLM backend configuration."""
    default_backend: str = "ollama"
    ollama_model: str = "qwen3:8b"
    ollama_base_url: str = "http://localhost:11434"
    groq_model: str = "llama-3.1-8b-instant"
    claude_model: str = "claude-sonnet-4-20250514"
    openai_model: str = "gpt-4o"


@dataclass
class OutputConfig:
    """Output preferences."""
    language: str = "both"
    format: str = "markdown"


@dataclass
class LearningConfig:
    """Pandit Ji learning system config."""
    data_dir: str = "data/pandit_corrections"
    min_confidence_for_rule: float = 0.5
    max_rules_in_prompt: int = 5


@dataclass
class ComputeConfig:
    """Chart computation config."""
    include_outer_planets: bool = False
    true_node: bool = True
    compute_upagrahas: bool = False


@dataclass
class Settings:
    """Master configuration — all framework settings."""
    ayanamsha: str = "lahiri"
    house_system: str = "whole_sign"
    default_timezone_offset: float = 5.5
    log_level: str = "INFO"
    log_json: bool = False
    llm: LLMConfig = field(default_factory=LLMConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    learning: LearningConfig = field(default_factory=LearningConfig)
    compute: ComputeConfig = field(default_factory=ComputeConfig)


_settings: Settings | None = None


def _find_config_path() -> Path:
    """Walk up from CWD looking for config.yaml, fall back to package default."""
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / "config.yaml"
        if candidate.exists():
            return candidate
    return Path(__file__).parent / "default.yaml"


def _env_override(key: str, default: str) -> str:
    """Check for JYOTISH_ prefixed env var override."""
    env_key = f"JYOTISH_{key.upper()}"
    return os.environ.get(env_key, default)


def load_settings(path: Path | str | None = None) -> Settings:
    """Load settings from YAML config + environment variable overrides."""
    global _settings
    if _settings is not None and path is None:
        return _settings

    config_path = Path(path) if path else _find_config_path()
    raw: dict[str, Any] = {}
    if config_path.exists():
        with open(config_path) as f:
            raw = yaml.safe_load(f) or {}

    llm_raw = raw.get("llm", {})
    llm = LLMConfig(
        default_backend=_env_override("LLM_BACKEND", llm_raw.get("default_backend", "ollama")),
        ollama_model=_env_override("LLM_MODEL", llm_raw.get("ollama", {}).get("model", "qwen3:8b")),
        ollama_base_url=llm_raw.get("ollama", {}).get("base_url", "http://localhost:11434"),
        groq_model=llm_raw.get("groq", {}).get("model", "llama-3.1-8b-instant"),
        claude_model=_env_override("CLAUDE_MODEL", llm_raw.get("claude", {}).get("model", "claude-sonnet-4-20250514")),
        openai_model=llm_raw.get("openai", {}).get("model", "gpt-4o"),
    )

    output_raw = raw.get("output", {})
    output = OutputConfig(
        language=output_raw.get("language", "both"),
        format=output_raw.get("format", "markdown"),
    )

    learning_raw = raw.get("learning", {})
    learning = LearningConfig(
        data_dir=learning_raw.get("data_dir", "data/pandit_corrections"),
        min_confidence_for_rule=learning_raw.get("min_confidence_for_rule", 0.5),
        max_rules_in_prompt=learning_raw.get("max_rules_in_prompt", 5),
    )

    compute_raw = raw.get("compute", {})
    compute = ComputeConfig(
        include_outer_planets=compute_raw.get("include_outer_planets", False),
        true_node=compute_raw.get("true_node", True),
        compute_upagrahas=compute_raw.get("compute_upagrahas", False),
    )

    _settings = Settings(
        ayanamsha=_env_override("AYANAMSHA", raw.get("ayanamsha", "lahiri")),
        house_system=raw.get("house_system", "whole_sign"),
        default_timezone_offset=raw.get("default_timezone_offset", 5.5),
        log_level=_env_override("LOG_LEVEL", raw.get("log_level", "INFO")),
        log_json=raw.get("log_json", False),
        llm=llm,
        output=output,
        learning=learning,
        compute=compute,
    )
    return _settings


def get_settings() -> Settings:
    """Get cached settings instance."""
    return load_settings()


def reset_settings() -> None:
    """Reset cached settings (useful for testing)."""
    global _settings
    _settings = None
