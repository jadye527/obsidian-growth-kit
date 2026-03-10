import os
import pathlib
import subprocess


ROOT = pathlib.Path(__file__).resolve().parents[1]
INSTALL_PATH = ROOT / "install.sh"


def write_stub(path: pathlib.Path, contents: str) -> None:
    path.write_text(contents, encoding="utf-8")
    path.chmod(0o755)


def test_install_uses_home_for_config_and_bin_dirs(tmp_path):
    fake_home = tmp_path / "fake-home"
    fake_home.mkdir()
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    pip_log = tmp_path / "pip.log"

    write_stub(
        bin_dir / "python3",
        "#!/usr/bin/env bash\nexit 0\n",
    )
    write_stub(
        bin_dir / "git",
        "#!/usr/bin/env bash\nexit 0\n",
    )
    write_stub(
        bin_dir / "pip3",
        (
            "#!/usr/bin/env bash\n"
            f"printf '%s\\n' \"$*\" >> {pip_log}\n"
            "exit 0\n"
        ),
    )

    env = os.environ.copy()
    env["HOME"] = str(fake_home)
    env["PATH"] = f"{bin_dir}:{env['PATH']}"

    result = subprocess.run(
        ["bash", str(INSTALL_PATH)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert (fake_home / ".config" / "x-api").is_dir()
    assert (fake_home / ".local" / "bin").is_dir()
    assert (fake_home / ".config" / "x-api" / "keys.env").is_file()
    assert (fake_home / ".local" / "bin" / "xpost").is_file()
    assert (fake_home / ".local" / "bin" / "xqueue").is_file()
    assert not (ROOT / "~").exists()
    assert str(fake_home / ".config" / "x-api" / "keys.env") in result.stdout
