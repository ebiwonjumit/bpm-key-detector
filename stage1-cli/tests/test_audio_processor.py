"""
Unit tests for the audio_processor module.
"""

import pytest
import numpy as np
from pathlib import Path
import tempfile
import os

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from audio_processor import AudioProcessor


class TestAudioProcessor:
    """Test suite for AudioProcessor class."""

    @pytest.fixture
    def processor(self):
        """Create an AudioProcessor instance for testing."""
        return AudioProcessor()

    @pytest.fixture
    def sample_audio(self):
        """Create sample audio data for testing."""
        # Generate 2 seconds of 440Hz sine wave (A4 note)
        sample_rate = 22050
        duration = 2.0
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)
        return audio.astype(np.float32), sample_rate

    @pytest.fixture
    def temp_wav_file(self, sample_audio):
        """Create a temporary WAV file for testing."""
        import soundfile as sf
        audio, sample_rate = sample_audio

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name

        sf.write(temp_path, audio, sample_rate)

        yield temp_path

        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

    def test_init_default_sample_rate(self):
        """Test initialization with default sample rate."""
        processor = AudioProcessor()
        assert processor.sample_rate == 22050

    def test_init_custom_sample_rate(self):
        """Test initialization with custom sample rate."""
        processor = AudioProcessor(sample_rate=44100)
        assert processor.sample_rate == 44100

    def test_load_audio_success(self, processor, temp_wav_file):
        """Test successfully loading an audio file."""
        audio_data, sample_rate = processor.load_audio(temp_wav_file)

        assert isinstance(audio_data, np.ndarray)
        assert len(audio_data) > 0
        assert sample_rate == processor.sample_rate
        assert audio_data.dtype in [np.float32, np.float64]

    def test_load_audio_file_not_found(self, processor):
        """Test loading a non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            processor.load_audio('/nonexistent/path/to/audio.wav')

    def test_load_audio_unsupported_format(self, processor):
        """Test loading unsupported format raises ValueError."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_path = f.name
            f.write(b'not an audio file')

        try:
            with pytest.raises(ValueError, match="Unsupported audio format"):
                processor.load_audio(temp_path)
        finally:
            os.remove(temp_path)

    def test_load_audio_empty_file(self, processor):
        """Test loading an empty/corrupted file raises RuntimeError."""
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name
            # Write invalid WAV data
            f.write(b'RIFF' + b'\x00' * 100)

        try:
            with pytest.raises(RuntimeError):
                processor.load_audio(temp_path)
        finally:
            os.remove(temp_path)

    def test_record_audio_invalid_duration(self, processor):
        """Test recording with invalid duration raises ValueError."""
        with pytest.raises(ValueError, match="Duration must be positive"):
            processor.record_audio(duration=0)

        with pytest.raises(ValueError, match="Duration must be positive"):
            processor.record_audio(duration=-5)

    def test_record_audio_excessive_duration(self, processor):
        """Test recording with excessive duration raises ValueError."""
        with pytest.raises(ValueError, match="cannot exceed 300 seconds"):
            processor.record_audio(duration=400)

    def test_save_audio_success(self, processor, sample_audio):
        """Test successfully saving audio data."""
        audio, sample_rate = sample_audio

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name

        try:
            processor.save_audio(audio, temp_path, sample_rate)
            assert os.path.exists(temp_path)
            assert os.path.getsize(temp_path) > 0
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_save_audio_empty_data(self, processor):
        """Test saving empty audio data raises ValueError."""
        with pytest.raises(ValueError, match="Audio data is empty"):
            processor.save_audio(np.array([]), 'output.wav')

        with pytest.raises(ValueError, match="Audio data is empty"):
            processor.save_audio(None, 'output.wav')

    def test_get_duration(self, processor, sample_audio):
        """Test calculating audio duration."""
        audio, _ = sample_audio
        duration = processor.get_duration(audio)

        # Should be approximately 2 seconds
        assert 1.9 < duration < 2.1

    def test_validate_audio_valid(self, processor, sample_audio):
        """Test validation of valid audio data."""
        audio, _ = sample_audio
        assert processor.validate_audio(audio) is True

    def test_validate_audio_empty(self, processor):
        """Test validation of empty audio data."""
        assert processor.validate_audio(None) is False
        assert processor.validate_audio(np.array([])) is False

    def test_validate_audio_too_short(self, processor):
        """Test validation of too short audio data."""
        # Less than 1 second
        short_audio = np.random.randn(processor.sample_rate // 2)
        assert processor.validate_audio(short_audio) is False

    def test_validate_audio_all_zeros(self, processor):
        """Test validation of silent audio (all zeros)."""
        silent_audio = np.zeros(processor.sample_rate * 2)
        assert processor.validate_audio(silent_audio) is False

    def test_validate_audio_minimum_valid(self, processor):
        """Test validation of minimum valid audio (1 second with signal)."""
        valid_audio = np.random.randn(processor.sample_rate)
        assert processor.validate_audio(valid_audio) is True

    def test_supported_formats(self, processor):
        """Test that all expected formats are supported."""
        expected_formats = {'.wav', '.mp3', '.flac', '.aiff', '.aif', '.ogg', '.m4a'}
        assert processor.SUPPORTED_FORMATS == expected_formats

    def test_load_audio_normalizes_to_mono(self, processor, temp_wav_file):
        """Test that loaded audio is converted to mono."""
        audio_data, _ = processor.load_audio(temp_wav_file)

        # Audio should be 1D (mono)
        assert audio_data.ndim == 1

    def test_load_audio_resamples_correctly(self):
        """Test that audio is resampled to target sample rate."""
        import soundfile as sf

        # Create audio at 44100 Hz
        original_sr = 44100
        duration = 1.0
        t = np.linspace(0, duration, int(original_sr * duration))
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name

        try:
            sf.write(temp_path, audio, original_sr)

            # Load with 22050 Hz processor
            processor = AudioProcessor(sample_rate=22050)
            loaded_audio, loaded_sr = processor.load_audio(temp_path)

            assert loaded_sr == 22050
            # Audio should be approximately half the original length
            assert abs(len(loaded_audio) - 22050) < 100

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestAudioProcessorEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_short_audio_file(self):
        """Test loading a very short audio file."""
        import soundfile as sf

        processor = AudioProcessor()

        # Create 0.5 second audio
        sample_rate = 22050
        audio = np.random.randn(sample_rate // 2).astype(np.float32)

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name

        try:
            sf.write(temp_path, audio, sample_rate)
            loaded_audio, _ = processor.load_audio(temp_path)

            # Should load successfully but fail validation
            assert len(loaded_audio) > 0
            assert not processor.validate_audio(loaded_audio)

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_very_quiet_audio(self):
        """Test audio with very low amplitude."""
        processor = AudioProcessor()

        # Create very quiet audio
        quiet_audio = np.random.randn(processor.sample_rate * 2) * 0.0001

        # Should still be valid (not all zeros)
        assert processor.validate_audio(quiet_audio) is True

    def test_clipped_audio(self):
        """Test audio with clipping (values at extremes)."""
        processor = AudioProcessor()

        # Create clipped audio
        clipped_audio = np.ones(processor.sample_rate * 2)

        # Should still be valid
        assert processor.validate_audio(clipped_audio) is True
