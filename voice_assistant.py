# imports

# import pyttsx3 to convert text to speech
import pyttsx3 as ts

# import datetime to get the date, time
import datetime

# import speech_recognition so that Google API can process input to the microphone
# https://pypi.org/project/SpeechRecognition/
# https://www.geeksforgeeks.org/python-speech-recognition-module/
import speech_recognition as sr

# import fontstyle for italic suggestions & red errors
# https://www.geeksforgeeks.org/fontstyle-module-in-python/
import fontstyle

# import re to search for a pattern in a string
import re 

# import classes for automated web search
from auto_web_tasks import WikiBot

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
    # 
    def __init__(self, engine):
        self.engine = engine
        # place self as a parameter when calling an instance for the user_suggestion, UserInput needs access to AssistantWel
        self.suggestion_format = UserInput(self).user_suggestion

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
        print(f"It is {time} on {day}, {date} of {month}. The weather is {weather}\n")
        # call assistant_speak to say the present conditions
        self.assistant_speak(f"It is {time} on {day}, {date} of {month}. The weather is {weather}")        

    # ask the user for their name
    def request_user_name(self):
        """A method where the assistant asks for the user's name.
        """
        print("What is your name?")
        self.assistant_speak("What is your name?")
        # include a suggestion for the user because these word will be checked
        suggestion = "Suggestion: My name is ...\n"
        # call UserInput class's user_suggestion method to format output of suggestion
        # put self as the argument because UserInput expects the assistant parameter
        # - inside request_user_name, self refers to current AssitantWelcome instance that calls assistant_speak method
        user_input_suggestion = UserInput(self)
        user_input_suggestion.user_suggestion(suggestion)                

    # greet the user with their name by both speaking and printing it out     
    def greet_user(self, username_stripped):
        """A method to greet the user by their name.

        :param user_name: Input from the microphone for the user's name
        :type user_name: str
        """                
        # get the current time's hour
        time = datetime.datetime.now().hour #int
        # use the hour to greet with either morning, afternoon or evening
        if time < 12:
            print(f"Good morning {username_stripped}.")
            self.assistant_speak(f"Good morning {username_stripped}.")

        elif time == 12 or time < 18:
            print(f"Good afternoon {username_stripped}.")
            self.assistant_speak(f"Good afternoon {username_stripped}.")
        
        else:
            print(f"Good evening {username_stripped}.\n")
            self.assistant_speak(f"Good evening {username_stripped}.")    

    # ask the user what they would like to do
    def user_task_inquiry(self):
        """A method where the assistant asks the user what task they want to perform.

        :return: _description_
        :rtype: _type_
        """
        # print out suggested task requests
        suggestion = ("""Suggestions:
                      What is my name?
                      What is the weather?
                      Search Wikipedia for...
                      What are the latest news headlines?
                      Goodbye.
                    """)
        # call UserInput's suggestion method to format output of suggestions
        self.suggestion_format(suggestion) 
        # print the assistant's question
        self.assistant_speak("How can I assist you?")


# create a class for the user's input
class UserInput():
    # add assistant parameter to constructor
    def __init__(self, assistant):
        # create an instance of the recogniser class to retrieve information from microphone
        # https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py
        self.r = sr.Recognizer()
        # store the reference to AssistantWelcome() instance so that the speak method can be used later
        self.assistant = assistant

    # define a method for the user to speak to the assistant
    def user_speak(self):
        """A method for the user to speak to the assistant

        :return: Return the text that Google thinks the user said.
        :rtype: str
        """
        # use a while loop that ends when Google understands the user's speech 
        while True:
            try: 
                with sr.Microphone() as source:  
                    self.r.energy_threshold = 600  
                    # add a pause threshold - seconds of non-speaking audio before a phrase is considered complete
                    # https://github.com/Uberi/speech_recognition/blob/master/speech_recognition/__init__.py
                    self.r.pause_threshold = 2.5            
                    # adjust for ambient noise
                    # https://github.com/Uberi/speech_recognition/blob/master/examples/calibrate_energy_threshold.py
                    print("Calibrating for background noises...")
                    self.r.adjust_for_ambient_noise(source, 1.5)

                    # listen for audio from the microphone & save it
                    print("Listening...")
                    self.assistant.assistant_speak("I'm listening...")
                    self.audio = self.r.listen(source)
                    # send audio to Google API engine to convert it to text
                    # use defensive programming with try-except blocks to save audio
                    # https://github.com/Uberi/speech_recognition/blob/master/examples/audio_transcribe.py
                    self.text = self.r.recognize_google(self.audio)
                    # print out the text Google recognised
                    print(f"Google thinks you said: \"{self.text}\"\n\n")
                    # return will break the loop
                    return self.text

            except sr.UnknownValueError as e:   
                error_message = f"Google Speech Recognition could not understand the audio for your name: {e}. Please try again.\n"            
                # call method to print error message
                self.user_error(error_message)

                # use the stored instance to call assistant_speak()                
                self.assistant.assistant_speak("I did not hear you clearly. Please try again.")
                # continue loop to try again
                continue

            except sr.RequestError as e:
                error_message = f"Unable to request results from Google Speech Recognition service: {e}\n"
                # call method to print error message
                self.user_error(error_message)

                # use the stored instance to call assistant_speak()
                self.assistant.assistant_speak(
                    "I am unable to connect to the Google Speech Recognition service. Please try again.")
                # continue loop to try again
                continue            

    def user_suggestion(self, suggestion):
        # use fontstyle to format the suggestion in blue, italic
        # print the suggestion 
        print(fontstyle.apply(suggestion, 'Italic/cyan'))

    def user_error(self, error_message):        
        # use fontstyle to format the error in bold, red
        # print the error message
        print(fontstyle.apply(error_message, 'red/bold'))

    # ask the assistant what is the user's name
    def check_user_name(self, user_name):
        """A method to check that the user said the suggested input followed by their name.

        :param user_name: Name input received over the microphone, from the user.
        :type user_name: str
        """
        # replace suggested words separately in case the user repeates the phrase
        # split() the str at the whitespaces then join the str again - resolve extra spaces in output, in the middle of str        
        username_stripped = " ".join(user_name.replace("my", "").replace("name", "").replace("is", "").split())        
        
        while True:
            # check if the user said their name according to the suggestion
            # https://docs.python.org/3.11/library/re.html#re.search
            # use conditional statements to check for if "My name is" in user_name        
            # use regular expression to check for the pattern in the str
            # check if the stripped username is not empty
            if re.search("my name is", user_name) and username_stripped != "":
                # call method for assistant to give a custom welcome
                self.assistant.greet_user(username_stripped)
                # break the loop 
                return username_stripped

            # check if there is no name found after the suggested phrase "my name is"
            elif user_name == "my name is":
                self.user_error("The Google Speech Recognition service did not catch your name. Please try again")
                self.assistant.assistant_speak(
                    "Your name is not present in Google Speech Recognition service. Please try again.")
                # call request_user_name() again
                self.assistant.request_user_name()
                user_name = self.user_speak()
                # continue the loop
                continue
            
            # check if the pattern is not found, call request_user_name() again
            else:
                self.user_error("Please use the suggested phrase before saying your name.")
                self.assistant.assistant_speak("Please use the suggested phrase before saying you name.")
                self.assistant.request_user_name()
                user_name = self.user_speak()
                # continue the loop
                continue
            
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
    # greet user
    assistant_welcome.assistant_greeting()
    # inform user of present conditions
    assistant_welcome.present_conditions() 

    # request the user to input the name over the microphone
    assistant_welcome.request_user_name()
    # call UserInput() methods to save the audio as the user's name
    user_name = user_input.user_speak()

    # call method to check if the user said their name
    # return the name with the command removed
    user_name_isolated = user_input.check_user_name(user_name)
    
    while True:        
        # use defensive programming to check user request
        try:
            # call method to ask user how the assistant can help
            assistant_welcome.user_task_inquiry()
            # call the method so that the user can say the task they want to do
            # format user input processed by Google Speech Recognition in lowecase
            user_task_request = user_input.user_speak().lower()

            # check which task the user want then call its method
            if "wikipedia" in user_task_request:
                # call an instance of the WikiBot class
                wiki_info = WikiBot()                

                # extract term to be searched from user_task_request
                # remove "search wikipedia for" from the user_task_request input str
                # remove any extra whitespaces
                wiki_term = user_task_request.replace("search wikipedia for", "").strip()                

                # print out the voice assistant saying they will search wikipedia
                print(f"Searching Wikipedia for {wiki_term}...\n")
                # call method to say that the assistant will search wikipedia
                assistant_welcome.assistant_speak(f"Searching Wikipedia for {wiki_term}.")
                # call the wiki_search method
                wiki_info.wiki_search(wiki_term)                

            # if the user wants to end the voice assistant session
            elif "bye" in user_task_request:
                # print out the assistant saying goodbye
                print(f"Goodbye {user_name_isolated}")
                # call assistant_speak method to say bye
                assistant_welcome.assistant_speak(f"Goodbye {user_name_isolated}")
                break

            else:
                print("I did not catch that. Please try again.")
                assistant_welcome.assistant_speak("I did not catch that. Please try again.")
                continue

        # check that its the term the user wants to search
        except:
            print("There was an error.")
            assistant_welcome.assistant_speak("There was an error. Please try again.")
            

        finally:
            pass

    
        

    

#################################################################################################
# call the main function

# Create a custom voice assistant using Python to personalise and automate tasks according to your
# needs. Python's versatility makes it an excellent choice for scripting and development, allowing you to build a
# voice assistant that can compete with the likes of Siri, Alexa, and Google Assistant.
main()


