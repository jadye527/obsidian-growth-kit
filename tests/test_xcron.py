import json
import sys

import pytest


def test_help_flag_prints_usage_examples(capsys, monkeypatch, load_tool_module):
    module = load_tool_module("xcron")

    monkeypatch.setattr(sys, "argv", ["xcron", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "Examples:" in captured.out
    assert "xcron content-scout" in captured.out
    assert captured.err == ""


def test_no_args_prints_help_without_running_commands(
    capsys, monkeypatch, load_tool_module
):
    module = load_tool_module("xcron")

    def fail_run_command(*args, **kwargs):
        raise AssertionError("run_command should not be called for help output")

    monkeypatch.setattr(module, "run_command", fail_run_command)
    monkeypatch.setattr(sys, "argv", ["xcron"])

    module.main()

    captured = capsys.readouterr()
    assert "Commands:" in captured.out
    assert captured.err == ""


def test_unknown_command_exits_with_error(monkeypatch, capsys, load_tool_module):
    module = load_tool_module("xcron")

    monkeypatch.setattr(sys, "argv", ["xcron", "bogus"])

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Unknown command: bogus" in captured.err


def test_queue_reactive_posts_adds_posts_until_target(
    monkeypatch, load_tool_module
):
    module = load_tool_module("xcron")
    commands = []

    monkeypatch.setattr(module, "get_queue_count", lambda dry_run=False: 1)
    monkeypatch.setattr(
        module,
        "load_scout_results",
        lambda: [
            {
                "id": "101",
                "topic": "ai-agents",
                "text": "Operators that iterate quickly keep winning distribution.",
            },
            {
                "id": "202",
                "topic": "prediction-markets",
                "text": "The market is rewarding faster feedback loops again.",
            },
            {
                "id": "303",
                "topic": "weather-trading",
                "text": (
                    "Weather data is becoming a tradable edge instead of "
                    "a forecast."
                ),
            },
        ],
    )

    def fake_run_command(args, dry_run=False):
        commands.append(args)
        return ""

    monkeypatch.setattr(module, "run_command", fake_run_command)

    added = module.queue_reactive_posts(target_count=3)

    assert added == 2
    assert commands[0][0:2] == ["xqueue", "add"]
    assert commands[1][0:2] == ["xqueue", "add"]
    assert len(commands) == 2


def test_like_top_scout_results_only_likes_numeric_ids_above_threshold(
    monkeypatch, load_tool_module
):
    module = load_tool_module("xcron")
    commands = []

    monkeypatch.setattr(
        module,
        "load_scout_results",
        lambda: [
            {"id": "not-numeric", "likes": 999},
            {"id": "12345", "likes": 60},
            {"id": "67890", "likes": 80},
            {"id": "11223", "likes": 40},
        ],
    )

    def fake_run_command(args, dry_run=False):
        commands.append(args)
        return ""

    monkeypatch.setattr(module, "run_command", fake_run_command)

    liked = module.like_top_scout_results(min_likes=50, limit=2)

    assert liked == 2
    assert commands == [["xpost", "like", "12345"], ["xpost", "like", "67890"]]


def test_morning_growth_runs_pipeline_and_refills_queue(
    monkeypatch, load_tool_module
):
    module = load_tool_module("xcron")
    commands = []
    queue_targets = []

    def fake_run_command(args, dry_run=False):
        commands.append(args)
        return ""

    monkeypatch.setattr(module, "run_command", fake_run_command)
    monkeypatch.setattr(
        module,
        "queue_reactive_posts",
        lambda target_count, dry_run=False: queue_targets.append(target_count),
    )

    module.run_morning_growth()

    assert commands == [
        ["xanalytics", "snapshot"],
        ["xanalytics", "compare"],
        ["xscout", "scan"],
        ["xgrowth", "track"],
        ["xgrowth", "new-strategy"],
    ]
    assert queue_targets == [5]


def test_load_scout_results_reads_configured_file(
    tmp_path, monkeypatch, load_tool_module
):
    module = load_tool_module("xcron")
    results_path = tmp_path / "scout-results.json"
    results_path.write_text(
        json.dumps({"results": [{"id": "1", "text": "hello"}]}),
        encoding="utf-8",
    )
    monkeypatch.setattr(module, "SCOUT_RESULTS_FILE", str(results_path))

    assert module.load_scout_results() == [{"id": "1", "text": "hello"}]
