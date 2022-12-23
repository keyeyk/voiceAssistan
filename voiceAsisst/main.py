import speech_recognition as sr
from datetime import datetime
import webbrowser
from gtts import gTTS
from playsound import playsound
import os
import time
import random
from random import choice
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

r = sr.Recognizer()

def record(ask = False):
    with sr.Microphone() as source:
        if ask:
            print(ask)
        audio = r.listen(source)
        voice = ""
        try:
            voice = r.recognize_google(audio, language="tr-TR")
        except sr.UnknownValueError:
            speak("Anlayamadım.")
        except sr.RequestError:
            speak("Sistem çalışmıyor.")
        return voice

def response(voice):
        if 'nasılsın' in voice:
            speak('İyi senden')
        
        if 'tamamdır' in voice:
            speak('Görüşürüz.')
            exit()

        if 'hangi gündeyiz' in voice:
            today = time.strftime("%A")
            if today == "Monday":
                today = "Pazartesi"
            elif today == "Tuesday":
                today = "Salı"
            elif today == "Wednesday":
                today = "Çarşamba"
            elif today == "Thursday":
                today = "Perşembe"
            elif today == "Friday":
                today = "Cuma"
            elif today == "Saturday":
                today = "Cumartesi"
            elif today == "Sunday":
                today = "Pazar"
            speak(today)

        if 'saat kaç' in voice:
            selection = ["Saat şu an: ", "Hemen bakıyorum: "]
            clock = datetime.now().strftime('%H:%M:%S')
            selection = random.choice(selection)
            speak(selection + clock)  
        
        if 'arama yap' in voice or 'google aç' in voice:
            speak("Ne arama mı istersiniz?")
            search = record()
            url = "https://www.google.com/search?q={}".format(search)
            webbrowser.get().open(url)
            speak("{} için Google'da bulduklarım".format(search))
        
        if 'video aç' in voice or 'müzik aç' in voice or 'youtube aç' in voice:
            speak("Ne açmamı istersiniz")
            search = record()
            url = "https://www.youtube.com/results?search_query={}".format(search)
            time.sleep(1)
            yt = webdriver.Chrome().get(url)
            speak("{} için Youtube'da bulduklarım".format(search))
        
        if 'film aç' in voice:
            speak("Hangi tür film istersin")
            search = record()
            url = "https://www.filmmodu10.com/hd-film-kategori/{}".format(search)
            tar = webdriver.Chrome().get(url)
            speak("{} için bulduğum filmler şunlar".format(search))

        if 'hava durumunu göster' in voice or 'hava durumu' in voice: 
            speak("Hangi şehrin hava durumunu istiyorsunuz")
            search = record()
            url = "https://www.ntv.com.tr/{}-hava-durumu".format(search)
            request = requests.get(url)
            html_ic = request.content
            soup = BeautifulSoup(html_ic, "html.parser")

            gunduz = soup.find_all("p",{"class":"hava-durumu--detail-data-item-bottom-temp-max"})
            gece = soup.find_all("p",{"class":"hava-durumu--detail-data-item-bottom-temp-min"})
            hav_dur = soup.find_all("div",{"class":"container hava-durumu--detail-data-item-bottom-desc"})
            
            gunduz_arr = []
            gece_arr = []
            hav_dur_arr = []

            for i in gunduz:
                i = i.text
                gunduz_arr.append(i)

            for j in gece:
                j = j.text
                gece_arr.append(j)

            for k in hav_dur:
                k = k.text
                hav_dur_arr.append(k)
            
            #print(gunduz_arr[0])
            
            birles = "{} için yarın hava durumu şöyle {} gündüz sıcaklığı {} gece sıcaklığı {}".format(search, hav_dur_arr[0], gunduz_arr[0], gece_arr[0])
            # = search + "için yarın hava durumu şöyle" + hav_dur_arr[0] + "gündüz sıcaklığı" + gunduz_arr[0] + "gece sıcaklığı" + gece_arr[0]
            speak(birles)

def speak(string):
    tts = gTTS(text=string, lang="tr", slow=False)
    file = "answer.mp3"
    tts.save(file)
    playsound(file)
    os.remove(file)

speak('Nasıl yardımcı olabilirim?')

while True:
    voice = record()
    if voice != '':
        voice = voice.lower()
        print(voice)
        response(voice)
