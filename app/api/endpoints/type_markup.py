from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.type_markup_schemas import (Create_Type_MarkUp,
                                                 List_Type_MarkUp_Read)
from app.core.database import get_asyncsession
from app.repositories.type_markup import TypeMarkupRepository
from app.utils.exceptions import handle_http_exceptions

router = APIRouter()


@handle_http_exceptions
@router.post("/api/typemarkup", summary="Добавление нового Типа разметки.")
async def add_type_markup(
    data: Create_Type_MarkUp, session: AsyncSession = Depends(get_asyncsession)
):
    dict = data.model_dump
    await TypeMarkupRepository.add_one(data=dict, session=session)


@handle_http_exceptions
@router.get(
    "/api/typemarkup",
    summary="Список Типов разметки",
    response_model=List_Type_MarkUp_Read,
)
async def get_assessments(session: AsyncSession = Depends(get_asyncsession)):
    return await TypeMarkupRepository.get_all(session=session)
