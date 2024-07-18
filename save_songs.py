import sqlite3
from dotenv import load_dotenv
import os
from songs import *


# Load environment variables from .env file
load_dotenv()


# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # Allows fetching rows as dictionaries
    return conn


# Create saved_songs table if not exists
def create_saved_songs_table():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS saved_songs (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   song_name TEXT NOT NULL,
                   artist_name TEXT NOT NULL,
                   album_name TEXT,
                   song_link TEXT NOT NULL,
                   user_id INTEGER,
                   FOREIGN KEY (user_id) REFERENCES users(user_id)
               )''')
    conn.commit()
    conn.close()


# Function to save a song for a user
def save_song(user_id, song_name, artist_name, album_name, song_link):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO saved_songs (song_name, artist_name, album_name, song_link, user_id)
                     VALUES (?, ?, ?, ?, ?)''', (song_name, artist_name, album_name, song_link, user_id))
        conn.commit()
        song_id = c.lastrowid
        conn.close()
        return song_id
    except sqlite3.IntegrityError as e:
        conn.close()
        return None


# Function to retrieve saved songs for a user
def get_saved_songs(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT * FROM saved_songs WHERE user_id=?''', (user_id,))
    saved_songs = c.fetchall()
    conn.close()
    return saved_songs


# Function to delete a saved song by its ID
def delete_saved_song_by_id(user_id, song_id):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM saved_songs WHERE id=? AND user_id=?", (song_id, user_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting song: {e}")
        conn.close()
        return False


# Call this function once to create the table if it doesn't exist
create_saved_songs_table()
