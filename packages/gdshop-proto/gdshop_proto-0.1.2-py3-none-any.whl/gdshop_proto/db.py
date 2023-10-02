import datetime
import uuid
from typing import Annotated, Generator

from sqlalchemy import ForeignKey, create_engine, func
from sqlalchemy.orm import mapped_column, registry, sessionmaker, Mapped
import sqlalchemy.dialects.postgresql as postgresql

from gdshop_proto.settings import DBSettings

mapper_registry = registry()


timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]


@mapper_registry.mapped
class BaseDBTable:
    __abstract__ = True

    created_at: Mapped[timestamp] = mapped_column(server_default=func.CURRENT_TIMESTAMP())
    edited_at: Mapped[timestamp] = mapped_column(server_default=func.CURRENT_TIMESTAMP(), onupdate=datetime.datetime.now)


@mapper_registry.mapped
class BaseCreatorTable:
    __abstract__ = True

    created_by: Mapped[str] = mapped_column(ForeignKey("profile_users.phone"), index=True)
    last_edited_by: Mapped[str] = mapped_column(ForeignKey("profile_users.phone"), index=True)


@mapper_registry.mapped
class BaseTable(BaseDBTable):
    __abstract__ = True

    id = mapped_column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True
    )


engine = create_engine(DBSettings().DB_DSB, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
