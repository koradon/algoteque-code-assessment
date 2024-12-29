from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "request_body,quotes_len",
    [
        (
            {
                "topics": {
                    "reading": 20,
                    "math": 50,
                    "science": 30,
                    "history": 15,
                    "art": 10,
                }
            },
            3,
        ),
        (
            {
                "topics": {
                    "reading": 20,
                    "math": 50,
                    "science": 30,
                }
            },
            3,
        ),
        (
            {
                "topics": {
                    "reading": 20,
                    "math": 50,
                }
            },
            3,
        ),
        (
            {
                "topics": {
                    "reading": 20,
                }
            },
            1,
        ),
        (
            {"topics": {}},
            0,
        ),
    ],
)
def test_quotes_can_be_fetched(client, request_body, quotes_len, app_state, snapshot):
    response = client.post("/api/v1/quote", json=request_body)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "quotes" in data
    quotes = data["quotes"]
    assert len(quotes) == quotes_len
    assert quotes == snapshot


def test_quotes_cant_be_calculated_if_providers_are_not_ready(client):
    response = client.post(
        "/api/v1/quote",
        json={
            "topics": {
                "reading": 20,
                "math": 50,
                "science": 30,
                "history": 15,
                "art": 10,
            }
        },
    )

    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE


def test_quotes_cant_be_calculated_for_unsupported_topics(client, app_state):
    response = client.post(
        "/api/v1/quote",
        json={"topics": {"unsupported_topic": 10}},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "request_body",
    [
        {"some_field": "some_value"},
        {},
        [],
    ],
)
def test_quotes_cant_be_fetched_with_bad_request(client, request_body, app_state):
    response = client.post("/api/v1/quote", json=request_body)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
