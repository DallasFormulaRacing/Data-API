from pydantic import BaseModel
from enum import Enum
from typing import Union, List, Literal

class exceptionSchema(BaseModel):
    message: str 

class statusSchema(BaseModel):
    status: str = "ok"
    version: str = "v0.1.0"

class uploadSchema(BaseModel):
    message: str

class downloadSchema(BaseModel):
    data: str
    format: str
