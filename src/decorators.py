import functools
import sys

def log(filename=None):
    """Декоратор для логирования начала и конца выполнения функции, а также её результатов или возникших ошибок."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Определяем, куда выводить логи
            if filename:
                # Открываем файл для записи (добавление в конец)
                output = open(filename, 'a', encoding='utf-8')
            else:
                # Используем консоль (stdout)
                output = sys.stdout

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)
                # Логируем успешный результат
                print(f"{func.__name__} ok", file=output)
                return result
            except Exception as e:
                # Логируем ошибку и входные параметры
                error_type = type(e).__name__
                print(
                    f"{func.__name__} error: {error_type}. "
                    f"Inputs: {args}, {kwargs}",
                    file=output
                )
                # Перебрасываем исключение дальше
                raise
            finally:
                # Закрываем файл, если логировались в файл
                if filename:
                    output.close()

        return wrapper
    return decorator
