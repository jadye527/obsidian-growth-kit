import subprocess
import sys

import pytest


def test_help_flag_prints_usage_examples(capsys, monkeypatch, load_tool_module):
    module = load_tool_module("xmemory")

    monkeypatch.setattr(sys, "argv", ["xmemory", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "ralph-session-log" in captured.out
    assert "memory-search" in captured.out
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


def test_build_memory_search_url_appends_expected_query(load_tool_module):
    module = load_tool_module("xmemory")

    result = module.build_memory_search_url(
        "http://127.0.0.1:3000/api/memory",
        "ralph notes",
    )

    assert result == (
        "http://127.0.0.1:3000/api/memory?action=search&query=ralph+notes"
    )


def test_parse_memory_search_args_reads_defaults(monkeypatch, load_tool_module):
    module = load_tool_module("xmemory")
    monkeypatch.setenv("OPENCLAW_MEMORY_API_KEY", "test-key")
    monkeypatch.setenv("OPENCLAW_MEMORY_API_URL", "http://localhost:3000/api/memory")

    url, api_key, query, output_file = module.parse_memory_search_args(
        ["--query", "ralph", "--output", "~/tmp/result.json"]
    )

    assert url == "http://localhost:3000/api/memory"
    assert api_key == "test-key"
    assert query == "ralph"
    assert output_file.endswith("/tmp/result.json")


def test_parse_memory_search_args_requires_api_key(
    monkeypatch, capsys, load_tool_module
):
    module = load_tool_module("xmemory")
    monkeypatch.delenv("OPENCLAW_MEMORY_API_KEY", raising=False)

    with pytest.raises(SystemExit) as exc_info:
        module.parse_memory_search_args(
            ["--query", "ralph", "--output", "/tmp/out.json"]
        )

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Missing required option: --api-key" in captured.err


def test_main_memory_search_writes_response_to_output_file(
    tmp_path, capsys, monkeypatch, load_tool_module
):
    module = load_tool_module("xmemory")
    output_file = tmp_path / "ralph-memory-test.json"

    def fake_run(command, capture_output, check):
        assert capture_output is True
        assert check is False
        assert command == [
            "curl",
            "-sS",
            "http://127.0.0.1:3000/api/memory?action=search&query=ralph",
            "-H",
            "x-api-key: secret",
        ]
        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout=b'{"results":["ralph"]}\n',
            stderr=b"",
        )

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xmemory",
            "memory-search",
            "--api-key",
            "secret",
            "--query",
            "ralph",
            "--output",
            str(output_file),
        ],
    )

    module.main()

    captured = capsys.readouterr()
    assert "Saved memory search results" in captured.out
    assert output_file.read_text(encoding="utf-8") == '{"results":["ralph"]}\n'


def test_fetch_memory_search_exits_on_curl_error(
    monkeypatch, capsys, load_tool_module
):
    module = load_tool_module("xmemory")

    def fake_run(command, capture_output, check):
        return subprocess.CompletedProcess(
            args=command,
            returncode=7,
            stdout=b"",
            stderr=b"connection refused\n",
        )

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    with pytest.raises(SystemExit) as exc_info:
        module.fetch_memory_search(
            "http://127.0.0.1:3000/api/memory",
            "secret",
            "ralph",
        )

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "connection refused" in captured.err
