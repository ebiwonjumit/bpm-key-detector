"""
Unit tests for batch processing functionality.
"""

import pytest
import tempfile
import os
import json
import csv
from pathlib import Path

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analyzer import analyze_batch, save_results, display_batch_summary, AudioAnalyzer
from rich.console import Console


class TestBatchProcessing:
    """Test suite for batch processing functions."""

    @pytest.fixture
    def analyzer(self):
        """Create an AudioAnalyzer instance."""
        return AudioAnalyzer(verbose=False)

    @pytest.fixture
    def console(self):
        """Create a Rich console instance."""
        return Console()

    @pytest.fixture
    def sample_audio_files(self):
        """Create multiple temporary audio files for testing."""
        import soundfile as sf
        import numpy as np

        files = []
        sample_rate = 22050

        for i in range(3):
            duration = 2.0
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio = 0.5 * np.sin(2 * np.pi * (440 + i * 50) * t)

            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                temp_path = f.name
                files.append(temp_path)

            sf.write(temp_path, audio, sample_rate)

        yield files

        # Cleanup
        for file_path in files:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_analyze_batch_success(self, analyzer, sample_audio_files, console):
        """Test successful batch analysis of multiple files."""
        results = analyze_batch(analyzer, sample_audio_files, continue_on_error=False, console=console)

        assert len(results) == 3
        for result in results:
            assert 'bpm' in result
            assert 'key_string' in result
            assert result['bpm'] > 0

    def test_analyze_batch_with_invalid_file(self, analyzer, sample_audio_files, console):
        """Test batch analysis with an invalid file."""
        # Add an invalid file to the list
        invalid_file = '/nonexistent/file.wav'
        file_list = sample_audio_files + [invalid_file]

        # Should raise an error without continue_on_error
        with pytest.raises(Exception):
            analyze_batch(analyzer, file_list, continue_on_error=False, console=console)

    def test_analyze_batch_continue_on_error(self, analyzer, sample_audio_files, console):
        """Test batch analysis with continue_on_error flag."""
        # Add an invalid file
        invalid_file = '/nonexistent/file.wav'
        file_list = sample_audio_files + [invalid_file]

        # Should continue and return results for valid files
        results = analyze_batch(analyzer, file_list, continue_on_error=True, console=console)

        # Should have results for 3 valid files
        assert len(results) == 3

    def test_analyze_batch_empty_list(self, analyzer, console):
        """Test batch analysis with empty file list."""
        results = analyze_batch(analyzer, [], continue_on_error=False, console=console)

        assert len(results) == 0

    def test_save_results_json(self, sample_audio_files, console):
        """Test saving results to JSON file."""
        # Create sample results
        results = [
            {'file': 'song1.mp3', 'bpm': 120.5, 'key_string': 'C major'},
            {'file': 'song2.mp3', 'bpm': 128.0, 'key_string': 'D minor'}
        ]

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            output_path = f.name

        try:
            save_results(results, output_path, console)

            # Verify file exists and contains correct data
            assert os.path.exists(output_path)

            with open(output_path, 'r') as f:
                loaded_data = json.load(f)

            assert len(loaded_data) == 2
            assert loaded_data[0]['bpm'] == 120.5
            assert loaded_data[1]['key_string'] == 'D minor'

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_save_results_csv(self, console):
        """Test saving results to CSV file."""
        results = [
            {
                'file': 'song1.mp3',
                'bpm': 120.5,
                'bpm_confidence': 0.85,
                'bpm_confidence_level': 'High',
                'key': 'C',
                'mode': 'major',
                'key_string': 'C major',
                'key_confidence': 0.75,
                'key_confidence_level': 'High',
                'duration': 180.5,
                'analysis_time': 2.3
            },
            {
                'file': 'song2.mp3',
                'bpm': 128.0,
                'bpm_confidence': 0.92,
                'bpm_confidence_level': 'High',
                'key': 'D',
                'mode': 'minor',
                'key_string': 'D minor',
                'key_confidence': 0.68,
                'key_confidence_level': 'Medium',
                'duration': 210.0,
                'analysis_time': 2.8
            }
        ]

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            output_path = f.name

        try:
            save_results(results, output_path, console)

            # Verify file exists and contains correct data
            assert os.path.exists(output_path)

            with open(output_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            assert len(rows) == 2
            assert float(rows[0]['bpm']) == 120.5
            assert rows[0]['key_string'] == 'C major'
            assert float(rows[1]['bpm']) == 128.0
            assert rows[1]['key_string'] == 'D minor'

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_save_results_empty_list(self, console):
        """Test saving empty results list."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            output_path = f.name

        try:
            save_results([], output_path, console)

            # File should exist but be empty array
            with open(output_path, 'r') as f:
                data = json.load(f)

            assert len(data) == 0

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_display_batch_summary(self, console):
        """Test displaying batch summary table."""
        results = [
            {
                'file': 'song1.mp3',
                'bpm': 120.5,
                'key_string': 'C major',
                'bpm_confidence_level': 'High',
                'key_confidence_level': 'High'
            },
            {
                'file': 'song2.mp3',
                'bpm': 128.0,
                'key_string': 'D minor',
                'bpm_confidence_level': 'High',
                'key_confidence_level': 'Medium'
            }
        ]

        # Should not raise any errors
        try:
            display_batch_summary(results, console)
        except Exception as e:
            pytest.fail(f"display_batch_summary raised unexpected exception: {e}")


class TestBatchCLIIntegration:
    """Integration tests for batch processing via CLI."""

    @pytest.fixture
    def sample_audio_files(self):
        """Create sample audio files."""
        import soundfile as sf
        import numpy as np

        files = []
        sample_rate = 22050

        for i in range(2):
            duration = 2.0
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio = 0.5 * np.sin(2 * np.pi * 440 * t)

            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                temp_path = f.name
                files.append(temp_path)

            sf.write(temp_path, audio, sample_rate)

        yield files

        for file_path in files:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_cli_batch_with_wildcard(self, sample_audio_files):
        """Test CLI batch processing with file pattern."""
        from analyzer import main
        import sys

        # Get directory containing files
        file_dir = os.path.dirname(sample_audio_files[0])
        pattern = os.path.join(file_dir, '*.wav')

        # Mock sys.argv
        old_argv = sys.argv
        try:
            sys.argv = ['analyzer.py', '--batch'] + sample_audio_files

            # Should not raise an error
            exit_code = main()
            assert exit_code == 0

        finally:
            sys.argv = old_argv

    def test_cli_dir_processing(self, sample_audio_files):
        """Test CLI directory processing."""
        from analyzer import main
        import sys

        file_dir = os.path.dirname(sample_audio_files[0])

        old_argv = sys.argv
        try:
            sys.argv = ['analyzer.py', '--dir', file_dir]

            exit_code = main()
            assert exit_code == 0

        finally:
            sys.argv = old_argv


class TestBatchEdgeCases:
    """Test edge cases for batch processing."""

    def test_large_batch(self, analyzer, console):
        """Test batch processing with many files."""
        # Create a large list of (non-existent) files
        large_list = [f'file{i}.mp3' for i in range(100)]

        # With continue_on_error, should handle all files
        results = analyze_batch(analyzer, large_list, continue_on_error=True, console=console)

        # All should fail, so results should be empty
        assert len(results) == 0

    def test_mixed_file_formats(self):
        """Test batch processing with different audio formats."""
        import soundfile as sf
        import numpy as np

        files = []
        sample_rate = 22050

        # Create files with different extensions
        for ext in ['.wav', '.flac']:
            duration = 2.0
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio = 0.5 * np.sin(2 * np.pi * 440 * t)

            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as f:
                temp_path = f.name
                files.append(temp_path)

            sf.write(temp_path, audio, sample_rate, format=ext[1:].upper())

        try:
            analyzer = AudioAnalyzer(verbose=False)
            console = Console()

            results = analyze_batch(analyzer, files, continue_on_error=True, console=console)

            # Should successfully analyze both formats
            assert len(results) == 2

        finally:
            for file_path in files:
                if os.path.exists(file_path):
                    os.remove(file_path)
