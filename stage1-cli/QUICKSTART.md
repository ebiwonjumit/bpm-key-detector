# Quick Start Guide - Stage 1 CLI

Get the BPM and Key Detector running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- macOS, Linux, or Windows
- Internet connection (for package installation)

## Installation

### Option 1: Automated Setup (macOS/Linux)

```bash
cd stage1-cli
./setup.sh
```

### Option 2: Manual Setup

```bash
cd stage1-cli

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### macOS: Install PortAudio

```bash
brew install portaudio
```

### Linux: Install PortAudio

```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

## Verify Installation

```bash
python verify_installation.py
```

You should see:
```
✅ All checks passed! Installation is complete.
```

## Usage

### 1. Analyze an Audio File

```bash
python src/analyzer.py --file path/to/song.mp3
```

**Example Output:**
```
Analyzing: song.mp3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃       Analysis Results              ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃  BPM:          128.5                ┃
┃  Key:          D minor              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Analysis completed in 2.3s
```

### 2. Record from Microphone

```bash
# Record for 10 seconds (default)
python src/analyzer.py --mic

# Record for 30 seconds
python src/analyzer.py --mic --duration 30
```

### 3. Verbose Mode (Detailed Info)

```bash
python src/analyzer.py --file song.mp3 --verbose
```

**Additional Output:**
- Confidence levels
- Scale notes
- Related keys
- Audio properties

## Supported Audio Formats

- WAV (.wav)
- MP3 (.mp3)
- FLAC (.flac)
- AIFF (.aiff, .aif)
- OGG (.ogg)
- M4A (.m4a)

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src --cov-report=html tests/

# Run specific test file
pytest tests/test_bpm_detector.py -v
```

## Common Issues

### "ModuleNotFoundError: No module named 'librosa'"

**Solution:** Make sure you activated the virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
```

### "PortAudio not found" or microphone errors

**macOS Solution:**
```bash
brew install portaudio
pip install --force-reinstall sounddevice
```

**Linux Solution:**
```bash
sudo apt-get install portaudio19-dev
pip install --force-reinstall sounddevice
```

### "Permission denied" when running scripts

**Solution:** Make scripts executable:
```bash
chmod +x setup.sh verify_installation.py src/analyzer.py
```

### Import errors in tests

**Solution:** Tests automatically add `src/` to the path. If issues persist:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

## Command Reference

```bash
# File analysis
python src/analyzer.py --file AUDIO_FILE [--verbose]

# Microphone recording
python src/analyzer.py --mic [--duration SECONDS] [--verbose]

# Help
python src/analyzer.py --help

# Run tests
pytest tests/                    # All tests
pytest tests/ -v                 # Verbose output
pytest tests/ -k test_detect     # Run specific tests
pytest --cov=src tests/          # With coverage

# Verify installation
python verify_installation.py
```

## Next Steps

1. **Try it out**: Analyze some of your own music files
2. **Run tests**: `pytest tests/` to ensure everything works
3. **Read the docs**: Check out `IMPLEMENTATION_SUMMARY.md` for technical details
4. **Customize**: Modify the source code to fit your needs
5. **Contribute**: Found a bug? Have an idea? Open an issue!

## Project Structure

```
stage1-cli/
├── src/                    # Source code
│   ├── analyzer.py         # Main CLI app
│   ├── audio_processor.py  # Audio I/O
│   ├── bpm_detector.py     # BPM detection
│   └── key_detector.py     # Key detection
├── tests/                  # Test suite
├── requirements.txt        # Dependencies
├── setup.sh               # Setup script
└── verify_installation.py  # Verification script
```

## Getting Help

- Read `README.md` for detailed documentation
- Check `IMPLEMENTATION_SUMMARY.md` for technical details
- Run `python src/analyzer.py --help` for CLI options
- Review test files for usage examples

## Performance Tips

- **Faster analysis**: Use shorter audio files or clips
- **Better accuracy**: Use high-quality audio (lossless formats preferred)
- **BPM detection**: Works best with clear, consistent beats
- **Key detection**: Works best with tonal, harmonic music

## What's Next?

After Stage 1 CLI is working:
- **Stage 2**: GUI Application (native macOS or cross-platform)
- **Stage 3**: DAW Plugin (VST3/AU using JUCE)

---

Happy analyzing! 🎵
