from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from system.app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    future=True,
    echo=False,  # se quiser ver SQL no log, troca pra True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()