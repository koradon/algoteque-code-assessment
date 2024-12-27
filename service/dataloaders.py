from .settings import settings
from .dataclasses import Provider
from .enums import Topics
import json
import logging
from fastapi import FastAPI

logger = logging.getLogger(__name__)


def load_providers(app: FastAPI):
    try:
        providers = {}
        with open(settings.providers_path, "r") as f:
            providers_data = json.load(f)
            providers_topics = providers_data["provider_topics"]

            for provider_name, topics in providers_topics.items():
                provider_topics = {Topics(topic) for topic in topics.split("+")}
                providers[provider_name] = Provider(
                    name=provider_name, topics=provider_topics
                )

        app.state.providers = providers
        logger.warning(f"Providers loaded: {providers}")

    except FileNotFoundError:
        logger.error(
            f"Warning: {settings.providers_path} not found. Creating empty providers state."
        )
        app.state.providers = {}
