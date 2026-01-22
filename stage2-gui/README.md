# Stage 2: macOS GUI Application

A native macOS desktop app for BPM and key detection with a clean, minimal black and white interface.

## Features

- **Native macOS App** built with SwiftUI
- **Drag & Drop** audio file support
- **Microphone Recording** with configurable duration
- **Clean Interface** - minimal black and white design
- **Real-time Analysis** using Stage 1 CLI backend
- **Multiple Formats** - WAV, MP3, FLAC, AIFF, OGG, M4A

## Requirements

- **macOS**: 12.0 (Monterey) or later
- **Xcode**: 14.0 or later
- **Python**: 3.8+ (for backend analysis)
- **Stage 1 CLI**: Must be installed and configured

## Quick Start

### 1. Setup Python Backend

The GUI uses a bundled Python backend in the `python-backend/` directory:

```bash
cd stage2-gui/python-backend
./setup.sh
```

This will create a virtual environment and install all dependencies locally.

### 2. Open in Xcode

```bash
cd stage2-gui
open BPMKeyDetector.xcodeproj
```

### 3. Build and Run

Press `⌘R` in Xcode to build and run the app.

**Note**: Sandboxing is disabled for development simplicity. The app has full file system access to work with the Python backend.

## Project Structure

```
stage2-gui/
├── BPMKeyDetector/
│   ├── BPMKeyDetectorApp.swift    # App entry point
│   ├── ContentView.swift           # Main UI with File/Batch/Mic tabs
│   ├── AudioAnalyzer.swift         # Python bridge
│   ├── Info.plist                  # App configuration
│   └── Assets.xcassets/            # App assets
├── python-backend/                 # Bundled Python backend
│   ├── analyzer.py                 # CLI analyzer
│   ├── audio_processor.py          # Audio processing
│   ├── bpm_detector.py             # BPM detection
│   ├── key_detector.py             # Key detection
│   ├── requirements.txt            # Python dependencies
│   ├── setup.sh                    # Setup script
│   └── venv/                       # Virtual environment
└── BPMKeyDetector.xcodeproj/       # Xcode project
```

## Usage

### Analyze Single File

1. Switch to "File" tab
2. Drag & drop an audio file onto the drop zone
3. Or click "Choose File" to select a file
4. View BPM and Key results

### Batch Processing

1. Switch to "Batch" tab
2. Click "Choose Files" to select multiple audio files
3. Results appear in the table as files are analyzed
4. Click "Export CSV" to save results to a spreadsheet

### Record from Microphone

1. Switch to "Microphone" tab
2. Adjust recording duration (5-60 seconds)
3. Click "Start Recording"
4. View results after recording completes

## Design

Simple black and white interface:
- White background
- Black text and buttons
- Gray secondary elements
- Clean, minimal layout

## Troubleshooting

### Python Not Found

If you get "Python executable not found" errors:

1. Verify the python-backend setup:
   ```bash
   cd stage2-gui/python-backend
   ls -la venv/bin/python3
   ```

2. Re-run setup if needed:
   ```bash
   ./setup.sh
   ```

3. If using a different project location, update paths in `AudioAnalyzer.swift`:
   ```swift
   let projectPath = "\(homeDirectory)/Documents/Codes/bpm-key-detector"
   ```

### Sandboxing

Sandboxing is **disabled** for development convenience. This allows the app to access the Python backend without path restrictions.

- ✅ Works for development and personal use
- ⚠️ Cannot be distributed via Mac App Store
- 💡 Can be re-enabled later with proper entitlements for distribution

### Microphone Permission

Enable in System Settings → Privacy & Security → Microphone

### File Access Permission

When using drag & drop or file picker, macOS will automatically grant access to selected files.

## Next Steps

- Customize the design and styling
- Add more features (waveform, batch processing, etc.)
- Stage 3: DAW Plugin
