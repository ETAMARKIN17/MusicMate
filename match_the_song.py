import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
from get_spotify_api_key import *  # Imports SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
from songs import *  # Import functions from songs.py


# Get similar songs feature
def get_similar_songs(song):
    return get_similar(song, limit=6)  # just returns song dict to be used for match_the_mood.html
