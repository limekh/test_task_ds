# Test task DS
## DataFrame Summarizer
### Клонирование и установка 
```bash
git clone https://github.com/limekh/test_task_ds.git
cd test_task_ds
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```
### Запуск 
```
python main.py
```
Результат будет сохранен в файл `iris_stat.html`. Формат можно изменить в инициализации `summarizer` (`output_type="markdown"/"html"/"xlsx"`), находящейся в `main.py`
### Запуск тестов
```
python -m pytest tests/ -v
```
### Технические требования
- Python 3.10 или выше
- Основные библиотеки: `pandas`, `numpy`
- Опционально: `openpyxl`(xlsx), `tabulate`(markdown), `pytest`(тесты)

### Структура проекта
- summarizer/
    - __init__.py
    - summarizer.py
- tests/
    - test_summarizer.py
- main.py
- requirements.txt
- README.md
