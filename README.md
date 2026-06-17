# Виджет банковских операций клиента

## Проект, над которым я работаю - это виджет, который показывает несколько последних успешных банковских операций клиента.

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/alexandrakokh/kokh-homework.git
```
2. Установите зависимости:
```
pip install -r requirements.txt
```

## Использование:

1. Откройте приложение в вашем веб-браузере.
2. Введите номер карты и(или) счёта, дату и время.
3. Отслеживайте свои банковские операции в режиме реального времени.
4. Так же для эффективной работы с большими объемами данных транзакций реализована функция генерирования. 
Эта функция позволяет финансовым аналитикам быстро и удобно находить нужную информацию о транзакциях и проводить анализ данных.
5. Теперь можно использовать функционал конвертации валют.
6. Источником данных о финансовых транзакциях теперь может быть не только JSON-файл, но и CSV- или XLSX-файл.

## Документация

Для получения дополнительной информации обратитесь к [документации](docs/README.md).

## Тестирование

1. src\__init__.py  100%
2. src\analysis.py  100%
3. src\data_reader.py  81%
4. src\decorators.py  100%
5. src\external_api.py  87%
6. src\generators.py   93%
7. src\logging_config.py  93%
8. src\main.py   72%
9. src\masks.py  87%
10. src\processing.py  72%
11. src\search.py  100%
12. src\utils.py  76%
13. src\widget.py 93%
14. tests\__init__.py  100%
15. tests\conftest.py  77%
16. tests\test_analysis.py  100%
17. tests\test_data_reader.py 100%
18. tests\test_decorators.py   97%
19. tests\test_external_api.py   100%
20. tests\test_generators.py  100%
21. tests\test_main.py  100%
22. tests\test_masks.py   100%
23. tests\test_processing.py 100%
24. tests\test_search.py  100%
25. tests\test_utils.py  100%
26. tests\test_widget.py   100%
------------------------------------------------
TOTAL     92%




## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE).
