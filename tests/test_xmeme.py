import pathlib
import sys
from datetime import datetime, timezone
from io import BytesIO

import pytest


def test_help_flag_prints_usage_examples(capsys, monkeypatch, load_tool_module):
    module = load_tool_module("xmeme")

    monkeypatch.setattr(sys, "argv", ["xmeme", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "generate" in captured.out
    assert "download-templates" in captured.out
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


def test_build_fresh_output_path_skips_existing_files(
    monkeypatch, load_tool_module, tmp_path
):
    module = load_tool_module("xmeme")
    existing = tmp_path / "release_existing.png"
    fresh = tmp_path / "release_fresh.png"
    existing.write_bytes(b"old")
    candidates = iter([str(existing), str(fresh)])

    monkeypatch.setattr(module, "build_output_path", lambda output_dir, prefix: next(candidates))

    assert module.build_fresh_output_path(str(tmp_path), "release") == str(fresh)


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


def test_parse_download_args_defaults(load_tool_module):
    module = load_tool_module("xmeme")

    options = module.parse_download_args([])

    assert options == {"count": 8, "output_dir": "out/templates"}


def test_select_templates_prefers_curated_variety(load_tool_module):
    module = load_tool_module("xmeme")

    templates = [
        {"name": "Ancient Aliens", "url": "https://example.com/aliens.jpg"},
        {"name": "Distracted Boyfriend", "url": "https://example.com/distracted.jpg"},
        {"name": "Change My Mind", "url": "https://example.com/change.jpg"},
        {"name": "Drake Hotline Bling", "url": "https://example.com/drake.jpg"},
        {"name": "Two Buttons", "url": "https://example.com/buttons.jpg"},
        {"name": "Gru's Plan", "url": "https://example.com/gru.jpg"},
    ]

    selected = module.select_templates(templates, 4)

    assert [template["name"] for template in selected] == [
        "Drake Hotline Bling",
        "Two Buttons",
        "Distracted Boyfriend",
        "Change My Mind",
    ]


def test_select_templates_falls_back_to_remaining_items(load_tool_module):
    module = load_tool_module("xmeme")

    templates = [
        {"name": "Ancient Aliens", "url": "https://example.com/aliens.jpg"},
        {"name": "Woman Yelling At Cat", "url": "https://example.com/cat.jpg"},
        {"name": "Is This A Pigeon", "url": "https://example.com/pigeon.jpg"},
    ]

    selected = module.select_templates(templates, 2)

    assert [template["name"] for template in selected] == [
        "Ancient Aliens",
        "Woman Yelling At Cat",
    ]


def test_download_templates_fetches_and_saves_files(
    monkeypatch, capsys, load_tool_module, tmp_path
):
    module = load_tool_module("xmeme")

    class FakeResponse(BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            self.close()
            return False

    payload = (
        b'{"success": true, "data": {"memes": ['
        b'{"name": "Ancient Aliens", "url": "https://i.imgflip.com/aliens.jpg"},'
        b'{"name": "Drake Hotline Bling", "url": "https://i.imgflip.com/30b1gx.jpg"},'
        b'{"name": "Two Buttons", "url": "https://i.imgflip.com/1g8my4.jpg"}'
        b"]}}"
    )

    def fake_urlopen(request, timeout):
        url = request.full_url
        assert timeout == 30
        if url == module.IMGFLIP_API_URL:
            return FakeResponse(payload)
        if url == "https://i.imgflip.com/aliens.jpg":
            return FakeResponse(b"aliens")
        if url == "https://i.imgflip.com/30b1gx.jpg":
            return FakeResponse(b"drake")
        if url == "https://i.imgflip.com/1g8my4.jpg":
            return FakeResponse(b"buttons")
        raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr(module, "urlopen", fake_urlopen)

    saved_paths = module.download_templates(
        {"count": 2, "output_dir": str(tmp_path / "templates")}
    )

    captured = capsys.readouterr()
    assert saved_paths == [
        str(tmp_path / "templates" / "drake-hotline-bling.jpg"),
        str(tmp_path / "templates" / "two-buttons.jpg"),
    ]
    assert (tmp_path / "templates" / "drake-hotline-bling.jpg").read_bytes() == b"drake"
    assert (tmp_path / "templates" / "two-buttons.jpg").read_bytes() == b"buttons"
    assert captured.out.strip().splitlines() == saved_paths
    assert captured.err == ""


def test_download_templates_reports_network_errors(
    monkeypatch, capsys, load_tool_module, tmp_path
):
    module = load_tool_module("xmeme")

    def fake_urlopen(request, timeout):
        raise OSError("offline")

    monkeypatch.setattr(module, "urlopen", fake_urlopen)

    with pytest.raises(SystemExit) as exc_info:
        module.download_templates({"count": 2, "output_dir": str(tmp_path / "templates")})

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "template download failed: offline" in captured.err
