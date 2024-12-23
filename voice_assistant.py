# imports

# convert text to speech
import pyttsx3 as ts

# import datetime to get the date, time
import datetime

# https://pypi.org/project/SpeechRecognition/
# https://www.geeksforgeeks.org/python-speech-recognition-module/
import speech_recognition as sr

#################################################################################################
# Functions

# create a function that starts the engine for pyttsx3 
def start_engine():  
    """Initialise the text-to-speech engine.

    :raises ImportError: _description_
    :raises RuntimeError: _description_
    :return: _description_
    :rtype: _type_
    """
    # Get a reference to an engine instance that will use the given driver
    # https://pyttsx3.readthedocs.io/en/stable/engine.html#the-engine-factory
    # initiate an instance of the pyttsx3 class
    # use defensive programming with try-except blocks
    try:
        engine = ts.init()
        # set the voice to USA Zira
        # https://pyttsx3.readthedocs.io/en/stable/engine.html#changing-voices
        voices = engine.getProperty("voices")    
        engine.setProperty("voice", voices[1].id)    
        return engine

    # Raise errors	
    # ImportError – When the requested driver is not found
    except ImportError as e:
        print(f"There was an error importing text-to-speech engine: {e}")
        raise ImportError("Check that pyttsx3 was installed & try again.")

    # RuntimeError – When the driver fails to initialise
    except RuntimeError as e:
        print(f"There was an error initiating text-to-speech engine: {e}")
        raise RuntimeError("There was a problem initiating pyttsx3.")

# create a  class) methods from the base class, StartEngine()
# the class contains the methods that welcome the user & introduce the program
class AssistantWelcome():
    # initialise AssistantWelcome() with ts engine
    def __init__(self, engine):
        self.engine = engine

    # create a method for the assistant to speak
    def assistant_speak(self, utterance):
        """A method for the assistant to speak.

        :param utterance: A sentence that the assistant will say.
        :type utterance: str
        """
        # Queue a command to speak an utterance
        self.engine.say(utterance)

        # pause program until spoken text is complete
        self.engine.runAndWait()

    # the assistant greets the user
    # https://pyttsx3.readthedocs.io/en/stable/engine.html#pyttsx3.engine.Engine.say
    # https://pyttsx3.readthedocs.io/en/stable/engine.html#speaking-text
    # https://pyttsx3.readthedocs.io/en/stable/engine.html#pyttsx3.engine.Engine.runAndWait
    def assistant_greeting(self):
        # print greeting
        print("Hello, I am Zira. I can assist you with a variety of tasks to the best of my ability.")
        # call assistant_speak() Queue a command to speak an utterance
        self.assistant_speak("Hello, I am Zira. I can assist you with a variety of tasks to the best of my ability.")
        # pause program until spoken text is complete
        ##engine.runAndWait()

    # tell the user the the date, time and weather where by the user
    def present_conditions(self):
        # get the current time
        # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        time = datetime.datetime.now().strftime("%I:%M%p")

        # get the day
        # https://docs.python.org/3/library/datetime.html#datetime.datetime.date
        day = datetime.date.today().strftime("%A")

        # get the date
        # https://docs.python.org/3/library/datetime.html#datetime.date.today
        date = datetime.date.today().strftime("%d")
        month = datetime.date.today().strftime("%B")

        # get the weather
        # https://openweathermap.org/api
        weather = "hot" ################################## incomplete

        # print the present conditions
        print(f"It is {time} on {day}, {date} of {month}. The weather is {weather}")
        # say the present conditions
        self.assistant_speak(f"It is {time} on {day}, {date} of {month}. The weather is {weather}")
        # pause program until spoken text is complete
        ##engine.runAndWait()

# ask the user for their name

# greet the user with their name by both speaking and writing it out 
# use hour to greet with either morning, afternoon or evening

## ask the user how they are doing ##

# ask the user what they would like to do

# ask the assistant what is the user's name

# code the various key words to listen for in a request

# search google for an answer 
# https://pypi.org/project/rpaframework/
# https://rpaframework.org/
# https://rpaframework.org/libraries/browser_playwright/
# use playwright to automate a search alternatively

# request a browser to be opened
# webbrowser.open
# https://docs.python.org/3.11/library/webbrowser.html
# https://www.askpython.com/python-modules/webbrowser-module

# open youtube to play a song

# say the date

# say the time

# say the weather

# open instagram

# open python IDE

# open VS code

# tell me a joke
# https://pypi.org/project/Joking/

# latest news in the last 24 hours
# https://newsapi.org/
# datetime.now()
# datetime.delta() https://www.geeksforgeeks.org/python-datetime-timedelta-class/

# listen for the user saying bye

#################################################################################################

# Main code
def main():
    engine = start_engine()
    # create an instance of AssistantWelcome
    assistant_welcome = AssistantWelcome(engine)

    # call AssistantWelcome methods
    assistant_welcome.assistant_greeting()
    assistant_welcome.present_conditions() 

#################################################################################################
# call the main function

# Create a custom voice assistant using Python to personalise and automate tasks according to your
# needs. Python's versatility makes it an excellent choice for scripting and development, allowing you to build a
# voice assistant that can compete with the likes of Siri, Alexa, and Google Assistant.
main()


