#!/usr/bin/env python3
"""
Installation verification script.
Checks that all dependencies are installed and working.
"""

import sys


def check_python_version():
    """Check Python version is 3.8 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python version {version.major}.{version.minor} is too old. Need 3.8+")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_imports():
    """Check that all required packages can be imported."""
    packages = {
        'numpy': 'NumPy',
        'scipy': 'SciPy',
        'librosa': 'librosa',
        'soundfile': 'soundfile',
        'sounddevice': 'sounddevice',
        'rich': 'Rich'
    }

    all_ok = True
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name} - {e}")
            all_ok = False

    return all_ok


def check_modules():
    """Check that custom modules can be imported."""
    sys.path.insert(0, 'src')

    modules = [
        'audio_processor',
        'bpm_detector',
        'key_detector',
        'analyzer'
    ]

    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}.py")
        except ImportError as e:
            print(f"❌ {module}.py - {e}")
            all_ok = False

    return all_ok


def test_basic_functionality():
    """Test basic functionality of the modules."""
    sys.path.insert(0, 'src')

    try:
        import numpy as np
        from audio_processor import AudioProcessor
        from bpm_detector import BPMDetector
        from key_detector import KeyDetector

        # Create test audio
        sample_rate = 22050
        duration = 2.0
        t = np.linspace(0, duration, int(sample_rate * duration))
        test_audio = 0.5 * np.sin(2 * np.pi * 440 * t)

        # Test audio processor
        processor = AudioProcessor()
        if not processor.validate_audio(test_audio):
            print("❌ Audio validation failed")
            return False
        print("✅ Audio validation")

        # Test BPM detector
        bpm_detector = BPMDetector()
        bpm, confidence = bpm_detector.detect(test_audio)
        if not (40 <= bpm <= 240):
            print(f"❌ BPM detection returned invalid value: {bpm}")
            return False
        print(f"✅ BPM detection (detected: {bpm:.1f} BPM)")

        # Test key detector
        key_detector = KeyDetector()
        key, mode, confidence = key_detector.detect(test_audio)
        if key not in key_detector.PITCH_CLASSES:
            print(f"❌ Key detection returned invalid key: {key}")
            return False
        print(f"✅ Key detection (detected: {key} {mode})")

        return True

    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("BPM Key Detector - Installation Verification")
    print("=" * 60)
    print()

    print("Checking Python version...")
    python_ok = check_python_version()
    print()

    print("Checking required packages...")
    imports_ok = check_imports()
    print()

    print("Checking custom modules...")
    modules_ok = check_modules()
    print()

    print("Testing basic functionality...")
    functionality_ok = test_basic_functionality()
    print()

    print("=" * 60)
    if python_ok and imports_ok and modules_ok and functionality_ok:
        print("✅ All checks passed! Installation is complete.")
        print()
        print("You can now run:")
        print("  python src/analyzer.py --file /path/to/audio.mp3")
        print("  python src/analyzer.py --mic")
        print()
        print("Run tests with:")
        print("  pytest tests/")
        print("=" * 60)
        return 0
    else:
        print("❌ Some checks failed. Please review the errors above.")
        print()
        print("Try reinstalling dependencies:")
        print("  pip install -r requirements.txt")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
