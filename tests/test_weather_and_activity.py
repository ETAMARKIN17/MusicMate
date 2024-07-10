import sys
import os
import unittest
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from weather_and_activity import *


class TestWeatherFunctions(unittest.TestCase):
    @patch('builtins.input', side_effect=['Running'])
    def test_users_activity_valid(self, mock_input):
        result = users_activity()
        self.assertEqual(result, 'Running')

    @patch('builtins.input', side_effect=['This is a very long activity that exceeds the character limit', 'Running'])
    def test_users_activity_invalid_then_valid(self, mock_input):
        result = users_activity()
        self.assertEqual(result, 'Running')


if __name__ == '__main__':
    unittest.main()
