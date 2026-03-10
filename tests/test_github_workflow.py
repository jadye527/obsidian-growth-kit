def test_test_workflow_runs_pytest_on_push_and_pull_request(repo_root):
    workflow_path = repo_root / ".github" / "workflows" / "test.yml"

    assert workflow_path.is_file()

    content = workflow_path.read_text(encoding="utf-8")

    assert "on:\n  push:\n  pull_request:\n" in content
    assert 'python-version: "3.10"' in content
    assert "python -m pip install -r tools/requirements.txt pytest" in content
    assert "run: pytest" in content


def test_lint_workflow_runs_ruff_on_push_and_pull_request(repo_root):
    workflow_path = repo_root / ".github" / "workflows" / "lint.yml"

    assert workflow_path.is_file()

    content = workflow_path.read_text(encoding="utf-8")

    assert "on:\n  push:\n  pull_request:\n" in content
    assert 'python-version: "3.10"' in content
    assert "python -m pip install -r tools/requirements.txt ruff" in content
    assert "run: ruff check ." in content
