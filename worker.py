import json
import logging
import os

import pika
from fastapi import HTTPException

from app.config import settings
from app.storage import minio_storage


def process_file(filename, file_path):
    try:

        object_name = "test" + filename
        # сохранение в MINIO
        minio_storage.upload_data(settings.BUCKET_NAME, object_name, file_path)
        return {
            "message": "File uploaded and processed successfully",
            "file_path": file_path,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="file_queue", durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        file_path = message["file_path"]
        file_name = message["file_name"]
        logging.info()
        process_file(file_path, file_name)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="file_queue", on_message_callback=callback)

    logging.info(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

    if __name__ == "__main__":
        start_worker()
