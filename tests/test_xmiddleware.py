import sys

import pytest


def test_help_flag_prints_usage(capsys, monkeypatch, load_tool_module):
    module = load_tool_module("xmiddleware")

    monkeypatch.setattr(sys, "argv", ["xmiddleware", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "probe --url <url>" in captured.out
    assert captured.err == ""


def test_parse_probe_args_requires_url(load_tool_module):
    module = load_tool_module("xmiddleware")

    with pytest.raises(SystemExit) as exc_info:
        module.parse_probe_args(["--host", "example.trycloudflare.com"])

    assert exc_info.value.code == 1


def test_parse_login_args_derives_me_url(load_tool_module):
    module = load_tool_module("xmiddleware")

    options = module.parse_login_args(
        [
            "--login-url",
            "https://example.trycloudflare.com/api/auth/login",
            "--username",
            "admin",
            "--password",
            "secret",
        ]
    )

    assert options["me_url"] == "https://example.trycloudflare.com/api/auth/me"


def test_probe_sets_host_and_cookie_headers(monkeypatch, load_tool_module):
    module = load_tool_module("xmiddleware")
    captured = {}

    class FakeResponse:
        headers = {"content-type": "text/plain"}

        def getcode(self):
            return 200

        def read(self):
            return b"ok"

    def fake_fetch_response(request, timeout):
        captured["headers"] = dict(request.header_items())
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(module, "fetch_response", fake_fetch_response)

    result = module.probe(
        "http://127.0.0.1:3000/api/auth/me",
        host="example.trycloudflare.com",
        cookie="session=abc123",
        timeout=7.5,
    )

    assert captured["headers"]["Host"] == "example.trycloudflare.com"
    assert captured["headers"]["Cookie"] == "session=abc123"
    assert captured["timeout"] == 7.5
    assert result["status"] == 200


def test_analyze_probe_flags_host_block(load_tool_module):
    module = load_tool_module("xmiddleware")

    analysis = module.analyze_probe(
        {
            "status": 403,
            "headers": {"content-type": "text/plain"},
            "body": "Forbidden: invalid host header",
            "host": "example.trycloudflare.com",
            "cookie_sent": False,
            "url": "http://127.0.0.1:3000/",
        }
    )

    assert analysis["host_blocked"] is True
    assert analysis["cookie_rejected"] is False
    assert "host blocked" in analysis["conclusion"].lower()


def test_analyze_probe_flags_cookie_rejection(load_tool_module):
    module = load_tool_module("xmiddleware")

    analysis = module.analyze_probe(
        {
            "status": 307,
            "headers": {
                "location": "/login",
                "x-middleware-rewrite": "/login",
            },
            "body": "",
            "host": None,
            "cookie_sent": True,
            "url": "https://example.trycloudflare.com/dashboard",
        }
    )

    assert analysis["host_blocked"] is False
    assert analysis["cookie_rejected"] is True
    assert analysis["middleware_headers"] == {"x-middleware-rewrite": "/login"}


def test_verify_login_confirms_session_cookie(monkeypatch, load_tool_module):
    module = load_tool_module("xmiddleware")
    requests = []

    def fake_perform_request(
        url,
        *,
        method,
        host=None,
        cookie=None,
        timeout=10.0,
        json_body=None,
    ):
        requests.append(
            {
                "url": url,
                "method": method,
                "host": host,
                "cookie": cookie,
                "timeout": timeout,
                "json_body": json_body,
            }
        )
        if method == "POST":
            return {
                "url": url,
                "status": 200,
                "headers": {"set-cookie": "mc-session=abc123; Path=/; HttpOnly; Secure; SameSite=None"},
                "set_cookie_headers": [
                    "mc-session=abc123; Path=/; HttpOnly; Secure; SameSite=None"
                ],
                "body": '{"user":{"username":"admin"}}',
                "host": host,
                "cookie_sent": False,
            }
        return {
            "url": url,
            "status": 200,
            "headers": {},
            "set_cookie_headers": [],
            "body": '{"user":{"username":"admin"}}',
            "host": host,
            "cookie_sent": bool(cookie),
        }

    monkeypatch.setattr(module, "perform_request", fake_perform_request)

    verification = module.verify_login(
        "https://example.trycloudflare.com/api/auth/login",
        "admin",
        "secret",
        me_url="https://example.trycloudflare.com/api/auth/me",
        host="example.trycloudflare.com",
        timeout=7.5,
    )

    assert verification["session_verified"] is True
    assert verification["session_cookie"] == "mc-session=abc123"
    assert requests[0]["json_body"] == {"username": "admin", "password": "secret"}
    assert requests[1]["cookie"] == "mc-session=abc123"
    assert requests[1]["host"] == "example.trycloudflare.com"


def test_verify_login_flags_browser_cookie_rejection(monkeypatch, load_tool_module):
    module = load_tool_module("xmiddleware")

    def fake_perform_request(
        url,
        *,
        method,
        host=None,
        cookie=None,
        timeout=10.0,
        json_body=None,
    ):
        if method == "POST":
            return {
                "url": url,
                "status": 200,
                "headers": {"set-cookie": "mc-session=abc123; Path=/; HttpOnly; SameSite=None"},
                "set_cookie_headers": [
                    "mc-session=abc123; Path=/; HttpOnly; SameSite=None"
                ],
                "body": '{"user":{"username":"admin"}}',
                "host": host,
                "cookie_sent": False,
            }
        return {
            "url": url,
            "status": 401,
            "headers": {"location": "/login"},
            "set_cookie_headers": [],
            "body": "",
            "host": host,
            "cookie_sent": bool(cookie),
        }

    monkeypatch.setattr(module, "perform_request", fake_perform_request)

    verification = module.verify_login(
        "https://example.trycloudflare.com/api/auth/login",
        "admin",
        "secret",
        me_url="https://example.trycloudflare.com/api/auth/me",
    )

    assert verification["session_verified"] is False
    assert (
        verification["cookie_analysis"]["browser_reject_reason"]
        == "SameSite=None without Secure will be dropped by browsers."
    )
    assert "SameSite=None without Secure" in verification["conclusion"]


def test_main_prints_probe_summary(capsys, monkeypatch, load_tool_module):
    module = load_tool_module("xmiddleware")

    monkeypatch.setattr(
        sys,
        "argv",
        ["xmiddleware", "probe", "--url", "https://example.com"],
    )
    monkeypatch.setattr(
        module,
        "probe",
        lambda url, host=None, cookie=None, timeout=10.0: {
            "url": url,
            "status": 200,
            "headers": {},
            "body": "ok",
            "host": host,
            "cookie_sent": bool(cookie),
        },
    )

    module.main()

    captured = capsys.readouterr()
    assert "URL: https://example.com" in captured.out
    assert "Conclusion:" in captured.out
    assert captured.err == ""


def test_main_prints_login_summary(capsys, monkeypatch, load_tool_module):
    module = load_tool_module("xmiddleware")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xmiddleware",
            "login",
            "--login-url",
            "https://example.com/api/auth/login",
            "--username",
            "admin",
            "--password",
            "secret",
        ],
    )
    monkeypatch.setattr(
        module,
        "verify_login",
        lambda login_url, username, password, *, me_url, host=None, timeout=10.0: {
            "login_result": {"url": login_url, "status": 200},
            "me_result": {"url": me_url, "status": 200},
            "me_analysis": {"location": "", "middleware_headers": {}},
            "cookie_analysis": {
                "cookie_header": "mc-session=abc123",
                "browser_reject_reason": "",
            },
            "session_cookie": "mc-session=abc123",
            "session_verified": True,
            "conclusion": "Login works end-to-end through the tunnel.",
        },
    )

    module.main()

    captured = capsys.readouterr()
    assert "Login URL: https://example.com/api/auth/login" in captured.out
    assert "Session verified: yes" in captured.out
    assert captured.err == ""
