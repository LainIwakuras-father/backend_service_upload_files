import os

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.produsser import rabbitmq_client
from app.uploaded_file import upload_file
from app.utils.exceptions import handle_http_exceptions

router = APIRouter()


@handle_http_exceptions
@router.post(
    "/api/batches",
    description="""
        Загрузка нового пакета (JSON + архив).
     - Параметры: настройки батча (приоритет, коэффициент перекрытия, тип оценки).
""",
)
async def proccessing_data(file: UploadFile = File(...)):
    """
    1.загрузка на сервер файлом
    2.парсинг файла(zip,xlsx, csv)
    3.обработка данных
    4.сохранение в MINIO
    5.возврат сообщения что все успешно
    """
    file_path = await upload_file(file)

    try:
        task = {
            "file_path": file_path,
            "file_name": file.filename,
        }
        rabbitmq_client.send_message("file_queue", task)
        return {
            "message": "File uploaded and processed successfully",
            "file_path": file_path,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {e}")
    finally:
        # Удаление временного файла (если не используется в фоновой задаче)
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/api/batches{id}", summary="Получение статуса и прогресса пакета.")
async def get_batch(id: int):
    pass


@router.put("/api/batches{id}")
async def update_batch(id: int):
    pass


@router.get(
    "/api/batches{id}/results", summary="Экспорт размеченных данных (JSON/CSV)."
)
async def get_results(id: int):
    pass


@router.get(
    "/api/assessments", summary="Список заданий для асессора (в зависимости от роли)."
)
async def get_assessments():
    pass
