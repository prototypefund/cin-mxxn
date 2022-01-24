"""Tests for the database module."""
from unittest.mock import patch, PropertyMock
from sqlalchemy.ext.asyncio.engine import AsyncEngine
import pytest
from mxxn.database import Database
from mxxn.settings import Settings
from mxxn.exceptions import database as database_ex


class TestDatabaseInit():
    """Tests for the __init__ method for the Database class."""

    def test_async_engine(self):
        """Is a async engine."""
        with patch.object(
                Settings, 'sqlalchemy_url', new_callable=PropertyMock) as mock:
            mock.return_value = 'sqlite+aiosqlite://'

            settings = Settings()
            db = Database(settings)

            assert isinstance(db.engine, AsyncEngine)

    def test_wrong_dialect(self):
        """Worng dialect in URL."""
        with patch.object(
                Settings, 'sqlalchemy_url', new_callable=PropertyMock) as mock:
            mock.return_value = 'xxyyzz://'

            settings = Settings()
            with pytest.raises(database_ex.URLError):
                Database(settings)

    def test_wrong_url_string(self):
        """Worng URL."""
        with patch.object(
                Settings, 'sqlalchemy_url', new_callable=PropertyMock) as mock:
            mock.return_value = 'sqlite+aiosqlite://%(here)s/database.sqlite'

            settings = Settings()
            with pytest.raises(database_ex.URLError):
                Database(settings)
