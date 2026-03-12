def test_from_obsidian_002_is_moved_to_processed(repo_root):
    source = repo_root / "inbox" / "from-obsidian-002.md"
    processed = repo_root / "inbox" / "processed" / "from-obsidian-002.md"

    assert not source.exists()
    assert processed.exists()
