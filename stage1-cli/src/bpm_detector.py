"""
BPM detection module using librosa's tempo estimation.
Analyzes onset strength envelope to determine tempo.
"""

import numpy as np
import librosa
from typing import Optional, Tuple


class BPMDetector:
    """Detects BPM (tempo) from audio data."""

    def __init__(self, sample_rate: int = 22050):
        """
        Initialize the BPM detector.

        Args:
            sample_rate: Sample rate of the audio data
        """
        self.sample_rate = sample_rate

    def detect(self, audio_data: np.ndarray) -> Tuple[float, float]:
        """
        Detect the BPM of the audio.

        Args:
            audio_data: Audio data as numpy array

        Returns:
            Tuple of (bpm, confidence)
            - bpm: Detected tempo in beats per minute
            - confidence: Confidence score (0-1)

        Raises:
            ValueError: If audio data is invalid
        """
        if audio_data is None or len(audio_data) == 0:
            raise ValueError("Audio data is empty")

        if len(audio_data) < self.sample_rate:
            raise ValueError("Audio data is too short (minimum 1 second)")

        try:
            # Calculate onset strength envelope
            onset_env = librosa.onset.onset_strength(
                y=audio_data,
                sr=self.sample_rate
            )

            # Estimate tempo using onset strength
            # Returns array of tempo estimates, we take the first (primary) tempo
            tempo = librosa.feature.tempo(
                onset_envelope=onset_env,
                sr=self.sample_rate
            )

            # Extract the primary tempo value
            bpm = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)

            # Calculate confidence based on onset strength analysis
            confidence = self._calculate_confidence(onset_env, bpm)

            return bpm, confidence

        except Exception as e:
            raise RuntimeError(f"Error detecting BPM: {str(e)}") from e

    def _calculate_confidence(self, onset_env: np.ndarray, bpm: float) -> float:
        """
        Calculate confidence score for the detected BPM.

        Args:
            onset_env: Onset strength envelope
            bpm: Detected BPM

        Returns:
            Confidence score between 0 and 1
        """
        try:
            # Use autocorrelation to measure periodicity
            autocorr = librosa.autocorrelate(onset_env)

            # Find the peak corresponding to the detected BPM
            # Convert BPM to frames
            hop_length = 512
            frames_per_beat = 60 * self.sample_rate / (bpm * hop_length)

            # Get autocorrelation value at the detected period
            if frames_per_beat < len(autocorr):
                idx = int(frames_per_beat)
                peak_value = autocorr[idx]
                max_value = np.max(autocorr[1:])  # Exclude zero lag

                if max_value > 0:
                    confidence = min(abs(peak_value / max_value), 1.0)
                else:
                    confidence = 0.5
            else:
                confidence = 0.5

            # Normalize confidence to be between 0 and 1
            confidence = max(0.0, min(1.0, confidence))

            return confidence

        except Exception:
            # If confidence calculation fails, return a neutral value
            return 0.5

    def detect_with_multiple_estimates(self, audio_data: np.ndarray,
                                       n_estimates: int = 2) -> Tuple[float, float, list]:
        """
        Detect BPM with multiple tempo estimates.

        Args:
            audio_data: Audio data as numpy array
            n_estimates: Number of tempo estimates to return

        Returns:
            Tuple of (primary_bpm, confidence, alternative_bpms)
        """
        if audio_data is None or len(audio_data) == 0:
            raise ValueError("Audio data is empty")

        try:
            # Calculate onset strength envelope
            onset_env = librosa.onset.onset_strength(
                y=audio_data,
                sr=self.sample_rate
            )

            # Get multiple tempo estimates
            tempos = librosa.feature.tempo(
                onset_envelope=onset_env,
                sr=self.sample_rate,
                aggregate=None  # Get all estimates
            )

            # Convert to list and sort by likelihood
            tempo_list = sorted(tempos.flatten(), reverse=True)[:n_estimates]

            # Primary tempo is the first one
            primary_bpm = float(tempo_list[0])

            # Calculate confidence
            confidence = self._calculate_confidence(onset_env, primary_bpm)

            # Alternative tempos
            alternatives = [float(t) for t in tempo_list[1:]]

            return primary_bpm, confidence, alternatives

        except Exception as e:
            raise RuntimeError(f"Error detecting BPM: {str(e)}") from e

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
        elif confidence >= 0.4:
            return "Medium"
        else:
            return "Low"

    def validate_bpm(self, bpm: float) -> bool:
        """
        Validate that a BPM value is reasonable.

        Args:
            bpm: BPM value to validate

        Returns:
            True if valid, False otherwise
        """
        # Typical music BPM range is 40-240
        return 40.0 <= bpm <= 240.0
