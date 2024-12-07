import pyttsx3
from decouple import config
from datetime import datetime
from conv import filler, thanks, how_are_you, thanks_cmd, stop_cmd, how_are_you_cmd, wiki_cmd, google_cmd, youtube_cmd, email_cmd, news_cmd, weather_cmd
import speech_recognition as sr
from random import choice
import keyboard
import os
import requests
import subprocess as sp
from online import find_my_ip, search_wikipedia, search_google, youtube, send_email, get_news, get_weather

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
    i = 0
    engine.setProperty('rate', 200)

    for voice in voices:
        print(f'{voice}, {voice.id}, index={i}')
        i += 1
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
    elif (hour >= 16) and (hour <= 24):
        speak(f'Good evening {USER}')

    speak(
        f'Hello, I am {HOSTNAME}, your digital assistant. How my I help you today, {USER}?')


listening = True


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


def add_hotkeys():
    keyboard.add_hotkey('j', start_listening)
    keyboard.add_hotkey('k', pause_listening)


def remove_hotkeys():
    keyboard.remove_all_hotkeys()


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
    if any(cmd in query for cmd in how_are_you_cmd):  # HOW ARE YOU
        speak(choice(how_are_you))

    elif 'ip address' in query:  # CHECK IP ADDRESS
        try:
            ip_address = find_my_ip()
        except requests.exceptions.RequestException:
            speak("Sorry, I couldn't retrieve your IP address due to a network issue.")
            return

        speak(f'Your IP address is {ip_address}')

    elif any(cmd in query for cmd in wiki_cmd):  # SEARCH WIKIPEDIA
        speak('What do you want to search on Wikipedia?')
        query = take_command().lower()

        try:
            result = search_wikipedia(query)
        except requests.exceptions.RequestException:
            speak("Sorry, I couldn't access Wikipedia due to a network issue.")
            return

        speak(result)
        print(result)

    elif any(cmd in query for cmd in google_cmd):  # SEARCH GOOGLE
        speak('What do you want to search on Google?')
        query = take_command().lower()

        try:
            search_google(query)
        except requests.exceptions.RequestException:
            speak("Sorry, I couldn't perform a Google search due to a network issue.")
            return

    elif any(cmd in query for cmd in youtube_cmd):  # SEARCH YOUTUBE
        speak('What do you want to play on YouTube?')
        video = take_command().lower()

        try:
            youtube(video)
        except requests.exceptions.RequestException:
            speak("Sorry, I couldn't access YouTube due to a network issue.")
            return

    elif any(cmd in query for cmd in email_cmd):  # COMPOSE EMAIL
        speak('Okay, to whom do you want to send it? Input in terminal.')
        remove_hotkeys()
        receiver_addr = input("Email address: ")  # TERMINAL INPUT
        add_hotkeys()
        speak('What should be the subject?')
        subject = take_command().capitalize()
        speak('And what do you want to say?')
        message = take_command().capitalize()

        try:
            if send_email(receiver_addr, subject, message):
                speak(f'Okay, the email has been sent to {receiver_addr}.')
            else:
                speak('Something went wrong.')
        except requests.exceptions.RequestException:
            speak("Sorry, I couldn't send the email due to a network issue.")
            return

    elif any(cmd in query for cmd in news_cmd):  # READ NEWS
        try:
            headlines = get_news()
        except requests.exceptions.RequestException:
            speak("Sorry, I couldn't fetch the news due to a network issue.")
            return

        if headlines:
            speak("Okay, here are the top news headlines.")
            [speak(headline) for headline in headlines]
        print(*get_news(), sep='\n')

    elif any(cmd in query for cmd in weather_cmd):  # READ WEATHER
        capture = query.lower().split()
        if 'in' in capture:
            in_index = capture.index('in')
            city_capture = capture[in_index+1:]
            city = ' '.join(city_capture).title() if city_capture else None
        else:
            city = None

        if not city:
            ip_address = find_my_ip()
            
            try:
                response = requests.get(f'https://ipinfo.io/{ip_address}/json')
                response.raise_for_status()
                data = response.json()
                city = data.get('city', None)
            except requests.exceptions.RequestException:
                speak(
                    "Sorry, I was unable to determine the weather for your location due to a network issue.")
                return

            if not city:
                speak('Sorry, I was unable to determine your location')
                return

        try:
            forecast, temperature, feels_like = get_weather(city)
        except requests.exceptions.RequestException:
            speak("Sorry, I was unable to fetch weather data due to a network issue.")
            return

        speak(f"Okay, here's the weather for {city}")
        speak(
            f'The temperature is {temperature}, but it feels like {feels_like}')
        speak(f'The forecast mentions {forecast}')
        print(
            f'Forecast: {forecast}\nTemperature: {temperature}\nFeels Like: {feels_like}')

    elif 'open' in query:  # OPEN APPLICATION
        app_name = query.split('open')[-1].strip()
        app_name = APP_MAP.get(app_name, app_name.title())
        open_app(app_name)

    elif 'quit' in query:  # QUIT APPLICATION
        app_name = query.split('quit')[-1].strip()
        app_name = APP_MAP.get(app_name, app_name.title())
        close_app(app_name)

    elif any(cmd in query for cmd in thanks_cmd):  # THANK YOU
        speak(choice(thanks))

    elif any(cmd in query for cmd in stop_cmd):  # EXIT KHADIJA
        speak(f"Okay, have a great day {USER}!")
        exit()


if __name__ == '__main__':
    # speak('Hello, I am Khadijah, your digital assistant. How may I help you today?')
    # test_voices()
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            parse_query(query)
