"""Pytest conftest.py file."""
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture()
def iter_entry_points_mixins():
    """Get mocks for the iter_entry_points function."""
    with patch('mxxn.env.iter_entry_points') as mock:
        mxnone = MagicMock
        mxntwo = MagicMock()
        mxnthree = MagicMock()
        mxnone.name = 'mxnone'
        mxntwo.name = 'mxntwo'
        mxnthree.name = 'mxnthree'

        mock.return_value = [mxnone, mxntwo, mxnthree]

        yield iter_entry_points_mixins
