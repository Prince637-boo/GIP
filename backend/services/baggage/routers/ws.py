from ..redis.redis_c import redis_client
from fastapi import APIRouter, WebSocket
import asyncio

router = APIRouter(prefix="/ws/baggages")

@router.websocket("/stream")
async def baggage_stream(ws: WebSocket):
    """
    WebSocket pour recevoir en temps réel les événements liés aux bagages.

    Événements écoutés depuis Redis :
    - "baggage.scan" : lorsqu'un bagage est scanné
    - "baggage.status" : lorsqu'un bagage change de statut
    - "baggage.gps": lorque la position du baggage est envoyé

    Frontend peut se connecter sur : ws://<host>/ws/baggages/stream
    """
    await ws.accept()
    print("WebSocket connection accepted")



    pubsub = redis_client.pubsub()
    await pubsub.subscribe("baggage.scan", "baggage.status", "baggage.gps")
    print("Subscribed to Redis channels: baggage.scan, baggage.status")

    try:
        while True:
            # Récupération des messages Redis
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message and "data" in message:
                await ws.send_text(message["data"])
            await asyncio.sleep(0.01)  # petite pause pour ne pas bloquer la boucle
    except Exception as e:
        print(f"WebSocket closed: {e}")
        await ws.close()
    finally:
        # Nettoyage : désabonnement et fermeture du client Redis
        await pubsub.unsubscribe("baggage.scan", "baggage.status", "baggage.gps")
        await redis_client.close()
        print("Redis connection closed and unsubscribed")
