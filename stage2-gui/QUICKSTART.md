# Quick Start Guide - Stage 2 GUI

Get the macOS desktop app running in 10 minutes!

## Prerequisites

✅ macOS 12.0 (Monterey) or later
✅ Xcode 14.0 or later installed
✅ Stage 1 CLI working (from Stage 1 setup)

## Step 1: Verify Stage 1 Backend

```bash
cd ../stage1-cli
source venv/bin/activate
python src/analyzer.py --file ../samples/test.mp3
```

If this works, you're ready! If not, run `./setup.sh` first.

## Step 2: Create Xcode Project

### Method A: Fresh Project (Recommended)

1. **Open Xcode** → Create New Project
2. Choose **macOS** → **App**
3. Settings:
   - Product Name: `BPMKeyDetector`
   - Interface: **SwiftUI**
   - Language: **Swift**
4. Save to: `bpm-key-detector/stage2-gui/`
5. **Delete** the auto-generated `BPMKeyDetector` folder
6. Keep the existing `BPMKeyDetector` folder with our files
7. In Xcode, add files to project:
   - Right-click project → "Add Files"
   - Select all `.swift` files
   - Add `Info.plist` and `.entitlements`

### Method B: Use Provided Files

All source files are ready in `BPMKeyDetector/` folder:
- ✅ BPMKeyDetectorApp.swift
- ✅ ContentView.swift
- ✅ AudioAnalyzer.swift
- ✅ Info.plist
- ✅ Assets.xcassets/

Just create the Xcode project wrapper.

## Step 3: Configure Python Path

Edit `AudioAnalyzer.swift` (line ~35):

```swift
// Update these paths to match your system
self.pythonExecutable = "/absolute/path/to/stage1-cli/venv/bin/python3"
self.analyzerScript = "/absolute/path/to/stage1-cli/src/analyzer.py"
```

Find your paths:
```bash
cd ../stage1-cli
echo "Python: $(pwd)/venv/bin/python3"
echo "Script: $(pwd)/src/analyzer.py"
```

## Step 4: Build and Run

In Xcode:
1. Select **My Mac** as target
2. Press **⌘R** (or Product → Run)
3. Grant microphone permission if prompted

## Step 5: Test It!

### Test File Analysis:
1. Drag an audio file to the drop zone
2. Or click "Choose File"
3. Wait for analysis (~2-5 seconds)
4. See BPM and Key results!

### Test Microphone:
1. Click "Microphone" tab
2. Adjust duration slider
3. Click "Start Recording"
4. Make some noise! (or play music)
5. Wait for results

## Troubleshooting

### ❌ "Python not found"

**Fix**: Update paths in `AudioAnalyzer.swift`

```bash
# Find the correct path
which python3  # System Python (DON'T use this)
cd ../stage1-cli && pwd  # Use this path + venv/bin/python3
```

### ❌ "Cannot parse module"

**Fix**: Clean and rebuild
- Product → Clean Build Folder (⌘⇧K)
- Product → Build (⌘B)

### ❌ "Microphone permission denied"

**Fix**: Grant permission
- System Settings → Privacy & Security → Microphone
- Enable for "BPMKeyDetector"
- Restart app

### ❌ "File access denied"

**Fix**: Sandboxing issue
- Make sure you use the file picker or drag-and-drop
- Don't try to access files outside user selection

### ❌ Analysis fails with no error

**Fix**: Test Python CLI directly
```bash
cd ../stage1-cli
source venv/bin/activate
python src/analyzer.py --file test.mp3 --json
```

Should output JSON. If not, Stage 1 has issues.

## Common Issues

### Issue: App crashes on launch

**Cause**: Missing files or incorrect target membership

**Fix**:
1. Select each `.swift` file
2. File Inspector → Target Membership
3. Check "BPMKeyDetector"

### Issue: UI doesn't update after analysis

**Cause**: SwiftUI state not updating

**Fix**: Verify `@ObservedObject` and `@Published` are used correctly

### Issue: No results displayed

**Cause**: JSON parsing failed

**Fix**:
1. Check Python CLI JSON output format
2. Add debug logging in `parseAnalysisOutput`

## Next Steps

1. ✅ **Verify it works** - Test file and mic
2. 🎨 **Customize design** - Update colors, fonts, layout
3. ➕ **Add features** - Waveform, batch processing, export
4. 📦 **Package** - Create .app bundle for distribution

## Customization Ideas

### Change Colors:
Edit `ContentView.swift`:
```swift
.background(Color.white)  // Change to any color
.foregroundColor(.black)  // Change text color
```

### Change Window Size:
Edit `BPMKeyDetectorApp.swift`:
```swift
.frame(minWidth: 600, minHeight: 500)  // Adjust dimensions
```

### Add Your Logo:
1. Add image to `Assets.xcassets`
2. Add to HeaderView:
```swift
Image("logo")
    .resizable()
    .frame(width: 32, height: 32)
```

## Development Tips

### Hot Reload:
- Edit UI in `ContentView.swift`
- Save (⌘S)
- Xcode auto-reloads preview (if enabled)

### Debug Logging:
Add `print()` statements:
```swift
print("Analysis result: \(result)")
```
View in Xcode console (⌘⇧C)

### Test Without Mic:
Use file analysis to test without needing microphone permission

## Distribution

### For Friends/Testing:
1. Archive: Product → Archive
2. Export → Export as macOS App
3. Share the .app file
4. Note: Recipients need to right-click → Open first time

### For Public Release:
1. Requires Apple Developer account ($99/year)
2. Archive → Distribute
3. Notarize with Apple
4. Create installer (.dmg) with:
   - `create-dmg` tool
   - Or Disk Utility

## Performance Tips

- **Faster Analysis**: Use shorter audio clips
- **Reduce Memory**: Close other apps during testing
- **Better Accuracy**: Use high-quality audio files
- **Mic Recording**: Record in quiet environment

## Getting Help

- 📖 Check `README.md` for detailed docs
- 🔧 Check `CREATE_PROJECT.md` for project setup
- 📋 Check `IMPLEMENTATION_SUMMARY.md` for architecture
- 🐛 Check Xcode console for error messages

## Success Checklist

- [ ] Stage 1 CLI working
- [ ] Xcode project created
- [ ] Python paths configured
- [ ] App builds successfully
- [ ] File analysis works
- [ ] Microphone recording works
- [ ] Results display correctly

If all checked, you're good to go! 🎉

---

**Stuck?** Check the console output (⌘⇧C) for detailed error messages.

**Ready to customize?** Start editing `ContentView.swift` to change the design!
