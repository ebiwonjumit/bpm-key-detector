/*
  ==============================================================================

    BPM Key Detector Plugin
    Audio Unit / VST3 Plugin for BPM and Key Detection

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "BPMDetector.h"
#include "KeyDetector.h"

//==============================================================================
/**
    Main audio plugin processor for BPM and Key detection.
*/
class BPMKeyDetectorAudioProcessor : public juce::AudioProcessor
{
public:
    //==============================================================================
    BPMKeyDetectorAudioProcessor();
    ~BPMKeyDetectorAudioProcessor() override;

    //==============================================================================
    void prepareToPlay (double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;

   #ifndef JucePlugin_PreferredChannelConfigurations
    bool isBusesLayoutSupported (const BusesLayout& layouts) const override;
   #endif

    void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    //==============================================================================
    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override;

    //==============================================================================
    const juce::String getName() const override;

    bool acceptsMidi() const override;
    bool producesMidi() const override;
    bool isMidiEffect() const override;
    double getTailLengthSeconds() const override;

    //==============================================================================
    int getNumPrograms() override;
    int getCurrentProgram() override;
    void setCurrentProgram (int index) override;
    const juce::String getProgramName (int index) override;
    void changeProgramName (int index, const juce::String& newName) override;

    //==============================================================================
    void getStateInformation (juce::MemoryBlock& destData) override;
    void setStateInformation (const void* data, int sizeInBytes) override;

    //==============================================================================
    // Analysis results
    float getCurrentBPM() const { return currentBPM.load(); }
    juce::String getCurrentKey() const { return currentKey; }
    juce::String getCurrentMode() const { return currentMode; }
    float getBPMConfidence() const { return bpmConfidence.load(); }
    float getKeyConfidence() const { return keyConfidence.load(); }

    bool isAnalyzing() const { return analyzing.load(); }
    void startAnalysis();
    void stopAnalysis();

private:
    //==============================================================================
    // Audio analysis
    BPMDetector bpmDetector;
    KeyDetector keyDetector;

    // Circular buffer for analysis
    juce::AudioBuffer<float> analysisBuffer;
    int analysisBufferWritePos = 0;
    int analysisBufferSize = 0;

    // Analysis state
    std::atomic<float> currentBPM { 0.0f };
    std::atomic<float> bpmConfidence { 0.0f };
    std::atomic<float> keyConfidence { 0.0f };
    juce::String currentKey = "C";
    juce::String currentMode = "major";
    std::atomic<bool> analyzing { false };

    // Threading
    juce::CriticalSection analysisLock;
    std::unique_ptr<juce::Thread> analysisThread;

    // Sample rate
    double currentSampleRate = 44100.0;

    // Analysis parameters
    static constexpr int analysisWindowSeconds = 10; // Analyze 10 seconds of audio
    static constexpr int analysisUpdateIntervalMs = 2000; // Update every 2 seconds

    void performAnalysis();
    void updateAnalysisResults(float bpm, float bpmConf,
                              const juce::String& key,
                              const juce::String& mode,
                              float keyConf);

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (BPMKeyDetectorAudioProcessor)
};
