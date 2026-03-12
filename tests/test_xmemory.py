import sys

import pytest


def test_help_flag_prints_usage_examples(capsys, monkeypatch, load_tool_module):
    module = load_tool_module("xmemory")

    monkeypatch.setattr(sys, "argv", ["xmemory", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "ralph-session-log" in captured.out
    assert "Examples:" in captured.out
    assert captured.err == ""


def test_upsert_session_log_adds_new_section(load_tool_module):
    module = load_tool_module("xmemory")
    note_text = "# Ralph\n\n## Status\n- Current\n"

    updated = module.upsert_session_log(
        note_text,
        "2026-03-12",
        ["Implemented xmemory", "Ran pytest and Ruff"],
    )

    assert "## Ralph's Session Log" in updated
    assert "### 2026-03-12" in updated
    assert "- Implemented xmemory" in updated
    assert "- Ran pytest and Ruff" in updated


def test_upsert_session_log_replaces_existing_date_entry(load_tool_module):
    module = load_tool_module("xmemory")
    note_text = (
        "# Ralph\n\n"
        "## Ralph's Session Log\n"
        "### 2026-03-11\n"
        "- Older work\n\n"
        "### 2026-03-12\n"
        "- Stale item\n"
    )

    updated = module.upsert_session_log(
        note_text,
        "2026-03-12",
        ["Implemented xmemory", "Verified tests"],
    )

    assert "- Stale item" not in updated
    assert updated.count("### 2026-03-12") == 1
    assert "- Implemented xmemory" in updated
    assert "- Verified tests" in updated


def test_main_writes_session_log_to_requested_file(
    tmp_path, capsys, monkeypatch, load_tool_module
):
    module = load_tool_module("xmemory")
    memory_file = tmp_path / "ralph.md"
    memory_file.write_text("# Ralph\n", encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xmemory",
            "ralph-session-log",
            "--memory-file",
            str(memory_file),
            "--date",
            "2026-03-12",
            "Implemented xmemory",
            "Ran pytest and Ruff",
        ],
    )

    module.main()

    captured = capsys.readouterr()
    note_text = memory_file.read_text(encoding="utf-8")
    assert "Updated Ralph session log" in captured.out
    assert "## Ralph's Session Log" in note_text
    assert "### 2026-03-12" in note_text


def test_main_exits_when_no_work_items_are_provided(
    monkeypatch, capsys, load_tool_module
):
    module = load_tool_module("xmemory")
    monkeypatch.setattr(sys, "argv", ["xmemory", "ralph-session-log"])

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Usage: xmemory ralph-session-log" in captured.err
