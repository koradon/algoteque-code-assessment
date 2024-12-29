from decimal import Decimal

import pytest


@pytest.mark.parametrize(
    "topics,expected",
    [
        (
            {"reading": 20, "math": 50, "science": 30, "history": 15, "art": 10},
            [("math", 50), ("science", 30), ("reading", 20)],
        ),
        (
            {"english": 90, "physics": 85, "chemistry": 70, "biology": 65},
            [("english", 90), ("physics", 85), ("chemistry", 70)],
        ),
        (
            {"history": 100, "geography": 100, "civics": 100, "economics": 90},
            [("history", 100), ("geography", 100), ("civics", 100)],
        ),
        ({"art": 30, "music": 20}, [("art", 30), ("music", 20)]),
        ({}, []),
    ],
)
def test_get_top_three_topics(quote_service, topics, expected):
    result = quote_service.get_top_three_topics(topics)
    assert result == expected


def test_calculate_quote_two_matches(quote_service):
    topics = [("math", 50), ("science", 30), ("reading", 20)]
    topic_ranks = {"math": 0, "science": 1, "reading": 2}

    # provider_a has math and science
    quote = quote_service.calculate_quote(
        quote_service.providers["provider_a"], topics, topic_ranks
    )

    assert quote
    assert quote.provider.name == "provider_a"
    assert quote.amount == Decimal("8.0")  # 10% of 80
    assert set(quote.matched_topics) == {("math", 50), ("science", 30)}


def test_calculate_quote_two_matches_lower_than_the_highest(quote_service):
    topics = [("math", 10), ("science", 20), ("reading", 80)]
    topic_ranks = {"math": 2, "science": 1, "reading": 0}

    # provider_a has math and science
    quote = quote_service.calculate_quote(
        quote_service.providers["provider_a"], topics, topic_ranks
    )

    assert quote
    assert quote.provider.name == "provider_a"
    assert quote.amount == Decimal("3.0")  # 10% of 30
    assert quote.matched_topics == [("math", 10), ("science", 20)]


def test_calculate_quote_single_match_highest(quote_service):
    topics = [("math", 50), ("science", 30), ("reading", 20)]
    topic_ranks = {"math": 0, "science": 1, "reading": 2}

    quote = quote_service.calculate_quote(
        quote_service.providers["provider_c"], topics, topic_ranks
    )

    assert quote
    assert quote.provider.name == "provider_c"
    assert quote.amount == Decimal("10")  # 20% of 50
    assert quote.matched_topics == [("math", 50)]


def test_calculate_quote_single_match_second_highest(quote_service):
    topics = [("math", 50), ("science", 20), ("reading", 30)]
    topic_ranks = {"math": 0, "science": 2, "reading": 1}

    # provider_b has reading
    quote = quote_service.calculate_quote(
        quote_service.providers["provider_b"], topics, topic_ranks
    )

    assert quote
    assert quote.provider.name == "provider_b"
    assert quote.amount == Decimal("7.5")  # 25% of 30
    assert quote.matched_topics == [("reading", 30)]


def test_calculate_quote_single_match_third_highest(quote_service):
    topics = [("math", 50), ("science", 30), ("reading", 20)]
    topic_ranks = {"math": 0, "science": 1, "reading": 2}

    # provider_b has reading
    quote = quote_service.calculate_quote(
        quote_service.providers["provider_b"], topics, topic_ranks
    )

    assert quote
    assert quote.provider.name == "provider_b"
    assert quote.amount == Decimal("6.0")  # 30% of 20
    assert quote.matched_topics == [("reading", 20)]


def test_calculate_quote_two_topics_withe_same_rank_single_match(quote_service):
    topics = [("math", 50), ("science", 20), ("reading", 20)]
    topic_ranks = {"math": 0, "science": 1, "reading": 1}

    quote = quote_service.calculate_quote(
        quote_service.providers["provider_b"], topics, topic_ranks
    )

    assert quote
    assert quote.provider.name == "provider_b"
    assert quote.amount == Decimal("5.0")  # 25% of 20
    assert quote.matched_topics == [("reading", 20)]


def test_calculate_quote_no_matches(quote_service):
    topics = [("math", 50), ("science", 20), ("art", 20)]
    topic_ranks = {"math": 0, "science": 1, "reading": 2}

    quote = quote_service.calculate_quote(
        quote_service.providers["provider_b"], topics, topic_ranks
    )

    assert not quote


def test_generate_quotes(quote_service):
    topics = {"reading": 20, "math": 50, "science": 30, "history": 15, "art": 10}

    quotes = quote_service.generate_quotes(topics)

    assert len(quotes) == 3
    quote_amounts = {q.provider.name: q.amount for q in quotes}
    assert quote_amounts == {
        "provider_a": Decimal("8.0"),  # Combined math + science
        "provider_b": Decimal("6.0"),  # Reading (third highest)
        "provider_c": Decimal("10.0"),  # Math (highest)
    }
