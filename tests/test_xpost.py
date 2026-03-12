import sys
import types

import pytest


def test_help_flag_prints_usage_examples(capsys, monkeypatch, load_tool_module):
    module = load_tool_module("xpost")

    monkeypatch.setattr(sys, "argv", ["xpost", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "Examples:" in captured.out
    assert 'xpost tweet "Shipping the help flag today"' in captured.out
    assert 'xpost --media ~/image.png --text "Shipping with media"' in captured.out
    assert captured.err == ""


def test_no_args_prints_help_without_loading_keys(
    capsys, monkeypatch, load_tool_module
):
    module = load_tool_module("xpost")

    def fail_load_keys():
        raise AssertionError("load_keys should not be called for help output")

    monkeypatch.setattr(module, "load_keys", fail_load_keys)
    monkeypatch.setattr(sys, "argv", ["xpost"])

    module.main()

    captured = capsys.readouterr()
    assert "Commands:" in captured.out
    assert captured.err == ""


def test_unknown_command_exits_with_error(monkeypatch, capsys, load_tool_module):
    module = load_tool_module("xpost")

    monkeypatch.setattr(sys, "argv", ["xpost", "bogus"])
    monkeypatch.setattr(module, "load_keys", lambda: {})
    monkeypatch.setattr(module, "get_client", lambda env: object())

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Unknown command: bogus" in captured.err


def test_missing_credentials_file_exits_with_actionable_error(
    monkeypatch, capsys, load_tool_module
):
    module = load_tool_module("xpost")

    monkeypatch.setattr(sys, "argv", ["xpost", "whoami"])
    monkeypatch.setattr(
        module,
        "load_keys",
        lambda: (_ for _ in ()).throw(
            module.CredentialsError("Credentials file not found: /tmp/keys.env")
        ),
    )

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Credential error:" in captured.err
    assert "Credentials file not found" in captured.err


def test_missing_required_credentials_exits(monkeypatch, capsys, load_tool_module):
    module = load_tool_module("xpost")

    monkeypatch.setattr(sys, "argv", ["xpost", "whoami"])
    monkeypatch.setattr(
        module,
        "load_keys",
        lambda: (_ for _ in ()).throw(
            module.CredentialsError(
                "Missing X credentials in /tmp/keys.env: X_API_KEY"
            )
        ),
    )

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Missing X credentials" in captured.err


def test_invalid_tweet_id_exits_before_client_call(
    monkeypatch, capsys, load_tool_module
):
    module = load_tool_module("xpost")
    client = types.SimpleNamespace(
        get_tweet=lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("client should not be called")
        )
    )

    monkeypatch.setattr(sys, "argv", ["xpost", "read", "abc123"])
    monkeypatch.setattr(module, "load_keys", lambda: {})
    monkeypatch.setattr(module, "get_client", lambda env: client)

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Invalid tweet ID" in captured.err


def test_network_error_is_reported(monkeypatch, capsys, load_tool_module):
    module = load_tool_module("xpost")
    client = types.SimpleNamespace(
        get_me=lambda **kwargs: (_ for _ in ()).throw(OSError("connection reset"))
    )

    monkeypatch.setattr(sys, "argv", ["xpost", "whoami"])
    monkeypatch.setattr(module, "load_keys", lambda: {})
    monkeypatch.setattr(module, "get_client", lambda env: client)

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Network error: connection reset" in captured.err


def test_bad_request_error_is_reported(monkeypatch, capsys, load_tool_module):
    module = load_tool_module("xpost")
    bad_request = type("BadRequest", (Exception,), {})
    client = types.SimpleNamespace(
        get_tweet=lambda *args, **kwargs: (_ for _ in ()).throw(
            bad_request("tweet not found")
        )
    )

    monkeypatch.setattr(sys, "argv", ["xpost", "read", "12345"])
    monkeypatch.setattr(module, "load_keys", lambda: {})
    monkeypatch.setattr(module, "get_client", lambda env: client)

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Bad tweet ID or request rejected: tweet not found" in captured.err


def test_flag_post_with_media_uploads_and_posts(
    monkeypatch, capsys, load_tool_module, tmp_path
):
    module = load_tool_module("xpost")
    media_file = tmp_path / "image.png"
    media_file.write_bytes(b"png")
    calls = {}

    class FakeClient:
        def create_tweet(self, **kwargs):
            calls["tweet"] = kwargs
            return types.SimpleNamespace(data={"id": "123"})

    class FakeMediaApi:
        def media_upload(self, filename):
            calls["media"] = filename
            return types.SimpleNamespace(media_id_string="999")

    monkeypatch.setattr(
        sys,
        "argv",
        ["xpost", "--media", str(media_file), "--text", "test"],
    )
    monkeypatch.setattr(
        module,
        "load_keys",
        lambda: {
            "X_API_KEY": "key",
            "X_API_SECRET": "secret",
            "X_ACCESS_TOKEN": "token",
            "X_ACCESS_TOKEN_SECRET": "token-secret",
            "X_USER_HANDLE": "tester",
        },
    )
    monkeypatch.setattr(module, "get_client", lambda env: FakeClient())
    monkeypatch.setattr(module, "get_media_api", lambda env: FakeMediaApi())

    module.main()

    captured = capsys.readouterr()
    assert calls["media"] == str(media_file)
    assert calls["tweet"] == {"text": "test", "media_ids": ["999"]}
    assert "https://x.com/tester/status/123" in captured.out
    assert captured.err == ""


def test_flag_post_missing_media_file_exits_before_api_calls(
    monkeypatch, capsys, load_tool_module, tmp_path
):
    module = load_tool_module("xpost")
    missing_file = tmp_path / "missing.png"

    monkeypatch.setattr(
        sys,
        "argv",
        ["xpost", "--media", str(missing_file), "--text", "test"],
    )
    monkeypatch.setattr(module, "load_keys", lambda: {})
    monkeypatch.setattr(
        module,
        "get_client",
        lambda env: (_ for _ in ()).throw(
            AssertionError("client should not be created")
        ),
    )

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert f"Media file not found: {missing_file}" in captured.err
