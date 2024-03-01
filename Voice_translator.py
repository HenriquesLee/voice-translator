import os
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from tkinter import *
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS

# Create a dictionary mapping language codes to their full names
language_dict = {code: name for code, name in LANGUAGES.items()}

# Generate a list of language options with full names
output_language_options = list(language_dict.values())

# Function to convert speech to text
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        input_text.delete(1.0, END)
        print("Speak something...")
        audio = r.listen(source)
        print("Converting speech to text...")
        try:
            text = r.recognize_google(audio)
            input_text.insert(END, text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error making the request: {e}")

# Function to translate text
def translate_text():
    translator = Translator()
    input_text_value = input_text.get("1.0", "end-1c")
    output_language = output_language_var.get()

    if input_text_value:
        translation = translator.translate(input_text_value, dest=output_language)
        output_text.delete(1.0, END)
        output_text.insert(END, translation.text)

        # Save translation to audio file
        translation_audio = translator.translate(input_text_value, dest=output_language, src='en')
        translation_audio_file = "translation_audio.wav"
        translation_audio_text = translation_audio.text
        translation_audio_text = translation_audio_text.encode("utf-8")  # Fix for non-ASCII characters
        tts = gTTS(text=translation_audio_text, lang=output_language, slow=False)
        tts.save(translation_audio_file)

        # Play the translation audio
        output_sound = AudioSegment.from_wav(translation_audio_file)
        play(output_sound)
        os.remove(translation_audio_file)
    else:
        output_text.delete(1.0, END)
        print("Please enter text for translation.")

# Function to speak the translated text
def speak_translation():
    translation_text = output_text.get("1.0", "end-1c")
    if translation_text:
        tts = gTTS(text=translation_text, lang=output_language_var.get(), slow=False)
        tts.save("translation_speech.wav")
        translation_sound = AudioSegment.from_wav("translation_speech.wav")
        play(translation_sound)
        os.remove("translation_speech.wav")
    else:
        print("No translated text to speak.")

# GUI setup
root = Tk()
root.title("Speech to Text and Translation")

# Input text box
input_text = Text(root, height=5, width=50)
input_text.pack()

# Button to start speech-to-text conversion
speech_to_text_button = Button(root, text="Speech to Text", command=speech_to_text)
speech_to_text_button.pack()

# Dropdown for selecting output language with full names
output_language_var = StringVar()
output_language_var.set("English")  # Set default language
output_language_dropdown = OptionMenu(root, output_language_var, *output_language_options)
output_language_dropdown.pack()

# Button to start translation
translate_button = Button(root, text="Translate", command=translate_text)
translate_button.pack()

# Output text box
output_text = Text(root, height=5, width=50)
output_text.pack()

# Button to speak the translation
speak_button = Button(root, text="Speak Translation", command=speak_translation)
speak_button.pack()

root.mainloop()
