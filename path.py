from os import environ
from pathlib import Pathjk

print(environ['PATH'])

environ['PATH'] += ':/test'
print(environ['PATH'])
