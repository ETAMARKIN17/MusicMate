import os
import requests
import sys
from api_key import *  # Imports SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET

# Function to get Spotify token
def get_spotify_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    })

    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

# Function to get available genres from Spotify
def get_spotify_genres():
    token = get_spotify_token()
    genre_url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
    response = requests.get(genre_url, headers={
        'Authorization': f'Bearer {token}'
    })
    genres = response.json()['genres']
    return genres

# Function to get songs from Spotify based on genre and query words
def get_songs_from_spotify(genre, query_words, limit):
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
