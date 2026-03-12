import pathlib
import sys
from datetime import datetime, timezone

import pytest


def test_help_flag_prints_usage_examples(capsys, monkeypatch, load_tool_module):
    module = load_tool_module("xmeme")

    monkeypatch.setattr(sys, "argv", ["xmeme", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "generate" in captured.out
    assert captured.err == ""


def test_build_output_path_is_unique(monkeypatch, load_tool_module, tmp_path):
    module = load_tool_module("xmeme")

    class FixedDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, 3, 12, 18, 45, 0, tzinfo=timezone.utc)

    unique_values = iter(["aaaabbbbccccdddd", "1111222233334444"])
    fake_uuid = type(
        "FakeUuid",
        (),
        {"hex": property(lambda self: next(unique_values))},
    )

    monkeypatch.setattr(module, "datetime", FixedDateTime)
    monkeypatch.setattr(module, "uuid4", lambda: fake_uuid())

    first = pathlib.Path(module.build_output_path(str(tmp_path), "release"))
    second = pathlib.Path(module.build_output_path(str(tmp_path), "release"))

    assert first != second
    assert first.name == "release_20260312T184500Z_aaaabbbb.png"
    assert second.name == "release_20260312T184500Z_11112222.png"


def test_generate_meme_runs_generator_and_prints_new_path(
    monkeypatch, capsys, load_tool_module, tmp_path
):
    module = load_tool_module("xmeme")
    output_dir = tmp_path / "out"
    expected_path = output_dir / "fresh.png"
    calls = {}

    monkeypatch.setattr(
        module,
        "build_output_path",
        lambda output_dir_arg, prefix: str(expected_path),
    )

    def fake_run(args, capture_output, text, check):
        calls["args"] = args
        expected_path.write_bytes(b"png")
        return type("Result", (), {"returncode": 0, "stdout": "Saved", "stderr": ""})()

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    created = module.generate_meme(
        {
            "generator": "~/generator/memegen.py",
            "python": "/usr/bin/python3",
            "template": "fire.jpg",
            "top_text": "Ship now",
            "bottom_text": "Polish later",
            "output_dir": str(output_dir),
            "prefix": "release",
        }
    )

    captured = capsys.readouterr()
    assert created == str(expected_path)
    assert calls["args"] == [
        "/usr/bin/python3",
        str(pathlib.Path("~/generator/memegen.py").expanduser()),
        "fire.jpg",
        "Ship now",
        "Polish later",
        "--output",
        str(expected_path),
    ]
    assert captured.out.strip() == str(expected_path)
    assert captured.err == ""


def test_generate_requires_generator_path(monkeypatch, capsys, load_tool_module):
    module = load_tool_module("xmeme")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xmeme",
            "generate",
            "--template",
            "fire.jpg",
            "--top-text",
            "Ship now",
            "--output-dir",
            "/tmp/out",
        ],
    )
    monkeypatch.setattr(module, "DEFAULT_MEMEGEN_PATH", None)

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Use --generator or set X_MEMEGEN_PATH" in captured.err
