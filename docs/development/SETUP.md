# Development Setup

## Requirements

- **Python 3.12+** (match statements, type params)
- **uv** package manager — `pip install uv`
- C compiler for pyswisseph — `xcode-select --install` (macOS)

## Install

```bash
git clone https://github.com/master12coder/vedic-ai-framework.git
cd vedic-ai-framework

# Development (all 3 packages linked via uv workspace)
uv sync

# Or with pip
pip install -e engine/ -e products/ -e apps/

# With LLM backends
pip install -e "products/[groq]"     # Free cloud
pip install -e "products/[ollama]"   # Free local
```

## Verify

```bash
jyotish --help                       # CLI works
jyotish chart --name "Test" --dob "01/01/2000" --tob "06:00" --place "Delhi" --gender Male
make test                            # 530+ tests pass
make all                             # lint + typecheck + test + audit
```

## Common Issues

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: jyotish_engine` | `uv sync` or `pip install -e engine/` |
| `ImportError: swisseph` | `pip install pyswisseph` (needs C compiler) |
| Font warnings in tests | Normal — NotoSansDevanagari in `assets/fonts/` |
| `make lint` fails | `pip install ruff` |

## Three Packages

| Package | Install | What |
|---------|---------|------|
| `jyotish-engine` | `pip install -e engine/` | Pure math, zero AI, standalone |
| `jyotish-products` | `pip install -e products/` | AI + plugins, needs engine |
| `jyotish` (apps) | `pip install -e apps/` | CLI + web + telegram, needs all |
