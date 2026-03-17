"""Jyotish exception hierarchy — single file.

Merged from jyotish.domain.exceptions with additional engine-specific classes.
"""

from __future__ import annotations


class JyotishError(Exception):
    """Base exception for all Jyotish errors."""


class ComputationError(JyotishError):
    """Error in astronomical computation."""


class EphemerisError(ComputationError):
    """Swiss Ephemeris computation failed."""


class BirthTimeError(ComputationError):
    """Birth time is invalid or near a lagna boundary."""


class ValidationError(JyotishError):
    """Error in input validation."""


class ConfigurationError(JyotishError):
    """Configuration is invalid or missing."""


class SafetyViolation(JyotishError):
    """Gemstone or interpretation safety violation."""


class ScriptureNotFound(JyotishError):
    """Scripture reference not found."""


class ChartNotFound(JyotishError):
    """Saved chart file not found."""


class GeocodingError(JyotishError):
    """Failed to resolve location coordinates."""


class LLMError(JyotishError):
    """Error communicating with LLM backend."""
