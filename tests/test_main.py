import sys
import os
import unittest
from unittest.mock import patch

# Add the main directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import start


class UnitTests(unittest.TestCase):
    @patch('builtins.input', side_effect=["3"])
    def test_start_exit(self, mock_input):
        """
        Test case for the start function to check if 'exit' choice works correctly.
        """
        status = start()
        self.assertEqual(status, 'exit')


if __name__ == '__main__':
    unittest.main()
