import pathlib
import subprocess


ROOT = pathlib.Path(__file__).resolve().parents[1]
XRECORD_PATH = ROOT / "tools" / "xrecord"


def run_xrecord(*args):
    return subprocess.run(
        ["bash", str(XRECORD_PATH), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_help_flag_prints_usage():
    result = run_xrecord("--help")

    assert result.returncode == 0
    assert "Usage:" in result.stdout
    assert "xrecord upload <name>" in result.stdout
    assert result.stderr == ""


def test_upload_requires_name():
    result = run_xrecord("upload")

    assert result.returncode == 1
    assert "Usage: xrecord upload <name>" in result.stderr


def test_svg_requires_existing_recording():
    result = run_xrecord("svg", "missing-demo")

    assert result.returncode == 1
    assert "Recording not found:" in result.stderr


def test_session_rejects_non_numeric_seconds():
    result = run_xrecord("session", "demo", "abc")

    assert result.returncode == 1
    assert "Seconds must be a positive integer" in result.stderr
