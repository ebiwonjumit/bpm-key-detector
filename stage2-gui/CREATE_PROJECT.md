# Creating the Xcode Project

Since we can't commit the full Xcode project file to git easily, here's how to create it from the source files.

## Option 1: Use Existing Files (Recommended)

The source files are already in place. You just need to create an Xcode project:

### Steps:

1. **Open Xcode**
2. **Create New Project**:
   - File → New → Project
   - Choose "macOS" → "App"
   - Click "Next"

3. **Configure Project**:
   - Product Name: `BPMKeyDetector`
   - Team: Select your team
   - Organization Identifier: `com.yourname` (or keep default)
   - Interface: **SwiftUI**
   - Language: **Swift**
   - Storage: **None**
   - Uncheck "Include Tests"
   - Click "Next"

4. **Save Location**:
   - Navigate to: `bpm-key-detector/stage2-gui/`
   - **Delete the `BPMKeyDetector` folder Xcode created**
   - Use the existing `BPMKeyDetector` folder
   - Click "Create"

5. **Replace Default Files**:
   - Delete the default `BPMKeyDetectorApp.swift` and `ContentView.swift` from the project
   - Right-click project → "Add Files to BPMKeyDetector"
   - Add all `.swift` files from the `BPMKeyDetector` folder:
     - BPMKeyDetectorApp.swift
     - ContentView.swift
     - AudioAnalyzer.swift

6. **Add Assets and Info**:
   - The `Assets.xcassets`, `Info.plist`, and `.entitlements` should already be there
   - If not, add them via "Add Files to BPMKeyDetector"

7. **Configure Capabilities**:
   - Select project → Target → "Signing & Capabilities"
   - Add "Audio Input" if not present
   - Verify sandbox settings

8. **Build and Run**: Press `⌘R`

## Option 2: Manual File Import

If you already have an Xcode project:

1. Drag the `.swift` files into the project navigator
2. Make sure "Copy items if needed" is checked
3. Add to target: `BPMKeyDetector`

## Required Files

Make sure these files are in the Xcode project:

- [x] `BPMKeyDetectorApp.swift` - App entry point
- [x] `ContentView.swift` - Main UI views
- [x] `AudioAnalyzer.swift` - Python bridge
- [x] `Info.plist` - App configuration
- [x] `BPMKeyDetector.entitlements` - Permissions
- [x] `Assets.xcassets/` - Asset catalog

## Configuration Checklist

- [ ] Minimum Deployment Target: macOS 12.0
- [ ] Bundle Identifier: `com.yourname.BPMKeyDetector`
- [ ] Signing: Automatic signing enabled
- [ ] Capabilities: Audio Input enabled
- [ ] Sandbox: File access (user-selected, read-only)
- [ ] Python Path: Updated in `AudioAnalyzer.swift`

## Build Settings

Key settings to verify:

- **Base SDK**: macOS
- **Deployment Target**: macOS 12.0 or later
- **Swift Language Version**: Swift 5
- **Enable Hardened Runtime**: Yes (for distribution)

## Testing the Build

1. **Build**: `⌘B`
2. **Run**: `⌘R`
3. **Test File**: Drag an audio file to test
4. **Test Mic**: Switch to Microphone tab and test recording

## Common Issues

### "Cannot find BPMKeyDetectorApp in scope"

**Fix**: Make sure all Swift files are added to the target
- Select file → File Inspector → Target Membership → Check "BPMKeyDetector"

### "Module not found"

**Fix**: Clean build folder
- Product → Clean Build Folder (`⌘⇧K`)
- Rebuild

### Missing entitlements

**Fix**:
1. File → New → File → Property List
2. Name it `BPMKeyDetector.entitlements`
3. Add the required keys (see the existing file)
4. Project Settings → Signing & Capabilities → Code Signing Entitlements → Select the file

## Next Steps

Once the project builds successfully:

1. Update Python paths in `AudioAnalyzer.swift` to match your system
2. Test with Stage 1 CLI to ensure backend works
3. Customize the UI as needed
4. Add your own features

## Distribution

To distribute the app:

1. **Archive**: Product → Archive
2. **Export**: Window → Organizer → Distribute App
3. **Notarize**: Required for distribution outside App Store
4. **Sign**: With Apple Developer certificate

---

For support, check the main README.md
