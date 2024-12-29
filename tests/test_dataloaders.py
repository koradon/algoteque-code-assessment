import pytest
from fastapi import FastAPI
import json
from service.dataloaders import load_providers
from service.enums import Topics
from unittest.mock import mock_open, patch


@pytest.fixture
def app():
    return FastAPI()


@pytest.fixture
def providers_data():
    return {"provider_topics": {"provider_a": "math+science", "provider_b": "reading"}}


@patch("service.dataloaders.settings")
@patch("builtins.open")
def test_app_can_load_providers_from_file_on_startup(
    mock_open_func, mock_settings, app, tmp_path, providers_data
):
    mock_open_func.return_value = mock_open(
        read_data=json.dumps(providers_data)
    ).return_value
    mock_settings.providers_path = "fake_path"

    load_providers(app)

    assert len(app.state.providers) == 2
    assert "provider_a" in app.state.providers
    assert "provider_b" in app.state.providers


@patch("builtins.open")
def test_app_can_handle_providers_file_not_found_error(
    mock_open_func, app, providers_data
):
    mock_open_func.side_effect = FileNotFoundError

    load_providers(app)

    assert hasattr(app.state, "providers")
    assert app.state.providers == {}


@patch("service.dataloaders.settings")
@patch("builtins.open")
def test_app_can_handle_invalid_json_in_providers_file(
    mock_open_func, mock_settings, app
):
    mock_open_func.return_value = mock_open(read_data=json.dumps("")).return_value
    mock_settings.providers_path = "fake_path"

    load_providers(app)

    assert hasattr(app.state, "providers")
    assert app.state.providers == {}
