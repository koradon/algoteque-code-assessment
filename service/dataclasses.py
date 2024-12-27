from dataclasses import dataclass
from typing import List, Tuple, Set
from decimal import Decimal
from .enums import Topics


@dataclass
class Provider:
    name: str
    topics: Set[Topics]


@dataclass
class Quote:
    provider: Provider
    amount: Decimal
    matched_topics: List[Tuple[Topics, int]]
