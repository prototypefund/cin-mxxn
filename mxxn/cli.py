"""CLI application for the MXXN framework."""
from argparse import ArgumentParser, Namespace
from pathlib import Path
from alembic import command
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


def db_init_handler(args: Namespace) -> None:
    try:
        versions_path = Path('migrations/versions')
        version_locations = 'mxxn:' + str(versions_path)

        for mxn in mxns():
            path = str(Mxn(mxn).path)/versions_path

            if path.is_dir():
                version_locations = version_locations + ' ' + mxn + ':'\
                        + str(versions_path)

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

        settings = Settings()
        alembic_cfg = Config()
        alembic_cfg.set_main_option('script_location', 'mxxn:migrations')
        alembic_cfg.set_main_option('version_locations', version_locations)
        alembic_cfg.set_main_option('sqlalchemy.url', settings.sqlalchemy_url)

        message = 'ADD: {} branch'.format(args.name)
        command.revision(
                alembic_cfg, message=message, head='base',
                branch_label=args.name, version_path=str(path))
    except env_ex.PackageNotExistError:
        log.error(
            'The {} package is not installed in '
            'the environment.\n'.format(args.name))

        sys.exit(1)


parser = ArgumentParser(description='The cli for MXXN management.')
subparsers = parser.add_subparsers()
db_parser = subparsers.add_parser('db', help='Database management.')
db_subparsers = db_parser.add_subparsers()
db_init_parser = db_subparsers.add_parser('init', help='Initialize branch.')
db_init_parser.add_argument('name', help='The name of the package.')
db_init_parser.set_defaults(func=db_init_handler)


def main() -> None:
    args = parser.parse_args()
    args.func(args)
