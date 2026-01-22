/*
  ==============================================================================

    Musical Key Detection Implementation
    Chromagram-based key detection using Krumhansl-Schmuckler algorithm

  ==============================================================================
*/

#include "KeyDetector.h"

void KeyDetector::prepare(double sr)
{
    sampleRate = sr;
}

std::tuple<juce::String, juce::String, float> KeyDetector::detectKey(
    const float* audioData, int numSamples)
{
    if (numSamples < fftSize)
        return {"C", "major", 0.0f};

    // Calculate chromagram (pitch class distribution)
    std::array<float, 12> chromagram = {0};
    calculateChromagram(audioData, numSamples, chromagram);

    // Normalize chromagram
    float sum = 0.0f;
    for (float val : chromagram)
        sum += val;

    if (sum > 0.0f)
    {
        for (float& val : chromagram)
            val /= sum;
    }

    // Find best matching key
    return findBestKey(chromagram);
}

void KeyDetector::calculateChromagram(const float* audioData, int numSamples,
                                     std::array<float, 12>& chromagram)
{
    chromagram.fill(0.0f);

    juce::dsp::FFT fft(12); // 4096 point FFT
    std::vector<std::complex<float>> fftData(fftSize);

    int numFrames = (numSamples - fftSize) / hopSize;

    for (int frame = 0; frame < numFrames; ++frame)
    {
        int startSample = frame * hopSize;

        // Apply Hann window
        std::vector<float> windowed(fftSize);
        for (int i = 0; i < fftSize; ++i)
        {
            float window = 0.5f * (1.0f - std::cos(2.0f * juce::MathConstants<float>::pi * i / (fftSize - 1)));
            windowed[i] = audioData[startSample + i] * window;
        }

        // Perform FFT
        fft.perform(windowed.data(), reinterpret_cast<float*>(fftData.data()), false);

        // Map FFT bins to pitch classes
        for (int bin = 1; bin < fftSize / 2; ++bin)
        {
            float frequency = bin * static_cast<float>(sampleRate) / fftSize;

            // Skip frequencies outside musical range (roughly 27.5 Hz to 4186 Hz)
            if (frequency < 27.5f || frequency > 4186.0f)
                continue;

            // Get magnitude
            float real = fftData[bin].real();
            float imag = fftData[bin].imag();
            float magnitude = std::sqrt(real * real + imag * imag);

            // Map to pitch class (0-11)
            float pitchClass = frequencyToPitchClass(frequency);
            int pitchClassIndex = static_cast<int>(pitchClass) % 12;

            chromagram[pitchClassIndex] += magnitude;
        }
    }
}

std::tuple<juce::String, juce::String, float> KeyDetector::findBestKey(
    const std::array<float, 12>& pitchClassDistribution)
{
    float maxCorrelation = -1.0f;
    juce::String bestKey = "C";
    juce::String bestMode = "major";

    // Try all 12 keys in both major and minor
    for (int root = 0; root < 12; ++root)
    {
        // Rotate profiles to match this root
        std::array<float, 12> rotatedMajor;
        std::array<float, 12> rotatedMinor;

        for (int i = 0; i < 12; ++i)
        {
            rotatedMajor[i] = majorProfile[(i + root) % 12];
            rotatedMinor[i] = minorProfile[(i + root) % 12];
        }

        // Calculate correlations
        float majorCorr = correlation(pitchClassDistribution, rotatedMajor);
        float minorCorr = correlation(pitchClassDistribution, rotatedMinor);

        // Check if major key is best so far
        if (majorCorr > maxCorrelation)
        {
            maxCorrelation = majorCorr;
            bestKey = pitchClasses[root];
            bestMode = "major";
        }

        // Check if minor key is best so far
        if (minorCorr > maxCorrelation)
        {
            maxCorrelation = minorCorr;
            bestKey = pitchClasses[root];
            bestMode = "minor";
        }
    }

    // Normalize correlation to 0-1 confidence
    float confidence = (maxCorrelation + 1.0f) / 2.0f;
    confidence = juce::jlimit(0.0f, 1.0f, confidence);

    return {bestKey, bestMode, confidence};
}

float KeyDetector::correlation(const std::array<float, 12>& x, const std::array<float, 12>& y)
{
    // Calculate means
    float meanX = 0.0f, meanY = 0.0f;
    for (int i = 0; i < 12; ++i)
    {
        meanX += x[i];
        meanY += y[i];
    }
    meanX /= 12.0f;
    meanY /= 12.0f;

    // Calculate standard deviations and covariance
    float stdX = 0.0f, stdY = 0.0f, covariance = 0.0f;
    for (int i = 0; i < 12; ++i)
    {
        float dx = x[i] - meanX;
        float dy = y[i] - meanY;

        stdX += dx * dx;
        stdY += dy * dy;
        covariance += dx * dy;
    }

    stdX = std::sqrt(stdX);
    stdY = std::sqrt(stdY);

    // Avoid division by zero
    if (stdX < 1e-10f || stdY < 1e-10f)
        return 0.0f;

    // Return Pearson correlation coefficient
    return covariance / (stdX * stdY);
}

float KeyDetector::frequencyToPitchClass(float frequency)
{
    // Convert frequency to MIDI note number
    // A4 = 440 Hz = MIDI note 69
    float midiNote = 69.0f + 12.0f * std::log2(frequency / 440.0f);

    // Convert to pitch class (0-11)
    return std::fmod(midiNote, 12.0f);
}
