# all our imports
import speech_recognition as sr
from time import sleep
from datetime import datetime
import webbrowser
import pyttsx3


r = sr.Recognizer()
engine = pyttsx3.init()

# turning text to speech.
def speak(text):
    engine.say(text)
    engine.runAndWait()


# function to return a text version of our speech
def recognize_voice():
    text = ''

    # create an instance of the Microphone class
    with sr.Microphone() as source:
        # adjust for ambient noise
        r.adjust_for_ambient_noise(source)

        # capture the voice
        voice = r.listen(source)

        # let's recognize it
        try:
            text = r.recognize_google(voice)
        except sr.RequestError:
            speak("Sorry, the I can't access the Google API...")
        except sr.UnknownValueError:
            speak("Sorry, I am unable to recognize your speech...")
    return text.lower()



# returns a message depending on the users speech, collected from recognize_voice().
def reply(speech_text):
    # name
    if "what is your name" in speech_text:
        speak("My name is JARVIS")

    # how are you?
    if "how are you" in speech_text:
        speak("I am fine...")

    # date
    if "what is the date" in speech_text:
        # get today's date and format it - 9 November 2020
        date = datetime.now().strftime("%-d %B %Y")
        speak(date)

    # time
    if "what is the time" in speech_text:
        # get current time and format it like - 02 28
        time = datetime.now().time().strftime("%H %M")
        speak("The time is " + time)

    # search google
    if "search" in speech_text:
        speak("What do you want me to search for?")
        keyword = recognize_voice()

        # if "keyword" is not empty
        if keyword != '':
            url = "https://google.com/search?q=" + keyword

            # web browser module to work with the web browser
            speak("Here are the search results for " + keyword)
            webbrowser.open(url)
            sleep(3)

    # quit/exit
    if "quit" in speech_text or "exit" in speech_text or "bye" in speech_text:
        speak("Ok, I am going to take a nap...")
        exit()


# wait 4 seconds for adjust_for_ambient_noise() to do its thing
sleep(4)

while True:
    speak("Is there anything I can help you with...")
    # listen for voice and convert it into text format
    text_version = recognize_voice()

    # give "text_version" to reply() fn
    reply(text_version)
