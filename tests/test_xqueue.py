import sys
import types

import pytest


def test_help_flag_prints_usage_examples(capsys, monkeypatch, load_tool_module):
    module = load_tool_module("xqueue")

    monkeypatch.setattr(sys, "argv", ["xqueue", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "Examples:" in captured.out
    assert 'xqueue add "Shipping one useful change at a time"' in captured.out
    assert captured.err == ""


def test_no_args_prints_help_without_loading_queue(
    capsys, monkeypatch, load_tool_module
):
    module = load_tool_module("xqueue")

    def fail_load_queue():
        raise AssertionError("load_queue should not be called for help output")

    monkeypatch.setattr(module, "load_queue", fail_load_queue)
    monkeypatch.setattr(sys, "argv", ["xqueue"])

    module.main()

    captured = capsys.readouterr()
    assert "Commands:" in captured.out
    assert captured.err == ""


def test_unknown_command_exits_with_error(monkeypatch, capsys, load_tool_module):
    module = load_tool_module("xqueue")

    monkeypatch.setattr(sys, "argv", ["xqueue", "bogus"])
    monkeypatch.setattr(module, "load_queue", lambda: {"tweets": [], "last_posted": 0})

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Unknown command: bogus" in captured.err


def test_load_queue_error_exits_with_actionable_message(
    monkeypatch, capsys, load_tool_module
):
    module = load_tool_module("xqueue")

    monkeypatch.setattr(sys, "argv", ["xqueue", "list"])
    monkeypatch.setattr(
        module,
        "load_queue",
        lambda: (_ for _ in ()).throw(
            module.QueueError("Unable to read queue file /tmp/queue.json: denied")
        ),
    )

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Queue error:" in captured.err
    assert "Unable to read queue file" in captured.err


def test_save_queue_error_on_add_exits_with_actionable_message(
    monkeypatch, capsys, load_tool_module
):
    module = load_tool_module("xqueue")

    monkeypatch.setattr(sys, "argv", ["xqueue", "add", "hello"])
    monkeypatch.setattr(module, "load_queue", lambda: {"tweets": [], "last_posted": 0})
    monkeypatch.setattr(
        module,
        "save_queue",
        lambda q: (_ for _ in ()).throw(
            module.QueueError("Unable to write queue file /tmp/queue.json: denied")
        ),
    )

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    captured = capsys.readouterr()
    assert exc_info.value.code == 1
    assert "Queue error:" in captured.err
    assert "Unable to write queue file" in captured.err


def test_next_on_empty_queue_prints_message(
    monkeypatch, capsys, load_tool_module, make_queue
):
    module = load_tool_module("xqueue")

    monkeypatch.setattr(sys, "argv", ["xqueue", "next"])
    monkeypatch.setattr(module, "load_queue", lambda: make_queue())

    module.main()

    captured = capsys.readouterr()
    assert captured.out.strip() == "Queue empty."
    assert captured.err == ""


def test_flush_on_empty_queue_prints_message(
    monkeypatch, capsys, load_tool_module, make_queue
):
    module = load_tool_module("xqueue")

    monkeypatch.setattr(sys, "argv", ["xqueue", "flush"])
    monkeypatch.setattr(module, "load_queue", lambda: make_queue())

    module.main()

    captured = capsys.readouterr()
    assert captured.out.strip() == "Queue empty."
    assert captured.err == ""


def test_add_appends_tweet_and_saves_queue(
    monkeypatch, capsys, load_tool_module, make_queue, make_queue_tweet
):
    module = load_tool_module("xqueue")
    saved_queue = {}

    monkeypatch.setattr(sys, "argv", ["xqueue", "add", "ship it"])
    monkeypatch.setattr(module, "load_queue", lambda: make_queue())
    monkeypatch.setattr(module.time, "time", lambda: 1234)

    def fake_save_queue(queue):
        saved_queue["value"] = queue

    monkeypatch.setattr(module, "save_queue", fake_save_queue)

    module.main()

    captured = capsys.readouterr()
    assert captured.out.strip() == "Queued. (1 in queue)"
    assert captured.err == ""
    assert saved_queue["value"] == make_queue(
        make_queue_tweet("ship it", 1234),
    )


def test_list_prints_numbered_queue_entries(
    monkeypatch, capsys, load_tool_module, make_queue, make_queue_tweet
):
    module = load_tool_module("xqueue")

    monkeypatch.setattr(sys, "argv", ["xqueue", "list"])
    monkeypatch.setattr(
        module,
        "load_queue",
        lambda: make_queue(
            make_queue_tweet("first queued tweet", 1),
            make_queue_tweet("second line\nwith newline", 2),
        ),
    )

    module.main()

    captured = capsys.readouterr()
    assert "1. first queued tweet..." in captured.out
    assert "2. second line with newline..." in captured.out
    assert captured.err == ""


def test_count_prints_queue_size(
    monkeypatch, capsys, load_tool_module, make_queue, make_queue_tweet
):
    module = load_tool_module("xqueue")

    monkeypatch.setattr(sys, "argv", ["xqueue", "count"])
    monkeypatch.setattr(
        module,
        "load_queue",
        lambda: make_queue(
            make_queue_tweet("a"),
            make_queue_tweet("b"),
        ),
    )

    module.main()

    captured = capsys.readouterr()
    assert captured.out.strip() == "2"
    assert captured.err == ""


def test_next_respects_cooldown(
    monkeypatch, capsys, load_tool_module, make_queue, make_queue_tweet
):
    module = load_tool_module("xqueue")

    monkeypatch.setattr(sys, "argv", ["xqueue", "next"])
    monkeypatch.setattr(module.time, "time", lambda: 1000)
    monkeypatch.setattr(
        module,
        "load_queue",
        lambda: make_queue(
            make_queue_tweet("queued tweet", 10),
            last_posted=100,
        ),
    )

    def fail_run(*args, **kwargs):
        raise AssertionError("subprocess.run should not be called during cooldown")

    monkeypatch.setattr(module.subprocess, "run", fail_run)

    module.main()

    captured = capsys.readouterr()
    assert captured.out.strip() == "Cooldown: 800s remaining"
    assert captured.err == ""


def test_flush_posts_all_tweets_and_sleeps_for_cooldown(
    monkeypatch, capsys, load_tool_module, make_queue, make_queue_tweet
):
    module = load_tool_module("xqueue")
    queue = make_queue(
        make_queue_tweet("first tweet", 1),
        make_queue_tweet("second tweet", 2),
    )
    saved_states = []
    posted_texts = []
    sleep_calls = []
    time_values = iter([1000, 1000, 1100, 2000, 2000])

    monkeypatch.setattr(sys, "argv", ["xqueue", "flush"])
    monkeypatch.setattr(module, "load_queue", lambda: queue)
    monkeypatch.setattr(module.time, "time", lambda: next(time_values))
    monkeypatch.setattr(
        module.time, "sleep", lambda seconds: sleep_calls.append(seconds)
    )

    def fake_save_queue(current_queue):
        saved_states.append(
            {
                "tweets": [tweet.copy() for tweet in current_queue["tweets"]],
                "last_posted": current_queue["last_posted"],
            }
        )

    def fake_run(args, capture_output, text, timeout):
        posted_texts.append(args[2])
        return types.SimpleNamespace(
            returncode=0,
            stdout=f"posted {args[2]}",
            stderr="",
        )

    monkeypatch.setattr(module, "save_queue", fake_save_queue)
    monkeypatch.setattr(module.subprocess, "run", fake_run)

    module.main()

    captured = capsys.readouterr()
    assert "Flushing 2 tweets (15-min intervals)..." in captured.out
    assert "[1/2] posted first tweet" in captured.out
    assert "Waiting 800s..." in captured.out
    assert "[2/2] posted second tweet" in captured.out
    assert "Done. Posted 2/2." in captured.out
    assert captured.err == ""
    assert posted_texts == ["first tweet", "second tweet"]
    assert sleep_calls == [800]
    assert saved_states == [
        {"tweets": [{"text": "second tweet", "added": 2}], "last_posted": 1000},
        {"tweets": [], "last_posted": 2000},
    ]
