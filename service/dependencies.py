from fastapi import Request, HTTPException
from service.services.quote import QuoteService
from http import HTTPStatus


def get_quote_service(request: Request) -> QuoteService:
    if not hasattr(request.app.state, "providers"):
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Providers are not ready",
        )

    return QuoteService(request.app.state.providers)
