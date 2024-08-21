import tkinter as tk
from tkinter import *
import customtkinter
import pygame
from PIL import Image, ImageTk
from threading import *
import time
import math

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.title('Music Player')
root.geometry('990x660+50+50')
root.resizable(0,0)
bgImage = ImageTk.PhotoImage(file='blackbg2.jpg')
background_label = tk.Label(root, image=bgImage)
background_label.place(x=0, y=0,relwidth=1, relheight=1)

pygame.mixer.init()

list_of_songs = ['music/City.wav','music/Retro1.wav','music/Oldbass1.wav']
list_of_covers = ['img/city.jpg','img/concert.jpg','img/girly.jpg']
n = 0

def get_album_cover(song_name, n):
    image1 = Image.open(list_of_covers[n])
    image2 = image1.resize((420, 420))
    load = ImageTk.PhotoImage(image2)

    # Create a label to display the album cover image
    label1 = tk.Label(root, image=load)
    label1.image = load  # Keeping a reference to the image to prevent garbage collection
    label1.place(x=130, y=80)

    # Create a label to display the song name
    stripped_string = song_name[6:-4]  # Assuming this is correct
    song_name_label = tk.Label(root, text=stripped_string, bg='grey23', fg='white',font=('Microsoft Yahei UI Light', 30, 'bold'))  # Set text color to white
    song_name_label.place(x=260, y=540)
def progress():
    a = pygame.mixer.sound(f'{list_of_songs[n]}')
    song_len = a.get_length() * 3
    for i in range(0, math.ceil(song_len)):
        time.sleep(.3)
        progressbar.set(pygame.mixer.music.get_pos() / 1000000)

def threading():
    t1 = Thread(target=progress)
    t1.start()

def play_music():
    threading()
    global n
    current_song = n
    if n>2:
        n=0
    song_name = list_of_songs[n]
    pygame.mixer.music.load(song_name)
    pygame.mixer.music.play(loops=0)
    pygame.mixer.music.set_volume(.5)
    get_album_cover(song_name, n)

    n += 1

def pause_music():
    pygame.mixer.music.pause()
def skip_forward():
    play_music()

def skip_back():
    global n
    n -= 2
    play_music()

def volume(value):
    pygame.mixer.music.set_volume(value)

#Buttons
play_button= customtkinter.CTkButton(master=root,text='Play', bg_color='grey20',hover_color='#a53cd6',fg_color='SlateBlue1',font=('Microsoft Yahei UI Light', 23, 'bold'),width=85,command=play_music)
play_button.place(x=165,y=500)

pause_button = customtkinter.CTkButton(master=root, text='Pause', bg_color='grey20', hover_color='#a53cd6', fg_color='SlateBlue1', font=('Microsoft Yahei UI Light', 23, 'bold'), width=80, command=pause_music)
pause_button.place(x=270, y=500)

skip_f = customtkinter.CTkButton(master=root,text='>', bg_color='grey20',hover_color='#a53cd6',fg_color='SlateBlue1',font=('Microsoft Yahei UI Light', 23, 'bold'),command=skip_forward,width=80)
skip_f.place(x=375,y=500)

skip_b = customtkinter.CTkButton(master=root,text='<', bg_color='grey20',hover_color='#a53cd6',fg_color='SlateBlue1',font=('Microsoft Yahei UI Light', 23, 'bold'),command=skip_back,width=80)
skip_b.place(x=60,y=500)

slider = customtkinter.CTkSlider(master=root, bg_color='grey20',button_color='SlateBlue1', button_hover_color='SlateBlue1',from_ = 0, to=1,command=volume,width=340)
slider.place(x=100,y=550)

progressbar = customtkinter.CTkProgressBar(master=root, progress_color='#a53cd6', border_color='grey20',width=455,height=10,corner_radius=3)
progressbar.place(x=40,y=590)

root.mainloop()