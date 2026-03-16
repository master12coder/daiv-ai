"""Custom exceptions for domain errors."""

from __future__ import annotations


class JyotishError(Exception):
    """Base exception for all Jyotish framework errors."""
    pass


class BirthTimeError(JyotishError):
    """Raised when birth time is invalid or near a lagna boundary."""
    pass


class GeocodingError(JyotishError):
    """Raised when place name cannot be resolved to coordinates."""
    pass


class LLMConnectionError(JyotishError):
    """Raised when LLM backend is unavailable or fails."""
    pass


class ScriptureNotFoundError(JyotishError):
    """Raised when a scripture reference cannot be found."""
    pass


class ValidationError(JyotishError):
    """Raised when input validation fails."""
    pass


class ConfigurationError(JyotishError):
    """Raised when configuration is invalid or missing."""
    pass


class EphemerisError(JyotishError):
    """Raised when Swiss Ephemeris computation fails."""
    pass
