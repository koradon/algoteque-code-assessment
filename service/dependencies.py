from fastapi import Request
from service.services.quote import QuoteService


def get_quote_service(request: Request) -> QuoteService:
    return QuoteService(request.app.state.providers)
