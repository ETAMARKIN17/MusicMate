import unittest
from unittest.mock import patch
from weather_tunes import *


class UnitTests(unittest.TestCase):
    def test_welcome_user(self):
        """
        Test case for welcome_user function.
        """
        self.assertEqual(welcome_user(), True)

    @patch('builtins.input', side_effect="Doing insane backflips")
    def test_users_activity(self, mock_input):
        """
        Test case for users_activity function.
        Mocks user input and checks if returned value is a string.
        """
        keywords = users_activity()
        self.assertIsInstance(keywords, str)

    @patch('builtins.input', side_effect=["n", "hip-hop"])
    def test_get_songs_from_genre(self, mock_input):
        """
        Test case for get_songs_from_genre function.
        Mocks user input and checks if returned value is a list.
        """
        songs = get_songs_from_genre()
        self.assertIsInstance(songs, list)

    @patch('builtins.input', side_effect="y")
    def test_show_genre_list(self, mock_input):
        """
        Test case for show_genre_list function.
        Mocks user input and checks if returned value is True.
        """
        self.assertEqual(show_genre_list(), True)


if __name__ == '__main__':
    unittest.main()
