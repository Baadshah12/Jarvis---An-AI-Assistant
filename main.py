import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from googleapiclient.discovery import build
import wikipediaapi




wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent="JarvisBot/1.0 (https://example.com; contact@example.com)"
)

recognizer =sr.Recognizer()
engine=pyttsx3.init()

API_KEY = "AIzaSyBGL9ZjzQbuUOmDiMbzdLj0b5WlH-VdnEU"
NEWS_API_KEY = "c815fd5ffadd43368c39bebeb909dcfe"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"




def speak(text):
    engine.say(text)
    engine.runAndWait()


def search_youtube(query):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    try:
        # Make the search request
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=1  # Adjust as needed
        )
        response = request.execute()
        
        # Log the response for debugging
        print("YouTube API Response:", response)

        # Get the first video result
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            speak(f"Playing {response['items'][0]['snippet']['title']} on YouTube.")
            webbrowser.open(video_url)
        else:
            speak("Sorry, I couldn't find any videos.")
    except Exception as e:
        speak("Sorry, there was a problem searching YouTube.")
        print(f"Error occurred while searching YouTube: {e}")

def fetch_news():
    try:
        response = requests.get(NEWS_API_URL, params={'apiKey': NEWS_API_KEY, 'country': 'us'})
        news_data = response.json()
        if news_data['status'] == 'ok' and news_data['articles']:
            headlines = [article['title'] for article in news_data['articles'][:5]]  
            news_summary = "Here are the top headlines: " + ", ".join(headlines)
            speak(news_summary)
        else:
            speak("Sorry, I couldn't fetch the news.")
    except Exception as e:
        speak("Sorry, there was a problem fetching the news.")
        print(f"Error occurred while fetching news: {e}")

def fetch_wikipedia_summary(query):
    query = query.strip()

    # Fetch the Wikipedia page
    page = wiki.page(query)

    # Debug: Print the title and check if page exists
    print(f"Searching Wikipedia for: {page.title}")
    if page.exists():
        print(f"Page found: {page.title}")
        return page.summary[:500]  # Return first 500 characters of the summary
    else:
        print(f"Page not found for: {query}")
        return "Sorry, I couldn't find any information on that topic."


   
def processCommand(c):
  command = c.lower()
  if "open google" in c.lower():
    webbrowser.open("https://google.com")
  elif "open youtube" in c.lower():
    webbrowser.open("https://youtube.com")
  elif "open facebook" in c.lower():
    webbrowser.open("https://facebook.com")
  elif  "wanna play a game" in c.lower():
      speak("Sure, let me open Tic Tac Toe for you!")
      open_tic_tac_toe()
  elif "headlines" in command:
      speak("Fetching the latest news for you.")
      fetch_news()
  elif "tell me something about" in command:
      subject = command.replace("tell me something about", "").strip()
      response = fetch_wikipedia_summary(subject)
      speak(response)
  else:
     speak(f"Searching for {command} on YouTube.")
     search_youtube(command)
  
        

def open_tic_tac_toe():
    url = "http://localhost:5174"  # Your local ReactJS app URL
    webbrowser.open(url)
    speak("Here is the Tic Tac Toe game. Let's play!")

   
if __name__=="__main__":
  speak("Initializing Jarvis....")
  while True:
    r= sr.Recognizer()
    print("recognizing..")
    try:
      with sr.Microphone() as source:
        print("listening...")
        audio=r.listen(source,timeout=5,phrase_time_limit=3)
      word= r.recognize_google(audio)
      if(word.lower()== "hey buddy"):
        speak("hey abdul, how can i help you")
        with sr.Microphone() as source:
          print("jarvis active...")
          audio=r.listen(source)
          comand=r.recognize_google(audio)

          processCommand(comand)

    except Exception as e:
        print("Error;{0}".format(e))
 