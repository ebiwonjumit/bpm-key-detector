"""
Unit tests for the bpm_detector module.
"""

import pytest
import numpy as np
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bpm_detector import BPMDetector


class TestBPMDetector:
    """Test suite for BPMDetector class."""

    @pytest.fixture
    def detector(self):
        """Create a BPMDetector instance for testing."""
        return BPMDetector()

    @pytest.fixture
    def sample_audio(self):
        """Create sample audio data for testing."""
        sample_rate = 22050
        duration = 5.0
        t = np.linspace(0, duration, int(sample_rate * duration))

        # Create audio with a clear beat at 120 BPM
        # 120 BPM = 2 beats per second
        beat_frequency = 2.0
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)  # Base tone

        # Add periodic beats
        beat_period = sample_rate / beat_frequency
        beat_envelope = np.zeros_like(t)
        for i in range(int(duration * beat_frequency)):
            start = int(i * beat_period)
            end = min(start + int(beat_period * 0.1), len(beat_envelope))
            beat_envelope[start:end] = 1.0

        audio = audio * (0.3 + 0.7 * beat_envelope)

        return audio.astype(np.float32)

    def test_init_default_sample_rate(self):
        """Test initialization with default sample rate."""
        detector = BPMDetector()
        assert detector.sample_rate == 22050

    def test_init_custom_sample_rate(self):
        """Test initialization with custom sample rate."""
        detector = BPMDetector(sample_rate=44100)
        assert detector.sample_rate == 44100

    def test_detect_success(self, detector, sample_audio):
        """Test successful BPM detection."""
        bpm, confidence = detector.detect(sample_audio)

        assert isinstance(bpm, float)
        assert isinstance(confidence, float)
        assert bpm > 0
        assert 0.0 <= confidence <= 1.0

    def test_detect_bpm_range(self, detector, sample_audio):
        """Test that detected BPM is in reasonable range."""
        bpm, _ = detector.detect(sample_audio)

        # Should be within reasonable music BPM range
        assert 40 <= bpm <= 240

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
        bpm, confidence = detector.detect(min_audio)
        assert isinstance(bpm, float)
        assert bpm > 0

    def test_get_confidence_level_high(self, detector):
        """Test confidence level for high confidence."""
        assert detector.get_confidence_level(0.8) == "High"
        assert detector.get_confidence_level(0.7) == "High"

    def test_get_confidence_level_medium(self, detector):
        """Test confidence level for medium confidence."""
        assert detector.get_confidence_level(0.6) == "Medium"
        assert detector.get_confidence_level(0.5) == "Medium"
        assert detector.get_confidence_level(0.4) == "Medium"

    def test_get_confidence_level_low(self, detector):
        """Test confidence level for low confidence."""
        assert detector.get_confidence_level(0.3) == "Low"
        assert detector.get_confidence_level(0.1) == "Low"
        assert detector.get_confidence_level(0.0) == "Low"

    def test_get_confidence_level_boundary(self, detector):
        """Test confidence level at boundaries."""
        assert detector.get_confidence_level(0.69) == "Medium"
        assert detector.get_confidence_level(0.70) == "High"
        assert detector.get_confidence_level(0.39) == "Low"
        assert detector.get_confidence_level(0.40) == "Medium"

    def test_validate_bpm_valid_range(self, detector):
        """Test BPM validation for valid values."""
        assert detector.validate_bpm(60.0) is True
        assert detector.validate_bpm(120.0) is True
        assert detector.validate_bpm(180.0) is True
        assert detector.validate_bpm(40.0) is True
        assert detector.validate_bpm(240.0) is True

    def test_validate_bpm_invalid_range(self, detector):
        """Test BPM validation for invalid values."""
        assert detector.validate_bpm(30.0) is False
        assert detector.validate_bpm(250.0) is False
        assert detector.validate_bpm(0.0) is False
        assert detector.validate_bpm(-60.0) is False

    def test_validate_bpm_boundary(self, detector):
        """Test BPM validation at boundaries."""
        assert detector.validate_bpm(39.9) is False
        assert detector.validate_bpm(40.0) is True
        assert detector.validate_bpm(240.0) is True
        assert detector.validate_bpm(240.1) is False

    def test_detect_with_multiple_estimates(self, detector, sample_audio):
        """Test detection with multiple tempo estimates."""
        primary_bpm, confidence, alternatives = detector.detect_with_multiple_estimates(
            sample_audio, n_estimates=2
        )

        assert isinstance(primary_bpm, float)
        assert isinstance(confidence, float)
        assert isinstance(alternatives, list)
        assert primary_bpm > 0
        assert 0.0 <= confidence <= 1.0
        # Should return n_estimates - 1 alternatives
        assert len(alternatives) == 1

    def test_detect_with_multiple_estimates_empty_audio(self, detector):
        """Test multiple estimates with empty audio raises ValueError."""
        with pytest.raises(ValueError, match="Audio data is empty"):
            detector.detect_with_multiple_estimates(np.array([]))

    def test_detect_with_multiple_estimates_count(self, detector, sample_audio):
        """Test requesting different numbers of estimates."""
        _, _, alternatives = detector.detect_with_multiple_estimates(
            sample_audio, n_estimates=3
        )
        assert len(alternatives) == 2

        _, _, alternatives = detector.detect_with_multiple_estimates(
            sample_audio, n_estimates=1
        )
        assert len(alternatives) == 0

    def test_confidence_calculation_fallback(self, detector):
        """Test confidence calculation with edge cases."""
        # Create audio that might cause issues in confidence calculation
        silence = np.zeros(detector.sample_rate * 2)

        # Should not crash, should return a confidence value
        try:
            _, confidence = detector.detect(silence)
            assert 0.0 <= confidence <= 1.0
        except RuntimeError:
            # It's acceptable to fail on silence
            pass


class TestBPMDetectorWithSyntheticBeats:
    """Test BPM detection with synthetic beat patterns."""

    def create_beat_pattern(self, bpm, duration=5.0, sample_rate=22050):
        """Helper to create audio with a specific BPM."""
        t = np.linspace(0, duration, int(sample_rate * duration))

        # Create base tone
        audio = 0.3 * np.sin(2 * np.pi * 440 * t)

        # Add beats at specified BPM
        beats_per_second = bpm / 60.0
        beat_period = sample_rate / beats_per_second

        beat_envelope = np.ones_like(t) * 0.3
        for i in range(int(duration * beats_per_second)):
            start = int(i * beat_period)
            end = min(start + int(beat_period * 0.2), len(beat_envelope))
            beat_envelope[start:end] = 1.0

        audio = audio * beat_envelope

        return audio.astype(np.float32)

    def test_detect_120_bpm(self):
        """Test detection of 120 BPM."""
        detector = BPMDetector()
        audio = self.create_beat_pattern(120)

        bpm, confidence = detector.detect(audio)

        # Should be close to 120 BPM (within reasonable margin)
        assert 100 <= bpm <= 140

    def test_detect_80_bpm(self):
        """Test detection of 80 BPM."""
        detector = BPMDetector()
        audio = self.create_beat_pattern(80)

        bpm, confidence = detector.detect(audio)

        # Should be close to 80 BPM (within reasonable margin)
        assert 60 <= bpm <= 100

    def test_detect_140_bpm(self):
        """Test detection of 140 BPM."""
        detector = BPMDetector()
        audio = self.create_beat_pattern(140)

        bpm, confidence = detector.detect(audio)

        # Should be close to 140 BPM (within reasonable margin)
        assert 120 <= bpm <= 160

    def test_different_sample_rates(self):
        """Test detection works with different sample rates."""
        for sample_rate in [22050, 44100]:
            detector = BPMDetector(sample_rate=sample_rate)
            audio = self.create_beat_pattern(120, sample_rate=sample_rate)

            bpm, confidence = detector.detect(audio)

            # Should detect reasonable BPM regardless of sample rate
            assert 40 <= bpm <= 240


class TestBPMDetectorEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_white_noise(self):
        """Test detection with white noise."""
        detector = BPMDetector()
        noise = np.random.randn(detector.sample_rate * 3)

        # Should not crash, but may have low confidence
        bpm, confidence = detector.detect(noise)

        assert isinstance(bpm, float)
        assert bpm > 0
        # Confidence might be low for random noise
        assert 0.0 <= confidence <= 1.0

    def test_sine_wave_no_beats(self):
        """Test detection with pure sine wave (no clear beats)."""
        detector = BPMDetector()
        t = np.linspace(0, 3.0, int(detector.sample_rate * 3))
        audio = np.sin(2 * np.pi * 440 * t)

        # Should detect something, even if not meaningful
        bpm, confidence = detector.detect(audio)

        assert isinstance(bpm, float)
        assert bpm > 0

    def test_very_long_audio(self):
        """Test detection with long audio."""
        detector = BPMDetector()
        # Create 30 seconds of audio
        long_audio = np.random.randn(detector.sample_rate * 30)

        # Should handle long audio without issues
        bpm, confidence = detector.detect(long_audio)

        assert isinstance(bpm, float)
        assert bpm > 0

    def test_clipped_audio(self):
        """Test detection with clipped audio."""
        detector = BPMDetector()
        # Create clipped audio (values at -1 and 1)
        audio = np.ones(detector.sample_rate * 3)
        audio[::100] = -1.0  # Add some variation

        # Should not crash
        bpm, confidence = detector.detect(audio)

        assert isinstance(bpm, float)
        assert bpm > 0
