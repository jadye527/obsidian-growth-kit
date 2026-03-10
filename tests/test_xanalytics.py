import sys

import pytest


def test_help_flag_prints_usage_examples(capsys, monkeypatch, load_tool_module):
    module = load_tool_module("xanalytics")

    monkeypatch.setattr(sys, "argv", ["xanalytics", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "Examples:" in captured.out
    assert "xanalytics top 10" in captured.out
    assert captured.err == ""


def test_no_args_prints_help_without_loading_keys(
    capsys, monkeypatch, load_tool_module
):
    module = load_tool_module("xanalytics")

    def fail_load_keys():
        raise AssertionError("load_keys should not be called for help output")

    monkeypatch.setattr(module, "load_keys", fail_load_keys)
    monkeypatch.setattr(sys, "argv", ["xanalytics"])

    module.main()

    captured = capsys.readouterr()
    assert "Commands:" in captured.out
    assert captured.err == ""


def test_unknown_command_exits_with_error(monkeypatch, capsys, load_tool_module):
    module = load_tool_module("xanalytics")

    monkeypatch.setattr(sys, "argv", ["xanalytics", "bogus"])
    monkeypatch.setattr(module, "load_keys", lambda: {})
    monkeypatch.setattr(module, "get_client", lambda env: object())
    monkeypatch.setattr(module, "load_data", lambda: {"snapshots": [], "posts": {}})

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Unknown command: bogus" in captured.err


def test_top_rejects_non_numeric_limit(monkeypatch, capsys, load_tool_module):
    module = load_tool_module("xanalytics")

    monkeypatch.setattr(sys, "argv", ["xanalytics", "top", "abc"])
    monkeypatch.setattr(module, "load_keys", lambda: {})
    monkeypatch.setattr(module, "get_client", lambda env: object())
    monkeypatch.setattr(module, "load_data", lambda: {"snapshots": [], "posts": {}})

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Invalid count for top: 'abc'" in captured.err


def test_top_rejects_non_positive_limit(monkeypatch, capsys, load_tool_module):
    module = load_tool_module("xanalytics")

    monkeypatch.setattr(sys, "argv", ["xanalytics", "top", "0"])
    monkeypatch.setattr(module, "load_keys", lambda: {})
    monkeypatch.setattr(module, "get_client", lambda env: object())
    monkeypatch.setattr(module, "load_data", lambda: {"snapshots": [], "posts": {}})

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Invalid count for top: '0'" in captured.err
