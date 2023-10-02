import uuid
from typing import Generator

from sqlalchemy import UUID, create_engine
from sqlalchemy.orm import mapped_column, registry, sessionmaker

from gdshop_db.settings import DBSettings

mapper_registry = registry()


@mapper_registry.mapped
class BaseTable:
    __abstract__ = True

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


engine = create_engine(DBSettings().DB_DSB, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
