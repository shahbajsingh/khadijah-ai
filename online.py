import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config

EMAIL = ""
PASSWORD = ""

def find_my_ip():
    response = requests.get('https://api.ipify.org?format=json')
    ip_address = response.json()
    return ip_address['ip']


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