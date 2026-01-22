#!/bin/bash

# Setup script for BPM Key Detector Stage 1 CLI

set -e

echo "=========================================="
echo "BPM Key Detector - Stage 1 CLI Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if Python 3.8 or higher
required_version="3.8"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.8 or higher is required"
    exit 1
fi

echo "✓ Python version is compatible"
echo ""

# Check for PortAudio on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Checking for PortAudio (required for microphone support)..."
    if ! brew list portaudio &>/dev/null; then
        echo "PortAudio not found. Installing via Homebrew..."
        brew install portaudio
    else
        echo "✓ PortAudio is already installed"
    fi
    echo ""
fi

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Installation complete!"
echo "=========================================="
echo ""
echo "To get started:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the analyzer:"
echo "     python src/analyzer.py --file /path/to/audio.mp3"
echo "     python src/analyzer.py --mic"
echo ""
echo "  3. Run tests:"
echo "     pytest tests/"
echo ""
echo "Happy analyzing!"
