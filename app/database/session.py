from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = getenv(
    "DATABASE_URL",
    "postgresql+psycopg://she_os_user:she_os_password@localhost:5432/she_os_dev",
)
ANTHROPIC_API = getenv("ANTHROPIC_API") or None
ANTHROPIC_MODEL = getenv("ANTHROPIC_MODEL", "claude-sonnet-5")

# For SQLite, set check_same_thread=False to allow usage with FastAPI's threaded
# server. For other databases (Postgres, MySQL, etc.) no special connect args.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, # changes to the database are not automatically committed; must call db.commit() to save changes
    autoflush=False,  # changes to the database are not automatically flushed; must call db.flush() to send changes to the database
    bind=engine,      # the engine to use for database connections
)