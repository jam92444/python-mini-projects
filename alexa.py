import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

# talking command
def take_command():
    command = ""  # Initialize command with an empty string to avoid UnboundLocalError
    try:
        with sr.Microphone() as source:
            print("listening.....")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')  # Fix here
                print(command)
    except sr.UnknownValueError:
        talk("Sorry, I did not catch that. Could you please repeat?")
    except sr.RequestError:
        talk("Sorry, I could not request results from Google. Please check your internet connection.")
    except Exception as e:
        talk(f"An error occurred: {str(e)}")
    return command

def run_alexa():
    command = take_command()
    print(command)
    
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    
    elif 'who is ' in command:
        person = command.replace('who is ', '')
        try:
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk(f"Could you be more specific? There are multiple results for {person}.")
        except wikipedia.exceptions.HTTPTimeoutError:
            talk("Sorry, I couldn't fetch the information due to a network issue.")
        except wikipedia.exceptions.PageError:
            talk(f"Sorry, I couldn't find any information on {person}.")
    
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    
    elif 'date' in command:
        talk("Sorry, I have a headache.")
    
    elif 'are you single' in command:
        talk("I am in a relationship with Wi-Fi.")
    
    else:
        try:
            talk("Searching for your query...")
            # Using Wikipedia to search for general questions
            answer = wikipedia.summary(command, sentences=2)
            print(answer)
            talk(answer)
        except wikipedia.exceptions.DisambiguationError:
            talk("Your question is too vague. Could you be more specific?")
        except wikipedia.exceptions.HTTPTimeoutError:
            talk("Sorry, I couldn't fetch the information due to a network issue.")
        except wikipedia.exceptions.PageError:
            talk("Sorry, I couldn't find the answer to that question.")
        except Exception as e:
            talk(f"I'm not sure about that. Let me check. Error: {str(e)}")

while True:
    run_alexa()
