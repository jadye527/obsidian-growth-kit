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
    assert (fake_home / ".local" / "bin" / "xcron").is_file()
    assert (fake_home / ".local" / "bin" / "xmiddleware").is_file()
    assert (fake_home / ".local" / "bin" / "xcleanup").is_file()
    assert (fake_home / ".local" / "bin" / "xmeme").is_file()
    assert not (repo_root / "~").exists()
    assert str(fake_home / ".config" / "x-api" / "keys.env") in result.stdout


def test_install_configures_systemd_timer_when_available(repo_root, install_env):
    install_path = repo_root / "install.sh"
    fake_home = install_env["fake_home"]
    bin_dir = install_env["bin_dir"]
    pip_log = install_env["pip_log"]
    systemctl_log = fake_home / "systemctl.log"

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
    write_stub(
        bin_dir / "systemctl",
        (
            "#!/usr/bin/env bash\n"
            f"printf '%s\\n' \"$*\" >> {systemctl_log}\n"
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
    service_file = (
        fake_home
        / ".config"
        / "systemd"
        / "user"
        / "obsidian-growth-kit-post.service"
    )
    timer_file = (
        fake_home
        / ".config"
        / "systemd"
        / "user"
        / "obsidian-growth-kit-post.timer"
    )

    assert service_file.is_file()
    assert timer_file.is_file()
    assert "xqueue next" in service_file.read_text(encoding="utf-8")

    timer_text = timer_file.read_text(encoding="utf-8")
    assert "OnCalendar=*-*-* 09:00:00 America/New_York" in timer_text
    assert "OnCalendar=*-*-* 18:00:00 America/New_York" in timer_text
    assert "Persistent=true" in timer_text

    systemctl_calls = systemctl_log.read_text(encoding="utf-8").splitlines()
    assert "daemon-reload" in systemctl_calls
    assert "enable --now obsidian-growth-kit-post.timer" in systemctl_calls


def test_install_falls_back_to_crontab_when_systemctl_is_unavailable(
    repo_root, install_env
):
    install_path = repo_root / "install.sh"
    fake_home = install_env["fake_home"]
    bin_dir = install_env["bin_dir"]
    pip_log = install_env["pip_log"]
    crontab_store = fake_home / "crontab.txt"
    crontab_log = fake_home / "crontab.log"

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
    write_stub(
        bin_dir / "crontab",
        (
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            f"printf '%s\\n' \"$*\" >> {crontab_log}\n"
            f"store={crontab_store}\n"
            "if [ \"$#\" -eq 1 ] && [ \"$1\" = \"-l\" ]; then\n"
            "  if [ -f \"$store\" ]; then\n"
            "    cat \"$store\"\n"
            "    exit 0\n"
            "  fi\n"
            "  exit 1\n"
            "fi\n"
            "if [ \"$#\" -eq 1 ] && [ \"$1\" = \"-\" ]; then\n"
            "  cat > \"$store\"\n"
            "  exit 0\n"
            "fi\n"
            "exit 1\n"
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
    assert "crontab installed at 9:00 AM and 6:00 PM ET" in result.stdout

    crontab_text = crontab_store.read_text(encoding="utf-8")
    assert "CRON_TZ=America/New_York" in crontab_text
    assert "0 9,18 * * *" in crontab_text
    assert "xqueue next >/dev/null 2>&1" in crontab_text
    assert str(fake_home / ".config" / "x-api" / "keys.env") in crontab_text

    crontab_calls = crontab_log.read_text(encoding="utf-8").splitlines()
    assert "-l" in crontab_calls
    assert "-" in crontab_calls
