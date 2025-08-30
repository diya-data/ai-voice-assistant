import pyttsx3  
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
from PIL import Image
import threading
import tkinter as tk
from tkinter import scrolledtext

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def play_song(song_name):
    music_folder = "C:\\Users\\sc683\\Downloads"
    song_found = False

    all_songs = os.listdir(music_folder)

    for song in all_songs:
        if song_name.lower() in song.lower():
            os.startfile(os.path.join(music_folder, song))
            song_found = True
            break

    if not song_found:
        print(f"Song '{song_name}' not found in the music folder.")

def open_word_document(file_path):
    try:
        os.system(f"start {file_path}")
        print(f"Opening {file_path}...")
        speak("opening document")
    except Exception as e:
        print(f"Error: {e}")

def open_images_in_folder(folder_path):
    try:
        if not os.path.exists(folder_path):
            print("Folder doesn't exist.")
            return

        files = os.listdir(folder_path)
        image_files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))
                       and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        if not image_files:
            print("No image files found in the folder.")
            return

        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            img = Image.open(image_path)
            img.show()

    except Exception as e:
        print(f"An error occurred: {e}")

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('sc6836747@gmail.com', 'mleo iixv nsas etkk')  # Make sure your password or app-specific password is correct
        server.sendmail('sc6836747@gmail.com', to, content)
        server.close()
    except Exception as e:
        print(f"Failed to send email: {e}")

def WishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Diya AI, how can I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()

    except Exception as e:
        print(f"Recognition error: {e}")
        print("Say that again please...")
        return "None"

def assistant_loop(output_box):
    def speak_gui(text):
        speak(text)
        output_box.insert(tk.END, f"Assistant: {text}\n")
        output_box.see(tk.END)

    WishMe()
    speak_gui("I am Sahana and Dia AI, how can I help you?")

    while True:
        query = takeCommand()
        if query == "None":
            speak_gui("Say that again please...")
            continue

        output_box.insert(tk.END, f"You said: {query}\n")
        output_box.see(tk.END)

        sites = [['youtube', 'https://www.youtube.com'], ['google', 'https://www.google.com'],
                 ['w3schools', 'https://www.w3schools.com'], ['stack overflow', 'https://www.stackoverflow.com'],
                 ['linkedin', 'https://www.linkedin.com/feed/']]

        for site in sites:
            if f"open {site[0]}" in query:
                speak_gui(f"Opening {site[0]}")
                webbrowser.open(site[1])
                break

        if 'wikipedia' in query:
            speak_gui('Searching Wikipedia...')
            query = query.replace('wikipedia', '')
            try:
                result = wikipedia.summary(query, sentences=2)
                speak_gui('According to Wikipedia')
                speak_gui(result)
            except Exception as e:
                speak_gui("Sorry, I could not find anything on Wikipedia.")
                print(e)

        elif 'play music' in query:
            speak_gui("Which song would you like to play?")
            song_name = takeCommand()
            play_song(song_name)

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak_gui(f"The time is {strTime}")

        elif 'open vs code' in query:
            speak_gui('Opening VS Code')
            vscodePath = "C:\\Users\\bindu\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code"
            os.startfile(vscodePath)

        elif 'email to sc' in query:
            try:
                speak_gui('What should I say?')
                content = takeCommand()
                to = 'sc6836747@gmail.com'
                sendEmail(to, content)
                speak_gui("Email has been sent successfully")
            except Exception as e:
                print(e)
                speak_gui("Sorry, I am not able to send the email at the moment. Please try again later.")

        elif 'open my document' in query:
            file_path = "E:\\cn lab\\1st3rd.txt"
            open_word_document(file_path)

        elif 'open my photos' in query:
            folder_path = "E:\\music_folder\\photos"
            open_images_in_folder(folder_path)

        elif 'play first song' in query:
            play_song("Appa")

        elif 'play second song' in query:
            play_song("Amma")

        elif 'play third song' in query:
            play_song("flute")

        elif 'play fourth song' in query:
            play_song("music3")

        elif 'play fifth song' in query:
            play_song("violin")

        elif 'play sixth song' in query:
            play_song("single tune")

        elif 'quit the chat' in query or 'exit' in query or 'stop' in query:
            speak_gui('Thank you, have a great day!')
            break

def start_assistant(output_box, start_button):
    start_button.config(state=tk.DISABLED)
    threading.Thread(target=assistant_loop, args=(output_box,), daemon=True).start()

def main():
    window = tk.Tk()
    window.title("Voice Assistant - Diya")
    window.geometry("600x400")

    output_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=20, font=("Arial", 10))
    output_box.pack(pady=10)

    start_button = tk.Button(window, text="Start Assistant", font=("Arial", 14),
                             command=lambda: start_assistant(output_box, start_button))
    start_button.pack(pady=10)

    window.mainloop()

if _name_ == "_main_":
    main()