import os
import requests
import sys
from api_key import *  # Imports SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
from spotify_genres import genres  # List of genres from Spotify

def get_spotify_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    })

    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

def get_spotify_genres():
    token = get_spotify_token()
    genre_url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
    response = requests.get(genre_url, headers={
        'Authorization': f'Bearer {token}'
    })
    genres = response.json()['genres']
    return genres

def select_genre():
    while True:
        show_genres = show_genre_list()
        if show_genres:
            print(list_of_genres())
        genre = input("So what genre are you feeling? ")
        if genre in genres:
            return genre
        else:
            print("Invalid genre. Please try again.")

# Function to prompt user if they want to see a list of genres
def show_genre_list():
    """
    Prompts user if they want to see a list of genres.

    Returns:
    - True if user wants to see the list, False otherwise.
    """
    while True:
        genre_list_request = input("Would you like to see a list of possible genres? Type 'y' if yes and 'n' if no: ")
        if genre_list_request == 'y':
            return True
        elif genre_list_request == 'n':
            return False
        else:
            print("Invalid Entry: enter 'y' or 'n'")

# Function to return list of available genres
def list_of_genres():
    """
    Returns a list of available genres from Spotify.

    Returns:
    - List of genres.
    """
    return genres

def get_songs_from_spotify(genre, query_words, limit):
    """
    Fetches songs from Spotify API based on genres and query words, stores them in SQLite database tables.

    Args:
    - query_words (str): Keywords used to refine Spotify API search.

    Returns:
    - None
    """
    SPOTIFY_API_KEY = get_spotify_token()
    headers = {"Authorization": f"Bearer {SPOTIFY_API_KEY}"}

    final_query = f"genre: {genre} {' '.join(query_words)}"

    params = {
        "q": final_query,
        "type": "track",
        "limit": limit
    }

    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    data = response.json()

    if "error" in data:
        # Handle API error response
        print(f"Error from Spotify API: {data['error']['message']}")
        sys.exit(0)

    songs_dict = {}

    for i, item in enumerate(data['tracks']['items']):
        # Extract song details from API response
        song_name = item['name']
        artist_name = item['artists'][0]['name']
        album_name = item['album']['name']
        song_link = item['external_urls']['spotify']
        songs_dict[i + 1] = {
            "song_name": song_name,
            "artist_name": artist_name,
            "album_name": album_name,
            "song_link": song_link
        }
    return songs_dict
