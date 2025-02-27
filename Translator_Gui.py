import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator
from gtts import gTTS
import os
import pygame
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
nltk.download('punkt')


def translate_text():
    text = text_input.get("1.0", tk.END).strip()
    language = language_var.get()
    
    if not text:
        messagebox.showerror("Error", "Please enter text to translate!")
        return
    
    translator = Translator()
    try:
        result = translator.translate(text, dest=languages[language]).text
        output_label.config(text=result)
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed! {e}")

def speak_text():
    text = output_label.cget("text").strip()
    language = language_var.get()
    
    if not text:
        messagebox.showerror("Error", "No translated text to speak!")
        return
    
    try:
        tts = gTTS(text=text, lang=languages[language])
        file_path = "speech.mp3"
        tts.save(file_path)
        
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            continue
        
        pygame.mixer.quit()
        os.remove(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Speech synthesis failed! {e}")

def summarize_text():
    text = text_input.get("1.0", tk.END).strip()
    
    if not text:
        messagebox.showerror("Error", "Please enter text to summarize!")
        return
    
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        
        # Limiting summary length based on input size
        num_sentences = min(3, len(text.split('.')))
        summary = summarizer(parser.document, num_sentences)
        
        summary_text = " ".join([str(sentence) for sentence in summary])
        summary_label.config(text=summary_text if summary_text else "Summary unavailable")
    
    except Exception as e:
        messagebox.showerror("Error", f"Summarization failed! {e}")


# GUI Setup
root = tk.Tk()
root.title("Language Translator & Summarizer")
root.geometry("500x500")
root.configure(bg="#f0f0f0")

# Input Text
tk.Label(root, text="Enter Text", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
text_input = tk.Text(root, height=5, width=50)
text_input.pack(pady=5)

# Language Selection
tk.Label(root, text="Select Language", font=("Arial", 12), bg="#f0f0f0").pack()
languages = {"Hindi": "hi", "Tamil": "ta", "Bengali": "bn", "English": "en"}
language_var = ttk.Combobox(root, values=list(languages.keys()))
language_var.pack()
language_var.set("English")

# Buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

translate_btn = tk.Button(button_frame, text="Translate", command=translate_text, bg="#4CAF50", fg="white", width=15)
translate_btn.grid(row=0, column=0, padx=5, pady=5)

speak_btn = tk.Button(button_frame, text="Speak Translation", command=speak_text, bg="#2196F3", fg="white", width=15)
speak_btn.grid(row=0, column=1, padx=5, pady=5)

summarize_btn = tk.Button(button_frame, text="Summarize", command=summarize_text, bg="#FF9800", fg="white", width=15)
summarize_btn.grid(row=0, column=2, padx=5, pady=5)

# Output Labels
tk.Label(root, text="Translated Text", font=("Arial", 12), bg="#f0f0f0").pack()
output_label = tk.Label(root, text="", wraplength=400, fg="blue", bg="white", height=5, width=50, relief="solid")
output_label.pack(pady=5)

tk.Label(root, text="Summarized Text", font=("Arial", 12), bg="#f0f0f0").pack()
summary_label = tk.Label(root, text="", wraplength=400, fg="green", bg="white", height=5, width=50, relief="solid")
summary_label.pack(pady=5)

# Run GUI
root.mainloop()
