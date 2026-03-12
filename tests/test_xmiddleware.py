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
