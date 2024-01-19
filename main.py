from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtGui import QMovie
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from playsound import playsound
import pyttsx3
import speech_recognition as sr
import os
import time
import webbrowser
import datetime
import wikipedia
import smtplib
from gtts import gTTS
import random
import bs4 as bs
import urllib.request
import playsound
from time import ctime

flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
voice_data =''
label= None
r = random.randint(1,20000000)
def record_audio(ask=""):
    with sr.Microphone() as source: # microphone as source
        if ask:
            speak(ask)
        audio = r.listen(source, 5, 5)  # listen for the audio via source
        print("Done Listening")
        global voice_data
        voice_data = ''
        
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError: # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down') # error: recognizer is not connected
        print(">>", voice_data.lower()) # print what user said
        return voice_data.lower()


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate',170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour <12:
        speak("Good morning,Have a good day")
    elif hour>=12 and hour<18:
        speak("Good Afternoon,Have a good day")
    else:
        speak("Good Evening, Great to see you")

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

class mainT(QThread):
    message_received = QtCore.pyqtSignal(str)
    def __init__(self):
        super(mainT,self).__init__()
    
    def run(self):
        self.assistant()()
    
    def STT(self):
        R = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listning...........")
            audio = R.listen(source)
        try:
            print("Recog......")
            text = R.recognize_google(audio,language='en-in')
            print(">> ",text)
            self.message_received.emit(text)
        except Exception:
            speak("Sorry , I could not recognize,please try again")
            return "None"
        text = text.lower()
        return text

    def assistant(self):
        wish()
        while True:
            
            self.query = self.STT()
            if 'good bye , exit , terminate ' in self.query:
                speak("Goodbye, See you soon")
                exit()
            elif 'open google' in self.query:
                webbrowser.open('www.google.co.in')
                speak("opening google")

            elif 'open youtube' in self.query:
                speak ("Opening Youtube")
                webbrowser.open("www.youtube.com")
            
  
            
            elif 'play music' in self.query:
               music_dir = 'D:\\songs'
               songs = os.listdir(music_dir)
               print(songs)    
               os.startfile(os.path.join(music_dir, songs[0]))

            elif 'time' in self.query:
               strTime = datetime.datetime.now().strftime("%H:%M:%S")    
               speak(f"Sir, the time is {strTime}")

            
            elif 'wikipedia' in self.query:
               speak('Searching Wikipedia...')
               self.query = self.query.replace("wikipedia", "")
               results = wikipedia.summary(self.query, sentences=2)# this will no. of sentences
               speak("According to Wikipedia")
               print(results)
               speak(results)


            elif 'open code' in self.query:
              codePath = "C:\\Users\\amamo\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
              speak ('Opening Visual Studio Code')
              os.startfile(codePath)
               

            elif "search for" in self.query and not "youtube "in self.query:
                search_term = voice_data.split("for")[-1]
                url = "https://google.com/search?q=" + search_term
                webbrowser.get().open(url)
                speak("Here is what I found for" + search_term + "on google")


            elif "amazon"in self.query:
                  search_term = voice_data.split("for")[-1]
                  url="https://www.amazon.in"+search_term
                  webbrowser.get().open(url)
                  speak("here is what i found for"+search_term + "on amazon.com")
            

            elif 'play music' in self.query:
                music_dir = 'D:\\songs'
        
                songs = os.listdir(music_dir)
                print(songs)    
                os.startfile(os.path.join(music_dir, songs[0]))

            # elif ("weather","tell me the weather report")in self.query:
                # search_term = voice_data.split("for")[-1]
                # url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
                # webbrowser.get().open(url)
                # speak("Here is what I found for on google")


            elif "game" in self.query:
                voice_data = record_audio("choose among rock paper or scissor")
                moves=["rock", "paper", "scissor"]
    
                cmove=random.choice(moves)
                pmove=voice_data
        

                speak("i chose " + cmove)
                speak("You chose " + pmove)
                
                if pmove==cmove:
                    speak("the match is draw")
                elif pmove== "rock" and cmove== "scissor":
                    speak("you win")
                elif pmove== "rock" and cmove== "paper":
                 speak("i win")
                elif "paper" and cmove== "rock":
                    speak("you win")
                elif pmove== "paper" and cmove== "scissor":
                    speak("i wins")
                elif pmove== "scissor" and cmove== "paper":
                    speak("you win")
                elif pmove== "scissor" and cmove== "rock":
                    speak("i win")

    #11 toss a coin
            elif "toss" in  self.query:
                moves=["head", "tails"]   
                cmove=random.choice(moves)
                speak("it is " + cmove)

    #12 calc
            elif there_exists(["plus","minus","multiply","divide","power","+","-","*","/"]):
                
                opr = voice_data.split()[1]

                if opr == '+':
                    speak(int(voice_data.split()[0]) + int(voice_data.split()[2]))
                elif opr == '-':
                    speak(int(voice_data.split()[0]) - int(voice_data.split()[2]))
                elif opr == 'multiply':
                    speak(int(voice_data.split()[0]) * int(voice_data.split()[2]))
                elif 'divide':
                    speak(int(voice_data.split()[0]) / int(voice_data.split()[2]))
                elif opr == 'power':
                    speak(int(voice_data.split()[0]) ** int(voice_data.split()[2]))
                else:
                    speak("Wrong input")







FROM_MAIN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"D:/Files/Voice Assistant/scifi.ui"))
class Main(QMainWindow,FROM_MAIN):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(1850,1020)
        
        self.exitB.setStyleSheet("background-image:url(D:/Files/Voice Assistant/lib/exit.png);\n"
        "border:none;")
        self.exitB.clicked.connect(self.close)
        self.setWindowFlags(flags)
        Dspeak = mainT()
        self.label_7 = QMovie("D:/Files/Voice Assistant/lib/gifloader.gif", QByteArray(), self)
        self.label_7.setCacheMode(QMovie.CacheAll)
        self.label_4.setMovie(self.label_7)
        self.label_7.start()
        self.ts = time.strftime("%A, %d %B")

        Dspeak.start()
        self.label.setPixmap(QPixmap("D:/Files/Voice Assistant/lib/1560881.png"))
        self.label_5.setText("<font size=8 color='cyan'>"+self.ts+"</font>")
        self.label_5.setFont(QFont(QFont('ROG Fonts',8)))
        Dspeak.message_received.connect(self.setlabel_text)
    @QtCore.pyqtSlot(str)
    def setlabel_text(self,text):
        self.label_2.setText("<font size=8 color='cyan'>"+text+"</font>")
        self.label_2.setFont(QFont(QFont('ROG Fonts',8)))

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    exit(app.exec_())