from pydantic import BaseModel, Field
from typing import Dict
from decimal import Decimal
from .enums import Topics


class TeachersRequest(BaseModel):
    topics: Dict[Topics, Decimal] = Field(
        description="Dictionary of topics and requested resources",
        example={"reading": 10, "math": 5, "science": 3, "history": 2, "art": 1},
    )


class QuoteResponse(BaseModel):
    quotes: Dict[str, Decimal] = Field(
        description="Dictionary of providers and their quotes",
        example={"provider1": 15.50, "provider2": 12.75, "provider3": 10.25},
    )
