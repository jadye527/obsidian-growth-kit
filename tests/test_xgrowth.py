import importlib.machinery
import importlib.util
import pathlib
import sys

import pytest


ROOT = pathlib.Path(__file__).resolve().parents[1]
XGROWTH_PATH = ROOT / "tools" / "xgrowth"


def load_xgrowth_module():
    loader = importlib.machinery.SourceFileLoader(
        "xgrowth_module", str(XGROWTH_PATH)
    )
    spec = importlib.util.spec_from_loader("xgrowth_module", loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_help_flag_prints_usage_examples(capsys, monkeypatch):
    module = load_xgrowth_module()

    monkeypatch.setattr(sys, "argv", ["xgrowth", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "Examples:" in captured.out
    assert 'xgrowth log-strategy "Thread hooks"' in captured.out
    assert captured.err == ""


def test_no_args_prints_help_without_tracking(capsys, monkeypatch):
    module = load_xgrowth_module()

    def fail_track_performance():
        raise AssertionError("track_performance should not run for help output")

    monkeypatch.setattr(module, "track_performance", fail_track_performance)
    monkeypatch.setattr(sys, "argv", ["xgrowth"])

    module.main()

    captured = capsys.readouterr()
    assert "Commands:" in captured.out
    assert captured.err == ""


def test_unknown_command_exits_with_error(monkeypatch, capsys):
    module = load_xgrowth_module()

    monkeypatch.setattr(sys, "argv", ["xgrowth", "bogus"])

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Unknown command: bogus" in captured.err


def test_log_strategy_requires_name_and_description(monkeypatch, capsys):
    module = load_xgrowth_module()

    monkeypatch.setattr(sys, "argv", ["xgrowth", "log-strategy", "Thread hooks"])

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert 'Usage: xgrowth log-strategy "name" "description" [metrics]' in captured.err
