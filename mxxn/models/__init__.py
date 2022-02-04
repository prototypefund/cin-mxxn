from sqlalchemy.orm import as_declarative
from sqlalchemy import Column, Integer
from mxxn.database import metadata


@as_declarative(metadata=metadata)
class Base():
    """The declarative base class."""

    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
