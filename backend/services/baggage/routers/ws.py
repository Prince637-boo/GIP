from fastapi import APIRouter, WebSocket
import asyncio
import aioredis
import json

router = APIRouter(prefix="/ws/baggages")

@router.websocket("/stream")
async def baggage_stream(ws: WebSocket):
    await ws.accept()

    redis = await aioredis.from_url("redis://redis:6379")
    pubsub = redis.pubsub()
    await pubsub.subscribe("baggage.scan", "baggage.status")

    try:
        while True:
            msg = await pubsub.get_message(ignore_subscribe_messages=True)
            if msg:
                await ws.send_text(msg["data"].decode())
            await asyncio.sleep(0.01)
    except:
        await ws.close()
