import unittest
from unittest.mock import patch, Mock
from src.external_api import convert_to_rubles, _get_exchange_rate

class TestConvertToRubles(unittest.TestCase):

    @patch('src.external_api._get_exchange_rate', return_value=90.0)
    def test_usd_conversion(self, mock_get_rate):
        transaction = {'amount': 10, 'currency': 'USD'}
        result = convert_to_rubles(transaction)
        self.assertAlmostEqual(result, 900.0)

    @patch('src.external_api._get_exchange_rate', return_value=100.0)
    def test_eur_conversion(self, mock_get_rate):
        transaction = {'amount': 5, 'currency': 'EUR'}
        result = convert_to_rubles(transaction)
        self.assertAlmostEqual(result, 500.0)

    def test_rub_no_conversion(self):
        transaction = {'amount': 1000, 'currency': 'RUB'}
        result = convert_to_rubles(transaction)
        self.assertEqual(result, 1000.0)

    @patch('requests.get')
    def test_successful_rate_fetch(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'rates': {'RUB': 90.0}}
        mock_get.return_value = mock_response

        rate = _get_exchange_rate('USD')
        self.assertEqual(rate, 90.0)

    @patch('requests.get')
    def test_failed_rate_fetch(self, mock_get):
        mock_get.side_effect = Exception('API error')
        rate = _get_exchange_rate('USD')
        self.assertIsNone(rate)  # Проверяем, что возвращается None при ошибке