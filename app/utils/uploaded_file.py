import uuid

from fastapi import UploadFile

from app.core.config import UPLOAD_FOLDER


async def upload_file(uploaded_file: UploadFile):
    unique_filename = f"{uuid.uuid4().hex}_{uploaded_file.filename}"
    file_path = UPLOAD_FOLDER / unique_filename
    with open(file_path, "wb") as f:
        content = await uploaded_file.read()
        f.write(content)
    return str(file_path)
