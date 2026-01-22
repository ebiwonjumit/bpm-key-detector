# Batch Processing Guide

Analyze multiple audio files at once with Stage 1 CLI and Stage 2 GUI.

## Overview

Batch processing allows you to analyze entire music libraries, folders, or multiple files simultaneously, perfect for DJs organizing their collection or producers cataloging samples.

---

## Stage 1: CLI Batch Processing

### Methods

**1. Batch Mode - Multiple Files**
```bash
python src/analyzer.py --batch song1.mp3 song2.mp3 song3.mp3
```

**2. Wildcard Patterns**
```bash
# All MP3 files in current directory
python src/analyzer.py --batch *.mp3

# All files matching pattern
python src/analyzer.py --batch track_*.wav
```

**3. Directory Mode - Analyze Entire Folder**
```bash
python src/analyzer.py --dir /path/to/music/folder
```

### Export Results

**CSV Format** (Great for spreadsheets):
```bash
python src/analyzer.py --batch *.mp3 --output results.csv
```

Output format:
```csv
file,bpm,bpm_confidence,bpm_confidence_level,key,mode,key_string,key_confidence,key_confidence_level,duration,analysis_time
song1.mp3,128.5,0.85,High,D,minor,D minor,0.72,High,180.5,2.3
song2.mp3,120.0,0.92,High,C,major,C major,0.88,High,210.2,2.1
```

**JSON Format** (Great for automation):
```bash
python src/analyzer.py --batch *.mp3 --output results.json
```

Output format:
```json
[
  {
    "file": "song1.mp3",
    "bpm": 128.5,
    "bpm_confidence_level": "High",
    "key_string": "D minor",
    ...
  }
]
```

### Error Handling

**Continue on Error**:
```bash
python src/analyzer.py --batch *.mp3 --continue-on-error
```

This will:
- Skip files that fail to analyze
- Continue processing remaining files
- Show summary of failed files at the end

**Default Behavior** (stop on error):
```bash
python src/analyzer.py --batch *.mp3
```

Stops immediately if any file fails.

### Examples

**Analyze entire music collection**:
```bash
cd ~/Music
python /path/to/analyzer.py --dir . --output library_analysis.csv
```

**Analyze specific genre**:
```bash
python src/analyzer.py --dir ~/Music/Electronic --output electronic.csv
```

**Quick batch with error recovery**:
```bash
python src/analyzer.py --batch *.{mp3,wav,flac} --continue-on-error
```

### Output Display

**Batch Summary Table**:
```
Batch Analysis: 10 files
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/10] Analyzing: song1.mp3
  BPM: 128.5 | Key: D minor

[2/10] Analyzing: song2.mp3
  BPM: 120.0 | Key: C major

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Completed: 10/10 files

┏━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ File        ┃  BPM ┃ Key     ┃ BPM Conf ┃ Key Conf ┃
┡━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ song1.mp3   │ 128.5│ D minor │   High   │   High   │
│ song2.mp3   │ 120.0│ C major │   High   │   High   │
└─────────────┴──────┴─────────┴──────────┴──────────┘
```

---

## Stage 2: GUI Batch Processing

### How to Use

1. **Launch App**
   - Open BPM Key Detector

2. **Switch to Batch Tab**
   - Click "Batch" tab in the toolbar

3. **Select Files**
   - Click "Choose Files" button
   - Select multiple audio files (⌘-click or Shift-click)
   - Click "Open"

4. **View Results**
   - Results appear in table as files are analyzed
   - Shows filename, BPM, key, and confidence levels

5. **Export Results**
   - Click "Export CSV" button
   - Choose save location
   - Import into Excel, Numbers, or database

### Features

**Results Table**:
- Scrollable list of all analyzed files
- Shows BPM, key, and confidence for each file
- Clean, easy-to-read format

**Actions**:
- **Clear Results**: Remove all results and start fresh
- **Add More Files**: Add additional files to current batch
- **Export CSV**: Save results to spreadsheet

**CSV Export Format**:
```csv
Filename,BPM,Key,BPM Confidence,Key Confidence
track1.mp3,128.5,D minor,High,High
track2.mp3,120.0,C major,High,Medium
```

---

## Performance

### Stage 1 CLI

**Speed**:
- ~2-5 seconds per file (depends on duration)
- Sequential processing
- Memory efficient

**Recommended for**:
- Large batches (100+ files)
- Automated workflows
- Server/background processing
- Integration with other tools

### Stage 2 GUI

**Speed**:
- ~2-5 seconds per file
- Parallel analysis (multiple files at once)
- Visual progress feedback

**Recommended for**:
- Medium batches (10-50 files)
- Visual feedback needed
- Interactive organization
- Desktop workflow

---

## Use Cases

### DJ Library Organization

**Sort by BPM**:
```bash
python src/analyzer.py --dir ~/Music/DJ --output dj_library.csv
```

Then open in Excel and sort by BPM column.

**Find Compatible Tracks**:
1. Analyze all tracks
2. Sort CSV by key
3. Group tracks in compatible keys (using Circle of Fifths)

### Producer Sample Management

**Catalog Sample Pack**:
```bash
python src/analyzer.py --dir ~/Samples/Drums --output drums_catalog.csv
```

**Find Samples in Specific Key**:
1. Analyze sample library
2. Filter CSV by key column
3. Find samples matching your project key

### Music Library Analysis

**Generate Library Statistics**:
```bash
python src/analyzer.py --dir ~/Music --output library.csv
```

Then use spreadsheet to:
- Count songs by BPM range
- Count songs by key
- Find most common tempos
- Identify duplicates

---

## Tips & Best Practices

### CLI Tips

1. **Use absolute paths** for reliability
   ```bash
   python src/analyzer.py --dir /Users/you/Music --output /Users/you/results.csv
   ```

2. **Test with small batch first**
   ```bash
   python src/analyzer.py --batch *.mp3 | head -20
   ```

3. **Always use --continue-on-error** for large batches
   ```bash
   python src/analyzer.py --dir . --continue-on-error --output results.csv
   ```

4. **Pipe to file for large outputs**
   ```bash
   python src/analyzer.py --batch *.mp3 > batch_output.txt
   ```

### GUI Tips

1. **Start small**: Test with 5-10 files first
2. **Clear results**: Clear between different batches
3. **Export frequently**: Save results as you go
4. **Use meaningful names**: Name exported CSV files clearly

### General Tips

1. **Organize by folder**: Keep similar tracks together
2. **Check file formats**: Ensure all files are supported
3. **Backup first**: Always have backups before batch processing
4. **Validate results**: Spot-check a few results for accuracy

---

## Troubleshooting

### "No audio files found"

**Problem**: Directory mode found no files

**Solution**:
- Check path is correct
- Ensure files have supported extensions (.mp3, .wav, .flac, etc.)
- Check file permissions

### Batch processing stops early

**Problem**: Process stops after first error

**Solution**: Use `--continue-on-error` flag
```bash
python src/analyzer.py --batch *.mp3 --continue-on-error
```

### Out of memory

**Problem**: Too many files at once

**Solution**:
- Process in smaller batches
- Close other applications
- Use CLI instead of GUI for very large batches

### Slow performance

**Problem**: Batch taking too long

**Tips**:
- Close other applications
- Use CLI for large batches (more efficient)
- Process smaller batches
- Upgrade Python environment

---

## Automation Examples

### Cron Job (Automated Analysis)

```bash
#!/bin/bash
# Analyze new music daily

cd ~/Music/New
python /path/to/analyzer.py --dir . --output analysis_$(date +%Y%m%d).csv
```

### Python Script Integration

```python
import subprocess
import json

# Analyze files via CLI
result = subprocess.run([
    'python', 'src/analyzer.py',
    '--batch', '*.mp3',
    '--json'
], capture_output=True, text=True)

# Parse results
data = json.loads(result.stdout)

# Process results
for track in data:
    print(f"{track['file']}: {track['bpm']} BPM, {track['key_string']}")
```

### Shell Script Workflow

```bash
#!/bin/bash
# Batch analyze and organize by BPM

# Analyze
python src/analyzer.py --dir ~/Music --output results.csv

# Create BPM folders
mkdir -p ~/Music/Organized/{Slow,Medium,Fast}

# Parse CSV and move files (requires csvkit)
# This is pseudo-code - customize as needed
csvgrep -c bpm -r "^[4-9][0-9]\.[0-9]$" results.csv | # Slow (<100)
    csvcut -c file | tail -n +2 | xargs -I {} mv ~/Music/{} ~/Music/Organized/Slow/
```

---

## Performance Benchmarks

**CLI Batch Processing**:
- 10 files (~3 min each): ~30 seconds total
- 100 files: ~5 minutes total
- 1000 files: ~50 minutes total

**GUI Batch Processing**:
- 10 files: ~30 seconds (parallel)
- 50 files: ~3 minutes
- 100+ files: Use CLI instead

**Export Speed**:
- CSV: Instant (any size)
- JSON: Instant (any size)

---

## Keyboard Shortcuts (GUI)

- `⌘O`: Open file picker
- `⌘⇧O`: Open multiple files
- `⌘S`: Export results
- `⌘K`: Clear results
- `Tab`: Switch between tabs

---

**Happy batch processing!** 🎵📊
