import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router as batch_router
from app.storage import minio_storage

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.getLogger("markup_logger")


app = FastAPI(
    title="MarkUpAPI-service upload file",
    description="Сервис загрузки разметки",
    debug=True,
)

app.include_router(batch_router)


origins = ["http://localhost", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


async def main():
    logging.info("Запускаю приложуху...")
    minio_storage.make_bucket()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
