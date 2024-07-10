import sys
import os
import unittest
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from intro import intro_page


class UnitTests(unittest.TestCase):
    @patch('builtins.input', side_effect=["1"])
    def test_intro_page_login(self, mock_input):
        result = intro_page()
        self.assertEqual(result, 'login')

    @patch('builtins.input', side_effect=["2"])
    def test_intro_page_register(self, mock_input):
        result = intro_page()
        self.assertEqual(result, 'register')

    @patch('builtins.input', side_effect=["3"])
    def test_intro_page_exit(self, mock_input):
        result = intro_page()
        self.assertEqual(result, 'exit')


if __name__ == '__main__':
    unittest.main()
