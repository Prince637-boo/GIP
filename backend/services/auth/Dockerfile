# base image
FROM python:3.11-slim

# system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

# create user for security
RUN useradd --create-home appuser
WORKDIR /home/appuser/app
USER appuser

# copy sources
COPY --chown=appuser:appuser pyproject.toml uv.lock ./
COPY --chown=appuser:appuser services/services_common/ ./services_common/
COPY --chown=appuser:appuser services/auth ./services/auth

# Install dependencies inside venv
ENV VIRTUAL_ENV=/home/appuser/.venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


RUN pip install --upgrade pip
RUN pip install fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg alembic pydantic passlib[bcrypt] python-jose[cryptography] aioredis

# copy entrypoint
COPY --chown=appuser:appuser docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
