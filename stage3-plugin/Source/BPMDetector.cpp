/*
  ==============================================================================

    BPM Detection Implementation
    Simplified tempo estimation for real-time analysis

  ==============================================================================
*/

#include "BPMDetector.h"

void BPMDetector::prepare(double sr)
{
    sampleRate = sr;
}

float BPMDetector::detectBPM(const float* audioData, int numSamples)
{
    if (numSamples < fftSize)
        return 0.0f;

    // Calculate onset strength envelope
    std::vector<float> onsetStrength;
    calculateOnsetStrength(audioData, numSamples, onsetStrength);

    if (onsetStrength.empty())
        return 0.0f;

    // Estimate tempo from onset strength
    float bpm = estimateTempoFromOnsets(onsetStrength);

    // Validate BPM range
    if (bpm < 40.0f || bpm > 240.0f)
    {
        confidence = 0.3f;
        return 120.0f; // Return default
    }

    // Calculate confidence based on onset strength variance
    float meanOnset = 0.0f;
    for (float val : onsetStrength)
        meanOnset += val;
    meanOnset /= onsetStrength.size();

    float variance = 0.0f;
    for (float val : onsetStrength)
        variance += (val - meanOnset) * (val - meanOnset);
    variance /= onsetStrength.size();

    // Higher variance = more rhythmic = higher confidence
    confidence = juce::jlimit(0.0f, 1.0f, variance * 10.0f);

    return bpm;
}

void BPMDetector::calculateOnsetStrength(const float* audioData, int numSamples,
                                         std::vector<float>& onsetStrength)
{
    onsetStrength.clear();

    juce::dsp::FFT fft(11); // 2048 point FFT
    std::vector<std::complex<float>> fftData(fftSize);
    std::vector<float> prevSpectrum(fftSize / 2, 0.0f);

    int numFrames = (numSamples - fftSize) / hopSize;

    for (int frame = 0; frame < numFrames; ++frame)
    {
        int startSample = frame * hopSize;

        // Apply Hann window
        auto windowedData = applyHannWindow(audioData + startSample, fftSize);

        // Copy to complex array
        for (int i = 0; i < fftSize; ++i)
            fftData[i] = std::complex<float>(windowedData[i], 0.0f);

        // Perform FFT
        fft.perform(windowedData.data(), reinterpret_cast<float*>(fftData.data()), false);

        // Calculate magnitude spectrum
        std::vector<float> spectrum(fftSize / 2);
        for (int i = 0; i < fftSize / 2; ++i)
        {
            float real = fftData[i].real();
            float imag = fftData[i].imag();
            spectrum[i] = std::sqrt(real * real + imag * imag);
        }

        // Calculate spectral flux (onset strength)
        float flux = 0.0f;
        for (int i = 0; i < fftSize / 2; ++i)
        {
            float diff = spectrum[i] - prevSpectrum[i];
            if (diff > 0.0f)
                flux += diff;
        }

        onsetStrength.push_back(flux);
        prevSpectrum = spectrum;
    }
}

float BPMDetector::estimateTempoFromOnsets(const std::vector<float>& onsetStrength)
{
    if (onsetStrength.size() < 10)
        return 0.0f;

    // Calculate autocorrelation of onset strength
    int maxLag = static_cast<int>(onsetStrength.size() / 2);
    float maxCorr = 0.0f;
    int bestLag = 0;

    // Search for tempo in range 40-240 BPM
    float framesPerSecond = static_cast<float>(sampleRate) / hopSize;
    int minLag = static_cast<int>(framesPerSecond * 60.0f / 240.0f); // 240 BPM
    int maxLagRange = static_cast<int>(framesPerSecond * 60.0f / 40.0f); // 40 BPM

    maxLagRange = juce::jmin(maxLagRange, maxLag);

    for (int lag = minLag; lag < maxLagRange; ++lag)
    {
        float corr = autocorrelate(onsetStrength, lag);

        if (corr > maxCorr)
        {
            maxCorr = corr;
            bestLag = lag;
        }
    }

    if (bestLag == 0)
        return 0.0f;

    // Convert lag to BPM
    float beatsPerFrame = 1.0f / bestLag;
    float beatsPerSecond = beatsPerFrame * framesPerSecond;
    float bpm = beatsPerSecond * 60.0f;

    return bpm;
}

float BPMDetector::autocorrelate(const std::vector<float>& signal, int lag)
{
    float sum = 0.0f;
    int count = 0;

    for (size_t i = 0; i < signal.size() - lag; ++i)
    {
        sum += signal[i] * signal[i + lag];
        count++;
    }

    return count > 0 ? sum / count : 0.0f;
}

std::vector<float> BPMDetector::applyHannWindow(const float* data, int size)
{
    std::vector<float> windowed(size);

    for (int i = 0; i < size; ++i)
    {
        float window = 0.5f * (1.0f - std::cos(2.0f * juce::MathConstants<float>::pi * i / (size - 1)));
        windowed[i] = data[i] * window;
    }

    return windowed;
}
