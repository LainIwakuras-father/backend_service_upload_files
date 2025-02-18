import logging

from minio import Minio
from minio.error import S3Error

from app.core.config import settings


class Storage:
    def __init__(self, endpoint, access_key, secret_key, secure=False):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )

    def make_bucket(self, bucket_name=settings.BUCKET_NAME):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            logging.info(f"Bucket {bucket_name} created.")
        else:
            logging.info(f"Bucket {bucket_name} already exists.")

    def upload_data(self, bucket_name, object_name, file_path):
        try:
            self.client.fput_object(
                bucket_name=bucket_name, object_name=object_name, file_path=file_path
            )
            return True
        except S3Error as e:
            logging.error(e)
            return False

    def download_data(self, bucket_name, object_name):
        try:
            self.client.get_object(bucket_name=bucket_name, object_name=object_name)
            logging.info(f"File {object_name} downloaded from {bucket_name} bucket.")
        except S3Error as e:
            logging.error(e)
            return False


minio_storage = Storage(
    f"{settings.S3_HOST}:{settings.S3_PORT}", settings.S3_USER, settings.S3_PASSWORD
)
