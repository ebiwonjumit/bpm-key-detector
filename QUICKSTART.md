# Quick Start Guide

Get up and running with Audio Analyzer in 5 minutes.

## Prerequisites

- **Python 3.8+** installed
- **pip** package manager
- **PortAudio** for microphone support (macOS: `brew install portaudio`)

## Installation

```bash
# Navigate to the CLI directory
cd audio-analyzer/stage1-cli

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## First Run

### Analyze an Audio File

```bash
python src/analyzer.py --file /path/to/your/song.mp3
```

### Record from Microphone

```bash
# Record for 10 seconds (default)
python src/analyzer.py --mic

# Record for 30 seconds
python src/analyzer.py --mic --duration 30
```

## Testing the Installation

```bash
# Run tests to verify everything works
pytest tests/
```

## Example Output

```
Analyzing: my_song.mp3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BPM: 128.5
Key: D minor

✓ Analysis complete
```

## Troubleshooting

### PortAudio errors on macOS
```bash
brew install portaudio
pip install --force-reinstall sounddevice
```

### Import errors
Make sure you're in the virtual environment:
```bash
source venv/bin/activate
```

### Permission errors (microphone)
Grant microphone permissions in System Preferences → Security & Privacy → Microphone

## Next Steps

- Read the full [Stage 1 README](stage1-cli/README.md)
- Check out the [Documentation](docs/)
- Explore the source code in `stage1-cli/src/`
- Run tests: `pytest tests/ -v`

## Need Help?

Open an issue or check the documentation in the `docs/` folder.