"""CLI application for the MXXN framework."""
from argparse import ArgumentParser, Namespace
from pathlib import Path
from alembic import command
from alembic.config import Config
import sys
import re
from copier import run_auto
from mxxn.env import mxns, Mxn, is_develop
from mxxn.settings import Settings
from mxxn.exceptions import env as env_ex
from mxxn.exceptions import filesys as filesys_ex


def generate_alembic_cfg() -> Config:
    """
    Generate a Alembic config object.

    This function adds the script location *mxxn:alembic* to the config.
    It also adds the *models/versions* folders of all installed mxns as
    version locations. The SQLAlchemy URL is taken from the application
    settings.
    """
    versions_path = Path('models/versions')
    version_locations = 'mxxn:' + str(versions_path)

    for mxn in mxns():
        path = str(Mxn(mxn).path)/versions_path

        if path.is_dir():
            version_locations = version_locations + ' ' + mxn + ':'\
                    + str(versions_path)

    settings = Settings()
    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', 'mxxn:alembic')
    alembic_cfg.set_main_option('version_locations', str(version_locations))
    alembic_cfg.set_main_option('sqlalchemy.url', settings.sqlalchemy_url)

    return alembic_cfg


def db_init_handler(args: Namespace) -> None:
    """
    Handle the db init command.

    Args:
        args: The argparse Namespace.

    Raises:
        mxxn.exceptions.filesys.PathNotEmptyError: If the version path is
            not empty.
        mxxn.exceptions.env.PackageNotExistError: If the package not in
            the environment.
    """
    alembic_cfg = generate_alembic_cfg()
    version_locations = str(alembic_cfg.get_main_option('version_locations'))
    versions_path = Path('models/versions')

    try:
        path = Mxn(args.name).path/versions_path

        if path.is_dir():
            if any(path.iterdir()):
                raise filesys_ex.PathNotEmptyError(
                    'The versions path of the {} package is '
                    'not empty.\n'.format(args.name))

        path.mkdir(parents=True, exist_ok=True)
        version_locations = version_locations + ' ' + args.name + ':' \
            + str(versions_path)

        alembic_cfg.set_main_option('version_locations', version_locations)

        message = 'ADD: {} branch'.format(args.name)
        command.revision(
            alembic_cfg, message=message, head='base',
            branch_label=args.name, version_path=str(path))

    except env_ex.PackageNotExistError as e:
        raise env_ex.PackageNotExistError(
            'The {} package is not installed in the environment.\n'
            .format(args.name)) from e


def db_upgrade_handler(args: Namespace) -> None:
    """
    Handle the db upgrade command.

    Args:
        args: The argparse Namespace.

    Raises:
        alembic.util.exc.CommandError: If alembic command error occurs.
    """
    alembic_cfg = generate_alembic_cfg()

    command.upgrade(
        alembic_cfg, args.revision, sql=args.sql)


def db_downgrade_handler(args: Namespace) -> None:
    """
    Handle the db downgrade command.

    Args:
        args: The argparse Namespace.

    Raises:
        alembic.util.exc.CommandError: If alembic command error occurs.
    """
    alembic_cfg = generate_alembic_cfg()

    command.downgrade(
        alembic_cfg, args.revision, sql=args.sql)


def db_branches_handler(args: Namespace) -> None:
    """
    Handle the db branches command.

    Args:
        args: The argparse Namespace.

    Raises:
        alembic.util.exc.CommandError: If alembic command error occurs.
    """
    alembic_cfg = generate_alembic_cfg()

    command.branches(alembic_cfg, verbose=args.verbose)


def db_current_handler(args: Namespace) -> None:
    """
    Handle the db current command.

    Args:
        args: The argparse Namespace.

    Raises:
        alembic.util.exc.CommandError: If alembic command error occurs.
    """
    alembic_cfg = generate_alembic_cfg()

    command.current(alembic_cfg, verbose=args.verbose)


def db_heads_handler(args: Namespace) -> None:
    """
    Handle the db heads command.

    Args:
        args: The argparse Namespace.

    Raises:
        alembic.util.exc.CommandError: If alembic command error occurs.
    """
    alembic_cfg = generate_alembic_cfg()

    command.heads(
        alembic_cfg, verbose=args.verbose,
        resolve_dependencies=args.resolve_dependencies)


def db_history_handler(args: Namespace) -> None:
    """
    Handle the db history command.

    Args:
        args: The argparse Namespace.

    Raises:
        alembic.util.exc.CommandError: If alembic command error occurs.
    """
    alembic_cfg = generate_alembic_cfg()

    command.history(
        alembic_cfg, verbose=args.verbose,
        rev_range=args.rev_range, indicate_current=args.indicate_current)


def db_merge_handler(args: Namespace) -> None:
    """
    Handle the db merge command.

    Args:
        args: The argparse Namespace.

    Raises:
        alembic.util.exc.CommandError: If alembic command error occurs.
    """
    alembic_cfg = generate_alembic_cfg()

    command.merge(
        alembic_cfg, revisions=args.revisions, message=args.message)


def db_show_handler(args: Namespace) -> None:
    """
    Handle the db show command.

    Args:
        args: The argparse Namespace.

    Raises:
        alembic.util.exc.CommandError: If alembic command error occurs.
    """
    alembic_cfg = generate_alembic_cfg()

    command.show(
        alembic_cfg, rev=args.rev)


def db_revision_handler(args: Namespace) -> None:
    """
    Handle the db revision command.

    Args:
        args: The argparse Namespace.

    Raises:
        alembic.util.exc.CommandError: If alembic command error occurs.

    """
    if not re.search(r'^\w+@\w+$', args.head):
        raise ValueError('head is not in format <branchname>@head.')

    branch_name = args.head.split('@')[0]
    alembic_cfg = generate_alembic_cfg()
    alembic_cfg.set_main_option('branch_name', branch_name)

    command.revision(
        alembic_cfg, message=args.message, sql=args.sql,
        autogenerate=args.autogenerate, head=args.head)


def mxn_init_handler(args: Namespace) -> None:
    """
    Handle the mxn init command.

    Args:
        args: The argparse Namespace.

    """

    if args.path:
        run_auto('gl:ccodein/mxxn/templates/mxn.git', args.path)
    else:
        run_auto('gl:ccodein/mxxn/templates/mxn.git')


parser = ArgumentParser(description='The cli for MXXN management.')
subparsers = parser.add_subparsers()
db_parser = subparsers.add_parser('db', help='Database management.')
db_subparsers = db_parser.add_subparsers()

db_upgrade_parser = db_subparsers.add_parser(
        'upgrade', help='Upgrade to a later version.')
db_upgrade_parser.add_argument('revision', help='The revision identifier.')
db_upgrade_parser.add_argument(
        '--sql',
        action='store_true',
        help='Don\'t emit SQL to database - dump to standard output/file '
        'instead. See docs on offline mode.')
db_upgrade_parser.set_defaults(func=db_upgrade_handler)

if is_develop():
    db_init_parser = db_subparsers.add_parser(
            'init', help='Initialize the mxn or mxnapp branch.')
    db_init_parser.add_argument(
            'name', help='The name of the mxn or mxnapp package.')
    db_init_parser.set_defaults(func=db_init_handler)

    db_upgrade_parser = db_subparsers.add_parser(
            'upgrade', help='Upgrade to a later version.')
    db_upgrade_parser.add_argument('revision', help='The revision identifier.')
    db_upgrade_parser.add_argument(
            '--sql',
            action='store_true',
            help='Don\'t emit SQL to database - dump to standard output/file '
            'instead. See docs on offline mode.')
    db_upgrade_parser.set_defaults(func=db_upgrade_handler)

    db_downgrade_parser = db_subparsers.add_parser(
            'downgrade', help='Revert to a previous version.')
    db_downgrade_parser.add_argument(
            'revision',
            help='The revision identifier.')
    db_downgrade_parser.add_argument(
            '--sql',
            action='store_true',
            help='Don\'t emit SQL to database - dump to standard output/file '
            'instead. See docs on offline mode.')
    db_downgrade_parser.set_defaults(func=db_downgrade_handler)

    db_branches_parser = db_subparsers.add_parser(
            'branches', help='Show current branch points.')
    db_branches_parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Use more verbose output')
    db_branches_parser.set_defaults(func=db_branches_handler)

    db_current_parser = db_subparsers.add_parser(
            'current', help='Display the current revision for a database.')
    db_current_parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Use more verbose output')
    db_current_parser.set_defaults(func=db_current_handler)

    db_heads_parser = db_subparsers.add_parser(
            'heads',
            help='Show current available heads in the script directory.')
    db_heads_parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Use more verbose output')
    db_heads_parser.add_argument(
            '--resolve-dependencies',
            action='store_true',
            help='Treat dependency versions as down revisions')
    db_heads_parser.set_defaults(func=db_heads_handler)

    db_history_parser = db_subparsers.add_parser(
            'history', help='List changeset scripts in chronological order.')
    db_history_parser.add_argument(
            '-r', '--rev-range',
            action='store',
            help='Specify a revision range; format is [start]:[end]')
    db_history_parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Use more verbose output')
    db_history_parser.add_argument(
            '-i', '--indicate-current',
            action='store_true',
            help='Indicate the current revision')
    db_history_parser.set_defaults(func=db_history_handler)

    db_merge_parser = db_subparsers.add_parser(
            'merge',
            help='Merge two revisions together. Creates a new migration file.')
    db_merge_parser.add_argument(
            'revisions',
            action='store',
            help='One or more revisions, or "heads" for all heads')
    db_merge_parser.add_argument(
            '-m', '--message',
            action='store',
            help='Message string to use with "revision"')
    db_merge_parser.set_defaults(func=db_merge_handler)

    db_show_parser = db_subparsers.add_parser(
            'show', help='Show the revision(s) denoted by the given symbol.')
    db_show_parser.add_argument(
            'rev',
            action='store',
            help='The revision target')
    db_show_parser.set_defaults(func=db_show_handler)

    db_revision_parser = db_subparsers.add_parser(
            'revision', help='Create a new revision file.')
    db_revision_parser.add_argument(
            'message',
            action='store',
            help='Message string to use with "revision"')
    db_revision_parser.add_argument(
            'head',
            action='store',
            help='Specify head revision or <branchname>@head '
            'to base new revision on.')
    db_revision_parser.add_argument(
            '--autogenerate',
            action='store_true',
            help='Populate revision script with candidate migration '
            'operations, based on comparison of database to model.')
    db_revision_parser.add_argument(
            '--sql',
            action='store_true',
            help='Don\'t emit SQL to database - dump to standard output/file '
            'instead. See docs on offline mode.')
    db_revision_parser.add_argument(
            '--depends-on',
            action='store',
            help='Specify one or more revision identifiers which this '
            'revision should depend on')
    db_revision_parser.set_defaults(func=db_revision_handler)

    mxn_parser = subparsers.add_parser('mxn', help='Mxn management.')
    mxn_subparsers = mxn_parser.add_subparsers()
    mxn_init_parser = mxn_subparsers.add_parser(
            'init', help='Initialize a mxn.')
    mxn_init_parser.add_argument(
            '--path',
            action='store',
            help='The path in which the Mxn should be initialized. '
            'If the path is not specified, the current working directory '
            'is used.')
    mxn_init_parser.set_defaults(func=mxn_init_handler)


def main() -> None:
    """
    CLI script entry point.

    Raises:
        SystemExit: The program exit exception.
    """
    try:
        args = parser.parse_args()
        args.func(args)

    except Exception as e:
        print('ERROR: ' + str(e))

        sys.exit(1)
