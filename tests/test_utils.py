import unittest
from unittest.mock import patch, mock_open
from src.utils import read_json_file

class TestReadJsonFile(unittest.TestCase):

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_empty_list(self, mock_file, mock_exists):
        result = read_json_file('test.json')
        self.assertEqual(result, [])

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='"not a list"')
    def test_not_a_list(self, mock_file, mock_exists):
        result = read_json_file('test.json')
        self.assertEqual(result, [])

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='[{"id": 1, "amount": 100}]')
    def test_valid_list(self, mock_file, mock_exists):
        result = read_json_file('test.json')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 1)