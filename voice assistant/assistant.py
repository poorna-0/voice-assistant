import speech_recognition as sr
import pyttsx3
import webbrowser
import pyautogui
import os
import subprocess
import ctypes
import time

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        return command.lower()
    except:
        return ""

def open_app(app_name):
    apps = {
        "notepad": "notepad.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "whatsapp": "C:\\Users\\venkaat\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
    }
    if app_name in apps:
        subprocess.Popen(apps[app_name])
        speak(f"Opening {app_name}")
    else:
        speak(f"{app_name} not found.")

def open_website(name):
    sites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "amazon": "https://amazon.in",
        "flipkart": "https://flipkart.com",
        "myntra": "https://myntra.com",
        "ajio": "https://ajio.com",
        "gfg": "https://geeksforgeeks.org",
        "chatgpt": "https://chat.openai.com",
        "pinterest": "https://pinterest.com",
        "github": "https://github.com"
    }
    if name in sites:
        webbrowser.open(sites[name])
        speak(f"Opening {name}")
    else:
        speak(f"Website {name} not found.")

def scroll_page(direction):
    if direction == "up":
        pyautogui.scroll(500)
    elif direction == "down":
        pyautogui.scroll(-500)

def control_volume(action):
    if action == "mute":
        pyautogui.press("volumemute")
    elif action == "up":
        pyautogui.press("volumeup", presses=5)
    elif action == "down":
        pyautogui.press("volumedown", presses=5)

def system_control(action):
    if action == "lock":
        ctypes.windll.user32.LockWorkStation()
    elif action == "shutdown":
        os.system("shutdown /s /t 1")
    elif action == "restart":
        os.system("shutdown /r /t 1")

def send_whatsapp_message():
    speak("Who is the message for?")
    contact = listen()
    speak("What is the message?")
    message = listen()

    pyautogui.hotkey("win", "s")
    time.sleep(1)
    pyautogui.write("whatsapp")
    pyautogui.press("enter")
    time.sleep(4)
    pyautogui.write(contact)
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.write(message)
    pyautogui.press("enter")
    speak("Message sent.")

def run_assistant(log_callback, stop_signal):
    active = False
    while not stop_signal():
        command = listen()
        if not command:
            continue

        if "charge" in command:
            active = True
            speak("I am listening.")
            log_callback("Assistant activated.")

        elif "bye charge" in command:
            active = False
            speak("Deactivating.")
            log_callback("Assistant deactivated.")

        elif active:
            log_callback(f"Command: {command}")

            if "open" in command:
                for app in ["notepad", "chrome", "whatsapp"]:
                    if app in command:
                        open_app(app)
                        break
                for site in ["youtube", "google", "amazon", "flipkart", "myntra", "ajio", "gfg", "chatgpt", "pinterest", "github"]:
                    if site in command:
                        open_website(site)
                        break
            elif "scroll up" in command:
                scroll_page("up")
            elif "scroll down" in command:
                scroll_page("down")
            elif "volume up" in command:
                control_volume("up")
            elif "volume down" in command:
                control_volume("down")
            elif "mute" in command:
                control_volume("mute")
            elif "lock" in command:
                system_control("lock")
            elif "shutdown" in command:
                system_control("shutdown")
            elif "restart" in command:
                system_control("restart")
            elif "send whatsapp" in command:
                send_whatsapp_message()
            elif "exit" in command or "quit" in command:
                speak("Goodbye!")
                log_callback("Assistant stopped.")
                break
