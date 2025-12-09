import asyncio
import pytest
import redis.asyncio as redis
from fastapi import FastAPI
from services.baggage.routers.ws import router
import websockets
import uvicorn

app = FastAPI()
app.include_router(router)

from unittest.mock import AsyncMock, patch

# Sans le serveur Redis

@patch("services.baggage.routers.ws.redis.Redis")
@pytest.mark.asyncio
async def test_ws_with_mock(mock_redis):
    # Simule pubsub et publish
    pubsub_mock = AsyncMock()
    pubsub_mock.get_message.side_effect = [
        {"data": "Scan 1"}, {"data": "Status OK"}, None
    ]
    mock_redis.return_value.pubsub.return_value = pubsub_mock

# Avec Redis qui tourne: ça va marcher seulement si redis est accessible

# @pytest.mark.asyncio
# async def test_ws_baggage_stream_multiple_messages():
#     # Démarrage serveur FastAPI
#     config = uvicorn.Config(app, host="127.0.0.1", port=8001, log_level="critical")
#     server = uvicorn.Server(config)
#     server_task = asyncio.create_task(server.serve())
#     await asyncio.sleep(0.5)  # Laisser le serveur démarrer

#     # Connexion WebSocket
#     ws_url = "ws://127.0.0.1:8001/ws/baggages/stream"
#     async with websockets.connect(ws_url) as ws:
#         r = redis.Redis(host="localhost", port=6379, decode_responses=True)

#         messages = [("baggage.scan", "Scan 1"), ("baggage.scan", "Scan 2"),
#                     ("baggage.status", "Status OK"), ("baggage.status", "Status Delayed")]

#         for channel, msg in messages:
#             await r.publish(channel, msg)
#             received = await asyncio.wait_for(ws.recv(), timeout=1.0)
#             assert received == msg

#         await r.close()

#     # Arrêt du serveur
#     server.should_exit = True
#     await server_task

