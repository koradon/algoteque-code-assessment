import pytest
from service.dataclasses import Provider
from service.enums import Topics
from service.services.quote import QuoteService
from service.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def providers():
    return {
        "provider_a": Provider(name="provider_a", topics=[Topics.MATH, Topics.SCIENCE]),
        "provider_b": Provider(name="provider_b", topics=[Topics.READING]),
        "provider_c": Provider(name="provider_c", topics=[Topics.MATH]),
    }


@pytest.fixture
def app_state(providers):
    app.state.providers = providers
    yield
    if hasattr(app.state, "providers"):
        delattr(app.state, "providers")


@pytest.fixture
def quote_service(providers):
    return QuoteService(providers)
