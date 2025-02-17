from pydantic import BaseModel



class Type_MarkUp(BaseModel):
    id: int
    name: str
    created_at: str






class List_Type_MarkUp_Read(BaseModel):
    type_markup: list[Type_MarkUp]
    
    class Config:
        orm_mode = True
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        