import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Load Spotify client ID and client secret from environment variables
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


def get_spotify_api_key():
    """
    Retrieves Spotify API access token using client credentials flow.

    Returns:
    - str: Access token for Spotify API authentication.
    """
    CLIENT_ID = SPOTIFY_CLIENT_ID
    CLIENT_SECRET = SPOTIFY_CLIENT_SECRET

    AUTH_URL = "https://accounts.spotify.com/api/token"

    # Send POST request to Spotify API to obtain access token
    auth_response = requests.post(AUTH_URL, {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })

    auth_response_data = auth_response.json()
    return auth_response_data["access_token"]
