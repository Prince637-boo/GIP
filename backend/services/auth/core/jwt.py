from datetime import datetime, timedelta, timezone
from jose import jwt
from libs.common.config import settings
import uuid
import hashlib

ALGO = "HS256"

# Access token
def create_access_token(sub: str, role: str, expires_minutes: int = None):
    exp = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode({"sub": sub, "role": role, "exp": exp}, settings.SECRET_KEY, algorithm=ALGO)


# Secure refresh token generation (non-JWT)
def generate_refresh_token() -> str:
    raw = uuid.uuid4().hex + uuid.uuid4().hex
    return raw


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
