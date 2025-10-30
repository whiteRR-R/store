import aio_pika
import json
import logging


logger = logging.getLogger(__name__)


class RabbitMQClient:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None

    async def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(self.amqp_url)
            self.channel = await self.connection.channel()
            logger.info(f"[RabbitMQ] Connected: {self.amqp_url}")
            
    def _create_message(self, body: str) -> aio_pika.Message:
        return aio_pika.Message(
            body=body.encode("utf-8"),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        
    async def publish(self, routing_key: str, event: dict, exchange_name: str):
        """Отправка события в обменник (exchange)."""
        await self.connect()

        exchange = await self.channel.declare_exchange(
            exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
        )

        message = self._create_message(json.dumps(event))
        await exchange.publish(message, routing_key=routing_key)
        logger.info(f"[RabbitMQ] Published -> {exchange_name}:{routing_key}")


    async def consume(self, queue_name: str, exchange_name: str, routing_key: str, handler):
        """Подписка на очередь с обработчиком."""
        await self.connect()

        exchange = await self.channel.declare_exchange(
            exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
        )

        queue = await self.channel.declare_queue(queue_name, durable=True)
        await queue.bind(exchange, routing_key)

        logger.info(f"[RabbitMQ] Consuming from '{queue_name}' (routing_key='{routing_key}')")

        await queue.consume(handler)
