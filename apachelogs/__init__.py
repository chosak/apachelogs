"""
Parse Apache access logs

Visit <https://github.com/jwodder/apachelogs> for more information.
"""

__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'apachelogs@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/apachelogs'

from .errors import Error, InvalidDirectiveError, InvalidEntryError, \
                    UnknownDirectiveError
from .format import AGENT, COMBINED, COMMON, COMMON_VHOST, REFERER
from .parser import LogEntry, LogParser
from .util   import parse_apache_timestamp

__all__ = [
    'AGENT',
    'COMBINED',
    'COMMON',
    'COMMON_VHOST',
    'Error',
    'InvalidDirectiveError',
    'InvalidEntryError',
    'LogEntry',
    'LogParser',
    'REFERER',
    'UnknownDirectiveError',
    'parse',
    'parse_apache_timestamp',
    'parse_lines',
]

def parse(fmt, entry, encoding=None, errors=None):
    return LogParser(fmt, encoding=encoding, errors=errors).parse(entry)

def parse_lines(fmt, entries, encoding=None, errors=None, ignore_invalid=False):
    return LogParser(fmt, encoding=encoding, errors=errors)\
        .parse_lines(entries, ignore_invalid)
