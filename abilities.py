import os, webbrowser, sys, requests, subprocess, pyttsx3, pyautogui
from datetime import datetime


################ Код, ответственный за text to speech

tts = pyttsx3.init()
tts.setProperty('rate',180) #speech speed

#более качественная озвучка, если она есть
for voice in tts.getProperty('voices'):
    if voice.name == 'Arina': #RHVoice-voice-Russian-Arina sati-5
        tts.setProperty('voice', voice.id)

def speaker(text):
    tts.say(text) #озвучивание
    tts.runAndWait() #ожидание

################ Конец кода, ответственного за text to speech

#def offbot():
#    sys.exit()

def passive():
    pass

def browser():
    webbrowser.open('https://google.com', new=2)

def youtube():
    webbrowser.open('https://youtube.com', new=2)

#def pc_shutdown():
#    os.system('shutdown /s')

def music():            #такой способ работает только на английской раскладке и даже так иногда печатает не те символы
    pyautogui.hotkey('winleft')
    pyautogui.typewrite('music:')
    pyautogui.hotkey('enter')


def createfile():
    r = open('file.txt','w')
    inp = input()
    r.write(inp)
    r.close()

def explorer():
    subprocess.Popen('C:/Windows/explorer.exe')


def current_time():
    current_date = datetime.now()
    speaker(f"{current_date.hour} {current_date.minute}")







