from sqlalchemy import Boolean, Integer, String, Text , func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.core.database import Base

class Type_MarkUp(Base):
    __tablename__ = "type_markup"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Batch(Base):
    __tablename__ = "batch"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    type_markup: Mapped[Type_MarkUp] = mapped_column()
    number_of_tasks: Mapped[int] = mapped_column(Integer, nullable=False)
    percentage_of_completion: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    overlaps: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
