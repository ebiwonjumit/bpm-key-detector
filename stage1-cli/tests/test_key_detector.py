"""
Unit tests for the key_detector module.
"""

import pytest
import numpy as np
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from key_detector import KeyDetector


class TestKeyDetector:
    """Test suite for KeyDetector class."""

    @pytest.fixture
    def detector(self):
        """Create a KeyDetector instance for testing."""
        return KeyDetector()

    @pytest.fixture
    def sample_audio(self):
        """Create sample audio data for testing."""
        sample_rate = 22050
        duration = 5.0
        t = np.linspace(0, duration, int(sample_rate * duration))

        # Create audio with C major chord (C, E, G)
        audio = (
            0.33 * np.sin(2 * np.pi * 261.63 * t) +  # C4
            0.33 * np.sin(2 * np.pi * 329.63 * t) +  # E4
            0.33 * np.sin(2 * np.pi * 392.00 * t)    # G4
        )

        return audio.astype(np.float32)

    def test_init_default_sample_rate(self):
        """Test initialization with default sample rate."""
        detector = KeyDetector()
        assert detector.sample_rate == 22050

    def test_init_custom_sample_rate(self):
        """Test initialization with custom sample rate."""
        detector = KeyDetector(sample_rate=44100)
        assert detector.sample_rate == 44100

    def test_pitch_classes_count(self, detector):
        """Test that all 12 pitch classes are defined."""
        assert len(detector.PITCH_CLASSES) == 12

    def test_major_profile_length(self, detector):
        """Test that major profile has 12 values."""
        assert len(detector.MAJOR_PROFILE) == 12

    def test_minor_profile_length(self, detector):
        """Test that minor profile has 12 values."""
        assert len(detector.MINOR_PROFILE) == 12

    def test_detect_success(self, detector, sample_audio):
        """Test successful key detection."""
        key, mode, confidence = detector.detect(sample_audio)

        assert isinstance(key, str)
        assert isinstance(mode, str)
        assert isinstance(confidence, float)
        assert key in detector.PITCH_CLASSES
        assert mode in ['major', 'minor']
        assert 0.0 <= confidence <= 1.0

    def test_detect_empty_audio(self, detector):
        """Test detection with empty audio raises ValueError."""
        with pytest.raises(ValueError, match="Audio data is empty"):
            detector.detect(np.array([]))

        with pytest.raises(ValueError, match="Audio data is empty"):
            detector.detect(None)

    def test_detect_too_short_audio(self, detector):
        """Test detection with too short audio raises ValueError."""
        short_audio = np.random.randn(detector.sample_rate // 2)

        with pytest.raises(ValueError, match="too short"):
            detector.detect(short_audio)

    def test_detect_minimum_length_audio(self, detector):
        """Test detection with minimum valid length (1 second)."""
        min_audio = np.random.randn(detector.sample_rate)

        # Should not raise an error
        key, mode, confidence = detector.detect(min_audio)
        assert isinstance(key, str)
        assert isinstance(mode, str)

    def test_get_key_string_major(self, detector):
        """Test formatting key string for major keys."""
        assert detector.get_key_string('C', 'major') == 'C major'
        assert detector.get_key_string('F#', 'major') == 'F# major'

    def test_get_key_string_minor(self, detector):
        """Test formatting key string for minor keys."""
        assert detector.get_key_string('A', 'minor') == 'A minor'
        assert detector.get_key_string('D#', 'minor') == 'D# minor'

    def test_get_confidence_level_high(self, detector):
        """Test confidence level for high confidence."""
        assert detector.get_confidence_level(0.8) == "High"
        assert detector.get_confidence_level(0.7) == "High"

    def test_get_confidence_level_medium(self, detector):
        """Test confidence level for medium confidence."""
        assert detector.get_confidence_level(0.6) == "Medium"
        assert detector.get_confidence_level(0.5) == "Medium"

    def test_get_confidence_level_low(self, detector):
        """Test confidence level for low confidence."""
        assert detector.get_confidence_level(0.4) == "Low"
        assert detector.get_confidence_level(0.2) == "Low"

    def test_get_confidence_level_boundary(self, detector):
        """Test confidence level at boundaries."""
        assert detector.get_confidence_level(0.49) == "Low"
        assert detector.get_confidence_level(0.50) == "Medium"
        assert detector.get_confidence_level(0.69) == "Medium"
        assert detector.get_confidence_level(0.70) == "High"

    def test_get_relative_keys_major(self, detector):
        """Test getting relative keys for major keys."""
        related = detector.get_relative_keys('C', 'major')

        assert 'relative' in related
        assert 'parallel' in related
        assert 'dominant' in related

        # C major relative minor is A minor
        assert related['relative'] == 'A minor'
        # C major parallel minor is C minor
        assert related['parallel'] == 'C minor'
        # C major dominant is G major
        assert related['dominant'] == 'G major'

    def test_get_relative_keys_minor(self, detector):
        """Test getting relative keys for minor keys."""
        related = detector.get_relative_keys('A', 'minor')

        assert 'relative' in related
        assert 'parallel' in related
        assert 'dominant' in related

        # A minor relative major is C major
        assert related['relative'] == 'C major'
        # A minor parallel major is A major
        assert related['parallel'] == 'A major'
        # A minor dominant is E minor
        assert related['dominant'] == 'E minor'

    def test_get_scale_notes_c_major(self, detector):
        """Test getting scale notes for C major."""
        scale = detector.get_scale_notes('C', 'major')

        assert len(scale) == 7
        assert scale == ['C', 'D', 'E', 'F', 'G', 'A', 'B']

    def test_get_scale_notes_a_minor(self, detector):
        """Test getting scale notes for A minor (natural)."""
        scale = detector.get_scale_notes('A', 'minor')

        assert len(scale) == 7
        assert scale == ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    def test_get_scale_notes_g_major(self, detector):
        """Test getting scale notes for G major."""
        scale = detector.get_scale_notes('G', 'major')

        assert len(scale) == 7
        # G major has F#
        assert 'G' in scale
        assert 'F#' in scale

    def test_get_scale_notes_d_minor(self, detector):
        """Test getting scale notes for D minor."""
        scale = detector.get_scale_notes('D', 'minor')

        assert len(scale) == 7
        assert scale[0] == 'D'


class TestKeyDetectorWithSyntheticAudio:
    """Test key detection with synthetic audio patterns."""

    def create_chord_audio(self, frequencies, duration=5.0, sample_rate=22050):
        """Helper to create audio with specific frequencies (chord)."""
        t = np.linspace(0, duration, int(sample_rate * duration))

        audio = np.zeros_like(t)
        for freq in frequencies:
            audio += np.sin(2 * np.pi * freq * t) / len(frequencies)

        return audio.astype(np.float32)

    def test_detect_c_major_chord(self):
        """Test detection with C major chord."""
        detector = KeyDetector()

        # C major chord: C, E, G
        frequencies = [261.63, 329.63, 392.00]
        audio = self.create_chord_audio(frequencies)

        key, mode, confidence = detector.detect(audio)

        # Should detect C or related key
        assert key in detector.PITCH_CLASSES
        assert mode in ['major', 'minor']

    def test_detect_a_minor_chord(self):
        """Test detection with A minor chord."""
        detector = KeyDetector()

        # A minor chord: A, C, E
        frequencies = [220.00, 261.63, 329.63]
        audio = self.create_chord_audio(frequencies)

        key, mode, confidence = detector.detect(audio)

        # Should detect A minor or related key
        assert key in detector.PITCH_CLASSES
        assert mode in ['major', 'minor']

    def test_detect_with_octaves(self):
        """Test detection with notes in different octaves."""
        detector = KeyDetector()

        # C notes in different octaves
        frequencies = [130.81, 261.63, 523.25]  # C3, C4, C5
        audio = self.create_chord_audio(frequencies)

        key, mode, confidence = detector.detect(audio)

        # Should detect C-based key
        assert key in detector.PITCH_CLASSES


class TestKeyDetectorCorrelation:
    """Test the correlation calculation used in key detection."""

    def test_correlation_identical_arrays(self):
        """Test correlation with identical arrays."""
        detector = KeyDetector()

        x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        corr = detector._correlation(x, x)

        # Perfect correlation should be 1.0
        assert abs(corr - 1.0) < 0.01

    def test_correlation_opposite_arrays(self):
        """Test correlation with opposite arrays."""
        detector = KeyDetector()

        x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y = -x

        corr = detector._correlation(x, y)

        # Perfect negative correlation should be -1.0
        assert abs(corr - (-1.0)) < 0.01

    def test_correlation_uncorrelated_arrays(self):
        """Test correlation with uncorrelated arrays."""
        detector = KeyDetector()

        x = np.array([1.0, 2.0, 1.0, 2.0, 1.0])
        y = np.array([1.0, 1.0, 2.0, 2.0, 1.0])

        corr = detector._correlation(x, y)

        # Should be between -1 and 1
        assert -1.0 <= corr <= 1.0


class TestKeyDetectorEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_white_noise(self):
        """Test detection with white noise."""
        detector = KeyDetector()
        noise = np.random.randn(detector.sample_rate * 3)

        # Should not crash, should return valid results
        key, mode, confidence = detector.detect(noise)

        assert key in detector.PITCH_CLASSES
        assert mode in ['major', 'minor']
        # Confidence might be lower for random noise
        assert 0.0 <= confidence <= 1.0

    def test_sine_wave_single_note(self):
        """Test detection with a single note."""
        detector = KeyDetector()
        t = np.linspace(0, 3.0, int(detector.sample_rate * 3))

        # A440 (A note)
        audio = np.sin(2 * np.pi * 440 * t)

        key, mode, confidence = detector.detect(audio)

        # Should detect A or related key
        assert key in detector.PITCH_CLASSES

    def test_very_long_audio(self):
        """Test detection with long audio."""
        detector = KeyDetector()

        # Create 30 seconds of audio
        long_audio = np.random.randn(detector.sample_rate * 30)

        # Should handle long audio without issues
        key, mode, confidence = detector.detect(long_audio)

        assert key in detector.PITCH_CLASSES
        assert mode in ['major', 'minor']

    def test_all_keys_have_seven_notes(self):
        """Test that all keys produce 7-note scales."""
        detector = KeyDetector()

        for key in detector.PITCH_CLASSES:
            for mode in ['major', 'minor']:
                scale = detector.get_scale_notes(key, mode)
                assert len(scale) == 7, f"Scale for {key} {mode} should have 7 notes"

    def test_all_keys_have_relative_keys(self):
        """Test that all keys have relative keys defined."""
        detector = KeyDetector()

        for key in detector.PITCH_CLASSES:
            for mode in ['major', 'minor']:
                related = detector.get_relative_keys(key, mode)
                assert 'relative' in related
                assert 'parallel' in related
                assert 'dominant' in related

    def test_silent_audio(self):
        """Test detection with silent audio (all zeros)."""
        detector = KeyDetector()
        silence = np.zeros(detector.sample_rate * 3)

        # Should not crash
        try:
            key, mode, confidence = detector.detect(silence)
            assert key in detector.PITCH_CLASSES
            assert mode in ['major', 'minor']
        except RuntimeError:
            # It's acceptable to fail on silence
            pass

    def test_clipped_audio(self):
        """Test detection with clipped audio."""
        detector = KeyDetector()
        # Create clipped audio (values at extremes)
        audio = np.ones(detector.sample_rate * 3)
        audio[::2] = -1.0

        # Should not crash
        key, mode, confidence = detector.detect(audio)

        assert key in detector.PITCH_CLASSES
        assert mode in ['major', 'minor']
