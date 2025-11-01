# min_sonu-voice-assistant
in-Sonu is a personal AI-powered voice assistant built using Python. It listens, understands, and performs real-time tasks through natural voice commands — from sending WhatsApp messages to opening applications, translating text, and even telling jokes!
# 🎙️ Min-Sonu — AI Voice Assistant (Python)

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🧠 Overview
**Min-Sonu** is an intelligent **AI-powered voice assistant** built using **Python**.  
It can understand natural language voice commands and perform real-time automation tasks such as sending WhatsApp messages, sending emails, opening apps, translating text, telling jokes, and more.

This project combines the power of **Speech Recognition**, **Text-to-Speech**, and **Task Automation** — all integrated into one interactive desktop assistant.  
A perfect beginner-to-intermediate Python project that demonstrates **real-world AI application development**.

---

## 🚀 Features

✅ **Voice Command Recognition** — Powered by `speech_recognition`  
✅ **Text-to-Speech Conversion** — Natural voice output using `pyttsx3`  
✅ **WhatsApp Integration** — Send instant or scheduled messages with `pywhatkit`  
✅ **Email Automation** — Send emails through secure SMTP connection  
✅ **App Launcher** — Open Chrome, Calculator, Notepad, etc.  
✅ **Text Translation** — Translate any text into different languages using `googletrans`  
✅ **Fun Add-ons** — Jokes, shutdown commands, and Google searches  
✅ **Dynamic Contacts** — Managed easily through a JSON configuration file

---

## 🧩 Tech Stack

- **Language:** Python  
- **Core Libraries:**  
  `speech_recognition`, `pyttsx3`, `pywhatkit`, `googletrans`, `smtplib`, `datetime`, `webbrowser`, `subprocess`, `json`, `os`

---

## 🛠️ Installation & Setup

### 1️⃣ Clone this repository
```bash
git clone https://github.com/yourusername/min-sonu.git
cd min-sonu
## install dependencies
pip install -r requirements.txt
##create a config.json for saving contact details
{
  "EMAIL_ADDRESS": "your_email@gmail.com",
  "EMAIL_PASSWORD": "your_password",
  "WHATSAPP_CONTACTS": {
    "puppy": "+919876xxxxx"
  },
  "EMAIL_CONTACTS": {
    "john": "john@example.com"
  }
}
##run this assistant
python min_sonu.py

