# Stage 1: CLI Audio Analyzer

Command-line tool for BPM and key detection.

## Features

- Analyze audio files (WAV, MP3, FLAC, AIFF)
- Record from microphone and analyze in real-time
- Detect BPM (tempo) with high accuracy
- Detect musical key (pitch class + major/minor)
- Simple, clean command-line interface

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- PortAudio (for microphone input)

### macOS Setup

```bash
# Install PortAudio for microphone support
brew install portaudio

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Linux Setup

```bash
# Install PortAudio
sudo apt-get install portaudio19-dev python3-pyaudio

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Analyze an Audio File

```bash
python src/analyzer.py --file path/to/audio.mp3
```

### Record from Microphone

```bash
# Record for 10 seconds (default)
python src/analyzer.py --mic

# Record for custom duration
python src/analyzer.py --mic --duration 30
```

### Options

```
--file PATH           Path to audio file to analyze
--mic                 Record from microphone
--duration SECONDS    Recording duration in seconds (default: 10)
--verbose            Show detailed analysis information
```

## Output Example

```
Analyzing: my_track.mp3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BPM: 128.5
Key: D minor
Confidence: High

Analysis complete in 2.3s
```

## Technical Details

### BPM Detection
- Uses librosa's tempo estimation
- Analyzes onset strength envelope
- Returns most likely BPM

### Key Detection
- Chromagram-based pitch class profile analysis
- Compares against major/minor templates
- Uses Krumhansl-Schmuckler key-finding algorithm

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Next Steps

- Optimize real-time microphone analysis
- Add batch processing for multiple files
- Improve key detection accuracy
- Add support for time signature detection