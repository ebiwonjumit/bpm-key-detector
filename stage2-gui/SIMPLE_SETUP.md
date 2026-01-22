# Stage 2 GUI - Simple Setup Guide

## Quick 3-Step Setup

### Step 1: Setup Python Backend

```bash
cd stage2-gui/python-backend
./setup.sh
```

This installs all Python dependencies locally.

### Step 2: Open in Xcode

```bash
cd ..
open BPMKeyDetector.xcodeproj
```

### Step 3: Build and Run

In Xcode, press `⌘R` to build and run.

That's it! 🎉

## What We Changed

**Disabled sandboxing** for simplicity during development:
- Changed `com.apple.security.app-sandbox` from `true` to `false`
- Removed complex path exceptions
- App now has full file system access

This means:
- ✅ No more sandboxing path issues
- ✅ Python backend works automatically
- ✅ FileManager.homeDirectory works correctly
- ⚠️ Cannot distribute on Mac App Store (not needed for development)

## Verify It Works

When the app starts, check Xcode Console:

**Good output:**
```
Python path: /Users/USERNAME/Documents/Codes/bpm-key-detector/stage2-gui/python-backend/venv/bin/python3
Analyzer script: /Users/USERNAME/Documents/Codes/bpm-key-detector/stage2-gui/python-backend/analyzer.py
```

**No warnings!**

## Troubleshooting

### Python Backend Not Found?

Run setup again:
```bash
cd stage2-gui/python-backend
./setup.sh
```

### Clean Build

If still having issues:
1. In Xcode: Product → Clean Build Folder (⇧⌘K)
2. Rebuild: ⌘B
3. Run: ⌘R

## Done!

Your Stage 2 GUI is ready to use. Drop an audio file and analyze! 🎵
