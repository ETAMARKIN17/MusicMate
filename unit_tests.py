import unittest
from unittest.mock import patch, MagicMock
from get_spotify_api_key import *
from match_the_day import *
from match_the_mood import *
from match_the_song import *
from save_songs import *
from songs import *
from user_accounts import *


class UnitTests(unittest.TestCase):
    @patch('get_spotify_api_key.requests.post')
    def test_get_spotify_api_key(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "test_token"}
        mock_post.return_value = mock_response

        token = get_spotify_api_key()
        self.assertEqual(token, "test_token")


    @patch('match_the_day.requests.get')
    def test_weather_forecast(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "location": {"name": "New York", "region": "NY"},
            "current": {"temp_f": 75, "condition": {"text": "Sunny"}}
        }
        mock_get.return_value = mock_response

        result = weather_forecast("New York", "fake_api_key")
        self.assertEqual(result, ((75, "Sunny"), "New York"))


    @patch('match_the_day.weather_forecast')
    @patch('match_the_day.gpt_query_words')
    @patch('match_the_day.recommend_songs')
    def test_get_songs_from_activity(self, mock_recommend_songs, mock_gpt_query_words, mock_weather_forecast):
        mock_weather_forecast.return_value = ((75, "Sunny"), "New York")
        mock_gpt_query_words.return_value = "sunny, jogging"
        mock_recommend_songs.return_value = {"song1": "details"}

        result, weather_stats = get_songs_from_activity("New York", "jogging", "pop")
        self.assertEqual(result, {"song1": "details"})
        self.assertEqual(weather_stats, (75, "Sunny"))


    @patch('match_the_mood.gpt_query_words_mood')
    @patch('match_the_mood.recommend_songs')
    def test_get_songs_from_mood(self, mock_recommend_songs, mock_gpt_query_words_mood):
        mock_gpt_query_words_mood.return_value = "happy, energetic"
        mock_recommend_songs.return_value = {"song1": "details"}

        result, mood = get_songs_from_mood("happy", "pop")
        self.assertEqual(result, {"song1": "details"})
        self.assertEqual(mood, "happy")


    @patch('match_the_song.get_similar')
    def test_get_similar_songs(self, mock_get_similar):
        mock_get_similar.return_value = {"song1": "details"}

        result = get_similar_songs("test_song")
        self.assertEqual(result, {"song1": "details"})


    @patch('songs.get_playlist_from_spotify')
    def test_get_songs_from_playlist(self, mock_get_playlist_from_spotify):
        mock_get_playlist_from_spotify.return_value = [
            {"track": {"name": "song1", "artists": [{"name": "artist1"}], "album": {"name": "album1", "images": [{"url": "link"}]}, "external_urls": {"spotify": "link"}, "popularity": 50, "uri":1}}
        ]

        result = get_songs_from_playlist("pop", mock_get_playlist_from_spotify.return_value)
        self.assertEqual(result[1]["song_name"], "song1")


    def test_hash_password(self):
        password = "password123"
        hashed_password = hash_password(password)
        self.assertTrue(hashed_password.endswith("83d4473e94f"))


if __name__ == '__main__':
    unittest.main()
