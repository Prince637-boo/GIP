import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from services.auth.models.user import User
from services.auth.models.company import Company
from services.auth.models.refresh_token import RefreshToken
from services.auth.core.roles import UserRole
from services.auth.core.hashing import hash_password
from services.auth.core.jwt import hash_refresh_token
from services.auth.main import app

from libs.common.database import get_db


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
async def override_db(db_session):
    """
    Override get_db() dependency for this service.
    """
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def client(override_db):
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c


@pytest.fixture
async def admin_user(db_session: AsyncSession):
    admin = User(
        email="admin@test.com",
        hashed_password=hash_password("adminpass"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin


@pytest.fixture
async def admin_token(client, admin_user):
    #  login the admin
    resp = await client.post("/auth/login", json={
        "email": admin_user.email,
        "password": "adminpass"
    })
    return resp.json()["access_token"]


# ============================================================
# TEST AUTH ROUTES
# ============================================================

@pytest.mark.asyncio
async def test_register_passenger(client):
    resp = await client.post("/auth/register", json={
        "email": "pax@test.com",
        "password": "123456"
    })
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.json()
    assert data["email"] == "pax@test.com"
    assert data["role"] == UserRole.PASSAGER


@pytest.mark.asyncio
async def test_register_fails_setting_role(client):
    resp = await client.post("/auth/register", json={
        "email": "test2@test.com",
        "password": "123456",
        "role": "ADMIN"
    })
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_login_success(client, admin_user):
    resp = await client.post("/auth/login", json={
        "email": admin_user.email,
        "password": "adminpass",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client, admin_user):
    resp = await client.post("/auth/login", json={
        "email": admin_user.email,
        "password": "wrongpass",
    })
    assert resp.status_code == 401


# ============================================================
# TEST ADMIN ROUTES
# ============================================================

@pytest.mark.asyncio
async def test_admin_create_company(client, admin_token):
    resp = await client.post(
        "/auth/admin/create/company",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "company": {
                "name": "AirTest",
                "legal_id": "TEST-ID",
                "contact_email": "info@airtest.com"
            },
            "user_payload": {
                "email": "ceo@airtest.com",
                "password": "comp123"
            }
        }
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "AirTest"


@pytest.mark.asyncio
async def test_admin_create_atc(client, admin_token):
    resp = await client.post(
        "/auth/admin/create/atc",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"email": "atc@test.com", "password": "atcpass"}
    )
    assert resp.status_code == 200
    assert resp.json()["role"] == UserRole.ATC


@pytest.mark.asyncio
async def test_admin_list_users(client, admin_token):
    resp = await client.get(
        "/auth/admin/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_admin_disable_user(client, db_session, admin_token):
    user = User(
        email="target@test.com",
        hashed_password=hash_password("password"),
        role=UserRole.PASSAGER
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    resp = await client.patch(
        f"/auth/admin/users/{user.id}/disable",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    assert resp.json()["is_active"] is False


# ============================================================
# TEST COMPANY ROUTES
# ============================================================

@pytest.mark.asyncio
async def test_company_create_passenger(client, db_session):
    # create a company
    company = Company(name="TestFly")
    db_session.add(company)
    await db_session.flush()

    company_user = User(
        email="company@test.com",
        hashed_password=hash_password("companypass"),
        role=UserRole.COMPAGNIE,
        company=company,
        is_active=True,
    )
    db_session.add(company_user)
    await db_session.commit()
    await db_session.refresh(company_user)

    # login company
    resp_login = await client.post("/auth/login", json={
        "email": "company@test.com",
        "password": "companypass"
    })
    token = resp_login.json()["access_token"]

    # create passenger
    resp = await client.post(
        "/auth/company/create/passenger",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "pax-from-company@test.com", "password": "123456"}
    )
    assert resp.status_code == 200
    assert resp.json()["role"] == "PASSAGER"
    assert resp.json()["company_id"] == str(company.id)


# ============================================================
# TEST RBAC PERMISSIONS
# ============================================================

@pytest.mark.asyncio
async def test_passenger_cannot_create_atc(client):
    # register passenger
    resp = await client.post("/auth/register", json={
        "email": "pax2@test.com", "password": "12345"
    })

    # login passenger
    resp_login = await client.post("/auth/login", json={
        "email": "pax2@test.com",
        "password": "12345"
    })
    pax_token = resp_login.json()["access_token"]

    resp = await client.post(
        "/auth/admin/create/atc",
        headers={"Authorization": f"Bearer {pax_token}"},
        json={"email": "bad@test.com", "password": "123"}
    )

    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_atc_cannot_list_users(client, db_session):
    atc = User(
        email="atc2@test.com",
        hashed_password=hash_password("atcpass"),
        role=UserRole.ATC
    )
    db_session.add(atc)
    await db_session.commit()

    resp_login = await client.post("/auth/login", json={
        "email": "atc2@test.com", "password": "atcpass"
    })
    token = resp_login.json()["access_token"]

    resp = await client.get(
        "/auth/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 403


# ============================================================
# TEST REFRESH TOKEN
# ============================================================

@pytest.mark.asyncio
async def test_refresh_token_success(client, db_session, admin_user):
    # create refresh token manually
    raw_token = "raw1234"
    hashed = hash_refresh_token(raw_token)

    rt = RefreshToken(
        user_id=admin_user.id,
        token=hashed,
        user_agent="pytest",
        ip_address="127.0.0.1",
        expires_at=RefreshToken.expiry(days=1)
    )
    db_session.add(rt)
    await db_session.commit()

    # call endpoint
    resp = await client.post("/auth/refresh", json={"refresh_token": raw_token})

    assert resp.status_code == 200
    assert "access_token" in resp.json()
    assert "refresh_token" in resp.json()


@pytest.mark.asyncio
async def test_refresh_token_expired(client, db_session, admin_user):
    from datetime import datetime, timedelta

    raw = "expired123"
    hashed = hash_refresh_token(raw)

    old = RefreshToken(
        user_id=admin_user.id,
        token=hashed,
        user_agent="pytest",
        ip_address="127.0.0.1",
        expires_at=datetime.utcnow() - timedelta(days=1)
    )
    db_session.add(old)
    await db_session.commit()

    resp = await client.post("/auth/refresh", json={"refresh_token": raw})
    assert resp.status_code == 401


# ============================================================
# TEST /me ROUTE
# ============================================================

@pytest.mark.asyncio
async def test_me_endpoint(client, admin_token):
    resp = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    assert resp.json()["email"] == "admin@test.com"
