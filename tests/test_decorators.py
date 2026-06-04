import pytest
import os
from src.decorators import log


# Вспомогательная функция для очистки тестового файла
def cleanup_test_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

class TestLogDecorator:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Очистка тестовых файлов перед и после всех тестов"""
        cleanup_test_file("test_log.txt")
        yield
        cleanup_test_file("test_log.txt")

    def test_successful_execution_console(self, capsys):
        """Тест успешного выполнения функции с логированием в консоль"""
        @log()
        def test_function(x, y):
            return x + y

        result = test_function(1, 2)

        # Проверяем результат функции
        assert result == 3

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "test_function ok" in captured.out
        assert captured.err == ""  # ошибок в stderr быть не должно

    def test_exception_handling_console(self, capsys):
        """Тест обработки исключения с логированием в консоль"""
        @log()
        def problematic_function(value):
            if value < 0:
                raise ValueError("Negative value not allowed")
            return value ** 2

        with pytest.raises(ValueError, match="Negative value not allowed"):
            problematic_function(-5)

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        expected_error = "problematic_function error: ValueError. Inputs: (-5,), {}"
        assert expected_error in captured.out

    def test_successful_execution_file(self):
        """Тест успешного выполнения функции с логированием в файл"""
        filename = "test_log.txt"

        @log(filename=filename)
        def another_test_function(a, b, c=0):
            return a * b + c

        result = another_test_function(2, 3, c=1)

        # Проверяем результат функции
        assert result == 7

        # Проверяем содержимое файла
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        assert content == "another_test_function ok"

    def test_exception_handling_file(self):
        """Тест обработки исключения с логированием в файл"""
        filename = "test_log.txt"

        @log(filename=filename)
        def error_prone_function(items):
            if not items:
                raise IndexError("Empty list not allowed")
            return len(items)

        with pytest.raises(IndexError, match="Empty list not allowed"):
            error_prone_function([])

        # Проверяем содержимое файла
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        expected_error = "error_prone_function error: IndexError. Inputs: ([],), {}"
        assert content == expected_error

    def test_multiple_calls_file(self):
        """Тест нескольких вызовов функции с логированием в один файл"""
        filename = "test_log.txt"

        @log(filename=filename)
        def simple_function(x):
            return x * 2

        # Несколько вызовов функции
        simple_function(5)
        simple_function(10)

        # Проверяем содержимое файла — должно быть две записи
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        assert len(lines) == 2
        assert lines[0].strip() == "simple_function ok"
        assert lines[1].strip() == "simple_function ok"

    def test_kwargs_handling_console(self, capsys):
        """Тест обработки именованных аргументов с логированием в консоль"""
        @log()
        def function_with_kwargs(a, b=0, c=None):
            return f"{a}-{b}-{c}"

        result = function_with_kwargs(1, b=2, c="test")

        # Проверяем результат функции
        assert result == "1-2-test"

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        expected_output = "function_with_kwargs ok"
        assert expected_output in captured.out

    def test_mixed_args_exception_console(self, capsys):
        """Тест обработки смешанных аргументов при исключении в консоли"""
        @log()
        def mixed_args_function(x, y, z=0, debug=False):
            if debug:
                raise RuntimeError("Debug mode not implemented")
            return x + y + z

        with pytest.raises(RuntimeError, match="Debug mode not implemented"):
            mixed_args_function(1, 2, z=3, debug=True)

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        expected_error = (
            "mixed_args_function error: RuntimeError. "
            "Inputs: (1, 2), {'z': 3, 'debug': True}"
        )
        assert expected_error in captured.out

    def test_no_arguments_function(self, capsys):
        """Тест функции без аргументов"""
        @log()
        def no_args_function():
            return "no args"

        result = no_args_function()

        # Проверяем результат функции
        assert result == "no args"

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "no_args_function ok" in captured.out