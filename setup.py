import os

# ------------- Helper ------------- #

def create_file(path, content=""):
    """Create file and write content."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def create_dir(path):
    """Create directory if not exists."""
    os.makedirs(path, exist_ok=True)


# ------------- Project Structure Generator ------------- #

def generate_backend_structure():
    print("🚀 Creating backend project structure...\n")

    # ---------------- ROOT ----------------
    create_dir("backend")

    # Root files
    create_file("backend/README.md", "# Backend Monorepo\n")
    create_file("backend/pyproject.toml", "[project]\nname = 'aviation-backend'\nversion = '0.1.0'\n")
    create_file("backend/.env.example", "DATABASE_URL=\nSECRET_KEY=\n")
    create_file("backend/docker-compose.yml", "")
    create_file("backend/uv.lock", "")
    create_file("backend/alembic.ini", "[alembic]\n")

    # ---------------- Alembic ----------------
    create_dir("backend/alembic/versions")
    create_file("backend/alembic/env.py", 
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import your models' metadata
# Example:
# from services.auth.models.user import Base
# target_metadata = Base.metadata

target_metadata = []

config = context.config
fileConfig(config.config_file_name)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
""")

    create_file("backend/alembic/script.py.mako", "")

    # ---------------- libs/common ----------------
    create_dir("backend/libs/common")
    create_file("backend/libs/common/__init__.py")
    create_file("backend/libs/common/config.py",
"""
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret")

settings = Settings()
""")

    create_file("backend/libs/common/database.py",
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from libs.common.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session
""")

    create_file("backend/libs/common/security.py",
"""
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)
""")

    create_file("backend/libs/common/exceptions.py",
"""
from fastapi import HTTPException, status

def NotFoundException(detail="Resource not found"):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
""")

    create_file("backend/libs/common/utils.py", "")

    # ---------------------- SERVICES ----------------------

    # AUTH SERVICE
    create_dir("backend/services/auth")
    create_file("backend/services/auth/__init__.py")
    create_file("backend/services/auth/main.py",
"""
from fastapi import FastAPI
from services.auth.routers.auth import router as auth_router

app = FastAPI(title="Auth Service")
app.include_router(auth_router)
""")

    create_dir("backend/services/auth/models")
    create_file("backend/services/auth/models/__init__.py")
    create_file("backend/services/auth/models/user.py",
"""
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="PASSAGER")
""")

    create_dir("backend/services/auth/schemas")
    create_file("backend/services/auth/schemas/user.py",
"""
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
""")

    create_dir("backend/services/auth/routers")
    create_file("backend/services/auth/routers/auth.py",
"""
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/")
def test():
    return {"message": "Auth service working"}
""")

    create_dir("backend/services/auth/core")
    create_file("backend/services/auth/core/jwt.py", "")
    create_file("backend/services/auth/core/hashing.py", "")
    create_file("backend/services/auth/core/roles.py", "")
    create_dir("backend/services/auth/dependencies")

    # BAGGAGE SERVICE
    create_dir("backend/services/baggage")
    create_file("backend/services/baggage/main.py",
"""
from fastapi import FastAPI

app = FastAPI(title="Baggage Service")
""")

    create_dir("backend/services/baggage/models")
    create_file("backend/services/baggage/models/bag.py", "")
    create_file("backend/services/baggage/models/scan_log.py", "")
    create_dir("backend/services/baggage/routers")
    create_dir("backend/services/baggage/schemas")
    create_dir("backend/services/baggage/dependencies")
    create_file("backend/services/baggage/__init__.py")

    # WEATHER SERVICE
    create_dir("backend/services/weather")
    create_file("backend/services/weather/main.py",
"""
from fastapi import FastAPI

app = FastAPI(title="Weather IA Service")
""")

    create_dir("backend/services/weather/models")
    create_file("backend/services/weather/models/prediction.py", "")
    create_dir("backend/services/weather/routers")
    create_dir("backend/services/weather/schemas")
    create_dir("backend/services/weather/dependencies")
    create_dir("backend/services/weather/workers")
    create_file("backend/services/weather/__init__.py")

    print("✅ Backend structure successfully created!")


# ------------- Run Script ------------- #

if __name__ == "__main__":
    generate_backend_structure()
    print("\n🎉 Project structure ready!\n")
