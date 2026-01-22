# Project Goals & Roadmap

## Vision

Create a versatile audio analysis tool that detects BPM and musical key, evolving from a simple CLI tool to a professional DAW plugin.

## Core Objectives

1. **Accurate Analysis**: Provide reliable BPM and key detection
2. **User-Friendly**: Easy to use for both technical and non-technical users
3. **Multi-Platform**: Eventually support macOS, Windows, and Linux
4. **Professional Quality**: Meet the standards for professional music production

## Stage 1: CLI Tool ✓ (Current)

**Goals:**
- [x] Project structure setup
- [ ] Core BPM detection using librosa
- [ ] Musical key detection using chromagram analysis
- [ ] File input support (WAV, MP3, FLAC, AIFF)
- [ ] Microphone recording capability
- [ ] Unit tests with >80% coverage
- [ ] Clean CLI interface with progress indicators
- [ ] Error handling and validation

**Success Criteria:**
- Detects BPM within ±2 BPM for typical electronic music
- Key detection accuracy >70% on well-defined tonal music
- Handles various audio formats gracefully
- Clear error messages for invalid input

## Stage 2: GUI Application (Planned)

**Goals:**
- Modern, native macOS interface (SwiftUI preferred)
- Drag-and-drop file support
- Real-time waveform visualization
- Microphone level monitoring
- Visual feedback during analysis
- Export results to file
- Batch processing support

**Technology Options:**
- **Option A**: Native macOS app with Swift/SwiftUI
  - Pros: Best performance, native look/feel, App Store ready
  - Cons: macOS only
- **Option B**: Cross-platform with Python/PyQt6
  - Pros: Reuse Python code, works on Windows/Linux
  - Cons: Larger file size, less native feel
- **Option C**: Electron with web technologies
  - Pros: Modern UI, cross-platform
  - Cons: Heavy resource usage

**Success Criteria:**
- Intuitive interface requiring no documentation
- Sub-second response time for UI interactions
- Handles drag-and-drop seamlessly
- Visual polish matching professional tools

## Stage 3: DAW Plugin (Future)

**Goals:**
- VST3 plugin format
- Audio Unit (AU) format for macOS
- Real-time analysis of playing tracks
- Integration with DAW automation
- Low CPU usage
- Visual feedback within plugin window

**Technology:**
- JUCE framework (C++)
- Port core algorithms from Python to C++
- Or: Embed Python runtime (less ideal for performance)

**Success Criteria:**
- Meets VST3 standard requirements
- Passes AU validation on macOS
- CPU usage <5% during real-time analysis
- Compatible with major DAWs (Ableton, Logic Pro, FL Studio)

## Technical Milestones

### Phase 1: Core Algorithms ✓
- [x] BPM detection algorithm
- [x] Key detection algorithm
- [ ] Algorithm validation with test suite

### Phase 2: Input Handling
- [ ] Multi-format audio file support
- [ ] Robust error handling
- [ ] Microphone input with proper buffering

### Phase 3: Output & UX
- [ ] Formatted CLI output
- [ ] Optional JSON export
- [ ] Verbose mode for debugging

### Phase 4: Optimization
- [ ] Performance profiling
- [ ] Memory usage optimization
- [ ] Parallel processing for batch analysis

## Long-term Features (Ideas)

- **Chord detection**: Identify chord progressions
- **Time signature detection**: Detect 4/4, 3/4, 6/8, etc.
- **Genre classification**: ML-based genre detection
- **Cloud sync**: Save analysis history
- **API service**: REST API for web integration
- **Mobile app**: iOS/Android version

## Success Metrics

### Stage 1
- BPM accuracy: >95% within ±2 BPM
- Key accuracy: >70% on tonal music
- Test coverage: >80%
- Documentation complete

### Stage 2
- User satisfaction: >4.5/5 stars
- Installation success rate: >95%
- Crash rate: <0.1%

### Stage 3
- DAW compatibility: 5+ major DAWs
- Plugin certification passes
- User reviews: >4/5 stars in plugin marketplaces

## Timeline Estimate

- **Stage 1**: 1-2 weeks (development + testing)
- **Stage 2**: 3-4 weeks (GUI design + implementation)
- **Stage 3**: 6-8 weeks (JUCE learning + plugin development)

**Total estimated time**: 3-4 months for all stages