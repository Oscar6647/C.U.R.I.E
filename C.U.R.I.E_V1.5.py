from tkinter import *
import tkinter as tk
from playsound import playsound 
import time
import gtts
import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests
import subprocess
import wikipedia
import imghdr
from datetime import datetime
from datetime import date
from pytz import timezone 
from email.message import EmailMessage
import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle

#Responde a los comandos mediante audio auto generado
def response(audio):
    print(audio)
    tts = gtts.tts.gTTS(text=audio, lang="en")
    tts.save("audio.mp3")
    playsound ('audio.mp3')
    os.remove("audio.mp3")

#escucha los comandos
def myCommand():
    #"listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        response('How may i help You?')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand()
    return command
#El gran metodo que hace que todo sea funcional 
def assistant(command):
    
    #Search in Wikipedia
    if 'what is ' in command:
        response("According to Wikipedia")
        reg_ex = re.search('what is (.*)', command)
        if reg_ex:
            subject = reg_ex.group(1) 
            test=wikipedia.summary(subject)
            response(test)
        response("please repeat the question")
        
    #Enviar Mail
    if 'send email' in command:
        response("To who are we sending this email?")
        print ("please write the reciver's email")
        Emailreciever=str(input())
        EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
        msg= EmailMessage()
        response("What will be the subject of our email?")
        print ("please write the email's subject")
        subject=str(input())
        msg['Subject'] = subject
        msg['From']= EMAIL_ADDRESS
        msg['To'] = Emailreciever
        response("What would you like to say in the email?")
        print ("please write the message")
        message=str(input())
        msg.set_content(message)
        response("Would you like to add an attachment ?")
        decision = str(input())
        if "yes" in decision:
            with open ('proof.jpg','rb')as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name
            msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
            with smtplib.SMTP_SSL('smtp.mail.yahoo.com',465)as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                
                smtp.send_message(msg)
            confirm = f'Email succesfuly sent to {Emailreciever}'
            response (confirm)
        if "no" in decision :
            with smtplib.SMTP_SSL('smtp.mail.yahoo.com',465)as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                
                smtp.send_message(msg)
            confirm = f'Email succesfuly sent to {Emailreciever}'
            response (confirm)
    
    #Open Google
    if 'google' in command:
        response ("Openinng google")
        url="https://www.google.com/"
        webbrowser.open(url)
        
    #Open Youtube   
    if "youtube" in command:
        response ("Openinng youtube")
        webbrowser.open(
        'https://www.youtube.com/'
        )
    #Open my School's Worksite
    if "canvas" in command:
        response ("Openinng canvas")
        webbrowser.open(
        'https://experiencia21.tec.mx/'
        )
        
    #Open facebook
    if "facebook" in command :
        response ("Openinng facebook")
        webbrowser.open(
        'https://www.facebook.com/'
        )
        
    #Open my drive    
    if "drive" in command:
        response ("Openinng drive")
        webbrowser.open(
        'https://drive.google.com/drive/u/1/my-drive'
        )
        
    #Open Reddit    
    if 'open reddit' in command:
        response ("Openning reddit")
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        
        #Open a reddit sub (specific can be said by user)
        if reg_ex:
            subreddit = reg_ex.group(1)
            response (f"Opening subreddit {subreddit}")
            url = url + 'r/' + subreddit
        webbrowser.open(url)

    #Open any website    
    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            response(f'Opening {domain}')
            url = 'https://www.' + domain
            webbrowser.open(url)
            
        else:
            pass
        
    #close webpage
    if 'close'in command:
        close_x(command)
        #os.system("taskkill /im chrome.exe /f")
        
    #tell time
    if "time" in command:
        zona_horaria = timezone('America/Monterrey') 
        fecha_hora = datetime.now(zona_horaria) 
        fecha_hora_formato = fecha_hora.strftime("%H:%M:%S") 
        response(fecha_hora_formato)
        
    #tell date
    if "day" in command:
        zona_horaria = timezone('America/Monterrey') 
        fecha_hora = datetime.now(zona_horaria) 
        fecha_hora_formato = fecha_hora.strftime("%B %d, %Y")
        day_week()
        response(f'Today is {day_week()} {fecha_hora_formato}')
        
    #Default play music
    if "play my work music" in command:
        response("Playing your Work Music!, Let's get the job done sir!")
        webbrowser.open("https://www.youtube.com/watch?v=bcyvZIoQp9A")
        
    #SUPER COMMANDS
    
    #open discord + Spotify
    if "hangout" in command:
        response("Hangout mode entered")
        discord = r"C:\Users\OCG\AppData\Local\Discord\app-0.0.308\Discord.exe"
        subprocess.Popen([discord]) 
        spotify = r"C:\Users\OCG\AppData\Roaming\Spotify\Spotify.exe"
        subprocess.Popen([spotify]) 
        
    #open discord+github+spotify
    if "hackathon" in command:
        response("Hackathon Mode engaged, Good Luck Sir!")
        discord = r"C:\Users\OCG\AppData\Local\Discord\app-0.0.308\Discord.exe"
        subprocess.Popen([discord]) 
        spotify = r"C:\Users\OCG\AppData\Roaming\Spotify\Spotify.exe"
        subprocess.Popen([spotify])
        github = r"C:\Users\OCG\AppData\Local\GitHubDesktop\GitHubDesktop.exe"
        subprocess.Popen([github])
        
    #Open zoom+school's workwebsite
    if "college" in command:
        college_mode()
        if(college_mode()==True):
            response("initiating College Mode")
            zoom = r"C:\Users\OCG\AppData\Roaming\Zoom\bin\Zoom.exe"
            subprocess.Popen([zoom])
            webbrowser.open('https://experiencia21.tec.mx/')
        else:
            response ("I'm sorry sir, but right now you don't have classes.")
            time.sleep(2)
            response ("College Mode overrided")
            
    #Open spotify + vscode
    if "software" in command:
        response("Entering Software Mode")
        spotify = r"C:\Users\OCG\AppData\Roaming\Spotify\Spotify.exe"
        subprocess.Popen([spotify])
        vscode = r"C:\Users\OCG\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        subprocess.Popen([vscode]) 
        
    #Open Eclipse
    if  "old-school" in command:
        response("Initiating Old-School Protocol")
        java = r"C:\Users\OCG\eclipse\java-photon\eclipse\eclipse.exe"
        subprocess.Popen([java])
        
    #Open matlab
    if  "simulation" in command:
        response("Initiating Mathematical Simulation Mode")
        matlab = r"C:\Program Files\MATLAB\R2020b\bin\matlab.exe"
        subprocess.Popen([matlab])
        
    #Open discord + steam
    if  "game night" in command:
        response("Initiating Game Night Protocols")
        discord = r"C:\Users\OCG\AppData\Local\Discord\app-0.0.308\Discord.exe"
        subprocess.Popen([discord])
        steam = r"C:\Program Files (x86)\Steam\steam.exe"   
        subprocess.Popen([steam]) 
        
   #Open CAD software
    if "hardware" in command:
        response("Starting Hardware mode")
        Digital_Design = r"C:\Program Files (x86)\LEGO Company\LEGO Digital Designer\LDD.exe"
        subprocess.Popen([Digital_Design])
        
    #Open CAD software + Lego Mindstorm Programming app
    if "teacher" in command:
        response("Entering Teaching mode")
        Digital_Design = r"C:\Program Files (x86)\LEGO Company\LEGO Digital Designer\LDD.exe"
        subprocess.Popen([Digital_Design])
        Ev3 = r"C:\Program Files (x86)\LEGO Software\LEGO MINDSTORMS Edu EV3\MindstormsEV3.exe"
        subprocess.Popen([Ev3])
        
    #Open Eclipse + FRC Project 
    if "app project" in command:
        response("Entering App Project work mode")
        java = r"C:\Users\OCG\eclipse\java-photon\eclipse\eclipse.exe"
        subprocess.Popen([java])
        frc_project = r"C:\Users\OCG\Desktop\Robot Inspector APP.exe"
        subprocess.Popen([frc_project])
    #Introductions
    if("present yourself")in command:
        response("Hello Everyone! I am the Central Unit of Robotics Inteligence and Experiements. Or Curie for short.")
    
    #Control computer (Shutdown,Reboot or Sleep)
    if ("computer status") in command:
        computer_status(command)
def computer_status (command):
    if "shutdown" in command:
        response("Your Computer will Shutdown at this moment")
        safeguard=str(input())
        if "yes" in safeguard:    
            response ("Goodbye")
            os.system("shutdown /s /t 1") 
        else:
            response("Shutdown Overrided")
    if  "reboot" in command:
        sfguard=str(input())
        response ("Rebooting your computer")
        if "yes" in sfguard:    
            os.system("shutdown /r /t l")
        else:
            response ("Reboot overrided")

#Method to control when to activate college mode             
def college_mode():
    correct = bool()
    if(date.today().weekday()!=6 and date.today().weekday()!=5):
        if (date.today().weekday()!= 0 and date.today().weekday()!=3):
            correct=True
        elif(date.today().weekday() == 0 and date.today().weekday() ==3 and datetime.now()<=9):
            correct=True
    else:
        correct=False
    return(correct)

#Close method for specific apps
def close_x(command):
    if "web"in command:
        os.system("taskkill /im chrome.exe /f")
    if "discord" in command:
        os.system("taskkill /im Discord.exe /f")
    if "steam" in command:
        os.system("taskkill /im steam.exe /f")
    if "zoom" in command:
        os.system("taskkill /im zoom.exe /f")
    if "github" in command:
        os.system("taskkill /im GitHubDesktop.exe /f")
    if "java" in command:
        os.system("taskkill /im eclipse.exe /f")
    if "matlab" in command:
        os.system("taskkill /im matlab.exe /f")
    if "frc project" in command:
        os.system("taskkill /im javaw.exe /f")
    if "lego design" in command:
        os.system("taskkill /im LDD.exe /f")
    if "mindstorm" in command:
        os.system("taskkill /im MindstormsEV3.exe /f")
    if "spotify" in command:
        os.system("taskkill /im Spotify.exe /f")
    if "vs code" in command:
        os.system("taskkill /im Code.exe /f")
        
#Date method
def day_week():
    day_week = ""  
    if date.today().weekday() == 0 :
        day_week = "Monday"
    elif date.today().weekday() == 1:
        day_week ="Tuesday"
    elif date.today().weekday() == 2:
        day_week ="Wednesday"
    elif date.today().weekday() == 3:
        day_week = "Thursday"
    elif date.today().weekday() == 4: 
        day_week = "Friday"
    elif date.today().weekday() == 5:
        day_week = "Saturday"
    else:
        day_week="Sunday"
    return day_week

#Predessor UI
class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 1

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

class Widget:
    def __init__(self):
        gui = Tk()
        gui.geometry("500x500")
        gui.resizable(0,0)
        gui.title("Central Unit of Robotics Inteligence and Experiements")
        photo = PhotoImage(file = "LOGO.png")
        gui.iconphoto(False, photo)
        lbl =ImageLabel(gui)
        lbl.load('Neutron.gif.gif')
        lbl.pack(fill = BOTH, expand = 1)
        callbtn = Button(gui, text ="Call C.U.R.I.E",bg='#4b4b4b', fg='black',command=self.clicked)
        callbtn.pack()
        callbtn.place(bordermode=OUTSIDE, height=40, width=100,x=400,y=460)
        gui.mainloop()
    def clicked(self):
        assistant(myCommand())

 #MAIN method       
if __name__ == '__main__':
    currentTime = datetime.now()
    currentTime.hour
    if currentTime.hour < 12:
        greet='Good morning'
    elif 12 <= currentTime.hour < 18:
        greet='Good afternoon'
    else:
        greet='Good evening'
    response (f"{greet}, initializing systems")
    mn = Widget()  
        
        
