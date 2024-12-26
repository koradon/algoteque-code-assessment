from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    providers_path: str = "data/providers.json"

settings = Settings()
