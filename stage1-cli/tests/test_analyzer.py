"""
Integration tests for the analyzer module.
"""

import pytest
import numpy as np
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analyzer import AudioAnalyzer


class TestAudioAnalyzer:
    """Test suite for AudioAnalyzer class."""

    @pytest.fixture
    def analyzer(self):
        """Create an AudioAnalyzer instance for testing."""
        return AudioAnalyzer(verbose=False)

    @pytest.fixture
    def verbose_analyzer(self):
        """Create a verbose AudioAnalyzer instance for testing."""
        return AudioAnalyzer(verbose=True)

    @pytest.fixture
    def sample_audio_file(self):
        """Create a temporary audio file for testing."""
        import soundfile as sf

        sample_rate = 22050
        duration = 3.0
        t = np.linspace(0, duration, int(sample_rate * duration))

        # Create audio with clear beat pattern
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name

        sf.write(temp_path, audio, sample_rate)

        yield temp_path

        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

    def test_init_default(self):
        """Test initialization with default parameters."""
        analyzer = AudioAnalyzer()

        assert analyzer.verbose is False
        assert analyzer.audio_processor is not None
        assert analyzer.bpm_detector is not None
        assert analyzer.key_detector is not None

    def test_init_verbose(self):
        """Test initialization with verbose mode."""
        analyzer = AudioAnalyzer(verbose=True)

        assert analyzer.verbose is True

    def test_analyze_file_success(self, analyzer, sample_audio_file):
        """Test successful file analysis."""
        results = analyzer.analyze_file(sample_audio_file)

        # Check that all expected keys are present
        assert 'file' in results
        assert 'bpm' in results
        assert 'bpm_confidence' in results
        assert 'bpm_confidence_level' in results
        assert 'key' in results
        assert 'mode' in results
        assert 'key_string' in results
        assert 'key_confidence' in results
        assert 'key_confidence_level' in results
        assert 'analysis_time' in results
        assert 'duration' in results

        # Check value types
        assert isinstance(results['bpm'], float)
        assert isinstance(results['bpm_confidence'], float)
        assert isinstance(results['key'], str)
        assert isinstance(results['mode'], str)
        assert results['mode'] in ['major', 'minor']
        assert isinstance(results['analysis_time'], float)

        # Check value ranges
        assert results['bpm'] > 0
        assert 0.0 <= results['bpm_confidence'] <= 1.0
        assert 0.0 <= results['key_confidence'] <= 1.0
        assert results['analysis_time'] > 0

    def test_analyze_file_verbose(self, verbose_analyzer, sample_audio_file):
        """Test file analysis with verbose mode."""
        results = verbose_analyzer.analyze_file(sample_audio_file)

        # Verbose mode should include additional information
        assert 'scale_notes' in results
        assert 'relative_keys' in results

        assert isinstance(results['scale_notes'], list)
        assert len(results['scale_notes']) == 7

        assert isinstance(results['relative_keys'], dict)
        assert 'relative' in results['relative_keys']
        assert 'parallel' in results['relative_keys']
        assert 'dominant' in results['relative_keys']

    def test_analyze_file_not_found(self, analyzer):
        """Test analysis of non-existent file."""
        with pytest.raises(FileNotFoundError):
            analyzer.analyze_file('/nonexistent/path/to/file.wav')

    def test_analyze_file_unsupported_format(self, analyzer):
        """Test analysis of unsupported file format."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_path = f.name
            f.write(b'not an audio file')

        try:
            with pytest.raises(ValueError):
                analyzer.analyze_file(temp_path)
        finally:
            os.remove(temp_path)

    def test_analyze_file_too_short(self, analyzer):
        """Test analysis of too short audio file."""
        import soundfile as sf

        # Create 0.5 second audio (too short)
        sample_rate = 22050
        audio = np.random.randn(sample_rate // 2).astype(np.float32)

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name

        try:
            sf.write(temp_path, audio, sample_rate)

            with pytest.raises(ValueError, match="too short"):
                analyzer.analyze_file(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    @patch('analyzer.AudioProcessor.record_audio')
    def test_analyze_microphone_success(self, mock_record, analyzer):
        """Test successful microphone analysis."""
        # Mock the recording to return sample audio
        sample_rate = 22050
        duration = 3.0
        t = np.linspace(0, duration, int(sample_rate * duration))
        mock_audio = 0.5 * np.sin(2 * np.pi * 440 * t)

        mock_record.return_value = (mock_audio, sample_rate)

        results = analyzer.analyze_microphone(duration=3.0)

        # Check that all expected keys are present
        assert 'source' in results
        assert results['source'] == 'microphone'
        assert 'bpm' in results
        assert 'key' in results
        assert 'mode' in results
        assert 'duration' in results

        # Check value types and ranges
        assert isinstance(results['bpm'], float)
        assert results['bpm'] > 0
        assert results['mode'] in ['major', 'minor']

        # Verify record_audio was called with correct duration
        mock_record.assert_called_once_with(3.0)

    @patch('analyzer.AudioProcessor.record_audio')
    def test_analyze_microphone_verbose(self, mock_record, verbose_analyzer):
        """Test microphone analysis with verbose mode."""
        # Mock the recording
        sample_rate = 22050
        duration = 3.0
        t = np.linspace(0, duration, int(sample_rate * duration))
        mock_audio = 0.5 * np.sin(2 * np.pi * 440 * t)

        mock_record.return_value = (mock_audio, sample_rate)

        results = verbose_analyzer.analyze_microphone(duration=3.0)

        # Verbose mode should include additional information
        assert 'scale_notes' in results
        assert 'relative_keys' in results

    def test_analyze_microphone_invalid_duration(self, analyzer):
        """Test microphone analysis with invalid duration."""
        with pytest.raises(ValueError):
            analyzer.analyze_microphone(duration=0)

        with pytest.raises(ValueError):
            analyzer.analyze_microphone(duration=-5)

        with pytest.raises(ValueError):
            analyzer.analyze_microphone(duration=400)

    def test_display_results_normal(self, analyzer, sample_audio_file):
        """Test displaying results in normal mode."""
        results = analyzer.analyze_file(sample_audio_file)

        # Should not raise any errors
        try:
            analyzer.display_results(results)
        except Exception as e:
            pytest.fail(f"display_results raised unexpected exception: {e}")

    def test_display_results_verbose(self, verbose_analyzer, sample_audio_file):
        """Test displaying results in verbose mode."""
        results = verbose_analyzer.analyze_file(sample_audio_file)

        # Should not raise any errors
        try:
            verbose_analyzer.display_results(results)
        except Exception as e:
            pytest.fail(f"display_results raised unexpected exception: {e}")

    def test_display_results_with_all_keys(self, analyzer):
        """Test displaying results with all expected keys."""
        # Create mock results
        results = {
            'file': 'test.wav',
            'bpm': 120.5,
            'bpm_confidence': 0.85,
            'bpm_confidence_level': 'High',
            'key': 'C',
            'mode': 'major',
            'key_string': 'C major',
            'key_confidence': 0.72,
            'key_confidence_level': 'High',
            'analysis_time': 1.23,
            'duration': 3.0
        }

        # Should not raise any errors
        try:
            analyzer.display_results(results)
        except Exception as e:
            pytest.fail(f"display_results raised unexpected exception: {e}")


class TestAudioAnalyzerCLI:
    """Test the CLI functionality."""

    @pytest.fixture
    def sample_audio_file(self):
        """Create a temporary audio file for testing."""
        import soundfile as sf

        sample_rate = 22050
        duration = 3.0
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name

        sf.write(temp_path, audio, sample_rate)

        yield temp_path

        if os.path.exists(temp_path):
            os.remove(temp_path)

    def test_main_with_file(self, sample_audio_file):
        """Test main function with file argument."""
        from analyzer import main

        with patch('sys.argv', ['analyzer.py', '--file', sample_audio_file]):
            exit_code = main()
            assert exit_code == 0

    def test_main_with_nonexistent_file(self):
        """Test main function with non-existent file."""
        from analyzer import main

        with patch('sys.argv', ['analyzer.py', '--file', '/nonexistent/file.wav']):
            exit_code = main()
            assert exit_code == 1

    def test_main_with_verbose(self, sample_audio_file):
        """Test main function with verbose flag."""
        from analyzer import main

        with patch('sys.argv', ['analyzer.py', '--file', sample_audio_file, '--verbose']):
            exit_code = main()
            assert exit_code == 0

    @patch('analyzer.AudioProcessor.record_audio')
    def test_main_with_mic(self, mock_record):
        """Test main function with microphone input."""
        from analyzer import main

        # Mock the recording
        sample_rate = 22050
        duration = 3.0
        t = np.linspace(0, duration, int(sample_rate * duration))
        mock_audio = 0.5 * np.sin(2 * np.pi * 440 * t)

        mock_record.return_value = (mock_audio, sample_rate)

        with patch('sys.argv', ['analyzer.py', '--mic']):
            exit_code = main()
            assert exit_code == 0

    @patch('analyzer.AudioProcessor.record_audio')
    def test_main_with_mic_custom_duration(self, mock_record):
        """Test main function with custom recording duration."""
        from analyzer import main

        # Mock the recording
        sample_rate = 22050
        duration = 15.0
        t = np.linspace(0, duration, int(sample_rate * duration))
        mock_audio = 0.5 * np.sin(2 * np.pi * 440 * t)

        mock_record.return_value = (mock_audio, sample_rate)

        with patch('sys.argv', ['analyzer.py', '--mic', '--duration', '15']):
            exit_code = main()
            assert exit_code == 0

    def test_main_keyboard_interrupt(self, sample_audio_file):
        """Test main function handles keyboard interrupt."""
        from analyzer import main

        with patch('sys.argv', ['analyzer.py', '--file', sample_audio_file]):
            with patch('analyzer.AudioAnalyzer.analyze_file', side_effect=KeyboardInterrupt):
                exit_code = main()
                assert exit_code == 130


class TestAudioAnalyzerIntegration:
    """Integration tests that verify the entire pipeline."""

    def test_complete_file_analysis_pipeline(self):
        """Test the complete pipeline from file loading to results."""
        import soundfile as sf

        # Create a test audio file with known properties
        sample_rate = 22050
        duration = 5.0
        t = np.linspace(0, duration, int(sample_rate * duration))

        # Create audio with C major chord
        audio = (
            0.33 * np.sin(2 * np.pi * 261.63 * t) +  # C4
            0.33 * np.sin(2 * np.pi * 329.63 * t) +  # E4
            0.33 * np.sin(2 * np.pi * 392.00 * t)    # G4
        )

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name

        try:
            sf.write(temp_path, audio, sample_rate)

            analyzer = AudioAnalyzer(verbose=True)
            results = analyzer.analyze_file(temp_path)

            # Verify complete results structure
            assert all(key in results for key in [
                'file', 'bpm', 'bpm_confidence', 'key', 'mode',
                'key_string', 'analysis_time', 'duration',
                'scale_notes', 'relative_keys'
            ])

            # Verify results are reasonable
            assert 40 <= results['bpm'] <= 240
            assert results['key'] in ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            assert len(results['scale_notes']) == 7
            assert results['duration'] > 4.0

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_error_handling_chain(self):
        """Test that errors propagate correctly through the system."""
        analyzer = AudioAnalyzer()

        # Test with various error conditions
        with pytest.raises(FileNotFoundError):
            analyzer.analyze_file('/nonexistent/file.wav')

        with pytest.raises(ValueError):
            analyzer.analyze_microphone(duration=-1)

    def test_multiple_analyses(self):
        """Test performing multiple analyses in sequence."""
        import soundfile as sf

        analyzer = AudioAnalyzer()

        # Create multiple test files
        files = []
        for i in range(3):
            sample_rate = 22050
            duration = 2.0
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio = 0.5 * np.sin(2 * np.pi * (440 + i * 50) * t)

            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                temp_path = f.name
                files.append(temp_path)

            sf.write(temp_path, audio, sample_rate)

        try:
            # Analyze all files
            all_results = []
            for file_path in files:
                results = analyzer.analyze_file(file_path)
                all_results.append(results)

            # Verify all analyses completed
            assert len(all_results) == 3

            for results in all_results:
                assert results['bpm'] > 0
                assert results['key'] in ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        finally:
            for file_path in files:
                if os.path.exists(file_path):
                    os.remove(file_path)
