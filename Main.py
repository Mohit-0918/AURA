import speech_recognition  as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import time
import subprocess
import ecapture as ec
import wolframalpha
import json
import requests
from TestEmotionDetector import test_Detector
from keras.models import model_from_json




#Setting up the speech engine
engine=pyttsx3.init()
voices=engine.getProperty('voices')
rate=engine.getProperty('rate')
fvoice=voices[0]
engine.setProperty('voice','fvoice')
engine.setProperty('rate','20')

def speak(text):
    engine.say(text)
    engine.runAndWait()

#Greeting function
def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello,Good Morning Sir")
        print("Hello,Good Morning Sir")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon Sir")
        print("Hello,Good Afternoon Sir")
    else:
        speak("Hello,Good Evening Sir")
        print("Hello,Good Evening Sir")

#Command Function
def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening....")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='en-in')
            print(f"user said:{statement}\n")
        
        except Exception as e:
            speak("Pardon me, Please say that again")
            return "None"
        return statement
wishMe()
time.sleep(1)
print("Loading your AI personal assistant Aura")
speak("I am loading things up,in a second.")
time.sleep(1)

def get_weather():
            api_key = "a60aafc58132acf984f32f02c27f198f"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"



#Main Function
if __name__=='__main__':
    # load json and create model
    json_file = open('model/emotion_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    emotion_model = model_from_json(loaded_model_json)

        # load weights into new model
    emotion_model.load_weights("model/emotion_model.h5")
    print("Loaded model from disk")
        # Define the emotion_labels list
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

        # Call the test_detector function to get the predicted emotion label
    predicted_emotion = test_Detector(emotion_model, emotion_labels)
    if predicted_emotion == 'Angry':
        speak("You seem a little annoyed heres something for you to cheer you up")
        response = requests.get("http://api.quotable.io/random")
        data = response.json()
        quote=data['content']
        speak(quote)

    if predicted_emotion == 'Disgust':
        speak("You seem a little disturbued is there anything i can do for you")
        speak("Well i think you should listen to this quote from quotable, this might help you")
        response = requests.get("http://api.quotable.io/random")
        data = response.json()
        quote=data['content']
        speak(quote)
    
    if predicted_emotion == 'Fear':
        speak("you seem to be traumatised of something! do you want me to take care of something?")
        speak("heres something for you")
        response = requests.get("http://api.quotable.io/random")
        data = response.json()
        quote=data['content']
        speak(quote)
    
    if predicted_emotion == 'Happy':
        speak("Ahh! you seem to be in a jolly mood,i too have something special for you loading up in a moment")
        response = requests.get("http://api.quotable.io/random")
        data = response.json()
        quote=data['content']
        speak(quote)
    
    if predicted_emotion == 'Sad':
        speak("You see a little depressed tell me how may i assist you")
        response = requests.get("http://api.quotable.io/random")
        data = response.json()
        quote=data['content']
        speak(quote)
    
    if predicted_emotion == 'Surprise':
        speak("you are baffeled by something, may i know why?")
        response = requests.get("http://api.quotable.io/random")
        data = response.json()
        quote=data['content']
        speak(quote)
    
    if predicted_emotion == 'Neutral':
        speak("i think you should express yourself openly anyway i have something for you")
        response = requests.get("http://api.quotable.io/random")
        data = response.json()
        quote=data['content']
        speak(quote)
    while True:
        statement = takecommand().lower()
        if statement==0:
            continue
        if "goodbye" in statement or "okbye" in statement or "stop" in statement or "thankyou" in statement:
            speak('your personal assistant Aura is shutting down,  Good bye')
            print('your personal assistant Aura is shutting down,  Good bye')
            break
        
        #all sets of skills
        #if 'tell me a joke' or 'jokes' in statement:
        #  speak(pyjokes.get_jokes())

        elif 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement =statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is open now")
            time.sleep(5)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now")
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now")
            time.sleep(5)
        elif "weather" in statement:
            api_key = "a60aafc58132acf984f32f02c27f198f"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"

            speak("What's the city name?")
            city_name = takecommand()

            complete_url = base_url + "appid=" + api_key + "&q=" + city_name

            try:
                response = requests.get(complete_url)
                response.raise_for_status()

                x = response.json()
                if x["cod"] != "404":
                    y = x["main"]
                    current_temperature = y["temp"]
                    current_humidity = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]

                    speak(" Temperature in kelvin unit is " +
                        str(current_temperature) +
                        "\n humidity in percentage is " +
                        str(current_humidity) +
                        "\n description  " +
                        str(weather_description))

                    print(" Temperature in kelvin unit = " +
                        str(current_temperature) +
                        "\n humidity (in percentage) = " +
                        str(current_humidity) +
                        "\n description = " +
                        str(weather_description))

            except requests.exceptions.HTTPError as e:
                if response.status_code == 404:
                    speak("Sorry, I could not find the city you specified. Can you please repeat the city name?")
                    get_weather()
                else:
                    speak("Sorry, I am unable to fetch the weather details at this moment. Please try again later.")

        elif 'time' in statement:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am Aura version 1 point O your persoanl assistant. I am programmed to make developers life easy'
                  'opening youtube,google chrome,gmail and stackoverflow ,predict time,take a photo,search wikipedia,predict weather' 
                  'in different cities , get top headline news from times of india and you can ask me computational or geographical questions too!')


        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was built by a group of developers namely Garima Kashish Karan and Mohit")

        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is stackoverflow")
            time.sleep(6)

        elif 'news' in statement:
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India,Happy reading')
            time.sleep(6)

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0,"robo camera","img.jpg")

        elif 'search'  in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'ask' in statement:
            speak('I can answer to computational and geographical questions and what question do you want to ask now')
            question=takecommand()
            app_id="E6TJRP-T35PAJT46Q"
            client = wolframalpha.Client('E6TJRP-T35PAJT46Q')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)


        elif "log off" in statement or "sign out" in statement:
            speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

time.sleep(3)

        