# Fix Container Issue

Even though sandboxing is disabled, Xcode is still running the app in a container because of cached settings.

## Solution: Clean Everything

### Step 1: Clean in Xcode

1. **Clean Build Folder**: Product → Clean Build Folder (⇧⌘K)
2. **Close Xcode**

### Step 2: Remove Derived Data

```bash
rm -rf ~/Library/Developer/Xcode/DerivedData/BPMKeyDetector-*
```

### Step 3: Remove App Container (Manual)

Since the container is protected, you need to:

1. Open **Finder**
2. Press `⌘⇧G` (Go to Folder)
3. Enter: `~/Library/Containers/`
4. Find and **drag to Trash**: `com.gentech.BPMKeyDetector`
5. Empty Trash

Or run in Terminal:
```bash
# Move to trash instead of rm
trash ~/Library/Containers/com.gentech.BPMKeyDetector
```

If that doesn't work, try with sudo:
```bash
sudo rm -rf ~/Library/Containers/com.gentech.BPMKeyDetector
```

### Step 4: Verify Entitlements

Open `BPMKeyDetector/BPMKeyDetector/BPMKeyDetector.entitlements` and confirm:

```xml
<key>com.apple.security.app-sandbox</key>
<false/>
```

### Step 5: Rebuild

1. Open Xcode
2. Build: ⌘B
3. Run: ⌘R

### Step 6: Verify

Check Console output - should see:
```
Python path: /Users/titoebiwonjumi/Documents/Codes/bpm-key-detector/...
```

**NOT**:
```
Python path: /Users/titoebiwonjumi/Library/Containers/...
```

## If Still Not Working

Try changing the bundle identifier:

1. Open Xcode project
2. Select project in navigator
3. Select "BPMKeyDetector" target
4. Go to "Signing & Capabilities"
5. Change Bundle Identifier from `com.gentech.BPMKeyDetector` to something else like `com.gentech.BPMKeyDetectorDev`

This forces Xcode to create a fresh app without the old container.
