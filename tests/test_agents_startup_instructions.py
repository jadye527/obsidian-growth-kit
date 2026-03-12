import re


def test_agents_file_requires_daily_log_and_relevant_topic_review(repo_root):
    agents_path = repo_root / "AGENTS.md"

    assert agents_path.exists()

    content = agents_path.read_text(encoding="utf-8")

    assert "At the start of every new session" in content
    assert "read the current daily log in `memory/`" in content
    assert "read the relevant topic files in `memory/`" in content
    assert re.search(r"memory/YYYY-MM-DD\.md", content)
