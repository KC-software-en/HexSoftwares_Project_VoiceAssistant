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

# import classes for automated web search with Selenium
from auto_web_tasks import *

# import webbrowser to open web pages
import webbrowser

# import Joking
import Joking

# import WeatherApiCalls and NewsApiCalls classes
from api_calls import *

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
        engine.setProperty("rate", 180)    
        # set the voice to USA Zira
        # https://pyttsx3.readthedocs.io/en/stable/engine.html#changing-voices
        voices = engine.getProperty("voices")    
        engine.setProperty("voice", voices[1].id)    
        # return engine
        return engine

    # Raise errors	    
    # ImportError – When the requested driver is not found
    except ImportError as e:
        # print error
        print(f"There was an error importing text-to-speech engine: {e}")
        raise ImportError("Check that pyttsx3 was installed & try again.")

    # Raise RuntimeError – When the driver fails to initialise
    except RuntimeError as e:
        # print error
        print(f"There was an error initiating text-to-speech engine: {e}")
        raise RuntimeError("There was a problem initiating pyttsx3.")

# create class methods from the base class, StartEngine()
# the class contains the methods that welcome the user & introduce the program
class AssistantWelcome(CurrentConditions):    
    def __init__(self, engine):
        # return a tempory object of the parent class so that its methods can be called
        super().__init__()
        # initialise AssistantWelcome() with ts engine    
        self.engine = engine
        # place self as a parameter when calling an instance for the user_suggestion, 
        # UserInput needs access to AssistantWelcome
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
        print("Hello, I am Zira. I can assist you with a variety of tasks to the best of my ability.\n")
        # call assistant_speak() to say the greeting
        self.assistant_speak("Hello, I am Zira. I can assist you with a variety of tasks to the best of my ability.")        

    # tell the user the the date & time 
    def present_conditions(self):
        """A method to collect the day, date & time. 
        """
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

        # call inherited class' methods to retrieve the current weather in cape town
        current_temperature = super().temperature()
        weather_description = super().weather_description()

        # print the present conditions        
        print(f"""
              It is {time} on {day}, {date} of {month}. 
              The current weather in Cape Town is {current_temperature} degrees Celsius with a {weather_description}.\n
              """)
        # call assistant_speak to say the present conditions
        self.assistant_speak(f"""
                             It is {time} on {day}, {date} of {month}. 
                             The current weather in Cape Town is {current_temperature} degrees Celsius with a {weather_description}.
                             """)        

    # ask the user for their name
    def request_user_name(self):
        """A method where the assistant asks for the user's name.
        """
        # print the assistant's request for the user's name.
        print("What is your name?")
        # call the assistant_speak method for the assistant to ask the user's name.
        self.assistant_speak("What is your name?")
        # include a suggestion for the user because these words will be checked
        suggestion = "Suggestion: My name is ...\n"

        # create an instance of UserInput
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
        # if morning
        if time < 12:
            print(f"Good morning {username_stripped}.")
            self.assistant_speak(f"Good morning {username_stripped}.")

        # if afternoon
        elif time == 12 or time < 18:
            print(f"Good afternoon {username_stripped}.")
            self.assistant_speak(f"Good afternoon {username_stripped}.")
        
        # if evening
        else:
            print(f"Good evening {username_stripped}.\n")
            self.assistant_speak(f"Good evening {username_stripped}.")    

    # ask the user what they would like to do
    def user_task_inquiry(self):
        """ A method where the assistant asks the user what task they want to perform.
        """
        # print out suggested task requests
        suggestion = ("""Suggestions:                                            
                      Search Wikipedia for...
                      Open Instagram.
                      Open Google.
                      Play...
                      Tell me a dad joke.     
                      What is the weather?                 
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
        """A method for the user to speak to the assistant.

        :return: Return the text that Google thinks the user said.
        :rtype: str
        """
        # use a while loop that ends when Google understands the user's speech 
        while True:
            # use defensive programming with try-except blocks
            try: 
                # initialise the microphone as the audio source
                with sr.Microphone() as source:  
                    # set the energy threshold for a quiet environment (set high e.g. 3000 for noisy)
                    self.r.energy_threshold = 1000  
                    # add a pause threshold - seconds of non-speaking audio before a phrase is considered complete
                    # https://github.com/Uberi/speech_recognition/blob/master/speech_recognition/__init__.py
                    self.r.pause_threshold = 2.5            
                    # adjust for ambient noise 
                    # print to let user know about ambient noise calibration
                    # https://github.com/Uberi/speech_recognition/blob/master/examples/calibrate_energy_threshold.py
                    print("Calibrating for background noises...")
                    self.r.adjust_for_ambient_noise(source, 1.5)

                    # print to let user know the assistant is listening
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

            # except UnknownValueError then continue the loop
            except sr.UnknownValueError as e:   
                error_message = f"Google Speech Recognition could not understand your audio over the microphone: {e}. Please try again.\n"            
                # call method to print error message
                self.user_error(error_message)

                # use the stored instance to call assistant_speak()                
                self.assistant.assistant_speak("I did not hear you clearly. Please try again.")
                # continue loop to try again
                continue

            # except sr.RequestError then continue the loop
            except sr.RequestError as e:
                error_message = f"Unable to request results from Google Speech Recognition service: {e}\n"
                # call method to print error message
                self.user_error(error_message)

                # use the stored instance to call assistant_speak()
                self.assistant.assistant_speak(
                    "I am unable to connect to the Google Speech Recognition service. Please try again.")
                # continue loop to try again
                continue            

    # define a method to format the suggestion for the user
    def user_suggestion(self, suggestion):
        """A method to format the suggestion for the user.

        :param suggestion: A phrase the assistent listens for to perform a command.
        :type suggestion: str
        """
        # use fontstyle to format the suggestion in blue, italic
        # print the suggestion 
        print(fontstyle.apply(suggestion, 'Italic/cyan'))

    # define a method to format the error for the user
    def user_error(self, error_message):   
        """A method to format the error for the user.
        """         
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
        
        # use a loop to ensure to username was received
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
                # call method to format error message
                self.user_error("The Google Speech Recognition service did not catch your name. Please try again")
                # call assistant_speak method to let the assistant say the error
                self.assistant.assistant_speak(
                    "Your name is not present in Google Speech Recognition service. Please try again.")
                
                # call request_user_name() again
                self.assistant.request_user_name()
                # call method to let the user speak again
                user_name = self.user_speak()
                # continue the loop
                continue
            
            # check if the pattern is not found, call request_user_name() again
            else:
                # call method to format error message
                self.user_error("Please use the suggested phrase before saying your name.")
                # call assistant_speak method to let the assistant say the error
                self.assistant.assistant_speak("Please use the suggested phrase before saying you name.")
                
                # call request_user_name() again
                self.assistant.request_user_name()
                user_name = self.user_speak()
                # continue the loop
                continue
            
# create a class for the user menu of suggested tasks the voice assistant can perform
class UserMenu():
    def __init__(self, user_input):
        self.user_input = user_input        

    # open google     
    def open_google(self):
        """A method to open Google in a browser.
        """
        # set the url
        url = 'https://www.google.com/'
        # call method to open browser with a url argument
        self.open_browser(url)

    # request a browser to be opened
    # use webbrowser
    # https://docs.python.org/3.11/library/webbrowser.html
    # https://www.askpython.com/python-modules/webbrowser-module
    def open_browser(self, url):
        """A method that opens a specific URL in a browser.

        :param url: The URL of the user's choosing.
        :type url: str
        """
        # call method to open browser with webbrowser
        webbrowser.open(url)

    # open youtube to play a song with selenium
    # use imported method from auto_web_tasks.py
    def open_youtube(self, query):
        """A method open youtube & play a video.

        :param query: The search term for the YouTube search results.
        :type query: str
        """
        # create an instance of YouTubeVideo class
        youtube = YouTubeVideo()
        # call the method to play a video
        youtube.play_video(query)    

    # open instagram
    def open_instagram(self):
        """A method to open instagram in a browser.
        """
        # assign the url
        # call the function to open instagram in a browser with the url as the arg
        url = 'https://www.instagram.com/'
        self.open_browser(url)    

    # tell me a dad joke
    # https://pypi.org/project/Joking/
    def dad_joke(self):
        """A method to fetch a random dad joke.

        :return: Return a random dad joke.
        :rtype: str
        """
        # call Joking class' method for random dad jokes
        dad_joke = Joking.random_dad_joke()
        # return the joke
        return dad_joke 
                    
#################################################################################################

# Main code
def main():
    """The main function to run the voice assistant.
    """
    # create an instance of start_engine
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
    
    # create an instance of UserMenu
    user_menu = UserMenu(user_input)

    # create an instance of CurrentConditions class 
    # - (no need to create an instance of WeatherApiCalls because its methods are inherited)
    # do not pass the weather instance as the argument because it is already inherited & initialised with super()
    # -fixes TypeError: CurrentConditions.__init__() takes 1 positional argument but 2 were given
    current_weather = CurrentConditions()

    # instruct the user on how to use the voice assistant
    print("Select an option from the following suggestions or exit the menu with a 'Goodbye'\n")
    assistant_welcome.assistant_speak("Select an option from the following suggestions or exit the menu with a 'Goodbye'.")

    # use a loop to use the menu until the user says goodbye to exit the voice assistant
    while True:        
        # use defensive programming to check user request
        try:
            # call method to ask user how the assistant can help
            assistant_welcome.user_task_inquiry()
            # call the method so that the user can say the task they want to do
            # format user input processed by Google Speech Recognition in lowercase
            user_task_request = (user_input.user_speak()).lower()
            
            # check which task the user wants with the various keywords to listen for in a request
            # then call its relevant method
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
                first_paragraph = wiki_info.wiki_search(wiki_term)       
                # print the first_paragraph of the wiki search result         
                print(f"{first_paragraph}\n")
                # call the assistant_speak so say the first_paragraph of the wiki search result
                assistant_welcome.assistant_speak(f"{first_paragraph}")

            # if the user wants to open instagram
            elif "open instagram" in user_task_request:
                # print out voice assistant opening insta
                print("Opening Instagram...\n")
                # call the assistant_speak to say Instagram is opening
                assistant_welcome.assistant_speak("Opening Instagram")
                # call method to open instagram
                user_menu.open_instagram()

            # if the user wants to play a video in Youtube
            elif "play" in user_task_request:
                # extract term to be searched from user_task_request
                # remove "search wikipedia for" from the user_task_request input str
                # remove any extra whitespaces
                youtube_term = user_task_request.replace("play", "").strip()

                # print out voice assistant opening insta
                print("Opening YouTube...\n")
                # call the assistant_speak to say YouTube is opening
                assistant_welcome.assistant_speak("Opening YouTube")

                # call the method to open youtube & play the video
                user_menu.open_youtube(youtube_term)

            # if the user wants to open Google
            elif "open google" in user_task_request:
                # print out voice assistant opening Google
                print("Opening Google...\n")
                # call the assistant_speak to say YouTube is opening
                assistant_welcome.assistant_speak("Opening Google")

                # call the method to open google browser
                user_menu.open_google()

            # if the user wants a dad joke
            elif "dad joke" in user_task_request:
                # call the method for dad jokes
                dad_joke = user_menu.dad_joke()
                # print out the joke
                print(f"Here's a dad joke:\n{dad_joke}\n")
                # call method so that the assistant can say the joke
                assistant_welcome.assistant_speak(f"Here's a dad joke: {dad_joke}")

            # if the user asks for the weather
            elif "weather" in user_task_request:                
                # call method to retrieve the current weather in cape town
                current_temperature = current_weather.temperature()
                weather_description = current_weather.weather_description()
                # print out the assistant saying the weather
                print(f"The current weather in Cape Town is {current_temperature} degrees Celsius with a {weather_description}.\n")
                # call method so that the assistant can say the weather
                assistant_welcome.assistant_speak(f"The current weather in Cape Town is {current_temperature} degrees Celsius with a {weather_description}.")

            # if the user wants to read the latest news
            elif "news" in user_task_request:
                # create an instance of NewsApiCalls
                news = NewsApiCalls()
                # call news api method   
                news.call_news_api()     
                # if news.store_json_response() returns self.sa_json_response then call sa_articles method
                # in other words it doesn't return None for an error or the tuple str, dict for USA

                news_outcome = news.store_json_response()
                if news_outcome != None and news_outcome.get("totalResults", 0) != 0:
                    news.sa_articles()
                else:                
                    news.usa_articles()

            # if the user wants to end the voice assistant session
            elif "bye" in user_task_request:
                # print out the assistant saying goodbye
                print(f"Goodbye {user_name_isolated}\n")
                # call assistant_speak method to say bye
                assistant_welcome.assistant_speak(f"Goodbye {user_name_isolated}!")

                # print a closing statement upon exit
                print("Thank you for using the voice assistant!\n")
                
                # break the loop to end the program
                break

            # if the voice assistant did not recognise a request
            else:
                print("I did not catch that. Please try again.")
                assistant_welcome.assistant_speak("I did not catch that. Please try again.")
                continue

        # check that its the term the user wants to search
        except Exception as e:
            print(f"There was an error {e}. Please try again.\n")
            assistant_welcome.assistant_speak("There was an error. Please try again.")                    
    

#################################################################################################
# call the main function

# Create a custom voice assistant using Python to personalise and automate tasks according to your
# needs. Python's versatility makes it an excellent choice for scripting and development, allowing you to build a
# voice assistant that can compete with the likes of Siri, Alexa, and Google Assistant.
main()


