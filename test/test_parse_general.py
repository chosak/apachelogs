from datetime   import datetime, timezone
from apachelogs import COMBINED, LogParser

ENTRY = '209.126.136.4 - - [01/Nov/2017:07:28:29 +0000] "GET / HTTP/1.1" 301 521 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"'

def test_parse_general():
    parser = LogParser(COMBINED, encoding='utf-8')
    assert parser.format == COMBINED
    parsed = parser.parse(ENTRY)
    assert parsed.remote_host == "209.126.136.4"
    assert parsed.remote_logname is None
    assert parsed.remote_user is None
    assert parsed.request_time == datetime(2017, 11, 1, 7, 28, 29, tzinfo=timezone.utc)
    assert parsed.request_line == "GET / HTTP/1.1"
    assert parsed.final_status == 301
    assert parsed.bytes_sent == 521
    assert parsed.header_in == {
        "Referer": None,
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    }
    assert parsed.entry == ENTRY
    assert parsed.format == COMBINED
    assert parsed.time_fields == \
        {"apache_timestamp": "[01/Nov/2017:07:28:29 +0000]"}
