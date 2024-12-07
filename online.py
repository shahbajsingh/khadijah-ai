import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config
from const import NEWS_API_KEY, WEATHER_API_KEY

EMAIL = ""
PASSWORD = ""


def find_my_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        ip_address = response.json()
        return ip_address['ip']
    except requests.exceptions.RequestException:
        return None


def search_wikipedia(query):
    try:
        result = 'According to Wikipedia, ' + \
            wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:  # disambiguation error
        options = e.options
        return f"The term '{query}' is ambiguous. It may refer to: {', '.join(options[:5])}, or more. Please specify further."
    except wikipedia.exceptions.PageError:  # no page found
        return f"No Wikipedia page found for '{query}'. Please try another term."


def search_google(query):
    kit.search(query)


def youtube(video):
    kit.playonyt(video)


def send_email(receiver_addr, subject, message):
    try:
        email = EmailMessage()
        email['From'] = EMAIL
        email['To'] = receiver_addr
        email['Subject'] = subject
        email.set_content(message + '\n\nSent with Khadija AI')

        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.starttls()
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(email)
        smtp.close()

        return True
    except Exception as e:
        print(e)
        return False


def get_news():
    headlines = []
    try:
        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&category=general&apiKey={NEWS_API_KEY}"
        )
        response.raise_for_status()
        result = response.json()
        articles = result.get('articles', [])

        for article in articles:
            headlines.append(article.get("title"))

        return headlines[:5]
    except requests.exceptions.RequestException:
        return []


def get_weather(city):
    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
        )
        response.raise_for_status()
        result = response.json()

        forecast = result['weather'][0]['main']
        temp_k = result['main']['temp']
        feels_k = result['main']['feels_like']

        temp_f = round((temp_k - 273.15) * 9/5 + 32)
        feels_f = round((feels_k - 273.15) * 9/5 + 32)

        return forecast, f'{temp_f}ºF', f'{feels_f}ºF'
    except requests.exceptions.RequestException:
        return None, None, None
