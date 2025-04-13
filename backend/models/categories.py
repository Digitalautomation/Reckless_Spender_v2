from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    is_custom: Optional[bool] = False

class CategoryCreate(CategoryBase):
    pass # For creating new categories later

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True # Pydantic V2 config 