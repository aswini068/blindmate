import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import os
import threading
import time
import requests
import speech_recognition as sr
import google.generativeai as genai
import pygame
from elevenlabs import ElevenLabs
from plyer import bluetooth

# API Keys
genai.configure(api_key="AI******")
client = ElevenLabs(api_key="sk*****")
GOOGLE_MAPS_API_KEY = "AI******"

VOICE_ID_ENGLISH = "EX*****"
MOCK_LAT, MOCK_LON = 12.9513, 80.1406  # Chromepet GPS coords


# Welcome Page
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text="Welcome to Voice Assistant for Blind People", font_size=24))
        start_btn = Button(text="Go to Home", size_hint=(1, 0.2))
        start_btn.bind(on_press=self.goto_home)
        layout.add_widget(start_btn)
        self.add_widget(layout)

    def goto_home(self, instance):
        self.manager.current = 'home'


# Home Page
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.audio_queue = []
        self.speaking_flag = [False]
        self.last_speech_time = [time.time()]

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text="Home - Voice Assistant", font_size=24))

        bluetooth_btn = Button(text="Connect Bluetooth")
        bluetooth_btn.bind(on_press=self.connect_bluetooth)
        layout.add_widget(bluetooth_btn)

        location_btn = Button(text="Get Location")
        location_btn.bind(on_press=self.get_location)
        layout.add_widget(location_btn)

        ai_btn = Button(text="Start AI Assistant")
        ai_btn.bind(on_press=self.start_listening)
        layout.add_widget(ai_btn)

        self.add_widget(layout)

    def start_listening(self, instance):
        self.listen_thread = threading.Thread(target=self.listen_audio)
        self.listen_thread.daemon = True
        self.listen_thread.start()

        self.process_thread = threading.Thread(target=self.process_audio)
        self.process_thread.daemon = True
        self.process_thread.start()

    def listen_audio(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            while True:
                try:
                    audio = recognizer.listen(source, timeout=10)
                    text = recognizer.recognize_google(audio, language="en-IN").strip()
                    if text:
                        self.audio_queue.append(text)
                        self.last_speech_time[0] = time.time()
                except:
                    continue

    def process_audio(self):
        while True:
            if self.audio_queue and not self.speaking_flag[0]:
                user_input = self.audio_queue.pop(0)
                self.speaking_flag[0] = True
                response = self.get_gemini_response(user_input)
                self.speak(response)
                self.speaking_flag[0] = False

            if time.time() - self.last_speech_time[0] > 20:
                self.speak("Please say something. I’m here to help.")
                self.last_speech_time[0] = time.time()

            time.sleep(0.1)

    def get_gemini_response(self, text):
        try:
            if "where am i" in text.lower():
                return self.get_current_location()
            elif "direction to" in text.lower():
                dest = text.lower().split("direction to")[-1].strip()
                return self.get_directions_to(dest)
            else:
                prompt = f"Reply politely and friendly in English: {text}"
                model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                response = model.generate_content(prompt)
                return response.text.strip()
        except Exception as e:
            return "Sorry, I couldn’t process that."

    def get_location(self, instance):
        location = self.get_current_location()
        self.speak(location)

    def get_current_location(self):
        try:
            url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={MOCK_LAT},{MOCK_LON}&key={GOOGLE_MAPS_API_KEY}"
            response = requests.get(url).json()
            if response['status'] == 'OK':
                address = response['results'][0]['formatted_address']
                return f"You're currently in {address}."
            else:
                return "Couldn't fetch location right now."
        except:
            return "Something went wrong fetching location."

    def get_directions_to(self, destination):
        try:
            url = f"https://maps.googleapis.com/maps/api/directions/json?origin={MOCK_LAT},{MOCK_LON}&destination={destination}&key={GOOGLE_MAPS_API_KEY}"
            response = requests.get(url).json()
            if response['status'] == 'OK':
                steps = response['routes'][0]['legs'][0]['steps']
                directions = [step['html_instructions'].replace('<b>', '').replace('</b>', '').replace('<div style=\"font-size:0.9em\">', ' ').replace('</div>', '') for step in steps]
                return "Here are the directions: " + ". ".join(directions[:5])
            else:
                return "Couldn't find directions."
        except Exception as e:
            return f"Direction error: {e}"

    def speak(self, text):
        try:
            response = client.text_to_speech.convert(
                voice_id=VOICE_ID_ENGLISH,
                output_format="mp3_44100_128",
                text=text,
                model_id="eleven_multilingual_v2",
            )
            audio_data = b"".join(response)
            filename = "response.mp3"
            with open(filename, "wb") as f:
                f.write(audio_data)

            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            os.remove(filename)
        except Exception as e:
            print(f"ElevenLabs Error: {e}")

    def connect_bluetooth(self, instance):
        try:
            devices = bluetooth.discover_devices()
            if devices:
                self.speak(f"Found {len(devices)} Bluetooth devices. Connecting to the first one.")
                bluetooth.connect(devices[0]['address'])
                self.speak("Connected to Bluetooth device.")
            else:
                self.speak("No Bluetooth devices found.")
        except Exception as e:
            self.speak(f"Bluetooth error: {e}")


# Main App Class
class VoiceAssistantApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(HomeScreen(name='home'))
        return sm


if __name__ == '__main__':
    VoiceAssistantApp().run()
