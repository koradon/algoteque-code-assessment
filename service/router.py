from fastapi import APIRouter
from .schema import TeachersRequest, QuoteResponse
from .services.quote import QuoteService
from fastapi import Depends
from .dependencies import get_quote_service

quote_router = APIRouter()


@quote_router.post("/quote", response_model=QuoteResponse)
def generate_quote(
    request: TeachersRequest, quote_service: QuoteService = Depends(get_quote_service)
):
    quotes = quote_service.generate_quotes(request.topics)
    return QuoteResponse(quotes={q.provider.name: q.amount for q in quotes})
