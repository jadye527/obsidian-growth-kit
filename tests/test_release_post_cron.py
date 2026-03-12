import json


def test_release_post_cron_example_targets_requested_post(repo_root):
    cron_text = (
        repo_root / "examples" / "release-post-2026-03-13.cron"
    ).read_text(encoding="utf-8")

    assert "CRON_TZ=America/New_York" in cron_text
    assert "18 9 13 3 *" in cron_text
    assert 'TODAY="$(date +\\%F)"' in cron_text
    assert '"$TODAY" = "2026-03-13"' in cron_text
    assert 'MEME_PATH="$(xmeme generate' in cron_text
    assert 'X_MEMEGEN_PATH:-$HOME/.openclaw/workspace-obsidian/out/memegen.py' in cron_text
    assert '--output-dir "$OGK_REPO_DIR/out"' in cron_text
    assert '--prefix release-post' in cron_text
    assert "x-post-release-package-2026-03-12.md" in cron_text
    assert '--media "$MEME_PATH"' in cron_text


def test_openclaw_cron_jobs_invoke_autonomous_scripts(repo_root):
    jobs_path = repo_root / "examples" / "cron-jobs.json"
    jobs = json.loads(jobs_path.read_text(encoding="utf-8"))["jobs"]

    messages = {job["id"]: job["payload"]["message"] for job in jobs}

    assert messages == {
        "x-morning-growth": "xcron morning-growth",
        "x-content-scout": "xcron content-scout",
        "x-nightly-review": "xcron nightly-review",
        "x-analytics-snapshot": "xcron analytics-snapshot",
    }
