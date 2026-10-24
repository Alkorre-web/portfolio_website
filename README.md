# Сайт-портфолио СА: Смена цвета фона + Артефакты

## Описание
Сайт демонстрирует навыки системного аналитика: проектирование БД, API-контрактов, работу с PostgreSQL, Redis, MongoDB.

## Функционал
- Регистрация и авторизация пользователей (JWT)
- Смена цвета фона сайта (RGB 0-255)
- Сохранение истории смены цветов
- Просмотр артефактов СА (ТЗ, диаграммы, контракты)
- Фильтрация артефактов по категориям

## Технологии
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: PostgreSQL (пользователи, цвета), MongoDB (артефакты)
- **Cache**: Redis (кэширование списка артефактов)
- **Frontend**: HTML/CSS/JavaScript
- **Deployment**: Docker, Docker Compose

## Быстрый старт

### 1. Клонировать репозиторий
```bash
git clone https://github.com/Alkorre-web/pet-project.git
cd pet-project
