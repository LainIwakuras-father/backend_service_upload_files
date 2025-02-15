from pydantic import BaseModel


class searchSchema(BaseModel):
    id: int
    batch_name: str
    overlaps: int
    priority: int


class matchSchema(BaseModel):
    id: int
    batch_name: str
    overlaps: int
    priority: int
