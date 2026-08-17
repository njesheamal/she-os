from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.session import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """Get a database session for one request, and close it when done."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()