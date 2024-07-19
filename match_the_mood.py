import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
from get_spotify_api_key import *  # Imports SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
from songs import *  # Import functions from songs.py


# Get API keys from environment variables
load_dotenv()
GPT_API_KEY = os.getenv('GPT_API_KEY')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


def gpt_query_words_mood(mood, api_key):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a spotify genius that specializes in finding the right playlist based off some information. Generate a list of 3 - 5 words or short phrases to use in the Spotify API search function to search for a playlist based on the given mood."},
            {"role": "user", "content": f"I am feeling {mood}."}  # Consider changing to get better responses
        ]
    )
    return completion.choices[0].message.content


def recommend_songs(query_words, genre):
    playlist = get_playlist_from_spotify(query_words, genre)

    songs = get_songs_from_playlist(genre, playlist)

    all_songs = list(songs.values())
    random_5_songs = random.sample(all_songs, k=min(5, len(all_songs)))

    random_5_songs_dict = {}
    for i, song in enumerate(random_5_songs):
        random_5_songs_dict[i + 1] = {
            "song_name": song["song_name"],
            "artist_name": song["artist_name"],
            "album_name": song["album_name"],
            "song_link": song["song_link"],
            "album_cover": song["album_cover"],
            "popularity": song["popularity"]
        }
    return random_5_songs_dict


def get_songs_from_mood(mood, genre):
    query_words = gpt_query_words_mood(mood, GPT_API_KEY)
    songs = recommend_songs(query_words, genre)
    return songs, mood  # return these to be used by match_the_mood.html
