/*
  ==============================================================================

    Musical Key Detection Algorithm
    Krumhansl-Schmuckler key-finding algorithm in C++

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include <vector>
#include <tuple>
#include <array>

class KeyDetector
{
public:
    KeyDetector() = default;
    ~KeyDetector() = default;

    void prepare(double sampleRate);

    /**
     * Detect musical key from audio buffer
     * @param audioData Pointer to mono audio data
     * @param numSamples Number of samples
     * @return Tuple of (key, mode, confidence)
     */
    std::tuple<juce::String, juce::String, float> detectKey(const float* audioData, int numSamples);

private:
    double sampleRate = 44100.0;

    // Krumhansl-Schmuckler key profiles
    static constexpr std::array<float, 12> majorProfile = {
        6.35f, 2.23f, 3.48f, 2.33f, 4.38f, 4.09f,
        2.52f, 5.19f, 2.39f, 3.66f, 2.29f, 2.88f
    };

    static constexpr std::array<float, 12> minorProfile = {
        6.33f, 2.68f, 3.52f, 5.38f, 2.60f, 3.53f,
        2.54f, 4.75f, 3.98f, 2.69f, 3.34f, 3.17f
    };

    static constexpr const char* pitchClasses[12] = {
        "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
    };

    // Analysis parameters
    static constexpr int hopSize = 512;
    static constexpr int fftSize = 4096;
    static constexpr int numBins = 12; // Chromagram bins

    // Helper methods
    void calculateChromagram(const float* audioData, int numSamples,
                            std::array<float, 12>& chromagram);

    std::tuple<juce::String, juce::String, float> findBestKey(
        const std::array<float, 12>& pitchClassDistribution);

    float correlation(const std::array<float, 12>& x, const std::array<float, 12>& y);

    float frequencyToPitchClass(float frequency);
};
