from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import json

from libs.common.database import get_db

from ..redis.redis_c import redis_client
from ..models.bag import Baggage
from ..schemas.bag import BaggageGPSUpdate
from ..schemas.baggage_event import BaggageScanGPS

router = APIRouter(prefix="/baggages", tags=["GPS Tracking"])


@router.post("/update-location", summary="Met à jour la position GPS d’un bagage")
async def update_location(
    data: BaggageGPSUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Met à jour la localisation GPS d’un bagage.

    Cette route est utilisée par un tracker GPS intégré, une passerelle IoT ou un
    service interne qui envoie périodiquement les coordonnées du bagage.

    ### Corps JSON attendu
    - **tag** : Identifiant du bagage
    - **latitude** : Position GPS latitude
    - **longitude** : Position GPS longitude

    ### Processus
    1. Vérifie si le bagage existe.
    2. Met à jour les coordonnées et l’horodatage.
    3. Sauvegarde en base.
    4. Diffuse l’événement GPS via Redis pour mise à jour du dashboard en temps réel.
    """

    # Recherche du bagage
    result = await db.execute(select(Baggage).where(Baggage.tag == data.tag))
    baggage = result.scalar_one_or_none()

    if not baggage:
        raise HTTPException(status_code=404, detail="Baggage not found")

    # Mise à jour GPS
    baggage.last_latitude = data.latitude
    baggage.last_longitude = data.longitude
    baggage.last_seen_at = datetime.utcnow()

    db.add(baggage)
    await db.commit()

    # Publication temps réel via Redis
    payload = {
        "tag": baggage.tag,
        "latitude": data.latitude,
        "longitude": data.longitude,
        "timestamp": baggage.last_seen_at.isoformat()
    }
    await redis_client.publish("baggage.gps", json.dumps(payload))

    return {"status": "ok", "tag": baggage.tag}



@router.post("/scan-gps", summary="Scanne un bagage et envoie la position GPS associée")
async def scan_and_send_gps(
    data: BaggageScanGPS,
    db: AsyncSession = Depends(get_db)
):
    """
    Scanne un bagage via un dispositif RFID ou un scanner portable
    et enregistre immédiatement la localisation GPS.

    ### Corps JSON attendu
    - **tag** : Identifiant du bagage scanné
    - **latitude** : Latitude GPS
    - **longitude** : Longitude GPS

    ### Processus
    1. Vérifie le bagage.
    2. Met à jour la position GPS.
    3. Enregistre en base.
    4. Diffuse l’événement sur Redis pour les WebSockets.

    Utilisé principalement par :
    - Agents au sol
    - Portes d’embarquement
    - Systèmes RFID + GPS couplés
    """

    # Recherche du bagage
    result = await db.execute(select(Baggage).where(Baggage.tag == data.tag))
    baggage = result.scalar_one_or_none()

    if not baggage:
        raise HTTPException(status_code=404, detail="Baggage not found")

    # Mise à jour GPS
    baggage.last_latitude = data.latitude
    baggage.last_longitude = data.longitude
    baggage.last_seen_at = datetime.utcnow()
    db.add(baggage)
    await db.commit()

    # Publication temps réel Redis
    payload = {
        "tag": baggage.tag,
        "latitude": data.latitude,
        "longitude": data.longitude,
        "timestamp": baggage.last_seen_at.isoformat()
    }
    await redis_client.publish("baggage.gps", json.dumps(payload))

    return {"status": "ok", "tag": baggage.tag}
