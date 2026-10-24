import os
import base64
from pymongo import MongoClient
from datetime import datetime

# Подключение к MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017")
db = client["portfolio_db"]
collection = db["artifacts"]

# Очищаем коллекцию перед добавлением
collection.delete_many({})
print("️  Коллекция очищена")

# Путь к папке с файлами
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")

# Функция для чтения текстового файла
def read_text_file(filename):
    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

# Функция для чтения PNG и конвертации в Base64
def read_png_as_base64(filename):
    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# Артефакты для добавления
artifacts = [
    {
        "title": "ТЗ: Описание базы данных PostgreSQL",
        "type": "requirements",
        "category": "backend",
        "description": "Техническое задание на проектирование реляционной базы данных для хранения пользователей и истории смены цветов.",
        "file_name": "ТЗ Описание базы данных PostgreSQL.md",
        "file_type": "md",
        "tags": ["postgresql", "erd", "sql"],
        "version": "1.0.0",
        "author": "Лобашев Андрей",
        "content": read_text_file("ТЗ Описание базы данных PostgreSQL.md"),  # ИСПРАВЛЕНО
        "content_type": "text/markdown",
        "created_at": datetime(2026, 10, 23, 10, 0, 0),
        "updated_at": datetime(2026, 10, 24, 10, 0, 0),
    },
    {
        "title": "ТЗ: Проектирование хранилища артефактов СА в MongoDB",
        "type": "requirements",
        "category": "backend",
        "description": "Техническое задание на проектирование документоориентированного хранилища для артефактов системного аналитика.",
        "file_name": "ТЗ Проектирование хранилища артефактов СА в MongoDB.md",
        "file_type": "md",
        "tags": ["mongodb", "nosql", "artifacts"],
        "version": "1.0.0",
        "author": "Лобашев Андрей",
        "content": read_text_file("ТЗ Проектирование хранилища артефактов СА в MongoDB.md"),
        "content_type": "text/markdown",
        "created_at": datetime(2026, 10, 24, 11, 0, 0),
        "updated_at": datetime(2026, 10, 24, 11, 0, 0),
    },
    {
        "title": "ТЗ: Фронтенд сайт-портфолио",
        "type": "requirements",
        "category": "frontend",
        "description": "Техническое задание на разработку фронтенда сайта-портфолио системного аналитика.",
        "file_name": "frontend ТЗ сайт-портфолио.md",
        "file_type": "md",
        "tags": ["frontend", "html", "css", "javascript"],
        "version": "1.0.0",
        "author": "Лобашев Андрей",
        "content": read_text_file("frontend ТЗ сайт-портфолио.md"),
        "content_type": "text/markdown",
        "created_at": datetime(2026, 10, 24, 14, 0, 0),
        "updated_at": datetime(2026, 10, 24, 14, 0, 0),
    },
    {
        "title": "ER-диаграмма базы данных",
        "type": "diagram",
        "category": "architecture",
        "description": "Схема связей таблиц users, user_current_colors и user_color_history в PostgreSQL.",
        "file_name": "er-diagram.png",
        "file_type": "png",
        "tags": ["erd", "uml", "postgresql"],
        "version": "1.0.0",
        "author": "Лобашев Андрей",
        "content": read_png_as_base64("er-diagram.png"),
        "content_type": "image/png",
        "created_at": datetime(2026, 10, 24, 13, 0, 0),
        "updated_at": datetime(2026, 10, 24, 13, 0, 0),
    },
]

# Вставляем все документы
result = collection.insert_many(artifacts)
print(f"✅ Добавлено {len(result.inserted_ids)} артефактов в MongoDB")

# Выводим список добавленных
for doc in artifacts:
    print(f"  - {doc['title']}")