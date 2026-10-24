from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId
import os

# 1. Прямое подключение к MongoDB (без сложных классов)
mongo_url = os.getenv("MONGODB_URL", "mongodb://admin:admin123@localhost:27017")
client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)

# 2. Проверка подключения
try:
    client.admin.command('ping')
    print("✅ MongoDB подключена успешно!")
except ConnectionFailure as e:
    print(f"❌ Ошибка подключения к MongoDB: {e}")

# 3. Прямой доступ к базе и коллекции
db = client["portfolio_db"]
artifacts_collection = db["artifacts"]

# --- Функции для работы с артефактами ---

def get_all_artifacts(limit: int = 100, skip: int = 0):
    """Получить все артефакты с пагинацией"""
    artifacts = artifacts_collection.find().sort("created_at", -1).skip(skip).limit(limit)
    return list(artifacts)

def get_artifact_by_id(artifact_id: str):
    """Получить конкретный артефакт по ID"""
    return artifacts_collection.find_one({"_id": ObjectId(artifact_id)})

def get_artifacts_by_category(category: str):
    """Фильтрация артефактов по категории"""
    artifacts = artifacts_collection.find({"category": category}).sort("created_at", -1)
    return list(artifacts)

def get_artifacts_by_tag(tag: str):
    """Поиск артефактов по тегу"""
    artifacts = artifacts_collection.find({"tags": tag}).sort("created_at", -1)
    return list(artifacts)