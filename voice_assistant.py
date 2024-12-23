# imports

# convert text to speech
import pyttsx3 as ts

# import datetime to get the date, time
import datetime

#################################################################################################
# Functions

# Get a reference to an engine instance that will use the given driver
# https://pyttsx3.readthedocs.io/en/stable/engine.html#the-engine-factory

# initiate an instance of the pyttsx3 class
# use defensive programming with try-except blocks
try:
    engine = ts.init()

# Raise errors	
# ImportError – When the requested driver is not found
except ImportError as e:
    print(f"There was an error importing text-to-speech engine: {e}")
    raise ImportError("Check that pyttsx3 was installed & try again.")

# RuntimeError – When the driver fails to initialise
except RuntimeError as e:
    print(f"There was an error initiating text-to-speech engine: {e}")
    raise RuntimeError("There was a problem initiating pyttsx3.")
  
# the assistant greets the user
# https://pyttsx3.readthedocs.io/en/stable/engine.html#pyttsx3.engine.Engine.say
# https://pyttsx3.readthedocs.io/en/stable/engine.html#speaking-text
# https://pyttsx3.readthedocs.io/en/stable/engine.html#pyttsx3.engine.Engine.runAndWait
def assistant_greeting():
    # print greeting
    print("Hello, I am Cal. I can assist you with a variety of tasks to the best of my ability.")
    # Queue a command to speak an utterance
    engine.say("Hello, I am Cal. I can assist you with a variety of tasks to the best of my ability.")
    # pause program until spoken text is complete
    engine.runAndWait()

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
    # start_ts_engine()
    assistant_greeting()

#################################################################################################
# call the main function

# Create a custom voice assistant using Python to personalise and automate tasks according to your
# needs. Python's versatility makes it an excellent choice for scripting and development, allowing you to build a
# voice assistant that can compete with the likes of Siri, Alexa, and Google Assistant.
main()


