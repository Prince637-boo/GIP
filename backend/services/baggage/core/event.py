import aio_pika
import json
from libs.common.config import settings  

EXCHANGE_NAME = "baggage.events"


async def publish_event(event_type: str, payload: dict):
    """
    Publish event to RabbitMQ topic exchange.
    """
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            EXCHANGE_NAME, type=aio_pika.ExchangeType.TOPIC, durable=True
        )

        message = aio_pika.Message(
            body=json.dumps(payload).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        routing_key = f"baggage.{event_type}"

        await exchange.publish(message, routing_key=routing_key)
