from contextlib import asynccontextmanager
from fastapi import FastAPI
from .router import quote_router
from .settings import settings
import json
import uvicorn
import logging
from .dataclasses import Provider
from .enums import Topics
from .dataloaders import load_providers

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    load_providers(app)

    yield
    # Shutdown


app = FastAPI(lifespan=lifespan)
app.include_router(quote_router, prefix="/api/v1")
