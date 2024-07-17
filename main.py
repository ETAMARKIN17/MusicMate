import os
from dotenv import load_dotenv
from openai import OpenAI
from api_key import *  # Imports SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
from songs import *  # Import functions from songs.py
from weather_and_activity import *  # Import functions from weather_and_activity.py
from user_accounts import *  # Import user account functions

# Get API keys from environment variables
load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
GPT_API_KEY = os.getenv('GPT_API_KEY')

# Function to generate query words using GPT-3 based on weather and activity
def gpt_query_words(weather_stats, activity, api_key):
    """
    Generates query words for Spotify API search based on weather and user's activity using GPT-3.

    Args:
    - weather_stats (list): Contains temperature and weather condition.
    - activity (str): User's current activity.
    - api_key (str): API key for GPT-3.

    Returns:
    - String containing query words.
    """
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a musical genius that generates a list of words or short phrases to use in the Spotify API search function based on the given activity and weather. Generate a maximum of 5 phrases and a minimum of 3."},
            {"role": "user", "content": f"The weather is {weather_stats[0]} degrees and {weather_stats[1]} and the activity is {activity}."}
        ]
    )
    return completion.choices[0].message.content

# Fetch weather and songs
def get_weather_and_songs(city, activity, genre):
    weather_stats, city_name = weather_forecast(city, WEATHER_API_KEY)
    query_words = gpt_query_words(weather_stats, activity, GPT_API_KEY)
    songs = get_songs_from_spotify(genre, query_words, limit=10)
    return weather_stats, city_name, activity, query_words, songs
