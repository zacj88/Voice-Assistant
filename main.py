# all our imports
import speech_recognition as sr
from time import sleep
from datetime import datetime
import webbrowser
import pyttsx3
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config

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
            speak("Sorry, can you repeat that sir...")
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

    # news
    if "what are the  headlines" in speech_text:
        headline_list = []
        intro_list = []

        print("....Initialising response")
        url = "https://www.bbc.co.uk/news"
        page = requests.get(url)  # Get access to the BBC news page

        soup = BeautifulSoup(page.content, 'html.parser')
        headline = soup.find('a', class_="gs-c-promo-heading")
        intro = soup.find('p', class_="gs-c-promo-summary")

        title = headline.get_text()
        headline_list.append(title)
        paragraph = intro.get_text()
        intro_list.append(paragraph)

        speak("Here is the main headline")
        speak(str(headline_list))
        speak(str(intro_list))
        print(headline_list)

    # music
    if "music" in speech_text:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.api_key,
                                                                   client_secret=config.api_secret))
        speak("What artist would you like to know about")
        artist = recognize_voice()

        if artist != '':
            results = sp.search(q=artist, type="album", limit=20)
            for idx, album in enumerate(results['albums']['items']):
                print(idx, album['name'])
            speak("Here are the albums released by  " + artist)

    # quit/exit
    if "quit" in speech_text or "bye" in speech_text or "no" in speech_text:
        speak("Ok, goodbye")
        print("Jarvis shutting down")
        exit()

def greeting():
    hour = int(datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning sir!")

    elif 12 <= hour < 18:
        speak("Good Afternoon sir!")

    else:
        speak("Good Evening sir!")

    speak("What can I help you with?")


# wait 2 seconds for adjust_for_ambient_noise() to do its thing
# sleep(2)

def talk():
    counter = 0
    while True:
        if counter < 1:
            print("Jarvis activated")
            speech = recognize_voice() # listen for voice and convert it into text format
            if "jarvis" in speech:
                print("....Initialising response")
                greeting()
                sleep(3)
                reply(speech)   # give "text_version" to reply()
                counter =+ 1
        else:
            speech = recognize_voice()
            print("....Initialising response")
            sleep(3)
            reply(speech)


if __name__ == '__main__':
    talk()
