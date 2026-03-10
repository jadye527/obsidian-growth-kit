import importlib.machinery
import importlib.util
import pathlib
import sys
from datetime import datetime

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


@pytest.mark.parametrize(
    ("text", "expected_category"),
    [
        ("😂 We accidentally shipped innovation again", "humor"),
        ("Day 1 update: honest numbers and win rate", "build-in-public"),
        ("Tip: tighten your strategy around the gap between signals", "value"),
        ("📊 Results are in → better retention this week", "update"),
        ("@alice Thanks for the feedback", "reply"),
        ("Plain observation without a special marker", "general"),
    ],
)
def test_categorize_returns_expected_category(text, expected_category):
    module = load_xgrowth_module()

    assert module.categorize(text) == expected_category


def test_log_strategy_appends_new_strategy_with_metrics(monkeypatch, capsys):
    module = load_xgrowth_module()
    saved = {}
    existing = {
        "strategies": [
            {
                "date": "2026-03-09",
                "name": "Existing",
                "description": "Already logged",
                "metrics_before": "baseline",
                "metrics_after": "",
                "result": "",
            }
        ]
    }

    class FixedDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, 3, 10)

    monkeypatch.setattr(module, "load_json", lambda path, default=None: existing)
    monkeypatch.setattr(module, "save_json", lambda path, data: saved.update(data=data))
    monkeypatch.setattr(module, "datetime", FixedDateTime)

    module.log_strategy(
        "Question endings",
        "End every post with a direct question",
        "Before: 0.4 avg engagement",
    )

    captured = capsys.readouterr()
    assert captured.out.strip() == "✅ Strategy logged: Question endings"
    assert captured.err == ""
    assert len(saved["data"]["strategies"]) == 2
    assert saved["data"]["strategies"][-1] == {
        "date": "2026-03-10",
        "name": "Question endings",
        "description": "End every post with a direct question",
        "metrics_before": "Before: 0.4 avg engagement",
        "metrics_after": "",
        "result": "",
    }
