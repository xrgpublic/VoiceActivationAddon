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
