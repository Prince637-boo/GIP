# tests/baggages/test_baggage_routes.py
import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from services.baggages.main import app as baggage_app
from libs.common.database import get_db

from services.auth.models.user import User
from services.auth.models.company import Company
from services.auth.core.roles import UserRole
from services.auth.core.hashing import hash_password
from services.auth.core.jwt import create_access_token, hash_refresh_token
from services.baggages.models.baggage import Baggage
from services.baggages.models.baggage_event import BaggageEvent
from services.baggages.models.scan_log import ScanLog
from services.auth.models.refresh_token import RefreshToken
from services.baggages.core.enums import BaggageStatus

# -------------------------
# Helpers / Fixtures
# -------------------------

@pytest.fixture
async def override_db(db_session: AsyncSession):
    """
    Override get_db to use test session.
    """
    baggage_app.dependency_overrides[get_db] = lambda: db_session
    yield
    baggage_app.dependency_overrides.clear()


@pytest.fixture
async def client(override_db):
    async with AsyncClient(app=baggage_app, base_url="http://test") as c:
        yield c


@pytest.fixture
async def create_users(db_session: AsyncSession):
    """
    Create admin / company / atc / passenger users and company for tests.
    Returns dict with tokens.
    """
    # create company
    company = Company(name="TestAir")
    db_session.add(company)
    await db_session.flush()

    admin = User(
        email="admin@test.com",
        hashed_password=hash_password("adminpass"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    company_user = User(
        email="company@test.com",
        hashed_password=hash_password("companypass"),
        role=UserRole.COMPAGNIE,
        company=company,
        is_active=True,
    )
    atc = User(
        email="atc@test.com",
        hashed_password=hash_password("atcpass"),
        role=UserRole.ATC,
        is_active=True,
    )
    pax = User(
        email="pax@test.com",
        hashed_password=hash_password("paxpass"),
        role=UserRole.PASSAGER,
        is_active=True,
    )

    db_session.add_all([admin, company_user, atc, pax])
    await db_session.commit()

    # tokens
    tokens = {
        "admin": create_access_token(str(admin.id), admin.role.value),
        "company": create_access_token(str(company_user.id), company_user.role.value),
        "atc": create_access_token(str(atc.id), atc.role.value),
        "pax": create_access_token(str(pax.id), pax.role.value),
    }
    return {"users": {"admin": admin, "company": company_user, "atc": atc, "pax": pax}, "company": company, "tokens": tokens}


# -------------------------
# Tests
# -------------------------

@pytest.mark.asyncio
async def test_company_can_create_baggage(client, create_users, monkeypatch, db_session: AsyncSession):
    """
    Company creates a baggage; QR generator mocked to avoid FS writes.
    """
    tokens = create_users["tokens"]
    company = create_users["company"]

    # Mock QR generation to return a deterministic filepath
    monkeypatch.setattr(
        "services.baggages.core.utils.generate_qr_code",
        lambda tag, output_dir="storage/qr_codes": f"/tmp/qr_{tag}.png"
    )

    payload = {
        "owner_id": str(create_users["users"]["pax"].id),
        "company_id": str(company.id),
        "description": "Black suitcase",
        "weight": "23kg"
    }

    resp = await client.post("/baggages/", headers={"Authorization": f"Bearer {tokens['company']}"}, json=payload)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data["description"] == "Black suitcase"
    assert "tag" in data
    assert data["qr_code_path"].startswith("/tmp/qr_")

    # verify baggage in DB
    q = await db_session.execute(Baggage.__table__.select().where(Baggage.tag == data["tag"]))
    baggage = q.scalar_one_or_none()
    assert baggage is not None
    assert baggage.company_id == company.id


@pytest.mark.asyncio
async def test_passenger_cannot_create_baggage(client, create_users):
    tokens = create_users["tokens"]
    payload = {
        "owner_id": str(create_users["users"]["pax"].id),
        "company_id": str(create_users["company"].id),
        "description": "Illegal create",
    }
    resp = await client.post("/baggages/", headers={"Authorization": f"Bearer {tokens['pax']}"}, json=payload)
    assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_change_status_and_scan_logging(client, create_users, monkeypatch, db_session: AsyncSession):
    tokens = create_users["tokens"]
    company = create_users["company"]

    # Create baggage directly in DB (simulate create_baggage)
    monkeypatch.setattr(
        "services.baggages.core.utils.generate_qr_code",
        lambda tag, output_dir="storage/qr_codes": f"/tmp/qr_{tag}.png"
    )

    payload = {
        "owner_id": str(create_users["users"]["pax"].id),
        "company_id": str(company.id),
        "description": "Blue bag",
        "weight": "10kg"
    }

    create_resp = await client.post("/baggages/", headers={"Authorization": f"Bearer {tokens['company']}"}, json=payload)
    assert create_resp.status_code == 200
    bag = create_resp.json()
    tag = bag["tag"]

    # ATC scans bag
    scan_payload = {"location": "NIM:GateA", "device_info": "scanner-01"}
    scan_resp = await client.post(f"/baggages/{tag}/scan", headers={"Authorization": f"Bearer {tokens['atc']}"}, json=scan_payload)
    assert scan_resp.status_code == 200
    scan = scan_resp.json()
    assert scan["location"] == "NIM:GateA"

    # Company updates status to LOADED
    status_payload = {"status": "LOADED", "location": "Ramp1"}
    status_resp = await client.post(f"/baggages/{tag}/status", headers={"Authorization": f"Bearer {tokens['company']}"}, json=status_payload)
    assert status_resp.status_code == 200
    updated = status_resp.json()
    assert updated["status"] == "LOADED"

    # Check scan_logs in DB count >= 1
    q = await db_session.execute(ScanLog.__table__.select().where(ScanLog.baggage_id == bag["id"]))
    scans = q.scalars().all()
    assert len(scans) >= 1


@pytest.mark.asyncio
async def test_passenger_view_own_baggage(client, create_users, monkeypatch):
    tokens = create_users["tokens"]
    company = create_users["company"]

    # create a bag by company for this pax
    monkeypatch.setattr(
        "services.baggages.core.utils.generate_qr_code",
        lambda tag, output_dir="storage/qr_codes": f"/tmp/qr_{tag}.png"
    )

    payload = {
        "owner_id": str(create_users["users"]["pax"].id),
        "company_id": str(company.id),
        "description": "Red bag",
    }
    resp = await client.post("/baggages/", headers={"Authorization": f"Bearer {tokens['company']}"}, json=payload)
    assert resp.status_code == 200
    bag = resp.json()

    # passenger requests bag info
    resp2 = await client.get(f"/baggages/{bag['tag']}", headers={"Authorization": f"Bearer {tokens['pax']}"})
    assert resp2.status_code == 200
    data = resp2.json()
    assert data["tag"] == bag["tag"]


@pytest.mark.asyncio
async def test_other_passenger_cannot_view(client, create_users, monkeypatch, db_session: AsyncSession):
    tokens = create_users["tokens"]
    company = create_users["company"]

    # create a bag for pax (A)
    monkeypatch.setattr(
        "services.baggages.core.utils.generate_qr_code",
        lambda tag, output_dir="storage/qr_codes": f"/tmp/qr_{tag}.png"
    )

    payload = {
        "owner_id": str(create_users["users"]["pax"].id),
        "company_id": str(company.id),
        "description": "Private bag",
    }
    resp = await client.post("/baggages/", headers={"Authorization": f"Bearer {tokens['company']}"}, json=payload)
    bag = resp.json()

    # create another passenger B
    other = User(
        email="otherpax@test.com",
        hashed_password=hash_password("otherpass"),
        role=UserRole.PASSAGER,
        is_active=True
    )
    db_session.add(other)
    await db_session.commit()
    await db_session.refresh(other)
    token_other = create_access_token(str(other.id), other.role.value)

    # B tries to access A's bag -> forbidden
    resp2 = await client.get(f"/baggages/{bag['tag']}", headers={"Authorization": f"Bearer {token_other}"})
    assert resp2.status_code == status.HTTP_403_FORBIDDEN
