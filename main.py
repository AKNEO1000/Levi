import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia


# Initialize the recognizer and the TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to make the assistant speak
def speak(audio):
    	
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[1].id) # 0 = male, 1 = female
	engine.say(audio) 
	engine.runAndWait()


# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
        except sr.RequestError:
            speak("There seems to be an issue with the speech recognition service.")
        except sr.WaitTimeoutError:
            speak("You didn't say anything.")
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
            elif "open" in command or "visit" in command:
                open_website(command)
            elif "wikipedia" in command:
                search_wikipedia(command)
            elif "exit" in command or "quit" in command:
                speak("Goodbye! Have a great day!")
                break
            else:
                speak("I'm not sure how to help with that. Please try again.")
        else:
            speak("Please say something.")

# Function to open a website
def open_website(command):
    websites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "github": "https://www.github.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
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
    ai_assistant()
