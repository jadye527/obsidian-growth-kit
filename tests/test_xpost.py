import importlib.util
import importlib.machinery
import pathlib
import sys

import pytest


ROOT = pathlib.Path(__file__).resolve().parents[1]
XPOST_PATH = ROOT / "tools" / "xpost"


def load_xpost_module():
    loader = importlib.machinery.SourceFileLoader("xpost_module", str(XPOST_PATH))
    spec = importlib.util.spec_from_loader("xpost_module", loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_help_flag_prints_usage_examples(capsys, monkeypatch):
    module = load_xpost_module()

    monkeypatch.setattr(sys, "argv", ["xpost", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "Examples:" in captured.out
    assert 'xpost tweet "Shipping the help flag today"' in captured.out
    assert captured.err == ""


def test_no_args_prints_help_without_loading_keys(capsys, monkeypatch):
    module = load_xpost_module()

    def fail_load_keys():
        raise AssertionError("load_keys should not be called for help output")

    monkeypatch.setattr(module, "load_keys", fail_load_keys)
    monkeypatch.setattr(sys, "argv", ["xpost"])

    module.main()

    captured = capsys.readouterr()
    assert "Commands:" in captured.out
    assert captured.err == ""


def test_unknown_command_exits_with_error(monkeypatch, capsys):
    module = load_xpost_module()

    monkeypatch.setattr(sys, "argv", ["xpost", "bogus"])
    monkeypatch.setattr(module, "load_keys", lambda: {})
    monkeypatch.setattr(module, "get_client", lambda env: object())

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Unknown command: bogus" in captured.err
