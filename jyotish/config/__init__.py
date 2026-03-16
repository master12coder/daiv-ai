"""Configuration management — backward-compatible re-export."""

from jyotish.config.settings import load_settings, get_settings, reset_settings, Settings

# Backward compatibility: re-export the old config.py functions
from jyotish.config._legacy import load_config, get
