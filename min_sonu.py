import os
import json
import webbrowser
import subprocess
import random
import pyttsx3
import speech_recognition as sr
from googletrans import Translator
import pywhatkit as kit
import smtplib
import datetime
import time

# ------------------- LOAD CONFIG -------------------
CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

EMAIL_ADDRESS = config.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = config.get("EMAIL_PASSWORD")

WHATSAPP_CONTACTS = config.get("WHATSAPP_CONTACTS", {})
EMAIL_CONTACTS = config.get("EMAIL_CONTACTS", {})

# ------------------- SPEECH ENGINE -------------------
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # female voice
engine.setProperty("rate", 170)

def speak(text):
    print(f"Min-Sonu: {text}")
    engine.say(text)
    engine.runAndWait()

# ------------------- LISTENING -------------------
recognizer = sr.Recognizer()

def listen(duration=6):
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=duration)
            text = recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text.lower()
        except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
            return ""

# ------------------- FEATURES -------------------
def tell_joke():
    jokes = [
        "Why don’t skeletons fight each other? Because they don’t have the guts.",
        "I asked my computer for a joke, but it just gave me a 404 error.",
        "Why did the math book look sad? Because it had too many problems."
    ]
    return random.choice(jokes)

def translate_text(text, dest="hi"):
    translator = Translator()
    translated = translator.translate(text, dest=dest)
    return translated.text

def open_app(app_name):
    if "notepad" in app_name:
        subprocess.Popen(["notepad.exe"])
    elif "calculator" in app_name:
        subprocess.Popen(["calc.exe"])
    elif "chrome" in app_name:
        subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"])
    else:
        speak("Sorry, I can’t open that app right now.")

def shutdown_pc():
    os.system("shutdown /s /t 5")

# ------------------- UPDATED WHATSAPP FUNCTION -------------------
def send_whatsapp(contact_name, message):
    if contact_name in WHATSAPP_CONTACTS:
        phone = WHATSAPP_CONTACTS[contact_name]
        speak(f"Sending WhatsApp message to {contact_name}...")

        try:
            # ✅ Try sending instantly first
            kit.sendwhatmsg_instantly(phone, message, wait_time=10, tab_close=True, close_time=3)
            speak("Message sent instantly ✅")

        except Exception as e:
            speak(f"Instant send failed, scheduling message due to: {e}")
            
            # Schedule 2 minutes later
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute + 2

            # Fix overflow (e.g., 23:59 -> 00:01)
            if minute >= 60:
                minute -= 60
                hour = (hour + 1) % 24

            try:
                kit.sendwhatmsg(phone, message, hour, minute, wait_time=10, tab_close=True, close_time=3)
                speak(f"Message scheduled to {contact_name} at {hour}:{minute:02d} 🕒")
            except Exception as e2:
                speak(f"Failed to schedule message: {e2}")

            time.sleep(10)
    else:
        speak("Contact not found in WhatsApp contacts.")

# ------------------- EMAIL FUNCTION -------------------
def send_email(to_name, subject, body):
    if to_name not in EMAIL_CONTACTS:
        speak("Email contact not found.")
        return
    to_address = EMAIL_CONTACTS[to_name]
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            msg = f"Subject: {subject}\n\n{body}"
            server.sendmail(EMAIL_ADDRESS, to_address, msg)
        speak("Email has been sent successfully.")
    except Exception as e:
        speak(f"Failed to send email: {e}")

# ------------------- CALL + CONTACT LIST -------------------
def call_contact(contact_name):
    if contact_name in WHATSAPP_CONTACTS:
        speak(f"Calling {contact_name}... (simulated)")
    else:
        speak("Contact not found in contacts.")

def list_contacts():
    whatsapp = config.get("WHATSAPP_CONTACTS", {})
    emails = config.get("EMAIL_CONTACTS", {})

    if not whatsapp and not emails:
        speak("You don’t have any contacts saved yet.")
        return

    if whatsapp:
        speak("Here are your WhatsApp contacts:")
        for name, number in whatsapp.items():
            speak(f"{name}, number {number}")

    if emails:
        speak("Here are your Email contacts:")
        for name, email in emails.items():
            speak(f"{name}, email {email}")

# ------------------- MAIN -------------------
if __name__ == "__main__":
    speak("Hello, I am Min-Sonu, your AI assistant. How can I help you today?")

    while True:
        query = listen(duration=8)
        if not query:
            continue

        if "exit" in query or "quit" in query or "stop" in query:
            speak("Goodbye! Have a nice day.")
            break

        elif "play" in query:
            song = query.replace("play", "").strip()
            speak(f"Playing {song} on YouTube.")
            kit.playonyt(song)

        elif "joke" in query:
            speak(tell_joke())

        elif "translate" in query:
            speak("What sentence should I translate?")
            text_to_translate = listen(duration=6)
            translated = translate_text(text_to_translate, dest="fr")
            speak(f"In French: {translated}")

        elif "open" in query:
            open_app(query)

        elif "shutdown" in query:
            speak("Shutting down your computer in 5 seconds.")
            shutdown_pc()

        elif "search" in query:
            search_term = query.replace("search", "").strip()
            url = f"https://www.google.com/search?q={search_term}"
            webbrowser.open(url)
            speak(f"Here are the search results for {search_term}.")

        elif "whatsapp" in query or "message" in query:
            speak("Who should I message?")
            contact = listen(duration=5)
            speak("What is the message?")
            message = listen(duration=8)
            if contact and message:
                send_whatsapp(contact, message)

        elif "email" in query:
            speak("Who should I email?")
            to_name = listen(duration=5)
            speak("What is the subject?")
            subject = listen(duration=5)
            speak("What is the body?")
            body = listen(duration=8)
            if to_name and body:
                send_email(to_name, subject, body)

        elif "call" in query:
            speak("Who should I call?")
            contact = listen(duration=5)
            call_contact(contact)

        elif "list contacts" in query or "my contacts" in query:
            list_contacts()

        else:
            speak("Sorry, I didn’t understand that. Please try again.")
