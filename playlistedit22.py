import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pygame
import random
import pickle


# Initialize pygame mixer for playing audio
pygame.mixer.init()

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

# Create a frame to hold the files
file_frame = tk.Frame(root, bg="purple")
file_frame.pack(pady=2)

# Display all songs from song_list
for file_path in song_list:
    if file_path.lower().endswith(('.mp3', '.wav', '.ogg')):
        file_label = tk.Label(file_frame, text=os.path.basename(file_path), bg="white", fg="black")
        file_label.pack(side="top", padx=5, pady=5)
        add_to_playlist_button = tk.Button(file_frame, text="Add to Playlist", command=lambda f=file_path: add_to_playlist(f, playlist_window)) 
        add_to_playlist_button.pack(side="top", padx=5)

# Create playlist window
playlist_window = tk.Toplevel(root)
playlist_window.title("Playlists")
playlist_window.geometry("400x400")
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
