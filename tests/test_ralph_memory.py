def test_ralph_memory_note_tracks_status_and_recent_work(repo_root):
    note = (repo_root / "memory" / "ralph.md").read_text(encoding="utf-8")

    assert "# Ralph Memory" in note
    assert "## Status" in note
    assert "Updated on 2026-03-12." in note
    assert "## Recent Work" in note
    assert "Read OpenClaw memory files in `xgrowth`." in note
    assert "Ensured the scheduler persists across reboots." in note
    assert "Added the scheduled autonomous post pipeline." in note
