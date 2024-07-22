import requests
import sys
from get_spotify_api_key import *  # Imports SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
import urllib.parse
from datetime import datetime
from flask import Flask, redirect, request, session, url_for, jsonify
from dotenv import load_dotenv

# Load environmental variables from .env
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
BASE_URL = 'https://api.spotify.com/v1/'
AUTH_URL = 'https://accounts.spotify.com/authorize'
REDIRECT_URI = 'https://armanisilk-memberavenue-5000.codio.io/callback'  # Change based on where you're hosting webiste
TOKEN_URL = 'https://accounts.spotify.com/api/token'


# Called in the dashboard page, probably going to redirect to spotifys auth page and get all the stuff we need to make our api calls
def get_spotify_auth_url():
    scope = 'playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'
    #playlist-read-private

    params = {
        'client_id': SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True,
    }


    auth_url= f'{AUTH_URL}?{urllib.parse.urlencode(params)}'
    return auth_url


def get_token_info(auth_code):
    request_body = {
        'code': auth_code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=request_body)
    return response.json()


def refresh_token():
    if 'refresh_token' not in session:
        return redirect(url_for('dashboard'))

    if datetime.now().timestamp() > session['expires_at']:
        request_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET,
        }

        response = requests.post(TOKEN_URL, data=request_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        return redirect(url_for('dashboard'))


def get_user_info():
    if 'access_token' not in session:
        return redirect(url_for('dashboard'))

    if datetime.now().timestamp() > session['expires_at']:
        return redirect(url_for('refresh_token'))

    headers = {
        "Authorization": f"Bearer {session['access_token']}",
    }

    response = requests.get(BASE_URL + 'me', headers=headers)
    return response.json()


def get_user_playlists():
    if 'access_token' not in session:
        return None

    if datetime.now().timestamp() > session['expires_at']:
        refresh_token()

    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }

    response = requests.get(BASE_URL + 'me/playlists', headers=headers)
    #print('actually changed')
    # Log additional information for debugging
    #print(session['access_token'])
    
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        return {"error": response.json().get('error', 'Unknown error occurred')}



def create_playlist_helper(name, description, public):
    user_info = get_user_info()
    user_id = user_info['id']

    if 'access_token' not in session:
        return redirect(url_for('dashboard'))

    if datetime.now().timestamp() > session['expires_at']:
        return redirect(url_for('refresh_token'))

    headers = {
        "Authorization": f"Bearer {session['access_token']}",
        "Content-Type": "application/json"
        }

    data = {
        'name': name,
        'description': description,
        'public': public,
    }

    response = requests.post(BASE_URL + f'users/{user_id}/playlists', headers=headers, json=data)
    return response.json()


def add_to_playlist_helper(playlist_id, track_uri):
    if 'access_token' not in session:
        return redirect(url_for('dashboard'))

    if datetime.now().timestamp() > session['expires_at']:
        return redirect(url_for(refresh_token))  # create this endpoint

    headers = {
        "Authorization": f"Bearer {session['access_token']}",
        "Content-Type": "application/json",
        }
    
    data = {
        'uris': [track_uri]
    }

    response = requests.post(BASE_URL + f'playlists/{playlist_id}/tracks', headers=headers, json=data)

    print(track_uri)
    print(response.json())

    if response.status_code == 200:
        return response.json()  # Success, return the response JSON
    else:
        return {"error": response.json().get('error', 'Unknown error occurred')}
