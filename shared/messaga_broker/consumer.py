import json
import logging
from aio_pika import IncomingMessage
from abc import ABC, abstractmethod


logger = logging.getLogger(__name__)

class BaseConsumer(ABC):
    async def handle_message(self, message: IncomingMessage):
        """Обработчик по умолчанию."""
        async with message.process():
            try:
                payload = json.loads(message.body)
                event = payload.get("event")
                data = payload.get("data", {})
                await self.process_event(event, data)
            except Exception as e:
                logger.exception(f"[RabbitMQ] Error processing message: {e}")
      
    @abstractmethod
    async def process_event(self, event: str, data: dict):
        raise NotImplementedError
