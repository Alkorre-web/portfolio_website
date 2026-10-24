from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# 1. Подключение
try:
    client = MongoClient("mongodb://admin:admin123@localhost:27017", serverSelectionTimeoutMS=2000)
    # Пингуем сервер, чтобы проверить соединение
    client.admin.command('ping')
    print("✅ Успешное подключение к MongoDB!")
except ConnectionFailure:
    print("❌ Ошибка: Не удалось подключиться к MongoDB. Проверь, запущен ли контейнер.")
    exit()

# 2. Выбрать базу данных и коллекцию
db = client["portfolio_db"]
artifacts = db["artifacts"]

# 3. Добавить ещё один тестовый документ (чтобы убедиться, что Python может писать)
new_doc = {
    "title": "OpenAPI Контракт",
    "type": "contract",
    "category": "api",
    "tags": ["swagger", "yaml"],
    "author": "Лобашев Андрей"
}
result = artifacts.insert_one(new_doc)
print(f"✅ Документ добавлен с ID: {result.inserted_id}")

# 4. Найти и вывести все документы
print("\n📄 Все документы в коллекции 'artifacts':")
for doc in artifacts.find():
    print(f"- {doc['title']} (Тип: {doc['type']})")

# Закрываем соединение
client.close()