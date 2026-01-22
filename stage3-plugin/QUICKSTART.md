# Quick Start - Stage 3 DAW Plugin

Build and use the BPM Key Detector plugin in your DAW in 15 minutes!

## Prerequisites

✅ macOS 10.13+ or Windows 10+
✅ JUCE Framework installed
✅ Xcode (macOS) or Visual Studio (Windows)
✅ A DAW to test in (Logic Pro, Ableton, FL Studio, etc.)

## Step 1: Install JUCE (5 minutes)

### Download JUCE:
1. Go to https://juce.com/get-juce
2. Download JUCE (free, no signup required for GPL)
3. Extract to `~/Development/JUCE` (or anywhere you like)

**Verify**:
```bash
ls ~/Development/JUCE/modules
# Should see: juce_audio_basics, juce_core, etc.
```

## Step 2: Open Project (2 minutes)

### Launch Projucer:
```bash
# Navigate to JUCE folder
cd ~/Development/JUCE
open Projucer.app

# Or find it in Applications
```

### Open Plugin Project:
1. In Projucer: File → Open
2. Navigate to: `bpm-key-detector/stage3-plugin/`
3. Select: `BPMKeyDetector.jucer`
4. Click Open

## Step 3: Configure Paths (1 minute)

### Set JUCE Module Path:
1. In Projucer, click "Modules" (left sidebar)
2. For each module, set path to your JUCE installation:
   - Click folder icon
   - Navigate to `~/Development/JUCE/modules`
   - Select
3. Click "Save Project" (⌘S)

**Or** set global path:
1. Projucer → Settings → Global Paths
2. Set "Path to JUCE": `~/Development/JUCE`
3. Reopen project

## Step 4: Generate Xcode Project (1 minute)

In Projucer:
1. Click "Save Project and Open in IDE" button
2. This generates Xcode project in `Builds/MacOSX/`
3. Xcode opens automatically

## Step 5: Build Plugin (3 minutes)

### In Xcode:

**Choose Target**:
- For Logic Pro/GarageBand → Build "BPM Key Detector - AU"
- For most other DAWs → Build "BPM Key Detector - VST3"
- For testing without DAW → Build "BPM Key Detector - Standalone Plugin"

**Build Steps**:
1. Select target from dropdown (top-left)
2. Product → Build (⌘B)
3. Wait for build to complete
4. Check for errors (should be none!)

**Build locations**:
- AU: `~/Library/Audio/Plug-Ins/Components/BPM Key Detector.component`
- VST3: `~/Library/Audio/Plug-Ins/VST3/BPM Key Detector.vst3`

## Step 6: Test in DAW (3 minutes)

### Open Your DAW:
Let's use Logic Pro as example:

1. **Launch Logic Pro**
2. **Create New Project** → Empty Project → Audio track
3. **Add Plugin**:
   - In mixer, click insert slot
   - Navigate to: Audio Units → Audio Analyzer → BPM Key Detector
   - Insert plugin
4. **Load Audio**:
   - Drag audio file to track
   - Or enable input monitoring for live audio
5. **Analyze**:
   - Click "Start Analysis" in plugin window
   - Play your audio
   - Watch BPM and Key update!

### For Other DAWs:

**Ableton Live**:
- Audio Effects → Audio Analyzer → BPM Key Detector

**FL Studio**:
- Mixer → Insert → More → BPM Key Detector

**Reaper**:
- FX → Add → BPM Key Detector

## Testing Checklist

- [ ] Plugin appears in DAW
- [ ] Plugin window opens
- [ ] Start Analysis button works
- [ ] BPM displays when playing audio
- [ ] Key displays correctly
- [ ] Confidence levels update
- [ ] Stop Analysis works
- [ ] No crashes or freezes

## Troubleshooting

### Plugin doesn't appear in DAW

**Fix 1**: Rescan plugins
- Logic Pro: Preferences → Plug-in Manager → Reset & Rescan
- Ableton: Preferences → Plug-ins → Rescan
- FL Studio: Options → Manage Plugins → Find Plugins

**Fix 2**: Check installation path
```bash
# AU plugins:
ls ~/Library/Audio/Plug-Ins/Components/ | grep BPM

# VST3 plugins:
ls ~/Library/Audio/Plug-Ins/VST3/ | grep BPM
```

### Build errors in Xcode

**Error: "JUCE modules not found"**

Fix: Configure module paths in Projucer (see Step 3)

**Error: "Code signing failed"**

Fix: Disable code signing for development:
1. Xcode → Select target
2. Signing & Capabilities
3. Uncheck "Automatically manage signing"
4. Set "Code Signing Identity" to "Sign to Run Locally"

### Plugin crashes DAW

**Fix**: Build Debug configuration:
1. Xcode → Product → Scheme → Edit Scheme
2. Run → Build Configuration → Debug
3. Rebuild
4. Attach debugger to see crash location

### No audio analysis happening

**Fix 1**: Check audio is playing
- Make sure DAW is playing audio through plugin
- Enable input monitoring if using live input

**Fix 2**: Click "Start Analysis"
- Plugin needs to be started manually
- Check button text changes to "Stop Analysis"

### High CPU usage

**Expected**: 2-5% during analysis
**If higher**: Check buffer size in DAW
- Larger buffers = lower CPU
- Smaller buffers = higher CPU

## Next Steps

### Customize the Plugin:

**Change Colors**:
Edit `PluginEditor.cpp`:
```cpp
juce::Colour backgroundColour = juce::Colours::white;
juce::Colour textColour = juce::Colours::black;
```

**Adjust Window Size**:
Edit `PluginEditor.cpp` constructor:
```cpp
setSize (400, 300); // Change dimensions
```

**Modify Analysis Window**:
Edit `PluginProcessor.h`:
```cpp
static constexpr int analysisWindowSeconds = 15; // Was 10
```

### Test Thoroughly:
- [ ] Different audio types (electronic, acoustic, vocals)
- [ ] Various BPMs (slow, medium, fast)
- [ ] Different keys (major, minor, sharps, flats)
- [ ] Long sessions (hours)
- [ ] Multiple plugin instances

### Package for Distribution:
1. Build Release configuration
2. Code sign with Apple Developer certificate
3. Notarize (required for macOS)
4. Create installer (.pkg)
5. Test on clean system

## Development Workflow

### Make Changes:
1. Edit source files in `Source/`
2. Save
3. Xcode auto-detects changes
4. Rebuild (⌘B)
5. Test in DAW

### Debug:
1. Xcode → Debug → Attach to Process
2. Select your DAW
3. Set breakpoints in plugin code
4. Trigger plugin action
5. Debugger stops at breakpoint

### Hot Tips:
- Use Standalone app for quick testing
- printf/DBG debugging works
- Check Console.app for crash logs
- Use Instruments for profiling

## Common Tasks

### Rebuild Everything:
```bash
cd Builds/MacOSX
xcodebuild clean
xcodebuild -configuration Release
```

### Validate AU Plugin:
```bash
auval -v aufx BKDe AuAn
```

### Validate VST3 Plugin:
Use pluginval from JUCE forum

### Package for Distri bution:
1. Product → Archive
2. Distribute App → Copy App
3. Code sign
4. Create DMG or PKG

## Success!

If you've made it here, you should have:
✅ Built the plugin successfully
✅ Tested in your DAW
✅ Seen BPM and Key detection working
✅ Ready to customize or distribute

## Resources

- **JUCE Docs**: https://docs.juce.com
- **JUCE Forum**: https://forum.juce.com
- **Plugin Validation**: Use auval (AU) or pluginval (VST3)
- **This Project**: Check IMPLEMENTATION_SUMMARY.md for details

---

**Happy plugin development!** 🎛️
