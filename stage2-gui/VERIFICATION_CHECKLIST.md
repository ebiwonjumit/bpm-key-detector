# Stage 2 GUI - Verification Checklist

Use this checklist to verify the Stage 2 GUI is properly configured and working.

## Setup Verification

### ✅ Python Backend

- [ ] Python backend directory exists:
  ```bash
  ls -la stage2-gui/python-backend/
  ```

- [ ] Virtual environment created:
  ```bash
  ls -la stage2-gui/python-backend/venv/bin/python3
  ```

- [ ] Dependencies installed:
  ```bash
  stage2-gui/python-backend/venv/bin/python3 -c "import librosa; print('✓ librosa installed')"
  ```

- [ ] Analyzer works standalone:
  ```bash
  stage2-gui/python-backend/venv/bin/python3 stage2-gui/python-backend/analyzer.py --help
  ```

### ✅ Path Configuration

- [ ] Project path in `AudioAnalyzer.swift` (line 52) matches your setup:
  ```bash
  grep "let projectPath" stage2-gui/BPMKeyDetector/BPMKeyDetector/AudioAnalyzer.swift
  ```
  Should show: `let projectPath = "/Users/YOUR_USERNAME/Documents/Codes/bpm-key-detector"`

- [ ] Entitlements path matches your setup:
  ```bash
  grep -A2 "absolute-path.read-write" stage2-gui/BPMKeyDetector/BPMKeyDetector/BPMKeyDetector.entitlements
  ```
  Should include your actual project path.

### ✅ Xcode Project

- [ ] Project opens without errors:
  ```bash
  open stage2-gui/BPMKeyDetector.xcodeproj
  ```

- [ ] Build succeeds (⌘B in Xcode)

- [ ] No compiler errors or warnings

## Runtime Verification

### ✅ Console Output

When the app starts, check Xcode Console for:

- [ ] Python path printed (should be your actual path, NOT sandboxed):
  ```
  Python path: /Users/USERNAME/Documents/Codes/bpm-key-detector/stage2-gui/python-backend/venv/bin/python3
  ```

- [ ] No "WARNING: Python executable not found" message

- [ ] No "WARNING: Analyzer script not found" message

### ✅ File Analysis

- [ ] Drag and drop an audio file (MP3, WAV, etc.)

- [ ] File is accepted (no error message)

- [ ] Analysis completes successfully

- [ ] BPM and Key are displayed

- [ ] Confidence levels shown

### ✅ Batch Processing

- [ ] Switch to "Batch" tab

- [ ] Click "Choose Files" and select multiple audio files

- [ ] Files appear in results table

- [ ] Each file shows BPM and Key

- [ ] "Export CSV" button works

### ✅ Microphone Recording

- [ ] Switch to "Microphone" tab

- [ ] System prompts for microphone permission (first time)

- [ ] Click "Start Recording"

- [ ] Timer counts up

- [ ] Recording completes after set duration

- [ ] Results are displayed

## Error Scenarios

### ❌ "Python executable not found"

**Symptom**: Warning in Console about Python not found

**Check**:
1. Python backend setup completed?
   ```bash
   ls -la stage2-gui/python-backend/venv/bin/python3
   ```
2. Path in `AudioAnalyzer.swift` correct?
3. Entitlements allow access to that path?

**Fix**: See [SETUP_NOTES.md](SETUP_NOTES.md)

### ❌ "Analysis failed. Please check the audio file format."

**Symptom**: Error message after dropping file

**Check**:
1. Run Python analyzer manually to see actual error:
   ```bash
   stage2-gui/python-backend/venv/bin/python3 \
   stage2-gui/python-backend/analyzer.py --file /path/to/test.mp3 --json
   ```

2. Check file format is supported (WAV, MP3, FLAC, etc.)

3. Verify file isn't corrupted

**Fix**: Check Python backend dependencies and file permissions

### ❌ Sandboxed Path in Console

**Symptom**: Console shows:
```
Python path: /Users/USERNAME/Library/Containers/com.gentech.BPMKeyDetector/...
```

**Check**: Still using relative path in `AudioAnalyzer.swift`

**Fix**: Use absolute path as shown in [SETUP_NOTES.md](SETUP_NOTES.md)

### ❌ Microphone Not Working

**Symptom**: Recording fails or no permission prompt

**Check**:
1. Entitlements include audio input permission
2. System Settings → Privacy & Security → Microphone
3. App has permission to access microphone

**Fix**: Grant microphone permission in System Settings

## Performance Checks

### ⚡ Analysis Speed

- [ ] Single file analysis: ~2-5 seconds for 3-minute song

- [ ] Batch processing: Similar per-file time

- [ ] No freezing or UI lockups

- [ ] Progress indicators work

### 💾 Resource Usage

- [ ] CPU usage reasonable during analysis

- [ ] Memory usage stable

- [ ] No memory leaks after multiple analyses

## Final Checklist

Before considering setup complete:

- [x] Python backend installed and verified
- [x] Paths configured correctly in code
- [x] App builds without errors
- [x] File analysis works
- [x] Batch processing works
- [x] Microphone recording works
- [x] No console warnings
- [x] UI responsive

## Success!

If all items are checked, your Stage 2 GUI is properly configured and ready to use! 🎉

## Next Steps

- Customize the UI design
- Add more features
- Test with various audio formats
- Share your music analysis results!
