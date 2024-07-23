import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Load Spotify client ID and client secret from environment variables
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')


def get_spotify_api_key():
    # Spotify API credentials
    CLIENT_ID = SPOTIFY_CLIENT_ID
    CLIENT_SECRET = SPOTIFY_CLIENT_SECRET

    # Spotify authorization URL
    AUTH_URL = "https://accounts.spotify.com/api/token"

    # Send POST request to Spotify API to obtain access token
    auth_response = requests.post(AUTH_URL, {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })

    # Parse the JSON response to get the access token
    auth_response_data = auth_response.json()
    return auth_response_data["access_token"]
