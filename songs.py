import os
import requests
import sys
from api_key import *  # Imports SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
import pprint


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


def get_similar(song, limit):
    SPOTIFY_API_KEY = get_spotify_token()
    headers = {"Authorization": f"Bearer {SPOTIFY_API_KEY}"}

# FIRST API CALL, GRAB ID OF USER'S SONG:

    params = {
        "q": song,
        "type": "track",
        "limit": 1
    }

    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    data = response.json()

    if "error" in data:
        # Handle API error response
        print(f"Error from Spotify API: {data['error']['message']}")
        sys.exit(0)

    # pprint.pprint(data)
    song_id = data['tracks']['items'][0]['id']

# SECOND API CALL, FINDING SONGS SIMILAR TO USER ENTERED SONG:

    params = {
        "seed_tracks": song_id,
        "limit": limit
    }

    response = requests.get("https://api.spotify.com/v1/recommendations", headers=headers, params=params)
    data = response.json()

    if "error" in data:
        # Handle API error response
        print(f"Error from Spotify API: {data['error']['message']}")
        sys.exit(0)
    
    songs_dict = {}
    # pprint.pprint(data)
    for i, item in enumerate(data['tracks']):
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


# For testing API calls, commented out for now
'''if __name__ == '__main__':
    similar = get_similar_songs("Not Like Us Kendrick Lamar", 5)
    pprint.pprint(similar)'''