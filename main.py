# all our imports
import speech_recognition as sr
from time import sleep
from datetime import datetime
import webbrowser
import pyttsx3
import requests
from bs4 import BeautifulSoup


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
    if "what is the headline news" in speech_text:
        headline_list = []
        intro_list = []

        speak("Would you like normal news or business news")
        news_type = recognize_voice()

        if news_type == "normal":
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

        elif news_type == "business":
            print("....Initialising response")
            url = "https://www.bbc.co.uk/news/business"
            page = requests.get(url)  # Get access to the BBC business news page

            soup = BeautifulSoup(page.content, 'html.parser')
            headline = soup.find('a', class_="gs-c-promo-heading")
            intro = soup.find('p', class_="gs-c-promo-summary")

            title = headline.get_text()
            headline_list.append(title)
            paragraph = intro.get_text()
            intro_list.append(paragraph)

            speak("Here is the main business headline")
            speak(str(headline_list))
            speak(str(intro_list))

        else:
            print("....Initialising response")
            speak("Sorry I cannot seem to find this")


    # quit/exit
    if "quit" in speech_text or "bye" in speech_text or "no" in speech_text:
        speak("Ok, see you later")
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

    speak("I am Jarvis. What can I help you with?")


# wait 2 seconds for adjust_for_ambient_noise() to do its thing
# sleep(2)

if __name__ == '__main__':
    counter = 0
    while True:
        if counter < 1:
            print("Jarvis activated")
            greeting()
            speech = recognize_voice() # listen for voice and convert it into text format
            print("....Initialising response")
            sleep(3)
            reply(speech)   # give "text_version" to reply()
            counter =+ 1
        else:
            speak("Is there anything else I can do for you today.")
            speech = recognize_voice()
            print("....Initialising response")
            sleep(3)
            reply(speech)


