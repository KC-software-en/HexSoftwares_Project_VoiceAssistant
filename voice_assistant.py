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
    """Initialise an instance of the text-to-speech engine.

    :raises ImportError: An error when the requested driver is not found
    :raises RuntimeError: An error for when the driver fails to initialise
    :return: Return an instance of the text-to-speech engine
    :rtype: pyttsx3.Engine
    """
    # Get a reference to an engine instance that will use the given driver
    # https://pyttsx3.readthedocs.io/en/stable/engine.html#the-engine-factory
    # initiate an instance of the pyttsx3 class
    # use defensive programming with try-except blocks
    try:
        engine = ts.init()
        # slow down the rate of speech
        # https://pyttsx3.readthedocs.io/en/stable/engine.html#pyttsx3.engine.Engine.getProperty
        # https://pyttsx3.readthedocs.io/en/stable/engine.html#changing-speech-rate
        rate = engine.getProperty("rate") 
        #print(f"rate:{rate}")
        engine.setProperty("rate", 180)    
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
        """A method for the assistant ot greet the user.
        """
        # print greeting
        print("Hello, I am Zira. I can assist you with a variety of tasks to the best of my ability.")
        # call assistant_speak() to say the greeting
        self.assistant_speak("Hello, I am Zira. I can assist you with a variety of tasks to the best of my ability.")        

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
        # call assistant_speak to say the present conditions
        self.assistant_speak(f"It is {time} on {day}, {date} of {month}. The weather is {weather}")        

    # ask the user for their name
    def request_user_name(self):
        """A method where the assistant asks for the user's name.
        """
        print("What is your name?")
        self.assistant_speak("What is your name?")

    # greet the user with their name by both speaking and writing it out 
    # use hour to greet with either morning, afternoon or evening
    def greet_user(self):
        pass

    ## ask the user how they are doing ##

    # ask the user what they would like to do

class UserInput():
    # add assistant parameter to constructor
    def __init__(self, assistant):
        # create an instance of the recogniser class to retrieve information from microphone
        # https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py
        self.r = sr.Recognizer()
        # store the reference to AssistantWelcome() instance so that the speak method can be used later
        self.assistant = assistant

    def user_speak(self):
        """A method for the user to speak to the assistant

        :return: Return the text that Google thinks the user said.
        :rtype: str
        """
        # use a while loop that ends when Google understands the user's speech 

        while True:
            try: 
                with sr.Microphone() as source:                
                    # adjust for ambient noise
                    # https://github.com/Uberi/speech_recognition/blob/master/examples/calibrate_energy_threshold.py
                    print("Calibrating for background noises...")
                    self.r.adjust_for_ambient_noise(source, 1.5)
                    # listen for audio from the microphone & save it
                    print("Listening...")
                    self.audio = self.r.listen(source)
                    # send audio to Google API engine to convert it to text
                    # use defensive programming with try-except blocks to save audio
                    # https://github.com/Uberi/speech_recognition/blob/master/examples/audio_transcribe.py
                    self.text = self.r.recognize_google(self.audio)
                    #try:
                    print(f"Google thinks you said: \"{self.text}\"\n")
                    # return will break the loop
                    return self.text

            except sr.UnknownValueError as e:                
                print("Google Speech Recognition could not understand the audio for your name: {e}. Please try again.")
                # use the stored instance to call assistant_speak()
                self.assistant.assistant_speak("I did not hear you clearly. Please try again.\n")
                # continue loop to try again
                continue

            except sr.RequestError as e:
                print("Unable to request results from Google Speech Recognition service: {e}")
                # use the stored instance to call assistant_speak()
                self.assistant.assistant_speak(
                    "I am unable to connect to the Google Speech Recognition service. Please try again.\n")
                # continue loop to try again
                continue

            # continue the loop
            #except Exception as e:
             #   print(f"There was an error: {e}")
              #  continue

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
    # create an instance of AssistantWelcome()
    assistant_welcome = AssistantWelcome(engine)

    # create an instance of UserInput()
    # store AssistantWelcome() instance in UserInput() so the assistant can speak up for errors
    user_input = UserInput(assistant_welcome)

    # call AssistantWelcome() methods
    assistant_welcome.assistant_greeting()
    assistant_welcome.present_conditions() 
    assistant_welcome.request_user_name()
    # call UserInput() methods
    user_input.user_speak()

    

#################################################################################################
# call the main function

# Create a custom voice assistant using Python to personalise and automate tasks according to your
# needs. Python's versatility makes it an excellent choice for scripting and development, allowing you to build a
# voice assistant that can compete with the likes of Siri, Alexa, and Google Assistant.
main()


