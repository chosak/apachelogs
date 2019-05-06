from   datetime   import datetime, timezone
import pytest
from   apachelogs import VHOST_COMBINED, LogParser

@pytest.mark.parametrize('fmt,entry,fields', [
    (
        '"%400r" "%r"',
        '"-" "GET /index.html HTTP/1.1"',
        {"request_line": "GET /index.html HTTP/1.1"},
    ),
    (
        '"%r" "%400r"',
        '"GET /index.html HTTP/1.1" "-"',
        {"request_line": "GET /index.html HTTP/1.1"},
    ),
    (
        '"%!400r" "%r"',
        '"-" "GET /index.xml HTTP/1.1"',
        {"request_line": "GET /index.xml HTTP/1.1"},
    ),
    (
        '"%r" "%!400r"',
        '"GET /index.xml HTTP/1.1" "-"',
        {"request_line": "GET /index.xml HTTP/1.1"},
    ),
    (
        '%<s %s %>s',
        '201 202 203',
        {
            "original_status": 201,
            "status": 202,
            "final_status": 203,
        },
    ),
    (
        '%<{Referer}i %{Referer}i %>{Referer}i',
        'http://example.com/original http://example.com/default http://example.com/final',
        {
            "original_headers_in": {
                "Referer": "http://example.com/original",
            },
            "headers_in": {
                "Referer": "http://example.com/default",
            },
            "final_headers_in": {
                "Referer": "http://example.com/final",
            },
        },
    ),
    (
        '%T %{ms}T',
        '1 1042',
        {
            "request_duration_seconds": 1,
            "request_duration_milliseconds": 1042,
        }
    ),
    (
        "%{%Y-%m-%d %H:%M:%S %z}t [%{msec_frac}t] %s %a:%{remote}p <-> %A:%p \"%m\" \"%U%q\" \"%f\" %P:%{tid}P \"%R\"",
        '2019-05-05 20:49:14 +0000 [690] 403 172.21.0.1:44782 <-> 172.21.0.2:80 "GET" "/wsgi/test?q=foo" "/usr/local/app/run.wsgi" 16:140168282543872 "wsgi-script"',
        {
            "request_time": datetime(2019, 5, 5, 20, 49, 14, 690000,
                                     tzinfo=timezone.utc),
            "request_time_fields": {
                "year": 2019,
                "mon": 5,
                "mday": 5,
                "hour": 20,
                "min": 49,
                "sec": 14,
                "timezone": timezone.utc,
                "msec_frac": 690,
            },
            "status": 403,
            "remote_address": "172.21.0.1",
            "remote_port": 44782,
            "local_address": "172.21.0.2",
            "server_port": 80,
            "request_method": "GET",
            "request_uri": "/wsgi/test",
            "request_query": "?q=foo",
            "request_file": "/usr/local/app/run.wsgi",
            "pid": 16,
            "tid": 140168282543872,
            "handler": "wsgi-script",
        },
    ),
    (
        "%{%Y-%m-%d %H:%M:%S %z}t [%{msec_frac}t] %s %a:%{remote}p <-> %A:%p \"%m\" \"%U%q\" \"%f\" %P:%{tid}P \"%R\"",
        r'2019-05-05 20:56:07 +0000 [148] 403 172.22.0.1:34488 <-> 172.22.0.2:80 "GET" "/wsgi/t\xc3\xa9st" "/usr/local/app/run.wsgi" 16:140436276180736 "wsgi-script"',
        {
            "request_time": datetime(2019, 5, 5, 20, 56, 7, 148000,
                                     tzinfo=timezone.utc),
            "request_time_fields": {
                "year": 2019,
                "mon": 5,
                "mday": 5,
                "hour": 20,
                "min": 56,
                "sec": 7,
                "timezone": timezone.utc,
                "msec_frac": 148,
            },
            "status": 403,
            "remote_address": "172.22.0.1",
            "remote_port": 34488,
            "local_address": "172.22.0.2",
            "server_port": 80,
            "request_method": "GET",
            "request_uri": "/wsgi/t\xc3\xa9st",
            "request_query": "",
            "request_file": "/usr/local/app/run.wsgi",
            "pid": 16,
            "tid": 140436276180736,
            "handler": "wsgi-script",
        },
    ),
    ("%200f", "-", {"request_file": None}),
    (
        "%200f",
        "/var/www/html/index.html",
        {"request_file": "/var/www/html/index.html"},
    ),
    (
        "%200{%Y-%m-%d}t",
        "-",
        {
            "request_time": None,
            "request_time_fields": {
                "year": None,
                "mon": None,
                "mday": None,
            }
        },
    ),
    (
        "%200{%Y-%m-%d}t",
        "2019-05-06",
        {
            "request_time": None,
            "request_time_fields": {
                "year": 2019,
                "mon": 5,
                "mday": 6,
            },
        },
    ),
    (
        VHOST_COMBINED,
        r'www.varonathe.org:80 185.234.218.71 - - [14/Apr/2018:18:39:42 +0000] "GET / HTTP/1.1" 301 539 "-" "}__test|O:21:\"JDatabaseDriverMysqli\":3:{s:4:\"\\0\\0\\0a\";O:17:\"JSimplepieFactory\":0:{}s:21:\"\\0\\0\\0disconnectHandlers\";a:1:{i:0;a:2:{i:0;O:9:\"SimplePie\":5:{s:8:\"sanitize\";O:20:\"JDatabaseDriverMysql\":0:{}s:5:\"cache\";b:1;s:19:\"cache_name_function\";s:6:\"assert\";s:10:\"javascript\";i:9999;s:8:\"feed_url\";s:54:\"eval(base64_decode($_POST[111]));JFactory::get();exit;\";}i:1;s:4:\"init\";}}s:13:\"\\0\\0\\0connection\";i:1;}\xf0\x9d\x8c\x86"',
        {
            "virtual_host": "www.varonathe.org",
            "server_port": 80,
            "remote_host": "185.234.218.71",
            "remote_logname": None,
            "remote_user": None,
            "request_time": datetime(2018, 4, 14, 18, 39, 42, tzinfo=timezone.utc),
            "request_time_fields": {
                "timestamp": datetime(2018, 4, 14, 18, 39, 42, tzinfo=timezone.utc),
            },
            "request_line": "GET / HTTP/1.1",
            "final_status": 301,
            "bytes_out": 539,
            "headers_in": {
                "Referer": None,
                "User-Agent": '}__test|O:21:\"JDatabaseDriverMysqli\":3:{s:4:\"\\0\\0\\0a\";O:17:\"JSimplepieFactory\":0:{}s:21:\"\\0\\0\\0disconnectHandlers\";a:1:{i:0;a:2:{i:0;O:9:\"SimplePie\":5:{s:8:\"sanitize\";O:20:\"JDatabaseDriverMysql\":0:{}s:5:\"cache\";b:1;s:19:\"cache_name_function\";s:6:\"assert\";s:10:\"javascript\";i:9999;s:8:\"feed_url\";s:54:\"eval(base64_decode($_POST[111]));JFactory::get();exit;\";}i:1;s:4:\"init\";}}s:13:\"\\0\\0\\0connection\";i:1;}\xf0\x9d\x8c\x86',
            },
        },
    ),
])
def test_parse_misc(fmt, entry, fields):
    log_entry = LogParser(fmt).parse(entry)
    for k,v in fields.items():
        assert getattr(log_entry, k) == v
