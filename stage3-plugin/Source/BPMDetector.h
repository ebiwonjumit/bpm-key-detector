/*
  ==============================================================================

    BPM Detection Algorithm
    Simplified C++ implementation for real-time use

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include <vector>
#include <complex>

class BPMDetector
{
public:
    BPMDetector() = default;
    ~BPMDetector() = default;

    void prepare(double sampleRate);

    /**
     * Detect BPM from audio buffer
     * @param audioData Pointer to mono audio data
     * @param numSamples Number of samples
     * @return Detected BPM value
     */
    float detectBPM(const float* audioData, int numSamples);

    float getConfidence() const { return confidence; }

private:
    double sampleRate = 44100.0;
    float confidence = 0.5f;

    // Analysis parameters
    static constexpr int hopSize = 512;
    static constexpr int fftSize = 2048;

    // Helper methods
    void calculateOnsetStrength(const float* audioData, int numSamples,
                               std::vector<float>& onsetStrength);

    float estimateTempoFromOnsets(const std::vector<float>& onsetStrength);

    float autocorrelate(const std::vector<float>& signal, int lag);

    // Utility
    std::vector<float> applyHannWindow(const float* data, int size);
};
