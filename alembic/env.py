import os
from logging.config import fileConfig
from dotenv import load_dotenv

from sqlalchemy import engine_from_config, pool
from alembic import context

# Load environment variables from .env file
load_dotenv()

# Alembic Config object
config = context.config

# Logging configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -------------------------------------------------------------------
# ✅ 1. Load DATABASE_URL from environment (critical)
# -------------------------------------------------------------------
database_url = os.getenv("DATABASE_URL")

# If provided, override sqlalchemy.url from alembic.ini
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# -------------------------------------------------------------------
# ✅ 2. Import your Base metadata for AUTOGENERATE
# -------------------------------------------------------------------
# Import all models so Alembic can detect them
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

# Import Base and all models
from app.models import Base

target_metadata = Base.metadata

# Offline migrations
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Online migrations
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

# Mode dispatch
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
