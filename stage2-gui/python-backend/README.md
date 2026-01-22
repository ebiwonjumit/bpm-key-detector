# Stage 2 Python Backend

This directory contains the Python backend used by the Stage 2 macOS GUI application.

## Overview

The Stage 2 GUI app uses a bundled Python backend to perform audio analysis. This avoids sandboxing issues by keeping all Python dependencies within the Stage 2 directory.

## Contents

- `analyzer.py` - Main CLI analyzer (copied from Stage 1)
- `audio_processor.py` - Audio loading and recording module
- `bpm_detector.py` - BPM detection algorithm
- `key_detector.py` - Musical key detection algorithm
- `requirements.txt` - Python dependencies
- `venv/` - Python virtual environment
- `setup.sh` - Setup script

## Setup

Run the setup script to create the virtual environment and install dependencies:

```bash
cd stage2-gui/python-backend
./setup.sh
```

This will:
1. Create a Python virtual environment in `venv/`
2. Install all required dependencies from `requirements.txt`

## Dependencies

- librosa - Audio analysis
- soundfile - Audio file I/O
- sounddevice - Microphone recording
- numpy - Numerical computing
- scipy - Scientific computing
- rich - Terminal formatting (for CLI mode)

## Integration with GUI

The Stage 2 GUI app (`AudioAnalyzer.swift`) calls this Python backend by:

1. Executing the Python interpreter: `venv/bin/python3`
2. Running the analyzer script: `analyzer.py`
3. Passing command-line arguments: `--file <path>` or `--mic --duration <seconds>`
4. Using `--json` flag for structured output
5. Parsing the JSON response

## File Synchronization

This directory is kept in sync with Stage 1 CLI:
- Copy updated files from `stage1-cli/src/` when Stage 1 is modified
- Re-run `./setup.sh` if `requirements.txt` changes

## Troubleshooting

### Python executable not found

If the GUI shows "Python executable not found":

1. Verify the virtual environment exists:
   ```bash
   ls -la venv/bin/python3
   ```

2. Re-run setup if needed:
   ```bash
   ./setup.sh
   ```

### Module import errors

If you see import errors when running the analyzer:

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Microphone access

If microphone recording fails, ensure:
- Python has microphone permissions in System Settings
- sounddevice is properly installed
- Your microphone is connected and working

## Notes

- This is a standalone copy of the Stage 1 backend
- Updates to Stage 1 CLI should be manually synced here
- The virtual environment is specific to this directory
- All paths in `AudioAnalyzer.swift` point to this directory
