# VoiceActivationAddon# Voice-Activated LLM Addon

> **Project Issues Notice:**  
> This repository is a work in progress.  I am aware that the playsound has issues and plan to move to a different method of playing sound.  I am also aware that the the first activation "hello" will not play unless the program is warmed up.  This will also be resolved once I change my method of playing the sound.

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

- **Modular Design**: Easily integrated as an addon into existing Python projects.
- **Custom LLM Selection**: Users can specify which LLM model to use at runtime.
- **Custom System Prompt**: Ability to change the AI assistant's behavior via a custom system prompt.
- **Initial Messages Support**: Accepts an initial list of messages to send to Ollama for context.
- **Voice Activation**: Listens for activation phrases like "Hello Llama" or "Hey Llama" to initiate interaction.
- **Voice Query and Response**: Converts spoken queries to text, sends them to the LLM, and reads the AI's response aloud.
- **gTTS Integration**: Utilizes Google Text-to-Speech for generating audible responses.
- **Ollama Integration**: Connects with Ollama to generate AI responses from the specified LLM model.

## Requirements

- **Python** 3.6 >= 3.8 
- **gTTS**: For text-to-speech conversion
- **Ollama API**: Installed and configured on your machine
- **playsound**: For audio playback
- **SpeechRecognition**: For handling voice input
- **pyaudio**: For microphone support in SpeechRecognition
- **argparse**: For command-line argument parsing
- **json**: For handling messages in JSON format

## Installation

Install the required libraries using pip:

```bash
pip install gtts playsound ollama SpeechRecognition pyaudio argparse
```

> **Note**: Installing `pyaudio` may require additional setup, especially on non-Windows systems.

## Usage

### As a Standalone Script

Run the script and specify optional arguments:

```bash
python voice_llm_addon.py --model <model_name> --system_prompt "<your_system_prompt>" --messages_file <path_to_messages_json>
```

- **`--model`**: (Optional) Specify the LLM model to use. Defaults to **llama3.2:1b**.
- **`--system_prompt`**: (Optional) Provide a custom system prompt to change the assistant's behavior.
- **`--messages_file`**: (Optional) Path to a JSON file containing initial messages to send to Ollama.

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
       ]
   )
   addon.run()
   ```

## Customization

- **Change Activation Phrase**: Modify the list `["hello llama", "hey llama"]` in the `run` method to set your own activation phrases.
- **Adjust AI Personality**: Provide a custom `system_prompt` when initializing `VoiceLLMAddon` or via the `--system_prompt` command-line argument.
- **Provide Initial Messages**: Supply an initial list of messages via the `initial_messages` parameter or by specifying a JSON file with `--messages_file`.

## Code Overview

### VoiceLLMAddon Class

The `VoiceLLMAddon` class encapsulates all functionality required for voice interaction with the LLM.

#### Initialization

```python
def __init__(self, model='llama3.2:1b', system_prompt=None, initial_messages=None):
    self.model = model
    self.system_prompt = system_prompt
    self.initial_messages = initial_messages or []
    self.recognizer = sr.Recognizer()
    self.activated = False  # Indicates if the activation phrase was detected
```

- **model**: Specifies the LLM model to use.
- **system_prompt**: Custom system prompt to alter the assistant's behavior.
- **initial_messages**: List of initial messages to send to Ollama.
- **recognizer**: An instance of `sr.Recognizer` for handling voice input.
- **activated**: A flag to track whether the activation phrase has been detected.

### Key Methods

#### `speak(self, text)`

Converts text to speech using gTTS and plays it using `playsound`.

- **Parameters**:
  - `text` (str): The text to convert to speech.

#### `query_ollama(self, prompt)`

Sends a text prompt to the Ollama LLM and returns the response.

- **Parameters**:
  - `prompt` (str): The user's query to send to the LLM.
- **Returns**:
  - `response` (str): The LLM's response.

#### `run(self)`

Starts the voice interaction loop. Listens for the activation phrase and processes user queries.

## Known Issues

- **Audio Playback**: `playsound` may have compatibility issues on some systems. If you experience problems, consider using an alternative like `pygame` or `pydub`.
- **Ollama Model Compatibility**: Ensure the specified LLM model is installed and compatible with Ollama.
- **Microphone Access**: The script requires access to your system's microphone. Ensure that permissions are granted.

## License

This project is licensed under the MIT License.

## Acknowledgments

This project utilizes:

- **[gTTS](https://gtts.readthedocs.io/en/latest/)** for text-to-speech conversion.
- **[Ollama](https://ollama.ai/)** for LLM interactions.
- **[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)** for voice input handling.
- **[playsound](https://pypi.org/project/playsound/)** for audio playback.

# Full Code Listing

```python
import os
import time
import argparse
import playsound
import ollama
import json
from gtts import gTTS
import speech_recognition as sr

class VoiceLLMAddon:
    def __init__(self, model='llama3.2:1b', system_prompt=None, initial_messages=None):
        self.model = model
        self.system_prompt = system_prompt or (
            'You are a funny and self-deprecating AI assistant. '
            'Each of your replies will be a maximum of 2 sentences long. '
            'Short responses are crucial to your success as an AI assistant. '
            'Long replies take a long time to process and ruin the user experience. '
            'Just use any useful data and respond in short responses as an intelligent AI assistant.'
        )
        self.initial_messages = initial_messages or []
        self.recognizer = sr.Recognizer()
        self.activated = False  # Flag to indicate if activation phrase was detected

    def speak(self, text):
        """Convert text to speech, play it, and remove the temporary file."""
        try:
            audio_file = os.path.dirname(__file__) + '\\response.mp3'
            if os.path.exists(audio_file):
                os.remove(audio_file)
                time.sleep(0.5)
            tts = gTTS(text=text, lang='en')
            tts.save(audio_file)
            time.sleep(0.5)
            print("Speaking...")
            playsound.playsound("response.mp3")
            print("Done Speaking")
        except Exception as e:
            print("Exception while speaking:", str(e))

    def query_ollama(self, prompt):
        """Query the Ollama AI assistant with the given prompt and return the response."""
        try:
            messages = self.initial_messages.copy()
            messages.append({'role': 'system', 'content': self.system_prompt})
            messages.append({'role': 'user', 'content': prompt})
            print (messages)
            ollama_response = ollama.chat(
                model=self.model,
                messages=messages,
                stream=False
            )
            response = str(ollama_response['message']['content'])
            print(f"Ollama response: {response}")
            return response
        except Exception as e:
            print("Exception while querying Ollama:", str(e))
            return "I'm sorry, I couldn't process your request."

    def run(self):
        with sr.Microphone() as source:
            print("Calibrating microphone for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source)

            while True:
                try:
                    if not self.activated:
                        print("Listening for activation phrase...")
                        audio = self.recognizer.listen(source)
                        print("Processing activation phrase...")
                        text = self.recognizer.recognize_google(audio).lower()
                        print(f"Detected text: {text}")
                        if text not in ["hello llama", "hey llama"]:
                            print("Activation phrase not detected.")
                            continue
                        print("Activation phrase detected.")
                        self.activated = True
                        self.speak("Hello!")
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
    args = parser.parse_args()

    initial_messages = []
    if args.messages_file:
        try:
            with open(args.messages_file, 'r') as f:
                initial_messages = json.load(f)
            print(f"Loaded initial messages from {args.messages_file}")
        except Exception as e:
            print(f"Failed to load messages from {args.messages_file}: {e}")

    addon = VoiceLLMAddon(
        model=args.model,
        system_prompt=args.system_prompt,
        initial_messages=initial_messages
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
