"""CLI application for the MXXN framework."""
from argparse import ArgumentParser

parser = ArgumentParser(description='The cli for MXXN management.')
subparsers = parser.add_subparsers()
db_parser = subparsers.add_parser('db', help='Database management.')
db_subparsers = db_parser.add_subparsers()
db_init_parser = db_subparsers.add_parser('init', help='Initialize branch.')
db_init_parser.add_argument('name', help='The name of the package.')

def main():
    args = parser.parse_args()
