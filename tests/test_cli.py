"""Tests for the cli module."""
from unittest.mock import Mock
from mxxn import cli


class TestDbInitHandler():
    """Tests for the db_init_handler function."""

    def test_branch_created(self, mxxn_env, db):
        """The branch was created."""
        args_mock = Mock()
        args_mock.name = 'mxnone'

        cli.db_init_handler(args_mock)
        versions_path = mxxn_env/'mxnone/models/versions'

        assert versions_path.is_dir()
        assert list(versions_path.glob('*add_mxnone_branch.py'))

    def test_package_not_installed(self, mxxn_env, db, capfd):
        """The package to be initialized is not installed."""
        args_mock = Mock()
        args_mock.name = 'xyz'

        try:
            cli.db_init_handler(args_mock)

        except SystemExit:
            captured = capfd.readouterr()

            assert 'The xyz package is not installed' in captured.out

    def test_already_intialized(self, mxxn_env, db, capfd):
        """The package was already initialized."""
        args_mock = Mock()
        args_mock.name = 'mxnone'

        versions_path = mxxn_env/'mxnone/models/versions'
        versions_path.mkdir(parents=True)
        (versions_path/'revision.py').touch()

        try:
            cli.db_init_handler(args_mock)

        except SystemExit:
            captured = capfd.readouterr()

            assert 'mxnone package is not empty.' in captured.out
