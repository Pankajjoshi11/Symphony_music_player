import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pygame
import os
import time
from pygame import mixer
from mutagen.mp3 import MP3
import random
from tkinter import *
from PIL import Image,ImageTk
import speech_recognition as sr
from gtts import gTTS
import pyautogui
import webbrowser
import threading
from pydub import AudioSegment
import winsound
import matplotlib.pyplot as plt
from datetime import datetime
import pickle
import scipy.io.wavfile as wav
import sounddevice as sd
from tkinter import filedialog
import numpy as np

main_window = Tk()
main_window.geometry('1242x700')  # 990x660+50+50
main_window.resizable(0, 0)
main_window.title("Symphony")
background_image = ImageTk.PhotoImage(file='Symphonybg5.png')
background_label = Label(main_window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Make the label cover the whole window

# You may need to keep a reference to the image object to prevent it from being garbage-collected
background_label.image = background_image


# functionality
def open_pop():
    pop_window = tk.Toplevel()
    pop_window.title("Pop Songs")
    pop_window.geometry('1250x700')
    pop_window.configure(bg='purple')

    pygame.mixer.init()

    global current_song_index, paused, repeat_mode

    def increase_volume():
        current_volume = mixer.music.get_volume()
        if current_volume < 1.0:
            new_volume = min(current_volume + 0.6, 1.0)
            mixer.music.set_volume(new_volume)

    def decrease_volume():
        current_volume = mixer.music.get_volume()
        if current_volume > 0.0:
            new_volume = max(current_volume - 0.6, 0.0)
            mixer.music.set_volume(new_volume)

    current_song_index = 0  # Initialize current song index
    paused = False
    repeat_mode = False

    background = "purple"
    frame_bg = "#000000"  # Black background color for the frame
    frame_fg = "#FFFFFF"  # White foreground color for the frame

    # Assuming you have an image file named 'example_image.png' in the same directory
    image_path = "./assets/shawn.png"
    image = tk.PhotoImage(file=image_path)
    image_label = tk.Label(pop_window, image=image, bg=background)
    image_label.place(relx=0.1, rely=0.15)

    pop_label = tk.Label(pop_window, text="Pop Songs", font=('Arial', 42, 'bold'), background=background,
                         foreground='white')
    pop_label.place(relx=0.42, rely=0.22)

    bottom_frame = tk.Frame(pop_window, bg=frame_bg)
    bottom_frame.place(relx=0, rely=0.35, relwidth=1, relheight=1)

    # List of songs
    song_list = [
        "./music/Kanye West - Heartless.mp3",
        "./music/The Weeknd, Ariana Grande - Die For You (Remix - Lyric Video).mp3",
        "./music/Badtameez Dil Full Song HD Yeh Jawaani Hai Deewani  PRITAM  Ranbir Kapoor, Deepika Padukone.mp3"
        # Add more songs here
    ]

    # Create a Listbox to display the list of songs
    song_listbox = tk.Listbox(bottom_frame, bg=frame_bg, fg=frame_fg, font=('Arial', 14), selectbackground="purple",
                              selectforeground="white")
    song_listbox.place(x=100, y=100, width=1300, height=370)
    for song in song_list:
        song_listbox.insert(tk.END, os.path.basename(song))  # Display only the filename, not the full path

    def play_music():
        selected_song_index = song_listbox.curselection()
        if selected_song_index:
            song_path = song_list[selected_song_index[0]]
            mixer.music.load(song_path)
            mixer.music.play(loops=0)

    # Bind the play_music function to handle the selection event in the listbox
    song_listbox.bind('<<ListboxSelect>>', lambda event: play_music())

    play_image = tk.PhotoImage(file="./assets/play.png")
    play_button = tk.Button(bottom_frame, image=play_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                            activeforeground='white', activebackground='#3C3C3C', cursor='hand2', command=play_music)
    play_button.place(x=100, y=30)

    def get_time():
        current_time = pygame.mixer.music.get_pos() / 1000
        formatted_current_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
        selected_song_index = song_listbox.curselection()
        if selected_song_index:
            song_length = int(MP3(song_list[selected_song_index[0]]).info.length)
            formatted_song_length = time.strftime("%H:%M:%S", time.gmtime(song_length))
            label_time.config(text=f"{formatted_song_length} / {formatted_current_time}")
            progress["maximum"] = song_length
            progress["value"] = int(current_time)
        pop_window.after(100, get_time)

    # Define a function to shuffle the playlist
    def shuffle_playlist_and_play():
        random.shuffle(song_list)
        song_listbox.delete(0, tk.END)
        for song in song_list:
            song_listbox.insert(tk.END, os.path.basename(song))
        play_selected_song()

    shuffle_image = tk.PhotoImage(file="./assets/shuffle.png")
    shuffle_button = tk.Button(bottom_frame, image=shuffle_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                               activeforeground='white', activebackground='white', cursor='hand2',
                               command=shuffle_playlist_and_play)
    shuffle_button.place(x=180, y=33)

    # Define a function to toggle repeat mode
    def toggle_repeat():
        global repeat_mode
        repeat_mode = not repeat_mode
        if repeat_mode:
            repeat_button.config(image=repeat_on_image)
        else:
            repeat_button.config(image=repeat_off_image)

    # Create a button to toggle repeat mode
    repeat_off_image = tk.PhotoImage(file="./assets/next.png")
    repeat_on_image = tk.PhotoImage(file="./assets/onrepeat.png")
    repeat_mode = False  # Initial state of repeat mode
    repeat_button = tk.Button(bottom_frame, image=repeat_off_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                              activeforeground='white', activebackground='white', cursor='hand2', command=toggle_repeat)
    repeat_button.place(x=260, y=30)

    low_frame = tk.Frame(pop_window, bg='black')
    low_frame.place(relx=0, rely=0.85, relwidth=1, relheight=1)

    border_frame = tk.Frame(pop_window, bg='white', height=2)  # Adjust height as needed
    border_frame.place(relx=0, rely=0.85, relwidth=1)

    # Create a progress bar
    progress = ttk.Progressbar(pop_window, orient='horizontal', mode='determinate', length=1200,
                               style="Custom.Horizontal.TProgressbar")
    progress.place(relx=0.1, rely=0.9)

    progress_bar_color = 'green'
    # Define a custom style for the progress bar
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Custom.Horizontal.TProgressbar", troughcolor=frame_bg, background=progress_bar_color)

    # Label to display time information
    label_time = tk.Label(low_frame, text="", bg='black', fg=frame_fg, font=('Arial', 12))
    label_time.place(relx=0.89, rely=0.049)

    def volume(x):
        pygame.mixer.music.set_volume(slider.get())
        slider.place(relx=0.072, rely=0.76)

    def toggle_slider():
        slider.place(relx=0.072, rely=0.76)

    image_vol = tk.PhotoImage(file='./assets/sound.png')
    slider_button = tk.Button(low_frame, image=image_vol, font=('Arial', 12), fg='white', bg='purple',
                              activeforeground='white', activebackground='purple', cursor='hand2',
                              command=toggle_slider)
    slider_button.place(relx=0.07, rely=0.044)

    slider = ttk.Scale(pop_window, from_=0, to=1, orient=tk.VERTICAL,
                       value=1, length=100, command=volume)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Vertical.TScale", background="purple", troughcolor="black", sliderlength=30)

    def play_selected_song():
        mixer.music.load(song_list[current_song_index])
        mixer.music.play(loops=0)
        get_time()

    repeat_img = tk.PhotoImage(file='./assets/onrepeat.png')
    button_repeat = tk.Button(low_frame, image=repeat_img, bg=background, fg='black', activebackground='black',
                              command=play_selected_song)
    button_repeat.place(relx=0.8, rely=0.07)

    def pause_unpause():
        global paused
        if paused:
            mixer.music.unpause()
            paused = False
            button_pause.config(image=pause_img)  # Change button image to pause image
        else:
            mixer.music.pause()
            paused = True
            button_pause.config(image=play_img)  # Change button image to play image

    paused = False  # Initial state of music playback

    pause_img = tk.PhotoImage(file='./assets/pause.png')
    play_img = tk.PhotoImage(file='./assets/play2.png')
    button_pause = tk.Button(low_frame, image=pause_img, width=4, bd=5,
                             font="Helvetica, 15", bg="purple", fg="white", command=pause_unpause)
    button_pause.place(relx=0.5, rely=0.07, relwidth=0.04, relheight=0.075)

    button_play = tk.Button(low_frame, image=play_img, width=4, bd=5,
                            font="Helvetica, 15", bg="black", fg="white", command=pause_unpause)

    current_song_index = 0  # Initialize the current song index

    def next_song():
        global current_song_index
        current_song_index = (current_song_index + 1) % len(song_list)
        play_selected_song()
        song_listbox.selection_clear(0, tk.END)  # Clear previous selection
        song_listbox.selection_set(current_song_index)  # Set selection to the next song
        song_listbox.see(current_song_index)

    def prev_song():
        global current_song_index
        current_song_index = (current_song_index - 1) % len(song_list)
        play_selected_song()
        song_listbox.selection_clear(0, tk.END)  # Clear previous selection
        song_listbox.selection_set(current_song_index)  # Set selection to the previous song
        song_listbox.see(current_song_index)

    def play_selected_song():
        mixer.music.load(song_list[current_song_index])
        mixer.music.play(loops=0)
        get_time()

    prev_img = tk.PhotoImage(file='./assets/previous.png')
    next_img = tk.PhotoImage(file='./assets/next.png')

    button_prev = tk.Button(low_frame, image=prev_img, bg=background, command=prev_song)
    button_prev.place(relx=0.45, rely=0.071)

    button_next = tk.Button(low_frame, image=next_img, bg=background, command=next_song)
    button_next.place(relx=0.55, rely=0.071)


    # Voice assistant functions

    def listen_for_command():
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening for commands...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except sr.RequestError:
            print("Unable to access the Google Speech Recognition API.")
            return None

    def process_command(command):
        global tasks, listeningToTask

        if command:
            if "play music" in command:
                play_music()
            elif "pause music" in command:
                pause_unpause()
            elif "next song" in command:
                next_song()
            elif "previous song" in command:
                prev_song()
            elif "stop music" in command:
                mixer.music.stop()
            elif "shuffle playlist" in command:
                shuffle_playlist_and_play()
            elif "repeat mode" in command:
                toggle_repeat()

            elif "volume up" in command:
                increase_volume()
            elif "volume down" in command:
                decrease_volume()





            elif "exit" in command:
                main_window.destroy()
            else:
                tasks.append(command)
                if not listeningToTask:
                    listeningToTask = True
                    listen_to_task()

    def listen_to_task():
        global tasks, listeningToTask

        if tasks:
            task = tasks.pop(0)
            process_command(task)  # Execute the task directly without audio output
            listeningToTask = False
        else:
            listeningToTask = False
            print("No tasks to perform")

    def speak(text):
        tts = gTTS(text=text, lang='en')
        tts.save("assistant_audio.mp3")
        sound = AudioSegment.from_mp3("assistant_audio.mp3")
        sound.export("assistant_audio.wav", format="wav")
        winsound.PlaySound("assistant_audio.wav", winsound.SND_FILENAME)
        os.remove("assistant_audio.mp3")
        os.remove("assistant_audio.wav")

    def assistant_task_listener():
        while True:
            command = listen_for_command()
            process_command(command)

    # Start the assistant task listener in a separate thread
    assistant_thread = threading.Thread(target=assistant_task_listener)
    assistant_thread.daemon = True
    assistant_thread.start()

    pop_window.mainloop()


def open_rock():
    rock_window = tk.Toplevel()
    rock_window.title("Rock Page")
    rock_window.geometry('1250x700')
    rock_window.configure(bg='purple')

    pygame.mixer.init()

    global current_song_index, paused, repeat_mode

    current_song_index = 0  # Initialize current song index
    paused = False
    repeat_mode = False

    background = "purple"
    frame_bg = "#000000"  # Black background color for the frame
    frame_fg = "#FFFFFF"  # White foreground color for the frame

    # Assuming you have an image file named 'example_image.png' in the same directory
    image_path = "./assets/rock2.png"
    image = tk.PhotoImage(file=image_path)
    image_label = tk.Label(rock_window, image=image, bg=background)
    image_label.place(relx=0.1, rely=0.15)

    pop_label = tk.Label(rock_window, text="Rock Songs", font=('Arial', 42, 'bold'), background=background,
                         foreground='white')
    pop_label.place(relx=0.42, rely=0.22)

    bottom_frame = tk.Frame(rock_window, bg=frame_bg)
    bottom_frame.place(relx=0, rely=0.35, relwidth=1, relheight=1)

    # List of songs
    song_list = [
        "./music/Dil Chahta Hai [Full Song] Dil Chahta Hai.mp3",
        "./music/The Strokes - The Adults Are Talking (Official Video).mp3"
        # Add more songs here
    ]

    # Create a Listbox to display the list of songs
    song_listbox = tk.Listbox(bottom_frame, bg=frame_bg, fg=frame_fg, font=('Arial', 14), selectbackground="purple",
                              selectforeground="white")
    song_listbox.place(x=100, y=100, width=1300, height=370)
    for song in song_list:
        song_listbox.insert(tk.END, os.path.basename(song))  # Display only the filename, not the full path

    def play_music():
        selected_song_index = song_listbox.curselection()
        if selected_song_index:
            song_path = song_list[selected_song_index[0]]
            mixer.music.load(song_path)
            mixer.music.play(loops=0)

    # Bind the play_music function to handle the selection event in the listbox
    song_listbox.bind('<<ListboxSelect>>', lambda event: play_music())

    play_image = tk.PhotoImage(file="./assets/play.png")
    play_button = tk.Button(bottom_frame, image=play_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                            activeforeground='white', activebackground='#3C3C3C', cursor='hand2', command=play_music)
    play_button.place(x=100, y=30)

    def get_time():
        current_time = pygame.mixer.music.get_pos() / 1000
        formatted_current_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
        selected_song_index = song_listbox.curselection()
        if selected_song_index:
            song_length = int(MP3(song_list[selected_song_index[0]]).info.length)
            formatted_song_length = time.strftime("%H:%M:%S", time.gmtime(song_length))
            label_time.config(text=f"{formatted_song_length} / {formatted_current_time}")
            progress["maximum"] = song_length
            progress["value"] = int(current_time)
        rock_window.after(100, get_time)

    # Define a function to shuffle the playlist
    def shuffle_playlist_and_play():
        random.shuffle(song_list)
        song_listbox.delete(0, tk.END)
        for song in song_list:
            song_listbox.insert(tk.END, os.path.basename(song))
        play_selected_song()

    shuffle_image = tk.PhotoImage(file="./assets/shuffle.png")
    shuffle_button = tk.Button(bottom_frame, image=shuffle_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                               activeforeground='white', activebackground='white', cursor='hand2',
                               command=shuffle_playlist_and_play)
    shuffle_button.place(x=180, y=33)

    # Define a function to toggle repeat mode
    def toggle_repeat():
        global repeat_mode
        repeat_mode = not repeat_mode
        if repeat_mode:
            repeat_button.config(image=repeat_on_image)
        else:
            repeat_button.config(image=repeat_off_image)

    # Create a button to toggle repeat mode
    repeat_off_image = tk.PhotoImage(file="./assets/next.png")
    repeat_on_image = tk.PhotoImage(file="./assets/onrepeat.png")
    repeat_mode = False  # Initial state of repeat mode
    repeat_button = tk.Button(bottom_frame, image=repeat_off_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                              activeforeground='white', activebackground='white', cursor='hand2', command=toggle_repeat)
    repeat_button.place(x=260, y=30)

    low_frame = tk.Frame(rock_window, bg='black')
    low_frame.place(relx=0, rely=0.85, relwidth=1, relheight=1)

    border_frame = tk.Frame(rock_window, bg='white', height=2)  # Adjust height as needed
    border_frame.place(relx=0, rely=0.85, relwidth=1)

    # Create a progress bar
    progress = ttk.Progressbar(rock_window, orient='horizontal', mode='determinate', length=1200,
                               style="Custom.Horizontal.TProgressbar")
    progress.place(relx=0.1, rely=0.9)

    progress_bar_color = 'green'
    # Define a custom style for the progress bar
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Custom.Horizontal.TProgressbar", troughcolor=frame_bg, background=progress_bar_color)

    # Label to display time information
    label_time = tk.Label(low_frame, text="", bg='black', fg=frame_fg, font=('Arial', 12))
    label_time.place(relx=0.89, rely=0.049)

    def volume(x):
        pygame.mixer.music.set_volume(slider.get())
        slider.place(relx=0.072, rely=0.76)

    def toggle_slider():
        slider.place(relx=0.072, rely=0.76)

    image_vol = tk.PhotoImage(file='./assets/sound.png')
    slider_button = tk.Button(low_frame, image=image_vol, font=('Arial', 12), fg='white', bg='purple',
                              activeforeground='white', activebackground='purple', cursor='hand2',
                              command=toggle_slider)
    slider_button.place(relx=0.07, rely=0.044)

    slider = ttk.Scale(rock_window, from_=0, to=1, orient=tk.VERTICAL,
                       value=1, length=100, command=volume)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Vertical.TScale", background="purple", troughcolor="black", sliderlength=30)

    def play_selected_song():
        mixer.music.load(song_list[current_song_index])
        mixer.music.play(loops=0)
        get_time()

    repeat_img = tk.PhotoImage(file='./assets/onrepeat.png')
    button_repeat = tk.Button(low_frame, image=repeat_img, bg=background, fg='black', activebackground='black',
                              command=play_selected_song)
    button_repeat.place(relx=0.8, rely=0.07)

    def pause_unpause():
        global paused
        if paused:
            mixer.music.unpause()
            paused = False
            button_pause.config(image=pause_img)  # Change button image to pause image
        else:
            mixer.music.pause()
            paused = True
            button_pause.config(image=play_img)  # Change button image to play image

    paused = False  # Initial state of music playback

    pause_img = tk.PhotoImage(file='./assets/pause.png')
    play_img = tk.PhotoImage(file='./assets/play2.png')
    button_pause = tk.Button(low_frame, image=pause_img, width=4, bd=5,
                             font="Helvetica, 15", bg="purple", fg="white", command=pause_unpause)
    button_pause.place(relx=0.5, rely=0.07, relwidth=0.04, relheight=0.075)

    button_play = tk.Button(low_frame, image=play_img, width=4, bd=5,
                            font="Helvetica, 15", bg="black", fg="white", command=pause_unpause)

    current_song_index = 0  # Initialize the current song index

    def next_song():
        global current_song_index
        current_song_index = (current_song_index + 1) % len(song_list)
        play_selected_song()
        song_listbox.selection_clear(0, tk.END)  # Clear previous selection
        song_listbox.selection_set(current_song_index)  # Set selection to the next song
        song_listbox.see(current_song_index)

    def prev_song():
        global current_song_index
        current_song_index = (current_song_index - 1) % len(song_list)
        play_selected_song()
        song_listbox.selection_clear(0, tk.END)  # Clear previous selection
        song_listbox.selection_set(current_song_index)  # Set selection to the previous song
        song_listbox.see(current_song_index)

    def play_selected_song():
        mixer.music.load(song_list[current_song_index])
        mixer.music.play(loops=0)
        get_time()

    prev_img = tk.PhotoImage(file='./assets/previous.png')
    next_img = tk.PhotoImage(file='./assets/next.png')

    button_prev = tk.Button(low_frame, image=prev_img, bg=background, command=prev_song)
    button_prev.place(relx=0.45, rely=0.071)

    button_next = tk.Button(low_frame, image=next_img, bg=background, command=next_song)
    button_next.place(relx=0.55, rely=0.071)

    # Button for navigation

    # Voice assistant functions

    def listen_for_command():
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening for commands...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except sr.RequestError:
            print("Unable to access the Google Speech Recognition API.")
            return None

    def process_command(command):
        global tasks, listeningToTask

        if command:
            if "play music" in command:
                play_music()
            elif "pause music" in command:
                pause_unpause()
            elif "next song" in command:
                next_song()
            elif "previous song" in command:
                prev_song()
            elif "stop music" in command:
                mixer.music.stop()
            elif "shuffle playlist" in command:
                shuffle_playlist_and_play()
            elif "repeat mode" in command:
                toggle_repeat()

            elif "volume up" in command:
                increase_volume()
            elif "volume down" in command:
                decrease_volume()





            elif "exit" in command:
                main_window.destroy()
            else:
                tasks.append(command)
                if not listeningToTask:
                    listeningToTask = True
                    listen_to_task()

    def listen_to_task():
        global tasks, listeningToTask

        if tasks:
            task = tasks.pop(0)
            process_command(task)  # Execute the task directly without audio output
            listeningToTask = False
        else:
            listeningToTask = False
            print("No tasks to perform")

    def speak(text):
        tts = gTTS(text=text, lang='en')
        tts.save("assistant_audio.mp3")
        sound = AudioSegment.from_mp3("assistant_audio.mp3")
        sound.export("assistant_audio.wav", format="wav")
        winsound.PlaySound("assistant_audio.wav", winsound.SND_FILENAME)
        os.remove("assistant_audio.mp3")
        os.remove("assistant_audio.wav")
    
    def increase_volume():
        current_volume = mixer.music.get_volume()
        if current_volume < 1.0:
            new_volume = min(current_volume + 0.6, 1.0)
            mixer.music.set_volume(new_volume)

    def decrease_volume():
        current_volume = mixer.music.get_volume()
        if current_volume > 0.0:
            new_volume = max(current_volume - 0.6, 0.0)
            mixer.music.set_volume(new_volume)

    def assistant_task_listener():
        while True:
            command = listen_for_command()
            process_command(command)

    # Start the assistant task listener in a separate thread
    assistant_thread = threading.Thread(target=assistant_task_listener)
    assistant_thread.daemon = True
    assistant_thread.start()

    

    rock_window.mainloop()




def open_hiphop():
    hiphop_window = tk.Toplevel()
    hiphop_window.title("Hiphop Page")
    hiphop_window.geometry('1250x700')
    hiphop_window.configure(bg='purple')

    pygame.mixer.init()

    global current_song_index, paused, repeat_mode

    current_song_index = 0  # Initialize current song index
    paused = False
    repeat_mode = False

    background = "purple"
    frame_bg = "#000000"  # Black background color for the frame
    frame_fg = "#FFFFFF"  # White foreground color for the frame

    # Assuming you have an image file named 'example_image.png' in the same directory
    image_path = "./assets/eminem.png"
    image = tk.PhotoImage(file=image_path)
    image_label = tk.Label(hiphop_window, image=image, bg=background)
    image_label.place(relx=0.1, rely=0.15)

    pop_label = tk.Label(hiphop_window, text="HipHop Songs", font=('Arial', 42, 'bold'), background=background,
                         foreground='white')
    pop_label.place(relx=0.42, rely=0.22)

    bottom_frame = tk.Frame(hiphop_window, bg=frame_bg)
    bottom_frame.place(relx=0, rely=0.35, relwidth=1, relheight=1)

    # List of songs
    song_list = [
        "./music/The Weeknd - Blinding Lights (Official Video).mp3",
        "./music/Dua Lipa - Levitating Featuring DaBaby (Official Music Video).mp3",
        "./music/Olivia Rodrigo - good 4 u (Official Video).mp3"
        # Add more songs here
    ]

    # Create a Listbox to display the list of songs
    song_listbox = tk.Listbox(bottom_frame, bg=frame_bg, fg=frame_fg, font=('Arial', 14), selectbackground="purple",
                              selectforeground="white")
    song_listbox.place(x=100, y=100, width=1300, height=370)
    for song in song_list:
        song_listbox.insert(tk.END, os.path.basename(song))  # Display only the filename, not the full path

    def play_music():
        selected_song_index = song_listbox.curselection()
        if selected_song_index:
            song_path = song_list[selected_song_index[0]]
            mixer.music.load(song_path)
            mixer.music.play(loops=0)

    # Bind the play_music function to handle the selection event in the listbox
    song_listbox.bind('<<ListboxSelect>>', lambda event: play_music())

    play_image = tk.PhotoImage(file="./assets/play.png")
    play_button = tk.Button(bottom_frame, image=play_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                            activeforeground='white', activebackground='#3C3C3C', cursor='hand2', command=play_music)
    play_button.place(x=100, y=30)

    def get_time():
        current_time = pygame.mixer.music.get_pos() / 1000
        formatted_current_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
        selected_song_index = song_listbox.curselection()
        if selected_song_index:
            song_length = int(MP3(song_list[selected_song_index[0]]).info.length)
            formatted_song_length = time.strftime("%H:%M:%S", time.gmtime(song_length))
            label_time.config(text=f"{formatted_song_length} / {formatted_current_time}")
            progress["maximum"] = song_length
            progress["value"] = int(current_time)
        hiphop_window.after(100, get_time)

    # Define a function to shuffle the playlist
    def shuffle_playlist_and_play():
        random.shuffle(song_list)
        song_listbox.delete(0, tk.END)
        for song in song_list:
            song_listbox.insert(tk.END, os.path.basename(song))
        play_selected_song()

    shuffle_image = tk.PhotoImage(file="./assets/shuffle.png")
    shuffle_button = tk.Button(bottom_frame, image=shuffle_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                               activeforeground='white', activebackground='white', cursor='hand2',
                               command=shuffle_playlist_and_play)
    shuffle_button.place(x=180, y=33)

    # Define a function to toggle repeat mode
    def toggle_repeat():
        global repeat_mode
        repeat_mode = not repeat_mode
        if repeat_mode:
            repeat_button.config(image=repeat_on_image)
        else:
            repeat_button.config(image=repeat_off_image)

    # Create a button to toggle repeat mode
    repeat_off_image = tk.PhotoImage(file="./assets/next.png")
    repeat_on_image = tk.PhotoImage(file="./assets/onrepeat.png")
    repeat_mode = False  # Initial state of repeat mode
    repeat_button = tk.Button(bottom_frame, image=repeat_off_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                              activeforeground='white', activebackground='white', cursor='hand2', command=toggle_repeat)
    repeat_button.place(x=260, y=30)

    low_frame = tk.Frame(hiphop_window, bg='black')
    low_frame.place(relx=0, rely=0.85, relwidth=1, relheight=1)

    border_frame = tk.Frame(hiphop_window, bg='white', height=2)  # Adjust height as needed
    border_frame.place(relx=0, rely=0.85, relwidth=1)

    # Create a progress bar
    progress = ttk.Progressbar(hiphop_window, orient='horizontal', mode='determinate', length=1200,
                               style="Custom.Horizontal.TProgressbar")
    progress.place(relx=0.1, rely=0.9)

    progress_bar_color = 'green'
    # Define a custom style for the progress bar
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Custom.Horizontal.TProgressbar", troughcolor=frame_bg, background=progress_bar_color)

    # Label to display time information
    label_time = tk.Label(low_frame, text="", bg='black', fg=frame_fg, font=('Arial', 12))
    label_time.place(relx=0.89, rely=0.049)

    def volume(x):
        pygame.mixer.music.set_volume(slider.get())
        slider.place(relx=0.072, rely=0.76)

    def toggle_slider():
        slider.place(relx=0.072, rely=0.76)

    image_vol = tk.PhotoImage(file='./assets/sound.png')
    slider_button = tk.Button(low_frame, image=image_vol, font=('Arial', 12), fg='white', bg='purple',
                              activeforeground='white', activebackground='purple', cursor='hand2',
                              command=toggle_slider)
    slider_button.place(relx=0.07, rely=0.044)

    slider = ttk.Scale(hiphop_window, from_=0, to=1, orient=tk.VERTICAL,
                       value=1, length=100, command=volume)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Vertical.TScale", background="purple", troughcolor="black", sliderlength=30)

    def play_selected_song():
        mixer.music.load(song_list[current_song_index])
        mixer.music.play(loops=0)
        get_time()

    repeat_img = tk.PhotoImage(file='./assets/onrepeat.png')
    button_repeat = tk.Button(low_frame, image=repeat_img, bg=background, fg='black', activebackground='black',
                              command=play_selected_song)
    button_repeat.place(relx=0.8, rely=0.07)

    def pause_unpause():
        global paused
        if paused:
            mixer.music.unpause()
            paused = False
            button_pause.config(image=pause_img)  # Change button image to pause image
        else:
            mixer.music.pause()
            paused = True
            button_pause.config(image=play_img)  # Change button image to play image

    paused = False  # Initial state of music playback

    pause_img = tk.PhotoImage(file='./assets/pause.png')
    play_img = tk.PhotoImage(file='./assets/play2.png')
    button_pause = tk.Button(low_frame, image=pause_img, width=4, bd=5,
                             font="Helvetica, 15", bg="purple", fg="white", command=pause_unpause)
    button_pause.place(relx=0.5, rely=0.07, relwidth=0.04, relheight=0.075)

    button_play = tk.Button(low_frame, image=play_img, width=4, bd=5,
                            font="Helvetica, 15", bg="black", fg="white", command=pause_unpause)

    current_song_index = 0  # Initialize the current song index

    def next_song():
        global current_song_index
        current_song_index = (current_song_index + 1) % len(song_list)
        play_selected_song()
        song_listbox.selection_clear(0, tk.END)  # Clear previous selection
        song_listbox.selection_set(current_song_index)  # Set selection to the next song
        song_listbox.see(current_song_index)

    def prev_song():
        global current_song_index
        current_song_index = (current_song_index - 1) % len(song_list)
        play_selected_song()
        song_listbox.selection_clear(0, tk.END)  # Clear previous selection
        song_listbox.selection_set(current_song_index)  # Set selection to the previous song
        song_listbox.see(current_song_index)

    def play_selected_song():
        mixer.music.load(song_list[current_song_index])
        mixer.music.play(loops=0)
        get_time()

    prev_img = tk.PhotoImage(file='./assets/previous.png')
    next_img = tk.PhotoImage(file='./assets/next.png')

    button_prev = tk.Button(low_frame, image=prev_img, bg=background, command=prev_song)
    button_prev.place(relx=0.45, rely=0.071)

    button_next = tk.Button(low_frame, image=next_img, bg=background, command=next_song)
    button_next.place(relx=0.55, rely=0.071)

    # Button for navigation

    # Voice assistant functions

    def listen_for_command():
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening for commands...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except sr.RequestError:
            print("Unable to access the Google Speech Recognition API.")
            return None

    def process_command(command):
        global tasks, listeningToTask

        if command:
            if "play music" in command:
                play_music()
            elif "pause music" in command:
                pause_unpause()
            elif "next song" in command:
                next_song()
            elif "previous song" in command:
                prev_song()
            elif "stop music" in command:
                mixer.music.stop()
            elif "shuffle playlist" in command:
                shuffle_playlist_and_play()
            elif "repeat mode" in command:
                toggle_repeat()

            elif "volume up" in command:
                increase_volume()
            elif "volume down" in command:
                decrease_volume()





            elif "exit" in command:
                main_window.destroy()
            else:
                tasks.append(command)
                if not listeningToTask:
                    listeningToTask = True
                    listen_to_task()

    def listen_to_task():
        global tasks, listeningToTask

        if tasks:
            task = tasks.pop(0)
            process_command(task)  # Execute the task directly without audio output
            listeningToTask = False
        else:
            listeningToTask = False
            print("No tasks to perform")

    def speak(text):
        tts = gTTS(text=text, lang='en')
        tts.save("assistant_audio.mp3")
        sound = AudioSegment.from_mp3("assistant_audio.mp3")
        sound.export("assistant_audio.wav", format="wav")
        winsound.PlaySound("assistant_audio.wav", winsound.SND_FILENAME)
        os.remove("assistant_audio.mp3")
        os.remove("assistant_audio.wav")
    
    def increase_volume():
        current_volume = mixer.music.get_volume()
        if current_volume < 1.0:
            new_volume = min(current_volume + 0.6, 1.0)
            mixer.music.set_volume(new_volume)

    def decrease_volume():
        current_volume = mixer.music.get_volume()
        if current_volume > 0.0:
            new_volume = max(current_volume - 0.6, 0.0)
            mixer.music.set_volume(new_volume)
            
    def assistant_task_listener():
        while True:
            command = listen_for_command()
            process_command(command)

    # Start the assistant task listener in a separate thread
    assistant_thread = threading.Thread(target=assistant_task_listener)
    assistant_thread.daemon = True
    assistant_thread.start()

    hiphop_window.mainloop()


def open_hindi():
    hindi_window = tk.Toplevel()
    hindi_window.title("Rock Page")
    hindi_window.geometry('1250x700')
    hindi_window.configure(bg='purple')

    pygame.mixer.init()

    global current_song_index, paused, repeat_mode

    current_song_index = 0  # Initialize current song index
    paused = False
    repeat_mode = False

    background = "purple"
    frame_bg = "#000000"  # Black background color for the frame
    frame_fg = "#FFFFFF"  # White foreground color for the frame

    # Assuming you have an image file named 'example_image.png' in the same directory
    image_path = "./assets/shreyahindi.png"
    image = tk.PhotoImage(file=image_path)
    image_label = tk.Label(hindi_window, image=image, bg=background)
    image_label.place(relx=0.1, rely=0.15)

    pop_label = tk.Label(hindi_window, text="Bollywood Songs", font=('Arial', 42, 'bold'), background=background,
                         foreground='white')
    pop_label.place(relx=0.42, rely=0.22)

    bottom_frame = tk.Frame(hindi_window, bg=frame_bg)
    bottom_frame.place(relx=0, rely=0.35, relwidth=1, relheight=1)

    # List of songs
    song_list = [
        "./music/Nachde Ne Saare - Full Video  Baar Baar Dekho  Sidharth Malhotra & Katrina Kaif  Jasleen Royal.mp3",
        "./music/Subha Hone Na De Full Song Desi Boyz  Akshay Kumar ,John Abraham  Pritam   Mika Singh, Kumaar.mp3",
        "./music/Deewani Mastani Full Video Song  Bajirao Mastani  Deepika Padukone.mp3"
        # Add more songs here
    ]

    # Create a Listbox to display the list of songs
    song_listbox = tk.Listbox(bottom_frame, bg=frame_bg, fg=frame_fg, font=('Arial', 14), selectbackground="purple",
                              selectforeground="white")
    song_listbox.place(x=100, y=100, width=1300, height=370)
    for song in song_list:
        song_listbox.insert(tk.END, os.path.basename(song))  # Display only the filename, not the full path

    def play_music():
        selected_song_index = song_listbox.curselection()
        if selected_song_index:
            song_path = song_list[selected_song_index[0]]
            mixer.music.load(song_path)
            mixer.music.play(loops=0)

    # Bind the play_music function to handle the selection event in the listbox
    song_listbox.bind('<<ListboxSelect>>', lambda event: play_music())

    play_image = tk.PhotoImage(file="./assets/play.png")
    play_button = tk.Button(bottom_frame, image=play_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                            activeforeground='white', activebackground='#3C3C3C', cursor='hand2', command=play_music)
    play_button.place(x=100, y=30)

    def get_time():
        current_time = pygame.mixer.music.get_pos() / 1000
        formatted_current_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
        selected_song_index = song_listbox.curselection()
        if selected_song_index:
            song_length = int(MP3(song_list[selected_song_index[0]]).info.length)
            formatted_song_length = time.strftime("%H:%M:%S", time.gmtime(song_length))
            label_time.config(text=f"{formatted_song_length} / {formatted_current_time}")
            progress["maximum"] = song_length
            progress["value"] = int(current_time)
        hindi_window.after(100, get_time)

    # Define a function to shuffle the playlist
    def shuffle_playlist_and_play():
        random.shuffle(song_list)
        song_listbox.delete(0, tk.END)
        for song in song_list:
            song_listbox.insert(tk.END, os.path.basename(song))
        play_selected_song()

    shuffle_image = tk.PhotoImage(file="./assets/shuffle.png")
    shuffle_button = tk.Button(bottom_frame, image=shuffle_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                               activeforeground='white', activebackground='white', cursor='hand2',
                               command=shuffle_playlist_and_play)
    shuffle_button.place(x=180, y=33)

    # Define a function to toggle repeat mode
    def toggle_repeat():
        global repeat_mode
        repeat_mode = not repeat_mode
        if repeat_mode:
            repeat_button.config(image=repeat_on_image)
        else:
            repeat_button.config(image=repeat_off_image)

    # Create a button to toggle repeat mode
    repeat_off_image = tk.PhotoImage(file="./assets/next.png")
    repeat_on_image = tk.PhotoImage(file="./assets/onrepeat.png")
    repeat_mode = False  # Initial state of repeat mode
    repeat_button = tk.Button(bottom_frame, image=repeat_off_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                              activeforeground='white', activebackground='white', cursor='hand2', command=toggle_repeat)
    repeat_button.place(x=260, y=30)

    low_frame = tk.Frame(hindi_window, bg='black')
    low_frame.place(relx=0, rely=0.85, relwidth=1, relheight=1)

    border_frame = tk.Frame(hindi_window, bg='white', height=2)  # Adjust height as needed
    border_frame.place(relx=0, rely=0.85, relwidth=1)

    # Create a progress bar
    progress = ttk.Progressbar(hindi_window, orient='horizontal', mode='determinate', length=1200,
                               style="Custom.Horizontal.TProgressbar")
    progress.place(relx=0.1, rely=0.9)

    progress_bar_color = 'green'
    # Define a custom style for the progress bar
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Custom.Horizontal.TProgressbar", troughcolor=frame_bg, background=progress_bar_color)

    # Label to display time information
    label_time = tk.Label(low_frame, text="", bg='black', fg=frame_fg, font=('Arial', 12))
    label_time.place(relx=0.89, rely=0.049)

    def volume(x):
        pygame.mixer.music.set_volume(slider.get())
        slider.place(relx=0.072, rely=0.76)

    def toggle_slider():
        slider.place(relx=0.072, rely=0.76)

    image_vol = tk.PhotoImage(file='./assets/sound.png')
    slider_button = tk.Button(low_frame, image=image_vol, font=('Arial', 12), fg='white', bg='purple',
                              activeforeground='white', activebackground='purple', cursor='hand2',
                              command=toggle_slider)
    slider_button.place(relx=0.07, rely=0.044)

    slider = ttk.Scale(hindi_window, from_=0, to=1, orient=tk.VERTICAL,
                       value=1, length=100, command=volume)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Vertical.TScale", background="purple", troughcolor="black", sliderlength=30)

    def play_selected_song():
        mixer.music.load(song_list[current_song_index])
        mixer.music.play(loops=0)
        get_time()

    repeat_img = tk.PhotoImage(file='./assets/onrepeat.png')
    button_repeat = tk.Button(low_frame, image=repeat_img, bg=background, fg='black', activebackground='black',
                              command=play_selected_song)
    button_repeat.place(relx=0.8, rely=0.07)

    def pause_unpause():
        global paused
        if paused:
            mixer.music.unpause()
            paused = False
            button_pause.config(image=pause_img)  # Change button image to pause image
        else:
            mixer.music.pause()
            paused = True
            button_pause.config(image=play_img)  # Change button image to play image

    paused = False  # Initial state of music playback

    pause_img = tk.PhotoImage(file='./assets/pause.png')
    play_img = tk.PhotoImage(file='./assets/play2.png')
    button_pause = tk.Button(low_frame, image=pause_img, width=4, bd=5,
                             font="Helvetica, 15", bg="purple", fg="white", command=pause_unpause)
    button_pause.place(relx=0.5, rely=0.07, relwidth=0.04, relheight=0.075)

    button_play = tk.Button(low_frame, image=play_img, width=4, bd=5,
                            font="Helvetica, 15", bg="black", fg="white", command=pause_unpause)

    current_song_index = 0  # Initialize the current song index

    def next_song():
        global current_song_index
        current_song_index = (current_song_index + 1) % len(song_list)
        play_selected_song()
        song_listbox.selection_clear(0, tk.END)  # Clear previous selection
        song_listbox.selection_set(current_song_index)  # Set selection to the next song
        song_listbox.see(current_song_index)

    def prev_song():
        global current_song_index
        current_song_index = (current_song_index - 1) % len(song_list)
        play_selected_song()
        song_listbox.selection_clear(0, tk.END)  # Clear previous selection
        song_listbox.selection_set(current_song_index)  # Set selection to the previous song
        song_listbox.see(current_song_index)

    def play_selected_song():
        mixer.music.load(song_list[current_song_index])
        mixer.music.play(loops=0)
        get_time()

    prev_img = tk.PhotoImage(file='./assets/previous.png')
    next_img = tk.PhotoImage(file='./assets/next.png')

    button_prev = tk.Button(low_frame, image=prev_img, bg=background, command=prev_song)
    button_prev.place(relx=0.45, rely=0.071)

    button_next = tk.Button(low_frame, image=next_img, bg=background, command=next_song)
    button_next.place(relx=0.55, rely=0.071)

    # Button for navigation

    # Voice assistant functions

    def listen_for_command():
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening for commands...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except sr.RequestError:
            print("Unable to access the Google Speech Recognition API.")
            return None

    def process_command(command):
        global tasks, listeningToTask

        if command:
            if "play music" in command:
                play_music()
            elif "pause music" in command:
                pause_unpause()
            elif "next song" in command:
                next_song()
            elif "previous song" in command:
                prev_song()
            elif "stop music" in command:
                mixer.music.stop()
            elif "shuffle playlist" in command:
                shuffle_playlist_and_play()
            elif "repeat mode" in command:
                toggle_repeat()

            elif "volume up" in command:
                increase_volume()
            elif "volume down" in command:
                decrease_volume()





            elif "exit" in command:
                main_window.destroy()
            else:
                tasks.append(command)
                if not listeningToTask:
                    listeningToTask = True
                    listen_to_task()

    def listen_to_task():
        global tasks, listeningToTask

        if tasks:
            task = tasks.pop(0)
            process_command(task)  # Execute the task directly without audio output
            listeningToTask = False
        else:
            listeningToTask = False
            print("No tasks to perform")

    def speak(text):
        tts = gTTS(text=text, lang='en')
        tts.save("assistant_audio.mp3")
        sound = AudioSegment.from_mp3("assistant_audio.mp3")
        sound.export("assistant_audio.wav", format="wav")
        winsound.PlaySound("assistant_audio.wav", winsound.SND_FILENAME)
        os.remove("assistant_audio.mp3")
        os.remove("assistant_audio.wav")
    
    def increase_volume():
        current_volume = mixer.music.get_volume()
        if current_volume < 1.0:
            new_volume = min(current_volume + 0.6, 1.0)
            mixer.music.set_volume(new_volume)

    def decrease_volume():
        current_volume = mixer.music.get_volume()
        if current_volume > 0.0:
            new_volume = max(current_volume - 0.6, 0.0)
            mixer.music.set_volume(new_volume)
            
    def assistant_task_listener():
        while True:
            command = listen_for_command()
            process_command(command)

    # Start the assistant task listener in a separate thread
    assistant_thread = threading.Thread(target=assistant_task_listener)
    assistant_thread.daemon = True
    assistant_thread.start()

    hindi_window.mainloop()


def open_sad():
    sad_window = tk.Toplevel()
    sad_window.title("Sad Songs page")
    sad_window.geometry('1250x700')
    sad_window.configure(bg='purple')

    pygame.mixer.init()

    global current_song_index, paused, repeat_mode

    current_song_index = 0  # Initialize current song index
    paused = False
    repeat_mode = False

    background = "purple"
    frame_bg = "#000000"  # Black background color for the frame
    frame_fg = "#FFFFFF"  # White foreground color for the frame

    # Assuming you have an image file named 'example_image.png' in the same directory
    image_path = "./assets/arijit2.png"
    image = tk.PhotoImage(file=image_path)
    image_label = tk.Label(sad_window, image=image, bg=background)
    image_label.place(relx=0.1, rely=0.11)

    pop_label = tk.Label(sad_window, text="Sad Songs", font=('Arial', 42, 'bold'), background=background,
                         foreground='white')
    pop_label.place(relx=0.42, rely=0.22)

    bottom_frame = tk.Frame(sad_window, bg=frame_bg)
    bottom_frame.place(relx=0, rely=0.35, relwidth=1, relheight=1)

    # List of songs
    song_list = [
        "./music/Channa Mereya Full Video - ADHMRanbir Kapoor, AnushkaArijit SinghPritamKaran Johar.mp3",
        "./music/Agar Tum Saath Ho FULL AUDIO Song  Tamasha  Ranbir Kapoor, Deepika Padukone  T-Series.mp3",
        "./music/Raabta Title Song (Full Video)  Deepika Padukone, Sushant Singh Rajput, Kriti Sanon  Pritam, Jam 8.mp3",
        "./music/Janam Janam  Dilwale  Shah Rukh Khan  Kajol  Pritam  SRK  Kajol  Lyric Video 2015.mp3"
        # Add more songs here
    ]

    # Create a Listbox to display the list of songs
    song_listbox = tk.Listbox(bottom_frame, bg=frame_bg, fg=frame_fg, font=('Arial', 14), selectbackground="purple",
                              selectforeground="white")
    song_listbox.place(x=100, y=100, width=1300, height=370)
    for song in song_list:
        song_listbox.insert(tk.END, os.path.basename(song))  # Display only the filename, not the full path

    def play_music():
        selected_song_index = song_listbox.curselection()
        if selected_song_index:
            song_path = song_list[selected_song_index[0]]
            mixer.music.load(song_path)
            mixer.music.play(loops=0)

    # Bind the play_music function to handle the selection event in the listbox
    song_listbox.bind('<<ListboxSelect>>', lambda event: play_music())

    play_image = tk.PhotoImage(file="./assets/play.png")
    play_button = tk.Button(bottom_frame, image=play_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                            activeforeground='white', activebackground='#3C3C3C', cursor='hand2', command=play_music)
    play_button.place(x=100, y=30)

    def get_time():
        current_time = pygame.mixer.music.get_pos() / 1000
        formatted_current_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
        selected_song_index = song_listbox.curselection()
        if selected_song_index:
            song_length = int(MP3(song_list[selected_song_index[0]]).info.length)
            formatted_song_length = time.strftime("%H:%M:%S", time.gmtime(song_length))
            label_time.config(text=f"{formatted_song_length} / {formatted_current_time}")
            progress["maximum"] = song_length
            progress["value"] = int(current_time)
        sad_window.after(100, get_time)

    # Define a function to shuffle the playlist
    def shuffle_playlist_and_play():
        random.shuffle(song_list)
        song_listbox.delete(0, tk.END)
        for song in song_list:
            song_listbox.insert(tk.END, os.path.basename(song))
        play_selected_song()

    shuffle_image = tk.PhotoImage(file="./assets/shuffle.png")
    shuffle_button = tk.Button(bottom_frame, image=shuffle_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                               activeforeground='white', activebackground='white', cursor='hand2',
                               command=shuffle_playlist_and_play)
    shuffle_button.place(x=180, y=33)

    # Define a function to toggle repeat mode
    def toggle_repeat():
        global repeat_mode
        repeat_mode = not repeat_mode
        if repeat_mode:
            repeat_button.config(image=repeat_on_image)
        else:
            repeat_button.config(image=repeat_off_image)

    # Create a button to toggle repeat mode
    repeat_off_image = tk.PhotoImage(file="./assets/next.png")
    repeat_on_image = tk.PhotoImage(file="./assets/onrepeat.png")
    repeat_mode = False  # Initial state of repeat mode
    repeat_button = tk.Button(bottom_frame, image=repeat_off_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                              activeforeground='white', activebackground='white', cursor='hand2', command=toggle_repeat)
    repeat_button.place(x=260, y=30)

    low_frame = tk.Frame(sad_window, bg='black')
    low_frame.place(relx=0, rely=0.85, relwidth=1, relheight=1)

    border_frame = tk.Frame(sad_window, bg='white', height=2)  # Adjust height as needed
    border_frame.place(relx=0, rely=0.85, relwidth=1)

    # Create a progress bar
    progress = ttk.Progressbar(sad_window, orient='horizontal', mode='determinate', length=1200,
                               style="Custom.Horizontal.TProgressbar")
    progress.place(relx=0.1, rely=0.9)

    progress_bar_color = 'green'
    # Define a custom style for the progress bar
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Custom.Horizontal.TProgressbar", troughcolor=frame_bg, background=progress_bar_color)

    # Label to display time information
    label_time = tk.Label(low_frame, text="", bg='black', fg=frame_fg, font=('Arial', 12))
    label_time.place(relx=0.89, rely=0.049)

    def volume(x):
        pygame.mixer.music.set_volume(slider.get())
        slider.place(relx=0.072, rely=0.76)

    def toggle_slider():
        slider.place(relx=0.072, rely=0.76)

    image_vol = tk.PhotoImage(file='./assets/sound.png')
    slider_button = tk.Button(low_frame, image=image_vol, font=('Arial', 12), fg='white', bg='purple',
                              activeforeground='white', activebackground='purple', cursor='hand2',
                              command=toggle_slider)
    slider_button.place(relx=0.07, rely=0.044)

    slider = ttk.Scale(sad_window, from_=0, to=1, orient=tk.VERTICAL,
                       value=1, length=100, command=volume)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Vertical.TScale", background="purple", troughcolor="black", sliderlength=30)

    def play_selected_song():
        mixer.music.load(song_list[current_song_index])
        mixer.music.play(loops=0)
        get_time()

    repeat_img = tk.PhotoImage(file='./assets/onrepeat.png')
    button_repeat = tk.Button(low_frame, image=repeat_img, bg=background, fg='black', activebackground='black',
                              command=play_selected_song)
    button_repeat.place(relx=0.8, rely=0.07)

    def pause_unpause():
        global paused
        if paused:
            mixer.music.unpause()
            paused = False
            button_pause.config(image=pause_img)  # Change button image to pause image
        else:
            mixer.music.pause()
            paused = True
            button_pause.config(image=play_img)  # Change button image to play image

    paused = False  # Initial state of music playback

    pause_img = tk.PhotoImage(file='./assets/pause.png')
    play_img = tk.PhotoImage(file='./assets/play2.png')
    button_pause = tk.Button(low_frame, image=pause_img, width=4, bd=5,
                             font="Helvetica, 15", bg="purple", fg="white", command=pause_unpause)
    button_pause.place(relx=0.5, rely=0.07, relwidth=0.04, relheight=0.075)

    button_play = tk.Button(low_frame, image=play_img, width=4, bd=5,
                            font="Helvetica, 15", bg="black", fg="white", command=pause_unpause)

    current_song_index = 0  # Initialize the current song index

    def next_song():
        global current_song_index
        current_song_index = (current_song_index + 1) % len(song_list)
        play_selected_song()
        song_listbox.selection_clear(0, tk.END)  # Clear previous selection
        song_listbox.selection_set(current_song_index)  # Set selection to the next song
        song_listbox.see(current_song_index)

    def prev_song():
        global current_song_index
        current_song_index = (current_song_index - 1) % len(song_list)
        play_selected_song()
        song_listbox.selection_clear(0, tk.END)  # Clear previous selection
        song_listbox.selection_set(current_song_index)  # Set selection to the previous song
        song_listbox.see(current_song_index)

    def play_selected_song():
        mixer.music.load(song_list[current_song_index])
        mixer.music.play(loops=0)
        get_time()

    prev_img = tk.PhotoImage(file='./assets/previous.png')
    next_img = tk.PhotoImage(file='./assets/next.png')

    button_prev = tk.Button(low_frame, image=prev_img, bg=background, command=prev_song)
    button_prev.place(relx=0.45, rely=0.071)

    button_next = tk.Button(low_frame, image=next_img, bg=background, command=next_song)
    button_next.place(relx=0.55, rely=0.071)

    # Button for navigation

    # Voice assistant functions

    def listen_for_command():
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening for commands...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except sr.RequestError:
            print("Unable to access the Google Speech Recognition API.")
            return None

    def process_command(command):
        global tasks, listeningToTask

        if command:
            if "play music" in command:
                play_music()
            elif "pause music" in command:
                pause_unpause()
            elif "next song" in command:
                next_song()
            elif "previous song" in command:
                prev_song()
            elif "stop music" in command:
                mixer.music.stop()
            elif "shuffle playlist" in command:
                shuffle_playlist_and_play()
            elif "repeat mode" in command:
                toggle_repeat()

            elif "volume up" in command:
                increase_volume()
            elif "volume down" in command:
                decrease_volume()





            elif "exit" in command:
                main_window.destroy()
            else:
                tasks.append(command)
                if not listeningToTask:
                    listeningToTask = True
                    listen_to_task()

    def listen_to_task():
        global tasks, listeningToTask

        if tasks:
            task = tasks.pop(0)
            process_command(task)  # Execute the task directly without audio output
            listeningToTask = False
        else:
            listeningToTask = False
            print("No tasks to perform")

    def speak(text):
        tts = gTTS(text=text, lang='en')
        tts.save("assistant_audio.mp3")
        sound = AudioSegment.from_mp3("assistant_audio.mp3")
        sound.export("assistant_audio.wav", format="wav")
        winsound.PlaySound("assistant_audio.wav", winsound.SND_FILENAME)
        os.remove("assistant_audio.mp3")
        os.remove("assistant_audio.wav")
    
    def increase_volume():
        current_volume = mixer.music.get_volume()
        if current_volume < 1.0:
            new_volume = min(current_volume + 0.6, 1.0)
            mixer.music.set_volume(new_volume)

    def decrease_volume():
        current_volume = mixer.music.get_volume()
        if current_volume > 0.0:
            new_volume = max(current_volume - 0.6, 0.0)
            mixer.music.set_volume(new_volume)
            
    def assistant_task_listener():
        while True:
            command = listen_for_command()
            process_command(command)

    # Start the assistant task listener in a separate thread
    assistant_thread = threading.Thread(target=assistant_task_listener)
    assistant_thread.daemon = True
    assistant_thread.start()

    sad_window.mainloop()


def open_eighty():
    eighty_window = tk.Toplevel()
    eighty_window.title("80's Songs")
    eighty_window.geometry('1250x700')
    eighty_window.configure(bg='purple')

    pygame.mixer.init()

    global current_song_index, paused, repeat_mode

    current_song_index = 0  # Initialize current song index
    paused = False
    repeat_mode = False

    background = "purple"
    frame_bg = "#000000"  # Black background color for the frame
    frame_fg = "#FFFFFF"  # White foreground color for the frame

    # Assuming you have an image file named 'example_image.png' in the same directory
    image_path = "./assets/lata.png"
    image = tk.PhotoImage(file=image_path)
    image_label = tk.Label(eighty_window, image=image, bg=background)
    image_label.place(relx=0.1, rely=0.15)

    pop_label = tk.Label(eighty_window, text="80's Top Hits", font=('Arial', 42, 'bold'), background=background,
                         foreground='white')
    pop_label.place(relx=0.42, rely=0.22)

    bottom_frame = tk.Frame(eighty_window, bg=frame_bg)
    bottom_frame.place(relx=0, rely=0.35, relwidth=1, relheight=1)

    # List of songs
    song_list = [
        "./music/Tumhari Sulu_  Hawa Hawai 2.0 Video Song  Vidya Balan  Vidya Balan, Neha Dhupia & Malishka.mp3",
        "./music/Aye Zindagi Gale Laga Le  Suresh Wadkar  Sadma 1983 Songs  Sridevi, Kamal Haasan.mp3",
        "./music/Papa Kehte Hain Bada Naam Karega -Video Song  Qayamat Se Qayamat Tak  Udit Narayan  Aamir Khan.mp3"
        # Add more songs here
    ]

    # Create a Listbox to display the list of songs
    song_listbox = tk.Listbox(bottom_frame, bg=frame_bg, fg=frame_fg, font=('Arial', 14), selectbackground="purple",
                              selectforeground="white")
    song_listbox.place(x=100, y=100, width=1300, height=370)
    for song in song_list:
        song_listbox.insert(tk.END, os.path.basename(song))  # Display only the filename, not the full path

    def play_music():
        selected_song_index = song_listbox.curselection()
        if selected_song_index:
            song_path = song_list[selected_song_index[0]]
            mixer.music.load(song_path)
            mixer.music.play(loops=0)

    # Bind the play_music function to handle the selection event in the listbox
    song_listbox.bind('<<ListboxSelect>>', lambda event: play_music())

    play_image = tk.PhotoImage(file="./assets/play.png")
    play_button = tk.Button(bottom_frame, image=play_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                            activeforeground='white', activebackground='#3C3C3C', cursor='hand2', command=play_music)
    play_button.place(x=100, y=30)

    def get_time():
        current_time = pygame.mixer.music.get_pos() / 1000
        formatted_current_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
        selected_song_index = song_listbox.curselection()
        if selected_song_index:
            song_length = int(MP3(song_list[selected_song_index[0]]).info.length)
            formatted_song_length = time.strftime("%H:%M:%S", time.gmtime(song_length))
            label_time.config(text=f"{formatted_song_length} / {formatted_current_time}")
            progress["maximum"] = song_length
            progress["value"] = int(current_time)
        eighty_window.after(100, get_time)

    # Define a function to shuffle the playlist
    def shuffle_playlist_and_play():
        random.shuffle(song_list)
        song_listbox.delete(0, tk.END)
        for song in song_list:
            song_listbox.insert(tk.END, os.path.basename(song))
        play_selected_song()

    shuffle_image = tk.PhotoImage(file="./assets/shuffle.png")
    shuffle_button = tk.Button(bottom_frame, image=shuffle_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                               activeforeground='white', activebackground='white', cursor='hand2',
                               command=shuffle_playlist_and_play)
    shuffle_button.place(x=180, y=33)

    # Define a function to toggle repeat mode
    def toggle_repeat():
        global repeat_mode
        repeat_mode = not repeat_mode
        if repeat_mode:
            repeat_button.config(image=repeat_on_image)
        else:
            repeat_button.config(image=repeat_off_image)

    # Create a button to toggle repeat mode
    repeat_off_image = tk.PhotoImage(file="./assets/next.png")
    repeat_on_image = tk.PhotoImage(file="./assets/onrepeat.png")
    repeat_mode = False  # Initial state of repeat mode
    repeat_button = tk.Button(bottom_frame, image=repeat_off_image, font=('Arial', 20, 'bold'), fg='white', bg='purple',
                              activeforeground='white', activebackground='white', cursor='hand2', command=toggle_repeat)
    repeat_button.place(x=260, y=30)

    low_frame = tk.Frame(eighty_window, bg='black')
    low_frame.place(relx=0, rely=0.85, relwidth=1, relheight=1)

    border_frame = tk.Frame(eighty_window, bg='white', height=2)  # Adjust height as needed
    border_frame.place(relx=0, rely=0.85, relwidth=1)

    # Create a progress bar
    progress = ttk.Progressbar(eighty_window, orient='horizontal', mode='determinate', length=1200,
                               style="Custom.Horizontal.TProgressbar")
    progress.place(relx=0.1, rely=0.9)

    progress_bar_color = 'green'
    # Define a custom style for the progress bar
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Custom.Horizontal.TProgressbar", troughcolor=frame_bg, background=progress_bar_color)

    # Label to display time information
    label_time = tk.Label(low_frame, text="", bg='black', fg=frame_fg, font=('Arial', 12))
    label_time.place(relx=0.89, rely=0.049)

    def volume(x):
        pygame.mixer.music.set_volume(slider.get())
        slider.place(relx=0.072, rely=0.76)

    def toggle_slider():
        slider.place(relx=0.072, rely=0.76)

    image_vol = tk.PhotoImage(file='./assets/sound.png')
    slider_button = tk.Button(low_frame, image=image_vol, font=('Arial', 12), fg='white', bg='purple',
                              activeforeground='white', activebackground='purple', cursor='hand2',
                              command=toggle_slider)
    slider_button.place(relx=0.07, rely=0.044)

    slider = ttk.Scale(eighty_window, from_=0, to=1, orient=tk.VERTICAL,
                       value=1, length=100, command=volume)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Vertical.TScale", background="purple", troughcolor="black", sliderlength=30)

    def play_selected_song():
        mixer.music.load(song_list[current_song_index])
        mixer.music.play(loops=0)
        get_time()

    repeat_img = tk.PhotoImage(file='./assets/onrepeat.png')
    button_repeat = tk.Button(low_frame, image=repeat_img, bg=background, fg='black', activebackground='black',
                              command=play_selected_song)
    button_repeat.place(relx=0.8, rely=0.07)

    def pause_unpause():
        global paused
        if paused:
            mixer.music.unpause()
            paused = False
            button_pause.config(image=pause_img)  # Change button image to pause image
        else:
            mixer.music.pause()
            paused = True
            button_pause.config(image=play_img)  # Change button image to play image

    paused = False  # Initial state of music playback

    pause_img = tk.PhotoImage(file='./assets/pause.png')
    play_img = tk.PhotoImage(file='./assets/play2.png')
    button_pause = tk.Button(low_frame, image=pause_img, width=4, bd=5,
                             font="Helvetica, 15", bg="purple", fg="white", command=pause_unpause)
    button_pause.place(relx=0.5, rely=0.07, relwidth=0.04, relheight=0.075)

    button_play = tk.Button(low_frame, image=play_img, width=4, bd=5,
                            font="Helvetica, 15", bg="black", fg="white", command=pause_unpause)

    current_song_index = 0  # Initialize the current song index

    def next_song():
        global current_song_index
        current_song_index = (current_song_index + 1) % len(song_list)
        play_selected_song()
        song_listbox.selection_clear(0, tk.END)  # Clear previous selection
        song_listbox.selection_set(current_song_index)  # Set selection to the next song
        song_listbox.see(current_song_index)

    def prev_song():
        global current_song_index
        current_song_index = (current_song_index - 1) % len(song_list)
        play_selected_song()
        song_listbox.selection_clear(0, tk.END)  # Clear previous selection
        song_listbox.selection_set(current_song_index)  # Set selection to the previous song
        song_listbox.see(current_song_index)

    def play_selected_song():
        mixer.music.load(song_list[current_song_index])
        mixer.music.play(loops=0)
        get_time()

    prev_img = tk.PhotoImage(file='./assets/previous.png')
    next_img = tk.PhotoImage(file='./assets/next.png')

    button_prev = tk.Button(low_frame, image=prev_img, bg=background, command=prev_song)
    button_prev.place(relx=0.45, rely=0.071)

    button_next = tk.Button(low_frame, image=next_img, bg=background, command=next_song)
    button_next.place(relx=0.55, rely=0.071)

    # Button for navigation

    # Voice assistant functions

    def listen_for_command():
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening for commands...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except sr.RequestError:
            print("Unable to access the Google Speech Recognition API.")
            return None

    def process_command(command):
        global tasks, listeningToTask

        if command:
            if "play music" in command:
                play_music()
            elif "pause music" in command:
                pause_unpause()
            elif "next song" in command:
                next_song()
            elif "previous song" in command:
                prev_song()
            elif "stop music" in command:
                mixer.music.stop()
            elif "shuffle playlist" in command:
                shuffle_playlist_and_play()
            elif "repeat mode" in command:
                toggle_repeat()

            elif "volume up" in command:
                increase_volume()
            elif "volume down" in command:
                decrease_volume()





            elif "exit" in command:
                main_window.destroy()
            else:
                tasks.append(command)
                if not listeningToTask:
                    listeningToTask = True
                    listen_to_task()

    def listen_to_task():
        global tasks, listeningToTask

        if tasks:
            task = tasks.pop(0)
            process_command(task)  # Execute the task directly without audio output
            listeningToTask = False
        else:
            listeningToTask = False
            print("No tasks to perform")

    def speak(text):
        tts = gTTS(text=text, lang='en')
        tts.save("assistant_audio.mp3")
        sound = AudioSegment.from_mp3("assistant_audio.mp3")
        sound.export("assistant_audio.wav", format="wav")
        winsound.PlaySound("assistant_audio.wav", winsound.SND_FILENAME)
        os.remove("assistant_audio.mp3")
        os.remove("assistant_audio.wav")
    
    def increase_volume():
        current_volume = mixer.music.get_volume()
        if current_volume < 1.0:
            new_volume = min(current_volume + 0.6, 1.0)
            mixer.music.set_volume(new_volume)

    def decrease_volume():
        current_volume = mixer.music.get_volume()
        if current_volume > 0.0:
            new_volume = max(current_volume - 0.6, 0.0)
            mixer.music.set_volume(new_volume)
            
    def assistant_task_listener():
        while True:
            command = listen_for_command()
            process_command(command)

    # Start the assistant task listener in a separate thread
    assistant_thread = threading.Thread(target=assistant_task_listener)
    assistant_thread.daemon = True
    assistant_thread.start()

    eighty_window.mainloop()

def playlist_Button():
    song_list = [
        './music/The Weeknd, Ariana Grande - Die For You (Remix - Lyric Video).mp3',
        './music/Kanye West - Heartless.mp3',
        './music/superman.mp3'
    ]

    def add_to_playlist(file_path, playlist_window): 
        playlist_window.deiconify()
        selected_playlist = playlist_listbox.curselection()
        if not selected_playlist:
            
            return
        playlist_name = playlist_listbox.get(selected_playlist)
        if playlist_name in playlists:
            playlists[playlist_name].append(file_path)
        save_playlists()
        update_playlist_buttons()

    def play_audio(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

    def pause_audio():
        pygame.mixer.music.pause()

    def shuffle_play():
        random.shuffle(song_list)
        for file_path in song_list:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
        else:
            tk.messagebox.showinfo("No Files", "Please add files before shuffling.")

    def save_files():
        with open('files.pkl', 'wb') as f:
            pickle.dump(song_list, f)

    def load_files():
        try:
            with open('files.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []

    def create_playlist():
        playlist_name = playlist_name_entry.get()
        if playlist_name:
            if playlist_name in playlists:
                tk.messagebox.showinfo("Existing Playlist", "Playlist with the same name already exists. Please choose a different name.")
            else:
                playlists[playlist_name] = []
                save_playlists()
                update_playlist_buttons()
                playlist_name_entry.delete(0, tk.END)
                playlist_window.withdraw()
        else:
            tk.messagebox.showinfo("Empty Name", "Please enter a name for the playlist.")

    def delete_playlist():
        selected_playlist_index = playlist_listbox.curselection()
        if selected_playlist_index:
            playlist_name = playlist_listbox.get(selected_playlist_index)
            del playlists[playlist_name]
            save_playlists()
            update_playlist_buttons()

    def save_playlists():
        with open('playlists.pkl', 'wb') as f:
            pickle.dump(playlists, f)

    def load_playlists():
        try:
            with open('playlists.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def open_playlist(event):
        selected_playlist_index = playlist_listbox.curselection()
        if selected_playlist_index:
            playlist_name = playlist_listbox.get(selected_playlist_index)
            playlist_files = playlists[playlist_name]
            playlist_window = tk.Toplevel(root)
            playlist_window.title(playlist_name)
            playlist_window.geometry("400x400")
            playlist_window.configure(bg="purple")

            playlist_frame = tk.Frame(playlist_window, bg="purple")
            playlist_frame.pack(pady=10)

            for file_path in playlist_files:
                file_label = tk.Label(playlist_frame, text=os.path.basename(file_path), bg="white", fg="black")
                file_label.pack(side="left", padx=5, pady=5)
                play_button = tk.Button(playlist_frame, text='Play', bd=0, bg='gray90', fg='SlateBlue1', activebackground='gray90', cursor='hand2', command=lambda f=file_path: play_audio(f))
                play_button.pack(side="left", padx=2)

            # Button to pause audio
            pause_button = tk.Button(playlist_window, text='Pause', bd=0, bg='gray90', fg='SlateBlue1', activebackground='gray90', cursor='hand2', command=pause_audio)
            pause_button.pack(side="left", padx=2)

            # Button to shuffle and play files
            shuffle_button = tk.Button(playlist_window, text='Shuffle', bd=0, bg='gray90', fg='SlateBlue1', activebackground='gray90', cursor='hand2', command=shuffle_play)
            shuffle_button.pack(side="left", padx=2)

    def update_playlist_buttons():
        playlist_listbox.delete(0, tk.END)
        for playlist_name in playlists:
            playlist_listbox.insert(tk.END, playlist_name)

    # Load existing playlists
    playlists = load_playlists()

    # Create the main window
    root = tk.Tk()
    root.title('Playlists')
    root.geometry('800x800')

    # Create a frame to hold the files
    file_frame = tk.Frame(root, bg="purple")
    file_frame.pack(pady=2,expand=True,fill=tk.BOTH)

    # Display all songs from song_list
    for file_path in song_list:
        if file_path.lower().endswith(('.mp3', '.wav', '.ogg')):
            file_label = tk.Label(file_frame, text=os.path.basename(file_path), bg="white", fg="black",font=40)
            file_label.pack(side="top", padx=40, pady=40)
            add_to_playlist_button = tk.Button(file_frame, text="Add to Playlist", command=lambda f=file_path: add_to_playlist(f, playlist_window),font=20) 
            add_to_playlist_button.pack(side="top", padx=40)

    # Create playlist window
    playlist_window = tk.Toplevel(root)
    playlist_window.title("Playlists")
    playlist_window.geometry("800x800")
    playlist_window.configure(bg="purple")
    playlist_window.withdraw()  # Hide the playlist window initially

    # Listbox to display playlists
    playlist_listbox = tk.Listbox(playlist_window, bg="white", fg="black")
    playlist_listbox.pack(expand=True, fill=tk.BOTH)

    # Bind double click event to open playlist
    playlist_listbox.bind("<Double-Button-1>", open_playlist)

    # Button to create new playlist
    create_playlist_button = tk.Button(playlist_window, text="Create Playlist", command=create_playlist)
    create_playlist_button.pack(side="bottom", pady=5)

    # Entry to input playlist name
    playlist_name_entry = tk.Entry(playlist_window)
    playlist_name_entry.pack(side="bottom", pady=5)

    # Button to delete playlist
    delete_playlist_button = tk.Button(playlist_window, text="Delete Playlist", command=delete_playlist)
    delete_playlist_button.pack(side="bottom", pady=5)

    # Run the Tkinter event loop
    root.mainloop()










bgLabel = Label(main_window, image=background_image)
bgLabel.place(x=0, y=0)

playlistButton = Button(main_window, text='Playlist', bd=0, bg='white', fg='SlateBlue1', activebackground='white',
                        cursor='hand2',command=playlist_Button, font=('Microsoft Yahei UI Light', 22, 'bold'))
playlistButton.place(x=95, y=112)


def karaoke_Button():
    def parse_lrc_file(lrc_file):
        lyrics = []
        with open(lrc_file, 'r') as file:
            for line in file:
                if line.strip():
                    line = line.strip()
                    parts = line.split(']')
                    timestamp = parts[0][1:]
                    lyric = parts[1]
                    lyrics.append((timestamp, lyric))
        return lyrics

    def display_lyrics(lyrics, start_time):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()

        current_lyric_index = 0

        while current_lyric_index < len(lyrics):
            current_time = datetime.now()
            elapsed_time = current_time - start_time

            # Parse the timestamp from the lyrics file
            lyric_timestamp = datetime.strptime(lyrics[current_lyric_index][0], '%M:%S.%f')

            # Check if it's time to display the next lyric
            if elapsed_time.total_seconds() >= lyric_timestamp.second + lyric_timestamp.microsecond / 1000000:
                screen.fill((255, 255, 255))
                text = font.render(lyrics[current_lyric_index][1], True, (0, 0, 0))
                text_rect = text.get_rect(center=(400, 300))
                screen.blit(text, text_rect)
                pygame.display.flip()
                current_lyric_index += 1

            pygame.event.pump()  # Process events to avoid freezing
            clock.tick(10)

    def play_music(song_index, songs):
        song, lrc_file = songs[song_index]
        start_time = datetime.now() 
        pygame.mixer.init()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()

        threading.Thread(target=display_lyrics, args=(parse_lrc_file(lrc_file), start_time)).start()

    def record_microphone_audio(duration, filename):
        print("Recording microphone audio...")
        fs = 44100  # Sample rate

        # Start recording microphone audio only
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype=np.int16)

        # Wait for the recording to complete
        sd.wait()

        # Save the recording to file with a unique timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename = f"{filename}_{timestamp}.wav"
        wav.write(output_filename, fs, recording)
        
        print("Recording finished. Saved as:", output_filename)

    def run_music_and_record(song_index, songs, duration, microphone_filename):
        start_time = datetime.now()
        music_thread = threading.Thread(target=play_music, args=(song_index, songs))
        record_thread = threading.Thread(target=record_microphone_audio, args=(duration, microphone_filename))

        music_thread.start()
        record_thread.start()

        music_thread.join()
        record_thread.join()

    def pause_music():
        pygame.mixer.music.pause()

    filename1='./instrumental/Heartless (ins).mp3'
    def play_audio(filename1, filename2):
        pygame.mixer.init()

        # Load audio files
        sound1 = pygame.mixer.Sound(filename1)
        sound2 = pygame.mixer.Sound(filename2)

        # Play audio files simultaneously
        channel1 = sound1.play()
        channel2 = sound2.play()


    file_die1='./instrumental/dieforyou(inst).mp3'
    def play_audio(file_die1, file_die2):
        pygame.mixer.init()

        # Load audio files
        sound1 = pygame.mixer.Sound(file_die1)
        sound2 = pygame.mixer.Sound(file_die2)

        # Play audio files simultaneously
        channel1 = sound1.play()
        channel2 = sound2.play()


    file_tu='./instrumental/Tu jaane na(ins).mp3'
    def play_audio(file_tu, file_tu1):
        pygame.mixer.init()

        # Load audio files
        sound1 = pygame.mixer.Sound(file_tu)
        sound2 = pygame.mixer.Sound(file_tu1)

        # Play audio files simultaneously
        channel1 = sound1.play()
        channel2 = sound2.play()


    file_kabhi1='./instrumental/Kabhi Kabhi Aditi (ins).mp3'
    def play_audio(file_kabhi1, file_kabhi2):
        pygame.mixer.init()

        # Load audio files
        sound1 = pygame.mixer.Sound(file_kabhi1)
        sound2 = pygame.mixer.Sound(file_kabhi2)

        # Play audio files simultaneously
        channel1 = sound1.play()
        channel2 = sound2.play()

    def main():
        def set_background_image(root):
            bgImage= tk.PhotoImage(file='karaokegui.png')

            bgLabel=tk.Label(root,image=bgImage)
            bgLabel.place(x=0,y=0,relwidth=1,relheight=1)

            root = tk.Tk()
            root.title("Song Player")
            
            set_background_image(root)

            #root.configure(bg='purple')

            # Function to select filename2
            def select_filename2():
                root.filename2 = filedialog.askopenfilename(initialdir="/Desktop", title="Select Instrumental File")
                label_filename2.config(text=root.filename2)

            def select_file_die2():
                root.file_die2 = filedialog.askopenfilename(initialdir="/Desktop", title="Select Instrumental File")
                label_filename2.config(text=root.file_die2)

            def select_file_tu1():
                root.file_tu1 = filedialog.askopenfilename(initialdir="/Desktop", title="Select Instrumental File")
                label_filename2.config(text=root.file_tu1)

            def select_file_kabhi2():
                root.file_kabhi2 = filedialog.askopenfilename(initialdir="/Desktop", title="Select Instrumental File")
                label_filename2.config(text=root.file_kabhi2)

            # GUI elements
            label_filename2 = tk.Label(root, text="Select instrumental file:")
            label_filename2.grid(row=0, column=0, padx=5, pady=5)

            button_filename2 = tk.Button(root, text="Select", command=select_filename2)
            button_filename2.grid(row=1, column=7, padx=5, pady=5)

            button_file_die2 = tk.Button(root, text="Select", command=select_file_die2)
            button_file_die2.grid(row=2, column=7, padx=5, pady=5)

            button_file_tu1 = tk.Button(root, text="Select", command=select_file_tu1)
            button_file_tu1.grid(row=3, column=7, padx=5, pady=5)

            button_file_tu1 = tk.Button(root, text="Select", command=select_file_kabhi2)
            button_file_tu1.grid(row=4, column=7, padx=5, pady=5)

            songs = [
                ("./instrumental/Heartless (ins).mp3", "./lyrics/Heartless.lrc"),
                ("./instrumental/dieforyou(inst).mp3","./lyrics/Die for you.lrc"),
                ("./instrumental/Tu jaane na(ins).mp3","./lyrics/Tu Jane na.lrc"),
                ("./instrumental/Kabhi Kabhi Aditi (ins).mp3","./lyrics/Kabhi kabhi aditi.lrc")
                # Add more songs here
            ]

            for i, (song, _) in enumerate(songs):
                song_label = tk.Label(root, text=song)
                song_label.grid(row=i+1, column=0, padx=5, pady=5)

                play_button = tk.Button(root, text="Play", command=lambda s=i: run_music_and_record(s, songs, 30, "./recordings/microphone_audio.wav"))
                play_button.grid(row=i+1, column=1, padx=5, pady=5)

                pause_button = tk.Button(root, text="Pause", command=pause_music)
                pause_button.grid(row=i+1, column=2, padx=5, pady=5)
            
            def pause_output_audio():
                pygame.mixer.pause()

            output_button1 = tk.Button(root, text="Output", command=lambda: play_audio(filename1, root.filename2))
            output_button1.grid(row=1, column=8, padx=5, pady=5)

            output_die2 = tk.Button(root, text="Output", command=lambda: play_audio(file_die1, root.file_die2))
            output_die2.grid(row=2, column=8, padx=5, pady=5)

            output_tu2 = tk.Button(root, text="Output", command=lambda: play_audio(file_tu, root.file_tu1))
            output_tu2.grid(row=3, column=8, padx=5, pady=5)

            output_kabhi2 = tk.Button(root, text="Output", command=lambda: play_audio(file_kabhi1, root.file_kabhi2))
            output_kabhi2.grid(row=4, column=8, padx=5, pady=5)

            output_pause = tk.Button(root, text="Pause Output", command=pause_output_audio)
            output_pause.grid(row=5, column=8, padx=5, pady=5)

            root.mainloop()

    if __name__ == "__main__":
        main()





karaokeButton = Button(main_window, text='Karaoke', bd=0, bg='white', fg='SlateBlue1', activebackground='white',
                       cursor='hand2',command=karaoke_Button, font=('Microsoft Yahei UI Light', 22, 'bold'))
karaokeButton.place(x=95, y=220)



# def user_Button():
#     class TkinterWindowDurationTracker:
#         def __init__(self):
#             self.window = tk.Tk()
#             self.start_time = None
#             self.end_time = None
#             self.durations = []  # Initialize durations as an empty list
#             self.run_count = 0
#             self.load_durations()

#             # Add a label to display statistics
#             self.stats_label = tk.Label(self.window, text="Statistics: ", font=("Helvetica", 12))
#             self.stats_label.pack()

#         def load_durations(self):
#             try:
#                 with open("durations.pkl", "rb") as f:
#                     self.durations, self.run_count = pickle.load(f)
#             except FileNotFoundError:
#                 pass

#             # Ensure self.durations is always a list
#             if not isinstance(self.durations, list):
#                 self.durations = []

#         def save_durations(self):
#             with open("durations.pkl", "wb") as f:
#                 pickle.dump((self.durations, self.run_count), f)

#         def calculate_statistics(self):
#             if self.durations:
#                 average_duration = sum(self.durations) / len(self.durations)
#                 max_duration = max(self.durations)
#                 min_duration = min(self.durations)
#                 return f"Average Duration: {average_duration:.2f} seconds, Max Duration: {max_duration:.2f} seconds, Min Duration: {min_duration:.2f} seconds"
#             else:
#                 return "No statistics available."

#         def on_window_close(self):
#             self.end_time = datetime.now()
#             if self.start_time:
#                 duration = (self.end_time - self.start_time).total_seconds()
#                 self.durations.append(duration)
#                 self.run_count += 1
#                 if self.run_count % 5 == 0:
#                     self.durations = []  # Reset durations after every 5 runs
#                 self.save_durations()
#             self.window.quit()

#         def run(self):
#             self.start_time = datetime.now()
#             self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)
#             self.window.mainloop()

#     def plot_durations(durations):
#         plt.plot(durations)
#         plt.xlabel('Run')
#         plt.ylabel('Window Open Duration (seconds)')
#         plt.title('Tkinter Window Open Duration Across Runs')
#         plt.show()

#     if __name__ == "__main__":
#         tracker = TkinterWindowDurationTracker()
#         tracker.run()
#         plot_durations(tracker.durations)
        

# loginuser = PhotoImage(file='userlogin7.png')
# userButton = Button(main_window, image=loginuser, bd=0, bg='grey25', activebackground='grey25',
#                     activeforeground='SlateBlue1', cursor='hand2',command=user_Button)
# userButton.place(x=1175, y=20)

# microphone = PhotoImage(file='microphone1.png')
# microButton = Button(main_window, image=microphone, bd=0, bg='grey25', activebackground='grey25',
#                      activeforeground='SlateBlue1', cursor='hand2')
# microButton.place(x=1100, y=20)

play = PhotoImage(file='play1.png')
playButton1 = Button(main_window, image=play, bd=0, bg='ivory2', activebackground='ivory2',
                     activeforeground='SlateBlue1', cursor='hand2', command=open_pop)
playButton1.place(x=535, y=280)

playButton2 = Button(main_window, image=play, bd=0, bg='ivory2', activebackground='ivory2',
                     activeforeground='SlateBlue1', cursor='hand2', command=open_hiphop)
playButton2.place(x=833, y=280)

playButton3 = Button(main_window, image=play, bd=0, bg='ivory2', activebackground='ivory2',
                     activeforeground='SlateBlue1', cursor='hand2', command=open_sad)
playButton3.place(x=1128, y=280)

playButton4 = Button(main_window, image=play, bd=0, bg='ivory2', activebackground='ivory2',
                     activeforeground='SlateBlue1', cursor='hand2', command=open_hindi)
playButton4.place(x=535, y=535)

playButton5 = Button(main_window, image=play, bd=0, bg='ivory2', activebackground='ivory2',
                     activeforeground='SlateBlue1', cursor='hand2', command=open_eighty)
playButton5.place(x=833, y=535)

playButton6 = Button(main_window, image=play, bd=0, bg='ivory2', activebackground='ivory2',
                     activeforeground='SlateBlue1', cursor='hand2', command=open_rock)
playButton6.place(x=1128, y=535)


def logout():
    print("Logged out successfully")
    main_window.destroy()


logoutButton = Button(main_window, text='Logout', bd=0, bg='grey25', fg='SlateBlue1', activebackground='grey25',
                      cursor='hand2', font=('Microsoft Yahei UI Light', 25, 'bold'), command=logout)
logoutButton.place(x=1050, y=620)



main_window.mainloop()