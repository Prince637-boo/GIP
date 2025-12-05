import aio_pika
import asyncio
import json
import aioredis

from libs.common.config import settings

async def main():
    redis = await aioredis.from_url(settings.REDIS_URL)
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()

    exchange = await channel.declare_exchange("baggage.events", aio_pika.ExchangeType.TOPIC)
    queue = await channel.declare_queue("", exclusive=True)
    await queue.bind(exchange, routing_key="baggage.*")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                data = json.loads(message.body)
                event_type = message.routing_key.split(".")[-1]

                
                await redis.publish(f"baggage.{event_type}", json.dumps(data))

                print(f"[EVENT] Forwarded {event_type} to Redis pubsub")

if __name__ == "__main__":
    asyncio.run(main())
