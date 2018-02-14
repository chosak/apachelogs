from   datetime   import datetime, timezone
import pytest
from   apachelogs import COMBINED, LogFormat

ENTRY = '66.240.205.34 - - [18/Nov/2017:12:30:55 +0000] "Gh0st\\xad" 400 0 "-" "-"'

NON_STR_FIELDS = {
    "remote_host": "66.240.205.34",
    "remote_logname": None,
    "remote_user": None,
    "request_time": datetime(2017, 11, 18, 12, 30, 55, tzinfo=timezone.utc),
    "final_status": 400,
    "bytes_sent": 0,
    "header_in": {
        "Referer": None,
        "User-agent": None,
    },
}

def test_parse_bad_utf8():
    with pytest.raises(UnicodeDecodeError):
        LogFormat(COMBINED, encoding='utf-8').parse(ENTRY)

def test_bytes_parse():
    assert dict(LogFormat(COMBINED).parse(ENTRY)) == \
        dict(NON_STR_FIELDS, request_line=b"Gh0st\xAD")

def test_parse_latin1():
    assert dict(LogFormat(COMBINED, encoding='iso-8859-1').parse(ENTRY)) == \
        dict(NON_STR_FIELDS, request_line="Gh0st\xAD")

def test_parse_utf8_surrogateescape():
    assert dict(LogFormat(COMBINED, encoding='utf-8', errors='surrogateescape').parse(ENTRY)) == \
        dict(NON_STR_FIELDS, request_line="Gh0st\xAD")

### TODO: Test bytes vs. chars when referer and/or user agent is non-None
