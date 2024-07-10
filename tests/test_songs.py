import sys
import os
import unittest
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spotify_genres import genres
from songs import *


class TestSpotifyFunctions(unittest.TestCase):
    @patch('builtins.input', side_effect=['y'])
    def test_show_genre_list_yes(self, mock_input):
        result = show_genre_list()
        self.assertTrue(result)

    @patch('builtins.input', side_effect=['n'])
    def test_show_genre_list_no(self, mock_input):
        result = show_genre_list()
        self.assertFalse(result)

    @patch('builtins.input', side_effect=['invalid', 'n'])
    def test_show_genre_list_invalid_then_no(self, mock_input):
        with patch('builtins.print') as mocked_print:
            result = show_genre_list()
            self.assertEqual(mocked_print.call_count, 1)  # Ensure invalid entry message printed once
            self.assertFalse(result)

    def test_list_of_genres(self):
        result = list_of_genres()
        self.assertEqual(result, genres)

if __name__ == '__main__':
    unittest.main()
