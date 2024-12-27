from pydantic_settings import BaseSettings
from decimal import Decimal


class Settings(BaseSettings):
    providers_path: str = "data/providers.json"

    number_of_topics: int = 3
    combined_topic_weight: Decimal = Decimal(0.10)
    single_highest_topic_weight: Decimal = Decimal(0.20)
    second_highest_topic_weight: Decimal = Decimal(0.25)
    third_highest_topic_weight: Decimal = Decimal(0.30)


settings = Settings()
