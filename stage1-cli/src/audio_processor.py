"""
Audio processing module for loading and recording audio.
Handles file I/O and microphone input.
"""

import numpy as np
import librosa
import soundfile as sf
import sounddevice as sd
from pathlib import Path
from typing import Tuple, Optional


class AudioProcessor:
    """Handles audio file loading and microphone recording."""

    SUPPORTED_FORMATS = {'.wav', '.mp3', '.flac', '.aiff', '.aif', '.ogg', '.m4a'}
    DEFAULT_SAMPLE_RATE = 22050

    def __init__(self, sample_rate: int = DEFAULT_SAMPLE_RATE):
        """
        Initialize the audio processor.

        Args:
            sample_rate: Target sample rate for audio processing
        """
        self.sample_rate = sample_rate

    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Load an audio file and return the audio data and sample rate.

        Args:
            file_path: Path to the audio file

        Returns:
            Tuple of (audio_data, sample_rate)

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is not supported
            RuntimeError: If there's an error loading the file
        """
        path = Path(file_path)

        # Check if file exists
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        # Check if format is supported
        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported audio format: {path.suffix}. "
                f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
            )

        try:
            # Load audio file with librosa
            # Convert to mono and resample to target sample rate
            audio_data, sr = librosa.load(
                file_path,
                sr=self.sample_rate,
                mono=True
            )

            # Validate audio data
            if len(audio_data) == 0:
                raise RuntimeError("Loaded audio file is empty")

            return audio_data, sr

        except Exception as e:
            if isinstance(e, (FileNotFoundError, ValueError, RuntimeError)):
                raise
            raise RuntimeError(f"Error loading audio file: {str(e)}") from e

    def record_audio(self, duration: float = 10.0) -> Tuple[np.ndarray, int]:
        """
        Record audio from the microphone.

        Args:
            duration: Recording duration in seconds

        Returns:
            Tuple of (audio_data, sample_rate)

        Raises:
            ValueError: If duration is invalid
            RuntimeError: If there's an error recording audio
        """
        if duration <= 0:
            raise ValueError("Duration must be positive")

        if duration > 300:  # 5 minutes max
            raise ValueError("Duration cannot exceed 300 seconds")

        try:
            # Record audio from default microphone
            audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32'
            )

            # Wait for recording to complete
            sd.wait()

            # Convert to 1D array and ensure it's not empty
            audio_data = audio_data.flatten()

            if len(audio_data) == 0:
                raise RuntimeError("Recorded audio is empty")

            return audio_data, self.sample_rate

        except Exception as e:
            if isinstance(e, (ValueError, RuntimeError)):
                raise
            raise RuntimeError(f"Error recording audio: {str(e)}") from e

    def save_audio(self, audio_data: np.ndarray, file_path: str,
                   sample_rate: Optional[int] = None) -> None:
        """
        Save audio data to a file.

        Args:
            audio_data: Audio data as numpy array
            file_path: Output file path
            sample_rate: Sample rate (uses default if not specified)

        Raises:
            ValueError: If audio data is invalid
            RuntimeError: If there's an error saving the file
        """
        if audio_data is None or len(audio_data) == 0:
            raise ValueError("Audio data is empty")

        sr = sample_rate or self.sample_rate

        try:
            sf.write(file_path, audio_data, sr)
        except Exception as e:
            raise RuntimeError(f"Error saving audio file: {str(e)}") from e

    def get_duration(self, audio_data: np.ndarray) -> float:
        """
        Get the duration of audio data in seconds.

        Args:
            audio_data: Audio data as numpy array

        Returns:
            Duration in seconds
        """
        return len(audio_data) / self.sample_rate

    def validate_audio(self, audio_data: np.ndarray) -> bool:
        """
        Validate that audio data is suitable for analysis.

        Args:
            audio_data: Audio data as numpy array

        Returns:
            True if valid, False otherwise
        """
        if audio_data is None or len(audio_data) == 0:
            return False

        # Check minimum duration (at least 1 second)
        if len(audio_data) < self.sample_rate:
            return False

        # Check if audio is all zeros (silence)
        if np.all(audio_data == 0):
            return False

        return True
