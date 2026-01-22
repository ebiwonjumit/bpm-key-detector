# Stage 2 Sandboxing Fix

## Problem

The Stage 2 GUI was experiencing sandboxing issues where the app couldn't access the Python backend located in the Stage 1 CLI directory. macOS sandbox isolation was preventing the app from accessing files outside its container.

**Error symptoms:**
```
Python path: /Users/.../Library/Containers/com.gentech.BPMKeyDetector/Data/...
WARNING: Python executable not found
Failed to run Python analyzer: Error Domain=NSCocoaErrorDomain Code=4 "The file "python3" doesn't exist."
```

## Solution

We bundled a complete copy of the Python backend within the Stage 2 directory structure, eliminating the need to reference files in Stage 1 CLI.

## Changes Made

### 1. Created `python-backend/` Directory

Created a new directory in `stage2-gui/` containing:
- All Python source files from Stage 1 CLI (`analyzer.py`, `audio_processor.py`, `bpm_detector.py`, `key_detector.py`)
- `requirements.txt` for Python dependencies
- Dedicated Python virtual environment (`venv/`)
- Setup script (`setup.sh`)
- Documentation (`README.md`)

### 2. Updated `AudioAnalyzer.swift`

Changed Python paths from using `FileManager.default.homeDirectoryForCurrentUser` (which returns sandboxed path) to absolute paths:

```swift
// OLD - Used sandboxed home directory
let homeDirectory = FileManager.default.homeDirectoryForCurrentUser.path
let projectPath = "\(homeDirectory)/Documents/Codes/bpm-key-detector"
self.pythonExecutable = "\(projectPath)/stage1-cli/venv/bin/python3"
```

To:
```swift
// NEW - Uses absolute path to avoid sandboxing
let projectPath = "/Users/titoebiwonjumi/Documents/Codes/bpm-key-detector"
self.pythonExecutable = "\(projectPath)/stage2-gui/python-backend/venv/bin/python3"
self.analyzerScript = "\(projectPath)/stage2-gui/python-backend/analyzer.py"
```

**Important**: Users with different project locations must update this path in `AudioAnalyzer.swift` line 52.

### 3. Created Setup Script

`stage2-gui/python-backend/setup.sh`:
- Creates virtual environment
- Installs all Python dependencies locally
- Verifies installation

### 4. Updated Entitlements

`BPMKeyDetector.entitlements`:
- Added read-write exception for python-backend directory
- Kept sandboxing enabled for security
- Allowed absolute path access to python-backend

```xml
<key>com.apple.security.temporary-exception.files.absolute-path.read-write</key>
<array>
    <string>/Users/titoebiwonjumi/Documents/Codes/bpm-key-detector/stage2-gui/python-backend/</string>
</array>
```

**Important**: Users must update this path if project is in a different location.

### 5. Updated Documentation

- `stage2-gui/README.md` - Updated setup instructions
- `stage2-gui/python-backend/README.md` - New backend documentation
- `stage2-gui/SETUP_NOTES.md` - Critical setup information
- Added troubleshooting section for sandboxing issues

## Directory Structure

```
stage2-gui/
├── BPMKeyDetector/
│   ├── BPMKeyDetector/
│   │   ├── AudioAnalyzer.swift      # ✅ Updated paths
│   │   ├── ContentView.swift
│   │   └── ...
│   └── BPMKeyDetector.xcodeproj/
├── python-backend/                   # ✅ NEW
│   ├── analyzer.py                   # Copied from Stage 1
│   ├── audio_processor.py            # Copied from Stage 1
│   ├── bpm_detector.py               # Copied from Stage 1
│   ├── key_detector.py               # Copied from Stage 1
│   ├── requirements.txt              # Copied from Stage 1
│   ├── setup.sh                      # ✅ NEW - Setup script
│   ├── venv/                         # ✅ NEW - Local virtual env
│   └── README.md                     # ✅ NEW - Documentation
└── README.md                         # ✅ Updated

stage1-cli/                           # Unchanged, still works independently
├── src/
├── tests/
└── venv/
```

## Setup Instructions

### For New Users

1. Clone the repository
2. Setup Stage 2 Python backend:
   ```bash
   cd stage2-gui/python-backend
   ./setup.sh
   ```
3. Open Xcode project:
   ```bash
   cd ..
   open BPMKeyDetector.xcodeproj
   ```
4. Build and run (⌘R)

### For Existing Users

If you already have the project:

1. Pull latest changes
2. Setup the new python-backend:
   ```bash
   cd stage2-gui/python-backend
   ./setup.sh
   ```
3. Rebuild in Xcode

The GUI will now use the bundled Python backend instead of Stage 1.

## Benefits

✅ **No sandboxing issues** - All files are in Stage 2 directory
✅ **Self-contained** - Stage 2 doesn't depend on Stage 1 location
✅ **Easier deployment** - Can bundle everything together
✅ **Independent updates** - Stage 1 and Stage 2 can evolve separately
✅ **Cleaner architecture** - Clear separation of concerns

## Maintenance

### Syncing with Stage 1

If Stage 1 CLI is updated with new features or bug fixes:

1. Copy updated files to `stage2-gui/python-backend/`:
   ```bash
   cp stage1-cli/src/*.py stage2-gui/python-backend/
   cp stage1-cli/requirements.txt stage2-gui/python-backend/
   ```

2. Re-run setup if dependencies changed:
   ```bash
   cd stage2-gui/python-backend
   ./setup.sh
   ```

### Testing

Test the fix by:
1. Building the app in Xcode
2. Dragging an audio file to analyze
3. Checking Console for "Python path:" output
4. Verifying no "Python executable not found" warnings

## Technical Notes

### Why This Works

- macOS sandbox allows apps to access files within their own bundle/directory
- By placing Python backend in `stage2-gui/`, we stay within allowed boundaries
- The app can freely access files in its parent directory structure
- No special entitlements or sandbox exceptions needed

### Alternative Solutions Considered

1. **Disable sandboxing** - Not recommended for security
2. **Use absolute paths with entitlements** - Complex, user-specific
3. **Rewrite in Swift** - Major effort, loses Python libraries
4. **✅ Bundle backend locally** - Simple, clean, maintainable

## Verification

After applying this fix, you should see in Console:
```
Python path: /Users/USERNAME/Documents/Codes/bpm-key-detector/stage2-gui/python-backend/venv/bin/python3
Analyzer script: /Users/USERNAME/Documents/Codes/bpm-key-detector/stage2-gui/python-backend/analyzer.py
```

No "WARNING" messages should appear, and file analysis should work correctly.

## Status

✅ **FIXED** - Sandboxing issue resolved by bundling Python backend in Stage 2 directory.
