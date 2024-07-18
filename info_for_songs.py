import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
from api_key import *  # Imports SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
from songs import *  # Import functions from songs.py


# Get API keys from environment variables
load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
GPT_API_KEY = os.getenv('GPT_API_KEY')


# Function to fetch weather forecast for a specified city
def weather_forecast(city, api_key):
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        city_from_response = json_response['location']['name']
        region_from_response = json_response['location']['region']
        fahrenheit = json_response['current']['temp_f']
        weather = json_response['current']['condition']['text']
        return (fahrenheit, weather), city_from_response
    else:
        print("Error, status code:", response.status_code)
        print("Please try again with a valid city name")


# Function to generate query words using GPT-3 based on weather and activity
def gpt_query_words(weather_stats, activity, api_key):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a musical genius that generates a list of words or short phrases to use in the Spotify API search function based on the given activity and weather. Generate a maximum of 5 phrases and a minimum of 3."},
            {"role": "user", "content": f"The weather is {weather_stats[0]} degrees and {weather_stats[1]} and the activity is {activity}."}
        ]
    )
    return completion.choices[0].message.content


# Function to generate query words using GPT-3 based on user's mood
def gpt_query_words_mood(mood, api_key):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a musical genius that generates a list of words or short phrases to use in the Spotify API search function based on a given mood and possible reason for feeling that way. Generate a maximum of 5 phrases and a minimum of 3."},
            {"role": "user", "content": f"I am feeling {mood}."}  # Consider changing to get better responses
        ]
    )
    return completion.choices[0].message.content


# Get songs from mood feature
def get_songs_from_mood(mood, genre):
    query_words = gpt_query_words_mood(mood, GPT_API_KEY)
    songs = get_songs_from_spotify(genre, query_words, limit=5)
    return songs, mood  # return these to be used by match_the_mood.html


# Get songs from activity and weather feature
def get_songs_from_activity(city, activity, genre):
    weather_stats, city_name = weather_forecast(city, WEATHER_API_KEY)
    query_words = gpt_query_words(weather_stats, activity, GPT_API_KEY)
    songs = get_songs_from_spotify(genre, query_words, limit=5)

    return songs, weather_stats  # get activity from session in app.py, use all this for match_the_mood.html


# Get similar songs feature
def get_similar_songs(song):
    return get_similar(song, limit=5)  # just returns song dict to be used for match_the_mood.html


# Fetch weather and songs
'''def get_weather_and_songs(city, activity, genre):
    weather_stats, city_name = weather_forecast(city, WEATHER_API_KEY)
    query_words = gpt_query_words(weather_stats, activity, GPT_API_KEY)
    songs = get_songs_from_spotify(genre, query_words, limit=10)
    return weather_stats, city_name, activity, query_words, songs


# Main function for testing functionality
if __name__ == '__main__':
    songs_dict, user_mood = get_songs_from_mood("I'm feeling sad since I lost a game", "rap")
    pprint.pprint(songs_dict)'''