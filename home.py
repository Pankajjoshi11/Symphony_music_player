import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pygame
import os
import time
from pygame import mixer
from mutagen.mp3 import MP3
import random

window = tk.Tk()
window.title("Login form")
window.geometry('700x500')
window.configure(bg='#333333')

# Function to be called when a button is clicked
def button_click():
    messagebox.showinfo("Button Clicked", "You clicked the button!")

def open_pop():
    pop_window = tk.Toplevel()
    pop_window.title("Pop Songs")
    pop_window.geometry('1250x700')
    pop_window.configure(bg='purple')

    pygame.mixer.init()

    global current_song_index, paused, repeat_mode

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

    pop_label = tk.Label(pop_window, text="Pop Songs", font=('Arial', 42, 'bold'), background=background, foreground='white')
    pop_label.place(relx=0.42, rely=0.22)

    bottom_frame = tk.Frame(pop_window, bg=frame_bg)
    bottom_frame.place(relx=0, rely=0.35, relwidth=1, relheight=1)

    # List of songs
    song_list = [
        "./music/Kanye West - Heartless.mp3",
        "./music/The Weeknd, Ariana Grande - Die For You (Remix - Lyric Video).mp3"
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
                            activeforeground='white', activebackground='white', cursor='hand2', command=shuffle_playlist_and_play)
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

    low_frame= tk.Frame(pop_window, bg='black')
    low_frame.place(relx=0, rely=0.85, relwidth=1, relheight=1)

    border_frame = tk.Frame(pop_window, bg='white', height=2)  # Adjust height as needed
    border_frame.place(relx=0, rely=0.85, relwidth=1)

    # Create a progress bar
    progress = ttk.Progressbar(pop_window, orient='horizontal', mode='determinate', length=1200, style="Custom.Horizontal.TProgressbar")
    progress.place(relx=0.1, rely=0.9)


    progress_bar_color='green'
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

    image_vol=tk.PhotoImage(file='./assets/sound.png')
    slider_button = tk.Button(low_frame, image=image_vol, font=('Arial', 12), fg='white', bg='purple',
                            activeforeground='white', activebackground='purple', cursor='hand2', command=toggle_slider)
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

    repeat_img=tk.PhotoImage(file='./assets/onrepeat.png')
    button_repeat=tk.Button(low_frame,image=repeat_img,bg=background,fg='black',activebackground='black',command=play_selected_song)
    button_repeat.place(relx=0.8,rely=0.07)

    

    def pause_unpause():
        global paused
        if paused:
            mixer.music.unpause()
            paused = False
            button_pause.config(image=pause_img)  # Change button image to pause image
        else:
            mixer.music.pause()
            paused = True
            button_pause.config(image=play_img)   # Change button image to play image

    paused = False  # Initial state of music playback



    pause_img=tk.PhotoImage(file='./assets/pause.png')
    play_img=tk.PhotoImage(file='./assets/play2.png')
    button_pause = tk.Button(low_frame, image=pause_img, width=4, bd=5,
                        font="Helvetica, 15", bg="purple", fg="white", command=pause_unpause)
    button_pause.place(relx=0.5, rely=0.07,relwidth=0.04, relheight=0.075)

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




    prev_img=tk.PhotoImage(file='./assets/previous.png')
    next_img=tk.PhotoImage(file='./assets/next.png')

    button_prev=tk.Button(low_frame,image=prev_img,bg=background,command=prev_song)
    button_prev.place(relx=0.45,rely=0.071)

    button_next=tk.Button(low_frame,image=next_img,bg=background,command=next_song)
    button_next.place(relx=0.55,rely=0.071)

    # Button for navigation
    

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

    pop_label = tk.Label(rock_window, text="Rock Songs", font=('Arial', 42, 'bold'), background=background, foreground='white')
    pop_label.place(relx=0.42, rely=0.22)

    bottom_frame = tk.Frame(rock_window, bg=frame_bg)
    bottom_frame.place(relx=0, rely=0.35, relwidth=1, relheight=1)

    # List of songs
    song_list = [
        "./music/Kanye West - Heartless.mp3",
        "./music/The Weeknd, Ariana Grande - Die For You (Remix - Lyric Video).mp3"
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
                            activeforeground='white', activebackground='white', cursor='hand2', command=shuffle_playlist_and_play)
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

    low_frame= tk.Frame(rock_window, bg='black')
    low_frame.place(relx=0, rely=0.85, relwidth=1, relheight=1)

    border_frame = tk.Frame(rock_window, bg='white', height=2)  # Adjust height as needed
    border_frame.place(relx=0, rely=0.85, relwidth=1)

    # Create a progress bar
    progress = ttk.Progressbar(rock_window, orient='horizontal', mode='determinate', length=1200, style="Custom.Horizontal.TProgressbar")
    progress.place(relx=0.1, rely=0.9)


    progress_bar_color='green'
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

    image_vol=tk.PhotoImage(file='./assets/sound.png')
    slider_button = tk.Button(low_frame, image=image_vol, font=('Arial', 12), fg='white', bg='purple',
                            activeforeground='white', activebackground='purple', cursor='hand2', command=toggle_slider)
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

    repeat_img=tk.PhotoImage(file='./assets/onrepeat.png')
    button_repeat=tk.Button(low_frame,image=repeat_img,bg=background,fg='black',activebackground='black',command=play_selected_song)
    button_repeat.place(relx=0.8,rely=0.07)

    

    def pause_unpause():
        global paused
        if paused:
            mixer.music.unpause()
            paused = False
            button_pause.config(image=pause_img)  # Change button image to pause image
        else:
            mixer.music.pause()
            paused = True
            button_pause.config(image=play_img)   # Change button image to play image

    paused = False  # Initial state of music playback



    pause_img=tk.PhotoImage(file='./assets/pause.png')
    play_img=tk.PhotoImage(file='./assets/play2.png')
    button_pause = tk.Button(low_frame, image=pause_img, width=4, bd=5,
                        font="Helvetica, 15", bg="purple", fg="white", command=pause_unpause)
    button_pause.place(relx=0.5, rely=0.07,relwidth=0.04, relheight=0.075)

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




    prev_img=tk.PhotoImage(file='./assets/previous.png')
    next_img=tk.PhotoImage(file='./assets/next.png')

    button_prev=tk.Button(low_frame,image=prev_img,bg=background,command=prev_song)
    button_prev.place(relx=0.45,rely=0.071)

    button_next=tk.Button(low_frame,image=next_img,bg=background,command=next_song)
    button_next.place(relx=0.55,rely=0.071)

    # Button for navigation
    

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

    pop_label = tk.Label(hiphop_window, text="HipHop Songs", font=('Arial', 42, 'bold'), background=background, foreground='white')
    pop_label.place(relx=0.42, rely=0.22)

    bottom_frame = tk.Frame(hiphop_window, bg=frame_bg)
    bottom_frame.place(relx=0, rely=0.35, relwidth=1, relheight=1)

    # List of songs
    song_list = [
        "./music/Kanye West - Heartless.mp3",
        "./music/The Weeknd, Ariana Grande - Die For You (Remix - Lyric Video).mp3"
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
                            activeforeground='white', activebackground='white', cursor='hand2', command=shuffle_playlist_and_play)
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

    low_frame= tk.Frame(hiphop_window, bg='black')
    low_frame.place(relx=0, rely=0.85, relwidth=1, relheight=1)

    border_frame = tk.Frame(hiphop_window, bg='white', height=2)  # Adjust height as needed
    border_frame.place(relx=0, rely=0.85, relwidth=1)

    # Create a progress bar
    progress = ttk.Progressbar(hiphop_window, orient='horizontal', mode='determinate', length=1200, style="Custom.Horizontal.TProgressbar")
    progress.place(relx=0.1, rely=0.9)


    progress_bar_color='green'
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

    image_vol=tk.PhotoImage(file='./assets/sound.png')
    slider_button = tk.Button(low_frame, image=image_vol, font=('Arial', 12), fg='white', bg='purple',
                            activeforeground='white', activebackground='purple', cursor='hand2', command=toggle_slider)
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

    repeat_img=tk.PhotoImage(file='./assets/onrepeat.png')
    button_repeat=tk.Button(low_frame,image=repeat_img,bg=background,fg='black',activebackground='black',command=play_selected_song)
    button_repeat.place(relx=0.8,rely=0.07)

    

    def pause_unpause():
        global paused
        if paused:
            mixer.music.unpause()
            paused = False
            button_pause.config(image=pause_img)  # Change button image to pause image
        else:
            mixer.music.pause()
            paused = True
            button_pause.config(image=play_img)   # Change button image to play image

    paused = False  # Initial state of music playback



    pause_img=tk.PhotoImage(file='./assets/pause.png')
    play_img=tk.PhotoImage(file='./assets/play2.png')
    button_pause = tk.Button(low_frame, image=pause_img, width=4, bd=5,
                        font="Helvetica, 15", bg="purple", fg="white", command=pause_unpause)
    button_pause.place(relx=0.5, rely=0.07,relwidth=0.04, relheight=0.075)

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




    prev_img=tk.PhotoImage(file='./assets/previous.png')
    next_img=tk.PhotoImage(file='./assets/next.png')

    button_prev=tk.Button(low_frame,image=prev_img,bg=background,command=prev_song)
    button_prev.place(relx=0.45,rely=0.071)

    button_next=tk.Button(low_frame,image=next_img,bg=background,command=next_song)
    button_next.place(relx=0.55,rely=0.071)

    # Button for navigation
    

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

    pop_label = tk.Label(hindi_window, text="Bollywood Songs", font=('Arial', 42, 'bold'), background=background, foreground='white')
    pop_label.place(relx=0.42, rely=0.22)

    bottom_frame = tk.Frame(hindi_window, bg=frame_bg)
    bottom_frame.place(relx=0, rely=0.35, relwidth=1, relheight=1)

    # List of songs
    song_list = [
        "./music/Kanye West - Heartless.mp3",
        "./music/The Weeknd, Ariana Grande - Die For You (Remix - Lyric Video).mp3"
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
                            activeforeground='white', activebackground='white', cursor='hand2', command=shuffle_playlist_and_play)
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

    low_frame= tk.Frame(hindi_window, bg='black')
    low_frame.place(relx=0, rely=0.85, relwidth=1, relheight=1)

    border_frame = tk.Frame(hindi_window, bg='white', height=2)  # Adjust height as needed
    border_frame.place(relx=0, rely=0.85, relwidth=1)

    # Create a progress bar
    progress = ttk.Progressbar(hindi_window, orient='horizontal', mode='determinate', length=1200, style="Custom.Horizontal.TProgressbar")
    progress.place(relx=0.1, rely=0.9)


    progress_bar_color='green'
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

    image_vol=tk.PhotoImage(file='./assets/sound.png')
    slider_button = tk.Button(low_frame, image=image_vol, font=('Arial', 12), fg='white', bg='purple',
                            activeforeground='white', activebackground='purple', cursor='hand2', command=toggle_slider)
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

    repeat_img=tk.PhotoImage(file='./assets/onrepeat.png')
    button_repeat=tk.Button(low_frame,image=repeat_img,bg=background,fg='black',activebackground='black',command=play_selected_song)
    button_repeat.place(relx=0.8,rely=0.07)

    

    def pause_unpause():
        global paused
        if paused:
            mixer.music.unpause()
            paused = False
            button_pause.config(image=pause_img)  # Change button image to pause image
        else:
            mixer.music.pause()
            paused = True
            button_pause.config(image=play_img)   # Change button image to play image

    paused = False  # Initial state of music playback



    pause_img=tk.PhotoImage(file='./assets/pause.png')
    play_img=tk.PhotoImage(file='./assets/play2.png')
    button_pause = tk.Button(low_frame, image=pause_img, width=4, bd=5,
                        font="Helvetica, 15", bg="purple", fg="white", command=pause_unpause)
    button_pause.place(relx=0.5, rely=0.07,relwidth=0.04, relheight=0.075)

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




    prev_img=tk.PhotoImage(file='./assets/previous.png')
    next_img=tk.PhotoImage(file='./assets/next.png')

    button_prev=tk.Button(low_frame,image=prev_img,bg=background,command=prev_song)
    button_prev.place(relx=0.45,rely=0.071)

    button_next=tk.Button(low_frame,image=next_img,bg=background,command=next_song)
    button_next.place(relx=0.55,rely=0.071)

    # Button for navigation
    

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

    pop_label = tk.Label(sad_window, text="Sad Songs", font=('Arial', 42, 'bold'), background=background, foreground='white')
    pop_label.place(relx=0.42, rely=0.22)

    bottom_frame = tk.Frame(sad_window, bg=frame_bg)
    bottom_frame.place(relx=0, rely=0.35, relwidth=1, relheight=1)

    # List of songs
    song_list = [
        "./music/Kanye West - Heartless.mp3",
        "./music/The Weeknd, Ariana Grande - Die For You (Remix - Lyric Video).mp3"
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
                            activeforeground='white', activebackground='white', cursor='hand2', command=shuffle_playlist_and_play)
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

    low_frame= tk.Frame(sad_window, bg='black')
    low_frame.place(relx=0, rely=0.85, relwidth=1, relheight=1)

    border_frame = tk.Frame(sad_window, bg='white', height=2)  # Adjust height as needed
    border_frame.place(relx=0, rely=0.85, relwidth=1)

    # Create a progress bar
    progress = ttk.Progressbar(sad_window, orient='horizontal', mode='determinate', length=1200, style="Custom.Horizontal.TProgressbar")
    progress.place(relx=0.1, rely=0.9)


    progress_bar_color='green'
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

    image_vol=tk.PhotoImage(file='./assets/sound.png')
    slider_button = tk.Button(low_frame, image=image_vol, font=('Arial', 12), fg='white', bg='purple',
                            activeforeground='white', activebackground='purple', cursor='hand2', command=toggle_slider)
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

    repeat_img=tk.PhotoImage(file='./assets/onrepeat.png')
    button_repeat=tk.Button(low_frame,image=repeat_img,bg=background,fg='black',activebackground='black',command=play_selected_song)
    button_repeat.place(relx=0.8,rely=0.07)

    

    def pause_unpause():
        global paused
        if paused:
            mixer.music.unpause()
            paused = False
            button_pause.config(image=pause_img)  # Change button image to pause image
        else:
            mixer.music.pause()
            paused = True
            button_pause.config(image=play_img)   # Change button image to play image

    paused = False  # Initial state of music playback



    pause_img=tk.PhotoImage(file='./assets/pause.png')
    play_img=tk.PhotoImage(file='./assets/play2.png')
    button_pause = tk.Button(low_frame, image=pause_img, width=4, bd=5,
                        font="Helvetica, 15", bg="purple", fg="white", command=pause_unpause)
    button_pause.place(relx=0.5, rely=0.07,relwidth=0.04, relheight=0.075)

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




    prev_img=tk.PhotoImage(file='./assets/previous.png')
    next_img=tk.PhotoImage(file='./assets/next.png')

    button_prev=tk.Button(low_frame,image=prev_img,bg=background,command=prev_song)
    button_prev.place(relx=0.45,rely=0.071)

    button_next=tk.Button(low_frame,image=next_img,bg=background,command=next_song)
    button_next.place(relx=0.55,rely=0.071)

    # Button for navigation
    

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

    pop_label = tk.Label(eighty_window, text="80's Top Hits", font=('Arial', 42, 'bold'), background=background, foreground='white')
    pop_label.place(relx=0.42, rely=0.22)

    bottom_frame = tk.Frame(eighty_window, bg=frame_bg)
    bottom_frame.place(relx=0, rely=0.35, relwidth=1, relheight=1)

    # List of songs
    song_list = [
        "./music/Kanye West - Heartless.mp3",
        "./music/The Weeknd, Ariana Grande - Die For You (Remix - Lyric Video).mp3"
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
                            activeforeground='white', activebackground='white', cursor='hand2', command=shuffle_playlist_and_play)
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

    low_frame= tk.Frame(eighty_window, bg='black')
    low_frame.place(relx=0, rely=0.85, relwidth=1, relheight=1)

    border_frame = tk.Frame(eighty_window, bg='white', height=2)  # Adjust height as needed
    border_frame.place(relx=0, rely=0.85, relwidth=1)

    # Create a progress bar
    progress = ttk.Progressbar(eighty_window, orient='horizontal', mode='determinate', length=1200, style="Custom.Horizontal.TProgressbar")
    progress.place(relx=0.1, rely=0.9)


    progress_bar_color='green'
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

    image_vol=tk.PhotoImage(file='./assets/sound.png')
    slider_button = tk.Button(low_frame, image=image_vol, font=('Arial', 12), fg='white', bg='purple',
                            activeforeground='white', activebackground='purple', cursor='hand2', command=toggle_slider)
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

    repeat_img=tk.PhotoImage(file='./assets/onrepeat.png')
    button_repeat=tk.Button(low_frame,image=repeat_img,bg=background,fg='black',activebackground='black',command=play_selected_song)
    button_repeat.place(relx=0.8,rely=0.07)

    

    def pause_unpause():
        global paused
        if paused:
            mixer.music.unpause()
            paused = False
            button_pause.config(image=pause_img)  # Change button image to pause image
        else:
            mixer.music.pause()
            paused = True
            button_pause.config(image=play_img)   # Change button image to play image

    paused = False  # Initial state of music playback



    pause_img=tk.PhotoImage(file='./assets/pause.png')
    play_img=tk.PhotoImage(file='./assets/play2.png')
    button_pause = tk.Button(low_frame, image=pause_img, width=4, bd=5,
                        font="Helvetica, 15", bg="purple", fg="white", command=pause_unpause)
    button_pause.place(relx=0.5, rely=0.07,relwidth=0.04, relheight=0.075)

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




    prev_img=tk.PhotoImage(file='./assets/previous.png')
    next_img=tk.PhotoImage(file='./assets/next.png')

    button_prev=tk.Button(low_frame,image=prev_img,bg=background,command=prev_song)
    button_prev.place(relx=0.45,rely=0.071)

    button_next=tk.Button(low_frame,image=next_img,bg=background,command=next_song)
    button_next.place(relx=0.55,rely=0.071)

    # Button for navigation
    

    eighty_window.mainloop()


# Create and place the buttons at different positions
button1 = tk.Button(window, text="pop", command=open_pop)
button1.place(x=50, y=50)

button2 = tk.Button(window, text="rock", command=open_rock)
button2.place(x=200, y=100)

button3 = tk.Button(window, text="hiphop", command=open_hiphop)
button3.place(x=350, y=150)

button4 = tk.Button(window, text="Hindi", command=open_hindi)
button4.place(x=100, y=200)

button5 = tk.Button(window, text="Sad", command=open_sad)
button5.place(x=250, y=250)

button6 = tk.Button(window, text="Eighty", command=open_eighty)
button6.place(x=400, y=300)

button7 = tk.Button(window, text="Button 7", command=button_click)
button7.place(x=150, y=350)

window.mainloop()
