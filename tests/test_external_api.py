import unittest
from unittest.mock import patch, Mock
import requests
from src.external_api import convert_to_rubles, _get_exchange_rate
from dotenv import load_dotenv

load_dotenv()

class TestConvertToRubles(unittest.TestCase):

    @patch('src.external_api._get_exchange_rate', return_value=90.0)
    def test_usd_conversion(self, mock_get_rate):
        """Тест конвертации USD в рубли."""
        transaction = {'amount': 10, 'currency': 'USD'}
        result = convert_to_rubles(transaction)
        self.assertAlmostEqual(result, 900.0)
        mock_get_rate.assert_called_once_with('USD')

    @patch('src.external_api._get_exchange_rate', return_value=100.0)
    def test_eur_conversion(self, mock_get_rate):
        """Тест конвертации EUR в рубли."""
        transaction = {'amount': 5, 'currency': 'EUR'}
        result = convert_to_rubles(transaction)
        self.assertAlmostEqual(result, 500.0)
        mock_get_rate.assert_called_once_with('EUR')

    def test_rub_no_conversion(self):
        """Тест для валюты RUB — конвертация не требуется."""
        transaction = {'amount': 1000, 'currency': 'RUB'}
        result = convert_to_rubles(transaction)
        self.assertEqual(result, 1000.0)

    def test_unsupported_currency(self):
        """Тест для неподдерживаемой валюты."""
        transaction = {'amount': 100, 'currency': 'GBP'}
        with self.assertRaises(ValueError) as context:
            convert_to_rubles(transaction)
        self.assertIn("Неподдерживаемая валюта", str(context.exception))

    def test_invalid_amount_type(self):
        """Тест для некорректного типа суммы."""
        transaction = {'amount': 'invalid', 'currency': 'USD'}
        with self.assertRaises(ValueError) as context:
            convert_to_rubles(transaction)
        self.assertIn("Некорректная сумма транзакции", str(context.exception))

    def test_negative_amount(self):
        """Тест для отрицательной суммы."""
        transaction = {'amount': -100, 'currency': 'USD'}
        with self.assertRaises(ValueError) as context:
            convert_to_rubles(transaction)
        self.assertIn("Некорректная сумма транзакции", str(context.exception))

    @patch('src.external_api.os.environ.get', return_value='test_api_key')
    @patch('requests.get')
    def test_successful_rate_fetch(self, mock_get, mock_os_environ_get):
        """Тест успешного получения курса из API."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': True,
            'result': 90.0
        }
        mock_get.return_value = mock_response

        rate = _get_exchange_rate('USD')
        self.assertEqual(rate, 90.0)

        # Проверка параметров запроса
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertIn('https://api.apilayer.com/exchangerates_data/convert', args[0])
        self.assertEqual(kwargs['params']['from'], 'USD')
        self.assertEqual(kwargs['params']['to'], 'RUB')
        self.assertEqual(kwargs['params']['amount'], 1)
        self.assertEqual(kwargs['headers']['apikey'], 'test_api_key')

    @patch('src.external_api.os.environ.get', return_value='test_api_key')
    @patch('requests.get')
    def test_api_error_response(self, mock_get, mock_os_environ_get):
        """Тест обработки ошибки от API."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': False,
            'error': {'info': 'Invalid API key'}
        }
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError) as context:
            _get_exchange_rate('USD')
        self.assertIn("API error", str(context.exception))

    @patch('src.external_api.os.environ.get', return_value='test_api_key')
    @patch('requests.get')
    def test_network_error(self, mock_get, mock_os_environ_get):
        """Тест обработки сетевой ошибки."""
        mock_get.side_effect = requests.exceptions.RequestException('Connection failed')

        with self.assertRaises(ConnectionError) as context:
            _get_exchange_rate('USD')
        self.assertIn("Ошибка сети", str(context.exception))

    @patch('src.external_api.os.environ.get', return_value='test_api_key')
    @patch('requests.get')
    def test_parsing_error(self, mock_get, mock_os_environ_get):
        """Тест обработки ошибки парсинга JSON."""
        mock_response = Mock()
        mock_response.status_code = 200
        # Некорректный JSON — отсутствует поле 'result'
        mock_response.json.return_value = {'success': True}
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError) as context:
            _get_exchange_rate('USD')
        self.assertIn("Ошибка парсинга", str(context.exception))

    @patch('src.external_api.os.environ.get', return_value=None)
    def test_missing_api_key(self, mock_os_environ_get):
        """Тест отсутствия API-ключа."""
        with self.assertRaises(ValueError) as context:
            _get_exchange_rate('USD')
        self.assertIn("API key not found", str(context.exception))