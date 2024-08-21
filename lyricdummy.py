import tkinter as tk
from tkinter import filedialog
import pygame
import threading
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from datetime import datetime
from PIL import Image, ImageTk


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
    root = tk.Tk()
    root.title("Song Player")

    # Load background image
    background_image = Image.open("./assets/karaokegui.png")
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a label with the background image
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Ensure the image is retained by Tkinter
    background_label.image = background_photo

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

    output_button1 = tk.Button(root, text="Output", command=lambda: play_audio(filename1, root.filename2))
    output_button1.grid(row=1, column=8, padx=5, pady=5)

    output_die2 = tk.Button(root, text="Output", command=lambda: play_audio(file_die1, root.file_die2))
    output_die2.grid(row=2, column=8, padx=5, pady=5)

    output_tu2 = tk.Button(root, text="Output", command=lambda: play_audio(file_tu, root.file_tu1))
    output_tu2.grid(row=3, column=8, padx=5, pady=5)

    output_kabhi2 = tk.Button(root, text="Output", command=lambda: play_audio(file_kabhi1, root.file_kabhi2))
    output_kabhi2.grid(row=4, column=8, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
