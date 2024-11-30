import pyttsx3
from decouple import config
from datetime import datetime
from conv import random_text
import speech_recognition as sr
from random import choice
import keyboard
import os
import subprocess as sp

engine = pyttsx3.init()  # pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
# 3, 4, 5, 11, 15, 31, 33, 34, 38, 39, 95, 132, 163
# engine.setProperty('voice', voices[132].id) # 132

USER = config('USER')
HOSTNAME = 'KHADIJAH'

APP_MAP = {
    "terminal": "Terminal",
    "facetime": "FaceTime",
    "notes": "Notes",
    "discord": "Discord",
    "firefox": "Firefox",
    "safari": "Safari",
    "chrome": "Google Chrome",
    "google chrome": "Google Chrome",
    "music": "Music",
    "apple music": "Music",
    "photos": "Photos",
    "messages": "Messages",
    "vs code": "Visual Studio Code",
    "visual studio code": "Visual Studio Code"
}


def test_voices():
    for voice in voices:
        print(voice, voice.id)
        engine.setProperty('voice', voice.id)
        engine.say("Hello, I am Khadijah, your digital assistant!")
        engine.runAndWait()
        engine.stop()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_me():
    hour = datetime.now().hour

    if (hour >= 6) and (hour <= 12):
        speak(f'Good morning {USER}')
    elif (hour >= 12) and (hour <= 16):
        speak(f'Good afternoon {USER}')
    elif (hour >= 16) and (hour <= 19):
        speak(f'Good evening {USER}')

    speak(f'I am {HOSTNAME}. How my I assist you today, {USER}?')


listening = False


def start_listening():
    global listening
    listening = True
    print("Started listening")


def pause_listening():
    global listening
    listening = False
    print("Paused listening")


keyboard.add_hotkey('j', start_listening)
keyboard.add_hotkey('k', pause_listening)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us').lower()
        print(query)

    except Exception:
        speak("Sorry, I couldn't understand. Can you please repeat that?")
        query = 'None'
    return query


def open_app(app_name):
    speak(f"Okay, opening {app_name}.")
    sp.run(["open", "-a", app_name])


def close_app(app_name):
    speak(f"Okay, closing {app_name}.")
    apple_script = f'tell application "{app_name}" to quit'
    sp.run(["osascript", "-e", apple_script])


def parse_query(query):
    if 'how are you' in query:
        speak("I am absolutely fine! What about you?")
    elif 'open' in query:
        app_name = query.split('open')[-1].strip()
        app_name = APP_MAP.get(app_name, app_name.title())
        open_app(app_name)
    elif 'quit' in query:
        app_name = query.split('quit')[-1].strip()
        app_name = APP_MAP.get(app_name, app_name.title())
        close_app(app_name)
    elif 'stop' in query or 'exit' in query:
        speak("Goodbye! Have a great day!")
        exit()


if __name__ == '__main__':
    # speak('Hello, I am Khadijah, your digital assistant. How may I help you today?')
    # test_voices()
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            parse_query(query)
