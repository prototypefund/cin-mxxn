"""The database module."""
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import MetaData
from sqlalchemy.sql.functions import now
from sqlalchemy import exc as sqlalchemy_ex
from sqlalchemy.ext.asyncio import (
        AsyncSession, async_scoped_session, create_async_engine)
from sqlalchemy.orm import sessionmaker
from asyncio import current_task
from typing import Any
from mxxn.exceptions import database as database_ex
from mxxn.settings import Settings
from mxxn.logging import logger


naming_convention: dict = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
"""The SQLAlchemy naming convention."""

metadata = MetaData(naming_convention=naming_convention)
"""A collection of Table objects and their associated schema constructs."""


@compiles(now, 'sqlite')
def sqlite_now(element: Any, compiler: Any, **kwargs: int) -> str:
    """Overwrite the func.now() function for SQLite."""
    return "strftime('%Y-%m-%d %H:%M:%f000', 'now')"


class Database():
    """The Database class."""

    def __init__(self, settings: Settings) -> None:
        """
        Initiliaze the Database instance.

        Args:
            settings: The settings object of the application.

        """
        try:
            self.engine = create_async_engine(settings.sqlalchemy_url)
            session_factory = sessionmaker(
                self.engine, expire_on_commit=False, class_=AsyncSession)

            self.session = async_scoped_session(
                    session_factory, scopefunc=current_task)

            log = logger('Database')
            log.debug('Engine and session initialized.')

        except (sqlalchemy_ex.NoSuchModuleError, sqlalchemy_ex.ArgumentError):
            raise database_ex.URLError(
                    'The SQLAlchemy database URL format is not correct.')
