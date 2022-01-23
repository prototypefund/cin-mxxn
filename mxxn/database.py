"""The database module."""
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import MetaData

naming_convention: dict = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
"""The SQLAlchemy naming convention."""


class DeclarativeBase():
    """The declarative base class."""

    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, autoincrement=True)


metadata = MetaData(naming_convention=naming_convention)
Base = declarative_base(cls=DeclarativeBase, metadata=metadata)
"""The Base class for all database models."""
