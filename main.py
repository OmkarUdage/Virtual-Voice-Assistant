import speech_recognition as sr     # For speech-to-text
import webbrowser                   # To open websites
import pyttsx3                      # For text-to-speech
import musicLibrary                 # Your custom music library (contains song links)
import requests                     # To make HTTP requests (used for news fetching)
import cohere                       # Cohere AI API for AI responses
import logging                      # Logging module to log data to a file
import os
from dotenv import load_dotenv


load_dotenv()


# Logging setup to write to a file called nova_log.txt
logging.basicConfig(
    filename = "nova_log.txt",                    # The log file where messages will be saved
    level = logging.INFO,
    format = "%(asctime)s - USER: %(message)s",   # Format of each log entry: includes time and message
    datefmt = "%d-%m-%Y %H:%M:%S"
)


# Initialize recognizer
recognizer = sr.Recognizer()
newsapi = os.getenv("NEWS_API_KEY")    # Insert your actual News API key


# Function to speak the given text using pyttsx3
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)              # Speed of speech
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)    # Select a voice (0 = default male, 1 = female)
    engine.say(text)
    engine.runAndWait()


# Function to send user command to Cohere API and return the AI's response
def aiProcess(command):
    co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))   # Insert your actual Cohere API key

    response = co.chat(
    model = "command-a-03-2025", 
    messages=[
        {"role": "system", "content": "You are Nova, a skilled and helpful virtual voice assistant like Alexa or Siri."},
        {"role": "user", "content": command}
        ]
    )

    # Handle list content (If response content is a list, join all parts into one string)
    if isinstance(response.message.content, list):
        content = " ".join([part.text for part in response.message.content])
    else:
        content = response.message.content

    return content.strip()    # Return cleaned-up AI response without any leading and trailing whitespace (like spaces, tabs or newline characters) from a string


# Function to process user commands like opening websites, playing music or fetching news
def processCommand(c):
    # Open specific websites based on keywords in command (You can add your favourite or any other popular websites you use on daily bases)
    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open whatsapp" in c.lower():
        webbrowser.open("https://whatsapp.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif "open spotify" in c.lower():
        webbrowser.open("https://spotify.com")

    elif "open amazon" in c.lower():
        webbrowser.open("https://amazon.com")

    elif "open weather" in c.lower():
        webbrowser.open("https://weather.com")

    # Play a song from the musicLibrary based on command like "play [song]"
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]     # Extract song name
        link = musicLibrary.music[song]    # Get link from your library
        webbrowser.open(link)

    # Fetch and speak top 5 news headlines using NewsAPI
    elif "news" in c.lower():
        print("Fetching news...")
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}") # region set to 'us' as there were currently no news article found in 'in' region
        print("Status Code:", r.status_code)
        # print("Response JSON:", r.json()) # a structured data format that contains all the news information returned by the API.

        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if articles:
                for article in articles[:5]:  # Only speak first 5 to avoid overload.
                    print("Headline:", article['title'])
                    speak(article['title'])
            else:
                speak("No news articles found.")
        else:
            speak("Failed to fetch news.")

    # For any other command, use Cohere AI to generate a response
    else:
        output = aiProcess(c)

        # Logs both command and response
        logging.info(f"{c}")
        logging.info(f"NOVA: {output}")

        speak(output)



# Main program loop: listens for wake word "Nova" and responds to commands
if __name__ == "__main__":
    speak("Initializing Nova...")
    while True:
        # obtain audio from the microphone
        r = sr.Recognizer()
        
        print("recognizing...")
        try:
            # Listen for the wake word "Nova"
            with sr.Microphone() as source:
                print("Listening for wake word 'Nova'...")
                r.adjust_for_ambient_noise(source, duration=1)  # Adjusts for background noise to improve voice recognition accuracy
                audio = r.listen(source, timeout = 3, phrase_time_limit = 3)
            word = r.recognize_google(audio)    # Convert speech to text
            
            if(word.lower() == "nova"):
                print("Saying yes...")
                speak("Yes")
                print("Done speaking...")

                # Listen for user command after wake word
                with sr.Microphone() as source:
                    print("Nova Active... Listening for command...")
                    audio = r.listen(source, timeout=4, phrase_time_limit=4)
                    command = r.recognize_google(audio)

                    print(f"You said {command}")
                    processCommand(command)      # Process the spoken command

        except Exception as e:
            print(f"Error: {e}")       # Print any recognition/speech errors