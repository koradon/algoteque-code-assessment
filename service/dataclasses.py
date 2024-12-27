from dataclasses import dataclass
from typing import List
from .enums import Topics

@dataclass
class Provider:
    name: str
    topics: List[Topics]
