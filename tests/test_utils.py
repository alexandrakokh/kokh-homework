import unittest
from unittest.mock import patch, mock_open
from src.utils import read_json_file


class TestReadJsonFile(unittest.TestCase):


    @patch('builtins.open', mock_open(read_data='[]'))
    @patch('os.path.exists', return_value=True)
    def test_empty_list(self, mock_exists, mock_file):
        result = read_json_file('test.json')
        self.assertEqual(result, [])


    @patch('builtins.open', mock_open(read_data='"not a list"'))
    @patch('os.path.exists', return_value=True)
    def test_not_a_list(self, mock_exists, mock_file):
        result = read_json_file('test.json')
        self.assertEqual(result, [])

    @patch('builtins.open', mock_open(read_data='[{"id": 1, "amount": 100}]'))
    @patch('os.path.exists', return_value=True)
    def test_valid_list(self, mock_exists, mock_file):
        result = read_json_file('test.json')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 1)