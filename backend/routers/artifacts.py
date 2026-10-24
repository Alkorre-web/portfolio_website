from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
import json

from database_mongo import (
    get_all_artifacts,
    get_artifact_by_id,
    get_artifacts_by_category,
    get_artifacts_by_tag
)

router = APIRouter(prefix="/api/artifacts", tags=["Artifacts"])


# Вспомогательная функция для сериализации ObjectId
def serialize_doc(doc):
    if doc:
        doc["_id"] = str(doc["_id"])
        if "created_at" in doc and hasattr(doc["created_at"], "isoformat"):
            doc["created_at"] = doc["created_at"].isoformat()
        if "updated_at" in doc and hasattr(doc["updated_at"], "isoformat"):
            doc["updated_at"] = doc["updated_at"].isoformat()
    return doc


@router.get("/", response_model=List[dict])
async def get_artifacts(
        limit: int = Query(100, ge=1, le=1000),
        skip: int = Query(0, ge=0),
        category: Optional[str] = None,
        tag: Optional[str] = None
):
    """
    Получить список артефактов с фильтрацией
    """
    if category:
        artifacts = get_artifacts_by_category(category)
    elif tag:
        artifacts = get_artifacts_by_tag(tag)
    else:
        artifacts = get_all_artifacts(limit=limit, skip=skip)

    # Сериализуем все документы
    return [serialize_doc(doc) for doc in artifacts]


@router.get("/{artifact_id}")
async def get_artifact(artifact_id: str):
    """
    Получить конкретный артефакт по ID
    """
    try:
        artifact = get_artifact_by_id(artifact_id)
        if not artifact:
            raise HTTPException(status_code=404, detail="Артефакт не найден")
        return serialize_doc(artifact)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Неверный ID: {str(e)}")


@router.get("/categories/{category}")
async def get_by_category(category: str):
    """
    Фильтрация по категории
    """
    artifacts = get_artifacts_by_category(category)
    return [serialize_doc(doc) for doc in artifacts]


@router.get("/tags/{tag}")
async def get_by_tag(tag: str):
    """
    Поиск по тегу
    """
    artifacts = get_artifacts_by_tag(tag)
    return [serialize_doc(doc) for doc in artifacts]