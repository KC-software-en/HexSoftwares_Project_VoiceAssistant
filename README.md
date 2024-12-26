# Project name
Voice Assistant   

# Project description
Welcome to the Voice Assistant project! This application combines the power of speech recognition, text-to-speech, and web automation to create an engaging, interactive experience. Inspired by the idea of building my own version of J.A.R.V.I.S., I set out to tackle this new and exciting project, learning a lot along the way and having plenty of fun in the process.  

The voice assistant not only responds to spoken commands but also automates tasks like web searches, YouTube playback, and social media interactions. With carefully selected Python libraries and some creative programming, this project showcases the versatility of Python and my passion for building intuitive, user-friendly tools.  

This README will guide you through the features, setup, and development notes of the Voice Assistant application. Whether you're here for inspiration or looking to contribute, I hope you enjoy exploring this project as much as I enjoyed creating it! 


**Core Features**  
- **Text-to-Speech**: Converts text into speech using `pyttsx3`, with a custom USA Zira voice.  
- **Speech Recognition**: Listens to user input via microphone with `SpeechRecognition` and processes it for commands.  
- **Web Automation**: Automates web searches, Wikipedia lookups, and social media actions using `selenium` and an Edge driver.  
- **Entertainment Features**: Plays YouTube videos via a custom class and tells jokes with `Joking`.  
- **Dynamic Interactions**: Uses regex for personalized greetings and responds to keywords with a user-friendly menu loop.  

**Key Libraries and Tools**  
- **`pyttsx3`**: For robust text-to-speech functionality.  
- **`SpeechRecognition`** + **`PyAudio`**: For speech input (resolved dependency challenges with PyAudio installation).  
- **`selenium`**: To automate browser tasks like Google searches and Wikipedia lookups.  
- **`fontstyle`**: Adds visual flair to console output (e.g., colored error messages).  
- **`Joking`**: Fetches random dad jokes for lighthearted interactions.  

**Development Notes**  
- Created a `voice_assistant.py` script and managed dependencies in a virtual environment.  
- Key workflows include defensive programming for error handling and conditionals for task execution.  

# Installation section

Outline the steps necessary to build and run your application with venv:

1. Open the Command Prompt
1. Create a Virtual Environment:
    + in Command Prompt (powershell)
    + create a folder for new virtual env: mkdir Virtual_env
    + cd Virtual_env
    + create virtual env: virtualenv VoiceVenv
    + you will see Scripts in my_djanVoiceVenvgo
    + change to Command Prompt (admin) 
    
1. Activate the Virtual Environment:
    + On Windows (Command Prompt):
        + cd to path to Scripts "C:\path\to\Scripts"
        + activate.bat
   
1. Download Python to run the program @ https://www.python.org/downloads/
1. Run the Python Installer
1. Check the Box for "Add Python to PATH"
In cmd:
1. Verify pip installation: `pip --version`

1. Clone this repository
1. Install Packages:
    + pip install [package_name]
    
    OR
    + python -m pip install -r requirements.txt

# Usage section

In the Command Prompt:
+ cd to project root directory and run the command: python voice_assistant.py

# Credits
@KC-software-en

# Add a URL to your GitHub repository

https://github.com/KC-software-en/HexSoftwares_Project_VoiceAssistant