import logging

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.batch_model import Type_MarkUp


class TypeMarkupRepository:

    @staticmethod
    async def add_one(data: dict, session: AsyncSession):
        stmt = insert(Type_MarkUp).values(**data).returning(Type_MarkUp.id)
        await session.execute(stmt)
        logging.debug("Добавлен новый тип разметки")

    @staticmethod
    async def get_all(session: AsyncSession):
        query = select(Type_MarkUp)
        res = await session.execute(query)
        return res.scalars().all()
