import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import pyaudio
import random
# Initialize the recognizer and the TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# List to store tasks
tasks = []
# List to store jokes:
jokes = ["why was the broom late for work? It over-swept.", 
         "why did the frog take the bus to work? because it's car got toad.", 
         "What kind of bugs tell the time? A clock roach.",
         "Why didn't scientists trust the atoms? because they made everything up.",
         "why did math look sad? its because it had too many problems.",
         "Why don't skeletons fight eachother? because they don't have the guts."]
# Function to make the assistant speak
def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # 0 = male, 1 = female
    engine.say(audio)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")

        # Adjusting for ambient noise with a longer duration (to give time for ambient noise adjustment)
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Ambient noise adjustment complete.")
        
        try:
            # Listen for audio input with a longer timeout (giving the user more time to speak)
            audio = recognizer.listen(source, timeout=10)
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Speech not recognized.")
            speak("Sorry, I didn't catch that. Could you repeat?")
        except sr.RequestError:
            print("Error with speech recognition service.")
            speak("There seems to be an issue with the speech recognition service.")
        except sr.WaitTimeoutError:
            print("Wait Timeout. No speech detected.")
            speak("You didn't say anything.")
        except Exception as e:
            print(f"An error occurred: {e}")
            speak("An unexpected error occurred. Please try again.")
        return None

# Main function for the assistant
def ai_assistant():
    speak("Hello! My name is Levi. How can I assist you today?")
    
    while True:
        command = recognize_speech()
        if command:
            if "time" in command:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"The current time is {current_time}")
            elif "joke" in command:
                tell_jokes()
            elif "are" in command:
                who()
            elif "created" in command:
                creator()
            elif "open" in command or "visit" in command:
                open_website(command)
            elif "wikipedia" in command:
                search_wikipedia(command)
            elif "add task" in command:
                add_task()
            elif "view tasks" in command:
                view_tasks()
            elif "remove task" in command:
                remove_task()
            elif "exit" in command or "quit" in command or "bye" in command:
                speak("Goodbye! Have a great day!")
                break
            else:
                speak("I'm not sure how to help with that. Please try again.")
        else:
            speak("Please say something.")

# Function for whoami:
def who():
    speak('I am Levi, your personal desktop assistant.')
    
# Function for jokes:
def tell_jokes():
    joke = random.choice(jokes)
    print(joke)
#Function for creators:
def creator():
    speak('I was created by my masters, Arsh Kumar and Avi Kapoor.')

# Function to add a task to the to-do list
def add_task():
    speak("What task would you like to add to your to-do list?")
    task = recognize_speech()
    if task:
        tasks.append(task)
        speak(f"Task added: {task}")
    else:
        speak("I didn't catch that. Please try again.")

# Function to view all tasks in the to-do list
def view_tasks():
    if tasks:
        speak("Here are your tasks:")
        for index, task in enumerate(tasks, start=1):
            speak(f"{index}. {task}")
    else:
        speak("Your to-do list is empty.")

# Function to remove a task from the to-do list
def remove_task():
    speak("Which task number would you like to remove?")
    task_number = recognize_speech()
    try:
        task_number = int(task_number)
        if 1 <= task_number <= len(tasks):
            removed_task = tasks.pop(task_number - 1)
            speak(f"Task removed: {removed_task}")
        else:
            speak("That's not a valid task number.")
    except ValueError:
        speak("Please say a valid number.")

# Function to open a website
def open_website(command):
    websites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "github": "https://www.github.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        'discord' : 'https://discord.com',
        'instagram' : 'https://instagram.com',
        'wikipedia' : 'https://wikipedia.com',
        'reddit' : 'https://reddit.com',
        'whatsapp' : 'https://web.whatsapp.com'
    }
    found = False
    for keyword, url in websites.items():
        if keyword in command:
            speak(f"Opening {keyword}")
            webbrowser.open(url)
            found = True
            break
    if not found:
        speak("I couldn't recognize the website. Please try again.")

# Function to search Wikipedia
def search_wikipedia(command):
    try:
        speak("What should I search for on Wikipedia?")
        topic = recognize_speech()
        if topic:
            speak(f"Searching Wikipedia for {topic}")
            summary = wikipedia.summary(topic, sentences=2)
            speak("Here is what I found:")
            speak(summary)
        else:
            speak("I couldn't hear a topic. Please try again.")
    except wikipedia.DisambiguationError as e:
        speak("The topic is ambiguous. Please be more specific.")
    except wikipedia.PageError:
        speak("I couldn't find a Wikipedia page for that topic.")
    except Exception as e:
        speak("There was an error accessing Wikipedia.")

# Run the assistant
if __name__ == "__main__":
    # Check if the microphone is available
    if sr.Microphone.list_microphone_names():
        print("Microphone is available!")
        ai_assistant()
    else:
        print("No microphone detected.")
