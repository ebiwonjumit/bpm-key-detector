#!/usr/bin/env python3
"""
Audio Analyzer CLI - BPM and Key Detection Tool

Command-line interface for analyzing audio files and microphone input
to detect BPM (tempo) and musical key.
"""

import argparse
import sys
import time
import json
import numpy as np
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table

from audio_processor import AudioProcessor
from bpm_detector import BPMDetector
from key_detector import KeyDetector


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types."""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


class AudioAnalyzer:
    """Main analyzer class that coordinates audio processing and analysis."""

    def __init__(self, verbose: bool = False):
        """
        Initialize the analyzer.

        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose
        self.console = Console()

        # Initialize processors and detectors
        self.audio_processor = AudioProcessor()
        self.bpm_detector = BPMDetector()
        self.key_detector = KeyDetector()

    def analyze_file(self, file_path: str) -> dict:
        """
        Analyze an audio file.

        Args:
            file_path: Path to the audio file

        Returns:
            Dictionary with analysis results

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
            RuntimeError: If analysis fails
        """
        start_time = time.time()

        # Display file being analyzed
        self.console.print(f"\n[bold cyan]Analyzing:[/bold cyan] {Path(file_path).name}")
        self.console.print("━" * 60)

        # Load audio file
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            progress.add_task(description="Loading audio file...", total=None)
            audio_data, sample_rate = self.audio_processor.load_audio(file_path)

        if self.verbose:
            duration = self.audio_processor.get_duration(audio_data)
            self.console.print(f"[dim]Duration: {duration:.2f}s | Sample rate: {sample_rate}Hz[/dim]")

        # Validate audio
        if not self.audio_processor.validate_audio(audio_data):
            raise ValueError("Audio file is invalid or too short for analysis")

        # Detect BPM
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            progress.add_task(description="Detecting BPM...", total=None)
            bpm, bpm_confidence = self.bpm_detector.detect(audio_data)

        # Detect Key
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            progress.add_task(description="Detecting key...", total=None)
            key, mode, key_confidence = self.key_detector.detect(audio_data)

        end_time = time.time()
        analysis_time = end_time - start_time

        # Prepare results
        results = {
            'file': file_path,
            'bpm': bpm,
            'bpm_confidence': bpm_confidence,
            'bpm_confidence_level': self.bpm_detector.get_confidence_level(bpm_confidence),
            'key': key,
            'mode': mode,
            'key_string': self.key_detector.get_key_string(key, mode),
            'key_confidence': key_confidence,
            'key_confidence_level': self.key_detector.get_confidence_level(key_confidence),
            'analysis_time': analysis_time,
            'duration': self.audio_processor.get_duration(audio_data)
        }

        if self.verbose:
            results['scale_notes'] = self.key_detector.get_scale_notes(key, mode)
            results['relative_keys'] = self.key_detector.get_relative_keys(key, mode)

        return results

    def analyze_microphone(self, duration: float = 10.0) -> dict:
        """
        Analyze audio from microphone.

        Args:
            duration: Recording duration in seconds

        Returns:
            Dictionary with analysis results

        Raises:
            ValueError: If duration is invalid
            RuntimeError: If recording fails
        """
        start_time = time.time()

        # Display recording info
        self.console.print(f"\n[bold cyan]Recording from microphone:[/bold cyan] {duration}s")
        self.console.print("━" * 60)

        # Record audio
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=False
        ) as progress:
            task = progress.add_task(
                description=f"Recording for {duration} seconds...",
                total=None
            )
            audio_data, sample_rate = self.audio_processor.record_audio(duration)
            progress.update(task, description="Recording complete")

        # Validate audio
        if not self.audio_processor.validate_audio(audio_data):
            raise ValueError("Recorded audio is invalid or too short for analysis")

        # Detect BPM
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            progress.add_task(description="Detecting BPM...", total=None)
            bpm, bpm_confidence = self.bpm_detector.detect(audio_data)

        # Detect Key
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            progress.add_task(description="Detecting key...", total=None)
            key, mode, key_confidence = self.key_detector.detect(audio_data)

        end_time = time.time()
        analysis_time = end_time - start_time

        # Prepare results
        results = {
            'source': 'microphone',
            'bpm': bpm,
            'bpm_confidence': bpm_confidence,
            'bpm_confidence_level': self.bpm_detector.get_confidence_level(bpm_confidence),
            'key': key,
            'mode': mode,
            'key_string': self.key_detector.get_key_string(key, mode),
            'key_confidence': key_confidence,
            'key_confidence_level': self.key_detector.get_confidence_level(key_confidence),
            'analysis_time': analysis_time,
            'duration': duration
        }

        if self.verbose:
            results['scale_notes'] = self.key_detector.get_scale_notes(key, mode)
            results['relative_keys'] = self.key_detector.get_relative_keys(key, mode)

        return results

    def display_results(self, results: dict) -> None:
        """
        Display analysis results in a formatted way.

        Args:
            results: Dictionary with analysis results
        """
        self.console.print()

        # Create results table
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style="bold cyan", no_wrap=True)
        table.add_column(style="bold white")

        # Add main results
        table.add_row("BPM:", f"{results['bpm']:.1f}")
        table.add_row("Key:", results['key_string'])

        if self.verbose:
            table.add_row("BPM Confidence:", results['bpm_confidence_level'])
            table.add_row("Key Confidence:", results['key_confidence_level'])

        # Display table in a panel
        panel = Panel(
            table,
            title="[bold green]Analysis Results[/bold green]",
            border_style="green"
        )
        self.console.print(panel)

        # Display verbose information
        if self.verbose and 'scale_notes' in results:
            self.console.print(f"\n[bold]Scale notes:[/bold] {', '.join(results['scale_notes'])}")

            if 'relative_keys' in results:
                self.console.print(f"\n[bold]Related keys:[/bold]")
                for relation, key in results['relative_keys'].items():
                    self.console.print(f"  {relation.capitalize()}: {key}")

        # Display timing info
        self.console.print(
            f"\n[dim]Analysis completed in {results['analysis_time']:.2f}s[/dim]\n"
        )


def analyze_batch(analyzer, file_list, continue_on_error, console):
    """
    Analyze multiple audio files.

    Args:
        analyzer: AudioAnalyzer instance
        file_list: List of file paths
        continue_on_error: Whether to continue if a file fails
        console: Rich console for output

    Returns:
        List of analysis results
    """
    results_list = []
    failed_files = []

    console.print(f"\n[bold cyan]Batch Analysis:[/bold cyan] {len(file_list)} files")
    console.print("━" * 60)

    for i, file_path in enumerate(file_list, 1):
        try:
            console.print(f"\n[{i}/{len(file_list)}] Analyzing: {Path(file_path).name}")

            results = analyzer.analyze_file(file_path)
            results_list.append(results)

            # Show quick summary
            console.print(f"  BPM: {results['bpm']:.1f} | Key: {results['key_string']}")

        except Exception as e:
            failed_files.append((file_path, str(e)))
            console.print(f"  [red]✗ Failed: {e}[/red]")

            if not continue_on_error:
                console.print(f"\n[bold red]Batch processing stopped.[/bold red]")
                console.print(f"Use --continue-on-error to skip failed files.\n")
                raise

    # Summary
    console.print("\n" + "━" * 60)
    console.print(f"[bold green]✓ Completed:[/bold green] {len(results_list)}/{len(file_list)} files")

    if failed_files:
        console.print(f"\n[bold yellow]Failed files ({len(failed_files)}):[/bold yellow]")
        for file_path, error in failed_files:
            console.print(f"  • {Path(file_path).name}: {error}")

    return results_list


def display_batch_summary(results_list, console):
    """
    Display summary table for batch analysis results.

    Args:
        results_list: List of analysis result dictionaries
        console: Rich console for output
    """
    from rich.table import Table

    console.print()

    # Create results table
    table = Table(title="Batch Analysis Results", show_header=True)
    table.add_column("File", style="cyan", no_wrap=False)
    table.add_column("BPM", style="bold", justify="right")
    table.add_column("Key", style="bold")
    table.add_column("BPM Conf", justify="center")
    table.add_column("Key Conf", justify="center")

    for result in results_list:
        filename = Path(result.get('file', 'Unknown')).name
        bpm = f"{result['bpm']:.1f}"
        key_str = result['key_string']
        bpm_conf = result['bpm_confidence_level']
        key_conf = result['key_confidence_level']

        table.add_row(filename, bpm, key_str, bpm_conf, key_conf)

    console.print(table)
    console.print()


def save_results(results_list, output_file, console):
    """
    Save analysis results to file (CSV or JSON).

    Args:
        results_list: List of analysis result dictionaries
        output_file: Output file path
        console: Rich console for output
    """
    import csv
    import json

    output_path = Path(output_file)

    try:
        if output_path.suffix.lower() == '.csv':
            # Save as CSV
            with open(output_path, 'w', newline='') as csvfile:
                if not results_list:
                    console.print("[yellow]No results to save[/yellow]")
                    return

                # Determine CSV headers from first result
                fieldnames = ['file', 'bpm', 'bpm_confidence', 'bpm_confidence_level',
                             'key', 'mode', 'key_string', 'key_confidence',
                             'key_confidence_level', 'duration', 'analysis_time']

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()

                for result in results_list:
                    writer.writerow(result)

            console.print(f"\n[green]✓ Results saved to:[/green] {output_path}")
            console.print(f"  Format: CSV | Records: {len(results_list)}\n")

        else:
            # Save as JSON (default)
            with open(output_path, 'w') as jsonfile:
                json.dump(results_list, jsonfile, indent=2, cls=NumpyEncoder)

            console.print(f"\n[green]✓ Results saved to:[/green] {output_path}")
            console.print(f"  Format: JSON | Records: {len(results_list)}\n")

    except Exception as e:
        console.print(f"\n[bold red]Error saving results:[/bold red] {e}\n", style="red")
        raise


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Audio Analyzer - Detect BPM and musical key from audio files or microphone",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Single file:
    %(prog)s --file song.mp3
    %(prog)s --file track.wav --verbose

  Batch processing:
    %(prog)s --batch song1.mp3 song2.mp3 song3.mp3
    %(prog)s --batch *.mp3
    %(prog)s --dir /path/to/music/folder

  Export results:
    %(prog)s --batch *.mp3 --output results.csv
    %(prog)s --dir music/ --output analysis.json

  Microphone:
    %(prog)s --mic
    %(prog)s --mic --duration 30
        """
    )

    # Input source (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--file',
        type=str,
        metavar='PATH',
        help='Path to audio file to analyze'
    )
    input_group.add_argument(
        '--batch',
        type=str,
        nargs='+',
        metavar='FILES',
        help='Analyze multiple audio files (e.g., --batch *.mp3)'
    )
    input_group.add_argument(
        '--dir',
        type=str,
        metavar='DIRECTORY',
        help='Analyze all audio files in a directory'
    )
    input_group.add_argument(
        '--mic',
        action='store_true',
        help='Record from microphone'
    )

    # Optional arguments
    parser.add_argument(
        '--duration',
        type=float,
        default=10.0,
        metavar='SECONDS',
        help='Recording duration in seconds (default: 10)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed analysis information'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    parser.add_argument(
        '--output',
        type=str,
        metavar='FILE',
        help='Save results to file (CSV or JSON based on extension)'
    )
    parser.add_argument(
        '--continue-on-error',
        action='store_true',
        help='Continue batch processing even if some files fail'
    )

    args = parser.parse_args()

    # Create analyzer
    analyzer = AudioAnalyzer(verbose=args.verbose)
    console = Console()

    try:
        # Analyze based on input source
        if args.file:
            results = analyzer.analyze_file(args.file)
            results_list = [results]
        elif args.batch:
            results_list = analyze_batch(analyzer, args.batch, args.continue_on_error, console)
        elif args.dir:
            import glob
            import os
            # Find all audio files in directory
            audio_files = []
            for ext in ['.wav', '.mp3', '.flac', '.aiff', '.aif', '.ogg', '.m4a']:
                audio_files.extend(glob.glob(os.path.join(args.dir, f'*{ext}')))
                audio_files.extend(glob.glob(os.path.join(args.dir, f'*{ext.upper()}')))

            if not audio_files:
                console.print(f"\n[bold red]No audio files found in:[/bold red] {args.dir}\n", style="red")
                return 1

            results_list = analyze_batch(analyzer, audio_files, args.continue_on_error, console)
        else:  # microphone
            results = analyzer.analyze_microphone(args.duration)
            results_list = [results]

        # Handle output
        if args.output:
            save_results(results_list, args.output, console)
        elif args.json:
            if len(results_list) == 1:
                print(json.dumps(results_list[0], indent=2, cls=NumpyEncoder))
            else:
                print(json.dumps(results_list, indent=2, cls=NumpyEncoder))
        else:
            # Display results
            if len(results_list) == 1:
                analyzer.display_results(results_list[0])
            else:
                display_batch_summary(results_list, console)

        return 0

    except FileNotFoundError as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}\n", style="red")
        return 1

    except ValueError as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}\n", style="red")
        return 1

    except RuntimeError as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}\n", style="red")
        return 1

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Analysis cancelled by user[/yellow]\n")
        return 130

    except Exception as e:
        console.print(f"\n[bold red]Unexpected error:[/bold red] {e}\n", style="red")
        if args.verbose:
            import traceback
            console.print("[dim]" + traceback.format_exc() + "[/dim]")
        return 1


if __name__ == '__main__':
    sys.exit(main())
