from typing import TypeVar, Optional, Dict, Callable, Any, Generic
from aio_pika import connect_robust, Message, ExchangeType
from aio_pika.abc import AbstractRobustConnection, AbstractChannel, AbstractExchange, AbstractQueue
import json

EventType = TypeVar("EventType")


class EventBusSubscriber(Generic[EventType]):
    def __init__(self, url: str, exchange_name: str, queue_name: str):
        self.handlers: Dict[EventType, Callable[[Any], Any]] = {}
        self.url = url
        self.exchange_name = exchange_name
        self.queue_name = queue_name 
        self.connection: Optional[AbstractRobustConnection] = None
        self.channel: Optional[AbstractChannel] = None
        self.queue: Optional[AbstractQueue] = None
        self.exchange: Optional[AbstractExchange] = None
    
    def register_handler(self, event_type: EventType, handler: Callable[[Any], Any]) -> None:
        """Register a handler for a specific event type."""
        self.handlers[event_type] = handler

    async def connect(self) -> None:
        """Establish a connection to RabbitMQ and set up the exchange and queue."""
        self.connection = await connect_robust(self.url)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(self.exchange_name, ExchangeType.FANOUT, durable=True)
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
        await self.queue.bind(self.exchange)

    async def subscribe(self) -> None:
        """Subscribe to the RabbitMQ queue and process messages."""
        if not self.queue:
            raise RuntimeError("RabbitMQ connection is not initialized. Call connect() first.")
        
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    body = message.body.decode()
                    data = json.loads(body)
                    event_type = data.get("event_type")

                    handler = self.handlers.get(event_type)
                    if handler:
                        await handler(data)
                    else:
                        print(f"No handler for event type: {event_type}")

    async def close(self) -> None:
        """Close the connection to RabbitMQ."""
        if self.connection:
            await self.connection.close()
