import logging

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.batch_model import Batch
from app.repositories.base import BaseDAO


class BatchRepository(BaseDAO):
    model = Batch

    async def filter_find_all(self, **filter_by):
        logging.debug(f"Поиск  по типу разметки : {filter_by}")
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        return res.scalars().all()
