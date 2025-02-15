import logging
from functools import wraps

from fastapi import HTTPException, status


def handle_http_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as e:
            logging.error(f"Exception: {e}")
            raise e
        except Exception as e:
            logging.error(f"Exception: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Произошла непредвиденная ошибка: {e}",
            )

    return wrapper
