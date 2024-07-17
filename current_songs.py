import sqlite3

# Function to create the current_songs table
def create_current_songs_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS current_songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            song_name TEXT,
            artist_name TEXT,
            album_name TEXT,
            song_link TEXT,
            saved BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')

    conn.commit()
    conn.close()

# Function to save current songs in the database
def save_current_songs(user_id, songs):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM current_songs WHERE user_id = ?', (user_id,))
    for song in songs.values():
        cursor.execute('''
            INSERT INTO current_songs (user_id, song_name, artist_name, album_name, song_link, saved)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, song['song_name'], song['artist_name'], song['album_name'], song['song_link'], False))
    conn.commit()
    conn.close()

# Function to get current songs from the database
def get_current_songs(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM current_songs WHERE user_id = ?', (user_id,))
    songs = cursor.fetchall()
    conn.close()
    return songs

# Function to mark a song as saved
def mark_song_as_saved(user_id, song_name, artist_name):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE current_songs
        SET saved = TRUE
        WHERE user_id = ? AND song_name = ? AND artist_name = ?
    ''', (user_id, song_name, artist_name))
    conn.commit()
    conn.close()


create_current_songs_table()
