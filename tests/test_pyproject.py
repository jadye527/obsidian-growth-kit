def test_pyproject_declares_project_metadata(repo_root):
    pyproject_text = (repo_root / "pyproject.toml").read_text(encoding="utf-8")

    assert 'name = "obsidian-growth-kit"' in pyproject_text
    assert 'version = "0.1.0"' in pyproject_text
    assert 'requires-python = ">=3.10"' in pyproject_text
    assert 'license = { text = "MIT" }' in pyproject_text


def test_pyproject_declares_runtime_and_dev_dependencies(repo_root):
    pyproject_text = (repo_root / "pyproject.toml").read_text(encoding="utf-8")

    assert '"tweepy>=4.14.0"' in pyproject_text
    assert '"asciinema>=2.4.0"' in pyproject_text
    assert '"pytest>=8.0"' in pyproject_text
    assert '"ruff>=0.11.0"' in pyproject_text


def test_pyproject_configures_pytest_and_ruff(repo_root):
    pyproject_text = (repo_root / "pyproject.toml").read_text(encoding="utf-8")

    assert "[tool.pytest.ini_options]" in pyproject_text
    assert 'testpaths = ["tests"]' in pyproject_text
    assert "[tool.ruff]" in pyproject_text
    assert 'target-version = "py310"' in pyproject_text
