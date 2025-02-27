import requests
import json
import os
import playsound

# API URL
API_URL = "http://127.0.0.1:5000/translate"

# Available languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "bn": "Bengali"
}

# Take user input
text = input("Enter the text to translate: ").strip()
print("Available languages:", SUPPORTED_LANGUAGES)
language = input("Enter the target language code (en/hi/ta/bn): ").strip()
voice_input = input("Do you want voice output? (yes/no): ").strip().lower()
voice = True if voice_input == "yes" else False

# Make API request
payload = {"text": text, "language": language, "voice": voice}
headers = {"Content-Type": "application/json"}
response = requests.post(API_URL, headers=headers, json=payload)

# Handle response
if response.status_code == 200:
    if voice:
        audio_file = "output.mp3"
        with open(audio_file, "wb") as f:
            f.write(response.content)
        print(f"✅ Translation saved as {audio_file}")
        playsound.playsound(audio_file)  # Play the audio
        os.remove(audio_file)  # Delete the file after playing
    else:
        translated_text = response.json().get("translated_text", "Error in translation")
        print(f"✅ Translated Text: {translated_text}")
else:
    print("❌ Error:", response.json().get("error", "Unknown error"))
