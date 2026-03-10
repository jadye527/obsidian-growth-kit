import importlib.machinery
import importlib.util
import pathlib
import sys

import pytest


ROOT = pathlib.Path(__file__).resolve().parents[1]
XQUEUE_PATH = ROOT / "tools" / "xqueue"


def load_xqueue_module():
    loader = importlib.machinery.SourceFileLoader("xqueue_module", str(XQUEUE_PATH))
    spec = importlib.util.spec_from_loader("xqueue_module", loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_help_flag_prints_usage_examples(capsys, monkeypatch):
    module = load_xqueue_module()

    monkeypatch.setattr(sys, "argv", ["xqueue", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "Examples:" in captured.out
    assert 'xqueue add "Shipping one useful change at a time"' in captured.out
    assert captured.err == ""


def test_no_args_prints_help_without_loading_queue(capsys, monkeypatch):
    module = load_xqueue_module()

    def fail_load_queue():
        raise AssertionError("load_queue should not be called for help output")

    monkeypatch.setattr(module, "load_queue", fail_load_queue)
    monkeypatch.setattr(sys, "argv", ["xqueue"])

    module.main()

    captured = capsys.readouterr()
    assert "Commands:" in captured.out
    assert captured.err == ""


def test_unknown_command_exits_with_error(monkeypatch, capsys):
    module = load_xqueue_module()

    monkeypatch.setattr(sys, "argv", ["xqueue", "bogus"])
    monkeypatch.setattr(module, "load_queue", lambda: {"tweets": [], "last_posted": 0})

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Unknown command: bogus" in captured.err


def test_load_queue_error_exits_with_actionable_message(monkeypatch, capsys):
    module = load_xqueue_module()

    monkeypatch.setattr(sys, "argv", ["xqueue", "list"])
    monkeypatch.setattr(
        module,
        "load_queue",
        lambda: (_ for _ in ()).throw(
            module.QueueError("Unable to read queue file /tmp/queue.json: denied")
        ),
    )

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Queue error:" in captured.err
    assert "Unable to read queue file" in captured.err


def test_save_queue_error_on_add_exits_with_actionable_message(monkeypatch, capsys):
    module = load_xqueue_module()

    monkeypatch.setattr(sys, "argv", ["xqueue", "add", "hello"])
    monkeypatch.setattr(module, "load_queue", lambda: {"tweets": [], "last_posted": 0})
    monkeypatch.setattr(
        module,
        "save_queue",
        lambda q: (_ for _ in ()).throw(
            module.QueueError("Unable to write queue file /tmp/queue.json: denied")
        ),
    )

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Queue error:" in captured.err
    assert "Unable to write queue file" in captured.err


def test_next_on_empty_queue_prints_message(monkeypatch, capsys):
    module = load_xqueue_module()

    monkeypatch.setattr(sys, "argv", ["xqueue", "next"])
    monkeypatch.setattr(module, "load_queue", lambda: {"tweets": [], "last_posted": 0})

    module.main()

    captured = capsys.readouterr()
    assert captured.out.strip() == "Queue empty."
    assert captured.err == ""


def test_flush_on_empty_queue_prints_message(monkeypatch, capsys):
    module = load_xqueue_module()

    monkeypatch.setattr(sys, "argv", ["xqueue", "flush"])
    monkeypatch.setattr(module, "load_queue", lambda: {"tweets": [], "last_posted": 0})

    module.main()

    captured = capsys.readouterr()
    assert captured.out.strip() == "Queue empty."
    assert captured.err == ""
