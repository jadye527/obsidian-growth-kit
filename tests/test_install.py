import pathlib
import subprocess


def write_stub(path: pathlib.Path, contents: str) -> None:
    path.write_text(contents, encoding="utf-8")
    path.chmod(0o755)


def test_install_uses_home_for_config_and_bin_dirs(repo_root, install_env):
    install_path = repo_root / "install.sh"
    fake_home = install_env["fake_home"]
    bin_dir = install_env["bin_dir"]
    pip_log = install_env["pip_log"]

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

    result = subprocess.run(
        ["bash", str(install_path)],
        cwd=repo_root,
        env=install_env["env"],
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
    assert (fake_home / ".local" / "bin" / "xmiddleware").is_file()
    assert (fake_home / ".local" / "bin" / "xcleanup").is_file()
    assert not (repo_root / "~").exists()
    assert str(fake_home / ".config" / "x-api" / "keys.env") in result.stdout
