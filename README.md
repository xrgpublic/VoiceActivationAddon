# VoiceActivationAddon# Voice-Activated LLM Addon

> **Note:**  
> This repository has been updated with pygame for audio playback, replacing the previous playsound implementation for better compatibility and performance.

This Python module provides a voice-activated, voice-to-voice interface for interacting with Large Language Models (LLMs) via Ollama and Google Text-to-Speech (gTTS). Designed as an addon, it can be easily integrated into other Python projects. The module allows users to:
- Choose a specific LLM model at runtime (default is **llama3.2:1b**).
- Customize the system prompt to alter the AI assistant's behavior.
- Provide initial messages to Ollama for more complex interactions.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [As a Standalone Script](#as-a-standalone-script)
  - [As a Module in Your Project](#as-a-module-in-your-project)
- [Customization](#customization)
- [Code Overview](#code-overview)
  - [VoiceLLMAddon Class](#voicellmaddon-class)
  - [Key Methods](#key-methods)
- [Known Issues](#known-issues)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **Enhanced Modular Design**: Easily integrated as an addon into existing Python projects with optional dependencies loaded only when needed.
- **Custom LLM Selection**: Users can specify which LLM model to use at runtime.
- **Custom System Prompt**: Ability to change the AI assistant's behavior via a custom system prompt.
- **Initial Messages Support**: Accepts an initial list of messages to send to Ollama for context.
- **Custom Activation Phrases**: Define your own activation phrases to initiate interaction (default: "Hello Llama" or "Hey Llama").
- **Voice Query and Response**: Converts spoken queries to text, sends them to the LLM, and reads the AI's response aloud.
- **Multiple TTS Options**: Choose between Google Text-to-Speech (gTTS) or Piper for text-to-speech conversion.
- **Pygame Audio Playback**: Reliable audio playback using the pygame library.
- **Ollama Integration**: Connects with Ollama to generate AI responses from the specified LLM model.

## Requirements

- **Python** 3.12 
- **gTTS**: For text-to-speech conversion
- **pygame**: For audio playback
- **SpeechRecognition**: For handling voice input (only needed if using voice recognition)
- **pyaudio**: For audio playback
- **Ollama API**: Installed and configured on your machine (only needed if using Ollama for LLM queries)
- **Piper**: Optional for higher quality text-to-speech
- **argparse**: For command-line argument parsing
- **json**: For handling messages in JSON format

## Installation

Install the required libraries using pip:

```bash
pip install gtts pygame SpeechRecognition pyaudio
```

For optional components:

```bash
# For Ollama LLM integration
pip install ollama piperTTS
```

> **Note**: Installing `pyaudio` may require additional setup, especially on non-Windows systems.

## Usage

### As a Standalone Script

Run the script and specify optional arguments:

```bash
python voice_llm_addon.py --model <model_name> --system_prompt "<your_system_prompt>" --messages_file <path_to_messages_json> --activation_phrases "hello llama" "hey there llama"
```

- **`--model`**: (Optional) Specify the LLM model to use. Defaults to **llama3.2:1b**.
- **`--system_prompt`**: (Optional) Provide a custom system prompt to change the assistant's behavior.
- **`--messages_file`**: (Optional) Path to a JSON file containing initial messages to send to Ollama.
- **`--activation_phrases`**: (Optional) Space-separated list of phrases that will activate the assistant. Defaults to "hello llama" "hey llama".

### As a Module in Your Project

1. **Include the Module**: Add `voice_llm_addon.py` to your project directory.

2. **Import the Class**:

   ```python
   from voice_llm_addon import VoiceLLMAddon
   ```

3. **Initialize and Run**:

   ```python
   addon = VoiceLLMAddon(
       model='your_model_name',             # Optional
       system_prompt='Your system prompt',  # Optional
       initial_messages=[                   # Optional
           {'role': 'system', 'content': 'System message'},
           {'role': 'user', 'content': 'User message'},
       ],
       activation_phrases=["hello llama", "hey assistant"]  # Optional
   )
   addon.run()
   ```

## Customization

- **Change Activation Phrases**: Provide custom activation phrases using the `activation_phrases` parameter when initializing `VoiceLLMAddon` or via the `--activation_phrases` command-line argument.
- **Choose TTS Engine**: Use the optional `piper` parameter in the `speak` method to toggle between gTTS (default) and Piper for text-to-speech.
- **Select Voice Model**: When using Piper, specify a different voice model file with the `piper_model` parameter in the `speak` method.
- **Adjust AI Personality**: Provide a custom `system_prompt` when initializing `VoiceLLMAddon` or via the `--system_prompt` command-line argument.
- **Provide Initial Messages**: Supply an initial list of messages via the `initial_messages` parameter or by specifying a JSON file with `--messages_file`.

## Code Overview

### VoiceLLMAddon Class

The `VoiceLLMAddon` class encapsulates all functionality required for voice interaction with the LLM.

#### Initialization

```python
def __init__(self, model='llama3.2:1b', system_prompt=None, initial_messages=None, activation_phrases=["hello llama", "hey llama"]):
    self.model = model
    self.system_prompt = system_prompt
    self.initial_messages = initial_messages or []
    self.recognizer = None  # Speech recognizer will be initialized in run()
    self.activation_phrases = activation_phrases or ["hello llama", "hey llama"]
    self.activated = False  # Indicates if the activation phrase was detected
```

- **model**: Specifies the LLM model to use.
- **system_prompt**: Custom system prompt to alter the assistant's behavior.
- **initial_messages**: List of initial messages to send to Ollama.
- **recognizer**: The speech recognizer that will be initialized in the `run()` method.
- **activation_phrases**: List of phrases that will trigger the assistant to start listening for a query.
- **activated**: A flag to track whether the activation phrase has been detected.

### Key Methods

#### `speak(self, text, piper=False, piper_model="en_US-lessac-medium.onnx")`

Converts text to speech using either gTTS (default) or Piper (if piper=True), and plays it using pygame.

- **Parameters**:
  - `text` (str): The text to convert to speech.
  - `piper` (bool, optional): If True, uses Piper for text-to-speech conversion instead of gTTS. Defaults to False.
  - `piper_model` (str, optional): The Piper voice model file to use. Defaults to "en_US-lessac-medium.onnx".

#### `query_ollama(self, prompt)`

Sends a text prompt to the Ollama LLM and returns the response.

- **Parameters**:
  - `prompt` (str): The user's query to send to the LLM.
- **Returns**:
  - `response` (str): The LLM's response.

#### `run(self)`

Starts the voice interaction loop. Listens for the activation phrase and processes user queries.

## Known Issues

- **Ollama Model Compatibility**: Ensure the specified LLM model is installed and compatible with Ollama.
- **Microphone Access**: The script requires access to your system's microphone. Ensure that permissions are granted.
- **Piper Models**: If using Piper, you need to download the appropriate voice model files and ensure they're in the correct path.
- **Optional Dependencies**: If you encounter import errors, ensure that you have installed the necessary dependencies for the features you're using (e.g., ollama, piper, speech_recognition).

## License

This project is licensed under the MIT License.

## Acknowledgments

This project utilizes:

- **[gTTS](https://gtts.readthedocs.io/en/latest/)** for text-to-speech conversion.
- **[Piper](https://github.com/rhasspy/piper)** for high-quality text-to-speech conversion (optional).
- **[Pygame](https://www.pygame.org/)** for audio playback.
- **[Ollama](https://ollama.ai/)** for LLM interactions.
- **[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)** for voice input handling.

# Full Code Listing

```python
import os
import time
import argparse
import json
from gtts import gTTS
import wave
import pygame

#These 2 imports are imported inside the "run()" function to ensure you dont need to install them if you dont use those features
# import ollama 
# import speech_recognition as sr 

# Piper is imported inside the "speak" function to ensure you dont need to install it if you dont use that feature
# import piper 

class VoiceLLMAddon:
    def __init__(self, model='llama3.2:1b', system_prompt=None, initial_messages=None, activation_phrases=["hello llama", "hey llama"]):
        self.model = model
        self.system_prompt = system_prompt or (
            'You are a funny and self-deprecating AI assistant. '
            'Each of your replies will be a maximum of 2 sentences long. '
            'Short responses are crucial to your success as an AI assistant. '
            'Long replies take a long time to process and ruin the user experience. '
            'Just use any useful data and respond in short responses as an intelligent AI assistant.'
        )
        self.initial_messages = initial_messages or []
        self.recognizer = None # Speech recognizer will be initialized in run()
        self.activation_phrases = activation_phrases or ["hello llama", "hey llama"]
        self.activated = False  # Flag to indicate if activation phrase was detected

    def speak(self, text, piper=False, piper_model="en_US-lessac-medium.onnx"):
        """Convert text to speech, play it, and remove the temporary file."""
        try:
            filename = "audio.wav"
            # Delete old audio file if it exists
            audio_file = os.path.join(os.path.dirname(__file__), filename)
            if os.path.exists(audio_file):
                os.remove(audio_file)
                time.sleep(0.5)
            
            # Creating audio file
            if piper:
                from piper import PiperVoice
                voice = PiperVoice.load(piper_model)
                with wave.open(filename, "wb") as wav_file:
                    voice.synthesize_wav(text, wav_file)
            else:
                tts = gTTS(text=text, lang='en')
                response_file = os.path.join(os.path.dirname(__file__), filename)
                tts.save(response_file)
            
            # Prepping Pygame to play audio
            time.sleep(0.5) # Wait a moment to ensure file is written
            print("Speaking...")
            pygame.init()
            pygame.mixer.quit()  # Clean up any existing mixer
            pygame.mixer.init(frequency=44100)  # Initialize with standard frequency (44.1kHz)
            if not pygame.mixer.get_init():
                raise Exception("Failed to initialize pygame.mixer")
            
            # Load and play the sound
            sound = pygame.mixer.Sound(filename)
            print("Audio device initialized and sound loaded")
            sound.play()
            
            # Wait for the sound to finish playing
            while pygame.mixer.get_busy():
                pygame.time.Clock().tick(10)
            print("Done Speaking")

        except Exception as e:
            print("Exception while speaking:", str(e))

    def query_ollama(self, prompt):
        import ollama
        """Query the Ollama AI assistant with the given prompt and return the response."""
        try:

            # Construct messages for the chat
            messages = []
            if self.initial_messages == []:
                messages.append({'role': 'system', 'content': self.system_prompt})
            else:
                messages = self.initial_messages.copy()
            messages.append({'role': 'user', 'content': prompt})

            # query ollama
            ollama_response = ollama.chat(
                model=self.model,
                messages=messages,
                stream=False
            )

            # Extract and return the response content
            response = str(ollama_response['message']['content'])
            return response
        
        except Exception as e:
            print("Exception while querying Ollama:", str(e))
            return "I'm sorry, I couldn't process your request."


    def run(self):
        """Main loop to listen for activation phrases and respond to user queries."""

        # initialize and calibratespeech recognition
        import speech_recognition as sr
        self.recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Calibrating microphone for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source)
            

            while True:
                try:

                    # Check for activation phrase
                    if not self.activated:
                        print("Listening for activation phrase...")
                        audio = self.recognizer.listen(source)
                        print("Processing activation phrase...")
                        text = self.recognizer.recognize_google(audio).lower()
                        print(f"Detected text: {text}")
                        if text not in self.activation_phrases:
                            print("Activation phrase not detected.")
                            continue
                        print("Activation phrase detected.")
                        self.activated = True
                        self.speak("Hello!")

                    # Once activation phrase is heard, Listen for user query
                    print("Listening for your request...")
                    audio = self.recognizer.listen(source)
                    print("Processing your request...")
                    text = self.recognizer.recognize_google(audio)
                    print(f"You said: {text}")
                    response = self.query_ollama(text)
                    self.speak(response)
                    self.activated = False

                except sr.UnknownValueError:
                    print("Could not understand the audio.")
                except sr.RequestError as e:
                    print(f"Speech Recognition service error: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description='Voice-Activated LLM Addon')
    parser.add_argument('--model', type=str, default='llama3.2:1b',
                        help='Specify the LLM model to use (default: llama3.2:1b)')
    parser.add_argument('--system_prompt', type=str, default=None,
                        help='Custom system prompt for the AI assistant')
    parser.add_argument('--messages_file', type=str, default=None,
                        help='Path to a JSON file containing initial messages')
    parser.add_argument('--activation_phrases', type=str, nargs='+', default=["hello llama", "hey llama"],
                        help='List of phrases to activate the assistant (space-separated)')
    args = parser.parse_args()

    # Parsing initial messages from file if provided
    initial_messages = []
    if args.messages_file:
        try:
            with open(args.messages_file, 'r') as f:
                initial_messages = json.load(f)
            print(f"Loaded initial messages from {args.messages_file}")
        except Exception as e:
            print(f"Failed to load messages from {args.messages_file}: {e}")
    print('activation phrases:', args.activation_phrases)
    addon = VoiceLLMAddon(
        model=args.model,
        system_prompt=args.system_prompt,
        initial_messages=initial_messages,
        activation_phrases=args.activation_phrases
    )
    addon.run()

if __name__ == "__main__":
    main()
```


## Providing a Custom System Prompt

You can change the AI assistant's behavior by providing a custom system prompt.

### Via Command Line

```bash
python voice_llm_addon.py --system_prompt "You are a helpful assistant that provides detailed answers."
```

### In Code

```python
addon = VoiceLLMAddon(system_prompt="You are a helpful assistant that provides detailed answers.")
```

## Providing Initial Messages

You can supply initial messages to give context to the AI assistant.

### Via Command Line

1. Create a JSON file (e.g., `messages.json`) with your messages:

   ```json
   [
       {"role": "system", "content": "You are an AI assistant specialized in astronomy."},
       {"role": "user", "content": "Tell me about black holes."},
       {"role": "assistant", "content": "Black holes are regions in space where gravity is so strong that nothing can escape."}
   ]
   ```

2. Run the script with the `--messages_file` argument:

   ```bash
   python voice_llm_addon.py --messages_file messages.json
   ```

### In Code

```python
initial_messages = [
    {'role': 'system', 'content': 'You are an AI assistant specialized in astronomy.'},
    {'role': 'user', 'content': 'Tell me about black holes.'},
    {'role': 'assistant', 'content': 'Black holes are regions in space where gravity is so strong that nothing can escape.'}
]

addon = VoiceLLMAddon(initial_messages=initial_messages)
```
