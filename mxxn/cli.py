"""CLI application for the MXXN framework."""
from argparse import ArgumentParser, Namespace
from pathlib import Path
from alembic import command
from alembic.util import exc as alembic_ex
from alembic.config import Config
import logging
import sys
from mxxn.env import mxns, Mxn
from mxxn.settings import Settings
from mxxn.exceptions import env as env_ex
from mxxn.logging import logger


logging.basicConfig(
        level=logging.WARNING,
        format='%(levelname)s: %(message)s')

log = logger()


def generate_alembic_cfg() -> Config:
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
    alembic_cfg.set_main_option('version_locations', version_locations)
    alembic_cfg.set_main_option('sqlalchemy.url', settings.sqlalchemy_url)

    return alembic_cfg


def db_init_handler(args: Namespace) -> None:
    alembic_cfg = generate_alembic_cfg()
    version_locations = alembic_cfg.get_main_option('version_locations')
    versions_path = Path('models/versions')

    try:
        path = Mxn(args.name).path/versions_path

        if path.is_dir():
            if any(path.iterdir()):
                log.error(
                    'The versions path of the {} package is '
                    'not empty.\n'.format(args.name))
                sys.exit(1)

        path.mkdir(parents=True, exist_ok=True)
        version_locations = version_locations + ' ' + args.name + ':' \
            + str(versions_path)

        alembic_cfg.set_main_option('version_locations', version_locations)

        message = 'ADD: {} branch'.format(args.name)
        command.revision(
            alembic_cfg, message=message, head='base',
            branch_label=args.name, version_path=str(path))

    except env_ex.PackageNotExistError:
        log.error(
            'The {} package is not installed in '
            'the environment.\n'.format(args.name))

        sys.exit(1)


def db_upgrade_handler(args: Namespace) -> None:
    alembic_cfg = generate_alembic_cfg()

    try:
        command.upgrade(alembic_cfg, args.revision)

    except alembic_ex.CommandError as e:
        log.error(e)


def db_downgrade_handler(args: Namespace) -> None:
    alembic_cfg = generate_alembic_cfg()

    try:
        command.downgrade(alembic_cfg, args.revision)

    except alembic_ex.CommandError as e:
        log.error(e)


def db_branches_handler(args: Namespace) -> None:
    alembic_cfg = generate_alembic_cfg()

    try:
        command.branches(alembic_cfg)

    except alembic_ex.CommandError as e:
        log.error(e)


parser = ArgumentParser(description='The cli for MXXN management.')
subparsers = parser.add_subparsers()
db_parser = subparsers.add_parser('db', help='Database management.')
db_subparsers = db_parser.add_subparsers()

db_init_parser = db_subparsers.add_parser('init', help='Initialize branch.')
db_init_parser.add_argument('name', help='The name of the package.')
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
db_downgrade_parser.add_argument('revision', help='The revision identifier.')
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


def main() -> None:
    args = parser.parse_args()
    args.func(args)
