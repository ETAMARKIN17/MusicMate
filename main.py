import os
import requests
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


def intro_page():
    """
    Displays the home screen with options to login, register, or exit.

    Returns:
    - str: Username of the logged-in user, or 'exit' if user chooses to exit.
    """
    create_users_table()  # Create the users table if it doesn't exist

    print("\nWelcome to WeatherTunes! 🌤️ 🎶")
    print("Discover the perfect soundtrack for your day with personalized song suggestions based on the weather and your activities.🌸")
    print("Let the Music Match the Mood! 😎")

    while True:
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            user = login_user()
            if user:
                print(f"Login successful! Welcome back, {user[1]}!")
                return 'success'
            else:
                print("Login failed. Please try again.")
        elif choice == '2':
            register_user()
            print(f"Registered successfully!")
            return 'success'
        elif choice == '3':
            print("Exiting WeatherTunes. Goodbye!")
            return 'exit'  # Return 'exit' to indicate user chose to exit
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


# Function to generate query words using GPT-3 based on weather and activity
def gpt_query_words(weather_stats, activity):
    """
    Generates query words for Spotify API search based on weather and user's activity using GPT-3.

    Args:
    - weather_stats (list): Contains temperature and weather condition.
    - activity (str): User's current activity.

    Returns:
    - String containing query words.
    """
    client = OpenAI(
        api_key=GPT_API_KEY,
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a musical genius that generates a list of words or short phrases to use in the Spotify API search function based on the given activity and weather. Generate a maximum of 5 phrases and a minimum of 3"},
            {"role": "user", "content": f"The weather is {weather_stats[0]} degrees and {weather_stats[1]} and the activity is {activity}"}
        ]
    )
    return completion.choices[0].message.content


# Function to display final response with song recommendations and options
def final_response(query_words, activity, city, weather_stats, songs):
    """
    Displays final response with song recommendations and options for further interaction.

    Args:
    - query_words (str): Keywords used in Spotify API search.
    - activity (str): User's activity.
    - city (str): User's city.
    - weather_stats (list): Contains temperature and weather condition.
    - songs (dict): Dictionary of songs fetched from Spotify API.

    Returns:
    - True
    """
    while True:
        more_info = input("Would you like to see the basic info or extended info for each song? Type 'b' for basic and 'e' for extended: ")
        if more_info == 'b':
            print(f"\nI hope you enjoy {activity} in {city} 😁")
            print(f"It will be around {weather_stats[0]} degrees and {weather_stats[1]}.")
            print("Here are some tunes to groove to:")
            for i, song in songs.items():
                print(f"{i}. {song['song_name']} by {song['artist_name']}. 🎶")
            break
        elif more_info == 'e':
            print(f"\nI hope you enjoy {activity} in {city} 😁")
            print(f"It will be around {weather_stats[0]} degrees and {weather_stats[1]}.")
            print("\nHere are some tunes to groove to:")
            for i, song in songs.items():
                print(f"{i}. {song['song_name']} by {song['artist_name']} from {song['album_name']}. 🎶")
                print(f"Song Link: {song['song_link']}\n")
            break
        else:
            print("Invalid Entry: enter 'b' or 'e'")

    while True:
        see_another_genre = input("Would you like to see similar songs from another genre? Type 'y' for yes or 'n' for no: ")
        if see_another_genre == 'y':
            genre = select_genre()
            songs = get_songs_from_spotify(genre, query_words, 5)
            final_response(query_words, activity, city, weather_stats, songs)
        elif see_another_genre == 'n':
            print("Awesome, enjoy your day with some great music! 🌟")
            exit()
        else:
            print("Invalid Entry: enter 'y' or 'n'")
    return True


# Main function to execute the WeatherTunes application
if __name__ == "__main__":
    status = intro_page()
    if status == 'exit':
        exit()
    weather_stats, city = weather_forecast(WEATHER_API_KEY)
    print(weather_stats, city)
    if isinstance(weather_stats, tuple):
        activity = users_activity()
        query_words = gpt_query_words(weather_stats, activity)
        print("Generating song recommendations based on your preferences...\n")
        songs = {}
        genre = select_genre()
        songs = get_songs_from_spotify(genre, query_words, 5)
        final_response(query_words, activity, city, weather_stats, songs)
