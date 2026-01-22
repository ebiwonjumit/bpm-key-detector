"""
Musical key detection module using chromagram analysis.
Implements Krumhansl-Schmuckler key-finding algorithm.
"""

import numpy as np
import librosa
from typing import Tuple


class KeyDetector:
    """Detects musical key from audio data."""

    # Krumhansl-Schmuckler key profiles
    # Major key profile (correlation weights for each pitch class)
    MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])

    # Minor key profile
    MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

    # Pitch class names
    PITCH_CLASSES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __init__(self, sample_rate: int = 22050):
        """
        Initialize the key detector.

        Args:
            sample_rate: Sample rate of the audio data
        """
        self.sample_rate = sample_rate

    def detect(self, audio_data: np.ndarray) -> Tuple[str, str, float]:
        """
        Detect the musical key of the audio.

        Args:
            audio_data: Audio data as numpy array

        Returns:
            Tuple of (key, mode, confidence)
            - key: Root note (C, C#, D, etc.)
            - mode: "major" or "minor"
            - confidence: Confidence score (0-1)

        Raises:
            ValueError: If audio data is invalid
        """
        if audio_data is None or len(audio_data) == 0:
            raise ValueError("Audio data is empty")

        if len(audio_data) < self.sample_rate:
            raise ValueError("Audio data is too short (minimum 1 second)")

        try:
            # Compute chromagram
            chroma = librosa.feature.chroma_cqt(
                y=audio_data,
                sr=self.sample_rate,
                hop_length=512
            )

            # Average across time to get pitch class distribution
            pitch_class_distribution = np.mean(chroma, axis=1)

            # Normalize the distribution
            pitch_class_distribution = pitch_class_distribution / np.sum(pitch_class_distribution)

            # Find best matching key using Krumhansl-Schmuckler algorithm
            key, mode, confidence = self._find_best_key(pitch_class_distribution)

            return key, mode, confidence

        except Exception as e:
            raise RuntimeError(f"Error detecting key: {str(e)}") from e

    def _find_best_key(self, pitch_distribution: np.ndarray) -> Tuple[str, str, float]:
        """
        Find the best matching key using correlation with key profiles.

        Args:
            pitch_distribution: Normalized pitch class distribution

        Returns:
            Tuple of (key, mode, confidence)
        """
        max_correlation = -1
        best_key = 'C'
        best_mode = 'major'

        # Try all 12 keys in both major and minor
        for i in range(12):
            # Rotate the profiles to match each key
            major_profile = np.roll(self.MAJOR_PROFILE, i)
            minor_profile = np.roll(self.MINOR_PROFILE, i)

            # Calculate correlation with major profile
            major_corr = self._correlation(pitch_distribution, major_profile)

            # Calculate correlation with minor profile
            minor_corr = self._correlation(pitch_distribution, minor_profile)

            # Check if major key is the best so far
            if major_corr > max_correlation:
                max_correlation = major_corr
                best_key = self.PITCH_CLASSES[i]
                best_mode = 'major'

            # Check if minor key is the best so far
            if minor_corr > max_correlation:
                max_correlation = minor_corr
                best_key = self.PITCH_CLASSES[i]
                best_mode = 'minor'

        # Normalize correlation to 0-1 confidence range
        confidence = (max_correlation + 1) / 2  # Correlation ranges from -1 to 1

        return best_key, best_mode, confidence

    def _correlation(self, x: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate Pearson correlation coefficient.

        Args:
            x: First array
            y: Second array

        Returns:
            Correlation coefficient
        """
        # Normalize arrays
        x_normalized = (x - np.mean(x)) / (np.std(x) + 1e-10)
        y_normalized = (y - np.mean(y)) / (np.std(y) + 1e-10)

        # Calculate correlation
        correlation = np.mean(x_normalized * y_normalized)

        return correlation

    def get_key_string(self, key: str, mode: str) -> str:
        """
        Format key and mode as a readable string.

        Args:
            key: Root note
            mode: "major" or "minor"

        Returns:
            Formatted key string (e.g., "C major", "A minor")
        """
        return f"{key} {mode}"

    def get_confidence_level(self, confidence: float) -> str:
        """
        Convert confidence score to a human-readable level.

        Args:
            confidence: Confidence score (0-1)

        Returns:
            Confidence level string: "Low", "Medium", or "High"
        """
        if confidence >= 0.7:
            return "High"
        elif confidence >= 0.5:
            return "Medium"
        else:
            return "Low"

    def get_relative_keys(self, key: str, mode: str) -> dict:
        """
        Get related keys (relative, parallel, dominant).

        Args:
            key: Root note
            mode: "major" or "minor"

        Returns:
            Dictionary with related keys
        """
        key_idx = self.PITCH_CLASSES.index(key)

        result = {}

        if mode == 'major':
            # Relative minor (6 semitones down)
            relative_idx = (key_idx - 3) % 12
            result['relative'] = f"{self.PITCH_CLASSES[relative_idx]} minor"

            # Parallel minor (same root)
            result['parallel'] = f"{key} minor"

            # Dominant (5 semitones up)
            dominant_idx = (key_idx + 7) % 12
            result['dominant'] = f"{self.PITCH_CLASSES[dominant_idx]} major"

        else:  # minor
            # Relative major (3 semitones up)
            relative_idx = (key_idx + 3) % 12
            result['relative'] = f"{self.PITCH_CLASSES[relative_idx]} major"

            # Parallel major (same root)
            result['parallel'] = f"{key} major"

            # Dominant (7 semitones up)
            dominant_idx = (key_idx + 7) % 12
            result['dominant'] = f"{self.PITCH_CLASSES[dominant_idx]} minor"

        return result

    def get_scale_notes(self, key: str, mode: str) -> list:
        """
        Get the notes in the scale for the given key.

        Args:
            key: Root note
            mode: "major" or "minor"

        Returns:
            List of notes in the scale
        """
        key_idx = self.PITCH_CLASSES.index(key)

        if mode == 'major':
            # Major scale intervals: W W H W W W H (2 2 1 2 2 2 1)
            intervals = [0, 2, 4, 5, 7, 9, 11]
        else:  # natural minor
            # Natural minor scale intervals: W H W W H W W (2 1 2 2 1 2 2)
            intervals = [0, 2, 3, 5, 7, 8, 10]

        scale = [self.PITCH_CLASSES[(key_idx + interval) % 12] for interval in intervals]

        return scale
