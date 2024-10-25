from pydantic import BaseModel
from typing import Optional

class TaskTesting(BaseModel):
    name:str
    birthyear:int=None