/*
  ==============================================================================

    BPM Key Detector Plugin Implementation

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"

//==============================================================================
BPMKeyDetectorAudioProcessor::BPMKeyDetectorAudioProcessor()
#ifndef JucePlugin_PreferredChannelConfigurations
     : AudioProcessor (BusesProperties()
                     #if ! JucePlugin_IsMidiEffect
                      #if ! JucePlugin_IsSynth
                       .withInput  ("Input",  juce::AudioChannelSet::stereo(), true)
                      #endif
                       .withOutput ("Output", juce::AudioChannelSet::stereo(), true)
                     #endif
                       )
#endif
{
}

BPMKeyDetectorAudioProcessor::~BPMKeyDetectorAudioProcessor()
{
    stopAnalysis();
}

//==============================================================================
const juce::String BPMKeyDetectorAudioProcessor::getName() const
{
    return JucePlugin_Name;
}

bool BPMKeyDetectorAudioProcessor::acceptsMidi() const
{
   #if JucePlugin_WantsMidiInput
    return true;
   #else
    return false;
   #endif
}

bool BPMKeyDetectorAudioProcessor::producesMidi() const
{
   #if JucePlugin_ProducesMidiOutput
    return true;
   #else
    return false;
   #endif
}

bool BPMKeyDetectorAudioProcessor::isMidiEffect() const
{
   #if JucePlugin_IsMidiEffect
    return true;
   #else
    return false;
   #endif
}

double BPMKeyDetectorAudioProcessor::getTailLengthSeconds() const
{
    return 0.0;
}

int BPMKeyDetectorAudioProcessor::getNumPrograms()
{
    return 1;
}

int BPMKeyDetectorAudioProcessor::getCurrentProgram()
{
    return 0;
}

void BPMKeyDetectorAudioProcessor::setCurrentProgram (int index)
{
}

const juce::String BPMKeyDetectorAudioProcessor::getProgramName (int index)
{
    return {};
}

void BPMKeyDetectorAudioProcessor::changeProgramName (int index, const juce::String& newName)
{
}

//==============================================================================
void BPMKeyDetectorAudioProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)
{
    currentSampleRate = sampleRate;

    // Allocate analysis buffer (10 seconds of audio)
    analysisBufferSize = static_cast<int>(sampleRate * analysisWindowSeconds);
    analysisBuffer.setSize(2, analysisBufferSize);
    analysisBuffer.clear();
    analysisBufferWritePos = 0;

    // Prepare detectors
    bpmDetector.prepare(sampleRate);
    keyDetector.prepare(sampleRate);
}

void BPMKeyDetectorAudioProcessor::releaseResources()
{
    stopAnalysis();
}

#ifndef JucePlugin_PreferredChannelConfigurations
bool BPMKeyDetectorAudioProcessor::isBusesLayoutSupported (const BusesLayout& layouts) const
{
  #if JucePlugin_IsMidiEffect
    juce::ignoreUnused (layouts);
    return true;
  #else
    // Support mono or stereo
    if (layouts.getMainOutputChannelSet() != juce::AudioChannelSet::mono()
     && layouts.getMainOutputChannelSet() != juce::AudioChannelSet::stereo())
        return false;

   #if ! JucePlugin_IsSynth
    if (layouts.getMainOutputChannelSet() != layouts.getMainInputChannelSet())
        return false;
   #endif

    return true;
  #endif
}
#endif

void BPMKeyDetectorAudioProcessor::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{
    juce::ScopedNoDenormals noDenormals;

    // Pass audio through unchanged
    auto totalNumInputChannels  = getTotalNumInputChannels();
    auto totalNumOutputChannels = getTotalNumOutputChannels();

    // Clear unused output channels
    for (auto i = totalNumInputChannels; i < totalNumOutputChannels; ++i)
        buffer.clear (i, 0, buffer.getNumSamples());

    // Copy incoming audio to analysis buffer for background processing
    if (analyzing.load())
    {
        const juce::ScopedLock sl(analysisLock);

        int numSamples = buffer.getNumSamples();
        int numChannels = juce::jmin(buffer.getNumChannels(), analysisBuffer.getNumChannels());

        for (int channel = 0; channel < numChannels; ++channel)
        {
            auto* src = buffer.getReadPointer(channel);
            auto* dst = analysisBuffer.getWritePointer(channel);

            for (int i = 0; i < numSamples; ++i)
            {
                dst[analysisBufferWritePos] = src[i];
                analysisBufferWritePos = (analysisBufferWritePos + 1) % analysisBufferSize;
            }
        }
    }
}

//==============================================================================
bool BPMKeyDetectorAudioProcessor::hasEditor() const
{
    return true;
}

juce::AudioProcessorEditor* BPMKeyDetectorAudioProcessor::createEditor()
{
    return new BPMKeyDetectorAudioProcessorEditor (*this);
}

//==============================================================================
void BPMKeyDetectorAudioProcessor::getStateInformation (juce::MemoryBlock& destData)
{
    // Save plugin state
    juce::MemoryOutputStream stream(destData, true);

    stream.writeFloat(currentBPM.load());
    stream.writeString(currentKey);
    stream.writeString(currentMode);
    stream.writeFloat(bpmConfidence.load());
    stream.writeFloat(keyConfidence.load());
}

void BPMKeyDetectorAudioProcessor::setStateInformation (const void* data, int sizeInBytes)
{
    // Restore plugin state
    juce::MemoryInputStream stream(data, static_cast<size_t>(sizeInBytes), false);

    currentBPM.store(stream.readFloat());
    currentKey = stream.readString();
    currentMode = stream.readString();
    bpmConfidence.store(stream.readFloat());
    keyConfidence.store(stream.readFloat());
}

//==============================================================================
void BPMKeyDetectorAudioProcessor::startAnalysis()
{
    if (!analyzing.load())
    {
        analyzing.store(true);
        analysisBufferWritePos = 0;
        analysisBuffer.clear();
    }
}

void BPMKeyDetectorAudioProcessor::stopAnalysis()
{
    analyzing.store(false);
}

void BPMKeyDetectorAudioProcessor::performAnalysis()
{
    // This would be called periodically to analyze the collected audio
    const juce::ScopedLock sl(analysisLock);

    if (analysisBuffer.getNumSamples() == 0)
        return;

    // Convert to mono for analysis
    juce::AudioBuffer<float> monoBuffer(1, analysisBufferSize);
    monoBuffer.clear();

    if (analysisBuffer.getNumChannels() > 1)
    {
        // Average stereo to mono
        for (int i = 0; i < analysisBufferSize; ++i)
        {
            float sum = 0.0f;
            for (int ch = 0; ch < analysisBuffer.getNumChannels(); ++ch)
                sum += analysisBuffer.getSample(ch, i);
            monoBuffer.setSample(0, i, sum / analysisBuffer.getNumChannels());
        }
    }
    else
    {
        monoBuffer.copyFrom(0, 0, analysisBuffer, 0, 0, analysisBufferSize);
    }

    // Perform BPM detection
    float bpm = bpmDetector.detectBPM(monoBuffer.getReadPointer(0), analysisBufferSize);
    float bpmConf = bpmDetector.getConfidence();

    // Perform key detection
    auto [key, mode, keyConf] = keyDetector.detectKey(monoBuffer.getReadPointer(0), analysisBufferSize);

    // Update results
    updateAnalysisResults(bpm, bpmConf, key, mode, keyConf);
}

void BPMKeyDetectorAudioProcessor::updateAnalysisResults(float bpm, float bpmConf,
                                                         const juce::String& key,
                                                         const juce::String& mode,
                                                         float keyConf)
{
    currentBPM.store(bpm);
    bpmConfidence.store(bpmConf);
    currentKey = key;
    currentMode = mode;
    keyConfidence.store(keyConf);
}

//==============================================================================
// This creates new instances of the plugin
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new BPMKeyDetectorAudioProcessor();
}
