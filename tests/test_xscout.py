import importlib.machinery
import importlib.util
import pathlib
import sys

import pytest


ROOT = pathlib.Path(__file__).resolve().parents[1]
XSCOUT_PATH = ROOT / "tools" / "xscout"


def load_xscout_module():
    loader = importlib.machinery.SourceFileLoader("xscout_module", str(XSCOUT_PATH))
    spec = importlib.util.spec_from_loader("xscout_module", loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_help_flag_prints_usage_examples(capsys, monkeypatch):
    module = load_xscout_module()

    monkeypatch.setattr(sys, "argv", ["xscout", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "Examples:" in captured.out
    assert "xscout scan --topic ai-agents" in captured.out
    assert captured.err == ""


def test_no_args_prints_help_without_running_scan(capsys, monkeypatch):
    module = load_xscout_module()

    def fail_scan(topic_filter=None):
        raise AssertionError("scan should not be called for help output")

    monkeypatch.setattr(module, "scan", fail_scan)
    monkeypatch.setattr(sys, "argv", ["xscout"])

    module.main()

    captured = capsys.readouterr()
    assert "Commands:" in captured.out
    assert captured.err == ""


def test_unknown_command_exits_with_error(monkeypatch, capsys):
    module = load_xscout_module()

    monkeypatch.setattr(sys, "argv", ["xscout", "bogus"])

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Unknown command: bogus" in captured.err


def test_scan_requires_topic_value(monkeypatch, capsys):
    module = load_xscout_module()

    monkeypatch.setattr(sys, "argv", ["xscout", "scan", "--topic"])

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Usage: xscout scan --topic <topic>" in captured.err
    assert "Available topics:" in captured.err


def test_scan_rejects_unknown_topic(monkeypatch, capsys):
    module = load_xscout_module()

    monkeypatch.setattr(sys, "argv", ["xscout", "scan", "--topic", "bogus-topic"])

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Unknown topic: bogus-topic." in captured.err
