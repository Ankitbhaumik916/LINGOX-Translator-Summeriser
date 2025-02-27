from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_mysqldb import MySQL
from googletrans import Translator
from gtts import gTTS
import os
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'KAERMORHEN2311'
app.config['MYSQL_DB'] = 'translator_db'

mysql = MySQL(app)
translator = Translator()
languages = {"Hindi": "hi", "Tamil": "ta", "Bengali": "bn", "English": "en"}

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text', '')
    language = data.get('language', 'English')

    if not text:
        return jsonify({'error': 'Text is required'}), 400

    try:
        translated = translator.translate(text, dest=languages[language]).text

        # Store translation in MySQL
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO translations (input_text, translated_text, language) VALUES (%s, %s, %s)",
                    (text, translated, language))
        mysql.connection.commit()
        cur.close()

        return jsonify({'translated_text': translated})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'Text is required'}), 400

    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 3)  # Summarize to 3 sentences

        summary_text = " ".join(str(sentence) for sentence in summary)

        # Store summary in MySQL
        cur = mysql.connection.cursor()
        cur.execute("UPDATE translations SET summary=%s WHERE input_text=%s", (summary_text, text))
        mysql.connection.commit()
        cur.close()

        return jsonify({'summary': summary_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/speak', methods=['POST'])
def speak_text():
    data = request.json
    text = data.get('text', '')
    language = languages.get(data.get('language', 'English'), 'en')

    if not text:
        return jsonify({'error': 'Text is required'}), 400

    try:
        tts = gTTS(text=text, lang=language)
        file_path = "output.mp3"
        tts.save(file_path)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT input_text, translated_text, language, summary FROM translations")
        records = cur.fetchall()
        cur.close()

        history = [{'text': row[0], 'translated_text': row[1], 'language': row[2], 'summary': row[3]} for row in records]
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
