"""Tests for the cli module."""
from unittest.mock import Mock
import pytest
from mxxn.exceptions import env as env_ex
from mxxn.exceptions import filesys as filesys_ex
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

    def test_package_not_installed(self, mxxn_env, db):
        """The package to be initialized is not installed."""
        args_mock = Mock()
        args_mock.name = 'xyz'

        with pytest.raises(env_ex.PackageNotExistError):
            cli.db_init_handler(args_mock)

    def test_already_intialized(self, mxxn_env, db):
        """The package was already initialized."""
        args_mock = Mock()
        args_mock.name = 'mxnone'

        versions_path = mxxn_env/'mxnone/models/versions'
        versions_path.mkdir(parents=True)
        (versions_path/'revision.py').touch()

        with pytest.raises(filesys_ex.PathNotEmptyError):
            cli.db_init_handler(args_mock)


class TestDbRevisionHandler():
    """Tests for the db_revision_handler."""

    def test_worng_head_format(self, mxxn_env, db, capfd):
        """Wrong format for head argument."""
        init_args_mock = Mock()
        init_args_mock.name = 'mxnone'

        upgrade_args_mock = Mock()
        upgrade_args_mock.revision = 'heads'

        revision_args_mock = Mock()
        revision_args_mock.message = 'ADD: some chnages'
        revision_args_mock.autogenerate = None
        revision_args_mock.sql = None
        revision_args_mock.head = 'mxnonehead'

        cli.db_init_handler(init_args_mock)
        cli.db_upgrade_handler(upgrade_args_mock)

        with pytest.raises(ValueError):
            cli.db_revision_handler(revision_args_mock)

    def test_correct_head_format(self, mxxn_env, db, capfd):
        """Correct format for head argument."""
        init_args_mock = Mock()
        init_args_mock.name = 'mxnone'

        upgrade_args_mock = Mock()
        upgrade_args_mock.revision = 'heads'

        revision_args_mock = Mock()
        revision_args_mock.message = 'ADD: some changes'
        revision_args_mock.autogenerate = None
        revision_args_mock.sql = None
        revision_args_mock.head = 'mxnone@head'

        cli.db_init_handler(init_args_mock)
        cli.db_upgrade_handler(upgrade_args_mock)
        cli.db_revision_handler(revision_args_mock)
        captured = capfd.readouterr()

        assert '_add_some_changes.py' in captured.out
