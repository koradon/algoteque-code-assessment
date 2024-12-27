from pydantic import BaseModel, Field
from typing import Dict
from .enums import Topics



class TeachersRequest(BaseModel):
    topics: Dict[Topics, int] = Field(
        description="Dictionary of topics and requested resources",
        example={
            "reading": 10,
            "math": 5,
            "science": 3,
            "history": 2,
            "art": 1    
        }
    )
    
