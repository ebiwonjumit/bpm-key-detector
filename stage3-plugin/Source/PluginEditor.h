/*
  ==============================================================================

    BPM Key Detector Plugin Editor (UI)

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "PluginProcessor.h"

//==============================================================================
/**
    Plugin editor with BPM and Key display
*/
class BPMKeyDetectorAudioProcessorEditor  : public juce::AudioProcessorEditor,
                                            private juce::Timer
{
public:
    BPMKeyDetectorAudioProcessorEditor (BPMKeyDetectorAudioProcessor&);
    ~BPMKeyDetectorAudioProcessorEditor() override;

    //==============================================================================
    void paint (juce::Graphics&) override;
    void resized() override;

private:
    //==============================================================================
    void timerCallback() override;

    // Reference to processor
    BPMKeyDetectorAudioProcessor& audioProcessor;

    // UI Components
    juce::Label titleLabel;
    juce::Label bpmLabel;
    juce::Label bpmValueLabel;
    juce::Label keyLabel;
    juce::Label keyValueLabel;
    juce::Label confidenceLabel;
    juce::TextButton analyzeButton;

    // Colors (black and white theme)
    juce::Colour backgroundColour = juce::Colours::white;
    juce::Colour textColour = juce::Colours::black;
    juce::Colour secondaryTextColour = juce::Colour(0xff808080);
    juce::Colour dividerColour = juce::Colour(0xfff0f0f0);

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (BPMKeyDetectorAudioProcessorEditor)
};
