def test_api_reference_lists_all_tool_sections(repo_root):
    doc = (repo_root / "docs" / "API-REFERENCE.md").read_text(encoding="utf-8")

    for heading in (
        "## `xpost`",
        "## `xqueue`",
        "## `xanalytics`",
        "## `xscout`",
        "## `xgrowth`",
        "## `xrecord`",
        "## `xmiddleware`",
    ):
        assert heading in doc


def test_api_reference_lists_every_command(repo_root):
    doc = (repo_root / "docs" / "API-REFERENCE.md").read_text(encoding="utf-8")

    commands = (
        "xpost whoami",
        'xpost tweet "text"',
        'xpost --text "text" [--media /path/to/file]',
        'xpost reply <tweet_id> "text"',
        'xpost quote <tweet_id> "text"',
        "xpost read <tweet_id>",
        "xpost user <@handle>",
        "xpost user-tweets <@handle>",
        'xpost search "query"',
        "xpost like <tweet_id>",
        "xpost unlike <tweet_id>",
        "xpost retweet <tweet_id>",
        "xpost unretweet <tweet_id>",
        "xpost delete <tweet_id>",
        "xpost mentions",
        "xpost thread <tweet_id>",
        "xpost follow <@handle>",
        "xpost unfollow <@handle>",
        "xpost followers <@handle>",
        "xpost following <@handle>",
        'xqueue add "tweet text"',
        "xqueue list",
        "xqueue flush",
        "xqueue next",
        "xqueue clear",
        "xqueue count",
        "xanalytics snapshot",
        "xanalytics top [n]",
        "xanalytics report",
        "xanalytics growth",
        "xanalytics compare",
        "xscout scan",
        "xscout scan --topic <topic>",
        "xscout viral",
        "xscout opportunities",
        "xscout report",
        "xgrowth track",
        "xgrowth report",
        "xgrowth strategy",
        'xgrowth log-strategy "name" "description" [metrics]',
        "xgrowth new-strategy",
        "xgrowth leaderboard",
        "xrecord demo [name]",
        "xrecord snapshot",
        "xrecord session [name] [sec]",
        "xrecord list",
        "xrecord upload <name>",
        "xrecord svg <name>",
        "xmiddleware login --login-url <url> --username <username> --password <password>",
    )

    for command in commands:
        assert f"`{command}`" in doc
