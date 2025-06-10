import speech_recognition as sr
import webbrowser as wb
import pyttsx3 as pt
import kitchen
import requests as req
from openai import OpenAI

# Initialize recognizer and TTS
reconize = sr.Recognizer()
ttsx = pt.init()
newsapi = "5da9e93847844e2e85880fcffc711839"

def speak(text):
    ttsx.say(text)
    ttsx.runAndWait()


def aiProcess(command):
    client = OpenAI(
       # api_key=
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like AWS and Google Cloud."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

def processcommand(c):
    print(c)
    c = c.lower()

    if "open google" in c:
        wb.open("https://www.google.com")
    elif "open facebook" in c:
        wb.open("https://www.facebook.com")
    elif "open youtube" in c:
        wb.open("https://www.youtube.com")
    elif "open instagram" in c:
        wb.open("https://www.instagram.com")
    elif "open linkedin" in c:
        wb.open("https://www.linkedin.com")
    elif c.startswith("play"):
        parts = c.split(" ")
        if len(parts) > 1:
            channel_name = parts[1]
            if channel_name in kitchen.rec:
                link = kitchen.rec[channel_name]
                speak(f"Playing {channel_name} on YouTube.")
                wb.open(link)
            else:
                speak(f"Sorry, I don't know {channel_name}.")
        else:
            speak("Please say the name of the YouTube channel.")
    elif "news" in c:
        response = req.get(f"https://newsapi.org/v2/everything?q=tesla&from=2025-04-21&sortBy=publishedAt&apiKey={newsapi}")
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            speak("Here are the top Tesla headlines.")
            for i, article in enumerate(articles[:5], 1):
                title = article.get("title", "No Title")
                print(f"{i}. {title}")
                speak(title)
        else:
            speak(f"Failed to fetch news. Status Code: {response.status_code}")
    else:
        result=aiProcess(c.lower())
        speak(result)



if __name__ == "__main__":
    speak("Initializing...")
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening")
                audio = reconize.listen(source, timeout=5)
            word = reconize.recognize_google(audio)
            if word.lower() == "hello":
                speak("Yeah?")
                with sr.Microphone() as source:
                    print("How may I assist you?")
                    audio = reconize.listen(source)
                    command = reconize.recognize_google(audio)
                    processcommand(command)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            speak(f"API request error: {e}")
        except Exception as e:
            speak(f"Unexpected error: {e}")

