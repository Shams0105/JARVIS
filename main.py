#used speech recognition code from github : https://github.com/uberi/speech_recognition/blob/master/examples/microphone_recognition.py

import webbrowser #to open the web

import speech_recognition as sr

#Install pyttsx3 fo text to speech conversion (user text -> computer's speech)
#import pyttsx3 #removed this

import win32com.client #used this from gpt cuz pyttsx was only responding once not after tht

import musicLibrary #to play songs in this file

import requests # to get apis

#we need a recognizer to recognize the voice 
recognizer = sr.Recognizer()


#Set the news api key -> go to newsapi get ur api key from there
newsapi = 'd05f345fec4844e0a8c29c7a8ae2a670'

speaker = win32com.client.Dispatch("SAPI.SpVoice") #Powershell's native speech engine

def speak(text):
    print(f"[JARVIS]: {text}")
    speaker.Speak(str(text))
    


def processCommand(c):  #To process the cmnd ahead & excute the required task IMP

    if "open google" in c.lower():
        speak("opening google.")
        webbrowser.open("https://google.com")
        

    elif "open instagram" in c.lower():
        speak("opening istagram.")
        webbrowser.open("https://instagram.com")
        

    elif "open facebook" in c.lower():
        speak("opening facebook.")
        webbrowser.open("https://facebook.com")
        

    elif "open whatsapp" in c.lower():
        speak("opening whatsapp.")
        webbrowser.open("https://whatsapp.com")
        

    elif "open chatgpt" in c.lower():
        speak("opening chatgpt.")
        webbrowser.open("https://chatgpt.com")
        

    elif c.lower().startswith("play"):
        speak("playing")
        song = c.lower().split(" ")[1] #Ex play skyfall-> ["play" , "skyfall"] -> 1 = skyfall name in musicLibrary.py
        link = musicLibrary.music[song]  #Since in musicLibrary we've music named dict so to search tht
        webbrowser.open(link)

    #For news ,odule
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
    


if __name__ == "__main__":
    speak("Initializing Jarvis...")


    while True:
       
        
        r = sr.Recognizer()
        #Listen Wake word = Jarvis            
        # recognize speech using Sphinx use -> pip install pocketsphinx 
        #Needed to download PocketSphinx 5.0.3 cp312 win_amd64. cuz i dont have cpp compiler
        #Note : r.recognize_sphinx(audio) was deleted later as it cannot grasp aduio efficiently as google
        
        print('Recognizing')

        try:
            # obtain audio from the microphone
            #LISTEN TO THE WAKE WORD ie "JARVIS"

            with sr.Microphone() as source:
                print("Listening for the wake word!")
                r.adjust_for_ambient_noise(source, duration=0.5) # Reduces microphone background static
                audio = r.listen(source,timeout=5,phrase_time_limit=13)
                #imp note abt timeout & timelimit in -> learnings.txt
                
            word = r.recognize_google(audio)  #at start listen for 1 word ie jarvis(wake word)
            print(f'Heard : {word}')


            if word.lower() == 'jarvis':  #If user says Jarvis he shld reply 
                speak("Yes")  #function using pyttsx to convert speech to text

            #Listen what is user's command next must be inside if condition
                with sr.Microphone() as source:
                    speak("Jarvis activated..., give the command!")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source, timeout=10, phrase_time_limit=16)
                    command = r.recognize_google(audio)

                processCommand(command) 
                print(f"you siad , {command}")


        except sr.WaitTimeoutError:
            # Prevents the terminal from crashing if no one speaks within the timeout window
            pass
        except sr.UnknownValueError:
            print("could not understand audio")
        except sr.RequestError as e:
            print("error; {0}".format(e))



