from application.interfaces.event import EventProtocol
from aio_pika import connect_robust, Message, ExchangeType
from aio_pika.abc import AbstractRobustConnection, AbstractChannel, AbstractQueue, AbstractExchange
from typing import Optional
from config import config_manager
import json


class PublisherEventBus:
    def __init__(self, url: str, exchange_name: str, queue_name: str) -> None:
        self.url = url
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.connection: Optional[AbstractRobustConnection] = None
        self.channel: Optional[AbstractChannel] = None
        self.exchange: Optional[AbstractExchange] = None
        self.queue: Optional[AbstractQueue] = None

    async def connect(self) -> None:
        """Establishes a connection to RabbitMQ."""
        print(f"Connecting to RabbitMQ at {self.url}...")
        self.connection = await connect_robust(self.url)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            self.exchange_name,
            ExchangeType.FANOUT,
            durable=True
        )
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
        await self.queue.bind(self.exchange)

    async def publish(self, event: EventProtocol) -> None:
        """Publishes an event to RabbitMQ."""
        if not self.exchange:
            raise RuntimeError("RabbitMQ connection is not initialized. Call connect() first.")
        
        body = json.dumps(event.to_dict()).encode()
        message = Message(body=body)

        await self.exchange.publish(
            message,
            routing_key="",
        )
        print(f"Published event to RabbitMQ: {event}")

    async def close(self) -> None:
        """Closes RabbitMQ connection."""
        if self.connection:
            await self.connection.close()
