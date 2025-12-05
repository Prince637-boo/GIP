from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from libs.common.database import get_db
from services.auth.dependencies.auth import get_current_user
from services.auth.dependencies.permissions import allow
from services.auth.core.roles import UserRole

from services.baggages.schemas.baggage import BaggageCreate, BaggageOut
from services.baggages.schemas.baggage_event import BaggageEventCreate, BaggageEventOut
from services.baggages.service.baggage_service import (
    create_baggage,
    update_baggage_status,
    get_baggage,
    list_baggages_for_user
)

from services.baggages.schemas.scan_log import ScanLogCreate, ScanLogOut
from services.baggages.service.baggage_service import log_scan

router = APIRouter(prefix="/baggages", tags=["Baggages"])


# --------------------------------------------
# CREATE BAGGAGE (COMPANY only)
# --------------------------------------------

@router.post("/", response_model=BaggageOut)
async def add_baggage(
    payload: BaggageCreate,
    db: AsyncSession = Depends(get_db),
    company = Depends(allow(UserRole.COMPAGNIE, UserRole.ADMIN))
):
    baggage = await create_baggage(db, payload)
    return baggage


# --------------------------------------------
# UPDATE STATUS (COMPANY or ADMIN)
# --------------------------------------------

@router.post("/{tag}/status", response_model=BaggageOut)
async def change_status(
    tag: str,
    event: BaggageEventCreate,
    db: AsyncSession = Depends(get_db),
    user = Depends(allow(UserRole.COMPAGNIE, UserRole.ADMIN, UserRole.ATC)),
):
    baggage = await get_baggage(db, tag)
    if not baggage:
        raise HTTPException(404, "Baggage not found")
    
    updated = await update_baggage_status(db, baggage, event.status, event.location)
    return updated


# --------------------------------------------
# GET BAGGAGE BY TAG (any role with proper rights)
# --------------------------------------------

@router.get("/{tag}", response_model=BaggageOut)
async def get_baggage_info(
    tag: str,
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),
):
    baggage = await get_baggage(db, tag)
    if not baggage:
        raise HTTPException(404, "Baggage not found")
    
    # PASSAGER: can only view their own baggages
    if user.role == UserRole.PASSAGER and baggage.owner_id != user.id:
        raise HTTPException(403, "Not allowed")

    return baggage


# --------------------------------------------
# LIST BAGGAGES FOR PASSAGER
# --------------------------------------------

@router.get("/my/list", response_model=list[BaggageOut])
async def my_baggages(
    db: AsyncSession = Depends(get_db),
    user = Depends(allow(UserRole.PASSAGER))
):
    return await list_baggages_for_user(db, user.id)


@router.post("/{tag}/scan", response_model=ScanLogOut)
async def scan_baggage(
    tag: str,
    payload: ScanLogCreate,
    db: AsyncSession = Depends(get_db),
    user = Depends(allow(UserRole.COMPAGNIE, UserRole.ATC, UserRole.ADMIN))
):
    baggage = await get_baggage(db, tag)
    if not baggage:
        raise HTTPException(404, "Baggage not found")
    
    scan = await log_scan(
        db=db,
        baggage_id=baggage.id,
        user_id=user.id,
        location=payload.location,
        device_info=payload.device_info
    )
    return scan
