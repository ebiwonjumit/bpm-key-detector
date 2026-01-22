# Microphone Permission Fix

## Problem

The microphone feature wasn't working because the app wasn't properly requesting microphone access permission from macOS.

**Symptoms**:
- Clicking "Start Recording" did nothing
- No permission prompt appeared
- Python script couldn't access microphone
- Silent failure with no error message

## Root Cause

The app had the microphone usage description in `Info.plist` and entitlements, but wasn't programmatically requesting permission using AVFoundation's authorization API.

## Solution

Added proper microphone permission checking and requesting:

### 1. Import AVFoundation

```swift
import AVFoundation
```

### 2. Check Permission Before Recording

Added `checkMicrophonePermission` method that:
- Checks current authorization status
- Requests permission if not determined
- Returns result via completion handler

```swift
private func checkMicrophonePermission(completion: @escaping (Bool) -> Void) {
    switch AVCaptureDevice.authorizationStatus(for: .audio) {
    case .authorized:
        completion(true)
    case .notDetermined:
        AVCaptureDevice.requestAccess(for: .audio) { granted in
            completion(granted)
        }
    case .denied, .restricted:
        completion(false)
    @unknown default:
        completion(false)
    }
}
```

### 3. Updated Recording Flow

```swift
func startRecording(duration: Double) {
    // First check permission
    checkMicrophonePermission { granted in
        if !granted {
            // Show error message
            self.handleError("Microphone access denied...")
            return
        }
        // Permission granted, start recording
        self.beginRecording(duration: duration)
    }
}
```

### 4. Show Error Messages

Updated `MicrophoneView` to display error messages when permission is denied:

```swift
// Error Message
if let error = audioAnalyzer.errorMessage {
    Text(error)
        .font(.system(size: 11))
        .foregroundColor(.red)
        .multilineTextAlignment(.center)
        .padding(.horizontal, 40)
}
```

## Permission States

### First Time Use
1. User clicks "Start Recording"
2. macOS shows permission dialog:
   ```
   "BPM Key Detector" would like to access the microphone

   [Don't Allow]  [OK]
   ```
3. If user clicks **OK**: Recording starts
4. If user clicks **Don't Allow**: Error message shown

### Permission Denied
Error message displayed:
```
Microphone access denied. Please grant permission in
System Settings → Privacy & Security → Microphone
```

### Permission Granted
Recording proceeds normally with timer and analysis.

## Files Modified

1. **AudioAnalyzer.swift**
   - Added `import AVFoundation`
   - Added `checkMicrophonePermission()` method
   - Renamed `startRecording()` to `beginRecording()` (private)
   - Updated `startRecording()` to check permission first

2. **ContentView.swift**
   - Added error message display in `MicrophoneView`
   - Shows red error text when `errorMessage` is set

## Testing

1. **First Run**:
   - Rebuild and run app (⌘R)
   - Switch to "Microphone" tab
   - Click "Start Recording"
   - **Expected**: Permission dialog appears
   - Click "OK"
   - **Expected**: Recording starts

2. **Permission Denied**:
   - Go to System Settings → Privacy & Security → Microphone
   - Uncheck "BPM Key Detector"
   - Try to record
   - **Expected**: Red error message appears

3. **Grant Permission**:
   - Go to System Settings → Privacy & Security → Microphone
   - Check "BPM Key Detector"
   - Try to record
   - **Expected**: Recording works

## Reset Permissions (For Testing)

To test the permission prompt again:

```bash
# Reset all permissions for the app
tccutil reset Microphone com.gentech.BPMKeyDetectorDev

# Or delete the app's container
rm -rf ~/Library/Containers/com.gentech.BPMKeyDetectorDev
```

Then rebuild and run the app.

## Info.plist Key

The permission dialog shows the text from Info.plist:

```xml
<key>NSMicrophoneUsageDescription</key>
<string>This app needs access to your microphone to record and analyze audio for BPM and key detection.</string>
```

## Status

✅ **FIXED** - Microphone now properly requests permission
✅ **User Friendly** - Clear error messages when permission denied
✅ **macOS Compliant** - Follows Apple's permission guidelines
