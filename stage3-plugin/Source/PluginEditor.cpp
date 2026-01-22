/*
  ==============================================================================

    BPM Key Detector Plugin Editor Implementation

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"

//==============================================================================
BPMKeyDetectorAudioProcessorEditor::BPMKeyDetectorAudioProcessorEditor (BPMKeyDetectorAudioProcessor& p)
    : AudioProcessorEditor (&p), audioProcessor (p)
{
    // Set window size
    setSize (400, 300);

    // Title Label
    titleLabel.setText ("BPM & Key Detector", juce::dontSendNotification);
    titleLabel.setFont (juce::Font (24.0f, juce::Font::bold));
    titleLabel.setJustificationType (juce::Justification::centred);
    titleLabel.setColour (juce::Label::textColourId, textColour);
    addAndMakeVisible (titleLabel);

    // BPM Label
    bpmLabel.setText ("BPM", juce::dontSendNotification);
    bpmLabel.setFont (juce::Font (14.0f));
    bpmLabel.setJustificationType (juce::Justification::centred);
    bpmLabel.setColour (juce::Label::textColourId, secondaryTextColour);
    addAndMakeVisible (bpmLabel);

    // BPM Value Label
    bpmValueLabel.setText ("--", juce::dontSendNotification);
    bpmValueLabel.setFont (juce::Font (48.0f, juce::Font::bold));
    bpmValueLabel.setJustificationType (juce::Justification::centred);
    bpmValueLabel.setColour (juce::Label::textColourId, textColour);
    addAndMakeVisible (bpmValueLabel);

    // Key Label
    keyLabel.setText ("Key", juce::dontSendNotification);
    keyLabel.setFont (juce::Font (14.0f));
    keyLabel.setJustificationType (juce::Justification::centred);
    keyLabel.setColour (juce::Label::textColourId, secondaryTextColour);
    addAndMakeVisible (keyLabel);

    // Key Value Label
    keyValueLabel.setText ("--", juce::dontSendNotification);
    keyValueLabel.setFont (juce::Font (48.0f, juce::Font::bold));
    keyValueLabel.setJustificationType (juce::Justification::centred);
    keyValueLabel.setColour (juce::Label::textColourId, textColour);
    addAndMakeVisible (keyValueLabel);

    // Confidence Label
    confidenceLabel.setText ("", juce::dontSendNotification);
    confidenceLabel.setFont (juce::Font (11.0f));
    confidenceLabel.setJustificationType (juce::Justification::centred);
    confidenceLabel.setColour (juce::Label::textColourId, secondaryTextColour);
    addAndMakeVisible (confidenceLabel);

    // Analyze Button
    analyzeButton.setButtonText ("Start Analysis");
    analyzeButton.setColour (juce::TextButton::buttonColourId, textColour);
    analyzeButton.setColour (juce::TextButton::textColourOffId, backgroundColour);
    analyzeButton.onClick = [this]
    {
        if (audioProcessor.isAnalyzing())
        {
            audioProcessor.stopAnalysis();
            analyzeButton.setButtonText ("Start Analysis");
        }
        else
        {
            audioProcessor.startAnalysis();
            analyzeButton.setButtonText ("Stop Analysis");
        }
    };
    addAndMakeVisible (analyzeButton);

    // Start timer to update display (30 FPS)
    startTimerHz (30);
}

BPMKeyDetectorAudioProcessorEditor::~BPMKeyDetectorAudioProcessorEditor()
{
    stopTimer();
}

//==============================================================================
void BPMKeyDetectorAudioProcessorEditor::paint (juce::Graphics& g)
{
    // Fill background
    g.fillAll (backgroundColour);

    // Draw divider line
    g.setColour (dividerColour);
    g.drawLine (40.0f, 130.0f, getWidth() - 40.0f, 130.0f, 1.0f);

    // Draw vertical divider between BPM and Key
    float centerX = getWidth() / 2.0f;
    g.drawLine (centerX, 150.0f, centerX, 240.0f, 1.0f);
}

void BPMKeyDetectorAudioProcessorEditor::resized()
{
    auto area = getLocalBounds();

    // Title at top
    titleLabel.setBounds (area.removeFromTop (60).reduced (20, 15));

    // Button at bottom
    analyzeButton.setBounds (area.removeFromBottom (50).reduced (100, 10));

    // Confidence label above button
    confidenceLabel.setBounds (area.removeFromBottom (20).reduced (20, 0));

    area.removeFromTop (20); // Spacing

    // Split remaining area in half for BPM and Key
    auto leftArea = area.removeFromLeft (area.getWidth() / 2);
    auto rightArea = area;

    // BPM (left side)
    bpmLabel.setBounds (leftArea.removeFromTop (25).reduced (10, 0));
    bpmValueLabel.setBounds (leftArea.reduced (10, 10));

    // Key (right side)
    keyLabel.setBounds (rightArea.removeFromTop (25).reduced (10, 0));
    keyValueLabel.setBounds (rightArea.reduced (10, 10));
}

void BPMKeyDetectorAudioProcessorEditor::timerCallback()
{
    // Update display with current analysis results
    float bpm = audioProcessor.getCurrentBPM();
    juce::String key = audioProcessor.getCurrentKey();
    juce::String mode = audioProcessor.getCurrentMode();

    // Update BPM display
    if (bpm > 0.0f)
        bpmValueLabel.setText (juce::String (bpm, 1), juce::dontSendNotification);
    else
        bpmValueLabel.setText ("--", juce::dontSendNotification);

    // Update Key display
    if (key.isNotEmpty())
    {
        juce::String keyString = key + " " + mode;
        keyValueLabel.setText (keyString, juce::dontSendNotification);
    }
    else
    {
        keyValueLabel.setText ("--", juce::dontSendNotification);
    }

    // Update confidence display
    if (bpm > 0.0f)
    {
        float bpmConf = audioProcessor.getBPMConfidence();
        float keyConf = audioProcessor.getKeyConfidence();

        juce::String confString = "Confidence: BPM ";
        confString += bpmConf >= 0.7f ? "High" : (bpmConf >= 0.4f ? "Medium" : "Low");
        confString += " | Key ";
        confString += keyConf >= 0.7f ? "High" : (keyConf >= 0.5f ? "Medium" : "Low");

        confidenceLabel.setText (confString, juce::dontSendNotification);
    }
    else
    {
        confidenceLabel.setText ("Play audio to analyze", juce::dontSendNotification);
    }

    // Update button state
    if (audioProcessor.isAnalyzing() && analyzeButton.getButtonText() == "Start Analysis")
        analyzeButton.setButtonText ("Stop Analysis");
    else if (!audioProcessor.isAnalyzing() && analyzeButton.getButtonText() == "Stop Analysis")
        analyzeButton.setButtonText ("Start Analysis");
}
