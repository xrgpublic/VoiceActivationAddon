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
