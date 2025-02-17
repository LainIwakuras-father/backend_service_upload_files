from pydantic import BaseModel

class Batch(BaseModel):
    id: int
    title: str
    type_markup: str
    number_of_tasks: int
    created_at: str

class List_Batch_Read(BaseModel):
    list_batch: list[Batch]

    class Config:
        orm_mode = True


class Current_Batch(BaseModel):
    id: int
    title:str
    type_markup: str
    number_of_tasks: int
    percentage_of_completion: int
    status: str
    overlaps: int 
    created_at: str