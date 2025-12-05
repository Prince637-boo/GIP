import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context

from libs.common.config import settings
from libs.common.database import engine as async_engine

# import all models so Alembic can see metadata
# IMPORTANT: import modules that define Base subclasses (services/*/models)
from services.auth.models import user as auth_user
from services.baggage.models import bag as bag_model
from services.weather.models import prediction as pred_model

from libs.common.base import Base

target_metadata = Base.metadata

# this is the Alembic Config object
config = context.config
fileConfig(config.config_file_name)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url") or str(settings.DATABASE_URL)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = async_engine.sync_engine
    with connectable.connect() as connection:
        do_run_migrations(connection)

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
