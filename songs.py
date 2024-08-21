
import mysql.connector
import os
import pyaudio
import wave

# Function to add a song to the database
def add_song(title, artist, album, audio_directory, audio_file_name):
    # Establish a connection to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="jmatheworden27",
        database="userdata"
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS songs
                    (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), artist VARCHAR(255), album VARCHAR(255), file_path VARCHAR(255))''')

    # Create the file path by joining the directory path and file name
    file_path = os.path.join(audio_directory, audio_file_name).replace("\\", "/")  # Replace backslashes with forward slashes

    # Insert the song data into the database
    insert_query = "INSERT INTO songs (title, artist, album, file_path) VALUES (%s, %s, %s, %s)"
    song_data = (title, artist, album, file_path)
    cursor.execute(insert_query, song_data)
    conn.commit()
    print("Song added successfully.")

    # Close the cursor and database connection
    cursor.close()
    conn.close()

# Function to play a song from the database using PyAudio
def play_song(song_id):
    # Establish a connection to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="jmatheworden27",
        database="userdata"
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Query the database to retrieve the file path of the song
    query = "SELECT file_path FROM songs WHERE id = %s"
    cursor.execute(query, (song_id,))
    result = cursor.fetchone()

    # Check if the song file path was found
    if result:
        file_path = result[0]
        print("Playing song:", file_path)

        # Initialize PyAudio
        p = pyaudio.PyAudio()

        # Open the audio file
        wf = wave.open(file_path, 'rb')

        # Open a PyAudio stream
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Read data and play audio in chunks
        chunk = 1024
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        # Close the stream and PyAudio
        stream.close()
        p.terminate()
    else:
        print("Song not found.")

    # Close the cursor and database connection
    cursor.close()
    conn.close()


# Example usage: Add a song to the database
add_song("City", "Shreya", "Music", r"C:\Users\jorde\Desktop\python\pythonProject2\music\The Weeknd, Ariana Grande - Die For You (Remix - Lyric Video).mp3", "City.wav")


# Example usage: Play the song with ID 1 from the database
play_song(1)





