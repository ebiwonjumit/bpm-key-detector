# Stage 2 Setup Notes

## Critical Setup Steps

### 1. Python Backend Setup

Before building the app, set up the Python backend:

```bash
cd stage2-gui/python-backend
./setup.sh
```

This creates a virtual environment and installs all dependencies locally.

### 2. Update Project Path (If Needed)

If your project is NOT located at `/Users/titoebiwonjumi/Documents/Codes/bpm-key-detector/`, you must update the path in **TWO** files:

#### A. AudioAnalyzer.swift (Line 52)

Open `BPMKeyDetector/BPMKeyDetector/AudioAnalyzer.swift` and update:

```swift
let projectPath = "/YOUR/ACTUAL/PATH/bpm-key-detector"
```

#### B. BPMKeyDetector.entitlements (Line 14)

Open `BPMKeyDetector/BPMKeyDetector/BPMKeyDetector.entitlements` and update:

```xml
<key>com.apple.security.temporary-exception.files.absolute-path.read-write</key>
<array>
    <string>/YOUR/ACTUAL/PATH/bpm-key-detector/stage2-gui/python-backend/</string>
</array>
```

### 3. Build in Xcode

```bash
open BPMKeyDetector.xcodeproj
```

Press `⌘R` to build and run.

## Why Absolute Paths?

macOS app sandboxing isolates apps in containers. When using `FileManager.default.homeDirectoryForCurrentUser`, it returns the sandboxed home directory:

```
/Users/USERNAME/Library/Containers/com.gentech.BPMKeyDetector/Data/
```

Not the actual home directory:

```
/Users/USERNAME/
```

Using absolute paths with proper entitlements bypasses this issue.

## Entitlements Explained

The `BPMKeyDetector.entitlements` file grants permissions:

- `app-sandbox`: Enables sandboxing (required for Mac App Store)
- `files.user-selected.read-only`: Access to files user selects
- `device.audio-input`: Microphone access
- `temporary-exception.files.absolute-path.read-only`: Read entire filesystem
- `temporary-exception.files.absolute-path.read-write`: Write to python-backend directory

## Alternative: Disable Sandboxing (Development Only)

For development, you can disable sandboxing:

1. Open `BPMKeyDetector.entitlements`
2. Change:
   ```xml
   <key>com.apple.security.app-sandbox</key>
   <false/>
   ```

**WARNING**: Apps without sandboxing cannot be distributed via Mac App Store.

## Troubleshooting

### Still Getting "Python executable not found"?

1. Verify Python backend is set up:
   ```bash
   ls -la /Users/titoebiwonjumi/Documents/Codes/bpm-key-detector/stage2-gui/python-backend/venv/bin/python3
   ```

2. Check Console output in Xcode for the actual paths being used

3. Verify entitlements are correct:
   ```bash
   codesign -d --entitlements - BPMKeyDetector.app
   ```

### Python Process Fails

If Python starts but analysis fails:

1. Test Python backend manually:
   ```bash
   /Users/titoebiwonjumi/Documents/Codes/bpm-key-detector/stage2-gui/python-backend/venv/bin/python3 \
   /Users/titoebiwonjumi/Documents/Codes/bpm-key-detector/stage2-gui/python-backend/analyzer.py --help
   ```

2. Check Python dependencies are installed:
   ```bash
   cd stage2-gui/python-backend
   source venv/bin/activate
   pip list
   ```

## Security Note

The temporary exceptions for absolute paths are for development convenience. For production distribution:

1. Bundle python-backend inside the app bundle
2. Use relative paths from `Bundle.main.bundlePath`
3. Remove temporary exception entitlements
4. Code sign properly for distribution

## Next Steps

After successful build:
- Test with audio files
- Test microphone recording
- Test batch processing
- Customize UI as needed
