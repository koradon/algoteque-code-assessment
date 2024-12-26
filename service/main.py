from contextlib import asynccontextmanager
from fastapi import FastAPI
from .router import quote_router
from .settings import settings
import json
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        with open(settings.providers_path, "r") as f:
            app.state.providers = json.load(f)
    except FileNotFoundError:
        print(f"Warning: {settings.providers_path} not found. Creating empty providers state.")
        app.state.providers = {}
    
    yield
    # Shutdown
    
app = FastAPI(lifespan=lifespan)
app.include_router(quote_router)
