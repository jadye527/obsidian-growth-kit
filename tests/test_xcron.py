import json
import subprocess
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


def test_main_allows_subcommand_options(monkeypatch, load_tool_module):
    module = load_tool_module("xcron")
    install_calls = []

    monkeypatch.setattr(
        module,
        "install_schedule",
        lambda args, dry_run=False: install_calls.append((args, dry_run)),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["xcron", "install-schedule", "--scheduler", "crontab", "--dry-run"],
    )

    module.main()

    assert install_calls == [(["--scheduler", "crontab"], True)]


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


def test_publish_meme_post_runs_full_pipeline(
    tmp_path, monkeypatch, load_tool_module
):
    module = load_tool_module("xcron")
    commands = []
    post_file = tmp_path / "post.md"
    self_reply_file = tmp_path / "self-reply.md"
    mention_reply_file = tmp_path / "mention-reply.md"
    post_file.write_text("Main post copy\n", encoding="utf-8")
    self_reply_file.write_text("First reply with the link", encoding="utf-8")
    mention_reply_file.write_text("Appreciate the mention.", encoding="utf-8")

    def fake_run_command(args, dry_run=False):
        commands.append((args, dry_run))
        if args[:2] == ["xmeme", "generate"]:
            return "/tmp/generated-meme.png"
        if args[0:2] == ["xpost", "--text-file"]:
            return "Tweet posted: https://x.com/tester/status/111"
        if args == ["xpost", "mentions"]:
            return (
                "@alice · 2026-03-12 10:00:00+00:00\n"
                "Congrats on the launch\n"
                "♥ 4  🔁 0  💬 1  id:222\n"
                "---\n"
                "@bob · 2026-03-12 11:00:00+00:00\n"
                "Nice meme\n"
                "♥ 2  🔁 0  💬 0  id:333\n"
                "---\n"
            )
        return ""

    monkeypatch.setattr(module, "run_command", fake_run_command)

    module.run_publish_meme_post(
        [
            "--template",
            "drake.jpg",
            "--top-text",
            "Ship now",
            "--bottom-text",
            "Polish later",
            "--output-dir",
            str(tmp_path / "out"),
            "--generator",
            "~/memegen.py",
            "--python",
            "~/venv/bin/python",
            "--text-file",
            str(post_file),
            "--self-reply-file",
            str(self_reply_file),
            "--mention-reply-file",
            str(mention_reply_file),
            "--mentions-limit",
            "2",
        ]
    )

    assert commands == [
        (
            [
                "xmeme",
                "generate",
                "--template",
                "drake.jpg",
                "--top-text",
                "Ship now",
                "--output-dir",
                str(tmp_path / "out"),
                "--bottom-text",
                "Polish later",
                "--generator",
                "~/memegen.py",
                "--python",
                "~/venv/bin/python",
            ],
            False,
        ),
        (
            [
                "xpost",
                "--text-file",
                str(post_file),
                "--media",
                "/tmp/generated-meme.png",
            ],
            False,
        ),
        (
            ["xpost", "reply", "111", "First reply with the link"],
            False,
        ),
        (["xpost", "mentions"], False),
        (
            ["xpost", "reply", "222", "Appreciate the mention."],
            False,
        ),
        (
            ["xpost", "reply", "333", "Appreciate the mention."],
            False,
        ),
    ]


def test_build_crontab_text_replaces_existing_managed_block(
    monkeypatch, load_tool_module
):
    module = load_tool_module("xcron")
    monkeypatch.setattr(module, "BIN_DIR", "/tmp/bin")
    monkeypatch.setattr(module, "QUEUE_FILE", "/tmp/queue.json")
    monkeypatch.setattr(module, "KEYS_FILE", "/tmp/keys.env")

    current_crontab = (
        "MAILTO=alerts@example.com\n"
        "# BEGIN_OBSIDIAN_GROWTH_KIT_DAILY_POSTING\n"
        "CRON_TZ=America/New_York\n"
        "0 8 * * * old-command\n"
        "# END_OBSIDIAN_GROWTH_KIT_DAILY_POSTING\n"
    )

    updated = module.build_crontab_text(current_crontab)

    assert updated.count(module.CRON_BLOCK_START) == 1
    assert "MAILTO=alerts@example.com" in updated
    assert "0 9,18 * * *" in updated
    assert "old-command" not in updated
    assert updated.endswith("\n")


def test_install_schedule_prefers_systemd_and_enables_linger(
    tmp_path, monkeypatch, capsys, load_tool_module
):
    module = load_tool_module("xcron")
    systemd_dir = tmp_path / "systemd"
    systemd_dir.mkdir()
    systemctl_calls = []
    loginctl_calls = []

    monkeypatch.setattr(module, "SYSTEMD_USER_DIR", str(systemd_dir))
    monkeypatch.setattr(module, "SERVICE_FILE", str(systemd_dir / "ogk.service"))
    monkeypatch.setattr(module, "TIMER_FILE", str(systemd_dir / "ogk.timer"))
    monkeypatch.setattr(module, "SYSTEMD_LINGER_USER", "tester")
    monkeypatch.setattr(
        module.shutil,
        "which",
        lambda name: "/usr/bin/fake" if name in {"systemctl", "loginctl"} else None,
    )

    def fake_run_system_command(args, dry_run=False, input_text=None):
        del dry_run, input_text
        if args[0] == "systemctl":
            systemctl_calls.append(args)
        if args[0] == "loginctl":
            loginctl_calls.append(args)
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(module, "run_system_command", fake_run_system_command)

    module.install_schedule([])

    captured = capsys.readouterr()
    assert "systemd timer installed at 9:00 AM and 6:00 PM ET" in captured.out
    assert "user lingering enabled for reboot persistence" in captured.out
    assert systemctl_calls == [
        ["systemctl", "--user", "daemon-reload"],
        ["systemctl", "--user", "enable", "--now", "obsidian-growth-kit-post.timer"],
    ]
    assert loginctl_calls == [["loginctl", "enable-linger", "tester"]]
    assert (systemd_dir / "ogk.service").is_file()
    assert (systemd_dir / "ogk.timer").is_file()


def test_install_schedule_falls_back_to_crontab_when_systemd_fails(
    monkeypatch, capsys, load_tool_module
):
    module = load_tool_module("xcron")
    crontab_inputs = []

    monkeypatch.setattr(
        module.shutil,
        "which",
        lambda name: "/usr/bin/fake" if name in {"systemctl", "crontab"} else None,
    )

    def fake_run_system_command(args, dry_run=False, input_text=None):
        del dry_run
        if args[:3] == ["systemctl", "--user", "daemon-reload"]:
            return subprocess.CompletedProcess(args, 1, "", "systemd unavailable")
        if args == ["crontab", "-l"]:
            return subprocess.CompletedProcess(
                args,
                0,
                "MAILTO=alerts@example.com\n",
                "",
            )
        if args == ["crontab", "-"]:
            crontab_inputs.append(input_text)
            return subprocess.CompletedProcess(args, 0, "", "")
        raise AssertionError(f"Unexpected command: {args}")

    monkeypatch.setattr(module, "run_system_command", fake_run_system_command)

    module.install_schedule([])

    captured = capsys.readouterr()
    assert "crontab installed at 9:00 AM and 6:00 PM ET" in captured.out
    assert len(crontab_inputs) == 1
    assert "MAILTO=alerts@example.com" in crontab_inputs[0]
    assert "0 9,18 * * *" in crontab_inputs[0]


def test_install_schedule_requires_crontab_when_requested(
    monkeypatch, load_tool_module
):
    module = load_tool_module("xcron")
    monkeypatch.setattr(
        module.shutil,
        "which",
        lambda name: None if name == "crontab" else "/usr/bin/fake",
    )

    with pytest.raises(SystemExit) as exc_info:
        module.install_schedule(["--scheduler", "crontab"])

    assert exc_info.value.code == 1


def test_extract_mention_ids_deduplicates_numeric_ids(load_tool_module):
    module = load_tool_module("xcron")

    mention_ids = module.extract_mention_ids(
        "♥ 1  🔁 0  💬 0  id:222\n"
        "♥ 2  🔁 0  💬 0  id:333\n"
        "♥ 3  🔁 0  💬 0  id:222\n"
    )

    assert mention_ids == ["222", "333"]
