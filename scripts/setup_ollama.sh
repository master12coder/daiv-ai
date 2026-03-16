#!/bin/bash
# One-command Ollama setup for Vedic AI Framework

set -e

echo "=== Vedic AI Framework — Ollama Setup ==="
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Download Ollama from: https://ollama.com/download"
        echo "Or install via: brew install ollama"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://ollama.com/install.sh | sh
    fi
    echo ""
    echo "After installing, run this script again."
    exit 1
fi

echo "✓ Ollama found: $(ollama --version)"

# Start Ollama server if not running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Starting Ollama server..."
    ollama serve &
    sleep 3
fi

echo "✓ Ollama server running"

# Pull the recommended model
echo ""
echo "Pulling qwen3:8b (recommended for Hindi+English)..."
echo "This may take 5-10 minutes on first download (~5GB)"
echo ""
ollama pull qwen3:8b

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Test with:"
echo "  jyotish report --name 'Test' --dob '13/03/1989' --tob '12:17' --place 'Varanasi' --llm ollama"
