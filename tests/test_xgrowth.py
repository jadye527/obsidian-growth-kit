import sys
from datetime import datetime

import pytest


def test_help_flag_prints_usage_examples(capsys, monkeypatch, load_tool_module):
    module = load_tool_module("xgrowth")

    monkeypatch.setattr(sys, "argv", ["xgrowth", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "Examples:" in captured.out
    assert 'xgrowth log-strategy "Thread hooks"' in captured.out
    assert captured.err == ""


def test_no_args_prints_help_without_tracking(capsys, monkeypatch, load_tool_module):
    module = load_tool_module("xgrowth")

    def fail_track_performance():
        raise AssertionError("track_performance should not run for help output")

    monkeypatch.setattr(module, "track_performance", fail_track_performance)
    monkeypatch.setattr(sys, "argv", ["xgrowth"])

    module.main()

    captured = capsys.readouterr()
    assert "Commands:" in captured.out
    assert captured.err == ""


def test_unknown_command_exits_with_error(monkeypatch, capsys, load_tool_module):
    module = load_tool_module("xgrowth")

    monkeypatch.setattr(sys, "argv", ["xgrowth", "bogus"])

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Unknown command: bogus" in captured.err


def test_log_strategy_requires_name_and_description(
    monkeypatch, capsys, load_tool_module
):
    module = load_tool_module("xgrowth")

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
def test_categorize_returns_expected_category(
    text, expected_category, load_tool_module
):
    module = load_tool_module("xgrowth")

    assert module.categorize(text) == expected_category


def test_log_strategy_appends_new_strategy_with_metrics(
    monkeypatch, capsys, load_tool_module
):
    module = load_tool_module("xgrowth")
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


def test_load_memory_files_reads_all_markdown_files(tmp_path, load_tool_module):
    module = load_tool_module("xgrowth")
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    (memory_dir / "b-note.md").write_text("# B\n", encoding="utf-8")
    (memory_dir / "a-note.md").write_text("# A\n", encoding="utf-8")
    (memory_dir / "ignore.txt").write_text("skip", encoding="utf-8")

    memories = module.load_memory_files(str(memory_dir))

    assert [memory["name"] for memory in memories] == ["a-note.md", "b-note.md"]
    assert [memory["content"] for memory in memories] == ["# A\n", "# B\n"]


def test_load_memory_files_returns_empty_list_for_missing_directory(load_tool_module):
    module = load_tool_module("xgrowth")

    assert module.load_memory_files("/tmp/does-not-exist-xgrowth-memory") == []


def test_new_strategy_reads_and_prints_memory_files(
    monkeypatch, capsys, load_tool_module
):
    module = load_tool_module("xgrowth")
    memories = [
        {"name": "agents.md", "path": "/tmp/agents.md", "content": "# Agents\n"},
        {
            "name": "build-in-public.md",
            "path": "/tmp/build-in-public.md",
            "content": "# Build\n",
        },
    ]

    monkeypatch.setattr(module, "MEMORY_DIR", "/tmp/shared-memory")
    monkeypatch.setattr(module, "load_memory_files", lambda: memories)
    monkeypatch.setattr(sys, "argv", ["xgrowth", "new-strategy"])

    module.main()

    captured = capsys.readouterr()
    assert "Loaded 2 memory files from /tmp/shared-memory." in captured.out
    assert "  - agents.md" in captured.out
    assert "  - build-in-public.md" in captured.out
    assert "self-deprecating build-in-public humor" in captured.out
    assert captured.err == ""
