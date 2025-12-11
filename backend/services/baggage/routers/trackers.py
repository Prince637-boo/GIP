from datetime import datetime
import json

from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from libs.common.database import get_db
from ..redis.redis_c import redis_client
from ..baggage_service import get_baggage_by_device
from ..models.bag import Baggage

router = APIRouter(prefix="/trackers", tags=["GPS Trackers"])


@router.post(
    "/ingest",
    summary="Réception des données envoyées par un tracker GPS",
    description="""
Réception des données d’un **tracker GPS physique** attaché au bagage.

Cette route est appelée automatiquement par :
- un module GPS LoRaWAN
- un tracker GSM/4G
- un module Bluetooth mesh
- un device IoT propriétaire

Le tracker envoie un JSON contenant :
- **device_id** : ID du tracker physique
- **lat** : latitude GPS
- **lon** : longitude GPS

L’API :
1. Trouve le bagage associé au tracker (`device_id`)
2. Met à jour la position GPS du bagage
3. Sauvegarde en base
4. Diffuse l’événement via Redis sur le canal `baggage.gps`
"""
)
async def ingest_tracker(
    req: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Ingestion des données d’un tracker GPS en temps réel.
    """

    # Lecture du JSON brut
    payload = await req.json()

    device_id = payload.get("device_id")
    latitude = payload.get("lat")
    longitude = payload.get("lon")

    if not device_id:
        raise HTTPException(400, detail="Missing 'device_id'")
    if latitude is None or longitude is None:
        raise HTTPException(400, detail="Missing 'lat' or 'lon' fields")

    # 1. Récupération du bagage lié au tracker
    baggage: Baggage | None = await get_baggage_by_device(db, device_id)

    if not baggage:
        raise HTTPException(404, detail="No baggage associated with this device_id")

    # 2. Mise à jour GPS du bagage
    baggage.last_latitude = latitude
    baggage.last_longitude = longitude
    baggage.last_seen_at = datetime.utcnow()

    db.add(baggage)
    await db.commit()

    # 3. Publication Redis pour les WebSockets en temps réel
    event_payload = {
        "tag": baggage.tag,
        "device_id": device_id,
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": baggage.last_seen_at.isoformat()
    }

    await redis_client.publish("baggage.gps", json.dumps(event_payload))

    # 4. Réponse
    return {"status": "ok", "baggage_tag": baggage.tag, "device_id": device_id}
