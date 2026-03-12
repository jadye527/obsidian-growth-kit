def test_release_post_cron_example_targets_requested_post(repo_root):
    cron_text = (
        repo_root / "examples" / "release-post-2026-03-13.cron"
    ).read_text(encoding="utf-8")

    assert "CRON_TZ=America/New_York" in cron_text
    assert "18 9 13 3 *" in cron_text
    assert 'TODAY="$(date +\\%F)"' in cron_text
    assert '"$TODAY" = "2026-03-13"' in cron_text
    assert "x-post-release-package-2026-03-12.md" in cron_text
    assert "out/charlie_fire_v1d.png" in cron_text
