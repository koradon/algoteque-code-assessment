from service.dataclasses import Quote, Provider
from service.enums import Topics
from typing import Dict, List, Tuple, Optional
from service.settings import settings
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


class QuoteService:
    percentage_ranks = {
        0: settings.single_highest_topic_weight,
        1: settings.second_highest_topic_weight,
        2: settings.third_highest_topic_weight,
    }

    def __init__(self, providers: Dict[str, Provider]):
        self.providers = providers

    def get_top_three_topics(
        self, topics: Dict[Topics, Decimal]
    ) -> List[Tuple[Topics, Decimal]]:
        return sorted(topics.items(), key=lambda x: x[1], reverse=True)[
            : settings.number_of_topics
        ]

    def calculate_quote(
        self,
        provider: Provider,
        topics: List[Tuple[Topics, Decimal]],
        topic_ranks: Dict[Topics, Decimal],
    ) -> Optional[Quote]:
        matched_topics = [
            (topic, amount) for (topic, amount) in topics if topic in provider.topics
        ]

        if not matched_topics:
            return None

        if len(matched_topics) >= 2:
            # two or more topics matched, use combined topic weight
            total = sum(topic[1] for topic in matched_topics)
            amount = total * settings.combined_topic_weight
        else:
            # one topic matched, use single topic weight base on the rank
            topic, level = matched_topics[0]
            rank = topic_ranks[topic]
            amount = level * self.percentage_ranks[rank]

        return Quote(
            provider=provider,
            matched_topics=matched_topics,
            amount=amount.quantize(Decimal("0.01")),
        )

    def generate_quotes(self, topics: Dict[Topics, Decimal]) -> List[Quote]:
        top_topics = self.get_top_three_topics(topics)
        topics_ranks = {topic: index for index, (topic, _) in enumerate(top_topics)}

        quotes = []
        for provider in self.providers.values():
            quote = self.calculate_quote(provider, top_topics, topics_ranks)
            if quote and quote.amount > 0:
                quotes.append(quote)

        return quotes
