import sys
import os
import unittest
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from user_accounts import *


class UnitTests(unittest.TestCase):
    def test_hash_password(self):
        hashed_password = hash_password('hi')
        self.assertEqual(hashed_password, '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4')



if __name__ == '__main__':
    unittest.main()
