import logging
import os
import json
import pandas as pd

from io import BytesIO
from typing import Annotated
from fastapi import (APIRouter, BackgroundTasks, Depends, File, HTTPException,
                     UploadFile, Form)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.batch_schema import Current_Batch, List_Batch_Read
from app.core.database import get_asyncsession
from app.repositories.batch import BatchRepository
from app.storage import minio_storage
# НАдо будет проверить
from app.utils.check_auth import (get_current_admin_user,
                                  get_current_assessor_user)
from app.utils.exceptions import handle_http_exceptions
from app.utils.uploaded_file import upload_file
from app.core.config import settings

router = APIRouter()

bucket_name = settings.BUCKET_NAME

async def load_file_in_minio(object_name: str, file_path: str):
    try:
        minio_storage.upload_data(bucket_name, object_name, file_path)
    except Exception as e:
        logging.info(f"Failed to upload file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {e}")
    finally:
        # Удаление временного файла (если не используется в фоновой задаче)
        if os.path.exists(file_path):
            os.remove(file_path)


async def create_task(batch_id:int, config:dict, session: AsyncSession):
        #1.cкачиваем файл
        file_response = 0

        df = pd.read_csv(BytesIO(file_response.content, encoding='utf-8'), sep=';')
        tasks = []
        task_data = {}

        session.add_all(tasks)

        await session.commit()

#логику в сервис запихни
@handle_http_exceptions
@router.post(
    "/api/batches",
    description="""
        Загрузка нового пакета (JSON + архив).
     - Параметры: настройки батча (приоритет, коэффициент перекрытия, тип оценки).
""",
)
async def proccessing_data(
    config: Annotated[str, Form()],
    backgrond_task: BackgroundTasks,
    file: UploadFile = File(...),
    #user = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_asyncsession),
):
    try:
        # Загрузка файла в S3 возможно отдельным сервисом выделить надо будет
        filepath = await upload_file(file)
        filename = file.filename
        backgrond_task.add_task(load_file_in_minio, filename, filepath)
        # Загрузка в POSTGRESQL

        data = config.module_dump()
        batch_db = BatchRepository(session)
        batch_id = await batch_db.add_one(data=data)

        session.commit()  # Сохранение изменений в БД

        logging.info(f"Batch {batch_id} added ")
        
        batch_config = json.loads(config)

        backgrond_task.add_task(create_task, batch_id, batch_config)
        
    except json.JSONDecodeError:
        session.rollback()
        raise HTTPException(400, "Invalid JSON config")
    except Exception as e:
        session.rollback()
        raise HTTPException(500, f"Batch creation failed: {str(e)}")



@handle_http_exceptions
@router.get("/api/batches", summary="Список Батчей", response_model=List_Batch_Read)
async def get_assessments(session: AsyncSession = Depends(get_asyncsession)):
    batch_db = BatchRepository(session)
    return await batch_db.find_all()


@handle_http_exceptions
@router.get(
    "/api/batches",
    summary="Список Батчей фильтрованный по типу разметки",
    response_model=List_Batch_Read,
)
async def get_assessments(
    type_markup: str, session: AsyncSession = Depends(get_asyncsession)
):

    batch_db = BatchRepository(session)
    return await batch_db.filter_find_all(type_markup=type_markup)


@router.get(
    "/api/batches{id}",
    summary="Получение статуса и прогресса пакета.",
    response_model=Current_Batch,
)
async def get_batch(id: int, session: AsyncSession = Depends(get_asyncsession)):
    batch_db = BatchRepository(session)
    return await batch_db.find_one(id=id)


@router.put("/api/batches{id}")
async def update_batch(id: int):
    pass


@router.get(
    "/api/batches{id}/results", summary="Экспорт размеченных данных (JSON/CSV)."
)
async def get_results(id: int, session: AsyncSession = Depends(get_asyncsession)):
    batch_db = BatchRepository(session)
    batch =  await batch_db.find_one(id=id)
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    else:
        object_name = batch.object_name
        minio_storage.download_data(bucket_name, object_name)
        
        
        
        
