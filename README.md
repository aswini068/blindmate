# blindmate

# Voice Assistant for Blind People 

A smart, AI-powered voice assistant designed to support **blind and visually impaired users**. This app provides real-time voice interaction, location guidance using Google Maps, and Bluetooth device connection — all with spoken input and output.

##  Features

-  **Voice Interaction**: Recognizes voice commands using `SpeechRecognition` and responds using `ElevenLabs` realistic text-to-speech.
-  **GPS Location Services**: Fetches the user's current location using Google Maps API.
-  **Direction Assistance**: Provides walking or driving directions to a destination via voice.
-  **Bluetooth Connectivity**: Scans and connects to available Bluetooth devices.
-  **Gemini AI Assistant**: Uses Google's Gemini model for intelligent and conversational replies.

##  Tech Stack

- **Python**
- **Kivy** for GUI and screen navigation
- **Google Gemini API** (`google.generativeai`)
- **Google Maps API**
- **ElevenLabs TTS API**
- **SpeechRecognition** with Google Speech
- **Pygame** for audio playback
- **Plyer Bluetooth** for hardware interaction

##  Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   