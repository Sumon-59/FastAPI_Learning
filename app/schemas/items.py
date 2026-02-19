""" 
it contains items schemas
purpose:request/response validatiion
"""
from typing import Optional
from pydantic import BaseModel,Field, ConfigDict

#----------------------------------------------------
# Data models
#----------------------------------------------------


#ItemCreate: POST body Schema
class ItemCreate(BaseModel):
    name: str = Field(min_length=2,description="The name should be minimum length 2")
    price: float = Field(ge=0)
    stock: int = Field(ge=0)


#ItemRead: API Response Scheme
class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    price: float
    stock: int

#ItemUpdate: PATCH/PUT body Schema
class ItemUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, description="The name should be minimum length 2")
    price: Optional[float] = Field(default=None, ge=0)
    stock: Optional[int] = Field(default=None, ge=0)


