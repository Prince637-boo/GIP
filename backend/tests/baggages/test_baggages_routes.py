import os
import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from services.baggage.main import app as baggage_app
from libs.common.database import get_db
from services.auth.models.user import User
from services.auth.core.roles import UserRole
from services.auth.core.hashing import hash_password
from services.auth.core.jwt import create_access_token
from services.baggage.models.bag import Baggage
from services.baggage.models.scan_log import ScanLog


# -------------------------
# Fixture AsyncClient
# -------------------------
@pytest.fixture
async def baggage_client(db_session: AsyncSession):
    baggage_app.dependency_overrides[get_db] = lambda: db_session
    transport = ASGITransport(app=baggage_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    baggage_app.dependency_overrides.clear()


# -------------------------
# Helper pour créer un bagage
# -------------------------
async def create_baggage_for_test(client: AsyncClient, token: str, owner_id: str, company_id: str):
    payload = {
        "owner_id": str(owner_id),
        "company_id": str(company_id),
        "description": "Test bag",
        "weight": "10kg"
    }
    resp = await client.post(
        "/baggages/",
        headers={"Authorization": f"Bearer {token}"},
        json=payload
    )
    assert resp.status_code == 200
    return resp.json()


# -------------------------
# TESTS COMPAGNIE / PASSAGER / ADMIN
# -------------------------

@pytest.mark.asyncio
async def test_company_can_create_baggage(baggage_client: AsyncClient, create_users):
    tokens = create_users["tokens"]
    company = create_users["company"]
    pax = create_users["users"]["pax"]

    bag = await create_baggage_for_test(baggage_client, tokens["company"], pax.id, company.id)
    assert bag["description"] == "Test bag"
    assert "tag" in bag


@pytest.mark.asyncio
async def test_passenger_cannot_create_baggage(baggage_client: AsyncClient, create_users):
    tokens = create_users["tokens"]
    company = create_users["company"]
    pax = create_users["users"]["pax"]

    payload = {
        "owner_id": str(pax.id),
        "company_id": str(company.id),
        "description": "Illegal create"
    }
    resp = await baggage_client.post(
        "/baggages/",
        headers={"Authorization": f"Bearer {tokens['pax']}"},
        json=payload
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_passenger_view_and_access_control(baggage_client: AsyncClient, create_users, db_session: AsyncSession):
    tokens = create_users["tokens"]
    company = create_users["company"]
    pax = create_users["users"]["pax"]

    # Create bag
    bag = await create_baggage_for_test(baggage_client, tokens["company"], pax.id, company.id)
    tag = bag["tag"]

    # Passenger sees own bag
    resp = await baggage_client.get(
        f"/baggages/{tag}",
        headers={"Authorization": f"Bearer {tokens['pax']}"}
    )
    assert resp.status_code == 200

    # Other passenger cannot see
    other = User(email="other@test.com", hashed_password=hash_password("pass"),
                 role=UserRole.PASSAGER, is_active=True)
    db_session.add(other)
    await db_session.commit()
    await db_session.refresh(other)

    token_other = create_access_token(str(other.id), other.role.value)
    resp2 = await baggage_client.get(
        f"/baggages/{tag}",
        headers={"Authorization": f"Bearer {token_other}"}
    )
    assert resp2.status_code == 403


@pytest.mark.asyncio
async def test_scan_and_status_updates(baggage_client: AsyncClient, create_users, db_session: AsyncSession):
    tokens = create_users["tokens"]
    company = create_users["company"]
    pax = create_users["users"]["pax"]

    # Create bag
    bag = await create_baggage_for_test(baggage_client, tokens["company"], pax.id, company.id)
    tag = bag["tag"]

    # ATC scans
    scan_payload = {"location": "NIM:GateA", "device_info": "scanner-01"}
    scan_resp = await baggage_client.post(
        f"/baggages/{tag}/scan",
        headers={"Authorization": f"Bearer {tokens['atc']}"},
        json=scan_payload
    )
    assert scan_resp.status_code == 200

    # Company updates status
    status_payload = {"status": "LOADED", "location": "Ramp1"}
    status_resp = await baggage_client.post(
        f"/baggages/{tag}/status",
        headers={"Authorization": f"Bearer {tokens['company']}"},
        json=status_payload
    )
    assert status_resp.status_code == 200
    assert status_resp.json()["status"] == "LOADED"

    # Check scan logs
    q = await db_session.execute(ScanLog.__table__.select().where(ScanLog.baggage_id == uuid.UUID(bag["id"])))
    scans = q.scalars().all()
    assert len(scans) >= 1


@pytest.mark.asyncio
async def test_my_baggages_list(baggage_client: AsyncClient, create_users):
    tokens = create_users["tokens"]
    pax = create_users["users"]["pax"]
    company = create_users["company"]

    # Create multiple bags
    for _ in range(3):
        await create_baggage_for_test(baggage_client, tokens["company"], pax.id, company.id)

    resp = await baggage_client.get(
        "/baggages/my/list",
        headers={"Authorization": f"Bearer {tokens['pax']}"}
    )
    data = resp.json()
    assert resp.status_code == 200
    assert len(data) >= 3


@pytest.mark.asyncio
async def test_admin_list_detail_metrics(baggage_client: AsyncClient, create_users):
    
    os.environ["OTEL_EXPORTER_OTLP_ENABLED"] = "false"
    
    tokens = create_users["tokens"]
    company = create_users["company"]
    pax = create_users["users"]["pax"]
    admin_token = tokens["admin"]

    # Create bag
    bag = await create_baggage_for_test(baggage_client, tokens["company"], pax.id, company.id)
    tag = bag["tag"]

    # List baggages
    resp = await baggage_client.get(
        "/admin/baggages/?page=1&size=10",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data and "items" in data

    # Get bag details
    resp = await baggage_client.get(
        f"/admin/baggages/{tag}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "baggage" in data and "events" in data and "scans" in data

    # Metrics (dépends de otl)
    # resp = await baggage_client.get(
    #     "/admin/baggages/metrics",
    #     headers={"Authorization": f"Bearer {admin_token}"}
    # )
    # assert resp.status_code == 200
    # metrics = resp.json()
    # print(metrics)
    # assert "created_last_24h" in metrics and "scans_last_24h" in metrics and "by_status" in metrics
