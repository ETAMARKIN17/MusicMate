import os
import random
import requests
import sys
from flask import flash
from get_spotify_api_key import *  # Imports SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET


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
         flash(f"Sorry, there was an error. Please try again. Error from Spotify API: {data['error']['message']}","error")
         return None 
       
        

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
        return None 

    songs_dict = {}

    for i, item in enumerate(data['tracks']):
        # Extract song details from API response
        song_name = item['name']
        artist_name = item['artists'][0]['name']
        album_name = item['album']['name']
        song_link = item['external_urls']['spotify']
        uri = item['uri']
        songs_dict[i + 1] = {
            "song_name": song_name,
            "artist_name": artist_name,
            "album_name": album_name,
            "song_link": song_link,
            "uri": uri
        }

    return songs_dict


# Function to fetch playlist from Spotify based on query words and genre
def get_playlist_from_spotify(query_words, genre):
    SPOTIFY_API_KEY = get_spotify_token()
    headers = {"Authorization": f"Bearer {SPOTIFY_API_KEY}"}

    final_query = f"{genre} {' '.join(query_words)}"

    params = {
        "q": final_query,
        "type": "playlist",
        "limit": 5
    }

    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    data = response.json()

    if "error" in data:
         flash(f"Sorry, there was an error. Please try again. Error from Spotify API: {data['error']['message']}","error")
         return None

    playlists = data['playlists']['items']
    if not playlists:
        flash(f"Sorry, there was an error. Please try again. Error from Spotify API: No playlist found that matches critera","error")
        return None

    selected_playlist = random.choice(playlists)
    playlist_id = selected_playlist['id']

    # Get tracks from the playlist
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    params = {
        "limit": 20
    }
    response = requests.get(playlist_url, headers=headers, params=params)
    playlist_data = response.json()

    if "error" in playlist_data:
        flash(f"Sorry, there was an error. Please try again. Error from Spotify API: {playlist_data['error']['message']}","error")
        return None
        
    tracks = playlist_data['items']
    return tracks


# Function to get songs from Spotify based on genre and query words
def get_songs_from_playlist(genre, tracks):
    if tracks is None:
        flash("Sorry, No tracks found.", "error")
        print("Flash message set: No tracks found or there was an error retrieving the playlist.")
        return {}
    songs_dict = {}
    for i, track in enumerate(tracks):
        song_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        album_name = track['track']['album']['name']
        # Handle the case where 'external_urls' might not have the 'spotify' key
        song_link = track['track'].get('external_urls', {}).get('spotify', 'URL not available')
        uri = track['track']['uri']
        # Handle the case where album images might be empty or missing
        album_cover = None
        if 'images' in track['track']['album'] and len(track['track']['album']['images']) > 0:
            album_cover = track['track']['album']['images'][0].get('url', None)

        popularity = track['track']['popularity']

        songs_dict[i + 1] = {
            "song_name": song_name,
            "artist_name": artist_name,
            "album_name": album_name,
            "song_link": song_link,
            "album_cover": album_cover,
            "popularity": popularity,
            "uri": uri,
        }

    print(uri)
    return songs_dict
