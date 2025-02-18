from fastapi import Depends, HTTPException, Request, status
from jwt import PyJWTError, decode

from app.core.config import get_auth_data
from app.utils.exceptions import NoJwtException

auth_data = get_auth_data()


def decoded_token(
    token: str | bytes,
    secret_key: str = auth_data["secret_key"],
    algorithm: str = auth_data["algorithm"],
):
    try:
        decoded = decode(token, secret_key, algorithm)
        return decoded
    except PyJWTError:
        raise NoJwtException


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не найден"
        )
    return token


@handle_http_exceptions
async def get_current_user(
    token: str = Depends(get_token), session=Depends(get_asyncsession)
):
    payload = decoded_token(token)
    expire: str = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise NoUserIdException
    user = await find_one_or_none(session=session, id=int(user_id))

    if not user:
        raise UserNotFoundException
    return user


async def get_current_admin_user(current_user=Depends(get_current_user)):
    if current_user.role == "ADMIN":
        return current_user
    raise ForbiddenExcept


async def get_current_assessor_user(current_user=Depends(get_current_user)):
    if current_user.role == "ASSESSOR":
        return current_user
    raise ForbiddenExcept
