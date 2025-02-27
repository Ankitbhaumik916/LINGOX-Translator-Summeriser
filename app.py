from flask import Flask, request, jsonify, send_file
import spacy
from googletrans import Translator
from gtts import gTTS
import os

# Load NLP Model for Summarization
nlp = spacy.load("en_core_web_sm")

# Initialize Flask App
app = Flask(__name__)
translator = Translator()

# Supported languages for translation and speech
SUPPORTED_LANGUAGES = {
    "hi": "Hindi",
    "ta": "Tamil",
    "bn": "Bengali",
    "en": "English"
}

def translate_text(text, target_lang):
    """Translates text into the target language using Google Translate."""
    if target_lang not in SUPPORTED_LANGUAGES:
        return f"Error: Language '{target_lang}' not supported. Choose from {', '.join(SUPPORTED_LANGUAGES.keys())}."

    translated = translator.translate(text, dest=target_lang)
    return translated.text

def text_to_speech(text, lang):
    """Converts translated text into speech using gTTS."""
    try:
        tts = gTTS(text=text, lang=lang)
        audio_file = "output.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        return str(e)

@app.route("/translate", methods=["POST"])
def process_translation():
    """Handles text translation and returns the translated text."""
    data = request.json
    text = data.get("text", "").strip()
    language = data.get("language", "").strip()
    voice = data.get("voice", False)  # If True, generate voice output

    if not text:
        return jsonify({"error": "No text provided"}), 400
    if not language:
        return jsonify({"error": "No target language provided"}), 400

    translated_text = translate_text(text, language)

    response_data = {"translated_text": translated_text}

    if voice:
        audio_file = text_to_speech(translated_text, language)
        if os.path.exists(audio_file):
            return send_file(audio_file, as_attachment=True, mimetype="audio/mpeg")

    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)
    