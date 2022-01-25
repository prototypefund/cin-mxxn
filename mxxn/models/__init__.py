from sqlalchemy.schema import MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer
from mxxn.database import naming_convention


class DeclarativeBase():
    """The declarative base class."""

    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, autoincrement=True)


metadata = MetaData(naming_convention=naming_convention)
Base = declarative_base(cls=DeclarativeBase, metadata=metadata)
"""The Base class for all database models."""
