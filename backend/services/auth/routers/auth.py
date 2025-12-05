from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from libs.common.database import get_db

from services.auth.models.refresh_token import RefreshToken
from services.auth.core.jwt import create_access_token, generate_refresh_token, hash_refresh_token
from datetime import datetime

from services.auth.schemas.user import UserCreate, UserLogin, UserOut
from services.auth.models.user import User
from services.auth.core.hashing import hash_password, verify_password
from services.auth.core.jwt import create_access_token
from services.auth.core.roles import UserRole
from services.auth.dependencies.user import get_current_user
from sqlalchemy import select
from libs.common.database import get_db

from services.auth.schemas.user import UserCreate, UserOut, UserUpdate
from services.auth.schemas.company import CompanyCreate, CompanyOut
from services.auth.service.user_service import create_user, get_user_by_email, get_user_by_id, create_company_and_user, disable_user
from services.auth.core.roles import UserRole
from services.auth.dependencies.permissions import allow

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut)
async def register_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    # Vérifier email existant
    q = await db.execute(
        User.__table__.select().where(User.email == payload.email)
    )
    existing = q.fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")

    new_user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post("/login")
async def login(payload: UserLogin, request: Request, db: AsyncSession = Depends(get_db)):

    q = await db.execute(
        User.__table__.select().where(User.email == payload.email)
    )
    user: User = q.scalar()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Access token
    access_token = create_access_token(str(user.id), user.role.value)

    # Refresh token 
    raw_refresh = generate_refresh_token()
    hashed_refresh = hash_refresh_token(raw_refresh)

    db.add(RefreshToken(
        user_id=user.id,
        token=hashed_refresh,
        user_agent=request.headers.get("user-agent", "unknown"),
        ip_address=request.client.host,
        expires_at=RefreshToken.expiry(days=7),
    ))

    await db.commit()

    return {
        "access_token": access_token,
        "refresh_token": raw_refresh,
        "token_type": "bearer"
    }

@router.post("/refresh")
async def refresh(refresh_token: str, request: Request, db: AsyncSession = Depends(get_db)):
    hashed = hash_refresh_token(refresh_token)

    q = await db.execute(
        RefreshToken.__table__.select().where(RefreshToken.token == hashed)
    )
    token_record = q.scalar()

    if not token_record or token_record.is_revoked:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    # Rotation : révoquer l'ancien
    token_record.is_revoked = True

    # Nouveau refresh
    new_raw = generate_refresh_token()
    new_hash = hash_refresh_token(new_raw)

    db.add(RefreshToken(
        user_id=token_record.user_id,
        token=new_hash,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host,
        expires_at=RefreshToken.expiry(days=7),
    ))

    await db.commit()

    access = create_access_token(str(token_record.user_id), "PASSAGER")  # role fetched below

    return {
        "access_token": access,
        "refresh_token": new_raw
    }


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/admin/create/company", response_model=CompanyOut)
async def admin_create_company(company: CompanyCreate, user_payload: UserCreate,
                               db: AsyncSession = Depends(get_db),
                               admin = Depends(allow(UserRole.ADMIN))):
    company_obj, user_obj = await create_company_and_user(db, company, user_payload)
    return company_obj

@router.post("/admin/create/atc", response_model=UserOut)
async def admin_create_atc(payload: UserCreate, db: AsyncSession = Depends(get_db), admin = Depends(allow(UserRole.ADMIN))):
    payload.role = UserRole.ATC
    if await get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, payload)
    return user

@router.post("/company/create/passenger", response_model=UserOut)
async def company_create_passenger(payload: UserCreate, db: AsyncSession = Depends(get_db),
                                   company_user = Depends(allow(UserRole.COMPAGNIE))):

    company = company_user.company
    if not company:
        raise HTTPException(status_code=400, detail="Company metadata not found for this account.")
    payload.role = UserRole.PASSAGER
    if await get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, payload, company=company)
    return user

@router.get("/admin/users", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_db), admin = Depends(allow(UserRole.ADMIN))):
    q = await db.execute(select(User))
    return q.scalars().all()

@router.patch("/admin/users/{user_id}/disable", response_model=UserOut)
async def admin_disable_user(user_id: str, db: AsyncSession = Depends(get_db), admin = Depends(allow(UserRole.ADMIN))):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = await disable_user(db, user)
    return user