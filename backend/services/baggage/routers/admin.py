from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta

from libs.common.database import get_db
from services.auth.core.roles import allow, UserRole
from services.baggages.models.baggage import Baggage
from services.baggages.models.baggage_event import BaggageEvent
from services.baggages.models.scan_log import ScanLog
from services.baggages.schemas.baggage import BaggageOut
from services.baggages.core.enums import BaggageStatus

router = APIRouter(
    prefix="/admin/baggages",
    tags=["Admin - Baggage"]
)


# ---------------------------------------------------------
# PAGINATED LIST / FILTERS
# ---------------------------------------------------------
@router.get("/", dependencies=[Depends(allow(UserRole.ADMIN))])
async def list_baggages(
    db: AsyncSession = Depends(get_db),
    company_id: str | None = None,
    status: BaggageStatus | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    page: int = 1,
    size: int = 50
):
    query = select(Baggage)

    if company_id:
        query = query.where(Baggage.company_id == company_id)

    if status:
        query = query.where(Baggage.status == status)

    if from_date:
        query = query.where(Baggage.created_at >= from_date)
    if to_date:
        query = query.where(Baggage.created_at <= to_date)

    total = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total.scalar()

    query = query.offset((page - 1) * size).limit(size)

    result = await db.execute(query)
    bags = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "size": size,
        "items": [BaggageOut.model_validate(b) for b in bags]
    }


# ---------------------------------------------------------
# BAGGAGE DETAIL (with events + scan logs)
# ---------------------------------------------------------
@router.get("/{tag}", dependencies=[Depends(allow(UserRole.ADMIN))])
async def baggage_detail(tag: str, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Baggage).where(Baggage.tag == tag))
    baggage = q.scalar_one_or_none()

    if not baggage:
        raise HTTPException(404, "Baggage not found")

    # Fetch events
    events_q = await db.execute(
        select(BaggageEvent).where(BaggageEvent.baggage_id == baggage.id).order_by(BaggageEvent.timestamp)
    )
    events = events_q.scalars().all()

    # Fetch scans
    scans_q = await db.execute(
        select(ScanLog).where(ScanLog.baggage_id == baggage.id).order_by(ScanLog.timestamp)
    )
    scans = scans_q.scalars().all()

    return {
        "baggage": BaggageOut.model_validate(baggage),
        "events": [e.to_dict() for e in events],
        "scans": [s.to_dict() for s in scans],
    }


# ---------------------------------------------------------
# STATISTICS / METRICS
# ---------------------------------------------------------
@router.get("/metrics", dependencies=[Depends(allow(UserRole.ADMIN))])
async def baggage_metrics(db: AsyncSession = Depends(get_db)):
    now = datetime.utcnow()
    day_start = now - timedelta(days=1)

    # number of baggages created last 24h
    q1 = await db.execute(select(func.count()).select_from(
        select(Baggage).where(Baggage.created_at >= day_start).subquery()
    ))
    created_24h = q1.scalar()

    # number by status
    q2 = await db.execute(select(Baggage.status, func.count()).group_by(Baggage.status))
    by_status = {status.value: count for status, count in q2.all()}

    # scan events last 24h
    q3 = await db.execute(select(func.count()).select_from(
        select(ScanLog).where(ScanLog.timestamp >= day_start).subquery()
    ))
    scans_24h = q3.scalar()

    return {
        "created_last_24h": created_24h,
        "scans_last_24h": scans_24h,
        "by_status": by_status,
    }
