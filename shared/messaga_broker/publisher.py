import json
import logging
from messaga_broker.rabbitmq import RabbitMQClient
from events.base import BaseEvent


logger = logging.getLogger(__name__)


class EventPublisher:
    def __init__(self, rabbitmq_client: RabbitMQClient, exchange_name: str):
        self.rabbitmq = rabbitmq_client
        self.exchange_name = exchange_name

    async def publish(self, event: BaseEvent, routing_key: str):
        payload = {
            "event": event.event_name,
            "data": event.to_dict()
        }
        await self.rabbitmq.publish(routing_key, payload, exchange_name=self.exchange_name)
