from contextlib import asynccontextmanager
from fastapi import FastAPI
from .router import quote_router
from .settings import settings
import json
import uvicorn
import logging
from .dataclasses import Provider
from .enums import Topics
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        providers = {}
        with open(settings.providers_path, "r") as f:
            providers_data = json.load(f)
            providers_topics = providers_data["provider_topics"]
            for provider_name, topics in providers_topics.items():
                provider_topics = [Topics(topic) for topic in topics.split("+")]
                logger.info(f"Provider {provider_name} has topics: {provider_topics}")
                provider = Provider(name=provider_name, topics=provider_topics)
                providers[provider_name] = provider
        app.state.providers = providers
        logger.warning(f"Providers loaded: {providers}")
            
    except FileNotFoundError:
        logger.error(f"Warning: {settings.providers_path} not found. Creating empty providers state.")
        app.state.providers = {}
    
    yield
    # Shutdown
    
app = FastAPI(lifespan=lifespan)
app.include_router(quote_router, prefix="/api/v1")
