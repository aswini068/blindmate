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


##  Installation Process

Follow these steps to set up and run the project on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

---

### 2. (Optional) Create a Virtual Environment

It's recommended to use a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

---

### 3. Install All Required Packages

Install all dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install manually:

```bash
pip install kivy requests SpeechRecognition google-generativeai pygame elevenlabs plyer
```

---

### 4. Set API Keys

Open the `main.py` file and replace the placeholders with your actual API keys:

- `AI******` → Your **Google Gemini** API key
- `sk_******` → Your **ElevenLabs** API key
- `EX*******` → Your **ElevenLabs** Voice ID
- Also replace Google Maps API key if used: `GOOGLE_MAPS_API_KEY = "AI******"`

Get API keys here:
- [Google Gemini API](https://aistudio.google.com/app/apikey)
- [ElevenLabs](https://www.elevenlabs.io/)
- [Google Maps API](https://console.cloud.google.com/)

---

### 5. Run the Application

```bash
python main.py
```
   